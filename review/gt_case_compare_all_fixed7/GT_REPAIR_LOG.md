# PureDocBench GT BBox Repair Log

This file is the persistent working memory for `review/gt_case_compare_all_fixed7`.
Every future GT/bbox correction must be recorded here before the task is considered done.

## Recording Rules

- Record every changed case with the exact `page_id`.
- Record the token written to `review_data.json`, `review_data.js`, and `index.html`.
- Separate true GT annotation changes from bbox-only fixes.
- Record every non-bbox GT semantic change long-term, including `category_type`, `text`/`preview`, quality/method resets caused by a semantic correction, merges, splits, and deletions.
- For added GT annotations, record: `anno_id`, `index`, `category_type`, text/preview, bbox, and why it was added.
- For split annotations, record the original annotation and each resulting annotation.
- For deleted/ignored items, record why they are not GT, especially for decorative marks, watermarks, seals, logos, QR/barcode, placeholder text inside figures, or frontend-only artifacts.
- For bbox-only fixes, record the affected indices and the reason, e.g. DOM absolute-coordinate rebuild, table whole-grid bbox, edge padding, or manual pixel tuning.
- Record verification artifacts when used: cover audit directory/file and residual report/debug directory.

## Current Baseline

Baseline token: `20260605_finance_tax008_split_header_v299`

Current review data compared with the local HF/release GT package:

- Original release GT annotations: `89,510`
- Current review annotations: `89,784`
- Positive added annotations: `293`
- Removed/merged/ignored annotations: `19`
- Net annotation delta: `+274`

Positive added annotations by category:

- `01_academic`: `200`
- `05_finance`: `31`
- `06_medical`: `62`

This baseline count does not include bbox-only moves, tightening, or edge padding.

## Known Working Rules

- Use browser `getBoundingClientRect` / `Range.getClientRects` viewport-absolute coordinates multiplied by DPR when repairing DOM-rendered cases. Do not mix page-local coordinates with screenshot-absolute coordinates.
- Table GT should usually remain a whole table/grid bbox if the source GT marks it as one table. Do not shrink table annotations to individual words.
- Do not add decorative watermarks, seals, QR/barcodes, logos, or figure placeholder text as GT unless the source GT explicitly contains them or the user asks for them.
- When a visually non-contiguous source GT item causes one huge over-covering bbox, prefer splitting into separate source-faithful annotations and record the split.

## Future Change Entries

Add new entries below this line.

### 2026-06-09 - `20260609_education_textbook001_007_visual_v570`

Scope: first five `02_education/01_textbook` review-list cases

BBox-only correction:

- Added script `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/scripts/fix_education_textbook001_007_visual_v570.py`.
- Method: rebuilt visible textbook bboxes from Chrome DOM selector/range rectangles with per-page clean-PNG scaling; used explicit selector order for headers, chapter titles, definitions, theorem/example labels, formulas, tables, footnotes, side notes, and page footers. Added visual padding to avoid tight text edges. Manually placed `textbook_004` vertical side title `#0` because its DOM node renders off the clean-PNG coordinate plane.
- No GT annotations were added or removed.

Case: `02_education/01_textbook/textbook_001_线性代数`

- Rebuilt all `67` existing bboxes; corrected header/chapter title stack, two-column section/objective blocks, definitions/theorems/examples, formulas, formula-summary tables, footnote, and footer/page number.
- Filled existing no-bbox annotation `#51` (`5.3.4 二次型 / Quadratic Forms`); boxed count `66/67 -> 67/67`.
- Added annotations: `0`; deleted annotations: `0`.

Case: `02_education/01_textbook/textbook_004_大学物理_Maxwell方程`

- Rebuilt all `85` existing bboxes; corrected top header/table, two-column physics text/formula/example flow, formula recap, short exercises, experiment table/body, safety note, footnote, and footer/page number.
- Manually corrected vertical side-title `#0` from the old narrow edge box `[2374, 1492, 2382, 2211]` to `[2275, 3575, 2338, 4055]`.
- Filled existing no-bbox annotations `#77` (`Experiment 7-3 ... Young's Double-Slit Interference Experiment`) and `#82` (footnote/reference block); boxed count `83/85 -> 85/85`.
- Added annotations: `0`; deleted annotations: `0`.

Case: `02_education/01_textbook/textbook_005_教辅练习册_高中数学`

- Rebuilt all `56` existing bboxes; corrected chapter-bar split headers, left/right column thermodynamics text, entropy definition box, derivation steps, example blocks, formulas, notes, Gibbs free-energy section, and page number.
- Boxed count remained `56/56`.
- Added annotations: `0`; deleted annotations: `0`.

Case: `02_education/01_textbook/textbook_006_中国近代史_洋务运动`

- Rebuilt all `26` existing bboxes; corrected split page headers, chapter/section titles, side margin notes, long history paragraphs, bullet list, quote box, footnotes, and page number.
- Boxed count remained `26/26`.
- Added annotations: `0`; deleted annotations: `0`.

Case: `02_education/01_textbook/textbook_007_Calculus_Integration`

- Rebuilt all `29` existing bboxes; corrected header split, chapter number/title, section title, historical sidenote, definition/theorem labels, formulas, figure caption, example steps, footer, and page number.
- Filled existing no-bbox annotation `#26` (final example formula `F(3)-F(1)=...=28`); boxed count `28/29 -> 29/29`.
- Added annotations: `0`; deleted annotations: `0`.

Verification:

- Final report: `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7/reports/pdb_education_textbook001_007_visual_v570.json`.
- Cover audit directory: `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7/cover_audit_education_textbook001_007_v570_only/`.
- Contact sheet: `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7/cover_audit_education_textbook001_007_v570_only/00_contact_sheet.jpg`.

### 2026-06-05 - `20260605_finance_tax008_split_header_v299`

Case: `05_finance/04_tax_document/tax_document_008`

GT annotation change:

- Split original `#0` header because the source text was visually non-contiguous and one bbox over-covered the page header area.
- Updated `#0` to text `滨海市税务局\nBINHAI MUNICIPAL TAX BUREAU`, bbox `[1430, 251, 2170, 442]`, method `finance_targeted_tax008_header_main`.
- Added `anno_id=26`, `index=3`, `category_type=text_block`, text `编号 No. BH-FCT-2025-003847 | 税务登记号 Tax Reg.: 91310115MA1K4XJ32R`, bbox `[1028, 678, 2572, 738]`, method `finance_targeted_tax008_split_doc_number`.

Reason:

- User observed `#0` was still visibly overboxed after v298; the review frontend only renders one rectangular `bbox`, so splitting was the cleanest source-faithful fix.

### 2026-06-05 - `20260605_finance_tax008_top_pixel_v301`

Case: `05_finance/04_tax_document/tax_document_008`

BBox-only correction:

- Pixel-measured and tightened the top header/title/doc-number group from the released clean PNG.
- `anno_id=0`, index `0`, header `滨海市税务局 / BINHAI MUNICIPAL TAX BUREAU`: `[1430, 251, 2170, 442]` -> `[1428, 253, 2168, 415]`.
- `anno_id=1`, index `1`, title `房产税纳税通知书`: `[1410, 483, 2190, 594]` -> `[1405, 458, 2168, 553]`.
- `anno_id=2`, index `2`, title `Property Tax Payment Notice`: `[1495, 593, 2105, 650]` -> `[1490, 553, 2110, 614]`.
- `anno_id=26`, index `3`, split doc-number/tax-registration line: `[1028, 678, 2572, 738]` -> `[1025, 625, 2580, 676]`.
- `anno_id=3`, index `4`, taxpayer/ID line: `[762, 797, 2838, 922]` -> `[790, 805, 2812, 864]`.
- `anno_id=4`, index `5`, TIN/tax-period line: `[762, 885, 2838, 1003]` -> `[790, 892, 2804, 950]`.
- `anno_id=5`, index `6`, section title `一、房产信息 Property Information`: `[762, 981, 2838, 1123]` -> `[760, 986, 1425, 1062]`.

Reason:

- User pointed out the top section was still visibly offset. Local DOM rects were drifting from the released clean PNG near the header, so this correction uses measured clean-image pixel boxes.
- An intermediate wide doc-number bbox accidentally included red page-border pixels; final v301 excludes those border pixels and keeps only the visible doc-number/tax-registration text.

Verification:

- Top overlay crop: `/tmp/tax008_top_v301_overlay.png`.
- Cover audit target: `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7/cover_audit_tax008_v301/11_tax_document_008_cover.jpg`.
- Residual audit: `/tmp/pdb_tax008_residual_v301.json`, result `text_like=0`, `comps=0`.

### 2026-06-05 - `20260605_finance_taxdoc_template_batch_v302`

Scope: `05_finance/04_tax_document`

BBox-only correction:

- Added script `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/scripts/repair_tax_document_template_batch.py`.
- Method: render each tax-document HTML locally, take the current small top non-table bbox patch from the local render, and template-match it against the released clean PNG nearby. This targets the recurring local-DOM-vs-release-clean vertical drift without touching table bboxes.
- No GT annotations were added or removed in this pass.

Case: `05_finance/04_tax_document/tax_document_009`

- `anno_id=1`, index `1`, `title`, `印花税纳税申报表`: `[1474, 204, 2126, 288]` -> `[1474, 179, 2126, 263]`, dy `-25`, score `0.3238`.
- `anno_id=2`, index `2`, `title`, `（适用于一般纳税人）`: `[1574, 314, 2026, 377]` -> `[1576, 279, 2028, 342]`, dy `-35`, score `0.2820`.
- `anno_id=3`, index `3`, `text_block`, `税款所属期：2025年07月01日 至 2025年09月30日 | 填报日期：2025年10月15日`: `[1137, 419, 2463, 473]` -> `[1115, 372, 2441, 426]`, dy `-47`, score `0.1675`.
- `anno_id=4`, index `4`, `title`, `一、纳税人基本信息`: `[805, 527, 1177, 584]` -> `[802, 471, 1174, 528]`, dy `-56`, score `0.2590`.
- `anno_id=6`, index `6`, `title`, `二、印花税应纳税额计算`: `[805, 1027, 1257, 1084]` -> `[801, 941, 1253, 998]`, dy `-86`, score `0.2059`.

Case: `05_finance/04_tax_document/tax_document_016`

- `anno_id=2`, index `2`, `text_block`, taxpayer/tax-id/period line: `[178, 259, 3422, 307]` -> `[178, 229, 3422, 277]`, dy `-30`, score `0.2751`.
- `anno_id=3`, index `3`, `text_block`, customs/refund authority/currency line: `[178, 312, 3422, 360]` -> `[187, 273, 3431, 321]`, dy `-39`, score `0.2553`.

Case: `05_finance/04_tax_document/tax_document_017`

- `anno_id=2`, index `2`, `text_block`, tax authority/settlement id/period line: `[1137, 260, 2440, 302]` -> `[1127, 222, 2430, 264]`, dy `-38`, score `0.2080`.
- `anno_id=4`, index `4`, `title`, `主表：土地增值税清算申报表`: `[1523, 595, 2055, 664]` -> `[1523, 550, 2055, 619]`, dy `-45`, score `0.2937`.

Case: `05_finance/04_tax_document/tax_document_019`

- `anno_id=1`, index `1`, `title`, `税收完税证明`: `[1476, 387, 2124, 522]` -> `[1476, 348, 2124, 483]`, dy `-39`, score `0.2576`.
- `anno_id=3`, index `3`, `text_block`, certificate number/date/amount block: `[717, 746, 2883, 901]` -> `[720, 671, 2886, 826]`, dy `-75`, score `0.1633`.

Verification:

- Dry-run report: `/tmp/pdb_taxdoc_template_batch_v302_dry.json`.
- Final report: `/tmp/pdb_taxdoc_template_batch_v302.json`.
- Top overlay contact sheet: `/tmp/taxdoc_top_overlays_v302_sheet.jpg`.
- Enlarged `tax_document_009` top overlay: `/tmp/taxdoc_top_overlays_v302/tax_document_009.jpg`.
- Residual report: `/tmp/pdb_tax_document_residual_v302.json`.
### 2026-06-05 - `20260605_full_text_range_unboxed_v303`

Scope: all categories with no-bbox text annotations

BBox-only correction:

- Filled existing unboxed text annotations using exact DOM text-node `Range.getClientRects` and a residual gate; no GT annotations were added or removed.
- Accepted `79` cases; filled `715` existing annotation bboxes.
- Full per-index bbox details are in `/tmp/pdb_full_text_range_unboxed_v303.json`.

Accepted cases:

- `01_academic/01_journal_paper/academic_paper_026_经济研究_面板数据`: filled `1` bbox(es), no-bbox `1` -> `0`.
- `01_academic/05_research_proposal/research_proposal_014_Industry_Collab_Pharma`: filled `1` bbox(es), no-bbox `1` -> `0`.
- `01_academic/06_conference_poster/conference_poster_008_EMNLP_情感分析`: filled `3` bbox(es), no-bbox `3` -> `0`.
- `01_academic/06_conference_poster/conference_poster_010_中文计算机视觉`: filled `1` bbox(es), no-bbox `2` -> `1`.
- `02_education/01_textbook/textbook_001_线性代数`: filled `7` bbox(es), no-bbox `8` -> `1`.
- `02_education/01_textbook/textbook_004_大学物理_Maxwell方程`: filled `4` bbox(es), no-bbox `6` -> `2`.
- `02_education/01_textbook/textbook_005_教辅练习册_高中数学`: filled `4` bbox(es), no-bbox `4` -> `0`.
- `02_education/01_textbook/textbook_007_Calculus_Integration`: filled `3` bbox(es), no-bbox `4` -> `1`.
- `02_education/01_textbook/textbook_008_数据结构_二叉树`: filled `3` bbox(es), no-bbox `7` -> `4`.
- `02_education/01_textbook/textbook_009_EM_Waves_Maxwell_EN`: filled `4` bbox(es), no-bbox `6` -> `2`.
- `02_education/01_textbook/textbook_010_电路分析_戴维南`: filled `3` bbox(es), no-bbox `3` -> `0`.
- `02_education/01_textbook/textbook_011_细胞生物学_细胞器_ZHCN`: filled `4` bbox(es), no-bbox `5` -> `1`.
- `02_education/01_textbook/textbook_013_Organic_Chem_EAS_EN`: filled `4` bbox(es), no-bbox `10` -> `6`.
- `02_education/01_textbook/textbook_014_Numerical_Analysis_EN`: filled `5` bbox(es), no-bbox `5` -> `0`.
- `02_education/01_textbook/textbook_015_数据结构_哈希表_ZHCN`: filled `1` bbox(es), no-bbox `2` -> `1`.
- `02_education/01_textbook/textbook_016_高等数学_多元微分_泰勒展开`: filled `1` bbox(es), no-bbox `2` -> `1`.
- `02_education/01_textbook/textbook_017_神经科学_记忆编码与突触可塑性`: filled `4` bbox(es), no-bbox `5` -> `1`.
- `02_education/01_textbook/textbook_023_Abstract_Algebra_EN`: filled `2` bbox(es), no-bbox `2` -> `0`.
- `02_education/01_textbook/textbook_024_DSP_EN`: filled `1` bbox(es), no-bbox `3` -> `2`.
- `02_education/01_textbook/textbook_028_微观经济学`: filled `2` bbox(es), no-bbox `3` -> `1`.
- `02_education/01_textbook/textbook_031_神经科学_记忆编码与突触可塑性`: filled `2` bbox(es), no-bbox `2` -> `0`.
- `02_education/02_exam_paper/exam_paper_011_高考数学_理科`: filled `4` bbox(es), no-bbox `4` -> `0`.
- `02_education/02_exam_paper/exam_paper_012_考研数学一`: filled `3` bbox(es), no-bbox `3` -> `0`.
- `02_education/02_exam_paper/exam_paper_013_司法考试_民法`: filled `2` bbox(es), no-bbox `2` -> `0`.
- `02_education/02_exam_paper/exam_paper_030_Bar_Exam_MBE`: filled `2` bbox(es), no-bbox `2` -> `0`.
- `02_education/02_exam_paper/exam_paper_036_Economics_Market_Macro`: filled `3` bbox(es), no-bbox `4` -> `1`.
- `02_education/02_exam_paper/exam_paper_037_Chemistry_Organic_Equilibrium`: filled `3` bbox(es), no-bbox `3` -> `0`.
- `02_education/02_exam_paper/exam_paper_046_数字电子技术`: filled `6` bbox(es), no-bbox `11` -> `5`.
- `02_education/03_slides/slides_014_材料化学_晶体结构`: filled `18` bbox(es), no-bbox `68` -> `50`.
- `02_education/03_slides/slides_015_DL_Systems_并行训练_ZHCN`: filled `13` bbox(es), no-bbox `53` -> `40`.
- `02_education/03_slides/slides_016_Keynote_AI`: filled `54` bbox(es), no-bbox `63` -> `9`.
- `02_education/03_slides/slides_019_竞品分析`: filled `57` bbox(es), no-bbox `62` -> `5`.
- `02_education/03_slides/slides_029_产品发布_手机`: filled `81` bbox(es), no-bbox `88` -> `7`.
- `02_education/03_slides/slides_030_Human_AI_CoReading`: filled `52` bbox(es), no-bbox `81` -> `29`.
- `02_education/03_slides/slides_030_Smart_Urban_Resilience_2in1`: filled `55` bbox(es), no-bbox `99` -> `44`.
- `02_education/03_slides/slides_030_多模态文档智能系统_上下伪两页科研汇报`: filled `38` bbox(es), no-bbox `114` -> `76`.
- `02_education/03_slides/slides_031_Autonomous_Research_Operations_2in1`: filled `64` bbox(es), no-bbox `122` -> `58`.
- `02_education/04_school_notice/school_notice_002_联合通知_课程调整交换综合测评`: filled `5` bbox(es), no-bbox `5` -> `0`.
- `02_education/04_school_notice/school_notice_005_实验室安全整改联合通知`: filled `6` bbox(es), no-bbox `9` -> `3`.
- `02_education/04_school_notice/school_notice_010_奖学金综合测评通知`: filled `2` bbox(es), no-bbox `4` -> `2`.
- `02_education/04_school_notice/school_notice_013_STEM_Workshop_Competition_EN`: filled `1` bbox(es), no-bbox `1` -> `0`.
- `02_education/04_school_notice/school_notice_020_实习协议`: filled `1` bbox(es), no-bbox `1` -> `0`.
- `02_education/04_school_notice/school_notice_025_Tuition_Invoice_EN`: filled `2` bbox(es), no-bbox `2` -> `0`.
- `02_education/04_school_notice/school_notice_030_春季多部门联合公告墙`: filled `4` bbox(es), no-bbox `4` -> `0`.
- `02_education/04_school_notice/school_notice_031_校外实践联合通知材料包`: filled `1` bbox(es), no-bbox `3` -> `2`.
- `02_education/04_school_notice/school_notice_032_奖学金评审公示材料`: filled `9` bbox(es), no-bbox `13` -> `4`.
- `02_education/04_school_notice/school_notice_033_Campus_Health_Emergency`: filled `1` bbox(es), no-bbox `1` -> `0`.
- `02_education/04_school_notice/school_notice_033_校园事务导航图`: filled `3` bbox(es), no-bbox `3` -> `0`.
- `02_education/04_school_notice/school_notice_034_教务处关于课程调整与学术讲座安排的联合通知`: filled `1` bbox(es), no-bbox `1` -> `0`.
- `02_education/05_syllabus/syllabus_013_电路原理`: filled `2` bbox(es), no-bbox `2` -> `0`.
- `02_education/05_syllabus/syllabus_031_Signals_and_Systems`: filled `11` bbox(es), no-bbox `12` -> `1`.
- `02_education/05_syllabus/syllabus_032_Global_Media_Culture`: filled `6` bbox(es), no-bbox `7` -> `1`.
- `02_education/05_syllabus/syllabus_033_Clinical_Immunology`: filled `2` bbox(es), no-bbox `7` -> `5`.
- `02_education/05_syllabus/syllabus_034_Python_Software_Engineering`: filled `4` bbox(es), no-bbox `7` -> `3`.
- `02_education/05_syllabus/syllabus_035_International_Arbitration`: filled `3` bbox(es), no-bbox `4` -> `1`.
- `02_education/05_syllabus/syllabus_037_Classical_Texts_Translation`: filled `2` bbox(es), no-bbox `6` -> `4`.
- `02_education/05_syllabus/syllabus_038_Mathematical_Economics`: filled `17` bbox(es), no-bbox `25` -> `8`.
- `02_education/05_syllabus/syllabus_039_Autonomous_Robotics`: filled `23` bbox(es), no-bbox `27` -> `4`.
- `02_education/05_syllabus/syllabus_039_Future_Intelligent_Systems`: filled `10` bbox(es), no-bbox `10` -> `0`.
- `02_education/05_syllabus/syllabus_040_Biomedical_Imaging_Lab`: filled `5` bbox(es), no-bbox `6` -> `1`.
- `02_education/05_syllabus/syllabus_040_Quantum_Computing`: filled `15` bbox(es), no-bbox `16` -> `1`.
- `02_education/05_syllabus/syllabus_041_Climate_Futures_Lab`: filled `6` bbox(es), no-bbox `7` -> `1`.
- `02_education/06_lab_report/lab_report_001_杨氏模量测定实验`: filled `1` bbox(es), no-bbox `3` -> `2`.
- `02_education/06_lab_report/lab_report_002_金属拉伸性能测试`: filled `2` bbox(es), no-bbox `3` -> `1`.
- `02_education/06_lab_report/lab_report_005_微生物菌落培养比较`: filled `1` bbox(es), no-bbox `1` -> `0`.
- `02_education/06_lab_report/lab_report_006_分析化学_滴定实验`: filled `2` bbox(es), no-bbox `3` -> `1`.
- `02_education/06_lab_report/lab_report_008_模拟电路_运放实验`: filled `5` bbox(es), no-bbox `5` -> `0`.
- `02_education/06_lab_report/lab_report_010_食品微生物检验报告`: filled `3` bbox(es), no-bbox `3` -> `0`.
- `02_education/06_lab_report/lab_report_012_无机化学_配合物`: filled `1` bbox(es), no-bbox `2` -> `1`.
- `02_education/06_lab_report/lab_report_015_混凝土配合比`: filled `3` bbox(es), no-bbox `3` -> `0`.
- `02_education/06_lab_report/lab_report_031_Astronomy_Spectral`: filled `5` bbox(es), no-bbox `14` -> `9`.
- `02_education/06_lab_report/lab_report_032_水质监测实验报告`: filled `11` bbox(es), no-bbox `12` -> `1`.
- `02_education/06_lab_report/lab_report_033_ECG_BP_Exercise`: filled `9` bbox(es), no-bbox `10` -> `1`.
- `02_education/06_lab_report/lab_report_034_移动机器人实验报告`: filled `3` bbox(es), no-bbox `7` -> `4`.
- `02_education/06_lab_report/lab_report_035_CV_Denoising`: filled `2` bbox(es), no-bbox `6` -> `4`.
- `02_education/06_lab_report/lab_report_036_维生素C含量变化测定`: filled `7` bbox(es), no-bbox `7` -> `0`.
- `03_legal_gov/01_gov_document/gov_document_014_应急部令_突发事件分级`: filled `1` bbox(es), no-bbox `1` -> `0`.
- `03_legal_gov/04_license_permit/license_permit_017_PE_License_Portal`: filled `1` bbox(es), no-bbox `1` -> `0`.
- `03_legal_gov/06_accident_report/accident_report_017_FDA_MedWatch_Adverse_Event`: filled `1` bbox(es), no-bbox `4` -> `3`.

Verification:

- Overall after v303: `89784` items, `88737` boxed, `1047` no-bbox, `7976` low-sim.
- Report: `/tmp/pdb_full_text_range_unboxed_v303.json`.

### 2026-06-05 - `20260605_education_dom_merge_v304`

Scope: `02_education`

BBox-only correction:

- Rebuilt candidate bboxes from DOM absolute coordinates, merged/restored old boxes when safer, and accepted only cases passing residual/no-bbox gates.
- No GT annotations were added or removed; this pass changed existing bbox coordinates and filled existing no-bbox annotations.
- Accepted `41` of `138` evaluated cases; filled `124` no-bbox annotations; total changed annotations reported by DOM pass: `3602`.
- Aggregate text-like residual gain over accepted cases: `8047613`.
- Rejected cases were left unchanged when residual/components worsened or gain was below the threshold.

Accepted cases:

- `02_education/01_textbook/textbook_014_Numerical_Analysis_EN`: changed `31` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `169356` -> `25154` (gain `144202`).
- `02_education/01_textbook/textbook_023_Abstract_Algebra_EN`: changed `35` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `169127` -> `6721` (gain `162406`).
- `02_education/01_textbook/textbook_024_DSP_EN`: changed `28` bbox(es), filled `0` no-bbox, no-bbox `2` -> `2`, residual `44582` -> `14787` (gain `29795`).
- `02_education/02_exam_paper/exam_paper_001_高考理综物理`: changed `73` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `92794` -> `46252` (gain `46542`).
- `02_education/02_exam_paper/exam_paper_002_高考理综物理`: changed `73` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `286671` -> `166655` (gain `120016`).
- `02_education/02_exam_paper/exam_paper_011_高考数学_理科`: changed `100` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `396645` -> `77430` (gain `319215`).
- `02_education/02_exam_paper/exam_paper_012_考研数学一`: changed `77` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `213851` -> `62141` (gain `151710`).
- `02_education/02_exam_paper/exam_paper_037_Chemistry_Organic_Equilibrium`: changed `75` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `465742` -> `165329` (gain `300413`).
- `02_education/02_exam_paper/exam_paper_040_Geography_Data_Interpretation`: changed `57` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `876104` -> `475258` (gain `400846`).
- `02_education/02_exam_paper/exam_paper_041_Biology_Medical_Image`: changed `66` bbox(es), filled `2` no-bbox, no-bbox `2` -> `0`, residual `851366` -> `457399` (gain `393967`).
- `02_education/02_exam_paper/exam_paper_042_Astronomy_Observational`: changed `67` bbox(es), filled `1` no-bbox, no-bbox `3` -> `2`, residual `1530759` -> `753433` (gain `777326`).
- `02_education/02_exam_paper/exam_paper_047_大学期末_电磁场与电磁波`: changed `80` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `252268` -> `193812` (gain `58456`).
- `02_education/02_exam_paper/exam_paper_047_模拟电子技术`: changed `134` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `283749` -> `221507` (gain `62242`).
- `02_education/02_exam_paper/exam_paper_048_高频电子线路考试`: changed `111` bbox(es), filled `12` no-bbox, no-bbox `22` -> `10`, residual `207822` -> `117188` (gain `90634`).
- `02_education/03_slides/slides_007_Art_History_Renaissance`: changed `68` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `1192983` -> `730872` (gain `462111`).
- `02_education/03_slides/slides_014_材料化学_晶体结构`: changed `109` bbox(es), filled `4` no-bbox, no-bbox `50` -> `46`, residual `264707` -> `0` (gain `264707`).
- `02_education/03_slides/slides_015_DL_Systems_并行训练_ZHCN`: changed `102` bbox(es), filled `2` no-bbox, no-bbox `40` -> `38`, residual `251328` -> `0` (gain `251328`).
- `02_education/03_slides/slides_016_Keynote_AI`: changed `87` bbox(es), filled `9` no-bbox, no-bbox `9` -> `0`, residual `0` -> `0` (gain `0`).
- `02_education/03_slides/slides_019_竞品分析`: changed `90` bbox(es), filled `5` no-bbox, no-bbox `5` -> `0`, residual `117573` -> `546` (gain `117027`).
- `02_education/03_slides/slides_029_产品发布_手机`: changed `100` bbox(es), filled `7` no-bbox, no-bbox `7` -> `0`, residual `0` -> `0` (gain `0`).
- `02_education/03_slides/slides_030_Human_AI_CoReading`: changed `199` bbox(es), filled `25` no-bbox, no-bbox `29` -> `4`, residual `400739` -> `20614` (gain `380125`).
- `02_education/03_slides/slides_030_Smart_Urban_Resilience_2in1`: changed `234` bbox(es), filled `10` no-bbox, no-bbox `44` -> `34`, residual `0` -> `0` (gain `0`).
- `02_education/03_slides/slides_030_多模态文档智能系统_上下伪两页科研汇报`: changed `175` bbox(es), filled `7` no-bbox, no-bbox `76` -> `69`, residual `0` -> `0` (gain `0`).
- `02_education/03_slides/slides_031_Autonomous_Research_Operations_2in1`: changed `260` bbox(es), filled `16` no-bbox, no-bbox `58` -> `42`, residual `2604` -> `0` (gain `2604`).
- `02_education/04_school_notice/school_notice_032_系统异常公告`: changed `105` bbox(es), filled `1` no-bbox, no-bbox `1` -> `0`, residual `29625` -> `0` (gain `29625`).
- `02_education/04_school_notice/school_notice_033_Campus_Health_Emergency`: changed `62` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `457783` -> `278226` (gain `179557`).
- `02_education/05_syllabus/syllabus_008_法学院_刑法学总论`: changed `94` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `1538421` -> `647612` (gain `890809`).
- `02_education/05_syllabus/syllabus_010_化工原理_教学大纲`: changed `44` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `623054` -> `511291` (gain `111763`).
- `02_education/05_syllabus/syllabus_031_Signals_and_Systems`: changed `52` bbox(es), filled `1` no-bbox, no-bbox `1` -> `0`, residual `382287` -> `39549` (gain `342738`).
- `02_education/05_syllabus/syllabus_037_Classical_Texts_Translation`: changed `48` bbox(es), filled `4` no-bbox, no-bbox `4` -> `0`, residual `165696` -> `127200` (gain `38496`).
- `02_education/05_syllabus/syllabus_038_Mathematical_Economics`: changed `134` bbox(es), filled `8` no-bbox, no-bbox `8` -> `0`, residual `476693` -> `363776` (gain `112917`).
- `02_education/05_syllabus/syllabus_040_Biomedical_Imaging_Lab`: changed `96` bbox(es), filled `1` no-bbox, no-bbox `1` -> `0`, residual `905679` -> `839023` (gain `66656`).
- `02_education/05_syllabus/syllabus_040_World_Literature`: changed `164` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `1462328` -> `1269237` (gain `193091`).
- `02_education/05_syllabus/syllabus_041_Climate_Futures_Lab`: changed `97` bbox(es), filled `1` no-bbox, no-bbox `1` -> `0`, residual `3335` -> `0` (gain `3335`).
- `02_education/06_lab_report/lab_report_012_无机化学_配合物`: changed `33` bbox(es), filled `1` no-bbox, no-bbox `1` -> `0`, residual `190049` -> `12513` (gain `177536`).
- `02_education/06_lab_report/lab_report_014_酶动力学实验`: changed `33` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `174381` -> `60101` (gain `114280`).
- `02_education/06_lab_report/lab_report_015_混凝土配合比`: changed `29` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `172458` -> `95103` (gain `77355`).
- `02_education/06_lab_report/lab_report_031_Astronomy_Spectral`: changed `57` bbox(es), filled `6` no-bbox, no-bbox `9` -> `3`, residual `521068` -> `405778` (gain `115290`).
- `02_education/06_lab_report/lab_report_032_水质监测实验报告`: changed `52` bbox(es), filled `1` no-bbox, no-bbox `1` -> `0`, residual `1062490` -> `663423` (gain `399067`).
- `02_education/06_lab_report/lab_report_033_ECG_BP_Exercise`: changed `35` bbox(es), filled `0` no-bbox, no-bbox `1` -> `1`, residual `923040` -> `392377` (gain `530663`).
- `02_education/06_lab_report/lab_report_036_维生素C含量变化测定`: changed `36` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `152620` -> `23857` (gain `128763`).

Verification:

- Overall after v304: `89784` items, `88861` boxed, `923` no-bbox, `7500` low-sim.
- Education after v304: `9127` items, `8778` boxed, `349` no-bbox, `1513` low-sim.
- Dry-run report: `/tmp/pdb_education_dom_merge_dry_v304.json`.
- Final report: `/tmp/pdb_education_dom_merge_v304.json`.
### 2026-06-05 - `20260605_logistics_dom_merge_v305`

Scope: `09_logistics`

BBox-only correction:

- Rebuilt candidate bboxes from DOM absolute coordinates using the same residual/no-bbox gate as v304.
- Important pitfall recorded: for this script, single-case `--only-page-id` can produce different DOM matching from full-category browser reuse; logistics v305 accepted cases were therefore written via full-category execution, not single-case rerun.
- No GT annotations were added or removed; this pass changed existing bbox coordinates only.
- Accepted `2` of `120` evaluated cases; aggregate text-like residual gain `201980`.
- Most logistics cases were rejected because DOM candidates had zero gain, worsened residuals, or increased residual components; shipping labels/BOL need a more targeted non-DOM strategy.

Accepted cases:

- `09_logistics/01_shipping_label/shipping_label_008_Maersk_Line_-_Container_Shipping_Manifest_集装箱货运清单`: changed `150` bbox(es), filled `0` no-bbox, no-bbox `49` -> `49`, residual `1046187` -> `956573` (gain `89614`).
- `09_logistics/03_ticket/ticket_018_Eurail_Global_Pass_欧洲铁路通票`: changed `101` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `743181` -> `630815` (gain `112366`).

Near-miss cases left unchanged for later visual review:

- `09_logistics/03_ticket/ticket_005_中国高铁电子票据_-_G1234`: residual gain `144032`, but components `173` -> `180`.
- `09_logistics/04_itinerary/itinerary_001_商务出差行程确认函_Business_Trip_Itinerary_Confirmation`: residual gain `49398`, but components `61` -> `72`.
- `09_logistics/04_itinerary/itinerary_020_国际峰会日程总览_International_Summit_Schedule_Overview`: residual gain `53647`, components `334` -> `292`, but relative gain only `4.2%` under this gate.
- `09_logistics/05_hotel_booking/hotel_booking_001_酒店热敏小票`: residual gain `87620`, but components `166` -> `167`.

Verification:

- Overall after v305: `89784` items, `88861` boxed, `923` no-bbox, `7500` low-sim.
- Dry-run report: `/tmp/pdb_logistics_dom_merge_dry_v305.json`.
- Final report: `/tmp/pdb_logistics_dom_merge_v305.json`.

### 2026-06-05 - `20260605_certificate_dom_merge_dry_v306` (dry-run only, not applied)

Scope: `10_certificate`

Dry-run finding:

- DOM merge dry-run accepted `3` of `104` cases, but the immediate full-category actual rerun did not reproduce the first accepted cases (`diploma_transcript_007`, `diploma_transcript_010`) and was stopped before writing outputs.
- No GT annotations or bboxes were changed in `review_data.json` by v306; current applied token remains `20260605_logistics_dom_merge_v305`.
- Pitfall recorded: for some certificate cases, DOM matching is non-deterministic across runs, likely due rendering/font/image/layout state; do not apply v306 dry-run results without a more stable reproduction or visual cover audit.

Dry-run accepted candidates left unapplied:

- `10_certificate/01_diploma_transcript/diploma_transcript_007_深圳职业技术大学_专科毕业证书暨学业档案`: dry-run changed `188` bbox(es), residual `723475` -> `639463`.
- `10_certificate/01_diploma_transcript/diploma_transcript_010_PHILLIPS_ACADEMY`: dry-run changed `245` bbox(es), residual `832275` -> `695724`.
- `10_certificate/03_award_honor/award_honor_017_EFQM国际质量管理大奖_Recognised_for_Excellence_5_Star`: dry-run changed `168` bbox(es), residual `6968799` -> `5246307`.

Reports:

- Dry-run report: `/tmp/pdb_certificate_dom_merge_dry_v306.json`.
- Aborted partial actual report: `/tmp/pdb_certificate_dom_merge_v306.json`.
### 2026-06-05 - `20260605_business_dom_merge_v307`

Scope: `04_business`

BBox-only correction:

- Rebuilt/merged bboxes from DOM absolute coordinates with residual/no-bbox gates, using full-category execution after v306 exposed some single/dry-run instability.
- No GT annotations were added or removed; this pass changed existing bbox coordinates and filled existing no-bbox annotations.
- Accepted `27` of `160` evaluated cases; filled `67` no-bbox annotations; aggregate text-like residual gain `4182659`.

Accepted cases:

- `04_business/01_contract/contract_008_建设工程施工合同`: changed `38` bbox(es), filled `2` no-bbox, no-bbox `2` -> `0`, residual `626789` -> `343940` (gain `282849`).
- `04_business/01_contract/contract_022_Emergency_Airdrop_Drone`: changed `111` bbox(es), filled `8` no-bbox, no-bbox `9` -> `1`, residual `165814` -> `153769` (gain `12045`).
- `04_business/01_contract/contract_022_深海微生物跨国转让合同`: changed `103` bbox(es), filled `3` no-bbox, no-bbox `3` -> `0`, residual `901091` -> `759498` (gain `141593`).
- `04_business/01_contract/contract_023_Space_Tourism`: changed `104` bbox(es), filled `10` no-bbox, no-bbox `10` -> `0`, residual `5183` -> `0` (gain `5183`).
- `04_business/02_quotation/quotation_011_Precision_Hydraulic_Export_Quote`: changed `43` bbox(es), filled `3` no-bbox, no-bbox `3` -> `0`, residual `783000` -> `327434` (gain `455566`).
- `04_business/02_quotation/quotation_025_Medical_Equipment`: changed `57` bbox(es), filled `3` no-bbox, no-bbox `3` -> `0`, residual `169295` -> `124037` (gain `45258`).
- `04_business/02_quotation/quotation_028_Curtainwall_MEP`: changed `64` bbox(es), filled `5` no-bbox, no-bbox `8` -> `3`, residual `362958` -> `364008` (gain `-1050`).
- `04_business/03_formal_letter/formal_letter_014_Joint_Venture_Proposal_ENZH`: changed `26` bbox(es), filled `1` no-bbox, no-bbox `1` -> `0`, residual `1534658` -> `1391007` (gain `143651`).
- `04_business/03_formal_letter/formal_letter_016_Notice_of_Default_EN`: changed `37` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `680217` -> `520987` (gain `159230`).
- `04_business/03_formal_letter/formal_letter_018_Cease_and_Desist_EN`: changed `43` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `1372734` -> `1164337` (gain `208397`).
- `04_business/03_formal_letter/formal_letter_019_工程竣工验收通知书`: changed `38` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `145323` -> `35583` (gain `109740`).
- `04_business/03_formal_letter/formal_letter_021_历史街区改造联合申诉函`: changed `30` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `102839` -> `40045` (gain `62794`).
- `04_business/04_meeting_memo/meeting_memo_010_MnA_Due_Diligence_Meeting_EN`: changed `40` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `142766` -> `44746` (gain `98020`).
- `04_business/04_meeting_memo/meeting_memo_011_安全生产专题会纪要`: changed `29` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `210634` -> `173740` (gain `36894`).
- `04_business/04_meeting_memo/meeting_memo_012_Strategic_Planning_Offsite_ENZH`: changed `47` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `1368163` -> `1084213` (gain `283950`).
- `04_business/04_meeting_memo/meeting_memo_013_供应链协调会纪要`: changed `34` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `898089` -> `381403` (gain `516686`).
- `04_business/04_meeting_memo/meeting_memo_014_Board_Audit_Committee_EN`: changed `39` bbox(es), filled `2` no-bbox, no-bbox `2` -> `0`, residual `657154` -> `405559` (gain `251595`).
- `04_business/04_meeting_memo/meeting_memo_015_研发项目评审会纪要`: changed `36` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `1140775` -> `631480` (gain `509295`).
- `04_business/04_meeting_memo/meeting_memo_017_薪酬绩效委员会纪要`: changed `84` bbox(es), filled `9` no-bbox, no-bbox `12` -> `3`, residual `548766` -> `520106` (gain `28660`).
- `04_business/05_resume/resume_012_Chief_Medical_Officer_ENZH`: changed `45` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `157244` -> `44215` (gain `113029`).
- `04_business/06_business_plan/business_plan_021_DeepCurrent_Energy`: changed `58` bbox(es), filled `8` no-bbox, no-bbox `9` -> `1`, residual `5761` -> `2938` (gain `2823`).
- `04_business/06_business_plan/business_plan_022_ForgeMind`: changed `98` bbox(es), filled `13` no-bbox, no-bbox `14` -> `1`, residual `409829` -> `288820` (gain `121009`).
- `04_business/07_employee_handbook/eh_007_Retail_Store_Trifold_Handbook`: changed `37` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `566612` -> `413166` (gain `153446`).
- `04_business/07_employee_handbook/employee_handbook_013_Warehouse_Logistics`: changed `32` bbox(es), filled `0` no-bbox, no-bbox `7` -> `7`, residual `357138` -> `164451` (gain `192687`).
- `04_business/07_employee_handbook/employee_handbook_016_Quick_Start_Guide`: changed `23` bbox(es), filled `0` no-bbox, no-bbox `1` -> `1`, residual `85685` -> `38948` (gain `46737`).
- `04_business/07_employee_handbook/employee_handbook_017_员工手册快速导航页`: changed `23` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `134054` -> `24907` (gain `109147`).
- `04_business/07_employee_handbook/employee_handbook_019_Archive_Wall_Handbook`: changed `32` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `145491` -> `52066` (gain `93425`).

Verification:

- Overall after v307: `89784` items, `88928` boxed, `856` no-bbox, `7328` low-sim.
- Business after v307: `8471` items, `8305` boxed, `166` no-bbox, `1159` low-sim.
- Dry-run report: `/tmp/pdb_business_dom_merge_dry_v307.json`.
- Final report: `/tmp/pdb_business_dom_merge_v307.json`.
### 2026-06-05 - `20260605_publishing_dom_merge_v308`

Scope: `07_publishing`

BBox-only correction:

- Rebuilt/merged bboxes from DOM absolute coordinates with residual gates.
- No GT annotations were added or removed; no no-bbox count changed in this pass.
- Accepted `3` of `100` evaluated cases; aggregate text-like residual gain `258834`.
- Newspaper and magazine pages were mostly rejected/unchanged because DOM candidates had zero gain or worsened residuals; these need non-DOM/text matching if further review is required.

Accepted cases:

- `07_publishing/03_book/book_019_哲学著作`: changed `25` bbox(es), residual `659110` -> `513722` (gain `145388`).
- `07_publishing/04_brochure_menu/brochure_menu_003_旅游景点宣传折页`: changed `39` bbox(es), residual `825784` -> `747166` (gain `78618`).
- `07_publishing/05_catalog_directory/catalog_directory_001_电子元器件目录`: changed `41` bbox(es), residual `320798` -> `285970` (gain `34828`).

Verification:

- Overall after v308: `89784` items, `88928` boxed, `856` no-bbox, `7328` low-sim.
- Publishing after v308: `5034` items, `5021` boxed, `13` no-bbox, `34` low-sim.
- Dry-run report: `/tmp/pdb_publishing_dom_merge_dry_v308.json`.
- Final report: `/tmp/pdb_publishing_dom_merge_v308.json`.

### 2026-06-05 - `20260605_technical_dom_merge_dry_v309` (dry-run only, no changes)

Scope: `08_technical`

Dry-run finding:

- DOM merge dry-run accepted `0` of `110` cases, so no data was written.
- Current applied token remains `20260605_publishing_dom_merge_v308`.
- The only remaining technical no-bbox case seen by this pass was `08_technical/05_release_notes/release_notes_004_API_v3_Migration_Guide`; DOM merge produced no residual/no-bbox improvement.
- Most technical cases had `0` residual gain, indicating the remaining low-sim items are more likely text/structure matching issues than bbox coordinate drift.

Report:

- Dry-run report: `/tmp/pdb_technical_dom_merge_dry_v309.json`.

### 2026-06-05 - `20260605_legal_gov_dom_merge_v310`

Scope: `03_legal_gov`

BBox-only correction:

- Rebuilt/merged bboxes from DOM absolute coordinates with residual gates.
- No GT annotations were added or removed; no no-bbox count changed in this pass.
- Accepted `7` of `151` evaluated cases; aggregate text-like residual gain `1324602`.
- Most government/court/notarial long-form documents were rejected because DOM candidates split paragraph/table-level GT into many smaller fragments and increased residual; keep those as original block-level GT unless a case is manually reviewed.

Accepted cases:

- `03_legal_gov/04_license_permit/license_permit_014_Business_License_US`: changed `16` bbox(es), no-bbox `4` -> `4`, residual `480879` -> `384379` (gain `96500`), components `91` -> `77`.
- `03_legal_gov/05_legislation/legislation_002_EU_GDPR_Excerpt`: changed `15` bbox(es), no-bbox `0` -> `0`, residual `1283417` -> `543139` (gain `740278`), components `99` -> `48`.
- `03_legal_gov/05_legislation/legislation_021_人大表决结果公告`: changed `16` bbox(es), no-bbox `4` -> `4`, residual `316831` -> `251221` (gain `65610`), components `57` -> `51`.
- `03_legal_gov/05_legislation/legislation_023_食品安全监督抽检通报`: changed `15` bbox(es), no-bbox `2` -> `2`, residual `397058` -> `304322` (gain `92736`), components `58` -> `21`.
- `03_legal_gov/06_accident_report/accident_report_003_危化品泄漏快报`: changed `14` bbox(es), no-bbox `0` -> `0`, residual `273101` -> `115499` (gain `157602`), components `83` -> `28`.
- `03_legal_gov/06_accident_report/accident_report_005_Workplace_Incident_EN`: changed `12` bbox(es), no-bbox `5` -> `5`, residual `305477` -> `212872` (gain `92605`), components `32` -> `38`.
- `03_legal_gov/06_accident_report/accident_report_015_US_MSHA_Mine_Accident`: changed `17` bbox(es), no-bbox `0` -> `0`, residual `79271` -> `0` (gain `79271`), components `32` -> `0`.

Verification:

- Overall after v310: `89784` items, `88928` boxed, `856` no-bbox.
- Legal/government after v310: `3672` items, `3621` boxed, `51` no-bbox.
- Dry-run report: `/tmp/pdb_legal_gov_dom_merge_dry_v310.json`.
- Final report: `/tmp/pdb_legal_gov_dom_merge_v310.json`.

### 2026-06-05 - `20260605_academic_dom_merge_v311`

Scope: `01_academic`

BBox correction and existing-annotation fill:

- Rebuilt/merged bboxes from DOM absolute coordinates with residual gates.
- No GT annotations were added or removed.
- Accepted `22` of `180` evaluated cases; changed `601` bbox(es), filled `3` existing no-bbox annotations, and reduced aggregate text-like residual by `3255720`.
- Journal papers, theses, patents, and grant proposals were mostly rejected when DOM candidates split original paragraph/table/poster-level GT into smaller fragments or worsened residual; keep those original block-level boxes unless manually reviewed.

Accepted cases:

- `01_academic/01_journal_paper/academic_paper_022_化学学报_有机合成`: changed `29` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `90081` -> `47205` (gain `42876`), components `28` -> `13`.
- `01_academic/02_thesis/thesis_010_博士论文_材料科学`: changed `17` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `350497` -> `310946` (gain `39551`), components `89` -> `35`.
- `01_academic/02_thesis/thesis_013_博士论文_化学_abstract`: changed `11` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `191071` -> `86813` (gain `104258`), components `11` -> `7`.
- `01_academic/03_technical_report/technical_report_006_Environmental_Impact_Assessment`: changed `11` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `421405` -> `211335` (gain `210070`), components `24` -> `7`.
- `01_academic/03_technical_report/technical_report_007_软件测试报告`: changed `27` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `43333` -> `0` (gain `43333`), components `7` -> `0`.
- `01_academic/03_technical_report/technical_report_016_Oil_Gas_Reservoir`: changed `18` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `335031` -> `225304` (gain `109727`), components `24` -> `50`.
- `01_academic/03_technical_report/technical_report_022_Data_Center_Capacity`: changed `15` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `104210` -> `0` (gain `104210`), components `2` -> `0`.
- `01_academic/03_technical_report/technical_report_023_农产品质量检测`: changed `20` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `41649` -> `8150` (gain `33499`), components `5` -> `2`.
- `01_academic/03_technical_report/technical_report_027_ESG_Sustainability_Report`: changed `17` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `70471` -> `3647` (gain `66824`), components `4` -> `8`.
- `01_academic/03_technical_report/technical_report_028_Bridge_Structural_Inspection`: changed `24` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `43715` -> `3173` (gain `40542`), components `12` -> `2`.
- `01_academic/03_technical_report/technical_report_029_Product_Quality_Inspection`: changed `25` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `601503` -> `60868` (gain `540635`), components `84` -> `17`.
- `01_academic/05_research_proposal/research_proposal_016_中科院先导_空间`: changed `13` bbox(es), filled `1` no-bbox, no-bbox `1` -> `0`, residual `120901` -> `65362` (gain `55539`), components `20` -> `11`.
- `01_academic/05_research_proposal/research_proposal_019_省重点研发_农业`: changed `15` bbox(es), filled `1` no-bbox, no-bbox `1` -> `0`, residual `172670` -> `108659` (gain `64011`), components `40` -> `22`.
- `01_academic/05_research_proposal/research_proposal_022_科技部重点研发_碳中和`: changed `14` bbox(es), filled `1` no-bbox, no-bbox `1` -> `0`, residual `123686` -> `39831` (gain `83855`), components `22` -> `4`.
- `01_academic/06_conference_poster/conference_poster_002_AAAI_NLP`: changed `42` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `210758` -> `98212` (gain `112546`), components `50` -> `18`.
- `01_academic/06_conference_poster/conference_poster_006_ICLR_生成模型`: changed `41` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `253153` -> `61399` (gain `191754`), components `14` -> `16`.
- `01_academic/06_conference_poster/conference_poster_017_CVPR_DriveDiff`: changed `45` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `365744` -> `273752` (gain `91992`), components `105` -> `43`.
- `01_academic/06_conference_poster/conference_poster_018_NeurIPS_MoEAtlas`: changed `46` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `930847` -> `787173` (gain `143674`), components `138` -> `120`.
- `01_academic/06_conference_poster/conference_poster_019_ICML_FoldFlow`: changed `46` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `1037366` -> `724222` (gain `313144`), components `310` -> `183`.
- `01_academic/06_conference_poster/conference_poster_021_CVPR_Video_Diffusion`: changed `32` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `369344` -> `251159` (gain `118185`), components `90` -> `57`.
- `01_academic/06_conference_poster/conference_poster_027_SIGIR_RAG`: changed `42` bbox(es), filled `0` no-bbox, no-bbox `0` -> `0`, residual `1063444` -> `569115` (gain `494329`), components `234` -> `129`.
- `01_academic/06_conference_poster/conference_poster_028_INTERSPEECH_VoiceClone`: changed `51` bbox(es), filled `0` no-bbox, no-bbox `4` -> `4`, residual `914558` -> `663392` (gain `251166`), components `168` -> `129`.

Important rejected cases:

- `01_academic/06_conference_poster/conference_poster_010_中文计算机视觉`: DOM candidate would have filled `1` no-bbox (`1` -> `0`) but worsened residual `152117` -> `391197`, so it was rejected.
- `01_academic/06_conference_poster/conference_poster_029_USENIX_KernelGhost`: DOM candidate would have filled `3` no-bbox (`3` -> `0`) but created new residual `0` -> `11284`, so it was rejected.

Verification:

- Overall after v311: `89784` items, `88931` boxed, `853` no-bbox.
- Academic after v311: `4875` items, `4864` boxed, `11` no-bbox.
- Residual spot checks: `technical_report_007_软件测试报告` and `technical_report_022_Data_Center_Capacity` both reported `text_like=0`, `components=0`.
- Dry-run report: `/tmp/pdb_academic_dom_merge_dry_v311.json`.
- Final report: `/tmp/pdb_academic_dom_merge_v311.json`.

### 2026-06-05 - `20260605_medical_dom_merge_v312`

Scope: `06_medical`

BBox-only correction:

- Rebuilt/merged bboxes from DOM absolute coordinates with residual gates.
- No GT annotations were added or removed; no no-bbox count changed in this pass.
- Accepted `11` of `200` evaluated cases; changed `609` bbox(es), aggregate text-like residual gain `1426344`.
- Previously hand-repaired cases such as `medical_report_003`, `medical_report_004`-`008`, `prescription_003`, `prescription_013`, `clinical_record_002`, `clinical_record_004`, `medical_bill_005`, `medical_bill_006`, and `medical_bill_015` were rejected/unchanged by this pass, preserving the manual fixes.

Accepted cases:

- `06_medical/01_medical_report/medical_report_019`: changed `18` bbox(es), no-bbox `0` -> `0`, residual `283581` -> `137491` (gain `146090`), components `6` -> `22`.
- `06_medical/02_prescription/prescription_016`: changed `19` bbox(es), no-bbox `0` -> `0`, residual `53896` -> `22536` (gain `31360`), components `28` -> `15`.
- `06_medical/03_clinical_record/clinical_record_006`: changed `174` bbox(es), no-bbox `0` -> `0`, residual `836206` -> `558542` (gain `277664`), components `115` -> `137`.
- `06_medical/04_medical_bill/medical_bill_009`: changed `32` bbox(es), no-bbox `0` -> `0`, residual `82102` -> `31592` (gain `50510`), components `12` -> `12`.
- `06_medical/04_medical_bill/medical_bill_017`: changed `35` bbox(es), no-bbox `0` -> `0`, residual `95286` -> `47127` (gain `48159`), components `34` -> `24`.
- `06_medical/05_health_record/health_record_001`: changed `13` bbox(es), no-bbox `0` -> `0`, residual `391866` -> `24834` (gain `367032`), components `15` -> `24`.
- `06_medical/07_imaging_report/imaging_report_004`: changed `134` bbox(es), no-bbox `0` -> `0`, residual `794970` -> `628843` (gain `166127`), components `308` -> `275`.
- `06_medical/08_surgical_record/surgical_record_002`: changed `14` bbox(es), no-bbox `0` -> `0`, residual `31389` -> `0` (gain `31389`), components `6` -> `0`.
- `06_medical/09_discharge_summary/discharge_summary_011`: changed `92` bbox(es), no-bbox `0` -> `0`, residual `177074` -> `66786` (gain `110288`), components `48` -> `51`.
- `06_medical/09_discharge_summary/discharge_summary_018`: changed `36` bbox(es), no-bbox `0` -> `0`, residual `175136` -> `88163` (gain `86973`), components `33` -> `65`.
- `06_medical/09_discharge_summary/discharge_summary_020`: changed `42` bbox(es), no-bbox `0` -> `0`, residual `301166` -> `190414` (gain `110752`), components `61` -> `127`.

Remaining medical no-bbox after v312:

- `06_medical/09_discharge_summary/discharge_summary_004`: annotation `#1` text `母婴安全`.
- `06_medical/10_drug_instruction/drug_instruction_018`: annotations `#0` `安宮牛黃丸`, `#1` `古法改良製劑說明`, `#2` `光緒御製原方·當代循證改良·國家級非物質文化遺產`, `#3` `處方來源`.
- DOM merge dry-run rejected these because it worsened page residual; handle them with a targeted visual/text-range pass rather than whole-page DOM merge.

Verification:

- Overall after v312: `89784` items, `88931` boxed, `853` no-bbox.
- Medical after v312: `9589` items, `9584` boxed, `5` no-bbox.
- Residual spot checks: `surgical_record_002` reported `text_like=0`, `components=0`; `health_record_001` and `imaging_report_004` still have residual but improved substantially under the v312 gate.
- Dry-run report: `/tmp/pdb_medical_dom_merge_dry_v312.json`.
- Final report: `/tmp/pdb_medical_dom_merge_v312.json`.

### 2026-06-05 - `20260605_certificate_dom_merge_dry_v313` (dry-run only, no changes)

Scope: `10_certificate`

Dry-run finding:

- DOM merge dry-run accepted `0` of `104` cases, so no data was written.
- Current applied token remains `20260605_medical_dom_merge_v312`.
- This confirms the earlier certificate instability: prior dry-run candidates from v306 did not reproduce in v313:
  - `10_certificate/01_diploma_transcript/diploma_transcript_007_深圳职业技术大学_专科毕业证书暨学业档案`: v313 residual gain `0`, rejected.
  - `10_certificate/01_diploma_transcript/diploma_transcript_010_PHILLIPS_ACADEMY`: v313 residual gain `0`, rejected.
  - `10_certificate/03_award_honor/award_honor_017_EFQM国际质量管理大奖_Recognised_for_Excellence_5_Star`: v313 residual gain `0`, rejected.
- Important rejected no-bbox examples:
  - `10_certificate/02_professional_cert/professional_cert_016_消防工程师资格证书_-_对角线分割_Fire_Protection_Engineer_Certificate`: no-bbox `38` -> `38`, residual gain `0`; left unchanged.
  - `10_certificate/04_service_receipt/service_receipt_011_律师服务费收据_Legal_Service_Fee_Receipt`: candidate would fill `2` no-bbox (`2` -> `0`) but worsened residual `281410` -> `561687`; left unchanged.

Related no-change checks:

- Medical remaining no-bbox targeted Range dry-runs accepted `0` of `2` checked cases:
  - `06_medical/09_discharge_summary/discharge_summary_004`: `.wm3` text `母婴安全` is outside the current clean-image crop/visible page area; do not hallucinate a bbox.
  - `06_medical/10_drug_instruction/drug_instruction_018`: the four missing title/source annotations are in the HTML but horizontally overflow outside the captured clean image; do not hallucinate bboxes.
- Technical remaining no-bbox inspection:
  - `08_technical/05_release_notes/release_notes_004_API_v3_Migration_Guide` has no-bbox annotations `Response Format (Before / After)` and `Pagination (v3)`, but these sections are present in HTML beyond the rendered/captured clean image; leave unchanged unless the source image/rendering is regenerated.

Reports:

- Certificate dry-run report: `/tmp/pdb_certificate_dom_merge_dry_v313.json`.
- Medical targeted reports: `/tmp/pdb_medical_missing_discharge004_dry_v313.json`, `/tmp/pdb_medical_missing_drug018_dry_v313.json`.

### 2026-06-05 - `20260605_all_unboxed_ranges_v314`

Scope: all cases with remaining no-bbox annotations

Existing-annotation bbox fill:

- Re-ran the no-bbox text Range matcher on the current v312/v313 state.
- No GT annotations were added or removed.
- Accepted `1` of `150` no-bbox cases; filled `9` existing no-bbox annotations.
- Most remaining no-bbox annotations are formulas/SVG text, figure-internal labels, hidden/off-crop HTML, or text whose candidate boxes worsened cover residual; those were left unchanged.

Accepted case:

- `02_education/02_exam_paper/exam_paper_048_高频电子线路考试`: filled `9` bbox(es), no-bbox `10` -> `1`, residual `125786` -> `121301` (gain `4485`), components `87` -> `85`. Filled annotation indices `#77`, `#79`, `#81`, `#87`, `#100`, `#101`, `#103`, `#104`, `#119`.

Important rejected examples:

- `09_logistics/01_shipping_label/shipping_label_018_跨境电商集运总表_Cross-Border_Consolidation_Master_Sheet`: found `11` candidates but residual worsened `2690904` -> `2698462`, so left unchanged.
- `02_education/06_lab_report/lab_report_035_Organic_Esterification`: found `3` candidates but residual worsened `146876` -> `154466`, so left unchanged.
- Medical/technical hidden or off-crop cases noted in v313 remained unchanged.

Verification:

- Overall after v314: `89784` items, `88940` boxed, `844` no-bbox.
- Education after v314: `9127` items, `8787` boxed, `340` no-bbox.
- Dry-run report: `/tmp/pdb_all_unboxed_ranges_dry_v314.json`.
- Final report: `/tmp/pdb_all_unboxed_ranges_v314.json`.

### 2026-06-05 - `20260605_publishing_newspaper_dom_merge_dry_v315` (dry-run only, no changes)

Scope: `07_publishing/01_newspaper`

Dry-run finding:

- DOM merge dry-run accepted `0` of `20` newspaper cases, so no data was written.
- Every case reported `0` cover-residual gain (`before == after`) with no no-bbox change.
- Although newspaper pages dominate the full residual ranking, the current residual is not corrected by DOM coordinate rebuild; keep the existing GT boxes rather than splitting/replacing dense newspaper layouts without visual/manual evidence.

Report:

- Dry-run report: `/tmp/pdb_publishing_newspaper_dom_merge_dry_v315.json`.

### 2026-06-05 - `20260605_logistics_shipping_dom_merge_dry_v316` (dry-run only, no changes)

Scope: `09_logistics/01_shipping_label`

Dry-run finding:

- DOM merge dry-run accepted `0` of `20` shipping-label cases, so no data was written.
- Existing old boxes were restored for DOM-unmatched annotations before evaluating candidates; even with this protection, no case improved cover residual.
- `shipping_label_008_Maersk_Line_-_Container_Shipping_Manifest_集装箱货运清单` would have worsened residual `956573` -> `1046187`; left unchanged.
- High no-bbox cases such as `shipping_label_005`, `shipping_label_007`, `shipping_label_008`, and `shipping_label_018` were not safely recoverable by DOM merge in this pass.

Report:

- Dry-run report: `/tmp/pdb_logistics_shipping_dom_merge_dry_v316.json`.

### 2026-06-05 - `20260605_finance_bank_tax_abs_dom_dry_v317` / `20260605_finance_tax_template_dry_v318` (dry-run only, no changes)

Scope: `05_finance/03_bank_statement`, `05_finance/04_tax_document`

Dry-run findings:

- Finance viewport-absolute DOM dry-run accepted `4` tax-document cases by residual gate (`tax_document_007`, `tax_document_013`, `tax_document_014`, `tax_document_016`), but manual inspection of the changed list showed over-broad header-union boxes:
  - `tax_document_007` header candidate expanded to `[717, 207, 2883, 3833]`.
  - `tax_document_013` header candidate expanded to `[808, 127, 2883, 4623]`.
  - `tax_document_014` header candidate expanded to `[1672, 136, 3114, 6959]`.
- These candidates would reduce residual by covering too much page content, so they were not written.
- Bank-statement candidates were all rejected by gate; examples: `bank_statement_014` worsened residual `19523` -> `40087`, `bank_statement_009` worsened `103031` -> `110939`.
- Tax-document template matching dry-run found `0` additional small top-text shifts to apply.

Reports:

- Finance absolute DOM dry-run report: `/tmp/pdb_finance_bank_tax_abs_dom_dry_v317.json`.
- Tax template dry-run report: `/tmp/pdb_finance_tax_template_dry_v318.json`.

### 2026-06-05 - `20260605_finance_tax008009_residual_cover_v328`

Scope: `05_finance/04_tax_document/tax_document_008`, `05_finance/04_tax_document/tax_document_009`

BBox edge-cover correction:

- Used OCR residual-cover expansion only on the two tax-document cases the user had flagged.
- No GT annotations were added or removed.
- Only expanded existing boxes by small amounts; no page-level/header-union rewrites were used.

Changed cases:

- `tax_document_008`: expanded `6` bbox(es), no-bbox `0` -> `0`. Expanded annotation indices `#1`, `#3`, `#15`, `#23`, `#25`, `#26`. Post-check residual `0`, components `0`.
- `tax_document_009`: expanded `7` bbox(es), no-bbox `0` -> `0`. Expanded annotation indices `#2`, `#3`, `#6`, `#9`, `#14` (twice by separate OCR lines), `#15`. Residual improved from prior full-audit value `329860`/`77` comps to `287247`/`50` comps.

Verification:

- Overall after v328: `89784` items, `88940` boxed, `844` no-bbox.
- Both cases remain fully boxed with `0` no-bbox.
- Dry-run report: `/tmp/pdb_finance_tax008009_residual_cover_dry_v328.json`.
- Final report: `/tmp/pdb_finance_tax008009_residual_cover_v328.json`.
- Residual report: `/tmp/pdb_finance_tax008009_residual_after_v328.json`.

### 2026-06-05 - `20260605_finance_bank_residual_cover_v329`

Scope: selected `05_finance/03_bank_statement` cases previously flagged or suspicious

BBox edge-cover correction:

- Used OCR residual-cover expansion on `bank_statement_009`, `bank_statement_013`, `bank_statement_014`, and `bank_statement_017`.
- No GT annotations were added or removed.
- Only small expansions were accepted; no DOM coordinate rewrite was used.

Changed cases:

- `bank_statement_009`: expanded `1` bbox (`#34`) by `1.04x`; no-bbox `0` -> `0`; post-check residual unchanged at `103031`, comps `7`.
- `bank_statement_014`: expanded `4` bboxes (`#19`, `#34`, `#41`, `#42`); no-bbox `0` -> `0`; residual improved from prior full-audit value `19523` to `18445`, comps stayed `12`.
- `bank_statement_017`: expanded `1` bbox (`#26`) by `1.40x`; no-bbox `0` -> `0`; residual improved from prior full-audit value `36846`/`2` comps to `35838`/`1` comp.
- `bank_statement_013`: checked; no changes proposed.

Verification:

- Overall after v329: `89784` items, `88940` boxed, `844` no-bbox.
- All checked bank-statement cases remain fully boxed.
- Dry-run report: `/tmp/pdb_finance_bank_residual_cover_dry_v329.json`.
- Final report: `/tmp/pdb_finance_bank_residual_cover_v329.json`.
- Residual report: `/tmp/pdb_finance_bank_residual_after_v329.json`.

### 2026-06-05 - `20260605_finance_tax_safe_residual_cover_v330`

Scope: selected safe cases from `05_finance/04_tax_document`

BBox edge-cover correction:

- Ran OCR residual-cover dry-run over the full tax-document subcategory, then applied only low-risk cases with small bbox growth and no large horizontal/page-level shifts.
- No GT annotations were added or removed.
- Applied cases: `tax_document_001`, `tax_document_002`, `tax_document_006`, `tax_document_007`, `tax_document_015`.
- Rejected risky dry-run candidates in `tax_document_003`, `005`, `010`, `011`, `012`, `013`, `014`, `016`, `017`, `018`, `019`, and `020` because they had large expansion ratios, large horizontal shifts, or many table/header changes.

Changed cases:

- `tax_document_001`: expanded `15` bbox(es), no-bbox `0` -> `0`; residual remained `35296`, comps `34`.
- `tax_document_002`: expanded `6` bbox(es), no-bbox `0` -> `0`; residual remained `1413`, comps `3`.
- `tax_document_006`: expanded `11` bbox(es), no-bbox `0` -> `0`; residual improved from prior full-audit value `520236` to `505160`, comps `17` -> `10`.
- `tax_document_007`: expanded `1` bbox, no-bbox `0` -> `0`; residual improved from prior full-audit value `46524` to `0`, comps `4` -> `0`.
- `tax_document_015`: expanded `4` bbox(es), no-bbox `0` -> `0`; residual improved from prior full-audit value `149172`/`85` comps to `104573`/`65` comps.

Verification:

- Overall after v330: `89784` items, `88940` boxed, `844` no-bbox.
- All applied tax-document cases remain fully boxed.
- Full tax dry-run report: `/tmp/pdb_finance_tax_residual_cover_dry_v330.json`.
- Final applied report: `/tmp/pdb_finance_tax_safe_residual_cover_v330.json`.
- Residual report: `/tmp/pdb_finance_tax_safe_residual_after_v330.json`.

### 2026-06-05 - `20260605_finance_bank_safe_residual_cover_v331`

Scope: selected safe cases from `05_finance/03_bank_statement`

BBox edge-cover correction:

- Ran OCR residual-cover dry-run over the full bank-statement subcategory, then applied only low-risk cases with small bbox growth and no large horizontal/page-level shifts.
- No GT annotations were added or removed.
- Applied cases: `bank_statement_001`, `002`, `003`, `005`, `008`, `010`, `012`, `020`.
- Rejected risky dry-run candidates in `bank_statement_004`, `006`, `007`, `011`, `016`, `018`, and `019` because they had large expansion ratios, large horizontal shifts, or too many changes.

Changed cases:

- `bank_statement_001`: expanded `1` bbox; no-bbox `0` -> `0`; residual remained `341`, comps `2`.
- `bank_statement_002`: expanded `2` bboxes; no-bbox `0` -> `0`; residual improved from prior full-audit value `31546` to `29740`, comps `4` -> `3`.
- `bank_statement_003`: expanded `6` bboxes; no-bbox `0` -> `0`; residual improved from prior full-audit value `1096` to `0`, comps `3` -> `0`.
- `bank_statement_005`: expanded `2` bboxes; no-bbox `0` -> `0`; residual remained `0`.
- `bank_statement_008`: expanded `2` bboxes; no-bbox `0` -> `0`; residual improved from prior full-audit value `58542` to `57411`, comps `8`.
- `bank_statement_010`: expanded `4` bboxes; no-bbox `0` -> `0`; residual remained `0`.
- `bank_statement_012`: expanded `4` bboxes; no-bbox `0` -> `0`; residual improved from prior full-audit value `8191`/`7` comps to `6413`/`5` comps.
- `bank_statement_020`: expanded `3` bboxes; no-bbox `0` -> `0`; residual improved from prior full-audit value `119142`/`32` comps to `117248`/`30` comps.

Verification:

- Overall after v331: `89784` items, `88940` boxed, `844` no-bbox.
- All applied bank-statement cases remain fully boxed.
- Full bank dry-run report: `/tmp/pdb_finance_bank_all_residual_cover_dry_v331.json`.
- Final applied report: `/tmp/pdb_finance_bank_safe_residual_cover_v331.json`.
- Residual report: `/tmp/pdb_finance_bank_safe_residual_after_v331.json`.

### 2026-06-05 - `20260605_logistics_bol_dom_merge_dry_v319` (dry-run only, no changes)

Scope: `09_logistics/06_bill_of_lading`

Dry-run finding:

- DOM merge dry-run accepted `0` of `20` bill-of-lading cases at the default residual gate, so no data was written.
- Most high-residual cases had `0` gain; several candidates would worsen residual.
- Small possible follow-up: `bill_of_lading_005_Cold_Chain_Pharmaceutical_Transport_Dashboard` improved residual `8661` -> `0`, but default `min_gain=25000` rejected it. It should be visually/low-threshold checked before any write because the gain is small.

Report:

- Dry-run report: `/tmp/pdb_logistics_bol_dom_merge_dry_v319.json`.

### 2026-06-05 - `20260605_logistics_bol005_dom_merge_dry_v320` (dry-run only, no changes)

Scope: `09_logistics/06_bill_of_lading/bill_of_lading_005_Cold_Chain_Pharmaceutical_Transport_Dashboard`

Dry-run finding:

- Rechecked the small v319 candidate with `min_gain=5000`.
- Candidate reduced residual `8661` -> `0`, but it would change `93` annotations for a very small residual-only gain.
- Because the edit size is disproportionate and could alter table/field grouping, it was not written.

Report:

- Dry-run report: `/tmp/pdb_logistics_bol005_dom_merge_dry_v320.json`.

### 2026-06-05 - `20260605_logistics_itinerary_dom_merge_dry_v321` (dry-run only, no changes)

Scope: `09_logistics/04_itinerary`

Dry-run finding:

- DOM merge dry-run accepted `0` of `20` itinerary cases, so no data was written.
- `itinerary_001` reduced residual `354871` -> `305473`, but component count worsened `61` -> `72`, so the gate rejected it.
- High-residual itinerary cases such as `itinerary_011`, `itinerary_013`, `itinerary_017`, and `itinerary_020` had `0` gain and were left unchanged.

Report:

- Dry-run report: `/tmp/pdb_logistics_itinerary_dom_merge_dry_v321.json`.

### 2026-06-05 - `20260605_logistics_customs_dom_merge_dry_v322` (dry-run only, no changes)

Scope: `09_logistics/02_customs_packing`

Dry-run finding:

- DOM merge dry-run accepted `0` of `20` customs/packing cases at the default residual gate, so no data was written.
- High-residual cases such as `customs_packing_017`, `customs_packing_018`, and `customs_packing_020` had `0` gain.
- Candidates for `customs_packing_013` and `customs_packing_019` would severely worsen residual, so they were rejected.
- Small low-threshold follow-up candidates exist (`customs_packing_014` residual `5443` -> `0`), but default gate correctly avoided a broad rewrite for very small gain.

Report:

- Dry-run report: `/tmp/pdb_logistics_customs_dom_merge_dry_v322.json`.

### 2026-06-05 - `20260605_logistics_hotel_dom_merge_dry_v323` (dry-run only, no changes)

Scope: `09_logistics/05_hotel_booking`

Dry-run finding:

- DOM merge dry-run accepted `1` of `20` hotel-booking cases by residual gate, but no data was written after visual inspection.
- Accepted-by-gate candidate:
  - `hotel_booking_001_酒店热敏小票`: residual `431863` -> `340545` (gain `91318`), but it would change `137` annotations.
- Before/after cover inspection showed the candidate was visually wrong: many boxes stretched or shifted far to the right/outside the receipt page. It was manually vetoed.
- High-residual `hotel_booking_019_跨城商旅总订单` had `0` gain and was left unchanged.

Reports / visual check:

- Dry-run report: `/tmp/pdb_logistics_hotel_dom_merge_dry_v323.json`.
- Temporary before/after cover check: `/tmp/pdb_hotel001_v323_wGRfkK/before_cover/11_hotel_booking_001_酒店热敏小票_cover.jpg`, `/tmp/pdb_hotel001_v323_wGRfkK/after_cover/11_hotel_booking_001_酒店热敏小票_cover.jpg`.

### 2026-06-05 - `20260605_logistics_ticket_dom_merge_dry_v324` (dry-run only, no changes)

Scope: `09_logistics/03_ticket`

Dry-run finding:

- DOM merge dry-run accepted `0` of `20` ticket cases, so no data was written.
- `ticket_005_中国高铁电子票据_-_G1234` reduced residual `730955` -> `586923`, but component count worsened `173` -> `180`, so it was rejected.
- `ticket_018_Eurail_Global_Pass_欧洲铁路通票` would worsen residual `630815` -> `743181`, so it was rejected.
- Other ticket cases had either `0` gain or small residual-only gains below the safety threshold.

Report:

- Dry-run report: `/tmp/pdb_logistics_ticket_dom_merge_dry_v324.json`.

### 2026-06-05 - `20260605_business_handbook_dom_merge_dry_v325` (dry-run only, no changes)

Scope: `04_business/07_employee_handbook`

Dry-run finding:

- DOM merge dry-run accepted `0` of `21` employee-handbook cases, so no data was written.
- High-residual `employee_handbook_001_互联网大厂` and `employee_handbook_002_Manufacturing_Safety` had `0` gain.
- Several candidates would worsen residual (`employee_handbook_006`, `employee_handbook_007`, `employee_handbook_015`, etc.) and were rejected.
- Small gains in `employee_handbook_008`, `employee_handbook_010`, and `employee_handbook_020_Control_Console_Handbook` did not pass safety thresholds.

Report:

- Dry-run report: `/tmp/pdb_business_handbook_dom_merge_dry_v325.json`.

### 2026-06-05 - `20260605_technical_product_manual_dom_merge_dry_v326` (dry-run only, no changes)

Scope: `08_technical/01_product_manual`

Dry-run finding:

- DOM merge dry-run accepted `0` of `20` product-manual cases, so no data was written.
- All `20` cases reported `0` residual gain; high-residual cases such as `product_manual_001`, `product_manual_005`, `product_manual_009`, `product_manual_010`, and `product_manual_017` were left unchanged.

Report:

- Dry-run report: `/tmp/pdb_technical_product_manual_dom_merge_dry_v326.json`.

### 2026-06-05 - `20260605_technical_datasheet_dom_merge_dry_v327` (dry-run only, no changes)

Scope: `08_technical/02_datasheet`

Dry-run finding:

- DOM merge dry-run accepted `0` of `30` datasheet/SDS cases, so no data was written.
- High-residual cases such as `datasheet_002`, `datasheet_005`, and `datasheet_025` had `0` gain.
- `datasheet_014_光纤收发器规格书` reduced a small residual `5030` -> `0`, but default `min_gain=25000` rejected it; leave for optional visual/low-threshold review.

Report:

- Dry-run report: `/tmp/pdb_technical_datasheet_dom_merge_dry_v327.json`.

### 2026-06-05 - `20260605_finance_remaining_strict_residual_cover_v332` / `20260605_finance_remaining_strict_residual_cover_v333_revert_utility020`

Scope: selected strict low-risk cases from remaining `05_finance` subcategories:
`01_invoice_receipt`, `02_financial_report`, `05_insurance`, `06_utility_bill`,
`07_securities_statement`, `08_audit_report`, `09_fund_prospectus`, `10_credit_report`

BBox edge-cover correction:

- Ran OCR residual-cover dry-run over `172` remaining finance cases outside bank/tax.
- Dry-run produced `161` changed candidates; only strict local expansions were applied.
- Strict selection rule: low changed-count, low area growth, no large horizontal/page-level shift.
- No GT annotations were added or removed.
- No DOM coordinate rewrite was used.
- Initially applied `32` cases / `112` bbox expansions in v332.
- Reverted `05_finance/06_utility_bill/utility_bill_020` in v333 because text-like residual worsened from `24730` to `97442` despite component count dropping from `10` to `9`.
- Final retained result: `31` cases / `107` bbox expansions.

Changed cases retained:

- `invoice_receipt_004`, `invoice_receipt_008`, `invoice_receipt_010`, `invoice_receipt_012`, `invoice_receipt_014`, `invoice_receipt_018`, `invoice_receipt_020`, `invoice_receipt_024`, `invoice_receipt_025`, `invoice_receipt_028`
- `financial_report_002`, `financial_report_011`, `financial_report_015`
- `insurance_007`, `insurance_008`, `insurance_011`
- `utility_bill_004`, `utility_bill_006`, `utility_bill_007`, `utility_bill_016`, `utility_bill_018`
- `securities_statement_006`, `securities_statement_010`, `securities_statement_014`, `securities_statement_016`
- `audit_report_005`, `audit_report_014`, `audit_report_016`
- `fund_prospectus_012`
- `credit_report_012`, `credit_report_019`

Residual verification after v333:

- Selected-check text-like residual improved from `2932452` to `2844425` (gain `88027`).
- Selected-check component count improved from `602` to `557` (gain `45`).
- Fully resolved residual in this selected check: `utility_bill_018` (`3332` -> `0`), `fund_prospectus_012` (`1553` -> `0`).
- Larger improvements included `insurance_007` (`77820` -> `56100`), `invoice_receipt_020` (`49963` -> `39757`), `utility_bill_016` (`254387` -> `245621`), `audit_report_016` (`85750` -> `78257`), and `financial_report_015` (`12681` -> `6815`).
- Several retained cases had unchanged residual but only local low-risk edge expansion; keep them because they do not worsen the cover audit.

Rejected / deferred high-risk candidates from the dry-run:

- `credit_report_004` remained deferred: dry-run would expand a table from `[643, 1751, 1614, 1868]` to `[643, 1733, 2952, 1868]`, indicating a broad horizontal table expansion rather than a safe local fix.
- `financial_report_009`, `fund_prospectus_009`, `fund_prospectus_010`, `fund_prospectus_018`, `securities_statement_015`, and `securities_statement_018` had too many changed boxes.
- `insurance_003`, `insurance_019`, `audit_report_007`, `audit_report_011`, `audit_report_018`, `credit_report_007`, `credit_report_010`, and similar table-heavy candidates had large area ratios or thousand-pixel horizontal shifts.
- These candidates were not written and should only be revisited with visual/manual review.

Reports:

- Full remaining-finance dry-run: `/tmp/pdb_finance_remaining_residual_cover_dry_v332.json`.
- v332 applied report: `/tmp/pdb_finance_remaining_strict_residual_cover_v332.json`.
- Before residual check: `/tmp/pdb_finance_remaining_strict_residual_before_v332.json`.
- v332 residual check: `/tmp/pdb_finance_remaining_strict_residual_after_v332.json`.
- v333 residual check after reverting `utility_bill_020`: `/tmp/pdb_finance_remaining_strict_residual_after_v333.json`.
- Debug residual images for the first v332 check: `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7/cover_residual_finance_strict_after_v332`.

### 2026-06-05 - `credit_report_004` targeted recheck after v333 (no changes)

Scope: `05_finance/10_credit_report/credit_report_004`

Finding:

- User had previously seen this case as `37/48 boxed, 11 no bbox`.
- Current v333 state is `48/48 boxed`, `0` no-bbox, `0` low-similarity.
- Cover residual is low for this page: `3863` text-like area, `8` components.
- Cover image inspection showed the remaining residual is mostly thin red rules, watermark/decoration, and tiny bottom artifacts, not obvious exposed正文.
- The risky dry-run table expansion for this case was still rejected and not written.

Reports / visual check:

- Cover image: `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7/cover_audit_credit_report_004_v333/11_credit_report_004_cover.jpg`.
- Residual report: `/tmp/pdb_credit_report_004_residual_v333.json`.
- Residual debug: `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7/cover_residual_credit_report_004_v333/001_credit_report_004_residual.jpg`.

### 2026-06-05 - full residual audit after v333 (triage only, no changes)

Scope: all `1475` review cases

Finding:

- Ran full cover residual audit to reprioritize the remaining overnight work.
- Category residual totals remained highest in `09_logistics`, `07_publishing`, and `10_certificate`; these are heavily influenced by decorative, newspaper, certificate, image, and background content, so high residual is not automatically a bbox error.
- `05_finance` now has `0` no-bbox cases; its residual total is lower than the large visual-layout categories.
- Remaining no-bbox total is `844` across `150` cases.
- Top no-bbox clusters include slide/deck-like education cases, several logistics labels/manifests, business plans/contracts, and a few certificate cases.

Reports:

- Full residual report: `/tmp/pdb_full_residual_after_v333.json`.
- Top residual debug images: `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7/cover_residual_full_after_v333`.

### 2026-06-05 - `20260605_business_strict_residual_cover_v335`

Scope: strict low-risk selected cases from `04_business`

BBox edge-cover correction:

- Ran OCR residual-cover dry-run over all `160` business cases.
- Dry-run produced `101` changed candidates.
- Applied only `13` strict candidates / `24` bbox expansions.
- No GT annotations were added or removed.
- No DOM coordinate rewrite was used.
- High-risk candidates with large changed counts, large table expansions, or large horizontal shifts were not written.

Changed cases retained:

- `contract_007_Software_License_Agreement`
- `quotation_001_IT设备采购报价单`, `quotation_002_Construction_Project_Quote`, `quotation_003_广告投放报价方案`, `quotation_021_安防监控系统报价单`, `quotation_026_Ultrafast_Laser_System`
- `resume_022_Draft_Review_CV`, `resume_024_Quant_Research_Dashboard`
- `employee_handbook_004_Attendance_Policy`, `employee_handbook_006_Leave_Benefits`, `employee_handbook_010_Workplace_Safety`, `employee_handbook_018_Transit_Map_Handbook`, `employee_handbook_020_Control_Console_Handbook`

Residual verification:

- Selected-check text-like residual improved from `2244007` to `2169584` (gain `74423`).
- Selected-check component count improved from `700` to `655` (gain `45`).
- No selected case worsened.
- Main gains:
  - `contract_007_Software_License_Agreement`: `197663` -> `149235`, comps `89` -> `60`.
  - `employee_handbook_004_Attendance_Policy`: `396949` -> `383115`, comps `51` -> `48`.
  - `employee_handbook_010_Workplace_Safety`: `240190` -> `229775`, comps `72` -> `66`.
  - `quotation_002_Construction_Project_Quote`: `44782` -> `43359`, comps `14` -> `8`.

Rejected / deferred high-risk candidates:

- Large table or horizontal expansions were rejected in cases such as `contract_022_Emergency_Airdrop_Drone`, `quotation_012`, `quotation_016`, `quotation_028`, `formal_letter_014`, `meeting_memo_010`, and `employee_handbook_016`.
- Large changed-count candidates were rejected in cases such as `contract_022_深海微生物跨国转让合同`, `contract_023_Space_Tourism`, `resume_023_科研人才全景履历海报`, `employee_handbook_001`, and `employee_handbook_002`.
- No-bbox-heavy business cases still need separate range/visual review; residual-cover only expands existing boxes.

Reports:

- Business dry-run report: `/tmp/pdb_business_residual_cover_dry_v334.json`.
- v335 applied report: `/tmp/pdb_business_strict_residual_cover_v335.json`.
- Before residual check: `/tmp/pdb_business_strict_residual_before_v335.json`.
- After residual check: `/tmp/pdb_business_strict_residual_after_v335.json`.
- Debug residual images: `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7/cover_residual_business_strict_after_v335`.

### 2026-06-05 - `20260605_technical_strict_residual_cover_v337`

Scope: strict low-risk selected cases from `08_technical`

BBox edge-cover correction:

- Ran OCR residual-cover dry-run over all `110` technical cases.
- Dry-run produced `92` changed candidates.
- Applied only `8` strict candidates / `19` bbox expansions.
- No GT annotations were added or removed.
- No DOM coordinate rewrite was used.
- High-risk candidates with large product-manual/table/spec-sheet expansions were not written.

Changed cases retained:

- `datasheet_015_LED_Driver_IC_EN`
- `api_doc_001_RESTful_API_Reference`
- `api_reference_009_OpenAPI_Swagger`
- `api_reference_012_OAuth2_Flow`
- `api_reference_015_ML_Inference_API`
- `api_reference_020_MQTT_IoT_Protocol`
- `architecture_diagram_008_数据仓库架构`
- `release_notes_010_版本更新说明`

Residual verification:

- Selected-check text-like residual improved from `1292680` to `1211553` (gain `81127`).
- Selected-check component count improved from `239` to `228` (gain `11`).
- No selected case worsened.
- Main gains:
  - `datasheet_015_LED_Driver_IC_EN`: `338042` -> `286559`.
  - `api_reference_012_OAuth2_Flow`: `92385` -> `73147`, comps `27` -> `21`.
  - `api_reference_009_OpenAPI_Swagger`: `190609` -> `180203`, comps `45` -> `40`.
- Several retained cases had unchanged residual but only local low-risk edge expansion.

Rejected / deferred high-risk candidates:

- Large product-manual expansions were rejected in cases such as `product_manual_001`, `003`, `004`, `006`, `009`, `010`, `013`, `018`, and `020`.
- Large datasheet/spec table expansions were rejected in cases such as `datasheet_002`, `004`, `005`, `006`, `010`, `012`, `013`, `017`, and `026`.
- Release notes/API candidates with large changed counts or large vertical growth were rejected, including `release_notes_004`, `005`, `008`, `013`, `020`, and `api_reference_019`.

Reports:

- Technical dry-run report: `/tmp/pdb_technical_residual_cover_dry_v336.json`.
- v337 applied report: `/tmp/pdb_technical_strict_residual_cover_v337.json`.
- Before residual check: `/tmp/pdb_technical_strict_residual_before_v337.json`.
- After residual check: `/tmp/pdb_technical_strict_residual_after_v337.json`.
- Debug residual images: `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7/cover_residual_technical_strict_after_v337`.

### 2026-06-05 - `20260605_publishing_strict_residual_cover_v339`

Scope: strict low-risk selected cases from `07_publishing`

BBox edge-cover correction:

- Ran OCR residual-cover dry-run over all `100` publishing cases.
- Dry-run produced `82` changed candidates.
- Applied only `12` strict candidates / `25` bbox expansions.
- No GT annotations were added or removed.
- High-risk newspaper, menu, catalog, and table-like candidates with large changed counts or broad table expansions were not written.

Changed cases retained:

- `magazine_002_科技杂志_Feature`
- `magazine_004_学术期刊目录页`
- `book_006_小说正文页`
- `book_007_Technical_Book_EN`
- `book_010_童话故事`
- `brochure_menu_007_Wine_List`
- `brochure_menu_014_海鲜珍馐`
- `catalog_directory_010_展会参展商名录`
- `catalog_directory_011_珠宝奢侈品目录`
- `catalog_directory_012_Automotive_Parts_Catalog`
- `catalog_directory_014_Fashion_Lookbook`
- `catalog_directory_019_有机食品产品目录`

Residual verification:

- Selected-check text-like residual improved from `3214401` to `3058094` (gain `156307`).
- Selected-check component count improved from `457` to `448` (gain `9`).
- No selected case worsened.
- Main gains:
  - `brochure_menu_007_Wine_List`: `129315` -> `0`, comps `2` -> `0`.
  - `catalog_directory_010_展会参展商名录`: `131536` -> `111803`, comps `21` -> `17`.
  - `book_007_Technical_Book_EN`: `177550` -> `170307`, comps `34` -> `31`.

Rejected / deferred high-risk candidates:

- All `newspaper_*` candidates were rejected because they had very large changed counts and would require visual/manual review instead of bulk residual-cover expansion.
- Large or broad catalog/menu candidates were rejected, including `catalog_directory_001`, `003`, `006`, `013`, `016`, `017`, `magazine_010`, and `book_012`.
- `magazine_003_财经杂志_数据报道` was deferred because the candidate had high max ratio / vertical growth for a header area.
- `brochure_menu_005`, `brochure_menu_011_法式米其林套餐`, and `brochure_menu_018_Wine_Pairing_Menu` were deferred despite being near-safe because menu/card layouts need visual confirmation before touching many local boxes.

Reports:

- Publishing dry-run report: `/tmp/pdb_publishing_residual_cover_dry_v338.json`.
- v339 applied report: `/tmp/pdb_publishing_strict_residual_cover_v339.json`.
- Before residual check: `/tmp/pdb_publishing_strict_residual_before_v339.json`.
- After residual check: `/tmp/pdb_publishing_strict_residual_after_v339.json`.
- Debug residual images: `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7/cover_residual_publishing_strict_after_v339`.

### 2026-06-05 - `20260605_certificate_strict_residual_cover_v341`

Scope: strict low-risk selected cases from `10_certificate`

BBox edge-cover correction:

- Ran OCR residual-cover dry-run over all `104` certificate cases.
- Dry-run produced `79` changed candidates.
- Applied only `5` strict candidates / `11` bbox expansions.
- No GT annotations were added or removed.
- Safe-but-not-strict candidates were deferred because certificate layouts include seals, ornate titles, table grids, and decorative residual that can fool area-based gating.

Changed cases retained:

- `diploma_transcript_001_南京大学理学学士学位证书`
- `diploma_transcript_002_Yale_University_Bachelor_of_Arts`
- `diploma_transcript_003_中国科学院计算技术研究所_结业证书`
- `diploma_transcript_004_University_of_Oxford_-_Honorary_Degree`
- `professional_cert_016_消防工程师资格证书_-_对角线分割_Fire_Protection_Engineer_Certificate`

Residual verification:

- Selected-check text-like residual improved from `1181234` to `1176923` (gain `4311`).
- Selected-check component count improved from `204` to `193` (gain `11`).
- No selected case worsened.
- Main gain:
  - `diploma_transcript_002_Yale_University_Bachelor_of_Arts`: `205653` -> `201342`, comps `63` -> `52`.
- Other retained cases had unchanged residual but only local low-risk edge expansion.

Rejected / deferred high-risk candidates:

- Large changed-count professional certificate candidates were rejected, including `professional_cert_017`, `professional_cert_020`, `professional_cert_006`, `professional_cert_014`, and `professional_cert_015`.
- Large changed-count award/honor candidates were rejected, including `award_honor_017`, `award_honor_019`, `award_honor_020`, `award_honor_012`, and `award_honor_015`.
- Large service receipt candidates were rejected, including `service_receipt_017`, `service_receipt_008`, `service_receipt_006`, `service_receipt_018`, and `service_receipt_010`.
- Large quality certification candidates were rejected, including `quality_certification_008`, `quality_certification_005`, `quality_certification_009`, `quality_certification_012`, `quality_certification_013`, and `quality_certification_019`.
- Safe-but-not-strict `diploma_transcript_006_MIT_Official_Academic_Transcript` and `quality_certification_011_欧盟有机认证证书_-_EU_Organic_Certification_Magazine` were deferred for visual review because their max ratio / vertical growth exceeded strict thresholds.

Reports:

- Certificate dry-run report: `/tmp/pdb_certificate_residual_cover_dry_v340.json`.
- v341 applied report: `/tmp/pdb_certificate_strict_residual_cover_v341.json`.
- Before residual check: `/tmp/pdb_certificate_strict_residual_before_v341.json`.
- After residual check: `/tmp/pdb_certificate_strict_residual_after_v341.json`.
- Debug residual images: `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7/cover_residual_certificate_strict_after_v341`.

### 2026-06-05 - `20260605_logistics_strict_residual_cover_v343`

Scope: strict low-risk selected cases from `09_logistics`

BBox edge-cover correction:

- Ran OCR residual-cover dry-run over all `120` logistics cases.
- Dry-run produced `104` changed candidates.
- Applied only `3` strict candidates / `9` bbox expansions.
- No GT annotations were added or removed.
- Barcode-, grid-, and label-border-driven candidates were treated as high risk unless they passed the strict changed-count / area-ratio / shift thresholds.

Changed cases retained:

- `shipping_label_001_顺丰速运_SF_Express_-_Complex_Multi-Section_Label`
- `itinerary_003_电子行程单_Electronic_Itinerary_Receipt`
- `bill_of_lading_011_Transshipment_Bill_of_Lading_Dossier`

Residual verification:

- Selected-check text-like residual improved from `1649096` to `1640862` (gain `8234`).
- Selected-check component count improved from `419` to `416` (gain `3`).
- No selected case worsened.
- Main gains:
  - `shipping_label_001_顺丰速运_SF_Express_-_Complex_Multi-Section_Label`: `444794` -> `438971`, comps `97` -> `96`.
  - `bill_of_lading_011_Transshipment_Bill_of_Lading_Dossier`: `1026151` -> `1023740`, comps `307` -> `305`.
- `itinerary_003_电子行程单_Electronic_Itinerary_Receipt` had unchanged residual but only local low-risk edge expansion.

Rejected / deferred high-risk candidates:

- Large shipping-label candidates were rejected, including `shipping_label_017`, `018`, `019`, `010`, `003`, `013`, and `014`.
- Large customs/packing candidates were rejected, including `customs_packing_008`, `018`, `016`, and `012`.
- Large itinerary candidates were rejected, including `itinerary_018`, `005`, `020`, `016`, and `009`.
- Large ticket/hotel candidates were rejected, including `ticket_013`, `ticket_007`, `ticket_020`, `hotel_booking_005`, `hotel_booking_014`, and `hotel_booking_003`.
- Large bill-of-lading candidates were rejected, including `bill_of_lading_010`, `017`, `007`, `008`, `009`, and `019`.
- Safe-but-not-strict candidates `shipping_label_011`, `customs_packing_002`, `customs_packing_007`, and `bill_of_lading_002` were deferred for visual review because they exceed strict thresholds or touch dense table/label layouts.

Reports:

- Logistics dry-run report: `/tmp/pdb_logistics_residual_cover_dry_v342.json`.
- v343 applied report: `/tmp/pdb_logistics_strict_residual_cover_v343.json`.
- Before residual check: `/tmp/pdb_logistics_strict_residual_before_v343.json`.
- After residual check: `/tmp/pdb_logistics_strict_residual_after_v343.json`.
- Debug residual images: `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7/cover_residual_logistics_strict_after_v343`.

### 2026-06-05 - `20260605_medical_strict_residual_cover_v345`

Scope: strict low-risk selected cases from `06_medical`

BBox edge-cover correction:

- Ran OCR residual-cover dry-run over all `200` medical cases.
- Dry-run produced `193` changed candidates.
- Applied only `31` strict candidates / local bbox expansions.
- No GT annotations were added or removed.
- User-pointed high-risk cases and PET/image-placeholder residuals were not bulk-written unless they passed strict thresholds.

Changed cases retained:

- Medical reports: `medical_report_001`, `medical_report_002`, `medical_report_008`, `medical_report_010`, `medical_report_012`, `medical_report_017`
- Prescriptions: `prescription_002`, `prescription_005`, `prescription_006`, `prescription_007`, `prescription_008`, `prescription_009`, `prescription_018`
- Clinical records: `clinical_record_007`, `clinical_record_020`
- Medical bills: `medical_bill_005`, `medical_bill_011`
- Health records: `health_record_003`, `health_record_010`
- Medical certificates: `medical_certificate_003`, `medical_certificate_004`, `medical_certificate_006`, `medical_certificate_007`, `medical_certificate_011`
- Surgical records: `surgical_record_001`, `surgical_record_013`, `surgical_record_016`, `surgical_record_019`, `surgical_record_020`
- Discharge summaries: `discharge_summary_016`
- Drug instructions: `drug_instruction_015`

Residual verification:

- Selected-check text-like residual improved from `2522080` to `2409868` (gain `112212`).
- Selected-check component count improved from `458` to `399` (gain `59`).
- No selected case worsened.
- Main gains:
  - `medical_certificate_007`: `276397` -> `243517`.
  - `prescription_009`: `112910` -> `92479`, comps `65` -> `46`.
  - `medical_report_017`: `65204` -> `54240`, comps `9` -> `5`.
  - `medical_bill_011`: `87530` -> `80049`, comps `9` -> `5`.
  - `surgical_record_001`: `95589` -> `88320`, comps `10` -> `5`.
  - `clinical_record_020`: `6096` -> `0`, comps `5` -> `0`.

Rejected / deferred high-risk candidates:

- User-pointed / visually sensitive cases deferred for single-case review: `medical_report_003`, `medical_report_015`, `medical_report_016`, `prescription_003`, `prescription_013`, `prescription_019`, `clinical_record_002`, `clinical_record_004`, `medical_bill_006`, and `medical_bill_015`.
- `medical_bill_005` was retained because its v345 changes were only tiny top/bottom edge expansions and passed residual verification.
- High changed-count imaging/discharge/drug-instruction candidates were rejected, including `imaging_report_005`, `imaging_report_006`, `imaging_report_007`, `discharge_summary_006`, `discharge_summary_007`, and `drug_instruction_001` through `drug_instruction_010` where applicable.
- PET/image placeholder text and other figure-internal residuals were not converted into text GT by this pass.

Reports:

- Medical dry-run report: `/tmp/pdb_medical_residual_cover_dry_v344.json`.
- v345 applied report: `/tmp/pdb_medical_strict_residual_cover_v345.json`.
- Before residual check: `/tmp/pdb_medical_strict_residual_before_v345.json`.
- After residual check: `/tmp/pdb_medical_strict_residual_after_v345.json`.
- Debug residual images: `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7/cover_residual_medical_strict_after_v345`.

### 2026-06-05 - global residual/no-bbox snapshot after `20260605_medical_strict_residual_cover_v345`

Scope: all `1475` cases

Current review-data state:

- Build token: `20260605_medical_strict_residual_cover_v345`.
- Total items: `89784`.
- Boxed items: `88940`.
- No-bbox items: `844`.
- Low-similarity items: `7290`.

Residual audit summary:

- Full residual report: `/tmp/pdb_full_residual_after_v345.json`.
- Debug residual images: `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7/cover_residual_full_after_v345`.
- Highest residual categories:
  - `09_logistics`: `85424558` text-like area, `18618` comps.
  - `07_publishing`: `84885313` text-like area, `17467` comps.
  - `10_certificate`: `82275790` text-like area, `16572` comps.
  - `04_business`: `38876859` text-like area, `8629` comps.
  - `08_technical`: `36515652` text-like area, `4547` comps.
- Highest residual subcategories:
  - `07_publishing/01_newspaper`: `61827374` area.
  - `10_certificate/03_award_honor`: `22852966` area.
  - `09_logistics/01_shipping_label`: `19575354` area.
  - `10_certificate/05_quality_certification`: `17905459` area.
  - `10_certificate/01_diploma_transcript`: `17805232` area.
- Highest residual individual cases include `award_honor_017`, `quality_certification_009`, `newspaper_012`, `newspaper_018`, `diploma_transcript_019`, `newspaper_019`, `newspaper_003`, `quality_certification_006`, `employee_handbook_001`, and `award_honor_020`.

No-bbox concentration:

- `844` no-bbox items across `150` cases.
- Largest no-bbox clusters:
  - `slides_030_多模态文档智能系统_上下伪两页科研汇报`: `69`.
  - `shipping_label_005_COSCO_SHIPPING_-_Bill_of_Lading`: `65`.
  - `shipping_label_008_Maersk_Line_-_Container_Shipping_Manifest_集装箱货运清单`: `49`.
  - `slides_014_材料化学_晶体结构`: `46`.
  - `slides_031_Autonomous_Research_Operations_2in1`: `42`.
  - `professional_cert_016_消防工程师资格证书_-_对角线分割_Fire_Protection_Engineer_Certificate`: `38`.
  - `slides_015_DL_Systems_并行训练_ZHCN`: `38`.
  - `slides_030_Smart_Urban_Resilience_2in1`: `34`.
  - `diploma_transcript_021_Wharton_MBA_Business_Talent_Data_Atlas_v2`: `27`.

Next-pass guidance:

- Residual-heavy newspaper, award/certificate, logistics, and architecture/manual pages need single-case visual/DOM rebuilds rather than residual-cover bulk expansion.
- No-bbox repair should be handled separately from edge-cover repair, starting with the largest clusters above.

### 2026-06-05 - `20260605_all_unboxed_ranges_dry_v346`

Scope: all remaining no-bbox cases

Dry-run result:

- Ran `repair_unboxed_text_ranges.py` over all `150` cases that still contain no-bbox annotations.
- Accepted cases: `0`.
- Filled items: `0`.
- Candidate-only cases: `2`.
  - `lab_report_035_Organic_Esterification`: `3` candidate fills rejected because residual worsened from `146876` to `154466`.
  - `shipping_label_018_跨境电商集运总表_Cross-Border_Consolidation_Master_Sheet`: `11` candidate fills rejected because residual worsened from `2690904` to `2698462`.
- No files were written.

Conclusion:

- Remaining `844` no-bbox items cannot be safely solved by exact text-node Range matching.
- Future no-bbox repair should use single-case visual/DOM reconstruction, especially for slide, logistics, certificate, and business-plan clusters.

Report:

- No-bbox range dry-run report: `/tmp/pdb_all_unboxed_ranges_dry_v346.json`.

### 2026-06-05 - `20260605_slides030_dom_gated_dry_v347`

Scope: single largest no-bbox cluster `slides_030_多模态文档智能系统_上下伪两页科研汇报`

Dry-run result:

- Ran `repair_review_bboxes_dom_gated.py` on this case only.
- The candidate was rejected.
- It would have changed no-bbox from `69` to `195` and boxed count from `187` to `61`.
- Cover residual stayed `0 -> 0`, which shows residual alone is insufficient for this no-bbox cluster.

Conclusion:

- This case should not be repaired by full DOM-gated rebuild.
- The no-bbox items are mostly chart/table/case-card subitems already covered by visible parent boxes; filling them safely needs single-case visual/DOM reconstruction, not full-case rebuild.

Report:

- `/tmp/pdb_slides030_dom_gated_dry_v347.json`

### 2026-06-05 - `20260605_academic_strict_residual_cover_v349`

Scope: strict low-risk selected cases from `01_academic`

BBox edge-cover correction:

- Ran OCR residual-cover dry-run over all `180` academic cases.
- Dry-run produced `39` changed candidates.
- Applied only `7` strict candidates / local bbox expansions.
- No GT annotations were added or removed.
- Large technical-report, thesis, and conference-poster candidates were not written.

Changed cases retained:

- `academic_paper_014_药学双栏论文`
- `academic_paper_026_经济研究_面板数据`
- `technical_report_014_碳排放核查报告`
- `technical_report_022_Data_Center_Capacity`
- `research_proposal_019_省重点研发_农业`
- `research_proposal_026_ARC_Discovery_Quantum`
- `conference_poster_011_ECCV_3D重建`

Residual verification:

- Selected-check text-like residual improved from `729428` to `722161` (gain `7267`).
- Selected-check component count improved from `242` to `237` (gain `5`).
- No selected case worsened.
- Main gains:
  - `academic_paper_014_药学双栏论文`: `269401` -> `264822`, comps `117` -> `115`.
  - `conference_poster_011_ECCV_3D重建`: `61343` -> `58655`, comps `15` -> `12`.
- Other retained cases had unchanged residual but only local low-risk edge expansion.

Rejected / deferred high-risk candidates:

- High changed-count technical-report candidates were rejected, including `technical_report_007`, `technical_report_027`, `technical_report_028`, and `technical_report_029`.
- High changed-count or large-shift conference-poster candidates were rejected, including `conference_poster_017`, `018`, `019`, `027`, and `028`.
- Safe-but-not-strict candidates `research_proposal_016`, `conference_poster_004`, and `conference_poster_022` were deferred for visual review.

Reports:

- Academic dry-run report: `/tmp/pdb_academic_residual_cover_dry_v348.json`.
- v349 applied report: `/tmp/pdb_academic_strict_residual_cover_v349.json`.
- Before residual check: `/tmp/pdb_academic_strict_residual_before_v349.json`.
- After residual check: `/tmp/pdb_academic_strict_residual_after_v349.json`.
- Debug residual images: `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7/cover_residual_academic_strict_after_v349`.

### 2026-06-05 - `20260605_education_strict_residual_cover_v351`

Scope: strict low-risk selected cases from `02_education`

BBox edge-cover correction:

- Ran OCR residual-cover dry-run over all `138` education cases.
- Dry-run produced `72` changed candidates.
- Applied only `14` strict candidates / local bbox expansions.
- No GT annotations were added or removed.
- Large slide, exam, syllabus, and lab-report candidates were not written.

Changed cases retained:

- Textbooks: `textbook_015_数据结构_哈希表_ZHCN`, `textbook_016_高等数学_多元微分_泰勒展开`
- Exam papers: `exam_paper_036_Economics_Market_Macro`, `exam_paper_044_建筑与空间设计`, `exam_paper_045_深海考察与海底遗址综合判读考试`
- Slides: `slides_008_数据分析_Python`, `slides_011_Corporate_Finance_2in1_EN`, `slides_012_商业BP_SaaS`
- School notices: `school_notice_030_春季多部门联合公告墙`, `school_notice_032_奖学金评审公示材料`, `school_notice_035_校园安全与生活服务温馨提醒`
- Syllabus: `syllabus_034_Python_Software_Engineering`
- Lab reports: `lab_report_006_分析化学_滴定实验`, `lab_report_008_模拟电路_运放实验`

Residual verification:

- Selected-check text-like residual improved from `5408275` to `5343379` (gain `64896`).
- Selected-check component count improved from `1495` to `1483` (gain `12`).
- No selected case worsened.
- Main gains:
  - `slides_011_Corporate_Finance_2in1_EN`: `105139` -> `64286`, comps `29` -> `27`.
  - `school_notice_030_春季多部门联合公告墙`: `547735` -> `529427`, comps `254` -> `252`.
  - `textbook_015_数据结构_哈希表_ZHCN`: `280403` -> `277767`, comps `67` -> `64`.

Rejected / deferred high-risk candidates:

- Large slide/no-bbox cluster cases were not repaired by this pass, including `slides_007`, `slides_015`, `slides_016`, `slides_030_*`, and `slides_031`.
- Large exam/syllabus candidates were rejected, including `exam_paper_002`, `037`, `040`, `041`, `042`, `047`, `048`, `syllabus_008`, `010`, `031`, `038`, `039`, `040_*`, and `041`.
- Large lab-report candidates were rejected, including `lab_report_012`, `014`, `015`, `031`, `032`, `033_ECG_BP_Exercise`, and `036`.
- Safe-but-not-strict candidates `textbook_004`, `textbook_028`, `school_notice_005`, and `syllabus_033` were deferred for visual review.

Reports:

- Education dry-run report: `/tmp/pdb_education_residual_cover_dry_v350.json`.
- v351 applied report: `/tmp/pdb_education_strict_residual_cover_v351.json`.
- Before residual check: `/tmp/pdb_education_strict_residual_before_v351.json`.
- After residual check: `/tmp/pdb_education_strict_residual_after_v351.json`.
- Debug residual images: `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7/cover_residual_education_strict_after_v351`.

### 2026-06-05 - `20260605_legalgov_strict_residual_cover_v353`

Scope: strict low-risk selected cases from `03_legal_gov`

BBox edge-cover correction:

- Ran OCR residual-cover dry-run over all `151` legal/government cases.
- Dry-run produced `15` changed candidates.
- Applied only `2` strict candidates / local bbox expansions.
- No GT annotations were added or removed.
- Large legal text, license/permit, and legislation candidates were not written.

Changed cases retained:

- `accident_report_003_危化品泄漏快报`
- `accident_report_005_Workplace_Incident_EN`

Residual verification:

- Selected-check text-like residual improved from `346251` to `317679` (gain `28572`).
- Selected-check component count improved from `76` to `67` (gain `9`).
- No selected case worsened.
- Main gain:
  - `accident_report_005_Workplace_Incident_EN`: `221782` -> `193210`, comps `46` -> `37`.
- `accident_report_003_危化品泄漏快报` had unchanged residual but only local low-risk edge expansion.

Rejected / deferred high-risk candidates:

- `legislation_002_EU_GDPR_Excerpt`, `accident_report_015_US_MSHA_Mine_Accident`, `license_permit_014_Business_License_US`, `legislation_021_人大表决结果公告`, and `accident_report_010_UK_MAIB_Marine_Report` were rejected because their candidates involved large growth, large shifts, or high changed counts.
- Safe-but-not-strict `license_permit_015_Liquor_License_EN` and `legislation_023_食品安全监督抽检通报` were deferred for visual review.

Reports:

- Legal/government dry-run report: `/tmp/pdb_legalgov_residual_cover_dry_v352.json`.
- v353 applied report: `/tmp/pdb_legalgov_strict_residual_cover_v353.json`.
- Before residual check: `/tmp/pdb_legalgov_strict_residual_before_v353.json`.
- After residual check: `/tmp/pdb_legalgov_strict_residual_after_v353.json`.
- Debug residual images: `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7/cover_residual_legalgov_strict_after_v353`.

### 2026-06-05 - `20260605_newspaper_dom_gated_dry_v354`

Scope: `07_publishing/01_newspaper`

Dry-run result:

- Ran `repair_review_bboxes_dom_gated.py` over all `20` newspaper cases.
- Accepted cases: `0`.
- Total text-like residual was unchanged: `60346293` -> `60346293`.
- No-bbox total was unchanged: `0` -> `0`.
- No files were written.

Conclusion:

- Existing DOM-gated full rebuild does not improve newspaper cases.
- Newspaper residual should not be attacked by automatic full-case DOM rebuild; it needs a dedicated visual/layout strategy or targeted manual case repair.

Report:

- `/tmp/pdb_newspaper_dom_gated_dry_v354.json`.

### 2026-06-05 - `20260605_award_honor_dom_gated_dry_v355`

Scope: `10_certificate/03_award_honor`

Dry-run result:

- Ran `repair_review_bboxes_dom_gated.py` over all `20` award/honor cases.
- Accepted cases: `0`.
- No files were written.
- Positive-gain-but-rejected cases:
  - `award_honor_001_员工月度之星`: residual `386880` -> `320196`, but components worsened `96` -> `131`.
  - `award_honor_007_2025_China_ESG_Excellence_Award`: residual `12213` -> `0`, components `3` -> `0`, but gain was below the dry-run `min-gain=50000` threshold.
  - `award_honor_013_2025中国科技行业十大领军人物`: residual `1293` -> `0`, components `1` -> `0`, but gain was below the dry-run `min-gain=50000` threshold.
- Clear rejected/worse cases included `award_honor_005`, `006`, `008`, `011`, `014`, `016`, `018`, and `020`; several would increase residual or no-bbox.

Conclusion:

- Full DOM-gated rebuild is unsafe for the award/honor subcategory.
- `award_honor_007` and `award_honor_013` can be considered later as low-gain single-case checks; the rest need visual/manual strategies.

Report:

- `/tmp/pdb_award_honor_dom_gated_dry_v355.json`.

### 2026-06-05 - `20260605_award_honor_small_dom_gated_v357`

Scope: two low-gain award/honor single-case DOM-gated repairs

BBox correction:

- Ran low-threshold single-case DOM-gated dry-run `20260605_award_honor_small_dom_gated_dry_v356` for:
  - `award_honor_007_2025_China_ESG_Excellence_Award`
  - `award_honor_013_2025中国科技行业十大领军人物`
- Both cases were accepted in dry-run with `min-gain=0`.
- Wrote the two accepted cases with token `20260605_award_honor_small_dom_gated_v357`.
- No GT annotations were added or removed.
- No-bbox counts stayed `0 -> 0` for both cases.

Residual verification:

- Selected-check text-like residual improved from `13717` to `0` (gain `13717`).
- Selected-check component count improved from `4` to `0` (gain `4`).
- No selected case worsened.
- Per-case gains:
  - `award_honor_007_2025_China_ESG_Excellence_Award`: `12213` -> `0`, comps `3` -> `0`.
  - `award_honor_013_2025中国科技行业十大领军人物`: `1504` -> `0`, comps `1` -> `0`.

Reports:

- Dry-run report: `/tmp/pdb_award_honor_small_dom_gated_dry_v356.json`.
- v357 applied report: `/tmp/pdb_award_honor_small_dom_gated_v357.json`.
- Before residual check: `/tmp/pdb_award_honor_small_before_v357.json`.
- After residual check: `/tmp/pdb_award_honor_small_after_v357.json`.
- Debug residual images: `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7/cover_residual_award_honor_small_after_v357`.

### 2026-06-05 - `20260605_shipping_label_dom_gated_dry_v358`

Scope: `09_logistics/01_shipping_label`

Dry-run result:

- Ran `repair_review_bboxes_dom_gated.py` over all `20` shipping-label cases.
- Accepted cases: `0`; no files were written.
- Aggregate text-like residual would worsen from `19209782` to `23088482`.
- Component count would worsen from `3613` to `4340`.
- No-bbox count would worsen from `142` to `1563`.
- Boxed item count would drop from `4127` to `2706`.
- Largest no-bbox regressions included:
  - `shipping_label_020_综合物流调度面单_中式竖横混排`: `1` -> `212` no-bbox, boxed `519` -> `308`.
  - `shipping_label_017_国际多式联运货物运单_International_Multimodal_Transport_Consignment_Note`: `0` -> `202` no-bbox, boxed `408` -> `206`.
  - `shipping_label_019_LOGISTICS_TODAY_物流纵横_Exhibition_Materials_Shipping_Plan`: `0` -> `152` no-bbox, boxed `402` -> `250`.
  - `shipping_label_018_跨境电商集运总表_Cross-Border_Consolidation_Master_Sheet`: `11` -> `147` no-bbox, boxed `489` -> `353`.

Conclusion:

- Full DOM-gated rebuild is unsafe for `shipping_label`.
- Future shipping-label work should use targeted visual/manual repair, not full-case DOM replacement.

Report:

- `/tmp/pdb_shipping_label_dom_gated_dry_v358.json`.

### 2026-06-05 - `20260605_taxdoc_template_dry_v359`

Scope: `05_finance/04_tax_document`

Dry-run result:

- Ran `repair_tax_document_template_batch.py` over the tax-document subcategory.
- Changed annotations: `0`.
- No files were written.

Conclusion:

- The existing template-match guard is too narrow to catch the remaining tax-document review/UI complaints such as `tax_document_008` and `tax_document_009`.
- Continue using case-level visual/DOM checks for this subcategory; do not assume the template pass has fixed all top-line drift.

Report:

- `/tmp/pdb_taxdoc_template_dry_v359.json`.

### 2026-06-05 - `20260605_finance_abs_dom_gated_dry_v360`

Scope: `05_finance`, excluding `01_invoice_receipt`

Dry-run result:

- Ran `repair_finance_bboxes_abs_dom_gated.py` over `180` finance cases.
- Residual gate accepted `10` candidates, but geometry screening found that `9` of them enlarged `header` boxes into large multi-thousand-pixel regions.
- Rejected broad-header candidates despite residual gains:
  - `financial_report_003`
  - `financial_report_004`
  - `financial_report_020`
  - `tax_document_013`
  - `tax_document_014`
  - `utility_bill_002`
  - `securities_statement_005`
  - `audit_report_007`
  - `fund_prospectus_018`
- Kept only one safe candidate for actual write:
  - `tax_document_016`, with no no-bbox increase and small geometry changes only.

Conclusion:

- Residual gain alone is insufficient for finance cases because broad header boxes can hide residual while making the review overlay obviously wrong.
- Future finance auto-writes must include a geometry sanity check: reject candidates where header/text boxes expand into full-page or multi-section regions.

Report:

- `/tmp/pdb_finance_abs_dom_gated_dry_v360.json`.

### 2026-06-05 - `20260605_tax_document016_abs_dom_gated_v361`

Scope: `05_finance/04_tax_document/tax_document_016`

BBox correction:

- Wrote the single safe finance candidate from v360.
- No GT annotations were added or removed.
- No-bbox count stayed `0 -> 0`.
- Boxed count stayed `9 -> 9`.
- Corrected small top-line/text-block drift:
  - `#2` text_block moved from `[178, 229, 3422, 277]` to `[178, 259, 3422, 307]`.
  - `#3` text_block moved from `[178, 351, 3422, 399]` to `[178, 312, 3422, 360]`.

Residual verification:

- v361 selected-case residual: `text_like=4275`, `components=11`.
- The applied report measured the candidate improvement from `26598` to `4275`.

Reports:

- v361 applied report: `/tmp/pdb_tax_document016_abs_dom_gated_v361.json`.
- After residual check: `/tmp/pdb_tax_document016_residual_after_v361.json`.
- Debug residual images: `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7/cover_residual_tax_document016_after_v361`.

### 2026-06-05 - `20260605_full_residual_after_v361`

Scope: all `1475` cases

Audit result:

- Full-library residual snapshot after v361 was generated.
- Current meta at snapshot time:
  - `88940` boxed
  - `844` no-bbox
  - `7269` low similarity
- Largest residual categories:
  - `09_logistics`: `85424558`
  - `07_publishing`: `84885313`
  - `10_certificate`: `82262073`
  - `04_business`: `38876859`
  - `08_technical`: `36515652`
- Largest residual subcategories:
  - `07_publishing/01_newspaper`: `61827374`
  - `10_certificate/03_award_honor`: `22839249`
  - `09_logistics/01_shipping_label`: `19575354`
  - `10_certificate/05_quality_certification`: `17905459`
  - `10_certificate/01_diploma_transcript`: `17805232`
- Remaining no-bbox total: `844` across `150` cases.
- Largest no-bbox clusters remained:
  - `slides_030_多模态文档智能系统_上下伪两页科研汇报`: `69`
  - `shipping_label_005_COSCO_SHIPPING_-_Bill_of_Lading`: `65`
  - `shipping_label_008_Maersk_Line_-_Container_Shipping_Manifest_集装箱货运清单`: `49`
  - `slides_014_材料化学_晶体结构`: `46`
  - `slides_031_Autonomous_Research_Operations_2in1`: `42`

Report:

- `/tmp/pdb_full_residual_after_v361.json`.
- Debug residual images: `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7/cover_residual_full_after_v361`.

### 2026-06-05 - `20260605_technical_residual_cover_dry_v362`

Scope: `08_technical`

Dry-run result:

- Ran `repair_review_bboxes_residual_cover.py` over all `110` technical cases.
- Cases with candidate expansions: `84`.
- Strict geometry screening accepted only `1` case.
- Six additional cases were near-safe but not written because at least one geometry threshold exceeded the strict band:
  - `product_manual_012_Drone_Flight_Guide_EN`
  - `api_reference_006_Payment_API`
  - `architecture_diagram_006_K8s集群架构`
  - `architecture_diagram_014_Event_Driven_Architecture`
  - `release_notes_014_Windows_Update_KB`
- Many candidates had large title/header expansions, so they were rejected despite possible cover improvement.

Conclusion:

- Technical documents need a strict geometry gate. OCR residual-cover candidates are common, but most are too broad for reliable automatic writing.

Report:

- `/tmp/pdb_technical_residual_cover_dry_v362.json`.

### 2026-06-05 - `20260605_technical_strict_residual_cover_v363`

Scope: `08_technical/05_release_notes/release_notes_017_Kubernetes_Release`

BBox correction:

- Wrote the single strict technical residual-cover candidate from v362.
- No GT annotations were added or removed.
- Boxed/no-bbox counts stayed unchanged globally.
- Expanded one body text block slightly to include the final line `smoother upgrades.`
- Nudged one `code_txt` block by 1 px horizontally to cover exposed command text.

Residual verification:

- v361 full snapshot residual for this case: `82043` text-like area, `17` components.
- v363 selected check residual: `68924` text-like area, `15` components.

Reports:

- v363 applied report: `/tmp/pdb_technical_strict_residual_cover_v363.json`.
- After residual check: `/tmp/pdb_technical_release017_after_v363.json`.
- Debug residual images: `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7/cover_residual_technical_release017_after_v363`.

### 2026-06-05 - `20260605_business_residual_cover_dry_v364`

Scope: `04_business`

Dry-run result:

- Ran `repair_review_bboxes_residual_cover.py` over all `160` business cases.
- Cases with candidate expansions: `89`.
- Strict geometry screening accepted only `2` cases.
- Five additional near-safe cases were not written because they exceeded at least one strict threshold:
  - `contract_021_Smart_Port_Logistics`
  - `formal_letter_020_Notice_of_Arbitration_ENZH`
  - `meeting_memo_014_Board_Audit_Committee_EN`
  - `meeting_memo_017_薪酬绩效委员会纪要`
  - `resume_026_科研型候选人履历墙`
- Many candidates had large title/header/table expansions and were rejected.

Conclusion:

- Business pages contain many OCR expansion opportunities, but most are too broad for automatic writing.
- Strict small expansions only should be applied unless a case is visually inspected.

Report:

- `/tmp/pdb_business_residual_cover_dry_v364.json`.

### 2026-06-05 - `20260605_business_strict_residual_cover_v365`

Scope: two strict `04_business` residual-cover repairs

BBox correction:

- Wrote the two strict candidates from v364:
  - `04_business/05_resume/resume_015_资深翻译项目经理简历`
  - `04_business/07_employee_handbook/employee_handbook_010_Workplace_Safety`
- No GT annotations were added or removed.
- Boxed/no-bbox counts stayed unchanged globally.
- Per-case corrections:
  - `resume_015`: expanded `#26` table upward from `[158, 2286, 2323, 2733]` to `[158, 2224, 2323, 2733]` to cover the `资质证明` row.
  - `employee_handbook_010`: expanded `#16` table upward from `[130, 2394, 2062, 2931]` to `[130, 2340, 2066, 2931]` to cover exposed PPE/N95 row text.

Residual verification:

- `resume_015`: v361 full snapshot residual `265346` -> v365 selected check `131992`; components `14` -> `13`.
- `employee_handbook_010`: v361 full snapshot residual `229775` -> v365 selected check `216382`; components `66` -> `59`.

Reports:

- v365 applied report: `/tmp/pdb_business_strict_residual_cover_v365.json`.
- After residual check: `/tmp/pdb_business_strict_after_v365.json`.
- Debug residual images: `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7/cover_residual_business_strict_after_v365`.

### 2026-06-05 - `20260605_finance_residual_cover_dry_v366`

Scope: `05_finance`

Dry-run result:

- Ran `repair_review_bboxes_residual_cover.py` over all `212` finance cases.
- Cases with candidate expansions: `150`.
- Strict geometry screening accepted only `1` case.
- Seven additional near-safe cases were not written because they exceeded at least one strict threshold:
  - `invoice_receipt_009`
  - `invoice_receipt_015`
  - `invoice_receipt_017`
  - `bank_statement_018`
  - `utility_bill_019`
  - `utility_bill_020`
  - `credit_report_014`
- Many rejected candidates were table expansions with large horizontal growth, including finance cases the user had previously flagged as visually fragile.

Conclusion:

- Finance OCR residual-cover must remain very conservative. It is not suitable for fixing bank/tax/credit coordinate-drift cases; those need targeted DOM/manual work.

Report:

- `/tmp/pdb_finance_residual_cover_dry_v366.json`.

### 2026-06-05 - `20260605_finance_strict_residual_cover_v367`

Scope: `05_finance/01_invoice_receipt/invoice_receipt_008`

BBox correction:

- Wrote the single strict finance residual-cover candidate from v366.
- No GT annotations were added or removed.
- Boxed/no-bbox counts stayed unchanged globally.
- Expanded `#18` table upward by 6 px from `[58, 570, 3242, 1792]` to `[58, 564, 3242, 1792]` to cover the shipping/import row edge.

Residual verification:

- v367 selected residual remained `167169` text-like area and `61` components, so this should be considered a small geometric correction rather than a measurable residual reduction.

Reports:

- v367 applied report: `/tmp/pdb_finance_strict_residual_cover_v367.json`.
- After residual check: `/tmp/pdb_finance_invoice008_after_v367.json`.
- Debug residual images: `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7/cover_residual_finance_invoice008_after_v367`.

### 2026-06-05 - `20260605_quality_cert_dom_gated_dry_v368`

Scope: `10_certificate/05_quality_certification`

Dry-run result:

- Ran `repair_review_bboxes_dom_gated.py` over all `20` quality-certification cases.
- Accepted cases: `0`; no files were written.
- Eight cases would worsen text-like residual.
- One case would introduce a new no-bbox:
  - `quality_certification_008_GMP药品生产质量管理规范认证`: `0` -> `1` no-bbox.
- Largest worsening examples:
  - `quality_certification_010_UL认证标识卡_-_Embossed_Metal_Nameplate`: residual `301725` -> `1830261`, components `71` -> `963`.
  - `quality_certification_006_FDA_510_k_Clearance_Letter`: residual `4057428` -> `5416696`, components `1300` -> `1748`.
  - `quality_certification_015_医疗器械注册证`: residual `349955` -> `1652995`, components `43` -> `236`.
  - `quality_certification_016_DNV船级社认证`: residual `903824` -> `1872813`, components `98` -> `310`.
  - `quality_certification_011_欧盟有机认证证书_-_EU_Organic_Certification_Magazine`: residual `2440595` -> `3205436`, components `622` -> `983`.
- Small positive-gain cases were still rejected because gains were below threshold or components worsened.

Conclusion:

- Full DOM-gated rebuild is unsafe for `quality_certification`.
- This subcategory needs dedicated visual/manual repair or a more local element-level strategy.

Report:

- `/tmp/pdb_quality_cert_dom_gated_dry_v368.json`.

### 2026-06-05 - `20260605_diploma_dom_gated_dry_v369`

Scope: `10_certificate/01_diploma_transcript`

Dry-run result:

- Ran `repair_review_bboxes_dom_gated.py` over all `21` diploma/transcript cases.
- Accepted cases: `0`; no files were written.
- Aggregate residual would worsen from `17547114` to `19438014`.
- No-bbox count would regress heavily from `36` to `1367`, while boxed count would drop from `5270` to `3939`.
- Largest no-bbox regressions:
  - `diploma_transcript_017_清_华_大_学`: no-bbox `3` -> `192`, boxed `457` -> `268`, residual `1571793` -> `1956252`.
  - `diploma_transcript_021_Wharton_MBA_Business_Talent_Data_Atlas_v2`: no-bbox `27` -> `194`, boxed `304` -> `137`, residual `808445` -> `881162`.
  - `diploma_transcript_020_Official_Academic_Dossier`: no-bbox `2` -> `159`, boxed `570` -> `413`, residual `1677483` -> `1978107`.
  - `diploma_transcript_018_diploma_transcript_018_Medical_School_Full_Transcript`: no-bbox `0` -> `120`, boxed `416` -> `296`, residual `294252` -> `300029`.
  - `diploma_transcript_007_深圳职业技术大学_专科毕业证书暨学业档案`: no-bbox `0` -> `114`, boxed `232` -> `118`, residual `723475` -> `1064856`.
  - `diploma_transcript_008_The_Wharton_School`: no-bbox `1` -> `91`, boxed `333` -> `243`, residual `176824` -> `243599`.
  - `diploma_transcript_012_Doctor_of_Philosophy_Research_Panorama_Certificate`: no-bbox `0` -> `89`, boxed `231` -> `142`, residual `821331` -> `919367`.
  - `diploma_transcript_019_diploma_transcript_019_研究生完整成绩单_中英对照`: no-bbox `0` -> `61`, boxed `355` -> `294`, residual `4814225` -> `4859159`.

Conclusion:

- Full DOM-gated rebuild is unsafe for `diploma_transcript`.
- These layouts need targeted/manual correction; do not apply broad DOM rebuilds to this subcategory.

Report:

- `/tmp/pdb_diploma_dom_gated_dry_v369.json`.

### 2026-06-05 - `20260605_professional_cert_dom_gated_dry_v370`

Scope: `10_certificate/02_professional_cert`

Dry-run result:

- Ran `repair_review_bboxes_dom_gated.py` over all `22` professional-certificate cases.
- Accepted cases: `0`; no files were written.
- Aggregate residual would worsen from `11634350` to `11768931`.
- Components would worsen from `2583` to `2588`.
- No-bbox would regress from `38` to `159`, while boxed count would drop from `2730` to `2609`.
- Largest no-bbox regressions:
  - `professional_cert_021_一级建造师注册证书_工程能力数据面板`: no-bbox `0` -> `68`, boxed `103` -> `35`, residual `763526` -> `852810`.
  - `professional_cert_022_中医执业医师资格证书_临床能力与传承数据系统`: no-bbox `0` -> `40`, boxed `80` -> `40`, residual `188108` -> `198833`.
  - `professional_cert_016_消防工程师资格证书_-_对角线分割_Fire_Protection_Engineer_Certificate`: no-bbox `38` -> `43`, boxed `95` -> `90`, residual `310113` -> `348711`.
  - `professional_cert_019_军事技术等级评定_-_军事机密档案_Military_Technical_Grade_Assessment`: no-bbox `0` -> `4`, boxed `216` -> `212`, residual `1029985` -> `1039892`.
- The only positive residual-gain examples still introduced no-bbox:
  - `professional_cert_018_International_PE_Mutual_Recognition_-_Color-Coded_Zone_Board`: residual `17924` -> `0`, but no-bbox `0` -> `1`.
  - `professional_cert_013_AWS_Solutions_Architect_Professional_-_Tech_App_Style`: residual `12076` -> `7629`, but no-bbox `0` -> `1`.

Conclusion:

- Full DOM-gated rebuild is unsafe for `professional_cert`.
- Even apparently small residual gains can hide annotation loss; use manual/local fixes only.

Report:

- `/tmp/pdb_professional_cert_dom_gated_dry_v370.json`.

### 2026-06-05 - `20260605_service_receipt_dom_gated_dry_v371`

Scope: `10_certificate/04_service_receipt`

Dry-run result:

- Ran `repair_review_bboxes_dom_gated.py` over all `21` service-receipt cases.
- Accepted cases: `0`; no files were written.
- Aggregate residual would worsen from `11610602` to `12428559`.
- Components would worsen from `2458` to `2557`.
- No-bbox would regress from `3` to `407`, while boxed count would drop from `3511` to `3107`.
- Largest no-bbox regressions:
  - `service_receipt_021_中国工商银行_-_金融交易与风控智能中枢`: no-bbox `1` -> `128`, boxed `279` -> `152`, residual `955439` -> `1161904`.
  - `service_receipt_020_国际会展服务结算单_Exhibition_Service_Settlement`: no-bbox `0` -> `109`, boxed `375` -> `266`, residual `743400` -> `826393`.
  - `service_receipt_025_物业维修服务回执_-_万科物业`: no-bbox `0` -> `87`, boxed `286` -> `199`, residual `2353792` -> `2407655`.
  - `service_receipt_017_装修工程结算书_Renovation_Project_Settlement`: no-bbox `0` -> `52`, boxed `257` -> `205`, residual `1648699` -> `1688933`.
  - `service_receipt_007_上海瑞金医院门诊收据_Shanghai_Ruijin_Hospital_Outpatient_Receipt`: no-bbox `0` -> `14`, boxed `218` -> `204`, residual `669848` -> `761186`.

Conclusion:

- Full DOM-gated rebuild is unsafe for `service_receipt`.
- Many receipts have dense table or carbon-copy layouts where DOM matching drops valid GT boxes.

Report:

- `/tmp/pdb_service_receipt_dom_gated_dry_v371.json`.

### 2026-06-05 - `20260605_bill_lading_dom_gated_dry_v372`

Scope: `09_logistics/06_bill_of_lading`

Dry-run result:

- Ran `repair_review_bboxes_dom_gated.py` over all `20` bill-of-lading cases.
- Accepted cases: `0`; no files were written.
- Aggregate residual would worsen from `16023990` to `18574619`.
- Components would worsen from `3348` to `3510`.
- No-bbox would regress from `14` to `1256`, while boxed count would drop from `3823` to `2581`.
- Largest no-bbox regressions:
  - `bill_of_lading_020_综合物流主提单_Master_Bill_of_Lading_-_UILG-MBL-2026-SH-00392`: no-bbox `0` -> `223`, boxed `413` -> `190`, residual `1386574` -> `1781187`.
  - `bill_of_lading_010_冷链药品运输提单_Cold_Chain_Pharmaceutical_Transport_Bill`: no-bbox `0` -> `178`, boxed `394` -> `216`, residual `640118` -> `1008820`.
  - `bill_of_lading_016_Ocean_Freight_Mosaic_Dashboard`: no-bbox `1` -> `126`, boxed `214` -> `89`, residual `456063` -> `605476`.
  - `bill_of_lading_018_危险品海运提单_Dangerous_Goods_Ocean_Bill_of_Lading`: no-bbox `0` -> `119`, boxed `353` -> `234`, residual `1182686` -> `1236841`.
  - `bill_of_lading_009_散货海运提单_Bulk_Cargo_Ocean_Bill_of_Lading`: no-bbox `13` -> `107`, boxed `249` -> `155`, residual `972830` -> `1290926`.
  - `bill_of_lading_017_联合运输提单_Combined_Transport_Bill_of_Lading_AGTC-PA-2026-SH-00847`: no-bbox `0` -> `88`, boxed `281` -> `193`, residual `2844041` -> `3149587`.
- Apparent positive-gain examples were still rejected because they introduced no-bbox:
  - `bill_of_lading_005_Cold_Chain_Pharmaceutical_Transport_Dashboard`: residual `8661` -> `0`, but no-bbox `0` -> `5`.
  - `bill_of_lading_015_LNG液化天然气船运提单_LNG_Tanker_Bill_of_Lading`: residual `1220` -> `0`, but no-bbox `0` -> `65`.

Conclusion:

- Full DOM-gated rebuild is unsafe for `bill_of_lading`.
- This subcategory needs targeted/manual table and label repair rather than broad DOM remapping.

Report:

- `/tmp/pdb_bill_lading_dom_gated_dry_v372.json`.

### 2026-06-05 - `20260605_finance_targeted_dry_v373`

Scope: selected case-aware `05_finance` targeted rules in `repair_finance_targeted_cases.py`

Dry-run result:

- Ran the finance targeted repair script over its selected case-aware list.
- No candidate introduced no-bbox or low-sim in the dry-run.
- Actual bbox differences were limited to:
  - `financial_report_015`: 4 reference-note boxes would be narrowed.
  - `bank_statement_009`: 1 footer/notice box would be shortened by 3 px.
  - `tax_document_006`: 11 mostly title/header boxes would be tightened.
  - `tax_document_008`: 6 top/bottom note/title boxes would be tightened.
- `utility_bill_015` reported `2` changed annotations internally, but JSON diff showed no actual bbox/field difference.

Verification / decision:

- Temporary residual check rejected `financial_report_015` and `tax_document_006` because their tightened boxes exposed residual:
  - `financial_report_015`: residual `6815` -> `8095`, components `6` -> `10`.
  - `tax_document_006`: residual `505160` -> `520236`, components `10` -> `17`.
- `bank_statement_009` only changed one footer box from `[1826, 2725, 2841, 2809]` to `[1826, 2725, 2841, 2806]`; this does not address the earlier user screenshot showing a historical large `#24` table drift, and current `#24` is already `[715, 754, 2885, 2601]`.
- `tax_document_008` had residual unchanged at `0` and visually fixed the top/title/doc-number boxes without adding no-bbox.

Conclusion:

- Do not apply the full finance targeted pass blindly.
- Apply only the confirmed `tax_document_008` correction in v374.

Reports / diagnostics:

- Dry-run report: `/tmp/pdb_finance_targeted_dry_v373.json`.
- Temporary applied report: `/tmp/pdb_finance_targeted_tmp_v373.json`.
- Before residual report: `/tmp/pdb_finance_targeted_before_v373_residual.json`.
- Temporary residual report: `/tmp/pdb_finance_targeted_tmp_v373_residual.json`.
- Top crop before/after diagnostics: `/tmp/tax008_top_before_v373.jpg`, `/tmp/tax008_top_tmp_v373.jpg`.

### 2026-06-05 - `20260605_tax_document008_targeted_v374`

Scope: `05_finance/04_tax_document/tax_document_008`

Code/support change:

- Added `--only-page-id` to `scripts/repair_finance_targeted_cases.py` so confirmed case-level finance fixes can be applied without pulling in rejected cases from the same targeted script.

BBox corrections:

- Wrote only `tax_document_008` using the case-aware targeted rules.
- No GT annotations were added or removed.
- Global counts stayed unchanged: `88940` boxed, `844` no-bbox, `7269` low-sim.
- Case counts stayed `27/27` boxed, `0` no-bbox, `0` low-sim.
- Tightened the following boxes:
  - `#1` title `房产税纳税通知书`: `[1405, 458, 2168, 571]` -> `[1405, 458, 2168, 553]`.
  - `#14` title `四、缴纳方式 Payment Methods`: `[762, 3246, 2838, 3409]` -> `[762, 3246, 2838, 3388]`.
  - `#20` note text: `[799, 4422, 2801, 4584]` -> `[799, 4436, 2801, 4584]`.
  - `#22` note text: `[799, 4616, 2801, 4765]` -> `[799, 4616, 2801, 4764]`.
  - `#23` footer/header note: `[799, 4709, 2801, 4820]` -> `[799, 4709, 2801, 4812]`.
  - `#26` doc-number line: `[1025, 625, 2580, 684]` -> `[1025, 625, 2580, 676]`.

Residual / visual verification:

- After residual check: `text_like=0`, `components=0`.
- Top overlay diagnostic confirmed the header/title/doc-number boxes are no longer broad page-spanning boxes.

Reports / diagnostics:

- Dry-run report: `/tmp/pdb_tax_document008_targeted_dry_v374.json`.
- Applied report: `/tmp/pdb_tax_document008_targeted_v374.json`.
- After residual report: `/tmp/pdb_tax_document008_after_v374_residual.json`.
- Debug residual dir: `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7/cover_residual_tax008_after_v374`.
- Top overlay diagnostic: `/tmp/tax008_top_after_v374.jpg`.

### 2026-06-05 - `20260605_financial_report013_targeted_v375`

Scope: `05_finance/02_financial_report/financial_report_013`

Code/support change:

- Added a case-aware `financial_report_013` branch to `scripts/repair_finance_targeted_cases.py`.
- The rule computes the union of the five visible SVG text fragments in `.arrows-layer svg text` for the composite annotation:
  - `EBITDA feeds into EV/EBITDA calc`
  - `+ $280M Series E`
  - `valuation bridge →`
  - `✓`
  - `✗ → revised`

BBox correction:

- Wrote only `financial_report_013`.
- No GT annotations were added or removed.
- Global counts stayed unchanged: `88940` boxed, `844` no-bbox, `7269` low-sim.
- Case counts stayed `34/34` boxed, `0` no-bbox, `0` low-sim.
- Corrected `#5` text_block from a whole-page false box to the SVG annotation union:
  - `[0, 0, 3306, 4356]` -> `[1346, 944, 2587, 1816]`.

Verification note:

- Residual changed from the previous `0` to `6667` text-like area / `10` components because the old incorrect whole-page box masked unrelated arrows, grid/background, and non-`#5` content.
- This residual increase is expected and accepted: the goal here is bbox-instance alignment, not preserving a false full-page cover.
- Overlay diagnostic confirmed the large all-page frame is gone; the remaining union box reflects the original GT choice to store several scattered SVG notes as one annotation.

Reports / diagnostics:

- Dry-run report: `/tmp/pdb_financial_report013_targeted_dry_v375.json`.
- Applied report: `/tmp/pdb_financial_report013_targeted_v375.json`.
- Before residual report: `/tmp/pdb_financial_report013_before_v374_residual.json`.
- After residual report: `/tmp/pdb_financial_report013_after_v375_residual.json`.
- Overlay before/after diagnostics: `/tmp/financial_report013_overlay_current_v374.jpg`, `/tmp/financial_report013_overlay_after_v375.jpg`.

### 2026-06-05 - finance anomaly review after v375

Scope: finance large-box anomaly scan

Reviewed / left unchanged:

- `05_finance/10_credit_report/credit_report_002 #47`
  - Current bbox: `[1439, 335, 2913, 2416]`.
  - At first glance this looks like a very large wrong box, but Range/getClientRects shows the original paragraph `Result: CLEAR — 无犯罪记录... Public Security Bureau... Limitation: PRC criminal record certificates...` flows from the bottom of the middle column into the top of the right column.
  - The large bbox is therefore the union of one original GT text_block split by CSS/multicolumn flow, not a coordinate-system drift.
  - Left unchanged; do not "fix" it by cropping only the lower PRC block unless the GT is explicitly split into separate annotations.

Diagnostics:

- Overlay diagnostic: `/tmp/credit_report002_overlay_current_v375.jpg`.

### 2026-06-05 - `20260605_resume022_targeted_v376`

Scope: `04_business/05_resume/resume_022_Draft_Review_CV`

Code/support change:

- Added `scripts/repair_business_targeted_cases.py` for case-aware business repairs that should not be handled by broad residual/DOM passes.

BBox correction:

- Wrote only `resume_022_Draft_Review_CV`.
- No GT annotations were added or removed.
- Global boxed/no-bbox counts stayed unchanged; global low-sim improved by 1: `7269` -> `7268`.
- Case counts changed from `105 total / 97 boxed / 8 no-bbox / 35 low-sim` to `105 total / 97 boxed / 8 no-bbox / 34 low-sim`.
- Corrected `#3` text_block, the first right-side Review Notes card:
  - Text: `Prof. Hayes [C1] Profile too generic. Add quantified impact statement. Lead with strongest result.`
  - `[0, 508, 2382, 2470]` -> `[2093, 167, 2366, 279]`.

Residual / visual verification:

- After residual check: `611703` text-like area / `158` components.
- Residual remains high because the case still contains 8 no-bbox items and many review/comment/revision marks; the specific `#3` broad-frame error is fixed.
- Overlay diagnostic confirms `#3` now covers only the right-side C1 Review Notes card.

Reports / diagnostics:

- Dry-run report: `/tmp/pdb_resume022_targeted_dry_v376.json`.
- Applied report: `/tmp/pdb_resume022_targeted_v376.json`.
- After residual report: `/tmp/pdb_resume022_after_v376_residual.json`.
- Debug residual dir: `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7/cover_residual_resume022_after_v376`.
- Overlay before/after diagnostics: `/tmp/resume022_overlay_current_v375.jpg`, `/tmp/resume022_overlay_after_v376.jpg`.

### 2026-06-05 - `20260605_resume022_nobbox_v377`

Scope: `04_business/05_resume/resume_022_Draft_Review_CV`

Code/support change:

- Extended `scripts/repair_business_targeted_cases.py` for the remaining visible no-bbox items in `resume_022`.
- Added a pixel-based footer fallback because the footer DOM rect lands below the released PNG crop; the visible footer text is detected from bottom-band gray pixels instead.

BBox additions/corrections:

- Wrote only `resume_022_Draft_Review_CV`.
- Added bboxes for all 8 previously no-bbox annotations; no GT annotations were added or removed.
- Global no-bbox improved by 8: `844` -> `836`; global boxed improved by 8: `88940` -> `88948`; global low-sim stayed `7268`.
- Case counts improved from `105 total / 97 boxed / 8 no-bbox / 34 low-sim` to `105 total / 105 boxed / 0 no-bbox / 34 low-sim`.
- Added:
  - `#14` right review note C12: `None` -> `[2093, 1309, 2366, 1421]`.
  - `#40` C2 resolved callout: `None` -> `[137, 963, 1022, 1003]`.
  - `#54` section title `4 Selected Publications UPDATED v2.3`: `None` -> `[1058, 656, 2026, 721]`.
  - `#59` section title `5 Technical Strengths 8 REFORMATTED v2.3`: `None` -> `[1058, 1405, 2026, 1469]`.
  - `#62` section title `6 Project Metrics & Performance Summary 10`: `None` -> `[1058, 1902, 2026, 1967]`.
  - `#63` metrics formula block: `None` -> `[1058, 1957, 2026, 2084]`.
  - `#77` section title `8 Open Issues / Suggested Edits / Attachment Reminders`: `None` -> `[83, 2979, 2026, 3044]`.
  - `#104` bottom footer/header: `None` -> `[84, 3180, 2024, 3208]`.

Residual / visual verification:

- Residual improved from v376 `611703` text-like area / `158` components to v377 `502985` / `140`.
- Overlay diagnostic confirms the added boxes are on visible review notes, section headings, formula block, and footer, not hidden content.

Reports / diagnostics:

- Dry-run report: `/tmp/pdb_resume022_nobbox_dry_v377.json`.
- Applied report: `/tmp/pdb_resume022_nobbox_v377.json`.
- After residual report: `/tmp/pdb_resume022_after_v377_residual.json`.
- Debug residual dir: `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7/cover_residual_resume022_after_v377`.
- Overlay diagnostic: `/tmp/resume022_overlay_after_v377.jpg`.

### 2026-06-05 - `20260605_publishing_brochure005_visible_dom_v378`

Scope: `07_publishing/04_brochure_menu/brochure_menu_005_健身房会员宣传页`

Code/support change:

- Added `scripts/repair_publishing_targeted_cases.py` for case-aware publishing repairs where the released clean PNG crop does not include all HTML-flow content.
- Dry-run first attempted a fuller DOM rebuild for this page, but visual overlay showed that lower coach-name/title/cert boxes were already more accurate in the existing GT than the local DOM projection. The applied pass was narrowed to only the obvious hero drift and off-crop hallucinated boxes.

BBox corrections:

- Wrote only `brochure_menu_005_健身房会员宣传页`.
- No GT annotations were added or removed.
- Global boxed/no-bbox changed from `88948 / 836` to `88945 / 839` because three existing boxes pointed to content that is not visible in the released clean PNG crop. Global low-sim improved by 1: `7268` -> `7267`.
- Case counts changed from `36 total / 25 boxed / 11 no-bbox / 1 low-sim` to `36 total / 22 boxed / 14 no-bbox / 0 low-sim`.
- Corrected the three visible hero lines that had been shifted down onto the promo badge:
  - `#0` header `焰动健身`: `[8, 495, 706, 541]` -> `[134, 130, 574, 277]`.
  - `#1` text_block `BLAZE FITNESS CLUB`: `[0, 495, 1226, 541]` -> `[134, 274, 949, 352]`.
  - `#2` text_block `点燃你的运动激情 — 专业 · 科学 · 高效`: `[0, 495, 1356, 539]` -> `[134, 374, 1047, 458]`.
- Cleared hallucinated/off-crop boxes:
  - `#22` text_block `限时`: `[2267, 3575, 2340, 3618]` -> `None`.
  - `#23` title `新会员专享`: `[1117, 3625, 1364, 3634]` -> `None`.
  - `#35` footer/store-info text: `[137, 824, 228, 838]` -> `None`.
- Left `#24`-`#34` as no-bbox because the promo-card body, price/notes, later cards, activity note, and footer exist in HTML but are outside the released clean PNG crop. Do not synthesize boxes for these unless the clean asset is regenerated with the full HTML height.

Residual / visual verification:

- After residual check: `114945` text-like area / `17` components.
- Top residual components are the four orange coach-avatar circles and small class legend/color elements, not missing GT text instances.
- Overlay diagnostics confirm the hero text is back on the correct visible instances and that no blank bottom-area boxes remain.

Reports / diagnostics:

- Dry-run report: `/tmp/pdb_brochure005_dry_v378.json`.
- Applied report: `/tmp/pdb_brochure005_v378.json`.
- After residual report: `/tmp/pdb_brochure005_after_v378_residual.json`.
- Debug residual dir: `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7/cover_residual_brochure005_after_v378`.
- Overlay diagnostics: `/tmp/brochure005_overlay_after_v378.jpg`, `/tmp/brochure005_overlay_after_v378_top.jpg`, `/tmp/brochure005_overlay_after_v378_bottom.jpg`.

### 2026-06-05 - `20260605_publishing_book016_lower_manual_v379`

Scope: `07_publishing/03_book/book_016_Cookbook_EN`

Code/support change:

- Extended `scripts/repair_publishing_targeted_cases.py` with an image-grid calibrated repair for the lower cookbook page.
- A DOM/local-affine dry-run was rejected before writing because it pushed steps 5-7 far downward. The applied pass uses released-clean-image grid coordinates from `/tmp/book016_steps_grid.jpg` and `/tmp/book016_3000_3800_grid.jpg`.

BBox corrections:

- Wrote only `book_016_Cookbook_EN`.
- No GT annotations were added or removed.
- Global no-bbox improved by 1: `839` -> `838`; global boxed improved by 1: `88945` -> `88946`; global low-sim stayed `7267`.
- Case counts improved from `55 total / 54 boxed / 1 no-bbox / 0 low-sim` to `55 total / 55 boxed / 0 no-bbox / 0 low-sim`.
- Corrected lower-page boxes:
  - `#37` step 6 `Prepare the garnish...`: `[998, 2371, 2207, 2636]` -> `[998, 2440, 2207, 2688]`, removing overlap with step 5 and covering the final `minutes).` line.
  - `#38` step 7 `Finish...`: `[1050, 2720, 2200, 2971]` -> `[998, 2710, 2207, 3045]`, adding the visible final `Serve with buttered egg noodles or crusty bread.` line.
  - `#39` title `Chef's Tip`: `[254, 3248, 652, 3311]` -> `[170, 3090, 455, 3140]`.
  - `#40` Chef's Tip body: `[254, 3129, 2227, 3822]` -> `[170, 3155, 2210, 3315]`, shrinking the previous over-broad box so it no longer covers Wine Pairing and nutrition content.
  - `#41` title `Wine Pairing`: `[254, 3471, 669, 3496]` -> `[170, 3375, 515, 3430]`.
  - `#42` Wine Pairing paragraph: `None` -> `[170, 3440, 2205, 3548]`.

Residual / visual verification:

- Residual text-like area improved from `138557` to `119118`.
- Component count changed from `37` to `42`, expected because the old giant `#40` box no longer hides unrelated lower content; the overlay is visually more faithful.
- Overlay diagnostics confirm steps 6/7, Chef's Tip, and Wine Pairing are now separately aligned with the visible instances.

Reports / diagnostics:

- Rejected DOM dry-run report: `/tmp/pdb_book016_dry_v379.json` from the first local-affine attempt.
- Applied report: `/tmp/pdb_book016_v379.json`.
- After residual report: `/tmp/pdb_book016_after_v379_residual.json`.
- Debug residual dir: `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7/cover_residual_book016_after_v379`.
- Overlay diagnostics: `/tmp/book016_overlay_after_v379.jpg`, `/tmp/book016_overlay_after_v379_steps.jpg`, `/tmp/book016_overlay_after_v379_tipwine.jpg`.

### 2026-06-05 - `book_018_Travel_Guide_EN` reviewed, left unchanged

Scope: `07_publishing/03_book/book_018_Travel_Guide_EN`

Decision:

- Reviewed the single no-bbox annotation `#15`.
- Left unchanged because the source GT text is a visually non-contiguous/duplicated merged block: it combines the left-column `Train` paragraph with right-column `Practical Information` table content.
- The visible `Train` paragraph is already covered by existing `#13`, and the right-column practical-information table is already covered by `#17`.
- Adding a bbox for `#15` would require a broad union across left and right columns and would create the kind of false large box the user has repeatedly flagged.

Diagnostics:

- Current residual report: `/tmp/pdb_books016018_current_residual.json`.
- Current overlay: `/tmp/book_018_Travel_Guide_EN_overlay_current.jpg`.
- Transport-area grid: `/tmp/book018_transport_grid.jpg`.

### 2026-06-05 - `20260605_certificate_service_receipt011_footer_v380`

Scope: `10_certificate/04_service_receipt/service_receipt_011_律师服务费收据_Legal_Service_Fee_Receipt`

Code/support change:

- Added `scripts/repair_certificate_targeted_cases.py` for visually confirmed small certificate/service-receipt footer repairs.

BBox additions:

- Wrote only `service_receipt_011_律师服务费收据_Legal_Service_Fee_Receipt`.
- No GT annotations were added or removed.
- Global no-bbox improved by 2: `838` -> `836`; global boxed improved by 2: `88946` -> `88948`; global low-sim stayed `7267`.
- Case counts improved from `43 total / 41 boxed / 2 no-bbox / 0 low-sim` to `43 total / 43 boxed / 0 no-bbox / 0 low-sim`.
- Added:
  - `#40` footer `委托人 / Client 2026年3月15日`: `None` -> `[1930, 7600, 2160, 7705]`.
  - `#42` bottom bilingual receipt notice: `None` -> `[450, 7955, 2020, 8055]`.

Residual / visual verification:

- Residual improved from `283283` text-like area / `57` components to `272878` / `56`.
- Overlay diagnostic confirms `#40` is on the right-side client label/date and `#42` covers the two bottom notice lines, excluding decorative swans and page border.

Reports / diagnostics:

- Dry-run report: `/tmp/pdb_service_receipt011_dry_v380.json`.
- Applied report: `/tmp/pdb_service_receipt011_v380.json`.
- After residual report: `/tmp/pdb_service_receipt011_after_v380_residual.json`.
- Debug residual dir: `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7/cover_residual_service_receipt011_after_v380`.
- Overlay diagnostics: `/tmp/service_receipt011_overlay_after_v380.jpg`, `/tmp/service_receipt011_bottom_after_v380.jpg`.

### 2026-06-06 - `20260605_business_quotation015_customer_address_v382`

Scope: `04_business/02_quotation/quotation_015_Industrial_Automation_Line_Quote`

Code/support change:

- Extended `scripts/repair_business_targeted_cases.py` with case-aware manual repairs for the quotation customer card and page-2 customer acceptance block.
- `v381` first moved `#5` and added `#39`; visual crop then exposed the wrapped address line outside `#6`, so `v382` immediately supersedes it with the address expansion.

BBox corrections/additions:

- Wrote only `quotation_015_Industrial_Automation_Line_Quote`.
- No GT annotations were added or removed.
- Global no-bbox improved by 1: `836` -> `835`; global boxed improved by 1: `88948` -> `88949`; global low-sim stayed `7267`.
- Case counts improved from `41 total / 40 boxed / 1 no-bbox / 0 low-sim` to `41 total / 41 boxed / 0 no-bbox / 0 low-sim`.
- Corrected:
  - `#5` `Customer: Apex Powertrain Components LLC`: `[1746, 5539, 2252, 5740]` -> `[155, 450, 605, 570]`, moving it from the page-2 signature area back to the page-1 customer card.
  - `#6` customer address: `[160, 580, 604, 614]` -> `[155, 580, 605, 640]`, including wrapped `42101`.
  - `#39` `Accepted by Customer... Signature...`: `None` -> `[1735, 5390, 2258, 5742]`, adding the right-side page-2 customer acceptance/signature block.

Residual / visual verification:

- Residual after `v381`: `108410` text-like area / `15` components.
- Residual after `v382`: `107066` text-like area / `14` components.
- Visual crops confirm `#5/#6` align with the page-1 customer card and address, and `#39` covers only the right-side customer acceptance block without spanning the left NexAuto signature or company seal.

Reports / diagnostics:

- Dry-run report: `/tmp/pdb_quotation015_dry_v381.json`.
- Applied reports: `/tmp/pdb_quotation015_v381.json`, `/tmp/pdb_quotation015_v382.json`.
- After residual reports: `/tmp/pdb_quotation015_after_v381_residual.json`, `/tmp/pdb_quotation015_after_v382_residual.json`.
- Debug residual dir: `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7/cover_residual_quotation015_after_v382`.
- Overlay diagnostics: `/tmp/quotation015_overlay_after_v382.jpg`, `/tmp/quotation015_top_customer_after_v382.jpg`, `/tmp/quotation015_signature_after_v382.jpg`.

### 2026-06-06 - `drug_instruction_018` reviewed, left unchanged for now

Scope: `06_medical/10_drug_instruction/drug_instruction_018`

Decision:

- Reviewed the four no-bbox annotations (`#0` title `安宮牛黃丸`, `#1`, `#2`, `#3` `處方來源`).
- Left unchanged for now because the released clean PNG starts at later vertical-writing sections while the HTML title/source columns appear off-crop to the right of the visible image. Several nearby early annotations also sit on the right edge/blank area, so this needs a dedicated vertical-layout/off-crop audit rather than a quick synthetic bbox.

Diagnostics:

- Current residual report: `/tmp/pdb_drug_instruction018_current_residual.json`.
- Visual diagnostics: `/tmp/drug_instruction018_top_current.jpg`, `/tmp/drug018_right_grid.jpg`.

### 2026-06-06 - `20260605_business_bp001_team_refine_v385`

Scope:

- `04_business/05_resume/resume_021_Research_Dossier`
- `04_business/05_resume/resume_022_Career_Atlas`
- `04_business/07_employee_handbook/employee_handbook_014_Global`
- `04_business/07_employee_handbook/employee_handbook_016_Quick_Start_Guide`
- `04_business/06_business_plan/business_plan_001_智能农业科技公司商业计划书`

Code/support change:

- Extended `scripts/repair_business_targeted_cases.py` with manual image-grid repairs for small, visually confirmed business cases.
- `v383` fixed the main missing/shifted instances; `v384` tightened `resume_021`, `resume_022_Career_Atlas`, and `employee_handbook_016`; `v385` widened/tightened `business_plan_001` team-name boxes after visual crop review.

Global impact:

- Global no-bbox improved by 12: `835` -> `823`.
- Global boxed improved by 12: `88949` -> `88961`.
- Global low-sim improved by 4: `7267` -> `7263`.

Case-level corrections:

- `resume_021_Research_Dossier`: case counts `53 total / 52 boxed / 1 no-bbox / 0 low-sim` -> `53 / 53 / 0 / 0`.
  - `#33` reviewer link note moved from the formula title area to the visible red handwritten note: `[296, 2795, 767, 2837]` -> `[300, 2725, 845, 2775]`.
  - `#34` formula-section title moved to `核心研究指标公式 Key Research Metrics`: `[296, 2795, 766, 2836]` -> `[300, 2795, 830, 2845]`.
  - `#35` combined three research metric formulas added: `None` -> `[300, 2845, 1900, 2990]`.

- `resume_022_Career_Atlas`: case counts `49 total / 45 boxed / 4 no-bbox / 0 low-sim` -> `49 / 49 / 0 / 0`.
  - Added four formula boxes in the `核心技术指标 Key Metrics` panel:
    - `#33` mAP: `None` -> `[90, 3835, 480, 3890]`.
    - `#34` CLIP score: `None` -> `[90, 3935, 540, 4020]`.
    - `#35` FLOPs: `None` -> `[90, 4050, 450, 4130]`.
    - `#36` MSE: `None` -> `[90, 4170, 610, 4260]`.

- `employee_handbook_014_Global`: case counts `58 total / 55 boxed / 3 no-bbox / 0 low-sim` -> `58 / 58 / 0 / 0`.
  - Rebuilt the compensation formula stack because adjacent formula titles/body boxes had drifted into each other.
  - Added missing formula expression boxes:
    - `#20` bonus formula: `None` -> `[1295, 1095, 1900, 1140]`.
    - `#23` Chinese annual-incentive formula: `None` -> `[1295, 1240, 2050, 1290]`.
    - `#26` annual vest formula: `None` -> `[1295, 1378, 2050, 1425]`.
  - Corrected surrounding formula title/detail boxes `#19`, `#21`, `#22`, `#24`, `#25`, `#27`, `#28` to the visible compensation section rows.

- `employee_handbook_016_Quick_Start_Guide`: case counts `24 total / 23 boxed / 1 no-bbox / 3 low-sim` -> `24 / 24 / 0 / 0`.
  - Rebuilt all visible page blocks `#0`-`#23` from the full-page image grid because the right/middle blocks were shifted into thin or unrelated lines.
  - Added `#20` `Mini Policy`: `None` -> `[1485, 645, 1610, 675]`.
  - Corrected the title/header, welcome text, checklist, access setup table, attendance policy/formula, caution box, emergency contacts, quick memos, mini-policy body, and both footer labels.

- `business_plan_001_智能农业科技公司商业计划书`: case counts `56 total / 53 boxed / 3 no-bbox / 1 low-sim` -> `56 / 56 / 0 / 0`.
  - Corrected/added team-name role boxes:
    - `#44` `王智远 CTO / 联合创始人`: `[319, 7913, 619, 7982]` -> `[1015, 7090, 1385, 7205]`.
    - `#46` `张雪梅 COO`: `None` -> `[1705, 7090, 1935, 7205]`.
    - `#48` `李海涛 VP of Sales`: `[499, 7654, 674, 7685]` -> `[500, 7580, 725, 7670]`.
    - `#50` `赵明辉 首席算法科学家`: `None` -> `[1095, 7580, 1410, 7670]`.
    - `#52` `刘文静 CFO`: `None` -> `[1730, 7580, 1950, 7670]`.

Residual / visual verification:

- After `v383`, residuals:
  - `resume_021_Research_Dossier`: `117953` text-like / `58` comps.
  - `resume_022_Career_Atlas`: `329568` / `63`.
  - `employee_handbook_014_Global`: `126822` / `39`.
  - `employee_handbook_016_Quick_Start_Guide`: `11562` / `11`.
  - `business_plan_001_智能农业科技公司商业计划书`: `729657` / `46`.
- After `v384`, `resume_022_Career_Atlas` improved to `317676` / `51`; `business_plan_001` improved to `714474` / `45`. `employee_handbook_016` residual increased slightly after title-box tightening, accepted visually because the boxes stopped covering unrelated pill labels.
- After `v385`, `business_plan_001` improved again to `710889` / `42`.
- Visual diagnostics confirm the repaired boxes are on the intended formula/card/team instances and avoid the old broad cross-section drift.

Reports / diagnostics:

- Dry-run reports: `/tmp/pdb_business_small_dry_v383.json`, `/tmp/pdb_business_small_refine_dry_v384.json`.
- Applied reports: `/tmp/pdb_business_small_v383.json`, `/tmp/pdb_business_small_refine_v384.json`, `/tmp/pdb_business_bp001_refine_v385.json`.
- After residual reports: `/tmp/pdb_business_small_after_v383_residual.json`, `/tmp/pdb_business_small_after_v384_residual.json`, `/tmp/pdb_business_bp001_after_v385_residual.json`.
- Debug residual dirs:
  - `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7/cover_residual_business_small_after_v383`
  - `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7/cover_residual_business_small_after_v384`
  - `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7/cover_residual_business_bp001_after_v385`
- Overlay diagnostics:
  - `/tmp/v384_resume_021_Research_Dossier_formula.jpg`
  - `/tmp/v384_resume_022_Career_Atlas_metrics.jpg`
  - `/tmp/v383_employee_handbook_014_Global_comp.jpg`
  - `/tmp/v384_employee_handbook_016_Quick_Start_Guide_full.jpg`
  - `/tmp/v385_business_plan_001_team.jpg`

## 20260606_newspaper012_raw_dom_v386

Scope:

- `07_publishing/01_newspaper/newspaper_012_NYT_FrontPage_EN`

Reason:

- Newspaper pages were already matched, but many dense paragraph boxes had been foreground-shrunk into nearby lines, producing visible vertical offsets and cut text.
- For this case, replaced the foreground-refined boxes with raw browser DOM Range/bounding rect boxes mapped directly to the clean PNG, with small padding and no ink snapping.

Case-level corrections:

- `newspaper_012_NYT_FrontPage_EN`: case counts remained `139 total / 139 boxed / 0 no-bbox / 0 low-sim`.
- Reprojected all `#0`-`#138` boxes from raw DOM rects.
- Representative fixes:
  - `#7` byline moved from `[136, 1230, 884, 1263]` to `[133, 1111, 906, 1156]`.
  - `#8` lead paragraph expanded/moved from `[135, 1230, 1878, 1349]` to `[133, 1161, 1881, 1444]`.
  - `#9` paragraph adjusted from `[135, 1474, 1879, 1652]` to `[133, 1456, 1881, 1668]`.
  - `#10` paragraph adjusted from `[135, 1673, 1878, 1789]` to `[133, 1676, 1881, 1941]`.

Code/support change:

- Added debug overlay output to `scripts/repair_newspaper_raw_dom.py` so newspaper raw-DOM candidates can be visually checked during dry-runs.

Diagnostics:

- Applied report: `/tmp/pdb_newspaper012_raw_dom_v386.json`.
- Debug overlay: `/tmp/newspaper_raw_dom_v386_debug/01_newspaper_012_NYT_FrontPage_EN_raw_dom_overlay.jpg`.

## 20260606_newspaper_all_raw_dom_v387

Scope:

- `07_publishing/01_newspaper` complete pass, cases `newspaper_001` through `newspaper_020`.

Reason:

- User reported the newspaper class still had obvious offsets.
- Root cause: previous newspaper boxes were already content-matched, but the generic foreground-refinement step shrank dense article boxes to nearby ink lines, causing visible vertical drift and cut paragraphs.
- Fix policy: reproject newspaper boxes from raw browser DOM Range/bounding rects directly to clean PNG coordinates, apply small padding, and do not run foreground/ink snapping.

Global effect:

- No GT instance additions or deletions in this pass.
- Case-level counts remain fully boxed for all 20 cases; `newspaper_020_文化副刊` retains one low-similarity item that is visually placed on the intended author line.
- Newspaper residual total improved from `57,255,405` to `6,971,138` text-like pixels after the raw-DOM pass.

Case-level corrections:

- `newspaper_001_财经日报头版`: reprojected 96 boxes; counts `96 boxed / 0 no-bbox / 0 low-sim`; residual `2,201,485 -> 49,624`.
- `newspaper_002_Financial_Times_EN`: reprojected 108 boxes; counts `108 / 0 / 0`; residual `2,837,476 -> 118,250`.
- `newspaper_003_经济导报`: reprojected 112 boxes; counts `112 / 0 / 0`; residual `4,082,214 -> 1,169,993`.
- `newspaper_004_环球时报`: reprojected 106 boxes; counts `106 / 0 / 0`; residual `2,646,060 -> 49,775`.
- `newspaper_005_Tech_Weekly_EN`: reprojected 112 boxes; counts `112 / 0 / 0`; residual `3,263,304 -> 312,160`.
- `newspaper_006_科技商报`: reprojected 94 boxes; counts `94 / 0 / 0`; residual `1,973,566 -> 33,953`.
- `newspaper_007_The_Guardian_EN`: reprojected 87 boxes; counts `87 / 0 / 0`; residual `2,537,204 -> 217,453`.
- `newspaper_008_China_Daily_EN`: reprojected 92 boxes; counts `92 / 0 / 0`; residual `2,408,686 -> 376,701`.
- `newspaper_009_南方周末`: reprojected 87 boxes; counts `87 / 0 / 0`; residual `2,646,412 -> 302,786`.
- `newspaper_010_体育版面`: reprojected 138 boxes; counts `138 / 0 / 0`; residual `2,879,305 -> 457,057`.
- `newspaper_011_Financial_Chronicle`: reprojected 90 boxes; counts `90 / 0 / 0`; residual `2,788,605 -> 335,032`.
- `newspaper_012_NYT_FrontPage_EN`: already repaired in v386; v387 changed 0 boxes; counts `139 / 0 / 0`; residual stayed `467,183`.
- `newspaper_013_都市晚报`: reprojected 111 boxes; counts `111 / 0 / 0`; residual `2,722,030 -> 71,190`.
- `newspaper_014_Guardian_Sports_EN`: reprojected 109 boxes; counts `109 / 0 / 0`; residual `3,258,514 -> 498,930`.
- `newspaper_015_中国经济日报`: reprojected 98 boxes; counts `98 / 0 / 0`; residual `2,800,208 -> 101,441`.
- `newspaper_016_人民日报_政治版`: reprojected 111 boxes; counts `111 / 0 / 0`; residual `3,182,419 -> 876,898`.
- `newspaper_017_体育周报`: reprojected 107 boxes; counts `107 / 0 / 0`; residual `1,974,205 -> 79,673`.
- `newspaper_018_Washington_Post_EN`: reprojected 111 boxes; counts `111 / 0 / 0`; residual `4,914,145 -> 619,918`.
- `newspaper_019_Global_Tribune`: reprojected 110 boxes; counts `110 / 0 / 0`; residual `4,630,982 -> 485,174`.
- `newspaper_020_文化副刊`: reprojected 126 boxes; counts `126 / 0 / 1`; residual `3,041,402 -> 347,947`.
  - `#35` `艺术评论家 范迪安` remains `low_similarity` with score `0.86`; bbox moved to the visible author label `[164, 3520, 374, 3578]`.

Verification:

- Dry-run report: `/tmp/pdb_newspaper_all_raw_dom_dry_v387.json`.
- Applied report: `/tmp/pdb_newspaper_all_raw_dom_v387.json`.
- Before residual report: `/tmp/pdb_newspaper_before_v387_residual.json`.
- After residual report: `/tmp/pdb_newspaper_after_v387_residual.json`.
- Candidate contact sheets:
  - `/tmp/newspaper_raw_dom_v387_debug/newspaper_contact_1.jpg`
  - `/tmp/newspaper_raw_dom_v387_debug/newspaper_contact_2.jpg`
- Applied overlays: `/tmp/newspaper_raw_dom_v387_apply_debug/`.

## 20260606_newspaper_raw_dom_image_size_v388

Scope:

- `07_publishing/01_newspaper` complete pass, cases `newspaper_001` through `newspaper_020`.

Reason:

- User reported `newspaper_004_环球时报` was still visibly offset in the review front-end after v387.
- Root cause: v387 bboxes were correct in clean-image pixel coordinates, but the review app case dimensions still used older CSS/render dimensions around `1474/1512 px` wide. The SVG `viewBox` therefore did not match the actual image or bbox coordinate system, making correct boxes render as huge shifted rectangles.

Fix:

- Kept the v387 raw-DOM bbox coordinates unchanged.
- Updated each newspaper case `width`/`height` to the actual clean PNG dimensions used by the front-end image.
- Updated `scripts/repair_newspaper_raw_dom.py` so future newspaper raw-DOM runs also synchronize case dimensions from the clean image.

Case-level dimension corrections:

- `newspaper_001_财经日报头版`: `[1474, 2683] -> [4606, 8759]`.
- `newspaper_002_Financial_Times_EN`: `[1512, 2864] -> [4725, 9619]`.
- `newspaper_003_经济导报`: `[1474, 3188] -> [4606, 10544]`.
- `newspaper_004_环球时报`: `[1474, 2751] -> [4606, 9469]`.
- `newspaper_005_Tech_Weekly_EN`: `[1512, 3179] -> [4725, 10669]`.
- `newspaper_006_科技商报`: `[1474, 2260] -> [4606, 7438]`.
- `newspaper_007_The_Guardian_EN`: `[1512, 2270] -> [4725, 7678]`.
- `newspaper_008_China_Daily_EN`: `[1512, 2534] -> [4725, 8431]`.
- `newspaper_009_南方周末`: `[1474, 3335] -> [4606, 10828]`.
- `newspaper_010_体育版面`: `[1474, 2993] -> [4606, 9769]`.
- `newspaper_011_Financial_Chronicle`: `[1512, 2342] -> [4725, 7509]`.
- `newspaper_012_NYT_FrontPage_EN`: `[1512, 4495] -> [4725, 14844]`.
- `newspaper_013_都市晚报`: `[1474, 3353] -> [4606, 11006]`.
- `newspaper_014_Guardian_Sports_EN`: `[1512, 2827] -> [4725, 9316]`.
- `newspaper_015_中国经济日报`: `[1474, 3196] -> [4606, 10425]`.
- `newspaper_016_人民日报_政治版`: `[1474, 2716] -> [4606, 9319]`.
- `newspaper_017_体育周报`: `[1474, 2121] -> [4606, 6878]`.
- `newspaper_018_Washington_Post_EN`: `[1512, 4914] -> [4725, 16225]`.
- `newspaper_019_Global_Tribune`: `[1512, 3338] -> [4725, 11100]`.
- `newspaper_020_文化副刊`: `[1474, 3425] -> [4606, 11088]`.

Verification:

- Front-end confirmed `newspaper_004_环球时报` now loads `data 20260606_newspaper_raw_dom_image_size_v388`.
- Front-end SVG viewBox changed from `0 0 1474 2751` to `0 0 4606 9469`, matching the actual image size.
- Visual clip confirmed `#2/#3` align with the two masthead metadata rows and `#6/#7/#8` align with the left-column byline/body blocks.
- Applied report: `/tmp/pdb_newspaper_raw_dom_image_size_v388.json`.

## 20260606_publishing_dimensions_v389

Scope:

- Whole `07_publishing` category: `01_newspaper`, `02_magazine`, `03_book`, `04_brochure_menu`, and `05_catalog_directory`.

Reason:

- User reported the publishing front-end still showed large visible offsets even after newspaper raw-DOM bbox repair.
- Root cause: many publishing cases had bboxes already expressed in released clean PNG coordinates, but the review app case `width`/`height` still used older CSS/front-end render dimensions. The SVG viewBox therefore scaled correct boxes into the wrong positions.

Fix:

- Synchronized each `07_publishing` case `width`/`height` to the actual released clean PNG dimensions.
- Did not change any bbox coordinates, GT texts, or instance counts in this pass.
- Added `scripts/sync_publishing_case_dimensions.py` so this dimension check can be rerun.

Case-level effect:

- `01_newspaper`: 0 cases changed; dimensions were already synchronized by v388.
- `02_magazine`: 20 cases changed.
- `03_book`: 20 cases changed.
- `04_brochure_menu`: 20 cases changed.
- `05_catalog_directory`: 20 cases changed.

Examples:

- `magazine_001_人工智能专题`: `[794, 852] -> [2513, 3509]`.
- `book_018_Travel_Guide_EN`: `[794, 1134] -> [2481, 4178]`.
- `brochure_menu_005_健身房会员宣传页`: `[1600, 1123] -> [2481, 3634]`.
- `catalog_directory_020_高端音响器材目录`: `[794, 5334] -> [2481, 16669]`.

Remaining known publishing issues after v389:

- Dimension mismatch and bbox overflow are cleared for all `07_publishing` cases.
- Remaining count issues are local bbox/content issues: `01_newspaper` has 1 low-sim item, `02_magazine` has 12 low-sim items, `03_book` has 1 no-bbox and 11 low-sim items, `04_brochure_menu` has 14 no-bbox and 4 low-sim items, and `05_catalog_directory` has 5 low-sim items.
- `brochure_menu_005_健身房会员宣传页` keeps 14 no-bbox items because the released clean PNG crop ends before the promo-card body/footer GT content; these are not synthesized into visible boxes.

Verification:

- Dry-run report: `/tmp/pdb_publishing_dimensions_dry_v389.json`.
- Applied report: `/tmp/pdb_publishing_dimensions_v389.json`.
- Problem-case contact sheet after dimension sync: `/tmp/publishing_problem_overlays_v389/publishing_problem_contact.jpg`.

## 20260606_publishing_books_manual_v390

Scope:

- Targeted `07_publishing/03_book` cleanup for visible remaining book issues after the v389 dimension sync.

Reason:

- The v389 contact sheet still showed three true book-page problems:
  - `book_018_Travel_Guide_EN` had the Getting Around transport cards vertically mixed; the `Train` body was no-bbox.
  - `book_011_医学教材_内科学` had the heart-failure diagnosis paragraph assigned to a tiny page-header artifact.
  - `book_017_数学定理证明` had the reference block assigned to a tiny page-header artifact.

Case-level corrections:

- `book_018_Travel_Guide_EN`: corrected 6 annotations in the Getting Around section.
  - `#10 Bus` moved to the Bus title.
  - `#11 Bus...` moved to the Bus card.
  - `#12 Bicycle` moved to the Bicycle title.
  - `#13 Bicycle...` moved to the Bicycle card.
  - `#14 Train` moved to the Train title.
  - `#15 Train...` was promoted from no-bbox to the visible Train card.
  - Counts changed `27 boxed / 1 no-bbox / 0 low-sim` -> `28 / 0 / 0`.
- `book_011_医学教材_内科学`: corrected `#12` from `[92, 93, 114, 133]` to the visible diagnostic paragraph below the NYHA box.
  - Counts changed `21 boxed / 0 no-bbox / 1 low-sim` -> `21 / 0 / 0`.
- `book_017_数学定理证明`: corrected `#31` from `[180, 209, 186, 220]` to the bottom two-line reference block.
  - Counts changed `33 boxed / 0 no-bbox / 1 low-sim` -> `33 / 0 / 0`.

Verification:

- Dry-run report: `/tmp/pdb_publishing_books_manual_dry_v390.json`.
- Applied report: `/tmp/pdb_publishing_books_manual_v390.json`.
- Cover overlays: `/tmp/publishing_books_manual_v390_overlays/`.
- Local outline crops used for manual visual QA:
  - `/tmp/publishing_books_manual_v390_outline_crops/book_018_Travel_Guide_EN_outline_crop.jpg`
  - `/tmp/publishing_books_manual_v390_outline_crops/book_011_医学教材_内科学_outline_crop.jpg`
  - `/tmp/publishing_books_manual_v390_outline_crops/book_017_数学定理证明_outline_crop.jpg`

## 20260606_publishing_manual_cleanup_v391

Scope:

- Additional `07_publishing` manual cleanup after the v390 book pass.

Case-level corrections:

- `book_001_计算机网络_传输层协议`: moved `#6` TCP congestion-control formula block from a small top artifact to the visible formula area; cleared the case low-sim count.
- `book_020_Art_Photography`: corrected 8 lower-page/detail/footer annotations:
  - `#3` author line.
  - `#20` `Details & Close-ups` heading.
  - `#22/#24/#26` detail captions.
  - `#23/#25` detail panel text.
  - `#29` bottom footer line.
- `brochure_menu_001_日式料理菜单`: moved footer/contact annotations `#57-#60` from top artifacts to the actual lower-page footer/contact rows.
- `catalog_directory_019_有机食品产品目录`: cleared `#42` to no-bbox because the GT text is embedded HTML/CSS style pollution and is not visible in the released clean PNG; the visible footer remains covered by `#43`.
- `catalog_directory_020_高端音响器材目录`: moved footer/contact annotations `#60-#63` to the visible bottom footer and contact block.

Verification:

- Applied report: `/tmp/pdb_publishing_manual_cleanup_v391.json`.

## 20260606_publishing_micro_adjust_v392

Scope:

- Micro-adjustments for publishing cases from v391 visual review.

Case-level corrections:

- `book_001_计算机网络_传输层协议`: tightened `#6` vertically to the formula block instead of covering adjacent paragraph/history text.
- `book_020_Art_Photography`: shifted detail captions `#22/#24/#26` downward to align with the visible caption rows below the image details.
- `brochure_menu_001_日式料理菜单`: shifted `#57` down after the first footer pass.

Verification:

- Applied report: `/tmp/pdb_publishing_micro_adjust_v392.json`.
- Visual crops included `book020_details` and `book001_formula` under `/tmp/publishing_micro_adjust_v392_outline_crops/`.

## 20260606_publishing_micro_adjust2_v393

Scope:

- Second micro-adjustment after v392 visual crop review.

Case-level corrections:

- `book_001_计算机网络_传输层协议`: tightened the right edge of `#6` so the formula box no longer covered the right-side historical note.
- `brochure_menu_001_日式料理菜单`: shifted footer/contact `#57-#60` down after v392, then later re-tightened in v395.

Verification:

- Applied report: `/tmp/pdb_publishing_micro_adjust2_v393.json`.

## 20260606_publishing_magazine_cleanup_v394

Scope:

- Cleared the remaining `07_publishing/01_newspaper` and `07_publishing/02_magazine` low-sim cases after dimension sync and manual book/catalog cleanup.

Case-level corrections:

- `newspaper_020_文化副刊`: marked `#35` author line `艺术评论家 范迪安` as visually correct at the existing bbox.
- `magazine_005_生活周刊`: moved `#38` from a tiny upper-page fragment to the visible bottom ticker/footer strip.
- `magazine_012_Sports_Illustrated_EN`: moved `#42` to the bottom issue/footer bar.
- `magazine_014_The_Economist_EN`: marked chart labels `#12/#14/#15` as visually correct at their existing bboxes.
- `magazine_018_Wired_Tech_EN`: moved `#23` to the right-column `Quantum Processor Comparison` title and moved `#38` to the bottom footer bar.
- `magazine_019_读者文摘`: moved `#24` from the top masthead area to the visible bottom footer line.
- `magazine_020_Rolling_Stone_Music_EN`: marked `#3` as visually correct, moved `#30` to the pull quote, `#31` to the quote byline, and `#36` to the bottom footer bar.

Verification:

- Applied report: `/tmp/pdb_publishing_magazine_cleanup_v394.json`.
- Visual QA crops: `/tmp/publishing_v394_qa/mag005_footer_v394.jpg`, `/tmp/publishing_v394_qa/mag012_footer_v394.jpg`, `/tmp/publishing_v394_qa/mag018_table_title_v394.jpg`, `/tmp/publishing_v394_qa/mag018_footer_v394.jpg`, `/tmp/publishing_v394_qa/mag019_footer_v394.jpg`, `/tmp/publishing_v394_qa/mag020_quote_v394.jpg`, `/tmp/publishing_v394_qa/mag020_footer_v394.jpg`.

## 20260606_publishing_brochure001_footer_tight_v395

Scope:

- Final tightening for `brochure_menu_001_日式料理菜单` footer/contact rows after v394 visual QA exposed line-level vertical drift.

Case-level corrections:

- `brochure_menu_001_日式料理菜单`: retightened footer/contact annotations:
  - `#57` address row.
  - `#58` business-hours row.
  - `#59` phone/WeChat row.
  - `#60` price/service/allergy note row.

Publishing category status after v395:

- `01_newspaper`: `20 cases`, `0 no-bbox`, `0 low-sim`.
- `02_magazine`: `20 cases`, `0 no-bbox`, `0 low-sim`.
- `03_book`: `20 cases`, `0 no-bbox`, `0 low-sim`.
- `04_brochure_menu`: `20 cases`, `14 no-bbox`, `0 low-sim`.
- `05_catalog_directory`: `20 cases`, `1 no-bbox`, `0 low-sim`.
- Remaining `15 no-bbox` are intentional rejects:
  - `brochure_menu_005_健身房会员宣传页`: 14 GT items are outside the released clean PNG crop / not visible.
  - `catalog_directory_019_有机食品产品目录`: `#42` is non-visible HTML/CSS style text; visible footer is already `#43`.

Verification:

- Applied report: `/tmp/pdb_publishing_brochure001_footer_tight_v395.json`.
- Final footer crop: `/tmp/publishing_v394_qa/brochure001_footer_v395.jpg`.
- Front-end confirmed loading `review_data.js?20260606_publishing_brochure001_footer_tight_v395`.

## 20260606_publishing_dom_gated_dry_v396

Scope:

- Dry-run only; no data files were changed.

Reason and result:

- Ran `scripts/repair_review_bboxes_dom_gated.py` across all 100 `07_publishing` cases to test whether a broad DOM rebuild could safely improve residual cover.
- The script rejected all newspaper/book/magazine/catalog candidates or found no meaningful change.
- Only `brochure_menu_005_健身房会员宣传页` was marked algorithmically acceptable because no-bbox would drop `14 -> 12`, but residual did not improve and dark area increased. This was not applied because those remaining GT items are known off-crop/non-visible for the released clean PNG.

Verification:

- Dry-run report: `/tmp/pdb_publishing_dom_gated_dry_v396.json`.
- Residual reports:
  - `/tmp/pdb_publishing_residual_v395.json`
  - `/tmp/pdb_publishing_residual_v395_pad12.json`

## 20260606_publishing_mag001_hero_tight_v399

Scope:

- Full visual repair for `magazine_001_人工智能专题` after front-end review showed the page was still visibly disordered despite `47/47 boxed`.

Case-level corrections:

- Rebuilt all `magazine_001_人工智能专题` bbox coordinates against the released clean PNG (`2513x3509`) in visual/reading order.
- Added 2 visible missing `text_block` GT items:
  - Pullquote body after the left-column investment paragraph: `"AI创业的黄金窗口正在关闭。未来12个月内，我们预期至少60%的大模型创业公司会被并购或停止运营。"`
  - Pullquote body before the middle-column `华为云AI首席科学家 田奇` attribution: `"未来三年，中国大模型市场的竞争将不是百米赛跑，而是铁人三项——模型能力、工程落地、生态构建缺一不可。"`
- Reindexed the case from `#0` to `#48` so the front-end label order matches the page reading order.
- Tightened/expanded the full-page layout groups:
  - `#0-#4` masthead and hero section.
  - `#5-#17` left column, stats cards, table, source line.
  - `#18-#29` middle column, pullquote, compute section.
  - `#30-#46` right sidebar ranking, timeline, chart, extension reading list.
  - `#47-#48` footnote and black page footer.

Verification:

- Applied reports:
  - `/tmp/pdb_publishing_mag001_pullquotes_v398.json` for the full case rebuild and 2 inserted pullquote body items.
  - `/tmp/pdb_publishing_mag001_hero_tight_v399.json` for the final hero summary/meta edge tightening.
- Cover QA: `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7/cover_audit_publishing_mag001_v399/11_magazine_001_人工智能专题_cover.jpg`.
- Residual QA: `/tmp/pdb_publishing_mag001_residual_v399.json` (`text_like_area=59490`, remaining components are decorative rules/card bars/page corners rather than uncovered body text).
- Front-end token: `20260606_publishing_mag001_hero_tight_v399`.

## 20260606_publishing_mag002_005_dom814_v400

Scope:

- Targeted full-page repair for `07_publishing/02_magazine` cases `magazine_002_科技杂志_Feature` through `magazine_005_生活周刊`.

Root cause:

- These magazine pages were still using bboxes derived from the wrong browser geometry: the source clean PNG corresponds to an approximately `814px` screenshot viewport with a uniform clean-image scale, while the older DOM rebuild used a wider viewport and a non-uniform `clean_height / body_height` y-scale. This made lower and multi-column items visibly drift or fall into the gray screenshot background.

Case-level corrections:

- `magazine_002_科技杂志_Feature`
  - Rebuilt all `35` existing bbox coordinates using DOM text/table rects rendered at viewport width `814`, mapped uniformly into the released clean PNG (`2513x3509`).
  - Added 1 visible missing `text_block` GT item for the yellow NISQ margin-note body:
    - `Noisy Intermediate-Scale Quantum——"含噪中等规模量子"，指当前量子计算机所处的发展阶段：量子比特数在50-1000范围，且无法进行完全纠错。由John Preskill于2018年提出。`
  - Reindexed the case to `36/36 boxed`, `0 no bbox`, `0 low-sim`.
- `magazine_003_财经杂志_数据报道`
  - Rebuilt all `50` existing bbox coordinates using the same viewport-814 DOM mapping.
  - Added 1 visible missing `text_block` GT item for the red quote-box body:
    - `"化债不是会计游戏。如果只是把数字从A表移到B表，投资者和评级机构迟早会看穿。真正的化债只有两条路：增加收入或减少支出，没有第三条路。"`
  - Reindexed the case to `51/51 boxed`, `0 no bbox`, `0 low-sim`.
- `magazine_004_学术期刊目录页`
  - Rebuilt all `60` existing bbox coordinates against the released clean PNG. No new GT item was added.
  - Final status: `60/60 boxed`, `0 no bbox`, `0 low-sim`.
- `magazine_005_生活周刊`
  - Rebuilt all `39` existing bbox coordinates against the released clean PNG, replacing the earlier footer-only manual fix with a full-page repair. No new GT item was added.
  - Final status: `39/39 boxed`, `0 no bbox`, `0 low-sim`.

Implementation:

- Extended `scripts/repair_publishing_targeted_cases.py` with a magazine-specific viewport-814 DOM mapping path and idempotent insertion of the two newly discovered visible text blocks.

Verification:

- Applied report: `/tmp/pdb_publishing_mag002_005_dom814_v400.json`.
- Cover QA: `/Users/lizhiheng/Desktop/科研/nips2026/puredocbench-open-source/review/gt_case_compare_all_fixed7/cover_audit_publishing_mag002_005_v400/`.
- Residual QA: `/tmp/pdb_publishing_mag002_005_residual_v400.json`.
  - `magazine_002_科技杂志_Feature`: `text_like_area=13929`, remaining components are decorative rules/left bars.
  - `magazine_003_财经杂志_数据报道`: `text_like_area=130912`, dominated by the red statistic block, sidebar/chart bars, and page-edge colored bands rather than uncovered body text.
  - `magazine_004_学术期刊目录页`: `text_like_area=390429`, dominated by the dark category divider bars and horizontal rules.
  - `magazine_005_生活周刊`: `text_like_area=0`.
- Front-end token: `20260606_publishing_mag002_005_dom814_v400`.

## 20260606_publishing_mag006_020_adaptive_v402

Scope:

- Finished the remaining `07_publishing/02_magazine` cases, `magazine_006_科技杂志` through `magazine_020_Rolling_Stone_Music_EN`.

Root cause:

- These pages use mixed magazine templates. Some are full `body { width: 210mm }` pages without the gray `.page` wrapper; others keep a `.page` container with browser padding. The old `content_fast` boxes mixed those coordinate bases and did not handle CSS columns/flex steps reliably.
- Multi-column article paragraphs in `magazine_006` and `magazine_012/014/016/020` can span column fragments. Since the review app draws only a single bbox rectangle, the repaired bbox is the visual outer rectangle for the whole GT instance.
- `cite` elements were not collected by the generic DOM extractor, which caused short quote attributions to be vulnerable to matching a page header with similar words. The extractor now includes `cite`.

Case-level corrections:

- `magazine_006_科技杂志`
  - Rebuilt all existing coordinates with adaptive page/body DOM mapping.
  - Added 1 visible missing `text_block` GT item for the sidebar quote attribution:
    - `——潘建伟 院士 / 中国科学技术大学`
  - Final status: `31/31 boxed`, `0 no bbox`, `0 low-sim`.
- `magazine_007_Vogue_Fashion_EN`
  - Rebuilt all existing coordinates with adaptive body-page DOM mapping.
  - Final status: `31/31 boxed`, `0 no bbox`, `0 low-sim`.
- `magazine_008_National_Geographic`
  - Rebuilt all existing coordinates with adaptive body-page DOM mapping.
  - Final status: `24/24 boxed`, `0 no bbox`, `0 low-sim`.
- `magazine_009_美食天地`
  - Rebuilt all existing coordinates and added a right-step flex layout left-edge correction.
  - Added 4 visible missing recipe step正文 `text_block` items:
    - Step 1 main text: `将樱花和樱叶盐渍物放入水中浸泡15分钟去除盐分，用厨房纸巾擦干水分。`
    - Step 3 main text: `在鲷鱼切片上轻轻撒盐，静置10分钟后淋上料酒。渗出的水分用厨房纸巾仔细擦干。`
    - Step 5 main text: `在蒸锅中加水，大火烧开。将步骤4的成品放在铺好烘焙纸的蒸盘上，大火蒸12至15分钟。`
    - Step 8 main text: `将樱花蒸盛入碗中，旁边放上山椒叶味噌。用油菜花、胡萝卜花刀和芥末装饰点缀即可完成。`
  - Final status: `22/22 boxed`, `0 no bbox`, `0 low-sim`.
- `magazine_010_学术期刊目录页`
  - Rebuilt all existing coordinates with adaptive body-page DOM mapping.
  - Final status: `74/74 boxed`, `0 no bbox`, `0 low-sim`.
- `magazine_011_医学期刊_论文页`
  - Rebuilt all existing coordinates with adaptive `.page` mapping.
  - Final status: `27/27 boxed`, `0 no bbox`, `0 low-sim`.
- `magazine_012_Sports_Illustrated_EN`
  - Rebuilt all existing coordinates with adaptive body-page DOM mapping, replacing the earlier footer-only manual fix.
  - Final status: `43/43 boxed`, `0 no bbox`, `0 low-sim`.
- `magazine_013_建筑设计杂志`
  - Rebuilt all existing coordinates with adaptive `.page` mapping.
  - Final status: `41/41 boxed`, `0 no bbox`, `0 low-sim`.
- `magazine_014_The_Economist_EN`
  - Rebuilt all existing coordinates with adaptive body-page DOM mapping, replacing the earlier chart-label-only manual fix.
  - Final status: `30/30 boxed`, `0 no bbox`, `0 low-sim`.
- `magazine_015_时尚芭莎_人物专访`
  - Rebuilt all existing coordinates with adaptive body-page DOM mapping.
  - Final status: `33/33 boxed`, `0 no bbox`, `0 low-sim`.
- `magazine_016_Scientific_American_EN`
  - Rebuilt all existing coordinates with adaptive body-page DOM mapping.
  - Final status: `33/33 boxed`, `0 no bbox`, `0 low-sim`.
- `magazine_017_旅行摄影杂志`
  - Rebuilt all existing coordinates with adaptive body-page DOM mapping.
  - Final status: `28/28 boxed`, `0 no bbox`, `0 low-sim`.
- `magazine_018_Wired_Tech_EN`
  - Rebuilt all existing coordinates with adaptive body-page DOM mapping, replacing the earlier table/footer-only manual fix.
  - Final status: `39/39 boxed`, `0 no bbox`, `0 low-sim`.
- `magazine_019_读者文摘`
  - Rebuilt all existing coordinates with adaptive `.page` mapping, replacing the earlier footer-only manual fix.
  - Final status: `25/25 boxed`, `0 no bbox`, `0 low-sim`.
- `magazine_020_Rolling_Stone_Music_EN`
  - Rebuilt all existing coordinates with adaptive body-page DOM mapping; the newly collected `cite` element prevents the pullquote attribution from matching the page header.
  - Final status: `37/37 boxed`, `0 no bbox`, `0 low-sim`.

Verification:

- Applied report: `/tmp/pdb_publishing_mag006_020_adaptive_v402.json`.
- Cover QA: `review/gt_case_compare_all_fixed7/cover_audit_publishing_mag006_020_v402/`.
- Residual QA: `/tmp/pdb_publishing_magazine_residual_v402.json`.
  - `magazine_006_科技杂志`: `text_like_area=38596`; remaining residue is sidebar rule/card edges and tiny graphic/text-edge artifacts, not an exposed paragraph block.
  - `magazine_009_美食天地`: `text_like_area=41241`; remaining residue is mainly step-number circles and recipe illustration elements after adding the four missing正文 blocks.
  - `magazine_018_Wired_Tech_EN`, `magazine_020_Rolling_Stone_Music_EN`, and `magazine_005_生活周刊`: `text_like_area=0`.
  - Higher residuals in `magazine_010/012/013/015/008` are dominated by dark section bars, image/graphic blocks, or decorative page elements rather than uncovered body text.
- Front-end token: `20260606_publishing_mag006_020_adaptive_v402`.

## 20260606_legal_court_page_dom_v404

Scope:

- Repaired the full `03_legal_gov/02_court_document` subcategory after the user reported that `court_document_001_民事判决书` was severely offset in the review UI.

Root cause:

- Several court-document cases had review `width`/`height` metadata that did not match the released clean PNG dimensions, so the front-end scaled valid clean-image bboxes into the wrong coordinate system.
- The older matcher also allowed repeated court/seal text to win over the page header, and long legal paragraphs split across many DOM `<p>`/line fragments were sometimes boxed as only one visible line.

Implementation:

- Added `scripts/repair_legal_court_document_bboxes.py`.
- Rebuilt court-document bboxes from page-local DOM `Range.getClientRects`, projected into the released clean PNG dimensions.
- Prefer earlier exact duplicate matches for repeated court names to avoid seal/stamp false matches.
- Use conservative sequence matching for long legal text blocks; keep table/long-text bboxes as visual union boxes rather than shrinking to individual words.

Case-level corrections:

- `03_legal_gov/02_court_document/court_document_001_民事判决书`: `22/22 boxed`, `0 no bbox`, `0 low-sim`, changed `12` boxes.
- `03_legal_gov/02_court_document/court_document_002_民事裁定书`: `18/18 boxed`, `0 no bbox`, `0 low-sim`, changed `9` boxes.
- `03_legal_gov/02_court_document/court_document_003_刑事判决书`: `20/20 boxed`, `0 no bbox`, `0 low-sim`, changed `10` boxes.
- `03_legal_gov/02_court_document/court_document_004_起诉状`: `15/15 boxed`, `0 no bbox`, `0 low-sim`, changed `8` boxes.
- `03_legal_gov/02_court_document/court_document_005_调解协议书`: `24/24 boxed`, `0 no bbox`, `0 low-sim`, changed `12` boxes.
- `03_legal_gov/02_court_document/court_document_006_行政裁定书`: `41/41 boxed`, `0 no bbox`, `0 low-sim`, changed `22` boxes.
- `03_legal_gov/02_court_document/court_document_007_US_Court_Opinion`: `41/41 boxed`, `0 no bbox`, `0 low-sim`, changed `27` boxes.
- `03_legal_gov/02_court_document/court_document_008_仲裁裁决书`: `35/35 boxed`, `0 no bbox`, `0 low-sim`, changed `23` boxes.
- `03_legal_gov/02_court_document/court_document_009_知识产权判决书`: `37/37 boxed`, `0 no bbox`, `0 low-sim`, changed `19` boxes.
- `03_legal_gov/02_court_document/court_document_010_刑事附带民事判决书`: `22/22 boxed`, `0 no bbox`, `0 low-sim`, changed `6` boxes.
- `03_legal_gov/02_court_document/court_document_011_UK_High_Court_Judgment`: `26/26 boxed`, `0 no bbox`, `0 low-sim`, changed `15` boxes.
- `03_legal_gov/02_court_document/court_document_012_行政判决书_工伤认定`: `25/25 boxed`, `0 no bbox`, `0 low-sim`, changed `13` boxes.
- `03_legal_gov/02_court_document/court_document_013_执行异议裁定书_股权冻结`: `26/26 boxed`, `0 no bbox`, `0 low-sim`, changed `15` boxes.
- `03_legal_gov/02_court_document/court_document_014_二审民事判决书`: `21/21 boxed`, `0 no bbox`, `0 low-sim`, changed `10` boxes.
- `03_legal_gov/02_court_document/court_document_015_知识产权侵权判决`: `19/19 boxed`, `0 no bbox`, `0 low-sim`, changed `7` boxes.
- `03_legal_gov/02_court_document/court_document_016_仲裁裁决书_劳动`: `21/21 boxed`, `0 no bbox`, `0 low-sim`, changed `11` boxes.
- `03_legal_gov/02_court_document/court_document_017_CICC_国际商事法庭判决书`: `27/27 boxed`, `0 no bbox`, `0 low-sim`, changed `17` boxes.
- `03_legal_gov/02_court_document/court_document_018_US_Federal_Court_Opinion`: `25/25 boxed`, `0 no bbox`, `0 low-sim`, changed `12` boxes.
- `03_legal_gov/02_court_document/court_document_019_UK_High_Court_Judgment_EN`: `27/27 boxed`, `0 no bbox`, `0 low-sim`, changed `14` boxes.
- `03_legal_gov/02_court_document/court_document_020_Arbitration_Award_EN`: `22/22 boxed`, `0 no bbox`, `0 low-sim`, changed `12` boxes.
- `03_legal_gov/02_court_document/court_document_021_庭审笔录_金融借款`: `37/37 boxed`, `0 no bbox`, `0 low-sim`, changed `10` boxes.
- `03_legal_gov/02_court_document/court_document_022_海事法院船舶扣押令`: `15/15 boxed`, `0 no bbox`, `0 low-sim`, changed `6` boxes.
- `03_legal_gov/02_court_document/court_document_023_司法鉴定意见书_笔迹`: `22/22 boxed`, `0 no bbox`, `0 low-sim`, changed `9` boxes.
- `03_legal_gov/02_court_document/court_document_024_检察院起诉书_虚开发票`: `26/26 boxed`, `0 no bbox`, `0 low-sim`, changed `8` boxes.
- `03_legal_gov/02_court_document/court_document_025_公证书_涉外继承`: `21/21 boxed`, `0 no bbox`, `0 low-sim`, changed `9` boxes.

GT annotation change:

- No GT annotations were added or removed in v404; this pass rebuilt existing bbox coordinates and synchronized case dimensions for court-document pages.

Verification:

- Applied report: `/tmp/pdb_legal_court_document_v404.json`.
- Cover QA: `review/gt_case_compare_all_fixed7/cover_audit_legal_court_v404/`.
- Final subcategory status after v404: 25 cases, 635 annotations, `635/635 boxed`, `0 no bbox`, `0 low-sim`.

## 20260606_legal_court_007_footnotes_v405

Scope:

- Targeted correction for `03_legal_gov/02_court_document/court_document_007_US_Court_Opinion`.

GT annotation change:

- Completed an existing truncated `reference` GT item rather than adding a new instance.
- `#40 reference` text length changed from `700` chars to `1768` chars by replacing the truncated source with the full visible `.footnotes` DOM content for footnotes `1-5`.
- `#40 bbox` expanded from `[279,13238,2201,13586]` to `[279,13231,2202,14145]`.

Reason:

- Residual QA showed visible footnotes 3-5 still exposed after v404. The source HTML contains one `.footnotes` block with footnotes 1-5, while the review GT text had been truncated after part of footnote 3.

Verification:

- Applied report: `/tmp/pdb_legal_court_document_v405.json`.
- Cover QA: `review/gt_case_compare_all_fixed7/cover_audit_legal_court_007_v405/11_court_document_007_US_Court_Opinion_cover.jpg`.
- Residual QA: `/tmp/pdb_legal_court_007_residual_v405.json`; `text_like_area=0`, `components=0`.
- Final case status: `41/41 boxed`, `0 no bbox`, `0 low-sim`.

## 20260606_0304_dimension_sync_v406

Scope:

- Synchronized review-page dimensions for `03_legal_gov` and `04_business` against the local released clean PNGs.

Root cause:

- The review UI scales each bbox using the case-level `width`/`height`. Many 03/04 cases had correct or near-correct clean-image bboxes but stale dimensions such as `2480x3508`, `794x1123`, or old cropped heights. This made the front-end overlay visibly shifted or squeezed even when bbox coordinates themselves were in clean-image space.

Implementation:

- Added `scripts/sync_review_case_dimensions.py`.
- Updated only case `width`/`height`; no bbox coordinates, GT text, annotation counts, or categories were changed.

Case-level dimension corrections:

- `03_legal_gov/01_gov_document/gov_document_002_国务院批复`: `2481x7175` -> `2481x7688`.
- `03_legal_gov/01_gov_document/gov_document_026_国家标准_关键信息基础设施`: `2480x3508` -> `2481x12075`.
- `03_legal_gov/01_gov_document/gov_document_027_INTERPOL_Red_Notice`: `2480x3508` -> `2481x4397`.
- `03_legal_gov/01_gov_document/gov_document_028_UN_Security_Council_Resolution`: `2480x3508` -> `2481x6238`.
- `03_legal_gov/01_gov_document/gov_document_029_最高法司法解释_AIGC著作权`: `2480x3508` -> `2481x6738`.
- `03_legal_gov/01_gov_document/gov_document_030_海关进出口报关单`: `2480x3508` -> `2481x3722`.
- `03_legal_gov/03_notarial_document/notarial_document_001_房产继承公证书`: `2481x7956` -> `2481x7831`.
- `03_legal_gov/03_notarial_document/notarial_document_002_Notarized_Translation_Certificate`: `2481x6575` -> `2481x6322`.
- `03_legal_gov/03_notarial_document/notarial_document_003_遗嘱公证书`: `2480x7800` -> `2481x11188`.
- `03_legal_gov/03_notarial_document/notarial_document_004_US_Escrow_Agreement`: `2480x5600` -> `2481x8353`.
- `03_legal_gov/03_notarial_document/notarial_document_005_UK_Affidavit_of_Service`: `2480x5500` -> `2481x7613`.
- `03_legal_gov/03_notarial_document/notarial_document_006_Notarized_Power_of_Attorney_EN`: `2480x5000` -> `2481x4475`.
- `03_legal_gov/03_notarial_document/notarial_document_007_Certified_Translation_EN`: `2480x4500` -> `2481x3509`.
- `03_legal_gov/03_notarial_document/notarial_document_008_Declaration_Under_Oath_EN`: `2480x4200` -> `2481x3981`.
- `03_legal_gov/03_notarial_document/notarial_document_009_US_Corporate_Resolution`: `2480x5500` -> `2481x6500`.
- `03_legal_gov/03_notarial_document/notarial_document_010_海牙认证附页`: `2480x4200` -> `2481x3509`.
- `03_legal_gov/03_notarial_document/notarial_document_011_德式公证_Urkunde_EN`: `2480x4500` -> `2481x5141`.
- `03_legal_gov/03_notarial_document/notarial_document_012_US_Medical_Directive`: `2480x5500` -> `2481x6825`.
- `03_legal_gov/03_notarial_document/notarial_document_013_UK_Grant_of_Probate`: `2480x5500` -> `2481x7063`.
- `03_legal_gov/03_notarial_document/notarial_document_014_US_Promissory_Note`: `2480x5800` -> `2481x7259`.
- `03_legal_gov/03_notarial_document/notarial_document_015_涉外收养公证`: `2480x5500` -> `2481x3903`.
- `03_legal_gov/03_notarial_document/notarial_document_016_US_Acknowledgment_Real_Estate`: `2480x5500` -> `2481x6156`.
- `03_legal_gov/03_notarial_document/notarial_document_017_UK_Statutory_Declaration`: `2480x5500` -> `2481x6834`.
- `03_legal_gov/03_notarial_document/notarial_document_018_US_Trust_Certification`: `2480x5500` -> `2481x6263`.
- `03_legal_gov/03_notarial_document/notarial_document_019_UK_Deed_Poll`: `2480x5500` -> `2481x5531`.
- `03_legal_gov/03_notarial_document/notarial_document_020_US_Notarized_Custody_Agreement`: `2480x5800` -> `2481x6638`.
- `03_legal_gov/03_notarial_document/notarial_document_021_US_Notarized_Vehicle_Bill_of_Sale`: `2480x5500` -> `2481x5484`.
- `03_legal_gov/04_license_permit/business_license_001_营业执照`: `2781x3509` -> `2481x3509`.
- `03_legal_gov/04_license_permit/business_license_002_食品经营许可证`: `2481x3722` -> `2481x3509`.
- `03_legal_gov/04_license_permit/business_license_003_职业资格证书`: `2481x4147` -> `2481x3509`.
- `03_legal_gov/04_license_permit/business_license_004_培训结业证书_双语`: `2481x4628` -> `2481x3509`.
- `03_legal_gov/04_license_permit/license_permit_005_建筑施工许可证`: `2481x6872` -> `2481x6684`.
- `03_legal_gov/04_license_permit/license_permit_006_Driving_License_Multi`: `2480x4500` -> `2481x3509`.
- `03_legal_gov/04_license_permit/license_permit_007_药品GSP许可册`: `2480x5800` -> `2481x5250`.
- `03_legal_gov/04_license_permit/license_permit_008_道路运输资质卡`: `2480x4600` -> `2481x3509`.
- `03_legal_gov/04_license_permit/license_permit_009_危化品经营许可证`: `2480x6500` -> `2481x3613`.
- `03_legal_gov/04_license_permit/license_permit_010_医疗机构执业许可证`: `2480x5500` -> `2481x3509`.
- `03_legal_gov/04_license_permit/license_permit_011_安全生产许可Dashboard`: `2480x6500` -> `2481x4250`.
- `03_legal_gov/04_license_permit/license_permit_012_特种设备金属铭牌`: `2480x5800` -> `2481x4406`.
- `03_legal_gov/04_license_permit/license_permit_013_网络安全等级保护备案`: `2480x5500` -> `2481x3509`.
- `03_legal_gov/04_license_permit/license_permit_014_Business_License_US`: `2480x5500` -> `2481x4553`.
- `03_legal_gov/04_license_permit/license_permit_015_Liquor_License_EN`: `2480x5800` -> `2481x4141`.
- `03_legal_gov/04_license_permit/license_permit_016_NYC_Health_Decal`: `2480x6800` -> `2481x5144`.
- `03_legal_gov/04_license_permit/license_permit_017_PE_License_Portal`: `2480x6800` -> `2591x4388`.
- `03_legal_gov/04_license_permit/license_permit_018_Real_Estate_License`: `2480x5500` -> `2481x3644`.
- `03_legal_gov/04_license_permit/license_permit_019_Import_License_EN`: `2480x6000` -> `2481x3634`.
- `03_legal_gov/04_license_permit/license_permit_020_食品生产许可证_mixed`: `2480x5800` -> `2481x3509`.
- `03_legal_gov/04_license_permit/license_permit_021_民办学校办学Dashboard`: `2480x6800` -> `2481x4359`.
- `03_legal_gov/04_license_permit/license_permit_022_烟草零售证_App截图`: `2480x4500` -> `2481x3947`.
- `03_legal_gov/04_license_permit/license_permit_023_ATF_FFL_Audit`: `2480x7000` -> `2481x5256`.
- `03_legal_gov/04_license_permit/license_permit_024_无线电频谱可视化`: `2480x6500` -> `2481x4559`.
- `03_legal_gov/04_license_permit/license_permit_025_CSLB_LinkedIn_Profile`: `2480x7500` -> `2481x6384`.
- `03_legal_gov/05_legislation/legislation_001_中华人民共和国数据安全法`: `2481x10375` -> `2481x10163`.
- `03_legal_gov/05_legislation/legislation_002_EU_GDPR_Excerpt`: `2481x10272` -> `2481x9719`.
- `03_legal_gov/05_legislation/legislation_003_劳动合同法实施条例`: `2481x10528` -> `2481x10141`.
- `03_legal_gov/05_legislation/legislation_004_California_Consumer_Privacy_Act`: `2480x10500` -> `2481x9578`.
- `03_legal_gov/05_legislation/legislation_005_城市房屋拆迁管理条例`: `2480x7500` -> `2481x8609`.
- `03_legal_gov/05_legislation/legislation_006_民法典_合同编`: `2480x11500` -> `2481x13059`.
- `03_legal_gov/05_legislation/legislation_007_US_Uniform_Commercial_Code`: `2480x11000` -> `2481x10744`.
- `03_legal_gov/05_legislation/legislation_008_UK_Companies_Act_Schedule`: `2480x10500` -> `2481x7703`.
- `03_legal_gov/05_legislation/legislation_009_US_Clean_Air_Act`: `2480x11000` -> `2481x8728`.
- `03_legal_gov/05_legislation/legislation_010_Australia_Privacy_Act`: `2480x11000` -> `2481x8753`.
- `03_legal_gov/05_legislation/legislation_011_US_Dodd_Frank_Act`: `2480x11000` -> `2481x8984`.
- `03_legal_gov/05_legislation/legislation_012_Canada_Criminal_Code`: `2480x11500` -> `2481x10931`.
- `03_legal_gov/05_legislation/legislation_013_US_ADA_Accessibility`: `2480x11000` -> `2481x10322`.
- `03_legal_gov/05_legislation/legislation_014_Tax_Code_Section_EN`: `2480x9500` -> `2481x3509`.
- `03_legal_gov/05_legislation/legislation_015_GDPR_Article_EN`: `2480x9500` -> `2481x3509`.
- `03_legal_gov/05_legislation/legislation_016_SEC_Exemption_Flowchart`: `2480x7800` -> `2481x5241`.
- `03_legal_gov/05_legislation/legislation_017_Ontario_ESA_Workplace_Poster`: `2480x8500` -> `2481x5122`.
- `03_legal_gov/05_legislation/legislation_018_ACCC_Chatbot`: `2480x9000` -> `2481x7106`.
- `03_legal_gov/05_legislation/legislation_019_WIPO_PLT_Dashboard`: `2480x7800` -> `2481x5406`.
- `03_legal_gov/05_legislation/legislation_020_民法典继承可视化图谱`: `2480x8500` -> `2481x7622`.
- `03_legal_gov/05_legislation/legislation_027_EU_AI_Act_Pyramid`: `2480x11000` -> `2481x7778`.
- `03_legal_gov/05_legislation/legislation_028_网络数据安全条例_监管沙盒`: `2480x11000` -> `2481x7406`.
- `03_legal_gov/05_legislation/legislation_029_Canada_Criminal_Code_Bilingual`: `2480x7000` -> `2481x4753`.
- `03_legal_gov/05_legislation/legislation_030_突发事件应对法_修订对照`: `2480x8500` -> `2481x5313`.
- `03_legal_gov/06_accident_report/accident_report_001_交通事故认定书`: `2480x7000` -> `2481x7547`.
- `03_legal_gov/06_accident_report/accident_report_002_Incident_Report_EN`: `2480x7500` -> `2481x8053`.
- `04_business/03_formal_letter/formal_letter_008_Business_Letter_EN`: `794x1123` -> `2544x4800`.
- `04_business/03_formal_letter/formal_letter_010_Resignation_Letter_EN`: `794x1123` -> `2544x5534`.
- `04_business/04_meeting_memo/meeting_memo_015_研发项目评审会纪要`: `2481x3509` -> `2481x5919`.

GT annotation change:

- No GT annotations were added or removed; no bbox coordinates were changed by v406.

Verification:

- Applied report: `/tmp/pdb_0304_dimension_sync_v406.json`.
- Post-sync structural audit:
  - `03_legal_gov`: `151` cases, `3672` annotations, `0` bad dimensions, `0` off-page boxes.
  - `04_business`: `160` cases, `8471` annotations, `0` bad dimensions, `0` off-page boxes.
- Front-end token: `20260606_0304_dimension_sync_v406`.

## 20260606_business_handbook_residual_sections_v411_v412

Scope:

- `04_business/07_employee_handbook/employee_handbook_001_互联网大厂`
- `04_business/07_employee_handbook/employee_handbook_002_Manufacturing_Safety`

What changed:

- v411 expanded existing handbook boxes from residual/cover evidence:
  - `employee_handbook_001`: 48 existing annotation bboxes expanded.
  - `employee_handbook_002`: 33 existing annotation bboxes expanded.
- v412 corrected remaining shifted handbook section boxes from DOM:
  - `employee_handbook_001`: corrected #18, #41, #58, #60, #78.
  - `employee_handbook_002`: corrected #8, #10, #29, #54.

GT annotation change:

- Added GT annotations: 0.
- Removed GT annotations: 0.

## 20260606_business_formal_letters_dom_v413_v414

Scope:

- `04_business/03_formal_letter/formal_letter_014_Cease_and_Desist_EN`
- `04_business/03_formal_letter/formal_letter_018_Termination_Notice_EN`

What changed:

- `formal_letter_014_Cease_and_Desist_EN`: remeasured all 26 existing annotations from DOM.
- `formal_letter_018_Termination_Notice_EN`: remeasured all 43 existing annotations from DOM.

GT annotation change:

- Added GT annotations: 0.
- Removed GT annotations: 0.

## 20260606_business_meeting_memo012_dom_v415

Scope:

- `04_business/04_meeting_memo/meeting_memo_012_Strategic_Planning_Offsite_ENZH`

What changed:

- Remeasured all 47 existing annotations from the DOM `.page` root.
- Fixed major mixed-coordinate offsets including #13, #30, #44 and related lower-page memo sections.

GT annotation change:

- Added GT annotations: 0.
- Removed GT annotations: 0.

Verification:

- Residual reduced from about `1,096,875` to `64,962` text-like pixels.
- Cover audit: `cover_audit_business_meeting_memo012_v415/11_meeting_memo_012_Strategic_Planning_Offsite_ENZH_cover.jpg`.

## 20260606_business_contract022_residual_expand_v416

Scope:

- `04_business/01_contract/contract_022_深海微生物跨国转让合同`

What changed:

- Conservatively expanded 59 existing annotation bboxes from residual/cover evidence.
- Rejected a DOM-gated rewrite because it would have reduced boxed annotations and introduced no-bbox items.

GT annotation change:

- Added GT annotations: 0.
- Removed GT annotations: 0.

Verification:

- Residual reduced from `793,821` to `520,889` text-like pixels.
- Remaining residual is mostly right-page schedules, flow/finance diagrams, and fine edge text; this case still needs deeper manual pass if targeting near-zero residual.

## 20260606_business_meeting_memo009_dom_vote_tables_v417

Scope:

- `04_business/04_meeting_memo/meeting_memo_009_董事会决议纪要`

What changed:

- Remeasured the original 42 annotations from DOM `.page`.
- Fixed large shifted boxes, including attendee/body sections and lower voting-result regions.
- Inserted 8 missing GT annotations for voting-result blocks:
  - `议案一表决情况` title.
  - Vote table for proposal 1.
  - `议案二表决情况（关联董事回避）` title.
  - Vote table for proposal 2.
  - `议案三表决情况` title.
  - Vote table for proposal 3.
  - `议案四表决情况` title.
  - Vote table for proposal 4.

GT annotation change:

- Added GT annotations: 8.
- Removed GT annotations: 0.
- Count changed from 42 to 50.

Verification:

- Residual reduced from `755,313` to `32,479` text-like pixels.
- Cover audit: `cover_audit_business_meeting_memo009_v417/11_meeting_memo_009_董事会决议纪要_cover.jpg`.

## 20260606_business_bp001_add_chart_v418

Scope:

- `04_business/06_business_plan/business_plan_001_智能农业科技公司商业计划书`

What changed:

- Added the missing market-size bar chart as one `figure` annotation after the market analysis paragraph and before SWOT.
- Added text begins: `中国智慧农业市场规模（亿元） 2022 456 ... 2028E 1,520`.

GT annotation change:

- Added GT annotations: 1.
- Removed GT annotations: 0.
- Count changed from 56 to 57.

Verification:

- Residual reduced from `710,889` to `184,369` text-like pixels.
- Cover audit: `cover_audit_business_bp001_v418/11_business_plan_001_智能农业科技公司商业计划书_cover.jpg`.

## 20260606_business_formal_letter001_dom_v419

Scope:

- `04_business/03_formal_letter/formal_letter_001_律师函_知识产权侵权`

What changed:

- Corrected #0 letterhead/header bbox from `[871,502,1610,745]` to `[109,123,2372,808]`.
- Corrected #19 software-infringement body/list bbox from `[353,5427,1955,5493]` to `[189,4777,2370,5549]`.

GT annotation change:

- Added GT annotations: 0.
- Removed GT annotations: 0.

Verification:

- Residual reduced from `592,184` to `175,182` text-like pixels.

## 20260606_legal_legislation026_dom_v420

Scope:

- `03_legal_gov/05_legislation/legislation_026_工程竣工验收记录`

What changed:

- Remeasured all 18 existing annotations from DOM `.wrap`.
- Corrected the large shifted quality-score table, project information tables, notice block, and five signature cards.
- Decorative blue `建` icon was not added as GT.

GT annotation change:

- Added GT annotations: 0.
- Removed GT annotations: 0.

Verification:

- Residual reduced from `968,141` to `36,778` text-like pixels.
- Cover audit: `cover_audit_legal_legislation026_v420/11_legislation_026_工程竣工验收记录_cover.jpg`.

## 20260606_legal_accident_report017_dom_v421

Scope:

- `03_legal_gov/06_accident_report/accident_report_017_FDA_MedWatch_Adverse_Event`

What changed:

- Corrected #14 from a too-wide suspect-device table bbox to the right-half table only.
- Expanded #19 from a caption-only bbox to the full patient clinical timeline figure block.
- Moved #21 from an incorrect upper-page location to the F. Manufacturer Device Analysis table.
- Moved #23 from an incorrect upper-page location to the CAPA table.

GT annotation change:

- Added GT annotations: 0.
- Removed GT annotations: 0.

Verification:

- Residual audit after v421: `text_like=0`, `comps=0`.
- Cover audit: `cover_audit_legal_accident_report017_v421/11_accident_report_017_FDA_MedWatch_Adverse_Event_cover.jpg`.

## 20260606_legal_accident_report016_dom_v422

Scope:

- `03_legal_gov/06_accident_report/accident_report_016_US_Police_Traffic_Report`

What changed:

- Corrected 7 colored section-title bboxes (#3, #5, #7, #9, #11, #13, #15) from tight text-only boxes to full blue title bars.
- Expanded #14 from a caption-only bbox to the full collision diagram SVG block.
- Expanded #16 Officer Narrative from a lower text-only bbox to the full narrative panel.
- Left the already-tight page header and normal tables unchanged to avoid over-boxing whitespace.

GT annotation change:

- Added GT annotations: 0.
- Removed GT annotations: 0.

Verification:

- Residual reduced from `893,929` to `11,500` text-like pixels.
- Cover audit: `cover_audit_legal_accident_report016_v422/11_accident_report_016_US_Police_Traffic_Report_cover.jpg`.

## 20260606_legal_gov_document027_dom_v423_v424

Scope:

- `03_legal_gov/01_gov_document/gov_document_027_INTERPOL_Red_Notice`

What changed:

- v423 corrected #3 `RED NOTICE` to the full red badge bbox.
- v423 corrected colored section-title bboxes #6, #8, #10, #12, #14 to full blue section bars.
- v423 expanded #16/#17 to cover the red action warning panel.
- v424 tightened over-wide topbar text boxes #0, #1, #2 using text-range measurement instead of block-element width.
- Did not add GT for the INTERPOL emblem, subject photograph placeholder, fingerprint placeholders, or QR placeholder because the original HF GT has no corresponding figure/image instances for those elements.

GT annotation change:

- Added GT annotations: 0.
- Removed GT annotations: 0.

Verification:

- Residual after v424: `203,116` text-like pixels; remaining high residual is dominated by unannotated decorative/placeholder elements.
- Cover audit: `cover_audit_legal_gov_document027_v424/11_gov_document_027_INTERPOL_Red_Notice_cover.jpg`.

## 20260606_legal_accident_report011_dom_v425

Scope:

- `03_legal_gov/06_accident_report/accident_report_011_US_DOT_Pipeline_Incident`

What changed:

- Corrected colored section bars #21, #23, #25, #28, #30 to full-width brown title bars.
- Corrected #26/#27 narrative paragraphs so they start below the `NARRATIVE DESCRIPTION OF INCIDENT` title bar instead of overlapping it.
- Corrected corrective-action rows #31, #32, #33, #34 to cover full form rows including right-side `Deadline` cells.
- Expanded #35 `FINAL REPORT` to the full rotated stamp bbox.

GT annotation change:

- Added GT annotations: 0.
- Removed GT annotations: 0.

Verification:

- Residual reduced from `800,500` to `45,864` text-like pixels.
- Cover audit: `cover_audit_legal_accident_report011_v425/11_accident_report_011_US_DOT_Pipeline_Incident_cover.jpg`.

## 20260606_business_meeting_memo015_dom_v426_v428

Scope:

- `04_business/04_meeting_memo/meeting_memo_015_研发项目评审会纪要`

What changed:

- v426 remeasured all 36 existing annotations against explicit DOM targets.
- Fixed major wrong placements where #9, #11, #13, #18, #19, #32 and related items had been mapped near the page header instead of their true middle/lower-page content.
- Mapped the original semantic summary items to their visible source regions:
  - #9 to the multi-dimensional scoring matrix table.
  - #11 to the technical KPI table.
  - #13 to the resource allocation table.
  - #15-#20 to the six Go/No-Go table rows.
- Corrected risk rows #22-#26, action rows #28-#33, signature block #34, and footer #35.
- v427/v428 manually widened the Chinese header title/subtitle boxes #0, #1, #2 after cover QA showed under-covered trailing characters from browser text-range measurement.

GT annotation change:

- Added GT annotations: 0.
- Removed GT annotations: 0.

Verification:

- Residual reduced from `635,659` to `67,299` text-like pixels.
- Cover audit: `cover_audit_business_meeting_memo015_v427/11_meeting_memo_015_研发项目评审会纪要_cover.jpg`.

## 20260606_business_formal_letter016_manual_v431

Scope:

- `04_business/03_formal_letter/formal_letter_016_Notice_of_Default_EN`

What changed:

- Rejected v429 full DOM rewrite after QA showed local Playwright font metrics compressed table heights relative to the release clean image.
- Restored this case to the pre-v429 baseline and applied targeted manual expansions only.
- Expanded #3 to include the missing `EIN / DUNS` borrower line.
- Expanded #5 and #7 to cover the full `Re:` paragraph and the full introductory paragraph.
- Expanded #13, #18, and #21 to include their second-line explanatory text below the section headings.
- Expanded legal/cure/warning content blocks #25, #27, #29, #31, #32, #33, and #36 to include missing lower lines and enclosure text.

GT annotation change:

- Added GT annotations: 0.
- Removed GT annotations: 0.

Verification:

- Residual reduced from `520,889` to `18,413` text-like pixels.
- Remaining residual components are panel/box/signature rules, not exposed body text.
- Cover audit: `cover_audit_business_formal_letter016_v431/11_formal_letter_016_Notice_of_Default_EN_cover.jpg`.

## 20260606_legal_gov_document008_bilingual_v433

Scope:

- `03_legal_gov/01_gov_document/gov_document_008_中美双语_合作备忘录`

What changed:

- Corrected bilingual article title/content bboxes #5-#10 and #12-#19 from one-sided/right-column placement to full-width left+right bilingual row bboxes, matching the original GT text that combines Chinese and English in a single instance.
- Corrected #0 Chinese heading/decorative star block from a low misplaced box to the top heading region.
- Corrected #22 footer from the bottom blank area to the actual bilingual authenticity footer line above the signature blocks.

GT annotation change:

- Added GT annotations: 0.
- Removed GT annotations: 0.

Verification:

- Residual reduced from `715,807` to `0` text-like pixels.
- Cover audit: `cover_audit_legal_gov008_v433/11_gov_document_008_中美双语_合作备忘录_cover.jpg`.

## 20260606_legal_legislation004_manual_v435

Scope:

- `03_legal_gov/05_legislation/legislation_004_California_Consumer_Privacy_Act`

What changed:

- Expanded #19 and #27 to include the lower numbered statutory subitems that were visibly exposed below the original boxes.
- Moved #0 from the department subtitle line back to the actual `STATE OF CALIFORNIA` heading.
- Expanded #8 upward to cover the full digest paragraph instead of only its lower lines.

GT annotation change:

- Added GT annotations: 0.
- Removed GT annotations: 0.

Verification:

- Residual reduced from `745,507` to `15,979` text-like pixels.
- Remaining residual components are the page-header scale icon, horizontal divider, and one tiny edge artifact rather than exposed body text.
- Cover audit: `cover_audit_legal_legislation004_v435/11_legislation_004_California_Consumer_Privacy_Act_cover.jpg`.

## 20260606_legal_gov_document009_manual_v437

Scope:

- `03_legal_gov/01_gov_document/gov_document_009_EU_Official_Journal`

What changed:

- Expanded #2 to cover the full regulation title block, not only the final subtitle lines.
- Expanded #19, #21, and #25 to cover the exposed lower lines of Article 1, Article 2 definitions, and Article 4 systemic evaluations.
- Expanded #37 to include the lower signature names.
- Expanded #39 to include the footnote and copyright/footer text that belonged to the same GT item.

GT annotation change:

- Added GT annotations: 0.
- Removed GT annotations: 0.

Verification:

- Residual reduced from `581,754` to `0` text-like pixels.
- Cover audit: `cover_audit_legal_gov009_v437/11_gov_document_009_EU_Official_Journal_cover.jpg`.

## 20260606_legal_legislation002_manual_v439

Scope:

- `03_legal_gov/05_legislation/legislation_002_EU_GDPR_Excerpt`

What changed:

- Expanded #1 and #2 to cover the complete GDPR regulation title/subtitle block.
- Expanded recital blocks #3, #4, and #5 so each covers its full highlighted recital card.
- Moved #7 back to the actual Article 1 heading and expanded #8 for the full Article 1 text.
- Expanded #10 to include the full visible Article 4 definitions block including the lower `processor` row.
- Expanded #13 to include the full Article 5 principles block and final `accountability` line.
- Moved #14 down to the real Article 6 heading, then expanded #15 and #17 for the full Article 6 and Article 7 text blocks.

GT annotation change:

- Added GT annotations: 0.
- Removed GT annotations: 0.

Verification:

- Residual reduced from `547,437` to `1,513` text-like pixels.
- Remaining residual components are tiny card-edge artifacts, not exposed body text.
- Cover audit: `cover_audit_legal_legislation002_v439/11_legislation_002_EU_GDPR_Excerpt_cover.jpg`.

## 20260606_business_contract022_manual_v443

Scope:

- `04_business/01_contract/contract_022_深海微生物跨国转让合同`

What changed:

- Re-aligned the right-page Schedule A term list (#67-#76), Schedule C formula/waterfall area (#79/#84), Schedule E checklist (#87-#97), milestone table (#98/#99), and legal review block (#101-#105) to their actual rendered positions.
- Re-aligned the left-page NLI equation (#46), Article 4 ending paragraph (#26), and lower royalty waterfall tier explanation.
- Expanded #97 and #101 after residual review so the red Schedule E warning and first legal-review item are fully covered.

GT annotation change:

- Added GT annotations: 3.
- Added #107 `figure`: `Schedule D patent ownership flowchart / 专利权归属流程图`.
- Added #108 `text_block`: left-page NLI tier explanation for the three royalty allocation tiers.
- Added #109 `title`: `Revenue Allocation Formula`.
- Removed GT annotations: 0.

Verification:

- Residual reduced from `520,889` to `48,919` text-like pixels.
- Remaining residual components are the central decorative spine, small badges, page/footer lines, and thin edge artifacts rather than exposed body text.
- Cover audit: `cover_audit_business_contract022_v443/11_contract_022_深海微生物跨国转让合同_cover.jpg`.

## 20260606_legal_legislation022_manual_v445

Scope:

- `03_legal_gov/05_legislation/legislation_022_GDPR_PIPL_Quick_Reference`

What changed:

- Rebuilt all 18 existing bboxes from the actual HTML block structure: hero title/subtitle/badge, tab row, EU GDPR card, China PIPL card, core comparison title/table, penalties title/table, KPI title/grid, notice, and footer.
- Corrected the previous fragment-level boxes that only covered small words inside each block and left most table/card content exposed.
- Applied a second edge pass for the badge icon, EU/CN card headings, and penalties/KPI headings.

GT annotation change:

- Added GT annotations: 0.
- Removed GT annotations: 0.

Verification:

- Residual reduced from `496,248` to `124,824` text-like pixels.
- Remaining residual components are card bottom border/shadow and tiny KPI/edge artifacts rather than exposed body text.
- Cover audit: `cover_audit_legal_legislation022_v445/11_legislation_022_GDPR_PIPL_Quick_Reference_cover.jpg`.

## 20260606_legal_legislation024_manual_v446

Scope:

- `03_legal_gov/05_legislation/legislation_024_证据登记保管单`

What changed:

- Rebuilt all 16 existing bboxes from the actual HTML form structure: court header, document title, document number, four section headers, four tables, notice block, three signature columns, and footer.
- Corrected the previous fragment-level boxes that only covered isolated words inside the tables and left most rows/columns visually exposed.
- Kept the three signature GT instances separate rather than merging the full signature area.

GT annotation change:

- Added GT annotations: 0.
- Removed GT annotations: 0.

Verification:

- Residual reduced from `469,497` to `62,465` text-like pixels.
- Remaining residual components are the page-header divider and short signature/edge lines rather than exposed body text.
- Cover audit: `cover_audit_legal_legislation024_v446/11_legislation_024_证据登记保管单_cover.jpg`.

## 20260606_business_employee_handbook009_manual_v449

Scope:

- `04_business/07_employee_handbook/employee_handbook_009_Travel_Expense`

What changed:

- Rebuilt the 20 existing bboxes for the Travel & Expense handbook page from the rendered HTML blocks: header, banner title/subtitle/meta, travel request panel, standards table, non-reimbursable list, approval/checklist title, reimbursement flow/formula, overseas travel title/paragraph/table, FAQ, notes, and footer/page number.
- Expanded #8 to include the list bullet markers after residual review.

GT annotation change:

- Added GT annotations: 5.
- Added #20 `title`: `💳 9.1A 标准费用上限 / Expense Standards`.
- Added #21 `figure`: `出差前审批检查卡` checklist card.
- Added #22 `figure`: `报销流转图` reimbursement workflow card.
- Added #23 `title`: `票据例外矩阵 / Receipt Exceptions`.
- Added #24 `figure`: `票据例外矩阵` receipt exception matrix.
- Removed GT annotations: 0.

Verification:

- Residual reduced from `519,962` to `0` text-like pixels.
- Cover audit: `cover_audit_business_employee_handbook009_v449/11_employee_handbook_009_Travel_Expense_cover.jpg`.

## 20260606_legal_license015_v460

Scope:

- `03_legal_gov/04_license_permit/license_permit_015_Liquor_License_EN`

What changed:

- Rebuilt all 19 existing bboxes from the rendered HTML DOM containers.
- Corrected the top agency/state/title/license-number rows (#0-#3), which previously overlapped around a tiny central header area.
- Corrected the major section/table blocks (#4-#14), including Licensee Information, License Classification, Conditions, Fee Schedule, and Disciplinary Record; the old Fee Schedule and Disciplinary blocks were vertically collapsed onto the same area.
- Corrected the three signature blocks (#15-#17) and footer/contact line (#18), which previously sat around the wrong lower-page region.

GT annotation change:

- Added GT annotations: 0.
- Removed GT annotations: 0.

Verification:

- Residual reduced from `317,572` to `65,904` text-like pixels.
- Remaining residual components are decorative gold rules, stars, and official-seal text, not exposed body/table text.
- Cover audit: `cover_audit_legal_license015_v460/11_license_permit_015_Liquor_License_EN_cover.jpg`.

## 20260606_legal_legislation025_v461

Scope:

- `03_legal_gov/05_legislation/legislation_025_CISA_Cybersecurity_Advisory`

What changed:

- Rebuilt all 19 existing bboxes from explicit CISA advisory DOM containers using the `.wrap` page root, uniform scale, and horizontal centering.
- Corrected the header title/subtitle/TLP badge (#0-#2), metabar (#3), summary panel (#4), and four KPI cards (#5-#8), which were previously tiny fragments or horizontally shifted.
- Corrected section titles, vulnerability/sector/mitigation tables, MITRE ATT&CK matrix, disclaimer, and footer (#9-#18) to cover the actual rendered blocks.

GT annotation change:

- Added GT annotations: 0.
- Removed GT annotations: 0.

Verification:

- Residual reduced from `336,644` to `0` text-like pixels.
- Cover audit: `cover_audit_legal_legislation025_v461/11_legislation_025_CISA_Cybersecurity_Advisory_cover.jpg`.

## 20260606_business_resume022_manual_dom_v463

Scope:

- `04_business/05_resume/resume_022_Draft_Review_CV`

What changed:

- Superseded the intermediate `v462` hybrid DOM repair with a case-specific manual DOM selector map.
- Rebuilt existing bboxes for the dense draft-review CV from stable HTML containers/text ranges:
  version bar, review-channel notes, profile/header metadata, education and experience entries, selected publications, patents, technical skills, metrics formula/table, awards, open-comments checklist, and attachment checklist.
- Corrected the major previous problems where publication/technical-strength/comment annotations were assigned to wrong blank containers or unrelated lower-page areas.
- Kept GT granularity from the original release: publication list remains one `text_block`, skills remain one `text_block`, and the metrics table remains one `table`.

GT annotation change:

- Added GT annotations: 0.
- Removed GT annotations: 0.

Verification:

- `105/105` boxed, `0` no-bbox, `0` low-similarity after the retained `v463` write.
- Residual after retained write: `138,124` text-like pixels / `51` components.
- Residual before this repair series was `502,985`; the lower `v462` residual (`140,686`) used larger generic boxes and was superseded for visual precision.
- Cover audit: `cover_audit_business_resume022_v463/11_resume_022_Draft_Review_CV_cover.jpg`.

## 20260606_business_plan008_dom_v464

Scope:

- `04_business/06_business_plan/business_plan_008_文旅项目投资计划`

What changed:

- Rebuilt all 39 existing bboxes from explicit DOM containers/text ranges.
- Corrected the cover title/subtitle/project-meta boxes (#0-#2), which were previously shifted down near the first section boundary.
- Corrected the payback table, paragraph blocks, section headers, zone text blocks, revenue/cost rows, profit paragraph, and footer against the rendered HTML.
- Added missing figure-level GT for two obvious visual objects:
  - #39 `figure`: `运营第3年月度客流量预测柱状图`
  - #40 `figure`: `分区规划布局示意图`

GT annotation change:

- Added GT annotations: 2.
- Removed GT annotations: 0.

Verification:

- Case counts changed from `39/39 boxed` to `41/41 boxed`, `0` no-bbox, `0` low-similarity.
- Residual reduced from `448,439` to `128,341` text-like pixels.
- Cover audit: `cover_audit_business_bp008_v464/11_business_plan_008_文旅项目投资计划_cover.jpg`.

## 20260606_business_plan023_figures_v465

Scope:

- `04_business/06_business_plan/business_plan_023_Zhijie_Research_Plan`

What changed:

- Added figure-level GT for four obvious visual objects that were present in the HTML but absent from the original GT:
  - #101 `figure`: `用户增长路径与转化漏斗图`
  - #102 `figure`: `产品模块与服务流程图`
  - #103 `figure`: `用户画像与市场规模条形图`
  - #104 `figure`: `融资用途条带图`
- Existing text/table/equation bboxes were left unchanged to preserve the original GT granularity.

GT annotation change:

- Added GT annotations: 4.
- Removed GT annotations: 0.

Verification:

- Case counts changed from `101/101 boxed` to `105/105 boxed`, `0` no-bbox.
- Residual reduced from `424,908` to `115,946` text-like pixels.
- Remaining `6` low-similarity flags are pre-existing text-match quality flags, not new no-bbox items.
- Cover audit: `cover_audit_business_bp023_v465/11_business_plan_023_Zhijie_Research_Plan_cover.jpg`.

## 20260606_legal_accident005_dom_v466

Scope:

- `03_legal_gov/06_accident_report/accident_report_005_Workplace_Incident_EN`

What changed:

- Rebuilt all 18 bboxes from explicit DOM selectors/text ranges.
- Corrected header company/title/report reference (#0-#2), section titles (#3, #5, #7, #9, #11, #13), incident-information/root-cause/corrective-actions tables (#4, #8, #12), and narrative paragraphs (#6, #10).
- Filled the 5 previously missing existing GT bboxes:
  - #13 `6. Signatures`
  - #14 `Lead Investigator — Sarah Chen, EHS Manager`
  - #15 `Plant Manager — David K. Torres`
  - #16 `VP Operations — Patricia M. Reeves`
  - #17 footer confidentiality line
- Coordinate note: this HTML overflows the fixed A4 `.page`, while the clean image is a full-page screenshot. The repair uses the uniform screenshot scale from the x axis for y coordinates to avoid pushing lower content out of the image.

GT annotation change:

- Added GT annotations: 0.
- Removed GT annotations: 0.

Verification:

- Case counts changed from `13/18 boxed, 5 no-bbox` to `18/18 boxed, 0 no-bbox, 0 low-similarity`.
- Residual reduced from `193,210` to `0` text-like pixels.
- Cover audit: `cover_audit_legal_accident005_v466/11_accident_report_005_Workplace_Incident_EN_cover.jpg`.

## 20260606_legal_license014_dom_v467

Scope:

- `03_legal_gov/04_license_permit/license_permit_014_Business_License_US`

What changed:

- Rebuilt all 20 bboxes from explicit DOM selectors/text ranges.
- Corrected the global y-offset caused by using the fixed A4 `.page` height on an overflowing full-page screenshot.
- Re-aligned the header/title/license-number boxes (#0-#4), section titles (#5, #7, #9, #11, #13), field/table-like regions (#6, #8, #10), permit and condition lists (#12, #14), issue date (#18), and footer (#19).
- Filled the 3 previously missing existing GT bboxes:
  - #15 `City Clerk — Jannette S. Goodall`
  - #16 `Director, Dev. Services — Denise V. Lucas`
  - #17 `Licensee / Agent — Michael R. Thornton`
- Did not add a new GT item for the circular `CITY OF AUSTIN TEXAS OFFICIAL SEAL`; this follows the standing rule that decorative seals/logos/watermarks are not added unless already present in source GT or explicitly requested.

GT annotation change:

- Added GT annotations: 0.
- Removed GT annotations: 0.

Verification:

- Case counts changed from `17/20 boxed, 3 no-bbox` to `20/20 boxed, 0 no-bbox, 0 low-similarity`.
- Residual reduced from `105,701` to `27,084` text-like pixels.
- Remaining residual is the official seal and decorative rules, not exposed body/table text.
- Cover audit: `cover_audit_legal_license014_v467/11_license_permit_014_Business_License_US_cover.jpg`.

## 20260606_business_meeting_memo020_low_sim_v468

Scope:

- `04_business/04_meeting_memo/meeting_memo_020_Compliance_Review_Meeting_EN`

What changed:

- Applied a local DOM repair only to the 22 low-similarity / visibly shifted annotations rather than rebuilding the whole dense memo.
- Corrected top metadata line boxes (#4-#9) and the duplicate header text block (#1).
- Corrected three-column compliance-stat items (#52, #59, #62, #67, #71).
- Corrected clearly wrong table/list/signature assignments:
  - #76 CARM table header moved back to the CARM header row.
  - #86 `CAR-010...` moved back to the CARM final row.
  - #117/#118 policy-update list items moved from the earlier regulatory-landscape area back to the right policy list.
  - #135/#137 signature titles moved back under the correct signature names.
- Corrected inspection-card location lines (#101, #104, #110, #113).

GT annotation change:

- Added GT annotations: 0.
- Removed GT annotations: 0.

Verification:

- Case counts remain `141/141 boxed, 0 no-bbox`.
- Low-similarity flags changed from `22` to `0`.
- Residual reduced from `435,077` to `300,497` text-like pixels.
- Remaining residual is mostly thin table text edges, status badges, and ruling lines in a dense compliance memo; no broad whole-page offset remains after v468.
- Cover audit: `cover_audit_business_meeting020_v468/11_meeting_memo_020_Compliance_Review_Meeting_EN_cover.jpg`.

## 20260606_business_meeting_memo014_manual_v469

Scope:

- `04_business/04_meeting_memo/meeting_memo_014_Board_Audit_Committee_EN`

What changed:

- Rebuilt all 39 bboxes from explicit DOM selectors/text ranges for the long Board Audit Committee memo.
- Corrected the page-height mismatch on this overflowing full-page screenshot; lower sections now use the actual full screenshot y scale rather than the fixed A4 page height.
- Re-aligned the header/banner/title blocks (#0-#2), meeting metadata (#3), all section headers (#4, #7, #9, #16, #18, #20, #23, #25, #31, #33), dense tables (#5, #8, #17, #19, #32), risk cards (#10-#15), auditor update card (#21-#22), hotline summary (#24), resolutions (#26-#30), next meeting (#34), signatures (#35-#36), and footer lines (#37-#38).

GT annotation change:

- Added GT annotations: 0.
- Removed GT annotations: 0.

Verification:

- Case counts remain `39/39 boxed, 0 no-bbox`.
- Low-similarity flags remain `0`.
- Residual reduced from `424,449` to `256,685` text-like pixels.
- Remaining residual is dominated by dark table/risk-card header backgrounds, horizontal rules, and thin text edges, not broad body-text exposure or whole-page offset.
- Cover audit: `cover_audit_business_meeting014_v469/11_meeting_memo_014_Board_Audit_Committee_EN_cover.jpg`.

## 20260606_business_meeting_memo017_unboxed_v470

Scope:

- `04_business/04_meeting_memo/meeting_memo_017_薪酬绩效委员会纪要`

What changed:

- Filled the only previously missing existing GT bbox:
  - #2 `薪酬与绩效考核委员会会议纪要`
- The bbox was generated from a DOM text Range and checked against the cover audit; existing bboxes in the case were left unchanged.

GT annotation change:

- Added GT annotations: 0.
- Removed GT annotations: 0.

Verification:

- Case counts changed from `89/90 boxed, 1 no-bbox` to `90/90 boxed, 0 no-bbox, 0 low-similarity`.
- Residual remains `32,176` text-like pixels because the prior residual was mostly tiny footer/signature/table-line remnants rather than this missing title.
- Cover audit: `cover_audit_business_meeting017_v470/11_meeting_memo_017_薪酬绩效委员会纪要_cover.jpg`.

## 20260606_legal_business_license001_top_scope_v472

Scope:

- `03_legal_gov/04_license_permit/business_license_001_营业执照`

What changed:

- Corrected three visibly misaligned existing GT bboxes:
  - #0 `营业执照`: widened/shifted to cover the full title text `营 业 执 照`.
  - #5 `住所：北京市朝阳区亚运村路1号亚运大厦18层`: shifted up/left to include the `住所：` label and value together.
  - #11 `经营范围：...`: expanded from a tiny label-only box to the full visible business-scope paragraph.
- The #11 visible HTML text differs from the stored GT text in several phrases; the repair keeps the source GT text unchanged and aligns the bbox to the corresponding visible `经营范围` block.

GT annotation change:

- Added GT annotations: 0.
- Removed GT annotations: 0.

Verification:

- Case counts remain `16/16 boxed, 0 no-bbox`.
- Low-similarity flags changed from `1` to `0`.
- Residual reduced from `238,052` to `27,038` text-like pixels.
- Remaining residual is the QR code, not exposed body text.
- Cover audit: `cover_audit_legal_business_license001_v472/11_business_license_001_营业执照_cover.jpg`.

## 20260606_legal_license006_driving_multi_v477

Scope:

- `03_legal_gov/04_license_permit/license_permit_006_Driving_License_Multi`

What changed:

- Corrected visibly misaligned existing GT bboxes on the multi-country driving-licence comparison page:
  - #0 `DRIVING LICENCE COMPARISON`: moved from the lower half of the title to the full headline.
  - #1 `中国驾照 / International Driving Permit / 日本免許証 / EU-Führerschein`: moved up to the visible subtitle line.
  - #2 `中华人民共和国机动车驾驶证`: moved up/widened to the full Chinese licence title.
  - #3 `DRIVING LICENSE OF THE PEOPLE'S REPUBLIC OF CHINA`: tightened to the English title line.
  - #5 `INTERNATIONAL DRIVING PERMIT`: moved up/widened to the full IDP title.
  - #6 `PERMIS INTERNATIONAL DE CONDUIRE`: moved up/widened to the French title line.
  - #7 `Convention on Road Traffic of 8 November 1968 (Vienna)`: moved up/widened to the subtitle line.
  - #8 IDP issued-by row: moved up to include the issuer/header text instead of only the line below it.
  - #9 IDP personal fields: widened to cover right-side values/restriction text.
  - #14 `優良 | ゴールド免許 | IC chip embedded`: widened and lowered to cover the full visible badge text.
  - #15 `BUNDESREPUBLIK DEUTSCHLAND`: expanded to the EU flag/header bar.
  - #16 `EU DRIVING LICENCE / FÜHRERSCHEIN`: widened to cover the full title text.
  - #17 EU personal fields: tightened from an over-broad card area to the visible field block and widened for right-side values.
- Large page/card title bboxes were pixel-measured because Chromium text Range boxes were consistently too low for this HTML.

GT annotation change:

- Added GT annotations: 0.
- Removed GT annotations: 0.

Verification:

- Case counts remain `21/21 boxed, 0 no-bbox`.
- Low-similarity flags remain `0`.
- Residual reduced from `228,993` to `28,154` text-like pixels.
- Remaining residual is dominated by card borders/ruling lines, EU table dashes, and decorative licence styling rather than exposed body text.
- Cover audit: `cover_audit_legal_license006_v477/11_license_permit_006_Driving_License_Multi_cover.jpg`.

## 20260606_legal_gov_low_sim_batch_v483

Scope:

- `03_legal_gov/05_legislation/legislation_020_民法典继承可视化图谱`
- `03_legal_gov/01_gov_document/gov_document_023_UK_Parliamentary_Act`
- `03_legal_gov/03_notarial_document/notarial_document_014_US_Promissory_Note`
- `03_legal_gov/06_accident_report/accident_report_007_UK_HSE_RIDDOR`
- `03_legal_gov/05_legislation/legislation_016_SEC_Exemption_Flowchart`
- `03_legal_gov/04_license_permit/license_permit_007_药品GSP许可册`
- `03_legal_gov/05_legislation/legislation_027_EU_AI_Act_Pyramid`
- `03_legal_gov/01_gov_document/gov_document_014_应急部令_突发事件分级`
- `03_legal_gov/01_gov_document/gov_document_002_国务院批复`
- `03_legal_gov/05_legislation/legislation_017_Ontario_ESA_Workplace_Poster`
- `03_legal_gov/04_license_permit/license_permit_017_PE_License_Portal`
- `03_legal_gov/06_accident_report/accident_report_018_UK_EA_Pollution_Incident`
- `03_legal_gov/06_accident_report/accident_report_020_SafeWork_NSW_Investigation`

What changed:

- Corrected existing low-sim or high-residual boxes only; no GT instances were added or removed.
- Expanded figure-level annotations to full visual blocks where the GT text describes a diagram:
  - `legislation_020` #6 family inheritance tree.
  - `legislation_016` #9 SEC exemption decision tree.
  - `legislation_027` #7 EU AI Act risk pyramid.
  - `license_permit_007` #15 GSP warehouse layout.
  - `license_permit_017` #10 US map.
  - `accident_report_018` #14 river spill schematic.
  - `accident_report_020` #15 Ishikawa fishbone diagram.
- Corrected dense text/table blocks:
  - `gov_document_023` #24 Board composition clauses.
  - `notarial_document_014` #11 Events of Default block.
  - `gov_document_014` #11 four emergency-response levels.
  - `gov_document_002` #23 copy/footer block.
  - `legislation_017` #19 statutory notice of termination block.
- Rebuilt `accident_report_007_UK_HSE_RIDDOR` #0-#24 from clean-image coordinates after cover audit showed a cropped-image/DOM vertical offset. The repair aligned the HSE header, ref bar, Part A/B/C form grids, injury/history/corrective-action tables, notes, signatures, and footer. RIDDOR residual dropped to `40,956` text-like pixels; remaining residue is mostly ruling lines/decorative strokes.

GT annotation change:

- Added GT annotations: 0.
- Removed GT annotations: 0.

Verification:

- RIDDOR cover audit: `cover_audit_legal_v483_riddor/11_accident_report_007_UK_HSE_RIDDOR_cover.jpg`.
- Earlier spot covers for the figure/text repairs:
  - `cover_audit_legal_v478_leg020/11_legislation_020_民法典继承可视化图谱_cover.jpg`
  - `cover_audit_legal_v478_gov023/11_gov_document_023_UK_Parliamentary_Act_cover.jpg`

## 20260606_legal_gov_remaining_low_v486

Scope:

- `03_legal_gov/01_gov_document/gov_document_018_Executive_Order_EN`
- `03_legal_gov/01_gov_document/gov_document_019_Federal_Register_Notice_EN`
- `03_legal_gov/01_gov_document/gov_document_021_中英双语政府公告`
- `03_legal_gov/03_notarial_document/notarial_document_003_遗嘱公证书`
- `03_legal_gov/04_license_permit/license_permit_012_特种设备金属铭牌`
- `03_legal_gov/06_accident_report/accident_report_016_US_Police_Traffic_Report`

What changed:

- Cleared visually verified low-sim flags while preserving already-correct boxes:
  - `gov_document_018` #10 Definitions list.
  - `gov_document_019` #18 threshold-parameter paragraph/list and #27 public-comments paragraph/list.
  - `notarial_document_003` #26 signature block.
  - `license_permit_012` #9 maintenance Gantt table.
  - `accident_report_016` #4 collision details table, #6 Vehicle 1 table, and #8 Vehicle 2 table.
- Corrected `gov_document_021_中英双语政府公告` visible bilingual-column issues:
  - #4 Chinese Innovation and Technology block expanded down to include the final `设立AI监管沙盒...先行先试。` line.
  - #6 Chinese Land and Housing intro moved up to the two visible lines before the table.
  - #17 English Innovation and Technology block tightened from an over-long right-column box to the actual first English section.
  - #18/#19 English Land and Housing title/intro moved back into the right column.
  - #22/#24/#26 English right-column paragraphs moved from cross-page boxes back to their true right-column text blocks.

GT annotation change:

- Added GT annotations: 0.
- Removed GT annotations: 0.

Verification:

- `03_legal_gov` now has `151` cases / `3672` annotations with `0 no-bbox` and `0 low-similarity`.
- `gov_document_021` residual dropped from `15,500` to `0` text-like pixels after the v486 refinements.
- Final `gov_document_021` cover audit: `cover_audit_legal_v486_gov021/11_gov_document_021_中英双语政府公告_cover.jpg`.

## 20260606_business_residual_accept_v487

Scope:

- `04_business` accepted residual-cover bbox expansions from a dry-run candidate set.

What changed:

- Accepted only candidate bbox expansions that improved residual coverage on the released clean PNG.
- Updated 86 business cases / 1105 existing annotations.
- Excluded two candidate cases that worsened residual:
  - `04_business/04_meeting_memo/meeting_memo_011_安全生产专题会纪要`
  - `04_business/06_business_plan/business_plan_021_DeepCurrent_Energy`

GT annotation change:

- Added GT annotations: 0.
- Removed GT annotations: 0.

Verification:

- Before audit: `/tmp/pdb_04_business_residual_v486.json`, `23,327,318` text-like pixels / `6103` components.
- After audit: `/tmp/pdb_04_business_residual_v487.json`, `21,189,414` text-like pixels / `5393` components.
- Debug residuals: `cover_residual_04_business_v487`.

## 20260607_targeted_legal_publishing_v489

Scope:

- `03_legal_gov/05_legislation/legislation_019_WIPO_PLT_Dashboard`
- `03_legal_gov/05_legislation/legislation_021_人大表决结果公告`
- `07_publishing/05_catalog_directory/catalog_directory_009_企业黄页`

What changed:

- `legislation_019_WIPO_PLT_Dashboard`
  - #0 `World Intellectual Property Organization`: expanded from a 13 px horizontal band to the full top title.
  - #1 subtitle: expanded from a 13 px horizontal band to the full subtitle line.
  - #2 UN agency badge text: expanded from a 13 px horizontal band to the full badge text.
  - #11/#13/#15/#17 Article titles: moved down/expanded to cover the visible article number + title text.
  - #19 `Treaty Adoption Timeline`: widened and moved down to the visible section title.
  - #21 `Selected Contracting Parties`: widened and moved down to the visible section title.
  - #23 footer: moved from a large white-block area above the footer to the actual blue-footer text lines.
- `legislation_021_人大表决结果公告`
  - Rebuilt all 20 existing bboxes from clean-image coordinates.
  - Kept #10/#12 as whole-table bboxes.
  - Kept #15/#18 as full signing blocks including the visible seal areas; #16/#17 cover their corresponding signing text blocks.
  - Fixed #19 footer from the bottom page margin back to the actual footer line.
- `catalog_directory_009_企业黄页`
  - Rebuilt all 8 existing bboxes from clean-image coordinates.
  - Kept #2/#3 as the two original directory table blocks.
  - Moved #4/#5/#6 from the lower blank area to the right-column advertisement title/body/phone.
  - Moved #7 footer from the lower blank area to the actual footer note.
  - Did not add the pinyin index or black `H` block because they are not present as original GT instances.

GT annotation change:

- Added GT annotations: 0.
- Removed GT annotations: 0.

Verification:

- `legislation_019_WIPO_PLT_Dashboard`: residual improved from `82,100` to `41,601` text-like pixels.
- `legislation_021_人大表决结果公告`: residual improved from `245,465` to `42,768` text-like pixels.
- `catalog_directory_009_企业黄页`: residual improved from `331,575` to `31,225` text-like pixels.
- Final cover audits:
  - `cover_audit_targeted_v489/11_legislation_019_WIPO_PLT_Dashboard_cover.jpg`
  - `cover_audit_targeted_v488/11_legislation_021_人大表决结果公告_cover.jpg`
  - `cover_audit_targeted_v488/11_catalog_directory_009_企业黄页_cover.jpg`

## 20260607_publishing_catalog_targeted_v492

Scope:

- `07_publishing/05_catalog_directory/catalog_directory_007_Course_Catalog`
- `07_publishing/05_catalog_directory/catalog_directory_008_Product_Catalog_EN`
- `07_publishing/05_catalog_directory/catalog_directory_010_展会参展商名录`

What changed:

- `catalog_directory_007_Course_Catalog`
  - Rebuilt all 11 existing bboxes from clean-PNG coordinates after review showed #10 footer sitting in the lower blank page area.
  - Kept #4/#6/#8 as whole course-table grid bboxes.
  - Moved #9 note and #10 footer back to the visible note/footer lines; expanded #2 Academic Year so no right-edge text remains exposed.
- `catalog_directory_008_Product_Catalog_EN`
  - Rebuilt all 11 existing bboxes from clean-PNG coordinates after the lower order form/footer had the same vertical-offset pattern.
  - Split #0 company title and #1 subtitle into separate boxes instead of the previous overlapping bbox.
  - Kept #4/#6 product tables and #8 order-form table as whole grid bboxes; moved #9 terms and #10 footer to their visible lines.
- `catalog_directory_010_展会参展商名录`
  - Rebuilt all 16 existing bboxes from clean-PNG coordinates.
  - Kept #4 as the whole exhibitor table.
  - Moved #5 Hall Layout title, #6-#13 hall labels, #14 entrance, and #15 organizer footer from the lower shifted positions back to the visible hall-map/footer area.

GT annotation change:

- Added GT annotations: 0.
- Removed GT annotations: 0.

Verification:

- `catalog_directory_007_Course_Catalog`: residual improved from `357,443` to `12,651` text-like pixels.
- `catalog_directory_008_Product_Catalog_EN`: residual improved from `305,836` to `5,670` text-like pixels.
- `catalog_directory_010_展会参展商名录`: residual improved from `111,803` to `270` text-like pixels.
- Final cover audits:
  - `cover_audit_catalog007_v492/11_catalog_directory_007_Course_Catalog_cover.jpg`
  - `cover_audit_catalog008_v492/11_catalog_directory_008_Product_Catalog_EN_cover.jpg`
  - `cover_audit_catalog010_v492/11_catalog_directory_010_展会参展商名录_cover.jpg`

## 20260607_publishing_followup_v493_to_v497

Scope:

- Follow-up pass over `07_publishing` after front-end review showed remaining visible offsets/edge leakage in newspaper, magazine, book, brochure/menu, and catalog/directory pages.

What changed:

- `07_publishing/05_catalog_directory/catalog_directory_003_图书出版目录`
  - Rebuilt all 43 existing bboxes from DOM/clean-image coordinates.
  - Later accepted 8 residual-cover expansions to reduce exposed product/detail text edges.
  - Did not add decorative cover placeholders or image-internal duplicate labels as new GT instances.
- `07_publishing/05_catalog_directory/catalog_directory_004_Wine_Catalog`
  - Rebuilt all 50 existing bboxes from DOM/clean-image coordinates.
  - Later accepted 13 residual-cover expansions around wine card details/table/footer text.
  - Kept wine label placeholders as image/decorative content, not new text GT.
- `07_publishing/03_book/book_014_History_Book_EN`
  - Repaired all 29 existing bboxes after selector-only v494 left lower-page vertical drift.
  - Final hybrid v496 keeps the sidebar date items split correctly and restores lower headings/paragraphs/table/footnotes to full block coverage.
  - Accepted 5 small residual-cover expansions after v496; final residual `13,778 -> 12,991`.
- `07_publishing/04_brochure_menu/brochure_menu_003_旅游景点宣传折页`
  - Rebuilt all 39 existing bboxes with selector-based DOM coordinates.
  - Accepted 15 residual-cover expansions around title/body/transport/contact text; residual `610,883 -> 440,734`.
- `07_publishing/04_brochure_menu/brochure_menu_004_Real_Estate_Brochure`
  - Rebuilt all 38 existing bboxes with selector-based DOM coordinates.
  - No residual-cover expansion was accepted afterward; v494 selector repair is the current state.

Residual-cover expansion batch:

- Accepted only evaluated OCR residual-cover expansions that did not worsen residual coverage on the clean PNG.
- Accepted cases: 76.
- Accepted existing-bbox expansions: 2103.
- Rejected case: `07_publishing/01_newspaper/newspaper_004_环球时报` because the candidate worsened residual `49,775 -> 55,139`.
- Per-case accepted expansion counts:
  - `newspaper_001_财经日报头版`: 34
  - `newspaper_002_Financial_Times_EN`: 64
  - `newspaper_003_经济导报`: 83
  - `newspaper_005_Tech_Weekly_EN`: 99
  - `newspaper_006_科技商报`: 41
  - `newspaper_007_The_Guardian_EN`: 49
  - `newspaper_008_China_Daily_EN`: 69
  - `newspaper_009_南方周末`: 70
  - `newspaper_010_体育版面`: 89
  - `newspaper_011_Financial_Chronicle`: 119
  - `newspaper_012_NYT_FrontPage_EN`: 156
  - `newspaper_013_都市晚报`: 57
  - `newspaper_014_Guardian_Sports_EN`: 79
  - `newspaper_015_中国经济日报`: 92
  - `newspaper_016_人民日报_政治版`: 86
  - `newspaper_017_体育周报`: 47
  - `newspaper_018_Washington_Post_EN`: 179
  - `newspaper_019_Global_Tribune`: 108
  - `newspaper_020_文化副刊`: 58
  - `magazine_001_人工智能专题`: 7
  - `magazine_002_科技杂志_Feature`: 9
  - `magazine_003_财经杂志_数据报道`: 4
  - `magazine_004_学术期刊目录页`: 7
  - `magazine_005_生活周刊`: 3
  - `magazine_006_科技杂志`: 5
  - `magazine_008_National_Geographic`: 6
  - `magazine_009_美食天地`: 2
  - `magazine_010_学术期刊目录页`: 13
  - `magazine_011_医学期刊_论文页`: 3
  - `magazine_012_Sports_Illustrated_EN`: 8
  - `magazine_013_建筑设计杂志`: 4
  - `magazine_014_The_Economist_EN`: 4
  - `magazine_016_Scientific_American_EN`: 6
  - `magazine_018_Wired_Tech_EN`: 1
  - `magazine_019_读者文摘`: 15
  - `magazine_020_Rolling_Stone_Music_EN`: 6
  - `book_001_计算机网络_传输层协议`: 11
  - `book_003_Popular_Science_EN`: 9
  - `book_011_医学教材_内科学`: 8
  - `book_012_目录页`: 28
  - `book_013_诗歌集`: 2
  - `book_014_History_Book_EN`: 5
  - `book_016_Cookbook_EN`: 12
  - `book_017_数学定理证明`: 5
  - `book_018_Travel_Guide_EN`: 8
  - `book_019_哲学著作`: 21
  - `brochure_menu_002_Coffee_Shop_Menu`: 6
  - `brochure_menu_003_旅游景点宣传折页`: 15
  - `brochure_menu_005_健身房会员宣传页`: 9
  - `brochure_menu_006_中餐厅菜单`: 8
  - `brochure_menu_008_旅游三折页`: 5
  - `brochure_menu_009_Restaurant_Menu_EN`: 9
  - `brochure_menu_010_咖啡馆菜单`: 16
  - `brochure_menu_011_法式米其林套餐`: 8
  - `brochure_menu_012_新中式创意料理`: 9
  - `brochure_menu_013_Italian_Fine_Dining`: 2
  - `brochure_menu_015_顶级牛排馆`: 15
  - `brochure_menu_017_粤式经典`: 8
  - `brochure_menu_018_Wine_Pairing_Menu`: 7
  - `brochure_menu_019_甜品品鉴`: 9
  - `brochure_menu_020_主厨品鉴套餐`: 4
  - `catalog_directory_001_电子元器件目录`: 12
  - `catalog_directory_002_Industrial_Tools_Catalog`: 8
  - `catalog_directory_003_图书出版目录`: 8
  - `catalog_directory_004_Wine_Catalog`: 13
  - `catalog_directory_005_办公家具产品目录`: 29
  - `catalog_directory_006_医疗器械目录`: 10
  - `catalog_directory_007_Course_Catalog`: 2
  - `catalog_directory_009_企业黄页`: 5
  - `catalog_directory_010_展会参展商名录`: 5
  - `catalog_directory_013_中药材鉴定图录`: 17
  - `catalog_directory_015_建筑材料产品手册`: 2
  - `catalog_directory_016_Scientific_Equipment`: 32
  - `catalog_directory_017_古董拍卖图录`: 26
  - `catalog_directory_018_Software_License_Directory`: 11
  - `catalog_directory_020_高端音响器材目录`: 2

GT annotation change:

- Added GT annotations: 0.
- Removed GT annotations: 0.
- All v497 accepted changes are expansions of existing bboxes only.

Verification:

- `07_publishing` residual audit before v497: `21,296,155` text-like pixels / `5,512` components.
- `07_publishing` residual audit after v497: `15,483,511` text-like pixels / `3,195` components.
- Token written to `review_data.json`, `review_data.js`, and `index.html`: `20260607_publishing_residual_expand_v497`.
- Final audit reports:
  - `/tmp/pdb_07_publishing_residual_v497.json`
  - `/tmp/pdb_07_publishing_residual_expand_apply_v497.json`
- Representative cover checks:
  - `/tmp/pdb_review_publishing_v497_cover_samples/11_newspaper_003_经济导报_cover.jpg`
  - `/tmp/pdb_review_publishing_v497_cover_samples/12_newspaper_016_人民日报_政治版_cover.jpg`
  - `/tmp/pdb_review_publishing_v497_cover_samples/14_magazine_006_科技杂志_cover.jpg`
  - `/tmp/pdb_review_publishing_v497_cover_samples/16_catalog_directory_007_Course_Catalog_cover.jpg`
  - `cover_audit_book014_v496_rerender/11_book_014_History_Book_EN_cover.jpg`

## 20260607_publishing_nonvisible_and_book011_v498_v499

Scope:

- Continued `07_publishing` full-category review after v497 residual expansion.
- Goal: remove confirmed non-visible GT noise, keep `07_publishing` at 0 no-bbox / 0 low-sim, and fix a high-residual book page with clearly missing visible text.

Token sequence:

- v498: `20260607_publishing_remove_nonvisible_v498`
- v499: `20260607_publishing_book011_complete_v499`

Case-level changes:

- `07_publishing/04_brochure_menu/brochure_menu_005_健身房会员宣传页`
  - Removed 14 source GT entries that are below the released clean PNG crop and are not visible foreground content.
  - Removed old annotation IDs: `22` through `35`.
  - Removed texts: `限时`, `新会员专享`, `¥99/首月`, `仅限首次办卡新会员含全部器械区使用权赠送InBody体测1次`, `热门`, `闺蜜/兄弟卡`, `8折`, `两人同时办理季卡/年卡享受8折优惠各赠私教体验课2节`, `超值`, `年卡+私教套餐`, `¥5,888`, `年卡 + 24节私教课原价 ¥8,088 立省 ¥2,200另赠运动背包一个`, activity-period text, and the store-address/footer text.
  - Count changed from `36 items / 14 no bbox` to `22 items / 0 no bbox`.

- `07_publishing/05_catalog_directory/catalog_directory_019_有机食品产品目录`
  - Removed 1 source GT entry that was an HTML/CSS style blob, not visible page content.
  - Removed old annotation ID: `42`.
  - Visible footer annotation remains and was reindexed after removal.
  - Count changed from `44 items / 1 no bbox` to `43 items / 0 no bbox`.

- `07_publishing/03_book/book_011_医学教材_内科学`
  - Realigned 20 existing annotations to clean PNG/DOM pixel coordinates.
  - Fixed the large shifted mechanism paragraph, flow-chart text block, NYHA/diagnosis blocks, drug-section headings, references, and page number.
  - Added 6 missing visible `text_block` annotations that were absent from the release GT:
    - margin-note body: `心力衰竭是各种心脏疾病的终末阶段...`
    - key-point body: `2023年指南将HFrEF的基石治疗更新为"新四联"...`
    - ARNI card body
    - β-blocker card body
    - MRA card body
    - SGLT2 inhibitor card body
  - Count changed from `21 items / 21 boxed` to `27 items / 27 boxed`.
  - Case residual improved from `668,049` text-like pixels / `97` components to `44,074` / `13`.

Category-level status after v499:

- `07_publishing`: `5034/5034 boxed`, `0 no bbox`, `0 low_similarity`.
- Added GT annotations in this v498-v499 pass: `6`.
- Removed GT annotations in this v498-v499 pass: `15`.
- Current token written to `review_data.json`, `review_data.js`, and `index.html`: `20260607_publishing_book011_complete_v499`.

Verification:

- v498 removal report: `/tmp/pdb_07_publishing_nonvisible_removed_v498.json`
- v499 book repair report: `/tmp/pdb_publishing_book011_v499.json`
- `book_011` residual report: `/tmp/pdb_book011_residual_v499.json`
- Full `07_publishing` residual report after v499: `/tmp/pdb_07_publishing_residual_v499.json`
- Full `07_publishing` residual changed from v498 `15,483,511` text-like pixels / `3,195` components to v499 `14,859,536` / `3,111`.
- Representative cover checks:
  - `cover_audit_book011_v499/11_book_011_医学教材_内科学_cover.jpg`
  - `cover_residual_book011_v499/001_book_011_医学教材_内科学_residual.jpg`
  - `cover_audit_publishing_v498_manual_targets/15_catalog_directory_007_Course_Catalog_cover.jpg`

Notes:

- `catalog_directory_007_Course_Catalog` was rechecked after the user's screenshot. In the current data token, annotation `#10` is on the white footer line, not in the gray blank area below the page. If the browser still shows the old gray-area placement, it is stale frontend/localStorage cache rather than current `review_data.json`.
- Remaining high residual cases such as `catalog_directory_003`, `catalog_directory_004`, and some book/brochure pages include a mixture of decorative colored blocks, image-placeholder text, and further possible visible-text gaps. They should be handled with case-level review rather than a blind full DOM rebuild, because full DOM rebuild dry-run made newspaper pages substantially worse.

## 20260607_publishing_books_v500_v501

Scope:

- Continued high-residual `07_publishing/03_book` review after v499.
- Fixed two book pages where residual showed real text block offset, not just decoration.

Token sequence:

- v500: `20260607_publishing_book010_tighten_v500`
- v501: `20260607_publishing_book001_complete_v501`

Case-level changes:

- `07_publishing/03_book/book_010_童话故事`
  - Repositioned 5 existing annotations: `#3` star separator, `#4` mixed Chinese/German paragraph, `#5` mixed Chinese/German paragraph, `#6` final paragraph, `#7` page number.
  - No GT annotations added or removed.
  - Count remains `8/8 boxed`, `0 no bbox`.
  - Residual improved from `653,599` text-like pixels / `108` components to `567,225` / `96`; remaining residual is mostly the colorful border and illustration/decorative content.

- `07_publishing/03_book/book_001_计算机网络_传输层协议`
  - Realigned 22 existing annotations using clean DOM/image coordinates.
  - Fixed compressed or shifted paragraph boxes, the equation block, figure caption, table, code block, exercises, footnotes, and page number.
  - Added 2 missing visible annotations:
    - `text_block`: right-side `历史注记` body.
    - `figure`: TCP Reno congestion-window line chart.
  - Count changed from `23 items / 23 boxed` to `25 items / 25 boxed`.
  - Residual improved from `594,508` text-like pixels / `122` components to `48,338` / `7`.

GT annotation change:

- Added GT annotations in this v500-v501 pass: `2`.
- Removed GT annotations in this v500-v501 pass: `0`.

Verification:

- v500 report: `/tmp/pdb_publishing_book010_v500.json`
- v501 report: `/tmp/pdb_publishing_book001_v501.json`
- `book_010` residual report: `/tmp/pdb_book010_residual_v500.json`
- `book_001` residual report: `/tmp/pdb_book001_residual_v501.json`
- Full `07_publishing` residual report after v501: `/tmp/pdb_07_publishing_residual_v501.json`
- Full `07_publishing` residual after v501: `14,226,992` text-like pixels / `2,984` components.
- `07_publishing` status after v501: `5036/5036 boxed`, `0 no bbox`, `0 low_similarity`.
- Representative cover checks:
  - `cover_audit_book010_v500/11_book_010_童话故事_cover.jpg`
  - `cover_audit_book001_v501/11_book_001_计算机网络_传输层协议_cover.jpg`

## 20260607_publishing_cache_and_dom_gated_v502_v503

Scope:

- Rechecked `07_publishing` after the user still saw obvious publishing offsets in the front-end, especially `catalog_directory_007_Course_Catalog`.
- Investigated whether the issue was stale front-end/localStorage state versus current `review_data.json`.
- Ran DOM-gated dry-runs over publishing to test whether a batch DOM rebuild could be safely applied.

Token sequence:

- v502 attempted: `20260607_publishing_catalog003_dom_gated_v502`
- v503 current: `20260607_publishing_cache_bump_catalog003_revert_v503`

Findings:

- `catalog_directory_007_Course_Catalog` current data is not in the gray blank region shown in the user's screenshot:
  - Current `#10` bbox is `[495, 2875, 2050, 2922]`, on the white footer text line.
  - Current residual is `6,549` text-like pixels / `2` components.
  - Cover check: `cover_audit_publishing_v502_check/12_catalog_directory_007_Course_Catalog_cover.jpg`
- The review app uses `localStorage` edits keyed by `DATA.meta.created_at`; a browser tab with old same-token manual bbox edits can display stale boxes even after `review_data.json` is corrected. v503 bumps the token so those local bbox edits no longer override the dataset after refresh.
- Full DOM rebuild is unsafe for `07_publishing`:
  - Newspaper dry-run made the first 10 newspaper cases substantially worse; examples include `newspaper_001` residual `49,624 -> 2,307,463` and `newspaper_004` `49,775 -> 2,817,499`.
  - Magazine dry-run rejected all 20 cases; examples include `magazine_006` `38,596 -> 476,478` and `magazine_010` `408,187 -> 644,380`.
  - Book and brochure/menu dry-runs were also mostly rejected. Many HTML containers are larger or structured differently from the intended GT instances.
  - Catalog dry-run accepted only `catalog_directory_003` numerically, but visual cover inspection showed the candidate shifted title/book-cover labels, so the change was reverted.

Case-level action:

- `07_publishing/05_catalog_directory/catalog_directory_003_图书出版目录`
  - v502 DOM-gated candidate temporarily changed existing bboxes and reduced residual numerically from `1,494,138` to `782,290`, but visual review showed obvious misalignment of title and book-cover labels.
  - v503 reverted this case back to the previous v501 boxes from `review_data.before_20260607_publishing_catalog003_dom_gated_v502.json`.
  - No GT annotations were added or removed.

Verification:

- Current token written to `review_data.json`, `review_data.js`, and `index.html`: `20260607_publishing_cache_bump_catalog003_revert_v503`.
- v502 dry-run reports:
  - `/tmp/pdb_07_publishing_dom_gated_dry_v502.json`
  - `/tmp/pdb_07_publishing_dom_gated_no_newspaper_dry_v502.json`
- v503 revert report: `/tmp/pdb_publishing_catalog003_revert_v503.json`
- Full `07_publishing` residual report after v503: `/tmp/pdb_07_publishing_residual_v503.json`
- Full `07_publishing` residual after v503: `14,226,992` text-like pixels / `2,984` components.
- `07_publishing` status after v503: `5036/5036 boxed`, `0 no bbox`, `0 low_similarity`.

Operational note for future 07 fixes:

- Do not use broad DOM rebuild for publishing. Use case-level visual repair, and accept residual-cover changes only after looking at the rendered cover image.
- For user reports where the current rendered cover is correct but the browser still shows old offsets, first check whether localStorage/manual edits are overriding the current token; bumping the data token or using the app's `Clear local edits` button resolves that class of front-end-only drift.
- Dark-background catalog pages can fool the residual audit into reporting `0` text-like residual even when the boxes are visibly wrong. In those cases, rely on direct cover rendering and visual review rather than residual score alone.

## 20260607_publishing_catalog020_v504_v505

Scope:

- Fixed `07_publishing/05_catalog_directory/catalog_directory_020_高端音响器材目录`, reported by the user as visibly shifted: most boxes were clustered near the upper-left while the actual dark catalog content was centered/full-width.

Token sequence:

- v504: `20260607_publishing_catalog020_dom_v504`
- v505 current: `20260607_publishing_catalog020_brand_en_v505`

Case-level changes:

- `07_publishing/05_catalog_directory/catalog_directory_020_高端音响器材目录`
  - Rebuilt all 64 existing annotation bboxes from the HTML DOM against the clean PNG.
  - Root cause: the previous boxes mixed CSS-page coordinates and clean-PNG coordinates; the page is a dark-background catalog, so the residual audit had reported `0` text-like residual and missed the visible misalignment.
  - After DOM rebuild, one repeated brand string was misassigned:
    - `#1` `S O U N D A R T` was matched to the footer `SOUNDART` line.
    - v505 manually reset `#1` from `[1001, 15941, 1480, 16003]` to `[930, 620, 1535, 670]`, based on top-header pixel bounds.
  - Footer brand `#58` remains `[113, 15938, 2368, 16012]`.
  - No GT annotations were added or removed.
  - Count remains `64/64 boxed`, `0 no bbox`, `0 low_similarity`.

Verification:

- DOM rebuild report: `/tmp/pdb_catalog020_dom_v504.json`
- Manual brand-line fix report: `/tmp/pdb_catalog020_brand_en_v505.json`
- Final cover check:
  - `cover_audit_catalog020_v505/11_catalog_directory_020_高端音响器材目录_cover.jpg`
- Current token written to `review_data.json`, `review_data.js`, and `index.html`: `20260607_publishing_catalog020_brand_en_v505`.
- `07_publishing` status after v505: `5036/5036 boxed`, `0 no bbox`, `0 low_similarity`.

## 20260607_logistics_dimension_and_shipping001_v506_v509

Scope:

- Began repairing `09_logistics`, starting from `09_logistics/01_shipping_label`.
- User reported severe visible offsets in the review UI for shipping labels.

Token sequence:

- v506: `20260607_logistics_dimension_sync_v506`
- v507: `20260607_logistics_shipping001_uniform_dom_v507`
- v508: `20260607_logistics_shipping001_domrect_v508`
- v509 current: `20260607_logistics_shipping001_space_match_v509`

Root causes found:

- All `09_logistics` cases had stale review `width` / `height` values that did not match the actual clean PNG dimensions. Example: `shipping_label_001` was recorded as `1600x1500`, while the PNG is `2481x3509`.
- Logistics PNGs often include extra blank canvas below the rendered HTML. Bbox reconstruction must use uniform render scale from page width (`scale_y = scale_x`), not `image_height / DOM_body_height`.
- For shipping labels, strong foreground snapping can jump from a correct DOM text rect to nearby black route bands, borders, QR/barcode strokes, or horizontal rules. Use DOM/text-node rects with light padding instead.
- Spaced and unspaced tracking codes can normalize to the same compact text; preserve visible whitespace for matching so `SF 1026 3847 5612 0` does not swap with `SF1026384756120`.

Case-level changes:

- `09_logistics`
  - Synchronized `width` / `height` for all 120 logistics cases to their actual clean PNG dimensions.
  - No GT annotations were added or removed in this dimension sync.

- `09_logistics/01_shipping_label/shipping_label_001_顺丰速运_SF_Express_-_Complex_Multi-Section_Label`
  - Rebuilt all 78 existing annotation bboxes from HTML DOM/text-node rects using uniform x/y render scale.
  - Fixed severe visible offsets in the header, route bar, QR/barcode area, recipient/sender blocks, contents table, fee grid, status strip, and bottom declaration text.
  - Fixed the spaced/unspaced tracking-code swap:
    - `#10` `SF 1026 3847 5612 0`
    - `#11` `SF1026384756120`
  - No GT annotations were added or removed.
  - Count remains `78/78 boxed`, `0 no bbox`, `0 low_similarity`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.

Verification:

- Dimension sync report: `/tmp/pdb_logistics_dimension_sync_v506.json`
- 001 rebuild report: `/tmp/pdb_logistics001_space_match_v509.json`
- 001 residual report: `/tmp/pdb_logistics001_residual_v509.json`
- 001 final cover check:
  - `cover_audit_logistics001_v509/11_shipping_label_001_顺丰速运_SF_Express_-_Complex_Multi-Section_Label_cover.jpg`

## 20260607_logistics_shipping_label_batch_v510_v512

Scope:

- Continued `09_logistics/01_shipping_label` after establishing the v509 logistics repair method.

Token sequence:

- v510: `20260607_logistics_shipping_safe_domrect_v510`
- v511: `20260607_logistics_shipping010_preserve_domrect_v511`
- v512 current: `20260607_logistics_shipping_mixed_preserve_v512`

Case-level changes:

- Rebuilt all existing bboxes from DOM/text-node rects with uniform x/y scale for the following fully matched shipping-label cases:
  - `shipping_label_002_中国邮政_国际挂号包裹面单_China_Post_International_Registered_Parcel`: `74/74 boxed`, `0 no bbox`, `0 low_similarity`.
  - `shipping_label_003_菜鸟驿站_Cainiao_Station_-_Complex_Multi-Package_Notification`: `89/89 boxed`, `0 no bbox`, `0 low_similarity`.
  - `shipping_label_004_手写包裹卡_Handwritten_Parcel_Card_-_Complex`: `74/74 boxed`, `0 no bbox`, `0 low_similarity`.
  - `shipping_label_006_圆通速递_合并发货清单`: `273/273 boxed`, `0 no bbox`, `0 low_similarity`.
  - `shipping_label_009_菜鸟国际物流面单_-_CN2JP-SL009`: `180/180 boxed`, `0 no bbox`, `0 low_similarity`.
  - `shipping_label_011_EMS_国际特快专递_-_Radial_Layout`: `131/131 boxed`, `0 no bbox`, `0 low_similarity`.
  - `shipping_label_013_Hazmat_Shipping_Label_-_Vertical_Bands`: `267/267 boxed`, `0 no bbox`, `0 low_similarity`.
  - `shipping_label_014_德邦快递_Carbon_Copy_Waybill`: `106/106 boxed`, `0 no bbox`, `0 low_similarity`.
  - `shipping_label_015_Nautical_Chart_Shipping_Label`: `101/101 boxed`, `0 no bbox`, `0 low_similarity`.
  - `shipping_label_016_Cold_Chain_Shipment_Record_冷链运输记录`: `90/90 boxed`, `0 no bbox`, `0 low_similarity`.
  - `shipping_label_018_跨境电商集运总表_Cross-Border_Consolidation_Master_Sheet`: `500/500 boxed`, `0 no bbox`, `0 low_similarity`.
  - `shipping_label_020_综合物流调度面单_中式竖横混排`: `520/520 boxed`, `0 no bbox`, `0 low_similarity`.

- `shipping_label_010_CN_23_-_Customs_Declaration_Zollinhaltserklärung_Déclaration_en_douane`
  - Rebuilt 273 matched existing bboxes and preserved 1 old bbox that the DOM pass could not match.
  - Count is now `274/274 boxed`, `0 no bbox`, `1 low_similarity`.

- `shipping_label_012_Amazon_FBA_Warehouse_Blueprint_Label`
  - Rebuilt 26 matched bboxes and preserved the rest of the old bboxes.
  - Count remains `118/118 boxed`, `0 no bbox`; `37 low_similarity` remain for later fine repair.

- `shipping_label_017_国际多式联运货物运单_International_Multimodal_Transport_Consignment_Note`
  - Rebuilt 394 matched bboxes and preserved 14 old bboxes.
  - Count is now `408/408 boxed`, `0 no bbox`, `0 low_similarity`.

- `shipping_label_019_LOGISTICS_TODAY_物流纵横_Exhibition_Materials_Shipping_Plan`
  - Rebuilt 360 matched bboxes and preserved 42 old bboxes.
  - Count is now `402/402 boxed`, `0 no bbox`, `0 low_similarity`.

Cases held back for manual/special handling:

- `shipping_label_005_COSCO_SHIPPING_-_Bill_of_Lading`: still `154/219 boxed`, `65 no bbox`, `9 low_similarity`.
- `shipping_label_007_UPS_Worldwide_Express_Saver_-_Pharmaceutical_Cold_Chain_Waybill`: still `141/154 boxed`, `13 no bbox`, `58 low_similarity`.
- `shipping_label_008_Maersk_Line_-_Container_Shipping_Manifest_集装箱货运清单`: still `162/211 boxed`, `49 no bbox`, `13 low_similarity`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.

Verification:

- v510 report: `/tmp/pdb_logistics_shipping_safe_domrect_v510.json`
- v511 report: `/tmp/pdb_logistics010_preserve_domrect_v511.json`
- v512 report: `/tmp/pdb_logistics_shipping_mixed_preserve_v512.json`
- Representative cover checks:
  - `cover_audit_logistics_shipping_safe_v510/11_shipping_label_002_中国邮政_国际挂号包裹面单_China_Post_International_Registered_Parcel_cover.jpg`
  - `cover_audit_logistics_shipping_safe_v510/12_shipping_label_006_圆通速递_合并发货清单_cover.jpg`
  - `cover_audit_logistics_shipping_safe_v510/13_shipping_label_018_跨境电商集运总表_Cross-Border_Consolidation_Master_Sheet_cover.jpg`
  - `cover_audit_logistics_shipping_safe_v510/14_shipping_label_020_综合物流调度面单_中式竖横混排_cover.jpg`
  - `cover_audit_logistics010_v511/11_shipping_label_010_CN_23_-_Customs_Declaration_Zollinhaltserklärung_Déclaration_en_douane_cover.jpg`
  - `cover_audit_logistics_shipping_mixed_v512/12_shipping_label_017_国际多式联运货物运单_International_Multimodal_Transport_Consignment_Note_cover.jpg`
  - `cover_audit_logistics_shipping_mixed_v512/13_shipping_label_019_LOGISTICS_TODAY_物流纵横_Exhibition_Materials_Shipping_Plan_cover.jpg`

Status after v512:

- `09_logistics/01_shipping_label`: `4142/4269 boxed`, `127 no bbox`, `118 low_similarity`.
- Full `09_logistics`: `21280/21444 boxed`, `164 no bbox`, `2182 low_similarity`.

## 20260607_logistics_customs_packing_v513

Scope:

- Rebuilt `09_logistics/02_customs_packing` with the logistics-specific DOM/text-node rect method:
  - synchronized image dimensions already in place from v506;
  - used uniform image-width scale for x/y;
  - avoided foreground snapping to rules/barcodes;
  - preserved old bboxes where DOM matching was incomplete.

Token:

- v513: `20260607_logistics_customs_packing_domrect_v513`

Case-level changes:

- `customs_packing_001_Packing_List_-_HM-PL-2026-03842`: rebuilt `86/86`, `0 no bbox`, `0 low_similarity`.
- `customs_packing_002_Customs_Declaration_-_EXP-2026-SZ-DE-08841`: rebuilt `51/51`, `0 no bbox`, `0 low_similarity`.
- `customs_packing_003_Customs_Declaration_for_Incoming_Passengers`: rebuilt `69/69`, `0 no bbox`, `0 low_similarity`.
- `customs_packing_004_Commercial_Invoice_-_EP-INV-2026-0384`: rebuilt `63/63`, `0 no bbox`, `0 low_similarity`.
- `customs_packing_005_保税区货物转关运输审批表`: rebuilt `28/28`, `0 no bbox`, `0 low_similarity`.
- `customs_packing_006_Cold_Chain_Logistics_Temperature_Compliance_and_Packing_Report`: rebuilt 147 matched bboxes and preserved 10 old bboxes; `0 no bbox`, `1 low_similarity`.
- `customs_packing_007_跨境电商综合税则税率对照手册`: rebuilt 68 matched bboxes and preserved 6 old bboxes; `0 no bbox`, `0 low_similarity`.
- `customs_packing_008_Container_Stowage_and_Cargo_Securing_Plan`: rebuilt 165 matched bboxes and preserved 4 old bboxes; `0 no bbox`, `0 low_similarity`.
- `customs_packing_009_出口退税会计处理实务指引`: rebuilt 91 matched bboxes and preserved 16 old bboxes; `0 no bbox`, `0 low_similarity`.
- `customs_packing_010_国际多式联运提单_Multimodal_Transport_Bill_of_Lading`: rebuilt `101/101`, `0 no bbox`, `0 low_similarity`.
- `customs_packing_011_ATA_Carnet_暂准进口单证册_Carbon_Copy`: rebuilt `146/146`, `0 no bbox`, `0 low_similarity`.
- `customs_packing_012_保税仓库入仓单_Bonded_Warehouse_Entry_Certificate`: rebuilt `210/210`, `0 no bbox`, `0 low_similarity`.
- `customs_packing_013_加工贸易手册_Processing_Trade_Manual`: rebuilt `48/48`, `0 no bbox`, `0 low_similarity`.
- `customs_packing_014_集装箱装箱检验报告_Container_Loading_Inspection_Report`: rebuilt 240 matched bboxes and preserved 1 old bbox; `0 no bbox`, `0 low_similarity`.
- `customs_packing_015_海关估价单_Customs_Valuation_Document`: rebuilt `185/187`; `2 no bbox` are empty-text GT entries, `0 low_similarity`.
- `customs_packing_016_跨境电商进口清关单_Cross-Border_Import_Clearance`: rebuilt `171/171`, `0 no bbox`, `0 low_similarity`.
- `customs_packing_017_综合进口报关套件_Comprehensive_Import_Declaration_Package`: rebuilt `136/136`, `0 no bbox`, `0 low_similarity`.
- `customs_packing_018_大宗散货装箱检验总表_Bulk_Cargo_Packing_Inspection_Master_Report`: rebuilt `497/497`, `0 no bbox`, `0 low_similarity`.
- `customs_packing_019_多国转口贸易清关文件_Multi-Country_Re-Export_Trade_Customs_Documentation`: rebuilt `142/142`, `0 no bbox`, `0 low_similarity`.
- `customs_packing_020_综合保税区进出区清单`: rebuilt `328/328`, `0 no bbox`, `0 low_similarity`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.

Verification:

- v513 report: `/tmp/pdb_logistics_customs_packing_domrect_v513.json`
- Representative cover checks:
  - `cover_audit_logistics_customs_v513/11_customs_packing_001_Packing_List_-_HM-PL-2026-03842_cover.jpg`
  - `cover_audit_logistics_customs_v513/12_customs_packing_015_海关估价单_Customs_Valuation_Document_cover.jpg`
  - `cover_audit_logistics_customs_v513/13_customs_packing_020_综合保税区进出区清单_cover.jpg`

Status after v513:

- `09_logistics/02_customs_packing`: `3009/3011 boxed`, `2 no bbox`, `37 low_similarity`.
- Full `09_logistics`: `21286/21444 boxed`, `158 no bbox`, `1811 low_similarity`.

## 20260607_logistics_ticket_v514_v515

Scope:

- Rebuilt `09_logistics/03_ticket`.
- v514 was written first with the earlier logistics uniform scale method, but visual cover checks showed narrow-ticket pages still had boxes in the right blank viewport area.
- Root cause found and fixed in `scripts/repair_logistics_bboxes_uniform_dom.py`:
  - some ticket HTML pages use a narrow body (for example 420 CSS px) inside a 794 CSS px screenshot viewport;
  - the correct scale is `clean_png_width / browser_viewport_width`, not `clean_png_width / local page/body width`;
  - getBoundingClientRect viewport coordinates must be mapped directly without subtracting local page/body left offset;
  - cross-node exact Range matching is needed because ticket GT often contains parent blocks and child field annotations that overlap.

Token sequence:

- superseded v514: `20260607_logistics_ticket_domrect_v514`
- current v515: `20260607_logistics_ticket_viewport_range_v515`

Case-level changes:

- `ticket_001_电影票`: rebuilt `123/123`, `0 no bbox`, `0 low_similarity`.
- `ticket_002_停车小票`: rebuilt `100/100`, `0 no bbox`, `0 low_similarity`.
- `ticket_003_博物馆门票`: rebuilt `122/122`, `0 no bbox`, `0 low_similarity`.
- `ticket_004_地铁单程票`: rebuilt `119/119`, `0 no bbox`, `0 low_similarity`.
- `ticket_005_中国高铁电子票据_-_G1234`: rebuilt `143/145`; `2 no bbox` remain for short amount strings `¥5.0` and `¥3.0`, `0 low_similarity`.
- `ticket_006_Singapore_Airlines_Boarding_Intelligence_Pass`: rebuilt `77/77`, `0 no bbox`, `0 low_similarity`.
- `ticket_007_周杰伦演唱会_VIP_电子票`: rebuilt `72/72`, `0 no bbox`, `0 low_similarity`.
- `ticket_008_DB_Doppelpassagier_Fahrkarte`: rebuilt `55/55`, `0 no bbox`, `0 low_similarity`.
- `ticket_009_黄山文化地理叙事门票系统`: rebuilt `129/129`, `0 no bbox`, `0 low_similarity`.
- `ticket_010_客运终端系统输出凭证`: rebuilt `95/95`, `0 no bbox`, `0 low_similarity`.
- `ticket_011_Cruise_Boarding_Pass_-_Symphony_of_the_Seas`: rebuilt `109/109`, `0 no bbox`, `0 low_similarity`.
- `ticket_012_CBA篮球赛门票`: rebuilt `48/48`, `0 no bbox`, `0 low_similarity`.
- `ticket_013_国家大剧院《茶馆》戏剧票据系统`: rebuilt `76/76`, `0 no bbox`, `0 low_similarity`.
- `ticket_014_JR_Green_Car_Ticket_System`: rebuilt `176/176`, `0 no bbox`, `2 low_similarity`.
- `ticket_015_上海迪士尼度假区_-_Future_Ticket_System`: rebuilt `93/93`, `0 no bbox`, `0 low_similarity`.
- `ticket_016_舟山群岛客运航程记录系统`: already aligned under the new mapping, `155/155`, `0 no bbox`, `0 low_similarity`.
- `ticket_017_国际联程机票行程单_Multi-Segment_International_Flight_Itinerary`: rebuilt `268/268`, `0 no bbox`, `0 low_similarity`.
- `ticket_018_Eurail_Global_Pass_欧洲铁路通票`: rebuilt `122/122`, `0 no bbox`, `0 low_similarity`.
- `ticket_019_草莓音乐节3日通票_Strawberry_Music_Festival_3-Day_Pass`: rebuilt `304/304`, `0 no bbox`, `0 low_similarity`.
- `ticket_020_长三角综合交通联票_Yangtze_Delta_Integrated_Transport_Combo_Ticket`: rebuilt `151/151`, `0 no bbox`, `0 low_similarity`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.

Verification:

- v515 report: `/tmp/pdb_logistics_ticket_viewport_range_v515.json`
- Representative cover checks:
  - `cover_audit_logistics_ticket_v515/11_ticket_001_电影票_cover.jpg`
  - `cover_audit_logistics_ticket_v515/12_ticket_005_中国高铁电子票据_-_G1234_cover.jpg`
  - `cover_audit_logistics_ticket_v515/13_ticket_009_黄山文化地理叙事门票系统_cover.jpg`
  - `cover_audit_logistics_ticket_v515/14_ticket_019_草莓音乐节3日通票_Strawberry_Music_Festival_3-Day_Pass_cover.jpg`
  - `cover_audit_logistics_ticket_v515/15_ticket_020_长三角综合交通联票_Yangtze_Delta_Integrated_Transport_Combo_Ticket_cover.jpg`

Status after v515:

- `09_logistics/03_ticket`: `2537/2539 boxed`, `2 no bbox`, `2 low_similarity`.
- Full `09_logistics`: `21286/21444 boxed`, `158 no bbox`, `1605 low_similarity`.

## 20260607_logistics_itinerary_hotel_bol_v516_v518

Scope:

- Continued `09_logistics` with the corrected viewport-DPR mapping and cross-node Range matching from v515.
- Rebuilt:
  - `09_logistics/04_itinerary`
  - `09_logistics/05_hotel_booking`
  - `09_logistics/06_bill_of_lading`

Token sequence:

- v516: `20260607_logistics_itinerary_viewport_range_v516`
- v517: `20260607_logistics_hotel_viewport_range_v517`
- v518 current: `20260607_logistics_bol_viewport_range_v518`

Case-level summary:

- `09_logistics/04_itinerary`: 20 cases processed; 3815 annotations matched to DOM/Range rects, 972 old structure bboxes preserved, 13 no bbox remain, 101 low_similarity remain in final review data.
- `09_logistics/05_hotel_booking`: 20 cases processed; 2715 annotations matched, 273 old structure bboxes preserved, 0 no bbox remain, 20 low_similarity remain in final review data.
- `09_logistics/06_bill_of_lading`: 20 cases processed; 3712 annotations matched, 111 old structure bboxes preserved, 14 no bbox remain, 17 low_similarity remain in final review data.

Notable per-case residuals:

- `itinerary_012_Trans-China_Rail_Topology_Interface`: 9 no bbox remain.
- `itinerary_017_三十天环球商务行程总览_30-Day_Global_Business_Itinerary`: 4 no bbox remain.
- `bill_of_lading_009_散货海运提单_Bulk_Cargo_Ocean_Bill_of_Lading`: 13 no bbox remain.
- `bill_of_lading_016_Ocean_Freight_Mosaic_Dashboard`: 1 no bbox remains.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.

Verification:

- v516 report: `/tmp/pdb_logistics_itinerary_viewport_range_v516.json`
- v517 report: `/tmp/pdb_logistics_hotel_viewport_range_v517.json`
- v518 report: `/tmp/pdb_logistics_bol_viewport_range_v518.json`
- Representative cover checks:
  - `cover_audit_logistics_itinerary_v516/11_itinerary_001_商务出差行程确认函_Business_Trip_Itinerary_Confirmation_cover.jpg`
  - `cover_audit_logistics_itinerary_v516/13_itinerary_008_锐进科技集团2026年度大会_cover.jpg`
  - `cover_audit_logistics_itinerary_v516/15_itinerary_012_Trans-China_Rail_Topology_Interface_cover.jpg`
  - `cover_audit_logistics_hotel_v517/11_hotel_booking_001_酒店热敏小票_cover.jpg`
  - `cover_audit_logistics_hotel_v517/12_hotel_booking_007_Hotel_Confirmation_Hybrid_Dashboard_cover.jpg`
  - `cover_audit_logistics_hotel_v517/13_hotel_booking_013_Dense_Invoice_Dashboard_cover.jpg`
  - `cover_audit_logistics_bol_v518/12_bill_of_lading_009_散货海运提单_Bulk_Cargo_Ocean_Bill_of_Lading_cover.jpg`
  - `cover_audit_logistics_bol_v518/13_bill_of_lading_016_Ocean_Freight_Mosaic_Dashboard_cover.jpg`
  - `cover_audit_logistics_bol_v518/14_bill_of_lading_020_综合物流主提单_Master_Bill_of_Lading_-_UILG-MBL-2026-SH-00392_cover.jpg`

Status after v518:

- `09_logistics/01_shipping_label`: `4142/4269 boxed`, `127 no bbox`, `118 low_similarity`.
- `09_logistics/02_customs_packing`: `3009/3011 boxed`, `2 no bbox`, `37 low_similarity`.
- `09_logistics/03_ticket`: `2537/2539 boxed`, `2 no bbox`, `2 low_similarity`.
- `09_logistics/04_itinerary`: `4787/4800 boxed`, `13 no bbox`, `101 low_similarity`.
- `09_logistics/05_hotel_booking`: `2988/2988 boxed`, `0 no bbox`, `20 low_similarity`.
- `09_logistics/06_bill_of_lading`: `3823/3837 boxed`, `14 no bbox`, `17 low_similarity`.
- Full `09_logistics`: `21286/21444 boxed`, `158 no bbox`, `295 low_similarity`.

## 20260607_logistics_shipping_hard_v519

Scope:

- Revisited the three `09_logistics/01_shipping_label` cases that were intentionally held back from the earlier safe shipping batch:
  - `shipping_label_005_COSCO_SHIPPING_-_Bill_of_Lading`
  - `shipping_label_007_UPS_Worldwide_Express_Saver_-_Pharmaceutical_Cold_Chain_Waybill`
  - `shipping_label_008_Maersk_Line_-_Container_Shipping_Manifest_集装箱货运清单`
- Used the corrected viewport-DPR mapping from v515.

Token:

- v519: `20260607_logistics_shipping_hard_viewport_v519`

Case-level changes:

- `shipping_label_005_COSCO_SHIPPING_-_Bill_of_Lading`: rebuilt 154 matched bboxes, preserved 1 old structure bbox, 64 no bbox remain, 1 low_similarity remains.
- `shipping_label_007_UPS_Worldwide_Express_Saver_-_Pharmaceutical_Cold_Chain_Waybill`: rebuilt 47 matched bboxes, preserved 94 old structure bboxes, 13 no bbox remain, 37 low_similarity remain.
- `shipping_label_008_Maersk_Line_-_Container_Shipping_Manifest_集装箱货运清单`: rebuilt 73 matched bboxes, preserved 89 old structure bboxes, 49 no bbox remain, 12 low_similarity remain.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.

Verification:

- v519 report: `/tmp/pdb_logistics_shipping_hard_viewport_v519.json`
- Representative cover checks:
  - `cover_audit_logistics_shipping_hard_v519/11_shipping_label_005_COSCO_SHIPPING_-_Bill_of_Lading_cover.jpg`
  - `cover_audit_logistics_shipping_hard_v519/12_shipping_label_007_UPS_Worldwide_Express_Saver_-_Pharmaceutical_Cold_Chain_Waybill_cover.jpg`
  - `cover_audit_logistics_shipping_hard_v519/13_shipping_label_008_Maersk_Line_-_Container_Shipping_Manifest_集装箱货运清单_cover.jpg`

Status after v519:

- Full `09_logistics`: `21287/21444 boxed`, `157 no bbox`, `265 low_similarity`.
- Remaining no bbox is dominated by these hard shipping cases plus a few complex itinerary/bill-of-lading cases.

## 20260607_logistics_shipping_dynamic_viewport_v520

Scope:

- Found an additional logistics rendering issue:
  - some clean PNGs are wider than 2481 px, meaning the original screenshot viewport width was not always 794 CSS px;
  - the stable mapping is fixed DPR `300/96 = 3.125`, with per-case browser viewport width inferred from `clean_png_width / DPR`.
- Updated `scripts/repair_logistics_bboxes_uniform_dom.py` to set viewport width per case before measuring DOM rects.
- Rebuilt the two hard shipping cases that benefited from this dynamic viewport correction:
  - `shipping_label_007_UPS_Worldwide_Express_Saver_-_Pharmaceutical_Cold_Chain_Waybill`
  - `shipping_label_008_Maersk_Line_-_Container_Shipping_Manifest_集装箱货运清单`
- Did not rewrite `shipping_label_005_COSCO_SHIPPING_-_Bill_of_Lading` in this pass because dry-run increased no bbox by 1.

Token:

- v520: `20260607_logistics_shipping_007_008_dynamic_v520`

Case-level changes:

- `shipping_label_007_UPS_Worldwide_Express_Saver_-_Pharmaceutical_Cold_Chain_Waybill`: rebuilt 152 matched bboxes; now `152/154 boxed`, `2 no bbox`, `0 low_similarity`.
- `shipping_label_008_Maersk_Line_-_Container_Shipping_Manifest_集装箱货运清单`: rebuilt 176 matched bboxes; now `176/211 boxed`, `35 no bbox`, `0 low_similarity`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.

Verification:

- v520 report: `/tmp/pdb_logistics_shipping_007_008_dynamic_v520.json`
- Representative cover checks:
  - `cover_audit_logistics_shipping_dynamic_v520/11_shipping_label_007_UPS_Worldwide_Express_Saver_-_Pharmaceutical_Cold_Chain_Waybill_cover.jpg`
  - `cover_audit_logistics_shipping_dynamic_v520/12_shipping_label_008_Maersk_Line_-_Container_Shipping_Manifest_集装箱货运清单_cover.jpg`

Status after v520:

- Full `09_logistics`: `21312/21444 boxed`, `132 no bbox`, `216 low_similarity`.

## 20260607_logistics_dynamic_safe_cases_v521

Scope:

- Applied the dynamic per-case viewport width fix to logistics cases that dry-run showed as safe: no bbox count did not increase and obvious stale viewport offsets were removed.
- This pass writes bbox coordinates only; it does not add or remove GT annotations.

Token:

- v521: `20260607_logistics_dynamic_safe_cases_v521`

Case-level changes:

- `09_logistics/04_itinerary/itinerary_010_医疗旅游行程计划_Medical_Tourism_Itinerary_Plan`: rebuilt 322 bboxes, `0 no bbox`.
- `09_logistics/04_itinerary/itinerary_011_WILDERNESS_LENS_荒野镜头_Issue_48`: rebuilt 164 bboxes, `0 no bbox`.
- `09_logistics/04_itinerary/itinerary_013_工业展会参观行程信息网络图`: rebuilt 293 bboxes, `0 no bbox`.
- `09_logistics/04_itinerary/itinerary_015_珠峰北坡攀登行程_Mt._Everest_North_Face_Expedition`: rebuilt 230 bboxes, `0 no bbox`.
- `09_logistics/04_itinerary/itinerary_016_行程确认函_Itinerary_Confirmation_for_Visa_Application`: rebuilt 284 bboxes, `0 no bbox`.
- `09_logistics/05_hotel_booking/hotel_booking_007_Hotel_Confirmation_Hybrid_Dashboard`: rebuilt 250 bboxes, `0 no bbox`.
- `09_logistics/05_hotel_booking/hotel_booking_011_Legal_Contract_Page`: rebuilt 129 bboxes, `0 no bbox`.
- `09_logistics/05_hotel_booking/hotel_booking_012_Enterprise_Mail_Thread`: rebuilt 99 bboxes, `0 no bbox`.
- `09_logistics/05_hotel_booking/hotel_booking_013_Dense_Invoice_Dashboard`: rebuilt 120 bboxes, `0 no bbox`.
- `09_logistics/05_hotel_booking/hotel_booking_014_Travel_Journal_Infographic`: rebuilt 228 bboxes, `0 no bbox`.
- `09_logistics/06_bill_of_lading/bill_of_lading_005_Cold_Chain_Pharmaceutical_Transport_Dashboard`: rebuilt 93 bboxes, `0 no bbox`.
- `09_logistics/06_bill_of_lading/bill_of_lading_009_散货海运提单_Bulk_Cargo_Ocean_Bill_of_Lading`: rebuilt 260 bboxes, `2 no bbox`.
- `09_logistics/06_bill_of_lading/bill_of_lading_011_Transshipment_Bill_of_Lading_Dossier`: rebuilt 85 bboxes, `0 no bbox`.
- `09_logistics/06_bill_of_lading/bill_of_lading_016_Ocean_Freight_Mosaic_Dashboard`: rebuilt 214 bboxes, `1 no bbox`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.

Verification:

- v521 report: `/tmp/pdb_logistics_dynamic_safe_cases_v521.json`

## 20260607_logistics_shipping008_table_struct_v522

Scope:

- Fixed `09_logistics/01_shipping_label/shipping_label_008_Maersk_Line_-_Container_Shipping_Manifest_集装箱货运清单`.
- Updated `scripts/repair_logistics_bboxes_uniform_dom.py` so `table`/`figure` categories use structural DOM candidates instead of cross-node text Range unions. This avoids huge white cover boxes and half-covered tables on complex logistics manifests.

Token:

- v522: `20260607_logistics_shipping008_table_struct_v522`

Case-level changes:

- `shipping_label_008_Maersk_Line_-_Container_Shipping_Manifest_集装箱货运清单`: rebuilt 175 bboxes, preserved 1 old structure bbox, `35 no bbox` remain. No bbox count did not increase.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.

Verification:

- v522 report: `/tmp/pdb_logistics_shipping008_table_struct_v522.json`
- Cover check: `cover_audit_logistics_shipping008_v522/11_shipping_label_008_Maersk_Line_-_Container_Shipping_Manifest_集装箱货运清单_cover.jpg`

## 20260607_logistics_ticket017_018_rerange_v523

Scope:

- Rebuilt the two ticket cases flagged by frontend review as visibly shifted:
  - `09_logistics/03_ticket/ticket_017_国际联程机票行程单_Multi-Segment_International_Flight_Itinerary`
  - `09_logistics/03_ticket/ticket_018_Eurail_Global_Pass_欧洲铁路通票`
- Both cases remain fully boxed with no added or removed GT annotations.

Token:

- v523: `20260607_logistics_ticket017_018_rerange_v523`

Case-level changes:

- `ticket_017_国际联程机票行程单_Multi-Segment_International_Flight_Itinerary`: rebuilt 268 bboxes, 177 coordinates changed, `0 no bbox`.
- `ticket_018_Eurail_Global_Pass_欧洲铁路通票`: rebuilt 122 bboxes, 61 coordinates changed, `0 no bbox`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.

Verification:

- v523 report: `/tmp/pdb_logistics_ticket017_018_rerange_v523.json`
- Cover checks:
  - `cover_audit_logistics_ticket017_018_v523/11_ticket_017_国际联程机票行程单_Multi-Segment_International_Flight_Itinerary_cover.jpg`
  - `cover_audit_logistics_ticket017_018_v523/12_ticket_018_Eurail_Global_Pass_欧洲铁路通票_cover.jpg`
- Residual audit after v523: `/tmp/pdb_logistics_ticket_residual_v523.json`; `ticket_017` residual is `0`, `ticket_018` residual is lower and dominated by graphic/stamp residue rather than global bbox offset.

Status after v523:

- `09_logistics/01_shipping_label`: `4168/4269 boxed`, `101 no bbox`, `0 low_similarity`.
- `09_logistics/02_customs_packing`: `3009/3011 boxed`, `2 no bbox`, `0 low_similarity`.
- `09_logistics/03_ticket`: `2537/2539 boxed`, `2 no bbox`, `0 low_similarity`.
- `09_logistics/04_itinerary`: `4787/4800 boxed`, `13 no bbox`, `0 low_similarity`.
- `09_logistics/05_hotel_booking`: `2988/2988 boxed`, `0 no bbox`, `0 low_similarity`.
- `09_logistics/06_bill_of_lading`: `3834/3837 boxed`, `3 no bbox`, `0 low_similarity`.
- Full `09_logistics`: `21323/21444 boxed`, `121 no bbox`, `0 low_similarity`.

## 20260608_certificate_range_dom_v524

Scope:

- Rebuilt all `104` cases in `10_certificate`.
- Root cause fixed: every certificate case in review data had stale logical `width`/`height` values that did not match the full release clean PNG. The frontend therefore displayed the image and SVG overlay in different coordinate systems.
- Added `scripts/repair_certificate_bboxes_range_dom.py`:
  - resets each case to the release image dimensions;
  - maps browser `getBoundingClientRect` / exact `Range` rects directly with DPR `300/96`;
  - uses exact text Range boxes for text/title/header/footer/page-number/caption annotations;
  - keeps full DOM `<table>` boxes for table annotations;
  - preserves an old valid bbox only when an exact DOM range is not found, to avoid increasing no-bbox counts.

Token:

- v524: `20260608_certificate_range_dom_v524`

Category-level changes:

- Before v524: `10_certificate` was `14589/14664 boxed`, `75 no bbox`, `7 low_similarity`.
- After v524: `10_certificate` is `14626/14664 boxed`, `38 no bbox`, `0 low_similarity`.
- `01_diploma_transcript`: `5306/5306 boxed`, `0 no bbox`.
- `02_professional_cert`: `2730/2768 boxed`, `38 no bbox`.
- `03_award_honor`: `1495/1495 boxed`, `0 no bbox`.
- `04_service_receipt`: `3514/3514 boxed`, `0 no bbox`.
- `05_quality_certification`: `1581/1581 boxed`, `0 no bbox`.

Case-level notes:

- All `104` certificate cases had image dimensions corrected to the actual release clean PNG size.
- `14570` annotation coordinates changed; `56` existing valid boxes were intentionally preserved where exact range matching failed.
- `diploma_transcript_001_南京大学理学学士学位证书`: fixed the user-flagged degree certificate; dimensions changed `1600x2248` -> `2500x3556`, `35/35 boxed`, `0 no bbox`, `0 low_similarity`.
- Remaining no-bbox case: `10_certificate/02_professional_cert/professional_cert_016_消防工程师资格证书_-_对角线分割_Fire_Protection_Engineer_Certificate`, `95/133 boxed`, `38 no bbox`. No additional no-bbox cases were introduced.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.

Verification:

- Frontend confirmed loaded token `data 20260608_certificate_range_dom_v524`.
- Frontend confirmed `diploma_transcript_001_南京大学理学学士学位证书` now uses `imgWidth=2500`, `imgHeight=3556`, `viewBox=0 0 2500 3556`, and the first title bbox is `[795, 339, 1705, 514]`.
- Repair report: `reports/pdb_certificate_range_dom_v524.json`.
- Residual report: `reports/pdb_certificate_residual_v524.json`.
- Cover checks:
  - `cover_audit_certificate_v524/11_diploma_transcript_001_南京大学理学学士学位证书_cover.jpg`
  - `cover_audit_certificate_v524/12_diploma_transcript_017_清_华_大_学_cover.jpg`
  - `cover_audit_certificate_v524/13_professional_cert_016_消防工程师资格证书_-_对角线分割_Fire_Protection_Engineer_Certificate_cover.jpg`
  - `cover_audit_certificate_v524/14_service_receipt_020_国际会展服务结算单_Exhibition_Service_Settlement_cover.jpg`
  - `cover_audit_certificate_v524/15_quality_certification_011_欧盟有机认证证书_-_EU_Organic_Certification_Magazine_cover.jpg`

## 20260608_certificate_prof016_clipped_v525

Scope:

- Revisited `10_certificate/02_professional_cert/professional_cert_016_消防工程师资格证书_-_对角线分割_Fire_Protection_Engineer_Certificate` after v524.
- DOM probe showed the remaining no-bbox cluster (`个人信息 / Personal Information`, `考试成绩 / Exam Scores`, early score rows, and `注册编号`) has negative viewport `top` values because the bottom-right triangle content overflows above the visible release PNG canvas.
- These clipped/off-canvas annotations should remain no-bbox; do not force them into visible page coordinates.

Token:

- v525: `20260608_certificate_prof016_clipped_v525`

Case-level changes:

- Removed 5 old preserved hallucination boxes that belonged to the same clipped/off-canvas exam-score area:
  - anno `18`, text `92`
  - anno `20`, text `84`
  - anno `21`, text `消防设施 Fire Protection Systems`
  - anno `28`, text `85`
  - anno `34`, text `78`
- `professional_cert_016`: `95/133 boxed`, `38 no bbox` -> `90/133 boxed`, `43 no bbox`, `0 low_similarity`.
- Full `10_certificate` after v525: `14621/14664 boxed`, `43 no bbox`, `0 low_similarity`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.

Verification:

- v525 report: `reports/pdb_certificate_prof016_clipped_v525.json`.
- Cover check: `cover_audit_certificate_prof016_v525/11_professional_cert_016_消防工程师资格证书_-_对角线分割_Fire_Protection_Engineer_Certificate_cover.jpg`.

## 20260608_certificate003_precision_v526

Scope:

- Targeted precision pass for `10_certificate/01_diploma_transcript/diploma_transcript_003_中国科学院计算技术研究所_结业证书`.
- User flagged the bottom evaluation/signature area as slightly imprecise after the full certificate rebuild.
- This pass only tightened existing visible bboxes; no GT annotations were added or removed.

Token:

- v526: `20260608_certificate003_precision_v526`

Case-level changes:

- Tightened evaluation-title overlap/line-height boxes:
  - anno `29`, text `优秀`: `[749, 4149, 851, 4223]` -> `[748, 4144, 856, 4185]`
  - anno `30`, text `结业`: `[843, 4149, 945, 4223]` -> `[838, 4144, 945, 4185]`
  - anno `31`, text `结业总评：优秀结业`: `[514, 4148, 946, 4224]` -> `[514, 4143, 945, 4185]`
- Tightened evaluation text rows:
  - anno `32`, text `综合成绩 91.1 分 | 出勤率 98% | 全部课程考核通过`: `[515, 4251, 1493, 4315]` -> `[515, 4250, 1485, 4317]`
  - anno `33`, text `结业项目获评"优秀结业项目"，推荐参加高级认证考试。`: `[515, 4328, 1532, 4392]` -> `[515, 4327, 1530, 4395]`
  - anno `34`, long evaluation paragraph: `[515, 4405, 2354, 4547]` -> `[515, 4401, 2357, 4512]`
- Tightened signature/date rows:
  - anno `37`, text `继续教育中心`: `[365, 4906, 579, 4964]` -> `[365, 4902, 579, 4933]`
  - anno `40`, text `2024年6月28日`: `[2139, 4906, 2395, 4964]` -> `[2150, 4902, 2390, 4931]`

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.

Verification:

- Local crop check: `/tmp/cert003_bottom_v526.jpg`.
- Repair report: `reports/pdb_certificate003_precision_v526.json`.

## 20260608_technical_api011_footer_v530

Scope:

- Repaired the full `08_technical` category after frontend review showed broad misalignment.
- Root cause: all `110` technical cases had stale review `width`/`height` metadata while most bbox coordinates were already in full clean-PNG coordinates. The frontend SVG `viewBox` therefore used the wrong coordinate system.
- Avoided a full brute-force DOM rewrite for every technical case because dry-runs on product/manual layouts could drop valid footer boxes or over-tighten table-like regions.

Tokens:

- v527: `20260608_technical_dim_sync_v527`
- v528: `20260608_technical_low_range_dom_v528`
- v529: `20260608_technical_api011_restore_v529`
- v530: `20260608_technical_api011_footer_v530`

Category-level changes:

- Before v527: `08_technical` had `3417/3419 boxed`, `2 no bbox`, `42 low_similarity`, and `110` cases with stale dimensions.
- After v530: `08_technical` has `3417/3419 boxed`, `2 no bbox`, `0 low_similarity`, and `0` stale-dimension cases.
- `01_product_manual`: `727/727 boxed`, `0 no bbox`, `0 low_similarity`.
- `02_datasheet`: `959/959 boxed`, `0 no bbox`, `0 low_similarity`.
- `03_api_reference`: `522/522 boxed`, `0 no bbox`, `0 low_similarity`.
- `04_architecture_diagram`: `537/537 boxed`, `0 no bbox`, `0 low_similarity`.
- `05_release_notes`: `672/674 boxed`, `2 no bbox`, `0 low_similarity`.

Case-level changes:

- All `110` cases in `08_technical`: synced case `width`/`height` to the actual release clean PNG dimensions; bbox coordinates were preserved in this dimension-sync step. Exact old/new sizes are in `reports/pdb_technical_dim_sync_v527.json`.
- `08_technical/01_product_manual/product_manual_012_Drone_Flight_Guide_EN`: rebuilt `50` bbox coordinates with exact DOM range boxes; low similarity cleared.
- `08_technical/02_datasheet/datasheet_006_MOSFET_Datasheet`: rebuilt `30` bbox coordinates; low similarity cleared; table annotations remain whole-grid boxes.
- `08_technical/02_datasheet/datasheet_014_光纤收发器规格书`: rebuilt `35` bbox coordinates; low similarity cleared; table annotations remain whole-grid boxes.
- `08_technical/03_api_reference/api_doc_005_GraphQL_Schema_Doc`: rebuilt `39` bbox coordinates; low similarity cleared.
- `08_technical/03_api_reference/api_reference_009_OpenAPI_Swagger`: rebuilt `20` bbox coordinates; low similarity cleared.
- `08_technical/03_api_reference/api_reference_017_Smart_Contract_ABI`: rebuilt `28` bbox coordinates; low similarity cleared.
- `08_technical/03_api_reference/api_reference_020_MQTT_IoT_Protocol`: rebuilt `41` bbox coordinates; low similarity cleared.
- `08_technical/04_architecture_diagram/architecture_diagram_011_CICD_Pipeline`: rebuilt `23` bbox coordinates; low similarity cleared.
- `08_technical/04_architecture_diagram/architecture_diagram_013_区块链节点架构`: rebuilt `35` bbox coordinates; low similarity cleared.
- `08_technical/04_architecture_diagram/architecture_diagram_016_数据库主从复制拓扑`: rebuilt `35` bbox coordinates; low similarity cleared.
- `08_technical/04_architecture_diagram/architecture_diagram_017_Zero_Trust_Network`: rebuilt `47` bbox coordinates; low similarity cleared.
- `08_technical/04_architecture_diagram/architecture_diagram_018_游戏服务器架构`: rebuilt `39` bbox coordinates; low similarity cleared.
- `08_technical/05_release_notes/release_notes_002_Open_Source_Library_v2.0_Changelog`: rebuilt `32` bbox coordinates; low similarity cleared.
- `08_technical/05_release_notes/release_notes_004_API_v3_Migration_Guide`: rebuilt `34` bbox coordinates; low similarity cleared. Remaining no-bbox annotations are #39 `Response Format (Before / After)` and #44 `Pagination (v3)`, which are present in HTML beyond the rendered/captured clean image and were not forced into visible coordinates.
- `08_technical/05_release_notes/release_notes_012_Tesla_OTA_Update`: rebuilt `38` bbox coordinates; low similarity cleared.
- `08_technical/05_release_notes/release_notes_019_Cybersecurity_Bulletin`: rebuilt `43` bbox coordinates; low similarity cleared.
- `08_technical/03_api_reference/api_reference_011_WebSocket_API`: v528 automatic rebuild incorrectly dropped six bottom/footer boxes, so v529 restored the case from the v527 backup. v530 then fixed only annotation #45, moving the footer `Realtime Gateway API v2.0 — Documentation generated 2026-04-05 — © ChatAPI Inc.` from stale top bbox `[459, 17, 1031, 60]` to bottom footer bbox `[712, 5213, 2394, 5288]`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.

Verification:

- Frontend confirmed loaded `review_data.js?20260608_technical_api011_footer_v530`.
- Frontend samples confirmed image/SVG dimensions match:
  - `product_manual_001_工业机器人操作手册`: clean image `2481x22397`, overlay `viewBox=0 0 2481 22397`.
  - `api_reference_011_WebSocket_API`: clean image `2481x5334`, overlay `viewBox=0 0 2481 5334`, `46/46 boxed`.
  - `release_notes_004_API_v3_Migration_Guide`: clean image `2525x7041`, overlay `viewBox=0 0 2525 7041`, `45/47 boxed`, `2 no bbox`.
- Reports:
  - `reports/pdb_technical_dim_sync_v527.json`
  - `reports/pdb_technical_low_range_dom_v528.json`
  - `reports/pdb_technical_api011_restore_v529.json`
  - `reports/pdb_technical_api011_footer_v530.json`
- Cover checks:
  - `cover_audit_technical_v530/11_product_manual_001_工业机器人操作手册_cover.jpg`
  - `cover_audit_technical_v530/12_datasheet_006_MOSFET_Datasheet_cover.jpg`
  - `cover_audit_technical_v530/13_api_reference_011_WebSocket_API_cover.jpg`
  - `cover_audit_technical_v530/14_architecture_diagram_013_区块链节点架构_cover.jpg`
  - `cover_audit_technical_v530/15_release_notes_004_API_v3_Migration_Guide_cover.jpg`

## 20260608_technical_datasheet022_sds_manual_v532

Scope:

- Targeted repair for `08_technical/02_datasheet/datasheet_022_Sulfuric_Acid_SDS` after frontend review showed obvious local offsets in the top SDS region.
- User-visible issue: #1/#4 and nearby section/table boxes were shifted and could span into the left navigation/sidebar instead of covering the actual title/table content.

Token:

- v532: `20260608_technical_datasheet022_sds_manual_v532`

Case-level changes:

- Replaced all `30` stale/offset boxes in `datasheet_022_Sulfuric_Acid_SDS` with verified DOM-range coordinates.
- Important corrected examples:
  - #0 `SAFETY DATA SHEET (SDS)`: `[553, 229, 1795, 318]` -> `[795, 211, 1559, 286]`
  - #1 product/SDS metadata block: `[544, 462, 1609, 684]` -> `[796, 299, 2216, 401]`
  - #2 `Section 1 Identification`: `[731, 489, 1154, 526]` -> `[795, 486, 1155, 536]`
  - #3 Section 1 table: `[777, 569, 2297, 1176]` -> `[796, 571, 2248, 1192]`
  - #4 `Section 2 Hazard Identification`: `[634, 1086, 1402, 1163]` -> `[795, 1233, 1265, 1283]`
- The final visible SDS sections were also corrected rather than left no-bbox:
  - #24 `Sec. 12 Ecology`: `[796, 6901, 2090, 7006]`
  - #25 `Sec. 13 Disposal`: `[796, 7019, 2216, 7124]`
  - #26 `Sec. 14 Transport`: `[796, 7138, 2190, 7183]`
  - #27 `Sec. 15 Regulatory`: `[796, 7197, 2230, 7301]`
  - #28 `Sec. 16`: `[796, 7315, 2235, 7419]`
  - #29 footer/disclaimer: `[796, 7498, 2246, 7639]`
- Case summary refreshed from `25/30 boxed, 5 no bbox` after the rejected v531 automatic application to `30/30 boxed, 0 no bbox`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.

Notes:

- v531 automatic application was not kept as final because it clipped the visible bottom SDS sections #25-#29 after a browser-layout mismatch. v532 overwrote it with the verified dry-run coordinates.
- Table annotations remain whole-table boxes.

Verification:

- Frontend confirmed loaded `data 20260608_technical_datasheet022_sds_manual_v532`.
- Frontend confirmed `datasheet_022_Sulfuric_Acid_SDS` now shows `30/30 boxed`, `0 no bbox`, image `2481x7766`, overlay `viewBox=0 0 2481 7766`.
- Repair report: `reports/pdb_technical_datasheet022_sds_manual_v532.json`.
- Cover check: `cover_audit_technical_datasheet022_v532/11_datasheet_022_Sulfuric_Acid_SDS_cover.jpg`.

## 20260608_technical_arch007_iot_manual_v533

Scope:

- Targeted repair for `08_technical/04_architecture_diagram/architecture_diagram_007_IoT_Platform` after frontend review showed many obvious local offsets.
- User-visible issue: title/module labels around the top and layered architecture area were clustered near the upper-left margin instead of covering the actual IoT platform title, layer labels, and module boxes.

Token:

- v533: `20260608_technical_arch007_iot_manual_v533`

Case-level changes:

- Replaced all `40` stale/offset boxes with verified DOM-range coordinates.
- Important corrected examples:
  - #0 `IoT Platform Architecture`: `[70, 63, 355, 89]` -> `[215, 204, 1128, 302]`
  - #1 document metadata line: `[218, 329, 1542, 370]` -> `[216, 327, 1554, 375]`
  - #2 `Layered Architecture`: `[70, 147, 227, 164]` -> `[215, 484, 724, 554]`
  - #3 `Application Layer`: `[86, 198, 195, 213]` -> `[266, 657, 622, 717]`
  - #4 `Web Dashboard`: `[305, 757, 2165, 795]` -> `[305, 752, 538, 797]`
  - #5 `Mobile App (iOS/Android)`: `[200, 226, 313, 238]` -> `[630, 752, 994, 797]`
  - #9 `Data Down / Commands`: `[809, 868, 1728, 920]` -> `[730, 865, 1813, 923]`
  - #33 `Protocol Comparison` table: `[70, 627, 734, 779]` -> `[216, 2091, 2327, 2608]`
  - #39 footer: `[539, 3109, 2004, 3144]` -> `[531, 3103, 2012, 3146]`
- Case summary remains `40/40 boxed`, `0 no bbox`, `0 low_similarity`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.

Notes:

- Used verified dry-run DOM-range coordinates rather than automatic apply, to avoid browser-layout mismatch on this single case.
- Table annotation #33 remains a whole-table box.

Verification:

- Frontend confirmed loaded `data 20260608_technical_arch007_iot_manual_v533`.
- Frontend confirmed `architecture_diagram_007_IoT_Platform` now shows `40/40 boxed`, `0 no bbox`, image `2513x3509`, overlay `viewBox=0 0 2513 3509`.
- Repair report: `reports/pdb_technical_arch007_iot_manual_v533.json`.
- Cover check: `cover_audit_technical_arch007_v533/11_architecture_diagram_007_IoT_Platform_cover.jpg`.

## 20260608_technical_hybrid_pad_v535

Scope:

- Continued `08_technical` visual bbox repair after v533.
- Applied hybrid repairs for cases where the previous DOM dry-run generated empty boxes, then added small padding to DOM-range text boxes that visibly leaked glyphs in cover mode.

Token:

- v535: `20260608_technical_hybrid_pad_v535`

Case-level changes:

- Hybrid bbox repair was applied to these `12` technical cases:
  - `08_technical/01_product_manual/product_manual_001_工业机器人操作手册`
  - `08_technical/01_product_manual/product_manual_017_CNC_操作手册`
  - `08_technical/01_product_manual/product_manual_020_电梯维保手册`
  - `08_technical/02_datasheet/datasheet_024_危险化学品SDS_中英`
  - `08_technical/03_api_reference/api_doc_002_REST_API_Reference`
  - `08_technical/03_api_reference/api_doc_003_Python_SDK_Doc`
  - `08_technical/03_api_reference/api_reference_007_Google_Maps_API`
  - `08_technical/03_api_reference/api_reference_010_Docker_API`
  - `08_technical/03_api_reference/api_reference_012_OpenGL_API`
  - `08_technical/04_architecture_diagram/architecture_diagram_003_Microservices_Platform`
  - `08_technical/04_architecture_diagram/architecture_diagram_014_Event_Driven_Architecture`
  - `08_technical/04_architecture_diagram/architecture_diagram_020_Cloud_Native_Architecture`
- Added small padding to DOM-range text boxes in `106` technical cases to stop cover-mode glyph leakage; per-case details are in `reports/pdb_technical_hybrid_pad_v535.json`.
- No GT annotation was added or removed.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.

Verification:

- Report: `reports/pdb_technical_hybrid_pad_v535.json`.
- Cover samples: `cover_audit_technical_v535_manual_samples/`.

## 20260608_technical_api018_manual_runs_v536

Scope:

- Targeted visual repair for `08_technical/03_api_reference/api_reference_018_iOS_UIKit_API`.
- User-visible issue: method signature and description rows were still partly uncovered after the left-column offset was corrected in v535.

Token:

- v536: `20260608_technical_api018_manual_runs_v536`

Case-level changes:

- Rebuilt `43` bbox coordinates from released clean PNG foreground runs.
- Covered existing API method signature, description, table, see-also, availability, and footer annotations.
- Did not add annotations for the visible but source-unannotated `h2`/class badge UI elements.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.

Verification:

- Report: `reports/pdb_technical_api018_manual_runs_v536.json`.
- Cover check: `cover_audit_technical_api018_v536/11_api_reference_018_iOS_UIKit_API_cover.jpg`.
- Method crop: `cover_audit_technical_api018_v536/11_api_reference_018_iOS_UIKit_API_method_crop.jpg`.

## 20260608_technical_api001_visual_runs_v537

Scope:

- Targeted visual repair for `08_technical/03_api_reference/api_doc_001_RESTful_API_Reference`.

Token:

- v537: `20260608_technical_api001_visual_runs_v537`

Case-level changes:

- Rebuilt `16` bbox coordinates from visual foreground runs.
- Corrected body paragraph, table, and code block boxes.
- Left top dark navigation and section headings visible where the source GT does not contain matching annotations.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.

Verification:

- Report: `reports/pdb_technical_api001_visual_runs_v537.json`.
- Cover check: `cover_audit_technical_api001_018_v537/01_api_doc_001_RESTful_API_Reference_cover.jpg`.

## 20260608_technical_api002_visual_runs_v538

Scope:

- Targeted visual repair for `08_technical/03_api_reference/api_doc_002_REST_API_Reference`.

Token:

- v538: `20260608_technical_api002_visual_runs_v538`

Case-level changes:

- Rebuilt `25` bbox coordinates with a three-zone visual mapping:
  - #0-#6 left navigation.
  - #7-#10, #12-#16, #18-#23 central documentation.
  - #11, #17, #20, #24 right-side code examples.
- Left duplicated central code blocks visible where the source GT does not separately annotate them.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.

Verification:

- Report: `reports/pdb_technical_api002_visual_runs_v538.json`.
- Cover check: `cover_audit_technical_api001_002_018_v538/01_api_doc_002_REST_API_Reference_cover.jpg`.

## 20260608_technical_api003_visual_runs_v539

Scope:

- Targeted visual repair for `08_technical/03_api_reference/api_doc_003_Python_SDK_Doc`.

Token:

- v539: `20260608_technical_api003_visual_runs_v539`

Case-level changes:

- Rebuilt `15` bbox coordinates.
- Corrected code block, table, Returns, Deprecation, Compatibility, and footer annotations.
- Left blue Sphinx headings visible where the source GT does not contain matching annotations.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.

Verification:

- Report: `reports/pdb_technical_api003_visual_runs_v539.json`.
- Cover check: `cover_audit_technical_api001_002_003_018_v539/01_api_doc_003_Python_SDK_Doc_cover.jpg`.

## 20260608_technical_pm012_formula_v540

Scope:

- Targeted repair for `08_technical/01_product_manual/product_manual_012_Drone_Flight_Guide_EN`.
- User-visible issue: the two performance-calculation formula annotations were still boxed up in the earlier checklist card area while the actual formula panels near section 4 remained visible.

Token:

- v540: `20260608_technical_pm012_formula_v540`

Case-level changes:

- Updated `2` bbox coordinates:
  - #30 `Flight Time ≈ ...`: `[86, 2328, 994, 2403]` -> `[125, 7638, 2355, 7993]`.
  - #31 `Max Range = ...`: `[86, 2449, 951, 2483]` -> `[125, 8038, 2355, 8258]`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.

Verification:

- Report: `reports/pdb_technical_pm012_formula_v540.json`.
- Cover check: `cover_audit_technical_pm012_v540/01_product_manual_012_Drone_Flight_Guide_EN_cover.jpg`.
- Formula crop: `cover_audit_technical_pm012_v540/01_product_manual_012_formula_crop.jpg`.

## 20260608_technical_api020_lwt_v541

Scope:

- Targeted repair for `08_technical/03_api_reference/api_reference_020_MQTT_IoT_Protocol`.
- User-visible issue: the Last Will and Testament section was locally shifted; #37 `{"status":"offline","ts":<epoch>}` was still boxed in the upper topic hierarchy area, and neighboring LWT labels/values/code were too low or too narrow.

Token:

- v541: `20260608_technical_api020_lwt_v541`

Case-level changes:

- Updated `14` bbox coordinates in the LWT section:
  - #28 `Last Will and Testament (LWT)`
  - #29 LWT explanatory paragraph
  - #30 `LWT Configuration`
  - #31 `Will Topic`
  - #32 `factory/{plant_id}/gateway/status`
  - #33 `Will QoS`
  - #34 `Will Retain`
  - #35 `true`
  - #36 `Will Payload`
  - #37 `{"status":"offline","ts":<epoch>}`
  - #38 `Will Delay`
  - #39 `10s(MQTT 5.0 delay interval)`
  - #40 online-message code block
  - #41 footer line
- The visible QoS value `1` remains unboxed because it is absent from the source GT; no GT annotation was added for it.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.

Verification:

- Report: `reports/pdb_technical_api020_lwt_v541.json`.
- Cover check: `cover_audit_technical_api020_v541/01_api_reference_020_MQTT_IoT_Protocol_cover.jpg`.
- LWT crop: `cover_audit_technical_api020_v541/01_api_reference_020_lwt_crop.jpg`.

## 20260608_technical_api020_subscription_v542

Scope:

- Follow-up repair for `08_technical/03_api_reference/api_reference_020_MQTT_IoT_Protocol`.
- User-visible issue: the `Subscription Examples` heading and table header were still leaking above the cover boxes.

Token:

- v542: `20260608_technical_api020_subscription_v542`

Case-level changes:

- Updated `2` bbox coordinates:
  - #23 `Subscription Examples`: `[782, 3656, 1404, 3753]` -> `[782, 3568, 1605, 3670]`.
  - #24 subscription examples table: `[788, 3740, 2381, 4613]` -> `[788, 3690, 2381, 4618]`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.

Verification:

- Report: `reports/pdb_technical_api020_subscription_v542.json`.
- Cover check: `cover_audit_technical_api020_v542/01_api_reference_020_MQTT_IoT_Protocol_cover.jpg`.
- Crops:
  - `cover_audit_technical_api020_v542/01_api_reference_020_subscription_crop.jpg`
  - `cover_audit_technical_api020_v542/01_api_reference_020_lwt_crop.jpg`

## 20260608_technical_api005_code_top_v543

Scope:

- Targeted repair for `08_technical/03_api_reference/api_doc_005_GraphQL_Schema_Doc`.
- User-visible issue: the first signature line of each GraphQL code block leaked above #31/#34/#37 because the bbox top edges were slightly too low.

Token:

- v543: `20260608_technical_api005_code_top_v543`

Case-level changes:

- Updated `3` bbox coordinates:
  - #31 query example code block: `[108, 3974, 922, 4802]` -> `[108, 3945, 940, 4805]`.
  - #34 mutation example code block: `[108, 5178, 1605, 5805]` -> `[108, 5150, 1610, 5808]`.
  - #37 subscription example code block: `[117, 6181, 1102, 6741]` -> `[108, 6150, 1115, 6745]`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.

Verification:

- Report: `reports/pdb_technical_api005_code_top_v543.json`.
- Cover check: `cover_audit_technical_api005_v543/01_api_doc_005_GraphQL_Schema_Doc_cover.jpg`.
- Code crop: `cover_audit_technical_api005_v543/01_api_doc_005_code_crop.jpg`.

Current technical status after v543:

- Latest token: `20260608_technical_api005_code_top_v543`.
- `08_technical/01_product_manual`: `727/727 boxed`, `0 no bbox`.
- `08_technical/02_datasheet`: `959/959 boxed`, `0 no bbox`.
- `08_technical/03_api_reference`: `522/522 boxed`, `0 no bbox`.
- `08_technical/04_architecture_diagram`: `537/537 boxed`, `0 no bbox`.
- `08_technical/05_release_notes`: `672/674 boxed`, `2 no bbox`.
- Remaining no-bbox annotations are unchanged and still limited to `08_technical/05_release_notes/release_notes_004_API_v3_Migration_Guide` #39 `Response Format (Before / After)` and #44 `Pagination (v3)`, which were previously judged not visible in the clean PNG capture.

## 20260608_technical_api012_oauth_v544

Scope:

- Targeted repair for `08_technical/03_api_reference/api_reference_012_OAuth2_Flow`.
- User-visible issue: after v543, the OAuth case still had visually shifted boxes: #1 covered part of the flow diagram, #2 was sitting near the Endpoints table area, and later table/code/section boxes were offset downward.

Token:

- v544: `20260608_technical_api012_oauth_v544`

Case-level changes:

- Updated `18` existing bbox coordinates using pixel-aligned visual foreground runs from the released clean PNG:
  - #0 header `OAuth 2.0 Authorization Framework`: `[46, 102, 1492, 307]` -> `[75, 90, 1465, 300]`.
  - #1 title `Authorization Code Flow`: `[103, 393, 821, 561]` -> `[75, 385, 805, 445]`.
  - #2 flow caption `1. Redirect to authorize ...`: `[224, 1507, 2257, 1668]` -> `[300, 1265, 2185, 1320]`.
  - #3 title `Endpoints`: `[114, 1658, 440, 1826]` -> `[75, 1405, 420, 1465]`.
  - #4 Endpoints table: `[57, 1790, 2424, 2381]` -> `[75, 1505, 2406, 2030]`.
  - #5 title `Token Types`: `[114, 2402, 514, 2570]` -> `[75, 2100, 480, 2165]`.
  - #6 Token Types table: `[57, 2534, 2424, 3016]` -> `[75, 2205, 2406, 2600]`.
  - #7 title `Example — POST /token`: `[114, 3036, 842, 3204]` -> `[75, 2680, 800, 2750]`.
  - #8 label `Request`: `[47, 3148, 262, 3308]` -> `[75, 2788, 250, 2840]`.
  - #9 request code block: `[95, 3291, 1374, 3765]` -> `[75, 2850, 2407, 3370]`.
  - #10 label `Response — 200 OK`: `[47, 3760, 507, 3921]` -> `[75, 3390, 485, 3445]`.
  - #11 response code block: `[95, 3904, 1510, 4290]` -> `[75, 3455, 2407, 3885]`.
  - #12 title `Scopes`: `[114, 4343, 369, 4511]` -> `[75, 3955, 350, 4025]`.
  - #13 Scopes table: `[57, 4475, 2424, 5284]` -> `[75, 4075, 2406, 4745]`.
  - #14 title `Error Responses`: `[114, 5305, 616, 5425]` -> `[75, 4840, 600, 4910]`.
  - #15 error intro paragraph: `[72, 4957, 1166, 5009]` -> `[75, 4950, 1170, 5010]`.
  - #16 error code lines: `[71, 4957, 1215, 5189]` -> `[75, 5030, 1300, 5190]`.
  - #17 footer line: `[71, 5311, 1302, 5355]` -> `[75, 5300, 1305, 5360]`.
- Added `1` GT annotation for the visible OAuth flow diagram that was present in the clean PNG but missing from the source GT:
  - #18 `figure`: bbox `[70, 470, 335, 1255]`, text `OAuth authorization flow diagram: User Agent Browser, Auth Server /authorize, Token Endpoint /token, Resource API Protected`.

GT annotation change:

- Added GT annotations in this pass: `1`.
- Removed GT annotations in this pass: `0`.

Verification:

- Report: `reports/pdb_technical_api012_oauth_v544.json`.
- Cover check: `cover_audit_technical_api012_oauth_v544/11_api_reference_012_OAuth2_Flow_cover.jpg`.
- Visual label overlay and crops:
  - `cover_audit_technical_api012_oauth_v544/top_labels.jpg`
  - `cover_audit_technical_api012_oauth_v544/tables_labels.jpg`
  - `cover_audit_technical_api012_oauth_v544/code_scopes_labels.jpg`

Current technical status after v544:

- Latest token: `20260608_technical_api012_oauth_v544`.
- `08_technical/01_product_manual`: `727/727 boxed`, `0 no bbox`.
- `08_technical/02_datasheet`: `959/959 boxed`, `0 no bbox`.
- `08_technical/03_api_reference`: `523/523 boxed`, `0 no bbox`.
- `08_technical/04_architecture_diagram`: `537/537 boxed`, `0 no bbox`.
- `08_technical/05_release_notes`: `672/674 boxed`, `2 no bbox`.
- Remaining no-bbox annotations are unchanged and still limited to `08_technical/05_release_notes/release_notes_004_API_v3_Migration_Guide` #39 `Response Format (Before / After)` and #44 `Pagination (v3)`, which were previously judged not visible in the clean PNG capture.

## 20260608_medical_discharge018_dom_v545

Scope:

- Targeted repair for `06_medical/09_discharge_summary/discharge_summary_018` after the user reported the UI case `1019. 06_medical/09_discharge_s...`.
- User-visible issue: many labels were drawn on blank/off-page regions, especially #0/#1 and #5-#34. Large clinical tables and the bottom signature/footer region were not visually aligned.

Token:

- v545: `20260608_medical_discharge018_dom_v545`

Case-level changes:

- Rebuilt `34` visible bboxes from released HTML DOM rects mapped to the clean PNG coordinate system (`x = 604 + 3 * css_x`, `y = 3 * css_y`):
  - #2 header block.
  - #3/#4 hospital title and discharge-record subtitle.
  - #5-#11 patient strip fields.
  - #12/#13 MMT/ROM/MAS title and table.
  - #14/#15 therapy-log title and table.
  - #16/#17 swallowing title and table.
  - #18/#19 assistive-devices title and checklist.
  - #20-#22 home-modification/caregiver-training callout title and two text columns.
  - #23 discharge medication/follow-up note box.
  - #24-#34 signature names, roles, date, and footer line.
  - #35 dashboard summary table added in an earlier pass, now re-aligned to the six score panels.
- Cleared bbox for `2` decorative/watermark source annotations without deleting them:
  - #0 `康复医学中心`: very low-opacity background watermark crossing the clinical tables; drawing it would create a misleading giant box over real content.
  - #1 `REHABILITATION`: CSS position is outside the 2400px clean PNG capture.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Cleared existing bbox values: `2` (#0/#1), annotations retained.

Verification:

- Report: `reports/pdb_medical_discharge018_dom_v545.json`.
- Visual check: `cover_audit_medical_discharge018_v545/`.
- v545 cover showed small anti-aliased leaks in the patient strip and callout tails, fixed in v546/v547 below.

## 20260608_medical_discharge018_strip_v546

Scope:

- Follow-up cover-mode refinement for `06_medical/09_discharge_summary/discharge_summary_018`.
- User-visible issue after v545: a few glyph tails still leaked at patient-strip boundaries, the `Assistive Devices` title tail, and the home-modification/caregiver callout endings.

Token:

- v546: `20260608_medical_discharge018_strip_v546`

Case-level changes:

- Updated `11` bbox coordinates:
  - #5-#11 patient-strip fields expanded horizontally to cover full cell text.
  - #18 assistive-devices title widened to include the full English tail.
  - #20 home-modification/caregiver title widened.
  - #21/#22 callout text columns widened to cover trailing characters.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.

Verification:

- Report: `reports/pdb_medical_discharge018_strip_v546.json`.
- Visual check: `cover_audit_medical_discharge018_v546/`.
- v546 cover still showed tiny patient-strip bottom anti-aliasing leakage, fixed in v547 below.

## 20260608_medical_discharge018_strip_v547

Scope:

- Final patient-strip refinement for `06_medical/09_discharge_summary/discharge_summary_018`.
- User-visible issue after v546: tiny bottom-edge anti-aliasing leakage remained in #5-#11 patient-strip labels.

Token:

- v547: `20260608_medical_discharge018_strip_v547`

Case-level changes:

- Updated `7` bbox coordinates:
  - #5 `姓名: 周建华`, #6 `性别: 男`, #7 `年龄: 62岁`, #8 diagnosis, #9 onset date, #10 rehab-transfer date, and #11 Brunnstrom grade were expanded vertically and slightly horizontally.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- #0/#1 remain retained GT annotations with no bbox from v545; no annotation was deleted.

Verification:

- Report: `reports/pdb_medical_discharge018_strip_v547.json`.
- Final visual checks:
  - `cover_audit_medical_discharge018_v547/top_labels.jpg`
  - `cover_audit_medical_discharge018_v547/top_cover.jpg`
  - `cover_audit_medical_discharge018_v547/middle_cover.jpg`
- Final case status: `36 total`, `34 boxed`, `2 no bbox` (#0/#1 decorative/watermark items).
- Latest token after this repair: `20260608_medical_discharge018_strip_v547`.

## 20260608_medical_discharge019020_dom_v548

Scope:

- Follow-up repair for user-reported UI cases `1020` and `1021`:
  - `1020` = `06_medical/09_discharge_summary/discharge_summary_019`.
  - `1021` = `06_medical/09_discharge_summary/discharge_summary_020`.
- These cases were previously counted as boxed, but visual review showed the boxes were not reliably aligned: `discharge_summary_019` had large decorative watermark boxes over clinical content, and `discharge_summary_020` had a page-wide coordinate offset plus a missing CGA score-grid annotation.

Token:

- v548: `20260608_medical_discharge019020_dom_v548`

Case-level changes:

- `06_medical/09_discharge_summary/discharge_summary_019`:
  - Updated `39` bbox coordinates from Chrome DOM rects mapped to the clean PNG coordinate system.
  - #0 confidentiality banner was re-aligned to the visible red banner text.
  - #4-#8 hospital header and patient-identification rows were re-aligned.
  - #9-#31 three-column clinical tables, section headers, genotype/ART/adherence notes, and follow-up table were re-aligned.
  - #32 legal warning block was re-aligned to the visible warning box.
  - #33-#41 signatures, roles, discharge date, date label, and footer were re-aligned.
  - #39 `2026-03-20` was moved from the incorrect top patient-strip position to the bottom signature/date area.
  - Cleared bbox for `3` decorative/watermark source annotations without deleting them: #1 `机密`, #2 `CONFIDENTIAL`, #3 `严禁泄露`.
- `06_medical/09_discharge_summary/discharge_summary_020`:
  - Updated `40` bbox coordinates from Chrome DOM rects mapped to the clean PNG coordinate system.
  - #2-#4 hospital header/title/subtitle were moved back to the actual top header.
  - #5-#14 patient strip fields were moved from the page-left blank area to their actual row.
  - #15-#30 diagnosis list, medication table, multi-system labs, interaction table, ACP block, medication-change table, MDT follow-up table, and caregiver warning were re-aligned.
  - #31-#41 signatures, roles, discharge date, date label, and footer were re-aligned.
  - #39 `2026-03-18` was moved from the incorrect top patient-strip position to the bottom signature/date area.
  - Cleared bbox for `2` decorative/watermark source annotations without deleting them: #0 `老年医学科`, #1 `GERIATRICS`.
  - Added #42 `table` annotation for the visible CGA score grid (`MMSE`, `MoCA`, `Barthel ADL`, `IADL`, `MNA`, `GDS-15`, `Morse`, `Braden`, `Frailty`) that was present in HTML/clean PNG but absent from the source GT annotation list.

GT annotation change:

- Added GT annotations in this pass: `1` (#42 CGA score grid in `discharge_summary_020`).
- Removed GT annotations in this pass: `0`.
- Cleared existing bbox values: `5` total (#1/#2/#3 in `discharge_summary_019`, #0/#1 in `discharge_summary_020`), annotations retained.

Verification:

- Report: `reports/pdb_medical_discharge019020_dom_v548.json`.
- Visual checks:
  - `cover_audit_medical_discharge019020_v548/11_discharge_summary_019_cover.jpg`
  - `cover_audit_medical_discharge019020_v548/12_discharge_summary_020_cover.jpg`
  - Candidate label/crop checks: `cover_audit_medical_discharge019020_v548_candidate/`.
- Final case status:
  - `discharge_summary_019`: `42 total`, `39 boxed`, `3 no bbox` (#1/#2/#3 decorative/watermark items).
  - `discharge_summary_020`: `43 total`, `41 boxed`, `2 no bbox` (#0/#1 decorative/watermark items).
- Latest token after this repair: `20260608_medical_discharge019020_dom_v548`.

## 20260608_publishing_book003_visual_v549

Scope:

- Follow-up repair for user-reported UI case `1084`:
  - `1084` = `07_publishing/03_book/book_003_Popular_Science_EN`.
- User-visible issue: the case was counted as fully boxed, but visual inspection showed remaining bbox offsets, especially #21, which was drawn in the left blank margin instead of around the paragraph above the CRISPR toolkit table.

Token:

- v549: `20260608_publishing_book003_visual_v549`

Case-level changes:

- Updated `25` bbox coordinates in `07_publishing/03_book/book_003_Popular_Science_EN`.
- Re-aligned #0-#4 header, chapter label/title, quote, and first section title.
- Re-aligned #5-#15 `Key Milestones` sidebar title and timeline entries, replacing overlapping/shifted sidebar boxes with row-level visual boxes.
- Re-aligned #16/#17 opening body paragraphs so they no longer start at the section title line.
- Fixed #20 `Beyond Cas9: The Expanding Toolkit` to cover the green section heading.
- Fixed #21 paragraph (`CRISPR-Cas9 was just the beginning...`) from the left blank margin to the actual two-line paragraph above the table.
- Nudged #22 CRISPR toolkit table to the visible table frame.
- Re-aligned lower-page #24-#27 (`The First CRISPR Medicines`, the two body paragraphs, and footnotes) so the boxes no longer split lines across adjacent annotations.
- #18/#19 `Did You Know?`, #23 quote attribution, and #28 page number were left unchanged because visual review showed them closer than the DOM-only candidate.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Cleared existing bbox values: `0`.

Verification:

- Report: `reports/pdb_publishing_book003_visual_v549.json`.
- Visual checks:
  - `cover_audit_publishing_book003_v549/11_book_003_Popular_Science_EN_cover.jpg`
  - Candidate/crop checks: `cover_audit_publishing_book003_v549_hybrid_candidate/`.
- Final case status: `29 total`, `29 boxed`, `0 no bbox`.
- Latest token after this repair: `20260608_publishing_book003_visual_v549`.

## 20260608_education_lab012_header_v550

Scope:

- Follow-up repair for user-reported UI case:
  - `02_education/06_lab_report/lab_report_012_无机化学_配合物`.
- User-visible issue: the case was counted as `34/34 boxed`, but visual inspection showed #0 and #1 drawn over the experiment-info table row instead of the green report masthead.

Token:

- v550: `20260608_education_lab012_header_v550`

Case-level changes:

- Updated `2` bbox coordinates in `02_education/06_lab_report/lab_report_012_无机化学_配合物`.
- Fixed #0 `化学实验报告` from `[881, 275, 1187, 316]` to `[1008, 136, 1362, 190]`, moving it from the `实验日期` table row back to the green masthead title.
- Fixed #1 `南京大学化学化工学院 · 无机化学实验(下)` from `[834, 275, 1187, 316]` to `[933, 202, 1512, 239]`, moving it from the same table row back to the masthead subtitle.
- Left #2 unchanged because it already covers the visible two-row experiment-info table (`实验名称`, `实验日期`, `实验室`, `姓名`, `学号`, `指导教师`).
- Full-page visual review showed the remaining annotations are not part of this top-header offset pattern, so no broader re-layout was applied.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Cleared existing bbox values: `0`.

Verification:

- Report: `reports/pdb_education_lab012_header_v550.json`.
- Visual checks:
  - `cover_audit_lab_report012_v550/11_lab_report_012_无机化学_配合物_cover.jpg`
  - Candidate label/crop checks: `cover_audit_lab_report012_v550_candidate/`.
- Final case status: `34 total`, `34 boxed`, `0 no bbox`, `1 low similarity`.
- Latest token after this repair: `20260608_education_lab012_header_v550`.

## 20260608_finance_audit007_visual_v551

Scope:

- Follow-up repair for user-reported UI case:
  - `05_finance/08_audit_report/audit_report_007`.
- User-visible issue: the case was counted as `58/58 boxed`, but visual inspection showed clipped/partial bboxes in the top metadata strip and in section 2, especially #21 (`2.2 资金回流核查 Fund Return Verification`), whose box ended before the visible title text.

Token:

- v551: `20260608_finance_audit007_visual_v551`

Case-level changes:

- Updated `10` bbox coordinates in `05_finance/08_audit_report/audit_report_007`.
- Expanded top metadata fields that were visually clipped:
  - #5 `委托方 Client...`: `[264, 699, 914, 750]` -> `[264, 699, 1010, 750]`.
  - #6 `被审计方 Auditee...`: `[1294, 699, 2020, 750]` -> `[1294, 699, 2140, 750]`.
  - #7 `审计期间 Period...`: `[2324, 699, 2902, 750]` -> `[2324, 699, 3085, 750]`.
  - #8 `资金总规模 Total...`: `[264, 759, 772, 810]` -> `[264, 759, 842, 810]`.
  - #9 `涉及关联方 RP Count...`: `[1294, 759, 1933, 810]` -> `[1294, 759, 2018, 810]`.
  - #10 `审计标准 Standards...`: `[2324, 759, 2885, 810]` -> `[2324, 759, 3025, 810]`.
- Repaired section-title clipping:
  - #18 `二、重大关联方资金拆借明细 Major RP Fund Lending Details`: `[261, 2799, 1371, 2865]` -> `[261, 2738, 1948, 2848]`.
  - #21 `2.2 资金回流核查 Fund Return Verification`: `[1203, 2910, 1927, 2973]` -> `[1203, 2910, 2515, 2973]`.
  - #34 `三、异常交易链路追踪 Suspicious Transaction Chain Tracing`: `[261, 5084, 1382, 5150]` -> `[261, 5084, 1390, 5154]`.
  - #44 `四、审计意见及建议 Audit Opinion & Recommendations`: `[261, 6929, 1292, 6995]` -> `[261, 6929, 1350, 6995]`.
- Kept #20 and #22 table bboxes unchanged after visual review because they already cover the left/right major fund-lending tables without cross-column spillover.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Cleared existing bbox values: `0`.

Verification:

- Report: `reports/pdb_finance_audit007_visual_v551.json`.
- Visual checks:
  - `cover_audit_audit007_v551/11_audit_report_007_cover.jpg`
  - Candidate label/crop checks: `cover_audit_audit007_v551_candidate/`.
- Final case status: `58 total`, `58 boxed`, `0 no bbox`, `0 low similarity`.
- Latest token after this repair: `20260608_finance_audit007_visual_v551`.

## 20260608_medical_report019_visual_v552

Scope:

- Follow-up repair for user-reported UI screenshot of a clinical trial laboratory report:
  - `06_medical/01_medical_report/medical_report_019`.
- User-visible issue: the case was counted as `18/18 boxed`, but #0, #6, #8, #10 and nearby blocks were visually offset into the left blank margin or stale vertical positions.
- Note: the URL in the report message pointed at `02_education/06_lab_report/lab_report_012_无机化学_配合物`, but the screenshot content matched `medical_report_019`.

Token:

- v552: `20260608_medical_report019_visual_v552`

Case-level changes:

- Updated `18` bbox coordinates in `06_medical/01_medical_report/medical_report_019`.
- Repaired top header:
  - #0 `CRO`: `[109, 50, 302, 128]` -> `[651, 38, 839, 144]`.
  - #1 `Clinical Trial Laboratory Report...`: `[1246, 207, 1771, 254]` -> `[869, 24, 1695, 158]`.
  - #2 `Report ID: COV-LAB-2024-XXXXXX...`: `[2845, 33, 3537, 147]` -> `[2491, 32, 2949, 150]`.
- Tightened the centered report title/subtitle:
  - #3 `Central Laboratory Report — Phase III Clinical Trial`: `[1246, 207, 2350, 254]` -> `[1249, 203, 2351, 249]`.
  - #4 `PHOENIX-BC-301...`: `[1153, 262, 2447, 297]` -> `[1158, 260, 2442, 291]`.
- Moved section title boxes from stale table/body positions back to the visible blue title text:
  - #5 `Subject Information & Sample Tracking`: `[700, 388, 1301, 444]` -> `[725, 318, 1420, 382]`.
  - #7 `Laboratory Results with CTCAE v5.0 Grading`: `[700, 589, 1533, 648]` -> `[725, 666, 1520, 730]`.
  - #9 `Visit-by-Visit Trend — Key Parameters`: `[700, 1603, 1325, 1662]` -> `[725, 1679, 1405, 1743]`.
  - #11 `Investigator Assessment & Action Required`: `[700, 2161, 1492, 2214]` -> `[725, 2235, 1495, 2299]`.
- Repaired table and matrix boxes that were shifted into the left blank margin:
  - #6 subject/sample table: `[145, 391, 3455, 645]` -> `[705, 391, 2895, 645]`.
  - #8 laboratory results table: `[145, 739, 3455, 1658]` -> `[705, 739, 2895, 1658]`.
  - #10 visit-by-visit trend matrix: `[150, 1758, 3450, 2211]` -> `[705, 1755, 2895, 2214]`.
- Repaired lower text blocks and footer:
  - #12 `Hematologic toxicity...`: `[700, 2339, 1778, 2459]` -> `[705, 2337, 1782, 2538]`.
  - #13 `Hepatic function...`: `[700, 2309, 2900, 2567]` -> `[705, 2308, 2895, 2687]`.
  - #14 `Tumor marker trend...`: `[1832, 2420, 2899, 2529]` -> `[1821, 2417, 2895, 2536]`.
  - #15 `Action items...`: `[1768, 2459, 2900, 2606]` -> `[1821, 2565, 2895, 2684]`.
  - #16 `CTCAE v5.0 Grading Reference...`: `[700, 2741, 2900, 2774]` -> `[705, 2696, 2895, 2806]`.
  - #17 footer service/CLIA/report line: `[701, 2827, 2900, 2857]` -> `[705, 2827, 2895, 2856]`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Cleared existing bbox values: `0`.

Verification:

- Report: `reports/pdb_medical_report019_visual_v552.json`.
- Visual checks:
  - `cover_audit_medical_report019_v552/11_medical_report_019_cover.jpg`
  - Candidate outline/cover checks:
    - `cover_audit_medical_report019_v552_candidate/medical_report019_candidate_outline.jpg`
    - `cover_audit_medical_report019_v552_candidate/medical_report019_candidate_cover.jpg`
- Final case status: `18 total`, `18 boxed`, `0 no bbox`, `0 low similarity`.
- Latest token after this repair: `20260608_medical_report019_visual_v552`.

## 20260608_business_quotation011_header_v553

Scope:

- Follow-up repair for user-reported UI screenshot of a quotation page:
  - `04_business/02_quotation/quotation_011_Precision_Hydraulic_Export_Quote`.
- User-visible issue: the case was counted as `48/48 boxed`, but #4 `Rev: 02` was visually shifted onto the `EUR` cell in the exchange-rate table. The same right-header area also had #1/#5/#7 stale coordinates.

Token:

- v553: `20260608_business_quotation011_header_v553`

Case-level changes:

- Updated `4` bbox coordinates in `04_business/02_quotation/quotation_011_Precision_Hydraulic_Export_Quote`.
- Repaired top-right quotation/exchange-rate header:
  - #1 `QUOTATION`: `[2436, 258, 2801, 296]` -> `[2304, 143, 2797, 249]`, moving it from the Ref line back to the dark quotation badge.
  - #4 `Rev: 02`: `[2821, 427, 2921, 462]` -> `[2688, 363, 2802, 402]`, moving it from the exchange-rate `EUR` row back to the visible revision line.
  - #5 `Exchange Rates (Mar 28, 2025)`: `[2756, 156, 3239, 297]` -> `[2830, 146, 3229, 239]`, tightening it to the exchange-rate title bar.
  - #7 `Source: PBOC midpoint rate`: `[2822, 562, 3236, 615]` -> `[2885, 568, 3174, 603]`, tightening it to the source text below the table.
- Left #2 `Ref: FTX-EU-Q-2025-0847`, #3 `Date: March 28, 2025`, and #6 exchange-rate table unchanged after visual review because they already align with the visible elements.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Cleared existing bbox values: `0`.

Verification:

- Report: `reports/pdb_business_quotation011_header_v553.json`.
- Visual checks:
  - `cover_audit_quotation011_v553/11_quotation_011_Precision_Hydraulic_Export_Quote_cover.jpg`
  - Candidate outline check:
    - `cover_audit_quotation011_v553_candidate/quotation011_candidate_outline.jpg`
- Final case status: `48 total`, `48 boxed`, `0 no bbox`, `0 low similarity`.
- Latest token after this repair: `20260608_business_quotation011_header_v553`.

## 20260608_academic_conference_posters_dom_v554

Scope:

- Batch visual repair for all `30` cases in `01_academic/06_conference_poster`.
- User-visible issue: `conference_poster_019_ICML_FoldFlow`, `conference_poster_020_CoRL_GraspBOOM`, and `conference_poster_021_CVPR_Video_Diffusion` were counted as fully boxed but still visibly misaligned. Root cause for many long posters was stale case canvas height (`3509`) while the clean PNG was taller, which made the front-end overlay scale incorrectly.

Token:

- v554: `20260608_academic_conference_posters_dom_v554`

Method:

- Added `scripts/fix_academic_conference_posters_dom_v554.py`.
- Used poster-specific DOM candidates for titles, KPI strips, equations, tables, code blocks, figures/captions, references, and footer/header bands.
- Mapped rendered CSS coordinates to clean PNG coordinates with DPR=3 and synced each case's `width`/`height` to the real clean PNG size.
- Preserved existing GT annotations. No annotation objects were added or deleted.
- Exact per-annotation old/new bbox changes are recorded in `reports/pdb_academic_conference_posters_dom_v554.json` under each case's `changed_items`.

Aggregate changes:

- Updated `1257` existing bbox coordinate sets.
- Filled `9` existing no-bbox annotations.
- Removed/cleared existing bbox values: `0`.
- Remaining no-bbox in this subcategory: `2`, both in `conference_poster_023_ACL_Multilingual`.
- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.

Case-level changes:

- `conference_poster_001_CVPR_目标检测`: updated `52` bboxes; matched `52/53`; no-bbox `0 -> 0`; size unchanged `[2481,3509]`.
- `conference_poster_002_AAAI_NLP`: updated `40` bboxes; matched `43/43`; no-bbox `0 -> 0`; size unchanged `[2481,3509]`.
- `conference_poster_003_ACL_机器翻译`: updated `49` bboxes; matched `49/49`; no-bbox `0 -> 0`; size unchanged `[2481,3509]`.
- `conference_poster_004_MICCAI_医学分割`: updated `46` bboxes; matched `46/46`; no-bbox `0 -> 0`; size unchanged `[2481,3509]`.
- `conference_poster_005_ICML_强化学习`: updated `50` bboxes; matched `50/50`; no-bbox `0 -> 0`; size unchanged `[2481,3509]`.
- `conference_poster_006_ICLR_生成模型`: updated `38` bboxes; matched `41/41`; no-bbox `0 -> 0`; size unchanged `[2481,3509]`.
- `conference_poster_007_KDD_数据挖掘`: updated `39` bboxes; matched `39/40`; no-bbox `0 -> 0`; size unchanged `[2481,3509]`.
- `conference_poster_008_EMNLP_情感分析`: updated `53` bboxes; matched `53/53`; no-bbox `0 -> 0`; size unchanged `[2481,3509]`.
- `conference_poster_009_ISBI_细胞分割`: updated `31` bboxes; matched `31/31`; no-bbox `0 -> 0`; size unchanged `[2481,3509]`.
- `conference_poster_010_中文计算机视觉`: updated `34` bboxes; matched `34/39`; filled `1` existing no-bbox; no-bbox `1 -> 0`; size unchanged `[2481,3509]`.
- `conference_poster_011_ECCV_3D重建`: updated `44` bboxes; matched `44/44`; no-bbox `0 -> 0`; size unchanged `[2481,3509]`.
- `conference_poster_012_CNCC_鸿图大模型`: updated `46` bboxes; matched `46/47`; no-bbox `0 -> 0`; size `[2481,3509] -> [2481,5375]`.
- `conference_poster_013_NAACL_Summarization`: updated `38` bboxes; matched `38/38`; no-bbox `0 -> 0`; size unchanged `[2481,3509]`.
- `conference_poster_014_SIGIR_推荐系统`: updated `45` bboxes; matched `45/50`; no-bbox `0 -> 0`; size unchanged `[2481,3509]`.
- `conference_poster_015_InterSpeech_语音`: updated `37` bboxes; matched `37/37`; no-bbox `0 -> 0`; size unchanged `[2481,3509]`.
- `conference_poster_016_MICCAI_Organ_Segmentation`: updated `24` bboxes; matched `24/28`; no-bbox `0 -> 0`; size unchanged `[2481,4141]`.
- `conference_poster_017_CVPR_DriveDiff`: updated `39` bboxes; matched `45/45`; no-bbox `0 -> 0`; size `[2481,3509] -> [2481,4744]`.
- `conference_poster_018_NeurIPS_MoEAtlas`: updated `38` bboxes; matched `40/46`; no-bbox `0 -> 0`; size `[2481,3509] -> [2481,5013]`.
- `conference_poster_019_ICML_FoldFlow`: updated `44` bboxes; matched `46/46`; no-bbox `0 -> 0`; size `[2481,3509] -> [2481,5484]`.
- `conference_poster_020_CoRL_GraspBOOM`: updated `41` bboxes; matched `41/47`; no-bbox `0 -> 0`; size `[2481,3509] -> [2481,5238]`.
- `conference_poster_021_CVPR_Video_Diffusion`: updated `30` bboxes; matched `31/32`; no-bbox `0 -> 0`; size unchanged `[2481,3509]`.
- `conference_poster_022_NeurIPS_RLHF`: updated `43` bboxes; matched `43/47`; no-bbox `0 -> 0`; size `[2481,3509] -> [2481,3738]`.
- `conference_poster_023_ACL_Multilingual`: updated `41` bboxes; matched `41/44`; filled `1` existing no-bbox; no-bbox `3 -> 2`; size `[2481,3509] -> [2481,4319]`.
- `conference_poster_024_MICCAI_PathDiff`: updated `50` bboxes; matched `50/53`; no-bbox `0 -> 0`; size `[2481,3509] -> [2481,3947]`.
- `conference_poster_025_ICML_GraphX`: updated `46` bboxes; matched `46/47`; no-bbox `0 -> 0`; size `[2481,3509] -> [2481,5078]`.
- `conference_poster_026_KDD_TempoFormer`: updated `42` bboxes; matched `42/46`; no-bbox `0 -> 0`; size unchanged `[2481,3509]`.
- `conference_poster_027_SIGIR_RAG`: updated `41` bboxes; matched `41/42`; no-bbox `0 -> 0`; size `[2481,3509] -> [2481,5400]`.
- `conference_poster_028_INTERSPEECH_VoiceClone`: updated `46` bboxes; matched `54/55`; filled `4` existing no-bbox; no-bbox `4 -> 0`; size `[2481,3509] -> [2481,4819]`.
- `conference_poster_029_USENIX_KernelGhost`: updated `48` bboxes; matched `48/48`; filled `3` existing no-bbox; no-bbox `3 -> 0`; size `[2481,3509] -> [2481,4209]`.
- `conference_poster_030_IAU_ExoCartographer`: updated `42` bboxes; matched `42/44`; no-bbox `0 -> 0`; size `[2481,3509] -> [2481,3816]`.

Verification:

- Report: `reports/pdb_academic_conference_posters_dom_v554.json`.
- Dry-run report: `/tmp/pdb_conference_posters_all_dry_v554.json`.
- Visual outline checks:
  - `/tmp/pdb_conference_posters_all_dry_v554_outline/`
  - Key checked cases: `conference_poster_019`, `conference_poster_020`, `conference_poster_021`, `conference_poster_022`, `conference_poster_024`, `conference_poster_026`.
- Latest token after this repair: `20260608_academic_conference_posters_dom_v554`.

## 20260608_education_exam002_header_notice_v555

Scope:

- Targeted visual repair for user-reported exam-paper case:
  - `02_education/02_exam_paper/exam_paper_002_高考理综物理`.
- User-visible issue: the case was counted as `73/73 boxed`, but #6 and #8/#9 were visually assigned to the wrong upper bands. #6 duplicated the top information row instead of the `准考证号` row, #8 was on the score table instead of `注意事项`, and #9 only covered middle notice lines rather than the full notice list.

Token:

- v555: `20260608_education_exam002_header_notice_v555`

Case-level changes:

- Updated `4` bbox coordinates in `02_education/02_exam_paper/exam_paper_002_高考理综物理`.
- Repaired the top information rows:
  - #4 `满分分值：100分`: `[1062, 521, 2392, 572]` -> `[1263, 521, 2392, 572]`.
  - #6 `准考证号：`: `[1062, 521, 2392, 572]` -> `[1263, 643, 2392, 694]`.
- Repaired the notice block:
  - #8 `注意事项`: `[88, 1016, 369, 1124]` -> `[141, 1210, 374, 1288]`.
  - #9 notice list text: `[166, 1405, 2085, 1542]` -> `[166, 1328, 2255, 1755]`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Cleared existing bbox values: `0`.

Verification:

- Report: `reports/pdb_education_exam002_header_notice_v555.json`.
- Visual check:
  - `/tmp/pdb_exam002_v555_top_outline.jpg`.
- Final case status: `73 total`, `73 boxed`, `0 no bbox`, `0 low similarity`.
- Latest token after this repair: `20260608_education_exam002_header_notice_v555`.

## 20260608_education_exam_paper_duplicate_bboxes_v556

Scope:

- Conservative follow-up repair for the broader `02_education/02_exam_paper` subcategory after the user noted related exam-paper cases also need repair.
- Audited all `24` exam-paper cases for the high-confidence failure mode where different annotations reuse an identical bbox.
- The generic full DOM dry-run was rejected for this subcategory because it would have converted many existing boxes to unmatched/no-bbox in complex electronics/math exam papers.

Token:

- v556: `20260608_education_exam_paper_duplicate_bboxes_v556`

Method:

- Added `scripts/fix_education_exam_paper_duplicate_bboxes_v556.py`.
- Rematched duplicated-bbox annotations against source HTML DOM candidates while preserving all non-duplicate annotations.
- If a duplicate annotation could not be matched safely, it was preserved unchanged.

Case-level changes:

- `exam_paper_004_answer_sheet_OMR`: updated `4` duplicate-bbox annotations:
  - #7 `考生号：`: `[1330, 405, 1480, 449]` -> `[1285, 392, 2424, 465]`.
  - #8 `准考证号：`: `[241, 485, 428, 529]` -> `[241, 501, 409, 525]`.
  - #31 barcode paste area text: `[1330, 405, 1480, 449]` -> `[1016, 2802, 1606, 2899]`.
  - #32 `填涂说明`: `[241, 485, 428, 529]` -> `[232, 3009, 364, 3048]`.
- `exam_paper_011_高考数学_理科`: updated `2` duplicate-bbox annotations:
  - #76 question 16 text: `[61, 1851, 1727, 1937]` -> `[106, 1851, 1727, 1937]`.
  - #77 `三、解答题...`: `[61, 1851, 1727, 1937]` -> `[142, 1851, 1561, 1937]`.
- `exam_paper_037_Chemistry_Organic_Equilibrium`: updated `1` duplicate-bbox annotation:
  - #66 `(2)（4分）计算Kc和Kp...`: `[176, 2602, 736, 2639]` -> `[176, 2602, 731, 2639]`.
- `exam_paper_046_数字电子技术`: updated `2` duplicate-bbox annotations:
  - #5 `姓名 Name:`: `[109, 365, 214, 395]` -> `[85, 360, 222, 393]`.
  - #10 `Note: Answer clearly...`: `[109, 365, 214, 395]` -> `[271, 458, 1316, 481]`.
- Audited but preserved unchanged due to no safe DOM rematch:
  - `exam_paper_040_Geography_Data_Interpretation`: duplicate targets `2`, changed `0`.
  - `exam_paper_047_模拟电子技术`: duplicate targets `2`, changed `0`.
  - `exam_paper_048_高频电子线路考试`: duplicate targets `8`, changed `0`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Cleared existing bbox values: `0`.

Verification:

- Report: `reports/pdb_education_exam_paper_duplicate_bboxes_v556.json`.
- Dry-run report: `/tmp/pdb_education_exam_paper_duplicate_bboxes_dry_v556.json`.
- Visual outline checks:
  - `/tmp/pdb_exam_duplicate_dry_v556_outline/exam_paper_004_answer_sheet_OMR_outline.jpg`.
  - `/tmp/pdb_exam_duplicate_dry_v556_outline/exam_paper_011_高考数学_理科_outline.jpg`.
  - `/tmp/pdb_exam_duplicate_dry_v556_outline/exam_paper_046_数字电子技术_outline.jpg`.
- Exam-paper subcategory after v556: `24 cases`, `1711 total annotations`, `1695 boxed`, `16 no bbox`, `146 low similarity`.
- Latest token after this repair: `20260608_education_exam_paper_duplicate_bboxes_v556`.

## 20260609_academic_conference001_visual_v557

Scope:

- Targeted visual repair for `01_academic/06_conference_poster/conference_poster_001_CVPR_目标检测`.
- User-visible issue: after broad v554, many boxes were counted as boxed but visually shifted across poster columns; formula, list, chart, conclusion, footer, and header boxes were mixed between left/middle/right regions.

Token:

- v557: `20260609_academic_conference001_visual_v557`

Method:

- Added `scripts/fix_academic_conference001_visual_v557.py`.
- Rebuilt this single case from visually checked Chrome text-range/component coordinates on the released clean PNG (`2481x3509`).
- Used tight text-range boxes for titles/authors/headings/paragraphs, component boxes for tables/flow/chart/footer, and tight visible equation boxes for formula annotations.
- No other conference-poster cases were modified in this pass.

Case-level changes:

- `01_academic/06_conference_poster/conference_poster_001_CVPR_目标检测`: rebuilt `53` existing bbox coordinate sets; boxed `53/53`; no-bbox `0`; low-similarity `0`.

Per-annotation changes:

- #0 `header` `CVPR 2025`: `[2030, 243, 2225, 279]` -> `[2115, 253, 2318, 290]`.
- #1 `title` `Real-Time Multi-Scale Object Detection with Deformable Attention`: `[108, 177, 1480, 256]` -> `[118, 124, 1537, 298]`.
- #2 `text_block` `Yichen Zhang¹, Sarah M. Johnson¹, Wei Liu², Takeshi Yamamoto³, Maria Garcia¹`: `[54, 240, 1413, 255]` -> `[118, 318, 1323, 363]`.
- #3 `text_block` `¹Stanford Vision Lab • ²Tsinghua University • ³University of Tokyo`: `[54, 265, 1021, 285]` -> `[118, 375, 967, 416]`.
- #4 `title` `Background`: `[86, 534, 394, 576]` -> `[89, 532, 391, 578]`.
- #5 `text_block` `Transformer-based detectors achieve state-of-the-art accuracy on COCO, but quadratic at...`: `[84, 623, 765, 761]` -> `[89, 611, 792, 755]`.
- #6 `title` `Key Challenges`: `[85, 776, 340, 819]` -> `[89, 775, 335, 812]`.
- #7 `text_block` `Multi-scale fusion increases cost by 3-5x. Standard attention attends to all spatial lo...`: `[84, 723, 765, 949]` -> `[89, 826, 792, 983]`.
- #8 `title` `Our Insight`: `[84, 1001, 269, 1044]` -> `[89, 1001, 264, 1038]`.
- #9 `text_block` `Restricting attention to deformable sampling points achieves sub-linear complexity whil...`: `[84, 1005, 799, 1164]` -> `[89, 1052, 792, 1232]`.
- #10 `title` `Key Contributions`: `[84, 1198, 322, 1232]` -> `[89, 1252, 375, 1289]`.
- #11 `text_block` `Deformable Multi-Scale Attention reducing FLOPs by 8x. Adaptive Scale Router for dynami...`: `[84, 1198, 765, 1400]` -> `[89, 1303, 792, 1539]`.
- #12 `title` `Architecture`: `[823, 541, 1202, 596]` -> `[872, 532, 1200, 578]`.
- #13 `text_block` `Pipeline: Input → ResNet-50 → FPN → Deformable Encoder → Scale Router → Detection Head.`: `[866, 534, 1522, 721]` -> `[872, 611, 1588, 745]`.
- #14 `title` `Deformable Multi-Scale Attention`: `[823, 739, 1403, 783]` -> `[872, 763, 1402, 800]`.
- #15 `text_block` `Each query attends to K learned offsets per scale. For L levels with K points, complexi...`: `[824, 696, 1574, 933]` -> `[872, 814, 1588, 964]`.
- #16 `title` `Adaptive Scale Router`: `[823, 997, 1231, 1018]` -> `[872, 984, 1226, 1021]`.
- #17 `text_block` `Gating network assigns each query a scale-specific weight vector. Trained end-to-end wi...`: `[823, 1045, 1592, 1066]` -> `[872, 1035, 1588, 1142]`.
- #18 `equation_isolated` `$$L_{\text{focal}} = -\alpha_t (1-p_t)^{\gamma}\log(p_t),\quad \alpha=0.25,\ \gamma=2.0$$`: `[1626, 825, 2270, 900]` -> `[989, 1210, 1470, 1260]`.
- #19 `equation_isolated` `$$L_{\text{GIoU}} = 1 - \text{IoU} + \frac{|C \setminus (A \cup B)|}{|C|}$$`: `[1626, 1028, 2270, 1102]` -> `[1026, 1346, 1434, 1386]`.
- #20 `text_block` `Total: 43.4 GFLOPs, 44.0M params (Backbone 26.4G/23.5M, FPN 5.2G/3.8M, Encoder 8.7G/12....`: `[750, 1288, 1592, 1410]` -> `[872, 1418, 1588, 1525]`.
- #21 `title` `Method Details`: `[1617, 504, 2018, 596]` -> `[1668, 532, 2035, 578]`.
- #22 `title` `Query Formulation`: `[1536, 685, 1949, 737]` -> `[1668, 611, 1963, 649]`.
- #23 `text_block` `300 learnable queries (256-d) interact with multi-scale features through 6 decoder laye...`: `[1513, 685, 2382, 720]` -> `[1668, 662, 2392, 770]`.
- #24 `title` `Scale Router Mechanism`: `[1617, 745, 2047, 813]` -> `[1668, 789, 2066, 827]`.
- #25 `equation_isolated` `$$g_l = \text{softmax}(W_g \cdot q + b_g)_l$$`: `[863, 1126, 1498, 1210]` -> `[1882, 897, 2177, 937]`.
- #26 `text_block` `Final feature is weighted sum across scales. Auxiliary load-balancing loss ensures unif...`: `[1514, 951, 2384, 1060]` -> `[1668, 969, 2392, 1039]`.
- #27 `equation_isolated` `$$L_{\text{bal}} = L \cdot \sum_l f_l \cdot \bar{g}_l,\quad \lambda_{\text{bal}}=0.01$$`: `[863, 1256, 1498, 1330]` -> `[1867, 1107, 2192, 1148]`.
- #28 `title` `Implementation Details`: `[1580, 1197, 2018, 1218]` -> `[1668, 1185, 2035, 1223]`.
- #29 `text_block` `Backbone: ResNet-50 + deformable conv stages 3-4. Training: AdamW, lr=2e-4, 50 epochs, ...`: `[1572, 1101, 2274, 1330]` -> `[1668, 1236, 2364, 1380]`.
- #30 `title` `Training Schedule`: `[1617, 1343, 1872, 1379]` -> `[1668, 1400, 1951, 1437]`.
- #31 `text_block` `3-phase progressive: (1) 480px/20ep, (2) 640px/20ep, (3) 800px/10ep with frozen backbon...`: `[1513, 1471, 2384, 1693]` -> `[1668, 1451, 2392, 1558]`.
- #32 `title` `Main Results on COCO`: `[86, 1747, 612, 1776]` -> `[89, 1737, 610, 1783]`.
- #33 `table` `Model Backbone AP AP50 AP75 FPS Faster R-CNN R-50 40.2 61.0 43.8 26 DETR R-50 42.0 62.4...`: `[85, 1743, 760, 2169]` -> `[89, 1816, 792, 2260]`.
- #34 `title` `Per-Category Analysis`: `[132, 2169, 489, 2201]` -> `[89, 2278, 442, 2316]`.
- #35 `table` `Category AP Improvement Small (<32²) 36.4 +3.8 Medium (32-96²) 56.1 +2.1 Large (>96²) 6...`: `[85, 2238, 760, 2421]` -> `[89, 2331, 792, 2523]`.
- #36 `title` `Ablation: Sampling Points K`: `[149, 2431, 497, 2468]` -> `[89, 2541, 530, 2578]`.
- #37 `table` `K AP GFLOPs FPS 2 51.0 38.6 52 4 52.8 43.4 45 8 53.1 52.8 33 16 53.2 71.5 21`: `[85, 2490, 760, 2720]` -> `[89, 2594, 792, 2834]`.
- #38 `title` `Component Ablation`: `[823, 1708, 1366, 1756]` -> `[872, 1737, 1365, 1783]`.
- #39 `table` `Configuration AP Δ Baseline (Def. DETR) 46.2 — + Scale Router 48.5 +2.3 + Progressive T...`: `[837, 1743, 1524, 2020]` -> `[872, 1816, 1588, 2105]`.
- #40 `title` `Scale Router Analysis`: `[772, 2051, 1211, 2106]` -> `[872, 2123, 1218, 2160]`.
- #41 `text_block` `Gating weights show the router assigns 45% weight to P3 for small objects and 38% to P5...`: `[750, 2098, 1589, 2192]` -> `[872, 2174, 1588, 2281]`.
- #42 `title` `Speed-Accuracy Tradeoff`: `[772, 2182, 1289, 2266]` -> `[872, 2301, 1275, 2338]`.
- #43 `table` `Model Variant AP FPS Ours-Tiny 48.2 72 Ours-Small 50.5 58 Ours-Base 52.8 45 Ours-Large ...`: `[837, 2260, 1524, 2490]` -> `[872, 2354, 1588, 2595]`.
- #44 `title` `Robustness Evaluation`: `[772, 2492, 1142, 2547]` -> `[872, 2612, 1236, 2650]`.
- #45 `text_block` `On COCO-C (corrupted): our method retains 87% of clean AP vs. 79% for DINO, showing imp...`: `[823, 2539, 1531, 2597]` -> `[872, 2663, 1588, 2771]`.
- #46 `title` `AP Comparison`: `[1617, 1708, 2005, 1799]` -> `[1668, 1737, 2021, 1783]`.
- #47 `text_block` `Bar chart: Def.DETR 46.2 · DINO 49.0 · Co-DETR 51.4 · Ours 52.8.`: `[322, 318, 338, 349]` -> `[1668, 1769, 2392, 2076]`.
- #48 `title` `Conclusion`: `[1536, 2070, 1936, 2165]` -> `[1668, 2100, 1949, 2147]`.
- #49 `text_block` `We present a real-time multi-scale detector bridging the accuracy-speed gap through two...`: `[1617, 2274, 2283, 2294]` -> `[1668, 2179, 2392, 2496]`.
- #50 `title` `Acknowledgements`: `[1536, 2363, 1968, 2397]` -> `[1668, 2516, 1982, 2553]`.
- #51 `text_block` `Supported by NSF Grant IIS-2024XXX and Google Research Award. Compute by Stanford HAI.`: `[1513, 2352, 2309, 2372]` -> `[1668, 2567, 2392, 2629]`.
- #52 `header` `CVPR 2025 | Seattle, WA | June 2025 | Code: github.com/stanford-vl/deformable-msdet | y...`: `[83, 2795, 1630, 2900]` -> `[106, 2989, 2375, 3024]`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Cleared existing bbox values: `0`.

Verification:

- Report: `reports/pdb_academic_conference001_visual_v557.json`.
- Visual outline checks: `cover_audit_academic_conference001_v557/full.jpg`, `cover_audit_academic_conference001_v557/top.jpg`, `cover_audit_academic_conference001_v557/middle.jpg`.
- Latest token after this repair: `20260609_academic_conference001_visual_v557`.

## 20260609_academic_conference019_visual_v558

Scope:

- Targeted visual repair for `01_academic/06_conference_poster/conference_poster_019_ICML_FoldFlow`.
- User-visible issue: after v554, the long-poster canvas height was correct but many boxes were still visually shifted across the notebook notes, KPI strip, tables/captions, reference list, and footer.

Token:

- v558: `20260609_academic_conference019_visual_v558`

Method:

- Added `scripts/fix_academic_conference019_visual_v558.py`.
- Rebuilt this single case from visually checked Chrome text-range/component coordinates on the released clean PNG (`2481x5484`).
- Subtracted the centered HTML body left margin before scaling, because this poster uses `body { margin: 0 auto; }`.
- Split table captions from table grids; split the inline reading-list references by their `[n]` text ranges. No other conference-poster cases were modified in this pass.

Case-level changes:

- `01_academic/06_conference_poster/conference_poster_019_ICML_FoldFlow`: rebuilt `46` existing bbox coordinate sets; boxed `46/46`; no-bbox `0`; low-similarity `0`.

Per-annotation changes:

- #0 `header` `📓 LAB NOTEBOOK · PROTEIN GENERATION · VOL.III | ICML 2029 · VIENNA · POSTER #2218 · WED...`: `[0, 95, 2481, 151]` -> `[121, 59, 2419, 149]`.
- #1 `text_block` `EXPERIMENT — 19 / draft 4 / fri 18:42`: `[126, 189, 821, 292]` -> `[121, 191, 801, 271]`.
- #2 `title` `FoldFlow: Riemannian Flow Matching for Protein Backbone Generation`: `[82, 284, 2253, 433]` -> `[121, 242, 2245, 581]`.
- #3 `text_block` `A geometry-aware flow-matching model that generates de-novo protein backbones directly ...`: `[130, 473, 2088, 666]` -> `[169, 556, 2024, 732]`.
- #4 `text_block` `Mei-Lin Chen¹ · Theo Ravensburg² · Aniket Joshi¹,³ · Sara Eikenberry⁴ · Olu Adebayo⁵ · ...`: `[45, 733, 1568, 764]` -> `[121, 748, 1497, 805]`.
- #5 `text_block` `¹ Mila / Université de Montréal   ² EPFL Laboratory of Biomolecular Modeling   ³ IIT Bo...`: `[0, 756, 1994, 812]` -> `[121, 808, 1866, 858]`.
- #6 `text_block` `Designability (scTM > 0.5) 87.4%. Sampling speedup 14×. Novel folds / 1k 312. Max lengt...`: `[71, 803, 2466, 977]` -> `[121, 893, 2419, 1112]`.
- #7 `title` `1  WHAT BUGS US`: `[167, 1139, 724, 1216]` -> `[169, 1170, 741, 1270]`.
- #8 `text_block` `Diffusion-based protein generators (RFdiffusion, Chroma, Genie) are now the de-facto to...`: `[210, 1260, 1389, 1355]` -> `[172, 1298, 1397, 1474]`.
- #9 `text_block` `Two consequences hurt every wet-lab pipeline we talked to:`: `[172, 1445, 934, 1476]` -> `[172, 1482, 924, 1532]`.
- #10 `text_block` `Slow: a 256-aa backbone takes ~90 s on an A100, blocking iterative loop-design. Geometr...`: `[179, 1435, 1345, 1682]` -> `[172, 1540, 1410, 1686]`.
- #11 `text_block` `We want a model that lives on SE(3)^N, samples in O(20 steps), and scales to 512 aa wit...`: `[72, 1652, 1505, 1781]` -> `[172, 1687, 1370, 1786]`.
- #12 `title` `2  THE FOLDFLOW PIPELINE`: `[111, 1861, 1048, 1907]` -> `[169, 1897, 1092, 1998]`.
- #13 `text_block` `Pipeline: NOISE (x₁ ~ N(SE(3)^N)) → FRAME (SE(3) tokens) → IPA-T (geom. transformer ×24...`: `[206, 1997, 1415, 2233]` -> `[172, 2032, 1410, 2250]`.
- #14 `figure_caption` `FIG 1 ↗ five-stage Riemannian flow chain — total 6.4 s for a 256-aa backbone`: `[360, 2198, 1222, 2234]` -> `[351, 2253, 1230, 2297]`.
- #15 `text_block` `The pipeline ingests Gaussian noise on the product manifold SE(3)^N, refines it through...`: `[166, 2206, 1415, 2418]` -> `[172, 2342, 1375, 2483]`.
- #16 `title` `3  METHOD — RIEMANNIAN FLOW MATCHING`: `[89, 2505, 1221, 2565]` -> `[169, 2595, 1269, 2747]`.
- #17 `text_block` `Let φ_t: SE(3)^N → SE(3)^N denote the geodesic interpolation between data x₀ and noise ...`: `[70, 2680, 1505, 2747]` -> `[172, 2763, 1384, 2868]`.
- #18 `equation_isolated` `$$\mathcal{L}_{\text{RFM}}(\theta) = \mathbb{E}_{t,x_0,x_1} \left\| v_{\theta}(x_t, t) ...`: `[214, 2755, 1403, 2917]` -> `[210, 2905, 1371, 3016]`.
- #19 `equation_isolated` `$$x_{t+\Delta t} = \exp_{x_t}\!\left( \Delta t \cdot v_{\theta}(x_t, t) \right) \quad (...`: `[214, 2928, 1403, 3082]` -> `[210, 3084, 1371, 3190]`.
- #20 `equation_isolated` `$$\mathcal{D}(x) = \mathbb{1}\!\left[\,\mathrm{scTM}(x, \mathrm{ESMfold}(x)) \geq 0.5\,...`: `[214, 3092, 1403, 3233]` -> `[210, 3256, 1371, 3344]`.
- #21 `text_block` `Key idea: staying on the manifold means no chirality drift — mirror folds vanish entire...`: `[82, 3307, 1474, 3355]` -> `[172, 3386, 1355, 3478]`.
- #22 `title` `4  SAMPLING ALGORITHM`: `[139, 3468, 1049, 3503]` -> `[169, 3589, 1000, 3690]`.
- #23 `code_txt` `# FoldFlow.sample — generates a single backbone def sample(model, n_res, n_steps=20):  ...`: `[215, 3565, 1403, 3964]` -> `[172, 3724, 1410, 4139]`.
- #24 `title` `5  RESULTS — UNCONDITIONAL DESIGN`: `[1509, 1055, 2168, 1330]` -> `[1544, 1170, 2203, 1381]`.
- #25 `table_caption` `↳ table 1 · designability vs sampling cost · 256 aa`: `[1486, 1320, 2134, 1393]` -> `[1569, 1394, 2154, 1438]`.
- #26 `table` `METHOD DES↑ DIV↑ s/sample ProteinSGM 42.1 0.61 128 Chroma 61.4 0.74 82 Genie 68.7 0.78 ...`: `[1534, 1341, 2323, 1781]` -> `[1547, 1445, 2367, 1857]`.
- #27 `title` `6  SAMPLE BACKBONE · 142 AA`: `[1451, 1889, 2277, 1988]` -> `[1544, 1970, 2311, 2122]`.
- #28 `figure_caption` `↑ FIG 2 — recovered backbone · designable in single ESMfold pass. α-helix 1, α-helix 2,...`: `[1590, 2453, 2267, 2486]` -> `[1605, 2556, 2309, 2597]`.
- #29 `title` `7  ABLATION`: `[1466, 2655, 1963, 2754]` -> `[1544, 2733, 1978, 2834]`.
- #30 `table_caption` `↳ table 2 · ablation on the 142-aa val split`: `[1491, 2789, 2046, 2865]` -> `[1569, 2861, 2068, 2905]`.
- #31 `table` `VARIANT DES DIV Euclidean FM 68.1 0.79 + SE(3) frames 76.4 0.82 + exp-map step 81.2 0.8...`: `[1534, 2749, 2323, 3133]` -> `[1547, 2912, 2367, 3266]`.
- #32 `text_block` `"We don't denoise atoms. We follow geodesics on shapes." — scribbled in margin, page 142`: `[1435, 3306, 2402, 3573]` -> `[1495, 3377, 2419, 3637]`.
- #33 `title` `8  CONTRIBUTIONS`: `[1461, 3589, 2135, 3644]` -> `[1544, 3716, 2184, 3817]`.
- #34 `text_block` `First flow matching directly on the SE(3)^N manifold for proteins. 14× sampling speedup...`: `[1541, 3685, 2327, 4045]` -> `[1546, 3844, 2368, 4214]`.
- #35 `title` `9  THINGS THAT STILL DON'T WORK`: `[1462, 4203, 2230, 4243]` -> `[1544, 4315, 2281, 4467]`.
- #36 `text_block` `Membrane proteins (TM domains) remain underrepresented in PDB. Sequence design is deleg...`: `[1542, 4298, 2328, 4479]` -> `[1546, 4481, 2368, 4755]`.
- #37 `title` `10  READING LIST`: `[1509, 4743, 2088, 4778]` -> `[1544, 4856, 2105, 4956]`.
- #38 `reference` `[1] Watson et al. RFdiffusion. Nature 23.`: `[1509, 4743, 2324, 4977]` -> `[1546, 4987, 2032, 5031]`.
- #39 `reference` `[2] Ingraham et al. Chroma. Nature 23.`: `[1439, 4780, 2078, 4918]` -> `[1546, 4987, 2345, 5070]`.
- #40 `reference` `[3] Lin et al. ESMfold. Science 23.`: `[1601, 4830, 2078, 4875]` -> `[1697, 5026, 2102, 5070]`.
- #41 `reference` `[4] Lipman et al. Flow matching. ICLR 23.`: `[1440, 4780, 2078, 4918]` -> `[1546, 5026, 2353, 5108]`.
- #42 `reference` `[5] Bose et al. SE(3) FM. ICML 24.`: `[1695, 4827, 2078, 4879]` -> `[1799, 5064, 2230, 5108]`.
- #43 `reference` `[6] Yim et al. FrameFlow. NeurIPS 23.`: `[1439, 4780, 2078, 4918]` -> `[1546, 5064, 2342, 5147]`.
- #44 `reference` `[7] Jumper et al. AlphaFold-2. Nature 21.`: `[1748, 4942, 2303, 4970]` -> `[1893, 5103, 2358, 5147]`.
- #45 `header` `ICML 2029 ✦ VIENNA ✦ POSTER #2218 | Wed Jul 25 · 17:00–19:00 · Exhibit Hall B · Aisle 4...`: `[82, 4915, 2466, 5264]` -> `[121, 5213, 2419, 5481]`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Cleared existing bbox values: `0`.

Verification:

- Report: `reports/pdb_academic_conference019_visual_v558.json`.
- Visual outline checks: `cover_audit_academic_conference019_v558/full_scaled.jpg`, `cover_audit_academic_conference019_v558/crop_0.jpg` ... `cover_audit_academic_conference019_v558/crop_4.jpg`.
- Latest token after this repair: `20260609_academic_conference019_visual_v558`.

## 20260609_academic_conference020_visual_v559

Scope:

- Targeted visual repair for `01_academic/06_conference_poster/conference_poster_020_CoRL_GraspBOOM`.
- User-visible issue: after v554, this comic-style poster still had hero/KPI/method/table/reference/footer boxes visibly shifted or matched to the wrong poster region.

Token:

- v559: `20260609_academic_conference020_visual_v559`

Method:

- Added `scripts/fix_academic_conference020_visual_v559.py`.
- Rebuilt this single case from visually checked Chrome DOM element/range coordinates on the released clean PNG (`2481x5238`).
- Subtracted the centered HTML body left margin before scaling, because this poster uses `body { margin: 0 auto; }`.
- Split table captions from table grids; split the inline references by their numbered text ranges. No other conference-poster cases were modified in this pass.

Case-level changes:

- `01_academic/06_conference_poster/conference_poster_020_CoRL_GraspBOOM`: rebuilt `47` existing bbox coordinate sets; boxed `47/47`; no-bbox `0`; low-similarity `0`.

Per-annotation changes:

- #0 `header` `VOL. XII | NO. 09 / 2218 ★ THE AMAZING CoRL 2029 ★ MUNICH ★ POSTER #2218 ★ FREE WED 13 NOV ·...`: `[0, 8, 2481, 77]` -> `[72, 72, 2409, 210]`.
- #1 `title` `GRASPBOOM! TACTILE-VISION PRETRAIN`: `[78, 210, 1102, 534]` -> `[72, 217, 1048, 690]`.
- #2 `text_block` `A self-supervised tactile-visual pretraining recipe that produces a generalist robot manipul...`: `[151, 734, 1444, 789]` -> `[100, 713, 1457, 865]`.
- #3 `text_block` `Marco Bellini¹ · Aiyana Hartwell² · Jin-Soo Park¹,³ · Camila Restrepo⁴ · Felix Adesanya⁵ · H...`: `[0, 901, 1646, 941]` -> `[72, 915, 1365, 962]`.
- #4 `text_block` `¹ Stanford IPRL · ² TU München / MIRMI · ³ KAIST · ⁴ Toyota Research Institute · ⁵ Universit...`: `[0, 944, 1284, 998]` -> `[72, 965, 1154, 1008]`.
- #5 `title` `TL;DR — ONE NET FOR EVERY GRIP! BOOM!`: `[1512, 290, 1831, 415]` -> `[1514, 234, 2444, 1061]`.
- #6 `text_block` `Vision tells you where. Touch tells you when. We pretrain on both — and the policy generalis...`: `[1553, 499, 2269, 571]` -> `[1557, 509, 2322, 605]`.
- #7 `text_block` `UNSEEN OBJECT GRASP 92.4%. REAL OBJECT CLASSES 412. SHOTS / NEW TASK 10. vs OCTO-V2 BASELINE...`: `[29, 944, 2444, 1234]` -> `[68, 1036, 2413, 1288]`.
- #8 `title` `1  THE PROBLEM — GRASPING IS STILL HARD!`: `[47, 1324, 1238, 1379]` -> `[125, 1363, 1235, 1446]`.
- #9 `text_block` `Generalist manipulation policies (Octo, OpenVLA, RT-2-X) have made enormous strides on scrip...`: `[120, 1357, 1348, 1575]` -> `[125, 1469, 1347, 1627]`.
- #10 `text_block` `We argue this gap is fundamentally a missing-modality problem. Existing pretraining corpora ...`: `[66, 1579, 1427, 1664]` -> `[125, 1648, 1297, 1750]`.
- #11 `text_block` `Force-blind: visual policies grip soft objects with up to 4× excess force. Slip-prone: 31% o...`: `[123, 1655, 1283, 1849]` -> `[125, 1771, 1358, 1891]`.
- #12 `title` `2  THE GRASPBOOM PIPELINE`: `[121, 1865, 951, 1884]` -> `[125, 2022, 847, 2105]`.
- #13 `text_block` `Pipeline: SEE (3 RGB cams + depth) → FEEL (GelSight tactile pads) → FUSE (cross-modal transf...`: `[214, 2161, 1271, 2228]` -> `[125, 2129, 1358, 2326]`.
- #14 `figure_caption` `FIG 1 ▸ FIVE-STAGE TACTILE-VISION PIPELINE — END-TO-END 47 ms / STEP`: `[268, 2232, 1255, 2318]` -> `[330, 2333, 1153, 2364]`.
- #15 `text_block` `Two GelSight tactile pads stream 24 Hz force images concurrently with 3 RGB-D cameras. A cro...`: `[66, 2316, 1464, 2399]` -> `[125, 2416, 1324, 2519]`.
- #16 `title` `3  METHOD — CONTRASTIVE TOUCH-VISION`: `[66, 2624, 1149, 2678]` -> `[125, 2664, 1189, 2747]`.
- #17 `text_block` `For paired (visual, tactile) clips (v, τ), we maximise their agreement against a batch of ne...`: `[66, 2624, 1413, 2679]` -> `[125, 2771, 1277, 2802]`.
- #18 `equation_isolated` `$$\mathcal{L}_{TV} = -\log\!\left[\,\frac{\exp(s(v,\tau)/T)}{\sum_{j} \exp(s(v,\tau_j)/T)}\,...`: `[170, 2711, 1353, 2850]` -> `[125, 2824, 1358, 2969]`.
- #19 `equation_isolated` `$$\mathcal{L}_{DA}(\theta) = \mathbb{E}_{t,a_0,\epsilon} \left\| \epsilon - \epsilon_{\theta...`: `[170, 2867, 1353, 3013]` -> `[125, 2987, 1358, 3140]`.
- #20 `equation_isolated` `$$\mathcal{L}_{\text{BOOM}} = \mathcal{L}_{DA} + \lambda \cdot \mathcal{L}_{TV} + \mu \cdot ...`: `[170, 3030, 1353, 3169]` -> `[125, 3157, 1358, 3302]`.
- #21 `text_block` `Key insight: the tactile branch acts as a distillation prior on the visual encoder — even wh...`: `[29, 3155, 1465, 3302]` -> `[125, 3320, 1347, 3387]`.
- #22 `title` `4  SAMPLING ALGORITHM`: `[121, 3364, 857, 3384]` -> `[125, 3532, 760, 3615]`.
- #23 `code_txt` `# GraspBOOM rollout — runs at 20 Hz on Franka Panda def act(obs, model, k=8):     z = model....`: `[170, 3492, 1353, 3794]` -> `[125, 3639, 1358, 3953]`.
- #24 `text_block` `Inference: 47 ms / step on a single RTX-4090. The whole stack fits in 6.4 GB.`: `[170, 3805, 1073, 3835]` -> `[125, 3965, 1066, 3996]`.
- #25 `title` `5  RESULTS — 412 OBJECTS`: `[1411, 1333, 2233, 1378]` -> `[1506, 1363, 2196, 1446]`.
- #26 `table_caption` `▸ TBL 1 · GRASP SUCCESS ON YCB-412 (REAL ROBOT)`: `[1448, 1412, 2161, 1482]` -> `[1506, 1469, 2125, 1504]`.
- #27 `table` `METHOD SEEN UNSEEN SLIP↓ RT-2-X 82.0 61.4 12.1 OpenVLA 85.6 68.2 9.8 Octo-V2 88.1 74.0 8.7 R...`: `[1495, 1410, 2311, 1846]` -> `[1506, 1504, 2356, 1924]`.
- #28 `title` `6  SUCCESS VS DEMO COUNT`: `[1408, 2020, 2122, 2075]` -> `[1506, 2060, 2224, 2143]`.
- #29 `figure_caption` `FIG 2 ▸ GRASP % VS DEMOS / TASK — GRASPBOOM CONVERGES IN 10 SHOTS`: `[1448, 2501, 2360, 2568]` -> `[1551, 2558, 2311, 2589]`.
- #30 `title` `7  ABLATION`: `[1528, 2698, 1878, 2718]` -> `[1506, 2755, 1841, 2838]`.
- #31 `table_caption` `▸ TBL 2 · WHICH PIECE MATTERS?`: `[1448, 2714, 1842, 2776]` -> `[1506, 2861, 1905, 2896]`.
- #32 `table` `VARIANT SUCC SLIP Vision only 74.1 9.4 + tactile input 82.6 5.3 + contrastive L_TV 87.4 3.8 ...`: `[1495, 2746, 2311, 3132]` -> `[1506, 2896, 2356, 3264]`.
- #33 `text_block` `VISION SAYS WHERE. TOUCH SAYS WHEN! — OVERHEARD AT CORL POSTER NIGHT`: `[1448, 3329, 2352, 3444]` -> `[1453, 3382, 2409, 3624]`.
- #34 `title` `8  CONTRIBUTIONS`: `[1431, 3627, 2026, 3661]` -> `[1506, 3730, 1999, 3813]`.
- #35 `text_block` `First tactile-vision pretraining recipe at 3.4 M episodes scale. +18 pp over Octo-V2 on unse...`: `[1452, 3627, 2352, 3876]` -> `[1506, 3836, 2356, 4041]`.
- #36 `title` `9  WHAT STILL FAILS`: `[1432, 4011, 2060, 4031]` -> `[1506, 4172, 2027, 4255]`.
- #37 `text_block` `Transparent and reflective objects degrade vision by 14%. GelSight pads wear out after ~40 h...`: `[1453, 4092, 2352, 4318]` -> `[1506, 4279, 2356, 4441]`.
- #38 `title` `10  REFERENCES`: `[1432, 4501, 1939, 4519]` -> `[1506, 4572, 1901, 4655]`.
- #39 `reference` `1 Brohan et al. RT-2. CoRL 23.`: `[1498, 4501, 2307, 4623]` -> `[1506, 4682, 1842, 4707]`.
- #40 `reference` `2 Octo Team. Octo. arXiv 24.`: `[177, 2133, 633, 2153]` -> `[1842, 4682, 2166, 4707]`.
- #41 `reference` `3 Kim et al. OpenVLA. CoRL 24.`: `[1506, 3162, 1605, 3176]` -> `[1506, 4682, 2298, 4742]`.
- #42 `reference` `4 Yuan et al. GelSight. RSS 17.`: `[1876, 3162, 1965, 3176]` -> `[1727, 4717, 2077, 4742]`.
- #43 `reference` `5 Chi et al. Diffusion policy. RSS 23.`: `[1506, 3162, 2304, 3200]` -> `[1506, 4717, 2304, 4778]`.
- #44 `reference` `6 Calandra et al. Touch-vision learning. ICRA 18.`: `[1870, 3186, 2094, 3200]` -> `[1681, 4753, 2212, 4778]`.
- #45 `reference` `7 Calli et al. YCB benchmark. ICAR 15.`: `[1505, 4786, 1775, 4810]` -> `[1506, 4753, 2346, 4811]`.
- #46 `header` `★ CoRL 2029 ▌ MUNICH ▌ POSTER #2218 ★ | Wed Nov 13 · 16:00–18:30 · Hall D · Bay 14 · Spotlig...`: `[114, 4693, 2367, 4899]` -> `[72, 4895, 2409, 5169]`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Cleared existing bbox values: `0`.

Verification:

- Report: `reports/pdb_academic_conference020_visual_v559.json`.
- Visual cover check: `cover_audit_academic_conference020_v559/11_conference_poster_020_CoRL_GraspBOOM_cover.jpg`.
- Dry-run outline checks: `/tmp/pdb_conference020_v559_dry/proposed_crop_0.jpg` ... `/tmp/pdb_conference020_v559_dry/proposed_crop_3.jpg`.
- Latest token after this repair: `20260609_academic_conference020_visual_v559`.

## 20260609_academic_conference021_visual_v560

Scope:

- Targeted visual repair for `01_academic/06_conference_poster/conference_poster_021_CVPR_Video_Diffusion`.
- User-visible issue: after v554, this three-column CVPR poster still had boxes shifted in the header, architecture SVG, formula stack, chart/caption, and footer.

Token:

- v560: `20260609_academic_conference021_visual_v560`

Method:

- Added `scripts/fix_academic_conference021_visual_v560.py`.
- Rebuilt this single case from visually checked Chrome DOM element/range coordinates on the released clean PNG (`2481x3509`).
- Subtracted the centered HTML body left margin before scaling, because this poster uses `body { margin: 0 auto; }`.
- Used component boxes for the architecture SVG, chart+caption region, tables, and footer; used text-range boxes for headings/paragraphs/formulas. No other conference-poster cases were modified in this pass.

Case-level changes:

- `01_academic/06_conference_poster/conference_poster_021_CVPR_Video_Diffusion`: rebuilt `32` existing bbox coordinate sets; boxed `32/32`; no-bbox `0`; low-similarity `0`.

Per-annotation changes:

- #0 `header` `CVPR 2029 ★ HIGHLIGHT`: `[2008, 244, 2334, 257]` -> `[2055, 130, 2325, 275]`.
- #1 `title` `VideoFlow-DiT: Cascaded Diffusion Transformers for Minute-Long Video Generation with Tempora...`: `[181, 243, 2097, 300]` -> `[142, 112, 2128, 408]`.
- #2 `text_block` `Yifei Chen¹, Sarah O'Brien¹, Hiroshi Tanaka², Wei Zhang³, Maria Santos¹,⁴, David Kim¹`: `[53, 277, 1689, 298]` -> `[142, 428, 1536, 474]`.
- #3 `text_block` `¹Stanford AI Lab • ²University of Tokyo • ³Tsinghua University • ⁴Google DeepMind`: `[186, 475, 1269, 514]` -> `[142, 495, 1270, 536]`.
- #4 `title` `Key Results`: `[94, 656, 319, 688]` -> `[98, 655, 317, 686]`.
- #5 `text_block` `71.4 FVD↓. +18% vs SOTA. 60s video length. 512² resolution. 2.3× faster sampling.`: `[139, 656, 1827, 756]` -> `[95, 690, 1828, 785]`.
- #6 `title` `1. Motivation`: `[102, 873, 430, 916]` -> `[104, 870, 429, 920]`.
- #7 `text_block` `Diffusion-based video generators (Sora, Veo, KLING) achieve photo-real frames but suffer fro...`: `[102, 879, 792, 1078]` -> `[104, 956, 748, 1117]`.
- #8 `text_block` `Identity drift: subjects morph between shots. Motion stuttering: low-rank temporal attention...`: `[139, 1041, 738, 1356]` -> `[145, 1135, 748, 1396]`.
- #9 `text_block` `We propose VideoFlow-DiT, a cascaded DiT that decouples spatial generation from temporal flo...`: `[145, 1362, 754, 1510]` -> `[104, 1406, 748, 1567]`.
- #10 `title` `2. Contributions`: `[100, 1684, 529, 1720]` -> `[104, 1674, 525, 1724]`.
- #11 `text_block` `Cascaded DiT with shared spatial encoder + lightweight temporal flow head. Long-context RoPE...`: `[184, 1683, 754, 2016]` -> `[145, 1759, 748, 2158]`.
- #12 `title` `3. Take-Aways`: `[101, 2129, 536, 2150]` -> `[104, 2256, 441, 2306]`.
- #13 `text_block` `Decoupling spatial & temporal saves 4.7× memory. RoPE-3D scales to 1500 frames without retra...`: `[184, 2344, 729, 2465]` -> `[145, 2342, 748, 2562]`.
- #14 `title` `4. Architecture`: `[817, 836, 1269, 941]` -> `[867, 870, 1266, 920]`.
- #15 `text_block` `Pipeline: Text Prompt (T5-XXL) → Cascaded DiT (24 layers, with Spatial Self-Attn / Cross-Att...`: `[2066, 136, 2292, 183]` -> `[867, 956, 1620, 1228]`.
- #16 `figure_caption` `Figure 1. VideoFlow-DiT pipeline: cascaded spatial-temporal decoupling.`: `[817, 1242, 1664, 1262]` -> `[881, 1234, 1607, 1301]`.
- #17 `title` `5. Method`: `[817, 1357, 1114, 1466]` -> `[867, 1394, 1112, 1444]`.
- #18 `title` `Cascaded Loss Formulation`: `[817, 1457, 1313, 1502]` -> `[867, 1482, 1312, 1520]`.
- #19 `equation_isolated` `$$\mathcal{L}_{\text{diff}} = \mathbb{E}_{t,\epsilon}\!\left[\,\| v_{\theta}(x_t, t, c) - v_...`: `[913, 1499, 1574, 1581]` -> `[867, 1537, 1620, 1678]`.
- #20 `equation_isolated` `$$\mathcal{L}_{\text{id}} = 1 - \cos\!\left(\mathrm{DINO}(\hat{x}_0^{(t)}),\, \mathrm{DINO}(...`: `[913, 1647, 1574, 1734]` -> `[867, 1692, 1620, 1837]`.
- #21 `equation_isolated` `$$\mathcal{L} = \mathcal{L}_{\text{diff}} + \lambda_1 \cdot \mathcal{L}_{\text{id}} + \lambd...`: `[913, 1800, 1574, 1882]` -> `[867, 1851, 1620, 1992]`.
- #22 `title` `RoPE-3D`: `[817, 1818, 881, 1840]` -> `[867, 2013, 1012, 2050]`.
- #23 `text_block` `3D rotary embedding factorises temporal and spatial dims independently, allowing extrapolati...`: `[863, 1982, 1624, 2146]` -> `[867, 2063, 1620, 2183]`.
- #24 `title` `6. Main Results`: `[1689, 836, 2121, 941]` -> `[1739, 870, 2118, 920]`.
- #25 `table` `Method FVD↓ FID↓ CLIP↑ Sec CogVideoX-5B 112.8 54.2 31.2 10 Open-Sora 2.0 98.6 48.7 32.0 15 V...`: `[1719, 917, 2337, 1314]` -> `[1739, 956, 2383, 1369]`.
- #26 `table_caption` `Table 1. UCF-101+MSR-VTT zero-shot evaluation (lower FVD/FID better).`: `[1689, 1305, 2361, 1371]` -> `[1764, 1381, 2359, 1448]`.
- #27 `title` `7. FVD vs Length`: `[1689, 1507, 2140, 1612]` -> `[1739, 1541, 2139, 1591]`.
- #28 `figure_caption` `Figure 2. FVD remains stable as length increases. Curves: Sora-mini, CogVideoX, VideoFlow-Di...`: `[1689, 1806, 2352, 1871]` -> `[1739, 1627, 2383, 1885]`.
- #29 `title` `8. Ablation`: `[1689, 1945, 2012, 2050]` -> `[1739, 1979, 2011, 2029]`.
- #30 `table` `Variant FVD↓ Δ Base DiT 112.8 — + Temporal Flow 96.4 −16.4 + RoPE-3D 84.0 −28.8 + Identity L...`: `[1719, 1981, 2337, 2321]` -> `[1739, 2064, 2383, 2418]`.
- #31 `header` `CVPR 2029 | Honolulu, HI · June 16–20, 2029 | Paper ID #4827 | 📧 yifei@stanford.edu | 🌐 vide...`: `[102, 2522, 792, 2603]` -> `[59, 2633, 2422, 2846]`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Cleared existing bbox values: `0`.

Verification:

- Report: `reports/pdb_academic_conference021_visual_v560.json`.
- Visual cover check: `cover_audit_academic_conference021_v560/11_conference_poster_021_CVPR_Video_Diffusion_cover.jpg`.
- Dry-run outline checks: `/tmp/pdb_conference021_v560_dry/proposed_crop_0.jpg` ... `/tmp/pdb_conference021_v560_dry/proposed_crop_3.jpg`.
- Latest token after this repair: `20260609_academic_conference021_visual_v560`.

## 20260609_academic_conference023_visual_v561

Scope:

- Targeted visual repair for `01_academic/06_conference_poster/conference_poster_023_ACL_Multilingual`.
- User-visible issue: this ACL poster still had two existing GT annotations without bbox (#25/#28), plus low-sim/mismatched figure-caption regions and reference boxes stacked on the heading.

Token:

- v561: `20260609_academic_conference023_visual_v561`

Method:

- Added `scripts/fix_academic_conference023_visual_v561.py`.
- Rebuilt this single case from visually checked Chrome DOM element/range coordinates on the released clean PNG (`2481x4319`).
- Subtracted the centered HTML body left margin before scaling, because this poster uses `body { margin: 0 auto; }`.
- Used component boxes for SVG figures, chart+caption regions, tables, code, and footer; split dark-card references by visible line. No other conference-poster cases were modified in this pass.

Case-level changes:

- `01_academic/06_conference_poster/conference_poster_023_ACL_Multilingual`: rebuilt `44` bbox coordinate slots; boxed `44/44`; no-bbox `0`; low-similarity `0`; unmatched `0`.
- Added bbox to existing GT annotations: `#25`, `#28`.

Per-annotation changes:

- #0 `header` `ACL 2029 ★ BEST PAPER AWARD`: `[1836, 230, 2286, 259]` -> `[1920, 130, 2295, 282]`.
- #1 `title` `PolyAlign: Universal Cross-Lingual LLM Alignment across 127 Languages via Contrastive Anchor...`: `[181, 155, 1578, 286]` -> `[142, 121, 1643, 410]`.
- #2 `text_block` `Closing the alignment gap between high- and low-resource languages without parallel SFT data`: `[46, 439, 2107, 452]` -> `[183, 425, 1929, 472]`.
- #3 `text_block` `Mikhail Zelensky¹, Priya Raghavan², Amara Boateng³, Léa Fournier⁴, Yuki Kobayashi⁵, Daniel N...`: `[186, 599, 2134, 637]` -> `[142, 624, 2171, 663]`.
- #4 `text_block` `¹Carnegie Mellon LTI • ²Allen Institute for AI • ³Masakhane NLP • ⁴Inria Paris • ⁵RIKEN AIP`: `[186, 655, 1297, 693]` -> `[142, 682, 1299, 722]`.
- #5 `title` `KEY GAINS`: `[104, 845, 295, 1021]` -> `[109, 851, 189, 1017]`.
- #6 `text_block` `127 Languages Aligned. +24.7 Δ XCOPA (low-res). −81% Hallucination ↓. 0.92 Cross-Ling Consis...`: `[158, 881, 2044, 982]` -> `[260, 870, 2072, 991]`.
- #7 `title` `1  Motivation`: `[104, 1120, 464, 1191]` -> `[109, 1124, 463, 1183]`.
- #8 `text_block` `Frontier LLMs are 100× better in English than in low-resource languages like Yoruba, Quechua...`: `[150, 1163, 722, 1392]` -> `[109, 1217, 716, 1446]`.
- #9 `text_block` `Three open problems remain: Data scarcity — 90% of languages lack quality SFT pairs. Anchor ...`: `[151, 1467, 710, 1730]` -> `[109, 1465, 716, 1769]`.
- #10 `text_block` `We replace parallel SFT with contrastive anchor translation in latent space — zero parallel ...`: `[111, 1645, 658, 1939]` -> `[154, 1820, 652, 1975]`.
- #11 `title` `2  Algorithm`: `[181, 2120, 458, 2163]` -> `[109, 2114, 457, 2173]`.
- #12 `code_txt` `Algorithm 1 — PolyAlign Step def polyalign_step(x, π_θ, π_ref):   # 1. Sample 2 languages   ...`: `[186, 2147, 706, 2641]` -> `[109, 2207, 716, 2778]`.
- #13 `text_block` `Complexity: O(B·L·d) per step, where B=batch, L=seq-len, d=hidden.`: `[105, 2794, 719, 2831]` -> `[109, 2796, 716, 2863]`.
- #14 `title` `3  Contributions`: `[105, 2794, 653, 2822]` -> `[109, 2975, 561, 3034]`.
- #15 `text_block` `Contrastive Anchor Translation: zero-parallel cross-lingual alignment. 127-language benchmar...`: `[150, 3069, 698, 3318]` -> `[154, 3068, 716, 3405]`.
- #16 `title` `4  References`: `[119, 3414, 499, 3462]` -> `[109, 3552, 487, 3611]`.
- #17 `reference` `[1] Lin et al. Few-shot learning with multilingual LMs. EMNLP 2022.`: `[119, 3414, 499, 3462]` -> `[109, 3645, 716, 3711]`.
- #18 `reference` `[2] Üstün et al. Aya: open-source multilingual LM. ACL 2024.`: `[119, 3414, 499, 3462]` -> `[109, 3715, 716, 3781]`.
- #19 `reference` `[3] Bai et al. Constitutional AI. Anthropic 2022.`: `[155, 3632, 648, 3662]` -> `[109, 3785, 623, 3816]`.
- #20 `reference` `[4] Conneau et al. XLM-R. ACL 2020.`: `[155, 3666, 551, 3696]` -> `[109, 3820, 522, 3851]`.
- #21 `reference` `[5] Devlin et al. BERT. NAACL 2019.`: `[155, 3699, 539, 3729]` -> `[109, 3855, 509, 3886]`.
- #22 `reference` `[6] Zhang et al. BLOOM. arXiv 2022.`: `[155, 3733, 541, 3763]` -> `[109, 3890, 511, 3921]`.
- #23 `reference` `[7] Workshop et al. Glot500. ACL 2023.`: `[155, 3767, 572, 3797]` -> `[109, 3925, 544, 3956]`.
- #24 `title` `5  Language Coverage`: `[789, 1085, 1432, 1166]` -> `[842, 1124, 1430, 1183]`.
- #25 `text_block` `Universal Anchor Space (d=1024) covers 9 typological families: Indo-Euro 32 (en de fr es ru ...`: `None` -> `[842, 1217, 1648, 1450]`.
- #26 `figure_caption` `Figure 1. Language coverage across 9 typological families, all aligned to a single anchor sp...`: `[789, 1394, 1654, 1474]` -> `[842, 1457, 1648, 1520]`.
- #27 `title` `6  PolyAlign Architecture`: `[917, 1623, 1537, 1666]` -> `[842, 1615, 1534, 1674]`.
- #28 `text_block` `Pipeline: Input Prompt ("Translate help" → 127 langs) → ① Pivot Translate (π_ref → ℓ_a, π_re...`: `None` -> `[842, 1708, 1648, 1941]`.
- #29 `figure_caption` `Figure 2. PolyAlign 3-step pipeline: pivot translate → anchor encode → contrastive align.`: `[905, 1861, 1601, 1921]` -> `[848, 1948, 1643, 2011]`.
- #30 `title` `7  Loss Formulation`: `[843, 1956, 1431, 1976]` -> `[842, 2106, 1378, 2165]`.
- #31 `equation_isolated` `$$\mathcal{L}_{\text{anc}} = -\mathbb{E}_{(\ell_a,\ell_b)\sim U}\!\left[\,\log\frac{\exp(z_a...`: `[890, 2134, 1600, 2257]` -> `[842, 2199, 1648, 2379]`.
- #32 `equation_isolated` `$$\mathcal{L}_{\text{reg}} = \max\!\left(0,\,\epsilon - \sqrt{\mathrm{Var}(z_i)}\right),\qua...`: `[890, 2321, 1600, 2403]` -> `[842, 2394, 1648, 2533]`.
- #33 `equation_isolated` `$$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{anc}} + \lambda_1 \cdot \mathcal{L}_{\text...`: `[890, 2468, 1600, 2550]` -> `[842, 2548, 1648, 2687]`.
- #34 `title` `8  Cross-Lingual Heatmap`: `[1720, 1085, 2206, 1166]` -> `[1775, 1124, 2217, 1228]`.
- #35 `figure_caption` `Figure 3. 8×10 transfer accuracy heatmap (diagonal = mono-lingual upper bound). Source → Tar...`: `[1720, 1662, 2381, 1682]` -> `[1775, 1266, 2381, 1715]`.
- #36 `title` `9  Main Results`: `[1720, 1662, 2210, 1747]` -> `[1775, 1810, 2183, 1869]`.
- #37 `table` `Model Hi-Res Mid-Res Lo-Res Avg mT5-XXL 72.3 54.1 32.8 53.1 XGLM-7.5B 74.1 56.8 35.6 55.5 BL...`: `[1753, 1826, 2335, 2359]` -> `[1775, 1903, 2381, 2458]`.
- #38 `table_caption` `Table 1. XCOPA + Belebele + FLORES-MT averaged over 127 langs grouped by resource tier.`: `[1788, 2375, 2368, 2444]` -> `[1786, 2470, 2369, 2532]`.
- #39 `title` `10  Per-Family Bar`: `[1780, 2509, 2253, 2537]` -> `[1775, 2627, 2228, 2686]`.
- #40 `figure_caption` `Figure 4. Per-family XCOPA gains; largest gain on Niger-Congo (+22.4). Indo-Euro (IE), Sino-...`: `[1787, 2965, 2367, 3030]` -> `[1775, 2720, 2381, 3028]`.
- #41 `title` `11  Ablation`: `[1846, 3130, 2075, 3173]` -> `[1775, 3123, 2075, 3182]`.
- #42 `table` `Component Avg Δ Base mLLaMA 61.2 — + Pivot Trans 67.5 +6.3 + Anchor Enc 72.1 +10.9 + Anti-Co...`: `[1753, 3087, 2335, 3428]` -> `[1775, 3216, 2381, 3572]`.
- #43 `header` `ACL 2029 — Vienna, Austria | Best Paper · Multilingual NLP Track · Wed July 18, 11:00 | CMU ...`: `[102, 3871, 762, 4010]` -> `[59, 4038, 2422, 4260]`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `2` (`#25`, `#28`).
- Cleared existing bbox values: `0`.

Verification:

- Report: `reports/pdb_academic_conference023_visual_v561.json`.
- Visual cover check: `cover_audit_academic_conference023_v561/11_conference_poster_023_ACL_Multilingual_cover.jpg`.
- Dry-run outline checks: `/tmp/pdb_conference023_v561_dry/proposed_crop_0.jpg` ... `/tmp/pdb_conference023_v561_dry/proposed_crop_3.jpg`.
- Latest token after this repair: `20260609_academic_conference023_visual_v561`.

## 20260609_certificate_diploma016017_visual_v562

Scope:

- Targeted visual repair for the two user-reported certificate rows:
  - `10_certificate/01_diploma_transcript/diploma_transcript_016_diploma_transcript_016_Joint_Degree_Certificate`
  - `10_certificate/01_diploma_transcript/diploma_transcript_017_清_华_大_学`
- User-visible issue: both cases were fully boxed by count, but visible labels were still offset/empty in the review app. `diploma_transcript_016` had DOM text hidden under the diagonal certificate band while still receiving bboxes. `diploma_transcript_017` had many line-height bboxes floating above the actual scroll text.

Token:

- v562: `20260609_certificate_diploma016017_visual_v562`

Method:

- Added `scripts/fix_certificate_diploma016017_visual_v562.py`.
- Rebuilt both cases from Chrome DOM text ranges at the released clean-PNG viewport/DPR (`DPR=300/96`).
- Added `elementFromPoint` visibility checks so DOM text covered by the diagonal/clip-path layers is not boxed.
- For `diploma_transcript_017_清_华_大_学`, post-processed DOM boxes against the clean PNG ink pixels to trim vertical line-height padding around visible text.
- Updated `review_data.json`, `review_data.js`, and `index.html` query token.

Case-level changes:

- `diploma_transcript_016_diploma_transcript_016_Joint_Degree_Certificate`: changed `215` existing bbox slots; boxed `223/223` -> `192/223`; no-bbox `0` -> `31`; low-similarity `0`.
  - Cleared existing bbox values for clean-PNG-invisible annotations: `#15`, `#17`, `#18`, `#19`, `#20`, `#21`, `#22`, `#23`, `#24`, `#25`, `#26`, `#27`, `#28`, `#29`, `#30`, `#31`, `#32`, `#33`, `#34`, `#35`, `#36`, `#37`, `#38`, `#39`, `#40`, `#41`, `#42`, `#43`, `#44`, `#45`, `#46`.
  - These cleared items are the SJTU course scores/lower course lines, SJTU seal fragments, and UMich header/info lines that are present in HTML but covered by the central diagonal band in the released clean image.
  - Retained visible top-left fields and visible diagonal-band/bottom-right text bboxes; no GT annotation was added or deleted.
- `diploma_transcript_017_清_华_大_学`: changed `451` existing bbox slots; boxed remains `460/460`; no-bbox remains `0`; low-similarity `0`.
  - Refit the long timeline/course-flow text boxes, including the user-visible Year 3 region around `#204` and neighboring course annotations, using visible DOM ranges plus ink trimming.
  - No existing bbox values were cleared; no GT annotation was added or deleted.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `31` in `diploma_transcript_016_diploma_transcript_016_Joint_Degree_Certificate` only.

Verification:

- Report with full per-index old/new bbox details: `reports/pdb_certificate_diploma016017_visual_v562.json`.
- Visual cover check directory: `cover_audit_certificate_diploma016017_v562/`.
- Key generated cover files:
  - `cover_audit_certificate_diploma016017_v562/11_diploma_transcript_016_diploma_transcript_016_Joint_Degree_Certificate_cover.jpg`
  - `cover_audit_certificate_diploma016017_v562/12_diploma_transcript_017_清_华_大_学_cover.jpg`
- Latest token after this repair: `20260609_certificate_diploma016017_visual_v562`.

## 20260609_academic_conference003_005_visual_v563

Scope:

- Targeted visual repair for the user-requested conference poster cases:
  - `01_academic/06_conference_poster/conference_poster_003_ACL_机器翻译`
  - `01_academic/06_conference_poster/conference_poster_004_MICCAI_医学分割`
  - `01_academic/06_conference_poster/conference_poster_005_ICML_强化学习`
- User-visible issue: these cases had been fully boxed by count after the earlier batch pass, but visible bboxes were still offset, including title lines, formula/table blocks, qualitative/algorithm panels, references, and footer regions.

Token:

- v563: `20260609_academic_conference003_005_visual_v563`

Method:

- Added `scripts/fix_academic_conference003_005_visual_v563.py`.
- Rebuilt the three cases from Chrome DOM coordinates at the released clean-PNG scale (`DPR=300/96`).
- Used exact DOM text ranges for text/title annotations, DOM table rectangles for table annotations, and explicit element rectangles for formulas, algorithm/code boxes, figure-like panels, bullet-list groups, qualitative-result grids, references, and footers.
- Updated `review_data.json`, `review_data.js`, and `index.html` query token.

Case-level changes:

- `conference_poster_003_ACL_机器翻译`: changed `49` existing bbox slots; boxed remains `49/49`; no-bbox remains `0`; low-similarity remains `0`.
  - Refit the ACL logo, two-line main title, subtitle/authors/affiliations, left-column background/method/analysis text, formula blocks `#12/#14`, all result tables, conclusion/future-work block `#47`, and footer `#48`.
  - No GT annotation was added, removed, or newly boxed.
- `conference_poster_004_MICCAI_医学分割`: changed `46` existing bbox slots; boxed remains `46/46`; no-bbox remains `0`; low-similarity `2` -> `0`.
  - Refit the header/logo, title/authors/affiliations, clinical-background/contribution text groups, method architecture panel `#12`, formula blocks `#14/#17`, qualitative-results grid `#24`, benchmark/efficiency/summary tables, conclusion/future-work groups, and footer `#45`.
  - No GT annotation was added, removed, or newly boxed.
- `conference_poster_005_ICML_强化学习`: changed `50` existing bbox slots; boxed remains `50/50`; no-bbox remains `0`; low-similarity remains `0`.
  - Refit the ICML logo, two-line main title, authors/affiliations, problem/setup text, equation `#8`, algorithm/code panel `#13`, right-column environment/baseline/key-insight lists, results/ablation tables, key-findings/conclusion/future-work blocks, references `#44`-`#48`, and footer `#49`.
  - No GT annotation was added, removed, or newly boxed.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `0`.

Verification:

- Report with full per-index old/new bbox details: `reports/pdb_academic_conference003_005_visual_v563.json`.
- Visual dry-run outline checks: `/tmp/pdb_conference003_005_v563_dry/`.
- Visual cover check directory: `cover_audit_academic_conference003_005_v563/`.
- Key generated cover files:
  - `cover_audit_academic_conference003_005_v563/11_conference_poster_003_ACL_机器翻译_cover.jpg`
  - `cover_audit_academic_conference003_005_v563/12_conference_poster_004_MICCAI_医学分割_cover.jpg`
  - `cover_audit_academic_conference003_005_v563/13_conference_poster_005_ICML_强化学习_cover.jpg`
- Latest token after this repair: `20260609_academic_conference003_005_visual_v563`.

## 20260609_academic_conference006_010_visual_v564

Scope:

- Targeted visual repair for the user-requested conference poster cases:
  - `01_academic/06_conference_poster/conference_poster_006_ICLR_生成模型`
  - `01_academic/06_conference_poster/conference_poster_007_KDD_数据挖掘`
  - `01_academic/06_conference_poster/conference_poster_008_EMNLP_情感分析`
  - `01_academic/06_conference_poster/conference_poster_009_ISBI_细胞分割`
  - `01_academic/06_conference_poster/conference_poster_010_中文计算机视觉`
- User-visible issue: these poster cases were boxed by count, but many visible boxes were still offset or mapped to blank/hidden poster areas. The pass was done case by case with visual cover checks.

Token:

- v564: `20260609_academic_conference006_010_visual_v564`

Method:

- Added `scripts/fix_academic_conference006_010_visual_v564.py`.
- Rebuilt the five cases from Chrome DOM coordinates at the released clean-PNG scale (`DPR=300/96`).
- Used exact DOM text ranges for text/title annotations, DOM table rectangles for tables, and explicit element rectangles for formulas, algorithm boxes, architecture/flow diagrams, statistic cards, dependency/figure panels, bullet-list groups, references, logos, and footers.
- For `conference_poster_010_中文计算机视觉`, manually offset the lower reference/logo/footer boxes `#32`-`#38` after visual comparison because the fresh DOM footer sat far below the released clean PNG.
- Cleared two existing bboxes that correspond to HTML text hidden outside/under the released clean PNG instead of forcing boxes onto blank regions.
- Updated `review_data.json`, `review_data.js`, and `index.html` query token.

Case-level changes:

- `conference_poster_006_ICLR_生成模型`: changed `41` existing bbox slots; boxed `41/41` -> `40/41`; no-bbox `0` -> `1`; low-similarity `1` -> `0`.
  - Refit the header/title/authors, abstract/introduction text, equation blocks `#6/#8/#10`, left and right section text, architecture diagram `#14`, result/ablation tables `#21/#24/#29/#31`, figure panel `#26`, references, and footer.
  - Cleared existing bbox for `#32` because `Our model degrades...` is present in HTML but not visible in the released clean PNG.
  - No GT annotation was added or deleted.
- `conference_poster_007_KDD_数据挖掘`: changed `40` existing bbox slots; boxed `40/40` -> `39/40`; no-bbox `0` -> `1`; low-similarity `1` -> `0`.
  - Refit the title/header area, stat-card group `#7`, formula `#12`, method text groups `#13/#18`, list `#15`, algorithm box `#17`, tables `#22/#25/#28`, sidebar detail group `#31`, references, and footer `#39`.
  - Cleared existing bbox for `#29` because `All components contribute...` is present in HTML but hidden by the footer/clean-PNG crop.
  - No GT annotation was added or deleted.
- `conference_poster_008_EMNLP_情感分析`: changed `53` existing bbox slots; boxed remains `53/53`; no-bbox remains `0`; low-similarity `1` -> `0`.
  - Refit the title/header, contribution list `#10`, equation blocks `#13/#15`, body text groups `#14/#16`, dependency panel `#18`, tables `#21/#24/#29/#32/#36`, key-findings list `#27`, conclusion list `#43`, references, and footer `#52`.
  - No GT annotation was added, removed, newly boxed, or cleared.
- `conference_poster_009_ISBI_细胞分割`: changed `31` existing bbox slots; boxed remains `31/31`; no-bbox remains `0`; low-similarity remains `0`.
  - Refit the sidebar header `#0`, title/header and section text, architecture flow `#10`, equation blocks `#13/#16`, metric-card group `#20`, result tables `#18/#21`, references, and sidebar footer/contact `#30`.
  - No GT annotation was added, removed, newly boxed, or cleared.
- `conference_poster_010_中文计算机视觉`: changed `39` existing bbox slots; boxed remains `39/39`; no-bbox remains `0`; low-similarity `4` -> `0`.
  - Refit the Chinese poster header/title/authors/affiliations, callout `#11`, equations `#13/#15`, body/table regions `#19/#23/#27`, figure caption `#25`, references `#32`-`#37`, and logo/footer `#38`.
  - No GT annotation was added, removed, newly boxed, or cleared.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `2` (`conference_poster_006_ICLR_生成模型` `#32`; `conference_poster_007_KDD_数据挖掘` `#29`).

Verification:

- Report with full per-index old/new bbox details: `reports/pdb_academic_conference006_010_visual_v564.json`.
- Visual dry-run outline checks: `/tmp/pdb_conference006_010_v564_dry/`.
- Visual cover check directory: `cover_audit_academic_conference006_010_v564/`.
- Key generated cover files:
  - `cover_audit_academic_conference006_010_v564/11_conference_poster_006_ICLR_生成模型_cover.jpg`
  - `cover_audit_academic_conference006_010_v564/12_conference_poster_007_KDD_数据挖掘_cover.jpg`
  - `cover_audit_academic_conference006_010_v564/13_conference_poster_008_EMNLP_情感分析_cover.jpg`
  - `cover_audit_academic_conference006_010_v564/14_conference_poster_009_ISBI_细胞分割_cover.jpg`
  - `cover_audit_academic_conference006_010_v564/15_conference_poster_010_中文计算机视觉_cover.jpg`
- Latest token after this repair: `20260609_academic_conference006_010_visual_v564`.

## 20260609_academic_conference011_015_visual_v565

Scope:

- Targeted visual repair for the user-requested conference poster cases:
  - `01_academic/06_conference_poster/conference_poster_011_ECCV_3D重建`
  - `01_academic/06_conference_poster/conference_poster_012_CNCC_鸿图大模型`
  - `01_academic/06_conference_poster/conference_poster_013_NAACL_Summarization`
  - `01_academic/06_conference_poster/conference_poster_014_SIGIR_推荐系统`
  - `01_academic/06_conference_poster/conference_poster_015_InterSpeech_语音`
- User-visible issue: the five cases were already fully boxed by count, but visual boxes were offset or mapped to blank regions in several poster sections, especially structured tables/formulas and the lower region of `conference_poster_014_SIGIR_推荐系统`.

Token:

- v565: `20260609_academic_conference011_015_visual_v565`

Method:

- Added `scripts/fix_academic_conference011_015_visual_v565.py`.
- Rebuilt all five cases from Chrome DOM coordinates at the released clean-PNG scale (`DPR=300/96`).
- Used exact DOM text ranges for ordinary text/title annotations, DOM table rectangles for table annotations, and explicit element rectangles for formula boxes, KPI panels, pipeline/figure/code blocks, conclusion lists, reference groups, and footer bands.
- For `conference_poster_014_SIGIR_推荐系统`, manually aligned the clean-PNG lower section `#33`-`#49` after visual inspection because the live DOM placed the bottom row and footer below the released clean image content area.
- Updated `review_data.json`, `review_data.js`, and `index.html` query token.

Case-level changes:

- `conference_poster_011_ECCV_3D重建`: changed `44` existing bbox slots; boxed remains `44/44`; no-bbox remains `0`; low-similarity remains `0`.
  - Refit title/header, introduction/challenge/contribution lists, method formulas `#15/#17/#20`, comparison and ablation/runtime/Tanks tables, conclusion/future-work blocks, and footer `#43`.
  - No GT annotation was added, removed, newly boxed, or cleared.
- `conference_poster_012_CNCC_鸿图大模型`: changed `47` existing bbox slots; boxed remains `47/47`; no-bbox remains `0`; low-similarity `1` -> `0`.
  - Refit the CNCC banner/meta/stamp, headline/deck/authors, KPI strip `#7`, problem/method titles and lists, pipeline `#13/#14`, formula blocks `#18`-`#20`, code block `#23`, experiment/ablation tables, cache-hit chart title/caption, quote, contribution/limitation lists, references, and footer `#46`.
  - No GT annotation was added, removed, newly boxed, or cleared.
- `conference_poster_013_NAACL_Summarization`: changed `38` existing bbox slots; boxed remains `38/38`; no-bbox remains `0`; low-similarity remains `0`.
  - Refit title/header, introduction/challenge text, formula blocks `#11/#14`, evaluation/ablation/transfer/speed/error-analysis tables, conclusion list `#34`, future-work text, and footer `#37`.
  - No GT annotation was added, removed, newly boxed, or cleared.
- `conference_poster_014_SIGIR_推荐系统`: changed `50` existing bbox slots; boxed remains `50/50`; no-bbox remains `0`; low-similarity `5` -> `0`.
  - Refit the title/header/sidebar, formula stack `#13`-`#16`, top/middle tables and notes, online-test/cold-start blocks, and manually moved lower-section boxes `#33`-`#49` back onto the visible efficiency, summary, related-work, reference, and footer content.
  - No GT annotation was added, removed, newly boxed, or cleared.
- `conference_poster_015_InterSpeech_语音`: changed `37` existing bbox slots; boxed remains `37/37`; no-bbox remains `0`; low-similarity remains `0`.
  - Refit title/header, background/challenge/contribution lists, formula blocks `#12/#14/#17`, dataset/results/ablation/low-resource/efficiency tables, lower explanatory lines, summary line, and footer `#36`.
  - No GT annotation was added, removed, newly boxed, or cleared.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `0`.

Verification:

- Report with full per-index old/new bbox details: `reports/pdb_academic_conference011_015_visual_v565.json`.
- Visual dry-run outline checks: `/tmp/pdb_conference011_015_v565_dry/`.
- Visual cover check directory: `cover_audit_academic_conference011_015_v565/`.
- Key generated cover files:
  - `cover_audit_academic_conference011_015_v565/11_conference_poster_011_ECCV_3D重建_cover.jpg`
  - `cover_audit_academic_conference011_015_v565/12_conference_poster_012_CNCC_鸿图大模型_cover.jpg`
  - `cover_audit_academic_conference011_015_v565/13_conference_poster_013_NAACL_Summarization_cover.jpg`
  - `cover_audit_academic_conference011_015_v565/14_conference_poster_014_SIGIR_推荐系统_cover.jpg`
  - `cover_audit_academic_conference011_015_v565/15_conference_poster_015_InterSpeech_语音_cover.jpg`
- Frontend verification: opened rows `161`-`165` with `cb=20260609_academic_conference011_015_visual_v565`; all five rows loaded the v565 token and show `0 no bbox`.
- Latest token after this repair: `20260609_academic_conference011_015_visual_v565`.

## 20260609_academic_conference016_020_visual_v566

Scope:

- Targeted visual repair for the user-requested conference poster cases:
  - `01_academic/06_conference_poster/conference_poster_016_MICCAI_Organ_Segmentation`
  - `01_academic/06_conference_poster/conference_poster_017_CVPR_DriveDiff`
  - `01_academic/06_conference_poster/conference_poster_018_NeurIPS_MoEAtlas`
  - `01_academic/06_conference_poster/conference_poster_019_ICML_FoldFlow`
  - `01_academic/06_conference_poster/conference_poster_020_CoRL_GraspBOOM`
- User-visible issue: cases `016`-`018` were boxed by count but still had visibly shifted boxes on header/affiliation lines, diagram/equation areas, section titles, references, and footer or KPI regions. Cases `019` and `020` had already been manually repaired in v558/v559 and were included in this range for explicit visual re-check.

Token:

- v566: `20260609_academic_conference016_020_visual_v566`

Method:

- Added `scripts/fix_academic_conference016_020_visual_v566.py`.
- Rebuilt `016`-`018` from Chrome DOM coordinates at the released clean-PNG scale (`DPR=300/96`).
- Used explicit DOM element rectangles for poster structure: masthead/header bars, title/deck/authors, KPI strips, h2 section titles, SVG pipeline panels, equations, code blocks, tables, charts, quotes, references, and footers.
- Used exact DOM text ranges for split author/affiliation and individual reference annotations where the GT granularity is smaller than the surrounding card.
- Preserved the existing manually verified v558/v559 coordinates for `conference_poster_019_ICML_FoldFlow` and `conference_poster_020_CoRL_GraspBOOM`; no bbox values changed for those two cases in v566.
- After cover audit, expanded `conference_poster_016_MICCAI_Organ_Segmentation` list bboxes `#7` and `#22` leftward so list bullets are covered as part of the text block.
- Updated `review_data.json`, `review_data.js`, and `index.html` query token.

Case-level changes:

- `conference_poster_016_MICCAI_Organ_Segmentation`: changed `28` existing bbox slots; boxed remains `28/28`; no-bbox remains `0`; low-similarity `1` -> `0`.
  - Refit the MICCAI masthead/title/authors/affiliations, motivation paragraphs and list `#5`-`#7`, architecture SVG/equation/BAM note `#9`-`#11`, ablation table `#13`, qualitative caption `#15`, per-organ and boundary attention titles/caption `#16`-`#18`, comparison title/table `#19/#20`, conclusion title/list `#21/#22`, references `#23`-`#25`, code/contact `#26`, and footer `#27`.
  - Specifically fixed old low-similarity affiliation box `#3` and the old misplaced `#19/#20/#21` lower-section boxes; padded `#7/#22` to cover visible bullets.
  - No GT annotation was added, removed, newly boxed, or cleared.
- `conference_poster_017_CVPR_DriveDiff`: changed `45` existing bbox slots; boxed remains `45/45`; no-bbox remains `0`; low-similarity remains `0`.
  - Refit the topbar `#0/#1`, hero kicker/title/deck/authors/affiliations `#2`-`#6`, KPI strip `#7`, problem/method/pipeline sections, equations `#18/#19`, code block `#22`, results and ablation tables `#25/#30`, chart caption `#28`, quote `#31`, contribution and limitation lists `#33/#35`, references `#36`-`#43`, and footer `#44`.
  - Fixed the previous visual drift where method/ablation titles stretched across columns and reference boxes overlapped the references heading.
  - No GT annotation was added, removed, newly boxed, or cleared.
- `conference_poster_018_NeurIPS_MoEAtlas`: changed `46` existing bbox slots; boxed remains `46/46`; no-bbox remains `0`; low-similarity `7` -> `0`.
  - Refit masthead/title/deck/authors/affiliations `#0`-`#4`, TL;DR panel `#5/#6`, KPI strip `#7`, routing and pipeline sections, equations `#18`-`#20`, code block `#23`, results/ablation tables `#26/#31`, chart caption `#29`, quote `#32`, contribution and limitation lists `#34/#36`, references `#37`-`#44`, and footer `#45`.
  - Specifically fixed the old low-similarity reference annotations `#38`-`#44`, which had been sitting in the middle of the poster instead of the references card.
  - No GT annotation was added, removed, newly boxed, or cleared.
- `conference_poster_019_ICML_FoldFlow`: changed `0` bbox slots; boxed remains `46/46`; no-bbox remains `0`; low-similarity remains `0`.
  - Re-checked using the v558 hard coordinates; no further movement was needed for title/header, method/code/table, references, or footer areas.
  - No GT annotation was added, removed, newly boxed, or cleared.
- `conference_poster_020_CoRL_GraspBOOM`: changed `0` bbox slots; boxed remains `47/47`; no-bbox remains `0`; low-similarity remains `0`.
  - Re-checked using the v559 hard coordinates; no further movement was needed for hero/KPI/method/table/reference/footer areas.
  - No GT annotation was added, removed, newly boxed, or cleared.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `0`.

Verification:

- Report with full per-index old/new bbox details: `reports/pdb_academic_conference016_020_visual_v566.json`.
- Visual dry-run outline checks: `/tmp/pdb_conf016_020_v566_dry_overlay/`.
- Visual cover check directory: `cover_audit_academic_conference016_020_v566_only/`.
- Key generated cover files:
  - `cover_audit_academic_conference016_020_v566_only/01_conference_poster_016_MICCAI_Organ_Segmentation_cover.jpg`
  - `cover_audit_academic_conference016_020_v566_only/02_conference_poster_017_CVPR_DriveDiff_cover.jpg`
  - `cover_audit_academic_conference016_020_v566_only/03_conference_poster_018_NeurIPS_MoEAtlas_cover.jpg`
  - `cover_audit_academic_conference016_020_v566_only/04_conference_poster_019_ICML_FoldFlow_cover.jpg`
  - `cover_audit_academic_conference016_020_v566_only/05_conference_poster_020_CoRL_GraspBOOM_cover.jpg`
- Static validation: `review_data.json` and `review_data.js` parse, `index.html` points to token `20260609_academic_conference016_020_visual_v566`, rows `166`-`170` are all boxed with `0 no bbox`.
- Frontend verification: opened rows `166`-`170` with `cb=20260609_academic_conference016_020_visual_v566`; all five rows loaded the v566 token and show `0 no bbox` in the active case row.
- Latest token after this repair: `20260609_academic_conference016_020_visual_v566`.

## 20260609_academic_conference021_025_visual_v567

Scope:

- Targeted visual repair for the user-requested conference poster cases:
  - `01_academic/06_conference_poster/conference_poster_021_CVPR_Video_Diffusion`
  - `01_academic/06_conference_poster/conference_poster_022_NeurIPS_RLHF`
  - `01_academic/06_conference_poster/conference_poster_023_ACL_Multilingual`
  - `01_academic/06_conference_poster/conference_poster_024_MICCAI_PathDiff`
  - `01_academic/06_conference_poster/conference_poster_025_ICML_GraphX`
- User-visible issue: cases `022`, `024`, and `025` were fully boxed by count but still had visually shifted boxes over the masthead, SVG pipeline/architecture areas, formula stacks, table/caption regions, references, right-column panels, and footer. Cases `021` and `023` had already been manually repaired in v560/v561 and were included in this range for explicit visual re-check.

Token:

- v567: `20260609_academic_conference021_025_visual_v567`

Method:

- Added `scripts/fix_academic_conference021_025_visual_v567.py`.
- Preserved the existing manually verified v560/v561 coordinates for `conference_poster_021_CVPR_Video_Diffusion` and `conference_poster_023_ACL_Multilingual`; no bbox values changed for those two cases in v567.
- Rebuilt `022`, `024`, and `025` from Chrome DOM coordinates at the released clean-PNG scale (`DPR=300/96`).
- Used explicit DOM element rectangles for title bars, badges, KPI strips, section titles, paragraphs, lists, pull quotes, formulas, algorithm/code blocks, SVG pipeline/architecture panels, tables, figure/table captions, references, right-column metric panels, and footers.
- Used exact DOM text ranges for individual reference lines where the GT granularity is smaller than the surrounding references card.
- Used small manual SVG subregion boxes for `conference_poster_022_NeurIPS_RLHF` training-configuration annotations `#25/#26`, because those SVG labels are split across many separate text nodes and are not a single contiguous DOM text range.
- Updated `review_data.json`, `review_data.js`, and `index.html` query token.

Case-level changes:

- `conference_poster_021_CVPR_Video_Diffusion`: changed `0` bbox slots; boxed remains `32/32`; no-bbox remains `0`; low-similarity remains `0`.
  - Re-checked using the v560 hard coordinates; no further movement was needed for title/header, metrics strip, left-column motivation/contribution/take-away blocks, architecture/figure/formula/table areas, or footer.
  - No GT annotation was added, removed, newly boxed, or cleared.
- `conference_poster_022_NeurIPS_RLHF`: changed `47` existing bbox slots; boxed remains `47/47`; no-bbox remains `0`; low-similarity remains `0`.
  - Refit the NeurIPS title badges/header `#0`-`#4`, key-results strip `#5/#6`, left-column motivation/contribution/take-away/reference sections `#7`-`#22`, DPO++ architecture SVG and training-configuration subregions `#23`-`#27`, mathematical formula stack and theorem block `#28`-`#33`, training-curve caption `#34/#35`, right-column main-results table/caption `#36`-`#38`, ability-radar title/caption `#39/#40`, ablation table and length-bias chart/caption `#41`-`#45`, and footer `#46`.
  - Specifically fixed the old visible drift where architecture and training-configuration annotations were tiny or placed far above their SVG text, formula boxes cut through the wrong rows, and right-column captions/table boxes were shifted.
  - No GT annotation was added, removed, newly boxed, or cleared.
- `conference_poster_023_ACL_Multilingual`: changed `0` bbox slots; boxed remains `44/44`; no-bbox remains `0`; low-similarity remains `0`.
  - Re-checked using the v561 hard coordinates; no further movement was needed for header/title, language-coverage and architecture SVG panels, formula blocks, table/chart captions, references, or footer.
  - No GT annotation was added, removed, newly boxed, or cleared.
- `conference_poster_024_MICCAI_PathDiff`: changed `53` existing bbox slots; boxed remains `53/53`; no-bbox remains `0`; low-similarity remains `0`.
  - Refit MICCAI badges/title/header `#0`-`#4`, key-metrics strip `#5/#6`, left-column motivation/quote/contribution/algorithm/dataset/reference sections `#7`-`#25`, architecture and diffusion-process SVG panels/captions `#26`-`#31`, loss formulas `#32`-`#36`, training/qualitative result captions `#37`-`#40`, right-column results/heatmap/ablation/speed/limitations sections `#41`-`#51`, and footer `#52`.
  - Specifically fixed the old visible drift where `#27/#30/#40/#45` had landed on unrelated areas or only a small caption fragment instead of the intended SVG/panel text.
  - No GT annotation was added, removed, newly boxed, or cleared.
- `conference_poster_025_ICML_GraphX`: changed `47` existing bbox slots; boxed remains `47/47`; no-bbox remains `0`; low-similarity remains `0`.
  - Refit the ICML masthead/ribbons/title/deck/byline/affiliation `#0`-`#4`, hero pipeline title and SVG `#5/#6`, main-column motivation/pull-quote/loss/formula/theorem/trade-off/results/ablation-speed sections `#7`-`#27`, right-column at-a-glance/contributions/algorithm/datasets/references/limitations `#28`-`#45`, and footer `#46`.
  - Specifically fixed the old large shifted boxes that covered the wrong side of the poster, and separated the references title `#37` from individual reference lines `#38`-`#43`.
  - No GT annotation was added, removed, newly boxed, or cleared.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `0`.

Verification:

- Report with full per-index old/new bbox details: `reports/pdb_academic_conference021_025_visual_v567.json`.
- Visual dry-run outline checks: `/tmp/pdb_conf021_025_v567_dry_overlay/`.
- Visual cover check directory: `cover_audit_academic_conference021_025_v567_only/`.
- Key generated cover files:
  - `cover_audit_academic_conference021_025_v567_only/01_conference_poster_021_CVPR_Video_Diffusion_cover.jpg`
  - `cover_audit_academic_conference021_025_v567_only/02_conference_poster_022_NeurIPS_RLHF_cover.jpg`
  - `cover_audit_academic_conference021_025_v567_only/03_conference_poster_023_ACL_Multilingual_cover.jpg`
  - `cover_audit_academic_conference021_025_v567_only/04_conference_poster_024_MICCAI_PathDiff_cover.jpg`
  - `cover_audit_academic_conference021_025_v567_only/05_conference_poster_025_ICML_GraphX_cover.jpg`
- Static validation: `review_data.json` and `review_data.js` parse, `index.html` points to token `20260609_academic_conference021_025_visual_v567`, rows `171`-`175` are all boxed with `0 no bbox`.
- Frontend verification: opened rows `171`-`175` with `cb=20260609_academic_conference021_025_visual_v567`; all five rows loaded the v567 token and show `0 no bbox` in the active case row.
- Latest token after this repair: `20260609_academic_conference021_025_visual_v567`.

## 20260609_academic_conference026_030_visual_v568

Scope:

- Targeted visual repair for the user-requested conference poster cases:
  - `01_academic/06_conference_poster/conference_poster_026_KDD_TempoFormer`
  - `01_academic/06_conference_poster/conference_poster_027_SIGIR_RAG`
  - `01_academic/06_conference_poster/conference_poster_028_INTERSPEECH_VoiceClone`
  - `01_academic/06_conference_poster/conference_poster_029_USENIX_KernelGhost`
  - `01_academic/06_conference_poster/conference_poster_030_IAU_ExoCartographer`
- User-visible issue: all five cases were fully boxed by count, but current cover inspection showed many visually shifted boxes: title/header regions spanning unrelated whitespace, pipeline/SVG boxes landing in the wrong panel, formula and table blocks covering neighboring rows, and lower references/footer boxes overlapping the wrong sections.

Token:

- v568: `20260609_academic_conference026_030_visual_v568`

Method:

- Added `scripts/fix_academic_conference026_030_visual_v568.py`.
- Rebuilt `026`-`030` from Chrome DOM coordinates at the released clean-PNG scale (`DPR=300/96`).
- Used explicit DOM element rectangles for top bars, title/deck/author/affiliation lines, KPI strips, section titles, paragraph/list blocks, algorithm/code blocks, SVG pipeline/chart panels, equations, tables, figure/table captions, references, quotes, footnotes, and footers.
- Used exact DOM text ranges for individual reference lines and other annotations whose GT granularity is smaller than the surrounding section.
- Used one thin static header-row bbox in `conference_poster_027_SIGIR_RAG` for `#0`, because the right-hand SIGIR badge is generated by CSS `::before` and has no DOM node.
- Updated `review_data.json`, `review_data.js`, and `index.html` query token.

Case-level changes:

- `conference_poster_026_KDD_TempoFormer`: changed `46` existing bbox slots; boxed remains `46/46`; no-bbox remains `0`; low-similarity remains `0`.
  - Refit the KDD topbar/headline/title/deck/authors/affiliations `#0`-`#4`, metric tile strip `#5`, left-column motivation/contribution/algorithm/reference sections `#6`-`#20`, architecture SVG/caption `#21`-`#23`, loss formulas `#24`-`#27`, dataset/results/ablation/production tables and captions `#28`-`#42`, limits list `#43/#44`, and footer `#45`.
  - Specifically fixed the old pipeline text block `#22`, which had been parked far down in the left references area instead of the architecture card.
  - No GT annotation was added, removed, newly boxed, or cleared.
- `conference_poster_027_SIGIR_RAG`: changed `42` existing bbox slots; boxed remains `42/42`; no-bbox remains `0`; low-similarity remains `0`.
  - Refit the brutalist title area/header row `#0`-`#3`, KPI strip `#4`, left-column problem/pipeline/method/results/curve sections `#5`-`#21`, right-column algorithm/contributions/datasets/ablation/speed/references/limits sections `#22`-`#40`, and footer `#41`.
  - Specifically fixed the old `#10` pipeline box that had been up in the title area, and separated the method formulas `#13`-`#15`, tables `#18/#27/#29/#31`, references `#33`-`#38`, and limits `#39/#40` onto their correct right/left panel positions.
  - No GT annotation was added, removed, newly boxed, or cleared.
- `conference_poster_028_INTERSPEECH_VoiceClone`: changed `55` existing bbox slots; boxed remains `55/55`; no-bbox remains `0`; low-similarity remains `0`.
  - Refit the Interspeech journal header/stamps/title/deck/authors/affiliations `#0`-`#4`, abstract and keywords `#5`-`#7`, left-column introduction/method/equations/pipeline/experiments blocks `#8`-`#29`, right-column results/figures/tables/ablation/conclusion/references `#30`-`#50`, footnotes `#51`-`#53`, and footer `#54`.
  - Specifically fixed the old duplicated/shifted formula boxes and the pipeline text block `#25`, which had been assigned to the wrong right-column region instead of the Figure 1 architecture panel.
  - No GT annotation was added, removed, newly boxed, or cleared.
- `conference_poster_029_USENIX_KernelGhost`: changed `48` existing bbox slots; boxed remains `48/48`; no-bbox remains `0`; low-similarity remains `0`.
  - Refit the ASCII/topline/header/title/deck/authors/affiliations `#0`-`#6`, KPI strip `#7`, left-column threat model/pipeline/method/equations/algorithm/hexdump sections `#8`-`#26`, right-column results/latency/ablation/quote/contributions/limitations/references `#27`-`#46`, and footer `#47`.
  - Specifically fixed old wide shifted boxes around the pipeline/caption `#13/#14`, main-results and ablation tables `#28/#33`, latency caption `#31`, and individual reference lines `#40`-`#46`.
  - No GT annotation was added, removed, newly boxed, or cleared.
- `conference_poster_030_IAU_ExoCartographer`: changed `44` existing bbox slots; boxed remains `44/44`; no-bbox remains `0`; low-similarity remains `0`.
  - Refit the IAU masthead/pretitle/title/deck/authors/affiliations `#0`-`#5`, KPI plate `#6`, left-column problem/pipeline/inverse-model/equation/algorithm sections `#7`-`#21`, right-column model-world figure/table/quote/contributions/caveats/references `#22`-`#39`, footnote/data notes `#40`-`#42`, and footer `#43`.
  - Specifically fixed the old table/caption overlap around `#24/#25`, contributions and caveats blocks `#27`-`#30`, and the bottom notes/footer `#40`-`#43`.
  - No GT annotation was added, removed, newly boxed, or cleared.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `0`.

Verification:

- Report with full per-index old/new bbox details: `reports/pdb_academic_conference026_030_visual_v568.json`.
- Visual dry-run cover checks: `/tmp/pdb_conf026_030_v568_dry_cover/`.
- Visual cover check directory: `cover_audit_academic_conference026_030_v568_only/`.
- Key generated cover files:
  - `cover_audit_academic_conference026_030_v568_only/01_conference_poster_026_KDD_TempoFormer_cover.jpg`
  - `cover_audit_academic_conference026_030_v568_only/02_conference_poster_027_SIGIR_RAG_cover.jpg`
  - `cover_audit_academic_conference026_030_v568_only/03_conference_poster_028_INTERSPEECH_VoiceClone_cover.jpg`
  - `cover_audit_academic_conference026_030_v568_only/04_conference_poster_029_USENIX_KernelGhost_cover.jpg`
  - `cover_audit_academic_conference026_030_v568_only/05_conference_poster_030_IAU_ExoCartographer_cover.jpg`
- Static validation: `review_data.json` and `review_data.js` parse, `index.html` points to token `20260609_academic_conference026_030_visual_v568`, rows `176`-`180` are all boxed with `0 no bbox`.
- Frontend verification: opened rows `176`-`180` with `cb=20260609_academic_conference026_030_visual_v568`; all five rows loaded the v568 token and show `0 no bbox` in the active case row.
- Latest token after this repair: `20260609_academic_conference026_030_visual_v568`.

## 20260609_academic_conference019_visual_v569

Scope:

- Targeted follow-up visual repair for the user-reported remaining offset in:
  - `01_academic/06_conference_poster/conference_poster_019_ICML_FoldFlow`
- User-visible issue: the case was already fully boxed, but the left-column `WHAT BUGS US` / `THE FOLDFLOW PIPELINE` region still had visibly low/loose boxes, especially `#11` and `#12`.

Token:

- v569: `20260609_academic_conference019_visual_v569`

Method:

- Added `scripts/fix_academic_conference019_visual_v569.py`.
- Used the rendered HTML DOM at the released clean-PNG scale and visual crop inspection to retighten the affected left-column note/pipeline area.
- Updated `review_data.json`, `review_data.js`, and `index.html` query token.

Case-level changes:

- `conference_poster_019_ICML_FoldFlow`: changed `9` existing bbox slots; boxed remains `46/46`; no-bbox remains `0`; low-similarity remains `0`.
  - `#7` `1 WHAT BUGS US`: moved the title box upward and trimmed the bottom from `[169, 1170, 741, 1270]` to `[169, 1151, 741, 1264]`.
  - `#8` first problem paragraph: moved upward and tightened from `[172, 1298, 1397, 1474]` to `[172, 1278, 1397, 1465]`.
  - `#9` transition sentence: moved upward/tightened from `[172, 1482, 924, 1532]` to `[172, 1461, 924, 1522]`.
  - `#10` three bullet consequences: moved upward/tightened from `[172, 1540, 1410, 1686]` to `[172, 1517, 1410, 1644]`.
  - `#11` terminal `We want a model...` paragraph: moved upward and reduced the low bottom drift from `[172, 1687, 1370, 1786]` to `[172, 1648, 1370, 1782]`.
  - `#12` `THE FOLDFLOW PIPELINE` title: moved upward/tightened from `[169, 1897, 1092, 1998]` to `[169, 1870, 1092, 1985]`.
  - `#13` pipeline node row: changed from the wider/looser figure-region box `[172, 2032, 1410, 2250]` to the visible pipeline node row `[190, 2035, 1392, 2228]`.
  - `#14` Figure 1 caption: moved upward/tightened from `[351, 2253, 1230, 2297]` to `[351, 2224, 1230, 2281]`.
  - `#15` pipeline explanatory paragraph: moved upward/tightened from `[172, 2342, 1375, 2483]` to `[172, 2311, 1375, 2466]`.
  - No GT annotation was added, removed, newly boxed, or cleared.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `0`.

Verification:

- Report with full per-index old/new bbox details: `reports/pdb_academic_conference019_visual_v569.json`.
- Visual comparison crop: `/tmp/conference019_v569_7_15_crop_final2.png`.
- Visual cover check directory: `cover_audit_academic_conference019_v569_only/`.
- Key generated cover file: `cover_audit_academic_conference019_v569_only/01_conference_poster_019_ICML_FoldFlow_cover.jpg`.
- Static validation: `review_data.json` and `review_data.js` parse, `index.html` points to token `20260609_academic_conference019_visual_v569`, and the case remains `46/46 boxed`, `0 no bbox`, `0 low`.
- Frontend verification: opened `conference_poster_019_ICML_FoldFlow` with `cb=20260609_academic_conference019_visual_v569`; the app loaded the v569 token and shows `46/46 boxed`, `0 no bbox`.
- Latest token after this repair: `20260609_academic_conference019_visual_v569`.

## 20260609_education_textbook008_012_visual_v571

Scope:

- Continued the user-requested textbook visual repair for review rows 6-10:
  - `02_education/01_textbook/textbook_008_数据结构_二叉树`
  - `02_education/01_textbook/textbook_009_EM_Waves_Maxwell_EN`
  - `02_education/01_textbook/textbook_010_电路分析_戴维南`
  - `02_education/01_textbook/textbook_011_细胞生物学_细胞器_ZHCN`
  - `02_education/01_textbook/textbook_012_区域经济地理_城镇化统计`
- User-visible issue: these cases still had visible bbox drift or missing boxes even when the list-level boxed/no-bbox counts looked mostly healthy. The main remaining failures were missing subsection/title boxes, shifted derivation/equation boxes in two-column layouts, and lower-table/keyword blocks that could not be judged from boxed counts alone.

Token:

- v571: `20260609_education_textbook008_012_visual_v571`

Method:

- Added `scripts/fix_education_textbook008_012_visual_v571.py`.
- Used explicit Chrome DOM selector rectangles at the released clean-PNG scale for headers, section titles, paragraphs, code blocks, formulas, theorem/example boxes, tables, table captions, notes, footnotes, and page numbers.
- Switched the two-column EM Waves page to element-level rectangles for paragraphs/equations/proofs/examples after visual cover inspection showed text-range rectangles still exposed first/last lines.
- Used manual visual bboxes for `textbook_011` `#11`, `#33`, and `#34`, based on clean-PNG crops, because the DOM vertical scale pushed the keyword/definition region too low.
- Updated `review_data.json`, `review_data.js`, and `index.html` query token.

Case-level changes:

- `textbook_008_数据结构_二叉树`: changed `23` existing bbox slots; boxed changed from `19/23` to `23/23`; no-bbox changed from `4` to `0`; low-similarity remains `0`.
  - Added bbox to existing GT annotations `#4` (`5.3.1 BST 插入算法`), `#8` (`5.3.2 BST 结构图示`), `#10` (`5.3.3 复杂度分析`), and `#19` (`5.3.4 BST 删除操作`).
  - Refit header/title/intro `#0`-`#4`, code and tip blocks `#5`-`#7`, BST figure/table/example region `#8`-`#18`, deletion section/code block `#19`-`#21`, and footer `#22`.
  - No GT annotation was added or removed.
- `textbook_009_EM_Waves_Maxwell_EN`: changed `53` existing bbox slots; boxed changed from `51/53` to `53/53`; no-bbox changed from `2` to `0`; low-similarity changed from `16` to `0`.
  - Added bbox to existing GT annotations `#35` (`9.2.4 Energy and the Poynting Vector`) and `#43` (Poynting theorem equation).
  - Refit the chapter heading `#0`-`#4`, left-column Maxwell/wave-equation/plane-wave region `#5`-`#29`, right-column theorem/proof/energy/radiation-pressure/example region `#30`-`#48`, footnotes `#49`-`#51`, and page number `#52`.
  - Specifically fixed the old `#3` chapter title and derivation/equation boxes `#14/#16/#18/#20/#22/#35/#43` that were previously shifted or missing.
  - No GT annotation was added or removed.
- `textbook_010_电路分析_戴维南`: changed `33` existing bbox slots; boxed remains `33/33`; no-bbox remains `0`; low-similarity changed from `5` to `0`.
  - Refit the header/title/intro `#0`-`#3`, theorem box `#4/#5`, parameter-solving section/formulas/figure caption `#6`-`#13`, note and worked example `#14`-`#25`, summary table `#26/#27`, exercises `#28`-`#31`, and footer `#32`.
  - Specifically fixed the old `#4` theorem title and `#6` parameter-solving title, which had been parked down in the example/table area.
  - No GT annotation was added, removed, newly boxed, or cleared.
- `textbook_011_细胞生物学_细胞器_ZHCN`: changed `7` existing bbox slots; boxed changed from `38/39` to `39/39`; no-bbox changed from `1` to `0`; low-similarity changed from `5` to `0`.
  - Added bbox to existing GT annotation `#34` (keyword terms table/list).
  - Refit only the visually problematic items: chapter label/title/English title `#2/#3/#4`, `Definition.` label `#11`, second-column section title `#14`, keyword title `#33`, and keyword terms table/list `#34`.
  - Preserved the previously aligned body, figure, summary, footnote, and footer boxes to avoid pushing the lower-page footnotes away from their visible text.
  - No GT annotation was added or removed.
- `textbook_012_区域经济地理_城镇化统计`: changed `17` existing bbox slots; boxed remains `17/17`; no-bbox remains `0`; low-similarity changed from `1` to `0`.
  - Refit page header/chapter title `#0`-`#3`, body paragraph `#4`, table captions/tables/notes `#5`-`#13`, references `#14/#15`, and footer `#16`.
  - No GT annotation was added, removed, newly boxed, or cleared.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `7` (`textbook_008` `#4/#8/#10/#19`, `textbook_009` `#35/#43`, `textbook_011` `#34`).
- Cleared existing bbox values: `0`.

Verification:

- Report with full per-index old/new bbox details: `reports/pdb_education_textbook008_012_visual_v571.json`.
- Visual dry-run cover checks: `cover_audit_education_textbook008_012_v571_dry/`.
- Visual cover check directory: `cover_audit_education_textbook008_012_v571_only/`.
- Key generated cover files:
  - `cover_audit_education_textbook008_012_v571_only/01_textbook_008_数据结构_二叉树_cover.jpg`
  - `cover_audit_education_textbook008_012_v571_only/02_textbook_009_EM_Waves_Maxwell_EN_cover.jpg`
  - `cover_audit_education_textbook008_012_v571_only/03_textbook_010_电路分析_戴维南_cover.jpg`
  - `cover_audit_education_textbook008_012_v571_only/04_textbook_011_细胞生物学_细胞器_ZHCN_cover.jpg`
  - `cover_audit_education_textbook008_012_v571_only/05_textbook_012_区域经济地理_城镇化统计_cover.jpg`
- Static validation: dry-run and final run produced no unresolved selector/manual entries; all five target cases finish with `0 no bbox` and `0 low-similarity`.
- Frontend verification: opened `textbook_008_数据结构_二叉树` with `cb=20260609_education_textbook008_012_visual_v571`; the app loaded `data 20260609_education_textbook008_012_visual_v571`, and rows `textbook_008`-`textbook_012` show `23/23`, `53/53`, `33/33`, `39/39`, and `17/17` boxed with `0 no bbox`.
- Latest token after this repair: `20260609_education_textbook008_012_visual_v571`.

## 20260609_education_textbook008_visual_v572

Scope:

- Follow-up single-case visual repair after frontend review showed `02_education/01_textbook/textbook_008_数据结构_二叉树` was still not aligned around `#10/#11`.
- User-visible issue: v571 had all items boxed, but the `5.3.2`/tree-caption/`5.3.3`/complexity-table region was still visually offset; `#10` sat above the `5.3.3 复杂度分析` title and `#11` started too high relative to the complexity table.

Token:

- v572: `20260609_education_textbook008_visual_v572`

Method:

- Added `scripts/fix_education_textbook008_visual_v572.py`.
- Replaced the remaining v571 DOM-derived coordinates for `textbook_008` with manual clean-PNG visual bboxes.
- Updated `review_data.json`, `review_data.js`, and `index.html` query token.

Case-level changes:

- `textbook_008_数据结构_二叉树`: changed `21` existing bbox slots; boxed remains `23/23`; no-bbox remains `0`; low-similarity remains `0`.
  - Retightened top content `#2`-`#5`, including the section title, intro paragraph, `5.3.1 BST 插入算法`, and the first code block.
  - Moved tip boxes `#6/#7` down to the actual yellow tip strip.
  - Moved `#8` to the real `5.3.2 BST 结构图示` title and `#9` to the figure caption without covering the tree root node.
  - Moved `#10` to the real `5.3.3 复杂度分析` title and `#11` to the complexity table/table-header region.
  - Moved lower example/delete-section items `#12`-`#22` down to the visible example box, deletion paragraph/code block, and footer.
  - No GT annotation was added or removed.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `0`.

Verification:

- Report with full per-index old/new bbox details: `reports/pdb_education_textbook008_visual_v572.json`.
- Visual dry-run cover check: `cover_audit_education_textbook008_v572_dry/`.
- Visual cover check directory: `cover_audit_education_textbook008_v572_only/`.
- Key generated cover file: `cover_audit_education_textbook008_v572_only/01_textbook_008_数据结构_二叉树_cover.jpg`.
- Static validation: `review_data.json` and `review_data.js` parse, `index.html` points to token `20260609_education_textbook008_visual_v572`, and the case remains `23/23 boxed`, `0 no bbox`, `0 low`.
- Frontend verification: opened `textbook_008_数据结构_二叉树` with `cb=20260609_education_textbook008_visual_v572`; the app loaded `data 20260609_education_textbook008_visual_v572`, shows `23/23 boxed` and `0 no bbox`, and the SVG overlay contains the v572 coordinates for `#8` `[198, 1215, 720, 1325]`, `#9` `[928, 1288, 1560, 1368]`, `#10` `[198, 1575, 700, 1668]`, and `#11` `[205, 1660, 2275, 2190]`.
- Latest token after this repair: `20260609_education_textbook008_visual_v572`.

## 20260609_education_textbook011_015_visual_v573

Scope:

- Continued the user-requested textbook visual repair for rows 11-15:
  - `02_education/01_textbook/textbook_011_细胞生物学_细胞器_ZHCN`
  - `02_education/01_textbook/textbook_012_区域经济地理_城镇化统计`
  - `02_education/01_textbook/textbook_013_Organic_Chem_EAS_EN`
  - `02_education/01_textbook/textbook_014_Numerical_Analysis_EN`
  - `02_education/01_textbook/textbook_015_数据结构_哈希表_ZHCN`
- User-visible issue: `textbook_013` still had formula boxes missing/misaligned; cover inspection also showed `textbook_011` still had visible title/body/reference drift and `textbook_015` still had uncovered right-column titles, bullets, side notes, and references.

Token:

- v573: `20260609_education_textbook011_015_visual_v573`

Method:

- Added `scripts/fix_education_textbook011_015_visual_v573.py`.
- Rebuilt bboxes from clean-PNG visual coordinates, assisted by DOM element locations where they matched the rendered clean page.
- Used solid cover images to verify visible text was actually covered, not just counted as boxed.
- Updated `review_data.json`, `review_data.js`, and `index.html` query token.

Case-level changes:

- `textbook_011_细胞生物学_细胞器_ZHCN`: changed `39` existing bbox slots; boxed remains `39/39`; no-bbox remains `0`; low-similarity remains `0`.
  - Rebuilt the full three-column layout: header/title `#0`-`#4`, side notes `#5/#6`, left-column mitochondria section `#7`-`#13`, center ER section `#14`-`#20`, right-column membrane trafficking/summary/key terms `#21`-`#34`, references `#35`-`#37`, and page number `#38`.
  - Fixed the v571 residual drift where the chapter title, English subtitle, definition block, UPR title, summary/key-terms region, and footer references still exposed text in cover mode.
  - No GT annotation was added, removed, newly boxed, or cleared.
- `textbook_012_区域经济地理_城镇化统计`: changed `0` existing bbox slots; boxed remains `17/17`; no-bbox remains `0`; low-similarity remains `0`.
  - Visually checked and retained the existing v571 boxes; visible table grid/header remnants in cover mode are non-text/table graphics rather than residual GT text drift.
  - No GT annotation was added, removed, newly boxed, or cleared.
- `textbook_013_Organic_Chem_EAS_EN`: changed `54` existing bbox slots; boxed changed from `48/54` to `54/54`; no-bbox changed from `6` to `0`; low-similarity changed from `1` to `0`.
  - Added bboxes to existing GT annotations `#7`, `#17`, `#21`, `#25`, `#29`, and `#45`, all formula/equation items.
  - Refit header/title/intro `#0`-`#8`, right note/caption `#9`-`#11`, mechanism text `#12`-`#14`, common reaction formula blocks `#15`-`#31`, substituent-effects table/glossary `#32`-`#43`, sulfonation formula block `#44`-`#50`, references `#51/#52`, and page number `#53`.
  - No GT annotation was added or removed.
- `textbook_014_Numerical_Analysis_EN`: changed `32` existing bbox slots; boxed remains `32/32`; no-bbox remains `0`; low-similarity changed from `8` to `0`.
  - Refit the header/title `#0`-`#6`, definition/theorem/proof/equation regions `#7`-`#17`, table `#18`, algorithm and theorem blocks `#19`-`#24`, exercises `#25`-`#30`, and page number `#31`.
  - No GT annotation was added, removed, newly boxed, or cleared.
- `textbook_015_数据结构_哈希表_ZHCN`: changed `44` existing bbox slots; boxed changed from `43/44` to `44/44`; no-bbox changed from `1` to `0`; low-similarity changed from `8` to `0`.
  - Added bbox to existing GT annotation `#34` (`例题 7.2 线性探测插入过程分析`).
  - Rebuilt the two-column hash-table layout, including bullets `#14`-`#17`, open-addressing text/formula lines `#19`-`#28`, figure caption `#30`, performance-comparison/table/example region `#31`-`#38`, rehashing section `#39/#40`, side note `#6`, references `#41/#42`, and page number `#43`.
  - No GT annotation was added or removed.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `7` (`textbook_013` `#7/#17/#21/#25/#29/#45`, `textbook_015` `#34`).
- Cleared existing bbox values: `0`.

Verification:

- Report with full per-index old/new bbox details: `reports/pdb_education_textbook011_015_visual_v573.json`.
- Visual dry-run cover checks: `cover_audit_education_textbook011_015_v573_dry/`.
- Visual cover check directory: `cover_audit_education_textbook011_015_v573/`.
- Key generated cover files:
  - `cover_audit_education_textbook011_015_v573/01_textbook_011_细胞生物学_细胞器_ZHCN_cover.jpg`
  - `cover_audit_education_textbook011_015_v573/03_textbook_013_Organic_Chem_EAS_EN_cover.jpg`
  - `cover_audit_education_textbook011_015_v573/04_textbook_014_Numerical_Analysis_EN_cover.jpg`
  - `cover_audit_education_textbook011_015_v573/05_textbook_015_数据结构_哈希表_ZHCN_cover.jpg`
- Static validation: dry-run and final run finish all five target cases with `0 no bbox` and `0 low-similarity`; final run reports `changed=169`, `resolved_to_bbox=7`, `added_annotations=0`, `removed_annotations=0`.
- Frontend verification: opened `textbook_013_Organic_Chem_EAS_EN` with `cb=20260609_education_textbook011_015_visual_v573`; the app loaded `data 20260609_education_textbook011_015_visual_v573`, the active case row shows `54/54 boxed · 0 no bbox`, and sidebar rows `textbook_011`-`textbook_015` show `39/39`, `17/17`, `54/54`, `32/32`, and `44/44` boxed with `0 no bbox`.
- Latest token after this repair: `20260609_education_textbook011_015_visual_v573`.

## 20260609_education_textbook016_020_visual_v574

Scope:

- Continued the user-requested textbook visual repair for rows 16-20.
- The current review/release package contains only these two cases in that range:
  - `02_education/01_textbook/textbook_016_高等数学_多元微分_泰勒展开`
  - `02_education/01_textbook/textbook_017_神经科学_记忆编码与突触可塑性`
- `textbook_018`, `textbook_019`, and `textbook_020` are absent from both `review_data.json` and the release clean-image package, so no GT annotations were created for those missing cases.
- User-visible issue: the existing boxes were counted as boxed but still visibly offset, especially formula/table/title regions in `textbook_016` and the right-column/long-page regions in `textbook_017`.

Token:

- v574: `20260609_education_textbook016_020_visual_v574`

Method:

- Added `scripts/fix_education_textbook016_020_visual_v574.py`.
- Rebuilt the two existing cases from clean-PNG visual coordinates and used both solid cover images and non-cover outline previews to check that boxes visually align, not merely pass boxed/no-bbox counts.
- Updated `review_data.json`, `review_data.js`, and `index.html` query token.

Case-level changes:

- `textbook_016_高等数学_多元微分_泰勒展开`: changed `49` existing bbox slots; boxed changed from `48/49` to `49/49`; no-bbox changed from `1` to `0`; low-similarity changed from `20` to `0`.
  - Added bbox to existing GT annotation `#40` (`§9.4.3 条件极值与 Lagrange 乘数法`).
  - Refit header/chapter/section title `#0`-`#4`, Taylor-expansion paragraphs and equations `#5`-`#13`, theorem and critical-point conditions `#14`-`#24`, derivation/table/example regions `#25`-`#39`, Lagrange-multiplier section `#40`-`#44`, references `#45`-`#47`, and page number `#48`.
  - Follow-up dry-run visual checks expanded formula/table/title upper edges for `#7/#8/#9/#10/#13/#20/#27/#29/#30/#40/#41` where cover mode still exposed text.
  - No GT annotation was added or removed.
- `textbook_017_神经科学_记忆编码与突触可塑性`: changed `45` existing bbox slots; boxed changed from `44/45` to `45/45`; no-bbox changed from `1` to `0`; low-similarity changed from `8` to `0`.
  - Added bbox to existing GT annotation `#36` (`12.2.3 记忆巩固：从海马到皮层`).
  - Refit header/chapter/title `#0`-`#6`, left-column memory/LTP paragraphs and formulas `#7`-`#19`, right-column mechanism snapshot and engram/research-note sections `#20`-`#35`, consolidation section `#36`-`#38`, key-terms index `#39`-`#41`, references/footer/page number `#42`-`#44`.
  - Follow-up dry-run visual checks left-expanded the right-column block `#20`-`#41` and lifted `#7` after cover mode showed the old boxes clipping column text.
  - No GT annotation was added or removed.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `2` (`textbook_016` `#40`, `textbook_017` `#36`).
- Cleared existing bbox values: `0`.

Verification:

- Report with full per-index old/new bbox details: `reports/pdb_education_textbook016_020_visual_v574.json`.
- Visual dry-run cover checks: `cover_audit_education_textbook016_020_v574_dry/`, `cover_audit_education_textbook016_020_v574_dry2/`, `cover_audit_education_textbook016_020_v574_dry3/`, and `cover_audit_education_textbook016_020_v574_dry4/`.
- Visual cover check directory: `cover_audit_education_textbook016_020_v574/`.
- Key generated cover files:
  - `cover_audit_education_textbook016_020_v574/01_textbook_016_高等数学_多元微分_泰勒展开_cover.jpg`
  - `cover_audit_education_textbook016_020_v574/02_textbook_017_神经科学_记忆编码与突触可塑性_cover.jpg`
- Static validation: dry-run and final run finish both existing target cases with `0 no bbox` and `0 low-similarity`; final run reports `changed=94`, `resolved_to_bbox=2`, `added_annotations=0`, `removed_annotations=0`.
- Frontend verification: opened `textbook_016_高等数学_多元微分_泰勒展开` and `textbook_017_神经科学_记忆编码与突触可塑性` with `cb=20260609_education_textbook016_020_visual_v574`; the app loaded `data 20260609_education_textbook016_020_visual_v574`, with active rows showing `49/49 boxed · 0 no bbox` and `45/45 boxed · 0 no bbox`.
- Latest token after this repair: `20260609_education_textbook016_020_visual_v574`.

## 20260609_education_textbook023_032_visual_v575

Scope:

- Continued the user-requested textbook visual repair for rows 23-32.
- The current review/release package contains these five cases in that range:
  - `02_education/01_textbook/textbook_023_Abstract_Algebra_EN`
  - `02_education/01_textbook/textbook_024_DSP_EN`
  - `02_education/01_textbook/textbook_028_微观经济学`
  - `02_education/01_textbook/textbook_031_神经科学_记忆编码与突触可塑性`
  - `02_education/01_textbook/textbook_032_比较文学_神话叙事`
- `textbook_025`, `textbook_026`, `textbook_027`, `textbook_029`, and `textbook_030` are absent from both `review_data.json` and the release clean-image package, so no GT annotations were created for those missing cases.
- User-visible issue: although many items were already counted as boxed, cover and outline checks showed visible drift in theorem/title/table/formula regions, side notes, two-column right panels, and footer/reference blocks.

Token:

- v575: `20260609_education_textbook023_032_visual_v575`

Method:

- Added `scripts/fix_education_textbook023_032_visual_v575.py`.
- Rebuilt existing target cases from clean-PNG visual coordinates.
- Iterated through dry-run cover checks through `dry6`; after each cover inspection, expanded or moved the specific boxes that still exposed text.
- Generated non-cover red outline previews to check box placement, not only cover/no-bbox statistics.
- Updated `review_data.json`, `review_data.js`, and `index.html` query token.

Case-level changes:

- `textbook_023_Abstract_Algebra_EN`: changed `35` existing bbox slots; boxed remains `35/35`; no-bbox remains `0`; low-similarity remains `0`.
  - Refit chapter/title `#0/#1`, section/theorem/definition blocks `#2`-`#25`, comparison table caption/table `#26/#27`, exercises `#28`-`#33`, and page number `#34`.
  - Follow-up cover checks lifted the theorem/corollary/exercise upper edges and the table `#27` upper edge so the dark table header and title tops no longer leaked.
  - No GT annotation was added, removed, newly boxed, or cleared.
- `textbook_024_DSP_EN`: changed `31` existing bbox slots; boxed changed from `29/31` to `31/31`; no-bbox changed from `2` to `0`; low-similarity remains `0`.
  - Added bboxes to existing GT annotations `#5` and `#13`, both equation/formula items.
  - Refit the chapter header `#0/#1`, DFT definition/formula block `#2`-`#6`, DFT properties table `#7/#8`, FFT theorem/formula/savings table/code block `#9`-`#17`, spectral-analysis/windowing table `#18`-`#21`, example/exercises `#22`-`#29`, and page number `#30`.
  - Follow-up cover checks specifically expanded formula `#5` and table boxes `#16/#21` to include exposed top/table-header text.
  - No GT annotation was added or removed.
- `textbook_028_微观经济学`: changed `45` existing bbox slots; boxed changed from `44/45` to `45/45`; no-bbox changed from `1` to `0`; low-similarity changed from `7` to `0`.
  - Added bbox to existing GT annotation `#43` (`Question 3` in the critical-thinking block).
  - Note: the case name is misleading; the clean image and GT text are a world-history/Industrial-Revolution textbook page, so the visual repair followed that clean page.
  - Refit header/title `#0`-`#3`, left side notes `#4/#25/#34`, main text and timeline `#5`-`#16`, historical-figure and source/document panels `#17`-`#24/#30`-`#33`, labor/global-impact/table regions `#26`-`#39`, critical-thinking block `#40`-`#43`, and page number `#44`.
  - Follow-up cover checks raised side-note boxes `#25/#34` after their top lines still showed in cover mode.
  - No GT annotation was added or removed.
- `textbook_031_神经科学_记忆编码与突触可塑性`: changed `54` existing bbox slots; boxed remains `54/54`; no-bbox remains `0`; low-similarity changed from `9` to `0`.
  - Refit narrow-page header/title/left-column memory sections `#0`-`#16`, mechanism snapshot/research-note/neural-coding/glossary right column `#17`-`#47`, bottom comparison table `#48`, references `#49`-`#51`, footer `#52`, and page number `#53`.
  - Follow-up cover checks expanded the left-column right edge and lifted right-column/glossary/table upper edges to eliminate narrow gutter text leaks.
  - No GT annotation was added, removed, newly boxed, or cleared.
- `textbook_032_比较文学_神话叙事`: changed `51` existing bbox slots; boxed remains `51/51`; no-bbox remains `0`; low-similarity changed from `6` to `0`.
  - Refit header/title/page number `#0`-`#3`, left side notes `#4/#11/#16/#38`, main myth/comparison sections and quote/caption `#5`-`#18`, author note `#19`-`#21`, concept map `#22`-`#31`, key terms and quotation/further-reading panels `#32`-`#45`, references `#46`-`#49`, and page number `#50`.
  - Follow-up cover checks expanded the center quote/caption, concept-map row boxes, key-terms rows, further-reading title/items, left-table top, and bottom reference right edge.
  - No GT annotation was added, removed, newly boxed, or cleared.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `3` (`textbook_024` `#5/#13`, `textbook_028` `#43`).
- Cleared existing bbox values: `0`.

Verification:

- Report with full per-index old/new bbox details: `reports/pdb_education_textbook023_032_visual_v575.json`.
- Visual dry-run cover checks: `cover_audit_education_textbook023_032_v575_dry3/`, `cover_audit_education_textbook023_032_v575_dry4/`, `cover_audit_education_textbook023_032_v575_dry5/`, and `cover_audit_education_textbook023_032_v575_dry6/`.
- Visual cover check directory: `cover_audit_education_textbook023_032_v575/`.
- Non-cover outline preview directory: `outline_audit_education_textbook023_032_v575/`.
- Key generated cover files:
  - `cover_audit_education_textbook023_032_v575/01_textbook_023_Abstract_Algebra_EN_cover.jpg`
  - `cover_audit_education_textbook023_032_v575/02_textbook_024_DSP_EN_cover.jpg`
  - `cover_audit_education_textbook023_032_v575/03_textbook_028_微观经济学_cover.jpg`
  - `cover_audit_education_textbook023_032_v575/04_textbook_031_神经科学_记忆编码与突触可塑性_cover.jpg`
  - `cover_audit_education_textbook023_032_v575/05_textbook_032_比较文学_神话叙事_cover.jpg`
- Static validation: dry-run and final run finish all five existing target cases with `0 no bbox` and `0 low-similarity`; final run reports `changed=216`, `resolved_to_bbox=3`, `added_annotations=0`, `removed_annotations=0`.
- Frontend verification: opened `textbook_032_比较文学_神话叙事` with `cb=20260609_education_textbook023_032_visual_v575`; the app loaded `data 20260609_education_textbook023_032_visual_v575`, script URLs include `review_data.js?20260609_education_textbook023_032_visual_v575` and `app.js?20260609_education_textbook023_032_visual_v575`, and sidebar rows show `textbook_023` `35/35`, `textbook_024` `31/31`, `textbook_028` `45/45`, `textbook_031` `54/54`, and `textbook_032` `51/51` boxed with `0 no bbox`.
- Latest token after this repair: `20260609_education_textbook023_032_visual_v575`.

## 20260610_education_textbook032_concept_map_v576

Scope:

- Follow-up visual repair for `02_education/01_textbook/textbook_032_比较文学_神话叙事`.
- User-visible issue: in the v575 frontend view, the Author Note lower paragraph `#21` and Concept Map title `#22` were not fully aligned; `#22` started too high in the gap under Author Note, and Concept Map rows `#23`-`#31` were still vertically shifted against their actual row bands.

Token:

- v576: `20260610_education_textbook032_concept_map_v576`

Method:

- Added `scripts/fix_education_textbook032_concept_map_v576.py`.
- Used a clean-PNG crop with coordinate grid for the right-column Author Note / Concept Map / Key Terms transition.
- Refit only the affected existing bbox slots and generated both cover and red-outline previews before writing formal data.
- Updated `review_data.json`, `review_data.js`, and `index.html` query token.

Case-level changes:

- `textbook_032_比较文学_神话叙事`: changed `14` existing bbox slots; boxed remains `51/51`; no-bbox remains `0`; low-similarity remains `0`.
  - Tightened Author Note split: `#20` bottom moved up to the first Author Note paragraph, and `#21` moved to the lower teaching-method paragraph without running into the Concept Map title region.
  - Moved Concept Map title `#22` down to the actual brown title band.
  - Re-banded Concept Map row annotations `#23`-`#31` to the visual row positions for Myth, Archetype, Monomyth, Ritual, Symbol, Intertextuality, Binary Opposition, Symbolic Order, and Cultural Memory.
  - Moved Key Terms title `#32` and first definition block `#33` down to the dashed Key Terms panel instead of overlapping the bottom of the Concept Map panel.
  - No GT annotation was added, removed, newly boxed, or cleared.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `0`.

Verification:

- Report with full per-index old/new bbox details: `reports/pdb_education_textbook032_concept_map_v576.json`.
- Visual dry-run cover check: `cover_audit_education_textbook032_concept_map_v576_dry/`.
- Visual dry-run outline check: `outline_audit_education_textbook032_concept_map_v576_dry/`.
- Visual cover check directory: `cover_audit_education_textbook032_concept_map_v576/`.
- Non-cover outline preview directory: `outline_audit_education_textbook032_concept_map_v576/`.
- Static validation: dry-run and final run finish `textbook_032` with `51/51 boxed`, `0 no bbox`, and `0 low-similarity`; final run reports `changed=14`, `resolved_to_bbox=0`, `added_annotations=0`, `removed_annotations=0`.
- Frontend verification: opened `textbook_032_比较文学_神话叙事` with `cb=20260610_education_textbook032_concept_map_v576`; the app loaded `data 20260610_education_textbook032_concept_map_v576`, script URLs include `review_data.js?20260610_education_textbook032_concept_map_v576` and `app.js?20260610_education_textbook032_concept_map_v576`, and the sidebar row shows `51/51 boxed · 0 no bbox`.
- Latest token after this repair: `20260610_education_textbook032_concept_map_v576`.

## 20260610_education_textbook031_glossary_table_v577

Scope:

- Follow-up visual repair for `02_education/01_textbook/textbook_031_神经科学_记忆编码与突触可塑性`.
- User-visible issue: the frontend still showed obvious visual drift in the lower-right region even though the case was counted as `54/54 boxed`. Neural Coding / Glossary boxes `#29`-`#47` were shifted into the table area, table `#48` was too tall and swallowed references/footer, and bottom references/footer/page number `#49`-`#53` were drawn too low.

Token:

- v577: `20260610_education_textbook031_glossary_table_v577`

Method:

- Added `scripts/fix_education_textbook031_glossary_table_v577.py`.
- Used clean-PNG coordinate crops with 10px/25px visual grids for the right-column Neural Coding / Glossary area and the lower table / references / footer area.
- Generated dry-run cover and red-outline previews before formal write, then generated final cover and outline previews.
- Updated `review_data.json`, `review_data.js`, and `index.html` query token.

Case-level changes:

- `textbook_031_神经科学_记忆编码与突触可塑性`: changed `25` existing bbox slots; boxed remains `54/54`; no-bbox remains `0`; low-similarity remains `0`.
  - Moved Neural Coding title/body `#29/#30` up to the actual right-column text block and trimmed `#30` so it no longer overlaps the Glossary strip.
  - Refit Glossary title and term annotations `#31`-`#47` to the visible compact glossary panel above the table, including the wrapped `Theta rhythm` / `Optogenetics` / `IEG` final line.
  - Shrunk table `#48` to the actual mechanism table only, ending before the footnotes rather than covering references/footer.
  - Moved references `#49/#50/#51` up to the three visible footnote lines directly below the table.
  - Moved footer `#52` and page number `#53` up to the visible footer line.
  - No GT annotation was added, removed, newly boxed, or cleared.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `0`.

Verification:

- Report with full per-index old/new bbox details: `reports/pdb_education_textbook031_glossary_table_v577.json`.
- Visual dry-run cover check: `cover_audit_education_textbook031_glossary_table_v577_dry/`.
- Visual dry-run outline check: `outline_audit_education_textbook031_glossary_table_v577_dry/`.
- Visual cover check directory: `cover_audit_education_textbook031_glossary_table_v577/`.
- Non-cover outline preview directory: `outline_audit_education_textbook031_glossary_table_v577/`.
- Static validation: dry-run and final run finish `textbook_031` with `54/54 boxed`, `0 no bbox`, and `0 low-similarity`; final run reports `changed=25`, `resolved_to_bbox=0`, `added_annotations=0`, `removed_annotations=0`.
- Frontend verification: opened `textbook_031_神经科学_记忆编码与突触可塑性` with `cb=20260610_education_textbook031_glossary_table_v577`; the app loaded `data 20260610_education_textbook031_glossary_table_v577`, script URLs include `review_data.js?20260610_education_textbook031_glossary_table_v577` and `app.js?20260610_education_textbook031_glossary_table_v577`, and the active sidebar row shows `54/54 boxed · 0 no bbox`. The lower-page viewport screenshot confirmed `#31`-`#47` on the glossary panel, `#48` on the table only, and `#49`-`#53` on the references/footer area.
- Latest token after this repair: `20260610_education_textbook031_glossary_table_v577`.

## 20260610_education_exam044_part4_v578

Scope:

- Follow-up visual repair for `02_education/02_exam_paper/exam_paper_044_建筑与空间设计`.
- User-visible issue: the lower Part IV area still had obvious visual offset even though many boxes were counted as present. Q8/Q9/Q10 boxes were shifted into answer regions or across columns, and the Reference Data / footer annotations had no bbox.

Token:

- v578: `20260610_education_exam044_part4_v578`

Method:

- Added `scripts/fix_education_exam044_part4_v578.py`.
- Used the released clean PNG with coordinate-grid crops for the Part IV lower-page region, then iterated dry-run cover/outline checks through `dry4`.
- Corrected second-pass cover leaks where `#48` clipped the Part IV title, `#50/#51/#53/#54` missed question labels or line endings, `#55`-`#60` missed right-column line starts, and `#57` was tight on the table outer border.
- Updated `review_data.json`, `review_data.js`, and `index.html` query/cache token.

Case-level changes:

- `exam_paper_044_建筑与空间设计`: changed `16` existing bbox slots; boxed changed from `61/64` to `64/64`; no-bbox changed from `3` to `0`; low-similarity changed from `4` to `3`.
  - `#48` Part IV title moved from `[131, 6437, 1200, 6520]` to `[130, 6378, 2205, 6515]`.
  - `#49` Q8 heading moved from `[133, 6539, 2009, 6591]` to `[130, 6530, 650, 6595]`.
  - `#50` Q8(a) moved from `[185, 6988, 1199, 7131]` to `[130, 6590, 1210, 6738]`.
  - `#51` Q8(b) moved from `[185, 7153, 1217, 7350]` to `[130, 6740, 1215, 6975]`.
  - `#52` Q9 heading moved from `[142, 7609, 448, 7647]` to `[130, 7178, 540, 7240]`.
  - `#53` Q9(a) moved from `[185, 7669, 1204, 7759]` to `[130, 7248, 1200, 7350]`.
  - `#54` Q9(b) moved from `[175, 7344, 1851, 7463]` to `[130, 7358, 1195, 7515]`.
  - `#55` Q10 heading moved from `[1259, 6928, 2137, 6966]` to `[1185, 6530, 2220, 6595]`.
  - `#56` Q10 scenario text moved from `[1259, 6988, 2339, 7078]` to `[1185, 6590, 2290, 6712]`.
  - `#57` Q10 function table moved from `[134, 7102, 2337, 7604]` to `[1185, 6695, 2245, 7105]`.
  - `#58` Q10(a) moved from `[1303, 7625, 2337, 7715]` to `[1185, 7100, 2245, 7238]`.
  - `#59` Q10(b) moved from `[1375, 7796, 2021, 7993]` to `[1185, 7238, 2225, 7505]`.
  - `#60` Q10(c) moved from `[1303, 8015, 2137, 8053]` to `[1185, 7495, 2215, 7575]`.
  - `#61` Reference Data was an existing GT annotation with no bbox; added bbox `[1175, 7768, 2245, 8075]`.
  - `#62` footer was an existing GT annotation with no bbox; added bbox `[50, 8100, 1970, 8150]`.
  - `#63` page number was an existing GT annotation with no bbox; added bbox `[1980, 8100, 2325, 8150]`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `3` (`#61/#62/#63`).
- Cleared existing bbox values: `0`.

Verification:

- Report with full per-index old/new bbox details: `reports/pdb_education_exam044_part4_v578.json`.
- Visual dry-run cover checks: `cover_audit_education_exam044_part4_v578_dry/`, `cover_audit_education_exam044_part4_v578_dry2/`, `cover_audit_education_exam044_part4_v578_dry3/`, and `cover_audit_education_exam044_part4_v578_dry4/`.
- Visual dry-run outline checks: `outline_audit_education_exam044_part4_v578_dry/`, `outline_audit_education_exam044_part4_v578_dry2/`, `outline_audit_education_exam044_part4_v578_dry3/`, and `outline_audit_education_exam044_part4_v578_dry4/`.
- Visual cover check directory: `cover_audit_education_exam044_part4_v578/`.
- Non-cover outline preview directory: `outline_audit_education_exam044_part4_v578/`.
- Static validation: final run finishes `exam_paper_044_建筑与空间设计` with `64/64 boxed`, `0 no bbox`, and `3 low-similarity`; final run reports `changed=16`, `resolved_to_bbox=3`, `added_annotations=0`, `removed_annotations=0`.
- Frontend verification: opened `exam_paper_044_建筑与空间设计` with `cb=20260610_education_exam044_part4_v578`; the app header shows `data 20260610_education_exam044_part4_v578`, script URLs include `review_data.js?20260610_education_exam044_part4_v578` and `app.js?20260610_education_exam044_part4_v578`, and the active case status shows `64/64 boxed · 0 no bbox`. The visible Part IV preview confirmed `#48`-`#60` on the question/table blocks and `#61`-`#63` on Reference Data/footer/page number instead of the old shifted answer-area positions.
- Latest token after this repair: `20260610_education_exam044_part4_v578`.

## 20260610_education_exam046_table_types_v579

Scope:

- Follow-up semantic-type and visual repair for `02_education/02_exam_paper/exam_paper_046_数字电子技术`.
- User-visible issue: the state-transition table was visibly a table in the rendered page, but its GT annotations `#80`-`#90` were labeled as `text_block`. The same HTML/table mismatch also appeared in the D flip-flop excitation table and JK excitation table.

Token:

- v579: `20260610_education_exam046_table_types_v579`

Method:

- Added `scripts/fix_education_exam046_table_types_v579.py`.
- Checked source HTML table tags and released clean-PNG coordinate crops for the D excitation table, state-transition table, and JK excitation table.
- Kept the existing GT annotation granularity to avoid renumbering or deleting row-level annotations; changed the affected existing annotations from `text_block` to `table` or `table_caption` and repaired their bboxes.
- Iterated dry-run cover/outline checks through `dry3`; expanded the state-transition table right edge after the Output column leaked, expanded `#90` after the caption leaked, and expanded the D/JK table boxes after bottom/K-column leaks.
- Updated `review_data.json`, `review_data.js`, `index.html` query token, and refreshed `meta.type_counts`.

Case-level changes:

- `exam_paper_046_数字电子技术`: changed `19` existing annotations; category type changed for all `19`; boxed changed from `113/118` to `116/118`; no-bbox changed from `5` to `2`; low-similarity changed from `26` to `23`.
  - D excitation table: `#75` changed from `text_block` to `table_caption` and moved to `[800, 3728, 1020, 3762]`; `#76` changed from `text_block` to `table` and moved from the lower-page wrong position to `[1042, 3767, 1248, 4008]`.
  - State-transition table: `#80`-`#89` changed from `text_block` to `table` and were re-banded to the table header/data rows:
    - `#80`: `[196, 4168, 642, 4215]`
    - `#81`: `[196, 4215, 642, 4262]`
    - `#82`: `[196, 4262, 642, 4308]`
    - `#83`: `[196, 4308, 642, 4354]`
    - `#84`: `[196, 4354, 642, 4400]`
    - `#85`: `[196, 4400, 642, 4446]`
    - `#86`: `[196, 4446, 642, 4492]`
    - `#87`: `[196, 4492, 642, 4538]`
    - `#88`: `[196, 4538, 642, 4584]`
    - `#89`: `[196, 4584, 642, 4630]`
  - State-transition caption: `#90` changed from `text_block` to `table_caption` and moved to `[52, 4636, 410, 4662]`.
  - JK excitation table: `#102` changed from `text_block` to `table_caption` and moved to `[86, 4966, 500, 4993]`; `#103`-`#107` changed from `text_block` to `table` and were re-banded to the JK table header/data rows:
    - `#103`: `[338, 5011, 540, 5060]`
    - `#104`: `[338, 5060, 540, 5108]`
    - `#105`: `[338, 5108, 540, 5155]`
    - `#106`: `[338, 5155, 540, 5203]`
    - `#107`: `[338, 5203, 540, 5240]`

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `3` (`#103/#104/#107`).
- Cleared existing bbox values: `0`.

Verification:

- Report with full per-index old/new bbox and type details: `reports/pdb_education_exam046_table_types_v579.json`.
- Visual dry-run cover checks: `cover_audit_education_exam046_table_types_v579_dry/`, `cover_audit_education_exam046_table_types_v579_dry2/`, and `cover_audit_education_exam046_table_types_v579_dry3/`.
- Visual dry-run outline checks: `outline_audit_education_exam046_table_types_v579_dry/`, `outline_audit_education_exam046_table_types_v579_dry2/`, and `outline_audit_education_exam046_table_types_v579_dry3/`.
- Visual cover check directory: `cover_audit_education_exam046_table_types_v579/`.
- Non-cover outline preview directory: `outline_audit_education_exam046_table_types_v579/`.
- Static validation: final run finishes `exam_paper_046_数字电子技术` with `116/118 boxed`, `2 no bbox`, and `23 low-similarity`; final run reports `changed=19`, `type_changed=19`, `resolved_to_bbox=3`, `added_annotations=0`, `removed_annotations=0`.
- Frontend verification: opened `exam_paper_046_数字电子技术` with `cb=20260610_education_exam046_table_types_v579`; the app header shows `data 20260610_education_exam046_table_types_v579`, script URLs include `review_data.js?20260610_education_exam046_table_types_v579` and `app.js?20260610_education_exam046_table_types_v579`, and the active case status shows `116/118 boxed · 2 no bbox`. The right-side type filters show refreshed counts (`table 3811`, `table_caption 413`, `text_block 66582`), and the annotation list shows `#75 table_caption`, `#76 table`, `#80`-`#89 table`, `#90 table_caption`, `#102 table_caption`, and `#103`-`#107 table`.
- Latest token after this repair: `20260610_education_exam046_table_types_v579`.

## 20260610_education_exam046_table_consolidate_v580

Scope:

- Follow-up consolidation repair for `02_education/02_exam_paper/exam_paper_046_数字电子技术`.
- User-visible issue: v579 was still too granular. The state-transition table was split into row-level annotations `#80`-`#89`, and the JK excitation table was split into row-level annotations `#103`-`#107`; these should be single full-table GT annotations instead of merely changing their type.

Token:

- v580: `20260610_education_exam046_table_consolidate_v580`

Method:

- Added `scripts/fix_education_exam046_table_consolidate_v580.py`.
- Kept original visible annotation indices and `anno_id` values for retained annotations to avoid renumbering unrelated later items.
- Merged row-level fragments into retained full-table annotations and intentionally left index gaps where fragments were deleted.
- Ran dry-run cover/outline visual checks, tightened `#80` after the first dry-run showed the state-transition table bottom border was clipped, then updated `review_data.json`, `review_data.js`, and `index.html` query/cache token.

Case-level changes:

- `exam_paper_046_数字电子技术`: changed `2` retained existing annotations and deleted `13` row-fragment annotations; boxed changed from `116/118` to `103/105`; no-bbox stayed `2`; low-similarity stayed `23`.
  - State-transition table: retained `#80` as the single full-table annotation and expanded it from `[196, 4168, 642, 4215]` to `[196, 4168, 642, 4636]`; text was replaced with the full table content including both header rows and all eight data rows.
  - Removed state-transition row/header fragments: `#81`, `#82`, `#83`, `#84`, `#85`, `#86`, `#87`, `#88`, and `#89`.
  - State-transition caption `#90` remains the separate `table_caption` from v579 at `[52, 4636, 410, 4662]`.
  - JK excitation table: retained `#103` as the single full-table annotation and expanded it from `[338, 5011, 540, 5060]` to `[338, 5011, 540, 5240]`; text was replaced with the full JK excitation table content including header and all four rows.
  - Removed JK row fragments: `#104`, `#105`, `#106`, and `#107`.
  - JK table caption `#102` remains the separate `table_caption` from v579 at `[86, 4966, 500, 4993]`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `13` (`#81`-`#89`, `#104`-`#107`).
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `0`.

Verification:

- Report with full retained old/new bbox details and removed annotation list: `reports/pdb_education_exam046_table_consolidate_v580.json`.
- Visual dry-run cover checks: `cover_audit_education_exam046_table_consolidate_v580_dry/` and `cover_audit_education_exam046_table_consolidate_v580_dry2/`.
- Visual dry-run outline checks: `outline_audit_education_exam046_table_consolidate_v580_dry/` and `outline_audit_education_exam046_table_consolidate_v580_dry2/`.
- Visual cover check directory: `cover_audit_education_exam046_table_consolidate_v580/`.
- Non-cover outline preview directory: `outline_audit_education_exam046_table_consolidate_v580/`.
- Static validation: final run finishes `exam_paper_046_数字电子技术` with `105` GT annotations, `103/105 boxed`, `2 no bbox`, and `23 low-similarity`; final run reports `changed_retained_annotations=2`, `added_annotations=0`, `removed_annotations=13`, and `resolved_to_bbox=-13`.
- Frontend verification: opened `exam_paper_046_数字电子技术` with `cb=20260610_education_exam046_table_consolidate_v580`; the app header shows `data 20260610_education_exam046_table_consolidate_v580`, script URLs include `review_data.js?20260610_education_exam046_table_consolidate_v580` and `app.js?20260610_education_exam046_table_consolidate_v580`, and the active case status shows `103/105 boxed · 2 no bbox · 105 open`. The annotation list now shows `#80 table`, `#90 table_caption`, `#102 table_caption`, and `#103 table`, with deleted row fragments `#81`-`#89` and `#104`-`#107` absent; the visible overlay IDs around the table region are only `80`, `90`, `102`, and `103`.
- Latest token after this repair: `20260610_education_exam046_table_consolidate_v580`.

## 20260610_education_exam047_table_consolidate_v581

Scope:

- Follow-up table-fragment consolidation repair for `02_education/02_exam_paper/exam_paper_047_模拟电子技术`.
- User-visible issue: the design-specification table in Part V was visibly one table, but GT annotations `#112`-`#118` were row-level `text_block` fragments. Full-case HTML inspection also found the same GT fragmentation in the earlier device-parameters table, where `#40`-`#45` were row/header fragments and several row fragments had drifted to unrelated page areas.
- This token records true GT semantic changes, not just bbox movement: `category_type` changes, retained annotation text replacement, and deletion/merge of row fragments.

Token:

- v581: `20260610_education_exam047_table_consolidate_v581`

Method:

- Added `scripts/fix_education_exam047_table_consolidate_v581.py`.
- Checked source HTML tables and clean-PNG table borders. The case has three HTML tables: the node table `#124` was already a single `table` annotation, so it was left unchanged; the fragmented device-parameters and design-specification tables were consolidated.
- Kept original visible annotation indices and `anno_id` values for retained annotations to avoid renumbering unrelated later items.
- Ran dry-run cover/outline visual checks, slightly expanded the device-parameters table bbox after the first pass, then updated `review_data.json`, `review_data.js`, and `index.html` query/cache token.

Case-level changes:

- `exam_paper_047_模拟电子技术`: changed `2` retained existing annotations into full-table annotations, changed `1` caption type, and deleted `11` row-fragment annotations; boxed changed from `134/134` to `123/123`; no-bbox stayed `0`; low-similarity changed from `51` to `43`.
  - Device-parameters caption: `#39` changed from `text_block` to `table_caption`; bbox stayed `[674, 1266, 1155, 1299]`; text stayed `Table 2-1: Device Parameters / 器件参数`.
  - Device-parameters table: retained `#40` as the single full-table annotation, changed from `text_block` to `table`, moved from `[749, 603, 764, 628]` to `[968, 1308, 1332, 1602]`, changed quality from `low_similarity` to `ok`, and replaced text with the full table content:
    - `Parameter Value Unit Condition`
    - `β (hFE) 100 - IC=2mA`
    - `VBE(on) 0.7 V active region`
    - `rbb' 200 Ω -`
    - `VCC 12 V DC supply`
    - `RL 6 kΩ external load`
  - Removed device-parameters row fragments: `#41`, `#42`, `#43`, `#44`, and `#45`.
  - Design-specification table: retained `#112` as the single full-table annotation, changed from `text_block` to `table`, expanded from `[615, 4682, 978, 4718]` to `[601, 4679, 986, 5018]`, and replaced text with the full table content:
    - `Parameter 指标 Requirement 要求 Unit`
    - `总电压增益 |Av| ≥ 80 (≈38dB) V/V`
    - `输入电阻 Ri ≥ 5kΩ Ω`
    - `输出电阻 Ro ≤ 100Ω Ω`
    - `通频带 BW 100Hz – 200kHz Hz`
    - `电源电压 VCC 15 V`
    - `负载电阻 RL 1kΩ Ω`
  - Removed design-specification row fragments: `#113`, `#114`, `#115`, `#116`, `#117`, and `#118`.
  - Existing node table `#124` remained unchanged as a single `table` annotation.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `11` (`#41`-`#45`, `#113`-`#118`).
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `0`.
- Non-bbox semantic changes recorded in this pass: `3` (`#39` category type; `#40` category type/text/quality/method; `#112` category type/text/method).

Verification:

- Report with retained old/new bbox, type/text changes, and removed annotation list: `reports/pdb_education_exam047_table_consolidate_v581.json`.
- Visual dry-run cover checks: `cover_audit_education_exam047_table_consolidate_v581_dry/` and `cover_audit_education_exam047_table_consolidate_v581_dry2/`.
- Visual dry-run outline checks: `outline_audit_education_exam047_table_consolidate_v581_dry/` and `outline_audit_education_exam047_table_consolidate_v581_dry2/`.
- Visual cover check directory: `cover_audit_education_exam047_table_consolidate_v581/`.
- Non-cover outline preview directory: `outline_audit_education_exam047_table_consolidate_v581/`.
- Static validation: final run finishes `exam_paper_047_模拟电子技术` with `123` GT annotations, `123/123 boxed`, `0 no bbox`, and `43 low-similarity`; final run reports `changed_retained_annotations=2`, `type_only_changes=1`, `added_annotations=0`, `removed_annotations=11`, and `resolved_to_bbox=-11`.
- Visual note: this token specifically repairs table GT fragmentation/consolidation. Other unrelated non-table bbox drift visible elsewhere in the same case was not treated as completed by this token.
- Frontend verification: opened `exam_paper_047_模拟电子技术` with `cb=20260610_education_exam047_table_consolidate_v581`; the app header shows `data 20260610_education_exam047_table_consolidate_v581`, script URLs include `review_data.js?20260610_education_exam047_table_consolidate_v581` and `app.js?20260610_education_exam047_table_consolidate_v581`, and the active case status shows `123/123 boxed · 0 no bbox · 123 open`. The annotation list now shows `#39 table_caption`, `#40 table`, `#112 table`, and the pre-existing `#124 table`; deleted row fragments `#41`-`#45` and `#113`-`#118` are absent, and the visible overlay IDs around the table regions are only `39`, `40`, `111`, `112`, and `124`.
- Latest token after this repair: `20260610_education_exam047_table_consolidate_v581`.

## 20260610_education_textbook009_footer_v582

Scope:

- Follow-up visual bbox repair for `02_education/01_textbook/textbook_009_EM_Waves_Maxwell_EN`.
- User-visible issue: the bottom reference/page-number region was visibly offset even though the case was counted as `53/53 boxed`. Reference annotations `#49`-`#51` were shifted downward into blank footer space, page-number annotation `#52` was too low and oversized, and the preceding Example 9.1 text annotation `#48` extended into the footnote area.
- This token is bbox-only. It does not change GT type/text/preview, does not add annotations, and does not delete annotations.

Token:

- v582: `20260610_education_textbook009_footer_v582`

Method:

- Added `scripts/fix_education_textbook009_footer_v582.py`.
- Checked source HTML footnotes/page footer and clean-PNG bottom crops.
- Used dark-pixel row/column inspection to locate the three footnote text bands and the light-gray page number.
- Ran dry-run cover/outline visual checks before writing the formal token; then updated `review_data.json`, `review_data.js`, and `index.html` query/cache token.

Case-level changes:

- `textbook_009_EM_Waves_Maxwell_EN`: changed `5` existing bbox slots; boxed stayed `53/53`; no-bbox stayed `0`; low-similarity stayed `0`.
  - `#48` Example 9.1 text block bottom was tightened from `[1249, 2459, 2370, 3085]` to `[1249, 2459, 2370, 2888]` so it no longer covers the footnote/reference area.
  - `#49` reference 1 moved from `[112, 3135, 2369, 3282]` to `[126, 2924, 2285, 3004]`.
  - `#50` reference 2 moved from `[112, 3230, 2369, 3333]` to `[126, 3012, 2172, 3050]`.
  - `#51` reference 3 moved from `[112, 3280, 2369, 3384]` to `[126, 3060, 2102, 3096]`.
  - `#52` page number moved from `[1196, 3355, 1285, 3448]` to `[1210, 3124, 1272, 3160]`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `0`.
- Non-bbox semantic changes recorded in this pass: `0`.

Verification:

- Report with full old/new bbox details: `reports/pdb_education_textbook009_footer_v582.json`.
- Visual dry-run cover check directory: `cover_audit_education_textbook009_footer_v582_dry/`.
- Visual dry-run outline check directory: `outline_audit_education_textbook009_footer_v582_dry/`.
- Visual cover check directory: `cover_audit_education_textbook009_footer_v582/`.
- Non-cover outline preview directory: `outline_audit_education_textbook009_footer_v582/`.
- Static validation: final run finishes `textbook_009_EM_Waves_Maxwell_EN` with `53/53 boxed`, `0 no bbox`, and `0 low-similarity`; final run reports `changed_annotations=5`, `added_annotations=0`, `removed_annotations=0`, and `non_bbox_semantic_changes=0`.
- Visual dry-run note: cover/outline crops confirmed `#48` no longer extends into the footnotes, `#49`-`#51` align with the three reference text bands, and `#52` is limited to the page number `274`; the footnote separator line remains uncovered because it is not a GT annotation.
- Frontend verification: opened `textbook_009_EM_Waves_Maxwell_EN` with `cb=20260610_education_textbook009_footer_v582`; the app header shows `data 20260610_education_textbook009_footer_v582`, script URLs include `review_data.js?20260610_education_textbook009_footer_v582` and `app.js?20260610_education_textbook009_footer_v582`, and the active case status shows `53/53 boxed · 0 no bbox · 53 open`. The annotation list shows `#48 text_block`, `#49 reference`, `#50 reference`, `#51 reference`, and `#52 page_number`, and the overlay reports the updated boxes `#48 [1249,2459,2370,2888]`, `#49 [126,2924,2285,3004]`, `#50 [126,3012,2172,3050]`, `#51 [126,3060,2102,3096]`, and `#52 [1210,3124,1272,3160]`.
- Latest token after this repair: `20260610_education_textbook009_footer_v582`.

## 20260610_education_textbook012_footer_v583

Scope:

- Follow-up visual bbox repair for `02_education/01_textbook/textbook_012_区域经济地理_城镇化统计`.
- User-visible issue: the lower table/note/footnote/page-number region was visibly offset even though the case was counted as `17/17 boxed`. The table annotation `#12` extended into the table note, table-note annotation `#13` extended into footnotes, footnotes `#14/#15` were shifted downward, and page-number annotation `#16` was too low and oversized.
- This token is bbox-only. It does not change GT type/text/preview, does not add annotations, and does not delete annotations.

Token:

- v583: `20260610_education_textbook012_footer_v583`

Method:

- Added `scripts/fix_education_textbook012_footer_v583.py`.
- Checked source HTML for the table note, two footnotes, and page footer, then inspected clean-PNG bottom crops.
- Used dark-pixel row/column inspection to locate table bottom, table-note text, footnote text, footer separator, and the page number.
- Ran dry-run cover/outline visual checks twice; second pass expanded `#14/#15` left edges to include the red circled footnote markers. Then updated `review_data.json`, `review_data.js`, and `index.html` query/cache token.

Case-level changes:

- `textbook_012_区域经济地理_城镇化统计`: changed `5` existing bbox slots; boxed stayed `17/17`; no-bbox stayed `0`; low-similarity stayed `0`.
  - `#12` table bbox tightened from `[132, 2374, 2349, 3080]` to `[132, 2374, 2349, 2945]` so it stops at the table bottom and no longer covers the note.
  - `#13` table note moved from `[131, 3031, 2331, 3216]` to `[145, 2953, 2340, 3078]`.
  - `#14` footnote ① moved from `[131, 3198, 2302, 3322]` to `[120, 3114, 2300, 3186]`.
  - `#15` footnote ② moved from `[131, 3275, 2340, 3398]` to `[120, 3196, 2290, 3260]`.
  - `#16` page number moved from `[1161, 3370, 1320, 3461]` to `[1175, 3290, 1306, 3330]`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `0`.
- Non-bbox semantic changes recorded in this pass: `0`.

Verification:

- Report with full old/new bbox details: `reports/pdb_education_textbook012_footer_v583.json`.
- Visual dry-run cover checks: `cover_audit_education_textbook012_footer_v583_dry/` and `cover_audit_education_textbook012_footer_v583_dry2/`.
- Visual dry-run outline checks: `outline_audit_education_textbook012_footer_v583_dry/` and `outline_audit_education_textbook012_footer_v583_dry2/`.
- Visual cover check directory: `cover_audit_education_textbook012_footer_v583/`.
- Non-cover outline preview directory: `outline_audit_education_textbook012_footer_v583/`.
- Static validation: final run finishes `textbook_012_区域经济地理_城镇化统计` with `17/17 boxed`, `0 no bbox`, and `0 low-similarity`; final run reports `changed_annotations=5`, `added_annotations=0`, `removed_annotations=0`, and `non_bbox_semantic_changes=0`.
- Visual dry-run note: cover/outline crops confirmed `#12` no longer covers the table note, `#13` covers only the table note, `#14/#15` align with footnotes ①/② including their red circled markers, and `#16` is limited to the page number `— 246 —`; footer separator lines remain uncovered because they are not GT annotations.
- Frontend verification: opened `textbook_012_区域经济地理_城镇化统计` with `cb=20260610_education_textbook012_footer_v583`; the app header shows `data 20260610_education_textbook012_footer_v583`, script URLs include `review_data.js?20260610_education_textbook012_footer_v583` and `app.js?20260610_education_textbook012_footer_v583`, and the active case status shows `17/17 boxed · 0 no bbox · 17 open`. The annotation list shows `#12 table`, `#13 reference`, `#14 reference`, `#15 reference`, and `#16 page_number`, and the overlay reports the updated boxes `#12 [132,2374,2349,2945]`, `#13 [145,2953,2340,3078]`, `#14 [120,3114,2300,3186]`, `#15 [120,3196,2290,3260]`, and `#16 [1175,3290,1306,3330]`.
- Latest token after this repair: `20260610_education_textbook012_footer_v583`.

## 20260610_education_textbook015_visual_v584

Scope:

- Follow-up visual bbox repair for `02_education/01_textbook/textbook_015_数据结构_哈希表_ZHCN`.
- User-visible issue: the case still had visible bbox drift even though it was counted as `44/44 boxed`. The main drift was in the open-addressing section, code block transition, performance-table caption/table transition, example box, rehashing paragraph, references, and page number.
- This token is bbox-only. It does not change GT type/text/preview/quality semantics, does not add annotations, and does not delete annotations.

Token:

- v584: `20260610_education_textbook015_visual_v584`

Method:

- Added `scripts/fix_education_textbook015_visual_v584.py`.
- Checked clean-PNG outline/cover crops and the source HTML element order (`h2`, paragraphs, list paragraph, code block, flowchart caption, performance table, example box, rehashing block, footnotes, and page footer).
- Ran two dry-run cover/outline visual checks; the second pass expanded `#40` bottom from the first candidate so the final rehashing paragraph line was not clipped. Then updated `review_data.json`, `review_data.js`, and `index.html` query/cache token.

Case-level changes:

- `textbook_015_数据结构_哈希表_ZHCN`: changed `26` existing bbox slots; boxed stayed `44/44`; no-bbox stayed `0`; low-similarity stayed `0`.
  - `#6` right-margin rehash note moved from `[2040,1860,2472,2200]` to `[2280,1932,2472,2116]`.
  - `#18` chaining closing paragraph tightened from `[126,1550,1226,1706]` to `[126,1518,1226,1642]`.
  - `#19` Open Addressing title moved from `[126,1638,1226,1748]` to `[126,1684,1226,1738]`.
  - `#20` Open Addressing paragraph moved from `[96,1718,1226,1938]` to `[126,1740,1226,1868]`.
  - `#21` linear-probing formula moved from `[96,1930,1226,1998]` to `[158,1888,1226,1932]`.
  - `#22` linear-probing note moved from `[96,1986,1226,2050]` to `[126,1938,1226,2010]`.
  - `#23` quadratic-probing formula moved from `[96,2038,1226,2102]` to `[126,2026,1226,2070]`.
  - `#24` quadratic-probing note moved from `[96,2088,1226,2152]` to `[158,2074,1226,2122]`.
  - `#25` double-hashing formula moved from `[96,2136,1226,2200]` to `[126,2124,1226,2170]`.
  - `#26` double-hashing note moved from `[96,2186,1226,2232]` to `[158,2174,1226,2218]`.
  - `#27` code title moved from `[126,2226,1226,2286]` to `[126,2208,1226,2262]`.
  - `#28` code block tightened from `[126,2286,1226,3136]` to `[126,2260,1226,3078]`.
  - `#30` flowchart caption tightened from `[1258,628,2340,720]` to `[1258,636,2340,686]`.
  - `#31` Performance Comparison title tightened from `[1258,700,2358,830]` to `[1258,718,2358,772]`.
  - `#32` performance-table caption moved from `[1258,1614,2358,1710]` to `[1258,1516,2358,1594]`.
  - `#33` performance table moved/tightened from `[1258,824,2358,1618]` to `[1258,778,2358,1508]`.
  - `#34` example title moved from `[1284,1664,2330,1792]` to `[1284,1608,2330,1656]`.
  - `#35` example setup paragraph moved from `[1284,1786,2330,1886]` to `[1284,1660,2330,1734]`.
  - `#36` example solution label moved from `[1284,1882,2330,1942]` to `[1284,1748,2330,1792]`.
  - `#37` example derivation lines moved/tightened from `[1284,1938,2330,2282]` to `[1284,1802,2250,2126]`.
  - `#38` example ASL/conclusion paragraph moved from `[1284,2278,2330,2468]` to `[1284,2138,2330,2318]`.
  - `#39` Rehashing title moved/tightened from `[1258,2388,2358,2578]` to `[1258,2360,2358,2416]`.
  - `#40` Rehashing paragraph moved/tightened from `[1258,2570,2358,2828]` to `[1258,2424,2358,2672]`.
  - `#41` reference ① moved/tightened from `[126,3090,2358,3240]` to `[126,3104,2358,3184]`.
  - `#42` reference ② moved/tightened from `[126,3210,2358,3318]` to `[126,3188,2358,3244]`.
  - `#43` page number moved from `[1170,3368,1310,3432]` to `[1170,3272,1310,3318]`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `0`.
- Non-bbox semantic changes recorded in this pass: `0`.

Verification:

- Report with full old/new bbox details: `reports/pdb_education_textbook015_visual_v584.json`.
- Visual dry-run cover checks: `cover_audit_education_textbook015_visual_v584_dry/` and `cover_audit_education_textbook015_visual_v584_dry2/`.
- Visual dry-run outline checks: `outline_audit_education_textbook015_visual_v584_dry/` and `outline_audit_education_textbook015_visual_v584_dry2/`.
- Visual cover check directory: `cover_audit_education_textbook015_visual_v584/`.
- Non-cover outline preview directory: `outline_audit_education_textbook015_visual_v584/`.
- Static validation: final run finishes `textbook_015_数据结构_哈希表_ZHCN` with `44/44 boxed`, `0 no bbox`, and `0 low-similarity`; final run reports `changed_annotations=26`, `added_annotations=0`, `removed_annotations=0`, and `non_bbox_semantic_changes=0`.
- Visual dry-run note: cover/outline crops confirmed `#18/#19/#20` no longer overlap the Open Addressing transition, `#21`-`#28` align with the list/code bands, `#32/#33/#34` separate the table caption/table/example boundary, `#6/#34`-`#40` align with the right-column example/rehashing content, and `#41/#42/#43` align with the two references and page number.
- Frontend verification: opened `textbook_015_数据结构_哈希表_ZHCN` with `cb=20260610_education_textbook015_visual_v584`; the app header shows `data 20260610_education_textbook015_visual_v584`, script URLs include `review_data.js?20260610_education_textbook015_visual_v584` and `app.js?20260610_education_textbook015_visual_v584`, and the active case status shows `44/44 boxed · 0 no bbox · 44 open`.
- Latest token after this repair: `20260610_education_textbook015_visual_v584`.

## 20260610_education_textbook017_right_column_v585

Scope:

- Follow-up visual bbox repair for `02_education/01_textbook/textbook_017_神经科学_记忆编码与突触可塑性`.
- User-visible issue: the right-column neural-coding / Research Note / consolidation / Key Terms region had visible vertical drift even though the case was counted as `45/45 boxed`. In particular, `#32/#33` cut the Research Note title and first paragraph, `#33/#34/#35` overlapped the formula boundary, and `#36-#41` continued the same downward offset into the next section and terms index.
- This token is bbox-only. It does not change GT type/text/preview/quality semantics, does not add annotations, and does not delete annotations.

Token:

- v585: `20260610_education_textbook017_right_column_v585`

Method:

- Added `scripts/fix_education_textbook017_right_column_v585.py`.
- Checked the source HTML order for the Neural Coding title, two right-column paragraphs, Research Note title/body/formula/explanation, consolidation title/body paragraphs, and Key Terms columns.
- Inspected clean-PNG grid crops and ran three dry-run cover/outline visual checks. The third pass expanded `#37`, `#38`, and `#40` bottom edges after cover crops showed minor bottom-line clipping.
- Updated `review_data.json`, `review_data.js`, and `index.html` query/cache token.

Case-level changes:

- `textbook_017_神经科学_记忆编码与突触可塑性`: changed `13` existing bbox slots; boxed stayed `45/45`; no-bbox stayed `0`; low-similarity stayed `0`.
  - `#29` title moved from `[1438, 1028, 2320, 1090]` to `[1438, 1052, 2320, 1126]`.
  - `#30` text_block moved from `[1438, 1080, 2320, 1760]` to `[1438, 1138, 2320, 1648]`.
  - `#31` text_block moved from `[1438, 1748, 2320, 2160]` to `[1438, 1676, 2320, 2044]`.
  - `#32` title moved from `[1438, 2150, 2298, 2222]` to `[1438, 2092, 2298, 2164]`.
  - `#33` text_block moved from `[1438, 2210, 2298, 3118]` to `[1438, 2176, 2298, 2974]`.
  - `#34` equation_isolated moved from `[1438, 3100, 2298, 3212]` to `[1438, 2996, 2298, 3098]`.
  - `#35` text_block moved from `[1438, 3196, 2298, 3448]` to `[1438, 3120, 2298, 3286]`.
  - `#36` title moved from `[1438, 3460, 2320, 3570]` to `[1438, 3312, 2320, 3398]`.
  - `#37` text_block moved from `[1438, 3560, 2320, 4155]` to `[1438, 3408, 2320, 3988]`.
  - `#38` text_block moved from `[1438, 4148, 2320, 4568]` to `[1438, 3996, 2320, 4442]`.
  - `#39` title moved from `[1438, 4582, 2320, 4660]` to `[1438, 4460, 2320, 4528]`.
  - `#40` text_block moved from `[1438, 4635, 1888, 4930]` to `[1438, 4530, 1888, 4830]`.
  - `#41` text_block moved from `[1836, 4635, 2320, 4865]` to `[1836, 4530, 2320, 4772]`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `0`.
- Non-bbox semantic changes recorded in this pass: `0`.

Verification:

- Report with full old/new bbox details: `reports/pdb_education_textbook017_right_column_v585.json`.
- Visual dry-run cover checks: `cover_audit_education_textbook017_right_column_v585_dry/`, `cover_audit_education_textbook017_right_column_v585_dry2/`, and `cover_audit_education_textbook017_right_column_v585_dry3/`.
- Visual dry-run outline checks: `outline_audit_education_textbook017_right_column_v585_dry/`, `outline_audit_education_textbook017_right_column_v585_dry2/`, and `outline_audit_education_textbook017_right_column_v585_dry3/`.
- Visual cover check directory: `cover_audit_education_textbook017_right_column_v585/`.
- Non-cover outline preview directory: `outline_audit_education_textbook017_right_column_v585/`.
- Static validation: final run finishes `textbook_017_神经科学_记忆编码与突触可塑性` with `45/45 boxed`, `0 no bbox`, and `0 low-similarity`; final run reports `changed_annotations=13`, `added_annotations=0`, `removed_annotations=0`, and `non_bbox_semantic_changes=0`.
- Visual dry-run note: cover/outline crops confirmed `#29-#31` separate the Neural Coding title and two paragraphs, `#32-#35` separate the Research Note title/body/formula/explanation without cross-covering, `#36-#38` align with the consolidation title and two body paragraphs including the final lines, and `#39-#41` align with the Key Terms title and left/right columns.
- Frontend verification: opened `textbook_017_神经科学_记忆编码与突触可塑性` with `cb=20260610_education_textbook017_right_column_v585`; the app header shows `data 20260610_education_textbook017_right_column_v585`, script URLs include `review_data.js?20260610_education_textbook017_right_column_v585` and `app.js?20260610_education_textbook017_right_column_v585`, and the active case status shows `45/45 boxed · 0 no bbox · 45 open`. The SVG overlay reports the updated rects for `#29-#41`, including `#32 [1438,2092,2298,2164]`, `#33 [1438,2176,2298,2974]`, `#34 [1438,2996,2298,3098]`, `#35 [1438,3120,2298,3286]`, `#37 [1438,3408,2320,3988]`, `#38 [1438,3996,2320,4442]`, and `#40 [1438,4530,1888,4830]`.
- Latest token after this repair: `20260610_education_textbook017_right_column_v585`.

## 20260610_education_textbook032_footer_refs_v586

Scope:

- Follow-up visual bbox repair for `02_education/01_textbook/textbook_032_比较文学_神话叙事`.
- User-visible issue: the bottom Further Reading / footnotes / page-number region still had visible bbox drift even though the case was counted as `51/51 boxed`. The right reading-list references `#40-#45` were vertically mis-segmented, the four footnotes `#46-#49` overlapped adjacent note lines, and `#50` was below the actual page number.
- This token is bbox-only. It does not change GT type/text/preview/quality semantics, does not add annotations, and does not delete annotations.

Token:

- v586: `20260610_education_textbook032_footer_refs_v586`

Method:

- Added `scripts/fix_education_textbook032_footer_refs_v586.py`.
- Checked the source HTML for the six Further Reading entries, four footnote lines, and page footer.
- Inspected clean-PNG grid crops for the right reference box and bottom footnote/page-number area, then ran dry-run cover/outline visual checks before writing the formal token.
- Updated `review_data.json`, `review_data.js`, and `index.html` query/cache token.

Case-level changes:

- `textbook_032_比较文学_神话叙事`: changed `11` existing bbox slots; boxed stayed `51/51`; no-bbox stayed `0`; low-similarity stayed `0`.
  - `#40` reference moved from `[1500, 3200, 2228, 3360]` to `[1500, 3192, 2228, 3288]`.
  - `#41` reference moved from `[1500, 3320, 2228, 3430]` to `[1500, 3288, 2228, 3368]`.
  - `#42` reference moved from `[1500, 3410, 2228, 3530]` to `[1500, 3382, 2228, 3458]`.
  - `#43` reference moved from `[1500, 3490, 2228, 3605]` to `[1500, 3464, 2228, 3558]`.
  - `#44` reference moved from `[1500, 3560, 2228, 3665]` to `[1500, 3556, 2228, 3628]`.
  - `#45` reference moved from `[1500, 3635, 2228, 3745]` to `[1500, 3628, 2228, 3688]`.
  - `#46` reference moved from `[155, 3710, 2382, 3840]` to `[95, 3728, 2295, 3808]`.
  - `#47` reference moved from `[155, 3785, 2382, 3910]` to `[95, 3810, 2295, 3884]`.
  - `#48` reference moved from `[155, 3855, 2382, 3990]` to `[95, 3886, 2220, 3925]`.
  - `#49` reference moved from `[155, 3920, 2382, 4090]` to `[95, 3924, 2295, 3995]`.
  - `#50` page_number moved from `[1125, 4100, 1300, 4148]` to `[1000, 4014, 1268, 4054]`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `0`.
- Non-bbox semantic changes recorded in this pass: `0`.

Verification:

- Report with full old/new bbox details: `reports/pdb_education_textbook032_footer_refs_v586.json`.
- Visual dry-run cover checks: `cover_audit_education_textbook032_footer_refs_v586_dry/`.
- Visual dry-run outline checks: `outline_audit_education_textbook032_footer_refs_v586_dry/`.
- Visual cover check directory: `cover_audit_education_textbook032_footer_refs_v586/`.
- Non-cover outline preview directory: `outline_audit_education_textbook032_footer_refs_v586/`.
- Static validation: final run finishes `textbook_032_比较文学_神话叙事` with `51/51 boxed`, `0 no bbox`, and `0 low-similarity`; final run reports `changed_annotations=11`, `added_annotations=0`, `removed_annotations=0`, and `non_bbox_semantic_changes=0`.
- Visual dry-run note: cover/outline crops confirmed `#40-#45` are separated by individual Further Reading entries, `#46-#49` align with the four distinct footnotes without cross-covering adjacent lines, and `#50` is limited to the page number `— 112 —`.
- Frontend verification: opened `textbook_032_比较文学_神话叙事` with `cb=20260610_education_textbook032_footer_refs_v586`; the app header shows `data 20260610_education_textbook032_footer_refs_v586`, script URLs include `review_data.js?20260610_education_textbook032_footer_refs_v586` and `app.js?20260610_education_textbook032_footer_refs_v586`, and the active case status shows `51/51 boxed · 0 no bbox · 51 open`. The SVG overlay reports the updated rects for `#40-#50`, including `#40 [1500,3192,2228,3288]`, `#45 [1500,3628,2228,3688]`, `#46 [95,3728,2295,3808]`, `#47 [95,3810,2295,3884]`, `#48 [95,3886,2220,3925]`, `#49 [95,3924,2295,3995]`, and `#50 [1000,4014,1268,4054]`.
- Latest token after this repair: `20260610_education_textbook032_footer_refs_v586`.

## 20260610_education_exam011_visual_v587

Scope:

- Follow-up visual bbox repair for `02_education/02_exam_paper/exam_paper_011_高考数学_理科`.
- User-visible issue: the top multiple-choice region still had visible offset and uneven option-box sizes, and several later solution annotations were incorrectly drawn inside the choice area. Boxed/no-bbox statistics alone were not sufficient because the case already showed `102/102 boxed`.
- This token is bbox-only. It does not change GT type/text/preview semantics, does not add annotations, and does not delete annotations.

Token:

- v587: `20260610_education_exam011_visual_v587`

Method:

- Added `scripts/fix_education_exam011_visual_v587.py`.
- Checked the source HTML structure for the choice columns, fill questions, solution subparts, score table, hints, optional questions, and footer.
- Generated clean-PNG grid crops and dry-run cover/outline previews; iterated dry-run coordinates for the left #6 choice group and right #10-#12 choice groups before writing the formal token.
- Updated `review_data.json`, `review_data.js`, and `index.html` query/cache token.

Case-level changes:

- `exam_paper_011_高考数学_理科`: changed `91` existing bbox slots; boxed stayed `102/102`; no-bbox stayed `0`; low-similarity changed `11` -> `0`.
- Changed bbox indices: `#11-#101`.
- Selection-area regrouping:
  - `#11-#41`: rebuilt the left-column choice-title, question-stem, and option boxes for questions 1-6 so each stem/option has its own visually aligned bbox instead of tall overlapping row blocks.
  - `#42-#71`: rebuilt the right-column question-stem and option boxes for questions 7-12; the largest old shifts were `#47`, `#52`, `#57`, `#62`, and `#67`, which previously covered later questions/options.
- Fill/solution/optional-area regrouping:
  - `#72-#77`: separated the fill-section title, four fill questions, and solution-section title so they no longer overlap the same horizontal rows.
  - `#78-#89`: separated problem 17, its subparts, hint, problem 18, its subparts/hint, and problem 19 entries.
  - `#90-#93`: separated problem 20 prompt, score table, follow-up question, and formula hint.
  - `#94-#97`: moved problem 21 and its two subparts/hint back from the choice area to the lower solution area.
  - `#98-#101`: separated optional-question title, question 22, question 23, and the footer page number.
- Key old/new bbox repairs for the visibly wrong or oversized boxes:
  - `#17` q2 stem moved from `[279, 539, 1200, 835]` to `[236, 645, 650, 710]`.
  - `#22` q3 stem moved from `[217, 745, 1569, 797]` to `[236, 787, 785, 830]`.
  - `#27` q4 stem moved from `[279, 803, 950, 1026]` to `[236, 892, 760, 935]`.
  - `#32` q5 stem moved from `[279, 930, 1121, 1212]` to `[236, 985, 910, 1045]`.
  - `#37` q6 stem moved from `[279, 973, 950, 1308]` to `[236, 1105, 790, 1170]`.
  - `#47` q8 stem moved from `[1322, 581, 2248, 842]` to `[1322, 650, 1840, 725]`.
  - `#52` q9 stem moved from `[1322, 628, 2317, 976]` to `[1322, 805, 2315, 890]`.
  - `#57` q10 stem moved from `[1323, 885, 2191, 1191]` to `[1322, 925, 2200, 980]`.
  - `#62` q11 stem moved from `[1323, 1058, 2046, 1294]` to `[1322, 1090, 2100, 1170]`.
  - `#67` q12 stem moved from `[1322, 1145, 2338, 1614]` to `[1322, 1328, 2338, 1485]`.
  - `#78` problem 17 stem moved from `[217, 1805, 2343, 2203]` to `[235, 1950, 1225, 1995]`.
  - `#79` problem 17 subpart I moved from `[473, 624, 532, 705]` to `[235, 2000, 460, 2040]`.
  - `#80` problem 17 subpart II moved from `[473, 624, 532, 668]` to `[235, 2045, 735, 2085]`.
  - `#82` problem 18 stem moved from `[128, 2073, 2343, 2390]` to `[235, 2165, 1790, 2205]`.
  - `#83` problem 18 subpart I moved from `[283, 746, 305, 789]` to `[235, 2210, 455, 2250]`.
  - `#84` problem 18 subpart II moved from `[531, 761, 544, 799]` to `[235, 2255, 980, 2295]`.
  - `#86` problem 19 stem moved from `[638, 761, 650, 799]` to `[235, 2345, 835, 2388]`.
  - `#87` problem 19 subpart I moved from `[686, 761, 699, 799]` to `[235, 2395, 490, 2435]`.
  - `#88` problem 19 subpart II moved from `[795, 761, 807, 799]` to `[235, 2450, 870, 2490]`.
  - `#92` problem 20 follow-up moved from `[217, 2668, 2248, 2906]` to `[235, 2755, 2185, 2808]`.
  - `#93` problem 20 hint moved from `[283, 2783, 1018, 2859]` to `[235, 2820, 965, 2865]`.
  - `#94` problem 21 stem moved from `[283, 3035, 662, 3111]` to `[235, 2950, 775, 2990]`.
  - `#95` problem 21 subpart I moved from `[283, 847, 305, 890]` to `[235, 3000, 555, 3040]`.
  - `#96` problem 21 subpart II moved from `[510, 839, 523, 877]` to `[235, 3050, 980, 3090]`.
  - Full old/new bbox details for all `#11-#101` are stored in `reports/pdb_education_exam011_visual_v587.json`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `0`.
- Non-bbox semantic changes recorded in this pass: `0`.

Verification:

- Report with full old/new bbox details: `reports/pdb_education_exam011_visual_v587.json`.
- Visual dry-run cover checks: `cover_audit_education_exam011_visual_v587_dry/`, `cover_audit_education_exam011_visual_v587_dry2/`, and `cover_audit_education_exam011_visual_v587_dry3/`.
- Visual dry-run outline checks: `outline_audit_education_exam011_visual_v587_dry/`, `outline_audit_education_exam011_visual_v587_dry2/`, and `outline_audit_education_exam011_visual_v587_dry3/`.
- Visual cover check directory: `cover_audit_education_exam011_visual_v587/`.
- Non-cover outline preview directory: `outline_audit_education_exam011_visual_v587/`.
- Static validation: final run finishes `exam_paper_011_高考数学_理科` with `102/102 boxed`, `0 no bbox`, and `0 low-similarity`; final run reports `changed_annotations=91`, `added_annotations=0`, `removed_annotations=0`, and `non_bbox_semantic_changes=0`.
- Visual dry-run note: cover/outline crops confirmed the choice boxes no longer contain the old solution labels `#79/#80/#83/#84/#86/#87/#88/#95/#96`; those boxes are back in the lower solution area. The adjusted `#32-#41` and `#57-#71` groups were re-checked after dry-run correction so the bottom of the choice columns is not shifted into the next question.
- Frontend verification: opened `exam_paper_011_高考数学_理科` with `cb=20260610_education_exam011_visual_v587`; the app header shows `data 20260610_education_exam011_visual_v587`, script URLs include `review_data.js?20260610_education_exam011_visual_v587` and `app.js?20260610_education_exam011_visual_v587`, and the active case status shows `102/102 boxed · 0 no bbox · 102 open`. The SVG overlay reports the updated rects for key repaired boxes, including `#17 [236,645,650,710]`, `#32 [236,985,910,1045]`, `#37 [236,1105,790,1170]`, `#52 [1322,805,2315,890]`, `#57 [1322,925,2200,980]`, `#62 [1322,1090,2100,1170]`, `#67 [1322,1328,2338,1485]`, `#79 [235,2000,460,2040]`, `#80 [235,2045,735,2085]`, `#83 [235,2210,455,2250]`, `#84 [235,2255,980,2295]`, `#86 [235,2345,835,2388]`, `#88 [235,2450,870,2490]`, `#93 [235,2820,965,2865]`, `#95 [235,3000,555,3040]`, and `#96 [235,3050,980,3090]`.
- Latest token after this repair: `20260610_education_exam011_visual_v587`.

## 20260610_education_exam036_footer_v588

Scope:

- Follow-up visual bbox repair for `02_education/02_exam_paper/exam_paper_036_Economics_Market_Macro`.
- User-visible issue: the bottom of the page still had visible drift. The market-structure table and q14(2) were shifted into the Essay Questions area; the Essay Questions title and prompts `#58-#60` were collapsed into left-side fragments; the three footnotes and footer `#61-#64` were below or overlapping the actual rendered text; and `#63` had no bbox.
- This token is bbox-only. It does not change GT type/text semantics, does not add annotations, and does not delete annotations.

Token:

- v588: `20260610_education_exam036_footer_v588`

Method:

- Added `scripts/fix_education_exam036_footer_v588.py`.
- Checked the source HTML for the Table 2 block, q14 subquestions, Essay Questions section, footnotes, and absolute footer.
- Generated clean-PNG grid crops plus dry-run cover/outline previews; adjusted the q15 and q17 right edges after the cover crop showed edge text was too tight.
- Updated `review_data.json`, `review_data.js`, and `index.html` query/cache token.

Case-level changes:

- `exam_paper_036_Economics_Market_Macro`: changed `12` existing bbox slots; boxed changed `64/65` -> `65/65`; no-bbox changed `1` -> `0`; low-similarity changed `13` -> `11`.
- Changed bbox indices: `#53-#64`.
- Key old/new bbox repairs:
  - `#53` table caption moved from `[754, 2404, 1476, 2447]` to `[636, 2399, 1482, 2445]`.
  - `#54` market-structure table moved from `[754, 2510, 2220, 2836]` to `[636, 2441, 1696, 2734]`.
  - `#55` q14(1) moved from `[198, 2745, 1715, 2792]` to `[198, 2738, 1722, 2782]`.
  - `#56` q14(2) moved from `[200, 2873, 2240, 2926]` to `[198, 2778, 2240, 2838]`.
  - `#57` Essay Questions title moved from `[209, 2936, 1224, 2957]` to `[168, 2844, 1264, 2888]`.
  - `#58` q15 prompt moved from `[170, 2980, 290, 3016]` to `[170, 2898, 2330, 2984]`.
  - `#59` q16 prompt moved from `[170, 3081, 290, 3117]` to `[170, 3000, 2230, 3112]`.
  - `#60` q17 prompt moved from `[170, 3215, 289, 3251]` to `[170, 3136, 2310, 3210]`.
  - `#61` footnote 1 moved from `[170, 3332, 863, 3359]` to `[170, 3232, 770, 3262]`.
  - `#62` footnote 2 moved from `[170, 3360, 888, 3369]` to `[170, 3262, 1270, 3291]`.
  - `#63` footnote 3 received a bbox, from `null` to `[170, 3292, 1010, 3321]`.
  - `#64` footer/page number moved from `[181, 3317, 2269, 3338]` to `[170, 3308, 2268, 3335]`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `1` (`#63`).
- Cleared existing bbox values: `0`.
- Non-bbox semantic changes recorded in this pass: `0`.

Verification:

- Report with full old/new bbox details: `reports/pdb_education_exam036_footer_v588.json`.
- Visual dry-run cover checks: `cover_audit_education_exam036_footer_v588_dry/` and `cover_audit_education_exam036_footer_v588_dry2/`.
- Visual dry-run outline checks: `outline_audit_education_exam036_footer_v588_dry/` and `outline_audit_education_exam036_footer_v588_dry2/`.
- Visual cover check directory: `cover_audit_education_exam036_footer_v588/`.
- Non-cover outline preview directory: `outline_audit_education_exam036_footer_v588/`.
- Static validation: final run finishes `exam_paper_036_Economics_Market_Macro` with `65/65 boxed`, `0 no bbox`, and `11 low-similarity`; final run reports `changed_annotations=12`, `added_annotations=0`, `removed_annotations=0`, `bbox_added_to_existing_annotations=[63]`, and `non_bbox_semantic_changes=0`.
- Visual dry-run note: cover/outline crops confirmed `#53` includes the full table caption, `#54` is limited to the visible table, `#56` no longer covers the Essay Questions title, `#58-#60` cover the full essay prompts instead of the left-side fragments, `#61-#63` align to the three footnotes, and `#64` aligns with the absolute footer line. The `#63/#64` overlap is retained because the rendered HTML footer visually overlaps the third footnote.
- Frontend verification: opened `exam_paper_036_Economics_Market_Macro` with `cb=20260610_education_exam036_footer_v588`; the app header shows `data 20260610_education_exam036_footer_v588`, script URLs include `review_data.js?20260610_education_exam036_footer_v588` and `app.js?20260610_education_exam036_footer_v588`, and the active case status shows `65/65 boxed · 0 no bbox · 65 open`. The SVG overlay reports the updated rects for `#53-#64`, including `#53 [636,2399,1482,2445]`, `#54 [636,2441,1696,2734]`, `#56 [198,2778,2240,2838]`, `#58 [170,2898,2330,2984]`, `#60 [170,3136,2310,3210]`, `#61 [170,3232,770,3262]`, `#62 [170,3262,1270,3291]`, `#63 [170,3292,1010,3321]`, and `#64 [170,3308,2268,3335]`.
- Latest token after this repair: `20260610_education_exam036_footer_v588`.

## 20260610_education_exam041_part4_v589

Scope:

- Follow-up visual bbox repair for `02_education/02_exam_paper/exam_paper_041_Forensic_Science_Exam`.
- User-visible issue: `#54` was visibly shifted into the timeline/table area near the `09:00` autopsy row, even though its GT text is the final `— END OF PAPER · 试卷结束 —` footer. Visual inspection also found the same tail-section drift for the Part IV title and essay prompts `#50/#51/#53`.
- This token is bbox-only. It does not change GT type/text semantics, does not add annotations, and does not delete annotations.

Token:

- v589: `20260610_education_exam041_part4_v589`

Method:

- Added `scripts/fix_education_exam041_part4_v589.py`.
- Checked the source HTML for the Part III timeline/table, Part IV essay section, Question 8/9 prompts, and page footer.
- Generated clean-PNG crops plus dry-run cover/outline previews around the timeline/table and Part IV footer regions before writing the formal token.
- Updated `review_data.json`, `review_data.js`, and `index.html` query/cache token.

Case-level changes:

- `exam_paper_041_Forensic_Science_Exam`: changed `5` existing bbox slots; boxed stayed `55/55`; no-bbox stayed `0`; low-similarity changed `6` -> `2`.
- Changed bbox indices: `#48`, `#50`, `#51`, `#53`, `#54`.
- Key old/new bbox repairs:
  - `#48` Part IV title expanded from `[115, 4986, 792, 5016]` to `[115, 4960, 1572, 5018]` so it includes `[35 marks] — Answer ONE question 任选一题`.
  - `#50` Question 8 quote moved from `[123, 312, 1542, 334]` to `[90, 5068, 1545, 5168]`.
  - `#51` Question 8 essay prompt moved from `[113, 382, 1552, 462]` to `[90, 5172, 1570, 5290]`.
  - `#53` Question 9 essay prompt moved from `[841, 587, 1054, 611]` to `[90, 5340, 1570, 5474]`.
  - `#54` final footer moved from `[363, 4100, 757, 4122]` to `[438, 5492, 1228, 5524]`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `0`.
- Non-bbox semantic changes recorded in this pass: `0`.

Verification:

- Report with full old/new bbox details: `reports/pdb_education_exam041_part4_v589.json`.
- Visual dry-run cover checks: `cover_audit_education_exam041_part4_v589_dry/`.
- Visual dry-run outline checks: `outline_audit_education_exam041_part4_v589_dry/`.
- Visual cover check directory: `cover_audit_education_exam041_part4_v589/`.
- Non-cover outline preview directory: `outline_audit_education_exam041_part4_v589/`.
- Static validation: final run finishes `exam_paper_041_Forensic_Science_Exam` with `55/55 boxed`, `0 no bbox`, and `2 low-similarity`; final run reports `changed_annotations=5`, `added_annotations=0`, `removed_annotations=0`, and `non_bbox_semantic_changes=0`.
- Visual dry-run note: cover/outline crops confirmed `#54` no longer appears in the timeline/table area and now aligns with the final page footer. The Part IV title `#48` includes the right-side marks/instruction text, `#50/#51` cover the Question 8 quote and essay prompt, and `#53` covers the Question 9 digital-forensics prompt without absorbing the `Question 9` label `#52`.
- Frontend verification: opened `exam_paper_041_Forensic_Science_Exam` with `cb=20260610_education_exam041_part4_v589`; the app header shows `data 20260610_education_exam041_part4_v589`, script URLs include `review_data.js?20260610_education_exam041_part4_v589` and `app.js?20260610_education_exam041_part4_v589`, and the active case status shows `55/55 boxed · 0 no bbox · 55 open`. The SVG overlay reports the updated rects for repaired boxes, including `#48 [115,4960,1572,5018]`, `#50 [90,5068,1545,5168]`, `#51 [90,5172,1570,5290]`, `#53 [90,5340,1570,5474]`, and `#54 [438,5492,1228,5524]`.
- Latest token after this repair: `20260610_education_exam041_part4_v589`.

## 20260610_education_exam042_tail_v590

Scope:

- Follow-up visual bbox repair for `02_education/02_exam_paper/exam_paper_042_Astronomy_Observational`.
- User-visible issue: the region after `#60` was still visibly shifted. Visual inspection also found earlier tail-section drift in q10(a) `#55`, q11(a) `#58`, the appendix formulas/constants `#64-#66`, and the footer/footnotes `#67/#68`.
- This token is bbox-only. It does not change GT type/text semantics, does not add annotations, and does not delete annotations.

Token:

- v590: `20260610_education_exam042_tail_v590`

Method:

- Added `scripts/fix_education_exam042_tail_v590.py`.
- Checked the source HTML for the Part IV q10-q12 blocks, appendix formula/constants box, absolute footer, and footnotes.
- Generated dry-run cover/outline previews before writing the formal token. After the first dry-run, widened `#66` to include the final `1 AU...` constant line and widened/lowered `#67` to include all four footnotes.
- Updated `review_data.json`, `review_data.js`, and `index.html` query/cache token.

Case-level changes:

- `exam_paper_042_Astronomy_Observational`: changed `14` existing bbox slots; boxed changed `67/69` -> `69/69`; no-bbox changed `2` -> `0`; low-similarity changed `16` -> `12`.
- Changed bbox indices: `#55-#68`.
- Key old/new bbox repairs:
  - `#55` q10(a) moved from `[126, 7858, 2376, 7923]` to `[118, 7568, 2250, 7628]`.
  - `#56` q10(b) tightened from `[117, 7844, 1750, 7884]` to `[118, 7838, 1750, 7885]`.
  - `#57` q11 title tightened from `[88, 8041, 2296, 8082]` to `[88, 8036, 2296, 8078]`.
  - `#58` q11(a) moved from `[126, 8392, 2280, 8423]` to `[118, 8088, 2248, 8128]`.
  - `#59` q11(b) tightened from `[117, 8285, 1642, 8325]` to `[118, 8284, 1648, 8326]`.
  - `#60` q12 title tightened from `[88, 8440, 2296, 8477]` to `[88, 8438, 2296, 8478]`.
  - `#61` q12(a) moved from `[118, 8549, 997, 8594]` to `[118, 8540, 1002, 8582]`.
  - `#62` q12(b) moved from `[118, 8581, 802, 8629]` to `[118, 8580, 806, 8622]`.
  - `#63` q12(c) tightened from `[117, 8618, 1390, 8657]` to `[118, 8614, 1392, 8658]`.
  - `#64` appendix title moved from `[85, 9034, 939, 9093]` to `[118, 9038, 940, 9084]`.
  - `#65` formula body moved from `[85, 9013, 555, 9344]` to `[118, 9086, 1608, 9332]`.
  - `#66` constants moved from `[2039, 265, 2232, 296]` to `[1198, 9248, 1608, 9412]`.
  - `#67` footnotes received a bbox, from `null` to `[90, 9490, 1088, 9594]`.
  - `#68` footer/page number received a bbox, from `null` to `[90, 9438, 2290, 9478]`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `2` (`#67`, `#68`).
- Cleared existing bbox values: `0`.
- Non-bbox semantic changes recorded in this pass: `0`.

Verification:

- Report with full old/new bbox details: `reports/pdb_education_exam042_tail_v590.json`.
- Visual dry-run cover check directory: `cover_audit_education_exam042_tail_v590_dry/`.
- Visual dry-run outline check directory: `outline_audit_education_exam042_tail_v590_dry/`.
- Visual cover check directory: `cover_audit_education_exam042_tail_v590/`.
- Non-cover outline preview directory: `outline_audit_education_exam042_tail_v590/`.
- Static validation: final run finishes `exam_paper_042_Astronomy_Observational` with `69/69 boxed`, `0 no bbox`, and `12 low-similarity`; final run reports `changed_annotations=14`, `added_annotations=0`, `removed_annotations=0`, `bbox_added_to_existing_annotations=[67, 68]`, and `non_bbox_semantic_changes=0`.
- Visual dry-run note: cover/outline crops confirmed `#55` and `#58` are back on their q10(a)/q11(a) question lines, `#60-#63` align to the q12 title and subquestions, `#64` is limited to the appendix title, `#65/#66` cover the formula/constants text including the bottom `1 AU...` line, and `#67/#68` cover the footnotes/footer without the old missing-bbox drift.
- Frontend verification: opened `exam_paper_042_Astronomy_Observational` with `cb=20260610_education_exam042_tail_v590`; the app header shows `data 20260610_education_exam042_tail_v590`, script URLs include `review_data.js?20260610_education_exam042_tail_v590` and `app.js?20260610_education_exam042_tail_v590`, and the active case status shows `69/69 boxed · 0 no bbox · 69 open`. The SVG overlay reports the updated rects for `#55-#68`, including `#55 [118,7568,2250,7628]`, `#58 [118,8088,2248,8128]`, `#60 [88,8438,2296,8478]`, `#61 [118,8540,1002,8582]`, `#62 [118,8580,806,8622]`, `#63 [118,8614,1392,8658]`, `#64 [118,9038,940,9084]`, `#65 [118,9086,1608,9332]`, `#66 [1198,9248,1608,9412]`, `#67 [90,9490,1088,9594]`, and `#68 [90,9438,2290,9478]`.
- Latest token after this repair: `20260610_education_exam042_tail_v590`.

## 20260610_education_exam047_em_visual_v591

Scope:

- Follow-up visual bbox repair for `02_education/02_exam_paper/exam_paper_047_大学期末_电磁场与电磁波`.
- User-visible issue: many elements were visually misaligned despite the case showing `80/80 boxed`. The drift affected Part II diagram labels, the Part III boundary-condition figure and right-column formula/question blocks, the Part IV/Part V lower cards, the derivation table rows, the answer-area notes, and the footer.
- This token is bbox-only. It does not change GT type/text semantics, does not add annotations, and does not delete annotations.

Token:

- v591: `20260610_education_exam047_em_visual_v591`

Method:

- Added `scripts/fix_education_exam047_em_visual_v591.py`.
- Checked the source HTML for the Part II conductor/dielectric diagram, Part III boundary-condition analysis, Part IV wave-propagation block, Part V derivation/calculation block, answer panels, notes, and footer.
- Generated clean-PNG grid crops plus dry-run cover/outline previews before writing the formal token.
- Updated `review_data.json`, `review_data.js`, and `index.html` query/cache token.

Case-level changes:

- `exam_paper_047_大学期末_电磁场与电磁波`: changed `58` existing bbox slots; boxed stayed `80/80`; no-bbox stayed `0`; low-similarity changed `16` -> `0`.
- Changed bbox indices: `#19`, `#21`, and `#24-#79`.
- New bbox values by visual region:
  - Part I/II figure labels: `#19 [388,1150,472,1184]`, `#21 [780,1162,900,1194]`, `#24 [1350,618,1500,654]`, `#25 [1868,604,1956,640]`, `#26 [1214,946,1324,982]`, `#27 [1320,946,1560,982]`, `#28 [1206,988,2298,1078]`, `#29 [1382,1082,1510,1116]`, `#30 [1810,1082,2030,1116]`, `#31 [1600,1068,1685,1104]`, `#32 [1370,1324,1648,1360]`.
  - Part III title/text/diagram/table: `#33 [34,1424,2298,1502]`, `#34 [54,1510,1652,1552]`, `#35 [130,1618,330,1655]`, `#36 [130,1858,330,1895]`, `#37 [970,1806,1142,1840]`, `#38 [174,2068,492,2102]`, `#39 [718,1988,888,2022]`, `#40 [54,2184,760,2224]`, `#41 [1254,1568,2298,1778]`.
  - Part III formulas/questions: `#42 [1254,1790,2298,1928]`, `#43 [1254,1936,2298,2070]`, `#44 [1254,2030,2298,2136]`, `#45 [1254,2150,2298,2228]`.
  - Part IV wave-propagation block: `#46 [34,2263,1166,2338]`, `#47 [54,2366,1146,2468]`, `#48 [238,2856,560,2892]`, `#49 [774,2532,906,2566]`, `#50 [54,2948,1146,3046]`, `#51 [54,3074,1146,3156]`.
  - Part V derivation/calculation block: `#52 [1205,2263,2298,2338]`, `#53 [1220,2362,2290,2430]`, `#54 [1220,2440,1612,2474]`, `#55 [1220,2486,1454,2520]`, `#56 [1220,2528,2044,2562]`, `#57 [1334,2888,1586,2924]`, `#58 [2070,2734,2164,2764]`, `#59 [1790,2628,2078,2660]`, `#60 [1205,2960,2298,3012]`, `#61 [1205,3012,2298,3064]`, `#62 [1205,3064,2298,3120]`, `#63 [1205,3120,2298,3164]`, `#64 [1205,3182,2298,3278]`.
  - Answer area and footer: `#65 [54,3334,264,3374]`, `#66 [54,3384,1564,3440]`, `#67 [1060,3458,1248,3490]`, `#68 [1288,3482,1510,3518]`, `#69 [1290,3528,1838,3558]`, `#70 [1290,3558,2060,3590]`, `#71 [1290,3590,2260,3624]`, `#72 [1290,3624,2060,3658]`, `#73 [2098,3670,2298,3706]`, `#74 [54,4048,868,4162]`, `#75 [880,4048,1582,4162]`, `#76 [1596,4048,2298,4162]`, `#77 [54,4214,2298,4258]`, `#78 [54,4268,640,4304]`, `#79 [2218,4268,2298,4304]`.
- Key old/new bbox repairs for visibly wrong items:
  - `#21` vector-basis label tightened from `[648,1083,1026,1326]` to `[780,1162,900,1194]`.
  - `#24/#25/#29/#30/#32` moved from unrelated top/left text areas back to the Part II diagram labels.
  - `#34` explanatory line moved from the Part III title row `[0,1426,2093,1503]` to `[54,1510,1652,1552]`.
  - `#35/#36/#37/#38/#39` moved from the legend/top page areas back to the Part III interface diagram.
  - `#42/#43/#44/#45` were rebuilt as separate right-column formula/question boxes instead of cross-column oversized rectangles.
  - `#47/#50/#51` no longer span into the right column; `#52-#64` no longer span from the Part V title into the wrong figure/table rows.
  - `#68-#73` were moved from the top answer-meta strip to the right-side working-notes and calculation-sheet labels.
  - `#74-#79` were tightened to the three note cards, footnote line, department footer, and page number.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `0`.
- Non-bbox semantic changes recorded in this pass: `0`.

Verification:

- Report with full old/new bbox details: `reports/pdb_education_exam047_em_visual_v591.json`.
- Visual dry-run cover check directory: `cover_audit_education_exam047_em_visual_v591_dry/`.
- Visual dry-run outline check directory: `outline_audit_education_exam047_em_visual_v591_dry/`.
- Visual cover check directory: `cover_audit_education_exam047_em_visual_v591/`.
- Non-cover outline preview directory: `outline_audit_education_exam047_em_visual_v591/`.
- Static validation: final run finishes `exam_paper_047_大学期末_电磁场与电磁波` with `80/80 boxed`, `0 no bbox`, and `0 low-similarity`; final run reports `changed_annotations=58`, `added_annotations=0`, `removed_annotations=0`, `bbox_added_to_existing_annotations=[]`, and `non_bbox_semantic_changes=0`.
- Visual dry-run note: cover/outline crops confirmed Part II labels `#24-#32`, Part III `#33-#45`, Part IV `#46-#51`, Part V `#52-#64`, and answer/footer `#65-#79` now align with their visible elements. The Part II caption is visually one connected line but GT splits it as `#26 induced E` and `#27 loop integral sketch`, so the two bboxes intentionally sit on the same rendered caption line.
- Frontend verification: opened `exam_paper_047_大学期末_电磁场与电磁波` with `cb=20260610_education_exam047_em_visual_v591`; the app header shows `data 20260610_education_exam047_em_visual_v591`, script URLs include `review_data.js?20260610_education_exam047_em_visual_v591` and `app.js?20260610_education_exam047_em_visual_v591`, and the active case status shows `80/80 boxed · 0 no bbox · 80 open`. The SVG overlay reports the updated rects for key repaired boxes, including `#21 [780,1162,900,1194]`, `#24 [1350,618,1500,654]`, `#33 [34,1424,2298,1502]`, `#34 [54,1510,1652,1552]`, `#42 [1254,1790,2298,1928]`, `#46 [34,2263,1166,2338]`, `#52 [1205,2263,2298,2338]`, `#60 [1205,2960,2298,3012]`, `#64 [1205,3182,2298,3278]`, `#74 [54,4048,868,4162]`, `#77 [54,4214,2298,4258]`, `#78 [54,4268,640,4304]`, and `#79 [2218,4268,2298,4304]`.
- Latest token after this repair: `20260610_education_exam047_em_visual_v591`.

## 20260610_education_exam048_table_consolidate_v592

Scope:

- Follow-up GT semantic and visual bbox repair for `02_education/02_exam_paper/exam_paper_048_高频电子线路考试`.
- User-visible issue: several real HTML tables were represented as split text fragments, especially the design table after `#89`. Visual inspection also found the same table-fragment pattern at `#61-#65` and `#108-#112`, plus nearby lower-section bbox drift that pushed non-table labels into table regions.
- This token intentionally includes non-bbox GT semantic changes: retained table annotations were converted/expanded to full tables, and row-level duplicate fragments were deleted. All such changes are recorded here.

Token:

- v592: `20260610_education_exam048_table_consolidate_v592`

Method:

- Added `scripts/fix_education_exam048_table_consolidate_v592.py`.
- Checked the source HTML tables for the Part III frequency-response parameter table, Part V design table, and checkpoint mini-matrix.
- Generated coordinate crops from the clean PNG, then generated dry-run cover/outline previews before formal write.
- Updated `review_data.json`, `review_data.js`, and `index.html` query/cache token.

Case-level changes:

- `exam_paper_048_高频电子线路考试`: annotation count changed from `121` to `109`; boxed changed from `120/121` to `109/109`; no-bbox changed from `1` to `0`; low-similarity changed from `39` to `21`.
- Changed retained table annotations: `#61`, `#88`, `#108`.
  - `#61`: `text_block` -> `table`; moved from `[50, 1858, 541, 1870]` to `[1236, 1096, 2296, 1213]`; text expanded from the header-only `Circuitf0QGainBandwidthRemark` to the full Part III parameter table with four rows.
  - `#88`: kept as `table`; tightened/expanded from `[272, 1976, 2295, 2087]` to `[1236, 1976, 2296, 2095]`; text expanded from the header-only `Design Item Given To Determine Hint` to the full design table with four rows.
  - `#108`: `text_block` -> `table`; expanded from `[27, 2509, 1678, 2546]` to `[26, 2507, 2296, 2609]`; text expanded from the checkpoint header-only fragment to the full checkpoint mini-matrix with four rows.
- Bbox-only visual repairs: `43` existing annotations were moved/tightened around Part III, Part IV, Part V, scoring panels, and the tag/checkpoint transition:
  - `#54 [102, 1302, 160, 1319]`, `#55 [610, 1196, 725, 1213]`, `#56 [646, 1295, 770, 1312]`, `#57 [365, 1413, 455, 1432]`, `#58 [746, 1413, 823, 1432]`, `#59 [28, 1455, 1170, 1478]`, `#60 [28, 1491, 910, 1514]`.
  - `#67 [26, 1531, 450, 1555]`, `#68 [88, 1566, 285, 1583]`, `#69 [88, 1665, 274, 1682]`, `#70 [88, 1800, 335, 1817]`, `#71 [28, 1848, 658, 1870]`, `#72 [1228, 1594, 1320, 1610]`, `#73 [1228, 1693, 1330, 1710]`, `#74 [1228, 1795, 1330, 1812]`, `#75 [1168, 1848, 1745, 1870]`.
  - `#76 [26, 1893, 420, 1917]`, `#77 [80, 2047, 148, 2064]`, `#78 [276, 1983, 862, 2064]`, `#79 [1045, 2047, 1157, 2064]`, `#80 [448, 2154, 660, 2174]`, `#81 [448, 2177, 623, 2196]`, `#82 [28, 2216, 545, 2236]`, `#83 [28, 2248, 610, 2268]`, `#84 [1257, 1939, 1368, 1958]`, `#85 [1257, 1958, 1588, 1974]`, `#86 [1485, 1958, 1818, 1974]`, `#87 [1788, 1958, 2215, 1974]`.
  - `#93 [27, 2292, 350, 2315]`, `#94 [30, 2330, 118, 2348]`, `#95 [30, 2355, 250, 2371]`, `#96 [30, 2370, 250, 2386]`, `#97 [30, 2386, 270, 2403]`, `#98 [790, 2330, 880, 2348]`, `#99 [790, 2355, 970, 2371]`, `#100 [790, 2370, 990, 2386]`, `#101 [790, 2386, 1010, 2403]`, `#102 [1548, 2330, 1664, 2348]`, `#103 [1548, 2355, 1700, 2371]`, `#104 [1548, 2370, 1705, 2386]`, `#105 [1548, 2386, 1700, 2403]`, `#106 [1548, 2402, 1705, 2419]`, `#107 [27, 2490, 612, 2505]`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `12`.
- Removed GT annotation indices: `#62-#65`, `#89-#92`, `#109-#112`.
  - `#62-#65` were row-level fragments of the Part III frequency-response parameter table and were merged into retained table annotation `#61`.
  - `#89-#92` were row-level fragments of the Part V design table and were merged into retained table annotation `#88`.
  - `#109-#112` were row-level fragments of the checkpoint mini-matrix and were merged into retained table annotation `#108`.
- Added bbox to existing GT annotations: `1` (`#78`, from no-bbox `CpLsCload` to `[276, 1983, 862, 2064]`).
- Cleared existing bbox values: `0`.
- Non-bbox semantic changes recorded in this pass: `15` (`3` retained full-table type/text updates plus `12` row-fragment annotation deletions).

Verification:

- Report with full old/new bbox details: `reports/pdb_education_exam048_table_consolidate_v592.json`.
- Visual dry-run cover check directory: `cover_audit_education_exam048_table_consolidate_v592_dry/`.
- Visual dry-run outline check directory: `outline_audit_education_exam048_table_consolidate_v592_dry/`.
- Visual cover check directory: `cover_audit_education_exam048_table_consolidate_v592/`.
- Non-cover outline preview directory: `outline_audit_education_exam048_table_consolidate_v592/`.
- Static validation: final run finishes `exam_paper_048_高频电子线路考试` with `109/109 boxed`, `0 no bbox`, and `21 low-similarity`; final run reports `changed_retained_annotations=3`, `bbox_only_changes=43`, `bbox_added_to_existing_annotations=[78]`, `added_annotations=0`, `removed_annotations=12`, `removed_annotation_indices=[62, 63, 64, 65, 89, 90, 91, 92, 109, 110, 111, 112]`, and `non_bbox_semantic_changes=15`.
- Visual dry-run note: cover/outline crops confirmed `#61`, `#88`, and `#108` now cover the full table extents, including all header/body rows, and the table-overlap check found no remaining non-table bbox intruding into these three retained table bboxes. Adjacent drift repairs moved the Part III graph labels/questions, Part IV waveform labels/questions, Part V circuit labels/questions, design-card text, scoring focus items, and tag row back to their visible locations.
- Frontend verification: opened `exam_paper_048_高频电子线路考试` with `cb=20260610_education_exam048_table_consolidate_v592`; the app header shows `data 20260610_education_exam048_table_consolidate_v592`, script URLs include `review_data.js?20260610_education_exam048_table_consolidate_v592` and `app.js?20260610_education_exam048_table_consolidate_v592`, and the active case row shows `109/109 boxed · 0 no bbox · 109 open`. The SVG overlay reports the updated rects `#61 [1236,1096,2296,1213]`, `#78 [276,1983,862,2064]`, `#88 [1236,1976,2296,2095]`, and `#108 [26,2507,2296,2609]`; removed row-fragment ids `#62-#65`, `#89-#92`, and `#109-#112` are absent from the overlay.
- Latest token after this repair: `20260610_education_exam048_table_consolidate_v592`.

## 20260610_education_slides006012_order_visual_v593

Scope:

- Follow-up GT reading-order and visual bbox repair for two slide cases:
  - `02_education/03_slides/slides_006_医学课件_心血管系统`
  - `02_education/03_slides/slides_012_商业BP_SaaS`
- User-visible issue: the visible annotation numbers did not follow the reading order. In `slides_012`, the middle tables were labeled before the page header/KPI row; in `slides_006`, slide 5/6 table annotations were ordered before the cover, and several slide 7/8 labels had drifted onto the slide 2 heart diagram.
- This token intentionally includes non-bbox GT metadata changes: `index` and `anno_id` were reassigned to match the visual reading order. These changes are recorded here separately from bbox edits.

Token:

- v593: `20260610_education_slides006012_order_visual_v593`

Method:

- Added `scripts/fix_education_slides006012_order_visual_v593.py`.
- Generated dry-run cover/outline previews, inspected crops for `slides_012` top/table/team/footer areas and `slides_006` cover, slide 2, slide 7, and slide 8 areas, then formally wrote the repaired data.
- Updated `review_data.json`, `review_data.js`, and `index.html` query/cache token.

Case-level changes:

- `slides_006_医学课件_心血管系统`: final status `54/54 boxed`, `0 no bbox`, `0 low-similarity`.
- Reading-order remap for `slides_006`: old order `[2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 0, 21, 22, 23, 1, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53]` was reassigned to sequential `#0-#53`.
- `slides_006` old-to-new id changes: `#2->#0`, `#3->#1`, `#4->#2`, `#5->#3`, `#6->#4`, `#7->#5`, `#8->#6`, `#9->#7`, `#10->#8`, `#11->#9`, `#12->#10`, `#13->#11`, `#14->#12`, `#15->#13`, `#16->#14`, `#17->#15`, `#18->#16`, `#19->#17`, `#20->#18`, `#0->#19`, `#21->#20`, `#22->#21`, `#23->#22`, `#1->#23`; `#24-#53` kept their numeric ids after the remap.
- `slides_006` bbox repairs:
  - `#27`: `[2198, 10695, 2418, 10748]` -> `[2198, 9186, 2418, 9239]` for `Slide 7 / 8`.
  - `#28`: `[1148, 1893, 1333, 1937]` -> `[113, 9350, 830, 9412]` for the ACEI title.
  - `#29`: `[113, 9455, 1161, 9555]` -> `[113, 9455, 1088, 9558]`.
  - `#30`: `[113, 9567, 732, 9617]` -> `[113, 9570, 780, 9622]`.
  - `#31`: `[110, 9622, 1890, 9683]` -> `[113, 9622, 880, 9684]`.
  - `#32`: `[1578, 1893, 1709, 1934]` -> `[1306, 9350, 1905, 9412]` for the ARB title.
  - `#33`: `[1306, 9455, 2354, 9555]` -> `[1306, 9455, 2354, 9558]`.
  - `#34`: `[1306, 9567, 1856, 9617]` -> `[1306, 9570, 1880, 9622]`.
  - `#35`: `[1306, 9630, 1887, 9673]` -> `[1306, 9622, 2020, 9684]`.
  - `#36`: `[772, 1893, 903, 1934]` -> `[113, 9750, 580, 9812]` for the CCB title.
  - `#37`: `[110, 9851, 2308, 9905]` -> `[113, 9848, 1125, 9908]`.
  - `#38`: `[113, 9911, 732, 9961]` -> `[113, 9911, 780, 9963]`.
  - `#39`: `[113, 9973, 800, 10017]` -> `[113, 9967, 885, 10026]`.
  - `#40`: `[843, 2054, 955, 2107]` -> `[1306, 9750, 1698, 9812]` for the beta-blocker title.
  - `#41`: `[1306, 9848, 2325, 9898]` -> `[1306, 9848, 2325, 9908]`.
  - `#42`: `[1306, 9911, 1925, 9961]` -> `[1306, 9911, 1950, 9963]`.
  - `#43`: `[110, 9967, 2011, 10026]` -> `[1306, 9967, 2200, 10026]`.
  - `#45`: `[955, 2059, 1120, 2102]` -> `[2198, 10695, 2418, 10748]` for `Slide 8 / 8`.

- `slides_012_商业BP_SaaS`: final status `22/22 boxed`, `0 no bbox`, `0 low-similarity`.
- Reading-order remap for `slides_012`: old order `[4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 0, 1, 14, 2, 3, 15, 16, 17, 18, 19, 20, 21]` was reassigned to sequential `#0-#21`.
- `slides_012` old-to-new id changes: `#4->#0`, `#5->#1`, `#6->#2`, `#7->#3`, `#8->#4`, `#9->#5`, `#10->#6`, `#11->#7`, `#12->#8`, `#13->#9`, `#0->#10`, `#1->#11`, `#14->#12`, `#2->#13`, `#3->#14`; `#15-#21` kept their numeric ids after the remap.
- `slides_012` bbox repairs:
  - old `#8` -> new `#4`: `[308, 447, 2052, 491]` -> `[308, 437, 505, 491]` for `¥18.6M`.
  - old `#9` -> new `#5`: `[336, 498, 2061, 531]` -> `[338, 497, 505, 531]` for `2024 ARR`.
  - old `#0` -> new `#10`: `[169, 641, 2179, 1128]` -> `[169, 641, 1128, 1128]` for the left financial forecast table.
  - old `#1` -> new `#11`: `[169, 1190, 2137, 1514]` -> `[169, 1190, 1128, 1514]` for the left unit economics table.
  - old `#2` -> new `#13`: `[176, 1085, 2213, 1360]` -> `[1258, 1085, 2213, 1360]` for the right revenue-structure table.
  - old `#3` -> new `#14`: `[1258, 1436, 2213, 1711]` was checked and retained for the right funding-requirement table while its id moved to the correct reading position.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `0`.
- Non-bbox semantic changes recorded in this pass: `39` (`24` index/anno_id remaps in `slides_006`, `15` index/anno_id remaps in `slides_012`).

Verification:

- Report with full old/new details: `reports/pdb_education_slides006012_order_visual_v593.json`.
- Visual dry-run cover check directory: `cover_audit_education_slides006012_order_visual_v593_dry/`.
- Visual dry-run outline check directory: `outline_audit_education_slides006012_order_visual_v593_dry/`.
- Visual cover check directory: `cover_audit_education_slides006012_order_visual_v593/`.
- Non-cover outline preview directory: `outline_audit_education_slides006012_order_visual_v593/`.
- Static validation: final run reports `order_changes=39`, `bbox_changes=24`, `added_annotations=0`, `removed_annotations=0`, and `non_bbox_semantic_changes=39`. The two final case statuses are `slides_006: 54/54 boxed, 0 no bbox, 0 low-similarity` and `slides_012: 22/22 boxed, 0 no bbox, 0 low-similarity`.
- Visual dry-run note: `slides_012` crops confirmed numbering now starts from `CloudFlow`, the header, the KPI cards, then the four financial tables, team row, and footer; the two left tables no longer span into the right column, and the two KPI bboxes no longer span across the entire KPI row. `slides_006` crops confirmed numbering now starts at the cover slide and the slide 7/8 drug labels sit on the ACEI/ARB/CCB/beta-blocker cards instead of the slide 2 heart diagram.
- Frontend verification: opened both cases with `cb=20260610_education_slides006012_order_visual_v593`; the app header shows `data 20260610_education_slides006012_order_visual_v593`, script URLs include the v593 token, and SVG overlay rects report the expected new positions. Key checked rects include `slides_006 #0 [1050,383,1432,440]`, `#19 [63,6319,2418,7005]`, `#23 [63,7909,2418,8541]`, `#27 [2198,9186,2418,9239]`, `#28 [113,9350,830,9412]`, `#32 [1306,9350,1905,9412]`, `#36 [113,9750,580,9812]`, `#40 [1306,9750,1698,9812]`, `#45 [2198,10695,2418,10748]`; and `slides_012 #0 [238,122,503,185]`, `#4 [308,437,505,491]`, `#5 [338,497,505,531]`, `#10 [169,641,1128,1128]`, `#11 [169,1190,1128,1514]`, `#13 [1258,1085,2213,1360]`, `#14 [1258,1436,2213,1711]`.
- Latest token after this repair: `20260610_education_slides006012_order_visual_v593`.

## 20260610_education_slides008_python_order_visual_v594

Scope:

- Follow-up GT reading-order and visual bbox repair for `02_education/03_slides/slides_008_数据分析_Python`.
- User-visible issue: the Python data-analysis slide deck had the same ordering problem as the previous slide cases, with table annotations originally numbered before the cover; several code/table/footer bboxes were also visibly shifted. The repair treats the output/data tables as full table annotations and keeps all table annotations as whole-table boxes.
- This token intentionally includes non-bbox GT metadata changes: `index` and `anno_id` were reassigned to match the visual reading order. No category type/text changes were made in this pass.

Token:

- v594: `20260610_education_slides008_python_order_visual_v594`

Method:

- Added `scripts/fix_education_slides008_python_order_visual_v594.py`.
- Generated dry-run cover/outline previews, inspected per-slide outline crops for slides 1, 4, 6, 7, and 8, then formally wrote the repaired data.
- Updated `review_data.json`, `review_data.js`, and `index.html` query/cache token.

Case-level changes:

- `slides_008_数据分析_Python`: final status `164/164 boxed`, `0 no bbox`, `0 low-similarity`.
- Reading-order remap: old order `[4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 0, 73, 74, 75, 76, 77, 78, 79, 80, 81, 1, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 2, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 3, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163]` was reassigned to sequential `#0-#163`.
- Important old-to-new id changes: slide 1 starts at old `#4-#8` -> new `#0-#4`; slide 4 output tables old `#0` -> new `#69` and old `#1` -> new `#79`; slide 7 tables old `#2` -> new `#129` and old `#3` -> new `#141`; slide 8 old `#142-#163` retained numeric ids after the remap.
- Bbox repairs, listed as old id -> new id and final bbox:
  - Slide 1: old `#4` -> new `#0 [894,426,1550,476]`; old `#8` -> new `#4 [2246,1401,2387,1435]`.
  - Slide 2: old `#10` -> new `#6 [2146,1624,2415,1665]`; old `#20` -> new `#16 [306,2046,621,2090]`; old `#21` -> new `#17 [238,2110,621,2154]`; old `#22` -> new `#18 [238,2110,373,2154]`; old `#23` -> new `#19 [396,2110,511,2154]`; old `#24` -> new `#20 [238,2174,643,2217]`; old `#25` -> new `#21 [238,2237,846,2281]`; old `#26` -> new `#22 [396,2237,643,2281]`.
  - Slide 3: old `#42` -> new `#38 [2146,3136,2415,3177]`; old `#44` -> new `#40 [178,3332,1082,3377]`; old `#46` -> new `#42 [329,3455,1230,3502]`; old `#48` -> new `#44 [329,3585,1260,3630]`; old `#53` -> new `#49 [155,3904,970,3950]`; old `#58` -> new `#54 [155,4161,853,4205]`; old `#59` -> new `#55 [155,4161,853,4205]`; old `#62` -> new `#58 [531,4225,824,4269]`; old `#64` -> new `#60 [155,4350,895,4396]`; old `#65` -> new `#61 [155,4350,895,4396]`.
  - Slide 4: old `#68` -> new `#64 [2146,4754,2415,4795]`; old `#69` -> new `#65 [113,4932,650,4975]`; old `#70` -> new `#66 [188,5048,650,5092]`; old `#71` -> new `#67 [347,5048,471,5092]`; old `#72` -> new `#68 [188,5116,650,5160]`; old `#0` -> new `#69 [1258,4985,2415,5315]`; old `#74` -> new `#71 [113,5397,422,5435]`; old `#77` -> new `#74 [188,5522,593,5565]`; old `#80` -> new `#77 [113,5689,278,5727]`; old `#81` -> new `#78 [1259,5348,1601,5404]`; old `#1` -> new `#79 [1258,5423,2415,5659]`.
  - Slide 5: old `#83` -> new `#81 [2146,6266,2415,6306]`; old `#97` -> new `#95 [1306,6488,1588,6525]`; old `#98` -> new `#96 [1306,6546,1637,6584]`; old `#99` -> new `#97 [1513,6546,1636,6584]`; old `#100` -> new `#98 [1389,6604,1719,6642]`; old `#101` -> new `#99 [1595,6604,1719,6642]`; old `#103` -> new `#101 [1389,6663,1533,6700]`; old `#105` -> new `#103 [1306,6780,1602,6817]`.
  - Slide 6: old `#116` -> new `#114 [2146,7778,2415,7818]`; old `#117` -> new `#115 [272,7938,596,7985]`; old `#118` -> new `#116 [97,8170,300,8210]`; old `#119` -> new `#117 [1040,7938,1365,7985]`; old `#120` -> new `#118 [882,8170,1100,8210]`; old `#121` -> new `#119 [1790,7938,2130,7985]`; old `#122` -> new `#120 [1658,8170,1900,8210]`; old `#123` -> new `#121 [270,8315,570,8365]`; old `#124` -> new `#122 [97,8528,340,8568]`; old `#125` -> new `#123 [1080,8315,1400,8365]`; old `#126` -> new `#124 [882,8528,1180,8568]`; old `#127` -> new `#125 [1830,8315,2150,8365]`; old `#128` -> new `#126 [1658,8528,1966,8568]`.
  - Slide 7: old `#130` -> new `#128 [2146,9289,2415,9330]`; old `#2` -> new `#129 [66,9511,2415,9788]`; old `#136` -> new `#135 [188,10135,514,10172]`; old `#137` -> new `#136 [395,10135,514,10172]`; old `#138` -> new `#137 [113,10246,665,10284]`; old `#139` -> new `#138 [231,10246,441,10284]`; old `#141` -> new `#140 [113,10302,461,10339]`; old `#3` -> new `#141 [1258,9913,2418,10306]`.
  - Slide 8: old `#143` -> new `#143 [2146,10801,2415,10842]`; old `#144` -> new `#144 [112,11056,687,11109]`; old `#145` -> new `#145 [111,11125,585,11167]`; old `#146` -> new `#146 [111,11186,618,11240]`; old `#147` -> new `#147 [111,11254,710,11299]`; old `#148` -> new `#148 [111,11315,379,11372]`; old `#152` -> new `#152 [1347,11254,1853,11299]`; old `#153` -> new `#153 [208,11647,393,11685]`; old `#154` -> new `#154 [189,11693,393,11780]`; old `#155` -> new `#155 [703,11647,828,11685]`; old `#156` -> new `#156 [703,11693,828,11780]`; old `#157` -> new `#157 [1170,11647,1311,11685]`; old `#158` -> new `#158 [1170,11693,1311,11780]`; old `#159` -> new `#159 [1608,11647,1782,11685]`; old `#160` -> new `#160 [1608,11693,1850,11780]`; old `#161` -> new `#161 [2105,11647,2275,11685]`; old `#162` -> new `#162 [2105,11693,2275,11780]`; old `#163` -> new `#163 [1900,12094,2387,12138]`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `0`.
- Non-bbox semantic changes recorded in this pass: `142` (`index`/`anno_id` remaps only).

Verification:

- Report with full old/new details: `reports/pdb_education_slides008_python_order_visual_v594.json`.
- Visual dry-run cover check directory: `cover_audit_education_slides008_python_order_visual_v594_dry/`.
- Visual dry-run outline check directory: `outline_audit_education_slides008_python_order_visual_v594_dry/`.
- Visual cover check directory: `cover_audit_education_slides008_python_order_visual_v594/`.
- Non-cover outline preview directory: `outline_audit_education_slides008_python_order_visual_v594/`.
- Static validation: final run reports `order_changes=142`, `bbox_changes=78`, `added_annotations=0`, `removed_annotations=0`, `bbox_added_to_existing_annotations=[]`, and `non_bbox_semantic_changes=142`; final case status is `164/164 boxed`, `0 no bbox`, `0 low-similarity`.
- Visual dry-run note: per-slide outline crops confirmed the corrected reading order starts at the cover slide and proceeds slide-by-slide. Slide 4 output result tables `#69` and `#79`, slide 7 tables `#129` and `#141`, slide 6 chart/code labels `#115-#126`, and slide 8 summary/footer labels now align with their visible elements.
- Frontend verification: opened `slides_008_数据分析_Python` with `cb=20260610_education_slides008_python_order_visual_v594`; the app header shows `data 20260610_education_slides008_python_order_visual_v594`, script URLs include `review_data.js?20260610_education_slides008_python_order_visual_v594` and `app.js?20260610_education_slides008_python_order_visual_v594`, and the active case row shows `164/164 boxed · 0 no bbox · 164 open`. Key checked rects include `#0 [894,426,1550,476]`, `#4 [2246,1401,2387,1435]`, `#69 [1258,4985,2415,5315]`, `#79 [1258,5423,2415,5659]`, `#115 [272,7938,596,7985]`, `#122 [97,8528,340,8568]`, `#124 [882,8528,1180,8568]`, `#126 [1658,8528,1966,8568]`, `#129 [66,9511,2415,9788]`, `#141 [1258,9913,2418,10306]`, and `#163 [1900,12094,2387,12138]`.
- Latest token after this repair: `20260610_education_slides008_python_order_visual_v594`.

## 20260610_education_slides014015_table_consolidate_v595

Scope:

- Follow-up GT table-fragment consolidation and visual bbox repair for two high-noise slide cases:
  - `02_education/03_slides/slides_014_材料化学_晶体结构`
  - `02_education/03_slides/slides_015_DL_Systems_并行训练_ZHCN`
- User-visible issue: both cases had full-table annotations already present, but those table bboxes were visually shifted or clipped, while duplicated cell-level `text_block` fragments remained and many of those fragments were either no-bbox or drifted to unrelated page areas.
- This token intentionally includes non-bbox GT semantic changes: duplicated cell-fragment annotations were deleted and merged into retained full-table annotations. Original `index`/`anno_id` values are preserved for retained annotations, so gaps after deleted ids are intentional.

Token:

- v595: `20260610_education_slides014015_table_consolidate_v595`

Method:

- Added `scripts/fix_education_slides014015_table_consolidate_v595.py`.
- Generated clean-PNG table crops and dry-run cover/outline previews, visually checked the table locations, then formally wrote the repaired data.
- Updated `review_data.json`, `review_data.js`, and `index.html` query/cache token.

Case-level changes:

- `slides_014_材料化学_晶体结构`: final status `93/107 boxed`, `14 no bbox`, `6 low-similarity`.
- Retained full-table bbox repairs:
  - `#33` crystal-structure table: `[149,1298,1949,1538]` -> `[92,866,1225,1026]`.
  - `#123` thermodynamic-data table: `[2781,457,3200,600]` -> `[2198,690,3092,904]`.
- Deleted GT annotations merged into `#33`: `#34-#56`.
- Deleted GT annotations merged into `#123`: `#124-#152`.
- `slides_015_DL_Systems_并行训练_ZHCN`: final status `84/89 boxed`, `5 no bbox`, `0 low-similarity`.
- Retained full-table bbox repairs:
  - `#80` benchmark-results table: `[2604,1237,3200,1490]` -> `[1600,1237,3136,1487]`.
  - `#120` communication-overhead table: `[2604,1543,3200,1710]` -> `[1600,1543,3136,1710]`.
- Deleted GT annotations merged into `#80`: `#81-#118`.
- Deleted GT annotations merged into `#120`: `#121-#138`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `108`.
- Removed GT annotations by case:
  - `slides_014_材料化学_晶体结构`: `52` removed (`#34-#56`, `#124-#152`).
  - `slides_015_DL_Systems_并行训练_ZHCN`: `56` removed (`#81-#118`, `#121-#138`).
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `0`.
- Non-bbox semantic changes recorded in this pass: `108` deletions of duplicated table cell fragments.

Verification:

- Report with full old/new details: `reports/pdb_education_slides014015_table_consolidate_v595.json`.
- Visual dry-run cover check directory: `cover_audit_education_slides014015_table_consolidate_v595_dry/`.
- Visual dry-run outline check directory: `outline_audit_education_slides014015_table_consolidate_v595_dry/`.
- Visual cover check directory: `cover_audit_education_slides014015_table_consolidate_v595/`.
- Non-cover outline preview directory: `outline_audit_education_slides014015_table_consolidate_v595/`.
- Static validation: final run reports `changed_retained_annotations=4`, `added_annotations=0`, `removed_annotations=108`, and `non_bbox_semantic_changes=108`; `index.html` contains the v595 cache token on all three asset URLs.
- Visual dry-run note: clean-PNG crops confirmed `slides_014 #33/#123` and `slides_015 #80/#120` now frame the visible tables rather than the previous shifted/clipped locations. The duplicated cell labels no longer clutter the table areas.
- Latest token after this repair: `20260610_education_slides014015_table_consolidate_v595`.

## 20260610_education_slides_table_fragments_v596

Scope:

- Follow-up slides-wide GT table-fragment consolidation for seven cases:
  - `02_education/03_slides/slides_016_Keynote_AI`
  - `02_education/03_slides/slides_019_竞品分析`
  - `02_education/03_slides/slides_029_产品发布_手机`
  - `02_education/03_slides/slides_030_Human_AI_CoReading`
  - `02_education/03_slides/slides_030_Smart_Urban_Resilience_2in1`
  - `02_education/03_slides/slides_030_多模态文档智能系统_上下伪两页科研汇报`
  - `02_education/03_slides/slides_031_Autonomous_Research_Operations_2in1`
- User-visible issue: these cases had existing full-table GT annotations, but also retained many duplicated cell-level `text_block` annotations. In the dense 030/031 slides, many of those cell fragments were visually shifted to unrelated regions and obscured the true table-level labels.
- This token intentionally includes non-bbox GT semantic changes: duplicated table cell annotations were deleted and merged into retained table annotations. No annotation indices were renumbered after deletion.

Token:

- v596: `20260610_education_slides_table_fragments_v596`

Method:

- Added `scripts/fix_education_slides_table_fragments_v596.py`.
- Generated a v595-current slides scout sheet, enumerated full-table annotations and their duplicated cell ranges, dry-ran the deletions, and visually checked the v596 dry-run contact sheet before writing.
- Updated `review_data.json`, `review_data.js`, and `index.html` query/cache token.

Case-level changes:

- `slides_016_Keynote_AI`: final status `71/71 boxed`, `0 no bbox`, `0 low-similarity`.
  - Retained full tables: `#29`, `#52`, `#74`.
  - Deleted GT annotations merged into those tables: `#30-#45`, `#53-#67`, `#75-#88`.
- `slides_019_竞品分析`: final status `46/46 boxed`, `0 no bbox`, `0 low-similarity`.
  - Retained full tables: `#28`, `#70`.
  - Deleted GT annotations merged into those tables: `#29-#68`, `#71-#90`.
- `slides_029_产品发布_手机`: final status `116/116 boxed`, `0 no bbox`, `6 low-similarity`.
  - Retained full table: `#95`.
  - Deleted GT annotations merged into that table: `#96-#103`.
- `slides_030_Human_AI_CoReading`: final status `116/116 boxed`, `0 no bbox`, `5 low-similarity`.
  - Retained full tables: `#43`, `#97`, `#149`.
  - Deleted GT annotations merged into those tables: `#44-#73`, `#98-#144`, `#150-#164`.
- `slides_030_Smart_Urban_Resilience_2in1`: final status `158/189 boxed`, `31 no bbox`, `49 low-similarity`.
  - Retained full tables: `#103`, `#157`, `#220`.
  - Deleted GT annotations merged into those tables: `#104-#123`, `#158-#205`, `#221-#236`.
- `slides_030_多模态文档智能系统_上下伪两页科研汇报`: final status `128/159 boxed`, `31 no bbox`, `48 low-similarity`.
  - Retained full tables: `#62`, `#123`, `#186`.
  - Deleted GT annotations merged into those tables: `#63-#86`, `#124-#182`, `#187-#200`.
- `slides_031_Autonomous_Research_Operations_2in1`: final status `164/206 boxed`, `42 no bbox`, `39 low-similarity`.
  - Retained full tables: `#64`, `#119`, `#170`, `#226`.
  - Deleted GT annotations merged into those tables: `#65-#92`, `#120-#135`, `#171-#220`, `#227-#239`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `493`.
- Removed GT annotations by case:
  - `slides_016_Keynote_AI`: `45`.
  - `slides_019_竞品分析`: `60`.
  - `slides_029_产品发布_手机`: `8`.
  - `slides_030_Human_AI_CoReading`: `92`.
  - `slides_030_Smart_Urban_Resilience_2in1`: `84`.
  - `slides_030_多模态文档智能系统_上下伪两页科研汇报`: `97`.
  - `slides_031_Autonomous_Research_Operations_2in1`: `107`.
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `0`.
- Non-bbox semantic changes recorded in this pass: `493` deletions of duplicated table cell fragments.

Verification:

- Report with full old/new details: `reports/pdb_education_slides_table_fragments_v596.json`.
- Visual dry-run cover check directory: `cover_audit_education_slides_table_fragments_v596_dry/`.
- Visual dry-run outline check directory: `outline_audit_education_slides_table_fragments_v596_dry/`.
- Visual cover check directory: `cover_audit_education_slides_table_fragments_v596/`.
- Non-cover outline preview directory: `outline_audit_education_slides_table_fragments_v596/`.
- Slides-wide scout used for this pass: `outline_audit_education_slides_all_v596_scout/`.
- Static validation: final run reports `changed_retained_annotations=0`, `added_annotations=0`, `removed_annotations=493`, and `non_bbox_semantic_changes=493`; `index.html` contains the v596 cache token on all three asset URLs.
- Visual dry-run note: the v596 contact sheet confirmed that the dense table-cell overlays were removed while full table boxes remained visible in `slides_016`, `slides_019`, `slides_029`, the three `slides_030*` cases, and `slides_031`. Remaining visible drift in the 030/031 cases is outside the table-cell consolidation scope and still needs later pass-level repair.
- Latest token after this repair: `20260610_education_slides_table_fragments_v596`.

## 20260610_education_slides_dom_selective_v597

Scope:

- Slides-wide follow-up pass for visually safer low-similarity/unmatched GT annotations in six cases:
  - `02_education/03_slides/slides_001_机器学习导论`
  - `02_education/03_slides/slides_002_思政课_中国式现代化`
  - `02_education/03_slides/slides_003_Optimization_ML_EN`
  - `02_education/03_slides/slides_009_Marketing_Strategy`
  - `02_education/03_slides/slides_010_历史课_丝绸之路`
  - `02_education/03_slides/slides_011_Corporate_Finance_2in1_EN`
- This token intentionally accepts only the v597 dry-run candidates that were checked in the generated outline views and appeared visually aligned. Higher-risk DOM candidates for `slides_014`, `slides_015`, `slides_030*`, and `slides_031` were not written in this token.
- No annotation ordering, type, or content semantics were changed in this pass.

Token:

- v597: `20260610_education_slides_dom_selective_v597`

Method:

- Added and ran `scripts/fix_education_slides_dom_selective_v597.py`.
- The script used slide DOM candidates only for annotations that were already unmatched or low-similarity, and only accepted candidates with a valid bbox and `ok` match quality.
- Generated and inspected dry-run and formal cover/outline images before accepting the formal write.
- Updated `review_data.json`, `review_data.js`, and `index.html` query/cache token.

Case-level bbox changes:

- `slides_001_机器学习导论`: final status `89/89 boxed`, `0 no bbox`, `7 low-similarity`.
  - `#10` `text_block`: `[206, 1047, 400, 1091]` -> `[108, 941, 1224, 1155]`.
  - `#12` `text_block`: `[999, 281, 1099, 315]` -> `[160, 1051, 362, 1095]`.
- `slides_002_思政课_中国式现代化`: final status `27/27 boxed`, `0 no bbox`, `0 low-similarity`.
  - `#1` `header`: `null` -> `[2898, 25, 3135, 56]`.
  - `#25` `text_block`: `[88, 19, 561, 42]` -> `[70, 1724, 3130, 1780]`.
- `slides_003_Optimization_ML_EN`: final status `25/25 boxed`, `0 no bbox`, `6 low-similarity`.
  - `#1` `header`: `[2921, 73, 3123, 132]` -> `[2919, 71, 3125, 176]`.
  - `#14` `code_txt`: `null` -> `[1620, 268, 2744, 306]`.
- `slides_009_Marketing_Strategy`: final status `81/81 boxed`, `0 no bbox`, `0 low-similarity`.
  - `#23` `text_block`: `[300, 8384, 423, 8421]` -> `[95, 4882, 422, 4935]`.
  - `#28` `text_block`: `[174, 7923, 475, 7963]` -> `[1286, 4842, 1671, 4890]`.
  - `#38` `text_block`: `[155, 8010, 475, 8051]` -> `[1285, 5289, 1564, 5381]`.
  - `#56` `text_block`: `[63, 6923, 2373, 6970]` -> `[60, 6867, 248, 6913]`.
  - `#64` `text_block`: `[1085, 9986, 1396, 10023]` -> `[171, 7904, 605, 7943]`.
  - `#65` `text_block`: `[113, 8384, 1030, 8421]` -> `[152, 7992, 605, 8031]`.
  - `#74` `text_block`: `[63, 6736, 2373, 6783]` -> `[2134, 9130, 2481, 9289]`.
  - `#76` `text_block`: `[1906, 9986, 2166, 10023]` -> `[1079, 9988, 1397, 10026]`.
  - `#78` `text_block`: `[113, 8384, 206, 8421]` -> `[1903, 9988, 2166, 10026]`.
  - `#80` `text_block`: `[1762, 2248, 1856, 2295]` -> `[2038, 10474, 2441, 10512]`.
- `slides_010_历史课_丝绸之路`: final status `69/69 boxed`, `0 no bbox`, `0 low-similarity`.
  - `#42` `text_block`: `[137, 2210, 203, 2235]` -> `[1140, 6340, 1341, 6384]`.
  - `#45` `text_block`: `[794, 2151, 902, 2176]` -> `[1936, 6340, 2136, 6384]`.
  - `#61` `text_block`: `[1170, 1983, 1270, 2008]` -> `[2178, 9202, 2419, 9246]`.
- `slides_011_Corporate_Finance_2in1_EN`: final status `43/43 boxed`, `0 no bbox`, `0 low-similarity`.
  - `#7` `text_block`: `null` -> `[2890, 79, 3200, 151]`.
  - `#42` `page_number`: `null` -> `[3071, 2406, 3164, 2443]`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations:
  - `slides_002_思政课_中国式现代化`: `#1`.
  - `slides_003_Optimization_ML_EN`: `#14`.
  - `slides_011_Corporate_Finance_2in1_EN`: `#7`, `#42`.
- Cleared existing bbox values: `0`.
- Non-bbox semantic changes recorded in this pass: `0`.

Verification:

- Report with full old/new details: `reports/pdb_education_slides_dom_selective_v597.json`.
- Visual dry-run cover check directory: `cover_audit_education_slides_dom_selective_v597_safe_dry/`.
- Visual dry-run outline check directory: `outline_audit_education_slides_dom_selective_v597_safe_dry/`.
- Visual cover check directory: `cover_audit_education_slides_dom_selective_v597/`.
- Non-cover outline preview directory: `outline_audit_education_slides_dom_selective_v597/`.
- Formal outline contact sheet inspected: `outline_audit_education_slides_dom_selective_v597/contact_sheet.jpg`.
- Static validation: final run reports `changed_annotations=21`, `added_annotations=0`, `removed_annotations=0`, and `non_bbox_semantic_changes=0`; `index.html` contains the v597 cache token on all three asset URLs.
- Visual note: the formal contact sheet confirmed the accepted v597 updates are localized to visible header/footer, note, chart-label, and slide-label text. Higher-risk DOM candidates with page-spanning or over-wide boxes remain excluded for separate manual repair.
- Latest token after this repair: `20260610_education_slides_dom_selective_v597`.

## 20260610_education_slides005_footer_v598

Scope:

- Follow-up manual visual repair for one slides case:
  - `02_education/03_slides/slides_005_商务培训_项目管理`
- User-visible issue: footer annotations `#21/#22` were visually shifted to the upper/middle slide content instead of the bottom green footer band.
- No annotation ordering, type, or content semantics were changed in this pass.

Token:

- v598: `20260610_education_slides005_footer_v598`

Method:

- Added and ran `scripts/fix_education_slides005_footer_v598.py`.
- Used a clean-PNG bottom crop to manually place `#21/#22` on the visible footer text.
- Generated and inspected dry-run and formal cover/outline images before accepting the formal write.
- Updated `review_data.json`, `review_data.js`, and `index.html` query/cache token.

Case-level bbox changes:

- `slides_005_商务培训_项目管理`: final status `24/24 boxed`, `0 no bbox`, `0 low-similarity`.
  - `#21` `text_block`: `[793, 172, 1688, 384]` -> `[154, 5768, 1070, 5832]`.
  - `#22` `text_block`: `[225, 797, 428, 844]` -> `[1576, 5768, 2295, 5832]`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `0`.
- Non-bbox semantic changes recorded in this pass: `0`.

Verification:

- Report with full old/new details: `reports/pdb_education_slides005_footer_v598.json`.
- Visual dry-run cover check directory: `cover_audit_education_slides005_footer_v598_dry/`.
- Visual dry-run outline check directory: `outline_audit_education_slides005_footer_v598_dry/`.
- Visual cover check directory: `cover_audit_education_slides005_footer_v598/`.
- Non-cover outline preview directory: `outline_audit_education_slides005_footer_v598/`.
- Formal footer crop inspected: `/tmp/slides005_footer_outline_formal_crop.jpg`.
- Static validation: final run reports `changed_annotations=2`, `added_annotations=0`, `removed_annotations=0`, and `non_bbox_semantic_changes=0`; `index.html` contains the v598 cache token on all three asset URLs.
- Latest token after this repair: `20260610_education_slides005_footer_v598`.

## 20260610_education_slides007_footer_v599

Scope:

- Follow-up manual visual repair for one slides case:
  - `02_education/03_slides/slides_007_Art_History_Renaissance`
- User-visible issue: footer annotation `#67` was visually shifted to the cover title area instead of the final-slide footer text.
- No annotation ordering, type, or content semantics were changed in this pass.

Token:

- v599: `20260610_education_slides007_footer_v599`

Method:

- Added and ran `scripts/fix_education_slides007_footer_v599.py`.
- Used the clean-PNG final-slide footer crop to manually place `#67` on the visible `Renaissance Art — Art History 301` footer.
- Generated and inspected dry-run and formal cover/outline images before accepting the formal write.
- Updated `review_data.json`, `review_data.js`, and `index.html` query/cache token.

Case-level bbox changes:

- `slides_007_Art_History_Renaissance`: final status `68/68 boxed`, `0 no bbox`, `0 low-similarity`.
  - `#67` `text_block`: `[766, 500, 1712, 547]` -> `[1980, 10585, 2465, 10645]`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `0`.
- Non-bbox semantic changes recorded in this pass: `0`.

Verification:

- Report with full old/new details: `reports/pdb_education_slides007_footer_v599.json`.
- Visual dry-run cover check directory: `cover_audit_education_slides007_footer_v599_dry/`.
- Visual dry-run outline check directory: `outline_audit_education_slides007_footer_v599_dry/`.
- Visual cover check directory: `cover_audit_education_slides007_footer_v599/`.
- Non-cover outline preview directory: `outline_audit_education_slides007_footer_v599/`.
- Formal footer crop inspected: `/tmp/slides007_footer_outline_crop.jpg`.
- Static validation: final run reports `changed_annotations=1`, `added_annotations=0`, `removed_annotations=0`, and `non_bbox_semantic_changes=0`; `index.html` contains the v599 cache token on all three asset URLs.
- Latest token after this repair: `20260610_education_slides007_footer_v599`.

## 20260610_education_slides029_specs_v600

Scope:

- Follow-up manual visual repair for one slides case:
  - `02_education/03_slides/slides_029_产品发布_手机`
- User-visible issue: parameter-row annotations `#24-#29` were visually shifted to the bottom price/preorder area instead of the left parameter table.
- No annotation ordering, type, or content semantics were changed in this pass.

Token:

- v600: `20260610_education_slides029_specs_v600`

Method:

- Added and ran `scripts/fix_education_slides029_specs_v600.py`.
- Used a clean-PNG crop of the parameter table top rows to manually place `#24-#29`.
- Generated and inspected dry-run and formal cover/outline images before accepting the formal write.
- Updated `review_data.json`, `review_data.js`, and `index.html` query/cache token.

Case-level bbox changes:

- `slides_029_产品发布_手机`: final status `116/116 boxed`, `0 no bbox`, `0 low-similarity`.
  - `#24` `text_block`: `[1923, 3056, 2010, 3090]` -> `[180, 1003, 280, 1044]`.
  - `#25` `text_block`: `[1898, 3100, 2036, 3131]` -> `[495, 1003, 925, 1044]`.
  - `#26` `text_block`: `[1865, 3140, 2068, 3221]` -> `[180, 1065, 345, 1106]`.
  - `#27` `text_block`: `[1917, 3225, 2017, 3256]` -> `[495, 1065, 1095, 1106]`.
  - `#28` `text_block`: `[740, 3343, 1738, 3377]` -> `[180, 1125, 260, 1166]`.
  - `#29` `text_block`: `[886, 3343, 1184, 3377]` -> `[495, 1125, 1060, 1166]`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `0`.
- Non-bbox semantic changes recorded in this pass: `0`.

Verification:

- Report with full old/new details: `reports/pdb_education_slides029_specs_v600.json`.
- Visual dry-run cover check directory: `cover_audit_education_slides029_specs_v600_dry/`.
- Visual dry-run outline check directory: `outline_audit_education_slides029_specs_v600_dry/`.
- Visual cover check directory: `cover_audit_education_slides029_specs_v600/`.
- Non-cover outline preview directory: `outline_audit_education_slides029_specs_v600/`.
- Parameter-table crop inspected: `/tmp/slides029_specs_outline_crop.jpg`.
- Static validation: final run reports `changed_annotations=6`, `added_annotations=0`, `removed_annotations=0`, and `non_bbox_semantic_changes=0`; `index.html` contains the v600 cache token on all three asset URLs.
- Latest token after this repair: `20260610_education_slides029_specs_v600`.

## 20260611_education_slides005_order_v601

Scope:

- Follow-up manual visual repair for one slides case:
  - `02_education/03_slides/slides_005_商务培训_项目管理`
- User-visible issue: reading order labels were semantically wrong. Table annotations that visually belong to the right/lower panels were ordered as `#0-#3` before the cover title, while the visual first elements started at `#4/#5`.
- No bbox coordinates, GT annotation contents, or category types were changed in this pass.

Token:

- v601: `20260611_education_slides005_order_v601`

Method:

- Added and ran `scripts/fix_education_slides005_order_v601.py`.
- Reordered annotations by visual reading order and rewrote each affected annotation's `index` and `anno_id`.
- Generated and inspected dry-run and formal cover/outline images before accepting the formal write.
- Updated `review_data.json`, `review_data.js`, and `index.html` query/cache token.

Case-level non-bbox semantic changes:

- `slides_005_商务培训_项目管理`: final status `24/24 boxed`, `0 no bbox`, `0 low-similarity`.
- Reading-order/id mapping:
  - old `#4` -> new `#0`; old `#5` -> new `#1`; old `#6` -> new `#2`; old `#7` -> new `#3`; old `#8` -> new `#4`.
  - old `#9` -> new `#5`; old `#10` -> new `#6`; old `#11` -> new `#7`; old `#12` -> new `#8`.
  - old `#0` -> new `#9`; old `#13` -> new `#10`; old `#14` -> new `#11`; old `#15` -> new `#12`; old `#1` -> new `#13`; old `#16` -> new `#14`.
  - old `#17` -> new `#15`; old `#2` -> new `#16`; old `#18` -> new `#17`; old `#19` -> new `#18`; old `#3` -> new `#19`.
  - old `#20/#21/#22/#23` remained `#20/#21/#22/#23`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `0`.
- Non-bbox semantic changes recorded in this pass: `20` annotation order/id changes.

Verification:

- Report with full old/new order details: `reports/pdb_education_slides005_order_v601.json`.
- Visual dry-run cover check directory: `cover_audit_education_slides005_order_v601_dry/`.
- Visual dry-run outline check directory: `outline_audit_education_slides005_order_v601_dry/`.
- Visual cover check directory: `cover_audit_education_slides005_order_v601/`.
- Non-cover outline preview directory: `outline_audit_education_slides005_order_v601/`.
- Formal outline inspected: `outline_audit_education_slides005_order_v601/slides_005_商务培训_项目管理_outline.jpg`.
- Static validation at write time: final run reports `order_changes=20`, `bbox_changes=0`, `added_annotations=0`, `removed_annotations=0`, and `non_bbox_semantic_changes=20`.
- Latest token after this repair: `20260611_education_slides005_order_v601`.

## 20260611_education_slides005_bbox_v602

Scope:

- Follow-up manual visual repair for one slides case:
  - `02_education/03_slides/slides_005_商务培训_项目管理`
- User-visible issue after v601: reading order was corrected, but several boxes were still visibly over-wide and crossed into adjacent panels.
- No annotation ordering, type, or content semantics were changed in this pass.

Token:

- v602: `20260611_education_slides005_bbox_v602`

Method:

- Added and ran `scripts/fix_education_slides005_bbox_v602.py`.
- Used clean-PNG coordinate crops and the formal v601 outline to manually tighten the over-wide boxes.
- Generated and inspected dry-run and formal cover/outline images before accepting the formal write.
- Updated `review_data.json`, `review_data.js`, and `index.html` query/cache token.

Case-level bbox changes:

- `slides_005_商务培训_项目管理`: final status `24/24 boxed`, `0 no bbox`, `0 low-similarity`.
  - `#2` `title`: `[228, 626, 2169, 712]` -> `[228, 626, 650, 712]`.
  - `#4` `text_block`: `[222, 1479, 1926, 1647]` -> `[222, 1479, 685, 1647]`.
  - `#11` `title`: `[230, 3130, 2167, 3191]` -> `[230, 3130, 620, 3191]`.
  - `#12` `text_block`: `[223, 3292, 2026, 3360]` -> `[223, 3292, 390, 3360]`.
  - `#13` `table`: `[225, 3394, 1546, 5078]` -> `[225, 3394, 735, 5078]`.
  - `#19` `table`: `[588, 3394, 2307, 4522]` -> `[1860, 3394, 2307, 4522]`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `0`.
- Non-bbox semantic changes recorded in this pass: `0`.

Verification:

- Report with full old/new details: `reports/pdb_education_slides005_bbox_v602.json`.
- Visual dry-run cover check directory: `cover_audit_education_slides005_bbox_v602_dry/`.
- Visual dry-run outline check directory: `outline_audit_education_slides005_bbox_v602_dry/`.
- Visual cover check directory: `cover_audit_education_slides005_bbox_v602/`.
- Non-cover outline preview directory: `outline_audit_education_slides005_bbox_v602/`.
- Clean-PNG coordinate crops inspected: `/tmp/slides005_clean_top.jpg`, `/tmp/slides005_clean_lower.jpg`.
- Formal outline inspected: `outline_audit_education_slides005_bbox_v602/slides_005_商务培训_项目管理_outline.jpg`.
- Static validation at write time: final run reports `changed_annotations=6`, `added_annotations=0`, `removed_annotations=0`, and `non_bbox_semantic_changes=0`.
- Frontend/cache validation: opened `http://127.0.0.1:8767/index.html?cb=20260611_education_slides005_bbox_v602`; visible page showed `data 20260611_education_slides005_bbox_v602`, and `review_data.js?20260611_education_slides005_bbox_v602` returned the same token with `slides_005_商务培训_项目管理` ordered from `#0` title through `#9` risk table.
- Latest token after this repair: `20260611_education_slides005_bbox_v602`.

## 20260611_education_slides009_order_v603

Scope:

- Follow-up manual visual repair for one slides case:
  - `02_education/03_slides/slides_009_Marketing_Strategy`
- User-visible issue: reading order labels were semantically wrong. The 7P table on Slide 3 was `#0`, and the ROI/channel table on Slide 7 was `#1`, before the visual first-page title content.
- No bbox coordinates, GT annotation contents, or category types were changed in this pass.

Token:

- v603: `20260611_education_slides009_order_v603`

Method:

- Added and ran `scripts/fix_education_slides009_order_v603.py`.
- Reordered annotations by visual slide/page flow and rewrote each affected annotation's `index` and `anno_id`.
- Generated and inspected dry-run and formal cover/outline images before accepting the formal write.
- Updated `review_data.json`, `review_data.js`, and `index.html` query/cache token.

Case-level non-bbox semantic changes:

- `slides_009_Marketing_Strategy`: final status `81/81 boxed`, `0 no bbox`, `0 low-similarity`.
- Reading-order/id mapping:
  - Slide 1: old `#2/#3/#4/#5/#6` -> new `#0/#1/#2/#3/#4`.
  - Slide 2: old `#7/#8/#9/#10/#11/#12/#13/#14/#15/#16/#17/#18` -> new `#5/#6/#7/#8/#9/#10/#11/#12/#13/#14/#15/#16`.
  - Slide 3: old `#19/#20/#0` -> new `#17/#18/#19`. This moves the 7P table from old `#0` to new `#19`.
  - Slide 4: old `#21/#22/#23/#24/#25/#26/#27/#28/#29/#30/#31/#32/#33/#34/#35/#36/#37/#38/#39/#40/#41/#42` -> new `#20/#21/#22/#23/#24/#25/#26/#27/#28/#29/#30/#31/#32/#33/#34/#35/#36/#37/#38/#39/#40/#41`.
  - Slide 5: old `#43/#44/#45/#46/#47/#48/#49/#50/#51/#52/#53/#54/#55/#56/#57` -> new `#42/#43/#44/#45/#46/#47/#48/#49/#50/#51/#52/#53/#54/#55/#56`.
  - Slide 6: old `#58/#59/#60/#61/#62/#63/#64/#65/#66/#67/#68/#69/#71/#72` -> new `#57/#58/#59/#60/#61/#62/#63/#64/#65/#66/#67/#68/#69/#70`.
  - Slide 7: old `#73/#74/#1/#70/#75/#76/#77/#78/#79/#80` -> new `#71/#72/#73/#74/#75/#76/#77/#78/#79/#80`. This moves the ROI/channel table from old `#1` to new `#73`; old `#75-#80` remain at `#75-#80`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `0`.
- Non-bbox semantic changes recorded in this pass: `75` annotation order/id changes.

Verification:

- Report with full old/new order details: `reports/pdb_education_slides009_order_v603.json`.
- Visual dry-run cover check directory: `cover_audit_education_slides009_order_v603_dry/`.
- Visual dry-run outline check directory: `outline_audit_education_slides009_order_v603_dry/`.
- Visual cover check directory: `cover_audit_education_slides009_order_v603/`.
- Non-cover outline preview directory: `outline_audit_education_slides009_order_v603/`.
- Formal outline inspected: `outline_audit_education_slides009_order_v603/slides_009_Marketing_Strategy_outline.jpg`.
- Static validation at write time: final run reports `order_changes=75`, `bbox_changes=0`, `added_annotations=0`, `removed_annotations=0`, and `non_bbox_semantic_changes=75`.
- Frontend/cache validation: opened `http://127.0.0.1:8767/index.html?cb=20260611_education_slides009_order_v603`; visible page showed `data 20260611_education_slides009_order_v603`, and `review_data.js?20260611_education_slides009_order_v603` returned the same token with `slides_009_Marketing_Strategy` ordered from first-page title content through Slide 3 table `#19` and Slide 7 table `#73`.
- Latest token after this repair: `20260611_education_slides009_order_v603`.

## 20260611_education_slides007_relabel_v604

Scope:

- Full manual visual relabel for one slides case:
  - `02_education/03_slides/slides_007_Art_History_Renaissance`
- User-visible issue: many annotations were visually out of order or attached to the wrong slide/row. Notable examples: old `#0` was the Slide 4 masters table but appeared before the cover title, old `#1` `Renaissance Art` was matched to Slide 6 instead of the cover title, and Slide 5/6/7 text boxes were overlapping wrong rows.

Token:

- v604: `20260611_education_slides007_relabel_v604`

Method:

- Added and ran `scripts/fix_education_slides007_relabel_v604.py`.
- Used clean-PNG coordinate crops for Slides 1-7: `/tmp/slides007_slide1_grid.jpg` through `/tmp/slides007_slide7_grid.jpg`.
- Reordered annotations by visual slide/page flow and rewrote affected `index` and `anno_id` values.
- Manually reset visually wrong bboxes for existing annotations only; no GT annotation was added or deleted.
- Generated and inspected dry-run and formal cover/outline images before accepting the formal write.
- Updated `review_data.json`, `review_data.js`, and `index.html` query/cache token.

Case-level non-bbox semantic changes:

- `slides_007_Art_History_Renaissance`: final status `68/68 boxed`, `0 no bbox`, `0 low-similarity`.
- Reading-order/id mapping:
  - Slide 1: old `#1/#2/#3/#4` -> new `#0/#1/#2/#3`.
  - Slide 2: old `#5-#19` -> new `#4-#18`.
  - Slide 3: old `#20/#21/#22/#24/#23/#25/#26/#27` -> new `#19/#20/#21/#22/#23/#24/#25/#26`.
  - Slide 4: old `#28/#29/#0` -> new `#27/#28/#29`; this moves the masters table from old `#0` to new `#29`.
  - Slides 5-7: old `#30-#67` remain in visual slide order as new `#30-#67`.

Case-level bbox changes:

- `slides_007_Art_History_Renaissance`: `67` existing bboxes changed. Old indices below refer to the pre-v604 ids.
  - old `#0` `table`: `[25, 4806, 2456, 5552]` -> `[60, 4925, 2420, 5755]`.
  - old `#1` `title`: `[1630, 8018, 2027, 8047]` -> `[760, 475, 1725, 570]`.
  - old `#2` `title`: `[686, 610, 1798, 678]` -> `[690, 610, 1798, 680]`.
  - old `#3` `text_block`: `[767, 847, 1702, 1024]` -> `[765, 845, 1710, 1028]`.
  - old `#4` `text_block`: `[2307, 1464, 2428, 1503]` -> `[2250, 1435, 2435, 1495]`.
  - old `#5` `header`: `[60, 1626, 2424, 1691]` -> `[55, 1600, 665, 1685]`.
  - old `#6` `text_block`: `[2247, 1641, 2424, 1689]` -> `[2245, 1605, 2425, 1685]`.
  - old `#7` `text_block`: `[133, 1806, 1259, 1998]` -> `[130, 1788, 1085, 2005]`.
  - old `#8` `text_block`: `[725, 1836, 1069, 1850]` -> `[720, 1780, 1070, 1835]`.
  - old `#9` `text_block`: `[912, 1879, 1071, 1923]` -> `[910, 1872, 1075, 1932]`.
  - old `#10` `text_block`: `[1223, 2054, 2329, 2238]` -> `[1410, 2055, 2265, 2175]`.
  - old `#11` `text_block`: `[1411, 2061, 1571, 2105]` -> `[1410, 2045, 1580, 2098]`.
  - old `#12` `text_block`: `[212, 2235, 1259, 2419]` -> `[215, 2255, 1080, 2365]`.
  - old `#13` `text_block`: `[1223, 2159, 1750, 2428]` -> `[1410, 2408, 1775, 2570]`.
  - old `#14` `text_block`: `[1410, 2144, 1600, 2193]` -> `[1410, 2398, 1775, 2458]`.
  - old `#15` `text_block`: `[1413, 2443, 1753, 2456]` -> `[1410, 2488, 1770, 2538]`.
  - old `#16` `text_block`: `[212, 2235, 1259, 2419]` -> `[560, 2610, 1080, 2700]`.
  - old `#17` `text_block`: `[1223, 2551, 1906, 2793]` -> `[1410, 2748, 2200, 2945]`.
  - old `#18` `text_block`: `[1411, 2525, 1873, 2563]` -> `[1410, 2742, 1885, 2805]`.
  - old `#19` `text_block`: `[1411, 2525, 1718, 2562]` -> `[1410, 2828, 1725, 2888]`.
  - old `#20` `header`: `[0, 3217, 2481, 3235]` -> `[55, 3260, 1120, 3355]`.
  - old `#21` `text_block`: `[2248, 3288, 2424, 3336]` -> `[2245, 3265, 2425, 3345]`.
  - old `#22` `text_block`: `[65, 3297, 1131, 3333]` -> `[60, 3408, 1260, 3470]`.
  - old `#23` `text_block`: `[2132, 3682, 2424, 3718]` -> `[2220, 3770, 2410, 3825]`.
  - old `#24` `text_block`: `[982, 3422, 1261, 3463]` -> `[1110, 3705, 1395, 3765]`.
  - old `#25` `text_block`: `[57, 3989, 789, 4062]` -> `[65, 4110, 790, 4228]`.
  - old `#26` `text_block`: `[882, 3989, 1602, 4062]` -> `[870, 4110, 1625, 4228]`.
  - old `#27` `text_block`: `[1692, 3989, 2424, 4062]` -> `[1690, 4110, 2425, 4228]`.
  - old `#28` `header`: `[0, 4726, 2481, 4744]` -> `[55, 4770, 1085, 4865]`.
  - old `#29` `text_block`: `[2247, 4797, 2424, 4845]` -> `[2245, 4775, 2425, 4865]`.
  - old `#30` `header`: `[0, 6239, 2481, 6257]` -> `[55, 6270, 820, 6355]`.
  - old `#31` `text_block`: `[2249, 6310, 2424, 6358]` -> `[2245, 6300, 2425, 6370]`.
  - old `#32` `text_block`: `[367, 6475, 877, 6614]` -> `[335, 6600, 900, 6765]`.
  - old `#33` `text_block`: `[57, 6914, 1224, 7049]` -> `[65, 6900, 1215, 7048]`.
  - old `#34` `text_block`: `[1207, 6560, 2089, 6585]` -> `[1260, 6438, 2035, 6505]`.
  - old `#35` `text_block`: `[1130, 6439, 2343, 6575]` -> `[1260, 6545, 2395, 6668]`.
  - old `#36` `text_block`: `[1207, 6576, 1594, 6648]` -> `[1260, 6698, 1515, 6755]`.
  - old `#37` `text_block`: `[1207, 6560, 2339, 6584]` -> `[1270, 6760, 2395, 6828]`.
  - old `#38` `text_block`: `[1064, 6886, 2308, 6923]` -> `[1270, 6838, 2395, 6898]`.
  - old `#39` `text_block`: `[1064, 6886, 2308, 6923]` -> `[1270, 6905, 2395, 6970]`.
  - old `#40` `text_block`: `[1075, 6886, 2308, 6923]` -> `[1270, 6975, 2395, 7045]`.
  - old `#41` `text_block`: `[1053, 6828, 2403, 6955]` -> `[1260, 7055, 2395, 7168]`.
  - old `#42` `text_block`: `[1259, 7194, 2371, 7217]` -> `[1260, 7195, 2395, 7315]`.
  - old `#43` `header`: `[0, 7751, 2481, 7769]` -> `[55, 7790, 1120, 7870]`.
  - old `#44` `text_block`: `[2247, 7822, 2424, 7870]` -> `[2245, 7805, 2425, 7875]`.
  - old `#45` `text_block`: `[386, 7844, 890, 7866]` -> `[480, 7978, 885, 8055]`.
  - old `#46` `text_block`: `[57, 7958, 816, 8077]` -> `[75, 8100, 760, 8212]`.
  - old `#47` `text_block`: `[57, 8070, 1364, 8249]` -> `[75, 8248, 815, 8358]`.
  - old `#48` `text_block`: `[57, 8231, 1364, 8384]` -> `[75, 8392, 820, 8508]`.
  - old `#49` `text_block`: `[57, 8365, 1364, 8521]` -> `[75, 8540, 820, 8650]`.
  - old `#50` `text_block`: `[57, 8503, 1364, 8655]` -> `[75, 8690, 640, 8790]`.
  - old `#51` `text_block`: `[57, 8637, 1364, 8790]` -> `[75, 8828, 795, 8932]`.
  - old `#52` `text_block`: `[1991, 10612, 2440, 10650]` -> `[1600, 7978, 2010, 8055]`.
  - old `#53` `text_block`: `[1626, 7958, 2424, 8077]` -> `[1260, 8100, 1900, 8212]`.
  - old `#54` `text_block`: `[1126, 8070, 2424, 8250]` -> `[1260, 8248, 2120, 8358]`.
  - old `#55` `text_block`: `[1273, 8231, 2424, 8384]` -> `[1260, 8392, 2100, 8508]`.
  - old `#56` `text_block`: `[1126, 8365, 2424, 8522]` -> `[1260, 8540, 2080, 8650]`.
  - old `#57` `text_block`: `[1126, 8502, 2424, 8656]` -> `[1260, 8690, 2180, 8790]`.
  - old `#58` `text_block`: `[1273, 8637, 2424, 8790]` -> `[1260, 8828, 2240, 8932]`.
  - old `#59` `header`: `[0, 9264, 2481, 9282]` -> `[55, 9320, 610, 9400]`.
  - old `#60` `text_block`: `[2250, 9335, 2424, 9383]` -> `[2245, 9328, 2425, 9398]`.
  - old `#61` `text_block`: `[94, 9501, 2225, 9524]` -> `[95, 9488, 2228, 9550]`.
  - old `#62` `text_block`: `[94, 9501, 2222, 9524]` -> `[95, 9608, 2230, 9672]`.
  - old `#63` `text_block`: `[78, 9515, 2237, 9542]` -> `[95, 9730, 2245, 9832]`.
  - old `#64` `text_block`: `[78, 9631, 2162, 9656]` -> `[95, 9892, 2175, 9960]`.
  - old `#65` `text_block`: `[78, 9735, 1923, 9775]` -> `[95, 10018, 1955, 10082]`.
  - old `#66` `text_block`: `[57, 9879, 1439, 10079]` -> `[80, 10182, 2365, 10538]`.
  - old `#67` `text_block`: unchanged at `[1980, 10585, 2465, 10645]`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `0`.
- Non-bbox semantic changes recorded in this pass: `29` annotation order/id changes.

Verification:

- Report with full old/new order and bbox details: `reports/pdb_education_slides007_relabel_v604.json`.
- Visual dry-run cover check directory: `cover_audit_education_slides007_relabel_v604_dry/`.
- Visual dry-run outline check directory: `outline_audit_education_slides007_relabel_v604_dry/`.
- Visual cover check directory: `cover_audit_education_slides007_relabel_v604/`.
- Non-cover outline preview directory: `outline_audit_education_slides007_relabel_v604/`.
- Formal outline inspected: `outline_audit_education_slides007_relabel_v604/slides_007_Art_History_Renaissance_outline.jpg`.
- Static validation at write time: final run reports `order_changes=29`, `bbox_changes=67`, `added_annotations=0`, `removed_annotations=0`, and `non_bbox_semantic_changes=29`.
- Frontend/cache validation: opened `http://127.0.0.1:8767/index.html?cb=20260611_education_slides007_relabel_v604`; visible page showed `data 20260611_education_slides007_relabel_v604`, and `review_data.js?20260611_education_slides007_relabel_v604` returned the same token with `slides_007_Art_History_Renaissance` ordered from cover title `#0` through Slide 4 table `#29`.
- Latest token after this repair: `20260611_education_slides007_relabel_v604`.

## 20260611_education_slides014_relabel_v605

Scope:

- Full manual visual relabel for one slides case:
  - `02_education/03_slides/slides_014_材料化学_晶体结构`
- User-visible issue: many annotations were visually out of order or attached to the wrong column / bottom blank area. Notable examples: old `#157` covered a huge bottom empty dark region, 14 existing GT annotations had no bbox, the right thermodynamics panel was shifted, and left/middle panel boxes crossed unrelated content.
- This pass did not add or delete GT annotations.

Token:

- v605: `20260611_education_slides014_relabel_v605`

Method:

- Added and ran `scripts/fix_education_slides014_relabel_v605.py`.
- Used clean-PNG coordinate crops `/tmp/slides014_header_grid.jpg`, `/tmp/slides014_left_grid.jpg`, `/tmp/slides014_middle_grid.jpg`, `/tmp/slides014_right_grid.jpg`, and `/tmp/slides014_footer_grid.jpg`.
- Reordered existing annotations into continuous visual order and rewrote affected `index` / `anno_id` values.
- Reset all 107 existing bboxes; 14 annotations had no bbox before this pass and received bboxes.
- Generated and inspected dry-run and formal cover/outline images before accepting the formal write.
- Updated `review_data.json`, `review_data.js`, and `index.html` query/cache token.

Case-level non-bbox semantic changes:

- `slides_014_材料化学_晶体结构`: final status `107/107 boxed`, `0 no bbox`, `0 low-similarity`.
- Reading-order/id mapping:
  - old `#0-#33` remain in the left/top visual sequence as new `#0-#33`.
  - old `#57-#99` -> new `#34-#76`.
  - old `#100-#123` -> new `#77-#100`.
  - old `#153-#158` -> new `#101-#106`.
  - This records `73` order/id changes caused by removing old deleted/gapped ids and enforcing visual reading order.

Case-level bbox changes:

- `slides_014_材料化学_晶体结构`: `107` existing bboxes changed/reset. Old indices below refer to the pre-v605 ids.
  - old `#0` `header`: `[0, 135, 3200, 1053]` -> `[65, 25, 3150, 115]`.
  - old `#1` `text_block`: `[63, 135, 3200, 282]` -> `[65, 25, 3150, 115]`.
  - old `#2` `text_block`: `[63, 135, 1934, 282]` -> `[65, 25, 1270, 115]`.
  - old `#3` `title`: `[63, 153, 1683, 218]` -> `[70, 30, 1075, 70]`.
  - old `#4` `text_block`: `[188, 153, 1683, 218]` -> `[250, 30, 1075, 70]`.
  - old `#5` `text_block`: `[63, 153, 1683, 218]` -> `[70, 85, 1280, 112]`.
  - old `#6` `text_block`: `None` -> `[2860, 25, 3150, 112]`; added bbox to existing GT.
  - old `#7` `header`: `[58, 135, 3200, 1053]` -> `[55, 150, 1230, 1040]`.
  - old `#8` `text_block`: `[139, 256, 1959, 1053]` -> `[95, 185, 1220, 1040]`.
  - old `#9` `title`: `[63, 153, 542, 218]` -> `[90, 185, 545, 230]`.
  - old `#10` `text_block`: `[63, 328, 322, 342]` -> `[95, 185, 130, 225]`.
  - old `#11` `text_block`: `[139, 331, 1959, 1053]` -> `[95, 245, 1220, 1040]`.
  - old `#12` `text_block`: `[89, 318, 330, 351]` -> `[95, 245, 360, 282]`.
  - old `#13` `text_block`: `[63, 153, 1683, 218]` -> `[100, 285, 1220, 330]`.
  - old `#14` `text_block`: `[602, 395, 617, 431]` -> `[330, 285, 470, 330]`.
  - old `#15` `text_block`: `[691, 398, 894, 431]` -> `[500, 285, 685, 330]`.
  - old `#16` `text_block`: `[1523, 345, 1946, 376]` -> `[990, 285, 1220, 330]`.
  - old `#17` `text_block`: `[88, 651, 576, 685]` -> `[95, 340, 390, 378]`.
  - old `#18` `text_block`: `[632, 543, 1466, 951]` -> `[400, 330, 930, 625]`.
  - old `#19` `text_block`: `[737, 888, 928, 931]` -> `[450, 560, 650, 610]`.
  - old `#20` `text_block`: `[737, 888, 928, 931]` -> `[510, 585, 650, 610]`.
  - old `#21` `text_block`: `[1179, 773, 1529, 863]` -> `[735, 560, 930, 610]`.
  - old `#22` `text_block`: `[1179, 773, 1529, 863]` -> `[795, 585, 930, 610]`.
  - old `#23` `text_block`: `[23, 955, 558, 996]` -> `[95, 635, 390, 675]`.
  - old `#24` `text_block`: `[0, 987, 1238, 1029]` -> `[95, 680, 710, 720]`.
  - old `#25` `text_block`: `[365, 987, 493, 1029]` -> `[230, 680, 305, 720]`.
  - old `#26` `equation_isolated`: `[652, 480, 974, 502]` -> `[500, 735, 930, 775]`.
  - old `#27` `header`: `[841, 1067, 1949, 1124]` -> `[500, 735, 930, 775]`.
  - old `#28` `text_block`: `[1911, 1067, 1949, 1099]` -> `[1175, 735, 1220, 775]`.
  - old `#29` `text_block`: `[149, 1154, 414, 1190]` -> `[95, 790, 320, 825]`.
  - old `#30` `equation_isolated`: `[652, 480, 974, 502]` -> `[600, 850, 930, 890]`.
  - old `#31` `header`: `[1221, 1035, 1264, 1053]` -> `[600, 850, 930, 890]`.
  - old `#32` `text_block`: `[1907, 1214, 1949, 1246]` -> `[1175, 850, 1220, 890]`.
  - old `#33` `table`: `[92, 866, 1225, 1026]` -> `[95, 850, 1215, 1035]`.
  - old `#57` `text_block`: `[2044, 730, 3200, 1053]` -> `[1255, 150, 2195, 1040]`.
  - old `#58` `title`: `[2168, 153, 2752, 218]` -> `[1280, 185, 1680, 225]`.
  - old `#59` `text_block`: `[1931, 252, 2019, 281]` -> `[1285, 185, 1325, 225]`.
  - old `#60` `text_block`: `[2044, 730, 3200, 1053]` -> `[1280, 245, 2190, 1040]`.
  - old `#61` `text_block`: `[2172, 184, 2546, 218]` -> `[1280, 245, 1600, 278]`.
  - old `#62` `text_block`: `[2172, 398, 3200, 438]` -> `[1290, 285, 2190, 320]`.
  - old `#63` `text_block`: `[2172, 405, 2197, 438]` -> `[1315, 285, 1380, 320]`.
  - old `#64` `text_block`: `[2107, 465, 2429, 561]` -> `[1390, 285, 1460, 320]`.
  - old `#65` `header`: `[2717, 477, 3093, 507]` -> `[1740, 285, 1960, 320]`.
  - old `#66` `text_block`: `[2128, 452, 3017, 484]` -> `[1290, 330, 2185, 365]`.
  - old `#67` `text_block`: `[2128, 452, 2197, 484]` -> `[1315, 330, 1380, 365]`.
  - old `#68` `text_block`: `[2129, 456, 2482, 470]` -> `[1390, 330, 1485, 365]`.
  - old `#69` `text_block`: `[2172, 496, 3093, 528]` -> `[1290, 375, 2190, 410]`.
  - old `#70` `text_block`: `[2172, 496, 2197, 528]` -> `[1315, 375, 1380, 410]`.
  - old `#71` `text_block`: `[2129, 456, 2475, 470]` -> `[1390, 375, 1485, 410]`.
  - old `#72` `text_block`: `[2100, 543, 3137, 583]` -> `[1290, 420, 2190, 455]`.
  - old `#73` `text_block`: `[2115, 550, 2229, 583]` -> `[1315, 420, 1440, 455]`.
  - old `#74` `text_block`: `[2136, 457, 2484, 475]` -> `[1450, 420, 1605, 455]`.
  - old `#75` `header`: `[3122, 182, 3200, 218]` -> `[2050, 420, 2185, 455]`.
  - old `#76` `text_block`: `[2172, 730, 2555, 773]` -> `[1280, 385, 1680, 420]`.
  - old `#77` `text_block`: `[2172, 730, 2890, 773]` -> `[1280, 425, 1850, 460]`.
  - old `#78` `equation_isolated`: `[1942, 322, 2349, 349]` -> `[1500, 500, 1940, 545]`.
  - old `#79` `header`: `[2357, 730, 3200, 773]` -> `[1500, 500, 1940, 545]`.
  - old `#80` `text_block`: `[2665, 319, 2698, 333]` -> `[2110, 500, 2160, 535]`.
  - old `#81` `text_block`: `[1757, 798, 3200, 838]` -> `[1280, 585, 2185, 635]`.
  - old `#82` `text_block`: `[2003, 773, 2273, 863]` -> `[1385, 585, 1415, 620]`.
  - old `#83` `text_block`: `[2358, 830, 2555, 871]` -> `[1490, 585, 1620, 620]`.
  - old `#84` `text_block`: `[2542, 798, 2673, 838]` -> `[1740, 585, 1770, 620]`.
  - old `#85` `text_block`: `[2938, 830, 3200, 871]` -> `[1900, 585, 2185, 620]`.
  - old `#86` `text_block`: `[2172, 863, 2555, 903]` -> `[1280, 570, 1620, 605]`.
  - old `#87` `text_block`: `[2172, 863, 2833, 903]` -> `[1280, 610, 1780, 645]`.
  - old `#88` `text_block`: `[2238, 933, 2523, 947]` -> `[1500, 610, 1645, 645]`.
  - old `#89` `equation_isolated`: `None` -> `[1450, 655, 2050, 705]`; added bbox to existing GT.
  - old `#90` `header`: `[2168, 933, 3200, 1053]` -> `[1450, 655, 2160, 705]`.
  - old `#91` `text_block`: `[2665, 442, 2698, 457]` -> `[2110, 655, 2160, 700]`.
  - old `#92` `text_block`: `[2168, 895, 3200, 1053]` -> `[1280, 730, 2185, 775]`.
  - old `#93` `text_block`: `[2054, 1091, 2090, 1130]` -> `[1280, 730, 1330, 775]`.
  - old `#94` `text_block`: `[1961, 450, 1983, 467]` -> `[1580, 730, 1610, 775]`.
  - old `#95` `text_block`: `[3122, 935, 3200, 1049]` -> `[1900, 730, 1945, 775]`.
  - old `#96` `text_block`: `[2122, 830, 3200, 1053]` -> `[1290, 795, 2185, 860]`.
  - old `#97` `text_block`: `[2082, 1173, 2179, 1209]` -> `[1310, 795, 1390, 835]`.
  - old `#98` `header`: `[2122, 830, 3200, 1053]` -> `[1680, 795, 2150, 835]`.
  - old `#99` `text_block`: `[2567, 1228, 2586, 1267]` -> `[1865, 835, 1900, 865]`.
  - old `#100` `text_block`: `[2801, 612, 3200, 648]` -> `[2200, 150, 3180, 1040]`.
  - old `#101` `title`: `[2835, 119, 3200, 143]` -> `[2250, 185, 3140, 225]`.
  - old `#102` `text_block`: `[2784, 119, 2818, 143]` -> `[2230, 185, 2265, 225]`.
  - old `#103` `text_block`: `[2779, 324, 3200, 364]` -> `[2250, 245, 3145, 1040]`.
  - old `#104` `text_block`: `[3185, 176, 3200, 192]` -> `[2250, 245, 2500, 278]`.
  - old `#105` `text_block`: `[2779, 176, 3200, 192]` -> `[2250, 285, 3120, 325]`.
  - old `#106` `text_block`: `None` -> `[2600, 285, 2800, 325]`; added bbox to existing GT.
  - old `#107` `equation_isolated`: `None` -> `[2550, 345, 2980, 390]`; added bbox to existing GT.
  - old `#108` `header`: `None` -> `[2550, 345, 2980, 390]`; added bbox to existing GT.
  - old `#109` `text_block`: `None` -> `[3100, 345, 3145, 390]`; added bbox to existing GT.
  - old `#110` `text_block`: `[2815, 241, 3130, 256]` -> `[2260, 365, 2700, 400]`.
  - old `#111` `text_block`: `[2815, 261, 3200, 275]` -> `[2260, 405, 2800, 440]`.
  - old `#112` `text_block`: `[3018, 261, 3200, 275]` -> `[2530, 405, 2760, 440]`.
  - old `#113` `text_block`: `[2815, 280, 3193, 295]` -> `[2260, 445, 2800, 480]`.
  - old `#114` `text_block`: `None` -> `[2250, 505, 2600, 540]`; added bbox to existing GT.
  - old `#115` `text_block`: `None` -> `[2250, 540, 3130, 600]`; added bbox to existing GT.
  - old `#116` `text_block`: `[2887, 326, 3023, 342]` -> `[2390, 540, 2520, 575]`.
  - old `#117` `text_block`: `[3029, 324, 3094, 347]` -> `[2600, 540, 2675, 575]`.
  - old `#118` `text_block`: `None` -> `[2250, 625, 2600, 660]`; added bbox to existing GT.
  - old `#119` `text_block`: `[2779, 396, 3200, 412]` -> `[2250, 665, 2900, 700]`.
  - old `#120` `equation_isolated`: `None` -> `[2500, 650, 3000, 690]`; added bbox to existing GT.
  - old `#121` `header`: `[3126, 425, 3200, 443]` -> `[2500, 650, 3000, 690]`.
  - old `#122` `text_block`: `None` -> `[3080, 650, 3130, 690]`; added bbox to existing GT.
  - old `#123` `table`: `[2198, 690, 3092, 904]` -> `[2250, 720, 3100, 925]`.
  - old `#153` `text_block`: `None` -> `[2250, 950, 3100, 1025]`; added bbox to existing GT.
  - old `#154` `text_block`: `[2801, 612, 2926, 628]` -> `[2250, 950, 2400, 990]`.
  - old `#155` `text_block`: `None` -> `[2660, 985, 2780, 1025]`; added bbox to existing GT.
  - old `#156` `code_txt`: `[153, 1610, 3200, 1635]` -> `[80, 1085, 3000, 1125]`.
  - old `#157` `text_block`: `[153, 1606, 3200, 1757]` -> `[80, 1085, 3000, 1165]`.
  - old `#158` `text_block`: `None` -> `[3040, 1060, 3150, 1185]`; added bbox to existing GT.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `14` (old `#6/#89/#106/#107/#108/#109/#114/#115/#118/#120/#122/#153/#155/#158`).
- Cleared existing bbox values: `0`.
- Non-bbox semantic changes recorded in this pass: `73` annotation order/id changes.

Verification:

- Report with full old/new order and bbox details: `reports/pdb_education_slides014_relabel_v605.json`.
- Visual dry-run cover check directory: `cover_audit_education_slides014_relabel_v605_dry/`.
- Visual dry-run outline check directory: `outline_audit_education_slides014_relabel_v605_dry/`.
- Visual cover check directory: `cover_audit_education_slides014_relabel_v605/`.
- Non-cover outline preview directory: `outline_audit_education_slides014_relabel_v605/`.
- Formal outline inspected: `outline_audit_education_slides014_relabel_v605/slides_014_材料化学_晶体结构_outline.jpg`.
- Static validation at write time: final run reports `order_changes=73`, `bbox_changes=107`, `bbox_added_to_existing=14`, `added_annotations=0`, `removed_annotations=0`, and `non_bbox_semantic_changes=73`.
- Frontend/cache validation: opened `http://127.0.0.1:8767/index.html?cb=20260611_education_slides014_relabel_v605`, filtered and selected case `236. 02_education/03_slides/slides_014_材料化学_晶体结构`; visible data label showed `data 20260611_education_slides014_relabel_v605`, active row showed `107/107 boxed · 0 no bbox`, page image was `03_slides/slides_014_材料化学_晶体结构.png` with natural size `3200x1800`, and overlay rendered `107` labels / `115` rect nodes.
- Latest token after this repair: `20260611_education_slides014_relabel_v605`.

## 20260611_education_slides015_relabel_v606

Scope:

- Full manual visual relabel for one slides case:
  - `02_education/03_slides/slides_015_DL_Systems_并行训练_ZHCN`
- User-visible issue: the page had widespread visual drift. Notable examples: old `#0/#9` spanned almost the whole page, right-side code annotations started around x=2600 instead of the actual code block at x=1620, bottom benchmark/communication tables and takeaway boxes were shifted, and 5 existing GT annotations had no bbox.
- This pass did not add or delete GT annotations.

Token:

- v606: `20260611_education_slides015_relabel_v606`

Method:

- Added and ran `scripts/fix_education_slides015_relabel_v606.py`.
- Used clean-PNG coordinate crops `/tmp/slides015_full_grid.jpg`, `/tmp/slides015_left_grid.jpg`, `/tmp/slides015_right_code_grid.jpg`, `/tmp/slides015_right_tables_grid.jpg`, and `/tmp/slides015_left_bottom_grid.jpg`.
- Reordered existing annotations into continuous visual order and rewrote affected `index` / `anno_id` values.
- Reset all 89 existing bboxes; 5 annotations had no bbox before this pass and received bboxes.
- Generated and inspected dry-run and formal cover/outline images before accepting the formal write.
- Updated `review_data.json`, `review_data.js`, and `index.html` query/cache token.

Case-level non-bbox semantic changes:

- `slides_015_DL_Systems_并行训练_ZHCN`: final status `89/89 boxed`, `0 no bbox`, `0 low-similarity`.
- Reading-order/id mapping:
  - old `#0-#80` remain in visual top-left-to-right sequence as new `#0-#80`.
  - old `#119/#120` -> new `#81/#82`.
  - old `#139/#140/#141` -> new `#83/#84/#85`.
  - old `#142/#143/#144` -> new `#86/#87/#88`.
  - This records `8` order/id changes caused by removing old deleted/gapped ids and enforcing continuous visual order.

Case-level bbox changes:

- `slides_015_DL_Systems_并行训练_ZHCN`: `89` existing bboxes changed/reset. Old indices below refer to the pre-v606 ids.
  - old `#0` `header`: `[65, 165, 3200, 1877]` -> `[65, 25, 3150, 115]`.
  - old `#1` `header`: `[220, 255, 3135, 271]` -> `[65, 25, 3150, 115]`.
  - old `#2` `text_block`: `[67, 165, 2026, 209]` -> `[65, 25, 1710, 115]`.
  - old `#3` `title`: `[67, 165, 2026, 209]` -> `[65, 25, 1710, 70]`.
  - old `#4` `text_block`: `[1612, 178, 2026, 209]` -> `[650, 25, 1710, 70]`.
  - old `#5` `text_block`: `[0, 39, 1296, 52]` -> `[70, 80, 1010, 112]`.
  - old `#6` `text_block`: `None` -> `[2810, 25, 3150, 112]`; added bbox to existing GT.
  - old `#7` `text_block`: `None` -> `[2820, 25, 3025, 55]`; added bbox to existing GT.
  - old `#8` `text_block`: `[103, 165, 2565, 1339]` -> `[65, 150, 1585, 1340]`.
  - old `#9` `text_block`: `[103, 165, 3200, 1817]` -> `[65, 150, 1585, 1340]`.
  - old `#10` `title`: `[65, 215, 899, 249]` -> `[65, 155, 930, 205]`.
  - old `#11` `text_block`: `[65, 215, 1827, 258]` -> `[70, 210, 1405, 250]`.
  - old `#12` `text_block`: `[472, 215, 899, 249]` -> `[415, 210, 600, 250]`.
  - old `#13` `text_block`: `[753, 259, 1215, 277]` -> `[715, 210, 900, 250]`.
  - old `#14` `text_block`: `[87, 281, 3135, 338]` -> `[90, 245, 1585, 310]`.
  - old `#15` `text_block`: `[107, 259, 675, 277]` -> `[110, 250, 560, 285]`.
  - old `#16` `text_block`: `[1614, 240, 2045, 258]` -> `[1120, 250, 1260, 285]`.
  - old `#17` `text_block`: `[2173, 260, 2294, 290]` -> `[1390, 250, 1490, 285]`.
  - old `#18` `text_block`: `[88, 377, 3045, 406]` -> `[90, 320, 1550, 378]`.
  - old `#19` `text_block`: `[88, 356, 557, 391]` -> `[110, 320, 610, 355]`.
  - old `#20` `text_block`: `[107, 443, 3135, 473]` -> `[90, 390, 1510, 445]`.
  - old `#21` `text_block`: `[88, 356, 557, 391]` -> `[110, 390, 620, 425]`.
  - old `#22` `text_block`: `[88, 414, 2714, 474]` -> `[90, 455, 1410, 495]`.
  - old `#23` `text_block`: `[91, 475, 774, 497]` -> `[110, 455, 650, 490]`.
  - old `#24` `title`: `[91, 470, 1080, 497]` -> `[65, 500, 1050, 550]`.
  - old `#25` `text_block`: `[66, 521, 575, 552]` -> `[65, 560, 590, 595]`.
  - old `#26` `equation_isolated`: `None` -> `[590, 595, 1270, 640]`; added bbox to existing GT.
  - old `#27` `header`: `[953, 608, 2555, 643]` -> `[590, 595, 1270, 640]`.
  - old `#28` `text_block`: `[2517, 608, 2555, 630]` -> `[1540, 600, 1580, 635]`.
  - old `#29` `text_block`: `[65, 653, 465, 685]` -> `[65, 655, 530, 690]`.
  - old `#30` `text_block`: `[91, 691, 463, 734]` -> `[90, 690, 520, 735]`.
  - old `#31` `text_block`: `[91, 691, 451, 734]` -> `[110, 690, 245, 735]`.
  - old `#32` `text_block`: `[91, 776, 850, 819]` -> `[90, 735, 520, 780]`.
  - old `#33` `text_block`: `[91, 734, 423, 777]` -> `[110, 735, 245, 780]`.
  - old `#34` `text_block`: `[91, 776, 950, 819]` -> `[90, 780, 960, 825]`.
  - old `#35` `text_block`: `[91, 776, 423, 819]` -> `[110, 780, 245, 825]`.
  - old `#36` `text_block`: `[91, 776, 950, 819]` -> `[90, 820, 650, 860]`.
  - old `#37` `text_block`: `[91, 815, 383, 854]` -> `[110, 820, 210, 860]`.
  - old `#38` `text_block`: `[173, 824, 624, 850]` -> `[250, 820, 430, 860]`.
  - old `#39` `equation_isolated`: `None` -> `[620, 860, 1200, 910]`; added bbox to existing GT.
  - old `#40` `header`: `[1010, 869, 2555, 904]` -> `[620, 860, 1200, 910]`.
  - old `#41` `text_block`: `[2513, 869, 2555, 892]` -> `[1540, 860, 1580, 900]`.
  - old `#42` `text_block`: `[65, 916, 994, 957]` -> `[65, 910, 990, 965]`.
  - old `#43` `header`: `[786, 921, 994, 954]` -> `[570, 910, 820, 960]`.
  - old `#44` `title`: `[65, 916, 633, 957]` -> `[65, 965, 620, 1005]`.
  - old `#45` `text_block`: `[113, 1009, 1685, 1037]` -> `[65, 1000, 1120, 1040]`.
  - old `#46` `text_block`: `[65, 1006, 345, 1040]` -> `[65, 1000, 150, 1040]`.
  - old `#47` `text_block`: `[65, 1005, 1068, 1042]` -> `[90, 1045, 680, 1080]`.
  - old `#48` `header`: `[641, 1005, 1068, 1040]` -> `[450, 1045, 665, 1080]`.
  - old `#49` `text_block`: `[91, 1048, 674, 1085]` -> `[90, 1080, 650, 1115]`.
  - old `#50` `header`: `[427, 1020, 965, 1042]` -> `[435, 1080, 650, 1115]`.
  - old `#51` `text_block`: `[91, 1120, 569, 1157]` -> `[90, 1115, 650, 1155]`.
  - old `#52` `header`: `[424, 1048, 674, 1084]` -> `[430, 1115, 570, 1155]`.
  - old `#53` `title`: `[65, 1213, 820, 1240]` -> `[65, 1165, 830, 1210]`.
  - old `#54` `text_block`: `[65, 1194, 2215, 1240]` -> `[65, 1200, 1515, 1270]`.
  - old `#55` `text_block`: `[66, 1213, 398, 1233]` -> `[65, 1205, 210, 1240]`.
  - old `#56` `text_block`: `[1807, 1216, 2026, 1231]` -> `[1110, 1205, 1165, 1240]`.
  - old `#57` `text_block`: `[1987, 1195, 2215, 1231]` -> `[1240, 1205, 1310, 1240]`.
  - old `#58` `text_block`: `[65, 1194, 2215, 1240]` -> `[65, 1285, 1565, 1340]`.
  - old `#59` `text_block`: `[83, 1289, 446, 1323]` -> `[85, 1288, 230, 1325]`.
  - old `#60` `code_txt`: `[2594, 1288, 3200, 1493]` -> `[1620, 155, 3135, 1115]`.
  - old `#61` `title`: `[2604, 166, 3200, 203]` -> `[1620, 155, 2100, 205]`.
  - old `#62` `text_block`: `[2604, 223, 3200, 253]` -> `[1620, 215, 2300, 255]`.
  - old `#63` `code_txt`: `[2632, 278, 3135, 1109]` -> `[1620, 260, 3135, 1115]`.
  - old `#64` `text_block`: `[2632, 278, 2748, 300]` -> `[1640, 275, 1760, 305]`.
  - old `#65` `text_block`: `[2632, 306, 2709, 328]` -> `[1640, 306, 1720, 335]`.
  - old `#66` `text_block`: `[3193, 334, 3200, 356]` -> `[2035, 330, 2080, 360]`.
  - old `#67` `text_block`: `[2632, 473, 3096, 495]` -> `[1640, 465, 1990, 495]`.
  - old `#68` `text_block`: `[2551, 375, 2971, 390]` -> `[1970, 550, 2370, 580]`.
  - old `#69` `text_block`: `[2632, 668, 3057, 691]` -> `[1640, 665, 1990, 695]`.
  - old `#70` `text_block`: `[2626, 506, 2776, 521]` -> `[2080, 745, 2210, 775]`.
  - old `#71` `text_block`: `[2821, 506, 2941, 521]` -> `[2230, 745, 2345, 775]`.
  - old `#72` `text_block`: `[3115, 836, 3135, 858]` -> `[2250, 825, 2405, 855]`.
  - old `#73` `text_block`: `[3019, 864, 3096, 886]` -> `[1970, 850, 2030, 880]`.
  - old `#74` `text_block`: `[3193, 891, 3200, 914]` -> `[2200, 885, 2460, 915]`.
  - old `#75` `text_block`: `[2632, 975, 3135, 998]` -> `[1640, 970, 2030, 1000]`.
  - old `#76` `text_block`: `[2746, 732, 2836, 747]` -> `[2290, 1085, 2370, 1115]`.
  - old `#77` `text_block`: `[2896, 732, 3046, 747]` -> `[2385, 1085, 2515, 1115]`.
  - old `#78` `title`: `[2604, 1140, 3200, 1177]` -> `[1620, 1135, 2200, 1185]`.
  - old `#79` `text_block`: `[2588, 1288, 3135, 1329]` -> `[1620, 1190, 2360, 1235]`.
  - old `#80` `table`: `[1600, 1237, 3136, 1487]` -> `[1620, 1235, 3135, 1485]`.
  - old `#119` `title`: `[2619, 1533, 3131, 1547]` -> `[1620, 1495, 2320, 1540]`.
  - old `#120` `table`: `[1600, 1543, 3136, 1710]` -> `[1620, 1545, 3135, 1705]`.
  - old `#139` `text_block`: `[2485, 1715, 3135, 1801]` -> `[1620, 1710, 3135, 1795]`.
  - old `#140` `text_block`: `[2499, 1715, 3135, 1801]` -> `[1640, 1715, 2000, 1760]`.
  - old `#141` `text_block`: `[2616, 1164, 2712, 1183]` -> `[2060, 1715, 2150, 1760]`.
  - old `#142` `text_block`: `[119, 1813, 3200, 1885]` -> `[80, 1800, 3130, 1865]`.
  - old `#143` `text_block`: `[136, 1841, 1880, 1870]` -> `[140, 1830, 1880, 1865]`.
  - old `#144` `text_block`: `None` -> `[3010, 1800, 3135, 1855]`; added bbox to existing GT.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `5` (old `#6/#7/#26/#39/#144`).
- Cleared existing bbox values: `0`.
- Non-bbox semantic changes recorded in this pass: `8` annotation order/id changes.

Verification:

- Report with full old/new order and bbox details: `reports/pdb_education_slides015_relabel_v606.json`.
- Visual dry-run cover check directory: `cover_audit_education_slides015_relabel_v606_dry/`.
- Visual dry-run outline check directory: `outline_audit_education_slides015_relabel_v606_dry/`.
- Visual cover check directory: `cover_audit_education_slides015_relabel_v606/`.
- Non-cover outline preview directory: `outline_audit_education_slides015_relabel_v606/`.
- Formal outline inspected: `outline_audit_education_slides015_relabel_v606/slides_015_DL_Systems_并行训练_ZHCN_outline.jpg`.
- Static validation at write time: final run reports `order_changes=8`, `bbox_changes=89`, `bbox_added_to_existing=5`, `added_annotations=0`, `removed_annotations=0`, and `non_bbox_semantic_changes=8`.
- Frontend/cache validation: opened `http://127.0.0.1:8767/index.html?cb=20260611_education_slides015_relabel_v606`, scrolled the case list and selected case `237. 02_education/03_slides/slides_015_DL_Systems_并行训练_ZHCN`; visible data label showed `data 20260611_education_slides015_relabel_v606`, active row showed `89/89 boxed · 0 no bbox`, page image was `03_slides/slides_015_DL_Systems_并行训练_ZHCN.png` with natural size `3200x1885`, and overlay rendered `89` labels / `97` rect nodes.
- Latest token after this repair: `20260611_education_slides015_relabel_v606`.

## 20260611_education_slides016_relabel_v607

Scope:

- Case: `02_education/03_slides/slides_016_Keynote_AI`.
- User-visible row: `238. 02_education/03_slides/slides_016_Keynote_AI`.
- Reason: slide case had obvious large-box overreach and non-continuous reading order after old id gaps; reset hero, metric cards, three content cards, quote, timeline, and footer bboxes to match visual regions.

Files updated:

- `review_data.json`
- `review_data.js`
- `index.html` cache/query token
- `GT_REPAIR_LOG.md`

Token and status:

- Previous token: `20260611_education_slides015_relabel_v606`.
- v607: `20260611_education_slides016_relabel_v607`.
- `slides_016_Keynote_AI`: final status `71/71 boxed`, `0 no bbox`, `0 low-similarity`.
- Visual reading order is now continuous `#0-#70`, top-to-bottom and left-to-right: hero, metrics, three feature cards, quote, timeline, footer.

Annotation order/id changes:

- old `#0-#29` remain new `#0-#29`.
- old `#46-#52` -> new `#30-#36`.
- old `#68-#74` -> new `#37-#43`.
- old `#89-#115` -> new `#44-#70`.
- Total non-bbox semantic/order changes recorded: `41`.

Case-level bbox changes:

- `slides_016_Keynote_AI`: `71` existing bboxes changed/reset. Old indices below refer to the pre-v607 ids.
  - old `#0` `header`: `[0, 0, 2478, 3388]` -> `[190, 175, 2290, 650]`.
  - old `#1` `text_block`: `[189, 178, 2289, 652]` -> `[190, 175, 2290, 650]`.
  - old `#2` `text_block`: `[917, 187, 1561, 218]` -> `[880, 175, 1600, 225]`.
  - old `#3` `title`: `[506, 295, 1972, 567]` -> `[500, 285, 1980, 565]`.
  - old `#4` `text_block`: `[739, 295, 1363, 433]` -> `[735, 285, 1365, 430]`.
  - old `#5` `text_block`: `[480, 602, 1998, 652]` -> `[480, 595, 2000, 650]`.
  - old `#6` `header`: `[189, 746, 2289, 1078]` -> `[190, 730, 2290, 1080]`.
  - old `#7` `text_block`: `[217, 781, 814, 1044]` -> `[220, 775, 820, 1048]`.
  - old `#8` `text_block`: `[352, 781, 678, 918]` -> `[335, 775, 690, 900]`.
  - old `#9` `text_block`: `[319, 924, 711, 962]` -> `[315, 915, 720, 965]`.
  - old `#10` `text_block`: `[293, 971, 738, 1006]` -> `[292, 968, 745, 1008]`.
  - old `#11` `text_block`: `[284, 1015, 746, 1044]` -> `[282, 1012, 750, 1050]`.
  - old `#12` `text_block`: `[941, 781, 1537, 1044]` -> `[940, 775, 1545, 1048]`.
  - old `#13` `text_block`: `[1051, 524, 1427, 548]` -> `[1040, 775, 1440, 900]`.
  - old `#14` `text_block`: `[1068, 924, 1410, 962]` -> `[1068, 915, 1415, 965]`.
  - old `#15` `text_block`: `[1009, 971, 1469, 1006]` -> `[1005, 968, 1470, 1008]`.
  - old `#16` `text_block`: `[1085, 1015, 1393, 1044]` -> `[1082, 1012, 1400, 1050]`.
  - old `#17` `header`: `[1664, 781, 2261, 1044]` -> `[1660, 775, 2265, 1048]`.
  - old `#18` `text_block`: `[1847, 807, 2078, 898]` -> `[1840, 775, 2090, 900]`.
  - old `#19` `text_block`: `[1766, 924, 2159, 962]` -> `[1765, 915, 2165, 965]`.
  - old `#20` `text_block`: `[1795, 971, 2131, 1006]` -> `[1790, 968, 2135, 1008]`.
  - old `#21` `code_txt`: `[1781, 1015, 2144, 1044]` -> `[1775, 1012, 2150, 1050]`.
  - old `#22` `header`: `[189, 1172, 2289, 2790]` -> `[190, 1170, 2290, 2785]`.
  - old `#23` `header`: `[223, 1200, 815, 1755]` -> `[190, 1170, 850, 2785]`.
  - old `#24` `text_block`: `[223, 1200, 612, 1269]` -> `[220, 1195, 625, 1268]`.
  - old `#25` `text_block`: `[235, 1208, 280, 1261]` -> `[220, 1200, 285, 1262]`.
  - old `#26` `title`: `[307, 1216, 612, 1254]` -> `[305, 1210, 625, 1258]`.
  - old `#27` `text_block`: `[223, 1285, 807, 1446]` -> `[220, 1280, 820, 1448]`.
  - old `#28` `text_block`: `[223, 1464, 771, 1558]` -> `[220, 1458, 790, 1562]`.
  - old `#29` `table`: `[223, 1571, 815, 1755]` -> `[220, 1568, 820, 1762]`.
  - old `#46` `header`: `[943, 1200, 1535, 1923]` -> `[910, 1170, 1570, 1930]`.
  - old `#47` `text_block`: `[943, 1200, 1384, 1269]` -> `[940, 1195, 1390, 1268]`.
  - old `#48` `text_block`: `[954, 1208, 1000, 1261]` -> `[950, 1200, 1010, 1262]`.
  - old `#49` `title`: `[1027, 1216, 1384, 1254]` -> `[1025, 1210, 1390, 1258]`.
  - old `#50` `text_block`: `[943, 1285, 1521, 1446]` -> `[940, 1280, 1530, 1448]`.
  - old `#51` `text_block`: `[943, 1464, 1510, 1558]` -> `[940, 1458, 1530, 1562]`.
  - old `#52` `table`: `[943, 1571, 1535, 1923]` -> `[940, 1568, 1540, 1930]`.
  - old `#68` `header`: `[1663, 1200, 2255, 1833]` -> `[1635, 1170, 2295, 1840]`.
  - old `#69` `text_block`: `[1663, 1200, 2081, 1269]` -> `[1660, 1195, 2095, 1268]`.
  - old `#70` `text_block`: `[1683, 1208, 1711, 1261]` -> `[1680, 1200, 1725, 1262]`.
  - old `#71` `title`: `[1747, 1216, 2081, 1254]` -> `[1745, 1210, 2095, 1258]`.
  - old `#72` `text_block`: `[1663, 1285, 2238, 1446]` -> `[1660, 1280, 2245, 1448]`.
  - old `#73` `text_block`: `[1663, 1464, 2237, 1558]` -> `[1660, 1458, 2250, 1562]`.
  - old `#74` `table`: `[1663, 1571, 2255, 1833]` -> `[1660, 1568, 2260, 1840]`.
  - old `#89` `text_block`: `[189, 2867, 2289, 2958]` -> `[650, 2865, 1845, 2960]`.
  - old `#90` `text_block`: `[966, 2921, 1512, 2952]` -> `[960, 2915, 1520, 2960]`.
  - old `#91` `header`: `[189, 3067, 2289, 3310]` -> `[190, 3060, 2290, 3310]`.
  - old `#92` `title`: `[1062, 3067, 1416, 3105]` -> `[1030, 3060, 1450, 3110]`.
  - old `#93` `header`: `[189, 3117, 2289, 3310]` -> `[190, 3115, 2290, 3310]`.
  - old `#94` `text_block`: `[198, 3133, 522, 3294]` -> `[200, 3130, 525, 3295]`.
  - old `#95` `text_block`: `[328, 3133, 392, 3167]` -> `[325, 3130, 395, 3170]`.
  - old `#96` `text_block`: `[208, 3205, 512, 3292]` -> `[205, 3200, 520, 3295]`.
  - old `#97` `text_block`: `[550, 3133, 873, 3264]` -> `[550, 3130, 875, 3265]`.
  - old `#98` `text_block`: `[679, 3133, 744, 3167]` -> `[675, 3130, 750, 3170]`.
  - old `#99` `header`: `[558, 3205, 865, 3263]` -> `[555, 3200, 870, 3265]`.
  - old `#100` `text_block`: `[901, 3133, 1225, 3264]` -> `[900, 3130, 1225, 3265]`.
  - old `#101` `text_block`: `[1031, 3133, 1096, 3167]` -> `[1025, 3130, 1100, 3170]`.
  - old `#102` `text_block`: `[910, 3205, 1217, 3263]` -> `[910, 3200, 1220, 3265]`.
  - old `#103` `header`: `[1253, 3133, 1577, 3264]` -> `[1250, 3130, 1580, 3265]`.
  - old `#104` `text_block`: `[1382, 3133, 1447, 3167]` -> `[1380, 3130, 1450, 3170]`.
  - old `#105` `text_block`: `[1281, 3205, 1549, 3263]` -> `[1280, 3200, 1555, 3265]`.
  - old `#106` `text_block`: `[1605, 3133, 1928, 3264]` -> `[1605, 3130, 1930, 3265]`.
  - old `#107` `text_block`: `[1734, 3133, 1799, 3167]` -> `[1730, 3130, 1805, 3170]`.
  - old `#108` `text_block`: `[1618, 3205, 1915, 3263]` -> `[1615, 3200, 1920, 3265]`.
  - old `#109` `header`: `[1956, 3133, 2280, 3294]` -> `[1955, 3130, 2285, 3295]`.
  - old `#110` `text_block`: `[2077, 3133, 2159, 3167]` -> `[2075, 3130, 2165, 3170]`.
  - old `#111` `text_block`: `[1981, 3205, 2256, 3292]` -> `[1980, 3200, 2260, 3295]`.
  - old `#112` `text_block`: `[189, 3357, 2289, 3388]` -> `[190, 3350, 2290, 3390]`.
  - old `#113` `text_block`: `[189, 3360, 589, 3388]` -> `[190, 3355, 590, 3390]`.
  - old `#114` `text_block`: `[989, 3357, 1554, 3388]` -> `[990, 3350, 1555, 3390]`.
  - old `#115` `text_block`: `[1954, 3360, 2289, 3388]` -> `[1950, 3355, 2290, 3390]`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `0`.
- Non-bbox semantic changes recorded in this pass: `41` annotation order/id changes.

Verification:

- Report with full old/new order and bbox details: `reports/pdb_education_slides016_relabel_v607.json`.
- Visual dry-run cover check directory: `cover_audit_education_slides016_relabel_v607_dry/`.
- Visual dry-run outline check directory: `outline_audit_education_slides016_relabel_v607_dry/`.
- Visual cover check directory: `cover_audit_education_slides016_relabel_v607/`.
- Non-cover outline preview directory: `outline_audit_education_slides016_relabel_v607/`.
- Formal outline inspected: `outline_audit_education_slides016_relabel_v607/slides_016_Keynote_AI_outline.jpg`.
- Static validation at write time: final run reports `order_changes=41`, `bbox_changes=71`, `bbox_added_to_existing=0`, `added_annotations=0`, `removed_annotations=0`, and `non_bbox_semantic_changes=41`.
- Frontend/cache validation: opened `http://127.0.0.1:8767/index.html?cb=20260611_education_slides016_relabel_v607`, selected case `238. 02_education/03_slides/slides_016_Keynote_AI`; visible data label showed `data 20260611_education_slides016_relabel_v607`, active row showed `71/71 boxed · 0 no bbox`, page image was `02_education/03_slides/slides_016_Keynote_AI.png` with natural size `2478x3506`, and overlay rendered `71` labels / `79` rect nodes with labels continuing through `#70`.
- Latest token after this repair: `20260611_education_slides016_relabel_v607`.

## 20260611_education_slides029_tables_v608

Scope:

- Case: `02_education/03_slides/slides_029_产品发布_手机`.
- User-visible row: `240. 02_education/03_slides/slides_029_产品发布_手机`.
- Reason: user flagged that some regions are visually tables but were marked as `text_block`; visual check also found the middle wrapper `#20` overreached into blank space and several top specification-card text boxes were slightly over-broad.

Files updated:

- `review_data.json`
- `review_data.js`
- `index.html` cache/query token
- `GT_REPAIR_LOG.md`

Token and status:

- Previous token: `20260611_education_slides016_relabel_v607`.
- v608: `20260611_education_slides029_tables_v608`.
- `slides_029_产品发布_手机`: final status `116/116 boxed`, `0 no bbox`, `0 low-similarity`.
- Visual reading order is now continuous `#0-#115`; old bottom ids `#104-#123` were compressed to new `#96-#115`.

Annotation order/id changes:

- Total order/id changes recorded: `64`.
- Main title order fixed: old `#60` -> new `#3`.
- Top specification cards reordered into visual left-to-right card order:
  - old `#12/#11/#10` -> new `#10/#11/#12` for the display card.
  - old `#15/#14/#13` -> new `#13/#14/#15` for the camera card.
  - old `#19/#75/#18/#16` -> new `#16/#17/#18/#19` for the battery card.
- Left detailed-specification table remains in visual row order; old `#53/#54/#55` -> new `#52/#53/#54`.
- Right comparison/AI table region moves to new `#55-#95`; notable moved table entries:
  - old `#56/#57/#58/#59` -> new `#55/#56/#57/#58`.
  - old `#3` table-column header `NovaPro X1` -> new `#59`.
  - old `#17` table battery value `6000 mAh` -> new `#74`.
  - old `#52` table row label `卫星通信` -> new `#87`.
- Bottom pricing/footer range old `#104-#123` -> new `#96-#115`.

Category/type changes:

- Changed `5` existing annotations from `text_block` to `table`:
  - old `#20`: `text_block` -> `table`, middle composite table region, bbox now `[165, 885, 2313, 1940]`.
  - old `#21`: `text_block` -> `table`, left `详细参数规格` table, bbox `[165, 920, 1215, 1940]`.
  - old `#23`: `text_block` -> `table`, left detail-table body, bbox `[165, 990, 1215, 1940]`.
  - old `#56`: `text_block` -> `table`, right comparison/AI table block, bbox `[1263, 908, 2313, 1838]`.
  - old `#58`: `text_block` -> `table`, right `vs 竞品参数对比` table body, bbox `[1263, 960, 2313, 1507]`.

Case-level bbox changes:

- `slides_029_产品发布_手机`: `7` existing bboxes changed/reset. Old indices below refer to the pre-v608 ids.
  - old `#12` `text_block`: `[736, 535, 1194, 729]` -> `[851, 632, 1078, 728]`.
  - old `#13` `text_block`: `[1341, 553, 1686, 567]` -> `[1390, 632, 1645, 728]`.
  - old `#15` `text_block`: `[1284, 535, 1742, 729]` -> `[1390, 632, 1645, 728]`.
  - old `#16` `text_block`: `[1895, 579, 2229, 728]` -> `[1895, 640, 2229, 728]`.
  - old `#19` `text_block`: `[1833, 535, 2291, 729]` -> `[1895, 640, 2229, 728]`.
  - old `#20` `text_block`: `[165, 885, 2313, 2996]` -> `[165, 885, 2313, 1940]`.
  - old `#59` `text_block`: `[1778, 911, 1836, 946]` -> `[1325, 968, 1380, 996]`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `0`.
- Non-bbox semantic changes recorded in this pass: `69` (`64` order/id changes + `5` category/type changes).

Verification:

- Report with full old/new order, bbox, and category details: `reports/pdb_education_slides029_tables_v608.json`.
- Visual dry-run cover check directory: `cover_audit_education_slides029_tables_v608_dry/`.
- Visual dry-run outline check directory: `outline_audit_education_slides029_tables_v608_dry/`.
- Visual cover check directory: `cover_audit_education_slides029_tables_v608/`.
- Non-cover outline preview directory: `outline_audit_education_slides029_tables_v608/`.
- Formal outline inspected: `outline_audit_education_slides029_tables_v608/slides_029_产品发布_手机_outline.jpg`.
- Static validation at write time: final run reports `order_changes=64`, `bbox_changes=7`, `category_changes=5`, `bbox_added_to_existing=0`, `added_annotations=0`, `removed_annotations=0`, and `non_bbox_semantic_changes=69`.
- Frontend/cache validation: opened `http://127.0.0.1:8767/index.html?cb=20260611_education_slides029_tables_v608`, selected case `240. 02_education/03_slides/slides_029_产品发布_手机`; visible data label showed `data 20260611_education_slides029_tables_v608`, active row showed `116/116 boxed · 0 no bbox`, page image was `02_education/03_slides/slides_029_产品发布_手机.png` with natural size `2478x3506`, and overlay rendered `116` labels / `124` rect nodes with labels continuing through `#115`.
- Latest token after this repair: `20260611_education_slides029_tables_v608`.

## 20260611_education_slides019_card_labels_v609

Scope:

- Case: `02_education/03_slides/slides_019_竞品分析`.
- User-visible row: `239. 02_education/03_slides/slides_019_竞品分析`.
- Reason: user flagged that top-card labels such as `#8/#13` visually drifted into the feature comparison matrix; visual check confirmed the same issue for the other product cards, plus a misplaced composite/header bbox and a misplaced `战略建议` title bbox.

Files updated:

- `review_data.json`
- `review_data.js`
- `index.html` cache/query token
- `GT_REPAIR_LOG.md`

Token and status:

- Previous token: `20260611_education_slides029_tables_v608`.
- v609: `20260611_education_slides019_card_labels_v609`.
- `slides_019_竞品分析`: final status `46/46 boxed`, `0 no bbox`, `0 low-similarity`.
- Visual reading order is now continuous `#0-#45`; the old lower-section id gaps were compressed while preserving visual top-to-bottom order.

Annotation order/id changes:

- old `#0-#28` remain new `#0-#28`.
- old `#69/#70` -> new `#29/#30`.
- old `#91-#105` -> new `#31-#45`.
- Total non-bbox semantic/order changes recorded: `17`.

Case-level bbox changes:

- `slides_019_竞品分析`: `6` existing bboxes changed/reset. Old indices below refer to the pre-v609 ids.
  - old `#0` `header`: `[114, 1939, 2368, 2269]` -> `[114, 104, 2368, 2210]`.
  - old `#8` `text_block`: `[866, 731, 898, 762]` -> `[330, 297, 440, 340]`.
  - old `#13` `text_block`: `[1253, 731, 1285, 761]` -> `[920, 297, 990, 340]`.
  - old `#18` `text_block`: `[1639, 731, 1672, 761]` -> `[1448, 297, 1608, 340]`.
  - old `#23` `text_block`: `[2090, 733, 2117, 764]` -> `[2036, 297, 2160, 340]`.
  - old `#102` `title`: `[132, 2505, 241, 2540]` -> `[135, 2610, 285, 2650]`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `0`.
- Non-bbox semantic changes recorded in this pass: `17` annotation order/id changes.

Verification:

- Report with full old/new order and bbox details: `reports/pdb_education_slides019_card_labels_v609.json`.
- Visual scout cover check directory: `cover_audit_education_slides019_v609_scout/`.
- Visual scout outline check directory: `outline_audit_education_slides019_v609_scout/`.
- Visual dry-run cover check directory: `cover_audit_education_slides019_card_labels_v609_dry/`.
- Visual dry-run outline check directory: `outline_audit_education_slides019_card_labels_v609_dry/`.
- Visual cover check directory: `cover_audit_education_slides019_card_labels_v609/`.
- Non-cover outline preview directory: `outline_audit_education_slides019_card_labels_v609/`.
- Formal outline inspected: `outline_audit_education_slides019_card_labels_v609/slides_019_竞品分析_outline.jpg`; `#8/#13/#18/#23` are back on the four product cards, and `#102` is back on `战略建议`.
- Static validation at write time: final run reports `order_changes=17`, `bbox_changes=6`, `bbox_added_to_existing=0`, `added_annotations=0`, `removed_annotations=0`, and `non_bbox_semantic_changes=17`.
- Frontend/cache validation: opened `http://127.0.0.1:8767/index.html?cb=20260611_education_slides019_card_labels_v609`, selected case `239. 02_education/03_slides/slides_019_竞品分析`; visible data label showed `data 20260611_education_slides019_card_labels_v609`, active row showed `46/46 boxed · 0 no bbox`, page image was `02_education/03_slides/slides_019_竞品分析.png` with natural size `2478x3506`, and overlay rendered `46` labels continuing through `#45`.
- Latest token after this repair: `20260611_education_slides019_card_labels_v609`.

## 20260611_education_slides029_table_dedupe_v610

Scope:

- Case: `02_education/03_slides/slides_029_产品发布_手机`.
- User-visible row: `240. 02_education/03_slides/slides_029_产品发布_手机`.
- Reason: after v608 changed several visual table regions to `table`, the same table contents still had duplicated cell-level `text_block` annotations and broad wrapper table annotations. This pass consolidates those duplicated GT fragments into the retained table-level annotations.

Files updated:

- `review_data.json`
- `review_data.js`
- `index.html` cache/query token
- `GT_REPAIR_LOG.md`

Token and status:

- Previous token: `20260611_education_slides019_card_labels_v609`.
- v610: `20260611_education_slides029_table_dedupe_v610`.
- `slides_029_产品发布_手机`: final status `45/45 boxed`, `0 no bbox`, `0 low-similarity`.
- Visual reading order is now continuous `#0-#44`.

Retained table-level GT annotations:

- old `#21` left `详细参数规格` table -> new `#20`, bbox `[165, 920, 1215, 1940]`.
- old `#57` right `vs 竞品参数对比` table -> new `#22`, bbox `[1263, 960, 2313, 1507]`.
- old `#95` right `AI 旗舰功能` table -> new `#24`, bbox `[1263, 1613, 2313, 1838]`.

Removed duplicated GT annotations:

- Deleted old `#20`: broad wrapper table covering both left and right tables.
- Deleted old `#22-#54`: left specification-table title/body/cell fragments duplicated by retained old `#21`.
- Deleted old `#55`: broad wrapper table covering the right comparison and AI tables.
- Deleted old `#58-#93`: right comparison-table cell fragments duplicated by retained old `#57`.
- Total removed GT annotations in this pass: `71`.

Annotation order/id changes:

- After deletion, retained annotations were renumbered to continuous visual order.
- Total order/id changes recorded: `25`.
- Notable remaps: old `#21` -> new `#20`; old `#56` -> new `#21`; old `#57` -> new `#22`; old `#94` -> new `#23`; old `#95` -> new `#24`; old `#96-#115` -> new `#25-#44`.

Case-level bbox changes:

- `0` existing bboxes were changed in this pass; this pass only removed duplicated GT annotations and renumbered retained annotations.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `71`.
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `0`.
- Non-bbox semantic changes recorded in this pass: `96` (`71` deletions + `25` order/id changes).

Verification:

- Report with full removed-item and order-change details: `reports/pdb_education_slides029_table_dedupe_v610.json`.
- Visual dry-run cover check directory: `cover_audit_education_slides029_table_dedupe_v610_dry/`.
- Visual dry-run outline check directory: `outline_audit_education_slides029_table_dedupe_v610_dry/`.
- Visual cover check directory: `cover_audit_education_slides029_table_dedupe_v610/`.
- Non-cover outline preview directory: `outline_audit_education_slides029_table_dedupe_v610/`.
- Formal outline inspected: `outline_audit_education_slides029_table_dedupe_v610/slides_029_产品发布_手机_outline.jpg`; the table-cell duplicate overlays are gone, while the three retained table boxes, top cards, pricing cards, preorder note, and footer remain boxed.
- Static validation at write time: final run reports `removed_annotations=71`, `added_annotations=0`, `bbox_changes=0`, `order_changes=25`, and `non_bbox_semantic_changes=96`.
- Frontend/cache validation: opened `http://127.0.0.1:8767/index.html?cb=20260611_education_slides029_table_dedupe_v610`, selected case `240. 02_education/03_slides/slides_029_产品发布_手机`; visible data label showed `data 20260611_education_slides029_table_dedupe_v610`, active row showed `45/45 boxed · 0 no bbox`, page image was `02_education/03_slides/slides_029_产品发布_手机.png` with natural size `2478x3506`, and overlay rendered `45` labels continuing through `#44`.
- Latest token after this repair: `20260611_education_slides029_table_dedupe_v610`.

## 20260611_education_slides030_human_ai_relabel_v611

Scope:

- Case: `02_education/03_slides/slides_030_Human_AI_CoReading`.
- User-visible row: `241. 02_education/03_slides/slides_030_Human_AI_CoReading`.
- Reason: user flagged the slides cases as broadly mislabelled. Visual review showed this case had broad wrapper boxes, nested duplicate spans, page-number drift, and many reading-order gaps from the original HTML-derived annotations.

Files updated:

- `review_data.json`
- `review_data.js`
- `index.html` cache/query token
- `GT_REPAIR_LOG.md`

Token and status:

- Previous token: `20260611_education_slides029_table_dedupe_v610`.
- v611: `20260611_education_slides030_human_ai_relabel_v611`.
- `slides_030_Human_AI_CoReading`: final status `54/54 boxed`, `0 no bbox`, `0 low-similarity`.
- Visual reading order is now continuous `#0-#53`.

Removed duplicated/drifted GT annotations:

- Deleted old `#0/#4/#5`: broad header wrappers that duplicated the top metadata/title region.
- Deleted old `#11/#12/#15`: metric-card wrappers/spans duplicated by retained metric value/label boxes.
- Deleted old `#18/#19/#22/#23/#24/#25`: broad/nested pipeline paragraph and sticky-note fragments duplicated by retained paragraph/note boxes.
- Deleted old `#28/#29/#31/#40/#42/#76`: formula/module broad wrappers and duplicate note fragments duplicated by retained equations/table/text boxes.
- Deleted old `#78/#81/#83/#84/#90/#91/#92/#93/#94/#96`: second-slide broad wrappers and table duplicates.
- Deleted old `#146/#148/#165`: duplicate user-study table wrapper/body/footer fragments.
- Deleted old `#167/#169/#171/#172/#173/#174/#175/#177/#178/#179/#180/#181/#183/#184/#185/#186/#187/#189/#190/#191/#192/#193/#195/#196/#197/#198/#199/#200/#201/#202/#205`: duplicate case-study/failure-note fragments.
- Total removed GT annotations in this pass: `62`.

Annotation order/id changes:

- Retained annotations were renumbered to continuous visual reading order.
- Top metadata/title/metric section: old `#1/#2/#6/#7/#8/#9/#10/#13/#14/#16/#17` -> new `#0-#10`.
- Pipeline paragraph and notes: old `#20/#21/#26/#27` -> new `#11-#14`.
- Formula/module panel: old `#30/#32/#33/#34/#35/#36/#37/#38/#39/#41/#43/#74/#75/#77/#3` -> new `#15-#29`.
- Second slide heading/results: old `#79/#80/#85/#86/#87/#88/#89` -> new `#30-#36`.
- Left result tables/figure title: old `#95/#97/#145/#147/#149/#166` -> new `#37-#42`.
- Right case-study/failure/footer area: old `#168/#170/#176/#182/#188/#194/#203/#204/#206/#207/#82` -> new `#43-#53`.
- Total order/id changes recorded: `54`.

Case-level bbox changes:

- `slides_030_Human_AI_CoReading`: `53` existing bboxes changed/reset. Old indices below refer to the pre-v611 ids.
  - old `#1` -> new `#0` `header`: `[0, 35, 404, 94]` -> `[60, 48, 340, 64]`.
  - old `#2` -> new `#1` `text_block`: `[1988, 35, 2400, 90]` -> `[2080, 48, 2345, 64]`.
  - old `#6` -> new `#2` `text_block`: `[19, 115, 449, 180]` -> `[110, 86, 354, 116]`.
  - old `#7` -> new `#3` `text_block`: `[266, 78, 656, 133]` -> `[378, 88, 550, 122]`.
  - old `#8` -> new `#4` `title`: `[0, 150, 1188, 227]` -> `[110, 134, 1065, 250]`.
  - old `#9` -> new `#5` `text_block`: `[0, 280, 949, 295]` -> `[110, 278, 1060, 316]`.
  - old `#10` -> new `#6` `text_block`: `[0, 291, 1048, 356]` -> `[110, 326, 1050, 352]`.
  - old `#13` -> new `#7` `text_block`: `[1820, 64, 2168, 77]` -> `[1942, 82, 2058, 132]`.
  - old `#14` -> new `#8` `text_block`: `[1848, 64, 2168, 77]` -> `[1918, 145, 2078, 190]`.
  - old `#16` -> new `#9` `text_block`: `[2044, 35, 2388, 90]` -> `[2150, 82, 2260, 132]`.
  - old `#17` -> new `#10` `text_block`: `[2044, 35, 2388, 90]` -> `[2122, 145, 2300, 190]`.
  - old `#20` -> new `#11` `text_block`: `[19, 365, 496, 398]` -> `[110, 360, 590, 394]`.
  - old `#21` -> new `#12` `header`: `[48, 488, 1410, 803]` -> `[110, 918, 1342, 1038]`.
  - old `#26` -> new `#13` `text_block`: `[12, 1071, 721, 1112]` -> `[110, 1062, 720, 1116]`.
  - old `#27` -> new `#14` `text_block`: `[600, 1103, 1459, 1179]` -> `[735, 1062, 1340, 1116]`.
  - old `#30` -> new `#15` `title`: `[1260, 316, 1748, 329]` -> `[1360, 360, 1810, 394]`.
  - old `#33` -> new `#17` `text_block`: `[2097, 478, 2256, 492]` -> `[2096, 474, 2268, 494]`.
  - old `#34` -> new `#18` `equation_isolated`: `[1669, 513, 1981, 548]` -> `[1668, 512, 1984, 548]`.
  - old `#35` -> new `#19` `text_block`: `[2045, 574, 2256, 588]` -> `[2044, 572, 2268, 592]`.
  - old `#36` -> new `#20` `equation_isolated`: `[1562, 608, 2089, 638]` -> `[1560, 607, 2090, 640]`.
  - old `#37` -> new `#21` `text_block`: `[2091, 666, 2256, 681]` -> `[2090, 664, 2268, 684]`.
  - old `#38` -> new `#22` `equation_isolated`: `[1668, 698, 1982, 728]` -> `[1666, 698, 1984, 730]`.
  - old `#39` -> new `#23` `text_block`: `[1988, 783, 2373, 806]` -> `[1988, 782, 2373, 808]`.
  - old `#41` -> new `#24` `text_block`: `[1274, 797, 1669, 848]` -> `[1360, 808, 1785, 846]`.
  - old `#43` -> new `#25` `table`: `[1372, 880, 2278, 1096]` -> `[1362, 866, 2285, 1078]`.
  - old `#74` -> new `#26` `text_block`: `[1140, 1029, 2400, 1072]` -> `[1360, 1098, 2300, 1152]`.
  - old `#75` -> new `#27` `figure_caption`: `[1204, 1225, 2335, 1277]` -> `[1360, 1165, 2300, 1210]`.
  - old `#77` -> new `#28` `text_block`: `[1540, 1225, 2112, 1268]` -> `[1662, 1240, 1995, 1268]`.
  - old `#3` -> new `#29` `page_number`: `[2185, 1152, 2400, 1213]` -> `[2250, 1260, 2338, 1292]`.
  - old `#79` -> new `#30` `text_block`: `[0, 1405, 391, 1450]` -> `[65, 1434, 340, 1455]`.
  - old `#80` -> new `#31` `text_block`: `[2071, 1405, 2400, 1450]` -> `[2140, 1420, 2325, 1458]`.
  - old `#85` -> new `#32` `text_block`: `[26, 1483, 514, 1519]` -> `[110, 1485, 350, 1518]`.
  - old `#86` -> new `#33` `text_block`: `[322, 1483, 689, 1519]` -> `[428, 1485, 620, 1518]`.
  - old `#87` -> new `#34` `title`: `[0, 1549, 1147, 1594]` -> `[110, 1540, 830, 1592]`.
  - old `#88` -> new `#35` `text_block`: `[0, 1571, 607, 1590]` -> `[110, 1596, 610, 1626]`.
  - old `#89` -> new `#36` `text_block`: `[1963, 1560, 2364, 1594]` -> `[2030, 1480, 2290, 1592]`.
  - old `#95` -> new `#37` `title`: `[0, 1699, 605, 1742]` -> `[110, 1658, 735, 1696]`.
  - old `#97` -> new `#38` `table`: `[122, 1717, 1323, 1969]` -> `[110, 1702, 1325, 1970]`.
  - old `#145` -> new `#39` `header`: `[773, 1909, 1430, 1950]` -> `[765, 1952, 1320, 1976]`.
  - old `#147` -> new `#40` `title`: `[0, 2045, 544, 2090]` -> `[110, 2000, 700, 2038]`.
  - old `#149` -> new `#41` `table`: `[122, 2076, 1323, 2185]` -> `[110, 2044, 1325, 2186]`.
  - old `#166` -> new `#42` `text_block`: `[0, 2163, 537, 2196]` -> `[110, 2164, 650, 2200]`.
  - old `#168` -> new `#43` `text_block`: `[1219, 1623, 1687, 1648]` -> `[1340, 1640, 1708, 1678]`.
  - old `#170` -> new `#44` `header`: `[1211, 1641, 1951, 1788]` -> `[1340, 1690, 1815, 1855]`.
  - old `#176` -> new `#45` `header`: `[1802, 1641, 2400, 1788]` -> `[1830, 1690, 2295, 1855]`.
  - old `#182` -> new `#46` `header`: `[1212, 1939, 1939, 1952]` -> `[1340, 1870, 1815, 2025]`.
  - old `#188` -> new `#47` `header`: `[1711, 1939, 2400, 1952]` -> `[1830, 1870, 2295, 2025]`.
  - old `#194` -> new `#48` `header`: `[1341, 2012, 2296, 2291]` -> `[1340, 1986, 2295, 2220]`.
  - old `#203` -> new `#49` `header`: `[1325, 2305, 1831, 2350]` -> `[1340, 2228, 1770, 2318]`.
  - old `#204` -> new `#50` `header`: `[1747, 2305, 2365, 2350]` -> `[1810, 2228, 2295, 2318]`.
  - old `#206` -> new `#51` `header`: `[0, 2665, 1039, 2706]` -> `[110, 2668, 850, 2696]`.
  - old `#207` -> new `#52` `text_block`: `[1783, 2665, 2400, 2706]` -> `[1810, 2668, 2320, 2696]`.
  - old `#82` -> new `#53` `page_number`: `[130, 417, 1328, 920]` -> `[2250, 2668, 2338, 2698]`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `62`.
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `0`.
- Category/type changes in this pass: `0`.
- Non-bbox semantic changes recorded in this pass: `116` (`62` deletions + `54` order/id changes).

Verification:

- Report with full removed-item, order-change, and bbox-change details: `reports/pdb_education_slides030_human_ai_relabel_v611.json`.
- Visual dry-run cover check directories: `cover_audit_education_slides030_human_ai_relabel_v611_dry2/`, `cover_audit_education_slides030_human_ai_relabel_v611_dry3/`, `cover_audit_education_slides030_human_ai_relabel_v611_dry4/`, `cover_audit_education_slides030_human_ai_relabel_v611_dry5/`.
- Visual dry-run outline check directories: `outline_audit_education_slides030_human_ai_relabel_v611_dry2/`, `outline_audit_education_slides030_human_ai_relabel_v611_dry3/`, `outline_audit_education_slides030_human_ai_relabel_v611_dry4/`, `outline_audit_education_slides030_human_ai_relabel_v611_dry5/`.
- Visual cover check directory: `cover_audit_education_slides030_human_ai_relabel_v611/`.
- Non-cover outline preview directory: `outline_audit_education_slides030_human_ai_relabel_v611/`.
- Formal outline inspected: `outline_audit_education_slides030_human_ai_relabel_v611/slides_030_Human_AI_CoReading_outline.jpg`; bottom-right failure-analysis/note crop also inspected after final bbox tightening.
- Static validation at write time: final run reports `removed_annotations=62`, `added_annotations=0`, `bbox_changes=53`, `order_changes=54`, `bbox_added_to_existing=0`, and `non_bbox_semantic_changes=116`.
- Frontend/cache validation: opened `http://127.0.0.1:8767/index.html?cb=20260611_education_slides030_human_ai_relabel_v611`, selected case `241. 02_education/03_slides/slides_030_Human_AI_CoReading`; visible data label showed `data 20260611_education_slides030_human_ai_relabel_v611`, active row showed `54/54 boxed · 0 no bbox`, page image was `02_education/03_slides/slides_030_Human_AI_CoReading.png` with natural size `2400x2740`, and overlay rendered `54` labels continuing through `#53`.
- Latest token after this repair: `20260611_education_slides030_human_ai_relabel_v611`.

## 20260611_education_slides030_urban_resilience_relabel_v612

Scope:

- Case: `02_education/03_slides/slides_030_Smart_Urban_Resilience_2in1`.
- User-visible row: `242. 02_education/03_slides/slides_030_Smart_Urban_Resilience_2in1`.
- Reason: user flagged the adjacent slides case as broadly mislabelled. Visual review showed full-page wrappers, misplaced fragments from the wrong page, no-bbox fragments in risk/timeline cards, duplicate table/text fragments, and incorrect reading order.

Files updated:

- `review_data.json`
- `review_data.js`
- `index.html` cache/query token
- `GT_REPAIR_LOG.md`

Token and status:

- Previous token: `20260611_education_slides030_human_ai_relabel_v611`.
- v612: `20260611_education_slides030_urban_resilience_relabel_v612`.
- `slides_030_Smart_Urban_Resilience_2in1`: final status `76/76 boxed`, `0 no bbox`, `0 low-similarity`.
- Visual reading order is now continuous `#0-#75`.

Removed duplicated/drifted GT annotations:

- Deleted old `#0-#3`, `#8`, `#11-#12`, `#16`, `#18`, `#20`, `#22`, `#24-#26`, `#28-#32`, `#34-#38`, `#40-#44`, `#46`, `#50-#56`, `#58-#62`, `#64-#68`, `#70-#77`, `#81-#93`, `#100`, `#103`, `#124`, `#126`, `#129-#131`, `#135`, `#138-#139`, `#143`, `#145`, `#147`, `#149`, `#151-#154`, `#206-#208`, `#212`, `#215-#217`, `#238-#239`, `#242`, `#244-#245`, `#247-#248`, `#250-#251`, `#253-#256`, `#259`, `#261`, `#263`, `#265`, `#267-#268`, `#270`.
- Total removed GT annotations in this pass: `113`.

Annotation order/id changes:

- Retained annotations were renumbered to continuous visual reading order.
- Page 1 header/title/KPI cards: old `#4/#5/#6/#7/#9/#10/#13/#14/#15/#17/#19/#21/#23` -> new `#0-#12`.
- Page 1 left cards, center map, right cards: old `#27/#33/#39/#47/#48/#45/#49/#57/#63/#69` -> new `#13-#22`.
- Page 1 workflow/rules/table/footer: old `#78/#79/#80/#94/#95/#96/#97/#98/#101/#102/#99/#125/#127/#128` -> new `#23-#36`.
- Page 2 header/title/KPI cards: old `#132/#133/#134/#136/#137/#140/#141/#142/#144/#146/#148/#150` -> new `#37-#48`.
- Page 2 budget/reading/trend: old `#155/#156/#157/#209/#210/#211/#213/#214` -> new `#49-#56`.
- Page 2 RACI/risk cards/timeline/footer: old `#218/#219/#220/#237/#240/#241/#243/#246/#249/#252/#257/#258/#260/#262/#264/#266/#269/#271/#272` -> new `#57-#75`.
- Total order/id changes recorded: `76`.

Category/type changes:

- old `#45` -> new `#18`: `text_block` -> `figure`, bbox `[520, 640, 1890, 1605]`, for the central city-network control map.
- old `#80` -> new `#25`: `text_block` -> `figure`, bbox `[55, 1760, 1415, 1915]`, for the Dispatch Workflow diagram.

Case-level bbox changes:

- `slides_030_Smart_Urban_Resilience_2in1`: `76` retained bboxes changed/reset. Old indices below refer to the pre-v612 ids.
  - old `#4` -> new `#0` `text_block`: `[0, 134, 938, 148]` -> `[35, 38, 315, 60]`.
  - old `#5` -> new `#1` `text_block`: `[722, 107, 1303, 120]` -> `[338, 32, 512, 66]`.
  - old `#6` -> new `#2` `text_block`: `[1266, 73, 1617, 95]` -> `[528, 32, 714, 66]`.
  - old `#7` -> new `#3` `text_block`: `[1618, 73, 2429, 95]` -> `[1608, 32, 1973, 66]`.
  - old `#9` -> new `#4` `text_block`: `[2000, 73, 2279, 95]` -> `[1985, 32, 2295, 66]`.
  - old `#10` -> new `#5` `page_number`: `[2307, 39, 2429, 95]` -> `[2308, 35, 2428, 60]`.
  - old `#13` -> new `#6` `title`: `[152, 110, 2464, 206]` -> `[35, 88, 1540, 151]`.
  - old `#14` -> new `#7` `text_block`: `[152, 210, 1828, 249]` -> `[35, 175, 790, 212]`.
  - old `#15` -> new `#8` `text_block`: `[152, 266, 2464, 328]` -> `[35, 238, 1835, 295]`.
  - old `#17` -> new `#9` `text_block`: `[1940, 197, 2137, 307]` -> `[1924, 86, 2170, 288]`.
  - old `#19` -> new `#10` `text_block`: `[2200, 104, 2407, 307]` -> `[2184, 86, 2430, 288]`.
  - old `#21` -> new `#11` `text_block`: `[1941, 321, 2133, 523]` -> `[1924, 304, 2170, 506]`.
  - old `#23` -> new `#12` `text_block`: `[2200, 321, 2404, 498]` -> `[2184, 304, 2430, 506]`.
  - old `#27` -> new `#13` `text_block`: `[199, 583, 1036, 780]` -> `[35, 530, 455, 775]`.
  - old `#33` -> new `#14` `text_block`: `[199, 840, 1036, 1070]` -> `[35, 795, 455, 1072]`.
  - old `#39` -> new `#15` `text_block`: `[199, 1130, 1036, 1359]` -> `[35, 1100, 455, 1368]`.
  - old `#47` -> new `#16` `title`: `[1179, 583, 1982, 621]` -> `[500, 530, 1200, 580]`.
  - old `#48` -> new `#17` `text_block`: `[1950, 383, 2094, 449]` -> `[1665, 545, 1890, 570]`.
  - old `#45` -> new `#18` `figure`: `[1179, 1624, 2464, 1660]` -> `[520, 640, 1890, 1605]`.
  - old `#49` -> new `#19` `text_block`: `[1207, 1631, 2464, 1653]` -> `[500, 1625, 1325, 1660]`.
  - old `#57` -> new `#20` `text_block`: `[2019, 719, 2393, 744]` -> `[1966, 532, 2432, 742]`.
  - old `#63` -> new `#21` `text_block`: `[2011, 906, 2378, 962]` -> `[1966, 790, 2432, 1034]`.
  - old `#69` -> new `#22` `text_block`: `[2019, 1234, 2357, 1291]` -> `[1966, 1080, 2432, 1290]`.
  - old `#78` -> new `#23` `title`: `[199, 1718, 758, 1756]` -> `[35, 1708, 620, 1750]`.
  - old `#79` -> new `#24` `text_block`: `[2106, 1727, 2464, 1746]` -> `[920, 1726, 1414, 1748]`.
  - old `#80` -> new `#25` `figure`: `[199, 1779, 2464, 1915]` -> `[55, 1760, 1415, 1915]`.
  - old `#94` -> new `#26` `title`: `[1491, 1718, 1703, 1756]` -> `[1465, 1708, 1800, 1750]`.
  - old `#95` -> new `#27` `text_block`: `[2284, 3759, 2409, 3778]` -> `[2280, 1728, 2410, 1750]`.
  - old `#96` -> new `#28` `equation_isolated`: `[1507, 1800, 1986, 1830]` -> `[1476, 1788, 2408, 1868]`.
  - old `#97` -> new `#29` `equation_isolated`: `[1507, 1913, 2026, 1943]` -> `[1476, 1900, 2408, 1978]`.
  - old `#98` -> new `#30` `equation_isolated`: `[1507, 2026, 2080, 2056]` -> `[1476, 2012, 2408, 2090]`.
  - old `#101` -> new `#31` `title`: `[1476, 2154, 1731, 2195]` -> `[1476, 2148, 1800, 2190]`.
  - old `#102` -> new `#32` `text_block`: `[1632, 3759, 1848, 3778]` -> `[2250, 2162, 2408, 2188]`.
  - old `#99` -> new `#33` `table`: `[1486, 2161, 2409, 2459]` -> `[1476, 2212, 2408, 2462]`.
  - old `#125` -> new `#34` `text_block`: `[199, 2520, 2464, 2544]` -> `[35, 2518, 2300, 2560]`.
  - old `#127` -> new `#35` `header`: `[199, 2577, 1474, 2599]` -> `[35, 2578, 900, 2602]`.
  - old `#128` -> new `#36` `header`: `[1891, 2578, 2409, 2600]` -> `[1880, 2578, 2410, 2602]`.
  - old `#132` -> new `#37` `text_block`: `[0, 2809, 979, 2822]` -> `[35, 2710, 330, 2735]`.
  - old `#133` -> new `#38` `text_block`: `[863, 2713, 1182, 2735]` -> `[343, 2705, 515, 2740]`.
  - old `#134` -> new `#39` `text_block`: `[1275, 2713, 1761, 2735]` -> `[530, 2705, 775, 2740]`.
  - old `#136` -> new `#40` `text_block`: `[104, 4430, 331, 4476]` -> `[2020, 2705, 2295, 2740]`.
  - old `#137` -> new `#41` `page_number`: `[88, 583, 461, 622]` -> `[2310, 2710, 2425, 2735]`.
  - old `#140` -> new `#42` `title`: `[152, 2755, 2464, 2845]` -> `[35, 2775, 1360, 2845]`.
  - old `#141` -> new `#43` `text_block`: `[152, 2850, 1393, 2889]` -> `[35, 2860, 680, 2908]`.
  - old `#142` -> new `#44` `text_block`: `[152, 2907, 2464, 2969]` -> `[35, 2925, 1345, 2988]`.
  - old `#144` -> new `#45` `text_block`: `[1271, 4365, 1514, 4476]` -> `[1422, 2770, 1662, 2942]`.
  - old `#146` -> new `#46` `text_block`: `[1271, 4430, 1514, 4476]` -> `[1678, 2770, 1920, 2942]`.
  - old `#148` -> new `#47` `text_block`: `[1944, 2876, 2077, 2898]` -> `[1934, 2770, 2176, 2942]`.
  - old `#150` -> new `#48` `text_block`: `[2200, 2876, 2276, 2898]` -> `[2190, 2770, 2430, 2942]`.
  - old `#155` -> new `#49` `title`: `[199, 3015, 1090, 3054]` -> `[55, 3020, 700, 3060]`.
  - old `#156` -> new `#50` `text_block`: `None` -> `[1165, 3024, 1365, 3048]`.
  - old `#157` -> new `#51` `table`: `[199, 3015, 2464, 3691]` -> `[55, 3080, 1365, 3520]`.
  - old `#209` -> new `#52` `title`: `[2185, 3829, 2331, 3859]` -> `[1428, 3020, 1710, 3060]`.
  - old `#210` -> new `#53` `text_block`: `None` -> `[2290, 3028, 2405, 3050]`.
  - old `#211` -> new `#54` `text_block`: `None` -> `[1428, 3100, 2385, 3225]`.
  - old `#213` -> new `#55` `title`: `[1444, 3224, 1652, 3263]` -> `[1428, 3272, 1710, 3315]`.
  - old `#214` -> new `#56` `text_block`: `None` -> `[2290, 3282, 2405, 3305]`.
  - old `#218` -> new `#57` `title`: `[199, 3749, 1188, 3787]` -> `[55, 3745, 900, 3788]`.
  - old `#219` -> new `#58` `text_block`: `None` -> `[1620, 3760, 1840, 3785]`.
  - old `#220` -> new `#59` `table`: `[199, 3810, 2464, 4149]` -> `[55, 3830, 1840, 4140]`.
  - old `#237` -> new `#60` `text_block`: `[239, 4186, 2464, 4211]` -> `[55, 4170, 1840, 4230]`.
  - old `#240` -> new `#61` `title`: `[1912, 3749, 2193, 3787]` -> `[1905, 3745, 2225, 3788]`.
  - old `#241` -> new `#62` `text_block`: `None` -> `[2280, 3760, 2408, 3785]`.
  - old `#243` -> new `#63` `text_block`: `None` -> `[1905, 3830, 2150, 4065]`.
  - old `#246` -> new `#64` `text_block`: `None` -> `[2165, 3830, 2410, 4065]`.
  - old `#249` -> new `#65` `text_block`: `None` -> `[1905, 4090, 2150, 4315]`.
  - old `#252` -> new `#66` `text_block`: `None` -> `[2165, 4090, 2410, 4315]`.
  - old `#257` -> new `#67` `title`: `[199, 4287, 820, 4326]` -> `[55, 4285, 550, 4328]`.
  - old `#258` -> new `#68` `text_block`: `None` -> `[2240, 4298, 2408, 4325]`.
  - old `#260` -> new `#69` `text_block`: `[233, 4364, 789, 4478]` -> `[55, 4365, 337, 4510]`.
  - old `#262` -> new `#70` `text_block`: `[1544, 4364, 2100, 4478]` -> `[648, 4365, 930, 4510]`.
  - old `#264` -> new `#71` `text_block`: `None` -> `[1240, 4365, 1522, 4510]`.
  - old `#266` -> new `#72` `text_block`: `None` -> `[1830, 4365, 2112, 4510]`.
  - old `#269` -> new `#73` `text_block`: `[199, 4568, 2464, 4593]` -> `[35, 4560, 2300, 4598]`.
  - old `#271` -> new `#74` `text_block`: `[199, 4626, 1470, 4648]` -> `[35, 4625, 900, 4652]`.
  - old `#272` -> new `#75` `header`: `None` -> `[1845, 4625, 2385, 4652]`.

Bbox additions to retained no-bbox GT annotations:

- Added bbox to old `#156/#210/#211/#214/#219/#241/#243/#246/#249/#252/#258/#264/#266/#272`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `113`.
- Added bbox to existing GT annotations: `14`.
- Cleared existing bbox values: `0`.
- Category/type changes in this pass: `2`.
- Non-bbox semantic changes recorded in this pass: `191` (`113` deletions + `76` order/id changes + `2` category/type changes).

Verification:

- Report with full removed-item, order-change, category-change, and bbox-change details: `reports/pdb_education_slides030_urban_resilience_relabel_v612.json`.
- Visual scout cover check directory: `cover_audit_education_slides030031_current_scout/`.
- Visual dry-run cover check directory: `cover_audit_education_slides030_urban_resilience_relabel_v612_dry/`.
- Visual dry-run outline check directory: `outline_audit_education_slides030_urban_resilience_relabel_v612_dry/`.
- Visual cover check directory: `cover_audit_education_slides030_urban_resilience_relabel_v612/`.
- Non-cover outline preview directory: `outline_audit_education_slides030_urban_resilience_relabel_v612/`.
- Formal outline inspected: `outline_audit_education_slides030_urban_resilience_relabel_v612/slides_030_Smart_Urban_Resilience_2in1_outline.jpg`; page 1/2 reading order, table boxes, figure boxes, risk cards, and timeline cards were visually checked.
- Static validation at write time: final run reports `removed_annotations=113`, `added_annotations=0`, `bbox_changes=76`, `order_changes=76`, `bbox_added_to_existing=14`, `category_changes=2`, and `non_bbox_semantic_changes=191`.
- Frontend/cache validation: opened `http://127.0.0.1:8767/index.html?cb=20260611_education_slides030_urban_resilience_relabel_v612`, selected case `242. 02_education/03_slides/slides_030_Smart_Urban_Resilience_2in1`; visible data label showed `data 20260611_education_slides030_urban_resilience_relabel_v612`, active row showed `76/76 boxed · 0 no bbox`, page image was `02_education/03_slides/slides_030_Smart_Urban_Resilience_2in1.png` with natural size `2464x4722`, and overlay rendered `76` labels continuing through `#75`.
- Latest token after this repair: `20260611_education_slides030_urban_resilience_relabel_v612`.

## 20260611_education_slides030_multimodal_doc_relabel_v613

Scope:

- Case: `02_education/03_slides/slides_030_多模态文档智能系统_上下伪两页科研汇报`.
- User-visible row: `243. 02_education/03_slides/slides_030_多模态文档智能系统_上下伪两页科研汇报`.
- Reason: user flagged the next slides case as completely disordered. Visual review showed page wrappers, wrong-page drift, many no-bbox residues, table/cell duplicates, bar-chart label fragments, and card-label fragments after whole table/chart/card regions were already available.

Files updated:

- `review_data.json`
- `review_data.js`
- `index.html` cache/query token
- `GT_REPAIR_LOG.md`

Token and status:

- Previous token: `20260611_education_slides030_urban_resilience_relabel_v612`.
- v613: `20260611_education_slides030_multimodal_doc_relabel_v613`.
- `slides_030_多模态文档智能系统_上下伪两页科研汇报`: final status `32/32 boxed`, `0 no bbox`, `0 low-similarity`.
- Visual reading order is now continuous `#0-#31`.

Removed duplicated/drifted GT annotations:

- Deleted old `#0-#2`, `#6-#9`, `#11-#15`, `#18-#46`, `#48-#60`, `#89-#101`, `#103-#104`, `#106-#107`, `#111-#121`, `#184`, `#203-#221`, `#223`, `#225-#229`, `#231-#235`, `#237-#241`, `#243-#248`, `#252-#254`.
- Total removed GT annotations in this pass: `127`.

Annotation order/id changes:

- Retained annotations were renumbered to continuous visual reading order.
- Page 1 title/header/architecture/right panels: old `#3/#4/#5/#10/#16/#17/#47/#61/#62/#87/#88/#102/#105` -> new `#0-#12`.
- Page 2 title/status/main table/ablation/chart/cards/footer: old `#108/#109/#110/#122/#123/#183/#185/#186/#201/#202/#222/#224/#230/#236/#242/#249/#250/#251/#255` -> new `#13-#31`.
- Total order/id changes recorded: `32`.

Category/type changes:

- old `#17` -> new `#5`: `text_block` -> `figure`, bbox `[50, 260, 1455, 910]`, for the full System Architecture Overview diagram.
- old `#202` -> new `#22`: `text_block` -> `figure`, bbox `[1605, 1570, 2320, 1678]`, for the Latency vs Quality bar-chart figure.

Case-level bbox changes:

- `slides_030_多模态文档智能系统_上下伪两页科研汇报`: `32` retained bboxes changed/reset. Old indices below refer to the pre-v613 ids.
  - old `#3` -> new `#0` `title`: `[285, 78, 2380, 144]` -> `[70, 66, 1585, 122]`.
  - old `#4` -> new `#1` `title`: `[285, 145, 2380, 173]` -> `[70, 128, 1125, 158]`.
  - old `#5` -> new `#2` `text_block`: `[2146, 182, 2318, 198]` -> `[2125, 45, 2325, 170]`.
  - old `#10` -> new `#3` `header`: `[261, 222, 2380, 239]` -> `[50, 180, 2325, 210]`.
  - old `#16` -> new `#4` `text_block`: `[267, 268, 1435, 293]` -> `[65, 228, 585, 260]`.
  - old `#17` -> new `#5` `text_block`: `[270, 302, 2380, 946]` -> `[50, 260, 1455, 910]`.
  - old `#47` -> new `#6` `text_block`: `[1926, 900, 2309, 914]` -> `[1470, 225, 2325, 470]`.
  - old `#61` -> new `#7` `text_block`: `[1607, 742, 1667, 758]` -> `[1470, 490, 1960, 520]`.
  - old `#62` -> new `#8` `table`: `[1478, 557, 2315, 704]` -> `[1475, 528, 2318, 650]`.
  - old `#87` -> new `#9` `title`: `[1490, 736, 1667, 760]` -> `[1470, 675, 1700, 705]`.
  - old `#88` -> new `#10` `text_block`: `[1512, 1233, 1568, 1249]` -> `[1475, 710, 2320, 830]`.
  - old `#102` -> new `#11` `text_block`: `[2258, 1298, 2320, 1313]` -> `[1475, 838, 2320, 890]`.
  - old `#105` -> new `#12` `header`: `[1997, 2192, 2331, 2207]` -> `[2055, 1048, 2325, 1072]`.
  - old `#108` -> new `#13` `title`: `[273, 1238, 2380, 1294]` -> `[70, 1185, 790, 1244]`.
  - old `#109` -> new `#14` `text_block`: `[273, 1293, 1613, 1315]` -> `[70, 1250, 760, 1275]`.
  - old `#110` -> new `#15` `header`: `None` -> `[1482, 1190, 2325, 1274]`.
  - old `#122` -> new `#16` `text_block`: `[261, 1366, 1470, 1391]` -> `[65, 1348, 610, 1384]`.
  - old `#123` -> new `#17` `table`: `[261, 1398, 2380, 1637]` -> `[70, 1395, 1585, 1638]`.
  - old `#183` -> new `#18` `text_block`: `[261, 1645, 2203, 1655]` -> `[70, 1648, 1210, 1662]`.
  - old `#185` -> new `#19` `title`: `[1602, 1366, 1789, 1391]` -> `[1600, 1348, 1910, 1384]`.
  - old `#186` -> new `#20` `table`: `[1602, 1399, 2317, 1512]` -> `[1610, 1395, 2320, 1515]`.
  - old `#201` -> new `#21` `title`: `[1598, 1548, 1867, 1573]` -> `[1600, 1530, 1920, 1568]`.
  - old `#202` -> new `#22` `text_block`: `None` -> `[1605, 1570, 2320, 1678]`.
  - old `#222` -> new `#23` `text_block`: `[261, 1739, 1637, 1764]` -> `[65, 1718, 720, 1755]`.
  - old `#224` -> new `#24` `text_block`: `[282, 1780, 1911, 1945]` -> `[78, 1770, 628, 1932]`.
  - old `#230` -> new `#25` `text_block`: `[1977, 1780, 2380, 1945]` -> `[635, 1770, 1197, 1932]`.
  - old `#236` -> new `#26` `text_block`: `None` -> `[1205, 1770, 1763, 1932]`.
  - old `#242` -> new `#27` `text_block`: `None` -> `[1770, 1770, 2322, 1932]`.
  - old `#249` -> new `#28` `text_block`: `[294, 1971, 967, 1993]` -> `[80, 1960, 620, 1990]`.
  - old `#250` -> new `#29` `text_block`: `[294, 1971, 2380, 2013]` -> `[80, 1992, 2280, 2015]`.
  - old `#251` -> new `#30` `text_block`: `[222, 2048, 2380, 2076]` -> `[65, 2050, 2310, 2072]`.
  - old `#255` -> new `#31` `header`: `None` -> `[2045, 2182, 2325, 2205]`.

Bbox additions to retained no-bbox GT annotations:

- Added bbox to old `#110/#202/#236/#242/#255`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `127`.
- Added bbox to existing GT annotations: `5`.
- Cleared existing bbox values: `0`.
- Category/type changes in this pass: `2`.
- Non-bbox semantic changes recorded in this pass: `161` (`127` deletions + `32` order/id changes + `2` category/type changes).

Verification:

- Report with full removed-item, order-change, category-change, and bbox-change details: `reports/pdb_education_slides030_multimodal_doc_relabel_v613.json`.
- Visual dry-run cover check directories: `cover_audit_education_slides030_multimodal_doc_relabel_v613_dry/`, `cover_audit_education_slides030_multimodal_doc_relabel_v613_dry2/`.
- Visual dry-run outline check directories: `outline_audit_education_slides030_multimodal_doc_relabel_v613_dry/`, `outline_audit_education_slides030_multimodal_doc_relabel_v613_dry2/`.
- Visual cover check directory: `cover_audit_education_slides030_multimodal_doc_relabel_v613/`.
- Non-cover outline preview directory: `outline_audit_education_slides030_multimodal_doc_relabel_v613/`.
- Formal outline inspected: `outline_audit_education_slides030_multimodal_doc_relabel_v613/slides_030_多模态文档智能系统_上下伪两页科研汇报_outline.jpg`; dry-run outline v613_dry2 was inspected before final write, with the second-page English title tightened before the official v613 write.
- Static validation at write time: final run reports `removed_annotations=127`, `added_annotations=0`, `bbox_changes=32`, `order_changes=32`, `bbox_added_to_existing=5`, `category_changes=2`, and `non_bbox_semantic_changes=161`.
- Frontend/cache validation: opened `http://127.0.0.1:8767/index.html?cb=20260611_education_slides030_multimodal_doc_relabel_v613`, selected case `243. 02_education/03_slides/slides_030_多模态文档智能系统_上下伪两页科研汇报`; visible data label showed `data 20260611_education_slides030_multimodal_doc_relabel_v613`, active row showed `32/32 boxed · 0 no bbox`, page image was `02_education/03_slides/slides_030_多模态文档智能系统_上下伪两页科研汇报.png` with natural size `2380x2270`, and overlay rendered `32` labels continuing through `#31`.
- Latest token after this repair: `20260611_education_slides030_multimodal_doc_relabel_v613`.

## 20260611_education_slides031_autonomous_relabel_v614

Scope:

- Case: `02_education/03_slides/slides_031_Autonomous_Research_Operations_2in1`.
- User-visible row: `244. 02_education/03_slides/slides_031_Autonomous_Research_Operations_2in1`.
- Reason: user flagged the adjacent slides case as broadly disordered. Visual review showed full-page wrappers, KPI/card fragments, table-cell fragments, risk-card residues, no-bbox lower-page notes, and many old bboxes drifting between the two stacked slide pages.

Files updated:

- `review_data.json`
- `review_data.js`
- `index.html` cache/query token
- `GT_REPAIR_LOG.md`

Token and status:

- Previous token: `20260611_education_slides030_multimodal_doc_relabel_v613`.
- v614: `20260611_education_slides031_autonomous_relabel_v614`.
- `slides_031_Autonomous_Research_Operations_2in1`: final status `37/37 boxed`, `0 no bbox`, `0 low-similarity`.
- Visual reading order is now continuous `#0-#36`.

Removed duplicated/drifted GT annotations:

- Deleted old `#0-#3`, `#5-#14`, `#19-#26`, `#28-#29`, `#31-#41`, `#43`, `#45-#52`, `#54-#61`, `#63`, `#93-#95`, `#97`, `#99-#108`, `#110-#111`, `#113-#116`, `#118`, `#137-#141`, `#143-#151`, `#153-#154`, `#156-#163`, `#165-#167`, `#169`, `#221-#223`, `#225`, `#240-#241`, `#243`, `#245-#259`, `#261-#262`, `#264-#283`, `#285`, `#288`, `#290-#302`, `#304-#307`, `#309-#312`.
- Total removed GT annotations in this pass: `169`.

Annotation order/id changes:

- Retained annotations were renumbered to continuous visual reading order.
- Page 1 overview/control/topology/right-panel/workflow/footer: old `#4/#15/#16/#17/#18/#30/#27/#42/#44/#53/#62/#64/#96/#98/#112/#109/#117/#119/#136` -> new `#0-#18`.
- Page 2 analytics header/cards/data/risk/responsibility/cases/narrative/timeline/footer: old `#142/#152/#155/#168/#170/#164/#263/#260/#224/#226/#242/#244/#284/#286/#289/#287/#303/#308` -> new `#19-#36`.
- Total order/id changes recorded: `37`.

Category/type changes:

- old `#27` -> new `#6`: `text_block` -> `figure`, bbox `[35, 565, 1950, 1735]`, for the Main Control Topology diagram.
- old `#44` -> new `#8`: `text_block` -> `figure`, bbox `[1985, 565, 2438, 1195]`, for the KPI Rings dashboard.
- old `#98` -> new `#13`: `text_block` -> `figure`, bbox `[35, 2660, 1415, 3060]`, for the Research Workflow Strip.
- old `#164` -> new `#24`: `text_block` -> `figure`, bbox `[55, 4290, 1265, 4488]`, for the Data Asset trend chart below the table.
- old `#244` -> new `#30`: `text_block` -> `figure`, bbox `[670, 4610, 1270, 4995]`, for the Case Thumbnails card group.
- old `#287` -> new `#34`: `text_block` -> `figure`, bbox `[35, 5110, 2428, 5365]`, for the Execution Timeline.

Case-level bbox changes:

- `slides_031_Autonomous_Research_Operations_2in1`: `37` retained bboxes changed/reset. Old indices below refer to the pre-v614 ids.
  - old `#4` -> new `#0` `header`: `[146, 60, 2464, 97]` -> `[30, 25, 2428, 58]`.
  - old `#15` -> new `#1` `title`: `[146, 103, 2464, 200]` -> `[30, 75, 1510, 150]`.
  - old `#16` -> new `#2` `text_block`: `[146, 206, 2132, 243]` -> `[30, 174, 1350, 210]`.
  - old `#17` -> new `#3` `text_block`: `[146, 264, 2464, 326]` -> `[30, 245, 1760, 318]`.
  - old `#18` -> new `#4` `text_block`: `[2192, 219, 2370, 271]` -> `[1900, 80, 2428, 460]`.
  - old `#30` -> new `#5` `title`: `[192, 527, 869, 564]` -> `[35, 515, 850, 565]`.
  - old `#27` -> new `#6` `text_block`: `[2133, 723, 2231, 834]` -> `[35, 565, 1950, 1735]`.
  - old `#42` -> new `#7` `title`: `[1990, 527, 2118, 564]` -> `[1985, 515, 2155, 565]`.
  - old `#44` -> new `#8` `text_block`: `[2133, 601, 2243, 834]` -> `[1985, 565, 2438, 1195]`.
  - old `#53` -> new `#9` `text_block`: `[1998, 1338, 2378, 1706]` -> `[1985, 1220, 2438, 1815]`.
  - old `#62` -> new `#10` `title`: `[1982, 1821, 2149, 1965]` -> `[1985, 1840, 2280, 1910]`.
  - old `#64` -> new `#11` `table`: `[52, 1988, 2412, 2617]` -> `[1995, 1925, 2428, 2570]`.
  - old `#96` -> new `#12` `title`: `[192, 2651, 928, 2688]` -> `[35, 2600, 1100, 2655]`.
  - old `#98` -> new `#13` `text_block`: `[192, 2711, 2464, 2834]` -> `[35, 2660, 1415, 3060]`.
  - old `#112` -> new `#14` `title`: `[1445, 2651, 1647, 2688]` -> `[1445, 2600, 1700, 2655]`.
  - old `#109` -> new `#15` `text_block`: `[1445, 2712, 2387, 2761]` -> `[1445, 2660, 2428, 2860]`.
  - old `#117` -> new `#16` `title`: `[1445, 2816, 1661, 2853]` -> `[1445, 2900, 1700, 2960]`.
  - old `#119` -> new `#17` `table`: `[1445, 2876, 2411, 3063]` -> `[1445, 2970, 2428, 3150]`.
  - old `#136` -> new `#18` `header`: `[192, 3135, 2464, 3213]` -> `[35, 3185, 2428, 3268]`.
  - old `#142` -> new `#19` `header`: `[146, 3316, 2464, 3353]` -> `[35, 3330, 2430, 3375]`.
  - old `#152` -> new `#20` `header`: `[199, 3386, 1210, 3734]` -> `[35, 3410, 540, 3825]`.
  - old `#155` -> new `#21` `text_block`: `[1313, 3374, 2464, 3521]` -> `[560, 3410, 2430, 3575]`.
  - old `#168` -> new `#22` `title`: `[192, 3796, 699, 3833]` -> `[35, 3770, 850, 3825]`.
  - old `#170` -> new `#23` `table`: `[192, 3856, 2464, 4282]` -> `[55, 3860, 1265, 4275]`.
  - old `#164` -> new `#24` `text_block`: `[146, 3779, 2464, 5050]` -> `[55, 4290, 1265, 4488]`.
  - old `#263` -> new `#25` `title`: `[86, 5089, 336, 5126]` -> `[1305, 3770, 1650, 3825]`.
  - old `#260` -> new `#26` `text_block`: `None` -> `[1305, 3860, 2428, 4495]`.
  - old `#224` -> new `#27` `title`: `[192, 4511, 814, 4549]` -> `[35, 4525, 700, 4580]`.
  - old `#226` -> new `#28` `table`: `[192, 4571, 1444, 4807]` -> `[55, 4610, 625, 4835]`.
  - old `#242` -> new `#29` `title`: `[1587, 4511, 2096, 4549]` -> `[660, 4525, 1080, 4580]`.
  - old `#244` -> new `#30` `text_block`: `[1587, 4571, 2464, 5033]` -> `[670, 4610, 1270, 4995]`.
  - old `#284` -> new `#31` `title`: `[938, 4609, 1550, 4650]` -> `[1305, 4525, 1700, 4580]`.
  - old `#286` -> new `#32` `text_block`: `None` -> `[1305, 4605, 2428, 4995]`.
  - old `#289` -> new `#33` `title`: `[192, 5089, 755, 5126]` -> `[35, 5040, 750, 5100]`.
  - old `#287` -> new `#34` `text_block`: `[192, 5089, 2464, 5322]` -> `[35, 5110, 2428, 5365]`.
  - old `#303` -> new `#35` `header`: `[192, 5410, 2464, 5513]` -> `[35, 5410, 1460, 5550]`.
  - old `#308` -> new `#36` `text_block`: `None` -> `[1480, 5410, 2428, 5550]`.

Bbox additions to retained no-bbox GT annotations:

- Added bbox to old `#260/#286/#308`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `169`.
- Added bbox to existing GT annotations: `3`.
- Cleared existing bbox values: `0`.
- Category/type changes in this pass: `6`.
- Non-bbox semantic changes recorded in this pass: `212` (`169` deletions + `37` order/id changes + `6` category/type changes).

Verification:

- Report with full removed-item, order-change, category-change, and bbox-change details: `reports/pdb_education_slides031_autonomous_relabel_v614.json`.
- Visual dry-run cover check directory: `cover_audit_education_slides031_autonomous_relabel_v614_dry/`.
- Visual dry-run outline check directory: `outline_audit_education_slides031_autonomous_relabel_v614_dry/`.
- Visual cover check directory: `cover_audit_education_slides031_autonomous_relabel_v614/`.
- Non-cover outline preview directory: `outline_audit_education_slides031_autonomous_relabel_v614/`.
- Formal outline inspected: `outline_audit_education_slides031_autonomous_relabel_v614/slides_031_Autonomous_Research_Operations_2in1_outline.jpg`; dry-run outline was inspected before final write for both stacked slide pages, including top KPI cards, right-side formula/table panels, workflow/table sections, page 2 data/risk/case/narrative blocks, and bottom timeline/footnotes.
- Static validation at write time: final run reports `removed_annotations=169`, `added_annotations=0`, `bbox_changes=37`, `order_changes=37`, `bbox_added_to_existing=3`, `category_changes=6`, and `non_bbox_semantic_changes=212`.
- Frontend/cache validation: opened `http://127.0.0.1:8767/index.html?cb=20260611_education_slides031_autonomous_relabel_v614`, selected case `244. 02_education/03_slides/slides_031_Autonomous_Research_Operations_2in1`; visible data label showed `data 20260611_education_slides031_autonomous_relabel_v614`, active row showed `37/37 boxed · 0 no bbox`, page image was `02_education/03_slides/slides_031_Autonomous_Research_Operations_2in1.png` with natural size `2464x5611`, and overlay rendered `37` labels continuing through `#36`.
- Latest token after this repair: `20260611_education_slides031_autonomous_relabel_v614`.

## 20260611_education_school_notice002_formula_v615

Scope:

- Case: `02_education/04_school_notice/school_notice_002_联合通知_课程调整交换综合测评`.
- User-visible row: `246. 02_education/04_school_notice/school_notice_002_联合通知_课程调整交换综合测评`.
- Reason: user flagged multiple formulas in Appendix 3 as visually non-standard/misaligned. Visual review of the clean PNG showed formula rows `#61/#64/#66/#68` should be full-row isolated equations including right-side equation tags, while `#66` incorrectly covered the entire appendix panel and `#71` had drifted to the upper page.

Files updated:

- `review_data.json`
- `review_data.js`
- `index.html` cache/query token
- `GT_REPAIR_LOG.md`

Token and status:

- Previous token: `20260611_education_slides031_autonomous_relabel_v614`.
- v615: `20260611_education_school_notice002_formula_v615`.
- `school_notice_002_联合通知_课程调整交换综合测评`: final status `92/92 boxed`, `0 no bbox`, `15 low-similarity`.
- Low-similarity count changed from `20` to `15` after clearing the repaired formula/reference matches.

Case-level bbox changes:

- `#61` `equation_isolated`: `[835, 3637, 1646, 3688]` -> `[665, 3655, 2320, 3716]`; standardized formula `(1)` to the full visible formula row including the right-side tag.
- `#64` `equation_isolated`: `[654, 3804, 1827, 3847]` -> `[495, 3796, 2320, 3855]`; standardized formula `(2)` to the full visible formula row including the right-side tag.
- `#66` `equation_isolated`: `[153, 3520, 2328, 4446]` -> `[448, 3892, 2320, 3952]`; fixed the oversized panel-level bbox to just the `Score_exchange` formula `(3)`.
- `#68` `equation_isolated`: `[643, 4101, 2318, 4203]` -> `[415, 4014, 2320, 4073]`; standardized formula `(4)` to the full visible formula row including the right-side tag.
- `#70` `reference`: `[645, 4077, 2331, 4122]` -> `[620, 4070, 1845, 4124]`; tightened note `(1)` to its visible text run under the formulas.
- `#71` `reference`: `[1682, 646, 1817, 693]` -> `[1780, 4070, 2318, 4168]`; moved drifted note `(2)` back to the Appendix 3 explanation line.
- `#72` `reference`: `[165, 4117, 2317, 4170]` -> `[930, 4120, 1645, 4172]`; tightened note `(3)` to its visible text run.
- `#73` `reference`: `[645, 4152, 1165, 4198]` -> `[1618, 4120, 2318, 4202]`; moved note `(4)` to the right-side wrapped explanation text.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0`.
- Cleared existing bbox values: `0`.
- Category/type changes in this pass: `0`.
- Order/id changes in this pass: `0`.
- Non-bbox semantic changes recorded in this pass: `0`.

Verification:

- Script: `scripts/fix_education_school_notice002_formula_v615.py`.
- Report: `reports/pdb_education_school_notice002_formula_v615.json`.
- Visual dry-run cover check directory: `cover_audit_education_school_notice002_formula_v615_dry2/`.
- Visual dry-run outline check directory: `outline_audit_education_school_notice002_formula_v615_dry2/`.
- Visual cover check directory: `cover_audit_education_school_notice002_formula_v615/`.
- Non-cover outline preview directory: `outline_audit_education_school_notice002_formula_v615/`.
- Formal outline inspected: `outline_audit_education_school_notice002_formula_v615/school_notice_002_联合通知_课程调整交换综合测评_outline.jpg`; dry-run outline/cover crops were inspected before final write to confirm four formulas align with the visible equation rows and `#71` no longer drifts to the page top.
- Static validation at write time: final run reports `changed_annotations=8`, `added_annotations=0`, `removed_annotations=0`, `bbox_added_to_existing=0`, `category_changes=0`, `order_changes=0`, and `non_bbox_semantic_changes=0`.
- Frontend/cache validation: opened `http://127.0.0.1:8767/index.html?cb=20260611_education_school_notice002_formula_v615&case=02_education%2F04_school_notice%2Fschool_notice_002_%E8%81%94%E5%90%88%E9%80%9A%E7%9F%A5_%E8%AF%BE%E7%A8%8B%E8%B0%83%E6%95%B4%E4%BA%A4%E6%8D%A2%E7%BB%BC%E5%90%88%E6%B5%8B%E8%AF%84`; visible data label showed `data 20260611_education_school_notice002_formula_v615`, active title showed `246. 02_education/04_school_notice/school_notice_002_联合通知_课程调整交换综合测评`, page image was `02_education/04_school_notice/school_notice_002_联合通知_课程调整交换综合测评.png` with natural size `2481x5200`, overlay rendered `92` boxes/labels, and the repaired ids `#61/#64/#66/#68/#70/#71/#72/#73` were present at their v615 coordinates.
- Latest token after this repair: `20260611_education_school_notice002_formula_v615`.

## 20260612_education_school_notice_slides_batch_v616

Scope:

- Cases:
  - `02_education/04_school_notice/school_notice_006_大学课程表_复杂`.
  - `02_education/04_school_notice/school_notice_005_实验室安全整改联合通知`.
  - `02_education/04_school_notice/school_notice_016_文化艺术节场地管理通知_ZHCN`.
  - `02_education/03_slides/slides_029_产品发布_手机`.
- Reason: user flagged `school_notice_006` as missing the visible timetable GT box, `slides_029` as having an old `#0` wrapper occupying almost the whole slide, and `school_notice_005` / `school_notice_016` as visibly offset with lower-page labels floating into upper sections.

Files updated:

- `review_data.json`
- `review_data.js`
- `index.html` cache/query token
- `GT_REPAIR_LOG.md`

Token and status:

- Previous token: `20260611_education_school_notice002_formula_v615`.
- v616: `20260612_education_school_notice_slides_batch_v616`.
- `school_notice_006_大学课程表_复杂`: final status `11/11 boxed`, `0 no bbox`, `0 low-similarity`.
- `school_notice_005_实验室安全整改联合通知`: final status `94/94 boxed`, `0 no bbox`, `0 low-similarity`.
- `school_notice_016_文化艺术节场地管理通知_ZHCN`: final status `71/71 boxed`, `0 no bbox`, `0 low-similarity`.
- `slides_029_产品发布_手机`: final status `44/44 boxed`, `0 no bbox`, `0 low-similarity`.

Case-level bbox changes:

- `school_notice_006_大学课程表_复杂`:
  - `#8` `table`: `None` -> `[45, 385, 2425, 3335]`; added the full visible course timetable bbox.
  - `#9` `reference`: `[98, 311, 2348, 355]` -> `[50, 3335, 820, 3395]`; moved the legend/reference line from the student-info strip to the bottom legend area.

- `school_notice_005_实验室安全整改联合通知`:
  - `#7` `title`: `[691, 247, 1790, 312]` -> `[110, 690, 455, 745]`.
  - `#35` `title`: `None` -> `[895, 1832, 1320, 1888]`.
  - `#36` `title`: `[896, 1826, 1181, 1881]` -> `[930, 1900, 1210, 1950]`.
  - `#50` `title`: `None` -> `[1745, 1832, 2205, 1888]`.
  - `#51` `text_block`: `[1770, 2025, 2314, 2088]` -> `[1770, 1900, 2370, 2002]`.
  - `#52` `text_block`: `[1770, 2127, 2342, 2189]` -> `[1770, 2020, 2370, 2118]`.
  - `#53` `text_block`: `[1770, 2228, 2313, 2291]` -> `[1770, 2138, 2370, 2235]`.
  - `#54` `text_block`: `[1770, 2330, 2335, 2392]` -> `[1770, 2258, 2370, 2355]`.
  - `#55` `text_block`: `[1770, 2431, 2347, 2494]` -> `[1770, 2375, 2370, 2480]`.
  - `#56` `text_block`: `[1770, 2533, 2339, 2596]` -> `[1770, 2492, 2370, 2588]`.
  - `#64` `equation_isolated`: `[843, 3823, 1638, 3867]` -> `[770, 3465, 2340, 3525]`.
  - `#66` `equation_isolated`: `[843, 3823, 1638, 3867]` -> `[835, 3565, 2340, 3630]`.
  - `#68` `equation_isolated`: `[892, 3921, 1589, 3965]` -> `[875, 3655, 2340, 3720]`.
  - `#70` `equation_isolated`: `None` -> `[740, 3748, 2340, 3885]`.
  - `#71` `table`: `[118, 4161, 1825, 4493]` -> `[120, 3900, 535, 4210]`.
  - `#72` `reference`: `[525, 4157, 2331, 4252]` -> `[545, 3900, 1735, 3948]`.
  - `#73` `reference`: `[707, 377, 1774, 446]` -> `[1735, 3900, 2340, 3995]`.
  - `#74` `reference`: `[144, 3925, 2338, 3991]` -> `[545, 3942, 2050, 3998]`.
  - `#75` `reference`: `[144, 631, 372, 663]` -> `[2050, 3942, 2340, 3998]`.
  - `#78` `title`: `[110, 4331, 1463, 4363]` -> `[110, 4335, 430, 4372]`.
  - `#79` `text_block`: `[436, 622, 689, 666]` -> `[110, 4370, 710, 4405]`.
  - `#80` `text_block`: `[721, 631, 1062, 663]` -> `[110, 4405, 875, 4440]`.
  - `#81` `text_block`: `[112, 1556, 502, 1606]` -> `[110, 4440, 780, 4475]`.
  - `#82` `text_block`: `[1126, 622, 1411, 666]` -> `[110, 4475, 780, 4510]`.
  - `#85` `title`: `[1245, 4330, 1464, 4366]` -> `[1245, 4335, 1510, 4372]`.
  - `#86` `text_block`: `[1380, 1413, 1578, 1444]` -> `[1245, 4370, 1990, 4405]`.
  - `#87` `text_block`: `[1983, 622, 2268, 666]` -> `[1245, 4405, 1990, 4440]`.
  - `#88` `text_block`: `[112, 631, 2369, 710]` -> `[1245, 4440, 1990, 4475]`.
  - `#89` `text_block`: `[112, 728, 325, 778]` -> `[1245, 4475, 1990, 4510]`.
  - `#90` `text_block`: `[491, 785, 649, 828]` -> `[1245, 4510, 1800, 4545]`.
  - `#91` `reference`: `[1250, 4791, 2349, 4816]` -> `[1245, 4515, 2345, 4555]`.

- `school_notice_016_文化艺术节场地管理通知_ZHCN`:
  - `#5` `title`: `[94, 401, 2396, 457]` -> `[88, 400, 965, 462]`.
  - `#8` `title`: `[1782, 161, 1940, 226]` -> `[985, 400, 1675, 462]`.
  - `#10` `text_block`: `[75, 524, 1960, 587]` -> `[1010, 530, 1680, 575]`.
  - `#12` `text_block`: `[75, 624, 1859, 685]` -> `[1010, 630, 1680, 675]`.
  - `#15` `title`: `[531, 220, 1951, 286]` -> `[1730, 400, 2405, 462]`.
  - `#19` `text_block`: `[84, 719, 2408, 841]` -> `[1753, 720, 2405, 835]`.
  - `#21` `title`: `None` -> `[88, 955, 1208, 1025]`.
  - `#28` `title`: `None` -> `[1285, 955, 2408, 1025]`.
  - `#35` `text_block`: `[155, 1267, 2398, 1332]` -> `[1285, 1240, 2398, 1325]`.
  - `#36` `title`: `[83, 1623, 2396, 1672]` -> `[88, 1600, 1460, 1665]`.
  - `#44` `title`: `None` -> `[1530, 1600, 2408, 1665]`.
  - `#62` `title`: `None` -> `[1530, 2045, 2408, 2110]`.

GT annotation deletion and order/id changes:

- `slides_029_产品发布_手机`: deleted old `#0` `header` bbox `[165, 118, 2313, 3412]` because it was a duplicate broad wrapper covering almost the whole slide and already overlapped retained finer/table-level annotations.
- `slides_029_产品发布_手机`: no new GT annotation was added. Retained annotations old `#1-#44` were renumbered to new `#0-#43` so the visible review order remains continuous after the deletion.
- `slides_029_产品发布_手机`: no category/type changes in this pass.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `1`.
- Removed GT annotation ids: `slides_029_产品发布_手机` old `#0`.
- Added bbox to existing GT annotations: `8` (`school_notice_006 #8`; `school_notice_005 #35/#50/#70`; `school_notice_016 #21/#28/#44/#62`).
- Bbox changes in this pass: `45`.
- Cleared existing bbox values: `0`.
- Category/type changes in this pass: `0`.
- Order/id changes in this pass: `44` (`slides_029` old `#1-#44` -> new `#0-#43`).
- Non-bbox semantic changes recorded in this pass: `45` (`1` deletion + `44` order/id changes).

Verification:

- Script: `scripts/fix_education_school_notice_slides_batch_v616.py`.
- Report: `reports/pdb_education_school_notice_slides_batch_v616.json`.
- Visual dry-run cover check directory: `cover_audit_education_school_notice_slides_batch_v616_dry/`.
- Visual dry-run outline check directory: `outline_audit_education_school_notice_slides_batch_v616_dry/`.
- Visual cover check directory: `cover_audit_education_school_notice_slides_batch_v616/`.
- Non-cover outline preview directory: `outline_audit_education_school_notice_slides_batch_v616/`.
- Visual review performed before final write using clean/outline crops for the timetable, `slides_029` top slide, `school_notice_005` top/middle/formula/footer regions, and `school_notice_016` top/middle panel title regions. The dry-run crops confirmed the old full-slide `slides_029 #0` was gone and the previously drifting notice labels were back in their visible sections.
- Static validation after final write: `review_data.json` parsed, `review_data.js` parsed from `window.REVIEW_DATA`, `index.html` contains the v616 token, and the four repaired cases report `11/11`, `94/94`, `71/71`, and `44/44` boxed respectively with `0 no bbox`.
- Frontend/cache validation: opened `http://127.0.0.1:8767/index.html?cb=20260612_education_school_notice_slides_batch_v616&case=...` for all four cases. Visible data label showed `data 20260612_education_school_notice_slides_batch_v616`; active rows showed `school_notice_006` `11/11 boxed`, `school_notice_005` `94/94 boxed`, `school_notice_016` `71/71 boxed`, and `slides_029` `44/44 boxed`; overlay rendered `11`, `94`, `71`, and `44` boxes respectively.
- Latest token after this repair: `20260612_education_school_notice_slides_batch_v616`.

## 20260612_education_notice030_syllabus023_v617

Scope:

- Cases:
  - `02_education/04_school_notice/school_notice_030_春季多部门联合公告墙`.
  - `02_education/05_syllabus/syllabus_023_教育心理学`.
- Reason: user flagged both cases as still visibly offset; `school_notice_030` had multiple lower-panel labels drifting into neighboring notice cards, and `syllabus_023` had lower table/reference/page-footer labels floating away from their visual targets.

Files updated:

- `review_data.json`
- `review_data.js`
- `index.html` cache/query token
- `GT_REPAIR_LOG.md`

Token and status:

- Previous token: `20260612_education_school_notice_slides_batch_v616`.
- v617: `20260612_education_notice030_syllabus023_v617`.
- `school_notice_030_春季多部门联合公告墙`: final status `118/118 boxed`, `0 no bbox`, `0 low-similarity`.
- `syllabus_023_教育心理学`: final status `21/21 boxed`, `0 no bbox`, `0 low-similarity`.

Case-level bbox changes:

- `02_education/04_school_notice/school_notice_030_春季多部门联合公告墙`:
  - `#31` `title`: `[123, 1847, 1606, 1900]` -> `[1075, 1298, 1650, 1348]`.
  - `#37` `title`: `[1980, 1856, 2524, 1916]` -> `[1080, 1548, 1245, 1588]`.
  - `#38` `text_block`: `[1085, 1624, 1842, 1728]` -> `[1110, 1550, 1780, 1665]`.
  - `#39` `reference`: `[1021, 1670, 1509, 1710]` -> `[1080, 1670, 1780, 1712]`.
  - `#43` `title`: `[116, 2012, 2641, 2077]` -> `[120, 1998, 520, 2040]`.
  - `#45` `text_block`: `[150, 2056, 2016, 2123]` -> `[335, 2062, 545, 2108]`.
  - `#48` `text_block`: `[401, 2121, 2669, 2180]` -> `[405, 2138, 650, 2185]`.
  - `#51` `reference`: `[1200, 2226, 1893, 2284]` -> `[1205, 2162, 1890, 2216]`.
  - `#53` `title`: `[123, 3088, 557, 3141]` -> `[1980, 1778, 2585, 1830]`.
  - `#54` `text_block`: `[1980, 1933, 2776, 1968]` -> `[1980, 1858, 2700, 1895]`.
  - `#55` `text_block`: `[1980, 1981, 2699, 2062]` -> `[1980, 1908, 2720, 1980]`.
  - `#56` `text_block`: `[2017, 2069, 2676, 2106]` -> `[2015, 1990, 2700, 2030]`.
  - `#57` `text_block`: `[2017, 2110, 2737, 2185]` -> `[2015, 2035, 2735, 2110]`.
  - `#58` `text_block`: `[2017, 2189, 2733, 2226]` -> `[2015, 2118, 2735, 2158]`.
  - `#59` `text_block`: `[2017, 2230, 2784, 2267]` -> `[2015, 2162, 2784, 2202]`.
  - `#60` `text_block`: `[2017, 2271, 2640, 2308]` -> `[2015, 2205, 2650, 2245]`.
  - `#61` `title`: `[1915, 2232, 2523, 2279]` -> `[1980, 2250, 2365, 2290]`.
  - `#62` `text_block`: `[1913, 2264, 2508, 2345]` -> `[1980, 2290, 2680, 2350]`.
  - `#63` `reference`: `[1898, 2346, 2428, 2385]` -> `[1980, 2360, 2520, 2390]`.
  - `#71` `title`: `[123, 4108, 837, 4158]` -> `[1005, 2450, 2400, 2508]`.
  - `#72` `text_block`: `[1051, 2619, 2014, 2653]` -> `[1055, 2525, 1880, 2565]`.
  - `#73` `text_block`: `[1051, 2666, 1985, 2707]` -> `[1055, 2575, 1960, 2615]`.
  - `#74` `text_block`: `[1095, 2720, 1947, 2757]` -> `[1100, 2628, 2000, 2670]`.
  - `#75` `text_block`: `[1095, 2770, 1898, 2808]` -> `[1100, 2680, 1950, 2720]`.
  - `#76` `text_block`: `[1095, 2821, 1866, 2858]` -> `[1100, 2731, 1970, 2770]`.
  - `#77` `text_block`: `[1095, 2871, 1871, 2908]` -> `[1100, 2781, 1950, 2823]`.
  - `#78` `table`: `[1968, 2631, 2829, 2919]` -> `[2050, 2585, 2790, 2828]`.
  - `#79` `reference`: `[2051, 2926, 2773, 2985]` -> `[2050, 2840, 2785, 2898]`.
  - `#80` `title`: `[53, 2987, 538, 3011]` -> `[120, 2970, 610, 3020]`.
  - `#81` `text_block`: `[123, 3159, 843, 3193]` -> `[120, 3035, 875, 3075]`.
  - `#82` `text_block`: `[123, 3206, 932, 3288]` -> `[120, 3078, 940, 3130]`.
  - `#83` `text_block`: `[160, 3294, 821, 3332]` -> `[160, 3130, 850, 3170]`.
  - `#84` `text_block`: `[160, 3335, 625, 3373]` -> `[160, 3172, 650, 3210]`.
  - `#85` `text_block`: `[160, 3380, 682, 3417]` -> `[160, 3215, 710, 3255]`.
  - `#86` `text_block`: `[160, 3421, 809, 3458]` -> `[160, 3255, 830, 3295]`.
  - `#87` `text_block`: `[123, 3471, 887, 3499]` -> `[120, 3295, 900, 3332]`.
  - `#88` `reference`: `[123, 3509, 733, 3541]` -> `[120, 3340, 760, 3375]`.
  - `#89` `title`: `[947, 2944, 1317, 3033]` -> `[1000, 2970, 1300, 3025]`.
  - `#90` `text_block`: `[1051, 3162, 1495, 3196]` -> `[1050, 3035, 1540, 3075]`.
  - `#91` `text_block`: `[1082, 3253, 1901, 3329]` -> `[1080, 3100, 1900, 3186]`.
  - `#92` `text_block`: `[1082, 3383, 1871, 3458]` -> `[1080, 3220, 1890, 3310]`.
  - `#93` `text_block`: `[1082, 3512, 1893, 3587]` -> `[1080, 3345, 1900, 3430]`.
  - `#94` `text_block`: `[1082, 3641, 1859, 3716]` -> `[1080, 3475, 1880, 3560]`.
  - `#95` `text_block`: `[1082, 3770, 1853, 3846]` -> `[1080, 3600, 1880, 3675]`.
  - `#96` `text_block`: `[1006, 3724, 1817, 3855]` -> `[1080, 3730, 1880, 3815]`.
  - `#97` `reference`: `[1007, 3853, 1711, 3917]` -> `[1050, 3830, 1780, 3892]`.
  - `#98` `title`: `[1833, 2944, 2477, 3002]` -> `[1920, 2970, 2560, 3025]`.
  - `#99` `text_block`: `[1980, 3153, 2494, 3190]` -> `[1980, 3045, 2520, 3085]`.
  - `#100` `text_block`: `[1980, 3194, 2494, 3231]` -> `[1980, 3090, 2520, 3130]`.
  - `#101` `text_block`: `[1980, 3234, 2389, 3272]` -> `[1980, 3135, 2420, 3175]`.
  - `#102` `text_block`: `[1980, 3275, 2380, 3312]` -> `[1980, 3180, 2420, 3220]`.
  - `#103` `text_block`: `[1980, 3315, 2368, 3353]` -> `[1980, 3225, 2405, 3265]`.
  - `#104` `text_block`: `[1980, 3362, 2267, 3394]` -> `[1980, 3272, 2280, 3310]`.
  - `#105` `title`: `[31, 3961, 782, 4012]` -> `[120, 3975, 870, 4030]`.
  - `#106` `text_block`: `[129, 4049, 1576, 4096]` -> `[135, 4045, 380, 4088]`.
  - `#107` `text_block`: `[406, 4183, 598, 4220]` -> `[410, 4045, 620, 4088]`.
  - `#108` `text_block`: `[645, 4183, 866, 4220]` -> `[650, 4045, 900, 4088]`.
  - `#109` `text_block`: `[912, 4183, 1132, 4220]` -> `[915, 4045, 1160, 4088]`.
  - `#110` `text_block`: `[1178, 4183, 1425, 4220]` -> `[1180, 4045, 1465, 4088]`.
  - `#111` `text_block`: `[1472, 4183, 1665, 4220]` -> `[1480, 4045, 1700, 4088]`.
  - `#112` `text_block`: `[129, 4115, 1462, 4162]` -> `[130, 4110, 390, 4155]`.
  - `#113` `text_block`: `[458, 4249, 706, 4286]` -> `[455, 4110, 720, 4155]`.
  - `#114` `text_block`: `[753, 4249, 934, 4286]` -> `[755, 4110, 950, 4155]`.
  - `#115` `text_block`: `[981, 4249, 1227, 4286]` -> `[980, 4110, 1250, 4155]`.
  - `#116` `text_block`: `[1274, 4249, 1541, 4286]` -> `[1280, 4110, 1560, 4155]`.
  - `#117` `header`: `[126, 4349, 2827, 4350]` -> `[90, 4215, 2750, 4265]`.

- `02_education/05_syllabus/syllabus_023_教育心理学`:
  - `#8` `title`: `[83, 1127, 283, 1158]` -> `[80, 1070, 290, 1110]`.
  - `#9` `table`: `[78, 1177, 2382, 1914]` -> `[80, 1120, 2300, 1830]`.
  - `#10` `title`: `[83, 1934, 316, 1966]` -> `[80, 1845, 320, 1890]`.
  - `#11` `table`: `[85, 1908, 1231, 2390]` -> `[80, 1895, 1190, 2280]`.
  - `#12` `title`: `[1248, 1934, 1382, 1966]` -> `[1200, 1845, 1350, 1890]`.
  - `#13` `table`: `[1197, 1958, 2382, 2331]` -> `[1200, 1895, 2300, 2228]`.
  - `#14` `title`: `[1248, 2352, 1415, 2383]` -> `[1200, 2250, 1400, 2295]`.
  - `#15` `text_block`: `[1250, 385, 1687, 413]` -> `[1200, 2298, 1850, 2335]`.
  - `#16` `text_block`: `[1411, 2443, 1739, 2471]` -> `[1200, 2335, 1800, 2370]`.
  - `#17` `text_block`: `[1011, 265, 1470, 306]` -> `[1200, 2370, 1700, 2405]`.
  - `#18` `text_block`: `[1372, 2516, 1700, 2544]` -> `[1200, 2405, 1785, 2440]`.
  - `#19` `text_block`: `[83, 340, 229, 368]` -> `[1200, 2440, 1600, 2475]`.
  - `#20` `header`: `[956, 2606, 1525, 2631]` -> `[800, 2492, 1500, 2525]`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0`.
- Bbox changes in this pass: `79`.
- Cleared existing bbox values: `0`.
- Category/type changes in this pass: `0`.
- Order/id changes in this pass: `0`.
- Non-bbox semantic changes recorded in this pass: `0`.

Verification:

- Script: `scripts/fix_education_notice030_syllabus023_v617.py`.
- Report: `reports/pdb_education_notice030_syllabus023_v617.json`.
- Visual dry-run cover check directory: `cover_audit_education_notice030_syllabus023_v617_dry/`.
- Visual dry-run outline check directory: `outline_audit_education_notice030_syllabus023_v617_dry/`.
- Visual cover check directory: `cover_audit_education_notice030_syllabus023_v617/`.
- Non-cover outline preview directory: `outline_audit_education_notice030_syllabus023_v617/`.
- Visual review performed before final write using clean/grid crops for `school_notice_030` upper/middle/lower panels and `syllabus_023` lower table/reference area. Formal cover and outline images were inspected after final write; the previously floating ids in the user screenshots were aligned back to their visible notice-card/table/reference targets.
- Static validation after final write: `review_data.json` parsed, `review_data.js` parsed from `window.REVIEW_DATA`, `index.html` contains the v617 token three times, `meta.created_at`, `meta.build_token`, and `metadata.last_manual_fix_token` all equal `20260612_education_notice030_syllabus023_v617`.
- Frontend/cache validation: opened `http://127.0.0.1:8767/index.html?cb=20260612_education_notice030_syllabus023_v617&case=...` for both cases. Visible data label showed `data 20260612_education_notice030_syllabus023_v617`; active rows showed `school_notice_030` `118/118 boxed · 0 no bbox` and `syllabus_023` `21/21 boxed · 0 no bbox`; overlay rendered `118` and `21` boxes/labels respectively; natural image sizes were `2835x4350` and `2382x3489`; browser console error log was empty.
- Latest token after this repair: `20260612_education_notice030_syllabus023_v617`.

## 20260612_education_syllabus032_visual_v618

Scope:

- Case: `02_education/05_syllabus/syllabus_032_Global_Media_Culture`.
- Reason: user reported remaining visual drift in the lower half of the syllabus page. Visual inspection showed the assessment block, weekly schedule table, lower policy/reading sections, references, and footer annotations were shifted from their visible text/table targets. The no-bbox `#71` header/footer annotation also needed a real bbox.
- Previous token: `20260612_education_notice030_syllabus023_v617`.
- New token: `20260612_education_syllabus032_visual_v618`.
- Files updated: `review_data.json`, `review_data.js`, `index.html`, `GT_REPAIR_LOG.md`.
- Status after repair for this case: `72/72 boxed`, `0 no bbox`, `0 low`.

Case-level bbox changes:

- `02_education/05_syllabus/syllabus_032_Global_Media_Culture`:
  - `#30` `text_block`: `[1288, 1028, 2274, 1076]` -> `[1210, 935, 2275, 985]`.
  - `#31` `title`: `[113, 1045, 753, 1088]` -> `[105, 1045, 760, 1090]`.
  - `#32` `table`: `[108, 1256, 2271, 1529]` -> `[100, 1108, 1165, 1305]`.
  - `#33` `text_block`: `[1285, 1267, 2347, 1398]` -> `[1215, 1108, 2280, 1192]`.
  - `#34` `text_block`: `[127, 1176, 2177, 1257]` -> `[1215, 1188, 2265, 1250]`.
  - `#35` `title`: `[114, 1331, 702, 1384]` -> `[105, 1335, 710, 1382]`.
  - `#36` `table`: `[101, 1534, 2374, 2383]` -> `[100, 1390, 2280, 2155]`.
  - `#37` `title`: `[98, 2303, 550, 2339]` -> `[100, 2158, 560, 2198]`.
  - `#38` `text_block`: `[1281, 59, 1486, 78]` -> `[100, 2205, 760, 2240]`.
  - `#39` `text_block`: `[108, 2434, 1045, 2572]` -> `[100, 2240, 840, 2275]`.
  - `#40` `text_block`: `[2081, 57, 2372, 77]` -> `[100, 2274, 990, 2308]`.
  - `#41` `text_block`: `[872, 195, 1605, 262]` -> `[100, 2306, 760, 2340]`.
  - `#42` `title`: `[100, 2442, 475, 2479]` -> `[100, 2345, 485, 2382]`.
  - `#43` `text_block`: `[378, 2621, 715, 2650]` -> `[100, 2388, 860, 2422]`.
  - `#44` `text_block`: `[101, 2418, 1000, 2449]` -> `[100, 2422, 1020, 2458]`.
  - `#45` `text_block`: `[101, 2430, 1704, 2486]` -> `[100, 2458, 850, 2495]`.
  - `#46` `title`: `[100, 2470, 1616, 2516]` -> `[100, 2498, 625, 2535]`.
  - `#47` `text_block`: `[101, 2508, 1592, 2561]` -> `[100, 2538, 770, 2574]`.
  - `#48` `text_block`: `[101, 2534, 1571, 2587]` -> `[100, 2574, 720, 2608]`.
  - `#49` `text_block`: `[359, 2821, 588, 2849]` -> `[100, 2608, 650, 2642]`.
  - `#50` `text_block`: `[101, 2593, 1787, 2645]` -> `[100, 2640, 950, 2675]`.
  - `#51` `text_block`: `[101, 2631, 1520, 2676]` -> `[100, 2672, 850, 2707]`.
  - `#52` `title`: `[1208, 2393, 1832, 2410]` -> `[1210, 2155, 1850, 2198]`.
  - `#53` `text_block`: `[1287, 2450, 2252, 2642]` -> `[1215, 2215, 2240, 2410]`.
  - `#54` `text_block`: `[120, 340, 308, 372]` -> `[1230, 2252, 1795, 2288]`.
  - `#55` `text_block`: `[871, 339, 978, 371]` -> `[1230, 2288, 1910, 2322]`.
  - `#56` `text_block`: `[1622, 338, 1698, 370]` -> `[1230, 2322, 1610, 2358]`.
  - `#57` `text_block`: `[1287, 2619, 2005, 2642]` -> `[1230, 2358, 2200, 2404]`.
  - `#58` `title`: `[1210, 2577, 1767, 2596]` -> `[1210, 2428, 1730, 2465]`.
  - `#59` `text_block`: `[120, 384, 262, 416]` -> `[1210, 2478, 1930, 2510]`.
  - `#60` `text_block`: `[871, 383, 956, 414]` -> `[1210, 2512, 1880, 2545]`.
  - `#61` `text_block`: `[963, 392, 1222, 414]` -> `[1210, 2548, 1910, 2580]`.
  - `#62` `text_block`: `[1266, 2708, 1877, 2871]` -> `[1210, 2580, 2065, 2615]`.
  - `#63` `text_block`: `[1622, 382, 1712, 413]` -> `[1210, 2615, 2160, 2650]`.
  - `#64` `title`: `[1154, 2768, 1573, 2786]` -> `[1210, 2655, 1605, 2690]`.
  - `#65` `text_block`: `[1212, 2674, 2066, 2716]` -> `[1210, 2695, 2210, 2728]`.
  - `#66` `text_block`: `[1212, 2710, 1884, 2745]` -> `[1210, 2728, 2060, 2760]`.
  - `#67` `reference`: `[102, 2755, 2279, 2790]` -> `[100, 2748, 825, 2772]`.
  - `#68` `reference`: `[121, 428, 166, 459]` -> `[865, 2748, 1455, 2776]`.
  - `#69` `reference`: `[871, 427, 1008, 458]` -> `[1465, 2748, 2295, 2776]`.
  - `#70` `reference`: `[101, 2774, 753, 2811]` -> `[100, 2772, 770, 2806]`.
  - `#71` `header`: `None` -> `[90, 3305, 2295, 3335]`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `1` (`#71`).
- Bbox changes in this pass: `42`.
- Cleared existing bbox values: `0`.
- Category/type changes in this pass: `0`.
- Order/id changes in this pass: `0`.
- Non-bbox semantic changes recorded in this pass: `0`.

Verification:

- Script: `scripts/fix_education_syllabus032_visual_v618.py`.
- Report: `reports/pdb_education_syllabus032_visual_v618.json`.
- Visual dry-run cover check directory: `cover_audit_education_syllabus032_visual_v618_dry/`.
- Visual dry-run outline check directory: `outline_audit_education_syllabus032_visual_v618_dry/`.
- Visual cover check directory: `cover_audit_education_syllabus032_visual_v618/`.
- Non-cover outline preview directory: `outline_audit_education_syllabus032_visual_v618/`.
- Visual review performed with current outline/cover and coordinate crops for the assessment, weekly schedule, lower section, footer, and full lower page areas. Formal cover and outline images were inspected after final write; the user-reported lower-page drift was corrected to the visible section/table/text/footer targets.
- Static validation after final write: `review_data.json` parsed, `review_data.js` parsed from `window.REVIEW_DATA`, `index.html` contains the v618 token three times, `meta.created_at`, `meta.build_token`, and `metadata.last_manual_fix_token` all equal `20260612_education_syllabus032_visual_v618`.
- Frontend/cache validation: opened `http://127.0.0.1:8767/index.html?cb=20260612_education_syllabus032_visual_v618&case=02_education%2F05_syllabus%2Fsyllabus_032_Global_Media_Culture`. Visible data label showed `data 20260612_education_syllabus032_visual_v618`; active row showed `syllabus_032_Global_Media_Culture` `72/72 boxed · 0 no bbox`; overlay rendered `72` boxes/labels; natural image size was `2382x3369`; browser console error log was empty.
- Latest token after this repair: `20260612_education_syllabus032_visual_v618`.

## 20260612_education_syllabus014_visible_v619

Scope:

- Case: `02_education/05_syllabus/syllabus_014_国际贸易实务`.
- Reason: user reported that `#0` had drifted down into the lower table and `#21` appeared at the top. Visual inspection of the clean PNG confirmed a broader vertical drift: visible table/title annotations were shifted between sections, while lower reference/policy entries were not visible in the current `2382x3369` image. The duplicate top header extraction `#21` was also redundant with the visible header retained as `#0`.
- Previous token: `20260612_education_syllabus032_visual_v618`.
- New token: `20260612_education_syllabus014_visible_v619`.
- Files updated: `review_data.json`, `review_data.js`, `index.html`, `GT_REPAIR_LOG.md`.
- Status after repair for this case: `11/11 boxed`, `0 no bbox`, `0 low`.

Case-level bbox changes:

- `02_education/05_syllabus/syllabus_014_国际贸易实务`:
  - `#0` `header`: `[957, 3189, 1524, 3225]` -> `[835, 78, 1548, 238]`.
  - `#1` `title`: `[532, 262, 1841, 338]` -> `[525, 276, 1855, 360]`.
  - `#2` `title`: `[130, 414, 391, 462]` -> `[130, 410, 395, 470]`.
  - `#3` `table`: `[108, 402, 2373, 711]` -> `[108, 500, 2373, 775]`.
  - `#4` `title`: `[129, 836, 391, 906]` -> `[130, 832, 398, 905]`.
  - `#5` `table`: `[108, 731, 2373, 1429]` -> `[108, 928, 2373, 1688]`.
  - `#6` `title`: `[132, 1733, 396, 1794]` -> `[132, 1732, 405, 1800]`.
  - `#7` `table`: `[108, 1431, 2373, 2343]` -> `[108, 1832, 2373, 2770]`.
  - `#8` `title`: `[130, 2795, 308, 2866]` -> `[130, 2792, 315, 2865]`.
  - `#9` `table`: `[108, 2332, 2373, 2692]` -> `[108, 2878, 2373, 3292]`.
  - `#10` `title`: `[138, 2698, 459, 2744]` -> `[130, 3310, 520, 3368]`.

Removed GT annotations:

- `#11` `text_block`: removed bbox `[232, 2779, 1298, 2816]`; text `黎孝先、王健《国际贸易实务》第七版，对外经贸大学出版社（主教材）`; reason: not visible in current clean PNG below the clipped reference/resources title.
- `#12` `text_block`: removed bbox `[232, 2819, 856, 2856]`; text `ICC, Incoterms 2020, ICC Publication No. 723`; reason: not visible in current clean PNG below the clipped reference/resources title.
- `#13` `text_block`: removed bbox `[232, 2859, 1202, 2896]`; text `ICC, UCP 600: Uniform Customs and Practice for Documentary Credits`; reason: not visible in current clean PNG below the clipped reference/resources title.
- `#14` `text_block`: removed bbox `[232, 2899, 825, 2936]`; text `联合国《国际货物销售合同公约》(CISG)`; reason: not visible in current clean PNG below the clipped reference/resources title.
- `#15` `text_block`: removed bbox `[232, 2939, 898, 2976]`; text `海关总署官网、中国国际贸易促进委员会官网`; reason: not visible in current clean PNG below the clipped reference/resources title.
- `#16` `title`: removed bbox `[138, 3010, 321, 3056]`; text `课程政策`; reason: not visible in current clean PNG below the clipped reference/resources title.
- `#17` `text_block`: removed bbox `[302, 2819, 508, 2856]`; text `纪律：缺课达三次自动取消成绩资格。`; reason: not visible in current clean PNG below the clipped reference/resources title.
- `#18` `text_block`: removed bbox `[107, 3076, 2364, 3148]`; text `学术诚信：案例报告严禁抄袭，引用须注明出处，一经发现报告计零分。`; reason: not visible in current clean PNG below the clipped reference/resources title.
- `#19` `text_block`: removed bbox `[302, 2859, 1202, 2896]`; text `迟交：每迟交一天扣总分的5%，超过7天不予接收。`; reason: not visible in current clean PNG below the clipped reference/resources title.
- `#20` `text_block`: removed bbox `[107, 3076, 207, 3112]`; text `答疑：周四16:00-17:30，学院608。`; reason: not visible in current clean PNG below the clipped reference/resources title.
- `#21` `header`: removed bbox `[1024, 151, 1457, 197]`; text `对外经济贸易大学 / 国际经济贸易学院`; reason: duplicate top header extraction; visible header retained as `#0`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `11` (`#11-#21`).
- Added bbox to existing GT annotations: `0`.
- Bbox changes in this pass: `11`.
- Cleared existing bbox values without deleting annotations: `0`.
- Category/type changes in this pass: `0`.
- Order/id changes in this pass: `0`.
- Non-bbox semantic changes recorded in this pass: `11` (the removed non-visible/duplicate GT annotations).

Verification:

- Script: `scripts/fix_education_syllabus014_visible_v619.py`.
- Report: `reports/pdb_education_syllabus014_visible_v619.json`.
- Visual dry-run cover check directory: `cover_audit_education_syllabus014_visible_v619_dry/`.
- Visual dry-run outline check directory: `outline_audit_education_syllabus014_visible_v619_dry/`.
- Visual cover check directory: `cover_audit_education_syllabus014_visible_v619/`.
- Non-cover outline preview directory: `outline_audit_education_syllabus014_visible_v619/`.
- Visual review performed with current outline/cover and coordinate crops for the top header/basic table, case table, weekly schedule, assessment table, and clipped lower reference area. Dry-run and formal outline images were inspected; `#0` is aligned to the top visible header, `#21` is no longer overlaid, and `#3/#5/#7/#9` cover their full visible table extents.
- Static validation after final write: `review_data.json` parsed, `review_data.js` parsed from `window.REVIEW_DATA`, `index.html` contains the v619 token three times, `meta.created_at`, `meta.build_token`, and `metadata.last_manual_fix_token` all equal `20260612_education_syllabus014_visible_v619`.
- Frontend/cache validation: opened `http://127.0.0.1:8767/index.html?cb=20260612_education_syllabus014_visible_v619&case=02_education%2F05_syllabus%2Fsyllabus_014_%E5%9B%BD%E9%99%85%E8%B4%B8%E6%98%93%E5%AE%9E%E5%8A%A1`. Visible data label showed `data 20260612_education_syllabus014_visible_v619`; active row showed `syllabus_014_国际贸易实务` `11/11 boxed · 0 no bbox`; overlay rendered `11` boxes/labels (`#0-#10`); natural image size was `2382x3369`; browser console error log was empty.
- Latest token after this repair: `20260612_education_syllabus014_visible_v619`.

## 20260612_education_syllabus014034_visual_v620

Scope:

- Cases:
  - `02_education/05_syllabus/syllabus_014_国际贸易实务`.
  - `02_education/05_syllabus/syllabus_034_Python_Software_Engineering`.
- Reason: user asked why `syllabus_014_国际贸易实务` had only 11 elements after v619, and reported that `syllabus_034_Python_Software_Engineering` still had visible bbox drift. v620 corrects the v619 over-deletion by restoring hidden GT annotations as no-bbox annotations, and repairs the Python syllabus visual offsets after clean-PNG/outline inspection.
- Previous token: `20260612_education_syllabus014_visible_v619`.
- New token: `20260612_education_syllabus014034_visual_v620`.
- Files updated: `review_data.json`, `review_data.js`, `index.html`, `GT_REPAIR_LOG.md`.
- Status after repair:
  - `syllabus_014_国际贸易实务`: `11/22 boxed`, `11 no bbox`, `0 low`.
  - `syllabus_034_Python_Software_Engineering`: `55/55 boxed`, `0 no bbox`, `0 low`.

Case-level GT annotation changes:

- `02_education/05_syllabus/syllabus_014_国际贸易实务`:
  - Added GT annotations in this pass: `11` (restored from `review_data.before_20260612_education_syllabus014_visible_v619.json`).
  - Removed GT annotations in this pass: `0`.
  - Existing bbox changes in this pass: `0`.
  - Restored annotations were intentionally left with `bbox=None` / `poly=None` because the current `2382x3369` clean PNG only shows the clipped `参考书目与资源` heading; the detailed reference/policy entries are not visible in the current image. `#21` is a duplicate top-header GT and is also restored as no-bbox to preserve GT count without overlay duplication.
  - Restored `#11` `text_block`: source bbox `[232, 2779, 1298, 2816]` -> `None`; text `黎孝先、王健《国际贸易实务》第七版，对外经贸大学出版社（主教材）`.
  - Restored `#12` `text_block`: source bbox `[232, 2819, 856, 2856]` -> `None`; text `ICC, Incoterms 2020, ICC Publication No. 723`.
  - Restored `#13` `text_block`: source bbox `[232, 2859, 1202, 2896]` -> `None`; text `ICC, UCP 600: Uniform Customs and Practice for Documentary Credits`.
  - Restored `#14` `text_block`: source bbox `[232, 2899, 825, 2936]` -> `None`; text `联合国《国际货物销售合同公约》(CISG)`.
  - Restored `#15` `text_block`: source bbox `[232, 2939, 898, 2976]` -> `None`; text `海关总署官网、中国国际贸易促进委员会官网`.
  - Restored `#16` `title`: source bbox `[138, 3010, 321, 3056]` -> `None`; text `课程政策`.
  - Restored `#17` `text_block`: source bbox `[302, 2819, 508, 2856]` -> `None`; text `纪律：缺课达三次自动取消成绩资格。`.
  - Restored `#18` `text_block`: source bbox `[107, 3076, 2364, 3148]` -> `None`; text `学术诚信：案例报告严禁抄袭，引用须注明出处，一经发现报告计零分。`.
  - Restored `#19` `text_block`: source bbox `[302, 2859, 1202, 2896]` -> `None`; text `迟交：每迟交一天扣总分的5%，超过7天不予接收。`.
  - Restored `#20` `text_block`: source bbox `[107, 3076, 207, 3112]` -> `None`; text `答疑：周四16:00-17:30，学院608。`.
  - Restored `#21` `header`: source bbox `[1024, 151, 1457, 197]` -> `None`; text `对外经济贸易大学 / 国际经济贸易学院`.

- `02_education/05_syllabus/syllabus_034_Python_Software_Engineering`:
  - Added GT annotations in this pass: `2`.
  - Removed GT annotations in this pass: `0`.
  - Existing bbox changes in this pass: `52`.
  - Added bbox to existing GT annotations: `3` (`#23`, `#31`, old `#52` -> new `#54`).
  - Order/id changes in this pass: `14` (old `#39-#52` shifted to new `#41-#54` after inserting the missing Weekly Schedule title/table).
  - Added `#39` `title`: bbox `[100, 1848, 740, 1918]`; text `📅 Weekly Schedule / 教学进度表`.
  - Added `#40` `table`: bbox `[100, 1938, 2290, 2865]`; text begins `Wk Topic / 主题 Lab / 实验 Assignment Tool Deliverable ...`.
  - `#1` `title`: `[1347, 3183, 1514, 3214]` -> `[130, 110, 910, 175]`.
  - `#2` `title`: `[131, 189, 969, 222]` -> `[130, 188, 780, 225]`.
  - `#3` `text_block`: `[307, 239, 407, 265]` -> `[130, 245, 415, 275]`.
  - `#4` `text_block`: `[883, 247, 1394, 278]` -> `[845, 245, 1395, 280]`.
  - `#5` `text_block`: `[1629, 247, 2019, 278]` -> `[1585, 245, 2040, 280]`.
  - `#6` `text_block`: `[138, 290, 583, 321]` -> `[130, 288, 610, 322]`.
  - `#7` `text_block`: `[930, 284, 1125, 311]` -> `[845, 288, 1135, 322]`.
  - `#8` `text_block`: `[1629, 290, 2086, 321]` -> `[1585, 288, 2100, 322]`.
  - `#9` `text_block`: `[138, 334, 374, 365]` -> `[130, 332, 390, 365]`.
  - `#10` `text_block`: `[883, 334, 1314, 365]` -> `[845, 332, 1320, 365]`.
  - `#11` `text_block`: `[1712, 319, 1865, 351]` -> `[1585, 332, 1885, 365]`.
  - `#12` `title`: `[107, 398, 499, 457]` -> `[100, 395, 520, 460]`.
  - `#13` `text_block`: `[99, 405, 1755, 673]` -> `[95, 480, 1165, 665]`.
  - `#14` `text_block`: `[100, 674, 1471, 768]` -> `[95, 682, 1165, 775]`.
  - `#15` `title`: `[103, 778, 506, 828]` -> `[100, 790, 520, 838]`.
  - `#16` `text_block`: `[99, 848, 1039, 883]` -> `[95, 860, 1045, 898]`.
  - `#17` `text_block`: `[98, 882, 707, 932]` -> `[95, 900, 725, 938]`.
  - `#18` `text_block`: `[98, 932, 998, 967]` -> `[95, 940, 1005, 978]`.
  - `#19` `text_block`: `[97, 977, 992, 1012]` -> `[95, 982, 1005, 1020]`.
  - `#20` `text_block`: `[98, 1012, 645, 1062]` -> `[95, 1024, 650, 1065]`.
  - `#21` `title`: `[163, 1074, 481, 1122]` -> `[100, 1082, 500, 1130]`.
  - `#22` `table`: `[108, 1149, 1210, 1531]` -> `[105, 1160, 1210, 1538]`.
  - `#23` `title`: `None` -> `[1210, 395, 1795, 460]`.
  - `#24` `code_txt`: `[1213, 1478, 2257, 2935]` -> `[1210, 480, 2290, 665]`.
  - `#25` `title`: `[1251, 713, 1470, 747]` -> `[1250, 725, 1490, 762]`.
  - `#26` `text_block`: `[1522, 795, 1621, 823]` -> `[1245, 782, 1628, 820]`.
  - `#27` `text_block`: `[1513, 835, 1612, 863]` -> `[1245, 825, 1628, 863]`.
  - `#28` `text_block`: `[1632, 875, 1796, 903]` -> `[1245, 868, 1818, 908]`.
  - `#29` `text_block`: `[1444, 915, 1537, 943]` -> `[1245, 910, 1540, 948]`.
  - `#30` `text_block`: `[1332, 949, 1508, 984]` -> `[1245, 952, 1965, 992]`.
  - `#31` `title`: `None` -> `[1215, 1038, 1610, 1095]`.
  - `#32` `text_block`: `[1248, 1068, 1734, 1143]` -> `[1245, 1135, 1835, 1198]`.
  - `#33` `text_block`: `[1991, 1195, 2272, 1229]` -> `[1245, 1205, 2175, 1248]`.
  - `#34` `text_block`: `[1249, 1177, 1896, 1224]` -> `[1245, 1248, 1950, 1290]`.
  - `#35` `text_block`: `[1249, 1212, 1634, 1261]` -> `[1245, 1290, 1695, 1332]`.
  - `#36` `text_block`: `[1249, 1246, 1849, 1296]` -> `[1245, 1332, 1900, 1375]`.
  - `#37` `title`: `[1217, 1330, 1591, 1377]` -> `[1215, 1395, 1630, 1452]`.
  - `#38` `code_txt`: `[110, 1329, 2257, 2935]` -> `[1215, 1500, 2290, 1938]`.
  - Old `#39` -> new `#41` `title`: `[97, 2898, 527, 2964]` -> `[115, 2885, 660, 2942]`.
  - Old `#40` -> new `#42` `text_block`: `[172, 424, 518, 468]` -> `[120, 2960, 780, 3002]`.
  - Old `#41` -> new `#43` `text_block`: `[107, 421, 160, 468]` -> `[120, 3005, 1000, 3046]`.
  - Old `#42` -> new `#44` `text_block`: `[480, 3165, 883, 3199]` -> `[120, 3048, 960, 3094]`.
  - Old `#43` -> new `#45` `text_block`: `[172, 816, 525, 860]` -> `[120, 3098, 970, 3140]`.
  - Old `#44` -> new `#46` `text_block`: `[302, 3245, 477, 3279]` -> `[120, 3142, 1000, 3186]`.
  - Old `#45` -> new `#47` `title`: `[1252, 2923, 1609, 2953]` -> `[1265, 2885, 1590, 2935]`.
  - Old `#46` -> new `#48` `text_block`: `[1239, 2953, 2342, 3133]` -> `[1260, 2890, 2290, 2990]`.
  - Old `#47` -> new `#49` `title`: `[1237, 3064, 1509, 3105]` -> `[1265, 3015, 1585, 3060]`.
  - Old `#48` -> new `#50` `text_block`: `[1239, 3061, 2025, 3363]` -> `[1260, 3060, 2060, 3100]`.
  - Old `#49` -> new `#51` `text_block`: `[1333, 3257, 1487, 3289]` -> `[1260, 3100, 1850, 3140]`.
  - Old `#50` -> new `#52` `text_block`: `[1333, 3295, 1650, 3326]` -> `[1260, 3140, 1950, 3180]`.
  - Old `#51` -> new `#53` `text_block`: `[1333, 3332, 1764, 3363]` -> `[1260, 3180, 2240, 3222]`.
  - Old `#52` -> new `#54` `header`: `None` -> `[95, 3295, 2290, 3330]`.

GT annotation change:

- Added GT annotations in this pass: `13` total (`11` restored no-bbox annotations for `syllabus_014`, `2` new visible annotations for `syllabus_034`).
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `3`.
- Existing bbox changes in this pass: `52`.
- Cleared existing bbox values without deleting annotations: `0`.
- Category/type changes in this pass: `0`.
- Order/id changes in this pass: `14`.
- Non-bbox semantic changes recorded in this pass: `27` (`11` restored no-bbox annotations, `2` added visible annotations, `14` order/id shifts).

Verification:

- Script: `scripts/fix_education_syllabus014034_visual_v620.py`.
- Report: `reports/pdb_education_syllabus014034_visual_v620.json`.
- Visual dry-run cover check directory: `cover_audit_education_syllabus014034_visual_v620_dry/`.
- Visual dry-run outline check directory: `outline_audit_education_syllabus014034_visual_v620_dry/`.
- Visual cover check directory: `cover_audit_education_syllabus014034_visual_v620/`.
- Non-cover outline preview directory: `outline_audit_education_syllabus014034_visual_v620/`.
- Visual review performed with clean-PNG crops, coordinate-grid crops for the `syllabus_034` Weekly Schedule and footer panels, plus dry-run and formal outline/cover inspection. The second dry-run adjusted `#39/#40` upward to the real Weekly Schedule title/table top and moved `#41-#54` to the Coding Standard / Academic Integrity / References / footer region.
- Static validation after final write: `review_data.json` parsed, `review_data.js` parsed from `window.REVIEW_DATA`, `index.html` contains the v620 token three times, `meta.created_at`, `meta.build_token`, and `metadata.last_manual_fix_token` all equal `20260612_education_syllabus014034_visual_v620`.
- Frontend/cache validation:
  - Opened `http://127.0.0.1:8767/index.html?cb=20260612_education_syllabus014034_visual_v620&case=02_education%2F05_syllabus%2Fsyllabus_014_%E5%9B%BD%E9%99%85%E8%B4%B8%E6%98%93%E5%AE%9E%E5%8A%A1`. Visible data label showed `data 20260612_education_syllabus014034_visual_v620`; active row showed `syllabus_014_国际贸易实务` `11/22 boxed · 11 no bbox · 22 open`; overlay rendered `11` labels (`#0-#10`); natural image size was `2382x3369`; browser console error log was empty.
  - Opened `http://127.0.0.1:8767/index.html?cb=20260612_education_syllabus014034_visual_v620&case=02_education%2F05_syllabus%2Fsyllabus_034_Python_Software_Engineering`. Visible data label showed `data 20260612_education_syllabus014034_visual_v620`; active row showed `syllabus_034_Python_Software_Engineering` `55/55 boxed · 0 no bbox · 55 open`; overlay rendered `55` labels (`#0-#54`); natural image size was `2382x3369`; browser console error log was empty.
- Latest token after this repair: `20260612_education_syllabus014034_visual_v620`.

## 20260612_education_syllabus036_visual_v621

Scope:

- Case: `02_education/05_syllabus/syllabus_036_Research_Methods`.
- Reason: user reported visible bbox drift in the Research Methods syllabus. Clean-PNG/outline inspection showed top contact-strip bboxes were over-wide, several visible section titles were still no-bbox, and Methods/Policies/References/footnote annotations were wrongly bound to the top contact strip or lower blank area.
- Previous token: `20260612_education_syllabus014034_visual_v620`.
- New token: `20260612_education_syllabus036_visual_v621`.
- Files updated: `review_data.json`, `review_data.js`, `index.html`, `GT_REPAIR_LOG.md`.
- Status after repair for this case: `45/45 boxed`, `0 no bbox`, `0 low`.

Case-level bbox changes:

- `#0` `header`: `[112, 76, 1204, 158]` -> `[105, 75, 1240, 158]`; text `Graduate Seminar · 2026 Spring Tsinghua University · Institute for Interdisciplinary Studies · 清华大学交叉信息研究院`.
- `#1` `title`: `[112, 167, 1100, 234]` -> `[105, 168, 1125, 235]`; text `Interdisciplinary Research Methods`.
- `#2` `title`: `[131, 231, 623, 296]` -> `[105, 232, 640, 295]`; text `《跨学科研究方法》课程大纲`.
- `#3` `text_block`: `[111, 288, 966, 330]` -> `[105, 305, 995, 338]`; text `IDS 510 • 3 Credits / 48 Hours • Weeks 1–16 • Thu 18:30–21:00, 六教 6B311`.
- `#4` `text_block`: `[126, 359, 2018, 404]` -> `[105, 360, 665, 405]`; text `Instructor: Dr. Zhang Yifan 张一凡 (Sociology / STS)`.
- `#5` `text_block`: `[793, 389, 1358, 420]` -> `[710, 360, 1200, 405]`; text `Co-instructor: Prof. Emily Hart (Data Science)`.
- `#6` `text_block`: `[1383, 389, 1732, 420]` -> `[1240, 360, 1565, 405]`; text `Email: zyf@tsinghua.edu.cn`.
- `#7` `text_block`: `[1757, 389, 2163, 420]` -> `[1595, 360, 2245, 405]`; text `Office: 新斋学堂 428, Tue 14–16h`.
- `#8` `title`: `[134, 440, 1640, 490]` -> `[105, 432, 540, 500]`; text `1 Course Overview`.
- `#9` `text_block`: `[144, 525, 1390, 782]` -> `[105, 510, 1310, 710]`; text `This seminar equips graduate students with the conceptual foundations and practical skills for conducting rigorous interdisciplinary research. Stud...`.
- `#10` `title`: `None` -> `[1215, 432, 1565, 500]`; text `2 课程定位`.
- `#11` `text_block`: `[1514, 519, 2324, 640]` -> `[1215, 510, 2245, 650]`; text `本课程面向全校研究生，尤其适合处于论文选题初期的博士生与硕士生。无论你的学科背景是工程、社会科学、人文还是自然科学，本课程都将帮助你掌握跨学科研究的核心能力。`.
- `#12` `text_block`: `[134, 664, 2143, 732]` -> `[1250, 675, 2218, 755]`; text `“The most exciting research happens at the boundaries between disciplines.” — E.O. Wilson`.
- `#13` `text_block`: `[653, 805, 1733, 883]` -> `[640, 790, 1940, 880]`; text `“Research is formalized curiosity. It is poking and prying with a purpose.” — Zora Neale Hurston`.
- `#14` `title`: `[134, 947, 1581, 997]` -> `[105, 945, 560, 1002]`; text `3 Learning Outcomes`.
- `#15` `text_block`: `[138, 999, 2152, 1033]` -> `[105, 995, 1015, 1038]`; text `Formulate interdisciplinary research questions (RQ) bridging ≥2 fields`.
- `#16` `text_block`: `[137, 1033, 1815, 1078]` -> `[105, 1035, 825, 1080]`; text `掌握定性、定量与混合研究设计的基本原理`.
- `#17` `text_block`: `[137, 1083, 887, 1117]` -> `[105, 1078, 910, 1122]`; text `Design and pilot a survey, interview protocol, or coding scheme`.
- `#18` `text_block`: `[136, 1125, 1559, 1159]` -> `[105, 1120, 860, 1165]`; text `Evaluate validity, reliability, bias, and sampling strategies`.
- `#19` `text_block`: `[175, 1229, 762, 1264]` -> `[105, 1162, 765, 1205]`; text `撰写符合学术规范的研究提案 (mini proposal)`.
- `#20` `text_block`: `[137, 1206, 761, 1240]` -> `[105, 1205, 785, 1248]`; text `Apply triangulation across data sources and methods`.
- `#21` `title`: `None` -> `[1215, 945, 1645, 1002]`; text `4 Methods Covered`.
- `#22` `text_block`: `[1295, 1057, 2325, 1356]` -> `[1215, 995, 2215, 1098]`; text `Qualitative Ethnography, grounded theory, discourse analysis, thematic coding, participant observation, semi-structured interviews`.
- `#23` `text_block`: `[134, 83, 593, 111]` -> `[1215, 1125, 2215, 1192]`; text `Quantitative Survey design, statistical inference, regression, factor analysis, experimental design, sampling theory`.
- `#24` `text_block`: `[1240, 1218, 2155, 1288]` -> `[1215, 1210, 2200, 1290]`; text `Mixed Methods Sequential / concurrent design, triangulation, QUAL→QUAN / QUAN→QUAL integration, case study with embedded units`.
- `#25` `title`: `[131, 1333, 632, 1394]` -> `[105, 1328, 650, 1395]`; text `5 Course Schedule / 教学进度`.
- `#26` `table`: `[135, 1404, 2339, 2442]` -> `[100, 1398, 2295, 2340]`; text `Wk Theme / 主题 Method Key Reading Task Due 1 What is Interdisciplinary Research? 跨学科研究导论 — Repko & Szostak, Ch.1–2 自我介绍 — 2 Research Questions & Lit...`.
- `#27` `title`: `None` -> `[105, 2375, 590, 2440]`; text `6 Grading / 成绩构成`.
- `#28` `table`: `[128, 2560, 1648, 2940]` -> `[105, 2458, 895, 2798]`; text `Component % Reflection Journals (×4) 20% Fieldwork Report 15% Mini Proposal 30% Presentation 15% Participation 10% Peer Review 10%`.
- `#29` `text_block`: `[140, 2986, 964, 3051]` -> `[105, 2830, 910, 2930]`; text `Mini Proposal: 3000–4000字，含研究问题、文献综述、方法设计、预期贡献。APA 7th / GB/T 7714。`.
- `#30` `title`: `None` -> `[980, 2375, 1470, 2440]`; text `7 Policies / 政策`.
- `#31` `text_block`: `[134, 389, 270, 420]` -> `[990, 2450, 1575, 2492]`; text `考勤: 缺课≥3次平时记0；≥1/3取消资格。`.
- `#32` `text_block`: `[793, 389, 973, 420]` -> `[990, 2492, 1465, 2535]`; text `迟交: 每天扣5%, 超7天记0分。`.
- `#33` `text_block`: `[1083, 2558, 2229, 2744]` -> `[990, 2538, 2215, 2582]`; text `AI Policy: 允许使用AI辅助文献检索与语言润色，但须声明。禁止直接提交AI生成文本。`.
- `#34` `text_block`: `[1083, 2672, 1187, 2707]` -> `[990, 2580, 1660, 2622]`; text `Ethics: 所有涉及人类受试的研究须获得IRB批准。`.
- `#35` `text_block`: `[1383, 389, 1464, 420]` -> `[990, 2620, 1915, 2665]`; text `Citation: APA 7th or GB/T 7714. Plagiarism → failing grade.`.
- `#36` `title`: `None` -> `[990, 2690, 1360, 2750]`; text `8 References`.
- `#37` `text_block`: `[1258, 2850, 1461, 2881]` -> `[990, 2760, 1610, 2795]`; text `[1] Creswell, J. Research Design, 6th ed., Sage`.
- `#38` `text_block`: `[1332, 2884, 1658, 2915]` -> `[990, 2795, 1765, 2832]`; text `[2] Repko & Szostak, Interdisciplinary Research, 4th ed.`.
- `#39` `text_block`: `[1255, 2918, 1496, 2949]` -> `[990, 2832, 1725, 2868]`; text `[3] Saldaña, J. The Coding Manual, 4th ed., Sage`.
- `#40` `text_block`: `[1470, 395, 1732, 420]` -> `[990, 2868, 1845, 2910]`; text `[4] 风笑天 主编，《社会研究方法》，人民大学出版社`.
- `#41` `reference`: `[119, 3088, 2344, 3151]` -> `[100, 2925, 865, 2985]`; text `1 Reflection journals: 800–1000字，回应当周阅读与课堂讨论，中英文均可。`.
- `#42` `reference`: `[1757, 389, 1842, 420]` -> `[870, 2925, 1715, 2985]`; text `2 Fieldwork: 选择一个真实场景进行2–3小时的参与式观察或半结构化访谈，撰写田野笔记与分析报告。`.
- `#43` `reference`: `[197, 470, 486, 507]` -> `[1710, 2925, 2310, 2985]`; text `3 课程网站: Canvas → IDS510 · 所有阅读材料已上传。`.
- `#44` `header`: `None` -> `[105, 3282, 2295, 3315]`; text `Tsinghua University · Institute for Interdisciplinary Studies · IDS 510 Dr. Zhang Yifan & Prof. Emily Hart · Spring 2026 Page 1 of 1`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `6` (`[10, 21, 27, 30, 36, 44]`).
- Existing bbox changes in this pass: `45`.
- Category/type changes in this pass: `0`.
- Order/id changes in this pass: `0`.
- Non-bbox semantic changes recorded in this pass: `0`.

Verification:

- Script: `scripts/fix_education_syllabus036_visual_v621.py`.
- Report: `reports/pdb_education_syllabus036_visual_v621.json`.
- Visual dry-run cover check directory: `cover_audit_education_syllabus036_visual_v621_dry/`.
- Visual dry-run outline check directory: `outline_audit_education_syllabus036_visual_v621_dry/`.
- Visual cover check directory: `cover_audit_education_syllabus036_visual_v621/`.
- Non-cover outline preview directory: `outline_audit_education_syllabus036_visual_v621/`.
- Visual review performed with clean PNG crops and grid overlays for the top, middle, and bottom page regions; formal cover/outline images were inspected after writing.
- Latest token after this repair: `20260612_education_syllabus036_visual_v621`.

## 20260612_finance_invoice017_visual_v622

Scope:

- Case: `05_finance/01_invoice_receipt/invoice_receipt_017`.
- Reason: user reported visible bbox drift in the school fee statement invoice/receipt case. Visual inspection showed the main fee table box extended into the discount table, discount/payment blocks were shifted, and bottom Bank/Refund/Contacts short-line boxes were interleaved with the wrong rows.
- Previous token: `20260612_education_syllabus036_visual_v621`.
- New token: `20260612_finance_invoice017_visual_v622`.
- Files updated: `review_data.json`, `review_data.js`, `index.html`, `GT_REPAIR_LOG.md`.
- Status after repair for this case: `41/41 boxed`, `0 no bbox`, `0 low`.

Case-level bbox changes:

- `#0` `text_block`: `[641, 200, 1187, 406]` -> `[632, 185, 1235, 392]`; text `通知单编号：SHWAS-2025-FEE-00382 打印日期：2025年03月20日 学年：2025-2026 财务部电话：021-6221-8900 ext.201`.
- `#1` `title`: `[1293, 330, 2007, 399]` -> `[1280, 312, 2030, 372]`; text `上海惠灵顿外籍人员子女学校`.
- `#2` `text_block`: `[1326, 390, 1974, 438]` -> `[1285, 368, 2030, 426]`; text `Wellington College International Shanghai`.
- `#3` `title`: `[1235, 438, 2065, 510]` -> `[1238, 418, 2085, 492]`; text `2025-2026学年学杂费缴纳通知单`.
- `#4` `text_block`: `[2113, 200, 2515, 406]` -> `[2085, 185, 2685, 392]`; text `SCHOOL FEE STATEMENT Academic Year 2025-2026 Currency: CNY (RMB) Ref: WCIS/FIN/2025/00382`.
- `#5` `text_block`: `[90, 570, 675, 636]` -> `[88, 552, 690, 595]`; text `Student 学生：Alexander Chen (陈浩然)`.
- `#6` `text_block`: `[90, 630, 576, 696]` -> `[88, 612, 592, 655]`; text `Student ID：WCIS-2023-0382`.
- `#7` `text_block`: `[90, 690, 745, 756]` -> `[88, 672, 760, 715]`; text `Year Group：Year 8 (初一) — Senior School`.
- `#8` `text_block`: `[90, 749, 528, 816]` -> `[88, 732, 555, 775]`; text `House：Benson House`.
- `#9` `text_block`: `[1362, 570, 1884, 636]` -> `[1358, 552, 1888, 595]`; text `Parent 家长：陈建华 / Sarah Chen`.
- `#10` `text_block`: `[1362, 630, 1852, 696]` -> `[1358, 612, 1875, 655]`; text `家庭编号：FAM-2023-00198`.
- `#11` `text_block`: `[1362, 690, 1935, 756]` -> `[1358, 672, 1940, 715]`; text `Email：chen.family@email.com`.
- `#12` `text_block`: `[1362, 749, 1837, 816]` -> `[1358, 732, 1848, 775]`; text `联系电话：+86 138****7291`.
- `#13` `text_block`: `[2316, 570, 2966, 636]` -> `[2312, 552, 3050, 595]`; text `Sponsor 赞助方：中金公司 CICC（雇主支付）`.
- `#14` `text_block`: `[2316, 630, 2854, 696]` -> `[2312, 612, 2925, 655]`; text `赞助比例：学费100% + 杂费50%`.
- `#15` `text_block`: `[2316, 690, 2874, 756]` -> `[2312, 672, 2880, 715]`; text `赞助编号：CICC-EDU-2025-0829`.
- `#16` `text_block`: `[2316, 749, 2754, 816]` -> `[2312, 732, 2765, 775]`; text `赞助有效期：至2026-06-30`.
- `#17` `table`: `[52, 825, 3248, 2249]` -> `[50, 812, 3248, 2065]`; text `序 Fee Item 收费项目 Annual 全年 Term 1 秋 Term 2 春 Term 3 夏 Sponsor 赞助方 Family 家庭 Notes 备注 CORE FEES 核心费用 A. Tuition 学费 1 Senior School Tuition Year 8 高中部学费（含教材、实验室使用） 328,00...`.
- `#18` `title`: `[117, 2280, 811, 2325]` -> `[116, 2088, 825, 2138]`; text `DISCOUNTS & SCHOLARSHIPS 减免与奖学金`.
- `#19` `table`: `[115, 2326, 3185, 2619]` -> `[112, 2162, 3185, 2424]`; text `Employer Sponsorship (CICC) 雇主赞助 学费100% + 杂费类50% -¥377,000.00 按协议比例计算 Sibling Discount 二孩优惠 (5%学费) 妹妹Emily Year 4在读 -¥16,400.00 328,000×5% Early Payment Discount 早缴优惠 ...`.
- `#20` `text_block`: `[99, 2686, 1078, 2740]` -> `[90, 2485, 1160, 2565]`; text `NET PAYABLE 家庭实付总额： 伍拾叁万壹仟壹佰贰拾肆元整`.
- `#21` `text_block`: `[2753, 2668, 3201, 2755]` -> `[2808, 2458, 3198, 2575]`; text `¥131,124.00`.
- `#22` `title`: `[84, 2794, 577, 2839]` -> `[88, 2588, 620, 2652]`; text `PAYMENT SCHEDULE 缴费安排`.
- `#23` `table`: `[82, 2840, 3218, 3120]` -> `[88, 2645, 3188, 2898]`; text `期次 缴费期限 项目 赞助方(CICC) 家庭自付 状态 1st 2025-04-30 Term 1 + 一次性费用 ¥194,850 ¥51,250 待缴 2nd 2025-11-30 Term 2 + Field Trip ¥115,417 ¥54,316 — 3rd 2026-03-31 Term 3 ¥66,733 ¥25,...`.
- `#24` `text_block`: `[84, 3121, 1797, 3163]` -> `[88, 2890, 2200, 2945]`; text `* 逾期缴费将收取每日0.03%滞纳金。逾期超过30天未缴，学校保留取消学位的权利。 * 雇主赞助款由CICC直接汇入学校账户，家庭无需代付。`.
- `#25` `title`: `[84, 3211, 420, 3256]` -> `[88, 2992, 485, 3044]`; text `Bank Details 汇款信息`.
- `#26` `text_block`: `[84, 3277, 834, 3322]` -> `[88, 3062, 900, 3105]`; text `Account Name: Wellington College International Shanghai`.
- `#27` `text_block`: `[84, 3326, 475, 3371]` -> `[88, 3110, 535, 3152]`; text `Bank: HSBC Shanghai Branch`.
- `#28` `text_block`: `[84, 3374, 477, 3384]` -> `[88, 3156, 625, 3198]`; text `A/C: 6231 0188 0002 9382 01`.
- `#29` `text_block`: `[90, 3225, 460, 3280]` -> `[88, 3204, 420, 3245]`; text `SWIFT: HSBCCNSH`.
- `#30` `text_block`: `[90, 3280, 390, 3335]` -> `[88, 3250, 430, 3292]`; text `请备注学生姓名+ID`.
- `#31` `title`: `[1144, 3211, 1499, 3256]` -> `[1142, 2992, 1518, 3044]`; text `Refund Policy 退费政策`.
- `#32` `text_block`: `[1144, 3277, 1603, 3322]` -> `[1142, 3062, 1685, 3105]`; text `· 开学前30天：退90%（扣注册费）`.
- `#33` `text_block`: `[1144, 3326, 1424, 3371]` -> `[1142, 3110, 1525, 3152]`; text `· 开学前15天：退70%`.
- `#34` `text_block`: `[1144, 3374, 1513, 3384]` -> `[1142, 3156, 1670, 3198]`; text `· 开学后：按学期剩余比例退`.
- `#35` `text_block`: `[1150, 3225, 1455, 3280]` -> `[1142, 3204, 1485, 3245]`; text `· 校服/iPad：不退`.
- `#36` `title`: `[2204, 3211, 2478, 3256]` -> `[2202, 2992, 2505, 3044]`; text `Contacts 联系方式`.
- `#37` `text_block`: `[2204, 3277, 2708, 3322]` -> `[2202, 3062, 2815, 3105]`; text `Finance: finance@wellingtoncollege.cn`.
- `#38` `text_block`: `[2204, 3326, 2803, 3371]` -> `[2202, 3110, 2920, 3152]`; text `Admissions: admissions@wellingtoncollege.cn`.
- `#39` `text_block`: `[2204, 3374, 2467, 3384]` -> `[2202, 3156, 2505, 3198]`; text `Tel: 021-6221-8900`.
- `#40` `text_block`: `[2210, 3225, 2810, 3280]` -> `[2202, 3204, 2830, 3245]`; text `Address: 耀华路88号, 浦东新区`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0` (`[]`).
- Existing bbox changes in this pass: `41`.
- Category/type changes in this pass: `0`.
- Order/id changes in this pass: `0`.
- Non-bbox semantic changes recorded in this pass: `0`.

Verification:

- Script: `scripts/fix_finance_invoice017_visual_v622.py`.
- Report: `reports/pdb_finance_invoice017_visual_v622.json`.
- Visual dry-run cover check directory: `cover_audit_finance_invoice017_visual_v622_dry/`.
- Visual dry-run outline check directory: `outline_audit_finance_invoice017_visual_v622_dry/`.
- Visual cover check directory: `cover_audit_finance_invoice017_visual_v622/`.
- Non-cover outline preview directory: `outline_audit_finance_invoice017_visual_v622/`.
- Visual review performed with full-page outline plus top/middle/bottom coordinate-grid crops; formal cover/outline images were inspected after writing.
- Latest token after this repair: `20260612_finance_invoice017_visual_v622`.

## 20260612_academic_technical013_flowdesc_v623

Scope:

- Case: `01_academic/03_technical_report/technical_report_013_Supply_Chain_Analysis`.
- Reason: user reported that the lower `Material Flow (Sankey Diagram Description)` block appeared unannotated. Source HTML contains a visible `<div class="flow-desc">` block, but source GT `layout_dets` and current review data only contained the section title `#15` and omitted the body block.
- Previous token: `20260612_finance_invoice017_visual_v622`.
- New token: `20260612_academic_technical013_flowdesc_v623`.
- Files updated: `review_data.json`, `review_data.js`, `index.html`, `GT_REPAIR_LOG.md`.
- Status after repair for this case: `17/17 boxed`, `0 no bbox`, `0 low`.

Added GT annotation:

- `#16` `text_block`: new bbox `[208, 3692, 2272, 4290]`; text `Material Flow (Sankey Diagram Description) Inbound (Tier-2 to Tier-1): Raw silicon wafers (Taiwan/Korea, 42%) and rare earth metals (China, 28%) flow to semiconductor fabs. Chemical precursors (Japan/Germany, 18%) sup...`.

Case-level bbox changes:

- `#9` `text_block`: `[208, 1414, 2269, 1511]` -> `[208, 1414, 2269, 1566]`; text `Tier-1 suppliers were assessed across 5 dimensions: Quality (defect rate), Delivery (OTD%), Cost (price variance), Responsiveness (lead time), and Sustainability (ESG ...`.
- Existing bbox changes in this pass: `1`.

GT annotation change:

- Added GT annotations in this pass: `1`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0` (`[]`).
- Category/type changes in this pass: `0`.
- Order/id changes in this pass: `0`.
- Non-bbox semantic changes recorded in this pass: `1` (added one missing visible HTML text block).

Verification:

- Script: `scripts/fix_academic_technical013_flowdesc_v623.py`.
- Report: `reports/pdb_academic_technical013_flowdesc_v623.json`.
- Visual dry-run cover check directory: `cover_audit_academic_technical013_flowdesc_v623_dry/`.
- Visual dry-run outline check directory: `outline_audit_academic_technical013_flowdesc_v623_dry/`.
- Visual cover check directory: `cover_audit_academic_technical013_flowdesc_v623/`.
- Non-cover outline preview directory: `outline_audit_academic_technical013_flowdesc_v623/`.
- Visual review performed against the source HTML and clean PNG grid crop; formal cover/outline images were inspected after writing.
- Latest token after this repair: `20260612_academic_technical013_flowdesc_v623`.

## 20260613_academic_patent029_bib_v624

Scope:

- Case: `01_academic/04_patent/patent_029_US_Chip_Architecture`.
- Reason: user reported that a visible patent bibliographic/abstract paragraph near the top of page appeared completely unannotated. Source HTML contains `<div class="bib">`, and source GT `layout_dets` contains a matching `text_block`; current review data had no annotation for it.
- Previous token: `20260612_academic_technical013_flowdesc_v623`.
- New token: `20260613_academic_patent029_bib_v624`.
- Files updated: `review_data.json`, `review_data.js`, `index.html`, `GT_REPAIR_LOG.md`.
- Status after repair for this case: `19/19 boxed`, `0 no bbox`, `0 low`.

Added GT annotation:

- `#4` `text_block`: new bbox `[162, 323, 2318, 621]`; text `(54) HETEROGENEOUS CHIPLET-BASED SYSTEM-ON-PACKAGE WITH SILICON PHOTONIC INTERCONNECT FOR AI INFERENCE ACCELERATION (75) Inventors: Wei Zhang, Shanghai (CN); Priya Patel, Santa Clara, CA (US); Takeshi Mori, Tsukuba (JP) (73) Assignee: NVIDIA Corporation, Sa...`.

Case-level bbox changes:

- Existing bbox changes in this pass: `0`.

GT annotation change:

- Added GT annotations in this pass: `1`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0` (`[]`).
- Category/type changes in this pass: `0`.
- Order/id changes in this pass: `14` (old `#4-#17` shifted to `#5-#18` so the new patent bibliographic/abstract block is in visual reading order).
- Non-bbox semantic changes recorded in this pass: `15` (one added visible text block plus shifted existing annotation indices).

Order/id changes:

- old `#4` -> new `#5` `figure_caption` bbox `[874, 642, 1607, 678]`; text `FIG. 3 — System-on-Package Architecture Block Diagram`.
- old `#5` -> new `#6` `figure_caption` bbox `[202, 718, 2279, 1413]`; text `text{font-size:6px;fill:#333;text-anchor:middle} Advanced Packaging Substrate (CoWoS-L, 65mm × 65mm) Compute Chiplet (TSMC N3E,...`.
- old `#6` -> new `#7` `text_block` bbox `[1268, 1430, 2318, 1508]`; text `[0055] Table 3 compares the present invention with state-of-the-art AI inference accelerators.`.
- old `#7` -> new `#8` `title` bbox `[162, 1447, 606, 1480]`; text `DETAILED DESCRIPTION`.
- old `#8` -> new `#9` `text_block` bbox `[163, 1493, 1468, 1683]`; text `[0052] Referring to FIG. 3, the SoP architecture 300 integrates three heterogeneous chiplet dies on a single CoWoS-L interposer...`.
- old `#9` -> new `#10` `table_caption` bbox `[1268, 1515, 1391, 1551]`; text `TABLE 3`.
- old `#10` -> new `#11` `table` bbox `[1270, 1561, 2316, 1984]`; text `Parameter Accelerator Present Inv. NVIDIA H100 Google TPU v5 AMD MI300X Process node 3nm + 45nm SiPh 4nm 5nm 5nm + 6nm INT8 TOP...`.
- old `#11` -> new `#12` `text_block` bbox `[162, 1690, 2316, 1842]`; text `[0053] Each PE includes a multiply-accumulate (MAC) unit supporting INT8, FP16, and BF16 data types, a local register file of 5...`.
- old `#12` -> new `#13` `text_block` bbox `[162, 1849, 1219, 2039]`; text `[0054] The SPI chiplet 340 is fabricated on GlobalFoundries' 45CLO silicon photonics platform. It integrates 64 micro-ring reso...`.
- old `#13` -> new `#14` `text_block` bbox `[1268, 1989, 2318, 2067]`; text `[0056] FIG. 4 illustrates the cross-sectional view of the hybrid-bonded chiplet stack.`.
- old `#14` -> new `#15` `title` bbox `[162, 2053, 701, 2086]`; text `PERFORMANCE COMPARISON`.
- old `#15` -> new `#16` `figure_caption` bbox `[1573, 2073, 2013, 2107]`; text `FIG. 4 — Packaging Cross-Section`.
- old `#16` -> new `#17` `figure_caption` bbox `[399, 2187, 2122, 2505]`; text `text{font-size:5px;fill:#333;text-anchor:middle} Organic Substrate (12-layer, 45μm L/S) Silicon Interposer (CoWoS-L, 65nm TSV, ...`.
- old `#17` -> new `#18` `header` bbox `[987, 2548, 1494, 2577]`; text `US 12,789,012 B2 Col. 14-16 Sheet 3 of 12`.

Verification:

- Script: `scripts/fix_academic_patent029_bib_v624.py`.
- Report: `reports/pdb_academic_patent029_bib_v624.json`.
- Visual dry-run cover check directory: `cover_audit_academic_patent029_bib_v624_dry/`.
- Visual dry-run outline check directory: `outline_audit_academic_patent029_bib_v624_dry/`.
- Visual cover check directory: `cover_audit_academic_patent029_bib_v624/`.
- Non-cover outline preview directory: `outline_audit_academic_patent029_bib_v624/`.
- Visual review performed against source HTML, source GT, clean PNG top crop, and formal cover/outline images.
- Latest token after this repair: `20260613_academic_patent029_bib_v624`.

## 20260613_academic_research001_refs_v625

Scope:

- Case: `01_academic/05_research_proposal/research_proposal_001_国家自然科学基金面上项目申请书`.
- Reason: user reported that the `八、主要参考文献` section body appeared unannotated. Source HTML contains a visible `<ol class="ref-list">` with eight references, but source GT `layout_dets` and current review data only contained the section title and then a footer block. The existing footer bbox was also visually drifted to the formula area.
- Previous token: `20260613_academic_patent029_bib_v624`.
- New token: `20260613_academic_research001_refs_v625`.
- Files updated: `review_data.json`, `review_data.js`, `index.html`, `GT_REPAIR_LOG.md`.
- Status after repair for this case: `34/34 boxed`, `0 no bbox`, `2 low`.

Added GT annotation:

- `#32` `reference`: new bbox `[374, 13238, 2232, 14268]`; text `1. M. Z. Hasan and C. L. Kane, "Colloquium: Topological insulators," Rev. Mod. Phys. 82, 3045 (2010). 2. I. Sodemann and L. Fu, "Quantum Nonlinear Hall Effect," Phys. Rev. Lett. 115, 216806 (2015). 3. T. Oka and S. Kitamura, "Floquet Engineering of Quantum Materials," Annu. Re...`.

Case-level bbox changes:

- old `#32` -> new `#33` `text_block`: `[472, 3252, 962, 3314]` -> `[740, 14372, 1810, 14425]`; text `国家自然科学基金委员会 | 申请书模板（2027年度）| 第 1 页`.
- Existing bbox changes in this pass: `1`.

GT annotation change:

- Added GT annotations in this pass: `1`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0` (`[]`).
- Category/type changes in this pass: `0`.
- Order/id changes in this pass: `1` (old footer `#32` shifted to `#33` after inserting the references body as `#32`).
- Non-bbox semantic changes recorded in this pass: `2` (one added visible reference block plus shifted existing footer index).

Order/id changes:

- old `#32` -> new `#33` `text_block` bbox `[740, 14372, 1810, 14425]`; text `国家自然科学基金委员会 | 申请书模板（2027年度）| 第 1 页`.

Verification:

- Script: `scripts/fix_academic_research001_refs_v625.py`.
- Report: `reports/pdb_academic_research001_refs_v625.json`.
- Visual dry-run cover check directory: `cover_audit_academic_research001_refs_v625_dry/`.
- Visual dry-run outline check directory: `outline_audit_academic_research001_refs_v625_dry/`.
- Visual cover check directory: `cover_audit_academic_research001_refs_v625/`.
- Non-cover outline preview directory: `outline_audit_academic_research001_refs_v625/`.
- Visual review performed against source HTML, clean PNG bottom grid crop, and dry-run/formal cover/outline crops.
- Latest token after this repair: `20260613_academic_research001_refs_v625`.

## 20260613_academic_research002_refs_v626

Scope:

- Case: `01_academic/05_research_proposal/research_proposal_002_NIH_R01_Grant_Application`.
- Reason: user reported that the `7. References Cited` body was visibly unannotated. A full-dataset scan for explicit reference headings followed by `ol/ul` lists found only this remaining missing-list candidate.
- HTML ambiguity note: this fix is limited to low-ambiguity cases where a reference-like heading is immediately followed by a multi-item ordered/unordered list. General HTML-to-GT conversion can still be ambiguous for decorative text, footnotes, and repeated page furniture, so visual confirmation remains required.
- Previous token: `20260613_academic_research001_refs_v625`.
- New token: `20260613_academic_research002_refs_v626`.
- Files updated: `review_data.json`, `review_data.js`, `index.html`, `GT_REPAIR_LOG.md`.
- Status after repair for this case: `28/28 boxed`, `0 no bbox`, `0 low`.

Added GT annotation:

- `#26` `reference`: new bbox `[314, 11774, 2187, 12670]`; text `1. Siegel RL, et al. Cancer statistics, 2027. CA Cancer J Clin. 2027;77(1):7-30. 2. Canon J, et al. The clinical KRAS(G12C) inhibitor AMG 510 drives anti-tumour immunity. Nature. 2019;575:217-223. 3. Hassan R, et al. Mesothelin-targeted therapies in pancreatic cancer. Lancet Oncol. 2024;25(3):e12...`.

Case-level bbox changes:

- old `#24` -> new `#24` `text_block`: `[1446, 1714, 1548, 1761]` -> `[294, 11310, 2185, 11546]`; text `1 Significance 1 Investigator(s) 2 Innovation 2 Approach 1 Environment`.
- old `#26` -> new `#27` `text_block`: `[1725, 1875, 1824, 1921]` -> `[700, 12750, 1810, 12803]`; text `PHS 398/2590  |  NIH R01 Application  |  PI: Mitchell, S.J.  |  Page 1 of 12`.
- Existing bbox changes in this pass: `2`.

GT annotation change:

- Added GT annotations in this pass: `1`.
- Removed GT annotations in this pass: `0`.
- Added bbox to existing GT annotations: `0` (`[]`).
- Category/type changes in this pass: `0`.
- Order/id changes in this pass: `1` (old footer `#26` shifted to `#27` after inserting the references body as `#26`).
- Non-bbox semantic changes recorded in this pass: `2` (one added visible reference block plus shifted existing footer index).

Order/id changes:

- old `#26` -> new `#27` `text_block` bbox `[700, 12750, 1810, 12803]`; text `PHS 398/2590  |  NIH R01 Application  |  PI: Mitchell, S.J.  |  Page 1 of 12`.

Verification:

- Script: `scripts/fix_academic_research002_refs_v626.py`.
- Report: `reports/pdb_academic_research002_refs_v626.json`.
- Visual dry-run cover check directory: `cover_audit_academic_research002_refs_v626_dry/`.
- Visual dry-run outline check directory: `outline_audit_academic_research002_refs_v626_dry/`.
- Visual cover check directory: `cover_audit_academic_research002_refs_v626/`.
- Non-cover outline preview directory: `outline_audit_academic_research002_refs_v626/`.
- Visual review performed against full-dataset missing-reference scan, clean PNG bottom grid crop, and dry-run/formal cover/outline crops.
- Post-write full-dataset scan for explicit reference heading plus `ol/ul` list omissions: `0` remaining candidates.
- Frontend/cache validation: `http://127.0.0.1:8767/index.html?cb=20260613_academic_research002_refs_v626` serves script URLs `styles.css?20260613_academic_research002_refs_v626`, `review_data.js?20260613_academic_research002_refs_v626`, and `app.js?20260613_academic_research002_refs_v626`; `review_data.js?20260613_academic_research002_refs_v626` reports this case as `28/28 boxed`, `0 no bbox`, `0 low`, with `#26` reference bbox `[314, 11774, 2187, 12670]`.
- Latest token after this repair: `20260613_academic_research002_refs_v626`.

## 20260613_academic_patent008_compare_table_v627

Scope:

- Case: `01_academic/04_patent/patent_008_专利无效宣告请求书`.
- Reason: user reported a possible omission around the lower patent invalidation page. Visual review confirmed the `五、权利要求对比分析` two-column comparison body was not boxed; only the caption, two column headers, and conclusion were annotated.
- Source/semantic note: source HTML implements this comparison as flex `div` columns, not a literal `<table>`, but the visible structure and content are a two-column claim/evidence comparison table.
- Previous token: `20260613_academic_research002_refs_v626`.
- New token: `20260613_academic_patent008_compare_table_v627`.
- Files updated: `review_data.json`, `review_data.js`, `index.html`, `GT_REPAIR_LOG.md`.
- Status after repair for this case: `22/22 boxed`, `0 no bbox`, `0 low`.

Added GT annotation:

- Added GT annotations in this pass: `0`.

Removed GT annotation:

- old `#14` `text_block` bbox `[1670, 2476, 1866, 2509]` removed as duplicate right-column header after expanding `#13` into a full comparison table; text `证据1公开内容`.

Case-level bbox/type/text changes:

- old `#13` -> new `#13`: category `text_block` -> `table`; bbox `[528, 2471, 1870, 2521]` -> `[198, 2460, 2250, 2783]`; old text `涉案专利权利要求1技术特征`; new text `涉案专利权利要求1技术特征 （A）一种微透镜阵列光学元件，包含基底及其表面的微透镜单元阵列； （B）各微透镜单元的面形偏差不大于0.3μm； （C）阵列的占空比大于98%； （D）基底材料为石英玻璃或硼硅酸盐玻璃； （E）微透镜单元的等效焦距为0.5-5.0mm。 证据1公开内容 （A'）Claim 1: a microlens array element comprising a substrate and a plurality of lenslets — 对应特征A； （B'）Col.5 L.32: s...`.
- Existing bbox changes in this pass: `1`.

GT annotation change:

- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `1`.
- Added bbox to existing GT annotations: `0` (`[]`).
- Category/type changes in this pass: `1` (`#13 text_block -> table`).
- Order/id changes in this pass: `8` (old `#15-#22` shifted down by one after removing old `#14`).
- Non-bbox semantic changes recorded in this pass: `10` (converted one text block into a table, replaced its text with full table content, removed one duplicate header, and shifted later ids).

Order/id changes:

- old `#15` -> new `#14` `text_block` bbox `[198, 2801, 2250, 2901]`; text `对比结论：涉案专利权利要求1的全部技术特征A-E均已被证据1相应内容所公开，两者属于相同技术领域，解决相同技术问题，且技术方案实质相同。因此，权利要求1相对于证据1不具备新颖性。`.
- old `#16` -> new `#15` `text_block` bbox `[513, 2933, 785, 2984]`; text `请求人（签章）：`.
- old `#17` -> new `#16` `text_block` bbox `[1696, 2933, 1968, 2984]`; text `代理人（签章）：`.
- old `#18` -> new `#17` `text_block` bbox `[603, 3127, 695, 3173]`; text `签章处`.
- old `#19` -> new `#18` `text_block` bbox `[1786, 3127, 1878, 3173]`; text `签章处`.
- old `#20` -> new `#19` `text_block` bbox `[499, 3309, 1986, 3365]`; text `日期：2025年01月15日`.
- old `#21` -> new `#20` `text_block` bbox `[1677, 3313, 1987, 3362]`; text `日期：2025年01月15日`.
- old `#22` -> new `#21` `header` bbox `[992, 3353, 1490, 3402]`; text `专利无效宣告请求书 第 1 页 / 共 1 页`.

Verification:

- Script: `scripts/fix_academic_patent008_compare_table_v627.py`.
- Report: `reports/pdb_academic_patent008_compare_table_v627.json`.
- Visual dry-run cover check directory: `cover_audit_academic_patent008_compare_table_v627_dry/`.
- Visual dry-run outline check directory: `outline_audit_academic_patent008_compare_table_v627_dry/`.
- Visual cover check directory: `cover_audit_academic_patent008_compare_table_v627/`.
- Non-cover outline preview directory: `outline_audit_academic_patent008_compare_table_v627/`.
- Visual review performed against clean PNG grid crop and dry-run/formal cover/outline crops.
- Frontend/cache validation: `http://127.0.0.1:8767/index.html?cb=20260613_academic_patent008_compare_table_v627` serves script URLs `styles.css?20260613_academic_patent008_compare_table_v627`, `review_data.js?20260613_academic_patent008_compare_table_v627`, and `app.js?20260613_academic_patent008_compare_table_v627`; `review_data.js?20260613_academic_patent008_compare_table_v627` reports this case as `22/22 boxed`, `0 no bbox`, `0 low`, with `#13` table bbox `[198, 2460, 2250, 2783]`.
- Latest token after this repair: `20260613_academic_patent008_compare_table_v627`.

## 20260613_pre_hf_unique_nobbox_v628

Scope:

- Case set: conservative pre-HF no-bbox exact/high-confidence repair across currently loaded review_data.
- Rule: only existing GT annotations with missing/invalid bbox were repaired, and only when HTML DOM text/formula matching was unique, non-duplicate within the case, not already boxed by same text, and not contained inside an already annotated table.
- Previous token: `20260613_academic_patent008_compare_table_v627`.
- New token: `20260613_pre_hf_unique_nobbox_v628`.
- Files updated: `review_data.json`, `review_data.js`, `index.html`, `GT_REPAIR_LOG.md`.
- Changed cases: `8`.
- Existing GT annotations given bbox: `27`.
- Added GT annotations in this pass: `0`.
- Removed GT annotations in this pass: `0`.
- Category/type changes in this pass: `0`.
- Order/id changes in this pass: `0`.
- Non-bbox semantic changes recorded in this pass: `0`.
- Global status after repair: `88389/88636 boxed`, `247 no bbox`, `2012 low`.

Case-level bbox additions:

- Case: `02_education/02_exam_paper/exam_paper_046_数字电子技术`.
  - Status after repair: `104/105 boxed`, `1 no bbox`, `23 low`.
  - Added GT annotations: `0`; removed GT annotations: `0`; existing bbox additions: `1`.
  - `#109` `text_block` bbox `None` -> `[1053, 5025, 1243, 5066]`; score `1.0`; text `Qn+1 = JQ̅n + K̅Qn`.

- Case: `02_education/04_school_notice/school_notice_010_奖学金综合测评通知`.
  - Status after repair: `50/50 boxed`, `0 no bbox`, `6 low`.
  - Added GT annotations: `0`; removed GT annotations: `0`; existing bbox additions: `2`.
  - `#17` `equation_isolated` bbox `None` -> `[887, 1458, 1594, 1502]`; score `1.0`; text `$$S_{\mathrm{quality}} = 0.40 \times D_{\mathrm{moral}} + 0.30 \times D_{\mathrm{ability}} + 0.30 \times D_{\mathrm{physical}} \tag{3}$$`.
  - `#19` `equation_isolated` bbox `None` -> `[820, 1554, 1661, 1683]`; score `0.8904`; text `$$S_{\mathrm{adjusted}} = S_{\mathrm{total}} \times (1 + \alpha \cdot R_{\mathrm{rank}}),\qquad \alpha = \begin{cases} 0.05, & \text{专业人数} \le 40 \ 0.03, & 40 < \text{专业人数} \le ...`.

- Case: `02_education/04_school_notice/school_notice_031_校外实践联合通知材料包`.
  - Status after repair: `87/88 boxed`, `1 no bbox`, `28 low`.
  - Added GT annotations: `0`; removed GT annotations: `0`; existing bbox additions: `1`.
  - `#64` `title` bbox `None` -> `[1288, 2391, 1780, 2431]`; score `1.0`; text `住宿分配表 / Accommodation Arrangement`.

- Case: `02_education/06_lab_report/lab_report_003_Spectrophotometric_Iron_EN`.
  - Status after repair: `58/60 boxed`, `2 no bbox`, `2 low`.
  - Added GT annotations: `0`; removed GT annotations: `0`; existing bbox additions: `3`.
  - `#42` `equation_isolated` bbox `None` -> `[966, 1884, 1957, 1932]`; score `0.9423`; text `$$c_{\mathrm{unk}} = \frac{A_{\mathrm{unk}} - 0.0038}{0.1842} = \frac{0.8734 - 0.0038}{0.1842} = 4.72\,\mathrm{ppm} \tag{3}$$`.
  - `#44` `equation_isolated` bbox `None` -> `[954, 2012, 1968, 2060]`; score `0.9583`; text `$$[\mathrm{Fe}] = \frac{4.72\,\mathrm{mg/L}}{55.845\,\mathrm{g/mol}} \times \left(\frac{1\,\mathrm{g}}{1000\,\mathrm{mg}}\right) = 8.45 \times 10^{-5}\,\mathrm{mol/L} \tag{4}$$`.
  - `#47` `equation_isolated` bbox `None` -> `[960, 2214, 1961, 2261]`; score `0.8889`; text `$$s = \sqrt{\frac{\sum (x_i - \bar{x})^2}{n - 1}} = 0.056\,\mathrm{ppm},\qquad \mathrm{RSD} = \frac{s}{\bar{x}} \times 100\% = 1.19\% \tag{5}$$`.

- Case: `02_education/06_lab_report/lab_report_006_分析化学_滴定实验`.
  - Status after repair: `66/66 boxed`, `0 no bbox`, `9 low`.
  - Added GT annotations: `0`; removed GT annotations: `0`; existing bbox additions: `1`.
  - `#52` `equation_isolated` bbox `None` -> `[776, 10331, 1705, 10384]`; score `0.961`; text `$$\text{相对误差} = \frac{|0.09542 - 0.09550|}{0.09550} \times 100\% = 0.08\%$$`.

- Case: `02_education/06_lab_report/lab_report_035_CV_Denoising`.
  - Status after repair: `55/57 boxed`, `2 no bbox`, `13 low`.
  - Added GT annotations: `0`; removed GT annotations: `0`; existing bbox additions: `2`.
  - `#45` `title` bbox `None` -> `[848, 3409, 1189, 3441]`; score `1.0`; text `§7 Error Analysis 失败案例分析`.
  - `#49` `title` bbox `None` -> `[1547, 2703, 1842, 2735]`; score `1.0`; text `§8 结论与讨论 Conclusions`.

- Case: `09_logistics/01_shipping_label/shipping_label_008_Maersk_Line_-_Container_Shipping_Manifest_集装箱货运清单`.
  - Status after repair: `191/211 boxed`, `20 no bbox`, `0 low`.
  - Added GT annotations: `0`; removed GT annotations: `0`; existing bbox additions: `15`.
  - `#79` `text_block` bbox `None` -> `[3306, 896, 3677, 928]`; score `1.0`; text `20' × 8' × 8'6" (22G1)`.
  - `#81` `text_block` bbox `None` -> `[3542, 934, 3677, 965]`; score `1.0`; text `2,230 kg`.
  - `#83` `text_block` bbox `None` -> `[3525, 971, 3677, 1002]`; score `1.0`; text `28,250 kg`.
  - `#85` `text_block` bbox `None` -> `[3542, 1008, 3677, 1040]`; score `1.0`; text `9,730 kg`.
  - `#91` `text_block` bbox `None` -> `[3306, 1473, 3677, 1505]`; score `1.0`; text `40' × 8' × 9'6" (45G1)`.
  - `#93` `text_block` bbox `None` -> `[3542, 1508, 3677, 1539]`; score `1.0`; text `3,940 kg`.
  - `#95` `text_block` bbox `None` -> `[3525, 1545, 3677, 1577]`; score `1.0`; text `26,740 kg`.
  - `#97` `text_block` bbox `None` -> `[3525, 1583, 3677, 1614]`; score `1.0`; text `10,300 kg`.
  - `#103` `text_block` bbox `None` -> `[3188, 2044, 3678, 2076]`; score `1.0`; text `40' × 8' × 9'6" (45R1) REEFER`.
  - `#105` `text_block` bbox `None` -> `[3542, 2079, 3678, 2110]`; score `1.0`; text `4,800 kg`.
  - `#107` `text_block` bbox `None` -> `[3525, 2116, 3678, 2148]`; score `1.0`; text `27,700 kg`.
  - `#109` `text_block` bbox `None` -> `[3525, 2151, 3678, 2182]`; score `1.0`; text `11,520 kg`.
  - `#120` `text_block` bbox `None` -> `[3543, 2684, 3678, 2716]`; score `1.0`; text `2,360 kg`.
  - `#122` `text_block` bbox `None` -> `[3526, 2722, 3678, 2753]`; score `1.0`; text `28,120 kg`.
  - `#124` `text_block` bbox `None` -> `[3543, 2756, 3678, 2788]`; score `1.0`; text `2,520 kg`.

- Case: `09_logistics/06_bill_of_lading/bill_of_lading_009_散货海运提单_Bulk_Cargo_Ocean_Bill_of_Lading`.
  - Status after repair: `262/262 boxed`, `0 no bbox`, `0 low`.
  - Added GT annotations: `0`; removed GT annotations: `0`; existing bbox additions: `2`.
  - `#258` `text_block` bbox `None` -> `[3312, 152, 3477, 212]`; score `1.0`; text `检验机构 / SURVEYOR`.
  - `#259` `text_block` bbox `None` -> `[3310, 225, 3478, 294]`; score `1.0`; text `SGS Dalian Branch`.

Verification:

- Script: `scripts/fix_pre_hf_unique_nobbox_v628.py`.
- Report: `reports/pre_hf_unique_nobbox_v628.json`.
- Visual dry-run cover check directory: `cover_audit_pre_hf_unique_nobbox_v628_dry/`.
- Visual dry-run outline check directory: `outline_audit_pre_hf_unique_nobbox_v628_dry/`.
- Visual cover check directory: `cover_audit_pre_hf_unique_nobbox_v628/`.
- Non-cover outline preview directory: `outline_audit_pre_hf_unique_nobbox_v628/`.
- Frontend/cache validation should use: `http://127.0.0.1:8767/index.html?cb=20260613_pre_hf_unique_nobbox_v628`.
- Frontend/cache validation completed: `index.html?cb=20260613_pre_hf_unique_nobbox_v628` returns `styles.css?20260613_pre_hf_unique_nobbox_v628`, `review_data.js?20260613_pre_hf_unique_nobbox_v628`, and `app.js?20260613_pre_hf_unique_nobbox_v628`.
- Latest token after this repair: `20260613_pre_hf_unique_nobbox_v628`.

## 20260613_academic_journal_target4_visual_v629

Scope:

- Cases: `01_academic/01_journal_paper/academic_paper_006_Lancet_临床试验`, `01_academic/01_journal_paper/academic_paper_007_PNAS_生态学`, `01_academic/01_journal_paper/academic_paper_009_PRL_粒子物理`, `01_academic/01_journal_paper/academic_paper_021_IEEE_TPAMI`.
- Reason: user reported visible truncation/missing text and misaligned boxes in four journal-paper cases.
- Previous token: `20260613_pre_hf_unique_nobbox_v628`.
- New token: `20260613_academic_journal_target4_visual_v629`.
- Files updated: `review_data.json`, `review_data.js`, `index.html`, `GT_REPAIR_LOG.md`.
- Preview dirs: `cover_audit_academic_journal_target4_visual_v629/`, `outline_audit_academic_journal_target4_visual_v629/`.
- Report: `reports/academic_journal_target4_visual_v629.json`.
- Global status after repair: `88389/88636 boxed`, `247 no bbox`, `2009 low`.

Counts:

- Existing bbox modified: `22`.
- Existing annotation text modified: `3`.
- Added GT annotations: `0`.
- Removed GT annotations: `0`.
- Type/category changes: `0`.
- Reading-order/id changes: `0`.
- Non-bbox semantic changes: `3` (text restored from visible HTML/DOM).

Per-case changes:

- `01_academic/01_journal_paper/academic_paper_006_Lancet_临床试验`
  - Status: `28/28 boxed`, `0 no bbox`, `2 low`.
  - Added GT annotations: `0`; removed GT annotations: `0`; text changes: `1`; bbox changes: `1`.
  - `#6` bbox `[192, 520, 2294, 726]` -> `[197, 519, 2290, 918]`; reason: Expand Summary bbox to include Findings and Interpretation; replace truncated text with complete visible summary.
  - `#6` text changed: old `Summary Background Immune checkpoint inhibitors have transformed the treatment landscape for advanced hepatocellular carcinoma (HCC), yet durable response rates remain modest. Dual checkpoint blockade targeting PD-1 and LAG-3 may enhance antitumour immunity. We aimed to assess...` -> new `Summary Background Immune checkpoint inhibitors have transformed the treatment landscape for advanced hepatocellular carcinoma (HCC), yet durable response rates remain modest. Dual checkpoint blockade targeting PD-1 and LAG-3 may enhance antitumour immunity. We aimed to assess...`.
- `01_academic/01_journal_paper/academic_paper_007_PNAS_生态学`
  - Status: `28/28 boxed`, `0 no bbox`, `1 low`.
  - Added GT annotations: `0`; removed GT annotations: `0`; text changes: `1`; bbox changes: `1`.
  - `#26` bbox `[1267, 2376, 2341, 2555]` -> `[1270, 2376, 2339, 2554]`; reason: Replace partial author-contributions text with full footnotes block including competing interest and data availability.
  - `#26` text changed: old `Author contributions: E.R.H. and P.L.D. designed research; E.R.H., J.-W.Z., and C.A.M.-R. performed research; I.K.B. and D.V.S. contributed data; E.R.H. analysed data; and E.R.H. and P.L.D. wrote the paper.` -> new `Author contributions: E.R.H. and P.L.D. designed research; E.R.H., J.-W.Z., and C.A.M.-R. performed research; I.K.B. and D.V.S. contributed data; E.R.H. and F.N.A.-R. analysed data; and E.R.H. wrote the paper. Competing interest statement: The authors declare no competing inte...`.
- `01_academic/01_journal_paper/academic_paper_009_PRL_粒子物理`
  - Status: `34/34 boxed`, `0 no bbox`, `4 low`.
  - Added GT annotations: `0`; removed GT annotations: `0`; text changes: `1`; bbox changes: `1`.
  - `#30` bbox `[256, 2773, 2224, 2819]` -> `[260, 2774, 2221, 2855]`; reason: Expand Results paragraph bbox to include wrapped second line and restore the complete visible paragraph.
  - `#30` text changed: old `Upper limits at 95% CL on σ × B are set as a function of Z′ mass. For the Sequential Standard Model (SSM) Z′, masses below 5.2 TeV are excluded. For the Z′_ψ model, the exclusion reaches 4.5 TeV.` -> new `Upper limits at 95% CL on σ × B are set as a function of Z′ mass. For the Sequential Standard Model (SSM) Z′, masses below 5.2 TeV are excluded. For the Z′_ψ model, the exclusion reaches 4.1 TeV. These represent improvements of 15-20% over previous CMS results at 13 TeV.`.
- `01_academic/01_journal_paper/academic_paper_021_IEEE_TPAMI`
  - Status: `45/45 boxed`, `0 no bbox`, `3 low`.
  - Added GT annotations: `0`; removed GT annotations: `0`; text changes: `0`; bbox changes: `19`.
  - `#7` bbox `[139, 515, 1658, 555]` -> `[142, 522, 438, 556]`; reason: Tighten Introduction heading.
  - `#9` bbox `[168, 690, 2307, 747]` -> `[171, 693, 861, 724]`; reason: Tighten left-column self-attention sentence.
  - `#11` bbox `[138, 796, 2093, 867]` -> `[142, 798, 1214, 864]`; reason: Tighten left-column DTA complexity paragraph.
  - `#16` bbox `[138, 1116, 1500, 1198]` -> `[142, 1112, 1214, 1193]`; reason: Tighten left-column attention-weight explanation.
  - `#18` bbox `[138, 1247, 2251, 1329]` -> `[142, 1246, 1214, 1330]`; reason: Tighten left-column pyramid paragraph.
  - `#19` bbox `[140, 1338, 2252, 1370]` -> `[142, 1339, 365, 1373]`; reason: Tighten Loss Function heading.
  - `#20` bbox `[168, 1373, 2251, 1416]` -> `[171, 1380, 970, 1411]`; reason: Tighten loss-intro sentence.
  - `#22` bbox `[644, 249, 840, 283]` -> `[158, 1489, 735, 1935]`; reason: Move Algorithm 1 bbox from page header to the actual algorithm block.
  - `#23` bbox `[139, 1961, 1682, 2001]` -> `[142, 1959, 442, 1994]`; reason: Tighten Experiments heading.
  - `#24` bbox `[136, 2008, 1955, 2045]` -> `[142, 2007, 647, 2041]`; reason: Tighten ADE20K subsection heading.
  - `#25` bbox `[255, 2046, 2141, 2100]` -> `[258, 2052, 1099, 2083]`; reason: Tighten Table I caption.
  - `#29` bbox `[432, 594, 2339, 788]` -> `[1267, 594, 2339, 783]`; reason: Move COCO detection table bbox to the right column.
  - `#32` bbox `[137, 876, 2339, 1137]` -> `[1267, 876, 2339, 1133]`; reason: Move NYUv2 depth table bbox to the right column.
  - `#35` bbox `[861, 1226, 2339, 1444]` -> `[1267, 1225, 2339, 1443]`; reason: Move ablation table bbox to the right column.
  - `#38` bbox `[240, 1532, 2344, 1773]` -> `[1267, 1536, 2339, 1757]`; reason: Move cross-task table bbox to the right column.
  - `#41` bbox `[555, 2111, 2252, 2165]` -> `[1267, 2110, 1542, 2144]`; reason: Move Conclusion heading to right-column location.
  - `#42` bbox `[183, 2149, 2343, 2229]` -> `[1267, 2153, 2339, 2219]`; reason: Move conclusion paragraph to right-column location.
  - `#43` bbox `[199, 2228, 1494, 2276]` -> `[1267, 2233, 1491, 2267]`; reason: Move References heading to right-column location.
  - `#44` bbox `[175, 2270, 2156, 2415]` -> `[1267, 2273, 2156, 2415]`; reason: Move references list to right-column location.

Frontend check URL: `http://127.0.0.1:8767/index.html?cb=20260613_academic_journal_target4_visual_v629`.

## Public release naming: puredocbench-gt-bbox-v1.0.0

Scope:

- Reason: public HF/community release names should be stable and readable; internal repair tokens such as `20260613_academic_journal_target4_visual_v629` should remain maintainer provenance only.
- Public annotation version: `puredocbench-gt-bbox-v1.0.0`.
- Internal build/provenance token retained: `20260613_academic_journal_target4_visual_v629`.
- Files updated: `review_data.json`, `review_data.js`, `index.html`, `app.js`, `docs/ANNOTATION_CORRECTIONS.md`, `.github/ISSUE_TEMPLATE/annotation_error.yml`, `scripts/package_hf_gt_release.py`, `GT_REPAIR_LOG.md`.
- HF package directory generated: `dist/hf_gt_bbox/puredocbench-gt-bbox-v1.0.0/`.
- Latest pointer generated: `dist/hf_gt_bbox/latest/`.

Counts:

- Added GT annotations: `0`.
- Removed GT annotations: `0`.
- Existing bbox modified: `0`.
- Type/category changes: `0`.
- Reading-order/id changes: `0`.
- Non-bbox semantic changes to GT annotations: `0`.

Notes:

- `annotation_version` in packaged HF manifests now uses the public version.
- `internal_build_token` in packaged HF manifests and exported correction patches keeps the repair provenance trace.
- Review app data label now displays `PureDocBench GT BBox v1.0.0`; the internal token is available only as hover/debug metadata.

## GitHub community review entry

Scope:

- Reason: expose the public GT review/correction workflow from the GitHub repository instead of relying on a local-only `127.0.0.1` link.
- Files updated: `README.md`, `docs/README_ZH.md`, `docs/ANNOTATION_CORRECTIONS.md`, `.github/ISSUE_TEMPLATE/config.yml`, `GT_REPAIR_LOG.md`.
- Public review app cache tag: `puredocbench_gt_bbox_v1_0_0_ui`.
- Public annotation version: `puredocbench-gt-bbox-v1.0.0`.

Counts:

- Added GT annotations: `0`.
- Removed GT annotations: `0`.
- Existing bbox modified: `0`.
- Type/category changes: `0`.
- Reading-order/id changes: `0`.
- Non-bbox semantic changes to GT annotations: `0`.

Notes:

- README and Chinese README now include a Community GT Review section with local launch instructions.
- `docs/ANNOTATION_CORRECTIONS.md` now includes the review app entry and correction issue link.
- GitHub issue template config now exposes quick links to the review app and correction guide from the New Issue page.

## GitHub README updates section

Scope:

- Reason: add a date-based `Updates` area to the GitHub-facing README so public GT/review/evaluation changes can be announced clearly over time.
- Files updated: `README.md`, `docs/README_ZH.md`, `GT_REPAIR_LOG.md`.
- Public annotation version referenced: `puredocbench-gt-bbox-v1.0.0`.

Counts:

- Added GT annotations: `0`.
- Removed GT annotations: `0`.
- Existing bbox modified: `0`.
- Type/category changes: `0`.
- Reading-order/id changes: `0`.
- Non-bbox semantic changes to GT annotations: `0`.

Notes:

- English README now has `## Updates` near the top.
- Chinese README now has `## 更新` near the top.
- Current update entries mention the public GT bbox version, review/correction workflow, and HF versioned GT package layout.

## Review app web updates entry

Scope:

- Reason: make the review app webpage itself expose the public `Updates`, `Submit Correction`, and `Guide` entry points, instead of only documenting them in GitHub README files.
- Files updated: `review_data.json`, `review_data.js`, `index.html`, `styles.css`, `GT_REPAIR_LOG.md`.
- Public review app cache tag: `puredocbench_gt_bbox_v1_0_0_web_updates`.
- Public annotation version referenced: `puredocbench-gt-bbox-v1.0.0`.

Counts:

- Added GT annotations: `0`.
- Removed GT annotations: `0`.
- Existing bbox modified: `0`.
- Type/category changes: `0`.
- Reading-order/id changes: `0`.
- Non-bbox semantic changes to GT annotations: `0`.

Notes:

- Top toolbar now links to `Updates`, `Submit Correction`, and `Guide`.
- Right correction panel now links directly to the GitHub correction issue template.
- `review_data` meta now records `public_review_app_cache_token`, `public_review_app_updates_url`, and `public_review_app_correction_issue_url`.

## GitHub public website publish hygiene

Scope:

- Reason: prepare a small GitHub-facing update without accidentally publishing local visual-audit artifacts or stale review-app cache links.
- Files updated: `.gitignore`, `README.md`, `docs/README_ZH.md`, `docs/ANNOTATION_CORRECTIONS.md`, `.github/ISSUE_TEMPLATE/config.yml`, `GT_REPAIR_LOG.md`.
- Public review app cache tag: `puredocbench_gt_bbox_v1_0_0_web_updates`.
- Public annotation version referenced: `puredocbench-gt-bbox-v1.0.0`.

Counts:

- Added GT annotations: `0`.
- Removed GT annotations: `0`.
- Existing bbox modified: `0`.
- Type/category changes: `0`.
- Reading-order/id changes: `0`.
- Non-bbox semantic changes to GT annotations: `0`.

Notes:

- README, Chinese README, correction guide, and GitHub issue contact links now use the same public review-app cache token as `index.html`.
- `.gitignore` now excludes generated `cover_audit_*`, `outline_audit_*`, `cover_residual_*`, `tmp_*`, and `review_data.before_*.json` artifacts under the review app directory.

## GitHub Pages review app image loading

Scope:

- Reason: make the public GitHub Pages review app usable without committing the full clean image release to GitHub.
- Files updated: `review_data.json`, `review_data.js`, `app.js`, `README.md`, `docs/README_ZH.md`, `docs/ANNOTATION_CORRECTIONS.md`, `GT_REPAIR_LOG.md`.
- Public review app cache tag: `puredocbench_gt_bbox_v1_0_0_web_updates`.
- Public annotation version referenced: `puredocbench-gt-bbox-v1.0.0`.

Counts:

- Added GT annotations: `0`.
- Removed GT annotations: `0`.
- Existing bbox modified: `0`.
- Type/category changes: `0`.
- Reading-order/id changes: `0`.
- Non-bbox semantic changes to GT annotations: `0`.

Notes:

- `app.js` now keeps local `assets/images/...` paths by default for `file://`, `localhost`, and `127.0.0.1` launches.
- GitHub Pages can resolve `assets/images/...` through `public_image_base_url` or an `imageBase=` query parameter when an unpacked clean-image mirror is available.
- `review_data` public metadata now uses `puredocbench-gt-bbox-v1.0.0` as the community-facing annotation version and no longer exposes local absolute release paths.
- README, Chinese README, and the correction guide now include a direct public review app link.
- The review app now shows a visible warning instead of silently blanking the page image when the image source is unavailable.
