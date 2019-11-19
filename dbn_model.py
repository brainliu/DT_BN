#-*-coding:utf8-*-
#user:brian
#created_at:2019/11/11 12:03
# file: dbn_model.py

#处理数据离散化并赋值标签，采用等距离散化的方式
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
##第一步计算变量与T之间的mi值，存储到dict中
##第二步设定虚拟变量并计算虚拟变量的值
##第三步构建贝叶斯网络并计算cpt条件概率值，输出cpt的概率分分布
##第四部构建贝叶斯网络模型并画图
##第四步预测模型构建，并输出预测精度
