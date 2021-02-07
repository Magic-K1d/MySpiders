from bs4 import BeautifulSoup
import os
from download import request
import re


class pachong(object):
    """docstring for pachong"""

    def __init__(self):
        self.url = 'http://www.pixiv.net/'
        self.mulu = 'F:\Pzhan'

    def get_path(self, mulu):
        self.mulu = mulu

    def all_page(self, PHP):
        html = request.get(self.url + PHP, 3)
        #input(html.text)
        Soup = BeautifulSoup(html.text, 'lxml')
        title = Soup.find('h1', class_='column-title').find('a', class_='self').get_text()
        author = str(title)
        self.mkdir(self.mulu, author)
        page_list = Soup.find('ul', class_='page-list').find_all('a')
        for page in page_list:
            self.allOfOnePage(Soup)
            list_url = page['href']
            html = request.get(self.url + 'member_illust.php' + list_url, 3)
            Soup = BeautifulSoup(html.text, 'lxml')

    def allOfOnePage(self, Soup):
        all_a = Soup.find('ul', class_='_image-items').find_all('a')
        # print(all_a)
        for a in all_a:
            try:
                if 'multiple' in a['class']:
                    page_url = a['href']
                    self.img_more(page_url)

                elif '_work' in a['class']:
                    page_url = a['href']
                    self.img(page_url)
                else:
                    print(a, '\n error!\n', a['class'])
            except:
                pass


                #	img_name = a.get_text()
                #	print(u'start save:',img_name)
                #	page_url = a.parent['href']
                ##	self.img(page_url , img_name)

    def img_more(self, page_url):
        page_html = request.get(self.url + page_url, 10)
        # print(page_html.text)
        img_name = BeautifulSoup(page_html.text, 'lxml').find('div', class_='layout-a').find('h1',
                                                                                             class_='title').get_text()
        print(img_name)
        page_img_list = re.sub('medium', 'manga', page_url)
        page_img_list_html = request.get(self.url + page_img_list[1:], 10)
        page_img_url = BeautifulSoup(page_img_list_html.text, 'lxml').find_all('a',class_=re.compile('full-size-container'),target='_blank')
        page_num = 0
        for a in page_img_url:
            request.headers['Upgrade-Insecure-Requests'] = '1'
            page_img_html = request.get(self.url + a['href'], 10)
            img_src = BeautifulSoup(page_img_html.text, 'lxml').find('img', src=re.compile('.jpg'))['src']
            self.save(img_src, img_name + str(page_num), page_img_list)
            page_num += 1

    def img(self, page_url):
        img_html = request.get(self.url + page_url, 10)
        img_name = BeautifulSoup(img_html.text, 'lxml').find('div', class_='layout-a').find('h1',
                                                                                            class_='title').get_text()
        print('Start save: ', img_name)
        img_src = BeautifulSoup(img_html.text, 'lxml').find('img', class_='original-image')['data-src']
        self.save(img_src, img_name, page_url)

    def save(self, img_src, img_name, page_url):
        name = img_name
        request.headers['referer'] = self.url + page_url[1:]
        img = request.get(img_src, 10)
        if re.compile('<center><h1>502 Bad Gateway</h1></center>').match(img.text):
            print(re.compile('<center><h1>502 Bad Gateway</h1></center>').match(img.text))
            return self.save(img_src, img_name, page_url)
        else:
            f = open(name + '__' + img_src[-15:], 'ab')
            f.write(img.content)
            f.close()

    def mkdir(self, mulu, author):
        author = author.strip()
        isExists = os.path.exists(os.path.join(mulu, author))
        if not isExists:
            print(u'建了一个名字叫做', author, u'的文件夹！')
            os.makedirs(os.path.join(mulu, author))
            os.chdir(os.path.join(mulu, author))  ##切换到目录
            return True
        else:
            print(u'名字叫做', author, u'的文件夹已经存在了！')
            os.chdir(os.path.join(mulu, author))  ##切换到目录
            return False


Pzhan = pachong()

if __name__ == '__main__':
    Pzhan.all_page('member_illust.php?id=2188232&type=all')
    ##pachong.img_more('/member_illust.php?mode=medium&illust_id=60181180')## text img_more
