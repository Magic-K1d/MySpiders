import requests
from bs4 import BeautifulSoup
import chardet
root_url_shandong = 'http://www.hnwsjsw.gov.cn/channels/854.shtml'
root = 'http://www.hnwsjsw.gov.cn'
pages_url = []
def get_pages_url():
    i = 1
    current_url = root_url_shandong
    while(requests.get(url = current_url)):
        print(current_url)
        req = requests.get(url = current_url)
        after_gzip = req.content
        chardet.detect(after_gzip)
        req = after_gzip.decode('UTF-8')
        bf = BeautifulSoup(req, "lxml")
        texts = bf.find_all('ul',class_="list-group listmain")
        a_bf = BeautifulSoup(str(texts[0]))
        a = a_bf.find_all('a')

        for each in a:
            if "河南省新型冠状病毒" in each.text:
                if "疫情情况" in each.text:
                    pages_url.append(root + each.get('href'))
                    print(each.text)

        i = i+1
        current_url = 'http://www.hnwsjsw.gov.cn/channels/854_'+str(i)+'.shtml'


def get_info(url):
    print(url)
    req = requests.get(url)
    after_gzip = req.content
    chardet.detect(after_gzip)
    req = after_gzip.decode('UTF-8')
    bf = BeautifulSoup(req, "lxml")
    texts = bf.find('div', id='artibody')
    try:
        info_parts = texts.text.strip()
        f.write(url)
        f.write('\n')
        f.write(info_parts)
        f.write('\n\n')
    except:
        pass
    pass


f = open('henan.txt', 'w')
get_pages_url()
for page in pages_url:
    get_info(page)
f.close()