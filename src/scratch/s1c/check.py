#!/usr/bin/python3
"""Independent cell-set audit of the completed corpus, with a 270s hard limit.

No import from the enumerator and no strict-corner formula is used.
Usage: /usr/bin/python3 src/scratch/s1c/check.py
"""
import gzip
import itertools
import json
import pathlib
import signal
import time

HERE = pathlib.Path(__file__).resolve().parent
PERMS = tuple(itertools.permutations(range(3)))


def parameters(d):
    lengths = [max(x[a] for x in d) + 1 for a in range(3)]
    h = tuple(sum((i, j, 0) in d for j in range(lengths[1])) for i in range(lengths[0]))
    f = tuple(sum((i, 0, k) in d for k in range(lengths[2])) for i in range(lengths[0]))
    g = tuple(sum((0, j, k) in d for k in range(lengths[2])) for j in range(lengths[1]))
    return h, f, g


def canon(d):
    return min(parameters({tuple(x[a] for a in p) for x in d}) for p in PERMS)


def main():
    signal.alarm(270)
    totals = [0, 0]
    summary = []
    started = time.monotonic()
    for result_path in sorted(HERE.glob('result_*.json')):
        result = json.loads(result_path.read_text())
        if not result['complete']:
            continue
        m = result['m']
        count = labelled = 0
        best = -10**9
        winners = set()
        seen = set()
        with gzip.open(HERE / ('corpus_%02d.jsonl.gz' % m), 'rt') as stream:
            for line in stream:
                hh, ff, gg, recorded_s = json.loads(line)
                h, f, g = map(tuple, (hh, ff, gg))
                assert all(a >= b for seq in (h, f, g) for a, b in zip(seq, seq[1:]))
                assert all(v > 0 for seq in (h, f, g) for v in seq)
                assert h[0] == len(g) and f[0] == g[0]
                assert min(h[1], f[1], g[1]) >= 2
                assert (h, f, g) not in seen
                seen.add((h, f, g))
                # Construct from three face predicates in the full bounding box.
                d = set()
                for i, j, k in itertools.product(range(len(h)), range(len(g)), range(f[0])):
                    if j < h[i] and k < f[i] and k < g[j]:
                        d.add((i, j, k))
                assert len(d) == m
                assert parameters(d) == (h, f, g)
                assert all(x in d for x in itertools.product((0, 1), repeat=3))
                assert all(tuple(x[b] - (b == a) for b in range(3)) in d
                           for x in d for a in range(3) if x[a] > 0)
                dims = (len(h), len(g), f[0])
                assert dims[0] <= dims[1] <= dims[2]
                assert m >= sum(dims) + 2
                # A cell is nonmaximal iff it is the predecessor of another cell.
                predecessors = set()
                for i, j, k in d:
                    predecessors.update(((i - 1, j, k), (i, j - 1, k), (i, j, k - 1)))
                maxima = d - predecessors
                s = sum(3 + sum(y) for y in maxima)
                assert s == recorded_s
                count += 1
                labelled += len(set(itertools.permutations(dims)))
                excess = s - 2 * m
                if excess >= best:
                    representative = canon(d)
                    if excess > best:
                        best = excess
                        winners.clear()
                    winners.add(representative)
        expected = {tuple(map(tuple, triple)) for triple in result['extrema']}
        assert (count, labelled, best, winners) == (
            result['sorted_axis_count'], result['labelled_count'], result['max_excess'], expected)
        summary.append(dict(m=m, checked=count, labelled=labelled, max_excess=best,
                            extremal_orbits=len(winners)))
        totals[0] += count
        totals[1] += labelled
    output = dict(complete=True, volumes=summary, sorted_axis_total=totals[0],
                  labelled_total=totals[1], seconds=round(time.monotonic()-started, 3))
    (HERE / 'audit.json').write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps(output), flush=True)
    signal.alarm(0)


if __name__ == '__main__':
    main()
