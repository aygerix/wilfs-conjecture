"""Necessary count profiles for a failed ONE-RELAY; run on fejer only.

Every test here is a necessary condition for L_+ < m at ONE-DEFICIT.
No assertion of realizability is made.
"""
import argparse
import json
from math import comb


def profiles(limit):
    out = []
    counts = dict(base=0, partial=0, rectangle=0, minsum=0, moment=0)
    for k in range(5, limit + 1):
        Q = comb(k + 1, 2)
        for s in range(4):
            if k + s < 6:
                continue
            # Flat-CR gives the t=1 result for k>=15, s>=4;
            # this file treats the complementary s<=3 strip only.
            for v in range(2, k + 1):
                g = k - v
                costs = sorted(i + j for i in range(v) for j in range(i, v))
                pref = [0]
                for c in costs:
                    pref.append(pref[-1] + c)
                Qv = comb(v + 1, 2)
                for e in range((v + 1) // 2, Qv + 1):
                    q = Q - e
                    if q < 1:
                        continue
                    m = k + q + s + 2
                    counts['base'] += 1
                    if s * (comb(v + 1, 2) - 1) + e + k - 6 >= g * (2*k - g + 1)//2:
                        continue
                    counts['partial'] += 1
                    if m < k * (g + 1) + 1:
                        continue
                    counts['rectangle'] += 1
                    Amax = m - 1 - s*(Q-2) - 2*(k+s-1)
                    if Amax < max(comb(v, 2), pref[e]):
                        continue
                    counts['minsum'] += 1
                    qv = Qv - e
                    if comb(qv, 2) > v*Amax:
                        continue
                    counts['moment'] += 1
                    out.append(dict(k=k,s=s,g=g,v=v,e=e,q=q,m=m,Amax=Amax,
                                    M=pref[e],qv=qv))
    return counts, out


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=100)
    ap.add_argument('--output')
    args = ap.parse_args()
    counts, out = profiles(args.limit)
    print(json.dumps(counts, sort_keys=True))
    for k in sorted({x['k'] for x in out}):
        rows = [x for x in out if x['k']==k]
        print(k, len(rows), 's', sorted({x['s'] for x in rows}),
              'v', (min(x['v'] for x in rows),max(x['v'] for x in rows)))
    print('total',len(out),'last',max((x['k'] for x in out),default=None))
    if args.output:
        with open(args.output,'w') as f:
            json.dump(dict(counts=counts,profiles=out),f,indent=2)
