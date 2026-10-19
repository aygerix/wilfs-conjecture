# Tight cases of PCI** : u = beta*min(w,2q-1), M = max(T, u+Jw), T=(2i-2)q-1, delta=M-u-Jw
import sys
from collections import Counter
imax=int(sys.argv[1]); qmax=int(sys.argv[2])
def F(t,q,i): return min(i,t//q)
cnt=Counter(); ex={}
for i in range(3,imax+1):
  for q in range(2,qmax+1):
    T=(2*i-2)*q-1
    for w in range(q+1,2*i*q+2):
      wp=min(w,2*q-1)
      for beta in range(1,i):
        for J in range(1,i):
          u=beta*wp; M=max(T,u+J*w); d=M-u-J*w
          if d>=u: continue
          L=sum(F(u+j*w,q,i)-F(d+j*w,q,i) for j in range(1,J+1))
          R=J*beta+F(d,q,i)
          assert L<=R,(i,q,w,beta,J)
          if L==R:
            key=('w<2q' if w<2*q else 'w>=2q', 'd=0' if d==0 else 'd>0', 'J+b vs i:%+d'%(J+beta-i))
            cnt[key]+=1
            ex.setdefault(key,(i,q,w,beta,J,M,d,L))
for k in sorted(cnt): print(k,cnt[k],'ex(i,q,w,b,J,M,d,L)=',ex[k])
