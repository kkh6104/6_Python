print("1" * 60)
"""
### 1. 몸무게(kg)와 키(cm)를 입력받아 BMI 지수를 계산하는 함수를 정의

- BMI = 몸무게(kg) / (키(m) * 키(m))
- 키는 cm로 입력받아 m로 변환

#### 입출력 예시

```
몸무게를 입력하세요(kg): 70
키를 입력하세요(cm): 175

BMI: 22.86
```
"""
weight = int(input("몸무게를 입력하세요(kg): "))
height = int(input("키를 입력하세요(cm): "))
print()
print(f"BMI: {weight / ((height / 100) ** 2):.2f}")
print("2" * 60)
"""
### 2. 여러 개의 숫자를 입력받아 평균을 계산하는 함수를 정의

- 사용자가 'q'를 입력할 때까지 숫자를 계속 입력받음 (입력받는 개수는 정해져 있지 않음)
- 평균 = 총합 / 총개수
- 반올림 함수: `round(숫자, 자릿수)`

#### 입출력 예시

```
========== 평균 계산기 ==========
숫자 입력 (q 입력 시 종료) : 1
숫자 입력 (q 입력 시 종료) : 4
숫자 입력 (q 입력 시 종료) : 5
숫자 입력 (q 입력 시 종료) : q

---> 평균: 3.33
```

```
========== 평균 계산기 ==========
숫자 입력 (q 입력 시 종료) : 1
숫자 입력 (q 입력 시 종료) : q

---> 평균: 1.0
```

```
========== 평균 계산기 ==========
숫자 입력 (q 입력 시 종료) : q

---> 값이 없습니다.
```
"""
numbers = []
while True:
    number = input("숫자 입력 (q 입력 시 종료) : ")
    if number == 'q':
        break
    number = int(number)
    numbers.append(number)
print()
if len(numbers) == 0:
    print("---> 값이 없습니다.")
else:
    print(f"---> 평균: {sum(numbers)/len(numbers):.2f}")
print("3" * 60)
"""
### 3. 단어 빈도수 분석 함수 정의

- 문장(문자열)을 입력받아 공백 단위로 단어를 분리하고, 각 단어의 등장 횟수를 딕셔너리로 계산하여 반환
- 대소문자를 구분하지 않도록 모든 문자를 소문자로 변환하여 처리
- 소문자 변환: `.lower()`
- 문자열 분리: `.split()`

#### 입출력 예시

```
문장을 입력하세요: Python is fun and Python is powerful

[단어 빈도수 결과]
- python: 2회
- is: 2회
- fun: 1회
- and: 1회
- powerful: 1회
```
"""
text = input("문장을 입력하세요: ").lower()
words = text.split()
result = {n : words.count(n) for n in words}
print()
print("[단어 빈도수 결과]")
for key in result:
    print(f"- {key}: {result[key]}회")
print("4" * 60)
"""
### 4. 로또 번호 자동 생성 함수 정의

- 1부터 45 사이의 서로 다른 무작위 숫자 6개를 생성한 후 오름차순으로 정렬하여 반환
- 구매할 게임 수를 입력받아 해당 횟수만큼 로또 번호 세트를 출력
- 정렬: `sorted()`
- 난수: `import random` 후 `random.randint(1, 45)` 활용

#### 입출력 예시

```
구매할 로또 게임 수를 입력하세요: 3

[로또 번호 발급 결과]
1게임: [3, 12, 19, 25, 33, 42]
2게임: [1, 7, 14, 28, 35, 40]
3게임: [5, 11, 21, 22, 38, 45]
```
"""
import random
numbers = set()
times = int(input("구매할 로또 게임 수를 입력하세요: "))
print()
print("[로또 번호 발급 결과]")
for i in range(1, times + 1):
    while len(numbers) < 6:
        numbers.add(random.randint(1, 45))
    print(f"{i}게임: {sorted(numbers)}")
    numbers = set()
print("5" * 60)
"""
### 5. 학생 성적 통계 분석 함수 정의

- 학생들의 이름과 점수가 담긴 딕셔너리를 전달받아 최고 득점자, 최저 득점자, 전체 평균 점수를 계산하여 반환
- 반환값은 `((최고득점자, 점수), (최저득점자, 점수), 평균점수)` 형태로 반환
- 함수 호출 후 반환값을 튜플 언패킹(Unpacking)으로 받아 결과 출력
- **데이터 예시:**
    
    ```python
    {
        "홍길동": 85,
        "이순신": 96,
        "강감찬": 72,
        "유관순": 91
    }
    ```
    

#### 입출력 예시

```
========== 학생 성적 분석 결과 ==========
- 최고 득점자: 이순신 (96점)
- 최저 득점자: 강감찬 (72점)
- 전체 평균: 86.0점
```
"""
data = {
    "홍길동": 85,
    "이순신": 96,
    "강감찬": 72,
    "유관순": 91
}
def analyze(data):
    h_name = max(data, key = data.get)
    l_name = min(data, key = data.get)
    avg = (sum(data.values())/len(data))
    return (h_name, data[h_name]),(l_name, data[l_name]),avg
(h_name, h_score), (l_name, l_score), avg = analyze(data)
print("========== 학생 성적 분석 결과 ==========")
print(f"- 최고 득점자: {h_name} ({h_score}점)")
print(f"- 최저 득점자: {l_name} ({l_score}점)")
print(f"- 전체 평균: {avg:.1f}점")
"""
from functools import reduce 
highest = reduce(lambda result, curr: result if data[result] >= data[curr] else curr, data)
lowest = reduce(lambda result, curr: result if data[result] < data[curr] else curr, data)
print("========== 학생 성적 분석 결과 ==========")
print(f"- 최고 득점자: {highest} ({data[highest]}점)")
print(f"- 최저 득점자: {lowest} ({data[lowest]}점)")
print(f"- 전체 평균: {(sum(data.values())/len(data)):.1f}점")
"""