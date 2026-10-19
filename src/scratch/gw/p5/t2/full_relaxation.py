"""Test whether all new scalar/arc constraints close a full-cubic relaxation.
fejer only. A surviving relaxed profile is not residue-complete.
"""
import numpy as np
import random,json,itertools as it
from math import comb
from functools import lru_cache
@lru_cache(None)
def mons(a):
    cells=[x for deg in range(4) for x in it.combinations_with_replacement(range(a),deg)]
    ids=np.full((len(cells),3),a,dtype=np.int32)
    deg=np.array([len(x) for x in cells])
    for i,x in enumerate(cells):ids[i,:len(x)]=x
    return ids,deg
def run(trials=10000,seed=202610199):
    rng=random.Random(seed);neg=0;arcs=0;surv=0;best=None
    for itn in range(trials):
        a=rng.randrange(7,41);m=comb(a+3,3);H=rng.randrange(m//2+1,(2*m-1)//3+1);h=3*H-m+1
        alpha=rng.randrange(2,a//2+1)
        t=sorted([rng.randrange((h+2)//3,(h+1)//2) for _ in range(alpha)]+
                 [rng.randrange((h+1)//2,H+1) for _ in range(a-alpha-1)]+[H])
        ids,dg=mons(a);tau=np.array(t+[0])[ids].sum(axis=1);rr=tau%m
        q2=int(np.sum((dg==2)&(tau<h)));u3=int(np.sum((dg==3)&(tau<h)));assert u3==0
        Q=comb(a+1,2);F=comb(a+1,3);LC=(a+1)*q2;WA=-F+LC;rho=m-h;Wband=WA+rho
        if Wband>=0:continue
        neg+=1
        bad=~((dg==2)&(tau>=h));freq=np.bincount(rr[bad],minlength=m);pref=np.r_[0,np.cumsum(freq)]
        def intr(HH):
            th=h+HH
            return int(pref[min(th,m)]-pref[h]+(pref[max(1,th-m)]-pref[1] if th>m else 0))
        arcmargin=min(Q-q2+intr(HH)+1-HH for HH in set(t) if 2*HH>=h)
        if arcmargin<0:continue
        arcs+=1
        sr=int(np.sum((rr-2*h)%m<rho))
        if sr>rho:continue
        surv+=1
        out=dict(a=a,m=m,h=h,t=t,q2=q2,LC=LC,WA=WA,Wband=Wband,
                 arcmargin=arcmargin,sr=sr,rho=rho,distinct_residues=int(len(set(rr))))
        if best is None or Wband<best['Wband']:best=out
    print(json.dumps(dict(seed=seed,trials=trials,negative_band=neg,all_high_arcs=arcs,
                          high_arcs_and_full_short_interval=surv,best=best)),flush=True)
if __name__=='__main__':run()
