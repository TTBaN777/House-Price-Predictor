from src.scraper import HouseScraper

def main():
    scraper = HouseScraper()
    print("📡 正在從 API 獲取資料...")
    results = scraper.scrape_list_page()
    
    if results:
        print(f"✅ 成功抓取到 {len(results)} 筆資料！")
        for i, h in enumerate(results[:3]):
            print(f"物件 {i+1}: {h['title']} | 租金: {h['price']} | 坪數: {h['size']}")
    else:
        print("❌ 依然抓不到資料，可能需要檢查 Headers 或 API 參數。")

if __name__ == "__main__":
    main()