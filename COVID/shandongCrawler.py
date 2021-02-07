import requests
from bs4 import BeautifulSoup
import chardet
root_url_shandong = 'http://wsjkw.shandong.gov.cn/ztzl/rdzt/qlzhfkgz/tzgg/'
root = 'http://wsjkw.shandong.gov.cn/ztzl/rdzt/qlzhfkgz/tzgg/'
pages_url = []
def get_pages_url():
    req = requests.get(url = root_url_shandong)
    after_gzip = req.content
    chardet.detect(after_gzip)
    req = after_gzip.decode('UTF-8')
    bf = BeautifulSoup(req)
    texts = bf.find_all('ul',class_="news-txtd")
    a_bf = BeautifulSoup(str(texts[0]))
    a = a_bf.find_all('a')

    for each in a:
        if "疫情情况" in each.text:
            pages_url.append(root+each.get('href').lstrip("./"))


def get_info(url):
    print(url)
    req = requests.get(url)
    after_gzip = req.content
    chardet.detect(after_gzip)
    req = after_gzip.decode('UTF-8')
    bf = BeautifulSoup(req)
    texts = bf.find_all('div', class_='text')

    try:
        info_parts = texts[0].text.strip()
        f.write(url)
        f.write('\n')
        f.write(info_parts)
        f.write('\n\n')
    except:
        pass
    pass


f = open('shandong.txt', 'w')
get_pages_url()
for page in pages_url:
    get_info(page)
f.close()