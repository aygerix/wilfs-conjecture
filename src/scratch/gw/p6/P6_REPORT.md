# P6: height-three MaxCL

2026-10-19. **The full height-three theorem remains open.** This
report proves three partial results, with their scopes kept separate:

1. **H3-D5, computer-assisted:** MaxCL holds at every phase for every
   residue-complete down-set of height at most three and at most five
   active directions. Consequently Wilf holds for height-three Apéry
   sets with embedding dimension at most six, at every depth.
2. **H3-CORE2, paper plus a small finite certificate:** MaxCL holds at
   every phase when at most two unit directions are non-maximal.
   The number of isolated unit spikes, the ambient dimension, and
   the modulus are unbounded.
3. **PAIR-ZERO and CENTERED-PAIR, paper:** two explicit carry regimes
   imply MaxCL at a specified phase, in every dimension. The first
   permits negative cubic carries and pays them exactly by a top
   interval; the second uses the shifted origin lift. An additional
   unit-load criterion proves the phase rho_0=0 in a structural class.

No counterexample to height-three MaxCL was found. All computation
was on fejer, in `~/wilf/p6`, nice 10, with at most four owned
single-core jobs. The laptop was used only for reading, editing,
and copying files. No commits. P4/P5h was not worked on.

## 1. Exact conventions and accepted dependencies

A tile is a finite down-set D in N^d, of cardinality m, such that
`phi(x)=sum_a x_a p_a mod m` is bijective on D. Initially all
directions are active: every e_a belongs to D. Removing inactive
directions preserves maximality, all cell heights, and the first
MaxCL left side, while decreasing its right-side coefficient.
Thus a proof in the active dimension suffices for an ambient tile
with additional inactive directions. The one-cell case is trivial.

Assume height(D)<=3. Let A be its maximal cells, N=D\A, and write

```
Q = set of all pairs,       q=|Q|,
A2 = A intersect Q,         N2 = N intersect Q, p=|N2|,
T = set of all cubics,      t=|T|,
k = number of non-maximal units,
number of isolated unit spikes = d-k,
m=1+d+q+t,                 |N|=1+k+p.
```

Here p without a subscript counts non-maximal pairs; the vector
of residue generators is always denoted p_a. For a phase sigma,

```
r(x)=(phi(x)-sigma) mod m in {0,...,m-1},
rho_0=r(0), rho_a=r(e_a), nu=m-rho_0,
S=(d+1)sum_N r - sum_A (|y|-1)r(y).
```

The desired assertion at that phase is S>=0. Equivalently, with
`C_m=m(m-1)/2`,

```
sum_A (d+|y|)r(y) <= (d+1)C_m.                  (MAX)
```

The project dependencies used are Flat-MaxCL, the lead's unit
identity under PROOFS "Column-top lemma and the carry form of
MaxCL", and the Lean-checked implications MaxCL => Tile-TOP'' =>
Wilf. The new computer-assisted theorem itself is NOT Lean-checked.
The formalization statements in section 9 distinguish that fact.

Define ordinary INTEGER lifts and carries by

```
ell(x)=(1-|x|)rho_0+sum_a x_a rho_a,
K(x)=floor(ell(x)/m), so ell(x)=r(x)+mK(x).
```

For z in N2 let
`psi(z)=sum_{a:z+e_a in T}(z_a+1)`, and let
`deg(a)=sum_{z in Q}z_a`. The elementary bounds are
`deg(a)<=d+1`, `psi(z)<=d+2`, and

```
2 sum_T y_a = sum_{z in N2} z_a psi(z).
```

The accepted exact identity is

```
S=Lplus+m(rho_0+Br0),
Lplus=sum_{e_a in N}(d+1-deg(a))rho_a
                 +sum_{z in N2}(d+2-psi(z))r(z) >=0,
Br0=sum_{A2}K + 2sum_T K - sum_{N2}(psi-1)K.       (UNIT)
```

All counts and residues here are those of the same tile and phase.
No integer Sidon-difference assertion from P5 is being applied
modulo m. In particular the possible 3-torsion exception to DIFF2
does not enter any proof in this report.

## 2. Two dimension-free carry-payment theorems

### 2.1. PAIR-ZERO

**Theorem PAIR-ZERO (proved on paper).** Suppose

```
K(z)=0 for every z in N2,
K(z)>=0 for every z in A2.                       (PZ-hyp)
```

Then at the specified phase

```
S >= Lplus + m*(rho_0 mod 2) >=0.                (PAIR-ZERO)
```

The hypothesis does not require cubic carries to vanish.

Proof. Every pair divisor of a cubic y is in N2. Direct expansion
gives the integer identity

```
2ell(y)+rho_0=sum_{a:y_a>0} y_a ell(y-e_a).        (CUBIC-LIFT)
```

Under PZ-hyp each term on the right is a nonnegative principal
pair residue. Consequently `ell(y)>=-floor(rho_0/2)>-m`.
If a cubic has negative carry, therefore K(y)=-1 and

```
m-floor(rho_0/2) <= r(y) <= m-1.
```

The negative-carry cubics have distinct residues. This interval
contains floor(rho_0/2) integers, so their number B is at most
floor(rho_0/2). In UNIT the N2 term is zero, the A2 term is
nonnegative, and the other cubic terms are nonnegative. Hence
`Br0>=-2B>=-2floor(rho_0/2)`. Substitution in UNIT proves
the displayed lower bound, including its parity term. QED.

This charges the cost TWO of each negative cubic by the density
of a half-size top interval; it does not charge two units for
each arbitrary residue in a rho_0-sized interval. It also does
not assert that PZ-hyp holds on every height-three tile.

The bound is sharp already for the column tile m=4, p_1=3,
sigma=2. Its residues at 0,e,2e,3e are 2,1,0,3. The pair has
K=0, the cubic K=-1, Lplus=0, and S=0.

### 2.2. CENTERED-PAIR

Put `ell_1(x)=ell(x)+(|x|-1)m`, corresponding to the origin
lift `rho_0-m=-nu`, and put `K1=K+|x|-1`. For every nonzero
cell,

```
ell_1(x)=sum_a x_a rho_a+(|x|-1)nu >=0.
```

Thus all nonzero K1 are nonnegative. Since sum_N2 psi=3t,

```
Br1=sum_{A2}K1+2sum_T K1-sum_{N2}(psi-1)K1
   =Br0+q+t=Br0+m-1-d,
S=Lplus+m(d+1-nu)+mBr1.                         (CENTER-ID)
```

**Theorem CENTERED-PAIR (proved on paper).** If

```
nu<=d+1, and K1(z)=0 for every z in N2,
```

then

```
S >= Lplus+m(d+1-nu) >=0.                       (CENTERED-PAIR)
```

Proof. All A2 and T carries in CENTER-ID are nonnegative and
its N2 term vanishes, so Br1>=0. QED.

Equivalently the pair condition is K(z)=-1 on N2. Maximal-pair
and cubic carries in the centered lift may be positive; they
need not vanish. This is stronger than requiring a centered
lift with no nonzero carries at all. In particular it covers
the lead's negative-bracket example <14,16,17,19> at sigma=2.
There d=3, nu=2, Lplus=36, Br0=-10 and Br1=0, giving
the exact slack `S=36+14*(4-2)=64`.

Neither theorem drops Lplus without additional hypotheses.
The unrestricted claim Br0>=-rho_0 is still false on E47.

## 3. An explicit unit-load criterion at rho_0=0

Let `adeg(a)=sum_{z in A2}z_a`, and `tc(a)=sum_T y_a`.

**Theorem UNIT-LOAD-0 (proved on paper).** If rho_0=0 and

```
3adeg(a)+2tc(a) <=3(d+1) for every a,             (UL3)
```

then S>=0. In fact

```
3S >= sum_{e_a in N}[3(d+1)-3adeg(a)-2tc(a)]rho_a
                   +sum_{N2}[3(d+1)-2psi(z)]r(z) >=0.
```

Proof. At rho_0=0 principal residues are subadditive on every
monomial split. A maximal pair z=e_a+e_b satisfies
`r(z)<=rho_a+rho_b`, counting twice for a=b. For each cubic y,

```
2r(y) <= (2/3) sum_a y_a [rho_a+r(y-e_a)].
```

The resulting unit load is `adeg(a)+(2/3)tc(a)`, and the
non-maximal pair load is `(2/3)psi(z)`. All loaded units are
non-maximal. The former load is <=d+1 by UL3; the latter
is <=d+1 since psi<=d+2 and d>=1. Subtract these upper
loads from the MaxCL right side. This gives the claimed
lower bound. QED.

**Corollary PSI3 (proved).** At rho_0=0, MaxCL holds whenever
psi(z)<=3 for every z in N2. Indeed
`2tc(a)=sum_N2 z_a psi(z)<=3sum_N2 z_a`, so UL3 follows
from `deg(a)<=d+1`.

This is an explicit sufficient class for the natural split;
it does not resurrect the false general Load Lemma. If the
semigroup conductor is divisible by m, rho_0=0 is the phase
needed by the Lean Wilf implication.

**E47, including its essential linear slack.** For the tile
of <14,22,23,57,61,62,63>, at sigma=0 the core unit residues
are 8,9, the three core pair residues are 2,3,4, and the four
cubic residues are 10,11,12,13. There are four isolated unit
spikes, so d=6. Directly,

```
Lplus=4(8+9)+4(2+3+4)=104,
Br0=-1, rho_0=0, S=104-14=90.
```

The natural-split load on each core unit is 4; the pair load
is 8/3. UNIT-LOAD-0 is exact here:
`S=3(8+9)+(13/3)(2+3+4)=90`.
Thus this partial theorem really does pay the E47 negative
bracket; it is not another assertion of the false Tile-CL.
All other phases of this family are covered by section 7.

## 4. Phase reduction and the precise role of the top window

The following elementary lemma holds at every height.

**Lemma MIN-PHASE (proved on paper).** Let D be an active
nontrivial tile. A phase minimizing the MaxCL slack has
its zero-residue cell in N and its (m-1)-residue cell in A.
In particular its rho_0 cannot equal m-1.

Proof. Give a non-maximal cell coefficient c(x)=d+1 and a
maximal cell coefficient c(x)=1-|x|. Then `S_sigma=sum_D c r`.
Let `C=sum_D c` and `Wtop=sum_A(d+|y|)`. The usual column
census gives `C=(d+1)m-Wtop=m+Dep>0`; alternatively positivity
of C follows from the column-top counting inequality.
As sigma advances by one, the cell of unshifted residue
sigma wraps from zero to m-1. Hence

```
S_(sigma+1)-S_sigma = m*c(phi^{-1}(sigma))-C.
```

Across a non-maximal cell the increase is exactly Wtop>0.
Across a maximal cell of height j>=1 the change is
`-C-m(j-1)<0`. A minimum can therefore have neither a
maximal zero-residue cell nor a non-maximal preceding cell.
The latter is exactly the top-residue assertion. The origin
is non-maximal, proving the last claim. QED.

This is a reduction of a possible WORST phase, not a proof
of nonnegativity at rho_0=m-1 by itself. It does not allow
one to infer MaxCL from a bound averaged over phases.
Indeed each cell satisfies sum_sigma K_sigma(x)=0, since
both its residue and its unit-lift expression have the same
phase sum C_m. Accordingly sum_sigma Br0=0; the positive
and negative bracket parts balance in aggregate but need
not balance at one phase.

## 5. Height-three tiles are a finite quadratic-face cover problem

This exact reduction is used for the certificate and is also
one precise statement of the remaining geometric problem.

Fix m,d, distinct nonzero unit residues p_a, and a set Q of
quadratic monomials whose residues are distinct from zero,
the units, and each other. Let R be the unoccupied residues.
For each cubic y all of whose pair divisors belong to Q,
let P(y) be the SET of these distinct pair divisors. For r
in R write

```
O_r={P(y): |y|=3, phi(y)=r, P(y) subset Q}.
```

**Lemma FACE-EXTENSION (proved).** The face Q extends to a
height-at-most-three tile exactly when every O_r is nonempty.
Every extension is obtained by choosing one such cubic at
each r. Its maximal units are the units isolated from Q,
its maximal pairs are precisely `Q\U`, where U is the union
of the chosen P(y), and all its cubics are maximal.

Proof. Necessity follows from residue bijectivity and the
down-set property. Conversely the origin, all units, Q, and
one eligible cubic for each remaining residue form a down-set
of exactly m cells with distinct residues. There are no
further closure conditions at height three. The assertions
about maximality follow directly from the possible upper
covers. QED.

A **feasible container** C is a subset of Q such that for
every r in R some eligible cubic has P(y) subset C. It need
not be the exact union of pair divisors in an extension.
Let I be the isolated units of Q, and for a phase let

```
F(C)=(d+3)sum_{r in R}(r-sigma mod m)
      +(d+2)sum_{z in Q\C}r(z)+(d+1)sum_{a in I}rho_a.
```

**Lemma CONTAINER (proved).** All extensions of this face
satisfy MaxCL at the given phase if and only if

```
F(C)<=(d+1)C_m for every feasible container C.     (COVER-PAY)
```

Proof. The actual union U of any extension is feasible and
its maximal weighted sum in MAX is exactly F(U). Conversely
choose any eligible cubic inside a feasible C at each r.
Its actual union U is a subset of C, so `F(U)>=F(C)` because
all pair-residue weights are nonnegative. Therefore a failed
container inequality produces an actual failed extension;
and testing all containers tests every actual union. QED.

Equivalently, define

```
Fempty=(d+3)sum_R r+(d+2)sum_Q r+(d+1)sum_I rho_a.
```

The exact payment problem is

```
(d+2) min_{C feasible} sum_C r >= Fempty-(d+1)C_m.  (MIN-COVER)
```

This is an equivalence, not an asserted new universal bound.
The minimum is over a finite family specified entirely by
the legal cubic residues and their pair divisors.

Two optimizations used in the finite checker are justified
as follows. For each r intersect all members of O_r, then
take the union of those intersections; call the result F.
Every feasible container contains F. If the optimistic
bound with only F covered already proves MAX, the whole
face is certified. If not, enumerate every feasible C
between F and Q. This is method 1 in the checker.

Method 0 independently evaluates cubic choices: subtract F
from the divisor sets in each O_r, discard a choice containing
a smaller choice in that same O_r, and enumerate unions of
the remaining choices by dynamic programming. Replacing a
discarded choice only reduces the covered set and increases
F(C), so the retained choices include a worst extension for
every phase. Both evaluations use the same monomial/residue
enumeration; they are not claimed to be independent source
implementations. Section 6 also has a separate Python check.

## 6. H3-D5: a complete finite certificate

**Theorem H3-D5 (proved by finite certificate).** For every
tile with at most five active directions and height <=3,
MaxCL holds at every sigma.

Proof and exact enumeration domain. Active dimension zero
is the one-cell tile. In dimension one a down-set is one
column of length m, and MAX reads `m*r(top)<=m(m-1)`, which
is immediate. For active d=2,3,4,5:

1. Stars and bars gives `d+1<=m<=C(d+3,3)`. The upper bounds
   are 10,20,35,56. Thus the residue and tile domain is finite
   even though the possible semigroup generator lifts and
   conductors are unbounded.
2. The unit residues are distinct and nonzero. A simultaneous
   permutation of coordinates sorts them, so enumerate ALL
   `1<=p_1<...<p_d<m`. No multiplication by a group unit,
   negation, or phase translation is used as a normalization.
3. List every pair and every cubic in these d variables.
   Enumerate every pair subset Q with injective residues
   disjoint from the origin and units. FACE-EXTENSION tests
   exactly which such faces have a tile extension.
4. A face with R empty has height <=2 and is covered by the
   Lean-checked Flat-MaxCL. For R nonempty, check COVER-PAY
   by the feasible-container method, including every phase.
   All pairs that a selected cubic actually covers are
   non-maximal; allowing extra covered pairs in a container
   is justified by CONTAINER, not by an independence claim.
5. A shape bound avoids unnecessary phase calculations. If
   there are t cubic residues, b maximal-pair residues and
   a isolated-unit residues, their total weighted sum is at
   most the dot product of weights d+3,d+2,d+1, repeated
   t,b,a times, with m-1,m-2,... in descending order. This
   is ordinary rearrangement. A nonnegative resulting slack
   certifies every phase for that container.
6. Otherwise the checker computes all phases exactly. For
   its maximal-weight array w(r), put F_sigma=sum_r w(r)
   ((r-sigma) mod m). Then
   `F_(sigma+1)=F_sigma-sum w+m*w(sigma)`. The initial sum
   and this recurrence test sigma=0,...,m-1 using integers.

Every case returns nonnegative slack. The exhaustive counts
are below. The loop description and the proofs of sections
5--6 show that a case outside the checked family cannot be
an active height-three tile in this dimension range. Finally
restore any inactive coordinates using section 1. QED.

The main source is `height3_certificate.c`. It has no floating
point arithmetic or solver dependency. For d<=5 there are at
most 15 potential pairs and 35 cubics; all masks fit in 15
bits, all residue masks in 56 bits. The source uses 64-bit
integer counts and sums. It stops and emits a complete actual
tile if a negative container or choice-union bound is found.

| Active d | m upper bound | All unit residue sets | Sets with <=3-fold coverage | Height-3 quadratic faces | Shape bound | Forced bound | Remaining faces |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | 10 | 120 | 40 | 36 | 35 | 0 | 1 |
| 3 | 20 | 4845 | 549 | 854 | 778 | 65 | 11 |
| 4 | 35 | 324632 | 9601 | 34457 | 32184 | 2121 | 152 |
| 5 | 56 | 32468436 | 229082 | 2443823 | 2341180 | 100466 | 2177 |

The remaining-face evaluations give:

| d | Method-0 unions | Method-1 feasible containers | Largest intermediate method-0 list |
|---:|---:|---:|---:|
| 2 | 2 | 3 | 2 |
| 3 | 24 | 142 | 4 |
| 4 | 784 | 6766 | 35 |
| 5 | 27266 | 575727 | 162 |

There are zero failures. The reported `min_bound` is a
CERTIFIED LOWER BOUND, which can come from rearrangement or
forced coverage; it is not claimed to be the actual minimum
slack over all tiles. The smallest reported bound is zero.
Flat faces counted separately number 11,82,823,13820.

`independent_small.py` does not use containers, forced
intersections, dominance or DP. For d=2,3 in the full ranges
above, it explicitly constructs every eligible cubic choice,
builds the actual down-set, finds its maximal cells by upper
covers, and tests every phase directly. It gives exactly the
same quadratic-face and flat-face counts as the C program,
with 1103 actual height-three tiles and 11963 (tile,phase)
pairs, all nonnegative. This validates the small-dimension
enumeration and evaluation by a separate implementation.

`coverage.c` is an additional independent residue-vector
enumeration at d=5; all its per-m coverage counts agree.
The largest m with a three-fold covering vector is 8,16,25,40
for d=2,3,4,5 respectively. The certificate still checks
the full stars-and-bars ranges; these smaller maxima are
outputs, not unproved bounds used to truncate the run.

**Semigroup corollary H3-E6 (proved, computer-assisted).**
Let S be a numerical semigroup of embedding dimension e<=6.
If every Apéry element with respect to the multiplicity m
has some factorization of length <=3 over the minimal
generators other than m, then Wilf holds for S.

Proof. S=N is trivial. Otherwise the minimum-degree grlex
factorization tile has
height <=3 and d=e-1<=5. It is a down-set, and represents
the m Apéry residues bijectively. H3-D5 gives MaxCL for
every phase, in particular sigma=c mod m. Apply the existing
Lean-checked MaxCL => Tile-TOP'' => Wilf implication. Only
H3-D5's finite assertion is external to that Lean chain.
QED.

In particular the corollary applies when `4n_1>c+m` and
e<=6: each Apéry element is <=c+m-1<4n_1, so none of its
factorizations over generators above m can have length >=4.
The stronger hypothesis "every Apéry factorization has
length <=3" is not needed for H3-E6 itself.

## 7. Arbitrarily many spikes: H3-CORE2

Deleting all isolated unit spikes leaves a cubic core with
k active, non-maximal unit directions, the same q,p,t and
the same set N. Its size is 1+k+q+t. The ambient tile has
d=k+(number of spikes), and `d+1=m-q-t`.

**Lemma SPIKE-BOUND (proved on paper).** Put

```
J=C(1+k+p,2), B=q-p+2t.
```

If `(m-q-t)J>=B(m-1)`, MaxCL holds at every phase.
For a genuine cubic core, J>B, and it suffices that

```
m >= ceil((J(q+t)-B)/(J-B)).                    (SPIKE)
```

Proof. The 1+k+p non-maximal cells have distinct nonnegative
residues, so their sum is >=J. The MaxCL left side is at
most `(q-p+2t)(m-1)=B(m-1)`. This proves the criterion.
For positivity, q<=C(k+1,2) and
`3t=sum_N2 psi(z)<=(k+2)p`: a spike cannot extend a pair.
Consequently

```
6(J-B) >= 6(C(k+1,2)-q)+(2k+1)p+3p^2 >0,
```

since t>0 implies p>0. Solving the linear inequality in m
now gives SPIKE. QED.

This is a convenient explicit spike threshold, derived
from rearrangement; it is not asserted to be sharp.

**Theorem H3-CORE2 (proved on paper plus finite base).**
If a height-at-most-three tile has at most two non-maximal
unit directions, then MaxCL holds at every phase, for
arbitrary total dimension and modulus.

Proof. Height <=2 is Flat-MaxCL. For a cubic core, k>=1.
If k=1, q=p=t=1, J=3, B=2; SPIKE holds for all m>=4,
the minimum possible cardinality. If k=2 then q<=3,
1<=p<=3 and 3t<=4p. The worst parameter values for the
SPIKE threshold at each p give:

| p | q upper | t upper | J | B upper | Sufficient m |
|---:|---:|---:|---:|---:|---:|
| 1 | 3 | 1 | 6 | 4 | 10 |
| 2 | 3 | 2 | 10 | 5 | 9 |
| 3 | 3 | 4 | 15 | 8 | 14 |

Thus every m>=14 is proved analytically. For m<14,
`core2.py` enumerates every pair subset on k=1,2 variables,
every subset of its eligible cubics, retaining only height
three cores with both core directions non-maximal. For
each such core C, every `|C|<=m<=13`, every ordered residue
vector `p_a in {1,...,m-1}` injective on C, and every sigma,
it checks

```
(k+m-|C|+1)sum_{N(C)}r
                   -sum_{A(C)}(|y|-1)r >=0.
```

The omitted residues are exactly the spikes. Hence this
is the original ambient tile inequality, not an injective
non-onto version of MaxCL with the core dimension k.
There are 167 (core,m) rows and 52724 phase checks, zero
failures. This covers every smaller-m case and completes
the proof. QED.

Both mandatory core-plus-spike examples are included
explicitly. At m=14, core Delta_3 and p_core=(5,6), the
spike residues are 7,8,9,13 and the minimum MaxCL slack
is 104. For p_core=(8,9), the spike residues are 1,5,6,7
and the minimum is 90. The full phase lists are in
`core2_named.json`. At the full Delta_3 parameter row,
SPIKE already gives `7*15-8*13=1>0` at m=14; the actual
residue information improves the bound substantially.

## 8. Checks, adversarial search, and preserved failures

### 8.1. Exact charging checks

`charging_checks.py` has an independent value/degree/lex
Dijkstra construction of Apéry tiles. It removes redundant
generators, verifies the down-set and residue-bijection
properties, and checks every phase of every accepted tile.
The named cases include E47, E51, their explicit core/spike
descriptions, <14,16,17,19>, <16,17,20,21>, and <4,7>.
The random run uses seed 2026101981, 1200 proposals,
5<=m<=250, proposed dimensions 2..12, with uniform,
near-arithmetic, and mixed generator modes.

It accepts 120 tiles of height <=3, including 76 of height
exactly three. There are 3327 phase checks, of which 2801
have height exactly three. Results:

```
UNIT and CENTER-ID: 0 mismatches;
PAIR-ZERO: 476 qualifying phases, including 29 with negative cubics;
CENTERED-PAIR: 383 phases, 216 with Br0<0,
  including 52 height-three phases with Br0<0;
UNIT-LOAD-0: 103 tiles satisfy UL3 at sigma=0;
MIN-PHASE: 79 minimizing height-three phases, all at the stated boundary;
dropping Lplus: 2 failures (the E47 tile in its two equivalent descriptions).
```

The checks include the stronger displayed lower bounds,
not just S>=0. Phase-summed Br0 is exactly zero on every
tile. `charging_named.json` gives every named tile and
phase's S,Lplus,Br0,Br1; `charging_witnesses.json` retains
examples exercising the two carry regimes nonvacuously.

### 8.2. Search over arbitrary height-three tiles

`milp_adversary.py` searches beyond the low-dimensional
certificate and beyond fixed normal-form choices. For
fixed p,m,sigma it introduces binary variables for all
pairs and cubics, residue-class exact-cover constraints,
the cubic-to-pair down-set constraints, and indicators for
maximal units and pairs. It maximizes the MaxCL left side.
This is a counterexample search, not a finite proof: SciPy
HiGHS uses floating point. Every returned incumbent is
rounded, then its actual cell set, down-set property,
cardinality, residue bijection and all MaxCL phase slacks
are checked with exact integers. A negative actual slack
would stop and save full data.

The run at seed 2026101982 has 30 residue profiles, active
d=6..12, including the three-block postage-stamp bases
of sizes m=27,64,125 and random three-fold covering bases.
It makes 89 phase optimization calls, with a 2-second
limit per call and HiGHS threads=1. Every call returns
an incumbent; 59 calls report optimality and 30 hit their
time limit. The
worst exact minimum phase slack among those incumbents
is 429. There is no MaxCL counterexample. Solver optimality
is recorded only as search data, not used to prove a
universal mathematical assertion.

### 8.3. Preserved false intermediate statements

**F1: the stated cubic carry range in pairform_h3.py.**
The expression

```
kappa(y)=[sum_a y_a r(y-e_a)-rho_0-2r(y)]/m
```

can be -2. The smallest possible m for a height-three tile
is four, and it already fails there: D={0,e,2e,3e}, p=3,
sigma=2, residues 2,1,0,3, kappa=-2. The pair-form identity
remains valid. Its integer range is [-2,2], since its
numerator lies strictly between -3m and 3m. Counting
negative cubic carries without their magnitude is not
the negative contribution when -2 occurs. This does not
alter the accepted UNIT identity. The exact example is
also the sharp PAIR-ZERO example from section 2.

**F2: some one of the two origin lifts always removes
the nonzero carries.** False on the same m=4 column, now
at sigma=0. Along 0,e,2e,3e the original carries are
`0,0,1,2`; after using origin lift -4 they are
`-1,0,2,4`. MaxCL is true, with slack 8. Thus the centered
strategy is a sufficient regime, not a universal reduction
to a no-carry case. This is already minimal m at height three.

**F3: the forced-pair intersection always suffices.**
A smallest-m example is m=6,d=2,p=(1,5), Q={2e_1,2e_2}. The sole
remaining residue is 3, with eligible cubics 3e_1 and 3e_2.
Their divisor-set intersection is empty. At sigma=5,
treating both pairs as maximal gives the optimistic
weighted sum 52 against target 45, slack -7. The two
actual cubic choices have slacks 5 and 13 at that phase;
their minima over ALL phases are 5 and 4. At least one
of the pairs must be non-maximal, and its positive cost
is exactly the payment lost by the forced-only bound.
Minimality in m follows without an exhaustive assumption:
an active height-three tile has m>=d+3. At m=4 it is a
single column. At m=5 the only additional possibility is
d=2,q=t=1, where the unique eligible cubic has its unique
pair divisor forced. Thus the forced bound is exact there
and is nonnegative by the one-core-variable case of section 7.
This is not an actual MaxCL counterexample. It explains
why the certificate needs cubic-choice/container reasoning
after the forced test. `failure_checks.py` verifies all
these small data exactly.

The preexisting false H3-BR / Tile-CL remains preserved
by the explicit E47 calculation in section 3. No failure
of Wilf or an accepted project theorem was found.

## 9. Formalization targets and the exact remaining family

The following pieces have direct finite/algebraic Lean
statements, with no analytic or asymptotic input:

- `cubic_lift_identity`: CUBIC-LIFT over integers.
- `negative_cubic_mem_top_half`: non-maximal pair K=0
  implies a negative cubic has K=-1 and residue in the
  specified interval of floor(rho_0/2) integers.
- `maxCLPhase_of_pair_zero`: UNIT, that injection bound,
  and nonnegativity give PAIR-ZERO, including its parity term.
- `centered_bracket_identity` and `maxCLPhase_of_centered_pair`:
  CENTER-ID and nonnegative nonzero centered carries.
- `maxCLPhase_of_unit_load_zero`: the subadditive split
  sum and the explicit UL3 load inequalities.
- `maxCL_min_phase_boundary`: the finite phase recurrence
  and positivity of its two step types.
- `height_three_face_extension` and `maxCL_of_cover_payment`:
  FACE-EXTENSION, the maximal-cell census, and CONTAINER.
- `maxCL_of_spike_bound`: the distinct-residue lower sum
  and SPIKE. The H3-CORE2 finite base is small enough for
  a separate direct finite check.

Here `MaxCLPhase` should mean the subtraction-free MAX
inequality at a fixed sigma; `MaxCLAt` in the current Lean
file quantifies over all sigma. Quantifiers should not be
silently interchanged. H3-D5 is a computer-assisted paper
theorem. The C execution has not been imported as a Lean
kernel theorem; translating the finite predicate/checker
is additional work, not a completed formalization claim.
For the semigroup corollary, the existing grlex factorization
tile argument for height two changes only its degree bound
from two to three, before using the same general Wilf chain.

For a hypothetical counterexample to height-three MaxCL,
remove inactive directions and choose a phase minimizing
its slack. The results here reduce it to the following
EXACT necessary family:

```
d>=6, height exactly 3, k>=3 non-maximal units;
d+3<=m<=C(d+3,3), m=1+d+q+t;
J=C(1+k+p,2), B=q-p+2t,
(m-q-t)J < B(m-1);
zero-residue cell in N, top-residue cell in A, rho_0<=m-2;
either some N2 carry K!=0, or some A2 carry K<0;
either nu>d+1, or some N2 carry K+1!=0;
if rho_0=0, UL3 fails for at least one unit (and some psi>=4);
the feasible-container inequality COVER-PAY fails for
  the actual quadratic face and some feasible container.
```

This family is still unbounded in d. It has not been
reduced to one finite computation. The exact remaining
payment problem is MIN-COVER, or equivalently the mixed
carry regime in UNIT after spending Lplus. No claim is
made that the two new carry regimes cover that family.

For the semigroup goal, the accepted Eliahou condition
3e>=m additionally removes that range without requiring
MaxCL. Thus a remaining height-three semigroup may be
assumed to have e>=7 and m>3e; its conductor phase must
also fail the applicable new sufficient criteria. The
worst-phase boundary assertion concerns the all-phase
MaxCL route and is not asserted automatically for c mod m.

Strategic assessment. The carry-window and centered-lift
arguments prove real dimension-free regimes, but making
the bracket nonnegative without Lplus is the already-false
Tile-CL. The forced-cover bound alone also loses necessary
payment, as F3 demonstrates. The finite face reduction
closes an infinite semigroup class by controlling all
residue data in active dimension five, and the spike
threshold closes the recurring two-variable core examples
uniformly. The next useful lemma must pay MIN-COVER for
mixed non-maximal-pair carries, using the non-forced pair
costs or Lplus. A further blind dimension increment or
more random carry sampling is not substituted for it.

## 10. Reproducibility

All programs and data are in this directory and on fejer
under `~/wilf/p6`. The C programs use the standard library.
The exact Python checkers use only the standard library;
the adversarial MILP search uses the installed numpy/scipy
in `~/mathenv`. No sympy or local numerical computation.

```sh
cd ~/wilf/p6
nice -n 10 gcc -O3 -Wall -Wextra height3_certificate.c -o height3_certificate
nice -n 10 ./height3_certificate 2 3 10 > cert_d2.log
nice -n 10 ./height3_certificate 3 4 20 > cert_d3.log
nice -n 10 ./height3_certificate 4 5 35 > cert_d4.log
nice -n 10 ./height3_certificate 5 6 19 > cert_d5_6_19.log
nice -n 10 ./height3_certificate 5 20 29 > cert_d5_20_29.log
nice -n 10 ./height3_certificate 5 30 56 > cert_d5_30_56.log
nice -n 10 ./height3_certificate 2 3 10 1 > container_d2.log
nice -n 10 ./height3_certificate 3 4 20 1 > container_d3.log
nice -n 10 ./height3_certificate 4 5 35 1 > container_d4.log
nice -n 10 ./height3_certificate 5 6 56 1 > container_d5.log
nice -n 10 gcc -O3 coverage.c -o coverage
nice -n 10 ./coverage 5 > coverage_d5.log
nice -n 10 ~/mathenv/bin/python independent_small.py > independent_small.log
nice -n 10 ~/mathenv/bin/python core2.py > core2.log
nice -n 10 ~/mathenv/bin/python charging_checks.py 2026101981 1200 > charging.log
nice -n 10 ~/mathenv/bin/python failure_checks.py > failure_checks.log
nice -n 10 ~/mathenv/bin/python milp_adversary.py 2026101982 30 2 > milp_2026101982.log
nice -n 10 ~/mathenv/bin/python audit_p6.py > audit.log
```

The initial C certificate used four concurrent single-core
jobs: d=2..4 sequentially in one job, and the three d=5
intervals in the other three. The later Python checks and
container evaluation also respected the four-core limit.
HiGHS was explicitly restricted to one thread. The final
audit checks full parameter-range coverage, all prefix
counts across the two C methods, the independent Python
face counts, the separate d=5 covering counts, the core
certificate, and the named/failure checks. Source/data
digests are in `SHA256SUMS`, with results in `P6_AUDIT.json`.
