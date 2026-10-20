"""Depth-four tools (lead, 2026-10-20): Apery set, K, Lambda, window data, shift sources.  Exact integers."""
import sys

def semigroup(gens):
    m = min(gens)
    INF = float('inf'); w = [INF] * m; w[0] = 0
    import heapq
    pq = [(0, 0)]
    while pq:
        d, r = heapq.heappop(pq)
        if d > w[r]: continue
        for n in gens:
            v = d + n; rr = v % m
            if v < w[rr]: w[rr] = v; heapq.heappush(pq, (v, rr))
    return m, w

def analyze(gens, verbose=True):
    m, w = semigroup(gens)
    ap = set(w)
    ins = lambda v: v >= 0 and w[v % m] <= v
    inap = lambda v: v >= 0 and w[v % m] == v
    # minimal generators
    P = [x for x in sorted(w) if x > 0 and not any(y > 0 and y < x and ins(x - y) for y in w)]
    P = [p for p in P]  # non-m generators (Apery elements that are minimal)
    M = max(w); c = M - m + 1; g = sum(x // m for x in w); e = len(P) + 1
    q = -(-c // m); h = c - (q - 1) * m
    W = e * (c - g) - c
    lam = {r: (M - w[r]) // m for r in range(m)}
    K = {}; Lam = 0; nu = {}
    for r in range(m):
        x = w[r]; k = q - lam[r]
        for a in P:
            j = 0
            while ins(x - (j + 1) * a): j += 1
            nu[(r, a)] = j
            if j: k -= j * ((M - (x - a)) // m - lam[r])
            if not inap(x + a): Lam += (j + 1) * lam[r]
        K[r] = k
    inw = lambda r: (r - h) % m < h
    Y = [r for r in range(m) if K[r] == 1 and inw(r)]
    Z = sum(-K[r] for r in range(m) if K[r] < 0)
    Nlo = sum(1 for r in range(m) if K[r] <= 0 and not inw(r))
    out = dict(m=m, c=c, h=h, q=q, e=e, W=W, Lam=Lam, Z=Z, Nlo=Nlo, RAhi=len(Y), P=P, w=w, K=K, lam=lam, Y=Y, M=M)
    if verbose:
        print(f"S=<{','.join(map(str, [m] + P))}> m={m} c={c} q={q} h={h} e={e} W={W} Lam={Lam} Z={Z} Nlo={Nlo} RAhi={len(Y)}")
        for y in Y:
            fac = [a for a in P if ins(w[y] - a)]
            print(f"  short critical cube at r={y}: v={w[y]} factors {fac} (offsets {[a - m for a in fac]})")
        for a in P:
            row = []
            for y in Y:
                x = (y - a) % m; v = w[x]
                kind = 'Z' if K[x] <= -1 else ('L' if lam[x] >= 1 and not inap(v + a) else ('C0' if lam[x] == 0 else '??'))
                row.append(f"y={y}<-x={x}(v={v},lam={lam[x]},K={K[x]}):{kind}")
            print(f"  t={a}: " + "; ".join(row))
    return out

if __name__ == "__main__":
    analyze([int(t) for t in sys.argv[1].split(',')])
