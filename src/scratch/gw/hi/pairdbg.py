# search the 'bad' configuration of the row pairing (w>=2q): rows j<j'=j+s both above cap,
# sigma = 2P+sw-(2i-2beta)q < q and pbar+pbar' >= q.  Report which hypothesis kills it.
import sys
qmax=int(sys.argv[1]); imax=int(sys.argv[2])
found=0; stats={}
for q in range(2,qmax+1):
 for i in range(3,imax+1):
  T=(2*i-2)*q-1
  for w in range(2*q,3*q+2):
   for beta in range(1,i):
    for L in range((2*beta-1)*q, beta*(2*q-1)+1):
     for s in range(1,i):
      for P in range(w, i*q):          # P=delta+jw with j>=1 => P>=w (delta>=0)
        Pp=P+s*w
        if Pp>=i*q: continue           # row j' has positive deficit
        if 2*P+L+(s-1)*w < T: continue # constraint C
        sigma=2*P+s*w-(2*i-2*beta)*q
        pb=P%q; pbp=Pp%q
        if sigma<q and pb+pbp>=q:
          S=(i-P//q)+(i-Pp//q)
          # realizability: P=delta+j*w, j>=1, 0<=delta, u=L+delta<=beta*(2q-1); rows tops >= iq
          ok=False
          for j in range(1,P//w+1):
            d=P-j*w
            if d<0: break
            if L+d<=beta*(2*q-1) and P+L>=i*q: ok=True; break
          key=('realizable' if ok else 'not realizable')
          stats[key]=stats.get(key,0)+1
          print("BAD" if ok else "unreal",dict(q=q,i=i,w=w,beta=beta,L=L,s=s,P=P,Pp=Pp,S=S,pb=pb,pbp=pbp,sigma=sigma))
print(stats)
