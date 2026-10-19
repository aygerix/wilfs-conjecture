"""Independent small base for H3-CORE3. fejer only, exact integers.
Two canonical shapes from the paper CR classification. ALL ordered residues.
Direct down-set maximality; no pair-union calculation or phase recurrence.
"""
from itertools import combinations_with_replacement,permutations
from pathlib import Path
import json

def vector(multi):return tuple(multi.count(a) for a in range(3))
Z=(0,0,0);E=[vector((a,)) for a in range(3)]
Q=[vector(t) for t in combinations_with_replacement(range(3),2)]
families=[('PURE',[(3,0,0)],[14,15]),
          ('BINARY',[vector(t) for t in combinations_with_replacement(range(2),3)],[17])]
rows=[]
for name,T,ms in families:
    C={Z,*E,*Q,*T}
    N={x for x in C if any(tuple(x[b]+(b==a) for b in range(3)) in C for a in range(3))}
    A=C-N
    for m in ms:
        d=3+m-len(C);count=0;phases=0;mn=None;witness=None
        for P in permutations(range(1,m),3):
            lab={x:sum(x[a]*P[a] for a in range(3))%m for x in C}
            if len(set(lab.values()))<len(C):continue
            count+=1
            for sig in range(m):
                r={x:(lab[x]-sig)%m for x in C}
                S=(d+1)*sum(r[x] for x in N)-sum((sum(y)-1)*r[y] for y in A)
                phases+=1
                if mn is None or S<mn:mn=S;witness=dict(P=P,sigma=sig)
                assert S>=0,dict(name=name,m=m,P=P,sigma=sig,S=S,C=sorted(C))
        row=dict(name=name,m=m,d=d,core=sorted(C),ordered_injections=count,phases=phases,min_slack=mn,witness=witness)
        rows.append(row);print('CORE3_INDEPENDENT',json.dumps(row,sort_keys=True),flush=True)
Path('core3_independent.json').write_text(json.dumps(rows,indent=2)+'\n')
print('CORE3_INDEPENDENT_PASS',sum(x['ordered_injections'] for x in rows),sum(x['phases'] for x in rows))
