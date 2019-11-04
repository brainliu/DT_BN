#-*- coding:utf-8 -*-
#created by brian
# create time :2019/11/4-21:17 
#location: sichuan chengdu
import math
import numpy as numpy
class Cluster:
    def __init__(self,x,y,sample_weight=None,base=2):
        self._x = x.T,self._y = y

