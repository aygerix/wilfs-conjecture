"""Among 4-D tiles (e=5 domain) with height >= 4 failing Omega-crude: how many are NO-WRAP (canonical lift x.r < m)
or WRAP-MAX (only maximal cells have x.r >= m)?  (lead 2026-10-19)  usage: python crude_fail_wrapclass.py mlo mhi certdir"""
import gzip, json, sys
mlo, mhi, cdir = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
for m in range(mlo, mhi+1):
    n = nw = wm = 0
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
                A = set(y for y in D if all(up(y, a) not in D for a in range(d)))
                if 2*sum(d+sum(y) for y in A) <= (d+1)*m: continue
                n += 1; v = {x: sum(x[i]*r[i] for i in range(d)) for x in D}
                nw += all(v[x] < m for x in D); wm += all(v[x] < m for x in D if x not in A)
    print("m=%d crude-failing height>=4 tiles %d: no-wrap %d, WRAP-MAX %d" % (m, n, nw, wm), flush=True)
