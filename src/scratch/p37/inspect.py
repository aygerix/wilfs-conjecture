# inspect TRUNC3 instances: U, T, T \ U, invariants (independent of the C tools)
from itertools import combinations_with_replacement as cwr
def inspect(A, m):
    A0 = [0] + list(A); S3 = sorted(set(sum(t) for t in cwr(A0, 3)))
    sig = {}
    for v in S3: sig.setdefault(v % m, v)
    assert len(sig) == m
    M = max(sig.values()); c = M - m + 1
    inU = lambda x: x >= sig[x % m]
    N = c + 3 * m; inT = [False] * N; inT[0] = True
    for x in range(1, N): inT[x] = any(x >= g and inT[x - g] for g in list(A) + [m])
    cT = max(x for x in range(N) if not inT[x]) + 1 if not all(inT) else 0
    lT = sum(inT[x] for x in range(cT)); lU = sum(inU(x) for x in range(c))
    gens = [g for g in sorted(set(A) | {m}) if not any(inT[h] and inT[g - h] for h in range(1, g))]
    TU = [x for x in range(N) if inT[x] and not inU(x)]
    e = len(A) + 1
    print(f"A={list(A)} m={m}: c_U={c} l_U={lU} e={e} W_e(U)={e*lU-c} ratio={e*lU/c:.3f} | T gens={gens} e(T)={len(gens)} c_T={cT} l_T={lT} W(T)={len(gens)*lT-cT} | T\\U={TU} h={len(TU)} dc={c-cT}")
    print("   L(U) =", [x for x in range(c) if inU(x)])
for A, m in [((4,9,10),13), ((7,16,17,19),23), ((12,25,26,28,30),31), ((7,15,17,18,22),24), ((17,36,38,39,43,44),46), ((9,14,28,29,30,31),32), ((14,27,35,36,38,40),41)]:
    inspect(A, m)
