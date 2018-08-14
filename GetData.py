# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 19:55:21 2018

@author: Annie
"""

import requests
import time
import random
import datetime
from lxml import etree
import pandas as pd
import os

#url='https://sh.lianjia.com/ershoufang/beicai/'
def get_page_num(url):#此函数用于获取页码，用于构造分页的链接
    import json
    r=requests.get(url,headers=headers)
    html=r.content
    lj=etree.HTML(html,parser=etree.HTMLParser(encoding='utf-8'))
    page=lj.xpath('//div[@class="contentBottom clear"] \
                    /div[@class="page-box fr"] \
                    /div[@class="page-box house-lst-page-box"] \
                    /@page-data')
    if len(page)==0:
        page=0
        return page
    else:
        page=page[0]#获取页码所在字符串
        page_dic=json.loads(page)
        return page_dic.get("totalPage")
    

#循环抓取列表页信息
def get_html(url,totalPage):
    #totalPage=get_page_num(url)
    for i in range(1,totalPage+1):
        print(i)
        if i == 1:
            i=str(i)
            a=(url+page+i+'/')
            r=requests.get(url=a,headers=headers)
            html=r.content
        else:
            i=str(i)
            a=(url+page+i+'/')
            r=requests.get(url=a,headers=headers)
            html2=r.content
            html = html + html2
        #每次间隔x秒
        time_interval = random.uniform(1,3) 
        time.sleep(time_interval)  
    return html

def save_html(html,datestr,quyu=''):
    #保存html
    if isinstance(html,str):
        html_str=html
    else:
        html_str=html.decode("utf-8")
    path='../LianJiaSaveData/save_html_data/'+datestr
    folder = os.path.exists(path)
    if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)

    filename=path+'/html_'+quyu+'.txt' #+datetime.datetime.now().strftime('%Y%m%d%H%M')
    
    fh = open(filename, 'w', encoding='utf-8')
    fh.write(html_str)
    fh.close()


################提 取 需 要 的 信 息#######################
def parse_html(html):
    #使用lxml库的xpath方法对页面进行解析
    lj=etree.HTML(html,parser=etree.HTMLParser(encoding='utf-8'))
        
    #1、提取房源总价
    price=lj.xpath('//div[@class="priceInfo"]')  
    tp=[]
    for a in price:
        totalPrice=a.xpath('.//span/text()')[0]
        tp.append(totalPrice)   
    #抽取打印前10条房源总价信息：
    #for p in tp[:10]:
    #    print(p)
        
    #2、提取房源信息
    houseInfo=lj.xpath('//div[@class="houseInfo"]')   
    hi=[]
    for b in houseInfo:
        house=b.xpath('.//text()')[0]+b.xpath('.//text()')[1]
        hi.append(house)    
    #抽取打印前10条房屋信息：
    #for i in hi[:10]:
    #    print(i)
        
    #3、提取房源关注度
    followInfo=lj.xpath('//div[@class="followInfo"]')    
    fi=[]
    for c in followInfo:
        follow=c.xpath('./text()')[0]
        fi.append(follow)   
    #抽取打印前10条房屋信息：
    #for i in fi[:10]:
    #    print(i)    
    
    #4、提取房源位置信息
    positionInfo=lj.xpath('//div[@class="positionInfo"]')
    pi=[]
    for d in positionInfo:
        position=d.xpath('.//text()')[0]+d.xpath('.//text()')[1]
        pi.append(position)
        
    #5、提取房源ID和名称信息
    #housecode=lj.xpath('//div[@class="info clear"]/div[@class="title"]/a/@data-housecode')
    housecode=lj.xpath('//div[@class="priceInfo"]/div[@class="unitPrice"]/@data-hid')
    housename=lj.xpath('//div[@class="info clear"]/div[@class="title"]/a/text()')
    
    #import pandas as pd
    #创建数据表
    house=pd.DataFrame({'id':housecode,'totalprice':tp,'houseinfo':hi,'followinfo':fi,'positioninfo':pi,
                        'housename':housename}) #,index=np.array(housecode)
    #查看数据表的内容
    #house.head()
    #house.to_csv("house_notsplit.csv")
    
    return house


################信 息 分 列#######################
def split_data(house):
    #house=pd.DataFrame({'totalprice':tp,'houseinfo':hi,'followinfo':fi,'positioninfo':pi,
    #                    'housename':housename},index=housecode)
    #1、对房源信息进行分列
    #一般是6列，但独栋别墅是7列，多出第二列“独栋别墅”
    houseinfo_replace=house.houseinfo
    for x in range(len(houseinfo_replace)):
        houseinfo_replace[x]=houseinfo_replace[x].replace('| 独栋', '独栋')
        houseinfo_replace[x]=houseinfo_replace[x].replace('| 联排', '联排')
        houseinfo_replace[x]=houseinfo_replace[x].replace('| 双拼', '双拼')
        houseinfo_replace[x]=houseinfo_replace[x].replace('| 叠拼', '叠拼')
        houseinfo_replace[x]=houseinfo_replace[x].replace('| 暂无数据别墅', '')
    
    try:    
        houseinfo_split = pd.DataFrame((x.split('|') for x in houseinfo_replace),
                                   columns=['xiaoqu','huxing','mianji',
                                            'chaoxiang','zhuangxiu','dianti']) #index=house.index,
    #houseinfo_split.head()
    except:
        houseinfo_split = pd.DataFrame((x.split('|') for x in houseinfo_replace),
                                   columns=['xiaoqu','huxing','mianji',
                                            'chaoxiang','zhuangxiu']) #index=house.index,
        houseinfo_split['dianti']=None
    finally:    
        #2、对房源关注度进行分列
        followinfo_split = pd.DataFrame((x.split('/') for x in house.followinfo),
                                        columns=['guanzhu','daikan','fabu'])  #,index=house.index
        
    
        
        #3、对房源位置信息进行分列
        positioninfo_split=pd.DataFrame((x.split('-') for x in house.positioninfo),
                                        columns=['louceng','quyu']) #index=house.index,
        positioninfo_split['louceng']=positioninfo_split['louceng'].map(str.strip)
        positioninfo_split['quyu']=positioninfo_split['quyu'].map(str.strip)
        
        #将分列后的关注度信息拼接回原数据表
        house_split=pd.concat([house,houseinfo_split,followinfo_split,positioninfo_split],axis=1)
        #house.head()
        
        #然后再删除原先的列
        house_split=house_split.drop(['houseinfo','followinfo','positioninfo'],axis=1)
        print("共采集"+str(len(house))+"条房源信息")
        #house.head()
  
        return house_split

#爬取区域的链接：文字text，链接href，拼音pinyin
def get_quyu_list(url='https://sh.lianjia.com/ershoufang/pudong/',quyudaxiao='xiao'):
    if quyudaxiao=='xiao':
        i=2
    elif quyudaxiao=='da':
        i=1
    else:
        print('Please input da or xiao.')
    r=requests.get(url,headers=headers)
    html=r.content
    lj=etree.HTML(html,parser=etree.HTMLParser(encoding='utf-8'))
    text=lj.xpath('//div[@data-role="ershoufang"]/div[%d]/a/text()'%i)
    href=lj.xpath('//div[@data-role="ershoufang"]/div[%d]/a/@href'%i)
    quyu=pd.DataFrame({'text':text,'href':href})
    href_split=pd.DataFrame(x.split('/') for x in quyu.href)
    quyu['pinyin']=href_split[2]
    quyu.href=pd.DataFrame(url+x+'/' for x in quyu.pinyin)
    return quyu


#获取小区域的链接
def get_xiaoquyu_lianjie(url='https://sh.lianjia.com/ershoufang/'):
    try:
        #小区域数据来源一：直接从文件读取小区域的链接
        df=pd.read_csv('链家二手房小区域列表.csv',engine='python')
        QuyuLianjie=df['ershoufanglianjie']
        Quyu=df['xiaoquyu']
        print('查询到“链家二手房小区域列表.csv”，直接导入...')
        #Quyu.head()
    except:
        ##小区域数据来源二：从网站上爬取
        print('未查询到“链家二手房小区域列表.csv”，爬取并保存...')
        daquyu=get_quyu_list(url,quyudaxiao='da')
        for i in range(0,len(daquyu)):
            href=daquyu.href[i]
            xiaoquyu=get_quyu_list(url=href,quyudaxiao='xiao')
            if i==0:
                df=xiaoquyu
            else:
                df=pd.concat([df,xiaoquyu],ignore_index=True)
        QuyuLianjie=df['href']
        Quyu=df['pinyin']
        df.rename(columns={'href':'ershoufanglianjie', 'pinyin':'xiaoquyu'}, inplace = True)
        df.to_csv('链家二手房小区域列表.csv')
    return(Quyu,QuyuLianjie)




#链家只能显示100页的数据，每页30个，不分区域最多只能爬取3000个数据
#房源数据有几万个，必须分区域爬取，且按浦东这种大区域也会超出3000个数据，所以必须分小区域

#设置列表页URL的固定部分
url='http://hz.lianjia.com/ershoufang/'
#设置页面页的可变部分
page=('pg')

#设置请求头部信息,我们最好在http请求中设置一个头部信息，否则很容易被封ip。
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
'Accept':'text/html;q=0.9,*/*;q=0.8',
'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Accept-Encoding':'gzip',
'Connection':'close',
'Referer':'http://www.baidu.com/link?url=_andhfsjjjKRgEWkj7i9cFmYYGsisrnm2A-TN3XZDQXxvGsM9k9ZZSnikW2Yds4s&amp;amp;wd=&amp;amp;eqid=c3435a7d00146bd600000003582bfd1f'
}
#encoding=requests.get(url,headers=headers).encoding

#获取小区域列表
(Quyu,QuyuLianjie)=get_xiaoquyu_lianjie(url)

datestr=datetime.datetime.now().strftime('%Y%m%d')

#爬数据，并保存在子文件夹save_html_data中，每个日期一个文件夹，同一天的数据放在以日期命名的子文件夹中
for i in range(0,len(QuyuLianjie)):
    url=QuyuLianjie[i]
    quyu=Quyu[i]
    totalPage=get_page_num(url)
    print(str(i)+'/'+str(len(QuyuLianjie))+','+quyu+',共'+str(totalPage)+'页')
    if totalPage==0:
        html=''
    else:
        html=get_html(url,totalPage)
    save_html(html,datestr,quyu=quyu)


#解析数据，并保存在子文件夹save_house_data中
for i in range(0,len(QuyuLianjie)):
    print(str(i+1)+'/'+str(len(QuyuLianjie)))
    quyu=Quyu[i]
    filename='../LianJiaSaveData/save_html_data/'+datestr+'/html_'+quyu+'.txt'
    fh = open(filename, 'r', encoding='utf-8')
    html=fh.read()
    fh.close()
    if len(html)>0:
        house=parse_html(html)
        house_split=split_data(house)
        if i==0:
            all_house_split=house_split
        if i>=1:
            all_house_split=pd.concat([all_house_split,house_split])

all_house_split1 = all_house_split[~all_house_split['id'].duplicated()]
filename='../LianJiaSaveData/save_house_data/house_'+datestr+'.csv'
all_house_split1.to_csv(filename)

