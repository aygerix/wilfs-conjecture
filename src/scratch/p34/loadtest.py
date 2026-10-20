import sys, random
sys.path.insert(0, '.')
from halltop import load
NS, SEED, MMAX = map(int, sys.argv[1:4]); rnd = random.Random(SEED); tot = f = 0; worst = None
for _ in range(NS):
    m = rnd.randint(4, MMAX); G = [rnd.randint(m + 1, rnd.choice([2, 3, 4]) * m) for _ in range(rnd.randint(2, 6))]
    v = load(m, G)
    if v is None: continue
    tot += 1
    if v[0] > 0:
        f += 1
        if f <= 6: print("LOAD FAIL m=%d c=%d rho=%d gens=%s excess=%s" % (m, v[1], v[3], v[2], v[0]), flush=True)
    if worst is None or v[0] > worst[0]: worst = (v[0], m) + v[1:]
print("leaves", tot, "load failures", f, "worst", worst)
