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
data_guangfu=pd.DataFrame(np.array(data_guangfu)[:,1:])
data_guangfu.columns=["guangfu1","guangfu2","guangfu3","guangfu4"]

#合并成为新的数据
data_all=data_fuhe.join(data_guangfu) # fuhe guangfu1 guangfu2 guangfu3 guangfu4
data_all=data_all.join(data_fengshu)  # fengsu1 fengsu2 fengsu3 fengsu4 fengsu5

#贝叶斯网络的层级关系，一共四层
#第一层为元件结点，包括变压器结点 T18-T40 以及线路结点 L35-44，L41，…，L59-64 共 33 个结点，
# 第二层是联合结点 一个s1 和一个等值功率节点
#第三层是负荷结点，包括 LP18-LP40 共 23 个结点
#第四层是系统节点，微网和非微网
# 第五层是最后的节点，表示系统
# 在逻辑关系上，第一层与第二层是联合关系，第一层与第三层是或关系，第三层与第四层是因果关系

##算法步骤
#1 初始化数据也就是，设置置信概率95%，循环次数为20000次，ssui精度为0.000006
# i=1  to 8760 进行循环
    # 循环2000次 产生元件状态，并利用贝叶斯去推断计算负荷节点的状态
        # 分别计算每一个元件进行模拟，找到其最小持续时间段
        #微网外的负荷 计算  贝叶斯推理计算负荷结点的状态
        #微网内的负荷 计算  利用时序推理计算 根据光伏和风速 与负荷关系判断是否正常
    # 累计停电时间和停电次数（也就是负荷结点的故障时间和故障次数） 在最小时间内
    # 最后计算其他相关的指标
    # 主要利用或，联合，因果等关系进行推理判断

#最后输出条件概率 系统故障时，各元件故障的概率
"""
%----------由风速转换为风机的发电功率
Pr=2.0;%风机额定功率2.0MW
V1=4;%切入风速，4m/s
V2=15;%额定风速，15m/s
V3=25;%切出风速，25m/s
 P=[];  %将原始风速矩阵x转换为风机的功率
 xxx=xx';
  for j1=1:nsamples;
        for j2=1:column;
            if xxx(j2,j1)<V1 
                P(j2,j1)=0;
            elseif xxx(j2,j1)>=V1 && xxx(j2,j1)<V2;
                P(j2,j1)=Pr*(xxx(j2,j1)-V1)./(V2-V1);
            elseif xxx(j2,j1)>V2 && xxx(j2,j1)<=V3;
                P(j2,j1)=Pr;
            else if xxx(j2,j1)>V3
                PZ(j2,j1)=0;
            end
        end
        end
  end
"""