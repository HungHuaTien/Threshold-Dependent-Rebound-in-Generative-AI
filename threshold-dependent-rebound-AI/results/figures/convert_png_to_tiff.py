"""
圖表格式轉換工具
PNG → TIFF (適用期刊投稿)

功能:
1. 將PNG圖表轉換為TIFF格式
2. 保持600 DPI解析度
3. 適合學術期刊投稿

使用方法:
python convert_png_to_tiff.py
"""

from PIL import Image
import os

def convert_png_to_tiff(input_file, output_file=None, dpi=600):
    """
    將PNG圖表轉換為TIFF格式
    
    Parameters:
    -----------
    input_file : str
        輸入PNG檔案路徑
    output_file : str, optional
        輸出TIFF檔案路徑 (若未指定,自動生成)
    dpi : int
        解析度 (預設600)
    """
    
    # 如果未指定輸出檔名,自動生成
    if output_file is None:
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}.tiff"
    
    # 開啟PNG圖片
    print(f"正在讀取: {input_file}")
    img = Image.open(input_file)
    
    # 取得原始DPI (如果有的話)
    original_dpi = img.info.get('dpi', (72, 72))
    print(f"原始DPI: {original_dpi}")
    
    # 轉換並儲存為TIFF
    print(f"正在轉換為TIFF (DPI={dpi})...")
    img.save(output_file, 
             format='TIFF',
             dpi=(dpi, dpi),
             compression='lzw')  # LZW壓縮 (無損壓縮)
    
    print(f"✓ 已儲存: {output_file}")
    
    # 顯示檔案資訊
    file_size_mb = os.path.getsize(output_file) / (1024*1024)
    print(f"  檔案大小: {file_size_mb:.2f} MB")
    print(f"  圖片尺寸: {img.size[0]} × {img.size[1]} pixels")
    print(f"  解析度: {dpi} DPI")
    
    return output_file

# ========== 主程式 ==========

if __name__ == "__main__":
    # 設定檔案路徑
    input_files = [
        "Figure_4_1_Dual_Event_Multipanel_EN_600dpi.png",
        # 如果有其他圖表,在這裡加入
    ]
    
    print("="*60)
    print("PNG → TIFF 轉換工具 (期刊投稿專用)")
    print("="*60)
    print()
    
    for input_file in input_files:
        if not os.path.exists(input_file):
            print(f"❌ 找不到檔案: {input_file}")
            print(f"   請確認檔案在當前目錄: {os.getcwd()}")
            continue
        
        try:
            # 轉換為TIFF
            output_file = convert_png_to_tiff(input_file, dpi=600)
            print()
        
        except Exception as e:
            print(f"❌ 轉換失敗: {str(e)}")
            print()
    
    print("="*60)
    print("轉換完成!")
    print("="*60)
    
    input("\n按Enter鍵結束...")
