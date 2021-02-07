import requests
from bs4 import BeautifulSoup
import chardet
root_url = 'http://wsjk.ln.gov.cn/wst_zdzt/xxgzbd/yqtb/index.html'
root = 'http://wsjk.ln.gov.cn/wst_zdzt/xxgzbd/yqtb/'
pages_url = []
def get_pages_url():
    i = 1
    current_url = root_url
    while(requests.get(url = current_url)):
        print(current_url)
        req = requests.get(url = current_url)
        after_gzip = req.content
        a = chardet.detect(after_gzip)
        print(a)
        req = after_gzip.decode('GB2312')
        bf = BeautifulSoup(req, "lxml")
        texts = bf.find_all('ul',class_="zxxx_list")
        a_bf = BeautifulSoup(str(texts[0]))
        a = a_bf.find_all('a')

        for each in a:
            if "疫情情况" in each.text:
                pages_url.append(root + each.get('href').lstrip("./"))
                print(each.text)

        current_url = 'http://wsjk.ln.gov.cn/wst_zdzt/xxgzbd/yqtb/index_'+str(i)+'.html'
        i = i+1


def get_info(url):
    print(url)
    req = requests.get(url)
    after_gzip = req.content
    chardet.detect(after_gzip)
    req = after_gzip.decode('GB2312')
    bf = BeautifulSoup(req, "lxml")
    texts = bf.find('div', class_='TRS_Editor')
    try:
        info_parts = texts.text.strip()
        f.write(url)
        f.write('\n')
        f.write(info_parts)
        f.write('\n\n')
    except:
        pass
    pass


f = open('liaoning.txt', 'w')
get_pages_url()
for page in pages_url:
    get_info(page)
f.close()