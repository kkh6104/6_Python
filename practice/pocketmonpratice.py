"""
    포켓몬 6스텟 합을 추세선으로 표시
    x축 : 도감 번호
    y축 : 스텟합계
"""
import matplotlib, pandas as pd
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns

from pathlib  import Path
from chart_config import setup

setup()

# 자료 읽고 정제
raw_data = pd.read_csv(Path(__file__).with_name("pokemon_complete_stats_korean_updated.csv"))
raw_data['total_status'] = raw_data["hp"] + raw_data["attack"] + raw_data["defense"] + raw_data["special_attack"] + raw_data["special_defense"] + raw_data["speed"]
raw_data['generation'] = raw_data['generation'].str.replace('generation-', '')
roman = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']
raw_data['generation'] = raw_data['generation'].map(roman.index) + 1
df = raw_data[['id','total_status','generation']]
# print(df)

# 정제된 데이터로 그래프 그리기
plt.figure(figsize=(12, 5))
sns.lineplot(
    data=df,
    x="id",
    y="total_status",
    marker="."
)
plt.title("포켓몬 총스텟 추세선")
plt.xlabel("도감 번호")
plt.ylabel("총스텟 합")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(Path(__file__).with_name("po.png"), dpi=120)