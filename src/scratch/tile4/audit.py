#!/usr/bin/python3
"""Adversarial geometry and certificate checks; run only on GCP fejer."""
import sys
sys.dont_write_bytecode = True
import copy
import itertools as it
import json
import random
import socket
import time
from fractions import Fraction as F
import enumerate as e
from check_certificate import check_record
from validate import intersection_vertices


def leibniz(rows):
    total = 0
    n = len(rows)
    for p in it.permutations(range(n)):
        sign = (-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
        term = sign
        for i,j in enumerate(p):
            term *= rows[i][j]
        total += term
    return total


def rejected(record, m=5):
    try:
        check_record(m,record)
    except AssertionError:
        return True
    raise AssertionError('A corrupted certificate was accepted')


def main():
    assert socket.gethostname().split('.')[0] == 'fejer'
    e.install_budget(240)
    t0 = time.monotonic()
    rng = random.Random(884120261018)
    dets = geometries = 0
    for d in (2,3,4):
        for _ in range(500):
            rows = [tuple(rng.randrange(-100,101) for _ in range(d)) for _ in range(d)]
            assert e.determinant(rows) == leibniz(rows)
            dets += 1
    for _ in range(300):
        center = (1,2,3,5)
        cons = []
        while len(cons) < 8:
            v = tuple(rng.randrange(-5,6) for _ in range(4))
            value = e.dot(v,center)
            if value:
                cons.append(e.primitive(v if value > 0 else tuple(-x for x in v)))
        cons = tuple(cons)
        faces = e.polytope(cons,4)
        vertices = {x for _,f in faces for x in f}
        assert vertices == intersection_vertices(cons,4)
        volume = e.normalized_volume(faces,4)
        assert 0 < volume <= 1
        reversed_faces = e.polytope(tuple(reversed(cons)),4)
        assert {x for _,f in reversed_faces for x in f} == vertices
        assert e.normalized_volume(reversed_faces,4) == volume
        geometries += 1
    m,r = 5,(1,2,3,4)
    T = e.enumerate_lattice(m,r)
    record = dict(r=r,tiles=len(T),tuple_orbit=24,lattice_orbit=6,sorted_orbit=1,
                  tile_cells=[e.tile_record(D) for D in T],
                  cone_volumes=[str(data[2]) for data in T.values()])
    assert check_record(m,record)['tiles'] == len(T)
    tests = []
    bad = copy.deepcopy(record)
    bad['cone_volumes'][0] = str(F(bad['cone_volumes'][0])+1)
    tests.append(('wrong exact cone volume',rejected(bad)))
    bad = copy.deepcopy(record)
    bad['tile_cells'].pop()
    bad['cone_volumes'].pop()
    bad['tiles'] -= 1
    tests.append(('omitted tile',rejected(bad)))
    bad = copy.deepcopy(record)
    bad['tile_cells'].append(bad['tile_cells'][0])
    bad['cone_volumes'].append(bad['cone_volumes'][0])
    bad['tiles'] += 1
    tests.append(('duplicated tile',rejected(bad)))
    bad = copy.deepcopy(record)
    bad['r'] = (1,1,1,1)
    tests.append(('wrong cyclic lattice',rejected(bad)))
    bad = copy.deepcopy(record)
    bad['tile_cells'][0][0] = [100,100,100,100]
    tests.append(('invalid down-set cell',rejected(bad)))
    result = dict(status='PASS',execution_host=socket.gethostname(),
                  seed=884120261018,determinant_crosschecks=dets,
                  arbitrary_polytope_crosschecks=geometries,
                  corruption_rejection_tests=tests,seconds=round(time.monotonic()-t0,3))
    (e.HERE/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)


if __name__ == '__main__':
    main()
