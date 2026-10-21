r"""Assert every step of  CH' => DEP bound => CR_DEP  on random S (lead, 2026-10-20):
 (1) m W = (d+1)M' - sum_b sum_{b-cols} |C| (w(top) - c)                      [CH', exact]
 (2) w(t) - c <= r(t) on maximal tops, <= r(t) - m on non-maximal tops        [hence mW >= (d+1)M' - sum omega rt]
 (3) sum_t omega(t) r(t) <= sum_i omega_(i) (m-1-i)                            [rearrangement]
 (4) CR_DEP slack = (d+1)M' + m Dep - sum_i omega_(i)(m-1-i)  and the pair form sum_k C(n_k,2) + m Dep - (d-1)C(m,2).
Usage: python crdep_chain.py NS SEED MMAX"""
import sys, random
sys.path.insert(0, '.')
from tile import build
from crdep import crdep
NS, SEED, MMAX = map(int, sys.argv[1:4]); rnd = random.Random(SEED); cnt = 0
while cnt < NS:
    m = rnd.randint(4, MMAX); c0 = rnd.randint(m + 1, 9 * m)
    G = sorted(rnd.sample(range(m + 1, c0 + m), min(rnd.randint(1, 9), c0 - 1)))
    R = build(m, G)
    if R is None: continue
    c, gens, M = R; d = len(gens); D = list(M); Ds = set(D)
    if d < 1: continue
    cnt += 1
    up = lambda x, b: tuple(x[t] + (t == b) for t in range(d))
    mx = {x for x in D if all(up(x, b) not in Ds for b in range(d))}
    g = sum(w // m for w in M.values()); W = (d + 1) * (c - g) - c; M2 = (d + 1) * m * (m - 1) // 2
    ch = M2; om = {}; bound = M2
    for b in range(d):
        for x in D:
            if up(x, b) not in Ds:
                L = x[b] + 1; w = M[x]; ch -= L * (w - c); om[x] = om.get(x, 0) + L
                r = (w - c) % m
                if x in mx: assert w - c <= r
                else: assert w - c <= r - m
                bound -= L * (r if x in mx else r - m)
    assert ch == m * W, (m, gens)
    assert m * W >= bound
    dep = sum(v for x, v in om.items() if x not in mx)
    assert sum(om.values()) == d * m
    lhs = sum(om[x] * ((M[x] - c) % m) for x in om)
    ws = sorted(om.values(), reverse=True); rea = sum(v * (m - 1 - i) for i, v in enumerate(ws))
    assert lhs <= rea
    sl, dep2 = crdep(D, d); assert dep2 == dep and sl == M2 + m * dep - rea
    nk = [sum(1 for v in om.values() if v >= k) for k in range(1, max(ws) + 1)]
    pair = sum(n * (n - 1) // 2 for n in nk) + m * dep - (d - 1) * m * (m - 1) // 2
    assert pair == sl, (pair, sl)
    assert bound >= sl
print("chain CH' >= DEP bound >= CR_DEP verified on %d random S (all steps asserted)" % cnt)
