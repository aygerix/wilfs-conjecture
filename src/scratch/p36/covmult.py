"""Multiplier images u*s (u a unit mod m) of the covers in FILE, deduplicated, printed in nearcov format (lead, 2026-10-21).
usage: python3 covmult.py FILE"""
import sys, re
from math import gcd
seen = set()
for line in open(sys.argv[1]):
    mm = re.match(r'm=(\d+) d=(\d+) s=([0-9,]+)', line)
    if not mm: continue
    m, d = int(mm.group(1)), int(mm.group(2)); s = [int(t) for t in mm.group(3).split(',')]
    for u in range(1, m):
        if gcd(u, m) != 1: continue
        t = tuple(sorted(u * x % m for x in s))
        if t not in seen: seen.add(t); print("m=%d d=%d s=%s" % (m, d, ",".join(map(str, t))))
