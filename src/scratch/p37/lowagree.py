r"""Independent check of Lemma LOW-AGREE and its corollary (lead, 2026-10-21).  No code shared with trunc3/q5d.
U_k = kA' + mN built from the explicit integer sumset; T = <m, A> by a membership DP.
Checks: (i) U_k n [0,(k+1)mu) == T n [0,(k+1)mu); (ii) c(U_k) <= (k+1)mu  =>  U_k == T; (iii) Kaplan transfer:
c(U_k) <= 2mu  =>  (|A|+1) l(U_k) >= c(U_k).  usage: python lowagree.py seed n"""
import sys, random
from itertools import combinations_with_replacement as cwr
random.seed(int(sys.argv[1])); n = int(sys.argv[2])
stats = dict(tested=0, eq_forced=0, kaplan=0, agree_fail=0, eq_fail=0, kap_fail=0)
for it in range(n):
    m = random.randint(5, 70); d = random.randint(2, min(9, m - 1)); k = random.choice([2, 3, 3, 3, 4])
    A = sorted(random.sample(range(1, m), d)); mu = A[0]
    sums = {0}
    for j in range(1, k + 1):
        for comb in cwr(A, j): sums.add(sum(comb))
    if len({x % m for x in sums}) < m: continue
    N = max(sums) + 2 * m
    inU = [False] * (N + 1)
    for x in sums:
        for z in range(x, N + 1, m): inU[z] = True
    inT = [False] * (N + 1); inT[0] = True
    for z in range(1, N + 1): inT[z] = any(z >= g and inT[z - g] for g in A + [m])
    gU = [z for z in range(N + 1) if not inU[z]]; cU = gU[-1] + 1 if gU else 0
    stats['tested'] += 1
    B = (k + 1) * mu
    if any(inU[z] != inT[z] for z in range(min(B, N + 1))): stats['agree_fail'] += 1
    if cU <= B:
        stats['eq_forced'] += 1
        if any(inU[z] != inT[z] for z in range(N + 1)): stats['eq_fail'] += 1
    if 0 < cU <= 2 * mu:
        stats['kaplan'] += 1; lU = sum(1 for z in range(cU) if inU[z])
        if (d + 1) * lU < cU: stats['kap_fail'] += 1
print(stats)
