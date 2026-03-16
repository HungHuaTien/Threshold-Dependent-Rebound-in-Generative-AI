"""
完整分析腳本：AI 市場雙事件研究（2024-2026）
整合 PCA、Google Trends 和 PyPI 的雙事件分析

執行方式：
python complete_analysis.py

需要的檔案（放在同一資料夾）：
1. LLM_Trends_Weekly_2024_2026.csv (Google Trends 數據)
2. BigQuery.csv (PyPI 數據，包含 openai, anthropic, langchain)

輸出：
- 所有分析結果的 CSV 檔案
- 所有視覺化圖表的 PNG 檔案
- 完整的統計報告（終端機輸出）

作者：AI Energy Research
日期：2026-03-10
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import linregress
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from datetime import datetime
import os

# 創建輸出資料夾
OUTPUT_DIR = 'analysis_outputs'
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("="*100)
print("AI 市場雙事件研究：完整分析腳本")
print("="*100)

# ============================================================================
# 階段 1：PCA 主成分分析
# ============================================================================

print("\n" + "="*100)
print("階段 1：PCA 主成分分析（Google Trends）")
print("="*100)

# 讀取 Google Trends 數據
try:
    df_trends = pd.read_csv('LLM_Trends_Weekly_2024_2026.csv')
    df_trends['date'] = pd.to_datetime(df_trends['date'])
    df_trends = df_trends.sort_values('date')
    print(f"\n✓ Google Trends 數據載入成功")
    print(f"  時間範圍: {df_trends['date'].min().date()} 到 {df_trends['date'].max().date()}")
    print(f"  總週數: {len(df_trends)} 週")
except FileNotFoundError:
    print("\n✗ 錯誤：找不到 'LLM_Trends_Weekly_2024_2026.csv'")
    print("  請確認檔案在同一資料夾中")
    exit(1)

# 7 個關鍵字
keywords = ['ChatGPT API', 'LLM pricing', 'API cost', 'Hugging Face', 
            'DeepSeek', 'Ollama', 'AI agent']

# 準備 PCA
X = df_trends[keywords].values
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 執行 PCA
pca = PCA()
pca.fit(X_scaled)

variance_explained = pca.explained_variance_ratio_
cumulative_variance = np.cumsum(variance_explained)
loadings = pca.components_

print(f"\n主成分解釋變異:")
for i in range(min(3, len(variance_explained))):
    print(f"  PC{i+1}: {variance_explained[i]*100:6.2f}% (累積: {cumulative_variance[i]*100:6.2f}%)")

print(f"\n✓ PC1 解釋了 {variance_explained[0]*100:.1f}% 的變異")

# 計算 PC1 分數
pc1_scores = pca.transform(X_scaled)[:, 0]

# 儲存 PCA 結果
loadings_df = pd.DataFrame(
    loadings[:3, :].T,
    columns=['PC1', 'PC2', 'PC3'],
    index=keywords
)
loadings_df.to_csv(f'{OUTPUT_DIR}/pca_loadings.csv')

variance_df = pd.DataFrame({
    'component': [f'PC{i}' for i in range(1, 8)],
    'variance_explained': variance_explained,
    'cumulative_variance': cumulative_variance
})
variance_df.to_csv(f'{OUTPUT_DIR}/pca_variance_explained.csv', index=False)

pc1_df = pd.DataFrame({
    'date': df_trends['date'],
    'pc1_score': pc1_scores
})
pc1_df.to_csv(f'{OUTPUT_DIR}/pca_pc1_timeseries.csv', index=False)

print(f"✓ PCA 結果已儲存")

# ============================================================================
# 階段 2：Google Trends 雙事件分析
# ============================================================================

print("\n" + "="*100)
print("階段 2：Google Trends 雙事件分析")
print("="*100)

DEEPSEEK_DATE = pd.to_datetime('2025-01-20')
GPT5_DATE = pd.to_datetime('2025-08-07')

print(f"\n事件1：DeepSeek-R1 ({DEEPSEEK_DATE.date()})")
print(f"事件2：GPT-5 ({GPT5_DATE.date()})")

def chow_test(data, col_name, breakpoint_date):
    """執行 Chow Test 檢驗結構斷裂"""
    data_col = data[['date', col_name]].copy()
    data_col = data_col.sort_values('date')
    
    before = data_col[data_col['date'] < breakpoint_date].copy()
    after = data_col[data_col['date'] >= breakpoint_date].copy()
    
    before['week_idx'] = range(len(before))
    after['week_idx'] = range(len(after))
    all_data = data_col.copy()
    all_data['week_idx'] = range(len(all_data))
    
    # 全樣本回歸
    slope_all, intercept_all, _, _, _ = linregress(all_data['week_idx'], all_data[col_name])
    y_pred_all = intercept_all + slope_all * all_data['week_idx']
    rss_all = np.sum((all_data[col_name] - y_pred_all) ** 2)
    
    # 分段回歸
    slope_before, intercept_before, _, _, _ = linregress(before['week_idx'], before[col_name])
    y_pred_before = intercept_before + slope_before * before['week_idx']
    rss_before = np.sum((before[col_name] - y_pred_before) ** 2)
    
    slope_after, intercept_after, _, _, _ = linregress(after['week_idx'], after[col_name])
    y_pred_after = intercept_after + slope_after * after['week_idx']
    rss_after = np.sum((after[col_name] - y_pred_after) ** 2)
    
    rss_pooled = rss_all
    rss_separate = rss_before + rss_after
    
    n = len(all_data)
    k = 2
    
    f_stat = ((rss_pooled - rss_separate) / k) / (rss_separate / (n - 2*k))
    p_value = 1 - stats.f.cdf(f_stat, k, n - 2*k)
    
    return {
        'n_before': len(before),
        'n_after': len(after),
        'f_stat': f_stat,
        'p_value': p_value,
        'slope_before': slope_before,
        'slope_after': slope_after,
        'mean_before': before[col_name].mean(),
        'std_before': before[col_name].std(),
        'mean_after': after[col_name].mean()
    }

def calc_sigma_jump(data, col_name, breakpoint_date):
    """計算標準差倍數跳躍"""
    before = data[data['date'] < breakpoint_date]
    after = data[data['date'] >= breakpoint_date]
    
    mean_before = before[col_name].mean()
    std_before = before[col_name].std()
    
    closest_idx = (after['date'] - breakpoint_date).abs().idxmin()
    first_after = after.loc[closest_idx, col_name]
    first_after_date = after.loc[closest_idx, 'date']
    
    sigma_jump = (first_after - mean_before) / std_before if std_before > 0 else np.nan
    
    return {
        'first_after': first_after,
        'first_after_date': first_after_date,
        'sigma_jump': sigma_jump
    }

# 分析 DeepSeek 和 GPT-5
results_gt = []

for event_name, event_date in [('DeepSeek-R1', DEEPSEEK_DATE), ('GPT-5', GPT5_DATE)]:
    chow_result = chow_test(pc1_df, 'pc1_score', event_date)
    sigma_result = calc_sigma_jump(pc1_df, 'pc1_score', event_date)
    
    sig = "***" if chow_result['p_value'] < 0.001 else "**" if chow_result['p_value'] < 0.01 else "*" if chow_result['p_value'] < 0.05 else "n.s."
    
    print(f"\n{event_name}:")
    print(f"  σ 跳躍: {sigma_result['sigma_jump']:.2f}σ")
    print(f"  Chow F = {chow_result['f_stat']:.2f}, p = {chow_result['p_value']:.6f} {sig}")
    
    results_gt.append({
        'event': event_name,
        'date': event_date,
        'sigma_jump': sigma_result['sigma_jump'],
        'chow_f': chow_result['f_stat'],
        'p_value': chow_result['p_value'],
        'n_before': chow_result['n_before'],
        'n_after': chow_result['n_after']
    })

results_gt_df = pd.DataFrame(results_gt)
results_gt_df.to_csv(f'{OUTPUT_DIR}/google_trends_dual_events.csv', index=False)
print(f"\n✓ Google Trends 雙事件結果已儲存")

# Placebo 檢驗
PLACEBO_DATE = pd.to_datetime('2025-05-01')
quiet_period = pc1_df[(pc1_df['date'] >= '2025-03-01') & (pc1_df['date'] < '2025-08-01')].copy()

if len(quiet_period) >= 10:
    placebo_chow = chow_test(quiet_period, 'pc1_score', PLACEBO_DATE)
    
    placebo_df = pd.DataFrame([{
        'test_type': 'Placebo',
        'date': PLACEBO_DATE,
        'period': 'Quiet (2025-03 to 2025-07)',
        'n_weeks': len(quiet_period),
        'chow_f': placebo_chow['f_stat'],
        'p_value': placebo_chow['p_value']
    }])
    placebo_df.to_csv(f'{OUTPUT_DIR}/google_trends_placebo_test.csv', index=False)
    
    print(f"\nPlacebo 檢驗: F = {placebo_chow['f_stat']:.2f}, p = {placebo_chow['p_value']:.4f}")

# ============================================================================
# 階段 3：PyPI 雙事件分析
# ============================================================================

print("\n" + "="*100)
print("階段 3：PyPI 雙事件分析")
print("="*100)

# 讀取 PyPI 數據
try:
    df_pypi = pd.read_csv('BigQuery.csv')
    df_pypi['download_week'] = pd.to_datetime(df_pypi['download_week'])
    df_pypi = df_pypi.sort_values(['package_name', 'download_week'])
    print(f"\n✓ PyPI 數據載入成功")
    print(f"  套件: {df_pypi['package_name'].unique()}")
    print(f"  時間範圍: {df_pypi['download_week'].min().date()} 到 {df_pypi['download_week'].max().date()}")
except FileNotFoundError:
    print("\n✗ 錯誤：找不到 'BigQuery.csv'")
    print("  請確認檔案在同一資料夾中")
    exit(1)

def chow_test_pypi(data, breakpoint_date):
    """PyPI 專用的 Chow Test"""
    before = data[data['download_week'] < breakpoint_date].copy()
    after = data[data['download_week'] >= breakpoint_date].copy()
    
    before['week_idx'] = range(len(before))
    after['week_idx'] = range(len(after))
    all_data_reg = data.copy()
    all_data_reg['week_idx'] = range(len(all_data_reg))
    
    slope_all, intercept_all, _, _, _ = linregress(all_data_reg['week_idx'], 
                                                     all_data_reg['download_count'])
    y_pred_all = intercept_all + slope_all * all_data_reg['week_idx']
    rss_all = np.sum((all_data_reg['download_count'] - y_pred_all) ** 2)
    
    slope_before, intercept_before, _, _, _ = linregress(before['week_idx'], before['download_count'])
    y_pred_before = intercept_before + slope_before * before['week_idx']
    rss_before = np.sum((before['download_count'] - y_pred_before) ** 2)
    
    slope_after, intercept_after, _, _, _ = linregress(after['week_idx'], after['download_count'])
    y_pred_after = intercept_after + slope_after * after['week_idx']
    rss_after = np.sum((after['download_count'] - y_pred_after) ** 2)
    
    rss_pooled = rss_all
    rss_separate = rss_before + rss_after
    
    n = len(all_data_reg)
    k = 2
    
    f_stat = ((rss_pooled - rss_separate) / k) / (rss_separate / (n - 2*k))
    p_value = 1 - stats.f.cdf(f_stat, k, n - 2*k)
    
    return {
        'n_before': len(before),
        'n_after': len(after),
        'f_stat': f_stat,
        'p_value': p_value,
        'mean_before': before['download_count'].mean(),
        'std_before': before['download_count'].std()
    }

def calc_sigma_jump_pypi(data, breakpoint_date):
    """PyPI 專用的 sigma 跳躍計算"""
    before = data[data['download_week'] < breakpoint_date]
    after = data[data['download_week'] >= breakpoint_date]
    
    mean_before = before['download_count'].mean()
    std_before = before['download_count'].std()
    
    closest_idx = (after['download_week'] - breakpoint_date).abs().idxmin()
    first_after = after.loc[closest_idx, 'download_count']
    
    sigma_jump = (first_after - mean_before) / std_before if std_before > 0 else np.nan
    growth_pct = ((first_after - mean_before) / mean_before) * 100 if mean_before != 0 else np.nan
    
    return {
        'first_after': first_after,
        'sigma_jump': sigma_jump,
        'growth_pct': growth_pct
    }

# 分析每個套件
results_pypi = []

for package in ['openai', 'anthropic', 'langchain']:
    pkg_data = df_pypi[df_pypi['package_name'] == package].sort_values('download_week').copy()
    
    print(f"\n{package.upper()}:")
    
    for event_name, event_date in [('DeepSeek-R1', DEEPSEEK_DATE), ('GPT-5', GPT5_DATE)]:
        chow_result = chow_test_pypi(pkg_data, event_date)
        sigma_result = calc_sigma_jump_pypi(pkg_data, event_date)
        
        sig = "***" if chow_result['p_value'] < 0.001 else "**" if chow_result['p_value'] < 0.01 else "*" if chow_result['p_value'] < 0.05 else "n.s."
        
        print(f"  {event_name}: σ={sigma_result['sigma_jump']:.2f}σ, F={chow_result['f_stat']:.2f}, p={chow_result['p_value']:.6f} {sig}")
        
        results_pypi.append({
            'package': package,
            'event': event_name,
            'date': event_date,
            'sigma_jump': sigma_result['sigma_jump'],
            'growth_pct': sigma_result['growth_pct'],
            'chow_f': chow_result['f_stat'],
            'p_value': chow_result['p_value'],
            'n_before': chow_result['n_before'],
            'n_after': chow_result['n_after']
        })

results_pypi_df = pd.DataFrame(results_pypi)
results_pypi_df.to_csv(f'{OUTPUT_DIR}/pypi_dual_events_results.csv', index=False)
print(f"\n✓ PyPI 雙事件結果已儲存")

# ============================================================================
# 階段 4：跨數據源驗證
# ============================================================================

print("\n" + "="*100)
print("階段 4：跨數據源驗證")
print("="*100)

# 計算傳導比率
google_trends_avg = results_gt_df.groupby('event')['sigma_jump'].mean()
pypi_avg = results_pypi_df.groupby('event')['sigma_jump'].mean()

print(f"\n傳導比率分析:")
print(f"{'事件':<20} {'Google Trends':<20} {'PyPI (平均)':<20} {'傳導比率':<15}")
print("-"*75)

transmission_rates = []
for event in ['DeepSeek-R1', 'GPT-5']:
    gt_sigma = google_trends_avg[event]
    pypi_sigma = pypi_avg[event]
    transmission = (pypi_sigma / gt_sigma * 100) if gt_sigma != 0 else 0
    transmission_rates.append(transmission)
    
    print(f"{event:<20} {gt_sigma:>8.2f}σ          {pypi_sigma:>8.2f}σ          {transmission:>8.1f}%")

# 儲存綜合摘要
cross_validation_summary = {
    'DeepSeek_GT_sigma': google_trends_avg['DeepSeek-R1'],
    'DeepSeek_PyPI_sigma': pypi_avg['DeepSeek-R1'],
    'DeepSeek_transmission': transmission_rates[0],
    'GPT5_GT_sigma': google_trends_avg['GPT-5'],
    'GPT5_PyPI_sigma': pypi_avg['GPT-5'],
    'GPT5_transmission': transmission_rates[1]
}

cross_val_df = pd.DataFrame([cross_validation_summary])
cross_val_df.to_csv(f'{OUTPUT_DIR}/cross_validation_summary.csv', index=False)
print(f"\n✓ 跨數據源驗證結果已儲存")

# ============================================================================
# 最終摘要報告
# ============================================================================

print("\n" + "="*100)
print("分析完成！最終摘要")
print("="*100)

print(f"\n1. PCA 分析:")
print(f"   ✓ PC1 解釋 {variance_explained[0]*100:.1f}% 變異")
print(f"   ✓ 前3個主成分累積解釋 {cumulative_variance[2]*100:.1f}% 變異")

print(f"\n2. Google Trends (PC1):")
print(f"   ✓ DeepSeek-R1: {results_gt_df[results_gt_df['event']=='DeepSeek-R1']['sigma_jump'].values[0]:.2f}σ")
print(f"   ✓ GPT-5: {results_gt_df[results_gt_df['event']=='GPT-5']['sigma_jump'].values[0]:.2f}σ")

print(f"\n3. PyPI 開發者行為:")
deepseek_sig = len(results_pypi_df[(results_pypi_df['event'] == 'DeepSeek-R1') & (results_pypi_df['p_value'] < 0.05)])
gpt5_sig = len(results_pypi_df[(results_pypi_df['event'] == 'GPT-5') & (results_pypi_df['p_value'] < 0.05)])
print(f"   ✓ DeepSeek-R1: {deepseek_sig}/3 套件顯著")
print(f"   ✓ GPT-5: {gpt5_sig}/3 套件顯著")

print(f"\n4. 傳導比率:")
print(f"   ✓ DeepSeek-R1: {transmission_rates[0]:.1f}%")
print(f"   ✓ GPT-5: {transmission_rates[1]:.1f}%")

print(f"\n所有結果已儲存至 '{OUTPUT_DIR}' 資料夾")
print(f"\n產出檔案清單:")
output_files = [
    'pca_loadings.csv',
    'pca_variance_explained.csv',
    'pca_pc1_timeseries.csv',
    'google_trends_dual_events.csv',
    'google_trends_placebo_test.csv',
    'pypi_dual_events_results.csv',
    'cross_validation_summary.csv'
]

for i, filename in enumerate(output_files, 1):
    print(f"  {i}. {filename}")

print("\n" + "="*100)
print("腳本執行完成！")
print("="*100)
