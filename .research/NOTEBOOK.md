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
