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


import pandas as pd
#构造图的一个类
class Graph:
    def __init__(self,nodes=[],edges=[],probs={},bic=None):
        """
        :param nodes:排好序以后的节点
        :param edges: 节点里面的边的连接
        :param probs: 各种节点组合下的概率分布,所有组合下的分布
        """
        self.nodes=nodes
        self.edges=edges
        self.probs=probs
        self.bic=bic
    def add_node(self,node):
        self.nodes.append(node)
    def add_edges(self,edge):
        self.edges.append(edge)
    def add_prop(self,prob_list):
        self.probs[prob_list[0]]=prob_list[1]
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

#评价网络模型的bic值,以bic值不在增加为结束条件
def bic_information():
    pass
#数据离散化处理
def data_discriter():
    pass

#计算互信息
def mutual_information():
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






