r"""Find and independently verify LASTWIN failures (lead, 2026-10-20).  Independent check: membership by direct
dynamic programming over [0, c + m) from the generators (no Apery code).  usage: lwfail.py seed N qmax"""
import sys, random
from backelin import lw
def brute(gens, c_hint):
    N = c_hint + 3 * max(gens); ins = [False] * N; ins[0] = True
    for x in range(1, N): ins[x] = any(x >= g and ins[x - g] for g in gens)
    F = max(x for x in range(N) if not ins[x]); c = F + 1; m = min(gens)
    q = -(-c // m); h = c - (q - 1) * m
    L = sum(1 for x in range((q - 1) * m, c) if ins[x])
    mg = [g for g in gens if not any(ins[g - a] and a != 0 and g - a != 0 and ins[a] for a in range(1, g))]
    return dict(c=c, q=q, h=h, L=L, e=len(mg), mingens=mg, LASTWIN=len(mg) * L - h)
if __name__ == "__main__":
  seed, N, qmax = map(int, sys.argv[1:4]); random.seed(seed); found = 0
  for _ in range(N):
    m = random.randint(20, 120); gens = [m] + random.sample(range(m + 1, 6 * m), 3)
    x = lw(gens)
    if x and x["LASTWIN"] < 0:
      b = brute(gens, x["c"]); found += 1
      print("gens", sorted(gens), "apery-based", x, "\n   brute", b)
      if found >= 4: break
