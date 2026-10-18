# Inj-TOP (A) extended ranges; prints min slack and failures for given d and m range.
import sys, itertools
sys.path.insert(0, 'src')
from exp_cl_tiling import downsets
d = int(sys.argv[1]); m0 = int(sys.argv[2]); m1 = int(sys.argv[3])
for m in range(m0, m1 + 1):
    n = fa = 0; best = None; bestT = None
    for k in range(1, m + 1):
        for D in downsets(k, d):
            if d > 1 and any(all(x[a] == 0 for x in D) for a in range(d)): continue
            S = set(D)
            A = [y for y in D if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))]
            N = [z for z in D if z not in A]
            wA = [sum(y)+1 for y in A]
            for p in itertools.product(range(1, m), repeat=d):
                res = [sum(i*j for i, j in zip(y, p)) % m for y in D]
                if len(set(res)) != k: continue
                rA = [sum(i*j for i, j in zip(y, p)) % m for y in A]
                rN = [sum(i*j for i, j in zip(z, p)) % m for z in N]
                for s in range(m):
                    sl = m*m + (d-1)*sum(m - (s - r) % m for r in rN) - sum(w*(m - (s - r) % m) for w, r in zip(wA, rA))
                    n += 1
                    if sl < 0:
                        fa += 1
                        if fa <= 3: print('FAIL', sorted(D), p, s, sl, flush=True)
                    if best is None or sl < best[0]: best = (sl, k, sorted(D), p, s)
                    if k == m and (bestT is None or sl < bestT[0]): bestT = (sl, sorted(D), p, s)
    print('d', d, 'm', m, 'cases', n, 'fails', fa, 'min', best, '| min over tiles', bestT, flush=True)
