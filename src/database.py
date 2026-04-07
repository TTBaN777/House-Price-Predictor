# src/database.py
# Responsible for database operations (Database Class)

import sqlite3
import os

class Database:
    def __init__(self, db_path="data/house_prices.db"):
        self.db_path = db_path
        self.conn = None
        self.create_connection()

    def create_connection(self):
        self.conn = sqlite3.connect(self.db_path)

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS house_prices (
            id INTEGER PRIMARY KEY,
            address TEXT,
            price REAL,
            bedrooms INTEGER,
            bathrooms INTEGER
        );
        """
        self.conn.execute(query)
        self.conn.commit()

    def save_data(self, data):
        # Example save logic
        self.create_table()
        self.conn.executemany("INSERT INTO house_prices (address, price, bedrooms, bathrooms) VALUES (?, ?, ?, ?)", data)
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()