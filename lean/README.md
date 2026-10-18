# Lean 4 formalization: Wilf's conjecture foundations and Apéry-chain results

- Toolchain: `leanprover/lean4:v4.33.1`; mathlib pinned to rev `0df444a360eaa60ab8c11dca51a86af692955474`
  (same as `/Users/jmercedes/prove2me_workspace`; `.lake/packages` was APFS-cloned from there, `.lake/` is git-ignored).
- Build: `cd lean && lake build` (about 1.5 min wall clock; the files import only the mathlib modules they need, not all of `Mathlib`).
- Axiom audit: `cd lean && lake env lean scripts/PrintAxioms.lean`.
- Files: `Wilf.lean` (root), `Wilf/Basic.lean` (definitions and general theorems),
  `Wilf/Chains.lean` (Identity CH, Corollary H, Lemma A, TOP'' ⇒ Wilf; see `.research/PROOFS.md`),
  `Wilf/Carry.lean` (factorization down-set D, column identity CH', CL ⇒ Wilf, Tile-CL statement),
  `Wilf/TileReduction.lean` (the factorization down-set is a tile; CL = Tile-CL at `s = M`; **Tile-CL ⇒ Wilf**),
  `Wilf/TileTop.lean` (Tile-TOP'' statement; **Tile-TOP'' ⇒ Wilf**),
  `Wilf/MaxCL.lean` (MaxCL statement; **MaxCL ⇒ Tile-TOP''**; **Flat-MaxCL**; **Wilf when every Apéry element has a factorization of length ≤ 2**),
  `Wilf/Ramp.lean` (the Ramp Lemma for finite down-sets and directionally convex `ρ`),
  `Wilf/Examples.lean` (kernel-checked examples), `scripts/PrintAxioms.lean` (axiom report; not part of the library).

## Status (2026-10-17, after the Tile-reduction / Ramp round)

- `lake build`: succeeds, 0 errors, 0 warnings.
- `sorry` count: **0** (`grep -rnw sorry Wilf Wilf.lean` gives nothing). No `axiom` declarations and no `native_decide`.
- `#print axioms`: every declaration listed in `scripts/PrintAxioms.lean` (124 of them, including all the main ones below)
  depends only on `[propext, Classical.choice, Quot.sound]`, the standard mathlib axioms.
- Every theorem below is **proved** (kernel-checked). Wilf's conjecture itself is only *stated* (`WilfConjecture`), not proved.
  Conjectures TOP'', CL and Tile-CL are only *stated* (`TOP2`, `CL`, `TileCL`); what is proved is the
  implications `TOP2 S → Wilf(S)`, `CL S → Wilf(S)`, and **`TileCL → WilfConjecture`** (`wilfConjecture_of_TileCL`).
  The Ramp Lemma is proved (`rampLemma`); it does not by itself imply Tile-CL (see `.research/PROOFS.md`).

### MaxCL ⇒ Tile-TOP'', Flat-MaxCL, height-≤-2 Wilf (`Wilf/MaxCL.lean`, 2026-10-17)

Kernel-checked (0 `sorry`, axioms `⊆ [propext, Classical.choice, Quot.sound]`). MaxCL in general is only *stated*.
- `MaxCLAt D p : ∀ σ : ZMod m, ∑ y ∈ D.filter (IsMaxCell D), (d + ∑ a, y a) * (tilePhi p y - σ).val ≤
  (d + 1) * ∑ x ∈ D, (tilePhi p x - σ).val`.
- (A) **`tileTOPAt_of_maxCLAt : 1 ≤ d → IsTile D p → MaxCLAt D p → TileTOPAt D p`** (the hypothesis `1 ≤ d` is
  not used by the proof). Uses `m - ⟨s - z⟩ = ⟨z - (s+1)⟩ + 1`, `2·Σ_D r = m(m-1)`, `Σ_{max} (d + |y|) ≤ d·m`.
- (B) **`maxCLAt_of_height_le_two : IsTile D p → (∀ x ∈ D, ∑ a, x a ≤ 2) → MaxCLAt D p`** (Flat-MaxCL; key step
  `sum_edges_le : Σ_{|e|=2} r(e) ≤ (d+1)·Σ_{non-max} r`).
- (C) **`wilf_of_factDownSet_height_le_two (S) : (∀ x ∈ S.factDownSet, ∑ a, x a ≤ 2) → S.conductor ≤ S.embDim * S.ell`**.
- (D) `IsFactTile S D` (finite down-set, `S.wt` a bijection `D → Ap(S,m)`); **`wilf_of_tileTOPAt_of_isFactTile`**
  (Tile-TOP'' ⇒ Wilf for any such `D`), `isFactTile_factDownSet`, the graded-lex factorization set
  `S.factDownSetG` (`grKey` = degree, then lex) with `isFactTile_factDownSetG`, and
  **`wilf_of_apery_height_le_two (S) : (∀ w ∈ S.aperySet S.multiplicity, ∃ x, S.wt x = w ∧ ∑ a, x a ≤ 2) →
  S.conductor ≤ S.embDim * S.ell`**.

### Tile-TOP'' ⇒ Wilf (`Wilf/TileTop.lean`, 2026-10-17)

Kernel-checked (0 `sorry`, axioms `[propext, Classical.choice, Quot.sound]`). Tile-TOP'' itself is only *stated*.
- `TileTOPAt D p : ∀ s : ZMod m, 2 * ∑ y ∈ D.filter (fun y => ∀ a, y + Pi.single a 1 ∉ D),
  (d + ∑ a, y a) * (m - (s - tilePhi p y).val) ≤ m * ((d + 1) * m + d - 1)` (all in `ℕ`; for `m ≥ 1` no subtraction
  truncates); `TileTOP : ∀ d m D p, 1 ≤ d → IsTile D p → TileTOPAt D p`; `IsMaxCell D y : ∀ a, y + Pi.single a 1 ∉ D`
  (`filter_isMaxCell` identifies the filter with `D.filter (IsMaxCell D)`, by `rfl`).
- **`wilf_of_tileTOPAt : TileTOPAt S.factDownSet S.genMod → S.conductor ≤ S.embDim * S.ell`**, for every `S`
  (no `S ≠ nat` hypothesis; only `s = M mod m` is used).
- **`wilfConjecture_of_TileTOP : TileTOP → WilfConjecture`**.
- Proof (as in `.research/PROOFS.md`): CH' (`columnIdentity`); a non-maximal `x ∈ D` has `M - w(x) ≥ m`
  (`multiplicity_le_aperyMax_sub_wt`, via `x + e_b ∈ D`, `wt_le_aperyMax` and `p_b > m`), a maximal one has
  `M - w(x) ≥ ⟨s - φ(x)⟩` (`val_le_aperyMax_sub_wt`); per direction `tileTop_column_bound`, summed with
  `tileTop_sum_columns`, gives `LHS(CH') ≥ d·m² - Σ_{max} (d + |y|)(m - ⟨s - φ(y)⟩)`, and
  `2·d·m² - m((d+1)m + d - 1) = (d - 1)·m(m-1)`.

## Definitions (`Wilf/Basic.lean`, namespace `NumericalSemigroup`)

| Lean | Meaning |
|---|---|
| `structure NumericalSemigroup extends AddSubmonoid ℕ where finite_compl : (carrierᶜ : Set ℕ).Finite` | additive submonoid of ℕ (so `0 ∈ S`, closed under `+`) with finite complement; `S = ℕ` allowed |
| `SetLike`, `AddSubmonoidClass` instances | `n ∈ S`, `zero_mem`, `add_mem`, `nsmul_mem` work |
| `ofPred p h0 hadd N hN` | semigroup `{n | p n}` from a predicate with `p 0`, closure under `+`, and `∀ n ≥ N, p n` |
| `ofClosure A (hA : Nat.setGcd A = 1)` | `AddSubmonoid.closure A` (cofinite by mathlib's `Nat.exists_mem_closure_of_ge`) |
| `nat` | the trivial semigroup `ℕ` (`⊤`) |
| `conductor := sInf {c \| ∀ n, c ≤ n → n ∈ S}` | `c(S)` |
| `gaps : Finset ℕ` (= `ℕ \ S`), `genus := gaps.card` | `g(S)` |
| `left : Finset ℕ` (= `{n ∈ S \| n < c}`), `ell := left.card` | `L(S)`, `ℓ(S)` |
| `multiplicity := sInf {n \| 0 < n ∧ n ∈ S}` | `m(S)` |
| `IsPrimitive n := n ∈ S ∧ 0 < n ∧ ∀ a ∈ S, ∀ b ∈ S, 0 < a → 0 < b → a + b ≠ n` | minimal generator |
| `primitives : Finset ℕ` (= `{n \| IsPrimitive n}`), `embDim := primitives.card` | `e(S)` |
| `WilfConjecture : Prop := ∀ S : NumericalSemigroup, S.conductor ≤ S.embDim * S.ell` | **Wilf's conjecture** |
| `IsSymmetric := ∀ x, x < S.conductor → x ∉ S → S.conductor - 1 - x ∈ S` | symmetric (`ℕ` is vacuously symmetric) |
| `apery n i := sInf {s \| s ∈ S ∧ s % n = i % n}` | least element of `S` that is `≡ i (mod n)` (meaningful for `0 < n`) |
| `kunz i := (S.apery S.multiplicity i - i) / S.multiplicity` | Kunz coordinate `x_i` |

`embDim` is the embedding dimension in the usual sense. `closure_primitives` shows the primitives generate `S`,
and `primitives_subset_of_closure_eq` shows every generating set contains them, so they form the unique
minimal generating set.

## Theorems (all proved, no `sorry`); `S : NumericalSemigroup` is implicit or explicit

Basic API
- `mem_carrier : n ∈ S.carrier ↔ n ∈ S`, `mem_toAddSubmonoid : n ∈ S.toAddSubmonoid ↔ n ∈ S`, `ext`, `finite_setOf_not_mem : {n | n ∉ S}.Finite`
- `mem_ofPred : n ∈ ofPred p h0 hadd N hN ↔ p n`; `mem_ofClosure : n ∈ ofClosure A hA ↔ n ∈ AddSubmonoid.closure A`; `mem_nat n : n ∈ nat`

Conductor
- `exists_forall_ge_mem : ∃ c, ∀ n, c ≤ n → n ∈ S`
- `mem_of_conductor_le : S.conductor ≤ n → n ∈ S`
- `conductor_le_of : (∀ n, c ≤ n → n ∈ S) → S.conductor ≤ c`
- `lt_conductor_of_not_mem : n ∉ S → n < S.conductor`
- `conductor_sub_one_not_mem : 0 < S.conductor → S.conductor - 1 ∉ S` (the Frobenius number is a gap)
- `conductor_eq_iff : S.conductor = c ↔ (∀ n, c ≤ n → n ∈ S) ∧ (0 < c → c - 1 ∉ S)`

Gaps, left elements, genus
- `mem_gaps : n ∈ S.gaps ↔ n ∉ S`; `mem_left : n ∈ S.left ↔ n ∈ S ∧ n < S.conductor`
- `gaps_subset_range : S.gaps ⊆ Finset.range S.conductor`; `left_union_gaps : S.left ∪ S.gaps = Finset.range S.conductor`; `disjoint_left_gaps`
- **`ell_add_genus : S.ell + S.genus = S.conductor`**
- `ell_eq : S.ell = S.conductor - S.genus` (exact: `genus_le_conductor : S.genus ≤ S.conductor`)

Multiplicity
- `exists_pos_mem`, `multiplicity_spec`, `multiplicity_pos : 0 < S.multiplicity`, `multiplicity_mem : S.multiplicity ∈ S`
- `multiplicity_le : 0 < n → n ∈ S → S.multiplicity ≤ n`
- `multiplicity_eq_of : 0 < m → m ∈ S → (∀ n, 0 < n → n < m → n ∉ S) → S.multiplicity = m`
- `not_mem_of_pos_of_lt_multiplicity`, `multiplicity_le_conductor_add_one : S.multiplicity ≤ S.conductor + 1`

Primitives and embedding dimension
- `exists_decomp_of_not_isPrimitive : n ∈ S → 0 < n → ¬ S.IsPrimitive n → ∃ a ∈ S, ∃ b ∈ S, 0 < a ∧ 0 < b ∧ a + b = n`
- `isPrimitive_multiplicity : S.IsPrimitive S.multiplicity`; `multiplicity_mem_primitives`
- `IsPrimitive.lt_conductor_add_multiplicity_add_one : S.IsPrimitive n → n < S.conductor + S.multiplicity + 1` (a crude bound, used only for finiteness)
- `finite_primitives`, `mem_primitives : n ∈ S.primitives ↔ S.IsPrimitive n`
- `mem_induction` (induction over `S` via `0`, primitives, and sums)
- **`closure_primitives : AddSubmonoid.closure (S.primitives : Set ℕ) = S.toAddSubmonoid`**
- **`primitives_subset_of_closure_eq : AddSubmonoid.closure A = S.toAddSubmonoid → (S.primitives : Set ℕ) ⊆ A`**
- **`IsPrimitive.eq_of_mod_eq : S.IsPrimitive p → S.IsPrimitive q → p % S.multiplicity = q % S.multiplicity → p = q`**
- **`embDim_le_multiplicity : S.embDim ≤ S.multiplicity`**; `embDim_pos : 0 < S.embDim`
- `dvd_of_forall_primitive_dvd : (∀ p, S.IsPrimitive p → d ∣ p) → n ∈ S → d ∣ n`
- **`two_le_embDim : S ≠ nat → 2 ≤ S.embDim`**

The trivial semigroup ℕ
- `multiplicity_eq_one_iff : S.multiplicity = 1 ↔ S = nat`; `conductor_eq_zero_iff : S.conductor = 0 ↔ S = nat`
- `conductor_pos_iff : 0 < S.conductor ↔ S ≠ nat`; `one_lt_multiplicity_iff : 1 < S.multiplicity ↔ S ≠ nat`
- `nat_conductor = 0`, `nat_multiplicity = 1`, `nat_gaps = ∅`, `nat_genus = 0`, `nat_left = ∅`, `nat_ell = 0`, `nat_primitives = {1}`, `nat_embDim = 1`
- `wilf_nat : nat.conductor ≤ nat.embDim * nat.ell` (0 ≤ 0)

Wilf statement checks
- **`wilf_iff_int : S.conductor ≤ S.embDim * S.ell ↔ 0 ≤ (S.embDim : ℤ) * ((S.conductor : ℤ) - (S.genus : ℤ)) - (S.conductor : ℤ)`**
- `wilfConjecture_iff_int : WilfConjecture ↔ ∀ S, 0 ≤ (e:ℤ) * ((c:ℤ) - (g:ℤ)) - (c:ℤ)` (no truncated subtraction)

Half-conductor bound and the symmetric case
- `reflect_not_mem : x ∈ S → x < S.conductor → S.conductor - 1 - x ∉ S`
- **`ell_le_genus : S.ell ≤ S.genus`**; **`two_mul_ell_le_conductor : 2 * S.ell ≤ S.conductor`**
- **`wilf_of_conductor_le_two_mul_ell : S.conductor ≤ 2 * S.ell → S.conductor ≤ S.embDim * S.ell`**
- `IsSymmetric.genus_le_ell`, `IsSymmetric.conductor_eq : S.IsSymmetric → S.conductor = 2 * S.ell`
- **`isSymmetric_iff : S.IsSymmetric ↔ S.conductor = 2 * S.ell`**
- **`IsSymmetric.wilf : S.IsSymmetric → S.conductor ≤ S.embDim * S.ell`**
- Because `2ℓ ≤ c` always holds, the hypothesis `c ≤ 2ℓ` holds exactly in the symmetric case, so this special case is no stronger than symmetry.

Apéry sets and Kunz coordinates
- `exists_mem_mod_eq : 0 < n → ∃ s, s ∈ S ∧ s % n = i % n`
- `apery_spec`, `apery_mem : 0 < n → S.apery n i ∈ S`, `apery_mod : 0 < n → S.apery n i % n = i % n`
- `apery_le : s ∈ S → s % n = i % n → S.apery n i ≤ s`; `apery_mod_self : S.apery n (i % n) = S.apery n i`; `apery_zero : S.apery n 0 = 0`
- **`mem_iff_apery_le : n ∈ S → 0 < n → (x ∈ S ↔ S.apery n x ≤ x)`**
- `apery_sub_not_mem : 0 < n → n ≤ S.apery n i → S.apery n i - n ∉ S`
- `le_apery_of_lt : 0 < n → i < n → i ≤ S.apery n i`
- **`genus_eq_sum_apery : n ∈ S → 0 < n → S.genus = ∑ i ∈ Finset.range n, (S.apery n i - i) / n`** (Selmer)
- **`genus_eq_sum_kunz : S.genus = ∑ i ∈ Finset.range S.multiplicity, S.kunz i`**

## Apéry chains: Identity CH, Corollary H, Lemma A, TOP'' (`Wilf/Chains.lean`)

Adversarial verdict: **Identity CH, Corollary H, Lemma A and the implication TOP'' ⇒ Wilf are correct as stated in
`.research/PROOFS.md`.** All are kernel-checked with no extra hypotheses. Several hold in more generality than stated:
the per-direction inequality holds for every `p ∈ S`, `p > 0` (not only `p ∈ P'`) and every Apéry modulus `0 < n ∈ S`;
CH and Corollary H hold for every `S`, including `S = ℕ`. Only Lemma A uses `S ≠ ℕ`, where the paper assumes it anyway.

New definitions (namespace `NumericalSemigroup`; `m = S.multiplicity`, `c = S.conductor`):

| Lean | Meaning |
|---|---|
| `IsApery n w := w ∈ S ∧ (n ≤ w → w - n ∉ S)` | `w ∈ Ap(S,n)` |
| `aperySet n := (range n).image (S.apery n)` | `Ap(S,n)` as a finset (`mem_aperySet : … ↔ IsApery n w`, `card_aperySet : … = n`) |
| `aperyMax n := (aperySet n).sup id` | `M = max Ap(S,n)` (`aperyMax_eq : = c + n - 1`) |
| `nu p w := sSup {k \| k * p ≤ w ∧ w - k * p ∈ S}` | `ν_p(w)` |
| `ht n p w := sSup {k \| IsApery n (w + k * p)}` | height of `w` in its `p`-chain; `w + p·ht` is the chain top |
| `primitives' := primitives.erase m` | `P' = P ∖ {m}` (`card_primitives' : … = e - 1`) |
| `minFactLen u := sInf {L \| ∃ f, Σ_{p∈P'} f p * p = u ∧ Σ_{p∈P'} f p = L}` | `ℓ(u)` (`minFactLen_spec`, `minFactLen_le` show it is the minimum) |
| `topLayer := (aperySet m).filter (fun u => c ≤ u ∧ u < c + m)` | `X_q = Ap ∩ [c, c+m)` |
| `wilfDefect : ℤ := e * ℓ - c` | `W(S)` |
| `defect p : ℤ := m * M - Σ_{w∈Ap} (w + p * ν_p w)` | `Def_p` (chain form: `defect_eq_sum_top`) |
| `excess w : ℤ := Σ_{p∈P'} p * ν_p w - w` | `E(w)` |
| `TOP2 : Prop := Σ_{u∈X_q} (u - c + 1) * ((e - 1) + ℓ u) ≤ m * ((e - 1 + 1) * m + (e - 1) - 1) / 2` | **Conjecture TOP''** (ℕ, literal transcription; `d = e - 1`) |

The paper's chains are treated element by element. Every `w ∈ Ap` lies in the `p`-chain whose top is
`top_p(w) = w + p·ht(w)` (`ht_spec`, `not_isApery_succ_ht`, `isApery_of_le_ht`). So the paper's
`Σ_C |C|·(M − top C)` equals `Σ_{w∈Ap} (M − top_p(w))`, which is how `defect_eq_sum_top` states it.

Main theorems (all proved):
- `IsApery.of_add` (fact (iii), summand closure); `aperyMax_eq : n ∈ S → 0 < n → S.aperyMax n = c + n - 1` (fact (ii));
  `sum_apery_eq : Σ_{i<n} w_i = n·g + Σ_{i<n} i` (Selmer, fact (i)); `exists_fact_of_isApery` (fact (iv)).
- `sum_nu_eq_sum_ht : Σ_{w∈Ap(S,n)} ν_p(w) = Σ_{w∈Ap(S,n)} ht_p(w)` (double counting of pairs `x <_p y` in `Ap`);
  `sum_add_nu_eq_sum_top : Σ_{w∈Ap} (w + p·ν_p w) = Σ_{w∈Ap} (w + p·ht_p w)` (paper step (1)).
- **Deliverable 1** `sum_apery_add_nu_le : n ∈ S → 0 < n → p ∈ S → 0 < p →
  Σ_{i<n} (S.apery n i + p * S.nu p (S.apery n i)) ≤ n * S.aperyMax n`
  (and `sum_apery_add_nu_le_mul_max` for `n = m`; `defect_nonneg : 0 ≤ S.defect p`; `defect_eq_sum_top`).
- **Deliverable 2** `le_sum_nu : IsApery m w → w ≤ Σ_{p∈P'} p * ν_p w`; `excess_nonneg`;
  `le_nu_of_fact : Σ_{q∈P'} f q * q = w → p ∈ P' → f p ≤ ν_p w`.
- **Corollary H** `corollaryH : e * Σ_{i<m} w_i ≤ (e - 1) * m * aperyMax m` (all `S`);
  `corollaryH_int : 2 * (c:ℤ) ≤ 2 * e * ℓ + ((e:ℤ) - 2) * ((m:ℤ) - 1)` (all `S`);
  `corollaryH_nat : S ≠ nat → 2 * c ≤ 2 * e * ℓ + (e - 2) * (m - 1)`.
- **Identity CH** `identityCH : (m:ℤ) * W = Σ_{p∈P'} defect p + Σ_{w∈Ap} excess w - ((e:ℤ) - 1 - 1) * ((m * (m - 1) / 2 : ℕ) : ℤ)`
  (all `S`), and the doubled form `identityCH_two_mul`.
- `sum_add_nu_le_topLayer : p ∈ S → 0 < p → Σ_{w∈Ap} (w + p·ν_p w) ≤ m·(c - 1) + Σ_{u∈X_q} (ν_p u + 1)·(u - c + 1)`
  (the chain step of Lemma A; it only needs "≤ ν_p(u) + 1 elements per chain with top `u`").
- `defect_ge_topLayer : S ≠ nat → … → m² - Σ_{u∈X_q} (ν_p u + 1)·π(u) ≤ defect p`;
  `topLayer_term_le : u ∈ X_q → π(u)·Σ_{p∈P'} (ν_p u + 1) - E(u) ≤ π(u)·(|P'| + ℓ(u))`.
- **Lemma A** `lemmaA : S ≠ nat → (m:ℤ) * ((d + 1) * m + d - 1) / 2 - Σ_{u∈X_q} π(u)·(d + ℓ u) + Σ_{w∈Ap∖X_q} E(w) ≤ m * W`
  with `d = (e:ℤ) - 1`, `π(u) = (u:ℤ) - c + 1` (`ℤ` division; the numerator is even). Doubled form: `lemmaA_two_mul`.
- **TOP'' ⇒ Wilf** `wilf_of_TOP2 : S.TOP2 → S.conductor ≤ S.embDim * S.ell` (every `S`; `ℕ` handled separately);
  `wilfConjecture_of_TOP2 : (∀ S, S.TOP2) → WilfConjecture`.

Sanity checks in `Wilf/Examples.lean`:
- `S35_TOP2_eq`: for `⟨3,5⟩` (`W = 0`), `X_q = {10}`, `ℓ(10) = 2`, and TOP'' reads `9 ≤ 9` (equality). Hence `S35_TOP2`.
- `S357_TOP2_vals`: for `⟨3,5,7⟩` (`W = 1`), `X_q = {5,7}`, `ℓ = 1` on both, and TOP'' reads `12 ≤ 15`. Hence `S357_TOP2`.

Independent numerical cross-check by the Lean agent (scratchpad script `check_ch.py`, not in the repo): the exact
formalized forms were tested on all 6,963 semigroups with `S ≠ ℕ` and genus ≤ 15, with 0 failures. The script checked
CH (with `Def_p` computed from literal maximal chains), Corollary H and its consequence, Lemma A, and the
per-direction and refined top-layer bounds for every `p ∈ S` with `p ≤ c + 2m`. TOP'' also had 0 failures there.

## Factorization down-set, CH', CL (`Wilf/Carry.lean`)

Verdict: the "Factorization down-set D and column identity CH'" section and "CL ⇒ Wilf" in `.research/PROOFS.md`
are correct as stated, with no extra hypotheses. CH' and `CL ⇒ Wilf` hold for every `S`, including `S = ℕ`.

**Monomial order:** lexicographic order (`toLex`) on `Fin d → ℕ`. `P'` is indexed increasingly
(`gen a = S.primitives'.orderEmbOfFin rfl a`), so coordinate `0`, the smallest generator in `P'`, is the most
significant. The down-set proof only uses that `toLex` is a linear order compatible with `+` and cancellative
(mathlib's `Pi.Lex.isOrderedCancelAddMonoid`), so any such order would work.

Definitions (`d = |P'| = e - 1`, `ι = Fin d`):

| Lean | Meaning |
|---|---|
| `IsDownSetFin D := ∀ x ∈ D, ∀ y, y ≤ x → y ∈ D` | finite down-set of `ι → ℕ` (componentwise order) |
| `colHt D a x := sSup {k \| x + Pi.single a k ∈ D}` | height of `x` in its `a`-column |
| `gen : Fin d → ℕ` | `p_a`, the elements of `P'` in increasing order |
| `wt x := Σ_a x a * gen a` | `w(x) = ⟨x, p⟩` |
| `factSet w := (piFinset (fun _ => range (w+1))).filter (wt · = w)` | factorizations of `w` (`mem_factSet : x ∈ factSet w ↔ wt x = w`) |
| `nf w := ofLex (min' ((factSet w).image toLex))` (junk `0` if no factorization) | `n(w)`, the lex-least factorization |
| `factDownSet := (aperySet m).image nf` | `D` |
| `CL : Prop := ((e:ℤ)-1-1) * ((m*(m-1)/2 : ℕ):ℤ) ≤ Σ_a Σ_{x∈D, x+e_a∉D} ((x a:ℤ)+1) * (((M:ℤ) - wt x) % m)` | **Conjecture CL** (for lex order) |
| `tilePhi p x := Σ_a (x a : ZMod m) * p a`; `tileT D y := Σ_{a : y+e_a∉D} (y a + 1)` | `φ`, `T` |
| `IsTile D p := IsDownSetFin D ∧ D.card = m ∧ Set.BijOn (tilePhi p) D univ` | tile hypotheses |
| `TileCLAt D p := ∀ s : ZMod m, (d-1) * (m*(m-1)/2) ≤ Σ_{y∈D} tileT D y * (s - tilePhi p y).val` | Tile-CL for one tile (`⟨x⟩ = ZMod.val`) |
| `TileCL : Prop := ∀ d m D p, 1 ≤ d → IsTile D p → TileCLAt D p` | **Conjecture Tile-CL** (statement only) |

Theorems (all proved):
- `sum_columns : IsDownSetFin D → Σ_{x∈D} F x = Σ_{y∈D, y+e_a∉D} Σ_{k<y_a+1} F (y - Pi.single a k)`
  (columns are `{y - k·e_a | k ≤ y_a}`); `card_eq_sum_columns : D.card = Σ_{a-tops y} (y a + 1)`.
- `sum_wt_add_eq_columns : Σ_{x∈D} (w(x) + p_a·x_a) = Σ_{a-tops y} (y_a + 1)·w(y)` (in `ℤ`, any weights `p`).
- `exists_wt_eq : IsApery m w → ∃ x, wt x = w`; `nf_spec : IsApery m w → wt (nf w) = w ∧ ∀ x, wt x = w → toLex (nf w) ≤ toLex x`.
- **(b)** `nf_downward : IsApery m w → y ≤ nf w → IsApery m (wt y) ∧ nf (wt y) = y`;
  `isDownSetFin_factDownSet : IsDownSetFin S.factDownSet`.
- **(a)** `nf_injOn : Set.InjOn S.nf (aperySet m)`; `card_factDownSet : S.factDownSet.card = S.multiplicity`.
- `dmM_sub_sum_apery : d·m·M - (d+1)·ΣAp = m·W + (d-1)·(m(m-1)/2)` (in `ℤ`, `d = |P'|`).
- **CH'** `columnIdentity : Σ_a Σ_{x∈D, x+e_a∉D} ((x a:ℤ)+1)·((M:ℤ) - wt x) = m·W + ((e:ℤ)-1-1)·((m(m-1)/2 : ℕ):ℤ)`.
- **CL ⇒ Wilf** `wilf_of_CL : S.CL → S.conductor ≤ S.embDim * S.ell`; `wilfConjecture_of_CL : (∀ S, S.CL) → WilfConjecture`.
- `IsTile.mk'`: builds `IsTile` from a down-set proof, `card = m`, and Finset-bounded injectivity/surjectivity
  that `decide` can check.

Tile-CL sanity checks (`Wilf/Examples.lean`, `decide` only, no `native_decide`):
- `tile1` (`d=2`, `D={00,01,10}`, `m=3`, `p=(1,2)`): `tile1_isTile`, `tile1_TileCLAt`. It is tight at `s = 2` (`f = 3`, `tile1_tight`).
- `tile2` (`d=1`, `D={0,1,2}`, `m=3`, `p=(1)`): `tile2_isTile`, `tile2_TileCLAt`.
- `tile3` (`d=2`, box `{0,1,2}×{0,1}`, `m=6`, `p=(2,1)`): `tile3_isTile`, `tile3_TileCLAt`. It is tight at `s = 5` (`f = 15`, `tile3_tight`).

Independent numerical check by the Lean agent (scratchpad script `check_cl.py`, not in the repo). It uses the lex
order exactly as formalized, on all 19,814 semigroups with `S ≠ ℕ` and genus ≤ 17. Results: `D` is a down-set with
`|D| = m`, CH' holds exactly, and CL(lex) holds, with 0 failures in each case.

## Tile-CL ⇒ Wilf (`Wilf/TileReduction.lean`)

Verdict: the remark "CL for `S` is Tile-CL for `(D, p mod m)` at `s = M mod m`" in `.research/PROOFS.md` is correct as
stated. `TileCL`, `CL`, `IsTile`, `TileCLAt` and `WilfConjecture` are used **unchanged** (as defined in `Carry.lean`/`Basic.lean`).

| Lean | Meaning |
|---|---|
| `genMod S a := (S.gen a : ZMod S.multiplicity)` | `p_a mod m` for `p_a ∈ P'` |

Theorems (all proved; `S` implicit; `d = S.primitives'.card`, `m = S.multiplicity`, `M = S.aperyMax m`, `D = S.factDownSet`):
- `IsApery.eq_of_mod_eq : n ∈ S → 0 < n → S.IsApery n w₁ → S.IsApery n w₂ → w₁ % n = w₂ % n → w₁ = w₂`
- `tilePhi_genMod : tilePhi S.genMod x = ((S.wt x : ℕ) : ZMod m)`
- **`isTile_factDownSet : IsTile S.factDownSet S.genMod`** (every `S`): down-set, `|D| = m`, and `φ` bijective `D → ℤ/m`
  (injective since distinct cells have distinct Apéry values, which are distinct mod `m`; surjective via `nf (apery m s.val)`).
- `val_aperyMax_sub_tilePhi : (((M : ZMod m) - tilePhi S.genMod y).val : ℤ) = ((M:ℤ) - S.wt y) % m`
- `CL_sum_eq_tile_sum : Σ_a Σ_{x∈D, x+e_a∉D} ((x a:ℤ)+1)·(((M:ℤ) - wt x) % m) = ((Σ_{y∈D} tileT D y * ((M : ZMod m) - tilePhi S.genMod y).val : ℕ) : ℤ)`
  (exchange of summation).
- **`CL_iff_tileCLAt_aperyMax : S.CL ↔ (d - 1) * (m * (m - 1) / 2) ≤ Σ_{y∈D} tileT D y * ((M : ZMod m) - tilePhi S.genMod y).val`**
  (every `S`, including `ℕ`: for `d = 0` one has `S = ℕ`, `m = 1`, and both left-hand sides are `0`; for `d ≥ 1`,
  `(e:ℤ) - 1 - 1 = ((d - 1 : ℕ) : ℤ)` exactly).
- `CL_of_tileCLAt : TileCLAt S.factDownSet S.genMod → S.CL` (uses only the instance `s = M mod m`).
- **`wilfConjecture_of_TileCL : TileCL → WilfConjecture`**. `S = ℕ` is `wilf_nat`; for `S ≠ ℕ`, `d = e - 1 ≥ 1`
  (`two_le_embDim`), so `TileCL` applies to the tile `(D, p mod m)` and `wilf_of_CL` finishes.

## The Ramp Lemma (`Wilf/Ramp.lean`)

Verdict: the Ramp Lemma of `.research/PROOFS.md` is correct as stated (any finite down-set, no tiling hypothesis), and holds
for `ρ` with values in any linearly ordered commutative ring `K` (`[CommRing K] [LinearOrder K] [IsStrictOrderedRing K]`:
`ℤ`, `ℚ`, `ℝ`, ...), not only `ℝ`. The proof replaces the lexicographic path of step (1) by an order-free induction.

| Lean | Meaning |
|---|---|
| `DirConvex ρ := ∀ a b u, ρ (u + e_a) - ρ u ≤ ρ (u + e_b + e_a) - ρ (u + e_b)` (`e_a = Pi.single a 1`) | `Δ_a ρ(u) ≤ Δ_a ρ(u + e_b)` for all `a, b` (`b = a` included), `ρ : (ι → ℕ) → K` |
| `tileBeta D y : ℤ := (d : ℤ) + 1 - tileT D y` | `β(y) = d + 1 - T(y)` |

Theorems (all proved):
- `pi_nat_induction`: a predicate on `ι → ℕ` holding at `0` and every `e_b` and closed under `+` holds everywhere.
- `DirConvex.delta_mono : DirConvex ρ → ρ (u + e_a) - ρ u ≤ ρ (u + w + e_a) - ρ (u + w)`.
- **`DirConvex.incr_mono : DirConvex ρ → u ≤ v → ρ (u + w) - ρ u ≤ ρ (v + w) - ρ v`** (increasing differences).
- Step 1 `DirConvex.sub_zero_le_sum_sub : DirConvex ρ → ρ x - ρ 0 ≤ Σ_a (ρ x - ρ (x - Pi.single a (x a)))`.
- Step 2 `DirConvex.column_ineq : Σ_{k<y_a+1} (ρ (y - k e_a) - ρ (y - y_a e_a)) ≤ Σ_{k<y_a+1} (ρ y - ρ (y - k e_a))`, and
  `DirConvex.direction_ineq : IsDownSetFin D → Σ_{x∈D} (ρ x - ρ (x - x_a e_a)) ≤ Σ_{y∈D, y+e_a∉D} ((y a : K) + 1) * ρ y - Σ_{x∈D} ρ x`.
- `sum_tileT_mul : Σ_{y∈D} (tileT D y : R) * f y = Σ_a Σ_{y∈D, y+e_a∉D} ((y a : R) + 1) * f y` (any `CommRing R`).
- **`rampLemma : IsDownSetFin D → DirConvex ρ → Σ_{y∈D} (tileBeta D y : K) * ρ y ≤ (D.card : K) * ρ 0`**
  (`D : Finset (Fin d → ℕ)`, `ρ : (Fin d → ℕ) → K`; every `d`, including `d = 0`, and `D = ∅`).
- `rampLemma_concave : IsDownSetFin D → DirConvex (fun y => -ρ y) → (D.card : K) * ρ 0 ≤ Σ_{y∈D} (tileBeta D y : K) * ρ y`;
  `rampLemma_eq` (both hypotheses, i.e. affine-type `ρ`): equality.
- Instance: `incr_mono_of_convex` and **`dirConvex_comp_linear : (∀ n, g (n+1) - g n ≤ g (n+2) - g (n+1)) → DirConvex (fun y => g (Σ_b q b * y b))`**
  for `g : ℕ → K`, `q : ι → ℕ` (the paper's `ρ = g(⟨y,q⟩)`, here with `q ∈ ℕ^d` and `g` defined on `ℕ`; real `q` is not formalized).

## Kernel-checked examples (`Wilf/Examples.lean`, namespace `NumericalSemigroup.Examples`)

Each example is built with `ofPred`, and its generating set is certified by `*_eq_closure : S.toAddSubmonoid = AddSubmonoid.closure {…}`.

| semigroup | proved facts |
|---|---|
| `S357 = ⟨3,5,7⟩` | `conductor = 5`, `gaps = {1,2,4}`, `genus = 3`, `left = {0,3}`, `ell = 2`, `multiplicity = 3`, `primitives = {3,5,7}`, `embDim = 3`, `S357_eq_closure`, `S357_wilf` (5 ≤ 6), `apery 3 1 = 7`, `apery 3 2 = 5`, `S357_selmer_check` |
| `S469 = ⟨4,6,9⟩` | `conductor = 12`, `gaps = {1,2,3,5,7,11}`, `genus = 6`, `left = {0,4,6,8,9,10}`, `ell = 6`, `multiplicity = 4`, `primitives = {4,6,9}`, `embDim = 3`, `S469_eq_closure`, `S469_wilf` (12 ≤ 18) |
| `S35 = ⟨3,5⟩` | `conductor = 8`, `gaps = {1,2,4,7}`, `genus = 4`, `left = {0,3,5,6}`, `ell = 4`, `primitives = {3,5}`, `embDim = 2`, `S35_eq_closure`, `S35_isSymmetric`, `S35_wilf_eq : c = e·ℓ` (8 = 8, the equality case) |
| `nat = ℕ` (in Basic) | `c = g = ℓ = 0`, `m = e = 1`, `wilf_nat` |
| TOP'' checks | `S35_multiplicity = 3`, `S35_aperySet : aperySet 3 = {0,10,5}`, `S35_topLayer = {10}`, `S35_primitives' = {5}`, `S35_minFactLen_ten = 2`, `S35_TOP2_eq`, `S35_TOP2`; `S357_aperySet = {0,7,5}`, `S357_topLayer = {7,5}`, `S357_primitives' = {5,7}`, `S357_minFactLen`, `S357_TOP2_vals`, `S357_TOP2` |

## `#print axioms` output (`lake env lean scripts/PrintAxioms.lean`)

Tile-reduction / Ramp round: the 20 new entries (`IsApery.eq_of_mod_eq, tilePhi_genMod, isTile_factDownSet,
val_aperyMax_sub_tilePhi, CL_sum_eq_tile_sum, CL_iff_tileCLAt_aperyMax, CL_of_tileCLAt, wilfConjecture_of_TileCL,
pi_nat_induction, DirConvex.delta_mono, DirConvex.incr_mono, DirConvex.sub_zero_le_sum_sub, DirConvex.column_ineq,
DirConvex.direction_ineq, sum_tileT_mul, rampLemma, rampLemma_concave, rampLemma_eq, incr_mono_of_convex,
dirConvex_comp_linear`) all report `[propext, Classical.choice, Quot.sound]`; all 115 entries are standard.

Carry round: the 27 new entries (`sum_columns, card_eq_sum_columns, sum_wt_add_eq_columns, exists_wt_eq,
mem_factSet, nf_spec, wt_nf, nf_downward, isDownSetFin_factDownSet, nf_injOn, card_factDownSet, sum_wt_factDownSet,
dmM_sub_sum_apery, columnIdentity, CL, wilf_of_CL, wilfConjecture_of_CL, TileCL, IsTile.mk', Examples.tile{1,2,3}_isTile,
Examples.tile{1,2,3}_TileCLAt, Examples.tile1_tight, Examples.tile3_tight`) all report
`[propext, Classical.choice, Quot.sound]`, so all 95 entries are standard. No `native_decide` is used anywhere.

All 68 declarations listed in `scripts/PrintAxioms.lean` report exactly
`depends on axioms: [propext, Classical.choice, Quot.sound]`. These are the 36 Basic and Examples items listed in an
earlier round, plus the Chains items: `mem_aperySet, card_aperySet, aperyMax_eq, sum_apery_eq, sum_nu_eq_sum_ht,
sum_add_nu_eq_sum_top, sum_apery_add_nu_le, sum_apery_add_nu_le_mul_max, defect_eq_sum_top, defect_nonneg,
exists_fact_of_isApery, le_nu_of_fact, le_sum_nu, excess_nonneg, corollaryH, corollaryH_int, corollaryH_nat,
identityCH_two_mul, identityCH, minFactLen_spec, minFactLen_le, sum_add_nu_le_topLayer, defect_ge_topLayer,
topLayer_term_le, lemmaA_two_mul, lemmaA, TOP2, wilf_of_TOP2, wilfConjecture_of_TOP2, Examples.S35_TOP2,
Examples.S35_TOP2_eq, Examples.S357_TOP2`. The Basic and Examples items are `ell_add_genus, ell_eq, conductor_eq_iff,
conductor_sub_one_not_mem, isPrimitive_multiplicity, IsPrimitive.eq_of_mod_eq, embDim_le_multiplicity, embDim_pos,
closure_primitives, primitives_subset_of_closure_eq, mem_induction, two_le_embDim, multiplicity_eq_one_iff,
conductor_eq_zero_iff, nat_embDim, wilf_iff_int, wilfConjecture_iff_int, wilf_nat, ell_le_genus,
two_mul_ell_le_conductor, wilf_of_conductor_le_two_mul_ell, isSymmetric_iff, IsSymmetric.wilf, mem_iff_apery_le,
apery_sub_not_mem, genus_eq_sum_apery, genus_eq_sum_kunz, Examples.S357_primitives, Examples.S357_eq_closure,
Examples.S357_wilf, Examples.S357_selmer_check, Examples.S469_wilf, Examples.S469_eq_closure,
Examples.S35_isSymmetric, Examples.S35_wilf_eq, WilfConjecture`.

## Conventions and pitfalls (for reviewing research lemmas)

- `S = ℕ` is a `NumericalSemigroup` with `c = 0`, `ℓ = 0`, `e = 1`, `m = 1`. Wilf holds trivially (`0 ≤ 0`).
- `ℓ` is `card (S ∩ [0,c))`, **not** `c - g` with truncated subtraction (they agree, by `ell_add_genus`).
- The Frobenius number is `c - 1` when `c > 0`; it is not defined as a separate quantity (it would be `-1` for ℕ).
- `apery n i` is defined for every `n`, but its lemmas need `0 < n` (and `n ∈ S` for `mem_iff_apery_le` and Selmer).
  For `n = 0` it is junk: `apery 0 i = i` if `i ∈ S`, and `0` otherwise.
- `kunz i` is meaningful for `i < m`; `kunz 0 = 0`.
- `nu p w`, `ht n p w` need `0 < p` (and `w ∈ S`, resp. `IsApery n w`) for their lemmas. `minFactLen u` is junk (`0`)
  when `u` has no factorization over `P'`; it is meaningful on `Ap(S,m)` (`minFactLen_spec`).
- In `TOP2` all subtractions are exact for `S ≠ ℕ`: `u ≥ c` on `X_q`, `e ≥ 2`, and `(e-1+1)·m + (e-1) ≥ 1`.
  The `/ 2` is floor division, but `Σ ≤ X / 2 ↔ 2·Σ ≤ X` holds for naturals anyway (`Nat.le_div_iff_mul_le`).
- The definitions are noncomputable (`sInf`, `Set.Finite.toFinset`). Concrete values are proved through the
  characterisation lemmas (`conductor_eq_iff`, `multiplicity_eq_of`, `mem_gaps`, `mem_left`, `mem_primitives`) together with `omega`.
