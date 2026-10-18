# Inj-TOP: for down-sets D (|D| = k <= m, no degenerate directions) with phi injective, all s:
#  (A)  sum_{y in A}(|y|+1) pi(y) <= m^2 + (d-1) sum_{z in D\A} pi(z)
#  (B)  sum_{y in A}(d+|y|) pi(y) <= m((d+1)m + d - 1)/2
# pi(z) = m - <s - phi(z)>  in [1,m].  A = maximal cells.
import sys, itertools
sys.path.insert(0, 'src')
from exp_cl_tiling import downsets
for d, mmax in [(1, 12), (2, 11), (3, 8), (4, 7)]:
    for m in range(2, mmax + 1):
        n = fa = fb = 0; exA = exB = None
        for k in range(1, m + 1):
            for D in downsets(k, d):
                if d > 1 and any(all(x[a] == 0 for x in D) for a in range(d)): continue
                S = set(D)
                A = [y for y in D if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))]
                N = [z for z in D if z not in A]
                for p in itertools.product(range(1, m), repeat=d):
                    res = {y: sum(i*j for i, j in zip(y, p)) % m for y in D}
                    if len(set(res.values())) != k: continue
                    for s in range(m):
                        pi = {y: m - (s - res[y]) % m for y in D}
                        n += 1
                        la = sum((sum(y)+1)*pi[y] for y in A); ra = m*m + (d-1)*sum(pi[z] for z in N)
                        lb = 2*sum((d+sum(y))*pi[y] for y in A); rb = m*((d+1)*m + d - 1)
                        if la > ra:
                            fa += 1
                            if exA is None: exA = (sorted(D), p, s, la, ra)
                        if lb > rb:
                            fb += 1
                            if exB is None: exB = (sorted(D), p, s, lb, rb)
        print('d', d, 'm', m, 'cases', n, 'A fails', fa, exA, '| B fails', fb, exB, flush=True)
