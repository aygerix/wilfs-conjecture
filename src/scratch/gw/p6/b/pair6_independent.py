"""Independent set-based prefix enumeration of the k=6 full pair bases.
Only m=43..45, the last base of THREE-CUBICS. fejer only.
"""
from itertools import combinations_with_replacement as cwr
from pathlib import Path
import json

rows=[]
for m in (43,44,45):
    count=0;nodes=0
    def dfs(P):
        global count,nodes
        nodes+=1
        if len(P)==6:count+=1;return
        start=P[-1]+1 if P else 1
        for x in range(start,m-(5-len(P))):
            PP=P+(x,)
            values=[0,*PP,*[(a+b)%m for a,b in cwr(PP,2)]]
            if len(set(values))==len(values):dfs(PP)
    dfs(())
    assert count==0,(m,count)
    row=dict(m=m,bases=count,nodes=nodes);rows.append(row)
    print('PAIR6_INDEPENDENT',json.dumps(row,sort_keys=True),flush=True)
Path('pair6_independent.json').write_text(json.dumps(rows,indent=2)+'\n')
print('PAIR6_INDEPENDENT_PASS')
