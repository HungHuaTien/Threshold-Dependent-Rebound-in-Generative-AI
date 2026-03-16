# Code Documentation

## Overview

This folder contains all analysis scripts used in the paper. Scripts are organized by analysis stage and can be executed independently or in sequence for full replication.

本資料夾包含論文中所有分析程式碼。程式按分析階段組織,可獨立執行或依序執行以完整複製結果。

---

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

**Required packages**:
- pandas >= 1.5.0
- numpy >= 1.23.0
- statsmodels >= 0.14.0
- scipy >= 1.9.0
- matplotlib >= 3.6.0

---

## Scripts Execution Guide

### Quick Start (Full Replication)

To replicate all analyses in the paper:

```bash
# Ensure CSV data files are in ../data/ folder
# Then run scripts in this order:

python run_B1_B2_analysis.py
python run_B2_Control_Group_analysis.py
python run_ITS_analysis.py
```

---

### Individual Scripts

#### 1. `run_B1_B2_analysis.py`

**Purpose**: Newey-West robust standard errors analysis (Robustness Check I)

**Input**:
- `../data/pca_pc1_timeseries.csv`

**Output**:
- `../results/B1_Newey_West_Results.txt`

**What it does**:
- Recalculates Chow Test with Newey-West HAC standard errors
- Lag order: 4 weeks
- Provides 95% confidence intervals for σ jumps

**Expected runtime**: ~30 seconds

**Key results**:
- DeepSeek-R1: 5.3σ (95% CI: [3.8σ, 6.7σ])
- GPT-5: 3.0σ (95% CI: [1.5σ, 4.4σ])

---

#### 2. `run_B2_Control_Group_analysis.py`

**Purpose**: Control group analysis (Robustness Check J)

**Input**:
- `../data/Non-AI-Python-3.csv`

**Output**:
- `../results/B2_Control_Group_Results.csv`
- `../results/B2_Control_Group_Report.txt`
- `../results/圖_B2_Control_Group對比.png`

**What it does**:
- Compares AI packages vs non-AI packages (numpy, pandas, requests)
- Executes Chow Test for 3 packages × 2 events = 6 combinations
- Generates visualization comparing AI vs control group responses

**Expected runtime**: ~1-2 minutes

**Key results**:
- AI packages: All σ > 2.1, p < 0.01 (highly significant)
- Control group: Most σ < 2.0, p > 0.05 (not significant)

---

#### 3. `run_ITS_analysis.py`

**Purpose**: Interrupted Time Series analysis (Robustness Check K)

**Input**:
- `../data/pca_pc1_timeseries.csv`

**Output**:
- `../results/ITS_Analysis_Results.txt`
- `../results/圖_ITS分析結果.png`

**What it does**:
- Estimates ITS regression model:  
  Y_t = β0 + β1·Time + β2·Event + β3·Time_After_Event + ε
- Estimates Level Change (β2) and Slope Change (β3)
- Generates visualization with counterfactual predictions

**Expected runtime**: ~45 seconds

**Key results**:
- DeepSeek-R1 Level Change: β2 = 1.66, t = 8.12, p < 0.001
- GPT-5 Level Change: β2 = 4.58, t = 11.24, p < 0.001

---

## File Naming Convention

All scripts follow the naming pattern:
- `run_[Analysis]_analysis.py`

All outputs are saved to `../results/` with descriptive names.

---

## Event Dates Reference

For all analyses:

**DeepSeek-R1 Event**
- Announcement: 2025-01-20
- Data point: 2025-01-26 (week index 57)

**GPT-5 Event**
- Announcement: 2025-08-07
- Data point: 2025-08-10 (week index 85)

---

## Troubleshooting

### Common Issues

**Issue**: `FileNotFoundError: pca_pc1_timeseries.csv`  
**Solution**: Ensure CSV files are in `../data/` folder

**Issue**: `ModuleNotFoundError: statsmodels`  
**Solution**: Install dependencies: `pip install -r requirements.txt`

**Issue**: Chinese characters not displaying  
**Solution**: This doesn't affect analysis results. Output files use UTF-8 encoding.

---

## Customization

To modify analysis parameters:

**Newey-West lag order** (in `run_B1_B2_analysis.py`):
```python
nlags = 4  # Change to desired lag order
```

**ITS event dates** (in `run_ITS_analysis.py`):
```python
deepseek_event_date = pd.Timestamp('2025-01-26')  # Modify if needed
gpt5_event_date = pd.Timestamp('2025-08-10')
```

---

## License

Code is provided under MIT License. See main repository LICENSE file.

---

## Contact

For questions about code execution:

**Honghua Tian**  
Email: francis@mail.shu.edu.tw  
Department of Economics, Shih Hsin University

---

**Last Updated**: 2026-03-16
