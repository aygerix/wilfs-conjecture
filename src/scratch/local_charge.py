# Local charging test for HT in the form  sum_x (h(x) - 1) >= -1,  h(x) = sum_a ht(t_a(x)).
# Cells with h = 0 are N3 = A u Z3'.  Rule R1: maximal y with some a, y_a >= 1, y-e_a+e_b, y-e_a+e_c not in D gets the
# private cell y - e_a (h >= 2).  Report how many N3 cells are NOT covered by R1, per tile, and the residual
# surplus  sum_x (h(x)-1)^+ - (#uncovered) ... over complete enumeration (non-two-face).   usage: m...
import sys
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from tile_enum import enumerate_tiles
add = lambda x, i: x[:i] + (x[i]+1,) + x[i+1:]
sub = lambda x, i: x[:i] + (x[i]-1,) + x[i+1:]
def analyse(D):
    ht = {}
    for x in sorted(D, key=lambda x: -sum(x)):
        ht[x] = max([ht[add(x, i)] + 1 for i in range(3) if add(x, i) in D], default=0)
    def top(x, i):
        while add(x, i) in D: x = add(x, i)
        return x
    h = {x: sum(ht[top(x, a)] for a in range(3)) for x in D}
    A = [x for x in D if ht[x] == 0]
    N3 = [x for x in D if h[x] == 0]
    unc = []
    for y in A:
        ok = False
        for a in range(3):
            if y[a] == 0: continue
            x = sub(y, a)
            if all(add(x, b) not in D for b in range(3) if b != a): ok = True
        if not ok: unc.append(y)
    Z = [x for x in N3 if x not in A]
    return h, A, Z, unc
if __name__ == '__main__':
    for m in map(int, sys.argv[1:]):
        mx = None; dist = {}
        for r, D, poly in enumerate_tiles(m):
            if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
            h, A, Z, unc = analyse(set(D))
            k = len(unc) + len(Z)
            dist[k] = dist.get(k, 0) + 1
            if mx is None or k > mx[0]: mx = (k, r, len(A), len(Z), sorted(unc))
        print(f'm={m}: max uncovered(A)+|Z3| {mx}; distribution {sorted(dist.items())}', flush=True)
