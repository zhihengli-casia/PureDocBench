"""Dolphin-v2 two-stage inference on PureDocBench with cross-page vLLM batching.

Same semantics as dolphin_v2_vllm_infer.py (per official demo_page.py), but
batches Stage 1 over N pages at once, then batches Stage 2 within the chunk
across all crops of each type. Designed to saturate vLLM throughput at TP=4.

Project defaults write final Markdown directly to predictions/dolphin_v2;
--smoke writes to outputs_smoke/dolphin_v2/predictions.
"""

import argparse
import json
import os
import sys
import time
import traceback
from collections import defaultdict

from PIL import Image

sys.path.insert(0, "${PDB_REPOS_ROOT}/Dolphin")
from utils.utils import (  # noqa: E402
    check_bbox_overlap,
    parse_layout_string,
    process_coordinates,
    resize_img,
    save_figure_to_local,
)
from utils.markdown_utils import MarkdownConverter  # noqa: E402

from transformers import AutoProcessor  # noqa: E402
from vllm import LLM, SamplingParams  # noqa: E402

STAGE1_PROMPT = "Parse the reading order of this document."
STAGE2_PROMPTS = {
    "tab": "Parse the table in the image.",
    "equ": "Read formula in the image.",
    "code": "Read code in the image.",
    "text": "Read text in the image.",
}

# Qwen2.5-VL processor rejects crops whose aspect ratio exceeds ~200; stay
# well below that. Typical offenders: header/divider rules detected as tall
# text boxes (e.g. 7840x28). Such crops are dropped (text left empty).
MAX_ASPECT_RATIO = 100


def build_prompt(processor, user_text):
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image"},
                {"type": "text", "text": user_text},
            ],
        }
    ]
    return processor.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )


def vllm_generate(llm, processor, sampling_params, items):
    if not items:
        return []
    batch_inputs = []
    for pil_img, text in items:
        img = resize_img(pil_img)
        batch_inputs.append(
            {
                "prompt": build_prompt(processor, text),
                "multi_modal_data": {"image": img},
            }
        )
    outputs = llm.generate(batch_inputs, sampling_params=sampling_params, use_tqdm=False)
    return [o.outputs[0].text for o in outputs]


def parse_page_elements(layout_text, pil_image, save_dir, stem):
    """Run Stage 1 parse for a single page. Returns (figure_results, grouped).

    grouped: dict[bucket] -> list of dict with keys: crop, label, bbox, reading_order, tags.
    """
    layout_list = parse_layout_string(layout_text)
    if not layout_list or not (
        layout_text.startswith("[") and layout_text.endswith("]")
    ):
        layout_list = [([0, 0, *pil_image.size], "distorted_page", [])]
    elif len(layout_list) > 1 and check_bbox_overlap(layout_list, pil_image):
        layout_list = [([0, 0, *pil_image.size], "distorted_page", [])]

    grouped = defaultdict(list)
    figure_results = []
    reading_order = 0
    for bbox, label, tags in layout_list:
        try:
            if label == "distorted_page":
                x1, y1, x2, y2 = 0, 0, *pil_image.size
                pil_crop = pil_image
            else:
                x1, y1, x2, y2 = process_coordinates(bbox, pil_image)
                pil_crop = pil_image.crop((x1, y1, x2, y2))

            cw, ch = pil_crop.size
            if cw > 3 and ch > 3 and max(cw / ch, ch / cw) <= MAX_ASPECT_RATIO:
                if label == "fig":
                    fig_name = save_figure_to_local(
                        pil_crop, save_dir, stem, reading_order
                    )
                    figure_results.append(
                        {
                            "label": label,
                            "text": f"![Figure](figures/{fig_name})",
                            "figure_path": f"figures/{fig_name}",
                            "bbox": [x1, y1, x2, y2],
                            "reading_order": reading_order,
                            "tags": tags,
                        }
                    )
                else:
                    bucket = label if label in STAGE2_PROMPTS else "text"
                    grouped[bucket].append(
                        {
                            "crop": pil_crop,
                            "label": label,
                            "bbox": [x1, y1, x2, y2],
                            "reading_order": reading_order,
                            "tags": tags,
                        }
                    )
            reading_order += 1
        except Exception as exc:
            print(f"[{stem}] bbox error label={label}: {exc}", flush=True)
            continue
    return figure_results, grouped


def process_chunk(chunk_rels, image_root, save_dir, pred_dir, json_dir,
                  llm, processor, sp_stage1, sp_stage2, md_conv):
    """Process one chunk of N pages. Writes md + json per page. Returns (ok, err)."""
    # Load images for this chunk.
    loaded = []  # list of (rel, stem, pil_image)
    for rel in chunk_rels:
        try:
            img = Image.open(os.path.join(image_root, rel)).convert("RGB")
            stem = os.path.splitext(os.path.basename(rel))[0]
            loaded.append((rel, stem, img))
        except Exception as exc:
            print(f"[load-error] {rel}: {exc}", flush=True)

    if not loaded:
        return 0, len(chunk_rels)

    # Stage 1 batch.
    stage1_items = [(img, STAGE1_PROMPT) for (_, _, img) in loaded]
    layouts = vllm_generate(llm, processor, sp_stage1, stage1_items)

    # Parse each page, collect figures and bucket non-fig elements by type.
    per_page_recognition = [[] for _ in loaded]  # index matches loaded order
    type_buckets = defaultdict(list)  # bucket -> list of (page_idx_in_chunk, elem)
    for page_idx, ((_, stem, img), layout_text) in enumerate(zip(loaded, layouts)):
        fig_results, grouped = parse_page_elements(layout_text, img, save_dir, stem)
        per_page_recognition[page_idx].extend(fig_results)
        for bucket, elems in grouped.items():
            for elem in elems:
                type_buckets[bucket].append((page_idx, elem))

    # Stage 2 batches per type, across all pages in this chunk.
    for bucket, entries in type_buckets.items():
        if not entries:
            continue
        prompt = STAGE2_PROMPTS[bucket]
        items = [(e["crop"], prompt) for (_, e) in entries]
        texts = vllm_generate(llm, processor, sp_stage2, items)
        for (page_idx, elem), txt in zip(entries, texts):
            per_page_recognition[page_idx].append(
                {
                    "label": elem["label"],
                    "bbox": elem["bbox"],
                    "text": txt.strip(),
                    "reading_order": elem["reading_order"],
                    "tags": elem["tags"],
                }
            )

    # Save per-page outputs.
    ok = 0
    err = 0
    for page_idx, (rel, stem, _img) in enumerate(loaded):
        try:
            recog = per_page_recognition[page_idx]
            recog.sort(key=lambda x: x.get("reading_order", 0))
            md_text = md_conv.convert(recog)
            with open(os.path.join(pred_dir, f"{stem}.md"), "w", encoding="utf-8") as f:
                f.write(md_text)
            with open(os.path.join(json_dir, f"{stem}.json"), "w", encoding="utf-8") as f:
                json.dump(recog, f, ensure_ascii=False, indent=2, default=str)
            ok += 1
        except Exception as exc:
            err += 1
            print(f"[save-error] {rel}: {exc}", flush=True)
            traceback.print_exc()
    return ok, err


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model-path", default="${PDB_MODEL_ROOT}/Dolphin-v2")
    p.add_argument("--image-root", default="${PDB_DATASET_ROOT}/images/clean")
    p.add_argument(
        "--image-list", default="${PDB_IMAGE_LIST_ROOT}/image_list_pdb.txt"
    )
    p.add_argument("--save-dir", default="${PDB_SUPPLEMENTAL_ROOT}/.cache/dolphin_v2")
    p.add_argument("--pred-dir", default="${PDB_SUPPLEMENTAL_ROOT}/predictions/dolphin_v2",
                   help="directory for final per-page Markdown files")
    p.add_argument("--tensor-parallel-size", type=int, default=4)
    p.add_argument("--gpu-memory-utilization", type=float, default=0.85)
    p.add_argument("--max-model-len", type=int, default=16384)
    p.add_argument("--max-pixels", type=int, default=2560000)
    p.add_argument("--min-pixels", type=int, default=784)
    p.add_argument("--chunk", type=int, default=32,
                   help="pages per chunk for Stage 1 batch; Stage 2 batches across the chunk")
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--start", type=int, default=0)
    p.add_argument("--smoke", action="store_true", help="write a small run to outputs_smoke/dolphin_v2")
    p.add_argument("--n", type=int, default=5, help="number of pages for --smoke")
    p.add_argument("--post-process", action="store_true")
    args = p.parse_args()

    if args.smoke:
        args.limit = args.n
        args.save_dir = "${PDB_SUPPLEMENTAL_ROOT}/outputs_smoke/dolphin_v2"
        args.pred_dir = os.path.join(args.save_dir, "predictions")

    pred_dir = args.pred_dir
    fig_dir = os.path.join(args.save_dir, "markdown", "figures")
    json_dir = os.path.join(args.save_dir, "output_json")
    os.makedirs(pred_dir, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(json_dir, exist_ok=True)

    with open(args.image_list) as f:
        rels = [ln.strip() for ln in f if ln.strip()]
    if args.start:
        rels = rels[args.start:]
    if args.limit and args.limit > 0:
        rels = rels[: args.limit]
    total_before = len(rels)
    done_stems = {
        os.path.splitext(fn)[0]
        for fn in os.listdir(pred_dir)
        if fn.endswith(".md")
    }
    rels = [r for r in rels if os.path.splitext(os.path.basename(r))[0] not in done_stems]
    skipped = total_before - len(rels)
    print(
        f"[dolphin-v2-fast] images to process: {len(rels)} chunk={args.chunk} "
        f"(skipped {skipped} already done in {pred_dir})",
        flush=True,
    )

    processor = AutoProcessor.from_pretrained(args.model_path)

    llm = LLM(
        model=args.model_path,
        tensor_parallel_size=args.tensor_parallel_size,
        dtype="bfloat16",
        trust_remote_code=True,
        gpu_memory_utilization=args.gpu_memory_utilization,
        max_model_len=args.max_model_len,
        limit_mm_per_prompt={"image": 1},
        mm_processor_kwargs={
            "max_pixels": args.max_pixels,
            "min_pixels": args.min_pixels,
        },
    )
    sp_stage1 = SamplingParams(temperature=0.0, max_tokens=4096)
    sp_stage2 = SamplingParams(temperature=0.0, max_tokens=4096)
    md_conv = MarkdownConverter(post_process=args.post_process)

    t_start = time.time()
    total_ok = 0
    total_err = 0
    n = len(rels)
    for chunk_start in range(0, n, args.chunk):
        chunk_rels = rels[chunk_start: chunk_start + args.chunk]
        t0 = time.time()
        ok, err = process_chunk(
            chunk_rels, args.image_root, args.save_dir, pred_dir, json_dir,
            llm, processor, sp_stage1, sp_stage2, md_conv,
        )
        total_ok += ok
        total_err += err
        dt_chunk = time.time() - t0
        done = chunk_start + len(chunk_rels)
        dt_total = time.time() - t_start
        rate = done / max(dt_total, 1e-6)
        eta = (n - done) / max(rate, 1e-6)
        print(
            f"[chunk {chunk_start // args.chunk + 1}] {done}/{n} "
            f"ok={total_ok} err={total_err} "
            f"chunk_time={dt_chunk:.1f}s rate={rate:.3f} pages/s "
            f"eta={eta / 60:.1f}min",
            flush=True,
        )

    print(
        f"[dolphin-v2-fast] DONE ok={total_ok} err={total_err} "
        f"total_time={time.time() - t_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
