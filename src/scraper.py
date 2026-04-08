import requests
from bs4 import BeautifulSoup

class HouseScraper:
    def __init__(self):
        # 直接指向資料接口
        self.api_url = "https://www.great-home.com.tw/ajax/dataService.aspx?job=search&path=rent"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.great-home.com.tw/RentHouse/",
            "X-Requested-With": "XMLHttpRequest" # 告訴伺服器這是一個 AJAX 請求
        }

    def scrape_list_page(self):
        """直接抓取 API 回傳的資料"""
        try:
            # 這裡我們直接對 API 發送請求
            response = requests.get(self.api_url, headers=self.headers, timeout=10)
            
            if response.status_code != 200:
                print(f"請求失敗，狀態碼：{response.status_code}")
                return []

            # 這裡回傳的是 HTML 片段
            soup = BeautifulSoup(response.text, 'html.parser')
            houses = []
            
            # 使用我們之前確認過的 class 名稱
            items = soup.select(".itemlist__main")
            
            for item in items:
                try:
                    # 解析標題
                    title = item.select_one(".itemlist__intro").get_text(strip=True)
                    
                    # 解析價格 (2.7 萬 -> 27000)
                    price_val = item.select_one(".hlight.color--red").get_text(strip=True)
                    price = float(price_val) * 10000

                    # 解析房/廳/衛/坪數
                    specs = item.select(".itemlist__info__header .color--black")
                    rooms = specs[0].get_text(strip=True) if len(specs) > 0 else "0"
                    size  = specs[3].get_text(strip=True) if len(specs) > 3 else "0"

                    houses.append({
                        "title": title,
                        "price": price,
                        "rooms": int(rooms),
                        "size": float(size)
                    })
                except Exception as e:
                    continue
            
            return houses

        except Exception as e:
            print(f"API 請求錯誤: {e}")
            return []