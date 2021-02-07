import requests
from bs4 import BeautifulSoup
import csv
import os


def get_projects(url, table_num):
    projects = []
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    content = soup.find('div', class_='single-content')
    content = content.find_all('table')[table_num].find('tbody')
    for tr in content.find_all('tr'):
        tmp = []
        for td in tr.find_all('td'):
            tmp.append(td.text)
        projects.append(tmp)

    return projects


def save_projects(projects, year):
    with open('projects_' + str(year) + '.csv', 'w', encoding='utf-8') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerows(projects)


if __name__ == '__main__':
    # url_dict = {
    #     2016: 'https://www.sciping.com/22798.html',
    #     2017: 'https://www.sciping.com/22487.html',
    #     2018: 'https://www.sciping.com/31249.html',
    #     2019: 'https://www.sciping.com/31299.html',
    #     2020: 'https://www.sciping.com/35357.html'
    # }
    # for year in url_dict:
    #     if year in [2018, 2019]:
    #         table_num = 3
    #     else:
    #         table_num = 2
    #     projects = get_projects(url_dict[year], table_num)
    #     print(projects)
    #     save_projects(projects, year)

    url = 'https://www.sciping.com/keyproject.html'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = soup.find('div', class_='single-content')
    content = content.find_all('ul')
    result_list = []
    for ul in content:
        tmp = []
        li_list = ul.find_all('li')
        for li in li_list:
            a = li.find('a')
            tmp.append([a['href'], a.text])
        result_list.append(tmp)

    keys = ['年度统计', '阶段统计', '深度分析', '公示信息', '征求意见稿', '项目指南', '答辩通知', '制度流程', '媒体报道']
    result_dict = {}
    for i in range(len(keys)):
        result_dict[keys[i]] = result_list[i]

    print(result_dict)

    for key in result_dict:
        path = '.\\' + key
        if not os.path.exists(path):
            os.makedirs(path)

        for link in result_dict[key]:
            res = requests.get(link[0])
            encoding = res.encoding
            # Format file name
            link[1] = link[1].replace('|', '')
            link[1] = link[1].replace('\\', '')
            link[1] = link[1].replace('/', '')
            link[1] = link[1].replace('*', '')
            link[1] = link[1].replace('<', '')
            link[1] = link[1].replace('>', '')
            link[1] = link[1].replace('?', '')
            print(link[1])

            with open(os.path.join(path, link[1] + '.html'), 'w', encoding=encoding) as f:
                f.write(res.text)



