# cycle rank of the tripod incidence graph (and qO/qU elimination excess) on dumped PW sets
import sys, re
sys.path.insert(0, 'src/scratch')
from tripod_cycles import analyze
mx = 0; n = 0; ex = None
for line in open(sys.argv[1]):
    mm = re.search(r'h=([\d,]+) F=([\d,]+) G=([\d,]+) q=\((\d+),(\d+),(\d+)\)', line)
    h, F, G = [tuple(map(int, mm.group(k).split(','))) for k in (1, 2, 3)]; q = tuple(map(int, mm.group(4, 5, 6)))
    r = analyze(h, F, G, q, verbose=False); n += 1
    if r > mx: mx = r; ex = (h, F, G, q)
print(sys.argv[1], 'sets', n, 'max tripod cycle rank', mx, ex)
