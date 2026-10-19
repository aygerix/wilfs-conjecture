# GW-27 in down-set form, on random residue-complete quadratic down-sets NOT from semigroups
# (arbitrary levels kappa_a >= 0, random pair choice). Checks identity GW-27a and dl >= g.
import random, sys
seed=int(sys.argv[1]); T=int(sys.argv[2]); random.seed(seed)
tested=fails=idf=0; minW=None
for t in range(T):
    m=random.randint(3,60); d=random.randint(1,min(m-1,14))
    res=random.sample(range(1,m),d)
    used=set([0]+res); pairs=[]
    cand=[(a,b) for a in range(d) for b in range(a,d)]; random.shuffle(cand)
    for (a,b) in cand:
        s=(res[a]+res[b])%m
        if s not in used: used.add(s); pairs.append((a,b))
    if len(used)<m: continue
    K0=random.randint(0,6)
    kap=[random.randint(0,K0) for _ in range(d)]
    n=[kap[a]*m+res[a] for a in range(d)]
    if min(n)<=0: continue
    vals=[0]+n+[n[a]+n[b] for (a,b) in pairs]
    M=max(vals); mu=M%m; K=M//m
    lam=lambda v:(M-v)//m
    l=sum(lam(v) for v in vals); g=sum(v//m for v in vals); W=d*l-g
    deg=[0]*d; sc=0
    for (a,b) in pairs:
        deg[a]+=1; deg[b]+=1; x=n[a]+n[b]; lx=lam(x); ex=(M-x)%m
        gam=int(res[a]+res[b]>=m); bet=int(ex+res[a]>=m)+int(ex+res[b]>=m)
        sc+=(d+2)*lx+bet-gam
    F=sum((d+1-deg[a])*lam(n[a]) for a in range(d)); Dhi=sum(1 for a in range(d) if res[a]>mu)
    if W!=F+Dhi+sc: idf+=1
    tested+=1
    if W<0: fails+=1; print("FAIL",m,n,pairs)
    if minW is None or W<minW: minW=W
print(f"seed={seed} tested={tested} identity_fail={idf} W<0: {fails} minW={minW}")
