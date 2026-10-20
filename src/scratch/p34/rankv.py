"""RANK version of CH' (lead, 2026-10-21). For the lex tile Mhat (or any down-set tile) with the linear order by phi,
rank(z) = #{z' in Mhat : phi(z') > phi(z)},  w(z) = sum_{i : z+e_i not in Mhat} (z_i + 1).
RANK:  sum_z w(z) rank(z) >= (N-1) m (m-1)/2.   (delta(z) >= rank(z), so RANK => CH' => Wilf.)
Usage: python rankv.py rnd NS SEED MMAX DMIN | python rankv.py ann NR IT SEED MMAX MMIN"""
import sys, random, math
sys.path.insert(0, '.')
from tile import build
def rk(m, G, DMIN=0):
    if m < 3 or any(g <= m for g in G): return None
    R = build(m, G)
    if R is None: return None
    c, gens, M = R; N = len(gens)
    if N < 2 or c <= DMIN * m: return None
    up = lambda a, i: tuple(a[t] + (t == i) for t in range(N))
    order = sorted(M.items(), key=lambda t: -t[1])
    s = 0
    for rank, (a, x) in enumerate(order):
        s += rank * sum(a[i] + 1 for i in range(N) if up(a, i) not in M)
    need = (N - 1) * m * (m - 1) // 2
    return s - need, c, gens
if __name__ == '__main__':
    if sys.argv[1] == 'rnd':
        NS, SEED, MMAX, DMIN = map(int, sys.argv[2:6]); rnd = random.Random(SEED); nb = fail = 0; mn = None
        for _ in range(NS):
            m = rnd.randint(4, MMAX); G = [rnd.randint(m + 1, rnd.choice([2, 3, 5, 8]) * m + 1) for _ in range(rnd.randint(2, 7))]
            v = rk(m, G, DMIN)
            if v is None: continue
            nb += 1
            if v[0] < 0:
                fail += 1
                if fail <= 6: print("RANK FAIL m=%d c=%d gens=%s slack=%d" % (m, v[1], v[2], v[0]), flush=True)
            if mn is None or v[0] / m < mn[0]: mn = (v[0] / m, m) + v
        print("tested", nb, "RANK failures", fail, "min slack/m", mn)
