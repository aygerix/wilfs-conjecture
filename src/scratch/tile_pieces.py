# Contact-piece bound over the COMPLETE tile enumeration (non-two-face).  For an a-top t, t + e_a lies in D + lam;
# P_lam = {t + e_a - lam} subset B_a is a translate of a 2-D down-set, all its tops have column length lam_a, and
# Hp := sum_{a,lam} lam_a S(P_lam) <= H  (S(P) = sum_{v in P} ht_P(v)).  m = sum_{a,lam} lam_a |P_lam| / 3 ... per a.
# Reports min (Hp - (m-1)), max singleton weight sigma = sum_{|P|=1} lam_a.   usage: tile_pieces.py m...
import sys
from collections import defaultdict
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from tile_enum import enumerate_tiles
add = lambda x, i: x[:i] + (x[i]+1,) + x[i+1:]
def piece_data(m, r, D):
    cls = {sum(ri*xi for ri, xi in zip(r, x)) % m: x for x in D}
    out = []
    for a in range(3):
        groups = defaultdict(list)
        for z in D:
            za = add(z, a)
            if za in D: continue
            rep = cls[sum(ri*xi for ri, xi in zip(r, za)) % m]
            lam = tuple(za[i] - rep[i] for i in range(3))
            assert rep[a] == 0
            groups[lam].append(z)
        for lam, zs in groups.items():
            P = set(zs); ht = {}
            for v in sorted(P, key=lambda v: -sum(v)):
                ht[v] = max([ht[add(v, i)] + 1 for i in range(3) if i != a and add(v, i) in P], default=0)
            out.append((a, lam, len(P), sum(ht.values())))
    return out
if __name__ == '__main__':
    for m in map(int, sys.argv[1:]):
        worst = None; sigmax = None; fails = 0; n = 0
        for r, D, poly in enumerate_tiles(m):
            if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
            n += 1
            out = piece_data(m, r, set(D))
            Hp = sum(lam[a]*S for a, lam, k, S in out)
            sig = sum(lam[a] for a, lam, k, S in out if k == 1)
            fails += Hp < m - 1
            if worst is None or Hp - (m-1) < worst[0]: worst = (Hp - (m-1), r, sig, sum(1 for o in out if o[2] == 1))
            if sigmax is None or sig > sigmax[0]: sigmax = (sig, r, Hp - (m-1))
        print(f'm={m}: non-two-face {n}; Hp<m-1: {fails}; min Hp-(m-1) {worst}; max sigma {sigmax}', flush=True)
