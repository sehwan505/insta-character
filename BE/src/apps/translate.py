import requests
from utils.util import config

def translate_en2ko(text):
    url = "https://openapi.naver.com/v1/papago/n2mt"
    headers = {
        "X-Naver-Client-Id": config["naver_client_id"],
        "X-Naver-Client-Secret": config["naver_client_secret"],
    }
    data = {"source": "en", "target": "ko", "text": text}
    response = requests.post(url, headers=headers, data=data)
    rescode = response.status_code
    if rescode == 200:
        return response.json()["message"]["result"]["translatedText"]
    else:
        return "Error Code:" + rescode