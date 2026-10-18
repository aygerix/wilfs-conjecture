# compare c0 = sum_x floor(sum_a <x_a p_a>/m) with upper carries chat = sum_x floor(sum_a l_a(x)/m), l_a(x)=<(top_a x - x)_a p_a>
import sys, itertools
sys.path.insert(0,'/Users/jmercedes/Desktop/Projects/Research/wilfs-conjecture/src')
from exp_cl_tiling import downsets
d=int(sys.argv[1]); M=int(sys.argv[2])
for m in range(3,M+1):
    tot=eq=0; diffs={}
    for D in downsets(m,d):
        Dl=sorted(D); S=set(Dl)
        if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
        tops={}
        for x in Dl:
            for a in range(d):
                t=list(x)
                while tuple(t[:a]+[t[a]+1]+t[a+1:]) in S: t[a]+=1
                tops[(x,a)]=tuple(t)
        for p in itertools.product(range(1,m),repeat=d):
            res={x:sum(i*j for i,j in zip(x,p))%m for x in Dl}
            if len(set(res.values()))!=m: continue
            tot+=1
            c0=sum(sum((x[a]*p[a])%m for a in range(d))//m for x in Dl)
            ch=sum(sum((res[tops[(x,a)]]-res[x])%m for a in range(d))//m for x in Dl)
            diffs[ch-c0]=diffs.get(ch-c0,0)+1
    print('d',d,'m',m,'tiles',tot,'distribution of chat-c0:',dict(sorted(diffs.items())),flush=True)
