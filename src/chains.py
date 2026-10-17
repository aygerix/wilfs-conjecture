r"""Chain decomposition identity (derived 2026-10-17, see .research/PROOFS.md, Identity CH).

For a numerical semigroup S != N with multiplicity m, Apery set Ap = Ap(S,m), M = max Ap = F+m,
P' = P \ {m} = {p_1..p_d} (d = e-1).  For each a, the relation w -> w + p_a (both in Ap) splits Ap into
maximal arithmetic progressions ('p_a-chains').  nu_a(w) = max{k : w - k p_a in S}.

  Def_a = sum_{chains C} |C| (M - top(C))        >= 0
  E     = sum_{w in Ap} (sum_a p_a nu_a(w) - w)   >= 0
  m*W(S) = sum_a Def_a + E - (d-1) m (m-1)/2.            (Identity CH)
"""
import sys
sys.path.insert(0, 'src')
from ns import NS, all_by_genus


def chain_data(s):
    m = s.m
    ap = s.apery()
    apset = set(ap)
    M = max(ap)
    Pp = [p for p in s.P if p != m]
    d = len(Pp)
    Defs = []
    for p in Pp:
        Def = 0
        for w in ap:
            if (w + p) not in apset:          # w is a chain top
                # chain length = number of k>=0 with w - k p in Ap
                k = 0
                while (w - (k + 1) * p) in apset:
                    k += 1
                Def += (k + 1) * (M - w)
        Defs.append(Def)
    E = 0
    for w in ap:
        tot = 0
        for p in Pp:
            k = 0
            while (w - (k + 1) * p) >= 0 and (w - (k + 1) * p) in s:
                k += 1
            tot += p * k
        E += tot - w
    return dict(m=m, d=d, M=M, Defs=Defs, E=E, target=(d - 1) * m * (m - 1) // 2)


if __name__ == '__main__':
    G = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    n = 0
    for g, s in all_by_genus(G):
        if s.m == 1:
            continue
        cd = chain_data(s)
        assert s.m * s.W == sum(cd['Defs']) + cd['E'] - cd['target'], (s, cd, s.W)
        assert cd['E'] >= 0 and min(cd['Defs'], default=0) >= 0
        n += 1
    print(f'Identity CH verified on all {n} semigroups of genus <= {G} (S != N).')
