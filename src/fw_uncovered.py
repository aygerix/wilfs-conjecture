"""FW / FWx on semigroups NOT covered by any THEORETICAL known condition (src/known.py minus the finite computational
ones: m <= 19, g <= 100, max P <= 60, m|c g <= 120).  Generators: random deep S with few small generators plus
Eliahou-type closures, kept only if uncovered.  Reports FW, FWx failures."""
import sys, random
sys.path.insert(0, 'src')
from ns import NS
from known import known_wilf
from fw_refine import bounds
from fw_hard import closure_with_conductor
COMP = ('m<=19', 'g<=100', 'maxP<=60', 'm|c, g<=120')
def uncovered(s):
    return all(any(k.startswith(p) for p in COMP) for k in known_wilf(s))
if __name__ == '__main__':
    N, seed = int(sys.argv[1]), int(sys.argv[2]); rnd = random.Random(seed)
    n = 0; fw_bad = []; fwx_bad = []; per_e = {}
    for it in range(N):
        try:
            if rnd.random() < 0.5:
                m = rnd.randint(20, 70); d = rnd.randint(4, 8)
                gens = [m] + rnd.sample(range(m + 1, rnd.choice((3, 4, 6)) * m), d)
                s = NS.from_generators(gens)
            else:
                m = rnd.randint(20, 50); q = rnd.randint(4, 8); k = rnd.randint(2, 5)
                s = closure_with_conductor([m] + rnd.sample(range(m + 1, rnd.choice((2, 3)) * m), k), q * m)
        except ValueError: continue
        if len(s.P) < 5 or not uncovered(s): continue
        b = bounds(s); n += 1; e = len(s.P)
        pe = per_e.setdefault(e, [0, 0, 0]); pe[0] += 1
        if b['FW'] < 0: fw_bad.append((s.P, s.m, s.c, b['mW'], b['FW'], b['FWx'])); pe[1] += 1
        if b['FWx'] < 0: fwx_bad.append((s.P, s.m, s.c, b['mW'], b['FWx'])); pe[2] += 1
    print(f'seed {seed}: {n} uncovered semigroups with e >= 5; FW < 0: {len(fw_bad)}, FWx < 0: {len(fwx_bad)}')
    for e in sorted(per_e): print(f'  e={e}: {per_e[e][0]} S, FW fails {per_e[e][1]}, FWx fails {per_e[e][2]}')
    for x in fw_bad[:15]: print('  FWbad', x)
    for x in fwx_bad[:15]: print('  FWXbad', x)
