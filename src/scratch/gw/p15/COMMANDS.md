# P15 exact computation and provenance

All mathematical computation is on fejer, `~/wilf/p15`, with GCC
and `~/mathenv/bin/python`; all jobs use `nice -n 10`. No commits.
The laptop only reads/edits/copies files. Copy this directory's
sources using `gcloud compute scp --zone us-east1-b`, and run the
following remotely with `gcloud compute ssh fejer --zone us-east1-b
--command 'cd ~/wilf/p15 && ...'`.

Initial two independent checks:

```sh
nice -n 10 ~/mathenv/bin/python first_check.py >first_check.log
nice -n 10 cc -O2 first_independent.c -o first_independent
nice -n 10 ./first_independent >first_independent.log
```

Complete dimension-two and dimension-three certificates:

```sh
nice -n 10 cc -O3 exhaust2.c -o exhaust2
nice -n 10 ./exhaust2 2 16 >exhaust2.log
nice -n 10 ~/mathenv/bin/python shape3.py >shape3.log
nice -n 10 cc -O3 exhaust3.c -o exhaust3
nice -n 10 ./exhaust3 <shape3.txt >exhaust3.log
```

The 2D generator enumerates all partition shapes of every size
<=m. The 3D generator enumerates all decreasing stacks of
partitions of every size <=13. Both C tests use all nondecreasing
residue vectors and every p; coordinate permutations of the
full shape lists cover the omitted residue-vector orders. Inactive
coordinates are allowed, as in Lemma U. All shapes are checked
for residue injectivity. These are certificates only over their
stated finite domains.

The adversarial search changes one residue, multiplies all
residues by a unit, adds/removes a maximal cell or swaps a
maximal cell for an admissible corner. All states remain order
ideals with injective residues. Its exact command is:

```sh
nice -n 10 cc -O3 ideal_search.c -lm -o ideal_search
nice -n 10 ./ideal_search 10 60 3 1200 150015 >ideal_search.log
```

It considers d=2,...,6, three starts per (m,d), 1,200 mutation
iterations per start, and scores the worst p over every shift.
The counters count valid proposed states, with repeats, rather
than distinct ideals. Greedy maximal and known binary-simplex
seeds are both used. It intentionally continues after finding
U failures to preserve smaller and larger witnesses.

Independent checks of the semigroup counterexamples:

```sh
nice -n 10 cc -O2 verify_case.c -o verify_case
nice -n 10 ./verify_case <case13.txt >case13_C.log
nice -n 10 ./verify_case <case14true.txt >case14true_C.log
nice -n 10 ~/mathenv/bin/python semigroup_checks.py >semigroup_checks.log
```

`verify_case` uses dense Dijkstra and literal integer counts in
C, with independent depth and chain-top traversal. It verifies
minimality of each supplied generator. It checks every shift
when m<=60 and the true shift otherwise.

`semigroup_checks.py` uses heap Dijkstra, independently extracts
minimal generators, computes literal depths/tops, computes J
and every sampled tail beyond m, and solves all required
below-poset capacitated bipartite matchings. It asserts the
direct down-set inequality for every matching failure. It
also checks lex-factorization order ideals, the cancellation
identity and K_semigroup<=K_ideal at every shift. Its random
seed is 150022, with 350 random/interval/truncation attempts
at m=10,...,127, plus the exact named and structured family
loops in the source. The script writes `semigroup_checks.json`.

Counterexample families and their independent C confirmations:

```sh
nice -n 10 ~/mathenv/bin/python families.py >families.log
for f in families/*.txt; do
  case "$f" in *_ap.txt) continue;; esac
  nice -n 10 ./verify_case <"$f" >"${f%.txt}_C.log" || exit
done
nice -n 10 ~/mathenv/bin/python audit.py >audit.log
```

The height family checks H=3,...,12,20,50. The height-three B3
family checks k=2,...,7, using the verified B3 prefixes of
{0,1,4,13,32,71,124}. Full generator files are retained.

Independent direct ideal checks and positive-lemma checks:

```sh
nice -n 10 ~/mathenv/bin/python verify_ideals.py >verify_ideals.log
nice -n 10 ~/mathenv/bin/python check_height3.py >check_height3.log
```

`verify_ideals.py` rechecks recorded annealing witnesses, the
explicit dimensions 2,...,6 examples, three dilute height
examples, and the squarefree six-variable counterexample,
using literal counts at every p. `check_height3.py` uses
seed 150033 and 3,000 random ideals of height <=3, including
noninjective residue vectors, to test the proved sharp error
bound, pair classification, pseudoforest case and squarefree
five-direction case. It writes only finite-check evidence;
the proofs are in P15_REPORT.md.

At most four single-core jobs may run simultaneously; the
above commands can all be run sequentially. For the retained
record, copy raw logs, JSON, input files and the `families/`
directory into `results/`, then generate and verify the
SHA256 manifest on fejer. Earlier report directories remain
unchanged.
