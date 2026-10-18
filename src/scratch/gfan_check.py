# Independent tile count via 4ti2 + gfan. For L = {x in Z^d : x.r = 0 mod m}: 4ti2 Markov basis of L -> binomial
# generators of the lattice ideal I_L -> gfan_bases (all reduced Groebner bases over the positive orthant).
# Each reduced Groebner basis <-> one tile (its standard monomials). Compare with the project's fan traversal.
import sys, os, subprocess, tempfile, re; sys.path.insert(0, 'src')
from math import gcd
def lattice_basis(m, r):
    d = len(r); i0 = next(i for i in range(d) if gcd(r[i], m) == 1)
    inv = pow(r[i0], -1, m); B = []
    for j in range(d):
        v = [0] * d
        if j == i0: v[j] = m
        else: v[j] = 1; v[i0] = (-r[j] * inv) % m
        B.append(v)
    return B
def gfan_count(m, r):
    d = len(r); V = 'xyzw'[:d]
    with tempfile.TemporaryDirectory() as td:
        f = os.path.join(td, 'L')
        B = lattice_basis(m, r)
        open(f + '.lat', 'w').write(f"{len(B)} {d}\n" + '\n'.join(' '.join(map(str, b)) for b in B) + '\n')
        subprocess.run(['4ti2-markov', '-q', f], check=True, capture_output=True)
        rows = [list(map(int, l.split())) for l in open(f + '.mar').read().split('\n')[1:] if l.strip()]
    mono = lambda u: '*'.join(f"{V[i]}^{e}" for i, e in enumerate(u) if e > 0) or '1'
    gens = [f"{mono([max(a, 0) for a in u])}-{mono([max(-a, 0) for a in u])}" for u in rows]
    inp = f"Q[{','.join(V)}]{{{','.join(gens)}}}"
    out = subprocess.run(['gfan_bases'], input=inp, capture_output=True, text=True, check=True).stdout
    body = out[out.index('{') + 1: out.rindex('}')]
    depth = 0; n = 0
    for ch in body:
        if ch == '{':
            if depth == 0: n += 1
            depth += 1
        elif ch == '}': depth -= 1
    return n, len(gens)
if __name__ == '__main__':
    from tile_enum import enumerate_lattice
    for spec in sys.argv[1:]:
        m, *r = map(int, spec.split(','))
        ours = len(enumerate_lattice(m, tuple(r))) if len(r) == 3 else None
        n, g = gfan_count(m, r)
        print(f"m={m} r={tuple(r)}: gfan bases {n} (Markov gens {g}); fan traversal {ours}", flush=True)
