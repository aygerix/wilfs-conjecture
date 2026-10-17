import Wilf.Carry

/-!
# The Ramp Lemma

Formalization of `.research/PROOFS.md`, section "Ramp Lemma" (2026-10-17).

Let `D ⊆ ℕ^d` be a finite down-set (`IsDownSetFin D`), `T = tileT D`, `β(y) = (d + 1) - T(y) ∈ ℤ`
(`tileBeta D y`). Call `ρ : ℕ^d → K` *directionally convex* (`DirConvex ρ`) if
`Δ_a ρ(u) := ρ(u + e_a) - ρ(u)` satisfies `Δ_a ρ(u) ≤ Δ_a ρ(u + e_b)` for all directions `a, b`
(`b = a` included) and all `u`. Then (`rampLemma`)

    Σ_{y∈D} β(y)·ρ(y) ≤ |D|·ρ(0).

`K` is any linearly ordered commutative ring with `IsStrictOrderedRing` (e.g. `ℤ`, `ℚ`, `ℝ`).
The concave version (`rampLemma_concave`, reversed inequality) follows by applying the lemma to `-ρ`.

Proof (as in the paper, with the lexicographic path replaced by an order-free induction):
* `DirConvex.incr_mono`: if `u ≤ v` then `ρ(u + w) - ρ(u) ≤ ρ(v + w) - ρ(v)` for every `w`;
* step 1 (`sub_zero_le_sum_sub`): `ρ(x) - ρ(0) ≤ Σ_a (ρ(x) - ρ(x - x_a e_a))`;
* step 2 (`column_ineq`): on each `a`-column `{y - k e_a | k ≤ y_a}` with top `y`,
  `Σ_k (ρ(y - k e_a) - ρ(y - y_a e_a)) ≤ Σ_k (ρ(y) - ρ(y - k e_a))` (pair `k` with `y_a - k`);
* `sum_tileT_mul`: `Σ_{y∈D} T(y)·f(y) = Σ_a Σ_{a-tops y} (y_a + 1)·f(y)` (exchange of summation).
-/

namespace NumericalSemigroup

open Finset

section Ramp

variable {ι : Type*} [Fintype ι] [DecidableEq ι]
variable {K : Type*} [CommRing K] [LinearOrder K] [IsStrictOrderedRing K]

/-- `ρ` is *directionally convex*: `Δ_a ρ(u) ≤ Δ_a ρ(u + e_b)` for all `a, b` (`b = a` included)
and all `u`, where `Δ_a ρ(u) = ρ(u + e_a) - ρ(u)`. -/
def DirConvex (ρ : (ι → ℕ) → K) : Prop :=
  ∀ (a b : ι) (u : ι → ℕ), ρ (u + Pi.single a 1) - ρ u ≤
    ρ (u + Pi.single b 1 + Pi.single a 1) - ρ (u + Pi.single b 1)

omit [Fintype ι] in
/-- Induction principle on `ι → ℕ`: `0`, the unit vectors, and closure under `+`. -/
theorem pi_nat_induction [Fintype ι] {P : (ι → ℕ) → Prop} (h0 : P 0)
    (hadd : ∀ x y, P x → P y → P (x + y)) (hs : ∀ b, P (Pi.single b 1)) (w : ι → ℕ) : P w := by
  rw [← Finset.univ_sum_single w]
  refine Finset.sum_induction _ P hadd h0 fun b _ => ?_
  generalize w b = n
  induction n with
  | zero => simpa using h0
  | succ n ih => rw [Pi.single_add]; exact hadd _ _ ih (hs b)

variable {ρ : (ι → ℕ) → K}

omit [IsStrictOrderedRing K] in
/-- `Δ_a ρ` is monotone: `Δ_a ρ(u) ≤ Δ_a ρ(u + w)` for every `w ≥ 0`. -/
theorem DirConvex.delta_mono (hρ : DirConvex ρ) (a : ι) (w u : ι → ℕ) :
    ρ (u + Pi.single a 1) - ρ u ≤ ρ (u + w + Pi.single a 1) - ρ (u + w) := by
  induction w using pi_nat_induction generalizing u with
  | h0 => simp
  | hadd x y hx hy =>
    refine (hx u).trans ?_
    have := hy (u + x)
    rwa [← add_assoc]
  | hs b => exact hρ a b u

/-- **Increasing differences**: if `u ≤ v` then `ρ(u + w) - ρ(u) ≤ ρ(v + w) - ρ(v)`. -/
theorem DirConvex.incr_mono (hρ : DirConvex ρ) {u v : ι → ℕ} (huv : u ≤ v) (w : ι → ℕ) :
    ρ (u + w) - ρ u ≤ ρ (v + w) - ρ v := by
  obtain ⟨t, rfl⟩ : ∃ t, v = u + t := ⟨v - u, by
    funext i; have h : u i ≤ v i := huv i; simp only [Pi.add_apply, Pi.sub_apply]; omega⟩
  clear huv
  refine (pi_nat_induction
    (P := fun w => ∀ u : ι → ℕ, ρ (u + w) - ρ u ≤ ρ (u + t + w) - ρ (u + t)) ?_ ?_ ?_ w) u
  · intro u; simp
  · intro x y hx hy u
    have h1 := hx u
    have h2 := hy (u + x)
    have e1 : u + (x + y) = u + x + y := by rw [add_assoc]
    have e2 : u + t + (x + y) = u + x + t + y := by abel
    have e3 : u + t + x = u + x + t := by abel
    rw [e1, e2]
    rw [e3] at h1
    linarith
  · intro b u; exact hρ.delta_mono b t u

/-- **Step 1.** `ρ(x) - ρ(0) ≤ Σ_a (ρ(x) - ρ(x - x_a e_a))`. -/
theorem DirConvex.sub_zero_le_sum_sub (hρ : DirConvex ρ) (x : ι → ℕ) :
    ρ x - ρ 0 ≤ ∑ a, (ρ x - ρ (x - Pi.single a (x a))) := by
  have key : ∀ A : Finset ι, ρ (fun b => if b ∈ A then x b else 0) - ρ 0 ≤
      ∑ a ∈ A, (ρ x - ρ (x - Pi.single a (x a))) := by
    intro A
    induction A using Finset.induction_on with
    | empty => simp; rfl
    | insert a A ha ih =>
      rw [Finset.sum_insert ha]
      set r : ι → ℕ := fun b => if b ∈ A then x b else 0 with hr
      have hsplit : (fun b => if b ∈ insert a A then x b else 0) = r + Pi.single a (x a) := by
        funext b
        by_cases hb : b = a
        · subst hb; simp [hr, ha]
        · simp [hr, hb]
      have hle : r ≤ x - Pi.single a (x a) := by
        intro b
        by_cases hb : b = a
        · subst hb; simp [hr, ha]
        · simp only [hr, Pi.sub_apply, Pi.single_eq_of_ne hb, Nat.sub_zero]
          split_ifs <;> omega
      have hG := hρ.incr_mono hle (Pi.single a (x a))
      rw [sub_single_add_single le_rfl] at hG
      rw [hsplit]
      linarith
  have := key Finset.univ
  simpa using this

/-- **Step 2 (one column).** For `y` and a direction `a`, with `n = y_a`:
`Σ_{k ≤ n} (ρ(y - k e_a) - ρ(y - n e_a)) ≤ Σ_{k ≤ n} (ρ(y) - ρ(y - k e_a))`. -/
theorem DirConvex.column_ineq (hρ : DirConvex ρ) (a : ι) (y : ι → ℕ) :
    ∑ k ∈ range (y a + 1), (ρ (y - Pi.single a k) - ρ (y - Pi.single a (y a))) ≤
      ∑ k ∈ range (y a + 1), (ρ y - ρ (y - Pi.single a k)) := by
  conv_rhs => rw [← Finset.sum_range_reflect]
  refine Finset.sum_le_sum fun k hk => ?_
  have hk' : k ≤ y a := by have := Finset.mem_range.1 hk; omega
  simp only [Nat.add_sub_cancel]
  have hle : y - Pi.single a (y a) ≤ y - Pi.single a (y a - k) := by
    intro b
    by_cases hb : b = a
    · subst hb; simp
    · simp [Pi.single_eq_of_ne hb]
  have hG := hρ.incr_mono hle (Pi.single a (y a - k))
  have e1 : y - Pi.single a (y a) + Pi.single a (y a - k) = y - Pi.single a k := by
    funext b
    by_cases hb : b = a
    · subst hb; simp only [Pi.add_apply, Pi.sub_apply, Pi.single_eq_same]; omega
    · simp [Pi.single_eq_of_ne hb]
  rw [e1, sub_single_add_single (Nat.sub_le _ _)] at hG
  exact hG

omit [Fintype ι] in
theorem sub_single_sub_single_self (y : ι → ℕ) (a : ι) {k : ℕ} (hk : k ≤ y a) :
    y - Pi.single a k - Pi.single a ((y - Pi.single a k : ι → ℕ) a) = y - Pi.single a (y a) := by
  funext b
  by_cases hb : b = a
  · subst hb; simp only [Pi.sub_apply, Pi.single_eq_same]; omega
  · simp [Pi.single_eq_of_ne hb]

/-- **Step 2 (one direction).** For a finite down-set `D` and a direction `a`:
`Σ_{x∈D} (ρ(x) - ρ(x - x_a e_a)) ≤ Σ_{a-tops y} (y_a + 1)·ρ(y) - Σ_{x∈D} ρ(x)`. -/
theorem DirConvex.direction_ineq (hρ : DirConvex ρ) {D : Finset (ι → ℕ)} (hD : IsDownSetFin D)
    (a : ι) :
    ∑ x ∈ D, (ρ x - ρ (x - Pi.single a (x a))) ≤
      ∑ y ∈ D.filter (fun y => y + Pi.single a 1 ∉ D), ((y a : K) + 1) * ρ y - ∑ x ∈ D, ρ x := by
  rw [sum_columns hD a, sum_columns hD a ρ, ← Finset.sum_sub_distrib]
  refine Finset.sum_le_sum fun y _ => ?_
  have h1 : ∑ k ∈ range (y a + 1),
      (ρ (y - Pi.single a k) - ρ (y - Pi.single a k - Pi.single a ((y - Pi.single a k : ι → ℕ) a))) =
      ∑ k ∈ range (y a + 1), (ρ (y - Pi.single a k) - ρ (y - Pi.single a (y a))) := by
    refine Finset.sum_congr rfl fun k hk => ?_
    have hk' : k ≤ y a := by have := Finset.mem_range.1 hk; omega
    rw [sub_single_sub_single_self y a hk']
  have h2 : ((y a : K) + 1) * ρ y - ∑ k ∈ range (y a + 1), ρ (y - Pi.single a k) =
      ∑ k ∈ range (y a + 1), (ρ y - ρ (y - Pi.single a k)) := by
    rw [Finset.sum_sub_distrib, Finset.sum_const, Finset.card_range, nsmul_eq_mul]
    push_cast
    ring
  rw [h1, h2]
  exact hρ.column_ineq a y

end Ramp

/-! ## `T` as a sum over columns, `β`, and the Ramp Lemma -/

section RampTile

variable {d : ℕ} {K : Type*} [CommRing K] [LinearOrder K] [IsStrictOrderedRing K]

/-- `β(y) = (d + 1) - T(y)` (an integer). -/
def tileBeta (D : Finset (Fin d → ℕ)) (y : Fin d → ℕ) : ℤ := (d : ℤ) + 1 - tileT D y

/-- **Exchange of summation**: `Σ_{y∈D} T(y)·f(y) = Σ_a Σ_{y∈D, y+e_a∉D} (y_a + 1)·f(y)`. -/
theorem sum_tileT_mul {R : Type*} [CommRing R] (D : Finset (Fin d → ℕ)) (f : (Fin d → ℕ) → R) :
    ∑ y ∈ D, (tileT D y : R) * f y =
      ∑ a, ∑ y ∈ D.filter (fun y => y + Pi.single a 1 ∉ D), ((y a : R) + 1) * f y := by
  simp_rw [tileT, Finset.sum_filter]
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun y _ => ?_
  push_cast
  rw [Finset.sum_mul]
  refine Finset.sum_congr rfl fun a _ => ?_
  split_ifs <;> simp

/-- **Ramp Lemma.** For a finite down-set `D ⊆ ℕ^d` and a directionally convex `ρ : ℕ^d → K`:
`Σ_{y∈D} β(y)·ρ(y) ≤ |D|·ρ(0)` with `β(y) = (d + 1) - T(y)`. -/
theorem rampLemma {D : Finset (Fin d → ℕ)} (hD : IsDownSetFin D) {ρ : (Fin d → ℕ) → K}
    (hρ : DirConvex ρ) :
    ∑ y ∈ D, (tileBeta D y : K) * ρ y ≤ (D.card : K) * ρ 0 := by
  -- step 1 summed over `D`, then step 2 summed over the directions
  have h1 : ∑ x ∈ D, (ρ x - ρ 0) ≤ ∑ a, ∑ x ∈ D, (ρ x - ρ (x - Pi.single a (x a))) := by
    rw [Finset.sum_comm]
    exact Finset.sum_le_sum fun x _ => hρ.sub_zero_le_sum_sub x
  have h2 : ∑ a, ∑ x ∈ D, (ρ x - ρ (x - Pi.single a (x a))) ≤
      ∑ a, (∑ y ∈ D.filter (fun y => y + Pi.single a 1 ∉ D), ((y a : K) + 1) * ρ y -
        ∑ x ∈ D, ρ x) :=
    Finset.sum_le_sum fun a _ => hρ.direction_ineq hD a
  rw [Finset.sum_sub_distrib, ← sum_tileT_mul, Finset.sum_const, Finset.card_univ,
    Fintype.card_fin, nsmul_eq_mul] at h2
  rw [Finset.sum_sub_distrib, Finset.sum_const, nsmul_eq_mul] at h1
  have hβ : ∑ y ∈ D, (tileBeta D y : K) * ρ y =
      ((d : K) + 1) * ∑ y ∈ D, ρ y - ∑ y ∈ D, (tileT D y : K) * ρ y := by
    rw [Finset.mul_sum, ← Finset.sum_sub_distrib]
    refine Finset.sum_congr rfl fun y _ => ?_
    simp only [tileBeta]
    push_cast
    ring
  rw [hβ]
  linarith

/-- The concave version: if `-ρ` is directionally convex then `Σ_{y∈D} β(y)·ρ(y) ≥ |D|·ρ(0)`. -/
theorem rampLemma_concave {D : Finset (Fin d → ℕ)} (hD : IsDownSetFin D) {ρ : (Fin d → ℕ) → K}
    (hρ : DirConvex (fun y => -ρ y)) :
    (D.card : K) * ρ 0 ≤ ∑ y ∈ D, (tileBeta D y : K) * ρ y := by
  have := rampLemma hD hρ
  simp only [mul_neg, Finset.sum_neg_distrib] at this
  linarith

/-- The affine case: if `ρ` and `-ρ` are both directionally convex then
`Σ_{y∈D} β(y)·ρ(y) = |D|·ρ(0)`. -/
theorem rampLemma_eq {D : Finset (Fin d → ℕ)} (hD : IsDownSetFin D) {ρ : (Fin d → ℕ) → K}
    (hρ : DirConvex ρ) (hρ' : DirConvex (fun y => -ρ y)) :
    ∑ y ∈ D, (tileBeta D y : K) * ρ y = (D.card : K) * ρ 0 :=
  le_antisymm (rampLemma hD hρ) (rampLemma_concave hD hρ')

end RampTile

/-! ## The instance `ρ(y) = g(⟨y, q⟩)` with `g` convex and `q ≥ 0` -/

section Instance

variable {ι : Type*} [Fintype ι] [DecidableEq ι]
variable {K : Type*} [CommRing K] [LinearOrder K] [IsStrictOrderedRing K]

/-- For `g : ℕ → K` with nondecreasing increments, `g(n + k) - g(n)` is nondecreasing in `n`. -/
theorem incr_mono_of_convex {g : ℕ → K} (hg : ∀ n, g (n + 1) - g n ≤ g (n + 2) - g (n + 1))
    (n j k : ℕ) : g (n + k) - g n ≤ g (n + j + k) - g (n + j) := by
  have hmono : Monotone (fun i => g (i + 1) - g i) := by
    refine monotone_nat_of_le_succ fun i => ?_
    simpa [add_assoc] using hg i
  have h1 : ∀ t, g (t + k) - g t = ∑ i ∈ range k, (g (t + (i + 1)) - g (t + i)) := by
    intro t
    rw [Finset.sum_range_sub (fun i => g (t + i)) k]
    simp
  rw [h1 n, h1 (n + j)]
  refine Finset.sum_le_sum fun i _ => ?_
  have := hmono (show n + i ≤ n + j + i by omega)
  simpa [add_assoc] using this

/-- `ρ(y) = g(Σ_b q_b y_b)` is directionally convex when `q ≥ 0` (`q : ι → ℕ`) and `g : ℕ → K`
has nondecreasing increments (`g(n+1) - g(n) ≤ g(n+2) - g(n+1)`). -/
theorem dirConvex_comp_linear {g : ℕ → K} (hg : ∀ n, g (n + 1) - g n ≤ g (n + 2) - g (n + 1))
    (q : ι → ℕ) : DirConvex (fun y : ι → ℕ => g (∑ b, q b * y b)) := by
  have hlin : ∀ (u : ι → ℕ) (a : ι), ∑ b, q b * (u + Pi.single a 1 : ι → ℕ) b = ∑ b, q b * u b + q a := by
    intro u a
    simp only [Pi.add_apply, mul_add, Finset.sum_add_distrib]
    congr 1
    rw [Finset.sum_eq_single a]
    · simp
    · intro b _ hb; simp [Pi.single_eq_of_ne hb]
    · simp
  intro a b u
  simp only [hlin]
  exact incr_mono_of_convex hg (∑ c, q c * u c) (q b) (q a)

end Instance

end NumericalSemigroup
