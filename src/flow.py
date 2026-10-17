"""Simple integer max-flow (Dinic) — no external deps."""
from collections import deque


class MaxFlow:
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]

    def add(self, u, v, cap):
        self.g[u].append([v, cap, len(self.g[v])])
        self.g[v].append([u, 0, len(self.g[u]) - 1])

    def run(self, s, t):
        flow = 0
        INF = float('inf')
        while True:
            level = [-1] * self.n
            level[s] = 0
            dq = deque([s])
            while dq:
                u = dq.popleft()
                for v, cap, _ in self.g[u]:
                    if cap > 0 and level[v] < 0:
                        level[v] = level[u] + 1
                        dq.append(v)
            if level[t] < 0:
                return flow
            it = [0] * self.n

            def dfs(u, f):
                if u == t:
                    return f
                while it[u] < len(self.g[u]):
                    e = self.g[u][it[u]]
                    v, cap, rev = e
                    if cap > 0 and level[v] == level[u] + 1:
                        d = dfs(v, min(f, cap))
                        if d > 0:
                            e[1] -= d
                            self.g[v][rev][1] += d
                            return d
                    it[u] += 1
                return 0
            while True:
                f = dfs(s, INF)
                if f == 0:
                    break
                flow += f
