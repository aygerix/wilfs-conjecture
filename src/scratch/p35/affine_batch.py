r"""Affine images of a sum cover {0} u delta of Z/m: delta' = u*(A - a) minus 0, for units u and a in A (lead,
2026-10-20).  Prints one delta' per line (deduplicated up to sorting), in random order with a fixed seed, for the
batch driver.  Usage: python affine_batch.py m a0,a1,... SEED"""
import sys, math, random
m = int(sys.argv[1]); A = [int(t) for t in sys.argv[2].split(',')]; rnd = random.Random(int(sys.argv[3]))
out = set()
for u in range(1, m):
    if math.gcd(u, m) != 1: continue
    for a in A:
        B = sorted({(u * (x - a)) % m for x in A} - {0})
        if len(B) == len(A) - 1: out.add(tuple(B))
L = sorted(out); rnd.shuffle(L)
for B in L: print(','.join(map(str, B)))
