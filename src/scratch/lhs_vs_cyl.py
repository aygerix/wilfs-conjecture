# Delta = LHS(D) - LHS(Cyl) for cone tiles (dumped) and for RCON sets from an annealing-free random sample.
import sys, json
sys.path.insert(0, 'src/scratch'); sys.path.insert(0, 'src/scratch/forest')
from tile_dump import rebuild
from cls_anneal import stats
def lhs(D):
    s = stats(D); return 2*s['t'] + 2*s['tri'] + s['qU'] + s['qO'], s
if __name__ == '__main__':
    for m in map(int, sys.argv[1:]):
        best = None
        for l in open(f'logs/tiles/m{m}.jsonl'):
            d = json.loads(l)
            if not d['q']: continue
            D = rebuild(d['h'], d['F'], d['G'], d['q']); Cy = rebuild(d['h'], d['F'], d['G'], None)
            a, s = lhs(D); b, s2 = lhs(Cy); dl = a - b
            if best is None or dl > best[0]: best = (dl, d['h'], d['F'], d['G'], d['q'], a, b, s['C'])
        print(f'm={m}: max LHS(D)-LHS(Cyl) = {best[0]}  {best[1:]}', flush=True)
