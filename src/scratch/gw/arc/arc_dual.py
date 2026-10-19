import numpy as np, sys
from scipy.optimize import linprog
exec(open('arc_lp2.py').read().split('amax=')[0].replace('return const+res.fun, dict(zip(names,np.round(res.x,2)))','return const+res.fun, res'))
rows=['q3<=Q','3u4<=(a+2)q3','s3+s4<=ab','hAC<=ac','t3+t4<=B','i<=bc','v3<=b q3','2v3<=(a+1)s3','w<=a t3','2w<=(b+1)s3','3z<=(b+2)t3','rho>=SR','rho>=ARC']
for (a,b,c,e) in [(5,0,0,0),(8,0,0,0),(8,1,0,0),(8,2,0,0),(8,5,0,0),(12,1,0,0),(12,3,0,0),(8,0,1,0),(8,0,0,1),(8,1,1,1),(3,4,0,0),(1,5,0,0),(20,2,1,1)]:
    g,res=W_lp(a,b,c,e)
    mu=-res.ineqlin.marginals
    print((a,b,c,e),'W_min=%.3f'%g,' '.join('%s:%.3g'%(r,u) for r,u in zip(rows,mu) if abs(u)>1e-9))
