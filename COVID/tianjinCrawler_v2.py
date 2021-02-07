import requests
from bs4 import BeautifulSoup,CData
import chardet
import re
import csv

pages_url = []
info_list = []
url = 'http://wsjk.tj.gov.cn/module/web/jpage/dataproxy.jsp?page=1&webid=1&path=http://wsjk.tj.gov.cn/&columnid=87&unitid=259&webname=%25E5%25A4%25A9%25E6%25B4%25A5%25E5%25B8%2582%25E5%258D%25AB%25E7%2594%259F%25E5%2581%25A5%25E5%25BA%25B7%25E5%25A7%2594%25E5%2591%2598%25E4%25BC%259A&permissiontype=0'
#request info page
req = requests.get(url = url)
after_gzip = req.content
code_type= chardet.detect(after_gzip)
req = after_gzip.decode(code_type['encoding'])
#analyze page
pattern = re.compile(r'<a href=\'(.*?)\'.*?>(.*?)</a>')
result = pattern.findall(str(req))
for link, title in result:
    if "确诊" in title and "无" not in title:
        pages_url.append(link)
        print(title)
print(len(pages_url))

#request and save each page
for page_url in pages_url:
    print(page_url)
    req = requests.get(page_url)
    after_gzip = req.content
    code_type = chardet.detect(after_gzip)
    req = after_gzip.decode(code_type['encoding'])
    bf = BeautifulSoup(req, "lxml")
    texts = bf.find('div', class_='page_content Clear')
    try:
        info_parts = texts.text.strip()
        info_list.append([page_url, info_parts])
    except:
        pass
    pass

with open('tianjin.csv', 'w', encoding='gbk',errors='ignore') as f:
    writer = csv.writer(f)
    writer.writerows(info_list)