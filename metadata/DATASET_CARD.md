# PureDocBench Dataset Card

## Dataset Summary

PureDocBench is a source-driven document parsing benchmark. It contains
1,475 annotated pages across 10 practical document domains and 66 fine-grained
subcategories. Each page has three aligned image tracks: clean HTML render,
digitally degraded image, and real-degraded image, for 4,425 official
evaluation images.

The benchmark evaluates OCR and document parsing systems on text recovery,
table structure, formula extraction, and reading order under layout complexity
and visual degradation.

## Intended Uses

- Benchmarking OCR and document parsing systems.
- Evaluating robustness across clean, digital-degraded, and real-degraded
  document images.
- Studying table-heavy, form-heavy, multilingual, and structured document
  parsing failures.
- Reproducing the PureDocBench evaluation protocol.

## Out-Of-Scope Uses

- Training models to identify real people or institutions.
- Making decisions about real individuals, finances, healthcare, legal status,
  education, employment, or benefits.
- Treating synthetic document content as factual records.
- Evaluating privacy leakage in real-world corpora.

## Composition

- Pages: 1,475
- Official images: 4,425
- Top-level domains: 10
- Fine-grained subcategories: 66
- Tracks: clean render, digital degradation, real degradation
- Languages: Chinese, English, and Chinese-English mixed content
- Main annotation types: text blocks, titles, tables, table captions, formulas,
  figure captions, code, references, headers, footers, page numbers

Domain counts:

- 01_academic: 180
- 02_education: 138
- 03_legal_gov: 151
- 04_business: 160
- 05_finance: 212
- 06_medical: 200
- 07_publishing: 100
- 08_technical: 110
- 09_logistics: 120
- 10_certificate: 104

## Data Collection And Generation

The dataset is synthetically generated rather than scraped from existing
documents. HTML/CSS sources are generated from document-type prompts and
rendered into document images. Ground-truth annotations are extracted from the
same structured source and checked against the rendered document assets.

The real-degraded track is created by applying controlled physical or capture
conditions to the document images, including screen capture, phone capture,
creased paper, bent paper, photocopy, flash, shadow, and low-light conditions.

## Annotation Protocol

Annotations are source-driven and page-level. Each official page includes a GT
JSON file with layout/content elements and a corresponding HTML source file.
The annotation schema covers text, titles, tables, formulas, captions, code,
references, and reading order metadata.

Quality checks include:

- 1,475/1,475 official GT files present.
- 1,475/1,475 corresponding HTML files present.
- 1,475/1,475 clean image paths valid.
- 1,475/1,475 digital-degraded images present.
- 1,475/1,475 real-degraded assignments present.
- 1,475/1,475 GT files have valid `anno_id` sequences.
- 1,475/1,475 GT files pass reading-order checks.

## Personal And Sensitive Information

PureDocBench does not contain documents collected from real people. The
document content is synthetic. Some templates imitate realistic domains such as
finance, medical, legal/government, logistics, and certificates, and may contain
fictional names, addresses, IDs, invoice numbers, diagnoses, or other
record-like fields. These fields should not be interpreted as real personal
data.

## Biases And Limitations

- The dataset is synthetic and may not capture all visual, linguistic, legal,
  institutional, or cultural variability of real documents.
- Domain coverage is broad but finite: 10 domains and 66 subcategories.
- Document styles may reflect the prompt design, rendering engine, fonts, and
  generation templates used during construction.
- Although real-degraded images introduce physical and capture artifacts, they
  are still paired with synthetic underlying documents.
- The benchmark emphasizes OCR/document parsing and should not be used as a
  measure of real-world decision quality in sensitive domains.

## Maintenance

The public release is versioned as `puredocbench-v1.0`. Any later
correction should be released as a new version with a changelog, manifest diff,
and updated Croissant metadata.

Primary hosting:

- Hugging Face: https://huggingface.co/datasets/zhihengli-casia/puredocbench
- GitHub: https://github.com/zhihengli-casia/PureDocBench
- Paper: https://arxiv.org/abs/2605.07492

## License

PureDocBench dataset assets are released under CC BY 4.0. See `LICENSE` for
details.

## Citation

```bibtex
@article{li2026puredocbench,
  title   = {How Far Is Document Parsing from Solved? PureDocBench: A Source-Traceable Benchmark across Clean, Degraded, and Real-World Settings},
  author  = {Li, Zhiheng and Ma, Zongyang and Chen, Jiaxian and Zhang, Jianing and Su, Zhaolong and Zhang, Yutong and Yu, Zhiyin and Liu, Ruiqi and Lv, Xiaolei and Li, Bo and Gao, Jun and Zhang, Ziqi and Yuan, Chunfeng and Li, Bing and Hu, Weiming},
  journal = {arXiv preprint arXiv:2605.07492},
  year    = {2026},
  doi     = {10.48550/arXiv.2605.07492},
  url     = {https://arxiv.org/abs/2605.07492}
}
```
