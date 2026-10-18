# Exact-cone LP relaxation of Wilf for a lattice tile D (residues r mod m):
#   min  Phi(n) = d*m*max_{x in D} x.n - (d+1)*sum_{x in D} x.n
#   s.t. (q - y(q)).n >= 0 for every minimal non-element q (y(q) = cell with q's residue), n_a >= m+1.
# Wilf holds for every S with this tile if LP >= (d-1)m(m-1)/2 (CH').  Ratio printed = LP / that.
import gzip, json, sys
import numpy as np
from fractions import Fraction
from scipy.optimize import linprog
sys.path.insert(0, '.')
from hcr4_low import analyse
def lp_ratio(D, r):
    D = [tuple(x) for x in D]; S = set(D); d = len(D[0]); m = len(D)
    res = {sum(a * b for a, b in zip(x, r)) % m: x for x in D}
    assert len(res) == m
    U = [tuple(int(i == a) for i in range(d)) for a in range(d)]
    add = lambda x, y: tuple(p + q for p, q in zip(x, y))
    sub = lambda x, y: tuple(p - q for p, q in zip(x, y))
    G = set()
    for x in D:
        for u in U:
            q = add(x, u)
            if q in S: continue
            if all((sub(q, v) in S) for v, c in zip(U, q) if c > 0 for _ in [0] if True):
                G.add(q)
    G = [q for q in G if all(sub(q, U[a]) in S for a in range(d) if q[a] > 0)]
    s = np.array([sum(x[a] for x in D) for a in range(d)], float)
    A = [x for x in D if all(add(x, u) not in S for u in U)]
    # variables: n (d), z ; minimize z - (d+1) s.n ; z >= d m x.n for x in A
    c = np.concatenate([-(d + 1) * s, [1.0]])
    Aub, bub = [], []
    for x in A:
        Aub.append(np.concatenate([d * m * np.array(x, float), [-1.0]])); bub.append(0.0)
    for q in G:
        y = res[sum(a * b for a, b in zip(q, r)) % m]
        Aub.append(np.concatenate([-(np.array(q, float) - np.array(y, float)), [0.0]])); bub.append(0.0)
    bounds = [(m + 1, None)] * d + [(None, None)]
    out = linprog(c, A_ub=np.array(Aub), b_ub=np.array(bub), bounds=bounds, method='highs')
    if out.status != 0: return None, out.status
    return out.fun / ((d - 1) * m * (m - 1) / 2), out.x[:d]
if __name__ == '__main__':
    lo, hi, thr, top = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4])
    for m in range(lo, hi + 1):
        rows = []
        with gzip.open(f'certificate_all_{m}.jsonl.gz', 'rt') as f:
            for line in f:
                rec = json.loads(line); r = rec['r']
                if len(set(r)) < 4 or 0 in r: continue
                for D in rec['tile_cells']:
                    S = set(map(tuple, D))
                    if any(tuple(int(i == a) for i in range(4)) not in S for a in range(4)): continue
                    z = analyse(D)
                    if z['hcr'] < thr: rows.append((z['hcr'], r, D))
        rows.sort(key=lambda w: w[0])
        for h, r, D in rows[:top]:
            lr, nx = lp_ratio(D, r)
            print(f"m {m} HCR {float(h):.4f} LP {lr if lr is None else round(lr, 4)} r{tuple(r)} n* {np.round(nx, 2) if lr is not None else nx}", flush=True)
