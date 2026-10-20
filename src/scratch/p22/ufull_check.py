# Independent check: Lemma U-FULL (bijective order ideal, the lex-max factorization ideal of a full Apery set) can fail.
import itertools, sys
from reviewcheck import semigroup, Cp, nu
gens = [int(t) for t in sys.argv[1].split(',')]
m, mem, ap, mg, c, g = semigroup(gens)
P = [n for n in mg if n != m]; d = len(P); e = d + 1
best = None
for perm in itertools.permutations(P):
    F = {}
    for x in ap:
        f = []; cur = x
        for n in perm:
            k = nu(cur, n, mem); f.append(k); cur -= k * n
        assert cur == 0
        F[x] = tuple(f)
    D = set(F.values())
    assert len(D) == m
    assert all(tuple(f[:i] + (f[i] - 1,) + f[i+1:]) in D for f in D for i in range(d) if f[i] > 0), "not order ideal"
    r = [n % m for n in perm]
    assert len({sum(a * b for a, b in zip(f, r)) % m for f in D}) == m, "not bijective"
    for p in range(1, m + 1):
        tot = 0
        for f in D:
            R = sum(a * b for a, b in zip(f, r))
            tot += Cp(R, p, m) - sum(f[a] * (Cp(R, p, m) - Cp(R - r[a], p, m)) for a in range(d))
        dec = sum(1 for f in D if sum(f) >= 2)
        if best is None or tot - dec > best[0]: best = (tot - dec, p, perm)
    uf = all(len([1 for f in itertools.product(*[range(x // n + 1) for n in P]) if sum(a * n for a, n in zip(f, P)) == x]) == 1 for x in ap)
nuK = max(sum(Cp(x, p, m) - sum(nu(x, n, mem) * (Cp(x, p, m) - Cp(x - n, p, m)) for n in P) for x in ap) - (m - e) for p in range(1, m + 1))
print("S =", mg, "m", m, "e", e, "c", c, "g", g, "W", e * (c - g) - c)
print("max over generator orders and p of sum_D K(f) - #dec:", best, " (T1 true-nu max violation:", nuK, ") UF:", uf)
