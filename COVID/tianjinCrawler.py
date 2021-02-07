import requests
from bs4 import BeautifulSoup,CData
import chardet
import re
import csv
root_url = 'http://wsjk.tj.gov.cn/col/col87/index.html'
root = 'http://wsjk.ln.gov.cn/wst_zdzt/xxgzbd/yqtb/'
pages_url = []
info_list = []

def get_pages_url():
    i = 1
    current_url = root_url
    #while(requests.get(url = current_url+str(i))):

    while(i<5):
        params = {
            'uid': '259',
            'pageNum':str(i)
                  }
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        }
        print(current_url)
        req = requests.get(url = current_url, params=params, headers=headers)
        after_gzip = req.content
        code_type= chardet.detect(after_gzip)
        req = after_gzip.decode(code_type['encoding'])
        print(req)
        bf = BeautifulSoup(req, "lxml")
        texts = bf.find_all('ul',class_="Clear")

        pattern = re.compile(r'<a href=\'(.*?)\'.*?>(.*?)</a>')  # 查找数字
        result = pattern.findall(str(texts[0]))
        print(str(texts[0]))

        for link,title in result:
            if "确诊" in title: #and "无" not in title:
                pages_url.append(link)
                print(title)

        i = i+1
        current_url = root_url


def get_info(url):
    print(url)
    req = requests.get(url)
    after_gzip = req.content
    code_type = chardet.detect(after_gzip)
    req = after_gzip.decode(code_type['encoding'])
    bf = BeautifulSoup(req, "lxml")
    texts = bf.find('div', class_='page_content Clear')
    try:
        info_parts = texts.text.strip()
        info_list.append([url, info_parts])
    except:
        pass
    pass


with open('tianjin.csv', 'w', encoding='gbk',errors='ignore') as f:
    get_pages_url()
    print(len(pages_url))
    for page in pages_url:
        get_info(page)
    # writer = csv.writer(f)
    # writer.writerows(info_list)