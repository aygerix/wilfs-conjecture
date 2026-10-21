r"""Near-B2 (height-2) factorization tiles (lead, 2026-10-20): S = <m, g_1..g_d> with g_b = delta_b + k_b m.
For random near-Sidon delta mod m (all degree<=2 sums of distinct residue), lifts k_b in {1..K}, report tiles of
height 2: CR_DEP slack, DEP-CARRY value rho0 + sum kappa + Dep (conductor phase and min over phases), MaxCL
slack (Lambda form: rho0 m + kappa m + Lam_nm), W, open-regime flag.  Usage: python b2fam.py NS SEED DMIN DMAX K"""
import sys, random
sys.path.insert(0, '.')
from tile import build
from crdep import crdep
from depcarry import carry
NS, SEED, DMIN, DMAX, K = map(int, sys.argv[1:6]); rnd = random.Random(SEED)
stats = {}; worst = {}
cnt = 0
while cnt < NS:
    d = rnd.randint(DMIN, DMAX); full = 1 + d + d * (d + 1) // 2
    m = full - rnd.randint(0, max(0, d // 2 + 1))
    delta = rnd.sample(range(1, m), d)
    G = sorted(set(x + rnd.randint(1, K) * m for x in delta))
    R = build(m, G)
    if R is None: continue
    c, gens, M = R; N = len(gens)
    if N < 2 or max(sum(a) for a in M) != 2: continue
    cnt += 1
    D = list(M); dl = [x % m for x in gens]; rho0 = (-c) % m
    sl, dep = crdep(D, N)
    kap, tops, dep2, mx, lnm = carry(m, D, dl, rho0)
    dc = rho0 + kap + dep; mcl = rho0 * m + kap * m + lnm
    dcmin = min(s + carry(m, D, dl, s)[0] + dep for s in range(m))
    g = sum(x // m for x in M.values()); W = (N + 1) * (c - g) - c
    op = int(3 * (N + 1) < m and c > 4 * m)
    key = (N, op); st = stats.setdefault(key, [0, 0, 0, 0, 0, 0])
    st[0] += 1; st[1] += sl < 0; st[2] += dc < 0; st[3] += dcmin < 0; st[4] += mcl < 0; st[5] += W < 0
    w = worst.get(key)
    if w is None or sl < w[0]: worst[key] = (sl, dep, dc, dcmin, mcl, W, m, c, gens)
for key in sorted(stats):
    st = stats[key]
    print("d=%2d open=%d: n=%5d CRDEP<0 %5d DEPCARRY<0 %d DEPCARRY(any phase)<0 %d MaxCL<0 %d W<0 %d | worst CRDEP %s" % (key + tuple(st) + (worst[key],)))
