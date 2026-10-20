# T1-UF (lead, 2026-10-20): order ideal F in N^d (|F| = m) with bijective residue map rho(f) = sum f_a r_a mod m.
# Claim tested: for all p in [1, m]:  sum_a sum_{f in F} ((rho(top_a(f)) - p) mod m) <= m*(e*(m-3)/2 + p),  e = d+1.
# No realizability (Kunz) condition is imposed.  Enumerates all staircases (d=2) / plane-partition-like ideals (d=3).
import itertools, sys
from functools import lru_cache
def partitions(n, maxpart=None):
    if maxpart is None: maxpart = n
    if n == 0: yield (); return
    for k in range(min(n, maxpart), 0, -1):
        for rest in partitions(n - k, k): yield (k,) + rest
def ideals2(m):
    for lam in partitions(m):
        yield [(i, j) for i, row in enumerate(lam) for j in range(row)]
def plane_partitions(m):
    # order ideals in N^3 of size m: stacks of partitions (plane partitions), brute via rows of partitions decreasing
    def rec(n, prev):
        if n == 0: yield []; return
        for k in range(1, n + 1):
            for lam in partitions(k):
                if prev is not None and (len(lam) > len(prev) or any(lam[i] > prev[i] for i in range(len(lam)))): continue
                for rest in rec(n - k, lam): yield [lam] + rest
    for layers in rec(m, None):
        yield [(z, i, j) for z, lam in enumerate(layers) for i, row in enumerate(lam) for j in range(row)]
def check(F, r, m):
    d = len(r); Fs = set(F)
    rho = {f: sum(f[a] * r[a] for a in range(d)) % m for f in F}
    if len(set(rho.values())) != m: return None
    tops = []
    for a in range(d):
        for f in F:
            g = list(f)
            while True:
                g[a] += 1
                if tuple(g) not in Fs: g[a] -= 1; break
            tops.append(rho[tuple(g)])
    e = d + 1; worst = None
    for p in range(1, m + 1):
        lhs = sum((t - p) % m for t in tops)
        rhs2 = m * (e * (m - 3) + 2 * p)  # 2*rhs
        sl = rhs2 - 2 * lhs
        if worst is None or sl < worst[0]: worst = (sl, p)
    return worst
if __name__ == '__main__':
  d = int(sys.argv[1]); M = int(sys.argv[2])
  gen = ideals2 if d == 2 else plane_partitions
  for m in range(3, M + 1):
      tested = 0; fails = 0; minsl = None
      for F in gen(m):
          if d == 3 and any(max(f[a] for f in F) == 0 for a in range(3)): continue
          if d == 2 and any(max(f[a] for f in F) == 0 for a in range(2)): continue
          for r in itertools.product(range(1, m), repeat=d):
              w = check(F, r, m)
              if w is None: continue
              tested += 1
              if w[0] < 0:
                  fails += 1
                  if fails <= 3: print("FAIL m=%d F=%s r=%s slack2=%d p=%d" % (m, sorted(F), r, w[0], w[1]))
              if minsl is None or w[0] < minsl[0]: minsl = (w[0], w[1], sorted(F), r)
      print("d=%d m=%d: tested %d, fails %d, min 2*slack %s" % (d, m, tested, fails, minsl[:2] if minsl else None), flush=True)
