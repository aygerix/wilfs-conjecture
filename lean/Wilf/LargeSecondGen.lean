import Wilf.MaxCL

/-!
# Wilf's conjecture for a large second generator

If every minimal generator `p ≠ m` satisfies `3 * p > max Ap(S, m)`, equivalently
`3 * n₁ > c + m - 1` for the least minimal generator `n₁ > m`, then every Apéry element has a
factorization of length at most two, and Wilf's inequality `c ≤ e * ℓ` follows from
`wilf_of_apery_height_le_two` (Flat-MaxCL).

This is Spirito's "large second generator" condition `n₁ > (c + m) / 3` (arXiv:1710.09245), here
without his further hypotheses on `e` and `m`; the bound `c + m - 1` is slightly weaker than `c + m`.
-/

namespace NumericalSemigroup

open Finset

variable (S : NumericalSemigroup)

/-- **Wilf for a large second generator.** If `3 * p > max Ap(S, m)` for every minimal generator
`p ≠ m`, then `c ≤ e * ℓ`. -/
theorem wilf_of_aperyMax_lt_three_mul
    (h : ∀ p ∈ S.primitives', S.aperyMax S.multiplicity < 3 * p) :
    S.conductor ≤ S.embDim * S.ell := by
  apply wilf_of_apery_height_le_two
  intro w hw
  have hA : S.IsApery S.multiplicity w := (mem_aperySet S.multiplicity_mem S.multiplicity_pos).1 hw
  obtain ⟨x, hx⟩ := exists_wt_eq hA
  refine ⟨x, hx, ?_⟩
  by_contra hlt
  push Not at hlt
  have hwle : w ≤ S.aperyMax S.multiplicity := le_aperyMax hw
  set K := S.aperyMax S.multiplicity with hK
  -- `3 * wt x = Σ x a * (3 * gen a) ≥ Σ x a * (K + 1) = (Σ x a) * (K + 1)`
  have key : (∑ a, x a) * (K + 1) ≤ 3 * S.wt x := by
    unfold wt
    rw [Finset.sum_mul, Finset.mul_sum]
    apply Finset.sum_le_sum
    intro a _
    have hg : K < 3 * S.gen a := h _ (gen_mem a)
    have : x a * (K + 1) ≤ x a * (3 * S.gen a) := Nat.mul_le_mul_left _ (by omega)
    calc x a * (K + 1) ≤ x a * (3 * S.gen a) := this
      _ = 3 * (x a * S.gen a) := by ring
  rw [hx] at key
  have h3 : 3 * (K + 1) ≤ (∑ a, x a) * (K + 1) := Nat.mul_le_mul_right _ hlt
  linarith

/-- The same statement with the conductor: if `3 * p > c + m - 1` for every minimal generator
`p ≠ m` (i.e. `3 * n₁ ≥ c + m`), then `c ≤ e * ℓ`. -/
theorem wilf_of_conductor_add_mult_le_three_mul
    (h : ∀ p ∈ S.primitives', S.conductor + S.multiplicity - 1 < 3 * p) :
    S.conductor ≤ S.embDim * S.ell := by
  apply wilf_of_aperyMax_lt_three_mul
  intro p hp
  rw [aperyMax_eq S.multiplicity_mem S.multiplicity_pos]
  exact h p hp

end NumericalSemigroup
