# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 20:16:43 2018

@author: Annie
"""

import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt
#import matplotlib
import csv

def save_analyze_result(fh,result_txt,result):
    fh.write(result_txt)
    if isinstance(result,pd.core.series.Series):
        result=result.to_frame()
    result.insert(0,'index',result.index)
    writer = csv.writer(fh)#,dialect='excel')
    writer.writerow(result.columns)
    writer.writerows(result.values)
    #for i in range(0,len(result)):
    #    writer.writerow(result.iloc[i].values)
    fh.write('\r\n')
    #fh.close()
    
    
datestr=input('请输入需要分析的日期：')
datafilename='house_'+datestr

filename='./AnalyzeResult/AnalyzeData.txt'
fh = open(filename, 'a', encoding='utf-8',newline='')

house=pd.read_csv('../LianJiaSaveData/save_house_data/'+datafilename+'.csv',sep=',',index_col=0)

#本文变量数量化
house['mianji']=house['mianji'].str[1:-3].astype(float)
house['guanzhu']=house['guanzhu'].str[:-4].astype(int)
#增加“每平米房价”字段
house['price']=house['totalprice']/house['mianji']

#汇总信息
fh.write('#####################分析日期：%s，共%d套房源#####################\r\n'%(datestr,len(house)))
         
#房价最高的10套二手房
result_txt='房价最高的10套二手房:\r\n'
result=house.sort_values('totalprice',ascending=False).head(10)
save_analyze_result(fh,result_txt,result)

#房价最低的10套二手房
result_txt='房价最低的10套二手房:\r\n'
result=house.sort_values('totalprice').head(10)
save_analyze_result(fh,result_txt,result)

#二手房源最多的10个小区
result_txt='二手房源最多的10个小区:\r\n'
result=house['xiaoqu'].value_counts().head(10)
save_analyze_result(fh,result_txt,result)

#出现最多的10种户型
result_txt='出现最多的10种户型:\r\n'
result=house['huxing'].value_counts().head(10)
save_analyze_result(fh,result_txt,result)

#画柱状图
fig=plt.figure()
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.bar(result.index,result)
plt.title("户型分布（出现最多的10种）")
plt.ylabel('')
plt.xlabel('area')
fig.savefig('./AnalyzeResult/%s户型分布.jpg'%datestr)


#面积最小的二手房
result_txt='面积最小的二手房:\r\n'
result=house.sort_values('mianji').iloc[0,:]
result=result.to_frame().stack()
result=result.unstack(0)
save_analyze_result(fh,result_txt,result)

#面积最大的二手房
result_txt='面积最大的二手房:\r\n'
result=house.sort_values('mianji',ascending=False).iloc[0,:]
result=result.to_frame().stack()
result=result.unstack(0)
save_analyze_result(fh,result_txt,result)

#关注人数最多的10套二手房
result_txt='关注人数最多的10套二手房:\r\n'
result=house.sort_values('guanzhu',ascending=False).head(10)
save_analyze_result(fh,result_txt,result)

#平均值
fh.write('上海市二手房平均面积为：%.2f平方米'%house['mianji'].mean()+'\r\n')
fh.write('上海市二手房平均总价为：%.2f万元'%house['totalprice'].mean()+'\r\n')
fh.write('上海市二手房平均价格为：%.2f万元每平米'%house['price'].mean()+'\r\n')

#按照面积分组
#%matplotlib inline
#house_filter=house[house['mianji']<=350] #大部分面积在350平米以下，小部分太大的面积会影响作图的分布效果
fig=plt.figure()
house.mianji.hist(range=(0,350),bins=35,rwidth=0.8) 
plt.title("Distribution of area of house")
plt.ylabel('count of house')
plt.xlabel('area')
fig.savefig('./AnalyzeResult/%s面积分布.jpg'%datestr)
#labels = ['1-50', '51-100', '101-150', '151-200', '201-250', '251-300','301-350']
# 面积分组的labels
bins = range(0, 351, 10) # [0, 50, 100, 150, 200, 250, 300, 350]
# 告诉我们bin是哪些
house['mianji_group'] = pd.cut(house.mianji, bins, right=False)
# 按照bin把数据cut下来，并附上labels，做成一个新的column，保存下来。


#最普遍的二手房面积
result_txt='最普遍的二手房面积:\r\n'
result=house['mianji_group'].value_counts().head(5)
result=result.to_frame()
result['percent']=result['mianji_group']/len(house)*100
save_analyze_result(fh,result_txt,result)

#房源数前50的小区的房价差异
xiaoqu_50=house.groupby('xiaoqu').size().sort_values(ascending=False)[:50]
house_in50xiaoqu=house[house['xiaoqu'].isin(list(xiaoqu_50.index))]
#房源数前50的小区，按平均总价排序：
result_txt='房源数前50的小区，按平均总价排序:\r\n'
result=house_in50xiaoqu.groupby('xiaoqu').mean()['totalprice'].sort_values().head(10)
save_analyze_result(fh,result_txt,result)

#房源数前50的小区，按每平米均价排序：
result_txt='房源数前50的小区，按每平米均价排序:\r\n'
result=house_in50xiaoqu.groupby('xiaoqu').mean()['price'].sort_values().head(10)
save_analyze_result(fh,result_txt,result)


#房源数前50的小区，各小区户型的数量
house_in50xiaoqu_huxingshu=house_in50xiaoqu.groupby('xiaoqu')['huxing'].value_counts()
#house_in50xiaoqu_huxingshu.head(10)
result_txt='房源数前50的小区，各小区户型的数量：\r\n'
result=house_in50xiaoqu_huxingshu.unstack(fill_value=0)
save_analyze_result(fh,result_txt,result)

#房源数前50的小区，各小区最多的户型
house_in50xiaoqu_huxingshu=house_in50xiaoqu.groupby('xiaoqu')['huxing'].value_counts()
house_in50xiaoqu_huxingshu=house_in50xiaoqu_huxingshu.unstack(fill_value=0)
house_in50xiaoqu_huxing=house_in50xiaoqu_huxingshu.apply(lambda x:x[x==x.max()],axis=1)
#house_in50xiaoqu_huxing.head()

'''house_in50xiaoqu_huxing=house_in50xiaoqu_huxing.fillna(0)
house_in50xiaoqu_huxing.shape
for i in range(house_in50xiaoqu_huxing.shape[0]):
    for j in range(house_in50xiaoqu_huxing.shape[1]):
        if house_in50xiaoqu_huxing.iloc[i,j]!=0:
            print('%s:%s'%(house_in50xiaoqu_huxing.index[i],house_in50xiaoqu_huxing.columns[j]))
'''
result_txt='房源数前50的小区，各小区最多的户型：\r\n'
result=house_in50xiaoqu_huxing
save_analyze_result(fh,result_txt,result)

#对不同户型的关注度差异
result_txt='对不同户型的关注度差异:\r\n'
result=house.groupby('huxing').sum()['guanzhu'].sort_values(ascending=False)
save_analyze_result(fh,result_txt,result)

#对不同总价的关注度差异
#首先将房价分组
#print(house['totalprice'].min())
#print(house['totalprice'].max())

#labels = ['1-50', '51-100', '101-150', '151-200', '201-250', '251-300','301-350']
# 总价分组的labels
bins = [0]+list(range(100, 2050, 50))+[100000]
# [0, 50, 100, 150, 200, 250, 300, 350]
# 告诉我们bin是哪些
house['totalprice_group'] = pd.cut(house.totalprice, bins, right=False)
# 按照bin把数据cut下来，并附上labels，做成一个新的column，保存下来。
totalprice_guanzhu=house.groupby('totalprice_group').sum()['guanzhu'].sort_values(ascending=False)
#totalprice_guanzhu.head()
result_txt='对不同总价的关注度差异：\r\n'
result=totalprice_guanzhu
save_analyze_result(fh,result_txt,result)

#作图
fig=plt.figure()
house.totalprice.hist(range=(0,1000),bins=len(totalprice_guanzhu),rwidth=0.8) #range指定数据范围，超出范围的数据被忽略
plt.title("Distribution of total price of house")
plt.ylabel('count of house')
plt.xlabel('totalprice')
#fig = ax2.get_figure()
fig.savefig('./AnalyzeResult/%s总价格分布.jpg'%datestr)


fh.close()



