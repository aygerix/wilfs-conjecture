"""Per-generator RC terms (lead, 2026-10-19).
RC  <=>  sum_a tau_a <= C2,  tau_a := n_a*Phi_a - m*ell,  Phi_a = #{x in L : (M - x) mod n_a < m}
       = sum_{j>=1} |S cap ([c, c+m) - j n_a)|.
Candidate tau-RES: tau_a <= b_a := n_a mod m for every minimal generator n_a != m (sum would give RC since the b_a are
distinct nonzero residues).  Tests the candidate on random and structured semigroups; reports the worst excess.
usage: python tau_test.py N seed"""
import sys, random, heapq
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
def analyse(m, gens_in):
    w = apery(m, [m] + gens_in)
    if any(x is None for x in w): return None
    M = max(w); c = M - m + 1; q = -(-c//m)
    gens = sorted(x for x in w if x > 0 and not any(w[j] + w[(x - w[j]) % m] == x for j in range(1, m) if (x - w[j]) % m))
    d = len(gens)
    if d < 2: return None
    inS = lambda x: x >= 0 and x >= w[x % m]
    L = [x for x in range(c) if inS(x)]; ell = len(L)
    C2 = m*(m-1)//2
    taus = []
    for n in gens:
        Phi = sum(1 for x in L if (M - x) % n < m)
        taus.append((n*Phi - m*ell, n % m, n, Phi))
    W = (d+1)*ell - c
    return dict(m=m, d=d, e=d+1, c=c, q=q, ell=ell, W=W, taus=taus, rc=sum(t[0] for t in taus) <= C2, C2=C2, gens=gens)
def rand_gens(rng):
    m = rng.randint(6, 60); kind = rng.random()
    if kind < 0.35:   # level-1 heavy
        k = rng.randint(2, max(2, m//3)); g = rng.sample(range(m+1, 2*m), min(k, m-1))
    elif kind < 0.7:  # mixed levels
        k = rng.randint(2, max(2, m//3)); top = rng.randint(2, 6)*m; g = rng.sample(range(m+1, top), min(k, top-m-1))
    else:             # interval-ish
        lev = rng.randint(1, 4); a = rng.randint(1, m-2); b = rng.randint(a, min(m-1, a + rng.randint(1, m//2)))
        g = list(range(lev*m + a, lev*m + b + 1)) + ([rng.randint(m+1, 5*m)] if rng.random() < 0.5 else [])
    return m, g
if __name__ == '__main__':
    N = int(sys.argv[1]); rng = random.Random(int(sys.argv[2]))
    tested = 0; viol = 0; worst = None; rcfail = 0; worst_rel = None
    bylev = {}
    for _ in range(N):
        m, g = rand_gens(rng)
        r = analyse(m, g)
        if not r or r['q'] < 2: continue
        tested += 1
        if not r['rc']: rcfail += 1
        for (tau, b, n, Phi) in r['taus']:
            lev = n // m
            ex = tau - b
            bl = bylev.setdefault(min(lev, 4), [0, 0, None])
            bl[0] += 1
            if ex > 0:
                viol += 1; bl[1] += 1
                if bl[2] is None or ex/r['C2'] > bl[2][0]: bl[2] = (ex/r['C2'], ex, m, n, r['q'], r['e'], r['gens'][:12])
            if worst is None or ex > worst[0]: worst = (ex, m, n, r['q'], r['e'], r['gens'][:12])
    print('tested', tested, 'generator-terms violating tau<=b:', viol, ' RC failures:', rcfail)
    print('worst excess:', worst)
    for lev in sorted(bylev): print(' level', lev, 'terms', bylev[lev][0], 'violations', bylev[lev][1], 'worst rel', bylev[lev][2])
