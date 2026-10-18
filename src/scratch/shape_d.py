# Shape criteria in every dimension d = e-1, on S with 3e < m and c > 3m (the range not covered by Eliahou).
#  HT_d     : (m+1) H > (d-1) C(m,2) - m   (=> W >= 0; proved implication via CH')
#  MAXSUM_d : sum_{y in Max} (|y| + d) <= (d+1) m/2 + (d-1)/2   (=> HT_d, since H >= d m - sum_Max (|y|+d))
import sys, random, time
sys.path.insert(0, 'src')
from math import comb, gcd
from functools import reduce
from ns import NS
from cl import factorizations_down_set
def shape(s):
    m = s.m; Pp, best = factorizations_down_set(s, 'grlex'); d = len(Pp); D = set(best.values())
    add = lambda x, i: x[:i] + (x[i]+1,) + x[i+1:]
    ht = {}
    for x in sorted(D, key=lambda x: -sum(x)):
        ht[x] = max([ht[add(x, i)] + 1 for i in range(d) if add(x, i) in D], default=0)
    top = {}
    for i in range(d):
        for x in sorted(D, key=lambda x: -x[i]):
            z = add(x, i); top[(x, i)] = top[(z, i)] if z in D else x
    H = sum(ht[top[(x, i)]] for x in D for i in range(d))
    MS = sum(sum(y) + d for y in D if ht[y] == 0)
    ht_ok = (m + 1) * H > (d - 1) * comb(m, 2) - m
    ms_slack = (d + 1) * m + (d - 1) - 2 * MS          # >= 0  <=>  MAXSUM_d
    return d, H, MS, ht_ok, ms_slack
if __name__ == '__main__':
  e0, e1, N, seed, budget = map(int, sys.argv[1:6])
  rnd = random.Random(seed); t0 = time.time(); st = {}
  while time.time() - t0 < budget:
      e = rnd.randint(e0, e1); m = rnd.randint(3 * e + 1, max(3 * e + 2, 70)); K = rnd.choice((2, 3, 4, 6))
      g = sorted(rnd.sample(range(m + 1, K * m), e - 1))
      if reduce(gcd, [m] + g) != 1: continue
      s = NS.from_generators([m] + g)
      if s.e != e or s.m != m or s.c <= 3 * s.m: continue
      d, H, MS, ok, sl = shape(s)
      r = st.setdefault(e, [0, 0, 0, None, None])
      r[0] += 1; r[1] += not ok; r[2] += sl < 0
      if r[3] is None or sl < r[3][0]: r[3] = (sl, [m] + g, s.c)
      hr = (m + 1) * H / max(1, (d - 1) * comb(m, 2) - m)
      if r[4] is None or hr < r[4][0]: r[4] = (round(hr, 3), [m] + g, s.c)
  print(f'seed {seed}, {time.time()-t0:.0f}s')
  for e in sorted(st):
      n, f1, f2, w, h = st[e]
      print(f' e={e}: {n} S (3e<m, c>3m); HT_d fails {f1}; MAXSUM_d fails {f2}; min MAXSUM slack {w}; min HT ratio {h}')
