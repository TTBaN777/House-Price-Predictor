import sqlite3

class Database:
    def __init__(self, db_path="data/house_prices.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS houses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            price REAL,
            location TEXT,
            size REAL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def insert_house(self, data):
        query = "INSERT INTO houses (title, price, location, size) VALUES (?, ?, ?, ?)"
        self.conn.execute(query, data)
        self.conn.commit()