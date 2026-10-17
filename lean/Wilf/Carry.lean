import Wilf.Chains
import Mathlib.Algebra.Order.Group.PiLex
import Mathlib.Data.Fintype.Pi
import Mathlib.Data.Finset.Sort
import Mathlib.Data.ZMod.Basic

/-!
# Factorization down-set `D`, column identity CH', Carry Lemma CL, and `CL ⇒ Wilf`

Formalization of `.research/PROOFS.md`, sections "Factorization down-set D and the column identity
CH'" and "Conjecture CL" (2026-10-17).

* `P' = P ∖ {m}` is indexed by `Fin d`, `d = |P'| = e - 1`, increasingly: `S.gen : Fin d → ℕ`
  (`Finset.orderEmbOfFin`).
* `S.wt x = Σ_a x_a · p_a` for `x : Fin d → ℕ`.
* **Monomial order used:** the lexicographic order `toLex` on `Fin d → ℕ` (coordinate `0`, i.e.
  the smallest generator of `P'`, is the most significant). `S.nf w` is the lex-least factorization
  of `w` over `P'`; it exists for Apéry elements.
* `S.factDownSet = {S.nf w | w ∈ Ap(S,m)}` is the down-set `D`.
* Column identity CH' (`columnIdentity`), CL (`CL`) and `wilf_of_CL : S.CL → c ≤ e·ℓ`.
* Tile-CL (`TileCL`) is only *stated*, with `decide`-checked sanity examples.

Columns: for a down-set `D` and direction `a`, the `a`-tops are the `y ∈ D` with `y + e_a ∉ D`; the
column with top `y` is `{y - k·e_a | k ≤ y_a}` (`sum_columns`).
-/

namespace NumericalSemigroup

open Finset

/-! ## Finite down-sets in `ι → ℕ` and their columns -/

section DownSet

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- `D` is a down-set of `ι → ℕ` for the componentwise order. -/
def IsDownSetFin (D : Finset (ι → ℕ)) : Prop := ∀ x ∈ D, ∀ y, y ≤ x → y ∈ D

/-- Height of `x` in its `a`-column of `D`: `max {k | x + k·e_a ∈ D}`. -/
noncomputable def colHt (D : Finset (ι → ℕ)) (a : ι) (x : ι → ℕ) : ℕ :=
  sSup {k | x + Pi.single a k ∈ D}

variable {D : Finset (ι → ℕ)} {a : ι}

omit [Fintype ι] in
theorem colHt_bdd (D : Finset (ι → ℕ)) (a : ι) (x : ι → ℕ) :
    BddAbove {k | x + Pi.single a k ∈ D} :=
  ⟨D.sup (fun z => z a), fun k hk => by
    have := Finset.le_sup (f := fun z => z a) (show x + Pi.single a k ∈ D from hk)
    simp only [Pi.add_apply, Pi.single_eq_same] at this
    omega⟩

omit [Fintype ι] in
theorem colHt_spec {x : ι → ℕ} (hx : x ∈ D) : x + Pi.single a (colHt D a x) ∈ D :=
  Nat.sSup_mem ⟨0, by simpa using hx⟩ (colHt_bdd D a x)

omit [Fintype ι] in
theorem le_colHt {x : ι → ℕ} {k : ℕ} (h : x + Pi.single a k ∈ D) : k ≤ colHt D a x :=
  le_csSup (colHt_bdd D a x) h

omit [Fintype ι] in
theorem mem_of_le_colHt (hD : IsDownSetFin D) {x : ι → ℕ} {k : ℕ} (hx : x ∈ D)
    (hk : k ≤ colHt D a x) : x + Pi.single a k ∈ D := by
  refine hD _ (colHt_spec (a := a) hx) _ fun b => ?_
  by_cases hb : b = a
  · subst hb; simp only [Pi.add_apply, Pi.single_eq_same]; omega
  · simp [Pi.single_eq_of_ne hb]

omit [Fintype ι] in
theorem sub_single_add_single {y : ι → ℕ} {k : ℕ} (hk : k ≤ y a) :
    y - Pi.single a k + Pi.single a k = y := by
  funext b
  by_cases hb : b = a
  · subst hb; simp only [Pi.add_apply, Pi.sub_apply, Pi.single_eq_same]; omega
  · simp [Pi.single_eq_of_ne hb]

/-- **Column decomposition.** For a finite down-set `D` and a direction `a`, summing over `D` is
summing over the `a`-tops `y` (`y ∈ D`, `y + e_a ∉ D`) and then down their columns
`{y - k·e_a | k ≤ y_a}`. -/
theorem sum_columns {β : Type*} [AddCommMonoid β] (hD : IsDownSetFin D) (a : ι)
    (F : (ι → ℕ) → β) :
    ∑ x ∈ D, F x = ∑ y ∈ D.filter (fun y => y + Pi.single a 1 ∉ D),
      ∑ k ∈ range (y a + 1), F (y - Pi.single a k) := by
  let top : (ι → ℕ) → (ι → ℕ) := fun x => x + Pi.single a (colHt D a x)
  have htop : ∀ x ∈ D, top x ∈ D.filter (fun y => y + Pi.single a 1 ∉ D) := by
    intro x hx
    refine Finset.mem_filter.2 ⟨colHt_spec hx, fun h => ?_⟩
    have h' : x + Pi.single a (colHt D a x + 1) ∈ D := by
      rw [Pi.single_add, ← add_assoc]; exact h
    have := le_colHt h'
    omega
  rw [← Finset.sum_fiberwise_of_maps_to htop F]
  refine Finset.sum_congr rfl fun y hy => ?_
  have hyD := Finset.mem_filter.1 hy
  have hfib : D.filter (fun x => top x = y) =
      (range (y a + 1)).image (fun k => y - Pi.single a k) := by
    ext x
    simp only [Finset.mem_filter, Finset.mem_image, Finset.mem_range]
    constructor
    · rintro ⟨hx, hxy⟩
      refine ⟨colHt D a x, ?_, ?_⟩
      · have := congrFun hxy a
        simp only [top, Pi.add_apply, Pi.single_eq_same] at this
        omega
      · rw [← hxy]
        funext b
        by_cases hb : b = a
        · subst hb; simp [top]
        · simp [top, Pi.single_eq_of_ne hb]
    · rintro ⟨k, hk, rfl⟩
      have hk' : k ≤ y a := by omega
      have hxD : y - Pi.single a k ∈ D := hD _ hyD.1 _ (fun b => Nat.sub_le _ _)
      refine ⟨hxD, ?_⟩
      have hadd := sub_single_add_single (a := a) hk'
      have h1 : k ≤ colHt D a (y - Pi.single a k) := le_colHt (by rw [hadd]; exact hyD.1)
      have h2 : colHt D a (y - Pi.single a k) ≤ k := by
        by_contra hlt
        push Not at hlt
        have := mem_of_le_colHt hD hxD (show k + 1 ≤ _ from hlt)
        rw [Pi.single_add, ← add_assoc, hadd] at this
        exact hyD.2 this
      show y - Pi.single a k + Pi.single a (colHt D a (y - Pi.single a k)) = y
      rw [le_antisymm h2 h1, hadd]
  rw [hfib, Finset.sum_image]
  intro k1 hk1 k2 hk2 h
  have hk1' := Finset.mem_range.1 (Finset.mem_coe.1 hk1)
  have hk2' := Finset.mem_range.1 (Finset.mem_coe.1 hk2)
  have := congrFun h a
  simp only [Pi.sub_apply, Pi.single_eq_same] at this
  omega

/-- The columns in direction `a` have total length `|D|`. -/
theorem card_eq_sum_columns (hD : IsDownSetFin D) (a : ι) :
    D.card = ∑ y ∈ D.filter (fun y => y + Pi.single a 1 ∉ D), (y a + 1) := by
  rw [Finset.card_eq_sum_ones, sum_columns hD a (fun _ => 1)]
  simp

/-- **Column sum of an arithmetic progression.** For weights `p : ι → ℕ` and `w(x) = Σ_b x_b p_b`:
`Σ_{x∈D} (w(x) + p_a·x_a) = Σ_{a-tops y} (y_a + 1)·w(y)` (in `ℤ`). -/
theorem sum_wt_add_eq_columns (hD : IsDownSetFin D) (a : ι) (p : ι → ℕ) :
    ∑ x ∈ D, ((∑ b, (x b : ℤ) * p b) + (p a : ℤ) * x a) =
      ∑ y ∈ D.filter (fun y => y + Pi.single a 1 ∉ D),
        ((y a : ℤ) + 1) * ∑ b, (y b : ℤ) * p b := by
  rw [sum_columns hD a]
  refine Finset.sum_congr rfl fun y _ => ?_
  have hterm : ∀ k ∈ range (y a + 1),
      (∑ b, (((y - Pi.single a k : ι → ℕ) b : ℕ) : ℤ) * p b) +
          (p a : ℤ) * ((y - Pi.single a k : ι → ℕ) a : ℕ) =
        (∑ b, (y b : ℤ) * p b) + (p a : ℤ) * y a - 2 * (p a : ℤ) * k := by
    intro k hk
    have hk' : k ≤ y a := by have := Finset.mem_range.1 hk; omega
    have hcoord : ∀ b, (((y - Pi.single a k : ι → ℕ) b : ℕ) : ℤ) =
        (y b : ℤ) - ((Pi.single a k : ι → ℕ) b : ℕ) := by
      intro b
      by_cases hb : b = a
      · subst hb; simp only [Pi.sub_apply, Pi.single_eq_same]; push_cast [Nat.cast_sub hk']; ring
      · simp [Pi.single_eq_of_ne hb]
    simp_rw [hcoord, sub_mul, Finset.sum_sub_distrib]
    have hsingle : ∑ b, (((Pi.single a k : ι → ℕ) b : ℕ) : ℤ) * p b = (k : ℤ) * p a := by
      rw [Finset.sum_eq_single a]
      · simp
      · intro b _ hb; simp [Pi.single_eq_of_ne hb]
      · simp
    rw [hsingle]
    simp only [Pi.single_eq_same]
    ring
  rw [Finset.sum_congr rfl hterm, Finset.sum_sub_distrib, Finset.sum_const, Finset.card_range,
    ← Finset.mul_sum]
  have hs := Finset.sum_range_id_mul_two (y a + 1)
  have hs' : (∑ i ∈ range (y a + 1), (i : ℤ)) * 2 = ((y a : ℤ) + 1) * y a := by
    have := congrArg (fun x : ℕ => (x : ℤ)) hs
    push_cast at this
    rw [this]
  rw [nsmul_eq_mul]
  push_cast
  linear_combination (-(p a : ℤ)) * hs'

end DownSet

/-! ## The factorization down-set of a numerical semigroup -/

variable (S : NumericalSemigroup)

/-- `p_a` (`a : Fin d`, `d = |P'|`): the elements of `P' = P ∖ {m}` in increasing order. -/
noncomputable def gen (a : Fin S.primitives'.card) : ℕ := S.primitives'.orderEmbOfFin rfl a

/-- `w(x) = Σ_a x_a · p_a`. -/
noncomputable def wt (x : Fin S.primitives'.card → ℕ) : ℕ := ∑ a, x a * S.gen a

/-- Factorizations of `w` over `P'` (they are automatically bounded by `w` coordinatewise). -/
noncomputable def factSet (w : ℕ) : Finset (Fin S.primitives'.card → ℕ) :=
  (Fintype.piFinset fun _ => range (w + 1)).filter (fun x => S.wt x = w)

open Classical in
/-- `n(w)`: the lex-least factorization of `w` over `P'` (junk `0` if there is none). -/
noncomputable def nf (w : ℕ) : Fin S.primitives'.card → ℕ :=
  if h : (S.factSet w).Nonempty then ofLex (((S.factSet w).image toLex).min' (h.image toLex))
  else 0

/-- The factorization down-set `D = {n(w) | w ∈ Ap(S,m)}`. -/
noncomputable def factDownSet : Finset (Fin S.primitives'.card → ℕ) :=
  (S.aperySet S.multiplicity).image S.nf

variable {S}

theorem gen_mem (a : Fin S.primitives'.card) : S.gen a ∈ S.primitives' :=
  Finset.orderEmbOfFin_mem _ _ a

theorem exists_gen_eq {p : ℕ} (hp : p ∈ S.primitives') : ∃ a, S.gen a = p := by
  have : p ∈ Set.range (S.primitives'.orderEmbOfFin rfl) := by
    rw [Finset.range_orderEmbOfFin]; exact hp
  obtain ⟨a, ha⟩ := this
  exact ⟨a, ha⟩

theorem gen_pos (a : Fin S.primitives'.card) : 0 < S.gen a := pos_of_mem_primitives' (gen_mem a)

theorem wt_add (x y : Fin S.primitives'.card → ℕ) : S.wt (x + y) = S.wt x + S.wt y := by
  simp only [wt, Pi.add_apply, add_mul, Finset.sum_add_distrib]

theorem wt_single (a : Fin S.primitives'.card) (k : ℕ) : S.wt (Pi.single a k) = k * S.gen a := by
  rw [wt, Finset.sum_eq_single a]
  · simp
  · intro b _ hb; simp [Pi.single_eq_of_ne hb]
  · simp

theorem wt_mem (x : Fin S.primitives'.card → ℕ) : S.wt x ∈ S :=
  sum_mem fun a _ => mul_mem (mem_of_mem_primitives' (gen_mem a)) (x a)

theorem wt_cast (x : Fin S.primitives'.card → ℕ) :
    (S.wt x : ℤ) = ∑ a, (x a : ℤ) * S.gen a := by
  simp [wt]

/-- Fact (iv) with `P'` indexed by `Fin d`. -/
theorem exists_wt_eq {w : ℕ} (hw : S.IsApery S.multiplicity w) :
    ∃ x : Fin S.primitives'.card → ℕ, S.wt x = w := by
  induction w using Nat.strong_induction_on with
  | _ w ih =>
    rcases Nat.eq_zero_or_pos w with rfl | hpos
    · exact ⟨0, by simp [wt]⟩
    by_cases hprim : S.IsPrimitive w
    · have hne : w ≠ S.multiplicity := by
        rintro rfl
        exact hw.2 le_rfl (by simp)
      have hmem : w ∈ S.primitives' := Finset.mem_erase.2 ⟨hne, S.mem_primitives.2 hprim⟩
      obtain ⟨a, ha⟩ := exists_gen_eq hmem
      exact ⟨Pi.single a 1, by rw [wt_single, one_mul, ha]⟩
    · obtain ⟨a, ha, b, hb, a0, b0, rfl⟩ := S.exists_decomp_of_not_isPrimitive hw.1 hpos hprim
      obtain ⟨x, hx⟩ := ih a (by omega) (hw.of_add ha hb rfl)
      obtain ⟨y, hy⟩ := ih b (by omega) (hw.of_add hb ha (add_comm b a))
      exact ⟨x + y, by rw [wt_add, hx, hy]⟩

theorem mem_factSet {w : ℕ} {x : Fin S.primitives'.card → ℕ} : x ∈ S.factSet w ↔ S.wt x = w := by
  rw [factSet, Finset.mem_filter, Fintype.mem_piFinset]
  refine ⟨fun h => h.2, fun h => ⟨fun a => ?_, h⟩⟩
  rw [Finset.mem_range]
  have h1 : x a * S.gen a ≤ S.wt x :=
    Finset.single_le_sum (f := fun b => x b * S.gen b) (fun _ _ => Nat.zero_le _) (Finset.mem_univ a)
  have h2 : x a ≤ x a * S.gen a := Nat.le_mul_of_pos_right _ (gen_pos a)
  omega

theorem nf_spec {w : ℕ} (hw : S.IsApery S.multiplicity w) :
    S.wt (S.nf w) = w ∧ ∀ x, S.wt x = w → toLex (S.nf w) ≤ toLex x := by
  classical
  have hne : (S.factSet w).Nonempty := by
    obtain ⟨x, hx⟩ := exists_wt_eq hw
    exact ⟨x, mem_factSet.2 hx⟩
  unfold nf
  rw [dif_pos hne]
  constructor
  · obtain ⟨x, hx, hx'⟩ := Finset.mem_image.1 (Finset.min'_mem _ (hne.image toLex))
    rw [← hx']
    exact mem_factSet.1 hx
  · intro x hx
    rw [toLex_ofLex]
    exact Finset.min'_le _ _ (Finset.mem_image_of_mem _ (mem_factSet.2 hx))

theorem wt_nf {w : ℕ} (hw : S.IsApery S.multiplicity w) : S.wt (S.nf w) = w := (nf_spec hw).1

/-- **(b) Down-set property of lex-least factorizations**: if `n = n(w)` (`w ∈ Ap`) and `y ≤ n`,
then `w(y) ∈ Ap` and `n(w(y)) = y`. -/
theorem nf_downward {w : ℕ} (hw : S.IsApery S.multiplicity w) {y : Fin S.primitives'.card → ℕ}
    (hy : y ≤ S.nf w) : S.IsApery S.multiplicity (S.wt y) ∧ S.nf (S.wt y) = y := by
  have hxyu : y + (S.nf w - y) = S.nf w := by
    funext b
    have hb : y b ≤ S.nf w b := hy b
    simp only [Pi.add_apply, Pi.sub_apply]
    omega
  generalize S.nf w - y = u at hxyu
  have hwx : S.wt (S.nf w) = w := wt_nf hw
  generalize hx : S.nf w = x at hxyu hwx
  have hAp : S.IsApery S.multiplicity (S.wt y) :=
    hw.of_add (wt_mem y) (wt_mem u) (by rw [← wt_add, hxyu, hwx])
  refine ⟨hAp, ?_⟩
  set z := S.nf (S.wt y) with hz
  obtain ⟨hzw, hzmin⟩ := nf_spec hAp
  have h1 : toLex z ≤ toLex y := hzmin y rfl
  have h2 : toLex x ≤ toLex (z + u) := by
    rw [← hx]; exact (nf_spec hw).2 (z + u) (by rw [wt_add, hzw, ← wt_add, hxyu, hwx])
  have h3 : toLex (z + u) ≤ toLex (y + u) := by
    rw [toLex_add, toLex_add]; exact add_le_add_left h1 _
  rw [hxyu] at h3
  have h4 : toLex (z + u) = toLex x := le_antisymm h3 h2
  have h5 : z + u = y + u := by rw [hxyu]; exact toLex.injective h4
  exact add_right_cancel h5

theorem mem_factDownSet {x : Fin S.primitives'.card → ℕ} :
    x ∈ S.factDownSet ↔ ∃ w, S.IsApery S.multiplicity w ∧ S.nf w = x := by
  rw [factDownSet, Finset.mem_image]
  constructor
  · rintro ⟨w, hw, rfl⟩
    exact ⟨w, (mem_aperySet S.multiplicity_mem S.multiplicity_pos).1 hw, rfl⟩
  · rintro ⟨w, hw, rfl⟩
    exact ⟨w, (mem_aperySet S.multiplicity_mem S.multiplicity_pos).2 hw, rfl⟩

theorem isApery_wt_of_mem {x : Fin S.primitives'.card → ℕ} (hx : x ∈ S.factDownSet) :
    S.IsApery S.multiplicity (S.wt x) ∧ S.nf (S.wt x) = x := by
  obtain ⟨w, hw, rfl⟩ := mem_factDownSet.1 hx
  rw [wt_nf hw]
  exact ⟨hw, rfl⟩

/-- **(b) `D` is a down-set.** -/
theorem isDownSetFin_factDownSet : IsDownSetFin S.factDownSet := by
  intro x hx y hy
  obtain ⟨w, hw, rfl⟩ := mem_factDownSet.1 hx
  obtain ⟨hAp, hnf⟩ := nf_downward hw hy
  exact mem_factDownSet.2 ⟨_, hAp, hnf⟩

/-- `n` is injective on `Ap(S,m)` (it has the left inverse `w`). -/
theorem nf_injOn : Set.InjOn S.nf (S.aperySet S.multiplicity : Set ℕ) := by
  intro w1 h1 w2 h2 h
  have h1' := (mem_aperySet S.multiplicity_mem S.multiplicity_pos).1 h1
  have h2' := (mem_aperySet S.multiplicity_mem S.multiplicity_pos).1 h2
  rw [← wt_nf h1', ← wt_nf h2', h]

/-- **(a) `|D| = m`.** -/
theorem card_factDownSet : S.factDownSet.card = S.multiplicity := by
  rw [factDownSet, Finset.card_image_of_injOn nf_injOn, card_aperySet S.multiplicity_pos]

theorem sum_wt_factDownSet :
    ∑ x ∈ S.factDownSet, (S.wt x : ℤ) = ∑ w ∈ S.aperySet S.multiplicity, (w : ℤ) := by
  rw [factDownSet, Finset.sum_image nf_injOn]
  refine Finset.sum_congr rfl fun w hw => ?_
  rw [wt_nf ((mem_aperySet S.multiplicity_mem S.multiplicity_pos).1 hw)]

theorem wt_le_aperyMax {x : Fin S.primitives'.card → ℕ} (hx : x ∈ S.factDownSet) :
    S.wt x ≤ S.aperyMax S.multiplicity :=
  le_aperyMax ((mem_aperySet S.multiplicity_mem S.multiplicity_pos).2 (isApery_wt_of_mem hx).1)

/-! ## Column identity CH' -/

/-- The arithmetic core shared with Identity CH:
`d·m·M - (d+1)·ΣAp = m·W + (d-1)·m(m-1)/2` with `d = |P'|`. -/
theorem dmM_sub_sum_apery :
    (S.primitives'.card : ℤ) * S.multiplicity * S.aperyMax S.multiplicity -
        ((S.primitives'.card : ℤ) + 1) * ∑ w ∈ S.aperySet S.multiplicity, (w : ℤ) =
      S.multiplicity * S.wilfDefect +
        ((S.primitives'.card : ℤ) - 1) * ((S.multiplicity * (S.multiplicity - 1) / 2 : ℕ) : ℤ) := by
  have hm := S.multiplicity_pos
  have hsum : ∑ w ∈ S.aperySet S.multiplicity, w =
      S.multiplicity * S.genus + ∑ i ∈ range S.multiplicity, i :=
    (sum_aperySet hm (fun w => w)).trans (sum_apery_eq S.multiplicity_mem hm)
  have hs := Finset.sum_range_id_mul_two S.multiplicity
  rw [← Finset.sum_range_id]
  generalize ∑ i ∈ range S.multiplicity, i = s at hsum hs ⊢
  have hsum' : ∑ w ∈ S.aperySet S.multiplicity, (w : ℤ) = (S.multiplicity : ℤ) * S.genus + s := by
    have := congrArg (fun x : ℕ => (x : ℤ)) hsum
    push_cast at this
    exact this
  have hs' : (s : ℤ) * 2 = S.multiplicity * ((S.multiplicity : ℤ) - 1) := by
    have := congrArg (fun x : ℕ => (x : ℤ)) hs
    push_cast [Nat.cast_sub (show 1 ≤ S.multiplicity from hm)] at this
    exact this
  have hM' : (S.aperyMax S.multiplicity : ℤ) = S.conductor + S.multiplicity - 1 := by
    rw [aperyMax_eq S.multiplicity_mem hm]
    push_cast [Nat.cast_sub (show 1 ≤ S.conductor + S.multiplicity by omega)]
    ring
  have hg' : (S.ell : ℤ) + S.genus = S.conductor := by exact_mod_cast S.ell_add_genus
  have hd' : (S.embDim : ℤ) = S.primitives'.card + 1 := by
    exact_mod_cast card_primitives'_add_one.symm
  rw [hsum', hM', wilfDefect, hd']
  linear_combination (-((S.primitives'.card : ℤ) + 1) * S.multiplicity) * hg' -
    (S.primitives'.card : ℤ) * hs'

/-- **Column identity CH'** (in `ℤ`), with `d = e - 1`, `w(x) = Σ_a x_a p_a`, `M = max Ap`:
`Σ_a Σ_{x∈D, x+e_a∉D} (x_a + 1)·(M - w(x)) = m·W + (d - 1)·m(m-1)/2`. -/
theorem columnIdentity :
    ∑ a, ∑ x ∈ S.factDownSet.filter (fun x => x + Pi.single a 1 ∉ S.factDownSet),
        ((x a : ℤ) + 1) * ((S.aperyMax S.multiplicity : ℤ) - S.wt x) =
      S.multiplicity * S.wilfDefect +
        ((S.embDim : ℤ) - 1 - 1) * ((S.multiplicity * (S.multiplicity - 1) / 2 : ℕ) : ℤ) := by
  have hD := isDownSetFin_factDownSet (S := S)
  have hcol : ∀ a : Fin S.primitives'.card,
      ∑ x ∈ S.factDownSet.filter (fun x => x + Pi.single a 1 ∉ S.factDownSet),
          ((x a : ℤ) + 1) * ((S.aperyMax S.multiplicity : ℤ) - S.wt x) =
        (S.multiplicity : ℤ) * S.aperyMax S.multiplicity -
          ∑ x ∈ S.factDownSet, ((S.wt x : ℤ) + (S.gen a : ℤ) * x a) := by
    intro a
    have h1 := sum_wt_add_eq_columns hD a S.gen
    have h2 := card_eq_sum_columns hD a
    rw [card_factDownSet] at h2
    have h2' : (S.multiplicity : ℤ) =
        ∑ y ∈ S.factDownSet.filter (fun y => y + Pi.single a 1 ∉ S.factDownSet),
          ((y a : ℤ) + 1) := by
      rw [h2]; push_cast; rfl
    simp only [← wt_cast] at h1
    rw [h1, h2', Finset.sum_mul, ← Finset.sum_sub_distrib]
    refine Finset.sum_congr rfl fun y _ => ?_
    ring
  rw [Finset.sum_congr rfl fun a _ => hcol a, Finset.sum_sub_distrib, Finset.sum_const,
    Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
  have hswap : ∑ a : Fin S.primitives'.card,
      ∑ x ∈ S.factDownSet, ((S.wt x : ℤ) + (S.gen a : ℤ) * x a) =
      (S.primitives'.card : ℤ) * ∑ x ∈ S.factDownSet, (S.wt x : ℤ) +
        ∑ x ∈ S.factDownSet, (S.wt x : ℤ) := by
    rw [Finset.sum_comm]
    simp only [Finset.sum_add_distrib, Finset.sum_const, Finset.card_univ, Fintype.card_fin,
      nsmul_eq_mul, Finset.mul_sum]
    congr 1
    refine Finset.sum_congr rfl fun x _ => ?_
    rw [wt_cast]
    exact Finset.sum_congr rfl fun a _ => mul_comm _ _
  rw [hswap, sum_wt_factDownSet]
  have h := dmM_sub_sum_apery (S := S)
  have hd' : (S.embDim : ℤ) - 1 = S.primitives'.card := by
    have := card_primitives'_add_one (S := S); omega
  rw [hd']
  linear_combination h

/-! ## The Carry Lemma CL and `CL ⇒ Wilf` -/

/-- **Conjecture CL** (Carry Lemma) for `S`, with the lex-least factorization down-set `D`:
`Σ_a Σ_{x∈D, x+e_a∉D} (x_a + 1)·((M - w(x)) mod m) ≥ (d - 1)·m(m-1)/2` (in `ℤ`, `d = e - 1`). -/
def CL (S : NumericalSemigroup) : Prop :=
  ((S.embDim : ℤ) - 1 - 1) * ((S.multiplicity * (S.multiplicity - 1) / 2 : ℕ) : ℤ) ≤
    ∑ a, ∑ x ∈ S.factDownSet.filter (fun x => x + Pi.single a 1 ∉ S.factDownSet),
      ((x a : ℤ) + 1) * (((S.aperyMax S.multiplicity : ℤ) - S.wt x) % S.multiplicity)

theorem emod_le_self_of_nonneg {a b : ℤ} (ha : 0 ≤ a) (hb : 0 < b) : a % b ≤ a := by
  have h1 := Int.mul_ediv_add_emod a b
  have h2 : 0 ≤ a / b := Int.ediv_nonneg ha hb.le
  nlinarith

/-- **`CL ⇒ Wilf`**: by CH', `m·W + (d-1)·m(m-1)/2 ≥ LHS(CL) ≥ (d-1)·m(m-1)/2`. -/
theorem wilf_of_CL (h : S.CL) : S.conductor ≤ S.embDim * S.ell := by
  have hCH := columnIdentity (S := S)
  have hm : (0 : ℤ) < S.multiplicity := by exact_mod_cast S.multiplicity_pos
  have hle : ∑ a, ∑ x ∈ S.factDownSet.filter (fun x => x + Pi.single a 1 ∉ S.factDownSet),
        ((x a : ℤ) + 1) * (((S.aperyMax S.multiplicity : ℤ) - S.wt x) % S.multiplicity) ≤
      ∑ a, ∑ x ∈ S.factDownSet.filter (fun x => x + Pi.single a 1 ∉ S.factDownSet),
        ((x a : ℤ) + 1) * ((S.aperyMax S.multiplicity : ℤ) - S.wt x) := by
    refine Finset.sum_le_sum fun a _ => Finset.sum_le_sum fun x hx => ?_
    have hxD := (Finset.mem_filter.1 hx).1
    have hM : (S.wt x : ℤ) ≤ S.aperyMax S.multiplicity := by exact_mod_cast wt_le_aperyMax hxD
    apply mul_le_mul_of_nonneg_left _ (by positivity)
    exact emod_le_self_of_nonneg (by linarith) hm
  rw [CL] at h
  have hW : 0 ≤ (S.multiplicity : ℤ) * S.wilfDefect := by linarith
  have hW' : 0 ≤ S.wilfDefect := nonneg_of_mul_nonneg_right (by linarith) hm
  rw [wilfDefect] at hW'
  have : (S.conductor : ℤ) ≤ S.embDim * S.ell := by linarith
  exact_mod_cast this

/-- `(∀ S, CL S) → WilfConjecture`. -/
theorem wilfConjecture_of_CL (h : ∀ S : NumericalSemigroup, S.CL) : WilfConjecture :=
  fun S => wilf_of_CL (h S)

/-! ## Tile-CL (statement only) -/

/-- `φ(x) = Σ_a x_a·p_a ∈ ℤ/m`. -/
def tilePhi {d m : ℕ} (p : Fin d → ZMod m) (x : Fin d → ℕ) : ZMod m := ∑ a, (x a : ZMod m) * p a

/-- `T(y) = Σ_{a : y + e_a ∉ D} (y_a + 1)` (sum of the lengths of the columns topped by `y`). -/
def tileT {d : ℕ} (D : Finset (Fin d → ℕ)) (y : Fin d → ℕ) : ℕ :=
  ∑ a ∈ Finset.univ.filter (fun a => y + Pi.single a 1 ∉ D), (y a + 1)

/-- Tile hypotheses: `D` a finite down-set with `|D| = m` and `φ` a bijection `D → ℤ/m`. -/
def IsTile {d m : ℕ} (D : Finset (Fin d → ℕ)) (p : Fin d → ZMod m) : Prop :=
  IsDownSetFin D ∧ D.card = m ∧ Set.BijOn (tilePhi p) (D : Set (Fin d → ℕ)) Set.univ

/-- The Tile-CL inequality for one tile: for every `s ∈ ℤ/m`,
`f(s) = Σ_{y∈D} T(y)·⟨s - φ(y)⟩ ≥ (d - 1)·m(m-1)/2`, `⟨x⟩ = ZMod.val x ∈ [0, m)`. -/
def TileCLAt {d m : ℕ} (D : Finset (Fin d → ℕ)) (p : Fin d → ZMod m) : Prop :=
  ∀ s : ZMod m, (d - 1) * (m * (m - 1) / 2) ≤ ∑ y ∈ D, tileT D y * (s - tilePhi p y).val

/-- Convenience constructor for `IsTile` from finite (decidable) injectivity/surjectivity data. -/
theorem IsTile.mk' {d m : ℕ} {D : Finset (Fin d → ℕ)} {p : Fin d → ZMod m} (hD : IsDownSetFin D)
    (hcard : D.card = m) (hinj : ∀ x ∈ D, ∀ y ∈ D, tilePhi p x = tilePhi p y → x = y)
    (hsurj : ∀ s, ∃ x ∈ D, tilePhi p x = s) : IsTile D p :=
  ⟨hD, hcard, fun _ _ => Set.mem_univ _, fun x hx y hy h => hinj x hx y hy h,
    fun s _ => let ⟨x, hx, h⟩ := hsurj s; ⟨x, hx, h⟩⟩

/-- **Conjecture Tile-CL** (`.research/PROOFS.md`): every tile with `d ≥ 1` satisfies `TileCLAt`. -/
def TileCL : Prop :=
  ∀ (d m : ℕ) (D : Finset (Fin d → ℕ)) (p : Fin d → ZMod m), 1 ≤ d → IsTile D p → TileCLAt D p

end NumericalSemigroup
