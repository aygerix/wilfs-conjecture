# General-d cylinder lemma check on Apery factorization tiles (grlex):
#  (a) at most one minimal non-element q in G has full support, and it lies in the lattice (phi(q) = 0);
#  (b') for every nonempty tau: #{q in G : supp q ⊇ tau} <= |D ∩ {x_tau = 0}|, via the injective map q -> y(q),
#       y(q) the cell of D congruent to q, with supp y(q) ∩ supp q = ∅;
#  (c) D = Cyl(D) \ (q* + N^d), Cyl(D) = {x : x with x_c := 0 lies in D, for every c}.
import sys, random, itertools; sys.path.insert(0, 'src')
from ns import NS
from cl import factorizations_down_set
E, n, seed = map(int, sys.argv[1:4]); rnd = random.Random(seed); done = 0; stats = {'cone': 0, 'C': 0}
while done < n:
    m = rnd.randint(E + 2, 40); gens = [m] + rnd.sample(range(m + 1, 4 * m), E - 1)
    try: s = NS.from_generators(gens)
    except ValueError: continue
    if s.e != E: continue
    Pp, best = factorizations_down_set(s, 'grlex'); d = len(Pp); D = set(best.values()); lam = {x: w for w, x in best.items()}
    phi = lambda x: sum(a * p for a, p in zip(x, Pp)) % m; byphi = {phi(x): x for x in D}
    U = [tuple(int(i == a) for i in range(d)) for a in range(d)]; add = lambda x, y: tuple(p + q for p, q in zip(x, y))
    G = [q for q in {add(x, u) for x in D for u in U} - D if all(tuple(q[b] - (b == a) for b in range(d)) in D for a in range(d) if q[a])]
    full = [q for q in G if all(q)]
    assert len(full) <= 1 and all(phi(q) == 0 for q in full), (s.P, full)
    for q in G:
        y = byphi[phi(q)]; assert all(not (q[c] and y[c]) for c in range(d)), (s.P, q, y)
    for k in range(1, d + 1):
        for tau in itertools.combinations(range(d), k):
            Q = [q for q in G if all(q[t] for t in tau)]
            assert len({byphi[phi(q)] for q in Q}) == len(Q), (s.P, tau)
    L = [max(x[a] for x in D) + 1 for a in range(d)]
    cyl = {x for x in itertools.product(*[range(l) for l in L]) if all(tuple(0 if b == c else x[b] for b in range(d)) in D for c in range(d))}
    if full: cyl = {x for x in cyl if not all(x[c] >= full[0][c] for c in range(d))}
    assert cyl == D, (s.P,)
    stats['cone' if full else 'C'] += 1; done += 1
print(f'e={E}: {n} random tiles (m <= 40, gens < 4m, seed {seed}): (a), (b\'), (c) hold on all; cone class {stats["cone"]}, class C {stats["C"]}')
