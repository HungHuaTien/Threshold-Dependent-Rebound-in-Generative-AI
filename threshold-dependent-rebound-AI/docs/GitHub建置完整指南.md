# GitHub Repository 建置指南

## 📦 **Repository 結構**

```
threshold-dependent-rebound-AI/
├── README.md                           # 專案說明(中英文)
├── LICENSE                             # 授權(建議MIT或CC BY 4.0)
├── data/                               # 數據資料夾
│   ├── raw/                           # 原始數據
│   │   ├── pca_pc1_timeseries.csv
│   │   ├── LLM_Trends_Weekly_2024_2026.csv
│   │   └── Non-AI-Python-3.csv
│   ├── processed/                     # 處理後數據
│   │   └── (可選)
│   └── README.md                      # 數據說明
├── code/                               # 分析程式碼
│   ├── 01_data_collection/           # 數據收集
│   ├── 02_analysis/                  # 主要分析
│   │   ├── chow_test.py
│   │   ├── run_B1_B2_analysis.py
│   │   ├── run_B2_Control_Group_analysis.py
│   │   └── run_ITS_analysis.py
│   ├── 03_visualization/             # 圖表生成
│   │   └── generate_figures.py
│   ├── 04_abm_simulation/            # ABM模擬
│   │   └── abm_policy_simulation.py
│   └── requirements.txt              # Python套件需求
├── results/                            # 分析結果
│   ├── tables/                        # 表格
│   │   ├── B1_Newey_West_Results.txt
│   │   ├── B2_Control_Group_Results.csv
│   │   └── ITS_Analysis_Results.txt
│   ├── figures/                       # 圖表
│   │   ├── 圖_B2_Control_Group對比.png
│   │   └── (其他圖表)
│   └── README.md                      # 結果說明
├── paper/                              # 論文相關
│   ├── manuscript.pdf                 # 論文PDF
│   ├── supplementary_materials.pdf    # 補充材料
│   └── README.md
└── docs/                               # 文檔
    ├── methodology.md                 # 方法說明
    ├── data_dictionary.md             # 數據字典
    └── replication_guide.md           # 複製指南
```

---

## 📝 **核心檔案內容**

### **1. README.md** (主要說明)

```markdown
# Threshold-Dependent Rebound in Generative AI
# 生成式AI產業的門檻依賴型反彈

[![DOI](https://img.shields.io/badge/DOI-pending-blue)](論文DOI)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

**Evidence from Adoption Proxies and Energy Policy Implications**  
**基於採用代理變數的實證與能源政策意涵**

## Overview | 概述

This repository contains replication materials for our study examining threshold-dependent rebound effects in the generative AI industry. We employ a dual-event quasi-natural experiment design to demonstrate that AI demand exhibits discrete jumps rather than continuous elasticity responses.

本儲存庫包含論文「生成式AI產業的門檻依賴型反彈」的完整複製材料。我們採用雙事件準自然實驗設計,證明AI需求展現離散跳躍而非連續彈性反應。

## Key Findings | 主要發現

- ✅ Market attention exhibits **10-11σ discrete jumps** following technological shocks
- ✅ Developer adoption behavior shows **3-4σ structural breaks** 
- ✅ **11 robustness checks** confirm core conclusions
- ✅ Control group analysis rules out Python ecosystem confounding

---

- ✅ 市場關注度展現**10-11σ離散跳躍**
- ✅ 開發者採用行為呈現**3-4σ結構斷裂**
- ✅ **11項穩健性檢驗**確認核心結論
- ✅ 對照組分析排除Python生態系統混淆

## Repository Contents | 儲存庫內容

- `data/` - Weekly Google Trends and PyPI download data (2024-2026)
- `code/` - Analysis scripts (Chow Test, Newey-West, ITS, ABM)
- `results/` - Tables, figures, and statistical outputs
- `paper/` - Manuscript and supplementary materials

## Reproducibility | 可複製性

All analysis code is provided with detailed comments. To replicate:

1. Clone this repository
2. Install dependencies: `pip install -r code/requirements.txt`
3. Run analysis scripts in `code/02_analysis/`
4. Results will be generated in `results/`

## Citation | 引用

If you use this data or code, please cite:

```bibtex
@article{tian2026threshold,
  title={Threshold-Dependent Rebound in Generative AI: Evidence from Adoption Proxies and Energy Policy Implications},
  author={Tian, Honghua},
  journal={Energy Policy},
  year={2026},
  note={Manuscript submitted for publication}
}
```

## Contact | 聯繫

**Honghua Tian (田弘華)**  
Department of Economics, Shih Hsin University  
Email: francis@mail.shu.edu.tw

## License | 授權

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

Data: CC BY 4.0  
Code: MIT License
```

---

### **2. data/README.md** (數據說明)

```markdown
# Data Documentation | 數據文檔

## Overview | 概述

This folder contains weekly time series data from January 2024 to January 2026 (110 weeks).

本資料夾包含2024年1月至2026年1月的週度時間序列數據(110週)。

## Files | 檔案

### `pca_pc1_timeseries.csv`
**Description**: Google Trends principal component (PC1) time series  
**來源**: Google Trends搜尋指數主成分分析

**Columns**:
- `date`: Week start date (YYYY-MM-DD)
- `pc1_score`: Standardized PC1 score

**Sample size**: 110 weeks  
**Time range**: 2023-12-31 to 2026-01-25

---

### `LLM_Trends_Weekly_2024_2026.csv`
**Description**: Raw Google Trends data for 7 AI-related keywords  
**來源**: Google Trends原始關鍵字數據

**Columns**:
- `date`: Week start date
- `ChatGPT API`: Search volume (0-100)
- `LLM pricing`: Search volume
- `API cost`: Search volume
- `Hugging Face`: Search volume
- `DeepSeek`: Search volume
- `Ollama`: Search volume
- `AI agent`: Search volume

**Sample size**: 110 weeks

---

### `Non-AI-Python-3.csv`
**Description**: PyPI download counts for control group packages  
**來源**: Google Cloud BigQuery PyPI下載統計

**Columns**:
- `week`: Week start date
- `package_name`: Package name (numpy, pandas, requests)
- `downloads`: Weekly download count

**Sample size**: 324 records (108 weeks × 3 packages)  
**Source**: Google Cloud BigQuery `bigquery-public-data.pypi.file_downloads`

## Data Collection | 數據收集

### Google Trends
- **Source**: https://trends.google.com
- **Geography**: Worldwide
- **Category**: All categories
- **Search type**: Web search

### PyPI Downloads
- **Source**: Google Cloud BigQuery
- **Dataset**: `bigquery-public-data.pypi.file_downloads`
- **Filter**: `details.installer.name = 'pip'`

## Events | 事件

### DeepSeek-R1
- **Date**: 2025-01-20
- **Data point**: 2025-01-26 (week 57, index 56)
- **Type**: Price-driven shock (94.5% price reduction)

### GPT-5
- **Date**: 2025-08-07
- **Data point**: 2025-08-10 (week 85, index 84)
- **Type**: Capability-driven shock

## License | 授權

Data is provided under CC BY 4.0 license.  
數據採用CC BY 4.0授權。

**Attribution**: If you use this data, please cite our paper.
```

---

### **3. code/requirements.txt**

```txt
pandas>=1.5.0
numpy>=1.23.0
scipy>=1.9.0
statsmodels>=0.14.0
matplotlib>=3.6.0
seaborn>=0.12.0
scikit-learn>=1.2.0
```

---

### **4. LICENSE** (建議MIT)

```
MIT License

Copyright (c) 2026 Honghua Tian

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🚀 **建置步驟**

### **Step 1: 在GitHub建立新repository**

1. 登入GitHub
2. 點擊右上角 "+" → "New repository"
3. Repository名稱: `threshold-dependent-rebound-AI`
4. Description: `Replication materials for "Threshold-Dependent Rebound in Generative AI"`
5. 選擇 **Public**
6. 勾選 "Add a README file"
7. 選擇 License: **MIT License**
8. 點擊 "Create repository"

### **Step 2: 上傳檔案**

#### **方法A: 透過網頁介面** (簡單)

1. 在repository頁面點擊 "Add file" → "Upload files"
2. 拖曳整個資料夾結構
3. 填寫commit message: "Initial commit: replication materials"
4. 點擊 "Commit changes"

#### **方法B: 透過Git指令** (進階)

```bash
# Clone repository
git clone https://github.com/你的使用者名稱/threshold-dependent-rebound-AI.git
cd threshold-dependent-rebound-AI

# 建立資料夾結構
mkdir -p data/raw data/processed code/02_analysis results/tables results/figures paper

# 複製檔案到對應位置
# (將您的檔案複製到相應資料夾)

# Commit and push
git add .
git commit -m "Initial commit: replication materials"
git push origin main
```

---

## ✅ **檢查清單**

```
□ 建立GitHub repository
□ 上傳README.md (主要說明)
□ 上傳data/資料夾 (3個CSV檔案)
□ 上傳data/README.md (數據說明)
□ 上傳code/資料夾 (分析程式碼)
□ 上傳code/requirements.txt
□ 上傳results/資料夾 (分析結果)
□ 上傳LICENSE
□ 確認所有連結正常
□ 在論文中加入GitHub連結
□ 完成!
```

---

## 📋 **論文中如何引用GitHub**

在論文的**資料可得性聲明 (Data Availability Statement)**:

```markdown
## 資料可得性聲明

本研究使用的所有數據、分析程式碼、以及複製材料均已公開於GitHub儲存庫:
https://github.com/[您的使用者名稱]/threshold-dependent-rebound-AI

數據採用CC BY 4.0授權，程式碼採用MIT授權。
```

**英文版**:
```markdown
## Data Availability Statement

All data, analysis code, and replication materials for this study are 
publicly available at: 
https://github.com/[您的使用者名稱]/threshold-dependent-rebound-AI

Data is licensed under CC BY 4.0, code under MIT License.
```

---

**我已準備好所有GitHub需要的內容!需要我協助什麼嗎?** 🚀
