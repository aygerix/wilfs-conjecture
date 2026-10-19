"""Independent incremental labeling of the fixed matching shape at m=26.
Uses the matching automorphisms instead of sorted unit sets plus matchings.
Run on fejer only, nice single core.
"""
from collections import Counter
from pathlib import Path
import json
m=26;k=6;missing={(0,1),(2,3),(4,5)}
P=[];used={0};stats=Counter()
def dfs(a):
    stats['depth_'+str(a)]+=1
    if a==6:
        stats['pair_bases']+=1;return
    if a in (1,3,5):start=P[a-1]+1
    elif a==2:start=P[0]+1
    elif a==4:start=P[2]+1
    else:start=1
    for v in range(start,m):
        new=[v,(2*v)%m]
        new.extend((v+P[i])%m for i in range(a) if (i,a) not in missing)
        if len(set(new))<len(new) or any(r in used for r in new):continue
        P.append(v);used.update(new);dfs(a+1)
        P.pop();used.difference_update(new)
dfs(0)
assert stats['pair_bases']==0
Path('matching6_independent.json').write_text(json.dumps(dict(stats),indent=2)+'\n')
print('MATCHING6_INDEPENDENT',dict(stats),flush=True)
