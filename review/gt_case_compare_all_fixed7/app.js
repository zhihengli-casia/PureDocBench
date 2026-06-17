
const DATA = window.REVIEW_DATA;
const INTERNAL_VERSION = DATA.meta?.build_token || DATA.meta?.created_at || `${DATA.meta?.case_count || 0}-${DATA.meta?.total_items || 0}`;
const PUBLIC_VERSION = DATA.meta?.public_annotation_version || DATA.meta?.annotation_version || INTERNAL_VERSION;
const PUBLIC_VERSION_LABEL = DATA.meta?.public_annotation_version_label || PUBLIC_VERSION;
const STORAGE_VERSION = INTERNAL_VERSION;
const STORAGE_KEY = `pdbFullGtCaseCompare1475:${STORAGE_VERSION}`;
const CORRECTION_SCHEMA_VERSION = "puredocbench-annotation-correction-patch-v1";
const URL_PARAMS = new URLSearchParams(window.location.search);
const PUBLIC_IMAGE_BASE = URL_PARAMS.get("imageBase") || DATA.meta?.public_image_base_url || "";
const IS_LOCAL_APP = window.location.protocol === "file:" || ["", "localhost", "127.0.0.1", "::1"].includes(window.location.hostname);
const USE_LOCAL_IMAGES = URL_PARAMS.get("localImages") === "1" || (IS_LOCAL_APP && !URL_PARAMS.get("imageBase"));
const IMAGE_PATH_PREFIX = "assets/images/";
const LOCAL_IMAGE_MARKERS = ["assets/images/", "images/clean/", "clean/"];
let caseIndex = 0;
let selectedId = null;
let activeCategories = new Set();
let activeTypes = new Set();
let query = "";
let review = JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
let suppressNextBoxClick = false;
let boxEdit = null;
let localImageFiles = new Map();
let localImageUrls = new Map();

const $ = (id) => document.getElementById(id);

function keyFor(pageId, annoKey) {
  return `${pageId}::${annoKey}`;
}

function encodePathSegments(path) {
  return path.split("/").map((part) => encodeURIComponent(part)).join("/");
}

function imageRelativePath(src) {
  return src?.startsWith(IMAGE_PATH_PREFIX) ? src.slice(IMAGE_PATH_PREFIX.length) : src;
}

function localImageCandidates(src) {
  const rel = imageRelativePath(src);
  const filename = rel?.split("/").pop();
  return [rel, src, `clean/${rel}`, `images/clean/${rel}`, `${IMAGE_PATH_PREFIX}${rel}`, filename].filter(Boolean);
}

function localImageObjectUrl(src) {
  for (const key of localImageCandidates(src)) {
    const file = localImageFiles.get(key);
    if (!file) continue;
    if (!localImageUrls.has(key)) {
      localImageUrls.set(key, URL.createObjectURL(file));
    }
    return localImageUrls.get(key);
  }
  return "";
}

function resolveImageSrc(src) {
  if (!src || /^(https?:|data:|blob:)/.test(src)) return src;
  const localSrc = localImageObjectUrl(src);
  if (localSrc) return localSrc;
  if (USE_LOCAL_IMAGES) return src;
  if (src.startsWith(IMAGE_PATH_PREFIX)) {
    if (!PUBLIC_IMAGE_BASE) return src;
    const base = PUBLIC_IMAGE_BASE.replace(/\/$/, "");
    return `${base}/${encodePathSegments(src.slice(IMAGE_PATH_PREFIX.length))}`;
  }
  return src;
}

function indexLocalImage(file, path) {
  const normalized = path.replace(/\\/g, "/").replace(/^\/+/, "");
  const aliases = new Set([normalized, file.name]);
  LOCAL_IMAGE_MARKERS.forEach((marker) => {
    const markerIndex = normalized.indexOf(marker);
    if (markerIndex >= 0) {
      aliases.add(normalized.slice(markerIndex + marker.length));
      aliases.add(normalized.slice(markerIndex));
    }
  });
  aliases.forEach((alias) => localImageFiles.set(alias, file));
}

function setLocalImages(fileList) {
  localImageUrls.forEach((url) => URL.revokeObjectURL(url));
  localImageFiles = new Map();
  localImageUrls = new Map();
  Array.from(fileList || [])
    .filter((file) => file.type.startsWith("image/") || /\.(png|jpe?g|webp)$/i.test(file.name))
    .forEach((file) => indexLocalImage(file, file.webkitRelativePath || file.name));
  updateImageSourceStatus();
  renderViewer();
}

function updateImageSourceStatus() {
  const status = $("imageSourceStatus");
  if (!status) return;
  const uniqueCount = new Set(localImageFiles.values()).size;
  if (uniqueCount) {
    status.textContent = `Images loaded: ${uniqueCount}`;
  } else if (USE_LOCAL_IMAGES) {
    status.textContent = "Images: not loaded";
  } else if (PUBLIC_IMAGE_BASE) {
    status.textContent = "Images: imageBase";
  } else {
    status.textContent = "Images: not loaded";
  }
}

function caseKey(item) {
  return keyFor(item.page_id, "__case__");
}

function bboxToPoly(bbox) {
  const [x0, y0, x1, y1] = bbox.map((value) => Math.round(value));
  return [x0, y0, x1, y0, x1, y1, x0, y1];
}

function sameBbox(left, right) {
  return validBbox(left) &&
    validBbox(right) &&
    left.map(Number).every((value, index) => Math.round(value) === Math.round(Number(right[index])));
}

function validBbox(value) {
  return Array.isArray(value) &&
    value.length === 4 &&
    value.every((part) => Number.isFinite(Number(part))) &&
    Number(value[2]) > Number(value[0]) &&
    Number(value[3]) > Number(value[1]);
}

function saveReview() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(review));
}

function currentCase() {
  return DATA.cases[caseIndex];
}

function annoKey(anno) {
  return String(anno.anno_id ?? anno.index);
}

function displayBbox(item, anno) {
  const entry = review[keyFor(item.page_id, annoKey(anno))];
  const edited = entry?.bbox_version === STORAGE_VERSION ? entry?.bbox : null;
  return validBbox(edited) ? edited.map(Number) : anno.bbox;
}

function annosWithBoxes(item) {
  return item.annotations.filter((anno) => validBbox(displayBbox(item, anno)));
}

function selectedAnno() {
  const item = currentCase();
  return item.annotations.find((anno) => annoKey(anno) === String(selectedId)) || item.annotations[0];
}

function annoStatus(item, anno) {
  return review[keyFor(item.page_id, annoKey(anno))]?.status || "";
}

function statusClass(status) {
  return status ? `status-${status}` : "";
}

function caseStatus(item) {
  if (review[caseKey(item)]?.status === "ok") return "ok";
  const statuses = item.annotations.map((anno) => annoStatus(item, anno)).filter(Boolean);
  if (!statuses.length) return "";
  if (statuses.includes("problem")) return "problem";
  if (statuses.includes("unsure")) return "unsure";
  if (statuses.length === item.annotations.length && statuses.every((status) => status === "ok")) return "ok";
  return "unsure";
}

function caseIsOpen(item) {
  if (review[caseKey(item)]?.status === "ok") return false;
  return item.annotations.some((anno) => !annoStatus(item, anno));
}

function matchesQuery(item) {
  if (!query) return true;
  const q = query.toLowerCase();
  return (
    item.page_id.toLowerCase().includes(q) ||
    item.category.toLowerCase().includes(q) ||
    item.subcategory.toLowerCase().includes(q) ||
    item.annotations.some((anno) => `${anno.category_type} ${anno.text}`.toLowerCase().includes(q))
  );
}

function visibleCases() {
  return DATA.cases.filter((item) =>
    activeCategories.has(item.category) &&
    matchesQuery(item)
  );
}

function visibleAnnos(item) {
  const problemOnly = $("showProblemOnly")?.checked;
  return item.annotations.filter((anno) => {
    if (!activeTypes.has(anno.category_type)) return false;
    if (problemOnly && anno.quality === "ok" && annoStatus(item, anno) !== "problem") return false;
    return true;
  });
}

function renderSummary() {
  $("summary").textContent = `${DATA.cases.length} cases · ${DATA.meta.total_items} annotations · ${DATA.meta.items_with_bbox} boxed · ${DATA.meta.items_unmatched} no bbox`;
  $("dataVersion").textContent = `Release: ${PUBLIC_VERSION_LABEL}`;
  $("dataVersion").title = PUBLIC_VERSION_LABEL;
}

function renderFilters() {
  const root = $("categoryFilters");
  const categories = Object.keys(DATA.meta.category_counts).sort();
  if (!activeCategories.size) categories.forEach((category) => activeCategories.add(category));
  root.innerHTML = "";
  categories.forEach((category) => {
    const label = document.createElement("label");
    label.className = "filter-chip";
    const input = document.createElement("input");
    input.type = "checkbox";
    input.checked = activeCategories.has(category);
    input.addEventListener("change", () => {
      input.checked ? activeCategories.add(category) : activeCategories.delete(category);
      renderCaseList();
      if (!visibleCases().includes(currentCase())) {
        const first = visibleCases()[0];
        if (first) setCase(first.index);
      }
    });
    label.append(input, document.createTextNode(`${category.replace(/^\d+_/, "")} ${DATA.meta.category_counts[category]}`));
    root.append(label);
  });
}

function renderTypeFilters() {
  const root = $("typeFilters");
  if (!root) return;
  const types = Object.keys(DATA.meta.type_counts).sort();
  if (!activeTypes.size) types.forEach((type) => activeTypes.add(type));
  root.innerHTML = "";
  types.forEach((type) => {
    const label = document.createElement("label");
    label.className = "filter-chip";
    const input = document.createElement("input");
    input.type = "checkbox";
    input.checked = activeTypes.has(type);
    input.addEventListener("change", () => {
      input.checked ? activeTypes.add(type) : activeTypes.delete(type);
      renderViewer();
      renderAnnoList();
    });
    label.append(input, document.createTextNode(`${type} ${DATA.meta.type_counts[type]}`));
    root.append(label);
  });
}

function renderCaseList() {
  const root = $("caseList");
  root.innerHTML = "";
  visibleCases().forEach((item) => {
    const dataIndex = DATA.cases.indexOf(item);
    const button = document.createElement("button");
    button.className = `case-row ${dataIndex === caseIndex ? "active" : ""}`;
    button.type = "button";
    button.addEventListener("click", () => setCase(dataIndex));

    const top = document.createElement("div");
    top.className = "case-name";
    const name = document.createElement("strong");
    name.textContent = item.page_id.split("/").pop();
    top.append(name);

    const meta = document.createElement("div");
    meta.className = "case-meta";
    const category = item.category.replace(/^\d+_/, "");
    const subcategory = item.subcategory.replace(/^\d+_/, "");
    meta.textContent = `${category} / ${subcategory} · ${item.items_with_bbox}/${item.items_total} boxed · ${item.items_unmatched} no bbox`;
    button.append(top, meta);
    root.append(button);
  });
}

function setCase(index) {
  caseIndex = Math.max(0, Math.min(index, DATA.cases.length - 1));
  const firstWithBox = currentCase().annotations.find((anno) => validBbox(anno.bbox));
  selectedId = annoKey(firstWithBox || currentCase().annotations[0] || { index: 0 });
  renderAll();
}

function stepVisibleCase(delta) {
  const cases = visibleCases();
  if (!cases.length) return;
  const currentVisibleIndex = cases.findIndex((item) => item.index === caseIndex);
  const base = currentVisibleIndex >= 0 ? currentVisibleIndex : 0;
  const next = cases[Math.max(0, Math.min(cases.length - 1, base + delta))];
  if (next) setCase(next.index);
}

function setSelected(annoId) {
  selectedId = String(annoId);
  renderViewer();
  renderDetails();
  renderAnnoList();
}

function qualityClass(anno) {
  if (anno.quality === "unmatched") return "unmatched";
  if (anno.quality === "low_similarity") return "low";
  return "";
}

function renderViewer() {
  const item = currentCase();
  $("caseTitle").textContent = `${item.index + 1}. ${item.page_id}`;
  const stage = $("stage");
  const zoom = Number($("zoom").value) / 100;
  const baseWidth = Math.min(item.width, 1000);
  stage.style.width = `${Math.round(baseWidth * zoom)}px`;
  stage.style.height = `${Math.round(baseWidth * item.height / item.width * zoom)}px`;

  const img = $("pageImage");
  const svg = $("overlay");
  const imageWarning = $("imageWarning");
  const setImageLoaded = (loaded) => {
    stage.classList.toggle("image-missing", !loaded);
    img.hidden = !loaded;
    svg.hidden = !loaded;
    svg.style.display = loaded ? "" : "none";
    if (imageWarning) imageWarning.hidden = loaded;
  };
  setImageLoaded(false);
  img.onload = () => {
    setImageLoaded(true);
  };
  img.onerror = () => {
    setImageLoaded(false);
  };
  const resolvedSrc = resolveImageSrc(item.image);
  img.src = resolvedSrc;
  if (img.complete && img.naturalWidth > 0) setImageLoaded(true);
  img.width = item.width;
  img.height = item.height;

  svg.setAttribute("viewBox", `0 0 ${item.width} ${item.height}`);
  svg.innerHTML = "";
  const showLabels = $("showLabels").checked;
  const selectedOnly = $("showOnlySelected")?.checked || false;
  const coverBoxes = $("coverBoxes")?.checked || false;

  visibleAnnos(item).forEach((anno) => {
    const isSelected = annoKey(anno) === String(selectedId);
    if (selectedOnly && !isSelected) return;
    const bbox = displayBbox(item, anno);
    if (!validBbox(bbox)) return;
    const box = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    box.setAttribute("x", bbox[0]);
    box.setAttribute("y", bbox[1]);
    box.setAttribute("width", bbox[2] - bbox[0]);
    box.setAttribute("height", bbox[3] - bbox[1]);
    box.setAttribute("class", `box ${qualityClass(anno)} ${coverBoxes ? "cover" : ""} ${isSelected ? "selected" : ""}`);
    box.dataset.annoId = annoKey(anno);
    if (!isSelected && selectedId !== null) box.classList.add("dimmed");
    box.addEventListener("pointerdown", (event) => startBoxEdit(event, anno, "move"));
    box.addEventListener("click", (event) => {
      if (suppressNextBoxClick) {
        suppressNextBoxClick = false;
        event.preventDefault();
        return;
      }
      setSelected(annoKey(anno));
    });
    svg.append(box);

    if (isSelected) renderResizeHandles(svg, bbox, anno);
    if (showLabels) {
      const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
      label.setAttribute("x", bbox[0] + 4);
      label.setAttribute("y", Math.max(22, bbox[1] - 6));
      label.setAttribute("class", "box-label");
      label.textContent = `#${anno.index}`;
      svg.append(label);
    }
  });
}

function handlePoints(bbox) {
  const [x0, y0, x1, y1] = bbox;
  const xm = (x0 + x1) / 2;
  const ym = (y0 + y1) / 2;
  return [
    ["nw", x0, y0], ["n", xm, y0], ["ne", x1, y0],
    ["e", x1, ym], ["se", x1, y1], ["s", xm, y1],
    ["sw", x0, y1], ["w", x0, ym]
  ];
}

function renderResizeHandles(svg, bbox, anno) {
  handlePoints(bbox).forEach(([handle, x, y]) => {
    const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    rect.setAttribute("x", x - 5);
    rect.setAttribute("y", y - 5);
    rect.setAttribute("width", 10);
    rect.setAttribute("height", 10);
    rect.setAttribute("class", "resize-handle");
    rect.dataset.annoId = annoKey(anno);
    rect.dataset.handle = handle;
    rect.addEventListener("pointerdown", (event) => startBoxEdit(event, anno, "resize", handle));
    svg.append(rect);
  });
}

function svgPoint(event) {
  const svg = $("overlay");
  const point = svg.createSVGPoint();
  point.x = event.clientX;
  point.y = event.clientY;
  const matrix = svg.getScreenCTM();
  if (!matrix) return { x: 0, y: 0 };
  const out = point.matrixTransform(matrix.inverse());
  return { x: out.x, y: out.y };
}

function clampBbox(bbox, item) {
  let [x0, y0, x1, y1] = bbox.map(Number);
  x0 = Math.max(0, Math.min(item.width, x0));
  y0 = Math.max(0, Math.min(item.height, y0));
  x1 = Math.max(0, Math.min(item.width, x1));
  y1 = Math.max(0, Math.min(item.height, y1));
  if (x1 < x0) [x0, x1] = [x1, x0];
  if (y1 < y0) [y0, y1] = [y1, y0];
  const minSize = 4;
  if (x1 - x0 < minSize) x1 = Math.min(item.width, x0 + minSize);
  if (y1 - y0 < minSize) y1 = Math.min(item.height, y0 + minSize);
  return [Math.round(x0), Math.round(y0), Math.round(x1), Math.round(y1)];
}

function setEditedBbox(item, anno, bbox) {
  const key = keyFor(item.page_id, annoKey(anno));
  const noteInput = $("noteInput");
  review[key] = {
    ...(review[key] || {}),
    bbox,
    poly: bboxToPoly(bbox),
    bbox_version: STORAGE_VERSION,
    note: noteInput?.value || review[key]?.note || ""
  };
  saveReview();
}

function updateBoxElements(annoId, bbox) {
  const box = document.querySelector(`.box[data-anno-id="${CSS.escape(String(annoId))}"]`);
  if (box) {
    box.setAttribute("x", bbox[0]);
    box.setAttribute("y", bbox[1]);
    box.setAttribute("width", bbox[2] - bbox[0]);
    box.setAttribute("height", bbox[3] - bbox[1]);
  }
  document.querySelectorAll(`.resize-handle[data-anno-id="${CSS.escape(String(annoId))}"]`).forEach((node) => node.remove());
  const anno = currentCase().annotations.find((item) => annoKey(item) === String(annoId));
  if (anno && String(selectedId) === String(annoId)) {
    renderResizeHandles($("overlay"), bbox, anno);
  }
  const bboxNode = $("selectedDetails").querySelector("[data-bbox]");
  if (bboxNode && String(selectedId) === String(annoId)) {
    bboxNode.textContent = `[${bbox.join(", ")}]`;
  }
}

function startBoxEdit(event, anno, mode, handle = null) {
  if (event.button !== 0) return;
  const item = currentCase();
  selectedId = annoKey(anno);
  renderDetails();
  renderAnnoList();
  boxEdit = {
    anno,
    item,
    mode,
    handle,
    pointerId: event.pointerId,
    start: svgPoint(event),
    bbox: displayBbox(item, anno),
    moved: false
  };
  $("overlay").setPointerCapture?.(event.pointerId);
  event.preventDefault();
  event.stopPropagation();
}

function updateBoxEdit(event) {
  if (!boxEdit || boxEdit.pointerId !== event.pointerId) return;
  const point = svgPoint(event);
  const dx = point.x - boxEdit.start.x;
  const dy = point.y - boxEdit.start.y;
  let [x0, y0, x1, y1] = boxEdit.bbox;
  if (boxEdit.mode === "move") {
    x0 += dx; x1 += dx; y0 += dy; y1 += dy;
  } else {
    if (boxEdit.handle.includes("w")) x0 += dx;
    if (boxEdit.handle.includes("e")) x1 += dx;
    if (boxEdit.handle.includes("n")) y0 += dy;
    if (boxEdit.handle.includes("s")) y1 += dy;
  }
  const next = clampBbox([x0, y0, x1, y1], boxEdit.item);
  setEditedBbox(boxEdit.item, boxEdit.anno, next);
  updateBoxElements(annoKey(boxEdit.anno), next);
  if (Math.abs(dx) + Math.abs(dy) > 2) boxEdit.moved = true;
}

function finishBoxEdit(event) {
  if (!boxEdit || boxEdit.pointerId !== event.pointerId) return;
  if (boxEdit.moved) suppressNextBoxClick = true;
  $("overlay").releasePointerCapture?.(event.pointerId);
  boxEdit = null;
  renderDetails();
  window.setTimeout(() => {
    suppressNextBoxClick = false;
  }, 120);
}

function escapeHtml(text) {
  return String(text || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function renderDetails() {
  const item = currentCase();
  const anno = selectedAnno();
  if (!anno) {
    $("selectedDetails").innerHTML = "<p>No annotation selected.</p>";
    const noteInput = $("noteInput");
    if (noteInput) noteInput.value = review[caseKey(item)]?.note || "";
    return;
  }
  const key = keyFor(item.page_id, annoKey(anno));
  const bbox = displayBbox(item, anno);
  const adjusted = validBbox(review[key]?.bbox);
  $("selectedDetails").innerHTML = `
    <dl>
      <dt>Item</dt><dd>#${anno.index}</dd>
      <dt>Type</dt><dd><span class="type-badge">${anno.category_type}</span></dd>
      <dt>Box</dt><dd data-bbox>${validBbox(bbox) ? `[${bbox.join(", ")}]${adjusted ? " edited" : ""}` : "no bbox"}</dd>
      <dt>Case</dt><dd>${item.items_with_bbox}/${item.items_total} boxed, ${item.items_unmatched} no bbox</dd>
    </dl>
    <div class="text">${escapeHtml(anno.text || "")}</div>
  `;
  const noteInput = $("noteInput");
  if (noteInput) noteInput.value = review[key]?.note || "";
}

function renderAnnoList() {
  const item = currentCase();
  const root = $("annoList");
  if (!root) return;
  root.innerHTML = "";
  visibleAnnos(item).forEach((anno) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `anno-row ${annoKey(anno) === String(selectedId) ? "active" : ""}`;
    button.addEventListener("click", () => setSelected(annoKey(anno)));

    const top = document.createElement("div");
    top.className = "anno-main";
    const title = document.createElement("strong");
    title.textContent = `#${anno.index} ${anno.category_type}`;
    const dot = document.createElement("span");
    dot.className = `status-dot ${statusClass(annoStatus(item, anno))}`;
    top.append(title, dot);

    const preview = document.createElement("div");
    preview.className = "anno-preview";
    const bboxText = validBbox(displayBbox(item, anno)) ? "boxed" : "no bbox";
    preview.textContent = `${bboxText} · ${anno.quality} · ${anno.preview || "[empty]"}`;
    button.append(top, preview);
    root.append(button);
  });
}

function renderAll() {
  updateImageSourceStatus();
  renderSummary();
  renderCaseList();
  renderTypeFilters();
  renderViewer();
  renderDetails();
  renderCaseIssue();
  renderAnnoList();
}

function renderCaseIssue() {
  const input = $("caseIssueInput");
  if (!input) return;
  input.value = review[caseKey(currentCase())]?.correction_note || "";
}

function downloadJson(filename, payload) {
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}

function correctionPatchCases() {
  const cases = [];
  DATA.cases.forEach((item) => {
    const changes = [];
    const caseEntry = review[caseKey(item)] || {};
    const caseNote = (caseEntry.correction_note || "").trim();
    if (caseNote) {
      changes.push({
        op: "case_note",
        note: caseNote,
        allowed_follow_up_ops: ["add_annotation", "delete_annotation", "update_type", "update_text", "update_reading_order"]
      });
    }

    item.annotations.forEach((anno) => {
      const key = keyFor(item.page_id, annoKey(anno));
      const entry = review[key];
      if (!entry) return;
      const note = (entry.note || "").trim();
      const status = entry.status || "";
      const oldBbox = validBbox(anno.bbox) ? anno.bbox.map(Number) : null;
      const editedBbox = entry.bbox_version === STORAGE_VERSION && validBbox(entry.bbox)
        ? entry.bbox.map(Number)
        : null;
      const base = {
        anno_id: anno.anno_id ?? anno.index,
        index: anno.index,
        type: anno.category_type,
        text_preview: anno.preview || (anno.text || "").slice(0, 220)
      };

      if (editedBbox && !sameBbox(oldBbox, editedBbox)) {
        changes.push({
          op: "update_bbox",
          ...base,
          old_bbox: oldBbox,
          new_bbox: editedBbox,
          old_poly: validBbox(oldBbox) ? bboxToPoly(oldBbox) : null,
          new_poly: bboxToPoly(editedBbox),
          status,
          note
        });
        return;
      }

      if ((status === "problem" || status === "unsure" || note) && status !== "ok") {
        changes.push({
          op: "flag_annotation",
          ...base,
          bbox: oldBbox,
          status: status || "unsure",
          note
        });
      }
    });

    if (changes.length) {
      cases.push({
        case_id: item.page_id,
        category: item.category,
        subcategory: item.subcategory,
        width: item.width,
        height: item.height,
        changes
      });
    }
  });
  return cases;
}

function exportCorrectionPatch() {
  const cases = correctionPatchCases();
  if (!cases.length) {
    window.alert("No correction patch to export. Drag a bbox or add a correction note first. / 暂无可导出的修正。请先移动标注框，或填写修正说明。");
    return;
  }
  const updateCount = cases.reduce(
    (total, item) => total + item.changes.filter((change) => change.op === "update_bbox").length,
    0
  );
  const flagCount = cases.reduce(
    (total, item) => total + item.changes.filter((change) => change.op === "flag_annotation").length,
    0
  );
  const caseNoteCount = cases.reduce(
    (total, item) => total + item.changes.filter((change) => change.op === "case_note").length,
    0
  );
  const payload = {
    schema_version: CORRECTION_SCHEMA_VERSION,
    base_annotation_version: PUBLIC_VERSION,
    exported_at: new Date().toISOString(),
    source: "review/gt_case_compare_all_fixed7",
    contributor: {
      name: "",
      contact: ""
    },
    summary: {
      case_count: cases.length,
      bbox_update_count: updateCount,
      annotation_flag_count: flagCount,
      case_note_count: caseNoteCount,
      added_annotations: 0,
      removed_annotations: 0
    },
    cases,
    submission: {
      github_repo: "https://github.com/zhihengli-casia/PureDocBench",
      instruction: "Submit this JSON as a GitHub issue or pull request attachment. Maintainers will validate the correction against the HTML and clean image before the next PureDocBench release."
    }
  };
  const stamp = new Date().toISOString().replace(/[:.]/g, "").replace("T", "_").slice(0, 17);
  downloadJson(`puredocbench_gt_correction_${PUBLIC_VERSION}_${stamp}.json`, payload);
}

function bindStagePan() {
  const scroller = $("stageScroll");
  let pan = null;
  scroller.addEventListener("pointerdown", (event) => {
    if (event.button !== 0) return;
    if (event.target.closest(".box, .resize-handle")) return;
    pan = { x: event.clientX, y: event.clientY, left: scroller.scrollLeft, top: scroller.scrollTop };
    scroller.classList.add("dragging");
    scroller.setPointerCapture?.(event.pointerId);
  });
  scroller.addEventListener("pointermove", (event) => {
    if (!pan) return;
    scroller.scrollLeft = pan.left - (event.clientX - pan.x);
    scroller.scrollTop = pan.top - (event.clientY - pan.y);
  });
  const stop = (event) => {
    if (!pan) return;
    pan = null;
    scroller.classList.remove("dragging");
    scroller.releasePointerCapture?.(event.pointerId);
  };
  scroller.addEventListener("pointerup", stop);
  scroller.addEventListener("pointercancel", stop);
}

function bindEvents() {
  const bind = (id, event, handler) => {
    const node = $(id);
    if (node) node.addEventListener(event, handler);
  };
  bind("caseSearch", "input", (event) => {
    query = event.target.value.trim();
    renderCaseList();
  });
  bind("prevCase", "click", () => stepVisibleCase(-1));
  bind("nextCase", "click", () => stepVisibleCase(1));
  bind("exportCorrectionPatch", "click", exportCorrectionPatch);
  bind("loadLocalImages", "click", () => $("localImageDir").click());
  bind("localImageDir", "change", (event) => setLocalImages(event.target.files));
  bind("showLabels", "change", renderViewer);
  bind("showOnlySelected", "change", renderViewer);
  bind("coverBoxes", "change", renderViewer);
  bind("showProblemOnly", "change", () => { renderViewer(); renderAnnoList(); });
  bind("zoom", "input", renderViewer);
  bind("caseIssueInput", "input", () => {
    const item = currentCase();
    const key = caseKey(item);
    review[key] = { ...(review[key] || {}), correction_note: $("caseIssueInput").value };
    if (!review[key].correction_note && !review[key].status && !review[key].note) delete review[key];
    saveReview();
  });
  bind("noteInput", "input", () => {
    const item = currentCase();
    const anno = selectedAnno();
    const key = anno ? keyFor(item.page_id, annoKey(anno)) : caseKey(item);
    review[key] = { ...(review[key] || {}), note: $("noteInput").value };
    saveReview();
  });
  window.addEventListener("keydown", (event) => {
    if (event.target.matches("input, textarea")) return;
    if (event.key === "ArrowLeft") stepVisibleCase(-1);
    if (event.key === "ArrowRight") stepVisibleCase(1);
  });
  window.addEventListener("pointermove", updateBoxEdit);
  window.addEventListener("pointerup", finishBoxEdit);
  window.addEventListener("pointercancel", finishBoxEdit);
  bindStagePan();
}

function initialCaseIndex() {
  const params = new URLSearchParams(window.location.search);
  const raw = (params.get("case") || "").trim();
  if (!raw) return 0;
  const needle = raw.toLowerCase();
  const exact = DATA.cases.find((item) =>
    String(item.index + 1) === raw ||
    item.page_id === raw ||
    item.page_id.split("/").pop() === raw
  );
  if (exact) return DATA.cases.indexOf(exact);
  const partial = DATA.cases.find((item) => item.page_id.toLowerCase().includes(needle));
  return partial ? DATA.cases.indexOf(partial) : 0;
}

function init() {
  Object.keys(DATA.meta.category_counts).forEach((category) => activeCategories.add(category));
  Object.keys(DATA.meta.type_counts).forEach((type) => activeTypes.add(type));
  caseIndex = initialCaseIndex();
  const firstWithBox = currentCase().annotations.find((anno) => validBbox(anno.bbox));
  selectedId = annoKey(firstWithBox || currentCase().annotations[0] || { index: 0 });
  renderFilters();
  renderTypeFilters();
  bindEvents();
  renderAll();
}

init();
