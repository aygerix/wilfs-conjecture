# Height-3 tiles (exhaustive small): with the uniform split scheme, slack = (H+d+1) rho0 - U - V - m(B - P).
# Report cases where m*B > (H+d+1) rho0 (wrap budget exceeded) and what pays: -U (units), -V (level 2), m*P (carries).
import sys, itertools
from fractions import Fraction as Fr
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from exp_cl_tiling import downsets
from h3diag import terms
if __name__ == '__main__':
    for d, mmax in [(2, 12), (3, 10), (4, 8)]:
        n = over = 0; worst = None; stats = []
        for m in range(4, mmax + 1):
            for D in downsets(m, d):
                if any(all(x[a] == 0 for x in D) for a in range(d)): continue
                if max(sum(x) for x in D) != 3: continue
                for p in itertools.product(range(1, m), repeat=d):
                    if len({sum(i*j for i, j in zip(y, p)) % m for y in D}) != m: continue
                    cells = {x: sum(i*j for i, j in zip(x, p)) for x in D}
                    for sg in range(m):
                        t = terms(cells, d, m, sg); n += 1
                        exc = m*t['B'] - (t['H'] + d + 1)*t['r0']
                        if exc > 0:
                            over += 1
                            key = (exc / m**2, m, sorted(D), p, sg, dict(U=float(t['U']), V=float(t['V']), mP=float(m*t['P']), B=float(t['B']), r0=t['r0'], H=t['H'], slack=float(t['slack'])))
                            if worst is None or key[0] > worst[0]: worst = key
        print('d', d, '(tile,sigma) pairs', n, 'wrap budget exceeded', over, flush=True)
        print('   worst excess', worst, flush=True)
