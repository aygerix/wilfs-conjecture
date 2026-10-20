# P14: a uniform high-pair graph relay, quadratic overlap, and the critical arc

2026-10-19. **Research record; partial result.** Wilf for every
`3m<c<=4m` is not proved here. The results below are exact inequalities
on infinite classes and a counterexample to the proposed single-E
simplification. Earlier reports are unchanged. Computation is on fejer
in `~/wilf/p14/`, with at most four of our nice single-core jobs.

## 1. Target, notation, and frontier

The target is Wilf, or a sufficient payment of the critical pure-A
cubics, for every depth-four numerical semigroup. Throughout Sections
1--7, `S` has multiplicity `m>=2`, embedding dimension `e=d+1`,
minimal generators `m,n_1,...,n_d`, and

    M=max Ap=4m+h-1, c=3m+h, 1<=h<=m, rho=m-h,
    lambda(v)=floor((M-v)/m), s(v)=(M-v) mod m,
    L1(v)=sum_a depth_a(v)[lambda(v-n_a)-lambda(v)],
    K(v)=4-lambda(v)-L1(v), Lambda=sum_(w,a)lambda(top_a(w)).

Here Ap means `Ap(S,m)`, `ell=sum_Ap lambda`, and `W=e ell-c`.
The unit classes A, B, C, E have co-levels 3, 2, 1, 0. Write their
numbers as `a,b,gamma,eta`, so `e=1+a+b+gamma+eta`. In particular
`eta` is an E-generator count, not the P18 notation for short elements.
Their generator intervals are respectively `(m,m+h)`,
`[m+h,2m+h)`, `[2m+h,3m+h)`, `[3m+h,4m+h)`.
UF/MF means one/several factorizations over the non-m generators.
For v in Ap put `U(v)={a:v-n_a in S}` and, explicitly,
`C_U=sum_(v MF) max(1,lambda(v)+|U(v)|-4)`.

P13 proves `K<=1`, `K<=-1` at every MF value, and `K=0` at zero
and primitives. Positive K is exactly one at UF BB pairs of co-level
one, UF BC pairs, or UF co-level-zero cubics all of whose pair faces
have co-level one. Let `R_A` count the pure-A cubics of the last type,
`R_out` the other positive-K values, `Z=sum(-K)^+`, and `p_A` the
number of distinct pair faces of the `R_A` cubics. The P13 quantities
`C_U`, A-OVERLAP, SHADOW-OVERLAP, MF-SHADOW and UF-SPARSE+ retain
their exact earlier meanings.

**Known (lead-verified):** the P13 statements, GW-24--GW-26i,
LARGE-A', and the P11 payments under the review status stated by the
lead. **Exact gap:** the original negative-A/LOW+/LC frontier with
`alpha>=6`, `19<=a<10*C(alpha+1,2)`, `3e<m`, `m>=211`, now also
escaping the P13 tests and DEPTH4-EH. **Candidate mechanisms:**
quadratic collision credit, the full support interval of the critical
A-cubics, and exact C/E column accounting. **Discriminating test:**
maximize `R_A-Lambda-C_U-p_A` at actual depth exactly four, with
critical-A surplus `R_A>p_A` in the focused runs.

## 2. Re-check of the lead's consequences and exact C credit

### 2.1 DEPTH4-EH and the arc identity (PROVED; re-derived)

Put `D_dec=Ap\({0} union primitives)` and
`D(v)=1-K(v)` for `v in D_dec`. Then

    W=e-h+Lambda+sum_(v in D_dec)D(v).              (DEC-ID)

This follows from `W=rho+Lambda-sum K`, `|D_dec|=m-e`, and
`K(0)=K(primitive)=0`. Every term `D(v)` is nonnegative at depth
four. Thus

    W>=e-h+Lambda+Z,                               (DEPTH4-EH)

because `sum D=(m-e)-R+Z>=Z`. This verifies the lead's bound.

For a critical A-cubic write `n_i=m+t_i`. Each of its pair faces
has co-level one, hence `t_i+t_j>=h`, with repetitions counted.
Summing these three inequalities gives `T=t_i+t_j+t_k>=ceil(3h/2)`.
Since the cubic has co-level zero,

    s=m+h-1-T<=m-1-ceil(h/2).

The other critical types satisfy the stronger `s<rho` from P13,
and hence the same upper bound. Every critical residue is therefore
in `I=[0,m-1-ceil(h/2)]`, which has `m-ceil(h/2)` integers.
Let `N_low` count the noncritical values with s in I. Then
`R+N_low=m-ceil(h/2)` and

    W=Lambda+Z+N_low-floor(h/2).                    (ARC-ID)

No estimate about the number of such occupants has been assumed.

For later relay applications, the earlier pair-shadow payment can
also be read directly from these quantities. MF values have
`-K>=max(1,lambda+|U|-4)` because L1>=|U| and MF-UNIT holds.
Each pair face of a critical A-cubic is UF (otherwise the cubic
would not be UF), is AA of co-level one, and has K=-1.
These values are disjoint from the MF values, so
`Z>=C_U+p_A`. The outside critical values have distinct
s-values in `[0,rho)`, hence `R_out<=rho`. Consequently

    W>=Lambda+C_U+p_A-R_A.                        (RELAY-PAY)

This explains why every sufficient UF-RELAY condition below
implies Wilf, without any additional residual-family hypothesis.

### 2.2 Exact C and E direction formulas (PROVED)

For an E generator `n>=c`, the only non-singleton chain is
`{0,n}`. Its two top co-levels are zero, whereas its original
co-level sum is four. Consequently

    Lambda_n=ell-4.                                (E-EXACT)

For a C generator `2m+h<=n<c`, one has `2n>M`. Its origin chain
is `{0,n}`, whose top co-level sum is two instead of `4+1=5`.
Every other non-singleton chain is `{w,w+n}`, where
`0<w<=M-n<=2m-1`. Such a w is a primitive: two non-m generators
already exceed 2m, and a nonzero Apéry value cannot use m.
The upper endpoint is in `[c,M]` and has co-level zero. Hence

    Lambda_n=ell-3-sum_(0<w<2m, w+n in Ap)lambda(w). (C-EXACT)

This is an equality, improving the lead's stated lower bound by one.
It uses the same chain definition; no tile choice or no-wrap
assumption enters. The removable lower values belong to A or B,
with co-levels three and two respectively.

Put `T_dec=sum_(v decomposable)lambda(v)`. Since
`ell=4+3a+2b+gamma+T_dec`, summing the preceding formulas gives

    Lambda>=B_CE+(gamma+eta)T_dec,
    B_CE=gamma(gamma+1)+eta(3a+2b+gamma).            (CE-BASE)

In particular `Lambda>=B_CE+(gamma+eta)p_A`. Formula CE-BASE
counts actual directions and does not replace many E generators by
a single one. The single-direction shortcut is false, as Section 5
shows.

### 2.3 A generator-count relay for C/E directions (PROVED)

Put `g=gamma+eta` and `Q=C(a+1,2)`. Then the following explicit
condition, involving only the generator counts, proves UF-RELAY
and hence Wilf:

    max(0,a-1-3g)*Q <= 3B_CE.                     (CE-DIRECTIONS)

In particular each of the following is a sufficient condition:

    a<=3(gamma+eta)+1;
    eta>=ceil((a^2-1)/(3(a+7)))   if a>=1.        (E-DIRECTIONS)

These are uniform in alpha, b, m and all factorization overlaps.
For a=0 the target has R_A=0 and requires no separate fraction.

**Proof.** The weighted pair-shadow incidence gives
`3R_A<=(a+2)p_A`: a cubic has total incidence weight three,
and the possible extensions of a fixed AA pair have total
weight at most a+2. Its pairs are UF, so distinct monomials
in this shadow correspond to distinct values. Thus

    R_A-p_A <= (a-1)p_A/3,
    Lambda+C_U >= B_CE+g*p_A+C_U.

If `a-1-3g<=0` the payment is immediate. Otherwise use
`p_A<=Q` and CE-DIRECTIONS. This proves the first assertion,
including the sharper sufficient test with `3(B_CE+C_U)` on
the right. To obtain E-DIRECTIONS alone, use
`g>=eta`, `B_CE>=3a*eta`. If `a-1-3eta` is positive, the
required inequality reduces exactly to

    (a-1-3eta)*a(a+1)<=18a*eta,
    a^2-1<=3eta(a+7).

If that coefficient is nonpositive the relay was already paid.
This proves the asserted rounded generator-only bound. QED.

Consequently a remaining depth-four counterexample must have
`a>=3(gamma+eta)+2` and fail CE-DIRECTIONS. This is an exact
reduction toward the A/B core, not a claim that all remaining
C/E directions can be discarded.

## 3. Quadratic fibers give additive credit

### 3.1 General-depth quadratic-fiber lemma (PROVED)

This subsection holds at **every** depth `q=floor(M/m)`. Set
`K=q-lambda-L1`. Let `F_2(v)` be the set of unordered quadratic
factorizations of an Apéry value v, including loops, and `r_2(v)`
its size. For a pair `(i,j)` define

    w_(i,j)=lambda(n_i)+lambda(n_j)-2lambda(v).

If `r_2(v)>0`, put

    QDef_q(v)=lambda(v)-q+1+sum_(F_2(v)) w_(i,j).

Then

    1-K(v)>=QDef_q(v)>=0.                          (QUAD-FIBER)

**Proof.** Two distinct quadratic factorizations cannot share a
generator, since cancelling it would equate two distinct minimal
generators. Their exponent vectors therefore have disjoint supports,
including the multiplicity two of a loop. The join of *all*
factorizations dominates their sum. Every layer drop is positive,
so `L1(v)>=sum_(F_2(v)) w_(i,j)`.

For a single pair, the floor inequality gives

    lambda(n_i)+lambda(n_j)>=q+lambda(v)-1.

Indeed the sum of the two floor arguments is
`(M+(M-v))/m`, whose floor is at least `q+lambda(v)`; the
sum of their floors is at least one less. Thus

    d_(i,j)=lambda(n_i)+lambda(n_j)-lambda(v)-q+1>=0.

Also `lambda(v)<=q-2` because v is a sum of two generators
greater than m. Expanding yields

    QDef_q(v)=sum_(F_2(v)) d_(i,j)
                   +(r_2(v)-1)(q-1-lambda(v))>=0.

The L1 bound proves the other inequality. QED.

In particular **an Apéry value admitting any quadratic factorization
has K<=1 at every depth**, even if it has many longer factorizations.
The lemma does not impose pair injectivity. Each quadratic collision
earns at least `q-1-lambda(v)` additional units beyond the sum of
the single-pair credits.

### 3.2 Depth-four conductor corridor (PROVED)

At q=4 let

    QDef=sum_(v: r_2(v)>0) QDef_4(v),
    H2=sum_(v: r_2(v)>0) lambda(v),
    F_no2=#{MF values with no quadratic factorization}.

The quadratic-value set and the latter MF set are disjoint. The
quadratic-fiber lemma and MF-UNIT give, respectively, `D>=QDef_4`
and `D>=2` on these two sets. Applying DEC-ID and CE-BASE proves

    W>=e-h+Lambda+QDef+2F_no2
     >=e-h+B_CE+(gamma+eta)H2+QDef+2F_no2.          (QUAD-PAY)

**Uniform Wilf class.** Every depth-four semigroup satisfying

    h<=e+B_CE+(gamma+eta)H2+QDef+2F_no2             (QUAD-CORRIDOR)

satisfies Wilf, with no restriction on a or alpha. The weaker test
obtained by omitting `2F_no2` requires only the generators and the
list of their quadratic sums that are Apéry. It does not require
computing all factorizations, all chains, or the unknown Wilf number.
This is a proved sufficient inequality on an infinite class, not an
assertion that the corridor covers every remaining semigroup.

### 3.3 An AA-only form (PROVED)

Let `r_AA(v)` count unordered AA factorizations. An AA Apéry value
has co-level one or two: its value is below c since
`n_i+n_j<=2m+2h-2<c`. If `r_AA(v)>0`, the same disjoint-support
argument gives

    D(v)>= (3-lambda(v))(2r_AA(v)-1).               (AA-FIBER)

Thus one may replace QDef in the weaker corridor by the sum of
these AA credits. In particular let `P2,P3` count **formal** AA
pair monomials, with multiplicity of representations, whose values
are Apéry of co-level two and one respectively. Then

    W>=e-h+Lambda+P2+2P3.

If every AA sum is Apéry, `P2+P3=C(a+1,2)`, so Wilf holds whenever

    h<=e+2*C(a+1,2)-P2.                            (FULL-AA-CORRIDOR)

For a chosen primary tile the weaker version
`h<=e+2q-q2` follows, where q counts its selected AA pairs and
q2 their co-level-two subfamily. The full-pair statement counts
all representations and can be stronger in the presence of overlap.

## 4. Critical support interval and arc payment

**PROVED.** Critical A-cubics satisfy

    max(0,m-2h+2)<=s<=m-1-ceil(h/2).

The upper endpoint was proved in Section 2. For the lower endpoint,
each A offset is at most h-1, so `T<=3h-3` and
`s=m+h-1-T>=m-2h+2`; co-level zero also gives `s>=0`.
Consequently

    R_A<=L_A=max(0,m-ceil(h/2)-max(0,m-2h+2)),
    R_A<=U_A=C(a+2,3).                              (A-SUPPORT)

For the outside critical types, a formal monomial bound is

    R_out<=J_out=b*C(a+1,2)+(a+1)*C(b+1,2)
                      +C(b+2,3)+b*gamma,
    R_out<=rho.                                    (OUT-SUPPORT)

Here the terms are respectively AAB, ABB together with BB, BBB,
and BC. UF values have only one representing monomial, so no
unjustified injectivity of all formal monomials is used.

Combining A-SUPPORT, OUT-SUPPORT and K-ID gives

    W>=rho+Lambda+Z-min(U_A,L_A)-min(rho,J_out).     (ARC-PAY)

This is a uniform sufficient Wilf test. In particular, for h>=2
and `m>=2h-2`, one has `L_A=floor(3h/2)-2`. Therefore

    W>=m-floor(5h/2)+2-J_out+Lambda+Z.

**Explicit infinite class (PROVED).** Wilf holds if

    m>=2h-2,
    m+B_CE>=floor(5h/2)-2+J_out.                   (ARC-CORRIDOR)

For h=1 DEPTH4-EH already applies. In particular, **when B is
empty**, J_out=0 regardless of the C/E counts; hence every such
depth-four semigroup with `m>=floor(5h/2)-2` satisfies Wilf.
This includes a modulus range in which cubic offsets can wrap.
No (U), no bound on alpha and no ambient packing conjecture is used.

These are sufficient classes, not a proof of all B-free semigroups.
The full ARC-PAY inequality can also retain the available negative-K
and exact top credit when the displayed numerical corridor fails.

## 5. The single-E simplification is false

**COUNTEREXAMPLE.** The proposed implication

    at least one E generator => R_A<=ell-4+C_U+p_A  (SINGLE-E)

is false. An exact example has

    m=3004, h=1001, c=10013, M=13016,
    A offsets {501,505,517,553,629,785,997},
    a=7, alpha=0, b=gamma=0, eta=2884,
    ell=53, R_A=84, p_A=28, C_U=0,
    Lambda=141316, Z=28, rho=2003, R_out=0,
    W=143263.

Thus SINGLE-E has slack `49+28-84=-7`, whereas UF-RELAY has
slack `141316+28-84=141260`. This is **not** a UF-RELAY failure,
not a Wilf counterexample, and not a counterexample to a statement
with **exactly** one E generator. It shows that mere existence of
one E direction does not justify discarding the other directions.
The example already satisfies A-OVERLAP, has alpha=0 and 3e>m.
Thus it does **not** refute SINGLE-E restricted to the exact remaining
frontier. That restricted question remains open here.

The full generating set and Apéry list are in
[`results/simplex_e_gens.txt`](results/simplex_e_gens.txt) and
[`results/simplex_e_ap.txt`](results/simplex_e_ap.txt).
Here is a compact exact description and an
infinite counterexample family.

Let Y be an integer B3 set of size a>=7 containing zero, with maximum
T: all unordered triples, repetitions allowed, have distinct sums.
Take `h=8(T+u)+9`, `u>=0`, large enough that
`m=3h+1>C(a+3,3)+1`. Put

    t_i=(h+1)/2+4Y_i,
    S=<m,m+t_1,...,m+t_a> union [3m+h,infinity).

All `h/2<t_i<h`, and all t_i are one modulo four; m is a multiple
of four. The sums of degrees zero through three have distinct
residues: distinct degrees have distinct residues modulo four, and
within a degree the B3 property applies. All their offset sums are
less than m. Four A generators exceed M since their offset sum
is at least `2h+2>h-1`. Thus the Apéry set is the full cubic A
simplex (size `N=C(a+3,3)`) plus one conductor-aligned tail
representative for every unused residue. Those tail representatives
are primitive E values: an E value plus any nonzero generator
exceeds M. The residue h-1 is zero modulo four, nonzero modulo m,
and unused by the core, so M itself is primitive and the conductor
is exactly `3m+h`.

All Apéry factorizations are unique. AA pairs have co-level one
and K=-1; A-cubics have co-level zero, all faces of co-level one,
and K=1. All other values are zero or primitives. Hence, exactly,

    R_A=C(a+2,3), p_A=Z=C(a+1,2), C_U=0,
    ell-4=3a+C(a+1,2), Lambda=(m-N)(ell-4).

The SINGLE-E deficit is

    R_A-(ell-4+p_A)=a(a^2-3a-22)/6>0               (a>=7).

Integer B3 sets of every finite size exist, for example zero together
with distinct powers of four: at most three copies occur in a sum,
so no base-four carry occurs. This proves an infinite family.

The displayed finite instance uses the greedily constructed B3 set
`Y={0,1,4,13,32,71,124}`, u=0. `simplex_e.py` checks all triple
sums and constructs its full Apéry and generator lists. A separate
C Dijkstra/full-chain evaluation in `verify_gens.c` reproduces all
quantities. Seven is the least a for failure **within this full-
simplex family**, not a global minimality claim.

**Smaller verified witness.** A finite search over translations of this
fixed Y, without the modulo-four scaling, gives

    m=532, h=313, c=1909, M=2440,
    A offsets {157,158,161,170,189,228,281},
    a=7, alpha=0, b=gamma=0, eta=412, e=420,
    ell=53, R_A=84, p_A=28, C_U=0,
    Lambda=20188, Z=28, rho=219, R_out=0, W=20351.

It has the same SINGLE-E slack -7 and positive UF-RELAY slack
20132. Precisely, take `S=<532,689,690,693,702,721,760,813>
union [1909,infinity)`. Its 120 core monomials of degree at most
three have distinct residues modulo 532; the remaining 412 Apéry
values are primitive E values. The full minimal generators and
Apéry set are in
[`results/simplex_e_small_gens.txt`](results/simplex_e_small_gens.txt) and
[`results/simplex_e_small_ap.txt`](results/simplex_e_small_ap.txt);
[`results/simplex_e_small.json`](results/simplex_e_small.json) contains the
compact data. Both the Python literal-chain computation and the
independent C Dijkstra computation reproduce the displayed numbers.
Here QUAD-PAY is an equality: `QDef=56`, `H2=28`, and
`e-h+412*21+412*28+56=20351`.

`simplex_search.py` tests m in increasing order, with the fixed Y
and translations specified in its source. The first witness is 532,
after 628 (m,translation) trials. This is minimal in that specified
search, **not** a claim of a smallest counterexample over all
semigroups. The larger modular witness and the infinite family
above are preserved.

## 6. Strategic review and the still-open payment

The quadratic mechanism is different from the cubic-fiber obstruction:
distinct quadratic factorizations have disjoint supports, so all their
credits add without a fiber-size loss. Three-term factorizations can
share factors; their supports need not add. QUAD-PAY therefore
provides a genuine uniform corridor but leaves a cubic-dominant family.

The single-E proposal fails on a fully verified semigroup. The exact
C/E formulas remain useful, but they do not prove that one E direction
alone pays a full dense cubic A-face. Using every direction is essential
in the counterexample. The critical-arc route does give the explicit
ARC-CORRIDOR without assuming UF-RELAY.

I do not have a proof of UF-RELAY on the complement of these classes.
After the direct searches, the next mathematical gap is the geometric
relation between the UF critical A-cubics and missing upper extensions;
identities and quadratic fibers do not supply it. No zero-failure
census is being promoted to that relation. The remaining family and
computational record are completed below.

## 7. A uniform graph relay for the critical A-cubics

### 7.1 Exact separation into high-pair and low-link graphs (PROVED)

Call an A direction low if `2t<h` and high otherwise; there are
alpha low directions. A critical A-cubic cannot contain two low
factor copies, since their pair sum would be below h and would
not have co-level one. Thus every such cubic has at least two
high factor copies.

Let G be the loop graph on the high A indices with one edge for
each high--high pair face of a critical A-cubic. For each low
index l, let G_l be the subgraph consisting of high pairs z for
which `z*X_l` is a critical cubic. Vertices of G_l mean incident
vertices; an empty G_l has zero vertices. Let T_H count the
critical cubics with all three factor copies high. Then, exactly,

    R_A=T_H+sum_l |E(G_l)|,
    p_A=|E(G)|+sum_l |V(G_l)|.                     (GRAPH-ID)

The second identity uses UF: different pair monomials in this
shadow cannot have equal values, and distinct Apéry values cannot
have equal residues. There is no assumption that all formal A
pairs are residue-injective.

### 7.2 Pseudoforest relay (PROVED, elementary)

Suppose every connected component of G has at most as many edges
as vertices, counting a loop as one edge. Then

    R_A<=p_A,                                      (PSEUDO-RELAY)

and therefore UF-RELAY and Wilf hold, for arbitrary alpha and all
B/C/E directions.

Here is a direct proof. Each G_l is a subgraph of a pseudoforest,
so `|E(G_l)|<=|V(G_l)|`. A connected pseudoforest is a tree or
has one cycle. A tree has no loops or triangles, hence no legal
all-high cubic. For a unicyclic component with a loop at u, the
only legal all-high cubics are `X_u^3` and `X_u^2 X_v` along
edges incident to u; there are at most `1+deg_nonloop(u)<=|E|`.
For a component with an ordinary 3-cycle there is at most its
one triangle cubic, and for a longer cycle there is none. Thus
`T_H<=|E(G)|`. Apply GRAPH-ID. QED.

This is componentwise. The tempting variant `|E(G)|<=|V(G)|`
without a component condition is false. The smallest abstract
example has three vertices, edges `X^2,XY,Y^2`, and the third
vertex isolated: four cubics `X^3,X^2Y,XY^2,Y^3` have only
three pair faces. This is a graph counterexample, not a claimed
semigroup or Wilf counterexample.

### 7.3 A quantitative graph-excess bound (PROVED)

For each connected component C of a loop graph let e_C and v_C
be its edge and vertex counts. Define

    f_all=sum_C max(0,e_C-v_C),
    f_nb=sum_(C nonbipartite)(e_C-v_C),
    E_bip=sum_(C bipartite)e_C.

A loop makes a component nonbipartite. Every nonbipartite connected
component has `e_C>=v_C`, so f_nb is nonnegative. For an integer
f>=0 write `f=C(r,2)+s`, `0<=s<r`, and put

    M2(f)=C(r+1,3)+C(s+1,2), M2(0)=0.

Let T_G be the number of all degree-three monomials whose every
pair divisor is an edge of G. Then

    T_G-|E(G)| <= M2(f_nb)-E_bip.                  (GRAPH-MAC)

**External input and its checked hypotheses.** Macaulay's Hilbert
function theorem says that a commutative standard graded algebra
over a field has `h_3<=M2(h_2)`. We use it over Q, for a quotient
of a polynomial ring by a homogeneous ideal and then by one
homogeneous linear form. These are standard graded algebras with
finite-dimensional homogeneous pieces. No nonzerodivisor assumption
is required. The exact statement is Theorem 5.5 in
[Eliahou, JEMS 20 (2018), pp. 2115--2116](https://ems.press/content/serial-article-files/32312),
checked directly in the publisher's PDF. Only this standard
Hilbert-function bound is an external input here.

**Proof of GRAPH-MAC.** Discard the bipartite components for the
moment. They have no loops or triangles and hence T_G=0 on
each of them. On the nonbipartite components form

    R=Q[X_v]/(quadratic monomials absent from G),
    L=sum_v X_v.

Its Hilbert function starts `1,V,E,T`. The map multiplication by
L from R_1 to R_2 is injective: a kernel vector `(a_v)` satisfies
`a_u+a_v=0` on every nonloop edge and `a_v=0` at every loop.
An odd cycle or a loop forces zero throughout a connected
component, over Q. Thus the degree-two dimension of R/(L) is
`E-V=f_nb`. Its degree-three dimension is `T-rank(L:R_2->R_3)`
and is at least `T-E`. Macaulay now gives
`T-E<=M2(f_nb)`. Restoring the bipartite components subtracts
their edge count and proves GRAPH-MAC. QED.

The bound is sharp on complete loop graphs: at k vertices,
`E=C(k+1,2)`, `f_nb=C(k,2)` and
`T-E=C(k+1,3)=M2(f_nb)`.

For every subgraph F of G,

    |E(F)|-|V(F)|<=f_all.                          (SUB-EXCESS)

To prove this componentwise, if F is nonempty in a connected
component, extend it to the entire component by adding each new
vertex with one path edge, then adding all other missing edges.
The edge-minus-vertex count cannot decrease. An empty contribution
is bounded by `max(0,e_C-v_C)`. Sum over components.

Applying GRAPH-MAC to T_H<=T_G and SUB-EXCESS to every G_l in
GRAPH-ID proves

    R_A-p_A <= M2(f_nb)+alpha*f_all-E_bip.           (HIGH-GRAPH)

**Uniform relay class (PROVED).** UF-RELAY, and hence Wilf, hold
whenever

    M2(f_nb)+alpha*f_all <= E_bip+Lambda+C_U.        (GRAPH-RELAY)

This has no upper bound on a or alpha. For instance a single
unit of componentwise graph excess, `f_all=1`, costs at most
`alpha+1`; all pseudoforests have zero such cost. The negative
E_bip term can pay low-link cycles in dense bipartite components.
The theorem does not claim that every residual graph has small
f_all or that the displayed cost is always available.

### 7.4 Component-local payment, independent of unrelated low units (PROVED)

For a connected component C of G let

    f_C=max(0,e_C-v_C),
    alpha_C=#{low indices l with E(G_l) meeting C}.

Define its cost by

    cost(C)=M2(f_C)+alpha_C*f_C       if C is nonbipartite,
    cost(C)=alpha_C*f_C-e_C          if C is bipartite,
    C_G=sum_C cost(C).

Then

    R_A-p_A<=C_G,                                  (LOCAL-GRAPH)

and the explicit condition `C_G<=Lambda+C_U` proves UF-RELAY.
This cost uses the low indices that actually meet a component,
not the total alpha. In particular it remains uniform when many
unrelated low directions are added.

To prove it, split GRAPH-ID over the components. Every all-high
cubic belongs to one component. Apply GRAPH-MAC separately on
each nonbipartite component, and use zero all-high cubics on a
bipartite component. Apply SUB-EXCESS to each nonempty low-link
subgraph of that component; at most alpha_C of them occur. Sum.
This proves LOCAL-GRAPH without a global regularity assumption.
For a component with f_C=1 the nonbipartite cost is alpha_C+1;
a pseudoforest component has zero nonbipartite cost. These give
explicit infinite families with bounded local graph excess and
bounded local incidence, even when global alpha is unbounded.

The complete loop-graph with every low link equal to it makes
the abstract bound sharp: its high-cubic excess is M2(f_C), and
each low link has excess f_C. The remaining dense-graph case
cannot be eliminated by improving this abstract bound alone;
one must use which such configurations admit actual residue-
complete Apéry labels, or spend additional available credits.

## 8. The depth-five continuation: paying K=2 cubics

This section was started after the depth-four gap was isolated in
Section 6. It does not replace the P14 depth-four target.

### 8.1 Complete positive-excess classification (PROVED)

Now assume `M=5m+h-1`, `c=4m+h`, `1<=h<=m`, and set
`K=5-lambda-L1`, with the same exact definitions of depth and
top credit. Then:

1. `K(v)<=2` for every value.
2. MF values have `K(v)<=0`.
3. `K(v)=2` is possible only at a UF cubic of co-level zero,
   every pair face of which has co-level one. Its three factors
   lie in `(m+h,2m)` and have unit co-level three. Its pair
   faces are UF and have K=0.
4. Every such K=2 value satisfies
   `s(v)<floor((m-h)/2)`.

**Proof.** Write J for the degree of the join of all factorizations.
For MF values, J>=5 gives `lambda+L1>=5`, hence K<=0.
If J<=4, cancel the common part of two distinct factorizations.
Both remaining lengths are at least two, since a length-one
remainder would decompose a minimal generator. Thus J=4, their
common part is zero, and they are two disjoint quadratic
factorizations. There can be no third factorization inside this
join: a third quadratic would be disjoint from either one;
a cubic would leave a single generator of value v in the join
of total value 2v, again decomposing that generator. A quartic
would use the full join and have value 2v. Put
`l=lambda(v)<=3`. The floor bound from Section 3 gives
`L1>=8-2l`, as well as `L1>=4`. For `l=0,1,2,3`,
`l+max(4,8-2l)>=6`; therefore K<=-1 in this case.

For a UF value of degree j, `L1>=j` and j<=5. Degree two
is covered by QUAD-FIBER, degree four has K<=1, and degree
five has K<=0. Only degree three can give K=2; it then has
`lambda=0`, `L1=3`, so all pair faces have co-level one.
Each pair is at least `3m+h`; subtracting it from
`v<=5m+h-1` shows that the remaining generator is at most
`2m-1`. Conversely, pairing any factor with another factor
at most `2m-1` shows it is at least `m+h+1`.
Thus every unit co-level is three. UF descends to pair
divisors, and the pair formula gives `K(pair)=5+1-3-3=0`.
Finally the three pair inequalities give
`2v>=9m+3h`, so

    s(v)<=5m+h-1-ceil((9m+3h)/2)
         =floor((m-h)/2)-1.

Zero and primitives have K=0 at every depth. This proves
all the assertions. Conversely a UF co-level-zero cubic with
all pair faces of co-level one has L1=3 and K=2. QED.

More generally, the same argument proves `MF => K<=q-5` for
every q>=4. If J>=5 this is immediate. If J=4, put
`l=lambda(v)<=q-2`. The two disjoint quadratic factorizations
give `L1>=max(4,2q-2-2l)`. Splitting at `l=q-3` proves
`l+L1>=q+1`, so K<=-1<=q-5. No GEN-EH assertion at
depth six or above is inferred from this bound.

**Sharpness / preserved failed extension.** MF-UNIT cannot be
extended unchanged to depth five. In `<10,16,17,18>`,

    Ap by residue=[0,51,32,33,34,35,16,17,18,49],
    M=51, c=42, h=2,
    51=3*17=16+17+18,
    depth(51)=(1,3,1), L1(51)=5, K(51)=0.

This fails the proposed unchanged extension `MF => K<=-1`;
it does not fail GEN-EH or Wilf. The depth-five MF bound is
zero, with equality here. The finite instance is independently
checked below.

The tree check also gives the smaller witness `<8,13,14,15>`:

    Ap=[0,41,26,27,28,13,14,15], M=41, c=34, h=2,
    41=2*13+15=13+2*14,
    depth(41)=(2,2,1), L1(41)=5, K(41)=0.

Multiplicity eight is the least found for this failure in the
genus-at-most-28 census. No global minimality beyond that domain
is asserted. Both witnesses are retained.

### 8.2 High-pair graph payment for GEN-EH (PROVED)

Let beta count the K=2 values. They are exactly the only
negative terms in `sum_decomp(1-K)`. Let p_5 count their
distinct pair faces, and F_M the MF count. Those faces are
UF with K=0, so they contribute one each to that sum. MF
values are disjoint from them and also contribute at least
one each. The all-depth version of DEC-ID therefore gives

    W>=e-h+Lambda+p_5+F_M-beta.                    (D5-PAY)

Every beta-cubic contains at least two factor copies in

    H={n_i : (3m+h-1)/2 < n_i < 2m}.

Indeed two smaller copies have pair sum less than `3m+h`.
The other possible factors belong to
`L={n_i : m+h<n_i<= (3m+h-1)/2}`. All remaining generators
are excluded by Section 8.1. Construct the high-pair and
low-link graphs of these beta-cubics exactly as in Section 7.
With `s_5=|L|`, the same proved graph lemma gives

    beta-p_5<=M2(f_nb)+s_5*f_all-E_bip.

Consequently **GEN-EH at depth five**,

    W>=e-h,

holds whenever

    M2(f_nb)+s_5*f_all<=E_bip+Lambda+F_M.           (D5-GRAPH-EH)

In particular it holds if the critical high-pair graph is a
pseudoforest. A simple generator-only infinite subclass is

    #{minimal generators in ((3m+h-1)/2,2m)}<=1.    (D5-HIGH1)

The graph then has at most one vertex and one loop, so it is
a pseudoforest. This pays every K=2 cubic by distinct pair
faces; no Macaulay theorem is needed for this special case.
For semigroups of **depth exactly five**, D5-HIGH1 together
with `h<=e` implies Wilf. This is not a statement settling
all smaller conductors, since the full depth-four case is
still open.

The component-local version also holds: replace alpha_C by
the number of eligible low indices meeting C, and compare
the resulting C_G with `Lambda+F_M`. The proof is exactly the
same component decomposition applied to D5-PAY.

## 9. Computational record (FINITE CHECK / OBSERVED)

All computation below was performed on fejer in `~/wilf/p14/`,
under `nice -n 10`. At most four single-core jobs were used;
the last three recorded annealers ran concurrently. The compiler
was GCC 13.3.0 (Ubuntu), and the independent Python was 3.12.3
at `~/mathenv/bin/python`. No sympy, external LP solver, local
mathematical computation, or commits were used. The immutable
result copies are in `results/`. Checks are evidence for the
written proofs; none is a proof over an unbounded parameter.

### 9.1 Exhaustive semigroup trees

`tree.c` uses the effective-generator deletion tree, starting at
the nonnegative integers, and visits every semigroup of genus
at most 28. It computes Apéry values directly from the gap set
and recomputes the non-m minimal generators from Apéry, rather
than using a factorization tile. `core.h` computes backward
depths and literal forward chain tops independently, then
asserts the join, chain, and K identities.

| Run | Total tree nodes | Relevant depth | Relevant semigroups |
|---|---:|---:|---:|
| `tree 28` | 5,311,726 | 4 | 642,239 |
| `tree5 28` | 5,311,726 | 5 | 118,215 |

On all the depth-four instances, the C evaluator asserts:
P13 MF-UNIT/K<=1, COUNT-PAY and SHADOW-PAY; the exact arc
identity and DEPTH4-EH; C-EXACT/E-EXACT and CE-BASE; each
quadratic-fiber and AA-fiber inequality; and QUAD-PAY.
There were zero failures. No UF-RELAY failure was found.
The stronger observed `Lambda>=R` also had zero failures in
this census, with minimum zero; it is **not** asserted as a
theorem here. This census is smaller than the lead's existing
genus bounds; its purpose is checking the new inequalities.

`tree5.c` separately computes all depths, joins and forward
tops. It checks K<=2, MF K<=0, the complete K=2 type, UF/K=0
pair faces, the high-factor condition, the short s-arc and the
all-depth K identity. Among the 118,215 depth-five semigroups,
108,701 satisfy D5-HIGH1 and 2,861 have a K=2 value. There
are 157 occurrences of MF values with K=0, counted as values
over the semigroups. All proved assertions passed. GEN-EH
itself had zero observed failures and minimum slack zero;
only the classes proved in Section 8 are concluded analytically.
Both tree domains include embedding dimension two. In the raw
`GEN_EH_RECORD` lines, the printed field `K` is the recorded
global GEN-EH slack, not an element's K; only the class/face
diagnostics use it as an element K.

### 9.2 Exhaustive abstract graph checks

`graph_check.c` enumerates every loop graph on n=1,...,6 labeled
vertices, including isolated vertices. The counts are

    2, 8, 64, 1024, 32768, 2097152;
    total 2,131,018 graphs.

It enumerates all legal cubic monomials and checks GRAPH-MAC,
its componentwise sum, and the pseudoforest conclusion. It
also checks the extremal all-low-links-equal-G configuration
for alpha=0,...,10. All checks pass; the maximum GRAPH-MAC
slack expression `T-E-M2(f_nb)+E_bip` is zero at every n.
The first failure of the false global E<=V variant is n=3,
mask 11, exactly the example preserved in Section 7.2. This
is a check of abstract graphs, not a residue-completeness
enumeration and not an exhaustive test of every low subgraph.

### 9.3 Direct depth-four adversarial searches

`search.c` mutates one Kunz coordinate by one, validates all
affected Kunz inequalities, and imposes q=4 as a hard
constraint. Objective 4 minimizes
`Relay=Lambda+C_U+p_A-R_A`; it adds 10 to the optimization
score at R_A=0, but always checks the unpenalized relay for
a counterexample. Objective 5 minimizes
`(Lambda+C_U)/(R_A-p_A)`. A supplied seed file imposes
`R_A>p_A` at every state; this restriction loses no possible
UF-RELAY counterexample, since Lambda and C_U are nonnegative.

The following final runs have their full command, RNG seed
and initial Apéry file recorded in `COMMANDS.md` and in a
`CONFIG` line in the log. Counts mean mutation proposals,
valid proposals in the hard class, and accepted proposals.

| Log | m | Objective / hard class | Proposals | Valid | Accepted | Best objective |
|---|---:|---|---:|---:|---:|---:|
| `repro101.log` | 101 | relay, R_A>p_A | 200,000 | 86,904 | 153 | 913 |
| `repro211.log` | 211 | ratio, R_A>p_A | 120,000 | 66,804 | 529 | 387.2 |
| `repro527.log` | 527 | relay, a>=19, alpha>=6, 3e<m | 50,000 | 12,038 | 104 | 16,671 |

There were no UF-RELAY, CHAIN-U, CHAIN-POOR, WILF+ or Wilf
failures. The m=527 best state has actual relay 16,661,
R_A=0, a=19, alpha=6 and e=44. It is numerically residual-
shaped, but is **not** certified to escape negative-A/LOW+,
all P11 tests, or the P13 payments. This search limitation
is material: it does not probe a demonstrated near-failure.

Earlier exploratory logs are also retained: `kunz101.log`
(2,000,000 proposals, 910,215 valid, penalized best 347,
actual relay 337), `kunz527_shaped.log` (120,000 / 28,845,
penalized best 16,609, actual 16,599), `kunz101_seed.log`
(2,000,000 / 848,153, best relay 834), `kunz211_seed.log`
(600,000 / 308,099, best relay 1,808), and
`kunz101_ratio.log` (720,000 / 345,171, best ratio 99.2).
Their final witnesses are independently re-evaluated below.
These are exploratory snapshots; the final CONFIG runs above
provide the fully specified annealing repetitions. The
unseeded pilot's preference for R_A=0 states was the reason
for switching to R_A>p_A seeds and the ratio objective.

`structured.c 2500 140414` samples upper-half B3 A-offsets,
Sidon A-offsets and six-low/requested-19-A shapes, with B/C
generators and optional conductor truncation. Greedy set
construction may stop short of its requested size; actual
minimal generators and depth are always recomputed. It keeps
1,278 depth-four semigroups, of which 1,060 have R_A>0, 447
have 3e<m, and 44 have a>=19, alpha>=6, 3e<m. Minimum relay
among R_A>0 is 366; there is no failure. The moduli sampled
are 61, 101, 211, 401, 809, 1601, 2003. The 44 count means
these three numerical conditions, not all unclosed-frontier
conditions.

`gensearch.c` is a generator/truncation pilot: 59,898 tested
mutations, 59,875 in q=4, and minimum relay zero at a trivial
R_A=0 state. It is preserved as a failed search strategy,
not as evidence of proximity to the conjectured boundary.
`seeds.c` supplies modular full-cubic-A seeds at m=101,211,401.
Its inability to find one at m=61 is only a sampling result.

### 9.4 Independent arithmetic and actual high-pair graphs

`independent.py` uses the unchanged P13 Python checker for
heap Dijkstra, coin-change factor counts and literal chains.
It then independently reconstructs all quadratic factorizations,
the C/E formulas, A-SUPPORT/OUT-SUPPORT, ARC-PAY, the actual
high-pair and low-link graphs, both graph costs, and every
depth-five assertion and conditional theorem.

Inputs are the final witnesses of 11 search/seed logs, six
named semigroups, 1,200 random generator/truncation attempts
with seed 140014 and m in [10,180], and the two SINGLE-E
witnesses. Attempts outside q=4,5 or with inappropriate gcd
are not counted. The non-q=4,5 named input `<8,14,15>` is
used only for the general MF bound. Counts include repeated
semigroups when separate inputs coincide.

| Actual inputs / classes | Count |
|---|---:|
| depth four | 591 |
| CE-DIRECTIONS | 579 |
| E-DIRECTIONS (a>=1) | 410 |
| GRAPH-RELAY / LOCAL-GRAPH | 591 / 591 |
| QUAD-CORRIDOR | 590 |
| depth five | 535 |
| D5-HIGH1 | 434 |
| depth-five inputs with K=2 | 114 |
| D5-GRAPH-EH / component version | 535 / 535 |

Every checked inequality passed. `independent.json` gives the
full generators, Apéry lists and recomputed summaries of the
named/search witnesses. `simplex_e_C.log` and
`simplex_e_small_C.log` are independent C Dijkstra/full-chain
checks of the SINGLE-E failures. In both, QUAD-PAY is exactly
W. The independent sample has no demonstrated example where
QUAD-CORRIDOR succeeds but the full
`e-h+Lambda+Z>=0` test fails; the proof does not assert such
strict empirical separation.

## 10. What is proved, and the exact remaining gap

**PROVED.** In depth four, UF-RELAY holds under CE-DIRECTIONS,
E-DIRECTIONS, the componentwise pseudoforest hypothesis, or
either quantitative graph-payment condition. Wilf also holds
under QUAD-CORRIDOR or ARC-PAY with nonnegative right side;
ARC-CORRIDOR is a generator-count/modulus-only specialization.
These results have no bound on alpha. The quadratic-fiber
inequality is valid at every depth. At depth five the K=2
classification and the graph GEN-EH classes, in particular
D5-HIGH1, are proved. None settles all depth-five semigroups.

**COUNTEREXAMPLES.** The unrestricted SINGLE-E shortcut fails
on the infinite family of Section 5, with a smaller verified
finite witness at m=532. The unchanged depth-five MF-UNIT
extension and the global E<=V graph substitute fail as recorded.
There is no UF-RELAY counterexample and no Wilf counterexample
in this work.

**OPEN.** The full assertion `Wilf for c<=4m` is not proved.
The remaining original frontier still has

    alpha>=6, 19<=a<10*C(alpha+1,2), 3e<m, m>=211,

and the original negative-A/LOW+/LC conditions and failures
of the earlier P11/P13 tests. It must now additionally fail
CE-DIRECTIONS, QUAD-CORRIDOR, the nonnegative ARC-PAY test,
GRAPH-RELAY and LOCAL-GRAPH. In particular it has

    a>=3(gamma+eta)+2,
    (a-1-3(gamma+eta))*C(a+1,2)>3B_CE,
    C_G>Lambda+C_U,
    M2(f_nb)+alpha*f_all-E_bip>Lambda+C_U.

Its high-pair graph has a component with more edges than
vertices. No numerical alpha interval beyond the lead's
already closed ranges is claimed, and no actual semigroup
escaping every previous closure is exhibited here.

**Next precise lemma.** For the actual dense high-pair components
of this reduced frontier, bound

    sum_C [T_H(C)-e_C
             +sum_l (|E(G_l intersect C)|-|V(G_l intersect C)|)]
       <= Lambda+C_U,                              (DENSE-RELAY)

or pay its excess by `rho-R_out` and the unused part of Z.
The left side is exactly R_A-p_A, but now only dense components
have an unpaid abstract graph cost. Complete loop graphs and
full low links attain the abstract Macaulay cost, so a proof
of DENSE-RELAY must use realizability by Apéry residues or
additional chain credit. Merely sharpening the abstract graph
count cannot remove that obstruction. This is the remaining
geometric/payment gap; no unproved ambient packing statement
has been used.

## 11. Reproducibility

`COMMANDS.md` lists the exact deterministic checks and the
fully specified final searches. `results/` contains their raw
outputs and the earlier exploratory snapshots, seeds, full
counterexample data and independent JSON. `SHA256SUMS.txt`
records source and artifact hashes, generated on fejer.
Earlier reports were not changed; no commits were made.
