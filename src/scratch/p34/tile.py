"""Lex tile of a numerical semigroup (lead, 2026-10-20).
S given by m and any generating list; minimal generators g_1 < ... < g_N (all except m, INCLUDING right primitives).
Mhat = lex-least (compare last coordinate first) factorizations of the m Apery elements: a down-set tiling Z^N.
Checks the residue identity (every S):
    W = (N+1)(m-1)/2 + Phat - sum_{y in Yhat} (|y| + N) theta_y,
Yhat = Apery elements in [c, c+m), theta_y = (phi(y)-c)/m, Phat = (1/m) sum_{z: phi(z)<c} sum_{i: z+e_i not in Mhat} (z_i+1)(c-phi(z)).
Usage: python tile.py show m g1 .. gk | python tile.py rnd NS SEED MMAX"""
import sys, random
from fractions import Fraction as Fr
def apery(m, G):
    INF = 10**18; w = [INF] * m; w[0] = 0; done = [False] * m
    for _ in range(m):
        u = None
        for x in range(m):
            if not done[x] and w[x] < INF and (u is None or w[x] < w[u]): u = x
        if u is None: break
        done[u] = True
        for g in G:
            v = w[u] + g; s = v % m
            if v < w[s]: w[s] = v
    return None if any(x >= INF for x in w) else w
def build(m, G):
    w = apery(m, G)
    if w is None: return None
    c = max(w) - m + 1
    gens = sorted(x for i, x in enumerate(w) if i and not any(w[a] + w[(i - a) % m] == x for a in range(1, m) if (i - a) % m))
    N = len(gens); A = sorted(w)
    Aset = set(A); fac = {0: (0,) * N}
    for x in A[1:]:
        best = None
        for i, g in enumerate(gens):
            if x - g in fac:
                a = list(fac[x - g]); a[i] += 1; a = tuple(a)
                if best is None or a[::-1] < best[::-1]: best = a
        fac[x] = best
    M = {a: x for x, a in fac.items()}
    return c, gens, M
def ident(m, G, verbose=False):
    R = build(m, G)
    if R is None: return None
    c, gens, M = R; N = len(gens)
    g = sum(x // m for x in M.values()); ell = c - g; W = (N + 1) * ell - c
    up = lambda a, i: tuple(a[t] + (t == i) for t in range(N))
    Ph = Fr(0); top = Fr(0); rows = []
    for a, x in sorted(M.items(), key=lambda t: t[1]):
        miss = [i for i in range(N) if up(a, i) not in M]
        if x < c:
            contrib = sum(Fr((a[i] + 1) * (c - x), m) for i in miss); Ph += contrib
            rows.append((x, a, 'B' if miss else 'I', miss, contrib))
        else:
            th = Fr(x - c, m); top += (sum(a) + N) * th
            rows.append((x, a, 'Y', miss, -(sum(a) + N) * th))
    rhs = Fr((N + 1) * (m - 1), 2) + Ph - top
    if verbose:
        print("m=%d c=%d gens=%s N=%d W=%d  (N+1)(m-1)/2=%s Phat=%s top=%s" % (m, c, gens, N, W, Fr((N + 1) * (m - 1), 2), Ph, top))
        for x, a, t, miss, ct in rows: print("  %5d %-22s %s miss=%s %s" % (x, a, t, miss, ct))
    return W, rhs, c, gens
def main():
  if sys.argv[1] == 'show':
    a = list(map(int, sys.argv[2:])); W, rhs, c, gens = ident(a[0], a[1:], True); print("W =", W, " identity rhs =", rhs)
  else:
    NS, SEED, MMAX = map(int, sys.argv[2:5]); rnd = random.Random(SEED); bad = 0; cnt = 0
    for _ in range(NS):
        m = rnd.randint(3, MMAX); k = rnd.randint(1, 6); G = [rnd.randint(m + 1, rnd.choice([2, 3, 6]) * m + 1) for _ in range(k)]
        v = ident(m, G)
        if v is None: continue
        cnt += 1
        if v[0] != v[1]: bad += 1; print("MISMATCH", m, G, v)
    print("checked", cnt, "mismatches", bad)
if __name__ == '__main__': main()
