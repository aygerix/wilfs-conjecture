# Joint LP: W = (d+1)(ell-4) - 4N + rho, ell-4 = 3a+2b+c+q3+s3+t3 (q2=u3=k=0),
# rho >= t3+i+v3+w+z (joint short-residue lemma), rho >= m-2(q3+b+c+e+s4+t4)-2 (refined arc), m=1+d+N.
import numpy as np, sys
from scipy.optimize import linprog
names=['q3','u4','s3','s4','hAC','t3','t4','i','v3','w','z','rho']
def W_lp(a,b,c,e):
    d=a+b+c+e; Q=a*(a+1)//2; B=b*(b+1)//2
    Ncoef={'q3':1,'u4':1,'s3':1,'s4':1,'hAC':1,'t3':1,'t4':1,'i':1,'v3':1,'w':1,'z':1}
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
    # rho >= t3+i+v3+w+z  ->  t3+i+v3+w+z-rho <= 0
    row({'t3':1,'i':1,'v3':1,'w':1,'z':1,'rho':-1},0)
    # rho >= 1+d+N - 2(q3+s4+t4) - 2(b+c+e) - 2  -> N -2q3-2s4-2t4 - rho <= -(1+d) + 2(b+c+e) + 2
    dct={n:1 for n in Ncoef}; dct['q3']-=2; dct['s4']-=2; dct['t4']-=2; dct['rho']=-1
    row(dct,-(1+d)+2*(b+c+e)+2)
    res=linprog(cvec,A_ub=np.array(A,float),b_ub=np.array(bb,float),bounds=[(0,None)]*len(names),method='highs')
    return const+res.fun, dict(zip(names,np.round(res.x,2)))
amax=int(sys.argv[1]) if len(sys.argv)>1 else 30
out=[]
for a in range(0,amax+1):
  for b in range(0,21):
    for c in range(0,8):
      for e in range(0,8):
        if a+b+c+e<1: continue
        g,x=W_lp(a,b,c,e); out.append((g,a,b,c,e,x))
out.sort(key=lambda t:t[0])
neg=[o for o in out if o[0]<-1e-9]
print("negative:",len(neg),"of",len(out))
import collections
print("negative by a:",sorted(collections.Counter(o[1] for o in neg).items()))
for o in out[:12]: print(round(o[0],2),o[1:5],{k:v for k,v in o[5].items() if abs(v)>1e-9})
