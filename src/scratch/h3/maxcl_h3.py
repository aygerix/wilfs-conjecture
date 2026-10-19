"""Test MaxCL on Apery tiles of height <= 3 (lead, 2026-10-19).
MaxCL(sigma): sum_{y in A} (|y|-1) r(y) <= (d+1) sum_{z in N} r(z),  r = (v - sigma) mod m,
A = maximal cells of the grlex factorization tile D, N = D \\ A.  MaxCL(c mod m) implies Wilf (Lean chain).
Reports, per sample, the minimum over sigma of the slack and the slack at sigma = c mod m.
usage: python maxcl_h3.py seed trials mmin mmax hmax"""
import sys, random, heapq

def apery_tile(m, gens):
    """grlex-min factorization tile of Ap(S,m) over gens (all != m); returns dict residue -> (w, x tuple)"""
    d = len(gens)
    best = {0: (0, (0,)*d)}
    # Dijkstra on residues by value; tie-break by (degree, then lex-max) to get grlex-min normal forms
    pq = [(0, 0, (0,)*d)]
    done = set()
    while pq:
        w, deg, x = heapq.heappop(pq)
        r = w % m
        if r in done: continue
        if best[r][0] != w or best[r][1] != x: continue
        done.add(r)
        for a in range(d):
            y = list(x); y[a] += 1; y = tuple(y)
            w2 = w+gens[a]; r2 = w2 % m
            if r2 == 0: continue
            cur = best.get(r2)
            key2 = (w2, sum(y), tuple(-t for t in y))
            if cur is None or key2 < (cur[0], sum(cur[1]), tuple(-t for t in cur[1])):
                best[r2] = (w2, y); heapq.heappush(pq, (w2, sum(y), y))
    return best

def in_semigroup(x, m, gens):
    """is x in <m, gens>? (simple DP)"""
    ok = [False]*(x+1); ok[0] = True
    for v in range(1, x+1):
        if v >= m and ok[v-m]: ok[v] = True; continue
        for g in gens:
            if v >= g and ok[v-g]: ok[v] = True; break
    return ok[x]

def check(m, gens):
    for a in range(len(gens)):
        if in_semigroup(gens[a], m, gens[:a]+gens[a+1:]): return None
    best = apery_tile(m, gens)
    if len(best) != m: return None
    d = len(gens)
    D = {x: w for (w, x) in best.values()}
    # minimal generators only: every gen must be in Ap and not decomposable
    for a in range(d):
        e = tuple(1 if i == a else 0 for i in range(d))
        if e not in D: return None
    # down-set check
    for x in D:
        for a in range(d):
            if x[a] > 0:
                y = list(x); y[a] -= 1
                if tuple(y) not in D: raise RuntimeError("not a down-set")
    H = max(sum(x) for x in D)
    M = max(D.values()); c = M-m+1
    A = [x for x in D if all(tuple(x[i]+(i == a) for i in range(d)) not in D for a in range(d))]
    Aset = set(A)
    g = sum(w//m for w in D.values()); l = sum((M-w)//m for w in D.values())
    W = d*l-g
    slacks = []
    for sig in range(m):
        lhs = sum((sum(y)-1)*((D[y]-sig) % m) for y in A)
        rhs = (d+1)*sum(((D[z]-sig) % m) for z in D if z not in Aset)
        slacks.append(rhs-lhs)
    return H, d, c, W, min(slacks), slacks[c % m], slacks.index(min(slacks))

if __name__ == '__main__':
    seed, T, mmin, mmax, hmax = map(int, sys.argv[1:6])
    rng = random.Random(seed)
    stats = {}; worst = None; n = 0; fails = 0; failc = 0
    for tr in range(T):
        m = rng.randint(mmin, mmax)
        mode = rng.randrange(3)
        if mode == 0:
            d = rng.randint(3, 9); gens = sorted(set(rng.randint(m+1, 2*m-1) for _ in range(d)))
        elif mode == 1:
            d = rng.randint(3, 9); gens = sorted(set(rng.randint(m+1, 4*m) for _ in range(d)))
        else:  # near-arithmetic
            d = rng.randint(3, 8); a0 = rng.randint(m+1, 3*m); st = rng.randint(1, max(1, m//(2*d)))
            gens = sorted(set(a0+i*st for i in range(d)))
        gens = [x for x in gens if x % m]
        if len(set(x % m for x in gens)) < len(gens) or len(gens) < 2: continue
        res = check(m, gens)
        if res is None: continue
        H, d, c, W, mn, atc, sg = res
        if H > hmax: continue
        n += 1
        stats[H] = stats.get(H, 0)+1
        if mn < 0:
            fails += 1
            if fails <= 10: print("FAIL(all sigma)", m, gens, "H", H, "min slack", mn, "at sigma", sg, "W", W, flush=True)
        if atc < 0:
            failc += 1
            if failc <= 10: print("FAIL(sigma=c)", m, gens, "H", H, "slack", atc, "W", W, flush=True)
        norm = mn/(m*m)
        if worst is None or norm < worst[0]: worst = (norm, m, gens, H, mn, sg)
    print(f"seed={seed} tested={n} by height={sorted(stats.items())} fails(all sigma)={fails} fails(sigma=c)={failc}")
    print("worst normalized min slack", worst)
