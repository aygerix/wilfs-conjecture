# P14 computational record

All commands involving mathematics run on fejer in `~/wilf/p14`.
The laptop is used to edit/read/copy files. No commits. Raw output
is retained under `results/`; executables are rebuilt from source.
The relative filenames below refer to the remote directory. The
environment used GCC 13.3.0 and `~/mathenv/bin/python` 3.12.3.

Copy the C/Python sources from this directory to `fejer:~/wilf/p14/`
with `gcloud compute scp --zone us-east1-b`. Run each block remotely
using `gcloud compute ssh fejer --zone us-east1-b --command '...'`.
For example:

```sh
gcloud compute ssh fejer --zone us-east1-b --command 'cd ~/wilf/p14 && nice -n 10 ./tree 28 >tree28.log 2>&1'
```

The complete deterministic checks are:

```sh
cd ~/wilf/p14
nice -n 10 cc -O3 tree.c -o tree
nice -n 10 ./tree 28 >tree28.log 2>&1
nice -n 10 cc -O3 tree5.c -o tree5
nice -n 10 ./tree5 28 >tree5_28.log 2>&1
nice -n 10 cc -O3 graph_check.c -o graph_check
nice -n 10 ./graph_check >graph_check.log 2>&1
nice -n 10 ~/mathenv/bin/python simplex_e.py >simplex_e.log 2>&1
nice -n 10 ~/mathenv/bin/python simplex_search.py >simplex_search.log 2>&1
nice -n 10 cc -O3 -DMM=8192 verify_gens.c -o verify_gens
nice -n 10 ./verify_gens <simplex_e_gens.txt >simplex_e_C.log
nice -n 10 ./verify_gens <simplex_e_small_gens.txt >simplex_e_small_C.log
nice -n 10 cc -O3 seeds.c -o seeds
nice -n 10 ./seeds >seeds.log 2>&1
nice -n 10 cc -O3 structured.c -o structured
nice -n 10 ./structured 2500 140414 >structured.log 2>&1
```

`seeds` has the fixed RNG seed 140061 in its source. It generates
`seed_101.txt`, `seed_211.txt`, `seed_401.txt`; copies are retained
in `results/`. The inability to find an m=61 seed is not a proof
of nonexistence. `simplex_e.py` and `simplex_search.py` have no
randomness.

The final three annealers were run concurrently, with exactly
these arguments and at most three single-core jobs:

```sh
nice -n 10 cc -O3 search.c -lm -o search_final
nice -n 10 ./search_final 101 4 50000 4 1401101 0 0 seed_101.txt >repro101.log 2>&1
nice -n 10 ./search_final 211 3 40000 5 1401211 0 0 seed_211.txt >repro211.log 2>&1
nice -n 10 ./search_final 527 1 50000 4 1401527 1 1 >repro527.log 2>&1
```

They can also be rerun sequentially. Arguments are multiplicity,
starts, steps per start, objective, RNG seed, sparse flag, shaped
flag, optional initial Apéry file. The sparse flag enforces 3e<m;
the shaped flag enforces a>=19, alpha>=6. A seed file additionally
enforces R_A>p_A. Every run has q=4 as a hard constraint. Objective
4 is the relay slack with a +10 penalty if R_A=0; objective 5 is
the ratio (Lambda+C_U)/(R_A-p_A). Every candidate's actual relay
is checked for negativity before accepting/rejecting a mutation.

Finally:

```sh
nice -n 10 ~/mathenv/bin/python independent.py >independent.log 2>&1
```

For byte-identical input coverage, first copy the retained exploratory
logs `kunz101.log`, `generators181.log`, `kunz527_shaped.log`,
`kunz101_seed.log`, `kunz211_seed.log`, `kunz101_ratio.log` from
`results/` into the remote working directory. The independent
checker re-evaluates the final generator witness of every available
log; it does not use a printed invariant as input. It then runs its
1,200 attempts with fixed seed 140014 and both SINGLE-E examples.
These earlier search snapshots are preserved as exploratory output;
their arbitrary old CLI RNG seeds were not separately logged. The
CONFIG runs above are the fully specified search repetitions.

The checker writes `independent.json`. It uses `check_p13.py`, an
unchanged copy of the P13 Python checker, for heap Dijkstra, factor
counts and literal chain traversal. It separately computes the
quadratic fiber credits, C/E formulas, support bounds, actual high-
pair graph and low links, component costs, and depth-five classes.

For hashes after syncing the final report and commands:

```sh
nice -n 10 sha256sum core.h search.c gensearch.c structured.c seeds.c tree.c tree5.c graph_check.c verify_gens.c check_p13.py independent.py simplex_e.py simplex_search.py P14_REPORT.md COMMANDS.md results/* >SHA256SUMS.txt
nice -n 10 sha256sum -c SHA256SUMS.txt
```

All result counts, limitations of the samplers and the mathematical
scope are specified in `P14_REPORT.md`, Sections 9 and 10.
