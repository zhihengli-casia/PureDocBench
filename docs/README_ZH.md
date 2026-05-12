# PureDocBench 中文说明

<p align="center">
  <strong>文档解析离真正解决还有多远？</strong><br>
  PureDocBench 是一个面向 OCR 与文档解析的源可追踪基准，覆盖清洁版、数字退化、真实退化三条评测轨道。
</p>

<p align="center">
  <a href="https://huggingface.co/datasets/zhihengli-casia/puredocbench">Hugging Face 数据集</a> |
  <a href="https://arxiv.org/abs/2605.07492">arXiv 论文</a> |
  <a href="../README.md">英文说明</a>
</p>

PureDocBench 的文档图像由 HTML/CSS 源文件渲染生成，真值标注从同一份结构化源中抽取。这样可以减少后验人工标注噪声，并让文本、公式、表格、阅读顺序等结构化元素都能被稳定评测。

<p align="center">
  <img src="../assets/figures/fig3_data_overview_final.png" alt="PureDocBench 数据概览" width="92%">
</p>

## 数据概览

| 项目 | 数量 |
|---|---:|
| 官方页面 | 1,475 |
| 官方图像 | 4,425 |
| 文档大类 | 10 |
| 细粒度子类 | 66 |
| 图像轨道 | 清洁版 / 数字退化 / 真实退化 |
| 评分结构 | 文本、公式、表格、阅读顺序 |

## 论文主表

论文主表评测了 40 个系统，包括流水线式专家模型、端到端文档解析模型和通用视觉语言模型。每条轨道报告 Overall、TextEdit、FormulaCDM、TableTEDS 和 ROEdit；Avg3 是三条轨道 Overall 的平均。

<p align="center">
  <img src="../assets/figures/table_main_leaderboard.png" alt="PureDocBench 三轨 leaderboard 主表" width="98%">
</p>

## 诊断结果

诊断图展示了当前模型的主要瓶颈：公式识别仍然是最大缺口，真实退化会比数字退化更明显地改变模型排序。

<p align="center">
  <img src="../assets/figures/fig_diagnostic_panels.png" alt="诊断图" width="96%">
</p>

## 案例分析

以下四个案例均来自论文原图，覆盖学术、商务、金融和证照场景。它们展示了聚合分数容易隐藏的问题，包括公式语义丢失、阅读顺序错误、批注污染、表格结构错误、字符级错误和印章区域遗漏。

### 案例 1：学术文档

<p align="center">
  <img src="../assets/figures/fig_case_study_academic.png" alt="学术文档案例" width="96%">
</p>

### 案例 2：商务表格

<p align="center">
  <img src="../assets/figures/fig_case_study_business.png" alt="商务表格案例" width="96%">
</p>

### 案例 3：金融精算报告

<p align="center">
  <img src="../assets/figures/fig_case_study_actuarial.png" alt="金融精算报告案例" width="96%">
</p>

### 案例 4：中文产品质量证书

<p align="center">
  <img src="../assets/figures/fig_case_study_certificate.png" alt="中文产品质量证书案例" width="96%">
</p>

## 附录精选图

附录中保留了退化设计和分领域表现，用于说明基准的可控性与可复现性。

<p align="center">
  <img src="../assets/figures/fig_degradation_ops.png" alt="退化算子" width="96%">
</p>

<p align="center">
  <img src="../assets/figures/fig_degradation_scenarios.png" alt="退化场景" width="96%">
</p>

<p align="center">
  <img src="../assets/figures/fig_per_category_overview.png" alt="分领域结果概览" width="92%">
</p>

## 数据下载

完整数据托管在 Hugging Face：

```bash
shasum -a 256 -c SHA256SUMS.txt
cat pdb_full.tar.part-* | tar -xf -
```

也可以用仓库里的脚本校验分片和解压后的发布包：

```bash
python scripts/verify_split_archive.py /path/to/downloaded/files

python scripts/validate_release_manifest.py \
  --release-root /path/to/puredocbench-v1.0 \
  --manifest manifests/release_manifest_candidate_1475.csv
```

## 推理与评分接口

仓库提供统一命令行工具，支持任意模型命令模板、快速轻量评分，以及调用 OmniDocBench 官方评测器。`puredocbench score` 用于快速检查；需要和平台的 CDM/TEDS 口径对齐时，使用 `puredocbench score-omnidocbench` 并指定 OmniDocBench 代码目录：

```bash
pip install -e .

puredocbench infer \
  --images /path/to/puredocbench-v1.0/images/clean \
  --output-dir predictions/my_model_clean \
  --command-template 'python my_model_infer.py --image {image} --out {output}'

puredocbench score \
  --release-root /path/to/puredocbench-v1.0 \
  --manifest manifests/release_manifest_candidate_1475.csv \
  --pred-dir predictions/my_model_clean \
  --track clean \
  --limit 20 \
  --out-dir scores/my_model_clean

puredocbench score-omnidocbench \
  --release-root /path/to/puredocbench-v1.0 \
  --manifest manifests/release_manifest_candidate_1475.csv \
  --pred-dir predictions/my_model_clean \
  --track clean \
  --omnidocbench-root /path/to/OmniDocBench \
  --out-dir omnidocbench_scores/my_model_clean
```

完整说明见 [docs/INFERENCE_SCORING.md](INFERENCE_SCORING.md)。

## 许可

- 数据集按 **CC BY 4.0** 发布，见 [LICENSE_DATA](../LICENSE_DATA)。
- 代码按仓库 [LICENSE](../LICENSE) 发布。
- 本仓库不重新分发模型权重。

## 引用

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
