# Counterexample to CASEB-FLAT-S (chain link L7): a case-B lex tile of height 3 in the open regime

S = ⟨63, 239, 282, 295, 318, 333, 379, 386, 390, 400, 405, 407⟩

| invariant | value |
|---|---|
| multiplicity m | 63 |
| embedding dimension e | 12 (3e = 36 < m) |
| conductor c | 750 (> 4m = 252) |
| genus g | 581 |
| ℓ = c − g | 169 |
| W = eℓ − c | 1278 |
| lex factorization tile | height 3; one cubic cell 3e₁ (3·239 = 717 ∈ Ap(S,63)) |
| Dep, Σ_x(|supp x| − 1)⁺ | 42, 44 (case B, margin μ = 2) |
| Tile-CL V (min over phases) | 11 |
| MaxCL slack (min over phases) | 1663 |

- Residues δ = g mod 63 = (1,3,8,12,18,22,27,29,30,43,50). Together with 0 these form Haanpää's 12-element sum cover of
  ℤ/63 (J. Integer Seq. 7 (2004), Table).
- Reproduce (fejer ~/wilf/p35, scripts in src/scratch/p35):
  - `caseb_fixlift.py 63 1,3,8,12,18,22,27,29,30,43,50 6 600 1` chooses the tile and the lifts, maximizing μ (Gurobi);
  - `verify_s.py 63 239 …` checks c, g, e, W directly by membership DP, and the tile through ../p34/tile.build;
  - `tilechecks.py 63 239 …` gives the MaxCL and Tile-CL slacks at every phase.
