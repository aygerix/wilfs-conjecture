"""Exact P5 certificate arithmetic; execute on fejer only."""
from fractions import Fraction as F
from collections import defaultdict
from math import comb

class P:
    def __init__(self, d=0):
        self.d = d.d.copy() if isinstance(d,P) else (d.copy() if isinstance(d,dict) else {(0,0):F(d)})
        self.d={k:F(v) for k,v in self.d.items() if v}
    def __add__(s,o):
        r=defaultdict(F,s.d)
        for k,v in P(o).d.items():r[k]+=v
        return P(dict(r))
    __radd__=__add__
    def __neg__(s):return P({k:-v for k,v in s.d.items()})
    def __sub__(s,o):return s+-P(o)
    def __rsub__(s,o):return P(o)+-s
    def __mul__(s,o):
        r=defaultdict(F)
        for (i,j),v in s.d.items():
            for (k,l),w in P(o).d.items():r[i+k,j+l]+=v*w
        return P(dict(r))
    __rmul__=__mul__
    def __truediv__(s,o):return s*F(1,o)
    def __pow__(s,n):
        r=P(1)
        for _ in range(n):r=r*s
        return r
    def subst(s,a,b):return sum((v*a**i*b**j for (i,j),v in s.d.items()),P())
    def val(s,a,b):return sum(v*a**i*b**j for (i,j),v in s.d.items())

a=P({(1,0):1});b=P({(0,1):1})
B=b*(b+1)/2
C0=3*a*(a+1)+a*b
W0=(a-1)*(b+1)
Ca=a*(a+1)*(a-1)/6
H=B+a*b-3*a*(a+1)
poly=6*(2*B**2*(C0-W0)-(2*b+1)*H*(C0+Ca))

if __name__=='__main__':
    for amin,boff in [(7,2),(3,6),(1,8),(1,2),(2,4),(3,2)]:
        shifted=poly.subst(a+amin,a+amin+b+boff)
        neg={k:str(v) for k,v in shifted.d.items() if v<0}
        print('shift a>=',amin,'b>=a+',boff,'negative coefficients',neg,flush=True)
        if not neg:
            print('coefficients',sorted((k,str(v)) for k,v in shifted.d.items()),flush=True)
    bad=[]
    for ai in range(1,201):
        for bi in range(ai+2,1001):
            if poly.val(ai,bi)<0:bad.append((ai,bi))
    print('bad sufficient curvature condition:',bad[:20],len(bad),flush=True)
