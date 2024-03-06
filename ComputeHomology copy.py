"""
目的是编写一个程序, 手动属于一个抽象链群, 并定义链映射, 可以计算出链群所对应的上同调群
"""
#定义群元素, 由两部分构成, sign表示符号, 取值为±1, st是元素, 用字符串形式写出
class elem(object):
    def __init__(self,sign,st):
        self.sign=sign 
        self.st=st

#定义链群
"""
class chain_group(object):
    def __init__(self,dim,e):
        self.e=e      #用list的形式记录链群, list中的元素都是elem
        self.dim=dim  #同调群维数
"""

from sympy import *
from sympy.matrices.normalforms import hermite_normal_form
from sympy.matrices.normalforms import smith_normal_form

#定义边缘映射, 对于特定元素计算其边缘, 输出结果为一个list
def ComputeBound(ele):
    result=[]
    for i in range(0,len(ele.st)):
        tt=ele.st
        del tt[i]
        temp=elem(ele.sign*((-1)**i),tt)
        result.insert(i+1,temp) 
    return result

#输出边缘映射矩阵群, 输入元素group均为list, list中的元素为elem类
def BoundMatrix(group1,group2):
    result=zeros(len(group1),len(group2))
    for i in range(len(group1)):
        bound=ComputeBound(group1[i])
        for j in range(len(bound)):
            for k in range(0,len(group2)):
                #print(bound[j].st, group2[k].st)
                if bound[j].st== group2[k].st:
                    result[i,k]=bound[j].sign * group2[k].sign
                    #print(result[i,k])
    return result

def BTnum(M):
    count=0
    zero=0
    j=0
    tor=[]
    cy=0
    for i in range(shape(M)[0]):
        if M[i,i]!=0:
            count=count+1
            if abs(M[i,i])==1:
                zero=zero+1
            else:
                j=j+1
                tor.insert(abs(M[i,i]))
        else: 
            break 
    return [shape(M)[0]-count, zero , tor]

from InvNum import InvNum

def main():
    dim=2
    g2=['abf','adf','cdf','cbf','abe','ade','cbe','cde']
    g1=['ab','ad','af','ae','cb','cd','cf','ce','bf','be','df','de']
    g0=['a','b','c','d','e','f']
    g=[g0,g1,g2]
    G=[]
    for i in range(len(g)):
        temp=[]
        for j in range(len(g[i])): 
            a=InvNum(g[i][j])
            temp.insert(j+1, elem(a[1],a[0]))
            #print(temp[0].st)
        G=G+[temp]

    """
    for i in range(len(G)):
        for j in range(len(G[i])):
            print(G[i][j].sign, G[i][j].st)
    """
    fina=[]
    for i in range(dim): 
        m=BoundMatrix(G[dim-i],G[dim-i-1])
        ans=BTnum(smith_normal_form(m))
        fina.insert(i+1,ans)
    
    fina.insert(dim,[len(g0),0,[]])
    
    res=fina  
    for i in range(len(fina)-1):
        res[i+1][0]=res[i+1][0]-res[i][1]
        res[i+1][2]=res[i][2]
    for i in range(len(fina)): 
        del res[i][1]
    print(res)

import time 
if __name__ == '__main__':
    #star=time.time()
    main()
    #end=time.time()
    #t=end-star 
    #print(t)
