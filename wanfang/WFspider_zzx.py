import time
import csv
import os
import re
import json
from bs4 import BeautifulSoup
import requests
from requests import RequestException
import urllib.parse

from params_operator import *

SLEEP_TIME_1 = 1  # 获取ID请求CD
SLEEP_TIME_2 = 0.1  # 获取论文请求CD

SLEEP_TIME_3 = 600  # 发生错误等待时间

def get_info(thesis_id, headers):
    payload = {'Id': thesis_id}
    url = 'http://d.wanfangdata.com.cn/Detail/Thesis/'
    thesis_url = 'http://d.wanfangdata.com.cn/thesis/' + thesis_id

    try:
        res = requests.post(url, data=json.dumps(payload), headers=headers)
        info = res.json()['detail'][0]['thesis']

    except RequestException as e:
        print(e)
        time.sleep(SLEEP_TIME_3)
        return []

    try:
        paper_info = []
        paper_info.append(info['Title'][0])
        paper_info.append(info['Creator'][0])
        paper_info.append(info['OrganizationNorm'][0])
        paper_info.append(info['Degree'])
        paper_info.append(info['Major'])
        paper_info.append(info['Tutor'][0])
        paper_info.append(info['PublishDate'][0:4])
        if info['Language'] == 'chi':
            paper_info.append('中文')
        else:
            paper_info.append(info['Language'])
        paper_info.append(thesis_url)

        # print(paper_info)
        return paper_info

    except:
        print('Format Error!')
        return []

def get_url(html):
    id_list = []
    soup = BeautifulSoup(html.text, 'html.parser')
    list = soup.find_all('div', class_ = 'ResultList')
    for div in list:
        title = div.find('div', class_ = 'title').find('input', class_ = 'chapters')['value']
        res = re.search(r'(.*):(.*)', title)
        id_list.append(res.group(2))

    # print(list)

    return id_list

def get_years(school_name):

    url = 'http://www.wanfangdata.com.cn/search/navigation.do'
    data = {
        'searchType': 'degree',
        'navSearchType': 'degree',
        'limit': 100,
        'startYear':'',
        'endYear':'',
        'facetField': '$common_year',
        'searchWord': urllib.parse.quote('(学位授予单位：'+ school_name +')'),
        'alreadyBuyResource': 'false',
        'single': 'true',
        'bindFieldLimit': '{}'
    }

    try:
        res = requests.post(url, data, headers = headers)
        res = res.json()
        years = []
        for a in res['facetTree']:
            if a['value'] != '年份':
                years.append(a['value'])

        return years
    except:
        print('Get years ERROR!!!!')
        time.sleep(SLEEP_TIME_3)
        get_years(school_name)

def get_school_ids(school_name):

        school_id_list = []
        years = get_years(school_name)
        print(years)

        base_url = 'http://www.wanfangdata.com.cn/search/searchList.do?beetlansyId=aysnsearch&searchType=degree&pageSize=50&page={}&searchWord=学位授予单位%3A{}&facetField=%24common_year%3A{}&showType=detail&order=pro_pub_date&isHit=&isHitUnit=&firstAuthor=false&navSearchType=degree&rangeParame='
        # years = ['2019', '2018']
        for year in years:
            # 总页数最大值
            MAX_PAGE = 1
            last_url = base_url.format(MAX_PAGE, school_name, year)
            thesis_list_page = requests.get(last_url, headers=headers)
            thesis_list_page.encoding='utf-8'
            print(thesis_list_page.text)
            print(last_url)

            soup = BeautifulSoup(thesis_list_page.text, 'html.parser')
            MAX_PAGE = int(soup.find('input', id='pageTotal')["value"])     #万方更新后找不到最大页？

            print('当前年份：' + str(year))
            print('本年页数：' + str(MAX_PAGE))

            if MAX_PAGE > 120:
                MAX_PAGE = 120

            for page in range(1, MAX_PAGE+1):
                new_url = base_url.format(page, school_name, year)
                print("第"+str(page)+"页:"+new_url)

                try:
                    # 爬取当前页面 发送请求、获取响应
                    html = requests.get(new_url)
                    # 解析响应 提取当前页面所有论文的url
                    id_list = get_url(html)

        #             print(html)
                    for id in id_list:
                        if id in school_id_list:
                            print(id)
                            print('重复了！！！！！！！！')
                        else:
                            school_id_list.append(id)
                    time.sleep(SLEEP_TIME_1)
                except:
                    print("请求第"+str(page)+"页错误!!!!!")
                    time.sleep(SLEEP_TIME_3)

        return school_id_list

if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
        'cookie': 'zh_choose=n; firstvisit_backurl=http%3A//www.wanfangdata.com.cn; hasNewToken=1; Hm_lvt_838fbc4154ad87515435bf1e10023fab=1605005722,1605005780,1605006891,1605061103; SEARCHHISTORY_0=UEsDBBQACAgIAFJSa1EAAAAAAAAAAAAAAAABAAAAMO2Z%2FU%2FbRhjH%2F5UqklGrIfCdfb47JDQ5b8Cg%0AEN4a2LQf3MRJPJw4sx0CTJWYRAGhURVNXaUNbdPUlW1qu0mTprZatz9mSUj%2Fiz0OKREvDtkKCVCk%0AyHnu7rmz%2Ff08Pj93%2FuizgKvdNvVRLasH%2BnIF0%2BwOGMlAXyCTUqKpUTaGGQl0BwqObg8l3zg4umYn%0AMlOLeeiCoNE2vQ6um%2B%2Fr7S0Wiz1FLZfScumk5mo9CSvbk8j17nWp%2F40YjtuTtN5vjNOf1NO2rnc5%0AGatYK3fltbQ%2BaSyBtecVt%2BxkvxAhghoWVEWIyEIwLLCwEFEEFhEYq9WoNYN49Zw0fCS1VhkSOK27%0AqaHaULKg0v0xuwxnyjbSad2e0tL9cNP6Qt7WHcewcnB75aePS682K%2FfWSy%2FXy5sPwO4rf%2FGw9PJJ%0A%2BdEOtIG7W9Oj7gjlXCEbtQo5UI1InErdgYSta64%2BZXhKI0UkoqhQzEHgO91%2BFEajau5mOIsUpLSD%0AQl63DasBIam7mmE2UGDxIAwmMCqoIC4VGMiqeDVq1FPTM6BVrKsMreDDRYGdoHJ17ZfdlT%2Bqvz6t%0A%2FrRcfrSye3%2B1IWxl%2B7vy%2BsYBYamo8ON0JRRjBVF%2FXYPGrbnp4eQkxnInovuwsKcU44oQBNFJvRW6%0AvH2MV57fLW%2FeayHGJcw4OY6FzBEDmf1Z4KGYXVz8IIMQawcLzTRbj%2FCaujxUC3WxIe1pC196tV1d%0AvttU8r3o%2F2f58z3twSj9%2BXX12TPPeP5lef1nMHZ3tioby5WNH8tbG43i%2Bv3Kt9tQrHy%2FVl5b9Yzf%0AH1R3Vryhtn%2BrfPWi%2FPdDsKs7q69%2F2PIqv%2Fmr9OLxQbZU5tLxcBkVEeL%2BcGez4xFCUkMUix2He9Ge%0Ask4iF4%2BnLUsUI3%2Fa8UFpYTCGRzih7aB9hfYU0UoSJ8wf7QIfs9y5OKMcX6G9WGgphx%2F2Rzsze3s8%0A6gbnMJYuRap%2FPtMgyOFBYH8KI1MRYs0vibQ9qf4ZU3ivpRVXC8pfe%2FtVlowkT9Umq6yb5khMlhUs%0At3M14JN0Xv%2F%2FkY%2FFVlS%2FIWACnphABSZQBQfFK8pwCHpF5h0iXh2cFQ5sv1XdL5I3fpwc7etdS90l%0A5LnQAwOoof2Te3UqPXQtRzI4wxk03P69v%2BmcZ6YM23HVgpux7P6UZjp6V8Ky9Zi3fK2XNRPiILkY%0ALCxO6I5VsBN6vcEGWnpMsyEIauliTpufbLA5HJHXTwrJG9fOZGdARkiGcPSPWTKr6qn50ayEOrKC%0A7ch08V9n7VOYOyRGMUjsz2HOdAvDGZQlCF1xOMs5HFGQ2J%2BDPjcTN4aTjiK3ZaH5bu5XyoiIIHCT%0AJObTDwcmFsbly7FnfD4TSSpjUWyyZywVbpHUUipF6GWYkc4rBYYUENifwnQ8FByYtscY41cbXxd%2B%0ACc1kDCD9afMwowYbjOO2bI68058TGKEibrKb4Roz0cVsljKxIy%2Bhk74oXDYaVGLNXkbpODdzckim%0A7OrJOGMWBHMRZG7Cgg6MxGhE4Z356HkmzwQP1XJj6mnP0VEOrSi%2F%2FQTeHi0of%2ByrQaEYc9zkCVAj%0Ao%2BH5T2IT0iVJx87jwkRBCCkg8J2P%2FwVQSwcIaFzYiKUEAADQIgAA%0A; JSESSIONID=74AFA263B8D889533021E8BB74DF46B3; ExportItem=thesis_XWN201704140000001516; Hm_lpvt_838fbc4154ad87515435bf1e10023fab=1605066412'
    }

    allschool=get_school()
    # 获取每个学校所有论文ID
    # allschool = {'天津大学':1}

    # 读取论文ID，获取论文具体信息，allschool.txt存储爬取论文个数，支持断点继续
    for school_name in allschool:
        print('学校：'+school_name)
        if not is_school_id_exists(school_name):
            print('该学校数据无存储，开始获取数据')
            school_id_list = get_school_ids(school_name)
            save_school_id(school_name, school_id_list)

        school_id_list = read_school_id(school_name)
        total_num = len(school_id_list)
        start_id_num = allschool[school_name]
        print('论文总数：'+str(total_num))
        if start_id_num != 1:
            if start_id_num == total_num+1:
                print('已全部完成！')
                continue
            print('从' + str(start_id_num) + '开始继续爬')
        i = 0
        for num in range(start_id_num, total_num+1):
            try:
                # 获取每篇论文的详细信息
                paper_info = get_info(school_id_list[num-1],headers)
                save_data(paper_info, school_name)
                i = i+1
                update_school(allschool, school_name, num+1)
                time.sleep(SLEEP_TIME_2)
            except:
                update_school(allschool, school_name, num)
                print("---------------爬取错误！！爬取至" + str(num) + "!---------------")
                time.sleep(SLEEP_TIME_3)

        print('---------------本次成功爬取'+str(i)+'条数据---------------')
        csv2json(school_name)