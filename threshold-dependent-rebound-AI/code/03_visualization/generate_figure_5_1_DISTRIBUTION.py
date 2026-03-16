"""
圖5.1優化版: 極端技術衝擊下不同政策工具的蒙地卡羅能耗分布對比
Monte Carlo Energy Distribution Comparison Across Policy Instruments

Opus視覺化建議實現:
1. 機率密度分布圖 (非長條圖)
2. 碳稅: 寬幅bell-curve (展現不確定性)
3. 定額: 垂直細線delta function (展現硬性約束)
4. 視覺衝擊: 寬幅vs垂直線的強烈對比

數據來源: monte_carlo_summary.csv (100次蒙地卡羅迭代)
執行環境: Local Python (已處理中文字型)
輸出: 中英文雙版本,600 DPI
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# ========== 中文字型設定 ==========
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Microsoft YaHei', 'SimHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 600
plt.rcParams['savefig.dpi'] = 600

# ========== 數據準備 (基於monte_carlo_summary.csv) ==========

# 5種政策情境的統計參數
policies_data = {
    'BAU': {'mean': 170490, 'std': 1201, 'ci_width': 2833, 'reduction': 0},
    '碳稅20%': {'mean': 162060, 'std': 974, 'ci_width': 3749, 'reduction': 4.9},
    '碳稅50%': {'mean': 149903, 'std': 1197, 'ci_width': 4170, 'reduction': 12.1},
    '定額5×': {'mean': 50000, 'std': 0, 'ci_width': 0, 'reduction': 70.7},
    '定額2×': {'mean': 20000, 'std': 0, 'ci_width': 0, 'reduction': 88.3}
}

# 英文政策名稱
policies_en = {
    'BAU': 'BAU',
    '碳稅20%': 'Tax 20%',
    '碳稅50%': 'Tax 50%',
    '定額5×': 'Quota 5×',
    '定額2×': 'Quota 2×'
}

# 生成機率分布曲線
x_range = np.linspace(0, 200000, 2000)

# ========== 圖表生成 (中文版) ==========

fig, ax = plt.subplots(figsize=(16, 10))

# 配色方案
colors = {
    'BAU': '#808080',
    '碳稅20%': '#FFA500',
    '碳稅50%': '#FF6B35',
    '定額5×': '#4CAF50',
    '定額2×': '#2E7D32'
}

# 繪製碳稅政策的寬幅分布曲線
for policy in ['BAU', '碳稅20%', '碳稅50%']:
    data = policies_data[policy]
    mean = data['mean']
    std = data['std']
    
    # 生成常態分布
    pdf = stats.norm.pdf(x_range, mean, std)
    
    # 繪製分布曲線
    ax.plot(x_range, pdf, color=colors[policy], linewidth=3, 
            label=f"{policy} (μ={mean:,.0f}, CI寬度={data['ci_width']:,.0f})",
            alpha=0.8)
    
    # 填充曲線下方區域
    ax.fill_between(x_range, 0, pdf, color=colors[policy], alpha=0.15)

# 繪製定額政策的垂直細線 (delta function)
for policy in ['定額2×', '定額5×']:
    data = policies_data[policy]
    mean = data['mean']
    
    # 垂直細線 (模擬delta function)
    max_height = 0.00025  # 調整高度使其顯著
    ax.plot([mean, mean], [0, max_height], color=colors[policy], 
            linewidth=5, label=f"{policy} (精確={mean:,.0f}, CI寬度=0)",
            alpha=0.95, linestyle='-')
    
    # 在垂直線頂部添加標註
    ax.annotate(f'{policy}\n硬性約束\nCI=0', 
                xy=(mean, max_height), xytext=(mean, max_height*1.3),
                ha='center', fontsize=12, fontweight='bold', color=colors[policy],
                bbox=dict(boxstyle='round,pad=0.6', facecolor='white', 
                         edgecolor=colors[policy], linewidth=2, alpha=0.95))

# 添加視覺對比說明文字框
textstr = ('視覺對比重點:\n'
           '• 碳稅政策 (寬幅曲線): 對需求波動高度敏感\n'
           '  CI寬度隨稅率提高而增加 (2,833→4,170)\n'
           '• 定額政策 (垂直細線): 硬性約束的確定性\n'
           '  CI寬度=0, 精確截斷超額需求')
ax.text(0.98, 0.97, textstr, transform=ax.transAxes, fontsize=11,
        verticalalignment='top', horizontalalignment='right',
        bbox=dict(boxstyle='round,pad=1', facecolor='wheat', alpha=0.85, 
                 edgecolor='black', linewidth=1.5))

# 設定標題與標籤
ax.set_title('圖5.1 極端技術衝擊下不同政策工具的蒙地卡羅能耗分布對比\n(100次迭代)', 
             fontsize=18, fontweight='bold', pad=20)
ax.set_xlabel('總體能耗單位 (Total Energy Consumption Units)', 
              fontsize=14, fontweight='bold')
ax.set_ylabel('機率密度 (Probability Density)', 
              fontsize=14, fontweight='bold')

# 設定x軸格式 (K為千)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}K'))
ax.set_xlim(0, 200000)
ax.set_ylim(0, 0.00030)

# 網格與邊框
ax.grid(True, alpha=0.25, linestyle=':', linewidth=1)
ax.spines['top'].set_linewidth(2)
ax.spines['right'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2)

# 圖例 (分兩欄,左側碳稅,右側定額)
handles, labels = ax.get_legend_handles_labels()
# 重新排序: BAU, 碳稅20%, 碳稅50%, 定額2×, 定額5×
order = [0, 1, 2, 4, 3]
ax.legend([handles[i] for i in order], [labels[i] for i in order],
          loc='upper left', fontsize=11, frameon=True, shadow=True, ncol=1)

plt.tight_layout()
plt.savefig('圖5_1_蒙地卡羅分布對比_中文版_600dpi.png', 
            dpi=600, bbox_inches='tight', facecolor='white')
print("✅ 中文版圖5.1機率分布對比已生成")
plt.close()

# ========== 圖表生成 (英文版) ==========

fig, ax = plt.subplots(figsize=(16, 10))

# Plot carbon tax policies as wide distributions
for policy_cn, policy_en in [('BAU', 'BAU'), ('碳稅20%', 'Tax 20%'), ('碳稅50%', 'Tax 50%')]:
    data = policies_data[policy_cn]
    mean = data['mean']
    std = data['std']
    
    # Generate normal distribution
    pdf = stats.norm.pdf(x_range, mean, std)
    
    # Plot distribution curve
    ax.plot(x_range, pdf, color=colors[policy_cn], linewidth=3, 
            label=f"{policy_en} (μ={mean:,.0f}, CI width={data['ci_width']:,.0f})",
            alpha=0.8)
    
    # Fill under curve
    ax.fill_between(x_range, 0, pdf, color=colors[policy_cn], alpha=0.15)

# Plot quota policies as vertical lines (delta functions)
for policy_cn, policy_en in [('定額2×', 'Quota 2×'), ('定額5×', 'Quota 5×')]:
    data = policies_data[policy_cn]
    mean = data['mean']
    
    # Vertical line (simulating delta function)
    max_height = 0.00025
    ax.plot([mean, mean], [0, max_height], color=colors[policy_cn], 
            linewidth=5, label=f"{policy_en} (exact={mean:,.0f}, CI width=0)",
            alpha=0.95, linestyle='-')
    
    # Annotate at top of line
    ax.annotate(f'{policy_en}\nHard\nConstraint\nCI=0', 
                xy=(mean, max_height), xytext=(mean, max_height*1.3),
                ha='center', fontsize=12, fontweight='bold', color=colors[policy_cn],
                bbox=dict(boxstyle='round,pad=0.6', facecolor='white', 
                         edgecolor=colors[policy_cn], linewidth=2, alpha=0.95))

# Add visual contrast explanation box
textstr = ('Visual Contrast:\n'
           '• Carbon Tax (Wide Curves): Highly sensitive to\n'
           '  demand volatility. CI width increases with tax rate\n'
           '  (2,833→4,170), reflecting greater uncertainty.\n'
           '• Quota (Vertical Lines): Deterministic hard constraint.\n'
           '  CI width=0, precisely truncates excess demand.')
ax.text(0.98, 0.97, textstr, transform=ax.transAxes, fontsize=11,
        verticalalignment='top', horizontalalignment='right',
        bbox=dict(boxstyle='round,pad=1', facecolor='wheat', alpha=0.85, 
                 edgecolor='black', linewidth=1.5))

# Set title and labels
ax.set_title('Figure 5.1 Monte Carlo Energy Consumption Distribution Comparison\nAcross Policy Instruments under Extreme Technological Shocks (100 Iterations)', 
             fontsize=18, fontweight='bold', pad=20)
ax.set_xlabel('Total Energy Consumption Units', 
              fontsize=14, fontweight='bold')
ax.set_ylabel('Probability Density', 
              fontsize=14, fontweight='bold')

# Format x-axis
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}K'))
ax.set_xlim(0, 200000)
ax.set_ylim(0, 0.00030)

# Grid and borders
ax.grid(True, alpha=0.25, linestyle=':', linewidth=1)
ax.spines['top'].set_linewidth(2)
ax.spines['right'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2)

# Legend (reorder)
handles, labels = ax.get_legend_handles_labels()
order = [0, 1, 2, 4, 3]
ax.legend([handles[i] for i in order], [labels[i] for i in order],
          loc='upper left', fontsize=11, frameon=True, shadow=True, ncol=1)

plt.tight_layout()
plt.savefig('Figure_5_1_Monte_Carlo_Distribution_Comparison_EN_600dpi.png', 
            dpi=600, bbox_inches='tight', facecolor='white')
print("✅ 英文版圖5.1機率分布對比已生成")
plt.close()

print("\n" + "="*70)
print("圖5.1機率分布對比版生成完成!")
print("="*70)
print("Opus視覺化建議實現:")
print("  ✅ 碳稅政策: 寬幅bell-curve分布 (展現不確定性)")
print("  ✅ 定額政策: 垂直細線delta function (展現硬性約束)")
print("  ✅ 視覺衝擊: 寬幅vs垂直線的強烈對比")
print("  ✅ CI寬度標註: 碳稅2,833→4,170, 定額CI=0")
print("\n核心視覺訊息:")
print("  - 碳稅: CI寬度隨稅率提高而增加 (不確定性上升)")
print("  - 定額: CI寬度=0 (硬性約束的確定性特徵)")
print("="*70)
