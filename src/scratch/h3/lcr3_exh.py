"""Exhaustive test of L-CR3 for small core dimension k (lead, 2026-10-19).
L-CR3 (conjecture): for every height-<=3 down-set C in N^k containing all units, every unit non-maximal, and every
injective linear labeling of C into Z/m with s = m-|C| and k+s >= 6, the crude bound CR holds:
    (2T+P_A)(n+s) + (T+P_A)^2 - P_A^2/2 + T + P_A/2 <= (k+s+1) n(n+1)/2,     n = k + P_N
(T cubics, P_N / P_A non-maximal / maximal pairs).  [CR for the tile C + s spikes; it implies MaxCL at every sigma.]
Method: enumerate all down-sets C (pair set, then down-closed cubic set), keep those with a failing s in the range
s >= max(0, 6-k) (CR is linear in s; the failing set is s < s*), and for each failing (C, s) search all labelings
p in (Z/m)^k (p sorted up to the coordinate symmetry of C is NOT used; all p with 1 <= p_i < m are tried).
usage: python lcr3_exh.py k [full]
   full: for every CR-failing (C,s) with k+s>=6, check the MaxCL spike form (k+s+1)sum_N r - sum_A (|y|-1) r >= 0
         on EVERY injective labeling p in [1,m-1]^k and every sigma (closing the core dimension k, given H3-D5 for d<=5)."""
import sys, itertools
from fractions import Fraction


def shapes(k):
    pairs = [tuple(sorted(c)) for c in itertools.combinations_with_replacement(range(k), 2)]
    cubs = [tuple(sorted(c)) for c in itertools.combinations_with_replacement(range(k), 3)]
    for pm in range(1 << len(pairs)):
        P = [pairs[i] for i in range(len(pairs)) if pm >> i & 1]; Ps = set(P)
        # every unit non-maximal: each unit lies in some pair
        if any(all(a not in z for z in P) for a in range(k)): continue
        legal = [c for c in cubs if all(tuple(sorted(c[:i]+c[i+1:])) in Ps for i in range(3))]
        for cm in range(1 << len(legal)):
            T = [legal[i] for i in range(len(legal)) if cm >> i & 1]
            yield P, T


def cr_fail_range(k, P, T):
    Tset = set(T)
    PN = [z for z in P if any(tuple(sorted(z+(c,))) in Tset for c in range(k))]
    nPN, nPA, nT = len(PN), len(P)-len(PN), len(T)
    n = k+nPN; Q = 2*nT+nPA
    L0 = Fraction(Q*n+(nT+nPA)**2)-Fraction(nPA*nPA, 2)+nT+Fraction(nPA, 2)
    R0 = Fraction((k+1)*n*(n+1), 2); den = Fraction(n*(n+1), 2)-Q
    if L0 <= R0: return None
    if den <= 0: return float('inf')
    sstar = (L0-R0)/den     # CR fails iff s < sstar
    return sstar


def vec(c, k):
    v = [0]*k
    for a in c: v[a] += 1
    return v


if __name__ == '__main__':
    k = int(sys.argv[1]); FULL = len(sys.argv) > 2; nlab = 0; nphase = 0; minsl = None; nsh = 0; nfail = 0; nreal = 0; cases = 0; ninf = 0
    for P, T in shapes(k):
        nsh += 1
        if not T: continue          # height <= 2 cores: Flat-MaxCL (LEAN); CR is not the tool there
        ss = cr_fail_range(k, P, T)
        if ss is None: continue
        if ss == float('inf'): ninf += 1; ss = 60
        size = 1+k+len(P)+len(T)
        cells = [[0]*k]+[vec((a,), k) for a in range(k)]+[vec(z, k) for z in P]+[vec(c, k) for c in T]
        for s in range(max(0, 6-k), int(ss)+1):
            if s >= ss: break
            nfail += 1; m = size+s
            found = None
            Tset = set(T); PNs = set(z for z in P if any(tuple(sorted(z+(c,))) in Tset for c in range(k)))
            # coefficient per cell in the spike form: N cells (origin, units, non-max pairs) d+1; max pairs -1; cubics -2
            dd = k+s
            coef = [dd+1]+[dd+1]*k+[(dd+1) if z in PNs else -1 for z in P]+[-2]*len(T)
            for p in itertools.product(range(1, m), repeat=k):
                lab = []
                seen = set(); ok = True
                for x in cells:
                    v = sum(x[i]*p[i] for i in range(k)) % m
                    if v in seen: ok = False; break
                    seen.add(v); lab.append(v)
                if not ok: continue
                found = p
                if not FULL: break
                nlab += 1
                for sg in range(m):
                    S = sum(c*((v-sg) % m) for c, v in zip(coef, lab)); nphase += 1
                    if minsl is None or S < minsl: minsl = S
                    if S < 0: print("MAXCL FAIL k", k, "m", m, "s", s, "P", P, "T", T, "p", p, "sigma", sg, "S", S, flush=True)
            cases += 1
            if found:
                nreal += 1
                if nreal <= 15: print("L-CR3 VIOLATION: k", k, "m", m, "s", s, "pairs", P, "cubics", T, "p", found, flush=True)
    print("full-check labelings", nlab, "phase checks", nphase, "min slack", minsl) if FULL else None
    print("k", k, "shapes", nsh, "height-3 shapes failing CR for all s (capped at s<60):", ninf, " CR-failing (C,s) with k+s>=6:", nfail, "realizable:", nreal)
