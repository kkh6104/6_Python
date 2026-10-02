"""
## STEP 1 · 진단

정제하기 전에 **무엇이 얼마나 망가졌는지** 파악합니다.

세 파일을 읽고 아래를 확인해 표로 정리하세요.

- 각 파일의 행 수, 컬럼별 dtype
- 숫자여야 하는데 문자열로 읽힌 컬럼 => 자동 결측 피하려고 옵션 쓰면 죄다 문자열로 읽히고 결측이 아닌걸로 인식됨.
- 컬럼별 결측 수와 비율
- `bike_id`, `rental_id` 의 중복 건수
- `bike_type`, `district`, `payment_method` 의 고유값 목록

<aside>

**참고**

`dtype=str, keep_default_na=False` 로 읽으면 파일에 적힌 그대로 볼 수 있습니다.

`read_csv` 는 `"N/A"` 를 자동으로 결측 처리하므로, 원본 상태를 보려면 이 옵션이 필요합니다.


### 확인 문항

1. `raw-bikes.csv` 는 55행인데 자전거는 몇 대입니까? 왜 다릅니까?
2. `bike_type` 의 고유값은 몇 종류입니까? 실제로는 몇 종류여야 합니까?
3. `distance_km` 을 숫자로 못 바꾸는 값에는 어떤 것들이 있습니까?
"""
import numpy as np
import pandas as pd
import unicodedata

def clean_bikes(data, logger):
    """
        정제 함수. 단계마다 건수를 로그로 기록.

        [처리 순서]
        1. 숫자 타입 정제
        2. 종목 코드 정규화 (대문자, 공백 제거, ...)
        3. 중복 제거 (code,date 기준)
        4. 이상치 탐지 -> NaN 처리
        5. 결측 보간 (interpolate -> ffill -> bfill)
        6. OHLC 정합성
        7. 소수점 -> 정수 (반올림)
    """
    # station_id 정제
    data['station_id'] = data['station_id'].astype(str).str.upper()

    # bike_type 정제
    data['bike_type'] = data['bike_type'].astype(str).str.replace(r'\s+', '', regex=True)

    # gear_count 정제
    data['gear_count'] = data['gear_count'].astype(str).apply(lambda x: unicodedata.normalize('NFKC', x))

    # manufacture_year 정제
    data['manufacture_year'] = data['manufacture_year'].astype(str).str.replace("불명", np.nan)

    # daily_fee 정제
    data['daily_fee'] = data['daily_fee'].astype(str).str.replace(",","")
    data['daily_fee'] = pd.to_numeric(data['daily_fee'], errors='coerce')

    # 중복제거
    data = data.drop_duplicates(subset=['bike_id'])

    # 결측제거






















print(raw_bikes_df.info())
print("=" * 60)
# manufacture_year '불명' 때문에 문자열타입 / daily_fee  쌍 따옴표와 콤마 때문에 문자열로 고정
print(pd.DataFrame({'결측수' : raw_bikes_df.isna().sum(),'결측비' : raw_bikes_df.isna().mean().round(2)}))
print("=" * 60)
print(f"bike_id 중복 수 : {len(raw_bikes_df) - raw_bikes_df['bike_id'].nunique()}")
print("=" * 60)
print(f"{raw_bikes_df['bike_type'].value_counts()}")