# P7 reproducibility record

All computation was run on fejer.  The working directory is
`~/wilf/p7/wrapmax/`; its parent already contains earlier research files.
Every research job used `nice -n 10`, and at most two jobs were active at
once.  No processes belonging to the lead were changed, and no commits were
made.  Earlier P6 reports were left unchanged.

Commands below are run after `gcloud compute ssh fejer --zone us-east1-b`.
The sources and report are copied with `gcloud compute scp --zone us-east1-b`.

```sh
cd ~/wilf/p7/wrapmax
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1

nice -n 10 ~/mathenv/bin/python partial.py --mmax 9 --dmax 8 \
  > results/partial_all.log 2> results/partial_all.err

nice -n 10 cc -O3 -std=c11 -Wall -Wextra search.c -o search
nice -n 10 ./search 71019 1000000 150 10 results/search_best.json \
  > results/search.log 2> results/search.err

nice -n 10 ~/mathenv/bin/python optimize.py --seed 71020 --trials 200 \
  --mmax 100 --kmax 8 --spikes --out results/lp.jsonl \
  > results/lp.log 2> results/lp.err

nice -n 10 ~/mathenv/bin/python optimize.py --seed 71022 --trials 1000 \
  --mmax 180 --kmax 10 --cap 12000 --spikes --phases 8 \
  --out results/lp_fixed.jsonl > results/lp_fixed.log 2> results/lp_fixed.err

nice -n 10 ~/mathenv/bin/python sidon_counter.py --pmax 313 \
  --out results/sidon_counter2.json \
  > results/sidon_counter2.log 2> results/sidon_counter2.err

nice -n 10 cc -O2 -std=c11 -Wall -Wextra sidon_count.c -o sidon_count
nice -n 10 ./sidon_count 127 > results/sidon_count.json

nice -n 10 ~/mathenv/bin/python verify_counter.py results/sidon_counter2.json \
  > results/verify_counter.json 2> results/verify_counter.err

nice -n 10 ~/mathenv/bin/python verify_semigroup.py results/sidon_counter2.json \
  > results/verify_semigroup.json 2> results/verify_semigroup.err

nice -n 10 ~/mathenv/bin/python once_check.py \
  > results/once_check.json 2> results/once_check.err

nice -n 10 ~/mathenv/bin/python small_checks.py \
  > results/small_checks.json 2> results/small_checks.err
```

`sidon_counter.py` stops at its first negative construction, which occurs at
`p=127` in the specified scan.  The final witness uses `m=6L+2`.  The file
`results/sidon_counter2.json` contains the offset set, core residues, one
chosen factor triple per cubic, and every added spike label.  No dense list
of 111233 coordinates per cell is needed.  The independent verifier uses
sorted sparse factor lists and computes all upper-cover incidences.

The C count is a separate enumeration of pairs and triples, using integer
marker arrays.  `verify_semigroup.py` uses all m residues and every core
generator for its explicit shortest-path inequalities; its spike inequalities
are certified by an integer bound, as stated in the report.

Auxiliary, non-certificate runs are retained: `partial.log` used only
dimensions at most three; `dual_probe.jsonl` contains floating discovery
duals; `sidon_counter.log` was the initial scan through 103 with the valid
larger modulus `12L+2`.  The preliminary `lp_large` run aborted on a sampling
range error after 640 complete trials; the fixed sampler is the seed-71022
run above.  None of these auxiliary runs is used for the counterexample
proof.

Python and compiler versions, the final exact verifier outputs, and SHA-256
checksums are saved under `results/`.  NumPy/SciPy are used only on fejer;
the counterexample count and tile verification need no SciPy, no symbolic
algebra, and no unproved input.
