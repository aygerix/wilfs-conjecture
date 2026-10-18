# 4-D: gfan tile count per lattice vs the codex certificates (first K lattices of each m, plus named ones).
import sys, gzip, json, time; sys.path.insert(0, '/home/jmercedes/wilf/atop/fwx')
from gfan_check import gfan_count
for m in map(int, sys.argv[1].split(',')):
    K = int(sys.argv[2]); done = 0; bad = 0; t0 = time.time()
    with gzip.open(f'/home/jmercedes/wilf/tile4/src/scratch/tile4/certificate_all_{m}.jsonl.gz', 'rt') as f:
        for line in f:
            rec = json.loads(line); r = rec['r']
            if 0 in r or len(set(r)) < 4: continue
            n, g = gfan_count(m, r); ok = n == rec['tiles']; bad += not ok; done += 1
            if not ok: print('MISMATCH', m, r, 'gfan', n, 'cert', rec['tiles'], flush=True)
            if done >= K: break
    print(f"m={m}: {done} lattices compared, mismatches {bad}, {time.time() - t0:.1f}s", flush=True)
