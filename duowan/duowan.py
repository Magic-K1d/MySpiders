#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from download import request
from pymongo import MongoClient
import datetime
import time
import os
import re

class duowan(object):
    ''''''

    def __init__(self):

        self.index = 'http://tu.duowan.com/tu'
        self.lxh_index = ''
        client = MongoClient()  ## MongDB client
        db = client['zzx']  ## choose a db
        self.duowan_collection = db['duowan_lxh']  ##choose a collection in db
        self.path = 'F:\\duowan'


    def get_all_href(self):
        index = request.get(self.index, 3)
        Soup = BeautifulSoup(index.text, 'lxml')
        li_tmp = Soup.find('div', id='subnav_pk').find_all('li')
        for li in li_tmp:
            if li.get_text()=='å·ç¬è¯':# å·ç¬è¯代表'冷笑话几个字'
                self.lxh_index = li.a['href']
                break
        lxh = request.get(self.lxh_index, 3)
        #print(lxh.text)
        Soup = BeautifulSoup(lxh.text, 'lxml')
        page_href_list = Soup.find_all('li', class_='box')
        page_num = 1
        for page in page_href_list:
            if page['class'] != ['box']:
                print(page['class'])
            else:
                page_title = page.find('em').get_text()
                page_link = page.find('em').find('a')['href']
                #print(page_title, page_link)
                self.get_img(page_title, page_link, page_num)
                page_num += 1


    def get_img(self, page_title, page_link, page_num):
        page_link = page_link.replace('gallery', 'scroll')
        page_img = request.get(page_link, 3)
        Soup = BeautifulSoup(page_img.text, 'lxml')
        img_div_list = Soup.find_all('div', class_='pic-box')
        img_num = 1
        for img_div in img_div_list:
            img_title = img_div.find('p').get_text()
            #input(img_div)
            if img_title != 'ä¸æé¢å':#'ä¸æé¢å'为'下集预告'
                img_src = img_div.find('span')['data-img']
                if not self.duowan_collection.find_one({'img_src': img_src}):
                    self.save_img(img_title, img_src, page_num, img_num)
                    post = {
                        'page_title': page_title,
                        'page_link': page_link,
                        'img_num': str(page_num)+'.'+str(img_num),
                        'img_title': img_title,
                        'img_src': img_src
                    }
                    print(img_title)
                    self.duowan_collection.save(post)
                    print('Success save img data')
                    img_num += 1
                else:
                    print('该页面已保存')
            else:
                break
        #return img_title, img_src

    def save_img(self, img_title, img_src, page_num, img_num):
        os.chdir(os.path.join(self.path))
        img = request.get(img_src, 3)
        name = str(page_num)+'.'+str(img_num)+'  ' + img_title + img_src[-8:]
        if re.compile('<center><h1>502 Bad Gateway</h1></center>').match(img.text):
            print(re.compile('<center><h1>502 Bad Gateway</h1></center>').match(img.text))
            time.sleep(10)
            return self.save_img(img_src, img_title)
        else:
            f = open(name, 'ab')
            f.write(img.content)
            f.close()
            print('Success save ', name, '\n')

duowan = duowan()
if __name__ == '__main__':
    duowan.get_all_href()