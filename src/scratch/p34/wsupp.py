r"""Check the PROVED bound W >= Dep - kappa0 + N(sigma_c) >= Dep - Sigma_supp (lead, 2026-10-20) on random S with an
independent brute-force W, and report coverage of the shape criterion Sigma_supp <= Dep (and kappa0 <= Dep) by regime.
Usage: python wsupp.py NS SEED MMIN MMAX"""
import sys, random
sys.path.insert(0, '.')
from tile import build
def brute(m, G):
    T = 40 * max(G)
    S = bytearray(T); S[0] = 1
    for x in range(1, T): S[x] = any(x >= g and S[x - g] for g in [m] + G)
    gaps = [x for x in range(T) if not S[x]]; c = max(gaps) + 1 if gaps else 0; g = len(gaps)
    mg = [x for x in [m] + G if not any(S[x - y] and S[y] for y in range(1, x))]
    return c, g, len(mg)
NS, SEED, MMIN, MMAX = map(int, sys.argv[1:5]); rnd = random.Random(SEED); cnt = 0
st = {}; mins = {}
while cnt < NS:
    m = rnd.randint(MMIN, MMAX); c0 = rnd.randint(m + 1, 9 * m)
    G = sorted(rnd.sample(range(m + 1, c0 + m), rnd.randint(2, min(14, c0 - 2))))
    R = build(m, G)
    if R is None: continue
    c, gens, M = R; N = len(gens)
    if N < 2: continue
    cb, gb, eb = brute(m, gens); assert cb == c and eb == N + 1
    W = eb * (cb - gb) - cb
    cnt += 1; D = list(M); Ds = set(D); delta = [x % m for x in gens]
    up = lambda x, b: tuple(x[t] + (t == b) for t in range(N))
    mx = {x for x in D if all(up(x, b) not in Ds for b in range(N))}
    K = {}
    for a in range(N):
        for x in D:
            k = 0; y = x
            while up(y, a) in Ds: y = up(y, a); k += 1
            K[(x, a)] = (k, y)
    dep = sum(x[a] + 1 for x in D for a in range(N) if K[(x, a)][0] == 0 and x not in mx)
    k0 = sum(sum((x[a] * delta[a]) % m for a in range(N)) // m for x in D)
    ss = sum(max(0, sum(1 for t in x if t) - 1) for x in D)
    lab = {x: (M[x] - c) % m for x in D}
    Nc = sum(1 for x in D for a in range(N) if K[(x, a)][0] and lab[x] > lab[K[(x, a)][1]])
    assert W >= dep - k0 + Nc >= dep - ss, (m, gens, c, W, dep, k0, Nc, ss)
    reg = 'open' if (3 * (N + 1) < m and c > 4 * m) else 'other'
    s = st.setdefault(reg, [0, 0, 0]); s[0] += 1; s[1] += ss <= dep; s[2] += k0 <= dep
    r = (dep - ss) / m
    if reg not in mins or r < mins[reg][0]: mins[reg] = (r, m, gens, c, dep, ss, k0, W)
for reg in st: print("%s: n %d  Sigma_supp <= Dep %d  kappa0 <= Dep %d  min (Dep - Ssupp)/m %s" % (reg, st[reg][0], st[reg][1], st[reg][2], mins[reg]))
print("bound W >= Dep - kappa0 + N_c >= Dep - Sigma_supp asserted on all %d S (brute-force W)" % cnt)
