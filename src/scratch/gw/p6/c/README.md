# P6c reproducible artifacts

All computation ran on fejer, `~/wilf/p6c`, with nice 10 and no more
than two simultaneous single-core jobs. No prior P6 report was edited.

The statements and complete proofs are in `../P6C_REPORT.md`.

- `checks.py`: integer actual-tile checks of window, cone, upper-arc,
  missing-degree and partial-row lemmas, including sharp failures.
- `digital.py`: mixed-radix products at heights 2--7, all phases,
  including spike lifts; exact CR family polynomial.
- `stress.py`: F3, the k=5 carry stress case, and balanced digital stars.
- `degree_check.py`: the uniform multi-cubic degree-defect theorem.
- `matching6.c`: exhaustive 6-unit-set and missing-matching search.
- `matching6_independent.py`: independently pruned fixed-shape DFS.
- `milp_hc.py`: adversarial shape optimization, with exact checking of
  every incumbent. MILP status is explicitly recorded; this is not a
  proof over all unit labelings.
- `audit.py`: saved-result audit, polynomial checks, full sharp witness
  data and SHA256 manifest. The manifest excludes live audit logs;
  the report hash is stored separately in `P6C_AUDIT.json`.

Use the commands in report section 12 from fejer. Python is
`~/mathenv/bin/python`; no sympy is used. The C program builds with
`nice -n 10 cc -O3 -o matching6 matching6.c`.

Failure preservation: the face-free positive-slack bound is refuted by
an infinite digital family; OW+B>=0 even for one cubic is refuted at
the smallest possible modulus 17; an incorrect spike top-form formula
has its smallest height-three failure at m=5 (also checked at m=9).
None is a MaxCL counterexample.
