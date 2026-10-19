# P5e artifacts

All execution is on fejer, in `~/wilf/p9`, using nice 10 and at
most four owned single-core jobs. The report is `../P5_REPORT.md`,
§§42--51. No ambient packing conjecture is used in the finite
exclusion through a=18.

The completed full-domain checks are reproducible with:

```sh
nice -n 10 gcc -O3 frontier_counts.c -o frontier_final
P5E_EREPAIR=0 nice -n 10 ./frontier_final 14 16 > final14_16.log 2> final14_16.err
P5E_EREPAIR=0 nice -n 10 ./frontier_final 17 17 > final17.log 2> final17.err
P5E_EREPAIR=1 nice -n 10 ./frontier_final 17 17 > erepair17_20.log 2> erepair17_20.err
P5E_EREPAIR=1 nice -n 10 ./frontier_final 18 18 > erepair18.log 2> erepair18.err
mkdir -p python_link python_bounded16
(cd python_link && P5E_EREPAIR=0 P5E_QUADRATIC=0 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 nice -n 10 ~/mathenv/bin/python ../frontier_counts.py 14 15 > linked_python14_16.log)
(cd python_bounded16 && P5E_EREPAIR=0 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 nice -n 10 ~/mathenv/bin/python ../frontier_counts.py 16 16 > bounded16.log)
```

Historical filenames retain the initially requested ranges. The
uncached Python job completed a=14,15; its redundant continuation
was stopped. The completed bounded-loop Python a=16 job matches
all three C count columns exactly. Two slower redundant a=16
jobs and an optional GLOC-pruned continuation to a=17 were stopped.
The C `erepair17_20.log` job completed a=17 and was stopped before
finishing a=18; the latter was rerun separately as shown above.

`P5E_EREPAIR` controls a proved necessary bound, not a conjecture:
0 is the original exception allowance, 1 the degree-only repair,
2 the localized missing-pair repair, and 3 (default) the cover
composition bound. `P5E_QUADRATIC=0` disables only the optional
quadratic collision bound in the Python implementation. C uses it.
The a=18 proof uses the weaker level-1 C export of 90 hulls and
an independent level-3 Python replay:

```sh
nice -n 10 ~/mathenv/bin/python replay_profiles.py final17.log 17 > replay17.log
nice -n 10 ~/mathenv/bin/python replay_profiles.py erepair18.log 18 > replay18.log
```

`cover_14_17.log` retains an earlier five-hull a=16 relaxation.
Its replay is an additional check, not the full-domain dependency
of the a=16 proof:

```sh
nice -n 10 ~/mathenv/bin/python replay_profiles.py cover_14_17.log 16 > replay16.log
```

All hulls are count profiles, never asserted to be actual tiles.
The replay enlarges each exported survivor set to its first/last
interval, so zero replay survivors is a valid exclusion.

Other checks:

```sh
nice -n 10 gcc -O3 cover_graphs.c -o cover_graphs_final
nice -n 10 ./cover_graphs_final > cover_graphs.log
nice -n 10 ~/mathenv/bin/python p5e_identities.py > p5e_identities_final.log
nice -n 10 gcc -O3 b0_strip.c -o b0_strip
nice -n 10 ./b0_strip 40 > b0_strip.log
nice -n 10 ~/mathenv/bin/python b0_verify.py > b0_verify.log
nice -n 10 ~/mathenv/bin/python profile_witness.py > profile_witness.log
nice -n 10 ~/mathenv/bin/python matching_moduli.py > matching_moduli.log
```

Actual semigroup controls use `uniform_semigroups.c`, `multi_low.h`
and `two_low.h`. The four seeds and ranges are in §48. The final
`actual_hot5.log` checks HOT-WINDOW and E-REPAIR incidence/budget;
earlier logs correspond to the documented incremental checks.
`fast_certificate.py` is an optional acceleration using GW-26e
and analytically positive GLOC terms to prune the endpoint domain;
it is not needed for the completed full-domain comparisons.

`audit_p9.py` compares the completed outputs, validates graph and
B-free certificates, and checks the critical-hull replay. It writes
`AUDIT.json` and `SHA256SUMS`. The checksum paths match this local
layout, including `../P5_REPORT.md`. Run it remotely after copying
the final report there as `P5_REPORT.md`. Logs are stored under
`logs/` here and replay data under `data/`.

Preliminary failures are retained, including the false extension
of the old nonnegative B-neighbor guard to a=17. It failed on a
raw count-domain profile, not an actual residue-complete instance.
The correction and full data are in §48.

The lead's n=9 Ambient SP12 log was copied for provenance, not
rerun. The n=10 log was still empty at the last check. No ambient
conjecture or conditional numerical result is used in an
unconditional finite exclusion.
