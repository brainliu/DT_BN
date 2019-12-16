#-*- coding:utf-8 -*-
#created by brian
# create time :2019/12/16-22:52 
#location: sichuan chengdu
#python算法教程书上4.4 p82页
M=[2,2,0,5,3,5,7,4] #表示映射关系
#寻找最大排列问题的递归算法朴素解决方案
def native_max_perms(M,A=None):
    if A is None:
        A=set(range(len(M)))
    if len(A)==1: return A #如果只有一个可选的，那就返回结果
    B=set(M[i] for i in A) ##这里很关键，从集合A中去寻找需要排出的集合B
    C=A-B #排除这些元素
    if C:
        A.remove(C.pop())
        return native_max_perms(M,A)
    return A
x=native_max_perms(M)
print(x)

#引入计数器
def max_perm(M):
    n=len(M)      #how many elements?
    A=set(range(n)) # A={0,1,...,n-1}
    count=[0]*n        #C[i]==0 for i in A
    for i in M:       #all that are pointed to
        count[i]+=1   # increment "point count"
    Q=[i for i in A if count[i]==0] #useless elements
    while Q:                 # while useless elts. lest...
        i=Q.pop()        # get one
        A.remove(i)      # remove it
        j=M[i]           # who is pointing to?
        count[j]-=1      # not anymore
        if count[j]==0:  # is J useless now?
            Q.append(j)  # then deal w/it next
    return A             # return the useful elts.=t

y=max_perm(M)
print(y)
