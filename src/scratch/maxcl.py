# MaxCL: sum_{y maximal} T(y) r(y) <= (d+1) m(m-1)/2  for all rotations r = <phi - sigma> (tiles)
# (Tile-TOP'' is the same with + Dep on the right; Tile-CL (II) is the same summed over ALL y.)
import sys, itertools
sys.path.insert(0, 'src')
from exp_cl_tiling import downsets
def maxcl(D, p, m, d):
    S = set(D)
    A = [y for y in D if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))]
    res = [(d + sum(y), sum(i*j for i, j in zip(y, p)) % m) for y in A]
    M = m*(m-1)//2
    Dep = d*m - sum(t for t, _ in res)
    worst = max(sum(t*((r - sg) % m) for t, r in res) for sg in range(m))
    return (d+1)*M - worst, Dep
if __name__ == '__main__':
    for d, mmax in [(2, 13), (3, 10), (4, 8), (5, 7)]:
        for m in range(3, mmax + 1):
            n = f = 0; worst = None
            for D in downsets(m, d):
                if any(all(x[a] == 0 for x in D) for a in range(d)): continue
                for p in itertools.product(range(1, m), repeat=d):
                    if len({sum(i*j for i, j in zip(y, p)) % m for y in D}) != m: continue
                    n += 1; v, dep = maxcl(D, p, m, d)
                    if v < 0:
                        f += 1
                        if worst is None or v < worst[0]: worst = (v, dep, sorted(D), p)
            print('d', d, 'm', m, 'tiles', n, 'MaxCL fails', f, worst, flush=True)
