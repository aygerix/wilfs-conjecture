# Lattice-free cone sets with qO − t unbounded (2026-10-18)

The intermediate conjecture "qO ≤ t + O(1) on the lattice-free cone class" is FALSE.

Family (Q ≥ 4): q = (1, 1, Q),
- F = (Q+3, Q+1, Q, Q−1, …, 1)   (length Q+2)
- G = (Q+3, Q+1, Q−1, Q−2, …, 1) (length Q+1)
- h = (Q+1, Q+1, 2, 2, …, 2)     (length Q+2)
(Corrected 2026-10-18 after review: this note first gave |G| = Q+2 and h(0) = Q+2, but the code and the table use Q+1.)
- D = {x : x₂ < h(x₁), x₃ < min(F(x₁), G(x₂))} ∖ (q + ℕ³)

| Q | m | t | qO | rank(G_O) | #DS |
|---|---|---|----|-----------|-----|
| 4 | 53 | 10 | 9 | 2 | 3 |
| 6 | 101 | 14 | 15 | 4 | 5 |
| 8 | 165 | 18 | 21 | 6 | 7 |
| 10 | 245 | 22 | 27 | 8 | 9 |
| 12 | 341 | 26 | 33 | 10 | 11 |

In general t = 2Q + 2, qO = 3Q − 3 and #DS = Q − 1, so qO − t = Q − 5 is unbounded. qO ≤ 2t − 1 + 2|Y| still holds.

Mechanism (proved on paper, NOTEBOOK 2026-10-18 night 17 late). The doubly-same cells are x(z) = (1, 1, z). Their
partners u(z) = (0, 1, z) and u′(z) = (1, 0, z) have fixed peak tops P = top₃(u) and P′ = top₃(u′). The three qO edges
P–r₁(z), r₁(z)–r₂(z) and r₂(z)–P′ form a new P–P′ path for each level z, so every level adds one cycle.

These sets fail the tile constraints (`corner_anneal.valid(..., 'cone')` = Wall + Floor is False), so they are not
lattice tiles. Reproduce: `/usr/bin/python3 src/scratch/ds_family.py` from the project root.
