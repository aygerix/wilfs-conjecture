"""Check a C assignment certificate against independently audited certprobe data.
usage: python3 verify_matching.py matching.jsonl probe.jsonl [more_probe.jsonl ...]
"""
import sys,json
from fractions import Fraction as F
from verify_probe import audit,open_text
D={}
for path in sys.argv[2:]:
 for line in open_text(path):
  x=json.loads(line); report=audit(x);D[tuple(sorted(x['generators']))]=(x,report)
for line in open_text(sys.argv[1]):
 if not line.startswith('{'):continue
 C=json.loads(line);S,R=D[tuple(sorted(C['G']))];m,e,q,c=(S[k] for k in ('m','e','q','c'))
 gr={g%m for g in S['generators'] if g!=m};to=[[] for _ in range(m)]
 for i,j,s,J,tau,lo,up in S['pairs']:
  if not J:to[s].append((i,j,up))
 b=[0]*m;b[0]=q
 for s in sorted(range(1,m),key=lambda k:S['w'][k]):
  b[s]=S['mu'][s] if s in gr else max([0]+[b[i]+b[j]-q-up for i,j,up in to[s]])
 assert b==C['b'] and e*sum(b)-c==C['B']
 res=[s for s in range(1,m) if s not in gr];assert res==C['residues'];ix={s:i for i,s in enumerate(res)};n=len(res)
 w=[[0]*n for _ in range(n)]
 for i,j,s,J,tau,lo,up in S['pairs']:
  if J:continue
  d=q-lo-b[i]-b[j]+b[s]
  if d<=0:continue
  a,z=ix.get(i),ix.get(j)
  if a is None or z is None:
   assert a is not None or z is not None
   t=z if a is None else a;w[t][t]=max(w[t][t],2*d)
  else:w[a][z]=w[z][a]=max(w[a][z],d)
 p=C['permutation'];alpha=C['alpha'];beta=C['beta'];assert sorted(p)==list(range(n))
 value=sum(w[i][p[i]] for i in range(n));assert value==C['M']==sum(alpha)+sum(beta)
 for i in range(n):
  for j in range(n):assert alpha[i]+beta[j]>=w[i][j]
 cover=[F(alpha[i]+beta[i],2) for i in range(n)]
 assert min(cover,default=0)>=0
 for i in range(n):
  for j in range(n):assert cover[i]+cover[j]>=w[i][j]
 assert sum(cover)==F(value,2)
 t=[S['mu'][s]-b[s] for s in res];assert min(t,default=0)>=0
 for i in range(n):
  for j in range(n):assert t[i]+t[j]>=w[i][j]
 fractional=C['B']+F(e*value,2);rounded=C['B']+e*((value+1)//2)
 assert fractional<=F(R['models']['UA3']['optimum']) and rounded==C['corrected']<=S['W']
 print('CERTIFIED G=%s B=%d M=%d corrected=%d UA3=%s W=%d'%(C['G'],C['B'],value,rounded,R['models']['UA3']['optimum'],S['W']))
