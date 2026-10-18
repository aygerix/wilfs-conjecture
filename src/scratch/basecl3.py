# Base-CL per-cell G_sigma(y) = #{a: l_a > r} - floor((sigma+sum l)/m), sorted by r = <sigma+phi(y)>
# test cumulative bounds:  for all R:  sum_{r>=R} G(y_r) >= -#{r >= max(R,u)}  (u=m-sigma)   [LOW]
#                          for all R:  sum_{r<=R} G(y_r) <= #{r <= min(R,u-2)}                  [UP]
import sys, itertools
sys.path.insert(0,'/Users/jmercedes/Desktop/Projects/Research/wilfs-conjecture/src')
from exp_cl_tiling import downsets
d=int(sys.argv[1]); M=int(sys.argv[2]); m0=int(sys.argv[3]) if len(sys.argv)>3 else 3
for m in range(m0,M+1):
    tot=0; badL=badU=badtot=0; exL=exU=None; Gdist={}
    for D in downsets(m,d):
        Dl=sorted(D)
        if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
        for p in itertools.product(range(1,m),repeat=d):
            res={x:sum(i*j for i,j in zip(x,p))%m for x in Dl}
            if len(set(res.values()))!=m: continue
            for sg in range(m):
                tot+=1; u=m-sg
                G=[0]*m
                for y in Dl:
                    l=[(y[a]*p[a])%m for a in range(d)]; S=sg+sum(l); r=S%m
                    G[r]=sum(1 for a in range(d) if l[a]>r)-S//m
                    Gdist[G[r]]=Gdist.get(G[r],0)+1
                if not (-sg<=sum(G)<=m-1-sg): badtot+=1
                for R in range(m):
                    if sum(G[R:])< -len([r for r in range(R,m) if r>=u]):
                        badL+=1
                        if exL is None: exL=(Dl,p,sg,G)
                        break
                for R in range(m):
                    if sum(G[:R+1])> len([r for r in range(R+1) if r<=u-2]):
                        badU+=1
                        if exU is None: exU=(Dl,p,sg,G)
                        break
    print('d',d,'m',m,'cases',tot,'BaseCL fails',badtot,'cumLOW fails',badL,'cumUP fails',badU,'G dist',dict(sorted(Gdist.items())),exL,flush=True)
