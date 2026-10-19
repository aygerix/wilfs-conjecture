"""Exact height-three core evaluator. All executions belong on fejer."""
from collections import Counter
from itertools import combinations_with_replacement
from math import comb


def evaluate(m, U, Q, T, rho):
    # U consists of residues at the phase under test, not original labels.
    k = len(U)
    Q = set(tuple(sorted(z)) for z in Q)
    T = set(tuple(sorted(y)) for y in T)
    assert all(tuple(y[:j]+y[j+1:]) in Q for y in T for j in range(3))
    assert {i for z in Q for i in z} == set(range(k))
    pfaces = {tuple(y[:j]+y[j+1:]) for y in T for j in range(3)}
    psi = Counter(tuple(y[:j]+y[j+1:]) for y in T for j in range(3))
    rp = {z:(sum(U[i] for i in z)-rho)%m for z in Q}
    rt = {y:(sum(U[i] for i in y)-2*rho)%m for y in T}
    vals = [rho]+list(U)+list(rp.values())+list(rt.values())
    assert len(vals)==len(set(vals))
    s = m-len(vals)
    assert s>=0
    d=k+s
    Kp = {z:(sum(U[i] for i in z)-rho)//m for z in Q}
    Kt = {y:(sum(U[i] for i in y)-2*rho)//m for y in T}
    deg=Counter(i for z in Q for i in z)
    delta=[k+1-deg[i] for i in range(k)]
    A=sum(delta[i]*U[i] for i in range(k))
    lp=A+s*sum(U)+sum((d+2-psi[z])*rp[z] for z in pfaces)
    OW=rho-sum(Kp[z]==-1 for z in Q-pfaces)
    B=2*sum(Kt.values())-sum((psi[z]-1)*Kp[z] for z in pfaces)
    pa=sum(Kp[z]==1 for z in Q-pfaces)
    HC=lp+m*(OW+B)
    S=(d+1)*(rho+sum(U)+sum(rp[z] for z in pfaces))-sum(rp[z] for z in Q-pfaces)-2*sum(rt.values())
    assert S==HC+m*pa
    bad=[]; gain=0; vtot=0
    for y in T:
        kap=2*Kt[y]-sum(Kp[tuple(y[:j]+y[j+1:])] for j in range(3))
        v=int(rt[y]>=m-rho)
        bv=kap+v
        assert bv>=-1
        if bv==-1: bad.append(y)
        gain+=max(bv,0)
        vtot+=v
    pm=sum(Kp[z]==-1 for z in pfaces)
    pp=sum(Kp[z]==1 for z in pfaces)
    orest=OW-pm-vtot
    assert orest>=0
    assert HC==lp+m*(orest+pp+gain-len(bad))
    D=[i for i in range(k) if delta[i]]
    v=len(D); g=k-v
    qD=sum(all(i in D for i in z) for z in Q)
    if v:
        assert comb(qD,2)<=v*A
    assert m>=k*(g+1)+1
    if len(T)==1 and OW+B<0:
        assert OW+B==-1
        assert all(Kp[z]==0 and rp[z]>=2 for z in pfaces)
        assert lp>=A+s*comb(k,2)+2*(d-1)
        assert lp>=A+s*(comb(k+1,2)-2)+2*(d-1)
    return dict(k=k,s=s,d=d,q=len(Q),p=len(pfaces),t=len(T),rho=rho,
                Lplus=lp,A=A,HC=HC,S=S,OW=OW,B=B,PAplus=pa,
                beta=len(bad),gain=gain,Pplus=pp,Orest=orest,
                delta=delta,g=g,v=v,e=comb(k+1,2)-len(Q),qD=qD)


def optimal_one(m, rho, U, y, forbid_positive=False):
    """Best Lplus for these unit residues and this single cubic in ONE-DEFICIT.

    Enumerate at most one pair per unused residue; choose the largest ordinary
    sum, which minimizes Lplus. Force all cubic faces and every window cell.
    """
    k=len(U); y=tuple(sorted(y)); b=sum(U[i] for i in y)-rho
    if not 0<b<rho: return None
    yr=m-rho+b
    faces={tuple(y[:j]+y[j+1:]) for j in range(3)}
    used={rho,*U,yr}
    if len(used)!=k+2: return None
    Q=set()
    for z in faces:
        w=sum(U[i] for i in z)-rho
        if not 0<=w<m-rho or w in used: return None
        used.add(w); Q.add(z)
    choices={}
    for z in combinations_with_replacement(range(k),2):
        if z in faces: continue
        w=sum(U[i] for i in z)-rho
        K=w//m; r=w%m
        if r in used: continue
        if r>=m-rho and K!=-1: continue
        if forbid_positive and K==1: continue
        if r not in choices or w>choices[r][0]: choices[r]=(w,z)
    if any(r not in choices for r in range(m-rho,m) if r!=yr): return None
    Q.update(z for _,z in choices.values())
    if {i for z in Q for i in z}!=set(range(k)): return None
    ans=evaluate(m,U,Q,{y},rho)
    assert ans['OW']+ans['B']==-1
    ans.update(U=list(U),Q=sorted(Q),T=[y],m=m)
    return ans
