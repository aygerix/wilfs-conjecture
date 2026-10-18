# STATE.md — handoff (updated 2026-10-18, night 12, latest)

## Main route
Wilf ⇐ TOP'' (Lemma A, LEAN `wilf_of_TOP2`) ⇐ Tile-TOP'' ⇐ MaxCL (LEAN) ⇐ Tile-CL (d ≤ 5 only; false at d = 6).
**τ-criterion (LEAN-CHECKED, lean/Wilf/TauCrit.lean):** with τ = |Ap ∩ [c, c+m)| = #gaps in [c−m, c),
Wilf holds when (e−2)(m+1) ≥ 2(e−2)τ + 2P₂ (crude: ≥ τ(τ+2e−5)). Kernel-checked corollaries: e = 4 & τ ≤ 4 & m ≥ 13,
e = 4 & τ ≤ 5 & m ≥ 19, τ ≤ e−1 & m ≥ 3e−4. Current focus: **Wilf for e = 4** (open in the literature).

## Proved facts (paper unless marked)
- CH, Corollary H, Lemma A, TOP'' ⇒ Wilf, CH', CL ⇒ Wilf, Tile-TOP'' ⇒ Wilf, MaxCL ⇒ Tile-TOP'': LEAN.
- Flat-MaxCL (height ≤ 2) and Ap ⊆ {0} ∪ P ∪ 2P ⇒ Wilf: LEAN. 2-D Tile-CL (every 2-D tile), Wilf e ≤ 3: LEAN.
- Cross Lemma + τ-criterion: LEAN. Two-face box theorem (MaxCL): paper.
- **New (night 12 latest):** exact e = 4 accounting m·W + m(m−1) = ARM + m·N + Depth (NOTEBOOK); level/residue split
  m·W + (d−1)m(m−1)/2 = m·Λ + R with Λ = Σ_z λ_L(z)T(z), R = Σ_z T(z)(m − pos z) ⇒ **Λ-criterion** Λ ≥ (e−2)(m−1)/2 ⇒ Wilf.
- **Cylinder structure of 3-D tiles** (PROOFS.md): ≤ 1 full-support minimal non-element q* (∈ Λ); support-{a,b}
  minimal non-elements ≡ t·e_c with distinct t, t e_c ∈ D; D = cylinders over coordinate slices minus (q* + ℕ³).
  Checked all 3-D tiles m ≤ 12.

## Observed (not proved)
- Tile-CL exhaustive d=3 m ≤ 20, d=4 m ≤ 14, d=5 m ≤ 12. TOP'' always (genus ≤ 18 + extended).
- NAW (Depth + mN ≥ m(m−1)) for all e = 4 with m ≥ 17 tested (75,588 S m ≤ 24 + families + random m ≤ 200).
- max τ (= max type) for e = 4 ≈ 2√m − 1 (box-like); min W for e = 4 ≥ m for m ≥ 17 except box a = 5.
- Non-two-face e = 4 tiles: T(A) ≤ 2m + 6 (m ≤ 20), random ≤ 1.9m; CR always.

## Refuted this session (preserved in NOTEBOOK/EXPERIMENTS)
Residual of sharp τ-criterion ⇒ two-face (FALSE m = 14..19); PE (⟨5,8,9⟩); Λ-dichotomy "m > 3e ⇒ Λ-criterion"
(⟨16,27,28,31⟩, ⟨29,30,34,42,43,48,51,53⟩, e=24 m=77); Λ-criterion for e = 4, m ≥ 20 (⟨23,25,28,35⟩);
S1 (Σ_A(|y|+2) ≤ 2m + 2) for two-face tiles (box excess a−1).

## Open gaps
- G1: Wilf/TOP''/MaxCL for **two-face** e = 4 (D = F₁ ∪ F₂ glued along the c-axis, e_a + e_b ≡ t e_c). Boxes done
  (t = 1); L-shapes and t ≠ 1 open. Counting criteria provably insufficient here (box family).
- G2: **non-two-face** e = 4: NT' (T(A) ≤ 2m + C) or CR; needs residue arithmetic (geometry alone allows
  three-triangle-face shapes with T(A) ≈ 3m; arithmetic of slice inner corners must exclude them).
- G3: Tile-CL d = 3 in general (route I).

## Three active approaches
1. Two-face e = 4 via 2-D pictures (+ Hajós-type additive combinatorics, as in the box theorem).
2. Non-two-face e = 4 via cylinder lemma + inner-corner arithmetic (t-values of a slice staircase form APs).
3. Universal: τ/Λ-criteria refinements toward TOP'' (positions π, depth); Tile-CL d = 3 with the cylinder structure.

## Next precise task
Two-face e = 4 (G1): write D = F₁ ∪ F₂ with e₁ + e₂ ≡ t e₃ (t e₃ ∈ D) and classify by t; for t = 1 use the 2-D picture
(Ω' tile) and the proved 2-D Tile-CL slack to close MaxCL for L-shape pictures; quantify how TOP'' slack depends on t.
