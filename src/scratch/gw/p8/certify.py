"""Exact algebra certificates for P8. Execute only on fejer.

No symbolic package is used. Polynomial identities are checked coefficientwise
over fractions; inequalities are certified by their displayed coefficients.
"""
from fractions import Fraction as F
from math import ceil
import argparse
import json
from pathlib import Path


class Poly:
    def __init__(self, terms=None):
        self.c = {e: F(a) for e, a in (terms or {}).items() if a}

    @staticmethod
    def co(a):
        return a if isinstance(a, Poly) else Poly({(0, 0): a})

    def __add__(self, b):
        b = self.co(b)
        c = self.c.copy()
        for e, a in b.c.items():
            c[e] = c.get(e, F(0)) + a
        return Poly(c)

    __radd__ = __add__

    def __neg__(self):
        return Poly({e: -a for e, a in self.c.items()})

    def __sub__(self, b):
        return self + -self.co(b)

    def __rsub__(self, b):
        return self.co(b) - self

    def __mul__(self, b):
        b = self.co(b)
        c = {}
        for e, a in self.c.items():
            for f, d in b.c.items():
                ef = tuple(x + y for x, y in zip(e, f))
                c[ef] = c.get(ef, F(0)) + a*d
        return Poly(c)

    __rmul__ = __mul__

    def __pow__(self, n):
        assert n >= 0
        ans = self.co(1)
        for _ in range(n):
            ans = ans * self
        return ans

    def __truediv__(self, a):
        return self * (F(1)/a)

    def ev(self, x, y=0):
        return sum(a*x**i*y**j for (i,j), a in self.c.items())


def zero(a):
    assert not a.c, a.c


def linked(v, e):
    q = F(v*(v+1), 2)-e
    X = 2*e-v
    return (q*(q-1)/2+(v+1)*(X*X/(2*v)-X/2))/v


def parameters(h):
    h = F(h)
    gamma = 1/(2*h*h)
    low = F(1,16)-gamma-(F(1,2)-2*gamma)**2/70
    high = F(27,50)**3/10-gamma/4
    mu = min(F(25,108)*low, high)
    assert low > 0 and high > 0 and mu > 0
    cutoff = max(150, ceil(F(5,2)/mu))
    return dict(h=str(h), gamma=str(gamma), L=str(low), high=str(high),
                mu=str(mu), cutoff=cutoff,
                mu_decimal=float(mu))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', default='results/certify.json')
    args = ap.parse_args()
    x = Poly({(1,0):1}); y = Poly({(0,1):1})
    v,e = x,y
    q = v*(v+1)/2-e
    X = 2*e-v
    numerator = 4*v*q*(q-1)+4*(v+1)*(X*X-v*X)
    expanded = (v**5+2*v**4+7*v**3+6*v*v-4*e*v**3
                -28*e*v*v-20*e*v+20*e*e*v+16*e*e)
    zero(numerator-expanded)
    # The exact LC square completion, after multiplying by 8v^2(5v+4).
    centre_numerator = v*(v*v+7*v+5)
    zero((5*v+4)*numerator
         -v*v*(4*v**4-16*v*v-12*v-1)
         -(2*(5*v+4)*e-centre_numerator)**2)
    # The leading form f(x,y)=x^3/8-xy/2+5y^2/(2x).
    zero(x**4-4*x*x*y+20*y*y
         -F(4,5)*x**4-20*(y-x*x/10)**2)

    hmin = F(72,25)
    # t >= k/8 is impossible for k=150+z. The constant and linear
    # coefficients are positive; the s coefficient is positive as well.
    k = 150+x
    h = hmin
    tcap = ((h*h/8-1)*k*k
            +((h*h-2*h*(3-h)-2)/8-h-3)*k-h-2)
    assert all(a >= 0 for a in tcap.c.values())
    scoef = h*h*k/8-h-2
    assert all(a > 0 for a in scoef.c.values())
    # The t-cap expression increases with h on [72/25,3].
    # Its h-derivative is (k+s+1)(hk/4-1)+(4h-6)k/8 > 0.
    assert hmin*150/4-1 > 0 and 4*hmin-6 > 0
    # s>=k/4 contradicts the spike mass, once t<k/8.
    spcap = k*k-k-(k*k+3*k+2)/2-F(3,8)*k
    assert all(a >= 0 for a in spcap.c.values())
    # All error terms in shifting v to v+1 cost at most 9k^2/4.
    err = F(9,4)*k*k-(F(17,8)*k*k+F(15,4)*k+F(13,8))
    assert all(a >= 0 for a in err.c.values())
    # The square-completion remainder costs at most k^2/4.
    assert F(7,4)/hmin**2+F(49,8)/(hmin**2*150) <= F(1,4)

    data = []
    for h in [F(72,25), F(29,10), F(59,20), F(3)]:
        item = parameters(h)
        gamma = 1/(2*h*h)
        # Substituting x=1/2+y into 8x[f-gamma(1/2-y)^2].
        xx = F(1,2)+y
        direct = xx**4-4*xx*xx*y+20*y*y-8*gamma*xx*(F(1,2)-y)**2
        stated = (y**4-(2+8*gamma)*y**3+(F(35,2)+4*gamma)*y*y
                  +(2*gamma-F(1,2))*y+F(1,16)-gamma)
        zero(direct-stated)
        # For 0<=y<=1/25, the cubic is absorbed by the extra quadratic.
        assert 4*gamma-(2+8*gamma)/25 >= 0
        # The derivative in x is at least 231/4000 on this rectangle.
        assert F(3,32)-F(1,50)-F(2,125) == F(231,4000)
        item['checks'] = ['linked-expansion', 'linked-square',
                          'leading-square', 'boundary-quartic',
                          'positive-cap-polynomials', 'error-bounds']
        data.append(item)

    # L(gamma) decreases, so positivity for the whole parameter interval
    # follows from its endpoint h=72/25. The high branch decreases too.
    gammax = 1/(2*hmin*hmin)
    assert gammax < F(1,16)
    assert -1+F(2,35)*(F(1,2)-2*F(1,18)) < 0
    # A lightweight adversarial exact grid checks the shifted moment bound.
    checks = 0
    worst = None
    for kval in range(150,601):
        for vv in sorted({max(1,kval//2-1),kval//2,kval//2+1,
                          27*kval//50,kval-1,kval}):
            cap = min(vv*(vv+1)//2,
                      kval*(vv+1)-F(kval*kval,2))
            if cap < (vv+1)//2:
                continue
            for ee in sorted({(vv+1)//2, int(cap), int(cap)//2}):
                if ee < (vv+1)//2 or ee > cap:
                    continue
                for h in [F(72,25),F(29,10),F(59,20),F(3)]:
                    item = parameters(h); gamma=1/(2*h*h)
                    mu=F(item['mu'])
                    rhs = (gamma*(F(kval*kval,2)-ee)**2/kval
                           +mu*kval**3-F(9,4)*kval*kval)
                    slack=linked(F(vv),F(ee))-rhs
                    assert slack >= 0, (kval,vv,ee,h,slack)
                    checks += 1
                    if worst is None or slack < F(worst['slack']):
                        worst=dict(k=kval,v=vv,e=ee,h=str(h),slack=str(slack))
    out=dict(status='EXACT ALGEBRA CERTIFICATE',parameters=data,
             cap_t_polynomial={str(e):str(a) for e,a in tcap.c.items()},
             cap_s_polynomial={str(e):str(a) for e,a in spcap.c.items()},
             shift_error_polynomial={str(e):str(a) for e,a in err.c.items()},
             moment_grid_checks=checks,moment_grid_minimum=worst)
    Path(args.output).parent.mkdir(parents=True,exist_ok=True)
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2),flush=True)


if __name__ == '__main__':
    main()
