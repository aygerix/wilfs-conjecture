"""Exact REST verification by Dijkstra, chains and pair counts. Fejer only."""
import heapq,json,sys
def apery(g):
    m=min(g);w=[10**100]*m;w[0]=0;pq=[(0,0)]
    while pq:
        x,r=heapq.heappop(pq)
        if x!=w[r]:continue
        for n in g:
            j=(r+n)%m;v=x+n
            if v<w[j]:w[j]=v;heapq.heappush(pq,(v,j))
    return w
def check(g):
    g=sorted(g);m=g[0];w=apery(g);ap=set(w);M=max(w);c=M-m+1;d=len(g)-1
    ellp=sum((M-x)//m for x in w if x)
    N={n:0 for n in g[1:]};con={x:0 for x in w};tops={}
    for x in sorted(w):
        tops[x]={}
        for n in g[1:]:
            t=x
            while t+n in ap:t+=n
            tops[x][n]=t;con[x]+=(M-x)%m-(M-t)
    for n in g[1:]:
        for x in w:
            if x:
                for z in w:
                    if z>x and (z-x)%n==0:N[n]+=1
    rest=sum(v for x,v in con.items() if x)
    rest_count=sum(n*N[n] for n in N)-m*d*ellp
    assert rest==rest_count
    return dict(generators=g,apery_by_residue=w,M=M,c=c,n1=g[1],M_ge_3n1=M>=3*g[1],
                ellp=ellp,N=N,con=con,tops=tops,REST=rest,REST_count=rest_count,
                con0=con[0],Delta=sum(con.values()),C2=m*(m-1)//2)
if __name__=='__main__':
    gg=list(map(int,sys.argv[1:])) if len(sys.argv)>1 else [4,5]
    print(json.dumps(check(gg),indent=2))
