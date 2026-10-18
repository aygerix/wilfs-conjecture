# HT <=> #{h = 0} <= 1 + sum_x (h(x)-1)^+, and {h = 0} = Max u Tripods (n(x) = 3).  Sufficient: t + |Tri| - 1 <= N2 :=
# #{x : h(x) >= 2}.  Report per m (non-two-face tiles): min N2 - (t + |Tri| - 1), min N2/m, max t, max |Tri|.
import sys
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
add = lambda x, i: x[:i] + (x[i]+1,) + x[i+1:]
def hvals(D):
    ht = {}
    for x in sorted(D, key=lambda x: -sum(x)):
        ht[x] = max([ht[add(x, i)] + 1 for i in range(3) if add(x, i) in D], default=0)
    T = [{}, {}, {}]
    for a in range(3):
        for x in sorted(D, key=lambda x: -x[a]):
            y = add(x, a); T[a][x] = T[a][y] if y in D else ht[x]
    return {x: T[0][x] + T[1][x] + T[2][x] for x in D}
if __name__ == '__main__':
    from tile_enum import enumerate_tiles
    for m in map(int, sys.argv[1:]):
        w1 = w2 = None; mt = mtr = 0
        for r, D, poly in enumerate_tiles(m):
            if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
            hv = hvals(set(D)); n0 = sum(1 for v in hv.values() if v == 0); n2 = sum(1 for v in hv.values() if v >= 2)
            t = sum(1 for x in D if all(add(x, a) not in D for a in range(3))); tri = n0 - t
            mt = max(mt, t); mtr = max(mtr, tri)
            s = n2 - (n0 - 1)
            if w1 is None or s < w1[0]: w1 = (s, r, n2, t, tri)
            if w2 is None or n2 / m < w2[0]: w2 = (n2 / m, r)
        print(f'm={m}: min N2-(t+tri-1) {w1}; min N2/m {w2[0]:.2f} {w2[1]}; max t {mt}, max tri {mtr}', flush=True)
