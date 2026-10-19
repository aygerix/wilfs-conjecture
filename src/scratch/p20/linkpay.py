"""Link decomposition of the chain deficit and the local RICH-PAY balance (lead, 2026-10-19).
For v in Ap: depth_a(v) = max{j : v - j n_a in S}; rho_a(v) = s_{v-n_a} - s_v (links only);
P(v) = sum_a depth_a(v) rho_a(v); E(v) = sum_a n_a depth_a(v) - v; L1(v) = sum_a depth_a(v) (lam(v - n_a) - lam(v)).
Checks (exact): Delta = sum_v P(v) - m*Ltop (Ltop = sum_{w,a} lam(top_a(w))), and P(v) - E(v) = v - m*L1(v) for all v.
Rich: m*L1(v) >= v (then P(v) <= E(v)).  Variants (each implies Wilf):
  CHAIN-U   : Delta - Eu <= C2,   Eu = sum_v max(0, sum_{a: v-n_a in S} n_a - v)
  CHAIN-POOR: sum_{v poor} P(v) - m*Ltop <= C2
  WILF+     : sum_v max(0, v - m*L1(v)) - m*Ltop <= C2   (Wilf is the same with the max removed)
usage: python linkpay.py m g1,g2,...   prints the numbers;  imported by scans."""
import sys
sys.path.insert(0, '../p18')
from chain_interval import apery
def linkpay(m, gens_in):
    w = apery(m, [m] + gens_in)
    if any(x is None for x in w): return None
    ap = set(w); M = max(w); c = M - m + 1
    gens = sorted(x for x in w if x > 0 and not any(w[j] + w[(x - w[j]) % m] == x for j in range(1, m) if (x - w[j]) % m))
    d = len(gens)
    if d < 2: return None
    C2 = m*(m-1)//2; need = (d-1)*C2
    s = lambda x: (M - x) % m; lam = lambda x: (M - x) // m
    Delta = 0; Ltop = 0
    for n in gens:
        for x in w:
            t = x
            while t + n in ap: t += n
            Delta += s(x) - (M - t); Ltop += lam(t)
    SP = 0; Ppoor = 0; E = 0; Eu = 0; idbad = 0; nrich = 0; Wp = 0
    for v in w:
        P = 0; Ev = -v; Ld = 0; U = 0
        for n in gens:
            dep = 0; y = v
            while y - n in ap: y -= n; dep += 1
            if dep: P += dep*(s(v - n) - s(v)); U += n; Ld += dep*(lam(v - n) - lam(v))
            Ev += n*dep
        if P - Ev != v - m*Ld: idbad += 1
        SP += P; E += Ev; Eu += max(0, U - v)
        Wp += max(0, v - m*Ld)
        if m*Ld >= v: nrich += 1
        else: Ppoor += P
    if Delta != SP - m*Ltop: idbad += 1000
    return dict(m=m, d=d, M=M, C2=C2, need=need, Delta=Delta, E=E, Eu=Eu, idbad=idbad, nrich=nrich,
                chain=(d*C2 - Delta)/need, chainU=(d*C2 - Delta + Eu)/need, poor=(Ppoor - m*Ltop) / C2, wplus=(Wp - m*Ltop) / C2, wilf=(d*C2 - Delta + E)/need)
if __name__ == '__main__':
    m = int(sys.argv[1]); g = [int(x) for x in sys.argv[2].split(',')]
    print(linkpay(m, g))
