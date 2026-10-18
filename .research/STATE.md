# STATE.md — handoff (updated 2026-10-18, night 12 late)

## Main route
Wilf ⇐ TOP'' (Lemma A, LEAN `wilf_of_TOP2`) ⇐ Tile-TOP'' ⇐ MaxCL (LEAN) ⇐ Tile-CL (d ≤ 5 only; false at d = 6).
**New this session: the τ-criterion** (PROOFS.md "τ-criterion"): with τ = |Ap ∩ [c, c+m)| = #{f ∈ PF : f ≥ c − m},
Wilf holds when (e−2)(m+1) ≥ τ(τ+2e−5) (sharper: ≥ 2(e−2)τ + 2P₂). Corollaries: e = 4 & τ ≤ 4 (no computation),
e = 4 & τ ≤ 5 (with m ≤ 19), any e with τ ≤ e − 1 (⊇ FGH range t ≤ e − 1). Paper proof complete; Lean formalization
running (lean/Wilf/TauCrit.lean, background agent).

## Proved facts (paper unless marked)
- CH, Corollary H, Lemma A, TOP'' ⇒ Wilf, CH', CL ⇒ Wilf, Tile-TOP'' ⇒ Wilf, MaxCL ⇒ Tile-TOP'': LEAN.
- Flat-MaxCL (height ≤ 2): LEAN. Corollary Ap ⊆ {0} ∪ P ∪ 2P ⇒ Wilf: LEAN.
- 2-D Tile-CL for every 2-D tile: LEAN (TileCL2.lean: tileCLAt_of_two, wilf_of_embDim_le_three).
- Cross Lemma + τ-criterion (paper; asserted on all S of genus ≤ 20).
- Any 3-D down-set: T(A) ≤ m + 2t + P₁ (cross counting over all maximal cells).
- At most one minimal non-element of full support in any tile; Σ_x φ(τx) ≡ 0 and Hall reformulation of Tile-CL.

## Observed (not proved)
- Every tile with d ≤ 3 is coherent (Gröbner/Gomory; m ≤ 9) ⇒ every 3-D tile is an e = 4 Apéry factorization tile.
- Tile-CL exhaustive d=3 m ≤ 20, d=4 m ≤ 14, d=5 m ≤ 12. μ = φ + φ∘τ bijective iff type ≤ 2 (always), sometimes 3,
  never ≥ 4. max(T(A) − m) by type constant in m (4, 8, 12, 16, 21, 26).

## Refuted this session (preserved in NOTEBOOK/EXPERIMENTS)
Partition-CL in d = 4; coupling CI_c; box extremality of K; K-descent along wall-crossings (non-box local minima);
non-monomial (G-cluster) Tile-CL; layer decompositions for d = 3 (proved impossible); NT (T(A) ≤ 2m) for non-two-face
tiles at small m; face-wise corner-sum bijection on two-face tiles.

## Open gaps
- G1 (e = 4 residual after the τ-criterion): τ ≥ 5 (≥ 6 with computation) and P₂ > m + 1 − 2τ, i.e. top-layer
  factorizations concentrated on coordinate planes (two-face-like). Needs a 2-D-type argument.
- G2: Tile-CL d = 3 in general (no 3-way mechanism found).
- G3: Lean τ-criterion (running).

## Three active approaches
1. τ-criterion refinements: use exact positions π(u) (not π ≤ m), P₂ exactly, cells outside crosses, and Lemma A's
   E(w) slack; aim to close the e = 4 residual or push the general range τ ≲ √((e−2)m).
2. Planar residual via 2-D theory: when top-layer factorizations lie on few coordinate planes, reduce TOP''/MaxCL to
   2-D tiles (proved 2-D Tile-CL) — the two-face picture.
3. Tile-CL d = 3 (route I) — deprioritized; only revisit with a genuinely new 3-way mechanism.

## Next precise task
Quantify the e = 4 residual of the sharp τ-criterion (P₂ version) on all e = 4 semigroups of genus ≤ 22 and on random /
hill-climbed e = 4 semigroups with m up to ~150: what fraction fails, and is every failure two-face (some e_a + e_b ∉ D)?
Then try to prove TOP'' for the residual using positions π(u) on the planar top layer.
