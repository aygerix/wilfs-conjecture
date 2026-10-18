# Exact four-coordinate Apéry tiles

All new software, saved certificates, validation inputs and results live here.
Run all computation on the GCP VM **fejer**, in `~/wilf/tile4/`, with the same
relative source layout as this repository. Locally only read/edit files in
this directory and use `gcloud` to transfer files or access the VM. Do not
execute even small Python tests on the laptop. No external mathematical
data or packages are downloaded. Use `/usr/bin/python3 -B` on the VM.
`-B` also prevents imports of existing project modules from creating files
outside this directory. No existing project file is modified.

## Domain and counts

For every integer m >= 5 we enumerate r in (Z/m)^4 with gcd(m,r)=1,
modulo multiplication by a unit and coordinate permutation. The default
`--domain all` includes zero and repeated residues, as the stated gcd condition
requires. `--domain minimal` restricts to distinct nonzero residues, the
necessary residue condition for four minimal non-m semigroup generators.
Every default result also gives the lattice and tile counts of that sector.
Counts are sums of tiles over canonical lattices; geometrically identical
shapes in different lattices are counted separately. All positive-weight
tiles are counted, including those with an unused coordinate.

For each canonical sorted r, let O be its orbit of sorted tuples under units,
and let c_j be the multiplicities of its entries. Its ordered residue-vector
orbit has size |O|*4!/product(c_j!). The unit action on primitive vectors is
free: if (u-1)r_i=0 mod m for every i, Bézout and gcd(m,r)=1 imply u=1 mod m.
Consequently the number of distinct kernels in the coordinate-permutation
orbit is the ordered vector orbit size divided by phi(m). Both sizes are
saved for each lattice. Their sums are checked against the fourth Jordan
totient m^4*product_{prime p|m}(1-p^-4).

“Non-two-face” uses the existing scan's missing-pair convention, extended to
four coordinates: all six e_i+e_j must belong to D. A missing pair means the
down-set lies in the union of the two coordinate hyperplanes x_i=0 or x_j=0.
HCR is computed over **every** tile, without restricting to non-two-face
tiles. It is exactly the rational formula in `src/scratch/hcr_shape.py`;
the original function returns a float, while this implementation never uses
floating point for HCR comparisons or minima.

## Geometry and enumeration

For every residue, Dijkstra minimizes `(p.x, secondary.x, |x|, x)` using
integer weights and Python's unbounded integers. Primary edge weights are
strictly positive, even when secondary weights are negative. Lexicographic
edge weights therefore remain positive. A minimum path has no repeated
residue, so every tile exponent has degree at most m-1. This also proves
finiteness of the possible tiles.

From a down-set D of size m with distinct residues, compute the minimal
non-elements q and the inward inequalities v=q-rep(q). These inequalities
are sufficient: replace any divisible q in a monomial by rep(q), strictly
decreasing its positive weight. The process terminates in D; its residue
determines the unique result. Thus a strictly feasible cone is exactly the
positive-weight cone of its saved tile.

Vertices are primitive integer vectors X representing X/sum(X). The initial
polytope is the standard simplex. Its facets have cyclic lists of vertices.
Half-space clipping intersects an edge (X,Y) with normal v using
`(v.X)*Y-(v.Y)*X`, then divides by the gcd and orients to positive sum.
New cap edges are assembled into a single checked cycle. Every geometric
operation is integer arithmetic. Three-dimensional polygons are supported
as well, for the dimension-reduction cross-check.

At every internal facet its vertex average is a rational relative-interior
point P, represented by an integer multiple. The adjacent tile is computed
with primary weight P and secondary weight minus the inward facet normal:
this is the exact limit P-epsilon*n as epsilon decreases to zero. Every
new active inequality is checked to have positive secondary weight. All
vertices of the old facet must satisfy all the neighboring inequalities;
the opposite normal must occur. Finally every directed facet link must
have an identical reverse link. Simplex-boundary facets are not crossed.

## Exact completeness certificate (unconditional, not modulo a prime)

For every cone, triangulate each cyclic polygonal facet by a fan from its
first vertex. Choose any vertex R of the polytope as reference and form the
tetrahedra (R,A,B,C) over those triangles. Convexity makes them a disjoint
volume decomposition, apart from boundaries; faces containing R contribute
zero. If the four homogeneous integer rows are X_0,...,X_3, the tetrahedron's
volume **divided by the simplex volume** is

    abs(det(X_0,X_1,X_2,X_3)) / product_i sum(X_i).

This is the usual affine determinant formula: normalized rows lie in
sum(p)=1, and subtracting one row from the others reduces it to the
three-coordinate affine determinant. Every determinant uses checked Bareiss
integer elimination. Terms and totals are `fractions.Fraction`. The exact
sum over all cones of each lattice is asserted to equal **1**, i.e. actual
projected three-volume 1/6 (intrinsic Euclidean simplex volume 1/3).

Why this proves completeness: each computed cone is inside the simplex
and has a strict witness. Distinct tiles have disjoint cone interiors:
different representatives of some residue would require contradictory
strict weight comparisons. Every positive weight has a minimum tile, and
grlex ties select a neighboring open cone. This last assertion needs only
the finite set of bounded exponent comparisons: perturb first by total
degree and then by a sufficiently separated positive base expansion of
the lexicographic coordinate weights. A missing tile would therefore give
a missing nonempty open cone of strictly positive volume. This contradicts
the exact total 1. Lower-dimensional boundaries do not hide extra grlex
tiles, by the same perturbation argument.

Facet closure supplies an additional rigorous certificate independently of
the volume calculation: the finite full-dimensional fan has connected
facet-adjacency graph on the open simplex. A generic polygonal path between
interior points can avoid its finitely many codimension-two faces. A
nonempty set of cones closed under every internal facet neighbor must thus
be the whole fan. The default run checks both certificates. `--facet-only`
omits volume computation during traversal but still saves enough data for
the checker to compute exact volumes later.

`certificate_all_m.jsonl.gz` saves one record per lattice, including every
tile and its exact volume. `check_certificate.py` reads this artifact without
performing fan traversal or flips. It checks every down-set, residue
transversal, strictly interior Dijkstra witness, reconstructed cone volume,
and exact lattice volume sum; it also verifies all canonical lattices and
orbit sizes are present. Its result is `checked_all_m.json`. It shares the
integer geometry routines with the enumerator; independent vertex
intersection checks are part of the separate validation suite.

## Validation and reproducibility

The suite in `validate.py` checks:

* Unit/permutation orbits against all ordered primitive vectors for m=2..7.
* Known simplex/order-chamber volumes, redundant cuts and degenerate cuts.
* Every original 3-D tile set for m=4..10, using `src/tile_enum.py` directly,
  then the same complete fan in 4-D with a zero fourth residue. Counts:
  7, 10, 45, 49, 123, 144, 255, respectively.
* All 2,494 tiles for m=5..8: the exact HCR agrees with the existing function.
  For 1,193 tiles at m=5..7, a separate conversion enumerates **all**
  intersections of three supporting planes and compares the vertex sets.
* 2,000 distinct random e=5 semigroups, seed 20261018, multiplicities 5..14.
  Four distinct nonzero residues and independent uniform heights 1..12 are
  drawn; gcd failures and nonminimal generator lists are rejected. The
  accepted semigroups are all saved. Each uses `NS.from_generators` and
  `factorizations_down_set(s,'grlex')`; its coordinate-permuted tile must
  occur in the full enumeration of its canonical lattice. It must also
  equal a direct Dijkstra tile in the original coordinate order. There
  were 311 exact boundary-weight cases, with zero missing tiles.

Every enumerated tile, beyond the validation range too, is checked to be
a down-set of size m, with all m residues distinct and degree <= m-1.
Assertions must be enabled; do not run Python with `-O`.

Sequential commands, to run **on fejer only** (these legacy entry points
retain their individual wall-clock alarms, maximum 280 seconds):

```sh
/usr/bin/python3 -B src/scratch/tile4/validate.py --seconds 270
/usr/bin/python3 -B src/scratch/tile4/enumerate.py 5 12 --seconds 270
/usr/bin/python3 -B src/scratch/tile4/check_certificate.py 5 12 --seconds 270
```

The project lead superseded the initial five-minute local-run rule with a
VM-only compute policy and an approximately two-hour VM budget. The driver
`vm_run.py` parallelizes independent lattices over eight worker processes,
then performs a separate parallel certificate-checking pass for each m.
It requires hostname `fejer`. One parent writes compressed certificates in
canonical lattice order; workers never modify result files. It rechecks
existing certificates on the VM before extending the table. Example launch:

```sh
gcloud compute ssh fejer --zone us-east1-b --command 'cd ~/wilf/tile4; nohup /usr/bin/python3 -B src/scratch/tile4/vm_run.py --seconds 6900 --workers 8 --recheck-existing > vm_run.log 2>&1 < /dev/null &'
```

Poll `~/wilf/tile4/src/scratch/tile4/vm_status.json` and
`~/wilf/tile4/vm_run.log` via SSH. The driver reserves time for independent
verification and stops before starting another m when that reserve is too
small. Its deadline stops workers and leaves any incomplete certificate
with a `.part` suffix. An interrupted m has no aggregate completeness claim;
its gzip `.part` artifact is partial. A subsequent invocation recomputes
it. Completed result and certificate files are renamed into place only
after successful completion. `--resume` reuses completed pairs of files.

This is finite computational evidence about HCR and Apéry tiles. An HCR
failure is a failure of a sufficient shape criterion, not a counterexample
to Wilf's conjecture.

## Completed run

Every m=5..39 is complete and independently checked on fejer: 56,188
canonical lattice classes, 9,532,388 lattice/tile pairs and 309,906
non-two-face pairs. FINAL_STATUS.json records the final PASS audit;
RESULTS.md and table_all.csv give the full table. There are exactly two
HCR failures, both m=13 and HCR=112/117; every cell is listed in RESULTS.md
and hcr_failures_all.json. The compressed per-lattice certificates and
their PASS files are included, together with artifact/source SHA-256
manifests and the VM logs. The last interrupted independent check at
m=39 was completed separately on fejer before finalization.

Continue at m=40, retaining the completed range:

```sh
gcloud compute ssh fejer --zone us-east1-b --command 'cd ~/wilf/tile4; nohup /usr/bin/python3 -B src/scratch/tile4/vm_run.py --mmin 40 --seconds 6900 --workers 8 > vm_extend.log 2>&1 < /dev/null &'
```
