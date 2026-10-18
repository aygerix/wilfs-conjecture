# Print a 4-D tile (from the certificates) by level, with maximal cells, heights and its minimal non-elements q -> y(q).
import gzip, json, sys
from hcr4_low import analyse
m = int(sys.argv[1]); R = tuple(map(int, sys.argv[2].split(','))); thr = float(sys.argv[3])
U = [tuple(int(i == a) for i in range(4)) for a in range(4)]
add = lambda x, y: tuple(p + q for p, q in zip(x, y)); sub = lambda x, y: tuple(p - q for p, q in zip(x, y))
with gzip.open(f'certificate_all_{m}.jsonl.gz', 'rt') as f:
    for line in f:
        rec = json.loads(line)
        if tuple(rec['r']) != R: continue
        for Dl in rec['tile_cells']:
            D = set(map(tuple, Dl))
            if any(u not in D for u in U): continue
            z = analyse(Dl)
            if float(z['hcr']) > thr: continue
            print('HCR', float(z['hcr']), 'H', z['H'], 'R', z['R'], 't', z['t'], 'two', z['two'])
            ht = {}
            for x in sorted(D, key=lambda x: -sum(x)):
                ht[x] = max([ht[add(x, u)] + 1 for u in U if add(x, u) in D], default=0)
            for L in range(max(map(sum, D)) + 1):
                print(' level', L, ' '.join(f"{''.join(map(str, x))}{'*' if ht[x] == 0 else ht[x]}" for x in sorted(D) if sum(x) == L))
            res = {sum(a * b for a, b in zip(x, R)) % m: x for x in D}
            G = sorted({add(x, u) for x in D for u in U if add(x, u) not in D and all(sub(add(x, u), U[a]) in D for a in range(4) if add(x, u)[a] > 0)})
            print(' corners q->y(q):', ' '.join(f"{''.join(map(str, q))}->{''.join(map(str, res[sum(a * b for a, b in zip(q, R)) % m]))}" for q in G))
