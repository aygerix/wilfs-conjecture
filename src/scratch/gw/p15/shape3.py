"""All plane-partition ideals through size 13. Fejer only."""
from functools import lru_cache
@lru_cache(None)
def parts(n,cap):
 if not n:return ((),)
 return tuple((k,)+tail for k in range(min(n,cap),0,-1) for tail in parts(n-k,k))
def layers(n,prev=None):
 if not n:yield [];return
 for k in range(1,n+1):
  for row in parts(k,k):
   if prev is not None and (len(row)>len(prev) or any(x>prev[i] for i,x in enumerate(row))):continue
   for rest in layers(n-k,row):yield [row]+rest
with open('shape3.txt','w') as out:
 for n in range(1,14):
  count=0
  for ls in layers(n):
   D=[(z,i,j) for z,row in enumerate(ls) for i,width in enumerate(row) for j in range(width)]
   assert len(D)==n
   DD=set(D)
   assert all(tuple(f[b]-(a==b) for b in range(3)) in DD for f in D for a in range(3) if f[a])
   out.write(str(n)+' '+' '.join(str(x) for f in D for x in f)+'\n');count+=1
  print(n,count,flush=True)
