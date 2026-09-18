"""
    실습용 사이트에서
        종목 메뉴 페이지(SSR)의 섹터를 "IT 서비스"로 검색한 결과 데이터를 추출

    - 요청 주소: ?? --> https://kh-lab.rockua.ai.kr/stocks?sector=S08&market=&q=
    TODO: 오늘(09/15) 18시까지 이메일로 제출
"""

print("=" * 60)
print("정적 페이지 스크래핑")

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

print("=" * 60)
print("동적 페이지 스크래핑")


# Playwright 동기 방식 API
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # browser : 크롬을 실행
    browser = p.chromium.launch(headless=True) # headless = True => 창이 보이지 않음.

    # context : 시크릿 창 하나. 쿠키, 캐시가 독립적으로 보관.
    context = browser.new_context(locale="ko-KR",
                                   viewport={'width': 1280, 'height': 720})

    # page : 실제로 조작하기 위한 탭 하나.
    page = context.new_page()

    # page.route(패턴, 처리함수) : 특정 패턴의 요청을 가로채서 직접 처리하는 함수
    # route.abort()             : 요청을 취소
    # route.continue_()         : 요청을 그대로 진행
    page.route(
        "**/*",
        lambda route: route.abort() if route.request.resource_type in {"image", "font", "media"}
                                    else route.continue_()
    )

    page.goto(f"{BASE}/csr/stocks", wait_until='domcontentloaded')
    # wait_until
    #   - domcontentloaded : HTML을 다 읽고 DOM트리가 만들어진 시점 (JS 실행 전)
    #   - load : 이미지를 포함한 모든 리소스가 로드된 시점 (기본값). 느림..

    page.wait_for_selector("tr.stock-row")

    # 섹터 선택 드롭다운에서 IT 서비스 선택
    page.select_option("div.filter-form.mb-4 select", "S08")
    
    page.wait_for_selector("tr.stock-row")
    # 해당 선택자가 DOM에 그려질 때까지 대기(기다림)

    # content() : DOM을 문자열로 반환
    html = page.content()

    items = parse_stocks(html)

    browser.close()

for s in items:
    print(f"{s['code']:<8}{s['name']:<16}{s['sector']:<10}{s['price']:>12}{s['rate']:>9}")

"""
무한 스크롤 연습
페이지를 내리면 https://kh-lab.rockua.ai.kr/api/v1/companies?page=2&limit=15 같은 곳으로 요청을 보냄
"""

print("=" * 60)
print("무한 스크롤 스크래핑")

import requests

from config import BASE, TIMEOUT, HEADERS
from parsers import get_text, get_number, parse_stocks


# 그냥 10번만 반복하게 해서 뽑는 방법
result = []
for i in range(1, 11):
    resp = requests.get(f"{BASE}/api/v1/companies?page={i}&limit=15", headers=HEADERS, timeout=TIMEOUT)
    resp.raise_for_status()
    result.extend(resp.json().get("items"))

# 데이터가 안들어오거나 앞의 데이터와 같으면 중단
i = 1
result = []
last_item = []
while True:
    resp = requests.get(f"{BASE}/api/v1/companies?page={i}&limit=15", headers=HEADERS, timeout=TIMEOUT)
    resp.raise_for_status()
    item = resp.json().get("items")
    if item is None:
        break
    if item == last_item:
        break
    last_item = item
    i += 1
    result.extend(item)


print(f"{'코드':<8}{'종목명':<16}{'섹터':<10}{'현재가':>12}{'등락률':>9}")
for s in result:
    print(f"{s['code']:<8}{s['name']:<16}{s['sectorName']:<10}{s['price']:>12}{s['changeRate']:>9}")



"""
더보기 목록 연습
더보기 버튼을 누르면 https://kh-lab.rockua.ai.kr/api/v1/companies?page=2&limit=15 같은 곳으로 요청을 보냄
=> 무한 스크롤과 같음
"""

"""
종목 검색
검색입력 조건은 엔터나 입력을 멈춘 후 0.3초이나 결국
page=1&limit=20&sector=all&sortBy=code_asc&keyword=%EA%B0%80%EC%98%A8 로 요청을 보내는건 같음
키워드는 내가 입력한 '가온'이라 추정됨.
키워드 입력 없을 시 page=1&limit=20&sector=all&sortBy=code_asc&keyword= 로 요청
"""

print("=" * 60)
print("종목 검색")

import requests

from config import BASE, TIMEOUT, HEADERS
from parsers import get_text, get_number, parse_stocks

i = 1
result = []
last_item = []
while True:
    resp = requests.get(f"{BASE}/api/v1/companies?page={i}&limit=20&sector=all&sortBy=code_asc&keyword=", headers=HEADERS, timeout=TIMEOUT)
    resp.raise_for_status()
    item = resp.json().get("items")
    if item is None:
        print("새 정보 없음")
        break
    if item == last_item:
        print("같은 정보")
        break
    last_item = item
    i += 1
    result.extend(item)

print(f"{'코드':<8}{'종목명':<16}{'섹터':<10}{'현재가':>12}{'등락률':>9}")
for s in result:
    print(f"{s['code']:<8}{s['name']:<16}{s['sectorName']:<10}{s['price']:>12}{s['changeRate']:>9}")

# 웹상에선 20개 출력 제한인거 같은데 이런식으로하면 120개 다 받을 수 있음(....)


"""
    캔버스 차트
    
    https://kh-lab.rockua.ai.kr/api/v1/prices?code=G0002&limit=100 <- 로 요청이 들어감

"""
import requests

from config import BASE, TIMEOUT, HEADERS
from parsers import get_text, get_number, parse_stocks

i = input("원하는 코드번호의 4자리의 숫자만 입력하세요 G0001~G0120? : ")
result = []
last_item = []

resp = requests.get(f"{BASE}/api/v1/prices?code=G{i}&limit=100", headers=HEADERS, timeout=TIMEOUT)
resp.raise_for_status()
item = resp.json()
result.extend(item)

print(f"{'코드':<8}{'날짜':<8}{'시가':<8}{'고가':<8}{'저가':<8}{'종가':<8}{'거래량':<8}{'등락폭':<8}{'등락률':<8}")
for s in result:
    print(f"{s['code']:<8}{s['date']:<8}{s['open']:<8}{s['high']:<8}{s['low']:<8}{s['close']:<8}{s['volume']:<8}{s['change']:<8}{s['changeRate']:<8}")