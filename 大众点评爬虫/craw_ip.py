# -*- coding: cp936 -*-
import requests
import random
import time

def get_proxy(headers):
    #proxy_url��ͨ������HTTP������վ��������ɴ���api���ӣ�ÿ������api���Ӷ����µ�ip
    proxy_url = ('http://api.dmdaili.com/dmgetip.asp?apikey=e8a2169f&pwd=ca7c374414bd4005c910e4f7461c738c&getnum=1&httptype=1&geshi=1&fenge=1&fengefu=&Contenttype=3&operate=all')
    aaa=requests.get(proxy_url, headers=headers).text
    proxy_host = aaa.splitlines()[0]
    print('����IPΪ��'+proxy_host)
    #proxy_host='117.35.254.105:22001'
    #proxy_host='192.168.0.134:1080'
    with open('proxies.txt', 'a') as f:
        # for proxy in proxys:
        f.write('https://'+proxy_host + '\n')
    proxy = {
        'http': 'http://'+proxy_host,
        'https': 'http://'+proxy_host
    }
    return proxy
def generalProxies():
    headers = {
        "User-Agent": 'Mozilla/5.0'
    }
    proxys = []
    for i in range(3):
        proxy = get_proxy(headers)
        print('HTTPS����')
        requests.packages.urllib3.disable_warnings()  # �ر�HTTPSУ��
        url = 'https://myip.top'
        try:
            r = requests.get(url, headers=headers, proxies=proxy, verify=False)
            proxys.append(proxy.get('http'))
        except:
            print('����ʹ��ʧ�ܣ����������IP')
        time.sleep(1)
    return proxys

if __name__ == '__main__':
    headers = {
        "User-Agent": 'Mozilla/5.0'
    }
    proxys = []
    for i in range(3):
        proxy = get_proxy(headers)
        print('HTTPS����')
        requests.packages.urllib3.disable_warnings()#�ر�HTTPSУ��
        url = 'https://myip.top'
        try:
            r = requests.get(url, headers=headers, proxies=proxy, verify=False)
            print(r.status_code)
            print(r.text)
        except:
            print('����ʹ��ʧ�ܣ����������IP')
        time.sleep(1)

