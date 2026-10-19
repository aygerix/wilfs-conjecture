# Joint LP + Macaulay on the B face: sweep t3 (fixed), z <= t3^{<2>} (Macaulay in b variables), z<=Z.
import numpy as np, sys
from math import comb
from scipy.optimize import linprog
def mac(h,j):
    res=0;i=j
    while h>0 and i>0:
        a=i
        while comb(a+1,i)<=h: a+=1
        res+=comb(a+1,i+1); h-=comb(a,i); i-=1
    return res
names=['q3','u4','s3','s4','hAC','t3','t4','i','v3','w','z','rho']
def W_fixed(a,b,c,e,t3fix):
    d=a+b+c+e; Q=a*(a+1)//2; B=b*(b+1)//2
    Ncoef={n:1 for n in names if n!='rho'}
    const=(d+1)*(3*a+2*b+c)
    coef={n:-4*Ncoef.get(n,0) for n in names}
    for n in ['q3','s3','t3']: coef[n]+=(d+1)
    coef['rho']=1
    cvec=np.array([coef[n] for n in names],float)
    A=[];bb=[]
    def row(dct,rhs): A.append([dct.get(n,0) for n in names]); bb.append(rhs)
    row({'q3':1},Q); row({'u4':3,'q3':-(a+2)},0); row({'s3':1,'s4':1},a*b); row({'hAC':1},a*c)
    row({'t3':1,'t4':1},B); row({'i':1},b*c); row({'v3':1,'q3':-b},0); row({'v3':2,'s3':-(a+1)},0)
    row({'w':1,'t3':-a},0); row({'w':2,'s3':-(b+1)},0); row({'z':3,'t3':-(b+2)},0)
    row({'z':1},min(mac(t3fix,2),comb(b+2,3)))
    row({'t3':1,'i':1,'v3':1,'w':1,'z':1,'rho':-1},0)
    dct={n:1 for n in Ncoef}; dct['q3']-=2; dct['s4']-=2; dct['t4']-=2; dct['rho']=-1
    row(dct,-(1+d)+2*(b+c+e)+2)
    bounds=[(0,None)]*len(names); bounds[names.index('t3')]=(t3fix,t3fix)
    res=linprog(cvec,A_ub=np.array(A,float),b_ub=np.array(bb,float),bounds=bounds,method='highs')
    if res.status!=0: return None
    return const+res.fun
for (a,b) in [(20,80),(20,160),(20,320),(30,320),(50,640),(7,640),(100,1000)]:
    B=b*(b+1)//2
    best=None
    grid=sorted(set([int(B*k/200) for k in range(201)]))
    for t3 in grid:
        g=W_fixed(a,b,0,0,t3)
        if g is not None and (best is None or g<best[0]): best=(g,t3)
    print((a,b),'min W with Macaulay = %.1f at t3=%d (B=%d)'%(best[0],best[1],B))
