"""Exact audit of the analytic a=6 reductions, executed only on fejer."""
from a4_stability import catalog
from packing_fibers import bound
from fractions import Fraction
from math import comb
from collections import Counter
import json

def P(d):return comb(d+3,3)
def H(d):return P(d)+2*comb(d+1,3)

def main():
    hist=Counter();profiles=catalog(6)
    for q2,q3,u3,u4,k,WA in profiles:
        rA=21-q2-q3;t=56-u3-u4;budget=-WA-1
        assert rA<=1 and q2<=4
        assert 39-rA>budget and 48-2*rA>budget
        for b in range(21):
            Ccost=23-rA+q2+6*b+(b+1)*u3
            if Ccost>budget:continue
            assert rA==0
            upper=P(6+b)-t+k+7+b
            assert H(6)-bound(7)*t>upper,(q2,u3,k,t,b)
            hist['surviving_C_cases_excluded_by_packing']+=1
    patterns=[(1,),(2,),(3,),(4,),(5,),(6,),(1,1),(1,2)]
    for b in range(1,51):
        for pd in patterns:
            if len(pd)>b:continue
            pads=list(pd)+[0]*(b-len(pd));p=sum(pd)
            losses=sorted([max(pads[j],pads[k]) for j in range(b) for k in range(j,b)],reverse=True)
            expected=(2*b-1,4*b-2,6*b-3,8*b-4,7*b-5,6*b-6,4*b-5,6*b-6)[patterns.index(pd)]
            for q in range(len(losses)+1):
                lower=12*q-(b+1)*p+3*sum(losses[q:])
                assert lower>=expected,(b,pd,q,lower,expected)
                hist['neighbor_minima']+=1
    for d in range(18,1001):
        R=Fraction(2*d+38,3)
        D0=H(d)-Fraction(3*(d+1),2)*R-(P(d)-R+6)
        poly0=2*d**3-6*d*d-118*d-74
        assert 6*D0==poly0 and poly0>0 and 6*d*d-12*d-118>0
        D1=H(d-1)-Fraction(3*d,2)*(R-d)-(P(d)-1-R+6)
        poly1=2*d**3-6*d*d-115*d+40
        assert 6*D1==poly1 and poly1>0 and 6*d*d-12*d-115>0
        assert 2*d-1>R
        hist['polynomial_and_two_missing_pair_checks']+=1
    print(json.dumps(dict(mode='a6_analytic_reductions',counts=hist)),flush=True)

if __name__=='__main__':main()
