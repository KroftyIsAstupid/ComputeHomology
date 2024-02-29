"""
定义函数,用来把抽象链复形中的字符串按照字典序排列,并且计算逆序数
"""

def InvNum(stri):
    Inv=0
    S=list(stri)
    for i in range(0,len(stri)-1):
        for j in range(0,len(stri)-1):
            if S[j]>S[j+1]:
                temp=S[j]
                S[j]=S[j+1]
                S[j+1]=temp
                Inv+=1
    stri=''.join(S)
    return [stri,(-1)**Inv]


