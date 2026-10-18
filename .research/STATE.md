# STATE.md — handoff (updated 2026-10-17, end of night 10)

## Main route
MaxCL ⇒ Tile-TOP'' (PROVED on paper, PROOFS.md) ⇒ Wilf (LEAN, lean/Wilf/TileTop.lean, 0 sorry, standard axioms).
**MaxCL**: for every tile (D,p) (down-set D ⊂ ℕ^d, |D| = m, φ(x) = p·x mod m bijective), every σ, r = ⟨φ − σ⟩:
    Σ_{y∈A} (|y| − 1) r(y) ≤ (d+1) Σ_{z∈N} r(z)     (A = maximal cells, N = the rest).
Wilf for S needs only σ = c mod m; for m | c that is σ = 0 (Wilf for m | c is itself open).

## Proved facts (paper unless marked)
- CH, Corollary H, Lemma A, TOP'' ⇒ Wilf, CH', CL ⇒ Wilf, Tile-TOP'' ⇒ Wilf: LEAN-checked (lean/Wilf/*.lean).
- MaxCL ⇒ Tile-TOP''; decomposition identity r(u)+r(v) = r(y)+r(0)+mκ, κ ∈ {−1,0,1}; κ = −1 forces r(y) ≥ m − r(0).
- **Flat-MaxCL (night 10): MaxCL for all tiles of height ≤ 2.** Corollary: Wilf when Ap(S,m) ⊆ {0} ∪ P ∪ (P+P)
  (contains reduction number ≤ 2). Novelty unverified: 2 searches (alphaXiv, web) found no such statement.
- Identities: sawtooth form; exact column form; lift form MaxCL ⇔ Σ_aβ_aρ_a + β_0ρ_0 ≤ m·Σ_x w(x)K(x) (night 10 notes).

## Refuted (preserved in examples/ and EXPERIMENTS.md)
CL, Tile-CL (E47), Load Lemma (E64, ⟨39,71,72,77⟩), GLL1, uniform box pairing, crude rearrangement bound in the open
regime (E69), injective (non-tile) MaxCL (d=1, D={0,1,2}, m=100, p=90, σ=90: 90 > 20).

## Open gaps
- G1: MaxCL for height ≥ 3. At height 3 every decomposition of a level-3 cell uses a unit, so unit loads exceed d+1
  in aggregate once n3 > d(d+1)/2; the flat template (pointwise load ≤ d+1 + window count) cannot work alone.
- G2: Lean: formalize Flat-MaxCL (statement + proof) and MaxCL ⇒ Tile-TOP''.
- G3: novelty of the height ≤ 2 corollary (compare Eliahou W_0 ≥ 0, Dhayni, Spirito exact hypotheses).

## Three active approaches
1. MaxCL by height: find the height-3 mechanism (unit overload paid by distinctness of positions; at σ = 0 the
   tile is a partition ℤ/m = {0} ⊔ U ⊔ (restricted 2-sums) ⊔ (restricted 3-sums), an additive-combinatorics statement).
2. m | c case: MaxCL at σ = 0 only (subadditive positions, carries only, no wraps).
3. Window/lift calculus: general wrap-counting via K(x) = ⌊L(x)/m⌋ and window counts of positions.

## Next precise task
Prove MaxCL at σ = 0 for height-3 tiles (approach 2 ∩ 1): Σ_aβ_aρ_a ≤ m(2Σ_T K + Σ_{E^A}K − (d+1)Σ_{E^N}K) with
K = carries, using distinctness of the sums. First find the smallest height-3 tiles with the least σ = 0 slack.
