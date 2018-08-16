# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 09:57:41 2018

@author: Administrator
"""

# 仅爬取西刺代理首页IP地址

from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request
from urllib import request

def get_ip_list(url = 'http://www.xicidaili.com/'):
    headers = {'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
    request = Request(url, headers=headers)
    response = urlopen(request)
    bsObj = BeautifulSoup(response, 'lxml')     # 解析获取到的html
    ip_list=get_ip_list(bsObj)
    ip_text = bsObj.findAll('tr', {'class': 'odd'})   # 获取带有IP地址的表格的所有行
    ip_list = []
    for i in range(len(ip_text)):
        ip_tag = ip_text[i].findAll('td')   
        ip_port = ip_tag[1].get_text() + ':' + ip_tag[2].get_text() # 提取出IP地址和端口号
        ip_list.append(ip_port)
    print("共收集到了{}个代理IP".format(len(ip_list)))
    print(ip_list)
    return ip_list

ip_list=get_ip_list()



url = 'https://www.baidu.com/'
#这是代理IP
proxy = {'https':'122.235.169.198:8118'}
#创建ProxyHandler
proxy_support = request.ProxyHandler(proxy)
#创建Opener
opener = request.build_opener(proxy_support)
#添加User Angent
opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
#安装OPener
request.install_opener(opener)
#使用自己安装好的Opener
response = request.urlopen(url)
#读取相应信息并解码
html = response.read().decode("utf-8")
#打印信息
print(html)

