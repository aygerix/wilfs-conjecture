# P13: depth-four overlap credit

2026-10-19. **Partial result.** The full assertion for `3m<c<=4m` is not
proved here. The new results are uniform structural inequalities, with
complete proofs, on actual Apéry sets. No unproved packing statement is
used. Earlier reports are unchanged. All computation is on fejer in
`~/wilf/p13/`, with at most four of our nice single-core jobs.

## 1. Results and exact frontier

Let `S` have multiplicity `m`, other minimal generators `n_1,...,n_d`,
and Apéry set `Ap`. Throughout this report

    M=max Ap=4m+h-1,  c=3m+h,  1<=h<=m,  rho=m-h,
    lambda(v)=floor((M-v)/m),  s(v)=(M-v) mod m,
    L1(v)=sum_a depth_a(v)[lambda(v-n_a)-lambda(v)],
    Lambda=sum_(w,a) lambda(top_a(w)),
    K(v)=4-lambda(v)-L1(v).

The sum in `L1` includes only directions with positive depth. Let
`J(v)=sum_a depth_a(v)` and `U(v)={a:v-n_a in S}`. An Apéry value
is UF if it has one factorization over the minimal generators other
than `m`, and MF if it has at least two. Every primitive is UF.

The conductor-aligned unit classes are A, B, C, E, with unit co-levels
three, two, one, zero respectively. Thus A consists of
`m<n<c-2m=m+h`, B of `m+h<=n<2m+h`, C of
`2m+h<=n<c`, and E of `c<=n<=M`.

**Theorem A (PROVED; integer overlap payment).** Every MF Apéry value
at depth four satisfies

    lambda(v)+L1(v)>=5,  equivalently K(v)<=-1.       (MF-UNIT)

In particular `m L1(v)>v`. Every nonzero Apéry value satisfies
`K(v)<=1`. If `K(v)=1`, then `v` is UF and is exactly one of:

1. a B--B pair with co-level one;
2. a B--C pair with co-level zero;
3. a cubic of co-level zero, all of whose pair divisors have co-level one.

Call these values critical. Write `R` for their number, `R_A` for
those in item 3 whose three factors are A, and `R_out=R-R_A`.

**Theorem B (PROVED; uniform overlap-count inequality).** Put

    Z=sum_v (-K(v))^+,
    C_U=sum_(v MF) max(1,lambda(v)+|U(v)|-4).

Here `C_U` is an integer count credit. It is not `E_U/m`, and the
theorem does not claim that the lower-cover value credit pays each
landing point separately.

Then

    W=rho+Lambda-R+Z,
    R_out<=rho,
    Z>=C_U>=#{MF values},
    W>=Lambda+C_U-R_A.                            (COUNT-PAY)

Consequently Wilf holds for every depth-four semigroup satisfying

    R_A <= Lambda+C_U.                             (A-OVERLAP)

Dropping `Lambda` gives a condition involving only factorization
multiplicity, lower covers and co-levels, with no full-chain computation.
This is a proved infinite structural class, uniform in `a`, `alpha`,
embedding dimension and multiplicity.

**Corollary C (PROVED; overlap majority).** Wilf holds if

    R_A <= #{MF Apéry values}.

In particular it holds if at least half of the decomposable Apéry
values have more than one factorization:

    2 #{MF values} >= m-1-d.                        (MF-HALF)

The latter is a sufficient condition, not a necessary condition for Wilf.

**Theorem C2 (PROVED; shadow-assisted overlap payment).** Write
`D_dec=m-1-d` and `F_M=#{MF values}`. If `a>=1`, then

    (a+5)W >= (a+5)(Lambda+C_U)-(a-1)(D_dec-F_M).    (SHADOW-PAY)

In particular either of the following explicit hypotheses implies Wilf:

    (a+5)(Lambda+C_U)+(a-1)F_M >= (a-1)D_dec,       (SHADOW-OVERLAP)
    2(a+2)F_M >= (a-1)D_dec.                       (MF-SHADOW)

This improves the one-half threshold in (MF-HALF) to
`(a-1)/(2(a+2))`. For example the threshold is `3/7` when `a=19`.
It approaches one-half as `a` grows. For `a=0`, `R_A=0` already gives
`W>=Lambda+C_U`; no division by `a-1` is used.

**Theorem D (PROVED; the stronger WILF+ criterion on a structural class).**
CHAIN-POOR and WILF+ are identical at depth four. Both hold whenever

    R <= Lambda + floor[rho(m+h-1)/(2m)].             (UF-SPARSE+)

Section 5 gives a stronger count test using holes in the short residue
interval and long-residue critical cells. None of these statements
asserts CHAIN-U on the entire depth-four class.

**Scope.** These theorems close every member of the P11 residual
satisfying their explicit factorization hypotheses, without a bound on
`alpha` or an extra per-`alpha` sweep. They do not give a numerical range
of `alpha` or `a` that automatically satisfies those hypotheses. The
remaining family still requires a geometric argument controlling many
critical UF A-cubics; it is stated precisely in Section 10.

## 2. Re-derivation of the overlap and link identities

For each `v in Ap`, exactly `lambda(v)` members of
`v+m*N` lie below `c=M-m+1`. Hence
`ell=sum_v lambda(v)` and `W=(d+1)ell-c`. Residue completeness
also gives

    sum_v floor(v/m)+ell=c,
    sum_v v=m(c-ell)+C2.                           (AP-SUM)

Indeed `floor(v/m)+lambda(v)=4-[v mod m>h-1]`, and
exactly `rho` residues satisfy the indicator. These facts justify
the Wilf normalization directly, without a factorization tile.

If `v in Ap` and `v-j n_a in S`, then `v-j n_a in Ap`: otherwise
adding `j n_a` to a representation of `v-j n_a-m` contradicts
`v-m notin S`. Hence its factorization followed by `j` copies of
`n_a` shows

    depth_a(v)=max_(x in Z(v)) x_a.

Thus `J` is the degree of the coordinatewise join. Distinct
factorizations of a fixed positive value are incomparable. Therefore

    E(v)=sum_a n_a depth_a(v)-v>=0,

with equality exactly for UF values. The lower-cover bound follows by
replacing each positive depth by one and then taking the positive part.

For a link `v-n_a -> v`, set

    r_a(v)=s(v-n_a)-s(v),
    P(v)=sum_a depth_a(v) r_a(v).

The equality

    r_a(v)=n_a-m[lambda(v-n_a)-lambda(v)]

gives `P(v)-E(v)=v-m L1(v)`. Every layer drop is at least one,
since `n_a>m`, so `L1(v)>=J(v)`.

For a chain `v_0,...,v_l` in one direction, with depth `j` at
`v_j`, telescoping gives

    sum_(j=1)^l j[lambda(v_(j-1))-lambda(v_j)]
       =sum_(j=0)^l lambda(v_j)-(l+1)lambda(v_l).

Summing over all chains and all directions proves

    sum_v L1(v)=d ell-Lambda.                       (TELE)

Here `ell=sum_v lambda(v)`. Equivalently the link deficit satisfies
`Delta=sum_v P(v)-m Lambda`, as in the lead's identity.
One can check this independently in each chain by telescoping
`sum j(s_(j-1)-s_j)=sum s_j-(l+1)s_l`, including `j=0`
with weight zero. Summing over directions uses `sum_v s(v)=C2`
and gives `sum P=d C2-B_chain+m Lambda`, as required.

Also, with `g(v)=v-mL1(v)`, (TELE) and (AP-SUM) give

    sum_v g(v)-m Lambda=C2-mW.                     (BAL-ID)

Thus `sum g^+-m Lambda<=C2` implies Wilf. Since
`P=g+E>=g`, the corresponding CHAIN-POOR inequality implies it
as well. The equality of these two positive-part tests at depth
four will follow from MF-UNIT, rather than being assumed.

Consequently

    sum_v K(v)=4m-(d+1)ell+Lambda,
    W=(d+1)ell-(3m+h)=rho+Lambda-sum_v K(v).         (K-ID)

This last identity is valid independently of the multiplicity
classification below; it is not by itself a proof of Wilf.

## 3. MF-UNIT: every overlap pays an integer unit

**Proof of Theorem A for MF values.** If `J(v)>=5`, then
`lambda(v)+L1(v)>=5` already. Assume henceforth `J(v)<=4`.
Choose two distinct factorizations
`x,y` of `v` and let `z=min(x,y)` coordinatewise. Their remainders
`x-z,y-z` have disjoint supports. Each remainder has degree at least
two. Indeed a remainder of degree one would express a minimal generator
as a sum of other positive generators, or equate two distinct minimal
generators. A zero remainder is impossible by positivity and equal value.

If `z!=0`, then `|x join y|>=|z|+4>=5`, a contradiction.
Thus the supports are disjoint and both factorizations are quadratic.
The same argument with any third factorization shows that it also
has degree two; a factorization of degree at least three would have
join degree at least five with one of the chosen factorizations.

The only remaining possibility is that the full join has degree four.
Then `x,y` are disjoint quadratic factorizations, and all factorizations
of `v` have degree two. Their supports and multiplicities account for
all four units of the join. A quadratic Apéry value has co-level at
most two.

- If `lambda(v)>=1`, each lower cover has co-level at least
  `lambda(v)+1`. Therefore `L1(v)>=4`, and
  `lambda(v)+L1(v)>=5`.
- If `lambda(v)=0`, each quadratic factorization has sum of the
  co-levels of its two generators at least three. To see this, E units
  cannot appear in a pair, and two C units have sum at least
  `4m+2h>M`. The smallest possible co-level sum is consequently the
  B--C value `2+1=3`. The two disjoint factorizations give
  `L1(v)>=3+3=6`.

Thus (MF-UNIT) holds in every case. Moreover

    m L1(v) >= m(5-lambda(v))
             > M-m lambda(v) >= v,

using `M<5m`. This proves strict richness as well. QED.

The argument also proves the earlier, weaker statement that every MF
value is rich. The extra integer unit in (MF-UNIT) is what is spent in
the majority theorem; richness alone would not give that unit.

## 4. Classification of critical UF values and the short arc

Let `v` be UF with unique factorization `x`, of degree `j`. Then
`depth=x`, and `j<=4`, since `v<=M<5m` and every generator exceeds `m`.
The origin has `K=0`; a primitive has
`L1=4-lambda(v)` and also `K=0`.

For `j=2`, writing the two factors with repetitions as `n_a,n_b`,

    K(v)=4+lambda(v)-lambda(n_a)-lambda(n_b).

The possible unit-class pairs give the following complete table.

| factors | maximum possible lambda(v) | K(v) |
|---|---:|---:|
| AA | 2 | at most 0 |
| AB | 1 | at most 0 |
| AC | 0 | 0 |
| BB | 1 | lambda(v) |
| BC | 0 | 1 |

Pairs containing E and pairs CC are impossible by value. Thus the
only positive cases are the two quadratic types in Theorem A.

For `j=3`, no C or E factor is possible: already a C and two other
generators exceed `M`. If `lambda(v)=1`, every pair divisor has
co-level at least two and `L1>=3`, so `K<=0`. If `lambda(v)=0`,
every pair divisor has co-level at least one. Equality `K=1` means
`L1=3`, precisely that all pair divisors have co-level one. Otherwise
`K<=0`. A quartic has co-level zero and `L1>=4`, so `K<=0`.
Together with MF-UNIT, this proves all of Theorem A.

**Short-arc lemma (PROVED).** Every critical value other than a pure-A
cubic has `s(v) in [0,rho)`. Indeed:

- a critical BB pair has `v>=2m+2h` and co-level one, so
  `s(v)=M-m-v<=m-h-1`;
- a BC pair has `v>=3m+2h` and co-level zero, giving the same bound;
- for a critical cubic containing a B factor, its opposite pair has
  co-level one and value at least `c-m=2m+h`. Adding the B factor
  gives `v>=3m+2h`, again `s(v)<=rho-1`.

The residues `s(v)` are distinct on Apéry, so `R_out<=rho`.
This is an Apéry-only version of the relevant joint short-residue count.

## 5. The structural Wilf and WILF+ bounds

Since every positive `K` equals one, `sum K=R-Z`. Identity (K-ID)
therefore proves the exact first line of (COUNT-PAY). For an MF value,

    -K=lambda+L1-4 >= max(1,lambda+J-4)
                           >=max(1,lambda+|U|-4).

All other contributions to `Z` are nonnegative. Combining this with
`R_out<=rho` gives

    W >= Lambda+C_U-R_A.

This proves Theorem B and (A-OVERLAP). Since `C_U>=#{MF}`,
Corollary C follows. There are `m-1-d` decomposable Apéry values;
`R_A` counts only UF decomposable values, so
`R_A<=m-1-d-#{MF}`. This proves (MF-HALF).

### 5.1 Pair shadows give additional credit

Let `P_A` be the set of distinct pair values dividing at least one
critical pure-A cubic, and put `p_A=|P_A|`. Such a pair is UF: an
alternative factorization could be multiplied by the remaining factor
to contradict uniqueness of the cubic. Its co-level is one. It is an
AA pair, hence the pair table gives `K=-1`.

Each pair value in `P_A` therefore earns a unit of `Z`, separately
from all MF credits. Moreover a UF pair has just one pair monomial.
Thus ordinary weighted shadow incidence, entirely within the A
directions, gives

    3R_A <= (a+2)p_A,
    F_M+R_A+p_A <= D_dec,
    W >= Lambda+C_U+p_A-R_A.                       (SHADOW-3)

In particular the explicit test `R_A<=Lambda+C_U+p_A` also implies
Wilf, and is stronger than (A-OVERLAP).

For completeness, assign to the incidence between a cubic `y` and
`y-e_i` the weight `y_i`. Its total at a cubic is three. At a fixed
pair `z`, all possible A extensions have total weight
`sum_i(z_i+1)=a+2`. Distinct UF pair values correspond to distinct
pair monomials. This proves the first inequality; the second counts
three disjoint subsets of decomposable Apéry values. No Macaulay
theorem is used.

For `a>=1`, the first two inequalities imply

    R_A <= (a+2)(D_dec-F_M)/(a+5).

Using the first inequality also in the last line of (SHADOW-3) gives

    W >= Lambda+C_U-(a-1)R_A/(a+2)
      >= Lambda+C_U-(a-1)(D_dec-F_M)/(a+5).

This proves (SHADOW-PAY) and (SHADOW-OVERLAP). Replacing `C_U` by
`F_M` and dropping `Lambda>=0` proves (MF-SHADOW). The case `a=1`
has zero coefficient on `R_A`, and is included without a limiting
argument. QED.

### 5.2 Positive-part chain criteria

For Theorem D, put `s0=h-1` and `g(v)=v-m L1(v)`. Then

    g(v)=s0-s(v)+m K(v).

MF values have `g<0`. Hence every positive `g` is UF and has
`E(v)=0`, so `P(v)=g(v)` there. This proves equality of CHAIN-POOR
and WILF+ as inequalities, including equality of their left sides.
It does not assert that every UF value is poor.

Since `K<=1` everywhere,

    sum_v g(v)^+ <= h(h-1)/2 + m R.

The first term is the sum of `(s0-s)^+` over all residues; this is
where completeness and injectivity of Apéry are used. Now

    C2-h(h-1)/2 = rho(m+h-1)/2.

This proves (UF-SPARSE+).

There is also a sharper count version. Let

    H = #{v : s(v)<s0, K(v)<0},
    D = #{v critical : s(v)>s0}.

The lost baseline at the `H` values is at least `H(H+1)/2`, and
the negative residue contribution of the `D` long critical values is
at least `D(D+1)/2`, by distinct integer distances from `s0`.
Thus CHAIN-POOR and WILF+ hold whenever

    m(R-Lambda) <= rho(m+h-1)/2
                    +H(H+1)/2+D(D+1)/2.             (UF-COUNT+)

This is a sufficient count inequality, not an identity or an assumption
that every remaining semigroup satisfies it.

## 6. Strategic review

The overlap identities alone do not close Wilf. The substantive new
step is MF-UNIT: at depth four every multiply factorized value earns
at least one integer unit in the count identity, including the power
trades that can defeat a pointwise `E_U>=P` rule. The resulting
majority/support-weighted theorems close a uniform structural part of
the residual, with no fixed `alpha` endpoint.

The remaining difficulty is UF-dominant, with many central pure-A
cubics and little low-top credit. I did not find a proof of the
unrestricted comparison `R<=Lambda`; it is a stronger candidate,
tested separately below. No zero-failure census is being promoted to
that statement. The next route is to bound the UF A-cubic count by
top credit and the support-weighted MF credit using residue packing.

## 7. Stronger criteria on the P12 chain-counterexample families

**Proposition E (PROVED).** CHAIN-POOR and WILF+ hold on

    S_k=<5k+2,6k+3,...,7k+3>,                       k>=1,
    S_(k,r)=<5k+2,5k+3,...,5k+2+r,
                    6k+3,...,7k+3>,                r>=1, k>3r.

The Wilf assertion for these families was already proved in P12.
The new assertion here is the positive-part chain criterion, including
the range in which CHAIN fails. This is an application, not a claim
of a new Wilf family outside the previously covered regimes.

Use the exact Apéry description from P12: for `S_k` it is

    {0} union [6k+3,7k+3] union [12k+6,14k+6]
        union [19k+9,20k+7] union [20k+9,21k+8].

For the perturbation, replace the values `4m+j`, `1<=j<=3r`, by
`m+j` for `j<=r`, `2m+j` for `r<j<=2r`, and `3m+j` for
`2r<j<=3r`. Thus in both families

    m=5k+2, M=21k+8=4m+k, h=k+1, rho=4k+1.

The hypotheses and the modular interval proof of these descriptions
are in P12 Sections 3 and 7; the independent Dijkstra/literal-chain
checks in Section 9 recompute them without using those descriptions.
Only these descriptions, not the P12 REST or CHAIN formulas, are used
below.

All non-m generators in the first family are B units; in the second,
the `r` new generators are A units and the old interval remains B.
There are no C or E units. A critical BB pair can only be one of the
four uniquely represented two-term sums from a consecutive interval:
the two sums nearest each endpoint. Adding generators cannot create
another unique representation of a BB sum, so there are at most four.

For `k>=2`, a sum of three members of a consecutive interval of
`k+1` integers is uniquely represented only at distances zero and
one from either endpoint. Here the low two such sums are not Apéry
values, because their residues already have a smaller BB value. The
largest triple is `M+1` and is not Apéry. Thus only the triple at `M`
can be critical UF. To check the uniqueness assertion directly,
subtract the bottom of the interval and consider
`0<=i<=j<=l<=k`, with total `t`. If `2<=t<=k`, the partitions
`(0,0,t)` and `(0,1,t-1)` differ. For `k<t<=3k/2`, use
`(0,t-k,k)` and `(1,t-k-1,k)` when `t>=k+2`; at `t=k+1`,
use `(0,1,k)` and `(1,1,k-1)`. Reflection handles the top half.
This includes `k=2`; the central total three has `(0,1,2)` and
`(1,1,1)`.

For the perturbation, A--A pair offsets are at most `2r<h`, so
AAA and AAB cubes cannot have all pair divisors of co-level one.
An ABB cube has offset

    2k+3 <= tau <= 4k+2+r < m.

If `tau<=4k+2`, its residue already has a smaller BB value.
If `tau>=4k+3`, its value also has a BBB factorization, since
`[4k+3,4k+2+r]` is contained in the BBB offset range
`[3k+3,6k+3]`. Hence an ABB cube is never critical UF.
We have proved `R<=5` in both families for `k>=2`.

Finally

    rho(m+h-1)/(2m)=(4k+1)(6k+2)/(10k+4)>=5          (k>=2),

because the difference after clearing denominators is
`24k^2-36k-18>0` for `k>=2`. Therefore (UF-SPARSE+) applies,
even after dropping `Lambda`. For `k=1`, the first semigroup is
`<7,9,10>`, with `R=4`, `Lambda=9`; its four nonzero Apéry
chains also give (UF-SPARSE+) directly. The perturbed family has
`k>=4` and needs no extra small case. QED.

## 8. Failed claims and scope corrections

### 8.1 A pointwise lower-cover relay fails

**COUNTEREXAMPLE.** The proposed local inequality

    E_U(v)>=P(v) whenever v is MF

is false already for `S=<8,10,11,12>` at depth four. The Apéry set,
listed by residue, is

    [0,33,10,11,12,21,22,23].

Here `M=33`, `h=2`, `c=26`, and `W=26`. At `v=22`,

    Z(v)={2*11,10+12},
    depth=(1,2,1), E=22, E_U=11, P=12, L1=4, g=-10.

At `v=33`,

    Z(v)={3*11,10+11+12},
    depth=(1,3,1), E=22, E_U=0, P=15, L1=5, g=-7.

Thus the lower-cover relay can miss the entire positive landing mass
at an MF cubic. The full overlap credit does pay it, as MF-UNIT
predicts. These are failures of the *local proposed lemma*, not of
CHAIN-U, CHAIN-POOR, WILF+, or Wilf. The aggregate slacks are
`175,176,176` respectively. The data and all rows are saved in
`results/local_counter.json` and `results/case_checks.json`.
Both MF values have `K=-1`, so the uniform one-unit assertion in
MF-UNIT is sharp; replacing it by two units per MF value would fail.

`local_scan.py` found this after 33 retained depth-four cases in its
increasing-m interval-plus-truncation family. It is the smallest m
failure found there, not a claim of a global minimality theorem.

### 8.2 UF does not mean locally poor

**COUNTEREXAMPLE to a nearby implication.** In `<5,9,12>`,

    Ap by residue=[0,21,12,18,9], M=21, c=17, W=4.

All Apéry factorizations are unique. Nevertheless `v=9` has
`L1=2` and `v-mL1=-1`; it is rich. Consequently CHAIN-U has
slack `20=mW`, whereas CHAIN-POOR and WILF+ have slack `14`.
On UF Apéry sets, CHAIN-U is exactly Wilf, but the two
positive-part criteria need not have the same slack. The degree
inequality `|x|<v/m` for a UF factorization does not justify replacing
`L1` by `|x|`.

### 8.3 Equality is not restricted to ordinary semigroups

**PROVED correction.** For every `m>=2`,

    T_(m,4)=<m,4m+1,...,5m-1>

has `Ap={0} union [4m+1,5m-1]`, `M=5m-1`, `c=4m`,
`e=m`, `ell=4`, and `W=0`. Every nonzero Apéry value is primitive.
Thus `E=E_U=0`, `Lambda=0`, `R=0`, and

    g(4m+i)=i, sum g^+=C2.

It follows that all three criteria are equalities. These examples
are of depth four and include arbitrarily large m. They refute an
"equality only at the ordinary semigroup" assertion; no criterion
itself fails.

### 8.4 Two earlier-scope issues

The lead's `<53,85,...,95>` CHAIN counterexample from P12 has
`M=275` and `c=223`, hence depth **five**, not four. It is retained
as a context check in `case_checks.json`, and is excluded from every
P13 depth-four census. An initial independent test-driver assumption
that it had depth four was rejected by Dijkstra and corrected.

The P12 families prove failure at thresholds `M>=kappa n_1` for
fixed `kappa<21/5` (and, in particular, at `kappa=4`). They do not
establish failure at every arbitrarily large kappa: their limiting
ratio is `21/5`. This corrects the unrestricted threshold wording
in the lead's current P12 summary. It does not weaken REST-M3's
refutation or any of the P12 exact formulas.

### 8.5 Tested but still open

`R<=Lambda` (TOP-STRONG) would imply WILF+ by Theorem D. It had
no failures in the tests below. It is **OPEN**, not used as a theorem.
In particular, I have not replaced the geometric packing problem by
an unproved inequality about the count of critical values.

## 9. Computational checks (FINITE CHECK, not a global proof)

All mathematical computation ran on fejer, in `~/wilf/p13/`.
Searches and checking runs used `nice -n 10`; at most four of our
single-core jobs were active. No other process was altered. No
external theorem is used in the new proofs in Sections 2--5.
Python is `~/mathenv/bin/python` (3.12.3); C code was compiled with
`cc` 13.3.0 (Ubuntu 13.3.0-6ubuntu2~24.04.1), using `-O3`
and `-lm` for annealers.

### 9.1 Independent implementations

`core.h` extracts primitive generators from the sorted Apéry set,
computes forward and backward chain lengths independently, and checks
the join, link, CH' and total-deficit identities. The updated version
also asserts MF-UNIT, `K<=1`, the short arc for outside critical
values, COUNT-PAY and SHADOW-PAY. It makes no factorization-tile
choice. Values and slacks use signed 64-bit integers; all runs here
have `m<=527` in C, far within the numerical bounds of that type.

`check.py` is an independent Python implementation: heap Dijkstra
from the generators, primitive extraction, literal traversal of each
chain, and coin-change factorization counts capped at two. It checks
`E=0` iff UF, all local and global identities, the complete critical
classification, MF-UNIT, the short arc and both payments. It also
constructs the actual critical pair shadow and checks each of its
members, all three inequalities (SHADOW-3), and SHADOW-PAY. It does
not infer UF from the C output. Its central-A enumeration is performed
when `a<=64`, which includes every independent case used here.

### 9.2 Genus tree and structured families

| checker | domain | retained actual depth-four cases | failures |
|---|---|---:|---:|
| `tree.c`, updated structural assertions | every semigroup of genus at most 28 | 642,239 | 0 |
| `structured.c`, updated structural assertions | m=5..90, intervals and power-trade truncations below | 140,715 evaluations | 0 |
| `quick.py`, independent Python | named cases and every level-1 interval at m=6..45 | 2,573 evaluations | 0 |

The genus tree visits **5,311,726** semigroups in total and filters
by the actual conductor. Its standard effective-generator recursion
is adapted from the lead's `m3_tree2.c`; its numerical evaluator is
`core.h`, not the lead's evaluator. The initial run and the final
structural run give the same counts. The final run verifies the new
MF/count/shadow assertions, not just the three pre-existing criteria.
The minimum `Lambda-R` is zero. This genus range does not reach the
large-a P11 frontier and is not presented as doing so.

The structured run tests 257,636 inputs, with repetitions allowed.
First it tests every interval
`<m,m+i,...,m+j>`, `1<=i<j<m`, at m=5..90. It then tests the
cores with generators `2t,3t` for `m/2<t<5m/6`, augmented by the
first w generators `m+1+((t+j^2) mod (m-1))`, `1<=j<=w`,
`w=1..8`, and completed by `[3m+h,infinity)`. Here `h=1..m-1`,
in steps of one for m<30 and five otherwise. The actual conductor
is recomputed. Of the retained depth-four evaluations, 34,364
satisfy `3e<m`. Minimum CHAIN-U slack is 56, and minimum
CHAIN-POOR/WILF+ slack is 45. The two criteria are equal at each
retained point, as proved in Theorem D.

No failures of CHAIN-U, CHAIN-POOR or WILF+ occurred. The new
structural assertions also had zero failures. These are finite
checks, not proofs that a sufficient count hypothesis always holds.

### 9.3 Adversarial annealing

`search.c` changes one Kunz coordinate by one, checks all affected
Kunz inequalities, and imposes actual depth exactly four as a hard
constraint. A sparse run additionally imposes `3e<m`. Objectives
are the three criterion slacks or `Lambda-R`, normalized as recorded
in the code. All valid proposed states are evaluated, including
states rejected by the acceptance rule.

| run | objective | proposals | valid retained proposals | best unnormalized objective |
|---|---|---:|---:|---:|
| m=61 | CHAIN-U | 3,000,000 | 1,913,316 | 0 |
| m=87 | CHAIN-POOR | 3,000,000 | 1,260,678 | 5,672 |
| m=211, sparse | WILF+ | 900,000 | 276,171 | 327,593 |
| m=61 | Lambda-R | 8,000,000 | 3,297,707 | 22 |
| m=127, sparse | Lambda-R | 3,450,000 | 1,018,218 | 540 |
| m=527, sparse and shaped | CHAIN-U | 120,000 | 41,824 | 12,216,999 |

The m=211 and m=127 sparse runs retain fewer starts than requested
because some initialization attempts cannot find a seed in the hard
class. This is recorded as `NO SEED` in the logs; nominal starts
are not counted as evaluated states.

`gensearch.c` separately varies generators and a conductor
truncation at m=101 to minimize `Lambda-R`: 1,786,540 tests,
1,783,250 actual depth-four evaluations, minimum zero. It can fall
into the maximal-embedding-dimension equality family, so this zero
does not indicate a near-counterexample in the sparse frontier.

The shaped m=527 run starts with

    m=5k+2, k=105,
    A offsets {2,6,10,14,18,22} union {54,58,...,102},
    B offsets [k+1,2k+1].

It then allows Kunz mutations while keeping `a>=19`, `alpha>=6`,
`3e<m` and q=4 as hard constraints. Since m=527 and e<=175,
the condition `a<10*C(alpha+1,2)` is automatic. The best final
state has `a=19`, `alpha=6`, `e=173`, `M=2197`, `W=23414`,
`R_A=6`, `F_M=150`, `C_U=636`, `Lambda=21617`. Its complete
generators and Apéry set are in the log. The elementary count-only
MF-SHADOW hypothesis fails there, but SHADOW-OVERLAP holds with
ample top/support credit. This is a stress check in the *coarse*
P11 parameter strip. No negative-A-face or failure-of-LOW+ constraint
is imposed, and it is not claimed to evade all the GW-26 closures.

No criterion failure or TOP-STRONG counterexample was found. The
ordinary Kunz annealers often settle in interval-like or large-e
states. They are not an exhaustive search of the actual negative-A
frontier, and their positive margins are not evidence of a proved
uniform margin there.

### 9.4 Independent exact cases

`case_checks.py` makes **232** independent depth-four evaluations:

* four named cases, including the two local/scope examples above;
* `S_k`, k=1..40;
* `S_(k,r)`, r=1..8 and `3r+1<=k<max(31,3r+11)` (137 cases);
* five shaped interval-plus-low/high seeds, k=105,109,125,201,501;
* `T_(m,4)`, m=2..40;
* the seven final best witnesses from the C adversarial logs.

All generators, Apéry labels, criterion slacks and structural checks
agree. Six evaluations meet the coarse P11 residual parameters
`a>=19`, `alpha>=6`, `3e<m`; they have not been certified as
members of the remaining negative-A-face family. The m=2507 Python
case is independent of the C array bound. The `<53,85..95>` context
case is evaluated separately and correctly has depth five.

For example, at k=17 in P12,

    B_chain=63419 < need=63597,
    E_U=70137, CHAIN-U slack=69959,
    CHAIN-POOR/WILF+ slack=27002,
    R=5, Lambda=271.

`local_scan.py` preserves the failed pointwise candidate and its
rows. `local_verify.c` recomputes its Apéry set by a second C
Dijkstra and recomputes the two local failures directly. No
counterexample was found to any global criterion.

## 10. Exact remaining gap and next lemma

**Status: PARTIAL, PROVED.** There is no proof here of Wilf for
every semigroup with `3m<c<=4m`. There is no counterexample to
Wilf, CHAIN-U, CHAIN-POOR or WILF+. The new uniform classes are
(A-OVERLAP), its pair-shadow strengthening (SHADOW-3),
(SHADOW-OVERLAP), (MF-SHADOW), and the explicit positive-part
classes (UF-SPARSE+) and (UF-COUNT+). No finite computation is
being used to replace their hypotheses.

Using the earlier closures stipulated in P13, the numerical frontier
is still

    alpha>=6, 19<=a<10*C(alpha+1,2), 3e<m, m>=211,

with the original GW-26 negative-A-face/LOW+/LC conditions and
the failures of the P11 A--C payments. The new arguments remove
all members that satisfy any of the sufficient tests above. In
particular every hypothetical Wilf counterexample in this frontier
must satisfy all of

    R_A > Lambda+C_U+p_A,
    (a+5)(Lambda+C_U)+(a-1)F_M < (a-1)(m-1-d),
    2(a+2)F_M < (a-1)(m-1-d),
    m(R-Lambda) > rho(m+h-1)/2+H(H+1)/2+D(D+1)/2.

In the last line D is the **long-critical count of Section 5.2**,
not the decomposition count `D_dec`. In this remaining family
every MF value still has `K<=-1`; all positive local balance is
on UF values of the three types in Theorem A. The outside types
are already bounded by the short arc. Only the central pure-A
UF cubics can defeat the present count payment.

**Next precise lemma (OPEN; not an input).** For actual Apéry sets
in this reduced frontier, prove

    R_A <= Lambda+C_U+p_A.                          (UF-RELAY)

This would close the remaining depth-four case by (SHADOW-3).
One may instead spend the additional negative UF values not in
`p_A`, or the unused short-arc slack `rho-R_out`. A counterexample
to UF-RELAY would therefore be a failure of this proposed payment,
not a Wilf counterexample. The prospective mechanism is residue
packing of the critical UF A-cubics against the missing upper
extensions that create `Lambda`, with MF fibers charged by
MF-UNIT. I have not supplied that packing inequality.

**Strategic decision.** Stop local `E_U>=P` charging: Section 8.1
disproves it. Keep integer join credit and pair shadows, whose
proofs are independent of alpha. Do not extend the per-alpha
profile sweep or claim a numerical alpha interval from the present
counts. The next discriminating task is a direct attempt to prove
or refute UF-RELAY on negative-A, LOW+-violating instances, rather
than another unconstrained anneal with a large-e equality trap.

## 11. Reproduction and artifacts

All files are under `src/scratch/gw/p13/`; corresponding remote
files are under `~/wilf/p13/`. Source and output hashes are in
`results/SHA256SUMS`. Earlier reports were not changed; no commits
were made.

Representative commands, run on fejer:

```sh
cd ~/wilf/p13
cc -O3 tree.c -o tree_structural
nice -n 10 ./tree_structural 28 >tree28_structural.log 2>&1
cc -O3 structured.c -o structured_new
nice -n 10 ./structured_new 5 90 >structured_verified.log 2>&1
cc -O3 search.c -lm -o search_shaped
nice -n 10 ./search_shaped 527 4 30000 0 130527 1 1 >anneal_shaped527.log 2>&1
nice -n 10 ~/mathenv/bin/python case_checks.py >case_checks.log 2>&1
cc -O3 local_verify.c -o local_verify
nice -n 10 ./local_verify >local_verify.log
```

The other Kunz commands and seeds are preserved in
`results/COMMANDS.md`. Counts in annealing and structured logs are
evaluations/proposals, with repetitions; only the genus-tree count
is a count of all distinct semigroups in its stated domain.
