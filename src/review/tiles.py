# Run the independent checker on all real tiles in logs/tiles/m*.jsonl (cone tiles and C tiles).
import sys, json, time
from multiprocessing import Pool
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from indep import analyse
P = '/Users/jmercedes/Desktop/Projects/Research/wilfs-conjecture/logs/tiles/'
def job(line):
    d = json.loads(line)
    o, v = analyse(d['h'], d['F'], d['G'], d['q'])
    return d, o, v
if __name__ == '__main__':
    for m in map(int, sys.argv[1:]):
        t0 = time.time()
        lines = open(P + f'm{m}.jsonl').readlines()
        with Pool(10) as p: res = p.map(job, lines, chunksize=50)
        nc = sum(1 for d, o, v in res if d['q']); nC = len(res) - nc
        bad = [(d, v) for d, o, v in res if v]
        msz = {o['m'] for d, o, v in res}
        tags = {}
        for d, v in bad:
            for x in v: tags[x[0]] = tags.get(x[0], 0) + 1
        def mx(key, cone=True):
            vals = [(key(o), (d['h'], d['F'], d['G'], d['q'])) for d, o, v in res if bool(d['q']) == cone]
            return max(vals) if vals else None
        print(f'm={m}: sizes {msz}; cone tiles {nc}, C tiles {nC}; violating {len(bad)} {tags}; {time.time()-t0:.0f}s')
        for name, key in [('maxYd', lambda o: max(o['Yd'])), ('Y', lambda o: o['Y']), ('qO-t', lambda o: o['qO'] - o['t']),
                          ('2tri-t', lambda o: 2*o['tri'] - o['t']), ('qU-t', lambda o: o['qU'] - o['t']), ('t-C', lambda o: o['t'] - o['C']),
                          ('nDS', lambda o: o['nDS']), ('crossonly', lambda o: o['cross_only']), ('rankO', lambda o: o['rankO']),
                          ('rankU', lambda o: o['rankU']), ('Scross', lambda o: o['Scross']), ('Sexc', lambda o: o['Sexc']),
                          ('maxPhi', lambda o: o['maxPhi']), ('LHS-6t', lambda o: o['LHS'] - 6*o['t']),
                          ('C-(3/2+sqrt(6m-15/4))', lambda o: o['C'] - (1.5 + (6*o['m'] - 3.75) ** .5)),
                          ('m+1-LHS-delta', lambda o: o['m'] + 1 - o['LHS'] - o['delta'])]:
            r = mx(key)
            print(f'   cone max {name}: {r[0] if r else None}  {r[1] if r else ""}')
        for d, v in bad[:5]: print('   VIOL', v[:3], d)
