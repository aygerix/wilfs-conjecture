# e = 4 residual of the sharp tau-criterion: (e-2)(m+1) >= 2(e-2) tau + 2 P2.  Exhaustive by genus + random.
import sys, itertools, random
from math import gcd
from functools import reduce
sys.path.insert(0, 'src')
from ns import NS, all_by_genus
from cl import factorizations_down_set
def analyse(s):
    m, c = s.m, s.c; P = s.P; e = len(P); d = e - 1
    ap = sorted(s.apery()); Xq = [u for u in ap if c <= u < c + m]
    _, best = factorizations_down_set(s, 'grlex'); cells = set(best.values())
    Y = [best[u] for u in Xq]
    P2 = sum(1 for y, z in itertools.combinations(Y, 2) if sum(1 for a in range(d) if y[a] != z[a]) == 2)
    tau = len(Xq)
    sharp = (d - 1)*(m + 1) >= 2*(d - 1)*tau + 2*P2
    crude = (d - 1)*(m + 1) >= tau*(tau + 2*e - 5)
    L = [d + sum(y) for y in Y]; pi = [u - c + 1 for u in Xq]
    top2_lhs = sum(a*b for a, b in zip(pi, L)); top2_rhs = m*((d + 1)*m + d - 1)//2
    two = any(tuple(int(i in (a, b)) for i in range(d)) not in cells for a in range(d) for b in range(a+1, d))
    cross_sum = sum(sum(y) + 1 for y in Y)
    return dict(m=m, tau=tau, P2=P2, sharp=sharp, crude=crude, two=two, t=s.t(), slack=(top2_rhs - top2_lhs)/top2_rhs,
                crossgap=m + P2 - cross_sum, q=s.q, P=P)
def _main():
  pass
mode = sys.argv[1] if __name__ == '__main__' else None
res = []
if mode is None:
    pass
elif mode == 'genus':
    G = int(sys.argv[2])
    for g, s in all_by_genus(G):
        if g and s.e == 4: res.append(analyse(s))
elif mode == 'random':
    rng = random.Random(int(sys.argv[2])); N = int(sys.argv[3]); MLO, MHI = int(sys.argv[4]), int(sys.argv[5])
    while len(res) < N:
        m = rng.randint(MLO, MHI); k = rng.choice([2, 3, 4, 6, 10])
        gens = sorted(set([m] + [rng.randint(m + 1, k*m) for _ in range(3)]))
        if len(gens) != 4 or reduce(gcd, gens) != 1: continue
        s = NS.from_generators(gens)
        if s.e != 4: continue
        res.append(analyse(s))
fail = [r for r in res if not r['sharp']]
if mode: print(f'{mode}: e=4 semigroups {len(res)}; crude criterion holds {sum(r["crude"] for r in res)}; sharp holds {len(res) - len(fail)}; residual {len(fail)}; residual two-face {sum(r["two"] for r in fail)}; residual with m>=20 {sum(r["m"] >= 20 for r in fail)}')
if mode and fail:
    print('  residual: min TOP2 slack', round(min(r['slack'] for r in fail), 3), ' max tau', max(r['tau'] for r in fail), ' max m', max(r['m'] for r in fail))
    for r in sorted(fail, key=lambda r: -r['m'])[:6]: print('   ', {k: r[k] for k in ('P', 'm', 'tau', 'P2', 't', 'q', 'two', 'crossgap')}, 'slack', round(r['slack'], 3))
