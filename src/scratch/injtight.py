# tightest cases of Inj-TOP (A): slack = m^2 + (d-1) sum_{z non-max} pi(z) - sum_{y max} (|y|+1) pi(y)
import sys, itertools
sys.path.insert(0, 'src')
from exp_cl_tiling import downsets
d = int(sys.argv[1]); m = int(sys.argv[2]); K = int(sys.argv[3])
rows = []
for k in range(1, m + 1):
    for D in downsets(k, d):
        if d > 1 and any(all(x[a] == 0 for x in D) for a in range(d)): continue
        S = set(D)
        A = [y for y in D if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))]
        N = [z for z in D if z not in A]
        for p in itertools.product(range(1, m), repeat=d):
            res = {y: sum(i*j for i, j in zip(y, p)) % m for y in D}
            if len(set(res.values())) != k: continue
            for s in range(m):
                pi = {y: m - (s - res[y]) % m for y in D}
                sl = m*m + (d-1)*sum(pi[z] for z in N) - sum((sum(y)+1)*pi[y] for y in A)
                rows.append((sl, k, sorted(D), p, s, sorted((y, pi[y]) for y in A), sorted((z, pi[z]) for z in N)))
rows.sort(key=lambda r: r[0])
for r in rows[:K]: print(r)
