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

Notes
- "Tight" in E6 means equality in TOP''. Observed: TOP'' equality ⇔ W = 0 for genus ≤ 24.
- A bounded search excludes only the enumerated sets; nothing here is a proof for all S.
- Logs: `logs/top2_g24.log`.
