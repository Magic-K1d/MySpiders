import csv
import os
from bs4 import BeautifulSoup
import json


file_dict = {}
for root, dirs, files in os.walk('./html/答辩通知'):
    for file in files:
        with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
            file_dict[file] = f.read()

# print(file_dict)
project_dict = {}
for file in file_dict:
    print(file)
    a = file.find('“')
    b = file.find('”')
    project_name = file[a+1:b]
    soup = BeautifulSoup(file_dict[file], 'html.parser')
    content = soup.find('div', class_='single-content')
    content = content.find_all('tbody')
    if content:
        content_list = []
        print(len(content))
        trs1 = content[0].find_all('tr')
        tds = trs1[0].find_all('td')
        if len(content) == 1 and len(tds) != 1:
            for tr in trs1:
                tmp = []
                tds = tr.find_all('td')
                # if len(tds) == 1:
                #     print(tds[0].text)
                #     exit(1)
                for td in tds:
                    tmp.append(td.text)
                if tmp:
                    content_list.append(tmp)
        else:
            content_list = {}
            zu = '0'
            date = '0'
            for tbody in content:
                trs = tbody.find_all('tr')
                for tr in trs:
                    tmp = []
                    tds = tr.find_all('td')
                    if len(tds) == 1:
                        if '组' in tds[0].text or tr == trs[0]:
                            zu = tds[0].text
                            content_list[zu] = {}
                            print(tds[0].text)
                        if '年' in tds[0].text or '-' in tds[0].text:
                            date = tds[0].text
                            print(tds[0].text)
                            content_list[zu][date] = []
                    else:
                        for td in tds:
                            tmp.append(td.text)
                    if tmp:
                        content_list[zu][date].append(tmp)
    else:
        print(content)
    project_dict[project_name] = content_list


print(project_dict)

with open('dabian.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(project_dict, ensure_ascii=False))

# with open('zhinan.csv', 'w', encoding='utf-8') as f:
#     csvwriter = csv.writer(f)
#     for res in result1:
#         csvwriter.writerow(res)