# Wilf research — start here

Updated: 2026-10-24 01:19 EDT. This is the single current handoff. Update this page in place at each checkpoint.

## Current status

**ACTIVE goal: DIRECT-WILF, the actual Wilf number for EVERY S.** On2026-10-24 the
user explicitly resumed universal proof work and forbade all side paths. The new
goal tracker is ACTIVE. The stopped transport/Hall/cofactor/GPU programmes and
agents remain stopped. Exact authorization and scope are in [SCOPE.md](SCOPE.md).

**Scope:** proves Wilf for EVERY numerical semigroup if the target below is proved.
Proved reduction from all S: **yes, exact equivalence by the Apéry identities**.
For proper S, let m be its multiplicity, e its ACTUAL embedding dimension,
p_j its nonmultiplicity primitives, w_r its Apéry values, and M=max w=c+m-1.
With A_t={r:w_r<=t}, empty for t<0, set Area=sum_(t=0..M-1)|A_t|. The target is

    e*Area >= m*M + (e-2)*m*(m-1)/2.

The difference of the two sides is EXACTLY m*W(S), not an auxiliary bound Q.
S=N has c=0 and is trivial. Neither m, e nor depth is bounded in this task.

**Latest universal-argument attempts E493–E496: three required steps rejected.**
The E492 border contribution alone is insufficient on a genuine sparse/deep,
cofactor-one source (border11760<C12096). Applying Zhai directly to rounded
conductor levels also lacks its linear-grading hypothesis; its proposed error
bound is exactly the old false Carry Lemma. Neither shortcut is being repaired.

A direct ALL-S multiplicity induction was then attempted: some clock contraction
n-floor((n+m-t)/m), followed by gcd normalization, should have actual W<=W(S).
That statement would prove Wilf by induction on m, but it is FALSE. One explicit
source m63,e12,c38322,g34357,W9258 has ALL63 contracted W larger; minimum157419.
Paper estimates already prove every contracted W>=9260. Existing C++ plus
independent heap/membership DP confirm all12 distinct outputs and every paper
bound (13 inputs total,9684edgechecks,794attainments,1.026925s after compilation).
Exact source/proof: [PROOFS E496](PROOFS.md#e496--every-clock-contraction-increases-w-on-one-explicit-source).
Witness and embedded exact runner: src/apery_scan/data/clock_contraction_496.json.
No new engine/flow/GPU/agent; the obsolete old60 test was canceled before execution.

This rejects the stronger monotone induction step, not Wilf, not a conditional
negative-W transfer, and not every possible descent. The source is flat and
already Wilf-positive; no restricted nonflat repair is activated. Do not present
these failures as a universal sign theorem. The actual area target remains open,
the goal remains ACTIVE, and all scoped numerical handles are terminal.

**E492 user-supplied sharp half-stability theorem — PAPER AUDIT PASSES.** For every
actual S with3<=e<m, the supplied nonsimplex downset argument proves

    mW+(e-2)m(m-1)/2 >= M/2.

Root independently rederived the planar block polynomial, its row estimate and
small coprime cases, and checked that plane-section columns are actual columns
of the full downset. Low surplus forces a complete weighted cutoff; equal axis
lengths then force a simplex, ruled out by cyclic injectivity. No gap found.
This is internally audited on paper, not Lean checked, externally refereed or
established novel. Precise proof/audit: [PROOFS.md, E492](PROOFS.md#e492--user-supplied-sharp-half-stability-theorem-paper-audit-passes).

Consequently an ACTUAL counterexample must satisfy
M<=(e-2)m(m-1)-2m. This supersedes E448's quartic cutoff by a cubic cutoff in m;
m remains unbounded. The1/2 coefficient is sharp over the stated range, using
<4,4t+1,8t+3>. This is a completed quantitative reduction, not full Wilf and not
an instruction to optimize constants or enumerate the remaining conductor box.
The border-column sum is also valid and gives W>=226 on <101,102,111>; direct
summation verifies exact W904. Its universal payment of the finite correction
is NOT asserted. User-reported finite checks were not rerun; sandbox attachments
are absent in this workspace. No numerical campaign or new agent was launched.

**E490 audit — sound on paper:** the user's full unequal-cost recursion is exact:
A_t={0} union UNION_j(delta_j+A_(t-p_j)). Also A_u+A_v subset A_(u+v), and
Area=sum_r(M-w_r). Crucial arithmetic remains: p_j=delta_j mod m and w_r=r mod m.
Consequently all birth times are distinct, with at most one new residue per
integer time. Minimal generators and their actual costs cannot be replaced by
an arbitrary weighted graph or a supplied generator count.

**E491 first proof attempt — coarse estimate rejected, full route still open.**
Kneser gives a valid common-threshold increment, but rounding unequal costs to
that threshold loses too much. On the ONE paper calibration <101,102,111>, its
resulting lower profile cannot even recover the homogeneous downset bound. An
abstract weighted cyclic graph also disproves an area theorem that omits actual
birth arithmetic. These are method falsifiers, not Wilf counterexamples or
special-case research programmes. A finer birth-rank inequality is proved, but
subtracting ranks does not preserve the linear weights needed by the downset
theorem. No integration paying the finite correction has been established.
Statements, proofs and qualifications: [PROOFS.md, E490–E491](PROOFS.md#e490--user-priority-change-actual-wilf-area-and-exact-reachability).

**SUSPENDED:** JOINT-ANCESTOR, cross-column transport, protected-prefix
rearrangement, cofactor-obstruction conjectures and GPU searches. Earlier
mathematical results and implementations remain available as history, not next
instructions. E488/E489 were unexecuted preparations: no E489 source/network
audit ran; its untested CLI has been removed. No numerical campaign, worker,
rental or new agent was launched for E490–E491. The same earlier agents remain
stopped. No universal proof, counterexample, Lean verification or novelty claim.

## Method and standing orders

Read [DIRECTIVES.md](DIRECTIVES.md) for the binding rules. Work backwards from the ACTUAL
Wilf inequality and seek an arithmetic estimate with a proved implication to it.
The user's new reachability priority supersedes old auxiliary-target selection.
C/C++ remains preferred if a later scoped experiment is needed. Every target
needs an explicit implication chain to full Wilf; bounded tests remain evidence.
Agent launches require the user's explicit approval.

## Retained mathematical results — historical, not active targets

The results below preserve context. Old requests to continue, compute or delegate
are superseded by the current status and the user's DIRECT-WILF instruction.

**E448, advisor's stronger stability theorem VERIFIED:** for EVERY S with3<=e<m,
M=c+m-1,C=(e-2)m(m-1)/2,L=m-e+1, now `mW+C>=M/L`, superseding E446's L^(e-1).
Thus W<=0 forces `c+m-1<=C*L<=m(m-1)/2*floor((m-1)^2/4)<=m(m-1)^3/8`.
The advisor's proof uses disjoint axis/singleton column deficits, forces equal axis
lengths under F<1/L, then forces a full simplex, excluded by cyclic residue injectivity.
Root and the same authorized geometric reviewer found no gap, including zero weights.
This is a completed QUARTIC actual-conductor reduction; m remains unbounded. Do not
start a bounded-conductor census or optimize the cutoff. For the original full joint
model, `mJ>=M/L-C-em*k(k+1)/2`, k=m-e, also over its real domain; no integrality or sign
of the finite minimum follows. The geometric arbitrary-primitive-modulus version holds.

**E448, correct parity Hilbert object VERIFIED:** with o=(A_odd),V0=A_even,
`o^n=V_n directsum V_(n+1)`, so `gr_o(A)_n=V_n/V_(n+2)` and b_n=v_n-v_(n+2).
The algebra is generated over B=A/o by q ORIGINAL odd primitive classes. Keep the
value-resolved B-module bound, not just b_n<=binom(q+n-1,n)*dimB. Ordinary field
Macaulay applies when all source primitives are odd (B=k); NO reduction from all S
to that specialization is proved. Exact lift mass is `sum n*b_n +2sum_(n>=3)eta_n`,
eta_n=h_n-v_n. The surviving moment has the correct generator budget; killed mass
still needs a GLOBAL payment from values, conductor/closure surplus and FULL reserves.

The advisor's all-odd e4 family<a,a+2,3a+8,3a+10>, odd a>=15, rigorously gives a-4
scalar descendants of ONE first-death edge, in c>4m,3e<m and cofactor1. It refutes any
fixed capacity on that map, not value-dependent/global allocation. No family-W programme.
Fejer C/membership/ideal-power audit checks ONLY old13/15/47, old19 and ONE a15 member,
0.18seconds: b=(1,2,3,4,2,1), b=(6,7,6) with dimB6, and11 shared deaths respectively.
All new results are advisor-supplied paper proofs, independently agent-reviewed, not
Lean checked or claimed novel. BOTH same authorized agents have completed their tasks.

**E449, earlier arithmetic component preserved / deferred:** ceiling only primitive
values to their residue classes preserves EXACTLY e, using the strict>=m primitive-word
margin. It realizes real actual points as genuine S', but the conductor and genus
increments compete. Two paper-checked points in the same OLD19 profile show rounding
can either lower or raise W (-18/19,+74/19). No negative real actual point was found;
both real defects in the witness are positive. No numerical run or LP expansion on
these points; priority remains E448's finite value/descendant payment. Shared all-Kunz
ceilings can create primitives and are not a substitute for the source generator count.

**E446, historical denominator bound (valid; superseded by E448):** for EVERY
S with3<=e<m, put M=c+m-1, C=(e-2)m(m-1)/2 and L=m-e+1. Then
`mW+C >= M/L^(e-1)`. Thus a hypothetical W<=0 forces
`c+m-1 <= C*(m-e+1)^(e-1)`. This quantifies the advisor's E416 strict recession theorem
uniformly over ALL profiles, without enumerating any. Proof: normalize primitive weights
to maximum1; the column deficit is strictly positive by E416's simplex/residue obstruction.
Every vertex has integer active rows of norm<=L, hence denominator<=L^(e-1), so its positive
integer-affine objective is at least the reciprocal. A word path misses e-2 other units,
giving |z|<=L. This also works for ANY primitive modulus a with3<=e<a, even when some p<a.

For the original full multiplicity-based joint model, k=m-e composite cells give
`sum x<=k(k+1)/2` by ordering their degrees. Hence
`mJ >= M/L^(e-1)-C-em*k(k+1)/2`, an explicit bound on every nonpositive full-certificate
sublevel. No integrality of the LP minimizer or finite-minimum positivity follows.
The bound depends strongly on m,e and leaves infinitely many residual domains as m varies.
Do NOT start a giant conductor census, fixed-multiplicity programme or cutoff optimization.
Finite parity/Hall payment is still the next mathematical obligation; no universal Wilf proof.
Status: paper proof, independently audited by one of the TWO Sol6.1-high agents expressly
authorized by the user this turn; not Lean checked, no novelty claim. BOTH agents completed
their tasks; no background research job or further agent launch is pending.

**E447, source kernel shortcut stopped:** the second agent disproved the proposed map
charging each killed scalar class to its FIRST vanishing odd multiplication edge. On the
ALREADY recorded13/15/47 example, nine scalar classes n in H_n,4<=n<=12, all first vanish
at45->60 by15. Parent45 survives since32 is not in S;60 dies since60-13=47. The parent
is ODD, so this is also absent from E445's even-parent reserve. A kernel edge can have
many scalar descendants. This refutes the specified map, not a dimension inequality for
ALL kernels or a full weighted descendant allocation. No compute or new family target.
Next retain BOTH directional kernels and the full descendant cost, actual values and
global conductor/closure surplus. No sufficient finite sign emerged from that pivot.

**E446 compute gate CLOSED before searching:** old mirror19/35/37/43/45/61 has height2,
m19,e6,c104,g64,W136,Dep4,kappa5,N20,Q_full19. Flat-MaxCL already covers it. The proposed
direct full-tile descent STOPPED in0.00seconds before any neighborhood comparisons; no new
seed or population was substituted. Independent membership/columns and existing parity/
advisor regressions pass. The temporary search mode was removed; only Q_full/phase fields
remain in the C/independent support audit. Do not treat this as a negative or positive search.

**E445, source-generator component proved / standalone payer stopped:** if q is the
number of odd primitives OTHER than the least odd a, each odd Apéry value has an even
Apéry parent through one of those q generators. Distinct children use distinct labeled
parent copies. Thus h_1<=q(a-h_1) and q*D_even-D_odd=P_par+R_par>=(a+2)h_1, where
P_par sums assigned primitive values and R_par sums unmatched parent deficits. This is
a positive typed functional, NOT the required total-deficit inequality. The exact full
budget is q*a*W=e*(q+1)*D_odd+e*(P_par+R_par)-q*a*(M+C_a).

The stronger primitive-only stage dropping R_par is FALSE on OLD19 in the remaining
domain/cofactor1: P319,R458,D_odd219, q3; its numerator is-924, while restoring6R gives
1824=3*19*W32. All seven parents are unique, so selector optimization cannot fix it.
Stop that stage; retain the FULL reserve. Do not count the three positive checks as a
sign theorem or optimize another selector. Higher-layer deaths can also occur with
only odd original primitives: the paper-only13/15/47 example has4 in H_4 but4*15=13+47.
It is a shortcut refutation, not a fixed-e target or added compute fixture.

**E445 modulus guard:** when a>m(S), an even primitive can be smaller than a. Then
mu(v)-mu(v+p)=floor(p/a)+phase_wrap can be0. The original E430 multiplicity strict-drop
claim remains valid, but cannot be transplanted unchanged. Source columns satisfy the
exact W=Gamma.mu+N-kappa; safe depth uses b(v)=max floor(p/a) over canonical children.
OLD6/7/11, a7, has tight17->23 by p6 with mu0->0. Naive unweighted depth would give6>W4;
the correct weighted bound gives4. This guard is necessary for the E444 parity proof.
The next all-S proof must couple the FULL R_par and odd deficits with higher multiplication
relations, or use the reserved full-tile Hall alternative. No finite sign has been proved.

**E444, current priority / advisor audit:** the four-generator family <6k+1,6k+3,6k+5,6k+7>
has h_1=3k with eS-1=3, even in c>4m,3e<m and cofactor1. All formulas, including the
support exclusion, verify on paper; ONLY k2 was computed. It is a calibration, not a
new restricted-family target. The advisor's source algebra k[S]/(t^a) has parity pieces
R/x^aM and z(M/R), dimensions a-h_1 and h_1, and EXACTLY eS-1 algebra generators.
It is the original Apéry algebra, not a new smaller object; value grading is retained,
whereas a standard grading by factorization length is not automatic.

**New multiplication consequence:** V_n, the span of n odd-class products, is obtained
from H_n by u -> n*a+2u, keeping only source-Apéry values. Thus dim V_1=h_1,
dim V_2=h_2 and V_(n+2) subset V_n; higher layers can die in the source quotient. OLD19
has h=(7,6,3) but dim V=(7,6,0), killing u31/32/33. This is concrete compatibility
missing from scalar ideal powers; it does NOT automatically pay their cost. The next
all-S proof target is the finite gain (e-2)(a-1)/2 in the source value mean-maximum
inequality. Its difference is exactly W. Do not merely reconstruct another Hilbert function.

**Hall alternative weakened to the useful budget:** for nonempty cuts exactly
Q=F_res+Leak+m-pool_size. BOTH discarded reserves must remain available. At the whole
tile Leak=0 and Q(D)>=0 already suffices for SUPP-WILF; optional all-cut, pool-only and
frozen targets are stronger. OLD19 whole budget is5, not its frozen margin1; selected114
is75 versus6, selected40 is35 versus2. The old40 leak control checks positive Leak2.
No new flow solve. The universal full-tile sign is still UNKNOWN. Forest cancellation
does not improve its numerical margin. E439 normalization remains proved and active.

**E443 diagnostic CLOSED:** a conductor differential bound would imply Wilf directly,
but is UNKNOWN and not prioritized on the basis of three positive fixed cases. The
exact Euler/torsion decomposition leaves the candidate torsion bound g-m+1. A single
graded reflection of the gaps is FALSE even on OLD19: no shift145..152 works, despite
torsion quotient dimension63 versus required50. All three rational trade-rank audits
and C ASan/UBSan replays pass. No new search/profile census or rank optimizer is next.
Preserve this alternative without mistaking another stronger invariant for a sign proof.

**E442, current correction:** unrestricted MON1, WS>=WU, is FALSE. The classical equality
source S=<5,21,22,23,24> has WS0 and closure U=<5,8,9,11,12> has WU2. All primitive
leave-one-out gcds are1. More generally m=2b+1,t>=2 gives WS0,WU=b, so the deficit is
unbounded. These witnesses have e=m and do NOT refute MON1 on the remaining sparse domain.
Full nonnegativity TRANSFER remains UNKNOWN and would still prove ALL Wilf by E441.
Here L=0 already: the binary lift cost can consume ALL2WU, not only the common-height cost.

**E442 ideal-power ingredient:** for 0I=T, the finite layers H_n=nI minus(n-1)I form
the positive pieces of a standard graded algebra with Hilbert function(1,h_1,h_2,...).
The exact E441 lift mass is h_1+2*sum_(n>=2)h_n. This exposes global growth constraints,
but its embedding dimension is h_1=|I minus T|, NOT eS-1. Even the old S=<5,7> has
Hilbert function(1,2,2,1,1) while eS-1=1. Quotient primitive7 acts nontrivially within
its first layer,1->8, and cannot be discarded from the coefficient action. A paper
admissible example also shows layers can grow2->3. Stop a scalar first-layer payment or
Macaulay substitution of eS-1 for h_1. No universal sign is proved by this standard algebra.
Indeed the classical source <2b+1,2b+3> has eS2 but h_1=b, unbounded. Its layers are
single nilpotent chains under quotient primitive2b+3, paid EXACTLY by the original
conductor; E442 proves this calibration on paper, without a family computation. The
next allocation must use value increments and handle overlaps between different actions.
Five FIXED cases pass independent finite-membership/modulo-a convolution/product/shift
audits on Fejer. No new search. Next: retain source-generator actions AND value labels in
a bound on the FULL weighted layer mass; if no finite sign emerges, return to E435/E437
or full weighted repair instead of adding another local reconstruction optimizer.

**E441, current arithmetic attempt:** for every proper S with least odd primitive a, let
H be the halves of even primitives and A+ the positive half differences (p-a)/2 of odd
primitives. U=<a,H,A+> is the additive closure of the normalized odd ideal I from E440.
It contains S/2, has eU<=eS and gU<gS. Thus conditional transfer WU>=0 => WS>=0 would
prove ALL Wilf by genus induction. Transfer is UNKNOWN; unrestricted WS>=WU is false (E442).
This is standard normalized ideal blowup, not a new representation or a proved Wilf descent.

**Paper-proved mixed identity:** modulo a (not necessarily the multiplicity), the Apéry
representatives satisfy wS(2s)=wT(s)+wI(s), T=S/2. Relative to wU, write integer lifts K,L;
0<=L<=K<=L+1. Only K-L is binary; the common height L can be large. The exact budget is
WS=2WU+2(eS-eU)ellU+(eS-1)(cS-2cU)-eS*(b+sum(K+L)), b=(a-1)/2. Its sign is NOT proved.
The stronger factor2 payer is already false on old19: WS32,WU23, correction-14.

**E441 bounded discriminator CLOSED:** one deterministic C descent from old19 made one
improving normalized-score move, then stopped at a local optimum after1392 comparisons,
1361 eligible. Endpoint19/41/50/52/53/58 has WS46,WU36; no negative margin. These two
cases and two boundary controls pass independent membership/ALL modulo-a entry audits;
ASan/UBSan reproduces the same search byte-for-byte. No more seeds or positive-profile
census. The next task is a GLOBAL common-height payment in the exact budget, retaining
both copies of WU if needed, rather than another reconstruction optimizer. E435/E437
cyclic payment and full genuinely weighted repair remain the other universal lines.

**E439/E440, actual arithmetic:** a least-genus Wilf counterexample must satisfy
gcd(P minus {n})=1 for EVERY primitive n. If that gcd is k>1, division of the other
generators gives T=S/k of strictly smaller genus and the exact identity
W(S)=kW(T)+k(eS-eT)ellT+(k-1)(eS-2)(n-1)/2, with nonnegative corrections. This holds
for nonmultiplicity pivots and changed multiplicity; the invariant formulas are known
rank-one results (Ojeda–Rosales2605.14775), not claimed new. The generic cofactor1 case remains.

The broader parity payer W(S)>=2W(S/2) is FALSE even after this normalization:
S=<17,18,21,37> has m17,e4,c84,g48,W60; T=S/2=<9,17,19,21,29> has c42,g24,e5,W48.
All four leave-one-out gcds are1 and S lies in c>4m,3e<m. The correction is exactly-36,
from losing one unit of embedding dimension under lifting. Normalized parity ideals give
W(S)=2W(T)+2(r-q)ellT+eS(v-b)+(eS-1)t; definitions/proof in E440. Here r,q are LOCAL
primitive counts (not top residue/depth), with r3,q4,ellT18,
v=b8,t0. An earlier reducible witness gives correction-79. Both W(S) are POSITIVE.
Stop monotone quotient funding and further variants. Conditional transfer of NONNEGATIVITY
is still UNKNOWN and would imply full Wilf by genus induction. Its next arithmetic proof
must retain WT and relate lost quotient primitives (halves of odd-generator pairs) to
filled-gap mass. Duplication itself is standard (Strazzanti1404.4959); no new representation
claim, fixed-rank target, solver or duplication-family census. The E435/E437 boundary and
full weighted-certificate lines remain active alternatives.

**E438 diagnostic closed:** the old BASE example15/37/39/40 already passes Dep10>T7,
with phase support12. No new positivity evidence; do not expand BASE or height-envelope checks.

**E437, exchange proved / finite sign still unknown:** the previous two-to-one exit collision
is repaired by rooting its two-edge positive-word tree at the shared word and charging its
two other endpoints to DISTINCT missing slots. More generally, a reserved exterior graph's
forest leaves exactly cycle_rank+sum(zero_capacity_vertices-1)_+ unpaid. Including internal
aliases removes the exhausted-vertex term: every noncanonical vertex has a full Gamma slot,
and each component has at most one canonical vertex. A rooted forest pays ALL tree edges;
only cycle edges remain. These are constructive paper lemmas, not a stronger positivity bound.
After p tree payments the exact remaining target is K+cycle_rank<=C+Gamma-p+V, still UNKNOWN.
The19 all-alias graph pays2 of12 aliases and leaves10 cycle units; the original internal
injection already paid4 aliases, so the new normal form is NOT numerically superior.
Stop graph/root optimizer refinements here. The next proof must supply finite surplus for
cycles AND carries jointly; no new profile census. Fejer audited only the old19/40/114 cuts
and the two-edge block, with distinct-slot witnesses and unchanged joint margins1/2/6.

**E436, stopped stages:** the separate claim L_out<=C is FALSE even with
K=F_in=0. A classical special-MSTD lift gives a genuine remaining-domain S with m97558,e513,
c623660,g383166,W122749762>0; its lex pair cut fails the stage by13924. A lower bound1440
holds for EVERY choice of pair representatives, so changing the tie order does not fix it.
JD on this pair cut is not refuted: margin227670; at the actual phase C+V also covers L_out by166,
so this witness does not make Gamma individually necessary. A corrected least-weight/lex
root association always finds a canonical cross-exit, but two explicit relations reuse one
capacity1 exit. The next proof needs JOINT exchange with all resources and raw carries,
not an independent staged/root allocation. No more MSTD examples or root optimizers are next.

**E435, current joint target:** internal negative-start aliases ALWAYS inject into distinct
missing-direction slots (u,j,0). This uniform component payment is PROVED, with no strict-gap
assumption. After cancellation the remaining debt is exterior aliases L_out plus raw carries K;
resources are unused column starts C, remaining missing slots Gamma-F_in and wrapped slots V.
The identity F_res=C+(Gamma-F_in)+V-L_out-K is exact; its universal sign remains UNKNOWN.
C>=0 is proved by choosing one distinct nontrivial column for each maximal cell. Cuts with
Gamma=K=0 are safe; zero-total-resource cuts reduce to that case and are also safe. These
are cut exclusions, not a universal Wilf theorem. The19 and old114 cuts refute both fixed
type assignments of unused starts, so the remaining allocation must permit adaptive sharing.

**E434, current proof obligation:** assigning every nonwrapping occurrence to its own parent
component is a PROVED feasible partial flow. The remaining nonzero demands are1+floor(z.delta/m),
and residual capacities are Gamma_D(u)+V_u, where V counts weighted wrapped child edges.
Universal extendability is UNKNOWN and stronger than E433 POOL. Its exact cut budget is
|U(E)|-h(E)-Leak(E). Three all-cut diagnostics pass and are CLOSED. The old19 tile gives
a sharp full-cut budget: demand24 versus missing4+wrapped7+free residues14, margin1. At least6
of7 wrap units must be used. Its alias kernel dimension12 cannot inject into missing4 or
even all11 auxiliary slots; actual source charges and aliases must be coupled. No universal sign proof.

**E433, current allocation test:** the joint-interior difference-set payment is FALSE,
including a zero-carry cut in <40,41,42,43> (Hall demand5, interior credit4). The62 cut
fails30 versus16. A replacement pool U(E) retains the residues of nonmaximal cells and
one-direction negative boundary starts, counting aliases once. The universal claim
h(E)<=|U(E)|<=m would imply E432, but is UNKNOWN. It is equivalent to routing all
nonzero sources in an explicit augmented graph; the origin reserves its one unit.
Two exact all-cut C checks pass (40 and114); they are closed diagnostics, not a theorem.
Critical-cut deletion conditions and an exact phase-walk/mean identity are paper-proved.

**E432, current finite-payment formulation:** the support completion functional over every
sub-tile is exactly a weighted closure/minimum-cut problem. Inversions linearize, all cell
benefits have the positive closed formula beta=1+floor(z.delta/m)+sum_(delta_j<=r(z))z_j,
and divisor capacities are d+|z|. The uniform Hall deficiency bound Delta_H<=m would prove
Wilf through SUPP-WILF, but its SIGN is UNKNOWN. A fixed one-free-unit-per-cell rule fails
by5 in the114case. Exact graph reductions and parent/inversion identities are paper-proved;
41 positive fixed-tile diagnostics are closed checks, not a universal positivity argument.

**E431, new general paper lemma:** any integer primitive direction annihilating the inner
primitive trades can be realized by genuine semigroups after L=1 mod m, L>2m(m-1)||v||_infinity.
The tight pattern, largest residue and canonical tile persist, all seed unpaid repairs remain
feasible, and the exact change is H.v. This realizes DIRECTIONS, not the sign of a fractional
LP objective. A common positive primitive shift can decrease W by an arbitrarily large amount
(-3N in an explicit genuine family). Thus monotone primitive lifts cannot fund the finite
correction. A necessary cap-load inequality now identifies negative primitive directions that
strict boundary/primitive/depth sources alone cannot match. No global positivity was proved.

**E430 strategy correction:** all36 saved transport anchors already satisfy the proved SUPP-WILF
shape exclusion. Their later positive certificate values are not evidence from resistant actual
Wilf cases. The old63 height3 example survives only that shape filter; the residue-aware theorem
also excludes it. See the current action below before reusing those examples.

**New paper fact:** every FULL feasible certificate strictly drops by at least1 along a tight
primitive addition, even on the real actual profile domain. Its superlevel sets are down-sets.
The raw/profile-patched baselines need not be antitone (8 exact comparisons on36 seeds), so a
level-set argument cannot silently substitute them. PROOFS E430 contains the elementary proof.
The lo-only cost<=rho payment proposal is FALSE on3 saved genuine S; discontinue it.

- **Recorded as Lean checked:** Wilf for c <= 4m. Together with the recorded 3e >= m theorem, the remaining
  domain is c > 4m and 3e < m. See [the literature record](LITERATURE.md) and `lean/external/conjio_d4/`.
- **PROVED in the record:** ID-q for every numerical semigroup; the implication ANCHOR => CORE1 => Wilf.
  See [PROOFS.md](PROOFS.md), section "ID-q for every numerical semigroup; Conjectures ANCHOR and CORE₁".
- **CONJECTURED:** ANCHOR and CORE1 themselves. Recorded checks include all 14,396,307 semigroups of genus <= 30.
  Their general proof is missing. The specific ANCHOR research program remains a proposal.
- **PROVED on paper this session:** upper-side closure B<=UA3<=W, an exact nonnegative repair LP, and
  W>=B+e ceil(M/2), where M is an integer assignment optimum on repair demands (PROOFS, E390/E392).
  Universal nonnegativity of this new bound is **unproved**. Any Wilf counterexample must make it negative.
  Matching-sum and rounding components are Lean checked (E394); the semigroup construction remains a paper proof.
- **Old gap closed on paper:** exact BASE-family deflation preserves Apéry minimality, reduces to c<=4m and
  gives W(S)=W(T)+3(k-1)(binom(d+3,3)-m). This excludes that profile, not general S (PROOFS, E393).
- **PROVED on paper:** b_s=max(0,mu_s-D_s), where D_s is the minimum sum of zero-or-one penalties on a
  tight factorization tree; D_s<=minimum factorization length-1. Thus the precise unpaid matching loss is
  W-(B+e ceil(M/2))=e(sum min(mu,D)-ceil(M/2)). The shortcut M>=sum min(mu,D) is FALSE (E396).
- **New general support:** kappa=[HH,i+j<=2r-m]+[LL,i+j<=m+r], algebraic identity Lean checked (E401).
  Qualifying primitive residues Z=[max(1,2r-m),r] union{m-1} never increase actual loss on tight addition;
  delta_s<=min(mu_s,(eta_s-1)_+), eta=min outside-Z primitive occurrences. This loss bound remains on paper.
- **Failed normal forms:** an original optimal cover need not fit actual repair caps (E399), and
  B<0 does not force W>=c/2 (E400). Capped covers have a separate exact assignment reduction and a valid
  W lower bound; universal positivity is still unproved. See PROOFS before reusing either failed shortcut.
- **New transport/rigidity (E403/E404):** unpaid variables satisfy certified difference constraints. The
  capped-pair graph raises the hard146 bound374->602; zero-loss composite summands alone improve none
  of27 saved cases. Exact-zero closure fixes146/146 in that case. Top-divisor unpaid repair is always zero,
  but that ideal can have size2 for arbitrarily large m. Arithmetic rigidity components are Lean checked;
  graph/semigroup closure proofs remain on paper. Universal nonnegativity is not established.
- **Residual support/weights (E405/E406):** the normalized homogeneous zero-side cone scales by1/2 into
  the full capped model; this scaling component is Lean checked. All12 nonempty cores among27 saved S
  have exact strictly positive directions, so there are no further forced zeros in those REAL capped models.
  A universal unpaid-coordinate bound1 is FALSE: an independently audited e11 semigroup has max x23=2.
  Residual counting must retain weights. These results do not prove universal certificate positivity.
- **Constructor correction (E407):** NS.from_gapset formerly accepted {0}, creating a false W=-1 object.
  Fixed/pushed in f93f460. Current p39 C search and independent checkers do not use this method or NS.
  The fixed constructor passes invalid-input regressions and round trips all1413 S of genus<=12 against
  generator/tree data and the independent Kunz implementation. No historical-use claim beyond the audit.
- **Coupled residual payment (E408/E409):** after propagation, exact assignment on positive overflows
  yields W>=Phi=W-e sum U+e ceil(M_U/2). Integer repeated-parent floors give a separate valid
  W>=IntCap>=Phi_Z, not a real-LP bound. User-supplied65case independently verifies integer1402->1407
  and exact real capped value1407. The central missing theorem remains global Phi_Z>=0.
- **Class-count payment (E411, paper lemma):** zero-allowance splits with a fixed-zero parent force
  equality of unpaid values. Give each equality class its actual residue multiplicity in pair cover;
  completing the assignment graph computes that weighted fractional cover exactly. On the new146case
  an8-residue class raises990->998, matching the full capped optimum. This is a local counting lemma;
  a general comparison with c/e is still missing. No class-size bound is assumed.
- **Limits/global budget (E412/E413):** the E411 zero-anchor merging rule has no active merges when
  rho0; it cannot be the sole universal mechanism. The general alpha position formula and rho0
  arithmetic implication are Lean checked. Factorization surplus E cannot pay all residual loss:
  <13,17,27,29> has unique Apéry factorizations,E0,R1. The global CH identity gives
  m Phi_Z=sum Def+E-C-e*m*R, so chain-end deficits and the discrete correction must be retained.
  This identity is a restatement of the positivity gap, not a newly proved lower bound on it.
- **Joint/primitive boundary model (E414/E415):** jointly varying actual Kunz coordinates and capped
  certificate y, with unbounded q>=5, gives positive exact LP minima on31 saved profiles. This proves
  regional full-capped nonnegativity, NOT Phi_Z positivity or universal Wilf. Fractional actual optima
  are not semigroups; integral ones are independently reconstructed. A general paper lemma reduces
  actual-side rows to primitive translations/positive primitive bounds, while retaining every coupled
  certificate row. These sources are primitive-chain boundary exits; uniform dual construction is open.

- **Advisor deduction verified on paper (E416):** for every realizable full joint profile with
  3<=e<m, every nonzero recession direction has STRICTLY positive objective slope. Repair loss has
  zero slope; equality in CH' would force a full simplex, ruled out by a difference-set residue count.
  Every sublevel is bounded and a finite minimum is attained. No finite-minimum sign or uniform depth
  bound follows. Credit: user's advisor; not yet Lean checked. Absence of negative full-model rays is
  structural, not additional evidence from the31 solved profiles.
- **Primitive affine projection (E417):** eliminate a,q using chosen primitive factorizations.
  mJ=H.p-C-e*m*sum x, with actual tight trades RHS0 and explicit residue/cap distances. Minimal
  excluded words of the canonical factorization down-set suffice for the ACTUAL domain, preserving
  every strict gap>=m by terminating integer rewriting. All coupled certificate rows remain.
  Independent audits cover fractional optima, column identities and every primitive translation.
  This is a canonical monomial-boundary reduction, not a claimed outer-Betti minimal presentation.
- **Failed sourcewise sign rule (E418):** discarding allowance-cost certificate sides AND requiring
  each actual a,q tight-row dual contribution nonnegative is false:19case has a verified ray slope-3;
  65case has slope-265/2. Those points violate original actual equalities and are NOT semigroups or
  failures of the full model. Discontinue that coordinate-dependent sign restriction. Removing just
  allowance-cost sides stays positive on31 saved profiles and gives0 on<13,17>; no universal claim.

- **Primitive dual transfer (E419):** the old dual converts exactly to
  J=N+K+Q+R_a+R_y-P-C', with nonnegative strict-boundary, primitive, depth and residue/cap credits;
  actual tight trade RHS0; P uses alpha/kappa, not old lo/up. The checker verifies the entire
  transformed coefficient vector. This is a normal form, not a universal nonnegative allocation.
- **Residue injection / limit (E420):** canonical fully extendible column bases inject into distinct
  canonical boundary cells. The finite rank-credit bound is valid but dominated by the old whole-
  boundary estimate; do not revive failed CR-TILE or call it a new positivity mechanism. Injected
  relations may be zero-gap trades (<11,12,18>), so they are not all sources of positive gap credit.
- **NEW genuine obstruction (E421):** <104,420,453,509> has c4784=46m,g2647,e4,W3764. Its w81=2265
  remains Apéry after adding EACH of420,453,509, yet its real capped unpaid maximum is7/3 and its
  integer maximum is exactly2. A separate exact LP dual and an independently checked integer witness
  prove those claims; MIP status is not used as a bound. All Apéry factorizations are unique. Thus
  weighted loss occurs even in the fully extendible interior without collisions. No global or interior
  unit cap; do not substitute a guessed2 cap. This is not a Wilf/full-certificate positivity failure.

- **Weighted transport (E422–E424, paper):** column reflections plus axis recombinations give
  e*sum x<=Gamma.x+P for arbitrary weighted real repairs. A pure-C integer min-cost flow optimizes
  axis-adding decompositions, with independent exact flow/dual/coefficient audits. This is not the
  full capped optimization. Its ORIGINAL baseline payment is FALSE: optimal bounds-13,-10,-33 on
  three saved genuine remaining-domain S. Forced-zero-aware transport repairs those examples and
  gives144,198,551, respectively; the weighted-interior104case gives3107. The corrected universal
  bound Omega>=0 remains UNPROVED. If all coordinates are forced zero, Omega=W, which explains
  nothing about its sign. The exact potential dual expresses the missing finite payment as (PAY),
  involving adjacent potential levels; do not replace it by a unit cap or unweighted single cut.

- **Primitive cycle allocation (E425, paper):** each primitive's column exits permute its column
  bases; a cycle has exactly m/h cells and total actual gap p/h, h=gcd(m,p). Excess strict gaps
  J-1 pay every primitive row's combined unit allowance alpha+kappa once, with positive surplus.
  A minimum-prefix cut gives an explicit nonnegative allocation. This bounds ROW allowances, not
  unpaid coordinates; arbitrary repeated composite-row weights, the objective coefficients and C
  are NOT paid. Every integer orbit has some J>=2; for coprime primitives/large p this already
  follows in the real domain. All31 saved joint points satisfy it, so no current integrality
  obstruction was found. Do not expand that diagnostic or claim a general repair of the real LP.
  The corrected E424 bound passed one closed36-anchor diagnostic (no new LPs); this is not a sign
  theorem. The natural column-scaled per-orbit extension is now refuted by E426; combine global routing
  with the E419 coefficient budget, rather than count more positive examples.

- **Weighted orbit obstruction (E426):** scaling E425 by canonical column lengths is FALSE even
  after known-zero closure. In the existing e11 example, primitive170/orbit4 has weighted strict
  excess7 against active row cost42 (unweighted7>=6 is valid). Another orbit has8<24. The complete
  E424 global bound is4419>0. This refutes only per-orbit column-scaled self-payment. Next use
  globally coupled primitive-boundary credits and match the E419 objective coefficients; no orbit,
  column or direction is required to pay separately. Exact table and regression are saved.

- **Coefficient no-gain theorem (E427, paper):** a nonnegative BALANCED primitive circulation,
  even across directions, strictly worsens a finite dual bound when its primitive coefficients
  are compensated using the existing primitive bounds. E425's scalar surplus cannot be counted
  again as independent credit. Stop that circulation-only approach. Signed tight trades and
  adaptive cap/residue loads remain essential possibilities.
- **Actual dual restriction (E428, paper/exact audit):** a joint optimum V and dual allowance cost P
  give an actual-domain dual bound V+P. Its gap at the joint actual point is exactly sum rc_y*x.
  This certifies20 of31 saved actual minima without new optimizer calls;11 have nonzero gaps and
  only lower/upper brackets. No actual value at a joint optimum is silently treated as a minimum.
- **Global boxed allocation (E429, paper; sign UNKNOWN):** use only profile-forced zeros K_0 and
  keep the entire real primitive domain, with no depth upper bound. Optimizing the clipped
  baseline has a dual with0<=lambda_s<=Gamma_s, signed inner trades, strict primitive sources,
  primitive/depth credit and complete residue distances. Its coefficient identity (BC) and exact
  budget (BB) retain transport cost P_0 AND tree cost sum lambda*T. An optimal dual can have at
  most e-1 PARTIALLY used baseline coordinates; signed tight trades sharpen this to the dimension
  of the primitive trade quotient. All others are0 orGamma. This does not prove its
  sign. The3 complete-profile minima100,300,312 (and3 preliminary positive-floor diagnostics)
  are exactly audited; that positive diagnostic is closed. Uniform nonnegative construction of
  (BC/BB), over every realizable profile, is the current mathematical obligation.

## Existing implementations

| Code | Purpose | Coverage and dependencies |
| --- | --- | --- |
| [apery.hpp / driver.cpp](../src/apery_scan/driver.cpp) | Exact cyclic-scan Apéry reconstruction, O(mk) actual primitive detection, certified predecessors and canonical support/phase analysis. | C++17, no solver. `--self-test N` compares every generator prefix with independent heap Dijkstra; `--warm B REPEATS SEED THREADS m k` compares batch evaluation, excluding generation/archive; `--adaptive B GENS SEED THREADS m p...` is scored-parent discovery. `adaptive.hpp` retains up to4 distinct heights per EXACT tile group and selects groups before representatives. `--archive-test` checks the advisor's neutral pair and collision separation. `--neighbors THREADS m p...` diagnoses one-input plateaus; `--neutral THREADS m p...` audits all19 saved first-step ties and their bounded exits; `--exchange THREADS m p...` enumerates proper two-atom cover changes (bitset m<=64, cap2million). Old `--bench`/`--mutate` remain closed pilot diagnostics. Never universal coverage. CPU m<=8192; pilot/GPU m<=1024. Signed64 arithmetic guarded by host128 bound8*m*m*max(p)<2^60. |
| [trade_policy.hpp](../src/apery_scan/trade_policy.hpp) | Exact original-label closure construction, unit-shadow restoration and exhaustive corner-policy falsification. | C++17 CPU. `--trade-policy m p...` exports source plus full word trace; `--trade-search 7` is the CLOSED E4594x128-at-most diagnostic, stopped at37 on its first certified failure. Least odd a<=256;1000corners is unresolved, not a stall; source-filter/cofactor/domain/rejection counts explicit. No device acceleration or general policy theorem. |
| [scan_cuda.cu](../src/apery_scan/scan_cuda.cu) | Batched CUDA/CUB segmented prefix/suffix minima and primitive/invariant extraction. | One block per candidate; same exact integer algorithm as CPU. GPU outputs compared with CPU arrays/statistics and O(mk) witnesses; Reusable GpuWorkspace supports warmed/feedback runs. E450/E452 provide actual CUDA and repeated-workspace checks, not just compilation. |
| [verify_scan.py](../src/apery_scan/verify_scan.py) | Independent coin-membership and explicit-column verifier for promoted records, including all conductor phases, exact neutral grouping/paths and complete two-atom set-sum coverage. | Python stdlib, no shortest-path dependency; bounded exact membership cap fails closed. Canonical lex ties checked explicitly. E453/E454 raw and independent results are in `src/apery_scan/data/cover_exchange_*453*`, `neutral_neighborhood_*454*`, `archive_control_454.jsonl`, `archive_integration_*454*`. |
| [run_pilot.py](../src/apery_scan/run_pilot.py) | User-authorized one-pod Runpod orchestration, bounded jobs, result download and confirmed cleanup. | runpodctl CLI; own task SSH key stays outside repository. Uses requested server deadline and detached cleanup watchdog. Price<=1USD/hour,<=20minutes, no persistent volume, never touches unrelated pods. Not a standing authorization to rerent or enlarge searches. |
| [enumh4.c](../src/scratch/p37/enumh4.c) | Direct semigroup enumeration; exact integer W; tight-pair keys. | No Gurobi. Fixed m/e, Kunz <= K, c > 4m, 3e < m; **height >= 4 filter**. |
| [enumlp.c](../src/scratch/p37/enumlp.c) | Same enumeration plus RT2/UA2 optimization and cached LPs. | Gurobi C API for certificate LPs; same height filter. |
| [enumlp3.c](../src/scratch/p37/enumlp3.c) | Newer C enumeration plus RT3/UA3, with optional height filter. | Pass h4only=0 for all heights. Audit found a 256-bit key overflow at m=24; key capacity is now derived from MAXM. |
| [anchgen.c](../src/scratch/p32/anchgen.c) | Genus-bounded tree; ID-q, ANCHOR and CORE1 checks. | No Gurobi; arbitrary heights/depths within finite enumeration and implementation limits. |
| [anchgen_t2.c](../src/scratch/p32/anchgen_t2.c) | Related T2 checker referenced in the proposal. | Audit before reuse. |
| [certprobe.c](../src/scratch/p39/certprobe.c) | Inspect genuine S; RT3/UA3/TX, cone/capped and joint-profile models; export exact-checkable data. | Gurobi C API. `--linear-lp FILE` solves a sparse nonnegative-variable CONTINUOUS model and exports primal/dual arrays; upper_dp.py `--axis-face INPUT OUTPUT [SOLVER] [EPSILON=0]` generates E429's exact integer matrix (stdlib, no Python optimizer), and verify_probe.py `--axis-face` audits it. `--face` is a CONTINUOUS joint actual/certificate LP with unbounded q>=5; `--face-primitive` reduces only actual-side rows. Neither treats fractional coordinates as semigroups. `--cone`, `--cap`, `--cap-max RES` remain. `--cap-int-max RES` exports an integer feasibility witness without an LP dual; the checker pairs it with a separate real LP bound when available. `--face-free`, `--face-free-oriented`, and `--face-zero-unpaid` are explicitly weaker diagnostics, never full-model counterexample checks. Independent checker: verify_probe.py (now also audits primitive projection and affine boundary rewriting). |
| [upper_scan.c](../src/scratch/p39/upper_scan.c) | Upper closure/assignment, local search, capacity, transport, unpaid-envelope, arithmetic and completion-cut audits. | Pure C. `--support-cut m g...` computes the exact minimum completion budget over all down-sets with integer flow/cut certificates; `--partial-support-audit` is the closed pattern diagnostic (E432). `--residue-audit G...` reconstructs S and its minimal-generator residue semigroup; `--residue-climb ITER m g...` is a bounded RD falsification diagnostic with the necessary genus-bound filter (E431, closed). `--axis-seed m g...` exports full seed invariants/tight rows without a solver; upper_dp.py `--axis-climb OUTPUT m g...` performs bounded deterministic generator +/-m descent in Omega/c using this exporter and the C flow solver. `--axis-flow FILE` returns an integer min-cost flow and exact residual dual potentials for E422–E424; `upper_dp.py --axis-transport INPUT OUTPUT [SOLVER] [--zero-aware]` builds the network and `verify_probe.py --axis-transport INPUT SUMMARY` independently checks it. `--weighted-audit` exports real-envelope residual matching; `--integer-weighted-audit` adds floors; `--equality-weighted-audit` counts forced-equal coordinates together. `--combined-climb-wide` tests Phi_Z/c in the existing neighborhood. `--weighted-search` tests the weaker propagation bound. `--interior-unit-search` filters targets to actual cells extendible by every non-multiplicity primitive; the new104case refutes its proposed unit cap. `--cover` is an UPPER certificate, not a Wilf lower bound. |
| [verify_matching.py](../src/scratch/p39/verify_matching.py) | Independent membership, heap Apéry, matching/capacity, equality and transport audits. | `--standalone` needs no Gurobi data. upper_dp.py has rational propagation, `--rigid` closure, and `--chain-budget INPUT MATCHING...` for exact CH/primitive-factorization budgets on audited data. |
| [lattice_cases.py](../src/scratch/p39/lattice_cases.py) | Reproduce the cofactor-shaped adversarial inputs and exact finite parking-tile check. | Diagnostic construction only; no separate family target. `--parking 6` checks all maximal-cell conductor alignments in the recorded tile. |

[Experiment E375](EXPERIMENTS.md) records 108 matching certificate minima against the MILP and C timings of
3.5-6.2 seconds versus 25-55 minutes for tested e = 4 instances. These are previous results, not new benchmarks.
Audit height filters, fixed-size limits and exact certificate coverage before adapting the existing code.

**E433/E434 inventory additions:** `upper_scan.c --support-pool-cut m g...` is pure C and exports
an exact all-down-set minimum of |U(E)|-h(E), with flow/cut certificate; exit5 means a failed
POOL claim, not Wilf. `verify_probe.py --completion-pool-check INPUT OUTPUT` independently
reconstructs membership, pool residues, full graph and integer certificate.
`--completion-structure-check data/completion_cut_probe.jsonl.gz OUTPUT` reuses just13/17,
40,62,114 to check residual-minimal cuts, strict deletion conditions and all their phase
identities. The41-fixture reports completion_interior_test.json and completion_pool_test.json
are selected-cut falsification diagnostics; only completion_pool_probe.jsonl.gz checks every
cut for the NEW pool objective, on TWO tiles. Do not conflate those coverages.
`upper_scan.c --support-frozen-cut m g...` tests extension of the fixed nonwrap partial flow,
exporting the exact residual min-cut. Its exit5 refutes this STRONGER allocation, not Wilf.
`verify_probe.py --completion-pool-check` also handles frozen_nonwrap=true, independently
checking residual capacities both by subtraction and by missing+wrapped components, the
leakage identity and full-tile budget/alias/wrap-load counts. Its `residual_budget` is the
frozen objective; `pool_budget` is the ORIGINAL pool budget at that selected cut. The three
frozen bundles are data/completion_frozen_probe.jsonl.gz and completion_frozen_audit.json.
`verify_probe.py --joint-defect-check FROZEN_INPUT OLD_CUT_INPUT OUTPUT` audits E435's
internal slot witnesses, maximal-column selection, exterior groups and exact cancellation.
It reuses ONLY the3 existing tiles, their old selected cuts and two40 zero-resource controls;
there is no new optimizer. Data are in data/joint_defect_audit.json and checkpoint_435_checks.log.

**E436 exact-witness implementation:** [mstd_shadow.cpp](../src/scratch/p39/mstd_shadow.cpp)
constructs ONE classical-base-expansion witness and computes its genuine Apéry set with
dynamically sized C++17 Dijkstra arrays (no solver). This exceeds upper_scan's m<256 limit;
it is not a new sampler. Compile with `g++ -std=c++17 -O3 mstd_shadow.cpp -o mstd_shadow`.
`verify_probe.py --mstd-shadow-check INPUT OUTPUT` independently reconstructs sum/difference
sets, sparse lex pair words and ALL97558 Apéry values using unbounded-coin bitset membership.
It also checks the two-to-one least-root exit collision. Raw data are
data/mstd_shadow_probe.json.gz; reports are mstd_shadow_audit.json,
mstd_shadow_sanitizer_audit.json and checkpoint_436_checks.log. Normal and ASan/UBSan
outputs match byte-for-byte. No Python optimizer or new profile census.
The JD audit covers ONE pair cut of this large D, not every down-set. Only the semigroup
membership/Apéry verification covers all97558 residues.

**E439/E440 exact arithmetic audit:** `verify_probe.py --quotient-descent-check ./repair_scan OUTPUT`
uses the existing pure-C --residue-audit reconstruction and separate Python membership DP.
It checks4 common-divisor descents, including a nonmultiplicity pivot and T=N;2 constructed
parity payer failures (one cofactor1); and the single closed E438 diagnostic. It verifies
ALL pivot-Apéry entries, minimal generator changes, parity membership, normalized ideal
generators/conductor/genus and the exact signed corrections. No new C code or optimizer.
Data: data/quotient_descent_audit.json and checkpoint_440_checks.log. run_checks.sh includes it.

**E441 implementation:** existing [upper_scan.c](../src/scratch/p39/upper_scan.c) adds pure-C
`--odd-audit G...` and `--odd-climb STEPS G...`, reusing its changed-multiplicity/generator
reconstruction. The bounded search has at most20 moves; its candidate box is m<256 and
other inputs<=8m, with c>4m,3e<m retained. Its printed `accepted` counts eligible neighbors,
NOT accepted moves. The single completed run stops after one move; do not expand it.
`verify_probe.py --odd-closure-check SEARCH_LOG ./repair_scan OUTPUT` compares saved
cases with fresh C outputs, then independent membership DP reconstructs S,T,I,U, minimal
generators and every representative modulo a. It verifies K,L, genus identities, cofactor
gcds and all four terms of the budget; controls include U=N and nonmultiplicity a.
Data: data/odd_closure_search.log, odd_closure_audit.json, checkpoint_441_checks.log.
ASan/UBSan search output matches normal SHA256
96bb30771b0c6751a68d74477ff57f2c9fd3012df1568006dcf602949ca5f7fa.
The old quotient audit also passed; no broad LP suite or new profile census. run_checks.sh
includes the targeted saved-case replay. All new mathematical statements are paper proofs.

**E442 implementation:** `verify_probe.py --odd-layer-check SEARCH_LOG ./repair_scan OUTPUT`
reuses C --odd-audit, then independently checks each ideal-power representative by finite
membership and modulo-a convolution, spans each layer by products of first-layer gap classes,
and verifies the two-step a-shift and exact weighted mass. It uses ONLY the two saved cases,
two old controls and the one paper-predicted unrestricted MON1 witness. No C source changed,
optimizer/search ran or new sanitizer path needed. The old E441 audit passed after the change.
Data: data/odd_closure_monotonicity_audit.json, odd_layer_audit.json, checkpoint_442_checks.log.
run_checks.sh includes this targeted replay. General algebra arguments remain paper proofs.

**E443/E444 implementation:** upper_scan.c adds `--differential-audit G...`, a bounded
pure-C factorization/trade-rank export (e<=10,c+maxP<=4096), stopping if selected rank>W.
`verify_probe.py --differential-check PROBE CONTROL BOUNDARY OUTPUT` independently enumerates
all factorizations by coin DP, uses exact rational ranks, checks Euler/torsion dimensions
and all possible reflection shifts. The THREE old inputs only have module dimensions
101/24/18 at c88/24/17; no theorem follows. Normal and ASan/UBSan outputs are byte-identical.
Data: differential_{probe,control,boundary,audit}.json and checkpoint_443_checks.log.

`verify_probe.py --advisor-parity-check EXE FROZEN_LOG ORIGINAL_LOG OUTPUT` audits source
algebra bases and ALL ordered basis products on k2 and old5/7,19 (169/25/361 products),
compares scalar layers with source odd products, checks k2 support via existing C
--axis-seed/--supp-audit, and restores reserves on seven OLD cut/control selections.
Data: advisor_parity_audit.json, checkpoint_444_checks.log. run_checks.sh includes both
targeted modes. The old layer audit also passes; no broad LP suite/new optimizer ran.

**E445 implementation:** `verify_probe.py --parity-credit-check EXE OUTPUT` reuses C
--odd-audit on ONLY old6/7/11, old19 and advisor k2. Membership reconstructs Ap(S,a),
then exact canonical columns check every ceiling drop and weighted depth. Odd-parent
witnesses, all allowed parent choices via per-child maxima, typed deficits and the full
primitive/reserve budget are checked. Data: parity_credit_audit.json and
checkpoint_445_checks.log. The old E444 algebra/reserve audit also passes; no C code,
new sanitizer path, solver or census. run_checks.sh includes the targeted replay.

**E446 implementation:** existing C `--supp-audit` and independent `support_geometry`
now both export `Q_full=Dep+N-kappa` and `phase=N-kappa`. No new search mode is retained.
`--support-audit data/full_tile_eligibility.jsonl OUTPUT EXE` independently replays the
OLD mirror19 eligibility rejection; raw seed/audit and aborted-gate log are in data/.
This checks a gate and added fields, not a new positive search. E446's all-profile
conductor bound is a paper proof with independent agent audit, not a numerical routine.

**E448 implementation:** `verify_probe.py --advisor-filtration-check EXE OUTPUT` uses
existing C `--odd-audit` and independent exact source multiplication/odd-ideal powers.
It verifies the V_n quotient and VALUE-graded module bound, mixed coefficient base,
moment/death identity and the a15 shared-edge witness. ONLY old13,old19 and that one
family member are controls; no solver or new C path. Data: advisor_filtration_audit.json,
checkpoint_448_checks.log; replay is in run_checks.sh. V_dimensions_from_n_zero includes
V0 explicitly. The general 1/L theorem and all-a countermap proof are PAPER arguments.

**E454 pointwise/source-trade implementation:**
`verify_probe.py --pointwise-death-check EXE OUTPUT G...` combines C `--odd-audit` with independent
membership, scalar layers, source multiplication and per-column prefix checking.
Only the advisor's31/33/101/103 input was run; its4/5-block packing is independently
verified column by column in `src/scratch/p39/data/parity_trade_control_454.json`.
No new C optimizer or source family. E455/E456 are paper proofs, not executable claims.

**E458/E459 independent word/policy audit:** `verify_probe.py --advisor-trade-check
OLD31 NEW39 NEW51 OUTPUT` verifies the exact saved controls, both unit orders, corner
geometry and scalar non-downset example. `--trade-policy-check SCAN_VERIFIER INPUT_JSONL
OUTPUT` independently checks source coin membership, U representatives/min-odd/lex words,
EVERY policy choice and update, all final corners, and diagnostic noncorner shadows.
CLI SCAN_VERIFIER points to apery_scan/verify_scan.py. Data: p39/data/{cyclic_source_control_457,
composite_source_control_458,advisor_trade_audit_458}.json; engine traces/audits in
apery_scan/data/trade_*459*. No new C/Gurobi implementation, GPU or broad suite run.

**E461 arithmetic cap/return audit:** same verify_probe.py now has
`--top-cap-check OLD31 OLD39 OLD51 NEW201 STALL_JSONL OUTPUT`. It checks exact scalar
cap values and net shadow credit on four cached controls plus one new CAP-TRANSFER
falsifier, including36 explicit return words and a symbolic-bound check. New source
still uses existing C --odd-audit and independent --pointwise-death-check. Data under
p39/data/: top_cap_control_461.json,top_cap_audit_461.json,top_cap_support_461.json,
top_cap_support_verified_461.json. No new C optimizer, CUDA kernel or search mode.
The E462 CRT and E463 fixed-rank theorems are paper proofs, independently reviewed;
no numerical family data or Lean formalization is claimed.

**E464/E465 implementations:** verify_probe.py --unit-orbit-check INPUTS... OUTPUT
loads ONLY cached promoted lex tiles, checks each unit image by explicit columns,
phase distances and both mirror identities; it reports normalized realization gates,
including all non-m deletion gcds. --factorization-energy-check RAW_SUPPORT OUTPUT
independently reconstructs one source, compares ALL C support fields and counts all
original-generator words belowc, with exact rational energy and E448-cutoff checks.
Data: p39/data/unit_orbit_465.json,energy_control_raw_464.json,
energy_control_verified_464.json. No new C search, solver, CUDA or optimizer path.
E466 strict-boundary normalization is PAPER ONLY; actual primitive values or W signs
are not claimed preserved. Exact reproduction is in EXPERIMENTS E464/E465.

**E468/E469 implementation:** [boundary.hpp](../src/apery_scan/boundary.hpp), exposed by
`scan_cpu --boundary threads 63 supplied...`, is restricted to the EXACT cached63
source. It computes all242 ray thresholds with primitive guards, deduplicates target
vectors, parallel-scores them and exports all witnesses/stop metadata. No adaptive
search or GPU dependency. `verify_probe.py --boundary-check SCAN_VERIFIER INPUT OUTPUT`
replays bounds and ALL evaluated source invariants/words/scores through independent
coin closure; on four selected full records it checks the physical axis map, on
ONLY origin the reflected mixed-edge guards. Reproduction: EXPERIMENTS E468.
Raw/verified files: apery_scan/data/boundary_468.jsonl,p39/data/boundary_verified_468.json.
The generic coin closure was factored out as verify_scan.py::coin_reconstruct; no
independence between two uses of that SAME coin algorithm is claimed. Scan, heap
and finite coin closure are the distinct reconstruction methods used here.

**E471 implementation:** `verify_probe.py --reserve-transfer-check` accepts ONLY
the four named old witness files (15 capped/coordinate records), rechecks exact
source/full-cap feasibility and support geometry, and exports J-Q and its two
signed terms. It performs NO optimization. Output:p39/data/reserve_transfer_471.json;
full command/input interpretation in EXPERIMENTS E471. The replay is CLOSED.
E470 wall-shadow/path/Qjump/calibration results are PAPER ONLY, no new wall walker.

**E472 implementation:** [cover_cubic.cpp](../src/apery_scan/cover_cubic.cpp) has
ONLY the fixed --output interface; sparse words degree<=3, all generator edges,
full invariants/cofactors, explicit columns and one-cell jump checks. No search
parameters or GPU dependency. Existing `verify_probe.py --cover-cubic-check INPUT
OUTPUT` independently verifies the basis, canonical pairs, exact shortest-path
certificate, tight-edge lex choices and active-column geometry; it does not call
the C++ code or the dense factor_basis/support routines. Input may be gzipped.
Data: [complete witness](../src/apery_scan/data/cover_cubic_472.json.gz),
[independent report](../src/apery_scan/data/cover_cubic_check_472.json). Reproduce
from repository root using the three commands in EXPERIMENTS E472. Both are CLOSED
fixed-control tools; no automatic generalization to a parameter scan.

**E473/E474 implementation:** existing [verify_probe.py](../src/scratch/p39/verify_probe.py)
adds two FIXED diagnostic modes. `--advisor-phase-path-check SAVED_E472 INPUT13 OUT`
checks both savedGamma sweeps and the one13source/twochambers; `--joint-ancestor-check
INPUT63 OUT` constructs the exact two-pool/axis-reassignable network, checks an integer
maxflow/primal-cut certificate and exports the axis-eliminated Hall cut. Both CLIs
assert their EXACT input generator lists; no general search parameters. Existing C
`upper_scan --axis-seed` supplies actual invariants, independently coin-replayed.
Data:p39/data/centroid_source_473.json,phase_path_check_473.json,
ancestor_source_474.json,joint_ancestor_474.json. Reproduction: EXPERIMENTS E473/E474.
The large E472 Apéry certificate was NOT replayed. All these finite controls CLOSED;
the input35network was cancelled as zero-demand before evaluation.

**E475–E477 implementation:** the SAME [verify_probe.py](../src/scratch/p39/verify_probe.py)
adds `--joint-ancestor65-check INPUT OUT` for ONE old65 control;
`--forced-ancestor-probe C_BINARY OUT` for the CLOSED four-island64-child critic;
and `--axis-augmentation-check PROBE_JSON_OR_GZ OUT` for ONLY its saved tight65
endpoint. No new C reconstruction code. Every ordinary/forced result checks integer
primal flow and equal-capacity cut; the postprocessor checks physical slots and a
modified complete102-token certificate without solving another flow. Data:
p39/data/ancestor_source_475.json,joint_ancestor_475.json,
forced_ancestor_476.json.gz,forced_ancestor_476.json.jsonl,axis_augmentation_477.json.
Exact counts, timings, hashes and reproduction are in EXPERIMENTS E475–E477.
No general compute activation, GPU dependence or new source/flow for E478.

**E481–E483 implementation:** the SAME [verify_probe.py](../src/scratch/p39/verify_probe.py)
adds `--unit-joint-check C_BINARY OLD476_PACK OUT_GZ` for the CLOSED one-new-tile
unit test (stops at18/48); `--small-joint-check C_BINARY OLD476_PACK UNIT481_PACK
OUT_GZ` for ONLY the L23 witness; `--axis-transport483-check SMALL482_PACK OUT_GZ`
for exactly two new permissions on its SAVED failed graph. Large values use an
independent heap/edge/attainment certificate; the small source also uses coin DP.
The residual repair keeps the full integer primal/equalcut certificate. Data:
p39/data/unit_joint_481.json.gz,small_joint_482.json.gz,axis_transport_483.json.gz.
E480 failed guard and every old tie are preserved in the report. No new C evaluator,
GPU dependency or general sampler. E484 is paper only; commands/counts/hashes in
EXPERIMENTS E480–E483. The old JOINT model remains implemented as a REFUTED policy.

**E486 implementation:** existing [verify_probe.py](../src/scratch/p39/verify_probe.py)
adds `--highrank486-check C_BINARY OUT_GZ` for ONLY the literal new153-source.
It uses the unchanged C reconstructor, independently heap-certifies canonical words
with ties allowed, builds both the old and source-indexed enlarged networks, and
checks integer primal/equalcut/label/column certificates. No general sampler or
union-neighbor merging of axis source groups. The output also records the eight
inherited contexts. Data:p39/data/highrank_486.json.gz; reproduction and hashes in
EXPERIMENTS E486. This ONE-input diagnostic is CLOSED; paper E485/E487 has no new
source/flow mode or W computation on the101 guard.

## Current attempt and next action

**Only objective:** prove the exact actual area inequality for EVERY S. E492 is
a completed large-conductor reduction, not a multiplicity bound or a census target.
The border-only, rounded-Zhai/phase-only and monotone-clock-contraction steps are
closed after E493–E496. Do not patch them with speculative exceptions. The latter
failure does not justify claiming that all universal descents are impossible.

**Next direct paper work:** use the FULL unequal-cost reachability recursion,
retaining residue congruences and all overlaps. One exact working form is to put
omega(t)=sum_j|A_(t-p_j)|-|A_t|+1>=0, Omega=sum_(t<M)omega(t), and
X=sum_(j,r)max(0,M-p_j-w_r). Then Area=M+X-Omega, so the universal target is

    e*Omega <= (e-m)*M + e*X - C_m.

This is only an equivalent working identity, NOT new progress or a stronger
auxiliary conjecture. The actual proof task is to derive the inequality from
the generating costs and cyclic arrivals, with root overlaps included. A coarse
common-threshold Kneser estimate is already too weak; dropping all overlap,
column level slack or nonborder columns repeats a rejected step. No unrelated
profile/hardware task should substitute for that argument.

The autonomous goal is ACTIVE, with no scoped computation left running. No
further experiment, sampler, agent launch or contraction variant is activated.
Old transport/Hall/cofactor/parity/source-repair/GPU programmes remain suspended.
Use existing records and the implementation inventory above; no new handoff or
manuscript. If a mathematical falsification check becomes necessary, it needs
an explicit all-S implication, exact predicate, budget and stop decision first.

## Supporting records — consult as needed

| Record | Role |
| --- | --- |
| [DIRECTIVES.md](DIRECTIVES.md) | Standing user rules. |
| [SCOPE.md](SCOPE.md) | Machine-readable active target and approval. |
| [PLAN.md](PLAN.md) | Detailed, unapproved ANCHOR proposal. |
| [PROOFS.md](PROOFS.md) | Exact mathematical statements, proofs and status labels. |
| [FAILED.md](FAILED.md) | Counterexamples and failed mechanisms; check before proposing a lemma. |
| [EXPERIMENTS.md](EXPERIMENTS.md) | Bounded results, timings and reproduction details. |
| [NOTEBOOK.md](NOTEBOOK.md) | Chronological history; old "next" entries do not set the current target. |
| [LITERATURE.md](LITERATURE.md) | Prior results and literature checks. |

Historical/specialized material: `ADVISOR.md`, `E4_MANUSCRIPT.md`, `LIT_CL.md`, `drafts/`, `reviews/`,
`number-theory/`, and `archive/`. These preserve context and do not set current research directions.

## Maintenance

Keep current status, code inventory and next action here; standing orders in DIRECTIVES.md; approval fields in
SCOPE.md. Store proofs, counterexamples and experiments in their existing records and link to them here.
Do not append competing handoffs or duplicate the standing rules across those records.
