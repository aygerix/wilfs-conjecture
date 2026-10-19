# H1′ (Tile-CL on WRAP-MAX tiles) is false: the Sidon family

Source: codex P7 (src/scratch/gw/p7/P7_REPORT.md §§7–10). Independently re-checked by the lead with
src/scratch/wrapmax/sidon_lead_check.py (own code, direct evaluation of S and Λ_r from the definitions).

Construction. A = {a_0 < … < a_{k−1}} ⊂ [1, L] a Sidon set (all pair sums a_i + a_j, i ≤ j, distinct), Q = k(k+1)/2,
T = 3A ∖ A, t = |T|. For q ≥ 3L + 1 put m = 2q and core unit weights P_i = q − a_i. The core C ⊂ ℕ^k is the origin, the
k units, all Q pairs, and one cubic for each s ∈ T. Labels: units q − a_i, pairs m − (a_i + a_j) (unwrapped), cubics
q − s (wrapped once). They are distinct. Fill every missing nonzero label with a spike (a maximal unit). The result D
is a complete WRAP-MAX tile of height 3 with d = m − 1 − Q − t.

At θ = m − 2L (phase ρ = 2L): partial(U_θ) = 2Q + (2L − Q) = 2L + Q, every cubic has λ < θ, so
(S − Λ_r)/m = 2L + Q − t.

Explicit witness: k = 127, a_i = 1 + 254 i + (i² mod 127), L = 32006, Q = 8128, t = 72676, 2L + Q = 72140.
For q = 96019 (m = 192038, d = 111233): S = 30,848,386,779,896 < Λ_r = 30,848,489,712,264, (S − Λ_r)/m = −536.
The lead's check gives the same numbers, and −536 again at q = 150000 (m = 300000).

Semigroup realization at the conductor phase: generators m + P_i (core), 4m + j (missing j < θ), 3m + j (missing
j ≥ θ); c = 3m + θ = 704140, c mod m = θ. Wilf holds (eℓ − c = 946,230,902), and MaxCL holds at every phase:
S ≥ (d+1)·C(|N|, 2) − (m−1)·Σ_A(|y|−1), with |N| = 8254 and Σ_A(|y|−1) = 2t + 2.

Lesson: on WRAP-MAX tiles the incomplete cubic face can exceed the boundary (t > 2L + Q), and the excess is paid only
by non-maximal column residue mass Λ_r. Here the payer is mostly the spike-direction singleton columns over the units
and pairs. No pure-counting (boundary-only) inequality can prove MaxCL, even when only maximal cells wrap.
