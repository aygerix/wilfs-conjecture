"""Lead's independent checks of codex P8 (not reusing P8 code).
(a) NL: f(x,y) = x^3/8 - xy/2 + 5y^2/(2x) >= (1/2-y)/21 + 1/50000 on D = {0<x<=2, 0<=y<=1, x>=1/2+y, x^2+3y>=1/2}: dense float grid.
(b) SHADOW-225 finite part: for 255<=k<=3249, h=9/4, every v in [ceil(k/2-5/4), k] and the real e-interval
    lo=ceil(max(v/2,(k^2/2-5k/4-v(v-1))/3)) <= e <= hi=floor(min(v(v+1)/2, kv-k^2/2+5k/4)),
    G(e) = F(v,e) - (Z0-e)^2/(2 a_h) > 0, F from its DEFINITION [C(qD,2)+(v+1)(X^2/(2v)-X/2)]/v, qD=v(v+1)/2-e, X=2e-v,
    a_h = h^2(k+1) - 2h(3-h), Z0 = k^2/2+9k/4+1+h(k+1)/2.  Exact Fractions; quadratic fitted from 3 exact evaluations.
usage: python p8_lead_check.py nl | shadow KMIN KMAX"""
import sys
from fractions import Fraction as Fr
from math import ceil, floor
def nl():
    best = None; N = 1500
    for i in range(1, N + 1):
        x = 2.0 * i / N
        for j in range(0, N + 1):
            y = 1.0 * j / N
            if x < 0.5 + y or x * x + 3 * y < 0.5: continue
            val = x**3 / 8 - x * y / 2 + 5 * y * y / (2 * x) - (0.5 - y) / 21 - 1 / 50000
            if best is None or val < best[0]: best = (val, x, y)
    # refine boundary x^2+3y=1/2 (the binding curve)
    for i in range(0, 200001):
        x = 0.5 + 1.5 * i / 200000
        y = (0.5 - x * x) / 3
        if y < 0 or x < 0.5 + y: continue
        val = x**3 / 8 - x * y / 2 + 5 * y * y / (2 * x) - (0.5 - y) / 21 - 1 / 50000
        if val < best[0]: best = (val, x, y)
    print("NL grid min (f - z/21 - 1/50000):", best)
def F(v, e):
    qD = Fr(v * (v + 1), 2) - e; X = 2 * e - v
    return (qD * (qD - 1) / 2 + (v + 1) * (X * X / (2 * v) - X / 2)) / v
def shadow(kmin, kmax):
    h = Fr(9, 4); worst = None; cnt = 0
    for k in range(kmin, kmax + 1):
        ah = h * h * (k + 1) - 2 * h * (3 - h); Z0 = Fr(k * k, 2) + Fr(9 * k, 4) + 1 + h * (k + 1) / 2
        G = lambda v, e: F(v, e) - (Z0 - e) ** 2 / (2 * ah)
        for v in range(ceil(Fr(k, 2) - Fr(5, 4)), k + 1):
            lo = ceil(max(Fr(v, 2), (Fr(k * k, 2) - Fr(5 * k, 4) - v * (v - 1)) / 3))
            hi = floor(min(Fr(v * (v + 1), 2), k * v - Fr(k * k, 2) + Fr(5 * k, 4)))
            if lo > hi: continue
            cnt += 1
            g0, g1, g2 = G(v, Fr(0)), G(v, Fr(1)), G(v, Fr(2))
            a = (g2 - 2 * g1 + g0) / 2; b = g1 - g0 - a  # G(e) = a e^2 + b e + g0
            assert a > 0
            ev = -b / (2 * a); e = min(Fr(hi), max(Fr(lo), ev))
            val = a * e * e + b * e + g0
            assert val == G(v, e)
            if worst is None or val < worst[0]: worst = (val, k, v, e)
        if k % 250 == 0: print("k", k, "intervals", cnt, "worst so far", float(worst[0]), worst[1:], flush=True)
    print("SHADOW range", kmin, kmax, "intervals", cnt, "min G", worst[0], "=", float(worst[0]), "at (k,v,e)=", worst[1:])
if sys.argv[1] == 'nl': nl()
else: shadow(int(sys.argv[2]), int(sys.argv[3]))
