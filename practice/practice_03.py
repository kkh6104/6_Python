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
try:
    row.select_one("td.test").text       # 해당하는 클래스가 없을 때
except Exception as e:
    print(f"오류:: {e}")

print(f"td.test -> {get_text(row, 'td.test')}")
print("=" * 80)

stocks = parse_stocks(html)

print(f"{'코드':<8}{'종목명':<16}{'섹터':<10}{'현재가':>12}{'등락률':>9}")

for s in stocks:
    print(f"{s['code']:<8}{s['name']:<16}{s['sector']:<10}{s['price']:>12}{s['rate']:>9}")