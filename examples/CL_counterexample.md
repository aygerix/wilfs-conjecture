# Counterexample to the Carry Lemma CL and to Tile-CL (found 2026-10-17, E47)

This is a counterexample to the conjectured strengthening CL. It is **not** a counterexample to Wilf: Wilf holds here with W = 35.

## The semigroup
S = ⟨14, 22, 23, 57, 61, 62, 63⟩. All 7 generators are minimal.

| Invariant | Value |
|---|---|
| m | 14 |
| e | 7 (d = 6) |
| c | 56 (F = 55) |
| g | 43 |
| ℓ = c − g | 13 |
| W = e·ℓ − c | 7·13 − 56 = 35 |

This is the "W0 < 0" example ⟨14,22,23⟩ ∪ [56, ∞) of Eliahou (LITERATURE #13 context).

Ap(S,14) = {0, 22, 23, 44, 45, 46, 57, 61, 62, 63, 66, 67, 68, 69}, and M = max Ap = 69 = F + m.

Every Apéry element has a unique factorization over P' = {22,23,57,61,62,63}. So the factorization down-set D is the same for every monomial order:
- D = Δ_3 ∪ {e_3, e_4, e_5, e_6}.
- Δ_3 = {(x_1, x_2) : x_1 + x_2 ≤ 3} in directions (22, 23).
- e_3, …, e_6 are four "spike" cells, one each for 57, 61, 62, 63.
- p mod 14 = (8, 9, 1, 5, 6, 7).

## Failure of CL
CL requires Σ_a Σ_{a-columns C} |C|·((M − w(top C)) mod m) ≥ (d−1)·m(m−1)/2.

Here the LHS is 441 and the target is 5·91 = 455. **CL fails**, with slack (441 − 455)/14 = −1.

The exact identity m·W = m·depth + (LHS − target) checks out: 14·35 = 14·36 + (441 − 455).

The depth part 36 comes entirely from singleton spike-direction columns at the low elements 22, 23, 44, 45, 46:
- ⌊(69 − w)/14⌋ = 3, 3, 1, 1, 1 for these five elements, which sums to 9.
- There are 4 spike directions, so the depth part is 9·4 = 36.

## Failure of Tile-CL (all residues s)
The slack vector for s = 0, …, 13 is [5, 4, 6, 8, 10, 9, 8, 7, 9, 11, 8, 5, 2, −1]. Its minimum is −1, at s = 13 = M mod m, the CL reference residue.

## Mechanism: spikes
Take a spike direction a, i.e. one whose only cells are 0 and e_a. It contributes exactly m·[s < p̂_a] − p̂_a to m·slack(s); all its other columns are singletons.

So any down-set core C with φ injective becomes a tile once spikes are added on the residues outside φ(C). This makes "CL for injective φ" (FALSE, E17) relevant to tiles.

Search over cores of dimension ≤ 2 (src/scratch/spikes.py):
- No spiky tile fails for m ≤ 13.
- The first failure is at m = 14: core Δ_3, p = (5,6), spikes (7,8,9,13), slack[0] = 14 > m − 1. This is the dual (p ↦ −p) of the tile above.

## Reproduce
```bash
python3 src/scratch/clverify.py
```
This runs an independent brute-force check: membership, c, g, e, Apéry set, all factorizations, and cl_value for three orders.

```bash
python3 src/exp_cl_adv.py 1 3000 100
```
This runs the adversarial and random suite. It finds 9 Tile-CL failures, the smallest being this one.
