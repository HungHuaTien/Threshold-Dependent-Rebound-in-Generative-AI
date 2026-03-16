# Data Documentation | 數據文檔

## 📋 Overview | 概述

This folder contains weekly time series data from January 2024 to January 2026 (110 weeks) used in our study of threshold-dependent rebound effects in generative AI.

本資料夾包含2024年1月至2026年1月的週度時間序列數據(110週),用於研究生成式AI的門檻依賴型反彈效應。

---

## 📁 Files | 檔案列表

### 1. `pca_pc1_timeseries.csv`

**Description**: Google Trends principal component (PC1) standardized time series  
**描述**: Google Trends搜尋指數主成分分析標準化時間序列

**Columns**:
- `date`: Week start date (YYYY-MM-DD) | 週起始日期
- `pc1_score`: Standardized PC1 score | 標準化PC1分數

**Sample size**: 110 weeks  
**Time range**: 2023-12-31 to 2026-01-25  
**Source**: Derived from `LLM_Trends_Weekly_2024_2026.csv` using PCA

**Usage**: Main dependent variable for structural break analysis

---

### 2. `LLM_Trends_Weekly_2024_2026.csv`

**Description**: Raw Google Trends search volume data for 7 AI-related keywords  
**描述**: 7個AI相關關鍵字的Google Trends原始搜尋量數據

**Columns**:
- `date`: Week start date | 週起始日期
- `ChatGPT API`: Search volume index (0-100) | 搜尋量指數
- `LLM pricing`: Search volume index
- `API cost`: Search volume index
- `Hugging Face`: Search volume index
- `DeepSeek`: Search volume index
- `Ollama`: Search volume index
- `AI agent`: Search volume index

**Sample size**: 110 weeks  
**Geography**: Worldwide | 全球  
**Search type**: Web search | 網頁搜尋  
**Source**: Google Trends (https://trends.google.com)

**Note**: Values represent relative search interest (0-100), not absolute volumes.

---

### 3. `Non-AI-Python-3.csv`

**Description**: PyPI weekly download counts for control group packages  
**描述**: 對照組套件的PyPI週度下載量

**Columns**:
- `week`: Week start date | 週起始日期
- `package_name`: Package name | 套件名稱 (numpy, pandas, requests)
- `downloads`: Weekly download count | 週度下載次數

**Sample size**: 324 records (108 weeks × 3 packages)  
**Time range**: 2024-01-01 to 2026-01-19

**Source**: Google Cloud BigQuery  
Dataset: `bigquery-public-data.pypi.file_downloads`  
Filter: `details.installer.name = 'pip'`

**Purpose**: Control group to rule out Python ecosystem confounding

**Packages**:
- `numpy`: Scientific computing foundation | 科學計算基礎
- `pandas`: Data processing | 資料處理  
- `requests`: HTTP requests | HTTP請求

All three are **non-AI packages** widely used in Python development.

---

## 🎯 Key Events | 關鍵事件

### DeepSeek-R1 Event

**Date**: 2025-01-20 (Monday)  
**Data point**: 2025-01-26 (following Monday)  
**Week index**: 57 (index 56 in 0-based indexing)  
**Type**: Price-driven shock | 價格主導型衝擊  
**Impact**: API pricing dropped 94.5% | API定價下降94.5%

**Market Response**:
- Google Trends PC1: 11.07σ jump | 跳躍
- PyPI downloads: 2.13σ - 3.69σ jump across AI packages

---

### GPT-5 Event

**Date**: 2025-08-07 (Thursday)  
**Data point**: 2025-08-10 (following Monday)  
**Week index**: 85 (index 84 in 0-based indexing)  
**Type**: Capability-driven shock | 能力主導型衝擊  
**Impact**: Reasoning capability breakthrough | 推理能力突破

**Market Response**:
- Google Trends PC1: 10.01σ jump
- PyPI downloads: 2.89σ - 4.07σ jump across AI packages

---

## 📊 Data Collection Methodology | 數據收集方法

### Google Trends

**Collection Date**: 2026-01-26  
**Tool**: Google Trends API / Manual export  
**Settings**:
- Geography: Worldwide
- Category: All categories  
- Search type: Web search
- Time range: 2024-01-01 to 2026-01-25

**Keywords Selection Rationale**:
1. `ChatGPT API` - Direct API usage intent
2. `LLM pricing` - Cost sensitivity signal
3. `API cost` - Alternative cost query
4. `Hugging Face` - Open-source alternative
5. `DeepSeek` - Event-specific
6. `Ollama` - Local deployment option
7. `AI agent` - Application layer demand

**PCA Methodology**:
- Standardization: Z-score normalization
- Method: Singular Value Decomposition (SVD)
- PC1 variance explained: ~65% (as reported in paper)

---

### PyPI Downloads

**Collection Date**: 2026-01-26  
**Source**: Google Cloud BigQuery  
**Query**:
```sql
SELECT
  DATE_TRUNC(DATE(timestamp), WEEK(MONDAY)) as week,
  file.project as package_name,
  COUNT(*) as downloads
FROM `bigquery-public-data.pypi.file_downloads`
WHERE
  file.project IN ('numpy', 'pandas', 'requests')
  AND DATE(timestamp) BETWEEN '2024-01-01' AND '2026-01-25'
  AND details.installer.name = 'pip'
GROUP BY week, package_name
ORDER BY week, package_name
```

**Filter Rationale**:
- `installer = 'pip'`: Excludes conda and other installers for consistency
- Week aggregation: Monday-start weeks to align with Google Trends

---

## 🔍 Data Quality | 數據品質

### Completeness | 完整性

- ✅ No missing weeks in time series
- ✅ All packages have complete download records
- ✅ Event dates verified against official announcements

### Validation | 驗證

- ✅ Cross-checked with alternative data sources (GitHub trends, Reddit mentions)
- ✅ Outlier detection: No anomalies beyond documented events
- ✅ Consistency check: Google Trends vs PyPI show aligned patterns

---

## 📜 License | 授權

All data in this folder is provided under **CC BY 4.0** license.

Data usage requirements:
1. **Attribution**: Cite our paper (see main README)
2. **Share-Alike**: Derived datasets should use compatible license
3. **No Additional Restrictions**: Cannot add legal/technical barriers

---

## 📧 Questions? | 疑問?

For questions about data collection or methodology:

**Honghua Tian**  
Email: francis@mail.shu.edu.tw  
Department of Economics, Shih Hsin University

---

**Last Updated**: 2026-03-16
