"""All height-3 cores in <=2 variables, plus arbitrary spikes.
The large-m proof is in P6_REPORT. Here check every m<14 exactly.
"""
from itertools import combinations_with_replacement,product
from math import comb
from pathlib import Path
import json

rows=[];named=[]
for k in (1,2):
    z=(0,)*k;E=[tuple(int(i==j) for i in range(k)) for j in range(k)]
    def vec(T):return tuple(T.count(a) for a in range(k))
    P=[vec(T) for T in combinations_with_replacement(range(k),2)]
    T=[vec(t) for t in combinations_with_replacement(range(k),3)]
    for pm in range(1<<len(P)):
        Q=[P[j] for j in range(len(P)) if pm>>j&1]
        if any(not any(q[a] for q in Q) for a in range(k)):continue
        eligible=[t for t in T if all(tuple(t[b]-(b==a) for b in range(k)) in Q for a in range(k) if t[a])]
        for tm in range(1,1<<len(eligible)):
            cubes=[eligible[j] for j in range(len(eligible)) if tm>>j&1]
            C={z,*E,*Q,*cubes};N={x for x in C if any(tuple(x[b]+(b==a) for b in range(k)) in C for a in range(k))};A=C-N
            p2=sum(sum(x)==2 for x in N);q=len(Q);t=len(cubes)
            c=comb(len(N),2);B=q-p2+2*t
            assert c>B
            threshold=(c*(q+t)-B+c-B-1)//(c-B)
            assert threshold<=14
            for m in range(len(C),14):
                count=0;mn=None
                for p in product(range(1,m),repeat=k):
                    ph={x:sum(a*b for a,b in zip(x,p))%m for x in C}
                    if len(set(ph.values()))!=len(C):continue
                    d=k+m-len(C)
                    for sig in range(m):
                        r={x:(ph[x]-sig)%m for x in C}
                        s=(d+1)*sum(r[x] for x in N)-sum((sum(x)-1)*r[x] for x in A)
                        assert s>=0,dict(k=k,m=m,p=p,sigma=sig,C=sorted(C),slack=s)
                        count+=1;mn=s if mn is None else min(mn,s)
                rows.append(dict(k=k,core=sorted(C),m=m,pairs=q,cubics=t,nonmaxpairs=p2,large_m_threshold=threshold,sigma_pairs=count,min_slack=mn))
print('CORE2',json.dumps(dict(rows=len(rows),sigma_pairs=sum(x['sigma_pairs'] for x in rows),max_threshold=max(x['large_m_threshold'] for x in rows)),sort_keys=True))
Path('core2.json').write_text(json.dumps(rows,indent=2)+'\n')
# Named E51: Delta_3 in two directions, plus spikes on complement residues.
C={t for x in range(4) for y in range(4-x) for t in [(x,y)]}
for pc in ((5,6),(8,9)):
    m=14;ph={x:sum(a*b for a,b in zip(x,pc))%m for x in C};assert len(set(ph.values()))==10
    missing=sorted(set(range(m))-set(ph.values()))
    N={x for x in C if sum(x)<3};A=C-N;d=6
    vals=[]
    for sig in range(m):
        r={x:(ph[x]-sig)%m for x in C}
        vals.append((d+1)*sum(r[x] for x in N)-2*sum(r[x] for x in A))
    assert min(vals)>=0
    entry=dict(core_weights=pc,spike_weights=missing,slacks=vals,min_slack=min(vals))
    print('NAMED_CORE_SPIKES',json.dumps(entry,sort_keys=True));named.append(entry)
Path('core2_named.json').write_text(json.dumps(named,indent=2)+'\n')
print('CORE2_ALL_PASS')
