import Wilf.NoWrap

/-!
# Tile-CL implies MaxCL, for any tile

`TileCLAt D p` (`Σ_{y∈D} T(y)·⟨s − φ(y)⟩ ≥ (d−1)·m(m−1)/2` for every `s`) is the same as
`Σ_{y∈D} T(y)·⟨φ(y) − σ⟩ ≤ (d+1)·m(m−1)/2` for every `σ` (put `σ = s + 1`, use `Σ_D T = d·m`).
Dropping the non-maximal tops (`T ≥ 0`) and using `T(y) = d + |y|` on maximal cells gives `MaxCLAt`.

So any proof of Tile-CL on a class of tiles (for example the WRAP-MAX conjecture H1′, which is
exactly Tile-CL on tiles whose canonical lift does not wrap on non-maximal cells) yields MaxCL,
hence Tile-TOP'' and Wilf, on that class.
-/

namespace NumericalSemigroup

open Finset

variable {d : ℕ} {D : Finset (Fin d → ℕ)}

theorem maxCLAt_of_tileCLAt {m : ℕ} {p : Fin d → ZMod m} (hT : IsTile D p) (h : TileCLAt D p) :
    MaxCLAt D p := by
  intro σ
  have hm := hT.pos
  have : NeZero m := ⟨hm.ne'⟩
  have hcl := h (σ - 1)
  have hk : ∀ y, (σ - 1 - tilePhi p y).val + ((tilePhi p y - σ).val + 1) = m := by
    intro y
    have h1 := sub_val_eq_val_sub_add_one (σ - 1) (tilePhi p y)
    have h2 := ZMod.val_lt (σ - 1 - tilePhi p y)
    rw [sub_add_cancel] at h1
    omega
  have hZ := sum_tileT hT.1
  rw [hT.2.1] at hZ
  have hR := hT.sum_val_mul_two σ
  have hmax : ∑ y ∈ D.filter (IsMaxCell D), (d + ∑ a, y a) * (tilePhi p y - σ).val ≤
      ∑ y ∈ D, tileT D y * (tilePhi p y - σ).val := by
    rw [Finset.sum_filter]
    apply Finset.sum_le_sum
    intro y _
    split_ifs with hmc
    · rw [tileT_of_isMaxCell hmc]
    · exact Nat.zero_le _
  have hsplit : ∑ y ∈ D, tileT D y * (σ - 1 - tilePhi p y).val +
      ∑ y ∈ D, tileT D y * (tilePhi p y - σ).val + ∑ y ∈ D, tileT D y =
      m * ∑ y ∈ D, tileT D y := by
    rw [← Finset.sum_add_distrib, ← Finset.sum_add_distrib, Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro y _
    calc tileT D y * (σ - 1 - tilePhi p y).val + tileT D y * (tilePhi p y - σ).val + tileT D y
        = tileT D y * ((σ - 1 - tilePhi p y).val + ((tilePhi p y - σ).val + 1)) := by ring
      _ = m * tileT D y := by rw [hk y, mul_comm]
  generalize ∑ y ∈ D, tileT D y * (σ - 1 - tilePhi p y).val = X at hcl hsplit
  generalize ∑ y ∈ D, tileT D y * (tilePhi p y - σ).val = Y at hmax hsplit
  generalize ∑ y ∈ D, tileT D y = Z at hZ hsplit
  generalize ∑ x ∈ D, (tilePhi p x - σ).val = R at hR ⊢
  generalize ∑ y ∈ D.filter (IsMaxCell D), (d + ∑ a, y a) * (tilePhi p y - σ).val = Mx at hmax ⊢
  subst hZ
  have hmZ : m * (d * m) = d * m + d * (m * (m - 1)) := by
    obtain ⟨k, rfl⟩ : ∃ k, m = k + 1 := ⟨m - 1, by omega⟩
    simp only [Nat.add_sub_cancel]
    ring
  have hdiv : m * (m - 1) / 2 = R := by rw [← hR, Nat.mul_div_cancel _ (by norm_num)]
  rw [hdiv] at hcl
  rw [hmZ, ← hR] at hsplit
  have hXY : X + Y = d * (R * 2) := by omega
  rcases d with _ | d'
  · simp at hXY
    omega
  · simp only [Nat.add_sub_cancel] at hcl
    nlinarith

end NumericalSemigroup
