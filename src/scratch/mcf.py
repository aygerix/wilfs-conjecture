# min-cost transportation (supplies -> demands) by successive shortest paths (Bellman-Ford), integer costs
def min_cost_transport(sup, dem, cost):
    # sup: list of supplies, dem: list of demands, cost[i][j] or None (forbidden). returns min cost or None
    S=len(sup); T=len(dem); n=S+T+2; src=S+T; snk=src+1
    g=[[] for _ in range(n)]
    def add(u,v,cap,c):
        g[u].append([v,cap,c,len(g[v])]); g[v].append([u,0,-c,len(g[u])-1])
    for i in range(S): add(src,i,sup[i],0)
    for j in range(T): add(S+j,snk,dem[j],0)
    for i in range(S):
        for j in range(T):
            if cost[i][j] is not None: add(i,S+j,10**6,cost[i][j])
    flow=0; tot=0; need=sum(sup)
    while flow<need:
        dist=[None]*n; dist[src]=0; prev=[None]*n
        changed=True
        while changed:
            changed=False
            for u in range(n):
                if dist[u] is None: continue
                for k,(v,cap,c,r) in enumerate(g[u]):
                    if cap>0 and (dist[v] is None or dist[u]+c<dist[v]):
                        dist[v]=dist[u]+c; prev[v]=(u,k); changed=True
        if dist[snk] is None: return None
        f=need-flow; v=snk
        while v!=src:
            u,k=prev[v]; f=min(f,g[u][k][1]); v=u
        v=snk
        while v!=src:
            u,k=prev[v]; g[u][k][1]-=f; g[v][g[u][k][3]][1]+=f; v=u
        flow+=f; tot+=f*dist[snk]
    return tot
