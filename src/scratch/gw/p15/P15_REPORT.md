# P15: Lemma U, T1-DOWN, TAIL and true-shift T1 are false

2026-10-19 local / 2026-10-20 UTC. **COUNTEREXAMPLES and PROVED
replacement bounds.** Computation is exclusively on fejer,
`~/wilf/p15/`, under nice, with at most four single-core jobs.
Earlier reports and lead files are unchanged. No commits.

The smallest modulus certified here for Lemma U in dimensions two
and three is **13**. A numerical-semigroup counterexample to T1 at
the true shift is

    S=<13,22,23,50,51,60>, p*=5,
    sum_Ap K_p*=8 > m-e=7.

This is **not** a Wilf counterexample: W=39. The asserted bound
`W>=e-h+Lambda` fails by one. Lemma U already fails on an injective
two-dimensional ideal; making the residue map bijective, or requiring
an actual unique-factorization Apéry tile, does not save it. The
unbounded families below show that the issue is not an isolated
one-unit error. The bare GEN-EH bound `W>=e-h` is not refuted here.

## 1. Exact target, definitions, and the first obstruction

Fix integers `m>=2`, `d>=1`, `1<=r_a<m`, `1<=p<=m`. For y>=0,

    C(y)=floor((y-p)/m)+1.

Let D be a finite coordinate order ideal in N^d. For f in D define

    R(f)=sum_a f_a*r_a,
    K(f)=C(R(f))-sum_(a:f_a>0) f_a[C(R(f))-C(R(f)-r_a)],
    dec(D)={f in D: |f|>=2},
    Exc(D)=sum_D K-|dec(D)|.

The factors with f_a=0 are omitted; no negative argument of C is
needed. Lemma U asserts Exc(D)<=0 when R modulo m is injective.
Injectivity implies |D|<=m but does not force Exc(D)<=0.

**Frontier review.** KNOWN: the one-dimensional pairing and the
lex-factorization reduction are valid. GAP AT START: prove or refute
the higher-dimensional count inequality. DISCRIMINATING EXAMPLE:
several cubic monomials can have C=2 and all pair faces C=2,
so each cubic has K=2, while the pair faces have K=0. A binary
full cubic simplex has four such cubics and only three pair credits.
The residue map can be injective despite this imbalance.

**Strategic decision after falsification.** Stop trying to prove
Lemma U or T1 as stated. Preserve exact counterexamples, establish
the size of the unavoidable error, check the reduction independently,
and prove the sharp height-three replacement. No experiment below
is offered as a proof of an unbounded conjecture.

## 2. Smallest certified two-dimensional counterexample

**COUNTEREXAMPLE.** Take

    m=13, r=(9,10), p=5,
    D={(i,j): i+j<=3}.

The complete calculation is:

| Degree | R-values | Residues modulo 13 | C-values | K-values |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 1 | 9,10 | 9,10 | 1,1 | 0,0 |
| 2 | 18,19,20 | 5,6,7 | 2,2,2 | 0,0,0 |
| 3 | 27,28,29,30 | 1,2,3,4 | 2,2,2,2 | 2,2,2,2 |

All ten residues are distinct. The set is an order ideal, its seven
decomposables are the three pairs and four cubics, and

    sum_D K=8, |dec(D)|=7, Exc(D)=1.

Every proper coordinate subideal satisfies the proposed inequality
for this same r,m,p. Indeed if q is its pair count and t its cubic
count, its excess is t-q. For q=0,1,2, the possible binary cubics
supported by those pairs number at most q. If q=3, a proper
subideal has t<=3. Thus this is an inclusion-minimal failure.

`exhaust2.c` enumerates every partition shape of every size <=m,
all r_1<=r_2 in [1,m-1], and all p. Coordinate permutation covers
the omitted residue order. For all m<=12 it finds no failure; at
m=13 the displayed shape and shift are the only failure in that
symmetry-reduced enumeration. Since every injective ideal has
size <=m, this is a complete finite certificate of minimal modulus
**in dimension two**, not a random-search minimality claim.
The independent dimension-three enumeration likewise excludes
m<=12. No global minimality across all dimensions is asserted.

The first discovered, slightly larger example is retained:

    m=14, r=(8,9), p=2, D={(i,j):i+j<=3}.

Its residue levels are `0; 8,9; 2,3,4; 10,11,12,13`, and the
same C and K table applies. It also has excess one.

Failures with every requested active dimension d=2,...,6 are
explicit. At m=13 append to the binary ideal one unit spike
of residue 8 (d=3), then one of residue 11 (d=4), then one
of residue 12 (d=5). At m=14 use r=(8,9) on the binary
core and append four unit spikes of residues 1,5,6,7 (d=6).
These are unused residues, so injectivity is preserved. A
unit spike has K=0 and is not decomposable, so the excess
remains one. The d=5 and d=6 versions are residue-complete.
`verify_ideals.py` checks these directly at every shift with
literal counts. No minimal-modulus claim for d>=4 is made.

## 3. An actual semigroup counterexample at the true shift

**COUNTEREXAMPLE TO T1, T1-DOWN AND TAIL.** Let

    S=<13,22,23,50,51,60>.

Its Apéry set by residue 0,...,12 is

    [0,66,67,68,69,44,45,46,60,22,23,50,51].

All minimal generators and all factorizations of Apéry elements are
accounted for as follows. The binary monomials of degree at most
three in 22,23 give ten values with distinct residues, as in Section
2. The additional values 50,51,60 occupy the three missing residues
11,12,8. A product of four binary generators is at least 88>69;
an extra generator plus any non-m generator is at least 72>69.
Thus these thirteen values are the only possible non-m factorizations
of values <=69. Their residues are distinct and complete, so no
smaller representative of any residue can lie in S: removing any
m's from a purported smaller representation would produce a second
listed representative. This proves the displayed Apéry set.
The same reasoning proves minimality of all six generators and
uniqueness of every Apéry factorization. Consecutive generators
22 and 23 ensure gcd one. Multiplicity is 13.

Consequently, exactly,

    m=13, d=5, e=6, M=69=5m+4, q=5, p*=5,
    c=57, h=c-4m=5, rho=5m-c=8,
    ell=16, genus=41, Lambda=39, W=39.

At p*=5, the two binary units have C=2; their pairs have C=4;
the four binary cubics have C=5. It follows that each pair has
K=0 and each cubic has K=2. Zero and all primitive values have
K=0. In residue order the complete K-vector is

    [0,2,2,2,2,0,0,0,0,0,0,0,0].

Thus sum K=8>7=m-e, at the true shift, not just an auxiliary one.
The K identity checks exactly:

    W=rho+Lambda-sum K=8+39-8=39,
    e-h+Lambda=6-5+39=40.

For an independent direct calculation of Lambda, each of the two
binary directions has top-credit sum two, from the singleton
values 50 and 51. Directions 50 and 51 each have top-credit
sum `ell-(5-1)=12`; their only non-singleton chain is their
origin chain. Direction 60 has sum `ell-5=11`. Therefore
Lambda=2+2+12+12+11=39.

### 3.1 TAIL data, without a matching computation

The nonzero J-coefficients are -3 at each of
`22,23,44,45,46`, and +2 at each of `66,67,68,69`.
The other nonzero Apéry values have J=0. The origin has J=-6.
Therefore the full p=5 sampling beyond m is

| z | 18 | 31 | 44 | 57 |
|---|---:|---:|---:|---:|
| Q(z) | 7 | 1 | 1 | -8 |

Its sum is one. There are no later nonzero terms, since the
next sample is 70>M. TAIL fails at y=18>m. In this example
the failure is already the whole sampled tail beyond m; no
claim about monotonicity is involved.

### 3.2 Full data for the first witnesses

The first true-shift T1 counterexample found was

    <14,22,23,61,62,63,71>,
    Ap=[0,71,44,45,46,61,62,63,22,23,66,67,68,69],
    M=71, p*=2, c=58, ell=14, Lambda=36, e=7, W=40,
    sum K=8>m-e=7.

The old E47 generator list `<14,22,23,57,61,62,63>` also fails
T1 at p=1,2, with M=69 and true shift 14. It is not a true-shift
failure. The lower-genus version `<14,22,23,48,49,57,61>` has
genus 41 and the same auxiliary-shift failure. These discovered
witnesses are retained, rather than overwritten by the smaller
modulus example.

`case13_C.log`, `case14true_C.log`, `first_check.log`,
`first_independent.log` and `semigroup_checks.json` contain
independent recomputations and full data. None is a Wilf
counterexample. The claim of minimality in Section 2 concerns
Lemma U and modulus in dimensions two/three only; genus 41
or this semigroup's generator list is not claimed globally minimal.

## 4. T1-DOWN fails even in embedding dimension three

**COUNTEREXAMPLE, including at the true shift.** For

    S=<14,22,23>,
    Ap=[0,113,44,45,46,89,90,91,22,23,66,67,68,69],
    M=113, p*=2, c=100, ell=47, genus=53, Lambda=37, W=41,

take the semigroup-order down-set

    D0={0,22,23,44,45,46,66,67,68,69}.

Each listed value is Apéry and has a unique binary factorization
of degree <=3; every divisor in the S-order has a subfactorization
and therefore stays in D0. Its three pairs have K=0 and its
four cubics have K=2, giving sum_D0 K=8>7 decomposables.
Moreover 3e=9<m=14. This refutes the hereditary conjecture
even for e=3 in the sparse regime.

The matching obstruction is exact. The four cubic deficits have
capacity one each. The only decomposable credits below them are
the three pairs, each of capacity one. Their entire lower-poset
neighborhood has capacity three, so full below-poset matching
fails, not merely cover-only matching. Primitive credits are
not admissible in T1-DOWN.

The full Apéry sum is nevertheless eight, below m-e=11:
the three quartics 89,90,91 have K=-1 and the quintic 113 has
K=3, so their total addition to the sum is zero. Thus this
example refutes T1-DOWN and does not refute global T1 for e=3.
The credits needed for a global statement cannot in general
be required to lie below each deficit.

## 5. Fixed dimension two: unbounded errors and true-shift realizations

### 5.1 An injective binary family (PROVED COUNTEREXAMPLE FAMILY)

For every integer H>=3 put

    L=H+4,
    m=(H-1)L+3=H^2+3H-1,
    r=m-L, s=r+1, p=2,
    D_H={(i,j):i+j<=H}, N=|D_H|=(H+1)(H+2)/2.

Then R is injective modulo m, but

    Exc(D_H)=C(H-1,2).                            (U-H)

In particular no dimension-dependent O(1) error repairs Lemma U
in dimension two when height is unrestricted.

**Proof.** For degree k write j for the exponent of s, so
`R=k*m-k*L+j`, `0<=j<=k`. For 1<=k<=H-1,
`0<kL-j<m`, and the residue interval is

    I_k=[m-kL,m-kL+k].

These intervals are pairwise disjoint, since L>H. Their lowest
start is three. For k=H, `m<HL-j<2m`, and the residues form

    I_H=[2m-HL,2m-HL+H].

This interval starts two above the largest element of I_1 and
ends at m-1. It is disjoint from all I_k and zero. This proves
injectivity. At p=2, C(R)=k for k<=H-1 and C(R)=H-1 at
degree H. Therefore K=0 at all degrees below H, and K=H-1
at each of the H+1 top monomials. Hence

    sum K=H^2-1,
    |dec|=N-3,
    sum K-(N-3)=(H-1)(H-2)/2.

All r,s belong to [1,m-1]. This checks every hypothesis. QED.

There is also an arbitrary-density version. For fixed H>=3,
take any `L>=H+4`, `m=(H-1)L+3`, and the same definitions
of r,s,p and D_H. Every calculation above still holds;
only the assertion that I_H ends at m-1 changes to the
inequality that it ends at most m-1. Thus the same positive
excess occurs with |D_H|/m arbitrarily small. For instance
letting L grow faster than H gives unbounded excess and
vanishing density simultaneously. These counterexamples
do not require near-saturation of the residue capacity.

The same values of C occur at p=1, but p=2 permits the following
true-shift realization.

### 5.2 Actual true-shift T1 failures with unbounded excess (PROVED)

In this subsection return to `L=H+4` and
`m=H^2+3H-1`, as originally fixed in Section 5.1. Put

    n=2m-L,
    c=(2H-2)m+2, M=(2H-1)m+1,
    S_H=<m,n,n+1> union [c,infinity).

Then its Apéry set is the full binary height-H simplex plus
one primitive tail value for each unused residue. Write
`eta=m-N`. Its exact parameters are

    q=2H-1, p*=2, h=2,
    e=eta+3=N=(m+3)/2,
    ell=H(H+1)(2H+1)/6,
    Lambda=eta*(ell-q),
    sum_Ap K=H^2-1,
    sum_Ap K-(m-e)=C(H-1,2)>0.                    (T1-H)

**Proof of realization.** The core monomials have the distinct
residues proved in Section 5.1. Their largest value is
`H(n+1)=(2H-1)m-1=M-2`. The smallest degree-(H+1) value
exceeds M, since

    (H+1)n-M=(2H-4)L+8>0.

Thus no additional core monomial can enter below M. Adding the
tail is semigroup closure, and any tail element plus any nonzero
semigroup element exceeds M. A tail representative in an unused
core residue is consequently primitive; one in a used residue
is the core representative plus a nonnegative multiple of m.
There are eta unused residues. Residue one is unused, so M
itself is a primitive tail value and the conductor is exactly c.
Every Apéry factorization is unique. All minimal generators are
the displayed three and the eta tail representatives. Gcd one
follows from consecutive n,n+1.

At p*=2 adding jm to a core value of degree j cancels in K,
so the full sum is the sum in Section 5.1; primitive tail values
have K=0. The identity `m=2N-3` proves e=N. Co-levels at core
degrees j<H are `q-2j`; degree H and all tail values have
co-level zero. Summing gives the displayed ell. Every core
direction has all chain tops at degree H or at a primitive
tail value, hence top-credit zero. A tail direction contributes
`ell-q`, proving the Lambda formula. QED.

These are not Wilf counterexamples. In fact

    W=N*(ell-4H+4)+6H-8>0,

because `ell-4H+4>=6` for H>=3 (equality at H=3 and the
increment is `(H+1)^2-4>0`). Also 2e=m+3, so the family lies
in a previously covered dense-embedding regime. No external
theorem is needed for its positive Wilf calculation.

### 5.3 Sparse hereditary realization (PROVED)

Omit the tail and consider `<m,n,n+1>` alone. The height-H
core remains an Apéry down-set: a smaller same-residue
representative would have a non-m factorization of degree
at most H, contradicting core injectivity. Its factorization
is unique for the same reason. A divisor in S of a core value
has a subfactorization of that unique factorization.
Therefore T1-DOWN at p=2 fails there by C(H-1,2), in embedding
dimension three, with 3e<m for every H>=3. This statement does
not assert that p=2 is the true shift of the untruncated semigroup.

## 6. Height-three counterexamples at fixed depth five

### 6.1 A family starting at the smallest modulus (PROVED)

For t>=4 put

    m=3t+1, r=2t+1, s=2t+2, p=t+1,
    D={(i,j):i+j<=3}.

The residue layers are

    0; 2t+1,2t+2; t+1,t+2,t+3; 1,2,3,4.

They are pairwise disjoint. Their C-layers are 0,1,2,2,
so the same elementary calculation gives Exc(D)=1. This
includes m=13 at t=4.

The actual semigroups

    S_t=<3t+1,5t+2,5t+3> union [13t+5,infinity)

have, exactly,

    c=13t+5, M=16t+5, q=5, p*=t+1,
    eta=3t-9, e=3t-6, ell=14,
    Lambda=9eta, W=29t-89>0,
    sum K=8>m-e=7.

To verify the Apéry description, its ten core values have
distinct residues as above, its largest is `15t+9<=M`, and
the smallest quartic `20t+8` exceeds M. Fill unused residues
with conductor-aligned tail representatives, which are primitive
because adding any nonzero element takes them past M. For t>4
the residue t of M is unused; at t=4, M is the cubic 3(5t+3).
Either way max Ap is exactly M. The C-layers at p* on actual
core values are 0,2,4,5, so the K-vector is unchanged. Core
co-levels are 5,3,1,0 and tail co-levels zero, proving ell=14
and the displayed Lambda and W.

TAIL also fails throughout this fixed-depth family. The four
nonzero sampled Q-values beyond m, at

    z=4t+2, 7t+3, 10t+4, 13t+5,

are `7,1,1,-8`, whose sum is one.

### 6.2 Unbounded error even at height three (PROVED)

Let Y be an integer B3 set of k>=2 nonnegative integers,
containing zero, with maximum T. Here B3 means all unordered
triples, repetitions permitted, have distinct sums. Such sets
exist for every k: use zero and distinct powers of four; no
carry occurs with at most three summands. Set

    N=C(k+3,3), Q=C(k+1,2), U=C(k+2,3),
    m a multiple of eight with m>max(24T+6,2N+1),
    r_i=m/2+1+4Y_i, p=2,
    D={f in N^k:|f|<=3}.

The residue map is injective. Distinct degrees 0,1,2,3 have
different residues modulo four. Within each degree, padding
with zeros reduces injectivity to B3. The degree-two residues
are `2+4(Y_i+Y_j)`; the degree-three residues are
`m/2+3+4(Y_i+Y_j+Y_l)<m`. All are nonzero, and residue one
is unused. C=1 on units and C=2 on pairs and cubics, hence

    Exc(D)=U-Q=C(k+1,3).                          (U3-SHARP)

The semigroup

    S=<m,m+r_i> union [4m+2,infinity)

has exactly the full cubic core plus eta=m-N primitive tail
values in its Apéry set. Its conductor and maximum are
`c=4m+2`, `M=5m+1`; residue one is unused by the core, so
M is a primitive tail value. Four core generators exceed M.
The realization argument is identical to Section 5.2. Thus

    q=5, p*=2, e=m-Q-U,
    ell=5+3k+Q, Lambda=eta*(3k+Q),
    sum K=2U, sum K-(m-e)=C(k+1,3).

The T1 error is unbounded even at depth five with a height-three
unique-factorization Apéry tile. Its Wilf number is positive:
`W=m-2+Lambda-2U>0`, since m>2N+1. Again no Wilf
counterexample is claimed.

For completeness, its sampled Q-values at p*=2, beyond m,
are `Q+U, U-Q, U-Q, -2U`; their sum is U-Q. This is an
unbounded family of TAIL failures at the true shift as well.

## 7. Sharp positive replacement at height three

The following bounds use no injectivity, no gcd assumption,
no completeness of residues and no external theorem.

### 7.1 Pointwise classification (PROVED)

For every ideal of height at most three,

1. zero and units have K=0;
2. pairs have K<=1;
3. cubics have K<=2;
4. a cubic has K=2 exactly when its C-value and every pair
   face's C-value are two. All its factor units then have C=1,
   and each pair face has K=0.

For pairs, `K=C(u)+C(v)-C(u+v)<=1`, including repeated
factors, by the elementary floor inequality. For a cubic,
if C(R)<=1 then K<=1. If C(R)=3, each face has C<=2,
so all three factor copies contribute a drop at least one
and K<=0. The remaining possibility is C(R)=2; equality
K=2 holds exactly when all the drops vanish. A pair with
C=2 has value >=m+p. Neither factor can be below p,
since the other factor is <m. Thus both factors have C=1,
and the pair formula gives K=0. This proves every assertion.

### 7.2 Graph payment and sharp error (PROVED)

Let beta count the K=2 cubics and P their distinct pair
monomials; let k be the number of directions appearing in
these cubics. Regard P as a loop graph G on these k directions.
Then

    Exc(D)<=beta-|P|<=C(k+1,3).                  (U3-ERR)

The first inequality counts one deficit at every K=2 cubic
and a distinct unit of credit at each pair face, using Section
7.1. Every other decomposable has K<=1. For the second,
let T_G count all cubic monomials whose pair divisors are
edges of G. Then beta<=T_G. Add each missing loop to G:
it creates at least its pure cubic, so T_G-|E| cannot decrease.
After all loops are present, adding a missing nonloop edge
creates both corresponding repeated-factor cubics, so again
T_G-|E| cannot decrease. Complete the graph. Its difference is

    C(k+2,3)-C(k+1,2)=C(k+1,3).

This proves U3-ERR by an elementary completion argument.
Section 6.2 gives injective examples attaining equality for
every k>=2; the constant is sharp even under injectivity.

Two useful zero-error subclasses follow.

**U3-PSEUDO.** If every component of G has at most as many
edges as vertices, counting a loop once, then Lemma U holds.
A tree has no legal cubic. A component with one ordinary
triangle has at most one; a longer cycle has none. A component
with a loop at v has at most the pure cube and one repeated-
factor cubic per edge incident to v, at most its edge count.
Thus beta<=|E|. This is the elementary P14 graph argument,
applied here to all K=2 cubics without a high/low partition.

**U3-SQ5.** If all the K=2 cubics are squarefree and use
at most five directions, Lemma U holds. Their pair graph
is loopless. Each edge belongs to at most k-2 possible
triangles, so `3beta<=(k-2)|P|<=3|P|`.
In particular every squarefree height-three ideal in at most
five variables satisfies Lemma U, even without injectivity.

The threshold five cannot be replaced by six: restrict the
B3 construction of Section 6.2 at k=6 to the squarefree
monomials of degree <=3. The 15 pairs have K=0 and the 20
cubics have K=2, so its excess is `40-(15+20)=5`. It is
still an injective order ideal, by restriction of the B3
ideal. `verify_ideals.py` checks the concrete choice
`m=1712`, `r=857+4Y`, `Y={0,1,4,13,32,71}` at every p.

These are positive infinite classes, not a restoration of
the false general lemma. The bound for squarefree critical
cubics need not apply when repeated-factor cubics occur,
as the binary counterexamples demonstrate.

## 8. Re-check of the reduction, and what survives

**PROVED: the lead's reduction itself is valid.** Choose the
lexicographically largest factorization f(x) of each Apéry
element over the non-m primitive generators. Factorizations
are finite in number. For a semigroup-order down-set E,
if g<=f(x), the value y represented by g is Apéry (otherwise
x-m would be in S) and belongs to E. Replacing g by a
lexicographically larger factorization of y would improve
f(x), so the chosen factorization of y is exactly g.
Thus f(E) is a coordinate order ideal and its residue map
is injective. These statements do not assume unique
factorization.

Write n_a=k_a*m+r_a. For a positive exponent f_a,
`C(x)=C(R(f))+sum f_a*k_a` and
`C(x)-C(x-n_a)=k_a+C(R(f))-C(R(f)-r_a)`.
The integer multiples of m cancel after multiplication
by f_a and summation. Finally nu_a(x)>=f_a and every
drop is nonnegative, so K_p(x)<=K(f(x)). Zero and
primitive values correspond precisely to degree zero/one.
This proves all steps of the conditional implication
`Lemma U => T1-DOWN => T1`.

The antecedent is false; the counterexamples do not expose
an algebra error in that implication. In Section 3 the
actual Apéry factorizations are unique, so the comparison
is an equality and the false U inequality is transferred
exactly to T1. Its factorization tile is the binary cubic
simplex plus three unit spikes, a complete injective tile
in dimension five. Thus neither bijectivity nor actual
semigroup realizability repairs the lemma.

The d=1 pairing remains valid at every height, without
injectivity. Ideals of height at most two also satisfy U
pointwise in every dimension, without injectivity. Section
7 gives further height-three subclasses. By the same
comparison, T1 holds at every p if a semigroup admits a
squarefree factorization tile of height at most three in
at most five non-m generator directions.

**Exact remaining question.** T1 at arbitrary shifts and at
the true shift is false; T1-DOWN and TAIL are false, even
with the additional hypotheses specified above. A proof
of T1 for e=3 or e=4 is not obtained here and is not ruled
out by the global T1 counterexamples. Its hereditary
version for e=3 is ruled out. The bare GEN-EH conjecture
and Wilf remain unrefuted. Any replacement intended to
imply them must permit positive K-sum excess and pay it,
for example from Lambda; injectivity alone and below-poset
matching cannot force the excess to vanish. Families U-H
and U3-SHARP quantify necessary errors for such a replacement.

The exact geometric obstruction is visible in Section 2:
four distinct cubic labels lie in [1,4], while their
three distinct pair labels lie in [5,7]. The threshold
p=5 therefore gives all cubic faces the same C-value as
the cubics. Additional unused residues may be filled by
primitive unit spikes, whose K is zero and which create
no decomposable credit. Injectivity and even completeness
of labels allow this configuration; they do not impose
the order of labels needed by the proposed inequality.

## 9. Computational record

**FINITE CHECK.** All runs were on fejer, `~/wilf/p15/`,
with `nice -n 10`, at most four single-core jobs, GCC
13.3.0 (Ubuntu) and `~/mathenv/bin/python` 3.12.3. No
external theorem or computer algebra package is needed
by the proofs in Sections 1--8. No commits were made.

### 9.1 Exact commands

The full command record is [COMMANDS.md](COMMANDS.md).
Each command below is run remotely, for example with

```sh
gcloud compute ssh fejer --zone us-east1-b --command 'cd ~/wilf/p15 && nice -n 10 ./exhaust2 2 16 >exhaust2.log'
```

The main invocations, after compilation with `nice -n 10
cc -O3` (and `-lm` for the annealer), were:

```sh
nice -n 10 ./exhaust2 2 16 >exhaust2.log
nice -n 10 ~/mathenv/bin/python shape3.py >shape3.log
nice -n 10 ./exhaust3 <shape3.txt >exhaust3.log
nice -n 10 ./ideal_search 10 60 3 1200 150015 >ideal_search.log
nice -n 10 ~/mathenv/bin/python semigroup_checks.py >semigroup_checks.log
nice -n 10 ~/mathenv/bin/python families.py >families.log
nice -n 10 ~/mathenv/bin/python verify_ideals.py >verify_ideals.log
nice -n 10 ~/mathenv/bin/python check_height3.py >check_height3.log
nice -n 10 ~/mathenv/bin/python audit.py >audit.log
```

`first_check.py` and `first_independent.c` independently
verify the initially found m=14 witnesses. `verify_case.c`
is a separate dense-Dijkstra/literal-count C verifier:

```sh
nice -n 10 ./verify_case <case13.txt >case13_C.log
nice -n 10 ./verify_case <case14true.txt >case14true_C.log
```

The same verifier was run on every `families/*.txt`
generator input, excluding the `_ap.txt` data files;
the exact shell loop is in COMMANDS.md. For m<=60 it
checks every shift; otherwise it checks the true shift.
It also verifies minimality of the supplied generators.

### 9.2 Complete small-dimensional enumerations

`exhaust2.c` enumerates every partition ideal of every size
1,...,m, every nondecreasing residue pair and every p.
`shape3.py` generates all decreasing stacks of partitions
of sizes 1,...,13, and `exhaust3.c` checks every applicable
m<=13, every nondecreasing residue triple and every p.
Coordinate permutations of the full shape lists justify
the residue-vector symmetry reduction. Inactive coordinates
are allowed. These are counts of symmetry-reduced inputs,
not claims of one representative per shape orbit.

| Domain | Injective (m,D,r) inputs | Shifts | Failing shifts |
|---|---:|---:|---:|
| d=2, 2<=m<=12 | 9,533 | 98,427 | 0 |
| d=2, m=13 | 6,366 | 82,758 | 1 |
| d=2, m=14 | 6,456 | 90,384 | 4 |
| d=2, m=15 | 9,162 | 137,430 | 1 |
| d=2, m=16 | 12,187 | 194,992 | 7 |
| d=3, 2<=m<=12 | 122,894 | 1,328,488 | 0 |
| d=3, m=13 | 123,696 | 1,608,048 | 17 |

The total d=2 run has 43,704 injective inputs and 603,991
shifts; the d=3 run has 246,590 inputs and 2,936,536
shifts. All failures in these runs have excess one and
the least failing size is ten. In d=3 the size-ten example
has an inactive coordinate; active three-dimensional
examples follow by the unit-spike construction in Section 2.
The plane-partition counts at sizes 1,...,13 are
`1,3,6,13,24,48,86,160,282,500,859,1479,2485`.
`audit.py` independently adds the raw counts and confirms
the zero-failure m<=12 prefixes. These finite certificates
justify the minimal-modulus statements in Section 2 only
for dimensions two and three.

### 9.3 Random/adversarial ideals

`ideal_search.c` uses xorshift seed 150015, all m=10,...,60
and d=2,...,6, three starts per pair and 1,200 mutation
iterations per start. Seeds are greedily grown injective
ideals and, where applicable, binary cubic cores with
unit spikes. Mutations change a residue, multiply all
residues by a unit, add an admissible corner, remove a
maximal cell, or swap a maximal cell with a corner. The
order-ideal and injectivity conditions are maintained.
The exact integer objective is the maximum excess over
every p, computed by residue events.

It tests 249,611 valid proposed states, with 706 positive-
excess events. These counts include repetitions. The
largest recorded excess is six at m=38, d=2, |D|=23,
r=(31,33), p=10; its height is six. Full point lists for
every record are retained in `ideal_search.log`. The
search missed the smaller m=13 example subsequently
found by exhaustive enumeration; no search minimality
claim is made.

`verify_ideals.py` independently reconstructs every recorded
search witness and the explicit d=2,...,6 examples, the
squarefree six-variable failure and three dilute height
examples. It uses literal integer counts at every p,
and explicitly checks the order ideal and residue map.
It verifies 16 input records and 3,263 shifts, including
repeated witnesses. Full rows are in `verified_ideals.json`.

### 9.4 Actual semigroups, TAIL, matching and the reduction

`semigroup_checks.py` uses heap Dijkstra, extracts actual
minimal generators, computes literal backward depths and
forward chain tops, and checks the K identity at the true
shift. At every p it also computes J and all sampled tail
suffixes beyond m, and uses capacitated bipartite matching
for deficits against decomposable credits below them.
Whenever matching fails, it extracts a down-set and
asserts its direct K-sum violation. Lex-factorization
closure, cancellation of generator multiples of m, and
`K_semigroup<=K_ideal` are checked separately at every
shift. All these identity/reduction checks pass.

Inputs comprise seven named semigroups, 48 examples from
the even-modulus binary family and its spike completions,
16 examples of Family 6.1 (t=4,...,19), and 350 interval,
random-generator and truncation examples. The random
seed is 150022; random moduli are in [10,127]. Counts
include semigroups appearing in more than one input.

| Quantity | Count |
|---|---:|
| Semigroup input records | 421 |
| All tested shifts | 26,428 |
| Shifts requiring a nontrivial matching | 8,428 |
| T1-failing semigroup records / shifts | 44 / 191 |
| True-shift T1 failures | 42 |
| T1-DOWN-failing semigroup records / shifts | 79 / 344 |
| TAIL-failing semigroup records / suffixes | 44 / 191 |

Every reported T1-DOWN failure is confirmed by its explicit
down-set. There are no Wilf failures. The smallest-modulus
true-shift witness in this sample is the m=13 example of
Section 3. Global minimality in genus, multiplicity across
all dimensions, or generator list is not asserted.

### 9.5 Counterexample families and the positive replacement

`families.py` constructs the full generator input and Apéry
data from the proved descriptions. `verify_case.c` then
recomputes each semigroup independently. All 18 cases
agree, including minimal generators, M, conductor, ell,
Lambda, W, sum K and excess; `audit.py` compares each
printed C result to the formula data.

- T1-H: H=3,...,12,20,50. At H=50 the true-shift excess
  is 1,176, with sum K=2,499 and m-e=1,323.
- Height-three B3 family: k=2,...,7, using the verified
  B3 prefixes of `{0,1,4,13,32,71,124}`. At k=7 it has
  m=2,984, sum K=168, m-e=112 and excess 56.

`check_height3.py` uses seed 150033 and 3,000 random
height-three ideals in dimensions 2,...,6, with moduli
3,...,60. Residues may be noninjective, as the positive
theorems do not need injectivity. On 93,055 shifts it
checks the pointwise classification and sharp error
bound. The pseudoforest sufficient condition applies
on 88,532 shifts and the squarefree-five-direction
condition on 81,645; their conclusions have zero
failures. These counts support the elementary proofs;
they do not prove a theorem outside the stated domains.

### 9.6 Artifacts and hashes

`results/` contains all raw logs, `audit.json`,
`semigroup_checks.json`, `verified_ideals.json`, full
counterexample inputs and `results/families/` with all
18 full generator inputs and their independent C logs.
The first witnesses remain preserved. Environment
metadata is in `results/ENVIRONMENT.txt`.

`SHA256SUMS.txt` lists the hashes of every source, input,
the report, COMMANDS.md and retained result. The manifest
was generated and checked on fejer using

```sh
nice -n 10 sha256sum *.c *.py case*.txt P15_REPORT.md COMMANDS.md results/*.* results/families/* >SHA256SUMS.txt
nice -n 10 sha256sum -c SHA256SUMS.txt
```

The manifest is external to the report to avoid a circular
self-hash. All listed hashes pass verification. Sections
1--8 were left unchanged while completing this section.
