# STATE.md — current state (updated 2026-10-17, session 1, late)

## Best current approach
Identity CH' (proved) writes m·W = m·(depth part ≥ 0) + [CL bracket]. The Carry Lemma CL (bracket ≥ 0) implies
Wilf, uses only residues mod m, and is an instance of Tile-CL, a purely combinatorial statement about down-set
fundamental domains of lattices Λ ⊆ ℤ^d with ℤ^d/Λ cyclic. Tile-CL: 0 failures on every tile with d=2 m≤15,
d=3 m≤11, d=4 m≤8; CL: 0 failures on all 712,372 semigroups of genus ≤ 24. Proving Tile-CL proves Wilf.

## Verified facts
- PROVED on paper: CH, Corollary H, Lemma A, CH', CL ⇒ Wilf, all equivalent forms of Tile-CL (PROOFS.md).
- LEAN (kernel-checked, lean/Wilf/Chains.lean, 0 sorry, standard axioms): CH, Corollary H, Lemma A, TOP'' ⇒ Wilf.
- FALSE: PDCL for d ≥ 3; CL for non-complete residue systems; all earlier localizations (PROOFS.md list).

## Open obligations / gaps
- G-CL: prove Tile-CL (the single remaining gap of the main route).  [G-TOP is implied numerically by CL.]
- Lean: formalize CH' and CL ⇒ Wilf (needs factorization down-set D); state Tile-CL as a Prop.
- Novelty of Corollary H and of CL vs literature (not checked).

## Experiments: EXPERIMENTS.md (E0–E17).

## Three most promising active approaches
1. Tile-CL via a cross-direction potential: find Ψ: D → ℤ with Σ_a(window_a sums) − Σ_a p̂_aȲ_a = Ψ-telescoping ≥ −(m−1)/2.
   Use d=3 PDCL failures (smallest: D={000,001,002,010,100,101}, p=(3,5,4), m=6) as test cases.
2. d = 2 case of Tile-CL by explicit L-shape floor sums (mechanism probe; PDCL holds for d=2).
3. Tile moves: D → D∖{z} ∪ {z+λ}; G(D) = Σ_{z∈D} γ(z) is additive over cells; characterize the minimizing tile
   (is it a Gröbner tile? then reduce to Apéry tiles with extra structure).

## Next precise task
Prove Tile-CL for d = 2 (L-shapes): write f(s) as explicit sawtooth sums over the two boundary staircases, and
extract the inequality's mechanism; in parallel search for a potential function coupling directions for d = 3.
