# Tile-TOP'':  sum_{y maximal in D} T(y) * (m - <s - phi(y)>)  <=  m((d+1)m + d - 1)/2   for all s.
# DR-CL: slack(s) + Dep(D) >= 0, Dep = sum_a sum_{a-columns C with non-maximal top} |C|.
# Exhaustive: all down-sets D (no degenerate directions), all bijective p, all s.  Plus spiky tiles.
import sys, itertools
sys.path.insert(0, 'src')
from exp_cl_tiling import downsets
def analyse(D, p, m):
    S = set(D); d = len(p)
    res = {y: sum(i*j for i, j in zip(y, p)) % m for y in D}
    T = {}; maxi = {}
    for y in D:
        t = 0; mx = True
        for a in range(d):
            z = list(y); z[a] += 1
            if tuple(z) not in S: t += y[a] + 1
            else: mx = False
        T[y] = t; maxi[y] = mx
    Dep = sum(T[y] for y in D if not maxi[y])
    M = m*(m-1)//2; rhs2 = m*((d+1)*m + d - 1)
    worst_top = None; worst_dr = None
    for s in range(m):
        lhs = sum(T[y]*(m - (s - res[y]) % m) for y in D if maxi[y])
        f = sum(T[y]*((s - res[y]) % m) for y in D)
        sl = (f - (d-1)*M)//m
        v = rhs2 - 2*lhs
        if worst_top is None or v < worst_top: worst_top = v
        if worst_dr is None or sl + Dep < worst_dr: worst_dr = sl + Dep
    return worst_top, worst_dr
if __name__ == '__main__':
    for d, mmax in [(2, 13), (3, 10), (4, 8), (5, 7)]:
        for m in range(3, mmax + 1):
            n = ft = fd = 0; wt = None
            for D in downsets(m, d):
                if any(all(x[a] == 0 for x in D) for a in range(d)): continue
                for p in itertools.product(range(1, m), repeat=d):
                    if len({sum(i*j for i, j in zip(y, p)) % m for y in D}) != m: continue
                    n += 1
                    t, r = analyse(D, p, m)
                    ft += t < 0; fd += r < 0
                    if wt is None or t < wt[0]: wt = (t, sorted(D), p)
            print('d', d, 'm', m, 'tiles', n, 'Tile-TOP2 fails', ft, 'DR-CL fails', fd, 'min 2*slack(TOP2)', wt[0] if wt else None, flush=True)
