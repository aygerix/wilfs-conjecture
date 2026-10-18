import sys, time; sys.path.insert(0,'.')
from e2e import analyse, new_stats
G=int(sys.argv[1]); B=2*G+3
def mingens(gaps):
    S=[n for n in range(1,B+1) if n not in gaps]
    Sset=set(S)
    return [x for x in S if not any((x-y) in Sset for y in S if y < x and y<=x-y)]
t0=time.time(); stats=new_stats(); level=[frozenset()]; tot=0; e4=0
for g in range(0,G+1):
    nxt=[]
    for gaps in level:
        tot+=1
        F=max(gaps) if gaps else -1
        mg=mingens(gaps)
        if gaps:
            m=mg[0]; others=[x for x in mg if x!=m]
            if len(mg)==4:
                e4+=1; analyse(m, others, stats, sieve=True)
        if g<G:
            for x in mg:
                if x>F: nxt.append(gaps|{x})
    level=nxt
print('genus<=',G,'semigroups',tot,'e=4',e4,f'{time.time()-t0:.0f}s')
for k,v in stats.items():
    if k=='class_': continue
    print(k, (len(v), v[:40]) if isinstance(v,list) else v)
