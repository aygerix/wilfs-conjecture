# Markov basis (minimal binomial generators of the lattice ideal) of L_r = {x : x.r = 0 mod m}, sorted by degree.
import sys; sys.path.insert(0, '/home/jmercedes/wilf/atop/fwx')
from gfan_hcr import markov
for spec in sys.argv[1:]:
    m, *r = map(int, spec.split(','))
    B = markov(m, r); B = [u if sum(u) >= 0 else [-x for x in u] for u in B]
    B.sort(key=lambda u: (max(sum(max(a, 0) for a in u), sum(max(-a, 0) for a in u)), u))
    show = lambda u: ' '.join(f"{'+' if a > 0 else ''}{a}e{i+1}" for i, a in enumerate(u) if a)
    print(f"m={m} r={tuple(r)}: {len(B)} Markov binomials;", ' | '.join(show(u) for u in B))
