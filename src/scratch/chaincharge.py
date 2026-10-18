# (1) Is the worst rotation for MaxCL always sigma = phi(0) (r = plain residue)?  (2) Chain charging at sigma=0:
#  load(z) = sum_{y max, y > z} 2 prod_a C(y_a,z_a)/C(|y|,|z|);  check  sum_z load(z) r(z) <= (d+1) sum_N r(z).
import sys, itertools
from math import comb, prod
from fractions import Fraction as Fr
sys.path.insert(0, 'src')
from exp_cl_tiling import downsets
for d, mmax in [(2, 12), (3, 10), (4, 8), (5, 7)]:
    for m in range(3, mmax + 1):
        n = notzero = cfail = 0; worstc = None
        for D in downsets(m, d):
            if any(all(x[a] == 0 for x in D) for a in range(d)): continue
            S = set(D)
            A = [y for y in D if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))]
            Nn = [z for z in D if z not in A]
            load = {}
            for z in Nn:
                if sum(z) == 0: load[z] = Fr(0); continue
                L = Fr(0)
                for y in A:
                    if sum(y) >= 2 and all(zi <= yi for zi, yi in zip(z, y)) and z != y:
                        L += Fr(2*prod(comb(yi, zi) for yi, zi in zip(y, z)), comb(sum(y), sum(z)))
                load[z] = L
            for p in itertools.product(range(1, m), repeat=d):
                res = {y: sum(i*j for i, j in zip(y, p)) % m for y in D}
                if len(set(res.values())) != m: continue
                n += 1
                def G(sg):
                    return sum((sum(y)-1)*((res[y]-sg) % m) for y in A) - (d+1)*sum((res[z]-sg) % m for z in Nn)
                vals = [G(sg) for sg in range(m)]
                if max(vals) > vals[0]: notzero += 1
                c = (d+1)*sum(res[z] for z in Nn) - sum(load[z]*res[z] for z in Nn)
                if c < 0:
                    cfail += 1
                    if worstc is None or c < worstc[0]: worstc = (c, sorted(D), p)
        print('d', d, 'm', m, 'tiles', n, 'worst sigma != phi(0) in', notzero, '; chain-charging fails at sigma=0:', cfail, worstc, flush=True)
