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
