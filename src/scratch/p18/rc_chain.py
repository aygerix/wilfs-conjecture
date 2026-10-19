"""B_chain criterion (lead): for each a, the a-chains of Ap (maximal progressions w, w+n_a, ... inside Ap).
B_chain = sum_a sum_{w in Ap} (M - top_a(w)),  top_a(w) = max{w + j n_a in Ap}.  Claims checked:
 (1) B = d m M - (d+1) sum Ap  >=  B_chain  >=  R = sum_{w,a} ((M-w) mod n_a)
 (2) distinct a-chains have distinct residues of M - w mod n_a
 (3) criterion CH-CHAIN: B_chain >= (d-1) m (m-1)/2 ==> W >= 0 ; coverage vs RC on the given list / random
usage: python rc_chain.py seed trials e mlo mhi Kmax cluster(0/1)"""
import sys, heapq, random, math
def apery(m, gens):
    w = [None]*m; w[0] = 0; pq = [(0, 0)]
    while pq:
        dd, r = heapq.heappop(pq)
        if dd > w[r]: continue
        for n in gens:
            r2 = (r+n) % m
            if w[r2] is None or dd+n < w[r2]:
                w[r2] = dd+n; heapq.heappush(pq, (dd+n, r2))
    return w
def analyse(m, gens):
    w = apery(m, [m]+gens)
    inS = lambda x: x >= 0 and x >= w[x % m]
    for n in gens:
        if n != w[n % m] or any(inS(a) and inS(n-a) for a in range(m, n-m+1)): return None
    d = len(gens); M = max(w); c = M - m + 1; q = -(-c//m); ap = set(w)
    ell = sum(1 for x in range(c) if inS(x)); W = (d+1)*ell - c
    B = d*m*M - (d+1)*sum(w); need2 = (d-1)*m*(m-1)
    R = 0; Bc = 0; ok2 = True
    for a in gens:
        tops = {}
        for x in w:
            t = x
            while t + a in ap: t += a
            Bc += M - t; R += (M - x) % a
            tops.setdefault(t, 0)
        res = [(M - t) % a for t in tops]
        if len(set(res)) != len(res): ok2 = False
    assert 2*B == 2*m*W + need2
    assert B >= Bc >= R, (m, gens)
    return dict(W=W, c=c, q=q, R=2*R/need2, Bc=2*Bc/need2, B=2*B/need2, ok2=ok2)
rng = random.Random(int(sys.argv[1])); T = int(sys.argv[2]); e = int(sys.argv[3]); mlo, mhi, Kmax = int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]); cl = int(sys.argv[7]); d = e-1
st = {'S': 0, 'RC': 0, 'BC': 0, 'chain_res_distinct_fail': 0}; worst = []
for _ in range(T):
    m = rng.randint(mlo, mhi)
    if cl:
        span = rng.randint(d, max(d, m//rng.choice([2, 4, 8, 16])))
        base = rng.randint(m+1, Kmax*m)
        gens = sorted(set(base + o for o in rng.sample(range(span+1), d)))
    else:
        gens = sorted(set(rng.randint(m+1, Kmax*m) for _ in range(d)))
    if len(gens) != d or math.gcd(m, *gens) != 1: continue
    r = analyse(m, gens)
    if not r or r['q'] < 5: continue
    st['S'] += 1; st['RC'] += r['R'] >= 1; st['BC'] += r['Bc'] >= 1
    if not r['ok2']: st['chain_res_distinct_fail'] += 1
    worst.append((round(r['Bc'], 3), round(r['R'], 3), round(r['B'], 3), m, gens, r['q']))
worst.sort()
print('e=%d m=[%d,%d] Kmax=%d clustered=%d (q>=5):' % (e, mlo, mhi, Kmax, cl), st)
print(' lowest B_chain/need (Bc, R, B, m, gens, q):')
for x in worst[:8]: print('   ', x)
