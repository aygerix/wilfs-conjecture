"""Sanity check of the truncated condensed-Macaulay inequality (lead, 2026-10-20):
   q*|(qA \ (q-1)A) n [0,L)| <= |A n (0,L)| * |(q-1)A n [0,L)|   for integer A with 0 in A, every L, q = 2..5.
   (Eliahou JEMS 2018 Thm 5.11 applied to k[C]/(x0, I_{>=L}).)  Random A, exhaustive L."""
import random, sys
random.seed(int(sys.argv[1])); N = int(sys.argv[2]); worst = None; cnt = 0
for _ in range(N):
    n = random.randint(2, 7); top = random.randint(n + 1, 60)
    A = sorted(set([0] + random.sample(range(1, top), n)))
    S = [set([0])]
    for q in range(1, 6): S.append(set(x + a for x in S[-1] for a in A))
    for L in range(1, 5 * top + 2):
        g1 = sum(1 for a in A if 0 < a < L)
        for q in range(2, 6):
            new = sum(1 for s in S[q] if s < L and s not in S[q - 1]); prev = sum(1 for s in S[q - 1] if s < L)
            sl = g1 * prev - q * new; cnt += 1
            if worst is None or sl < worst[0]: worst = (sl, A, L, q)
            if sl < 0: print("VIOLATION", A, L, q, new, prev, g1); sys.exit()
print("checked", cnt, "instances; min slack", worst)
