"""P5f exact auxiliary checks; fejer only, one core.

Checks the new Macaulay block estimates exhaustively to a=300,
and the parameter-dependent endpoint inequalities at alpha=4..2000.
The proofs in the report do not depend on extrapolating these grids.
"""
from math import comb
from fractions import Fraction as F
import json

def C(n,k):return comb(n,k) if n>=k else 0
blocks=half=middle=0
for a in range(24,301):
    for j in range(a+1):
        base=C(j+1,2)
        for z in range(j+1):
            q=base+z
            if q>C(a+1,2):break
            mac=C(j+2,3)+C(z+1,2)
            gap=(a+2)*q-3*mac
            assert 3*mac<=(j+3)*q
            if 3*a*(a+1)+(a-3)*q-4*mac<0:
                assert 2*j>a;half+=1
            if 2*j>a and j<=a-2:
                assert 8*gap>a*a;middle+=1
            blocks+=1
endpoints=0
for al in range(4,2001):
    R=C(al+1,2);K=R-1
    for a in (16*R,16*R+1,32*R):
        assert a-1-2*al-R>=a//2
        assert F(4*al+5,3)<=F(a,8) and al+2<=F(a,8)
        assert F(R*(4*a-3*R-1),2)>=K*a
        assert F(a*(a-1),2)>=K*a
        assert F(a*a,8)>K*a
        endpoints+=1
assert F(3375,4096)-F(65,64)**2/64-F(65,64)/96>F(2,3)
assert F(67,64)**3/6<F(1,5)
assert F(1,5)+F(1,256)<F(1,3)
out=dict(macaulay_profiles=blocks,negative_original_lower=half,
         middle_block_profiles=middle,large_A_endpoints=endpoints,
         B_bound_constants=True)
print(json.dumps(out,sort_keys=True))
