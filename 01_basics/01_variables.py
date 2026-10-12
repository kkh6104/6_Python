"""
    변수와 자료형
"""

# 동적 타입 => 타입 선언 생략
name = "권경환"
age = 39
height = 176.7
is_tired = True         # False
temp = None             # java 에서 null과 통일

print(name, age, height, is_tired, temp)

print("=" * 60)
# 변수에 저장된 데이터 타입확인 => type(변수)
print("=" * 60)
# 변수에 저장된 데이터 타입 확인 => type(변수)
print(f"{name} : {type(name)}")
print(f"{age} : {type(age)}")
print(f"{height} : {type(height)}")
print(f"{is_tired} : {type(is_tired)}")
print(f"{temp} : {type(temp)}")

print("=" * 60)

value = 27
print(f"{value} : {type(value)}")
value = "스물일곱"
print(f"{value} : {type(value)}")

# 이전에 저장한 타입과 이후에 저장된 타입이 달라도 저장 가능
# --> 혼란을 방지하기 위해 하나의 변수에는 하나의 타입만 사용 (권장)

print("=" * 60)

# 다중 할당
x, y, z = 10, 20, 30
print(f"x, y, z -> {x}, {y}, {z}")

a = b = c = 0
print(f"a = b = c -> {a}, {b}, {c}")

# 값 교환
x, y = y, x
print(f"x, y -> {x}, {y}")

print("=" * 60)

# 타입 힌트
menu: str = "삼김"
print(f"menu : {menu} ({type(menu)})")

price: int = "12000원"
print(f"price : {price}({type(price)})")

# 타입 힌트는 강제성이 없으며 에러도 발생되지 않음!

print("=" * 60)
# 상수 -> 대문자로 변수를 작성하는 것을 약속(관례), final 키워드 x

# 최대 입원: 60 이라는 값을 저장
MAX_PERSON = 60
print(f"최대 인원 : {MAX_PERSON}")


# MAX_PERSON = 1
# print(f"최대 인원" {MAX_PERSON})