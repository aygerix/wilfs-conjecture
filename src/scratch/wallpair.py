# Wilf direction X(s) >= K with X(s) = sum_j F(E_{s+jm}),  K = sum_j |{z: V(z) >= (j+1)m}|.
# Local pairings: P1 per wall j: F(E_{s+jm}) >= N_{j+1} := #{z : V(z) >= (j+1)m}
#                 P2 tail sums: sum_{j>=J} F_j >= sum_{j>=J} N_{j+1}  for all J
#                 P3 head sums: sum_{j<=J} F_j >= sum_{j<=J} N_{j+1}  for all J
# lifts: phat in [1,m-1] (standard) ; also report whether SOME lift with k in [0,K]^d makes P1 hold.
import sys, itertools
sys.path.insert(0,'src')
from exp_cl_tiling import downsets, Tvals
d=int(sys.argv[1]); M=int(sys.argv[2]); KL=int(sys.argv[3])
def Fval(D,E,d):
    c=0
    for w in E:
        for a in range(d):
            t=list(w)
            while True:
                t[a]+=1
                if tuple(t) not in D: break
            t[a]-=1
            if tuple(t) not in E: c+=1
    return c
for m in range(3,M+1):
    tot=0; f1=f2=f3=0; any1=0; ex=None
    for D in downsets(m,d):
        Dl=sorted(D)
        if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
        for p in itertools.product(range(1,m),repeat=d):
            res={n:sum(x*y for x,y in zip(n,p))%m for n in Dl}
            if len(set(res.values()))!=m: continue
            for s in range(m):
                tot+=1
                ok_some=False
                for k in itertools.product(range(KL+1),repeat=d):
                    ph=[p[a]+m*k[a] for a in range(d)]
                    V={z:sum(x*q for x,q in zip(z,ph)) for z in Dl}
                    J=max(V.values())//m+1
                    Fs=[Fval(D,{z for z in Dl if V[z]<=s+j*m},d) for j in range(J+1)]
                    Ns=[sum(1 for z in Dl if V[z]>=(j+1)*m) for j in range(J+1)]
                    p1=all(Fs[j]>=Ns[j] for j in range(J+1))
                    if all(x==0 for x in k):
                        if not p1:
                            f1+=1
                            if ex is None: ex=(Dl,p,s,Fs,Ns)
                        if not all(sum(Fs[j:])>=sum(Ns[j:]) for j in range(J+1)): f2+=1
                        if not all(sum(Fs[:j+1])>=sum(Ns[:j+1]) for j in range(J+1)): f3+=1
                    if p1: ok_some=True
                any1+=ok_some
    print(f'd={d} m={m}: (tile,s) {tot}; standard lift: P1 fails {f1}, P2(tail) fails {f2}, P3(head) fails {f3}; P1 holds for some lift k<= {KL}: {any1}/{tot}',ex if ex and m<=5 else '',flush=True)
