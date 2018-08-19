# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 19:55:21 2018

@author: Annie
"""

#从已爬取下来的html文件中获取需要的房源信息
from lxml import etree
import pandas as pd


#提取需要的信息
#北京的数据格式不同，单独处理

def parse_html(html):
    #使用lxml库的xpath方法对页面进行解析
    link=etree.HTML(html,parser=etree.HTMLParser(encoding='utf-8'))
        
    #1、提取房源总价
    price=link.xpath('//div[@class="priceInfo"]')  
    tp=[]
    for a in price:
        totalPrice=a.xpath('.//span/text()')[0]
        tp.append(float(totalPrice))

    #2、提取房源信息
    #20180815:北京的houseInfo格式与其他不同，单独处理
    #上海的格式为'共富二村 | 2室2厅 | 81.01平米 | 南 | 精装 | 无电梯'(整体)
    #北京的格式为‘流星花园三区 /4室2厅/118.32平米/南 西 北/精装/有电梯’（5-6部分）
    houseInfo=link.xpath('//div[@class="houseInfo"]')   
    hi=[]
    for b in houseInfo:
        h=b.xpath('.//text()')
        house=h[0]
        for j in list(range(2,len(h),2)):
            house=house+'|'+h[j]
        hi.append(house)         
       
    #3、提取房源关注度
    followInfo=link.xpath('//div[@class="followInfo"]')    
    fi=[]
    for c in followInfo:
        follow=c.xpath('./text()')[0]+'/'+c.xpath('./text()')[1]
        fi.append(follow)   
      
    #4、提取房源位置信息
    positionInfo=link.xpath('//div[@class="positionInfo"]')
    pi=[]
    for d in positionInfo:
        if len(d.xpath('.//text()'))==5:
            position=d.xpath('.//text()')[0]+'/'+d.xpath('.//text()')[2]+'/'+d.xpath('.//text()')[4]
        elif len(d.xpath('.//text()'))==4:
            position=''+'/'+d.xpath('.//text()')[1]+'/'+d.xpath('.//text()')[3]
                    
        pi.append(position)
        
    #5、提取房源ID和名称信息
    #housecode=link.xpath('//div[@class="info clear"]/div[@class="title"]/a/@data-housecode')
    housecode=link.xpath('//div[@class="priceInfo"]/div[@class="unitPrice"]/@data-hid')
    housename=link.xpath('//div[@class="info clear"]/div[@class="title"]/a/text()')
    
    #创建数据表
    house=pd.DataFrame({'id':housecode,'totalprice':tp,'houseinfo':hi,'followinfo':fi,'positioninfo':pi,
                        'housename':housename}) #,index=np.array(housecode)
    #查看数据表的内容
    #house.head()
    #house.to_csv("house_notsplit.csv")
    
    return house


#信息分列
def split_data(house):
    #house=pd.DataFrame({'totalprice':tp,'houseinfo':hi,'followinfo':fi,'positioninfo':pi,
    #                    'housename':housename},index=housecode)
    #1、对房源信息进行分列
    #一般是6列，但独栋别墅是7列，多出第二列“独栋别墅”
    houseinfo_replace=house.houseinfo.copy()
    for x in range(len(houseinfo_replace)):
        houseinfo_replace[x]=houseinfo_replace[x].replace('|独栋', '独栋') #别墅会多出一列，单独处理
        houseinfo_replace[x]=houseinfo_replace[x].replace('|联排', '联排')
        houseinfo_replace[x]=houseinfo_replace[x].replace('|双拼', '双拼')
        houseinfo_replace[x]=houseinfo_replace[x].replace('|叠拼', '叠拼')
        houseinfo_replace[x]=houseinfo_replace[x].replace('|暂无数据别墅', '')
  
    try:    
        houseinfo_split = pd.DataFrame((x.split('|') for x in houseinfo_replace),
                                   columns=['xiaoqu','huxing','mianji',
                                            'chaoxiang','zhuangxiu','dianti'])
    except:
        houseinfo_split = pd.DataFrame((x.split('|') for x in houseinfo_replace),
                                   columns=['xiaoqu','huxing','mianji',
                                            'chaoxiang','zhuangxiu']) 
        houseinfo_split['dianti']=None
    
    #2、对房源关注度进行分列
    followinfo_split = pd.DataFrame((x.split('/') for x in house.followinfo),
                                    columns=['guanzhu','daikan'])  
    
    
    #3、对房源位置信息进行分列
    positioninfo_split=pd.DataFrame((x.split('/') for x in house.positioninfo),
                                    columns=['louceng','nianfen','quyu']) 
    positioninfo_split['louceng']=positioninfo_split['louceng']+positioninfo_split['nianfen']
    del positioninfo_split['nianfen']
    
    #将分列后的关注度信息拼接回原数据表
    house_split=pd.concat([house,houseinfo_split,followinfo_split,positioninfo_split],axis=1)
    
    #然后再删除原先的列
    house_split=house_split.drop(['houseinfo','followinfo','positioninfo'],axis=1)
    
    house_split1=house_split.copy()
    #去除字符串的头尾空格
    for j in range(0,house_split1.columns.size):
        try:
            colname=house_split1.columns[j]
            house_split1.loc[house_split1.loc[:,colname].isnull()==False,colname]=\
            house_split1.loc[house_split1.loc[:,colname].isnull()==False,colname].map(str.strip)
        except:
            pass
    
    house_split1['mianji']=house_split1['mianji'].str[:-2].astype(float)
    house_split1['guanzhu']=house_split1['guanzhu'].str[:-3].astype(int)
    house_split1['price']=house_split1['totalprice']/house_split1['mianji']
    
    print("共采集"+str(len(house))+"条房源信息")        
    return house_split1



#链家只能显示100页的数据，每页30个，不分区域最多只能爬取3000个数据
#房源数据有几万个，必须分区域爬取，且按浦东这种大区域也会超出3000个数据，所以必须分小区域

#获取小区域列表
#(quyu_list,quyu_link_list)=get_small_quyu_link(city,headers)
city=input("请输入城市拼音首字母（如：上海'sh'北京'bj'深圳'sz'广州'gz'杭州'hz'）：")
datestr=input('请输入需要处理的日期：')
save_folder_path='../LianJiaSaveData/save_html_data/'

df=pd.read_csv('链家二手房小区域列表'+city+'.csv',engine='python')
quyu_link_list=df['ershoufanglianjie']
quyu_list=df['xiaoquyu']

#解析数据，并保存在子文件夹save_house_data中
for i in range(0,len(quyu_link_list)):
    print(str(i+1)+'/'+str(len(quyu_link_list)))
    quyu=quyu_list[i]
    filename=save_folder_path+datestr+'_'+city+'/html_'+quyu+'.txt'
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

#变量数量化
#house_result=all_house_split1.copy()
#house_result['mianji']=house_result['mianji'].str[1:-3].astype(float)
#house_result['guanzhu']=house_result['guanzhu'].str[:-4].astype(int)
#增加“每平米房价”字段
#house_result['totalprice']=house_result['totalprice'].astype('float64')
#house_result['price']=house_result['totalprice']/house['mianji']
#字符型的字段去掉首尾的空格
#house.loc[:,np.issubdtype(house.iloc[0,:],np.object_)].map(str.strip)

filename='../LianJiaSaveData/save_house_data/house_'+city+'_'+datestr+'.csv'
all_house_split1.to_csv(filename,encoding = "utf_8_sig")

