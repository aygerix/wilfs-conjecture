r"""Merge enumlp part outputs: per (m, e) global minima of RT2, UA2, W, RT2/W, UA2/W with representatives; counts.
usage: python3 mergelp.py lp_M_E_p*.txt ..."""
import sys, re, collections
G = collections.defaultdict(lambda: dict(S=0, keys=0, ua=0, neg=0, wneg=0, rt2=(1e30, ''), ua2=(1e30, ''), w=(1 << 60, ''), rt2w=(1e30, ''), ua2w=(1e30, '')))
for fn in sys.argv[1:]:
    me = None
    for line in open(fn):
        mm = re.match(r'SUMMARY m=(\d+) e=(\d+) .* S=(\d+) keys=(\d+) UA2solves=(\d+) negRT2=(\d+) W<=0:(\d+)', line)
        if mm:
            me = (int(mm.group(1)), int(mm.group(2))); g = G[me]
            for k, i in (('S', 3), ('keys', 4), ('ua', 5), ('neg', 6), ('wneg', 7)): g[k] += int(mm.group(i))
            continue
        mm = re.match(r'r=(\d+) minRT2=([-\d.]+) (<[^>]+>) minUA2=([-\d.]+) (<[^>]+>) minW=(-?\d+) (<[^>]+>)', line)
        if mm and me:
            g = G[me]
            if float(mm.group(2)) < g['rt2'][0]: g['rt2'] = (float(mm.group(2)), mm.group(3))
            if float(mm.group(4)) < g['ua2'][0]: g['ua2'] = (float(mm.group(4)), mm.group(5))
            if int(mm.group(6)) < g['w'][0]: g['w'] = (int(mm.group(6)), mm.group(7))
        mm = re.match(r'minRT2/W=([-\d.]+) (<[^>]+>) minUA2/W=([-\d.]+) (<[^>]+>)', line)
        if mm and me:
            g = G[me]
            if float(mm.group(1)) < g['rt2w'][0]: g['rt2w'] = (float(mm.group(1)), mm.group(2))
            if float(mm.group(3)) < g['ua2w'][0]: g['ua2w'] = (float(mm.group(3)), mm.group(4))
for me in sorted(G):
    g = G[me]
    print("m=%d e=%d S=%d keys=%d UA2solves=%d negRT2=%d W<=0=%d | minRT2 %.4f %s | minUA2 %.4f %s | minW %d %s | minRT2/W %.4f %s | minUA2/W %.4f %s" % (
        me[0], me[1], g['S'], g['keys'], g['ua'], g['neg'], g['wneg'], *g['rt2'], *g['ua2'], *g['w'], *g['rt2w'], *g['ua2w']))
