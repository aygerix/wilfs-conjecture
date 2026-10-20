# Seeds for rl2s: B_3 A-cores of the codex P14 simplex family (h = 8T+9, m = 3h+1, t = 4T+5+4y), k = |Y| = 3..7.
import itertools
def b3(y):
    s = [sum(x) for x in itertools.combinations_with_replacement(y, 3)]
    return len(s) == len(set(s))
for k in range(3, 8):
    Y = [0]; v = 1
    while len(Y) < k:
        if b3(Y + [v]): Y.append(v)
        v += 1
    T = max(Y); h = 8 * T + 9; m = 3 * h + 1; t = [4 * T + 5 + 4 * y for y in Y]
    print(k, m, ','.join(str(m + u) for u in t))
