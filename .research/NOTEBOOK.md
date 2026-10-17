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
