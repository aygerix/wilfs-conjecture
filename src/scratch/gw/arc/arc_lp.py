# LP lower bound for G = (d+1)(1+3a+2b+c+q3+s3+t3) - 3N - 2(q3+b+c+e+s4+t4) - 2  (primary regime, q2=u3=k=0)
# N = q3+s3+s4+hAC+t3+t4+i+u4+v3+w+z; constraints: shadows/capacities. Report min over (a,b,c,e) grid.
import numpy as np
from scipy.optimize import linprog
names=['q3','u4','s3','s4','hAC','t3','t4','i','v3','w','z']
def G_lp(a,b,c,e):
    d=a+b+c+e; Q=a*(a+1)//2; B=b*(b+1)//2
    # G = const + sum coef*x
    const=(d+1)*(1+3*a+2*b+c) - 2*(b+c+e) - 2
    coef={'q3':(d+1)-3-2,'u4':-3,'s3':(d+1)-3,'s4':-3-2,'hAC':-3,'t3':(d+1)-3,'t4':-3-2,'i':-3,'v3':-3,'w':-3,'z':-3}
    cvec=np.array([coef[n] for n in names],float)
    A=[];bb=[]
    def row(dct,rhs):
        A.append([dct.get(n,0) for n in names]); bb.append(rhs)
    row({'q3':1},Q); row({'u4':3,'q3':-(a+2)},0); row({'s3':1,'s4':1},a*b); row({'hAC':1},a*c)
    row({'t3':1,'t4':1},B); row({'i':1},b*c); row({'v3':1,'q3':-b},0); row({'v3':2,'s3':-(a+1)},0)
    row({'w':1,'t3':-a},0); row({'w':2,'s3':-(b+1)},0); row({'z':3,'t3':-(b+2)},0)
    res=linprog(cvec,A_ub=np.array(A,float),b_ub=np.array(bb,float),bounds=[(0,None)]*len(names),method='highs')
    return const+res.fun, dict(zip(names,np.round(res.x,2)))
worst=[]
for a in range(0,31):
  for b in range(0,21):
    for c in range(0,8):
      for e in range(0,8):
        if a+b+c+e<1: continue
        g,x=G_lp(a,b,c,e)
        worst.append((g,a,b,c,e,x))
worst.sort(key=lambda t:t[0])
print("negative count:",sum(1 for w in worst if w[0]<0),"of",len(worst))
for w in worst[:15]: print(round(w[0],2),w[1:5],w[5])
