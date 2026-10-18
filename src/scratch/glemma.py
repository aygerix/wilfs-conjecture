# G-bound lemma: l_1..l_d in [1,m-1] with all 2^d subset sums distinct mod m; sigma in [0,m).
# S=sigma+sum l, C=S//m, r=S%m, k=#{a: l_a>r}, G=k-C.  Claim: G in {-1,0,1}, G=1 => r<=m-sigma-2, G=-1 => r>=m-sigma
import sys, itertools
d=int(sys.argv[1]); M=int(sys.argv[2])
for m in range(2**d, M+1):
    viol=0; ex=None; cnt=0
    for l in itertools.combinations_with_replacement(range(1,m),d):
        sums=set()
        ok=True
        for A in range(1<<d):
            s=sum(l[a] for a in range(d) if A>>a&1)%m
            if s in sums: ok=False; break
            sums.add(s)
        if not ok: continue
        cnt+=1
        for sg in range(m):
            S=sg+sum(l); C=S//m; r=S%m; k=sum(1 for x in l if x>r); G=k-C
            bad = G>1 or G<-1 or (G==1 and r>m-sg-2) or (G==-1 and r<m-sg)
            if bad:
                viol+=1
                if ex is None: ex=(l,sg,S,C,r,k,G)
    print('d',d,'m',m,'admissible l-vectors',cnt,'violations',viol,ex,flush=True)
