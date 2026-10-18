# INDEPENDENT re-verification of "HCR >= 1 on every e = 5 tile with 14 <= m <= M" (E153), sharing no code with the
# codex enumerator:
#   lattices: canonical residue vectors r (distinct, nonzero, gcd(m, r) = 1) mod units and permutations, generated here;
#   tiles: 4ti2 Markov basis of L_r -> lattice ideal -> gfan_bases (all marked reduced Groebner bases, positive orthant);
#          tile = standard monomials of the leading terms (asserted to be m monomials);
#   HCR computed exactly (Fractions) from the definition. Domain: e = 5 (every e_a in the tile).
import sys, os, subprocess, tempfile, itertools, json
from fractions import Fraction
from math import gcd
from multiprocessing import Pool
def canon(m):
    units = [u for u in range(1, m) if gcd(u, m) == 1]; seen = set(); out = []
    for r in itertools.combinations(range(1, m), 4):
        if gcd(gcd(gcd(gcd(m, r[0]), r[1]), r[2]), r[3]) != 1: continue
        c = min(tuple(sorted(u * x % m for x in r)) for u in units)
        if c not in seen: seen.add(c); out.append(c)
    return out
def markov(m, r):
    # lattice L = {x in Z^4 : x.r = 0 mod m} = projection of ker_Z [r_1 r_2 r_3 r_4 -m]; basis via 4ti2 zbasis (any r, no unit needed)
    with tempfile.TemporaryDirectory() as td:
        f = os.path.join(td, 'K'); open(f + '.mat', 'w').write("1 5\n" + ' '.join(map(str, list(r) + [-m])) + '\n')
        subprocess.run(['4ti2-zbasis', '-q', f], check=True, capture_output=True)
        B = [list(map(int, l.split()))[:4] for l in open(f + '.lat').read().split('\n')[1:] if l.strip()]
        assert len(B) == 4 and all(sum(a * b for a, b in zip(v, r)) % m == 0 for v in B)
        g = os.path.join(td, 'L'); open(g + '.lat', 'w').write("4 4\n" + '\n'.join(' '.join(map(str, b)) for b in B) + '\n')
        subprocess.run(['4ti2-markov', '-q', g], check=True, capture_output=True)
        return [list(map(int, l.split())) for l in open(g + '.mar').read().split('\n')[1:] if l.strip()]
V = 'abcd'
def parse_mono(t):
    e = [0] * 4
    for part in t.split('*'):
        part = part.strip()
        if not part or part.lstrip('-').isdigit(): continue
        v, _, k = part.partition('^'); e[V.index(v)] += int(k) if k else 1
    return tuple(e)
def tiles(m, r):
    mono = lambda u: '*'.join(f"{V[i]}^{x}" for i, x in enumerate(u) if x > 0) or '1'
    gens = [f"{mono([max(a, 0) for a in u])}-{mono([max(-a, 0) for a in u])}" for u in markov(m, r)]
    out = subprocess.run(['gfan_bases'], input=f"Q[a,b,c,d]{{{','.join(gens)}}}", capture_output=True, text=True, check=True).stdout
    body = out[out.index('{') + 1: out.rindex('}')]
    res, depth, cur = [], 0, ''
    for ch in body:
        if ch == '{':
            depth += 1
            if depth == 1: cur = ''; continue
        if ch == '}':
            depth -= 1
            if depth == 0: res.append(cur); continue
        if depth >= 1: cur += ch
    T = []
    for basis in res:
        lead = []
        for poly in basis.split(','):
            poly = poly.strip()
            if not poly: continue
            first = poly.replace('-', '+-').split('+'); first = [x for x in first if x.strip()][0]
            lead.append(parse_mono(first.lstrip('-')))
        D = [x for x in itertools.product(range(m), repeat=4) if sum(x) < m and not any(all(x[i] >= l[i] for i in range(4)) for l in lead)] \
            if False else std(lead, m)
        assert len(D) == m, (m, r, len(D))
        assert len({sum(a * b for a, b in zip(x, r)) % m for x in D}) == m
        T.append(D)
    return T
def std(lead, m):
    # standard monomials by BFS from 0 (down-set)
    S = {(0, 0, 0, 0)}; todo = [(0, 0, 0, 0)]
    while todo:
        x = todo.pop()
        for a in range(4):
            y = tuple(x[i] + (i == a) for i in range(4))
            if y in S: continue
            if any(all(y[i] >= l[i] for i in range(4)) for l in lead): continue
            S.add(y); todo.append(y)
            assert len(S) <= m
    return sorted(S)
def hcr(D):
    D = set(D); m = len(D); U = [tuple(int(i == a) for i in range(4)) for a in range(4)]
    add = lambda x, y: tuple(p + q for p, q in zip(x, y)); ht = {}
    for x in sorted(D, key=lambda x: -sum(x)):
        ht[x] = max([ht[add(x, u)] + 1 for u in U if add(x, u) in D], default=0)
    H = 0
    for x in D:
        for u in U:
            t = x
            while add(t, u) in D: t = add(t, u)
            H += ht[t]
    T = sorted((4 + sum(y) for y in D if ht[y] == 0), reverse=True)
    return Fraction(2 * ((m + 1) * H + sum(i * t for i, t in enumerate(T))), 3 * m * (m - 1))
def work(args):
    try: return work1(args)
    except Exception as ex: return args[1], -1, None, [('ERROR ' + repr(ex), [])]
def work1(args):
    m, r = args; best = None; fails = []; n = 0
    for D in tiles(m, r):
        if any(tuple(int(i == a) for i in range(4)) not in set(D) for a in range(4)): continue
        n += 1; h = hcr(D)
        if h < 1: fails.append((str(h), D))
        if best is None or h < best: best = h
    return r, n, best, fails
if __name__ == '__main__':
    lo, hi, P = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    for m in range(lo, hi + 1):
        C = canon(m); tot = 0; mn = None; F = []
        with Pool(P) as pool:
            for r, n, best, fails in pool.imap_unordered(work, [(m, r) for r in C], chunksize=4):
                tot += n; F += [(r, f) for f in fails]
                if best is not None and (mn is None or best < mn): mn = best
        errs = sum(1 for r, f in F if f[0].startswith('ERROR'))
        print(json.dumps({'errors': errs, 'm': m, 'lattices': len(C), 'e5_tiles': tot, 'min_hcr': str(mn), 'failures': [(list(r), h) for r, (h, D) in F]}), flush=True)
