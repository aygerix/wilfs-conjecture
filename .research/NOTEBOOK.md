# NOTEBOOK.md — dated research log (Wilf's conjecture)

## 2026-10-17 — Session 1

### Orientation
- Exact target: ∀ numerical semigroups S: e·(c − g) ≥ c (S = ℕ: c = g = ell = 0, e = 1, holds).
- Phase 0 done: two independent checkers (E0), literature map (.research/LITERATURE.md, by literature agent;
  key: proved for q ≤ 3, 3e ≥ m, m ≤ 19, genus ≤ 100, ell ≤ 12; W_0 ≥ 0 false at q = 4; D'Anna–Moscariello
  m − 1 ≤ (e−1)n; any counterexample has q ≥ 4, m ≥ 20, 4 ≤ e < m/3, t ≥ e, ...).

### Reformulations (all exact, checked)
- Levels: Wilf ⇔ (d+1)Σ_{w∈Ap}λ(w) ≤ dqm + ρ, λ(w) = ⌊(w+ρ)/m⌋ ("mean Apéry level ≤ (d/(d+1))·q + ρ/((d+1)m)").
  d/(d+1) is the mean degree ratio of a d-simplex: Wilf = "Apéry set is no more top-heavy than a simplex".
- Value form: Wilf ⇔ (d+1)Σ_{w∈Ap} w ≤ d·m·M − (d−1)m(m−1)/2, M = F + m.
- W = ρ + Σ_{w∈Ap} (d·δ(w) − λ(w)), δ = q − λ (depth).

### Main new result of the session: Identity CH (PROVED) — see PROOFS.md
  m·W = Σ_a Def_a + E − (d−1)m(m−1)/2,  Def_a = Σ_{p_a-chains C}|C|(M − top C) ≥ 0,  E ≥ 0.
- Gives a 3-line proof of the homogeneous ("continuous") Wilf inequality (d+1)Σ Ap ≤ d m max Ap, i.e.
  Corollary H: e·n ≥ c − (e−2)(m−1)/2 for all S. (Novelty unchecked.)
- Interpretation: Wilf = discrete divergence theorem on the Apéry down-set + a discrete correction of
  exactly (d−1)m(m−1)/2. The correction is where all difficulty lives.

### Lemma A (PROVED) and Conjecture TOP'' (CONJ, strong evidence)
- Lemma A: m·W ≥ m((d+1)m+d−1)/2 − Σ_{u∈X_q} π(u)(d + ℓ(u)) + Σ_{w∈Ap, w<c} E(w).
- TOP'': Σ_{u∈X_q} π(u)(d + ℓ(u)) ≤ m((d+1)m+d−1)/2. Equivalently
  m + Σ_{u∈X_q} π(u)(ℓ(u) − 1) ≤ e·Σ_{w∈Ap, w<c} π(w), π(x) = ((x − c) mod m) + 1.
  ("Wilf localized to the last two levels, weighted by position").
- Evidence: genus ≤ 24 exhaustive (0 failures, equality exactly when W = 0), 3002 adversarial.
- Structural facts proved along the way: top-layer elements are pairwise incomparable maximal elements of the
  Apéry poset (difference of two would be ≥ m+1 > window); each u ∈ X_q has ℓ(u) ≤ q; for every nonzero
  divisor s of u in Ap, the last-level representative of u − s is a left element, and s ↦ position is injective.

### Failed claims (preserved, with smallest counterexamples)
- COV, COV′ (rigid covering of gaps by e−1 reflected copies of L): ⟨7,9,10,15⟩.
- S1 (positive-part per-direction budget): ⟨7,11,12,20⟩.  TOP_0 (no E): ⟨9,13,14,15,16⟩.
- FLOW (Hall-local TOP''): ⟨10,11,13,19⟩.  SC′ (offset sum): ⟨5,8,9⟩.  X1/X2/X3 per-direction excess:
  ⟨9,10,12,13⟩, ⟨7,11,12,20⟩.
- Lesson: every per-direction or per-element localization of TOP'' fails on small cases although TOP'' holds
  with slack; the directions interact (elements with several factorizations carry the balance via E and ν).

### Open questions generated
1. Exact identity for the TOP'' slack (what does it count?).
2. Does TOP'' reduce in depth (induction on q via adding pseudo-Frobenius numbers in the last level)?
3. q = 2 case of TOP'' is a pure sumset inequality: for A ⊆ [1,N−1], R ≥ 1, B = ((A+A)∖A) ∩ [1,N], k = |A|:
   N + R + Σ_{s∈B}(s+R) ≤ (N+R−|B|)·((k+1)R + ΣA). Prove it (warm-up / pattern for general q).
4. Novelty check for Corollary H.
