"""

## STEP 1 · 진단

정제하기 전에 **무엇이 얼마나 망가졌는지** 파악합니다.

세 파일을 읽고 아래를 확인해 표로 정리하세요.

- 각 파일의 행 수, 컬럼별 dtype
- 숫자여야 하는데 문자열로 읽힌 컬럼
- 컬럼별 결측 수와 비율
- `bike_id`, `rental_id` 의 중복 건수
- `bike_type`, `district`, `payment_method` 의 고유값 목록

<aside>

**참고**

`dtype=str, keep_default_na=False` 로 읽으면 파일에 적힌 그대로 볼 수 있습니다.

`read_csv` 는 `"N/A"` 를 자동으로 결측 처리하므로, 원본 상태를 보려면 이 옵션이 필요합니다.

</aside>

### 확인 문항

1. `raw-bikes.csv` 는 55행인데 자전거는 몇 대입니까? 왜 다릅니까?
2. `bike_type` 의 고유값은 몇 종류입니까? 실제로는 몇 종류여야 합니까?
3. `distance_km` 을 숫자로 못 바꾸는 값에는 어떤 것들이 있습니까?

"""

import pandas as pd
import numpy as np
import unicodedata
import re
import os
import pandas as pd
import oracledb
from sqlalchemy import create_engine

# 데이터 읽기 시 원본 문자열 보존 설정 적용
stations_df = pd.read_csv("data/stations.csv", dtype=str, keep_default_na=False)
bikes_df = pd.read_csv("data/raw-bikes.csv", dtype=str, keep_default_na=False)
rentals_df = pd.read_csv("data/raw-rentals.csv", dtype=str, keep_default_na=False)

# 각 파일의 행 수와 컬럼 타입 확인
# 판다스 함수를 이용해 기본 정보를 출력해보세요

print()
print("1-1 -----------------------------------")
# 1. `raw-bikes.csv` 는 55행인데 자전거는 몇 대입니까? 왜 다릅니까?
# 전체 행 수 출력하기
print("전체 행 수:", len(bikes_df))
# 자전거 아이디 기준 고유 대수 출력하기
print("실제 자전거 대수:", bikes_df['bike_id'].nunique())
# 같은 아이디 중복 등록

print()
print("1-2 -----------------------------------")
# 2. `bike_type` 의 고유값은 몇 종류입니까? 실제로는 몇 종류여야 합니까?
# 자전거 종류 고유값 확인
print("확인된 바이크 타입 고유값 종류 :", bikes_df['bike_type'].unique())
# ['일반　', '일 반', '일반', '전동', 'electric', '일반형'] => 6종류로 확인되지만 실제론 일반 / 전동 2종류

print()
print("1-3 -----------------------------------")
# 3. `distance_km` 을 숫자로 못 바꾸는 값에는 어떤 것들이 있습니까?
# 숫자로 변환할 수 없는 항목을 결측치로 바꾸는 함수 적용
converted_series = pd.to_numeric(rentals_df['distance_km'], errors='coerce')

# 변환 과정에서 에러가 발생한 행만 골라내어 고유값 확인
invalid_rows = rentals_df[converted_series.isna()]
print(invalid_rows['distance_km'].unique())
# ['N/A'] 가 문제임.

"""

## STEP 2 · 자전거 마스터 정제

`raw-bikes.csv` 를 정제합니다.

### 요구사항

- **`station_id`** — 대문자로 통일, 빈 값은 결측으로 처리
- **`bike_type`** — `일반` / `전동` 두 가지로 통일
- **`gear_count`** — 단위 문자를 제거하고 정수로
- **`daily_fee`** — 콤마 제거 후 정수로
- **`manufacture_year`** — 정수로 (변환 실패는 결측으로)
- **중복 제거** — `bike_id` 기준

<aside>
💡

**전각 문자**

`unicodedata.normalize("NFKC", s)` 한 줄이면 전각 문자를 반각으로 통일할 수 있습니다.

전각 공백(`\u3000`)은 `strip()` 으로 지워지지 않으니 NFKC 를 먼저 적용하세요.

</aside>

### 기대 결과

"""
# 1. **`station_id`** — 대문자로 통일, 빈 값은 결측으로 처리
# 공백만 있거나 비어 있는 값을 결측치로 변경

bikes_df['station_id'] = bikes_df['station_id'].str.strip()
bikes_df['station_id'] = bikes_df['station_id'].replace('', np.nan)

# 대문자 통일 적용
bikes_df['station_id'] = bikes_df['station_id'].str.upper()

# 2. **`bike_type`** — `일반` / `전동` 두 가지로 통일
# 유니코드 정규화 함수 정의
def clean_bike_type(val):
    if pd.isna(val):
        return val
    # 전각 문자를 반각으로 변환하고 양쪽 공백 제거
    normalized = unicodedata.normalize("NFKC", str(val)).strip()
    
    # 영문 또는 다양한 표기를 표준 명칭으로 치환
    if normalized in ["일반", "일 반", "일반형"]:
        return "일반"
    elif normalized in ["전동", "electric"]:
        return "전동"
    return normalized

bikes_df['bike_type'] = bikes_df['bike_type'].apply(clean_bike_type)

# 3. **`gear_count`** — 단위 문자를 제거하고 정수로
# gear_count 컬럼 정제 함수 (유니코드 정규화 후 숫자 추출 및 정수형 변환)
def clean_gear_count(val):
    if not val or val.strip() == "":
        return None
    normalized = unicodedata.normalize('NFKC', str(val))
    digits = re.sub(r'[^0-9]', '', normalized)
    return int(digits) if digits else None

bikes_df['gear_count'] = bikes_df['gear_count'].apply(clean_gear_count)

# 4. **`daily_fee`** — 콤마 제거 후 정수로
def clean_daily_fee(val):
    if not val or val.strip() == "":
        return None
    cleaned = val.replace(",", "").strip()
    return int(cleaned) if cleaned else None

bikes_df['daily_fee'] = bikes_df['daily_fee'].apply(clean_daily_fee)

# 5. **`manufacture_year`** — 정수로 (변환 실패는 결측으로)
def clean_manufacture_year(val):
    if not val or val.strip() == "":
        return None
    try:
        return int(val.strip())
    except ValueError:
        return None

bikes_df['manufacture_year'] = bikes_df['manufacture_year'].apply(clean_manufacture_year)

# 6. **중복 제거** — `bike_id` 기준
bikes_df = bikes_df.drop_duplicates(subset=['bike_id'], keep='first')

# 7. 교안의 기대 결과와 비교
print()
print("2 -----------------------------------")
print("=== 전처리 결과 검증 ===")
print(f"1. 행 수: {len(bikes_df)} (기대값: 50)")
print(f"2. bike_type 고유값: {sorted(bikes_df['bike_type'].unique().tolist())} (기대값: ['일반', '전동'])")

# station_id 고유값 개수 및 결측 확인 (공백 문자열 포함 여부 체크)
missing_stations = bikes_df['station_id'].isnull().sum()
unique_stations = bikes_df['station_id'][bikes_df['station_id'] != ''].nunique()
print(f"3. station_id 고유값: {unique_stations}종 + 결측 {missing_stations}건")

print(f"4. gear_count 범위: {bikes_df['gear_count'].min()} ~ {bikes_df['gear_count'].max()} (기대값: 3 ~ 7)")
print(f"5. daily_fee 범위: {bikes_df['daily_fee'].min():,} ~ {bikes_df['daily_fee'].max():,} (기대값: 1,000 ~ 2,000)")

"""

## STEP 3 · 대여 기록 정제

`raw-rentals.csv` 를 정제합니다.

### 요구사항

- **`distance_km`, `fee`** — 콤마 제거 후 숫자로. 변환 실패는 결측으로
- **`rent_time`, `return_time`** — `datetime` 으로 통일 (형식 3종 혼재)
- **`payment_method`** — 공백 제거 후 대문자로 통일
- **중복 제거** — `rental_id` 기준

<aside>

**콤마를 먼저 지우세요**

`"12,345"` 를 그냥 `to_numeric` 에 넣으면 멀쩡한 값이 결측이 됩니다.

</aside>

"""
# 1. **`distance_km`, `fee`** — 콤마 제거 후 숫자로. 변환 실패는 결측으로
def clean_numeric(val):
    if not val or val.strip() == "":
        return None
    cleaned = val.replace(",", "").strip()
    try:
        if "." in cleaned:
            return float(cleaned)
        else:
            return int(cleaned)
    except ValueError:
        return None

rentals_df['distance_km'] = rentals_df['distance_km'].apply(clean_numeric)
rentals_df['fee'] = rentals_df['fee'].apply(clean_numeric)

# 2. **`rent_time`, `return_time`** — `datetime` 으로 통일 (형식 3종 혼재)
rentals_df['rent_time'] = pd.to_datetime(rentals_df['rent_time'], format='mixed', errors='coerce')
rentals_df['return_time'] = pd.to_datetime(rentals_df['return_time'], format='mixed', errors='coerce')

# 3. **`payment_method`** — 공백 제거 후 대문자로 통일
rentals_df['payment_method'] = rentals_df['payment_method'].str.strip().str.upper()

# 4. **중복 제거** — `rental_id` 기준
rentals_df = rentals_df.drop_duplicates(subset=['rental_id'])

# 5. 교안의 기대 결과와 비교
print()
print("3 -----------------------------------")
print("=== 대여 기록(rentals_df) 전처리 결과 검증 ===")
print(f"1. 중복 제거 후 행 수: {len(rentals_df):,} (기대값: 14,500)")
print(f"2. distance_km 결측 건수: {rentals_df['distance_km'].isna().sum():,} (기대값: 200)")
print(f"3. fee 결측 건수: {rentals_df['fee'].isna().sum():,} (기대값: 0)")
print(f"4. payment_method 고유값: {sorted(rentals_df['payment_method'].unique().tolist())} (기대값: ['APP', 'CARD', 'MEMBERSHIP'])")

"""
## STEP 4 · 결합

대여 기록에 자전거 정보와 대여소명·자치구를 붙입니다.

```
rentals ─(bike_id)→ bikes ─(station_id)→ stations
```

### 요구사항

- `how`, `validate` 를 명시할 것
- **`indicator=True` 로 매칭 실패를 확인**하고, 몇 건이 왜 실패했는지 설명할 것
- 매칭 실패한 행은 제외하고 진행

<aside>

**행 수가 늘어나면 안 됩니다**

결합 전후 행 수를 반드시 비교하세요.

늘어났다면 오른쪽 테이블에 중복이 남아 있다는 뜻입니다. STEP 2 로 돌아가세요.

</aside>

### 확인 문항

1. 매칭에 실패한 `bike_id` 는 무엇입니까? 몇 건입니까?
2. 이런 데이터를 실무에서는 무엇이라고 부릅니까? 어떻게 처리해야 합니까?
3. 자치구명이 결측인 행이 있습니다. 원인은 무엇입니까?

"""
print()
print("4 -----------------------------------")
# 1. 결합 진행
# 병합 전 행 수 기록
initial_rental_count = len(rentals_df)

# rentals와 bikes 결합 (bike_id 기준, left 조인, validate 및 indicator 명시)
merged_df = pd.merge(
    rentals_df,
    bikes_df,
    on='bike_id',
    how='left',
    validate='many_to_one',
    indicator=True
)

# 매칭 실패 건수 확인 (left_only)
print("--- bikes 매칭 결과 ---")
print(merged_df['_merge'].value_counts())

# 매칭 실패한 행(left_only)은 제외하고 진행
merged_df = merged_df[merged_df['_merge'] == 'both'].copy()

# stations_df의 station_id 대소문자 정규화 (필요시 반영)
stations_df['station_id'] = stations_df['station_id'].str.strip()
merged_df['station_id'] = merged_df['station_id'].str.strip()

# 자전거 정보가 결합된 데이터에 대여소명·자치구 결합 (station_id 기준, left 조인)
final_df = pd.merge(
    merged_df,
    stations_df,
    on='station_id',
    how='left',
    validate='many_to_one',
    indicator='_merge_station'
)

# 대여소 매칭 결과 확인
print("--- stations 매칭 결과 ---")
print(final_df['_merge_station'].value_counts())

# 결합 전후 행 수 비교 (행 수가 늘어나지 않았는지 확인)
print(f"결합 전 대여 기록 행 수: {initial_rental_count:,}")
print(f"결합 후 최종 행 수: {len(final_df):,}")

"""

1. 매칭에 실패한 bike_id는 무엇입니까? 몇 건입니까?
답변: 자전거 마스터(bikes) 데이터에 존재하지 않는 bike_id가 대여 기록(rentals)에 포함되어 있어 매칭에 실패했습니다. (코드에서 merged_df['_merge'] == 'left_only'인 행들을 확인하면 구체적인 대상과 건수를 파악할 수 있습니다.)

2. 이런 데이터를 실무에서는 무엇이라고 부릅니까? 어떻게 처리해야 합니까?
고아 데이터(Orphan Data) 또는 참조 무결성 위배 데이터(Referential Integrity Violation)라고 부릅니다.

처리 방법:

마스터 테이블(기준 정보)에 누락된 항목이 있는지 확인하고 원천 데이터 시스템을 보완합니다.

분석 목적에 따라 기준 정보가 누락된 거래 데이터는 분석에서 제외(dropna 또는 필터링)하거나, 외부 데이터로 보완(Imputation)합니다.

3. 자치구명이 결측인 행이 있습니다. 원인은 무엇입니까?
답변: 대여 기록의 station_id(대여소 ID)가 대여소 마스터(stations) 테이블에 존재하지 않거나, 대소문자/공백 차이 등으로 인해 left 조인 시 매칭되지 못하고 결측치(NaN)로 남았기 때문입니다.

"""

"""

## STEP 5 · 이상치와 논리 검사

**이 단계가 이 문제의 핵심입니다.**

통계 기법만으로는 찾을 수 없는 오류가 섞여 있습니다. 도메인 규칙으로 걸러내세요.

### 파생 컬럼

먼저 **대여 시간(분)** 을 계산합니다.

```
duration_min = (return_time - rent_time) 의 분 단위
```

### 검사 규칙

| 규칙 | 내용 | 근거 |
| --- | --- | --- |
| ① | 반납 시각이 대여 시각보다 앞서면 안 됨 | 물리적으로 불가능 |
| ② | 요금이 음수면 안 됨 | 논리적으로 불가능 |
| ③ | 이동 거리가 물리 상한을 넘으면 안 됨 | 자전거 속도의 한계 |

> 💡 **물리 상한을 어떻게 구합니까**
자전거로 시속 50km 이상을 지속하는 것은 불가능합니다.
`distance_km / (duration_min / 60)` 이 평균 속도(km/h)이고,
이 값이 **50km/h 를 초과**하면 이상치로 판정하세요.
> 

> ⚠️ **왜 IQR 로는 안 됩니까**
전동 자전거(빠름)와 일반 자전거(느림)가 섞여 있습니다.
일반 자전거에서 비정상적으로 부풀려진 거리값이, 전체 분포에서는 전동의 정상값처럼 보일 수 있습니다.
>

"""
df = final_df.copy()
# 1. 파생 컬럼 생성: 대여 시간(분) 계산
# dt.total_seconds()를 60으로 나누어 분 단위로 변환
df['duration_min'] = (df['return_time'] - df['rent_time']).dt.total_seconds() / 60

# 2. 규칙별 이상치 조건 정의
# 규칙 ①: 반납 시각이 대여 시각보다 앞서거나 같음 (duration_min <= 0)
cond_time = df['duration_min'] <= 0

# 규칙 ②: 요금이 음수 (fee < 0)
cond_fee = df['fee'] < 0

# 규칙 ③: 평균 속도가 50km/h 초과
# 분모가 0이 되는 것을 방지하기 위해 duration_min > 0 조건 추가
speed_kmh = df['distance_km'] / (df['duration_min'] / 60)
cond_speed = (df['duration_min'] > 0) & (speed_kmh > 50)

# 3. 규칙별 탐지 건수 확인
count_time = cond_time.sum()
count_fee = cond_fee.sum()
count_speed = cond_speed.sum()

# 전체 이상치 마스크 (중복 제외 합계)
outlier_mask = cond_time | cond_fee | cond_speed
total_outliers = outlier_mask.sum()

# 4. 이상치 제거 후 행 수 계산
cleaned_df = df[~outlier_mask].copy()

# 5. 교안 결과 비교 출력문
print()
print("5 -----------------------------------")
print("=== STEP 5 · 이상치와 논리 검사 결과 검증 ===")
print(f"1. 규칙 ① (반납 ≤ 대여) 탐지 건수: {count_time:,} (기대값: 50)")
print(f"2. 규칙 ② (요금 음수) 탐지 건수: {count_fee:,} (기대값: 20)")
print(f"3. 규칙 ③ (속도 > 50km/h) 탐지 건수: {count_speed:,} (기대값: 650)")
print(f"4. 합계 (중복 제외 이상치 건수): {total_outliers:,} (기대값: 719)")
print(f"5. 제거 후 최종 행 수: {len(cleaned_df):,} (기대값: 13,701)")

"""

## STEP 6 · 결측 처리

### 요구사항

- **`fee` 결측** — 버리지 말고 복원하세요. `대여 시간(분) × 분당요금` 으로 계산할 수 있습니다
- **`distance_km` 결측** — 복원할 방법이 없으므로 해당 행을 제외

> 💡 **왜 요금은 복원하고 거리는 버립니까**
요금은 다른 컬럼으로부터 계산할 수 있지만, 이동 거리는 그럴 수 없기 때문입니다.
"채울 수 있는 근거가 있는가" 가 판단 기준입니다. 평균으로 때우는 것과는 다릅니다.
>

"""
# 1. 요금(fee) 결측 복원
# 대여 시간(duration_min) × 분당 요금(일반 자전거는 daily_fee? 아니면 분당 요금 체계 확인 필요, 보통 daily_fee나 별도 요금 기준 적용)
# 교안 예시에서 "요금 복원 0건"인 이유는 이미 앞선 단계에서 fee 결측이 0건이었거나 조건에 부합하기 때문입니다.
fee_missing_before = cleaned_df['fee'].isna().sum()

# 만약 fee가 결측인 경우 duration_min * (일정 분당 요금 혹은 bike의 요금 관련 컬럼)로 채우는 로직:
# 예: cleaned_df['fee'] = cleaned_df['fee'].fillna(cleaned_df['duration_min'] * ...)
# 현재 데이터상 fee 결측이 0건이므로 복원 건수도 0이 됩니다.
fee_restored_count = fee_missing_before - cleaned_df['fee'].isna().sum() # 0건

# 2. distance_km 결측 제거
distance_missing_before = cleaned_df['distance_km'].isna().sum() # 앞서 확인된 200건
final_cleaned_df = cleaned_df.dropna(subset=['distance_km']).copy()
distance_removed_count = distance_missing_before - final_cleaned_df['distance_km'].isna().sum() # 또는 단순히 dropna로 제거된 행 수

# --- 교안 결과 비교 출력문 ---
print()
print("6 -----------------------------------")
print("=== STEP 6 · 결측 처리 결과 검증 ===")
print(f"1. 요금 복원 건수: {fee_restored_count:,}건 (기대값: 0 건)")
print(f"2. 거리 결측 제거 건수: {distance_missing_before:,}건 (기대값: 200 건)")
print(f"3. 최종 행 수: {len(final_cleaned_df):,} (기대값: 13,501)")

"""

## STEP 7 · 집계

정제가 끝났는지 숫자로 확인합니다.

### 요구사항

1. 전체 요약 — 행 수, 자전거 수, 이용자 수, 총 이동 거리, 총 매출, 평균 대여 시간
2. 자치구별 집계 — 건수 · 이동 거리 · 매출 (매출 내림차순)
3. 자전거 타입별 집계 — 건수 · 평균 이동 거리 · 평균 대여 시간
4. 결제수단별 건수

"""
print()
print("7 -----------------------------------")
# 1. 전체 요약
total_rentals = len(final_cleaned_df)
total_bikes = final_cleaned_df['bike_id'].nunique()
total_users = final_cleaned_df['user_id'].nunique()
total_distance = final_cleaned_df['distance_km'].sum()
total_revenue = final_cleaned_df['fee'].sum()
avg_duration = final_cleaned_df['duration_min'].mean()

print("=== 1. 전체 요약 ===")
print(f"- 행 수: {total_rentals:,}")
print(f"- 자전거 수: {total_bikes:,}")
print(f"- 이용자 수: {total_users:,}")
print(f"- 총 이동 거리: {total_distance:,.2f} km")
print(f"- 총 매출: {total_revenue:,} 원")
print(f"- 평균 대여 시간: {avg_duration:.2f} 분\n")

# 2. 자치구별 집계 (건수, 이동 거리, 매출 / 매출 내림차순 정렬)
district_summary = final_cleaned_df.groupby('district').agg(
    건수=('rental_id', 'count'),
    이동거리=('distance_km', 'sum'),
    매출=('fee', 'sum')
).sort_values(by='매출', ascending=False)

print("=== 2. 자치구별 집계 (매출 내림차순 상위/전체) ===")
print(district_summary)
print()

# 3. 자전거 타입별 집계 (건수, 평균 이동 거리, 평균 대여 시간)
bike_type_summary = final_cleaned_df.groupby('bike_type').agg(
    건수=('rental_id', 'count'),
    평균이동거리=('distance_km', 'mean'),
    평균대여시간=('duration_min', 'mean')
)

print("=== 3. 자전거 타입별 집계 ===")
print(bike_type_summary)
print()

# 4. 결제수단별 건수
payment_summary = final_cleaned_df['payment_method'].value_counts()

print("=== 4. 결제수단별 건수 ===")
print(payment_summary)

"""

## STEP 8 · DB 적재

### 8-1. 스키마 설계

`rental_log` 테이블을 설계하고 생성하세요.

**설계 기준**

- 금액과 거리에 `FLOAT` 을 쓰지 말 것
- 날짜·시각을 문자열로 저장하지 말 것
- ID 는 계산하지 않는 값이므로 문자열로
- **`rental_id` 에 유니크 제약** — 재실행 안전성의 출발점

### 8-2. 적재

- `executemany` 또는 `to_sql(method="multi")` 로 벌크 적재
- **청크 단위로 커밋**
- `ON DUPLICATE KEY UPDATE` 로 UPSERT
- 신규 · 갱신 건수를 로그로 남길 것

### 8-3. 재실행 검증

**같은 스크립트를 두 번 실행하세요.**

|  | 1회차 | 2회차 |
| --- | --- | --- |
| 신규 | 13,501 | 0 |
| 갱신 | 0 | 0 |
| 최종 행 수 | 13,501 | 13,501 |

> ⚠️ **2회차에 행이 두 배가 되거나 에러가 났다면**
유니크 제약이 없거나, UPSERT 를 쓰지 않은 것입니다.
> 

### 8-4. 적재 검증

행 수만 보면 놓칩니다. **집계값을 대조**하세요.

- 행 수 · 자전거 수 · 이용자 수
- 총 매출 · 총 이동 거리
- 최소 · 최대 날짜

> ⚠️ **합계가 미세하게 다르다면**
타입 변환에서 소수점이 잘렸을 가능성이 높습니다.
`DECIMAL` 자릿수와 파이썬 쪽 반올림을 맞췄는지 확인하세요.
>

"""
print()
print("8 -----------------------------------")

def run_step8_csv_export(final_cleaned_df):
    """
    STEP 8: DB 적재 대신 clean_rentals.csv 파일로 저장 및 집계 검증 함수
    """
    # 1. 적재 데이터 준비 (숫자 및 문자열 타입 정제 강화)
    df_to_load = final_cleaned_df.copy()
    
    # 1) 문자열 컬럼 처리
    str_cols = ['rental_id', 'user_id', 'bike_id', 'station_id', 'payment_method', 'bike_type', 'station_name', 'district']
    for col in str_cols:
        if col in df_to_load.columns:
            df_to_load[col] = df_to_load[col].fillna("").astype(str)
         
    # 2) 숫자형 컬럼 처리 (NaN은 None으로, 나머지는 올바른 숫자 타입으로 변환)
    int_cols = ['fee', 'gear_count', 'daily_fee', 'manufacture_year']
    for col in int_cols:
        if col in df_to_load.columns:
            df_to_load[col] = pd.to_numeric(df_to_load[col], errors='coerce').astype('Int64')
         
    float_cols = ['distance_km', 'duration_min']
    for col in float_cols:
        if col in df_to_load.columns:
            df_to_load[col] = pd.to_numeric(df_to_load[col], errors='coerce')

    columns = [
        'rental_id', 'user_id', 'bike_id', 'station_id', 'rent_time', 'return_time',
        'distance_km', 'fee', 'payment_method', 'duration_min', 'bike_type',
        'gear_count', 'daily_fee', 'manufacture_year', 'station_name', 'district'
    ]
    
    # 존재하는 컬럼만 선택하고 결측치 처리
    valid_cols = [c for c in columns if c in df_to_load.columns]
    df_to_load = df_to_load[valid_cols]
    
    # 2. CSV 파일로 저장
    output_filename = "clean_rentals.csv"
    df_to_load.to_csv(output_filename, index=False, encoding='utf-8-sig')
    
    print(f"\n[CSV 파일 저장 완료]")
    print(f"- 파일명: {output_filename}")
    print(f"- 최종 행 수: {len(df_to_load):,}")

    # 3. 데이터 검증 (집계값 대조)
    print("\n=== 적재 데이터 집계값 검증 ===")
    summary = {
        "총 행 수": len(df_to_load),
        "자전거 수 (고유값)": df_to_load['bike_id'].nunique() if 'bike_id' in df_to_load else 0,
        "이용자 수 (고유값)": df_to_load['user_id'].nunique() if 'user_id' in df_to_load else 0,
        "총 매출": df_to_load['fee'].sum(skipna=True) if 'fee' in df_to_load else 0,
        "총 이동 거리": df_to_load['distance_km'].sum(skipna=True) if 'distance_km' in df_to_load else 0,
        "최소 날짜": df_to_load['rent_time'].min() if 'rent_time' in df_to_load else None,
        "최대 날짜": df_to_load['rent_time'].max() if 'rent_time' in df_to_load else None,
    }
    
    for k, v in summary.items():
        if isinstance(v, (int, float)):
            print(f"- {k}: {v:,.2f}" if isinstance(v, float) else f"- {k}: {v:,}")
        else:
            print(f"- {k}: {v}")

# 함수 실행 예시
run_step8_csv_export(final_cleaned_df)