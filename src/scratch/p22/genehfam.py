# GEN-EH slack e(l-1) - (q-1)m on structured families (lead, 2026-10-20): intervals <m..m+k>, digital <a^2, a^2+1, a^2+a, a^2+a+1>,
# arithmetic <m, m+s, ..., m+ks>, and P15's T1-H / 6.1 families. Reports min slack and min slack/m per family.
import heapq, math, sys
def apery(m, gens):
    dist = {0: 0}; h = [(0, 0)]
    while h:
        d0, i = heapq.heappop(h)
        if dist.get(i) != d0: continue
        for n in gens:
            j = (i + n) % m; nd = d0 + n
            if j not in dist or nd < dist[j]: dist[j] = nd; heapq.heappush(h, (nd, j))
    return [dist.get(i) for i in range(m)]
def stats(m, gens):
    w = apery(m, gens)
    if any(x is None for x in w): return None
    M = max(w); c = M - m + 1
    if c <= m: return None
    q = -(-c // m); ell = sum((M - x) // m for x in w)
    mg = [n for n in sorted(set(gens)) if w[n % m] == n and not any(w[i] + w[(n - i) % m] == n for i in range(1, m) if (n - i) % m)]
    e = len(mg) + 1
    return dict(m=m, e=e, c=c, q=q, ell=ell, slack=e * (ell - 1) - (q - 1) * m, W=e * ell - c)
fams = {}
def rec(name, r):
    if r is None: return
    b = fams.get(name)
    if b is None or r['slack'] < b['slack']: fams[name] = r
    key = name + '_ratio'; b = fams.get(key)
    if b is None or r['slack'] / r['m'] < b['slack'] / b['m']: fams[key] = r
for m in range(4, 160):
    for k in range(2, m):
        rec('interval', stats(m, list(range(m + 1, m + k + 1))))
    for s in range(2, m):
        for k in range(2, 8):
            g = [m + i * s for i in range(1, k + 1)]
            if math.gcd(m, s) == 1: rec('arith', stats(m, g))
for a in range(2, 30):
    m = a * a; rec('digital', stats(m, [a * a + 1, a * a + a, a * a + a + 1]))
neg = [(k, v) for k, v in fams.items() if v['slack'] < 0]
for k, v in sorted(fams.items()): print(k, v)
print("negative:", neg)
