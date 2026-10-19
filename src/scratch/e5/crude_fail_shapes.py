"""Shapes of 4-D tiles (e = 5 domain, height >= 4) failing Omega-crude (Omega > (d+1)m/2): level profile of maximal
cells, column-length mass, min MaxCL ratio (lead, 2026-10-19).  usage: python crude_fail_shapes.py m certdir nshow"""
import gzip, json, sys
from collections import Counter
m, cdir, nshow = int(sys.argv[1]), sys.argv[2], int(sys.argv[3]); shown = 0; prof = Counter()
with gzip.open(f'{cdir}/certificate_all_{m}.jsonl.gz', 'rt') as f:
    for line in f:
        rec = json.loads(line); r = rec['r']
        if len(set(r)) < 4 or 0 in r: continue
        d = 4
        for Dl in rec['tile_cells']:
            D = set(map(tuple, Dl))
            if any(tuple(int(i == a) for i in range(d)) not in D for a in range(d)): continue
            if max(sum(x) for x in D) < 4: continue
            up = lambda x, a: tuple(x[i]+(i == a) for i in range(d))
            A = [y for y in D if all(up(y, a) not in D for a in range(d))]
            Om = sum(d+sum(y) for y in A)
            if 2*Om <= (d+1)*m: continue
            levA = Counter(sum(y) for y in A); levD = Counter(sum(x) for x in D)
            high = sorted([y for y in D if sum(y) >= 4], key=sum)
            prof[(tuple(sorted(levA.items())), len(high))] += 1
            if shown < nshow:
                M1 = m*(m-1)//2; lab = {y: sum(y[i]*r[i] for i in range(d)) % m for y in A}
                S = min((d+1)*M1-sum((d+sum(y))*((lab[y]-sg) % m) for y in A) for sg in range(m))
                print("r", r, "Omega/m %.3f" % (Om/m), "levels(D)", sorted(levD.items()), "levels(A)", sorted(levA.items()), "cells>=4:", high, "minS", S)
                shown += 1
print("profiles (levels of A, #cells of degree >= 4): count")
for k, v in prof.most_common(12): print("  ", k, v)
