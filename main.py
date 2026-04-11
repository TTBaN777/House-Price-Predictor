import math
import os
import random
import time
from src.scraper import HouseScraper
from src.database import Database

def main():
    print("=== 🏠 全台租屋資料採集工具 ===")
    
    # --- 1. 初始化 Scraper (這不影響檔案) ---
    scraper = HouseScraper()

    # --- 2. 使用者輸入縣市與筆數 ---
    while True:
        target_city = input(f"📍 請輸入想採集的縣市 (例如: 台北市, 新北市): ").strip()
        if target_city in scraper.city_index:
            break
        print(f"❌ 抱歉，暫不支援 '{target_city}'，請檢查字是否輸入正確。")

    while True:
        try:
            total_count = int(input("🔢 請問大約需要抓取幾筆資料？(建議 10-100): "))
            if total_count > 0:
                total_pages = math.ceil(total_count / 10)
                break
            print("❌ 請輸入大於 0 的數字。")
        except ValueError:
            print("❌ 請輸入有效的整數數字。")

    # --- 3. 【核心修正】先處理檔案刪除，再初始化 Database ---
    db_path = "data/house_rent.db"
    csv_path = f"data/{target_city}_rent_export.csv"
    
    # 刪除資料庫檔案 (此時 db = Database() 還沒執行，所以不會被鎖定)
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print(f"\n🧹 已清空舊資料庫...")
        except PermissionError:
            print(f"\n❌ 錯誤：無法刪除 {db_path}。")
            print("👉 請關閉 DB Browser、VS Code 資料庫預覽或其他正在使用該檔案的程式，然後再試一次。")
            return # 終止程式

    # 刪除舊的 CSV
    if os.path.exists(csv_path):
        os.remove(csv_path)
        print(f"🗑️ 已刪除舊的 CSV 檔案：{csv_path}")

    # --- 4. 檔案處理完畢，現在才初始化資料庫連線 ---
    db = Database()

    # --- 5. 開始執行採集迴圈 ---
    print(f"\n🚀 開始採集 {target_city} 的租屋資料，預計抓取 {total_pages} 頁...")
    
    actual_count = 0
    for p in range(1, total_pages + 1):
        print(f"📡 正在採集第 {p} 頁...")
        
        results = scraper.scrape_list_page(page=p, city_name=target_city)
        
        if results:
            db.insert_houses(results)
            actual_count += len(results)
        else:
            print(f"⚠️ 第 {p} 頁沒抓到新資料，可能已到末頁。")
            break
        
        if p < total_pages:
            wait_time = random.uniform(3, 5)
            time.sleep(wait_time)

    # --- 6. 產出報表 ---
    print(f"\n--- 任務完成 ---")
    print(f"✅ 總計抓取並過濾出 {actual_count} 筆資料")
    db.export_to_csv(csv_path)

if __name__ == "__main__":
    main()