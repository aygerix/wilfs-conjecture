"""Independent sparse verification of a complete WRAP-MAX counterexample.

Reads the saved selected triples; constructs every core cell and every
missing-label spike.  Computes maximality, T, S and Lambda from the actual
upper-cover incidences, not from the proposed slack formula.  It separately
computes the window, shadow, degree and beta/tau versions.
Usage: python verify_counter.py results/sidon_counter2.json
"""
import collections
import itertools
import json
import sys


def main():
    with open(sys.argv[1]) as f:z=json.load(f)
    m=z['m'];P=tuple(z['P']);k=len(P);rho=z['rho'];theta=m-rho
    assert len(set(P))==k and all(1<=p<m for p in P)
    # Sparse monomials are sorted tuples of their factor indices.
    C={()}
    C.update((a,) for a in range(k))
    C.update(itertools.combinations_with_replacement(range(k),2))
    triples=set(map(tuple,z['triple_indices']))
    assert all(len(y)==3 and tuple(sorted(y))==y for y in triples)
    C.update(triples)
    assert len(C)==z['core_cells']
    vals={x:sum(P[a] for a in x) for x in C}
    corelabs={v%m for v in vals.values()}
    assert len(corelabs)==len(C)
    missing=[j for j in range(m) if j not in corelabs]
    assert 0 not in missing and missing==z['spike_labels']
    s=len(missing);d=k+s
    cells=set(C)
    cells.update((k+a,) for a in range(s))
    PP=P+tuple(missing)
    v=dict(vals)
    v.update({(k+a,):j for a,j in enumerate(missing)})
    assert len(cells)==m
    assert {w%m for w in v.values()}==set(range(m))
    load=collections.Counter()
    up=collections.Counter()
    uppers=collections.defaultdict(set)
    for y in cells:
        mult=collections.Counter(y)
        for a,mu in mult.items():
            x=list(y);x.remove(a);x=tuple(x)
            assert x in cells
            load[x]+=mu
            up[x]+=1
            uppers[x].add(a)
    N={x for x in cells if up[x]}
    A=cells-N
    assert all(v[x]<m for x in N)
    assert all(v[x]<2*m for x in A)
    V={x for x in A if v[x]>=m}
    assert V==triples
    r={x:(v[x]+rho)%m for x in cells}
    T={x:d+len(x)-load[x] for x in cells}
    assert all(T[x]>=0 for x in cells)
    assert sum(T.values())==d*m
    assert sum(T[x]*v[x] for x in cells)==(d+1)*sum(v.values())
    M=m*(m-1)//2
    S=(d+1)*M-sum((d+len(y))*r[y] for y in A)
    Lam=sum(T[x]*r[x] for x in N)
    W={x for x in cells if r[x]<rho}
    assert len(W)==rho
    qwindow=sum(T[x]-d for x in W)+sum(len(y)-1 for y in V)
    low={x for x in cells if v[x]<theta}
    # FIRST-ID for the shadow; immediate-parent version for the exit count.
    boundary=exits=0
    for x in cells:
        if v[x]<theta:continue
        for a,mu in collections.Counter(x).items():
            if v[x]-PP[a]<theta:
                boundary+=mu
                exits+=1
    highV={y for y in V if v[y]-m>=theta}
    qshadow=boundary+sum(len(y) for y in highV)-len(V)
    qexit=exits+sum(len(y) for y in highV)-len(V)
    # Direct beta and tau.  Singleton columns contribute zero below their tops,
    # so only directions in a top's support have to be listed.
    beta=0
    for t in N & W:
        for a,mu in collections.Counter(t).items():
            if a in uppers[t]:continue
            for j in range(1,mu+1):
                x=list(t)
                for _ in range(j):x.remove(a)
                x=tuple(x)
                beta += x not in W
    tau=collections.Counter()
    for y in A:
        nb=0
        for a,mu in collections.Counter(y).items():
            for j in range(1,mu+1):
                x=list(y)
                for _ in range(j):x.remove(a)
                nb+=tuple(x) in W
        K=(v[y]+rho)//m
        tt=(len(y)-1)*K+(y in W)-nb
        tau[tt]+=1
    budget=beta+sum(tt*num for tt,num in tau.items())
    assert S-Lam==m*qwindow==m*qshadow==m*budget
    assert qwindow==z['H1_slack']<0
    assert sum(v[x]//m for x in cells)==len(V)
    mass=sum(len(y)-1 for y in A)
    allphase_bound=(d+1)*len(N)*(len(N)-1)//2-(m-1)*mass
    assert allphase_bound>0
    ans=dict(verified=True,m=m,d=d,core_dimension=k,spikes=s,core_cells=len(C),
        height=max(map(len,cells)),rho=rho,theta=theta,wrapped_maximals=len(V),
        min_canonical_unit=min(PP),min_core_unit=min(P),
        nonmaximals=len(N),maximals=len(A),S=S,Lambda_r=Lam,
        S_minus_Lambda=S-Lam,normalized_slack=qwindow,
        boundary=boundary,exits=exits,exit_slack=qexit,window_cells=len(W),
        beta_N=beta,tau_distribution=dict(sorted(tau.items())),
        bad_F=tau[-1],tau_positive=sum(tt*num for tt,num in tau.items() if tt>0),
        core_pairs=k*(k+1)//2,covered_pairs=sum(len(x)==2 for x in N),
        maximal_pairs=sum(len(x)==2 for x in A),
        pure_cubics=sum(len(set(y))==1 for y in triples),
        mixed_cubics=sum(len(set(y))==2 for y in triples),
        squarefree_cubics=sum(len(set(y))==3 for y in triples),
        max_nonmax_lift=max(v[x] for x in N),min_wrap_lift=min(v[x] for x in V),
        max_wrap_lift=max(v[x] for x in V),maxcl_positive=S>=0,
        maximal_excess_mass=mass,allphase_maxcl_lower_bound=allphase_bound)
    print(json.dumps(ans,sort_keys=True))


if __name__=='__main__':main()
