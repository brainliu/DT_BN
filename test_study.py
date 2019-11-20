#-*- coding:utf-8 -*-
#created by brian
# create time :2019/11/9-17:09 
#location: sichuan chengdu
from thinkbayes import Pmf
import pandas as pd
pmf=Pmf()
for x in [1,2,3,4,5,6]:
    pmf.Set(x,1/6.0)

ppp=list()
ppp.append(1)
print(ppp)






def cal_conditional_properties(data,x_list,y_node,result_condition_dict_cpt):
    groupby_list=x_list.copy()
    groupby_list.append(y_node)
    print(groupby_list,x_list)

    count_data_temp_condition = dict(data.groupby(list(x_list)).size())
    count_data_temp_y=dict(data.groupby(list(groupby_list)).size())
    #y的取值范围，通过数据来获取
    y_list_set=set(data[y_node])
    print(y_list_set)
    first_dict_name="P("+y_node+"|"+str(x_list)+")"
    # print(first_dict_name)
    result_condition_dict_cpt[first_dict_name]={}
    #{p(y_node|x_list): {[0,1,2]:{1:p1,2:p2}, [0,1,3]:{1:p1,2:p2},[0,1,4]:{1:p1,2:p2} }}
    ##如上所示的一个嵌套dict，外层为索引的节点变量，第二层字典名称为x_list具体的取值，第三层为y的取值以及相应的概率
    ##预测的时候去这样的dict中去求
    for condition_compare in count_data_temp_condition.keys(): #condition_compare=(0,1,2) 类似于tuple 作为条件
        value_count_all=count_data_temp_condition[condition_compare]#求得各种条件下的组合情况
        name=str(list(condition_compare))
        prob_dict_temp={} #{1:0.2,2:0.3,3:0.4} 类似于这种的各种概率字典
        for j in y_list_set:
            count_one_temp_tuple = list(condition_compare)
            count_one_temp_tuple.append(j)
            try:
                value_count_one=count_data_temp_y[tuple(count_one_temp_tuple)]
            except:
                value_count_one=0.0
            value_prob_temp=value_count_one/value_count_all
            prob_dict_temp[j]=value_prob_temp
        result_condition_dict_cpt[first_dict_name][name]=prob_dict_temp
    # print(result_condition_dict_cpt)
    return result_condition_dict_cpt
#{"P(v1|['hp', 'tk', 'p'])": {'[0, 0, 2]': {0: 1.0, 1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0}, '[0, 1, 0]': {0: 1.0, 1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0}... typeN

data=pd.read_csv("finally.csv")
result_all_cpt_dict={}

x_list1,y_node1=["hp","tk","p"],"v1"
x_list2,y_node2=["sale","collcet"],"v2"
x_list3,y_node3=['cn_add', 'cn_z', 'picture', 'opening_hours',"v1","v2"],"NNN"

result_all_cpt_dict=cal_conditional_properties(data,x_list1,y_node1,result_all_cpt_dict)
result_all_cpt_dict=cal_conditional_properties(data,x_list2,y_node2,result_all_cpt_dict)
result_all_cpt_dict=cal_conditional_properties(data,x_list3,y_node3,result_all_cpt_dict)
for key,value in result_all_cpt_dict.items():
   print("#" * 50)
   print(key)
   print("#"*50)
   for key_2,value_2 in value.items():
       print(key_2+":",value_2)
   print("#" * 50)
   print("\n")
data=pd.read_csv("test.csv")
test_node_list=['p', 'sale', 'collcet', 'cn_add', 'cn_z', 'picture', 'opening_hours', 'hp', 'tk', 'NNN']

for keys in x_list1:
    index=test_node_list.index(keys)
    print(index)
