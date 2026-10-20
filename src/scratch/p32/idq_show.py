"""Print canonical reps, levels, wraps j, crossing weight c of every position of a model (lead, 2026-10-20).
Usage: python idq_show.py m rho q b1,b2,..."""
import sys
sys.path.insert(0, __import__('os').path.dirname(__file__))
from idq import canon
m, rho, q = map(int, sys.argv[1:4]); B = [int(x) for x in sys.argv[4].split(',')]
best = canon(m, rho, B, q, q + 3)
for u in range(m):
    if u not in best: print(u, "unreached"); continue
    lam, t, code, a = best[u]
    j = lam - t
    c = sum(a[i] for i, b in enumerate(B) if a[i] > 0 and b > u)
    rep = "+".join(str(B[i]) for i in range(len(B)) for _ in range(a[i])) or "0"
    tag = "DEF" if c < j and lam <= q else ("exc" if c > j and lam <= q else "")
    print(f"u={u:3d} lam={lam} t={t} j={j} c={c} rep={rep} {tag}")
