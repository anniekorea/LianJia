# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 13:20:43 2018

@author: Administrator
"""

#对比同一个城市，不同时期的房源数据
def compare_two_date(date_earlier,date_later,city):
    import pandas as pd
    import numpy as np
#    filename_earlier='house_sh_20180809'
#    filename_later='house_sh_20180816'
    filename_earlier='house_%s_%s'%(date_earlier,city)
    filename_later='house_%s_%s'%(date_later,city)
    
    house1=pd.read_csv('../LianJiaSaveData/save_house_data/%s.csv'%(filename_earlier),sep=',',index_col=0)
    house2=pd.read_csv('../LianJiaSaveData/save_house_data/%s.csv'%(filename_later),sep=',',index_col=0)
    house_merge=house1.merge(house2,on='id',how='inner')
    house_merge['diff_totalprice']=house_merge['totalprice_y']-house_merge['totalprice_x']
    house_merge['diffpct_totalprice']=house_merge['totalprice_y']/house_merge['totalprice_x']-1
    
    diff_tp=house_merge['diff_totalprice']
    diffpct_tp=house_merge['diffpct_totalprice']
    
    diff_count=len(house2)-len(house1)
    if diff_count>0:
        a1='%s有%d套房源，%s有%d套房源，增加%d套'%(filename_earlier,len(house1),filename_later,len(house2),diff_count)
    elif diff_count<0:
        a1='%s有%d套房源，%s有%d套房源，减少%d套'%(filename_earlier,len(house1),filename_later,len(house2),-diff_count)
    else:
        a1='%s有%d套房源，%s有%d套房源，房源数无变化'%(filename_earlier,len(house1),filename_later,len(house2))

    a2='，两个文件共同的房源%d套'%len(diff_tp)
    
    diff_mean_price=np.mean(house2['price'])-np.mean(house1['price'])
    if diff_mean_price>0.01:
        a9='%s的单价平均值为%.2f万元，%s的单价平均值为%.2f万元，上涨%.2f万元'%\
            (filename_earlier,np.mean(house1['price']),
            filename_later,np.mean(house2['price']),diff_mean_price)
    elif diff_mean_price<-0.01:
        a9='%s的单价平均值为%.2f万元，%s的单价平均值为%.2f万元，下跌%.2f万元'%\
            (filename_earlier,np.mean(house1['price']),
            filename_later,np.mean(house2['price']),diff_mean_price)
    else:
        a9='%s的单价平均值为%.2f万元，%s的单价平均值为%.2f万元，基本保持不变'%\
            (filename_earlier,np.mean(house1['price']),
            filename_later,np.mean(house2['price']))
    
    a3='其中%d套房源价格上调，占比%.4f%%，平均上涨%.2f万元，平均涨幅%.2f%%'%\
        (sum(diff_tp>0),sum(diff_tp>0)/len(house_merge),
         np.mean(diff_tp[diff_tp>0]),np.mean(diffpct_tp[diffpct_tp>0])*100)
    a4='其中%d套房源价格下调，占比%.4f%%，平均下跌%.2f万元，平均跌幅%.2f%%'%\
        (sum(diff_tp<0),sum(diff_tp<0)/len(house_merge),
         np.mean(diff_tp[diff_tp<0]),np.mean(diffpct_tp[diffpct_tp<0])*100)
    
    house_merge_sortby_diffpct=house_merge.sort_values(by='diffpct_totalprice')
    a5='上调幅度最大的房源ID：%d，原价格：%.2f万元-->现价格：%.2f万元，涨幅%.2f%%'\
            %(house_merge_sortby_diffpct.tail(1)['id'],
            house_merge_sortby_diffpct.tail(1)['totalprice_x'],
            house_merge_sortby_diffpct.tail(1)['totalprice_y'],
            house_merge_sortby_diffpct.tail(1)['diffpct_totalprice']*100)
    a6='下调幅度最大的房源ID：%d，原价格：%.2f万元-->现价格：%.2f万元，跌幅%.2f%%'\
            %(house_merge_sortby_diffpct.head(1)['id'],
            house_merge_sortby_diffpct.head(1)['totalprice_x'],
            house_merge_sortby_diffpct.head(1)['totalprice_y'],
            house_merge_sortby_diffpct.head(1)['diffpct_totalprice']*100)

    
    house_merge_sortby_diffpct=house_merge[house_merge['totalprice_x']<=500].sort_values(by='diffpct_totalprice')
    a7='总价500万元以下，上调幅度最大的房源ID：%d，原价格：%.2f万元-->现价格：%.2f万元，涨幅%.2f%%'\
            %(house_merge_sortby_diffpct.tail(1)['id'],
            house_merge_sortby_diffpct.tail(1)['totalprice_x'],
            house_merge_sortby_diffpct.tail(1)['totalprice_y'],
            house_merge_sortby_diffpct.tail(1)['diffpct_totalprice']*100)  
    a8='总价500万元以下，下调幅度最大的房源ID：%d，原价格：%.2f万元-->现价格：%.2f万元，跌幅%.2f%%'\
            %(house_merge_sortby_diffpct.head(1)['id'],
            house_merge_sortby_diffpct.head(1)['totalprice_x'],
            house_merge_sortby_diffpct.head(1)['totalprice_y'],
            house_merge_sortby_diffpct.head(1)['diffpct_totalprice']*100)
  
    print(a1+a2)
    print(a9)
    print(a3)
    print(a4)
    print(a5)
    print(a6)
    print(a7)
    print(a8)

#对比不同城市的房源数据
def compare_many_files(filename_list):
#    filename_list=['house_bj_20180815','house_sz_20180818','house_sh_20180809',
#                   'house_gz_20180819','house_hz_20180814','house_nj_20180817',
#                   'house_wh_20180819','house_cd_20180819','house_hui_20180819',
#                   'house_cs_20180819','house_xa_20180819']
    import pandas as pd    
    for i in range(0,len(filename_list)):
        house=pd.read_csv('../LianJiaSaveData/save_house_data/%s.csv'%(filename_list[i]),sep=',',index_col=0)
        df1=pd.DataFrame({'filename':[filename_list[i]],'housenum':[len(house)]})
        df2=pd.DataFrame({'totalprice_median':[house['totalprice'].median()],
                        'totalprice_mean':[house['totalprice'].mean()],
                        'totalprice_min':[house['totalprice'].min()],
                        'totalprice_max':[house['totalprice'].max()]})
        df3=pd.DataFrame({'price_median':[house['price'].median()],
                        'price_mean':[house['price'].mean()],
                        'price_min':[house['price'].min()],
                        'price_max':[house['price'].max()]})
        df4=pd.DataFrame({'mianji_median':[house['mianji'].median()],
                        'mianji_mean':[house['mianji'].mean()],
                        'mianji_min':[house['mianji'].min()],
                        'mianji_max':[house['mianji'].max()]})
        df=pd.concat([df1,df2,df3,df4],axis=1)
        if i==0:
            result=df
        else:
            result=result.append(df)
        #指定顺序
        result=result.loc[:,['filename','housenum',
                             'totalprice_median','totalprice_mean','totalprice_min','totalprice_max',
                             'price_median','price_mean','price_min','price_max',
                             'mianji_median','mianji_mean','mianji_min','mianji_max']]
    return result



