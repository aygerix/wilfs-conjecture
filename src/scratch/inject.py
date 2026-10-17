# Search for a natural injection gaps -> good triples (a, v, k): v in [c, c+n_a), 1<=k<=x(v)_a.
# Candidate maps (each injective for fixed a since gamma is recoverable from (a,v,k)):
#  C1: v = c + (g mod n_a), k = g//n_a + 1
#  C2: v = c + n_a-1 - (g mod n_a), k = g//n_a + 1
#  C3: v = c + (g mod n_a), k = (F-g)//n_a + 1     (not nec. injective)
# Report: #semigroups where some gap has no valid direction under each candidate.
import sys
sys.path.insert(0,'src')
from ns import all_by_genus
from cl import factorizations_down_set
G=int(sys.argv[1])
bad={'C1':0,'C2':0}; tot=0; ex={}
for gen,s in all_by_genus(G):
    if s.m==1: continue
    tot+=1
    m=s.m; c=s.c; F=c-1
    Pp,best=factorizations_down_set(s,'grlex')
    d=len(Pp)
    cell={w%m:n for w,n in best.items()}
    gaps=[x for x in range(1,c) if x not in s]
    for name in ('C1','C2'):
        ok=True
        for gm in gaps:
            found=False
            for a,na in enumerate(Pp):
                r=gm%na; k=gm//na+1
                v = c+r if name=='C1' else c+na-1-r
                if k<=cell[v%m][a]: found=True; break
            if not found: ok=False; break
        if not ok:
            bad[name]+=1
            if name not in ex: ex[name]=(sorted(s.P),gm)
print('semigroups',tot,'failing',bad,ex)
