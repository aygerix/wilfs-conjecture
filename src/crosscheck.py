"""Cross-check implementation A (ns.py) vs B (ns_kunz.py) on all semigroups of genus <= G,
plus known counts n_g (OEIS A007323) and hand-checked examples."""
import sys, time
sys.path.insert(0, 'src')
from ns import NS, all_by_genus
import ns_kunz

KNOWN = [1, 1, 2, 4, 7, 12, 23, 39, 67, 118, 204, 343, 592, 1001, 1693, 2857, 4806, 8045,
         13467, 22464, 37396]

def main(G):
    t0 = time.time()
    counts = [0] * (G + 1)
    minW = {}
    for g, s in all_by_genus(G):
        counts[g] += 1
        assert s.g == g, (s, g)
        A = s.summary()
        # Exercise gap-set construction on every independently checked semigroup.
        rebuilt = NS.from_gapset(s.gaps)
        assert 0 in rebuilt and rebuilt.summary() == A
        B = ns_kunz.invariants(s.P)
        for k in ('m', 'e', 'c', 'g', 'ell', 'W'):
            assert A[k] == B[k], (k, A, B)
        assert sorted(A['P']) == sorted(B['P'])
        # Kunz coords satisfy Kunz inequalities, Selmer
        x = s.kunz()
        assert ns_kunz.is_kunz(x) or s.m == 1
        assert sum(x) == s.g
        if A['W'] < 0:
            print('COUNTEREXAMPLE', A)
        minW[g] = min(minW.get(g, 10**9), A['W'])
    print('counts', counts)
    assert counts == KNOWN[: G + 1], 'count mismatch'
    print('min W by genus', minW)
    print(f'ok, {sum(counts)} semigroups, {time.time()-t0:.1f}s')

# hand examples
for gaps in ({0}, {-1}, {0, 1}, {1, 2.5}, {1.0}, {True}, {"1"}, [1, True]):
    try:
        NS.from_gapset(gaps)
    except ValueError:
        pass
    else:
        raise AssertionError(f"accepted invalid gaps: {gaps!r}")
try:
    NS.from_gapset({2})  # Contains 1 but omits 1+1.
except ValueError:
    pass
else:
    raise AssertionError("accepted a gap set violating additive closure")
try:
    NS(1, 1, bytes([0, 1])).check_closed()
except ValueError:
    pass
else:
    raise AssertionError("accepted membership without zero")
assert NS.from_gapset(iter([1, 2, 3, 5, 7, 11, 11])).gaps == [1, 2, 3, 5, 7, 11]
s = NS.from_generators([3, 5, 7]); assert (s.c, s.g, s.ell, s.e, s.m) == (5, 3, 2, 3, 3), s.summary()
s = NS.from_generators([4, 6, 9]); assert (s.gaps, s.c, s.g, s.ell, s.e) == ([1,2,3,5,7,11], 12, 6, 6, 3), s.summary()
s = NS.from_generators([3, 5]);    assert (s.c, s.g, s.ell, s.e, s.W) == (8, 4, 4, 2, 0)
s = NS.from_generators([1]);       assert (s.c, s.g, s.ell, s.e, s.W) == (0, 0, 0, 1, 0)
s = NS.from_generators([5, 11, 12, 13, 14]); assert (s.c, s.ell, s.e, s.W) == (10, 2, 5, 0), s.summary()
main(int(sys.argv[1]) if len(sys.argv) > 1 else 16)
