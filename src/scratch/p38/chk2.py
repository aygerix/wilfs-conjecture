# chk2: second check of the F0 examples with rayU0.evalS (Dijkstra-based Q5 test + W-mu terms, identity asserted)
exec(open('rayU0.py').read().split('rng = random.Random')[0])
for m, A in ((85, [3,46,47,50,52,58,59,65,76,83]), (86, [3,47,49,52,53,59,61,67,77,85]), (92, [3,50,52,56,58,68,70,77,82,89,91])):
    print(m, A, evalS(m, A))
