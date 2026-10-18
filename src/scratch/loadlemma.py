# Load Lemma (combinatorial, residue-free): for each maximal y with |y|>=2 choose weights on unordered pairs {u, y-u}
# (0 < u < y) totalling |y|-1, such that every nonzero non-maximal cell z carries total load <= d+1
# (a pair {u,u} loads u twice).  Necessary count condition: sum_A 2(|y|-1) <= (d+1)(|N|-1).
import sys, itertools
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from exp_cl_tiling import downsets
from exactlp import feasible
def check(D, d):
    S = set(D)
    A = [y for y in D if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))]
    N = [z for z in D if z not in A and sum(z) > 0]
    A2 = [y for y in A if sum(y) >= 2]
    cnt = sum(2*(sum(y)-1) for y in A2) <= (d+1)*len(N)
    zi = {z: i for i, z in enumerate(N)}
    cols = []  # (y index, loads dict)
    for k, y in enumerate(A2):
        seen = set()
        for u in itertools.product(*[range(v+1) for v in y]):
            v = tuple(a - b for a, b in zip(y, u))
            if sum(u) == 0 or sum(v) == 0: continue
            key = min(u, v)
            if key in seen: continue
            seen.add(key)
            ld = {}
            ld[zi[u]] = ld.get(zi[u], 0) + 1; ld[zi[v]] = ld.get(zi[v], 0) + 1
            cols.append((k, ld))
    if not A2: return cnt, True
    nv = len(cols) + len(N)
    Am = []; b = []
    for k, y in enumerate(A2):
        Am.append([1 if c[0] == k else 0 for c in cols] + [0]*len(N)); b.append(sum(y) - 1)
    for i, z in enumerate(N):
        Am.append([c[1].get(i, 0) for c in cols] + [1 if j == i else 0 for j in range(len(N))]); b.append(d + 1)
    return cnt, feasible(Am, b) is not None
for d, mmax in [(2, 12), (3, 10), (4, 8), (5, 7)]:
    for m in range(3, mmax + 1):
        n = fc = fl = 0; ex = None
        for D in downsets(m, d):
            if any(all(x[a] == 0 for x in D) for a in range(d)): continue
            # tile?
            ok = False
            for p in itertools.product(range(1, m), repeat=d):
                if len({sum(i*j for i, j in zip(y, p)) % m for y in D}) == m: ok = True; break
            if not ok: continue
            n += 1
            c, l = check(D, d)
            fc += not c; fl += not l
            if not l and ex is None: ex = sorted(D)
        print('d', d, 'm', m, 'tile shapes', n, 'count-condition fails', fc, 'Load Lemma fails', fl, ex, flush=True)
