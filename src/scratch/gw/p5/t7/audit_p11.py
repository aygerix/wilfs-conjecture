"""Final exact P5g output audit; run on fejer only."""
import hashlib
import json
from pathlib import Path
import platform
import re

root=Path('.')
weak=root.joinpath('weak40.log').read_text()
assert 'FAILURES=0' in weak
rows=[tuple(map(int,m)) for m in re.findall(r'n=(\d+) weak=(\d+) strict=(\d+) sf_unique=(\d+)',weak)]
assert rows==[(1,1,1,1),(2,39,39,39),(3,741,722,741),(4,8778,7758,8778),
              (5,65724,45694,65724),(6,270180,111202,232610),
              (7,418384,55550,100904),(8,106904,710,4)]
matching=root.joinpath('matching.log').read_text()
assert 'ALL_MATCHING_CHECKS_PASSED' in matching
matched=[tuple(map(int,m)) for m in re.findall(r'n (\d+) sets (\d+) retained_graph_states (\d+)',matching)]
assert matched==[(2,14,28),(3,91,364),(4,364,3346),(5,998,15426),(6,1683,18820),(7,328,790)]
assert 'ANTIPODAL_EXACT_CHECKS_PASSED' in root.joinpath('antipodal.log').read_text()
assert 'ALL_EXACT_CHECKS_PASSED' in root.joinpath('independent.log').read_text()
instances=[]
for order,expected in [('lex',1484),('grlex',987)]:
    txt=root.joinpath('instances_'+order+'.log').read_text()
    m=re.search(r'trials=(\d+) actual=(\d+)',txt); assert m
    assert int(m[2])==expected
    cores=[]
    for name,count in re.findall(r'P5g_core=([AB]) cores=(\d+).*?FAILURES=0',txt):
        cores.append((name,int(count)))
    assert len(cores)==2
    instances.append(dict(order=order,trials=int(m[1]),actual=int(m[2]),cores=cores))
planted=json.loads(root.joinpath('planted_verified.json').read_text())
assert [(x['n'],x['s'],x['ex'],x['F47']) for x in planted]==[(33,3968,1451,62642),(48,12835,4259,184484)]
assert all(x['heavy_sf_fibres']==1 for x in planted)
weakheavy=json.loads(root.joinpath('weak_heavy_verified.json').read_text())
assert (weakheavy['n'],weakheavy['ex'],weakheavy['heavy_sf_fibres'])==(36,46,1)
paths=sorted([p for p in root.iterdir() if p.suffix in ('.c','.h','.py','.md','.log') and p.name!='P5_REPORT.md'])
paths += [root/'planted_verified.json',root/'weak_heavy_verified.json']
dependencies=[root/'deps'/name for name in ['multi_low.h','two_low.h','instance_checks.h']]
digests={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths+dependencies}
Path('SHA256SUMS').write_text(''.join(h+'  '+str(p)+'\n' for p,h in digests.items()))
report=Path('P5_REPORT.md')
assert all('## '+str(j)+'.' in report.read_text() for j in range(60,68))
out=dict(status='PASS',python=platform.python_version(),
         weak_sets=sum(x[1] for x in rows),strict_sets=sum(x[2] for x in rows),
         matching_states=sum(x[2] for x in matched),instances=instances,
         actual_tiles=sum(x['actual'] for x in instances),planted=planted,
         report_sha256=hashlib.sha256(report.read_bytes()).hexdigest(),
         sha256=digests,
         scope='Full ambient P(C,K) and unrestricted MATCH-P remain open; hypotheses in report sections 60--67.')
Path('AUDIT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:out[k] for k in ['status','weak_sets','strict_sets','matching_states','actual_tiles','report_sha256']},sort_keys=True))
