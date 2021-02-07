import requests
import re
import random
import time


class download(object):
    """docstring for download"""

    def __init__(self):
        self.headers = {}#'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'

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
            self.iplist.append(iplistn[x] + ':' + portlistn[x])

    def get(self, url, timeout, proxy=None, num_retries=6):
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
