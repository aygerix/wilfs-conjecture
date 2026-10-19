"""MaxCL profile of all 4-D tiles (e = 5 domain) by height, from the exact E153 certificates (lead, 2026-10-19).
For each tile: height H, Omega = sum_A (d+|y|), exact min_sigma MaxCL slack S, normalized ratio S/(Ctot (m-1)/2),
CR ratio = (d+1)M' / sum_i w_(i) (m-1-i) (weights sorted decreasingly against residues m-1, m-2, ...).
Height <= 3 tiles with d <= 5 are already PROVED (H3-D5); the question is whether height >= 4 tiles are easy
(Omega-crude: Omega <= (d+1)m/2, or CR >= 1) for large m.
usage: python maxcl4_profile.py mlo mhi certdir"""
import gzip, json, sys
from fractions import Fraction
mlo, mhi, cdir = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
for m in range(mlo, mhi+1):
    st = {}
    with gzip.open(f'{cdir}/certificate_all_{m}.jsonl.gz', 'rt') as f:
        for line in f:
            rec = json.loads(line); r = rec['r']
            if len(set(r)) < 4 or 0 in r: continue
            d = 4
            for Dl in rec['tile_cells']:
                D = set(map(tuple, Dl))
                if any(tuple(int(i == a) for i in range(d)) not in D for a in range(d)): continue
                up = lambda x, a: tuple(x[i]+(i == a) for i in range(d))
                A = [y for y in D if all(up(y, a) not in D for a in range(d))]
                H = max(sum(x) for x in D); key = min(H, 6)
                w = sorted((d+sum(y) for y in A), reverse=True); Om = sum(w)
                M1 = m*(m-1)//2
                lab = [sum(y[i]*r[i] for i in range(d)) % m for y in A]
                S = min((d+1)*M1-sum(wy*((l-sg) % m) for wy, l in zip([d+sum(y) for y in A], lab)) for sg in range(m))
                Ct = (d+1)*m-Om; ratio = S/(Ct*(m-1)/2) if Ct > 0 else 9
                crden = sum(wi*(m-1-i) for i, wi in enumerate(w)); cr = (d+1)*M1/crden if crden else 9
                s = st.setdefault(key, [0, 0, 9.0, 9.0, 0.0, 0])
                s[0] += 1; s[1] += S < 0; s[2] = min(s[2], ratio); s[3] = min(s[3], cr); s[4] = max(s[4], Om/m)
                s[5] += Om*2 > (d+1)*m      # Omega-crude fails
    for key in sorted(st):
        s = st[key]
        print("m=%d height%s%d tiles=%d MaxCL_neg=%d min_ratio=%.3f min_CR=%.3f max_Omega/m=%.3f Omega_crude_fail=%d" % (m, '>=' if key == 6 else '=', key, s[0], s[1], s[2], s[3], s[4], s[5]), flush=True)
