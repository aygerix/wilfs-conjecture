from collections import deque
class MF:
    def __init__(s,n): s.n=n; s.g=[[] for _ in range(n)]
    def add(s,u,v,c):
        s.g[u].append([v,c,len(s.g[v])]); s.g[v].append([u,0,len(s.g[u])-1])
    def flow(s,src,snk):
        tot=0
        while True:
            lvl=[-1]*s.n; lvl[src]=0; q=deque([src])
            while q:
                u=q.popleft()
                for v,c,r in s.g[u]:
                    if c>0 and lvl[v]<0: lvl[v]=lvl[u]+1; q.append(v)
            if lvl[snk]<0: return tot
            it=[0]*s.n
            def dfs(u,f):
                if u==snk: return f
                while it[u]<len(s.g[u]):
                    e=s.g[u][it[u]]; v,c,r=e
                    if c>0 and lvl[v]==lvl[u]+1:
                        d=dfs(v,min(f,c))
                        if d>0:
                            e[1]-=d; s.g[v][r][1]+=d; return d
                    it[u]+=1
                return 0
            while True:
                f=dfs(src,10**9)
                if f==0: break
                tot+=f
