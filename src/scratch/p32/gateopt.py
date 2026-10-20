"""[gateopt.py: variant of core1opt.py; extra argv TARGET in {WR1, ANCHOR}: minimizes WR1 = rho + r - (J - C) + P_W
(P_W = sum over wrapped x of (q - lam_x) u(x)) or ANCHOR = rho + r - (J - C) + U_top (E340); strips allowed.]
Gate test (E338): minimize CORE1 = W0 + p over P18 truncations T = <m, m+O> u [qm - rho, inf) of TRUE depth q
(lambda(m-1) >= q, i.e. qm - rho - 1 not in <m, m+O>). W0 = (K+1) ell - q d + rho, p = m - d (lead, 2026-10-20).
CORE1 < 0 refutes ANCHOR-q (ANCHOR-q + ID-q => CORE1). Wilf W = W0 + p (ell - q) is also printed.
Seeds: random O in [m/3, m/2) or a scaled dense seed. Usage: python core1opt.py Q MMIN MMAX KMIN KMAX ITERS SEED"""
import heapq, math, random, sys

def levels(m, rho, O, q):
    INF = 10**9
    lam = [INF] * m; lam[rho % m] = 0
    heap = [(0, rho % m)]
    while heap:
        l, u = heapq.heappop(heap)
        if l != lam[u] or l > q: continue
        for b in O:
            v = u + b; l2 = l + 1 + (1 if v >= m else 0); u2 = v % m
            if l2 < lam[u2]: lam[u2] = l2; heapq.heappush(heap, (l2, u2))
    return lam

sys.path.insert(0, __import__('os').path.dirname(__file__))
from idq import canon
TARGET = sys.argv[8]
def core1(m, rho, O, q):
    lam = levels(m, rho, O, q)
    if lam[m - 1] < q: return None
    ell = sum(q - l for l in lam if l < q); d = sum(1 for l in lam if l <= q)
    K = len(O); W0 = (K + 1) * ell - q * d + rho; p = m - d
    best = canon(m, rho, O, q, q + 3); JC = 0; PW = 0; Ut = 0
    reach = {x: v for x, v in best.items() if v[0] <= q}
    for x, (lx, tx, cx, ax) in reach.items():
        JC += (lx - tx) - sum(ax[i] for i, b in enumerate(O) if ax[i] > 0 and b > x)
        u = 0
        for i, b in enumerate(O):
            y = (x + b) % m; ay = tuple(ax[k] + (k == i) for k in range(K))
            if not (y in reach and reach[y][3] == ay): u += ax[i] + 1
        if lx > tx: PW += (q - lx) * u
        if lx == q - 1: Ut += u
    extra = PW if TARGET == "WR1" else Ut
    return rho + p - JC + extra, W0, p, ell, W0 + p * (ell - q)

def main():
    Q, MMIN, MMAX, KMIN, KMAX, IT, SEED = map(int, sys.argv[1:8])
    rnd = random.Random(SEED)
    def fresh():
        m = rnd.randint(MMIN, MMAX); rho = 0 if rnd.random() < 0.5 else rnd.randint(0, m // 4)
        K = rnd.randint(KMIN, KMAX)
        # EF-type band for depth Q: offsets in [m/(Q-2), m/(Q-3)) when Q >= 4 (Q = 4: [m/2, m)); else anywhere
        if Q >= 4 and rnd.random() < 0.7:
            lo = m // (Q - 2) + 1; hi = min(m - rho, (2 * m) // (2 * Q - 5) + 1) if Q > 4 else min(m - rho, (2 * m) // 3 + 1)
        else:
            lo, hi = 1, m - rho
        if hi - lo < K + 1: lo, hi = 1, m - rho
        O = sorted(rnd.sample(range(lo, hi), K))
        return [m, rho, O]
    def val(st):
        m, rho, O = st
        if len(O) < 1 or len(set(O)) != len(O) or any(b < 1 or b >= m for b in O) or rho < 0 or rho >= m - 1: return None
        return core1(m, rho, O, Q)
    best = None
    for rs in range(10**9):
        cur = fresh(); v = val(cur)
        tries = 0
        while v is None and tries < 200: cur = fresh(); v = val(cur); tries += 1
        if v is None: continue
        T = max(2.0, 0.05 * abs(v[0]) + 2)
        for it in range(IT):
            m, rho, O = cur[0], cur[1], list(cur[2])
            r = rnd.random()
            if r < 0.4:
                i = rnd.randrange(len(O)); O[i] += rnd.choice([-3, -2, -1, 1, 2, 3])
            elif r < 0.55 and len(O) > KMIN: O.pop(rnd.randrange(len(O)))
            elif r < 0.7 and len(O) < KMAX: O.append(rnd.randint(1, m - 1) if rnd.random() < 0.3 else rnd.randint(1, max(1, m - rho - 1)))
            elif r < 0.85: m += rnd.choice([-3, -2, -1, 1, 2, 3])
            else: rho = max(0, rho + rnd.choice([-2, -1, 1, 2]))
            if m < MMIN or m > MMAX: continue
            nxt = [m, rho, sorted(O)]; v2 = val(nxt)
            if v2 is None: continue
            if v2[0] <= v[0] or rnd.random() < math.exp((v[0] - v2[0]) / T):
                cur, v = nxt, v2
                if best is None or v[0] < best[0][0]:
                    best = (v, list(cur[:2]) + [list(cur[2])]); print(TARGET + " best=%d W0=%d p=%d ell=%d W=%d" % v, best[1], flush=True)
            T = max(0.3, T * 0.9995)
        if rs % 20 == 0: print("restart", rs, "best", best[0][0] if best else None, flush=True)

main()
