"""Show the column-reflection localization Delta(x) on the Apery tile (lex normal forms) and, for each deficient
cell y, the cells of the principal ideal below y with their Delta, column tops and rooms.  usage: cp_show.py m n1 n2 ..."""
import sys
def tile(m, gens):
    INF = 10**9
    ap = [INF]*m; ap[0] = 0; done = [False]*m
    for _ in range(m):
        b = min((r for r in range(m) if not done[r] and ap[r] < INF), key=lambda r: ap[r])
        done[b] = True
        for g in gens:
            r2 = (b+g) % m
            if ap[b]+g < ap[r2]: ap[r2] = ap[b]+g
    ng = [ap[r] for r in range(1, m) if not any(ap[s]+ap[(r-s) % m] == ap[r] for s in range(1, m) if (r-s) % m)]
    ng.sort(); d = len(ng)
    X = {0: (0,)*d}
    for r in sorted(range(1, m), key=lambda r: ap[r]):
        w = ap[r]; best = None
        for j in range(d):
            if w >= ng[j]:
                t = (w-ng[j]) % m
                if ap[t] == w-ng[j]:
                    c = tuple(X[t][h]+(h == j) for h in range(d))
                    if best is None or c > best: best = c
        X[r] = best
    return ap, ng, X
def main():
    m = int(sys.argv[1]); gens = [int(a) for a in sys.argv[2:]]
    ap, ng, X = tile(m, gens); d = len(ng); M = max(ap)
    cells = {X[r]: ap[r] for r in range(m)}
    def top(x, b):
        J = x[b]
        while True:
            y = list(x); y[b] = J+1; y = tuple(y)
            if y in cells: J += 1
            else: break
        y = list(x); y[b] = J; return tuple(y), J
    Dl = {}
    for x, v in cells.items():
        s = -(v//m)
        for b in range(d):
            t, J = top(x, b); s += (M - (v + (J-2*x[b])*ng[b]))//m
        Dl[x] = s
    g = sum(v//m for v in cells.values()); l = sum((M-v)//m for v in cells.values())
    print(f"m={m} gens={ng} M={M} K={M//m} mu={M%m} W={d*l-g} sumDelta={sum(Dl.values())}")
    for y in sorted(cells, key=lambda x: cells[x]):
        if Dl[y] < 0:
            vy = cells[y]
            print(f" deficient y={y} v={vy} res={vy%m} eps={M-vy} Delta={Dl[y]}  digits={[ (y[b]*ng[b])%m for b in range(d)]}")
            below = [x for x in cells if all(x[h] <= y[h] for h in range(d))]
            tot = 0
            for x in sorted(below, key=lambda x: cells[x]):
                tops = []
                for b in range(d):
                    t, J = top(x, b); tops.append(f"{b}:J={J},u={M-cells[t]}")
                tot += Dl[x]
                print(f"    x={x} v={cells[x]} kappa={cells[x]//m} Delta={Dl[x]}  " + " ".join(tops))
            print(f"    principal ideal sum = {tot}")
main()
