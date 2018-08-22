# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 09:29:37 2018

@author: Administrator
"""
#其他经纬度转换为高德经纬度
#链家用的是baidu的经纬度，要消除偏移，必须先转换成高德的经纬度
def transform(location):
    import requests
    parameters = {'coordsys':'baidu','locations': location, 'key': 'f30c9d52b003c2b3ac089e2672e18baf'}
    base = 'http://restapi.amap.com/v3/assistant/coordinate/convert'
    response = requests.get(base, parameters)
    answer = response.json()
    return answer['locations']

#逆地理编码:通过经纬度获取地址
def regeocode(location):
    import requests
    parameters = {'location': location, 'key': '7ec25a9c6716bb26f0d25e9fdfa012b8'}
    base = 'http://restapi.amap.com/v3/geocode/regeo'
    response = requests.get(base, parameters)
    answer = response.json()
    return answer['regeocode']['addressComponent']['district'],answer['regeocode']['formatted_address']

#地理编码:地址获取经纬度                    
def geocode(address,city):
    import requests
    parameters = {'key': '7ec25a9c6716bb26f0d25e9fdfa012b8','address': address, 'city':city}
    base = 'http://restapi.amap.com/v3/geocode/geo'
    response = requests.get(base, parameters)
    answer = response.json()
    result={'location':answer['geocodes'][0]['location'],'address':answer['geocodes'][0]['formatted_address']}
    return result

#公交路线规划，获得两地点间距离和时间
def direction(origion,destination,city):
    import requests
    parameters = {'key': '7ec25a9c6716bb26f0d25e9fdfa012b8','origin': origion,'destination':destination,'city':city}
    base = 'https://restapi.amap.com/v3/direction/transit/integrated'
    response = requests.get(base, parameters)
    answer = response.json()
    result={'distance':int(answer['route']['distance'])/1000,'duration':int(int(answer['route']['transits'][0]['duration'])/60)}
    return result


x=transform('121.530817,31.224111')
y=regeocode('121.530817,31.224111')
home=geocode('竹园新村','上海')
company1=geocode('国投大厦','上海')
company2=geocode('环球金融中心','上海')

a=direction(home['location'],company1['location'],'上海')
b=direction(home['location'],company2['location'],'上海')


#<---获取静态高德地图--->
def getStaticAmap(str_city_center):      
    import webbrowser
    # sh = '121.472644,31.231706'  # 上海中心点
    #高德地图-->静态地图API地址
    url = r'http://restapi.amap.com/v3/staticmap?location=%s&zoom=10&size=1024*768&key=7ec25a9c6716bb26f0d25e9fdfa012b8'
    url_1 = url % str_city_center                                       #加入城市
    #url_amap=url_1+'&markers=mid,0xFF0000,A:'+lonlat_str            #增加marker点
    url_amap=url_1
    print(url_amap)                                                     #
    webbrowser.open(url_amap)                                          #打开