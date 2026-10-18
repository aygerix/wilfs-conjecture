import Wilf.TileReduction

/-!
# `Tile-TOP'' ⇒ Wilf`

Formalization of the implication "Tile-TOP'' ⇒ Wilf" from `.research/PROOFS.md`. Tile-TOP'' itself
(`TileTOP`) is only *stated*; what is proved is `wilf_of_tileTOPAt` (per semigroup) and
`wilfConjecture_of_TileTOP : TileTOP → WilfConjecture`.

Notation (as in `Wilf.Carry` / `Wilf.TileReduction`): `m = S.multiplicity`, `d = |P'|`,
`D = S.factDownSet`, `w = S.wt`, `M = S.aperyMax m`, `p = S.genMod`, `φ = tilePhi p`, `s = M mod m`,
`⟨x⟩ = ZMod.val x ∈ [0, m)`. A cell `y ∈ D` is *maximal* if `y + e_a ∉ D` for every direction `a`.

Proof. By the column identity CH' (`columnIdentity`),
`Σ_a Σ_{a-tops x} (x_a + 1)(M - w(x)) = m·W + (d - 1)·m(m-1)/2`. Each term is bounded below:
* if `x` is not maximal, `x + e_b ∈ D` for some `b`, so `w(x) + p_b = w(x + e_b) ≤ M` and `p_b > m`,
  hence `M - w(x) ≥ m` (`multiplicity_le_aperyMax_sub_wt`);
* if `x` is maximal, `M - w(x) ≥ (M - w(x)) mod m = ⟨s - φ(x)⟩` (`val_le_aperyMax_sub_wt`).
Since the `a`-columns have total length `m` (`card_eq_sum_columns`) and a maximal cell is an
`a`-top for every `a`, this gives (`tileTop_column_bound`, summed over `a`)
`LHS(CH') ≥ d·m² - Σ_{x max} (d + |x|)·(m - ⟨s - φ(x)⟩)`. Tile-TOP'' at `s` bounds the subtracted
sum by `m·((d+1)·m + d - 1)/2`, and `2·d·m² - m·((d+1)·m + d - 1) = (d - 1)·m(m-1)`, so `m·W ≥ 0`.
-/

namespace NumericalSemigroup

open Finset

/-! ## Statements -/

/-- `y` is a maximal cell of `D` (it tops its column in every direction). -/
def IsMaxCell {d : ℕ} (D : Finset (Fin d → ℕ)) (y : Fin d → ℕ) : Prop :=
  ∀ a, y + Pi.single a 1 ∉ D

/-- **Tile-TOP''** for one tile: for every `s ∈ ℤ/m`,
`2·Σ_{y∈D maximal} (d + |y|)·(m − ⟨s − φ(y)⟩) ≤ m·((d+1)·m + d − 1)`, `|y| = Σ_a y_a`,
`⟨x⟩ = ZMod.val x`. (All quantities are natural numbers; for `m ≥ 1` neither subtraction truncates.) -/
def TileTOPAt {d m : ℕ} (D : Finset (Fin d → ℕ)) (p : Fin d → ZMod m) : Prop :=
  ∀ s : ZMod m, 2 * ∑ y ∈ D.filter (fun y => ∀ a, y + Pi.single a 1 ∉ D),
      (d + ∑ a, y a) * (m - (s - tilePhi p y).val) ≤ m * ((d + 1) * m + d - 1)

/-- **Conjecture Tile-TOP''**: every tile with `d ≥ 1` satisfies `TileTOPAt`. -/
def TileTOP : Prop :=
  ∀ (d m : ℕ) (D : Finset (Fin d → ℕ)) (p : Fin d → ZMod m), 1 ≤ d → IsTile D p → TileTOPAt D p

instance instDecidablePredIsMaxCell {d : ℕ} (D : Finset (Fin d → ℕ)) :
    DecidablePred (IsMaxCell D) :=
  fun y => inferInstanceAs (Decidable (∀ a, y + Pi.single a 1 ∉ D))

/-- The filter in `TileTOPAt` is the set of maximal cells. -/
theorem filter_isMaxCell {d : ℕ} (D : Finset (Fin d → ℕ)) :
    D.filter (fun y => ∀ a, y + Pi.single a 1 ∉ D) = D.filter (IsMaxCell D) := rfl

/-! ## The two lower bounds for `M - w(x)` -/

variable {S : NumericalSemigroup}

/-- If `x` is not a maximal cell of `D` then `M - w(x) ≥ m`: `x + e_b ∈ D` gives `w(x) + p_b ≤ M` and
`p_b > m`. -/
theorem multiplicity_le_aperyMax_sub_wt {x : Fin S.primitives'.card → ℕ}
    (hnot : ¬ ∀ b, x + Pi.single b 1 ∉ S.factDownSet) :
    (S.multiplicity : ℤ) ≤ (S.aperyMax S.multiplicity : ℤ) - S.wt x := by
  obtain ⟨b, hb⟩ := not_forall_not.1 hnot
  have h1 := wt_le_aperyMax hb
  rw [wt_add, wt_single, one_mul] at h1
  have h2 := multiplicity_lt_of_mem_primitives' (gen_mem (S := S) b)
  omega

/-- For `x ∈ D`: `⟨M - φ(x)⟩ = (M - w(x)) mod m ≤ M - w(x)`. -/
theorem val_le_aperyMax_sub_wt {x : Fin S.primitives'.card → ℕ} (hx : x ∈ S.factDownSet) :
    (((((S.aperyMax S.multiplicity : ℕ) : ZMod S.multiplicity) - tilePhi S.genMod x).val : ℕ) :
        ℤ) ≤ (S.aperyMax S.multiplicity : ℤ) - S.wt x := by
  rw [val_aperyMax_sub_tilePhi]
  have hM : (S.wt x : ℤ) ≤ S.aperyMax S.multiplicity := by exact_mod_cast wt_le_aperyMax hx
  exact emod_le_self_of_nonneg (by linarith) (by exact_mod_cast S.multiplicity_pos)

/-! ## The column bound and `Tile-TOP'' ⇒ Wilf` -/

/-- **Column bound in direction `a`**:
`m·m - Σ_{y∈D max} (y_a + 1)·(m - ⟨s - φ(y)⟩) ≤ Σ_{a-tops x} (x_a + 1)·(M - w(x))`, `s = M mod m`. -/
theorem tileTop_column_bound (a : Fin S.primitives'.card) :
    (S.multiplicity : ℤ) * S.multiplicity -
        ∑ y ∈ S.factDownSet.filter (fun y => ∀ b, y + Pi.single b 1 ∉ S.factDownSet),
          ((y a : ℤ) + 1) * ((S.multiplicity : ℤ) -
            ((((S.aperyMax S.multiplicity : ℕ) : ZMod S.multiplicity) -
              tilePhi S.genMod y).val : ℕ)) ≤
      ∑ x ∈ S.factDownSet.filter (fun x => x + Pi.single a 1 ∉ S.factDownSet),
        ((x a : ℤ) + 1) * ((S.aperyMax S.multiplicity : ℤ) - S.wt x) := by
  have hD := isDownSetFin_factDownSet (S := S)
  have h2 := card_eq_sum_columns hD a
  rw [card_factDownSet] at h2
  have hmm : (S.multiplicity : ℤ) * S.multiplicity =
      ∑ x ∈ S.factDownSet.filter (fun x => x + Pi.single a 1 ∉ S.factDownSet),
        ((x a : ℤ) + 1) * S.multiplicity := by
    have h2' : (S.multiplicity : ℤ) =
        ∑ x ∈ S.factDownSet.filter (fun x => x + Pi.single a 1 ∉ S.factDownSet),
          ((x a : ℤ) + 1) := by
      rw [h2]; push_cast; rfl
    rw [← Finset.sum_mul, ← h2']
  have hmax : S.factDownSet.filter (fun y => ∀ b, y + Pi.single b 1 ∉ S.factDownSet) =
      (S.factDownSet.filter (fun x => x + Pi.single a 1 ∉ S.factDownSet)).filter
        (fun y => ∀ b, y + Pi.single b 1 ∉ S.factDownSet) := by
    rw [Finset.filter_filter]
    exact Finset.filter_congr fun y _ => ⟨fun h => ⟨h a, h⟩, fun h => h.2⟩
  rw [hmax, Finset.sum_filter, hmm, ← Finset.sum_sub_distrib]
  refine Finset.sum_le_sum fun x hx => ?_
  have hxD := (Finset.mem_filter.1 hx).1
  have hpos : (0 : ℤ) ≤ (x a : ℤ) + 1 := by positivity
  split_ifs with hxmax
  · have := mul_le_mul_of_nonneg_left (val_le_aperyMax_sub_wt hxD) hpos
    linarith
  · have := mul_le_mul_of_nonneg_left (multiplicity_le_aperyMax_sub_wt hxmax) hpos
    linarith

/-- Summing the column bounds over the `d` directions: the subtracted sums add up to
`Σ_{y∈D max} (d + |y|)·(m - ⟨s - φ(y)⟩)` (the Tile-TOP'' sum, cast to `ℤ`). -/
theorem tileTop_sum_columns (s : ZMod S.multiplicity) :
    ∑ a : Fin S.primitives'.card,
        ∑ y ∈ S.factDownSet.filter (fun y => ∀ b, y + Pi.single b 1 ∉ S.factDownSet),
          ((y a : ℤ) + 1) * ((S.multiplicity : ℤ) - ((s - tilePhi S.genMod y).val : ℕ)) =
      ((∑ y ∈ S.factDownSet.filter (fun y => ∀ a, y + Pi.single a 1 ∉ S.factDownSet),
        (S.primitives'.card + ∑ a, y a) *
          (S.multiplicity - (s - tilePhi S.genMod y).val) : ℕ) : ℤ) := by
  have : NeZero S.multiplicity := ⟨S.multiplicity_pos.ne'⟩
  rw [Finset.sum_comm]
  push_cast
  refine Finset.sum_congr rfl fun y _ => ?_
  have hv : (s - tilePhi S.genMod y).val ≤ S.multiplicity := (ZMod.val_lt _).le
  rw [← Finset.sum_mul, Nat.cast_sub hv, Finset.sum_add_distrib]
  simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul, mul_one]
  ring

/-- **`Tile-TOP'' ⇒ Wilf`** for one numerical semigroup: if the tile `(D, p mod m)` of `S`
satisfies Tile-TOP'' (it is only used at `s = M mod m`), then `c(S) ≤ e(S)·ℓ(S)`.
(No hypothesis `S ≠ ℕ` is needed: for `S = ℕ` the argument goes through with `d = 0`.) -/
theorem wilf_of_tileTOPAt (h : TileTOPAt S.factDownSet S.genMod) :
    S.conductor ≤ S.embDim * S.ell := by
  have hm := S.multiplicity_pos
  have hmZ : (0 : ℤ) < S.multiplicity := by exact_mod_cast hm
  -- Tile-TOP'' at `s = M mod m`, cast to `ℤ`.
  have hTOP := h ((S.aperyMax S.multiplicity : ℕ) : ZMod S.multiplicity)
  have hTOPZ : (2 : ℤ) * ((∑ y ∈ S.factDownSet.filter
      (fun y => ∀ a, y + Pi.single a 1 ∉ S.factDownSet),
        (S.primitives'.card + ∑ a, y a) *
          (S.multiplicity - (((S.aperyMax S.multiplicity : ℕ) : ZMod S.multiplicity) -
            tilePhi S.genMod y).val) : ℕ) : ℤ) ≤
      (S.multiplicity : ℤ) * (((S.primitives'.card : ℤ) + 1) * S.multiplicity +
        S.primitives'.card - 1) := by
    have h1 : 1 ≤ (S.primitives'.card + 1) * S.multiplicity + S.primitives'.card := by
      nlinarith
    have := (Nat.cast_le (α := ℤ)).2 hTOP
    push_cast [Nat.cast_sub h1] at this ⊢
    linarith
  -- Lower bound for the left-hand side of CH'.
  have hlow := Finset.sum_le_sum fun a (_ : a ∈ (Finset.univ : Finset (Fin S.primitives'.card))) =>
    tileTop_column_bound (S := S) a
  rw [Finset.sum_sub_distrib, tileTop_sum_columns, Finset.sum_const, Finset.card_univ,
    Fintype.card_fin, nsmul_eq_mul] at hlow
  -- CH' and `2·(m(m-1)/2) = m(m-1)`.
  have hCH := columnIdentity (S := S)
  have hH : (((S.multiplicity * (S.multiplicity - 1) / 2 : ℕ) : ℤ)) * 2 =
      (S.multiplicity : ℤ) * ((S.multiplicity : ℤ) - 1) := by
    have h1 := Nat.div_two_mul_two_of_even (Nat.even_mul_pred_self S.multiplicity)
    have h2 : ((S.multiplicity * (S.multiplicity - 1) / 2 : ℕ) : ℤ) * 2 =
        ((S.multiplicity * (S.multiplicity - 1) : ℕ) : ℤ) := by exact_mod_cast h1
    rw [h2, Nat.cast_mul, Nat.cast_sub (show 1 ≤ S.multiplicity from hm), Nat.cast_one]
  have he : (S.embDim : ℤ) = S.primitives'.card + 1 := by
    exact_mod_cast (card_primitives'_add_one (S := S)).symm
  rw [he] at hCH
  have hkey : 2 * ((S.multiplicity : ℤ) * S.wilfDefect) =
      2 * ∑ a, ∑ x ∈ S.factDownSet.filter (fun x => x + Pi.single a 1 ∉ S.factDownSet),
        ((x a : ℤ) + 1) * ((S.aperyMax S.multiplicity : ℤ) - S.wt x) -
      ((S.primitives'.card : ℤ) - 1) * ((S.multiplicity : ℤ) * ((S.multiplicity : ℤ) - 1)) := by
    linear_combination (-2) * hCH - ((S.primitives'.card : ℤ) - 1) * hH
  have hW : 0 ≤ (S.multiplicity : ℤ) * S.wilfDefect := by linarith
  have hW' : 0 ≤ S.wilfDefect := nonneg_of_mul_nonneg_right hW hmZ
  rw [wilfDefect] at hW'
  have : (S.conductor : ℤ) ≤ S.embDim * S.ell := by linarith
  exact_mod_cast this

/-- **`Tile-TOP'' ⇒ Wilf`.** For `S ≠ ℕ`, `d = |P'| = e - 1 ≥ 1` and `(D, p mod m)` is a tile
(`isTile_factDownSet`), so Tile-TOP'' applies; `S = ℕ` is `wilf_nat`. -/
theorem wilfConjecture_of_TileTOP (h : TileTOP) : WilfConjecture := by
  intro S
  by_cases hS : S = nat
  · subst hS; exact wilf_nat
  · have hd : 1 ≤ S.primitives'.card := by
      have := card_primitives'_add_one (S := S)
      have := S.two_le_embDim hS
      omega
    exact wilf_of_tileTOPAt (h _ _ _ _ hd isTile_factDownSet)

end NumericalSemigroup
