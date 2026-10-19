"""Lead re-check of the THREE-CUBICS finite bases with lcr_check2: k=4 (m=21), k=5 (m=31,32), k=6 (m=43,44,45);
all pairs present, t=2 cubics, p=2 non-maximal pairs, the two face types {x0^3,x1^3} and {x0^3,x0^2 x1}.
Also ONE-CUBIC k=4 (pure cube, m=21..27) and the k=4,t=4 binary face (m=21..24). Output: lcr_check2 case lines."""
import sys, itertools
def cells(k, T):
    units = [tuple(int(i == a) for i in range(k)) for a in range(k)]
    pairs = sorted(set(tuple(u[i]+v[i] for i in range(k)) for u in units for v in units))
    return units, pairs, T
def mono(k, idx): v = [0]*k; [v.__setitem__(i, v[i]+1) for i in idx]; return tuple(v)
def emit(k, m, T):
    units, pairs, T = cells(k, T)
    s = m - (1+k+len(pairs)+len(T))
    if s < 0: return
    d = k+s
    def below(z, y): return all(z[i] <= y[i] for i in range(k))
    out = [("0"*k, d+1)]
    for u in units: out.append(("".join(map(str, u)), d+1))
    for z in pairs: out.append(("".join(map(str, z)), d+1 if any(below(z, y) for y in T) else -1))
    for y in T: out.append(("".join(map(str, y)), -2))
    print(m, s, len(out), " ".join("%s:%d" % c for c in out))
mode = sys.argv[1]
if mode == "two":
    for k, ms in [(4, [21]), (5, [31, 32]), (6, [43, 44, 45])]:
        for m in ms:
            emit(k, m, [mono(k, [0, 0, 0]), mono(k, [1, 1, 1])]); emit(k, m, [mono(k, [0, 0, 0]), mono(k, [0, 0, 1])])
elif mode == "one4":
    for m in range(21, 28): emit(4, m, [mono(4, [0, 0, 0])])
elif mode == "bin4":
    for m in range(21, 25): emit(4, m, [mono(4, [0, 0, 0]), mono(4, [0, 0, 1]), mono(4, [0, 1, 1]), mono(4, [1, 1, 1])])
