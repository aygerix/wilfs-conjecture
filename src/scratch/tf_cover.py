# Two-face e = 4: which semigroups are covered by (alpha) base part of the identity [Def2D dropped],
# (beta) the sharp tau-criterion m+1 >= 2 tau + P2, or (gamma) Eliahou c <= 3m.  Report the uncovered ones.
import sys, itertools, collections, random
from math import gcd
from functools import reduce
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from tf_ident import parts
from tau_residual import analyse
def cover(s):
    r = parts(s)
    if r is None: return None
    t = analyse(s)
    return dict(P=s.P, m=s.m, L3=r['L3'], alpha=r['base'] >= 0, beta=t['sharp'], gamma=s.c <= 3*s.m, tau=t['tau'], P2=t['P2'])
if __name__ == '__main__':
    unc = collections.defaultdict(list); n = collections.Counter()
    if sys.argv[1] == 'exh':
        for m in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
            for g3 in itertools.combinations(range(m + 1, int(sys.argv[4])*m), 3):
                if reduce(gcd, (m,) + g3) != 1: continue
                s = NS.from_generators([m, *g3])
                if s.e != 4: continue
                r = cover(s)
                if r is None: continue
                n[m] += 1
                if not (r['alpha'] or r['beta'] or r['gamma']): unc[m].append(r)
    else:
        rng = random.Random(int(sys.argv[2])); N = int(sys.argv[3]); lo, hi = int(sys.argv[4]), int(sys.argv[5]); cnt = 0
        while cnt < N:
            m = rng.randint(lo, hi); pa = rng.randint(m + 1, 3*m); pb = rng.randint(m + 1, 3*m); t = rng.randint(0, 2); n0 = rng.randint(0, 3)
            if t == 0: pb = n0*m - pa if n0*m - pa > m else pb
            q = pa + pb - n0*m
            if t == 0 or q <= 0 or q % max(t, 1): continue
            pc = q // t
            if pc <= m or len({pa, pb, pc}) < 3 or reduce(gcd, (m, pa, pb, pc)) != 1: continue
            s = NS.from_generators([m, pa, pb, pc])
            if s.e != 4: continue
            r = cover(s)
            if r is None: continue
            cnt += 1; n[m] += 1
            if not (r['alpha'] or r['beta'] or r['gamma']): unc[m].append(r)
    tot = sum(n.values()); totu = sum(len(v) for v in unc.values())
    print('two-face total', tot, 'uncovered', totu)
    for m in sorted(unc): print(' m', m, 'uncovered', len(unc[m]), 'of', n[m], [(r['P'], r['L3'], r['tau'], r['P2']) for r in unc[m][:4]])
