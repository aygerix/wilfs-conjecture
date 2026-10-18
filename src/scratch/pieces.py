# Contact-region (piece) bound for H.  For an a-top z, z + e_a lies in the neighbour tile D + lam (lam in Lambda) and
# z + e_a - lam in B_a.  Grouping a-tops by lam gives contact regions C_lam (constant column length lam_a); their
# translates P_lam partition B_a, and each P_lam is a translate of a 2-D down-set.  Hp = sum_a sum_lam lam_a S(P_lam)
# <= H, S(P) = sum_{v in P} ht_P(v).  2-D fact: S(P) >= |P|/3 unless |P| = 1.  usage: pieces.py m0 m1 K  |  pieces.py show g
import sys, itertools
from math import gcd
from functools import reduce
from collections import defaultdict
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from cl import factorizations_down_set
from heightH import H_of
add = lambda x, i: x[:i] + (x[i]+1,) + x[i+1:]
def tile(gens):
    s = NS.from_generators(gens); p, best = factorizations_down_set(s, 'grlex')
    return s, p, {v: k for k, v in best.items()}
def residue_rep(cells, p, m):
    return {(sum(pi*xi for pi, xi in zip(p, x)) % m): x for x in cells}
def pieces(gens):
    s, p, cells = tile(gens); D = set(cells); m = s.m; rep = residue_rep(D, p, m)
    out = []
    for a in range(3):
        groups = defaultdict(list)
        for z in D:
            za = add(z, a)
            if za in D: continue
            r = rep[sum(pi*xi for pi, xi in zip(p, za)) % m]       # cell of D congruent to z + e_a
            lam = tuple(za[i] - r[i] for i in range(3))
            assert r[a] == 0, (gens, z, a, r)
            groups[lam].append(z)
        for lam, zs in groups.items():
            P = set(zs)
            ht = {}
            for v in sorted(P, key=lambda v: -sum(v)):
                ht[v] = max([ht[add(v, i)] + 1 for i in range(3) if i != a and add(v, i) in P], default=0)
            out.append((a, lam, lam[a], len(P), sum(ht.values())))
            assert all(z[a] + 1 == lam[a] for z in zs)
    return s, D, out
def stats(gens):
    s, D, out = pieces(gens); m = s.m
    Hp = sum(la*S for a, lam, la, n, S in out)
    sig = sum(la for a, lam, la, n, S in out if n == 1)
    return m, H_of(D), Hp, sig, out
if sys.argv[1] == 'show':
    for g in sys.argv[2:]:
        m, H, Hp, sig, out = stats([int(t) for t in g.split(',')])
        print(g, 'm', m, 'H', H, 'Hp', Hp, 'sigma', sig, 'H-(m-1)', H - m + 1, 'Hp-(m-1)', Hp - m + 1)
        for a, lam, la, n, S in sorted(out): print('   a', a, 'lam', lam, 'len', la, '|P|', n, 'S', S)
else:
    m0, m1, K = map(int, sys.argv[1:4])
    for m in range(m0, m1 + 1):
        worst = None; n = 0; fails = 0
        for g3 in itertools.combinations(range(m + 1, K*m), 3):
            if reduce(gcd, (m,) + g3) != 1: continue
            s = NS.from_generators([m, *g3])
            if s.e != 4: continue
            p, best = factorizations_down_set(s, 'grlex'); D = set(best.values())
            if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
            mm, H, Hp, sig, out = stats([m, *g3]); n += 1
            sl = Hp - (m - 1); fails += sl < 0
            if worst is None or sl < worst[0]: worst = (sl, [m, *g3], H - m + 1, sig)
        print(f'm={m}: {n}; min Hp-(m-1) {worst}; fails {fails}', flush=True)
