# FAILED.md — registry of failed proof mechanisms (Wilf)

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

