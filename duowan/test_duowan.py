from download import request
from bs4 import BeautifulSoup
lxh_index = ''
html = request.get('http://tu.duowan.com/tu', 3)
Soup = BeautifulSoup(html.text, 'lxml')
li_tmp = Soup.find('div', id='subnav_pk').find_all('li')
for li in li_tmp:
    print(li.get_text())
    if li.get_text()=='å·ç¬è¯':
        lxh_index = li.a['href']
        break
lxh = request.get(lxh_index, 3)
Soup = BeautifulSoup(lxh.text, 'lxml')
page_href_list = Soup.find_all('li', class_='box')
page_num = 1
for page in page_href_list:
    if page['class'] != ['box']:
        print(page['class'])
    else:
        page_title = page.find('em').get_text()
        page_link = page.find('em').find('a')['href']
        print(page_title, page_link)
#print(html.text)

