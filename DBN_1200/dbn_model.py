#-*-coding:utf8-*-
#user:brian
#created_at:2019/11/11 12:03
# file: dbn_model.py
import matplotlib.pyplot as plt
import pandas as pd
import itertools
from math import log
from operator import itemgetter
import networkx as nx
import matplotlib.pyplot as plt
##第一步计算变量与T之间的mi值，存储到dict中
##第二步设定虚拟变量并计算虚拟变量的值
##第三步构建贝叶斯网络并计算cpt条件概率值，输出cpt的概率分分布
##第四部构建贝叶斯网络模型并画图
##第四步预测模型构建，并输出预测精度

#################################  1 ###########################################
###############################################################################
#处理数据离散化并赋值标签，采用等距离散化的方式
def classified_plot(data,k,name):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    d = pd.cut(data, k, labels=range(k))
    plt.figure(figsize=(7,5))
    discrete_list=[]
    for j in range(0, k):
        temp=[]
        plt.plot(data[d==j], [i for i in d[d==j]], 'o')
        temp.append(min(data[d==j]))
        temp.append(max(data[d==j]))
        discrete_list.append(temp)

    plt.savefig("./MWK/%s_variable.png"%name)  #可视化数据离散化的结果并保存
    plt.show()
    return d,discrete_list

data=pd.read_csv("data1.csv")
node_list_all=data.columns.values.tolist()
print(node_list_all)
new_data=pd.DataFrame()

###############对数据进行离散化处理########################
discrete_dict={} #用来保存离散化处理的结果的字典
print("离散化处理的结果：\n")
print("#"*20)
for name in node_list_all[1:]:
    data_temp=data[name].copy()
    k_max=5 #最多分成5个区间
    for k in range(k_max):
        K_select=5-k
        try:
            cut_temp, cut_list = classified_plot(data_temp, K_select,name)
            new_data[name]=cut_temp
            print("%s is 被离散化成了 %d 部分!"%(name,K_select))
            new_data[name] = cut_temp
            print("%s分段离散的区间的点如下："%name)
            print(cut_list)
            discrete_dict[name] =cut_list
            break
        except:
            continue
new_data.to_csv("new.csv") #生成的新的数据集
print("#"*20)
print("\n")
################################################################################
##计算条件概率的值
##计算全概率表和单个变量的概率表用字典表示
################计算概率表以及相关性##################################
def cal_total_and_two_prob_dict(node_list,all_data,result_dict={}):#可以传,也可以不传
    #先计算两个变量的全概率
    N=len(all_data)
    print("#" * 50)
    print("变量两两之间的分布如下：")
    for node_compare in itertools.combinations(node_list,2):
        # node_compare=list(node_compare) #全概率没有顺序，无关
        prob_value_dict={}
        #构造字典名称P(SepalLength,SepalWidth,PetalLength,PetalWidth)
        prob_name_dict="P("+node_compare[0]+","+node_compare[1]+")"
        input_node=(set(all_data[name]) for name in node_compare) #tuple 输入的数据集合
        count_data_temp = dict(new_data.groupby(list(node_compare)).size())  # 转化为字典方便操作
        for prob_compare in itertools.product(*input_node):#对每一种组合进行循环
            try:
                prob_value = count_data_temp[prob_compare] / N
            except:
                prob_value = 0.0  #将没有出现的组合填充为0.0
            prob_value_dict[prob_compare] = prob_value
        print(prob_name_dict + "          :", prob_value_dict)
        result_dict[prob_name_dict] = prob_value_dict

    #再计算单个变量的概率，并输出
    print("#"*50)
    print("单个变量的概率分布如下：")
    for node_one in node_list:
        prob_value_dict = {}
        prob_name_dict ="P("+node_one+")"
        input_node = set(all_data[node_one])  # tuple 输入的数据集合
        count_data_temp=dict(new_data.groupby(node_one).size())  # 转化为字典方便操作
        for prob_one in input_node:
            try:
                prob_value=count_data_temp[prob_one]/N
            except:
                prob_value=0.0
            prob_value_dict[prob_one] = prob_value
        result_dict[prob_name_dict] = prob_value_dict
        print(prob_name_dict+"          :",prob_value_dict)
    return result_dict
####计算mi的值 与目标变量之间的bic值
##目标便变量为数据中的最后一列 也就是"NNN"
#['date', 'p', 'sale', 'collcet', 'cn_add', 'cn_z', 'picture', 'opening_hours', 'hp', 'tk', 'NNN']
def mutual_information(node_list,all_data,all_prob_dict,result_mutual={}):
    for node_compare in itertools.combinations(node_list, 2):
        MI_name_dict = "MI(" + node_compare[0] + "," + node_compare[1] + ")"
        p_x_name="P("+node_compare[0]+")"
        p_y_name="P("+node_compare[1]+")"
        p_x_y_name="P("+node_compare[0]+","+node_compare[1]+")"
        input_node = (set(all_data[name]) for name in node_compare)  # tuple 输入的数据集合
        #计算每个组合的互信息
        mu_value=0.0
        for prob_compare in itertools.product(*input_node):  # 对每一种组合进行循环
            p_x_y=all_prob_dict[p_x_y_name][prob_compare]
            p_x=all_prob_dict[p_x_name][prob_compare[0]]
            p_y=all_prob_dict[p_y_name][prob_compare[1]]
            try:
                mu_value+=p_x_y*log(p_x_y/(p_x*p_y))
            except:
                continue
        result_mutual[MI_name_dict]=mu_value
    return result_mutual
mutual_nodelist=['p', 'sale', 'collcet', 'cn_add', 'cn_z', 'picture', 'opening_hours', 'hp', 'tk', 'NNN']
all_data=new_data #所有的处理好的数据
result_prob_dict=cal_total_and_two_prob_dict(mutual_nodelist,all_data)#计算条件概率分布以及输出单个变量的分布概率表

all_mutil_value=mutual_information(mutual_nodelist,new_data,result_prob_dict)
##输出计算后的互信息依次为MI(P,NNN),MI(sale,NNN)
mutual_nodelist_A=['p', 'sale', 'collcet', 'cn_add', 'cn_z', 'picture', 'opening_hours', 'hp', 'tk']
result_list=[]
for mutual_A in mutual_nodelist_A:
    temp=[]
    prob_name_dict = "MI(" + mutual_A + "," + 'NNN' + ")"
    value=all_mutil_value[prob_name_dict]
    temp.append(mutual_A)
    temp.append(value)
    result_list.append(temp)
sort_d = sorted(result_list,key=itemgetter(1),reverse=True)
print("#"*20)
print(u"计算出来的与目标变量之间互信息值为：")
for item in sort_d:
    print("%15s -->NNN  :    %.8f"%(item[0],item[1]))
print("#"*20)
print("\n")
#########输出得到排好序的各个节点与预测的目标节点NNN之间的互信息相关性#############
##寻找阈值，需要进行观察，这里一般设定在0.06左右，
yuzhi=0.06 #表示需要进行合并的节点
##本测试数据中算出来的的各项相MI信息如下：
###################################################################################
##下表为输出数据以及分析过程
#[['opening_hours', 0.15478329090721105], ['cn_z', 0.09912488795134498],
# ['picture', 0.08704216312450302], ['cn_add', 0.0791674853845806],
# ['hp', 0.05711082764131546], ['tk', 0.0563649514304303],
# ['p', 0.0520151046249294], ['sale', 0.04092725833370645],
# ['collcet', 0.0024383957458229415]]
#################重要部分######################
#因此可以考虑用0.06 设定为阈值
##那么经过观察可以发现，合并的点有如下四个：
# ['hp', 0.05711082764131546], ['tk', 0.0563649514304303],
# ['p', 0.0520151046249294], ['sale', 0.04092725833370645],
# ['collcet', 0.0024383957458229415]]
##这五个点随机组合成两个虚拟节点：(hp,tk,p)--v1  以及 (sale,collect)--V2
#########################################################################################

##############根据结果画出来贝叶斯网络结构的图###################
###############################################################################
G = nx.DiGraph(name='my graph')
node_list_all=['p', 'sale', 'collcet', 'cn_add', 'cn_z', 'picture', 'opening_hours', 'hp', 'tk', 'NNN']
target="NNN"
edge_list_first=['cn_add', 'cn_z', 'picture', 'opening_hours'] ######剩下与的互信息比较大的值的集合
#(hp,tk,p)--v1  以及 (sale,collect)--V2
edge_list_second=[("hp","v1"),("tk","v1"),("p","v1"),("sale","v2"),("collcet","v2")] ###新生成的虚拟变量的集合
xu_ni_v=["v1","v2"] ##两个虚拟变量的点
edge_list_all=[]
for i in edge_list_first:
    edge_list_all.append((i,target))
for j in xu_ni_v:
    edge_list_all.append((j,target))
G.add_nodes_from(node_list_all)
G.add_edges_from(edge_list_all)
G.add_edges_from(edge_list_second)
nx.draw(G,with_labels=True, edge_color='b', node_color='g', node_size=1000)
plt.savefig("./MWK/myfigure.png")
plt.show()

######################处理虚拟变量计算虚拟变量的值，采取分类以后的加权和，然后再进行离散化划分
###############################################################################
##这五个点随机组合成两个虚拟节点：(hp,tk,p)--v1  以及 (sale,collect)--V2
##这个数据里面有两个虚拟变量
def add_new_vitural_value(v_list):
    v_temp=[]
    for i in range(len(new_data)):
        temp=0 #初始化temp的值，用来求和
        for j in v_list:
            temp += new_data[j][i]
        v_temp.append(temp)
    return pd.Series(v_temp)
v1_list=["hp","tk","p"]
v2_list=["sale","collcet"]
v1=add_new_vitural_value(v1_list)
v2=add_new_vitural_value(v2_list)

##对新的V1和v2进行划分和添加
def add_new_virtual_result(data_temp,name):
    k_max=5
    for k in range(k_max):
        K_select = 5 - k
        try:
            cut_temp, cut_list = classified_plot(data_temp, K_select, name)
            new_data[name] = cut_temp
            print(u"%s is 被离散化成了 %d 部分!" % (name, K_select))
            new_data[name] = cut_temp
            print(u"%s分段离散的区间的点如下：" % name)
            print(cut_list)
            discrete_dict[name] = cut_list
            break
        except:
            continue
###对V2进行离散化
add_new_virtual_result(v1,"v1")
add_new_virtual_result(v2,"v2")
##保存最终的数据以及网络模型
new_data.to_csv("finally.csv") ##增加了 V1和V2以后的节点

##########################计算条件概率以及预测最终结果################################################
###############################################################################
###第一步根据已知数据计算(hp,tk,p)--v1  以及 (sale,collect)--V2 的条件概率分布
##第二步骤，根据V1和V2的数据，以及其他数据计算最终变量"NNN"的条件概率分布
###预测阶段
##先预测出V1和V2的概率最大的值，然后在根据V1和V2的值以及其他已知的值，去推演预测最终的值
##最后选择分布中概率最大的值作为输出结果
##最后根据预测的值，利用离散化区间区还原预测结果根据离散化的表


#{p(y_node|x_list): {[0,1,2]:{1:p1,2:p2}, [0,1,3]:{1:p1,2:p2},[0,1,4]:{1:p1,2:p2} }}
##如上所示的一个嵌套dict，外层为索引的节点变量，第二层字典名称为x_list具体的取值，第三层为y的取值以及相应的概率
##预测的时候去这样的dict中去求
def cal_conditional_properties(data,x_list,y_node,result_condition_dict_cpt):
    groupby_list=x_list.copy()
    groupby_list.append(y_node)
    count_data_temp_condition = dict(data.groupby(list(x_list)).size())
    count_data_temp_y=dict(data.groupby(list(groupby_list)).size())
    #y的取值范围，通过数据来获取
    y_list_set=set(data[y_node])
    print(y_list_set)
    first_dict_name="P("+y_node+"|"+str(x_list)+")"
    # print(first_dict_name)
    result_condition_dict_cpt[first_dict_name]={}
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
    return result_condition_dict_cpt

###############根据构建好的贝叶斯网络模型计算条件概率表
data=new_data
result_all_cpt_dict={}
##根据网络层次结构输入需要计算的变量以及节点
x_list1,y_node1=["hp","tk","p"],"v1"
x_list2,y_node2=["sale","collcet"],"v2"
x_list3,y_node3=['cn_add', 'cn_z', 'picture', 'opening_hours',"v1","v2"],"NNN"

result_all_cpt_dict=cal_conditional_properties(data,x_list1,y_node1,result_all_cpt_dict)
result_all_cpt_dict=cal_conditional_properties(data,x_list2,y_node2,result_all_cpt_dict)
result_all_cpt_dict=cal_conditional_properties(data,x_list3,y_node3,result_all_cpt_dict)
##输出条件概率分布表
print("条件概率分布表如下所示：\n")
for key,value in result_all_cpt_dict.items():
   print("#" * 50)
   print(key)
   print("#"*50)
   for key_2,value_2 in value.items():
       print(key_2+":",value_2)
   print("#" * 50)
   print("\n")


##############################最后阶段为预测阶段#################################
###############################################################################
##预测阶段--输入数据放在test.csv文件夹里面

test_data=pd.read_csv("test.csv")
###第一步根据前面的离散规则对数据进行离散化处理 离散规则放在 discrete_dict 表中
test_node_list=['p', 'sale', 'collcet', 'cn_add', 'cn_z', 'picture', 'opening_hours', 'hp', 'tk', 'NNN']
print(discrete_dict)
test_data_disct_all=[]
for i in range(len(test_data)): #对每一行的数据进行处理
    test_data_disct=[]
    for node_name in test_node_list:
        discrete_list_temp=discrete_dict[node_name] #离散规则表
        K_select=0
        data_temp=test_data[node_name][i] #待离散的数据
        for k in range(len(discrete_list_temp)):
            zone_list=discrete_list_temp[k]
            if data_temp>= zone_list[0] and data_temp<=zone_list[1]:
                K_select=k
            else:
                continue
        test_data_disct.append(K_select)
    test_data_disct_all.append(test_data_disct)
print(test_data_disct_all)# 得到所有的离散化的数据
test_x=[]
test_y=[]
for index in range(len(test_data_disct_all)):
    test_x_item=[]
    for i in range(len(test_node_list)-1):
        test_x_item.append(test_data_disct_all[index][i]) #前面的时测试输入数据
    test_x.append(test_x_item)
    test_y.append(test_data_disct_all[index][-1]) #最后一列为真实预测数据
##下面是进行预测的阶段
#计算逻辑分为以下三个环节
# ##根据网络层次结构输入需要计算的变量以及节点
x_list1,y_node1=["hp","tk","p"],"v1"
x_list2,y_node2=["sale","collcet"],"v2"
#最终要预测的节点
x_list_test,y_node_test=['cn_add', 'cn_z', 'picture', 'opening_hours',"v1","v2"],"NNN"
edge_list_first=['cn_add', 'cn_z', 'picture', 'opening_hours']  #从表中查找的节点的参数


#计算贝叶斯网络中概率最大的值作为预测结果输出
def predict_one(x_list1,y_node1,test_x,test_node_list,result_all_cpt_dict):
    V1_list = []  # 用来保存计算出来的V1的值
    condition_key="P("+y_node1+"|"+str(x_list1)+")"
    for number in range(len(test_x)): #对每一行的数据进行循环获取求得指标值V1相关的变量
        key_temp=[]
        for keys in x_list1:
            index=test_node_list.index(keys)
            key_temp.append(test_x[number][index]) #获取条件变量组合的情况
        value_prob_dict=result_all_cpt_dict[condition_key][str(key_temp)] #利用条件概率表求最大值
        result_max = max(value_prob_dict, key=lambda x: value_prob_dict[x])
        V1_list.append(result_max)
    return V1_list
#分别结算处V1和V2的预测值
v1_list_pred=predict_one(x_list1,y_node1,test_x,test_node_list,result_all_cpt_dict)
v2_list_pred=predict_one(x_list2,y_node2,test_x,test_node_list,result_all_cpt_dict)

def predict_final(x_list1,edge_list_first,y_node1,test_x,test_node_list,result_all_cpt_dict,v1_list,v2_list):
    result_pred=[]
    condition_key="P("+y_node1+"|"+str(x_list1)+")"
    for number in range(len(test_x)):
        key_temp=[]
        for keys in edge_list_first:
            index=test_node_list.index(keys)
            key_temp.append(test_x[number][index])
        key_temp.append(v1_list[number]) #加入生成的两个变量的节点
        key_temp.append(v2_list[number]) #加入第二个变量的节点
        value_prob_dict = result_all_cpt_dict[condition_key][str(key_temp)]  # 利用条件概率表求最大值
        result_max = max(value_prob_dict, key=lambda x: value_prob_dict[x])
        result_pred.append(result_max)
    return result_pred

#最终的预测结果
resuslt_pred=predict_final(x_list_test,edge_list_first,y_node_test,test_x,test_node_list,result_all_cpt_dict,v1_list_pred,v2_list_pred)
print("预测值和真实值的对比")
print("#"*50)
for i in range(len(test_y)):
    print("输入数据为：",test_x[i])
    print("真实结果：%3s --> 预测结果： %3s"%(test_y[i],resuslt_pred[i]))


