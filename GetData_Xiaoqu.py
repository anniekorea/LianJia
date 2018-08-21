# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 15:36:29 2018

@author: Administrator
"""


headers={'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
       'Accept-Language': 'zh-CN,zh;q=0.9',
       'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}



#爬取小区的经纬度，画热力图
def get_html_xiaoqu(city,headers):
    from GetData_html import get_small_quyu_link,get_page_num,get_html,save_html
    import datetime

    datestr=datetime.datetime.now().strftime('%Y%m%d')
    
    (quyu_list,quyu_link_list)=get_small_quyu_link(city,headers,url_last='xiaoqu',savefolder='linklist_xiaoqu')

    #爬数据，并保存在子文件夹save_html_data_xiaoqu中，每个日期一个文件夹，同一天的数据放在以日期命名的子文件夹中
    for i in range(0,len(quyu_link_list)):
        url=quyu_link_list[i]
        quyu=quyu_list[i]
        totalPage=get_page_num(url,headers)
        print(str(i)+'/'+str(len(quyu_link_list))+','+quyu+',共'+str(totalPage)+'页')
        if totalPage==0:
            html=''
        else:
            html=get_html(url,totalPage,headers)
        save_html(html,datestr,city,quyu,save_folder_path='../LianJiaSaveData/save_html_data_xiaoqu/')

def parse_html_xiaoqu(html):
    import pandas as pd
    from lxml import etree
    
    #使用lxml库的xpath方法对页面进行解析
    link=etree.HTML(html,parser=etree.HTMLParser(encoding='utf-8'))
        
    #1、提取房源总价
    xiaoquName=link.xpath('//div[@class="info"]/div[@class="title"]')
    xqn=[]
    for a in xiaoquName:
        x=a.xpath('.//text()')[1]
        xqn.append(x)
    
    #2、提取房源链接
    href=link.xpath('//div[@class="info"]/div[@class="title"]/a/@href')
    
    #3、提取房源信息
    houseInfo=link.xpath('//div[@class="houseInfo"]')   
    deal=[]
    rent=[]
    for a in houseInfo:
        deal.append(a.xpath('.//text()')[2])
        rent.append(a.xpath('.//text()')[5])
    
    #4、提取房源位置信息
    positionInfo=link.xpath('//div[@class="positionInfo"]')
    daquyu=[]
    xiaoquyu=[]
    builtyear=[]
    for a in positionInfo:
        daquyu.append(a.xpath('.//text()')[2])
        xiaoquyu.append(a.xpath('.//text()')[4])
        builtyear.append(a.xpath('.//text()')[5])
    
    #5、小区二手挂牌均价
    totalPrice=link.xpath('//div[@class="totalPrice"]/span/text()')
    
    #6、小区在售二手房套数
    houseNum=link.xpath('//div[@class="xiaoquListItemSellCount"]/a/span/text()')
    
    
    #创建数据表
    xiaoqu=pd.DataFrame({'xiaoqu':xqn,'lianjie':href,'chengjiao':deal,'chuzu':rent,
                         'daquyu':daquyu,'xiaoquyu':xiaoquyu,'jiancheng':builtyear,
                        'junjia':totalPrice,'fangyuanshu':houseNum}) 

    return xiaoqu
    
def get_latitude(xiaoqu_link_list,headers):
    import requests
    from lxml import etree
    import re
    import random
    import time
    import pandas as pd
    
    latitude=[]
    len_list=len(xiaoqu_link_list)
    for i in range(0,len_list):
        print(i,end=',')
            
        url=xiaoqu_link_list[i]
        
        r=requests.get(url,headers)
        html=r.content
        link=etree.HTML(html,parser=etree.HTMLParser(encoding='utf-8'))
        a=link.xpath('//script[@type="text/javascript"]/text()')
        b=str(a[1])
        resblockPosition=re.findall(r"resblockPosition:\'(.*)\'",b)
        latitude.append(resblockPosition)
        
        time_interval = random.uniform(1,4) 
        time.sleep(time_interval) 
    
    result=pd.DataFrame({'lianjie':xiaoqu_link_list,'jingweidu':latitude})
    
    return result
 