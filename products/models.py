# Product, FreshProduct 등 도메인 클래스 정의
from datetime import date

"""
각 주제는 상속을 활용하여 공통 속성을 가진 부모 클래스와 타입별 자식 클래스로 분리하여 구현해야 합니다.
각 클래스에 __str__ 메소드를 구현하여, 정보 출력 시 일관된 형식을 제공해야 합니다

- 상품 정보는 `상품 코드`, `품명`, `단가`, `재고수량`을 기본적으로 등록할 수 있어야 합니다.
- 일반 물품의 경우 `위험물 여부` 정보를 추가로 등록할 수 있어야 합니다.
- 신선 식품의 경우 `유통기한(날짜)` 정보를 추가로 등록할 수 있어야 합니다.
    - 유통기한이 오늘로부터 3일 이내인 경우, 단가를 50% 할인한 가격을 반환하는 `get_price()` 메소드를 구현해야 합니다.

- 입고 수량을 증가시키거나 출고 수량을 감소시킬 수 있어야 합니다.
    - 출고 수량이 현재 재고를 초과하는 경우 예외를 발생시켜야 합니다.
- 상품의 단가를 수정할 수 있어야 합니다.
"""

class Product:
    def __init__(self, product_code, product_name, product_price, product_stock):
        self.product_code = product_code
        self.product_name = product_name
        self._product_price = product_price
        self._product_stock = product_stock
    def __str__(self):
        return f"상품 코드: {self.product_code}, 품명: {self.product_name}, 단가: {self._product_price}, 재고수량: {self._product_stock}"
    def get_price(self):
         return self.product_price
    @property
    def product_stock(self):
        return self._product_stock
    @property
    def product_price(self):
        return self._product_price
    @product_price.setter
    def product_price(self, value):
         self._product_price = value
    def add_stock(self, value):
        if value <= 0 :
            raise InputNumberError(value)
        self._product_stock += value
    def sub_stock(self, value):
        if value <= 0 :
            raise InputNumberError(value)
        if value > self._product_stock:
            raise ExceedStockError(self._product_stock, value)
        self._product_stock -= value
    def __repr__(self):
        return self.__str__()    # 이부분은 제미나이가 알려줌
         

class GeneralProduct(Product):
    def __init__(self, product_code, product_name, product_price, product_stock, is_danger):
        super().__init__(product_code, product_name, product_price, product_stock)
        self.is_danger = is_danger
    def __str__(self):
            return f"상품 코드: {self.product_code},\t품명: {self.product_name},\t단가: {self.product_price},\t재고수량: {self.product_stock},\t위험물 여부: {self.is_danger}"

class FreshProduct(Product):
    def __init__(self, product_code, product_name, product_price, product_stock, expiration_date):
        super().__init__(product_code, product_name, product_price, product_stock)
        self.expiration_date = expiration_date
    def get_price(self):
        if 3 >= (self.expiration_date - date.today()).days >= 0:
            return int(round(self.product_price * 0.5))
        return self.product_price
    def __str__(self):
            return f"상품 코드: {self.product_code},\t품명: {self.product_name},\t단가: {self.product_price},\t재고수량: {self.product_stock},\t유통기한(날짜): {self.expiration_date}"

class InputNumberError(Exception):
    """ 입고 숫자 에러 """
    def __init__(self, value):
        self.value = value
        super().__init__(f"입력하신 값 {value} : 입력하실 값은 0이나 음수가 될 수 없습니다.")

class ExceedStockError(Exception):
    """ 출고 수량이 재고를 초과 """
    def __init__(self, stock, value):
        self.value = value
        super().__init__(f"입력하신 값 {value} : 출고 수량이 현재 재고({stock})보다 더 많습니다.")

class ProductNotFoundError(Exception):
    """ 입력한 코드에 해당하는 품목이 없음 """
    def __init__(self, code):
        self.code = code
        super().__init__(f"입력하신 코드({code})에 해당하는 상품이 없습니다.")