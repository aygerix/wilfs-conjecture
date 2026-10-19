"""Final reproducibility checks and SHA-256 inventory; fejer only."""
from pathlib import Path
import hashlib,json,platform,re,subprocess
import numpy,scipy

root=Path('.')
py=json.loads(Path('small_counts.log').read_text().splitlines()[-1])
assert py['survivors']==0 and py['unbounded']==0
crows=[]
for line in Path('small_c.log').read_text().splitlines():
    z=re.fullmatch(r'a=(\d+) base=(\d+) u=(\d+) packing_profiles=(\d+) surviving_delta_tuples=(\d+)',line)
    assert z,line
    crows.append(list(map(int,z.groups())))
assert [z[0] for z in crows]==list(range(7,14))
assert all(z[-1]==0 for z in crows)
assert sum(z[1] for z in crows)==py['total']['base']
assert sum(z[2] for z in crows)==py['total']['u']
assert sum(z[3] for z in crows)==py['total']['packing_profiles']
assert json.loads(Path('small_survivors.json').read_text())==[]
assert json.loads(Path('small_unbounded.json').read_text())==[]
joint=json.loads(Path('joint_profiles_survivors.json').read_text())
assert len(joint)==11 and sum(z['delta'][1]-z['delta'][0]+1 for z in joint)==101
assert all(z['partial_lower']>z['joint_span_max'] for z in joint)
assert all(z['cold_lower']>=0 for z in joint)
ids=json.loads(Path('uniform_identities.log').read_text().splitlines()[-1])
assert json.loads(Path('uniform_polys.log').read_text().splitlines()[-1])['global_certificate_verified']
fam=json.loads(Path('fiber_family.json').read_text())
assert len(fam)==11 and all(z['H']-z['signed_union']==z['loss'] for z in fam)
controls=[]
for name in ('uniform_final4.log','uniform_final6.log','uniform_mix.log'):
    data=Path(name).read_text()
    prim=re.search(r'P7 primary=(\d+)',data)
    jointn=re.search(r'NEW joint=(\d+) cold_fix=(\d+) missing_pair_packing=(\d+)',data)
    assert prim and jointn,name
    controls.append(dict(file=name,primary=int(prim[1]),joint=int(jointn[1]),cold=int(jointn[2]),psp=int(jointn[3])))
files=set()
for pattern in ('*.py','*.c','*.h','*.log'):
    files.update(root.glob(pattern))
files.update(Path(x) for x in ('fiber_family.json','joint_profiles_survivors.json','small_survivors.json','small_unbounded.json','P5_REPORT.md'))
def artifact_path(p):
    if p.name=='P5_REPORT.md':return '../P5_REPORT.md'
    if p.suffix=='.log':return 'logs/'+p.name
    return str(p)
inventory={artifact_path(p):dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(files)}
manifest=dict(versions=dict(python=platform.python_version(),numpy=numpy.__version__,scipy=scipy.__version__,gcc=subprocess.check_output(['gcc','-dumpfullversion'],text=True).strip()),
    finite_rows=crows,finite_totals=py['total'],joint_survivors=len(joint),joint_expanded=101,
    exact_identities=ids['verified'],controls=controls,inventory_paths_relative_to='src/scratch/gw/p5/t4',files=inventory)
Path('MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
Path('SHA256SUMS').write_text(''.join(v['sha256']+'  '+k+'\n' for k,v in inventory.items()))
print(json.dumps({k:v for k,v in manifest.items() if k!='files'}),flush=True)
