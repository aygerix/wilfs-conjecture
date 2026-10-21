# f0mulo: MU-LO ratio (mu*hlo_mu + h_hi)/Delta3 and PAY2-type slacks on every Q5 example printed by f0ann (files given)
import sys, re
exec(open('rayU0.py').read().split('rng = random.Random')[0])
seen = set(); rows = []
for fn in sys.argv[1:]:
    for L in open(fn):
        g = re.search(r'm=(\d+).*A=<([\d,]+)>', L)
        if not g: continue
        m = int(g.group(1)); A = list(map(int, g.group(2).split(',')))
        if (m, tuple(A)) in seen: continue
        seen.add((m, tuple(A))); r = evalS(m, A)
        if r: r['A'] = A; rows.append(r)
print(len(rows), 'distinct F0 examples re-evaluated')
for r in sorted(rows, key=lambda r: -(r['ratio'] or 0))[:6]:
    print(f"  ratio={r['ratio']:.3f} e={r['e']} mu={r['mu']} m={r['m']} cT={r['cT']} D3={r['D3']} hlo_mu={r['hlo_mu']} hhi={r['hhi']} P1={r['P1']} W={r['W']} A={r['A']}")
print('  MU-LO fails:', sum(1 for r in rows if r['mu'] <= r['e'] and r['D3'] < r['mu'] * r['hlo_mu'] + r['hhi']))
