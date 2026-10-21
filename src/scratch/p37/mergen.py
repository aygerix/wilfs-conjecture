# merge trunc3n part files: per-m totals, global minima (all, U != T), bucket minima by t = ceil(c/mu)
import re, sys, glob
files = sorted(glob.glob(sys.argv[1]))
perm = {}; gall = None; gne = None; bk = {}
rx = re.compile(r'(minratio|minratioNE)=([0-9.]+) \(m=(\d+) c=(\d+) l=(\d+)\) A=\{([0-9,]*)\}')
bx = re.compile(r'BUCKET t=(\d+)')
def better(cur, new): return new if cur is None or new[0] < cur[0] else cur
for f in files:
    for line in open(f):
        if line.startswith('R ') or line.startswith('N '):
            m = int(re.search(r' m=(\d+) ', line).group(1))
            cov, une, fa, fne = [int(re.search(k + r'=(\d+)', line).group(1)) for k in ('covering', 'UneT', 'FAILS', 'FAILSne')]
            p = perm.setdefault(m, [0, 0, 0, 0, None, None])
            p[0] += cov; p[1] += une; p[2] += fa; p[3] += fne
            for k, r, mm, c, l, A in rx.findall(line):
                rec = (float(r), int(mm), int(c), int(l), A)
                if k == 'minratio': p[4] = better(p[4], rec); gall = better(gall, rec)
                else: p[5] = better(p[5], rec); gne = better(gne, rec)
        elif line.startswith('BUCKET'):
            t = int(bx.search(line).group(1)); b = bk.setdefault(t, [None, None])
            for k, r, mm, c, l, A in re.findall(r'(all|NE)=([0-9.]+) \(m=(\d+) c=(\d+) l=(\d+)\) A=\{([0-9,]*)\}', line):
                rec = (float(r), int(mm), int(c), int(l), A)
                if k == 'all': b[0] = better(b[0], rec)
                else: b[1] = better(b[1], rec)
tot = [sum(p[i] for p in perm.values()) for i in range(4)]
print('files', len(files), 'm range', min(perm), max(perm), 'covering', tot[0], 'UneT', tot[1], 'FAILS', tot[2], 'FAILSne', tot[3])
print('GLOBAL all', gall); print('GLOBAL NE ', gne)
if len(sys.argv) > 2:
    for m in sorted(perm): p = perm[m]; print('m', m, 'cov', p[0], 'une', p[1], 'all', p[4], 'NE', p[5])
for t in sorted(bk):
    if t <= 12 or t % 10 == 0: print('t', t, 'all', bk[t][0], 'NE', bk[t][1])
