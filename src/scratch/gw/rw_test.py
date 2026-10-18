# Decoupled sufficient condition for Wilf (any e). W = max_y F(y), F(y) = Lev(y) + Car(y), so W >= F(y_r) with
# y_r = argmax_D x.r. Hence Wilf <== (RW) B(D,r) >= (d-1)m(m-1)/2   [Car(y_r) >= 0; B(D,r) = d m max(x.r) - (d+1) sum x.r]
#                              and (LV) Lev(y_r) = d m (y_r.k) - (d+1) sum x.k >= 0.
# RW is equality for carry-free tiles ({x.r} = {0..m-1}). Test RW and LV on random S.
import sys, random; sys.path.insert(0, 'src')
from ns import NS
from cl import factorizations_down_set
rnd = random.Random(int(sys.argv[1])); N = int(sys.argv[2]); E0, E1, M0, M1, K = map(int, sys.argv[3:8])
st = {}; worst = {}
for _ in range(N):
    e = rnd.randint(E0, E1); m = rnd.randint(max(M0, e + 1), M1)
    try: s = NS.from_generators([m] + rnd.sample(range(m + 1, K * m), e - 1))
    except Exception: continue
    if s.e != e: continue
    P, best = factorizations_down_set(s, 'grlex'); D = list(best.values()); d = len(P)
    k = [p // m for p in P]; r = [p % m for p in P]
    if 0 in r: continue
    dot = lambda x, v: sum(a * b for a, b in zip(x, v))
    yr = max(D, key=lambda x: (dot(x, r), dot(x, k)))
    Br = d * m * dot(yr, r) - (d + 1) * sum(dot(x, r) for x in D); tgt = (d - 1) * m * (m - 1) // 2
    LV = d * m * dot(yr, k) - (d + 1) * sum(dot(x, k) for x in D)
    rw = Br - tgt
    t = st.setdefault(e, [0, 0, 0, 0]); t[0] += 1; t[1] += rw < 0; t[2] += LV < 0; t[3] += (rw >= 0 and LV >= 0)
    if rw < 0 and (e not in worst or rw / tgt < worst[e][0]): worst[e] = (round(rw / tgt, 4), s.P, rw, LV, s.W)
for e in sorted(st):
    t = st[e]; print(f"e={e}: {t[0]} S | RW fails {t[1]} | LV fails {t[2]} | both hold (=> Wilf) {t[3]} | worst RW (rel, gens, RW-excess, LV, W): {worst.get(e)}", flush=True)
