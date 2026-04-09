import requests

class HouseScraper:
    def __init__(self):
        # 使用 Session 會自動幫我們處理 Cookie
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.great-home.com.tw/RentHouse/Main.aspx",
            "X-Requested-With": "XMLHttpRequest"
        }
        # 關鍵：先去首頁打個招呼，拿到 Cookie
        try:
            self.session.get("https://www.great-home.com.tw/RentHouse/Main.aspx", headers=self.headers, timeout=10)
        except:
            pass

    def _safe_int(self, value, default=0):
        try:
            if value is None or str(value).strip() == "": return default
            return int(float(value))
        except: return default

    def scrape_list_page(self, page=1):
        try:
            # 這是搜尋接口
            api_url = "https://www.great-home.com.tw/ajax/dataService.aspx?job=search"
            
            # 調整參數：city 改用代碼 "A" (代表台北市)，並加入所有搜尋必備欄位
            payload = {
                "path": "rent/search",
                "city": "A",       # 台北市的代碼通常是 A
                "page": str(page),
                "range": "1",      # 搜尋範圍：縣市
                "sort": "1",
                "sw": "",
                "mrt": "",
                "mrtline": "",
                "mrtsta": ""
            }

            # 嘗試改用不同的 Content-Type 模擬 (有時伺服器很挑剔)
            response = self.session.post(
                api_url, 
                headers=self.headers, 
                data=payload, 
                timeout=10
            )

            result_json = response.json()
            data_list = result_json.get("data", [])
            
            if data_list:
                # 這裡最關鍵：看區域是不是變成了台北市
                print(f"✅ 第 {page} 頁回應：第一筆是「{data_list[0].get('n')}」，區域：{data_list[0].get('x')}")
            
            houses = []
            for item in data_list:
                p_list = item.get("p", ["0", "0", "0"])
                while len(p_list) < 3: p_list.append("0")
                data = {
                    "id": item.get("s", ""),
                    "title": item.get("n", "無標題"),
                    "price": float(item.get("np", 0)) * 100,
                    "size": float(item.get("a", 0)),
                    "rooms": self._safe_int(p_list[0]),
                    "halls": self._safe_int(p_list[1]),
                    "bath": self._safe_int(p_list[2]),
                    "location": item.get("x", ""),
                    "house_type": item.get("t", ""),
                    "current_floor": str(item.get("w", "")),
                    "total_floor": str(item.get("z", "")),
                    "age": float(item.get("k", 0)) if item.get("k") else 0.0,
                    "lon": str(item.get("lon", "")),
                    "lat": str(item.get("lat", "")),
                    "url": f"https://www.great-home.com.tw/RentHouse/Detail.aspx?s={item.get('s')}"
                }
                houses.append(data)
            return houses
        except Exception as e:
            print(f"❌ 錯誤: {e}")
            return []