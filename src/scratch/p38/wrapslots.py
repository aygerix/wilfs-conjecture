# wrapslots: for each large standard square x (u = sigma - m), its children l: position p = u + a_l (mod m), status:
#  'Z' (p<m, p in Z: missing), 'M1' (p<m, std if rep), 'w' (wrap: p-m in I: missing), 'W2' (wrap, p-m in M2': std if rep)
# Global: slots by type, standard counts; checks  sum_x [#wrap slots] - 3t  and the M1-part.
import sys
from itertools import combinations_with_replacement as cwr
def run(m, A, verbose):
    d = len(A); e = d + 1
    best = {}
    for k in range(4):
        for c in cwr(range(d), k):
            s = sum(A[i] for i in c); cl = s % m; key = (k * m + s, -k)
            if cl not in best or key < best[cl][0]: best[cl] = (key, c)
    sg = {cl: best[cl][0][0] + best[cl][0][1] * m for cl in best}; rep = {cl: best[cl][1] for cl in best}
    D = set(rep.values()); val = lambda c: sum(A[i] for i in c)
    eta = {c: sg[c] // m for c in range(m)}
    tot = {'Z': 0, 'M1s': 0, 'M1m': 0, 'w': 0, 'W2s': 0, 'W2m': 0}
    for x in D:
        if len(x) != 2 or val(x) < m: continue
        u = val(x) - m; row = []
        for l in range(d):
            p = u + A[l]; y = tuple(sorted(x + (l,))); std = y in D; wt = x.count(l) + 1
            if p < m: k = 'Z' if eta[p] == 0 else ('M1s' if std else 'M1m')
            else: k = 'w' if eta[p - m] <= 1 else ('W2s' if std else 'W2m')
            tot[k] += wt; row.append(k)
        if verbose: print(f"   sq {tuple(A[i] for i in x)} u={u}: " + ' '.join(f"{A[l]}:{row[l]}" for l in range(d)))
    t = sum(1 for c in eta if eta[c] == 2)
    D3 = 3 * (e - 1) * m - e * sum(len(rep[c]) for c in rep)
    return tot, t, D3
for arg in sys.argv[1:]:
    tt = list(map(int, arg.split(','))); tot, t, D3 = run(tt[0], tt[1:], True)
    print(f" m={tt[0]} A={tt[1:]}: slot totals {tot}; t={t}; 3t={3*t}; D3={D3}")
