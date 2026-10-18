# Edmonds blossom maximum matching (general graphs), O(V^3)
from collections import deque
def max_matching(n, adj):
    match=[-1]*n; p=[-1]*n; base=list(range(n))
    def lca(a,b):
        used=[False]*n
        while True:
            a=base[a]; used[a]=True
            if match[a]==-1: break
            a=p[match[a]]
        while True:
            b=base[b]
            if used[b]: return b
            b=p[match[b]]
    def mark_path(v,b,ch,blossom):
        while base[v]!=b:
            blossom[base[v]]=blossom[base[match[v]]]=True
            p[v]=ch; ch=match[v]; v=p[match[v]]
    def find_path(root):
        nonlocal p,base
        used=[False]*n; p=[-1]*n
        for i in range(n): base[i]=i
        used[root]=True; q=deque([root])
        while q:
            v=q.popleft()
            for to in adj[v]:
                if base[v]==base[to] or match[v]==to: continue
                if to==root or (match[to]!=-1 and p[match[to]]!=-1):
                    cur=lca(v,to); blossom=[False]*n
                    mark_path(v,cur,to,blossom); mark_path(to,cur,v,blossom)
                    for i in range(n):
                        if blossom[base[i]]:
                            base[i]=cur
                            if not used[i]: used[i]=True; q.append(i)
                elif p[to]==-1:
                    p[to]=v
                    if match[to]==-1: return to
                    to2=match[to]; used[to2]=True; q.append(to2)
        return -1
    for i in range(n):
        if match[i]==-1:
            for j in adj[i]:
                if match[j]==-1: match[i]=j; match[j]=i; break
    for i in range(n):
        if match[i]==-1:
            v=find_path(i)
            while v!=-1:
                pv=p[v]; ppv=match[pv]
                match[v]=pv; match[pv]=v; v=ppv
    return sum(1 for i in range(n) if match[i]>i), match
