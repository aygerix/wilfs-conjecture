"""Stress test of the final-window criterion FW (src/fw.py) on hard regions:
  (R) random S = <m, a_1..a_d> with a_i in (m, K m), kept only if the depth q = ceil(c/m) >= 4;
  (E) Eliahou-type S = <gens> U [c, oo) with c = q m, q >= 4 (the W_0 < 0 examples live here), random small gens;
  (X) explicit: Eliahou's <14,22,23>_56 and family variants.
Reports, per e, how many S satisfy FW (bound >= 0), the worst bound/m, and the failures (with W and known_wilf coverage)."""
import sys, random
sys.path.insert(0, 'src')
from ns import NS
from fw import fw
from known import known_wilf
def closure_with_conductor(gens, c):
    s = NS.from_generators(gens + list(range(c, c + gens[0] + 1)))
    return s
def run(mode, N, seed):
    rnd = random.Random(seed); stat = {}; fails = []; tested = 0
    for it in range(N):
        if mode == 'R':
            m = rnd.randint(16, 60); d = rnd.randint(4, 9); K = rnd.choice((2, 3, 4, 6, 8))
            gens = [m] + rnd.sample(range(m + 1, K * m), min(d, K * m - m - 1))
            try: s = NS.from_generators(gens)
            except ValueError: continue
            if s.c < 4 * s.m: continue
        elif mode == 'E':
            m = rnd.randint(10, 40); q = rnd.randint(4, 6); k = rnd.randint(1, 4)
            gens = [m] + rnd.sample(range(m + 1, 2 * m), k)
            try: s = closure_with_conductor(gens, q * m)
            except ValueError: continue
        else:
            s = closure_with_conductor([14, 22, 23], 56)
        r = fw(s)
        if r is None: continue
        tested += 1
        k = r['e']; st = stat.setdefault(k, [0, 0, float('inf')]); st[0] += 1
        if r['bound'] >= 0: st[1] += 1
        else:
            fails.append((s.P, r['m'], s.c, r['W'], r['tau'], r['E'], r['deep'], r['bound'], known_wilf(s)[:3]))
        st[2] = min(st[2], r['bound'] / r['m'])
        if mode == 'X': break
    print(f'mode {mode} seed {seed}: tested {tested}')
    for k in sorted(stat): print(f'  e={k}: {stat[k][0]} S, FW holds {stat[k][1]}, min bound/m {stat[k][2]:.3f}')
    print('  failures:', len(fails))
    for f in fails[:25]: print('   ', f)
if __name__ == '__main__':
    run(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
