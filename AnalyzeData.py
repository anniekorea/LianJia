# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 20:16:43 2018

@author: Annie
"""

import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt
house=pd.read_csv('./save_house_data/house_20180805.csv',sep=',')
house.head()

#房价最高的10套二手房
house.sort_values('totalprice',ascending=False).head(10)

#房价最低的10套二手房
house.sort_values('totalprice').head(10)

#二手房源最多的10个小区
house['xiaoqu'].value_counts().head(10)

#出现最多的5种户型
house['huxing'].value_counts().head(5)

#本文变量数量化
house['mianji']=house['mianji'].str[1:-3].astype(float)
house['guanzhu']=house['guanzhu'].str[:-4].astype(int)

#面积最小的二手房
house.sort_values('mianji').iloc[0,:]

#面积最大的二手房
house.sort_values('mianji',ascending=False).iloc[0,:]

#关注人数最多的10套二手房
house.sort_values('guanzhu',ascending=False).head(10)

#增加“每平米房价”字段
house['price']=house['totalprice']/house['mianji']
print('上海市二手房平均面积为%f平方米'%house['mianji'].mean())
print('上海市二手房平均总价为%f万元'%house['totalprice'].mean())
print('上海市二手房平均价格为%f万元每平米'%house['price'].mean())

#按照面积分组
#%matplotlib inline
house_filter=house[house['mianji']<=350] #大部分面积在350平米以下，小部分太大的面积会影响作图的分布效果
house_filter.mianji.hist(bins=35)
plt.title("Distribution of area of house")
plt.ylabel('count of house')
plt.xlabel('area')
#labels = ['1-50', '51-100', '101-150', '151-200', '201-250', '251-300','301-350']
# 面积分组的labels
bins = range(0, 351, 10) # [0, 50, 100, 150, 200, 250, 300, 350]
# 告诉我们bin是哪些
house['mianji_group'] = pd.cut(house.mianji, bins, right=False)
# 按照bin把数据cut下来，并附上labels，做成一个新的column，保存下来。


#最普遍的二手房面积
house['mianji_group'].value_counts().head(5)
print('占比是%f%%'%(100.0*house['mianji_group'].value_counts().head(5).sum()/len(house)))


#不同小区的房价差异
xiaoqu_50=house.groupby('xiaoqu').size().sort_values(ascending=False)[:50]
house_in50xiaoqu=house[house['xiaoqu'].isin(list(xiaoqu_50.index))]
#按平均总价排序：
house_in50xiaoqu.groupby('xiaoqu').mean()['totalprice'].sort_values().head(10)
#按每平米均价排序：
house_in50xiaoqu.groupby('xiaoqu').mean()['price'].sort_values().head(10)



#不同小区各户型的数量
house_in50xiaoqu_huxingshu=house_in50xiaoqu.groupby('xiaoqu')['huxing'].value_counts()
house_in50xiaoqu_huxingshu.head(10)

house_in50xiaoqu_huxingshu=house_in50xiaoqu_huxingshu.unstack(fill_value=0)
house_in50xiaoqu_huxingshu.head()


#不同小区最多的户型
house_in50xiaoqu_huxing=house_in50xiaoqu_huxingshu.apply(lambda x:x[x==x.max()],axis=1)
house_in50xiaoqu_huxing.head()

house_in50xiaoqu_huxing=house_in50xiaoqu_huxing.fillna(0)
house_in50xiaoqu_huxing.shape
for i in range(house_in50xiaoqu_huxing.shape[0]):
    for j in range(house_in50xiaoqu_huxing.shape[1]):
        if house_in50xiaoqu_huxing.iloc[i,j]!=0:
            print('%s:%s'%(house_in50xiaoqu_huxing.index[i],house_in50xiaoqu_huxing.columns[j]))


#对不同户型的关注度差异
house.groupby('huxing').sum()['guanzhu'].sort_values(ascending=False)


#对不同总价的关注度差异
#首先将房价分组
print(house['totalprice'].min())
print(house['totalprice'].max())

#labels = ['1-50', '51-100', '101-150', '151-200', '201-250', '251-300','301-350']
# 总价分组的labels
bins = range(100, 1500, 50)
# [0, 50, 100, 150, 200, 250, 300, 350]
# 告诉我们bin是哪些
house['totalprice_group'] = pd.cut(house.totalprice, bins, right=False)
# 按照bin把数据cut下来，并附上labels，做成一个新的column，保存下来。
totalprice_guanzhu=house.groupby('totalprice_group').sum()['guanzhu'].sort_values(ascending=False)
totalprice_guanzhu.head()

house_filter=house[house['totalprice']<1000]
house_filter.totalprice.hist(bins=len(totalprice_guanzhu))
print(len(totalprice_guanzhu))
















