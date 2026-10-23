import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Lean.Elab.Tactic.Omega

/-!
Finite matching step of the upper-closure repair bound.
This file does not formalize the semigroup construction of the baseline or the
repair demands, and does not assert universal Wilf nonnegativity.
-/
namespace Wilf

open scoped BigOperators

/-- A permutation uses each repair variable exactly twice. -/
theorem assignment_repair_sum_bound {ι : Type*} [Fintype ι]
    (π : Equiv.Perm ι) (t : ι → ℝ) (H : ι → ι → ℝ)
    (h : ∀ i, H i (π i) ≤ t i + t (π i)) :
    (∑ i, H i (π i)) ≤ 2 * ∑ i, t i := by
  calc
    (∑ i, H i (π i)) ≤ ∑ i, (t i + t (π i)) :=
      Finset.sum_le_sum fun i _ => h i
    _ = 2 * ∑ i, t i := by
      rw [Finset.sum_add_distrib, Equiv.sum_comp π]
      ring

/-- Integer repair counts justify rounding the assignment lower bound upward. -/
theorem rounded_assignment_repair_bound (W B e M T : ℤ)
    (he : 0 ≤ e) (hW : W = B + e * T) (hM : M ≤ 2 * T) :
    B + e * ((M + 1) / 2) ≤ W := by
  have hceil : (M + 1) / 2 ≤ T := by omega
  have hmul := mul_le_mul_of_nonneg_left hceil he
  omega

end Wilf

#print axioms Wilf.assignment_repair_sum_bound
#print axioms Wilf.rounded_assignment_repair_bound
