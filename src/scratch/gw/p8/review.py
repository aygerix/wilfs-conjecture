"""Independent direct-form checks of the polynomial certificates (fejer).

The producer expands polynomials. This reviewer instead reconstructs each
Bernstein polynomial and checks n+1 exact rational values. Both sides have
degree <=n, so these values independently certify the identity.
"""
import json
from fractions import Fraction as F
from math import comb
from pathlib import Path


def f(x,y):return x**3/8-x*y/2+5*y*y/(2*x)


def main():
    d=json.loads(Path('results/symmetric.json').read_text())
    rows=d['quadratic']+d['linear'];intervals=points=0
    for row in rows:
        if not row['proved']:continue
        mu=F(row['mu'])
        for cc in row['subdivision']:
            a,b=map(F,cc['interval']);coef=list(map(F,cc['bernstein']));n=len(coef)-1
            assert all(c>0 for c in coef)
            for j in range(n+1):
                u=F(j,n);x=a+(b-a)*u;y=(F(1,2)-x*x)/3;z=F(1,2)-y
                rhs=sum(c*comb(n,i)*u**i*(1-u)**(n-i) for i,c in enumerate(coef))
                if 'h' in row:
                    h=F(row['h']);target=8*x*(f(x,y)-z*z/(2*h*h)-mu)
                else:target=8*x*(f(x,y)-F(row['coefficient'])*z-mu)
                assert rhs==target,(row,x,rhs,target)
                points+=1
            intervals+=1
    # The finite convex certificate must include each k of its asserted
    # closed range; this validates its table, not a substitute for the scan.
    dd=json.loads(Path('results/finite_shadow_sym_9_4.json').read_text())
    mm={r['k']:F(r['value']) for r in dd['minima_by_k']}
    assert set(mm)==set(range(150,3250))
    assert all(mm[k]>=0 for k in range(255,3250))
    ds=json.loads(Path('results/small_disjoint_sym254.json').read_text())
    assert ds['range']==[5,254] and ds['negative_intervals']==0
    assert ds['intervals']==585036 and F(ds['minimum']['value'])>0
    x=F(29,50);y=(F(1,2)-x*x)/3;z=F(1,2)-y
    obstruction=f(x,y)-z/20
    assert obstruction==F(-229819,261000000)
    k=127;s=111106;t=72676;p=8126;m=192038;w=3*t-p
    payment=s*comb(k,2)+(k+s+1)*comb(p,2)-w*(p-1)-m*t
    assert payment>0
    out=dict(status='INDEPENDENT EXACT REVIEW',bernstein_intervals=intervals,
             rational_identity_points=points,finite_tables_checked=True,
             relaxed_twenty_obstruction=str(obstruction),
             P7_sidon_all_phase_HC_lower_bound=payment)
    Path('results/review.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2),flush=True)


if __name__=='__main__':main()
