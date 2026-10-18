# STATE.md — handoff (updated 2026-10-18, night 13 late)

## Main route
Wilf ⇐ TOP'' (Lemma A, LEAN `wilf_of_TOP2`) ⇐ Tile-TOP'' ⇐ MaxCL (LEAN) ⇐ Tile-CL (d ≤ 5 only; false at d = 6).
**τ-criterion (LEAN-CHECKED, lean/Wilf/TauCrit.lean):** with τ = |Ap ∩ [c, c+m)| = #gaps in [c−m, c),
Wilf holds when (e−2)(m+1) ≥ 2(e−2)τ + 2P₂. Focus through night 17: **Wilf for e = 4**. CORRECTION 2026-10-18: NOT open. kseth/wilf-e4 (GitHub, Sept 2026) claims a
complete computer-assisted proof (unrefereed); see LITERATURE §3 items 11–12.
**e = 4 split:** two-face tiles (some e_a + e_b ∉ D) — **PROVED (paper)**; non-two-face tiles — **reduced to HT**
(H(D) ≥ m − 1, shape-only) and **verified completely for m ≤ 60** (computer-assisted); HT for m > 60 OPEN (G2).

## Proved facts (paper unless marked)
- CH, Corollary H, Lemma A, TOP'' ⇒ Wilf, CH', CL ⇒ Wilf, Tile-TOP'' ⇒ Wilf, MaxCL ⇒ Tile-TOP'': LEAN.
- Flat-MaxCL (height ≤ 2) and Ap ⊆ {0} ∪ P ∪ 2P ⇒ Wilf: LEAN. 2-D Tile-CL (every 2-D tile), Wilf e ≤ 3: LEAN.
- Cross Lemma + τ-criterion: LEAN. Two-face box theorem (MaxCL): paper.
- Λ-criterion; cylinder structure of 3-D tiles (PROOFS.md).
- THEOREM — Wilf for every e = 4 semigroup with a two-face tile (PROOFS.md "THEOREM (two-face e = 4)"). Novelty
  UNVERIFIED; not in Lean.
- e = 4 faces+core identity (NOTEBOOK night 13).
- **Height criterion** (NOTEBOOK night 13 cont.): (m+1)·H(D) ≤ mW + m(m−1); so H ≥ m − 1 ⇒ Wilf (any e = 4).
- **Per-tile LP certificate** (src/tile_lp.py; NOTEBOOK night 13 late): (m+1)κ_D ≥ m(m−1) ⇒ Wilf for all S with tile D.
- **Exact terrace formula** H_a = Σ_k (k+1) Σ_{band_k} ht_{S^a(k)} (any down-set); singletons of q*-free cylindrical
  tiles are exposed unit-step face corners lying in the L-shaped fins Φ_c; wall lemma for consecutive face corners.

## Computer-assisted (complete enumeration; trust base: Gröbner-fan traversal + code; validated m ≤ 13)
- **Wilf holds for every e = 4 semigroup with m ≤ 60** (logs/tile_scan_H.log; scan continuing to m = 70 in the
  background at last check). HT fails only at m ∈ {8,15,16,17,19,20,23}; those tiles LP-certified (m = 8: BGOW).
- min H − (m−1) grows ≈ 0.9(m − 20) (60 at m = 60, 74 at m = 61). Hp ≥ m−1 for 24 ≤ m ≤ 48.

## Observed (not proved)
- Tile-CL exhaustive d=3 m ≤ 20, d=4 m ≤ 14, d=5 m ≤ 12. TOP'' always (genus ≤ 18 + extended).
- max |A| (non-two-face) = 10 for m ≤ 48; unbounded in general (Backelin, |A| = 15 at m = 213).
- Cylindrical sets alone do NOT give HT: q*-free fail up to m = 30; three triangular fins fail up to m = 64.

## Refuted (preserved in NOTEBOOK/EXPERIMENTS)
Residual of sharp τ-criterion ⇒ two-face; PE; Λ-dichotomy; Λ-criterion e = 4 m ≥ 20; S1 for two-face;
non-two-face ⇒ τ-criterion; face-wise ν injectivity; VTC; naive dominance injection; continuum "2/3 law";
**Cross-Lemma |A|-route for HT (Bresinsky |A| ~ 2√m); N-route without H₂; HT for general cylindrical sets.**

## Open gaps
- **G2': HT for non-two-face 3-D lattice tiles with m > 60** (scan limit). This alone would complete Wilf for e = 4.
- G3: Tile-CL d = 3 in general (route I). G4: Lean formalization of the two-face theorem, height criterion, LP lemma.
- G5: independent re-implementation of the tile enumeration/scan (second checker) before claiming the m ≤ 60 result.

## Three active approaches
1. **(A) q*-free cylindrical HT for m ≥ m_A** via the terrace formula: charge each exposed unit-step face corner
   (singleton, cost (k+1)/3) to the fin Φ_c of its face and to the stretches of the perpendicular columns.
2. **(B) q*-tiles:** wall lemma ⇒ unit steps of a face consume t-values on a spike/fin of the axis, whose cells pay
   ≈ C(len,2); target: Σ_{unit-step corners} cost ≤ spike/fin surplus.
3. **Extend the complete scan** (parallel/compiled second implementation, also satisfies G5) to m ≈ 100–120, so that
   (A)/(B) may be proved with lossy constants.

## Next precise task
Formulate and test the charging inequality for (A): for every q*-free cylindrical set,
Σ_{singletons (a,k)} (k+1)/3 ≤ 1 + Σ_c [Σ_{u∈Φ_c} ht_{F_c}(u) − |Φ_c|/3] + Σ (other band surpluses); find its minimal
counterexamples with cyl_exhaust.py and identify the extra local surplus needed; then attempt the proof.
