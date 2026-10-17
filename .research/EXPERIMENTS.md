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

Notes
- "Tight" in E6 means equality in TOP''. Observed: TOP'' equality ⇔ W = 0 for genus ≤ 24.
- A bounded search excludes only the enumerated sets; nothing here is a proof for all S.
- Logs: `logs/top2_g24.log`, `logs/cl_g24.log`.
- E16/E17: run from repo root, e.g. `python3 src/scratch/clinj.py 2 9`.
