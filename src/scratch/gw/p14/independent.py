"""P14 independent Dijkstra, literal chains, factor counts, graph accounting.
Run on fejer only. check_p13.py is an unchanged copy of P13's Python checker.
"""
import json,math,itertools,random,re
from pathlib import Path
from collections import Counter
from check_p13 import apery,evaluate
def mac(f):
 r=1
 while (r+1)*r//2<=f:r+=1
 s=f-r*(r-1)//2
 return (r+1)*r*(r-1)//6+(s+1)*s//2
def graph_stats(H,edges):
 adj={i:set() for i in H}
 for i,j in edges:adj[i].add(j);adj[j].add(i)
 color={};fall=fnb=eb=0;components=[]
 for root in H:
  if root in color:continue
  color[root]=0;todo=[root];vs=set();nb=False
  for i in todo:
   vs.add(i)
   for j in adj[i]:
    if j not in color:color[j]=1-color[i];todo.append(j)
    elif color[j]==color[i]:nb=True
  ec=sum(i in vs and j in vs for i,j in edges);vc=len(vs)
  fall+=max(0,ec-vc)
  if nb:fnb+=ec-vc
  else:eb+=ec
  components.append(dict(vertices=sorted(vs),E=ec,V=vc,f=max(0,ec-vc),nonbip=nb))
 legal=sum(all(tuple(sorted(p)) in edges for p in itertools.combinations(x,2)) for x in itertools.combinations_with_replacement(H,3))
 assert legal-len(edges)<=mac(fnb)-eb
 return dict(f_all=fall,f_nb=fnb,E_bip=eb,E=len(edges),legal=legal,components=components)
def relay_graph(rows,gens,H,L,cubes,faceK):
 edges=set();lowlinks={l:set() for l in L};T=0;pairs=set()
 for r in cubes:
  f=[n for n,k in r['depth'].items() for _ in range(k)]
  assert len(f)==3 and sum(n in H for n in f)>=2
  assert all(n in H or n in L for n in f)
  low=[n for n in f if n in L]
  if not low:T+=1
  for p in itertools.combinations(f,2):
   pairs.add(sum(p))
   if all(n in H for n in p):
    edge=tuple(sorted(p));edges.add(edge)
    if low:lowlinks[low[0]].add(edge)
 gs=graph_stats(H,edges)
 vv=lambda ee:set(itertools.chain.from_iterable(ee))
 assert len(pairs)==len(edges)+sum(len(vv(ee)) for ee in lowlinks.values())
 assert len(cubes)==T+sum(map(len,lowlinks.values()))
 by={r['v']:r for r in rows}
 assert all(by[v]['UF'] and by[v]['K']==faceK for v in pairs)
 assert all(len(ee)-len(vv(ee))<=gs['f_all'] for ee in lowlinks.values())
 cost=mac(gs['f_nb'])+len(L)*gs['f_all']-gs['E_bip']
 assert len(cubes)-len(pairs)<=cost
 local=0
 for component in gs['components']:
  vs=set(component['vertices']);active=sum(any(i in vs for i,j in ee) for ee in lowlinks.values());f=component['f']
  term=active*f+(mac(f) if component['nonbip'] else -component['E'])
  component.update(active_low=active,cost=term);local+=term
 assert len(cubes)-len(pairs)<=local
 if gs['f_all']==0:assert len(cubes)<=len(pairs)
 return dict(gs,beta=len(cubes),p=len(pairs),T_H=T,cost=cost,local_cost=local)
stats=Counter();examples={}
def test(w,tag):
 z=evaluate(w);s=z['summary'];q=s['q'];rows=z['rows'];m=s['m'];M=s['M'];gens=z['generators'][1:];d=len(gens);lam=lambda v:(M-v)//m
 if q>=4:assert all(r['K']<=q-5 for r in rows if not r['UF'])
 if q not in (4,5):return
 stats[f'q{q}']+=1;by={r['v']:r for r in rows};pairs={}
 for i,n in enumerate(gens):
  for nn in gens[i:]:
   v=n+nn
   if v in by:pairs.setdefault(v,[]).append((n,nn))
 qdef=H2=0
 for v,pp in pairs.items():
  qw=sum(lam(n)+lam(nn)-2*lam(v) for n,nn in pp)
  credit=lam(v)-q+1+qw
  assert 0<=credit<=1-by[v]['K']
  qdef+=credit;H2+=lam(v)
 if q==4:
  h=s['h'];a=[n for n in gens if lam(n)==3];b=[n for n in gens if lam(n)==2];cc=[n for n in gens if lam(n)==1];ee=[n for n in gens if lam(n)==0]
  LD=[]
  for n in gens:
   Ld=0
   for v in w:
    while v+n in by:v+=n
    Ld+=lam(v)
   if n in ee:assert Ld==s['ell']-4
   if n in cc:assert Ld==s['ell']-3-sum(lam(v) for v in w if 0<v<2*m and v+n in by)
   LD.append(Ld)
  assert sum(LD)==s['Ltop']
  base=len(cc)*(len(cc)+1)+len(ee)*(3*len(a)+2*len(b)+len(cc))
  assert s['Ltop']>=base+(len(cc)+len(ee))*H2
  mfno=sum(not r['UF'] and r['v'] not in pairs for r in rows)
  qb=s['e']-h+base+(len(cc)+len(ee))*H2+qdef+2*mfno
  assert s['W']>=qb
  LA=max(0,m-(h+1)//2-max(0,m-2*h+2));J=len(b)*len(a)*(len(a)+1)//2+(len(a)+1)*len(b)*(len(b)+1)//2+math.comb(len(b)+2,3)+len(b)*len(cc)
  assert s['R_A']<=LA and s['R_out']<=J
  assert s['W']>=m-h+s['Ltop']+s['Z']-min(math.comb(len(a)+2,3),LA)-min(m-h,J)
  cubes=[r for r in rows if r['critical'] and r['kind']=='(3, 0, (3, 3, 3))']
  H=[n for n in a if 2*(n-m)>=h];L=[n for n in a if 2*(n-m)<h]
  gs=relay_graph(rows,gens,H,L,cubes,-1)
  assert 3*s['R_A']<=(len(a)+2)*gs['p']
  g=len(cc)+len(ee);Q=math.comb(len(a)+1,2)
  if max(0,len(a)-1-3*g)*Q<=3*base:
   stats['q4_CE_directions_class']+=1
   assert s['R_A']<=s['Ltop']+s['C_U']+gs['p']
  if len(a)>0 and 3*len(ee)*(len(a)+7)>=len(a)**2-1:
   stats['q4_E_directions_class']+=1
   assert s['R_A']<=s['Ltop']+s['C_U']+gs['p']
  if gs['cost']<=s['Ltop']+s['C_U']:
   stats['q4_graph_class']+=1;assert s['R_A']<=s['Ltop']+s['C_U']+gs['p']
  if gs['local_cost']<=s['Ltop']+s['C_U']:stats['q4_component_class']+=1;assert s['R_A']<=s['Ltop']+s['C_U']+gs['p']
  if qb>=0:stats['q4_quad_class']+=1
  if s['e']-h+s['Ltop']+s['Z']<0 and qb>=0:stats['quad_beyond_full_EH']+=1
  s.update(QDef=qdef,H2=H2,MFno2=mfno,QBound=qb,graph=gs)
 else:
  h=M-5*m+1;rho=m-h;beta=[r for r in rows if r['K']==2]
  assert all(r['K']<=2 for r in rows)
  assert all(r['K']<=0 for r in rows if not r['UF'])
  for r in beta:
   assert r['UF'] and r['lam']==0 and r['L1']==3
   assert all(m+h<n<2*m and lam(n)==3 and lam(r['v']-n)==1 for n in r['depth'])
   assert r['s']<rho//2
  eligible=[n for n in gens if m+h<n<2*m]
  H=[n for n in eligible if 2*n>3*m+h-1];L=[n for n in eligible if n not in H]
  gs=relay_graph(rows,gens,H,L,beta,0)
  FM=sum(not r['UF'] for r in rows)
  assert s['W']>=s['e']-h+s['Ltop']+FM+gs['p']-len(beta)
  if gs['cost']<=s['Ltop']+FM:
   stats['q5_graph_EH_class']+=1;assert s['W']>=s['e']-h
  if gs['local_cost']<=s['Ltop']+FM:stats['q5_component_EH_class']+=1;assert s['W']>=s['e']-h
  if len(H)<=1:
   stats['q5_HIGH1']+=1;assert s['W']>=s['e']-h
  if beta:stats['q5_K2_cases']+=1
  keep={key:s[key] for key in ['m','e','M','q','c','W','ell','C2','need','Bc','E','Eu','Delta','Ltop','CU_slack','PLUS_slack','POOR_slack','MF','Z']}
  s.clear();s.update(keep);s.update(h=h,rho=rho,graph=gs,beta5=len(beta),H5=len(H),GEN_EH_slack=s['W']-s['e']+h)
  if beta and 'q5_K2' not in examples:examples['q5_K2']=dict(generators=z['generators'],summary=s,beta=beta,graph=gs)
 if tag:examples[tag]=dict(summary=s,generators=z['generators'],apery=w)
 return s

for log in ['kunz101.log','generators181.log','kunz527_shaped.log','structured.log','seeds.log','kunz101_seed.log','kunz211_seed.log','kunz101_ratio.log','repro101.log','repro211.log','repro527.log']:
 if not Path(log).exists():continue
 lines=[ln for ln in Path(log).read_text().splitlines() if 'gens=[' in ln]
 if not lines:continue
 ln=lines[-1];g=list(map(int,re.search(r'gens=\[([^]]+)\]',ln).group(1).split(',')))
 s=test(apery(g),log)
for g in [[5,9,12],[8,10,11,12],[8,13,14,15],[10,16,17,18],[11,18,21,30,31,34,37,38],[8,14,15]]:
 test(apery(g),'named'+str(g))
rnd=random.Random(140014)
for it in range(1200):
 m=rnd.randrange(10,181);q=rnd.choice([4,5]);h=rnd.randrange(1,m);k=rnd.randrange(2,10)
 g=[m]+[rnd.randrange(m+1,3*m) for _ in range(k)]
 if math.gcd(*g)>1:continue
 w=apery(g);cap=(q-1)*m+h
 for i in range(1,m):w[i]=min(w[i],cap+(i-cap)%m)
 test(w,None)
# A complete, independent reconstruction of the SINGLE-E counterexample.
g=list(map(int,Path('simplex_e_gens.txt').read_text().split()))
s=test(apery(g),'single_E_counter')
assert s['R_A']>s['ell']-4+s['C_U']+s['critical_pair_shadow']
assert s['W']==s['QBound']
if Path('simplex_e_small_gens.txt').exists():
 g=list(map(int,Path('simplex_e_small_gens.txt').read_text().split()))
 s=test(apery(g),'small_single_E_counter')
 assert s['R_A']>s['ell']-4+s['C_U']+s['critical_pair_shadow'] and s['W']==s['QBound']
Path('independent.json').write_text(json.dumps(dict(stats=stats,examples=examples),indent=2))
print(json.dumps(stats,sort_keys=True))
