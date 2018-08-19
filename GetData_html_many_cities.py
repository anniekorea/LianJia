# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 22:52:44 2018

@author: Annie
"""

import GetData_html

cities=['xm','cq']
save_folder_path='../LianJiaSaveData/save_html_data/'
#设置请求头部信息,我们最好在http请求中设置一个头部信息，否则很容易被封ip。
headers={'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
       'Accept-Language': 'zh-CN,zh;q=0.9',
       'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
#encoding=requests.get(url,headers=headers).encoding

for city in cities:
    #设置参数
    url_base='https://'+city+'.lianjia.com/ershoufang/'
    
    #获取小区域列表
    (quyu_list,quyu_link_list)=get_small_quyu_link(city,headers)
    
    datestr=datetime.datetime.now().strftime('%Y%m%d')
    
    proxies={'https':''}
    #爬数据，并保存在子文件夹save_html_data中，每个日期一个文件夹，同一天的数据放在以日期命名的子文件夹中
    for i in range(0,len(quyu_link_list)):
        url=quyu_link_list[i]
        quyu=quyu_list[i]
        filename=save_folder_path+datestr+'_'+city+'/html_'+quyu+'.txt'
        if os.path.exists(filename):
            print(str(i)+'/'+str(len(quyu_link_list))+','+quyu+',文件已存在，跳过')
            pass
        else:
            totalPage=get_page_num(url,headers=headers,proxies=proxies)
            print(str(i)+'/'+str(len(quyu_link_list))+','+quyu+',共'+str(totalPage)+'页')
            if totalPage==0:
                html=''
            else:
                html=get_html(url,totalPage,headers=headers,proxies=proxies)
            save_html(html,datestr,city,quyu,save_folder_path)