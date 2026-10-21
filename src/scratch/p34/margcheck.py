r"""Check of the height-2 margin identity (lead, 2026-10-20): for a factorization tile D of height <= 2 in N^d,
Sigma_supp - Dep = C(d,2) - 3 k_mixed - 2 k_loop + (d+1) z, where k_mixed / k_loop count the missing cells e_a+e_b (a<b) /
2e_a and z the directions a with no height-2 cell through e_a.  Random S = <m, m+delta> (and lifts in (2m,3m)) whose
tile has height <= 2.  Usage: python margcheck.py N SEED"""
import sys, random
sys.path.insert(0, '.')
from tile import build
from tcldich import stats
N, SEED = map(int, sys.argv[1:3]); rnd = random.Random(SEED); done = 0; tries = 0
while done < N:
    tries += 1
    m = rnd.randrange(8, 60); d = rnd.randrange(2, min(10, m - 1))
    G = sorted(set(rnd.randrange(m + 1, 3 * m) for _ in range(d)))
    R = build(m, G)
    if R is None: continue
    c, gens, M = R; D = list(M); d = len(gens)
    if d < 2 or max(sum(x) for x in D) > 2: continue
    Ds = set(map(tuple, D)); E = lambda a, b: tuple((a == i) + (b == i) for i in range(d)) in Ds
    km = sum(1 for a in range(d) for b in range(a + 1, d) if not E(a, b)); kl = sum(1 for a in range(d) if not E(a, a))
    z = sum(1 for a in range(d) if not any(E(a, b) for b in range(d)))
    v, dep, ss = stats(m, D, [g % m for g in gens])
    assert ss - dep == d * (d - 1) // 2 - 3 * km - 2 * kl + (d + 1) * z, (m, gens, ss, dep, km, kl, z)
    done += 1
print("margin identity OK on %d height-<=2 tiles (%d draws), seed %d" % (done, tries, SEED))
