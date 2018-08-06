# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 21:09:57 2018

@author: Annie
"""

#获取各小区的经纬度，绘制房价地图

#1.获取各小区的经纬度

import urllib
import json

url = 'http://api.map.baidu.com/geocoder/v2/'
ak = '&ak=C3KyxnzaNma4dXtTXZRSII10gu2Egq9W' # 调用百度地图API的密钥，个人可自由申请
city_name = '上海'
city_name = urllib.parse.quote(city_name) # 编码url链接中的中文部分
city = '&city=%s'%(city_name)
output = '&output=json&pois=0'

lng = []
lat = []

for i in range(0, df_2.shape[0]):
	area_name = df_2.loc[i,”area_name”]
	area_name = urllib.parse.quote(area_name)
	address = 'address=%s'%(area_name)

	url = 'http://api.map.baidu.com/geocoder/v2/' # url初始化
	url = url + '?'+ address + city + output + ak
	temp = urllib.request.urlopen(url)
	hjson = json.loads(temp.read())
	try:
		lng.append(hjson[“result”][“location”][“lng”])
		lat.append(hjson[“result”][“location”][“lat”])
	except:
		lng.append(None)
		lat.append(None)

df_lng = pd.DataFrame(lng, columns=[['lng']])
df_lat = pd.DataFrame(lat, columns=[['lat']])
df_2 = pd.concat([df_2, df_lng，df_lat], axis=1) # 将获得的经纬度信息更新到原始数据中
df_loc = df_2[['area_name', 'price', 'lng', 'lat']].drop_duplicates() # 去重+去除空值

if df_loc.isnull().values.any():
	df_loc = df_loc.dropna()
	df_loc_group = df_loc.groupby(['area_name','lng', 'lat'], as_index=False)['price'].mean()
	df_loc_group.to_csv('.\location.csv', index=False)


#2.绘制房价地图

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib import cm

%matplotlib inline

map = Basemap(projection='stere',lat_0=31,lon_0=121,
	llcrnrlat=30,urcrnrlat=32,
	llcrnrlon=120,urcrnrlon=122,
	rsphere=6371200.,resolution='h',area_thresh=10)
map.drawmapboundary() # 绘制边界
map.drawstates() # 绘制州
map.drawcoastlines() # 绘制海岸线
map.drawcountries() # 绘制国家
map.drawcounties() # 绘制县

parallels = np.arange(30.,32.,.5)
map.drawparallels(parallels,labels=[1,0,0,0],fontsize=10) # 绘制纬线
meridians = np.arange(120.,122.,.5)
map.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10) # 绘制经线
lat = df_loc_group[“lat”] # 获取纬度值
lon = df_loc_group[“lng”] # 获取经度值
price = df_loc_group[“price”] # 获取平均房价
cm = plt.cm.get_cmap('Reds')
z = (price - price.min())/(price.max() - price.min()) # 绘制散点图时散点颜色深浅表示均价高低，颜色越深价格越高

lon = np.array(lon)
lat = np.array(lat)
x,y = map(lon, lat)
sc = map.scatter(x,y,marker=',',c=z,s=0.1,cmap=cm)

plt.colorbar(sc) # 绘制颜色标尺
plt.title('上海房价分布图')
plt.savefig('.\homeprice_distibution_2.png', dpi=300, bbox_inches='tight')
plt.show()