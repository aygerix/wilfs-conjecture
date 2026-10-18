# Height criterion in dimension d = e-1: Def_all = mW + (d-1) C(m,2) >= (m+1) H  (CH' + p_a >= m+1).
# Asserts the inequality on each S, and reports the HT ratio H / ((d-1)(m-1)/2): >= ~1 means the height criterion gives Wilf.
import sys, random, time
sys.path.insert(0, 'src')
from ns import NS
from cl import factorizations_down_set
from math import gcd
from functools import reduce
def H_of(D, d):
    add = lambda x, i: x[:i] + (x[i]+1,) + x[i+1:]
    ht = {}
    for x in sorted(D, key=lambda x: -sum(x)):
        ht[x] = max([ht[add(x, i)] + 1 for i in range(d) if add(x, i) in D], default=0)
    def top(x, i):
        while add(x, i) in D: x = add(x, i)
        return x
    return sum(ht[top(x, i)] for x in D for i in range(d))
e, m0, m1, N, seed, K = map(int, sys.argv[1:7])
rnd = random.Random(seed); t0 = time.time()
worst = {}; nfail = 0; ntot = 0
while ntot < N and time.time() - t0 < 240:
    m = rnd.randint(m0, m1); g = sorted(rnd.sample(range(m + 1, K * m), e - 1))
    if reduce(gcd, [m] + g) != 1: continue
    s = NS.from_generators([m] + g)
    if s.e != e or s.m != m: continue
    p, best = factorizations_down_set(s, 'grlex'); D = set(best.values()); d = e - 1
    H = H_of(D, d); W = s.W
    assert (m + 1) * H <= m * W + (d - 1) * m * (m - 1) // 2 + 0, (s, H, W)
    need = (d - 1) * m * (m - 1) / 2 / (m + 1)
    r = H / need; ntot += 1
    ok = (m + 1) * H > (d - 1) * m * (m - 1) // 2 - m   # => W >= 0
    nfail += not ok
    if m not in worst or r < worst[m][0]: worst[m] = (round(r, 3), [m] + g, H, W, s.c > 3 * m)
print(f'e={e} m in [{m0},{m1}] K={K} seed={seed}: {ntot} S, height criterion fails {nfail}; time {time.time()-t0:.0f}s')
for m in sorted(worst)[::max(1, len(worst)//12)]: print('  m', m, 'min H/need', worst[m])
