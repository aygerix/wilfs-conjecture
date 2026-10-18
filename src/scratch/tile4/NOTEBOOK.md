# Research software record — 2026-10-18

## Exact target and domain

For each m >= 5 and each primitive r in (Z/m)^4, enumerate every down-set
of minimum representatives for the cyclic kernel, for positive weights,
modulo units and coordinate permutations on r. Include zero/repeated
residues in the default domain; separately record the distinct-nonzero
sector necessary for four minimal non-m generators. Count tiles per
canonical lattice, rather than distinct shapes across different lattices.
Compute the exact rational HCR for every tile and list every value < 1.

## Frontier and discriminating tests

* PROVED (in README): strict minimal-non-element inequalities characterize
  the weight cone. Distinct tile cones have disjoint interiors. Minimum
  representatives have degree <= m-1. Grlex ties are realizable by finite
  positive perturbations; they introduce no additional lower-dimensional
  tile types. Hence exact cone volume sum 1 proves completeness.
* IMPLEMENTED: primitive integer projective vertices, clipping of 3-D
  polyhedra, symbolic facet flips, reverse facet matching, unbounded integer
  determinants and exact rational normalized volumes.
* VERIFIED: complete 3-D tile sets agree with the existing implementation
  for m=4..10, both intrinsically and as 4-D fans with unused coordinate 4.
  Unit/permutation orbit counts agree with exhaustive primitive tuples for
  m=2..7; all-domain sums equal the fourth Jordan totient.
* VERIFIED on fejer: 2,000 distinct random e=5 semigroups from the existing
  NS and grlex factorization code, seed 20261018, m=5..14. No missing tiles;
  311 boundary-weight cases. A separate all-supporting-plane intersection
  algorithm agrees with the clipped vertex sets for 1,193 cones. HCR
  agrees with the existing function for 2,494 tiles.
* EXPERIMENTAL: the first shape-criterion failures occur at m=13, two
  canonical lattice/tile pairs with HCR=112/117. Direct height-definition
  calculations and semigroup realizations independently verify them.
  They are not Wilf counterexamples (defects 27 and 36).

The exact gap for larger m is computational coverage, not a sampling or
floating-point geometry gap. Each saved certificate can be checked without
trusting the traversal. There is no claim of a universal HCR inequality or
of Wilf's conjecture from these finite computations.

## Strategic decisions and execution provenance

1. Rejected a modular volume sum as an unconditional completeness
   certificate: a rational defect can vanish in a finite field. Use exact
   Fraction sums and, independently, matched internal facet closure.
2. Kept the full primitive-vector domain requested by the gcd condition,
   while reporting the minimal-generator residue sector separately. This
   avoids silently excluding zero/repeated residues or silently identifying
   distinct coordinate-lattice orbits.
3. Kept integer geometry rather than calling a floating convex-hull/LP
   routine. Exact clipping was independently tested against intersection
   enumeration; redundant and nonsimple cuts are included in tests.
4. The project lead required all remaining computation on GCP fejer.
   All earlier local jobs were already stopped (their sessions no longer
   existed). SSH succeeded. The source and saved artifacts were copied to
   ~/wilf/tile4/ with the repository-relative layout. All future calculation,
   validation, enumeration, and certificate checking occurs there. Locally
   only reads, edits under this directory, and gcloud operations are used.
5. The approximately two-hour VM driver uses eight independent lattice
   workers, canonical-order certificate output, and a separate checking
   pass. `vm_status.json` and `vm_run.log` give actual progress; interrupted
   `.part` files supply no aggregate completeness claim.

The authoritative completed range is the intersection of `results_all_m.json`
and PASS `checked_all_m.json` files. The final `RESULTS.md`, CSV table and
full HCR failure JSON are generated on the VM and copied back. Extension
should reuse completed pairs and continue at the next multiplicity.

## Final completed range and handoff

The VM finalizer reports **PASS for every m=5..39**: 56,188 canonical
lattice classes, 9,532,388 lattice/tile pairs, and 309,906 non-two-face
pairs. Every saved lattice certificate has been checked in a separate
pass on fejer. The original 6,900-second VM job completed enumeration at
m=39 but exhausted its checking budget there; the remaining independent
check was rerun on fejer and passed all 4,662 lattices (768.378 seconds).
No local computation was used after the VM-only instruction.

There are exactly two HCR failures, both at m=13 with value 112/117;
their complete cells, canonical residues, independent height calculation,
and positive-Wilf-defect semigroup witnesses are in RESULTS.md and
hcr_failures_all.json. No other failure was found in the completed range.
The VM reran the 2,000-semigroup validation (311 ties), the original 3-D
comparison, the 1,193 enumerated-cone vertex checks, and the additional
adversarial audit (1,500 determinants, 300 polytopes, five corruptions).

FINAL_STATUS.json is the consolidated audit. artifact_manifest.sha256
records hashes of all complete result/certificate/check files, and the
source manifest records the exact software and imported project modules.
All final artifacts and logs were copied back into this directory. The
next multiplicity is 40; extend with vm_run.py --mmin 40 on fejer only.
