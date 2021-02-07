import requests
import re
import random
import time


class download(object):
    """docstring for download"""

    def __init__(self):
        self.headers = {
            'Cookie': "p_ab_id=4; p_ab_id_2=7; login_ever=yes; special_notification_rating=1; login_bc=1; _ga=GA1.2.866230686.1490967496; _gid=GA1.2.128659359.1497019443; PHPSESSID=22256281_55e12087306321e5f0b7758dcbcfebd4; device_token=7201c780ae5152ae4df9510e7283feca; a_type=0; is_sensei_service_user=1; module_orders_mypage=%5B%7B%22name%22%3A%22recommended_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22fanbox%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D; __utmt=1; __utma=235335808.866230686.1490967496.1496910978.1497019439.17; __utmb=235335808.8.10.1497019439; __utmc=235335808; __utmz=235335808.1494048895.15.4.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=22256281=1^9=p_ab_id=4=1^10=p_ab_id_2=7=1^11=lang=zh=1^14=hide_upload_form=yes=1^15=machine_translate_test=no=1"}

        self.user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
        self.iplist = []
        #		html = requests.get("http://haoip.cc/tiqu.htm")
        #		iplistn = re.findall(r'r/>(.*?)<b', html.text, re.S)
        #		for ip in iplistn:
        #			i = re.sub('\n', '', ip)
        #			self.iplist.append(i.strip())
        html = requests.get("http://www.kuaidaili.com/free/inha/1/")
        iplistn = re.findall(r'IP">(.*?)</td', html.text, re.S)
        portlistn = re.findall(r'PORT">(\d*?)</td', html.text, re.S)
        for x in range(len(iplistn)):
            self.iplist.append(iplistn[x] + ' ' + portlistn[x])

    def get(self, url: object, timeout: object, proxy: object = None, num_retries: object = 6) -> object:
        print(url + '\n')
        UA = random.choice(self.user_agent_list)
        self.headers['user_agent'] = UA

        if proxy == None:
            try:
                return requests.get(url, headers=self.headers, timeout=timeout)
            except:
                if num_retries > 0:
                    time.sleep(10)
                    print(u'Error! well try ', num_retries, u' times.')
                    return self.get(url, timeout, num_retries - 1)
                else:
                    print(u'start use proxy!')
                    time.sleep(10)
                    IP = ''.join(str(random.choice(self.iplist)).strip())
                    proxy = {'http': IP}
                    return self.get(url, timeout, proxy, )
        else:
            try:
                print(u'start use proxy!')
                time.sleep(10)
                IP = ''.join(str(random.choice(self.iplist)).strip())
                proxy = {'http': IP}
                print('proxy is :', proxy)
                return requests.get(url, headers=self.headers, proxies=proxy, timeout=timeout)
            except:
                print(u'Proxy is useless! Well shut down it!')
                return self.get(url, 3)


request = download()  ##
