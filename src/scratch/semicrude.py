# Semi-crude TOP: m*(1 + sum_{y max}(|y|-1)) <= (d+1) * sum_{z non-max} pi(z)   for all s (tiles)
# equivalently  min_s sum_{non-max} pi_s(z)  >= m(1+H)/(d+1),  H = sum_{max}(|y|-1).
import sys, itertools
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from exp_cl_tiling import downsets
def semi(D, p, m, d):
    S = set(D)
    A = [y for y in D if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))]
    N = [z for z in D if z not in A]
    H = sum(sum(y) - 1 for y in A)
    res = [sum(i*j for i, j in zip(z, p)) % m for z in N]
    mn = min(sum(m - (s - r) % m for r in res) for s in range(m))
    return (d+1)*mn - m*(1 + H)
if __name__ == '__main__':
    for d, mmax in [(2, 12), (3, 10), (4, 8), (5, 7)]:
        for m in range(3, mmax + 1):
            n = f = 0; worst = None
            for D in downsets(m, d):
                if any(all(x[a] == 0 for x in D) for a in range(d)): continue
                for p in itertools.product(range(1, m), repeat=d):
                    if len({sum(i*j for i, j in zip(y, p)) % m for y in D}) != m: continue
                    n += 1; v = semi(D, p, m, d)
                    if v < 0:
                        f += 1
                        if worst is None or v < worst[0]: worst = (v, sorted(D), p)
            print('d', d, 'm', m, 'tiles', n, 'semi-crude fails', f, worst, flush=True)
