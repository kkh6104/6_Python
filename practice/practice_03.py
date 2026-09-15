"""
    실습용 사이트에서
        종목 메뉴 페이지(SSR)의 섹터를 "IT 서비스"로 검색한 결과 데이터를 추출

    - 요청 주소: ?? --> https://kh-lab.rockua.ai.kr/stocks?sector=S08&market=&q=
    TODO: 오늘(09/15) 18시까지 이메일로 제출
"""

import requests, json, csv, importlib
from bs4 import BeautifulSoup

from config import BASE, TIMEOUT, HEADERS
from parsers import get_text, parse_stocks

resp = requests.get(f"{BASE}/stocks?sector=S08&market=&q=", headers=HEADERS, timeout=TIMEOUT)
resp.raise_for_status()     # 응답 코드가 200이 아니면 예외 발생

html = resp.text
soup = BeautifulSoup(html, 'lxml')
row = soup.select_one("tr.stock-row")
stocks = parse_stocks(html)

print(f"{'코드':<8}{'종목명':<16}{'섹터':<10}{'현재가':>12}{'등락률':>9}")
for s in stocks:
    print(f"{s['code']:<8}{s['name']:<16}{s['sector']:<10}{s['price']:>12}{s['rate']:>9}")


"""
    실습용 사이트에서
        종목 메뉴 페이지(CSR)의 섹터를 "IT 서비스"로 검색한 결과 데이터를 추출
"""

