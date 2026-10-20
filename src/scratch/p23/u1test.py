r"""Does U1 <= E2 + E3 need the depth-four hypotheses?  (lead, 2026-10-20)
U1 = |3A n [m, m+h)|, E3 = (e+2)|2A n [0,m+h)| - 3|3A n [0,m+h)|, E2 = a|3A n [0,h)| - 4|(4A \ 3A) n [0,h)|, a = |A n (0,h)|.
Random integer A (0 in A, A in [0,m)), all 1 <= h <= m.  Reports violations with/without the depth-4 covering conditions."""
import random, sys
random.seed(int(sys.argv[1])); N = int(sys.argv[2])
viol_free = 0; viol_d4 = 0; tot = 0; tot4 = 0; ex = None
for _ in range(N):
    m = random.randint(8, 60); k = random.randint(2, 7)
    A = sorted(set([0] + random.sample(range(1, m), min(k, m - 1)))); e = len(A)
    X2 = set(x + y for x in A for y in A); X3 = set(x + y for x in X2 for y in A); X4 = set(x + y for x in X3 for y in A)
    T3 = set(s for s in X3 if s < m) | set(s - m for s in X2 if m <= s < 2 * m)
    T4 = set(s for s in X4 if s < m) | set(s - m for s in X3 if m <= s < 2 * m)
    for h in range(1, m + 1):
        a = sum(1 for x in A if 0 < x < h)
        U1 = sum(1 for s in X3 if m <= s < m + h)
        E3 = (e + 2) * sum(1 for s in X2 if s < m + h) - 3 * sum(1 for s in X3 if s < m + h)
        E2 = a * sum(1 for s in X3 if s < h) - 4 * sum(1 for s in X4 if s < h and s not in X3)
        d4 = all(r in T3 for r in range(h, m)) and (h - 1) not in T3 and all(r in T4 for r in range(h))
        tot += 1; tot4 += d4
        if U1 > E2 + E3:
            viol_free += 1
            if d4: viol_d4 += 1; print("D4 VIOLATION", m, A, h, U1, E2, E3)
            elif ex is None: ex = (m, A, h, U1, E2, E3)
print("instances", tot, "depth4", tot4, "violations without depth hyp", viol_free, "with", viol_d4, "example", ex)
