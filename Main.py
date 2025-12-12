import re
import requests
import json
import time
import random

def removeHtmlTags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def getCookieByFile():
    cookie = "123"
    with open("cookie.txt", "r") as f:
        cookie = f.read();
    return cookie

def getSongByFile():
    with open(r"searchinfo.txt", 'r') as f:
        lines = f.readlines()
    print(f"共读取 {len(lines)} 首歌曲,预计{len(lines) * 12 / 60 }min 完成")
    return lines

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

def getFavFolder(mid, datas):
    url = 'https://api.bilibili.com/x/v3/fav/folder/created/list-all'
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
        'Cookie': 'SESSDATA=' + datas['SESSDATA'] + ';'
    }
    params = {
        'up_mid': mid
    }

    result = requests.get(url = url, params= params, headers = headers)
    result = json.loads(result.text)
    return result["data"]['list']


def doSearch(target, cookie):
    url = 'https://api.bilibili.com/x/web-interface/wbi/search/all/v2'
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
        'Cookie': cookie
    }
    params = {
        'keyword': target
    }
    result = requests.get(url = url, params = params, headers = headers)
    result = json.loads(result.text)
    return result["data"]["result"][11]['data'][0]

def main():
    searchInfo = getSongByFile()
    cookie = getCookieByFile()
    datas = getData(cookie)
    mid = getMid(datas)

    time.sleep(random.randint(2,6))
    
    folders = getFavFolder(mid, datas)
    print("输入目标文件夹序号进行选择")
    for i in range(0, len(folders)):
        print(f'{i}. {folders[i]["title"]}')
    target = int(input())
    folder = folders[target]["id"]
    success = 0
    for target in searchInfo:
        time.sleep(random.randint(2,6))
        data = doSearch(target, cookie)
        success += 1
        print(f"找到结果:{removeHtmlTags(data['title'])}, 当前已经完成{success} / {len(searchInfo)}")
        time.sleep(random.randint(2,6))



if __name__ == "__main__":
    main()



