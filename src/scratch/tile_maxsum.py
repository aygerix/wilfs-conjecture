# HT <=> sum_{y in Max} (|y|+3) <= 2m + 1 + E,  E = sum_{y not max} w(y)(ht(y)-1),  w(y) = sum_{a: y+e_a notin D}(y_a+1).
# (From H = sum_y w(y) ht(y) and sum_y w(y) = 3m.)  Report per m over non-two-face tiles: max of M3 - (2m+1)
# (M3 = sum_Max (|y|+3)), its tile, #tiles with M3 > 2m+1, min E, and |Max| range.   usage: tile_maxsum.py m...
import sys
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from tile_enum import enumerate_tiles
add = lambda x, i: x[:i] + (x[i]+1,) + x[i+1:]
def parts(D):
    ht = {}
    for x in sorted(D, key=lambda x: -sum(x)):
        ht[x] = max([ht[add(x, i)] + 1 for i in range(3) if add(x, i) in D], default=0)
    M3 = sum(sum(y) + 3 for y in D if ht[y] == 0); nmax = sum(1 for y in D if ht[y] == 0)
    E = sum(sum(y[a] + 1 for a in range(3) if add(y, a) not in D) * (ht[y] - 1) for y in D if ht[y] > 0)
    return M3, E, nmax
if __name__ == '__main__':
    for m in map(int, sys.argv[1:]):
        worst = None; nbad = 0; minE = None; nm = [10**9, 0]; n = 0
        for r, D, poly in enumerate_tiles(m):
            if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
            n += 1; M3, E, k = parts(set(D)); ex = M3 - (2*m + 1)
            nbad += ex > 0; nm = [min(nm[0], k), max(nm[1], k)]
            if worst is None or ex > worst[0]: worst = (ex, r, E, k)
            if minE is None or E < minE[0]: minE = (E, r, ex)
        print(f'm={m}: non-two-face {n}; max M3-(2m+1) {worst}; #M3>2m+1: {nbad}; min E {minE}; |Max| in {nm}', flush=True)
