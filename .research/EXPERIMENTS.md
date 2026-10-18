# EXPERIMENTS.md — exact finite tests (all integer arithmetic, Python 3.14, no randomness unless seeded)

Tools: `src/ns.py` (implementation A: membership bitsets, tree enumeration by genus),
`src/ns_kunz.py` (implementation B: Apéry set by Dijkstra, Selmer/Brauer–Shockley, Apéry-poset generators).

| id | script | predicate | domain | result | runtime |
|---|---|---|---|---|---|
| E0 | `src/crosscheck.py 18` | A and B agree on m,e,c,g,ell,W,P; Kunz inequalities; counts = OEIS A007323 | all S, genus ≤ 18 (33,282) | all agree; counts match; min W = 0 | 1 s |
| E1 | `src/exp_levels.py 18` | ell = qm − Σ_{w∈Ap} λ(w), λ = ⌊(w+ρ)/m⌋; Wilf ⇔ (d+1)Λ ≤ dqm + ρ | genus ≤ 18 | identity holds; W=0 iff e=2 or S = T_{m,q} = mℕ∪[qm,∞) (79 cases) | 1 s |
| E2 | `src/exp_hard.py 21` | smallest e·ell/c with q ≥ 4 excluding equality families | genus ≤ 21 | min ratio ≈1.031 at ⟨3,32,34⟩ (near-T_{m,q} shapes) | 2 s |
| E3 | `src/exp_cover.py 18` | COV: gaps ⊆ ∪ of e−1 sets f−L, f∈PF | genus ≤ 18, t > e−1 (1105 S) | FALSE in all 1105 (PF maximality) | <1 s |
| E3b | `src/exp_cover2.py 16` | COV′: gaps ⊆ ∪ of e−1 translates T−L | genus ≤ 16, t>e−1 (309 S) | FALSE in 22; smallest ⟨7,9,10,15⟩, ⟨7,8,10,19⟩ | <1 s |
| E4 | `src/chains.py 18` | Identity CH exact | genus ≤ 18 (33,281 S≠ℕ) | holds | 1 s |
| E4b | `src/exp_chains.py 18` | S1: Σ_a(C−Def_a)^+ ≤ C+E; S2 without E | genus ≤ 18 | S1 fails once ⟨7,11,12,20⟩; S2 fails 4 | 2 s |
| E5 | `src/exp_top.py 18` | TOP_E / TOP_0 (Lemma A predecessor) | genus ≤ 18 | TOP_E 0 failures; TOP_0 fails 4 (e.g. ⟨9,13,14,15,16⟩) | 5 s |
| E5b | `src/exp_top_adv.py` | TOP_E on adversarial set (seed 12345) | W0<0 examples, Backelin ⟨213,216,226,227⟩, Delgado S(p), 1075 random deep | 0 failures | 5 s |
| **E6** | **`src/top2.py`, `src/run_top2_big.py 24`** | **TOP''** | **all S, genus ≤ 24 (712,372)** | **0 failures; tight in 116 = exactly the W=0 semigroups** | 25 s |
| E6b | `src/exp_top2_adv.py 1 3000` | TOP'' adversarial+random (seed 1): m∈[5,60], ≤7 gens, truncations ⟨A⟩∪[c',∞) | 3002 S | 0 failures; min normalized slack (W>0) 0.185 | 5 s |
| E7 | `src/exp_top2_near.py 18` | near-tight TOP'' cases | genus ≤ 18 | listed; tightest W>0: ⟨7,11,12,20⟩ (slack 3), ⟨4,7,13⟩ (slack 1) | 1 s |
| E8 | `src/exp_flow.py 18` | FLOW (Hall-localized TOP'') | genus ≤ 18 | FALSE once: ⟨10,11,13,19⟩ (top 38 = 2·19 underfunded) | 2 s |
| E9 | `src/exp_offsets.py 18` | SC′ offsets ≤ m(m−1)/2; offsets positive/distinct | genus ≤ 18 | SC′ fails 16 (⟨5,8,9⟩); offsets not positive/distinct | 2 s |
| E10 | `src/exp_excess.py 18` | per-direction excess X1/X2/X3 | genus ≤ 18 | X1 fails 1115; X2 fails 3 (⟨9,10,12,13⟩); X3 fails 1 (⟨7,11,12,20⟩) | 3 s |
| E11 | `src/exp_tree_mono.py 16` | TOP'' slack monotone along the semigroup tree (parent→child) | genus ≤ 16 | FALSE: slack decreases on 1912 of 4106 edges | 2 s |
| E12 | `src/exp_freepos.py 18` | "free-position" localization of TOP'' | genus ≤ 18 | FALSE in 14 cases | 2 s |
| E12b | `src/carries.py 18` | CH-λ identity W = Σ|C|δ(top) + ρ + K − Σκ; strong carry claim Σκ − K ≤ ρ | genus ≤ 18 | identity exact; claim 0 failures | 2 s |
| **E13** | **`src/cl.py 18 grlex,lex,revlex`; `src/cl.py 24 grlex,lex`** | **CL (asserts m·W = m·depth + LHS − target exactly)** | **genus ≤ 18 (3 orders); genus ≤ 24 (712,372 S; grlex, lex)** | **0 failures; tight 6702 (g≤18, grlex), 102,188 (g≤24)** | 1 s / ~4 min |
| E14 | `src/exp_cl_variants.py 15` | CL with M replaced by any maximal element (V1) / any element (V2) of D | genus ≤ 15 (6963 S) | 0 failures both: CL holds for every reference residue s | 3 s |
| **E15** | **`src/exp_cl_tiling.py`** | **Tile-CL for ALL down-sets D ⊆ ℕ^d, |D| = m, all p ∈ (ℤ/m)^d bijective on D, all s** | **d=2: m ≤ 15; d=3: m ≤ 11; d=4: m ≤ 8 (exhaustive)** | **0 failures** | ~10 min |
| E16 | `src/scratch/pdcl.py` | PDCL: Σ_a min_s f_a(s) ≥ (d−1)m(m−1)/2 | tiles d=2 m ≤ 12; d=3 m ≤ 9 | d=2: 0 failures; d=3: FALSE (6 at m=6, 12 at m=7, …) | 1 min |
| E17 | `src/scratch/clinj.py 1 12`; `... 2 9` | CL for down-sets with φ merely injective (|D| ≤ m), form (II) | d=1 m ≤ 12; d=2 m ≤ 9 | FALSE (d=1: D={0,1,2}, p=7, m=10, σ=3) | 1 min |

| E18 | `src/scratch/ramp.py` | Ramp Lemma Σ_D βρ ≤ |D|ρ(0), ρ directionally convex | all down-sets d=2 m≤9, d=3 m≤7; q ∈ [1,5]^2 / [1,4]^3 | 0 failures (now PROVED + Lean) | — |
| E19 | `src/scratch/divis.py` | slack integrality, slack ∈ [0,m−1] | d=2 m≤10, d=3 m≤8 | always integer in range | — |
| E20 | `src/scratch/ptcl.py`, `rptcl.py`, `pmaj.py` | P-TCL (partial, uncorrected) / RP-TCL (virtual-completion corrected) / partial majorization | d=2 m≤10, d=3 m≤7 | P-TCL FALSE (d=2 m=7, D'={00,01,02,10,11,20}, p=(2,3)); RP-TCL and pmaj 0 failures | — |
| E21 | `src/scratch/fraccert.py`, `fraccert2.py`, `grcheck.py` | arc certificates (integer/fractional) for majorization | small tiles | FALSE: d=2 m=8, 3×3∖{22}, p=(5,7) | — |
| E22 | `src/scratch/dslp.py` | LP over region R = {Π(z_a+1) ≤ m} | d=2 m=8..10; d=3 m=4..6 | tight d=2; d=3 NOT tight (13/3 at m=5, 21/4 at m=6) | minutes |
| **E23** | **`src/scratch/dslpbox.py`** | **LP over box-injective region R'(p), x_0=1** | **d=3 m=5,6,7; d=4 m=5,6 (all p, s)** | **tight: max = m−1, min = 0 in every case** | ~1 h |
| E24 | `src/scratch/scl.py 2 6 6`, `2 8 7`, `3 6 5` | single-cut lemma F(E) ≤ θ + |D'∖E| (any V-injective down-set) | all down-sets of size N, all weights ≤ P | 0 violations (tight cases exist) | 1 min |
| E25 | `src/scratch/xscl.py 1` | XSCL d|E| ≤ θ + |∂⁺E| (simplex E, V injective on E∪∂⁺E) | 4000 random p̂, d ∈ {2..5}, weights ≤ 80, seed 1 | max excess 0 | 1 min |
| E26 | `src/scratch/aperylift.py 2 10`, `3 7` | every tile is an Apéry tile for some lift (LP on exit vectors) | all tiles d=2 m≤10 (462), d=3 m≤7 (624) | strictly feasible in every case | 1 min |
| E27 | `src/scratch/rampstair.py 2 9 3`, `3 6 2` | ⌊(V+σ*)/m⌋ directionally convex for some Apéry lift (⇒ CL by Ramp) | lifts k ∈ [0,3]^2 / [0,2]^3 | 30/126 tiles (d=2 m=9), 102/126 (d=3 m=6) | 1 min |
| E28 | `src/scratch/rampdecomp.py 2 9`, `3 7` | Ramp decomposition T1 (supermodular) + T2 (column trapezoid) | all tiles, all σ | T1 ≥ 0 always; T2 ≥ −54 (m=9) | 1 min |
| **E29** | **`src/scratch/basecl.py 2 9`, `3 7`** | **Base-CL: base-slack ∈ [0,m−1]** | **all tiles, all σ, d=2 m≤9, d=3 m≤7** | **0 violations; always integral** | 1 min |
| E30 | `src/scratch/colcl.py 9`, `colcl2.py 9`, `mixedex.py` | Column-CL for orthogonally convex polyominoes, split by orientation | d=2, all fixed polyominoes m≤9 | all-(+) and all-(−): 0 failures; general ortho-convex FALSE from m=4; mixed FALSE at m=9 | 3 min |
| E31 | `src/scratch/topbase.py 2 9`, `3 7` | are base-slack shapes relabelings of top-slack shapes? | all tiles | NO (e.g. d=2 m=9: 54 top shapes, 37 base shapes, 31 base shapes not top shapes) | 2 min |

| E32 | `src/scratch/wallpair.py 2 8 2`, `3 6 1` | wall pairings of X(s) ≥ K: per wall (P1), tail sums (P2), head sums (P3) | all tiles, lifts k ∈ [0,2]^2 / [0,1]^3 | P1, P3 FALSE (e.g. 336/608 at d=2 m=8); P2 0 failures | 2 min |
| **E33** | **`src/scratch/tailpair.py 2 10 0`, `3 7 0`, `2 7 2`, `3 6 1`** | **tail pairing TP for all J** | **all tiles; std lift and lifts k ≤ 2 / ≤ 1** | **0 failures** | 5 min |
| **E34** | **`src/scratch/gtp.py 2 10 0`, `3 7 0`, `2 7 2`, `4 6 0`** | **GTP: Hall condition for upward matching gaps → wall crossings, all thresholds θ** | **all tiles, d=2 m≤10, d=3 m≤7, d=4 m≤6** | **0 failures; intermediate tight thresholds occur** | 5 min |
| **E35** | **`src/scratch/apramp.py 2 9 1`, `3 7 0`, `3 6 1`** | **AP-Ramp A(t0) ≤ (m−1−t0)⁺ for all t0 ≥ 0** | **all tiles, lifts as listed** | **max excess 0** | 5 min |
| E36 | `src/scratch/taupos.py 2 9 1`, `3 7 0` | pointwise τ(t) ≤ 0 for t ≥ m−1 | all tiles | FALSE (d=2 m=6 std lift: 2; d=3 m=7: 18) | 2 min |
| E37 | `src/scratch/colthresh.py 2 8`, `3 6` | column-threshold formula slack = Σ_C[H_C(τ_C) − H_C(κ_C)] | all tiles, all s | 0 mismatches | 1 min |
| E38 | `src/scratch/colthresh2.py 2 9`, `3 7` | per-column / per-direction / best-order localizations | all tiles, all s | all FALSE in general (best order fails 6/3108 at d=3 m=7) | 10 min |

| E39 | `src/scratch/coverpairs.py`, `coverpairs2-5.py` (+`blossom.py`) | PCL: c0 disjoint covering pairs of column arcs; restricted types | d=2 m≤10, d=3 m≤8, d=4 m≤7 | TRUE d=2, d=3 m≤7, d=4 m≤7; FALSE d=3 m=8 (cube {0,1}^3, p=(2,3,4)); line/HT/ABOVE/BELOW restrictions FALSE | 30 min |
| E40 | `src/scratch/monotrans.py` (+`mcf.py`) | monotone transport cost ≤ m(m−1)/2 | d=2 m≤9, d=3 m≤6 | FALSE (2 tiles at d=2 m=8) | 5 min |
| E41 | `src/scratch/gaproute.py` (+`maxflow.py`) | monotone gap routing b-matching | d=2 m≤9, d=3 m≤6 | FALSE (406/1134 at d=2 m=9) | 5 min |
| E42 | `src/scratch/loccl.py` | LocCL: carries absorbed by columns through the cell | d=2 m≤10, d=3 m≤7 | FALSE (2×2 box) | 5 min |
| E43 | `src/scratch/slackrange.py`, `uppercarry.py` | distribution of min/max slack; upper vs lower carries | d=2 m≤10, d=3 m≤7 | min slack ∈ {0,1,2,3}; Σĉ ≠ c0 in general | 2 min |
| **E44** | **`src/scratch/basecheck.py 2 9`, `3 8`** | **Base-CL carry form; box reflection Tile = Base; Base-CL range** | **all tiles** | **0 mismatches; 0 range failures** | 3 min |
| E45 | `src/scratch/basecl3.py`, `glemma.py` | per-cell G ∈ {−1,0,1} with localization (d=3); pure subset-sum lemma | d=3 tiles m≤7; ℓ-vectors m≤40 (d=3), ≤34 (d=4) | holds on tiles m≤7; FALSE for cube m=8 and as a pure lemma | 15 min |
| **E46** | **`src/scratch/tauclass.py`, `lshape.py`** | **τ-class decomposition identity; per-class positivity; CDL (d=2)** | **d=2 m≤10, d=3 m≤7** | **identity 0 mismatches; per-class FALSE; CDL 0 failures** | 10 min |
| E46b | `src/scratch/sametile.py`, `mincorner.py`, `cdlparts.py` | slack lattice-invariance; min slack at s = φ(maximal cell); partial CDL class sums | d=2 m≤11, d=3 m≤7 | slack NOT lattice-invariant; "min at a maximal cell" FALSE (2×3 box, p=(3,5): slack [5,2,2,2,1,3]); every proper partial CDL class sum goes negative, only the full sum is ≥ 0 | 2 min |
| **E47** | **`src/exp_cl_adv.py 1 3000 100`** (+ `src/scratch/clverify.py`) | **Tile-CL and CL on adversarial + random large S (seed 1; m ≤ 100 random, plus W0<0, Backelin, Delgado; up to 12 extra gens; truncations)** | **3001 S, max d 98, max m 213** | **CL FALSE: S = ⟨14,22,23,57,61,62,63⟩ (c=56, g=43, e=7, W=35): LHS 441 < 455 (examples/CL_counterexample.md); 9 Tile-CL failures (both bounds)** | 16 s |
| **E48** | **`src/exp_cl_regime.py 7 4000 90`** | **CL (reference s) and Tile-CL (all s) split by regime 3e < m vs 3e ≥ m; clustered gens; truncations with c > 3m** | **4000 S (seed 7)** | **3e<m: 1664 S, CL 0 fails, Tile-CL 9 fails; 3e≥m: 2336 S, CL 3 fails, Tile-CL 43 fails** | 26 s |
| **E49** | **`src/exp_top2_regime.py 11 5000 90`** | **TOP'' on the same hard generators (+W0<0, Backelin), every-depth truncations** | **5005 S (seed 11), m ≤ 90 (+213)** | **TOP'' 0 failures (CL(ref) fails on 7 of them); min normalized TOP'' slack 0.0225 (W = 1)** | 16 s |
| **E50** | **`src/scratch/hajos.py 16`** | **Box tiles: Hajós (some k_a p_a ≡ 0) and the inductive identity ΣG = ΣG'_red − n⌊σ/n⌋ + Σ_{x'}⌊⟨σ+Λ'(x')⟩_m/n⌋; Base-CL range** | **all boxes d=2,3,4, m ≤ 16, all p, all σ** | **0 identity failures; Hajós factor always present; 0 range failures** | 1 min |
| E51 | `src/scratch/spikes.py` | Tile-CL for core ∪ spikes (core = down-set of dim ≤ 2 with φ injective, spikes on the complement residues) | m ≤ 14 | first failure m = 14, core Δ_3, p = (5,6), spikes (7,8,9,13) (dual of E47's S); none for m ≤ 13 | 3 min |
| E52 | `src/scratch/clh.py 11 5000 90`, `23 5000 140` | CL-H: CL(ref) + d_high(ℓ − q) ≥ 0; do CL failures need high generators? | 10,009 S (two seeds) | CL-H 0 fails; all 14 CL(ref) fails have high generators | 30 s |
| E53 | `src/scratch/srcl.py 11 5000 90`, `1 3000 100`; `src/scratch/dspikes.py 5 13` | SR-CL: slack(s) ≥ −#spikes; spike-free Tile-CL; double spikes | 8005 adversarial tiles; core(dim≤2)+spikes+double spikes m≤13 (~90k) | 0 failures; worst min/σ ≈ −0.42 | 2 min |
| **E54** | **`src/scratch/tiletop.py`** | **Tile-TOP'' (all s) and DR-CL, all tiles** | **d=2 m≤13, d=3 m≤10, d=4 m≤8, d=5 m≤7** | **0 failures; slack 0 only for simplex tiles** | 10 min |
| **E55** | **`src/scratch/tiletop_adv.py 11 5000 90`, `1 3000 120`** | **Tile-TOP'' and rearranged R-TOP on adversarial Apéry tiles** | **8008 tiles** | **Tile-TOP'' 0 fails; R-TOP FALSE (3 fails: ⟨7,15,16,17⟩∪[28,∞), ⟨7,11,12,13⟩∪[18,∞), one m=59)** | 1 min |
| E56 | `src/scratch/injtop.py`, `injtop2.py`, `injtight.py`, `stairinj.py` | injective generalizations (A),(B) of Tile-TOP''; tightest cases; 2D staircases | d=1 m≤12, d=2 m≤14, d=3 m≤10, d=4 m≤8; Δ_k, k≤9 | 0 failures; tightest are non-tiles with |D| = m−1; Δ_k needs m ≳ 1.3·|Δ_k| to embed | 15 min |
| E57 | `src/scratch/boxtop.py`, `src/scratch/semicrude.py` | strengthenings of Tile-TOP'': Box weight |[0,y]|−2, |[0,y]|−1, 2|y|−2; semi-crude (π ↦ m on maximal cells) | all tiles d=2 m≤12, d=3 m≤10, d=4 m≤8, d=5 m≤7 | all FALSE (Box: d=2 m=5; semi-crude: d=3 m=9,10); weight |y|−1 exact | 10 min |
| **E58** | **`src/scratch/maxcl.py`** | **MaxCL: Σ_A(|y|−1)r ≤ (d+1)Σ_N r for all rotations** | **all tiles d=2 m≤13, d=3 m≤10, d=4 m≤8, d=5 m≤7** | **0 failures** | 10 min |
| **E59** | **`src/scratch/maxcl_adv.py 11 5000 90`, `1 3000 120`; `src/scratch/maxcl_d3.py`** | **MaxCL on adversarial Apéry tiles; random 4/5-generated S with large m** | **8008 tiles; 6800 S, m ≤ 260, type ≤ 22** | **0 failures; worst slack/m² ≈ 0.25 (random)** | 5 min |
| E60 | `src/scratch/chaincharge.py` | is the worst σ = φ(0)? chain charging with uniform load at σ = 0 | all tiles, ranges of E58 | worst σ ≠ φ(0) in most tiles; chain charging 0 failures | 10 min |
| **E61** | **`src/scratch/loadlemma.py`** (+`exactlp.py`) | **Load Lemma (exact LP) and count condition** | **all tile shapes d=2 m≤12, d=3 m≤10, d=4 m≤8, d=5 m≤7** | **0 failures** | 10 min |
| E62 | `src/scratch/loadcount_adv.py 3 6000 100` | count condition 2Σ_A(|y|−1) ≤ (d+1)(|N|−1) | 6002 adversarial Apéry tiles | 0 failures; min slack 0 (N = {0}) | 20 s |
| **E63** | **`src/scratch/groupcone.py 2 11`, `3 8`, `4 7`; `src/scratch/groupcone_adv.py 7 200 60 all`, `13 3000 120 ref`, `11 600 100 all`** | **GCL: MaxCL on the whole group-subadditive cone (exact LP small; HiGHS adversarial)** | **all tiles, all σ (small); 202 tiles × all σ; 3002 tiles × {c mod m, 0}** | **0 failures; minimizers are quotient positions ⟨ug⟩_k** | 30 min |
| **E64** | **`src/scratch/loadlemma_adv.py 7 600 70`, `5 3000 90`** | **Load Lemma on adversarial tiles (HiGHS, min max-load)** | **3600 tiles** | **FALSE: S = ⟨39,71,72,77⟩, L* = 5.037 > 4 (MaxCL slack 1910 there)** | 10 min |
| E65 | `src/scratch/gll1.py 2 11`, `3 8`, `4 7`; `src/scratch/gll1_adv.py 3 1500 90 ref` | GLL1: one-level lattice pairing in N∖z0 | small tiles all z0; 1500 adversarial at σ = c | FALSE (d=2 m=4,5; d=3 m=7,8; d=4 m≤7; 5/535 LPs with m > 3e, all "no admissible pair", spike-heavy) | 15 min |
| E66 | `src/scratch/maxcl_tight.py` | near-tight MaxCL tiles | all tiles d≤5 small m | tight: column, simplex, column+spikes (m = d+2); next ≈ 0.012 normalized | 5 min |
| E67 | `src/scratch/ecount.py exh`, `adv 5 3000 90` | E-count (Hall condition): 2Σ_Y(|y|−1) ≤ (d+1)(|↓Y|−|Y|−1) ∀Y ⊆ A | all tile shapes small; 3001 adversarial | 0 failures | 5 min |
| E68 | `src/scratch/boxload.py exh`, `adv 7 3000 90` | uniform box pairing load ≤ d+1 | small exhaustive; 3002 adversarial | exhaustive 0 fails (max exactly d+1 at e_a); adversarial FALSE 319/3002 | 5 min |
| E69 | `src/scratch/crude_regime.py 21 4000 120`; `src/scratch/crude_open.py 1 400`; `src/scratch/crude_search.py 1 400 12` | crude rearrangement bound Σ T_(i)(m−1−i) ≤ (d+1)M' (residue-free ⇒ MaxCL) | 4001 adversarial tiles; 400 open-regime S; hill-climb in open regime | holds 3883/4001 and all 400 random open-regime S; FALSE in open regime by hill-climb (⟨34,46,65,66,75,81,88,105⟩: −0.021) while MaxCL slack there ≥ 0.108 | 40 min |
Notes
- "Tight" in E6 means equality in TOP''. Observed: TOP'' equality ⇔ W = 0 for genus ≤ 24.
- A bounded search excludes only the enumerated sets; nothing here is a proof for all S.
- Logs: `logs/top2_g24.log`, `logs/cl_g24.log`.
- E16/E17: run from repo root, e.g. `python3 src/scratch/clinj.py 2 9`.
