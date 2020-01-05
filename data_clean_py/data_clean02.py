#-*-coding:utf8-*-
#user:brian
#created_at:2019/12/27 16:04
# file: data_clean02.py
#location: china chengdu 610000
#当前清洗好的数据为data_04
import pandas as pd
import numpy as np
import time
# import os
# os.environ["CUDA_VISIBLE_DEVICES"]="0"
name_index_global=['641 靠梯桥', '644 清洁完成', '645开货仓', '655 配餐完成',
       '660 机务完成', '662登机开始', '668关货仓 ', '669 撤轮档', '361机务完成', '365加油完成 缺失较多',
       '368开客舱', '369上轮档', '370登机结束', '378 配餐开始 8个', '379清洁开始', '380撤梯桥',
       '637关客舱']

#得到新的数据，然后再利用贝叶斯网络参数估计对数据进行补齐操作
from pgmpy.models import BayesianModel
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination
from pgmpy.estimators import ParameterEstimator
#获取两个变量之间的数据
def get_diff_of_two_node2(A,B,data):
    data_temp=data[[A,B]]
    data_temp=data_temp[data_temp[A]!=-1]
    data_temp=data_temp[data_temp[B]!=-1]
    return data_temp
#获取两个变量之间的诊断模型
def get_all_cpb_infer_models(name_list,data):
    model_dict={}
    for i in range(len(name_list)-1):
        for j in range(i+1,len(name_list)):
            A=name_list[i]
            B=name_list[j]
            name_compare=A+"_"+B
            print(A,B)
            try:
                model = BayesianModel([(A,B)])
                two_nodedata=get_diff_of_two_node2(A,B,data)
                model.fit(two_nodedata, estimator=MaximumLikelihoodEstimator)
                infer_temp=VariableElimination(model)
                #print(infer_temp.map_query([B], evidence={A: 90})) #查询的代码
                model_dict[name_compare]=infer_temp
            except:
                print(name_compare,"failed****************")
                model_dict[name_compare]=-1
    return model_dict
#获取所有模型的贝叶斯网络参数估计模型
def get_all_corrrelation_list(name_list):
    corr_dict={}
    for i in range(len(name_list)-1):
            for j in range(i+1,len(name_list)):
                A=name_list[i]
                B=name_list[j]
                name_compare=A+"_"+B
                print(A,B)
                try:
                    two_nodedata=get_diff_of_two_node2(A,B)
                    coor=two_nodedata.corr().iloc[0,1] #提取到的两个变量之间的相关系数
                    print(coor)
                    if coor>0:
                        corr_dict[name_compare]=coor
                    else:
                        corr_dict[name_compare]=-1
                except:
                    corr_dict[name_compare]=-1
    return corr_dict
#从字典中索引corrdata
def get_corr_data(A,B,corr_dict):
    name=A+"_"+B
    name2=B+"_"+A
    try:
        resul=corr_dict[name]
    except:
        resul=corr_dict[name2]
    return resul
#对相关性进行排序
def get_sorted_corr_dict(name_list):
    corr_dict=get_all_corrrelation_list(name_list)
    corr_dict_sorted={} #计算好的按照相关度排序的节点名称
    for A in name_list:
        temp_dict={}
        for B in name_list:
            if B!=A:
                temp_dict[B]=get_corr_data(A,B,corr_dict)
        corr_dict_sorted[A] =sorted(temp_dict, key=lambda x:temp_dict[x])
    return corr_dict_sorted
def get_bayesin_model(A,B,all_model_cpb):
    name=A+"_"+B
    name2=B+"_"+A
    try:
        resul=all_model_cpb[name]
    except:
        resul=all_model_cpb[name2]
    return resul

##有了相关性，也有了数据，也有了模型，下一步对数据进行填充
#主要耗时不在模型的建立，而在于计算，因此建立循环计算模型来进行填充值
#必须把值填充成功的目标，挨个用每个值进行循环
def cleand_cycle(data_05,save_file="cleaned_final06.csv"):
    # data_05=data_05[data_05['369上轮档']!=-1]
    data_06=data_05.copy()
    for target_name in name_index_global:
       name_compare_list=corr_dict_sorted[target_name]
       # print(name_compare_list)
       for index in data_05.index:
           for name_compare in name_compare_list:
               valule_compare=data_05.loc[index,name_compare]
               if valule_compare!=-1:
                   #获取待比较的模型
                   model=get_bayesin_model(target_name,name_compare,all_model_cpb)
                   try:
                       target_value=model.map_query([target_name], evidence={name_compare: valule_compare},show_progress=False)
                       data_06.loc[index,target_name] = target_value
                       break
                   except:
                       continue
           if index%500==0:
               print(data_06.loc[index,target_name],"current node->",target_name,name_index_global.index(target_name),"this node remain %d"%(len(data_06)-index))
    data_06.to_csv(save_file)
def cleand_cycle2(data_05,all_model_cpb,corr_dict_sorted,save_file="cleaned_final06.csv"):
    # data_05=data_05[data_05['369上轮档']!=-1]
    data_06=data_05.copy()
    for target_name in name_index_global:
       start_time=time.time()
       name_compare_list=corr_dict_sorted[target_name]
       # print(name_compare_list)
       data_temp=data_06[data_06[target_name]==-1] #筛选出来为空值的数据
       for index in data_temp.index:
           for name_compare in name_compare_list:
               valule_compare=data_05.loc[index,name_compare]
               if valule_compare!=-1:
                   #获取待比较的模型
                   model=get_bayesin_model(target_name,name_compare,all_model_cpb)
                   try:
                       target_value=model.map_query([target_name], evidence={name_compare: valule_compare},show_progress=False)
                       data_06.loc[index,target_name] =  list(target_value.values())[0]
                       break
                   except:
                       continue
           if list(data_temp.index).index(index)%500==0:
               print(data_06.loc[index,target_name],"current node->",target_name,name_index_global.index(target_name),"this node remain %d"%(len(data_temp)-list(data_temp.index).index(index)))
       end_time=time.time()
       print("本次迭代变量--> %s 耗时: %s "%(target_name,end_time-start_time))
    data_06.to_csv(save_file)


data_04=pd.read_csv("cleaned_final02.csv")
data_05=data_04[name_index_global]
all_model_cpb=get_all_cpb_infer_models(name_index_global,data_05) #获得是所有的变量之间的模型
corr_dict_sorted=get_sorted_corr_dict(name_index_global)
cleand_cycle2(data_05,all_model_cpb,corr_dict_sorted,"cleaned_final06.csv")

save_file_cycle="cleaned_final06.csv"
for name_save in range(10):
    print("正在进行的第？次循环迭代",name_save)
    data_cycle1=pd.read_csv(save_file_cycle)
    save_file_cycle="save_file_cycle_%d.csv"%name_save
    data_cycle2 = data_cycle1[name_index_global]
    all_model_cpb = get_all_cpb_infer_models(name_index_global, data_05)  # 获得是所有的变量之间的模型
    corr_dict_sorted = get_sorted_corr_dict(name_index_global)
    cleand_cycle2(data_cycle2, all_model_cpb,corr_dict_sorted,save_file_cycle)


