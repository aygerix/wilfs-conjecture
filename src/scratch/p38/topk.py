# topk: the k residual S with least Delta3/h from Q5DUMP files (fields: m e D3 DEQ h hlo hhi ne2 ne3 dc n2eq n3eq cT r A...)
import sys
from fractions import Fraction as F
k = int(sys.argv[1])
for fn in sys.argv[2:]:
    R = []
    for f in fn.split('+'):
        for L in open(f):
            t = L.split()
            if t[0] != 'DUMP': continue
            v = list(map(int, t[1:15])); A = list(map(int, t[15:]))
            R.append((F(v[2], v[4]), v, A))
    R.sort(key=lambda x: x[0])
    for r, v, A in R[:k]:
        m = v[0]
        print(f"{float(r):.3f} D3={v[2]} h={v[4]} ne2={v[7]} ne3={v[8]} S={','.join(str(x) for x in [m] + [m + a for a in A])}")
