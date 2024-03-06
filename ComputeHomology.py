"""
目的是编写一个程序, 手动属于一个抽象链群, 并定义链映射, 可以计算出链群所对应的上同调群
"""
import copy
from InvNum import InvNum
from sympy import *
from sympy.matrices.normalforms import hermite_normal_form
from sympy.matrices.normalforms import smith_normal_form
#定义群元素, 由两部分构成, sign表示符号, 取值为±1, st是元素, 用list模式写出
class elem(object):
    def __init__(self,sign,st):
        self.sign=sign 
        self.st=st
#定义边缘映射, 对于特定元素计算其边缘, 输出结果为一个list
def ComputeBound(ele):
    result=[]
    for i in range(0,len(ele.st)):
        s=copy.deepcopy(ele.st)
        sign= ele.sign*((-1)**i)
        
        if s[i]=='e' or s[i]=='f':
            w=2
        else:
            w=1
        """
        if len(s)==2 and (s[0]=='e' or s[1]=='e' or s[0]=='f' or s[1]=='f') and s[i]!='e' and s[i]!='f':
            w=2
        else:
            w=1
        """
        del s[i]
        temp=elem(sign*w,s)
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

def singlecomp(A,B): #一个无序列表和另外一个列表判断是否相等
    a=copy.deepcopy(A)
    b=copy.deepcopy(B)
    if len(a)==len(b):
        while len(a)>0:
            sin=0
            for i in range(0,len(b)):
                if a[0]==b[i]:
                    sin=1
                    del a[0]
                    del b[i]
                    break
            if sin==0:
                return False 
        return True
    else:
        return False
    
def comp(A,B):
    res=False
    for i in range(len(B)):
        res= res or singlecomp(A,B[i])
    return res 
                
def genera(cn):
    line=[]
    po=0
    for i in range(len(cn)): 
        for j in range(len(cn[i])):
            temp=copy.deepcopy(cn[i]) 
            del temp[j]
            if comp(temp,line)==False:
                line.insert(po,temp)
                po=po+1
    return line 

def inpo(C):
    dim=len(C[0])-1
    cn=[] #输入C
    for i in range(len(C)):
        cn.insert(i,list(C[i]))
    G=[]
    G.insert(0,cn)
    for i in range(1,dim+1):
        G.insert(i,genera(G[i-1]))
    G.reverse()
    return G

def Infm(mg):
    g=[]
    for i in range(len(mg)):
        temp1=[]
        for j in range(len(mg[i])):
            temp1.insert(j+1, list(mg[i][j]))
        g.insert(i+1,temp1)
    return g

def outPutSmith(g): #反序输出边缘同态的smith矩阵
    G=[]
    dim=len(g[-1][0])-1
    for i in range(len(g)):
        temp=[]
        for j in range(len(g[i])): 
            a=InvNum(g[i][j])
            temp.insert(j+1, elem(a[1],a[0]))
            #print(temp[0].st)
        G=G+[temp]
    fina=[]
    dim=len(G)-1
    for i in range(dim): 
        m=BoundMatrix(G[dim-i],G[dim-i-1])
        ans=smith_normal_form(m)
        fina.insert(i+1,ans)
    return fina

def outPutNum(G):
    fina=[]
    dim=len(G)
    for i in range(dim): 
        ans=BTnum(G[i])
        fina.insert(i+1,ans)
    return fina

def BTnum(M):
    count=0
    zero=0
    j=0
    tor=[]
    for i in range(min(shape(M)[0],shape(M)[1])):
        if M[i,i]!=0:
            count=count+1
            if abs(M[i,i])==1:
                zero=zero+1
            else:
                j=j+1
                tor.insert(j,abs(M[i,i]))
        else: 
            break 
    return [shape(M)[0]-count, zero , tor]

def Hom(G,p):
    res=outPutNum(G)
    res.insert(len(res),[p,0,[]])
    #print(res)
    for i in range(len(res)-1):
        res[i+1][0]=res[i+1][0]-res[i][1]
        res[-1-i][2]=res[-2-i][2]
    for i in range(len(res)): 
        del res[i][1]
    res[0][1]=[]
    for i in range(len(res)):
        res[i][0]=res[i][0]-len(res[i][1])
    return res

def CoHom(G,n):
    for i in range(len(G)):
        temp=transpose(G[i])
        G[i]=temp
    G.reverse()
    #print(G)
    res=Hom(G,n)
    res.reverse()
    return res

def CompHcoH(C):
    g=Infm(inpo(C))
    G=outPutSmith(g)
    #print(shape(G[0])[1])
    return [Hom(G,len(g[0])), CoHom(G,len(C))]
    
def main():
    C=['abf','adf','cdf','cbf','abe','ade','cbe','cde']
    #C=['abd','ebd','bce','fce','caf','gaf','deg','heg','efh','ifh','fgi','dgi','gha','bha','hib','cib','idc','adc']
    res=CompHcoH(C)
    print(res[0]) 
    print(res[1])
    
if __name__ == '__main__':
    main()
    
