# STATE.md — handoff (updated 2026-10-19, afternoon; GW-27 quadratic Apéry sets, G-ID line)
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

- **GW-27 (2026-10-19): Wilf for every S whose Apéry set is quadratic (each element 0, a generator or a sum of two
  generators), at every depth.** Hence Wilf whenever 3n_1 > c + m, without Spirito's conditions. Also holds in down-set
  form (residue-complete, degree ≤ 2) and with Ap(S, n) for any minimal generator n. Paper proof in PROOFS; every step
  checked on 62M semigroups (E219). Lean: queued.
- GW-26 (codex P5, verified): Wilf for 3m < c ≤ 4m when 2n_1 ≥ c − m. P5b reports a one-low-unit extension
  (2n_2 ≥ c − m); not yet verified by the lead.

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
1. **HCR, a shape-only criterion through CH′ (MAIN for e = 5).** Bound each column deficit by (m+1)·height for
   non-maximal tops, with distinct residues for maximal tops. HCR ≥ 1 implies Wilf for every S with that tile.
   - **Computational theorem (E153):** the complete exact 4-D tile enumeration gives HCR ≥ 1 on every 4-D lattice tile
     with 14 ≤ m ≤ 39 (only failures: two tiles at m = 13; 9,532,388 tiles, exact certificates checked through 39).
     With BGOW (m ≤ 18), **Wilf holds for every e = 5 S with m ≤ 39.** Trust base: the enumerator and its exact volume and facet certificates, checked by an independent
     checker pass, but the same codebase.
   - 4-D tightness: thin near-simplex tiles (levels ≤ 3, t ≈ m/2, mostly two-face), with H/m ≈ 0.8–1.2 and R carrying
     about 45%. The m = 13 failures are exactly the near-star formula with d = 4, q = 8.
   - Open link: a proof for m ≥ M0. HT4 alone (H ≥ 1.5m) fails up to at least m = 27, because thin tiles persist.
     Next: the H–t trade-off and an inverse theorem ("small H ⇒ D nearly contains a big coordinate simplex"),
     contradicted by the discrete Minkowski bound (a 4-D tile containing Δ_N has m ≥ |X_N| = 21, 55, 131 for
     N = 2, 3, 4).
2. **General Wilf: Down-set Wilf GW (MAIN universal line, PROOFS "Down-set Wilf").**
   - Statement: for EVERY down-set D ⊂ ℕ^d (|D| = m) on which x ↦ x·n mod m is bijective,
     dmM − (d+1)Σ_D v ≥ (d−1)m(m−1)/2; equivalently (d+1)ℓ(Δ) ≥ c(Δ) for Δ = v(D) + mℕ.
     - GW ⟹ Wilf (Apéry tile).
     - GW on largest-generator tiles is Wilf itself (Lemma GW-1).
   - Evidence:
     - Exhaustive over ALL down-sets (codex C scanner, E186): 0 failures in 1.38·10¹¹ instances (d = 3, m ≤ 30;
       d = 4, m ≤ 22; d = 5, m ≤ 19; k ∈ {0,1,2}^d). Also d = 2 (m ≤ 26) and signed n. Adversary to m = 100: none.
     - Non-minimal domains can beat the Apéry tile (d = 3), so GW is strictly stronger than Wilf.
     - Residue completeness is essential: the injective-only version is false (GW-6).
   - Proved:
     - the reformulations, the column form, and boxes (B = (d−1)mM/2);
     - corner reflection g ≤ tℓ, so GW when t ≤ d (GW-8/9);
     - GW for d ≤ 2 (GW-10/11);
     - the descent lemma GW-13/14: only corners deeper than k_min = min⌊n_a/m⌋ can break GW.
   - **Stronger conjecture PGW (prefix/window family, PROOFS).**
     - Statement: Σ_{j≤i}|U_j| ≤ dΣ_{j≤i}|L_j| for every i. For semigroups: #(gaps < im) ≤ (e−1)·#(S ∩ [c−im, c)).
     - Evidence: 0 failures on 5.9·10⁹ down-set instances and on all semigroups of genus ≤ 36 (E188, E189).
     - Proved: P_1 and **P_2 (GW-16; multiplicity form, no residues needed)**, all P_i when t ≤ d, P_i for i ≤ k_min.
       Semigroup corollary GW-17: #(gaps < 2m) ≤ (e−1)·#(S ∩ [c−2m, c)), which contains Kaplan's c ≤ 2m.
     - **P_3 PROVED (GW-19, paper; codex P3, re-checked by the lead).**
       - Band count for 3m ≤ M < 4m: residues give t ≤ ρ and g + ℓ = M − m + 1.
       - Residue-free Theorem H for M ≥ 4m − 1: column reflection plus payments.
       - Semigroup form WW_3 for every S, which contains Eliahou's c ≤ 3m with no Macaulay theorem.
       - Corollary **GW-20: Wilf holds if at most e − 1 PF numbers are ≥ 3m.** It misses 1,794 of the 38.9M S of
         genus ≤ 32 (E204). Those have e ≤ 7, and the ladder with P_4, P_5, P_6 would cover them all.
     - P_4 (GW-21, GW-24, GW-25). Its regime 4m ≤ M < 5m is Wilf for 3m < c ≤ 4m, which is OPEN in the literature.
       - Proved: a ≤ 6 (a = 6 with certificates); pure A with 2n_1 ≥ c − m for every a (GW-25, arc lemma); H4 for
         M ≥ 6m − 3. See Next precise task (c).
       - Proved so far: a transfer lemma, a joint short-residue lemma, and the case a ≤ 3 (a = number of directions
         with n < 2m − ρ). Also the signed B_3 packing m ≥ C(a+3,3) + 2C(a+1,3) and degree-≤ 2 down-sets.
       - Open: a ≥ 4 in the primary regime, and the truncated regime M ≥ 5m (residue-free fails at 6m − 2).
     - New tools and conjectures (PROOFS):
       - identity GW-CR (exact): dℓ − g = Σ r(x)/m + Σ column terms Ψ;
       - CP (deficits routed to lower covers) and CCP (carries routed to columns through x or its lower covers).
         Both hold on all residue-complete data and both need residues (E202, E203).
     - Use: it is the Hall condition for matching gaps to elements with depth-lowering allowed. A proof must trade the
       descent map (fails only through directions with n_a < jm) against corner reflection (fails only through more
       than d corners at depth j).
   - Killed (E183–E185, E187, E190): per-depth, suffix family, column reflections, depth-lowering without columns,
     single crossing.
   - The level/carry split (W = Lev + Car) and the exchange-inequality picture are kept as tools. RW = GW with k = 0.
3. **e = 4 formal verification (background; G-Lean).** Next Lean items: the cylinder lemma and Wall/Floor from IsTile.
Killed this cycle: TL (false at e = 5); the unsorted S1 ≤ 2m (false at m = 25); ATOP_γ as a universal criterion (6
two-face e = 5 failures); the cube version of ATOP (false in d = 4); crude CR for 4-D (φ up to 0.8); the cone-LP
relaxation (weaker than HCR on thin tiles); the generator-drop induction W(S) ≥ min W(S minus one generator) (false).

## Next precise task
(a) Codex P5b is RUNNING (session 01a1525d-16ff-7fc2-a405-17a585c3ec31, log scratchpad codex/p5b_log.txt). Target: Wilf for
    all 3m < c ≤ 4m (low units). It reports a proof for one low unit (2n_2 ≥ c − m). Verify step by step when it lands.
(b) Lead, G-ID line (PROOFS GW-27 and NOTEBOOK 2026-10-19 midday):
    - Exact cell identity W = Σ λφ + Σ x_aβ_{x,a} − Σ γ for every residue-complete down-set.
    - Deficient cells (c_x < 0) are almost all top cells with residue ≤ μ, in every degree (E220).
    - WQ (units + window (μ, 2μ] pay all deficits) holds for all e ≥ 4, genus ≤ 30, but is FALSE in general. It fails
      for cubic and higher D at μ ≈ m − 1 or μ ≈ 1, where pairs with λ ≥ 1 pay. Next: the cubic case (Wilf for
      4n_1 > c + m) with window + lower-cover payments.
(c) Lean, queued after P5b (one agent at a time): GW-27 first (elementary, self-contained, down-set form), then GW-19/GW-25.
(d) Background: gfan re-check of E153 (m = 38–39); codex HT4 subclass claims are unverified.
