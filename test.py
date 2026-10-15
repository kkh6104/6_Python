
import requests

url = "http://apis.data.go.kr/B553077/api/open/sdsc2/storeZoneInAdmi"

params = {
    "serviceKey": "e747f03128ae91b1965af9c3d9ca0b192bc68aba7528dbcd3dafe8d6b8913d2b",  # 공공데이터포털에서 발급받은 인증키 입력
    "divId": "ctprvnCd",  # 시도는 ctprvnCd, 시군구는 signguCd, 행정동은 adongCd 사용
    "key": "11",  # 시도코드값, 시군구코드값, 행정동코드값 사용
    "type": "json",  # 데이터 유형 (xml 또는 json)
}

response = requests.get(url, params=params)

if response.status_code == 200:
    # 요청 성공 시 데이터 출력 (JSON 형태)
    print(response.json())
else:
    print(f"에러 발생: {response.status_code}")