# MaxCL at sigma = 0 (r = <phi>, r(0) = 0): list tiles with the smallest normalized slack, excluding N = {0}
# (simplex-type, where the slack is 0 trivially).  Exhaustive small tiles.
import sys, itertools
sys.path.insert(0, 'src')
from exp_cl_tiling import downsets
rows = []
for d, mmax in [(1, 14), (2, 12), (3, 10), (4, 8)]:
    for m in range(3, mmax + 1):
        for D in downsets(m, d):
            if any(all(x[a] == 0 for x in D) for a in range(d)): continue
            S = set(D)
            A = set(y for y in D if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d)))
            N = [z for z in D if z not in A]
            if len(N) == 1: continue
            for p in itertools.product(range(1, m), repeat=d):
                r = {x: sum(i*j for i, j in zip(x, p)) % m for x in D}
                if len(set(r.values())) != m: continue
                sl = (d+1)*sum(r[z] for z in N) - sum((sum(y)-1)*r[y] for y in A)
                rows.append((sl/((d+1)*m*(m-1)/2), d, m, sorted(D), p, sl))
rows.sort(key=lambda t: t[0])
seen = set()
for t in rows:
    key = (t[1], t[2], tuple(t[3]))
    if key in seen: continue
    seen.add(key); print(round(t[0], 4), 'd', t[1], 'm', t[2], 'D', t[3], 'p', t[4], 'slack', t[5])
    if len(seen) >= 25: break
