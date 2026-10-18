# Test F0: at sigma = 0 (r(0) = 0), F = sum_A (|y|-1) K(y) - (d+1) sum_N K(z) >= 0, K(x) = floor(sum_a x_a r(e_a) / m).
# Together with beta_a <= 0 (observed on all small tiles) F0 implies MaxCL at sigma = 0, hence Wilf for m | c.
# Also test the general-sigma analogue F >= -rho_0.
import sys, itertools
sys.path.insert(0, 'src')
from exp_cl_tiling import downsets
def run(D, p, m, d):
    S = set(D); zero = tuple([0]*d)
    A = set(y for y in D if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d)))
    w = {x: (sum(x) - 1 if x in A else -(d+1)) for x in D}
    phi = {x: sum(i*j for i, j in zip(x, p)) % m for x in D}
    res = []
    for sg in range(m):
        r = {x: (phi[x] - sg) % m for x in D}
        rho0 = r[zero]; rho = [r[tuple(int(i == a) for i in range(d))] for a in range(d)]
        F = sum(w[x]*((sum(x[a]*rho[a] for a in range(d)) - (sum(x) - 1)*rho0) // m) for x in D)
        res.append((F, rho0))
    return res
if __name__ == '__main__':
    for d, mmax in [(2, 12), (3, 10), (4, 8), (5, 7)]:
        n = f0 = fg = 0; ex0 = exg = None
        for m in range(3, mmax + 1):
            for D in downsets(m, d):
                if any(all(x[a] == 0 for x in D) for a in range(d)): continue
                for p in itertools.product(range(1, m), repeat=d):
                    if len({sum(i*j for i, j in zip(y, p)) % m for y in D}) != m: continue
                    n += 1; res = run(D, p, m, d)
                    if res[0][0] < 0:
                        f0 += 1
                        if ex0 is None or m < ex0[0]: ex0 = (m, sorted(D), p, res[0][0])
                    if any(F < -rho0 for F, rho0 in res):
                        fg += 1
                        if exg is None or m < exg[0]: exg = (m, sorted(D), p, [(s, F, r0) for s, (F, r0) in enumerate(res) if F < -r0][:2])
        print('d', d, 'tiles', n, 'F0 fails (sigma=0)', f0, ex0, '| F >= -rho0 fails', fg, exg, flush=True)
