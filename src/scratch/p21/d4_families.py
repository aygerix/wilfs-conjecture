"""Emit depth-four structured families for d4_check -g: level-1 intervals <m, m+a..m+a+L-1> and
Sidon-type A-offset sets in (h/2, h) completed by B generators.  Lines: m n1 n2 ..."""
import sys, random
mode = sys.argv[1]
if mode == "int":
    for m in range(20, 151):
        for a in range(1, m):
            for L in range(2, m - a + 1):
                print(m, *[m + a + i for i in range(L)])
elif mode == "sidon":
    rnd = random.Random(int(sys.argv[2]))
    for _ in range(int(sys.argv[3])):
        m = rnd.randint(60, 250); h = rnd.randint(8, m // 2)
        k = rnd.randint(3, 8)
        X = set()
        tries = 0
        while len(X) < k and tries < 2000:
            tries += 1; t = rnd.randint(h // 2 + 1, h - 1)
            if t in X: continue
            Y = sorted(X | {t}); ok = True
            sums = set()
            for i in range(len(Y)):
                for j in range(i, len(Y)):
                    for l in range(j, len(Y)):
                        s = Y[i] + Y[j] + Y[l]
                        if s in sums: ok = False
                        sums.add(s)
            if ok: X.add(t)
        nb = rnd.randint(0, 6)
        B = set(rnd.randint(m + h, 2 * m + h - 1) for _ in range(nb))
        gens = sorted(set(m + t for t in X) | B)
        print(m, *gens)
