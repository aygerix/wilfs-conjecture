"""Print integer coefficient certificates; independent formula checks. fejer."""
from fractions import Fraction as F
from math import lcm,comb
from pathlib import Path
import json

d=json.loads(Path('dense_poly.json').read_text());g=json.loads(Path('generic_density.json').read_text())
tables={}
for name,row in [('D9zero',d['endpoints']['zero']),('D9max',d['endpoints']['max']),
                 ('G075zero',g['D075']['endpoints']['zero']),('G075max',g['D075']['endpoints']['max'])]:
    p=list(map(F,row['poly']));a=row['shift'];c=list(map(F,row['coeff']));L=lcm(*(x.denominator for x in p+c))
    out=dict(denominator=L,poly=[int(x*L) for x in p],shift=a,coeff=[int(x*L) for x in c])
    assert all(x>=0 for x in out['coeff'])
    tables[name]=out;print('INTEGER_CERT',name,json.dumps(out,sort_keys=True))
for k in range(3,201):
    Q=F(k*(k+1),2);U=F(k*(k+1)*(k+2),6)
    for tag,r in [('zero',F(0)),('max',F(k*k,9))]:
        a=F(k,3);N=1+k+Q-a;J=N*(N-1)/2;t=U-r
        M=F(k**3+2*k*k+3*k+2,2)-3*(k-1)*r
        target=(M-Q-t)*J-(a+2*t)*(M-1)+t*(t-1)+a*t+a*(a-1)/2
        p=list(map(F,d['endpoints'][tag]['poly']));assert target==sum(x*k**i for i,x in enumerate(p))
    for tag,r in [('zero',F(0)),('max',F(3*k*k,40))]:
        n=F(23*k,25);a=F(2*k,25);N=1+k+Q-a;J=N*(N-1)/2;t=U-r
        M=(n**3+2*n*n+3*n+2)/2-3*(n-1)*r
        target=(M-Q-t)*J-(a+2*t)*(M-1)+t*(t-1)
        p=list(map(F,g['D075']['endpoints'][tag]['poly']));assert target==sum(x*k**i for i,x in enumerate(p))
    C=F(k*(k-1),2)
    assert C*C-(C+3*k*(k+1)+1)+1==F(k*(k+1)*(k-5)*(k+2),4)
    t=F(k*k,16)
    assert C*C-(C+3*k*(k+1)+1)*t+t*t==F(3*k*k,256)*(3*k*k-56*k+16)
Path('certificate_tables.json').write_text(json.dumps(tables,indent=2)+'\n')
print('CERTIFICATE_TABLES_PASS range=3..200')
