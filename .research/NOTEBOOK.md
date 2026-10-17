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
