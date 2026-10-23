"""Independent finite coin closure and explicit-column check of promoted scan records."""
import argparse
import json
from collections import defaultdict
from math import gcd
from functools import reduce
from itertools import combinations


def verify_exchanges(record):
    m = record['m']; A = tuple(record['old_atoms']); old = set(A)
    assert m >= 3 and A == tuple(sorted(old)) and 0 in old
    assert {(a+b) % m for a in old for b in old} == set(range(m))
    outside = sorted(set(range(m)) - old)
    histogram = [0] * (m+1); full = []; one = []; proposals = 0
    for removed in combinations(A[1:], 2):
        B = old - set(removed)
        for added in combinations(outside, 2):
            C = B | set(added)
            sums = {(a+b) % m for a in C for b in C}
            histogram[len(sums)] += 1; proposals += 1
            if len(sums) == m: full.append(sorted(C))
            elif len(sums) == m-1:
                assert {(s+a) % m for s in sums for a in C} == set(range(m))
                one.append(sorted(C))
    full.sort(); one.sort()
    orbit = {tuple(sorted((unit*(a-pivot)) % m for a in A))
             for unit in range(1, m) if gcd(unit, m) == 1 for pivot in A}
    assert record['proposals'] == proposals
    assert record['coverage_histogram'] == histogram
    assert record['full_cover_sets'] == full and record['one_hole_sets'] == one
    assert record['affine_orbit_size'] == len(orbit)
    assert record['full_covers_in_old_affine_orbit'] == sum(tuple(C) in orbit for C in full)
    return {'m': m, 'proposals': proposals, 'all_set_sums_independently_checked': True,
            'full_covers': len(full), 'one_hole_covers': len(one), 'affine_orbit_size': len(orbit)}


def verify(record):
    m = record['m']
    supplied = record['input_generators']
    w = record['w']
    assert m >= 2 and all(p > m for p in supplied)
    assert len(w) == m and w[0] == 0 and all(v >= 0 and v % m == s for s, v in enumerate(w))
    # Exact unbounded coin closure: binary copies of each coin realize all counts
    # needed below the finite bound. This algorithm does not use shortest paths.
    bound = max(max(w) + m, max(supplied, default=m))
    assert bound <= 5000000, 'finite-membership audit bound exceeded; do not accept unchecked'
    mask = (1 << (bound + 1)) - 1
    bits = 1
    minimal = []
    for p in sorted(set([m] + supplied)):
        if not (bits >> p) & 1:
            minimal.append(p)
        shift = p
        while shift <= bound:
            bits |= (bits << shift) & mask
            shift *= 2
    member = bits.to_bytes((bound + 8) // 8, 'little')
    contains = lambda x: bool(member[x // 8] & (1 << (x % 8)))
    actual_w = [next(v for v in range(s, bound + 1, m) if contains(v)) for s in range(m)]
    assert actual_w == w and minimal == record['generators']
    gaps = (~bits) & mask
    c = gaps.bit_length()
    g = gaps.bit_count()
    e = len(minimal)
    assert ((bits >> c) & ((1 << m) - 1)) == (1 << m) - 1
    assert (e, c, g, e * (c - g) - c) == tuple(record[k] for k in ('e', 'c', 'g', 'W'))
    for s in range(m):
        for p in supplied:
            assert w[(s + p) % m] <= w[s] + p
        if s:
            parent = record['predecessor_residue'][s]
            index = record['predecessor_generator_index'][s]
            assert 0 <= parent < m and 0 <= index < len(supplied)
            assert w[parent] < w[s] and w[parent] + supplied[index] == w[s]
    residues = sorted(p % m for p in minimal if p != m)
    d = len(residues)
    words = {0: (0,) * d}
    for s in sorted(range(1, m), key=lambda t: w[t]):
        choices = []
        for j, delta in enumerate(residues):
            parent = (s - delta) % m
            if w[parent] + w[delta] == w[s]:
                v = list(words[parent]); v[j] += 1; choices.append(tuple(v))
        words[s] = min(choices)
    assert record['primitive_residues'] == residues
    assert record['canonical_words'] == [x for s in range(m) for x in words[s]]
    height = max(map(sum, words.values()))
    inv = {word: s for s, word in words.items()}
    assert len(inv) == m
    top = w.index(max(w)); rho = (-c) % m
    gamma = [0] * m; nonmax = set(); inversions = 0
    for j in range(d):
        columns = defaultdict(list)
        for word in inv:
            columns[word[:j] + word[j + 1:]].append(word)
        for column in columns.values():
            end = max(column, key=lambda z: z[j])
            assert sorted(z[j] for z in column) == list(range(len(column)))
            gamma[inv[end]] += len(column)
            for word in column:
                child = list(word); child[j] += 1
                if tuple(child) in inv:
                    nonmax.add(inv[word])
                inversions += (inv[word] + rho) % m > (inv[end] + rho) % m
    dep = sum(gamma[s] for s in nonmax)
    kappa = sum(sum((word[j] * residues[j]) % m for j in range(d)) // m for word in inv)
    mu = [max(0, (c - v + m - 1) // m) for v in w]
    Q = dep + inversions - kappa
    R = sum(a * b for a, b in zip(gamma, mu)) - dep
    assert (gamma, dep, inversions, kappa, Q, R) == tuple(record[k] for k in ('gamma', 'Dep', 'N', 'kappa', 'Q', 'R'))
    assert R >= 0 and Q + R == record['W'] and mu == record['mu']
    correction = (e - 2) * m * (m - 1) // 2
    # Direct O(m^2) phase sums independently check the C++ O(m) sweep.
    phases = []
    for r in range(m):
        numerator = sum(gamma[s] * ((r - s) % m) for s in range(m)) - correction
        assert numerator % m == 0
        phases.append(dep + numerator // m)
    assert phases[top] == Q
    assert min(phases) == record['Qmin'] and phases.index(min(phases)) == record['minimum_top_phase']
    if record['kind'] == 'negative_Q_candidate': assert Q < 0
    if record['kind'] == 'negative_W_candidate': assert record['W'] < 0
    if record['kind'] == 'support_resistant_candidate':
        assert kappa > dep and height >= 3 and e >= 4 and 3 * e < m and c > 4 * m
    return {'kind': record['kind'], 'm': m, 'e': e, 'c': c, 'g': g, 'W': record['W'],
            'Q': Q, 'R': R, 'Qmin': min(phases), 'F': kappa - dep, 'height': height,
            'leave_one_out_gcds': [reduce(gcd, minimal[:j] + minimal[j + 1:]) for j in range(e)],
            'all_apery_entries_checked': m,
            'coin_membership_bound': bound, 'exact_predecessors': True,
            'canonical_columns': True, 'abstract_phases_are_not_realizations': True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('inputs', nargs='+')
    parser.add_argument('--output')
    args = parser.parse_args()
    results = []; coverage_results = []; neutral_origin = None; neutral_seeds = []; neutral_path = {}
    for path in args.inputs:
        with open(path) as source:
            for line in source:
                if line.strip().startswith('{'):
                    record = json.loads(line)
                    if record.get('kind') == 'two_atom_coverage':
                        coverage_results.append(verify_exchanges(record))
                    if 'w' in record:
                        results.append(verify(record))
                        kind = record.get('kind', '')
                        if kind == 'neutral_origin': neutral_origin = record
                        if kind.startswith('neutral_seed_'): neutral_seeds.append(record)
                        if kind.startswith('neutral_path_'): neutral_path[kind] = record
    assert results or coverage_results, 'no promoted records to verify'
    report = {'checked': len(results), 'results': results,
              'negative_Q': sum(r['Q'] < 0 for r in results),
              'negative_W': sum(r['W'] < 0 for r in results)}
    if coverage_results: report['independent_exchange_coverage'] = coverage_results
    if neutral_seeds:
        assert neutral_origin is not None
        for seed in neutral_seeds:
            assert seed['m'] == neutral_origin['m']
            assert all(seed[k] == neutral_origin[k] for k in ('e','primitive_residues','canonical_words','gamma'))
            assert seed['kappa']-seed['Dep'] == neutral_origin['kappa']-neutral_origin['Dep']
            assert len(seed['input_generators']) == len(neutral_origin['input_generators'])
            assert sum(a!=b for a,b in zip(seed['input_generators'],neutral_origin['input_generators'])) == 1
        report['exact_neutral_representatives_verified'] = len(neutral_seeds)
    if neutral_path:
        assert set(neutral_path) == {'neutral_path_origin','neutral_path_middle','neutral_path_exit'}
        start = neutral_path['neutral_path_origin']; middle = neutral_path['neutral_path_middle']; end = neutral_path['neutral_path_exit']
        assert all(start[k] == middle[k] for k in ('e','m','primitive_residues','canonical_words','gamma','Dep','kappa'))
        assert len(start['input_generators']) == len(middle['input_generators']) == len(end['input_generators'])
        assert sum(a!=b for a,b in zip(start['input_generators'],middle['input_generators'])) == 1
        assert sum(a!=b for a,b in zip(middle['input_generators'],end['input_generators'])) == 1
        improved = end['kappa']-end['Dep'] > start['kappa']-start['Dep']
        assert improved or end['W'] < 0 or end['Q'] < 0
        report['improving_neutral_path_independently_verified'] = improved
        report['negative_neutral_path_independently_verified'] = end['W'] < 0 or end['Q'] < 0
    if args.output:
        with open(args.output, 'w') as out: json.dump(report, out, indent=2)
    print(json.dumps(report))
