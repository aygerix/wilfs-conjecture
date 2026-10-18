# GLL1 (one-level group Load Lemma): for tile (D,p) and z0 in D (sigma = phi(z0)), psi(x) = phi(x) - sigma.
# For each maximal y != z0 with |y| >= 2: weights on unordered pairs {u,v} of NON-maximal cells != z0 with
# psi(u) + psi(v) = psi(y), total |y| - 1;  every non-maximal cell != z0 carries load <= d+1.
# GLL1 at z0 + subadditivity  =>  MaxCL at sigma = phi(z0) (for every subadditive r with r(z0)=0).
import sys, itertools
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from exp_cl_tiling import downsets
from exactlp import feasible
def gll1(D, d, p, m, z0, A, ph):
    N = [z for z in D if z not in A and z != z0]
    zi = {z: i for i, z in enumerate(N)}
    inv = {v: x for x, v in ph.items()}
    sg = ph[z0]
    ys = [y for y in A if sum(y) >= 2 and y != z0]
    if not ys: return True
    cols = []
    for k, y in enumerate(ys):
        tgt = (ph[y] - sg) % m   # psi(y)
        seen = set()
        for u in N:
            pu = (ph[u] - sg) % m
            v = inv[(tgt - pu + sg) % m]   # psi(v) = tgt - pu  => phi(v) = tgt - pu + sg
            if v not in zi: continue
            key = tuple(sorted([u, v]))
            if key in seen: continue
            seen.add(key)
            ld = {}; ld[zi[u]] = ld.get(zi[u], 0) + 1; ld[zi[v]] = ld.get(zi[v], 0) + 1
            cols.append((k, ld))
    if any(not any(c[0] == k for c in cols) for k in range(len(ys))): return False
    Am = []; b = []
    for k, y in enumerate(ys):
        Am.append([1 if c[0] == k else 0 for c in cols] + [0]*len(N)); b.append(sum(y) - 1)
    for i in range(len(N)):
        Am.append([c[1].get(i, 0) for c in cols] + [1 if j == i else 0 for j in range(len(N))]); b.append(d + 1)
    return feasible(Am, b) is not None
if __name__ == '__main__':
    d, mmax = int(sys.argv[1]), int(sys.argv[2])
    for m in range(3, mmax + 1):
        n = f = 0; ex = None
        for D in downsets(m, d):
            if any(all(x[a] == 0 for x in D) for a in range(d)): continue
            S = set(D)
            A = {y for y in D if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))}
            for p in itertools.product(range(1, m), repeat=d):
                ph = {x: sum(i*j for i, j in zip(x, p)) % m for x in D}
                if len(set(ph.values())) != m: continue
                for z0 in D:
                    n += 1
                    if not gll1(D, d, p, m, z0, A, ph):
                        f += 1
                        if ex is None: ex = (sorted(D), p, z0, z0 in A)
        print('d', d, 'm', m, '(tile,z0)', n, 'GLL1 fails', f, ex, flush=True)
