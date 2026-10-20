"""Independent exact P13 quantities, including UF classification. Fejer only."""
import heapq,json,sys
from collections import Counter
def apery(g):
 m=min(g);w=[10**100]*m;w[0]=0;heap=[(0,0)]
 while heap:
  x,i=heapq.heappop(heap)
  if w[i]!=x:continue
  for n in g:
   j=(i+n)%m;y=x+n
   if y<w[j]:w[j]=y;heapq.heappush(heap,(y,j))
 return w
def evaluate(w):
 m=len(w);ap=set(w);M=max(w);q=M//m;h=M-4*m+1;s0=M%m
 gens=[]
 for x in sorted(ap-{0}):
  if not any(x-n in ap for n in gens):gens.append(x)
 d=len(gens);lam=lambda x:(M-x)//m;s=lambda x:(M-x)%m
 cnt={x:0 for x in ap};cnt[0]=1
 for n in gens:
  for x in sorted(ap):
   if x-n in ap:cnt[x]=min(2,cnt[x]+cnt[x-n])
 rows=[];Bc=Ltop=Delta=0
 for x in sorted(ap):
  dp={};Uv=Pv=L1v=0
  for n in gens:
   dep=0;y=x
   while y-n in ap:dep+=1;y-=n
   if dep:dp[n]=dep;Uv+=n;Pv+=dep*(s(x-n)-s(x));L1v+=dep*(lam(x-n)-lam(x))
   t=x
   while t+n in ap:t+=n
   Bc+=M-t;Ltop+=lam(t);Delta+=s(x)-(M-t)
  Ev=sum(n*z for n,z in dp.items())-x;Eu=max(0,Uv-x);g=x-m*L1v;K=q-lam(x)-L1v
  assert Ev>=0 and ((Ev==0)==(cnt[x]==1))
  assert Pv-Ev==g
  kind=''
  if Ev==0 and K>0:
   ordv=sum(dp.values());classes=tuple(sorted(lam(n) for n,z in dp.items() for _ in range(z)))
   kind=str((ordv,lam(x),classes))
   if q==4:
    assert K==1,(x,K)
    assert (ordv==2 and ((lam(x)==1 and classes==(2,2)) or (lam(x)==0 and classes==(1,2)))) or (ordv==3 and lam(x)==0 and all(lam(x-n)==1 for n in dp)),(x,kind)
  rows.append(dict(v=x,lam=lam(x),s=s(x),depth=dp,E=Ev,Eu=Eu,P=Pv,L1=L1v,g=g,K=K,UF=Ev==0,critical=bool(kind),kind=kind))
 ell=sum(map(lam,w));c=M-m+1;W=(d+1)*ell-c;C2=m*(m-1)//2;need=(d-1)*C2;B=d*m*M-(d+1)*sum(w)
 E=sum(r['E'] for r in rows);Eu=sum(r['Eu'] for r in rows);Wp=sum(max(0,r['g']) for r in rows);Pp=sum(r['P'] for r in rows if r['g']>0)
 assert E==B-Bc and Delta==d*C2-Bc and B==m*W+need and Delta==sum(r['P'] for r in rows)-m*Ltop
 if q==4:assert not any(r['E']>0 and r['g']>=0 for r in rows),[r for r in rows if r['E']>0 and r['g']>=0]
 crit=[r for r in rows if r['UF'] and r['K']>0];u=len(crit)
 base=s0*(s0+1)//2;rho=m-s0-1
 Z=sum(max(0,-r['K']) for r in rows)
 RA=sum(r['critical'] and r['kind']=='(3, 0, (3, 3, 3))' for r in rows)
 if q==4:
  assert W==rho+Ltop-u+Z
  assert all(r['K']<=-1 for r in rows if not r['UF'])
  assert all(r['s']<rho for r in crit if r['kind']!='(3, 0, (3, 3, 3))')
  CU=sum(max(1,r['lam']+len(r['depth'])-4) for r in rows if not r['UF'])
  assert Z>=CU and W>=Ltop+CU-RA
  byvalue={r['v']:r for r in rows};pairshadow=set()
  for r in crit:
   if r['kind']=='(3, 0, (3, 3, 3))':
    for n in r['depth']:pairshadow.add(r['v']-n)
  assert all(byvalue[v]['UF'] and byvalue[v]['K']==-1 for v in pairshadow)
 else:CU=None
 T_A=set();A=[n for n in gens if lam(n)==3]
 if q==4 and len(A)<=64:
  for i,na in enumerate(A):
   for j in range(i,len(A)):
    nb=A[j]
    for nc in A[j:]:
     x=na+nb+nc
     if x in ap and all(lam(x-n)==1 for n in (na,nb,nc)):T_A.add(x)
  zA=sum(cnt[v]>=2 for v in T_A);uA=sum(cnt[v]==1 for v in T_A)
  assert uA==RA and Z>=zA and W>=Ltop+zA-uA
 else:zA=uA=None
 if q==4:
  mf=sum(not r['UF'] for r in rows);dec=m-1-d;ps=len(pairshadow)
  assert 3*RA<=(len(A)+2)*ps
  assert mf+ps+RA<=dec and Z>=CU+ps
  assert W>=Ltop+CU+ps-RA
  shadow_rhs=(len(A)+5)*(Ltop+CU)-(len(A)-1)*(dec-mf)
  if A:assert (len(A)+5)*W>=shadow_rhs
 else:ps=shadow_rhs=None
 summary=dict(m=m,e=d+1,a=len(A),alpha=sum(2*(n-m)<h for n in A),M=M,q=q,h=h,c=c,W=W,ell=ell,C2=C2,need=need,Bc=Bc,E=E,Eu=Eu,Delta=Delta,Ltop=Ltop,
              CU_slack=Bc+Eu-need,PLUS_slack=C2+m*Ltop-Wp,POOR_slack=C2+m*Ltop-Pp,Ucrit=u,
              TOP_strong_slack=Ltop-u,TOP_count_slack=Ltop+(C2-base)//m-u,critical_types=dict(Counter(r['kind'] for r in crit)),
              Z=Z,R_A=RA,R_out=u-RA,rho=rho,MF_Acentral=zA,UF_Acentral=uA,Wilf_count_slack=rho+Ltop-u,
              MF=sum(not r['UF'] for r in rows),C_U=CU,overlap_payment_slack=Ltop+(CU or 0)-RA,
              critical_pair_shadow=ps,shadow_payment_slack=shadow_rhs)
 return dict(summary=summary,generators=[m]+gens,apery_by_residue=w,rows=rows)
if __name__=='__main__':
 g=list(map(int,sys.argv[1:])) if len(sys.argv)>1 else [53]+list(range(85,96))
 print(json.dumps(evaluate(apery(g)),indent=2))
