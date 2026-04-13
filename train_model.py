import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# --- 1. 強化版資料清洗 ---
df = pd.read_csv("data/台北市_rent_export.csv")
df['location'] = df['location'].str.replace('臺北', '台北')
df['district'] = df['location'].str.extract(r'(..區)')

# 關鍵：過濾掉極端高房價（例如超過 10 萬的通常是店面或超豪宅）
# 以及過濾掉單價太誇張的
df['price_per_ping'] = df['price'] / df['size']
df_clean = df[
    (df['rooms'] > 0) & 
    (df['price'] < 100000) &            # 只看 10 萬以下的住宅
    (df['price_per_ping'] < 3000) &     # 排除超高單價噪音
    (df['size'] < 100)                  # 排除超大坪數
].copy()

# --- 2. 特徵工程：One-Hot Encoding ---
# 這樣模型就不會誤會行政區有順序關係
X = pd.get_dummies(df_clean[['district', 'size', 'rooms', 'halls', 'bath', 'age']], columns=['district'])
y = df_clean['price']

# --- 3. 訓練與評估 ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 調整參數：減少樹的深度，防止在小數據上過擬合 (Overfitting)
model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)

print(f"📊 優化後 MAE: {mae:.2f} 元")

# --- 4. 儲存 ---
if not os.path.exists('models'): os.makedirs('models')
joblib.dump(model, 'models/house_model.pkl')
# 儲存欄位名稱，這在 API 預測時很重要
joblib.dump(X.columns.tolist(), 'models/model_columns.pkl')