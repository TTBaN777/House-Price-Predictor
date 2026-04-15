# 1. 使用官方 Python 輕量版作為基礎 Image
FROM python:3.11-slim

# 2. 設定容器內的工作目錄
WORKDIR /app

# 3. 複製相依套件清單並安裝
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 複製專案所有內容到容器中
COPY . .

# 5. 宣告容器運行的連接埠
EXPOSE 8000

# 6. 啟動指令 (使用 uvicorn 跑你的 app)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]