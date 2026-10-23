"""Cross-check the BASE-family deflation lemma, not a general proof by computation.
Checks hypotheses and independently reconstructs invariants of S and its deflation.
"""
from heapq import heappop,heappush
from math import comb

def data(G):
 m=min(G);w=[10**30]*m;w[0]=0;Q=[(0,0)]
 while Q:
  d,s=heappop(Q)
  if d!=w[s]:continue
  for g in G:
   v=d+g;t=v%m
   if v<w[t]:w[t]=v;heappush(Q,(v,t))
 assert max(w)<10**30
 c=max(w)-m+1;q=(c+m-1)//m;r=w.index(max(w));mu=[max(0,(c-v+m-1)//m) for v in w]
 N=m*max(G)+m;member=bytearray(N+1);member[0]=1
 for v in range(1,N+1):member[v]=any(v>=g and member[v-g] for g in G)
 cc=max(v for v in range(N+1) if not member[v])+1;gg=sum(not member[v] for v in range(cc));assert cc==c
 gen=[v for v in range(1,max(G)+1) if member[v] and not any(member[a] and member[v-a] for a in range(1,v))]
 e=len(gen);assert gen==sorted(G)
 h=[0]*m;hn=[0]*m
 for s in sorted(range(1,m),key=lambda s:w[s]):
  lengths=[h[i]+h[j] for i in range(1,m) for j in range(i,m) if (i+j)%m==s and w[i]+w[j]==w[s]]
  short=[hn[i]+hn[j] for i in range(1,m) for j in range(i,m) if (i+j)%m==s and w[i]+w[j]==w[s]]
  h[s]=max(lengths,default=1);hn[s]=min(short,default=1)
 assert h==hn
 return dict(m=m,e=e,c=c,g=gg,W=e*(c-gg)-c,q=q,r=r,w=w,mu=mu,h=h)

n=0
for A in ([5,6,8],[6,7,10],[7,9,10]):
 for k in range(1,11):
  G=[15]+[15*k+a for a in A];S=data(G);m=S['m'];d=len(A);r=S['r'];T=data([m]+[m+a for a in A])
  assert S['q']==3*k+1 and max(S['h'])==3
  assert all(a<=r and S['mu'][a]==2*k+1 for a in A)
  pair_res=[]
  for ia,a in enumerate(A):
   for b in A[ia:]:
    s=(a+b)%m;assert S['w'][s]==2*k*m+a+b and S['mu'][s]==k
    pair_res.append(s)
  assert len(set(pair_res))==comb(d+1,2)
  assert all(S['mu'][s]==0 for s in range(m) if S['h'][s]==3)
  assert all(2*a>r for a in A)
  predicted=[S['w'][s]-(k-1)*m*S['h'][s] for s in range(m)]
  assert T['w']==predicted and T['c']==3*m+r+1 and T['c']<=4*m and T['e']==S['e']
  assert S['W']==T['W']+3*(k-1)*(comb(d+3,3)-m)
  n+=1
print('VERIFIED',n,'BASE examples (three recorded residue covers, k=1..10), with independent membership invariants and exact Apéry reconstruction.')
