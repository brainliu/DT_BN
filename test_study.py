#-*- coding:utf-8 -*-
#created by brian
# create time :2019/11/9-17:09 
#location: sichuan chengdu
from thinkbayes import Pmf
pmf=Pmf()
for x in [1,2,3,4,5,6]:
    pmf.Set(x,1/6.0)

ppp=list()
ppp.append(1)
print(ppp)