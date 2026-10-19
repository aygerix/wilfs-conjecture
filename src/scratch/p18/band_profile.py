"""Band profile of S = <m, m+B*> (all generators < 2m): u_H = |R_H| (residues present in band H), the no-carry part
|HB cap [0,m)|, carry part, LK bound.  usage: python band_profile.py m b1 b2 ..."""
import sys
def semigroup_bands(m, Bs):
    gens = [m] + [m + b for b in Bs]
    # exact membership up to bound via DP
    N = 40 * m * m // max(1, len(Bs)) + 10 * m
    while True:
        mem = bytearray(N); mem[0] = 1
        for n in range(1, N):
            for g in gens:
                if g <= n and mem[n - g]: mem[n] = 1; break
        # conductor: need run of m consecutive
        run = 0; c = None
        for n in range(N):
            if mem[n]: run += 1
            else: run = 0
            if run == m: c = n - m + 1; break
        if c is not None: break
        N *= 2
    return mem, c
m = int(sys.argv[1]); Bs = list(map(int, sys.argv[2:])); k = len(Bs); B = [0] + Bs
mem, c = semigroup_bands(m, Bs)
D = -(-c // m); ell = sum(mem[:c]); e = k + 1
print("m=%d B=%s c=%d D=%d ell=%d e*ell/c=%.4f" % (m, B, c, D, ell, e * ell / c))
HB = {0}
for H in range(0, D + 1):
    if H > 0: HB = {x + b for x in HB for b in B}
    R = [r for r in range(m) if mem[H * m + r]]
    nc = len([x for x in HB if x < m])
    print("H=%2d u=%4d nocarry|HB<m|=%4d |HB|=%5d carry_extra=%4d" % (H, len(R), nc, len(HB), len(R) - nc))
