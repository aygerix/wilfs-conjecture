# HCR / HCR+ on structured families with many generators, to test "HCR(+) >= 1 whenever m > 3e"
# (m <= 3e is Eliahou's range).  Families: intervals <m, m+1..m+d>, arithmetic <m, m+k, .., m+dk>,
# shifted intervals <m, a, a+1, .., a+d-1>.
import sys; sys.path.insert(0, 'src'); sys.path.insert(0, 'fwx')
from math import gcd
from ns import NS
from cl import factorizations_down_set
from hcr import parts
from hcrp import hcrp_shape
fam = sys.argv[1]; dlo, dhi, mfac = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
worst = {}
for d in range(dlo, dhi + 1):
    e = d + 1
    for m in range(3 * e + 1, mfac * e + 1):
        gens = []
        if fam == 'int': gens = [[m] + [m + j for j in range(1, d + 1)]]
        elif fam == 'ari': gens = [[m] + [m + k * j for j in range(1, d + 1)] for k in range(2, m) if gcd(k, m) == 1][:6]
        elif fam == 'sh': gens = [[m] + [a + j for j in range(d)] for a in range(m + 2, 3 * m, max(1, m // 7))]
        for g in gens:
            try: s = NS.from_generators(g)
            except Exception: continue
            if s.e != e or s.c <= 3 * m: continue
            hcr, hto, two, W = parts(s)
            flag = ''
            if hcr < 1 - 1e-12:
                Pp, best = factorizations_down_set(s, 'grlex'); hp = hcrp_shape(list(best.values()))
                flag = f' HCR+ {hp:.4f}' + (' <-- HCR+ FAIL' if hp < 1 - 1e-12 else '')
                print(f'e={e} m={m} {g[:3]}..{g[-1]} c={s.c} W={W} two={two} HCR {hcr:.4f}{flag}', flush=True)
            if d not in worst or hcr < worst[d][0]: worst[d] = (round(hcr, 4), m, g[1], g[-1])
    print(f'# d={d} e={e} worst HCR {worst.get(d)}', flush=True)
