#-*-coding:utf8-*-
#user:brian
#created_at:2019/11/28 14:22
# file: BN_P.py
from scipy.io import loadmat
import pandas as pd
import numpy as np
#将mat文件转化为csv文件的程序
def mat_to_csv(matfilename,csvfilename):
    annots = loadmat(matfilename)
    data_name=list(annots.keys())[-1]
    csv_data = pd.DataFrame(annots[data_name])
    csv_data.to_csv(csvfilename)
""" 
mat_to_csv("fuhe.mat","fuhe.csv")# 负荷数据
mat_to_csv("fengsu2006_2010","fengsu2006_2010.csv") #为34个风电场每小时风速数据,[8760*4]*33
mat_to_csv("fuhe1999.mat","fuhe1999.csv")#1999年负荷数据
mat_to_csv("fuhe2014.mat","fuhe2014.csv")#2014年负荷数据
mat_to_csv("h.mat","h.csv")#%RTS79系统负荷数据[364*24],364天,每天24小时的负荷
mat_to_csv("guangfu.mat","guangfu.csv")#[8760*4]*2
"""
##将负荷数据拼接为风速相同的维度【8760*4】*1 由于原先只有364天，因此需要加4天的数据 改为365天
data_fuhe=pd.read_csv("h.csv")
data_fuhe=data_fuhe.append(data_fuhe) # 叠加 1*1
data_fuhe=data_fuhe.append(data_fuhe) #叠加2*2
data_fuhe=data_fuhe.append(data_fuhe[0:4]) #增加4天 凑成365*4 天
#得到负荷数据
data_fuhe=np.array(data_fuhe)[:,1:25].reshape(35040,1) #转化为与风速相同的维度的数据

data_fuhe=pd.DataFrame(data_fuhe)
data_fuhe.columns=["fuhe"] #构造新的 datafame中名称
#计算风速数据 第3：7 行为5个风速数据
data_fengshu=pd.read_csv("fengsu2006_2010.csv")
data_fengshu=pd.DataFrame(np.array(data_fengshu)[:,2:7])
data_fengshu.columns=["fengsu1","fengsu2","fengsu3","fengsu4","fengsu5"]
#提取光伏数据
data_guangfu=pd.read_csv("guangfu.csv")
data_guangfu.columns=["guangfu1","guangfu2","guangfu3","guangfu4"]



