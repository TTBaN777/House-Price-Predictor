import requests

class HouseScraper:
    def __init__(self):
        # Session 處理 Cookie
        self.session = requests.Session()
        self.city_index = {
            "宜蘭縣": 1, "基隆市": 2, "台北市": 3, "新北市": 4, 
            "桃園市": 5, "新竹市": 6, "新竹縣": 7, "苗栗縣": 8, 
            "台中市": 9, "南投縣": 11, "彰化縣": 12, "雲林縣": 13, 
            "嘉義市": 14, "嘉義縣": 15, "台南市": 16, "高雄市": 18, 
            "屏東縣": 20, "台東縣": 21, "花蓮縣": 22, "澎湖縣": 23, 
            "金門縣": 24
        }
        self.headers = {
            # 假裝自己是 Chrome 避免被反爬蟲
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.great-home.com.tw/RentHouse/Main.aspx",
            "X-Requested-With": "XMLHttpRequest"
        }
        # 去首頁拿 Cookie ，網站 API 需要 Cookie 才會回資料
        try:
            self.session.get("https://www.great-home.com.tw/RentHouse/Main.aspx", headers=self.headers, timeout=10)
        except:
            pass
    
    # 處理空字串、None 或其他奇怪的格式
    def _safe_int(self, value, default=0):
        try:
            if value is None or str(value).strip() == "": return default
            return int(float(value))
        except: return default

    def _safe_float(self, value, default=0.0):
        try:
            if value is None or str(value).strip() == "":
                return default
            return float(value)
        except:
            return default

    def scrape_list_page(self, page=1, city_name="台北市"):
        try:
            api_url = "https://www.great-home.com.tw/ajax/dataService.aspx?job=search&path=rent"
            
            # 取得該縣市的 index ，預設為 3 (台北市)
            idx = self.city_index.get(city_name, 3)
            
            # 這是 API 的 搜尋條件編碼
            q_value = f"1^1^{idx}^^^P_^^^^^^^^^^^0^^0^1^{page}^0"
            
            payload = {
                "q": q_value,
                "rlg": "1"
            }

            headers = self.headers.copy()
            headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"

            # timeout 20 秒並執行請求
            response = self.session.post(api_url, headers=headers, data=payload, timeout=20)

            try:
                # strict=False 可以處理 JSON 內容中的換行符或特殊字元
                import json
                result_json = json.loads(response.text, strict=False)
            except Exception as je:
                print(f"第 {page} 頁 JSON 解析異常，嘗試自動修復...")
                return []

            data_list = result_json.get("data", [])
            if data_list:
                print(f"第 {page} 頁成功！第一筆：{data_list[0].get('n')} ({data_list[0].get('x')})")
            
            houses = []
            for item in data_list:
                # 格局解析
                p_raw = item.get("p", [])
                p_list = p_raw if isinstance(p_raw, list) else ["0", "0", "0"]
                processed_p = [p_list[i] if len(p_list) > i else "0" for i in range(3)]

                data = {
                    "id": item.get("s", ""),
                    "title": item.get("n", "無標題"),
                    # 使用 _safe_float 處理價格、坪數與屋齡
                    "price": self._safe_float(item.get("np", 0)) * 10000, 
                    "size": self._safe_float(item.get("a", 0)),
                    "rooms": self._safe_int(processed_p[0]),
                    "halls": self._safe_int(processed_p[1]),
                    "bath": self._safe_int(processed_p[2]),
                    "location": item.get("x", ""),
                    "house_type": item.get("t", ""),
                    "current_floor": str(item.get("w", "")),
                    "total_floor": str(item.get("z", "")),
                    "age": self._safe_float(item.get("k", 0)), # 使用安全轉換
                    "lon": str(item.get("lon", "")),
                    "lat": str(item.get("lat", "")),
                    "url": f"https://www.great-home.com.tw/RentHouse/Detail.aspx?s={item.get('s')}"
                }
                houses.append(data)
            return houses
        except Exception as e:
            print(f"❌ 嚴重錯誤: {e}")
            return []