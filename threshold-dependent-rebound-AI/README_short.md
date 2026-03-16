# Threshold-Dependent Rebound in Generative AI

**Evidence from Adoption Proxies and Energy Policy Implications**

生成式AI產業的門檻依賴型反彈：基於採用代理變數的實證與能源政策意涵

---

## Overview

Replication materials for "Threshold-Dependent Rebound in Generative AI" (submitted to *Energy Policy*).

We demonstrate that AI demand exhibits **10-11σ discrete jumps** following technological shocks, rather than continuous elasticity responses.

---

## Repository Structure

```
├── data/          # Time series data (2024-2026)
├── code/          # Analysis scripts
└── results/       # Tables and figures
```

---

## Quick Start

**Requirements**: Python 3.8+, pandas, numpy, statsmodels, scipy, matplotlib

**Installation**:
```bash
pip install pandas numpy statsmodels scipy matplotlib
```

**Run analyses**:
```bash
cd code
python run_B1_B2_analysis.py
python run_B2_Control_Group_analysis.py
python run_ITS_analysis.py
```

Results will be saved to `results/` folder.

---

## Key Results

- Market attention: **11.07σ jump** (DeepSeek-R1), **10.01σ jump** (GPT-5)
- Developer adoption: **2-4σ structural breaks** across AI packages
- Control group: No significant jumps in non-AI packages
- **11 robustness checks** confirm findings

---

## Citation

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

## Contact

**Honghua Tian (田弘華)**  
Department of Economics, Shih Hsin University  
Email: francis@mail.shu.edu.tw

---

## License

- Data: CC BY 4.0
- Code: MIT License
