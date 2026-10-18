# STATE.md — handoff (updated 2026-10-18, night 13)

## Main route
Wilf ⇐ TOP'' (Lemma A, LEAN `wilf_of_TOP2`) ⇐ Tile-TOP'' ⇐ MaxCL (LEAN) ⇐ Tile-CL (d ≤ 5 only; false at d = 6).
**τ-criterion (LEAN-CHECKED, lean/Wilf/TauCrit.lean):** with τ = |Ap ∩ [c, c+m)| = #gaps in [c−m, c),
Wilf holds when (e−2)(m+1) ≥ 2(e−2)τ + 2P₂. Current focus: **Wilf for e = 4** (open in the literature).
**e = 4 split:** two-face tiles (some e_a + e_b ∉ D) — **PROVED (paper)**; non-two-face tiles — OPEN (G2).

## Proved facts (paper unless marked)
- CH, Corollary H, Lemma A, TOP'' ⇒ Wilf, CH', CL ⇒ Wilf, Tile-TOP'' ⇒ Wilf, MaxCL ⇒ Tile-TOP'': LEAN.
- Flat-MaxCL (height ≤ 2) and Ap ⊆ {0} ∪ P ∪ 2P ⇒ Wilf: LEAN. 2-D Tile-CL (every 2-D tile), Wilf e ≤ 3: LEAN.
- Cross Lemma + τ-criterion: LEAN. Two-face box theorem (MaxCL): paper.
- Λ-criterion Λ ≥ (e−2)(m−1)/2 ⇒ Wilf; cylinder structure of 3-D tiles (PROOFS.md).
- **NEW (night 13): THEOREM — Wilf for every e = 4 semigroup with a two-face tile** (PROOFS.md section "THEOREM
  (two-face e = 4)"): two-face identity + four bounds A', B'', C, D + exact integer check m ∈ [18, 400]
  (tf_bounds2.py) + analytic m ≥ 75 + Eliahou (c ≤ 3m) + BGOW (m ≤ 18). Novelty UNVERIFIED; not in Lean.
- **NEW: t = 0 two-face tiles are rigid** (each face ≤ 1 inner corner, |A| ≤ 4).
- **NEW: general e = 4 faces+core identity** (NOTEBOOK night 13, proved; exact on 7,019 S):
  3mW + 3m(m−1) = (m − 4(ΣL−2))M + 4Def_faces + 4SumAxes + 4Σ_{core}(2M − 3w).

## Observed (not proved)
- Tile-CL exhaustive d=3 m ≤ 20, d=4 m ≤ 14, d=5 m ≤ 12. TOP'' always (genus ≤ 18 + extended).
- NAW for all e = 4 with m ≥ 17 tested. max τ (e = 4) ≈ 2√m − 1 (box-like, two-face).
- θ = mean(Ap)/max(Ap): non-two-face, c > 3m, m ≤ 20: θ ≤ 0.664 (need ≤ 11/16 = 0.6875 for Wilf when c > 3m).
  Continuum cylinder-minus-cone: θ ≤≈ 0.677.

## Refuted (preserved in NOTEBOOK/EXPERIMENTS)
Residual of sharp τ-criterion ⇒ two-face; PE; Λ-dichotomy; Λ-criterion e = 4 m ≥ 20; S1 for two-face;
**non-two-face ⇒ τ-criterion (FALSE m = 23, 25: ⟨23,25,28,35⟩, ⟨25,27,32,40⟩)**; face-wise ν injectivity; VTC
(virtual Tile-CL for non-down hook tiles); naive dominance injection (⟨13,22,23,25⟩); continuum "2/3 law" for
cylinder shapes (θ ≈ 0.677).

## Open gaps
- G2: **non-two-face** e = 4 (every p_a + p_b ∈ Ap). Sub-cases: three-face tiles (core = ∅ or q* = (1,1,1)) and tiles
  with a core. Tools: faces+core identity, τ-criterion, cylinder lemma, θ ≤ 11/16.
- G3: Tile-CL d = 3 in general (route I). G4: Lean formalization of the two-face theorem.

## Three active approaches
1. Non-two-face e = 4 via the faces+core identity with A'/B''/C/D-type bounds (parameters: axis lengths, top-layer
   counts per face, core size).
2. θ-route: Def := Σ_Ap(M − w) ≥ mM/4 for non-two-face tiles with c > 3m (shape inequality + lattice-tile condition).
3. Universal: τ/Λ-criteria refinements toward TOP''; Tile-CL d = 3 with the cylinder structure.

## Next precise task
Non-two-face e = 4: collect all τ-criterion failures (c > 3m, m ≥ 19) and test which faces+core bound covers them;
formulate the parametric bounds (face top-layer counts, core size) and attempt the analogue of the two-face proof.
