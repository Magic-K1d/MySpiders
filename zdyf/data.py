import csv
import os

years = [2016, 2017, 2018, 2019, 2020]

data = {}
for year in years:
    data[year] = []
    with open('projects_' + str(year) + '.csv', 'r', encoding='utf-8') as f:
        csvreader = csv.reader(f)
        header = next(csvreader)
        print(header)
        for row in csvreader:
            if row:
                data[year].append(row)

# print(data)
input()
zhuanxiang = []
for year in years:
    if year in [2016, 2017]:
        for x in data[year]:
            zhuanxiang.append(x[7])
    if year in [2018, 2019]:
        for x in data[year]:
            zhuanxiang.append(x[6])
    if year in [2020]:
        for x in data[year]:
            zhuanxiang.append(x[4])

zhuanxiang = list(set(zhuanxiang))
print(len(zhuanxiang))

file_dict = {}
for root, dirs, files in os.walk('./html/项目指南'):
    for file in files:
        with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
            file_dict[file] = f.read()

# print(file_dict)

result1 = [['重点专项', '指南']]
for xiangmu in zhuanxiang:
    # xiangmu = xiangmu.replace('”', '')
    # xiangmu = xiangmu.replace('“', '')
    print(xiangmu)
    for file in file_dict:
        if xiangmu in file_dict[file]:
            result1.append([xiangmu, file])
            break

print(result1)
print(len(result1))

with open('zhinan.csv', 'w', encoding='utf-8') as f:
    csvwriter = csv.writer(f)
    for res in result1:
        csvwriter.writerow(res)