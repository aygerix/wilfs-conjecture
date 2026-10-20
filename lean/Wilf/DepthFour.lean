import Wilf.Window2

/-!
# Wilf's conjecture for `3m < c ≤ 3m + e`

Let `m` be the multiplicity, `M = max Ap(S, m) = c + m - 1` and `λ(w) = ⌊(M - w)/m⌋`, so that
`ℓ = Σ_{w ∈ Ap} λ(w)`. For `w ∈ Ap` put

* `L1(w) = Σ_{p ∈ P'} ν_p(w) · λ(w - p)` and `N(w) = Σ_{p ∈ P'} ν_p(w) · λ(w)`,

where `P'` is the set of minimal generators other than `m` and `ν_p(w)` is the largest `k` with
`w - k p ∈ S`.

* **Column inequality.** For each `p ∈ P'`, reindexing `w ↦ w - p` gives
  `Σ_w ν_p(w) λ(w - p) ≤ ℓ + Σ_w ν_p(w) λ(w)`. Summing over `p`: `Σ_w L1(w) ≤ d ℓ + Σ_w N(w)`.
* **Pointwise bound.** If `c > 3m` (so `M ≥ 4m`), then `λ(w) + L1(w) ≥ 3 + N(w)` for every Apéry
  element, and `≥ 4 + N(w)` for `w = 0` and for the primitives. Take a factorization `f` of `w` of
  length `J`. If `J ≥ 3`, every step drops `λ` by at least one. If `J ≤ 2`, the floor inequality
  `m ⌊x/m⌋ + m - 1 ≥ x` applied to `x_q = M - (w - q)` does it.
* Summing: `(d + 1) ℓ ≥ 3m + d + 1`, i.e. `e · ℓ ≥ 3m + e`. Hence `c ≤ e · ℓ` whenever
  `3m < c ≤ 3m + e`.
-/

namespace NumericalSemigroup

open Finset

variable {S : NumericalSemigroup}

theorem isApery_of_mem_primitives' {p : ℕ} (hp : p ∈ S.primitives') :
    S.IsApery S.multiplicity p := by
  have hprim := isPrimitive_of_mem_primitives' hp
  have hlt := multiplicity_lt_of_mem_primitives' hp
  refine ⟨hprim.1, fun _ hmem => ?_⟩
  exact hprim.2.2 (p - S.multiplicity) hmem S.multiplicity S.multiplicity_mem
    (by omega) S.multiplicity_pos (by omega)

theorem isApery_zero' : S.IsApery S.multiplicity 0 :=
  ⟨zero_mem S, fun h _ => by have := S.multiplicity_pos; omega⟩

variable (S)

/-- `λ(w) = ⌊(M - w)/m⌋`, `M = max Ap(S, m)`. -/
noncomputable def lam (w : ℕ) : ℕ := (S.aperyMax S.multiplicity - w) / S.multiplicity

/-- `L1(w) = Σ_{p ∈ P'} ν_p(w) λ(w - p)`. -/
noncomputable def linkSum (w : ℕ) : ℕ := ∑ p ∈ S.primitives', S.nu p w * S.lam (w - p)

/-- `N(w) = Σ_{p ∈ P'} ν_p(w) λ(w)`. -/
noncomputable def linkBase (w : ℕ) : ℕ := ∑ p ∈ S.primitives', S.nu p w * S.lam w

variable {S}

theorem lam_le_lam_sub (w q : ℕ) : S.lam w ≤ S.lam (w - q) := by
  unfold lam
  exact Nat.div_le_div_right (by omega)

/-- One step of size `q ≥ m` drops `λ` by at least one. -/
theorem lam_succ_le_lam_sub {w q : ℕ} (hwM : w ≤ S.aperyMax S.multiplicity) (hqw : q ≤ w)
    (hq : S.multiplicity ≤ q) : S.lam w + 1 ≤ S.lam (w - q) := by
  unfold lam
  have hm := S.multiplicity_pos
  rw [← Nat.add_div_right _ hm]
  exact Nat.div_le_div_right (by omega)

/-- `ℓ = Σ_{w ∈ Ap} λ(w)`. -/
theorem ell_eq_sum_lam : S.ell = ∑ w ∈ S.aperySet S.multiplicity, S.lam w := by
  have hm := S.multiplicity_pos
  have hMeq := aperyMax_eq S.multiplicity_mem hm
  have h := Window2.apery_left_count S (S.aperyMax S.multiplicity)
  have hmin : ∀ w ∈ S.aperySet S.multiplicity,
      min (S.aperyMax S.multiplicity) ((S.aperyMax S.multiplicity - w) / S.multiplicity) =
        S.lam w := by
    intro w _
    unfold lam
    exact min_eq_right ((Nat.div_le_self _ _).trans (Nat.sub_le _ _))
  rw [sum_congr rfl hmin] at h
  unfold ell
  rw [h, filter_true_of_mem]
  intro x _
  have : S.aperyMax S.multiplicity ≤ S.aperyMax S.multiplicity * S.multiplicity :=
    Nat.le_mul_of_pos_right _ hm
  omega

theorem nu_le_nu_sub_add_one {p w : ℕ} (hp : 0 < p) (hw : w ∈ S)
    (h1 : 1 ≤ S.nu p w) : S.nu p w ≤ S.nu p (w - p) + 1 := by
  obtain ⟨h1', h2'⟩ := nu_spec hp hw
  obtain ⟨k, hk⟩ : ∃ k, S.nu p w = k + 1 := ⟨S.nu p w - 1, by omega⟩
  rw [hk] at h1' h2' ⊢
  have e : (k + 1) * p = k * p + p := by ring
  rw [e] at h1' h2'
  have : k ≤ S.nu p (w - p) := by
    apply le_nu hp (by omega)
    rwa [show w - p - k * p = w - (k * p + p) by omega]
  omega

/-- **Column inequality.** -/
theorem column_sum_le {p : ℕ} (hp : p ∈ S.primitives') :
    ∑ w ∈ S.aperySet S.multiplicity, S.nu p w * S.lam (w - p) ≤
      ∑ w ∈ S.aperySet S.multiplicity, S.lam w +
        ∑ w ∈ S.aperySet S.multiplicity, S.nu p w * S.lam w := by
  classical
  have hpS := mem_of_mem_primitives' hp
  have hp0 := pos_of_mem_primitives' hp
  have hmS := S.multiplicity_mem
  have hm := S.multiplicity_pos
  have hmemA1 : ∀ w ∈ (S.aperySet S.multiplicity).filter (fun w => 1 ≤ S.nu p w),
      p ≤ w ∧ S.IsApery S.multiplicity (w - p) ∧ 1 ≤ S.nu p w ∧
        S.IsApery S.multiplicity w := by
    intro w hw
    rw [mem_filter] at hw
    have hwA := (mem_aperySet hmS hm).1 hw.1
    obtain ⟨h1, h2⟩ := sub_mem_of_le_nu hpS hp0 hwA.1 hw.2
    rw [one_mul] at h1 h2
    exact ⟨h1, hwA.of_add h2 hpS (by omega), hw.2, hwA⟩
  have hsplit : ∑ w ∈ S.aperySet S.multiplicity, S.nu p w * S.lam (w - p) =
      ∑ w ∈ (S.aperySet S.multiplicity).filter (fun w => 1 ≤ S.nu p w),
        S.nu p w * S.lam (w - p) := by
    rw [sum_filter_of_ne]
    intro w _ hne
    by_contra h
    exact hne (by rw [show S.nu p w = 0 by omega, zero_mul])
  have himg : ((S.aperySet S.multiplicity).filter (fun w => 1 ≤ S.nu p w)).image
      (fun w => w - p) ⊆ S.aperySet S.multiplicity := by
    intro u hu
    rw [mem_image] at hu
    obtain ⟨w, hw, rfl⟩ := hu
    exact (mem_aperySet hmS hm).2 (hmemA1 w hw).2.1
  calc ∑ w ∈ S.aperySet S.multiplicity, S.nu p w * S.lam (w - p)
      = ∑ w ∈ (S.aperySet S.multiplicity).filter (fun w => 1 ≤ S.nu p w),
          S.nu p w * S.lam (w - p) := hsplit
    _ ≤ ∑ w ∈ (S.aperySet S.multiplicity).filter (fun w => 1 ≤ S.nu p w),
          (S.nu p (w - p) + 1) * S.lam (w - p) := by
        apply sum_le_sum
        intro w hw
        obtain ⟨_, _, h1, hwA⟩ := hmemA1 w hw
        exact Nat.mul_le_mul_right _ (nu_le_nu_sub_add_one hp0 hwA.1 h1)
    _ = ∑ u ∈ ((S.aperySet S.multiplicity).filter (fun w => 1 ≤ S.nu p w)).image
          (fun w => w - p), (S.nu p u + 1) * S.lam u := by
        rw [sum_image]
        intro x hx y hy h
        have := (hmemA1 x hx).1
        have := (hmemA1 y hy).1
        simp only at h
        omega
    _ ≤ ∑ u ∈ S.aperySet S.multiplicity, (S.nu p u + 1) * S.lam u :=
        sum_le_sum_of_subset himg
    _ = ∑ w ∈ S.aperySet S.multiplicity, S.lam w +
          ∑ w ∈ S.aperySet S.multiplicity, S.nu p w * S.lam w := by
        rw [← sum_add_distrib]
        apply sum_congr rfl
        intro w _
        ring

/-- Termwise comparison of a factorization with the depths. -/
theorem linkSum_add_ge {w : ℕ} {f : ℕ → ℕ} (hf : ∑ q ∈ S.primitives', f q * q = w) :
    S.linkBase w + ∑ q ∈ S.primitives', f q * S.lam (w - q) ≤
      S.linkSum w + (∑ q ∈ S.primitives', f q) * S.lam w := by
  unfold linkBase linkSum
  rw [sum_mul, ← sum_add_distrib, ← sum_add_distrib]
  apply sum_le_sum
  intro q hq
  have h1 := le_nu_of_fact hf hq
  have h2 : S.lam w ≤ S.lam (w - q) := lam_le_lam_sub w q
  obtain ⟨u, hu⟩ := Nat.exists_eq_add_of_le h1
  obtain ⟨v, hv⟩ := Nat.exists_eq_add_of_le h2
  rw [hu, hv]
  nlinarith [Nat.zero_le (u * v)]

theorem factor_le {w q : ℕ} {f : ℕ → ℕ} (hf : ∑ q ∈ S.primitives', f q * q = w)
    (hq : q ∈ S.primitives') (h1 : 1 ≤ f q) : q ≤ w := by
  have hs := Finset.single_le_sum (f := fun q => f q * q) (fun _ _ => Nat.zero_le _) hq
  rw [hf] at hs
  have h2 : 1 * q ≤ f q * q := Nat.mul_le_mul_right q h1
  omega

/-- The floor inequality: `J (M - w) + w + J ≤ m Σ_q f_q λ(w - q) + J m`. -/
theorem floor_sum {w : ℕ} {f : ℕ → ℕ} (hf : ∑ q ∈ S.primitives', f q * q = w)
    (hwM : w ≤ S.aperyMax S.multiplicity) :
    (∑ q ∈ S.primitives', f q) * (S.aperyMax S.multiplicity - w) + w +
        ∑ q ∈ S.primitives', f q ≤
      S.multiplicity * ∑ q ∈ S.primitives', f q * S.lam (w - q) +
        (∑ q ∈ S.primitives', f q) * S.multiplicity := by
  have hm := S.multiplicity_pos
  have hterm : ∀ q ∈ S.primitives',
      f q * (S.aperyMax S.multiplicity - w) + f q * q + f q ≤
        S.multiplicity * (f q * S.lam (w - q)) + f q * S.multiplicity := by
    intro q hq
    rcases Nat.eq_zero_or_pos (f q) with h0 | hpos
    · simp [h0]
    have hqw := factor_le hf hq hpos
    have hlt : S.aperyMax S.multiplicity - (w - q) <
        S.multiplicity * (S.lam (w - q) + 1) := by
      unfold lam
      exact Nat.lt_mul_div_succ _ hm
    rw [mul_add, mul_one] at hlt
    have h1 : S.aperyMax S.multiplicity - w + q + 1 ≤
        S.multiplicity * S.lam (w - q) + S.multiplicity := by omega
    calc f q * (S.aperyMax S.multiplicity - w) + f q * q + f q
        = f q * (S.aperyMax S.multiplicity - w + q + 1) := by ring
      _ ≤ f q * (S.multiplicity * S.lam (w - q) + S.multiplicity) :=
          Nat.mul_le_mul_left _ h1
      _ = S.multiplicity * (f q * S.lam (w - q)) + f q * S.multiplicity := by ring
  have hs := sum_le_sum hterm
  simp only [sum_add_distrib, ← sum_mul, ← mul_sum, hf] at hs
  exact hs

/-- `λ(0) ≥ 4` when `c > 3m`. -/
theorem four_le_lam_zero (hq1 : 3 * S.multiplicity < S.conductor) : 4 ≤ S.lam 0 := by
  have hm := S.multiplicity_pos
  have hMeq := aperyMax_eq S.multiplicity_mem hm
  unfold lam
  rw [Nat.sub_zero, Nat.le_div_iff_mul_le hm]
  omega

theorem pointwise_zero (hq1 : 3 * S.multiplicity < S.conductor) :
    4 + S.linkBase 0 ≤ S.lam 0 + S.linkSum 0 := by
  have h4 := four_le_lam_zero hq1
  have hL : S.linkSum 0 = S.linkBase 0 := by
    unfold linkSum linkBase
    apply sum_congr rfl
    intro q _
    rw [Nat.zero_sub]
  omega

/-- **Pointwise bound, length one.** If `c > 3m` and `w` has a factorization of length one, then
`λ(w) + L1(w) ≥ 4 + N(w)`. -/
theorem pointwise_one {w : ℕ} (hq1 : 3 * S.multiplicity < S.conductor)
    (hw : S.IsApery S.multiplicity w) {f : ℕ → ℕ}
    (hf : ∑ q ∈ S.primitives', f q * q = w) (hJ : ∑ q ∈ S.primitives', f q = 1) :
    4 + S.linkBase w ≤ S.lam w + S.linkSum w := by
  have hm := S.multiplicity_pos
  have hMeq := aperyMax_eq S.multiplicity_mem hm
  have hwM : w ≤ S.aperyMax S.multiplicity :=
    le_aperyMax ((mem_aperySet S.multiplicity_mem hm).2 hw)
  have hkey := linkSum_add_ge hf
  have hfl := floor_sum hf hwM
  rw [hJ] at hkey hfl
  have hsf : 4 ≤ ∑ q ∈ S.primitives', f q * S.lam (w - q) := by
    by_contra hlt
    have : S.multiplicity * ∑ q ∈ S.primitives', f q * S.lam (w - q) ≤
        S.multiplicity * 3 := Nat.mul_le_mul_left _ (by omega)
    omega
  omega

/-- **Pointwise bound.** If `c > 3m`, then `λ(w) + L1(w) ≥ 3 + N(w)` for every Apéry `w`. -/
theorem pointwise_three {w : ℕ} (hq1 : 3 * S.multiplicity < S.conductor)
    (hw : S.IsApery S.multiplicity w) :
    3 + S.linkBase w ≤ S.lam w + S.linkSum w := by
  obtain ⟨f, hf⟩ := exists_fact_of_isApery hw
  have hm := S.multiplicity_pos
  have hMeq := aperyMax_eq S.multiplicity_mem hm
  have hwM : w ≤ S.aperyMax S.multiplicity :=
    le_aperyMax ((mem_aperySet S.multiplicity_mem hm).2 hw)
  have hkey := linkSum_add_ge hf
  have hfl := floor_sum hf hwM
  have hlamw : S.multiplicity * S.lam w ≤ S.aperyMax S.multiplicity - w := by
    unfold lam
    exact Nat.mul_div_le _ _
  have hstep : (∑ q ∈ S.primitives', f q) * (S.lam w + 1) ≤
      ∑ q ∈ S.primitives', f q * S.lam (w - q) := by
    rw [sum_mul]
    apply sum_le_sum
    intro q hq
    rcases Nat.eq_zero_or_pos (f q) with h0 | hpos
    · simp [h0]
    exact Nat.mul_le_mul_left _ (lam_succ_le_lam_sub hwM (factor_le hf hq hpos)
      (multiplicity_lt_of_mem_primitives' hq).le)
  rcases Nat.lt_or_ge (∑ q ∈ S.primitives', f q) 3 with hJ | hJ
  · rcases (by omega : ∑ q ∈ S.primitives', f q = 0 ∨ ∑ q ∈ S.primitives', f q = 1 ∨
        ∑ q ∈ S.primitives', f q = 2) with hJ0 | hJ1 | hJ2
    · have hz : ∀ q ∈ S.primitives', f q = 0 := Finset.sum_eq_zero_iff.1 hJ0
      have hw0 : w = 0 := by
        rw [← hf]
        exact sum_eq_zero fun q hq => by rw [hz q hq, zero_mul]
      subst hw0
      have := pointwise_zero hq1
      omega
    · have := pointwise_one hq1 hw hf hJ1
      omega
    · -- `J = 2`: `2 (M - w) + w + 2 ≤ m Σf + 2m`, `m λ(w) ≤ M - w`, `M ≥ 4m` give `Σf ≥ λ(w) + 3`.
      rw [hJ2] at hkey hfl
      have hsf : S.lam w + 3 ≤ ∑ q ∈ S.primitives', f q * S.lam (w - q) := by
        by_contra hlt
        have h1 : S.multiplicity * ∑ q ∈ S.primitives', f q * S.lam (w - q) ≤
            S.multiplicity * (S.lam w + 2) := Nat.mul_le_mul_left _ (by omega)
        rw [mul_add] at h1
        omega
      omega
  · -- `J ≥ 3`: each factor drops `λ` by at least one.
    rw [mul_add, mul_one] at hstep
    have : 3 * S.lam w ≤ (∑ q ∈ S.primitives', f q) * S.lam w := Nat.mul_le_mul_right _ hJ
    omega

/-- **Theorem.** If `c > 3m`, then `e · ℓ ≥ 3m + e`. -/
theorem three_mul_add_embDim_le (hq1 : 3 * S.multiplicity < S.conductor) :
    3 * S.multiplicity + S.embDim ≤ S.embDim * S.ell := by
  classical
  have hm := S.multiplicity_pos
  have hTA : insert 0 S.primitives' ⊆ S.aperySet S.multiplicity := by
    intro w hw
    rw [mem_insert] at hw
    rw [mem_aperySet S.multiplicity_mem hm]
    rcases hw with rfl | hw
    · exact isApery_zero'
    · exact isApery_of_mem_primitives' hw
  have h0T : (0 : ℕ) ∉ S.primitives' := fun h => by have := pos_of_mem_primitives' h; omega
  have hcardT : (insert 0 S.primitives').card = S.embDim := by
    rw [card_insert_of_notMem h0T, card_primitives'_add_one]
  have hpt : ∀ w ∈ S.aperySet S.multiplicity,
      3 + (if w ∈ insert 0 S.primitives' then 1 else 0) + S.linkBase w ≤
        S.lam w + S.linkSum w := by
    intro w hw
    have hwA : S.IsApery S.multiplicity w := (mem_aperySet S.multiplicity_mem hm).1 hw
    split_ifs with hwT
    · rw [mem_insert] at hwT
      rcases hwT with rfl | hwP
      · have := pointwise_zero hq1
        omega
      · have := pointwise_one hq1 hwA (f := fun q => if q = w then 1 else 0)
          (by simp [hwP]) (by simp [hwP])
        omega
    · have := pointwise_three hq1 hwA
      omega
  have hsum := sum_le_sum hpt
  simp only [sum_add_distrib] at hsum
  have h3 : ∑ w ∈ S.aperySet S.multiplicity, 3 = 3 * S.multiplicity := by
    rw [sum_const, card_aperySet hm, smul_eq_mul, mul_comm]
  have hind : ∑ w ∈ S.aperySet S.multiplicity, (if w ∈ insert 0 S.primitives' then 1 else 0) =
      S.embDim := by
    rw [sum_ite_mem, inter_eq_right.2 hTA, sum_const, smul_eq_mul, mul_one, hcardT]
  have hcol : ∑ w ∈ S.aperySet S.multiplicity, S.linkSum w ≤
      S.primitives'.card * S.ell + ∑ w ∈ S.aperySet S.multiplicity, S.linkBase w := by
    unfold linkSum linkBase
    calc ∑ w ∈ S.aperySet S.multiplicity, ∑ p ∈ S.primitives', S.nu p w * S.lam (w - p)
        = ∑ p ∈ S.primitives', ∑ w ∈ S.aperySet S.multiplicity, S.nu p w * S.lam (w - p) :=
          sum_comm
      _ ≤ ∑ p ∈ S.primitives', (∑ w ∈ S.aperySet S.multiplicity, S.lam w +
            ∑ w ∈ S.aperySet S.multiplicity, S.nu p w * S.lam w) :=
          sum_le_sum fun p hp => column_sum_le hp
      _ = S.primitives'.card * S.ell + ∑ p ∈ S.primitives',
            ∑ w ∈ S.aperySet S.multiplicity, S.nu p w * S.lam w := by
          rw [sum_add_distrib, sum_const, smul_eq_mul, ell_eq_sum_lam]
      _ = S.primitives'.card * S.ell + ∑ w ∈ S.aperySet S.multiplicity,
            ∑ p ∈ S.primitives', S.nu p w * S.lam w := by
          rw [sum_comm]
  have hell := ell_eq_sum_lam (S := S)
  have he : S.embDim * S.ell = S.primitives'.card * S.ell + S.ell := by
    rw [← card_primitives'_add_one (S := S)]
    ring
  omega

/-- **Wilf for `3m < c ≤ 3m + e`.** -/
theorem wilf_of_conductor_le_three_mul_add_embDim (hq1 : 3 * S.multiplicity < S.conductor)
    (h : S.conductor ≤ 3 * S.multiplicity + S.embDim) : S.conductor ≤ S.embDim * S.ell :=
  h.trans (three_mul_add_embDim_le hq1)

end NumericalSemigroup
