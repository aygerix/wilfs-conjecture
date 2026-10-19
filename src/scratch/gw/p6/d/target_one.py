import argparse,json,random
from collections import Counter
from core import optimal_one

ap=argparse.ArgumentParser();ap.add_argument('--trials',type=int,default=100000)
ap.add_argument('--seed',type=int,default=260619);ap.add_argument('--output',default='target_one.json')
args=ap.parse_args();rng=random.Random(args.seed);counts=Counter();best={}
for step in range(args.trials):
    m=rng.randrange(17,151);rho=rng.randrange(8,(m+1)//2)
    rp=rng.randrange(2,(rho-2)//3+1)
    if (rho+rp)%2: continue
    u=(rho+rp)//2
    pool=[v for v in range(m-rho) if v not in (0,1,u,rho,rp)]
    k=rng.randrange(5,min(18,len(pool)+3)+1)
    U=sorted([0,1,u]+rng.sample(pool,k-3));y=(U.index(u),)*3
    counts['trials']+=1
    for nopos in (False,True):
        ans=optimal_one(m,rho,U,y,nopos)
        if ans is None: continue
        counts['deficits']+=1;counts['s='+str(ans['s'])]+=1
        key='no_positive' if nopos else 'HC'
        if key not in best or ans['Lplus']-m<best[key]['Lplus']-best[key]['m']:
            best[key]=ans
        assert ans['S']>=0
        assert ans['HC']>=0
print(json.dumps(dict(counts=counts,best=best),sort_keys=True),flush=True)
with open(args.output,'w') as f:json.dump(dict(counts=counts,best=best),f,indent=2)
