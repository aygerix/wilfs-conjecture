# Lambda-criterion stress test on random / structured semigroups with m > 3e (outside Eliahou's 3e >= m range).
import sys, random, itertools
from math import gcd
from functools import reduce
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from lam import lam
def test(g, tag, out):
    if reduce(gcd, g) != 1: return
    s = NS.from_generators(g)
    if s.e < 3 or 3*s.e >= s.m: return
    L, P, m, d = lam(s); need = (d - 1)*(m - 1)/2
    out.append((L/need, tag, s.P[:12], s.e, m, s.c, L, need, s.W))
out = []
rng = random.Random(int(sys.argv[1])); N = int(sys.argv[2]); MMAX = int(sys.argv[3])
# 1) random: m in [10, MMAX], k generators in (m, K m)
while len(out) < N:
    m = rng.randint(10, MMAX); k = rng.randint(2, max(2, min(12, m//3 - 1))); K = rng.choice([2, 3, 4, 6])
    g = sorted(set([m] + [rng.randint(m + 1, K*m) for _ in range(k)]))
    test(g, 'rnd', out)
# 2) clustered generators (dense near a point) -- high type, two-face-like
for _ in range(N//2):
    m = rng.randint(20, MMAX); k = rng.randint(3, max(3, min(10, m//3 - 1))); base = rng.randint(m + 1, 2*m)
    g = sorted(set([m] + [base + rng.randint(0, max(2, m//5)) for _ in range(k)]))
    test(g, 'clu', out)
# 3) Eliahou-Fromentin style: <{m} u A>_{4m}: A in [(3m+1)/2, (5m-1)/3] (truncate at 4m)
for _ in range(N//4):
    m = rng.randint(30, MMAX); lo, hi = (3*m + 1)//2, (5*m - 1)//3
    if hi - lo < 4: continue
    A = sorted(rng.sample(range(lo, hi + 1), rng.randint(3, min(8, hi - lo))))
    g = sorted(set([m] + A + list(range(4*m, 5*m))))
    test(g, 'EF4m', out)
# 4) truncations <m, a, b> u [k m, inf)
for _ in range(N//4):
    m = rng.randint(20, MMAX); k = rng.randint(3, 6)
    base = sorted(set([m] + [rng.randint(m + 1, 2*m) for _ in range(rng.randint(2, 4))]))
    if reduce(gcd, base) != 1: continue
    s0 = NS.from_generators(base)
    g = sorted(set(base + [x for x in range(k*m, (k + 1)*m) if x not in s0]))
    if g: test(g, 'trunc', out)
out.sort()
print('tested', len(out), 'with m > 3e; Lambda-criterion fails', sum(1 for r in out if r[0] < 1))
for r in out[:12]: print('  ratio %.3f' % r[0], r[1:])
