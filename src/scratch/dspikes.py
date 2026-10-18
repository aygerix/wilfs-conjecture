# Core (down-set, dim<=2, phi injective) + attachments covering the remaining residues:
#   spike {e_b} (residue r) or double spike {e_b, 2e_b} (residues r, 2r).  Check SR-CL: min slack + sigma >= 0,
#   sigma = number of (single) spikes.  Report the worst (min slack + sigma) and failures.
import sys, itertools
sys.path.insert(0,'/Users/jmercedes/Desktop/Projects/Research/wilfs-conjecture/src')
from exp_cl_tiling import downsets
def tile_slack(D,p,m):
    D=set(D); d=len(p); w=[0]*m
    for y in D:
        T=0
        for a in range(d):
            z=list(y); z[a]+=1
            if tuple(z) not in D: T+=y[a]+1
        w[sum(i*j for i,j in zip(y,p))%m]+=T
    M=m*(m-1)//2
    return [(sum(w[r]*((s-r)%m) for r in range(m))-(d-1)*M)//m for s in range(m)]
def covers(R,m):
    # yield lists of attachments: ('s',r) or ('d',r) with {r,2r} subset R, partitioning R
    R=sorted(R)
    if not R: yield []; return
    r0=R[0]; rest=R[1:]
    for t in covers(rest,m): yield [('s',r0)]+t
    # r0 as base of double spike
    r2=(2*r0)%m
    if r2 in rest and r2!=r0:
        for t in covers([x for x in rest if x!=r2],m): yield [('d',r0)]+t
    # r0 as the 2r of a double spike with base r (r in rest, 2r = r0)
    for r in rest:
        if (2*r)%m==r0:
            for t in covers([x for x in rest if x!=r],m): yield [('d',r)]+t
M0=int(sys.argv[1]); M1=int(sys.argv[2])
for m in range(M0,M1+1):
    worst=None; fails=0; n=0
    for d0 in (1,2):
        for k in range(2,m-1):
            for C in downsets(k,d0):
                if d0==2 and any(all(x[a]==0 for x in C) for a in range(2)): continue
                for pc in itertools.product(range(1,m),repeat=d0):
                    res=[sum(i*j for i,j in zip(x,pc))%m for x in C]
                    if len(set(res))!=k: continue
                    R=set(range(m))-set(res)
                    for att in covers(R,m):
                        if not any(t=='d' for t,_ in att): continue   # spikes-only done in spikes.py
                        nb=len(att); D=[tuple(x)+(0,)*nb for x in C]; p=list(pc)
                        for i,(t,r) in enumerate(att):
                            e=[0]*(d0+nb); e[d0+i]=1; D.append(tuple(e))
                            if t=='d': e2=list(e); e2[d0+i]=2; D.append(tuple(e2))
                            p.append(r)
                        sl=tile_slack(D,p,m); sig=sum(1 for t,_ in att if t=='s'); n+=1
                        v=min(sl)+sig
                        if v<0: fails+=1
                        if worst is None or v<worst[0]: worst=(v,min(sl),sig,sorted(C),pc,att)
    print('m',m,'tiles',n,'SR-CL fails',fails,'worst (min+sigma, min, sigma, core, pc, att):',worst,flush=True)
