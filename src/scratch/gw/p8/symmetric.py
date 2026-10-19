"""Exact polynomial certificates using symmetric rectangle packing.

Run only on fejer. Bernstein coefficients are exact rationals. Positivity
of all of them proves positivity on the entire displayed real interval.
"""
import argparse,json
from fractions import Fraction as F
from math import comb,lcm
from pathlib import Path
from certify import Poly,zero


def subst(p,q):
    ans=Poly.co(0)
    for (i,j),a in p.c.items():
        assert j==0
        ans+=a*q**i
    return ans


def bernstein(p,a,b):
    z=Poly({(1,0):1})
    q=subst(p,a+(b-a)*z)
    n=max(i for i,j in q.c)
    cs=[q.c.get((i,0),F(0)) for i in range(n+1)]
    return [sum(cs[j]*F(comb(i,j),comb(n,j)) for j in range(i+1)) for i in range(n+1)]


def cover(p,a,b,depth=0):
    bc=bernstein(p,a,b)
    if min(bc)>0:
        den=lcm(*(c.denominator for c in bc))
        return [dict(interval=[str(a),str(b)],bernstein=[str(c) for c in bc],
                     denominator=den,numerators=[int(c*den) for c in bc])]
    mid=(a+b)/2
    if p.ev(mid)<0:
        return [dict(counterexample=str(mid),value=str(p.ev(mid)))]
    if depth>=12:
        return [dict(unresolved=[str(a),str(b)])]
    return cover(p,a,mid,depth+1)+cover(p,mid,b,depth+1)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',default='results/symmetric.json')
    args=ap.parse_args()
    x=Poly({(1,0):1});y=(F(1,2)-x*x)/3;q=F(1,2)-y
    num=x**4-4*x*x*y+20*y*y
    a=F(14,25);b=F(31,50)
    rows=[]
    for h,mu in [(F(9,4),F(1,1000)),(F(11,5),F(1,2000)),
                 (F(13,6),F(1,10000)),(F(13,6),F(1,50000))]:
        gamma=1/(2*h*h)
        p=num-8*gamma*x*q*q-8*mu*x
        bc=bernstein(p,a,b)
        cc=cover(p,a,b)
        derivative=-b/2+gamma+(5/b-2*gamma)*(F(1,2)-b*b)/3
        # Unconstrained y-quadratic, after multiplying by 4x alpha.
        Q=b**3-gamma*b**4/2+gamma*b*b+4*gamma*mu*b-(5*gamma/2+10*mu)
        ok=all('bernstein' in c for c in cc) and derivative>0 and Q>0
        rows.append(dict(h=str(h),gamma=str(gamma),mu=str(mu),proved=ok,
                         bernstein=[str(c) for c in bc],
                         subdivision=cc,
                         small_derivative_lower=str(derivative),
                         large_Q_at_31_50=str(Q)))
    linear=[]
    for b0,mu in [(F(1,22),F(1,1000)),(F(1,21),F(1,50000))]:
        p=num-8*b0*x*q-8*mu*x
        bc=bernstein(p,a,b)
        cc=cover(p,a,b)
        derivative=-b/2+b0+(5/b)*(F(1,2)-b*b)/3
        high=b**3/10-b0/2-mu
        linear.append(dict(coefficient=str(b0),mu=str(mu),proved=all('bernstein' in c for c in cc) and derivative>0 and high>0,
                           bernstein=[str(c) for c in bc],small_derivative_lower=str(derivative),
                           subdivision=cc,high_margin=str(high)))
    # t<k/4 for h>=13/6, conditional on HC'<0. k=150+z.
    h=F(13,6);k=150+x
    tcap=(h*h/4-1)*k*k+((h*h-2*h*(3-h)-2)/4-h-3)*k-h-2
    assert all(a>0 for a in tcap.c.values())
    scoef=h*h*k/4-h-2
    assert all(a>0 for a in scoef.c.values())
    spcap=k*k-k-(k*k+3*k+2)/2-F(3,4)*k
    assert all(a>0 for a in spcap.c.values())
    # v is shifted by 2. This contains all dropped O(k^2) terms.
    error=F(11,4)*k*k-(F(5,2)*k*k+6*k+F(17,4))
    assert all(a>0 for a in error.c.values())
    assert 2/h**2+8/(150*h*h)<=F(1,2)
    # Symmetric rectangle + the m cap imply (v+2)^2+3e >= k^2/2.
    # Use v>=k/2-5/4 from the ordinary rectangle.
    assert 5*(F(150,2)-F(5,4))+4-F(5*150,4)>0
    # The two final branches of GENERAL-FEW21+240.
    assert F(11,4)+F(9,84)==F(240,84)
    assert F(282**2,50000)>F(1,21)
    kk=8+x
    sparse_defect=(F(25,252)*kk*kk-F(5,14)*kk-F(1,21))
    assert all(c>0 for c in sparse_defect.c.values())
    out=dict(status='EXACT BERNSTEIN CERTIFICATES',interval=[str(a),str(b)],
             quadratic=rows,linear=linear,
             tcap_coefficients={str(e):str(a) for e,a in tcap.c.items()},
             spikecap_coefficients={str(e):str(a) for e,a in spcap.c.items()},
             shift_error_coefficients={str(e):str(a) for e,a in error.c.items()})
    Path(args.output).parent.mkdir(parents=True,exist_ok=True)
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2),flush=True)


if __name__=='__main__':main()
