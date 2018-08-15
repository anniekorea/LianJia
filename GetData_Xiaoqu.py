# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 15:36:29 2018

@author: Administrator
"""

#爬取小区的经纬度，画热力图
url='https://'+city+'.lianjia.com/xiaoqu/'
(quyu_list,quyu_link_list)=get_small_quyu_link(city,headers)

datestr=datetime.datetime.now().strftime('%Y%m%d')

#爬数据，并保存在子文件夹save_html_data中，每个日期一个文件夹，同一天的数据放在以日期命名的子文件夹中
for i in range(0,len(quyu_link_list)):
    url=quyu_link_list[i]
    quyu=quyu_list[i]
    totalPage=get_page_num(url,headers)
    print(str(i)+'/'+str(len(quyu_link_list))+','+quyu+',共'+str(totalPage)+'页')
    if totalPage==0:
        html=''
    else:
        html=get_html(url,totalPage,headers)
    save_html(html,datestr,city,quyu)