# P6d checks

All execution belongs on fejer, in `~/wilf/p6d`. Python is
`~/mathenv/bin/python` (3.12.3). These scripts use only its standard
library. Run each job with `nice -n 10`; do not exceed four owned
single-core jobs. No local numerical execution is needed.

The proof of ONE-RELAY in `../P6D_REPORT.md` is analytic, including its
small cases. The following runs audit its ingredients and the other
new statements. After copying these source files to fejer:

```sh
cd ~/wilf/p6d
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
nice -n 10 ~/mathenv/bin/python stress.py
nice -n 10 ~/mathenv/bin/python algebra.py
nice -n 10 ~/mathenv/bin/python weighted_pack_check.py
nice -n 10 ~/mathenv/bin/python window_h.py --trials 4000 --output window_h4000.json
nice -n 10 ~/mathenv/bin/python wpack_actual.py
nice -n 10 ~/mathenv/bin/python quartic_audit.py
nice -n 10 ~/mathenv/bin/python target_one.py --trials 200000 --output target_one200k.json
```

The seeds and exact construction policies are in the source. `stress.py`
contains all eight lead unpaid examples. `window_h.py` also includes the
mandatory E47/E51 binary cores, at every phase. The named deficit in
`wpack_actual.py` exercises A<m explicitly. The quartic audit distinguishes
the smallest all-phase witness from the smallest origin-phase witness.

The following are independent, now redundant, finite audits of the six
bases that remained before the hole-2 argument:

```sh
nice -n 10 cc -O3 -std=c11 -Wall -Wextra one_small.c -o one_small
nice -n 10 ./one_small
nice -n 10 ~/mathenv/bin/python one_small_check.py
```

Earlier necessary-profile diagnostics, superseded for MaxCL by the analytic
proof, can be reproduced in this order:

```sh
nice -n 10 ~/mathenv/bin/python one_moment.py --limit 100 --output one_moment100.json
nice -n 10 ~/mathenv/bin/python moment_cover.py
nice -n 10 ~/mathenv/bin/python one_reserve.py
nice -n 10 ~/mathenv/bin/python one_anchor.py
nice -n 10 ~/mathenv/bin/python local_pairpack.py
```

They enumerate count profiles, not realizable tiles. The saved profile JSON
must not be described as a remaining MaxCL frontier after ONE-RELAY.
Logs and outputs from the actual runs are in `results/`.
