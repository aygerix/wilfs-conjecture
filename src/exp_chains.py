"""Experiment E4: per-direction deficiencies in Identity CH.
C = m(m-1)/2.  Wilf <=> sum_a (C - Def_a) <= C + E.
Test strengthenings:
  S1: sum_a (C - Def_a)^+ <= C + E
  S2: sum_a (C - Def_a)^+ <= C
  S3: Def_a >= C - (p_a mod m)*?  (just record extreme ratios)"""
import sys
sys.path.insert(0, 'src')
from ns import all_by_genus
from chains import chain_data
G = int(sys.argv[1]) if len(sys.argv) > 1 else 16
f1 = f2 = n = 0
ex1, ex2 = [], []
minratio = (9, None)
for g, s in all_by_genus(G):
    if s.m <= 2:
        continue
    cd = chain_data(s)
    C = s.m * (s.m - 1) // 2
    defic = [max(0, C - D) for D in cd['Defs']]
    n += 1
    if sum(defic) > C + cd['E']:
        f1 += 1
        if len(ex1) < 5: ex1.append((s.P, cd['Defs'], cd['E'], C, s.W))
    if sum(defic) > C:
        f2 += 1
        if len(ex2) < 5: ex2.append((s.P, cd['Defs'], cd['E'], C, s.W))
    r = min(cd['Defs']) / C if cd['Defs'] else 9
    if r < minratio[0]:
        minratio = (r, s.P, cd['Defs'], C)
print(f'genus<={G}, m>=3: {n} semigroups; S1 fails {f1}; S2 fails {f2}')
print('S1 examples', ex1)
print('S2 examples', ex2)
print('min Def_a / C:', minratio)
