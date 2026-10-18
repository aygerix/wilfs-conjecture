# Near-tight MaxCL instances: normalized slack  (d+1)M' - max_sigma sum_A T r   divided by (d+1)M'.
import sys, itertools
sys.path.insert(0, 'src')
from exp_cl_tiling import downsets
res = []
for d, mmax in [(2, 12), (3, 10), (4, 8), (5, 7)]:
    for m in range(3, mmax + 1):
        for D in downsets(m, d):
            if any(all(x[a] == 0 for x in D) for a in range(d)): continue
            S = set(D)
            A = [y for y in D if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))]
            M = m*(m-1)//2
            best = None
            for p in itertools.product(range(1, m), repeat=d):
                ph = [sum(i*j for i, j in zip(y, p)) % m for y in D]
                if len(set(ph)) != m: continue
                tr = [(d + sum(y), sum(i*j for i, j in zip(y, p)) % m) for y in A]
                w = max(sum(t*((r - sg) % m) for t, r in tr) for sg in range(m))
                v = (d+1)*M - w
                if best is None or v < best[0]: best = (v, p)
            if best is None: continue
            res.append((best[0] / ((d+1)*M), best[0], d, m, sorted(A), best[1]))
res.sort()
for r in res[:25]: print(round(r[0], 4), r[1:])
