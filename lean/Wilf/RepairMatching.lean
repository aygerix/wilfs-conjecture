import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.SplitIfs
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

/-- The unit upper-row penalty is supported on two explicit residue regions.
`s` is the nonzero sum residue, and `rp` is its conductor-shifted residue.
This algebraic identity does not assert semigroup realizability. -/
theorem upper_penalty_position (m r i j s rp : ℤ)
    (_hm : 2 ≤ m) (hr0 : 0 ≤ r) (hrm : r < m)
    (hi0 : 0 < i) (him : i < m) (hj0 : 0 < j) (hjm : j < m)
    (_hne : i + j ≠ m)
    (hs : s = if i + j > m then i + j - m else i + j)
    (hrp : rp = if s > r then s - r - 1 else s + m - r - 1) :
    (if rp ≤ r - 1 ∧ i ≤ r ∧ j ≤ r then (1 : ℤ) else 0) -
        ((if i + j > m then (1 : ℤ) else 0) +
          (if s > r then (1 : ℤ) else 0) -
          (if i > r then (1 : ℤ) else 0) -
          (if j > r then (1 : ℤ) else 0)) =
      (if i ≤ r ∧ j ≤ r ∧ i + j ≤ 2 * r - m then (1 : ℤ) else 0) +
        (if i > r ∧ j > r ∧ i + j ≤ m + r then (1 : ℤ) else 0) := by
  split_ifs at * <;> omega

/-- A tight split into the largest Apéry residue has no lower-row allowance. -/
theorem lower_allowance_at_top (m r i j : ℤ)
    (_hm : 2 ≤ m) (hr0 : 0 < r) (hrm : r < m)
    (hi0 : 0 < i) (him : i < m) (hj0 : 0 < j) (hjm : j < m)
    (hsum : i + j = r ∨ i + j = r + m) :
    ((if i + j > m then (1 : ℤ) else 0) -
      (if i > r then (1 : ℤ) else 0) -
      (if j > r then (1 : ℤ) else 0)) +
      (if m - 1 ≥ r + 1 ∧ i > r ∧ j > r then (1 : ℤ) else 0) = 0 := by
  rcases hsum with hsum | hsum <;> split_ifs <;> omega

/-- Nonnegative unpaid amounts cannot survive an exact split into a zero target. -/
theorem unpaid_vanishes_at_exact_split (x y : ℝ)
    (hx : 0 ≤ x) (hy : 0 ≤ y) (hxy : x + y ≤ 0) : x = 0 ∧ y = 0 := by
  exact ⟨le_antisymm (le_trans (le_add_of_nonneg_right hy) hxy) hx,
    le_antisymm (le_trans (le_add_of_nonneg_left hx) hxy) hy⟩

end Wilf

#print axioms Wilf.assignment_repair_sum_bound
#print axioms Wilf.rounded_assignment_repair_bound
#print axioms Wilf.upper_penalty_position
#print axioms Wilf.lower_allowance_at_top
#print axioms Wilf.unpaid_vanishes_at_exact_split
