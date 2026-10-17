import Wilf.Carry

/-!
# `Tile-CL ⇒ CL ⇒ Wilf`

Formalization of the remark "CL for `S` is Tile-CL for `(D, p mod m)` at `s = M mod m`" in
`.research/PROOFS.md` (section "Tile-CL").

For a numerical semigroup `S` with multiplicity `m`, `d = |P'|` (`P' = P ∖ {m}`), the factorization
down-set `D = S.factDownSet` and the residues `p_a = S.gen a mod m` (`S.genMod`):

* `isTile_factDownSet : IsTile S.factDownSet S.genMod` — `D` is a down-set with `|D| = m` and
  `φ(x) = Σ_a x_a p_a mod m` is a bijection `D → ℤ/m` (injective: distinct cells have distinct
  Apéry values, which are distinct mod `m`; surjective: every residue class has an Apéry element);
* `CL_sum_eq_tile_sum`: the double sum in `CL` (over directions `a` and `a`-tops `x`) equals
  `Σ_{y∈D} T(y)·⟨M - φ(y)⟩` (exchange of the order of summation and
  `(M - w(y)) mod m = ⟨M - φ(y)⟩`);
* `CL_iff_tileCLAt_aperyMax : S.CL ↔ (the Tile-CL inequality for (D, p) at s = M mod m)`, for every `S`;
* `CL_of_tileCLAt (hS : S ≠ nat) : TileCLAt S.factDownSet S.genMod → S.CL`;
* **`wilfConjecture_of_TileCL : TileCL → WilfConjecture`**.

`S = ℕ` (the only case with `d = 0`) is handled by `wilf_nat`; `TileCL` is only applied with `d ≥ 1`.
-/

namespace NumericalSemigroup

open Finset

/-- The residues `p_a mod m` of the generators `p_a ∈ P'`, `m = S.multiplicity`. -/
noncomputable def genMod (S : NumericalSemigroup) (a : Fin S.primitives'.card) :
    ZMod S.multiplicity :=
  (S.gen a : ZMod S.multiplicity)

variable {S : NumericalSemigroup}

/-- Elements of `Ap(S,n)` are determined by their residue mod `n`. -/
theorem IsApery.eq_of_mod_eq {n w₁ w₂ : ℕ} (hnS : n ∈ S) (hn : 0 < n)
    (h₁ : S.IsApery n w₁) (h₂ : S.IsApery n w₂) (h : w₁ % n = w₂ % n) : w₁ = w₂ := by
  rw [← apery_eq_self_of_isApery hnS hn h₁, ← apery_eq_self_of_isApery hnS hn h₂,
    ← S.apery_mod_self n w₁, h, S.apery_mod_self]

/-- `φ(x) = w(x) mod m`. -/
theorem tilePhi_genMod (x : Fin S.primitives'.card → ℕ) :
    tilePhi S.genMod x = ((S.wt x : ℕ) : ZMod S.multiplicity) := by
  simp [tilePhi, genMod, wt]

/-- **The factorization down-set is a tile**: `D` is a down-set, `|D| = m`, and
`φ(x) = Σ_a x_a p_a mod m` maps `D` bijectively onto `ℤ/m`. -/
theorem isTile_factDownSet : IsTile S.factDownSet S.genMod := by
  have hm := S.multiplicity_pos
  refine IsTile.mk' isDownSetFin_factDownSet card_factDownSet ?_ ?_
  · intro x hx y hy h
    rw [tilePhi_genMod, tilePhi_genMod, ZMod.natCast_eq_natCast_iff'] at h
    obtain ⟨hx1, hx2⟩ := isApery_wt_of_mem hx
    obtain ⟨hy1, hy2⟩ := isApery_wt_of_mem hy
    rw [← hx2, ← hy2, IsApery.eq_of_mod_eq S.multiplicity_mem hm hx1 hy1 h]
  · intro s
    have : NeZero S.multiplicity := ⟨hm.ne'⟩
    refine ⟨S.nf (S.apery S.multiplicity s.val),
      mem_factDownSet.2 ⟨_, isApery_apery hm _, rfl⟩, ?_⟩
    rw [tilePhi_genMod, wt_nf (isApery_apery hm _), ← ZMod.natCast_mod, S.apery_mod hm,
      ZMod.natCast_mod, ZMod.natCast_zmod_val]

/-- `⟨M - φ(y)⟩ = (M - w(y)) mod m` (as integers), with `⟨·⟩ = ZMod.val`. -/
theorem val_aperyMax_sub_tilePhi (y : Fin S.primitives'.card → ℕ) :
    ((((S.aperyMax S.multiplicity : ℕ) : ZMod S.multiplicity) - tilePhi S.genMod y).val : ℤ) =
      ((S.aperyMax S.multiplicity : ℤ) - S.wt y) % S.multiplicity := by
  have : NeZero S.multiplicity := ⟨S.multiplicity_pos.ne'⟩
  rw [tilePhi_genMod, ← ZMod.val_intCast]
  push_cast
  rfl

/-- **Exchange of summation**: the `CL` double sum (directions `a`, then `a`-tops `x` of `D`) is
`Σ_{y∈D} T(y)·⟨M - φ(y)⟩`, the Tile-CL sum for `(D, p mod m)` at `s = M mod m`. -/
theorem CL_sum_eq_tile_sum :
    ∑ a, ∑ x ∈ S.factDownSet.filter (fun x => x + Pi.single a 1 ∉ S.factDownSet),
        ((x a : ℤ) + 1) * (((S.aperyMax S.multiplicity : ℤ) - S.wt x) % S.multiplicity) =
      ((∑ y ∈ S.factDownSet, tileT S.factDownSet y *
        (((S.aperyMax S.multiplicity : ℕ) : ZMod S.multiplicity) - tilePhi S.genMod y).val : ℕ) :
          ℤ) := by
  push_cast
  simp_rw [val_aperyMax_sub_tilePhi, tileT, Finset.sum_filter]
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun y _ => ?_
  push_cast
  rw [Finset.sum_mul]
  refine Finset.sum_congr rfl fun a _ => ?_
  split_ifs <;> simp

/-- **CL is Tile-CL at `s = M mod m`** for the tile `(D, p mod m)` (every `S`, including `ℕ`). -/
theorem CL_iff_tileCLAt_aperyMax :
    S.CL ↔ (S.primitives'.card - 1) * (S.multiplicity * (S.multiplicity - 1) / 2) ≤
      ∑ y ∈ S.factDownSet, tileT S.factDownSet y *
        (((S.aperyMax S.multiplicity : ℕ) : ZMod S.multiplicity) - tilePhi S.genMod y).val := by
  rw [CL, CL_sum_eq_tile_sum]
  have hlhs : ((S.embDim : ℤ) - 1 - 1) * ((S.multiplicity * (S.multiplicity - 1) / 2 : ℕ) : ℤ) =
      (((S.primitives'.card - 1) * (S.multiplicity * (S.multiplicity - 1) / 2) : ℕ) : ℤ) := by
    have he := card_primitives'_add_one (S := S)
    rcases Nat.eq_zero_or_pos S.primitives'.card with hd | hd
    · -- `d = 0`: then `e = 1`, so `S = ℕ` and `m = 1`; both sides vanish.
      have hS : S = nat := by
        by_contra hS
        have := S.two_le_embDim hS
        omega
      have hm : S.multiplicity = 1 := S.multiplicity_eq_one_iff.2 hS
      simp [hm]
    · push_cast [Nat.cast_sub hd]
      rw [← he]
      push_cast
      ring
  rw [hlhs]
  exact Nat.cast_le

/-- Tile-CL for `(D, p mod m)` (at the single point `s = M mod m`) implies `CL`. -/
theorem CL_of_tileCLAt (h : TileCLAt S.factDownSet S.genMod) : S.CL :=
  CL_iff_tileCLAt_aperyMax.2 (h _)

/-- **`Tile-CL ⇒ Wilf`.** For `S ≠ ℕ`, `d = |P'| = e - 1 ≥ 1` and `(D, p mod m)` is a tile, so
Tile-CL gives `CL` and hence Wilf (`wilf_of_CL`); `S = ℕ` is `wilf_nat`. -/
theorem wilfConjecture_of_TileCL (h : TileCL) : WilfConjecture := by
  intro S
  by_cases hS : S = nat
  · subst hS; exact wilf_nat
  · have hd : 1 ≤ S.primitives'.card := by
      have := card_primitives'_add_one (S := S)
      have := S.two_le_embDim hS
      omega
    exact wilf_of_CL (CL_of_tileCLAt (h _ _ _ _ hd isTile_factDownSet))

end NumericalSemigroup
