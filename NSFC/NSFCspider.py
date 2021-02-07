#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File: NSFCspider.py
# @Author: MK<zzx65706780@gmail.com>
# @Device: MK_lab 
# @Date: 2020/12/8

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

res_data = {
    "ratifyNo": "",
    "projectName": "",
    "personInCharge": "",
    "dependUnit": "",
    "code": "",
    "projectType": "",
    "subPType": "",
    "psPType": "",
    "keywords": "",
    "ratifyYear": "",
    "conclusionYear": "",
    "beginYear": "",
    "endYear": "",
    "checkDep": "",
    "checkType": "",
    "quickQueryInput": "",
    "adminID": "",
    "complete": "false"
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

url_supportQuery = 'http://kd.nsfc.gov.cn/baseQuery/data/supportQueryResultsDataForNew'
url_conclusionQuery = 'http://kd.nsfc.gov.cn/baseQuery/data/supportQueryResultsData'
author_url = 'http://kd.nsfc.gov.cn/advancedQuery/personInfo/100134042'

need_field = ['218', '220', '630', '631']
years = [str(a) for a in range(2000, 2021)]


def field_init():
    if not os.path.exists('NSFC_record.txt'):
        with open('NSFC_supportType.txt', 'r', encoding='utf-8') as f:
            types = eval(f.read())
        all_type = {a['value']: {'name': a['name']} for a in types}
        # with open('NSFC_field.txt', 'r', encoding='utf-8') as f:
        with open('NSFC_field1.txt', 'r', encoding='utf-8') as f:
            a = f.read()
            NSFC_class = eval(a)
        NSFC_class_dict = {}
        for a in NSFC_class:
            if len(a["code"]) > 3:
                NSFC_class_dict[a["code"]] = {'year': '2000', 'count': 0}
        for a in all_type:
            if a in need_field:
                all_type[a]['field'] = NSFC_class_dict
            all_type[a]['count'] = 0
            all_type[a]['current'] = {'year': '2000', 'count': 0}

        with open("NSFC_record.txt", 'w', encoding='utf-8') as f:
            f.write(str(all_type))
        return all_type
    else:
        with open('NSFC_record.txt', 'r', encoding='utf-8') as f:
            all_type = eval(f.read())
        return all_type


def update_NSFC_record(NSFC_record):
    with open("NSFC_record.txt", 'w', encoding='utf-8') as f:
        f.write(str(NSFC_record))


def get_more_info(code):
    # url = 'http://kd.nsfc.gov.cn/baseQuery/data/conclusionProjectInfo/' + info[0][2]
    url = 'http://kd.nsfc.gov.cn/baseQuery/data/conclusionProjectInfo/' + code
    res = requests.get(url, headers=headers)
    if res.status_code == 500:
        print('Not find project!')
        return {}
    else:
        res_json = res.json()
        return res_json


def get_project_list(projectType, conclusionYear, field_code='', complete='true'):
    req_data = {
        "ratifyNo": "",
        "projectName": "",
        "personInCharge": "",
        "dependUnit": "",
        "code": field_code,
        "projectType": projectType,
        "subPType": "",
        "psPType": "",
        "keywords": "",
        "ratifyYear": "",
        "conclusionYear": conclusionYear,
        "beginYear": "",
        "endYear": "",
        "checkDep": "",
        "checkType": "",
        "quickQueryInput": "",
        "adminID": "",
        "complete": complete,
        "pageNum": 0,
        "pageSize": 10,
        "queryType": "input"
    }

    res = requests.post(url_conclusionQuery, data=json.dumps(req_data), headers=headers)
    if res.status_code != 200:
        print('Get_project_list request error!')
        print('Error Code:' + str(res.status_code))
        return [], 0
    res_json = res.json()
    res_code = res_json['code']
    if res_code != 200:
        print('Get_project_list request error!')
        print('Error Code:' + str(res_code))
        return [], 0

    info = res_json['data']['resultsData']
    num = res_json['data']['iTotalRecords']
    page_nums = num // 10 + 1
    print(page_nums)
    print("Get page 0")
    for i in range(1, page_nums):
        # time.sleep(SLEEP_TIME_1)
        req_data['pageNum'] = i
        res = requests.post(url_conclusionQuery, data=json.dumps(req_data), headers=headers)
        res_json = res.json()
        info = info + res_json['data']['resultsData']
        print(len(info))
        print("Get page " + str(i))
    print(len(info))
    return info, num


def save_data(name, projects):
    if not os.path.exists("result/" + name + ".csv"):
        with open("result/" + name + ".csv", "w", encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(projects)
    else:
        with open("result/" + name + ".csv", "a", encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(projects)


if __name__ == '__main__':

    NSFC_record = field_init()
    print(NSFC_record)
    input()
    for NSFC_type in NSFC_record:
        print("Start get" + NSFC_record[NSFC_type]['name'])
        total_count = 0
        if NSFC_type in need_field:
            for field in NSFC_record[NSFC_type]['field']:
                print("Field code:" + field)
                field_count = 0
                for year in years:
                    if year < NSFC_record[NSFC_type]['field'][field]['year']:
                        continue
                    print("Year:" + year)
                    try:
                        project_list, year_count = get_project_list(NSFC_type, year, field)
                    except:
                        project_list = []
                        year_count = 0
                    # csvfile.close()
                    print("Get project num:" + str(year_count))
                    if project_list and year_count != 0:
                        save_data(NSFC_record[NSFC_type]['name'], project_list)
                        field_count = field_count + year_count
                        NSFC_record[NSFC_type]['field'][field]['year'] = year
                        NSFC_record[NSFC_type]['field'][field]['count'] = field_count
                    else:
                        if NSFC_record[NSFC_type]['field'][field].__contains__('error_year'):
                            NSFC_record[NSFC_type]['field'][field]['error_year'].append(year)
                        else:
                            NSFC_record[NSFC_type]['field'][field]['error_year'] = [year]
                    update_NSFC_record(NSFC_record)
                total_count = total_count + field_count
                NSFC_record[NSFC_type]['count'] = total_count
        else:
            for year in years:
                if year < NSFC_record[NSFC_type]['current']['year']:
                    continue
                print("Year:" + year)
                project_list, year_count = get_project_list(NSFC_type, year)
                print("Get project num:" + str(year_count))
                if project_list and year_count != 0:
                    save_data(NSFC_record[NSFC_type]['name'], project_list)
                    total_count = total_count + year_count
                    NSFC_record[NSFC_type]['current']['year'] = year
                    NSFC_record[NSFC_type]['current']['count'] = total_count
                else:
                    if NSFC_record[NSFC_type]['current'].__contains__('error_year'):
                        NSFC_record[NSFC_type]['current']['error_year'].append(year)
                    else:
                        NSFC_record[NSFC_type]['current']['error_year'] = [year]
                update_NSFC_record(NSFC_record)
            NSFC_record[NSFC_type]['count'] = total_count

    print("爬取完成！")
