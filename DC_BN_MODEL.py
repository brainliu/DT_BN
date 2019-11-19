#-*- coding:utf-8 -*-
#created by brian
# create time :2019/11/4-23:38 
#location: sichuan chengdu
############################1 用决策树划分状态和数据集，并计算出相应的概率
###已经完成 cart_decisiontree 程序中


############################2 利用概率进行合并数据集，得到决策树对于的数据
####根据输出结果对数据集进行合并
####也可以分开建模然后用概率进行表达，或者合并数据进行关系发现，最后搞一个对比试验
####能够根据网络模型的构建找到每个节点对最后的节点的影响程度
###相当于利用因果关系贝叶斯网络结构图预测出最后一个节点的值是多少
##中间会利用每两个节点之间的差值来分析其概率关系，找到因果关系。
#贝叶斯更新的应用！！！

###########################3 动态贝叶斯网络结构算法，寻找各个节点之间的相关关系
###1）利用互信息对两个个节点任何进行连接得到初始的连接
###2）利用动态规划算法对每个节点进行连接，分为已知和未知两部分，由已知的推导出未知的部分
###3）也就是父节点和子节点的集合划分，对每一个节点进行判断，判断顺序为业务保障的阶段顺序
###初始父节点为航班属性A，子节点第一个为上轮档x1，
##更新父节点区域为A+x1，子节点为x2
##连接关系为保证该过程构成的子网络bic值最大，也就是最能够解释该网络结构下的值
##增加后的节点除了初始父节点，以外，其他的节点的值均为预测值。！！！这里更新公式需要注意，这里需要用到动态规划的思想，在预测值下面的更新整个概率值。
##依次循环，直到最后一个节点为止，那么各个节点的值均预测出来了
##最后得到的是图结构，
##########################2019-11-08核心代码思路
# A）	互信息计算得到初始的图，并且在选择的时候必须一个farther和一个son，得到一个完备的图
# B）	根据初始的图，判断节点顺序order
# C）	Bic评价值的函数计算
# D）	动态规划算法，节点的构造下逐步迭代算法
# E）	输出最终的结果。
##计算互信息，利用置信度进行转化？
##变量离散化处理
#构造的图需要有子节点和父节点

###最大似然估计变量的参数sitar


import pandas as pd
import matplotlib.pyplot as plt
import itertools
from math import log
#构造图的一个类
class Graph:
    def __init__(self,data=None,nodes=None,edges=None,probs_all=None,bic=None):
        """
        :param nodes:排好序以后的节点
        :param edges: 节点里面的边的连接
        :param probs: 各种节点组合下的概率分布,所有组合下的分布
        """
        self.data=data
        self.nodes=nodes
        self.edges=edges
        self.probs_all=probs_all
        self.bic=bic
    def add_node(self,node):
        self.nodes.append(node)
    def add_edges(self,edge):
        self.edges.append(edge)
    #节点的顺序很重要，是决定最后预测结构的重要因素
    def update_nodes(self,ordered_node):
        self.nodes=ordered_node
    def delete_edge(self,edge):
        self.edges.remove(edge)
    def update_bic(self,bic_value):
        self.bic=bic_value
    #找到每个节点的farther
    def find_farther(self,node):
        pass
    #找到每个节点的son
    def find_son(self,node):
        pass

class X_Node(object):
    def __init__(self,name,farther,son,order,farther_node_list,son_node_list):
        self.name = name
        self.farther = farther
        self.son = son
        self.order = order
        self.farther_node_list =farther_node_list
        self.son_node_list =son_node_list
    def update_farthernode_list(self,farther_node_list):
        self.farther_node_list =farther_node_list
    def update_son_node_list(self,son_node_list):
        self.son_node_list =son_node_list
    def update_order(self,order):
        self.order = order
    def update_farther(self,farther):
        self.farther = farther
    def update_son(self,son):
        self.son = son

##第一步输入初始的节点顺序
#需要输入的数据为：节点、父节点的order为0，子节点的order初始为-1，
#最开始是没有farther和son的
#需要根据顺序去制定farther_node_list和son_node_list

##第二步为每一个节点寻找farther和son
##从farther_node_list 和 son_node_list 里面去选

##第三步更新节点顺序，最好用字典来表示{1:[],2:[],3:[],4:[]} 每一个list也包含了内在的顺序
##更新节点的父节点和子节点

##按照阶段来进行选择连接方式，此处需要一个循环，并计算最大的bic值
###得到新的连接结果，并输出graph

X1=X_Node(name="x1",farther=None,son=None,order=1,farther_node_list=None,son_node_list=None)




#######################2019-11-18################
###贝叶斯网络结构训练核心步骤
###1 构建节点，输入初始的节点信息
###2  根据节点得到初始的graph，保存初始的节点顺序信息 得到graph1，以及farther_list 和 son_list
###3  根据顺序信息和互相关信息来update节点信息，并加入了edge信息到graph中去得到graph2
###4  根据graph2 的edge信息来更新graph2 的节点的order，以及farher_list ，
###5  生成新的graph3 根据graph2的节点顺序信息和 MDI值 来更缩小farther_list和son_list





















"""
x={}
x[1]=2
print(x[1])
data_g=Graph()
data_g.add_node("a")
data_g.add_prop(["abc",{'name':'jinxin','age':18,'male':'男'}])
print(data_g.probs)
"""

#计算各种连接情况下的cpt条件概率表,用一个数组表示
def CPT_all():
    pass


#数据离散化处理 ok
def data_discriter():
    pass



#利用互信息得到第一次的网络连接结构
def first_connect_by_MI():
    pass


#动态规划寻找最优bic值，并得到最优的网络结构********************核心代码
def DAG_dbn():
    pass


#利用训练好的网络结构进行预测
def dbn_predict():
    pass


#可视化当前结构的网络图
def plot_graph():
    pass


#数据离散化并画图展示出来，返回离散化的每个区间大小，针对每一个变量而言进行划分
def classified_plot(data,k):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    d = pd.cut(data_temp, k, labels=range(k))
    plt.figure(figsize=(7,5))
    discrete_list=[]
    for j in range(0, k):
        temp=[]
        plt.plot(data[d==j], [i for i in d[d==j]], 'o')
        temp.append(min(data[d==j]))
        temp.append(max(data[d==j]))
        discrete_list.append(temp)
    plt.show()
    return d,discrete_list


data=pd.read_csv("fishiris.csv")
node_list_all=data.columns.values.tolist()
# print(node_list_all)
#['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth', 'Name']


##测试数据离散化并输出结果
# data_temp=data["SepalWidth"].copy()
# k=4
# cut_temp,cut_list=classified_plot(data_temp,k)
new_data=pd.DataFrame()
# new_data["SepalLength"]=cut_temp
# print(new_data,cut_list)
##得到新的数据new_data
for name in node_list_all[:-1]:
    data_temp=data[name].copy()
    k=5
    cut_temp, cut_list = classified_plot(data_temp, k)
    new_data[name]=cut_temp
    print(cut_list)
# print(new_data)

##根据新的data计算CPT_all 所有的组合的全概率表，返回的样式为字典
##{"组合名称":dataframe}
def cal_all_props(node_list,dataframe):
    pass

##构造字典 名称为表达式P(a,b) 或者P（a|b）
# name="P"+"("+node_list[0]+","+node_list[1]+")"
# print(name)

#要根据节点的分类，得到多种组合效果

##计算条件概率表，输入为{node:value,node:value},node,返回样式为字典
##{"条件概率名称":dataframe}

#统计每个节点的概率分布p(x)以及p（x,y） 输出是一个字典 p（a）:dataframe[a],[p] # p(a,b),dataframe[a],[b],[p]
##计算全概率表和单个变量的概率表用字典表示
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
    print(result_dict)
    return result_dict


node_list=['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth']
all_data=new_data
result_prob_dict=cal_total_and_two_prob_dict(node_list,all_data)

#####计算互信息##
#计算互信息,仅仅限于两个变量之间的互信息
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

mu_value_dict=mutual_information(node_list,all_data,result_prob_dict)

#评价网络模型的bic值,以bic值不在增加为结束条件
##首先i j k 是？
#先计算满足 xi=k 第i个节点的取值为k 的时候，该点父样本集为j （第j中组合）的样本集的数量 m_ijk 然后再 计算所有情况
#也就是mij*的值，xi的取值为所有的时候，的样本集的数量
##最后再循环可得到整个情况下的bic值
##后半部分 减去LOGN 乘以 qi为父节点取值的组合个数，是基于当前数据下的组合个数？更能够反应问题？
##或者是不基于当前数据下，而是将没出现的情况也算进去？


def bic_information(current_node,farther_node_list,all_data):
    """
    :param current_node:第i个节点
    :param farther_node_list: 当前节点的父节点
    :param all_data:所有的数据
    :return:bic值
    """
    N=len(all_data)
    #计算j 和 k 的取值范围以及相应的值 父节点和当前节点取值组合个数
    #mijk数量可以用全概率乘以总数据量来计算计算mijk的字典的表 取出来mijk的值
    m_ijk_list=[node for node in farther_node_list] #加入父节点
    m_ijk_list.append(current_node) #得到所有的组合的一张表，加入子节点，注意顺序，最后一个节点为当前节点，因此前面三个为父节点
    m_ijk_dict=dict(all_data[m_ijk_list].groupby(m_ijk_list).size()) #当前节点的个数
    m_ij_dict=dict(all_data[farther_node_list].groupby(farther_node_list).size())#以父节点进行groupby 然后计算个数
    #计算mij*的表 也即是所有farther的集合的数量
    r_current=len(set(all_data[current_node]))#当前节点的状态的个数 根据节点直接计算
    q_current=len(m_ij_dict.keys())#得到所有父亲的组合以及每个组合的个数，只是统计父节点
    #计算后半部分的减法
    L2=log(N)*q_current*(r_current-1)/2
    L1=0.0
    for one_compare in m_ijk_dict.keys():
        mijk=m_ijk_dict[one_compare]
        mij=m_ij_dict[one_compare[0:-1]]
        L1+=mijk*log(mijk/mij)
    return L1-L2



x=bic_information("SepalLength",['SepalWidth', 'PetalLength', 'PetalWidth'],new_data)
print(x)
##计算一个节点的值


