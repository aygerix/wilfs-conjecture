"""Discriminating origin experiments. Run on fejer only, integer predicates.

Tests the target and deliberately stronger proposed payments, saves the least
witness for every refuted proposal. The target itself is never inferred from
sampling. Unit pools distinguish narrow/high/mixed origin geometries.
"""
import argparse
import json
import random
import sys
from collections import Counter
from itertools import combinations_with_replacement as cwr
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'd'))
from core import evaluate


def make(rng, m, U, prefer_bad):
    k = len(U)
    used = {0, *U}
    Q = set()
    pairs = list(cwr(range(k), 2))
    rng.shuffle(pairs)
    for z in pairs:
        r = sum(U[i] for i in z) % m
        if r not in used and rng.random() < .98:
            Q.add(z)
            used.add(r)
    T = set()
    cubes = list(cwr(range(k), 3))
    rng.shuffle(cubes)
    if prefer_bad:
        cubes.sort(key=lambda y: not (sum(U[i] for i in y) < 2*m and
                         all(sum(U[i] for i in y[:j]+y[j+1:]) > m for j in range(3))))
    for y in cubes:
        if not all(y[:j]+y[j+1:] in Q for j in range(3)):
            continue
        r = sum(U[i] for i in y) % m
        if r in used or rng.random() > .96:
            continue
        T.add(y)
        used.add(r)
    active = sorted({i for z in Q for i in z})
    if not active or not T:
        return None
    ren = {i:j for j,i in enumerate(active)}
    return ([U[i] for i in active], {tuple(ren[i] for i in z) for z in Q},
            {tuple(ren[i] for i in y) for y in T})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--trials', type=int, default=10000)
    ap.add_argument('--seed', type=int, default=2026101972)
    ap.add_argument('--output', default='origin_probe.json')
    args = ap.parse_args()
    rng = random.Random(args.seed)
    stats = Counter()
    failures = {}
    minima = {}
    for step in range(args.trials):
        m = rng.randint(12, 500)
        mode = step % 4
        if mode == 0:
            pool = range(m//2+1, (2*m-1)//3+1)
        elif mode == 1:
            pool = range(m//2+1, m)
        elif mode == 2:
            pool = range(1, m)
        else:
            pool = range(max(1, m//3), min(m, 5*m//6))
        k = min(rng.randint(3, 18), len(pool))
        if k < 2:
            continue
        U = sorted(rng.sample(pool, k))
        made = make(rng, m, U, step % 2 == 0)
        if made is None:
            continue
        U, Q, T = made
        ans = evaluate(m, U, Q, T, 0)
        ans.update(m=m, U=U, Q=sorted(Q), T=sorted(T))
        stats['cores'] += 1
        stats['t_ge_2'] += ans['t'] >= 2
        stats['bad_cores'] += ans['beta'] > 0
        stats['bad_cubes'] += ans['beta']
        high = all(2*u > m for u in U)
        if ans['S'] < 0:
            print('STOP MaxCL', json.dumps(ans), flush=True)
            raise SystemExit(2)
        tests = {'HC': ans['HC']}
        if high:
            stats['high'] += 1
            assert ans['gain'] == ans['t']-ans['beta']
            assert ans['Pplus'] == ans['p']
            # New count implications, not assertions of the target.
            half = (m-1)//2
            assert len(U)+ans['beta'] <= half
            assert 2*ans['HC'] >= m*(2*(ans['e']+len(U)-ans['q']+ans['p']) + (len(U)-2)*ans['s'])
            tests['high_count_payment'] = 2*(ans['e']+ans['p']-ans['beta']+ans['gain'])+len(U)*ans['s']
            tests['ignore_gain'] = ans['Lplus']+m*(ans['p']-ans['beta'])
            tests['twice_ignore_gain'] = ans['Lplus']+m*(ans['p']-2*ans['beta'])
        # Is every bad cubic all-high? This is intentionally false.
        b_low = 0
        for y in T:
            if sum(U[i] for i in y) < 2*m and all(sum(U[i] for i in y[:j]+y[j+1:]) > m for j in range(3)):
                b_low += any(2*U[i] <= m for i in y)
        stats['one_low_bad'] += b_low
        for name, slack in tests.items():
            if name not in minima or slack < minima[name]['slack']:
                minima[name] = dict(slack=slack, data=ans)
            if slack < 0:
                stats[name+'_failures'] += 1
                if name not in failures or (m, len(U), U) < (failures[name]['m'], failures[name]['k'], failures[name]['U']):
                    failures[name] = ans
        if step % 2000 == 0:
            print('progress', step, dict(stats), flush=True)
    out = dict(seed=args.seed, trials=args.trials, stats=stats, minima=minima, failures=failures)
    Path(args.output).write_text(json.dumps(out, indent=2))
    print('DONE', json.dumps(dict(seed=args.seed, trials=args.trials, stats=stats,
          minima={k:v['slack'] for k,v in minima.items()}, failures=failures)), flush=True)


if __name__ == '__main__':
    main()
