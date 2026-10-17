"""Experiment E3: covering strengthening of Wilf.
COV(S): the gap set H is covered by e-1 'reflected copies' f - L (f in PF(S)).
COV => g <= (e-1)*ell <=> Wilf.  (FGH: H = U_{f in PF} (f - L), so COV holds when t <= e-1.)
Compute kappa(S) = minimum number of f in PF with H subset U (f - L) and compare with e-1.
Also test the specific choice: the e-1 largest pseudo-Frobenius numbers."""
import sys
from itertools import combinations
sys.path.insert(0, 'src')
from ns import all_by_genus, NS

def cover_data(s):
    H = set(s.gaps)
    L = s.L
    PF = s.PF()
    sets = {f: frozenset(f - x for x in L if x <= f) for f in PF}
    for f in PF:
        assert sets[f] <= H
    full = frozenset(H)
    assert frozenset().union(*sets.values()) == full
    kappa = None
    for k in range(1, len(PF) + 1):
        for comb in combinations(PF, k):
            if frozenset().union(*(sets[f] for f in comb)) == full:
                kappa = k
                break
        if kappa:
            break
    top = sorted(PF)[-(s.e - 1):] if s.e > 1 else []
    top_ok = frozenset().union(*(sets[f] for f in top)) == full if top else (not H)
    return kappa, len(PF), top_ok

if __name__ == '__main__':
    G = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    nfail = ntopfail = ntot = nt_gt = 0
    worst = []
    for g, s in all_by_genus(G):
        if s.m == 1:
            continue
        ntot += 1
        if s.t() <= s.e - 1:
            continue
        nt_gt += 1
        kappa, t, top_ok = cover_data(s)
        if not top_ok:
            ntopfail += 1
        if kappa > s.e - 1:
            nfail += 1
            if len(worst) < 15:
                worst.append((s.P, s.e, t, kappa, s.c, s.g, s.ell, s.W))
    print(f'genus<={G}: total {ntot}, with t>e-1: {nt_gt}, COV fails: {nfail}, top-(e-1) choice fails: {ntopfail}')
    for w in worst:
        print('  fail P=%s e=%d t=%d kappa=%d c=%d g=%d ell=%d W=%d' % w)
