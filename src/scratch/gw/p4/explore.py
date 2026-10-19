"""Exact P4 discovery tests. Execute only on fejer, with nice.

Modes record counterexamples, not proof claims. All PRNG seeds explicit.
"""
import argparse
import itertools as it
import json
import random
import heapq
from collections import Counter


def stats(D, n, q):
    vs = [sum(xi * ni for xi, ni in zip(x, n)) for x in D]
    M = max(vs)
    F = lambda z: min(4, z // q)
    lhs = sum(map(F, vs))
    rhs = len(n) * sum(F(M - z) for z in vs)
    return dict(d=len(n), q=q, m=len(D), n=n, M=M,
                lhs=lhs, rhs=rhs, slack=rhs-lhs,
                residues=len({z % q for z in vs}),
                degree=max(map(sum, D)))


def quad_trials(trials, seed):
    rng = random.Random(seed)
    checked = high = payments = 0
    for _ in range(trials):
        d = rng.randrange(2, 13)
        q = rng.randrange(2, 101)
        n = tuple(rng.randrange(q+1, 6*q+1) for _ in range(d))
        D = [(0,)*d] + [tuple(int(i == j) for i in range(d)) for j in range(d)]
        for i in range(d):
            for j in range(i, d):
                if rng.randrange(3):
                    D.append(tuple(int(i == k)+int(j == k) for k in range(d)))
        s = stats(D, n, q)
        if s['M'] < 4*q-1:
            continue
        checked += 1
        if s['M']>=5*q-1:
            high+=1;F=lambda z:min(4,z//q);M=s['M']
            vals={x:sum(xi*ni for xi,ni in zip(x,n)) for x in D}
            used=set()
            for x in D:
                sep=sum(F(xi*ni) for xi,ni in zip(x,n))
                if sep>=F(vals[x]):continue
                dirs=[j for j in range(d) if x[j]]
                assert len(dirs)==2 and sum(x)==2
                a,b=sorted(dirs,key=lambda j:(n[j],j))
                assert q<n[a]<2*q and n[b]<3*q
                key=(b,a);assert key not in used;used.add(key)
                sl=F(M-n[a])+F(M-n[a]-n[b])-F(n[b])
                assert sl>=1;payments+=1
        if s['slack'] < 0:
            print(json.dumps(dict(counterexample=s, D=D)), flush=True)
            return
    print(json.dumps(dict(mode='quad', trials=trials, seed=seed, checked=checked,
                         high_theorem=high,payments=payments)), flush=True)


def simplex(d, k):
    return [x for x in it.product(range(k+1), repeat=d) if sum(x) <= k]


def independent_verify(D, n):
    m=len(D);d=len(n);zero=(0,)*d
    assert zero in D and all(ni>m for ni in n)
    V={x:sum(xi*ni for xi,ni in zip(x,n)) for x in D}
    assert len({z%m for z in V.values()})==m
    for x in D:
        for j in range(d):
            if x[j]:
                assert x[:j]+(x[j]-1,)+x[j+1:] in D
    out=stats(D,n,m)
    assert out['slack']>=0
    M=max(V.values())
    if M//m!=4:return out
    rho=5*m-1-M;classes=[(ni+rho)//m for ni in n]
    a,b,c,e=(classes.count(i) for i in range(1,5))
    short=[];quad={};cube={};four=0
    for x,v in V.items():
        band=(v+rho)//m
        assert (M-v)//m==4-band
        typ=tuple(sorted(j for j,xi in zip(classes,x) for _ in range(xi)))
        if sum(x)==2:
            assert (typ,band) in {((1,1),2),((1,1),3),((1,2),3),((1,2),4),
                ((1,3),4),((2,2),3),((2,2),4),((2,3),4)}
            quad[typ,band]=quad.get((typ,band),0)+1
            if (typ,band) in {((2,2),3),((2,3),4)}:short.append(v)
        if sum(x)==3:
            assert (typ,band) in {((1,1,1),3),((1,1,1),4),((1,1,2),4),
                ((1,2,2),4),((2,2,2),4)}
            cube[typ,band]=cube.get((typ,band),0)+1
            if typ in {(1,2,2),(2,2,2)}:short.append(v)
            if typ==(1,1,2):
                dv=v-sum(xi*ni for cl,xi,ni in zip(classes,x,n) if cl==2)
                if (dv+rho)//m==3:short.append(v)
        if sum(x)==4:assert typ==(1,1,1,1) and band==4;four+=1
        assert sum(x)<=4
    assert len(short)<=rho
    assert all((v%m+2*rho)%m<rho for v in short)
    out.update(a=a,b=b,c=c,e=e,rho=rho,short=len(short))
    q2=quad.get(((1,1),2),0);q3=quad.get(((1,1),3),0)
    s3=quad.get(((1,2),3),0);t3=quad.get(((2,2),3),0)
    u3=cube.get(((1,1,1),3),0);u4=cube.get(((1,1,1),4),0)
    WA=3*a*(a+1)+(2*a-2)*q2+(a-3)*(q3+u3)-4*(u4+four)
    T=a*b-s3+c*(c+1)+e*(3*a+2*b+c)+(c+e)*(2*q2+q3+s3+t3+u3)+b*u3
    Q=a*(a+1)//2
    assert out['slack']>=WA+T
    assert 3*WA>=18*(Q-q2-q3)-(a-1)*q3
    if a<=1:assert WA>=0
    if a==2 and WA<0:assert (WA,q2,q3,u3,u4,four)==(-1,0,3,0,4,0)
    if a==3 and WA<0:assert (WA,q2,q3,u3,u4,four)==(-4,0,6,0,10,0)
    out.update(WA=WA,transfer=T)
    if max(map(sum,D))<=2 and d>=3:
        bound=3*a*(a+1)+a*b+c*(c+1)+e*(3*a+2*b+c)
        assert out['slack']>=bound
    if a==0:
        t=quad.get(((2,2),3),0)
        assert out['slack']>=c*(c+1)+e*(2*b+c)+(c+e)*t
    Q=a*(a+1)//2;U=a*(a+1)*(a+2)//6
    if rho==0 and a>=2 and quad.get(((1,1),3),0)==Q and cube.get(((1,1,1),4),0)==U:
        B=[0]+[ni%m for cl,ni in zip(classes,n) if cl==1]
        signed={ (x+y-z)%m for z in B for x,y in it.combinations_with_replacement([t for t in B if t!=z],2)}
        assert signed.isdisjoint(B)
        assert len(signed)==len(B)*len(B)*(len(B)-1)//2
        assert m>=len(signed)+len(B)
        F=a*(a+1)*(a-1)//6;k=d-a
        assert 3*k>a-1 and out['slack']>=-F+k*Q>0
        out['saturated']=True
    return out


def tile(n, costs):
    m=tile.modulus;d=len(n);zero=(0,)*d
    dist={0:(0,zero)};todo=[(0,zero,0)]
    while todo:
        cost,x,r=heapq.heappop(todo)
        if (cost,x)!=dist[r]:continue
        for j in range(d):
            y=x[:j]+(x[j]+1,)+x[j+1:];s=(r+n[j])%m
            val=(cost+costs[j],y)
            if s not in dist or val<dist[s]:
                dist[s]=val;heapq.heappush(todo,(val[0],y,s))
    if len(dist)!=m:return None
    D={x for cost,x in dist.values()}
    active=[j for j in range(d) if any(x[j] for x in D)]
    return {tuple(x[j] for j in active) for x in D},tuple(n[j] for j in active)


def random_tiles(trials,seed):
    rng=random.Random(seed);hist=Counter();examples=[]
    for i in range(trials):
        d=rng.randrange(5,11);m=rng.randrange(d+1,121)
        n=tuple(m*rng.randrange(1,5)+r for r in rng.sample(range(1,m),d))
        costs=n if i%2 else tuple(rng.randrange(1,4*m) for _ in n)
        tile.modulus=m;result=tile(n,costs)
        if result is None:continue
        D,nn=result
        if not 5<=len(nn)<=10:continue
        s=independent_verify(D,nn);hist['checked']+=1;hist[f'd{len(nn)}']+=1
        hist[f'K{s["M"]//m}']+=1
        if s['M']//m==4:
            hist['primary']+=1;hist['rho_zero']+=s['rho']==0
            hist['rho_near_m']+=s['rho']*5>=4*m
            hist['negative_A_face']+=s['WA']<0
            hist['transfer_alone_insufficient']+=s['WA']+s['transfer']<0
            if len(examples)<3:examples.append(s)
    print(json.dumps(dict(mode='random_tiles',trials=trials,seed=seed,counts=hist,examples=examples)),flush=True)


def packing_trials(trials,seed):
    rng=random.Random(seed);hist=Counter()
    for _ in range(trials):
        m=rng.randrange(5,201);s=rng.randrange(3,9)
        B=(0,)+tuple(rng.sample(range(1,m),min(s-1,m-1)))
        pairs=list(it.combinations_with_replacement(B,2))
        if len({sum(x)%m for x in pairs})!=len(pairs):continue
        hist['B2']+=1
        triples=list(it.combinations_with_replacement(B,3))
        residues=Counter(sum(x)%m for x in triples)
        r=len(triples)-len(residues)
        signed={(x+y-z)%m for z in B for x,y in it.combinations_with_replacement([t for t in B if t!=z],2)}
        assert signed.isdisjoint(B)
        s=len(B);H=s*(s*(s-1)//2+1);J=min(9,s*s//4)
        assert len(signed)+s>=H-J*r*(r+1)//2
        if r<=1:hist[f'collision_excess_{r}']+=1
    print(json.dumps(dict(mode='packing',trials=trials,seed=seed,counts=hist)),flush=True)


def ef_trials(last):
    hist = Counter()
    for m in range(6, last+1):
        lo = (3*m+2)//2
        hi = (5*m-1)//3
        for a in (2, 3, 4):
            if hi-lo+1 < a:
                continue
            for A in it.combinations(range(lo, hi+1), a):
                # Construct the numerical semigroup <m,A> union [4m,infty).
                c = 4*m
                S = [False]*(c+m)
                S[0] = True
                for z in range(1, c):
                    S[z] = any(z >= w and S[z-w] for w in (m,)+A)
                if S[c-1]:
                    continue
                for z in range(c, c+m):
                    S[z] = True
                ap = [next(z for z in range(r, c+m, m) if S[z]) for r in range(m)]
                gens = [z for z in range(m, c+m) if S[z] and
                        not any(S[w] and S[z-w] for w in range(m, z//2+1))]
                ell = sum(S[:c])
                W = len(gens)*ell-c
                M = max(ap)
                assert M == 5*m-1
                assert W >= 0
                facevals={sum(xi*ni for xi,ni in zip(x,A)) for x in simplex(a,3)}
                F = [z for z in ap if z in facevals]
                L = sum((M-z)//m for z in F)
                WA = (a+1)*L-4*len(F)
                hist['semigroups'] += 1
                hist['negative_face'] += WA < 0
                hist['B3'] += len(F) == len(simplex(a,3))
                if len(F)==len(simplex(a,3)):
                    B=(0,)+tuple(z%m for z in A)
                    signed={(x+y-z)%m for z in B for x,y in it.combinations_with_replacement([t for t in B if t!=z],2)}
                    assert len(signed)==len(B)*len(B)*(len(B)-1)//2
                    assert signed.isdisjoint(B)
                    k=len(gens)-1-a;Q=a*(a+1)//2
                    deficit=a*(a+1)*(a-1)//6
                    assert 3*k>a-1 and W>=-deficit+k*Q>0
                    extra=tuple(z for z in ap if z not in facevals)
                    nn=A+extra;dd=len(nn)
                    assert set(gens)=={m,*nn}
                    DD={x+(0,)*len(extra) for x in simplex(a,3)}
                    DD.update(tuple(int(j==t) for j in range(dd)) for t in range(a,dd))
                    verified=independent_verify(DD,nn)
                    assert verified['WA']==WA and verified['slack']==W
                    hist['saturated_proof_checks']+=1
                if WA < 0 and hist['negative_face'] <= 3:
                    print(json.dumps(dict(mode='EF', m=m, A=A, e=len(gens),
                         ell=ell, W=W, WA=WA, face=len(F))), flush=True)
    print(json.dumps(dict(mode='EF', last=last, counts=hist)), flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--quad', type=int, default=0)
    p.add_argument('--ef', type=int, default=0)
    p.add_argument('--tiles', type=int, default=0)
    p.add_argument('--packing', type=int, default=0)
    p.add_argument('--seed', type=int, default=20261018)
    a = p.parse_args()
    if a.quad:
        quad_trials(a.quad, a.seed)
    if a.ef:
        ef_trials(a.ef)
    if a.tiles:
        random_tiles(a.tiles,a.seed)
    if a.packing:
        packing_trials(a.packing,a.seed)
