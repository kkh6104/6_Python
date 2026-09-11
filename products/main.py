# 사용자 메뉴 루프 진입점

from models import *        # * 사용을 지양해야하지만 미니프로젝트인 관계상 다 사용되어서 사용하겠습니다
from inventory import *
from datetime import date, timedelta
import sys

"""
main.py에는 사용자가 번호를 입력하여 기능을 선택하는 반복 메뉴(while 루프) 를 구현해야 합니다.
"""

# 제미나이가 생성해 준 더미데이터
data = [
    # 1. 일반 상품 (GeneralProduct: 위험물 여부 True/False)
    GeneralProduct("G001", "모니터 세정제", 12000, 50, is_danger=False),
    GeneralProduct("G002", "산업용 알코올", 25000, 15, is_danger=True),
    GeneralProduct("G003", "사무용 키보드", 45000, 8, is_danger=False),  # 재고 10개 미만 (긴급)
    GeneralProduct("G004", "부탄가스 4팩", 6000, 120, is_danger=True),

    # 2. 신선 식품 (FreshProduct: 유통기한 날짜 지정)
    # 오늘 기준 유통기한 임박 상품 (3일 이내 -> get_price() 호출 시 50% 할인 적용)
    FreshProduct("F001", "유기농 우유 1L", 3800, 20, expiration_date=date.today() + timedelta(days=2)),
    FreshProduct("F002", "신선 샐러드", 6500, 5, expiration_date=date.today() + timedelta(days=1)), # 할인 + 재고 부족
    
    # 여유 있는 신선 상품 (정가 적용)
    FreshProduct("F003", "국산 계란 30구", 8900, 40, expiration_date=date.today() + timedelta(days=10)),
    FreshProduct("F004", "돼지 삼겹살 500g", 15000, 3, expiration_date=date.today() + timedelta(days=5))  # 재고 부족
]

while True:
    print("-" * 80)
    print(" 재 고 관 리 프 로 그 램 ")
    print("-" * 80)
    print("1. 전체 재고 확인")
    print("2. 긴급 발주 필요 목록 확인")
    print("3. 전체 재고의 총 금액 확인")
    print("4. 입고 진행")
    print("5. 출고 진행")
    print("6. 단가 수정")
    print("7. 단종 품목 삭제")
    print("9. 전체 정보 확인")
    print("0. 프로그램 종료")
    menu = input("메뉴를 입력해주세요: ")
    match menu:
        case '0':
            print("프로그램을 종료하겠습니다.")
            sys.exit()
        case '1':
            li = check_inventory(data)
            for l in li:
                print(f"상품 코드: {l[0]},\t품명: {l[1]},\t재고 수량: {l[2]}")
            continue
        case '2':
            li = check_urgent(data)
            for l in li:
                print(f"상품 코드: {l[0]},\t품명: {l[1]},\t재고 수량: {l[2]}")
            continue
        case '3':
            print(f"재고 총 판매금액: {total_price(data)}")
            continue
        case '4':
            code = input("상품 코드를 입력해주세요(일반G / 신선F 001~004): ")
            try:
                amount = int(input("입고할 수량을 입력해주세요: "))
                print(inbound(data, code, amount))
            except ValueError:
                print("숫자를 입력해주세요.")
            except InputNumberError as e:
                print(e)
            except ProductNotFoundError as e:
                print(e)
            finally:
                continue
        case '5':
            code = input("상품 코드를 입력해주세요(일반G / 신선F 001~004): ")
            try:
                amount = int(input("출고할 수량을 입력해주세요: "))  
                print(outbound(data, code, amount))
            except ValueError:
                print("숫자를 입력해주세요.")
            except InputNumberError as e:
                print(e)
            except ExceedStockError as e:
                print(e)
            except ProductNotFoundError as e:
                print(e)
            finally:
                continue
        case '6':
            code = input("상품 코드를 입력해주세요(일반G / 신선F 001~004): ")
            try:
                value = int(input("판매할 단가를 입력해주세요: "))  
                print(adjust(data, code, value))
            except ValueError:
                print("숫자를 입력해주세요.")
            except InputNumberError as e:
                print(e)
            except ProductNotFoundError as e:
                print(e)
            finally:
                continue
        case '7':
            code = input("상품 코드를 입력해주세요(일반G / 신선F 001~004): ")
            try:
                print(remove(data, code))
            except ProductNotFoundError as e:
                print(e)
            finally:
                continue
        case '9':               # 이부분은 제미나이가 알려줌
            list_all(data)
            continue