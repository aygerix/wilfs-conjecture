import Wilf.Basic
import Mathlib.Algebra.BigOperators.Intervals
import Mathlib.Algebra.Ring.Int.Parity
import Mathlib.Tactic.LinearCombination

/-!
# Apéry chains: Identity CH, Corollary H, Lemma A, and `TOP'' ⇒ Wilf`

Formalization of the statements in `.research/PROOFS.md` (2026-10-17).

Notation (for a fixed `S`): `m = S.multiplicity`, `A = S.aperySet m` (the Apéry set `Ap(S,m)` as a
finset), `M = S.aperyMax m = max A`, `c = S.conductor`, `P' = S.primitives'` (`= P ∖ {m}`),
`d = |P'| = e - 1`, `ν_p(w) = S.nu p w = max {k | k·p ≤ w ∧ w - k·p ∈ S}`,
`X_q = S.topLayer = A ∩ [c, c+m)`, `ℓ(u) = S.minFactLen u` (shortest factorization length over `P'`).

The paper's `p`-chains (maximal arithmetic progressions of difference `p` inside `A`) are handled
element-wise: `S.ht n p w` is the number of steps from `w` up to the top of its chain, so
`w + p·ht(w)` is the top of the chain through `w` (`ht_spec`, `not_isApery_succ_ht`), and the
chain-sum `Σ_C |C|·top(C)` is `Σ_{w∈A} (w + p·ht(w))`.
-/

namespace NumericalSemigroup

open Finset

variable (S : NumericalSemigroup)

/-! ### The Apéry set as a predicate and as a finset -/

/-- `w` lies in the Apéry set of `S` with respect to `n`: `w ∈ S` and `w - n ∉ S`. -/
def IsApery (n w : ℕ) : Prop := w ∈ S ∧ (n ≤ w → w - n ∉ S)

/-- The Apéry set `Ap(S, n) = {S.apery n i | i < n}` as a finset. -/
noncomputable def aperySet (n : ℕ) : Finset ℕ := (range n).image (S.apery n)

/-- `max Ap(S, n)` (as `Finset.sup`; equal to `c + n - 1` by `aperyMax_eq`). -/
noncomputable def aperyMax (n : ℕ) : ℕ := (S.aperySet n).sup id

/-- `ν_p(w) = max {k | k·p ≤ w ∧ w - k·p ∈ S}`. -/
noncomputable def nu (p w : ℕ) : ℕ := sSup {k | k * p ≤ w ∧ w - k * p ∈ S}

/-- Height of `w` in its `p`-chain inside `Ap(S,n)`: `max {k | w + k·p ∈ Ap(S,n)}`. -/
noncomputable def ht (n p w : ℕ) : ℕ := sSup {k | S.IsApery n (w + k * p)}

/-- `P' = P ∖ {m}`: the primitive elements other than the multiplicity. -/
noncomputable def primitives' : Finset ℕ := S.primitives.erase S.multiplicity

/-- `ℓ(u)`: the minimal length `Σ_p f(p)` of a factorization `u = Σ_{p∈P'} f(p)·p` over `P'`
(junk value `0` if `u` has no such factorization). -/
noncomputable def minFactLen (u : ℕ) : ℕ :=
  sInf {L | ∃ f : ℕ → ℕ, ∑ p ∈ S.primitives', f p * p = u ∧ ∑ p ∈ S.primitives', f p = L}

/-- The top layer `X_q = Ap(S,m) ∩ [c, c+m)`. -/
noncomputable def topLayer : Finset ℕ :=
  (S.aperySet S.multiplicity).filter
    (fun u => S.conductor ≤ u ∧ u < S.conductor + S.multiplicity)

/-- Wilf defect `W(S) = e·ℓ - c` (in `ℤ`). -/
noncomputable def wilfDefect : ℤ := (S.embDim : ℤ) * S.ell - S.conductor

/-- `Def_p = m·M - Σ_{w∈Ap} (w + p·ν_p(w))` (in `ℤ`); see `defect_eq_sum_top` for the chain form
`Σ_{w∈Ap} (M - top_p(w))`. -/
noncomputable def defect (p : ℕ) : ℤ :=
  (S.multiplicity : ℤ) * S.aperyMax S.multiplicity -
    ∑ w ∈ S.aperySet S.multiplicity, ((w : ℤ) + p * S.nu p w)

/-- `E(w) = Σ_{p∈P'} p·ν_p(w) - w` (in `ℤ`). -/
noncomputable def excess (w : ℕ) : ℤ := ∑ p ∈ S.primitives', (p : ℤ) * S.nu p w - w

variable {S}

/-! ### Basic facts on Apéry sets -/

theorem isApery_apery {n : ℕ} (hn : 0 < n) (i : ℕ) : S.IsApery n (S.apery n i) :=
  ⟨S.apery_mem hn i, S.apery_sub_not_mem hn i⟩

theorem apery_eq_self_of_isApery {n w : ℕ} (hnS : n ∈ S) (hn : 0 < n) (hw : S.IsApery n w) :
    S.apery n w = w := by
  apply le_antisymm (S.apery_le hw.1 rfl)
  by_contra hlt
  push Not at hlt
  obtain ⟨k, hk⟩ : n ∣ w - S.apery n w :=
    Nat.dvd_of_mod_eq_zero (Nat.sub_mod_eq_zero_of_mod_eq (S.apery_mod hn w).symm)
  have hk0 : k ≠ 0 := by rintro rfl; omega
  have hmk : n * (k - 1) = n * k - n := Nat.mul_sub_one _ _
  have hle : n ≤ n * k := Nat.le_mul_of_pos_right _ (by omega)
  apply hw.2 (by omega)
  have : w - n = S.apery n w + (k - 1) • n := by rw [smul_eq_mul, mul_comm]; omega
  rw [this]
  exact add_mem (S.apery_mem hn w) (nsmul_mem hnS _)

theorem mem_aperySet {n w : ℕ} (hnS : n ∈ S) (hn : 0 < n) :
    w ∈ S.aperySet n ↔ S.IsApery n w := by
  constructor
  · intro h
    obtain ⟨i, -, rfl⟩ := Finset.mem_image.1 h
    exact isApery_apery hn i
  · intro h
    refine Finset.mem_image.2 ⟨w % n, Finset.mem_range.2 (Nat.mod_lt _ hn), ?_⟩
    rw [S.apery_mod_self, apery_eq_self_of_isApery hnS hn h]

theorem apery_injOn {n : ℕ} (hn : 0 < n) : Set.InjOn (S.apery n) (range n : Set ℕ) := by
  intro i hi j hj h
  have hi' := Finset.mem_range.1 (Finset.mem_coe.1 hi)
  have hj' := Finset.mem_range.1 (Finset.mem_coe.1 hj)
  have h1 := S.apery_mod hn i
  have h2 := S.apery_mod hn j
  rw [h] at h1
  have := h1.symm.trans h2
  rwa [Nat.mod_eq_of_lt hi', Nat.mod_eq_of_lt hj'] at this

theorem card_aperySet {n : ℕ} (hn : 0 < n) : (S.aperySet n).card = n := by
  rw [aperySet, Finset.card_image_of_injOn (apery_injOn hn), Finset.card_range]

theorem sum_aperySet {β : Type*} [AddCommMonoid β] {n : ℕ} (hn : 0 < n) (f : ℕ → β) :
    ∑ w ∈ S.aperySet n, f w = ∑ i ∈ range n, f (S.apery n i) := by
  rw [aperySet, Finset.sum_image (apery_injOn hn)]

/-- Summand closure: if `w = x + y ∈ Ap` with `x, y ∈ S` then `x ∈ Ap`. -/
theorem IsApery.of_add {n w x y : ℕ} (hw : S.IsApery n w) (hx : x ∈ S) (hy : y ∈ S)
    (h : x + y = w) : S.IsApery n x := by
  refine ⟨hx, fun hnx hxn => hw.2 (by omega) ?_⟩
  have := add_mem hxn hy
  rwa [show x - n + y = w - n by omega] at this

theorem IsApery.lt {n w : ℕ} (hw : S.IsApery n w) : w < S.conductor + n := by
  by_cases h : n ≤ w
  · have := S.lt_conductor_of_not_mem (hw.2 h); omega
  · omega

theorem isApery_conductor_add_sub_one {n : ℕ} (hn : 0 < n) :
    S.IsApery n (S.conductor + n - 1) := by
  refine ⟨S.mem_of_conductor_le (by omega), fun h => ?_⟩
  rw [show S.conductor + n - 1 - n = S.conductor - 1 by omega]
  exact S.conductor_sub_one_not_mem (by omega)

theorem le_aperyMax {n w : ℕ} (hw : w ∈ S.aperySet n) : w ≤ S.aperyMax n :=
  Finset.le_sup (f := id) hw

/-- **Brauer–Shockley**: `max Ap(S,n) = c + n - 1` (`= F + n`). -/
theorem aperyMax_eq {n : ℕ} (hnS : n ∈ S) (hn : 0 < n) :
    S.aperyMax n = S.conductor + n - 1 := by
  apply le_antisymm
  · apply Finset.sup_le
    intro w hw
    have := ((mem_aperySet hnS hn).1 hw).lt
    simp only [id]
    omega
  · exact le_aperyMax ((mem_aperySet hnS hn).2 (isApery_conductor_add_sub_one hn))

/-- Selmer, in additive form: `Σ_{i<n} w_i = n·g + Σ_{i<n} i`. -/
theorem sum_apery_eq {n : ℕ} (hnS : n ∈ S) (hn : 0 < n) :
    ∑ i ∈ range n, S.apery n i = n * S.genus + ∑ i ∈ range n, i := by
  rw [S.genus_eq_sum_apery hnS hn, Finset.mul_sum, ← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl fun i hi => ?_
  have hi' := Finset.mem_range.1 hi
  have hle := S.le_apery_of_lt hn hi'
  have hdvd : n ∣ S.apery n i - i :=
    Nat.dvd_of_mod_eq_zero (Nat.sub_mod_eq_zero_of_mod_eq (S.apery_mod hn i))
  rw [Nat.mul_div_cancel' hdvd]
  omega

/-! ### `ν_p` -/

theorem nu_bdd {p : ℕ} (hp : 0 < p) (w : ℕ) : BddAbove {k | k * p ≤ w ∧ w - k * p ∈ S} :=
  ⟨w, fun k hk => le_trans (Nat.le_mul_of_pos_right k hp) hk.1⟩

theorem nu_spec {p w : ℕ} (hp : 0 < p) (hw : w ∈ S) :
    S.nu p w * p ≤ w ∧ w - S.nu p w * p ∈ S :=
  Nat.sSup_mem ⟨0, by simpa using hw⟩ (nu_bdd hp w)

theorem le_nu {p w k : ℕ} (hp : 0 < p) (h1 : k * p ≤ w) (h2 : w - k * p ∈ S) :
    k ≤ S.nu p w :=
  le_csSup (nu_bdd hp w) ⟨h1, h2⟩

theorem sub_mem_of_le_nu {p w k : ℕ} (hpS : p ∈ S) (hp : 0 < p) (hw : w ∈ S)
    (hk : k ≤ S.nu p w) : k * p ≤ w ∧ w - k * p ∈ S := by
  obtain ⟨h1, h2⟩ := nu_spec hp hw
  have hkp : k * p ≤ S.nu p w * p := Nat.mul_le_mul_right p hk
  refine ⟨le_trans hkp h1, ?_⟩
  have : w - k * p = (w - S.nu p w * p) + (S.nu p w - k) • p := by
    rw [smul_eq_mul, Nat.sub_mul]; omega
  rw [this]
  exact add_mem h2 (nsmul_mem hpS _)

theorem mul_mem {p : ℕ} (hpS : p ∈ S) (k : ℕ) : k * p ∈ S := by
  simpa [smul_eq_mul] using nsmul_mem hpS k

/-! ### Heights in `p`-chains -/

theorem ht_bdd {n p w : ℕ} (hp : 0 < p) : BddAbove {k | S.IsApery n (w + k * p)} :=
  ⟨S.conductor + n, fun k hk => by
    have := (show S.IsApery n (w + k * p) from hk).lt
    have := Nat.le_mul_of_pos_right k hp
    omega⟩

theorem ht_spec {n p w : ℕ} (hp : 0 < p) (hw : S.IsApery n w) :
    S.IsApery n (w + S.ht n p w * p) :=
  Nat.sSup_mem ⟨0, by simpa using hw⟩ (ht_bdd hp)

theorem le_ht {n p w k : ℕ} (hp : 0 < p) (h : S.IsApery n (w + k * p)) : k ≤ S.ht n p w :=
  le_csSup (ht_bdd hp) h

/-- The top `w + p·ht(w)` of the chain through `w` is indeed a top: one more step leaves `Ap`. -/
theorem not_isApery_succ_ht {n p w : ℕ} (hp : 0 < p) :
    ¬ S.IsApery n (w + (S.ht n p w + 1) * p) := fun h => by
  have := le_ht hp h; omega

theorem isApery_of_le_ht {n p w k : ℕ} (hpS : p ∈ S) (hp : 0 < p) (hw : S.IsApery n w)
    (hk : k ≤ S.ht n p w) : S.IsApery n (w + k * p) := by
  have htop := ht_spec hp hw
  refine htop.of_add (add_mem hw.1 (mul_mem hpS k)) (mul_mem hpS (S.ht n p w - k)) ?_
  rw [Nat.sub_mul]
  have : k * p ≤ S.ht n p w * p := Nat.mul_le_mul_right p hk
  omega

/-! ### Double counting: `Σ_{w∈Ap} ν_p(w) = Σ_{w∈Ap} ht_p(w)` (paper step (1)) -/

theorem sum_nu_eq_sum_ht {n p : ℕ} (hnS : n ∈ S) (hn : 0 < n) (hpS : p ∈ S) (hp : 0 < p) :
    ∑ w ∈ S.aperySet n, S.nu p w = ∑ w ∈ S.aperySet n, S.ht n p w := by
  classical
  set A := S.aperySet n with hA
  let R : ℕ → ℕ → Prop := fun x y => ∃ k, 0 < k ∧ y = x + k * p
  have h1 : ∀ y ∈ A, S.nu p y = (A.filter (fun x => R x y)).card := by
    intro y hy
    have hy' := (mem_aperySet hnS hn).1 hy
    have hset : A.filter (fun x => R x y) =
        (Finset.Icc 1 (S.nu p y)).image (fun k => y - k * p) := by
      ext x
      simp only [Finset.mem_filter, Finset.mem_image, Finset.mem_Icc, R]
      constructor
      · rintro ⟨hx, k, hk, rfl⟩
        have hxS := ((mem_aperySet hnS hn).1 hx).1
        refine ⟨k, ⟨hk, le_nu hp (by omega) ?_⟩, by omega⟩
        rwa [show x + k * p - k * p = x by omega]
      · rintro ⟨k, ⟨hk1, hk2⟩, rfl⟩
        obtain ⟨hle, hmem⟩ := sub_mem_of_le_nu hpS hp hy'.1 hk2
        exact ⟨(mem_aperySet hnS hn).2 (hy'.of_add hmem (mul_mem hpS k) (by omega)), k, hk1,
          by omega⟩
    rw [hset, Finset.card_image_of_injOn, Nat.card_Icc]
    · omega
    · intro k1 hk1 k2 hk2 h
      have h1 := (sub_mem_of_le_nu hpS hp hy'.1 (Finset.mem_Icc.1 (Finset.mem_coe.1 hk1)).2).1
      have h2 := (sub_mem_of_le_nu hpS hp hy'.1 (Finset.mem_Icc.1 (Finset.mem_coe.1 hk2)).2).1
      simp only at h
      exact Nat.eq_of_mul_eq_mul_right hp (by omega)
  have h2 : ∀ x ∈ A, S.ht n p x = (A.filter (fun y => R x y)).card := by
    intro x hx
    have hx' := (mem_aperySet hnS hn).1 hx
    have hset : A.filter (fun y => R x y) =
        (Finset.Icc 1 (S.ht n p x)).image (fun k => x + k * p) := by
      ext y
      simp only [Finset.mem_filter, Finset.mem_image, Finset.mem_Icc, R]
      constructor
      · rintro ⟨hy, k, hk, rfl⟩
        exact ⟨k, ⟨hk, le_ht hp ((mem_aperySet hnS hn).1 hy)⟩, rfl⟩
      · rintro ⟨k, ⟨hk1, hk2⟩, rfl⟩
        exact ⟨(mem_aperySet hnS hn).2 (isApery_of_le_ht hpS hp hx' hk2), k, hk1, rfl⟩
    rw [hset, Finset.card_image_of_injOn, Nat.card_Icc]
    · omega
    · intro k1 _ k2 _ h
      simp only at h
      exact Nat.eq_of_mul_eq_mul_right hp (by omega)
  calc ∑ y ∈ A, S.nu p y = ∑ y ∈ A, (A.filter (fun x => R x y)).card := Finset.sum_congr rfl h1
    _ = ∑ y ∈ A, ∑ x ∈ A, if R x y then 1 else 0 := by simp only [Finset.card_filter]
    _ = ∑ x ∈ A, ∑ y ∈ A, if R x y then 1 else 0 := Finset.sum_comm
    _ = ∑ x ∈ A, (A.filter (fun y => R x y)).card := by simp only [Finset.card_filter]
    _ = ∑ x ∈ A, S.ht n p x := (Finset.sum_congr rfl h2).symm

/-- Paper step (1): `Σ_{w∈Ap} (w + p·ν_p(w)) = Σ_{w∈Ap} top_p(w)` with `top_p(w) = w + p·ht(w)`. -/
theorem sum_add_nu_eq_sum_top {n p : ℕ} (hnS : n ∈ S) (hn : 0 < n) (hpS : p ∈ S) (hp : 0 < p) :
    ∑ w ∈ S.aperySet n, (w + p * S.nu p w) = ∑ w ∈ S.aperySet n, (w + p * S.ht n p w) := by
  rw [Finset.sum_add_distrib, Finset.sum_add_distrib, ← Finset.mul_sum, ← Finset.mul_sum,
    sum_nu_eq_sum_ht hnS hn hpS hp]

theorem sum_add_nu_le {n p : ℕ} (hnS : n ∈ S) (hn : 0 < n) (hpS : p ∈ S) (hp : 0 < p) :
    ∑ w ∈ S.aperySet n, (w + p * S.nu p w) ≤ n * S.aperyMax n := by
  rw [sum_add_nu_eq_sum_top hnS hn hpS hp]
  calc ∑ w ∈ S.aperySet n, (w + p * S.ht n p w) ≤ ∑ _w ∈ S.aperySet n, S.aperyMax n :=
        Finset.sum_le_sum fun w hw => le_aperyMax ((mem_aperySet hnS hn).2 (by
          rw [mul_comm]; exact ht_spec hp ((mem_aperySet hnS hn).1 hw)))
    _ = n * S.aperyMax n := by rw [Finset.sum_const, card_aperySet hn, smul_eq_mul]

/-- **Deliverable 1 (`Def_p ≥ 0`)**: for every `p ∈ S`, `p > 0`, and every `0 < n ∈ S`,
`Σ_{i<n} (w_i + p·ν_p(w_i)) ≤ n·M` with `w_i = S.apery n i` and `M = max Ap(S,n)`. -/
theorem sum_apery_add_nu_le {n p : ℕ} (hnS : n ∈ S) (hn : 0 < n) (hpS : p ∈ S) (hp : 0 < p) :
    ∑ i ∈ range n, (S.apery n i + p * S.nu p (S.apery n i)) ≤ n * S.aperyMax n := by
  have h : ∑ w ∈ S.aperySet n, (w + p * S.nu p w) =
      ∑ i ∈ range n, (S.apery n i + p * S.nu p (S.apery n i)) :=
    sum_aperySet hn (fun w => w + p * S.nu p w)
  rw [← h]
  exact sum_add_nu_le hnS hn hpS hp

/-- The same with respect to the multiplicity (the paper's setting). -/
theorem sum_apery_add_nu_le_mul_max {p : ℕ} (hpS : p ∈ S) (hp : 0 < p) :
    ∑ i ∈ range S.multiplicity, (S.apery S.multiplicity i + p * S.nu p (S.apery S.multiplicity i))
      ≤ S.multiplicity * S.aperyMax S.multiplicity :=
  sum_apery_add_nu_le S.multiplicity_mem S.multiplicity_pos hpS hp

/-- Chain form of `Def_p`: `Def_p = Σ_{w∈Ap} (M - top_p(w))`, a sum of nonnegative terms. -/
theorem defect_eq_sum_top {p : ℕ} (hpS : p ∈ S) (hp : 0 < p) :
    S.defect p = ∑ w ∈ S.aperySet S.multiplicity,
      ((S.aperyMax S.multiplicity : ℤ) - ((w + p * S.ht S.multiplicity p w : ℕ) : ℤ)) := by
  have h := sum_add_nu_eq_sum_top S.multiplicity_mem S.multiplicity_pos hpS hp
  have h' : (∑ w ∈ S.aperySet S.multiplicity, ((w : ℤ) + p * S.nu p w)) =
      ∑ w ∈ S.aperySet S.multiplicity, ((w + p * S.ht S.multiplicity p w : ℕ) : ℤ) := by
    have := congrArg (fun x : ℕ => (x : ℤ)) h
    push_cast at this ⊢
    exact this
  rw [defect, h', Finset.sum_sub_distrib, Finset.sum_const,
    card_aperySet S.multiplicity_pos, nsmul_eq_mul]

theorem defect_nonneg {p : ℕ} (hpS : p ∈ S) (hp : 0 < p) : 0 ≤ S.defect p := by
  have h := sum_add_nu_le S.multiplicity_mem S.multiplicity_pos hpS hp
  rw [defect, sub_nonneg]
  exact_mod_cast h

/-! ### Factorizations over `P' = P ∖ {m}` and `E(w) ≥ 0` -/

theorem card_primitives' : S.primitives'.card = S.embDim - 1 :=
  Finset.card_erase_of_mem S.multiplicity_mem_primitives

theorem card_primitives'_add_one : S.primitives'.card + 1 = S.embDim := by
  rw [card_primitives']; have := S.embDim_pos; omega

theorem isPrimitive_of_mem_primitives' {p : ℕ} (hp : p ∈ S.primitives') : S.IsPrimitive p :=
  S.mem_primitives.1 (Finset.mem_of_mem_erase hp)

theorem mem_of_mem_primitives' {p : ℕ} (hp : p ∈ S.primitives') : p ∈ S :=
  (isPrimitive_of_mem_primitives' hp).1

theorem pos_of_mem_primitives' {p : ℕ} (hp : p ∈ S.primitives') : 0 < p :=
  (isPrimitive_of_mem_primitives' hp).2.1

theorem multiplicity_lt_of_mem_primitives' {p : ℕ} (hp : p ∈ S.primitives') :
    S.multiplicity < p := by
  have hne := Finset.ne_of_mem_erase hp
  have := S.multiplicity_le (pos_of_mem_primitives' hp) (mem_of_mem_primitives' hp)
  omega

/-- Fact (iv): every Apéry element (w.r.t. `m`) is an `ℕ`-combination of `P' = P ∖ {m}`. -/
theorem exists_fact_of_isApery {w : ℕ} (hw : S.IsApery S.multiplicity w) :
    ∃ f : ℕ → ℕ, ∑ p ∈ S.primitives', f p * p = w := by
  induction w using Nat.strong_induction_on with
  | _ w ih =>
    rcases Nat.eq_zero_or_pos w with rfl | hpos
    · exact ⟨0, by simp⟩
    by_cases hprim : S.IsPrimitive w
    · have hne : w ≠ S.multiplicity := by
        rintro rfl
        exact hw.2 le_rfl (by simp)
      have hmem : w ∈ S.primitives' := Finset.mem_erase.2 ⟨hne, S.mem_primitives.2 hprim⟩
      refine ⟨fun q => if q = w then 1 else 0, ?_⟩
      simp [hmem]
    · obtain ⟨a, ha, b, hb, a0, b0, rfl⟩ := S.exists_decomp_of_not_isPrimitive hw.1 hpos hprim
      obtain ⟨fa, hfa⟩ := ih a (by omega) (hw.of_add ha hb rfl)
      obtain ⟨fb, hfb⟩ := ih b (by omega) (hw.of_add hb ha (add_comm b a))
      refine ⟨fa + fb, ?_⟩
      simp only [Pi.add_apply, add_mul, Finset.sum_add_distrib, hfa, hfb]

/-- For any factorization `f` of `w` over `P'`, `f(p) ≤ ν_p(w)`. -/
theorem le_nu_of_fact {w p : ℕ} {f : ℕ → ℕ} (hf : ∑ q ∈ S.primitives', f q * q = w)
    (hp : p ∈ S.primitives') : f p ≤ S.nu p w := by
  have hsplit := Finset.add_sum_erase S.primitives' (fun q => f q * q) hp
  have hrest : ∑ q ∈ S.primitives'.erase p, f q * q ∈ S :=
    sum_mem fun q hq => mul_mem (mem_of_mem_primitives' (Finset.mem_of_mem_erase hq)) (f q)
  apply le_nu (pos_of_mem_primitives' hp) (by omega)
  rwa [show w - f p * p = ∑ q ∈ S.primitives'.erase p, f q * q by omega]

/-- **Deliverable 2 (`E(w) ≥ 0`)**: for `w ∈ Ap(S,m)`, `w ≤ Σ_{p∈P'} p·ν_p(w)`. -/
theorem le_sum_nu {w : ℕ} (hw : S.IsApery S.multiplicity w) :
    w ≤ ∑ p ∈ S.primitives', p * S.nu p w := by
  obtain ⟨f, hf⟩ := exists_fact_of_isApery hw
  calc w = ∑ p ∈ S.primitives', f p * p := hf.symm
    _ ≤ ∑ p ∈ S.primitives', p * S.nu p w := Finset.sum_le_sum fun p hp => by
        rw [mul_comm]; exact Nat.mul_le_mul_left p (le_nu_of_fact hf hp)

theorem excess_nonneg {w : ℕ} (hw : S.IsApery S.multiplicity w) : 0 ≤ S.excess w := by
  rw [excess, sub_nonneg]
  exact_mod_cast le_sum_nu hw

/-! ### Corollary H -/

/-- **Corollary H**: `e · Σ_{i<m} w_i ≤ (e - 1) · m · M`, i.e. `(d+1)·ΣAp ≤ d·m·max Ap`.
(No hypothesis `S ≠ ℕ` is needed.) -/
theorem corollaryH :
    S.embDim * ∑ i ∈ range S.multiplicity, S.apery S.multiplicity i ≤
      (S.embDim - 1) * S.multiplicity * S.aperyMax S.multiplicity := by
  set m := S.multiplicity
  set A := S.aperySet m
  have hm := S.multiplicity_pos
  have hA : ∑ w ∈ A, w = ∑ i ∈ range m, S.apery m i := sum_aperySet hm (fun w => w)
  rw [← hA]
  have key : ∑ p ∈ S.primitives', ∑ w ∈ A, (w + p * S.nu p w) ≤
      ∑ _p ∈ S.primitives', m * S.aperyMax m :=
    Finset.sum_le_sum fun p hp =>
      sum_add_nu_le S.multiplicity_mem hm (mem_of_mem_primitives' hp) (pos_of_mem_primitives' hp)
  rw [Finset.sum_const, smul_eq_mul] at key
  have hE : ∑ w ∈ A, w ≤ ∑ w ∈ A, ∑ p ∈ S.primitives', p * S.nu p w :=
    Finset.sum_le_sum fun w hw => le_sum_nu ((mem_aperySet S.multiplicity_mem hm).1 hw)
  have hsplit : ∑ p ∈ S.primitives', ∑ w ∈ A, (w + p * S.nu p w) =
      S.primitives'.card * ∑ w ∈ A, w + ∑ w ∈ A, ∑ p ∈ S.primitives', p * S.nu p w := by
    simp only [Finset.sum_add_distrib, Finset.sum_const, smul_eq_mul]
    rw [Finset.sum_comm]
  rw [hsplit] at key
  rw [show S.embDim - 1 = S.primitives'.card from card_primitives'.symm,
    ← card_primitives'_add_one, mul_assoc]
  nlinarith

/-- Pure arithmetic step behind `corollaryH_int`. -/
theorem corollaryH_arith (e m g s c ell : ℕ) (hm : 0 < m) (he : 0 < e)
    (hH : e * (m * g + s) ≤ (e - 1) * m * (c + m - 1)) (hs : s * 2 = m * (m - 1))
    (hg : ell + g = c) :
    2 * (c : ℤ) ≤ 2 * e * ell + ((e : ℤ) - 2) * ((m : ℤ) - 1) := by
  obtain ⟨e, rfl⟩ : ∃ e', e = e' + 1 := ⟨e - 1, by omega⟩
  obtain ⟨m, rfl⟩ : ∃ m', m = m' + 1 := ⟨m - 1, by omega⟩
  rw [show c + (m + 1) - 1 = c + m by omega, Nat.add_sub_cancel] at hH
  rw [Nat.add_sub_cancel] at hs
  have hH' : ((e : ℤ) + 1) * (((m : ℤ) + 1) * g + s) ≤ (e : ℤ) * ((m : ℤ) + 1) * (c + m) := by
    exact_mod_cast hH
  have hs' : (s : ℤ) * 2 = ((m : ℤ) + 1) * m := by exact_mod_cast hs
  have hg' : (ell : ℤ) + g = c := by exact_mod_cast hg
  have hm' : (0 : ℤ) < (m : ℤ) + 1 := by positivity
  push_cast
  have key : ((m : ℤ) + 1) * (2 * (c : ℤ)) ≤
      ((m : ℤ) + 1) * (2 * ((e : ℤ) + 1) * ell + (((e : ℤ) + 1) - 2) * (((m : ℤ) + 1) - 1)) := by
    linear_combination 2 * hH' - ((e : ℤ) + 1) * hs' - 2 * ((m : ℤ) + 1) * ((e : ℤ) + 1) * hg'
  exact le_of_mul_le_mul_left key hm'

/-- Consequence of Corollary H, in `ℤ` (no truncated subtraction):
`2c ≤ 2·e·ℓ + (e - 2)(m - 1)`, i.e. Wilf up to the additive error `(e-2)(m-1)/2`. -/
theorem corollaryH_int :
    2 * (S.conductor : ℤ) ≤
      2 * S.embDim * S.ell + ((S.embDim : ℤ) - 2) * ((S.multiplicity : ℤ) - 1) := by
  have hm := S.multiplicity_pos
  have hH := corollaryH (S := S)
  rw [sum_apery_eq S.multiplicity_mem hm, aperyMax_eq S.multiplicity_mem hm] at hH
  exact corollaryH_arith _ _ _ _ _ _ hm S.embDim_pos hH
    (Finset.sum_range_id_mul_two S.multiplicity) S.ell_add_genus

/-- Natural-number form of the consequence of Corollary H, for `S ≠ ℕ` (then `e ≥ 2`, `m ≥ 2`). -/
theorem corollaryH_nat (hS : S ≠ nat) :
    2 * S.conductor ≤ 2 * S.embDim * S.ell + (S.embDim - 2) * (S.multiplicity - 1) := by
  have h := corollaryH_int (S := S)
  have he := S.two_le_embDim hS
  have hm := S.multiplicity_pos
  have : ((2 * S.embDim * S.ell + (S.embDim - 2) * (S.multiplicity - 1) : ℕ) : ℤ) =
      2 * S.embDim * S.ell + ((S.embDim : ℤ) - 2) * ((S.multiplicity : ℤ) - 1) := by
    push_cast [Nat.cast_sub he, Nat.cast_sub (show 1 ≤ S.multiplicity from hm)]
    ring
  rw [← this] at h
  exact_mod_cast h

/-! ### Identity CH -/

/-- Pure arithmetic step behind Identity CH. -/
theorem identityCH_arith (d m g s c ell M sw X : ℤ) (hsum : sw = m * g + s)
    (hs : s * 2 = m * (m - 1)) (hM : M = c + m - 1) (hg : ell + g = c) :
    2 * (m * ((d + 1) * ell - c)) =
      2 * (d * (m * M) - d * sw - X) + 2 * (X - sw) - ((d + 1 - 1) - 1) * m * (m - 1) := by
  subst hsum hM
  linear_combination (2 * m * (d + 1)) * hg + (d + 1) * hs

/-- **Identity CH** (doubled, in `ℤ`):
`2·m·W = 2·Σ_{p∈P'} Def_p + 2·Σ_{w∈Ap} E(w) - (d - 1)·m·(m - 1)` with `d = e - 1`. -/
theorem identityCH_two_mul :
    2 * ((S.multiplicity : ℤ) * S.wilfDefect) =
      2 * ∑ p ∈ S.primitives', S.defect p + 2 * ∑ w ∈ S.aperySet S.multiplicity, S.excess w
        - (((S.embDim : ℤ) - 1) - 1) * S.multiplicity * ((S.multiplicity : ℤ) - 1) := by
  have hm := S.multiplicity_pos
  have hsum : ∑ w ∈ S.aperySet S.multiplicity, w =
      S.multiplicity * S.genus + ∑ i ∈ range S.multiplicity, i :=
    (sum_aperySet hm (fun w => w)).trans (sum_apery_eq S.multiplicity_mem hm)
  have hs := Finset.sum_range_id_mul_two S.multiplicity
  generalize ∑ i ∈ range S.multiplicity, i = s at hsum hs
  have hM := aperyMax_eq S.multiplicity_mem hm
  have h1 : ∑ p ∈ S.primitives', S.defect p =
      (S.primitives'.card : ℤ) * ((S.multiplicity : ℤ) * S.aperyMax S.multiplicity) -
        (S.primitives'.card : ℤ) * ∑ w ∈ S.aperySet S.multiplicity, (w : ℤ) -
          ∑ w ∈ S.aperySet S.multiplicity, ∑ p ∈ S.primitives', (p : ℤ) * S.nu p w := by
    simp only [defect, Finset.sum_sub_distrib, Finset.sum_add_distrib, Finset.sum_const,
      nsmul_eq_mul]
    rw [Finset.sum_comm (s := S.primitives')]
    ring
  have h2 : ∑ w ∈ S.aperySet S.multiplicity, S.excess w =
      ∑ w ∈ S.aperySet S.multiplicity, ∑ p ∈ S.primitives', (p : ℤ) * S.nu p w -
        ∑ w ∈ S.aperySet S.multiplicity, (w : ℤ) := by
    simp only [excess, Finset.sum_sub_distrib]
  have hsum' : ∑ w ∈ S.aperySet S.multiplicity, (w : ℤ) = (S.multiplicity : ℤ) * S.genus + s := by
    have := congrArg (fun x : ℕ => (x : ℤ)) hsum
    push_cast at this
    exact this
  have hs' : (s : ℤ) * 2 = S.multiplicity * ((S.multiplicity : ℤ) - 1) := by
    have := congrArg (fun x : ℕ => (x : ℤ)) hs
    push_cast [Nat.cast_sub (show 1 ≤ S.multiplicity from hm)] at this
    exact this
  have hM' : (S.aperyMax S.multiplicity : ℤ) = S.conductor + S.multiplicity - 1 := by
    rw [hM]
    push_cast [Nat.cast_sub (show 1 ≤ S.conductor + S.multiplicity by omega)]
    ring
  have hg' : (S.ell : ℤ) + S.genus = S.conductor := by exact_mod_cast S.ell_add_genus
  have hd' : (S.embDim : ℤ) = S.primitives'.card + 1 := by
    exact_mod_cast card_primitives'_add_one.symm
  rw [h1, h2, wilfDefect, hd', hsum', hM']
  exact identityCH_arith _ _ _ _ _ _ _ _ _ rfl hs' rfl hg'

/-- **Identity CH** exactly as in the paper: `m·W = Σ_{p∈P'} Def_p + E - (d-1)·m(m-1)/2`. -/
theorem identityCH :
    (S.multiplicity : ℤ) * S.wilfDefect =
      ∑ p ∈ S.primitives', S.defect p + ∑ w ∈ S.aperySet S.multiplicity, S.excess w
        - (((S.embDim : ℤ) - 1) - 1) * ((S.multiplicity * (S.multiplicity - 1) / 2 : ℕ) : ℤ) := by
  have h := identityCH_two_mul (S := S)
  have hs := Finset.sum_range_id_mul_two S.multiplicity
  rw [← Finset.sum_range_id]
  have hm := S.multiplicity_pos
  generalize ∑ i ∈ range S.multiplicity, i = s at hs ⊢
  have hs' : (s : ℤ) * 2 = S.multiplicity * ((S.multiplicity : ℤ) - 1) := by
    have := congrArg (fun x : ℕ => (x : ℤ)) hs
    push_cast [Nat.cast_sub (show 1 ≤ S.multiplicity from hm)] at this
    exact this
  apply mul_left_cancel₀ (two_ne_zero : (2 : ℤ) ≠ 0)
  linear_combination h + (((S.embDim : ℤ) - 1) - 1) * hs'

/-! ### Lemma A (top-layer reduction) -/

theorem mem_topLayer {u : ℕ} :
    u ∈ S.topLayer ↔ u ∈ S.aperySet S.multiplicity ∧ S.conductor ≤ u ∧
      u < S.conductor + S.multiplicity := by
  rw [topLayer, Finset.mem_filter]

theorem topLayer_subset : S.topLayer ⊆ S.aperySet S.multiplicity :=
  Finset.filter_subset _ _

theorem minFactLen_spec {u : ℕ} (hu : S.IsApery S.multiplicity u) :
    ∃ f : ℕ → ℕ, ∑ p ∈ S.primitives', f p * p = u ∧
      ∑ p ∈ S.primitives', f p = S.minFactLen u := by
  obtain ⟨f, hf⟩ := exists_fact_of_isApery hu
  exact Nat.sInf_mem (s := {L | ∃ f : ℕ → ℕ, ∑ p ∈ S.primitives', f p * p = u ∧
      ∑ p ∈ S.primitives', f p = L}) ⟨_, f, hf, rfl⟩

/-- `ℓ(u)` is a lower bound for the length of every factorization of `u` over `P'`. -/
theorem minFactLen_le {u : ℕ} {f : ℕ → ℕ} (hf : ∑ p ∈ S.primitives', f p * p = u) :
    S.minFactLen u ≤ ∑ p ∈ S.primitives', f p :=
  Nat.sInf_le ⟨f, hf, rfl⟩

/-- Refined per-direction bound (the chain step of Lemma A): for `p ∈ S`, `p > 0`,
`Σ_{w∈Ap} (w + p·ν_p(w)) ≤ m·(c - 1) + Σ_{u∈X_q} (ν_p(u) + 1)·(u - c + 1)`.
(Chains whose top is `u ∈ X_q` have at most `ν_p(u) + 1` elements; all other tops are `≤ c - 1`.) -/
theorem sum_add_nu_le_topLayer {p : ℕ} (hpS : p ∈ S) (hp : 0 < p) :
    ∑ w ∈ S.aperySet S.multiplicity, (w + p * S.nu p w) ≤
      S.multiplicity * (S.conductor - 1) +
        ∑ u ∈ S.topLayer, (S.nu p u + 1) * (u - S.conductor + 1) := by
  classical
  have hm := S.multiplicity_pos
  have hmS := S.multiplicity_mem
  rw [sum_add_nu_eq_sum_top hmS hm hpS hp]
  let T : ℕ → ℕ := fun w => w + p * S.ht S.multiplicity p w
  have hTA : ∀ w ∈ S.aperySet S.multiplicity, T w ∈ S.aperySet S.multiplicity :=
    fun w hw => (mem_aperySet hmS hm).2 (by
      show S.IsApery S.multiplicity (w + p * S.ht S.multiplicity p w)
      rw [mul_comm]; exact ht_spec hp ((mem_aperySet hmS hm).1 hw))
  let gt : ℕ → ℕ := fun t => if S.conductor ≤ t then t - S.conductor + 1 else 0
  have step1 : ∑ w ∈ S.aperySet S.multiplicity, T w ≤
      ∑ w ∈ S.aperySet S.multiplicity, ((S.conductor - 1) + gt (T w)) :=
    Finset.sum_le_sum fun w _ => by
      show T w ≤ (S.conductor - 1) + (if S.conductor ≤ T w then T w - S.conductor + 1 else 0)
      split_ifs <;> omega
  have hconst : ∑ w ∈ S.aperySet S.multiplicity, ((S.conductor - 1) + gt (T w)) =
      S.multiplicity * (S.conductor - 1) + ∑ w ∈ S.aperySet S.multiplicity, gt (T w) := by
    rw [Finset.sum_add_distrib, Finset.sum_const, card_aperySet hm, smul_eq_mul]
  rw [hconst] at step1
  have step2 : ∑ w ∈ S.aperySet S.multiplicity, gt (T w) =
      ∑ u ∈ S.aperySet S.multiplicity,
        ((S.aperySet S.multiplicity).filter (fun w => T w = u)).card * gt u := by
    rw [← Finset.sum_fiberwise_of_maps_to hTA (fun w => gt (T w))]
    refine Finset.sum_congr rfl fun u _ => ?_
    have : ∀ w ∈ (S.aperySet S.multiplicity).filter (fun w => T w = u), gt (T w) = gt u :=
      fun w hw => by rw [(Finset.mem_filter.1 hw).2]
    rw [Finset.sum_congr rfl this, Finset.sum_const, smul_eq_mul]
  have step3 : ∀ u ∈ S.aperySet S.multiplicity,
      ((S.aperySet S.multiplicity).filter (fun w => T w = u)).card ≤ S.nu p u + 1 := by
    intro u _
    calc ((S.aperySet S.multiplicity).filter (fun w => T w = u)).card
        ≤ (range (S.nu p u + 1)).card := by
          apply Finset.card_le_card_of_injOn (fun w => S.ht S.multiplicity p w)
          · intro w hw
            have hw' := Finset.mem_filter.1 (Finset.mem_coe.1 hw)
            have hTw : w + p * S.ht S.multiplicity p w = u := hw'.2
            have hwS := ((mem_aperySet hmS hm).1 hw'.1).1
            have hc := mul_comm (S.ht S.multiplicity p w) p
            have := le_nu (S := S) (k := S.ht S.multiplicity p w) (w := u) hp (by omega)
              (by rw [show u - S.ht S.multiplicity p w * p = w by omega]; exact hwS)
            simp only [Finset.coe_range, Set.mem_Iio]
            omega
          · intro w1 hw1 w2 hw2 h
            have e1 : w1 + p * S.ht S.multiplicity p w1 = u :=
              (Finset.mem_filter.1 (Finset.mem_coe.1 hw1)).2
            have e2 : w2 + p * S.ht S.multiplicity p w2 = u :=
              (Finset.mem_filter.1 (Finset.mem_coe.1 hw2)).2
            simp only at h
            rw [h] at e1
            omega
      _ = S.nu p u + 1 := Finset.card_range _
  have step4 : ∑ u ∈ S.aperySet S.multiplicity,
        ((S.aperySet S.multiplicity).filter (fun w => T w = u)).card * gt u ≤
      ∑ u ∈ S.aperySet S.multiplicity, (S.nu p u + 1) * gt u :=
    Finset.sum_le_sum fun u hu => Nat.mul_le_mul_right _ (step3 u hu)
  have step5 : ∑ u ∈ S.aperySet S.multiplicity, (S.nu p u + 1) * gt u =
      ∑ u ∈ S.topLayer, (S.nu p u + 1) * (u - S.conductor + 1) := by
    rw [topLayer, Finset.sum_filter]
    refine Finset.sum_congr rfl fun u hu => ?_
    have hlt := ((mem_aperySet hmS hm).1 hu).lt
    by_cases h : S.conductor ≤ u
    · simp [gt, h, hlt]
    · simp [gt, h]
  rw [step2] at step1
  show ∑ w ∈ S.aperySet S.multiplicity, T w ≤ _
  omega

/-- Cast of a top-layer sum (`u - c + 1` is exact on `X_q`). -/
theorem cast_sum_topLayer (F : ℕ → ℕ) :
    ((∑ u ∈ S.topLayer, F u * (u - S.conductor + 1) : ℕ) : ℤ) =
      ∑ u ∈ S.topLayer, (F u : ℤ) * ((u : ℤ) - S.conductor + 1) := by
  rw [Nat.cast_sum]
  refine Finset.sum_congr rfl fun u hu => ?_
  have := (mem_topLayer.1 hu).2.1
  rw [Nat.cast_mul, Nat.cast_add, Nat.cast_sub this, Nat.cast_one]

/-- Cast of a top-layer sum, other factor order. -/
theorem cast_sum_topLayer' (F : ℕ → ℕ) :
    ((∑ u ∈ S.topLayer, (u - S.conductor + 1) * F u : ℕ) : ℤ) =
      ∑ u ∈ S.topLayer, ((u : ℤ) - S.conductor + 1) * (F u : ℤ) := by
  rw [Nat.cast_sum]
  refine Finset.sum_congr rfl fun u hu => ?_
  have := (mem_topLayer.1 hu).2.1
  rw [Nat.cast_mul, Nat.cast_add, Nat.cast_sub this, Nat.cast_one]

/-- Per-direction lower bound for `Def_p` (`S ≠ ℕ`):
`Def_p ≥ m² - Σ_{u∈X_q} (ν_p(u) + 1)·π(u)` with `π(u) = u - c + 1`. -/
theorem defect_ge_topLayer (hS : S ≠ nat) {p : ℕ} (hpS : p ∈ S) (hp : 0 < p) :
    (S.multiplicity : ℤ) * S.multiplicity -
        ∑ u ∈ S.topLayer, ((S.nu p u : ℤ) + 1) * ((u : ℤ) - S.conductor + 1) ≤
      S.defect p := by
  have hm := S.multiplicity_pos
  have hc : 0 < S.conductor := (S.conductor_pos_iff).2 hS
  have h := sum_add_nu_le_topLayer hpS hp
  have h' := Nat.cast_le (α := ℤ) |>.2 h
  rw [Nat.cast_add, cast_sum_topLayer (fun u => S.nu p u + 1)] at h'
  push_cast [Nat.cast_sub (show 1 ≤ S.conductor from hc)] at h'
  have hM : (S.aperyMax S.multiplicity : ℤ) = S.conductor + S.multiplicity - 1 := by
    rw [aperyMax_eq S.multiplicity_mem hm]
    push_cast [Nat.cast_sub (show 1 ≤ S.conductor + S.multiplicity by omega)]
    ring
  rw [defect, hM]
  linarith

/-- Per-element bound on the top layer, with `π(u) = u - c + 1` and `d = |P'|`:
`π(u)·Σ_{p∈P'} (ν_p(u) + 1) - E(u) ≤ π(u)·(d + ℓ(u))`. -/
theorem topLayer_term_le {u : ℕ} (hu : u ∈ S.topLayer) :
    ((u : ℤ) - S.conductor + 1) * ∑ p ∈ S.primitives', ((S.nu p u : ℤ) + 1) - S.excess u ≤
      ((u : ℤ) - S.conductor + 1) * ((S.primitives'.card : ℤ) + S.minFactLen u) := by
  have hm := S.multiplicity_pos
  obtain ⟨huA, hcu, hum⟩ := mem_topLayer.1 hu
  have hu' := (mem_aperySet S.multiplicity_mem hm).1 huA
  obtain ⟨f, hf, hlen⟩ := minFactLen_spec hu'
  set π : ℤ := (u : ℤ) - S.conductor + 1 with hπ
  have hπm : π ≤ S.multiplicity := by
    have : (u : ℤ) < S.conductor + S.multiplicity := by exact_mod_cast hum
    rw [hπ]; linarith
  have hterm : ∀ p ∈ S.primitives',
      π * ((S.nu p u : ℤ) + 1) - p * S.nu p u ≤ π * ((f p : ℤ) + 1) - p * f p := by
    intro p hp
    have h1 : (f p : ℤ) ≤ S.nu p u := by exact_mod_cast le_nu_of_fact hf hp
    have h2 : π ≤ p := by
      have : (S.multiplicity : ℤ) < p := by exact_mod_cast multiplicity_lt_of_mem_primitives' hp
      linarith
    nlinarith [mul_nonneg (sub_nonneg.2 h2) (sub_nonneg.2 h1)]
  have hf' : ∑ p ∈ S.primitives', (p : ℤ) * f p = u := by
    have := congrArg (fun x : ℕ => (x : ℤ)) hf
    push_cast at this
    rw [← this]
    exact Finset.sum_congr rfl fun p _ => mul_comm _ _
  have hlen' : ∑ p ∈ S.primitives', (f p : ℤ) = S.minFactLen u := by exact_mod_cast hlen
  calc π * ∑ p ∈ S.primitives', ((S.nu p u : ℤ) + 1) - S.excess u
      = ∑ p ∈ S.primitives', (π * ((S.nu p u : ℤ) + 1) - p * S.nu p u) + u := by
        rw [excess, Finset.mul_sum, Finset.sum_sub_distrib]; ring
    _ ≤ ∑ p ∈ S.primitives', (π * ((f p : ℤ) + 1) - p * f p) + u := by
        have := Finset.sum_le_sum hterm
        linarith
    _ = π * ((S.primitives'.card : ℤ) + S.minFactLen u) := by
        rw [Finset.sum_sub_distrib, ← Finset.mul_sum, Finset.sum_add_distrib, Finset.sum_const,
          nsmul_eq_mul, hf', hlen']
        ring

/-- **Lemma A** (doubled, in `ℤ`), for `S ≠ ℕ`, with `d = e - 1`, `π(u) = u - c + 1`:
`2·m·W ≥ m·((d+1)·m + d - 1) - 2·Σ_{u∈X_q} π(u)·(d + ℓ(u)) + 2·Σ_{w∈Ap∖X_q} E(w)`. -/
theorem lemmaA_two_mul (hS : S ≠ nat) :
    (S.multiplicity : ℤ) * ((((S.embDim : ℤ) - 1) + 1) * S.multiplicity + ((S.embDim : ℤ) - 1) - 1)
      - 2 * ∑ u ∈ S.topLayer,
          ((u : ℤ) - S.conductor + 1) * (((S.embDim : ℤ) - 1) + S.minFactLen u)
      + 2 * ∑ w ∈ S.aperySet S.multiplicity \ S.topLayer, S.excess w
      ≤ 2 * ((S.multiplicity : ℤ) * S.wilfDefect) := by
  have hCH := identityCH_two_mul (S := S)
  have hd' : (S.embDim : ℤ) - 1 = S.primitives'.card := by
    have := card_primitives'_add_one (S := S); omega
  rw [hd'] at hCH ⊢
  set d : ℤ := (S.primitives'.card : ℤ)
  set m : ℤ := (S.multiplicity : ℤ)
  -- lower bound on Σ Def
  have hDef : ∑ p ∈ S.primitives', (m * m -
      ∑ u ∈ S.topLayer, ((S.nu p u : ℤ) + 1) * ((u : ℤ) - S.conductor + 1)) ≤
      ∑ p ∈ S.primitives', S.defect p :=
    Finset.sum_le_sum fun p hp =>
      defect_ge_topLayer hS (mem_of_mem_primitives' hp) (pos_of_mem_primitives' hp)
  have hDef' : ∑ p ∈ S.primitives', (m * m -
      ∑ u ∈ S.topLayer, ((S.nu p u : ℤ) + 1) * ((u : ℤ) - S.conductor + 1)) =
      d * (m * m) - ∑ u ∈ S.topLayer,
        ((u : ℤ) - S.conductor + 1) * ∑ p ∈ S.primitives', ((S.nu p u : ℤ) + 1) := by
    rw [Finset.sum_sub_distrib, Finset.sum_const, nsmul_eq_mul, Finset.sum_comm]
    congr 1
    refine Finset.sum_congr rfl fun u _ => ?_
    rw [Finset.mul_sum]
    exact Finset.sum_congr rfl fun p _ => mul_comm _ _
  -- split E over X_q and the rest
  have hE : ∑ w ∈ S.aperySet S.multiplicity, S.excess w =
      ∑ w ∈ S.aperySet S.multiplicity \ S.topLayer, S.excess w +
        ∑ u ∈ S.topLayer, S.excess u :=
    (Finset.sum_sdiff topLayer_subset).symm
  -- per-element top-layer bound
  have hX : ∑ u ∈ S.topLayer,
      (((u : ℤ) - S.conductor + 1) * ∑ p ∈ S.primitives', ((S.nu p u : ℤ) + 1) - S.excess u) ≤
      ∑ u ∈ S.topLayer, ((u : ℤ) - S.conductor + 1) * (d + S.minFactLen u) :=
    Finset.sum_le_sum fun u hu => topLayer_term_le hu
  rw [Finset.sum_sub_distrib] at hX
  rw [hDef'] at hDef
  rw [hE] at hCH
  linear_combination -hCH + 2 * hDef + 2 * hX

/-- **Lemma A** exactly as in the paper (`ℤ`-division; the numerator is even):
`m·W ≥ m·((d+1)·m + d - 1)/2 - Σ_{u∈X_q} π(u)·(d + ℓ(u)) + Σ_{w∈Ap∖X_q} E(w)`, `S ≠ ℕ`. -/
theorem lemmaA (hS : S ≠ nat) :
    (S.multiplicity : ℤ) * ((((S.embDim : ℤ) - 1) + 1) * S.multiplicity + ((S.embDim : ℤ) - 1) - 1)
        / 2
      - ∑ u ∈ S.topLayer,
          ((u : ℤ) - S.conductor + 1) * (((S.embDim : ℤ) - 1) + S.minFactLen u)
      + ∑ w ∈ S.aperySet S.multiplicity \ S.topLayer, S.excess w
      ≤ (S.multiplicity : ℤ) * S.wilfDefect := by
  have h := lemmaA_two_mul hS
  obtain ⟨r, hr⟩ := Int.even_mul_succ_self (S.multiplicity : ℤ)
  have hX : (S.multiplicity : ℤ) *
      ((((S.embDim : ℤ) - 1) + 1) * S.multiplicity + ((S.embDim : ℤ) - 1) - 1) =
      2 * ((S.embDim : ℤ) * r - S.multiplicity) := by
    linear_combination (S.embDim : ℤ) * hr
  rw [hX] at h ⊢
  rw [Int.mul_ediv_cancel_left _ two_ne_zero]
  linarith

/-! ### Conjecture TOP'' and `TOP'' ⇒ Wilf` -/

/-- **Conjecture TOP''** (`.research/PROOFS.md`), with `d = e - 1`, `π(u) = u - c + 1`,
`ℓ(u)` the shortest factorization length over `P' = P ∖ {m}`:
`Σ_{u∈X_q} π(u)·(d + ℓ(u)) ≤ m·((d+1)·m + d - 1)/2`. -/
def TOP2 : Prop :=
  ∑ u ∈ S.topLayer, (u - S.conductor + 1) * ((S.embDim - 1) + S.minFactLen u) ≤
    S.multiplicity * ((S.embDim - 1 + 1) * S.multiplicity + (S.embDim - 1) - 1) / 2

/-- **Lemma A ⇒ (TOP'' ⇒ Wilf)**: every numerical semigroup satisfying TOP'' satisfies Wilf. -/
theorem wilf_of_TOP2 (h : S.TOP2) : S.conductor ≤ S.embDim * S.ell := by
  by_cases hS : S = nat
  · subst hS; simp
  have hA := lemmaA_two_mul hS
  have he := S.two_le_embDim hS
  have hm := S.multiplicity_pos
  rw [TOP2, Nat.le_div_iff_mul_le two_pos] at h
  have h2 : 2 * ∑ u ∈ S.topLayer, (u - S.conductor + 1) * ((S.embDim - 1) + S.minFactLen u) ≤
      S.multiplicity * ((S.embDim - 1 + 1) * S.multiplicity + (S.embDim - 1) - 1) := by omega
  have h' := Nat.cast_le (α := ℤ) |>.2 h2
  have he1 : 1 ≤ S.embDim := by omega
  have hX : ((S.multiplicity * ((S.embDim - 1 + 1) * S.multiplicity + (S.embDim - 1) - 1) : ℕ)
      : ℤ) = (S.multiplicity : ℤ) *
        ((((S.embDim : ℤ) - 1) + 1) * S.multiplicity + ((S.embDim : ℤ) - 1) - 1) := by
    have h3 : 1 ≤ (S.embDim - 1 + 1) * S.multiplicity + (S.embDim - 1) := by
      have : 1 ≤ S.embDim - 1 := by omega
      omega
    rw [Nat.cast_mul, Nat.cast_sub h3, Nat.cast_add, Nat.cast_mul, Nat.cast_add, Nat.cast_sub he1]
    push_cast
    ring
  have hsum : ((∑ u ∈ S.topLayer, (u - S.conductor + 1) * ((S.embDim - 1) + S.minFactLen u) : ℕ)
      : ℤ) = ∑ u ∈ S.topLayer,
        ((u : ℤ) - S.conductor + 1) * (((S.embDim : ℤ) - 1) + S.minFactLen u) := by
    rw [cast_sum_topLayer' (fun u => (S.embDim - 1) + S.minFactLen u)]
    refine Finset.sum_congr rfl fun u _ => ?_
    rw [Nat.cast_add, Nat.cast_sub he1, Nat.cast_one]
  rw [Nat.cast_mul, hX, hsum, Nat.cast_ofNat] at h'
  have hR : 0 ≤ ∑ w ∈ S.aperySet S.multiplicity \ S.topLayer, S.excess w :=
    Finset.sum_nonneg fun w hw =>
      excess_nonneg ((mem_aperySet S.multiplicity_mem hm).1 (Finset.mem_sdiff.1 hw).1)
  have hW : 0 ≤ (S.multiplicity : ℤ) * S.wilfDefect := by linarith
  have hW' : 0 ≤ S.wilfDefect :=
    nonneg_of_mul_nonneg_right (by linarith) (by exact_mod_cast hm : (0 : ℤ) < S.multiplicity)
  rw [wilfDefect] at hW'
  have : (S.conductor : ℤ) ≤ S.embDim * S.ell := by linarith
  exact_mod_cast this

/-- The implication as a statement about all semigroups: `(∀ S, TOP'' S) → WilfConjecture`. -/
theorem wilfConjecture_of_TOP2 (h : ∀ S : NumericalSemigroup, S.TOP2) : WilfConjecture :=
  fun S => wilf_of_TOP2 (h S)

end NumericalSemigroup
