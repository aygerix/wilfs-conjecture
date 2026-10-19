# P5f: uniform scaling and retained pair information

Appendix: P5_REPORT.md §§52--59. No commits. Every mathematical
calculation ran on fejer, in `~/wilf/p10`, with nice 10 and at most
two single-core jobs at once. No a=19 enumeration or ambient P search.

Proved on paper: LOW-CUBIC/CE-LINEAR, LARGE-A2 (`a>=16Q_alpha`),
MIX-BUDGET, B-SQRT, SPARSE-COVER and HPAIR. The continuous system
and the polynomial certificates concern necessary count relaxations;
their negative formal W values are not Wilf counterexamples.

Files:

* `algebra_checks.py`: exact Macaulay block grid and LARGE-A2 endpoints.
* `polynomial_certificates.py`: a standalone sparse rational polynomial
  ring, with 168 slack certificates for four infinite profile families,
  and 24 for the B-heavy loop family. It also checks the three B-heavy
  equalities and ten rational constant comparisons.
* `scaling_profiles.py`: independent integer evaluation of 16 specified
  profiles; it reads just the helper definitions from P5e
  `frontier_counts.py`, replacing its bounded Macaulay routine by an
  unbounded binary-search implementation.
* `instance_checks.h`, `uniform_semigroups.c`: actual semigroup checks
  of the new quartic and HPAIR statements, in addition to P5e checks.
  The proposed A range need not equal the actual A count after closure.
* `audit_p10.py`: verifies the output records and produces the audit
  and SHA256 inventory on fejer.

All exported JSON coefficient lists are ordered by increasing power
of X. Nonnegative coefficients prove nonnegativity for every X>=0.
Zero coefficients and zero polynomials are allowed. These are direct
polynomial expressions, not interpolations of sampled outputs.

Remote reproduction (P5e sources in `../p9`):

```sh
cd ~/wilf/p10
cp ../p9/multi_low.h ../p9/two_low.h .
nice -n 10 ~/mathenv/bin/python algebra_checks.py > algebra_checks.log
nice -n 10 ~/mathenv/bin/python polynomial_certificates.py > polynomial_certificates.log
nice -n 10 ~/mathenv/bin/python scaling_profiles.py ../p9/frontier_counts.py > scaling_profiles.log
nice -n 10 gcc -O2 uniform_semigroups.c -o uniform_semigroups
nice -n 10 ./uniform_semigroups 2026101961 3000 200 6000 4 0 7 > instances61.log
nice -n 10 ./uniform_semigroups 2026101962 2000 1000 9000 8 1 24 > instances62.log
nice -n 10 ~/mathenv/bin/python audit_p10.py
```

The audit expects the final report copied to `P5_REPORT.md` in the
remote working directory. Its inventory maps that copy to
`../P5_REPORT.md`, and maps the unchanged helper/header dependencies
to their sibling `../t5/` paths. Locally, compile with `-I../t5` if
the headers have not been copied beside the driver. Run computation
on fejer only, as instructed by the lead.

`logs/preliminary_profiles.log` is preserved as a failure record:
the first choice of h passed derived payments but violated raw arc
occupancy. It is not an input to a theorem. The corrected profiles
include both raw arcs, the low-loop range and END failure.

The sampler found no deficient A face at a>=24. Accordingly its
LOW-CUBIC conditional control and LARGE-A2 conditional control are
vacuous on these two runs. HPAIR has 4,941 nonvacuous cases and
4,555 strict improvements. The large-parameter results have paper
proofs and exact arithmetic checks, rather than a claim of actual
frontier examples in these samples.
