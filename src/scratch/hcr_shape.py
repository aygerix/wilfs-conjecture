# Shape-only HCR value for a down-set D (any d):
#   [(m+1) * sum_{(x,a): top_a(x) not maximal} ht(top_a(x)) + sum_i T_(i) i] / ((d-1) m (m-1)/2);  >= 1 certifies Wilf
# for any semigroup whose factorization tile is D (CH' identity).
import sys; sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
def hcr_shape(D):
    D = set(D); d = len(next(iter(D))); m = len(D)
    U = [tuple(int(i == a) for i in range(d)) for a in range(d)]; add = lambda x, y: tuple(p + q for p, q in zip(x, y))
    ht = {}
    for x in sorted(D, key=lambda x: -sum(x)):
        ht[x] = max([ht[add(x, u)] + 1 for u in U if add(x, u) in D], default=0)
    Hn = 0
    for x in D:
        for a in range(d):
            t = x
            while add(t, U[a]) in D: t = add(t, U[a])
            Hn += ht[t]
    T = sorted((d + sum(y) for y in D if ht[y] == 0), reverse=True)
    return ((m + 1) * Hn + sum(i * t for i, t in enumerate(T))) / ((d - 1) * m * (m - 1) / 2)
if __name__ == '__main__':
    from tile_enum import enumerate_tiles
    for m in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
        res = {False: [0, 0, None], True: [0, 0, None]}; seen = set()
        for r, D, poly in enumerate_tiles(m):
            k = frozenset(D)
            if k in seen: continue
            seen.add(k)
            two = any(tuple(int(i in (a, b)) for i in range(3)) not in k for a in range(3) for b in range(a + 1, 3))
            v = hcr_shape(k); R = res[two]; R[0] += 1; R[1] += v < 1 - 1e-12
            if R[2] is None or v < R[2][0]: R[2] = (round(v, 4), r)
        print(f'm={m}: non-two-face {res[False][0]}, HCR fails {res[False][1]}, worst {res[False][2]} | two-face {res[True][0]}, fails {res[True][1]}, worst {res[True][2]}', flush=True)
