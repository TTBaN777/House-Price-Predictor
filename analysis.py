import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 資料清洗與特徵強化
df = pd.read_csv("data/台北市_rent_export.csv")
df['location'] = df['location'].str.replace('臺北', '台北')
# 「台北市信義區」與「信義區」重複問題：先取「區」字結尾
df['district'] = df['location'].str.extract(r'(..區)') 

# 排除 rooms 為 0 的物件（排除車位）
df_clean = df[df['rooms'] > 0].copy()

# 計算每坪單價
df_clean['price_per_ping'] = df_clean['price'] / df_clean['size']

# 進行單價篩選（排除大於 5000 的離群值）
df_clean = df_clean[df_clean['price_per_ping'] < 5000]

# 排除極小坪數
df_clean = df_clean[df_clean['size'] > 3]

# 設定繪圖風格
sns.set_theme(style="whitegrid", font='Microsoft JhengHei')
plt.rcParams['axes.unicode_minus'] = False

# 一列兩圖
fig, axes = plt.subplots(1, 2, figsize=(18, 7))

# 圖一：行政區單價排行 (Barplot)
order = df_clean.groupby('district')['price_per_ping'].mean().sort_values(ascending=False).index
sns.barplot(ax=axes[0], x='price_per_ping', y='district', data=df_clean, 
            order=order, palette='magma', errorbar=None)

# 加入樣本數標籤在長條圖後方
counts = df_clean['district'].value_counts()
for i, d in enumerate(order):
    axes[0].text(df_clean[df_clean['district']==d]['price_per_ping'].mean() + 50, i, 
                 f'樣本: {counts[d]}', va='center', fontsize=10)

axes[0].set_title('台北市各區 - 每坪租金單價排行', fontsize=16, fontweight='bold')
axes[0].set_xlabel('每坪租金 (元)')
axes[0].set_ylabel('行政區')

# 圖二：特徵相關性熱力圖 (Heatmap)
# 只選取數值欄位來分析
corr_cols = ['price', 'size', 'rooms', 'halls', 'bath', 'age', 'price_per_ping']
corr_matrix = df_clean[corr_cols].corr()

sns.heatmap(ax=axes[1], data=corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
axes[1].set_title('特徵相關性熱力圖 (Correlation Matrix)', fontsize=16, fontweight='bold')

plt.tight_layout()
plt.show()

# 坪數 vs 租金的散佈圖
plt.figure(figsize=(10, 6))
sns.regplot(x='size', y='price', data=df_clean, scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
plt.title('坪數與總租金的線性關係', fontsize=14)
plt.xlabel('坪數')
plt.ylabel('總租金')
plt.show()