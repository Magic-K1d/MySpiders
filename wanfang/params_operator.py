import os
import csv
import json


def init_school():
    f = open('allschool.csv', 'r')
    content = f.read()
    school_list = {}
    rows = content.split('\n')
    for row in rows:
        row = row.split(',')
        if row[0] != '':
            school_list[row[0]] = row[1]
    # print(school_list)
    print(school_list)
    file1 = open('allschool.txt', 'w', encoding='utf-8')
    file1.write(str(school_list))
    file1.close()


def get_school():
    file = open('allschool.txt', 'r', encoding='utf-8')
    school_list = eval(file.read())
    file.close()
    return school_list


def update_school(school_list, school, page):
    school_list[school] = page
    file1 = open('allschool.txt', 'w', encoding='utf-8')
    file1.write(str(school_list))
    file1.close()


def save_school_id(school, school_id_list):
    if not os.path.exists('./school_id_data'):
        os.makedirs('./school_id_data/')
    with open('./school_id_data/' + school + '.txt', 'w', encoding = 'utf-8') as file:
        file.write(str(school_id_list))

def read_school_id(school):
    with open('./school_id_data/' + school + '.txt', 'r', encoding = 'utf-8') as file:
        school_id_list = eval(file.read())
        return school_id_list

def is_school_id_exists(school):
    if os.path.exists('./school_id_data/' + school + '.txt'):
        return True
    else:
        return False


def save_data(paper_info, school):
    if not os.path.exists('data/' + school + '.csv'):
        with open('data/' + school + '.csv', 'a', encoding='utf-8') as file:
            file.write('title, authors, organizations, degree, major, tutors, year, language, url')
            file.write('\n')
        file.close()
    if (paper_info[0] != ''):
        with open('data/' + school + '.csv', 'a', encoding='utf-8') as file:
            for i in range(9):
                if i != 8:
                    file.write(str(paper_info[i]))
                    file.write(',')
                else:
                    file.write(str(paper_info[i]))
            file.write('\n')


def csv2json(school):
    if not os.path.exists('data/' + school + '.csv'):
        return
    schoolData = []
    with open('data/'+school+'.csv','r',encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # 读取的内容是字典格式的
            if dict(row) not in schoolData:
                schoolData.append(dict(row))
    print("---------------csv2json转换共"+str(len(schoolData))+"条数据------------")
    with open('json_data/'+school+'.json','w', encoding = 'utf-8') as f:
        f.write(json.dumps(schoolData,ensure_ascii=False,indent=2 ))
    
    