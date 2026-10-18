# Lift form of MaxCL (night 10): with rho_0 = r(0), rho_a = r(e_a), L(x) = sum x_a rho_a - (|x|-1) rho_0,
# K(x) = floor(L(x)/m), r(x) = L(x) - m K(x):
#   MaxCL slack(sigma) = (d+1) sum_N r - sum_A (|y|-1) r = m F - (sum_a beta_a rho_a - beta' rho_0),
#   beta_a = sum_A (|y|-1) y_a - (d+1) sum_N z_a,  beta' = sum_a beta_a + m + Dep,  F = sum_x w(x) K(x).
# Checks the identity, tests beta_a <= 0, and reports the height-3 tiles with least slack at sigma = 0 (and overall).
import sys, itertools
sys.path.insert(0, 'src')
from exp_cl_tiling import downsets
def analyse(D, p, m, d):
    S = set(D); zero = tuple([0]*d)
    A = [y for y in D if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))]
    Aset = set(A)
    w = {x: (sum(x) - 1 if x in Aset else -(d+1)) for x in D}
    beta = [sum(w[x]*x[a] for x in D) for a in range(d)]
    T = sum(d + sum(y) for y in A); Dep = d*m - T
    betap = sum(beta) + m + Dep
    assert betap == sum(w[x]*(sum(x) - 1) for x in D)
    phi = {x: sum(i*j for i, j in zip(x, p)) % m for x in D}
    out = []
    for sg in range(m):
        r = {x: (phi[x] - sg) % m for x in D}
        rho0 = r[zero]; rho = [r[tuple(int(i == a) for i in range(d))] for a in range(d)]
        F = 0
        for x in D:
            L = sum(x[a]*rho[a] for a in range(d)) - (sum(x) - 1)*rho0
            K = L // m; assert L - m*K == r[x]; F += w[x]*K
        slack = sum(w[x]*(-r[x]) for x in D)   # = (d+1) sum_N r - sum_A (|y|-1) r
        assert slack == m*F - (sum(b*q for b, q in zip(beta, rho)) - betap*rho0)
        out.append(slack)
    return beta, Dep, out
if __name__ == '__main__':
    for d, mmax in [(2, 12), (3, 10), (4, 8), (5, 7)]:
        bpos = 0; n = 0; best0 = None; best = None
        for m in range(3, mmax + 1):
            for D in downsets(m, d):
                if any(all(x[a] == 0 for x in D) for a in range(d)): continue
                h = max(sum(x) for x in D)
                for p in itertools.product(range(1, m), repeat=d):
                    if len({sum(i*j for i, j in zip(y, p)) % m for y in D}) != m: continue
                    n += 1
                    beta, Dep, sl = analyse(D, p, m, d)
                    if max(beta) > 0: bpos += 1
                    if h == 3:
                        k0 = (sl[0] / m**2, m, sorted(D), p)
                        if best0 is None or k0 < best0: best0 = k0
                        k = (min(sl) / m**2, m, sorted(D), p, sl.index(min(sl)))
                        if best is None or k < best: best = k
        print('d', d, 'tiles', n, 'tiles with some beta_a > 0:', bpos, flush=True)
        print('   height-3 least slack at sigma=0 (norm):', best0, flush=True)
        print('   height-3 least slack any sigma (norm):', best, flush=True)
