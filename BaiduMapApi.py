# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 15:47:07 2018

@author: Administrator
"""

from urllib import parse
import hashlib
 
def get_urt(address,city,myak):
 
    # 以get请求为例http://api.map.baidu.com/geocoder/v2/?address=百度大厦&output=json&ak=你的ak
    queryStr = '/geocoder/v2/?address=%s&output=json&city=%s&ak=%s' % (address,city,myak)
 
    # 对queryStr进行转码，safe内的保留字符不转换
    encodedStr = parse.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")
 
    # 在最后直接追加上yoursk
    #rawStr = encodedStr + 'tFHW4eSwspGUcg7sI1jNiG5Ri1u6kBhr'
 
    #计算sn
    #sn = (hashlib.md5(parse.quote_plus(rawStr).encode("utf8")).hexdigest())
     
    #由于URL里面含有中文，所以需要用parse.quote进行处理，然后返回最终可调用的url
    url = parse.quote("http://api.map.baidu.com"+queryStr, safe="/:=&?#+!$,;'@()*[]")  #+"&sn="+sn
     
    return url



import requests

myak='gv7AD3IpfaWdDVugtaoSXxbkCuy4LIxL'

def get_location(address,city,myak=myak):
    url=get_urt(address,city,myak)
    response=requests.get(url)
    answer = response.json()
    lng=answer['result']['location']['lng']
    lat=answer['result']['location']['lat']
    location='%.6f,%.6f'%(lat,lng)
    return location

location1=get_location('陆家嘴金融城人才公寓','上海')
location2=get_location('虹口星外滩','上海')


def get_transit(location1,location2,myak=myak):
    url='http://api.map.baidu.com/direction/v2/transit?origin=%s&destination=%s&ak=%s'%(location1,location2,myak)
    response=requests.get(url)
    answer=response.json()
                              
    route=answer['result']['routes'][0]
    distance=route['distance']
    duration=route['duration']










