"""Audit P5e artifacts; execute on fejer after all listed jobs finish."""
from pathlib import Path
import re,json,ast,hashlib,subprocess,sys,shutil
root=Path('.')
def rows(path):
    return [tuple(map(int,m)) for m in re.findall(r'a=(\d+) base=(\d+) u=(\d+) packing_profiles=(\d+) surviving_delta_tuples=(\d+)',Path(path).read_text())]
cc=rows('final14_16.log');assert len(cc)==3 and all(r[-1]==0 for r in cc)
py=[]
for line in (Path('python_link/linked_python14_16.log').read_text()+Path('python_bounded16/bounded16.log').read_text()).splitlines():
    j=json.loads(line)
    if 'a' in j:py.append((j['a'],j['base'],j['u'],j['packing_profiles'],j.get('survive',0)))
assert cc==py,(cc,py)
assert json.loads(Path('python_bounded16/bounded16.log').read_text().splitlines()[-1])['survivors']==0
rr=rows('final17.log');assert rr==[(17,16337,29039496,1119332,2197)]
prof=[dict(re.findall(r'(\w+)=(-?\d+)',s)) for s in Path('final17.log').read_text().splitlines() if s.startswith('PROFILE')]
assert len(prof)==4 and sum(int(p['last'])-int(p['first'])+1 for p in prof)==2197
assert rows('erepair17_20.log')==[(17,16337,29039496,1119332,0)]
assert rows('erepair18.log')==[(18,26725,71891624,4008931,151063)]
replays=[]
for a,num in ((16,5),(17,4),(18,90)):
    rj=json.loads(Path(f'replay{a}.json').read_text());assert rj['profile_hulls']==num and rj['surviving_hulls']==0
    replays.append(rj)
graph=Path('cover_graphs.log').read_text();g=[dict((k,int(v)) for k,v in re.findall(r'(\w+)=(-?\d+)',s)) for s in graph.splitlines()]
assert [x['graphs'] for x in g]==[2,8,64,1024,32768,2097152]
b0=[dict((k,int(v)) for k,v in re.findall(r'(\w+)=(-?\d+)',s)) for s in Path('b0_strip.log').read_text().splitlines()]
bp=[ast.literal_eval(s) for s in Path('b0_verify.log').read_text().splitlines()]
assert sum(x['endpoint_intervals'] for x in bp[:-1])==49289
for x,y in zip(b0,bp[:-1]):assert x['alpha']==y['alpha'] and x['checked']==y['endpoint_intervals'] and x['survivors']==y['survivors']==0
assert b0[11]['alpha']==15 and b0[11]['a_first']==44 and b0[11]['first_n']==36 and b0[11]['first_eps']==248
ids=ast.literal_eval(Path('p5e_identities_final.log').read_text().splitlines()[-1]);assert ids['all_checks']==36
actual=[]
for name in ('actual_4','actual_link6','actual_final4','actual_hot5'):
    s=Path(name+'.log').read_text();z=re.search(r'MULTI primary=(\d+)',s);assert z
    assert Path(name+'.err').read_text()==''
    actual.append(dict(log=name+'.log',primary=int(z[1]),p5e=dict((k,int(v)) for k,v in re.findall(r'(\w+)=(\d+)',next(x for x in s.splitlines() if x.startswith('P5E '))))))
mod=[json.loads(s) for s in Path('matching_moduli.log').read_text().splitlines()];assert [s['balanced'] for s in mod]==[2,3,10]
assert 'global_SP' in Path('profile_witness.log').read_text() and Path('profile_witness.log').read_text().count('matching_forced')==3
assert Path('profile_witness.log').read_text().count('E_REPAIR_exclusion')==4
record=dict(finite=cc,python_full_slices=py,a17_pre_E=rr,a17_profiles=prof,replays=replays,graphs=g,graph_total=sum(x['graphs'] for x in g),b0_endpoint_intervals=49289,actual=actual,primary_total=sum(x['primary'] for x in actual),identities=36,ambient_constant='unproved',versions=dict(python=sys.version,gcc=subprocess.check_output(['gcc','--version'],text=True).splitlines()[0]))
Path('AUDIT.json').write_text(json.dumps(record,indent=2)+'\n')
inventory={};paths={}
for p in sorted(root.rglob('*')):
    if not p.is_file() or '__pycache__' in str(p):continue
    if p.name=='P5_REPORT.md':local='../P5_REPORT.md'
    elif p.suffix in ('.log','.err'):local='logs/'+p.name
    elif p.suffix=='.json':local=p.name if p.name=='AUDIT.json' else 'data/'+str(p).replace('/','_')
    elif p.suffix in ('.py','.c','.h','.md'):local=p.name
    else:continue
    inventory[local]=hashlib.sha256(p.read_bytes()).hexdigest()
    paths[local]=p
Path('SHA256SUMS').write_text(''.join(f'{v}  {k}\n' for k,v in inventory.items()))
dest=Path.home()/'wilf'/'p9_export';dest.mkdir(exist_ok=True)
for local,p in paths.items():
    if local.startswith('../'):continue
    target=dest/local;target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(p,target)
    assert hashlib.sha256(target.read_bytes()).hexdigest()==inventory[local]
shutil.copy2('SHA256SUMS',dest/'SHA256SUMS')
print(json.dumps(record,indent=2))
