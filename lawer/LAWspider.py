#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File: LAWspider.py
# @Author: MK<zzx65706780@gmail.com>
# @Device: MK
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
import hashlib


SLEEP_TIME_1 = 0.1  # 获取ID请求CD

SLEEP_TIME_2 = 600  # 发生错误等待时间

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
	"User-Agent" : random.choice(agent_list),
	# "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
	"Host": "www.12348.gov.cn",
	"Connection": "keep-alive",
	"Content-Length": "173",
	"Accept": "application/json, text/plain, */*",
	"Content-Type": "application/json;charset=UTF-8",
	# "Origin": "http://www.12348.gov.cn",
	"Referer": "http://www.12348.gov.cn/",
	"Accept-Encoding": "gzip, deflate",
	"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,zh-TW;q=0.6,ja;q=0.5",
	"Cookie": "__jsluid_h=60b8c92bb4e5cf024fab9dee6a7dc553; Hm_lvt_3638a62525c09282e5cd18863d8f4456=1608866347,1609582031,1610022809,1610107189; JSESSIONID=5E4800EF3EF21DEFEE08A418F89F7FBA; Hm_lpvt_3638a62525c09282e5cd18863d8f4456=1610110885",
	# "Referer":"http://kd.nsfc.gov.cn/baseQuery/conclusionQuery"
}

url_supportQuery = 'http://kd.nsfc.gov.cn/baseQuery/data/supportQueryResultsDataForNew'
url_conclusionQuery = 'http://kd.nsfc.gov.cn/baseQuery/data/supportQueryResultsData'
lawer_dept_url = 'http://www.12348.gov.cn/lawerdeptlist/getlawerdeptlist'

law_dept_info_url = 'http://www.12348.gov.cn/lawdeptinfo/getlawdeptinfo'
lawer_list_url = 'http://www.12348.gov.cn/lawdeptinfo/getlawerlist'

def uuid():
	hexDigits = "0123456789abcdef"
	s = []
	for i in range(36):
		a = random.choice(hexDigits)
		s.append(a)
	s[14] = '4'
	s[19] = hexDigits[(1 & 0x3) | 0x8]
	s[8] = s[13] = s[18] = s[23] = "-"
	uuid = ''.join(s)
	print(uuid)
	return uuid


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


def get_project_list():

	req_data = {
		"pageSize":12,
		"pageNum":1,
		"xzqh":"",
		"yw":"",
		"pzslsj":0,
		"nums":0,
		"v_key":"71ca2828-cc34-4593-9629-52d22c9cb813",
		"guid":"d429d3f9-5917-47de-a24b-c74a8e56287a",
		"number":206
	}
	req_data["v_key"] = uuid()

	total_page = 32139//12+1
	# print(urllib.parse.quote(lawer_dept_url))

	law_dept_list = []
	for i in range(1, total_page+1):
		req_data["guid"] = uuid()
		print(req_data["guid"])
		req_data["pageNum"] = i
		encode_str = urllib.parse.quote(
			req_data['v_key'] + req_data['guid'] + str(req_data["pageNum"]) + '.' + str(req_data["pageSize"])).encode(
			'utf-8')
		md5str = hashlib.md5(encode_str).hexdigest()
		num = ord(md5str[2]) + ord(md5str[5]) + ord(md5str[8])
		print(num)
		req_data["number"] = num
		headers["Content-Length"] = str(len(req_data))
		res = requests.post(lawer_dept_url, data=json.dumps(req_data), headers=headers)
		res_json = res.json()
		print(res_json)
		law_dept_list += res_json['list']
		time.sleep(SLEEP_TIME_1)

	return law_dept_list

def get_law_dept_info_and_lawer_list(dept_list):
	dept_info_list = []
	lawer_list = []
	num = 1
	for dept in dept_list:
		print('第' + str(num) + '家律师事务所！')
		lsswsbs = dept['lsswsbs']
		req_data = {
			'lsswsbs' : lsswsbs
		}
		headers["Content-Length"] = str(len(req_data))
		res = requests.post(law_dept_info_url, data=json.dumps(req_data), headers=headers)
		with open('dept_info_list_tmp.txt', 'a', encoding='utf-8') as f:
			f.write(res.text)
			f.write(',')
			f.write('\n')
		try:
			res_json = res.json()
			print(res_json['lsswsmc'])
			dept_info_list.append(res_json)
		except:
			print('ERR---------')
			print(res.text)



		lsswsbs = dept['lsswsbs']
		req_data = {
			'pageNum': 1,
			'pageSize': 8,
			'pkid': lsswsbs
		}
		headers["Content-Length"] = str(len(req_data))
		res = requests.post(lawer_list_url, data=json.dumps(req_data), headers=headers)
		with open('lawer_list_tmp.txt', 'a', encoding='utf-8') as f:
			f.write(res.text)
			f.write(',')
			f.write('\n')
		res_json = res.json()
		lawer_list += res_json['list']
		total = res_json['total']
		print(total)
		print(1)

		total_pages = 0
		if total > 8:
			total_pages = total//8+1
			for i in range(2, total_pages):
				print(i)
				req_data["pageNum"] = i
				res = requests.post(lawer_list_url, data=json.dumps(req_data), headers=headers)
				with open('lawer_list_tmp.txt', 'a', encoding='utf-8') as f:
					f.write(res.text)
					f.write(',')
					f.write('\n')
				res_json = res.json()
				# print(res_json)
				lawer_list += res_json['list']
		else:
			continue

		num += 1


	return dept_info_list, lawer_list










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
	# law_dept_list = get_project_list()
	# with open('law_dept_list.txt', 'w', encoding = 'utf-8') as f:
	# 	f.write(str(law_dept_list))

	# with open('law_dept_list.txt', 'r', encoding='utf-8') as f:
	# 	a = eval(f.read())
	#
	# dept_info_list, lawer_list = get_law_dept_info_and_lawer_list(a)
	#
	# with open('dept_info_list.txt', 'w', encoding = 'utf-8') as f:
	# 	f.write(str(dept_info_list))
	#
	# with open('lawer_list.txt', 'w', encoding = 'utf-8') as f:
	# 	f.write(str(lawer_list))

	with open('lawer_list.txt', 'r', encoding='utf-8') as f:
		a = eval(f.read())
	print(a[0])
	print(len(a))

	# print("爬取完成！")
