# STATE.md — handoff (updated 2026-10-20; T1/Lemma U line DEAD (codex P15 + external review, lead-verified); next: depth-four LOW closure, item 0d)
(The previous handoff, night 13, is in git history: commit cb2738b and earlier.)

## PLAN TO FULL WILF (2026-10-19, lead; supersedes the 2026-10-18 directive below for direction)
Frame:
- Wilf ⟺ B_tile ≥ (e−2)·m(m−1)/2 (CH′, PROVED).
- Known theorems settle c ≤ 3m (Eliahou), 3e ≥ m (Eliahou) and the very deep regime (VOL-MINK).
- So every unproved S has c > 3m, 3e < m and is not very deep. The goal is a lower bound on B in that window, uniform
  in e.
Lines, in order of cost to decide:
0d. **NEWEST (2026-10-20): the T1 / Lemma U line is DEAD (PROOFS "Conjecture T1", "Lemma U"; E296, E297).**
    - Refuted, all lead-verified:
      - Lemma U (review: m = 83; codex: m = 13, r = (9,10), p = 5, the binary cubic simplex);
      - U-FULL (lead: ⟨23,25,59,61,124⟩);
      - T1-DOWN (review: ⟨20,33,36⟩; codex: ⟨14,22,23⟩, e = 3);
      - TAIL;
      - **T1 itself at the true shift** (codex: ⟨13,22,23,50,51,60⟩, q = 5; unbounded families; lead annealing: e = 5, 6).
    - Survives:
      - T1 at q ≤ 4 (pointwise K ≤ 1; DepthFour.lean);
      - GEN-EH (unrefuted);
      - the exact identities I1–I5 (Wilf ⟺ S_{p*} − mean S ≤ ρ + Λ + E/m);
      - no T1 or U-FULL failure is known with e ≤ 4 (annealing to m = 40, d ≤ 3).
    - Lesson: anneal every new K-type conjecture at m ≤ 200 before trusting the genus census.
    - codex P15: report written but the process died before its §9 (computational record). Resume it with the next
      task and ask it to finish §9.
    - **Next (lead):** the depth-four closure is the live frontier target, Wilf for 3m < c ≤ 4m. With DEPTH4-EH its
      residual is exactly the LOW case Λ + Z < h − e at q = 4. Mechanism to test: Σ_{x ∈ Ap, x < c} τ(x) ≤ Λ, where τ(x) =
      #{a : x + n_a ∉ Ap}. So LOW forces Ap ∩ [0, c) to be nearly closed under adding generators.
0c. **NEW (2026-10-19, latest): Wilf for c ≤ 3m + e (DEPTH4-EH, PROVED; from codex P13 Theorem A, lead-verified E292).**
    - **LEAN (kernel-checked, standard axioms): c > 3m ⇒ e·ℓ ≥ 3m + e**, hence Wilf for 3m < c ≤ 3m + e
      (lean/Wilf/DepthFour.lean, `wilf_of_conductor_le_three_mul_add_embDim`). Elementary proof in PROOFS.
    - At depth four, W = ρ + Λ − R + Z with K ≤ 1. Codex P13 is VERIFIED (hand + own code, genus ≤ 32).
    - Open: UF-RELAY R_A ≤ Λ + C_U + p_A closes c ≤ 4m. Codex P14 is RUNNING on it (log $SP/codex/p14_log.txt,
      waiter bxaonrulc, report src/scratch/gw/p14/P14_REPORT.md).
    - GEN-EH (W ≥ e − (c − (q−1)m), every depth) is CONJ, 0 failures on genus ≤ 31. Its depth-five core has the same
      shape as UF-RELAY.
0a. **NEW THEOREM, LEAN-CHECKED (2026-10-19):** Wilf for every S with 3n_1 ≥ c + m (lean/Wilf/LargeSecondGen.lean).
    It is unconditional, whereas Spirito 1710.09245 needs m ≤ quadratic(e).
0b. **Problem 1.8 landscape (E291, 2026-10-19):** for ⟨m, m+B*⟩ with q ≥ 4, min e·ℓ/c is 1.2 (k = 3, exhaustive
    m ≤ 60). The extremal sets are digital, ⟨a², a²+1, a²+a, a²+a+1⟩, with ratio (4/3)(2a−1)/(2a). They are NO-WRAP,
    hence LEAN-covered. Open: a "carries only help" mechanism in P18.
0. **UPDATE (2026-10-19, latest): overlap-credited chains (E290); codex P13 launched.**
   - Exact: E = B − B_chain = Σ_v (n·∨Z(v) − v), the factorization join excess.
   - Local balance: P(v) − E(v) = v − m·L1(v).
   - CHAIN-U (B_chain + Σ(Σ_{v−n_a∈S} n_a − v)⁺ ≥ need), CHAIN-POOR and WILF+ have 0 failures on genus ≤ 33 (63.75M S),
     on intervals to m = 150, on P12's S_k and in annealing. Each implies Wilf.
   - On multiplicity-free Apéry sets they equal Wilf, so they localize the difficulty in the tile core.
   - At depth four, CHAIN fails (185 interval cases) but CHAIN-U does not.
   - codex P13: prove an overlap-credited chain inequality for 3m < c ≤ 4m. That would be Wilf for c ≤ 4m, a frontier
     theorem.
   - Lead: (a) look for a provable local payment for poor elements at depth 4; (b) P11 full review; (c) height-3 MaxCL
     residual next for codex after P13.
1. **PIVOT (2026-10-19, latest): the Apéry-chain line is dead.** Level-1 intervals refute REST-M3, CHAIN-H3, CHAIN-M3
   and CHAIN-WILF(3e<m) (E289). The smallest is ⟨53, 85..95⟩: height 3, 3e < m, M ≥ 3n_1, ratio 0.99956.
   - MaxCL holds there with slack ≥ 0.85·m². What survives:
     - the n_1 dichotomy (PROVED): M < (h+1)n_1 ⇒ tile height ≤ h;
     - Flat-MaxCL (LEAN), which gives Wilf whenever 3n_1 > c + m − 1.
   - New line-1 target: **MaxCL at height 3**, i.e. close the codex P6 residual. With the dichotomy this gives Wilf
     whenever 4n_1 > c + m − 1, extending Spirito's n_1 > (c+m)/3 (which needs e ≥ 10 and m ≤ (8/25)e² + …) to
     (c+m−1)/4 unconditionally.
     - It is a genuine new infinite class, and the next step on a ladder (height h ⇔ (h+1)n_1 > c+m−1).
     - Next: re-read the P6/P6e residual (k ≥ 5, t ≥ 2, k < min(40t+8, 21t+240), p < 3t), and test MaxCL at
       height 3 on level-1 intervals and B_3-like bases.
     - codex P13 = this residual, once P12 returns.
   - codex P12 is working on REST-M3, which is now known FALSE. Rule: no mid-turn messages. On return, record its
     findings and redirect.
   Superseded entry, kept: **REST-M3** (lead + codex P12, from 2026-10-19 late; PROOFS "The n_1 dichotomy" and
   "Conjecture REST-M3").
   - The dichotomy: if M < 3n_1, the Apéry height is ≤ 2, so Wilf holds (Flat-MaxCL, LEAN).
   - If M ≥ 3n_1, REST := Σ_{w≠0} con(w) ≤ 0 would give Δ ≤ con(0) ≤ d(m−1) ≤ C2 when d ≤ m/2. Sammartano covers
     d > m/2.
   - So REST-M3 alone ⇒ Wilf for every S (PROVED implication).
   - Evidence (E288): genus ≤ 33, 18.4M S in the class, REST < 0 in all, max −0.198·C2.
   - Next:
     - (a) a proof for e = 3 (rectangles and L-shapes) as a template;
     - (b) the count form Σ_a n_a N_a ≤ d m ℓ′, looking for a charging of chain links to left elements;
     - (c) codex P12: an adversarial search plus a proof attempt.
   - Pivot trigger: a counterexample to REST-M3. Then keep the class A and target Δ ≤ C2 directly (CHAIN on A had 0
     failures).
   Previous line-1 target, kept: **CHAIN-H3** (it supersedes CHAIN-WILF(3e<m), PROOFS). If some Apéry element has least
   factorization length ≥ 3, then B_chain ≥ need. With Flat-MaxCL (height ≤ 2, LEAN) this implies Wilf for every S,
   using no depth condition and no Eliahou.
   - Evidence (E286): every CHAIN failure ever seen has height 2. Genus ≤ 33 height ≥ 3: 1,768,572 semigroups, 0
     failures. It is tight near T_{m,q} (≈ 1 + 7.3/m).
   - Next: anneal at m ≥ 48; targeted mixed constructions (an interval core + a height-3 element below M); then a
     proof mechanism (codex P12 after P11).
   Earlier formulation, kept for the record: **CHAIN-WILF(3e<m)**. With Eliahou it would imply Wilf.
   - (a) Break it first: Kunz annealing up to m ≈ 150–200 at e ∈ [m/4, m/3), plus level-2 sets B with
     B ∪ (B+B) = ℤ_m \ {0} (the m = 61 near-miss, ratio 1.08).
   - (b) Sub-lemma: Σ_{w≠0} con(w) ≤ C2/3, which suffices by Lemma W0 since con(0) ≤ d(m−1) < (2/3)C2. Template: the
     layer-1 identity (chain links charged to gaps in [c−m, c−1]), extended to all layers.
   - Decision: a counterexample ⇒ record it and drop the line. It survives ⇒ codex task after P11.
2. **c ≤ 4m closure** (codex P11, running). A theorem either way, and the prototype for higher depth. If its
   mechanism is not specific to q = 4, push to c ≤ 5m, 6m, …
3. **Tile height payments, uniform in e** (robust, harder).
   - P10's missing-direction payment (B2/B4) handles support-restricted tiles.
   - Next: FULL-INTERIOR H + 7|max D| ≥ 2|D| (d = 4, closes e = 5 for large m).
   - Then dimension d with constants polynomial in d, giving "Wilf for m ≥ F(e)". This leaves the window
     3e < m < F(e), which line 1 or the band/Kneser tools must cover.
Operating rules:
- One codex agent at a time; lead verifies everything independently.
- Review every 1–2 days: which infinite class closed? Kill census-only lines.
- Stable results go to Lean.
Pivot triggers:
- A counterexample to line 1 shifts everything to line 3.
- A depth-independent P11 mechanism makes depth induction the main line.

## Current directive (user + advisor, 2026-10-18) — SUPERSEDED for direction by the plan above (kept for history)
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

- Wilf for every S whose Apéry set is quadratic (Ap ⊆ {0} ∪ P ∪ (P+P)), at every depth: Flat-MaxCL (2026-10-17, LEAN
  `wilf_of_apery_height_le_two`). GW-27 (2026-10-19) is a second proof in Kunz coordinates, not a new result. Hence Wilf
  whenever 3n_1 > c + m, without Spirito's conditions.
- GW-26 (codex P5, verified): Wilf for 3m < c ≤ 4m when 2n_1 ≥ c − m. GW-26c (codex P5b, verified by the lead, E221):
  the same when 2n_2 ≥ c − m (at most one low unit). GW-26d (codex P5c, verified by the lead, E227): the same when
  2n_3 ≥ c − m (at most two low units). GW-26e (codex P5c + lead refinements, E228–E232): exactly three low units
  and a ≥ 13. GW-26f (codex P5d T2-SMALL, verified by the lead E234–E235): a ≤ 13 for every α. GW-26g (codex P5e
  T2-SMALL16/17/18, verified by the lead E237): a ≤ 18 for every α, hence **Wilf for every S with e ≤ 19 and c ≤ 4m**,
  and (with Eliahou's 3e ≥ m) for c ≤ 4m and m ≤ 60. Also U-SMALL, U-B0, the B-free strip for α ≤ 14, and
  **LARGE-A′ (lead, 2026-10-19): a ≥ 10·C(α+1,2) ⇒ W ≥ 0** (codex had 16·C(α+1,2)²).
  **GW-26h (lead): α = 4 is closed for every a**, so the primary regime is proved whenever α ≤ 4 (Wilf for
  3m < c ≤ 4m with at most four minimal generators in (m, (c−m)/2)).
  Remaining in 3m < c ≤ 4m: α ≥ 5, 19 ≤ a < 10·C(α+1,2). It is finite for each α, but α is unbounded.
  - Codex P5f (§§52–59) showed the count relaxation has NEGATIVE leading profiles for unbounded α. These are relaxed
    profiles, not semigroups.
    - BASE: a = 3α, ε = α³/24. It is killed by P(C) with constant C, but not by LSP.
    - The matching perturbation needs MATCH-P.
    - The B-loop family (b ≍ α^{3/2}) needs retained-pair packing.
  - So uniform closure needs ambient packing lemmas, not more enumeration.

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
- G-doc: CLOSED 2026-10-19. logs/tf_bounds2_5_500.log is a rerun on fejer with the range (m = 5..500), date and
  script md5 in its header. Its uncovered list is identical to logs/tf_bounds2.log; largest uncovered m = 17 (BGOW).
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
     With BGOW (m ≤ 18), **Wilf holds for every e = 5 S with m ≤ 39.** Trust base: the enumerator and its exact volume
     and facet certificates. Since 2026-10-19 a method-independent enumerator agrees for every m ≤ 39 (E160:
     4ti2 + gfan, own canonical lattices, exact HCR).
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

## New conjectures with strong evidence (2026-10-19 evening; PROOFS "Conjecture CP", "Layer-profile domination")
- CP (column-reflection cells Δ, every order ideal has Σ Δ ≥ 0): 0 failures on all semigroups of genus ≤ 32 and on
  ≈ 260k random instances with m ≤ 220. It survives the deep families on which G-ID downward payment is false. The
  binding ideals are principal; equal fractional splitting (FS) is false.
- STAIR ⇒ RECT ⇒ {PGW, MAJ} ⇒ Wilf (intrinsic, tile-free): 0 failures at genus ≤ 30 and on 64k random instances.
  Exact identity a_j = b_j + p_j (bottom-layer gaps = mirrored top-layer elements + gap pairs).

## Next precise task
(0M) NEW 2026-10-19 latest++++, read first.
    - **Codex P10 VERIFIED (PROOFS "Codex P10", E285).** Two new infinite e = 5 classes:
      - B4: a tile without (1,1,1,1) and m ≥ 10,648 ⇒ W ≥ 3 (intrinsic form: Σ_{i≤4} n_i ≥ c+m);
      - B2: a support-two tile and m ≥ 60 ⇒ W ≥ 1 (intrinsic form: Σ_{i≤3} n_i ≥ c+m).
      Both certificates were reproduced exactly by lead code.
      Open e = 5 residual: full-support tiles (unbounded m), boundary tiles with 40 ≤ m ≤ 10,647, support-two tiles with
      40 ≤ m ≤ 59. Next lemma: FULL-INTERIOR H + 7|max D| ≥ 2m.
    - **CHAIN-WILF is FALSE** (E284): interval semigroups at q = 5, smallest found ⟨23, 54..61⟩, ratio → 0.70.
      - All failures have 3e ≥ m. The repaired CHAIN-WILF(3e<m) survives and, with Eliahou (c ≤ 3m, 3e ≥ m), would
        imply Wilf. Its 3e < m boundary campaign is E284/ck3.
      - PACK, PACK-A, PW0′ are FALSE. PACK-W is false by implication. Deficit form, Lemma W0 and the layer-1 identity
        are PROVED (PROOFS).
    - Tool: src/scratch/p18/chain_kunz.c is a Kunz-coordinate annealer, the only one of our searches that reaches
      large e at depth ≥ 4.
    - NEXT: P11 (codex) = close c ≤ 4m, i.e. the residual α ≥ 6, 19 ≤ a < 10·C(α+1,2), 3e < m, q = 4. Tools: CHAIN at
      q = 4 (0 failures so far, slack ≥ 2.5 in the residual), RC reformulations, the GW-26 framework.
    - **P11 LAUNCHED 2026-10-19** (message $SP/codex/p11_msg.md, log $SP/codex/p11_log.txt; report will be
      src/scratch/gw/p11/P11_REPORT.md). The lead meanwhile stress-tests CHAIN-WILF(3e<m): at m = 61 the boundary
      campaign reached ratio 1.08 (e = 16, q = 5). Thin-basis level-2 families (m = 60, 90): min 1.41, no failure.
(0L) NEW 2026-10-19 latest+++, read first.
    - **Codex P9 REVIEWED and accepted** (PROOFS "Codex P9", E279: own code, exhaustive m ≤ 15 + 11.7k random + sympy;
      0 failures). Problem 1.8 criteria:
      - PAIR-SPAN12: 12a ≤ e|2B∩[0,m)| ⇒ Wilf;
      - SUMSET-MODULUS: T_j = e(|jB|−1) > 2ja and m ≥ 2jβ(T_j+3a)/(T_j−2ja) ⇒ Wilf. For fixed B this gives all
        m ≥ C_B·β (linear in the span);
      - explicit carried Sidon classes ET-31 and ET-2.
      Open: the large-span, near-free core (β ≈ m, k ≪ √m). Codex's next lemma: the pair gain at modulus m + β without
      m > 3β.
    - E278: on e = 5, q ≥ 5 the band criteria cover ≤ 3%, since every band tool is linear growth.
    - The carry-free upper growth u_{t+1} ≤ u_t + μ_d(u_t) holds for every S but is vacuous alone (NOTEBOOK latest+++++).
    - NEXT: codex P10 = e = 5 (see $SP/codex/p10_msg.md). The lead works on VOL-MINK: cube volume (Prop VOL) +
      Minkowski on the inscribed simplex + a corner lemma, aiming at Wilf for c ≥ K_e·(m + Σn_i) for every e.
(0K) NEW 2026-10-19 latest++, read first.
    - PRIORITY: Yang–Zhang (Preprints.org 202604.0551, Apr 2026) contains LK (a). Their staircase bound is
      ℓ ≥ q + (q−2)η + η_ρ. LK (b), the Kneser growth, remains ours; combined as Theorem LK+YZ (PROOFS, E272).
      Literature checks must now include Preprints.org.
    - Macaulay on bands is FALSE with carries (E273). In P18, W = W_0, and Wilf ⟺ (k+1)Σ_{i<q}(q−i)α_i ≥ qm − ρ (Eliahou's
      α_i). The obstruction is the ±1 carry.
    - Codex P8 REVIEWED and accepted (PROOFS "Codex P8", E274): SR packing lemma; GENERAL-FEW21+240; SHADOW-225; DISJOINT-CUBICS.
    - LEAN: YZ staircase (any m ∈ S) and LK+YZ (prime m) kernel-checked (`ell_ge_staircase`, `ell_ge_lkyz_prime`, `'`).
    - NEW band lemmas (PROOFS; exhaustive genus ≤ 33):
      - LK-SUPER (E275): Kneser from every band j; prime m ⇒ Θ_{a+b+1} ≥ Θ_a + Θ_b. It covers deep S with an empty first
        layer, beyond all first-layer methods. Lean: `shift_mem_band`, `card_bandGaps_step_band`, `band_superadditive`.
      - LK-SHARP (E276): the wrap only reaches the window [m − β_j, m), so g_H + a_H ≥ g_{H+j} + δ_j. Growth per j bands at
        a one-time cost β_j.
    - LEAN: P8's SYMMETRIC-RECTANGLE kernel-checked (lean/Wilf/SymRect.lean).
    - Strategic note: every band/Kneser result is a LOWER growth bound, at most linear in the depth. The Wilf-tight
      profiles (free / B_h-like B) grow polynomially and are shallow. The missing ingredient for P18 and for general S is
      an UPPER growth (carry-corrected Macaulay) principle. That is the P9 target (b).
    - c ≤ 4m frontier + YZ Cor 4.2: the residual (α ≥ 5, 19 ≤ a < 10·C(α+1,2)) also needs (a+1)(a+2) < 2m, so m ≥ 211.
    - Codex P9 launched: Problem 1.8 (generators < 2m). Message $SP/codex/p9_msg.md, log $SP/codex/p9_log.txt.
(0J) 2026-10-19 latest+.
    - **Theorem LAYER-KNESER (PROVED, PROOFS).** For every S: ℓ ≥ D + (D−2)k, where k = |S∩(m,2m)| and D = ⌈c/m⌉.
      If moreover gcd(m, B) = 1, then ℓ ≥ D + (D−2)k + δ⌊(D−3)²/4⌋, with δ = ⌈(k+1)/2⌉ (k for m prime).
      - Method: Kneser on the band gap sets, G_{H+2} − B ⊆ G_H.
      - It strictly contains Delgado–Kumar–Marion Thm 1.5 (arXiv 2501.04417v3) and gives Wilf for D ≳ 8m/(k+1)².
      - Exhaustive check genus ≤ 33 (E271).
      - It settles the deep (slow-growth) part of their open Problem 1.8 (all generators < 2m).
    - Next for this line:
      - (i) DONE: Lean kernel-checked (lean/Wilf/LayerKneser.lean). Covers part (a) and the prime-m case, for any m ∈ S
        (not only the multiplicity). The general-m Kneser case is paper only.
      - (ii) The fast-growth remainder of Problem 1.8 (4 ≤ D ≲ 8m/k²), via an inverse-theorem (Freiman/Vosper)
        dichotomy.
      - (iii) Whether the band-Kneser growth combines with the MaxCL/HCR machinery for general S.
    - Codex P8 (height-3 MaxCL, many-cubic regime) is RUNNING (log $SP/codex/p8_log.txt; waiter on PID 94093).
(0I) NEW 2026-10-19 latest, read first.
    - **H1′ is FALSE** (codex P7; lead re-check E269; examples/h1prime_sidon_counterexample.md). An infinite height-3
      WRAP-MAX family built from a Sidon set has (S − Λ_r)/m = −536, at the conductor phase of an actual semigroup.
      MaxCL and Wilf hold on it. With E47, E266 and E268, every boundary-only (pure-counting) strengthening of MaxCL
      is false, so any MaxCL proof must spend Λ_r.
    - Advisor's bar for the next round (2026-10-19): prove H1′ beyond the first threshold (now moot: refuted), extend
      H-FEW40 to its complementary regime, or close a genuinely new infinite class. Identities and larger censuses do
      not count.
    - Side results this cycle, all negative (NOTEBOOK latest):
      - H-SF (Tile-CL on spike-free tiles) is FALSE (E268).
      - The 3-D Ω trend does not decay (E267), so the OMEGA route is dropped.
      - The run and per-direction decompositions of H1′ fail (E270).
    - **Next:** codex P8 = the height-3 complement of GENERAL-FEW40 (many cubics: k < 40t + 8). Height-3 MaxCL is the
      hub: it gives Wilf for every height-≤3 Apéry set and reduces P_4 (3m < c ≤ 4m) to the quartic rows. The lead
      works on the additive-combinatorics structure of the cubic face (3U versus 2U with distinct labels; the
      dimension count d + 1 = m − Q − t).
(0H) NEW 2026-10-19 late night, read first.
    - **Codex P6e received** (77e27a7; PROOFS "Codex P6e"; E265). BAD-TWO is lead-checked. ORIGIN-EDGE, GENERAL-FEW40
      and H-FEW40 (all heights: HC_H when k ≥ 40B + 8) are codex-proved and NOT yet re-derived by the lead.
      The height-3 line is PAUSED: five codex rounds, with the residual family shrinking but no closing mechanism.
    - **WRAP-MAX pure counting H1′ (CONJ, strong evidence; NOTEBOOK "night, late"; E264).**
      - Statement: on every tile whose canonical lift has v < m on non-maximal cells, S(σ) ≥ Λ_r(σ) at every phase.
      - Equivalent window form: d|W| ≤ T(W) + Σ_V(|y|−1) for every top label window W.
      - Evidence: 0 failures on all 4-D tiles with m ≤ 26 and on 64k random instances (d ≤ 9).
      - If proved, it gives MaxCL for WRAP-MAX, which contains Flat (height ≤ 2) and NO-WRAP. Both cases are already
        proved; θ = min P is also PROVED (translation by the smallest step).
      - FALSE neighbours, preserved: the sufficient forms without Σ_{λ≥θ}(|y|−1) (m = 17 example); PC on all tiles
        (E47 at ρ_0 = 0); H1′ on partial structures (incomplete labels).
    - **Codex P7 RUNNING** (session 01a1525d; message $SP/codex/p7_msg.md; log $SP/codex/p7_log.txt; waiter on PID
      83952; report src/scratch/gw/p7/P7_REPORT.md).
      - Task: prove or refute H1′ at every height; then the Wilf corollary; then the one-wrap generalization with Λ_r.
      - After it ends: review, verify, commit. Tell codex that H1′ fails for partial structures (it may find this
        itself) and give it the θ = min P proof.
    - Deep-slack identity (checked on 2,778 S): S_W/m = eℓ − c + Λ_r/m − Σ_x T(x)G(x), where G(x) is the number of left
      elements in the class of w(x). So Wilf ⟺ S_W ≥ −Θ with Θ = Σ_{t∈N} T(t)(c − w(t)) + m·Σ_{A, w<c} T(y)G(y). This is
      CH′ reorganized, not a new inequality.
(0G) NEW 2026-10-19 night, read first.
    - **Codex P6c and P6d accepted** (d699d04, 0ca1a29; PROOFS "Codex P6c", "Codex P6d"; E258, E261).
      - ONE-CUBIC: HC′ ≥ 0 and MaxCL at every phase for every height-3 tile with exactly one cubic. Hence Wilf for every
        S with a factorization tile of height ≤ 3 and ≤ 1 cubic.
      - BAD-NARROW (ρ = 0, core units in (m/2, 2m/3)), GENERAL-SHAPE, ONE-BAD-SHAPE.
      - WINDOW-H: exact all-height identity with local loss (j−2)m. The lead re-implemented it independently on
        heights 2–19.
      - Remaining at height 3: t ≥ 2 bad cubics, k ≥ 5, d ≥ 6. Next lemma: HIGH-ORIGIN.
    - **Codex P6e RUNNING** (same session 01a1525d; message $SP/codex/p6e_msg.md; log $SP/codex/p6e_log.txt; waiter
      on PID 70732; report src/scratch/gw/p6/P6E_REPORT.md).
      - Order: HIGH-ORIGIN; then the origin phase with one low factor; then general phases t ≥ 2; then a short note on
        which tools scale under WINDOW-H.
      - After it ends: review, commit, then decide P6f vs Lean (NO-WRAP and ONE-CUBIC) vs P5h.
    - **Lead, general height** (PROOFS "Column form for any lift, and phase-free NO-WRAP"; E260):
      - Phase-free NO-WRAP is PROVED: x·P < m on D ⇒ MaxCL at every σ. The elementary proof is ready for Lean.
      - Corollary: Wilf when every Apéry element w_i has a factorization with residue sum exactly i.
      - Exact cell form at any height; WRAP-MAX target (only maximal cells wrap). Pure-counting H1 is FALSE (m = 17).
      - Single-flip WRAP-DESCENT is FALSE.
      - Literature search 2026-10-19 night (LITERATURE.md) found no prior statement of these classes.
    - Lean queue (one agent at a time): NO-WRAP MaxCL ⇒ Wilf corollary (small), then ONE-CUBIC (large).
(0F) NEW 2026-10-19 late evening, read first.
    - **Codex P6b accepted** (bcce63c; PROOFS "Height-3 MaxCL: partial results"; lead re-check E256).
      - New proved classes, at every σ with any spikes:
        - DENSE075: ε ≤ ⌊3k²/40⌋;
        - DENSE9: complete face, ε ≤ ⌊k²/9⌋;
        - THREE-CUBICS: complete face, t ≤ 3;
        - FEW-CUBICS: complete face, k ≥ 19, t ≤ ⌊k²/16⌋.
      - Tools: ROW-PACK, SHADOW-COVER, FLAT-CR.
      - Remaining: k ≥ 5, d ≥ 6, CR < 0, FLAT-CR < 0, outside those classes.
    - **Codex P6c RUNNING.**
      - Session 01a1525d; message $SP/codex/p6c_msg.md; log $SP/codex/p6c_log.txt; fejer ~/wilf/p6c; report
        src/scratch/gw/p6/P6C_REPORT.md.
      - Task: the k ≥ 5 middle family, via partial-row packing, B-COVER/SINGLE-COVER, or HC′ at the near-flat end.
      - Also: which tools generalize to height H.
      - After it ends: review, commit, then decide P6d vs P5h (draft $SP/codex/p5h_draft.md).
    - **Lead annealers** (E257; src/scratch/h3/anneal_h3.c, src/scratch/hh/anneal_hh.c).
      - No MaxCL or HC′ violation at height 3 (K = 5..8, m ≤ 60), nor at heights 4–5 (K = 4..7, m ≤ 60).
      - The middle family is realizable but loose (normalized slack 0.19–0.46 for t ≥ 2). MaxCL is tight only at the
        near-flat end, e.g. flat + one pure-power column.
      - Spike bonus is sharp: β < 1 fails already at k = 1.
      - Unpaid examples for codex: examples/h3_middle_family_unpaid.md (when written).
    - **Per-α sweeps α = 6, 7 stopped** (diverging). Counts are in the NOTEBOOK, 2026-10-19 late evening. α = 6 falls
      after a = 25; restart at a = 28 if needed.
    - Growth / sumset line assessed and NOT pursued: the elementary Freiman bound is of the same kind as the known
      Macaulay results. NOTEBOOK.
(0E) NEW 2026-10-19 evening, read first.
    - **Codex P6 (accepted):**
      - H3-D5: MaxCL for every height-≤3 tile with d ≤ 5, by finite certificate. The lead's independent DFS
        enumerator reproduces every count for d ≤ 5, with 0 failures on 7.67M height-3 tiles (E249).
      - Hence H3-E6: Wilf for height-3 Apéry sets with e ≤ 6.
      - Also H3-CORE2 (k ≤ 2 non-maximal units, any number of spikes), PAIR-ZERO, CENTERED-PAIR, UNIT-LOAD-0.
      - Remaining: d ≥ 6, k ≥ 3 (PROOFS "Height-3 MaxCL: partial results").
    - **Codex P6b RUNNING** (log $SP/codex/p6b_log.txt; report src/scratch/gw/p6/P6B_REPORT.md): that remaining
      family.
    - **Lead (later): H3-CORE3 and H3-CORE4.**
      - Height-3 MaxCL is proved, computer-assisted, for every tile with ≤ 4 non-maximal units and any number of
        spikes: CR for all but finitely many (core, s), plus an exhaustive check of those (E250, E252).
      - Remaining: k ≥ 5 and d ≥ 6.
    - **Lead: the bound HC′.**
      - S = HC′ + m·P_A^+, where HC′ is the flat window applied to maximal pairs only.
      - HC′ ≥ 0 at every phase on every injective labeling of every k = 3 core (s ≤ 14) and k = 4 core (s ≤ 2), and
        on about 7,000 random tiles (E254, E255). This is a candidate target that removes maximal pairs.
    - Middle regime: CR needs only m − |C| ≥ (2/9)θ²k² there (t = θ·C(k+2,3)).
    - Diagnosis: local carry accounting alone cannot work; it must be coupled with distinctness/packing.
    - Lead tools sent to codex:
      - the spike reduction MaxCL ⟺ IMaxCL;
      - the CR rearrangement bound (proves almost every tile; L-CR3 FALSE, because of maximal pairs);
      - cyclic a+b−c packing (NOTEBOOK 2026-10-19 evening; E244–E248).
    - **GW-26i: α = 5 CLOSED for every a** (sweep a = 19..149, 0 survivors). The primary regime is proved for α ≤ 5.
    - Per-α sweeps (fejer ~/wilf/lead23, al_sweep2.sh).
      - The binary now has the quartic face cap k1 ≤ p·u0 (q1cap=1 in lines after 13:03 UTC) and counts
        withquartic.
      - α = 8, a = 19: 58 survivors, only 1 with a quartic.
      - So after full height-3 MaxCL, P4 reduces to the quartic rows only.
    - e = 5: CR has 0 failures on all 4-D tiles for m = 35–39, but its minimum ratio ≈ 1.0–1.08. Height-≤3 4-D
      tiles end at m = 25, so e = 5 needs CR/HCR for near-simplices of every height (E247).
(0) 2026-10-19 late afternoon.
    - **Convergence (proved reduction).** In the primary regime every height-4 cell is an A-quartic. So quartic-free
      primary tiles have Apéry height ≤ 3, and height-3 MaxCL (codex P6, RUNNING) would close every quartic-free
      profile: BASE and all α = 6/8 residual rows (u0 = u1 = 0 ⇒ no A-quartic; the printed `k` there is the LINK
      pair-cover number, not the quartic count). The P4 remainder after P6 would be the profiles with ≥ 1 A-quartic only.
    - Per-α closure with the fixed and fast certificate (E242):
      - α = 5 is clean so far (to a = 149; finish, then record "primary regime for α ≤ 5").
      - **α = 6, a = 20: 3 B-loop survivors.**
      - **α = 8, a = 19: 61 and a = 20: 781 matching-type survivors.**
      - So the current relaxation cannot close α ≥ 6. Survivor dumps: fejer ~/wilf/lead23/surv_a19_al8.log and
        surv_a20_al6.log (all fields, δ ranges). Sweeps of α = 6, 7, 8 continue (al_sweep_{6,7,8}f.log).
    - P5h draft: $SP/codex/p5h_draft.md. Send after reviewing P5g §60+. Task: close these finite residual families
      using localized defects or retained pairs, or realize one as a residue-complete down-set.
    - Bug fixed: the kE/klist[64] truncation. Never fired (krange>64 = 0 everywhere), so GW-26g and GW-26h stand.
      The fast build is 18× faster with identical output (E242).
    - Height-3 MaxCL (own line), all in PROOFS "Column-top lemma and the carry form of MaxCL":
      - column-top lemma, Lean-checked (lean/Wilf/ColumnTop.lean);
      - carry form at any height, and unit form at height 3;
      - margin data: lin/(−m·Br) ≥ 1.457, worst at ρ_0 ≈ m;
      - postage-stamp bases are the no-wrap tight family.
      Next: an adaptively-based charging proof of the height-3 carry inequality (or hand it to P6).
    - Laptop disk was briefly full (ENOSPC around 08:05 local). Codex's rollout writes failed and were then retried.
      About 9.7 GB is now free. ~/.codex is 19 GB, repo .claude 7.5 GB, local lean/.lake 7.5 GB (unused: Lean runs on
      fejer). Ask the user before deleting anything.
(a) Codex P5g is RUNNING (session 01a1525d-16ff-7fc2-a405-17a585c3ec31; message scratchpad codex/p5g_msg.md; log
    codex/p5g_log.txt; report P5_REPORT §60 onward). Task: ambient packing. In order:
    - P(C) with O(n²) error (any explicit C < 130 kills BASE), then the zero-error P(C†) for n ≥ 33;
    - MATCH-P (§59) and the B-loop variant;
    - what each closes;
    - or explicit counterexample families.
    Lead data sent with it: C*(9) = 107/19, annealing ≈ 5.2 for n ≤ 48, the end-loaded t^{1/3} extremal structure.
(a′) Lead, per-α closure (fejer ~/wilf/lead23; lead_t2small_g with flags MLPEHG and α restriction).
    - α = 4 is done (GW-26h).
    - α = 5..8 are next, over a ∈ [19, a0_coupled) with a0_coupled = 62, 84, 109, ~135. Above a0_coupled, the coupled
      check (coupled_large_a.py, exact per (α, a)) closes [a0, 10R0), and LARGE-A′ closes a ≥ 10R0.
    - The slow part is small a < 1 + 2α + R0, where the GLOC b coefficient can be negative and the early cap does not
      apply. α = 5 timings are in al5_time.log.
(b) Lead, G-ID line (PROOFS GW-27 and NOTEBOOK 2026-10-19 midday):
    - Exact cell identity W = Σ λφ + Σ x_aβ_{x,a} − Σ γ for every residue-complete down-set.
    - Deficient cells (c_x < 0) are almost all top cells with residue ≤ μ, in every degree (E220).
    - WQ (units + window (μ, 2μ] pay all deficits) holds for all e ≥ 4, genus ≤ 30, but is FALSE in general. It fails
      for cubic and higher D at μ ≈ m − 1 or μ ≈ 1, where pairs with λ ≥ 1 pay. Next: the cubic case (Wilf for
      4n_1 > c + m) with window + lower-cover payments.
(c) Lean, queued after P5b (one agent at a time): GW-19/GW-25 (GW-27 needs no Lean work: its semigroup form is already
    `wilf_of_apery_height_le_two`).
(d) Background: the gfan re-check of E153 is COMPLETE for m ≤ 39 (E160): an independent second enumeration agrees, so
    Wilf for e = 5 with m ≤ 39 rests on two independent enumerations. The codex HT4 subclass claims are still unverified.
