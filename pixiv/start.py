from pachong import Pzhan
import re

while True:
    ID = input('请输入作者ID: ')
    if re.match(r'^\d{0,11}$', str(ID)):
        break
    else:
        print('输入格式错误,请重新输入!')

key = input('默认目录为F:\Pzhan,若要使用默认目录请输入Y/y,若自定义目录请输入N/n\n')

while key != 'y' and key != 'Y' and key != 'N' and key != 'n':
    key = input('输入格式错误,请重新输入!\n')

if key == 'n' or key == 'N':
    while True:
        mulu = input('请输入目录: ')
        if re.match(r'[A-Z]\:\\(\w+\\?)+', str(mulu)):
            break
        else:
            print('输入格式错误,请重新输入!')
elif key == 'y' or key == 'Y':
    mulu = 'F:\\Pzhan'

Pzhan.get_path(mulu)

Pzhan.all_page('member_illust.php?id=' + str(ID) + '&type=all')

input('爬虫结束~')
