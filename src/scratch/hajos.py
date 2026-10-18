# Box tiles: check (i) Hajos: some coordinate a has k_a*p_a = 0 mod m (subgroup factor);
# (ii) the inductive identity  SumG = SumG'_red - n*q_sigma + sum_{x'} floor(<sigma+Lambda'(x')>_m / n)
# where coordinate a0 is a subgroup factor, n = m/k_{a0}; (iii) Base-CL range.
import itertools, sys
def boxes(m,d):
    # all k with prod = m, k_a >= 2
    def rec(rem,d):
        if d==0:
            if rem==1: yield ()
            return
        for k in range(2,rem+1):
            if rem%k==0:
                for r in rec(rem//k,d-1): yield (k,)+r
    yield from rec(m,d)
def sumG(ks,ps,m,sig):
    tot=0
    for x in itertools.product(*[range(k) for k in ks]):
        l=[(xi*pi)%m for xi,pi in zip(x,ps)]
        r=(sig+sum(l))%m
        tot+=sum(1 for la in l if la>r)-(sig+sum(l))//m
    return tot
bad=0; cnt=0; nohajos=0
for d in range(2,5):
  for m in range(4,int(sys.argv[1])+1):
    for ks in boxes(m,d):
      for ps in itertools.product(range(1,m),repeat=d):
        vals={sum(xi*pi for xi,pi in zip(x,ps))%m for x in itertools.product(*[range(k) for k in ks])}
        if len(vals)!=m: continue
        subs=[a for a in range(d) if (ks[a]*ps[a])%m==0]
        if not subs: nohajos+=1; continue
        a0=subs[0]; n=m//ks[a0]
        ks2=ks[:a0]+ks[a0+1:]; ps2=ps[:a0]+ps[a0+1:]
        for sig in range(m):
            cnt+=1
            G=sumG(ks,ps,m,sig)
            assert -sig<=G<=m-1-sig, (ks,ps,sig,G)
            if d-1>=1:
                ps2n=tuple(p%n for p in ps2)
                Gred=sumG(ks2,ps2n,n,sig%n) if len(ks2)>0 else 0
                corr=0
                for x in itertools.product(*[range(k) for k in ks2]):
                    L=sum((xi*pi)%m for xi,pi in zip(x,ps2))
                    corr+=((sig+L)%m)//n
                if G!=Gred-n*(sig//n)+corr: bad+=1
    print('d',d,'m',m,'checked',cnt,'identity failures',bad,'no-Hajos',nohajos,flush=True)
