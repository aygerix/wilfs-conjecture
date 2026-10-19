import Wilf.TileTop

/-!
# The column-top lemma

For a finite down-set `D ⊆ ℕ^d` and a direction `a`,

    Σ_{y ∈ D maximal} (d + |y|)·y_a ≤ (d + 1)·Σ_{x ∈ D} x_a        (`column_top_lemma`).

Proof. `d + |y| = Σ_b (y_b + 1)`, and a maximal cell is a `b`-top for every `b`. By the column
decomposition (`sum_columns`), for `b ≠ a` the `b`-tops satisfy
`Σ_{b-tops y} (y_b + 1)·y_a = Σ_D x_a` (the coordinate `x_a` is constant on `b`-columns), and for
`b = a` they satisfy `Σ_{a-tops y} (y_a + 1)·y_a = 2·Σ_D x_a` (`sum_tops_mul_self`). Summing over the
`d` directions gives at most `(d - 1 + 2)·Σ_D x_a`.

Use: with `ℓ(x) = ρ_0 + Σ_a x_a δ_a` (`δ_a ≥ 0`) this says that the linear part of MaxCL is
nonpositive, so MaxCL holds trivially when no residue wraps.
-/

namespace NumericalSemigroup

open Finset

variable {d : ℕ} {D : Finset (Fin d → ℕ)}

/-- `2·Σ_{k ≤ n} (n - k) = (n + 1)·n`. -/
theorem two_mul_sum_range_sub (n : ℕ) : 2 * ∑ k ∈ range (n + 1), (n - k) = (n + 1) * n := by
  have h' : ∑ k ∈ range (n + 1), (n - k) = ∑ k ∈ range (n + 1), k := by
    have h := Finset.sum_range_reflect (fun k => k) (n + 1)
    simpa using h
  rw [h', mul_comm, Finset.sum_range_id_mul_two]
  simp

/-- In direction `a`, the `a`-tops satisfy `Σ (y_a + 1)·y_a = 2·Σ_{x ∈ D} x_a`. -/
theorem sum_tops_mul_self (hD : IsDownSetFin D) (a : Fin d) :
    ∑ y ∈ D.filter (fun y => y + Pi.single a 1 ∉ D), (y a + 1) * y a = 2 * ∑ x ∈ D, x a := by
  rw [sum_columns hD a (fun x => x a), Finset.mul_sum]
  refine Finset.sum_congr rfl fun y _ => ?_
  have hk : ∀ k ∈ range (y a + 1), (y - Pi.single a k : Fin d → ℕ) a = y a - k := by
    intro k _
    simp
  rw [Finset.sum_congr rfl hk, two_mul_sum_range_sub]

/-- In a direction `b ≠ a`, the `b`-tops satisfy `Σ (y_b + 1)·y_a = Σ_{x ∈ D} x_a`. -/
theorem sum_tops_mul_other (hD : IsDownSetFin D) {a b : Fin d} (hba : b ≠ a) :
    ∑ y ∈ D.filter (fun y => y + Pi.single b 1 ∉ D), (y b + 1) * y a = ∑ x ∈ D, x a := by
  rw [sum_columns hD b (fun x => x a)]
  refine Finset.sum_congr rfl fun y _ => ?_
  have hk : ∀ k ∈ range (y b + 1), (y - Pi.single b k : Fin d → ℕ) a = y a := by
    intro k _
    simp [Pi.single_eq_of_ne (Ne.symm hba)]
  rw [Finset.sum_congr rfl hk, Finset.sum_const, card_range, smul_eq_mul]

/-- **Column-top lemma.** For every finite down-set `D ⊆ ℕ^d` and direction `a`,
`Σ_{y ∈ D maximal} (d + |y|)·y_a ≤ (d + 1)·Σ_{x ∈ D} x_a`. -/
theorem column_top_lemma (hD : IsDownSetFin D) (a : Fin d) :
    ∑ y ∈ D.filter (IsMaxCell D), (d + ∑ b, y b) * y a ≤ (d + 1) * ∑ x ∈ D, x a := by
  have h1 : ∀ y : Fin d → ℕ, (d + ∑ b, y b) * y a = ∑ b, (y b + 1) * y a := by
    intro y
    rw [← Finset.sum_mul, Finset.sum_add_distrib, Finset.sum_const, Finset.card_univ,
      Fintype.card_fin, smul_eq_mul, mul_one, add_comm]
  simp_rw [h1]
  rw [Finset.sum_comm]
  have hb : ∀ b : Fin d, ∑ y ∈ D.filter (IsMaxCell D), (y b + 1) * y a ≤
      (1 + if b = a then 1 else 0) * ∑ x ∈ D, x a := by
    intro b
    have hsub : D.filter (IsMaxCell D) ⊆ D.filter (fun y => y + Pi.single b 1 ∉ D) := by
      intro y hy
      simp only [mem_filter] at hy ⊢
      exact ⟨hy.1, hy.2 b⟩
    calc ∑ y ∈ D.filter (IsMaxCell D), (y b + 1) * y a
        ≤ ∑ y ∈ D.filter (fun y => y + Pi.single b 1 ∉ D), (y b + 1) * y a :=
          Finset.sum_le_sum_of_subset_of_nonneg hsub (fun _ _ _ => Nat.zero_le _)
      _ = (1 + if b = a then 1 else 0) * ∑ x ∈ D, x a := by
          split_ifs with hba
          · subst hba
            rw [sum_tops_mul_self hD b]
          · rw [add_zero, one_mul, sum_tops_mul_other hD hba]
  calc ∑ b, ∑ y ∈ D.filter (IsMaxCell D), (y b + 1) * y a
      ≤ ∑ b : Fin d, (1 + if b = a then 1 else 0) * ∑ x ∈ D, x a :=
        Finset.sum_le_sum fun b _ => hb b
    _ = (d + 1) * ∑ x ∈ D, x a := by
      rw [← Finset.sum_mul, Finset.sum_add_distrib, Finset.sum_const, Finset.card_univ,
        Fintype.card_fin, smul_eq_mul, mul_one, Finset.sum_ite_eq' Finset.univ a (fun _ => 1)]
      simp

end NumericalSemigroup
