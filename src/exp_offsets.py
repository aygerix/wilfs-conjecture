"""E9: offsets along shortest factorizations of top-layer elements.
For u in X_q with a shortest factorization n(u) (lex-min among shortest), a in [d], 1<=k<=n_a(u):
   off(u,a,k) = pi(u) - pi(u - k p_a),  pi(x) = ((x-c) mod m) + 1.
SC' : sum of all offsets <= m(m-1)/2   (SC' => TOP'' => Wilf; see NOTEBOOK)
Also test: all offsets positive; all offsets distinct."""
import sys
sys.path.insert(0, 'src')
from ns import all_by_genus

def shortest_facts(s):
    m = s.m
    Pp = [p for p in s.P if p != m]
    ap = sorted(s.apery()); apset = set(ap)
    best = {0: tuple([0] * len(Pp))}
    for w in ap[1:]:
        cands = []
        for a, p in enumerate(Pp):
            if (w - p) in apset:
                v = list(best[w - p]); v[a] += 1
                cands.append((sum(v), tuple(v)))
        best[w] = min(cands)[1]
    return Pp, best

def offsets(s):
    m, c = s.m, s.c
    pos = lambda x: ((x - c) % m) + 1
    Pp, best = shortest_facts(s)
    offs = []
    for u in s.apery():
        if u < c:
            continue
        n = best[u]
        for a, p in enumerate(Pp):
            for k in range(1, n[a] + 1):
                offs.append(pos(u) - pos(u - k * p))
    return offs

if __name__ == '__main__':
    G = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    n = fSC = fpos = fdist = 0
    ex = {'SC': [], 'pos': [], 'dist': []}
    for g, s in all_by_genus(G):
        if s.m <= 1:
            continue
        n += 1
        offs = offsets(s)
        if sum(offs) > s.m * (s.m - 1) // 2:
            fSC += 1
            if len(ex['SC']) < 5: ex['SC'].append((s.P, s.c, s.W, sorted(offs)))
        if any(o <= 0 for o in offs):
            fpos += 1
            if len(ex['pos']) < 3: ex['pos'].append((s.P, s.c, sorted(offs)))
        if len(set(offs)) < len(offs):
            fdist += 1
            if len(ex['dist']) < 3: ex['dist'].append((s.P, s.c, s.W, sorted(offs)))
    print(f"genus<={G}: {n}; SC' fails {fSC}; nonpositive offsets {fpos}; non-distinct {fdist}")
    for k, v in ex.items():
        for x in v: print(' ', k, x)
