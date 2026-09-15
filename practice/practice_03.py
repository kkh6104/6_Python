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

print("=" * 60)

"""
    실습용 사이트에서
        종목 메뉴 페이지(CSR)의 섹터를 "IT 서비스"로 검색한 결과 데이터를 추출
"""

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