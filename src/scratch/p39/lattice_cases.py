"""Generate genuine numerical-semigroup inputs from integer matrix cofactors.
No parking-function claim is required: gcd is checked and certprobe/repair_scan reconstruct S.
L=t*((d+1)I-J)+N, where N has unit superdiagonal. A row of adj(L) gives
positive residue representatives much smaller than det(L) in scaled cases.
"""
from fractions import Fraction as F
from math import gcd
from functools import reduce

def det(A):
 B=[list(map(F,row)) for row in A];v=F(1);n=len(A)
 for i in range(n):
  k=next((k for k in range(i,n) if B[k][i]),None)
  if k is None:return 0
  if k!=i:B[k],B[i]=B[i],B[k];v=-v
  q=B[i][i];v*=q
  for j in range(i,n):B[i][j]/=q
  for k in range(i+1,n):
   q=B[k][i]
   for j in range(i,n):B[k][j]-=q*B[i][j]
 assert v.denominator==1
 return int(v)

def adjrow(A,r):
 n=len(A)
 return [(-1)**(r+j)*det([[A[x][y] for y in range(n) if y!=r] for x in range(n) if x!=j]) for j in range(n)]

def cases():
 for d in range(3,7):
  for t in (1,2,4):
   A=[[t*((d+1)*(i==j)-1)+(j==i+1) for j in range(d)] for i in range(d)]
   m=det(A)
   for row in range(d):
    a=adjrow(A,row);g=reduce(gcd,[m]+a)
    if g!=1:continue
    assert all(x>0 for x in a)
    a=[x%m for x in a]
    assert all(a) and len(set(a))==d
    yield d,t,row,[m]+[m+x for x in a]

def parking_slice(d):
 """Exact finite tile check and rho=0 rescalings of all its maximal cells.
 If g^T L is positive, every non-parking nonnegative configuration can be
 reduced by L*1_U to a cheaper one. Distinct residue labels then certify that
 the parking configurations are exactly the Apéry factorizations.
 """
 from itertools import product
 A=[[(d+1)*(i==j)-1+(j==i+1) for j in range(d)] for i in range(d)]
 m=det(A);a=next(v for r in range(d) if reduce(gcd,[m]+(v:=adjrow(A,r)))==1)
 forbidden=[]
 for bits in range(1,1<<d):
  U=[i for i in range(d) if bits>>i&1]
  forbidden.append([(i,sum(A[i][j] for j in U)) for i in U])
 forbidden.sort(key=len,reverse=True)
 tile=[x for x in product(range(d),repeat=d) if not any(all(x[i]>=v for i,v in row) for row in forbidden)]
 labels=[sum(v*z for v,z in zip(a,x))%m for x in tile]
 assert len(tile)==len(set(labels))==m
 degree=[sum(x) for x in tile];H=max(degree)
 tile_set=set(tile)
 tops=[i for i,x in enumerate(tile) if all(tuple(v+(j==k) for j,v in enumerate(x)) not in tile_set for k in range(d))]
 print('PARKING_TILE d=%d m=%d cells=%d max_degree=%d top_degree_cells=%d maximal_cells=%d'%(d,m,len(tile),H,degree.count(H),len(tops)),flush=True)
 tried=set();positive=0;rhozero=0
 for at in tops:
  if gcd(labels[at],m)!=1:continue
  u=(-pow(labels[at],-1,m))%m
  if u in tried:continue
  tried.add(u);g=[m+(u*v)%m for v in a]
  if not all(sum(g[i]*A[i][j] for i in range(d))>0 for j in range(d)):continue
  positive+=1;w=[sum(v*z for v,z in zip(g,x)) for x in tile]
  if w[at]!=max(w):continue
  c=max(w)-m+1;q=(c+m-1)//m
  assert c==q*m
  rhozero+=1;e=d+1;genus=sum((v-l)//m for v,l in zip(w,[(u*v)%m for v in labels]))
  W=e*(c-genus)-c
  B=e*(q+sum(max(0,q+1-2*h) for h in degree if h))-c
  low=sum(0<h and 2*h<=q for h in degree)
  upper=e*(q+m-1+(q-2)*low)-c
  print('RHO_ZERO u=%d q=%d B=%d W=%d low_cells=%d matching_bound_upper=%d G=%s'%(u,q,B,W,low,upper,[m]+g),flush=True)
 print('PARKING_RESULT units=%d positive_cost=%d rho_zero=%d'%(len(tried),positive,rhozero),flush=True)

if __name__=='__main__':
 import argparse,json,subprocess,time
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--run',help='C repair_scan binary (compiled with sufficient MM)')
 p.add_argument('--max-m',type=int,default=4095)
 p.add_argument('--output',default='lattice_matching.jsonl')
 p.add_argument('--parking',type=int,help='enumerate a finite t=1 parking tile; use d<=6')
 args=p.parse_args()
 if args.parking:
  if not 2<=args.parking<=6:p.error('--parking requires 2<=d<=6')
  parking_slice(args.parking);raise SystemExit
 out=open(args.output,'w') if args.run else None
 for d,t,row,G in cases():
  if not args.run:
   print('d=%d t=%d row=%d m=%d G=%s'%(d,t,row,G[0],G));continue
  if G[0]>args.max_m:continue
  start=time.monotonic()
  try:r=subprocess.run([args.run,'--case']+list(map(str,G)),capture_output=True,text=True,timeout=60)
  except subprocess.TimeoutExpired:
   print('TIME_LIMIT',G,flush=True);break
  for line in r.stdout.splitlines():
   if line.startswith('{'):
    out.write(line+'\n');out.flush();C=json.loads(line)
    print({k:C[k] for k in ('G','m','e','c','B','M','corrected','W')},'seconds',round(time.monotonic()-start,3),flush=True)
   else:print(line,flush=True)
  if r.returncode:print('REJECT_OR_ERROR',G,r.returncode,r.stderr,flush=True)
  if 'BOUND_FAILURE' in r.stdout or 'WILF_FAILURE' in r.stdout:break
 if out:out.close()
