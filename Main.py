import re
import requests
import json

def getCookie():
    cookie = "123"
    with open("cookie.txt", "r") as f:
        cookie = f.read();
    return cookie

def getData(cookie):
    pattern = r'([^=;\s]+)=([^;]*)'
    matches = re.findall(pattern, cookie)
    cookies = {}
    for key, value in matches:
        cookies[key.strip()] = value.strip()
    return cookies

def getMid(datas):
    url = 'https://api.bilibili.com/x/web-interface/nav'
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
        'Cookie': 'SESSDATA=' + datas['SESSDATA'] + ';'
    }
    result = requests.get(url = url, headers = headers)
    result = json.loads(result.text)
    return result['data']['mid'];


def main():
    cookie = getCookie()
    datas = getData(cookie)
    mid = getMid(datas)
    print(mid)


if __name__ == "__main__":
    main()



