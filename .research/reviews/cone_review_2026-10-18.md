# Referee report: cone-tile lemmas (e = 4, 3-D lattice tiles)

Reviewed: PROOFS.md §"Cone tiles: QF-pair lemma, location corollary, Fiber Lemma, and qO ≤ 2t + 11"; NOTEBOOK.md
"2026-10-18 (night 17)" (Lemma TF-cone, Lemma F-cone); and their inputs in PROOFS.md (CHT, T, T′, B, F, S/S′, P/P′, QF,
(P0)/(P1), level picture, Wall and Floor Lemmas). Reviewer: independent subagent, 2026-10-18. I edited no project files.

## 0. Bottom line

- **I found no false step in any proof I was asked to review.** Every lemma that the Corollary "HT for every cone tile with
  m ≥ 281" depends on is CORRECT as stated (current text). I checked each one line by line and also by computation.
- **One misstatement, now fixed.** The version I first read began Theorem qO-cone with "qO ≤ t − 1 + 2|Y|". The proof gives
  only 2t − 1 + 2|Y|. The lead has since fixed this (PROOFS.md line 687, "Correction … a typo").
  - The typo'd bound is **FALSE** on the lattice-free cone class. Smallest counterexample I found: m = 243, qO = 27 > 26 =
    t − 1 + 2|Y| (§2).
  - The Corollary never used the typo'd bound. It uses qO ≤ 2t + 11, so the HT chain is not affected.
- The threshold arithmetic is correct. The last failing m is 280, and HT holds for every m ≥ 281 (exact check up to
  2·10⁵, analytic proof from m ≥ 287).
- The suggested repairs (§4) are wording fixes and checker weaknesses. None of them changes a statement.

## 1. Per-lemma verdicts

"Argument" means I re-derived every step. "Computation" gives the range in which my independent checker
(scratchpad `review/indep.py`, written from the statements, not from project code) found 0 violations. Ranges:

- **EXH4:** every lattice-free set with L₁, L₂, L₃ ≤ 4 (all h, F, G, every q ∈ Cyl with q ≥ (1,1,1), and q = None for 𝒞).
  That is 84,537 sets: 66,325 cone and 18,212 𝒞.
- **EXH5:** the same with L ≤ 5: 8,630,220 sets, of which 7,843,965 are cone (see §3).
- **TILES:** every real tile in logs/tiles/m{30,40,50,60,64}.jsonl. That is 13,299 cone tiles and 68,943 𝒞 tiles.
- **RND/ANN:** random samples and annealing, described in §3.

| Item | Verdict | Checked by |
|---|---|---|
| Lemma CHT, δ ≥ m + 1 − LHS (any D) | CORRECT | argument; computation EXH4/5, TILES (δ is computed directly from H) |
| Level picture (𝒞) (i), (ii) | CORRECT | argument |
| Lemma T, t ≤ C − 2 (𝒞) | CORRECT | argument; EXH4/5 (𝒞), TILES (𝒞) |
| Lemma T′, t ≤ C (cone) | CORRECT | argument; EXH4/5, TILES, ANN (max t − C = 0, attained) |
| Lemma B, C² − 3C + 6 ≤ 6m (𝒞 and cone) | CORRECT | argument; EXH4/5, TILES, ANN (tight: three staircases with q = (1,1,1), e.g. (5,4,3,2,1)³ with m = 31) |
| Lemma F, qU ≤ t − 1 (𝒞) | CORRECT | argument; EXH4/5 (𝒞), TILES (𝒞) |
| (P0), (P1), Lemma S, Lemma P, Lemma QF (𝒞) | CORRECT | argument; EXH4/5 (𝒞): S′ with K = ∅, and qO ≤ t − 1 |
| S′ (defect localization) | CORRECT | argument; asserted for **all** cells with x + e_d ∈ D ∀d (not just tripods/qO) in EXH4/5, TILES |
| "a top is used in ≤ 2 directions"; Y₁, Y₂, Y₃ pairwise disjoint | CORRECT | argument (y + e_a, y + e_b ∈ K ⇒ y ∈ K); computation as above |
| P′ | CORRECT | argument; all ordered tripod pairs × 6 planes, EXH4/5, TILES |
| (P0′), (P1′) | CORRECT | argument (they use only that ψ is nonincreasing) |
| (Peak′) | CORRECT | argument; all p, all 6 orientations, EXH4/5, TILES |
| QF-pair Lemma + mirror | CORRECT | argument; every pair (v, u), all 6 orientations (c, a), EXH4/5, TILES, the DS family |
| Location Corollary | CORRECT | argument; EXH4/5, TILES, family (13 DS cells at Q = 14) |
| Fiber Lemma | CORRECT | argument; EXH4/5, TILES, family, ANN maximizing #DS |
| Theorem qO-cone, qO ≤ 2t − 1 + 2\|Y\| (current text) | CORRECT | argument; every sub-claim asserted separately (list below) |
| *qO ≤ t − 1 + 2\|Y\| (original headline typo)* | **FALSE** (lattice-free) | counterexample in §2 |
| Refinement qO ≤ t − 1 + 2\|Y\| + \|Max ∩ B\| | CORRECT | argument (top_a of x ∈ B_c stays in B_c, a ≠ c) |
| Lemma TF-cone, 2Tri ≤ t + 17 (\|Y_d\| ≤ 2) | CORRECT (two wording fixes, §4) | argument; claims (i)–(v) and the budget asserted separately |
| Lemma F-cone, qU ≤ t + 2 | CORRECT | argument; level counts and per-level cycle rank asserted |
| Wall Lemma, Floor Lemma (lattice input) | CORRECT | argument; TILES: t_w ∈ [L_c − q_c, L_c − 1] and distinct, ≤ q_c quadrant corners, ≤ 1 floor inner corner, \|Y_d\| ≤ 2 |
| Corollary: LHS ≤ 6t + 30, δ ≥ m − 6C − 29, HT for m ≥ 281 | CORRECT | argument; exact arithmetic (§1 (g), §3 item 7); LHS ≤ 6t + 30 asserted on every set with all \|Y_d\| ≤ 2 |

Sub-claims of Theorem qO-cone asserted separately (exact counts, not just the final inequality):

- qO = t − comp + rank.
- Every cycle-closer either has both tops already used in the same direction (and is then DS), or has a "case-2" top.
- A case-2 top lies in Y. Each y is case-2 for at most one cell.
- #case-2 cells ≤ |Y|.
- The DS map x ↦ top_{a(x)}(x) collides only inside Y, at most twice per y.
- #DS ≤ t + |Y|.
- Each of these was also tested with a second tie-breaking order for equal |x| (EXH4, 0 violations).

Sub-claims of TF-cone asserted separately:

- Every cross-shared top lies in Y, at most one cross share per top, and Σ s_cross ≤ |Y|.
- (ii) holds for **every** pair of partners (u, u′), not only for some pair.
- (iii) x_a = q_a − 1 and x_c < q_c.
- (iv) Φ(a,b) lies on one b-line.
- (v) At most 1 member has x_b < q_b, and at most |Y_a| − 1 members have x_b ≥ q_b. Both parts are lattice-free.
- |Φ| ≤ 2 when |Y_a| ≤ 2.
- Σ(s_same − 1)⁺ ≤ Σ|Φ(a,b)|.
- 2T − t ≤ −1 + Σ s_cross + Σ(s_same − 1)⁺.
- 2Tri ≤ t + 17 whenever all |Y_d| ≤ 2.

Sub-claims of F-cone asserted separately:

- Every qU cell has x + e_a, x + e_b ∈ Max.
- Level counts (direction 3): at most one c = 1 edge and one c = 2 edge per level v ≠ q₃, at most 2 of each at v = q₃.
- Cycles of G_U are created only at level v = q₃ (top-down construction).
- rank(G_U) ≤ 3 and qU ≤ t + 2.

### Notes on the specific points (a)–(g) of the brief

**(a) Cycle-closers in G_O.** The classification is exhaustive.

- A closer's two endpoints lie in one component with ≥ 2 vertices, so both tops have already been used.
- Per top y_d, either some earlier qO user has top_d(u) = y_d (case 1), or none has. In case 1, u lies on the d-ray
  below x, since |u| ≤ |x| and u ≠ x. In case 2 every earlier user uses y_d in another direction, so y_d ∈ Y by S′.
- If both tops are case 1, x is DS. (DS is order-independent; its witnesses are automatically processed earlier.)
- Case-2 count. If y is used in the two directions d₁ (first) and d₂, only the first d₂-user can be case-2 at y.
  So there are ≤ |Y| case-2 cells.
- Checked: exact counts in EXH4/5 and TILES, plus the second tie order. The maximum number of cross-only closers found
  lattice-free is 6 (ANN, m = 249). On tiles it is 1.

**(b) Fiber Lemma, both cases.**

- ĉ ≠ c: x ∈ B_c gives x_ĉ ≥ q_ĉ, x̂ ∈ B_ĉ gives x̂_ĉ < q_ĉ, and a ≠ ĉ gives x̂_ĉ = x_ĉ. Correct.
- ĉ = c = 3, a = 1:
  - (P1′) forces ψ(p) > ψ(p̂). Because Q = q₃ at both points, the drop comes from F: F(X+k) < min(G(Y), q₃).
  - The mirror QF-pair at x̂ then needs (α′) or (β′). (β′) needs ψ(p̂) = q₃, which fails.
  - (α′) forces Y − i′ = q₂ − 1 and ψ(X+k, q₂−1) = min(F(X+k), G(q₂−1)) ≥ q₃ + 1, which contradicts F(X+k) < q₃.
  - a = 2 is the 1↔2 mirror. Correct.
- Stress test: the lattice-free family (examples/qO_lattice_free_family.md) has Q − 1 DS cells stacked at
  p = (q₁, q₂). None of them share a maximal top in the same direction. Verified for Q = 4..14.

**(c) Top used in ≤ 2 directions.** S′ applied to two of the three directions gives y + e_a, y + e_b ∈ K, hence y ≥ q.
Correct. I tested this over all cells with all x + e_d ∈ D, not only tripods or qO cells.

**(d) F-cone.**

- U_v = A₃ ∩ R_v for v ≤ q₃ and U_v = (A₃ ∩ R_v) ∖ Quad for v > q₃. So U_{v+1} = U_v ∩ R_{v+1} fails only at v = q₃.
- The 𝒞 no-cycle argument needs only three things: that relation, the down-set property of U_v, and the notch of two
  consecutive corners of U_v lying in U_v. All three hold at every v ≠ q₃.
- At v = q₃, a c = 1 edge needs p + e₂ ∈ U_v ∖ U_{v+1}. Then either p + e₂ ∉ R_{v+1} (the old e_L), or p + e₂ ∈ Quad ∌ p.
  The second case gives p₂ = q₂ − 1, p₁ ≥ q₁, and p is the end of row q₂ − 1. That row end is unique.
- Symmetrically there is at most one extra c = 2 edge.
- So level q₃ has ≤ 4 cross edges. The first one joins a fresh component, so at most 3 new cycles appear. Correct.
- Computation: per-level counts were never exceeded. No cycle was ever created at a level ≠ q₃. Max rank(G_U) = 1 in
  every range.

**(e) TF-cone.**

- (iii) is correct. (iv) is correct: P′ is used in the (a, c)-plane with third direction b.
- (v): two members below q_b are impossible. Members with x_b ≥ q_b have c-tops in Y_a: the column over (q_a − 1, x_b)
  is at least as tall as the one under the partner's c-top, which has height ≥ q_c. These c-tops are distinct from each
  other and from the c-top of the topmost member's b-partner.
- Accounting: an s_same = 2 tripod lies in Φ(a,b) ∪ Φ(b,a). An s_same = 3 tripod lies in ≥ 3 families. So
  Σ(s_same − 1)⁺ ≤ Σ over the 6 ordered pairs of |Φ(a,b)| ≤ 12. Correct.
- Observed maxima with all |Y_d| ≤ 2 (lattice-free, EXH5 + ANN): 2Tri − t = 5, Σ s_cross = 6 (= |Y|, so the bound in (i)
  is attained), Σ(s_same − 1)⁺ = 2, |Φ| = 1.
  On tiles: 2Tri − t ≤ −2, s_cross ≤ 1, excess ≤ 1, |Φ| ≤ 1.

**(f) Lemma B and Lemma T′ for the cone class.**

- Lemma B. K misses the coordinate planes (q ≥ (1,1,1)), so the three faces of D equal those of Cyl and lie in D.
  - Union of faces: Σ|A_c| − ΣL + 1.
  - Each face satisfies |A| ≥ L + L′ − 1 + T(k), because corner s has coordinates ≥ (s − 1, k − s).
  - L₁ ≥ k₃, L₂ ≥ k₁, L₃ ≥ k₂.
  - Jensen on the real quadratic T(x) = (x−1)(x−2)/2, with k_c ≥ 1, gives C² − 3C + 6 ≤ 6m.
  - Tight for three staircases with q = (1,1,1).
- Lemma T′. The telescoping t = κ(A₃) + Σν_v is general. ν_v ≤ [a drop] + [b drop] for v ≠ q₃. At v = q₃ there are at
  most 2 more: the top of column q₁ − 1 and the end of row q₂ − 1. ν_{L₃} = 0 and q₃ ≤ L₃ − 1. So t ≤ C. Correct.

**(g) Arithmetic.**

- LHS ≤ 2t + (t + 17) + (t + 2) + (2t + 11) = 6t + 30.
- δ ≥ m + 1 − LHS ≥ m − 6t − 29 ≥ m − 6C − 29.
- With C_max(m) = max{C : C² − 3C + 6 ≤ 6m} (integer arithmetic, which equals ⌊3/2 + √(6m − 15/4)⌋): 6C_max + 29 > m for
  every m ≤ 280 (all 280 values), and 6C_max + 29 ≤ m for every 281 ≤ m ≤ 200,000.
- For m ≥ 287 the closed form suffices: 6C ≤ 9 + 6√(6m), and m − 6√(6m) − 38 ≥ 0 there.
- The slack at m = 281 is exactly 0, and at m = 288 it is 1 (C jumps to 43).
- δ ≥ m − 6√(6m) − 38 also holds. Correct.

## 2. Counterexamples found

**To the original typo "qO ≤ t − 1 + 2|Y|" (lattice-free cone class).** Both examples below satisfy every |Y_d| = 1, so the
Floor-type bound holds, but they are not tiles: the lead reports that they fail Wall + Floor.

- Lead's family (examples/qO_lattice_free_family.md, code src/scratch/ds_family.py) at Q = 11:
  - h = (12, 12, 2×11), F = (14, 12, 11, …, 1), G = (14, 12, 10, …, 1), q = (1, 1, 11).
  - m = 291, t = 24, qO = 30, |Y| = 3, so qO > t − 1 + 2|Y| = 29.
- Smaller variant I found (top value L₃ = Q + 1 instead of Q + 3), Q = 10:
  - h = (11, 11, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2)
  - F = (11, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1)
  - G = (11, 11, 9, 8, 7, 6, 5, 4, 3, 2, 1)
  - q = (1, 1, 10)
  - m = 243, t = 21, qO = 27, |Y| = 3, #DS = 9, rank(G_O) = 8, so qO = 27 > 26 = t − 1 + 2|Y|.
  - The correct bound gives 27 ≤ 2·21 − 1 + 6 = 47.
- The variant family has qO − (t − 1 + 2|Y|) = Q − 9.
- This is the smallest violation I found. Short hill-climbs from Q = 9 found nothing smaller; it is not proved minimal.
- In EXH4/5 (L ≤ 5) the typo'd bound is never violated; the maximum of qO − (t − 1 + 2|Y|) is −5.

**To the stated lemmas: none.** Every assertion above returned 0 violations in every range.

**Bookkeeping discrepancy.** examples/qO_lattice_free_family.md says G has length Q+2 and h(0) = Q+2. ds_family.py builds
G of length Q+1 and h(0) = Q+1. The table (m = 53, 101, 165, 245, 341; t = 2Q + 2; qO = 3Q − 3; rank = Q − 2; #DS = Q − 1)
matches the **code** version: I reproduced it exactly.

## 3. Computations run (all exact integer arithmetic; scripts in this directory)

1. **Independent checker** `indep.py`.
   - Membership is computed from the three projections minus K, not from the project's `build`.
   - ht comes from a reach-DP. On 4,211 random sets I cross-checked C against the distinct-value count, and the DP and
     H(D) against brute force (for the sets with |D| ≤ 60).
   - t, Tri, qU, qO and C agree with the project's `cls_anneal.stats` on those sets (`sanity.py`, 0 mismatches).
2. **Exhaustive lattice-free** (`exh.py`), every L₁, L₂, L₃ ≤ M, all nonincreasing h, F, G with h(0) = L₂ and
   F(0) = G(0) = L₃, every q ∈ Cyl with q ≥ (1,1,1), plus q = None:
   - M = 3: 892 sets, 0 violations.
   - M = 4: 84,537 sets, 0 violations (17 s). Repeated with the second tie-break order (`exh_tie.py`, cone only, 66,325
     sets): 0 violations.
   - M = 5: 8,630,220 sets (786,255 cylinders; 7,843,965 cone sets). **0 violations of any assertion** (1,193 s,
     10 processes; log `exh5.log`).
   - Maxima at M = 5 on cone sets with all |Y_d| ≤ 2 ("tile-like"):

     | Quantity | Max | Where attained |
     |---|---|---|
     | 2Tri − t | 5 | — |
     | Σ s_cross | 6 = \|Y\| | (5,3,2,1,1)³, q = (1,1,1), so (i) is tight |
     | Σ(s_same − 1)⁺ | 2 | — |
     | \|Φ\| | 1 | — |
     | #DS | 2 | — |
     | qO − t | 2 | — |
     | rank(G_O) | 3 | — |
     | qU − t | 0 | — |
     | rank(G_U) | 1 | — |
     | t − C | 0 | — |
     | C² − 3C + 6 − 6m | 0 | tight |
     | LHS − 6t | −9 | — |
     | qO − (2t − 1 + 2\|Y\|) | −11 | — |
     | qO − (t − 1 + 2\|Y\|) | −5 | — |

   - Cone sets with some |Y_d| > 2 reach 2Tri − t = 8 and |Y| = 12 (three staircases (5,4,3,2,1), q = (1,1,1)). That is
     consistent with the lead's remark that 2Tri − t is unbounded lattice-free.
   - On 𝒞 the maxima are exactly the 𝒞 lemmas, all attained: 2Tri − t = −1, qO − t = −1, qU − t = −1, t − C = −2.
3. **Real tiles** (`tiles.py`, `wallfloor.py`), all records of logs/tiles/m{30,40,50,60,64}.jsonl:
   - Counts: 13,299 cone tiles (418, 1,015, 2,158, 5,356, 4,352) and 68,943 𝒞 tiles. 0 violations of any assertion.
   - Each tile is a fundamental domain of x ↦ r·x mod m, and q* ∈ Λ.
   - Wall Lemma (t_w range, distinctness, ≤ q_c corners) and Floor Lemma (≤ 1 inner corner) hold, with |Y_d| ≤ 2.
   - Cone-tile maxima: qO − t = −2, 2Tri − t = −2, qU − t = 0, t − C = 0, #DS = 1, cross-only closers = 1,
     rank(G_O) = 1, rank(G_U) = 1, |Φ| = 1, LHS − 6t = −11.
   - CHT slack m + 1 − LHS − δ ≤ −5.
4. **Random lattice-free cone sets** (`rnd.py`): 13,200 sets with lengths/values ≤ 9, 91,406 with ≤ 10, and 7,339 with
   ≤ 14/12. 0 violations.
   - **Family neighbourhoods** (`famnbhd.py`): 7,200 random walks of 1–8 mutations from the DS-rich family, Q = 4..9.
     0 violations, with up to 8 DS cells and rank(G_O) = 7.
5. **Annealing** (`ann.py`; 92 runs: logs ann.log, ann2.log, ann3.log; lattice-free, optionally penalising |Y_d| > 2;
   windows m ∈ [30, 250]; 2.5k–20k iterations, seeds 1–7). Every visited state was run through all assertions, with full
   checks at least every 25th step. 0 violations in all 92 runs. Annealing is heuristic, not exhaustive.

   | Target | Max reached (lattice-free) | Max reached with all \|Y_d\| ≤ 2 |
   |---|---|---|
   | qU − t | 0 | — |
   | t − C | 0 | — |
   | C² − 3C + 6 − 6m | 0 (tight) | — |
   | qO − (2t − 1 + 2\|Y\|) | −11 | — |
   | qO − (t − 1 + 2\|Y\|) | −4 for m ≤ 250 (positive only via the hand family, §2) | — |
   | 2Tri − t | — | 5 |
   | Σ s_cross | — | 3 |
   | Σ(s_same − 1)⁺ | — | 2 |
   | LHS − 6t | — | −11 |
   | #DS − t − \|Y\| | −6 | — |
   | rank(G_O) | 9 | — |
   | cross-only closers | 6 | — |
   | \|Φ\| | 1 | — |
6. **Lead's DS family** (`family.py`), Q = 4..14: every assertion holds, including Fiber and Location with up to 13 DS
   cells and the 2t − 1 + 2|Y| bound (slack −16 to −26). The typo'd bound fails exactly for Q ≥ 11.
7. **Arithmetic**: integer evaluation for m ≤ 200,000 plus the closed form above.
8. **Broad Φ** (`broadphi.py`, EXH4 cone): even without requiring an a-share, Φ(a,b) satisfied (iv) and (v). So the
   restriction in §4 item 2 is needed for the proof, not for the truth of the claim, in this range.
9. **Outside the brief** (`dsstruct.py`): the night-17-late "Structure of DS cells" claims (a), (b) and (c) were checked on
   81,424 sets (EXH4 cone, family neighbourhoods, all cone tiles). (a): ψ_c(p) = q_c. (b): every partner satisfies
   u_d < q_d and ψ_c(u) > q_c. (c): ≤ 8 DS cells per direction off p = (q_a, q_b). 0 violations; on tiles at most 1
   such cell. Only computation; I did not referee these proofs.

## 4. Suggested repairs and edits (no statement changes)

1. **Theorem qO-cone headline.** Already corrected to 2t − 1 + 2|Y|. Record the counterexample of §2 next to the
   correction, so the typo'd version is not revived as a "sharpening" later.
2. **TF-cone (ii)/(v), definition of Φ(a,b).** Write Φ(a,b) = {tripods x with same shares in **both** a and b such that
   some b-partner u′ has top_c(u′) ∈ Y_a}. The proofs of (iv) and (v) use the a-partner of x, which exists only under
   this restriction. The accounting only needs this restricted family.
3. **TF-cone (v), first bullet.** "x_b = q_b − 1" should read "x_b ≥ q_b − 1, hence x_b = q_b − 1 when x_b < q_b". The
   P′ alternative top_c(u) + e_b ∈ K gives only x_b ≥ q_b − 1.
4. **Theorem qO-cone, case-2 count.** Add the sentence: "the first user of y (in any direction) is not case-2 at y, and
   in the second direction only its first user is". This is what makes "≤ |Y| cells" immediate.
5. **Location Corollary under (α).** Say that u + e₁ ∈ D because u is qO, so every u + e_d lies in D.
6. **Project checkers (a weakness of the evidence, not of the proof).** In `src/scratch/qo_fiber_check.py`:
   - (D) 'Drank' is vacuous: every closer is classified as DS or cross-only by construction.
   - 'Dq' is the graph identity.
   - 'final' tests qO ≤ 2t + 5 + 2|Y|, which is weaker than the claimed 2t − 1 + 2|Y|.
   - There is no test of #DS ≤ t + |Y|, of #case-2 ≤ |Y|, or that a cross-only closer is genuinely case-2.

   So the "0 violations" logged for (D) carries no information beyond (A)–(C). My checker tests these counts directly.
   Also, `tf_cone_check.py`'s header says |Φ| ≤ 3, while the code (and the lemma) say ≤ 2.
7. **Tile count.** The notebook cites 82,254 non-two-face tiles for m = 30, 40, 50, 60, 64. The five jsonl files contain
   82,242 records. Reconcile the 12-tile difference or cite the file counts.
8. **Not reviewed, but noted.** The Corollary's last bullet relies on Theorem C-HT and the HT scan (m ≤ 130, and
   131–280 for cone tiles). Those were outside this review. The cone part of the e = 4 chain is complete on paper only
   once the 131 ≤ m ≤ 280 cone-tile scan finishes.
