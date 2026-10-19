# List the e = 5 tiles (E153 certificates) on which the crude bound CR fails, with their structure and the exact
# MaxCL slack (min over sigma) (lead, 2026-10-19).
# usage (in the certificate directory): python cr4_fail.py lo hi
import gzip, json, sys
if __name__ == "__main__":
    lo, hi = int(sys.argv[1]), int(sys.argv[2]); d = 4
    U = [tuple(int(i == a) for i in range(d)) for a in range(d)]
    for m in range(lo, hi + 1):
        with gzip.open(f'certificate_all_{m}.jsonl.gz', 'rt') as f:
            for line in f:
                rec = json.loads(line); r = rec['r']
                if len(set(r)) < 4 or 0 in r: continue
                for D in rec['tile_cells']:
                    S = set(map(tuple, D))
                    if any(u not in S for u in U): continue
                    up = lambda y, a: tuple(y[i] + U[a][i] for i in range(d))
                    A = [y for y in S if all(up(y, a) not in S for a in range(d))]; As = set(A)
                    w = sorted((sum(y) - 1 for y in A), reverse=True)
                    lhs = sum(wi * (m - 1 - i) for i, wi in enumerate(w)); nN = m - len(A)
                    rhs = (d + 1) * nN * (nN - 1) // 2
                    if lhs <= rhs: continue
                    dep = 0
                    for x in S:
                        for a in range(d):
                            t = x
                            while up(t, a) in S: t = up(t, a)
                            dep += t not in As
                    lev = {}
                    for x in S: lev[sum(x)] = lev.get(sum(x), 0) + 1
                    mlev = {}
                    for y in A: mlev[sum(y)] = mlev.get(sum(y), 0) + 1
                    phi = {x: sum(x[i] * r[i] for i in range(d)) % m for x in S}
                    mn = min((d + 1) * sum((phi[x] - sg) % m for x in S if x not in As)
                             - sum((sum(y) - 1) * ((phi[y] - sg) % m) for y in A) for sg in range(m))
                    ext = [max(x[a] for x in S) + 1 for a in range(d)]
                    print(f"m {m} r{tuple(r)} rhs/lhs {rhs/lhs:.4f} t {len(A)} Dep/m {dep/m:.3f} levels {dict(sorted(lev.items()))} "
                          f"maximal-by-level {dict(sorted(mlev.items()))} ext {ext} MaxCL-min-slack {mn} (norm {mn/((d+1)*m*(m-1)/2):.4f})", flush=True)
