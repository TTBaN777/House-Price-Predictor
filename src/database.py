import sqlite3
import os
import pandas as pd

class Database:
    def __init__(self, db_path="data/house_rent.db"):
        # 確保 data 資料夾存在
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.create_table()

    def create_table(self):
        """建立資料表"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS houses (
                    id TEXT PRIMARY KEY,       -- 物件編號 (s)
                    title TEXT,                -- 名稱 (n)
                    price REAL,                -- 租金 (np * 100)
                    size REAL,                 -- 坪數 (a)
                    rooms INTEGER,             -- 房 (p[0])
                    halls INTEGER,             -- 廳 (p[1])
                    bath INTEGER,              -- 衛 (p[2])
                    location TEXT,             -- 區域 (x)
                    house_type TEXT,           -- 型態 (t)
                    current_floor TEXT,        -- 樓層 (w)
                    total_floor TEXT,          -- 總高 (z)
                    age REAL,                  -- 屋齡 (k)
                    lon TEXT,                  -- 經度
                    lat TEXT,                  -- 緯度
                    url TEXT,                  -- 網址
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def insert_houses(self, house_list):
        """批量插入資料，若 ID 重複則忽略"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            sql = '''
                INSERT OR IGNORE INTO houses 
                (id, title, price, size, rooms, halls, bath, location, house_type, current_floor, total_floor, age, lon, lat, url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            # 將字典轉換成元組列表
            data_tuples = [
                (
                    h['id'], h['title'], h['price'], h['size'], 
                    h['rooms'], h['halls'], h['bath'], h['location'],
                    h['house_type'], h['current_floor'], h['total_floor'],
                    h['age'], h['lon'], h['lat'], h['url']
                ) for h in house_list
            ]
            cursor.executemany(sql, data_tuples)
            conn.commit()
            print(f"💾 資料庫更新完成，本次新增/更新筆數: {cursor.rowcount}")
    
    def export_to_csv(self, file_path="data/house_rent_export.csv"):
        """將資料庫內容匯出為 CSV 檔，解決 Excel 中文亂碼問題"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # 使用 pandas 直接讀取資料庫
                df = pd.read_sql_query("SELECT * FROM houses", conn)
                
                # 確保資料夾存在
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                #匯出 CSV，使用 utf-8-sig 編碼（Excel 專用防亂碼）
                df.to_csv(file_path, index=False, encoding='utf-8-sig')
                print(f"📊 CSV 匯出成功！路徑: {file_path}")
        except Exception as e:
            print(f"❌ 匯出 CSV 失敗: {e}")