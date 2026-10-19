import Wilf.MaxCL
import Wilf.ColumnTop

/-!
# MaxCL without wraps (phase-free NO-WRAP)

Let `(D, p)` be a tile and `P : Fin d → ℕ` a lift of `p` (`(P a : ZMod m) = p a`) such that the
integer weight `v(x) = Σ_a x_a·P_a` is `< m` on `D` ("no wrap"; then `v` is a bijection `D → [0, m)`).
Then MaxCL holds at every phase (`maxCLAt_of_noWrap`), and hence Wilf holds for every numerical
semigroup with a factorization tile on which `Σ_a x_a·(n_a mod m) < m` (`wilf_of_isFactTile_noWrap`).

Proof (any phase; `ρ = ⟨-σ⟩`, `r = (v + ρ) mod m = v + ρ - m·c`, `c = [m - ρ ≤ v]`; `T = tileT`,
`T(y) = d + |y|` on maximal cells, `A` maximal cells, `N` the others):
* (Gauss) `Σ_D T·v = (d + 1)·Σ_D v` (`sum_tileT_mul_linW`, from `sum_tops_mul_self/other`);
* `Σ_D T = d·m` (`card_eq_sum_columns`);
* (up-set count) `d·Σ_D c ≤ Σ_D T·c`: in each direction, a column meeting `{c = 1}` has its top
  there, since `v` is monotone (`card_filter_le_tops`);
* (window) `Σ_D c ≤ ρ`, since `v` is injective with values in `[m - ρ, m)` on `{c = 1}`;
* (nonmaximal tops) `m·T(y)·c(y) ≤ T(y)·(v(y) + ρ)`.
Then `(d+1)·Σ_D r - Σ_A T·r = Σ_N T(v + ρ) - m·Σ_N T·c + m·(Σ_D T·c - d·Σ_D c) + m·(ρ - Σ_D c) ≥ 0`.
-/

namespace NumericalSemigroup

open Finset

variable {d : ℕ} {D : Finset (Fin d → ℕ)}

/-- The integer weight `v(x) = Σ_a x_a·P_a`. -/
def linW (P : Fin d → ℕ) (x : Fin d → ℕ) : ℕ := ∑ a, x a * P a

theorem linW_mono (P : Fin d → ℕ) {x y : Fin d → ℕ} (h : x ≤ y) : linW P x ≤ linW P y :=
  Finset.sum_le_sum fun a _ => Nat.mul_le_mul_right _ (h a)

/-- `tileT`-weighted sums over `D` are sums over all columns, weighted by their lengths. -/
theorem sum_tileT_mul_nat (f : (Fin d → ℕ) → ℕ) :
    ∑ y ∈ D, tileT D y * f y =
      ∑ b, ∑ y ∈ D.filter (fun y => y + Pi.single b 1 ∉ D), (y b + 1) * f y := by
  simp only [tileT, Finset.sum_mul, Finset.sum_filter, ite_mul, zero_mul]
  rw [Finset.sum_comm]

/-- On a maximal cell, `T(y) = d + |y|`. -/
theorem tileT_of_isMaxCell {y : Fin d → ℕ} (hy : IsMaxCell D y) : tileT D y = d + ∑ a, y a := by
  have hf : Finset.univ.filter (fun a => y + Pi.single a 1 ∉ D) = Finset.univ :=
    Finset.filter_true_of_mem fun a _ => hy a
  rw [tileT, hf, Finset.sum_add_distrib, Finset.sum_const, Finset.card_univ, Fintype.card_fin,
    smul_eq_mul, mul_one, add_comm]

/-- **Gauss on columns.** `Σ_{y∈D} T(y)·v(y) = (d + 1)·Σ_{x∈D} v(x)`. -/
theorem sum_tileT_mul_linW (hD : IsDownSetFin D) (P : Fin d → ℕ) :
    ∑ y ∈ D, tileT D y * linW P y = (d + 1) * ∑ x ∈ D, linW P x := by
  rw [sum_tileT_mul_nat]
  have h : ∀ b, ∑ y ∈ D.filter (fun y => y + Pi.single b 1 ∉ D), (y b + 1) * linW P y =
      ∑ a, P a * ((1 + if b = a then 1 else 0) * ∑ x ∈ D, x a) := by
    intro b
    simp only [linW, Finset.mul_sum]
    rw [Finset.sum_comm]
    refine Finset.sum_congr rfl fun a _ => ?_
    have e1 : ∑ y ∈ D.filter (fun y => y + Pi.single b 1 ∉ D), (y b + 1) * (y a * P a) =
        P a * ∑ y ∈ D.filter (fun y => y + Pi.single b 1 ∉ D), (y b + 1) * y a := by
      rw [Finset.mul_sum]
      exact Finset.sum_congr rfl fun y _ => by ring
    rw [e1, ← Finset.mul_sum]
    congr 1
    split_ifs with hba
    · subst hba
      rw [sum_tops_mul_self hD b, Finset.mul_sum]
    · rw [sum_tops_mul_other hD hba]
      simp
  rw [Finset.sum_congr rfl fun b _ => h b, Finset.sum_comm]
  have h2 : ∀ a : Fin d, ∑ b : Fin d, P a * ((1 + if b = a then 1 else 0) * ∑ x ∈ D, x a) =
      (d + 1) * ∑ x ∈ D, x a * P a := by
    intro a
    rw [← Finset.mul_sum, ← Finset.sum_mul, Finset.sum_add_distrib, Finset.sum_const,
      Finset.card_univ, Fintype.card_fin, smul_eq_mul, mul_one,
      Finset.sum_ite_eq' Finset.univ a (fun _ => 1), if_pos (Finset.mem_univ a)]
    simp only [Finset.mul_sum]
    exact Finset.sum_congr rfl fun x _ => by ring
  rw [Finset.sum_congr rfl fun a _ => h2 a, ← Finset.mul_sum]
  congr 1
  simp only [linW]
  exact Finset.sum_comm

/-- `Σ_{y∈D} T(y) = d·|D|`. -/
theorem sum_tileT (hD : IsDownSetFin D) : ∑ y ∈ D, tileT D y = d * D.card := by
  have h := sum_tileT_mul_nat (D := D) (fun _ => 1)
  simp only [mul_one] at h
  rw [h]
  have : ∀ b : Fin d, ∑ y ∈ D.filter (fun y => y + Pi.single b 1 ∉ D), (y b + 1) = D.card :=
    fun b => (card_eq_sum_columns hD b).symm
  rw [Finset.sum_congr rfl fun b _ => this b, Finset.sum_const, Finset.card_univ,
    Fintype.card_fin, smul_eq_mul]

/-- **Up-set count.** In one direction `b`: `#{x ∈ D : T₀ ≤ v(x)} ≤ Σ_{b-tops y} (y_b + 1)·[T₀ ≤ v(y)]`. -/
theorem card_filter_le_tops (hD : IsDownSetFin D) (P : Fin d → ℕ) (T₀ : ℕ) (b : Fin d) :
    (D.filter (fun x => T₀ ≤ linW P x)).card ≤
      ∑ y ∈ D.filter (fun y => y + Pi.single b 1 ∉ D),
        (y b + 1) * (if T₀ ≤ linW P y then 1 else 0) := by
  rw [Finset.card_filter, sum_columns hD b]
  refine Finset.sum_le_sum fun y _ => ?_
  calc ∑ k ∈ range (y b + 1), (if T₀ ≤ linW P (y - Pi.single b k) then 1 else 0)
      ≤ ∑ _k ∈ range (y b + 1), (if T₀ ≤ linW P y then 1 else 0) := by
        refine Finset.sum_le_sum fun k _ => ?_
        have hle : linW P (y - Pi.single b k) ≤ linW P y :=
          linW_mono P (fun a => Nat.sub_le _ _)
        split_ifs with h1 h2 <;> omega
    _ = (y b + 1) * (if T₀ ≤ linW P y then 1 else 0) := by
        rw [Finset.sum_const, card_range, smul_eq_mul]

/-- Summed over directions: `d·#{x ∈ D : T₀ ≤ v(x)} ≤ Σ_{y∈D} T(y)·[T₀ ≤ v(y)]`. -/
theorem mul_card_filter_le_sum_tileT (hD : IsDownSetFin D) (P : Fin d → ℕ) (T₀ : ℕ) :
    d * (D.filter (fun x => T₀ ≤ linW P x)).card ≤
      ∑ y ∈ D, tileT D y * (if T₀ ≤ linW P y then 1 else 0) := by
  rw [sum_tileT_mul_nat]
  calc d * (D.filter (fun x => T₀ ≤ linW P x)).card
      = ∑ _b : Fin d, (D.filter (fun x => T₀ ≤ linW P x)).card := by
        rw [Finset.sum_const, Finset.card_univ, Fintype.card_fin, smul_eq_mul]
    _ ≤ _ := Finset.sum_le_sum fun b _ => card_filter_le_tops hD P T₀ b

/-- **Window count.** If `v` is injective on `D` with values `< m`, then at most `ρ` cells have
`v ≥ m - ρ`. -/
theorem card_window_le {m : ℕ} (P : Fin d → ℕ) (hlt : ∀ x ∈ D, linW P x < m)
    (hinj : Set.InjOn (linW P) (D : Set (Fin d → ℕ))) (ρ : ℕ) (hρ : ρ ≤ m) :
    (D.filter (fun x => m - ρ ≤ linW P x)).card ≤ ρ := by
  have h := Finset.card_le_card_of_injOn (linW P)
    (s := D.filter (fun x => m - ρ ≤ linW P x)) (t := Finset.Ico (m - ρ) m)
    (fun x hx => by
      have hx' := Finset.mem_filter.1 hx
      exact Finset.mem_Ico.2 ⟨hx'.2, hlt x hx'.1⟩)
    (fun x hx y hy hxy => hinj (Finset.mem_filter.1 hx).1 (Finset.mem_filter.1 hy).1 hxy)
  simpa [Nat.card_Ico, Nat.sub_sub_self hρ] using h

/-- `r = (v + ρ) mod m` equals `v + ρ - m·c` with `c = [m - ρ ≤ v]` (no wrap: `v < m`, `ρ < m`). -/
theorem mod_add_mul_ind {m v ρ : ℕ} (hv : v < m) (hρ : ρ < m) :
    (v + ρ) % m + m * (if m - ρ ≤ v then 1 else 0) = v + ρ := by
  split_ifs with h
  · have h1 : m ≤ v + ρ := by omega
    have h2 : v + ρ - m < m := by omega
    have : (v + ρ) % m = v + ρ - m := by
      rw [Nat.mod_eq_sub_mod h1, Nat.mod_eq_of_lt h2]
    omega
  · rw [Nat.mod_eq_of_lt (by omega)]
    omega

/-- **NO-WRAP MaxCL, integer form.** For a finite down-set `D` with `|D| = m` and a weight `v`
injective on `D` with values `< m`: for every `ρ < m`,
`Σ_{y max} (d + |y|)·((v(y) + ρ) mod m) ≤ (d + 1)·Σ_{x∈D} ((v(x) + ρ) mod m)`. -/
theorem maxCL_noWrap_aux (hD : IsDownSetFin D) {m : ℕ} (hcard : D.card = m) (P : Fin d → ℕ)
    (hlt : ∀ x ∈ D, linW P x < m) (hinj : Set.InjOn (linW P) (D : Set (Fin d → ℕ)))
    (ρ : ℕ) (hρ : ρ < m) :
    ∑ y ∈ D.filter (IsMaxCell D), (d + ∑ a, y a) * ((linW P y + ρ) % m) ≤
      (d + 1) * ∑ x ∈ D, (linW P x + ρ) % m := by
  classical
  set c : (Fin d → ℕ) → ℕ := fun x => if m - ρ ≤ linW P x then 1 else 0 with hc
  set A := D.filter (IsMaxCell D) with hA
  set N := D.filter (fun y => ¬ IsMaxCell D y) with hN
  -- the split of `T`-weighted sums into maximal and non-maximal cells
  have split : ∀ f : (Fin d → ℕ) → ℕ, ∑ y ∈ D, tileT D y * f y =
      ∑ y ∈ A, (d + ∑ a, y a) * f y + ∑ y ∈ N, tileT D y * f y := by
    intro f
    rw [← Finset.sum_filter_add_sum_filter_not D (IsMaxCell D)]
    congr 1
    exact Finset.sum_congr rfl fun y hy => by
      rw [tileT_of_isMaxCell (Finset.mem_filter.1 hy).2]
  -- facts (a)–(g)
  have ha : ∑ y ∈ A, (d + ∑ a, y a) * ((linW P y + ρ) % m) + m * ∑ y ∈ A, (d + ∑ a, y a) * c y =
      ∑ y ∈ A, (d + ∑ a, y a) * linW P y + ρ * ∑ y ∈ A, (d + ∑ a, y a) := by
    rw [Finset.mul_sum, Finset.mul_sum, ← Finset.sum_add_distrib, ← Finset.sum_add_distrib]
    refine Finset.sum_congr rfl fun y hy => ?_
    have := mod_add_mul_ind (hlt y (Finset.mem_filter.1 hy).1) hρ
    calc (d + ∑ a, y a) * ((linW P y + ρ) % m) + m * ((d + ∑ a, y a) * c y)
        = (d + ∑ a, y a) * ((linW P y + ρ) % m + m * c y) := by ring
      _ = (d + ∑ a, y a) * (linW P y + ρ) := by rw [this]
      _ = (d + ∑ a, y a) * linW P y + ρ * (d + ∑ a, y a) := by ring
  have hb : ∑ x ∈ D, (linW P x + ρ) % m + m * ∑ x ∈ D, c x = ∑ x ∈ D, linW P x + ρ * m := by
    rw [Finset.mul_sum, ← Finset.sum_add_distrib]
    rw [show ρ * m = ∑ _x ∈ D, ρ by rw [Finset.sum_const, hcard, smul_eq_mul, mul_comm],
      ← Finset.sum_add_distrib]
    exact Finset.sum_congr rfl fun x hx => mod_add_mul_ind (hlt x hx) hρ
  have hgauss := sum_tileT_mul_linW hD P
  rw [split] at hgauss
  have hT1 := sum_tileT hD (D := D)
  have hT1' : ∑ y ∈ D, tileT D y * 1 = d * m := by simp only [mul_one]; rw [hT1, hcard]
  rw [split] at hT1'
  simp only [mul_one] at hT1'
  have hcard_c : (D.filter (fun x => m - ρ ≤ linW P x)).card = ∑ x ∈ D, c x := by
    rw [Finset.card_filter]
  have he : d * ∑ x ∈ D, c x ≤ ∑ y ∈ D, tileT D y * c y := by
    have := mul_card_filter_le_sum_tileT hD P (m - ρ)
    rw [hcard_c] at this
    exact this
  rw [split] at he
  have hf : ∑ x ∈ D, c x ≤ ρ := by
    rw [← hcard_c]; exact card_window_le P hlt hinj ρ hρ.le
  have hg : m * ∑ y ∈ N, tileT D y * c y ≤
      ∑ y ∈ N, tileT D y * linW P y + ρ * ∑ y ∈ N, tileT D y := by
    rw [Finset.mul_sum, Finset.mul_sum, ← Finset.sum_add_distrib]
    refine Finset.sum_le_sum fun y hy => ?_
    have hv := hlt y (Finset.mem_filter.1 hy).1
    by_cases h : m - ρ ≤ linW P y
    · have : c y = 1 := by simp only [hc, if_pos h]
      rw [this]
      have : m ≤ linW P y + ρ := by omega
      nlinarith
    · have : c y = 0 := by simp only [hc, if_neg h]
      rw [this]; simp
  -- name the sums, then combine over ℤ
  generalize ∑ y ∈ A, (d + ∑ a, y a) * ((linW P y + ρ) % m) = SAr at ha ⊢
  generalize ∑ y ∈ A, (d + ∑ a, y a) * c y = SAc at ha he
  generalize ∑ y ∈ A, (d + ∑ a, y a) * linW P y = SAv at ha hgauss
  generalize ∑ y ∈ A, (d + ∑ a, y a) = SA1 at ha hT1'
  generalize ∑ x ∈ D, (linW P x + ρ) % m = Xr at hb ⊢
  generalize ∑ x ∈ D, c x = Xc at hb he hf
  generalize ∑ x ∈ D, linW P x = Xv at hb hgauss
  generalize ∑ y ∈ N, tileT D y * linW P y = SNv at hgauss hg
  generalize ∑ y ∈ N, tileT D y = SN1 at hT1' hg
  generalize ∑ y ∈ N, tileT D y * c y = SNc at he hg
  have hm0 : (0 : ℤ) ≤ m := by positivity
  zify at ha hb hgauss hT1' he hf hg ⊢
  have key : ((d : ℤ) + 1) * Xr - SAr =
      (SNv + ρ * SN1 - m * SNc) + m * (SAc + SNc - d * Xc) + m * (ρ - Xc) := by
    linear_combination ((d : ℤ) + 1) * hb - ha - hgauss - (ρ : ℤ) * hT1'
  nlinarith [mul_nonneg hm0 (sub_nonneg.2 he), mul_nonneg hm0 (sub_nonneg.2 hf)]

/-- **NO-WRAP MaxCL.** If a tile `(D, p)` has a lift `P` (`(P a : ZMod m) = p a`) with
`Σ_a x_a·P_a < m` on `D`, then MaxCL holds at every phase. -/
theorem maxCLAt_of_noWrap {m : ℕ} {p : Fin d → ZMod m} (hT : IsTile D p) (P : Fin d → ℕ)
    (hP : ∀ a, (P a : ZMod m) = p a) (hlt : ∀ x ∈ D, linW P x < m) : MaxCLAt D p := by
  have hm := hT.pos
  have : NeZero m := ⟨hm.ne'⟩
  have hphi : ∀ x, tilePhi p x = ((linW P x : ℕ) : ZMod m) := by
    intro x
    simp only [tilePhi, linW, Nat.cast_sum, Nat.cast_mul, hP]
  have hinj : Set.InjOn (linW P) (D : Set (Fin d → ℕ)) := by
    intro x hx y hy h
    exact hT.2.2.injOn hx hy (by rw [hphi, hphi, h])
  intro σ
  have hval : ∀ x, (tilePhi p x - σ).val = (linW P x + (-σ).val) % m := by
    intro x
    rw [hphi, sub_eq_add_neg, ← ZMod.natCast_zmod_val (-σ), ← Nat.cast_add, ZMod.val_natCast,
      ZMod.natCast_zmod_val]
  simp_rw [hval]
  exact maxCL_noWrap_aux hT.1 hT.2.1 P hlt hinj _ (ZMod.val_lt _)

/-- **Wilf without wraps.** If a numerical semigroup `S` has a factorization tile `D` on which
`Σ_a x_a·(n_a mod m) < m` for every `x ∈ D` (`n_a` the minimal generators other than `m`), then
`c(S) ≤ e(S)·ℓ(S)`. -/
theorem wilf_of_isFactTile_noWrap {S : NumericalSemigroup}
    {D : Finset (Fin S.primitives'.card → ℕ)} (hD : IsFactTile S D)
    (hw : ∀ x ∈ D, ∑ a, x a * (S.gen a % S.multiplicity) < S.multiplicity) :
    S.conductor ≤ S.embDim * S.ell := by
  by_cases hS : S = nat
  · subst hS; exact wilf_nat
  · have hd : 1 ≤ S.primitives'.card := by
      have := card_primitives'_add_one (S := S)
      have := S.two_le_embDim hS
      omega
    refine wilf_of_tileTOPAt_of_isFactTile hD (tileTOPAt_of_maxCLAt hd hD.isTile ?_)
    refine maxCLAt_of_noWrap hD.isTile (fun a => S.gen a % S.multiplicity) (fun a => ?_) hw
    rw [genMod, ZMod.natCast_mod]

end NumericalSemigroup
