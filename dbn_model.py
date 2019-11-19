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
    plt.show()
    plt.savefig("%s_variable.png"%name)
    return d,discrete_list
data=pd.read_csv("data1.csv")
node_list_all=data.columns.values.tolist()
print(node_list_all)
new_data=pd.DataFrame()

###############对数据进行离散化处理########################
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
        result_dict[prob_name_dict] = prob_value_dict
    #再计算单个变量的概率
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
result_prob_dict=cal_total_and_two_prob_dict(mutual_nodelist,all_data)

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

##############根据结果画出来贝叶斯网络结构的图###################
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
plt.savefig("myfigure.png")
plt.show()

######################处理虚拟变量计算虚拟变量的值，采取分类以后的加权和，然后再进行离散化划分
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
            break
        except:
            continue
###对V2进行离散化并画图
add_new_virtual_result(v1,"v1")
add_new_virtual_result(v2,"v2")
##保存最终的数据以及网络模型
new_data.to_csv("finally.csv") ##增加了 V1和V2以后的节点


##########################计算条件概率以及预测最终结果################################################
###计算最终的条件概率表以及预测

###第一步根据已知数据计算(hp,tk,p)--v1  以及 (sale,collect)--V2 的条件概率分布
##第二步骤，根据V1和V2的数据，以及其他数据计算最终变量"NNN"的条件概率分布

###预测阶段
##先预测出V1和V2的概率最大的值，然后在根据V1和V2的值以及其他已知的值，去推演预测最终的值
##最后选择分布中概率最大的值作为输出结果

##最后根据预测的值，利用离散化区间区还原预测结果根据离散化的表

##同样用字典存储，字典的名称为p(y1|x1,x2,x3) 其值也是字典{y=1|x1=，x2=,x3=,:}这样一个字典样式进行

def cal_conditional_properties():
    pass
