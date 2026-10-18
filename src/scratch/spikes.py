# Tile-CL for core + spikes: D = C (down-set in N^d0, phi injective) U {e_a : spike a}, spike residues = complement of phi(C).
import sys, itertools
sys.path.insert(0,'/Users/jmercedes/Desktop/Projects/Research/wilfs-conjecture/src')
from exp_cl_tiling import downsets
def tile_slack(D,p,m):
    D=set(D); d=len(p)
    w=[0]*m
    for y in D:
        T=0
        for a in range(d):
            z=list(y); z[a]+=1
            if tuple(z) not in D: T+=y[a]+1
        w[sum(i*j for i,j in zip(y,p))%m]+=T
    M=m*(m-1)//2
    out=[]
    for s in range(m):
        num=sum(w[r]*((s-r)%m) for r in range(m))-(d-1)*M
        assert num%m==0; out.append(num//m)
    return out
def with_spikes(C,pc,m):
    d0=len(pc); res={sum(i*j for i,j in zip(x,pc))%m for x in C}
    R=sorted(set(range(m))-res); k=len(R); d=d0+k
    D=[tuple(x)+(0,)*k for x in C]+[tuple([0]*d0+[1 if j==i else 0 for j in range(k)]) for i in range(k)]
    return D,tuple(pc)+tuple(R)
# E17 example
D,p=with_spikes([(0,),(1,),(2,)],(7,),10); print('E17+spikes',p,tile_slack(D,p,10))
# smallest failing: cores of dim 1,2 with |C| small, m small
best={}
for m in range(3,16):
    found=None
    for d0 in (1,2):
        for k in range(2,m):
            for C in downsets(k,d0):
                if d0==2 and any(all(x[a]==0 for x in C) for a in range(2)): continue
                for pc in itertools.product(range(1,m),repeat=d0):
                    res=[sum(i*j for i,j in zip(x,pc))%m for x in C]
                    if len(set(res))!=k: continue
                    D,p=with_spikes(C,pc,m)
                    sl=tile_slack(D,p,m)
                    if min(sl)<0 or max(sl)>m-1:
                        if found is None or len(p)<len(found[2]): found=(sorted(C),pc,p,sl)
    print('m',m,'smallest-d failing spiky tile:',found,flush=True)
    if found and m>=10: break
