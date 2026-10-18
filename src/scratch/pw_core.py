# Minimal infeasible core of the PW relaxation: greedily drop corner vectors (and q*) while PW stays infeasible.
# usage: pw_core.py h F G q
import sys
sys.path.insert(0, 'src/scratch')
from is_tile import build
from lattice_pairwise import corners
def mk(h, F, G, q):
    D = build(h, F, G, q); L1, L2, L3 = len(h), len(G), G[0]
    items = []
    for (i, hi) in corners(h): items.append(('A3', (i, hi), L3, lambda t, i=i, hi=hi: (i, hi, -t)))
    for (i, Fi) in corners(F): items.append(('A2', (i, Fi), L2, lambda s, i=i, Fi=Fi: (i, -s, Fi)))
    for (j, Gj) in corners(G): items.append(('A1', (j, Gj), L1, lambda u, j=j, Gj=Gj: (-u, j, Gj)))
    items.append(('q', tuple(q), 1, lambda _, q=tuple(q): q))
    return D, items
def feas(D, items, sums=True):
    def bad(v):
        if v == (0, 0, 0): return True
        p = tuple(max(c, 0) for c in v); n = tuple(max(-c, 0) for c in v)
        return p in D and n in D
    vals = [None] * len(items)
    def ok(k):
        v = items[k][3](vals[k])
        if bad(v): return False
        for l in range(k):
            w = items[l][3](vals[l])
            if bad(tuple(a - b for a, b in zip(v, w))) or (sums and bad(tuple(a + b for a, b in zip(v, w)))): return False
        return True
    def rec(k):
        if k == len(items): return True
        for x in range(items[k][2]):
            vals[k] = x
            if ok(k) and rec(k + 1): return True
        return False
    return rec(0)
if __name__ == '__main__':
    h, F, G, q = [eval(a) for a in sys.argv[1:5]]
    D, items = mk(h, F, G, q)
    print('m', len(D), 'items', [(it[0], it[1]) for it in items], 'feasible', feas(D, items))
    core = list(items)
    for it in list(items):
        trial = [x for x in core if x is not it]
        if not feas(D, trial): core = trial
    print('core', [(it[0], it[1], it[2]) for it in core])
    # which difference/sum kinds are needed: test with sums disabled
    print('core feasible without sums:', feas(D, core, sums=False))
