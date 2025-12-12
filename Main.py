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
    if result["code"] == 0:
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
    return result


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

def favVideo2Folder(aid, mid, cookie):
    url = 'https://api.bilibili.com/x/v3/fav/resource/deal'
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
        'Cookie': f'SESSDATA={cookie["SESSDATA"]};'
    }
    params = {
        'rid': aid,
        'type': 2,
        'add_media_ids': mid,
        'csrf': cookie['bili_jct']
    }
    result = requests.post(url = url, data = params, headers = headers).text
    result = json.loads(result)
    return result

def main():
    searchInfo = getSongByFile()
    cookie = getCookieByFile()
    datas = getData(cookie)
    mid = getMid(datas)
    time.sleep(random.randint(2,6))
    folders = getFavFolder(mid, datas)    
    print("输入目标文件夹序号进行选择")
    for i in range(0, len(folders)):
        title = folders[i]["title"]
        print(f'{i}. {title}')
    target = int(input())

    folder = folders[target]["id"]
    success = 0
    for target in searchInfo:
        time.sleep(random.randint(20,60))
        data = doSearch(target, cookie)
        if(data['code'] == 0):
            data = ["data"]['list']
            print(f"找到结果:{removeHtmlTags(data['title'])}")
        else:
            code = data["code"]
            msg = data["message"]
            print(f'搜索失败, target: {target}, code: {code}, msg: {msg}')
            with open('log.txt', 'a', encoding='utf-8') as f:
                code = res['code']
                msg = res['message']
                f.write(f'keyword: {target} code: {code}, msg: {msg}')
            continue;

        time.sleep(random.randint(20,60))
        res =  favVideo2Folder(data['aid'], folder, datas)
        if res["code"] == 0:
            success += 1
            print(f'收藏成功, 当前已经成功{success} / {len(searchInfo)}')
        else:
            print('失败,具体请见日志')
            with open('log.txt', 'a', encoding='utf-8') as f:
                code = res['code']
                msg = res['message']
                f.write(f'keyword: {target} code: {code}, msg: {msg}')

    print(f'收藏结束,成功 {success} / {len(searchInfo)}')


if __name__ == "__main__":
    main()