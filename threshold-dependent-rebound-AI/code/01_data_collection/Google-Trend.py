"""
Google Trends 週度數據收集腳本
時間範圍: 2024-01-01 到 2026-01-31 (109週)
關鍵字: ChatGPT API, LLM pricing, API cost, Hugging Face,
        DeepSeek, Ollama, AI agent
"""

import pandas as pd
from pytrends.request import TrendReq
import time

# 初始化 pytrends
pytrends = TrendReq(hl='zh-TW', tz=-480, timeout=(10, 25))

# 定義關鍵字組 (Google Trends 一次最多5個關鍵字)
kw_groups = [
    ["ChatGPT API", "LLM pricing", "API cost", "Hugging Face"],
    ["DeepSeek", "Ollama", "AI agent"]
]

# 設定時間範圍 (確保獲得週資料)
timeframe = '2024-01-01 2026-01-31'

all_data = pd.DataFrame()

print(f"開始抓取時間區間: {timeframe} 的週資料...")

for kw_list in kw_groups:
    try:
        # 建立請求
        pytrends.build_payload(kw_list, cat=0, timeframe=timeframe, geo='')

        # 抓取興趣隨時間變化的數據
        df = pytrends.interest_over_time()

        if not df.empty:
            # 移除 isPartial 欄位
            df = df.drop(columns=['isPartial'])

            # 合併數據
            if all_data.empty:
                all_data = df
            else:
                all_data = pd.merge(
                    all_data, df,
                    left_index=True,
                    right_index=True,
                    how='outer'
                )

        print(f"✓ 成功抓取關鍵字: {', '.join(kw_list)}")

        # 避免請求過快被封鎖
        time.sleep(7)

    except Exception as e:
        print(f"✗ 抓取 {kw_list} 時發生錯誤: {e}")

# 儲存結果
if not all_data.empty:
    file_name = "LLM_Trends_Weekly_2024_2026.csv"
    all_data.to_csv(file_name)
    print(f"\n=== 任務完成 ===")
    print(f"資料筆數: {len(all_data)} 週")
    print(f"檔案已儲存: {file_name}")
    print(all_data.head())
else:
    print("未抓取到任何數據")
