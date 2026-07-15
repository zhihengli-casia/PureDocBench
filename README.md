# PureDocBench

<p align="center">
  <strong>How far is document parsing from solved?</strong><br>
  A source-traceable benchmark for OCR and document parsing across clean, digitally degraded, and real-degraded document settings.
</p>

<p align="center">
  <a href="https://huggingface.co/datasets/zhihengli-casia/puredocbench"><img alt="Hugging Face Dataset" src="https://img.shields.io/badge/Dataset-Hugging%20Face-yellow"></a>
  <a href="LICENSE_DATA"><img alt="Data License" src="https://img.shields.io/badge/Data-CC%20BY%204.0-lightgrey"></a>
  <a href="LICENSE"><img alt="Code License" src="https://img.shields.io/badge/Code-MIT-green"></a>
  <a href="paper/PureDocBench-paper.pdf"><img alt="Paper" src="https://img.shields.io/badge/Paper-PDF-red"></a>
</p>

<p align="center">
  <a href="docs/README_ZH.md">中文说明</a> |
  <a href="https://huggingface.co/datasets/zhihengli-casia/puredocbench">Dataset</a> |
  <a href="paper/PureDocBench-paper.pdf">Paper</a> |
  <a href="docs/ANNOTATION_CORRECTIONS.md">GT Review & Corrections</a>
</p>

PureDocBench uses HTML/CSS document sources as hidden anchors: each page is rendered into images and annotated from the same structured source. This gives a benchmark where text, tables, formulas, captions, and reading order can be scored with less post-hoc annotation noise.

PureDocBench 是一个源可追踪的 OCR / 文档解析 benchmark。数据由 HTML/CSS 源文件渲染而来，GT 标注从同源结构中抽取，覆盖 clean、digital-degraded、real-degraded 三条图像轨道。

## Updates

- **2026-06-14**: Updated GT annotations and opened a [GT Review app](docs/ANNOTATION_CORRECTIONS.md) for community corrections. Release ID: `puredocbench-2026-06-14`.
- **2026-05-08**: Initial public release of PureDocBench, including the paper PDF and full dataset on [Hugging Face](https://huggingface.co/datasets/zhihengli-casia/puredocbench). Release ID: `puredocbench-2026-05-08`.

## GT Annotation Examples

The examples below show colored coordinate boxes over clean rendered pages from an academic paper, a patent form, and a tuition invoice.

<p align="center">
  <img src="assets/figures/gt_coordinate_overlay_examples.png" alt="PureDocBench GT coordinate annotation examples" width="98%">
</p>

<p align="center">
  <img src="assets/figures/fig3_data_overview_final.png" alt="PureDocBench overview" width="92%">
</p>

## At A Glance

| Item | Count |
|---|---:|
| Official pages | 1,475 |
| Official images | 4,425 |
| Top-level domains | 10 |
| Fine-grained subcategories | 66 |
| Image tracks | clean, digital-degraded, real-degraded |
| Scored structures | text, formulas, tables, reading order |

## Main Leaderboard

The paper evaluates 40 systems across pipeline specialists, end-to-end document parsers, and general-purpose VLMs. Table 2 is the main leaderboard: each track reports Overall, TextEdit, FormulaCDM, TableTEDS, and ROEdit; Avg3 averages the three track Overall scores.

<p align="center">
  <a href="https://zhihengli-casia.github.io/PureDocBench/leaderboard.html"><strong>Open the interactive sortable leaderboard ↗</strong></a>
</p>

<table style="width:100%; border-collapse: collapse;">
  <caption>Table 2: Three-track leaderboard on PureDocBench</caption>
  <thead>
    <tr>
      <th rowspan="2">Model</th>
      <th rowspan="2">Params</th>
      <th colspan="5">Clean</th>
      <th colspan="5">Digital Degraded</th>
      <th colspan="5">Real Degraded</th>
      <th rowspan="2">Avg<sub>3</sub>&#x2191;</th>
    </tr>
    <tr>
      <th>Overall&#x2191;</th>
      <th>Text<sup>Edit</sup>&#x2193;</th>
      <th>Formula<sup>CDM</sup>&#x2191;</th>
      <th>Table<sup>TEDS</sup>&#x2191;</th>
      <th>RO<sup>Edit</sup>&#x2193;</th>
      <th>Overall&#x2191;</th>
      <th>Text<sup>Edit</sup>&#x2193;</th>
      <th>Formula<sup>CDM</sup>&#x2191;</th>
      <th>Table<sup>TEDS</sup>&#x2191;</th>
      <th>RO<sup>Edit</sup>&#x2193;</th>
      <th>Overall&#x2191;</th>
      <th>Text<sup>Edit</sup>&#x2193;</th>
      <th>Formula<sup>CDM</sup>&#x2191;</th>
      <th>Table<sup>TEDS</sup>&#x2191;</th>
      <th>RO<sup>Edit</sup>&#x2193;</th>
    </tr>
  </thead>
  <tbody>
    <tr><th colspan="18" align="left"><em>Pipeline / Multi-stage Specialists</em></th></tr>
    <tr><td><a href="https://github.com/rednote-hilab/dots.mocr">DotsMOCR</a></td><td>3B</td><td>76.27</td><td><strong>0.151</strong></td><td>66.23</td><td>77.65</td><td><strong>0.273</strong></td><td>73.16</td><td><strong>0.198</strong></td><td>64.32</td><td>74.95</td><td><strong>0.309</strong></td><td>61.73</td><td>0.312</td><td>54.39</td><td>61.97</td><td>0.393</td><td>70.39</td></tr>
    <tr><td><a href="https://github.com/bytedance/Dolphin">Dolphin-v2</a></td><td>3B</td><td>65.90</td><td>0.342</td><td>59.80</td><td>72.12</td><td>0.429</td><td>60.24</td><td>0.393</td><td>52.20</td><td>67.86</td><td>0.461</td><td>44.92</td><td>0.553</td><td>39.98</td><td>50.04</td><td>0.558</td><td>57.02</td></tr>
    <tr><td><a href="https://github.com/Yuliang-Liu/MonkeyOCR">MonkeyOCR-pro-3B</a></td><td>3B</td><td>62.23</td><td>0.346</td><td>48.46</td><td>72.83</td><td>0.492</td><td>57.40</td><td>0.397</td><td>45.57</td><td>66.32</td><td>0.526</td><td>46.49</td><td>0.511</td><td>38.18</td><td>52.43</td><td>0.600</td><td>55.37</td></tr>
    <tr><td><a href="https://github.com/TencentCloudADP/youtu-parsing">YouTu-Parsing</a></td><td>2B</td><td>75.02</td><td>0.230</td><td>67.34</td><td>80.74</td><td>0.358</td><td>69.66</td><td>0.270</td><td>61.44</td><td>74.49</td><td>0.388</td><td>60.29</td><td>0.360</td><td>52.20</td><td>64.69</td><td>0.430</td><td>68.32</td></tr>
    <tr><td><a href="https://github.com/opendatalab/MinerU">MinerU2.5-Pro</a></td><td>1.2B</td><td>75.87</td><td>0.222</td><td>65.14</td><td><ins>84.68</ins></td><td>0.346</td><td>71.77</td><td>0.272</td><td>61.79</td><td>80.73</td><td>0.378</td><td>62.56</td><td>0.375</td><td>52.70</td><td>72.47</td><td>0.446</td><td>70.07</td></tr>
    <tr><td><a href="https://github.com/opendatalab/MinerU">MinerU2.5</a></td><td>1.2B</td><td>74.90</td><td><ins>0.184</ins></td><td>62.08</td><td>81.04</td><td><ins>0.327</ins></td><td>68.92</td><td>0.245</td><td>56.99</td><td>74.24</td><td>0.374</td><td>59.15</td><td>0.370</td><td>49.01</td><td>65.41</td><td>0.446</td><td>67.66</td></tr>
    <tr><td><a href="https://github.com/Yuliang-Liu/MonkeyOCR">MonkeyOCR-pro-1.2B</a></td><td>1.2B</td><td>61.09</td><td>0.358</td><td>47.43</td><td>71.60</td><td>0.498</td><td>55.72</td><td>0.416</td><td>43.91</td><td>64.83</td><td>0.529</td><td>43.82</td><td>0.556</td><td>36.94</td><td>50.07</td><td>0.609</td><td>53.54</td></tr>
    <tr><td><a href="https://github.com/PaddlePaddle/PaddleOCR">PaddleOCR-VL-1.5</a></td><td>0.9B</td><td>73.01</td><td>0.266</td><td>63.53</td><td>82.12</td><td>0.428</td><td>66.73</td><td>0.339</td><td>58.03</td><td>76.07</td><td>0.478</td><td>60.50</td><td>0.398</td><td>54.00</td><td>67.33</td><td>0.510</td><td>66.75</td></tr>
    <tr><td><a href="https://github.com/zai-org/GLM-OCR">GLM-OCR</a></td><td>0.9B</td><td>68.65</td><td>0.314</td><td>57.89</td><td>79.44</td><td>0.470</td><td>63.06</td><td>0.383</td><td>53.23</td><td>74.21</td><td>0.520</td><td>58.31</td><td>0.433</td><td>50.34</td><td>67.83</td><td>0.543</td><td>63.34</td></tr>
    <tr><td><a href="https://github.com/Topdu/OpenOCR">OpenOCR</a></td><td>0.1B</td><td>32.70</td><td>0.354</td><td>33.50</td><td>0.00</td><td>0.507</td><td>30.03</td><td>0.410</td><td>31.09</td><td>0.00</td><td>0.541</td><td>25.73</td><td>0.486</td><td>25.81</td><td>0.00</td><td>0.591</td><td>29.49</td></tr>
    <tr><th colspan="18" align="left"><em>End-to-End Specialists</em></th></tr>
    <tr><td><a href="https://github.com/allenai/olmocr">olmOCR-2-7B</a></td><td>7B</td><td>69.36</td><td>0.284</td><td>56.89</td><td>79.59</td><td>0.358</td><td>65.87</td><td>0.318</td><td>54.57</td><td>74.81</td><td>0.378</td><td>56.10</td><td>0.417</td><td>48.79</td><td>61.25</td><td>0.439</td><td>63.78</td></tr>
    <tr><td><a href="https://github.com/allenai/olmocr">olmOCR-7B</a></td><td>7B</td><td>62.56</td><td>0.388</td><td>58.69</td><td>67.77</td><td>0.466</td><td>57.84</td><td>0.436</td><td>55.44</td><td>61.66</td><td>0.499</td><td>47.30</td><td>0.542</td><td>46.26</td><td>49.80</td><td>0.568</td><td>55.90</td></tr>
    <tr><td><a href="https://github.com/DocTron-hub/FD-RL">FD-RL</a></td><td>4B</td><td><strong>78.38</strong></td><td>0.193</td><td><ins>68.21</ins></td><td><strong>86.22</strong></td><td>0.334</td><td><ins>76.33</ins></td><td><ins>0.214</ins></td><td>67.16</td><td><strong>83.22</strong></td><td><ins>0.350</ins></td><td>67.04</td><td>0.298</td><td>58.82</td><td>72.08</td><td>0.391</td><td><ins>73.92</ins></td></tr>
    <tr><td><a href="https://github.com/alibaba/Logics-Parsing">Logics-Parsing-v2</a></td><td>4B</td><td><ins>76.35</ins></td><td>0.213</td><td>67.67</td><td>82.67</td><td>0.342</td><td>73.85</td><td>0.248</td><td>67.33</td><td>79.02</td><td>0.375</td><td>67.64</td><td>0.304</td><td>61.65</td><td>71.64</td><td>0.416</td><td>72.61</td></tr>
    <tr><td><a href="https://github.com/DocTron-hub/OCRVerse">OCRVerse</a></td><td>4B</td><td>73.18</td><td>0.273</td><td>63.78</td><td>83.09</td><td>0.393</td><td>71.36</td><td>0.302</td><td>63.95</td><td>80.36</td><td>0.415</td><td>63.66</td><td>0.363</td><td>57.03</td><td>70.30</td><td>0.452</td><td>69.40</td></tr>
    <tr><td><a href="https://github.com/baidubce/Qianfan-VL">Qianfan-OCR</a></td><td>4B</td><td>57.22</td><td>0.370</td><td>49.79</td><td>58.83</td><td>0.443</td><td>50.85</td><td>0.438</td><td>44.41</td><td>51.96</td><td>0.485</td><td>45.06</td><td>0.494</td><td>39.08</td><td>45.53</td><td>0.509</td><td>51.04</td></tr>
    <tr><td><a href="https://github.com/NanoNets/Nanonets-OCR2">Nanonets-OCR2</a></td><td>3B</td><td>64.83</td><td>0.254</td><td>44.98</td><td>74.94</td><td>0.377</td><td>61.23</td><td>0.307</td><td>45.40</td><td>68.97</td><td>0.408</td><td>49.03</td><td>0.435</td><td>35.50</td><td>55.09</td><td>0.468</td><td>58.36</td></tr>
    <tr><td><a href="https://github.com/deepseek-ai/DeepSeek-OCR-2">DeepSeek-OCR-2</a></td><td>3B</td><td>55.53</td><td>0.354</td><td>46.00</td><td>56.01</td><td>0.466</td><td>49.41</td><td>0.412</td><td>40.78</td><td>48.67</td><td>0.493</td><td>43.60</td><td>0.486</td><td>37.30</td><td>42.06</td><td>0.533</td><td>49.51</td></tr>
    <tr><td><a href="https://github.com/chatdoc-com/OCRFlux">OCRFlux-3B</a></td><td>3B</td><td>47.14</td><td>0.454</td><td>38.35</td><td>48.46</td><td>0.424</td><td>41.82</td><td>0.486</td><td>31.90</td><td>42.17</td><td>0.437</td><td>37.21</td><td>0.559</td><td>32.65</td><td>34.87</td><td>0.491</td><td>42.06</td></tr>
    <tr><td><a href="https://github.com/deepseek-ai/DeepSeek-OCR">DeepSeek-OCR</a></td><td>3B</td><td>53.50</td><td>0.419</td><td>45.39</td><td>57.06</td><td>0.514</td><td>46.95</td><td>0.478</td><td>39.99</td><td>48.64</td><td>0.548</td><td>40.48</td><td>0.537</td><td>34.04</td><td>41.12</td><td>0.575</td><td>46.98</td></tr>
    <tr><td><a href="https://github.com/rednote-hilab/dots.ocr">dots.ocr</a></td><td>2.9B</td><td>72.01</td><td>0.248</td><td>61.37</td><td>79.51</td><td>0.379</td><td>65.95</td><td>0.307</td><td>56.67</td><td>71.86</td><td>0.417</td><td>55.68</td><td>0.403</td><td>47.70</td><td>59.63</td><td>0.467</td><td>64.55</td></tr>
    <tr><td><a href="https://github.com/FireRedTeam/FireRed-OCR">FireRed-OCR</a></td><td>2B</td><td>70.81</td><td>0.287</td><td>63.86</td><td>77.23</td><td>0.396</td><td>68.49</td><td>0.319</td><td>62.64</td><td>74.77</td><td>0.422</td><td>57.42</td><td>0.415</td><td>51.60</td><td>62.16</td><td>0.474</td><td>65.57</td></tr>
    <tr><td><a href="https://github.com/Tencent-Hunyuan/HunyuanOCR">HunyuanOCR</a></td><td>1B</td><td>65.61</td><td>0.269</td><td>55.74</td><td>68.02</td><td>0.382</td><td>61.49</td><td>0.308</td><td>51.62</td><td>63.68</td><td>0.400</td><td>54.58</td><td>0.421</td><td>48.30</td><td>57.54</td><td>0.459</td><td>60.56</td></tr>
    <tr><td><a href="https://github.com/Topdu/OpenOCR">UniRec-0.1B</a></td><td>0.1B</td><td>58.91</td><td>0.422</td><td>51.31</td><td>67.60</td><td>0.526</td><td>52.42</td><td>0.501</td><td>48.37</td><td>59.04</td><td>0.578</td><td>34.44</td><td>0.658</td><td>30.97</td><td>38.16</td><td>0.685</td><td>48.59</td></tr>
    <tr><td><a href="https://github.com/Topdu/OpenOCR">OpenDoc-0.1B</a></td><td>0.1B</td><td>60.28</td><td>0.411</td><td>53.09</td><td>68.86</td><td>0.519</td><td>52.46</td><td>0.501</td><td>48.41</td><td>59.04</td><td>0.577</td><td>44.27</td><td>0.547</td><td>38.46</td><td>49.06</td><td>0.603</td><td>52.00</td></tr>
    <tr><th colspan="18" align="left"><em>General VLMs: Qwen3.5</em></th></tr>
    <tr><td><a href="https://github.com/QwenLM/Qwen3.5">Qwen3.5-397B-A17B</a></td><td>397B/17B</td><td>69.12</td><td>0.233</td><td>65.26</td><td>65.40</td><td>0.366</td><td>68.34</td><td>0.244</td><td>63.91</td><td>65.53</td><td>0.376</td><td>62.70</td><td>0.287</td><td>60.70</td><td>56.12</td><td>0.399</td><td>66.72</td></tr>
    <tr><td><a href="https://github.com/QwenLM/Qwen3.5">Qwen3.5-122B-A10B</a></td><td>122B/10B</td><td>76.14</td><td>0.226</td><td>67.96</td><td>83.03</td><td>0.375</td><td><strong>76.34</strong></td><td>0.220</td><td><ins>67.82</ins></td><td><ins>83.21</ins></td><td>0.366</td><td><ins>69.85</ins></td><td><strong>0.281</strong></td><td>62.19</td><td><ins>75.44</ins></td><td>0.401</td><td><strong>74.11</strong></td></tr>
    <tr><td><a href="https://github.com/QwenLM/Qwen3.5">Qwen3.5-35B-A3B</a></td><td>35B/3B</td><td>68.40</td><td>0.232</td><td>64.94</td><td>63.45</td><td>0.374</td><td>68.04</td><td>0.245</td><td>64.78</td><td>63.86</td><td>0.379</td><td>60.59</td><td>0.310</td><td>59.68</td><td>53.07</td><td>0.419</td><td>65.68</td></tr>
    <tr><td><a href="https://github.com/QwenLM/Qwen3.5">Qwen3.5-27B</a></td><td>27B</td><td>72.07</td><td>0.227</td><td>66.36</td><td>72.51</td><td>0.362</td><td>70.73</td><td>0.236</td><td>64.61</td><td>71.17</td><td>0.367</td><td>65.92</td><td><ins>0.283</ins></td><td>61.23</td><td>64.82</td><td><ins>0.390</ins></td><td>69.57</td></tr>
    <tr><td><a href="https://github.com/QwenLM/Qwen3.5">Qwen3.5-9B</a></td><td>9B</td><td>73.87</td><td>0.254</td><td>67.60</td><td>79.39</td><td>0.388</td><td>73.34</td><td>0.260</td><td>67.00</td><td>79.01</td><td>0.396</td><td>65.45</td><td>0.332</td><td>60.91</td><td>68.59</td><td>0.437</td><td>70.89</td></tr>
    <tr><td><a href="https://github.com/QwenLM/Qwen3.5">Qwen3.5-4B</a></td><td>4B</td><td>73.45</td><td>0.276</td><td><strong>69.96</strong></td><td>78.02</td><td>0.410</td><td>72.53</td><td>0.281</td><td><strong>68.88</strong></td><td>76.78</td><td>0.412</td><td>63.47</td><td>0.380</td><td>61.27</td><td>67.17</td><td>0.477</td><td>69.82</td></tr>
    <tr><td><a href="https://github.com/QwenLM/Qwen3.5">Qwen3.5-2B</a></td><td>2B</td><td>66.24</td><td>0.348</td><td>62.84</td><td>70.70</td><td>0.473</td><td>65.22</td><td>0.350</td><td>58.30</td><td>72.36</td><td>0.477</td><td>55.92</td><td>0.440</td><td>50.99</td><td>60.79</td><td>0.521</td><td>62.46</td></tr>
    <tr><td><a href="https://github.com/QwenLM/Qwen3.5">Qwen3.5-0.8B</a></td><td>0.8B</td><td>60.77</td><td>0.376</td><td>54.39</td><td>65.54</td><td>0.500</td><td>59.28</td><td>0.386</td><td>54.22</td><td>62.22</td><td>0.510</td><td>47.93</td><td>0.498</td><td>44.60</td><td>48.98</td><td>0.557</td><td>55.99</td></tr>
    <tr><th colspan="18" align="left"><em>General VLMs: Qwen3-VL</em></th></tr>
    <tr><td><a href="https://github.com/QwenLM/Qwen3-VL">Qwen3-VL-8B</a></td><td>8B</td><td>72.44</td><td>0.261</td><td>65.10</td><td>78.35</td><td>0.411</td><td>72.03</td><td>0.266</td><td>64.88</td><td>77.82</td><td>0.409</td><td>62.73</td><td>0.342</td><td>55.55</td><td>66.81</td><td>0.448</td><td>69.07</td></tr>
    <tr><td><a href="https://github.com/QwenLM/Qwen3-VL">Qwen3-VL-4B</a></td><td>4B</td><td>72.04</td><td>0.262</td><td>65.10</td><td>77.17</td><td>0.418</td><td>70.84</td><td>0.272</td><td>63.54</td><td>76.13</td><td>0.425</td><td>59.61</td><td>0.378</td><td>55.15</td><td>61.47</td><td>0.480</td><td>67.50</td></tr>
    <tr><td><a href="https://github.com/QwenLM/Qwen3-VL">Qwen3-VL-2B</a></td><td>2B</td><td>66.37</td><td>0.300</td><td>59.04</td><td>70.03</td><td>0.439</td><td>65.81</td><td>0.314</td><td>60.25</td><td>68.52</td><td>0.448</td><td>54.09</td><td>0.428</td><td>51.05</td><td>53.99</td><td>0.511</td><td>62.09</td></tr>
    <tr><th colspan="18" align="left"><em>General VLMs: Other</em></th></tr>
    <tr><td><a href="https://github.com/MoonshotAI/Kimi-K2">Kimi K2.6</a></td><td>1T/32B</td><td>72.32</td><td>0.303</td><td>66.93</td><td>80.30</td><td>0.466</td><td>69.95</td><td>0.322</td><td>64.69</td><td>77.31</td><td>0.475</td><td>68.02</td><td>0.335</td><td><ins>62.44</ins></td><td>75.14</td><td>0.481</td><td>70.10</td></tr>
    <tr><td><a href="https://github.com/stepfun-ai/Step3-VL-10B">Step3-VL</a></td><td>10B</td><td>53.65</td><td>0.496</td><td>53.41</td><td>57.16</td><td>0.509</td><td>52.74</td><td>0.516</td><td>53.62</td><td>56.15</td><td>0.529</td><td>45.06</td><td>0.579</td><td>45.42</td><td>47.66</td><td>0.573</td><td>50.48</td></tr>
    <tr><td><a href="https://github.com/OpenBMB/MiniCPM-V">MiniCPM-V-4.5</a></td><td>8B</td><td>51.81</td><td>0.439</td><td>45.97</td><td>53.36</td><td>0.481</td><td>49.38</td><td>0.461</td><td>42.79</td><td>51.50</td><td>0.489</td><td>37.59</td><td>0.583</td><td>32.01</td><td>39.06</td><td>0.552</td><td>46.26</td></tr>
    <tr><td><a href="https://github.com/googleapis/python-genai">Gemini-3.1-Pro</a></td><td>---</td><td>70.04</td><td>0.306</td><td>65.63</td><td>75.08</td><td>0.409</td><td>69.28</td><td>0.322</td><td>65.81</td><td>74.24</td><td>0.417</td><td><strong>71.98</strong></td><td>0.300</td><td><strong>68.62</strong></td><td><strong>77.26</strong></td><td><strong>0.386</strong></td><td>70.43</td></tr>
  </tbody>
</table>

<strong>Bold</strong> marks the best score in each column; <ins>underlined</ins> marks the runner-up. GitHub README tables cannot run sorting scripts, so use the <a href="https://zhihengli-casia.github.io/PureDocBench/leaderboard.html">interactive leaderboard</a> to sort any metric in either direction.

## Diagnostics

The diagnostic panel shows where current systems still have headroom. Formula recognition is the largest single bottleneck, and real degradation changes rankings more sharply than digital degradation.

<p align="center">
  <img src="assets/figures/fig_diagnostic_panels.png" alt="Diagnostic panels" width="96%">
</p>

## Case Studies

The four case studies below are all taken from the paper. They show failures that aggregate scores can hide: notation loss, reading-order mistakes, annotation contamination, table-structure errors, character-level corruption, and missing visual authentication cues.

### Case 1: Academic

<p align="center">
  <img src="assets/figures/fig_case_study_academic.png" alt="Case study 1: academic structured lab report" width="96%">
</p>

### Case 2: Business

<p align="center">
  <img src="assets/figures/fig_case_study_business.png" alt="Case study 2: business product specification table" width="96%">
</p>

### Case 3: Finance

<p align="center">
  <img src="assets/figures/fig_case_study_actuarial.png" alt="Case study 3: finance actuarial valuation report" width="96%">
</p>

### Case 4: Certificate

<p align="center">
  <img src="assets/figures/fig_case_study_certificate.png" alt="Case study 4: Chinese product quality certificate" width="96%">
</p>

## Appendix Highlights

The appendix documents the degradation design, per-category behavior, and source-validity checks used to make the benchmark reproducible.

<p align="center">
  <img src="assets/figures/fig_degradation_ops.png" alt="Degradation operations" width="96%">
</p>

<p align="center">
  <img src="assets/figures/fig_degradation_scenarios.png" alt="Degradation scenarios" width="96%">
</p>

<p align="center">
  <img src="assets/figures/fig_per_category_overview.png" alt="Per-category overview" width="92%">
</p>

<p align="center">
  <img src="assets/figures/fig_source_validity_dashboard.png" alt="Source-validity dashboard" width="96%">
</p>

## Download

The full image/GT/HTML release is hosted on Hugging Face:

```bash
# After downloading all files from Hugging Face:
shasum -a 256 -c SHA256SUMS.txt
cat pdb_full.tar.part-* | tar -xf -
```

Verify the split archive and reconstructed release:

```bash
python scripts/verify_split_archive.py /path/to/downloaded/files

python scripts/validate_release_manifest.py \
  --release-root /path/to/puredocbench-2026-06-14 \
  --manifest manifests/release_manifest_candidate_1475.csv
```

## GT Review

Current release ID: `puredocbench-2026-06-14`.
Use the review app to inspect annotations and export correction patches.

- Public review app:
  [Open GT Review App](https://zhihengli-casia.github.io/PureDocBench/review/gt_case_compare_all_fixed7/index.html?cb=puredocbench_2026_06_14_clean_ui)
- Repository file:
  [`review/gt_case_compare_all_fixed7/index.html`](review/gt_case_compare_all_fixed7/index.html)
- Correction guide:
  [docs/ANNOTATION_CORRECTIONS.md](docs/ANNOTATION_CORRECTIONS.md)
- Submit a correction:
  [New GT annotation correction issue](https://github.com/zhihengli-casia/PureDocBench/issues/new?template=annotation_error.yml) (English or Chinese)

Local launch:

```bash
mkdir -p review/gt_case_compare_all_fixed7/assets
ln -s /path/to/puredocbench-2026-06-14/images/clean review/gt_case_compare_all_fixed7/assets/images
python3 -m http.server 8767 --directory review/gt_case_compare_all_fixed7
```

Open:

```text
http://127.0.0.1:8767/index.html?cb=puredocbench_2026_06_14_clean_ui
```

Static app URL:

```text
https://zhihengli-casia.github.io/PureDocBench/review/gt_case_compare_all_fixed7/index.html?cb=puredocbench_2026_06_14_clean_ui
```

The GitHub repository does not include the full image release. For visual
review on GitHub Pages, click `Load Images` and select the downloaded
`images/clean` folder. Local launch can also use the symlink above.

## GT Coordinates

If you need spatial labels, regenerate clean-render coordinates from the
HTML/CSS sources:

```bash
python scripts/add_gt_coordinates.py \
  --release-root /path/to/puredocbench-2026-06-14 \
  --manifest manifests/release_manifest_candidate_1475.csv \
  --in-place \
  --include-bbox \
  --include-coordinate-system \
  --report coordinate_report.json

python scripts/validate_release_manifest.py \
  --release-root /path/to/puredocbench-2026-06-14 \
  --manifest manifests/release_manifest_candidate_1475.csv \
  --require-coordinates \
  --require-bbox
```

The script follows the OmniDocBench GT convention and adds a rectangular `poly`
field to each `layout_dets` item. `poly` is a flat list of clean-image pixel
coordinates in top-left, top-right, bottom-right, bottom-left order:
`[x1, y1, x2, y1, x2, y2, x1, y2]`. A derived `bbox: [x1, y1, x2, y2]` can also
be written with `--include-bbox`, but `poly` is the primary coordinate field.
Run `playwright install chromium` first if the Playwright browser is not
installed, or pass `--browser-channel chrome` to use a local Chrome
installation.

## Inference And Scoring

PureDocBench includes a public CLI for model-agnostic inference, lightweight scoring, and OmniDocBench export:

```bash
pip install -e .

puredocbench infer \
  --images /path/to/puredocbench-2026-06-14/images/clean \
  --output-dir predictions/my_model_clean \
  --command-template 'python my_model_infer.py --image {image} --out {output}'

puredocbench score \
  --release-root /path/to/puredocbench-2026-06-14 \
  --manifest manifests/release_manifest_candidate_1475.csv \
  --pred-dir predictions/my_model_clean \
  --track clean \
  --out-dir scores/my_model_clean
```

See [docs/INFERENCE_SCORING.md](docs/INFERENCE_SCORING.md) for the full interface and OmniDocBench export path.

## Repository Contents

```text
manifests/                         Release and sample manifests
metadata/                          Dataset card and Croissant metadata
scripts/                           Rendering, degradation, validation, leaderboard tools
puredocbench/                      Public inference, scoring, and OmniDocBench export CLI
model_inference/                   Sanitized model inference configs and runners
supplemental_inference_scoring/    API/local inference and scoring utilities
assets/figures/                    Figures from the paper
paper/                             Paper PDF
```

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

Render one HTML page:

```bash
python scripts/render_single_image.py \
  --html /path/to/page.html \
  --out /path/to/page.png \
  --dpi 300
```

Apply a deterministic degradation profile:

```bash
python scripts/apply_degradation_ablation.py \
  --input /path/to/clean_images \
  --output /path/to/degraded_images \
  --profile full_medium
```

## License

- Dataset assets are released under **CC BY 4.0**; see [LICENSE_DATA](LICENSE_DATA).
- Code in this repository is released under the license in [LICENSE](LICENSE).
- Model weights are not redistributed.

## Citation

```bibtex
@misc{puredocbench,
  title        = {How Far Is Document Parsing from Solved? PureDocBench: A Source-Traceable Benchmark across Clean, Degraded, and Real-World Settings},
  author       = {Li, Zhiheng and collaborators},
  year         = {2026},
  howpublished = {\url{https://github.com/zhihengli-casia/puredocbench}},
  note         = {Dataset and benchmark release}
}
```
