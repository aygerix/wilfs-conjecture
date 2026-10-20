"""Exact full-A-simplex counterexample to the SINGLE E-credit proposal.
This is not a UF-RELAY counterexample. Run only on fejer.
"""
import itertools,json
from pathlib import Path
def b3(y):
 s=[sum(x) for x in itertools.combinations_with_replacement(y,3)]
 return len(s)==len(set(s))
Y=[0];v=1
while len(Y)<7:
 if b3(Y+[v]):Y.append(v)
 v+=1
T=max(Y);h=8*T+9;m=3*h+1;t=[4*T+5+4*y for y in Y]
assert m%4==0 and h%4==1 and all(h<2*u<2*h for u in t)
core={0:()}
for j in range(1,4):
 for x in itertools.combinations_with_replacement(range(7),j):
  value=sum(m+t[i] for i in x)
  assert value not in core
  core[value]=x
assert len(core)==120 and len({v%m for v in core})==120
c=3*m+h;M=c+m-1
assert max(core)<=M and 4*min(m+u for u in t)>M
w=[c+(i-c)%m for i in range(m)]
for x in core:w[x%m]=x
assert max(w)==M
E=sorted(v for v in w if v not in core)
g=[m]+[m+u for u in t]+E
ell=sum((M-v)//m for v in w)
RA=84;pA=28;CU=0;Lam=len(E)*(ell-4);Z=28;rho=m-h;e=len(g);W=e*ell-c
assert RA>ell-4+CU+pA and W==rho+Lam+Z-RA
Path('simplex_e_gens.txt').write_text(' '.join(map(str,g))+'\n')
Path('simplex_e_ap.txt').write_text(' '.join(map(str,w))+'\n')
z=dict(Y=Y,A_offsets=t,m=m,h=h,c=c,M=M,e=e,E_count=len(E),ell=ell,R_A=RA,p_A=pA,C_U=CU,Lambda=Lam,Z=Z,rho=rho,R_out=0,W=W,
       single_E_slack=ell-4+CU+pA-RA,UF_RELAY_slack=Lam+CU+pA-RA,
       core_values=sorted(core),E_generator_description='one c-aligned tail representative for each residue not represented by the listed core values')
Path('simplex_e.json').write_text(json.dumps(z,indent=2))
print(json.dumps(z))
