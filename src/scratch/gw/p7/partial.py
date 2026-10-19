"""Small injective WRAP-MAX downsets; exact falsification of injectivity-only H1'.

Enumerates every residue vector with distinct nonzero entries, every downset
with those units and injective labels, and no extensions of wrapped cells.
Coordinate permutation is removed by increasing P.  Empty directions omitted.
Usage: python partial.py --mmax 9 --dmax 3
"""
import argparse
import itertools
import json
from core import add, sub, evaluate, brief


def downsets(m, P):
    d = len(P)
    zero = (0,)*d
    units = {add(zero, a) for a in range(d)}
    root = frozenset({zero}|units)
    seen = {root}
    stack = [root]
    while stack:
        D = stack.pop()
        yield D
        labels = {sum(x[i]*P[i] for i in range(d)) % m for x in D}
        cand = {add(x, a) for x in D for a in range(d)}-D
        for y in cand:
            if not all(sub(y, a) in D for a in range(d) if y[a]):
                continue
            vy = sum(y[i]*P[i] for i in range(d))
            if vy % m in labels:
                continue
            if any(sum(sub(y, a)[i]*P[i] for i in range(d)) >= m for a in range(d) if y[a]):
                continue
            DD = frozenset(set(D)|{y})
            if DD not in seen:
                seen.add(DD)
                stack.append(DD)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mmax', type=int, default=9)
    ap.add_argument('--dmax', type=int, default=3)
    args = ap.parse_args()
    stats = dict(downsets=0, partial=0, complete=0, partial_fail=0, complete_fail=0)
    first = None
    first_degree = None
    for m in range(2, args.mmax+1):
        for d in range(1, min(args.dmax, m-1)+1):
            for P in itertools.combinations(range(1, m), d):
                for D in downsets(m, P):
                    z = evaluate(m, P, D)
                    stats['downsets'] += 1
                    stats['complete' if z['complete'] else 'partial'] += 1
                    bad = [r for r in z['rows'] if r['shadow'] < 0]
                    if bad:
                        stats['complete_fail' if z['complete'] else 'partial_fail'] += 1
                        key = (m, len(D), d, P, tuple(z['D']), bad[0]['theta'])
                        if first is None or key < first[0]:
                            first = (key, dict(**brief(z), row=bad[0]))
                    bad = [r for r in z['rows'] if r['exit_slack'] < 0]
                    if bad and first_degree is None:
                        first_degree = dict(**brief(z), row=bad[0])
        print(json.dumps(dict(m_done=m, stats=stats)), flush=True)
    print(json.dumps(dict(stats=stats, first_shadow_failure=first[1] if first else None,
                          first_degree_failure=first_degree), sort_keys=True))


if __name__ == '__main__':
    main()
