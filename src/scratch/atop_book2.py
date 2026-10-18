import sys, itertools; sys.path.insert(0, sys.argv[0].rsplit('/', 1)[0])
from atop_shape import atop_shape
def simplex_pages(d, n, pages):
    # pages: list of coordinate sets; T = union over pages of {x supported on page, |x| <= n}
    T = set()
    for P in pages:
        for x in itertools.product(range(n + 1), repeat=len(P)):
            if sum(x) <= n:
                z = [0] * d
                for c, v in zip(P, x): z[c] = v
                T.add(tuple(z))
    return sorted(T)
if __name__ == '__main__':
    tests = [('d4: two 3-D pages on a 2-D spine', 4, [(0, 1, 2), (0, 1, 3)]),
             ('d4: two 2-D pages + spike', 4, [(0, 1), (0, 2), (3,)]),
             ('d4: two 2-D pages on axis + 2-D page off-axis', 4, [(0, 1), (0, 2), (2, 3)]),
             ('d4: chain of pages (0,1),(1,2),(2,3)', 4, [(0, 1), (1, 2), (2, 3)]),
             ('d5: two 4-D pages on a 3-D spine', 5, [(0, 1, 2, 3), (0, 1, 2, 4)]),
             ('d5: two 3-D pages on a 2-D spine + spike', 5, [(0, 1, 2), (0, 1, 3), (4,)])]
    for name, d, pages in tests:
        for n in range(2, 9):
            T = simplex_pages(d, n, pages)
            if len(T) > 70: break
            lhs, rhs, m, _, nx = atop_shape(T)
            print(f'{name}, n={n}: m={m} |A|={nx} slack {(rhs-lhs)/rhs:+.4f}', 'FAIL' if lhs > rhs + 1e-6 else '')
