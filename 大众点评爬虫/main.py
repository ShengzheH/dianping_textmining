# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 16:42:52 2018

@author: bin
"""

#目标爬取店铺的评论

import requests
from bs4 import BeautifulSoup
import time, random
import mysqls
import re
from fake_useragent import UserAgent
import os

ua = UserAgent()

#设置cookies
# cookie = "_lxsdk_cuid=18d8d0b2b4ac8-050d3433d8267b-26001851-1bcab9-18d8d0b2b4ac8; _lxsdk=18d8d0b2b4ac8-050d3433d8267b-26001851-1bcab9-18d8d0b2b4ac8; _hc.v=3f5a2a7d-cb97-170a-f1db-541fb4e7c7a7.1707468336; WEBDFPID=v7wwvzz8y9x75w9z0549438wu4yx75x481w1w9y2v7097958v6583u07-2022828356662-1707468356662WOAMMOIfd79fef3d01d5e9aadc18ccd4d0c95072944; s_ViewType=10; dper=0202252374fefdda8d3bcaf2190df68da0685fee41e7046be951c15080b9b3d6500886d3d7b210c31a62bdfc7018fa258694527dc576dc16484b00000000ff1d000005ccc7b447bf00053ad20b3bd31f5ef0e3ebfae3a93954f3cd429a245d6c73ab51d66fb2dd07978dec317c7cf6258b34; qruuid=98aae10d-b00d-41b9-805d-335fd5b8c605; fspop=test; ll=7fd06e815b796be3df069dec7836c3df; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1707468338,1707987682,1708568364; cy=2345; cye=chiangmai; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1708571635; _lxsdk_s=18dcf1b402d-d4b-f2f-cfa%7C%7C1"
cookie = "_lxsdk_cuid=18d8d0b2b4ac8-050d3433d8267b-26001851-1bcab9-18d8d0b2b4ac8; _lxsdk=18d8d0b2b4ac8-050d3433d8267b-26001851-1bcab9-18d8d0b2b4ac8; _hc.v=3f5a2a7d-cb97-170a-f1db-541fb4e7c7a7.1707468336; WEBDFPID=v7wwvzz8y9x75w9z0549438wu4yx75x481w1w9y2v7097958v6583u07-2022828356662-1707468356662WOAMMOIfd79fef3d01d5e9aadc18ccd4d0c95072944; s_ViewType=10; dper=0202252374fefdda8d3bcaf2190df68da0685fee41e7046be951c15080b9b3d6500886d3d7b210c31a62bdfc7018fa258694527dc576dc16484b00000000ff1d000005ccc7b447bf00053ad20b3bd31f5ef0e3ebfae3a93954f3cd429a245d6c73ab51d66fb2dd07978dec317c7cf6258b34; fspop=test; cy=2345; cye=chiangmai; ll=7fd06e815b796be3df069dec7836c3df; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1708583111,1708921943,1708925236,1708938439; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1708938560; _lxsdk_s=18de4ab22b7-48d-882-d53%7C%7C90"

#修改请求头
headers = {
        'User-Agent':ua.random,
        'Cookie':cookie,
        'Connection':'keep-alive',
        'Host':'www.dianping.com',
        'Referer': 'http://www.dianping.com/shop/l9mmAq3BMmspvQb8/review_all/p1'
}

#从ip代理池中随机获取ip
ips = open('proxies.txt','r').read().split('\n')

def get_random_ip():
   ip = random.choice(ips)
   pxs = {ip.split(':')[0]:ip}
   return pxs

#获取html页面
def getHTMLText(url,code="utf-8"):
    try:
        proxy = get_random_ip()
        print(proxy)
        time.sleep(random.random()*6 + 2)
        r=requests.get(url, timeout = 5, headers=headers, 
                      proxies=proxy
                       )
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        print("产生异常")
        return "产生异常"

#因为评论中带有emoji表情，是4个字符长度的，mysql数据库不支持4个字符长度，因此要进行过滤
def remove_emoji(text):
    try:
        highpoints = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return highpoints.sub(u'',text)

#从html中提起所需字段信息
def parsePage(html,shpoID):
    infoList = [] #用于存储提取后的信息，列表的每一项都是一个字典
    soup = BeautifulSoup(html, "html.parser")
    
    for item in soup('div','main-review'):
        cus_id = item.find('a','name').text.strip()
        comment_time = item.find('span','time').text.strip()
        try:
            comment_star = item.find('span',re.compile('sml-rank-stars')).get('class')[1]
        except:
            comment_star = 'NAN'
        cus_comment = item.find('div',"review-words").text.strip()
        scores = str(item.find('span','score'))
        try:
            kouwei = re.findall(r'口味：([\u4e00-\u9fa5]*)',scores)[0]
            huanjing = re.findall(r'环境：([\u4e00-\u9fa5]*)',scores)[0]
            fuwu = re.findall(r'服务：([\u4e00-\u9fa5]*)',scores)[0]
        except:
            kouwei = huanjing = fuwu = '无'
        
        infoList.append({'cus_id':cus_id,
                         'comment_time':comment_time,
                         'comment_star':comment_star,
                         'cus_comment':remove_emoji(cus_comment),
                         'kouwei':kouwei,
                         'huanjing':huanjing,
                         'fuwu':fuwu,
                         'shopID':shpoID})
    return infoList

#构造每一页的url，并且对爬取的信息进行存储
def getCommentinfo(shop_url, shpoID, page_begin, page_end):
    for i in range(page_begin, page_end):
        try:
            url = shop_url + 'p' + str(i)
            html = getHTMLText(url)
            infoList = parsePage(html,shpoID)
            print('成功爬取第{}页数据,有评论{}条'.format(i,len(infoList)))
            for info in infoList:
                mysqls.save_data(info)
            #断点续传中的断点
            if (html != "产生异常") and (len(infoList) != 0):
                with open('xuchuan.txt','a') as file:
                    duandian = str(i)+'\n'
                    file.write(duandian)
            else:
                print('休息60s...')
                time.sleep(60)
        except:
            print('跳过本次')
            continue
    return

def xuchuan():
    if os.path.exists('xuchuan.txt'):
        file = open('xuchuan.txt','r')
        nowpage = int(file.readlines()[-1])
        file.close()
    else:
        nowpage = 0
    return nowpage

#根据店铺id，店铺页码进行爬取
def craw_comment(shopID='l9mmAq3BMmspvQb8',page = 37):
    shop_url = "http://www.dianping.com/shop/" + shopID + "/review_all/"
    #读取断点续传中的续传断点
    nowpage = xuchuan()
    getCommentinfo(shop_url, shopID, page_begin=nowpage+1, page_end=page+1)
    mysqls.close_sql()
    return

if __name__ == "__main__":
    craw_comment()
        