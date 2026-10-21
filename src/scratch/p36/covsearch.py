r"""Hill-climb for full-pair height-3 covers (lead, 2026-10-20): s_1..s_d in Z/m with {0} u {s_a} u {s_a+s_b} distinct
and Delta_3(s) = Z/m.  Objective: number of residues covered by Delta_3 (pair injectivity enforced as a hard constraint,
restarts on failure).  Prints every distinct full cover found (sorted s, up to the multiplier action not removed).
usage: ~/mathenv/bin/python -I covsearch.py d m RESTARTS STEPS SEED"""
import sys, random, itertools
d, m, RS, ST, seed = map(int, sys.argv[1:6]); rng = random.Random(seed)
pairs = [(a, b) for a in range(d) for b in range(a, d)]
cubes = [(a, b, c) for a in range(d) for b in range(a, d) for c in range(b, d)]
def ok2(s):
    R = {0} | set(s)
    if len(R) != d + 1: return False
    for a, b in pairs:
        x = (s[a] + s[b]) % m
        if x in R: return False
        R.add(x)
    return True
def cov(s):
    R = {0} | set(s) | {(s[a] + s[b]) % m for a, b in pairs} | {(s[a] + s[b] + s[c]) % m for a, b, c in cubes}
    return len(R)
found = set()
for r in range(RS):
    while True:
        s = rng.sample(range(1, m), d)
        if ok2(s): break
    v = cov(s)
    for it in range(ST):
        t = s[:]; t[rng.randrange(d)] = rng.randrange(1, m)
        if not ok2(t): continue
        u = cov(t)
        if u >= v:
            s, v = t, u
            if v == m:
                key = tuple(sorted(s))
                if key not in found:
                    found.add(key); print("m=%d d=%d s=%s" % (m, d, ",".join(map(str, key))), flush=True)
                break
print("# d=%d m=%d restarts=%d full covers=%d" % (d, m, RS, len(found)), file=sys.stderr)
