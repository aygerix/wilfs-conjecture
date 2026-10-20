# P11 reproduction

All mathematical computation is on fejer, zone `us-east1-b`.
Working directory: `~/wilf/p11/primary/`. Existing `~/wilf/p11/` files are preserved.
Use at most four single-core jobs. No commits.

Upload the code and the planted P5g data, then run the following **on fejer**:

```sh
cd ~/wilf/p11/primary
nice -n 10 cc -O3 scan.c -o scan
nice -n 10 cc -O3 kunz.c -lm -o kunz
nice -n 10 ./scan 33 >scan.log 2>scan.err
nice -n 10 ./kunz 21 85 18000 8 1 0 >kunz85b.log 2>kunz85b.err
nice -n 10 ./kunz 22 257 12000 8 2 0 >kunz257b.log 2>kunz257b.err
nice -n 10 ./kunz 23 503 12000 8 2 0 >kunz503b.log 2>kunz503b.err
nice -n 10 ./kunz 31 320 30000 10 2 1 >kunz320high_nice.log 2>kunz320high_nice.err
nice -n 10 ~/mathenv/bin/python audit.py >audit.log 2>audit.err
nice -n 10 ~/mathenv/bin/python poly.py >poly.log 2>poly.err
nice -n 10 ~/mathenv/bin/python instances.py 71 2500 >instances.log 2>instances.err
nice -n 10 ~/mathenv/bin/python instances.py 72 0 60 targeted >targeted.log 2>targeted.err
nice -n 10 ~/mathenv/bin/python packing.py >packing.log 2>packing.err
```

`packing.py` expects `planted_input.json`, copied from
`src/scratch/gw/p5/t7/planted_verified.json`. This is input data, not newly discovered sets.

The `b`-suffixed Kunz runs use the corrected initialization. The original failed-start
logs are retained under their unsuffixed names and are **not** a nonzero census.
The recorded seed 31 run is the nice rerun, `kunz320high_nice.log`.

Kunz modes: 0 all exact-depth-four states; 1 additionally `3e<m`; 2 additionally
the original numeric residual and the Yang--Zhang exclusion `e(eta+2)<2m`.
Objective 0 maximizes nonzero Bulk, 1 seeks a negative high-generator RC term,
2 minimizes CHAIN/need. Evaluated mutations can repeat a state. `instances.py`
also reads saved start/best states and rebuilds their actual grlex tiles.

`results/` contains the checked outputs and checksums. The polynomial script uses
exact rational coefficient comparison; the finite rational grids are supplementary.
The all-parameter proofs are in `P11_REPORT.md`.
