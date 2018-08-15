# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 22:57:50 2018

@author: Annie
"""

#提取需要的信息
def parse_html(html,city):
    #使用lxml库的xpath方法对页面进行解析
    link=etree.HTML(html,parser=etree.HTMLParser(encoding='utf-8'))
        
    #1、提取房源总价
    price=link.xpath('//div[@class="priceInfo"]')  
    tp=[]
    for a in price:
        totalPrice=a.xpath('.//span/text()')[0]
        tp.append(totalPrice)   
    #抽取打印前10条房源总价信息：
    #for p in tp[:10]:
    #    print(p)
        
    #2、提取房源信息
    #20180815:北京的houseInfo格式与其他不同，单独处理
    #上海的格式为'共富二村 | 2室2厅 | 81.01平米 | 南 | 精装 | 无电梯'(整体)
    #北京的格式为‘流星花园三区 /4室2厅/118.32平米/南 西 北/精装/有电梯’（5-6部分）

    houseInfo=link.xpath('//div[@class="houseInfo"]')   
    hi=[]
    if city=='bj':
        for b in houseInfo:
            h=b.xpath('.//text()')
            house=h[0]
            for j in list(range(2,len(h),2)):
                house=house+'|'+h[j]
            hi.append(house)      
    else:
        for b in houseInfo:
            house=b.xpath('.//text()')[0]+b.xpath('.//text()')[1]
            hi.append(house)    
    #抽取打印前10条房屋信息：
    #for i in hi[:10]:
    #    print(i)
        
    #3、提取房源关注度
    followInfo=link.xpath('//div[@class="followInfo"]')    
    fi=[]
    for c in followInfo:
        follow=c.xpath('./text()')[0]
        fi.append(follow)   
    #抽取打印前10条房屋信息：
    #for i in fi[:10]:
    #    print(i)    
    
    #4、提取房源位置信息
    #20180815:北京的positionInfo格式与其他不同，单独处理
    #上海的格式为'中楼层(共6层)2005年建板楼 - 共富'
    #北京的格式为‘高楼层(共6层)/2003年建板楼/回龙观’
    positionInfo=link.xpath('//div[@class="positionInfo"]')
    pi=[]
    if city=='bj':
        for d in positionInfo:
            position=d.xpath('.//text()')[0]+d.xpath('.//text()')[2]+'-'+d.xpath('.//text()')[4]
            pi.append(position)        
    else:
        for d in positionInfo:
            position=d.xpath('.//text()')[0]+d.xpath('.//text()')[1]
            pi.append(position)
        
    #5、提取房源ID和名称信息
    #housecode=link.xpath('//div[@class="info clear"]/div[@class="title"]/a/@data-housecode')
    housecode=link.xpath('//div[@class="priceInfo"]/div[@class="unitPrice"]/@data-hid')
    housename=link.xpath('//div[@class="info clear"]/div[@class="title"]/a/text()')
    
    #import pandas as pd
    #创建数据表
    house=pd.DataFrame({'id':housecode,'totalprice':tp,'houseinfo':hi,'followinfo':fi,'positioninfo':pi,
                        'housename':housename}) #,index=np.array(housecode)
    #查看数据表的内容
    #house.head()
    #house.to_csv("house_notsplit.csv")
    
    return house