#-*-coding:utf8-*-
#user:brian
#created_at:2019/11/13 8:44
# file: data_clean.py
#location: china chengdu 610000
#处理原始数据
import pandas as pd
import numpy as np
data=pd.read_csv("origindata.csv")
print(data.index)
#Index(['flight', 'name', 'date', 'time'], dtype='object')
name_index=set(data["name"].values)
date_index=set(data["date"].values)
flight_index=set(data["flight"].values)
merged_data={}
merged_data["flight"]=[]
merged_data["date"]=[]
for i in name_index:
    merged_data[i]=[]


for date in date_index:
    data_temp=data[data["date"]==date]
    flight_set=set(data_temp["flight"].values)
    for flight_temp in flight_set:
        merged_data["date"].append(date) #增加航班日期
        merged_data["flight"].append(flight_temp) #增加航班号
        node_value_all=data_temp[data_temp["flight"]==flight_temp]
        for node_name in name_index:
            try:
                node_value=node_value_all[node_value_all["name"]==node_name]["time"].values[0]
                print(node_value)
                merged_data[node_name].append(node_value)
            except:
                merged_data[node_name].append(-1)
pd.DataFrame(merged_data).to_csv("cleaned.csv")