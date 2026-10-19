# P6b reproducibility

Full proofs, quantifiers, finite bases and remaining family are in
[`../P6B_REPORT.md`](../P6B_REPORT.md). The full height-three MaxCL theorem
remains open. The accepted P6 report is unchanged.

All calculation ran on fejer, `~/wilf/p6b`, nice 10, at most four owned
single-core jobs. No local numerical computation and no commits.

The proof artifacts are:

- `core3.c`, `shape3.py`, `core3_independent.py`: H3-CORE3, all phases,
  unbounded spike count. Analytic CR classification plus three small loops.
- `dense_poly.py`, `generic_density.py`, `certificate_tables.py`: exact
  rational expansions and shifted positive coefficients for DENSE9 and
  DENSE075. Lower-order terms are retained; the statements are uniform in k.
- `one_cubic4.c`, `one_cubic4_independent.py`: ONE-CUBIC finite base.
- `few_poly.py`, `two_cubic45.py`, `two_cubic6.c`,
  `pair6_independent.py`: THREE-CUBICS over complete quadratic faces,
  including the corrected k=4,m=21 two-cubic base.
- `shadow_cover.c`: exhaustive check of SHADOW-COVER on every loop graph
  through six vertices. The unbounded proof is algebraic, in the report.
- `packing_checks.py`: exact checks on actual cores completed by spikes;
  includes E47/E51, composite moduli, dense and sparse cubic faces, the
  actual CR-table correction and an actual failure of CR/FLAT-CR exhaustion.
- `frontier_search.py`: full k=4 quadratic faces with binary cubic faces,
  m=21..24; no injective extension. This is used for the small t=4 corollary.
- `frontier_two5.py`: adversarial search that exhibits a true tile with
  CR=-12, FLAT-CR=-83, but minimum MaxCL slack 473. Its finite domain is
  also covered by `two_cubic45.py`; it is not a MaxCL counterexample.
- `adversary_min.py`: the smallest-modulus CR/FLAT-CR exhaustion failure
  with k>=4,d>=6, at m=16; 405 relaxed smaller profiles certify minimality.
  Its actual minimum MaxCL slack is 78.
- `audit_p6b.py`: range/count/certificate/witness cross-checks, with results
  in `P6B_AUDIT.json` and source/data digests in `SHA256SUMS`.

All `.log` and `.json` outputs are saved beside their sources. The report
gives full commands. Python uses only the standard library; all arithmetic
is integral or `fractions.Fraction`. No numerical optimizer is used.

The audit is run on fejer after the substantive checks complete. From its
flat remote directory, pass `P6B_REPORT.md` as the report argument. If the
repository layout is copied to fejer, run from this `b` directory with
`../P6B_REPORT.md` instead. The report's content digest is recorded in the
audit JSON; the checksum manifest covers the files in `b` and excludes
the open audit stdout log and generated audit summary.

```sh
nice -n 10 ~/mathenv/bin/python audit_p6b.py ../P6B_REPORT.md > audit.log
sha256sum -c SHA256SUMS
```

No new result here is claimed to have been imported into the Lean kernel.
