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

## Pattern C — a relaxation that removes the structure doing the work
| Statement | Counterexample |
|---|---|
| TB4 with only the half window [h, 3h′) | E314 |
| Z12 without any window covering | m = 47, B = {10,12,13}, h = 20, slack −2 (E335) |
| Small-part inequality (core regime) | STATE 0f |

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
