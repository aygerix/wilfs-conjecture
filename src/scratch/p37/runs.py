# mu-run structure of T\U on the residual: runs = maximal chains t, t+mu, ... in T\U.  Per S: #runs, lengths, whether
# each run starts with an NE2 class, #orphans (NE3 whose predecessor t - mu in the run is NE3), min D3/#orphans.
import sys
from itertools import combinations_with_replacement as cwr
from fractions import Fraction as F
for fn in sys.argv[1:]:
    n = 0; startNE3 = 0; nruns = 0; lens = {}; worst = None; startnotU = 0; mixed = 0
    for f in fn.split('+'):
        for L in open(f):
            t = L.split()
            if t[0] != 'DUMP': continue
            m = int(t[1]); e = int(t[2]); D3 = int(t[3]); A = list(map(int, t[15:])); mu = A[0]; d = len(A); n += 1
            sig = {}; lev = {}
            for k in range(4):
                for c in cwr(A, k):
                    v = sum(c); s = v % m
                    if s not in sig or v < sig[s] or (v == sig[s] and k < lev[s]): sig[s] = v; lev[s] = k
            N = 4 * m; inT = [False] * (N + 1); inT[0] = True
            for x in range(1, N + 1): inT[x] = any(x >= g and inT[x - g] for g in A + [m])
            cU = max(sig.values()) - m + 1
            TU = sorted(x for x in range(cU) if inT[x] and x < sig[x % m])
            S = set(TU); runs = []
            for x in TU:
                if x - mu in S: continue
                r = [x]
                while r[-1] + mu in S: r.append(r[-1] + mu)
                runs.append(r)
            if sum(len(r) for r in runs) != len(TU): mixed += 1
            orph = 0
            for r in runs:
                nruns += 1; lens[len(r)] = lens.get(len(r), 0) + 1
                if lev[r[0] % m] == 3: startNE3 += 1
                if not (r[0] - mu >= 0 and r[0] - mu >= sig[(r[0] - mu) % m]): startnotU += 1
                for a, b in zip(r, r[1:]):
                    if lev[a % m] == 3 and lev[b % m] == 3: orph += 1
            if orph and (worst is None or F(D3, orph) < worst[0]): worst = (F(D3, orph), m, A, D3, orph, len(TU), len(runs))
    print(fn, 'n', n, 'runs', nruns, 'run lengths', dict(sorted(lens.items())), '| runs starting with NE3:', startNE3, '| runs whose t1 - mu not in U:', startnotU,
          '| min D3/#orphans', (float(worst[0]),) + worst[1:] if worst else None)
