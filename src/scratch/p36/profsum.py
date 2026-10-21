r"""Summarize prof.log (kunz_prof.py): per instance the shares of total time spent before the first incumbent, before the
final (optimal) incumbent, and before the bound reaches 0; root bound vs optimum.  usage: python3 profsum.py prof.log"""
import sys, re
rows = []
for line in open(sys.argv[1]):
    mm = re.search(r'm=(\d+) e=(\d+) r=(\d+) obj=(\w+) (\w+) .*val=([-\d.]+) .*PROF root=\(([\d.e-]+), ([-\d.e]+)\) first=([\d.e-]+) final_inc=([\d.e-]+) bound>=0 at ([\d.e-]+|None) .* total=([\d.]+) nodes=(\d+)', line)
    if not mm: continue
    m, e, r, o, st, val, rt, rb, fi, fin, b0, tot, nd = mm.groups()
    tot = float(tot); rows.append(dict(m=int(m), r=int(r), o=o, st=st, val=float(val), root=float(rb), first=float(fi), fin=float(fin),
                                        b0=float(b0) if b0 != 'None' else tot, tot=tot, nodes=int(nd)))
for o in ('RT2', 'UA2'):
    R = [x for x in rows if x['o'] == o]
    if not R: continue
    T = sum(x['tot'] for x in R)
    print("%s: %d instances, total %.0fs | time before optimal incumbent %.0f%% | proving after it %.0f%% | bound reaches 0 at %.0f%% of total"
          " | first incumbent median %.2fs | root bound range [%.0f, %.0f] vs optimum [%.1f, %.1f] | nodes median %d" % (
          o, len(R), T, 100 * sum(x['fin'] for x in R) / T, 100 * sum(x['tot'] - x['fin'] for x in R) / T,
          100 * sum(x['b0'] for x in R) / T, sorted(x['first'] for x in R)[len(R) // 2],
          min(x['root'] for x in R), max(x['root'] for x in R), min(x['val'] for x in R), max(x['val'] for x in R),
          sorted(x['nodes'] for x in R)[len(R) // 2]))
    for x in sorted(R, key=lambda x: -x['tot'])[:3]:
        print("   slowest: m=%d r=%d total %.0fs, optimum found at %.0fs, bound>=0 at %.0fs, root %.0f, opt %.2f, nodes %d" % (
              x['m'], x['r'], x['tot'], x['fin'], x['b0'], x['root'], x['val'], x['nodes']))
