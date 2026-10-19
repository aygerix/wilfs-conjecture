import numpy as np
exec(open('arc_lp2.py').read().split('amax=')[0])
from math import comb
for (a,b) in [(20,80),(20,160),(20,320),(10,160),(5,320)]:
    g,x=W_lp(a,b,0,0)
    Q=a*(a+1)//2; B=b*(b+1)//2; Z=comb(b+2,3)
    N=sum(x[n] for n in names if n!='rho'); m=1+a+b+N
    print((a,b),'Wmin=%.1f'%g,'Q=%d B=%d Z=%d'%(Q,B,Z),{k:v for k,v in x.items() if abs(v)>1e-9},'m=%.0f h=%.0f'%(m,m-x['rho']))
