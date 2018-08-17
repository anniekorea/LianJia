# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 16:02:32 2018

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 19:55:21 2018

@author: Annie
"""

import requests
import time
import random
from lxml import etree
import pandas as pd
import os
import datetime

#爬取区域的链接：文字text，链接href，拼音pinyin
def get_quyu_list(url,region_big_small,headers):
    if region_big_small=='big':
        i=1
    elif region_big_small=='small':
        i=2
    else:
        print("Please input 'big' or 'small'.")
    r=requests.get(url,headers)
    html=r.content
    link=etree.HTML(html,parser=etree.HTMLParser(encoding='utf-8'))
    text=link.xpath('//div[@data-role="ershoufang"]/div[%d]/a/text()'%i)
    href=link.xpath('//div[@data-role="ershoufang"]/div[%d]/a/@href'%i)
    quyu=pd.DataFrame({'text':text,'href':href})
    href_split=pd.DataFrame(x.split('/') for x in quyu.href)
    quyu['pinyin']=href_split[2]
    if i==1:
        quyu.href=pd.DataFrame(url+x+'/' for x in quyu.pinyin)
    if i==2:
        url=url[:-(len(url.split('/')[-2])+1)] #作用是删掉'大区域/'，因为小区域的链接是ershoufang/小区域，而不是ershoufang/大区域/小区域
        quyu.href=pd.DataFrame(url+x+'/' for x in quyu.pinyin)
    return quyu


#获取小区域的链接
def get_small_quyu_link(city,headers):
    url='https://'+city+'.lianjia.com/ershoufang/'
    try:
        #小区域数据来源一：直接从文件读取小区域的链接
        df=pd.read_csv('链家二手房小区域列表'+city+'.csv',engine='python')
        quyu_link_list=df['ershoufanglianjie']
        quyu_list=df['xiaoquyu']
        print('查询到“链家二手房小区域列表.csv”，直接导入...')
        #quyu_list.head()
    except:
        ##小区域数据来源二：从网站上爬取
        print('未查询到“链家二手房小区域列表.csv”，爬取并保存...')
        big_quyu_list=get_quyu_list(url,'big',headers)
        for i in range(0,len(big_quyu_list)):
            href=big_quyu_list.href[i]
            try:
                xiaoquyu=get_quyu_list(href,'small',headers)
                if i==0:
                    df=xiaoquyu
                else:
                    df=pd.concat([df,xiaoquyu],ignore_index=True)
            except:
                print(href+'有问题，已忽略！')
                pass
        quyu_link_list=df['href']
        quyu_list=df['pinyin']
        df.rename(columns={'href':'ershoufanglianjie', 'pinyin':'xiaoquyu'}, inplace = True)
        df.to_csv('链家二手房小区域列表'+city+'.csv')
    return(quyu_list,quyu_link_list)

#获取页码，用于构造分页的链接
def get_page_num(url,headers):
    import json
    r=requests.get(url,headers)
    html=r.content
    link=etree.HTML(html,parser=etree.HTMLParser(encoding='utf-8'))
    page=link.xpath('//div[@class="contentBottom clear"] \
                    /div[@class="page-box fr"] \
                    /div[@class="page-box house-lst-page-box"] \
                    /@page-data')
    if len(page)==0:
        page=0
        return page
    else:
        page=page[0]#获取页码所在字符串
        page_dic=json.loads(page)
        totalPage=page_dic.get("totalPage")
        return totalPage

#循环抓取列表页信息
def get_html(url,totalPage,headers):
    #totalPage=get_page_num(url)
    for i in range(1,totalPage+1):
        if i<totalPage:
            print(i,end=',')
        else:
            print(i)
        
        if i == 1:
            i=str(i)
            a=(url+'pg'+i+'/')
            r=requests.get(a,headers)
            html=r.content
        else:
            i=str(i)
            a=(url+'pg'+i+'/')
            r=requests.get(a,headers)
            html2=r.content
            html = html + html2
        #为了避免被反爬，设置间隔时间，经测试，设成1-2秒比较合适，再短可能就会中断
        time_interval = random.uniform(1,2) 
        time.sleep(time_interval)  
    return html

#保存html
def save_html(html,datestr,city,quyu,save_folder_path='../LianJiaSaveData/save_html_data/'):    
    if isinstance(html,str):
        html_str=html
    else:
        html_str=html.decode("utf-8")
    path=save_folder_path+datestr+'_'+city
    folder = os.path.exists(path)
    if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)

    filename=path+'/html_'+quyu+'.txt' #+datetime.datetime.now().strftime('%Y%m%d%H%M')
    
    fh = open(filename, 'w', encoding='utf-8')
    fh.write(html_str)
    fh.close()


#链家只能显示100页的数据，每页30个，不分区域最多只能爬取3000个数据
#房源数据有几万个，必须分区域爬取，且按浦东这种大区域也会超出3000个数据，所以必须分小区域

#设置参数
city=input("请输入城市拼音首字母（如：上海'sh'北京'bj'深圳'sz'广州'gz'杭州'hz'）：")
url_base='https://'+city+'.lianjia.com/ershoufang/'
save_folder_path='../LianJiaSaveData/save_html_data/'

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
(quyu_list,quyu_link_list)=get_small_quyu_link(city,headers)

datestr=datetime.datetime.now().strftime('%Y%m%d')

#爬数据，并保存在子文件夹save_html_data中，每个日期一个文件夹，同一天的数据放在以日期命名的子文件夹中
for i in range(0,len(quyu_link_list)):
    url=quyu_link_list[i]
    quyu=quyu_list[i]
    filename=save_folder_path+datestr+'_'+city+'/html_'+quyu+'.txt'
    if os.path.exists(filename):
        print(str(i)+'/'+str(len(quyu_link_list))+','+quyu+',文件已存在，跳过')
        pass
    else:
        totalPage=get_page_num(url,headers)
        print(str(i)+'/'+str(len(quyu_link_list))+','+quyu+',共'+str(totalPage)+'页')
        if totalPage==0:
            html=''
        else:
            html=get_html(url,totalPage,headers)
        save_html(html,datestr,city,quyu,save_folder_path)

