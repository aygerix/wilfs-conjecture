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
2. Height criterion: (m+1)H(D) ≤ mW + m(m−1), so δ ≥ 0 ⇒ Wilf. PROVED on paper (NOTEBOOK night 13).
   Per-tile LP certificate (src/tile_lp.py) for tiles with δ < 0.
3. Two-face tiles ⇒ Wilf. PROVED (paper + exact finite check m ∈ [18, 74]).
4. Non-two-face tiles lie in 𝒞 (Loomis–Whitney) or the cone class Cyl ∖ (q + ℕ³). PROVED (cylinder lemma; (b) is HRW Prop 2.6).
5. 𝒞 tiles: δ ≥ m + 14 − 5C, so HT for m ≥ 131 (Theorem C-HT). PROVED on paper.
6. Cone tiles: δ ≥ m − 6C − 29, so HT for m ≥ 281. PROVED on paper 2026-10-18.
   Ingredients: Lemma CHT, TF-cone, F-cone, qO-cone (Fiber Lemma), T′ (t ≤ C), B (C ≤ 3/2 + √(6m − 15/4)).
   Lattice input: only |Y| ≤ 6, via the Floor Lemma.
7. Finite range, by complete computer enumeration of tiles (tile_scan, Python + C port):
   - All non-two-face tiles m ≤ 130: HT 0 failures except m ∈ {8, 15, 16, 17, 19, 20, 23}, which are LP-certified.
     The gaps m = 90, 100, 108, 114, 115 were closed on 2026-10-18 (logs/tile_scan_C_gaps.log).
   - m = 131–280: RUNNING (logs/tile_scan_C_131_280.log, private MAXM-300 build of src/c/tile_scan.c). HT 0 failures through m = 170.
   When it finishes, every e = 4 semigroup is covered by links 1–7, subject to the review below.
- Independent adversarial review of links 5–6 (subagent, report → $SP/review/cone_review.md): RUNNING.
- In Lean (2026-10-18, lean/Wilf/CornerArea.lean, verified by the lead): Lemma B (`cornerArea`, any finite down-set),
  Lemma CHT (`cht`, any finite D), Lemma T (`typeBound`, class 𝒞). So the sublinear bound t ≤ C − 2 ≤ √(6m) on 𝒞 is
  kernel-checked. NOT in Lean: T′ (cone class), the forest lemmas (TF, F, QF, TF-cone, F-cone, qO-cone), Wall/Floor, links 2–4
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
- G-scan: finish HT for cone tiles with 131 ≤ m ≤ 280 (running). If an HT failure appears, LP-certify it with tile_lp.py
  (as for m ≤ 23).
- G-review: the adversarial review of TF-cone, F-cone, qO-cone, T′, B and the threshold arithmetic.
- G-Lean: CHT, T and B are done. Next: T′ (cone class), then the forest lemmas, then Wall/Floor and the height criterion (link 2).
- G-second-check: a method-independent second enumeration for m ≤ 280, or a reduction of the finite range by a sharper
  constant (e.g. LHS ≤ 5C + β ⇒ threshold ≈ 160).

## Three active approaches
1. **e = 4 tile route (current).** Close G-scan and G-review, write the self-contained manuscript of our e = 4 proof,
   and start G-Lean with Lemma CHT + Lemma T + Lemma B.
2. **Tiles in dimension d = e − 1 ≥ 4.** Which links generalize? Link 2 (a height criterion for e ≥ 5), the cylinder
   structure and the floor/wall lemmas in ℕ^d. First task: state the e = 5 analogue of the height criterion and test it
   on 4-D tiles with m ≤ 20.
3. **All-e final-window criteria (parked).** FWx-deep (FWx ≥ 0 when c > 3m), combined with Eliahou, would give Wilf.
   Next step when unparked: bound Σ_final R_j(L) through the residues [r a_j]_m.

## Next precise task
When the scan finishes: read logs/tile_scan_C_131_280.log and confirm "HT fails 0" for every m = 131..280. Record E136.
Read the review report and repair any gap it finds. Then write the e = 4 manuscript (.research/E4_MANUSCRIPT.md) with
every link and its status, and reassess with the advisor (budget ends 2026-10-19/20).
