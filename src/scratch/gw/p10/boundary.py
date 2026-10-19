#!/usr/bin/env python3
"""Exact boundary-height falsification and certificate; run on fejer only."""
import argparse, heapq, itertools, json, math, random
from collections import Counter

ZERO = (0, 0, 0, 0)
UNITS = [tuple(int(a == b) for a in range(4)) for b in range(4)]

def add(x, a):
    y = list(x); y[a] += 1
    return tuple(y)

def degree_floor(n, r, copies=1):
    """Smallest sum of degrees of n distinct points in copies of N^r."""
    j = total = 0
    while n:
        take = min(n, copies * math.comb(j + r - 1, r - 1))
        total += j * take; n -= take; j += 1
    return total

def convex_choose_sum(S, q):
    S=max(0,S); a,b=divmod(S,q)
    return q*a*(a-1)//2+b*a

def axis_floor(n1,n2):
    return convex_choose_sum(3*n1-n2-6,12)

def stats(D):
    D = set(D)
    Ht, Top, local = {}, {}, {}
    ts, ns = [0]*5, [0]*5
    for x in sorted(D, key=sum, reverse=True):
        Ht[x] = max([1 + Ht[add(x,a)] for a in range(4) if add(x,a) in D] or [0])
        for a in range(4):
            Top[x,a] = Top[add(x,a),a] if add(x,a) in D else x
        su = sum(v > 0 for v in x); ns[su] += 1
        if Ht[x] == 0: ts[su] += 1
    for x in D: local[x] = sum(Ht[Top[x,a]] for a in range(4))
    return sum(local.values()), ts, ns, Ht, local

def check(D):
    H, t, n, ht, local = stats(D); m = len(D)
    assert n[4] == 0
    assert 6*H >= 12*m - 15*t[1] - 20*t[2] - 36*t[3], (D, H,t,n,'BH2')
    assert 12*n[2] >= t[2]**2 + 6*t[2], (D,H,t,n,'TYPE2')
    a = 6*n[3] - 3*t[3]
    assert a >= 0 and a*a >= t[3]**2 * (2*t[3]+1), (D,H,t,n,'TYPE3')
    assert 3*H >= degree_floor(n[3],3,4), (D,H,t,n,'G3')
    if not n[3]:
        assert 4*H >= 12*m - 15*t[1] - 24*t[2], (D,H,t,n,'BH3')
        assert H >= degree_floor(n[2],2,6)+axis_floor(n[1],n[2]), (D,H,t,n,'G2-AXIS')
    return H, t, n

def downset(maxima):
    return set(itertools.chain.from_iterable(itertools.product(*(range(z+1) for z in y)) for y in maxima))

def random_boundary(rng, m, support=3):
    D = {ZERO}; frontier = set(UNITS)
    for i in range(m-1):
        front = sorted(frontier)
        # Mixture of uniform growth, deep columns, and nearly rank-flat growth.
        if i % 4 == 0: x = min(front, key=lambda x: (sum(x), rng.random()))
        elif i % 4 == 1: x = max(front, key=lambda x: (max(x), rng.random()))
        else: x = rng.choice(front)
        D.add(x); frontier.remove(x)
        for a in range(4):
            y = add(x,a)
            if y in D or sum(v>0 for v in y)>support: continue
            if all(tuple(v-int(a==b) for a,v in enumerate(y)) in D for b in range(4) if y[b]):
                frontier.add(y)
    return D

def apery(m, gens, grlex=False):
    dist = [None]*m; fact = [None]*m
    dist[0] = 0; fact[0] = ZERO
    heap = [(0, (0, ZERO) if grlex else ZERO, 0)]
    while heap:
        v, tie, r = heapq.heappop(heap)
        if dist[r] != v or tie != ((sum(fact[r]),fact[r]) if grlex else fact[r]): continue
        for a,g in enumerate(gens):
            nr = (r+g)%m; nv = v+g; nx = add(fact[r],a)
            nt = (sum(nx),nx) if grlex else nx
            ot = ((sum(fact[nr]),fact[nr]) if grlex else fact[nr]) if fact[nr] is not None else None
            if dist[nr] is None or nv < dist[nr] or (nv == dist[nr] and nt < ot):
                dist[nr] = nv; fact[nr] = nx; heapq.heappush(heap,(nv,nt,nr))
    if any(v is None for v in dist): return None
    for g in gens:
        if any(g-h >= dist[(g-h)%m] for h in [m]+gens if h<g): return None
    return set(fact), dist

def randomized(seed, count):
    rng = random.Random(seed); shapes = semis = boundary_semis = two_semis = 0
    for j in range(count):
        m = rng.randrange(5,501)
        D = random_boundary(rng,m,2 if j%3==0 else 3)
        check(D); shapes += 1
    # Explicit flat-boundary stress families and boxes glued along faces.
    for h in range(1,13):
        D = {x for x in itertools.product(range(h+1),repeat=4) if sum(x)<=h and 0 in x}
        check(D); shapes += 1
    for j in range(count):
        m = rng.randrange(40,1001)
        mode = j%5
        if mode == 0: gens = sorted(rng.sample(range(m+1,2*m),4))
        elif mode == 1:
            b = rng.randrange(1,max(2,m//8)); step=rng.randrange(1,max(2,m//8))
            gens=sorted(set([m+b,m+b+step,m+b+2*step,rng.randrange(2*m,20*m)]))
        elif mode == 2:
            gens=sorted(rng.sample(range(m+1,4*m),3)+[rng.randrange(8*m,30*m)])
        elif mode == 3:
            gens=sorted(rng.sample(range(2*m,15*m),4))
        else:
            a,b=rng.randrange(1,m),rng.randrange(1,m)
            gens=sorted(set(m+(v%m) for v in [a,b,a+b,a+2*b] if v%m))
        if len(gens)!=4: continue
        for grlex in [False,True]:
            ap = apery(m,gens,grlex)
            if ap is None: continue
            D, w = ap; semis += 1
            if all(0 in x for x in D):
                H,t,n=check(D); boundary_semis+=1
                two_semis += n[3]==0
    print(json.dumps(dict(seed=seed,random_shapes=shapes,semigroup_tiles=semis,
        boundary_semigroup_tiles=boundary_semis,two_support_tiles=two_semis)))

def rank_profile_certificate(mlo, mhi, support):
    """Enumerate necessary support profiles and certify the height/rank criterion.
    Floating point is not used in pruning or the final inequality.
    """
    survivors=[]; tested=0
    for m in range(mlo,mhi+1):
        left=[]
        for t1 in range(5):
            for t2 in range(math.isqrt(12*m)+1):
                n2min=(t2*t2+6*t2+11)//12
                for t3 in (range(m+1) if support==3 else [0]):
                    # Minimize n3 across the four positive three-faces.
                    a=math.isqrt(2*t3+1)
                    if a*a<2*t3+1:a+=1
                    # Exact ceiling using the squared condition, not rounded root.
                    n3min=(3*t3)//6
                    while (6*n3min-3*t3)<0 or (6*n3min-3*t3)**2 < t3*t3*(2*t3+1):n3min+=1
                    if 1+max(4,t1)+n2min+n3min>m:
                        if t3:break
                        continue
                    tested+=1
                    hb=max(0, (12*m-15*t1-20*t2-36*t3+5)//6)
                    if support==2:hb=max(hb,(12*m-15*t1-24*t2+3)//4)
                    # Minimal rank term at given support counts.
                    R=7*t3*(t3-1)//2+6*(t3*t2+t2*(t2-1)//2)+5*((t3+t2)*t1+t1*(t1-1)//2)
                    if (m+1)*hb+R>=3*m*(m-1)//2:continue
                    if support==2:
                        # n1+n2=m-1; large n1 also restricts t1 but is not spent here.
                        hb=max(hb,degree_floor(n2min,2,6))
                    else:hb=max(hb,(degree_floor(n3min,3,4)+2)//3)
                    if (m+1)*hb+R<3*m*(m-1)//2:left.append((t1,t2,t3))
        if left:survivors.append((m,len(left),left[:8]))
    print(json.dumps(dict(profile_tested=tested,survivors=survivors)))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--count',type=int,default=1000);p.add_argument('--seed',type=int,default=1019)
    p.add_argument('--profile',nargs=3,type=int)
    args=p.parse_args()
    if args.profile:rank_profile_certificate(*args.profile)
    else:randomized(args.seed,args.count)
