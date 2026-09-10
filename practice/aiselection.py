print("1" * 60)
"""
📝 [실습 1] 쇼핑몰 장바구니 품목 분석
온라인 쇼핑몰의 장바구니 데이터(제품명, 수량, 단가)가 딕셔너리 리스트로 주어집니다.
이 데이터를 바탕으로 분석 결과를 출력하는 analyze_cart(cart) 함수를 작성하세요.

요구사항:

각 품목의 총금액(수량 * 단가)을 계산하여 가장 지출이 큰 품목(제품명, 총금액)을 구하세요. (max와 key= 활용)

장바구니에 담긴 모든 품목의 전체 총금액을 구하세요. (sum 또는 reduce 활용)

함수는 ((최고지출품목명, 최고지출금액), 전체총금액) 형태로 반환하세요.

메인에서 반환값을 튜플 언패킹으로 받아 출력하세요.

입력 데이터:

Python
cart = [
    {"name": "노트북", "count": 1, "price": 1200000},
    {"name": "마우스", "count": 3, "price": 35000},
    {"name": "모니터", "count": 2, "price": 300000},
    {"name": "키보드", "count": 2, "price": 89000}
]
출력 예시:

Plaintext
========== 장바구니 분석 결과 ==========
- 가장 많은 돈을 쓴 품목: 노트북 (1,200,000원)
- 전체 결제 예정 금액: 1,978,000원
"""
cart = [
    {"name": "노트북", "count": 1, "price": 1200000},
    {"name": "마우스", "count": 3, "price": 35000},
    {"name": "모니터", "count": 2, "price": 300000},
    {"name": "키보드", "count": 2, "price": 89000}
]
def analyze_cart(cart):
    valueable = max(cart, key=lambda x: x["count"] * x["price"])
    return((valueable["name"], valueable["count"] * valueable["price"]), sum(item["count"] * item["price"] for item in cart))
print(analyze_cart(cart))

print("2" * 60)

"""
[실습 2] 단어 길이 기반 최장/최단 단어 및 정렬
사용자로부터 공백으로 구분된 문장을 입력받아, 단어의 길이를 기준으로 분석해 반환하는 analyze_words(sentence) 함수를 작성하세요.

요구사항:

입력받은 문장을 소문자로 변환한 뒤 단어 단위로 분리합니다. (.lower(), .split())

가장 길이가 길고 짧은 단어를 구하세요. (max, min과 key=len 활용)

모든 단어들을 글자 수가 긴 순서대로(내림차순) 정렬한 리스트를 만드세요. (sorted와 key=len 활용)

(가장긴단어, 가장짧은단어, 정렬된리스트)를 반환하고, 출력 예시처럼 나타내세요.

입력 예시:

Plaintext
문장을 입력하세요: Python is dynamic and powerful language
출력 예시:

Plaintext
========== 단어 분석 결과 ==========
- 가장 긴 단어: powerful (8글자)
- 가장 짧은 단어: is (2글자)
- 길이순 정렬: ['powerful', 'language', 'dynamic', 'python', 'and', 'is']
"""
def analyze_words(sentence):
    words = sentence.lower().split()
    l_word = max(words, key = len)
    s_word = min(words, key = len)
    return (l_word, s_word, sorted(words, reverse=True, key = len))

sentence = input("문장을 입력하세요: ")
lword, sword, words_list = analyze_words(sentence)
print()
print("========== 단어 분석 결과 ==========")
print(f"- 가장 긴 단어: {lword} ({len(lword)}글자)")
print(f"- 가장 짧은 단어: {sword} ({len(sword)}글자)")
print(f"- 길이순 정렬: {words_list}")



print("3" * 60)
"""
[실습 3] 직원 월급 및 부서별 통계 (응용)
직원 이름과 (부서, 월급) 튜플이 담긴 딕셔너리가 주어집니다.
월급을 기준으로 통계를 내는 analyze_employees(employees) 함수를 작성하세요.

요구사항:

가장 월급을 많이 받는 직원과 가장 적게 받는 직원의 이름과 월급을 구하세요. (max, min 활용)

전체 직원의 평균 월급을 계산하세요. (소수점 첫째 자리까지)

((최고월급자, 월급), (최저월급자, 월급), 평균월급)을 반환하고 언패킹하여 출력하세요.

입력 데이터:

Python
employees = {
    "김철수": ("개발팀", 520),
    "이영희": ("디자인팀", 380),
    "박민수": ("기획팀", 450),
    "최수진": ("개발팀", 610),
    "정우성": ("마케팅팀", 320)
}
출력 예시:

Plaintext
========== 직원 월급 통계 ==========
- 최고 연봉자: 최수진 (610만원)
- 최저 연봉자: 정우성 (320만원)
- 평균 월급: 458.0만원
"""
employees = {
    "김철수": ("개발팀", 520),
    "이영희": ("디자인팀", 380),
    "박민수": ("기획팀", 450),
    "최수진": ("개발팀", 610),
    "정우성": ("마케팅팀", 320)
}
def analyze_employees(employees):
    h = max(employees.items(), key=lambda x : x[1][1])
    l = min(employees.items(), key=lambda x : x[1][1])
    avg = sum(x[1] for x in employees.values()) / len(employees)
    return (h[0],h[1][1]), (l[0],l[1][1]), avg

h,l,avg = analyze_employees(employees)
print("========== 직원 월급 통계 ==========")
print(f"- 최고 연봉자: {h[0]} ({h[1]}만원)")
print(f"- 최저 연봉자: {l[0]} ({l[1]}만원)")
print(f"- 평균 월급: {avg:.1f}만원")




"""
📝 연습 문제: BankUser 클래스 만들기
다음 조건에 맞는 클래스를 하나 작성해 보세요.

클래스명: BankUser

필드 (생성자 __init__):

name (이름, 문자열)

__balance (잔액, 정수형, 비공개 필드로 선언)

Getter / Setter (@property):

@property를 사용해 balance 값을 조회할 수 있게 만드세요.

@balance.setter를 사용해 입금/출금을 처리하되, 음수 값이 들어오면 "잔액은 0원 이상이어야 합니다." 메시지를 출력하고 값을 바꾸지 마세요.

던더 메소드 (__str__):

print(user)를 실행하면 "[사용자이름] 님의 잔액: [잔액]원" 형태로 출력되도록 만드세요.

Python
# 아래 틀에 맞춰 작성해보세요!
class BankUser:
    def __init__(self, name, balance=0):
        # 작성할 위치
        pass

    # @property 작성 위치

    # @balance.setter 작성 위치

    # __str__ 작성 위치


# 테스트 코드
user = BankUser("권경환", 10000)
print(user)        # 권경환 님의 잔액: 10000원

user.balance = 20000
print(user.balance) # 20000

user.balance = -5000 # 잔액은 0원 이상이어야 합니다.
"""
class BankUser:
    def __init__(self, name, balance = 0):
        self.name = name
        self.__balance = balance

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            print("잔액은 0원 이상이어야 합니다.")
            return
        self.__balance = value

    def __str__(self):
        return f"[{self.name}] 님의 잔액: [{self.__balance}]원"

user = BankUser("권경환", 10000)
print(user)

user.balance = 20000
print(user.balance)

user.balance = -5000

"""
파이썬 OOP 종합 퀴즈 & 실습 문제
[문제 1] 쇼핑몰 장바구니 클래스 (__len__, __add__, __str__ 구현)
상품(Item) 객체들을 장바구니(Cart)에 담고, 던더 메소드를 활용해 수량 파악 및 장바구니 병합 기능을 구현하세요.

요구사항:

Item 클래스는 name과 price를 필드로 가집니다.

Cart 클래스는 내부 리스트(self.items)에 Item들을 저장합니다.

len(cart) 호출 시 장바구니에 담긴 전체 상품 개수를 반환하도록 __len__을 구현하세요.

cart1 + cart2 연산 시 두 장바구니의 상품이 합쳐진 새로운 Cart 객체를 반환하도록 __add__를 구현하세요.

print(cart) 호출 시 "장바구니 총 X개 상품 (총금액: Y원)" 형태로 출력되도록 __str__을 구현하세요.
"""