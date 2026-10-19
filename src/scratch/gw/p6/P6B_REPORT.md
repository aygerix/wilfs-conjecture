# P6b: height-three MaxCL, core dimension and two packing payments

2026-10-19. **The full height-three MaxCL theorem remains open.**
The accepted `P6_REPORT.md` is unchanged. New results in this report are:

1. **H3-CORE3, analytic proof with a small finite base:** MaxCL at every
   phase when at most three unit directions are non-maximal, with no
   bound on the total number of directions or spikes. CR leaves two
   canonical realizable shapes, only at m=14,15,17. The independent
   base has 224 ordered injective labelings and 3400 phase checks.
2. **ROW-PACK and RETAINED-PACK, proved:** a cyclic signed-label bound
   from pairs whose every cubic successor is present. It applies on
   any retained complete quadratic face. No integer DIFF2 statement
   is transferred to a cyclic group.
3. **DENSE9, proved analytically:** if all pairs are present and at most
   floor(k^2/9) cubics are missing, MaxCL holds at every phase, for every
   core dimension k>=3 and any spike count.
4. **DENSE075, proved analytically:** for arbitrary quadratic faces,
   at most floor(3k^2/40) missing cubics imply MaxCL at every phase,
   uniformly for k>=3. This uses a quadratic-defect bound, deletion of
   endpoints, signed packing and an explicit CR polynomial certificate.
5. **FLAT-CR, proved:** a second rearrangement payment which first pays
   maximal pairs by the flat top-window argument. With a complete
   quadratic face this proves **THREE-CUBICS** (t<=3) for every k,
   and the **FEW-CUBICS** theorem for k>=19 and t<=floor(k^2/16).
6. **SHADOW-COVER, proved by a standard algebraic argument:** the upper
   cubic shadow of a loop graph on k vertices has size at least k
   times its minimum vertex-cover number. It sharpens the retained
   face reduction; it is not needed by the DENSE075 constant.

These are statements about all injective labelings of the indicated
cores, and therefore about all residue-complete tiles obtained by
spikes. They are not assumptions about semigroup normal forms. The
full missing-middle family is specified in section 9.

All numerical work ran on fejer, `~/wilf/p6b`, nice 10, with at most
four owned single-core jobs. No commits. P4/P5h was not investigated.
Programs and data are in `b/`; commands are in section 10.

## 1. Exact notation and accepted dependencies

Delete isolated maximal units from a height-at-most-three tile. The
remaining core C has k unit directions, all non-maximal. Put

```
Q = quadratic cells,       q=|Q|,
T = cubic cells,           t=|T|,
N2 = non-maximal pairs,    p=|N2|,
a=q-p,                    |C|=1+k+q+t,
s=m-|C|,                  d=k+s,
N=C\Max(C),               |N|=1+k+p.
```

Every injective linear labeling of C into Z/m extends to a tile by
one maximal unit on each missing residue. These spikes contribute
zero to the first MaxCL left side. Thus the exact slack at a phase is

```
S=(d+1)sum_N r - sum_{Max(C)}(|y|-1)r(y),
r(x)=(phi(x)-sigma) mod m in {0,...,m-1}.
```

The accepted spike reduction identifies this with the original tile
slack, for every sigma. Write rho_0=r(0), rho_i=r(e_i), and

```
Q_k=C(k+1,2), U_k=C(k+2,3), epsilon=U_k-t,
j=Q_k-p, e=Q_k-q, so j=e+a,
J=C(1+k+p,2), B=a+2t.
```

Height <=2 is Flat-MaxCL. At height exactly three, the accepted
SPIKE-BOUND proof gives J>B. We use the accepted H3-D5 for d<=5,
H3-CORE2, the phase-boundary lemma MIN-PHASE, and the two carry
criteria PAIR-ZERO and CENTERED-PAIR. None is weakened here.

The exact CR lower bound is

```
S >= R(m),
R(m)=(m-q-t)J - B(m-1) + t(t-1)+a*t+C(a,2).       (CR)
```

Indeed the |N| residues sum to at least J, while giving the t
cubics the largest residues and the a maximal pairs the next
largest gives the upper sum
`B(m-1)-t(t-1)-a*t-C(a,2)`. This is the lead's CR, written in
a form linear in m. In particular, with

```
A_CR=J(q+t)-t^2-t-a*t-a(a+1)/2,
m_CR=ceil(A_CR/(J-B)),
```

every m>=m_CR is proved. A hypothetical counterexample must have
`m<=m_CR-1`. This is a finite cutoff for a fixed core, not for
unbounded k.

For fixed k,q,t,m, increasing p also increases R. If
`N_0=1+k+p` and a=q-p, its exact increment is
`(m-q-t)N_0+(m-t-a)>0`. This follows either from the
displayed formula or by removing the last maximal-pair
weight and adding one non-maximal cell to the lower sum.
FLAT-CR below is likewise increasing with p. These
monotonicities justify all worst-shadow-size tests.

## 2. Cyclic pair packing and successor-complete rows

Here phi is unshifted. All assertions are in Z/m, at arbitrary m,
including composite m and groups with 3-torsion.

**Lemma PAIR-PACK (proved).** If all quadratic monomials on h
directions are present, then

```
m >= h^2+h+1.                                    (PAIR-PACK)
```

Proof. Put A={0,p_1,...,p_h}. All formal two-term sums from A,
with 0 interpreted as padding, are distinct: they are exactly
the origin, units and pairs. The h(h+1) off-diagonal differences
u-v, u!=v in A, are nonzero and distinct. Equality u-v=u'-v'
would give equality of the present two-term sums u+v'=u'+v;
equality of formal multisets, together with the off-diagonal
condition, implies u=u', v=v'. Add zero. QED.

Suppose all pairs on these h directions are present. Call a pair
z **successor-complete** when z+e_i is a present cubic for every
one of the h directions. Let f_0 count the successor-complete
loops and f_1 the successor-complete ordinary pairs.

**Lemma ROW-PACK (proved).**

```
m >= h^2+h+1 + h*f_0 + (h-1)*f_1.                (ROW-PACK)
```

Proof. Start with zero and all off-diagonal differences from A.
For each successor-complete pair z add the labels

```
phi(z)-c,  c in A, c not in the support of z.
```

Here 0 never belongs to the support of z. A loop contributes h
labels; an ordinary pair contributes h-1.

Two such labels being equal gives `phi(z)+c'=phi(z')+c`.
Both sides are present: a pair if the extra term is zero, a
cubic otherwise. Injectivity gives equality of the padded
formal multisets. If c!=c', the index c occurs on the right
but not on the left, because c is outside supp(z); the case
where one is zero is also excluded by degree. Thus c=c' and
z=z'. This is exactly uniqueness of the reduced signed label.

Equality with an old difference u-v gives `phi(z)+v=u+c`.
The left side is present by successor completeness, and the
right side is a present pair, unit or origin. Formal equality
is impossible since c is outside supp(z). Equality with zero
is excluded in the same way. All counted labels are therefore
distinct in Z/m. QED.

Let epsilon_3, epsilon_21, epsilon_111 count missing cubics of
the three multiplicity types on this h-dimensional face. Put
`H(h+1)=(h^3+2h^2+3h+2)/2`.

**Corollary ROW-DEF (proved, h>=2).**

```
m >= H(h+1) - h*epsilon_3 -(2h-1)*epsilon_21
                         -3(h-1)*epsilon_111
  >= H(h+1)-3(h-1)*epsilon_I,                   (ROW-DEF)
```

where epsilon_I is their sum. To prove it, start with all pair
rows. Their label count plus PAIR-PACK is H(h+1). A missing
pure cube spoils a loop row, of weight h; a 21 cube spoils
one loop and one ordinary row, total 2h-1; a 111 cube spoils
three ordinary rows, total 3(h-1). Union bound the spoiled
row weights. For h>=2 each listed weight is <=3(h-1). QED.

**Lemma RETAINED-PACK (proved).** Every subset I of the core
directions whose complete quadratic face is present satisfies
ROW-PACK and ROW-DEF with h=|I|, successor completeness tested
only within I, and epsilon_I the missing cubics within I.
Only present cross-cubics are used by the proof, so directions
outside I do not matter. In particular this gives an explicit
packing lower bound for the ORIGINAL modulus m, without
asserting MaxCL for a non-surjective subcore.

The labels and their reduced normal forms avoid the DIFF2
3-torsion issue. No assertion that pairwise distances +/-d
determine at most two points is used.

## 3. H3-CORE3, with complete CR classification

**Theorem H3-CORE3 (proved, small finite base).** Every tile
of height <=3 with at most three non-maximal unit directions
satisfies MaxCL at every phase. The total dimension and the
number of spikes are unbounded.

Proof. Use H3-CORE2 if k<=2, Flat-MaxCL if t=0, and H3-D5
if d<=5. It remains to treat k=3, s>=3.

The possible cubic-shadow sizes have the exact table

| p | 1 | 2 | 3 | 4 | 5 | 6 |
|---:|---:|---:|---:|---:|---:|---:|
| Maximum t | 1 | 2 | 4 | 5 | 7 | 10 |

Here is a direct proof, requiring no general shadow theorem.
A missing pair forbids exactly three of the ten cubics.
Two different pairs have at most one common cubic successor.
Thus one or two missing pairs leave at most 7 or 5 cubics.
Three missing pairs leave at most 4. Equality in the last
case requires their three pairwise intersections to be
distinct and no triple intersection. On three vertices this
means the absent pairs are the loop and two incident edges
at one vertex; the remaining pairs and cubics are the full
binary simplex. A triangle has one triple intersection and
leaves only three cubics. With only one or two present pairs,
there is no squarefree cubic; a 21 cubic needs its loop and
ordinary pair, and its only possible companion with two
pairs is the pure cube at that loop. This proves t<=1,2.
All table entries are attained.

At s=3, d=6, CR is

```
7*C(p+4,2) >= t^2+(2q+13)t+(q-p)(q+6)-C(q-p,2). (CORE3-CR)
```

For fixed p,t its right side increases with q. For fixed p,q
it increases with t. If q<=5, replace q by 5 and t by the
table maximum. The CR slacks for p=1,...,5 are

```
8, 25, 18, 45, 42.
```

If q=6 the six slacks at the maximum t are

```
-6, 9, -2, 23, 16, -35.
```

Reducing t to the next integer already makes the negative
p=3 and p=6 entries positive. The slope as s increases is
J-B>0. Thus CR leaves EXACTLY these cardinalities:

| q,p,t | s | m | Shape of T | CR slack |
|---|---:|---:|---|---:|
| 6,1,1 | 3 | 14 | one pure cube | -6 |
| 6,1,1 | 4 | 15 | one pure cube | -3 |
| 6,3,4 | 3 | 17 | full binary cubic face | -2 |
| 6,6,10 | 3 | 23 | full ternary simplex | -35 |
| 6,6,10 | 4 | 24 | full ternary simplex | -10 |

The full ternary simplex has m>=H(4)=28 by ROW-PACK,
excluding its two rows. Up to coordinate permutation, the
remaining two canonical shapes are Q=all six pairs and
T={x_1^3}, at m=14,15, or T=all four cubics on x_1,x_2,
at m=17. The exact independent finite base is:

| Shape | m | Ordered injective residue vectors | Phases | Minimum S |
|---|---:|---:|---:|---:|
| pure | 14 | 24 | 336 | 39 |
| pure | 15 | 168 | 2520 | 52 |
| binary | 17 | 32 | 544 | 69 |

`core3_independent.py` lists EVERY ordered vector of three
distinct nonzero residues, retains the injective core
labelings, determines maximal cells directly, and evaluates
every phase with multiplier `k+1+m-|C|`. Thus it is exactly
IMaxCL, with the spike bonus, not the false unbonused
injective version. Its three finite loops complete the
proof. QED.

As a separate cross-check, `core3.c` enumerates all 2246
height-three cores with three non-maximal units. Below
their CR thresholds and outside H3-D5 it has 11 shape/m
rows, 6941 nominal sorted vectors, 112 injective vectors,
1700 phase checks, nine realized rows, zero failures.
The largest CR threshold is 25. This exhaustive calculation
agrees with the analytic classification; it is not used to
replace that classification in the proof.

Semigroup consequence: if a height-three factorization tile
has at most three non-maximal unit directions, Wilf follows
from MaxCL at sigma=c mod m and the accepted Lean implication.
There is no bound on its embedding dimension. The new finite
base itself has not been imported into Lean.

## 4. Two quadratic-defect bounds and a cover refinement

Let E be the set of all quadratic monomials NOT in N2,
including absent pairs and present maximal pairs, so |E|=j.
Every z in E has all k cubics z+e_i missing. Different z
have at most one common cubic successor. Each missing
cubic has at most three distinct pair divisors. Hence

```
k*j <=3epsilon,
k*j-C(j,2) <=epsilon.                           (SHADOW-DEF)
```

The second bound is the first two terms of inclusion-exclusion
on these successor families. Both bounds apply to the same
localized defect epsilon; absent pairs are not counted a
second time. These are elementary proved inequalities.

Deleting one endpoint from every absent pair produces a
retained complete quadratic face of at least k-e directions,
and therefore of at least k-j directions. This elementary
deletion is enough for DENSE075 below.

There is a stronger, separate statement.

**Lemma SHADOW-COVER (proved).** If E is ANY family of
quadratic monomials in k variables, with loops permitted,
and tau(E) is the minimum number of variables hitting every
monomial, then its upper cubic shadow satisfies

```
|{y: |y|=3, some z in E divides y}| >= k*tau(E). (SHADOW-COVER)
```

Proof. Work over the infinite field Q in R=Q[X_1,...,X_k],
and let I be the monomial ideal generated by E. A coordinate
prime contains I exactly when its variables hit E. Any
prime containing I contains such a coordinate prime: a
prime containing X_iX_j contains X_i or X_j. Consequently
height(I)=tau(E).

Choose tau(E) generic Q-linear combinations of the quadratic
generators forming a regular sequence f_1,...,f_tau. Here
is the existence argument. After i<tau choices, the complete
intersection has its associated primes of height i; none
contains I. The degree-two span of E is therefore not
contained in any of these finitely many primes. Over Q a
finite union of proper linear subspaces cannot cover that
span, so a further quadratic combination can be chosen as
a nonzerodivisor. Polynomial rings are Cohen-Macaulay and
quotients by regular sequences have this complete-intersection
property; the standard dimension/regular-sequence facts are
in [Stacks 10.104](https://stacks.math.columbia.edu/tag/00N7)
and [Proposition 10.103.4](https://stacks.math.columbia.edu/tag/00N6).

Regular sequences are Koszul-regular, so there is no linear
syzygy among these quadrics: a degree-three first syzygy
would be a Koszul boundary from degree at least four.
Thus the k*tau cubic forms X_i f_b are linearly independent.
They belong to I_3, whose monomial basis is exactly the
upper cubic shadow of E. This proves the inequality. The
Koszul implication used here is
[Stacks Lemma 15.31.2](https://stacks.math.columbia.edu/tag/062F).
QED.

The coefficient k is sharp. For E consisting of tau
different loops, the tau successor families are disjoint
(a cubic cannot contain two different squares), each
has k elements, and the cover number is tau.

Applied to the missing-pair family Q_k\Q, this proves
`tau_Q<=floor(epsilon/k)`. Thus one may retain at least
`k-floor(epsilon/k)` directions with every pair present.
Applied to E=Q_k\N2 it gives the same cover bound for the
larger defect family. This is a stronger choice of retained
face in RETAINED-PACK. It is not an invocation of the
unproved ambient P(C) or a matching-number substitute for
the vertex-cover number.

`shadow_cover.c` checks every loop graph for k=1,...,6:
2,8,64,1024,32768,2097152 graphs respectively. It independently
computes the upper shadow and minimum vertex cover and has
minimum slack zero throughout. Those finite checks support,
but do not supply, the unbounded algebraic proof.

## 5. DENSE9: complete quadratic face, epsilon<=k^2/9

**Theorem DENSE9 (proved analytically).** Let k>=3, let all
Q_k pairs be present, and suppose `epsilon<=floor(k^2/9)`.
Then every injective core labeling, with arbitrary spikes,
satisfies MaxCL at every phase.

Proof. Put Q=Q_k, U=U_k, t=U-epsilon and

```
H=(k^3+2k^2+3k+2)/2,
M=H-3(k-1)epsilon.
```

ROW-DEF gives m>=M. Moreover

```
M-|C|=k(k^2-1)/3-(3k-4)epsilon
      >=(4k^2-3k)/9>0.                          (D9-SIZE)
```

By SHADOW-DEF, a=j<=3epsilon/k<=k/3. With
`N_a=1+k+Q-a`, `J_a=N_a(N_a-1)/2`, let

```
F(k,epsilon,a)=(M-Q-t)J_a -(a+2t)(M-1)
                         +t(t-1)+a*t+a(a-1)/2.
```

Since R has positive m-slope J-B, `R(m)>=F(k,epsilon,a)`.
For real 0<=a<=k/3 its derivative is

```
-(M-Q-t)(N_a-1/2)-M+t+a+1/2 <0,
```

using D9-SIZE. Thus replace a by k/3. As a polynomial in
epsilon the resulting F is concave, with quadratic
coefficient `7-6k<0`. It is enough to check epsilon=0 and
epsilon=k^2/9. Call these endpoints E_0(k),E_1(k). Their
complete symbolic certificates, with coefficients listed
in increasing powers, are:

```
216 E_0(k): [0,18,-87,-208,-189,-59,12,9]
216 E_0(4+x): [73176,197210,181129,83328,21671,3253,264,9]

216 E_1(k): [0,18,-63,-176,-99,-22,6]
216 E_1(7+x): [35112,178378,107765,27432,3541,230,6].
```

All shifted coefficients are positive, proving the result
for k>=7, without any asymptotic remainder.

For k=3,4,5,6 the permitted epsilon is <k. A maximal pair
would have k missing successors, so a=0. Now F is still
concave in epsilon. Its two endpoint values are:

| k | floor(k^2/9) | F(k,0,0) | F(k,floor(k^2/9),0) |
|---:|---:|---:|---:|
| 3 | 1 | 90 | 9 |
| 4 | 1 | 845 | 417 |
| 5 | 2 | 4200 | 1410 |
| 6 | 4 | 15050 | 918 |

They are positive. Thus R(m)>=0 at every parameter, and
CR proves every phase. QED.

`dense_poly.py` constructs these polynomials with exact
Fractions. `certificate_tables.py` independently evaluates
the original endpoint expressions at every k=3,...,200
and checks them against the displayed coefficient arrays.
The shifted coefficient identities, not that finite range,
prove the assertions for all k.

## 6. DENSE075: arbitrary quadratic faces

**Theorem DENSE075 (proved analytically).** For every k>=3,
every height-three core with

```
epsilon=U_k-t <= floor(3k^2/40)
```

satisfies MaxCL at every phase, for every injective labeling
and every number of spikes. No completeness assumption on
the quadratic face is made.

Proof. SHADOW-DEF gives j<=9k/40<k. On [0,k] the function
`kx-x(x-1)/2` is increasing. At x=2k/25 it equals
`48k^2/625+k/25`, strictly exceeding 3k^2/40. Its quadratic
coefficient exceeds 3/40 by 9/5000. Thus

```
j<2k/25, p>=Q_k-2k/25, a<=2k/25.               (G-DEF)
```

Delete one endpoint of each absent pair. There is a
retained complete quadratic face with h>=k-j>23k/25.
Set n=23k/25 and, for 0<=epsilon<=3k^2/40, put

```
M= (n^3+2n^2+3n+2)/2 - 3(n-1)epsilon,
N_0=1+k+Q_k-2k/25, J_0=N_0(N_0-1)/2,
t=U_k-epsilon.
```

The ROW-DEF lower bound is increasing in the retained
dimension on h>=n: its derivative is
`3h^2/2+2h+3/2-3epsilon>0`. The missing cubic count on
the retained face is at most epsilon. Hence m>=M.
Also `M-Q_k-t>0`: this affine function of epsilon is
positive at both endpoints (its cubic coefficient is
positive at both, and its only negative lower coefficient
at epsilon=0 is absorbed already at k>=1).

Use the positive m-slope of actual R, then G-DEF. Since
`a*t+C(a,2)>=0` for integer a>=0,

```
R(m)>=G(k,epsilon),
G=(M-Q_k-t)J_0 -(2k/25+2t)(M-1)+t(t-1).          (G075)
```

G is concave in epsilon: its quadratic coefficient is
`7-138k/25<0` for k>=3. Thus check epsilon=0 and
epsilon=3k^2/40, denoted G_0,G_1. The complete integer
polynomial and positive shifted certificates are:

```
703125000 G_0(k):
 [0,264843750,159640625,-391325625,-532985875,
  -186581751,25943450,19571250]
703125000 G_0(4+x):
 [77984419176,328032750270,345367776485,169793836215,
  45801407105,7012001049,573938450,19571250]

5625000000 G_1(k):
 [0,2118750000,1699000000,-1994355000,-2849846375,
  -1003817883,-20096150,11023125]
5625000000 G_1(12+x):
 [22919125863744,75808090115760,31471986477760,5721335523480,
  560191996645,30883189317,905846350,11023125].
```

Every shifted coefficient is positive, so k>=12 is proved.
For 3<=k<12, epsilon<k. An absent pair would have k missing
cubic successors, so no pair is absent. DENSE9 applies,
since 3/40<1/9. QED.

This theorem is unconditional. The calculations in
`generic_density.py` and `certificate_tables.py` verify
the two identities with exact rationals; no LP solver,
Macaulay approximation, conjectural P(C), or limiting
positivity assumption enters the proof.

## 7. A flat-window payment for few cubics

**Theorem FLAT-CR (proved, all k, all phases).** In the
notation of section 1, every core and spike completion has

```
S >= F_flat(m),
F_flat(m)=s*C(k,2)+(k+s+2)*C(p,2)
                       -3t(m-1)+t(t-1).         (FLAT-CR)
```

In particular `F_flat(m)>=0` is an unconditional MaxCL
criterion. It treats maximal pairs by the flat window
rather than assigning all of them the largest residues.

Proof. For every pair z let

```
K(z)=(sum_i z_i rho_i-rho_0-r(z))/m in {-1,0,1},
b_- = #{z in Q: K(z)=-1},
b_+ = #{z in Q: K(z)=1},
U=sum_i(d+1-deg_Q(i))rho_i.
```

The flat identity on ALL pairs, including N2, gives

```
S=U-t*rho_0+(d+2)sum_N2 r-2sum_T r
                         +m(rho_0-b_-+b_+).    (HYBRID-ID)
```

This follows by summing
`r(z)=sum_i z_i rho_i-rho_0-mK(z)` over Q and using
`d+1+q=m-t`. A negative pair lies in the top window
[m-rho_0,m), so b_-<=rho_0 by residue injectivity. Also
deg_Q(i)<=k+1, hence U>=s sum_i rho_i. The k unit residues
and the p pair residues are individually distinct, giving
their lower sums C(k,2), C(p,2). Finally rho_0<=m-1 and
the distinct cubic residues have
`2sum_T r<=2t(m-1)-t(t-1)`. Substitute these bounds and
drop the nonnegative window remainder to obtain FLAT-CR.
QED.

No assertion that the bracket alone is nonnegative has
been made; HYBRID-ID retains the available unit and pair
linear payments. In particular this is not the false
Tile-CL strengthening.

For a complete quadratic face, put C_2=C(k,2). PAIR-PACK
gives `m>=k^2+k+1`, so `s>=C_2-t`. Dropping the pair
term in FLAT-CR, and assuming C_2-3t>=0, yields

```
S >= C_2^2 -(C_2+3k(k+1)+1)t+t^2.               (FEW-POLY)
```

Here the positive slope C_2-3t justifies using the packing
lower bound on m; there is no unverified monotonicity.

**Corollary FEW-CUBICS (proved).** If all pairs are present,
k>=19 and t<=floor(k^2/16), MaxCL holds at every phase.

Indeed the FEW-POLY expression decreases with t throughout
that interval. At t=k^2/16 it is exactly

```
(3k^2/256)(3k^2-56k+16).
```

For k=19+x, the quadratic factor is `35+58x+3x^2>0`.
The required m-slope is also positive. QED.

**Theorem ONE-CUBIC (proved, finite k=4 base).** If all
pairs are present and there is exactly one cubic, MaxCL
holds at every phase, for every k and spike count.

Proof. k<=3 is H3-CORE3. For k>=5, FEW-POLY at t=1 is
exactly `k(k+1)(k-5)(k+2)/4>=0`, and C_2-3>0.
For k=4, the worst shadow size is p=1; p>=2 only
increases the CR slack. In the worst case CR reads
`R(m)=4m-109`, so it handles m>=28. PAIR-PACK excludes
m<21. If p=1, the cubic is a pure power; enumerate the
four possible axes. The remaining finite base is:

| m | Sorted full-pair bases | Injective (base,cubic-axis) | Phases | Min S |
|---:|---:|---:|---:|---:|
| 21 | 10 | 12 | 252 | 148 |
| 22 | 0 | 0 | 0 | -- |
| 23 | 110 | 176 | 4048 | 173 |
| 24 | 60 | 80 | 1920 | 203 |
| 25 | 300 | 600 | 15000 | 148 |
| 26 | 180 | 360 | 9360 | 162 |
| 27 | 900 | 1800 | 48600 | 176 |

There are 3028 actual injections and 79180 phases, all
nonnegative. `one_cubic4.c` enumerates every increasing
four-tuple, checks injectivity of the full pair face and
chosen cubic, and tests every phase with d=m-12.

For p>=2 at k=4 the same one-cubic CR bound is stronger:
J increases and a decreases, and at m>=|C| all its
changes increase R. Alternatively at the smallest p=2,
q=10,t=1, CR has slack 46 at m=21, with positive
m-slope; p=3 is stronger again. Thus only the pure-cubic
base is needed. QED.

`one_cubic4_independent.py` fixes the pure cubic at one
axis, enumerates ALL ordered four-tuples, builds actual
cells and determines maximality directly. Its counts are
exactly six times the preceding injection/phase counts:
18168 injections, 475080 phases, identical minima. The
factor six is the permutations of the other three axes.

**Theorem THREE-CUBICS (proved, small finite bases).** A
complete quadratic core face with t<=3 satisfies MaxCL
at every phase, for every k and spike count.

Proof. t=0 is flat and t=1 is ONE-CUBIC. With two cubic
cells p>=2; with three cubic cells p>=3, since two pairs
allow at most two cubics. Increasing p improves both CR
and FLAT-CR, so use these minimum p values.

At m=k^2+k+1 the FLAT-CR expressions for (t,p)=(2,2)
and (3,3), denoted L_2,L_3, respectively satisfy

```
4 L_2(k)=k^4-2k^3-25k^2-18k+8,
4 L_2(7+x)=[372,710,227,26,1];
4 L_3(k)=k^4-2k^3-35k^2-24k+12,
4 L_3(8+x)=[652,1080,301,30,1].
```

The arrays again list increasing powers. Their coefficients
are positive. The m-slopes are C(k,2)-5 and C(k,2)-6,
positive on these ranges. Thus t=2 is proved for k>=7,
and t=3 for k>=8. For t=3 and k=4,5,6,7 the CR values
at the pair-packing lower bound are 12,36,60,75, with
positive m-slope. k<=3 is H3-CORE3.

For t=2 the only remaining cardinalities are

| k | CR with p=2 | Pair-packing minimum | Unpaid m |
|---:|---|---:|---|
| 4 | 9m-194 | 21 | 21 |
| 5 | 11m-353 | 31 | 31,32 |
| 6 | 13m-594 | 43 | 43,44,45 |

If p>=3, CR at the pair-packing minimum for k=4,5,6
has slack at least 69,116,167 respectively, and is
increasing with m. Thus only p=2 remains. At p=2 the two
possible cubic faces are {x_i^3,x_j^3} and
{x_i^3,x_i^2 x_j}, i!=j. This follows by inspecting the
two pair divisors: either they are two loops, or one loop
and its incident ordinary edge. The exact finite base is

| k,m | Full-pair sorted bases | Injective (base,face) | Phases | Min S |
|---|---:|---:|---:|---:|
| 4,21 | 10 | 24 | 504 | 147 |
| 5,31 | 60 | 120 | 3720 | 420 |
| 5,32 | 0 | 0 | 0 | -- |
| 6,43 | 0 | 0 | 0 | -- |
| 6,44 | 0 | 0 | 0 | -- |
| 6,45 | 0 | 0 | 0 | -- |

`two_cubic45.py` enumerates all sorted bases and both
face types, then every phase, with actual maximality.
`two_cubic6.c` enumerates every full quadratic labeling
by adding unit residues in increasing order, rejecting
a prefix exactly when two present cells at degree <=2
collide. An injective full labeling cannot have such a
prefix, so the pruning is exact. It finds no full-pair
bases for m=43,44,45. The set-based independent Python
enumerator `pair6_independent.py` reproduces the absence
and the prefix-node counts 39934,34054,58510. Thus all
finite bases are complete and the theorem follows. QED.

The identities and the four small positive CR values are
independently checked in `few_poly.py`. The direct k=5
base is also reproduced by `frontier_two5.py`, written
as an adversarial search before the uniform theorem.

There is one further small finite exclusion. If k=4,
Q is complete and t=4, then p>=3. At p>=4, CR at m=21
has slack at least 23. At p=3 all four cubics are a
full binary face: three pair divisors permit four cubes
only with two loops and their connecting edge. In this
case `R(m)=13m-316`, proving m>=25, while PAIR-PACK
excludes m<21. `frontier_search.py` enumerates all full
pair bases and all six binary faces for m=21,...,24:
the pair-base counts are 10,0,110,60 and there are zero
injective binary cubic extensions. Thus this k=4,t=4
case is excluded as well, for every spike count.

## 8. Checks and preserved failures

The sources and logs distinguish proved assertions from
bounded verification. In particular the polynomial
identities and shifted coefficients prove uniform theorems;
their independent evaluation at k=3,...,200 is a check,
not the range of those theorems.

`packing_checks.py`, seed 2026101991, uses 1200 fresh
random core proposals, explicit core/spike tiles E47/E51,
the two core-three minimum examples, a small failed
quadratic-packing extension, and base-four integer B3
examples with k=3,6,10,16,20. The latter include complete,
cubic-defective, pair-defective, one-cubic and few-cubic faces. Every retained
core is a down-set with injective labels, and its missing
residues are completed by actual spikes. At m<=500 it
checks every phase. At larger m MIN-PHASE reduces the
all-phase minimum to the finitely many phases where a
non-maximal core cell has residue zero.

The checked statements include HYBRID-ID, S>=FLAT-CR,
S>=CR, both SHADOW-DEF bounds, SHADOW-COVER at computed
minimum covers, literal distinctness of all counted
ROW-PACK labels, ROW-DEF, and the conclusions of DENSE9,
DENSE075 and the few/one-cubic criteria when applicable.
There are 1228 actual core/spike tiles, 1207 of height
exactly three, and 119462 direct phase evaluations.
Seventeen large-modulus cases use the proved MIN-PHASE
reduction. The checks include 1117 ROW-PACK label sets,
374 of them at moduli divisible by three, 613 exact
SHADOW-COVER minimum covers, ten DENSE9 instances, seven
DENSE075 instances, six one-cubic cases and two cases
in the k>=19 FEW-CUBICS range. CR pays 1224 tiles and
FLAT-CR pays 783; these counts overlap. Two deliberately
included k>=4,d>=6 examples fail BOTH scalar criteria
and remain positive by direct phase calculation, as
described below. All checked statements pass. Complete
data and the audit are retained in `b/`.

**Preserved false extension F1: PAIR-PACK without a complete
quadratic face.** It is false already at height three with

```
k=2, m=6, P=(1,4),
C={0,x,y,x^2,xy,x^3}.
```

The six residues are 0,1,4,2,5,3. The pair y^2 is absent;
its residue 2 equals that of x^2. Thus the claimed bound
`m>=k^2+k+1=7` fails. The core is already a tile and does
not violate MaxCL. This is smallest m for a genuine
height-three core with at least two non-maximal unit
directions: the origin, two units, at least two pairs and
a cubic are required. The complete-face hypothesis is
therefore retained in PAIR-PACK, and RETAINED-PACK only
uses subsets on which it holds.

**Preserved F2: CR alone for all injective height-three
cores with d>=6.** The lead's example, independently
rechecked here, has k=3, all six pairs, T={x_1^3},
m=14,s=3,P=(1,4,6). CR is -6 and actual minimum slack
is 43. FLAT-CR is also negative there;
H3-CORE3 pays it by its exact finite base. No assertion
that CR and FLAT-CR exhaust all actual tiles is made.

**Preserved F3: CR or FLAT-CR always pays at k>=4,d>=6.**
The smallest-modulus counterexample in this stated class is

```
k=4, m=16, P=(1,4,6,9),
Q=all ten pairs except x_2*x_3 and x_4^2,
T={x_1^3}, s=2, d=6, p=1.
```

Its fourteen core residues are distinct; the two spikes
occupy residues 11 and 14. CR=-2, FLAT-CR=-33, and the
exact minimum S is 78 at sigma=0. `adversary_min.py`
checks every phase. Its minimizing phase has zero pair
carries, so PAIR-ZERO also explains its positive slack.
The flat t=0 case has nonnegative FLAT-CR. For t>=1,
the same program proves minimality for this
failure by checking all 405 elementary count profiles
with m<=15, k>=4,d>=6, using only q<=Q_k, 2q>=k,
1<=p<=q, and p<=3t<=(k+2)p. Every such relaxed profile
has nonnegative CR, so an actual failure cannot have
smaller modulus. This core has a non-complete quadratic
face; it shows why the full-face hypothesis in the
sparse-cubic theorems is substantive.

A larger example has genuinely mixed carry payment:

```
k=5, m=31, P=(1,3,8,12,18), Q=all 15 pairs,
T={x_5^3,x_4*x_5^2}, s=8, d=13, p=2.
```

CR=-12 and FLAT-CR=-83, while the exact minimum S is
473, at sigma=30, rho_0=1. PAIR-ZERO and CENTERED-PAIR
both fail at that phase. This is a counterexample to
the proposed exhaustion by the two scalar bounds, not
to MaxCL. It is now covered by the finite TWO-CUBICS
base inside THREE-CUBICS. `frontier_two5.json` retains
the entire core and the phase data. Its full search has
120 injections and 3720 phases at m=31, and no full-pair
bases at m=32.

**Preserved F4: CR already pays the k=4,t=p=2 case at
the pair-packing minimum.** This intermediate table
claim was false: `R(21)=9*21-194=-5`. An actual example
is P=(2,7,8,11), all ten pairs, and two pure cubes at
the directions of residues 2 and 11, m=21. The true
minimum S is 147. The pair-packing lower bound makes
m=21 the smallest possible modulus for this fixed
profile. The error was caught by the exact small-table
check; the extra base is included explicitly in the
proof of THREE-CUBICS above. No accepted P6 theorem
used that incorrect intermediate table entry.

The accepted P6 failures (dropping Lplus, the two-lift
no-carry assertion, and forced-only cover payment) remain
in that report and are not discarded by these arguments.
No actual counterexample to MaxCL or Wilf was found.

## 9. Exact remaining gap and formalization targets

For a hypothetical height-three MaxCL counterexample,
use the P6 reductions and MIN-PHASE, delete spikes to
obtain the core, and retain the same modulus and phase.
In addition to every P6 necessary carry/boundary condition,
the remaining family necessarily has

```
d>=6, k>=4, t>=1,
m=1+k+q+t+s, s>=0, J>B,
R(m)<0 and F_flat(m)<0,
epsilon=U_k-t > floor(3k^2/40),
m <= ceil(A_CR/(J-B))-1,
k*(Q_k-p)<=3epsilon,
k*(Q_k-p)-C(Q_k-p,2)<=epsilon.
```

Every retained complete quadratic face I supplies the
additional modulus lower bounds ROW-PACK and ROW-DEF.
The missing-pair graph has a minimum cover of size at
most floor(epsilon/k) by SHADOW-COVER. These bounds are
all for the original cyclic group. In particular any
lower bound M_I must fit below the CR threshold.

If Q is complete, further necessary conditions are

```
t>=4, epsilon>floor(k^2/9),
if k=4 then t>=5,
if k>=19 then t>floor(k^2/16).
```

The family remains unbounded in k. Neither a full proof
nor a reduction of this family to one finite computation
has been obtained. The semigroup conclusion still follows
only for the proved structural classes, at sigma=c mod m;
the existing e<=6 height-three corollary remains unchanged.
More explicitly, take the minimum-degree grlex factorization
tile of an Apéry set whose elements have some factorization
of length <=3, remove its maximal unit directions, and test
the resulting core against H3-CORE3, DENSE9, DENSE075,
THREE-CUBICS, FEW-CUBICS, CR or FLAT-CR. Any qualifying
core gives MaxCL at every phase and hence Wilf. This is
the exact translation of all the new structural results;
no assertion about every Apéry factorization is required.

Strategic assessment. Paying maximal pairs by the flat
window removes precisely the obstruction to pure CR in
near-flat cores. Signed packing on successor-complete
rows pays the opposite, dense cubic end, including
localized missing pairs. The surviving middle can have
many present cubics but no large successor-complete
retained face, and the crude lower sum of N2 residues can
lose their actual spread. The next precise target is a
payment for those incomplete successor rows in MIN-COVER,
or a lower bound for the residue sum of their quadratic
shadow that strengthens the independent lower sum C(p,2).
It must use residue distribution, not just extend the
dimension of the finite certificate. The unrestricted
core enumeration stops at k=3; the higher-dimensional
pair-base loops are bounded bases of THREE-CUBICS, not
enumerations of all those cores. The unbounded results
come from the two packing payments.

For an exact next lemma with all numerical terms fixed,
use the full spike-completed quadratic face, its cubic
residue set R_T, and its isolated unit set I_sp. For a
phase, put

```
F_empty=(d+3)sum_{R_T}r +(d+2)sum_Q r
                              +(d+1)sum_{I_sp}r.
```

A feasible pair container U is a subset of Q such that
each residue in R_T has an eligible cubic whose distinct
pair divisors all lie in U. The remaining payment lemma
is, precisely for the residual family displayed above,

```
(d+2) min_{U feasible} sum_U r
                   >= F_empty-(d+1)m(m-1)/2.    (B-COVER)
```

The accepted CONTAINER equivalence makes B-COVER sufficient
and necessary. ROW-PACK settles its dense-successor end
by forcing the modulus past CR, while the flat window
settles the sparse-cubic end. Extending the signed-label
injection to incomplete rows must retain their actual
pair weights in B-COVER; a claim of exhaustion by the two
scalar rearrangements is already refuted by F3.

A first local version is **SINGLE-COVER**, B-COVER with
one cubic residue and arbitrary Q. If O is its set of
eligible cubics, the minimum feasible-container weight
is exactly `min_{y in O} sum_{z in P(y)}r(z)`, since
extra pair weights are nonnegative. Thus the next
specific local lemma is

```
(d+2) min_{y in O} sum_{z in P(y)}r(z)
                  >= F_empty-(d+1)m(m-1)/2
```

for all height-three, one-cubic-residue faces, without
assuming Q complete. ONE-CUBIC proves this when Q is
complete; H3-CORE3 proves it at k<=3. The explicit
m=16 face in F3 is a small actual stress case for the
remaining k>=4, defective-Q version. SINGLE-COVER is
an open next target, not an input to any theorem here.

Formalization statements with elementary finite proofs:

- `pair_pack`: injection of off-diagonal differences from
  a complete two-skeleton;
- `row_pack`: injection of reduced signed labels from
  successor-complete quadratic rows, including the zero
  padding case;
- `row_defect_bound`: union bound with weights h,2h-1,3h-3;
- `quadratic_defect_incidence` and
  `quadratic_defect_bonferroni`: the two SHADOW-DEF counts;
- `maxCLPhase_of_cr` and its linear m-slope J-B>0;
- `hybrid_pair_window_identity`, `maxCLPhase_of_flat_cr`;
- the four explicit shifted-polynomial identities and
  endpoint concavity proofs for DENSE9 and DENSE075;
- the CORE3 table, together with separate finite checks
  of its three canonical base loops;
- the ONE-CUBIC k=4 finite base and the two FEW-POLY
  factorizations.
- the two shifted fourth-degree polynomials for t=2,3,
  and the explicitly bounded THREE-CUBICS finite bases.

SHADOW-COVER also has a finite combinatorial statement,
but its supplied proof uses regular sequences and the
Koszul complex; importing that algebraic proof into Lean
is additional work. None of the new finite assertions
has been claimed to be kernel-checked.

## 10. Reproduction

All sources below are in this repository's `b/` directory
and on fejer under `~/wilf/p6b`. Standard C and exact Python
Fractions suffice; numpy/scipy and sympy are not needed.
Commands, executed on fejer, are:

```sh
cd ~/wilf/p6b
nice -n 10 gcc -O3 -Wall -Wextra core3.c -o core3
nice -n 10 ./core3 > core3.log
nice -n 10 ~/mathenv/bin/python shape3.py > shape3.log
nice -n 10 ~/mathenv/bin/python core3_independent.py > core3_independent.log
nice -n 10 ~/mathenv/bin/python dense_poly.py > dense_poly.log
nice -n 10 ~/mathenv/bin/python generic_density.py > generic_density.log
nice -n 10 ~/mathenv/bin/python certificate_tables.py > certificate_tables.log
nice -n 10 gcc -O3 -Wall -Wextra one_cubic4.c -o one_cubic4
nice -n 10 ./one_cubic4 > one_cubic4.log
nice -n 10 ~/mathenv/bin/python one_cubic4_independent.py > one_cubic4_independent.log
nice -n 10 ~/mathenv/bin/python few_poly.py > few_poly.log
nice -n 10 ~/mathenv/bin/python two_cubic45.py > two_cubic45.log
nice -n 10 gcc -O3 -Wall -Wextra two_cubic6.c -o two_cubic6
nice -n 10 ./two_cubic6 > two_cubic6.log
nice -n 10 ~/mathenv/bin/python pair6_independent.py > pair6_independent.log
nice -n 10 gcc -O3 -Wall -Wextra shadow_cover.c -o shadow_cover
nice -n 10 ./shadow_cover > shadow_cover.log
nice -n 10 ~/mathenv/bin/python packing_checks.py 2026101991 1200 > packing_checks.log
nice -n 10 ~/mathenv/bin/python frontier_search.py > frontier_search.log
nice -n 10 ~/mathenv/bin/python frontier_two5.py > frontier_two5.log
nice -n 10 ~/mathenv/bin/python adversary_min.py > adversary_min.log
nice -n 10 ~/mathenv/bin/python audit_p6b.py P6B_REPORT.md > audit.log
```

The final audit records parameter ranges, cross-checks,
the source/data digests and any concrete unpaid example.
It does not substitute audit success for the mathematical
arguments or claim a proof of the remaining family.
