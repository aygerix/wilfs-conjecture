# Wilf research — start here

Updated: 2026-10-23 06:30 EDT. This is the single current handoff. Update this page in place at each checkpoint.

## Current status

**ACTIVE: BACKWARDS-WILF**, resumed by the user; exact scope/approval in [SCOPE.md](SCOPE.md).
Fejer is running in us-east1-b on e2-standard-8 after two c2d-standard-8 capacity failures. The startup process check
found no previous research jobs. User also authorized laptop calculations if fejer cannot run.
The specific ANCHOR plan remains **proposed, not automatically approved** by the resumption.

**Goal:** prove Wilf for every numerical semigroup. Q5-only targets have no proved reduction from all semigroups
and are retired as active directions. The old handoff is [archived](archive/STATE_2026-10-21.md).

## Method and standing orders

Read [DIRECTIVES.md](DIRECTIVES.md) for the binding rules. Work backwards from a hypothetical counterexample:
search genuine semigroups for small W, optimize splitting weights, inspect tight constraints and exact dual
obstructions, then extract and prove a parameter-independent lemma. C/C++ is preferred for search and checks;
use a solver where weight optimization needs it. Every target needs an explicit implication chain to full Wilf.
Bounded searches remain evidence. Agent launches each require the user's explicit approval.

## Where the mathematics stands

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

## Current attempt and next action

**Current exact target (E432):** for every genuine canonical tile in c>4m,3e<m at its ACTUAL
conductor phase, bound the maximum weighted Hall deficiency by m. Cell z has positive benefit
beta(z)=1+floor(z.delta/m)+sum_(delta_j<=r(z))z_j; every proper-divisor sink u has capacity
d+|u|. The graph uses immediate parent implications, with2m+2 nodes and O(dm) arcs. A flow
of value at least B-m, B=sum beta, would prove the proposed completion bound Q(E)>=0 for
ALL down-sets E. At E=D it gives W>=Dep+N-kappa_0>=0, hence universal Wilf with the complements.

**Proved versus open:** inversion counts linearize exactly in the selected cells. The source
benefits above are always positive. The minimum completion budget is exactly m+maxflow-B,
and generalized Hall gives its equivalent deficiency formulation. These reductions are paper
proofs, not positivity. The uniform deficiency<=m theorem remains UNKNOWN and is stronger
than the complete-tile support bound, itself stronger than Wilf. A negative proper cut need
not refute Wilf. No reduction from all S to the41 diagnostic profiles is claimed.

**First precise next proof task:** construct the global flow/charge allocation using the COMPLETE
cyclic residue system. The canonical degree allocation respects parent capacities; its unused
amount at a nonmaximal parent is Gamma. The explicit inversion flux cancels eta in the source
balances and leaves1+kappa(z)-sum_(missing directions)I_j(z). Those balances can be negative;
neither construction is asserted feasible under the actual beta source capacities. Resolve
these balances globally, leaving at most m unmatched units. An injection of all remaining
unmatched charges into DISTINCT cyclic residue classes would suffice. Do not assign one free
unit rigidly to each source: the114case has a34-cell witness with Hall deficiency39, failing
that local rule by5. Do not require columns, directions or cells to pay separately.

If the stronger completion claim fails, classify the exact cut and keep the weaker full-tile
payment target; do not abandon the universal goal or assume the stronger auxiliary conjecture
is necessary. Coefficient feasibility, positive recession and accurate reconstruction of an
individual W still do not pay the finite constants. The advisor's warning remains applicable.

**Closed E432 diagnostic:** first principal-upset/value-prefix scans, then exact optimization
over EVERY down-set of the SAME41 existing tiles; all minima nonnegative. These were mostly
already-settled examples, not a new resistant-semigroup census. The small-tile audits independently
enumerate14,52,166 ideals. These are model/algorithm checks, NOT a universal sign argument.
Do not enlarge this positive list; the next work is the uniform capacity proof, not sampling.

Three distinct universal lines stay active: (1) actual primitive boundary and complete cyclic
residue payment; (2) full weighted repair coupling/order ideals (E419/E429/E430); (3) actual
arithmetic/integrality, including E431's integer realization. The current actual-support Hall
route does not assert positivity of the stronger capped certificate or Phi_Z. Keep their
implication directions and weighted counterexamples intact. No fixed height/e/Q5 family target.

**Important earlier corrections:** all36 transport anchors satisfy old SUPP's shape exclusion;
the63 height3 example is also excluded by its residue-aware version. E431 realizes integer
tangent directions exactly and refutes common primitive-lift monotonicity by unbounded drops,
but does not preserve a fractional finite objective's sign under scaling. Retain U=T when
applying the Lean NoWrap result to T=ℕ. One-unit residual caps, source-only/circulation-only
funding and the E430 lo-only payment remain false. Full statements/counters are in PROOFS/FAILED.

**Verification and implementation:** new pure-C modes --partial-support-audit and --support-cut
share the current p39 canonical geometry. The latter exports exact integer flows/cuts and
definition-level source weights; verify_probe.py --completion-cut-check reconstructs the graph,
verifies its positive closed benefit formula, flow/cut equality and selected columns. There
are41 normal exact flow certificates plus3 sanitizer replays, and41 selected-pattern audits;
C ASan/UBSan passes the flow paths and partial geometry. Logs are data/checkpoint_432_checks.log
and data/completion_cut_sanitizer.log. The checks are in run_checks.sh; unchanged264 LP optima
were not rerun merely to inflate this checkpoint. E430/E431 checks remain in that suite.
All E432 general mathematical statements remain paper-proved, not Lean checked. No universal
Wilf proof or genuine counterexample has been obtained. The implementation inventory above
and this section are the single current code/handoff record.

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
