# Referee report: e = 4 tile route, links 1, 2, 3, 4, 5 (C-HT), 6 (finite computation)

Referee scope: everything except the cone-tile lemmas (TF-cone, F-cone, QF-pair, Fiber, qO-cone, T', B), which another
referee has. Project read only; all code and logs are in this directory (paths at the end).
Scratch = /private/tmp/claude-501/-Users-jmercedes-Desktop-Projects-Research-wilfs-conjecture/01462dfe-b5df-469d-99d1-f1cc96de9daa/scratchpad/review2

## Summary of verdicts

| Link | Verdict | Basis |
|---|---|---|
| 1 Factorization down-set / tile | CORRECT (Lean reference points to the wrong file, see 1) | argument + computation |
| 2 Height criterion | CORRECT; it can be sharpened to H ≥ m − 2 | argument + computation |
| 3 Two-face theorem (finite part m ∈ [18,74]) | CORRECT, given Eliahou (c ≤ 3m), BGOW (m ≤ 18) and the Lean τ-criterion | argument; finite part rerun independently |
| 4 Cylinder lemma / exhaustiveness | CORRECT; "two-face" is defined the same way everywhere | argument + computation |
| 5 Theorem C-HT (𝒞, m ≥ 131) | CORRECT (uses Lemma B, now in Lean) | argument + exhaustive check |
| 6 Finite computation | CORRECT as a method, with three gaps (G6a–G6c) | code read + independent checks |

No counterexample was found to any claim in my scope.

## Per-link findings

### Link 1: factorization down-set D, tile property, CH'
- Checked by argument. For any monomial order: |D| = m. The map φ = r·x mod m is a bijection D → ℤ/m, so D is a
  set of coset representatives of Λ = ker φ, and Λ has index m because gcd(m, p) = 1. D is a down-set by summand
  closure plus compatibility of the order with addition. Each e_a ∈ D, because a minimal generator has only one
  factorization over P'. CH' gives Σ_a Σ_C |C|(M − w(top C)) = 3mM − 4ΣAp = mW + m(m−1) when d = 3.
- **Lean statement mismatch (not a math gap).** `lean/Wilf/TileReduction.lean: isTile_factDownSet` is about
  `factDownSet`, which is built from `nf`, the **lex**-least factorization (`toLex`, Carry.lean l.197). The e = 4
  chain uses the **grlex** tile. The grlex facts are in Lean, but in a different file:
  - `MaxCL.lean: isFactTile_factDownSetG`;
  - `IsFactTile.isTile` (so `IsTile factDownSetG genMod`);
  - `IsFactTile.columnIdentity` (CH' for any factorization tile).

  Cite those instead. Note also that `IsTile` = down-set ∧ |D| = m ∧ BijOn φ D ℤ/m. This matches what the paper uses.
- **Not in Lean, though the chain uses them** (all elementary):
  - (c) e_a ∈ D;
  - D is a fundamental domain in ℤ³ (used by the cylinder lemma);
  - closed-cone membership: for every minimal non-element q, p·q ≥ p·rep(q), because p·q ∈ S lies in the class of
    the Apéry element p·rep(q). The LP certificate and the coverage argument of the scan both rely on this.
- Checked by computation, with asserts on every e = 4 semigroup in the tests below (≈ 50,000):
  - down-set, |D| = m, e_a ∈ D, w-values = Ap;
  - CH' as an exact identity;
  - c, g, ℓ cross-checked by an independent membership sieve (m ≤ 25, generators < 40m).

### Link 2: height criterion (m+1)·H(D) ≤ mW + m(m−1)
- Checked by argument.
  - For a top t and any y ≥ t in D: M − w(t) ≥ w(y) − w(t) = p·(y − t) ≥ (m+1)|y − t|, since p_a ≥ m + 1.
  - Summing over the 3m incidences (x, a) gives Def_all ≥ (m+1)H, and CH' says Def_all = mW + m(m−1).
  - The direction is right: H ≥ m−1 ⇒ mW ≥ m−1 > 0.
  - Code: H_of in heightH.py and the C ht/top arrays compute exactly H = Σ_{x,a} ht(top_a x), with ht = longest
    unit up-chain (= max|y − t|, since D is a down-set).
  - W, c, ℓ through D: M = max_{x∈D} p·x, c = M − m + 1, g = Σ_{x∈D} ⌊p·x/m⌋.
- **Sharpening (free).** W is an integer, so (m+1)H > m(m−2) already gives W ≥ 0. Hence **H ≥ m − 2 (δ ≥ −1) ⇒
  Wilf** for m ≥ 3. Consequences:
  - the m = 17 and m = 23 HT-failing tiles (δ = −1) no longer need the LP;
  - C-HT closes at m ≥ 130 instead of 131 (5C ≤ m + 15; the last failing m is 129).
- Minor: the docstring of src/scratch/heightH.py claims "deficit ≥ (m+1)|y−t| + 1" and "Def_all ≥ (m+1)H + 3m".
  - The "+1" is false for every S: incidences whose top is the Apéry maximum have deficit 0.
  - The aggregate "+3m" never failed in about 50,000 tests, but it is unproved.
  - It is not used in the chain. Correct the docstring.
- Checked by computation: asserted on every tested e = 4 semigroup, 0 failures.

### Link 3: THEOREM (two-face e = 4)
- Checked by argument. I re-derived:
  - the two-face identity, in both forms. This is pure algebra: CH' in the form 3mM − 4ΣD w, plus the AP sums over
    the 2m + L₃ runs.
  - F1 (including x_i ≤ L₃ − x_ax), F2, F3 (crosses meet once, never three at a time), F4 and F5.
  - Each of the bounds A′, B″, C, D, including:
    - the max(0, ·) relaxations;
    - the requirements c > 3m (M ≥ 4m) for A′ and p_c ≥ m+1;
    - the constraints H_i ≥ 1 (e_a ∈ D) and H₁ + H₂ ≤ m − L₃.
- Bound C is the Lean τ-criterion `wilf_of_tauCriterion_P2` with e = 4.
  - It uses `nfG` (grlex), the same D as the theorem.
  - `topPairs2` counts ordered pairs, so the hypothesis 4τ + 2P₂ ≤ 2(m+1) is exactly m + 1 ≥ 2τ + P₂.
- tf_bounds2.py is a faithful encoding.
  - It checks the strictly stronger statement "one bound for all feasible tuples".
  - Its feasible set (joint x₁(x₁+1)/2 + x₂(x₂+1)/2 ≤ m − L₃, τ = 0 allowed) is a superset, so the check is sound.
- Analytic tail, re-derived independently:
  - (I) L₃ ≤ m/4: A′ with Def2D ≥ 0 alone needs m + 2L₃² − 18L₃ + 3 ≥ 0, true for m ≥ 37;
  - (II) m/4 < L₃ ≤ m/2 − 4: B″ with Def2D′ ≥ 0, concave in L₃; the endpoints need m ≥ 27 and m ≥ 35;
  - (III) L₃ > m/2 − 4: C, since 2τ + P₂ ≤ cap + 2.5s + 2 with s ≤ 2√cap and cap < m/2 + 4; this needs m ≥ 75.
  - So every (m, L₃) with m ≥ 75 is covered.
- Checked by computation:
  - **Independent rerun of the finite part** (tf_check.py, m = 5…500, both the single-bound and the per-tuple
    quantifier). The only uncovered (m, L₃) have m ≤ 17, and the list equals logs/tf_bounds2.log exactly.
  - **On real semigroups**: about 16,800 two-face semigroups (random, m 19–130) plus all 1,555 two-face e = 4
    semigroups of genus ≤ 20. Every one of the above inequalities was asserted, and each semigroup's actual tuple was
    covered by Eliahou, BGOW, A′, B″, C or D. 0 failures, 0 uncovered.
- External dependencies, both genuinely needed:
  - Eliahou JEMS 2018 (c ≤ 3m), for region I when c ≤ 3m;
  - BGOW IJAC 2020 Thm 4.3 (m ≤ 18): two-face (m, L₃) pairs remain uncovered for m ≤ 17 (e.g. m = 15, L₃ = 4), and
    the m = 8 non-two-face tile is not LP-certified (κ = 4 < 56/9).

  These are verified results by citation only; I did not re-check them.

### Link 4: cylinder lemma; every non-two-face tile is in 𝒞 or in Cyl ∖ (q + ℕ³)
- Checked by argument.
  - (a): q ∈ G lies in D + λ with λ ≠ 0, and (q − λ)_a = 0 on supp q. Full support gives q ∈ Λ. Two such q would
    put two cells of one class in D.
  - (b): the same argument with q − λ = t·e_c.
  - (c): x ∉ D ⇔ x ≥ q for some q ∈ G; if q_c = 0 this is π_c(x) ∉ π_c(D).
- Hence D = Cyl ∖ (q* + ℕ³), or D = Cyl when there is no q*.
  - Cyl = {x₂ < h(x₁), x₃ < min(F(x₁), G(x₂))} is exactly class 𝒞, with h(0) = L₂, F(0) = G(0) = L₃ and F ≥ 1 on
    dom h.
  - q* ≥ (1,1,1) and q* ∈ Cyl, because π_c(q*) = π_c(q* − e_c) ∈ π_c(D).
  - So the dichotomy is exhaustive.
  - Two-face tiles have no q*, because a full-support q dominates e_a + e_b. They are therefore all in 𝒞.
- "Two-face" means "e_a + e_b ∉ D for some pair" in link 3, in PROOFS (iv), in tile_scan_H/HM.py (line 14/15) and in
  tile_scan.c `stats()`. The scan analyses exactly the tiles containing all three e_a + e_b. **Consistent.**
- Checked by computation: classification asserted on every tested non-two-face tile.
  - Random tests: 24,707 in 𝒞 and 8,734 cone, 0 "other".
  - Genus ≤ 20: 39 in 𝒞 and 30 cone.
  - Every two-face tile was in 𝒞.
- Minor: STATE says "(b) is HRW Prop 2.6", while PROOFS says "(a) [HRW Prop 2.6(b)]". Make the attribution
  consistent.

### Link 5: Theorem C-HT (𝒞 tiles, m ≥ 131)
- Checked by argument, line by line:
  - Lemma CHT: {h = 0} = Max ⊔ Tri, {h = 1} = Q′, δ = 1 + Σ(h − 1).
  - Level picture (i), (ii).
  - Lemma T: telescoping |M_v| = κ(U_v) − κ(U_{v+1}) + ν_v with ν_v ≤ [a drops] + [b drops]; the drop values are the
    values of F, G other than L₃.
  - (P0) and (P1).
  - Lemma S: the three projections force y + e_c ∈ D.
  - Lemma P: the strict chain F(X′) ≤ F(X+1) < G(Y) ≤ G(Y′+1) < F(X′).
  - Lemma TF: by Lemmas S and P, at most one of x's three distinct tops is old; 3 + 2(|Tri| − 1) ≤ t.
  - Lemma QF: all four sub-cases of (1)/(2), including c′ = 2 via (P0) at p′ + e₁ ≤ p and c′ = 3 via (P1).
  - Lemma F (qU forest):
    - c = 3 edges join consecutive corners of one M_v;
    - c = 1 (resp. c = 2) edges have their upper end at the leftmost (resp. rightmost) corner of U_{v+1}, at most one
      of each per level;
    - a cycle needs e_L and e_R on one c = 3 path of M_v, which is impossible: the crossing notch
      (a_{v+1} − 1, b_{v+1} − 1) lies in U_{v+1}, and a corner that is both "top" and "right" forces R_{v+1} ⊆ U_v,
      which kills e_L.
  - Lemma B: inclusion–exclusion of the faces, arms + triangle, convexity of T(k).
  - Totals: LHS ≤ 2t + 3(t − 1) ≤ 5C − 13, so δ ≥ m + 14 − 5C.
- Lean now has CHT, B and T (CornerArea.lean). The statements match the paper:
  - `cht`: 2|D| ≤ Σh + 2t + 2|Tri| + |Q′|;
  - `cornerArea`: C² + 6 ≤ 6m + 3C;
  - `typeBound`: t + 2 ≤ C under `LWClass`.
- Threshold arithmetic, checked exactly:
  - Cmax(m) = the largest integer C with C² − 3C + 6 ≤ 6m = ⌊3/2 + √(6m − 15/4)⌋ (checked for m < 2·10⁴).
  - 5·Cmax(m) ≤ m + 14 for every 131 ≤ m ≤ 2·10⁵; it fails at m = 130.
  - For m ≥ 160: m − 5√(6m) is increasing (m ≥ 38), and 5(1.5 + √(6m)) − 14 ≤ m holds with slack ≥ 11.5 there.
- Checked by computation:
  - **every** down-set |D| ≤ 20 (198,832 sets; 123,072 in 𝒞, 72,307 cone, lattice-free): CHT, B, T, TF, F, QF on 𝒞
    and T′ on the cone class all hold;
  - all tested tile instances satisfy δ ≥ m + 14 − 5C.

### Link 6: role of the finite computation
**What the code checks.** For each m:
1. It enumerates one residue triple per lattice up to units and permutations: sorted, distinct, nonzero,
   gcd(r, m) = 1, lexicographically minimal among sorted(u·r).
2. For each lattice, a facet-flip DFS over the Gröbner fan of I_Λ in the positive simplex lists every tile of every
   open cone.
   - The cone is {p : p·(q − rep q) > 0 over minimal non-elements q}. Correct: for p in it, reduction n → n − q + rep q
     terminates in D.
   - A flip must land in a cone whose closure contains the edge midpoint; otherwise the program exits or asserts.
3. For each tile containing all e_a + e_b, it computes H and reports δ < 0.
4. The Python version passes each failure to tile_lp with that lattice's own closed cone polygon (the C version
   prints the failure for later LP).

**Coverage.** Let S have e = 4, m ≤ M, and a non-two-face grlex tile D.
- D is the standard set of the term order (p, degree, lex). That order is a generic weight in an open cone adjacent
  to p, so D is an open-cone tile of Λ_{r(S)}.
- After a unit u and a permutation σ, it is an open-cone tile of the canonical lattice.
- HT and two-face are invariant under σ. κ is invariant under u, which does not change Λ, and is equivariant under σ.
- So "HT fails 0 except LP-certified (r, D)" plus links 1–3 gives Wilf for S, provided the traversal is complete.

Neither "per lattice vs per semigroup" nor term-order choice is a problem. Residues of e = 4 minimal generators are
automatically distinct and nonzero, so m ≥ 4, and m ≤ 18 is BGOW anyway.

**LP certificate (tile_lp.py): sound.**
- Def(p) = 3m·max_{y∈Max} p·y − p·T(D) is convex and 1-homogeneous.
- The relevant p lie in the closed cone (link 1) and have p_a ≥ m + 1, so Def ≥ (m+1)κ when κ > 0.
- On each cell, Def/min p_a is linear-fractional. Skipping boundary vertices (p_a = 0) is legitimate because
  Def > 0 there: Def(p₀) = 0 would force p₀ = 0.
- I recomputed κ with a **different method** (three LPs, HiGHS, my own cone constraints) for **every** realizable
  (D, r), not only the canonical r. The values reproduce the logs exactly: m=8: 4.0 (fails, BGOW); 15: 15; 16: 22.67
  and 28; 17: 23.33 and 26; 19: 32.5; 20: 33.33 and 44.5; 23: 40. All pass (m+1)κ ≥ m(m−1) with large margins.

**Independent checks of completeness and of the failure list.**
- **Fan-free, shape-first enumeration** (shapes.py):
  - It lists every non-two-face down-set of size m. The generator was validated against brute force for n ≤ 11 and
    against PL(n) for n ≤ 12.
  - For those with δ < 0, it tests all r ∈ (ℤ/m)³ for injectivity and computes the open-cone area exactly.
  - m = 7…26 (up to 815,620 down-sets per m): the realizable δ < 0 tiles are m=8: 1, m=15: 2, m=16: 2, m=17: 2,
    m=19: 1, m=20: 2, m=23: 1, and none elsewhere. **This is exactly the scan's list.**
- **Exact area certificate of traversal completeness.** Open cones of distinct tiles are disjoint, so a lattice's tile
  list is complete iff the cone areas sum to the area of the simplex. Results:
  - Python traversal (copy of tile_enum.py) with my own exact polygons, every lattice, m = 7…40: all sums exact,
    counts equal to the logs.
  - C traversal (copy of tile_scan.c, plus a sum of areas mod 2⁶¹−1; detection validated by dropping one tile, which
    flags every lattice), every lattice, m = 19–30 and 46–119: 0 defects. Tile, non-two-face and HT counts are
    identical to the project logs for all of 19–45 and 46–119.
  - C traversal, a 1/40 sample of lattices at m ∈ {120, 125, 130, 150, 175, 189, 230, 256, 270}: 0 defects, 0 HT fails.
- Random end-to-end tests: about 48,400 e = 4 semigroups (m 19–130; generators up to 10⁴·m, including skewed
  generators near the simplex boundary), plus all 1,624 e = 4 semigroups of genus ≤ 20. HT fails occur only at
  m ∈ {19, 20, 23} (and m = 8 in genus ≤ 20).

**Gaps in link 6.**
- **G6a (known, open).** logs/tile_scan_C_131_280.log ends at m = 189. Until m = 190…280 finish, cone tiles in that
  range are covered by nothing; C-HT covers only 𝒞 there. The chain is incomplete until then.
- **G6b (new; must be checked before trusting m ≥ 257).** The public src/c/tile_scan.c stores coordinates as
  `uint8_t` (`Key.x`, the tile array `T`, the hash arena) and has MAXM 255. A "MAXM-300 build" that only raises MAXM
  wraps any coordinate ≥ 256.
  - The traversal must pass long-axis tiles near the simplex boundary. For r₁ a unit, the full axis {k e₁ : k < m}
    is a tile.
  - Demonstrated on a copy, comparing a uint8 build with a uint16 build, both MAXM = 300:
    - m = 257 (1/500 sample of lattices): 1 of 22 lattices has a wrong cone area;
    - m = 280 (1/150 sample): the uint8 build exits normally (code 0) but finds **61,277 tiles instead of 61,279**,
      with 42 of 219 lattices showing area defects.
  - In this sample the lost tiles were two-face, so the non-two-face count and HT result agreed. That is luck, not a
    guarantee.
  - Non-two-face tiles themselves had coordinates ≤ 248 at m = 280 (hill climb), so wrapping hits the traversal, not
    the analysed tiles.
  - The private build's source is not in the repo. Confirm it widened all three, or rerun 257–280 with uint16.
- **G6c (trust base).** For m ∈ [120, 189], and later [190, 280], I certified completeness only on 1/40 lattice
  samples. A full area-certified run would remove the "Gröbner fan traversal assumed complete" trust item for the
  whole range. It costs about 2× runtime; the patch is in proj_copy/tile_scan_v.c.
- Minor:
  - STATE says the m = 8 tile is "LP-certified". It is not (κ = 4); it is covered by BGOW.
  - tile_scan.c says the start point is "Python's start * 5979003". The LCD is 5,979,009, so it is a different
    point. This is harmless: any start point works.

## Counterexamples
None to any claim in links 1–6. The only false statement found is the heightH.py docstring ("+1 per incidence"),
which is not used by the chain. The demonstrated failure in G6b is a build/configuration risk, not a counterexample.

## Computations run (exact ranges and counts)
1. e2e.py (random): about 48,400 e = 4 semigroups, all built from random generator triples.

   | seed | draws | m range | e = 4 | two-face | non-two-face |
   |---|---|---|---|---|---|
   | 2 | 20,000 | 19–40 | 14,097 | 4,319 | 7,308 𝒞 + 2,470 cone |
   | 4 | 40,000 | 19–30 | 27,925 | 9,774 | 13,809 𝒞 + 4,342 cone |
   | 3 | 8,000 | 41–130 | 6,349 | 837 | 3,590 𝒞 + 1,922 cone |

   - Generator modes: <3m, <4–10m, <20–10⁴m, skewed.
   - Every assertion in links 1–5 passed.
   - HT fails occurred only at m = 19 (−4), m = 20 (−2) and m = 23 (−1, cone tiles).
2. genus_exh.py: all 93,142 semigroups of genus ≤ 20, of which 1,624 have e = 4. Same assertions, 0 failures. HT fails
   only for the m = 8 tile (7 semigroups).
3. shapes.py, m = 7…26: fan-free enumeration, results as listed under link 6.
4. lpcert.py: HiGHS LP κ for all realizable failing (D, r) at m ∈ {8, 15, 16, 17, 19, 20, 23}.
5. area_check.py: exact area certificate for the Python traversal, m = 7…40, every lattice.
6. Area-certified C traversal (proj_copy/tile_scan_v.c):
   - all lattices, m = 19–30 and 46–119 (logs c16_area_46_130.log, c_19_45.log);
   - sampled at m = 120–270 (c16_sampled.log);
   - uint8 vs uint16 comparison at m = 257 and 280.
7. tf_check.py: independent finite check for the two-face theorem, m = 5…500.
8. lemma_exh.py: all down-sets with |D| ≤ 20, lemmas for 𝒞 and the cone class.
9. Threshold arithmetic for C-HT, m ≤ 2·10⁵.

Not done: the full area-certified C run for m = 120–130 was stopped at m = 119. A new rule caps local jobs at 5 min,
and the permission system denied `gcloud compute ssh fejer` ("Containment Escape"), so the VM was not used. No other
computation exceeded a few minutes.

## Suggested repairs
1. G6b: confirm or fix the coordinate width in the MAXM-300 build: `Key.x`, `T`, the hash arena, and byte arithmetic
   on the stack. Rerun m = 257–280 with uint16, ideally with the area certificate. A drop-in patch is
   proj_copy/tile_scan_v.c (`-DMAXM=300 -DCT=uint16_t`).
2. Add the per-lattice area certificate to tile_scan.c and rerun 120–280 on the VM. Then the completeness of the finite
   range becomes a per-lattice certificate instead of a trust assumption.
3. Use δ ≥ −1 (H ≥ m − 2) in link 2. It is a free integrality gain: no LP is needed at m = 17 and 23, and the C-HT
   threshold drops to 130.
4. Fix the Lean citation for link 1: use MaxCL.lean `isFactTile_factDownSetG`, `IsFactTile.isTile` and
   `IsFactTile.columnIdentity`, not TileReduction.lean's lex-tile `isTile_factDownSet`. If the LP certificate is to be
   formalized, add e_a ∈ D and the closed-cone inequality p·q ≥ p·rep(q).
5. Text fixes:
   - heightH.py docstring;
   - STATE "m = 8 LP-certified" should read "m = 8 by BGOW";
   - HRW Prop 2.6 attribution: (a) vs (b);
   - the tile_scan.c start-point comment.

## Files
- Report: <scratch>/e4_chain_review.md
- Toolkit and tests: tk.py, e2e.py, genus_exh.py, shapes.py, lpcert.py, area_check.py, tf_check.py, lemma_exh.py,
  maxcoord.py, maxcoord2.py
- C copies: proj_copy/tile_scan_orig.c, proj_copy/tile_scan_v.c (area check, configurable width), proj_copy/tile_scan_droptest.c
- Logs: e2e_s2_19_40.log, e2e_s3_41_130.log, e2e_s4_19_30.log, genus20.log, shapes_19_26.log, lpcert.log,
  area_17_40.log, c_19_45.log, c16_area_46_130.log, c16_sampled.log
