# U = T near-equality family check: A = {mu, 3mu, 5mu} u [5mu+1, 6mu-2], m = 6mu-1 (|A| = mu+1)
import importlib.util, sys
spec = importlib.util.spec_from_file_location('fam', sys.argv[1]); fam = importlib.util.module_from_spec(spec)
src = open(sys.argv[1]).read().split('for d in range')[0]; exec(src)
for mu in range(4, 16):
    A = [mu, 3 * mu, 5 * mu] + list(range(5 * mu + 1, 6 * mu - 1)); m = 6 * mu - 1; d = len(A); e = d + 1
    r = stats(A, m)
    if r is None: print(mu, 'not covering'); continue
    c, l, ne = r
    print(f"mu={mu} d={d} m={m} c={c} l={l} U!=T={ne} e*l-c={e*l-c} ratio={e*l/c:.4f} (d+1)/(d-1)={(d+1)/(d-1):.4f}")
