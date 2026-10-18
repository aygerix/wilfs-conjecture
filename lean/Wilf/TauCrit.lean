import Wilf.TileCL2
import Mathlib.Tactic.IntervalCases

/-!
# The τ-criterion: Cross Lemma and Wilf when few Apéry elements lie in the top layer

Formalization of `.research/PROOFS.md`, section "τ-criterion" (2026-10-18).

Notation: `m = S.multiplicity`, `c = S.conductor`, `e = S.embDim`, `P' = S.primitives'`,
`d = |P'| = e - 1`, `X = S.topLayer = Ap(S,m) ∩ [c, c+m)`, `τ = |X|`, `ℓ(u) = S.minFactLen u`,
`n(u) = S.nfG u` (the graded-lex-least factorization of `u` over `P'`), and
`D = S.factDownSetG = {n(w) | w ∈ Ap(S,m)}` (a factorization tile: a down-set with `|D| = m`).

* `sum_nfG_eq_minFactLen`: `|n(u)| = ℓ(u)` for every Apéry element `u` (the graded-lex-least
  factorization has minimal length).
* `cross y = {y} ∪ {y - k·e_a | a, 1 ≤ k ≤ y_a}` has `|y| + 1` cells (`card_cross`), all `≤ y`.
* `not_nfG_le_nfG`: for `u ≠ u'` in `X`, `n(u) ≰ n(u')` (else `u' ≥ u + p_a > c + m`).
* `eq_inf_of_mem_cross`: for incomparable `y, y'`, a common cell of the two crosses is
  `y ⊓ y'` (coordinatewise minimum); hence two crosses share at most one cell.
* `two_mul_sum_card_le`: (double counting) `2·Σ_i |A_i| ≤ 2·|U| + Σ_{i ≠ j} |A_i ∩ A_j|`
  for finsets `A_i ⊆ U`.
* **Cross Lemma** `crossLemma_two_mul`: `2·Σ_{u∈X} (ℓ(u) + 1) ≤ 2·m + τ·(τ - 1)`,
  and `crossLemma`: `Σ_{u∈X} (ℓ(u) + 1) ≤ m + τ·(τ - 1)/2`.
  Sharper: `crossLemma_two_mul_P2`: `2·Σ_{u∈X} (ℓ(u) + 1) ≤ 2·m + P₂ord`, where `P₂ord`
  (`S.topPairs2`) is the number of *ordered* pairs `(u, u')`, `u ≠ u'` in `X`, whose vectors
  `n(u), n(u')` differ in exactly two coordinates (`P₂ord = 2·P₂`).
* **τ-criterion** `wilf_of_tauCriterion`: if `2(e-2)τ + τ(τ-1) ≤ (e-2)(m+1)` then
  `c ≤ e·ℓ` (via `TOP2`, `wilf_of_TOP2`); `wilf_of_tauCriterion_P2` is the `P₂` version.
* Corollaries: `e = 4`, `τ ≤ 4`, `m ≥ 13` (`wilf_of_embDim_four_tau_le_four`);
  `e = 4`, `τ ≤ 5`, `m ≥ 19`; and `τ ≤ e - 1`, `m + 4 ≥ 3e` (`wilf_of_tau_le_embDim_sub_one`).
-/

namespace NumericalSemigroup

open Finset

/-! ## Combinatorics of crosses in `ℕ^d` -/

section Cross

variable {d : ℕ}

/-- `cross y = {y} ∪ {y - (k+1)·e_a | a, k < y_a}`. -/
def cross (y : Fin d → ℕ) : Finset (Fin d → ℕ) :=
  insert y (((univ : Finset (Fin d)).sigma fun a => range (y a)).image
    fun t : (Σ _ : Fin d, ℕ) => y - Pi.single t.1 (t.2 + 1))

theorem card_cross (y : Fin d → ℕ) : (cross y).card = ∑ a, y a + 1 := by
  have hinj : Set.InjOn (fun t : (Σ _ : Fin d, ℕ) => y - Pi.single t.1 (t.2 + 1))
      (((univ : Finset (Fin d)).sigma fun a => range (y a)) : Set (Σ _ : Fin d, ℕ)) := by
    rintro ⟨a, k⟩ hak ⟨b, l⟩ hbl h
    simp only [coe_sigma, Set.mem_sigma_iff, mem_coe, mem_univ, mem_range, true_and] at hak hbl
    have ha := congrFun h a
    by_cases hab : a = b
    · subst hab
      simp only [Pi.sub_apply, Pi.single_eq_same] at ha
      have : k = l := by omega
      subst this
      rfl
    · simp only [Pi.sub_apply, Pi.single_eq_same, Pi.single_apply, if_neg hab] at ha
      omega
  rw [cross, card_insert_of_notMem, card_image_of_injOn hinj, card_sigma]
  · simp
  · intro hy
    obtain ⟨⟨a, k⟩, hak, h⟩ := mem_image.1 hy
    have := congrFun h a
    simp only [mem_sigma, mem_univ, mem_range, true_and] at hak
    simp only [Pi.sub_apply, Pi.single_eq_same] at this
    omega

theorem le_of_mem_cross {x y : Fin d → ℕ} (hx : x ∈ cross y) : x ≤ y := by
  rcases mem_insert.1 hx with rfl | hx
  · exact le_rfl
  · obtain ⟨⟨a, k⟩, -, rfl⟩ := mem_image.1 hx
    exact fun c => Nat.sub_le _ _

/-- A cell of `cross y` differs from `y` in at most one coordinate. -/
theorem eq_of_mem_cross {x y : Fin d → ℕ} (hx : x ∈ cross y) {a b : Fin d} (ha : x a ≠ y a)
    (hb : x b ≠ y b) : a = b := by
  rcases mem_insert.1 hx with rfl | hx
  · exact absurd rfl ha
  · obtain ⟨⟨c, k⟩, -, rfl⟩ := mem_image.1 hx
    simp only [Pi.sub_apply, Pi.single_apply] at ha hb
    by_cases hac : a = c
    · by_cases hbc : b = c
      · rw [hac, hbc]
      · rw [if_neg hbc] at hb; omega
    · rw [if_neg hac] at ha; omega

theorem cross_subset {D : Finset (Fin d → ℕ)} (hD : IsDownSetFin D) {y : Fin d → ℕ} (hy : y ∈ D) :
    cross y ⊆ D :=
  fun _ hx => hD y hy _ (le_of_mem_cross hx)

/-- For incomparable `y, y'`, every common cell of `cross y` and `cross y'` is `y ⊓ y'`. -/
theorem eq_inf_of_mem_cross {x y y' : Fin d → ℕ} (h1 : ¬ y ≤ y') (h2 : ¬ y' ≤ y)
    (hx : x ∈ cross y) (hx' : x ∈ cross y') : x = fun c => min (y c) (y' c) := by
  funext c
  have hxy : x c ≤ y c := le_of_mem_cross hx c
  have hxy' : x c ≤ y' c := le_of_mem_cross hx' c
  show x c = min (y c) (y' c)
  by_contra hne
  have hlt : x c < min (y c) (y' c) := lt_of_le_of_ne (le_min hxy hxy') hne
  have hc : x c ≠ y c := (lt_of_lt_of_le hlt (min_le_left _ _)).ne
  have hc' : x c ≠ y' c := (lt_of_lt_of_le hlt (min_le_right _ _)).ne
  have hy : ∀ b, b ≠ c → y b = x b := fun b hb => by
    by_contra h
    exact hb (eq_of_mem_cross hx (Ne.symm h) hc)
  have hy' : ∀ b, b ≠ c → y' b = x b := fun b hb => by
    by_contra h
    exact hb (eq_of_mem_cross hx' (Ne.symm h) hc')
  rcases le_total (y c) (y' c) with h | h
  · apply h1
    intro b
    by_cases hb : b = c
    · rw [hb]; exact h
    · rw [hy b hb, hy' b hb]
  · apply h2
    intro b
    by_cases hb : b = c
    · rw [hb]; exact h
    · rw [hy b hb, hy' b hb]

/-- Crosses of incomparable vectors share at most one cell. -/
theorem card_cross_inter_le_one {y y' : Fin d → ℕ} (h1 : ¬ y ≤ y') (h2 : ¬ y' ≤ y) :
    (cross y ∩ cross y').card ≤ 1 := by
  rw [card_le_one]
  intro x hx z hz
  rw [mem_inter] at hx hz
  rw [eq_inf_of_mem_cross h1 h2 hx.1 hx.2, eq_inf_of_mem_cross h1 h2 hz.1 hz.2]

/-- If the crosses of incomparable `y, y'` meet, then `y, y'` differ in exactly two coordinates. -/
theorem card_ne_eq_two_of_cross_inter {y y' : Fin d → ℕ} (h1 : ¬ y ≤ y') (h2 : ¬ y' ≤ y)
    (hne : (cross y ∩ cross y').Nonempty) :
    (univ.filter fun a => y a ≠ y' a).card = 2 := by
  obtain ⟨x, hx⟩ := hne
  rw [mem_inter] at hx
  have hxe := eq_inf_of_mem_cross h1 h2 hx.1 hx.2
  obtain ⟨a, ha⟩ : ∃ a, y' a < y a := by
    by_contra h; push Not at h; exact h1 h
  obtain ⟨b, hb⟩ : ∃ b, y b < y' b := by
    by_contra h; push Not at h; exact h2 h
  have hxa : x a ≠ y a := by rw [hxe]; simp only; omega
  have hxb : x b ≠ y' b := by rw [hxe]; simp only; omega
  have hset : (univ.filter fun c => y c ≠ y' c) = {a, b} := by
    ext c
    simp only [mem_filter, mem_univ, true_and, mem_insert, mem_singleton]
    constructor
    · intro hc
      rcases Nat.lt_or_gt_of_ne hc with hc | hc
      · right
        refine eq_of_mem_cross hx.2 ?_ hxb
        rw [hxe]; simp only; omega
      · left
        refine eq_of_mem_cross hx.1 ?_ hxa
        rw [hxe]; simp only; omega
    · rintro (rfl | rfl) <;> omega
  rw [hset, card_pair]
  rintro rfl
  omega

end Cross

/-! ## A double-counting inequality -/

/-- For finsets `A_i ⊆ U` (`i ∈ I`): `2·Σ_i |A_i| ≤ 2·|U| + Σ_{(i,j) ∈ I.offDiag} |A_i ∩ A_j|`.
(With `j(x) = #{i | x ∈ A_i}`: `2·j ≤ 2 + j(j-1)` pointwise.) -/
theorem two_mul_sum_card_le {ι α : Type*} [DecidableEq ι] [DecidableEq α] (I : Finset ι)
    (U : Finset α) (A : ι → Finset α) (hA : ∀ i ∈ I, A i ⊆ U) :
    2 * ∑ i ∈ I, (A i).card ≤ 2 * U.card + ∑ p ∈ I.offDiag, (A p.1 ∩ A p.2).card := by
  have h1 : ∑ i ∈ I, (A i).card = ∑ x ∈ U, (I.filter fun i => x ∈ A i).card := by
    simp_rw [card_filter]
    rw [sum_comm]
    refine sum_congr rfl fun i hi => ?_
    rw [← card_filter, filter_mem_eq_inter, inter_eq_right.2 (hA i hi)]
  have h2 : ∑ p ∈ I.offDiag, (A p.1 ∩ A p.2).card =
      ∑ x ∈ U, (I.filter fun i => x ∈ A i).offDiag.card := by
    have hoff : ∀ x, (I.filter fun i => x ∈ A i).offDiag =
        I.offDiag.filter fun p => x ∈ A p.1 ∧ x ∈ A p.2 := by
      intro x
      ext ⟨i, j⟩
      simp only [mem_offDiag, mem_filter]
      tauto
    simp_rw [hoff, card_filter]
    rw [sum_comm]
    refine sum_congr rfl fun p hp => ?_
    have hp1 : p.1 ∈ I := (mem_offDiag.1 hp).1
    rw [← card_filter]
    congr 1
    ext x
    simp only [mem_filter, mem_inter]
    constructor
    · rintro ⟨hx1, hx2⟩; exact ⟨hA _ hp1 hx1, hx1, hx2⟩
    · rintro ⟨-, hx⟩; exact hx
  rw [h1, h2, card_eq_sum_ones U, mul_sum, mul_sum, ← sum_add_distrib]
  refine sum_le_sum fun x _ => ?_
  rw [offDiag_card]
  generalize (I.filter fun i => x ∈ A i).card = j
  rcases (show j ≤ 1 ∨ 2 ≤ j by omega) with h | h
  · rcases (show j = 0 ∨ j = 1 by omega) with rfl | rfl <;> simp
  · rcases (show j = 2 ∨ 3 ≤ j by omega) with rfl | h3
    · simp
    · have : 3 * j ≤ j * j := Nat.mul_le_mul_right j h3
      omega

/-! ## Graded-lex factorizations of top-layer elements -/

variable {S : NumericalSemigroup}

theorem sum_primitives'_eq_sum_gen {β : Type*} [AddCommMonoid β] (g : ℕ → β) :
    ∑ p ∈ S.primitives', g p = ∑ a, g (S.gen a) := by
  have := Finset.sum_map (univ : Finset (Fin S.primitives'.card))
    (S.primitives'.orderEmbOfFin rfl).toEmbedding g
  rw [Finset.map_orderEmbOfFin_univ] at this
  exact this

theorem gen_injective : Function.Injective (S.gen) :=
  (S.primitives'.orderEmbOfFin rfl).injective

/-- `|n_G(u)| = ℓ(u)`: the graded-lex-least factorization of an Apéry element has minimal length. -/
theorem sum_nfG_eq_minFactLen {u : ℕ} (hu : S.IsApery S.multiplicity u) :
    ∑ a, S.nfG u a = S.minFactLen u := by
  apply le_antisymm
  · obtain ⟨f, hf, hlen⟩ := minFactLen_spec hu
    have hx : S.wt (fun a => f (S.gen a)) = u := by
      rw [← hf, sum_primitives'_eq_sum_gen (fun p => f p * p)]
      rfl
    have := sum_le_of_grKey_le ((nfG_spec hu).2 _ hx)
    rw [← hlen, sum_primitives'_eq_sum_gen f]
    exact this
  · set x := S.nfG u
    let f : ℕ → ℕ := Function.extend S.gen x 0
    have hf : ∀ a, f (S.gen a) = x a := fun a => gen_injective.extend_apply x 0 a
    have hfu : ∑ p ∈ S.primitives', f p * p = u := by
      rw [sum_primitives'_eq_sum_gen (fun p => f p * p)]
      simp only [hf]
      exact wt_nfG hu
    have := minFactLen_le hfu
    rw [sum_primitives'_eq_sum_gen f] at this
    simpa only [hf] using this

theorem isApery_of_mem_topLayer {u : ℕ} (hu : u ∈ S.topLayer) : S.IsApery S.multiplicity u :=
  (mem_aperySet S.multiplicity_mem S.multiplicity_pos).1 (mem_topLayer.1 hu).1

/-- For `u ≠ u'` in the top layer, `n_G(u) ≰ n_G(u')`: otherwise `u' = u + w(z)` with `z ≠ 0`,
so `u' ≥ u + p_a > c + m`. -/
theorem not_nfG_le_nfG {u u' : ℕ} (hu : u ∈ S.topLayer) (hu' : u' ∈ S.topLayer) (hne : u ≠ u') :
    ¬ S.nfG u ≤ S.nfG u' := by
  intro hle
  obtain ⟨-, hcu, -⟩ := mem_topLayer.1 hu
  obtain ⟨-, -, hum'⟩ := mem_topLayer.1 hu'
  have hAp := isApery_of_mem_topLayer hu
  have hAp' := isApery_of_mem_topLayer hu'
  set z := S.nfG u' - S.nfG u with hzdef
  have hz : S.nfG u + z = S.nfG u' := by
    funext b
    have : S.nfG u b ≤ S.nfG u' b := hle b
    simp only [hzdef, Pi.add_apply, Pi.sub_apply]
    omega
  have hw : u + S.wt z = u' := by rw [← wt_nfG hAp, ← wt_add, hz, wt_nfG hAp']
  by_cases hz0 : z = 0
  · apply hne
    rw [hz0] at hw
    simpa [wt] using hw
  · obtain ⟨a, ha⟩ : ∃ a, z a ≠ 0 := by
      by_contra h
      push Not at h
      exact hz0 (funext h)
    have h1 : z a * S.gen a ≤ S.wt z :=
      Finset.single_le_sum (f := fun b => z b * S.gen b) (fun _ _ => Nat.zero_le _)
        (Finset.mem_univ a)
    have h2 : S.gen a ≤ z a * S.gen a := Nat.le_mul_of_pos_left _ (Nat.pos_of_ne_zero ha)
    have h3 := multiplicity_lt_of_mem_primitives' (gen_mem a)
    omega

/-! ## The Cross Lemma -/

/-- `P₂ord`: the number of ordered pairs `(u, u')` of distinct top-layer elements whose graded-lex
factorizations `n(u), n(u')` differ in exactly two coordinates (`= 2·P₂` in the paper). -/
noncomputable def topPairs2 (S : NumericalSemigroup) : ℕ :=
  (S.topLayer.offDiag.filter fun p =>
    (univ.filter fun a => S.nfG p.1 a ≠ S.nfG p.2 a).card = 2).card

/-- Cross Lemma, sharp form (`×2`): `2·Σ_{u∈X} (ℓ(u) + 1) ≤ 2·m + P₂ord` (`P₂ord = 2·P₂`). -/
theorem crossLemma_two_mul_P2 (S : NumericalSemigroup) :
    2 * ∑ u ∈ S.topLayer, (S.minFactLen u + 1) ≤ 2 * S.multiplicity + S.topPairs2 := by
  have hD := isFactTile_factDownSetG (S := S)
  have key := two_mul_sum_card_le S.topLayer S.factDownSetG (fun u => cross (S.nfG u))
    (fun u hu => cross_subset hD.1
      (mem_factDownSetG.2 ⟨u, isApery_of_mem_topLayer hu, rfl⟩))
  have hcard : ∀ u ∈ S.topLayer, (cross (S.nfG u)).card = S.minFactLen u + 1 := fun u hu => by
    rw [card_cross, sum_nfG_eq_minFactLen (isApery_of_mem_topLayer hu)]
  rw [sum_congr rfl hcard, hD.card_eq] at key
  refine key.trans (Nat.add_le_add_left ?_ _)
  rw [topPairs2, card_filter]
  refine sum_le_sum fun p hp => ?_
  obtain ⟨hp1, hp2, hp12⟩ := mem_offDiag.1 hp
  have h1 := not_nfG_le_nfG hp1 hp2 hp12
  have h2 := not_nfG_le_nfG hp2 hp1 (Ne.symm hp12)
  by_cases hne : (cross (S.nfG p.1) ∩ cross (S.nfG p.2)).Nonempty
  · rw [if_pos (card_ne_eq_two_of_cross_inter h1 h2 hne)]
    exact card_cross_inter_le_one h1 h2
  · rw [not_nonempty_iff_eq_empty] at hne
    rw [hne, card_empty]
    exact Nat.zero_le _

theorem topPairs2_le (S : NumericalSemigroup) :
    S.topPairs2 ≤ S.topLayer.card * (S.topLayer.card - 1) := by
  rw [Nat.mul_sub_one, ← offDiag_card]
  exact card_filter_le _ _

/-- **Cross Lemma** (`×2` form): `2·Σ_{u∈X} (ℓ(u) + 1) ≤ 2·m + τ·(τ - 1)`. -/
theorem crossLemma_two_mul (S : NumericalSemigroup) :
    2 * ∑ u ∈ S.topLayer, (S.minFactLen u + 1) ≤
      2 * S.multiplicity + S.topLayer.card * (S.topLayer.card - 1) :=
  (crossLemma_two_mul_P2 S).trans (Nat.add_le_add_left (topPairs2_le S) _)

/-- **Cross Lemma**: `Σ_{u∈X} (ℓ(u) + 1) ≤ m + τ·(τ - 1)/2`. -/
theorem crossLemma (S : NumericalSemigroup) :
    ∑ u ∈ S.topLayer, (S.minFactLen u + 1) ≤
      S.multiplicity + S.topLayer.card * (S.topLayer.card - 1) / 2 := by
  have h := crossLemma_two_mul S
  have hev : (S.topLayer.card * (S.topLayer.card - 1)) % 2 = 0 :=
    Nat.even_iff.1 (Nat.even_mul_pred_self _)
  generalize S.topLayer.card * (S.topLayer.card - 1) = P at h hev ⊢
  omega

/-! ## The τ-criterion -/

/-- The arithmetic of the τ-criterion: from the Cross Lemma bound `2·Σ(ℓ+1) ≤ 2m + Q` and
`2(e-2)τ + Q ≤ (e-2)(m+1)` (any `Q`), `TOP''` follows. -/
theorem top2_of_crossBound (S : NumericalSemigroup) (he : 2 ≤ S.embDim) (Q : ℕ)
    (hX : 2 * ∑ u ∈ S.topLayer, (S.minFactLen u + 1) ≤ 2 * S.multiplicity + Q)
    (h : 2 * (S.embDim - 2) * S.topLayer.card + Q ≤ (S.embDim - 2) * (S.multiplicity + 1)) :
    S.TOP2 := by
  rw [TOP2, Nat.le_div_iff_mul_le two_pos]
  have hsum : ∑ u ∈ S.topLayer, (u - S.conductor + 1) * ((S.embDim - 1) + S.minFactLen u) ≤
      S.multiplicity * (∑ u ∈ S.topLayer, (S.minFactLen u + 1) +
        (S.embDim - 2) * S.topLayer.card) := by
    calc ∑ u ∈ S.topLayer, (u - S.conductor + 1) * ((S.embDim - 1) + S.minFactLen u)
        ≤ ∑ u ∈ S.topLayer, S.multiplicity * ((S.minFactLen u + 1) + (S.embDim - 2)) :=
          sum_le_sum fun u hu => by
            obtain ⟨-, h1, h2⟩ := mem_topLayer.1 hu
            exact Nat.mul_le_mul (by omega) (by omega)
      _ = S.multiplicity * (∑ u ∈ S.topLayer, (S.minFactLen u + 1) +
            (S.embDim - 2) * S.topLayer.card) := by
          rw [← mul_sum, sum_add_distrib, sum_const, smul_eq_mul, mul_comm S.topLayer.card]
  have hR : (S.embDim - 1 + 1) * S.multiplicity + (S.embDim - 1) - 1 =
      2 * S.multiplicity + (S.embDim - 2) * (S.multiplicity + 1) := by
    obtain ⟨k, hk⟩ : ∃ k, S.embDim = k + 2 := ⟨S.embDim - 2, by omega⟩
    rw [hk, show k + 2 - 1 = k + 1 by omega, show k + 2 - 2 = k by omega,
      show (k + 1 + 1) * S.multiplicity + (k + 1) - 1 = (k + 1 + 1) * S.multiplicity + k by omega]
    ring
  rw [hR]
  refine (Nat.mul_le_mul_right 2 hsum).trans ?_
  rw [mul_assoc]
  apply Nat.mul_le_mul_left
  have : 2 * (S.embDim - 2) * S.topLayer.card = 2 * ((S.embDim - 2) * S.topLayer.card) := by ring
  omega

/-- **τ-criterion ⇒ TOP''** (for `e ≥ 2`). -/
theorem top2_of_tauCriterion (S : NumericalSemigroup) (he : 2 ≤ S.embDim)
    (h : 2 * (S.embDim - 2) * S.topLayer.card + S.topLayer.card * (S.topLayer.card - 1) ≤
      (S.embDim - 2) * (S.multiplicity + 1)) :
    S.TOP2 :=
  top2_of_crossBound S he _ (crossLemma_two_mul S) h

/-- **τ-criterion** (Wilf): with `τ = |Ap(S,m) ∩ [c, c+m)|`,
`2(e-2)τ + τ(τ-1) ≤ (e-2)(m+1) ⇒ c ≤ e·ℓ`. -/
theorem wilf_of_tauCriterion (S : NumericalSemigroup)
    (h : 2 * (S.embDim - 2) * S.topLayer.card + S.topLayer.card * (S.topLayer.card - 1) ≤
      (S.embDim - 2) * (S.multiplicity + 1)) :
    S.conductor ≤ S.embDim * S.ell := by
  by_cases he : S.embDim ≤ 3
  · exact wilf_of_embDim_le_three S he
  · exact wilf_of_TOP2 (top2_of_tauCriterion S (by omega) h)

/-- **τ-criterion, sharp form** (Wilf): `2(e-2)τ + P₂ord ≤ (e-2)(m+1) ⇒ c ≤ e·ℓ`, where
`P₂ord = S.topPairs2 = 2·P₂`. -/
theorem wilf_of_tauCriterion_P2 (S : NumericalSemigroup)
    (h : 2 * (S.embDim - 2) * S.topLayer.card + S.topPairs2 ≤
      (S.embDim - 2) * (S.multiplicity + 1)) :
    S.conductor ≤ S.embDim * S.ell := by
  by_cases he : S.embDim ≤ 3
  · exact wilf_of_embDim_le_three S he
  · exact wilf_of_TOP2 (top2_of_crossBound S (by omega) _ (crossLemma_two_mul_P2 S) h)

/-! ## Corollaries -/

/-- `e = 4`, `τ ≤ 4`, `m ≥ 13` ⇒ Wilf. -/
theorem wilf_of_embDim_four_tau_le_four (S : NumericalSemigroup) (he : S.embDim = 4)
    (hτ : S.topLayer.card ≤ 4) (hm : 13 ≤ S.multiplicity) :
    S.conductor ≤ S.embDim * S.ell := by
  apply wilf_of_tauCriterion
  rw [he]
  generalize S.topLayer.card = τ at hτ
  interval_cases τ <;> omega

/-- `e = 4`, `τ ≤ 5`, `m ≥ 19` ⇒ Wilf. -/
theorem wilf_of_embDim_four_tau_le_five (S : NumericalSemigroup) (he : S.embDim = 4)
    (hτ : S.topLayer.card ≤ 5) (hm : 19 ≤ S.multiplicity) :
    S.conductor ≤ S.embDim * S.ell := by
  apply wilf_of_tauCriterion
  rw [he]
  generalize S.topLayer.card = τ at hτ
  interval_cases τ <;> omega

/-- `τ ≤ e - 1` and `m ≥ 3e - 4` ⇒ Wilf. -/
theorem wilf_of_tau_le_embDim_sub_one (S : NumericalSemigroup)
    (hτ : S.topLayer.card ≤ S.embDim - 1) (hm : 3 * S.embDim ≤ S.multiplicity + 4) :
    S.conductor ≤ S.embDim * S.ell := by
  by_cases he : S.embDim ≤ 3
  · exact wilf_of_embDim_le_three S he
  apply wilf_of_tauCriterion
  obtain ⟨k, hk⟩ : ∃ k, S.embDim = k + 2 := ⟨S.embDim - 2, by omega⟩
  rw [hk] at hτ hm ⊢
  simp only [Nat.add_sub_cancel]
  generalize S.topLayer.card = τ at hτ
  generalize S.multiplicity = m at hm
  -- `2kτ + τ(τ-1) ≤ (k+1)(3k) ≤ k(m+1)` since `τ ≤ k + 1` and `3(k+1) ≤ m + 1`.
  have hτ' : τ ≤ k + 1 := by omega
  have hm' : 3 * k + 3 ≤ m + 1 := by omega
  rcases Nat.eq_zero_or_pos τ with rfl | hτpos
  · simp
  obtain ⟨t, rfl⟩ : ∃ t, τ = t + 1 := ⟨τ - 1, by omega⟩
  simp only [Nat.add_sub_cancel]
  have h1 : 2 * k * (t + 1) + (t + 1) * t ≤ (k + 1) * (3 * k) := by
    have := Nat.mul_le_mul (show t + 1 ≤ k + 1 by omega) (show 2 * k + t ≤ 3 * k by omega)
    nlinarith
  have h2 : (k + 1) * (3 * k) ≤ k * (m + 1) := by
    have := Nat.mul_le_mul_left k hm'
    nlinarith
  omega

end NumericalSemigroup
