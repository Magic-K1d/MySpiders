#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from download import request
from pymongo import MongoClient
import datetime
import time
import os
import re


class jiandan(object):
    def __init__(self):
        self.path = 'D:\jiandan'
        self.pageNum = 1
        self.index_url = 'http://jandan.net/ooxx'
        self.url = 'http://jandan.net/ooxx/page-' + str(self.pageNum) + '#comments'
        client = MongoClient()  ##与MongDB建立client（这是默认连接本地MongDB数据库）
        db = client['zzx']  ## choose a db
        self.jiandan_collection = db['jiandan']  ##choose a collection in db
        self.author = ''  ##author
        self.img_urls = []  ##img url list
        self.pageNum_Max = int(BeautifulSoup(request.get(self.index_url, 3).text, 'lxml').find('div', class_='cp-pagenavi').find('span').get_text().strip('[]'))

    def all_page(self):
        while(self.pageNum <= self.pageNum_Max):
            html = request.get(self.url, 3)
            self.get_img(html)


            self.pageNum += 1
            self.url = 'http://jandan.net/ooxx/page-' + str(self.pageNum) + '#comments'

    def get_img(self, html):
        Soup = BeautifulSoup(html.text, 'lxml')
        all_li = Soup.find('ol', class_="commentlist").find_all('li')
        for li in all_li:
            img_href_list = []
            author = li.find('div', class_='author').find('strong').get_text()
            time = li.find('div', class_='author').find('small').get_text()
            like = int(li.find('div', class_='jandan-vote').find('span', class_='tucao-like-container').find('span').get_text())
            unlike = int(li.find('div', class_='jandan-vote').find('span', class_='tucao-unlike-container').find('span').get_text())

            if like > 2*unlike:
                print(author, time)
                '''
                if self.jiandan_collection.find_one({'img_url': href}):  ##判断这个主题是否已经在数据库中、不在就运行else下的内容，在则忽略。
                    print(u'这个页面已经爬取过了')
                    break
                '''
                img_tag_a_n = li.find('div', class_='text').find('p').find_all('a', class_='view_img_link')
                for img_tag_a in img_tag_a_n:
                    img_href_list.append('http:'+img_tag_a['href'])
                if not self.jiandan_collection.find_one({'img_url': img_href_list}):
                    img_num = 0
                    for img_href in img_href_list:
                        img_num += 1
                        self.save_img(img_href, author, img_num, like, unlike)
                    post = {
                        'author': author,
                        'time': time,
                        'get_time': datetime.datetime.now(),
                        'like': like,
                        'unlike': unlike,
                        'img_url': img_href_list
                    }
                    self.jiandan_collection.save(post)
                    print('Success add ',img_href_list, like, unlike, '\n')
                else:
                    print("The URL is exists!\n")


    def save_img(self, img_url, author, img_num, like, unlike):
        os.chdir(os.path.join(self.path))
        name = author + str(img_num) + '__' + str(like) + str(unlike) + '__' + img_url[-7:]
        #request.headers['referer'] = self.url + page_url[1:]
        img = request.get(img_url, 10)
        if re.compile('<center><h1>502 Bad Gateway</h1></center>').match(img.text):
            print(re.compile('<center><h1>502 Bad Gateway</h1></center>').match(img.text))
            time.sleep(10)
            return self.save_img(img_url, author, img_num)
        else:
            f = open(name, 'ab')
            f.write(img.content)
            f.close()
            print('Success save ', name, '\n')


jiandan1 = jiandan()
if __name__ == "__main__":
    #jiandan1.get_img(request.get('http://jandan.net/ooxx/page-1#comments', 3))
    jiandan1.all_page()
