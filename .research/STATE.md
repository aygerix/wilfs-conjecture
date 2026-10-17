# STATE.md — current state (updated 2026-10-17, session 1)

## Best current approach
Identity CH (proved) reduces Wilf to a discrete correction term. Lemma A (proved) shows the
correction is controlled by the top layer X_q = Ap ∩ [c, c+m). Conjecture TOP'' (two-level, position-weighted
inequality) implies Wilf and has 0 failures through genus 24 plus 3002 adversarial cases, with equality
exactly at W = 0.

## Verified facts (PROVED on paper; see PROOFS.md)
- Identity CH; Corollary H (e·n ≥ c − (e−2)(m−1)/2, all S); Lemma A (TOP'' ⇒ Wilf).
- Top-layer elements are pairwise incomparable maximal Apéry elements; ℓ(u) ≤ q for u ∈ X_q.

## Open obligations / gaps
- G-TOP: prove TOP'' (the single remaining gap in this route).
- Novelty of Corollary H vs literature (not checked).
- Lean: CH and Lemma A not yet formalized (Lean agent building foundations).

## Experiments: see EXPERIMENTS.md (E0–E10), reproducible with `python3 src/<script> <genus>`.

## Three most promising active approaches
1. TOP'' via an exact identity for its slack (chain-type argument restricted to last two levels).
2. TOP'' by induction on depth / number of decomposable top elements (adding pseudo-Frobenius numbers
   f ∈ PF ∩ [c−m, c) moves a top element to the low part).
3. q = 2 case of TOP'' as an additive-combinatorics inequality (pattern-finding for the general proof);
   then e = 3 case via L-shaped Apéry sets.

## Next precise task
Derive the exact expression for slack(TOP'') analogous to CH (identify what nonnegative quantities it is a sum of),
by redoing the CH computation keeping all low-chain terms and E exactly, then test candidate decompositions.
