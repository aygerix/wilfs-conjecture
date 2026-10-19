# P4 research report

Status: **P4 is not proved in full. The subcases and residue-coverage
reduction below have complete proofs and the reported verification is
finished.** No claim in this
report promotes a finite search to a proof.

## Exact target and resources

For a nonempty finite down-set `D in N^d` and `n in Z^d`, put `m=|D|`, assume
`n_a>m` for each active direction, and assume `x.n mod m` is bijective
on D. Set `v=x.n`, `M=max v`, `kappa=floor(v/m)`, and
`lambda=floor((M-v)/m)`. The target is

`sum_D min(4,kappa) <= d sum_D min(4,lambda)`.

The primary regime is `4m<=M<5m`; here there is no truncation, and the
target is `g<=d ell`. The supplied GW-19 settles `M<4m`.
All arithmetic, enumeration, compilation, and execution is restricted
to **fejer**, directory `~/wilf/p4`, via gcloud; local actions are file
reading, editing, and copying. No commits are made.

Read in full: `.research/PROOFS.md`, section “Prefix (window) Wilf —
PGW”, through its final H1 reformulation; `p3/P3_REPORT.md`; and the
last notebook entry. The existing K4 scanner and semigroup-tree code
are being adapted with explicit assertion checks.

## Research frontier

* PROVED (prior work): P3, the column identity H1, and
  `g+ell=M-m+1` under residue completeness.
* EXACT GAP: pay the extra cubic carry deficits and the deficient
  pure-A band faces using residue coverage.
* REASON: the residue-free P3 payment and separate class-face argument
  both have explicit K4 counterexamples.
* CANDIDATE MECHANISMS: global residue-interval coverage in the band
  expansion; and a column payment that retains cubic and quadratic
  shadow information.
* DISCRIMINATING TESTS: small exhaustive residue-complete down-sets;
  semigroup tree through genus 28; EF-type constructions with m above
  60; random residue-complete examples in dimensions 5 through 10.

## Work log

Initial state recorded before computation. Complete proofs, exact
failed predicates and counterexamples, and reproducible counts will
be appended as obtained.

The first genus-28 semigroup-tree pass checked 5,311,726 nodes, of which
642,239 have `3m<c<=4m`. All band, weighted-shadow, joint short-residue,
carry/column, and quadratic-subcase assertions passed. Later additions
to the reduction are being rerun separately rather than attributed to
that first pass.

## Proved results

1. **Joint short-residue lemma.** With the notation defined below,
   `t3 + BC + AAB_3 + ABB + BBB <= rho`. The five families have distinct
   residues in a common cyclic interval of length rho.
2. **Transfer lemma.** Write
   `WA=3a(a+1)+(2a-2)q2+(a-3)(q3+u3)-4(u4+k4)`. Then

   `W >= WA + (ab-s3) + c(c+1) + e(3a+2b+c)`
   `          + (c+e)(2q2+q3+s3+t3+u3) + b*u3`.

   Every displayed term other than WA is nonnegative.
3. **Primary regime with at most three A directions.** P4 holds whenever
   `4m<=M<5m` and `a<=3`. For a=2 or 3 the only possibly deficient A
   face is the full cubic simplex with all AA in I3 and AAA in I4.
   A failure forces the entire D to be a full cubic simplex with at
   most one missing cubic, excluded by a quantitative signed-sum bound.
4. **Sparse upper AA band.** The transfer lemma and weighted shadows
   give `3WA >= 18(Q-q2-q3)-(a-1)q3`, where `Q=a(a+1)/2`.
   In particular P4 holds if the right side is nonnegative, including
   every instance with no AA cell in I3.
5. **Signed B3 packing.** A full cubic face in a variables forces
   `m >= binom(a+3,3)+2 binom(a+1,3)`.
6. **Saturated bad face at rho=0.** If the A face is the full cubic
   simplex, all its AA cells are in I3, all its AAA cells in I4, and
   rho=0, then W>0 for a>=2, regardless of the other directions.
7. **Quadratic down-sets, all maxima.** P4 holds for every
   residue-complete down-set of total degree at most two. The primary
   regime follows by band counts. For `M>=5m-1` a residue-free
   two-cell-column payment proves the stronger statement for an
   arbitrary scale q with `n_a>q`.

These are subcases of the requested target, not a proof of the primary
regime for arbitrary a and not a proof of the secondary regime with
cubics in `5m<=M<=6m-2`.

8. **Theorem H4, sharp residue-free cutoff.** For any integer q>=1,
   any finite nonempty down-set, and active weights n_a>q, if
   `M>=6q-1`, then

   `sum_D min(4,floor(v/q)) <= d sum_D min(4,floor((M-v)/q))`.

   No residues or cardinality relation with q are required. The cutoff
   is sharp: the full degree-four simplex in three variables with
   q=35, n=(52,52,52) has M=208=6q-2 and sides 115 and 114.

## 1. Band notation and exact accounting

Assume all d directions active (delete inactive directions first).
Put `rho=5m-1-M`, so `0<=rho<m`, and
`I_j=[jm-rho,(j+1)m-rho)`. Classify units by I1,I2,I3,I4 as A,B,C,E,
of sizes a,b,c,e. Thus `d=a+b+c+e`. The letter e counts class E;
the semigroup embedding dimension is d+1.

Classify nonzero nonunit cells as follows, allowing repeated directions:

| symbol | type and band |
|---|---|
| q2, q3 | AA in I2, I3 |
| s3, s4 | AB in I3, I4 |
| h | AC in I4 |
| t3, t4 | BB in I3, I4 |
| i | BC in I4 |
| u3, u4 | AAA in I3, I4 |
| v2, v3 | AAB in I4, according as its AA divisor is in I2, I3 |
| w | ABB in I4 |
| z | BBB in I4 |
| k | AAAA in I4 |

This list is exhaustive. Weights exceed m, so total degree is at most
four. A quadratic involving E exceeds M, and so does CC. A cubic
involving C exceeds M; a quartic involving B exceeds M. AA cannot
reach I4 since its value is below `4m-2rho`; AB cannot be below I3;
AC and BC must be in I4. The other assertions follow by adding band
endpoints and using n_A>=m+1.

Write `Q=a(a+1)/2`, `B=b(b+1)/2`, and N for the number of nonunit,
nonzero cells. Since lambda=4-j on I_j,

`m=1+d+N`,
`ell=4+3a+2b+c+2q2+q3+s3+t3+u3`.

Residue completeness gives `g+ell=4m-rho`, so the P4 slack is exactly

`W=d*ell-g=(d+1)(ell-4)-4N+rho`.                    (1)

Both floor functions are at most four here. Thus P4 is W>=0.

## 2. Weighted shadows and a joint short-residue lemma

The following bounds will be used:

`q2+q3<=Q`, `s3+s4<=ab`, `h<=ac`, `t3+t4<=B`, `i<=bc`,

`3u3 <= (a+2)q2`,
`3(u3+u4) <= (a+2)(q2+q3)`,
`4k <= (a+3)u3`,

`v2<=b*q2`, `v3<=b*q3`,
`2(v2+v3)<=(a+1)s3`,

`w<=a*t3`, `2w<=(b+1)s3`, `3z<=(b+2)t3`.           (2)

Every divisor of AAA in I3 is AA in I2: removing a weight greater than
m leaves a value below `3m-rho`. Every cubic divisor of AAAA is AAA
in I3. Removing A from AAB leaves AB in I3. Removing either type
from ABB leaves AB or BB in I3. Count incidences `(x,j)` with weight
x_j, removing e_j to obtain the divisor. A quadratic in a variables
receives total possible incoming weight a+2; an AB pair receives
A-incoming weight a+1 and B-incoming weight b+1. These observations
prove the weighted bounds. Removing the unique B or A proves v2,v3,w.

**Joint short-residue lemma:**

`t3+i+v3+w+z <= rho`.                               (3)

The t3 values lie in `[4m-2rho,4m-rho)`. The four other families lie
in `[5m-2rho,5m-rho)`: BC by class endpoints, v3 by its AA divisor
and B unit, ABB since its value is at least `5m-2rho+1`, and BBB since
`6m-3rho > 5m-2rho`. Translate the first interval by m. All five
families have residues in a common cyclic interval of rho residues;
injectivity proves (3), also when the interval wraps or rho=0. QED.

## 3. Exact mixed-class transfer identity

Define

`WA=3a(a+1)+(2a-2)q2+(a-3)(q3+u3)-4(u4+k)`,

`T=(ab-s3)+c(c+1)+e(3a+2b+c)`
`    +(c+e)(2q2+q3+s3+t3+u3)+b*u3`.

Define R as the sum of these eight nonnegative terms:

```
4(ab-s3-s4)
4(ac-h)
4(B-t3-t4)
rho-t3-i-v3-w-z
3(bc-i)
(b+2)t3-3z
a*t3+(b+1)s3-3w
2b*q2+b*q3+(a+1)s3-4v2-3v3.
```

For the last term add `2(b*q2-v2)`, `b*q3-v3`, and
`(a+1)s3-2(v2+v3)`. For the preceding term add `a*t3-w` and
`(b+1)s3-2w`. All other signs follow directly from (2)-(3).

Direct expansion of (1) gives the **exact identity**

`W=WA+T+R`.                                        (4)

One derivation eliminates s4,h,t4 using quadratic capacities, uses
(3), then i<=bc, then pays BBB with its BB shadow, ABB with one BB
and two AB incidences, and AAB with its AA and AB incidences. The
eight losses are exactly R. In particular, **W>=WA+T>=WA**.

Put

`D3=(a+2)(q2+q3)-3(u3+u4)`,
`Dlow=(a+2)q2-3u3`, `D4=(a+3)u3-4k`.

They are nonnegative, and another exact expansion gives

`3WA=18(Q-q2-q3)-(a-1)q3+4D3+2Dlow+3D4`.          (5)

Thus the primary target is proved whenever
`18(Q-q2-q3)>=(a-1)q3`, including q3=0.

## 4. Signed sums: exact and quantitative residue coverage

Let `B0={0,s1,...,sa}` in Z/m, with s=a+1. If all unordered triples
of B0, allowing repetitions, are distinct, B0 is a B3 set. Padding
by zeros shows this condition follows from a full cubic face of a
residue-injective down-set.

Consider normal signed labels `(p,q;r)`, with `p,q in B0\{r}` and
p<=q, having residue p+q-r. There are `s^2(s-1)/2` labels. Equal
residues give `p+q+r'=p'+q'+r`. Triple injectivity makes the multisets
equal. The absence of r from {p,q} and r' from {p',q'} then forces
r=r' and {p,q}={p',q'}. A normal signed residue also cannot lie in
B0: that would contradict pair injectivity. Consequently

`m >= s*(s*(s-1)/2+1)`
`   = binom(a+3,3)+2 binom(a+1,3)`.                 (6)

For a quantitative version assume only pair injectivity and put

`r=binom(s+2,3)-#{residues of unordered triples of B0}`,
`J_s=min(9,floor(s^2/4))`.

Then

`m >= s*(s*(s-1)/2+1) - J_s*r*(r+1)/2`.            (7)

Proof. Distinct triples of equal residue have disjoint supports:
otherwise cancellation contradicts pair injectivity. Each colliding
triple pair creates at most the product of its support sizes in
colliding normal signed label pairs. That product is at most J_s.
A triple residue of multiplicity 1+t contributes t(t+1)/2 colliding
pairs; summing with sum t=r gives at most r(r+1)/2 pairs. A fiber of
h equal signed labels loses h-1 residues, at most its h(h-1)/2
colliding pairs. Finally signed residues are disjoint from B0 by pair
injectivity. These facts prove (7). QED.

**Corollary.** A residue-complete down-set in d>=2 variables cannot be
the full cubic simplex with zero or one cubic deleted.

All pairs are represented and distinct. With no deletion use (6).
With one deletion the triple collision excess is at most one, since
D represents all m residues distinctly. Put `P=binom(d+3,3)` and
`H=P+2binom(d+1,3)`. For d=2,3, the bounds `H-J_{d+1}` are 10,24,
exceeding P-1=9,19. For d>=4, `2binom(d+1,3)>=20>9>=J_{d+1}`.
Thus (7) again gives more than P-1 residues. QED.

## 5. Complete primary-regime proof for a<=3

**Theorem.** Under the exact P4 hypotheses, if `4m<=M<5m` and at most
three active weights are below `2m-rho` (equivalently a<=3), then P4.

For a=0,1, (5) gives WA>=0, so (4) suffices.

For a=2, (5) gives WA>0 if any AA is missing. If all three are
present, use `3u3<=4q2`, `u3+u4<=4`, `4k<=5u3` in
`WA=18+2q2-q3-u3-4(u4+k)`. For q2=1,2 the resulting lower bounds
are 1,3. For q2=3, `u4+k<=4+floor(u3/4)` and u3<=4 give WA>=0.
For q2=0 negativity forces exactly

`WA=-1, q3=3, u4=4, u3=k=0`.                       (8)

If W<0, integrality and (4) force T=R=0. Thus c=e=0, s3=2b, all
AB and BB pairs are present, v3=3b, and both ABB shadows and the BBB
shadow are equalities. The ABB equalities give t3=B,w=2B; then the
BBB equality gives `z=b(b+1)(b+2)/6`. All quadratics and cubics in
d=2+b variables are present, and no quartic exists since k=0. This
is the full cubic simplex, excluded by (6). Therefore W>=0.

For a=3, `WA=4(9+q2-u4-k)`. The shadows give

`u4+k <= (u3+u4)+u3/2 <= 10+5q2/6`.

If q2>=1 this is strictly below 10+q2, so integrality gives WA>=0.
If q2=0, u3=k=0 and u4<=10; negativity therefore forces

`WA=-4, q3=6, u4=10, u3=k=0`.                      (9)

Suppose W<0 in (9). Then `S:=T+R<=3`. A C direction contributes
at least `2+q3=8` to T and an E direction at least `3a+q3=15`, so
c=e=0. Put p=3b-s3. The coefficient-four terms of R force all AB
and BB pairs to be present. The AAB term is

`D_v=6b+4s3-3v3=18b-4p-3v3`.

Since v3<=2s3, D_v>=2p; hence S>=3p and p<=1. If p=1, exactly
one B direction has only two A neighbors among the I3 AB pairs.
Every AAB uses two such neighbors, with repetitions. This B supplies
at most three AAB instead of six, so v3<=6b-3. Then D_v>=5 and
S>=p+D_v>=6, impossible. Thus p=0 and s3=3b.

All BB pairs are present, t3=B-t4. The ABB term satisfies

`D_w=3t3+(b+1)s3-3w >= 6t4`,

using w<=3t3. Thus t4=0, t3=B. The AAB, ABB, BBB terms of R become

`3(6b-v3)`, `3(3B-w)`, `3(b(b+1)(b+2)/6-z)`.

Their sum is three times the number of missing cubics of the full
d-variable simplex; all ten AAA are already present. At most one
cubic is missing, all quadratics are present, and no quartic exists.
This contradicts the corollary to (7). Therefore W>=0. QED.

## 6. Saturated EF-type face at rho=0, arbitrary a

**Theorem.** Suppose rho=0, a>=2, and the A face contains every
monomial of degree at most three, all AA in I3, all AAA in I4.
Then W>0, regardless of the other directions, without minimality.

Put `F=binom(a+1,3)`, k0=d-a, `P_A=binom(a+3,3)`. The A face has
P_A cells and WA=-F. No mixed cubic exists: AAB is at least 5m by
its AA divisor and B unit, and (3) excludes ABB/BBB. No quartic
exists because its AAA divisors would be in I3. Therefore

`m <= P_A+k0*(a+1)+k0*(k0+1)/2`.

But (6) gives m>=P_A+2F. If k0<=(a-1)/3, the extra-cell bound is
at most `(a-1)(7a+8)/18`, strictly below `2F=a(a+1)(a-1)/3` for
a>=2. Thus k0>(a-1)/3. Directly expanding (1) and bounding the
external quadratic families gives

`W-WA >= k0*Q+ab+3ae+2b(c+e)+c(k0+1)+(d+1)s3 >= k0*Q`.

Since `F=(a-1)Q/3`, we have W>=-F+k0*Q>0. QED.

This establishes the missing-residue compensation in the saturated
EF-type face even for nonminimal tiles. It does not claim every
deficient face is saturated when a>=4, or permit discarding rho.

## 7. Sharp residue-free theorem H4 for large maxima

**Theorem H4.** Let q>=1 be an integer, D a finite nonempty down-set
in N^d, n in Z^d, and n_a>q for every active direction. Put M=max_D v and
`F(t)=min(4,floor(t/q))`. If M>=6q-1, then

`sum_D F(v) <= d sum_D F(M-v)`.

Delete inactive directions. Put `B(x)=sum_a F(x_a*n_a)` and
`sigma(x)=max(0,B(x)-F(v(x)))`. Column reflection, exactly as H1,
gives

`d sum_D F(M-v)=sum_D B+CS`,                        (10)

where every column slack is nonnegative. The only deficits B<F(v)
are mixed quadratics and mixed cubics, each with deficit one. Indeed
degree>=4 gives `B>=sum_a min(4,x_a)>=4`; axes give equality. A
quadratic deficit has floors 1+1 carrying to 3 or 1+2 carrying to 4.
A cubic deficit has B=3,F(v)=4: either three distinct floor-one units
or an axis double with floor two and one floor-one unit.

For each deficit choose b of largest weight in its support, breaking
ties by index. Its b-column has base z obtained by zeroing x_b. Put
j0=x_b, and choose j* by this table:

| deficit | base degree | j0 | j* |
|---|---:|---:|---:|
| quadratic, floor(n_b/q)=2 | 1 | 1 | 2 |
| quadratic, floor(n_b/q)=1 | 1 | 1 | 3 |
| cubic with doubled largest direction | 1 | 2 | 3 |
| other cubic, 2n_b>=3q | 2 | 1 | 2 |
| other cubic, 2n_b<3q | 2 | 1 | 3 |

Each column is chosen by at most one deficit. The only possible
overlap would be a quadratic and a cubic with a base of degree one.
The cubic requires n_b<3q/2, so maximality of n_b makes that
quadratic sum below 3q, and it is not deficient. All other bases
have only the single possible j0.

In every row `y=z+j*e_b` has sigma(y)>=1. For the floor-two quadratic,
F(2n_b)=4, with one extra base unit. For the floor-one quadratic the
carry and maximality give n_b>=3q/2, so F(3n_b)=4. A cubic has
n_b>=4q/3 by maximality. A doubled-largest cubic has F(3n_b)=4
and one base unit. The remaining rows have base B=2 and respectively
F(2n_b)>=3 or F(3n_b)=4. Thus y is a surplus cell in all cases.

If y belongs to D, charge one unit of sigma(y). The assignment is
injective: the support of y determines the same distinguished b,
then its other coordinates determine z and the chosen column.

If y is absent, the column ends at J<j*. Its slack is

`s=sum_{j=0}^J F(M-v(z)-j*n_b)-sum_{j=0}^J F(j*n_b)`.

It is at least one in every case:

* Base degree one, floor-two quadratic: J=1. The first term is 4,
  since v(z)<=2q-1 and M>=6q-1; the only negative term is 2.
* Base degree one, floor-one quadratic: J=1 or 2. The first term is 4.
  For J=1 subtract only 1. For J=2 the second term is at least 2,
  since v(z)+n_b<=4q-2, while the negative sum is 1+3=4.
* Base degree one, doubled-largest cubic: J=2. The first term is 4;
  the negative sum is 1+2=3.
* Base degree two, J=1: v(z)<=4q-2, so the first term is at least 2
  and the only negative term is 1.
* Base degree two, J=2: n_b<3q/2 and b has largest weight, hence
  `v(z)<=2n_b<=3q-1`. The first term is at least 3. Also
  `M-v(z)-n_b>=M-3n_b>=q`, so the second term is at least 1.
  The negative sum is 1+2=3.

All omitted positive terms are nonnegative because column cells
have value at most M. Charged columns are distinct, and columns and
cells are separate resources. Therefore

`#deficits <= CS+sum sigma`.

Together with (10) and `sum B-sum F(v)=sum sigma-#deficits`, this
proves H4. QED. No step uses residues or q=|D|.

**Sharpness and preserved failed claim.** The attempted cutoff 6q-2
is false. For any odd q>=3, take the full degree-four simplex in three
variables with all weights `(3q-1)/2`. For q=35 its cardinality is m=35,
n=(52,52,52), M=208=6m-2. The left sum by degree is
`3+2*6+4*10+4*15=115`; the right sum is
`3*(4+4*3+2*6+1*10)=114`. This is the first failing dimension in
this full-simplex uniform-weight family, not a claim of a globally
smallest example. It lacks residue injectivity. The q=30 min-cut run
missed this odd-denominator boundary; that run does not validate the
rejected cutoff. The corrected proof uses the extra unit in M in
the final base-degree-two J=2 payment.

## 8. Quadratic down-sets: P4 for every maximum

**Theorem.** P4 holds under its exact hypotheses if every cell has
total degree at most two.

For M<4m use prior P3. In the primary regime (4) suffices:
`WA=3a(a+1)+(2a-2)q2+(a-3)q3` is nonnegative. For a>=3 all
coefficients are nonnegative; for a=2 the bound is at least 15;
for a=1 at least 4; for a=0 zero.

For M>=5m use a stronger residue-free fact. At any scale q, if
M>=5q-1 and degree is at most two, a deficit is a mixed pair
e_a+e_b with `q<n_a<2q`, `n_a<=n_b<3q`, and deficit one. The
b-column based at e_a has exactly two cells and slack

`F(M-n_a)+F(M-n_a-n_b)-F(n_b) >= 3+0-2=1`.

Different pairs use distinct columns. Apply (10). With q=m all
regimes are covered. QED.

In the primary regime, direct quadratic capacities and rho>=i also
give, when d>=3,

`W>=3a(a+1)+ab+c(c+1)+e(3a+2b+c)`.

To see this, drop nonnegative q2,q3,s3,t3 coefficients, bound s4,h,t4
by ab,ac,B, then use `rho-4i>=-3bc`. Expanding yields the bound.

## 9. Exact unresolved statement and strategic review

The primary gap has been reduced to a>=4. By (4)-(5), the primary
target is **equivalent** to this precise residue-coverage inequality:

`(a-1)q3 <= 18(Q-q2-q3)+4D3+2Dlow+3D4+3T+3R`.      (RC4)

It is proved above for a<=3, for the sparse-AA criterion in section 3,
and for the saturated bad face at rho=0. No proof for general a>=4
is supplied. WA>=0 cannot replace RC4, since EF-type faces have
WA<0. Signed-sum packing controls full or nearly full cubic faces;
the remaining issue is to turn a negative WA at a>=4 into enough
near-saturation for that lemma to apply while allowing low AA pairs
and quartics.

The secondary regime is proved for M>=6m-1 without residues, and for
every M in the quadratic subcase. What remains there is exactly
`5m<=M<=6m-2` with cubic or higher cells and residue completeness.

Strategic decision: discard the residue-free 6q-2 route (explicitly
false), retain sharp H4, and give the lead the exact transfer/packing
reduction rather than extend blind small scans that miss large
deficient faces. The next discriminating proof task is a stability
form of (6) coupled to the three pure-A shadow defects in (5), starting
at a=4. This is a mathematical gap, not evidence that P4 is false.

## 10. Computational verification and reproducibility

All execution, arithmetic evaluation, enumeration, compilation, flow
optimization, aggregation, and hashing took place on **fejer** in
`~/wilf/p4/`. Local operations were reading, editing, and copying files.
Jobs used nice -n 10 and at most four simultaneous single-core jobs;
flow jobs used OPENBLAS_NUM_THREADS=1 and OMP_NUM_THREADS=1. No other
processes were touched. Software was Python 3.12.3 and GCC 13.3.0.
No commits were made.

### Exhaustive residue-complete down-sets

`p4_scan.c` uses canonical shapes up to coordinate permutation. Every
residue vector s in `{1,...,m-1}^d` that is injective on the shape is
enumerated, then every lift `n=s+m*k`, `k in {1,2,3,4}^d`. All d
directions are required active; inactive directions are covered by the
proved deletion argument. Counts below are **canonical-shape instances,
not orbit-weighted labeled counts**. Symmetry still covers all labeled
instances in these ranges.

| d | m | all instances | K4 assertions | H4 assertions | H4 deficits paid |
|---|---|---:|---:|---:|---:|
| 2 | 3–24 | 99,200 | 94 | 98,918 | 8,971 |
| 3 | 4–18 | 1,919,744 | 3,430 | 1,906,310 | 396,061 |
| 4 | 5–14 | 12,976,640 | 100,433 | 12,591,956 | 3,112,752 |

All completed without an assertion failure. `p4_check.h` checks the
full band classification, each listed divisor-band implication, all
weighted shadows, the joint short interval (including the actual
cyclic residue interval), both exact expansions (4)-(5), residue sum,
carry/column equality, the a<=2 and a=3 negative-WA characterizations,
and the quadratic/no-A bounds. There are 55 negative two-A faces in
these canonical counts, so testing includes cases where WA>=0 fails.

`h4_check.h` checks the exact truncated column identity, every deficit's
degree and size, the selected maximal-weight direction, at most one
deficit per chosen column, actual surplus or actual column slack,
injectivity of both payment kinds, and the final inequality. It is
called only when M>=6m-1.

### Exhaustive residue-free charging checks

Same canonical shape generator, mode 0, now every integer weight
`n_a in [m+1,3m]`, with no residue test. Only the H4 predicate and proof
assertions are checked in this mode.

| d | m | all instances | M>=6m-1 | deficits | cell payments | column payments |
|---|---|---:|---:|---:|---:|---:|
| 2 | 3–12 | 54,648 | 51,412 | 16,292 | 6,893 | 9,399 |
| 3 | 4–9 | 354,800 | 219,024 | 74,695 | 14,486 | 60,209 |
| 4 | 5–7 | 281,968 | 37,907 | 1,428 | 0 | 1,428 |

All assertions passed. The zero cell-payment count in the last row
is a property of that small range, not a claim that cell payments are
unnecessary in general.

### Semigroup tree through genus 28

`p4_tree.c` visits all **5,311,726** numerical semigroups through genus
28. It filters `3m<c<=4m`, constructs the minimal factorization tile by
lexicographically largest factorization, and checks downward closure
independently before calling the shared verifier. Results:

* **642,239** depth-four semigroups; all K4 assertions passed.
* 479,231 quadratic tiles; 453,098 with a=0.
* 633,345 with a<=2; **640,993 with a<=3**.
* 981,715 members of the joint short-residue families checked.
* 834,429 untruncated carry units; exact equality to column slack minus
  W checked in every instance. Minimum W was zero.

The tree filters to K4, so it does not test H4 at larger conductors.
The factorization tie-break is lexicographically **largest**:
the implementation repeatedly removes the least generator admitting an
Apéry predecessor, thereby maximizing earlier coordinates. Closure is also
asserted directly; no proof depends on this descriptive convention.

### Independent and adversarial verification

`explore.py --tiles 20000 --packing 200000`, seed 20261018:

* 15,865 accepted residue-complete down-sets with actual active
  dimension 5–10 and m<=120. Shapes come from shortest paths on the
  cyclic residue graph, with either actual weights or independent
  positive costs. Independent costs allow nonminimal tiles. The code
  checks downward closure and residue completeness directly.
* All P4 inequalities passed. Of these, 308 are K4, with 54 at rho=0
  and eight with rho>=4m/5. Independent Python classification,
  short-residue, transfer, pure-A shadow bound, and a<=3 characterization
  checks passed in the K4 cases. These random cases had no negative
  WA, so the EF tests below are necessary, not optional corroboration.
* 83,155 pair-injective B0 sets among 200,000 proposals, cardinalities
  3–8 and modulus 5–200, checked (7). There were 42,729 with triple
  collision excess zero and 18,374 with excess one. Every bound passed.

`explore.py --ef 90` exhaustively constructs
`<m,A> union [4m,infty)` for m=6–90, |A|=2,3,4, and
`A subset [ceil((3m+1)/2),floor((5m-1)/3)]`, retaining exact conductor
4m. There are **30,863** semigroups, **10,663** negative A-face
expressions, and **6,578** full B3 faces. For all 6,578 full faces,
the script constructs the entire tile (the remaining representatives
are class-E units), checks it independently, verifies the transfer
bound, the signed-sum cardinality, and the strict saturated-rho-zero
theorem. Every instance passed.

The original supplied example is independently reproduced by
`summarize.py`: m=23, A={35,37}, M=114, a=2,e=13, genus=79,
ell=13, WA=-1, T=117, W=116. The smallest negative face in the
enumerated EF family is m=14,A={22,23}, with WA=-1 and W=35. No
global minimality beyond that specified family is claimed.

`explore.py --quad 20000`, seed 20261018, has 19,631 instances of
the quadratic residue-free theorem at arbitrary q independent of the
cardinality, and **19,972** distinct column payments, all verified.

`closure4.py` independently solves an exact integer minimum-cut problem:
for fixed n,q and a required top y, minimize the complete P4 slack
over **all** order ideals in `{x:x.n<=y.n}` that contain y. The final
run used q=31, 1,000 random weight vectors, d=2–12,
`n_a in [q+1,3q]`, and up to four tops each with
`6q-1<=y.n<=8q`. All **3,961** optimizations had nonnegative minimum.
This is independent of the column charging implementation and allows
q!=|D|. The earlier q=30, cutoff-6q-2 run has 3,977 nonnegative
optimizations, but its candidate theorem is false; see the explicit
odd-q counterexample in section 7.

`summarize.py` also independently evaluates:

* The supplied nonresidue example m=10,n=(16,17), degree<=3: 27>26.
* The new sharpness example m=35,n=(52,52,52), degree<=4: 115>114.
* The equality example <5,6>: both sums are 10.
* **4,950** class-E star tiles, m=2–100 and rho=0–m-2, all with W=rho.
  The rho=0 cases include every T_{m,4} in that range.

### Commands and files

Copy the seven source files in this directory to `~/wilf/p4/`, compile
on fejer, and run each command with nice. The aggregate command verifies
that each listed m-range is complete before writing its JSON summary.

```sh
nice -n 10 gcc -O3 -std=c11 -Wall -Wextra p4_scan.c -o p4_scan_nr
nice -n 10 gcc -O3 -std=c11 -Wall -Wextra p4_tree.c -o p4_tree_h4
nice -n 10 ./p4_scan_nr 2 3 24 > scan2_h4.log 2>scan2_h4.err
nice -n 10 ./p4_scan_nr 3 4 18 > scan3_h4.log 2>scan3_h4.err
nice -n 10 ./p4_scan_nr 4 5 14 > scan4_h4.log 2>scan4_h4.err
nice -n 10 ./p4_scan_nr 2 3 12 0 > nores2.log 2>nores2.err
nice -n 10 ./p4_scan_nr 3 4 9 0 > nores3.log 2>nores3.err
nice -n 10 ./p4_scan_nr 4 5 7 0 > nores4.log 2>nores4.err
nice -n 10 ./p4_tree_h4 28 > tree28_h4.log 2>tree28_h4.err
nice -n 10 python3 explore.py --tiles 20000 --packing 200000 > random_final.log
nice -n 10 python3 explore.py --ef 90 > ef90_final.log
nice -n 10 python3 explore.py --quad 20000 > quad_final.log
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 nice -n 10 ~/mathenv/bin/python closure4.py --trials 1000 --dmax 12 --cap 8 --weightmax 3 --tops 4 > closure4_sharp.log
nice -n 10 python3 summarize.py > summary_stdout.json
```

Original logs, including earlier passes and the rejected-cutoff run,
are copied to `logs/`. `logs/verification_summary.json` contains all
final counts, the independently evaluated examples, raw random/EF
summaries, and SHA-256 hashes of the archived source files.

## 11. Explicit residue dependency and limitations

The band transfer uses residues only in (1), which uses completeness,
and (3), which uses injectivity. The primary a<=3 proof additionally
uses the signed-sum packing (6)-(7), a stronger global injectivity
consequence. The saturated EF-face proof uses the same packing.
H4 uses no residue information. The quadratic proof uses residue
completeness only in its lower-maximum regimes.

No numerical-semigroup addition closure is used in these down-set
proofs. In particular the primary subcase statements apply to
nonminimal residue-complete down-sets as requested.

The task's exact P4 and general Wilf for 3m<c<=4m are **not proved**
by this report. RC4 for a>=4 and the secondary middle interval remain
the stated gaps. The proofs are on paper with exact computational
checks; no Lean formalization is claimed, and publication priority of
the subcases has not been investigated.

## 12. Continuation: a=4 stability and linear packing

The lead independently verified sections 1–11 and recorded them as
GW-21. Those sections are retained. This continuation targets RC4
for a>=4 first, then the secondary middle interval.

**New stability lemma for a=4 (proved via Macaulay; mixed-case
proof and verification completed below).** If WA<0, then all ten AA monomials are
present, and exactly one of the following six profiles occurs:

| family | q2 | q3 | u3 | u4 | k | WA |
|---|---:|---:|---:|---:|---:|---:|
| I_t, t=0,1,2 | 0 | 10 | 0 | 20-t | 0 | -10+4t |
| II_t, t=0,1 | 1 | 9 | 0 | 20-t | 0 | -5+4t |
| III | 1 | 9 | 1 | 19 | 1 | -4 |

Let p=q2+q3, r=10-p and t=20-u3-u4. Algebra gives

`WA=-10-r+5(q2+u3)-4k+4t`.

For a monomial order ideal the Hilbert function obeys Macaulay growth,
`h_{j+1}<=h_j^{<j>}`. The required statement, with the binomial
expansion defining this integer operator, is Theorem 5.5 in
[Eliahou, Wilf's conjecture and Macaulay's theorem, section 5.1](https://arxiv.org/html/1703.01761#S5.SS1).
It applies both to the pure-A ideal and its sub-ideal cut out by
`sum x_i(n_i-m)<m-rho`: the latter has degree-2,3,4 counts q2,u3,k.
The bounds q2=0,...,10 give these minima of `5(q2+u3)-4k`:

`0, 5, 10, 15, 20, 24, 20, 25, 29, 25, 10`.

They are obtained by minimizing `5q2+5u-4u^{<3>}` over
`0<=u<=q2^{<2>}`. All are nonnegative. If r>=2, the existing
weighted shadow gives t>=2r, hence WA>=-10+7r>=4. If r=1, the
missing AA monomial excludes its four distinct cubic multiples, so
t>=4 and WA>=5. Thus r=0. For q2>=2 the displayed minimum is at
least 10. For q2=0 or 1, elementary enumeration u3<=1,k<=u3 gives
the six rows. `a4_stability.py --a 4` independently checks all
integer profiles allowed by both Macaulay bounds and reproduces
exactly these six negative rows.

**Linear weighted packing lemma.** Let B0 have distinct unordered
pair residues. Let C be a family of unordered triples with distinct
residues, and let E be its complementary family of omitted triples.
If the residues of E are also distinct, then, with s=|B0|,

`m >= s(s(s-1)/2+1) - sum_{x in E} |supp(x)| min(3,s-|supp(x)|)`.

Indeed each residue has at most one chosen and at most one omitted
triple; hence every triple collision is between one of each. As in
(7), their supports are disjoint, and a fixed omitted triple generates
at most the displayed number of colliding signed-label pairs. Sum
this linear loss and use signed-label residues' disjointness from B0.
The hypothesis on E holds in particular if its triples pairwise share
a variable, since equal triple residues would have disjoint supports.

An exact random check, seed 20261019, tested 40,995 chosen/omitted
partitions satisfying this hypothesis, including 33,572 with an
intersecting omitted family. All bounds passed. These are 100,000
proposals, 42,024 of them pair-injective, moduli 7–200 and |B0|=3–8.
The linear lemma is a proof, not an inference from this check.

The proposed a=4 argument now uses W<0 to force all AB/BB pairs and
almost all mixed cubics, and then uses this linear bound in the few
small-dimensional cases where (7) alone is too weak. In particular
family III explicitly retains rho>0, q2=1 and a quartic; it is not
discarded as an EF-type simplification.

## 13. Complete primary-regime proof for a=4

**Theorem.** Under the exact P4 hypotheses, if `4m<=M<5m` and
`a=4`, then W>=0. In conjunction with section 5 this proves the
primary regime whenever a<=4. No condition on rho is imposed.

Here and below a full cubic simplex in d variables has
`P_d=binom(d+3,3)` cells, and its signed-label count is
`H_d=P_d+2binom(d+1,3)`.

First record two packing consequences of section 4:

* A full cubic simplex with at most two cubics omitted cannot be a
  residue-complete tile when d>=4. For d=4, `H_d-3J_{d+1}=37>P_d=35`;
  for d=5 it is `69>56`; for d>=6 use
  `2binom(d+1,3)>=70>27>=3J_{d+1}`.
* A full cubic simplex with at most three cubics omitted cannot be
  a residue-complete tile when d>=6, since
  `2binom(d+1,3)>=70>54>=6J_{d+1}`.

If WA>=0, (4) proves the theorem. Assume WA<0 and W<0. Use the six
profiles of section 12. Since q3>=9, one C direction contributes at
least 11 to T, and one E direction at least 21. But -WA<=10.
Therefore c=e=0. Write `B=b(b+1)/2`, `Z=b(b+1)(b+2)/6`, and

`p=4b-s3`, `r_AB=4b-s3-s4`, `r_BB=B-t3-t4`,
`D_v=2b*q2+b*q3+5s3-4v2-3v3`,
`D_w=4t3+(b+1)s3-3w`, `D_z=(b+2)t3-3z`,
`R_s=rho-t3-v3-w-z`.

Then

`T+R=p+b*u3+4r_AB+4r_BB+R_s+D_v+D_w+D_z`.       (A4.1)

All terms except the grouping p+D_v are individually nonnegative.

### The AB-neighbor loss (also a uniform lemma)

For a B direction j, let N_j be its A neighbors among the I3 AB
pairs, `r_j=|N_j|`, `p_j=a-r_j`. Let q2(N_j) be the low AA pairs
supported inside N_j, and let v2_j,v3_j count the AAB cells using j.
If **all AA pairs are present**, then

`p_j + [2q2+q3+(a+1)r_j-4v2_j-3v3_j]`
` >= p_j(4a+3-3p_j)/2 + q2-q2(N_j)`.             (A4.2)

Proof: `4v2_j+3v3_j <= 3binom(r_j+1,2)+q2(N_j)`, because every
AB divisor of an AAB lies in I3. Substitute q2+q3=Q and expand.
The concave quadratic on the right of (A4.2) is at least 2a when
1<=p_j<=a. Thus **each B direction missing any I3 AB neighbor costs
at least 2a in p+D_v**. This lemma is valid for arbitrary a, not
only a=4, and explicitly retains low AA pairs.

For a=4, q2=0, the costs for p_j=1,2,3,4 are respectively
8,13,15,14. If q2=1 these are still valid lower bounds. In every
negative profile, all ten AA pairs are present, so (A4.2) applies.

Two further elementary bounds will be used:

* If p=0, then `D_w>=8(B-t3)`, using w<=4t3. Therefore the terms
  `4r_BB+D_w` are at least `12r_BB+8t4`.
* If B>t3, one BB pair is absent from I3. Its b distinct cubic
  multiples are all excluded from BBB, so `Z-z>=b`.

### Family I_t: q2=0, u3=k=0, u4=20-t, 0<=t<=2

Here WA=-10+4t, so `S=T+R<=9-4t`. Formula (A4.2) shows that
either p=0, or t=0 and exactly one B direction has exactly one
missing I3 AB neighbor (p=1).

**Case p=0.** The bound `12r_BB+8t4<=S<=9` forces r_BB=0 and
t4<=1. Thus all quadratics are present.

If t4=0, the three mixed-cubic defects become

`D_v=3(10b-v3)`, `D_w=3(4B-w)`, `D_z=3(Z-z)`.

Consequently the number r of missing cubics in all d=4+b variables
satisfies

`r <= t+floor((9-4t)/3)`.

This is at most two unless t=0, when it is at most three. Packing
excludes d>=6, and excludes d=4 because then b=0 and r=t<=2.
At d=5, the only remaining case is t=0,r=3. All omitted cubics
use the sole B variable, so they have distinct residues by pair
injectivity. The linear bound of section 12 loses at most 9 per
omitted cubic: `m>=H_5-27=69`, contradicting m=P_5-3=53.

If t4=1, necessarily t=0. Since `D_z=3(Z-z)-(b+2)>=2b-2`, the
remaining budget after D_w>=8 gives b<=1. Thus b=1,t3=0, w=z=0,
and the remaining budget forces v3=10. The whole D is the full
cubic simplex in five variables with four ABB and one BBB omitted.
Their support sizes are 2,2,2,2,1, and all contain the B variable.
The linear packing loss is at most `4*6+3=27`. Again m>=69, whereas
the actual cardinality is P_5-5=51. Contradiction.

**Case p=1.** This requires t=0. The neighbor loss is at least 8,
leaving budget at most one for all other terms of (A4.1). Hence
r_AB=r_BB=0, and D_w,D_z<=1. Let j be the unique B direction
missing an A neighbor i, and let L_j be the number of I3 BB pairs
containing j. Then

`w<=4t3-L_j`, `L_j>=b-t4`,
`D_w>=8t4-(b+1)+3L_j>=5t4+2b-1`.

It follows that b=1,t4=0,t3=1. Now s3=3, and D_w<=1 forces w=3.
The budget forces D_v=7, v3=6, and D_z=0,z=1. All quadratics are
present and precisely five cubics are omitted: i^2*j, the three
i*k*j with k another A variable, and i*j^2. They all use j, and
their support sizes are 2,3,3,3,2. The linear packing loss is at
most `6+3*9+6=39`. Hence m>=H_5-39=57, contradicting m=51.
This closes every I_t case.

### Family II_t: q2=1, u3=k=0, u4=20-t, t=0,1

WA=-5+4t, so S<=4-4t. The neighbor loss of at least 8 forces p=0.
Then `12r_BB+8t4<=S` forces r_BB=t4=0: all quadratics are present.
The mixed defects are

`D_v=4(b-v2)+3(9b-v3)`,
`D_w=3(4B-w)`, `D_z=3(Z-z)`.

The number of missing mixed cubics is at most floor((4-4t)/3).
Including the t missing A cubics, the entire D is a full cubic
simplex with at most one cubic omitted. Section 4 excludes it.

### Family III: q2=1, u3=k=1, u4=19

WA=-4 gives S<=3. Since `S=p+b+R`, the neighbor bound forces
p=0 and b<=3. Again r_BB=t4=0. If b>=1, the remaining budget
3-b<=2 forces every mixed-cubic defect in the preceding display to
vanish. For b=0 there are no mixed cubics. Thus every cubic in all
d=4+b variables is present, and there is exactly one quartic.
The cardinality is m=P_d+1, but full cubic packing gives
`m>=H_d=P_d+2binom(d+1,3)>P_d+1` for d>=4. Contradiction.

All six profiles are excluded under W<0. This proves W>=0 and the
a=4 theorem, including rho>0, q2>0 and the quartic case. QED.

At this stage of the continuation the primary gap was a>=5. The Macaulay relaxation at a=5
has 22 negative profiles (recorded in `a5_catalog.log`), so the
a=4 six-profile proof is not being promoted to a uniform theorem.

## 14. Uniform control of the low AA band

**Uniform low-cost lemma.** For a>=3 and any monomial ideal of the
kind used here, put `F_a=binom(a+1,3)`. Then

`L_a:=(a+1)(q2+u3)-4k >= min((a+1)q2,F_a)`.        (LC)

Proof. Write `q2=binom(r+1,2)` with real 0<=r<=a. The condensed
Macaulay theorem (Eliahou, Theorem 5.10 in the source cited in
section 12) gives `u3<=binom(r+2,3)`. Write
`u3=binom(x,3)`, 2<=x<=r+2. Applying it once more gives
`4k<=(x+1)u3`. Thus

`L_a >= (a+1)q2+(a-x)binom(x,3)`.

For x<=a the last term is nonnegative. For x>=a it decreases with
x, so its minimum is at x=r+2. If r<=a-2 we obtain
`L_a>=(a+1)q2`. If a-2<=r<=a the remaining expression is

`ell_a(r)=r(r+1)[a(r+5)-r^2-4r-1]/6`.

The exact factorization

`ell_a(r)-F_a=(a-r)[r^3+5r^2+(5-a)r-a^2+1]/6`

is nonnegative on this interval. The cubic bracket at r=a-2 is
`(a-3)(a^2-1)>=0`; its derivative is
`3r^2+10r+5-a>0` for r>=a-2 and a>=3. This proves (LC). QED.

Let `r_A=Q-q2-q3`, `t_A=binom(a+2,3)-u3-u4`. Direct algebra gives

`WA=-F_a+L_a-(a-3)r_A+4t_A`.

The cubic shadow gives `3t_A>=(a+2)r_A`. Therefore if WA<0, (LC)
forces

`q2<a(a-1)/6`,
`3(a+1)q2+(a+17)r_A<3F_a`.                        (LC-)

Indeed L_a>=F_a would imply WA>=0; below that threshold the proof
of (LC) gives L_a>=(a+1)q2. These are necessary conditions for a
deficient face, uniform in a. They strengthen the q2 coefficient in
the earlier coarse consequence of (5).

`uniform_lowcost.py --amax 24` checked all 1,446,390 integer pairs
(q2,u3) permitted by exact Macaulay growth, using the largest permitted
k, for a=3–24. Every (LC) inequality passed. It also checked the
displayed factorization and signs at 19,698 rational points, a=3–100.
The proof is the factorization and monotonicity argument above, not
the bounded checks.

## 15. A universal linear packing bound; distinct-weight H4

**Universal linear packing lemma.** Let B0 have s distinct elements
with injective unordered pair residues modulo m. Let r be the excess
of the number of unordered triples over their number of residues.
Then

`2m >= 2s(s(s-1)/2+1)-3s*r`.                       (LP)

Proof. In a residue fiber with g distinct triples, their supports
are pairwise disjoint. If their support sizes are t_1,...,t_g,
then 1<=t_i<=3 and sum t_i<=s. The number of signed-label collision
pairs arising from this fiber is at most

`sum_{i<j} t_i*t_j <= (3/2)(g-1)sum_i t_i <= (3s/2)(g-1)`.

The first inequality follows by summing
`sum_{j!=i}t_j<=3(g-1)` against t_i and dividing by two. Sum over
fibers; sum(g-1)=r. Normal signed residues still avoid B0. The same
loss-counting argument as in (7) proves (LP). QED.

In particular, a face in d0 directions containing every quadratic and
all but r cubic monomials forces

`m>=H_{d0}-(3/2)(d0+1)r`.                          (LP-face)

No completeness of the face is required. Its represented triples are
distinct, so its full triple collision excess is at most r.

Two useful consequences, including a small quartic allowance, are:

* If d>=5, an entire residue-complete tile cannot contain all
  quadratics, all but at most four cubics, at most two quartics, and
  no higher cells. Its cardinality is `P_d-r+k`, r<=4,k<=2, but
  (LP) exceeds that number: the difference is at least 6 at d=5
  and increases with d.
* If d>=6, a full cubic simplex with at most six cubics omitted is
  impossible. The corresponding difference is at least 13 at d=6
  and increases with d.

For the first comparison use
`2binom(d+1,3)-((3d+1)/2)r-k`; for the second set k=0,r<=6.

The 200,000-proposal packing run, seed 20261019, checked (LP) on all
84,001 pair-injective sets among them (s=3–8,m=7–200), without the
distinct-omitted-residues hypothesis used by the weighted linear
lemma. Every check passed.

**Distinct-weight H4.** If q>=1, all active integer weights are
pairwise distinct and exceed q, and M>=6q-3, then the P4 inequality
at scale q holds without any residue hypothesis.

Use exactly the table and injective assignment of section 7. The
only changed task is the early-ending column bound. The distinguished
largest weight b is now strictly larger than every weight in its base.

* For a floor-one quadratic at J=2, `n_a+n_b<=4q-3`. Thus the first
  two positive terms are at least 3 and 2, against the negative 1+3.
  At J=1 the first term alone suffices.
* For a floor-two quadratic the first term is at least 3, against 2.
* For a doubled-largest cubic the base unit has weight at most
  `(3q-3)/2`; its first positive term is at least 4. This case is
  empty for q<3.
* For a base of degree two at J=1, `v(z)<=4q-4`, so the first term
  is at least 2, against 1.
* For such a base at J=2, `v(z)<=2n_b-2<=3q-3`. The first term is
  at least 3; the second is at least 1 since
  `M-v(z)-n_b>=6q-1-3n_b>=q`.

These give one payment per deficit as before. For q=1 all deficits
are absent; the small q=2 cases satisfy the same bounds whenever
their indicated deficit exists. This proves the theorem. Residue
injectivity implies distinct active weights, so the original P4 is
now proved for M>=6m-3. Its remaining secondary interval is
`5m<=M<=6m-4`. No optimality of this distinct-weight cutoff is claimed.

`hd4_check.h` repeats the actual charge assignment at the new cutoff.
The exhaustive residue-free checks include 618,629 distinct-weight
instances in d=3,m=4–10 and 276,274 in d=4,m=5–8; all assertions
passed. These are cumulative counts from the last HD4 summary line.
Independent integer min-cuts passed for 3,990 tops at q=31 and 3,976
at q=30, using 1,000 distinct-weight vectors each, d=2–12 and
`n_a in [q+1,3q]`. Cardinality is independent of q in those tests.

## 16. Complete primary-regime proof for a=5

**Theorem.** Under the exact P4 hypotheses, `4m<=M<5m` and a=5
imply W>=0. Together with sections 5 and 13, the primary regime is
therefore proved whenever a<=5, for every rho.

We use the following finite Macaulay classification, also reproduced
by `a4_stability.py --a 5`. A negative WA has either

`(q2,q3,u3,u4,k,WA)=(0,14,0,30,0,-2)`,             (E5)

or all fifteen AA pairs are present, with the following rows. Put
`t=35-u3-u4`; each listed t-range gives the negative profiles in
that row, and `WA=-20+6(q2+u3)-4k+4t`.

| q2 | u3 | k | t |
|---:|---:|---:|---|
| 0 | 0 | 0 | 0–4 |
| 1 | 0 | 0 | 0–3 |
| 1 | 1 | 0 | 0–1 |
| 1 | 1 | 1 | 0–2 |
| 2 | 0 | 0 | 0–1 |
| 2 | 1 | 0 | 0 |
| 2 | 1 | 1 | 0–1 |
| 2 | 2 | 2 | 0 |
| 3 | 0 | 0 | 0 |

This is 22 profiles including (E5). To prove completeness, (LC-)
gives q2<=3. Put r_A=15-q2-q3. If r_A>=3, the cubic shadow and
L_a>=0 give `WA>=-20+(22/3)r_A>=2`. If r_A=2, Macaulay growth
from thirteen quadratics gives at most 26 cubics, hence t>=9 and
WA>=12. If r_A=1, at least five cubic multiples of the missing AA
are absent, so `WA>=L_a-2`. This is nonnegative if q2>=1; otherwise
negativity forces exactly (E5). For r_A=0, use
u3<=q2^{<2>} and k<=u3^{<3>} with q2=0,1,2,3. These give exactly
the displayed table, with no additional hypothesis on weights.

Assume WA<0 and W<0. Every E direction contributes at least 27 to
T, exceeding -WA<=20, so e=0. A C direction is excluded as well,
except possibly q2=u3=k=t=0 with q3=15,u4=35 and c=1. Indeed two
C directions cost at least 36, and one C costs at least 17, or at
least 18 when q2>=1; the other negative profiles have smaller
deficits. In the remaining c=1 case

`T=17+5b+t3`, `T+R<=19`,

so b=0. The term 4(ac-h) then forces all five AC pairs present.
The entire D has 56+1+5=62 cells, while its full five-direction
cubic face forces m>=H_5=96. Contradiction. Hence c=e=0 below.

Write

`B=b(b+1)/2`, `Z=b(b+1)(b+2)/6`, `p=5b-s3`,
`r_AB=5b-s3-s4`, `r_BB=B-t3-t4`,
`D_v=2b*q2+b*q3+6s3-4v2-3v3`,
`D_w=5t3+(b+1)s3-3w`, `D_z=(b+2)t3-3z`.

Except for (E5), all AA pairs are present. Then

`S:=T+R=p+b*u3+4r_AB+4r_BB+D_v+D_w+D_z+R_s`,
`S<=-WA-1`, `R_s=rho-t3-v3-w-z>=0`.              (A5.1)

The uniform neighbor lemma (A4.2) gives costs 10,17,21,22,20 for
one B direction missing 1,2,3,4,5 I3 A-neighbors. Thus there is at
most one such B direction, with p=1 or 2; p=2 is possible only
when q2=0. The following consequences are used repeatedly:

* If p=0, `4r_BB+D_w>=14r_BB+10t4`.
* If p=1, `D_w>=7(r_BB+t4)+2b-1`.
* If p=2, `D_w>=4(r_BB+t4)+4b-2`.
* If B>t3, `Z-z>=b`.

The first follows from w<=5t3. For the next two, let j be the B
direction missing p A-neighbors, and L_j the I3 BB pairs containing
j. Then `w<=5t3-pL_j`, `L_j>=b-(B-t3)`. Substitute into D_w.
The last is the b forbidden cubic multiples of a BB pair not in I3.

### The single missing-AA profile (E5)

Now S<=1. For a B direction with p_j missing A-neighbors, the same
derivation as (A4.2), allowing the one missing AA, gives a cost at
least `p_j(23-3p_j)/2-1` when p_j>0. This is at least nine, so all
B directions have all five I3 A-neighbors. Each then contributes
at least two to D_v: `14+6*5-3*14=2`. Thus b=0. The whole D has
50 cells, and deleting an endpoint of its missing AA leaves a full
four-direction cubic face. This forces m>=H_4=55. Contradiction.

### Full AA family, q2>=2

The largest possible deficit in the displayed rows is eight. The
neighbor cost ten forces p=0; the BB bound forces r_BB=t4=0. All
quadratics in d=5+b directions are therefore present. The three
mixed defects become

`D_v=4(b*q2-v2)+3(b*q3-v3)`,
`D_w=3(5B-w)`, `D_z=3(Z-z)`.

Every missing mixed cubic costs at least three. In each of the
seven rows/profiles with q2>=2, the number r of all missing cubics
is at most two, and k<=2. Explicitly

`r<=t+floor((-WA-1-b*u3)/3)<=2`.

The first near-simplex exclusion following (LP) applies for d>=5.

### Full AA family, q2=1

Here S<=13. Either p=0, or one B direction has p=1.

For p=0, r_BB=0 and t4<=1. If t4=0, the preceding defect display
implies r<=4 missing cubics and k<=1. The same near-simplex
exclusion applies. If t4=1, it is possible only in the t=0 row
with u3=k=0, WA=-14, or the t=0 row with u3=k=1, WA=-12.
The bound `D_z>=2b-2`, after D_w>=10, gives b<=2 in the first
case and b<=1 in the second. For b=1 the whole D has at most
P_6+1=85 cells but contains the full five-A cubic face, which
forces m>=96. For b=2 only the first row remains. The budget 13
forces every mixed cubic permitted by its one I4 BB pair to be
present: precisely five ABB and two BBB are missing. Thus d=7,
r=7,k=0, and (LP) gives `m>=H_7-12*7=148`, while m=P_7-7=113.

For p=1 the neighbor cost is at least ten. The case u3=1 would
require the WA=-12,t=0 row, but then S is at least
`10+b+(2b-1)>=12`, exceeding its budget eleven. Thus u3=k=t=0
and WA=-14. The remaining budget forces r_AB=r_BB=t4=0 and
b<=2. Again b=1 contradicts m<=84 versus the full A-face bound
96. At b=2 the neighbor cost ten and D_w>=3 exhaust the budget.
They force all permitted mixed cubics to be present: five AAB
and two ABB are omitted. There are again exactly seven omitted
cubics in seven directions, excluded by the same 148>113 bound.
(If the absent neighbor contains the unique low AA, its extra
unit of neighbor cost already contradicts the budget.)

### Full AA family, q2=0

Now u3=k=0, WA=-20+4t, 0<=t<=4, and S<=19-4t. At most one B
direction has a missing I3 A-neighbor, with p=1 or 2.

**p=0.** The bound `14r_BB+10t4<=19` gives
r_BB+t4<=1.

If r_BB=t4=0, the full tile has at most
`t+floor((19-4t)/3)<=6` missing cubics. For b>=1 use the second
near-simplex exclusion (d>=6,r<=6). For b=0, r=t<=4 and use the
first exclusion at d=5.

If r_BB=1,t4=0, then

`S>=12+2b+3E`,

where E counts missing mixed cubics beyond the d=5+b forced by the
missing BB pair. This follows by writing w=5B-5-e_w,
z=Z-b-e_z and v3=15b-e_v in the defect formulas. Consequently
b<=3, t<=1, and `t+E<=1`. Delete a B endpoint of the missing BB
pair. The remaining d-1 directions have all quadratics and at
most one missing cubic. Their (LP-face) lower bound is greater
than `P_d-d-1`, the largest possible whole cardinality. For
d=6,7,8 the lower bounds are respectively at least 87,143.5,220,
whereas those cardinalities are at most 77,112,156.

If r_BB=0,t4=1, then `S>=8+2b`; hence b<=5, t<=2.
The total number of missing cubics satisfies

`r<=floor((26+b-t)/3)`.

For b=2,3,4,5 these bounds are respectively 9,9,10,10. The
differences between the (LP) lower bound and P_d-r are at least
13,55.5,100,175, respectively. For b=1, all ABB and BBB are
absent. Its pure-A face forces `m>=96-9t`, while the whole
cardinality is at most `84-6-t=78-t`; the former is larger for
t=0,1,2.

**p=2.** Its neighbor cost seventeen forces t=0 and leaves budget
two. Thus all quadratics are present; the bound
`D_w>=4t4+4b-2` forces b=1,t4=0. The whole D has at most P_6=84
cells and contains the full five-A cubic face, contrary to m>=96.

**p=1.** Its neighbor cost ten forces t<=2. The strengthened BB
bound yields

`S>=9+2b+11r_BB+7t4+4r_AB`.

Thus r_BB=0. If t4=1, only b=1,t=0,r_AB=0 remains, excluded by
the full A-face bound 96>84. Otherwise t4=0 and r_AB is zero or
one. Writing E for missing cubics beyond the 5+b forced by the
one absent I3 AB neighbor gives exactly

`S>=9+2b+4r_AB+3E`.

If r_AB=0, then b<=5, and r=t+5+b+E obeys the same bounds
9,9,10,10 for b=2,3,4,5, excluded by the preceding (LP)
comparisons. At b=1, use again 96-9t>78-t for t<=2.

If r_AB=1, then b<=3 and t+E<=1. Delete a B endpoint of this
missing AB pair. The remaining face has all pairs and at most
one omitted cubic. The same deleted-variable comparisons
87>77,143.5>112,220>156 apply for d=6,7,8.

Every negative profile is excluded under W<0. This proves the a=5
theorem. All uses of small dimension above are exact cases forced
by the inequalities; b was not bounded by an experimental cutoff.
QED.

As an independent audit, `a5_critical.py --bmax 20` enumerated all
5,878 nonnegative count vectors surviving the necessary inequalities
for the full-AA profiles. It excluded 274 by A-face packing, 5,597
by whole-face packing, and seven by deleting an endpoint of a missing
pair. There were no survivors. This finite audit is supplementary;
the proof above gives the bounds for arbitrary b and treats (E5)
separately.

## 17. Sharp support constants and a congruence for heavy fibers

The linear packing constant can be improved without an omitted-residue
hypothesis. For s>=5 put

`L_s=(3/2)s` if 3 divides s, and `L_s=(3/2)(s-1)` otherwise.

For s=2,3,4 the corresponding constants are 1,2,4. If B0 has s
elements and injective unordered pair residues, and r is its triple
collision excess, then

`m >= H_{s-1}-L_s*r`.                            (SP)

Here H_{s-1}=s(s(s-1)/2+1), as before. The constant L_s is the
largest possible ratio

`[sum_{i<j} t_i*t_j]/(g-1)`

over g>=2, t_i in {1,2,3}, and sum t_i<=s. This is sharp as an
inequality about support sizes; no claim is made that every optimizing
support partition is realized by residues.

For completeness, write s=3k+r0, 0<=r0<=2. If g<=k, the ratio
is at most 9g/2. If g>=k+1, Cauchy's inequality bounds it by
s^2/(2g). This proves the stated maximum for r0=1, since
`(3k+1)^2<=9k(k+1)`. For r0=2, separate g=k+1: increasing the
support sum to s and balancing its entries gives k threes and one
two, and ratio `(9k+3)/2`. For g>=k+2, use
`(3k+2)^2<=(9k+3)(k+2)`. For r0=0, the earlier bound 3s/2 is
attained by k threes. These witnesses apply for s>=5; direct
enumeration of the partitions gives the three smaller constants.
Applying this ratio in each residue fiber proves (SP).

There is a further arithmetic improvement when s=3k>=6. A fiber
with g=k triples, each of support three and with union all of B0,
will be called a full-support fiber in this section. Its triples are
squarefree and disjoint, so if R is their common residue,

`k*R = sum_{b in B0} b (mod m)`.                  (HF)

Consequently there are at most gcd(k,m) such fibers. Every other
fiber has signed-label collision count at most

`(3s/2-3)(g-1)`.

Indeed, if its support sum is at most s-1, apply the just-proved
support constant L_{s-1}=3(s-2)/2. If its support sum is s, then
g>=k+1 unless it is a full-support fiber. Cauchy gives a ratio at
most `9k^2/[2(k+1)] <= (9k-6)/2`, since k>=2. A full-support
fiber contributes at most an additional 3(k-1) over this bound.
Summing proves the uniform residue-sensitive inequality

`m >= H_{s-1}-(3s/2-3)r-3(k-1)gcd(k,m)`.         (HP)

One may take the larger of the lower bounds (SP) and (HP).
For s=9, (HP) reads

`m >= H_8-(21/2)r-6gcd(3,m)`.

Unlike a bound that merely charges nine units for each pair of
colliding triples, this controls how often the maximum-size collision
fiber can occur. Its use of the cyclic group is explicit in (HF).

`packing_fibers.py` enumerates the support partitions exactly for
s=2–100, tests the bounds on actual pair-injective residue sets,
and audits the pure-A count profiles. The completed numerical counts
are recorded with the continuation verification below.

## 18. Primary regime a=6: a proof with two finite certificates

**Computer-assisted theorem.** Under the exact P4 hypotheses,
`4m<=M<5m` and a=6 imply W>=0, for every rho and every number of
outside directions. The two finite computations used in this section
are explicitly bounded below and have independent C and Python
implementations. Sections 13 and 16 are paper proofs; this section
retains these finite computations as dependencies.

Assume W<0. As usual, WA<0. Put

`r_A=21-q2-q3`, `t=56-u3-u4`,
`L=7(q2+u3)-4k`.

Then `WA=-35+L-3r_A+4t`, L>=0, and (LC-) gives q2<=4.
If r_A>=2, Macaulay gives t>=11 at r_A=2. Increasing r_A by one
increases its minimum t by at least one, so WA is at least
`-35-3*2+4*11=3`. Thus r_A is zero or one.

When r_A=1, t>=6, and the complete list of negative profiles is

| q2 | u3 | k | t | WA |
|---:|---:|---:|---|---|
| 0 | 0 | 0 | 6–9 | -14+4(t-6) |
| 1 | 0 | 0 | 6–7 | -7+4(t-6) |
| 1 | 1 | 1 | 6 | -4 |

Indeed L>=7q2 excludes q2>=2, and exact Macaulay growth for q2=0,1
gives precisely these seven profiles. When r_A=0, the profiles are
specified by the finite intervals

`0<=q2<=4`, `0<=u3<=q2^{<2>}`, `0<=k<=u3^{<3>}`,
`t>=0`, `L+4t<=34`.                              (A6.0)

There are exactly 75 such profiles. Here the degree-two growth
values for q2=0,...,4 are 0,1,2,4,5, and the degree-three growth
values for u3=0,...,5 are 0,1,2,3,5,6.

### Elimination of C and E

One E direction costs at least 39-r_A in T, exceeding every
possible deficit (at most 35, or at most 14 if r_A=1). Two C
directions cost at least 48-2r_A. For c=1 the exact lower bound is

`T>=23-r_A+q2+6b+t3+(b+1)u3`.

This excludes r_A=1, and also q2>=2. For r_A=0,q2=1 only
u3=k=t=b=0 can remain: the case u3=k=1 has deficit 25 and C
cost at least 25. Its whole cardinality is at most 91, versus
the A-face lower bound 154. For q2=0, u3=k=0 and the displayed
bound forces t<=2,b<=1. The whole D has at most
`P_{6+b}-t+7+b <=128-t` cells, while its A face forces
`m>=154-9t>128-t` for t<=2. Thus c=e=0.

### The one-missing-AA family

For one B direction with p_j missing I3 A-neighbors, the proof of
(A4.2), allowing the single missing AA, gives

`p_j+D_{v,j} >= p_j(27-3p_j)/2-1+3*eta_j`,

where eta_j=1 if that missing AA is entirely supported on the
remaining A-neighbors, and zero otherwise. A full-neighbor B
therefore costs at least two. A B with p_j>0 costs at least
11,20,26,29,29,26 for p_j=1,...,6.

If all B directions have full neighbors, the budget is at most
13, so b<=6 and every BB pair is in I3: a BB pair outside I3
would already cost at least 12 in D_w, in addition to 2b.
Let j=t-6 and let E be the number of omitted mixed cubics beyond
those forced by the one missing AA. Then

`S>=b(u3+2)+3E`,
`j+E<=floor((13-L-j-b(u3+2))/3)`.

Deleting an endpoint of the missing AA leaves d-1=5+b directions
with all quadratics and at most j+E missing cubics. For b=1,...,6,
the upper bounds on j+E are 3,3,2,1,1,0. Their (SP) lower bounds
on m are at least

`127, 200.5, 306, 446.5, 601, 804`,

while `m<=P_{6+b}-(6+b)` is respectively at most

`113,157,211,276,353,443`.

If some B has a missing neighbor, only the WA=-14,t=6,q2=0 row
can remain. There is exactly one such B, with p_j=1. The missing
AA must contain the missing A-neighbor; otherwise its cost is at
least 14. Including the other full B directions and
`D_w>=2b-1` gives `S>=4b+8`, so b=1. The BB loop is in I3,
the absent I3 AB pair is present in I4, and all mixed cubics
permitted by these shadows are present: any additional omission
would cost at least three, beyond the budget 13. Delete the
missing A-neighbor. The remaining six directions form a full
cubic face, forcing m>=154, although the whole D has at most
P_7=120 cells. Contradiction.

It remains in this family to consider b=0. Deleting a missing-AA
endpoint gives `m>=96-9j`, while `m=77-j+k`. This excludes j<=2.
The only survivor is

`m=74, q2=0,q3=20,u3=k=0,u4=47,WA=-2`,
`rho in {0,1}`.                                 (A6.1)

Here is the complete finite weight certificate for (A6.1). Write
`h=m-rho` and order the six weights as `n_i=m+t_i`,
`1<=t_1<...<t_6<h`. Choose the one omitted AA monomial. Every
other pair must have sum t_i+t_j>=h and distinct residues, also
distinct from 0 and all six units. If the omitted pair is not the
smallest variable's loop, every t_i>=ceil(h/2). If it is that
loop, t_1 may range from 1; the other pair inequalities are still
imposed. These cover every possible ordered weight vector.

There are at most fifty cubic monomials not divisible by the
omitted pair. Eligible ones satisfy `sum t_i<=m+h-1`. To realize
(A6.1), at least 47 eligible cubics must supply all residues not
already covered by the 27 lower cells, and one must attain the
prescribed maximum. Both `a6_one_pair.c` and `a6_one_pair.py`
enumerate this finite domain exactly. At rho=0 they find only two
eligible choices: the same vector

`(t_1,...,t_6)=(38,39,42,43,49,51)`

with omitted pair (1,4) or (2,3), using one-based indices. Each
leaves eighteen residues uncovered, namely

`1,5,9,21,22,23,25,27,29,30,31,32,33,34,35,36,37,72`.

At rho=1 no choice has the required number of eligible cubics.
The implementations agree on 663,140 and 525,989 lower-face
weight/pair choices and on all eligible outputs. This excludes
(A6.1), completing the one-missing-AA family.

### Full AA family: reducing arbitrary b to b<=11

For a full AA face write p_j=6-|N_j|. The neighbor costs are
12,21,27,30,30,27. Since the entire budget is at most 34, the
multiset of positive p_j is one of

`(), (1), (2), (3), (4), (5), (6), (1,1), (1,2)`. (A6.2)

Put q=r_BB+t4. With one bad B of deficiency p, the BB-neighbor
count gives

`D_w>=12q-p(b+1)+3p*max(0,b-q)`.

Minimizing over q gives respectively
`2b-1,4b-2,6b-3,8b-4,7b-5,6b-6` for p=1,...,6. For two bad
B directions of deficiencies (1,1), the analogous lower bound is
4b-5; for (1,2), it is 6b-6. Adding their neighbor costs shows
that a nonempty multiset in (A6.2) requires b<=11. In fact the
sharper bounds are b<=11,3,1,1,1,2,3 respectively, and (1,2)
is impossible.

Suppose now b>=12. Then every AB pair is in I3 and q<=2, from
D_w>=12q. Let r be the total number of missing cubics in d=6+b
directions. Exact algebra gives

`S=b*u3+4r_BB+3(r-t)-(b+8)q+(b*q2-v2)+R_s`.

Since `S<=34-L-4t`, this implies

`r<=(2b+50)/3=(2d+38)/3`.                        (A6.3)

Also k<=6. If r_BB=2, the missing BB pairs force at least
2d-1 missing cubics, contradicting (A6.3) already at b>=12.
If r_BB=0, compare the whole cardinality `P_d-r+k` with
the universal packing bound. Six times the difference is at least

`2d^3-6d^2-118d-74>0` for d>=18.

If r_BB=1, delete one endpoint of that BB pair. At most r-d
cubics are missing in the remaining face. Six times its packing
lower bound minus the upper cardinality `P_d-1-r+6` is at least

`2d^3-6d^2-115d+40>0` for d>=18.

Both polynomials are positive at 18 and increasing thereafter.
Thus b>=12 is impossible. This reduction uses no finite b search.

### Full AA family: the finite count certificate at b<=11

For clarity, here is the exact finite domain checked by the two
implementations. Start with (A6.0), b=0,...,11, and a multiset
(A6.2) with at most b entries. Put

`B=binom(b+1,2)`, `Z=binom(b+2,3)`, `p=sum p_j`,
`s3=6b-p`, `ellost=sum_j[21-binom(7-p_j,2)]`.

Let l range from zero to min(q2 times the number of bad B
directions, ellost); it represents the lost low-AA neighbors.
Use

`0<=v2<=b*q2-l`, `0<=v3<=b*q3-ellost+l`,
`0<=r_AB<=p`, `0<=r_BB<=min(B,floor(budget/4))`,
`0<=t4<=B-r_BB`, `t3=B-r_BB-t4`,
`budget=34-L-4t`.

For each BB pair (j,k), assign a lower bound max(p_j,p_k) to
its missing A-neighbors, padding (A6.2) by zeros. Delete the
r_BB+t4 largest such lower bounds and let Lkeep be the sum of
the rest. Then impose

`0<=w<=min(6t3-Lkeep, floor((b+1)s3/2))`,
`0<=z<=min(t3^{<2>}, Z-b)` if r_BB+t4>0,
`0<=z<=Z` otherwise.

Finally require

`S=p+b*u3+4r_AB+4r_BB+D_v+D_w+D_z<=budget`,

where D_v,D_w,D_z have the definitions of section 16 with a=6.
Dropping R_s only enlarges this domain. Every actual negative-W
tile satisfies these necessary conditions.

There are exactly 36,389 integer vectors in this domain. Apply
the following packing exclusions in order: the pure-A face (SP);
the whole face (SP) and then (HP) when all its quadratics are
present; and, when q0=r_AB+r_BB>0, the face obtained by deleting
an endpoint of each missing quadratic, when d-q0>=1. In the last test at most

`r-[q0*d-binom(q0,2)]`

cubics are omitted in the remaining d-q0 directions. The term
in brackets is a valid lower bound on the forced missing cubics:
each missing quadratic has d cubic multiples, and two such
sets intersect in at most one cubic.

The counts excluded by these tests are respectively 3,118;
32,639; 65; and 564. Exactly three vectors remain. All have
`q2=u3=k=0,t=1,b=2,m=148,r=16`, with the following data:

| bad p_j | r_AB | r_BB | t4 | v3 | w | z | S |
|---|---:|---:|---:|---:|---:|---:|---:|
| none | 0 | 1 | 1 | 42 | 6 | 1 | 29 |
| 1 | 0 | 1 | 0 | 36 | 11 | 2 | 30 |
| 1 | 1 | 0 | 1 | 36 | 11 | 2 | 30 |

These three are excluded on paper. In the first row the one I3
BB pair must be a loop, since z=1; a cross pair alone has no
BBB multiple with all BB divisors in I3. Every permitted mixed
cubic is present. Keep that B direction and all six A directions.
They have a full quadratic face and only one missing cubic.
For the other rows, exactly one B has all six A-neighbors. Of
the two I3 BB pairs, one must be the good B's loop: otherwise
both involve the bad B, losing at least two ABB cells and
contradicting w=11. Again v3,w,z attain every permitted cap.
Keeping this good B and the A directions gives the same face.
In all three rows (SP) therefore forces

`m>=H_7-(21/2)*1=221.5>148`.

The finite count lemma is checked by `a6_critical.py --bmax 11`
and independently by `a6_count_check.c`. The latter enumerates
losses from the caps in nonnegative cost increments, whereas the
former enumerates the actual counts. They agree on all 36,389
vectors, every exclusion count, the three final shapes, and zero
survivors. The C certificate does not call the target inequality
as an oracle. Together with the analytic reductions and the
independent weight certificate for (A6.1), this proves the stated
computer-assisted a=6 theorem. QED.

## 19. Pure-A, upper-AA family at a=7: a finite coverage exclusion

**Computer-assisted subcase.** Suppose a=7, b=c=e=0, every AA
monomial is present, and q2=0. Then W>=0 for every rho.

Every A weight has the form n_i=m+t_i with
`ceil(h/2)<=t_i<h`, h=m-rho, because all its squares are in I3.
Consequently u3=k=0. Put t=84-u4. Then

`m=120-t`, `W=-56+4t+rho`.

From (SP), `120-t>=232-(21/2)t`, giving t>=12. If W<0 then
t<=13. Thus only the following parameter sets can remain:

* m=107,t=13,rho=0,...,3;
* m=108,t=12,rho=0,...,7.

For each parameter set, enumerate all increasing seven-element
vectors t_i in the interval above with injective lower-face
residues. There are 36 lower cells. Every eligible cubic has
`T=t_i+t_j+t_k<=m+h-1`, and the maximum requires equality for
at least one such cubic. Taking the union of the lower residues
and **all** eligible cubic residues gives a necessary coverage
condition, independently of any choice of representatives.

`a7_cover.c` performs this exact enumeration, using a monotone
bound on the number of ineligible cubics to prune. Independently,
`a7_independent.py` enumerates the pair-injective sets without
that cubic pruning. The eligible and maximum-attaining counts
agree in every parameter set. None covers all residues. Among
candidates that can supply enough cubics and the prescribed
maximum, the smallest number of uncovered residues is 24,
at m=107,rho=1. For m=108,rho=3 there is no candidate with enough
eligible cubics. This exhausts the parameters forced by the
inequalities and proves the stated subcase. QED.

The minimum-24 example has

`(t_i)=(53,55,56,63,69,74,78)` at m=107,rho=1.

It is a failed candidate for residue coverage, not a Wilf
counterexample or a nearly tight residue-complete semigroup.
The other best-cover vectors and every missing residue are
retained in `a7_independent.log`.

## 20. Continuation verification, failed steps, and reproducibility

All execution, compilation, exact arithmetic, random generation, and
compression in this continuation took place on fejer. Jobs used
`nice`, at most four cores in total, and the private directory
`~/wilf/p4/continue/`. Local actions were reading, editing, and copying
files. No commits were made. The lead-verified sections 1–11 are
retained without alteration.

### Exact and exhaustive checks

| Claim / object | Source and log | Range and result |
|---|---|---|
| Negative A profiles | `a4_stability.py`; `a4_catalog.log`, `a5_catalog.log`, `a6_catalog.log` | Exact Macaulay count relaxations: 6 profiles at a=4, 22 at a=5, 82 at a=6 (75 with full AA and 7 with one missing AA). |
| Uniform (LC) | `uniform_lowcost.py`; `uniform_lowcost.log` | All 1,446,390 permitted integer (q2,u3) pairs at a=3–24, taking maximal k; 19,698 rational factorization/sign checks at a=3–100. All passed. |
| Universal (LP) | `a4_stability.py`; `packing_linear.log` | 200,000 proposals, seed 20261019; 84,001 pair-injective residue sets at s=3–8,m=7–200. All passed. |
| Sharp support constants | `packing_fibers.py`; `packing_fibers_hp.log` | Every support partition at s=2–100 agrees with the closed formula. |
| Actual-residue (SP),(HP),(HF) | Same script/log | 200,000 proposals, seed 20261023; 67,738 pair-injective sets, including 10,174 nonvacuous (HP) checks and 493 full-support fibers. The s=9 sample has 879 sets; the s=12 sample has one. All passed. Actual s=9 witnesses are saved in `heavy_fiber_examples.json`. |
| a=5 critical counts | `a5_critical.py`; `a5_critical.log` | b=0–20; 5,878 vectors. A-face packing excludes 274, whole-face packing 5,597, and deletion of a missing-pair endpoint seven. No survivors. The paper proof supplies bounds for arbitrary b. |
| a=6 critical counts | `a6_critical.py`, `a6_count_check.c`; `a6_critical_b11.log`, `a6_count_check.log` | Exactly 36,389 vectors at the analytically forced b=0–11. Both implementations agree on every exclusion count and no survivors. |
| a=6 exceptional weights | `a6_one_pair.c`, `a6_one_pair.py`; corresponding logs | m=74,rho=0,1, all missing-AA choices and all ordered A weights. Counts and all eligible outputs agree; 18 uncovered residues in each of the only two eligible cases. |
| a=7 pure-A coverage | `a7_cover.c`, `a7_independent.py`; `a7_m107.log`, `a7_m108.log`, `a7_independent.log` | All 12 parameter sets forced in section 19. Independent enumeration without cubic pruning agrees on every eligible/maximal count and coverage minimum. No completion. |
| Distinct-weight H4 | `hd4_check.h`; `hd4_nores3.log`, `hd4_nores4.log` | All canonical shapes in d=3,m=4–10 and d=4,m=5–8, all distinct n in [m+1,3m]: 618,629 and 276,274 checks respectively. All charge/capacity assertions passed. |
| Independent H4 closures | `hd4_closure.py`; `hd4_closure31.log`, `hd4_closure30.log` | 1,000 distinct-weight vectors each at q=31 and q=30, d=2–12, n in [q+1,3q]; 3,990 and 3,976 integer min-cuts. All passed. Here q need not equal cardinality. |

`a6_reduction_check.py` additionally audits the C/E elimination,
the neighbor minima in the arbitrary-b reduction, and both displayed
polynomial identities using exact arithmetic. This supplements the
paper arguments; it does not replace their unbounded quantifiers.

The final genus-tree run (`tree28_fiber_noinline.log`) visits all
5,311,726 semigroups of genus at most 28, including 642,239 in
`3m<c<=4m`. It verifies the original band, transfer, shadow, residue,
and carry assertions, and the new assertions whenever their
hypotheses apply. The primary a-distribution is:

`a<=3: 640,993; a=4: 1,116; a=5: 122; a=6: 8; a>=7: 0`.

There are 98,808 actual-face (SP) checks, 8,894 (LC) checks, and
three full-AA neighbor checks with a>=3. No (HP) face occurs in
this small-genus tree; its nonvacuous checks are the random residue
sets above. None of the genus-28 cases has a negative WA face at
a=4,5,6. Thus this tree alone cannot validate the delicate negative
profiles. The separate large-m constructions and finite certificates
are essential.

The new canonical residue-complete scan (`scan4_fiber.log`) covers
d=4,m=5–12, all residue vectors and lifts 1–4, and makes 19,678
actual-face (SP) checks and 10,424 (LC) checks. The earlier
continuation scan (`scan4_a4.log`) extends the original a=4
predicates to m=16, with 7,181 primary a=4 instances in total.
The seven saved explicit completions, including the m=74 quartic
example below, are independently rechecked in C (`cases_check.log`),
with 36 full-AA neighbor checks and all direct identities passing.

**Verifier build failure, retained.** The first optimized genus-tree
binary exited 139 with the default stack limit; that run contributes
no verification count. GCC's `-fstack-usage` output records a
331,696-byte frame for the recursive `visit` after inlining, so the
genus-28 recursion exceeds the default 8 MiB stack. The same
optimized build passes genus 28 with a 64 MiB process stack
(`tree28_fiber_stack.log`). The final build instead uses
`-O2 -fno-inline` and passes the full tree with the default stack.
An AddressSanitizer diagnostic run through genus 12 also passed.
The initial empty logs, stack-usage output, and successful diagnostic
logs are retained. No assertion failure is concealed by this repair.

### Adversarial residue-complete constructions

`continuation_probe.py` keeps all eligible pure-A cells when their
residues are distinct, adds B directions with a greedy search for
small W, and completes every unused residue by an E singleton.
Every stage is checked directly, independently of the count proof.
These are finite down-sets satisfying the exact target hypotheses.

* a=4, seed 20261020: 2,000 proposals, m=60–240; 112 accepted
  negative faces and 672 additional stages with b=1–6. The profiles
  include 18 low-AA quartic faces. The smallest W in this batch is
  1,102 at m=91,rho=38,b=6,e=23,WA=-6.
* a=5, seed 20261021: 2,000 proposals, m=120–700; 113 accepted
  negative faces and 339 additional stages with b=1–3, including
  thirteen quartic faces. Smallest W is 3,680.
* a=5 low-pair stars, seed 20261022 (`a5_star_probe.py`): 5,000
  proposals, m=200–700; 269 accepted negative faces and 538 B
  extension stages. The accepted low-band profiles include q2=2
  with (u3,k)=(0,0),(1,0),(1,1),(2,2), and q2=3 with (0,0).
  Smallest W is 8,408.
* a=6, seed 20261024: 1,500 proposals, m=180–1,000; 23 accepted
  negative faces and 69 stages with b=1–3, including a quartic
  face. Smallest W is 25,753.

The a=4 and a=5 batches include rho close to m; positive rho and
q2 are exercised extensively. Full coordinate/weight artifacts are
saved, with compressed copies of the large JSON files. These
particular searches did **not** produce a new nearly tight actual
family. Their large positive W is reported as such; the incomplete
coverage vectors from section 19 are not substituted for actual
semigroups.

### Failed intermediate steps, with scope of the counterexamples

1. **WA<0 need not mean q2=0 or k=0, even at a=4.** The smallest
   example in the exact profile-III parameter search is m=74,
   rho=37, with A weights `(83,102,104,107)`. Take every pure-A
   monomial of degree at most three, together with 4e_1. These
   36 cells have distinct residues. Complete the other 38 residues
   by E singletons, using their representatives in [259,333).
   Then M=332, d=42, ell=28,
   `(q2,q3,u3,u4,k,WA)=(1,9,1,19,1,-4)`, and W=945.
   The full coordinates are in `quartic_counterexample.json` and
   were checked independently in C. `quartic_face_search.c`
   exhausts m=36–73 before finding this m=74 case; it also allows
   the prescribed maximum to lie in the A face. An earlier search
   that required the maximum to be supplied by E found m=76.
   That restricted result is retained in `quartic_min.log`, and
   is not a global minimality claim.

2. **The sharp support constant and elementary shadows alone do
   not exclude the a=6 count relaxation.** The b<=20 relaxation
   before (HP) has 68 survivors in twelve groups, recorded in
   `a6_critical_before_hp.json`. One smallest-m survivor has
   `a=6,b=2,q2=0,q3=21,u3=k=0,u4=54`, all AB pairs in I3,
   all BB pairs present with `(t3,t4)=(1,2)`, and
   `(v3,w,z)=(42,6,1)`. It has m=148,r=17,WA=-27,S=25.
   These are abstract counts, **not** a residue-complete down-set
   or a Wilf counterexample. They satisfy the stated shadow and
   (SP) tests. The new (HP) bound is `m>=148.5`, excluding them
   by a half-unit before integer rounding. After (HP), only the
   three explicitly analyzed m=148 rows in section 18 remain.

The earlier false cutoff and residue-free claims in sections 7–11
remain recorded there.

### Reproduction and archive

Representative commands, all executed inside the private fejer
directory, are:

```sh
cd ~/wilf/p4/continue
nice python3 a4_stability.py --a 4
nice python3 a4_stability.py --a 5
nice python3 uniform_lowcost.py --amax 24
nice python3 packing_fibers.py --constants --trials 200000
nice python3 a5_critical.py --bmax 20
nice python3 a6_critical.py --bmax 11
nice gcc -O2 a6_count_check.c -o a6_count_check
nice ./a6_count_check
nice gcc -O2 a6_one_pair.c -o a6_one_pair
nice ./a6_one_pair
nice python3 a6_one_pair.py
nice gcc -O2 a7_cover.c -o a7_cover
nice ./a7_cover 107 0 3
nice ./a7_cover 108 0 7
nice python3 a7_independent.py
nice gcc -O2 -fno-inline -I.. a4_tree.c -o fiber_tree_noinline
nice ./fiber_tree_noinline 28
nice gcc -O2 -fno-inline -I.. a4_scan.c -o fiber_scan
nice ./fiber_scan 4 5 12
nice python3 continuation_summary.py
```

The compiler includes the unchanged original `p4_check.h` and
`h4_check.h` from the parent directory. Exact final source hashes,
raw logs, full finite-count artifacts, and C/Python agreement checks
are collected in `continuation_summary.json`. Local evidence copies
are under `logs/continuation/`; the working originals remain on
fejer. This archive distinguishes final passing runs, earlier
relaxations that had survivors, and the build failure above.

## 21. Consolidated result and exact remaining frontier

Under the exact multiplicity-form hypotheses in the task, P4 now
holds in each of the following cases:

1. M<4m, by GW-19 / P3.
2. 4m<=M<5m with a<=5, by the paper proofs in sections 5,13,16;
   with a=6, by the two independently checked finite certificates
   and the unbounded reductions in section 18.
3. M>=6m-3, by distinct-weight H4 in section 15. Residue
   bijectivity makes active weights pairwise distinct.
4. Total degree at most two, for every M, by section 8.
5. The saturated EF subcase at rho=0 and arbitrary a, by section 6;
   also the pure-A, full-AA, q2=0 subcase at a=7 and every rho,
   by the finite coverage proof in section 19.

This consolidates the continuation results; the open-range remarks
in sections 9,11,13 describe earlier stages and are superseded here.
For semigroups, item 2 proves Wilf in `3m<c<=4m` whenever at most
six minimal generators lie in `(m,c-2m)`, with the a=6 step
computer-assisted.

**The full task remains open in this report.** No counterexample
to Wilf or to the exact P4 target was found. The primary unresolved
statement is exactly RC4, now needed only for a>=7:

`(a-1)q3 <= 18(Q-q2-q3)+4D3+2Dlow+3D4+3T+3R`,

under all original down-set, weight, residue-completeness and primary
band hypotheses. Here

`D3=(a+2)(q2+q3)-3(u3+u4)`,
`Dlow=(a+2)q2-3u3`, `D4=(a+3)u3-4k`.

Even in the pure-A, full-AA, q2=0 family with no outside directions,
the uniform remaining claim for a>=8 is the precise inequality

`4[binom(a+2,3)-u4]+rho >= binom(a+1,3)`.

The secondary unresolved statement is P4 for residue-complete
down-sets with a cubic cell and `5m<=M<=6m-4`.

**Strategic review.** The low-band cost lemma is uniform and shows
how missing AA cells and low-band mass reduce the negative budget.
The new congruence (HF) controls the most expensive collision fiber
and is decisive for a=6. However, increasing the dimension cutoff
one at a time does not establish uniform RC4. In the pure-A family
WA<0 still permits on the order of a^3 missing cubics, while the
support packing loss can cost on the order of a per omitted cubic.
That dimensional loss is too large for an unbounded proof.

Accordingly, further fixed-a enumeration is not being promoted to
the main mechanism. The next mathematical gap is to control
heavy triple-residue fibers with unused generator labels, using
the integer band and complete residue coverage, and charge their
excess to T+R or to column slack. The a=7 coverage enumeration
shows a substantial gap between the abstract packing relaxation
and actual admissible weights, but does not itself supply this
uniform lemma. The next proof attempt should target that gap;
the secondary cubic window still needs a separate residue argument.
