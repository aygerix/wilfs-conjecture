import sys, itertools; sys.path.insert(0, sys.argv[0].rsplit('/', 1)[0])
from atop_shape import atop_shape
def twoface(d, n, k):
    # {x : |x| <= n, min(x_{d-2}, x_{d-1}) < k}; k = 1 is two-face; k >= 2 adds back e_a + e_b, ... (near-two-face)
    return [x for x in itertools.product(range(n + 1), repeat=d) if sum(x) <= n and min(x[d - 2], x[d - 1]) < k]
for d, n in ((3, 5), (3, 6), (4, 3), (4, 4)):
    for k in range(1, n // 2 + 2):
        T = twoface(d, n, k)
        if len(T) > 75: continue
        lhs, rhs, m, _, nx = atop_shape(T)
        print(f'd={d} n={n} min(x_a,x_b)<{k}: m={m} |A|={nx} slack {(rhs-lhs)/rhs:+.4f}', 'FAIL' if lhs > rhs + 1e-6 else '')
