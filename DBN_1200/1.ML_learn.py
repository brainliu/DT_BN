#-*-coding:utf8-*-
#user:brian
#created_at:2019/11/11 9:22
# file: 1.ML_learn.py
##第一步先计算数据的先验概率以及条件概率
##第二步计算互信息，根据互信息选择初始的网络父节点和子节点
##基于搜索评分算法来选择最佳网络结构
##得到最优的网络结构，用于预测,主要建立条件概率表进行预测
import networkx as nx
import matplotlib.pyplot as plt
G = nx.DiGraph(name='my graph')
node_list_all=['p', 'sale', 'collcet', 'cn_add', 'cn_z', 'picture', 'opening_hours', 'hp', 'tk', 'NNN']
target="NNN"
edge_list_first=['cn_add', 'cn_z', 'picture', 'opening_hours']
#(hp,tk,p)--v1  以及 (sale,collect)--V2
edge_list_second=[("hp","v1"),("tk","v1"),("p","v1"),("sale","v2"),("collcet","v2")]
xu_ni_v=["v1","v2"]
edge_list_all=[]
for i in edge_list_first:
    edge_list_all.append((i,target))
for j in xu_ni_v:
    edge_list_all.append((j,target))
G.add_nodes_from(node_list_all)
G.add_edges_from(edge_list_all)
G.add_edges_from(edge_list_second)
nx.draw(G,with_labels=True, edge_color='b', node_color='g', node_size=1000)
plt.savefig("myfigure.pnf")
plt.show()

