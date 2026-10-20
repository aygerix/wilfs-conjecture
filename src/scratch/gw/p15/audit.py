"""Audit finite counts and independent family C outputs. Fejer only."""
import re,json
from pathlib import Path
out={}
for dim in [2,3]:
 lines=Path('exhaust'+str(dim)+'.log').read_text().splitlines()
 data=[]
 for ln in lines:
  if not ln.startswith('SUMMARY'):continue
  z={k:int(v) for k,v in re.findall(r'(\w+)=(\d+)',ln)};data.append(z)
 assert all(z['badshifts']==0 for z in data if z['m']<=12)
 assert next(z for z in data if z['m']==13)['badshifts']>0
 out['dimension'+str(dim)]=dict(rows=data,total_injective=sum(z['injective'] for z in data),total_shifts=sum(z['shifts'] for z in data),prefix12_injective=sum(z['injective'] for z in data if z['m']<=12),prefix12_shifts=sum(z['shifts'] for z in data if z['m']<=12))
families=json.loads(Path('families.json').read_text())
for z in families:
 log=Path('families',z['tag']+'_C.log').read_text()
 first=next(ln for ln in log.splitlines() if ln.startswith('VERIFIED'))
 got={k:int(v) for k,v in re.findall(r'(\w+)=(-?\d+)',first)}
 for key in ['m','e','M','c','pstar','ell','W']:assert got[key]==z[key],(z['tag'],key)
 assert got['Lambda']==z['spikes']*(z['ell']-z['M']//z['m'])
 true=next(ln for ln in log.splitlines() if ln.endswith(' TRUE'))
 got={k:int(v) for k,v in re.findall(r'(\w+)=(-?\d+)',true)}
 for key in ['sumK','bound','excess']:assert got[key]==z[key]
out['verified_semigroup_families']=len(families)
Path('audit.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,sort_keys=True))
