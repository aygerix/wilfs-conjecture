r"""Mirror consequence of KAPPA-DEP (lead, 2026-10-20): kappa0(delta) + kappa0(-delta) = sum_{x != 0}(|supp x| - 1)
(exact), so KAPPA-DEP for both delta and -delta forces SUPP2: sum_x (|supp x| - 1)^+ <= 2 Dep (shape only).
Reports SUPP2 failures by tile height on random S, and the KAPPA-DEP status of (D, delta), (D, -delta).
Usage: python suppdep.py NS SEED MMIN MMAX"""
import sys, random
sys.path.insert(0, '.')
from tile import build
from kdep import kslack
NS, SEED, MMIN, MMAX = map(int, sys.argv[1:5]); rnd = random.Random(SEED)
st = {}; cnt = 0; ex = {}
while cnt < NS:
    m = rnd.randint(MMIN, MMAX); c0 = rnd.randint(m + 1, 9 * m)
    G = sorted(rnd.sample(range(m + 1, c0 + m), rnd.randint(2, min(12, c0 - 2))))
    R = build(m, G)
    if R is None: continue
    c, gens, M = R; N = len(gens)
    if N < 2: continue
    cnt += 1; D = list(M); dl = [g % m for g in gens]; nd = [(-g) % m for g in gens]
    h = max(sum(x) for x in D); ss = sum(max(0, sum(1 for t in x if t) - 1) for x in D)
    s1, dep = kslack(m, D, dl); s2, _ = kslack(m, D, nd)
    assert (dep - s1) + (dep - s2) == ss
    op = int(3 * (N + 1) < m and c > 4 * m); key = (min(h, 4), op)
    a = st.setdefault(key, [0, 0, 0]); a[0] += 1; a[1] += ss > 2 * dep; a[2] += s2 < 0
    if s2 < 0 and key not in ex: ex[key] = (m, gens, c, s2, dep, ss)
for k in sorted(st): print("height %s open %d: n %d  SUPP2 fails %d  KAPPA-DEP(-delta) fails %d  ex %s" % (k[0] if k[0] < 4 else '>=4', k[1], st[k][0], st[k][1], st[k][2], ex.get(k)))
