"""Per-direction split of H1' (lead, 2026-10-19).  Shadow form: f(theta) = sum_b g_b(theta) - |V| >= 0 with
g_b(theta) = E_b(L_theta) + sum_{y in V, lam(y) >= theta} y_b.   PD_b[beta]: for an assignment beta: V -> directions
with beta(y) in supp(y), test  #{y in V : beta(y) = b} <= g_b(theta)  for every b and every theta.
Rules: 'maxP' (argmax P over supp, ties -> larger coordinate y_b, then index), 'minP', 'maxcoord'.
usage: python wm_perdir.py cert mlo mhi certdir | rand seed trials mmin mmax dmin dmax"""
import sys, random, gzip, json
from math import gcd
RULES = ['maxP', 'minP', 'maxcoord', 'maxPy']

def analyze(m, P, D, st):
    d = len(P); Ds = set(D)
    up = lambda x, a: tuple(x[i]+(i == a) for i in range(d))
    A = set(y for y in D if all(up(y, a) not in Ds for a in range(d)))
    v = {x: sum(x[i]*P[i] for i in range(d)) for x in D}
    if any(v[x] >= m for x in D if x not in A): return False
    V = [y for y in A if v[y] >= m]
    if not V: return True
    st['tiles'] += 1
    top = {}
    for b in range(d):
        for x in D:
            y = x
            while up(y, b) in Ds: y = up(y, b)
            top[(x, b)] = y
    beta = {}
    for rule in RULES:
        bb = {}
        for y in V:
            S = [b for b in range(d) if y[b] > 0]
            if rule == 'maxP': bb[y] = max(S, key=lambda b: (P[b], y[b], -b))
            elif rule == 'minP': bb[y] = min(S, key=lambda b: (P[b], -y[b], b))
            elif rule == 'maxcoord': bb[y] = max(S, key=lambda b: (y[b], P[b], -b))
            else: bb[y] = max(S, key=lambda b: (P[b]*y[b], P[b], -b))
        beta[rule] = bb
    Vset = set(V)
    for th in range(1, m+1):
        L = set(x for x in D if x not in Vset and v[x] < th)
        g = [sum(1 for x in L if top[(x, b)] not in L)+sum(y[b] for y in V if v[y]-m >= th) for b in range(d)]
        st['inst'] += 1
        assert sum(g) >= len(V), ("H1' FAIL", m, P, th)
        for rule in RULES:
            cnt = [0]*d
            for y in V: cnt[beta[rule][y]] += 1
            bad = [b for b in range(d) if cnt[b] > g[b]]
            if bad:
                st['fail_'+rule] += 1
                if st['fail_'+rule] <= 2: print("PD FAIL", rule, m, P, "theta", th, "b", bad, "cnt", cnt, "g", g, sorted(D), flush=True)
    return True

def newst():
    s = dict(tiles=0, inst=0)
    for r in RULES: s['fail_'+r] = 0
    return s

if __name__ == '__main__':
    if sys.argv[1] == 'cert':
        mlo, mhi, cdir = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        for m in range(mlo, mhi+1):
            st = newst(); units = [u for u in range(1, m) if gcd(u, m) == 1]
            with gzip.open(f'{cdir}/certificate_all_{m}.jsonl.gz', 'rt') as fh:
                for line in fh:
                    rec = json.loads(line); r0 = [x % m for x in rec['r']]
                    if 0 in r0: continue
                    for Dl in rec['tile_cells']:
                        D = list(map(tuple, Dl))
                        for u in units: analyze(m, [(u*x) % m for x in r0], D, st)
            print("m=%d" % m, st, flush=True)
