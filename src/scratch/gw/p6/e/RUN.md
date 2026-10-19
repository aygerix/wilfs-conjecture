# P6e checks

All commands below run on fejer, in `~/wilf/p6e/e`. The accepted
`src/scratch/gw/p6/d/core.py` is copied to `../d/core.py`. Do not execute
the scripts on the laptop. Set `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1`
and use `nice -n 10`; at most four single-core jobs, including any other
owned jobs, may run concurrently.

The report is `../P6E_REPORT.md` in the repository layout. No commits.

```
nice -n 10 ~/mathenv/bin/python origin_probe.py --trials 12000 --seed 2026101972 --output results/origin_probe.json > results/origin_probe.log 2>&1
nice -n 10 ~/mathenv/bin/python verify.py --trials 3500 --seed 2026101973 --output results/verify.json > results/verify.log 2>&1
nice -n 10 ~/mathenv/bin/python algebra.py > results/algebra.json 2> results/algebra.err
nice -n 10 ~/mathenv/bin/python few_actual.py > results/few_actual.json 2> results/few_actual.err
nice -n 10 ~/mathenv/bin/python relay_check.py > results/relay_check.json 2> results/relay_check.err
```

* `payments.py`: exact new predicates and bounds, imported by checks.
* `origin_probe.py`: discriminating origin samples and stronger unproved
  candidate payments; seed and retained witnesses are in the JSON.
* `verify.py`: every phase of actual cores, with the eight required stress
  cores and E47/E51; no claim of exhaustive labeling enumeration.
* `algebra.py`: local carry exhaustion, exact rational identities,
  cutoff polynomials, and minimum forced-shape counterexamples.
* `few_actual.py`: twelve large-dimensional actual tiles at the
  `40t+8`, `72t+10` and `80t` bounds, with t=2..5; 12 phases each.
* `relay_check.py`: explicit maximum matchings and weighted zero-extension
  reservations at unit-zero phases; actual face-excess stress examples.

The finite local searches and the actual-instance samples have different
quantifiers. The analytic theorems are proved in the report.
