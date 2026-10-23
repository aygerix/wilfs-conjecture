"""Independent finite coin closure and explicit-column check of promoted scan records."""
import argparse
import json
from collections import defaultdict


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
    return {'kind': record['kind'], 'm': m, 'e': e, 'c': c, 'g': g, 'W': record['W'],
            'Q': Q, 'R': R, 'Qmin': min(phases), 'all_apery_entries_checked': m,
            'coin_membership_bound': bound, 'exact_predecessors': True,
            'canonical_columns': True, 'abstract_phases_are_not_realizations': True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('inputs', nargs='+')
    parser.add_argument('--output')
    args = parser.parse_args()
    results = []
    for path in args.inputs:
        with open(path) as source:
            for line in source:
                if line.strip().startswith('{'):
                    record = json.loads(line)
                    if 'w' in record:
                        results.append(verify(record))
    assert results, 'no promoted records to verify'
    report = {'checked': len(results), 'results': results,
              'negative_Q': sum(r['Q'] < 0 for r in results),
              'negative_W': sum(r['W'] < 0 for r in results)}
    if args.output:
        with open(args.output, 'w') as out: json.dump(report, out, indent=2)
    print(json.dumps(report))
