# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 10:21:01 2018

@author: Annie
"""

def save_data_mongodb(df,city,datestr):
    import pymongo
    
    # 链接本地的数据库 默认端口号的27017
    client = pymongo.MongoClient('localhost', 27017)
    # 数据库的名字（mongo中没有这个数据库就创建）
    database = client['LianJIa']
    # 表名
    savename='house_%s_%s'%(city,datestr)
    table = database[savename]
    
    data=df.to_dict(orient='records') #dataframe转为dict 
    table.insert_many(data)
    
def read_data_mongodb(city,datestr):
    import pymongo
    import pandas as pd
    
    client = pymongo.MongoClient('localhost', 27017)
    database = client['LianJIa']
    filename = 'house_%s_%s'%(city,datestr)
    table = database[filename]
    
    df=pd.DataFrame(list(table.find()))
    del df['_id']
    
    return df

