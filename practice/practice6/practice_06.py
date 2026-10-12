import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from pathlib import Path

# OS별 한글 폰트 및 마이너스 기호 설정
plt.rc("font", family="Malgun Gothic")  # Windows 기준 (Mac은 'AppleGothic')
plt.rc("axes", unicode_minus=False)

# 데이터 로드
row_df = pd.read_csv(Path(__file__).with_name("business_data.csv"))


"""
과제 A. 장르별 데이터 유효성 검증 및 집계
비즈니스 문제 의도

장르 정보가 누락된 데이터 분포를 확인하고, 정상 수집된 장르별 표본 수 및 평균 매출 규모를 파악해 특정 장르에 편중이 발생하는지 파악한다.

분석 포인트 힌트

- isnull().sum()으로 결측치를 파악한다.

- Seaborn의 countplot을 활용해 장르별 건수를 시각화한다.
"""

# 데이터 진단
# print(df.info())
# print(df.isnull().sum())  # genre = 10, wau_k = 8 : 결측치

df = row_df.dropna(subset=['genre', 'wau_k']).copy()
print(f"결측치제거 전(행 수): {len(row_df)},  후: {len(df)}")

plt.figure(figsize=(8, 5))
sns.countplot(data=row_df, x="genre", hue="genre", palette="Set2")
plt.title("장르별 수집 데이터 수 분포")
plt.xlabel("장르")
plt.ylabel("수집 건수")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.savefig(Path(__file__).with_name("Figure_A(1).png"), dpi=120)      

# rpg에 매출이 집중되었으며 캐주얼이나 스포츠 쪽엔 매출이 적음.
# 수집형 rpg가 매출이 잘나오니 어느정도 현실과 맞지만 fc온라인이나 피파온라인 같은 게임을 생각하면 실제로 이런지는 모르겠음.




"""
과제 B. WAU 대비 매출액 관계 및 이상치 식별
비즈니스 문제 의도

주간 접속자 수(WAU)와 매출 간의 비례 관계를 확인하고, 접속자 수 대비 비정상적으로 높은 매출을 기록한 이상치를 식별한다.

분석 포인트 힌트

scatterplot을 사용하고, hue 옵션에 플랫폼을 지정해 차원을 추가한다.

정상 범주를 크게 벗어난 포인트를 시각적으로 탐지한다.
"""

plt.figure(figsize=(9, 6))
sns.scatterplot(
    data=df,
    x="wau_k",
    y="revenue_mil",
    hue="platform",
    alpha=0.8,
    s=70,
)
plt.title("WAU 대비 매출액 분포 (플랫폼별 구분)")
plt.xlabel("주간 활성 유저 (천 명)")
plt.ylabel("매출액 (백만 원)")
plt.axhline(y=300, color="r", linestyle="--", label="매출 이상치 기준선")
plt.legend()
plt.savefig(Path(__file__).with_name("Figure_B(1).png"), dpi=120)


# 이상치 제거 1차
# Figure_B(1)에서 매출액이 정상범주를 넘었으니 매출액(300)을 기준으로 이상치 제거

# print(f"{(df['revenue_mil'] > 300).sum()}")
df_clean1 = df[df['revenue_mil'] < 300].copy()






"""
과제 C. 플랫폼 및 장르별 매출 분산 및 편차 비교
비즈니스 문제 의도

플랫폼(크로스플랫폼 vs 모바일 단독) 및 장르에 따른 매출 분포의 중위수, 사분위수 및 변동성을 비교해 안정적인 수익을 내는 영역을 식별한다.

분석 포인트 힌트

boxplot을 활용해 이상치를 제외한 중앙값과 분포 범위를 확인한다.
"""


plt.figure(figsize=(10, 6))
sns.boxplot(
    data=df_clean1,
    x="genre",
    y="revenue_mil",
    hue="platform",
)
plt.title("장르 및 플랫폼별 매출액 분포 비교")
plt.xlabel("장르")
plt.ylabel("매출액 (백만 원)")
plt.savefig(Path(__file__).with_name("Figure_C(1).png"), dpi=120)

# 이상치 제거 2차
# iqr 기준으로 이상치를 제거
"""
per_genre = 0

for _, g in df_clean1.groupby(["genre","platform"]):
    a, b = g["revenue_mil"].quantile([0.25, 0.75])
    i = b - a

    per_genre += ((g['revenue_mil'] < a - 1.5 * i)|(g['revenue_mil'] > b + 1.5 * i)).sum()

print(f"섹터별 실제 이상치 합 : {per_genre:,}건")
섹터별 실제 이상치 합 : 8건
"""
clean_groups = []
for _, g in df_clean1.groupby(['genre','platform']):
    a, b = g["revenue_mil"].quantile([0.25, 0.75])
    i = b - a

    mask = (
        (g["revenue_mil"] >= a - 1.5 * i)
        & (g["revenue_mil"] <= b + 1.5 * i)
    )

    clean_groups.append(g[mask])

df_clean2 = pd.concat(clean_groups)


"""
과제 D. 기간별 매출 추세 및 상관관계 구조 파악
비즈니스 문제 의도

8월 한 달간의 일별 매출 추이를 확인하거나 주요 지표 간 피벗 히트맵을 작성해 다차원적인 상관관계를 도출한다.

분석 포인트 힌트

lineplot을 활용해 날짜별 매출 흐름을 시각화한다.

pd.to_datetime을 통해 날짜 형식 변환 후 축을 설정한다.
"""

row_df["record_date"] = pd.to_datetime(row_df["record_date"])

plt.figure(figsize=(12, 5))
sns.lineplot(
    data=row_df,
    x="record_date",
    y="revenue_mil",
    marker="o",
    ms=4,
)
plt.title("2026년 8월 일별 매출 추이")
plt.xlabel("기록 일자")
plt.ylabel("매출액 (백만 원)")
ax = plt.gca()
ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=16))
plt.xticks(rotation=45)
plt.grid(True, linestyle=":", alpha=0.6)
plt.tight_layout()
plt.savefig(Path(__file__).with_name("Figure_D(1).png"), dpi=120)




# ---------------------------------------------------------

# 처리 후 차트 출력 모음

plt.figure(figsize=(8, 5))
sns.countplot(data=df_clean2, x="genre", hue="genre", palette="Set2")
plt.title("장르별 수집 데이터 수 분포")
plt.xlabel("장르")
plt.ylabel("수집 건수")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.savefig(Path(__file__).with_name("Figure_A(2).png"), dpi=120)      

plt.figure(figsize=(9, 6))
sns.scatterplot(
    data=df_clean2,
    x="wau_k",
    y="revenue_mil",
    hue="platform",
    alpha=0.8,
    s=70,
)
plt.title("WAU 대비 매출액 분포 (플랫폼별 구분)")
plt.xlabel("주간 활성 유저 (천 명)")
plt.ylabel("매출액 (백만 원)")
plt.axhline(y=300, color="r", linestyle="--", label="매출 이상치 기준선")
plt.legend()
plt.savefig(Path(__file__).with_name("Figure_B(2).png"), dpi=120)


plt.figure(figsize=(10, 6))
sns.boxplot(
    data=df_clean2,
    x="genre",
    y="revenue_mil",
    hue="platform",
)
plt.title("장르 및 플랫폼별 매출액 분포 비교")
plt.xlabel("장르")
plt.ylabel("매출액 (백만 원)")
plt.savefig(Path(__file__).with_name("Figure_C(2).png"), dpi=120)


df_clean2["record_date"] = pd.to_datetime(df_clean2["record_date"])

plt.figure(figsize=(12, 5))
sns.lineplot(
    data=df_clean2,
    x="record_date",
    y="revenue_mil",
    marker="o",
    ms=4,
)
plt.title("2026년 8월 일별 매출 추이")
plt.xlabel("기록 일자")
plt.ylabel("매출액 (백만 원)")
ax = plt.gca()
ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=16))
plt.xticks(rotation=45)
plt.grid(True, linestyle=":", alpha=0.6)
plt.tight_layout()
plt.savefig(Path(__file__).with_name("Figure_D(2).png"), dpi=120)