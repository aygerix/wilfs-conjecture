# NOTEBOOK.md — dated research log (Wilf's conjecture)

## 2026-10-17 — Session 1

### Orientation
- Exact target: ∀ numerical semigroups S: e·(c − g) ≥ c (S = ℕ: c = g = ell = 0, e = 1, holds).
- Phase 0 done: two independent checkers (E0), literature map (.research/LITERATURE.md, by literature agent;
  key: proved for q ≤ 3, 3e ≥ m, m ≤ 19, genus ≤ 100, ell ≤ 12; W_0 ≥ 0 false at q = 4; D'Anna–Moscariello
  m − 1 ≤ (e−1)n; any counterexample has q ≥ 4, m ≥ 20, 4 ≤ e < m/3, t ≥ e, ...).

### Reformulations (all exact, checked)
- Levels: Wilf ⇔ (d+1)Σ_{w∈Ap}λ(w) ≤ dqm + ρ, λ(w) = ⌊(w+ρ)/m⌋ ("mean Apéry level ≤ (d/(d+1))·q + ρ/((d+1)m)").
  d/(d+1) is the mean degree ratio of a d-simplex: Wilf = "Apéry set is no more top-heavy than a simplex".
- Value form: Wilf ⇔ (d+1)Σ_{w∈Ap} w ≤ d·m·M − (d−1)m(m−1)/2, M = F + m.
- W = ρ + Σ_{w∈Ap} (d·δ(w) − λ(w)), δ = q − λ (depth).

### Main new result of the session: Identity CH (PROVED) — see PROOFS.md
  m·W = Σ_a Def_a + E − (d−1)m(m−1)/2,  Def_a = Σ_{p_a-chains C}|C|(M − top C) ≥ 0,  E ≥ 0.
- Gives a 3-line proof of the homogeneous ("continuous") Wilf inequality (d+1)Σ Ap ≤ d m max Ap, i.e.
  Corollary H: e·n ≥ c − (e−2)(m−1)/2 for all S. (Novelty unchecked.)
- Interpretation: Wilf = discrete divergence theorem on the Apéry down-set + a discrete correction of
  exactly (d−1)m(m−1)/2. The correction is where all difficulty lives.

### Lemma A (PROVED) and Conjecture TOP'' (CONJ, strong evidence)
- Lemma A: m·W ≥ m((d+1)m+d−1)/2 − Σ_{u∈X_q} π(u)(d + ℓ(u)) + Σ_{w∈Ap, w<c} E(w).
- TOP'': Σ_{u∈X_q} π(u)(d + ℓ(u)) ≤ m((d+1)m+d−1)/2. Equivalently
  m + Σ_{u∈X_q} π(u)(ℓ(u) − 1) ≤ e·Σ_{w∈Ap, w<c} π(w), π(x) = ((x − c) mod m) + 1.
  ("Wilf localized to the last two levels, weighted by position").
- Evidence: genus ≤ 24 exhaustive (0 failures, equality exactly when W = 0), 3002 adversarial.
- Structural facts proved along the way: top-layer elements are pairwise incomparable maximal elements of the
  Apéry poset (difference of two would be ≥ m+1 > window); each u ∈ X_q has ℓ(u) ≤ q; for every nonzero
  divisor s of u in Ap, the last-level representative of u − s is a left element, and s ↦ position is injective.

### Failed claims (preserved, with smallest counterexamples)
- COV, COV′ (rigid covering of gaps by e−1 reflected copies of L): ⟨7,9,10,15⟩.
- S1 (positive-part per-direction budget): ⟨7,11,12,20⟩.  TOP_0 (no E): ⟨9,13,14,15,16⟩.
- FLOW (Hall-local TOP''): ⟨10,11,13,19⟩.  SC′ (offset sum): ⟨5,8,9⟩.  X1/X2/X3 per-direction excess:
  ⟨9,10,12,13⟩, ⟨7,11,12,20⟩.
- Lesson: every per-direction or per-element localization of TOP'' fails on small cases although TOP'' holds
  with slack; the directions interact (elements with several factorizations carry the balance via E and ν).

### Open questions generated
1. Exact identity for the TOP'' slack (what does it count?).
2. Does TOP'' reduce in depth (induction on q via adding pseudo-Frobenius numbers in the last level)?
3. q = 2 case of TOP'' is a pure sumset inequality: for A ⊆ [1,N−1], R ≥ 1, B = ((A+A)∖A) ∩ [1,N], k = |A|:
   N + R + Σ_{s∈B}(s+R) ≤ (N+R−|B|)·((k+1)R + ΣA). Prove it (warm-up / pattern for general q).
4. Novelty check for Corollary H.

## 2026-10-17 (late) — from TOP'' to the Carry Lemma (CL) and Tile-CL

### Chain of strengthenings
- Redoing CH with D-columns (monomial-order-minimal factorizations) instead of p_a-chains removes E:
  m·W + (d−1)m(m−1)/2 = Σ_aΣ_C |C|(M − w(top C)) (CH', PROVED). Splitting M − w(top) = m·depth + residue gives
  m·W = m·(depth part ≥ 0) + [Σ|C|·((M − w(top)) mod m) − (d−1)m(m−1)/2]. CL := "bracket ≥ 0" ⇒ Wilf (PROVED).
- CL forgets all depth (Kunz-coordinate) information: it only sees (D, p mod m, M mod m).
- E14: CL holds for every reference residue s, not just M mod m. E15: CL holds for every down-set fundamental
  domain of every lattice with cyclic quotient (no Apéry minimality, no realizability). So CL is a theorem-candidate
  about lattice tiles ("Tile-CL", PROOFS.md).
- E16: the per-direction version PDCL is true for d = 2 but false for d = 3: directions must be coupled.
- E17: dropping "complete residue system" (|D| = m) breaks it even for d = 1. The proof must use Σ_y r(y) = m(m−1)/2.

### Reformulations (all PROVED equivalent; PROOFS.md)
- Walk form: let u(y) = T(φ^{-1}y) − d on ℤ/m in residue order, U its partial sums. Tile-CL(φ) ⇔ max U − mean U ≤ (m−1)/2.
  Tile-CL(−φ) ⇔ mean U − min U ≤ (m−1)/2. Hence (conditional) oscillation of U ≤ m − 1: the column-length mass of
  tops in any residue interval I differs from d|I| by at most m − 1.
- Window form: Φ(t) = Σ_a Σ_{j=1}^{p̂_a}(c_a(t+j) − Ȳ_a) with c_a = a-coordinate as a function of residue. Each window
  sum counts wall-crossings on upward column paths: Φ(t) = Σ_aΣ_x [#{t-walls crossed between x and top_a x} − h_a(x)p̂_a/m].
- Wall form: Σ_y k(y) ≤ σ + Σ_y Σ_a y_a·[r(y) < p̂_a]: "walls below cells (any monotone path from 0) ≤ σ + walls above
  cells along their d columns". Per-wall version (isoperimetric |U_j| ≤ ∂U_j) is false; the sum over walls is needed.
- Continuous analogue reduces to a 1-D statement about the density a(h) of ⟨z,p̂⟩ on D (with Σ_j a(h+jm) ≡ 1):
  μ(σ) ≥ μ̄ − m/2 for the fiber means. PROVED when a is nonincreasing (fiber index mean is monotone in σ). a is not
  monotone in general (boxes), so this is only a guide; and the discrete statement has extra per-direction thresholds.

### Open questions generated
5. Prove Tile-CL for d = 2 (L-shapes): explicit floor-sum computation; does PDCL (true for d=2) have a short proof?
6. Find the cross-direction coupling for d ≥ 3: a potential Ψ on D whose increments dominate Σ_a(window_a) termwise.
7. Is the minimum of f over all tiles of a fixed lattice attained at a Gröbner tile (D_θ)? (would reduce to Apéry tiles)
8. Which test functions g (in place of the sawtooth) satisfy Σ_y T(y) g(σ+φ(y)) ≤ (d+1)Σ g? (cone of valid g)

## 2026-10-17 (night) — proof attempts on Tile-CL; Ramp Lemma; semigroup form of CL

### New PROVED result: Ramp Lemma (all down-sets, no tiling needed) — PROOFS.md
For any finite down-set D ⊆ ℕ^d, β := d+1−T, and any directionally convex ρ (Δ_aρ(u) nondecreasing in every
coordinate of u): Σ_{y∈D} β(y)ρ(y) ≤ |D|·ρ(0).  (Reverse inequality for directionally concave ρ.)
Proof: lex-path decomposition + supermodularity (step 1), trapezoid inequality on each column (step 2).
Special case ρ = (⟨y,q⟩ − K)^+: the "wall excess" E(θ) = β(H_θ) has all tail sums Σ_{θ>K} E(θ) ≤ 0.
Checked numerically (ramp.py): d=2 m≤9, d=3 m≤7, all down-sets, all q ∈ [1,5]^d / [1,4]^3: 0 failures.
What it does NOT give: Tile-CL needs the sawtooth r = ⟨σ+V⟩, which is neither convex nor concave; the AP-sampling
Σ_j E(jm−σ) is not controlled by tail sums alone.

### Exact reformulations found (all equivalent to CL / Tile-CL; derivations in PROOFS.md)
- Semigroup form: CL ⇔ #bad pairs ≤ W, where a pair (s,a), s ∈ L = S∩[0,c), 1≤a≤d, is *good* if
  s + h·n_a ≥ c for h = height of the a-column above the D-cell of s (else bad). Equivalently
  Σ_{a=1}^{d} Σ_{v=c}^{c+n_a−1} x(v)_a ≥ g (x(v) = D-cell of v mod m), and CL ⇔ W ≥ Σ_aΣ_{x∈D} δ(top_a x),
  δ = number of left elements in the class. "Strong CL" (all s): Σ_aΣ_{v=t}^{t+n_a−1} x(v)_a ≥ g for EVERY t.
- Tile form: Σ_aΣ_{j=0}^{p̂_a−1} c_a(t+j) − Σ_y⌊⟨y,p̂⟩/m⌋ ∈ [0, m−1] for every t (two-sided).
- Geometric: Ψ(t) = total column depth at the hyperplane ⟨y,p̂⟩ = t + 1/2 in the periodic tiling, per period
  of K_0 = Λ ∩ p̂^⊥ (there are p̂_a a-lines per period). Tile-CL ⇔ Ψ is within (m−1)/2 of its mean.
- Slack is always an integer in [0,m−1] (divis.py: verified d=2 m≤10, d=3 m≤8); slack(s) + c_0 =
  #{(x,a): top_a x precedes x in the rotated order} ("ascending pairs"), c_0 constant.

### Failed / negative findings this round
- y* (cell whose rotated label equals slack(s)) has no fixed type (ystar.py): not always maximal, sometimes 0.
- Local monotonicity of E on scale m: (U) E(θ) ≤ mean of previous m values would imply the CL side; fails in some
  tiles (d=2 m≥7, d=3 m≥6). (L) the mirror statement fails in almost all tiles (E jumps up at heavy tops).
- Convex-majorant/minorant sandwich of k_σ = ⌊(σ+V)/m⌋: loses a factor ~d; a sufficient "touching at heavy tops"
  condition is already false for d = 1.
- d=2 per-direction data (perdir.py): Σ_a(max U_a − mean U_a) = (m−1)/2 in most d=2 tiles (PDCL tight).

## 2026-10-17 (night, cont.) — cone of test functions, additive cell formula, virtual completion, certificates

### Lean (verified by me: `lake build` OK, 115 PrintAxioms entries all [propext, Classical.choice, Quot.sound], no sorry)
- `lean/Wilf/TileReduction.lean`: `wilfConjecture_of_TileCL : TileCL → WilfConjecture` (commit c043ab4).
- `lean/Wilf/Ramp.lean`: `rampLemma` (Ramp Lemma, any ordered comm ring), concave/equality variants.

### New exact facts (PROVED on paper, numerically re-checked)
1. **Additive cell formula.** For every tile and s:  slack(s) = Σ_{z∈D} γ_s(z),
   γ_s(z) = Σ_a z_a·#{t ∈ [V(z)−p̂_a, V(z)) : t ≡ s} − ⌊V(z)/m⌋  (lift-invariant; Σ_s γ_s(z) = φ(z)).
   On each class r, γ_s is AFFINE in z (slope ε^s(r) − p̂/m).  (gamma.py: 0 mismatches, d=1..2.)
2. **Tents / interval form.** Valid test functions g (Σ_y T(y) g(s−φ(y)) ≥ (d−1)Σg ∀ tiles, s) include all
   cyclically concave g (tents τ_k = discrete Green's functions); tents ⇔ I-TCL:
   |Σ_{t∈I}(Ψ(t) − Ψ̄)| ≤ |I|(m−|I|)/2 for every cyclic interval I. Implied by majorization. (tents.py, cone.py)
3. **Virtual completion (PROVED).** For a partial down-set D' (φ injective), add one new direction b_r with p̂ = r
   and cell e_{b_r} for each missing residue r: the result is a full tile in dimension d + |M|, and its slack is
   Ĝ_s(D') = Σ_{z∈D'} γ_s(z) + #{r ∉ φ(D') : r > s}. So "partial Tile-CL" with this correction ≡ Tile-CL.
   Every tile is reached from the MED tile {0, e_1..e_{m−1}} (slack = m−1−s, a permutation) by replacing
   trivial directions with cells one at a time; each step adds ξ_z = γ(z) − 1_{[0,φ(z))}, which depends ONLY on z.
4. **Landau reformulation.** Majorization slack ≺ (0..m−1) ⇔ slack is the score sequence of a tournament on Z/m
   (Landau 1953) ⇔ a 0/1 matrix rows s, columns z ∈ D, column sums φ(z), row sums slack(s) (Gale–Ryser).
5. c0 identity: slack = #{(x,a) : s ∈ [φ(x), φ(top_a x))} − c0 with c0 = Σ_y ⌊Σ_a ⟨y_a p_a⟩/m⌋ ∈ [0, E],
   E = #pairs − (m−1); column reflection pairs (x,a) ↔ (ρ_a x, a) with arc length φ((ρ_a x)_a e_a).

### Falsified (preserved)
- **P-TCL** (0 ≤ Σ_{z∈D'}γ_s(z) ≤ |D'|−1 for partial down-sets): FALSE. Smallest: d=2 m=7,
  D' = {00,01,02,10,11,20}, p=(2,3), G = [2,2,4,6,4,2,0] (6 > 5). All violations by exactly 1. (ptcl.py)
  Corrected version (RP-TCL, fact 3) holds: d=2 m≤10, d=3 m≤7 exhaustive; partial majorization too (pmaj.py).
- **Monotone contraction along build-ups** (slack(D_{k+1}) ≺ slack(D_k) in V/deg/lex order): FALSE (chainmaj.py).
- **Arc certificates** (A_z an arc of length φ(z)): impossible when Σ_y (d−T(y))^+ > m−1 (e.g. every 3×4 box):
  arc starts minus ends at s equal d − T. Even **fractional** arc certificates (any rotations) FAIL:
  d=2 m=8, D = 3×3 minus {22}, p=(5,7), slack=[7,4,3,0,2,4,3,5]: slack(0)=m−1 forces all arcs ∋ 0,
  slack(3)=0 forbids 3, so coverage would be unimodal on {4..7,0,1,2} but it is not. (fraccert*.py, grcheck.py)
  A non-arc Gale–Ryser certificate exists (unions of disjoint pair-intervals, see below).
- slack = S^a (direction-a arc family) for some a: holds in many small tiles but not all (dirfam.py).

### Perfect tiles (V: D → [0,m) bijective; e.g. 3×3 minus corner with p̂=(3,1))
- slack(s) = X_s = #{(x,a): V(x) ≤ s < V(top_a x)} (single cut). Window form: X_s = Σ_a Σ_{j=1}^{p̂_a} c_a(s+j),
  c(t) = V^{-1}(t). Tile-CL here ⇔ X_s ≤ m−1. In the m=8 example a certificate groups pair-intervals so that each
  group's differences sum to one cell z (bijectively) with disjoint intervals; it permutes which column's pair is used.

### Next
- Perfect-tile single-cut lemma X_s ≤ m−1 (clean, no modular arithmetic): attempt a direct proof.
- Certificate structure: "one pair per (cell, direction), columns permuted within each (a, height)" — test existence.

## 2026-10-17 (night, 3) — LP tightness, wall-sum formula, single-cut lemma, Apéry lifts, Base-CL

### LP relaxation (dslp.py, dslpbox.py; exact rational simplex src/scratch/exactlp.py)
max/min Σ_z γ_s(z)x_z over fractional down-set transversals (class sums 1, x monotone).
- Region R = {z : Π(z_a+1) ≤ m}: LP value = m−1 / 0 (tight) for d=2 m≤10; NOT tight for d=3 (m=5: 13/3, min −1/3;
  m=6: 21/4, min −1/4).
- Box-injective region R'(p) = {z : φ injective on [0,z]}: tight (max m−1, min 0) for d=3 m=5,6,7 and d=4 m=5,6.
  So for every (d,m,p,s) tested there is a dual certificate (u on Z/m, flow f ≥ 0 on edges of R'):
  u_{φ(z)} + in(z) − out(z) ≥ γ_s(z), Σu = m−1. Min-flow duals (dualbox.py) have no visible closed form
  (u takes negative values; e.g. d=2 m=9 p=(1,4)). OPEN: a structured dual family.

### Wall-sum formula (PROVED, any positive lift p̂)
With E_t = {z ∈ D : V(z) ≤ t}, U_t = D∖E_t, F(E) = #{(w,a): w ∈ E, top_a w ∉ E} = Σ_{y∈E}(d − T(y)) (any down-set E ⊆ D):
    slack(s) = m − 1 − s + Σ_{j≥0} [F(E_{s+jm}) − |U_{s+jm}|]          (s ∈ [0,m)).
Proof: γ_s(z) = Σ_{walls t≡s, t<V(z)} (w_t(z) − 1) with w_t(z) = Σ_{a: V(z)−p̂_a ≤ t} z_a, and Σ_j|U_{s+jm}| = K + m−1−s
with K = Σ_z⌊V(z)/m⌋. Equivalently slack(s) = Σ_{r>s}(T(c(r)) − d) − Σ_y β(y)⌊V(y)/m⌋, and
**Wilf direction (slack ≥ 0) ⇔ X(s) := Σ_j F(E_{s+jm}) ≥ K**: depth-weighted crossings of the walls ≡ s are at least
the number of (cell, multiple of m below it) incidences. For perfect tiles K = 0 (trivial); only the upper bound has content.

### Single-cut lemma (SCL) — CONJ, implied by Tile-CL; tested
SCL: D' any finite down-set, p̂ ≥ 1 with V injective on D', E = D'∩{V ≤ θ}: F(E) ≤ θ + |D'∖E|.
(Implied by Tile-CL via virtual completion with m > max V.) scl.py: d=2 N≤8, d=3 N=6, all weights ≤ 7/5: 0 violations.
Reduction (PROVED): worst case is D' = E ∪ ∂⁺E with E = {y ∈ ℕ^d : V(y) ≤ θ} (adding a boundary cell b raises
F − |U| by Σ_{a: b−e_a∈E} b_a − 1 ≥ 0). Sweep identity (PROVED, p̂_1 < … < p̂_d, V injective on E∪∂⁺E):
    d|E| − |∂⁺E| = Σ_{y∈E} top(y),  top(y) = max{a : y_a ≥ 1}, top(0)=0.
So **XSCL ⇔ Σ_{t ∈ S∩[1,θ]} rank(t) ≤ θ**, S = ⟨p̂⟩, rank(t) = least b with t ∈ ⟨p̂_1..p̂_b⟩ (unique factorization
up to θ + boundary). xscl.py: 4000 random p̂, d ≤ 5, weights ≤ 80, all θ in the injective range: max excess 0 (tight often).
d=2 PROVED: rank-2 elements t = iα+jβ map injectively to gaps via t ↦ (J+1)β − α − t (J = ⌊θ/β⌋), with a fix-up into the
class of (J+1)β when θ ≥ (J+1)β − α.
Recursion (PROVED): XSCL_d ⇔ Σ_{k≥0} G'_{d−1}(θ − kα) ≤ #gaps of S in [1,θ] (α = p̂_1, G' = the d−1 dim
analogue for p̂_2..p̂_d) — a MULTI-wall statement one dimension down with modulus α. So "single wall in dim d" is
as hard as "multi-wall in dim d−1": no free induction.

### Every tested tile is an Apéry tile (aperylift.py) — OBSERVED
For each tile (D,p) there is k ≥ 0 with ⟨λ,k⟩ > 0 for all exit vectors λ = z+e_a − z' (z a-top, z' ≡ z+e_a in D):
d=2 m≤10 (all 462 tiles), d=3 m≤7 (all 624). Then p̂ = p + Nmk (N large) gives V(D) = Ap(⟨m,p̂⟩, m).
Consequence: Tile-CL ≡ "strong CL" for numerical semigroups with arbitrary generating sets and down-set
factorization tiles; CL for S itself only needs s* = φ(argmax_D V) (the Frobenius class).
OPEN: prove it (is every down-set fundamental domain of a cyclic-quotient lattice a Gröbner/weight staircase?).

### Ramp route for CL (PROVED sufficient condition; rampstair.py)
CL at s* ⇔ Σ_y β(y)ρ(y) ≤ mρ(0) for ρ = ⌊(V + σ*)/m⌋, σ* = m−1−s*. If ρ is directionally convex on D for some
Apéry lift, CL follows from the Ramp Lemma. Holds for some Apéry lift in 30/126 tiles (d=2 m=9), 102/126 (d=3 m=6, lifts in
[0,2]^3): a genuine proved subfamily, not the general case.
Exact Ramp decomposition (PROVED, residue-only): m·(Σβ R) = T1 + T2 with R = ⟨φ+σ⟩,
  T1 = Σ_aΣ_C L_C R(base_C) − (d−1)m(m−1)/2 (lex/supermodular part), T2 = Σ_C[2Σ_{c∈C}R(c) − L_C(R(base_C)+R(top_C))]
(column-trapezoid part; T2 = 0 if all columns have length ≤ 2). Observed: T1 ≥ 0 ALWAYS, T2 often negative.

### Base-CL — NEW CONJ (basecl.py, topbase.py): the reversed-orientation twin of Tile-CL
    base-slack(σ) = (Σ_aΣ_C L_C⟨φ(base_C)+σ⟩ − (d−1)m(m−1)/2)/m ∈ [0, m−1], always an integer.
Verified d=2 m≤9, d=3 m≤7 (all tiles, all σ). Equivalent forms (PROVED):
- inversion form: #{(x,a) : R_σ(base_a x) > R_σ(x)} is within (m−1)/2 of its mean (Top-CL: #{(x,a): R_σ(top_a x) < R_σ(x)});
- carry form: base-slack = σ + Σ_{x∈D}(k(x) − C(x)), C(x) = ⌊(σ + Σ_a⟨x_a p_a⟩)/m⌋ (carries),
  k(x) = #{a : ⟨x_a p_a⟩ > ⟨φ(x)+σ⟩};
- Ramp form: Σ_y α(y)⌊(σ + Ṽ(y))/m⌋ ∈ [σ−m+1, σ], α = Λ − (d−1), Λ(y) = Σ_{a: y_a=0} L_a(y), Ṽ(y) = Σ_a⟨y_ap_a⟩;
  "Base Ramp Lemma" (PROVED): Σ_y α(y)ρ(y) ≤ mρ(0) for every ρ with Δ_aρ nondecreasing in all coordinates b ≠ a
  (no convexity in the own direction needed — only step (1) of the Ramp proof).
Base-CL is Tile-CL for −D (column-convex tile oriented the other way). Its slack vectors are NOT relabelings of top
slack vectors (topbase.py: different shape sets).
**Orientation obstruction (FALSE, preserved):** "Column-CL" for orthogonally convex tiles fails in general
(non-integral slack, out of range from m=4), and for MIXED orientations (tops on the staircase in one direction, on the
flat side in the other) it fails at d=2 m=9: D = column of height 7 with a 2×2 block on top
(rows: ##,##,#.,#.,#.,#.,#.), p=(2,1): slack = 73/9 > 8; p=(7,8): slack −1/9 (colcl2.py, mixedex.py).
Only consistent orientations (all tops at the staircase = Tile-CL, all at the flat side = Base-CL) survive.

### Strategic note
Every route so far reduces to the same coupling: the depth-weighted crossings of several walls (≡ s mod m) must be
controlled jointly. New handles this round: (i) Wilf direction = "X(s) ≥ K" (crossings vs. multiples of m below cells);
(ii) the two-orientation symmetry (Top/Base) — a proof should explain why consistent orientation is needed;
(iii) LP duality on R'(p) is tight through d=4 m=6.

## 2026-10-17 (night, 4) — tail pairing, GTP / AP-Ramp, column-threshold formula

### Strengthening that survives every test: AP-Ramp (= GTP) — CONJ
τ(t) := β(D ∩ {V > t}) (β-mass above level t), A(t0) := Σ_{j≥0} τ(t0 + jm) = Σ_y β(y)⌈(V(y) − t0)/m⌉⁺.
    **AP-Ramp:  A(t0) ≤ (m − 1 − t0)⁺  for every integer t0 ≥ 0, every tile, every positive lift.**
- t0 ∈ [0,m): exactly the Wilf direction of Tile-CL at s = t0 (slack(s) = m−1−s − A(s)).
- t0 ≥ m: NEW: AP-sampled β-tails are ≤ 0 (the Ramp Lemma gives this only for the full sum Σ_{t≥K} τ(t)).
- Pointwise τ(t) ≤ 0 for t ≥ m−1 is FALSE (taupos.py: d=2 m=6 std lift 2 cases; many for larger lifts; d=3 m=7: 18):
  the AP sampling across periods is essential.
Equivalent (PROVED) forms:
- Hall/matching form (GTP): for every θ ≥ 0, Σ_{t≡s, t≥θ} F(E_t) ≥ #{gaps of S_D = V(D)+mℕ in [θ,∞)}, i.e. gaps can be
  matched injectively UPWARD to depth-weighted wall crossings (crossing level ≥ gap level).
- tail-pairing form (TP): Σ_{j≥J} F(E_{s+jm}) ≥ Σ_z (⌊V(z)/m⌋ − J)⁺ for all J (per-wall version P1 is FALSE).
- semigroup form (Apéry lift): Σ_{u > t0, u ∉ m+S} β(class of u) ≤ (m − 1 − t0)⁺, where ℕ∖(m+S) = gaps ∪ Ap(S,m)
  = ⊔_k (Ap − km)∩ℕ ("shifted Apéry layers").
Evidence (exact integer arithmetic): wallpair.py/tailpair.py (d=2 m≤10, d=3 m≤7, lifts k∈[0,2]^2, [0,1]^3: 0 failures);
gtp.py (all thresholds θ: d=2 m≤10, d=3 m≤7, d=4 m≤6, d=2 lifts [0,2]^2 m≤7: 0 failures; intermediate thresholds are
often tight, e.g. 174 cases at d=3 m=7); apramp.py (all t0: d=2 m≤9 lifts [0,1]^2, d=3 m≤7, d=3 m≤6 lifts [0,1]^3: max
excess exactly 0).
Why it matters: a statement indexed by a continuous-looking parameter t0 (all levels) with a Hall interpretation; the
Ramp Lemma's proof is a level-raising bijection Ψ (below), so AP-Ramp is "Ramp with residue bookkeeping".

### The Ramp Lemma as a level-raising bijection (PROVED)
Ψ: {(x,u): x∈D, 0≤u<V(x)} → {(w,a,u''): V(w) ≤ u'' < V(top_a w)}: for u in the a-th lex segment [V(x^{(a−1)}), V(x^{(a)}))
of x, set w = reflection of x in its a-column, u'' = u + V(top_a x) − V(x^{(a)}) ≥ u. Ψ is a bijection (step 1: lex
segments → column segments below x, translation up; step 2: column reflection c_i ↦ c_{L−1−i}). Hence Σ_{t≥K}(|U_t| −
F(E_t)) ≤ 0 for all K (Ramp for ramps), combinatorially. For AP-Ramp, each translated segment pair (length ℓ = x_a p̂_a)
carries ⌊ℓ/m⌋ or ⌈ℓ/m⌉ AP points on each side; the defect e(x,a) ∈ {−1,0,1} sits at the TOP AP point of the segment, so
AP-Ramp ⇔ an upward Hall matching of the e = −1 "demands" to the e = +1 "spares" (plus allowance (m−1−t0)⁺).
Per-cell residue-preserving versions of step 1 are impossible (Σ_a⌈(ℓ_a−δ)/m⌉⁺ < ⌈(Σℓ_a−δ)/m⌉⁺ can happen).

### Column-threshold formula (PROVED; colthresh.py: 0 mismatches d=2 m≤8, d=3 m≤6)
For an a-column C of length L_C let H_C(t) = #{1 ≤ i < L_C : ⟨i p_a⟩ ≥ t}. Then
    slack(s) = Σ_C [ H_C(τ_C) − H_C(κ_C) ],   τ_C = ⟨φ(top_C) − s − 1⟩ + 1,  κ_C = m − ⟨Σ_{b>a}(base_C)_b p_b⟩.
(Σ_C H_C(τ_C) = #arcs [φ(w), φ(top_a w)) containing s; Σ_C H_C(κ_C) = c0 = Σ_x ⌊Σ_a⟨x_a p_a⟩/m⌋ = total carries,
computed in the order a = d, d−1, …, 1; any order π of directions gives another decomposition of c0.)
Both terms are upper-tail counts of the same multiset {⟨i p_a⟩ : 1 ≤ i < L_C}, so a column contributes ≥ 0 iff τ_C ≤ κ_C
(effectively). Localization tests (colthresh2.py): per-column negative in ~1–2% of columns; per direction with lex order
direction 1 is negative in 79/1134 (d=2 m=9) cases, the last direction never (κ = m); "some order π makes every direction
≥ 0" holds for all d=2 m≤9 and d=3 m≤6 but FAILS in 6/3108 cases at d=3 m=7. So no order-based localization proves it.

## 2026-10-17 (night, 5) — covering pairs, transport views, Base-CL for d = 2, boxes, τ-class decomposition

### Clean equivalent forms (PROVED, elementary)
- β-positivity: Tile-CL (Wilf direction) ⇔ Σ_{y∈D} β(y)·⟨σ + φ(y)⟩ ≥ 0 for every σ (increasing labeling).
  Both bounds of Tile-CL for all tiles ⇔ this for all tiles, since slack_{−p}(−1−s) = m−1−slack_p(s) (walk increments cancel).
- Transfer form: slack(s) = Ψ(s+1) − K, Ψ(r) = Σ_a Σ_{k=0}^{p̂_a−1} c_a(r+k) (c_a(r) = a-coordinate of φ^{-1}(r)); T − d is a
  τ_1-coboundary on the torus and Ψ is its transfer function.
- Semigroup form: CL ⇔ Σ_{u ∈ L} β(x(u)) ≥ c  (L = left elements, x(u) = factorization cell of u's class); ⇔ Σ_a |R_a| ≥ g,
  R_a = {u ∈ L : the a-run u, u+n_a, … inside the D-column reaches ≥ c}. (Wilf is the same with R_a replaced by L.)
- Arc/transport form: slack(s) = N(s) − c0, N(s) = #column arcs [φ(x), φ(top_a x)) ∋ s. Equivalently the min-cost clockwise
  transport from supply d·1 to demand T on ℤ/m costs ≤ m(m−1)/2; the column plan costs m(m−1)/2 + m·c0.

### Covering-pair certificate PCL (s-independent strengthening) — d=2 TRUE in tests, FALSE in general
PCL: the multiset of column arcs contains c0 pairwise disjoint pairs, each pair covering ℤ/m (⇒ N(s) ≥ c0 for all s).
coverpairs*.py: d=2 m≤10, d=3 m≤7, d=4 m≤7: TRUE; pairs from different directions suffice for d=2.
FALSE at d=3 m=8 (6 tiles): D = {0,1}^3, p = (2,3,4), c0 = 1 — every arc has length ≤ 4, no pair covers (a triple does).
Restricted versions FALSE: same-direction pairs; head-to-tail pairs (d=2 m=8); "ABOVE"/"BELOW" types; line pairs
(start cells differing in one coordinate) FALSE at d=3 m=8 (12 tiles).
### Monotone mechanisms FALSE (the proof must use the torus wrap-around)
- Monotone transport (each unit goes to a top ≥ its cell): FALSE, d=2 m=8, D = 3×3 minus (2,2), p = (5,7): min cost 36 > 28.
- Monotone gap routing (gap of class x ↦ a straddling column edge on a monotone path 0→x): FALSE (406/1134 at d=2 m=9).
- LocCL (carries of x absorbed by arcs in columns through x): FALSE already for the 2×2 box, p = (2,3), s = 1.

### Base-CL for d = 2 — PROVED
Carry form (re-derived): base-slack(σ) = σ + Σ_x G(x), G(x) = #{a : ℓ_a(x) > r(x)} − ⌊(σ + Σ_aℓ_a(x))/m⌋,
ℓ_a(x) = ⟨x_a p_a⟩, r(x) = ⟨σ + φ(x)⟩. [Σ_a r(base_a x) − (d−1)r(x) = σ + m(k(x) − C(x)) since r(base_a x) = r(x) − ℓ_a(x) + m[ℓ_a > r].]
For d = 2 and ANY ℓ_1, ℓ_2 ∈ [0,m), u := m − σ: G ∈ {−1,0,1}; G = 1 ⇔ ℓ_1, ℓ_2 < u ≤ ℓ_1+ℓ_2, forcing r ∈ [0, u−2];
G = −1 ⇔ ℓ_1, ℓ_2 ≥ u and ℓ_1+ℓ_2 < m+u, forcing r ∈ [u, m−1]. r is a bijection D → [0,m), so
−σ ≤ Σ_x G ≤ u − 1, i.e. base-slack ∈ [0, m−1]. ∎  (basecheck.py confirms the carry form, 0 mismatches.)
For d ≥ 3 the per-cell bound FAILS: cube {0,1}^3, p = (1,2,4), m = 8, σ = 1: G(1,1,1) = 2 at r = 0 (Base-CL still holds).
The pure lemma "distinct subset sums of ℓ ⇒ |G| ≤ 1" is FALSE (glemma.py, ℓ = (1,2,4), m = 8, σ = 1).

### Tile-CL for box tiles = Base-CL for box tiles (PROVED, any d); hence Tile-CL holds for all 2-dim box tiles
x ↦ κ − x (κ = far corner) maps a-columns to a-columns, tops ↔ bases: slack_Tile(s) = base-slack(s − φ(κ))
(basecheck.py: 0 mismatches on 2- and 3-dim boxes). With Base-CL(d=2): Tile-CL holds for every rectangle tile.

### τ-class decomposition (PROVED identity; tauclass.py 0 mismatches d=2 m≤9, d=3 m≤7)
τ(x) := (t_1(x),…,t_d(x)), t_a(x) = a-coordinate of top_a x; X_τ = {x : τ(x) = τ}. With ℓ'_a(x) = ⟨(t_a(x) − x_a)p_a⟩,
ρ_x = ⟨s − φ(x)⟩, Ĝ(x) = #{a : ℓ'_a(x) > ρ_x} − ⌈(Σ_a ℓ'_a(x) − ρ_x)/m⌉:
    slack(s) = Σ_τ [ Σ_{x∈X_τ} Ĝ(x) + |X_τ|·⟨s − φ(τ)⟩/m ].
Ĝ(x) is the Base-CL per-cell function of the reflected point τ − x with offset e_τ = ⟨φ(τ) − s⟩. One class ⇔ box.
Per-class nonnegativity FALSE (classes interact). For d = 2 (Ĝ ∈ {−1,0,1}, Ĝ = −1 ⇒ ρ_x ≥ e_τ ≥ 1) Tile-CL follows from
**CDL (class discrepancy, d=2):** #{x ∈ D : ρ_x < e_{τ(x)}} ≥ (1/m)Σ_x e_{τ(x)}, i.e. Σ_τ |φ(X_τ) ∩ (s−e_τ, s]| ≥ Σ_τ |X_τ|e_τ/m.
lshape.py: CDL holds for all d = 2 tiles m ≤ 10. L-shape classes: Q = [0,a')×[0,b') (τ = (a−1,b−1) ∉ D), R_1 = [a',a)×[0,b')
(τ = (a−1,b'−1)), R_2 = [0,a')×[b',b) (τ = (a'−1,b−1)); φ(a−1,b−1) = φ(a−1,b'−1) + a p_1 = φ(a'−1,b−1) + b p_2.
OPEN: prove CDL for L-shapes (gives Tile-CL for d = 2, i.e. CL for every 3-generated semigroup); Base-CL for d ≥ 3.

## 2026-10-17 (night, 6) — Base-CL for all boxes (Hajós induction); **CL and Tile-CL are FALSE**; pivot to TOP''

### Theorem (Base-CL, hence Tile-CL, for every box tile in every dimension) — PROVED (uses Hajós's theorem, CITED)
D = Π_a [0,k_a), m = Π k_a, φ bijective. With C(x) = ⌊(σ + Σ_a ℓ_a(x))/m⌋ (ℓ_a = ⟨x_a p_a⟩) and G as in the carry form:
1. Face formula (G(x) = #{a : C(x − x_a e_a) = C(x) − 1} − C(x), each difference ∈ {0,1}):
   ΣG = (d−1)·Σ_D C − Σ_a k_a·Σ_{F_a} C,  F_a = {x_a = 0}.
2. Hajós (1941; factorizations of finite abelian groups into cyclic subsets): Z/m = ⊕_a {0, p_a, …, (k_a−1)p_a} forces
   some factor to be a subgroup, wlog {j p_1 : j < k_1} = nZ/mZ with n = m/k_1.
3. Hermite: Σ_{i<k}⌊(Z + i n)/m⌋ = ⌊Z/n⌋. So every C-sum over full 1-lines becomes ⌊(σ + Λ'(x'))/n⌋, Λ' = Σ_{a≥2} ℓ_a.
4. Reduce mod n: box' = Π_{a≥2}[0,k_a) with p_a mod n is a box tile of Z/n. Write ℓ_a = ℓ_a^{(n)} + n q_a and σ = σ_n + n q_σ.
   The linear terms q_a cancel in (d−2)Σ − Σ k_a Σ_{F'_a}; the constant gives −n q_σ.
5. ΣG(σ) = ΣG'(σ_n) − n q_σ + Σ_{x'∈box'} ⌊⟨σ + Λ'(x')⟩_m / n⌋, where the last sum has n terms, each in [0, k_1 − 1].
   Induction (ΣG' ∈ [−σ_n, n−1−σ_n]; d = 1 gives G ≡ 0) yields ΣG ∈ [−σ, m−1−σ]. ∎
Check: hajos.py (E50) — the identity of step 5 has 0 failures on all boxes with d ≤ 4, m ≤ 16, all p, all σ.
**Scope remark:** a box Apéry tile means S is symmetric. The map w ↦ w_κ − w preserves Ap, so Ap has a unique ≤_S-maximum.
So this theorem only reaches a family where Wilf is trivial. Its value is the mechanism: a Hajós subgroup factor plus
Hermite's identity gives an exact induction on dimension.

### CL and Tile-CL are FALSE (E47; examples/CL_counterexample.md) — decisive for the main route
S = ⟨14,22,23,57,61,62,63⟩ (Eliahou's W0<0 example ⟨14,22,23⟩ ∪ [56,∞)) has c = 56, g = 43, e = 7, W = 35. Facts:
- Every Apéry element has a unique factorization.
- The tile is D = Δ_3 ∪ {4 spikes}, with p = (8,9,1,5,6,7) mod 14.
- CL: LHS = 441 < 455 = target, so slack(M mod m) = −1. Wilf is carried entirely by the depth part (36).
- Check: independent brute force (clverify.py) for every monomial order.
- E47 also shows violations of the Tile-CL upper bound.
Consequences:
- Tile-CL ⇒ CL ⇒ Wilf has a false premise. The route "prove Tile-CL" is CLOSED.
- AP-Ramp/GTP is CLOSED too: at t0 ∈ [0,m) it is the Wilf direction of Tile-CL.
- PCL, CDL-for-general-d and all other strengthenings of Tile-CL are dead as routes to Wilf.
- The d = 2 results (Base-CL, rectangles, τ-classes) and the box theorem stay TRUE but only cover e = 3 and symmetric S.
Spike mechanism (spikes.py, E51):
- A direction a whose only cells are 0 and e_a contributes m[s < p̂_a] − p̂_a to m·slack(s).
- So any injective core plus spikes on the missing residues is a tile, which lets the E17 failure (CL for injective φ) propagate.
- The first spiky failure is at m = 14 (core Δ_3).
Why the exhaustive tile tests missed it: they covered d = 4 only up to m ≤ 8 and d = 3 only up to m ≤ 11. The failures need many spikes and m ≥ 14.

### Regime split (E48) and the surviving inequality TOP'' (E49)
- **Regime 3e < m (4000 S, seed 7):** CL at the reference residue 0/1664 failures, Tile-CL (some s) 9 failures. All CL(ref) failures so far have 3e ≥ m, where Wilf is a theorem (LITERATURE #21, Eliahou EJC 2020).
- **TOP'' (5005 hard S, seed 11):** 0 failures, while CL(ref) fails on 7 of the same S. TOP'' is strictly more robust.
  Its minimum normalized slack is 0.0225, attained with W = 1.
  Lemma A + TOP'' ⇒ Wilf is LEAN-checked (wilf_of_TOP2).

### Strategic review (mandatory after a major obstruction)
- **Distance:** the single gap of the main route (G-CL) was refuted. Proof work on Tile-CL produced true theorems that do not reach Wilf.
- **Lesson:** residue-only (depth-free) statements are false once d is large: spikes cost m·[s < p̂] − p̂ with no compensation.
  A true route must use depth (actual Apéry values). Two such statements exist:
  (a) TOP'' (top layer + shortest factorization lengths, depth through π(u) = u − c + 1);
  (b) CL(ref) restricted to 3e < m and c > 3m, combined with the theorems #13 (c ≤ 3m) and #21 (3e ≥ m).
- **Kill:** Tile-CL in general, AP-Ramp/GTP, PCL, CDL for L-shapes (it would only yield CL for e = 3).
- **Continue:** (1) TOP'' as the main line; (2) the hybrid CL(ref) for 3e < m; (3) a new depth-aware mechanism.
- **Bias check:** the last ~15 attempts were all residue-level reformulations of one statement. The adversarial
  semigroups (E5b/E6b) had been run for TOP'' but never for CL; that test would have saved this branch.
- **Procedure change:** every new candidate inequality must pass `src/exp_cl_adv.py`-style adversarial semigroups
  (W0<0 family, Backelin, Delgado, deep truncations) BEFORE any proof effort.

## 2026-10-17 (night, 7) — depth-aware repair: SR-CL, DR-CL, **Tile-TOP''** (new main conjecture)

### What the CL failure needs: spikes
A *spike* of a tile is a direction b with {x ∈ D : x_b ≥ 1} = {e_b}. Every high generator (n_b ≥ c) is a spike. A spike's
columns are {0, e_b} and singletons, and its exact contribution to Σ_C|C|(M − V(t_C)) is K − n_b with K = mℓ + m(m−1)/2.
- CL loses exactly m(ℓ − q) per high generator (q = ⌈c/m⌉). The counterexample has 4·14·9 = 504 = 14·36, i.e. the whole depth part.
- Facts: all CL(ref) failures in 10,009 S have high generators. CL-H (CL + d_high·(ℓ − q)) has 0 failures (clh.py, two seeds).

### SR-CL (spike-relaxed Tile-CL) — CONJ, implies Wilf (PROVED implication)
SR-CL: slack(s) ≥ −σ(D) for every tile and s, where σ(D) = number of spike directions.
Proof that it implies Wilf:
- Every spike direction b has depth Σ_{y≠0}δ(y) + δ(e_b) ≥ ℓ − q.
- If ℓ > q, then W = depth + slack(s_M) ≥ σ + slack(s_M) ≥ 0.
- If ℓ = q, then S = mℕ ∪ [c, ∞), so e = m (or m = c) and Wilf is trivial. ∎
Evidence: 0 failures on 8005 adversarial Apéry tiles (srcl.py seeds 11, 1). Spike-free Tile-CL has 0 lower-bound failures there too. Worst min-slack/σ ≈ −0.42.
Double spikes ({e_b, 2e_b}) plus spikes plus a core of dim ≤ 2: 0 SR-CL failures for m ≤ 13, about 90k tiles (dspikes.py).

### DR-CL and Tile-TOP'' — CONJ, both imply Wilf (PROVED implication; Lean in progress)
Key observations:
- If t ∈ D is not maximal (t + e_b ∈ D), then V(t) + n_b ≤ M, so M − V(t) ≥ n_b > m: every column with a non-maximal top has depth ≥ 1.
- A maximal y tops every column through it, so T(y) = d + |y|.
Hence, from CH',
   m·W + (d−1)M' ≥ Σ_{y max} T(y)⟨s_M − φ(y)⟩ + m·Σ_{C: non-max top}|C| = d m² − Σ_{y max}(d+|y|)(m − ⟨s_M − φ(y)⟩).

**Tile-TOP'':** for every tile (D,p) and every s ∈ ℤ/m,
   Σ_{y ∈ max D} (d + |y|)·π_s(y) ≤ m((d+1)m + d − 1)/2,  π_s(y) = m − ⟨s − φ(y)⟩ ∈ [1,m].
Clean form (tiles; positions are a bijection D → [1,m]): **m + Σ_{y max}(|y| − 1)π(y) ≤ (d+1)·Σ_{z non-max}π(z)**.
Properties:
- Tile-TOP'' ⇒ DR-CL (slack(s) ≥ −Dep(D), Dep = Σ over columns with non-maximal top of |C|) ⇒ Wilf.
- Tile-TOP'' at s_M is TOP'' with every maximal cell (not just X_q) on the left, so it is stronger than TOP'' and lift-free.
- Spikes have |y| = 1: they drop out of the left side and only raise d. This is why Tile-TOP'' survives where CL fails.
- Max over s: LHS(s) is a walk with drift −T(A) and up-jumps m·T(y) at maximal residues. The max is at s = φ(y0) for a maximal y0.
  In a semigroup, y0 = cell(max Ap), which is the CL/TOP'' reference.
  Equivalent: ∀ y0 ∈ max D: Σ_{y∈max D∖y0} T(y)⟨φ(y0) − φ(y)⟩ ≥ m(T(A) − ((d+1)m + d − 1)/2). So maximal residues cannot cluster below φ(y0).
- Tight: the column (d = 1) and the simplex {0, e_1, …, e_d} (m = d+1). These are the e = 2 and T_{m,q} equality cases of Wilf.
Evidence:
- tiletop.py: 0 failures on ALL tiles for d=2 m≤13, d=3 m≤10, d=4 m≤8, d=5 m≤7 (all p, all s).
- tiletop_adv.py: 0 failures on 8008 adversarial Apéry tiles; slack 0 only at simplex-like tiles.
- The rearranged, residue-free version R-TOP is FALSE (⟨7,15,16,17⟩ ∪ [28,∞), ⟨7,11,12,13⟩ ∪ [18,∞)). Residue structure is essential.
- The injective generalization holds as well (injtop.py, injtop2.py; ~1.2M cases): for every down-set D with φ merely injective and
  every s, (A) Σ_{y max}(|y|+1)π(y) ≤ m² + (d−1)Σ_{z non-max}π(z) and (B) the original form. The tightest cases are non-tiles with
  |D| = m − 1 (e.g. d=3, m=8, D = {000,001,002,010,100,101,200}: slack 5).
- Staircases Δ_k embed injectively only for m ≳ 1.3–1.5·|Δ_k| (Δ_5 first at m = 19; Δ_6, …, Δ_9 never within |Δ_k|+6). This is a geometry-of-numbers effect
  (Λ ∩ (D − D) = {0}, Minkowski), and the slack is then positive.
  **Mechanism hypothesis:** the packing condition forces maximal cells' residues to spread; the proof should use it.

### Strategic note
Main conjecture now: Tile-TOP'' (lift-free, combinatorial, survives the full adversarial suite, implies Wilf; Lean agent formalizing
the implication). Secondary: SR-CL (stronger in spirit, still combinatorial). TOP'' remains the weakest Lean-linked target.

## 2026-10-17 (night, 8) — **MaxCL** (Tile-TOP'' without the Dep term), decomposition identity, Load Lemma

### MaxCL — CONJ, strongest surviving tile statement; MaxCL ⇒ Tile-TOP'' ⇒ Wilf (PROVED implications)
For a tile (D,p), maximal cells A, non-maximal cells N (0 ∈ N unless D = {0}), and every rotation r = ⟨φ − σ⟩ (a bijection D → [0,m−1]):
   **Σ_{y∈A} (|y| − 1)·r(y) ≤ (d+1)·Σ_{z∈N} r(z)**   ⇔   Σ_{y∈A} T(y) r(y) ≤ (d+1)M'   (T(y) = d + |y|, M' = m(m−1)/2).
- Tile-TOP'' in r-form is Σ_A T r ≤ (d+1)M' + Dep (r = π − 1 = ⟨φ − s − 1⟩), so MaxCL = Tile-TOP'' with Dep dropped.
- Column form: Σ_a Σ_{a-columns C with maximal top} |C|·r(top C) ≤ (d+1)M'. Tile-CL was the same sum over ALL columns (FALSE);
  MaxCL drops exactly the non-maximal-top columns, which carry the spike losses.
- Semigroup meaning of the Wilf-relevant rotation: σ = c mod m, so r(x) = (w(x) − c) mod m = position of w(x)'s class in the
  window [c, c+m). Exact identity (CH' rewritten): **m·W = (d+1)M' − Σ_a Σ_C |C|·(w(top C) − c)**. MaxCL replaces w(top) − c by
  r(top) ≥ w(top) − c on maximal tops and drops non-maximal tops (where w(top) − c ≤ −n_b − 1 + m < 0).
- Tight: column (d = 1, r(top) = m − 1) and simplex {0, e_1..e_d} (r(0) = 0).
Evidence (0 failures everywhere):
- maxcl.py: all tiles d=2 m≤13, d=3 m≤10, d=4 m≤8, d=5 m≤7, all p, all σ.
- maxcl_adv.py: 8008 adversarial Apéry tiles (same suite as tiletop_adv).
- maxcl_d3.py: 6800 random 4- and 5-generated S, m ≤ 260, type ≤ 22; worst normalized slack (slack/m²) ≈ 0.25.

### Worst rotation
F(σ) := Σ_A(|y|−1)⟨φ(y)−σ⟩ − (d+1)Σ_N⟨φ(z)−σ⟩ satisfies F(σ+1) − F(σ) = −W_tot + m·w(x_σ) (x_σ = cell with φ = σ,
w = |y|−1 on A, −(d+1) on N, W_tot = Σw < 0). So F rises when σ passes a maximal residue and falls at a non-maximal one:
the max is at σ = φ(z0) with z0 ∈ N and φ(z0) − 1 ∈ φ(A). chaincharge.py: the worst σ is usually NOT φ(0).

### Decomposition identity (PROVED, trivial)
For u + v = y (all in D): r(u) + r(v) = r(y) + r(0) + mκ, κ ∈ {−1,0,1}. At r(0) = 0, κ ∈ {0,1}, so r is subadditive on D.
More generally, for any cells with Σ_i φ(x_i) ≡ φ(y) + (k−1)σ: r(y) ≤ Σ_i r(x_i) (least nonnegative representative).

### Load Lemma (residue-free) — CONJ; with the identity it gives MaxCL at σ = φ(0)
For each maximal y with |y| ≥ 2 there are weights λ ≥ 0 on unordered pairs {u, y−u}, 0 < u < y, with Σλ = |y| − 1, such that
every nonzero non-maximal cell carries total load ≤ d+1 (a pair {u,u} loads u twice).
- Proof of "Load Lemma ⇒ MaxCL at σ = φ(0)": (|y|−1) r(y) ≤ Σ_pairs λ (r(u)+r(y−u)) by subadditivity; sum over A;
  u, y−u < y are non-maximal; load ≤ d+1. ∎ It is valid for EVERY nonnegative r subadditive on D with r(0) = 0.
- General σ: the same computation gives Σ_A(|y|−1)r ≤ (d+1)Σ_N r provided m(B − P) ≤ (H + d + 1)·r(0), with H = Σ_A(|y|−1),
  B / P = λ-weight of pairs with κ = −1 / +1. This "bad event" bound is unproved.
- Necessary count condition (r = 1 off 0): 2Σ_A(|y|−1) ≤ (d+1)(|N| − 1). Tight for column and simplex. FALSE for non-tile
  down-sets (Δ_3 in d=2: 16 > 15), so the tile property is used already here.
Evidence: loadlemma.py (exact LP, Fractions): all tile SHAPES d=2 m≤12, d=3 m≤10, d=4 m≤8, d=5 m≤7: 0 count fails, 0 Load fails.
loadcount_adv.py: count condition on 6002 adversarial Apéry tiles (seed 3, m ≤ 100): 0 fails (min 0, at tiles with N = {0}).
Chain charging with the uniform load load(z) = Σ_{y>z} 2Π_a C(y_a,z_a)/C(|y|,|z|): 0 failures at σ = 0 on the same exhaustive range.

## 2026-10-17 (night, 9) — Load Lemma REFUTED; group-cone strengthening GCL; why residue-free routes must fail

### Load Lemma — **FALSE** (E64)
S = ⟨39,71,72,77⟩ (m = 39, d = 3, c = 394, W = 190). D is two 2-D staircases glued along the x_1-axis
(no cell with x_2, x_3 ≥ 1); A = 11 maximal cells at levels 5 and 6 (H = 47), |N| = 28, count slack 14.
Optimal max load (HiGHS) = 5.037 > d + 1 = 4. MaxCL at σ = 0 has slack 1910 here, so only the residue-free sufficient
condition fails. Consequence: **the conditional "Load Lemma ⇒ Wilf for m | c" is void.** What survives:
**MaxCL at σ = 0 ⇒ Wilf for every S with m | c** (σ = c mod m = 0; Wilf for m | c is OPEN in general: LITERATURE #5 has
it only with 4e ≥ m, DEF to g ≤ 120). Also FALSE: uniform box pairing (load Σ_{y>z} 2(|y|−1)/(|[0,y]|−2); 319/3002
adversarial tiles, max ratio 2.29; exhaustive small tiles pass with max load exactly d+1 at unit vectors).

### GCL: MaxCL holds on the whole cone of group-subadditive functions — CONJ (E63)
For a tile and z0 ∈ D (σ = φ(z0)) put ψ(x) = φ(x) − σ. Claim: for every r: ℤ/m → ℝ≥0 with r(0) = 0 and
r(g) + r(h) ≥ r(g+h): Σ_A(|y|−1) r(ψ y) ≤ (d+1) Σ_N r(ψ z). (Positions ⟨g⟩ are one such r, so GCL ⇒ MaxCL.)
Evidence: exact LP, all tiles d=2 m≤11, d=3 m≤8, d=4 m≤7, all σ: 0 failures; HiGHS, 202 adversarial tiles × all σ and
3002 adversarial tiles × {c mod m, 0} (m ≤ 120), incl. the Load Lemma counterexample: 0 failures.
Equivalent forms: (i) token splitting — tokens start at maximal y (|y|−1 each), a token at g may be split into g = h + (g−h),
tokens at 0 vanish, final tokens on N∖{z0} ≤ d+1 each; (ii) additive: for every cost q ≥ 0 on P = ψ(N∖z0),
Σ_y (|y|−1)·dist_q(ψ y) ≤ (d+1)Σ_P q, dist_q = cheapest representation as a sum of elements of P.
Structure of the dual: the minimizing r in small cases are quotient positions r(g) = ⟨u g⟩_k (k | m), i.e. MaxCL itself for
(D, up) and its quotients ℤ/k. **So the cone relaxation is tight exactly at the original instances: GCL is not easier than
MaxCL** (it adds only quotient instances). Important negative structural fact.
- Certificates need lattice (non-geometric) triples: on the 39-tile, 27.6 of 47 split units are lattice pairs.
- GLL1 (one-level pairing inside N∖z0) is FALSE: small tiles (d=2 m=4,5; d=3 m=7,8; d=4 m≤7) and 5/535 adversarial LPs with
  m > 3e, all "no admissible pair" cases with many spikes (|A| > m/2, huge W). Spikes serve as relays.
- E-count (Hall condition of the transport): for every Y ⊆ A, 2Σ_Y(|y|−1) ≤ (d+1)(|↓Y| − |Y| − 1): 0 failures (exhaustive
  + 3001 adversarial). It is necessary for the Load Lemma but the pair symmetry makes it insufficient.

### Exact tight cases of MaxCL (E66)
Column (d = 1), simplex (m = d+1), and **column-plus-spikes** {0, e_1, …, (k−1)e_1} ∪ {e_2, …, e_d} (seen for k = 3,
m = d + 2, at σ ≠ 0: e.g. d=3, m=5, p=(4,1,2), z0 = e_1: certificate r(2e_1) ≤ 2r(e_2) ≤ 4r(0), positions 4, 2, 1).
Next-tightest: staircase-like A (normalized slack ≈ 0.012). A proof must be exact on spike relays at σ ≠ 0.

### Reformulations recorded (all PROVED identities)
- Sawtooth form: MaxCL ⇔ ∀σ: Σ_{y∈A} T(y)·(⟨φ(y)−σ⟩ − (m−1)/2) ≤ (m−1)(m + Dep)/2 (a weighted discrepancy bound).
- With any linear lift w, positions r = w − σ − m⌊(w−σ)/m⌋ and F(w) = Σ_{non-max-top columns}|C|·w(top) (column identity
  holds for every linear function), so MaxCL(0) ⇔ m(d+1)g ≤ Σ_{nonmax}|C|w(top) + mΣ_A T(y)K(y) (K = Kunz coordinate).
- Position language: x maximal ⇔ r(x) + p_a ∈ B_a for all a (B_a = positions of the a-floor); y_a + 1 = distance back to B_a.

### Strategic review (night 9)
- Distance to result: the main conjecture MaxCL survives everything; but every residue-free or "soft" sufficient condition
  tried (Load Lemma, GLL1, uniform pairings) is false, and the soft cone relaxation is tight at the original instances.
  A proof must use the arithmetic of positions (φ mod m) together with the tile geometry.
- Theory of success: MaxCL is exact on column/simplex/column+spikes; any proof is an exact inequality. Candidates:
  (a) additive combinatorics (Kneser/Vosper: indicator duals reduce to count conditions on quotients; the extremal r are AP-
  structured exactly as in Vosper), (b) induction on tiles with a potential that is exact on column+spikes.
- Kill: Load Lemma / box pairing / GLL1 as proof targets. Keep E-count (true, necessary, residue-free) as a lemma target.
- Third line (CLAUDE.md requires ≥ 3): the m | c case — MaxCL at σ = 0 alone gives Wilf for m | c (open), and σ = 0 has
  geometric subadditivity for free; attack it as a self-contained theorem.

### Crude rearrangement bound and the open regime (E69)
CR(D): Σ_i T_(i)·(m−1−i) ≤ (d+1)M' (T sorted decreasing) is residue-free and implies MaxCL for all p, σ.
- Holds on 3883/4001 adversarial tiles (crude_regime.py, seed 21); on 400 random semigroups in the open Wilf regime
  (q ≥ 4, 3e < m, t ≥ e, m ≥ 20; crude_open.py) it never fails (worst normalized slack 0.024, ⟨20,43,45,48⟩).
- **FALSE in the open regime** under hill-climbing (crude_search.py): ⟨34,46,65,66,75,81,88,105⟩ (c=160, q=5, e=8, t=17)
  normalized crude slack −0.021; four more examples −0.005 … −0.014. All have T(A)/(dm) ≈ 0.85–0.87, Dep/m ≈ 1.1–1.6.
  MaxCL's true normalized slack on them: 0.108–0.168 (min over σ), ≈ 0.21 at σ = c. So the arithmetic of positions buys
  13–20% there; a residue-free proof of MaxCL is impossible even restricted to the open regime.

### Exact column form of MaxCL (PROVED identity)
For an a-column C with top at position t = r(top) and length L: E_C := L·t − Σ_{x∈C} r(x) = S_a(L) − m·N_a(L,t), where
S_a(L) = Σ_{h<L} ⟨h p_a⟩ and N_a(L,t) = #{h < L : ⟨h p_a⟩ > t} (σ-independent except through t). Hence
   **MaxCL ⇔ Σ_a Σ_{C: top ∈ A} S_a(|C|) ≤ M' + Σ_a R_a + m·Σ_a Σ_{C: top∈A} N_a(|C|, r(top C))**,
R_a = Σ of positions over non-maximal-top a-columns. The left side depends only on (D, p); the column-subadditive bound (★)
is this with the N_a carry terms dropped (and fails on staircases). Averaged over σ, m·N_a = S_a exactly.

## 2026-10-17 (night, 10) — first unconditional MaxCL family: height ≤ 2 (PROVED); height 3 scheme

### Flat-MaxCL (PROVED; full proof in PROOFS.md)
Tiles of height ≤ 2: the identity ρ_a + ρ_b = ρ_ab + ρ_0 + mκ, the degree bound deg(a) ≤ d+1 and the window-counting
B ≤ ρ_0 (wrapped cells sit at distinct positions ≥ m − ρ_0) close the inequality exactly (m = 1 + d + |E|).
Corollary: Wilf for reduction number ≤ 2 (Ap ⊆ {0} ∪ P ∪ 2P). Novelty unverified (see PROOFS.md).
- The mechanism answers the "bad-event control" gap left open in night 8 for this family: m(B − P) ≤ (H+d+1)r(0)
  holds because H + d + 1 = m and B ≤ r(0).
- src/known.py: reusable checker of literature conditions; flat_new.py found height-2 S with 3e < m outside all of them.

### Height-3 natural scheme — CORRECTION (same night)
Pairs: level-3 maximal y → (e_a, y − e_a) for a ∈ supp(y), weight 2/|supp y| each; level-2 maximal y → (e_a, e_b).
**The "sufficient inequality" Σ_z (load(z) − d − 1) r(z) + m(B − P) ≤ (H + d + 1) r(0) is IDENTICAL to MaxCL** for every
choice of pair weights (the decomposition identity is exact), so the "0 failures" recorded for it are just MaxCL evidence
(all height ≤ 3 tiles d=2 m≤8, d=3 m≤10, d=4 m≤8, d=5 m≤7; 300 random; 300 dense, worst normalized slack 0.12).
A scheme says something only once its two terms are bounded SEPARATELY (as in the flat proof: term 1 ≤ 0 pointwise,
term 2 ≤ m·r(0)). Facts that do hold: level-2 loads ≤ d+1 (load(z) = Σ_c [z+e_c ∈ L3]·2/|supp(z+e_c)| ≤ d+1); unit
loads can exceed d+1 (up to 1.44(d+1) seen), and Σ over units of load = 2(n2^A + n3^A) can exceed d(d+1), so NO choice of
weights gives pointwise load ≤ d+1 at height 3: every decomposition of a level-3 cell uses one unit and one level-2 cell.

### Lift form of MaxCL (PROVED identity, liftform.py asserts it on all small tiles)
ρ_0 = r(0), ρ_a = r(e_a), L(x) = Σ_a x_aρ_a − (|x|−1)ρ_0, K(x) = ⌊L(x)/m⌋ (so r = L − mK), w = |y|−1 on A, −(d+1) on N:
   (d+1)Σ_N r − Σ_A(|y|−1)r = m·F − (Σ_a β_aρ_a − β'ρ_0),   F = Σ_x w(x)K(x),
   β_a = Σ_A(|y|−1)y_a − (d+1)Σ_N z_a,   β' = Σ_aβ_a + m + Dep   (uses H − (d+1)|N| = −(m + Dep)).
Simplices Δ_k: β = 0, β' = m, so MaxCL there ⇔ F ≥ −ρ_0.
- OBSERVED: β_a ≤ 0 for every a on all tiles d=2 m≤12, d=3 m≤10, d=4 m≤8, d=5 m≤7 (residue-free; unproved).
- FALSE: F ≥ 0 at σ = 0 (F0) and F ≥ −ρ_0 (600/924 d=2 tiles; smallest D = {00,01,10,20,30}, p = (3,2), F = −1):
  the linear part and the carry part cannot be bounded separately (the column needs the negativity of Σβ_aρ_a).

### Uniform split scheme: Wrap Lemma (WL), Sumset Lemma (SL), and LD — CONJ, strong evidence
Uniform scheme: each maximal y (|y| ≥ 2) spreads |y|−1 over its q_y − 2 ordered geometric splits (u, y−u), 0<u<y,
q_y = |[0,y]|, weight w_y = (|y|−1)/(q_y−2) ≤ 1. All splits of y have position sum ≡ r(y)+r(0): the low value
s_y = ⟨r(y)+ρ_0⟩ or s_y + m; the s_y are distinct over y.
- **SL(t)**: for every σ and every t ∈ [0, m): Σ_{y∈A} w_y·#{0<u<y : r(u)+r(y−u) ≤ t} ≤ t+1.
  Evidence: all tiles d=2 m≤12, d=3 m≤10, d=4 m≤8, d=5 m≤7, all σ, t: 0 failures (sumlemma.py). **Holds also for non-tile
  down-sets with φ merely injective** (sumlemma_inj.py: d=1..3, |D| ≤ 8, m ≤ 30, ~110k instances, 0 failures), so the
  tile property is NOT needed — SL is a statement about down-sets with injective linear positions, amenable to induction.
- For t < ρ_0 every counted split wraps, so SL(t) is the nested-window form **WL-t** and SL(ρ_0−1) is **WL: B ≤ ρ_0**
  (generalizes "B ≤ ρ_0" of the flat proof to all heights). Box-local Hall versions are FALSE (wlhall.py: per-box 176
  d=2 fails; spikes in the top window serve as relays).
- **LD**: Σ_{N∖0}(load−d−1)r − mP ≤ (H+d+1−m)ρ_0, equivalently MaxCL-slack(σ) ≥ m(ρ_0 − B). Then WL + LD ⇒ MaxCL.
  LD at σ = 0 is MaxCL(0); LD holds for flat tiles (flat proof). Evidence: 0 failures on 700 semigroup tiles of height ≥ 3
  (m ≤ 70; wraplemma_adv.py seeds 1, 2) together with WL.
- Status: SL/WL are the σ-part of MaxCL isolated as a residue-light lemma; LD still contains MaxCL(0).

### Wilf for e = 4 as a target (e = 4 is OPEN; literature check: web search 2026-10-17 finds only e ≤ 3)
MaxCL (even Tile-TOP'') for d = 3 tiles ⇒ Wilf for e = 4. Height ≤ 2 gives nothing there (m ≤ 10).
Residue-free crude bound CR for d = 3 rewrites as **Σ_i i·T_(i) ≥ (m−1)(T(A) − 2m)** (T sorted decreasing), automatic when
T(A) ≤ 2m. Random e=4 tiles: 1 failure in 2353 (⟨9,10,12,16⟩, m = 9 ≤ 19, Wilf known). Hill-climb (m ∈ [20,60]):
minimum CR slack exactly 0 at ⟨29,50,69,90⟩ (m = 29): D = Δ_4(x_2,x_3) ∪ Δ_4(x_1,x_3) ∪ tail (5..8,0,0) — two 2-D
staircases glued along an axis (relation 50+69 = 29+90). There Dep ≈ m − O(√m) and both sides of CR are Θ(m^{3/2}):
CR is borderline on this family, while MaxCL slack is ≈ 0.29 (lots of arithmetic room).

### Low splits = low box cells (PROVED, slexcess.py asserts it)
For maximal y and the rotation r: the ordered split (u, y−u) is low (sum s_y = ⟨r(y)+r(0)⟩) iff r(u) ≤ s_y.
(Proof: r(u)+r(y−u) ∈ {s_y, s_y+m}; if r(u) ≤ s_y then r(y−u) ≡ s_y − r(u) ∈ [0,s_y].) Hence the uniform low mass is
B_y = w_y·(|[0,y] ∩ {r ≤ s_y}| − 2[y not wrapped]), and SL(t) ⇔ Σ_{y∈A, s_y ≤ t} B_y ≤ t+1.
- FALSE sharpenings: "(B_y−1)^+ summed ≤ free s-slots" (with or without spikes as free slots; 116/924 d=2): deficits
  B_y < 1 are needed, SL is genuinely cumulative. Proved special case sketch: L-shapes with one corner on an axis
  (w_2 ≤ 1/2 and the box involution maps overlap cells outside the overlap) — to be written carefully.

### Which relations certify MaxCL(0)? (E76, E77)
- PALL(0) (position-aware load lemma, one-level geometric splits, capacities only on top windows of positions): FAILS
  on ⟨39,71,72,77⟩ and ⟨25,44,45,49⟩ (2/400; pointwise Load Lemma fails 8/400). In ⟨25,44,45,49⟩ (p ≡ (−6,−5,−1)) every
  geometric split carries (r(u)+r(v) = r(y)+m), so carry-free subadditivity is useless although MaxCL(0) slack is 0.60.
- RGCL0 (LP: geometric subadditivity + column successor relations r(f_a(x)) ≤ r(x) + r(e_a)): FAILS on exactly the hard
  tiles ⟨39,71,72,77⟩, ⟨25,44,45,49⟩, ⟨36,37,42,43⟩, ⟨29,50,69,90⟩, ⟨58,240,…⟩ (passes 145 random). GCL (all group
  relations) holds on them. **So MaxCL(0) needs non-local lattice relations on these tiles.**

### Strategic review (night 10b)
- Distance: Flat-MaxCL proved (Lean in progress). General MaxCL: every local / residue-free method (Load Lemma, PALL,
  RGCL0, crude CR, box pairing) fails on ONE recurring family: **two-face tiles** D = D_1 ∪ D_2 with D_1 ⊂ {x_1 = 0},
  D_2 ⊂ {x_2 = 0} (relation n_1 + n_2 = m + n_3, so x_1x_2 = 0 on D), e.g. ⟨36,37,42,43⟩, ⟨29,50,69,90⟩, ⟨25,44,45,49⟩,
  ⟨39,71,72,77⟩. They are also the e = 4 cases where CR fails. MaxCL slack there is 0.11–0.60, so they are not tight —
  they defeat the methods, not the inequality.
- Theory of success: on two-face tiles the geometry is two 2-D down-sets sharing an axis; 2-D is the regime where
  crude/rearrangement arguments work. A proof of MaxCL for two-face tiles (any d with the x_1x_2 = 0 structure) would
  remove the common obstruction and is a concrete test of a "face decomposition" mechanism.
- Decision: CONTINUE MaxCL; PIVOT the next session to (1) MaxCL for two-face tiles, (2) SL proof for d = 2.
  KILL: further local-relation LPs (RGCL variants) — the obstruction is established.

## 2026-10-17 (night, 11) — Lean closes Flat-MaxCL; e = 4 structure: CR misses only two-face tiles

### Lean (verified by the lead)
lean/Wilf/MaxCL.lean: MaxCLAt, tileTOPAt_of_maxCLAt, maxCLAt_of_height_le_two, wilf_of_factDownSet_height_le_two,
wilf_of_apery_height_le_two (Ap ⊆ {0} ∪ P ∪ 2P ⇒ Wilf). lake build OK; #print axioms: propext, Classical.choice,
Quot.sound only; no sorry. Flat-MaxCL is now KERNEL-CHECKED.

### AMaxCL (affine relaxation) — OBSERVED for every down-set (not only tiles)
For every affine L ≥ 0 on D: Σ_A (|y|−1) L(y) ≤ (d+1) Σ_N L(z) (amaxcl.py: all non-degenerate down-sets d=2 m≤13,
d=3 m≤10, d=4 m≤8, and 400 adversarial tiles; 0 failures, max exactly 0 when some β_a = 0).
Equivalent (Farkas): Σ_x w(x)(1,x) = −(m+Dep)(1,C) with **C = −β/(m+Dep) ∈ conv(D)** (a barycenter lemma), and then
Σ_x w(x)L(x) = −(m+Dep)L(C) for every affine L. Consequence: MaxCL holds for every rotation in which r is affine on D
(carry-free rotations). Leverage low (carries are the whole difficulty), but it is the exact "linear part".

### IntervalCL — FALSE (trivially)
Replacing group subadditivity by integer subadditivity (f(a)+f(b) ≥ f(a+b) only for a+b < m) fails: f = δ_1 is
integer-subadditive and a maximal cell can sit at position 1 (⟨39,71,72,77⟩, σ = 0, LP min −5). Low positions need wrap
relations; certificates must allow wraps, whose identity cost is m each.

### Smallest tile where geometric splits cannot certify MaxCL(0): m = 13 (gcl_cert.py)
⟨13,14,16,17⟩ (two-face, D_1 = {(0,j,k): j+k ≤ 3}). Units (0,1,0), (0,0,1) are overloaded under geometric splits by
exactly one unit. A carry-free GROUP certificate exists using one non-geometric relation 2·(0,2,0) ≡ (0,0,3)
(lattice vector (0,4,−3); positions 6 + 6 = 12). All relations in the certificate are carry-free (g + h < m).

### e = 4: where the residue-free crude bound CR fails (heavy3.py, twoface_census.py, heavy_nontwo.py)
For d = 3, CR ⇔ Σ_i i·T_(i) ≥ (m−1)(T(A) − 2m), automatic when T(A) ≤ 2m (Dep ≥ m).
- Random e = 4 grlex tiles: 35/2286 have T(A) > 2m; CR fails on 3 of them; 29/35 are two-face.
- All 8 known CR failures (hill-climb) are TWO-FACE with e_a + e_b ≡ e_c (a unit vector), e.g. 54+75 = 60+3·23.
- Non-two-face tiles (all e_a+e_b ∈ D): hill-climb of CR slack (30 runs, m ∈ [20,70]): 0 failures, min normalized
  0.045; hill-climb of T(A)/m: max 2.0 at m = 24, ≤ 1.81 for m ≥ 40 (16 runs, m ≤ 90).
  **CONJ NT: a non-two-face d = 3 tile with m ≥ m_0 has T(A) ≤ 2m, hence satisfies CR, hence MaxCL.**
- So Wilf for e = 4 reduces (modulo NT and a finite check) to MaxCL for two-face tiles.

### Two-face tiles with e_1 + e_2 ≡ e_3 are 2-D tiles in disguise (PROVED, elementary)
ψ(i,j,k) = (i+k, j+k) is injective on {x_1x_2 = 0} and φ = s·p_1 + v·p_2 on the image (since p_3 ≡ p_1 + p_2).
So Ω' = ψ(D) ⊂ ℕ² is a fundamental domain of a 2-D lattice with linear positions; |y| = max(s,v) (levels of D are
the hooks max(s,v) = h), T = 3 + max(s,v). If Ω' is a 2-D down-set then D = ψ^{-1}(Ω') is automatically a 3-D down-set;
3-D maximal cells = row ends below the diagonal ∪ column tops above it (∪ diagonal corner).
- ⟨36,37,42,43⟩: Ω' = 6×6 box, p' = (1,6); A = the outer hook (11 cells, T = 8). ⟨29,50,69,90⟩: Ω' = 5×5 box + row
  tail (an L-shape). Census: of two-face tiles with z* = e_c, 50 have Ω' a down-set, 143 do not (Ω' = L-shape with a
  bump, still a 2-D lattice tile); 418 two-face tiles have z* ≠ e_c (mostly e_a + e_b ≡ 0).
- Box case, proof sketch (CONJ → to be written): for a box tile with lattice ⟨(a,−t),(0,b)⟩ the right column is a full
  coset of ⟨p_2⟩ (spread: Σ r ≤ b(a−1) + ab(b−1)/2) and the top row is an AP with step p_1 (crude bound); the sum is
  ≤ 4M' once 3a²b − 2ab² − a² − 4ab + b² + b + 2 ≥ 0 (a ≥ b ≥ 2, a ≥ 7; small cases by computation). The other lattice
  type swaps the roles; for a ≫ b the crude bound on the heavy column suffices.
- FALSE: per-face split Σ_{A∩D_i} T r ≤ 2 Σ_{D_i} r (facecl.py; ⟨36,37,42,43⟩ −0.20): faces must be coupled.

### MaxCL has uniform room away from tiny tiles (from logs/maxcl_search_*.log)
Minimum normalized MaxCL slack found by hill-climbing semigroup tiles (m ≈ 30–90, all σ): 0.087. The only tight cases
are tiny (column, simplex, column+spikes, m ≤ d+2). So an argument with o(m²) error plus a finite check would suffice
for each fixed d — "robust" mechanisms are admissible.

### Tile-CL revisited for d ≤ 3 (night 11) — integral, tight, and a candidate route to e = 4
Tile-CL: X(σ) = Σ_{y∈D} T(y) r_σ(y) ≤ (d+1)M' with T(y) = Σ_{a: y top of its a-column}(y_a+1) (all column tops).
Tile-CL ⇒ MaxCL (drop non-maximal tops) ⇒ Wilf. Known FALSE at d = 6 (E47; core ∪ 4 spikes, E51).
- **Integrality (PROVED):** slack(σ) = (d+1)M' − X(σ) is always a multiple of m. Proof: X(σ+1) − X(σ) = −dm + m·T(x_σ),
  and slack(0) ≡ M' − Σ_a p_aΣ_{a-cols C} C(|C|,2) ≡ M' − Σ_x φ̃(x) ≡ 0 (mod m), since Σ_x x_a = Σ_C C(|C|,2) and
  Σ_x φ(x) = M'. So K(σ) := slack/m is an integer walk with steps d − T(x_σ), mean (m−1)/2, and
  **Tile-CL ⇔ K > −1 ⇔ X(σ) < (d+1)M' + m** (an error budget of m − 1 for free).
- **Inversion form (PROVED identity):** K(σ) = N(σ) − κ with N(σ) = #{(x,a) : x ≠ top_a(x), r_σ(x) > r_σ(top_a x)}
  (column inversions) and κ = (Σ_a Σ_{a-cols C} S_a(|C|) − M')/m ∈ ℤ, S_a(L) = Σ_{h<L}⟨h p_a⟩ = m·(average of the
  column's inversion count over top heights). So Tile-CL ⇔ min_σ N(σ) ≥ κ. (d = 1: κ = 0. Row-major boxes: κ = 0.)
- **Evidence for d = 3:** exhaustive all d = 3 tiles m ≤ 15 (tilecl_d3_exh.py: 5136 + 12984 + 12210 + 19416 tiles for
  m = 12..15; 0 failures, ~25% tight), plus E15 (m ≤ 11); 8352 varied e = 4 semigroup tiles (grlex/lex/revlex × all
  generator orders, conductor truncations; tilecl_e4_var.py) and 1500 random + 12 climbs (tilecl_e4.py): 0 failures,
  min slack exactly 0 (tight) very often.
- **2-D L-shapes:** Tile-CL holds on all L-shape tiles m ≤ 40, all p, all σ (lshape_tc.py exh 40; 3837 shapes); slack/m
  is an integer in [0, m−1] there (lslack.py); tight at σ = end of the top row block when p_1 = 1.
- The reflected τ-classes of an L-shape never re-tile ℤ/m (zsets.py, 5516 cases) — no direct box reduction.
- **CONJ Tile-CL(d ≤ 3).** It would give Wilf for e = 4 through the Lean chain (Tile-CL ⇒ MaxCL ⇒ Tile-TOP'' ⇒ Wilf).

### Strategic review (night 11)
- Distance: Flat-MaxCL is kernel-checked. New PROVED family: two-face box tiles (unbounded height). New maps of e = 4:
  (a) CR fails only on two-face tiles (exhaustive non-two-face d=3 m ≤ 18: CR always holds); (b) two-face tiles with
  e_1+e_2 ≡ e_3 are 2-D tiles whose 3-D columns are the rows, columns and DIAGONALS of the picture; (c) Tile-CL(d = 3)
  survives exhaustive m ≤ 15 and ~10k semigroup tiles, is integral and tight.
- Theory of success: e = 4 is the open frontier closest to our machinery. Two routes: (I) Tile-CL for d ≤ 3 — exact and
  integral, so a counting/injection proof (inversions N ≥ κ) is the natural shape; d = 2 L-shapes is the base case
  (CDL). (II) MaxCL d = 3 = CR (non-two-face; residue-free, needs a structural proof) + two-face (2-D pictures; boxes done).
- Kill: per-face splits, IntervalCL. Deprioritize: SL for d = 2 (only useful together with LD ⊇ MaxCL(0)).
- Next: prove Tile-CL for 2-D L-shapes via the inversion form (base case of route I and input for route II).

## 2026-10-18 (night 12) — 2-D Tile-CL PROVED (corner-sum bijection); d=3 structure

### THEOREM (2-D Tile-CL, every 2-D tile) — PROVED; full proof in PROOFS.md ("2-D Tile-CL for EVERY 2-D tile")
For x ∈ D let τ(x) = (end of its row, top of its column) (the corner; may lie outside D). Then
**μ(x) := φ(x) + φ(τ(x)) is a bijection D → ℤ/m** (rectangle: translation; L-shape: the three τ-classes translated by
their corners reassemble, mod Λ = ⟨(a',b'),(a,−c)⟩, into a translate of −D). Since r(t_1x)+r(t_2x) ∈ [0, 2m−2] and
≡ μ(x) − 2s, X(s) ≤ Σ_{w∈ℤ/m} max{y ≤ 2m−2 : y ≡ w} = 3M'. Exact slack: 3M' − X = m·Σ_x([r(x)+r(τx) ≤ m−2] − ε(x)).
How found: the L-shape class-discrepancy sum CC = Σ_τ #{x ∈ X_τ : r(x)+ρ_τ ≤ m−2} − Σ_τ n_τ(m−1−ρ_τ)/m turned out to
be IDENTICALLY 0 (52108 cases), i.e. an identity, which is exactly bijectivity of μ. Old "CDL" (TC section) is this
identity plus the pointwise bound ε ≤ [r+ρ ≤ m−2].
Also proved on the way: 2-D down-set tiles have ≤ 2 outer corners (two full-support minimal non-elements q_1 ≠ q_2
would give q_2 − q_1 ∈ (D−D) ∩ Λ); in ANY dimension a tile has at most one minimal non-element of full support (same
argument: q_2 − q_1 = δ⁺ − δ⁻ with δ^± ≤ q_i − (1,…,1) ∈ D).
Consequences: Wilf for e ≤ 3 by a new route (known: FGH 1987); the 2-D input of the two-face reduction is closed.

### Hall's theorem makes the counting identity dimension-free
Σ_x φ(τ(x)) ≡ 2M' ≡ 0 (mod m) in every dimension (from slack integrality: Σ_aΣ_C |C|φ(top) ≡ (d+1)M' and
Σ_aφ(t_a x) = (d−1)φ(x) + φ(τx)). By M. Hall (1952: a sequence of |G| elements of an abelian group G with sum 0 is
the difference sequence of two orderings of G) there is a bijection β: D → ℤ/m with β(x) + φ(τx) bijective, and then
for every s: Σ_x [⟨β(x) − s⟩ + r(τx) ≤ m−2] = T(s) := Σ_x (m−1−r(τx))/m. So Tile-CL(d) ⇔ Σ_x ε(x) ≤ T(s) where
ε(x) = (Σ_a r(t_ax) − (d−1)r(x) − r(τx))/m ∈ [−(d−1), d−1], and T(s) has a combinatorial count for any such β.
For d = 2, β = φ works and ε ≤ the indicator pointwise. For d = 3 no canonical β among φ∘(column-flip words)
(flipbij.py), and ε = 2 occurs (then u+v ≤ m−3 automatically).

### d = 3 structure (E87)
- Pairwise 2-D sums inside a 3-D tile can exceed M' (pairs3.py max 1.055M'), total ≤ M': directions must be coupled.
- Face chain: ε = ε_ab + ε'_c with ε_ab the slice-face carry at x (corner τ_ab(x) = (t_a,t_b,x_c)) and ε'_c the carry of
  the "diagonal rectangle" (x, τ_ab x, t_c x, τ x). Then **X − M' = Y_c + m·E_ab for every c**, where
  Y_c = Σ_x [r(τ_ab x) + r(t_c x)], E_ab = Σ_x ε_ab(x).
- **OBSERVED (P1): Y_c ≤ 3M' for every c** (all 3-D tiles m ≤ 10; tight). P1 is a 2-D Tile-CL for the pair
  (slice corners, c-columns) inside a 3-D tile. But E_ab can be positive (≤ 2 for m ≤ 10), so P1 is not enough:
  Tile-CL ⇔ (3M' − Y_c)/m ≥ E_ab.
- μ-discrepancy A(s) = Σ_x[u+v ≤ m−2] − T(s) ∈ [−2, 2] for m ≤ 9 (small but nonzero).
- Dimension threshold (E83, E88): Tile-CL exhaustive d=4 m ≤ 14, d=5 m ≤ 12, 0 failures; core+spike failures only at
  d = 6. Plausibly Tile-CL holds for d ≤ 5 — a d=3 proof need not be specific to d = 3.

### Partition-CL is NOT a robust law (kpart.py, E89) — refutes STATE's "test P1 in every d"
For a set partition Π of [d] into k ≥ 2 parts, τ_S(x) := x with the coordinates in S replaced by the tops t_a(x).
Partition-CL(Π): Y_Π = Σ_x Σ_{S∈Π} r(τ_S x) ≤ (k+1)M'. Π = all singletons is Tile-CL; d = 3, Π = {ab | c} is P1.
- d = 3, m ≤ 16 (exhaustive): every partition holds (max excess 0). So P1 is exhaustively true for d = 3, m ≤ 16.
- d = 4, m = 11 (exhaustive): Tile-CL and (1,3) hold, but **(1,1,2) and (2,2) FAIL** (excess exactly 1·m);
  m = 12: all hold.
- d = 6 core+spike tile at m = 19: partitions of every k fail, including k = 2 types (1,5), (3,3).
Merge rule: K_Π = K_{Π'} − E_{S1,S2} (merging two parts subtracts the slice-carry sum), so partition-CL for a coarser
Π is Tile-CL *minus* carries, and the carries are not controlled in d ≥ 4. Conclusion: P1 is not a dimension-free
statement; any proof of P1 for d = 3 must use d = 3 (a 2-part split there is (1,2), whose 2-element part is a 2-D
slice, where 2-D Tile-CL is a theorem). Tile-CL (all singletons) is the distinguished partition.

### Coupling inequality CI_c (coupling3.py) — REFUTED
Exact (any 3-D tile): X_a + X_b = Σ_x H(w_ab x) − m·Q_ab, w_ab = ⟨r(t_a x)+r(t_b x)⟩, Q_ab = #{x : r(t_a)+r(t_b) ≤ m−2},
H(w) = w + m (w ≤ m−2), H(m−1) = m−1. Hence Tile-CL ⇔ X_c − m·Q_ab ≤ 4M' − Σ_x H(w_ab x). If w_ab is bijective
(Σ H = 3M') this reads E_c := X_c − M' ≤ m·Q_ab ("CI_c"). Tested unconditionally on all 3-D tiles m ≤ 11: CI_c fails
in ~40% of (tile, s, c) triples, worst (E_c − mQ_ab)/m = 1.82 at m = 11. So when it fails, Σ H(w_ab) < 3M' must
compensate: the non-bijectivity of the pair map is load-bearing, not a nuisance. Pair-by-pair coupling is dead in
this form.

### Literature check (night 12)
e = 4 Wilf remains OPEN. Delgado–Kumar (arXiv 2512.23891, Dec 2025) verify Wilf for maximum primitive ≤ 60; known
classes: e ≤ 3, c ≤ 3m, e ≥ m/3, |L| ≤ 12, m ≤ 19, g ≤ 100, arithmetic-sequence generators. Nothing equivalent to
Tile-CL / corner-sum bijection was found (search over arXiv 2306.09876, 1610.08726, 2106.07246, 2512.23891,
Dobbs–Matthews notes); this is a limited search, not a priority claim.

### Lean: 2-D Tile-CL KERNEL-CHECKED (night 12; verified by the lead)
lean/Wilf/TileCL2.lean (529 lines): tileCLAt_two_of_injOn (L3 from μ injective), Tile2.classify (L1), shape_inj /
cornerSum_injOn_of_two (L2), tileCLAt_of_two : IsTile D p → TileCLAt D p for d = 2 (the original TileCLAt of Carry.lean,
unchanged), tileCLAt_of_le_two (d ≤ 2), wilf_of_embDim_le_three : e ≤ 3 → c ≤ e·ℓ (known result, FGH 1987; new route,
now kernel-checked end to end). Lead checks: lake build OK; scripts/PrintAxioms.lean 170/170 entries only
[propext, Classical.choice, Quot.sound]; no sorry/admit/native_decide; Carry.lean definitions untouched (git diff).
Formalization showed L2 needs only one lattice relation ((a,−c) ∈ Λ) and L3 is ⟨u⟩+⟨v⟩ ≥ ⟨u+v⟩ summed (PROOFS.md).

## 2026-10-18 (night 12, cont.) — coherence of 3-D tiles; local-move landscape; refutations; Route II revisited

### OBSERVED: every tile with d ≤ 3 is COHERENT (coherent.py, E91)
LP-certified for all tiles d=2 m ≤ 12 and d=3 m ≤ 9: D = {w-minimal representative of each Λ-class in ℕ^d} for some
w ∈ ℝ^d_{>0}. Equivalently D is the solution set of Gomory's group problem min w·x s.t. Σ x_a p_a ≡ g (mod m).
Consequences (conditional on coherence in general, d = 3):
- every 3-D tile is the factorization tile of the numerical semigroup ⟨m, w_1, w_2, w_3⟩ for integral w ≡ p (mod m) in
  its chamber (scale up so w_a > m); maximal cells ↔ PF(S) + m, |A| = type t(S);
- tiles of a fixed p = chambers of the Gröbner fan of I_Λ on the positive octant; literature: Nakamura (abelian
  G ⊂ GL(3): the cones σ(Γ) of G-graphs form a fan; tiles = Nakamura's G-graphs). Wall-crossing = λ-shift
  y ↦ y + k(y)λ, k(y) = max{k ≥ 0 : y + kλ ≥ 0}, λ the primitive lattice vector of a corner relation q − f(q).
- Boundary chambers (w_a → 0) are products D' × [0, ord p_a) over 2-D tiles of the quotient.

### Move graph and K-landscape (flipgraph.py, E92)
Corner-relation wall crossings connect all tiles of every p (d=2 m ≤ 10, d=3 m ≤ 8). But K_s has MANY non-global local
minima that are not boxes (d=3 m=8: 9366 local minima, 3096 non-global, 3678 non-box). K-descent to boxes is dead.
### Box extremality — FALSE (boxmin.py, E93)
min over boxes of K_s exceeds min over all tiles by up to m − 3, already in d = 2 (p = (1, −1)). Per-(p,s) minimum of
K over tiles is not 0 in general either (kmin_shape.py), so no universal equality structure per (p, s).
### Non-monomial generalization — FALSE (by hand)
G-cluster k[x,y]/(x² − y, xy, y²) for ℤ/3 with weights (1,2): the Jordan-type version of Tile-CL gives X(0) = 11 > 9.
Injectivity of φ on exponents (monomial G-graphs = tiles) is essential.
### Layer obstruction for d = 3 (proved, elementary)
A "layer" proof f(s) ≥ Σ_layers Σ_groups ⟨k s − Σφ⟩ needs uniform group sizes per layer and Σ sizes ≤ d; for d = 3
this forces a singleton layer whose tops form a complete residue system, impossible when some cell is a top in no
direction (e.g. 0 in a non-degenerate tile). So 3-D Tile-CL needs carries: no pure equidistribution proof exists.
### μ-defect (mudefect.py)
Defect multiset of μ = φ + φ∘τ grows with m (up to (−1)^5, 2, 3 at m = 8); collisions are driven by cells (0 and
similar) whose corner τ(x) lies far outside D. μ is the wrong 3-D object.

### Route II revisited: NT is FALSE as stated, but with small excess (nt_exh.py, nt_struct.py, E94)
T(A) = Σ_{y∈A}(3 + |y|) = #{(x,a) : t_a(x) maximal} = Σ_x (3 − ν(x)), ν(x) = #{a : t_a(x) not maximal};
T(A) ≤ 2m ⇒ MaxCL trivially (Σ_A T r ≤ (m−1)T(A)). Exhaustive non-two-face 3-D tile shapes m ≤ 20: T(A) − 2m > 0
occurs (m = 7, 8, 10, 14–20), max excess 6 (m = 19); CR slack ≥ 15 always. Max-excess shapes: core {0,1}³ (with
(1,1,1) maximal) plus three 2-D face staircases ("three-face-like"); |A| ≤ 7.
Revised CONJ NT': non-two-face d = 3 tiles with m ≥ m_0 satisfy T(A) ≤ 2m (night 11 hill-climbs: T(A)/m ≤ 1.81 for
m ≥ 40). Combined with exhaustive Tile-CL m ≤ 20 (E83) this would reduce MaxCL d = 3 to two-face tiles.
NT ⇔ #{exposed cells (ν = 0)} ≤ #{ν = 2} + 2·#{ν = 3} (buried cells outnumber exposed ones).

### Strategic review (night 12, cont.) — decision PIVOT to Route II pieces
Route I (Tile-CL d = 3) has no 3-way correlation mechanism after ~10 refuted attempts (this session: CI_c, box
extremality, K-descent, non-monomial generalization, layer decomposition). Route II splits e = 4 into residue-free
geometry (NT' for non-two-face tiles) and two-face tiles (2-D pictures). First test of R2: the face-wise corner-sum map
(φ(x) + φ(2-D corner of x in its face; axis cells in the right face, or the left) is NEVER a bijection on two-face
tiles (tf_mu.py, all two-face tiles m ≤ 13, both conventions). In the k = 1 picture Ω' the 3-D columns are rows
(below the diagonal), columns (above) and DIAGONALS: two-face Tile-CL is a three-direction statement inside a 2-D
tile, so the 2-D bijection does not transfer verbatim.

## 2026-10-18 (night 12, late) — NEW THEOREM: the τ-criterion (Cross Lemma); Wilf for e = 4, τ ≤ 4 (or ≤ 5)

### How it was found
Route II data (ta_by_type.py, E95): over ALL 3-D tile shapes, max_{type t}(T(A) − m) is CONSTANT in m (4, 8, 12, 16,
21, 26 for t = 2..7, m ≤ 20): extremal shapes are compact two-face cores plus rods, and lengthening a rod adds 1 to
both T(A) and m. Explanation (proved): T(A) − m = Σ_x (c(x) − 1), c(x) = #{a : t_a(x) maximal}; a non-maximal x with
c(x) ≥ 2 is the meet of two maximal cells agreeing in exactly one coordinate, and each such pair meets once. So
T(A) ≤ m + 2t + P₁ for every 3-D down-set (P₁ = pairs agreeing in exactly one coordinate). Applied not to all maximal
cells but to the TOP LAYER X_q = Ap ∩ [c, c+m) inside TOP'' (Lemma A), the same cross count gives the theorem below.

### THEOREM (τ-criterion) — PROVED on paper; final step Lean (wilf_of_TOP2); formalization in progress
τ := |Ap(S,m) ∩ [c, c+m)| = #{f ∈ PF(S) : f ≥ c − m} ≤ t(S). If e ≥ 3 and (e−2)(m+1) ≥ τ(τ + 2e − 5), Wilf holds.
Sharper: (e−2)(m+1) ≥ 2(e−2)τ + 2P₂, P₂ = pairs of top-layer elements whose grlex-least factorizations differ in exactly
two coordinates. Key: Cross Lemma Σ_{u∈X_q}(ℓ(u)+1) ≤ m + P₂ (crosses of top-layer factorizations are disjoint except
one cell per pair). Corollaries: e = 4 & τ ≤ 4 ⇒ Wilf (m ≤ 12 by 3e ≥ m, Eliahou 2020); e = 4 & τ ≤ 5 ⇒ Wilf (with
Kliem–Stump m ≤ 19); any e: τ ≤ e − 1 ⇒ Wilf (contains the FGH range t ≤ e − 1). Full statement/proof: PROOFS.md.
Checks: src/taucrit.py 20 asserts every step on all 93,141 S ≠ ℕ of genus ≤ 20 (E96).
Novelty: UNVERIFIED (limited search found nothing equivalent; Marashdeh 2026: no theorem in the literature assumes t ≥ e).

### Consequence for e = 4 (new reduction)
The open e = 4 cases now have τ ≥ 5 AND P₂ > m + 1 − 2τ: many top-layer Apéry factorizations pairwise sharing a
coordinate — top layers concentrated on coordinate planes (two-face-like). This is exactly the planar regime where the
2-D theorems (2-D Tile-CL, two-face box theorem) live. Next: quantify the residual and attack it with 2-D methods.

## 2026-10-18 (night 12, later) — τ-criterion kernel-checked; residual is NOT two-face; positions carry the slack

**Lean.** lean/Wilf/TauCrit.lean (Lean agent; verified by the lead: lake build OK, 0 sorryAx, axioms propext/Choice/
Quot.sound, statements as requested, no existing definition changed). Kernel-checked: Cross Lemma (plain and P₂ form),
TOP'' from the criterion (e ≥ 2), Wilf from the criterion, e = 4 & τ ≤ 4 & m ≥ 13, e = 4 & τ ≤ 5 & m ≥ 19,
τ ≤ e−1 & m ≥ 3e−4. Proof simplification found by Lean: common cross cells of incomparable y, y' are exactly min(y,y').

**Residual (E98).** Conjecture "sharp-criterion residual ⇒ two-face tile" is FALSE: exhaustive over ⟨m,a,b,c⟩ with
generators < 3m gives non-two-face residual semigroups for m = 14..19 (⟨15,39,41,44⟩: τ = 5, P₂ = 7; ⟨19,29,41,42⟩:
τ = 7, P₂ = 14, deficit 16), none for m = 20..22 in that box. Kliem–Stump (m ≤ 19) covers them, but the pattern has no
mechanism; dropped as a route. The real two-face residual (box family) stays.

**Where TOP'' slack lives (E99).** Decomposing crude-bound loss: L_pos = Σ_u (m−π(u))(d+ℓ(u)) vs
L_cross = m(m+P₂−Σ(ℓ+1)). Box ⟨36,37,42,43⟩: L_pos 840, L_cross 180, needed 720. ⟨19,29,41,42⟩: L_pos 451, needed 152.
So the residual is closed by *positions*, not by better overlap counting. Box family: positions on the face x₂ = 0 are
6, 12, …, 30 (an AP with difference p₃ − p₁ = a): a line of top cells in direction v has positions in AP with
difference p·v, so k cells on a line need (k−1)|p·v| < m.

**Reformulation (exact).** For a non-top cell y ∈ D∖X let ψ(y) ∈ [1,m] be the position of the unique element of
w(y) + mℕ in the last layer [c−m, c). Then ψ: D∖X → Π^c is a BIJECTION (left elements of the last layer = lifts of
non-top Apéry elements). Each non-top cell lies on ≤ 1 arm per direction. So
  TOP'' ⇔ Σ_{(y,a): y on the a-arm of u_a(y)} (π(u_a(y)) − ψ(y)) ≤ m(m−1)/2 + Σ_y (d − deg y)·ψ(y),
with π(u) − ψ(y) ≡ k·p_a (mod m) for y = n(u) − k e_a. In T_{m,q} the origin carries the whole budget m(m−1)/2.
Per-direction form: TOP'' ⇔ Σ_a B_a ≤ m(m−1)/2, B_a = Σ_u π(u) n_a(u) − Σ_{Π^c} j; B_a alone can reach 2.6(m−1)
for d = 3 (so no per-direction bound of size m−1).

## 2026-10-18 (night 12, late 2) — the e = 4 accounting: ARM / Depth / N; NAW; τ ~ 2√m; min W ~ m

**Exact decomposition (PROVED, elementary; CH' with D-columns).** For every S with e = 4 (d = 3), summing over all
(cell x, direction a) incidences with column top t = t_a(x):
  m·W + m(m−1) = Σ_{(x,a)} (M − w(t)) = ARM + m·N + Depth, where
  ARM = Σ_{u∈X} (ℓ(u)+3)(m − π(u))  [incidences whose column top is in the top layer X],
  N = #incidences whose top t has w(t) < c (= 3(m−τ) − Σ_u ℓ(u)),  Depth = Σ over those of (c−1−w(t)) ≥ 0.
Hence
  τ-criterion  ⇔  m·N ≥ m(m−1);   TOP'' ⇔ ARM + m·N ≥ m(m−1);   **NAW ⇔ Depth + m·N ≥ m(m−1)**;
  Wilf ⇔ ARM + Depth + m·N ≥ m(m−1).  (General d: replace m(m−1) by (d−1)m(m−1)/2, 3 by d.)
Lemma A / TOP'' discard Depth entirely. NAW ("non-arm Wilf") discards the top-layer positions entirely.

**Max-arm PE is trivial; PE false; κ form.** PE (Σ over arm incidences of (π(top) − ψ(cell))⁺ ≤ m(m−1)/2) is FALSE
(⟨5,8,9⟩: 11 > 10). Restricting to the max arm at each cell it is trivial (each non-top cell z owns the row of pairs
(ψ(z), j), j > ψ(z); ψ injective). Exact per-cell form: TOP'' ⇔ Σ_{z∉X} κ(z) ≤ Σ_{u∈X} (m − π(u)),
κ(z) = Σ_{arms at z} π(top) − m − (d−1)ψ(z); κ > 0 only at cells where ≥ 2 crosses meet (src/scratch/kappa.py).
In the box family ⟨36,37,42,43⟩ every non-top cell is a 2- or 3-arm cell; positive κ only on the 5 axis triple points.
Every reformulation of CH'/Selmer of the form "Σ_x (3M − 4w(x)) ≥ m(m−1)" is a tautology; the content is always the
inequality used for M − w(t) (residue bound ⇒ CL/Tile-CL; ≥ m ⇒ TOP''; exact depth ⇒ NAW).

**NAW data (E100).** genus ≤ 18 (1,092 e = 4 S): fails only for m ≤ 9. All 75,588 e = 4 S with m ∈ [10,24], generators
< 3m: fails for 8, all with m ≤ 16 (incl. box a = 4, ⟨16,17,20,21⟩). Large m: box family NA/need ≈ a/3 (1.13 at a = 5,
3.8 at a = 13), arithmetic ⟨m..m+3⟩ ratio 8–35, ⟨m,m+1,m+k,m+k+1⟩ ≥ 3.3, Backelin ≥ 7.5, 400 random (m ≤ 200) ≥ 4.2.
CONJ (NAW, e = 4, m ≥ 17): Σ over (x,a) whose a-column tops below c of (M − w(t_a x)) ≥ m(m−1); equivalently
m·W ≥ Σ_{f∈PF, f ≥ c−m} (F − f)(ℓ(f+m) + 3) — a strong Wilf inequality with a pseudo-Frobenius correction.

**max τ for e = 4 (E101).** All ⟨m,a,b,c⟩ with generators < 3m, m ≤ 30: max τ = max type ≈ 2√m − 1 (box-like
⟨m, m+1, m+k, m+k+1⟩); hill-climbing with unrestricted generators never exceeded τ/√m = 0.79. Heuristic reason:
maximal cells of a 3-D down-set ↔ strict local maxima of the column-height function on its shadow; a "hook" of τ such
cells needs ≥ τ²/4 cells (box family), a 2-D region of them needs ~τ^{3/2}, but simplex-like tiles would need perfect
B_k-type residue sets (none found). CONJ: τ ≤ t ≤ 2√m for e = 4 (not checked against literature).
**min W for e = 4 (E102).** m ∈ [10,30], generators < 3m: min W/m ∈ [0.5, 2.3]; for m ≥ 17 min W ≥ m except m = 25
(box a = 5, W = 20); minimizers are two-face box-like. Box family W = a³/3 + O(a²) ~ m^{1.5}/3: e = 4 Wilf has a
growing margin, so a cruder-than-TOP'' argument can suffice.
Insight: in the simplex-like model (p_a = m + r_a, D = {|x| ≤ k}) Wilf ⇔ k(2r_max − r_others) ≥ m − 1, and the tile
condition (r·x distinct mod m on Δ_k) is exactly what forces the spread in r. The discrete correction (m−1)/4 in
"mean(Ap) ≤ (3/4)M − (m−1)/4" comes from distinct residues forcing generator spread.

## 2026-10-18 (night 12, latest) — Λ-criterion; cylinder structure of 3-D tiles; S1/NT' need arithmetic

**Λ-criterion (PROVED sufficient).** For every column top t: M − w(t) = m·λ_L(t) + (m − pos(t)), λ_L(t) = number of
left elements ≡ w(t) (mod m). Summing CH' over incidences: m·W + (d−1)m(m−1)/2 = m·Λ + R, Λ = Σ_z λ_L(z)T(z),
R = Σ_z T(z)(m − pos z) ∈ [0, dm(m−1)]. So W = Λ + dm − P/m − (d−1)(m−1)/2 ≥ Λ − (d−1)(m−1)/2:
**Λ ≥ (e−2)(m−1)/2 ⇒ Wilf.** CL is "R alone suffices", Λ-criterion is "level part alone suffices"; Λ ≥ N contains the
τ-criterion. Data (lam.py): genus ≤ 17, all e: every failure has m ≤ 3e (Eliahou's range!) — but the dichotomy is
FALSE on adversarial S (lam_adv.py: ⟨16,27,28,31⟩ 14 < 15; ⟨29,30,34,42,43,48,51,53⟩ 76 < 84; EF-type e = 24, m = 77,
829 < 836; all near-boundary with large W) and for e = 4 at m = 23 (⟨23,25,28,35⟩, 21 < 22; 13/73,014 fail, m ≤ 23).

**Cylinder structure of 3-D tiles (PROVED; PROOFS.md; cylinder.py all tiles m ≤ 12).** ≤ 1 full-support minimal
non-element q* (q* ∈ Λ); every other non-axis minimal non-element lies on a coordinate plane x_c = 0 and is ≡ t e_c with
distinct t, t e_c ∈ D; D = (∩ cylinders over coordinate slices) ∖ (q* + ℕ³). Horizontal slices are (base slice ∩
rectangle) minus a quadrant; column tops are min of two 1-D step functions (and q*). Explains no simplex-like tiles.
Generalizes to any d: minimal non-elements with support U inject into the face D ∩ {x_U = 0} via q ↦ q − λ.

**S1 / NT' (stair3.py, cdist.py).** Exact: Σ_{y∈A}(|y|+2) = Σ_{z∉A} c(z) + 2|A|, c(z) = #{a : t_a(z) maximal}; in 2-D
this gives the staircase inequality Σ(|y|+2) ≤ 2|F| trivially (c ≤ 2). In 3-D, S1 (avg c over non-max ≤ 2) holds for
all tile shapes m ≤ 14 up to excess 2 but FAILS on the box family (excess a−1 = #axis triple points). NT' (T(A) ≤ 2m) on
non-two-face shapes: excess ≤ 2 for m ≤ 14; random non-two-face tiles ≤ −0.095m. Geometry alone (cylinder structure)
permits D = three triangular faces with q* = (1,1,1) and T(A) ≈ 3m: excluded only by arithmetic (slice inner corners
i p_1 + (n+1−i) p_2 ≡ t_i p_3 form an AP whose t_i must be distinct in [0, n], forcing p_1 − p_2 ≡ ±p_3, etc.).
So NT' needs the inner-corner arithmetic, not just geometry.

## 2026-10-18 (night 13) — Wilf for all two-face e = 4 tiles (PROVED); general faces+core identity

**Two-face survey (twoface_survey.py, tf_cr.py, tf1_hooks.py).** Two-face tile: e_a + e_b ∉ D, so D = F_1 ∪ F_2 glued
along the c-axis (length L_3), e_a + e_b ≡ t·e_c. t = 0 is rigid (PROVED: each face has ≤ 1 inner corner, |A| ≤ 4;
planar argument, inner corners ≡ (−(h_2−1), 0) mod the face lattice). CR fails only for t = 1 (exhaustive m ≤ 18,
random m ≤ 80). t = 1 picture: ψ(i,j,k) = (i+k, j+k) maps D onto a union of diagonal hooks Ω'; Ω' is a Young diagram
iff ρ_1, ρ_2 strictly decrease. S = ⟨m, p_a, p_b, p_a + p_b − nm⟩, Ap_g = min over class g of the convex function
f(s,v) = s p_a + v p_b − nm·min(s,v).

**Two-face identity** 3mW + 3m(m−1) = (m − 4L_3)M + 4Def2D + 2p_c L_3(L_3−1) (PROOFS.md). It is CH' rewritten; the
content: singleton columns make each face 2-dimensional (mean ≈ (2/3)max). Four bounds A', B'', C, D cover every
(m, L_3) with m ≥ 18 (tf_bounds2.py exact to m = 400 + analytic m ≥ 75). With Eliahou (c ≤ 3m) and BGOW (m ≤ 18):
**THEOREM: Wilf for every e = 4 semigroup with a two-face tile.** Every intermediate inequality asserted on 26,779
two-face semigroups (tf_verify.py). This covers the box family (where the τ-criterion fails). Bound refinement
history: crude bounds left m ≤ 55 uncovered; B'', D, x_i ≤ L_3 − x_ax, p_c ≥ m + 1 and distinct-position gains
reduced it to m ≤ 17.

**Non-two-face: τ-criterion FAILS (nt_tau.py).** Exhaustive non-two-face e = 4, generators < 3m: max(2τ + P₂ − m − 1)
= −1, −1, −1, **9**, 0, **8**, 0 for m = 20..26 (⟨23,25,28,35⟩ τ = 8, P₂ = 17, W = 25; ⟨25,27,32,40⟩). Hill-climb with
free generators: best −2 (⟨25,110,113,118⟩). So non-two-face needs Depth or more than C.

**θ law (meanmax.py).** θ := mean(Ap)/max(Ap). Wilf ⇔ θ ≤ 3/4 − (m−1)/(4M); with c > 3m (M ≥ 4m) it suffices that
θ ≤ 11/16 (⇔ Def := Σ_Ap (M − w) ≥ mM/4). Non-two-face, m ≤ 20, generators < 4m, c > 3m: max θ = 0.664
(⟨8,27,30,31⟩); extremals are three-face-like (core ≤ 1 cell). Two-face θ reaches 0.6935 (> 11/16, handled by the
theorem). Continuum model: D = three-triangle cylinder minus cone (q* + ℝ³₊) with q* = r·(1,1,1): Monte Carlo θ(r) =
0.6684 (r = .01), .6714 (.03), .6735 (.05), .675 (.07), .676 (.09), **.6766 (.12)**, .6758 (.15). So the continuum
sup over this family ≈ 0.677 < 0.6875 but > 2/3: a homogeneous (shape-only) θ bound has margin ≈ 0.011 and needs the
lattice-tile condition (cylinder structure) at least.

**General e = 4 faces+core identity (face_core_ident.py; 7,019 e = 4 S, m ≤ 14, generators < 3m, 2,243 with
nonempty core: exact).** With L_i = axis lengths, Def_faces = Σ over the 2-D runs lying in the three coordinate faces
(each axis run once) of |R|(M − w(end R)), SumAxes = Σ_i p_i L_i(L_i−1)/2, core = {x ∈ D : min x ≥ 1}:
    3mW + 3m(m−1) = (m − 4(L_1+L_2+L_3−2))·M + 4·Def_faces + 4·SumAxes + 4·Σ_{x∈core}(2M − 3w(x)).
Proof (PROVED). CH' in the form mW + m(m−1) = 3mM − 4Σ_D w. AP identity on each face run, summed: a face cell with one
zero coordinate lies in 2 face runs and contributes 2w + (w) = 3w; an axis cell k e_i (k ≥ 1) lies in 3 face runs and
contributes 4w; the origin 0. Total face-run length = 2|F| + ΣL − 2 (F = D ∖ core). Hence
3Σ_F w + SumAxes = (2|F| + ΣL − 2)M − Def_faces. Eliminate Σ_F w from 3·CH' using |F| = m − |core|. ∎
(For two-face tiles core = ∅, L_1 = L_2 = 1: reduces to the two-face identity.) Since w(x) ≤ M, each core cell
contributes ≥ −M; core cells with w ≤ 2M/3 contribute ≥ 0.

## 2026-10-18 (night 13, cont.) — non-two-face e = 4: height criterion H ≥ m − 1 (shape-only), B1, hybrid

**Failure map of existing criteria on NON-two-face e = 4, c > 3m (nt_fail.py, nt_T.py; gens < 3m).** τ-criterion fails
only at m = 19 (7 S), 23 (2), 25 (27), 27 (29), 31 (1), 43 (1); max excess per m for 28 ≤ m ≤ 44 mostly −1..−12.
T(X) ≤ 2m+1 (⇔ N ≥ m−1) fails only m ≤ 27; shape-only T(A) ≤ 2m+1 fails up to m = 33 (excess ≤ 7). Failing tiles are
small compact "staircase" shapes (L ≈ 5,5,5, core 1–3). Correction to night 12: the three-triangle shape (faces = full
triangles of side L, q* = (1,1,1)) has T(A) = 2m + 6L − 8 (not ≈ 3m) and **is never a lattice tile** (tri3 check
L = 3..8: no p mod m with p_1+p_2+p_3 ≡ 0 is injective on it).

**Height criterion (PROVED, elementary, any e = 4).** For a column top t let ht(t) = max{|y − t| : y ∈ D, y ≥ t}.
Since every p_a ≥ m + 1, M − w(t) ≥ w(y) − w(t) = p·(y − t) ≥ (m+1)|y − t|. Summing over incidences (CH'):
    mW + m(m−1) = Def_all ≥ (m+1)·H(D),   H(D) := Σ_{x∈D} Σ_a ht(t_a(x))   (shape-only).
So **H(D) ≥ m − 1 ⇒ Wilf**. (General e: (m+1)H ≥ (e−2)m(m−1)/2 ⇒ Wilf.) Refinements: tops t ∉ X have deficit ≥ m and
≥ (m+1)ht(t), so mW + m(m−1) ≥ m(N + H₂), H₂ = Σ (ht − 1)⁺ ⇒ **hybrid: T(X) ≤ 2m + 1 + H₂ ⇒ Wilf**; and
B1 := Σ_{(x,a)} max_{y∈A, y≥t}[(m+1)|y−t| + δ̂(y)] (δ̂ = m off X, m − π on X) ≤ Def_all.
**Data (heightB.py, heightH_climb.py, heightH_rand.py, hybrid.py; NON-two-face, all c):**
 - HT: H ≥ m − 1 holds for every non-two-face tile with 24 ≤ m ≤ 36 (gens < 3m, exhaustive) and in 40 adversarial climbs
   (m ∈ [24,60], gens < 10m; min H − (m−1) = 2 at m = 25). Fails only m ∈ {15,16,17,19,20,23}, by ≤ 4.
   min H − (m−1) for m = 24..36: 8, 2, 5, 2, 4, 7, 10, 12, 12, 10, 12, 14, 16. Random tiles: min H/m = 1.58 (m=40),
   1.98 (60), 3.0 (90), 3.8 (130) — grows ~ m^{1/2}.
 - B1 ≥ m(m−1) for every non-two-face S, 10 ≤ m ≤ 36 (gens < 3m), margin (B1 − m(m−1))/m ≥ 8, ≈ 1.5m at m = 36.
 - hybrid fails only ⟨15,17,18,23⟩-type (m = 15,16,17), ⟨19,20,25,27⟩ (−4), ⟨23,25,28,35⟩ (−1).
 - per-view: H^{(a)} ≈ m/3 each in extremal tiles; no single view suffices.
**Structure for a proof (PROVED pieces).** (i) h_a = min(f(v_b), g(v_c), Q) (cylinder lemma) ⇒ level sets E_k of h_a are
L-shaped strips ∩ B_a; strict corners = maximal cells. H^{(a)} = Σ_k k Σ_{u∈E_k} ht_{E_k}(u) ≥ m − CM_a, CM_a =
Σ_{y∈A}(y_a+1). (ii) Neighbor map: for an a-top t, t + e_a ∈ D + λ with (t + e_a − λ)_a = 0; t ↦ t + e_a − λ is a
bijection {a-tops} → B_a; for maximal y the three neighbors λ_1, λ_2, λ_3 are pairwise distinct, and (non-two-face) at
most one has λ_a = y + e_a (else e_a − e_b ∈ Λ). The a-tops grouped by neighbor ("contact regions", constant height λ_a)
translate to a PARTITION of the face B_a. (iii) Each a-top z under the foot [π(λ_a), π(y)] of a maximal y has
ht(z) ≥ |π(y) − π(z)|.
**Target lemma HT:** every non-two-face 3-D lattice tile with m ≥ 24 has H(D) ≥ m − 1. With BGOW (m ≤ 18) and a
shape-by-shape finite check for 19 ≤ m ≤ 23 this would prove Wilf for all non-two-face e = 4, hence (with the two-face
theorem) **Wilf for e = 4**.

## 2026-10-18 (night 13, late) — COMPLETE tile enumeration; Wilf for every e = 4 semigroup with m ≤ 60 (computer-assisted)

**Complete enumerator of 3-D Apéry tiles (src/tile_enum.py).** For residues r = (p_1,p_2,p_3) mod m the grlex tile
depends only on the lattice Λ_r = {x : r·x ≡ 0 (m)} and the open Gröbner cone containing p + ε(1,1,1) + ε²(lex)
(grlex tie-break = limit of an adjacent open cone). Cone of a tile D = {p : p·(q − rep(q)) > 0, q minimal non-element}.
The positive orthant (slice p_1+p_2+p_3 = 1) is a polyhedral fan of such cones; BFS by facet flips (flip point = facet
midpoint pushed out by ε, ε halved until the new cone's closure contains the midpoint; exact Fractions) visits all of
them. Lattices taken up to units of ℤ/m and coordinate permutations, residues distinct and nonzero (forced for minimal
generators). Validation (src/scratch/tile_enum_validate.py, logs/tile_enum_validate.log): every grlex tile of every
e = 4 semigroup ⟨m,a,b,c⟩ with gens < 5m, m = 5..13 (≈ 36,000 semigroups) is in the enumeration: 0 missing. Counts:
m = 10: 21 lattices / 255 tiles; m = 20: 2,501; m = 40: 20,436; m = 60: 79,051 (31,156 non-two-face).

**Per-tile LP certificate (src/tile_lp.py) — PROVED (elementary).** By CH', mW + m(m−1) = Def(p) := 3m·M(p) − p·T(D)
(T(D) = Σ_{(x,a)} t_a(x) ∈ ℕ³, M(p) = max_{x∈D} p·x). Def is convex and positively homogeneous in p, so over
{p ∈ closed cone C_D, p_a ≥ m+1}: Def(p) ≥ (m+1)·κ_D, κ_D := min_{p ∈ C_D ∩ simplex} Def(p)/min_a p_a. On each cell of the
arrangement {p·x = p·x' (x,x' maximal)} ∪ {p_a = p_b} ∪ edges(C_D ∩ simplex) the ratio is linear-fractional, so the min
is at an arrangement vertex; we enumerate them exactly. **(m+1)κ_D ≥ m(m−1) ⇒ Wilf for every semigroup with tile D.**

**COMPLETE SCAN (src/scratch/tile_scan_H.py, logs/tile_scan_H.log), m = 7..60 (running on to 70).** Every
non-two-face tile satisfies HT (H ≥ m − 1) except at m ∈ {8, 15, 16, 17, 19, 20, 23} (one, two, two, two, one, two, one
tiles); all of these except the m = 8 tile (covered by BGOW, m ≤ 18) are LP-certified. min H − (m−1) for m = 24..60:
8,2,5,2,4,7,10,12,12,10,12,14,16,14,17,20,22,24,27,22,24,26,28,36,35,34,40,42,44,46,48,52,47,46,56,43,60 (m = 61: 74).
**⇒ COMPUTER-ASSISTED THEOREM: Wilf's conjecture holds for every numerical semigroup with e = 4 and m ≤ 60.**
(Two-face tiles: two-face theorem, all m. Non-two-face: HT or LP certificate; m = 8: BGOW.) Trust base: fan traversal
completeness (standard Gröbner-fan facts; validated m ≤ 13), the CH' identity (LEAN), code correctness. NOT yet
independently re-implemented. Remaining gap for e = 4: **HT for non-two-face tiles with m > 60 (or wherever the scan ends).**

**Data toward the asymptotic step (all complete enumerations, non-two-face).**
 - max |A| = 8 (m ≤ 32), 9 (36–40), 10 (44–48). Type is unbounded for e = 4 (Backelin ⟨213,216,226,227⟩: |A| = 15,
   non-two-face, H − (m−1) = 896). Bresinsky ⟨(2h−1)2h, (2h−1)(2h+1), 2h(2h+1), 2h(2h+1)+2h−1⟩ (two-face): |A| = 4h−3
   ~ 2√m, P₂(A) + 2|A| − m − 1 = 4h − 5 > 0 while H − (m−1) ≈ 1.75h⁴ — **the |A|/P₂ (Cross-Lemma) route cannot work in
   general**; HT itself has huge slack there.
 - N-counts (n(x) = #maximal tops of x; HT ⇔ N₃ ≤ N₁ + 2N₀ + 1 + H₂): min(N₁ + 2N₀ − N₃) = −4, −1, 0, 0, 5, 3, 7 at
   m = 16, 24, 30, 36, 40, 44, 48: **H₂ is needed** below m ≈ 37; N₀ = 0 occurs at every m ((1,2,k) family).
 - Contact pieces (tile_pieces.py): Hp := Σ_{a,λ} λ_a S(P_λ) ≤ H; min Hp − (m−1) = −4 (m=20), 1, 5, 10, 17, 17, 24 at
   m = 24, 30, 36, 40, 44, 48: **Hp ≥ m − 1 for all tiles with 24 ≤ m ≤ 48.** Singleton pieces cost λ_a/3 each
   (weight σ up to 75 at m = 48); the surplus comes from a few large "fin" contacts (e.g. m = 51 min-H tile: one piece
   |P| = 19, S = 43, w = 1 pays 37 of the 38 margin).
 - q*-classes: tiles without q* are the tight class (min H − (m−1) = 11, 16 at m = 30, 36); three-face tiles
   (q* = (1,1,1)) are slack (30, 55); other q*: 10, 22.

**Exact terrace formula (PROVED, any finite down-set D ⊂ ℕ³).** For an a-top t, every up-path from t stays in the layer
x_a = t_a (moving +e_a from any v ≥ t in that layer would give t + e_a ∈ D). Hence ht(t) = ht_{S^a(t_a)}(π_a t), where
S^a(k) = π_a(D ∩ {x_a = k}) (a 2-D down-set), and
        H_a = Σ_k (k+1) Σ_{u ∈ S^a(k) ∖ S^a(k+1)} ht_{S^a(k)}(u).
For a q*-free cylindrical tile S^3(k) = F_3 ∩ [0,X(k)) × [0,Y(k)) (X, Y = row lengths of F_2, F_1 at height k), and the
band S(k) ∖ S(k+1) = V ∪ Hz with V = F_3 ∩ [X(k+1),X(k)) × [0,Y(k)), Hz = F_3 ∩ [0,X(k)) × [Y(k+1),Y(k)) — each a translated
2-D down-set, so Σ_band ht ≥ |band|/3 unless V or Hz is a single cell. **Single cells occur only at exposed outer corners
of the faces with a unit step**: V = {pt} ⇔ X(k+1) = X(k) − 1 and (X(k)−1, 1, k) ∉ D; the cell is y = (X(k)−1, 0, k), a
maximal element on F_2 lying in the fin Φ_2 = {x ∈ F_2 : x + e_2 ∉ D} = F_2 ∖ [0, a_2) × [0, b_2) (a_2 = #{i : h(i) ≥ 2},
b_2 = g(1)), an L-shaped up-set of F_2. Fin cells have singleton normal columns and ht = ht_{F_2} there, so
H_2 ≥ Σ_{u∈Φ_2} ht_{F_2}(u): the fin pays for its own corners when it is large.

**Cylindrical sets are NOT enough (src/scratch/cyl_exhaust.py, cyl_search.py).** q*-free cylindrical non-two-face sets
D = {x_2 < h(x_1), x_3 < min(f(x_1), g(x_2))}: exhaustive for |D| ≤ 22 — HT fails at every size 13..22 (min −7 at 17);
annealing: −2 at m = 30, then +5, +7, +13, +29, +97 at m = 36, 45, 48, 60, 100 (upper bounds on the min). With one
removed cone (q*): three triangular fins (faces = triangles of side n, q* = (1,1,1)) have exactly H = 3·C(n−1,3),
m = (3n² − 3n + 2)/2, so **HT fails for n ≤ 7 (m ≤ 64)**; annealing also finds q* = (2,1,1) shapes with −11 at m = 48.
These shapes are not lattice tiles (tri3 check; walls). ⇒ for q*-tiles the lattice is essential at least up to
m ≈ 64; for q*-free tiles the cylinder structure alone plausibly suffices from m ≈ 32 on.

**Wall lemma (lattice ingredient, from the cylinder lemma).** Inner corners q_j = (α_j, β_j, 0) of F_3 (α increasing)
satisfy q_j ≡ t_j e_3 with distinct t_j, and the translates D + (q_j − t_j e_3) are disjoint from each other and from D:
at height 0 the translate occupies (α_j, β_j) + S^3(t_j). For j < k: α_k − α_j ≥ X(t_j) or β_j − β_k ≥ Y(t_k). A unit
step (Δα = Δβ = 1) therefore needs t_j ≥ f(1) or t_{j+1} ≥ g(1): unit steps of F_3 consume distinct t-values from the
part of the x_3-axis where F_2 or F_1 has width 1 (a spike/fin, which itself contributes ≈ C(len, 2) to H). This is the
mechanism that kills triangular fins in tiles.

**Failed attempts this round.** (1) Grid-box decomposition (boxes from minimal-non-element breakpoints): degenerates to
unit boxes, bound −(m−1) — useless. (2) N-route without H₂: fails (above). (3) Local rule "maximal y owns y − e_a when
y − e_a + e_b, y − e_a + e_c ∉ D": covers interior maximal elements but leaves face/axis ones (≤ 8 per tile at m = 30).
(4) HT for all cylindrical sets: false up to m ≥ 30 (q*-free) and m = 64 (q*).

**Next precise target.** Asymptotic HT in two parts: (A) q*-free cylindrical sets with m ≥ m_A: prove
Σ_{a,k}(k+1)[Σ_band ht − |band|/3] ≥ −1 by charging exposed unit-step face corners to the fin of that face (Φ_c) and
to the spike/arm cells (stretch argument along columns); (B) tiles with q*: wall lemma ⇒ unit steps are paid by spikes.
In parallel push the complete scan beyond 60 (parallel/compiled) to lower the analytic threshold requirement.

## 2026-10-18 (night 14) — Peeling induction; exhaustive cylinder class to |D| = 44 (C); cone-layer reduction

**Peeling identity (PROVED, any finite down-set D ⊂ ℕ³).** For D'_c = {x : x + e_c ∈ D}: chains from x in D' are chains
from x + e_c in D, and a-rays commute with the shift, so h_{D'}(x) = h_D(x + e_c) (h(x) = Σ_a ht(top_a x)). Hence
H(D) = H(D'_c) + Σ_{x∈F_c} h(x) and, with δ(D) := H(D) − (|D| − 1),
        δ(D) = δ(D'_c) + Ψ_c(D),   Ψ_c(D) := Σ_{x ∈ F_c} (h(x) − 1)        (F_c = {x ∈ D : x_c = 0}).
Iterating to ∅ just re-sums δ = 1 + Σ_x (h(x) − 1); the content is in the induction class. Also H = Σ_y w(y)·ht(y) with
w(y) = Σ_{a : y+e_a ∉ D} (y_a + 1) and ht(y) = max{|z| : z ∈ D, z ≥ y} − |y|.

**Class 𝒞 (Loomis–Whitney down-sets).** D = {x : π_c(x) ∈ A_c for c = 1,2,3} for three compatible 2-D partitions A_c —
exactly the q*-free cylindrical sets {x_2 < h(x_1), x_3 < min(F(x_1), G(x_2))} (two-face and degenerate included).
𝒞 is symmetric and closed under peeling. A cylinder minus one cone q* + ℕ³ lands in 𝒞 after q*_c peels in direction c
(the cone becomes the cut {x_a ≥ q*_a, x_b ≥ q*_b}, which only lowers one face function) — PROVED.

**Exhaustive enumeration of 𝒞, |D| ≤ 44 (src/c/cyl_class.c, C, independent of the Python code; ≈ 3.3·10^8 sets,
logs/cyl_class_44.log; agrees with peel_class.py at |D| = 9, 13, 15, 16).** Per size: min δ / min max_c Ψ_c:
 |D| ≤ 30: min δ < 0 at every size 3..30 except 1, 2; **global min δ = −7** (|D| = 16, 17); at 29: −4, at 30: −2.
 **31..44: min δ = 0, 2, 1, 0, 2, 5, 6, 8, 6, 8, 8, 9, 11, 9 — HT holds for every D ∈ 𝒞 with 31 ≤ |D| ≤ 44.**
 (P1) max_c Ψ_c ≥ 0: fails only for |D| ≤ 19 and at |D| = 29 (two sets, −1); min max Ψ = 3..8 for |D| = 31..44.
 Peeling the largest face is NOT enough (min Ψ = −8 at 28..44). Slack (logs/cyl_class2_38.log, src/c/cyl_class2.c):
 max_c(3Ψ_c − |F_c|) ≥ 0 for 33 ≤ |D| ≤ 38; max_c(2Ψ_c − |F_c|) < 0 throughout ≤ 38.
 (This supersedes the night-13 cyl_exhaust figures: that run's pruning was too aggressive — complete only for |D| ≤ 19,
 not 22 as written; the corrected Python script and the C code agree.)
 Extremal sets are small and thin (unit-width spikes, staircase faces of side 5–6); the triple staircase
 {x_1+x_2, x_1+x_3, x_2+x_3 < n} has δ = 2, 8, 49, …, 2242 (n = 3..12): fat sets have huge slack.

**REDUCTION (PROVED): HT for all non-two-face tiles with m ≥ 31 follows from (I) + (II):**
 (I) [𝒞-theorem] every D ∈ 𝒞 has δ(D) ≥ −7, and δ(D) ≥ 0 when |D| ≥ 31;
 (II) [cone lemma] every non-two-face tile T with a cone q* has a direction c with
      S_c := Σ_{k<q*_c} Ψ_c(T_k) ≥ 7, or S_c ≥ 0 and |T_{q*_c}| ≥ 31        (T_k = k-fold peel of T in direction c).
 Proof: tiles without q* lie in 𝒞; otherwise δ(T) = S_c + δ(T_{q*_c}) with T_{q*_c} ∈ 𝒞. ∎
 (I) is verified for |D| ≤ 44 and follows for all sizes from **(P1*)**: for |D| ≥ 45 there is c with Ψ_c(D) ≥ 0 and
 (|D| − |F_c| ≥ 31 or Ψ_c(D) ≥ 7) (strong induction on |D|). (P1*) and (II) are the two OPEN analytic statements.
 **q* ∈ Λ (PROVED):** reduced Gröbner-basis binomials of the saturated lattice ideal I_Λ have disjoint supports, and q*
 has full support, so its binomial is x^{q*} − 1.
 Data for (II) (src/scratch/tile_cone_peel.py, tile_cone_stats.py, complete enumerations): min over q*-tiles of max_c S_c
 = 8, 11, 22, 22 at m = 24, 30, 36, 40 (requirement met with margin ≥ 1, 4, 15 at m = 24, 30, 36). q* is (1,1,k) for
 the vast majority (m = 40: 805 of 1015), else (1,2,k), (1,3,k), (2,2,2). A single cone layer can have Ψ = −4.
 Tiles (no lattice-free analogue): peeling the largest face gives Ψ ≥ 0 for every tile at m = 24, 30 (min 0, 2).

**Scan:** m = 68 complete (36,279 non-two-face tiles, HT fails 0, min δ = 80; logs/tile_scan_H_68.log, running on).

### Night 14 (cont.) — MAXSUM (heights dropped), private cells, peeling rules

**MAXSUM criterion (PROVED ⇒ HT).** H = Σ_y w(y)·ht(y), Σ_y w(y) = 3m, ht ≥ 1 off Max ⇒ H ≥ 3m − M3 with
M3 := Σ_{y∈Max(D)} (|y| + 3) = #{(x,a) : top_a(x) maximal}. So **M3 ≤ 2m + 1 ⇒ HT** (this is the old "N-route without
H₂": M3 ≤ 2m+1 ⇔ N₃ ≤ N₁ + 2N₀ + 1; night 13 called it refuted because it fails for small m).
Complete enumeration (src/scratch/tile_scan_HM.py; logs/tile_scan_M_7.log, tile_scan_HM_*.log), min slack 2m+1−M3 over
non-two-face tiles: fails at m = 8, 10, 15–23, 25–28, **33 (2 tiles, −2), 38 (1 tile, −1)**; holds for m = 24, 29–32,
34–37 and **every m ∈ [39, 54]** (slack 1..10) and m = 71, 72, 73, 91, 101 (slack 12, 13, 14, 28, 27). Margin ≈ (m − 38)/2.3,
far below HT's (≈ 0.9(m − 20)). Over the cylinder class 𝒞 (src/c/cyl_class3.c, |D| ≤ 40) MAXSUM fails massively
(min slack −11..−15 for 31..40; tens of thousands of sets): **MAXSUM is a lattice phenomenon** (staircase flaps make
N₃ large; in tiles the wall lemma forces axis spikes whose cells have n ≤ 1).
**Structure (PROVED, any down-set).** For non-maximal x, n(x) = 3 iff x is a *tripod centre* (x + s_a e_a maximal,
s_a ≥ 1, a = 1,2,3); crosses of two maxima meet in ≤ 1 cell (their meet). Hence MAXSUM ⇔
#crowded + #tripods ≤ 1 + 2N₀ + Σ_y (priv(y) − 1)⁺, priv(y) = #non-maximal cells lying only on the cross of y, crowded ⇔
priv = 0. Tiles (src/scratch/tile_private.py): ≤ 5 crowded maxima and ≤ 4 tripods per tile for m ≤ 50; the excess is
paid by axis spikes (e.g. m = 50, r = (1,7,15): three unit-step corners of F_2 crowded, x_2-spike gives 13 excess).
**Peeling rules over 𝒞** (src/c/cyl_class4.c, |D| ≤ 36): shortest axis (min Ψ −4..−5), longest axis (−8), largest face
(−8) all fail; **Σ_c Ψ_c ≥ 0 for every D ∈ 𝒞 with 30 ≤ |D| ≤ 36** (min 1, 1, 5, 1, 2, 6, 7) — a symmetric statement
Σ_x z(x)(h(x) − 1) ≥ 0 (z = #zero coordinates), stronger than (P1).
**Unpaid-peak analysis for 𝒞 (PROVED; = terrace formula re-derived).** 3δ − 3 = Σ_c Γ_c, Γ_c = Σ_{u∈A_c} ℓ_c(u)(3π_c(u) − 1)
(π_c = height of the column top). Per level v, γ_v = Σ_{L_v}(3 ht_{U_v} − 1) ≥ g(V_v) + g(Hz_v) for the two arms of
L_v = U_v ∖ U_{v+1}, and g(P) ≥ −1 with equality iff P is one cell (L-tromino: 0). An interior maximum is never a
singleton (in 𝒞, y − e_a + e_c, y − e_b + e_c ∈ D force y + e_c ∈ D). Singletons = exposed planar corners with a unit
step on that side; cost = the corresponding coordinate + 1. For lattice tiles: a corner unpaid in face c has
σ_c(y) on an axis (σ_c = translation by e_c mod Λ, a bijection B_c → F_c), so unpaid corners inject into axis points.

### Night 14 (late) — CHT: counting criterion #{h ≥ 2} ≥ #{h = 0} − 1; type bound; corner inequalities

**CHT (PROVED ⇒ HT, any finite down-set D ⊂ ℕ³).** δ = 1 + Σ_x (h(x) − 1) with h ≥ 0 integer, so
#{h ≥ 2} ≥ #{h = 0} − 1 ⇒ δ ≥ 0. Structure of h (PROVED): with n(x) = #{a : top_a(x) maximal} (top_a(x) = end of the a-ray),
 {h = 0} = Max ∪ Tri (Tri = tripod centres: non-maximal, n = 3); h = 1 ⇔ n = 2 and the third top has height 1;
 n ≤ 1 ⇒ h ≥ 2. Counting cells with n = 2 via pairs of maxima: N'_2 + 3|Tri| = P_2 (P_2 = #pairs of maxima agreeing in
 exactly one coordinate). Hence CHT ⇔ **2t + 2|Tri| + Q' ≤ m + 1**, t = |Max|, Q' = #{x : n(x) = 2, h(x) = 1}.

**Type bound (PROVED for 𝒞):** t ≤ c(A1) + c(A2) + c(A3) + 2 =: C + 2, c(A) = #outer corners of face A. For a maximal y
each coordinate is blocked by one of two faces (x1 by R3/R2, x2 by C3/C1, x3 by T2/T1); the blocking combos {R3,C3},
{R2,T2}, {C1,T1} host the column top over a face corner (injective per face), and the two cyclic combos (R3,C1,T2),
(R2,C3,T1) are fixed points of a nonincreasing composite map — ≤ 1 maximum each. (With a cone: + O(1) via Q-blocking.)

**Lattice-free evidence (exhaustive):**
 𝒞, |D| ≤ 40 (src/c/cyl_cht.c, logs/cyl_cht_40.log, logs/cyl_cht_36b.log): **max(t − C) = −2** (every size 6..40);
 **max(2t + 2Tri + Q' − 4C) = −10** (tight for boxes); max(2Tri + Q' − 2C) = −6; max(Tri − C) = −3; max(Q' − C) = +1;
 max C/√|D| ≤ 2.42 (decreasing, 2.21 at 40). CHT itself fails on 𝒞 at |D| ≤ 39 (min slack −4..−1), holds at 40 (+1).
 Cone class (cylinder minus one cone q ≥ (1,1,1), faces with union ≤ 24; src/c/cone_class.c, logs/cone_class_24.log):
 max(t − C) ≤ 0, max(2Tri + Q' − 2C) ≤ −3, max(LHS − 4C) ≤ −3 for every size 7..24; max(2Tri + Q' − 2t) rises
 −4 → 0 (so Tri/Q' are NOT controlled by t alone in the cone class); maxTri 7, maxQ' 11 at 24.
**Conjectured (A4) on 𝒞:** (A4a) t ≤ C − 2, (A4b) 2Tri + Q' ≤ 2C − 6, hence 2t + 2Tri + Q' ≤ 4C − 10.
**(B) corner bound (sketch, not yet rigorous):** |A| ≥ k(k+1)/2 + arms for a face with k corners, and
|A1 ∪ A2 ∪ A3| ≤ m; at most two faces can be "staircase flaps" without the third losing area ⇒ C ≲ √(6m) + 1.5.
(A4) + (B) ⇒ 2t + 2Tri + Q' ≤ 4√(6m) − 4 ≤ m + 1 for m ≥ 94 — i.e. **CHT, hence HT, for every 𝒞-tile with m ≥ 94**;
the cone version (constant −3) gives m ≥ ~100. With the scan (complete to m = 101 at last check, running to 115) this
would close G2' for tiles if (A4)/(B)/cone-(A4) are proved.

### Night 14 (latest) — CHT pieces proved: t ≤ C − 2, C² − 3C + 6 ≤ 6m, qU-forest; (K) refuted; cone class needs the lattice

Full statements/proofs in PROOFS.md ("e = 4, asymptotic HT via CHT").
**PROVED (𝒞):** Lemma T (t ≤ C − 2; level telescoping t = c(A₃) + Σ_v ν_v, ν_v ≤ [a drops] + [b drops]);
Lemma B (C² − 3C + 6 ≤ 6m, also for the cone class); Lemma F (unit-notch Q' cells form a forest on Max ⇒ qU ≤ t − 1).
**PROVED (cone class):** t ≤ C (the cone adds ≤ 2 new corners at level q₃).
**Cone class is different (lattice-free):** three staircase faces with q = (1,1,1): t = C − 3, Tri = C − 5 (axis tripods),
Q' = C − 9 ⇒ LHS = 5C − 25; CHT holds there only from k = 9 (m = 109). Exhaustively (src/c/peel_lhs.c, cone_split.c)
max(LHS − 4C) in the cone class rises −3 (≤ 27) → +1 (30), max(2Tri + Q' − 2t) → +3 (31–32).
**Real cone tiles look like 𝒞** (src/scratch/tile_cht_cone.py, logs/tile_cht_cone.log): m = 30/40/50: max(t − C) = 0,
max(LHS − 4C) = −5/−3/−5, max C/√m = 1.64/1.90/1.70, CHT slack ≥ 3/9/13; (K)-quantity 2Tri + Q' − 2t ≤ −3 (m ≤ 36,
logs/tile_K.log). ⇒ for cone tiles the lattice must enter (or a 5C-type bound + scan to ≈ 150).
**Ω = 2Tri + qO:** Ω ≤ C − 2 holds exhaustively (𝒞, ≤ 34) but annealing (src/scratch/cls_anneal.py) finds Ω − C = +5 at
m = 248 — FALSE; the split LHS ≤ 3t − 1 + Ω is lossy (when Ω is big, t and qU have slack).
**Conjecture (K) 2Tri + Q' ≤ 2t − 2 (would give LHS ≤ 4t − 2): exhaustive on 𝒞 for |D| ≤ 32 (max exactly −2), but FALSE:**
annealing counterexample h = (8,5,4,3,2,2), F = (10,8,3,3,3,2), G = (10,9,7,6,3,3,2,1), m = 104: t = 13, Tri = 5, Q' = 16
(qU 10, qO 6), C = 16 — K = 0; confirmed with the independent tile_cht.cht. It is EXACTLY tight for (A4b) 2Tri + Q' ≤ 2C − 6
and has LHS − 4C = −12, CHT slack 53. Lesson: small exhaustive ranges (≤ 32) miss mechanisms that need ≥ 6 corners per face.
**Other refuted helpers:** per-level form of (K) (fails from |D| = 16, levels compensate); single-peel monotonicity of
LHS − 4C (fails at 17, 28–30 on sets with slack ≥ 1) and of K; o-pair bound 3Tri + qO ≤ C − 2 (fails at 27);
tripod row-end injection (two tripods can share their row-end maximum: h = (4,3,1,1), F = (3,2,1,1), G = (3,1,1,1)
has t = 5, Tri = 2 sharing (3,0,0) — 2Tri = t − 1 tight).
**Observed (𝒞, |D| ≤ 15):** tripod hypergraph on Max is Berge-acyclic (⇒ 2Tri ≤ t − 1 if true); qO graph is a forest
(⇒ qO ≤ t − 1); mixtures have cycles. Annealing to m ≈ 200: 2Tri − t ≤ −1, qO − t ≤ −1 not violated.
**Status of the 𝒞 route:** proved LHS ≤ 3t − 1 + Ω. Two candidate closings:
 (a) (A4b) 2Tri + Q' ≤ 2C − 6 (no violation: exhaustive ≤ 34, annealing m ≤ 250 incl. restarts from the K-counterexample)
     ⇒ LHS ≤ 4C − 10 ⇒ CHT for m ≥ 88;
 (b) 2Tri ≤ t − 1 and qO ≤ t − 1 (hyperforest/forest) ⇒ LHS ≤ 5t − 3 ≤ 5C − 13 ⇒ CHT for m ≥ 131 (scan must reach 130).

## 2026-10-18 (night 15) — 𝒞 closed for m ≥ 131: tripod forest + qO forest (PROVED); vector peeling data

**Result (PROVED on paper, PROOFS.md "Theorem C-HT").** For every Loomis–Whitney set D ∈ 𝒞: 2|Tri| ≤ t − 1 (Lemma TF),
|qO| ≤ t − 1 (Lemma QF). With qU ≤ t − 1 (Lemma F) and t ≤ C − 2 (Lemma T) this gives LHS ≤ 5t − 3 ≤ 5C − 13. With CHT and
Lemma B, δ ≥ 0 for every D ∈ 𝒞 with |D| ≥ 131. So **Wilf holds for every e = 4 semigroup whose tile lies in 𝒞 and has
m ≥ 131.** The remaining e = 4 gaps are cone-class tiles (all m beyond the scan) and the unscanned m ≤ 130.

How it was found. The vector-peel data (E126) showed that a fixed potential needs growing peel vectors: |s| = 2 is
needed at 17 and 28–30, and |s| = 3 by 31–34 is used with growing counts. So I stopped that line. Per-level telescoping of
(A4b) is exactly single peeling, and it fails at 18. Instead I tested elimination orders on the incidence hypergraphs.
Every order passes for tripods, and increasing |x| passes for qO. That pointed to two local statements:
- Lemma S (one line, uses only that an LW set is cut out by its projections): two cells whose three forward neighbours
  all lie in D can share a maximal top only in the same direction.
- Lemma P: tripod projections to any coordinate plane form a chain. The proof uses the peak inequalities
  F(X+1) < G(Y) and G(Y'+1) < F(X'), which close into a cycle of strict inequalities.
- For qO with non-maximal direction 3 at p = (X, Y): an earlier qO on the 1-ray forces F(X) < G(Y), and one on the 2-ray
  forces G(Y) < F(X). Both of x′'s possible types give the same inequality: a peak via P0, a plateau-1 point via the
  plateau inclusion P1.
Elimination: tripods in decreasing |x| each bring ≥ 2 new maxima; qO cells in increasing |x| each bring ≥ 1.

**What did not work tonight (preserved, E126/E127).**
- Single peel needs |s| up to 3 at |D| ≤ 34, with growing counts.
- Per-level (A4b) fails at 18.
- Simple parent-direction rules for tripods (longest/shortest arm, fixed direction) fail at 9.

**Cone class: the new obstacle.** Lemma S uses the LW property, which fails near q*. Lattice-free cone data: 2Tri − t ≤ 8
and qO − t ≤ 1 at union ≤ 32, and the three-staircase family makes 2Tri − t unbounded. Real cone tiles (m ≤ 50):
LHS − 4C ≤ −3. Next: (1) localize the failures of Lemmas S/P/QF to cells near q* and count them with the tile lattice
(q* ∈ Λ, wall lemma). (2) Alternatively prove a cone bound LHS ≤ 5C + β and scan up to the matching threshold.

## 2026-10-18 (night 16) — cone tiles: the Lattice Corner Lemma, the pairwise relaxation PW, corner–area data

**Goal of the night.** The cone class is the last gap for e = 4. Proving LHS ≤ 5C + β there needs lattice input beyond
Wall/Floor, or a better corner–area bound than Lemma B, or both. Threshold arithmetic (PROVED, trivial): if C ≤ 2√m + c
and LHS ≤ 5C + β then CHT gives HT once m − 10√m − 5c − β + 1 ≥ 0. For (c, β) = (2, −2): m ≥ 114; (2, 5): 127;
(3, 5): 136. So a sharp-constant corner bound plus a crude forest bound would close e = 4 with the scan up to ~130.

**Lattice Corner Lemma (PROVED, PROOFS.md).** Let w, w' be non-axis inner corners of A_c (w left of w'), α = Δx_a,
β = −Δx_b, t, t' their cylinder-lemma multipliers. Then t' > t ⇒ t' − t ≥ #{z : βe_b + ze_c ∈ D}, and t' < t ⇒
t − t' ≥ #{z : αe_a + ze_c ∈ D}. (v = λ' − λ is a nonzero lattice vector, and v⁺, v⁻ cannot both lie in D.) With the
Wall Lemma (quadrant corners have t ∈ [L_c − q_c, L_c − 1]) this kills the 2×2-block excess pattern by hand: for h=(4,3,2,1),
F=(6,5,1,1), G=(6,4,1,1), q*=(1,1,3), the three quadrant corners need t ∈ {3,4,5}, but LCL needs consecutive gaps ≥ 4.

**PW relaxation (necessary condition, PROVED).** All face inner-corner vectors (w, −t_w e_c) (unknown t_w) and q*, with
all pairwise differences and sums, satisfy NOT(v⁺ ∈ D ∧ v⁻ ∈ D). Data (E130):
- Every real tile passes, as it must.
- Every one of the 4,311 Wall+Floor sets with tripod excess fails.
- On the PW class (union ≤ 34): 2Tri − t ≤ −1, qO − t ≤ −2, qU − t ≤ 0, LHS − 5C ≤ −6.
So the needed lattice input is captured by pairwise Gröbner-vector consistency. Caveat: tiles can have a tripod CYCLE
(m = 23 example in E130). The forest statement is false for tiles, and the bound must use maxima unused by tripods; in
real tiles, r(B) = 1 only with ≥ 2 unused maxima.

**Corner–area (E129, E131).**
- Real tiles: C − 2√m ≤ +0.05 (m = 30) and decreasing (−1.0 at m = 64); the smallest face has ≤ 4 corners for m ≤ 64.
- Annealing: 𝒞 reaches C − 2√m = 2.17. Wall+Floor cone sets stay ≤ 1.64 up to m = 160; the extremal shape is two
  staircase faces inside one slab x_c < q_c.
- 𝒞 proof sketch: with k₁ ≥ k₂ ≥ k₃, m ≥ ΣT(k) + ΣL − 2 + |P(k)|, where P(k) = {(u,w,z) ≥ 1 : u+w ≤ k₃−1,
  u+z ≤ k₂−1, w+z ≤ k₁−1} ⊆ D. The case k₃ ≤ 2 gives exactly C ≤ 2√m + 2; k₃ = 3 needs c ≈ 2.25.
  For the cone class, K deletes part of P(k), and Wall/Floor must make up the loss (OPEN).

**Rejected tonight.**
- "Tripod graph B is a forest for tiles": false (m = 23).
- "LHS(D) − LHS(Cyl) small": it is 13 at m = 40/50, too lossy.
- Slab reduction C(D) ≤ C(D_c) + (lost corners): the lost corners are ≤ 2(q_a + q_b) + 2, not O(1).
- Slab decomposition of Tri: the interface term λ ≤ q_a + q_b is unbounded.

**Insight for the next attempt.** In the level picture along any axis c, a cone set is a 𝒞 set except at one
transition (v = q_c, where the quadrant Q is removed). So every LEVEL-WISE proof of a 𝒞 lemma (Lemma T, Lemma F) has an
O(1) defect in the cone class. Plan: re-prove TF/QF level-wise (Lemma P becomes "same-level tripods are nested").

## 2026-10-18 (night 17) — cone tiles: crude TF and qU bounds proved; the qO forest fails in the cone class

**Scanner.** The C port src/c/tile_scan.c (written by a parallel session, E132) matches every completed Python HT/MAXSUM
line: 188 lines over 119 values of m ≤ 130, 0 mismatches (my private copy; the only earlier differences were format
artifacts of the MAXSUM-only log tile_scan_M_7.log). So HT holds for every non-two-face e = 4 tile with m ≤ 130.

**Lemma TF-cone (PROVED on paper; cone class with the Floor Lemma, i.e. |Y_d| ≤ 2): 2Tri ≤ t + 17.**
Eliminate tripods by decreasing |x|; s(x) = # tops of x already used. Then 2T − t ≤ −1 + Σ s_cross + Σ (s_same − 1)⁺.
(i) Cross shares: by S′ a top y used in two directions a ≠ b has y + e_c ∈ K. y cannot lie in two of the Y_d (then y ∈ K),
so y is used in ≤ 2 directions and gives ≤ 1 cross share. Hence Σ s_cross ≤ |Y_1| + |Y_2| + |Y_3| ≤ 6.
(ii) Let x have same shares in a and b (partners u = x + ie_a, u' = x + i'e_b, tripods with the same tops). Then P′ on
(u', u) gives top_c(u') ∈ Y_a or top_c(u) ∈ Y_b. Define Φ(a,b) = {tripods x with same shares in BOTH a and b : some
b-partner u' has top_c(u') ∈ Y_a}. [Referee edit 2026-10-18: "in both a and b" added; (iv) and (v) use the a-partner.]
(iii) x ∈ Φ(a,b) ⇒ x_a = q_a − 1 and x_c < q_c. [y = top_c(u') has y + e_a ∈ K and y ∉ K, so y_a = q_a − 1 and y_b ≥ q_b;
u' + e_a ∈ D ∖ K forces u'_c < q_c.]
(iv) All members of Φ(a,b) have the same c-height. [If x̃_c > x_c, apply P′ to x̃ and the a-partner u of x in the (a,c)-plane.
top_b(x̃) + e_a ∉ K since x̃_c < q_c. top_b(u) + e_c ∈ K would force x_c = q_c − 1 and then x̃_c ≥ q_c.]
So Φ(a,b) lies on one b-line ℓ.
(v) |Φ(a,b)| ≤ 2.
- At most one member has x_b < q_b. For members x <_b x̃, P′ on (x̃, a-partner of x) gives x̃_b ≥ q_b or x_b ≥ q_b − 1, hence x_b = q_b − 1
  when x_b < q_b. [Referee edit 2026-10-18; first written "or x_b = q_b − 1".]
- Members with x_b ≥ q_b have top_c ∈ Y_a. The column over (q_a − 1, x_b) is at least as tall as the one under the partner's
  top, which reaches ≥ q_c. These tops are distinct from each other and from the c-top of the topmost member's b-partner.
  So there are ≤ |Y_a| − 1 ≤ 1 such members.
A tripod with s_same = 3 lies in Φ for all three pairs. Hence Σ(s_same − 1)⁺ ≤ Σ_{(a,b)} |Φ(a,b)| ≤ 12, and 2T − t ≤ −1 + 6 + 12.
Checked: claims (i)–(v) and the budget inequality on every cone tile with m = 30, 40, 50, 60, 64 (0 violations;
src/scratch/tf_cone_check.py). The observed maxima are cross ≤ 1 and same-excess ≤ 1.

**Lemma F-cone (PROVED on paper; any cone set): qU ≤ t + 2.**
In the level proof of Lemma F (direction 3), the relation U_{v+1} = U_v ∩ R_{v+1} holds for every v ≠ q₃. So every
level except q₃ adds ≤ 2 cross-level edges (e_L, e_R) and no cycle. At v = q₃ the removal of the quadrant adds at most
one more c = 1 edge: p = (p₁, q₂ − 1) with p₁ ≥ q₁, the row end of U_{q₃} at row q₂ − 1. Symmetrically it adds at most one
c = 2 edge. So ≤ 4 cross edges, ≤ 3 new cycles, rank(G_U) ≤ 3 and qU = t − comp + rank ≤ t + 2.
Checked on cone tiles m = 30..64 (src/scratch/qu_cone.py): rank(G_U) ≤ 1, qU − t ≤ 0, level counts never exceeded.

**qO in the cone class: the elimination proof FAILS, and so does the forest statement.** (src/scratch/qo_cone.py, qo_cycles.py)
- Cycle-closing qO cells (increasing |x|) are either cross shares (≤ 6, as above) or doubly-same cells whose QF
  contradiction is broken by a Q-drop. These come in **stacks**. Example in nonmax direction c: x_z = (W_a, W_b, z) for
  several z < q_c − 1, under a floor cell w = (W, q_c − 1) of height 1 next to a floor maximum. The partners are stacked on
  the c-lines (q_a − 1, W_b, ·) and (W_a, q_b − 1, ·), whose c-tops are Y-points.
- Each z needs both face profiles to take the value z + 1 beyond the quadrant: F(W_a + k_z) = z + 1 = G(W_b + l_z).
  The stack gives paths y_a – T_a(z) – T_b(z) – y_b, one per z, so rank(G_O) grows with |Z|.
- RCON (Wall + Floor) anneals: rank(G_O) up to 3, stack size up to 3 (m ≤ 200), elimination excess up to 4.
  Yet qO − t ≤ 1 throughout. Every extremal example fails PW (lattice_pairwise.py). The infeasible core of one is
  4 A₁-corner vectors plus q* (src/scratch/pw_core.py), which is not obviously related to the stack.
- Real tiles (m = 30..64): floor-line qO cells per line ≤ 2 (m = 60). "Doubly realized" levels (the necessary
  condition) reach 3, so the lattice does not exclude stacks outright (src/scratch/floorline.py).
- **New conjecture (OBSERVED): t + rank(G_O) ≤ C**, i.e. qO + comp(G_O) ≤ C. Evidence: max 0 on all 82,242 [corrected
  2026-10-18 from 82,254 by the referee's count of logs/tiles] non-two-face
  tiles of m = 30, 40, 50, 60, 64, and max 0 in every RCON anneal (t+rank−C target, m ≤ 300). By contrast t + exc − C
  reaches 2, so the crude elimination count does not satisfy it.
  It would give qO ≤ C − 1 and LHS ≤ 2t + (t + 17) + (t + 2) + (C − 1) ≤ 5C + 18 for cone tiles.
  Per-level Lemma T′ slack (src/scratch/tslack.py) does not line up level-by-level with the stack levels in the m = 198
  example. The injection must be global.
- Threshold arithmetic with Lemma B (C ≤ ⌊3/2 + √(6m − 15/4)⌋): 5C + β ≤ m + 1 holds for all m > 160 (β = 2), m > 191 (β = 18),
  m > 203 (β = 25). So the conjecture plus an HT scan of m ≤ 191 would settle cone tiles.

## 2026-10-18 (night 17, cont.) — PIVOT to all e: the final-window criterion generalizes

**Literature event.** github.com/kseth/wilf-e4 (Sept 2026) gives a complete computer-assisted proof of Wilf for e = 4.
It covers our open cone-class case, and the audit found no error. Our earlier "Corollary H" is Zhai 2011 Thm 1, and our
cylinder lemma (a) is HRW 2018 Prop 2.6(b) (LITERATURE §3 items 11–13). Decision (ledger review): stop the e = 4 cone
work and move to all e.

**FW criterion for every e (PROVED; generalizes kseth eq. (p:6) from d = 3).** Notation:
- S has multiplicity m and other minimal generators a_1..a_d (d = e − 1).
- T ⊂ ℕ^d is the term-order factorization ideal of Ap(S, m). It is a down-set, λ(x) = a·x is a bijection T → Ap,
  and M = max Ap = c + m − 1.
- u(x) = M − λ(x) ≥ 0. Lines are the maximal segments of T in a coordinate direction; P(T) = #lines = Σ_j |π_j T|.
- Z = {x ∈ T : λ(x) ≥ c}, the τ-set. Z ⊆ Max T, since λ(z) + a_j > M.

EXACT (any d): m·W = C(m,2) + Σ_ℓ σ_ℓ, where σ_ℓ = Σ_{x∈ℓ} (u(t_ℓ) − [u(x)]_m) and t_ℓ is the top of ℓ.
Equivalently m·W = Σ_x Σ_j u(top_j x) − (d−1)·C(m,2), which is Zhai's Lemma 3 / our CH′.
Proof sketch:
- Σ_j Σ_ℓ L_ℓ u(t_ℓ) = d·mM − (d+1)·a·s, where s = Σ_T x.
- In each direction the residues [u(x)]_m run over 0..m−1 exactly once.
- Our CH step (3) gives mW = d·mM − (d+1)Σλ − (d−1)C(m,2).
Bounds:
- A deep line (t ∉ Z) has σ ≥ m + C(L,2), because its axis-prefix residues [r a_j]_m (r ≥ 1) are distinct and nonzero.
- A final line has σ = m·C_ℓ − R_j(L), where R_j(L) = Σ_{r<L} [r a_j]_m and C_ℓ counts wraparounds.
- So **FW: m·W ≥ m·(P(T) − dτ) − (m−1)·E(Z)**, where E(Z) = Σ_Z |z|₁ − Σ_j max_Z z_j.
  If P(T) − dτ ≥ E(Z), Wilf follows. (Asserted along with EXACT on every S below; src/fw.py.)
- **FWx** (sharper; exact residues on final lines): m·W ≥ C(m,2) + Σ_deep (m + C(L,2)) − Σ_final R_j(L).
Data (EXPERIMENTS E134):
- FW alone proves Wilf for 258,561 of the 258,581 S with genus ≤ 22. All 20 failures have e ∈ {4, 5, 6}; none for e ≥ 7.
- FWx ≥ 0 on all 258,581, and on all but one of about 22k random hard S (c ≥ 4m or Eliahou-type).
  The one failure is ⟨13,20,21,23,25⟩ (W = 12, FWx = −15), which is covered by 3e ≥ m. Its τ = 8 of m = 13, so the final
  lines dominate, and the loss is the ignored wraparounds C_ℓ (13 per final line).
- Eliahou's ⟨14,22,23⟩₅₆ (W₀ < 0, W = 35) satisfies FW with bound 202 = 14.4m. (An earlier note said "bound exactly 0";
  that was a bug in fw_hard.py, whose minimum tracker started at 0. Corrected.) The family ⟨16,25,26⟩₆₄, ⟨18,28,29⟩₇₂, ⟨20,31,32⟩₈₀, ⟨22,34,35⟩₈₈ (c = 4m) has FW/m = 24.4, 34.3, 44.3, 54.3.
- Mechanism of FW failure: T simplex-like with Z the whole top layer gives P − dτ = 0 < E(Z) (interval-type semigroups).
- Random S almost never lie outside the known theorems (23 of 24k; FW holds on all 23). An adversarial search there is running.

## 2026-10-18 (night 17, late) — the shape of DS cells; the advisor lowers the target to qO ≤ 2t + O(1)
**Advisor's revision (relayed by the user).** Only the weakest bounds that close the argument are needed:
2Tri ≤ t + O(1), qO ≤ 2t + O(1), qU ≤ t + O(1), and a PROVED sublinear bound on t. These give δ ≥ m − 6t − O(1). After that,
compute the threshold and compare it with the exhaustive range before trying to improve constants.
Our status against that list:
- All four bounds are proved on paper: TF-cone, qO-cone (qO ≤ 2t − 1 + 2|Y| ≤ 2t + 11), F-cone, and t ≤ C (T′) with
  C ≤ 3/2 + √(6m − 15/4) (Lemma B, a proof, not the experimental 2√m corner estimate).
- Threshold: m ≥ 281.
- Exhaustive range: every tile with m ≤ 130 is done (the gaps m = 90, 100, 108, 114, 115 were closed today). Cone tiles with
  131 ≤ m ≤ 280 are being scanned.
- Decision: stop trying to improve the qO coefficient.

**Structure of DS cells (proved on paper, c = 3; not needed for the main line).** Let x = (X, Y, z) be doubly-same.
(a) ψ(p) = q₃, so p lies in the floor F₃.
- Each of the four defect cases (α), (β), (α′), (β′) gives F(X) ≥ q₃ or G(Y) ≥ q₃. The non-defective pair supplies the
  other inequality.
- Since γ(p) = 1, p = r − e₁ or r − e₂ for an outer corner r of F₃. By the Floor Lemma there are at most 4 such p.
(b) The 1-partner u = (X − i, Y, z) satisfies X − i < q₁ and ψ(X − i, Y) > q₃.
- If u's nonmax direction is 3: by (P1′), ψ(X − i, Y) ≠ q₃.
- If it is 2: u is a peak with ψ(p_u + e₁) ≥ q₃.
- The mirror statement holds for the 2-partner.
(c) If either partner has nonmax direction 3, z is determined by p: z = G(h(X) − 1) − 1, resp. z = F(a(Y) − 1) − 1.
- Suppose top₂(u) is maximal. It lies strictly above top₂(x), so column X is cut by h(X). Then maximality of top₂(x)
  gives G(h(X) − 1) = z + 1.
- If the partners have directions 2 and 1, the same argument forces i = i′ = 1, so p = (q₁, q₂), unless z is again
  determined.
- So, apart from p = (q₁, q₂), there are at most 4·2 = 8 DS cells per direction.
(d) At p = (q₁, q₂) the number of z is NOT bounded lattice-free.
- The family in examples/qO_lattice_free_family.md has #DS = Q − 1 and qO − t = Q − 5.
- It violates Wall + Floor, so it is not a tile.
- Real cone tiles (m = 30, 40, 50, 60, 64) have #DS ≤ 1. RCON anneals maximizing #DS (m ∈ [60, 200], seeds 11–12,
  4000 iterations) also reach only 1.
- |Max ∩ B_c| is not O(1) on tiles (up to 8 at m = 60), so the refinement qO ≤ t − 1 + 2|Y| + |Max ∩ B| does not give
  t + O(1) either.
Consequence: a proof of qO ≤ t + O(1) would have to bound the z-multiplicity at the quadrant corner using the lattice.
That is a sharpening, not a gap; it is parked under the advisor's revised plan.

## 2026-10-18 (midday) — e = 4 route complete; first look at the height criterion for e = 5
**Status.** Every link of our e = 4 route is in place (STATE "The e = 4 argument").
- The certified 16-bit scan on fejer covers m = 256–280: 0 HT failures and 0 area defects.
- Combined with the earlier scans, every non-two-face tile with m ≤ 280 satisfies HT, apart from the LP/BGOW-certified small cases.
- The proved thresholds are m ≥ 281 for cone tiles and m ≥ 131 for 𝒞 tiles (m ≥ 280 and 130 with the δ ≥ −1 sharpening).
- Lean has CHT, B, T, T′, TF, F, QF and the 𝒞 δ-bound. The cone forest bounds are in progress.
- The manuscript is being drafted (.research/E4_MANUSCRIPT.md).
- The re-certification of m = 120–255 is still running on fejer. [Later the same day: finished, E141; m = 236–255 had
  no log before it, so the "every tile with m ≤ 280" sentence above was premature until E141.]

**Height criterion in dimension d = e − 1 (OBSERVED; the inequality itself is PROVED).** CH′ and p_a ≥ m + 1 give
(m+1)·H(D) ≤ mW + (d−1)·C(m,2), where H(D) = Σ_x Σ_a ht(top_a x) over the d directions. So H > ((d−1)C(m,2) − m)/(m+1)
implies W ≥ 0.
- src/scratch/height_e.py asserts the inequality on every sample and reports H divided by the threshold.
- 400 random S each for e = 4 and e = 5, m ∈ [20, 60], generators < 6m, seed 1; 0 assertion failures.
- e = 5: the criterion fails once (m = 23: ⟨23, 40, 51, 62, 118⟩, ratio 0.95).
- e = 5: the minimum ratio over the sample is 1.4–3.1 for m ≥ 29 (e.g. 1.42 at m = 53). For e = 4 the same sampler gives (m = 44–59)
  ratios 2.8–5.7, but random samples are not adversarial; the e = 4 extremal tiles sit near ratio 1 for m ≈ 25.
- Question for the reassessment: does "4-D HT", H ≥ 1.5(m−1)·m/(m+1) for all non-degenerate 4-D tiles with large m,
  hold? If it does, the e = 4 mechanism has a d = 4 analogue: CHT counting plus a structure theorem for 4-D tiles. The
  missing ingredient is the 4-D cylinder/cone structure, which is much richer than in 3-D.

## 2026-10-18 (afternoon) — strategic review after e = 4; shape-only criteria fail in high d; window subadditivity for m | c
**Decision (lead, with the user's delegation of direction).**
- The e = 4 tile method needs a structure theorem for each e, so it cannot reach all e by itself.
- Main line: residue-weighted universal statements (TOP'', MaxCL, FWx).
- Second line: e = 5 tiles, deprioritized (see the shape-only result below).
- Background: Lean verification of e = 4.

**Shape-only criteria are not universal (OBSERVED, src/scratch/shape_d.py).** Sample: random S with 3e < m and c > 3m, e = 4..12, 150 s, seed 1.
- HT_d ((m+1)H > (d−1)C(m,2) − m ⇒ Wilf) fails in 30/11644 (e=4), 16/11042 (e=5), …, 1889/4233 (e=12).
- MAXSUM_d (Σ_Max(|y|+d) ≤ (d+1)m/2 + (d−1)/2) fails even more often.
- So a proof for all e must use the generator arithmetic.
- For fixed e = 5 the HT failures sit at small m: 47,625 random S, failures only for m ≤ 28; the min ratio rises from 1.09 (m ≈ 30) to 2.7 (m = 120); src/scratch/ht_e_bands.py.
- But a crude O(t)-counting proof in 4-D would need m ≳ 10⁴ before the threshold, far beyond 4-D tile enumeration. So the e = 5 tile route needs near-sharp constants.
- Literature check, 2026-10-18 (arXiv via alphaXiv newest first; GitHub via web search): no proof of Wilf for e = 5 found. Related: github.com/michelfgaspar-spec/Wilfs13 (Lean proof for |L| = 13).

**Slack in the open range (OBSERVED, src/scratch/open_slack.py).** Random S, 3e < m, c > 3m: min e·ℓ/c is 1.24 (e=3) … 3.63 (e=14), and the τ-criterion applies to ≥ 89%. Random samples are not adversarial.

**FWx decomposition (OBSERVED, src/scratch/fwx_decomp.py).** Genus ≤ 18 with c > 3m: F > C(m,2) in 159/5815 S, so the deep-line term is needed. FWx = 0 exactly for e = 2.

**Window subadditivity (PROVED; asserted on 38,859 splits, genus ≤ 16, src/scratch/winsub.py).**
- Setting: ρ(x) = ((λ(x) − c) mod m) + 1 ∈ [1, m] (window position, a bijection T → [1, m]), γ = c mod m. For u ∈ X and a split n(u) = x + y (x, y ∈ T ∖ {0}):
    ρ(x) + ρ(y) − 1 = ρ(u) − γ + mκ, κ ∈ {0, 1, 2}.
- **If m | c then κ ∈ {0, 1}, so ρ(u) ≤ ρ(x) + ρ(y) − 1.** Proof: ρ(u) − 1 = λ(u) − c exactly, λ(u) = λ(x) + λ(y), and the range forces κ ∈ {0, 1}. Also ρ(0) = 1, and every split cell is outside X.
- TOP'' in window form (PROVED equivalent): m + Σ_{u∈X} ρ(u)(ℓ(u) − 1) ≤ (d+1)·Σ_{x∈T∖X} ρ(x).

**Top-layer load condition TL (residue-free) and TL ⇒ TOP'' when m | c (PROVED).**
- TL: each u ∈ X with ℓ(u) ≥ 2 spreads ℓ(u) − 1 units over splits {x, n(u) − x}, and every nonzero cell receives load ≤ d + 1.
- Proof that TL ⇒ TOP'' (m | c): subadditivity gives Σ_X ρ(ℓ−1) ≤ Σ L(x)ρ(x) − H with H = Σ(ℓ−1). The remaining term m is covered because Σ_{u∈X}(ℓ(u) + d) ≤ dm (incidences ending in X).
- So TL ⇒ Wilf for every S with m | c, any e. This case is open in the literature; LITERATURE #22 needs 4e ≥ m as well.
- Evidence (src/scratch/topload.py, HiGHS LP):
  - all 33,242 S of genus ≤ 18 (6,417 with m | c): 0 failures; tight (L* = d+1) at ⟨5,6,8⟩;
  - 52,060 random S with m | c, c ≥ 4m, e = 3..9, m ≤ 60: 1 failure.
- **TL is FALSE.** Counterexamples:
  - ⟨24,25,29,30⟩ (m | c, c = 4m, L* = 4.364 > 4);
  - ⟨36,37,42,43⟩ (m | c, c = 5m, L* = 5.5 > 4; TOP'' slack 300 there);
  - ⟨25,44,45,49⟩ (L* = 4.909).
- All three are e = 4 two-face tiles: two 2-D staircases glued along an axis, whose cells are loaded by both planes. This is the same family that broke the old Load Lemma and every residue-free MaxCL method.

**Next (main line).** A position-aware TL. Splits with κ = 1 gain m, so the axis overload of glued staircases must be paid by wrap splits. Test whether the LP with the gain m·κ_s always certifies TOP'' when m | c. If it does, the remaining task is a provable rule for where wraps occur.

## 2026-10-18 (evening) — TL refuted at e = 5; ATOP (permutation hull + full subadditivity); simplex obstruction
**TL is FALSE at e = 5 (CERTIFIED).** S = ⟨37,38,41,45,46⟩: m = 37, c = 148 = 4m, W = 72. Then L* = 21/4 > d+1 = 5, by an
exact rational dual certificate (src/scratch/tl_cert.py).
- The overload sits in the plane of the consecutive generators 45 and 46 (residues 8 and 9): X contains the
  anti-diagonal (0,0,i,4−i), and π grows linearly along the plane (π = 8(i+j) + j + 1).
- TOP'' slack there is 718, so the inequality holds easily; only the residue-free certificate fails.
- The conjecture "TL holds for e ≥ 5" is dead.

**ATOP (new relaxation, residue-free).** Maximize Σ_X (r(u)+1)(|u|+d) over r in the convex hull of permutations of
{0, …, m−1}, with r(0) = 0 and r(x+y) ≤ r(x) + r(y) for all x, y, x+y ∈ T. ATOP holds if the maximum is at most
m((d+1)m + d − 1)/2. When m | c the true residues are feasible, so ATOP ⇒ TOP'' ⇒ Wilf. ATOP keeps both injectivity
(dropped by TL and the Load Lemma) and all geometric subadditivity (dropped by CR).
- Semigroups (src/scratch/atop.py):
  - holds on the e = 5 TL failure (slack 0.13) and on ⟨24,25,29,30⟩ and ⟨21,22,25,26⟩;
  - FAILS on ⟨25,26,30,31⟩ (−0.020) and ⟨36,37,42,43⟩ (−0.038), both e = 4 two-face;
  - adding any fifth generator to ⟨36,37,42,43⟩ (m | c cases) gives slack ≥ 0.37.
- Abstract shapes, with X = all maximal cells (src/scratch/atop_shape.py, atop_book2.py, atop_perturb.py):
  - two-page books {|x| ≤ n, x_a x_b = 0} FAIL in d = 3 (n ≥ 4), d = 4 (n ≥ 3) and d = 5 (n = 3);
  - books with three or more pages, and books plus spikes, hold;
  - the full simplex {|x| ≤ 5} in d = 3 FAILS (−0.22).
  - So the obstruction is simplex-likeness, not two-faceness; two-face lattice tiles are the realizable form of it.
- **Every non-two-face 3-D lattice tile at m = 30 (2,639 tiles, logs/tiles) satisfies ATOP**, min slack 0.122. On a
  quarter of m = 40 (1,532 tiles) the min slack is 0.174 (src/scratch/atop_tiles.py). Slack grows with m.
- Candidate structural conjecture **ATOP-NTF**: every lattice tile T ⊂ ℕ^d (down-set fundamental domain) with
  e_a + e_b ∈ T for all a ≠ b satisfies ATOP. Combined with a two-face theorem in general d, this would give Wilf for
  all m | c. Any proof must use the lattice-tile property (the simplex is non-two-face and fails).
- Next: the d ≥ 4 evidence (fejer runs, e = 5–7), then the structure of the ATOP dual on non-two-face tiles.
- **Exhaustive 3-D (src/scratch/atop_alltiles.py).** Every non-two-face 3-D lattice tile with m ≤ 30 satisfies ATOP; the
  worst slack is 0.047 (m = 23). Two-face tiles are tighter: the worst slack is 0.0076 at m = 16, and the first failure is
  at m = 21, r = (1,4,5) (atop_alltiles_tf.py). So in d = 3, ATOP fails only on two-face tiles.
- **The book family ⟨n², n²+1, n²+n, n²+n+1⟩** (m = n², c = n²(n−1), W = 2·C(n,3), so Wilf has slack ≈ c/3):
  - ATOP fails for n ≥ 4.
  - Adding the relation of the quadratic corner (ATOP+R2: group subadditivity generated by e_1 + e_2 ≡ e_3,
    atop_r2.py) repairs n = 4, 5, 6 (n = 6 by only +0.0003) but fails for n = 7 and 8, with any range of multiples.
  - The quasi-additivity lower bound r(x+y) ≥ r(x) + r(y) − m changes nothing.
  - Unit twists ⟨u·φ⟩ are all harmless (u = 1 is the worst, TOP ratio 0.87), so the LP maximizer is a fractional
    artifact.
  - But integral permutations without relations also violate ATOP (MILP: n = 5 slack −0.010, n = 7 slack −0.017).
  - Conclusion: on books, the linear structure λ = ⟨z, p⟩ is needed, not just one relation.
- **Cylinder lemma in every dimension (PROVED; PROOFS).** Every lattice tile is Cyl(D) minus at most one orthant
  q* + ℕ^d, with q* ∈ Λ. The 3-D proof never used d = 3. Hence the 𝒞/cone dichotomy, the first structural link of the
  e = 4 route, holds for every e. Cone tiles get rare as d grows (61 / 4 / 0 of 400 random tiles at e = 4 / 5 / 6).
- **The cylinder conditions do not replace lattice structure.** An anneal over non-two-face down-sets satisfying all
  necessary conditions (b′) (atop_cyl.py) finds ATOP failures:
  - d = 3, m = 17: simplex_3 minus {(1,1,1), (1,2,0), (2,1,0)}, a cone-class shape. It is not a tile: q* = (1,1,1) ∈ Λ
    and the two support-{1,2} corners give e_1 ≡ (1+t′)e_3 and e_2 ≡ (1+t)e_3 with t, t′ ≤ 3, so ord(e_3) ≤ 9 < 17.
  - Restricted to cylindrical sets (D = Cyl(D)), no failure in d = 3 (best ratio 0.90). In d = 4 there is a failure at
    m = 28, with e_1+e_2+e_4 and e_2+e_3+e_4 missing and only 2 cells of support 3. It is a union of 2-D pages: the
    d = 4 analogue of a book.
- **Picture.** Residue-light certificates fail exactly on tiles concentrated on low-dimensional coordinate skeleta
  (books); two-face is the d = 3 case. Everything else in reach passes with margin.
- **General c: ATOP_γ.** With γ = c mod m and r = (λ − c) mod m, r(x+y) ≤ r(x) + r(y) + γ and r(0) = (−c) mod m. Lemma A
  gives TOP'' ⇒ Wilf for every c, so ATOP_γ ⇒ Wilf for every c (src/scratch/atop_g.py).
  - Random, c > 3m, 3e < m: 0 failures at e = 3 (9,870 S, worst 0.81), e = 4 (11,626, worst 0.989), e = 5–7 (13,032,
    worst 0.891). Books are rare in random samples.
  - Exhaustive e = 5, generators < 2m, m | c, m = 17–30: 9,693 S, 0 failures, worst 0.928 (atop_exh5.py, fejer).
- **CR (crude rearrangement, shape only, any c) splits exactly along two-face.** CR: Σ_i T_(i)(m−1−i) ≤ (d+1)m(m−1)/2,
  with T(y) = d + |y| over the maximal cells. CR ⇒ MaxCL for every σ ⇒ Wilf (Lean chain).
  - 152,855 random S with e = 4–9, c > 3m, 3e < m (src/scratch/cr_test.py): 111 failures, **all two-face**. Worst
    non-two-face ratios: 0.976 (e = 4), 0.963 (e = 5), 0.94 (e = 6, 7). For e = 8, 9 every sampled tile was two-face.
  - Every non-two-face 3-D lattice tile with m ≤ 26 (exhaustive), and all 82,242 stored tiles at m = 30–64, satisfy
    CR (cr_tiles.py). The worst ratio is 0.982 (m = 8), falling to 0.85 at m = 64. Two-face tiles fail at most m.
  - It needs lattice input: a cylindrical non-two-face non-tile at m = 17 fails CR (1.0037; seven maximal cells of
    length 3). The anneal found no other failing m in d = 3 (best 0.964 for m ≤ 16, 0.80 for m ≥ 25; cr_anneal.py).
  - In d = 4, cylindrical non-two-face sets fail CR (1.11 at m = 25). Adding ⊇ {0,1}^4 gives best 0.993 (no failure).
- **Conjecture CR-NTF:** every non-two-face lattice tile satisfies CR. Two-face tiles need residues: our e = 4 theorem;
  ATOP_γ (no failure found for e ≥ 5).
  - If both hold, Wilf follows for all e: CR-NTF for non-two-face tiles, ATOP_γ for two-face tiles with e ≥ 5.
  - CR-NTF is a statement about the lengths of the maximal cells of lattice tiles. It is equivalent to a lower bound on
    Dep = dm − Σ_A(d + |y|), the incidences in columns with non-maximal top (roughly Dep ≳ (d−1)m/2 when t ≪ m).
- **ATOP_γ FAILS at e = 5 for m ∤ c (fejer exhaustive, generators < 2m, c > 3m, m = 16–34; atop_exh5g.py).**
  - 6 failures in about 350k S:
    - m = 25: ⟨25,31,32,33,39⟩, ⟨25,34,37,38,41⟩, ⟨25,34,43,46,47⟩, ⟨25,42,43,46,49⟩ (each 1.0237), ⟨25,36,42,43,44⟩
      (1.0019);
    - m = 26: ⟨26,29,31,34,43⟩ (1.011).
  - All are two-face, all fail CR (1.023–1.036), and all have t = 12 maximal cells of length 3. True TOP ratios are
    0.61–0.76 and W = 36–52.
  - For m | c, ATOP still has no failure.
  - So the two-face side needs more than residue-light certificates when m ∤ c, as in our e = 4 two-face theorem
    (τ-criterion).
- **Cube version of ATOP is FALSE (abstract):** the d = 4 anneal (cylindrical, ⊇ {0,1}^4) found ratio 1.0074 at m = 36
  (fejer, seed 11). Seeds 12–14 (d = 4, 5) stayed ≤ 0.92.
- **Mechanism in d = 3 (OBSERVED):** S1 := Σ_A(3 + |y|) ≤ 2m, i.e. Dep ≥ m, implies CR without sorting.
  - It holds on all 82,242 stored non-two-face tiles (m = 30–64; max S1 − 2m = 0) and fails only at small m (≤ 23,
    excess ≤ 6), where CR's rank discount takes over (maxsum.py, colcount.py).
  - On cylindrical non-two-face sets (tile or not), the anneal max of S1/(2m) is 0.861 for m ∈ [25, 90] and 0.721 for
    m ∈ [40, 150] (s1_anneal.py). So for class 𝒞 the large-m statement looks purely combinatorial.
  - Per cell: S1 = Σ_{x∉A} c(x) + 3t with c(x) = #{a : the a-column top of x is maximal}. Cells with c(x) = 3 are rare
    (≤ 5 per tile).
  - Column form: the a-column over p has a maximal top iff p is a strict corner of the a-height function h_a. So
    F_a·m = Σ_{strict corners} h_a, and the target is F_1 + F_2 + F_3 ≤ 2.
  - Books: F_spine = 1 and F_page ≈ 1/2, so the sum ≈ 2 + 3/n > 2.
  - MAXSUM_d fails on some non-two-face tiles in d ≥ 4 (excess up to 0.76m at e = 7). There CR's sorting is essential.

## 2026-10-18 (night) — S1-C refuted; HCR, HCR+ and HCR++: shape-only criteria that combine heights with distinct residues
**S1 ≤ 2m for class 𝒞 is FALSE** (codex subagent, Sol 6.1 xhigh; verified by the lead). Counterexample:
h = (4,2,1,1,1), F = (8,4,3,2,1), G = (8,2,2,1). It is cylindrical, non-two-face, m = 25, S1 = 56 > 50, and passes all
cylinder count conditions. CR still holds on it (0.972).
- Exhaustive class-𝒞 sets, m ≤ 25: 53,345 sorted-axis triples, max excess 6 at m = 25, attained by 21 orbits
  (src/scratch/s1c/, .research/drafts/S1C_PROOF.md). No threshold M0 in range.
- Kill: the unsorted S1 bound. CR's rank discount is needed even in 3-D.

**HCR (PROVED implication; shape-only).** Use CH′ exactly: mW + (d−1)m(m−1)/2 = B := Σ_{(x,a)} (Λ − λ(top_a x)). This was
asserted on every test.
- Bound the deficits:
  - for a non-maximal top t, Λ − λ(t) ≥ (m+1)·ht(t), where ht is the longest upward path in D;
  - the maximal tops have distinct values in [0, m−1].
- Hence HCR(D) := [(m+1)·Σ_{(x,a): top non-maximal} ht(top_a x) + Σ_i T_(i)·i] / ((d−1)m(m−1)/2) ≥ 1 ⇒ W ≥ 0, for every
  S with tile D.
- HCR dominates HT (which drops the residue term) and the CR/Tile-TOP'' route (which uses m in place of (m+1)·ht).
- It is tight at both classical equality families (e = 2 and T_{m,q}).
- Evidence:
  - **every 3-D lattice tile with 10 ≤ m ≤ 25 satisfies HCR, two-face included** (exhaustive; src/scratch/hcr_shape.py).
    The only failures for m ≤ 25 are 2 two-face tiles at m = 9 (r = (1,3,4), 0.972), covered by BGOW. The worst value
    for m ≥ 10 is 1.058 (m = 13), and it is ≥ 1.29 at m = 25;
  - books ⟨n², …⟩ pass (1.29, 1.52, 1.79 for n = 5, 6, 7), as do all ATOP_γ failures;
  - random e = 4–9 (≈ 280k S): failures only at e ≥ 6, all two-face (1 at e = 6, 8 at e = 8, 2 at e = 9).
    Non-two-face tiles pass with margin ≥ 1.16 at every e.
- **HCR+** (assignment; src/scratch/hcrp.py): all top deficits are distinct mod m and v(t) ≥ (m+1)ht(t). Minimize
  Σ_t w(t)·v over assignments of residue classes to cells (an m × m assignment problem).
  - It fixes every HCR failure at e = 8, 9 (1.14–1.22).
  - 138,790 random S with e = 5–9: 0 HCR+ failures.
  - The only HCR+ failure seen is ⟨19,26,28,36,41,42⟩ (e = 6, m = 19, two-face, 0.994).
- **HCR++** (MILP; src/scratch/hcrpp.py) adds the path constraints v(t) ≥ v(t+e_a) + m + 1, with distinct residues and
  integer v. On ⟨19,26,28,36,41,42⟩ it gives 1.294, solved to optimality.
- **Consequence.** "Shape-only criteria fail in high d" was true only of HT_d and MAXSUM_d. Adding the distinctness of
  the residues of column-top deficits, with no residue arithmetic, certifies Wilf on every semigroup tested.
  - The universal target becomes: **HCR+ (or HCR++) for every lattice tile with m ≥ 19** (m ≤ 18 is BGOW).
  - For e = 4: **HCR for every 3-D tile with m ≥ 10**. That would be a uniform e = 4 proof with no two-face split,
    once proved for large m by counting and checked for the finite range.
- **HCR_exit is too weak (fejer; logs/atop/hcrexit*.log).** HCR_exit replaces column tops by exits:
  H_n ≥ Σ_x (d − outdeg x)·ht(x).
  - 3-D tiles: it fails at m = 8, 9, 12 and at most m in 20–26 (worst 0.824 at m = 24).
  - Random (m ≥ 20, about 246k S): 409 failures at e = 4, 236 at e = 5, 75 at e = 6, 23 at e = 7. HCR passes all of
    these (e.g. 0.824 vs HCR 1.82).
  - So HCR's strength comes from the heights of non-maximal column tops away from the exits, not just from the exits.
  - Kill as a proof target.
- **4-D lattice-tile enumeration (codex subagent; src/scratch/tile4/, running on fejer).**
  - Exact volume certificate per lattice; all 2,000 random e = 5 semigroup tiles were found; 3-D counts reproduced.
  - Status at 20:54 UTC: complete through m = 32, 3.22M tiles. Only 2 HCR failures, both at m = 13 (r = (1,2,6,9),
    (1,5,8,12); HCR = 112/117; covered by m ≤ 19).
  - Min HCR rises: 1.055 (m = 14) to 1.234 (m = 32). Not yet verified by the lead.
- **Where HCR is tight in 3-D (fejer, src/scratch/hcr_tight.py).** For 10 ≤ m ≤ 22, the only tiles with HCR < 1.15 are
  two-face books: r = (1,3,4) at m = 13 (1.058), and the n = 4 book at m = 16 (1.092; r = (1,4,5), (1,5,12)). Every
  non-two-face tile there is ≥ 1.15.
- **Books, exactly (PROVED by direct count).** Book_n: two triangular pages {i + j ≤ n−1} on a common axis, m = n²,
  t = 2n − 1 maximal cells, all of length n − 1.
  - Cross-page lemma (any two-face tile with e_a + e_b ∉ D): every x with x_b ≥ 1 has x + e_a ∉ D, so it is its own
    a-column top. Hence H_n ≥ Σ_{x_b ≥ 1} ht(x) + Σ_{x_a ≥ 1} ht(x).
  - In books these are the only nonzero terms: H_n = 2Σ_{s=1}^{n−1} s(n−1−s) = n(n−1)(n−2)/3, and
    R = (n+2)(2n−1)(n−1).
  - HCR(book_n) = [(n²+1)n(n−1)(n−2)/3 + (n+2)(2n−1)(n−1)] / (n²(n²−1)): 0.972, 1.092, 1.287 for n = 3, 4, 5
    (matches computation); ≥ 1 iff n ≥ 4; ~ n/3.
  - So two-face tiles are carried by the heights of the other page's cells. A general two-face HCR proof needs
    Σ_page ht large unless the page is thin, in which case t is large and R takes over.

## 2026-10-18 (late night) — where HCR is tight in 4-D; the near-star formula; shape-only limits
- **4-D low-HCR tiles are thin (fejer, src/scratch/tile4/hcr4_low.py, e = 5 domain: distinct nonzero residues, all
  e_a ∈ D).** For 12 ≤ m ≤ 34 every tile with HCR < 1.2 has all maximal cells at level |y| ∈ {2, 3} (max level ≤ 4),
  t ≈ m/2 maximal cells, φ = S_T/(dm) ≈ 0.75–0.92, and is two-face in all but three cases (m = 22, 26, 27).
  Per-m minimum: 1.030 (m = 12), 0.957 (13), 1.055, 1.095, 1.136, >1.2 (17), 1.113, 1.142, 1.153, >1.2 (21), 1.160, 1.194,
  1.117, 1.091 (25), 1.166, 1.190, >1.2 (28); whole-table minima 1.108 (m = 30), 1.196, 1.234, 1.295 (m = 33).
- **φ does not decay.** The share of (cell, direction) pairs whose column top is maximal reaches 0.73–0.80 at every
  m ≤ 29 (phi4.py). So the crude bound H ≥ dm − S_T (CR) cannot prove HCR. Heights ≥ 2 and R are both needed.
- **Near-star formula (PROVED by direct count).** Let D = {0, e_1..e_d} ∪ Q with Q a set of q level-2 non-square cells,
  every e_b below some cell of Q, and m = d + 1 + q. Then:
  - H = d(d+1) − 2q;
  - the maximal cells are exactly Q, each with T = d + 2;
  - HCR = [(m+1)(d(d+1) − 2q) + (d+2)q(q−1)/2] / [(d−1)m(m−1)/2].

  Checks:
  - d = 4, q = 8 gives 112/117, exactly the two m = 13 failures. Those are Δ_2 minus 2 cells, i.e. near-stars.
  - q = αd: HCR → 1 + 1/(1+α)².
  - q = βd² (0 < β < 1/2): HCR = 1 − 1/d + O(1/(βd²)). So for large e, shape-only HCR (and HCR+, whose residue
    bound is the same here) fails on near-stars with m ~ βe², far outside Eliahou's m ≤ 3e.
  - Random near-stars (hcr_star.py) at m = 150, 250 with d = 37, 47 give HCR 1.022 and 1.010. The predicted crossing
    below 1 needs βd ≫ 1, around d ≈ 100.
- **Shift lemma (PROVED).** Replace n by n + km·(1,…,1).
  - Condition: (i) the tile is unchanged (true for level-≤ 2 tiles, since distinct residues forbid a lower-level
    representative), and (ii) the λ-argmax cell lies at maximal level N.
  - Conclusion: mW increases by km[dmN − (d+1)Σ_D|x|] ≥ 0.
  - Proof of the sign: ℕ^d truncated at level N is a product of chains, hence LYM (normalized matching). So the level
    densities f_j / C(j+d−1, d−1) of a down-set are non-increasing, and Chebyshev gives mean|x| ≤ dN/(d+1).
  - Consequence: on near-star shapes Wilf reduces to the unshifted generators in (m, 2m), where c ≤ Λ − m + 1 ≤ 3m,
    which is Eliahou's range. The near-star HCR failures are therefore not threats to Wilf. They show that any
    universal proof must use the actual Apéry values (residue structure), not only the shape.
- **Cone-LP relaxation is weak (lp4.py).** Minimize Φ(n) = dmΛ − (d+1)Σλ over the closed Gröbner cone with n ≥ m+1.
  On the thin tiles it gives 0.24–1.46 of the target. Its optimum sits at ties n = (m+1)·(1,1,1,1), where all
  top-level deficits vanish. So HCR's R term (distinct deficits) is essential: the integrality of n is what HCR uses
  beyond the cone.
- **Reformulation used above (exact; it is CH′).** mW + (d−1)m(m−1)/2 = Φ(n) = dmΛ − (d+1)Σ_{x∈D} λ(x). So Wilf says
  that the mean Apéry element is at most (d/(d+1))Λ − (d−1)(m−1)/(2(d+1)). For star-shaped continuous sets,
  dΛ|F| − (d+1)∫λ = ∫_θ R(θ)^d (Λ − R(θ)) dθ ≥ 0, with equality only for the simplex. Wilf is thus a quantitative
  "lattice tiles are far from λ-simplices" statement.
- **Exact Wilf number in the thin regime (PROVED; checked on ⟨5,6,7⟩, W = 2).**
  - Setup: generators n_a = m + r_a, so k_a = 1. Write the Kunz coordinate of tile cell x as K(x) = |x| + κ(x), with
    carry κ(x) = ⌊x·r/m⌋.
  - Then W = Lev + Car, where:
    - Lev = dmN − (d+1)Σ_D|x|, with N = |x*| the level of the λ-argmax. Lev ≥ 0 by LYM when x* is at maximal level.
    - Car = d(ρ* − m + 1) − (d+1)Σ_D κ(x), with ρ* = x*·r.
  - Corollary: if Ap consists of sums of ≤ 2 generators and every r_a < m/2, then all carries vanish and ρ* = m − 1, so
    **W(S) = e(e+1) − 2m**. Wilf holds since m ≤ |Δ_2| = C(e+1, 2).
  - In general (n = r + mk), Lev uses the weights k (weighted DSI), and the carries obey Σκ = (s·r)/m − (m−1)/2,
    because the residues form a complete system.
- **Thin tiles and additive bases.**
  - A level-2 near-star tile with residues R′ = {0, r_1..r_d} needs R′ + R′ = ℤ/m. Its excess j = C(e+1,2) − m counts the
    sum collisions, and Lev = 2j.
  - Under the uniform shift n → n + km·1, mW grows by km·Lev. The normalized slack σ = Φ/(mΛ) tends to j/m.
  - So σ is bounded below on thin tiles exactly when near-perfect additive 2-bases of ℤ/m are impossible
    (|R′|² ≥ (2 + ε)m). Level-N thin tiles correspond likewise to N-fold bases.
  - Hence the hard core of Wilf in the thin regime is additive-combinatorial (sumset excess vs. carry arrangement).
    In the fat regime it is geometric: by Minkowski, (D − D) ∩ L = {0} and D ⊇ Δ_n(T) force
    vol K_T ≤ 2^d m, i.e. a tile is ≥ C(2d,d)/2^d times larger than any λ-simplex it contains (d = 4: 4.4×).
    The same bound applies to every k-dimensional coordinate simplex inside D (k = 3: 2.5×, k = 2: 1.5×).
  - Continuous consequence: a down-set with vol ≥ (1−η)vol Δ contains (1 − η^{1/d})Δ. So rescaled tiles have
    η ≥ (1 − ρ_d)^d with ρ_d = (2^d/C(2d,d))^{1/d}, i.e. a positive but small DSI slack (d = 4: η ≥ 0.009) in the fat
    regime only.
- **Correction (simpler proof).** The LYM / normalized-matching step in the shift lemma is unnecessary.
  - For every finite down-set D and positive weights w, d|D|·max_D(x·w) − (d+1)Σ_D x·w = Σ_{(x,a)} (max − w·top_a x) ≥ 0.
    This is CH, valid for any down-set.
  - So Lev = dmN − (d+1)Σ|x| is the unit-weight column-top sum B(D, 1) ≥ 0, and the "discrete star inequality" is
    trivial.
  - All of Wilf's content is the lattice lower bound B ≥ (d−1)m(m−1)/2.
- **Test: generator-drop induction fails (tf_drop.py, fejer, 300 two-face e = 5 S, c > 3m).** Let S_a, S_b be S with
  n_b, resp. n_a, removed. Then W(S) ≥ min(W(S_a), W(S_b)) fails in 50/300 cases (worst ratio 0.52 at
  ⟨26,50,67,71,73⟩). There is no naive two-face reduction to e = 4.
- **Random level-≤2 semigroups (lev2.py)** have large W (≥ 33 at m = 20–30). Level 2 with c > 3m essentially requires
  near-uniform k, which is the shift-lemma regime.
- **Level/carry split of the Wilf number (exact, every e; checked on 1,600+ random S with e = 3–9, src/scratch/split.py).**
  - Setup: write n_a = r_a + m k_a with 1 ≤ r_a ≤ m − 1, so λ(x) = m(x·k) + x·r on the grlex tile, and let x* be the
    λ-argmax. Then W = Lev + Car, where:
    - Lev = dm(x*·k) − (d+1)Σ_D x·k is the geometric part. Lev ≥ 0 by CH whenever x* also maximizes x·k.
    - Car = d(x*·r) − (d+1)·mean_D(x·r) − (d−1)(m−1)/2 is the arithmetic part. Equivalently,
      Car = dm(κ* − (d+1)κ̄/d) + d(res* − m + 1), with carries κ(x) = ⌊x·r/m⌋.
  - This is the Kunz coordinate split K(x) = x·k + κ(x), so it is a reorganization. The content is the data:
    - Lev < 0 in 3 of about 1,600 cases.
    - Car < 0 in 25–40%.
    - Whenever Car < 0 in the random sample, Lev ≥ 1.65|Car|. This is not adversarial; near-tight S will push the
      ratio toward 1.
  - Reading:
    - Shape-only proofs fail because Car is needed (near-stars).
    - Residue-only proofs fail because Car < 0 often.
    - A general proof must be an exchange inequality: when the residues produce a carry deficit, the λ-argmax is
      chosen by the k-part against the residue order, and that misalignment must force a matching level surplus.
  - Adversarial search for min W/Lev with Car < 0: src/scratch/split_climb.py, e = 4, 5, 6, 8 on fejer
    (logs/split_climb_e.log).

## 2026-10-18 (late night, continued) — Down-set Wilf (GW): the inequality holds on every residue-complete down-set

- **RW is Wilf itself, not a reduction.**
  - Selmer's formulas hold for the Apéry set Ap(T, t) of ANY nonzero t ∈ T, not only the multiplicity:
    F(T) = max Ap − t and g(T) = ΣAp/t − (t−1)/2.
  - Hence, for every d ≥ e(T) − 1:
    (d+1)ℓ(T) ≥ c(T) ⟺ dt·max Ap(T,t) − (d+1)ΣAp(T,t) ≥ (d−1)t(t−1)/2.
  - Let T = ⟨s_1, …, s_d, m⟩ with m the LARGEST generator, and let D be a factorization tile of Ap(T, m) under the
    weight s. Then RW(D, s) is exactly Wilf for T.
  - So RW on tiles that are Gröbner for s is Wilf, written through the Apéry set of the largest generator. RW on
    other residue-bijective down-sets is a strengthening.
- **The general statement (GW).** Take a down-set D ⊂ ℕ^d with |D| = m and an integer vector n such that x ↦ x·n mod m
  is a bijection D → ℤ/m. Put v = x·n and M = max_D v. Then
  d·m·M − (d+1)·Σ_D v ≥ (d−1)m(m−1)/2,
  equivalently (d+1)·Σ_D ⌊v/m⌋ ≤ d·(M − m + 1).
  - On the Apéry tile of S (multiplicity m, n the other generators, d = e − 1) this is Wilf(S).
  - No minimality is assumed.
- **Exhaustive evidence, every down-set (not only tiles).** All down-sets using all d directions, all residue
  representatives s ∈ [1, m−1]^d, all lifts n = s + mk:
  - d = 2: m ≤ 26 with k ∈ {0..3}²;
  - d = 3: m ≤ 14 with k ∈ {0,1,2}³;
  - d = 4: m ≤ 10 with k ∈ {0,1,2}⁴.
  - 0 failures. Equality occurs ONLY on minimal domains (v(D) = Ap(⟨m,n⟩, m)).
  - On non-minimal domains, min E = 2–12, where E = d(M−m+1) − (d+1)Σκ.
- **Signed weights.** GW also holds with entries of n of any sign: k ∈ [−2,2]² for d = 2, m ≤ 12, and k ∈ [−1,1]³ for
  d = 3, m ≤ 9. So the statement is about (D, Λ) and the dual lattice Λ^∨ = ℤs + mℤ^d, not about positive weights.
- **Residue completeness is essential.** Requiring only distinct values (an injective v) is FALSE. Smallest
  counterexample: d = 2, D = {(0,0),(0,1),(0,2),(1,0)}, n = (3,2).
  - Values {0,2,4,3}, M = 4, Σ = 9, so B = 32 − 27 = 5 < 6 = τ.
  - Residues mod 4 are {0,2,0,3}, not complete.
  - Up to m = 12 (d = 2) and m = 9 (d = 3) the failures reach B − τ = −27 and −12.
- **GW is strictly stronger than Wilf, even for the same weights.**
  - In d = 2 (m ≤ 16) the Apéry tile always minimizes E over all residue-bijective down-sets for its n.
  - In d = 3 non-minimal domains beat it, also when every n_a is a minimal generator. For n = (19,17,12), m = 10:
    - D = {0, e3, e2, 2e2, 3e2, e1, e1+e2, e1+2e2, 2e1, 2e1+e2};
    - values 0,12,17,34,51,19,36,53,38,55, residues complete;
    - E = 165 − 108 − 27 = 30, against E(Apéry) = 46.
  - So GW is not "Wilf plus flip monotonicity".
- **Reformulations (exact).**
  - Put A = v(D) and Δ = A + mℕ. Then:
    - g(Δ) = Σ_D κ with κ = ⌊v/m⌋;
    - ℓ(Δ) = Σ_D λ with λ = ⌊(M − v)/m⌋;
    - c(Δ) = M − m + 1 = g + ℓ.
  - GW ⟺ (d+1)ℓ(Δ) ≥ c(Δ) ⟺ d·ℓ(Δ) ≥ g(Δ): "Wilf for Δ with e replaced by d+1".
  - Δ need not be a semigroup. It is the image of a down-set plus mℕ, so it is closed under going down in D.
- **Boxes (proved, needs only injectivity).**
  - For a box D = ∏[0, L_a) and any n: Σ_a u(top_a x) = (d−1)u(x) for every cell, with u = M − v.
  - Hence B = (d−1)Σu = (d−1)mM/2, using the symmetry x ↦ L−1−x.
  - GW then follows from M ≥ m − 1. A box gives a symmetric Δ (c = 2g).
- **Geometry-of-numbers form.**
  - For fixed D, B(D,n) = h_P(n) with P = dm·conv(D) − (d+1)Σ_D x. This is a support function: convex and
    1-homogeneous.
  - GW for D ⟺ the convex body τ·P° contains no unit-class point of Λ^∨, where τ = (d−1)m(m−1)/2.
  - Its volume is of order m^{d−1} = det Λ^∨, so the statement is at the scale of the lattice.
  - Residue completeness is the discrete shadow of the tiling D + Λ = ℤ^d. The ISI counterexamples do not tile.
- **Why GW matters for the proof.** Since minimality is not needed, moves that leave the Apéry world are allowed:
  - flips (remove a corner y, add an addable y' ≡ y);
  - lifts n → n ± m e_a;
  - unit changes s → us.
  - A proof can be a local-minimum analysis. Show that every (D, n) that no E-decreasing move improves has E ≥ 0.
    The richer move set should make the local minima rare (carry-free domains, boxes, the MED stars).
  - Adversarial annealing over exactly these moves is running on fejer: d = 3..6, m ≤ 40
    (src/scratch/gw/gw_anneal.py).

## 2026-10-18 (late night, continued) — GW proved in dimension 2; how far the reflection method goes

- **Corner reflection (PROOFS GW-8).**
  - For n > 0, every gap v(x) − im reflects through any maximal y ≥ x to the element v(y − x) + (i−1)m of Δ below c.
  - Hence |U_i| ≤ t_i|L_i| and g ≤ t(D)·ℓ, so GW holds when t(D) ≤ d.
  - This is FGH's g ≤ tℓ, valid for all residue-complete down-sets. Checked on every instance: d = 2 (m ≤ 20),
    d = 3 (m ≤ 12), d = 4 (m ≤ 9), with 0 violations.
- **Dimension 2 (PROOFS GW-10, GW-11).**
  - A residue-bijective staircase has ≤ 2 corners. Proof: three-distance theorem on each fibre mod gcd(s_1, m), plus a
    splitting argument showing that all fibres have the same size.
  - So GW holds for d = 2: Down-set Wilf in dimension 2 is a theorem.
  - Computer check of the lemma: no residue-bijective staircase with ≥ 3 corners for m ≤ 34 (all s), nor for
    m = 35–42 with both s_i non-units (E172).
- **What does not work (each recorded with data in EXPERIMENTS E171–E176).**
  - **Continuous relaxation.** Replace the down-set by a star-shaped density φ with periodization 1 mod m. The resulting
    bound ∫⌊t/m⌋φ ≤ (d/(d+1))(M − m) FAILS when d ≫ K = ⌊M/m⌋: the mass can sit in the top window with exponentially
    small mass below.
    - The discrete inequality survives because 0 and the d unit vectors are cells.
    - The MED star (d = m − 1) is exactly that extreme. Discreteness is essential.
  - **GW\*** (no residue hypothesis, right side (d−1)Σ(v mod m)): false. Example: m = 3, D = {0, e1, e2}, n = (2,2).
  - **Reflection Hall** (match every gap into d copies using reflection edges only): holds for d = 2 but fails for
    d = 3, needing capacity 4 > 3.
    - Example: m = 7, n = (8,11,5), D = {0, e3, 2e3, e2, e1, e1+e3, 2e1}.
    - Every corner's own gap v(y) − m can reflect only to 0. With t₁ > d such corners, 0 is overloaded.
  - **Lift monotonicity** (some n_a → n_a − m never raises E): fails in about 10% of instances. So GW does not reduce to
    the residue form RW by lifts.
  - **Single-flip corner reduction** (a flip with E' ≤ E and t' < t whenever t > d): fails in 10–40% of the t > d
    instances for d = 3.
  - **Depth-refined reflection** (GW-9, weighted by |L_i|): covers 50–60% of the t > d instances for d = 3, and 85–95%
    for d = 4 (m ≤ 9).
- **Exact accounting for t > d.**
  - Put Θ = Σ_{gaps}(ν − 1), where ν(z) is the number of corners above the class cell of z. Put σ = Σ_y(ℓ − ℓ_y), where
    ℓ_y = Σ_{x ≤ y} κ(x) is the exact image size of y's reflection.
  - Then g = Σ_y ℓ_y − Θ, so GW ⟺ (t − d)ℓ ≤ σ + Θ. This is the GW analogue of Marashdeh's identity
    W = (e−t−1)ℓ + σ + Θ.
  - The missing ingredient for d ≥ 3: a second family of injections that absorbs the corner gaps v(y) − m.
    - In the multiplicity form (n_a > m) the corner gap v(y) − m has a canonical second image: the element v(y − e_a)
      < c, for any a with y_a > 0. The map y ↦ y − e_a is injective for each a.
    - Combining these "direction maps" with reflections for the other gaps is the next thing to test.
- **Box-sum criterion BS (nearly always true).**
  - The sharp reflection count is g = Σ_{corners y} ℓ_y − Θ, with ℓ_y = Σ_{x≤y} κ(x).
  - BS: Σ_y ℓ_y ≤ dℓ. BS implies GW.
  - BS holds on every instance except:
    - d = 3: 30 of 44,712 at m = 9, 6 of 60,264 at m = 10, 0 at m = 11, 6 of 138,672 at m = 12;
    - d = 4: no failures (m ≤ 9).
  - Example failure: m = 9, n = (19,21,22), D = level-≤2 simplex minus e1+e2, with five corners all at κ = 4.
    - There Σ_y ℓ_y = 34 > 30 = dℓ, while g = 26 because Θ = 8.
  - So the overlap term Θ matters only for near-stars.
- **Flip-local minima are not all covered by GW-9.** For d = 3, m = 7–10, 42/1626, 192/3222, 462/6306 and 690/10536 of
  the local minima of E (no E-decreasing flip) have t > d and fail GW-9. They have E = 6–18, not tight. The descent
  strategy "flip down to a local minimum, then apply GW-9" needs another ingredient.
- **RRW (real relaxation of the lifts) is FALSE.**
  - Replace integer k ≥ 0 by real k ≥ 0. By LP duality, GW for all lifts at once becomes
    max{(x̄ − p_D)·s : x̄ ∈ conv(D), x̄ ≥ p_D} ≥ (d−1)(m−1)/(2d), with p_D = ((d+1)/d)·centroid.
  - It fails by 1–2.4 in d = 2, 3 (e.g. d = 2, m = 10, s = (1,7)). Integrality of the lift k is essential.
- **Near-stars (level ≤ 2), exact reduction.**
  - Setup: D = {0, e_a} ∪ Q, with Q a multigraph on [d] (loops allowed) and m = 1 + d + q. Put n_a = mk_a + s_a,
    K = ⌊M/m⌋ and δ_a = K − k_a.
  - GW ⟺ (d+1)·Σ_a (1+deg a)δ_a ≥ (d+2)qK + (d+1)Σ_Q ε + d(m−1−ρ*), with ε_ab = [s_a + s_b ≥ m].
  - The constraints are δ_a + δ_b ≥ K + ε_ab on edges.
  - LP duality with y_e = 1 + 1/(d+1) (feasible because deg a ≤ d+1) gives the left side
    ≥ (d+2)qK + (d+2)Σε. This proves GW for near-stars whenever the maximum has residue ρ* = m − 1.
  - The general case needs the residue slack d(m−1−ρ*). The units with residue above ρ* and high degree are the
    obstacle. NEXT: finish this case, since near-stars are exactly the thin regime that defeats HCR.

## 2026-10-19 (early) — the prefix (window) family PGW; the GW scan; mechanisms that fail for t > d

- **GW scan (codex, E186).**
  - Independent C enumerator: 0 failures in 138,091,734,792 instances (d = 3, m ≤ 30; d = 4, m ≤ 22; d = 5, m ≤ 19).
  - Adversarial search: 92.8M candidates to m = 100, 0 failures.
  - Smallest E/c with t > d and c ≥ m: 1/9, at d = 3, m = 7, n = (12,11,20).
- **Mechanisms that fail for t > d.**
  - Per-depth |U_i| ≤ d|L_i| is false (E183). So is the suffix family (E187).
  - Column reflections do not cover every gap. Column + corner edges still need capacity 4 in 3-D (E184).
  - Allowing depth-lowering edges (gap at depth i → element at depth h ≤ i) changes the picture:
    - corner edges alone still fail;
    - corner + column edges give b* ≤ d on every d = 3, m ≤ 8 instance (E185).
- **New conjecture PGW (PROOFS, "Prefix (window) Wilf").**
  - If depth-lowering is allowed, Hall's condition is exactly the prefix family
    P_i: Σ_{j≤i}|U_j| ≤ dΣ_{j≤i}|L_j|.
  - For semigroups P_i reads WW_i: #(gaps below im) ≤ (e−1)·#(S ∩ [c − im, c)). It is Wilf for im ≥ c.
  - Evidence: 0 failures on 5.86·10⁹ down-set instances (E188) and on all 2.8·10⁸ semigroups of genus ≤ 36 (E189).
  - It is false for windows that are not multiples of m.
  - The increments are not single-crossing (E190), so PGW does not follow from GW that way.
- **Proved.**
  - GW-12: PGW when t ≤ d.
  - GW-13: per-depth |U_j| ≤ d|L_j| whenever every n_a ≥ jm. Proof: the descent map x ↦ x − e_a, at most d to one,
    lands in L_j because x − e_a is non-maximal.
  - GW-14: g ≤ dΣ_{j≤k_min}|L_j| + Σ_{j>k_min} t_j|L_j|. So only corners deeper than k_min = min⌊n_a/m⌋ can break GW.
  - GW-15: WW_1 for every semigroup, (e−1)|Ap ∩ [0, c)| ≥ m − 1, and the corner bound d·t(D) ≤ (d−1)|D| + 1.
    Elementary.
- **Reading.**
  - The descent map handles the shallow depths; corner reflection handles the case of few corners.
  - The two failure modes are disjoint in kind. Descent fails at depth j only through directions with n_a < jm.
    Reflection fails only through corners: more than d corners at depth j.
  - A proof of PGW has to trade between them across depths. The tight cases (e = 2 and maximal embedding dimension)
    are the extreme of each mechanism.
- NEXT: P_2 in the multiplicity form with k_min = 1. The obstruction there is a cell x with κ(x) ≥ 2 all of whose lower
  covers x − e_a use directions with n_a < 2m.

## 2026-10-19 (early, continued) — P_2 proved without residues; arithmetic first enters at depth 3

- **Theorem GW-16 (PROOFS).** In the multiplicity form (every n_a > m), Σ min(2, κ) ≤ dΣ min(2, λ). It holds for every
  down-set and every such n; residue completeness is not used.
  - Left side, exact: 2(m − 1) − |A|, with A = {a : n_a < 2m}.
  - Right side: NonMax ⊂ L_1, and every non-maximal cell with a 2-step or a "long" upper cover lies in L_2.
  - What is left is a pure shape inequality. Call T the non-maximal cells whose upper covers are all corners in
    A-directions. It reads d|T| − |A| ≤ 2·(d|NonMax| − (m − 1)): twice the slack of the corner bound CL.
  - Proof: route the descent map away from T. Only the corners Y whose lower covers all lie in T are forced into it.
    Counting pairs (corner, lower cover) gives 2|Y| ≤ |A|(|T| + 1).
- **Corollary GW-17 (semigroups).** #(gaps < 2m) ≤ (e − 1)·#(S ∩ [c − 2m, c)) for every S. For c ≤ 2m it is Kaplan's
  theorem; for c > 2m it is a new constraint on the first two Kunz layers against the top two windows below c.
- **Depth 3 needs arithmetic.** Without residues P_3 fails already for d = 2: the 2-D level-2 simplex with n = (9,9)
  and m = 6. Every pair carries (ε = 1), which residue completeness forbids.
  - This matches the literature: c ≤ 2m (Kaplan) is elementary; c ≤ 3m (Eliahou) needs Macaulay's theorem. P_3
    contains Eliahou's case.
- So the ladder is: P_1 (descent), P_2 (descent + corner counting; shape only), P_3 (first arithmetic rung), …,
  P_q = Wilf.
- NEXT: formulate P_3 as shape + carry graph. The data are κ(e_a + e_b) = k_a + k_b + ε_ab. Residue completeness
  constrains which carry patterns ε can occur together with the shape. Find the residue fact that kills the d = 2
  example and test whether it suffices.

## 2026-10-19 (night) — each window rung gives a pseudo-Frobenius criterion; trapped cells; column reflection per cell

- **Window rungs to Wilf criteria (PROOFS GW-PF, GW-18).**
  - FGH reflection refined by depth: only PF numbers ≥ (j − 1)m serve the gaps at depth j.
  - So P_i plus this reflection gives: Wilf holds whenever at most e − 1 PF numbers are ≥ im.
  - With P_2 (proved), this is GW-18. It covers 99.86% of semigroups of genus ≤ 24; the classical t ≤ e − 1 covers
    95.16%.
  - With P_3, all but 32 semigroups of genus ≤ 24 would be covered. Each rung removes nearly all remaining
    semigroups, but a uniform mechanism is still needed.
- **Trapped-cell inequalities (PROOFS).**
  - Routing the descent map away from the shallow cells reduces local P_i to TCI_i: i|Y^{(i)}| ≤ dΣ_{j<i} j|T^{(j)}| + β'_i.
  - TCI_2 is Lemma Y. TCI_∞ is local GW, and the reduction is lossless in the limit.
  - TCI_i holds on all data. Pair counting leaves only the trapped cells of support < i. The crude slot bound is false,
    so the unused upper-cover slots are needed.
- **Column reflection per cell (E196).**
  - Since every column reflection R_a is a bijection, Σ_x[Σ_a λ(R_a x) − κ(x)] = dℓ − g exactly.
  - Per cell this fails only at corners, by at most d − 1 (carries among the axis residues r(y_a e_a)).
  - Inner cells carry slack ≈ Σ_a(M − v(top_a x))/m. This is the column form of B ≥ τ. What remains is to move the
    inner slack to the corners near the top.
- **Residue structure that matters: translation permutations.**
  - Residue completeness makes each τ_a (residue + s_a) a permutation of D. It links the a-columns into cycles: the top
    of each column goes to the bottom of the next, and the drops μ sum to n_a.
  - The 2-D proof (three-distance theorem) is this cycle structure. P_3 needs some consequence of it; residues are
    necessary there (E191).
- Delegated: codex P3 task (prove P_3 / LP_3 / TCI_3; brief in session scratchpad).

## 2026-10-19 (late night) — P_3 proved; Wilf is "carries ≤ column slack"; the c ≤ 4m frontier

- **P_3 is a theorem (PROOFS GW-19).** The proof is by codex; I re-checked every step.
  - For 3m ≤ M < 4m, P_3 = GW. The band classification, the weighted shadow count 3u ≤ (a+2)q, the bound t ≤ ρ and
    g + ℓ = M − m + 1 suffice; no Macaulay theorem is needed.
  - For M ≥ 4m − 1, Theorem H needs no residues. Column reflection gives d Σ F(M−v) = Σ_x Σ_a F(x_a n_a) + CS. The only
    deficit cells are the carried mixed quadratics, and each is paid by a surplus cubic or by a two-cell column.
  - Semigroup form: #(gaps < 3m) ≤ (e−1)·#(S ∩ [c−3m, c)) for every S. This contains Eliahou's c ≤ 3m theorem.
- **Untruncated (H1) gives a clean form of Wilf:**

      Σ_x carry(x) ≤ Σ_{columns} [(J+1)λ(top) + #{j : (j n_b mod m) + ε_top ≥ m}].

  - carry(x) = ⌊Σ_a ((x_a n_a) mod m)/m⌋ lives only on cells with support ≥ 2.
  - Column slack lives on columns whose top is below M − m, or whose top's residue offset ε catches the column's own
    residues.
  - Tight families (⟨5,6⟩, T_{m,4}): no carries and zero slack.
- **K = 4 (Wilf for 3m < c ≤ 4m, OPEN in the literature, item 22).** The K = 3 band proof does not transfer face by
  face.
  - The pure-A face can be deficient by up to about a³/6. The configuration has every AA cell in I_3 and every AAA
    cell in I_4; these are exactly the Eliahou–Fromentin B_3-sets.
  - Example: ⟨23,35,37⟩ ∪ [92,∞) has W(F_1) = −1 with ρ = 0. The deficit is offset only because residue completeness
    forces the uncovered residues (≈ m/6 of them, in the middle third) onto other directions, and each of those adds
    ℓ(F_1) ≈ a²/2 to the multiplier.
  - So the missing ingredient at K = 4 is a residue-coverage lemma: the residues a deficient face misses force many
    directions outside it.
  - GW = P_{K−1} + (N_top ≤ d + slack). N_top ≤ d alone is false, though rarely (E201).
  - Near-tight K = 4 semigroups are only T_{m,4}-type (W = ρ), so a lossy argument has room.
- Next:
  - (1) Delegate P_4 / K = 4 to codex, with the column-carry framework.
  - (2) Lead: a general carry-to-column charging, i.e. a Theorem H for i ≥ 4 using residues. Find which columns pay
    each carry, and why residue completeness guarantees enough slack.

## 2026-10-19 (small hours) — P_4 partly proved; Wilf for 3m < c ≤ 4m reduced to RC4; uniform conjectures TR and H_i

- **GW-21 (codex P4, re-checked by the lead; identities verified by exact polynomial arithmetic).**
  - H4: residue-free P_4 for M ≥ 6q − 1. The cutoff is sharp (degree-4 simplex in ℕ³, n = (52,52,52), q = 35).
  - Primary regime (Wilf for 3m < c ≤ 4m) proved when a ≤ 3 small generators lie in (m, c − 2m). This covers
    99.8% of such S at genus ≤ 28.
  - The mechanism is the one I guessed and codex quantified: the exact identity W = W_A + T + R (outside cells
    never hurt), plus the signed-B_3 packing m ≥ C(a+3,3) + 2C(a+1,3). The packing turns a deficient
    (B_3-saturated) A-face into missing residues, hence outside directions, hence compensation.
  - Open: RC4 for a ≥ 4, and the window 5m ≤ M ≤ 6m − 2. The codex session was resumed on these.
- **TR (uniform transfer, E205).** W ≥ W_A at every K, on all semigroups of genus ≤ 28 and all small residue-complete
  down-sets. Residue-free it fails only when A = ∅, which is plain GW failure. So "outside cells never hurt" looks
  uniform in K.
- **H_i (uniform residue-free window, E208).** The residue-free cutoffs are 4q (i = 3) and 6q (i = 4), and simplices
  give exactly 2i − 2 for i ≤ 6.
  - If H_i holds for all i, then with GW-PF Wilf follows whenever ≤ e − 1 PF numbers lie in the upper half
    (≥ ⌊(K+2)/2⌋m), uniformly in K. That would generalize FGH.
  - The residual class sits at K = 4, 5 (E206), where residues are unavoidable.
- **Strategic picture.** Universal Wilf now splits into:
  - (i) residue-free large-M window theorems H_i (combinatorial charging; i ≤ 4 done);
  - (ii) low-K regimes with residues, i.e. GW at K = 4 (RC4), K = 5, … The mechanism there is transfer + packing.
    It needs a K-uniform packing/stability lemma: a deficient small-generator face is B_h-saturated, saturation
    forces missing residues, and missing residues force compensating directions.
  - (iii) the top correction N_top ≤ d + slack, where it is not already implied.

## 2026-10-19 (early morning) — PCI on light columns proved; the half/half split is dead; the hard class

- **Proved (GW-23).** PCI holds for every dominant column with n_b ≤ 2q − 1, at every i.
  - Proof: c_k ≤ trapezoid φ(a_k); the multiples of q per w-block are ≤ 2; reflect the trapezoid; the "middle region"
    has length ≤ 2 and contains no doubled block. This is because of the cutoff (2i−2)q − 1.
  - Corollary: H_i (residue-free P_i for M ≥ (2i−2)q − 1) for every down-set with active weights in (q, 2q).
- **Refuted.** PCI for heavy columns (w ≥ 2q) at i ≥ 10 (first: i = 10, q = 9, w = 22, three base components 17,
  J = 5). The GW-22 route cannot give H_i for all weights; the discarded non-dominant slack is needed.
- **Refuted (E212).** The top-half split. S_i = Σ_{k>i}(|U_k| − d|L_k|) ≤ 0 at i = ⌊(K+2)/2⌋ fails often at m ≤ 40
  (up to +88). So "bottom half residue-free + top half arithmetic" does not decouple.
- **Measured (E212).** GW-PF + H_i covers only ≈ 4 points more than GW-20 at m ≤ 40. The residual is semigroups with
  many PF numbers near the very top. Decision: stop H_i at GW-23 (heavy weights not worth it).
- **Observation (E212).** The hard class (> e − 1 PF numbers ≥ 3m, the only class not covered by Eliahou + GW-20)
  carries large Wilf slack: W ≥ 0.11c in all 4.8e5 samples, and ≈ 0.17c under adversarial search.
- **Reformulation (E213).** Marashdeh's Conj 5.2 (open; checked by him for genus ≤ 35) is equivalent to
  W(S) ≥ σ_d(S) := Σ_{top e−1 PF f} |S ∩ (f, F]|, i.e. g ≤ Σ_{top e−1 PF f} |S ∩ [0, f]|. Our test: 0 failures up to
  m = 60.
  - Down-set form DMC: Σ_x κ(x) ≤ Σ_{k ≤ min(d,t)} Σ_x ⌊(V_k − v(x))/m⌋₊, with V_1 ≥ V_2 ≥ … the values of maximal
    cells. It interpolates between corner reflection (t ≤ d, proved) and GW.
- **Next.**
  - Test DMC on general residue-complete down-sets, together with its prefix version MC_i (PGW with the top-d
    corners).
  - If it survives, try to prove MC_2 / MC_3 with the GW-16/19 machinery. Those proofs pay deficits with column slack;
    with several corners, the top d corners' columns should carry the slack.

## 2026-10-19 (morning) — P4 continuation verified; the arc lemma; a uniform result in the primary regime

- **Verified (GW-24).** Codex P4 §§12–19, line by line.
  - On paper: a = 4, 5, LC, LP/SP/HP, and distinct-weight H4 (M ≥ 6m − 3).
  - Both a = 6 certificates and the a = 7 coverage were re-implemented independently. All counts match exactly
    (36,389 vectors; exclusions 3,118/32,639/65/564; 3 survivors).
  - Semigroup corollary: Wilf for 3m < c ≤ 4m with ≤ 6 generators in (m, c − 2m).
- **New mechanism: the arc (GW-25a).** Elements of S in [c, (k+1)n_1) sit over residue classes whose Apéry
  elements have length ≤ k. So the short Apéry elements number at least (k+1)n_1 − c.
  - In band language this uses where τ = v − deg·m sits *inside* its band. Packing (LP/SP/HP) uses only residues
    and loses a factor ≈ a. The arc does not.
- **Proved (GW-25).** Pure A (all generators < c − 2m), 2n_1 ≥ c − m, 3m < c ≤ 4m:
  W = 3a² + 4a + 1 + (a−2)p − 3u − h exactly. The arc gives h ≤ 2p + 2, so W ≥ a − 1 + 6(C(a+1,2) − p) ≥ e − 2.
  - This holds for every e. It has r = 0 right generators, so E = W there.
  - CORRECTION: it does NOT contain the Eliahou–Fromentin near-misses, which need r > 0. Those are in the GW-26
    class.
  - It replaces the a = 7 computer certificate and closes codex's "uniform remaining claim".
  - Sharp: there are semigroups with h = 2p + 2 (E216).
- **Refined arc.** With outside directions (still 2n_1 ≥ c − m), the arc Y ⊂ [h, 3h/2) can only hold AA, B/C/E
  units, and I₄ AB/BB cells. No cubic, AC or BC cell can occupy it.
  - LP: exact identity + shadows + short-residue lemma + refined arc gives min W = (a−1)(b+1) for c = e = 0,
    except for b ≫ a.
  - In that regime the minimiser is a "B-world" (c ≈ 3m behaviour on the B face). Adding Macaulay z ≤ t₃^{⟨2⟩}
    restores min = (a−1)(b+1) (checked to (100, 1000)).
  - Conjecture GW-26: Wilf for 3m < c ≤ 4m whenever 2n_1 ≥ c − m.
  - Sent to codex (P5) for an analytic all-parameter certificate, with the q₂ > 0 extension as a stretch goal.
- **Strategic note.**
  - The primary regime (Wilf for c ≤ 4m) now has two uniform pieces (GW-25, and GW-26 pending) plus a ≤ 6.
  - What is left is low units (q₂ > 0) with many A directions.
  - The general lesson for all K: W = Σ_x [Kd − (d+1)j(x)] + ρ, where only top-band cells cost. ρ is controlled by
    arcs, which see positions inside bands. This should be tried as the K-uniform mechanism.

## 2026-10-19 (midday) — Wilf for quadratic Apéry sets at every depth (GW-27); a general cell identity
CORRECTION (same day): GW-27 re-proves the Flat-MaxCL corollary of 2026-10-17 (night 10), which is already LEAN-checked
(`wilf_of_apery_height_le_two`). It is not a new theorem of the project. The height-3 obstruction found below
(every cubic split uses a unit, so no pointwise load bound) was also recorded on 2026-10-17 ("Height-3 natural scheme —
CORRECTION"). New here: the G-ID cell identity for all degrees, the location data of E220, and the refutation of WQ.

- **GW-27 (proved, checked on 62M semigroups).** If every Apéry element is 0, a generator or a sum of two
  generators, Wilf holds. Corollary: Wilf whenever 3n_1 > c + m, with no condition on e or m. This removes Spirito's
  hypotheses (e ≥ 10, m ≤ (8/25)e² + …).
- **Mechanism.**
  - Exact identity: W = Σ f_a λ_a + D_hi + Σ_pairs c_x with c_x = (d+2)λ(x) + β_x − γ_x ≥ −1.
  - A cell has c_x = −1 only if it lies in the top window, has a carry and no bonus. Such cells have residue in
    [1, μ] and both units above μ.
  - Every pair cell with residue in (μ, 2μ] has c_x ≥ 1.
  - Counting residue occupancy in [1, μ] against (μ, 2μ] gives W ≥ F + d − D_mid. When 2μ ≥ m it gives W ≥ F.
  - Nothing uses depth: K = ⌊M/m⌋ never enters.
- **General cell identity (G-ID, exact for every residue-complete down-set D).**

      W = Σ_{y≠0} λ(y)φ(y) + Σ_x Σ_a x_a β_{x,a} − Σ_x γ(x),

  where φ(y) = Σ_{a : y+e_a ∉ D} (y_a + 1) ≥ 0, β_{x,a} = [ε_x + r_a ≥ m] and γ(x) = ⌊Σ_a x_a r_a / m⌋.
  - Proof: λ(x − e_a) = λ(x) + κ_a + β_{x,a} and κ(x) = Σ_a x_a κ_a + γ(x). Sum over D; the coefficient of λ(0)
    cancels.
  - GW-27a is the degree-2 case. Wilf in general ⟺ Γ ≤ Σ λφ + B.
- **Why degree 3 is harder.**
  - The deficiency of a cubic cell can be 2.
  - An interior cell (φ = 0) with λ ≥ 1 can be deficient.
  - A window cell can have c_x = 0, e.g. three units with r = 6 when μ = 10 and s = 18.
- **Open question.** Is there a multi-window version of the occupancy count, (μ, 2μ], (2μ, 3μ], …, that pays the
  cubic deficits?
