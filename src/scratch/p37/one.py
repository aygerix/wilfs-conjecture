import sys
from itertools import combinations_with_replacement as cwr
for arg in sys.argv[1:]:
    gens = list(map(int, arg.split(','))); m = gens[0]; A = [g - m for g in gens[1:]]; d = len(A); e = d + 1
    N = 4 * m; inT = [False] * (N + 1); inT[0] = True
    for x in range(1, N + 1): inT[x] = any(x >= g and inT[x - g] for g in A + [m])
    cT = max(x for x in range(N + 1) if not inT[x]) + 1; lT = sum(inT[x] for x in range(cT))
    eT = sum(1 for g in A + [m] if not any(inT[y] and inT[g - y] for y in range(1, g)))
    sig = {}; lev = {}
    for k in range(4):
        for c in cwr(A, k):
            v = sum(c); s = v % m
            if s not in sig or v < sig[s] or (v == sig[s] and k < lev[s]): sig[s] = v; lev[s] = k
    assert len(sig) == m
    D3 = 3 * d * m - e * sum(lev.values()); cU = max(sig.values()) - m + 1
    TU = [x for x in range(cU) if inT[x] and x < sig[x % m]]
    hlo = sum(1 for x in TU if x < cT); hhi = len(TU) - hlo
    lUlo = sum(1 for x in range(cT) if x >= sig[x % m]); rho = e - eT
    dc = cU - cT; p2 = D3 + (e - 1) * dc - e * len(TU)
    print(f"S={gens} m={m} mu={A[0]} e={e} eT={eT} rho={rho} D3={D3} cT={cT} cU={cU} lT={lT} hlo={hlo} hhi={hhi} |U<cT|={lUlo}")
    print(f"   A1 slack {D3 - e*hlo - hhi}  A1-eT slack {D3 + rho*lUlo - eT*hlo - hhi}  PAY2 {p2}  DESC {p2 + rho*lT}  T\\U={TU}")
