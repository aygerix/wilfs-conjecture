"""Independent literal-chain checks. Run only on fejer in ~/wilf/p13."""
import json,re
from collections import Counter
from pathlib import Path
from check import apery,evaluate

stats=Counter();named={};min_slack=None
def test(g,tag):
 global min_slack
 z=evaluate(apery(g));s=z['summary']
 assert s['q']==4,(tag,s)
 assert min(s['CU_slack'],s['PLUS_slack'],s['POOR_slack'])>=0,(tag,z)
 stats['instances']+=1
 for name,key in [('A-OVERLAP','overlap_payment_slack'),('SHADOW-OVERLAP','shadow_payment_slack'),('TOP-STRONG','TOP_strong_slack')]:
  if s[key]>=0:stats[name]+=1
 if s['R_A']<=s['MF']:stats['OVERLAP-MAJORITY']+=1
 if 2*s['MF']>=s['m']-s['e']:stats['MF-HALF']+=1
 if s['a'] and 2*(s['a']+2)*s['MF']>=(s['a']-1)*(s['m']-s['e']):stats['MF-SHADOW']+=1
 if s['a']>=19 and s['alpha']>=6 and 3*s['e']<s['m']:stats['coarse-P11-residual']+=1
 if min_slack is None or s['TOP_strong_slack']<min_slack[0]:min_slack=(s['TOP_strong_slack'],tag)
 return z

named['chain53-outside-q4']=evaluate(apery([53]+list(range(85,96))))
assert named['chain53-outside-q4']['summary']['q']==5
for tag,g in [('rest32',[32]+list(range(39,46))),
              ('Sk17',[87]+list(range(105,123))),('uf5',[5,9,12]),('local8',[8,10,11,12])]:
 z=test(g,tag);named[tag]=z
for k in range(1,41):
 g=[5*k+2]+list(range(6*k+3,7*k+4));z=test(g,f'Sk{k}')
 expected={0}|set(range(6*k+3,7*k+4))|set(range(12*k+6,14*k+7))|set(range(19*k+9,20*k+8))|set(range(20*k+9,21*k+9))
 assert set(z['apery_by_residue'])==expected
 if k>=2:assert z['summary']['Ucrit']<=5
 stats['Sk']+=1
for r in range(1,9):
 for k in range(3*r+1,max(31,3*r+11)):
  m=5*k+2;g=[m]+list(range(m+1,m+r+1))+list(range(6*k+3,7*k+4))
  z=test(g,f'Skr{k},{r}');assert z['summary']['Ucrit']<=5
  expected={0}|set(range(6*k+3,7*k+4))|set(range(12*k+6,14*k+7))|set(range(19*k+9,20*k+8))|set(range(20*k+9,21*k+9))
  for j in range(1,3*r+1):
   expected.remove(4*m+j)
   expected.add(m+j if j<=r else 2*m+j if j<=2*r else 3*m+j)
  assert set(z['apery_by_residue'])==expected
  stats['Skr']+=1
for k in [105,109,125,201,501]:
 m=5*k+2;h=k+1;first=(h+1)//2
 while first%4!=2:first+=1
 g=[m]+[m+2+4*j for j in range(6)]+[m+first+4*j for j in range(13)]+list(range(m+k+1,m+2*k+2))
 z=test(g,f'shaped{k}')
 assert z['summary']['a']==19 and z['summary']['alpha']==6 and 3*z['summary']['e']<m
 named[f'shaped{k}']=z['summary'];stats['shaped-seeds']+=1
for m in range(2,41):
 z=test([m]+list(range(4*m+1,5*m)),f'T{m},4')
 assert all(z['summary'][s]==0 for s in ['W','CU_slack','PLUS_slack','POOR_slack'])
 stats['Tmq']+=1

# Recompute the final best witness in each C adversarial log from its generators.
for log in ['anneal_cu61.log','anneal_poor87.log','anneal_plus211.log','anneal_top61.log','anneal_top127.log','gensearch101.log','anneal_shaped527.log']:
 if not Path(log).exists():continue
 lines=[s for s in Path(log).read_text().splitlines() if ' gens=[' in s]
 if not lines:continue
 line=lines[-1];g=list(map(int,re.search(r'gens=\[([^]]+)\]',line).group(1).split(',')))
 z=test(g,log)
 assert z['apery_by_residue']==list(map(int,re.search(r'Ap=\[([^]]+)\]',line).group(1).split(',')))
 for ckey,pkey in [('W','W'),('CU','CU_slack'),('POOR','POOR_slack'),('PLUS','PLUS_slack'),('E','E'),('Eu','Eu'),('Bc','Bc'),('Ltop','Ltop')]:
  assert int(re.search(r'\b'+ckey+r'=(-?\d+)',line).group(1))==z['summary'][pkey],(log,ckey)
 named[log]=z['summary'];stats['anneal-witnesses']+=1
Path('case_checks.json').write_text(json.dumps(dict(stats=stats,min_top=min_slack,named=named),indent=2))
print(json.dumps(dict(stats=stats,min_top=min_slack),sort_keys=True))
