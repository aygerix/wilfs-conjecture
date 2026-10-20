r"""LASTWIN / SUMH on Backelin's large-type family <s, s+3, s+3n+1, s+3n+2>, s = r(3n+2)+3 (lead, 2026-10-20),
and on random e = 4 semigroups with large m.  usage: backelin.py"""
import random
from layer import apery
def lw(gens):
    w = apery(gens)
    if w is None: return None
    m = min(gens); aps = set(w); srt = sorted(w)
    gen = [v for v in srt[1:] if not any((v - u) in aps for u in srt[1:] if u < v)]
    e = len(gen) + 1; c = max(w) - m + 1; q = -(-c // m); h = c - (q - 1) * m
    lv = [x // m for x in w]
    X = [r for r in range(h) if lv[r] <= q - 1]; D = [r for r in range(h) if lv[r] == q]
    Astar = {0} | {g % m for g in gen}
    XA = {(u + a) % m for u in X for a in Astar}
    typ = sum(1 for v in w if all((v + g) not in aps for g in gen))
    return dict(m=m, e=e, c=c, q=q, h=h, d=len(D), X=len(X), type=typ, LASTWIN=e * len(X) - h, SUMH=len(XA) - h)
if __name__ == "__main__":
 for n in (2, 3, 4):
   for r in (3 * n + 2, 3 * n + 3, 3 * n + 5):
    s = r * (3 * n + 2) + 3
    print("Backelin n", n, "r", r, lw([s, s + 3, s + 3 * n + 1, s + 3 * n + 2]))
 random.seed(7); worst = None
 for _ in range(3000):
    m = random.randint(20, 120); gens = [m] + random.sample(range(m + 1, 6 * m), 3)
    x = lw(gens)
    if x and x["q"] >= 3 and (worst is None or x["LASTWIN"] < worst["LASTWIN"]): worst = x
 print("random e<=4 worst LASTWIN", worst)
