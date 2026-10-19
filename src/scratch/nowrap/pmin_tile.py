"""Wrap number of factorization tiles (lead, 2026-10-19).
Wilf needs MaxCL only at sigma = c mod m and only for SOME factorization tile (Lean: wilf_of_tileTOPAt_of_isFactTile).
For a monomial order <, the <-least factorizations of the Apery elements form a factorization tile D_<.
Orders used: grlex; 'P-min' = weight x.P (P_a = n_a mod m) refined by grlex.  E(D) = sum_D floor(x.P/m);
the P-min tile minimizes E over all factorization tiles, and E = 0 implies MaxCL at every sigma (phase-free NO-WRAP).
Reports, per random S: E(grlex), E(Pmin), MaxCL at sigma = c and min over sigma for both tiles, Wilf defect.
usage: python pmin_tile.py seed trials mmin mmax"""
import sys, random, heapq

def apery(m, gens):
    dist = [None]*m; dist[0] = 0; pq = [(0, 0)]
    while pq:
        dv, i = heapq.heappop(pq)
        if dv > dist[i]: continue
        for g in gens:
            j = (i+g) % m; nd = dv+g
            if dist[j] is None or nd < dist[j]: dist[j] = nd; heapq.heappush(pq, (nd, j))
    return dist

def minimal_gens(m, gens):
    ap = apery(m, gens); ins = lambda x: x >= 0 and x >= ap[x % m]
    out = []
    for g in sorted(set(gens)):
        if g % m == 0: continue
        if any(h != g and ins(g-h) for h in [m]+list(gens)): continue
        out.append(g)
    return out, ap

def tile(m, n, ap, key):
    d = len(n); best = {0: (0,)*d}
    for w in sorted(ap)[1:]:
        cands = []
        for a in range(d):
            u = w-n[a]
            if u in best:
                x = list(best[u]); x[a] += 1; cands.append(tuple(x))
        best[w] = min(cands, key=key)
    return best  # w -> x

def maxcl(m, D, P):
    d = len(P); Ds = set(D)
    A = [y for y in D if all(tuple(y[i]+(i == a) for i in range(d)) not in Ds for a in range(d))]
    M1 = m*(m-1)//2; res = []
    for sg in range(m):
        res.append((d+1)*M1-sum((d+sum(y))*((sum(y[i]*P[i] for i in range(d))-sg) % m) for y in A))
    return res

if __name__ == '__main__':
    seed, T, mmin, mmax = map(int, sys.argv[1:5]); rng = random.Random(seed)
    stats = dict(n=0, E0_grlex=0, E0_pmin=0, neg_c=0, neg_any=0, same=0)
    hist = {}
    for tr in range(T):
        m = rng.randint(mmin, mmax); k = rng.randint(2, 7)
        gens = [rng.randint(m+1, rng.choice([2, 3, 5])*m) for _ in range(k)]
        if None in apery(m, gens): continue
        n, ap = minimal_gens(m, gens)
        if len(n) < 2: continue
        n, ap = minimal_gens(m, n)
        d = len(n); P = [g % m for g in n]
        c = max(ap)-m+1; g_ = sum(w//m for w in ap); ell = c-g_; W = (d+1)*ell-c
        grlex = lambda x: (sum(x), tuple(-t for t in x))
        pkey = lambda x: (sum(x[i]*P[i] for i in range(d)), sum(x), tuple(-t for t in x))
        out = []
        for key in (grlex, pkey):
            tb = tile(m, n, ap, key); D = list(tb.values())
            E = sum(sum(x[i]*P[i] for i in range(d))//m for x in D)
            S = maxcl(m, D, P)
            out.append((E, S[c % m], min(S), set(D)))
        stats['n'] += 1; stats['E0_grlex'] += out[0][0] == 0; stats['E0_pmin'] += out[1][0] == 0
        stats['same'] += out[0][3] == out[1][3]
        stats['neg_c'] += min(out[0][1], out[1][1]) < 0; stats['neg_any'] += min(out[0][2], out[1][2]) < 0
        if min(out[0][1], out[1][1]) < 0 or min(out[0][2], out[1][2]) < 0: print("NEG", m, n, out[0][:3], out[1][:3])
        b = out[1][0]*1.0/m; hist[min(int(b*4), 12)] = hist.get(min(int(b*4), 12), 0)+1
        assert W >= 0, (m, n)
    print(stats); print("histogram of E(Pmin)/m in quarters:", sorted(hist.items()))
