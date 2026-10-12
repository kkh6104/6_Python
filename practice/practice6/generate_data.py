import numpy as np
import pandas as pd

# 재현성을 위한 난수 고정
np.random.seed(42)

# 데이터 규모 설정
n_rows = 200

# 범주형 데이터 정의
game_titles = [f"Game_{chr(65 + i)}" for i in range(20)]
genres = ["RPG", "Strategy", "Action", "Casual", "Sports"]
platforms = ["Cross-Platform", "Mobile-Only"]

# 기초 데이터 생성
data = {
    "game_title": np.random.choice(game_titles, size=n_rows),
    "genre": np.random.choice(genres, size=n_rows, p=[0.35, 0.25, 0.20, 0.10, 0.10]),
    "platform": np.random.choice(platforms, size=n_rows, p=[0.6, 0.4]),
    "record_date": pd.date_range(start="2026-08-01", periods=n_rows, freq="D"),
    "revenue_mil": np.random.normal(loc=50, scale=15, size=n_rows).round(2),
    "wau_k": np.random.normal(loc=120, scale=30, size=n_rows).round(1),
    "mau_k": np.random.normal(loc=400, scale=80, size=n_rows).round(1),
}

df = pd.DataFrame(data)

# 논리적 오류 방지 (음수 값 처리)
df["revenue_mil"] = df["revenue_mil"].clip(lower=1.0)
df["wau_k"] = df["wau_k"].clip(lower=10.0)
df["mau_k"] = df["mau_k"].clip(lower=50.0)

# 의도적 결측치 주입 (3~7% 수준)
df.loc[df.sample(frac=0.05).index, "genre"] = np.nan
df.loc[df.sample(frac=0.04).index, "wau_k"] = np.nan

# 의도적 이상치 주입 (매출 및 MAU 컬럼)
df.loc[15, "revenue_mil"] = 350.0
df.loc[88, "revenue_mil"] = 420.0
df.loc[42, "mau_k"] = 2500.0

# CSV 저장 및 출력
df.to_csv("business_data.csv", index=False)
print("business_data.csv 생성 완료")