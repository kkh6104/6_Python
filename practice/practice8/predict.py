"""
## [STEP 1] 파생변수 생성 및 정답지(Target) 만들기

### 요구사항

`clean_rentals.csv`를 불러온 뒤 아래 파생변수들을 만드세요.

1. **대여 시간(분)**: `duration_min = return_time - rent_time` 의 분 단위 계산
2. **`is_overdue_100m` (예측 대상)**: 대여 시간(`duration_min`)이 100분(1시간 40분)을 초과하면 `1`, 아니면 `0`
3. 대여 시점(`rent_time`) 기준 **시간대(hour)** 와 **요일** 추출
- 전체 행 수와 **`is_overdue_100m` 의 비율**을 확인하세요.
- **"전부 정상(미반납 아님)"이라고 답할 때의 정확도**를 계산하세요. 담당자가 말한 "정확도 84%"의 정체가 바로 이것입니다.

"""
import pandas as pd

pd.read_csv("data/clean_rentals.csv", date_format="mixed", parse_dates=["rent_time", "return_time"])