# Low-HCR 4-D tiles from the exact enumeration certificates (e = 5 domain only:
# distinct nonzero residues, every e_a in D). Prints structure of the lowest ones.
import gzip, json, sys
from fractions import Fraction
def analyse(D):
    D = set(map(tuple, D)); d = len(next(iter(D))); m = len(D)
    U = [tuple(int(i == a) for i in range(d)) for a in range(d)]
    add = lambda x, y: tuple(p + q for p, q in zip(x, y))
    ht = {}
    for x in sorted(D, key=lambda x: -sum(x)):
        ht[x] = max([ht[add(x, u)] + 1 for u in U if add(x, u) in D], default=0)
    Hn = 0; ST = 0
    for x in D:
        for a in range(d):
            t = x
            while add(t, U[a]) in D: t = add(t, U[a])
            Hn += ht[t]; ST += (ht[t] == 0)
    A = [y for y in D if ht[y] == 0]
    T = sorted((d + sum(y) for y in A), reverse=True)
    R = sum(i * t for i, t in enumerate(T))
    hcr = Fraction((m + 1) * Hn + R, (d - 1) * m * (m - 1) // 2 if (d-1)*m*(m-1) % 2 == 0 else 1)
    if (d - 1) * m * (m - 1) % 2: hcr = Fraction(2 * ((m + 1) * Hn + R), (d - 1) * m * (m - 1))
    two = [(a, b) for a in range(d) for b in range(a + 1, d) if add(U[a], U[b]) not in D]
    ext = [max(x[a] for x in D) + 1 for a in range(d)]
    lev = sorted((sum(y) for y in A), reverse=True)
    return dict(m=m, hcr=hcr, H=Hn, R=R, t=len(A), phi=Fraction(ST, d * m), two=two, ext=ext, lev=lev,
                maxht=max(ht.values()))
if __name__ == "__main__":
  lo, hi, thr, top = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4])
  for m in range(lo, hi + 1):
      rows = []
      with gzip.open(f'certificate_all_{m}.jsonl.gz', 'rt') as f:
          for line in f:
              rec = json.loads(line); r = rec['r']
              if len(set(r)) < 4 or 0 in r: continue
              for D in rec['tile_cells']:
                  S = set(map(tuple, D))
                  if any(tuple(int(i == a) for i in range(4)) not in S for a in range(4)): continue
                  z = analyse(D)
                  if z['hcr'] < thr: rows.append((z['hcr'], r, z))
      rows.sort(key=lambda w: w[0])
      print(f"m {m}: {len(rows)} e5-tiles with HCR < {thr}", flush=True)
      for h, r, z in rows[:top]:
          print(f"  {float(h):.4f} r{tuple(r)} two{z['two']} t{z['t']} phi {float(z['phi']):.3f} H/m {z['H']/m:.2f} "
                f"R/(1.5m^2) {z['R']/(1.5*m*m):.3f} ext{z['ext']} maxht {z['maxht']} lev{z['lev'][:12]}", flush=True)
