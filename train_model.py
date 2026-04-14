import pandas as pd
import numpy as np
import joblib
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# 1. 資料讀取
df = pd.read_csv("data/台北市_rent_export.csv")
df['location'] = df['location'].str.replace('臺北', '台北')
df['district'] = df['location'].str.extract(r'(..區)')
df_clean = df[(df['rooms'] > 0) & (df['price'] < 100000)].copy()

# 2. One-Hot Encoding
X = pd.get_dummies(df_clean[['district', 'size', 'rooms', 'halls', 'bath', 'age']], columns=['district'])
y = df_clean['price']
print(f"總共: {X.shape[0]} 筆")

# 3. 目標值對數轉換
y_log = np.log1p(y)

X_train, X_test, y_log_train, y_log_test = train_test_split(X, y_log, test_size=0.2, random_state=42)

# 4. XGBoost
model = XGBRegressor(
    n_estimators=500,
    learning_rate=2e-2,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    n_jobs=-1
)
model.fit(X_train, y_log_train)

# 預測並轉換回原始價格
y_log_pred = model.predict(X_test)
y_pred = np.expm1(y_log_pred) # 將 log 轉回真實金額
y_test_real = np.expm1(y_log_test)

mae = mean_absolute_error(y_test_real, y_pred)
print(f"XGBoost + Log: MAE: {mae:.2f} 元")

# 儲存模型與欄位順序 (供 API 使用)
joblib.dump(model, 'models/house_model.pkl')
joblib.dump(X.columns.tolist(), 'models/model_columns.pkl')