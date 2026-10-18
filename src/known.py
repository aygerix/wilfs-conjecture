"""known_wilf(S): list of literature conditions (LITERATURE.md table) that already guarantee Wilf for S.
Empty list => S is not covered by any implemented condition.  Implemented: #numbers refer to LITERATURE.md §1.
Conditions not implemented (rare / hard to test): positioned (#6), true grading (#14), Spirito large-ratio variant,
gluings/dilations.  A non-empty answer is a sufficient certificate only if the cited theorem's hypotheses are exactly as coded."""
from math import gcd, isqrt, ceil
from functools import reduce

def known_wilf(s):
    m, e, c, g = s.m, s.e, s.c, s.g
    ell = c - g
    q = -(-c // m)
    t = s.t()
    P = list(s.P)
    out = []
    if c <= 1 or e >= m: out.append('trivial/MED')
    if m <= 19: out.append('m<=19 (#Kliem-Stump)')
    if 3*e >= m: out.append('3e>=m (#21)')
    if q <= 3: out.append('q<=3 (#13)')
    if e <= 3: out.append('e<=3')
    if t <= e - 1: out.append('t<=e-1 (FGH)')
    if c <= 4*ell: out.append('c<=4n (#7)')
    if 2*g < 3*m: out.append('2g<3m (#11)')
    if g < 2*m - (2*m)**0.5: out.append('g<2m-sqrt(2m) (#12)')
    if g <= 100: out.append('g<=100 (DEF)')
    if c % m == 0 and g <= 120: out.append('m|c, g<=120 (DEF)')
    if c % m == 0 and 4*e >= m: out.append('m|c, 4e>=m (Divsets)')
    if max(P) <= 60: out.append('maxP<=60 (#41)')
    if ell <= 12: out.append('n<=12 (Eliahou-Marin)')
    k = sum(1 for x in range(m + 1, 2*m) if x in s)
    if q > 2 and k*k*(q - 2) >= q*m: out.append('|S∩(m,2m)|>=sqrt(qm/(q-2)) (#33)')
    if 2*g == (c - 1) + t: out.append('almost symmetric (#5)')
    L = [x for x in range(1, c) if x in s]
    if L and reduce(gcd, L) >= 2: out.append('gcd(L)>=2')
    r2 = P[1] if len(P) > 1 else None
    if e >= 10 and r2 is not None and 3*r2 > c + m and 25*m <= 8*e*e + 5*e - 31.25: out.append('Spirito (#24)')
    rp = -(-m // e)
    if rp > 3:
        bound = rp*(3*rp*rp - rp - 4)*(3*rp*rp - rp - 2) / (8*(rp - 2))
        phi = 1
        x = rp; p = 2
        while x > 1:
            if x % p == 0:
                phi *= p
                while x % p == 0: x //= p
            p += 1
        if m >= bound and gcd(m, phi) == 1: out.append('Moscariello-Sammartano (#23)')
    return out
