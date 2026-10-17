"""Experiment E3b: COV'(S): H subset of a union of e-1 translates T_i - L, T_i arbitrary integers.
COV' => g <= (e-1)*ell <=> Wilf.  Compute kappa'(S) = min number of translates (exact, branch&bound)."""
import sys
sys.path.insert(0, 'src')
from ns import all_by_genus

def min_cover(H, L, limit):
    """min k <= limit such that H is covered by k translates T - L; None if > limit."""
    H = frozenset(H)
    if not H:
        return 0
    Ls = set(L)
    # candidate translates for each gap h: T = h + x, x in L
    cand = {h: [h + x for x in L] for h in H}
    cover_of = {}
    def cov(T):
        if T not in cover_of:
            cover_of[T] = frozenset(T - x for x in L if T - x in H)
        return cover_of[T]
    best = [None]
    def rec(unc, k):
        if not unc:
            return True
        if k == 0:
            return False
        # lower bound: max coverage
        h = min(unc, key=lambda h: len(cand[h]))
        # sort candidates by coverage of uncovered
        for T in sorted(cand[h], key=lambda T: -len(cov(T) & unc)):
            if rec(unc - cov(T), k - 1):
                return True
        return False
    for k in range(1, limit + 1):
        if rec(H, k):
            return k
    return None

if __name__ == '__main__':
    G = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    nt = nfail = 0
    ex = []
    for g, s in all_by_genus(G):
        if s.m == 1 or s.t() <= s.e - 1:
            continue
        nt += 1
        k = min_cover(s.gaps, s.L, s.e - 1)
        if k is None:
            nfail += 1
            if len(ex) < 12:
                ex.append((s.P, s.e, s.t(), s.c, s.g, s.ell, s.W))
    print(f'genus<={G}: t>e-1 cases {nt}; COV\' fails (needs > e-1 translates): {nfail}')
    for x in ex:
        print('  fail P=%s e=%d t=%d c=%d g=%d ell=%d W=%d' % x)
