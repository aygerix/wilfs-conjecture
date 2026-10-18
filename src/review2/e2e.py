# End-to-end referee test on e = 4 semigroups: tile, CH', height criterion, two-face bounds, cylinder class, lemmas.
import sys, random, time
from math import comb, gcd
from functools import reduce
from collections import Counter, defaultdict
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from tk import *

EXC = {8, 15, 16, 17, 19, 20, 23}

def sieve_check(m, gens, inv):
    # second, independent computation of c, g by membership sieve
    B = inv['M'] + m + 5
    inS = [False]*(B + 1); inS[0] = True
    for n in range(1, B + 1):
        inS[n] = any(n >= q and inS[n - q] for q in [m] + list(gens))
    F = max(n for n in range(B + 1) if not inS[n]) if not all(inS) else -1
    g = sum(1 for n in range(B + 1) if not inS[n])
    assert F + 1 == inv['c'], (m, gens, F, inv['c'])
    assert g == inv['g'], (m, gens, g, inv['g'])
    ell = sum(1 for n in range(F + 1) if inS[n])
    assert ell == inv['ell']

def twoface_checks(m, P, D, wmap, inv, a, b, stats):
    c3 = 3 - a - b
    pa, pb, pc = P[a], P[b], P[c3]
    M, W, cc = inv['M'], inv['W'], inv['c']
    L3 = sum(1 for x in D if x[a] == 0 and x[b] == 0)
    N1 = [x for x in D if x[a] >= 1]; N2 = [x for x in D if x[b] >= 1]
    assert all(x[b] == 0 for x in N1) and all(x[a] == 0 for x in N2)
    assert len(N1) + len(N2) == m - L3
    X = [x for x in D if wmap[x] >= cc]
    assert all(wmap[x] < cc + m for x in X)
    T = tops(D)
    # runs: a-rows of F1 (cells with x_b = 0), b-rows of F2 (x_a = 0), all c-columns
    Def2D = 0; Def2Dp = 0
    for x in D:
        # a-row run containing x, only for x_b == 0
        if x[b] == 0: Def2D += M - wmap[T[x][a]]; Def2Dp += M - wmap[T[x][a]]
        if x[a] == 0: Def2D += M - wmap[T[x][b]]; Def2Dp += M - wmap[T[x][b]]
        Def2D += M - wmap[T[x][c3]]
        if not (x[a] == 0 and x[b] == 0): Def2Dp += M - wmap[T[x][c3]]
    lhs = 3*m*W + 3*m*(m - 1)
    assert lhs == (m - 4*L3)*M + 4*Def2D + 2*pc*L3*(L3 - 1), 'two-face identity'
    assert lhs == m*M + 4*Def2Dp - 2*pc*L3*(L3 - 1), 'two-face identity 2'
    axtop = tuple((L3 - 1) if i == c3 else 0 for i in range(3))
    x1 = sum(1 for x in X if x[a] >= 1); x2 = sum(1 for x in X if x[b] >= 1); xax = int(axtop in X)
    tau = x1 + x2 + xax; assert tau == len(X)
    # F1
    assert x1*(x1 + 1)//2 <= len(N1) and x2*(x2 + 1)//2 <= len(N2), 'F1'
    assert x1 <= L3 - xax and x2 <= L3 - xax, 'F1b'
    # F3
    assert sum(sum(u) + 2 for u in X if u[a] >= 1) <= len(N1) + 2*x1 + comb(x1, 2), 'F3'
    assert sum(sum(u) + 2 for u in X if u[b] >= 1) <= len(N2) + 2*x2 + comb(x2, 2), 'F3'
    # F5
    P2 = sum(1 for u, v in combinations(X, 2) if sum(1 for i in range(3) if u[i] != v[i]) == 2)
    assert P2 <= comb(x1, 2) + comb(x2, 2) + xax*(x1 + x2) + min(x1, x2), 'F5'
    # Def2D lower bounds
    bA = m*(m + 2*L3 - 2*(x1 + x2) - comb(x1, 2) - comb(x2, 2) - xax*(L3 + 2)) + 3*comb(tau, 2)
    assert Def2D >= bA, 'Def2D bound'
    bB = m*(m + L3 - 2*(x1 + x2) - comb(x1, 2) - comb(x2, 2) - 2*xax) + 2*comb(tau, 2)
    assert Def2Dp >= bB, "Def2D' bound"
    covered = []
    if cc <= 3*m: covered.append('Eliahou')
    if m <= 17: covered.append('BGOW')
    if cc > 3*m and 4*L3 <= m:
        rhs = 4*m*(m - 4*L3) + 2*(m + 1)*L3*(L3 - 1) + 4*Def2D
        assert lhs >= rhs, "A'"
        if 4*m*(m - 4*L3) + 2*(m + 1)*L3*(L3 - 1) + 4*max(0, bA) >= 3*m*(m - 1): covered.append("A'")
    if m >= 2*L3:
        rhs = (L3 - 1)*(m + 1)*(m - 2*L3) + 4*Def2Dp
        assert lhs >= rhs, "B''"
        if (L3 - 1)*(m + 1)*(m - 2*L3) + 4*max(0, bB) >= 3*m*(m - 1): covered.append("B''")
    if m + 1 >= 2*tau + P2: covered.append('C')
    H1 = len({x[c3] for x in D if x[a] == 1 and x[b] == 0})
    H2 = len({x[c3] for x in D if x[b] == 1 and x[a] == 0})
    h = lambda H: (L3 - H)*(L3 - H - 1) if H < L3 else 0
    G = m*(L3 - 1) - 2*L3*(L3 - 1) + 2*h(H1) + 2*h(H2)
    assert lhs >= pc*G, 'D'
    assert 1 <= H1 and 1 <= H2 and H1 + H2 <= m - L3
    if G >= 0 and (m + 1)*G >= 3*m*(m - 1): covered.append('D')
    if not covered:
        stats['twoface_uncovered'].append((m, P, L3, x1, x2, xax, H1, H2, cc))
    stats['tf_cov'][tuple(sorted(set(covered)))] += 1

def analyse(m, gens, stats, sieve=False, verbose=False):
    inv = invariants(m, gens)
    if inv['e'] != 4: return None
    P = inv['P']
    if sieve: sieve_check(m, gens, inv)
    cls2x, cls2w = grlex_tile(m, P)
    D = set(cls2x.values()); wmap = {cls2x[g]: cls2w[g] for g in cls2x}
    assert len(D) == m and is_downset(D)
    assert all(e in D for e in E)
    assert sorted(wmap.values()) == sorted(inv['Ap'])
    for x in D: assert wmap[x] == sum(P[a]*x[a] for a in range(3))
    M = inv['M']; W = inv['W']
    Dall = def_all(D, wmap, M)
    assert Dall == m*W + m*(m - 1), 'CH prime'
    H = H_of(D)
    assert (m + 1)*H <= m*W + m*(m - 1), 'height criterion'
    stats['n'] += 1
    if Dall < (m + 1)*H + 3*m: stats['heightH_docstring_+3m_false'] += 1
    delta = H - (m - 1)
    tf = two_face_pairs(D)
    if tf:
        stats['twoface'] += 1
        for (a, b) in tf: twoface_checks(m, P, D, wmap, inv, a, b, stats)
        kind = classify(D)[0]
        stats['twoface_class'][kind] += 1
        return ('2f', delta)
    kind, q, full = classify(D)
    stats['class'][kind] += 1
    assert kind in ('C', 'cone'), (m, P, kind, full)
    t, Tri, qU, qO = counts(D)
    C = sum(face_corners(D, c) for c in range(3))
    assert delta >= m + 1 - (2*t + 2*Tri + qU + qO), 'CHT'
    assert C*C - 3*C + 6 <= 6*m, 'Lemma B'
    if kind == 'C':
        assert t <= C - 2, 'Lemma T'
        assert 2*Tri <= t - 1, 'TF'
        assert qU <= t - 1, 'F'
        assert qO <= t - 1, 'QF'
        assert delta >= m + 14 - 5*C, 'C-HT'
    else:
        assert t <= C, "T'"
        stats['cone_q'][q] += 1
    if delta < 0:
        stats['ht_fail'].append((m, P, delta, kind))
    if verbose: print(m, P, delta, kind)
    return (kind, delta)

def rand_gens(m, rng, mode):
    while True:
        if mode == 'small': K = 3
        elif mode == 'mid': K = rng.choice([4, 6, 10])
        else: K = rng.choice([20, 100, 1000, 10000])
        g = sorted(rng.sample(range(m + 1, K*m), 3)) if K*m - m - 1 >= 3 else None
        if g is None: continue
        if mode == 'skew':  # one small, others huge, to push weights toward the simplex boundary
            g = sorted([m + rng.randint(1, m), rng.randint(m + 1, K*m), rng.randint(m + 1, K*m)])
        if len(set(x % m for x in g)) < 3 or any(x % m == 0 for x in g): continue
        if reduce(gcd, [m] + g) != 1: continue
        return g

def new_stats():
    return dict(n=0, twoface=0, class_=None, ht_fail=[], twoface_uncovered=[],
                tf_cov=Counter(), twoface_class=Counter(), cone_q=Counter(), **{'class': Counter()},
                **{'heightH_docstring_+3m_false': 0})

if __name__ == '__main__':
    seed = int(sys.argv[1]); N = int(sys.argv[2]); m0, m1 = int(sys.argv[3]), int(sys.argv[4])
    modes = sys.argv[5].split(',')
    rng = random.Random(seed); stats = new_stats(); t0 = time.time()
    permd = defaultdict(Counter)
    for i in range(N):
        m = rng.randint(m0, m1); mode = rng.choice(modes)
        g = rand_gens(m, rng, mode)
        r = analyse(m, g, stats, sieve=(m <= 25 and max(g) < 40*m))
        if r: permd[m][r[0]] += 1
    print('seed', seed, 'N', N, 'm', m0, m1, 'modes', modes, f'{time.time()-t0:.0f}s')
    for k, v in stats.items():
        if k == 'class_': continue
        if isinstance(v, list): print(k, len(v), v[:30])
        else: print(k, v)
