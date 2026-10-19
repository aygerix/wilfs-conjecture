# P7: WRAP-MAX and the all-height boundary inequality

Research date: 2026-10-19.  This report leaves the P6 reports unchanged.
All research computations are run on fejer in `~/wilf/p7/wrapmax/` (the parent
`~/wilf/p7/` already contains earlier project work).  No commits are made.

**Main result (COUNTEREXAMPLE, exactly verified). H1' is false.** There is an
explicit height-three WRAP-MAX tile with

```
m = 192038, d = 111233, rho = 64012,
S = 30848386779896 < Lambda_r = 30848489712264,
(S-Lambda_r)/m = -536.
```

It is the factorization tile of a numerical semigroup, and the failure is at
its conductor phase, with `c=704140`.  The construction gives an infinite
family.  Sections 7--10 give the construction, proof, two independent exact
checks, and the semigroup realization.  **MaxCL and Wilf remain positive on
this family** (the simple uniform bounds are in sections 9--10).
Thus this is a counterexample to the requested stronger lemma,
not to either of those conjectures.

## 1. Exact target and status labels

Let `D` be a finite down-set in `N^d`, with `|D|=m`, and let
`P_a in {1,...,m-1}`.  Put `v(x)=x.P`.  The residues `v(x) mod m` are required
to be distinct, hence complete.  Write `A` for the maximal cells and
`N=D\A`.  The **WRAP-MAX** hypothesis is `v<m` on `N`.
The degenerate case `m=1`, `D={0}`, has zero slack and is immediate; below
`m>=2` whenever a minimum active unit weight is used.

Let `V={y in A:v(y)>=m}` and `lambda(y)=v(y)-m`.  Every proper divisor of a
wrapped maximal cell is non-maximal, so `v(y)<2m`, and
`lambda(y)<P_b` for every `b` in its support.

The target H1' is `S(rho)>=Lambda_r(rho)` for every phase `0<=rho<m`, where
`S` is the MaxCL slack and `Lambda_r` is the residue mass of non-maximal
column tops.  Statements below are explicitly marked **PROVED**, **FINITE
CHECK**, **COUNTEREXAMPLE**, or **OPEN**.  In particular, a negative search
does not prove H1'.

## 2. The equivalent forms, independently re-derived (PROVED)

For a column `C`, let `t(C)` be its top.  Set

```
T(x) = sum_{b: x is a b-top} (x_b+1),
M' = m(m-1)/2,
r(x) = (v(x)+rho) mod m,
theta = m-rho,
W = {x: v(x) mod m >= theta}.
```

The column identities are

```
sum_D T = dm,
sum_D T(x)v(x) = (d+1)sum_D v(x),
T(y) = d+|y|  (y maximal).
```

The second identity follows in each column by summing the arithmetic
progression: `sum_{x in C}(v(t)-v(x)) = sum_{x in C}x_b P_b`.
Summing over the directions proves it.  Completeness and WRAP-MAX give
`sum_D v=M'+m|V|`, and `K=floor((v+rho)/m)=1_V+1_W`.  Thus

```
S-Lambda_r = (d+1)M' - sum_D T(x)r(x)
            = m[ T(W)-d|W| + sum_V(|y|-1) ].                 (W-ID)
```

Here `|W|=rho`.  The expression contains no phase carries, but `T(W)` does
depend on the chosen window.

The asserted `beta_N/tau` identity follows columnwise as well.  A column
whose top is non-maximal has only unwrapped cells, so its window cells form
a terminal interval.  Its contribution to `T(W)-d|W|` is zero if its top is
outside the window, and otherwise equals its number of cells outside the
window.  Summing gives `beta_N`.  For the columns topped by a maximal `y`,
the contribution is `|y|c_y-nb(y)`.  Since
`K(y)=1_V(y)+c_y`, adding the credit `sum_V(|y|-1)` gives exactly
`sum_A tau(y)`.  This proves the payment identity with no inequality.
For unwrapped maximal cells `tau>=0` by monotonicity of the window along
their columns.  For a wrapped maximal cell outside the window,
`tau=|y|-1-nb>=-1`, with equality exactly when all its column-below cells
are in the window.  A wrapped maximal cell in the window has
`tau=2|y|-1-nb>=|y|-1>=0`.  Thus the exceptional set is precisely `F`.

For an up-set `U`, put

```
partial(U) = sum_b #{x outside U: the b-column of x meets U}.
```

Columnwise `partial(U)=T(U)-d|U|`.  Let

```
L_theta = {x:v(x)<theta},
U_theta = D\L_theta = {x in D\V:v(x)>=theta} union V,
V_lo = {y in V:lambda(y)<theta},
V_hi = V\V_lo.
```

Since `W=U_theta\V_lo`, substitution in W-ID gives

```
(S-Lambda_r)/m
 = partial(U_theta)-|V_lo|+sum_{V_hi}(|y|-1)
 = partial(U_theta)+sum_{V_hi}|y|-|V|.                       (SH-ID)
```

The equality between the window and shadow combinatorial expressions also
holds for an injectively labeled partial down-set.  Identification with
`(S-Lambda_r)/m`, and the equality `|W|=rho`, use completeness.

If `Ex(U)` counts the *immediate* edges from `D\U` to `U`, then
`partial(U)>=Ex(U)`.  Counting edges entering an up-set gives

```
Ex(U_theta)=sum_{x in D\V,v(x)>=theta}(supp(x)-up(x))
             +sum_{y in V}supp(y).
```

Consequently the degree/exit inequality in the task is exactly the stronger
inequality obtained by replacing `partial` by `Ex` in SH-ID.  It is not
silently identified with the equivalent shadow form.

There is also a direct all-height lift verification.  Put `U_j={v>=jm}` and
`U'_j={v+rho>=jm}`.  The column carry identity is

```
(S-Lambda_r)/m = sum_{j>=1}(partial(U'_j)-|U_j|).             (LEVEL-ID)
```

Under WRAP-MAX, `U_1=V`, `U_j=empty` for `j>=2`,
`U'_1=U_theta`, and `U'_2=V_hi`.  A subset of maximal cells has
`partial(E)=sum_{y in E}|y|`, since distinct maximal cells cannot share a
column.  This proves SH-ID once more.

## 3. Injectivity alone is insufficient (COUNTEREXAMPLE)

Take `m=7`, `P=(4,5)`, and the quadratic simplex

```
D={ (0,0),(1,0),(0,1),(2,0),(1,1),(0,2) }.
v(D)={0,4,5,8,9,10}; labels={0,4,5,1,2,3}.
```

This is an injectively labeled WRAP-MAX down-set, but it is not complete.
At `theta=4`, `L_theta={0}`, `V_lo` is the set of all three pairs,
`V_hi=empty`, and `partial(U_theta)=Ex(U_theta)=2`.  The shadow and degree
slacks are both `-1`.  Thus the proposed induction on arbitrary partial
down-sets cannot use H1' without an additional missing-label allowance.

Adding a spike of label `6` gives a complete tile in three dimensions and
increases the boundary by one; its H1' slack at this phase is zero.

**FINITE CHECK.** `partial.py --mmax 9 --dmax 8` enumerates every active
dimension, every increasing distinct unit-residue vector, and every
injective WRAP-MAX down-set for `2<=m<=9` (coordinate permutations removed).
There are 9,167 down-sets, 1,978 complete and 7,189 partial.  Thirteen partial
ones fail H1'; no complete one does.  The displayed counterexample has the
smallest `m`, and then the smallest number of cells, in this complete search.
The independent evaluator checks down-closure, injectivity and all the
identities of section 2.  Logs: `results/partial_all.log` and
`results/partial_all.err` on fejer.

## 4. Small-threshold theorem (PROVED)

**Theorem BOUNDARY.** Every WRAP-MAX tile satisfies H1', and in fact its
stronger exit form, whenever `1<=theta<=a`, where `a` is the smallest active
unit weight.  In particular this covers `theta<=min_b P_b`.

Inactive directions may be discarded: they contribute zero to the boundary,
and their columns are singletons.  Let `k` be the number of active directions.
For these thresholds `L_theta={0}`, so
`partial(U_theta)=Ex(U_theta)=k` and `|V_lo|=theta-1`.
The last equality uses completeness: every positive label below `theta`
has to be wrapped.

If `a=1`, the only threshold is `theta=1`, and the assertion is immediate.
Suppose `a>=2`.  Label `1` must be represented by a wrapped cell of degree
at least two.  Hence `m+1>=2a`.  The integer interval

```
J=[a,a+theta-2]
```

therefore lies in `[0,m)` and has `theta-1` members.  For `j in J`, consider
its unique representative.  If this representative is unwrapped, its value
is `j<2a`, so it is a unit.  Otherwise it is a wrapped maximal cell with
`lambda=j>=a>=theta`; it belongs to `V_hi`.  Distinct members of `J` give
distinct cells.  Since every wrapped cell has degree at least two,

```
theta-1 <= k + #{y in V_hi:lambda(y) in J}
         <= k + sum_{V_hi}(|y|-1).
```

This is the required exit inequality.  The proof uses both completeness and
WRAP-MAX; the partial example in section 3 fails precisely because label `6`
in the atomic interval `J={4,5,6}` is absent.

## 5. Spike completion as an exact reduction (PROVED)

Let `C` be any injectively labeled WRAP-MAX down-set of size `n<=m` in `N^k`.
Append one new direction and its unit cell for each missing nonzero label.
The resulting down-set is a complete WRAP-MAX tile.  For `theta>=1`, each
new spike of label at least `theta` increases the shadow by exactly one;
a spike of smaller label does not change it.  No wrapped cell is added.
Thus H1' for all complete tiles is equivalent to the following statement
for all partial cores:

```
partial_C(U_theta)-|V_lo|+sum_{V_hi}(|y|-1)
   + #{missing labels in [theta,m)} >= 0.                   (MISSING)
```

This is a reformulation, not a proved universal inequality.  It explains
the payment in section 3 and supplies a broader adversarial tile generator.
The generator `search.c` tests MISSING on cores directly and records the
missing labels needed to reconstruct the complete tile.

## 6. Intermediate frontier and the successful pivot

**PROVED:** the exact reductions, failure of injectivity-only H1', and H1'
in the whole boundary range `theta<=min P`.

At this stage H1' beyond the boundary range was unresolved.  Random tiles and
fixed-residue LP relaxations gave no negative examples; their ranges are
recorded in section 11.  Extending the same searches was discontinued in favor
of an explicit near-half unit construction.  Its non-maximal pairs lie in a
short upper window, while an incomplete cubic face can occupy more than that
window plus the pair count.  This produces the counterexample below.

## 7. A Sidon-set construction (PROVED)

Here a **Sidon set** means a positive integer set whose unordered pair sums,
including loops, are all distinct.  Let

```
A={a_0,...,a_{k-1}} subset [1,L],  max A=L,
Q=k(k+1)/2,
T=(A+A+A)\A,  t=|T|.
```

For each `s in T`, choose one nondecreasing triple of indices whose offsets
sum to `s`.  The lexicographically least triple is a definite choice.  Fix
an arbitrary integer `q>=3L+1`, and set

```
m=2q,  P_i=q-a_i,
rho=2L,  theta=m-2L.
```

Let `C subset N^k` consist of the origin, all `k` units, all `Q` pairs, and
the chosen `t` cubics.  Its nontrivial labels are

```
units:  q-a_i,
pairs:  m-(a_i+a_j),
cubics: q-s,  s in T.
```

All pairs are unwrapped, with values in `[m-2L,m-2]`.  All cubics are wrapped
once, since `v(y)=3q-s` lies strictly between `m` and `2m`.  Unit labels and
cubic labels are positive and less than `q`; pair labels are greater than
`q`.  Sidonicity makes the pair labels distinct, and the chosen cubic labels
are distinct.  A unit/cubic collision would be `s=a_i`, excluded by the
definition of `T`.  Thus `C` is injective modulo `m`.  It is a down-set,
because every pair has been included.  Its only possibly wrapped cells are
the maximal cubics.

Complete it by spikes as in section 5, one for each missing nonzero label.
Call the resulting tile `D`.  Then

```
|C|=1+k+Q+t,
s_spike=m-(1+k+Q+t),
d=k+s_spike=m-1-Q-t.
```

This is a complete WRAP-MAX tile of height three (provided `T` is nonempty).
At the specified threshold all units and cubics have labels below `theta`,
and every pair is in the upper label window.  Therefore exactly
`rho-Q=2L-Q` spikes are in that window.  In particular `V_hi=empty`.

For clarity, the boundary calculation can be made without enumerating
columns.  For any positive linear weight and up-set `{v>=theta}`,

```
partial({v>=theta})
 = sum_{x in D} sum_b x_b [v(x)-P_b < theta <= v(x)].          (FIRST-ID)
```

Indeed each column meeting the up-set has a unique first cell `x` in it,
and exactly `x_b` cells below it, of coordinates `0,...,x_b-1`.

Every pair contributes `2` to FIRST-ID, because its unit parents are below
the threshold.  Every cubic contributes `0`, because its pair parents are
at least `theta`.  Every high spike contributes `1`; everything else
contributes `0`.  Consequently

```
partial(U_theta)=2Q+(2L-Q)=2L+Q,
V_lo=V, |V|=t,
(S-Lambda_r)/m = 2L+Q-t.                                   (SIDON-ID)
```

**Theorem SIDON-OBSTRUCTION.** If a positive Sidon set satisfies
`|3A\A|>2 max A + k(k+1)/2`, the construction above is a counterexample to
H1', for every integer `q>=3 max A+1`.  This is a proved construction; no
packing conjecture is assumed.

## 8. An explicit set and the counterexample (EXACT FINITE CERTIFICATE)

Take the prime `p=127` and define

```
a_i = 1 + 254 i + (i^2 mod 127),  0<=i<=126.
```

This formula is a compact full specification of the set.  It is strictly
increasing, and `L=a_126=32006`.

Here is a direct proof of Sidonicity.  Write `r_i=i^2 mod p`, in `[0,p-1]`.
An equality of two pair sums implies

```
2p(i+j-r-s)=r_r+r_s-r_i-r_j.
```

The right side has absolute value less than `2p`, so `i+j=r+s` and
`r_i+r_j=r_r+r_s`.  Reduction modulo `p` gives equal sums and equal sums of
squares, hence equal products, because `p` is odd.  The pairs are the roots
of the same quadratic over `F_p`.  Thus their unordered index multisets are
equal, since all indices lie in `[0,p)`.  This includes loop pairs.

Two independent integer enumerations give

```
k=127, L=32006, Q=8128,
|3A\A|=72676,
2L+Q=72140,
|3A\A|-(2L+Q)=536.
```

This finite count is part of the counterexample certificate.  It involves
only the nondecreasing triples of 127 indices.  `sidon_counter.py` enumerates
them in Python and saves one witness triple per sum; `sidon_count.c` repeats
the count independently with integer marker arrays.  Their results agree.
The saved list is checked independently for distinct residues and
down-closure by `verify_counter.py`; therefore the negative example does not
depend on trusting that all possible triple sums were found.

For the smallest `q` in this construction, `q=96019`, the full data are:

| Quantity | Exact value |
|---|---:|
| `m` | 192038 |
| core dimension `k` | 127 |
| core cells | 80932 |
| new spikes | 111106 |
| dimension `d` | 111233 |
| threshold `theta` | 128026 |
| phase `rho` | 64012 |
| non-maximal cells | 8254 |
| maximal cells | 183784 |
| wrapped maximal cells | 72676 |
| maximal unwrapped pairs | 2 |
| covered, non-maximal pairs | 8126 |
| `max_N v` | 192036 |
| `min_V v` | 192039 |
| `max_V v` | 288054 |
| shadow boundary | 72140 |
| immediate exit count | 72013 |
| `S` | 30848386779896 |
| `Lambda_r` | 30848489712264 |
| `S-Lambda_r` | -102932368 |
| `(S-Lambda_r)/m` | -536 |

In the task's original payment variables the same counterexample is

```
beta_N = 12344,
tau=-1 on 68803 squarefree cubics,
tau=0 on 59060 maximal cells,
tau=1 on 55919 maximal cells,
tau=2 on 2 maximal pairs.
```

Hence `tau_+=55923`, and

```
beta_N+tau_+-|F|=12344+55923-68803=-536.
```

Thus all three equivalent H1' forms fail.  The stronger immediate-exit form
has slack `-663`.  No wraps occur on non-maximal cells.  This is not an
injectivity-only example; every one of the `192038` residues occurs exactly
once.  Notice also `theta=2 min_i P_i` in the core.  This is **not** twice
the smallest canonical unit weight of the complete tile: the added spikes
include weight `2`.  The boundary theorem uses all active directions.

## 9. A numerical-semigroup realization at the conductor phase (PROVED)

The counterexample is realizable as a factorization tile with respect to
the **minimal** generators of a numerical semigroup.  In fact this holds
for every member of the family in section 7 with `q>=3L+1`.

Let `J` be the set of missing labels of the core `C`, and put

```
c=3m+theta=4m-2L,
n_i=m+P_i=3q-a_i  (0<=i<k),
g_j = 4m+j  if j<theta,
      3m+j  if j>=theta,  (j in J),
S_semigroup=<m, n_i (i<k), g_j (j in J)>.
```

The spike values all lie in `[c,c+m)`.  Use the factorizations of `C` for
its labels and the unit factorization `g_j` for each missing label.  We show
that these are precisely representatives of the Apéry elements.

The candidate values are

```
0,
units:  3q-a_i = m+(q-a_i),
pairs:  6q-s = 2m+(m-s), s in 2A,
cubics: 9q-s = 4m+(q-s), s in T,
spikes: g_j.
```

All are at most `c+m-1=10q-2L-1`.  All sums of four core generators are
larger, since

```
4 min_i n_i >=12q-4L > 10q-2L-1.
```

Every sum involving a spike and another positive generator is larger as
well: spikes are at least `c=8q-2L`, core generators are at least `3q-L`,
and their sum is at least `11q-3L >10q-2L-1`.  Adding `m` to a spike also
exceeds this upper bound, because all spikes are at least `c`.

It remains to compare factorizations using at most three core generators
(and any copies of `m`).  Their residues are exactly those used in `C`,
except that a triple with offset sum in `A` has the same residue as a unit
and is `3m` larger than that unit.  The other collisions are precisely equal
triple sums; their generator weights are equal.  Pair sums are unique and
their labels lie in a separate band.  Thus each candidate is the least
semigroup element in its residue.  This proves the asserted Apéry table.

All displayed generators are minimal.  Each core generator lies strictly
between `m` and `2m`, so it cannot be decomposed.  For a spike, a decomposition
using only core generators and `m` would give a missing label using at most
three core generators (impossible), or use at least four (too large).
A decomposition involving another spike is too large by the bounds above.

The existence of an element in every residue implies that this is a numerical
semigroup.  The label `theta-1` is missing from `C`: it is below the pair
band and above every unit and cubic label.  Its spike is exactly
`c+m-1`, so the conductor is **exactly** `c`, rather than just at most `c`.
Its factorization tile is `D` and has WRAP-MAX.  Finally

```
c mod m = theta,
(-c) mod m = rho=2L.
```

This is precisely the failing phase for H1'.  Hence restricting H1' to
factorization tiles or to the phase needed by the Wilf implication does
**not** rescue it.

For the explicit `q=96019` member:

```
m=192038, c=704140, e=111234,
n_1=256051, 2n_1=c-m=512102,
genus=695627, ell=8513,
e*ell-c=946230902 >0.
```

In the whole family, exactly four multiples of `m`, three translates of
each core unit, and one copy of each pair lie below `c`.  All cubics and
spikes are at least `c`.  Consequently

```
ell=4+3k+Q,
e=m-Q-t,
W=e*ell-c=(m-Q-t)(4+3k+Q)-(4m-2L).
```

For the explicit offset set this is positive at the smallest allowed `m`,
and strictly increases with `m`.  Thus Wilf holds on the entire displayed
counterexample family.  Moreover `3m<c<4m` and `2n_1=c-m`; this is already
inside the upper-unit primary regime proved earlier.  The new failure is
only the stronger pure-counting/Tile-CL statement.

## 10. Independent verifications (EXACT COMPUTATION)

`verify_counter.py` reads the saved triples and builds every core cell and
every spike as sparse monomials.  It checks down-closure and the full set of
labels.  From actual upper-cover incidences it computes

```
load(x)=sum_{a:x+e_a in D}(x_a+1),
T(x)=d+|x|-load(x),
A={x:load(x)=0}.
```

It then evaluates `S` and `Lambda_r` directly from their definitions.  It
independently evaluates FIRST-ID, the window form, the immediate exits,
`beta_N`, and every maximal cell's `tau`.  The negative results in section 8
agree exactly.  This check does not construct `d*m` singleton columns;
their contribution is included exactly by the formula for `T`.

`verify_semigroup.py` builds the **whole** proposed Apéry table and checks,
for every core generator `g` and all `m` residues, the shortest-path
inequalities `w_i+g>=w_{i+g mod m}`: 24,388,826 exact inequalities.  For spike
generators the inequalities at zero are checked, while all nonzero ones
follow from the separately checked bound
`min_spike+min_nonzero_apery>max_apery`; the implied 21,336,574,028 inequalities
are **not individually enumerated**.  It also checks 14,110,462 individual
spike/core-generator subtraction inequalities for minimality.  Thus the
semigroup realization is checked independently of the short analytic proof.

There is a uniform elementary proof of MaxCL on the **whole** counterexample
family, at **every** phase.  Its number of non-maximal cells is `n=8254` and
its maximal excess mass is

```
R=sum_{y in A}(|y|-1)=2t+2=145354.
```

Residue distinctness and `0<=r<m` imply

```
S=(d+1)sum_N r-sum_A(|y|-1)r
 >=(d+1)n(n-1)/2-(m-1)R
  =(m-Q-t)*34060131-(m-1)*145354.
```

At the smallest `m=192038`, this is `3760731265556>0`.  Its coefficient of
`m` is `34060131-145354=33914777>0`, so it remains positive for every larger
member of the family.  This verifies that no MaxCL failure is being hidden
by the scope of the counterexample.

All arithmetic is integer arithmetic (NumPy int64 only for quantities
bounded far below its limit).  The C count and the sparse Python evaluations
are independent implementations.  No external theorem is used to obtain the
counterexample.

## 11. Other computation and preserved failures

All jobs ran with `nice -n 10`, with BLAS/OpenMP limited to one thread.  At
most two research computations ran concurrently.  Runtime commands and the
final file checksums are in `RUN.md` and `results/SHA256SUMS`.

| Script / run | Exact domain or sampling policy | Result |
|---|---|---|
| `partial.py --mmax 9 --dmax 8` | All active residue vectors and all injective WRAP-MAX down-sets, coordinate permutations removed | 9167 structures; 13 partial failures; 0 complete failures |
| `search.c`, seed 71019 | 1000000 greedy WRAP-MAX cores, `6<=m<=150`, `2<=k<=10`, completed by every missing-label spike | 78035487 phases; 0 H1' failures; heights up to 64 |
| `optimize.py`, seed 71020 | 200 residue vectors, `10<=m<=100`, `k<=8`; fractional down-closure/residue LP, sampled phases | 1145 LPs; none negative (numerical discovery data, not an exact certificate) |
| `optimize.py`, seed 71022 | 1000 residue vectors, `10<=m<=180`, `k<=10`; same LP, up to 10 phases per pool | 998 pools within the 12000-cell cap, 9696 LPs; none negative |
| `sidon_counter.py` | Prime-index formula through 127, stopping at the first negative value | First failure in this tested formula at `p=127` |
| `sidon_count.c 127` | All unordered pairs and nondecreasing triples | `Q=8128`, `t=72676`, slack `-536` |
| `verify_counter.py` | Every cell of the saved completed tile | All hypotheses and identities pass; H1' fails |
| `verify_semigroup.py` | Full Apéry table and the checks of section 10 | All pass; Wilf positive |
| `once_check.py`, seed 2026101977 | 500 random semigroup attempts; grlex and residue-weight tiles; `8<=m<=100`; retain `v<2m` on `N` | 343 retained tiles, 12699 phases, heights up to 19; both next-level identities pass; E47 and the named `m=17` fixture add 31 phases |

The numerical LP probes do not exclude all fixed-residue profiles in their
parameter boxes.  One preliminary larger LP run, seed 71021, terminated on
an invalid sampling range after 640 completed trials; it is preserved as
`results/lp_large.*` and is not used as a completed experiment.  The corrected
sampler is the seed-71022 run.  The prime scan initially used the also-valid
larger modulus `m=12L+2` through 103; the final witness and verifications use
`m=6L+2` throughout.

The mathematical false claims are preserved explicitly:

1. **Injectivity-only H1': false.** Smallest counterexample in the complete
   `m<=9` search is section 3.
2. **H1' on complete WRAP-MAX tiles: false.** Section 8 gives a full exact
   witness and section 7 gives the infinite family.
3. **H1' only on factorization tiles, only at the conductor phase: false.**
   Section 9 realizes the same witness with the required minimal generators
   and phase.
4. **Applying the boundary theorem using only the core minimum: invalid.**
   The section-8 example has `theta=2 min P_core`, but the smallest spike
   weight is `2`.  It does not refute a proposed extension with
   `theta<=2 min P` for the full tile; that extension has not been proved or
   disproved here.

No assertion is made that the section-8 witness is globally smallest.

A separate attempted induction was also discarded: replacing a proper
non-maximal composite by a new unit need not weakly decrease
`(S-Lambda_r)/m`.  The smallest possible height-three chain is already a
counterexample.  For `m=4`, `P=(1)`, `D={0,1,2,3}` and `rho=3`, the normalized
slack is `1` (`S=4,Lambda_r=0`).  Replacing two copies of this direction by
a unit of canonical weight `2` gives the square
`{(0,0),(1,0),(0,1),(1,1)}`, `P=(1,2)`, still no-wrap and complete.
At the same phase its normalized slack is `2` (`S=10,Lambda_r=2`).  This
refutes the unconditional monotone-compression claim; it does not refute a
descent restricted to hypothetical negative-slack tiles.  `small_checks.py`
verifies this calculation and the partial/spike-completion example exactly.

## 12. The next wrap level and final status

The proposed Wilf corollary in the task was conditional on H1'.  That route
is unavailable: even its conductor-phase premise is false.  This does not
disprove Wilf for semigroups admitting a WRAP-MAX factorization tile.

For reference, there is a simple exact identity at the next level, requiring
no conjecture.  Suppose `v<2m` on non-maximal cells, so `v<3m` on all cells.
Put

```
k(x)=floor(v(x)/m),
N_1={x in N:v(x)>=m},
W={x:v(x) mod m>=theta}, rho=m-theta.
```

Then `k=1` on `N_1`, and substitution in the same Gauss identity as W-ID gives

```
S = Lambda_r + m[
    T(W)-d*rho
    +sum_{y in A}(|y|-1)k(y)
    +sum_{x in N_1}(T(x)-d-1) ].                            (ONCE-ID)
```

Equivalently, using `U_b={v>=b}`,

```
S = Lambda_r + m[
    partial(U_theta)+partial(U_{m+theta})
    +sum_{y in A,v(y)>=2m+theta}|y|
    -#{x:v(x)>=m}-#{x:v(x)>=2m} ].                         (ONCE-LEVEL)
```

The term with threshold `2m+theta` consists only of maximal cells, which
explains its sum of degrees.  These are exact replacements; asserting the
bracket nonnegative would already include the false H1'.  The inequality
needed for MaxCL is that the bracket is at least `-Lambda_r/m`.
`once_check.py` checks both identities independently on 12730 phases,
including E47 (where the pure-counting bracket is `-1` at one phase).

**Final status.** P7's proof-or-refutation deliverable is settled negatively:
H1' is refuted at height three, on actual factorization tiles and at the
conductor phase.  The small-threshold exit inequality is proved, and an
injectivity-only obstruction is also recorded.  NO-WRAP, Flat-MaxCL, the
previous height-three MaxCL results, and all recorded Wilf results are
unchanged.  The broader remaining question is the residue-mass-corrected
boundary inequality `Lambda_r/m+partial(U_theta)+sum_{V_hi}|y|>=|V|` on
WRAP-MAX tiles.  The counterexample identifies a concrete necessary payment:
an incomplete cubic face can have `t>rho+Q`, and its excess must draw on
non-maximal column residue mass.  Pure boundary counting cannot pay it.
