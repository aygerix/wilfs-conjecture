"""Print Apery sets of failing interval semigroups (seeds for chain_kunz4 start=3). usage: python seed_intervals.py m k a b"""
import sys
from chain_interval import apery
m, k, a, b = map(int, sys.argv[1:5])
print(','.join(str(x) for x in apery(m, [m] + list(range(k*m + a, k*m + b + 1)))))
