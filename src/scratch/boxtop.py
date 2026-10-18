# Variants of the clean form  m + sum_{y max} w(y) pi(y) <= (d+1) sum_{z non-max} pi(z), for tiles, all s:
#   w = |y| - 1 (Tile-TOP''),  w = |B_y| - 2 with B_y = [0,y] (Box-TOP),  w = (# lower covers of y) ... etc.
import sys, itertools
sys.path.insert(0, 'src')
from exp_cl_tiling import downsets
from math import prod
variants = {
  'TOP2': lambda y: sum(y) - 1,
  'Box':  lambda y: prod(v + 1 for v in y) - 2,
  'Box-1': lambda y: prod(v + 1 for v in y) - 1,
  '2|y|-2': lambda y: 2*sum(y) - 2,
}
for d, mmax in [(2, 12), (3, 10), (4, 8), (5, 7)]:
    for m in range(3, mmax + 1):
        fails = {k: 0 for k in variants}; mins = {k: None for k in variants}; n = 0
        for D in downsets(m, d):
            if any(all(x[a] == 0 for x in D) for a in range(d)): continue
            S = set(D)
            A = [y for y in D if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))]
            N = [z for z in D if z not in A]
            for p in itertools.product(range(1, m), repeat=d):
                res = {y: sum(i*j for i, j in zip(y, p)) % m for y in D}
                if len(set(res.values())) != m: continue
                n += 1
                for y0 in A:
                    s = res[y0]
                    pi = {y: m - (s - res[y]) % m for y in D}
                    R = (d+1)*sum(pi[z] for z in N)
                    for k, w in variants.items():
                        v = R - m - sum(w(y)*pi[y] for y in A)
                        if v < 0: fails[k] += 1
                        if mins[k] is None or v < mins[k]: mins[k] = v
        print('d', d, 'm', m, 'tiles', n, {k: (fails[k], mins[k]) for k in variants}, flush=True)
