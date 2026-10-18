# STATE.md — handoff (updated 2026-10-18, night 12)

## Main route
MaxCL ⇒ Tile-TOP'' (PROVED on paper; LEAN: tileTOPAt_of_maxCLAt) ⇒ Wilf (LEAN, lean/Wilf/TileTop.lean).
Tile-CL ⇒ MaxCL (drop non-maximal tops). **Current main target: Tile-CL for d = 3 (⇒ Wilf for e = 4, OPEN in the
literature).**  Tile-CL: for every tile (D,p) and s, X(s) = Σ_{x∈D} Σ_a r(t_a x) ≤ (d+1)M', r = ⟨φ − s⟩.

## Proved facts (paper unless marked)
- CH, Corollary H, Lemma A, TOP'' ⇒ Wilf, CH', CL ⇒ Wilf, Tile-TOP'' ⇒ Wilf, MaxCL ⇒ Tile-TOP'': LEAN-checked.
- Flat-MaxCL (MaxCL for height ≤ 2): LEAN-checked (lean/Wilf/MaxCL.lean). Corollary: Wilf when Ap ⊆ {0} ∪ P ∪ 2P.
- **2-D Tile-CL for every 2-D tile (night 12)**: corner-sum map μ(x) = φ(x) + φ(τx) is a bijection; exact slack
  3M' − X = m·Σ_x([r(x)+r(τx) ≤ m−2] − ε(x)) ≥ 0. Classification: 2-D tiles = rectangles and L-shapes. PROOFS.md.
- Tile-CL slack ≡ 0 mod m (integer walk K, steps d − T, mean (m−1)/2); inversion form K = N − κ.
- Σ_x φ(τx) ≡ 0 mod m in every d ⇒ (M. Hall 1952) a complete mapping β exists and T(s) = Σ_x (m−1−r(τx))/m is an
  exact count; Tile-CL(d) ⇔ Σ_x ε(x) ≤ T(s).
- Two-face box tiles satisfy MaxCL; boxes satisfy Tile-CL in every d (Hajós).
- At most one minimal non-element of full support in any tile (any d).

## Refuted (preserved in examples/ and EXPERIMENTS.md)
CL, Tile-CL at d = 6 (E47/E51/E88), Load Lemma, GLL1, uniform box pairing, CR in the open regime, IntervalCL,
per-face split, pairwise 2-D Tile-CL inside 3-D tiles (E87).

## Evidence for the main target
Tile-CL exhaustive: d=3 m ≤ 20, d=4 m ≤ 14, d=5 m ≤ 12 (E83); 10k e=4 semigroup tiles (E82). Tight in ~25% of tiles.
Failures known only at d = 6.

## Open gaps
- G1: Tile-CL d = 3. Known structure: X − M' = Y_c + m·E_ab for each c (E87); (P1) Y_c ≤ 3M' observed; need
  E_ab ≤ (3M' − Y_c)/m. No canonical complete mapping found (E86).
- G2: Lean: formalize 2-D Tile-CL (classification + μ bijection + counting) — high-value, self-contained.
- G3: two-face L-shape MaxCL (bracket can be negative; must use the exact 2-D slack).

## Three active approaches
1. Tile-CL d=3 via the face-chain split: prove P1 (a 2-D Tile-CL for (slice corners, c-columns)) with its exact slack,
   then bound E_ab (sum of slice carries) by that slack.
2. Tile-CL d=3 via a dimension-free mechanism valid for d ≤ 5 (fails at 6): look for the quantity that changes sign
   between d = 5 and d = 6 on core+spike tiles.
3. Route II for e = 4: CR (residue-free) on non-two-face tiles + MaxCL on two-face tiles via 2-D pictures and the
   exact 2-D slack.

## Next precise task
Prove (P1) for d = 3 tiles: Σ_x [r(τ_ab x) + r(t_c x)] ≤ 3M'. First test whether it holds for every tile in every d
(as a statement about one direction c plus slice corners), find its exact slack formula, and check whether
E_ab ≤ slack/m has a pointwise/matching proof.
