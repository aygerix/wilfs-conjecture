import numpy as np
exec(open('arc_lp2.py').read().split('amax=')[0].replace('return const+res.fun, dict(zip(names,np.round(res.x,2)))','return const+res.fun, res'))
rows=['q3<=Q','3u4<=(a+2)q3','s3+s4<=ab','hAC<=ac','t3+t4<=B','i<=bc','v3<=bq3','2v3<=(a+1)s3','w<=at3','2w<=(b+1)s3','3z<=(b+2)t3','rho>=SR','rho>=ARC']
bad=[]
for a in [1,2,3,5,7,10,20]:
  for b in [1,2,5,10,20,40,80,160,320]:
    for (c,e) in [(0,0),(3,0),(0,3),(5,5)]:
      g,res=W_lp(a,b,c,e)
      if g< -1e-6: bad.append((a,b,c,e,g))
      if (c,e)==(0,0):
        mu=-res.ineqlin.marginals
        print((a,b),'Wmin=%.2f'%g,'(a-1)(b+1)=%d'%((a-1)*(b+1)),' '.join('%s:%.3g'%(r,u) for r,u in zip(rows,mu) if abs(u)>1e-9))
print("negatives:",bad)
