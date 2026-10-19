# P5g ambient and retained-pair packing

All calculations ran on fejer, in `~/wilf/p11`, nice 10, no more than two
owned single-core calculations at a time. No commits. The report is
`../P5_REPORT.md` sections 60--67; statements there distinguish proved
lemmas with explicit structural hypotheses from the still-open full P(C)
and ambient MATCH-P.

- `weak_check.c`: exhaustive weak Sidon sets of size at most 8 in 40 integers;
  checks difference multiplicities, repeated cubics and signed-label counts.
- `matching_check.py`: all normalized sets in 15 integers, n=2..7, and all
  retained-pair matching states that have injective retained pair sums.
- `planted_search.c`: adversarial annealing preserving 11 or 16 disjoint
  equal-sum triples and all pair sums; heuristic search, exact final counts.
- `independent_checks.py`: independent enumeration of planted witnesses;
  checks of both SF-M bounds, including the weak heavy-fibre example;
  rational constants and polynomial coefficients for the primary applications.
- `antipodal.py`: exact checks of the infinite counterfamily to the SUPPORT
  strengthening of MATCH-P. This is not an ambient MATCH-P counterexample.
- `ambient_semigroups.c` and `p5g_checks.h`: actual semigroup checks. The former
  is the P5f scanner with the new core checks added. The three unchanged
  dependency headers are snapshotted unchanged in `deps/`; their hashes are
  recorded by the audit. Originals are in ../t5 and ../t6 locally and
  ../p10 on fejer.
- `*.log`, `planted_verified.json`, `weak_heavy_verified.json`: exact output
  and complete integer witnesses.
- `AUDIT.json`, `SHA256SUMS`: final feasibility/count audit and file digests.

Reproduce on fejer after copying this directory's sources to `~/wilf/p11`:

```sh
cd ~/wilf/p11
nice -n 10 gcc -O2 planted_search.c -lm -o planted_search
nice -n 10 ./planted_search 2026101971 11 0 4000 200000 2 47 > planted11.log
nice -n 10 ./planted_search 2026101972 16 0 13000 200000 2 47 > planted16.log
nice -n 10 gcc -O2 weak_check.c -o weak_check
nice -n 10 ./weak_check 40 8 > weak40.log
nice -n 10 ~/mathenv/bin/python matching_check.py > matching.log
nice -n 10 ~/mathenv/bin/python antipodal.py > antipodal.log
nice -n 10 ~/mathenv/bin/python independent_checks.py > independent.log
nice -n 10 gcc -O2 -Ideps ambient_semigroups.c -o ambient_semigroups
nice -n 10 ./ambient_semigroups 2026101973 1500 300 4000 5 0 12 > instances_lex.log
nice -n 10 ./ambient_semigroups 2026101974 1000 600 5000 7 1 19 > instances_grlex.log
nice -n 10 ~/mathenv/bin/python audit_p11.py
```

Python is `~/mathenv/bin/python`; it uses only the standard library.
No unproved P(C) is used in an unconditional conclusion. In particular,
the SF-G theorem caps all ordinary squarefree fibres, and RET-G caps all
legal squarefree fibres, including absent cubics. Present-fibre
injectivity by itself is not this hypothesis.
