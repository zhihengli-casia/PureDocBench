# PureDocBench 中文说明

<p align="center">
  <strong>源标注可追溯的文档解析评测基准</strong><br>
  1,475 个页面 · 10 个领域 · 66 个子类 · 4,425 张 Clean / Digital / Real 配对图像
</p>

<p align="center">
  <a href="https://huggingface.co/datasets/zhihengli-casia/puredocbench">数据集</a> |
  <a href="https://zhihengli-casia.github.io/PureDocBench/leaderboard.html">交互榜单</a> |
  <a href="../results/">结果文件</a> |
  <a href="ANNOTATION_CORRECTIONS.md">GT 标注 Review</a> |
  <a href="../README.md">English README</a>
</p>

PureDocBench 评测文本、公式、表格和阅读顺序。文档图像由 HTML/CSS 源文件生成，结构化标注也从同一份源文件中提取。Clean、Digital、Real 三轨共享页面内容和参考标注，用于比较不同图像条件下的解析表现。

<p align="center">
  <a href="../assets/figures/teaser.png"><img src="../assets/figures/teaser.png" alt="PureDocBench 十类文档与三轨配对图像概览" width="100%"></a>
</p>

## 更新

- **2026-09-26**：更新为 **58 个模型**的三轨结果与四项组件指标，提供 53 个模型的十领域结果；同步新版概览、数据构造、模型比较、组件分析和七个错误案例图。[结果文件](../results/) · [交互榜单](https://zhihengli-casia.github.io/PureDocBench/leaderboard.html)。
- **2026-09-21**：收录 WeVisDoc 作者提交的结果，原始文件保留在[社区结果归档](../data/README.md)。
- **当前 GT**：稳定别名为 `puredocbench-gt-latest`，精确版本记录在 [Hugging Face `gt/latest.json`](https://huggingface.co/datasets/zhihengli-casia/puredocbench/blob/main/gt/latest.json)。

## 模型结果

当前结果覆盖 **13 个多阶段专用模型、19 个端到端专用模型和 26 个通用视觉语言模型**，包括截至 2026 年 9 月的近期发布模型。[完整主表](../README.md#main-leaderboard)展示 Clean、Digital、Real 的 Overall 及三轨均值 Avg₃，并为模型提供官方链接和发布日期。

[交互榜单](https://zhihengli-casia.github.io/PureDocBench/leaderboard.html)支持按模型搜索、类别筛选和各项指标排序，默认展示上述 58 个模型。社区筛选项另保留 NaviDC-OCR 的作者报告结果。[三轨结果](../results/leaderboard.csv)、[组件指标](../results/components.csv)和[领域指标](../results/category_components.csv)均可下载。

Overall = [100 × (1 − TextEdit) + FormulaCDM + TableTEDS] / 3；阅读顺序单独评测。历史提交及来源说明保留在 [data/](../data/README.md)。

### 准确率与鲁棒性

三轨均分与相对 Clean 的分数损失展示各模型在不同图像条件下的表现，负损失表示分数提升。

<p align="center">
  <a href="../assets/figures/model_rankings.png"><img src="../assets/figures/model_rankings.png" alt="58 模型的准确率与三轨鲁棒性比较" width="100%"></a>
</p>

### 组件表现

各项指标取三轨平均。文本和阅读顺序转换为 100 × (1 − Edit)，公式使用 CDM，表格使用 TEDS，数值越高表示表现越好。不同模型在不同组件上具有优势。

<p align="center">
  <a href="../assets/figures/component_profiles.png"><img src="../assets/figures/component_profiles.png" alt="58 模型的文本、公式、表格及阅读顺序表现" width="100%"></a>
</p>

## 数据构造

HTML/CSS 源文档同时提供页面图像和结构化标注。渲染、数字变换与物理重拍构成三轨配对输入，自动检查与人工交叉复核用于检查标注质量。

<p align="center">
  <a href="../assets/figures/data_construction.png"><img src="../assets/figures/data_construction.png" alt="PureDocBench 数据构造与源标注流程" width="100%"></a>
</p>

## 错误案例

七个案例展示配料遗漏、图版标签缺失、百分比篡改、金额表述不一致、表格单元格缺失、下标误写为除法，以及希腊符号误识别为数字。原始页面与局部放大图定位错误，并对照参考内容和模型输出。

<p align="center">
  <a href="../assets/figures/case_studies.png"><img src="../assets/figures/case_studies.png" alt="七个典型解析错误及原图、放大细节、参考内容和模型输出" width="100%"></a>
</p>

<details>
<summary><strong>退化设计与标注示例</strong></summary>

15 种退化操作涵盖打印、纸张、采集和数字处理，10 种场景组合模拟不同文档采集条件。

<p align="center">
  <a href="../assets/figures/fig_degradation_ops.png"><img src="../assets/figures/fig_degradation_ops.png" alt="15 种退化操作" width="100%"></a>
  <a href="../assets/figures/fig_degradation_scenarios.png"><img src="../assets/figures/fig_degradation_scenarios.png" alt="10 种退化场景" width="100%"></a>
  <a href="../assets/figures/gt_coordinate_overlay_examples.png"><img src="../assets/figures/gt_coordinate_overlay_examples.png" alt="学术文档、专利和学费单的 GT 坐标示例" width="100%"></a>
</p>

</details>

## 数据下载

完整数据托管在 Hugging Face：

```bash
shasum -a 256 -c SHA256SUMS.txt
cat pdb_full.tar.part-* | tar -xf -
```

也可以用仓库里的脚本校验分片和解压后的 release：

```bash
python scripts/verify_split_archive.py /path/to/downloaded/files

python scripts/validate_release_manifest.py \
  --release-root /path/to/puredocbench \
  --manifest manifests/release_manifest_candidate_1475.csv
```

## GT 标注 Review

公开命名统一使用稳定标识：GT 归档为 `puredocbench-gt-latest`，Review UI 为
`puredocbench-review-v1`。精确更新时间只保留在 Hugging Face 元数据和更新记录中，
不再写入公开 URL 或目录名。可以使用 review app 检查标注并导出 correction patch。

- 公开 Review app：
  [Open GT Review App](https://zhihengli-casia.github.io/PureDocBench/review/)
- 仓库文件：
  [`review/index.html`](../review/index.html)
- 修正说明：
  [docs/ANNOTATION_CORRECTIONS.md](ANNOTATION_CORRECTIONS.md)
- 提交修正：
  [New GT annotation correction issue](https://github.com/zhihengli-casia/PureDocBench/issues/new?template=annotation_error.yml)（表单支持中文或英文）

本地启动：

```bash
mkdir -p review/assets
ln -s /path/to/puredocbench/images/clean review/assets/images
python3 -m http.server 8767 --directory review
```

打开：

```text
http://127.0.0.1:8767/index.html
```

静态 app URL：

```text
https://zhihengli-casia.github.io/PureDocBench/review/
```

GitHub 仓库不包含完整图片。网页端视觉检查时，点击 `Load Images`，
选择下载后的 `images/clean` 文件夹；本地启动也可以使用上面的软链方式。

## GT 坐标补齐

如果需要空间标注，可以从 HTML/CSS 源重新渲染并补齐 clean 轨道坐标：

```bash
python scripts/add_gt_coordinates.py \
  --release-root /path/to/puredocbench \
  --manifest manifests/release_manifest_candidate_1475.csv \
  --in-place \
  --include-bbox \
  --include-coordinate-system \
  --report coordinate_report.json

python scripts/validate_release_manifest.py \
  --release-root /path/to/puredocbench \
  --manifest manifests/release_manifest_candidate_1475.csv \
  --require-coordinates \
  --require-bbox
```

脚本会按 OmniDocBench GT 约定为每个 `layout_dets` 元素写入矩形 `poly`。
`poly` 是 clean 图像像素坐标，顺序为左上、右上、右下、左下：
`[x1, y1, x2, y1, x2, y2, x1, y2]`。如需额外写入派生的
`bbox: [x1, y1, x2, y2]`，可以加 `--include-bbox`；正式坐标字段以
`poly` 为准。如果本机还没有 Playwright 浏览器，先运行
`playwright install chromium`；也可以加 `--browser-channel chrome` 使用本机
Chrome。

## 推理与评分接口

仓库提供统一 CLI，支持任意模型命令模板、轻量评分，以及导出到 OmniDocBench 官方 evaluator：

```bash
pip install -e .

puredocbench infer \
  --images /path/to/puredocbench/images/clean \
  --output-dir predictions/my_model_clean \
  --command-template 'python my_model_infer.py --image {image} --out {output}'

puredocbench score \
  --release-root /path/to/puredocbench \
  --manifest manifests/release_manifest_candidate_1475.csv \
  --pred-dir predictions/my_model_clean \
  --track clean \
  --out-dir scores/my_model_clean
```

完整说明见 [docs/INFERENCE_SCORING.md](INFERENCE_SCORING.md)。

## 许可

- 数据集按 **CC BY 4.0** 发布，见 [LICENSE_DATA](../LICENSE_DATA)。
- 代码按仓库 [LICENSE](../LICENSE) 发布。
- 本仓库不重新分发模型权重。

## 引用

```bibtex
@misc{puredocbench,
  title        = {How Far Is Document Parsing from Solved? PureDocBench: A Source-Traceable Benchmark across Clean, Degraded, and Real-World Settings},
  author       = {Li, Zhiheng and collaborators},
  year         = {2026},
  howpublished = {\url{https://github.com/zhihengli-casia/puredocbench}},
  note         = {Dataset and benchmark release}
}
```
