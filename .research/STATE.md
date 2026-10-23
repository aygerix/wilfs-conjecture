# Wilf research — start here

Updated: 2026-10-23 01:47 EDT. This is the single current handoff. Update this page in place at each checkpoint.

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

## Existing implementations

| Code | Purpose | Coverage and dependencies |
| --- | --- | --- |
| [enumh4.c](../src/scratch/p37/enumh4.c) | Direct semigroup enumeration; exact integer W; tight-pair keys. | No Gurobi. Fixed m/e, Kunz <= K, c > 4m, 3e < m; **height >= 4 filter**. |
| [enumlp.c](../src/scratch/p37/enumlp.c) | Same enumeration plus RT2/UA2 optimization and cached LPs. | Gurobi C API for certificate LPs; same height filter. |
| [enumlp3.c](../src/scratch/p37/enumlp3.c) | Newer C enumeration plus RT3/UA3, with optional height filter. | Pass h4only=0 for all heights. Audit found a 256-bit key overflow at m=24; key capacity is now derived from MAXM. |
| [anchgen.c](../src/scratch/p32/anchgen.c) | Genus-bounded tree; ID-q, ANCHOR and CORE1 checks. | No Gurobi; arbitrary heights/depths within finite enumeration and implementation limits. |
| [anchgen_t2.c](../src/scratch/p32/anchgen_t2.c) | Related T2 checker referenced in the proposal. | Audit before reuse. |
| [certprobe.c](../src/scratch/p39/certprobe.c) | Inspect genuine S; RT3/UA3/TX, cone/capped and joint-profile models; export exact-checkable data. | Gurobi C API. `--face` is a CONTINUOUS joint actual/certificate LP with unbounded q>=5; `--face-primitive` reduces only actual-side rows. Neither treats fractional coordinates as semigroups. `--cone`, `--cap`, `--cap-max RES` remain. `--cap-int-max RES` exports an integer feasibility witness without an LP dual; the checker pairs it with a separate real LP bound when available. `--face-free`, `--face-free-oriented`, and `--face-zero-unpaid` are explicitly weaker diagnostics, never full-model counterexample checks. Independent checker: verify_probe.py (now also audits primitive projection and affine boundary rewriting). |
| [upper_scan.c](../src/scratch/p39/upper_scan.c) | Upper closure/assignment, local search, capacity, transport and unpaid-envelope audits. | Pure C. `--weighted-audit` exports real-envelope residual matching; `--integer-weighted-audit` adds floors; `--equality-weighted-audit` counts forced-equal coordinates together. `--combined-climb-wide` tests Phi_Z/c in the existing neighborhood. `--weighted-search` tests the weaker propagation bound. `--interior-unit-search` filters targets to actual cells extendible by every non-multiplicity primitive; the new104case refutes its proposed unit cap. `--cover` is an UPPER certificate, not a Wilf lower bound. |
| [verify_matching.py](../src/scratch/p39/verify_matching.py) | Independent membership, heap Apéry, matching/capacity, equality and transport audits. | `--standalone` needs no Gurobi data. upper_dp.py has rational propagation, `--rigid` closure, and `--chain-budget INPUT MATCHING...` for exact CH/primitive-factorization budgets on audited data. |
| [lattice_cases.py](../src/scratch/p39/lattice_cases.py) | Reproduce the cofactor-shaped adversarial inputs and exact finite parking-tile check. | Diagnostic construction only; no separate family target. `--parking 6` checks all maximal-cell conductor alignments in the recorded tile. |

[Experiment E375](EXPERIMENTS.md) records 108 matching certificate minima against the MILP and C timings of
3.5-6.2 seconds versus 25-55 minutes for tested e = 4 instances. These are previous results, not new benchmarks.
Audit height filters, fixed-size limits and exact certificate coverage before adapting the existing code.

## Current attempt and next action

Completed: 135 exactly rationally certified LP optima on 27 S; independently verified integer assignment
certificates. The simple B>=0 shortcut is false (e=5 example B=-33,W=467); matching raises its bound to347.
Earlier gates and bounded sample counts are in E392; none proves universal certificate positivity.

Local C search improves the credit ratio to1052/1720 at <146,155,175,184>: B=-526,M430,bound334,W1130.
Here full UA3=W; coordinate propagation gives421 after one pass but does not recover the full payment (E395/E397).
The cofactor-shaped construction and its conductor-alignment test are closed as diagnostics; do not enlarge it (E398).

New actual-W search: <43,155,184,193>, c926,W366,matching bound366 (q22,height6). Within B<0 it reaches
<60,71,121,143>, c655,W237,B-111,M150,bound189,UA3=W237. These are local minima only. The simpler
<60,67,71,121> already refutes B>=0 or2W>=c. At <66,67,71,72,98,103,128>, unrestricted cover41 versus
actual-capped42 refutes the nonnegative-unpaid optimal-cover normal form. Exact data: E399/E400.

Latest structural test: all12 saved nonempty cores have genuine positive residual directions. Five
targeted coordinate LPs on saved S each have maximum1, but a fresh C diagnostic stops at candidate12
with an actual maximum2 at residue23 of <153,166,170,317,325,474,617,766,921,925,1080>.
Its c1683,g1013,e11,W5687 and full feasible vector are independently checked. Discontinue unit-weight
counting. A maximal Apéry cell with no tight successor can carry two unpaid units; all maximal elements
and their weights must be retained. No genuine Wilf failure or universal proof has been obtained.

Latest coupling check: no-floor propagation plus residual assignment improves232->236 and176->180
on the two saved60cases. Integer propagation alone captures both increases. On the supplied
<65,82,214,217,265>, integer propagation1402 plus residual matching gives1407; independently audited
real CapUA3=1407. This confirms that individual upper bounds need not be jointly feasible even after
integer propagation. The new stage is a valid strengthening, not a global counting theorem.

New backwards descent (E410): three deterministic local searches find no negative Phi_Z. Two new
local optima are <64,69,77,129,149>,W284,Phi274,c446; and <146,155,184,535>,W1334,Phi990,c2334.
The latter has real/ integer capped optimum998, exactly certified. Its forced-equal class
{76,85,94,103,114,123,132,141} has size8; class-weighted cover raises residual assignment18->22,
giving998. This explains the missing8 as a residue-multiplicity payment, not a uniform positivity proof.

Latest global falsification test: E414 varies actual mu/q AND capped certificate y on each saved tight
profile, fixing only m,largest residue and exact tight pattern; no upper depth/height bound. All31
distinct profile LP minima positive, including180,452,3070/3,998,31,60673/44,5027. Seven actual optima
fractional;24 integral actual optima independently reconstructed. Four changed integer witnesses have
Phi281,128,22,5027. These are regional certificates and diagnostics, not an exhaustive profile list.

**Next mathematical action:** follow the advisor's primitive-coordinate finite-surplus programme.
Use E417's exact projection mJ=H.p-C-e*m*sum x: zero-RHS inner trades, strict affine boundaries>=m,
positive primitive bounds, depth and explicit residue/cap credits. Construct an adaptive global
allocation paying C plus ALL admissible weighted certificate loss, including genuinely weighted
fully extendible interior cells as demonstrated by E421. Retain zero-RHS trades in any matching.
No uniform allocation is proved. The E419 exact transferred budget is now audited coefficient by coefficient; it is not itself the missing inequality.
E416 already settles strict positivity at infinity (3<=e<m); focus on the sign of the FINITE minimum.
E417 canonical corners preserve unit margins by integer rewriting; a further outer-Betti compression
must be justified separately, not inferred just from homogeneous cone equivalence. All composite-parent
certificate rows stay. Do not continue the failed E418 sourcewise sign rule in a,q coordinates or
expand the list of regional certificates. If a full-model negative point appears, separately minimize
the actual objective on the same domain to distinguish integrality from coupling loss. An actual
objective evaluated at the joint optimum is NOT its independently minimized value.

Original Phi_Z>=0 and its equivalent CH budget remain unproved, stronger sufficient targets. Positive
joint CapUA3 minima do NOT imply Phi_Z>=0; these implications must not be reversed. A negative joint
primal needs integer reconstruction before any semigroup/certificate-failure claim. The same universal
backwards strategy/scope remains active; no reduction of all S to these31 profiles is claimed.
The old class-merging-only, collision-only and local/per-direction chain funding rules are closed;
the boundary-only/interior-unit-cap shortcut is now also FALSE. The E420 injection-image rank estimate
is dominated by the old whole-boundary estimate; the false CR-TILE positivity criterion is not revived.
E412/E413 and the older FAILED record explain why. No single-top-ideal size, bounded core, unit cap,
partial-tile deletion or guessed W/c constant. The old10000-candidate sample needs no rerun.
Code and compressed raw data: `src/scratch/p39/` and fejer `~/wilf/p39/`. Full statements are in PROOFS; E390-E393
record earlier checks; E394 records the first two Lean components; E395-E421 record the latest work.
The enumlp3 capacity fix passed sanitizers and an old/new output comparison. `run_checks.sh` is the consolidated
certificate check entry point; it includes all saved LP sets, matching/cover audits and the BASE examples.
Latest consolidated checks pass258 exact LP optima (the212 earlier checks plus46 diagnostic optima),
and2 exact diagnostic rays, plus1 independently feasible integer repair witness. The separate real
LP upper bound certifies its integer coordinate optimum2. Source transfer and boundary packing are
also audited on74 genuine-domain joint points. The2 diagnostic rays have no semigroup reconstruction;
they falsify only the weakened sourcewise-sign model. Primitive projection/boundary rewriting includes
fractional actual coordinates. These checks include
the four new integer witness assignments and existing checks. See the
[validation log](../src/scratch/p39/data/checkpoint_421_checks.log) and data/allowance_lean.log.
The new cone scaling component is kernel checked with the same three standard axioms, no sorry.
New equality/empty-core/integer paths pass C ASan/UBSan; log data/equality_sanitizer.log.
New full/reduced joint-face C paths also pass ASan/UBSan, Gurobi leak detection disabled;
data/joint_face_sanitizer.log. No FULL-model unbounded ray occurred. The diagnostic oriented model now
has2 exact rays; its model-point scaling was checked, with semigroup reconstruction deliberately disabled.
The new free/oriented C branches pass ASan/UBSan, leak detection disabled for Gurobi; checkpoint_418_checks.log.
The new allowance audit checks33,375,552 residue pairs;13 saved S pass exact CH and independent
factorization-count diagnostics. General semigroup consequences and CH budget allocation remain paper/open. The new integer-witness,
zero-unpaid and interior-search C branches pass ASan/UBSan, leak detection disabled, in the checkpoint log.
The interior search stops at sample2045/1798 accepted, seed421; it is a targeted falsification, not
a universal/large-bound verification. Candidate/provenance: data/interior_unit_candidate.jsonl; all new
solver data were consolidated into existing data/allowance_source_probe.jsonl.gz.

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
