# Exact split of the Wilf number into a geometric and an arithmetic part (any e).
#   n_a = r_a + m k_a (1 <= r_a <= m-1), lam(x) = m (x.k) + x.r on the grlex tile D, x* = lam-argmax.
#   W = Lev + Car,  Lev = d m (x*.k) - (d+1) sum_D x.k   (shape/level part; >= 0 when x* also maximizes x.k: CH)
#                   Car = d (x*.r) - (d+1) mean_D(x.r) - (d-1)(m-1)/2   (residue/carry part)
import sys, random; sys.path.insert(0, 'src')
from fractions import Fraction as Fr
from ns import NS
from cl import factorizations_down_set
rnd = random.Random(int(sys.argv[1])); N = int(sys.argv[2]); E0, E1, M0, M1, K = map(int, sys.argv[3:8])
st = {}
for _ in range(N):
    e = rnd.randint(E0, E1); m = rnd.randint(max(M0, e + 1), M1)
    try: s = NS.from_generators([m] + rnd.sample(range(m + 1, K * m), e - 1))
    except Exception: continue
    if s.e != e: continue
    P, best = factorizations_down_set(s, 'grlex'); D = list(best.values()); d = len(P)
    k = [p // m for p in P]; r = [p % m for p in P]
    if 0 in r: continue
    lam = {x: w for w, x in best.items()}; xs = max(D, key=lambda x: lam[x])
    dot = lambda x, v: sum(a * b for a, b in zip(x, v))
    Lev = d * m * dot(xs, k) - (d + 1) * sum(dot(x, k) for x in D)
    Car = d * dot(xs, r) - Fr(d + 1, m) * sum(dot(x, r) for x in D) - Fr((d - 1) * (m - 1), 2)
    assert Lev + Car == s.W, (P, Lev, Car, s.W)
    key = (e, s.c > 3 * m); t = st.setdefault(key, [0, 0, 0, None])
    t[0] += 1; t[1] += Car < 0; t[2] += Lev < 0
    if Car < 0:
        q = float(Lev / -Car) if Car else 0
        if t[3] is None or q < t[3][0]: t[3] = (round(q, 3), s.P, int(Lev), float(Car), s.W)
for key in sorted(st):
    t = st[key]; print(f"e={key[0]} c>3m={key[1]}: {t[0]} S, Car<0 {t[1]}, Lev<0 {t[2]}, min Lev/|Car| when Car<0: {t[3]}")
