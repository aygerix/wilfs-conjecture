"""P5 experiments. Run only on fejer in ~/wilf/p5."""
from math import comb, isqrt
from fractions import Fraction as F
import sys
import numpy as np
from scipy.optimize import linprog

names = 'q u s S H t T I v w z rho'.split()
rows = 'qcap ushadow scap Hcap tcap Icap vq vs wt ws zt SR ARC zmac'.split()

def mac2(t):
    k = (1+isqrt(1+8*t))//2
    r = t-comb(k,2)
    return comb(k+1,3)+comb(r+1,2)

def lp(a,b,c=0,e=0,tfix=None,condensed=False,qmac=False):
    d=a+b+c+e; Q=comb(a+1,2); B=comb(b+1,2)
    obj=np.array([-4.]*11+[1.])
    obj[[0,2,5]] += d+1
    mat=[]; rhs=[]
    def row(dic,h):
        mat.append([dic.get(n,0) for n in names]);rhs.append(h)
    row({'q':1},Q);row({'u':3,'q':-a-2},0)
    row({'s':1,'S':1},a*b);row({'H':1},a*c)
    row({'t':1,'T':1},B);row({'I':1},b*c)
    row({'v':1,'q':-b},0);row({'v':2,'s':-a-1},0)
    row({'w':1,'t':-a},0);row({'w':2,'s':-b-1},0)
    row({'z':3,'t':-b-2},0)
    row({'t':1,'I':1,'v':1,'w':1,'z':1,'rho':-1},0)
    row(dict(q=-1,u=1,s=1,S=-1,H=1,t=1,T=-1,I=1,v=1,w=1,z=1,rho=-1),1-a+b+c+e)
    bounds=[(0,None)]*12
    if tfix is not None:
        bounds[5]=(tfix,tfix)
        if condensed:
            x=(np.sqrt(8*tfix+1)-1)/2
            row({'z':1},x*(x+1)*(x+2)/6)
        else:row({'z':1},mac2(tfix))
    res=linprog(obj,A_ub=mat,b_ub=rhs,bounds=bounds,method='highs')
    return res.fun+(d+1)*(3*a+2*b+c),res

if __name__=='__main__':
    for a,b in [(2,2),(3,10),(7,20),(20,160),(100,1000)]:
        B=comb(b+1,2)
        for frac in [0,.01,.1,.25,.5,.75,.9,.99,1]:
            t=int(B*frac);W,r=lp(a,b,tfix=t,condensed=True)
            print((a,b,t),round(W,5),'x=',dict(zip(names,np.round(r.x,4))),
                  'dual=',dict((n,str(F(float(-v)).limit_denominator(100000))) for n,v in zip(rows,r.ineqlin.marginals) if abs(v)>1e-7),flush=True)
