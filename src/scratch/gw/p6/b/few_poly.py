"""Exact window certificates for 1,2,3 cubics over a full pair face. fejer."""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json

def shift(p,A):return [sum(p[j]*comb(j,i)*A**(j-i) for j in range(i,len(p))) for i in range(len(p))]
out={}
for t,p,coef,A in [(2,2,[8,-18,-25,-2,1],7),(3,3,[12,-24,-35,-2,1],8)]:
    cf=shift(coef,A);assert all(x>0 for x in cf)
    for k in range(3,201):
        C=F(k*(k-1),2);m=k*k+k+1;s=C-t
        lower=s*C+(k+s+2)*comb(p,2)-3*t*(m-1)+t*(t-1)
        assert lower*4==sum(c*k**j for j,c in enumerate(coef))
    out[str(t)]=dict(p=p,poly4=coef,shift=A,coeff4=cf)
    print('FEW_POLY',t,json.dumps(out[str(t)],sort_keys=True))
small=[]
for t,p,ks in [(1,2,[4]),(2,3,[4,5,6]),(3,3,[4,5,6,7]),(4,4,[4])]:
    for k in ks:
        q=comb(k+1,2);a=q-p;J=comb(1+k+p,2);B=a+2*t;m=k*k+k+1
        R=(m-q-t)*J-B*(m-1)+t*(t-1)+a*t+a*(a-1)//2
        assert R>=0,(k,t,p,m,R);small.append(dict(k=k,t=t,p=p,m=m,CR=R))
print('FEW_SMALL_CR',json.dumps(small,sort_keys=True));out['small']=small
Path('few_poly.json').write_text(json.dumps(out,indent=2)+'\n')
print('FEW_POLY_ALL_PASS')
