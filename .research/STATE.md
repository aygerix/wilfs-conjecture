# STATE.md — handoff (updated 2026-10-18, night 17 late)
(The previous handoff, night 13, is in git history: commit cb2738b and earlier.)

## Current directive (user + advisor, 2026-10-18)
- FOCUS: our own route to Wilf for e = 4, a standalone structural theorem on 3-D lattice tiles:
  HT, δ(D) = H(D) − (m − 1) ≥ 0, via the forest/tripod/qO-cycle counting and the lattice restrictions (Wall/Floor).
  kseth/wilf-e4 (GitHub, Sept 2026) has a different, complete proof. We have read it; our argument is independent.
- REVISED TARGET (advisor, 2026-10-18 late): the weakest bounds that close the argument. These are 2Tri ≤ t + O(1),
  qO ≤ 2t + O(1), qU ≤ t + O(1), and a PROVED sublinear bound on t. Then compare the threshold with the exhaustive range.
  Do not pursue sharper constants (e.g. qO ≤ t + O(1)) unless the threshold is out of reach.
- BUDGET: 24–48 h of focused work from 2026-10-18 ~11:00 local, then reassess. No open-ended computation.
- PARKED: FWx/FWy all-e criteria (PROOFS "Final-window criteria … PARKED").

## The e = 4 argument (our route) and the status of each link
1. e = 4 ⇒ the factorization tile D ⊂ ℕ³ is a down-set fundamental domain of a lattice, |D| = m. PROVED (PROOFS "Factorization down-set").
   LEAN for the grlex tile used here: MaxCL.lean `isFactTile_factDownSetG`, `IsFactTile.isTile`, `IsFactTile.columnIdentity`.
   (TileReduction.lean `isTile_factDownSet` is about the LEX tile.) Not in Lean: e_a ∈ D, and the closed-cone inequality
   p·q ≥ p·rep(q) used by the LP certificate.
2. Height criterion: (m+1)H(D) ≤ mW + m(m−1), so δ ≥ 0 ⇒ Wilf. PROVED on paper (NOTEBOOK night 13).
   Integrality sharpening (referee 2026-10-18, checked by the lead): W ∈ ℤ, so δ ≥ −1 (H ≥ m − 2) ⇒ mW ≥ −2 ⇒ W ≥ 0 for m ≥ 3.
   Per-tile LP certificate (src/tile_lp.py) for tiles with δ < 0.
3. Two-face tiles ⇒ Wilf. PROVED (paper + exact finite check m ∈ [18, 74]). External inputs, cited and not rechecked by us:
   Eliahou JEMS 2018 (c ≤ 3m ⇒ Wilf) and BGOW IJAC 2020 Thm 4.3 (m ≤ 18 ⇒ Wilf), plus the Lean τ-criterion.
4. Non-two-face tiles lie in 𝒞 (Loomis–Whitney) or the cone class Cyl ∖ (q + ℕ³). PROVED (cylinder lemma; its part (a) is
   HRW Prop 2.6(b)). Two-face tiles are all in 𝒞.
5. 𝒞 tiles: δ ≥ m + 14 − 5C, so HT for m ≥ 131 (Theorem C-HT); δ ≥ −1 for m ≥ 130. PROVED on paper, reviewed (below).
6. Cone tiles: δ ≥ m − 6C − 29, so HT for m ≥ 281 and δ ≥ −1 for m ≥ 280. PROVED on paper 2026-10-18, reviewed (below).
   Ingredients: Lemma CHT, TF-cone, F-cone, qO-cone (Fiber Lemma), T′ (t ≤ C), B (C ≤ 3/2 + √(6m − 15/4)).
   Lattice input: only |Y| ≤ 6, via the Floor Lemma.
7. Finite range, by complete computer enumeration of tiles (tile_scan, Python + C port):
   - All non-two-face tiles m ≤ 130: HT 0 failures except m ∈ {8, 15, 16, 17, 19, 20, 23}. m = 8 is covered by BGOW (its LP
     bound fails, κ = 4); the others are LP-certified (κ recomputed independently with HiGHS by the referee). m = 17 and 23
     have δ = −1, so the integrality sharpening covers them without LP.
     The gaps m = 90, 100, 108, 114, 115 were closed on 2026-10-18 (logs/tile_scan_C_gaps.log).
   - [Superseded by E141.] Earlier 8-bit logs: logs/tile_scan_C_131_280.log (local, m = 131–229) and
     logs/tile_scan_C_226_280_fejer_uint8.log (m = 226–235); m = 236–255 had no log until E141 (manuscript gap G1, closed).
   - BUG FOUND by the chain referee (2026-10-18): src/c/tile_scan.c stores coordinates as uint8_t, so a MAXM-300 build wraps
     coordinates ≥ 256 and corrupts the traversal for m ≥ 257. Confirmed by the lead on fejer: at m = 257 the 8-bit build has
     127 area-defective lattices, the 16-bit build 0.
   - FIX: src/c/tile_scan_v.c (16-bit coordinates via -DCT=uint16_t, and a per-lattice completeness certificate: the cone
     areas, summed mod 2^61−1, must equal the simplex). It is identical to the old build at m = 131, 200, 257, with every
     lattice certified.
   - **m = 256–280 DONE (fejer, 16-bit, certified): HT fails 0 and area-defects 0 for every m**
     (logs/tsv16_256_280_fejer.log; min H − (m−1) ≥ 845). Re-certification COMPLETE: m = 4–119 and m = 120–255 with the
     16-bit build (logs/tsv16_4_119_fejer.log, logs/tsv16_120_255_fejer.log). **Every m in [4, 280] is area-certified
     complete (0 defects).** HT fails only at m ∈ {8, 15, 16, 17, 19, 20, 23}, with the same tiles as the referee's
     independent fan-free enumeration. All 116 m values that overlap the old 8-bit logs give identical lines.
   **So every link 1–7 is now in place: Wilf holds for every e = 4 semigroup, by our own route**, subject to
   (i) the cited external inputs Eliahou (c ≤ 3m) and BGOW (m ≤ 18); (ii) the computer enumeration, now certified
   complete per lattice (area sums mod 2^61−1) for every m ≤ 280, plus exact areas for m ≤ 40 (referee). Two independent adversarial reviews and the Lean checks are listed below.
- Independent adversarial reviews, 2026-10-18, both COMPLETE:
  - cone lemmas, all CORRECT (.research/reviews/cone_review_2026-10-18.md);
  - links 1–6, all CORRECT except the scan bug above, plus minor text fixes, now applied
    (.research/reviews/e4_chain_review_2026-10-18.md).
  The chain referee also independently reproduced the HT-failure list for m = 7–26 by a fan-free enumeration of all
  down-sets, and the LP values κ with a different LP solver. It area-certified traversal completeness for every lattice
  at m ≤ 40 (exact) and m = 19–119 (C, mod p).
- In Lean (2026-10-18, lean/Wilf/CornerArea.lean, verified by the lead): Lemma B (`cornerArea`, any finite down-set),
  Lemma CHT (`cht`, any finite D), Lemma T (`typeBound`, class 𝒞), Lemma T′ (lean/Wilf/ConeType.lean `typeBound_cone`, cone
  class). So the sublinear bound on t is kernel-checked for both classes: t ≤ C, and C² − 3C + 6 ≤ 6m.
  Also in Lean (lean/Wilf/Forest.lean): TF, F, QF and `deltaBound` (δ ≥ m + 14 − 5C on 𝒞), i.e. all of Theorem C-HT except
  the threshold arithmetic.
  Also in Lean (lean/Wilf/ConeForest.lean): the C-HT threshold (m ≥ 131 ⇒ δ ≥ 0), F-cone, qO-cone, TF-cone and the cone
  δ-bound, in sharper forms: δ ≥ m − 6C − 21, so δ ≥ 0 for m ≥ 267. The only hypothesis is |Y_d| ≤ 2.
  NOT in Lean: Wall/Floor (the |Y_d| ≤ 2 input), links 2–4
  and 7. Earlier Lean: TauCrit, TileCL2 (e ≤ 3), TileTop, MaxCL (see PROOFS).
- Trust base of link 7: Gröbner-fan traversal enumerating lattices + code. The C port is a re-implementation of the same
  algorithm (0 mismatches against Python on 188 lines), not an independent method. kseth's enumeration uses a different
  method: a second check exists but has not been run by us (session card proposed; we do not execute their code).

## Proved facts (paper unless marked)
- CH, Corollary H (= Zhai 2011 Thm 1), Lemma A, TOP'' ⇒ Wilf, CH′, CL ⇒ Wilf, Tile-TOP'' ⇒ Wilf, MaxCL ⇒ Tile-TOP'': LEAN.
- Flat-MaxCL, 2-D Tile-CL (every 2-D tile), Wilf for e ≤ 3, τ-criterion: LEAN.
- e = 4 links 1–6 above. Lemmas T, T′, B, F, S, P, TF, QF, (P0′), (P1′), (Peak′), QF-pair, Location Corollary, Fiber Lemma, Wall,
  Floor, LCL, PW (PROOFS.md).
- DS structure (NOTEBOOK night 17 late): DS cells sit over the floor; outside the quadrant corner there are ≤ 8 per direction.
- FW, FWx, FWy are proved as inequalities, for any e (parked).

## Refuted on the way (preserved in NOTEBOOK/EXPERIMENTS/examples)
- Ω = 2Tri + qO ≤ C − 2.
- (K) 2Tri + Q′ ≤ 2t − 2.
- LHS ≤ 4C + O(1) on the lattice-free cone class.
- qO ≤ t + O(1) on the lattice-free cone class (examples/qO_lattice_free_family.md: qO − t = Q − 5).
- |Max ∩ B| = O(1) on tiles.
- CL (Carry Lemma), Tile-CL for d = 6.
- Shape-only FW3/FW3b.

## Open gaps (exact)
- G-scan: CLOSED (E140, E141; every m ≤ 280 area-certified). G-review: CLOSED (both reviews in .research/reviews/).
- G-doc: logs/tf_bounds2.log does not record its m range (manuscript G4); rerun with the range printed.
- G-Lean: all lattice-free counting is done (CHT, B, T, T′, TF, F, QF, the cone bounds, both thresholds). Next: the
  cylinder lemma (link 4) and Wall/Floor from IsTile, which would give "every 3-D lattice tile with m ≥ 267 has δ ≥ 0" in
  Lean; then the height criterion (link 2).
- G-second-check: a method-independent second enumeration for m ≤ 280, or a reduction of the finite range by a sharper
  constant (e.g. LHS ≤ 5C + β ⇒ threshold ≈ 160).

## Three active approaches
1. **Two-face dichotomy, shape side: CR-NTF** (every non-two-face lattice tile satisfies the crude rearrangement bound CR,
   which implies Wilf for every c through the Lean chain MaxCL ⇒ Tile-TOP'' ⇒ Wilf).
   - Evidence: 0 non-two-face failures in 152,855 random S with e = 4–9; exhaustive 3-D tiles m ≤ 26; 82,242 stored
     3-D tiles.
   - Needs lattice input beyond the cylinder lemma (non-tile failure at m = 17, d = 3).
   - Tools: the cylinder lemma in every d (PROVED), t ≤ C, forest counting.
2. **Two-face side: ATOP_γ** (permutation hull + shifted geometric subadditivity; residue-light; any c). It fails only on
   e = 4 books ⟨n², n²+1, n²+n, n²+n+1⟩ (covered by the e = 4 theorem). No failure for e ≥ 5 (random, hill-climb,
   exhaustive generators < 2m). Books in d ≥ 4 are the test case: realizable or not?
3. **e = 4 formal verification (background; G-Lean)** and the e = 5 tile route (cylinder lemma in every d gives link 4).
Killed this cycle: TL (false at e = 5); ATOP without relations on two-face tiles; single-relation repair ATOP+R2 (fails
on books n ≥ 7).

## Next precise task
Find the mechanism behind CR on non-two-face tiles in d = 3 (fully classified: class 𝒞 or cone). Prove a lower bound on
Dep, the incidences in columns with non-maximal top, in terms of m and t, using the cylinder lemma and the Wall/Floor
lemmas. Target: CR for every non-two-face 3-D tile with m ≥ M0 and M0 small. Then test the same mechanism in d = 4.
In parallel (fejer): CR and ATOP_γ exhaustively for e = 5 with generators < 2m and m ≤ 40, and a structured search
for realizable books in d = 4.
