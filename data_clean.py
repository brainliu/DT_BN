#-*-coding:utf8-*-
#user:brian
#created_at:2019/11/13 8:44
# file: data_clean.py
#location: china chengdu 610000
#处理原始数据
x=([3,2,1],[1,2,6],[7,8,9])
import itertools
for i in itertools.combinations(x,2):
    print(i)
for y in itertools.product(*x):
    print(y[0],y[1],y[2])
