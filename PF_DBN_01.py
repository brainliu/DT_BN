#-*-coding:utf8-*-
#user:brian
#created_at:2019/12/17 10:35
# file: PF_DBN_01.py
#location: china chengdu 610000
import pandas as pd

##字段整理
#选取的字段
#DFLIGHTNO 离港航班id  DIATACD 航空公司代码  ALTEXECDATE 实际执行日期
# ONGEAR 上轮档时间  REGEAR 撤轮档时间 ONBRIDGE 靠梯桥 REBRIDGE 撤梯桥 OPENCABINGATE 开客舱 OPENCARGOGATE 开货仓
#GATE 登机口
#LUGLOADSTART 行李装载开始 LUGLOADEND 行李装载结束
#CLEANSTART 清洁开始  CLEANEND 清洁结束
# CLOSECABINGATE 关客舱  CLOSECARGOGATE 关货仓
#PERMITPUSH 允许放行
#TRACTORARR 牵引车到位
#ALANDINTIME 实际着落时间  DTAKEOFFTIME 实际起飞时间
#DROPOFFSTART 开始卸机  DROPOFFEND 卸机完成  缺失值比较多* 先不考虑这个字段
#STANDNEARFAR 远近机位 0 近机位 1远机位
# AFLIGHTATTR 进港航班属性  DFLIGHTATTR 离港航班属性
#ADDCLEARWATERSTART 清水加水开始  ADDCLEARWATEREND清水完成
#DSCHETAKEOFFTIME 离港计划起飞时间 ASCHELANDINTIME 离港计划着陆时间
#CRAFTTYPE 机型  SIZETYPE 尺寸
all_list=["DFLIGHTNO","DIATACD","ALTEXECDATE","ONGEAR","REGEAR","DROPOFFSTART","DROPOFFEND",
          "OPENCABINGATE","OPENCARGOGATE","GATE","LUGLOADSTART","LUGLOADEND",                 #"CLEANSTART",
          "CLEANEND","PERMITPUSH","TRACTORARR", "DTOTALPSG",  "DTOTALLUG", "CLOSECABINGATE", #"CLOSECARGOGATE",
          "ALANDINTIME","DTAKEOFFTIME","STANDNEARFAR","AFLIGHTATTR","DFLIGHTATTR",
          "BOARDINGEND","BOARDINGSTART",
          "ADDCLEARWATERSTART","DSCHETAKEOFFTIME","ASCHELANDINTIME"] #,"CRAFTTYPE","SIZETYPE"]
try:
    model_data=pd.read_csv("cleaned_Data.csv")
except:

    data=pd.read_csv("xining_admerges1.csv")
    print(1)
    model_data=data[all_list].copy()
    model_data.to_csv("cleaned_Data1.csv")
    model_data=model_data.dropna()
    model_data.to_csv("cleaned_Data.csv")
# 一、影响航班的外在因素用于数据分类
# 前置条件  决策树的标签分为四类 到达和离开的延误 四种标签 进行数据分类 或者A,B,C,D
#输入因素有： 星期、月份、远近机位、大中机型、航空公司、         计划起飞时刻（0-23小时）、机位号、进港航班属性、     离港航班属性，            计划着陆时刻
#      ALTEXECDATE    STANDNEARFAR    CRAFTTYPE   DIATACD          GATE     AFLIGHTATTR     DFLIGHTATTR    ASCHELANDINTIME
#     DTOTALPSG          DTOTALLUG
#      离港总人数          离港总行李

#二、航班保障网络节点数据动态预测
#航班保障网络模型：
#上轮档时间、撤轮档时间、        开客舱、            开货仓、 行李装载开始、 行李装载结束、 清洁开始、    清洁结束、   关客舱、         关货仓、
#  ONGEAR     REGEAR    OPENCABINGATE  OPENCARGOGATE      LUGLOADSTART  LUGLOADEND   CLEANSTART   CLEANEND    CLOSECABINGATE  CLOSECARGOGATE
#牵引车到位、    清水开始、          清水结束                     开始卸机         卸机完成         开始上客           上客结束
# TRACTORARR  ADDCLEARWATERSTART   ADDCLEARWATEREND          DROPOFFSTART      DROPOFFEND     "BOARDINGEND","BOARDINGSTART",
# 允许放行、       实际起飞              计划起飞
#  PERMITPUSH    DTAKEOFFTIME        DSCHETAKEOFFTIME

#时间转化


























