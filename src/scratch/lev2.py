# Semigroups whose Apery set (w.r.t. m) consists of 0, single generators and sums of two generators ("level <= 2").
# Random search over d generators n_a = r_a + k_a m; report the smallest W (and W relative to the near-star bound).
import sys, random; sys.path.insert(0, 'src')
from ns import NS
rnd = random.Random(int(sys.argv[1])); trials = int(sys.argv[2])
for m in map(int, sys.argv[3].split(',')):
    for d in map(int, sys.argv[4].split(',')):
        best = None; cnt = 0
        for _ in range(trials):
            R = rnd.sample(range(1, m), d); kmax = rnd.choice([1, 2, 3, 5])
            g = [m] + [r + m * rnd.randint(1, kmax) for r in R]
            try: s = NS.from_generators(g)
            except Exception: continue
            if s.e != d + 1: continue
            P = sorted(set(g[1:])); two = {a + b for a in P for b in P}
            ap = s.apery()
            if not all(w == 0 or w in P or w in two for w in ap): continue
            cnt += 1; W = s.W
            if best is None or W < best[0]: best = (W, s.c, round(s.c / m, 2), sorted(g))
        print(f"m={m} d={d}: {cnt} level<=2 S; min W {best[:3] if best else None} gens {best[3] if best else ''}", flush=True)
