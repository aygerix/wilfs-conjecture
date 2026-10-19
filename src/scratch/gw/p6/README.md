# P6: height-three MaxCL

Theorems, complete arguments, finite domain, preserved failures and exact
remaining family are in [P6_REPORT.md](P6_REPORT.md). The full height-three
MaxCL conjecture remains open.

Proved results here:

- H3-D5: all phases, height <=3, at most five active directions; a finite
  certificate. Semigroup consequence: height-three Apéry sets with e<=6.
- H3-CORE2: all phases and arbitrarily many spikes when at most two unit
  directions are non-maximal; paper proof for m>=14 plus a finite base.
- PAIR-ZERO and CENTERED-PAIR: explicit sufficient carry regimes in arbitrary
  active dimension; UNIT-LOAD-0 and PSI3 give additional phase-zero classes.

All calculation ran on fejer, `~/wilf/p6`, nice 10, at most four owned
single-core jobs. No commits and no local numerical computation.

## Files

- `height3_certificate.c`: full residue-vector/pair-face enumeration, d=2..5,
  m<=C(d+3,3). Method 0 uses unions of cubic choices; method 1 enumerates
  feasible pair containers. It does not normalize by multiplication in Z/m.
- `coverage.c`: separate covering-vector count at d=5.
- `independent_small.py`: independent explicit construction of every actual
  tile in the full d=2,3 domains; no DP or container optimization.
- `core2.py`: all cubic cores of dimension <=2, every m<14, every injective
  core labeling and every phase, with the correct ambient spike dimension.
- `charging_checks.py`: independent Apéry construction; exact identities,
  carry-window bounds, centered bounds, unit loads, and phase-boundary checks;
  includes E47/E51 and named tight examples.
- `failure_checks.py`: exact smallest examples for the false carry range,
  the two-base no-carry assertion and forced-only payment; E47 and centered
  example numerical identities.
- `milp_adversary.py`: heuristic search over arbitrary height-three tiles
  in d=6..12. Floating solver results are not universal certificates;
  every incumbent's actual tile and all phase slacks are checked exactly.
- `audit_p6.py`: parameter-domain, count, cross-method, independent-check and
  witness audit. `P6_AUDIT.json` records its results; `SHA256SUMS` records
  the substantive sources and data. The audit's own open stdout log is
  excluded from its checksum manifest.

All `.log` and `.json` outputs are retained alongside their sources.
The report's section 10 gives every command. Python is `~/mathenv/bin/python`;
only the MILP adversary requires numpy/scipy. The C certificate and all
mathematical witness checks use exact integer arithmetic.

For a short verification after copying the directory back to fejer:

```sh
cd ~/wilf/p6
nice -n 10 ~/mathenv/bin/python failure_checks.py
nice -n 10 ~/mathenv/bin/python audit_p6.py
```

The raw finite checks are complete within their stated dimensions; random
and optimization searches are labeled evidence. None is a claim of a
general height-three proof or a Lean kernel check of the new finite theorem.
