"""T1 counterexamples (E340): ANCHOR, WR1 and the pool split on given P18 models. Usage: python t1cex.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.argv = ["wrself.py", "none"]
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "wrself.py")).read().split("mode = sys.argv[1]")[0]
exec(src.replace("__import__('os').path.dirname(__file__)", "'" + os.path.dirname(os.path.abspath(__file__)) + "'"))
for (m, rho, B, q) in [(66, 4, [1, 5, 6, 32, 37, 62], 5), (61, 10, [1, 2, 6, 27, 28, 51], 5), (64, 2, [1, 5, 11, 31, 36], 6)]:
    s = split(m, rho, B, q)
    print(m, rho, B, q, "E", s['E'], "r", s['r'], "J-C", s['JC'], "T1", rho + s['r'] - s['JC'],
          "ANCHOR", rho + s["r"] + s["Pq1"] - s["JC"], "WR1", s["PW"] + rho + s["r"], "T2", rho + s["r"] + s["PWq1"] - s["JC"], "P_W", s["PWid"], "PU", s["PU"])
