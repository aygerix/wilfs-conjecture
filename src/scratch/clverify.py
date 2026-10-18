# Independent from-scratch check of CL on S = <14,22,23,57,61,62,63> + check of every factorization down-set choice
import sys, itertools
sys.path.insert(0,'src')
from cl import cl_value
from ns import NS
gens=[14,22,23,57,61,62,63]
# brute-force semigroup membership
N=400
inS=[False]*N; inS[0]=True
for x in range(1,N):
    inS[x]=any(x>=g and inS[x-g] for g in gens)
gaps=[x for x in range(N) if not inS[x]]
F=max(gaps); c=F+1; g=len(gaps); m=min(gens)
ell=c-g
mingens=[x for x in gens if not any(inS[x-y] and inS[y] for y in range(1,x))]
e=len(mingens)
print('c',c,'g',g,'ell',ell,'e',e,'mingens',mingens,'W',e*ell-c)
ap=[min(x for x in range(N) if inS[x] and x%m==i) for i in range(m)]
print('Apery',sorted(ap))
s=NS.from_generators(gens)
print('NS: c',s.c,'g',s.g,'e',s.e,'P',s.P)
for o in ['grlex','lex','revlex']:
    lhs,target,dp=cl_value(s,o)
    print(o,'CL lhs',lhs,'target',target,'CL holds' if lhs>=target else 'CL FAILS','depth part',dp)
# all factorizations of each Apery element over the non-m generators
P=[x for x in mingens if x!=m]; d=len(P)
facs={}
for w in ap:
    fs=[]
    def rec(i,rem,cur):
        if i==d:
            if rem==0: fs.append(tuple(cur))
            return
        for k in range(rem//P[i]+1):
            rec(i+1,rem-k*P[i],cur+[k])
    rec(0,w,[])
    facs[w]=fs
print('factorization counts',{w:len(f) for w,f in facs.items() if len(f)>1})
