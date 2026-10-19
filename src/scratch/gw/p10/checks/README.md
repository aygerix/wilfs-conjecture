# P10 check outputs

All commands below run on fejer in `~/wilf/p10/e5/`, with sources copied from the parent directory in this repository. Copy the local `shape_scan.c` as `shape_scan_v5.c`; the other filenames stay the same. No mathematical computation ran on the laptop.

```sh
nice -n 10 cc -O3 shape_scan_v5.c -lz -o shape_scan_v5
nice -n 10 ./shape_scan_v5 5 39 ~/wilf/tile4/src/scratch/tile4 > shape_scan_v5.log
nice -n 10 ~/mathenv/bin/python boundary.py --count 1200 --seed 1019 > boundary_test.log
nice -n 10 ~/mathenv/bin/python boundary.py --count 1600 --seed 1020 > boundary_test2.log
nice -n 10 ~/mathenv/bin/python two_refined.py > two_refined_final.log
nice -n 10 cc -O3 two_verify.c -o two_verify
nice -n 10 ./two_verify > two_verify.log
nice -n 10 cc -O3 support2_fin.c -o support2_fin_v2
nice -n 10 ./support2_fin_v2 > support2_fin_v2.log
nice -n 10 ~/mathenv/bin/python families.py > families_v2.log
nice -n 10 ~/mathenv/bin/python stress.py > stress.log
nice -n 10 ~/mathenv/bin/python obstructions.py > obstructions.log
```

The local `shape_scan.c` is the final v5 source. `boundary_test.log` predates addition of the axis inequality; `boundary_test2.log` includes it. Both contain every other boundary check. `two_refined_final.log` and `two_verify.log` are independent implementations of the same 64–143 certificate. The 60–63 rows of `support2_fin_v2.log` complete the support-two theorem; its earlier rows are preserved unsuccessful relaxations.

Exploratory `two_certificate.py` and the earlier 40–224 version of `two_refined.py` are not required for the final theorem. Their negative relaxed profiles are not semigroup counterexamples.

Fejer software: Python 3.12.3; GCC 13.3.0 on Ubuntu 24.04. `shape_scan_v4.log` is retained as an earlier run; v5 adds the continuous face bound, TYPE4 and placed-face rank/axis checks.
