# 재고 관리 클래스 (등록·조회·수정·삭제)

from models import InputNumberError, ProductNotFoundError

"""
- 전체 재고를 확인할 수 있어야 합니다.
- 긴급 발주 목록을 확인할 수 있어야 합니다. (재고 수량이 10개 미만인 품목)
- 전체 재고의 총 금액을 확인할 수 있어야 합니다.
- 입고 수량을 증가시키거나 출고 수량을 감소시킬 수 있어야 합니다.
    - 출고 수량이 현재 재고를 초과하는 경우 예외를 발생시켜야 합니다.
- 상품의 단가를 수정할 수 있어야 합니다.
- 단종된 품목은 상품 코드를 통해 제거할 수 있어야 합니다.
- 예외 클래스를 최소 2개 정의하여 활용해야 합니다.
    - 예: `OutOfStockError` (출고량이 재고 초과 시), `ProductNotFoundError` (존재하지 않는 상품 코드 조회 시)
"""

def check_inventory(data):
    result = []
    for product in data:
        result.append([product.product_code, product.product_name, product.product_price, product.product_stock])
    return result

def check_urgent(data):
    result = []
    for product in data:
        if product.product_stock < 10:
            result.append([product.product_code, product.product_name, product.product_price, product.product_stock])
    return result

def total_price(data):
    return sum((x.product_stock * x.get_price()) for x in data)

def inbound(data, product_code, value):
    for product in data:
        if product.product_code == product_code:
            product.add_stock(value)
            return f"{product_code} 코드 상품 {value}개 입고 완료!"
    else:
        raise ProductNotFoundError(product_code)

def outbound(data, product_code, value):
    for product in data:
        if product.product_code == product_code:
            product.sub_stock(value)
            return f"{product_code} 코드 상품 {value}개 출고 완료!"
    else:
        raise ProductNotFoundError(product_code)

def adjust(data, product_code, value):
    if value <= 0:
        raise InputNumberError(value)
    for product in data:
        if product.product_code == product_code:
           product.product_price = value
           return f"{product_code} 코드 상품 {value}원으로 단가 변경 완료!"
    else:
        raise ProductNotFoundError(product_code)

def remove(data, product_code):
    for product in data:
        if product.product_code == product_code:
            data.remove(product)
            return f"{product_code} 코드 상품이 단종으로 인해 삭제되었습니다."
    else:
        raise ProductNotFoundError(product_code)

def list_all(data):
    for product in data:
        print(product)