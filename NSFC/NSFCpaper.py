#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File: NSFCpaper.py
# @Author: MK<zzx65706780@gmail.com>
# @Device: MK
# @Date: 2021/2/4

import time
import csv
import os
import re
import json
import random
from bs4 import BeautifulSoup
import requests
from requests import RequestException
import urllib.parse

SLEEP_TIME_1 = 1  # 获取ID请求CD

SLEEP_TIME_2 = 600  # 发生错误等待时间

req_data = {
    "authorID": "",
    "fieldCode": "",
    "journalName": "",
    "orderBy": "rel",
    "orderType": "desc",
    "organizationID": "",
    "pageNum": 0,
    "pageSize": 10,
    "projectName": "",
    "query": "",
    "supportType": "",
    "title": "",
    "year": "",
}

agent_list = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50"
]

headers = {
    "User-Agent": random.choice(agent_list),
    # "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Cookie": "JSESSIONID=247E777B1F6EE8025BCB4EF3DB98CAA9",
    "Accept": "*/*",
    "Content-Type": "application/json",
    # "Referer":"http://kd.nsfc.gov.cn/baseQuery/conclusionQuery"
}

url_paperQuery = 'http://ir.nsfc.gov.cn/baseQuery/data/paperQueryForOr'


def save_data(papers):
    if not os.path.exists("result.json"):
        with open("result.json", "w", encoding='utf-8', newline='') as f:
            f.write(json.dumps(papers, ensure_ascii=False))
    else:
        with open("result.json", "w", encoding='utf-8', newline='') as f:
            f.write(json.dumps(papers, ensure_ascii=False))


if __name__ == '__main__':

    result = []
    for i in range(76290):
        print("Start save page:", i)
        req_data["pageNum"] = i
        res = requests.post(url_paperQuery, data=json.dumps(req_data), headers=headers)
        if res.status_code != 200:
            print('Get request error!')
            print('Error Code:' + str(res.status_code))
            continue
        res_json = res.json()
        res_code = res_json['code']
        print(res_code)
        data = res_json['data']
        result += data
        save_data(result)
        print("Success save page:", i, "\n")
