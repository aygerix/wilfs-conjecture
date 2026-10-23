# FAILED.md — registry of failed proof mechanisms (Wilf)

> Current handoff: [STATE.md](STATE.md). Binding user rules: [DIRECTIVES.md](DIRECTIVES.md).

Purpose: before a new conjecture gets proof effort, state why none of the mechanisms below undermines it. Each entry:
statement, smallest/clearest counterexample, and what actually pays the deficit. Experiment IDs refer to EXPERIMENTS.md.

## Gate for new conjectures
1. **Necessity audit.** List the nonnegative terms of the exact identity that the conjecture discards. Show on data
   (ablation) that they are not the terms paying the deficit.
2. **Adversarial falsification.** Run annealers or optimizers (Gurobi on fejer) and explicit constructions aimed at
   the discarded structure. Also do a scaling estimate: B3/Sidon blocks, large e, concentrated carries, many wrapped
   pairs.
3. **Equality and scaling tests.** Cover W = 0 families, near-tight families, large m and unusual depth.
4. **Proof deadline.** If no structural mechanism appears quickly, record the conjecture as an observation. Spawn no
   stronger descendants.

## Pattern A — local positivity demanded of a piece of a globally nonnegative quantity
| Statement | Counterexample | Who pays |
|---|---|---|
| LASTWIN (Wilf on the last window) | ⟨55,109,159,319⟩, depth 26, slack −2 (E328) | earlier layers |
| DK (LASTWIN at depth four) | P18, m = 302, B = {36,37,38,41,42,43,45,51,53,63,65,71,75,97,170,171,175,176,178,183,185,186}: d4 = 35, L3 = 1, Q4 = −118, W = 3014 (E328) | Q3, almost all of it from σ_T = 2874 (unwrapped-triple incidence slack) |
| STAR (P18 depth four) | m = 47, B = {5,6,7,8,9,12,16,17}: STAR = −2, W = 205 (E331) | σ_T = 179 |
| J | ⟨21,23,33,35,38,39⟩, h = 2, J = −1 (E331) | — |
| PREFIX (P ≥ 0 in W = P + T) | 34 depth-four S of genus ≤ 30 with P < 0 (E330) | T ≥ 1.67(−P) |
| Per-direction / per-chain / base / reflection refinements of DEAD (PERB, CHAIN, BASE) | E322 | global collision count |
| Slot counts S2, S3, TFZ | sym construction at large e (E325) | — |
| COV ("every level-4 residue is a generator translate of S_3 ∩ [0,h)") | 138,918 of 642,239 depth-four S, genus ≤ 28; e.g. m = 18, c = 56 | DK is counting, not covering |
| HGI (per interval) | m = 23, B = {6,7,9,11} (E328) | — |
| HG1 at q = 3 | 258 failures, min −4 (E328) | — |
| L6, K5, K6, L3, L5 (pieces of CARRY-ID) | L6: ⟨13,18,20,24⟩; K5: ⟨17,19,26,28⟩ (E332) | other slack terms |
| O1 (overshoot incidences pay residual carried triples) | ⟨15,19,20,22⟩: N_over = 0 < q_res = 4 (E332) | non-overshoot unused incidences |
| O3 (swap incidences pay residual carried triples) | 1,389 failures at e = 5, m ≤ 26; e.g. m = 22, B = {9,10,12,13} (E335) | — |
| CT (r ↦ r + h injects residual carried triples into window tokens) | m = 12, B = {3,4,10}, h = 6: 5 + h = 11 = 3+4+4 is core (E335) | big tokens, extra tokens |
| Z8 (core elements ≤ y0 + extra tokens) | m = 62, B = {8,9,11,33,35,38,40,41,45,49,50,51,52}, slack −1 (E335) | B_L tokens, p_lo |
| Z5 (window tokens pay residual carried triples) | m = 11, B = {4,7,9,10}, h = 2 (E335) | carried pairs p_hi |
| LM degree condition, uniform discharging, per-largest-summand column split | E333; column split fails at m = 17, B = {2,9,11} | — |
| TOP-CR (TRUNC₃ by the crude window count: \|Top₂\| + \|G₀\| ≤ N_< + (m−c)⁺, PROOFS ID-TOP) (2026-10-21) | U ≠ T: 6 failures at \|A\| = 5 and 113 at \|A\| = 6; minimum −9 at A = {16,33,34,36,38,40}, m = 41 (c = 65, ℓ = 16, Top₂ = 7, N_< = 20, G₀ = 22). U = T: 790 / 6172 failures, min −14 (topid.c, E381) | \|Π_M\| (26) and the multiplicity Ov (30); W_e(U) = 47 |
| TOP-K1 (c > m: \|G₀\| ≤ \|Π_M\|) (2026-10-21) | U ≠ T: A = {15,32,34,36,41,43}, m = 44 (c = 70, G₀ = 24, Π_M = 23); U = T: 291 failures at \|A\| = 6, min −10 at A = {17,34,41,43,44,48}, m = 49 (E381) | K2 = N_< + Ov − \|Top₂\| (≥ 0 on every instance, min 10 at \|A\| = 6) |
| PAY2-H2 (Q5 residual: level-2 NE classes pay for themselves, Σ_{NE2} P ≥ e·\|NE2\|; PROOFS "PAY2: tile structure") (2026-10-21) | 1 failure at e = 6, 93 at e = 7, 2,903 at e = 8; minimum −7 at ⟨42,45,56,64,67,69,80⟩ (the RESID-PAY counterexample), −9 at e = 8 (⟨54,57,70,80,83,87,100,102⟩). Also H1 ("every NE2 tile element is a top in every direction") fails on 7,647 of 10,663 residual S at e = 7 (E382) | the EQ tops Peq and (e−1)δc (ID-NE); C* holds |
| A1 and C* as proof targets (Q5 residual: Δ₃ ≥ e·h_lo + h_hi; C* ⟹ A1 when j ≤ 1) (2026-10-21) | not refuted, but the gate fails at the scaling step: the worst ratio (e·h_lo + h_hi)/Δ₃ is 0.353, 0.413, 0.490, 0.633 at e = 5–8 (exhaustive), and 0.443 at e = 10 (annealing, h_lo = 14). Expected failure near e ≈ 10–12. Small μ makes h_lo ~ c(T)/μ while Δ₃ does not grow with it (E383) | ρ·ℓ(T) = (e − e(T))ℓ(T): the descent needs W(S) ≥ W(T), not PAY2, so a low NE element costs e(T) ≤ min(e, μ) (A1-eT, DESC) |
| P43 (Q5 residual: 3·prim + 4M₂ ≥ 6h, prim = missing cubes all of whose lower neighbours are in D; would imply D6 via 3|∇X| ≥ (e+1)|X|) (2026-10-21) | worst ratio 0.867, 0.783, 0.711 at e = 5, 6, 7; e.g. 3 S at e = 5, one at m = 20, A = [3,7,14,18] (E384) | the overlap structure of the level-2 shadows: |∇Miss₂| − ((e−3)/3)M₂ is often near (2e/3)M₂, not 4M₂/3 |
| T3 (Q5 residual: 3|G₃^T| + 4(|J₂| − b₂) ≥ 9b₃, G₃^T = minimal cubic generators of the T-leading ideal) (2026-10-21) | worst ratio 0.630, 0.653, 0.444 at e = 5, 6, 7 (e = 7: m = 42, A = [3,14,22,25,27,38]) (E384) | the shadow cubes of T-quadrics and of NE2 reps |
| WRAPV (Q5 residual: #{distinct values of ≤3-sums that are not class minima} ≥ h) (2026-10-21) | e = 7: m = 28, A = [3,8,11,16,19,24], 6 < 8 (E384) | multiplicity: the monomial count WRAPM survives |
| DIR (Q5 residual: Δ₃^{(i)} = 3m − Σ_s(h_s + (x_s)_i) ≥ h in every direction i with a_i ≠ μ) (2026-10-21) | e = 6: m = 40, A = [9,14,23,25,38], Δ₃^{(i)} = 1 < 2; 3 S at e = 7 (min 0.9h). Cannot scale: Σ_i Δ₃^{(i)}/h ≈ 6.5 against e − 2 directions | other directions |
| QA / P1 (Q5 residual: Qa := (e−μ)U_μ + eU′ − μh_lo^μ ≥ 0 for μ ≤ e; and P1 := e·\|U ∩ [0, c_T)\| − c_T = Qa + θ ≥ 0 for every μ. Either one with Qb := Δ₃ + (e−1)u′ − h_hi ≥ 0 would give Wilf, since W = P1 + Qb) (2026-10-21) | e = 11: m = 85, A = [3,46,47,50,52,58,59,65,76,83], c_T = 45, U ∩ [0, c_T) = {0,3,6,9}, P1 = Qa = −1 (W = 677, Δ₃ = 460, Qb = 678). Also e = 11, m = 86, A = [3,47,49,52,53,59,61,67,77,85]: P1 = −3, Qa = −4; e = 12, m = 92, A = [3,50,52,56,58,68,70,77,82,89,91]: P1 = −2, Qa = −3. Exhaustive e ≤ 8 had min Qa = 4 and min P1 = 5 (E385) | (e−1)u′: the U-elements above c_T. In family F0 (A = {μ} ∪ B, B ⊂ [c_T, m)) P1 = 4e − c_T, and Q5 allows c_T to grow about 4.5 per extra element of B. Also P1 = W_e(T) − e·h_lo needs a quantitative amount of T's Wilf slack, which induction does not supply. MU-LO survives on all three examples (ratio 0.10–0.12) |
| TR (Q5: (e+1)t ≤ (e−1)(r+1), t = #{σ_s ≥ 2m}, 2m + r = max σ; with ZT1 it would give Wilf via Identity SPLIT, with Δ₃ as pure slack) (2026-10-21) | Residual, e = 8: m = 54, A = [13,27,34,35,37,38,53], M₂′ = [1,5] (t = r = 5), (e+1)t − (e−1)(r+1) = 3 (Δ₃ = 158). Non-residual, e = 6: S = ⟨14,23,24,25,26,27⟩, t = r = 3, excess 1 (Δ₃ = 66, W = 90). Exhaustive e ≤ 7 residual has none (max excess 0) | Δ₃: the weakening TRΔ (E ≤ Δ₃) has max E/Δ₃ = 0.019 at e = 8. TR's tight shape is M₂′ = [1, r], where it reads r ≤ (e−1)/2 |
| μ-RUN injection (Q5 residual: every class reaches a class with σ < m in at most e − 1 backward μ-steps; this would inject the classes into Z × [0, e−1] and give e·z ≥ m) (2026-10-21) | e = 5: m = 18, A = [3,11,15,17]. A μ-cycle mod m contains no class with σ < m, so the walk never ends. At e = 7 the excess K − (e−1) reaches 23, and 1,210 / 10,663 residual S have such a cycle (murun.py) | Steps by the other elements of A. The pair count (Identity PAIR, ZT1) uses all of Z × A |
| N3 / 2L₃ (Q5 residual: Δ₃ ≥ 2n₃, or Δ₃ ≥ 2L₃ with L₃ = #{level 3, σ ≥ m}; crude sufficient conditions for Q3T, since \|Q3\| + t ≤ 2\|Q3\| ≤ 2L₃ ≤ 2n₃) (2026-10-21) | e = 6: m = 40, A = [9,14,23,25,38]: Δ₃ = 36, n₃ = 21, L₃ = 20 (2n₃ = 42, 2L₃ = 40), while \|Q3\| + t is small. Exhaustive e = 5 has max 2n₃/Δ₃ = 0.47 | Only cubes with all pairwise sums ≥ m (Q3) need paying; low-pair cubes are free in SPLIT-Q3 |
| WRAPPAY / WRAP2 (Q5 residual: the missing wrap slots of large standard squares, i.e. (x, l) with σ(x) + a_l ≥ 2m and x + e_l ∉ D weighted by x_l + 1, are ≥ 2t + \|Q1′\|, or ≥ 2t) (2026-10-21) | WRAPPAY: 3 S at e = 7 (min −4 at m = 34, A = [3,15,18,21,22,25]: 6 missing slots against 2t + \|Q1′\| = 10) and 38 S at e = 8. WRAP2: e = 7, m = 34, A = [3,15,18,27,30,31] (17 against 18); e = 8, m = 59, A = [3,9,30,45,48,53,54] (24 against 30) | 4M₂: missing large squares lower the weights. The unweighted count K2 (K₂ ≥ 2t) survives with equality |
| TGT (Q5 residual: each column top (x, i) of D pays the class of σ(x) + a_i, and every NE class t receives ≥ e if τ_t < c(T), else ≥ 1) (2026-10-21) | 49 / 72 NE classes (21 / 22 S) at e = 5, 908 / 1,477 (407 / 454) at e = 6, 21,059 / 33,952 (9,693 / 10,663) at e = 7. It fails even summed over the NE classes of one S (min −12 at ⟨22,27,34,41,43⟩, −23, −45) (E383) | the tops landing in EQ classes, mostly wraps (Peq) |
| PAY2-B1 (δc ≥ Σ_{NE3} j: the conductor pays e−1 per level-3 NE class) (2026-10-21) | 27 failures at e = 6, 1,155 at e = 7, 39,827 at e = 8; minimum −4 at ⟨38,43,60,61,62,67,70⟩, −7 at e = 8 (⟨52,61,69,86,92,93,94,100⟩). NE3 classes below max τ exist (4,189 of 17,653 at e = 7) (E382) | Peq + \|NE2\| (B2 holds, minimum 53 at e = 7) |

## Pattern B — strengthening beyond what is needed
| Statement | Counterexample |
|---|---|
| LAYER(j) for j ≥ 4 | LAYER(4): ⟨35,54,55⟩, slack −1; LAYER(7): ⟨52,80,81⟩, slack −3 |
| LAYER_j(n) for window length n ≠ m | genus ≤ 18, failures for j = 1, 2, 3 (E332) |
| CHAIN-WILF | ⟨23,54..61⟩ at q = 5, ratio → 0.70 (E284) |
| WQ | 0 failures to genus 30, false beyond (STATE) |
| XDEAD (conductor-free DEAD) | PROOFS "DEAD" section |
| Q3 ≥ 4h − (k+4) | ⟨27,28,32,35⟩, Q3 = 3 (E332) |
| ALL-BUT-ONE (every S, lex tile M̂ ⊆ ℕ^N, N = e − 1): B^i := Σ_{β∈M̂}(c + m − 1 − φ(end_i β)) ≥ m(m−1)/2 for every direction i except at most one; equivalently γ_i·Σ_{w∈Ap} α_i(w) ≤ m·ℓ. Sum form = CH′ = Wilf. Right-primitive directions always satisfy it (proved) | ⟨7,11,12,20⟩ (c = 18): B/h = 0.571, 0.381, 1.714; at depth 5: ⟨34,38,42,43,71,73⟩ (c = 139): B/h = 2.49, 0.907, 0.927, 2.417, 2.652. Even pairs fail (0.571 + 0.381 < 1). Random census: 0 failures on 3,179 S with c > 4m; the annealer found them in minutes (E345) |

| T1 (every S): Σ_y (j_y − c_y) ≤ ρ + r, i.e. E + r ≥ P (the whole ID-q pool); also T1′ (holes below ρ dropped), T0 (≤ ρ), and the combinatorial version for arbitrary injective multiset ideals | ⟨66,67,71,72,98,103,128⟩: c = 326, q = 5, ρ = 4, r = 0, J − C = 6, T1 = −2; also ⟨61,62,63,67,88,89,112⟩ (−1) and ⟨64,65,69,75,95,100⟩ (q = 6, −1). Two codes agree (E340). T0 already fails at ⟨14,22,23⟩₅₆ (J − C = 1, ρ = 0). T1 had 0 failures and min slack 0 on all of genus ≤ 30, e = 3 exhaustive, e = 4 random and the negative-Eliahou families: tight statements need annealing, not census | the pool P (unused incidences); E + r = 451 there |

| (B) / P1 (every S with r ≥ 1): E + (k − q) ≥ 0, i.e. Wilf with r replaced by min(r, 1); also E + a ≥ 0 (a = #nonzero left Apéry residues). This would have reduced Wilf to the case r = 0 | ⟨798, 1205, 1206, 1209, 1218, 1237, 1276, 1329⟩ ∪ [3192, ∞): r = 678, E = −56, k − q = 49, (B) = −7 (E343). Family Γ ⊂ (3m/2, 5m/3), c = 4m, collision-free: E = −(n³−n)/6 while k − q = 3n + C(n+1, 2); fails for all n ≥ 7. It survived 46,862 negative-Eliahou Delgado truncations (slack ×8) and P18 annealing: small-e families never reach it | many right primitives (r ≥ n/3 is needed; the difference body gives n(n²−1)/3) |

| MAJ(v) (every S, 1 ≤ v ≤ m): the ray incidences ending in the top v-slice number at most (N−1)v + m (a Hall/layer-cake strengthening of CH′) | ⟨5,11,12⟩ (c = 20), ⟨12,13,59⟩ (c = 107), ⟨4,7,13⟩ (c = 11): deficit 1 against early slack 16, 427, 3 (E345). Exact form: mW = Σ_v[(N−1)v + m − cnt_v] + early |
| TOP (every S): Λ ≤ G (ceiling gains alone pay the top loss); also TOPP (the same, given P̃ > 0) and GT (Λ ≤ G + max(R_gen,0)(k−q)) | TOP: ⟨37,69,70⟩₂₄₄, r = 22, P̃ = 0, slack −8.9 (P0 class: r(k−q) pays). TOPP: ⟨41,72,73,75⟩₁₈₅, P̃ = 2.85, slack −8.6. GT: ⟨31,55,56,57⟩₁₄₁, R_gen = −6, P̃ = 9.2 pays (E345). TOP restricted to leaves (r = 0) survives: Conjecture TOP0 |
| LEAF-MIN: W(S) ≥ W(⟨L(S)⟩) (truncations dominate their leaf) | ⟨11,13,18,25,36,43⟩ truncated at c = 20, 21, 22: W = 20, 15, 14 < W(leaf) = 34 (E345) |
| SUBADD-TOP for general down-sets (any down-set D with maximal set Z, any subadditive ε ≥ 0 with ε(0) = 0): Σ_Z(\|y\|−1)ε(y) ≤ (n+1)Σ_{D∖Z}ε | 2D, size 11, Z = {(0,4),(1,2),(2,1),(3,0)}: LP value 0.23 > 0. 3D: first failures at size 12 with \|Z\| = 5. No failure seen with \|Z\| ≤ n+1 (E345). The tile structure must enter for large type |
| HALL-TOP at threshold c for ρ > 0 (box-local transport for TOP0); LOAD (uniform box shares) | 304/4,548 leaves with ρ > 0; e.g. ⟨10,11,17,18⟩ (c = 27, ρ = 3), shortfall 20. LOAD: ⟨12,13,14,19⟩ (c = 36), excess 2/3. Box pairing loses when h(y) + ρ ≥ m. At threshold qm (ρ′ = 0), HALL-TOP holds on all tested leaves |

| REARR (shape-only TM; = R-TOP, already FALSE in PROOFS "Tile-TOP''"; re-found 2026-10-20): residues of maximal elements replaced by the rearrangement bound Σ_k w_(k)(m−k), even restricted to m > 3e | ⟨19,33,35,39,42,44⟩ (c = 70): ratio 1.064; ⟨16,28,29,33⟩: 1.05; ⟨49,53,56,60⟩: 1.045. TM itself holds there (ratios 0.96, 0.94, 0.87). Random census: 0 failures for m ≥ 3e (2,408 S), 12/776 for m < 3e; the annealer broke it at once (E346) |
| RISE (TM sufficient form: the total fiber-rise into maximal elements is ≤ C(m,2)) | all tiles, n = 2 (m ≤ 12) and n = 3 (m ≤ 8): 24 and 198 failures, deficit ≤ 4 (E346). It drops Σ_β (n − \|I(β)\|)ε(β) |
| PSHIFT (P̂′ ≥ Nρ at threshold qm, so that the λ = 0 case of TM would suffice) | ⟨11,13,14,16,18⟩ (c = 24, ρ = 9): P̂′ = 22.5 < 36; 41/2,165 (E346) |
| INJ-SUBADD (= the FALSE "partial tiles" extension of MaxCL, PROOFS; re-found 2026-10-20): TM-type inequality on arbitrary down-sets E with an injective mod-linear ε, m ≥ \|E\| (Hall's condition for the box transport) | E = Δ_3 ⊆ ℕ², m = 16, b = (9,10), λ = 0: slack −16 (E346). It holds only inside tiles, which in 2D have ≤ 2 maximal elements |
| WINDOW (q = 5, height ≤ 3, level 1): e·|X| ≥ m + r + 1, X = {s : σ_s ≤ m + r} (2026-10-21; a strengthening of E3 ≤ 0) | ⟨19,32,33,35,37⟩: r = 6, X = {0,13,14,16,18}, e|X| = 25 < 26 (independent DP check, winchk.py); also one S at m = 13, d = 3 (E378). E3 ≤ 0 holds there (e(|X|+|Y|) = 30): the degree-4 left elements Y are needed |
| RD′ (every S): W(S) ≥ e·ℓ(T) − c(T), T = ⟨m, g_i mod m⟩ (2026-10-21) | ⟨7,11,13,23⟩: W = 4, eℓ_T − c_T = 6 (genus 14; 9 failures at genus ≤ 25, min −6 at ⟨11,17,19,29,31,32,35,37⟩) (E379). RD itself (with e(T)) survives: the (e − e_T)ℓ_T term pays |
| Local level drops (every S): W(S) ≥ W(S′), S′ = generator g replaced by g − m (2026-10-21) | low drop: ⟨5,6,7,8,9⟩, 8 → 3 (W = 0 → 1); high drop: ⟨15,18,…,29,31,32⟩, 31 → 16 (W = 12 → 24) (rdloc, E380). Only the simultaneous reduction to T is monotone in the data |
| Δ′ ≥ 0 under U = T (every S; ID-U) | 7 S at genus ≤ 24, min Δ′ = −6 (E379); the residue semigroup has e(T) = 2 there and RD holds |
| Split of RD on the residual U ≠ T into Δ′ ≥ 0 and MONO* W_e(U) ≥ W(T) (every S, max-κ down-set) | Δ′ < 0 on ≈ 2% of the residual (genus 25: 2830 of 127224, min −56); MONO* fails at ⟨8,14,23,29⟩ (genus 26: W_e(U) = 9 < W(T) = 10, Δ′ = 37, W = 46) (rdexh2, E379). RD = Δ′ + W_e(U) − W(T) + … survives: each half pays for the other |
| MONO (fixed e): W_e(U_k) ≥ W_e(T) for truncated sumsets (2026-10-21) | A = {4,9,10}, m = 13, k = 3: 15 < 16 (trunc.c); inside the q = 5 residual: A = {4,11,15,22,27}, m = 28, deficit 18 (resid.py, E380). The e(T)-version MONO* survives there |
| MONO*-Q5: on the q = 5, height ≤ 3, level-1 residual U ≠ T, W_e(U) ≥ W(T) (2026-10-21) | ⟨34,42,53,54,56,57,67⟩ (e = 7, m = 34, r = 3): T∖U = {32} = {4·8}, c_U = c_T = 38, ℓ_U = 16, ℓ_T = 17, e(T) = 7, W_e(U) = 74 < W(T) = 81 (q5d2 mode 1 and independent monochk.py). E3 ≤ 0 still holds (W_e(U) = 74 ≥ 0): the residual needs TRUNC₃ directly, not a route through W(T). Side claim also false: T∖U ⊂ [0, m) (⟨20,23,27,34,38⟩ has 22 ∈ T∖U in the conductor class) |
| RESID-PAY: on the q = 5, height ≤ 3, level-1 residual, Δ₃ ≥ e·|T∖U| (2026-10-21) | ⟨42,45,56,64,67,69,80⟩ (e = 7, m = 42, r = 4, A = {3,14,22,25,27,38}, T = ⟨3,14,22⟩, e(T) = 3): Δ₃ = 98 < e·h = 105 (h = 15, T∖U = {12,15,18,21,23,24,26,29,32,34,35,37,40,43,46}). The 1 failure among 10,663 residual S at e = 7 (q5d3; independent monochk.py). Who pays: (e−1)δc = 162 (c_U = 47, c_T = 20) and (e − e_T)ℓ_T = 36; W(S) − W(T) = 191, TRUNC₃ slack W_e(U) = 100. Complementary to MONO*-Q5 (δc = 0, e = e_T, h = 1, paid by Δ₃ = 115): no single payer dominates |

## Pattern D — a structure classification read off small d that fails once extremal additive objects exist
| Statement | Counterexample | Who pays |
|---|---|---|
| CASEB-FLAT (every lattice tile with Dep < Σsupp has height ≤ 2) and its needed form CASEB-FLAT-S = chain link L7 (the lex factorization tile of an open-regime S in case B has height ≤ 2) | Lattice: Haanpää's sum cover of ℤ/63, δ = (1,3,8,12,18,22,27,29,30,43,50), best flat μ = 16, best tile with a cubic μ = 4. Semigroup (open regime): ⟨63,239,282,295,318,333,379,386,390,400,405,407⟩, c = 750, e = 12; lex tile of height 3 (3·239 = 717 ∈ Ap), Dep = 42 < Σsupp = 44 (μ = 2), W = 1278 (E353; verified by two independent computations). True for every height-≤3 tile with d ≤ 5 (exhaustive, E352), but d = 11 has the anomalously large cover f(11,2) = 63 | Tile-CL: V ≥ 11 at every phase; MaxCL slack ≥ 1663 at every phase. So TCL-DICHOTOMY survives, and the chain's open link becomes TCL-DICHOTOMY-S |
| H3-CASEA by difference bodies (DB_U inequalities exclude height-3 case-B shapes) | d = 3: 18 down-sets (Δ₂ plus 6 cubics, m = 16) satisfy every DB_U with U ⊆ Δ₂, yet none is a tile (E352) | the arithmetic of ℤ/m (character sums) |

## Pattern C — a relaxation that removes the structure doing the work
| Statement | Counterexample |
|---|---|
| ASYM-RT (RT(q) ≥ q·lead − K∞ with K∞ ≤ q·lead, i.e. the single dual optimal at q → ∞ certifies RT ≥ 0 at q ≥ 5) | ⟨13,17,27,29⟩ (c = 63, q = 5, open regime): lead 5.5, K∞ 34.5, asymptote −7 while RT = 9 via another dual; K∞/lead reaches 6.54 at ⟨14,17,69⟩ (E366, 2026-10-20) |
| CR-TILE (CR_DEP on every lattice tile: Σ_i i·ω_(i) + m·Dep ≥ (d−1)C(m,2); shape-only rearrangement of DEP-CARRY) | ⟨19,39,41,50,52,53⟩ (c = 88, open regime): unique height-2 tile in ℕ⁵, slack −4 (E349). Structural: the full height-h simplex needs d·C(d+h−1,h−1) ≤ C(d+h,h) − 1, false for h ≥ 2 |
| PD+ (pair/Hamming form, ⇒ CR_DEP) | same tile, slack −10 (E349) |
| ID (cyclic label-interval discrepancy Σ_J(d − ω̃) ≤ (m−1)/2 + Dep, sufficient for DEP-ALL) | 10/3,000 S; the same tile (16 > 13) (E349) |
| KAPPA-DEP (κ₀ ≤ Dep, i.e. column inversions not needed) | ⟨19,35,37,43,45,61⟩ (c = 104, open regime, the δ ↦ −δ mirror of the CR-TILE counterexample): κ₀ = 5 > Dep = 4 (E349). Forced by the mirror identity κ₀(δ) + κ₀(−δ) = Σ(\|supp\| − 1). Slack 0 also at height 3 (⟨25,38,40,53⟩, ⟨16,44,59,63⟩) |
| SC1′ (Hasse-edge bound for Dep), PD (per-direction split of CR_DEP) | SC1′: 156/3,000 S, worst in d = 2; PD: fails at the simplex (E349) |
| TB4 with only the half window [h, 3h′) | E314 |
| RANK (replace the depth δ(z) of a ray end by its rank in the φ-order) | 2,586 of 2,738 random S fail, e.g. ⟨12,17,19,20⟩ (c = 48), −15 (E345). The gaps between φ-values matter |
| Z12 without any window covering | m = 47, B = {10,12,13}, h = 20, slack −2 (E335) |
| Small-part inequality (core regime) | STATE 0f |
| UCG (every S, c > 4m): Σ_{y∈Y}(\|y\| − 1) ≤ R*(k − q) + P̃ with R* = max(R_gen, min(r, 1)); it drops G, ρR*/m and the θ-weights of Λ from the ray identity | two-generated S with r = 0 and W = 0: ⟨8,9⟩ (c = 56, slack −6), ⟨9,10⟩ (c = 72, −7), ⟨7,8⟩ (−5); also ⟨7,9,24⟩₃₀ (W = 6, −1/7) and the tile ⟨16,27,28,31⟩₇₈ (r = 0, −23/8). Annealers found these in minutes (E345). Who pays: the ceiling gains G pay all of Λ in the two-generated case |
| SPLIT-CERT (2026-10-20: every S with e ≥ 3 has a split certificate — Theorem CERT with μ ≥ 0 and worst-case τ only, no level information) | ⟨37,75,78,80,88,89⟩ (residues {1,4,6,14,15}, a postage-stamp B₃ basis mod 37; c = 222 = 6m, e = 6, W = 102): best Γ = −1, also with ternary splits; likewise ⟨37,112,115,117,162,163⟩ and the {1,6,9,14,15} mod 40 family (E360). Structural: at height ≤ 3 every split has ≥ k − 1 unit parts, so Γ ≤ e² − m; certificates need m ≤ e² + ρ/q. Who pays: the unit levels μ_b (UNIT-CERT holds on all of them) |

## Pattern E — reductions that are only conditional
| Statement | Counterexample |
|---|---|
| Core transfer W(S) ≥ W(⟨A⟩ ∪ [c, ∞)), A = generators in [m, 2m) (any depth) | ⟨8,10,12,14,17⟩ (q = 3, −22); ⟨8,10,12,14,21⟩ (q = 4, −28); every depth 3…15 at genus ≤ 24 (E336). The external depth-four reduction needs W₀(S) < 0 and residual hypotheses |

## Pattern D — false side claims
- "Every S with e ≤ 3 has unique Apéry factorizations." FALSE: in ⟨5,6,9⟩, 18 = 6+6+6 = 9+9 ∈ Ap(S,5), Λ − O = 2.
  Corrected in PROOFS.md.
- "In the open regime c(U₃) > 4·min A, TRUNC₃ holds with ratio e·ℓ/c ≥ 1.44" (an observation from |A| = 4, 5;
  2026-10-21). FALSE as a uniform bound. Family F_T (PROOFS): A = {μ, 3μ, 5μ} ∪ [5μ+1, 6μ−2], m = 6μ − 1 has
  U₃ = T = ⟨μ, 5μ+1, …, 6μ−1⟩ and ratio (μ+2)/μ → 1 (1.333 at |A| = 7, 1.286 at |A| = 8). The 1.44 was a small-|A|
  effect: the padding needs about 2 elements, so the family starts at |A| = 5 with ratio 1.5.

## Live conjectures — audit status (P18 depth four unless stated)
**2026-10-20: depth four (c ≤ 4m) is settled by the external Lean proof, kernel-checked by us (LITERATURE).** Every
depth-four entry below (TB4, TB4-LOC, LM, K1, K7, L1, L2, Z1, Z12, SIG) is MOOT. Keep them only as records. DEAD, DOWN
and MD are statements about every S and remain observations.
| Conjecture | Discards | Status |
|---|---|---|
| DEAD (all S) | nothing; it is a strengthening of Wilf by Λ − O | observation; 0 failures, genus ≤ 34 |
| DOWN, MD | strengthen DEAD | observations only; no descendants |
| TB4, TB4-LOC | 2δ2, slA (TB4 uses E1 only) | observation |
| LM, K1, K7 | 2δ2 (LM), more (K7) | observations; no structural mechanism |
| L1, L2 | sl_B, defU (L1) | observations |
| Z1, Z12 (2h ≤ m) | p_lo, N4, 2δ2, incU, incC, defU | observations. Scaling estimate: a B3-Sidon block in (h/2, 2h/3) of size d ≳ 13–26, with carried pairs covering the half window, should break them at e ≈ 80–300, where incU pays. Not proof targets |
| SIG := Q4 + σ_T ≥ 0 | 3(P_w − p) + 2(P_u − u2) + P_w | under falsification (E335): necessity ablation shows σ_T is the essential payer at e = 4 |
| ANCHOR (every S): DEF ≤ ρ + EXC + U_top + r | the pool of weight ≥ 2 and r(\|L\| − q − 1) | gate steps 1–3 passed (E337, E338); proof attempt open. Not a piece of a positive quantity demanded locally: it is the full deficit of the exact identity ID-q against all weight-1 credits |
| CORE₁ (every S): E + r ≥ 0 | r(\|L\| − q − 1) only | 0 failures (E338), extremal families have growing margins |
| WR1 (every S): J − C ≤ ρ + r + P_W, with P_W = Σ over wrapped x of (q − λ_x)u(x) | the pool of unwrapped positions | 0 failures: exhaustive q = 5, 6, m ≤ 20, strips (92,257 models), random; survives the T1 counterexamples (margins 130–182). Annealers (E340, E343): best slack 3, 3, 6 after ~3,000 restarts each; no failure |

## Corrections log
- 2026-10-20: I first wrote "CORE₁ is implied by Wilf". It is the reverse: CORE₁ implies Wilf (W = E + r(|L| − q)).
  Corrected in PROOFS/STATE the same day.
| T2 (every S): J − C ≤ ρ + r + Σ_{wrapped x, λ_x = q−1} u(x) | the pool except wrapped top-1 positions | 0 failures: genus ≤ 30, e = 3 exhaustive. Annealers q = 5–7 best slack 1, 3, 1 (running). In the collision-free regular regime P = 0, so T2 = WR1 = ANCHOR = CORE₁ there. CORE₁ survives the dense n = 2 packings up to h = 14 (E343) |


### 2026-10-22: retaining only upper-side UA3 rows is insufficient (E390)
Claim: fixing true generator levels and retaining only A_p y <= q+up_p on tight pairs always gives a
nonnegative Wilf bound in c>4m,3e<m. FALSE: <20,21,22>, c=200,g=100,e=3,q=10,rho=0,W=100;
the exact upper-side closure has sum b=60 and bound -20. Full UA3 is 100, exactly rationally certified.
The dropped lower-side split inequalities pay the deficit. This is distinct from the older one-sided R
certificate, which kept lower-side rows and dropped upper-side rows. The DP remains a valid lower bound,
and B<0 is a necessary condition for a Wilf counterexample; its positivity is not a theorem.

### Matching pays at least half the total upper-closure loss (FALSE, 2026-10-22; E396)

The proposed shortcut M>=sum_s(mu_s-b_s) fails even for genuine S in c>4m,3e<m.
For S=<34,42,53,54,56,57,67>, c140,g93,e7,W189,B133, the loss sum is8 but M=0.
The vector b already satisfies every UA3 row, with certified UA3=B=133. Some loss is on maximal Apéry cells;
other loss cells occur as parents but still produce no positive repair demand. Thus lost actual level does
not by itself create compulsory repair payment. A second example <20,25,61,102,143,184> has loss22,M10.
This kills the shortcut, not the proved bound W>=B+e ceil(M/2) or its still-unproved universal positivity.

### An optimal repair cover can always be bounded by actual repair (FALSE, E399)

For <66,67,71,72,98,103,128>, c326,g215,e7,W451,B115 and sum(mu-b)=48. The unrestricted pair-cover
optimum is M/2=41, but the optimum with 0<=t<=mu-b is42. Two exact assignments plus an independent
bounded primal/dual audit verify the strict gap. Thus no unrestricted optimum admits nonnegative unpaid
loss at every cell. The separate capped-cover bound is valid for W; it is not automatically a UA3 bound.

### Negative upper baseline forces W>=c/2 (FALSE, E400)

Even on e>=4,c>4m,3e<m, the proposed full-Wilf dichotomy B>=0 or2W>=c fails:
<60,67,71,121> has c480,g301,e4,W236,B-164, with matching M156 and bound148. Full UA3=180 is exactly
certified. Continuing the B<0 actual-W/c descent gives <60,71,121,143>, c655,W237,B-111,M150,bound189.
This disproves the dichotomy, not Wilf or universal matching positivity. Do not substitute a smaller guessed
constant as a research plan. Local search supplies no global minimum.
