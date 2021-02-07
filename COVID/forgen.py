# -*- coding: UTF-8 -*-


import requests
from bs4 import BeautifulSoup

citys = ['korea']
root_url = 'https://raw.githubusercontent.com/pomber/covid19/master/docs/timeseries.json'
page = requests.get(url = root_url)
print(page.text)