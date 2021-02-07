# coding=utf-8
#  同步爬取链家网信息，保存至csv文件

import math
import random
import re
import time
import pandas
import csv
import requests
from lxml import etree


city_url = f'https://tj.lianjia.com/zufang/'
down = 1
up = 1000000

#  链家网二手房源信息最多只能显示100页3000条，因此通过二分法切割价格区间
inter_list = [(down, up)]

def write_att(att, file_name):
    file = open(file_name, 'w')
    str1 = str(att)
    file.write(str1)
    file.close()
    print('write file ' + file_name + ' success！')


def binary(inter):
    lower = inter[0]
    upper = inter[1]
    ave = int((upper - lower) / 2)
    inter_list.remove(inter)
    print("已经缩小价格区间：", inter)
    inter_list.append((lower, lower + ave))
    inter_list.append((lower + ave, upper))


pagenum = {}
headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"}


def get_num(inter):
    link = city_url + f'brp{inter[0]}erp{inter[1]}/'
    r = requests.get(link, headers=headers)
    abc = etree.HTML(r.text).xpath("//span[@class='content__title--hl']/text()")
    num = int(abc[0].strip())
    pagenum[(inter[0], inter[1])] = num
    return num


totalnum = get_num(inter_list[0])
print(f"一共有{totalnum}条房源信息")

# judge = True
# while judge:
#     a = [get_num(x) > 3000 for x in inter_list]
#     if True in a:
#         judge = True
#         for i in inter_list:
#             if get_num(i) > 3000:
#                 binary(i)
#     else:
#         judge = False
# print("价格区间缩小完毕！", inter_list)
file = open('url_list.txt', 'r')
url_list = eval(file.read())
file.close()
print('url_list读取完成！')
print(pagenum)

# url_list = []
url_list_failed = []
# url_list_successed = []
url_list_duplicated = []

# for i in inter_list:
#     totalpage = math.ceil(pagenum[i] / 30)
#     for j in range(1, totalpage + 1):
#         url = city_url + f'pg{j}brp{i[0]}erp{i[1]}/'
#         url_list.append(url)
# print("url列表获取完毕")
# write_att(url_list, 'url_list.txt')

info_list = []
scrap_times = 0
start = time.time()
inf_num = 0
csvfile = open("test.csv", "w", newline='')
writer = csv.writer(csvfile)
writer.writerow(['房屋名称', '链接', '小区', '面积', '朝向', '户型', '楼层', '发布时间', '价格（元/月）'])
for url in url_list:
    try:
        r = requests.get(url, headers=headers, timeout=20)
    except Exception as e:
        print(url)
        print(e)
    html = etree.HTML(r.text)
    house_list = html.xpath('//div[@class="content__list"]/div[@class="content__list--item"]')
    info_dict = {}
    index = 1
    print("开始抓取，", url)
    for house in house_list:
        try:
            info_dict['房屋名称'] = house.xpath('.//div[@class="content__list--item--main"]/p/a/text()')[0].strip()
        except:
            info_dict['房屋名称'] = 'None'
        try:
            info_dict['链接'] = 'https://tj.lianjia.com'+house.xpath('.//div[@class="content__list--item--main"]/p/a/@href')[0]
        except:
            info_dict['链接'] = 'None'
        try:
            detail = house.xpath('.//p[@class="content__list--item--des"]')[0].xpath('.//text()')
            info_dict['小区'] = detail[1]+'-'+detail[3]+'-'+detail[5]
        except:
            info_dict['小区'] = 'None'
        try:
            info_dict['面积'] = detail[8].strip()
        except:
            info_dict['面积'] = 'None'
        try:
            info_dict['朝向'] = detail[10].strip()
        except:
            info_dict['朝向'] = 'None'
        try:
            info_dict['户型'] = detail[12].strip()
        except:
            info_dict['户型'] = 'None'
        try:
            info_dict['楼层'] = detail[15].strip().replace(' ','')
        except:
            info_dict['楼层'] = 'None'
        try:
            info_dict['发布时间'] = house.xpath('.//p[@class="content__list--item--time oneline"]/text()')[0].strip()
        except:
            info_dict['发布时间'] = 'None'
        try:
            info_dict['价格（元/月）'] = house.xpath('.//span[@class="content__list--item-price"]/em/text()')[0].strip()+'元/月'
        except:
            info_dict['价格（元/月）'] = 'None'

        if True in [info_dict['链接'] in dic.values() for dic in info_list]:
            url_list_duplicated.append(info_dict)
        else:
            a = list(info_dict.values())
            print(a)
            writer.writerow(a)
            # info_list.append(info_dict)
            # url_list_successed.append(info_dict)
        print(f"第{index}条:    {info_dict['房屋名称']}→房屋信息抓取完毕！")
        index += 1
        inf_num += 1
        info_dict = {}

        scrap_times += 1
        if scrap_times % 100 == 0:
            sleep_time = random.randint(1, 3) + random.random()
            time.sleep(sleep_time)
            print(f"开始休息：{sleep_time}秒")
        elif scrap_times % 300 == 0:
            sleep_time = random.randint(5, 10) + random.random()
            time.sleep(sleep_time)
            print(f"开始休息：{sleep_time}秒")
        elif scrap_times % 900 == 0:
            sleep_time = random.randint(20, 25) + random.random()
            time.sleep(sleep_time)
            print(f"开始休息：{sleep_time}秒")
        else:
            pass

    print(f"进度:{inf_num/totalnum}%")

csvfile.close()
end = time.time()
print(f"实际获得{inf_num}条房源信息。")
# print(f"实际获得{len(info_list)}条房源信息。")
print(f"总共耗时{end - start}秒")

# df = pandas.DataFrame(info_list)
# df.to_csv("lianjia_pandas.csv", mode='a+', encoding='utf-8-sig')