import sys
from fractions import Fraction as F
for fn in sys.argv[1:]:
    R = []
    for L in open(fn):
        t = L.split()
        if t[0] != 'DUMP': print(L); continue
        v = list(map(int, t[1:15])); A = list(map(int, t[15:]))
        m,e,D3,DEQ,h,hlo,hhi,ne2,ne3,dc,n2eq,n3eq,cT,r = v
        R.append(dict(m=m,e=e,D3=D3,DEQ=DEQ,h=h,hlo=hlo,hhi=hhi,ne2=ne2,ne3=ne3,dc=dc,n2eq=n2eq,n3eq=n3eq,cT=cT,r=r,A=A))
    e = R[0]['e']; d = e - 1
    print(fn, 'n =', len(R), 'e =', e)
    # best alpha with D3 >= alpha*hlo + 1*hhi
    rat = [F(x['D3'] - x['hhi'], x['hlo']) for x in R if x['hlo'] > 0]
    print(' min (D3-hhi)/hlo =', float(min(rat)), ' min D3/h =', float(min(F(x['D3'], x['h']) for x in R)))
    print(' min D3/hlo (hlo>0) =', float(min(F(x['D3'], x['hlo']) for x in R if x['hlo'])), ' hlo=0 count', sum(1 for x in R if x['hlo']==0))
    print(' min DEQ/h =', float(min(F(x['DEQ'], x['h']) for x in R)), ' min (DEQ+d*dc)/h', float(min(F(x['DEQ']+d*x['dc'], x['h']) for x in R)))
    # slack of PAY2 = DEQ + d dc - 3 ne2 - (e+3) ne3
    p2 = [x['DEQ'] + d*x['dc'] - 3*x['ne2'] - (e+3)*x['ne3'] for x in R]
    assert all(p == x['D3'] + d*x['dc'] - e*x['h'] for p, x in zip(p2, R))
    # extremal for A1 slack
    R.sort(key=lambda x: x['D3'] - e*x['hlo'] - x['hhi'])
    for x in R[:4]:
        print('  A1slack', x['D3'] - e*x['hlo'] - x['hhi'], {k: x[k] for k in ('m','D3','DEQ','h','hlo','hhi','ne2','ne3','dc','n2eq','n3eq','cT','r')}, 'A', x['A'])
    # per hlo: min D3
    by = {}
    for x in R: by.setdefault((x['hlo'], x['hhi']), []).append(x['D3'])
    print(' (hlo,hhi): count, min D3 :', ' '.join(f"{k}:{len(v)},{min(v)}" for k, v in sorted(by.items())))
