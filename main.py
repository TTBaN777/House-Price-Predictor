from src.scraper import HouseScraper
from src.database import Database
import time
import os # 新增這行

db_path = "data/house_rent.db"
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"🧹 已清空舊資料庫，準備重新抓取最新數據...")
    
def main():
    # --- 新增：刪除舊 CSV 的功能 ---
    csv_path = "data/house_rent_export.csv"
    if os.path.exists(csv_path):
        os.remove(csv_path)
        print(f"🗑️ 已刪除舊的 CSV 檔案：{csv_path}")
    # ----------------------------

    scraper = HouseScraper()
    db = Database()
    
    # 這裡我們來挑戰抓 5 頁
    for p in range(1, 6):
        print(f"📡 正在採集台北市租屋：第 {p} 頁...")
        results = scraper.scrape_list_page(page=p)
        
        if results:
            db.insert_houses(results)
        else:
            print(f"⚠️ 第 {p} 頁沒抓到新資料。")
            
        time.sleep(2)

    print("\n--- 正在產生報表 ---")
    db.export_to_csv(csv_path)

if __name__ == "__main__":
    main()