# Is MaxCL valid on the whole cone of group-subadditive functions?  For tile (D,p) and sigma, put
# c(g) = (d+1) if the cell with phi = g + sigma is non-maximal, -(|y|-1) if maximal.  Minimize sum_g c(g) r(g) over
# r : Z/m -> R>=0, r(0) = 0, r(g) + r(h) >= r(g+h), sum r = 1.  min >= 0  <=>  MaxCL at sigma follows from subadditivity alone.
import sys, itertools
from math import gcd
from fractions import Fraction as Fr
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from exp_cl_tiling import downsets
from exactlp import maximize
cache = {}
def groupmin(cvec, m):
    units = [u for u in range(1, m) if gcd(u, m) == 1]
    key = min(tuple(cvec[(u*g) % m] for g in range(m)) for u in units)
    if key in cache: return cache[key]
    n = m - 1  # r_1..r_{m-1}
    rows = []; b = []
    pairs = [(g, h) for g in range(1, m) for h in range(g, m) if (g + h) % m != 0]
    nv = n + len(pairs)
    for k, (g, h) in enumerate(pairs):
        row = [0]*nv; row[g-1] += 1; row[h-1] += 1; row[(g+h) % m - 1] -= 1; row[n+k] = -1
        rows.append(row); b.append(0)
    rows.append([1]*n + [0]*len(pairs)); b.append(1)
    obj = [-cvec[g] for g in range(1, m)] + [0]*len(pairs)
    val, x = maximize(obj, rows, b)
    res = (-val, tuple(x[:n]))
    cache[key] = res
    return res
if __name__ == '__main__':
    d, mmax = int(sys.argv[1]), int(sys.argv[2])
    for m in range(3, mmax + 1):
        n = f = 0; worst = None
        for D in downsets(m, d):
            if any(all(x[a] == 0 for x in D) for a in range(d)): continue
            S = set(D)
            A = {y for y in D if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))}
            wt = {x: (-(sum(x) - 1) if x in A else d + 1) for x in D}
            for p in itertools.product(range(1, m), repeat=d):
                ph = {x: sum(i*j for i, j in zip(x, p)) % m for x in D}
                if len(set(ph.values())) != m: continue
                inv = {v: x for x, v in ph.items()}
                for sg in range(m):
                    cvec = [wt[inv[(g + sg) % m]] for g in range(m)]
                    n += 1
                    v, r = groupmin(cvec, m)
                    if v < 0:
                        f += 1
                        if worst is None or v < worst[0]: worst = (v, sorted(D), p, sg, r)
        print('d', d, 'm', m, '(tile,sigma)', n, 'distinct LPs', len(cache), 'group-cone fails', f, worst, flush=True)
