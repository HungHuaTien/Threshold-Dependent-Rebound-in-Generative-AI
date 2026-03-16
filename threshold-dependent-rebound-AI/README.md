# Threshold-Dependent Rebound in Generative AI
# 生成式AI產業的門檻依賴型反彈

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

**Evidence from Adoption Proxies and Energy Policy Implications**  
**基於採用代理變數的實證與能源政策意涵**

---

## 📋 Overview | 概述

This repository contains **complete replication materials** for our study examining threshold-dependent rebound effects in the generative AI industry. We employ a dual-event quasi-natural experiment design to demonstrate that AI demand exhibits discrete jumps rather than continuous elasticity responses.

本儲存庫包含論文「生成式AI產業的門檻依賴型反彈」的**完整複製材料**。我們採用雙事件準自然實驗設計,證明AI需求展現離散跳躍而非連續彈性反應。

---

## 🎯 Key Findings | 主要發現

### Empirical Results | 實證結果

- ✅ **Market attention exhibits 10-11σ discrete jumps** following technological shocks (DeepSeek-R1: 11.07σ; GPT-5: 10.01σ)
- ✅ **Developer adoption behavior shows 2-4σ structural breaks** across PyPI packages
- ✅ **11 robustness checks confirm core conclusions** (including Newey-West, Control Group, ITS)
- ✅ **Control group analysis rules out Python ecosystem confounding**

---

- ✅ **市場關注度展現10-11σ離散跳躍** (DeepSeek-R1: 11.07σ; GPT-5: 10.01σ)
- ✅ **開發者採用行為呈現2-4σ結構斷裂** 跨PyPI套件驗證
- ✅ **11項穩健性檢驗確認核心結論** (包含Newey-West、對照組、ITS)
- ✅ **對照組分析排除Python生態系統混淆**

### Policy Implications | 政策意涵

- 💡 Carbon taxation shows **limited transmission** due to low electricity cost share (~18%)
- 💡 Computational quotas demonstrate **robust constraint** (70-88% emission reduction)
- 💡 Quantity-based instruments serve as **crucial complements** under extreme shocks

---

## 📂 Repository Contents | 儲存庫內容

```
threshold-dependent-rebound-AI/
├── data/                   # 數據 (110週時間序列, 2024-2026)
│   ├── pca_pc1_timeseries.csv
│   ├── LLM_Trends_Weekly_2024_2026.csv
│   └── Non-AI-Python-3.csv
├── code/                   # 分析程式碼
│   ├── run_B1_B2_analysis.py          # Newey-West穩健標準誤
│   ├── run_B2_Control_Group_analysis.py  # 對照組分析
│   └── run_ITS_analysis.py            # Interrupted Time Series
├── results/                # 分析結果
│   ├── B1_Newey_West_Results.txt
│   ├── B2_Control_Group_Results.csv
│   └── 圖_B2_Control_Group對比.png
└── README.md              # 本檔案
```

---

## 🔬 Methodology | 研究方法

### Events | 事件

**DeepSeek-R1** (2025-01-20)
- Type: **Price-driven shock** (94.5% price reduction)
- Impact: 11.07σ market attention jump

**GPT-5** (2025-08-07)  
- Type: **Capability-driven shock** (reasoning breakthrough)
- Impact: 10.01σ market attention jump

### Data Sources | 數據來源

1. **Google Trends** - Market attention (7 AI-related keywords)
2. **PyPI Downloads** - Developer adoption behavior (BigQuery)
3. **Control Group** - Non-AI packages (numpy, pandas, requests)

### Robustness Checks | 穩健性檢驗 (11項)

- [A] Placebo Test
- [B] Pure Baseline Analysis  
- [C] Local Window Analysis
- [D] Log Transformation
- [E-H] Breakpoint Sensitivity, Single Keyword, MAD/IQR, Autocorrelation
- [I] **Newey-West HAC Standard Errors**
- [J] **Control Group Analysis**
- [K] **Interrupted Time Series (ITS)**

---

## 🚀 Reproducibility | 如何複製

### Requirements | 環境需求

```bash
Python 3.8+
pandas >= 1.5.0
numpy >= 1.23.0
statsmodels >= 0.14.0
scipy >= 1.9.0
matplotlib >= 3.6.0
```

### Installation | 安裝

```bash
# Clone repository
git clone https://github.com/[USERNAME]/threshold-dependent-rebound-AI.git
cd threshold-dependent-rebound-AI

# Install dependencies
pip install -r code/requirements.txt
```

### Running Analysis | 執行分析

```bash
# Navigate to code directory
cd code

# Run analyses (ensure CSV files are in parent data/ folder)
python run_B1_B2_analysis.py          # Newey-West analysis
python run_B2_Control_Group_analysis.py  # Control group
python run_ITS_analysis.py            # ITS analysis
```

### Expected Outputs | 預期輸出

- `B1_Newey_West_Results.txt` - Newey-West robust standard errors
- `B2_Control_Group_Results.csv` - Control group test results
- `B2_Control_Group_Report.txt` - Control group analysis report
- `ITS_Analysis_Results.txt` - ITS regression results
- `圖_B2_Control_Group對比.png` - Control group visualization
- `圖_ITS分析結果.png` - ITS visualization

---

## 📊 Sample Results | 範例結果

### Newey-West Robust Standard Errors

| Event | σ Jump | 95% CI | t-statistic | p-value |
|-------|--------|--------|-------------|---------|
| DeepSeek-R1 | 5.3σ | [3.8σ, 6.7σ] | 4.34 | <0.001*** |
| GPT-5 | 3.0σ | [1.5σ, 4.4σ] | 4.67 | <0.001*** |

### Control Group vs AI Packages (DeepSeek-R1)

| Type | Package | σ Jump | F-stat | p-value |
|------|---------|--------|--------|---------|
| AI | anthropic | 3.69σ | 45.20 | <0.001*** |
| AI | openai | 2.41σ | 28.50 | <0.001*** |
| Control | numpy | 1.05σ | 0.53 | 0.593 |
| Control | pandas | 0.82σ | 0.16 | 0.855 |

---

## 📖 Citation | 引用

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

---

## 📧 Contact | 聯繫

**Honghua Tian (田弘華)**  
Department of Economics, Shih Hsin University  
世新大學經濟系  
Email: francis@mail.shu.edu.tw

---

## 📜 License | 授權

- **Data**: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)  
- **Code**: [MIT License](LICENSE)

---

## 🙏 Acknowledgments | 致謝

We thank the reviewers and editors for their valuable feedback. All errors remain our own.

感謝審稿人與編輯的寶貴意見。所有錯誤由作者自負。

---

**Last Updated**: 2026-03-16  
**Repository**: https://github.com/HungHuaTien/Threshold-Dependent-Rebound-in-Generative-AI/
