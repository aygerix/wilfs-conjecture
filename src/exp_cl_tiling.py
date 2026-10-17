"""E15: CL as a pure tiling statement.  D = any down-set in N^d with |D| = m, p in (Z/m)^d with
phi(n) = <n,p> mod m bijective on D (so D is a fundamental domain of the lattice ker phi).
T(n) = sum_{a : n+e_a not in D} (n_a+1).   CL-all:  for every s in Z/m,
   f(s) = sum_n T(n) * ((s - phi(n)) mod m)  >=  (d-1) m (m-1)/2.
No Apery minimality, no realizability.  Exhaustive over down-sets of size m (d = 2,3,4) and all p."""
import sys, itertools

def downsets(m, d):
    """all down-sets of N^d of size m (as frozensets of tuples), by adding addable cells (dedup)."""
    level = {frozenset([tuple([0]*d)])}
    for _ in range(m - 1):
        nxt = set()
        for D in level:
            for n in D:
                for a in range(d):
                    x = list(n); x[a] += 1; x = tuple(x)
                    if x in D: continue
                    if all(x[b] == 0 or tuple(x[:b] + (x[b]-1,) + x[b+1:]) in D for b in range(d)):
                        nxt.add(D | {x})
        level = nxt
    return level

def Tvals(D, d):
    T = {}
    for n in D:
        t = 0
        for a in range(d):
            x = list(n); x[a] += 1
            if tuple(x) not in D: t += n[a] + 1
        T[n] = t
    return T

def check(m, d, units_only=False):
    target = (d - 1) * m * (m - 1) // 2
    nD = nP = fails = 0; ex = []
    for D in downsets(m, d):
        Dl = sorted(D)
        if any(all(n[a] == 0 for n in Dl) for a in range(d)):  # degenerate direction: neutral, skip
            continue
        nD += 1
        T = Tvals(D, d)
        for p in itertools.product(range(m), repeat=d):
            res = [sum(x * y for x, y in zip(n, p)) % m for n in Dl]
            if len(set(res)) != m: continue
            nP += 1
            w = [0] * m
            for n, r in zip(Dl, res): w[r] = T[n]
            mn = min(sum(k * w[(s - k) % m] for k in range(m)) for s in range(m))
            if mn < target:
                fails += 1
                if len(ex) < 5: ex.append((sorted(D), p, mn, target))
    return nD, nP, fails, ex

if __name__ == '__main__':
    for d, ms in [(2, range(2, 16)), (3, range(2, 12)), (4, range(2, 9))]:
        for m in ms:
            nD, nP, f, ex = check(m, d)
            print(f'd={d} m={m}: downsets {nD}, (D,p) pairs {nP}, CL-all failures {f}', ex[:2] if ex else '', flush=True)
