"""Exact tests of the uniform Macaulay low-cost lemma. fejer only."""
from a4_stability import grow
from math import comb
from fractions import Fraction as F
import argparse
import json


def test(last):
    cases=0;per=[]
    for a in range(3,last+1):
        Q=comb(a+1,2);deficit=comb(a+1,3);subcases=0
        for q2 in range(Q+1):
            bound=min((a+1)*q2,deficit)
            for u in range(grow(q2,2)+1):
                k=grow(u,3)
                L=(a+1)*(q2+u)-4*k
                assert L>=bound,(a,q2,u,k,L,bound)
                cases+=1;subcases+=1
        per.append(dict(a=a,cases=subcases))
    # Rational checks of the exact factorization and derivative sign used
    # in the proof. These checks are supplementary to the symbolic identity.
    rational=0
    for a in range(3,101):
        for i in range(201):
            r=F(a-2)+F(i,100)
            G=r**3+5*r**2+(5-a)*r-a*a+1
            low=r*(r+1)*(a*(r+5)-r*r-4*r-1)/6
            assert low-F(comb(a+1,3))==(a-r)*G/6
            assert G>=0 and 3*r*r+10*r+5-a>0
            rational+=1
    print(json.dumps(dict(a_max=last,integer_Macaulay_cases=cases,per_a=per,rational_checks=rational)),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--amax',type=int,default=24);args=p.parse_args();test(args.amax)
