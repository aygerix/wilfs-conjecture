"""Audit completed P5f artifacts and hash them, on fejer only."""
from pathlib import Path
from fractions import Fraction
import json,re,hashlib

root=Path('.')
p=json.loads(Path('polynomial_certificates.json').read_text())
assert set(p)=={'base','B','l','matching'}
for v in p.values():
    assert v['checks']==42 and not v['failed_positive_coefficient_test']
    assert len(v['coefficients'])==42
    assert all(Fraction(x)>=0 for a in v['coefficients'].values() for x in a)
heavy=json.loads(Path('heavy_certificates.json').read_text())
assert heavy['checks']==24 and not heavy['failed']
assert all(Fraction(x)>=0 for a in heavy['coefficients'].values() for x in a)
rows=[json.loads(s) for s in Path('scaling_profiles.log').read_text().splitlines()]
assert len(rows)==16
assert {x['N'] for x in rows}=={480,960,1920,3840}
for x in rows:
    assert not x['failed'] and len(x['checks'])==30 and all(x['checks'].values())
    assert x['data']['W_formal']<0
algebra=json.loads(Path('algebra_checks.log').read_text())
assert algebra==dict(B_bound_constants=True,large_A_endpoints=5991,
    macaulay_profiles=4543077,middle_block_profiles=3339578,
    negative_original_lower=1853859)
instances=[]
for fn,expected in [('instances61.log',(2981,2968,2646)),
                    ('instances62.log',(1983,1973,1909))]:
    text=Path(fn).read_text()
    m=re.search(r'P5f instances=(\d+) HPAIR=(\d+) strict_improvements=(\d+) WAneg_a24=(\d+) large_hyp=(\d+)',text)
    assert m
    vals=tuple(map(int,m.groups()));assert vals[:3]==expected and vals[3:]==(0,0)
    instances.append(dict(file=fn,instances=vals[0],HPAIR=vals[1],strict=vals[2]))
assert sum(x['instances'] for x in instances)==4964
out=dict(status='PASS',coefficient_certificates=192,integer_profiles=16,
    predicates_per_integer_profile=30,actual_semigroups=4964,
    HPAIR_cases=4941,HPAIR_strict_improvements=4555,
    algebra=algebra,instances=instances,
    scope='count profiles are not residue-complete or semigroup witnesses')
Path('AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
inventory={}
for name in ['README.md','algebra_checks.py','polynomial_certificates.py',
 'scaling_profiles.py','instance_checks.h','uniform_semigroups.c','audit_p10.py',
 'AUDIT.json']:
    inventory[name]=name
for name in ['algebra_checks.log','polynomial_certificates.log',
 'scaling_profiles.log','preliminary_profiles.log','instances61.log','instances62.log']:
    inventory['logs/'+name]=name
for name in ['polynomial_certificates.json','heavy_certificates.json']:
    inventory['data/'+name]=name
inventory['../P5_REPORT.md']='P5_REPORT.md'
for name in ['frontier_counts.py','multi_low.h','two_low.h']:
    inventory['../t5/'+name]='../p9/'+name
digests=[]
for target,source in sorted(inventory.items()):
    digests.append(hashlib.sha256(Path(source).read_bytes()).hexdigest()+'  '+target)
Path('SHA256SUMS').write_text('\n'.join(digests)+'\n')
print(json.dumps(out,sort_keys=True))
