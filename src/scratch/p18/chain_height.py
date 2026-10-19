"""CHAIN failures vs Apery height (lead). minlen(w) = least factorization length of w in Ap (DP over Ap);
height2 = (max minlen <= 2), the Flat-MaxCL class.  Tests: (1) every interval CHAIN failure for m <= 40;
(2) perturbations of failing intervals by one extra generator at level 1 or 3; (3) an Apery set given on the command line.
usage: python chain_height.py scan | python chain_height.py apery m w0,w1,..."""
import sys, heapq, random
from chain_interval import chain_stats, apery
def minlen_profile(m, gens):
    w = apery(m, [m] + gens); ap = set(w)
    order = sorted(w); L = {0: 0}
    for x in order[1:]:
        L[x] = 1 + min(L[x - g] for g in gens if x - g in ap and x - g in L)
    return max(L.values()), sum(1 for x in w if L[x] >= 3)
if __name__ == '__main__' and sys.argv[1] == 'apery':
    m = int(sys.argv[2]); w = [int(x) for x in sys.argv[3].strip(',').split(',')]
    ap = set(w); gens = sorted(x for x in w if x > 0 and not any(w[j] + w[(x - w[j]) % m] == x for j in range(1, m) if (x - w[j]) % m))
    print(chain_stats(m, gens)['ratio'], minlen_profile(m, gens)); sys.exit()
def scan():
    nf = 0; nf3 = 0
    for m in range(10, 41):
        for k in (2, 3):
            for a in range(1, m):
                for b in range(a + 1, m):
                    g = list(range(k*m + a, k*m + b + 1)); r = chain_stats(m, g)
                    if not r or r['q'] < 4 or r['ratio'] >= 1: continue
                    nf += 1; h, n3 = minlen_profile(m, r['gens'])
                    if h >= 3: nf3 += 1; print('interval failure with height >= 3:', m, k, a, b, round(r['ratio'], 4), h, n3)
    print('interval CHAIN failures m<=40:', nf, ' of which height>=3:', nf3, flush=True)
    pert = []
    for m, a, b in ((30, 11, 21), (36, 10, 23), (44, 16, 31), (60, 21, 41), (80, 28, 55)):
        base = list(range(2*m + a, 2*m + b + 1))
        for extra in list(range(m + 1, 2*m)) + list(range(3*m + 1, 4*m, 3)):
            r = chain_stats(m, base + [extra])
            if not r or r['q'] < 4: continue
            h, n3 = minlen_profile(m, r['gens'])
            pert.append((round(r['ratio'], 4), m, extra, r['e'], r['q'], h, n3, 3*r['e'] < m))
    pert.sort()
    print('perturbed intervals: total', len(pert), ' failures', sum(1 for p in pert if p[0] < 1), ' failures with height>=3:', sum(1 for p in pert if p[0] < 1 and p[5] >= 3))
    for p in [p for p in pert if p[5] >= 3][:12]: print('  height>=3:', p)
if __name__ == '__main__' and sys.argv[1] == 'scan':
    scan()
