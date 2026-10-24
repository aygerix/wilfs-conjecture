# FAILED.md — registry of failed proof mechanisms (Wilf)

**E447, charge each scalar death to its first vanishing odd edge — map NOT injective
(2026-10-23).** On the already recorded13/15/47 example, n is in H_n for4<=n<=12,
but all nine source words(t^15)^n first vanish at45->60 by15. Parent45 survives since
32 is not in S;60 dies since60-13=47. This is an odd-parent/even-target edge, so it is
also absent from E445's even-parent reserve. A kernel edge can have many scalar
descendants. Stop this map and kernel-count-only payment; no total-kernel dimension
inequality or weighted global descendant allocation is refuted. PROOFS E447 contains
the hand proof. No new computation or three-generator target.

> Current handoff: [STATE.md](STATE.md). Binding user rules: [DIRECTIVES.md](DIRECTIVES.md).

Purpose: before a new conjecture gets proof effort, state why none of the mechanisms below undermines it. Each entry:
statement, smallest/clearest counterexample, and what actually pays the deficit. Experiment IDs refer to EXPERIMENTS.md.

**E440, monotone parity payer — FALSE (2026-10-23).** W(S)>=2W(S/2) fails even in
c>4m,3e<m and with gcd(P minus {p})=1 for every primitive p. Take S=<17,18,21,37>:
m17,e4,c84,g48,ell36,W60. Its quotient T=<9,17,19,21,29> has c42,g24,ell18,e5,W48,
so60<96. With S=2T union(a+2I), a17, normalized ideal generators0/2/10, there are
r3 odd primitives and q4 lost doubled quotient primitives. The PAR-W correction is
2(r-q)ellT=-36; its filled-gap and conductor terms vanish (v=b8,t0). Thus q<=r is
also false. The earlier reducible S=<17,18,21,33> gives W65, quotient W72 and correction-79.
This refutes the standalone nonnegative correction, NOT conditional transfer of Wilf
nonnegativity or Wilf. WT's actual surplus must remain in any such proof. Both examples
were independently reconstructed by C and membership DP. Stop further variants; full
proof, scope and data are in PROOFS/EXPERIMENTS E439–E440 and STATE's sole inventory.

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

### The single largest Apéry divisor ideal has size at least m/e (FALSE, E404)

For every n>=7 set m=2n and S=<m,m+1,m+2,nm-1>. The last generator is the Frobenius number of
<m,m+1,m+2>; adjoining it lowers only the largest Apéry representative. It is now itself the largest
Apéry element and is primitive, so its divisor ideal is exactly {0,nm-1}, of size2, while m/e=n/2 grows.
These S have c>4m,3e<m. PROOFS gives exact Apéry/conductor/genus formulas. Thus no uniform positive
fraction of the residues is controlled by that SINGLE top ideal. This does not disprove top-divisor
rigidity; it requires a counting proof to retain other maximal elements and the full residue bijection.

### Every full capped unpaid coordinate is at most one (FALSE, E406)

S=<153,166,170,317,325,474,617,766,921,925,1080> has c1683,g1013,e11,W5687.
An exactly verified feasible capped unpaid vector has x_23=2 (its actual cap delta_23 is2),
thirty other coordinates equal1 and all others0. Thus max x_23=2, with a bound-only dual certificate.
The Apéry element w_23=1400 is maximal: its four incoming tight pairs all have alpha0,kappa1,
and it has no outgoing tight pair. The full vector and proof are recorded in PROOFS/E406 and
src/scratch/p39/data/capped_core_probe.jsonl.gz. Five tested coordinates on the older saved examples
had optimum1; this stronger adversarial example shows those checks cannot justify unit weights.
This refutes a certificate simplification, not Wilf; weighted residual mass must be retained.

### Factorization excess pays every unpaid unit (FALSE, E413)

The candidate E>=e*m*(sum U-ceil(M_U/2)), with E the recorded CH factorization-excess term,
fails at S=<13,17,27,29>: c63,g37,e4,W41,unique Apéry factorizations,E0,U2=1,M_U0.
The right side is52. Its equality class is singleton, so equality completion does not change this.
Independent coin-change factor counts and primitive-multiple subtraction verify uniqueness/E0 and
the CH identity. The saved <146,147,155,185> likewise has E0 and residual42. This is not a Wilf
counterexample. Global charging must also use primitive-chain boundary deficits and retain the
discrete correction; loss cannot be identified with factorization redundancy alone.

### E418: sourcewise nonnegative actual-tight dual contributions after dropping allowance costs — FALSE

In a,q coordinates, discard every nonzero-RHS typed certificate side, and orient each actual tight
row with RHS tau toward pi*tau>=0. This proposed sourcewise-positive dual rule fails on the genuine
profile of <19,26,27,48> (m19,e4,c90,W22): Q1 and A=Y indicator{7,8,10} is an exact negative ray of
that weakened model, slope-3. It violates original actual equalities, e.g.7+7->14; eight steps from
the seed give diagnostic objective-2 but do NOT give a semigroup. The original full joint and free-side
joint minima are both22. The65case provides a second diagnostic ray. Do not call either a Wilf or
full-certificate counterexample. Data/checking: PROOFS E418 and p39/data/allowance_source_probe.jsonl.gz.
Signed tight-row RHS costs depend on parametrization; E417 primitive coordinates put actual trades
at RHS0. Discontinue this sourcewise a,q sign restriction rather than patching its examples.

### E421: unit unpaid mass even in fully extendible Apéry cells — FALSE over R and Z

The proposed repair shortcut x_s<=1 for cells extendible by every primitive OTHER THAN the multiplicity
fails at S=<104,420,453,509>, m104,e4,c4784,g2647,W3764. The cell w81=2265=5*453 has all three extensions
2685,2718,2774 in Apéry. Its exact real capped maximum is7/3. A separate integer feasible witness has
x81=2; the real bound floors to2, proving exact integer maximum2. Every Apéry factorization is unique.
Do not restrict weighted unpaid mass to maximal/boundary cells or treat interior mass as vertex count.
No new uniform cap2 is proposed. Full data/checking and witness support are in PROOFS E421,
p39/data/allowance_source_probe.jsonl.gz, and p39/data/interior_unit_candidate.jsonl.

Also false: every source in the E420 interior-to-canonical-boundary injection is a strict actual exit.
In<11,12,18>, the source v=(0,2),j=1 maps to u=(2,0), with3*12=2*18 a tight zero-gap trade. Keep the
inner trade structure when translating canonical geometry into arithmetic credit. E420's rank bound
is dominated by the old whole-boundary bound; it is not a revival of the false CR-TILE criterion.

### E423: optimal axis recombination alone pays the original finite baseline — FALSE

For the general E422 weighted transport, choose the cheapest axis-adding decomposition flow and
claim rho+Gamma.b>=P_old. Exact flow primal/dual certificates refute this on genuine remaining-domain
semigroups: <60,67,71,121> has14<27 (bound-13), <60,61,67,71> has16<26 (bound-10), and
<146,147,155,185> has82<115 (bound-33). This is not a Wilf or full capped failure. It excludes fixing
the claimed payment by another axis-adding allocation within this network. Shared-row cancellation
helps compared with independent local decompositions but does not close the arithmetic budget.
E424 makes a justified correction using already forced-zero coordinates; its universal sign remains
unproved. Do not revive an interior unit cap, require each column to pay for itself, or infer
positivity from the corrected bound's positive saved examples. Data: p39/data/axis_transport.jsonl.gz.

### E426: scale the primitive orbit allocation by canonical column lengths — FALSE after zero closure

In E406's genuine e11 semigroup <153,166,170,317,325,474,617,766,921,925,1080>, primitive170 has an
orbit {4,21,38,55,72,89,106,123,140}. Strict excess supplies have column weights1 and give7; six active
tight allowances have column weight7 and give42. They remain active after full known-zero closure.
The unweighted cycle pays7>=6 exactly as E425 proves; column scaling is the invalid step. Another
orbit has8<24. The full corrected E424 bound remains4419>0. Do not call this a certificate/Wilf
failure or abandon global compensation: discontinue only per-orbit column-scaled self-payment.
Exact table/proof/checker regression: PROOFS E426, verify_probe.py primitive_cycle_budget, run_checks.sh.

### E427: treat positive orbit slack as free new dual credit — coefficient accounting forbids it

For any nonzero nonnegative balanced primitive-edge circulation lambda, compensating its primitive
coefficients with the existing primitive-bound multipliers changes the finite lower bound by
-m*sum_tight lambda-sum_j g_j*sum_s lambda_(s,j)<0. This holds across primitive directions too.
Thus the E425 scalar surplus is not an independent additional source after objective matching;
its primitive value credit has already been spent. This does not rule out signed zero-RHS trades,
unbalanced flows matched by adaptive cap loads, or a global boxed allocation. E429 retains exactly
those possibilities. Do not revive nonnegative circulation-only funding under a new local weight.

## E430 — baseline order and lo-only payment failures (2026-10-23)

**False:** the raw or profile-zero-patched upper-closure baseline is antitone along tight primitive
addition. In <60,67,71,121>, w55=355,w11=71,w6=426, but the patched baseline has l55=0<l6=1.
Every full feasible certificate instead has y55>=2, since y6=1. The raw baseline already fails
on <66,67,71,72,98,103,128>: b34=0<b35=1 along primitive67. The36-seed audit finds8 offending
comparisons. Full certificates DO have strict primitive decrease (PROOFS E430); do not transfer
that property to a cheaper baseline without proof.

**False:** the ordinary axis network's uncovered lo-only reflection cost is at most rho. Reprice
every positive arc to0, retain negative lo prices, and solve exactly: <114,305,307,310> gives183>111;
<62,87,88,89> gives52>49; <65,82,214,217,265> gives79>62. Integer flow/dual audits and regeneration
are in EXPERIMENTS E430. The larger P<=rho+support_sum remains unproved; this payment argument
cannot prove it.

**Strategy correction:** all36 current transport anchors satisfy the older proved SUPP shape
criterion. Their positive certificate values are not evidence from unresolved actual Wilf cases.
The old63 height3 case survives the shape-only filter but is also excluded by the residue-aware
SUPP bound (kappa8<Dep42). Always distinguish those criteria. No enlarged positive-anchor survey.

## E431 — common primitive-lift monotonicity is false (2026-10-23)

Increasing EVERY nonmultiplicity primitive by m, keeping m fixed, need not increase W even
when e, the exact tight pattern, the canonical tile and the largest residue remain unchanged:
<10,187,451> has c1344,g705,W573, while <10,197,461> has c1374,g726,W570. Both have e3.
The primitive coefficient vector is H=(24,-27), so the direction(1,1) changes W by-3.

This failure is arbitrarily large. From the seed <10,17,41>, put L=180N+1, then compare
<10,17L,41L> and <10,17L+10N,41L+10N>. For all N>=1 the exact Wilf numbers are9450N+48
and9447N+48. PROOFS E431's general zero-trade integer-realization lemma proves the claim;
independent membership/Apéry audits check the explicit small and coarse-bound realizations.
This is a failure of the universal monotonicity shortcut, not of Wilf, RD, or positive recession:
the direction leaves the fixed-largest-residue region eventually. All these e3 examples are
known Wilf cases; they are not passed off as resistant actual candidates.

Also do not equate T=ℕ with the Lean NoWrap hypothesis without U=T. In <10,17,41>, T=ℕ,
but w4=34 has only factorization2*17 and residue sum14>=10. The earlier general descent text
has been clarified to retain U=T when applying NoWrap. The Lean theorem itself is unchanged.

## E432 — a fixed one-per-cell free allowance is insufficient (2026-10-23)

In the completion/Hall graph for genuine <114,305,307,310>, a34-cell down-set has source
benefit exceeding its proper-divisor capacity by39. A scheme allowing at most ONE unmatched
unit at each source cell would allow only34 and fails by5. Equivalently its raw support
value Dep+N-kappa is-5. Exact integer flow and cut plus direct column counts are saved in
data/completion_cut_probe.jsonl.gz and independently checked by --completion-cut-check.

This does not refute the proposed GLOBAL m114 allowance, COMP, the full-tile support bound,
or Wilf. It rules out the tempting fixed cellwise allocation in a proof of that global claim.
The canonical degree allocation has sufficient PARENT capacities but may exceed individual
beta source capacities; do not describe it or the inversion preflow as a feasible full flow.
The41 positive exact cut checks are closed diagnostics, not a uniform capacity theorem.

## E433 — joint-interior credit does not pay the cut (2026-10-23)

FALSE: h(E)<=|A-Delta_1|, where A consists of cells with ALL active successors inside E.
The cross-sum proof that |A-Delta_1|<=m is valid; the claimed payment is not.

Genuine S=<40,41,42,43>, m40,e4,c520,g273,W468, rho0, has canonical cut
E={0,e1,e2,e3,2e2,e2+e3,2e3}. Benefits total16 and nonmaximal divisor capacities total11,
so h5. A={0} and its difference set has4 points. Direct columns give Dep2,N0,kappa0:
the missed credit is already a boundary problem without modular carry loss. Another
checked cut in <62,87,88,89> has demand30 and interior credit16.

The independent membership/flow/column audits are in data/completion_structure_audit.json.
Five discovery failures on the SAME41 saved selected cuts are listed in
data/completion_interior_test.json; only40 and62 are used as independently audited
falsifications. No failure of the global m allowance or Wilf is asserted.

STOP this interior-only allocation. The replacement directional residue pool in PROOFS
E433 counts separate ray starts and their actual cyclic aliases; its global payment remains
UNKNOWN. Two exact all-cut checks are diagnostics, not a new positivity theorem. Also stop
the generic supported-matrix idea unless an arithmetic operator is actually constructed:
mere existence of a high-rank supported matrix is equivalent to the same Hall condition.

## E434 — one slot per formal boundary alias is too strong (2026-10-23)

In genuine <19,39,41,50,52,53> (m19,e6,c88,W32), the full tile has6 nonmaximal cells and
21 directional negative starts. Their27 formal Laurent monomials map onto15 residue basis
vectors, with kernel dimension12. Missing-direction capacity is4; even all residual auxiliary
capacity (missing4+wrapped7=11) is smaller than12. Therefore a separate injection of EVERY
alias relation into either of those slot spaces is FALSE.

This does NOT refute the E434 residual flow: actual expanded demand including the reserved
origin is25, not27. Its24 nonzero units fit into4+7+14=25 slots, with margin1. Independent
membership, C flow/cut and definition-level counts are in completion_frozen_audit.json.
Do not overcount all formal aliases as additional source debt. Carry charges and alias
compensation must share a single budget; at least6 wrapped units are required on this tile.
Also do not assume the integer lift set is closed under every primitive residue subtraction:
this is the old U=T condition (E379/E431), not automatic. The10 seed already refutes it.

## E435 — neither fixed use of surplus column starts is universal (2026-10-23)

After the PROVED cancellation of internal aliases, JD has debts L_out+K and resources
C+(Gamma-F_in)+V. Reserving C ONLY for carries fails on the old19 full tile: exterior
aliases8 exceed remaining missing0+wrapped7. Reserving C ONLY for exterior aliases fails
on the old34-cell114 cut: carries54 exceed remaining missing2+wrapped45. Wrapped capacity
alone also cannot pay those raw carries,54>45. These are failures of fixed accounting rules,
not JD+, the C flow or Wilf. Exact decompositions are in data/joint_defect_audit.json.

The scalar lowering trial T=sum c_j X_j^(-1)(Z_j+M_j), with M_j indicating a successor in E,
fails the proposed nullity<=Gamma bound already on E={0,e_1,...,e_d}: all unit columns land
in the same e_0 row and the origin adds only one vector, so rank2 versus domain d+1. For
d>=2, nullity d-1>0 although Gamma_D(nonmax E)=0. This symbolic failure persists for
generic nonzero coefficients. Stop coefficient tuning for that operator. It does not
invalidate the distinct internal slot map or the safe-cut proof in PROOFS E435.

## E436 — exterior aliases cannot always be paid from C first (2026-10-23)

FALSE stage: L_out<=C for every genuine tile cut. A normalized special sum-dominant set H
with |H+H|-|H-H|>=|H| gives a genuine-semigroup counterexample by B=H+max(H)+1,
m=4max(B)+2 and S=<m,m+B>. The Apéry pair cut has K=F_in=0 and
L_out-C>=|H+H|-|H|-|H-H|+1>0, for EVERY choice of pair representatives.

Using the classical base29 cube gives m97558,e513,c623660,g383166,W122749762>0. The lex
cut has L_out30988,C17064, shortfall13924; the representative-independent lower bound is1440.
This is not a JD+ or Wilf failure: Gamma227504 and V14090 leave joint margin227670.
All the missing pair directions here are zero-gap canonical trades, not strict exits.
See PROOFS E436 and data/mstd_shadow_audit.json; no new MSTD-set novelty is claimed.

The repaired least-weight/lex root association always gives a canonical exit, but is not
injective: exterior images2 and3 in this SAME witness both charge the one-unit exit
u_14+e_(j_0), canonically replaced by2u_7. Stop independent least-root assignment and
the C-only stage. No more witnesses or root-weight optimizers are next; a joint exchange
with unused starts, unreserved missing slots and wrapped capacity is still required.

## E442 — unrestricted closure monotonicity and a Hilbert-dimension substitution (2026-10-23)

FALSE on all S: W(S)>=W(U), U the E441 normalized odd-ideal closure. The exact witness
S=<5,21,22,23,24> has c20,g16,e5,W0; U=<5,8,9,11,12> has c8,g6,e5,W2. All source
leave-one-out gcds are1. More generally classical S=<m,2tm+1,...,2tm+m-1>, m=2b+1,
t>=2, gives W(S)=0,W(U)=b, so the gap is unbounded. Proof in E442, one C/membership
witness audit only. These examples have e=m and DO NOT refute MON1 restricted by3e<m.
They refute neither Wilf nor full nonnegativity transfer. No family search is next.

Also FALSE: applying Macaulay to E442's ideal-power algebra with embedding dimension
e(S)-1, or merely the number of nonzero odd-ideal generators. The OLD S=<5,7> has
eS-1=1 and one nonzero ideal generator, but layer Hilbert function(1,2,2,1,1). The paired
quotient primitive7 acts in degree1 by1->8 (and degree2 by2->9), so it cannot simply be
discarded from coefficient actions. Actual algebra embedding dimension is |I minus T|=2.
The standard-graded construction itself is valid; its generator-sensitive positivity
application remains missing. Neither counting layer support nor a generic O-sequence
bound can silently substitute for the source generator budget.

## E443 — a single graded reflection cannot supply the torsion gap payment (2026-10-23)

Optional sufficient mechanism: reflect every gap n>=m into one nonzero degree D-n of
the conductor differential torsion quotient, using one common integer shift D. FALSE
even for OLD S=<19,39,41,50,52,53>. The only possible shifts145..152 all fail by explicit
zero torsion degrees; its total torsion dimension63 nonetheless exceeds the required50.
OLD6/7/11 also admits no shift29..31; OLD5/7 admits35. Exact witnesses are in
data/differential_audit.json, independently reconstructed using all factorization trades.
This refutes even a graded vector-space reflection injection, NOT the ungraded torsion
bound, the conductor differential inequality or Wilf. Do not repair it by merely choosing
another common shift or enumerate more positive differential examples.

## E445 — primitive-only parity funding and transplanted unit depth (2026-10-23)

FALSE even in the remaining cofactor1 domain: after source odd-parent assignment, the
primitive credit alone pays the finite gain. OLD19 has q3,D_odd219,P_par319 and reserve458;
the reserve-free numerator is-924 for EVERY parent rule (all seven parents are unique).
Full W remains32. Do not optimize selectors or discard the unmatched deficit reserve.

FALSE transplantation: every primitive step drops the a-based coordinate by1, or the
unweighted m-based Dep bound applies unchanged when a is not the multiplicity. OLD
S6/7/11, a7, has tight17->23 by p6, mu0->0. The naive bound6>W4; safe weighted depth
uses floor(p/a) and gives4. This is not a counterexample to E430 at its stated modulus.

Also FALSE on paper: higher-layer deaths require an ORIGINAL even primitive. For all-odd
S13/15/47, I={0,1,17}+T with min(T positive)=13, so4 belongs to H_4, but4*15=13+47.
No additional numerical search/invariants are used for this hand counterexample.


## E451 — minimum odd increment is too coarse as the sole descendant payer

The valid VALUE-DEATH inequality controls ALL killed scalar classes by their closure
values (no fixed first-edge capacity). It does NOT pay OC-W alone. On the existing
S=<13,15,17,19> calibration, alpha1,U=N,A_alpha78,b6,e4,c64 and J<=12 force its proposed
standalone lower bound <=-96 while actual W48. This refutes the standalone-payment
proposal, not VALUE-DEATH, TRANSFER or Wilf. No new calculation/family programme.
Retain full original increment distribution, source filtration and all global reserves.

## E453/E454 — closure-moment shortcuts and finite neutral exits (2026-10-23)

FALSE: plain U odd moment Z, even with one credit per actual dead column, always pays
OC-W. Paper control S=<101,103,311,313>, U=N has Z5050,b50,J<=100 and c<=6564, so
3c-4(b+Z-J)<=-308. This is an upper bound refuting that proposed lower-bound sign,
not an exact c/g/W computation or a Wilf counterexample. The original relation
5*103=313+2*101 supplies omitted descendant credit1940 across these closure words.
Do not replace the original source presentation by U's minimal generator description.

FALSE as COMPLETE source-death mechanisms: pure-coordinate inputs only, or primitive
outputs only. Paper S=<31,33,37,72> has birth3 at u5 and source representative72,
requiring mixed input2*33+37=72+31. Distinct paper S=<31,33,43,91> has birth5 at u5,
source representative134=43+91, nu2,lambda4,D1; no primitive-output block fits5*33,
but5*33=31+43+91 saves1. Both satisfy the deep/sparse/cofactor guards; no new invariant
search was performed. General mixed-input/composite-output SOURCE-TRADE remains valid.

The advisor's zero-death alpha refinement is valid, but NOT a sufficient universal
payer. On the ONE fixed31/33/101/103 control, it still gives joint upper438 instead
of297 and Wlower-48 instead of516. Explicit disjoint original-source4/5-block trades
repair this control exactly; that does not establish their universal sufficiency.

Bounded access result, NOT a universal failed lemma: all19 saved neutral representatives
and their complete8294-replacement outgoing neighborhoods have no improving F exit.
Total165880 evaluations including initial collection. The proper two-atom residue-cover
recipe also finds0 full/one-hole covers among70125 exchanges at the saved input. Stop
these recipes at their stated bounds. Neither finding rules out deeper neutral paths,
other coordinated changes or globally resistant configurations. E455 proves a general
buffered connection after coordinated shifts; it does not preserve W or stay in the box.

## E456 — completed source units do not alone pay the finite correction

FALSE for arbitrary constructed residue tiles: a downset containing every original
primitive unit automatically has nonnegative constructed Wilf lower bound. Paper
S=<4,5,7>,pivot4,D={0,e1,e2,2e2} has weights0,5,7,14, actual max10 and actualW2,
but L(D)=2*10-(3/4)*26-3/2=-1. It already contains every unit, so unit completion
makes no change. This is not a counterexample to Wilf, the cyclic-tile inequality,
E456 compression, or a remaining-domain theorem. It demonstrates the unpayable step
of substituting the constructed maximum for actual M without retaining the excess.
Also, all units may be present in D_U while deaths remain (old paper31/33/43/91).
Therefore missing-unit primitive blocks are a proved component, not a complete
source-trade catalogue; mixed/composite relations and full reserves remain necessary.

## E457 — complete units/primitive outputs/bounded input degrees cannot pay uniformly

For odda>=39, canonical closure tile of S=<a,a+2,3a-4,3a-2> has EVERY source unit,
but L<=(-a²+40a-81)/5<0. All deep/sparse/cofactor1 guards hold. Thus the actual
closure construction, not merely an arbitrary completed tile, refutes unit restoration
as a sufficient payer. Primitive-output trades give ZERO credit on this D_U. For ANY
fixed inputdegree capB, choose3a-2>5B: after cancellation the source-saving bound
sigma<=(5B-3a+4)/2<1 rules out every positive applicable block, even with composite
outputs. A successful input may need degree>=ceil((3a-2)/5), and the required total
credit grows quadratically. This is a universal-mechanism falsifier, not an e4 Wilf
programme; only a39 was computed (actualW780,L-144). Keep cyclic/macroscopic relations.

## E458/E459 — single corners fail even from canonical D_U

The arbitrary-tile guard S24/40/195/396/402, box-times-chainD, has L-9 and no corner
exchange; a six-word shadow repairs it. It has cofactor3 and is NOT asserted reachable
from the odd closure. Its role is to reject an unrestricted quantifier, not the
normalized target. E460 proves why every full-unit one-max box fails cofactor1.

The stronger REACHABLE falsifier is S=<38,51,67,120,193>,a51. Canonical original-label
D_U already has allunits and L-8, but exhaustive13-border enumeration finds NO positive
corner. There is no first restoration/corner move, so even the existential standalone
unit+single-corner payer fails. It has cofactor1,c333>4m152,3e15<m38. A compatible
TWO-cell13*67->5*38+120 shadow gives credit22,L102; scalar alternatives give valid
positive bounds with non-downset images. Thus stop corner-only as a universal rule,
not source trades generally. ActualW287 and SUPP Q103 are positive: the combined
[SUPP OR source policy] statement is NOT refuted, and this is not a resistant Wilf case.
Full exact witnesses/independent audits are trade_search_459*.json in apery_scan/data.
## E461/E463 — cap transfer and fixed-rank one-pass returns are insufficient

FALSE: W(U)>=0 implies the arithmetic-capped original D_U lower bound Lcap>=0.
Genuine S=<201,203,593,595> has U=N,allunits,cofactor1,c15025>4m,e4,3e<m and
Lcap=-2209 although W14735. Paper estimates already give Lcap<=-1246 without
using exact invariants.36 explicit backward words supply NET2090 additional
credits and give valid L6151. Do not count their raw savings on top of cap credit.
This source is ALREADY SUPP-covered,Q484,so combined max(Q,L) is not refuted.

The old four raw-negative controls ALL have positive free-capped bounds. The38
corner-stall repair's raw22 credit becomes net1 after cap. Keep the original move
policy falsifications, but do not call them an unpaid capped/combined obstruction.

FALSE FOR EVERY FIXED r>=1: from the INITIAL D_U, allowing arbitrary nonnegative
extensions on ANY at most r original coordinates, plus arithmetic caps, always
gives a nonnegative scalar Wilf lower bound. E463 gives a proof-only family with
d=r+2,a=B^d+2 and genuine cofactor1/deep/sparse source<a,a+2,3a-2B,...,3a-2B^(d-1)>.
All source units are present. Even with UNBOUNDED return lengths, only O(B^(d-1))
of a~B^d residues get a candidate <=M; most retain caps nearM, forcing Lr<0.
Both independent paper reviews pass. No W sign, negativeQ or numerical family
search is asserted. The statement concerns one frozen-tile pass; sequential or
evolving coupled constructions and general mixed-output packings are NOT refuted.

Stop fixed-rank catalogue patches as standalone payers. Retain original labels,
genuinely joint coordination, all reserves and the weaker support/source target.
E462 also guards against inferring a removable cofactor from mere sharp periodicity:
the Z35 two-coset example has all cofactors1. The necessary full-Q one-label bridge
remains UNKNOWN, not refuted by that periodicity guard.
## E464 — exposure and unrestricted word counts do not supply the proposed sign shortcuts

FALSE: actual-top exposure makes the outward weighted tile flux B(t) unimodal or
makes conductor-grid samples always an upper sum. The paper cofactor1/deep/sparse
source<5t+3,5t+4,20t+11,20t²+21t+5>,t>=2, has a strict flux drop followed by rise,
and sampling discrepancy -(3t+2)/2. Old mirror19 gives opposite discrepancy+6.
The new guard has Q>0,type3<e4,so it falsifies the UNCONDITIONAL helper, not the
corrected allowance Dep+(m-1)/2 or a counterexample-conditional variant. Exact
full-Q target is now also written as sum B(M-km)>=g-Dep; that sign is UNKNOWN.

FALSE: count all original words without a rank/degree cap, then use the universal
collision bound E/A²<=e/c. Cauchy-Schwarz ell>=A²/E is valid, but multiplicities
can concentrate nearc. Paper family<6b,6b+3,6b+6,N,N+1>,fixedb>=4,N=1mod6 large,
has arbitrarym and allcofactor1, yet E/A²=27/(5N)+O_b(N^-2)>5/c. This asymptotic
claim supplies no uniform E448-cutoff comparison. One exact control DOES lie
inside that cutoff:24/27/30/1003/1004,c1098,W812,Q84,A12635,E754417,
eA²-cE=-30133741,M1121<=16560. Even integerceil(A²/E)=212 yields bound-38.
It is already support-covered, not a negativeW or combined-target failure.

Stop raw uniform-word energy as a universal payer. Weighted disjoint-band bounds
remain valid but need an actual arithmetic overlap estimate; singleton bins merely
reconstruct support. E463's catalogue obstruction and this all-rank collision
obstruction are distinct. No family-W programme or larger source census follows.

E465 is a CLOSED finite diagnostic, not a failed general theorem: all468 unit images
of9 cached tiles have Q>0,F<=0. It gives no global exclusion. E466 strictification
does not revive any prior staged/alias payer: their D/delta/phase countergeometry
is retained exactly, even though canonical missing edges become genuine strict gaps.

## E467/E469 — stop duplicate alias capacity and forced reflected-edge transport

The candidate WHOLE alias-kernel bound F_in+L_out<=Gamma_D(P) is ALREADY refuted by
E435 OLD19:12>4. No new counterexample or calculation is claimed. The correct full
budget retains m-|U|; all alias terms cancel to Q=Dep+V-K. A larger alias forest
does not by itself improve this margin. Do not relaunch the duplicate stronger bound.

FALSE: every weighted canonical edge can be paid by its reflected missing direction
at the actual-top residue involution h. OLD19 edge e39->2e39 has demand2, reflected
parent2e52 maximal with raw capacity1, and strict actual gap38. Strictification cannot
change the maximality/capacity. This is an edgewise rule, not a global matching failure.

The issue also affects a genuine mixed-carry increment in the NONFLAT cofactor1
cached63 origin:454+492=946 has kappa1; h(e454+e492)=e477+e307, value784, is maximal.
Both prefix orders therefore reflect their final edge from a parent excluded from
Dep. The492 exit gap is315>0. This refutes even the LAST-EDGE-REFLECTION-TO-DEP rule
for this token, not joint use of wrapped slots, other missing directions or full
source reserves. Q56,W708 already cover it. No negativeQ/W or all-routing obstruction.

E468 is a CLOSED finite diagnostic, not a failed general theorem:349 distinct ray
targets/309eligible, bestF-3,minQ52,0negativeW/eligibleQ orpositiveF. No inference to
full chamber adjacency, longer neutral paths or all support-two starting directions.
The general axis-carry injection remains valid; stop forced reflected-edge allocation,
retain joint mixed-carry augmentation with BOTH unused wraps and Dep available.

## E470/E471 — coherent accessibility does not supply sign or a boundary-only payment

False unconditional shortcut: nonnegative endpoints of the coherent cost path imply
J_e(t)>=0 throughout. PAPER S=<5,7,8>,a5,beta(1,4),chi(1,0), has J0=2,J1=actualW3,
but at t2/15 costs(8/3,8), minima(0,8/3,16/3,8,8) give J=-2/5. These are positive
REAL costs, not a numerical semigroup or a full actual-coordinate LP witness. The
control is outside sparse/deep remaining domain, so no restricted theorem is refuted.
Old equality5/21/22/23/24 also consumes ALL initialgluing surplus10: separate reserve
or fixed-fraction funding is insufficient unconditionally. Endpoint arithmetic matters.

False shortcut linking the two routes: source-credit-improving coherent exchanges
force monotone fullQ. The SAME51 paper path has first two genuine walls48p->q+r,
47p->2q, with normalized realizable profiles Q96->100->96 at topres45. Finalsource
P53/149/151 gives positive scalar credits44/43. These compare distinct coherent
profile realizations; Q of ONE fixed actual source is not changing under its scalar
word substitutions. No negativeQ or Wilf failure follows. Stop a monotonicity proof,
not general Qjump analysis or source quota. Full unrestricted coherent paths cannot
stall before exact Apéry values; a search for such auxiliary stalls is unnecessary.

False even for FULL capped feasible x: Gamma.x>=e*sumx. The already saved65/82/214/
217/265 source has x1 on9 residues, Gamma.x39<e*sumx45. Its Gamma.y-Dep1231 gives
J-Q1225 despite the deficit6. Saved146/155/184/535 gives332<336 with ysurplus651.
Both exact feasibility checks pass, no new solves. This stops dropping the second
term of J-Q=(Gamma.x-e*sumx)+(Gamma.y-Dep), not universal reserve transfer J>=Q.
All15 saved transfer margins positive, minimum82; those point tests are CLOSED.
The attempted column/tree proof is the ALREADY recorded E422/E423 budget, not a
new payment lemma or a reason for another transport optimizer. No universal sign.

E472 (2026-10-23): the NONFLAT restriction does not rescue kappa<=Dep. The explicit
508-element complete cyclic two-basis in PROOFS E472, reflected and given one
cheap primitive, produces a genuine m95250,e508 source with canonical height3,
c>4m,3e<m and every primitive-deletion gcd1. On paper F=kappa-Dep>=525. The
general one-cubic change is DeltaDep=e(1-z_new), Deltakappa=-kappa(removed pair).
For this reflected source that removed mixed pair has kappa0. Independent paper
review passes the covering, carry bounds, exact one-cell change and all guards.

This improves on the old FLAT19 counterexample to unrestricted KAPPA-DEP; it
closes the later NONFLAT phase-free helper, which E457/E466 left UNKNOWN. It
does NOT refute kappa<=Dep+N or Wilf. The actual N and the actual reserve R must
both be reported. The explicit source can have very large positive W; it is a
mechanism falsifier, not a low-W witness or an unresolved Wilf case. No automatic
cover-size increase, atom scan, orbit census or GPU campaign follows this result.

E473 (2026-10-23): the valid coefficient-fiber centroid bound Xi<=Hcal does NOT
give its proposed integrated quota, even with ALL initial reserves in the actual
remaining domain. ONE S=<13,15,35,37> has U=N,J0=12,c95,g51,W81,allcofactors1,
3e<m,c>4m. Firsttop/walls4/117,1/4,2/7 yield envelope loss>=12+39/4=87/4>12;
the rest is nonnegative. Actual full loss is -69. The surrogate discards the
useful negative loss on[4/117,1/4] (exactly-909/26). Stop the stronger envelope
quota, not the valid centroid inequality, original integrated budget or Wilf.
Paper review and independent455-word/1820-rational-comparison audit pass. No family
scan/path engine. Full Xi, actual-top odd count and all reserves remain necessary.

Likewise a skew Fourier/Hilbert correction is not nonnegative merely because
the top is actually exposed. E472 plus the GENERAL E465 mirror-realizability
theorem gives opposite corrections +/-47843/2, with the same center232407/2,
on normalized nonflat realizations (PAPER ONLY, no extra numerical source/image).
Both fullQ values staypositive. Symmetrizing annihilates the skew term and loses
the phase; it does not pay it. The Fourier representation duplicates old Win.

E474 status guard: the principal Qnegative=>one-original-label prime bridge is
UNKNOWN. The precise JOINT-ANCESTOR flow rule is also UNKNOWN universally, not
refuted by its passing cached63 control. Its Hall condition includes stronger
PROPER-downset inequalities; closure alone yields neither translation periodicity
nor a prime quotient with one original surviving label. A Qpositive deficient cut
would falsify THIS rule/classifier only. E462's original35 guard has K=0 on paper,
so its planned numerical rule test was cancelled before execution as vacuous.

E475–E478 (2026-10-23): the ORIGINAL E469 axis injection cannot be frozen in a
deficient-component=>cofactor argument. The genuine E476 endpoint
S=<65,147,270,319>,W1919,Q155,all deletioncofactors1, has the six-cell downset
E={1,p,r,pr,r^2,pr^2},p147,r319. It has mixed demand2 and no boundary capacity.
Every accessible unused slot of the original fixed axis map is absent: its two
free r-column slots lie at parents r^4,r^5 outside E. Thus that frozen graph has
a Hall-cut deficit2 with no one-label prime quotient. Reassigning TWO axes frees
the front slots needed by pr/pr^2, and an exact global102-token certificate passes.
The JOINT cut is TIGHT, not deficient: kappa(E)=2=min(V_C(E),N_C). No positive
JOINT deficit, negativeQ or Wilf counterexample is obtained. Its residue set has
trivial stabilizer, so even positive mixed demand plus saturation is insufficient
for a cofactor conclusion. Strict unpaid debt AFTER all permitted moves matters.

The bounded64-proposal signed-component critic is CLOSED without actual failure;
its tight endpoint above is useful for permissions, not evidence proving the bridge.
Forced flow>K gives a negative signed margin and is not new actual demand. Do not
apply largest-maximizer strict marginal claims to the default SMALLEST residual
cut or omit zero-demand word cells when recovering a largest WORD downset.

Generic matching is not a shortcut to the arithmetic subgroup bridge. E478 checks
two primary theorems and records the incompatible ground set/translation and
modularity hypotheses; the existing E464 family has a U_(3,6) resource block.
Another primary paper has generic partition matching failures even over prime
cyclic groups, but for a DIFFERENT matching relation. Neither observation refutes
JOINT-ANCESTOR or the principal Qnegative bridge; both stop an unsupported appeal
to a generic theorem. Keep all original labels, physical capacities and reserves.

E479–E483 (2026-10-23): the FULL JOINT-ANCESTOR policy, including arbitrary
reassignment WITHIN each axis's own column, is now FALSE on genuine normalized
deep/sparse sources. Small self-contained witness S=<65,3381,6275,7337> has
c47339,g24192,ell23147,W45249,Dep128,kappa17,N29,Q140,allcofactors1 and unique
Apéry factorizations. Nine positive word reductions certify the whole65-cell tile
on paper (PROOFS E482), independently of source/flow software.

At residues(p,g,r)=(1,35,57),phase46, the12-word box p^0..1*g^0..1*r^0..2 has
four mixed demands, no boundary capacity and only two usable column-reserve units.
Equivalently52 original group demands reach capacity50. Its residue stabilizer
is trivial, and primes5/13 retain2/3 ORIGINAL labels. Thus even STRICT unpaid
debt after all permitted own-column reassignments does NOT force a removable
cofactor under this rule. The principal Qnegative=>one-label bridge is NOT refuted:
Q140 is already covered by Dep>=kappa, and W is positive. Stop the old policy/
classifier; do not call passing earlier controls evidence of a universal theorem.

The deletion-stable ten-word subcut has a support-two maximal gr^2 at phase0.
All its children exist, yet none of its outgoing edges wraps. The correct E479
successor/saturation lemma therefore has a vacuous saturation conclusion here.
Also PAPER <13,17,19,31> has a global-maximal support-three carry word whose every
support-two divisor has zero carry. No carry-only reduction to support two is valid.

E480's original uniqueness GUARD failed before any new source evaluation, because
the saved base has17 tight trades3g+p=3r. It was not a failed new semigroup or a
completed48-run. Revised E481 explicitly proves that +65g breaks all17 ties in
the retained direction;18 new unit sources then run, stopping at first failureu23.
No remaining30 units or old468-image orbit replay was performed.

The repair must permit axis transport BETWEEN columns. On the SAME small witness,
two same-direction, ancestor-supported axis permissions increase flow102->104.
They move one axis from each N0 column into a parallel column's spare reserve,
while preserving total physical capacity. This repairs the FULL certificate,
not only the local cut. It does not prove a new universal policy. E477 fixed
N_C quotas are valid only with own-column axes; after transport the valid bound
is mixedload_C<=N_C+netaxisexport_C, with global netexports0. Ignoring these signed
exports recreates an artificial obstruction; allowing unrestricted arbitrary
transport merely restates Q>=0. A direction/source-sensitive theorem remains needed.
