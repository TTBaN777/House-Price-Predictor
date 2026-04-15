import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# 1. 初始化 API
app = FastAPI(title="台北市租屋行情預測系統")

# 2. 載入模型與欄位清單
model = joblib.load('models/house_model.pkl')
model_columns = joblib.load('models/model_columns.pkl')

# 3. 定義 API 輸入數據格式
class HouseInput(BaseModel):
    district: str  # 例如: "大安區"
    size: float    # 坪數
    rooms: int     # 房
    halls: int     # 廳
    bath: int      # 衛
    age: float     # 屋齡

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(os.path.join("static", "favicon.ico")) # 或是回傳一個空的 Response

@app.get("/")
def index():
    return FileResponse(os.path.join("static", "index.html"))

# 4. 預測端點
@app.post("/predict")
def predict_rent(data: HouseInput):
    # a. 建立一個只有基礎特徵的 DataFrame
    # Note：這裡要跟訓練時的處理邏輯一致
    input_data = {
        'size': [data.size],
        'rooms': [data.rooms],
        'halls': [data.halls],
        'bath': [data.bath],
        'age': [data.age]
    }
    input_df = pd.DataFrame(input_data)
    
    # b. 處理 One-Hot Encoding：建立所有行政區欄位並設為 0
    for col in model_columns:
        if col.startswith("district_"):
            input_df[col] = 0
            
    # c. 將使用者輸入的行政區欄位設為 1
    target_col = f"district_{data.district}"
    if target_col in model_columns:
        input_df[target_col] = 1
    
    # d. 確保欄位順序與訓練時完全一致
    input_df = input_df[model_columns]
    # e. 執行預測 (之前用了 Log 轉換，這裡要 expm1)
    prediction_log = model.predict(input_df)[0]
    real_prediction = np.expm1(prediction_log)
    
    return {
        "status": "success",
        "predicted_price": round(float(real_prediction), 0),
        "unit": "TWD",
        "message": "預測結果僅供參考！"
    }

@app.get("/health")
def health_check():
    return {"status": "online", "model_version": "v2.0_xgboost"}