"""Crude (rearrangement) bound for IMaxCL on actual tiles (lead, 2026-10-19).
IMaxCL (equivalent to MaxCL): for the core C (cells of height >= 0 in the non-maximal unit directions, i.e. the tile
minus its maximal units = spikes), k = #core directions, s = m - |C| = #spikes,
      sum_{y in A(C)} (|y|-1) r(y)  <=  (k+1+s) * sum_{z in N(C)} r(z)        for every sigma.
Crude bound: give A the |A| largest residues (weights |y|-1 sorted decreasing) and N the |N| smallest:
      CR_s:  sum_i w_i (m-1-i)  <=  (k+1+s) * |N|(|N|-1)/2.
CR_s is shape-only and implies MaxCL for every sigma.  Report, per height, how many tiles CR_s proves, and the
structure (s, k, |C|) of those it does not.
usage: python crude_imaxcl.py seed trials mmin mmax"""
import sys, random
sys.path.insert(0, '/home/jmercedes/wilf/h3')
from maxcl_h3 import apery_tile, in_semigroup


def crude(m, gens):
    best = apery_tile(m, gens)
    if len(best) != m: return None
    d = len(gens); D = set(x for (w, x) in best.values())
    def add(x, a): return tuple(x[i]+(i == a) for i in range(d))
    A = [y for y in D if all(add(y, a) not in D for a in range(d))]
    spikes = [a for a in range(d) if tuple(int(i == a) for i in range(d)) in A]
    s = len(spikes); k = d-s
    Ac = [y for y in A if sum(y) >= 2 or (sum(y) == 1 and y.index(1) not in spikes)]
    Nc = [x for x in D if x not in set(A)]
    w = sorted((sum(y)-1 for y in Ac), reverse=True)
    lhs = sum(wi*(m-1-i) for i, wi in enumerate(w))
    rhs = (k+1+s)*len(Nc)*(len(Nc)-1)//2
    H = max(sum(x) for x in D)
    return H, d, k, s, m-s, len(Ac), len(Nc), lhs <= rhs, (rhs-lhs)


if __name__ == '__main__':
    seed, T, mmin, mmax = map(int, sys.argv[1:5]); rng = random.Random(seed)
    st = {}; ex = {}
    for t in range(T):
        m = rng.randint(mmin, mmax); fam = rng.random()
        if fam < 0.4:   # random generators in (m, 4m)
            gens = sorted(set(rng.randint(m+1, 4*m) for _ in range(rng.randint(2, 8))))
        elif fam < 0.7:  # core + spikes (as spike_maxcl_h)
            k = rng.randint(2, 4); Hc = 3
            core = [m+x for x in sorted(set(rng.randint(1, m-1) for _ in range(k)))]
            sums = {0}
            for _ in range(Hc): sums |= {a+x for a in sums for x in core}
            hit = {a % m for a in sums}
            gens = core+[rng.randint(2, 4)*m+res for res in range(1, m) if res not in hit]
        else:            # near-B_3: small offsets
            L = rng.randint(3, max(4, m//2))
            gens = [m+x for x in sorted(set(rng.randint(1, L) for _ in range(rng.randint(3, 7))))]
        gens = sorted(set(g for g in gens if g % m))
        gens = [g for g in gens if not in_semigroup(g, m, [h for h in gens if h != g])]
        if not gens or len(set(g % m for g in gens)) < len(gens): continue
        R = crude(m, gens)
        if R is None: continue
        H, d, k, s, C, a, n, ok, sl = R
        key = min(H, 6)
        z = st.setdefault(key, [0, 0]); z[0] += 1; z[1] += ok
        if not ok:
            e = ex.setdefault(key, [])
            if len(e) < 6: e.append((m, gens, 'k', k, 's', s, '|C|', C, '|A|', a, '|N|', n))
            ex.setdefault(('smax', key), [0])[0] = max(ex.get(('smax', key), [0])[0], s)
    for key in sorted(st):
        print("height", key, "tiles", st[key][0], "crude-proved", st[key][1], " max s among unproved:", ex.get(('smax', key), ['-'])[0])
        for e in ex.get(key, [])[:4]: print("   unproved:", e)
