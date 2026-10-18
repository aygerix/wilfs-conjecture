import Wilf.TileTop

/-!
# MaxCL ⇒ Tile-TOP'', Flat-MaxCL (tiles of height `≤ 2`), and Wilf for factorization height `≤ 2`

Notation (as in `Wilf.Carry`, `Wilf.TileReduction`, `Wilf.TileTop`): a tile `(D, p)` is a finite
down-set `D ⊆ ℕ^d` with `|D| = m` on which `φ = tilePhi p` (`φ(x) = Σ_a x_a p_a ∈ ℤ/m`) is a
bijection onto `ℤ/m` (`IsTile`); `|y| = Σ_a y_a`; `y` is *maximal* (`IsMaxCell D y`) if
`y + e_a ∉ D` for every `a`. For `σ ∈ ℤ/m` write `r(x) = ⟨φ(x) - σ⟩ = ZMod.val (φ(x) - σ) ∈ [0, m)`.

**MaxCL** at a tile (`MaxCLAt`, subtraction-free form): for every `σ ∈ ℤ/m`,

    Σ_{y ∈ D maximal} (d + |y|)·r(y) ≤ (d + 1)·Σ_{x ∈ D} r(x).

(Over `ℤ` this is `Σ_{y max} (|y| - 1)·r(y) ≤ (d + 1)·Σ_{z non-max} r(z)`.)

Main results:
* (A) `tileTOPAt_of_maxCLAt : 1 ≤ d → IsTile D p → MaxCLAt D p → TileTOPAt D p`.
  Proof: with `σ = s + 1`, `m - ⟨s - φ(y)⟩ = r(y) + 1` (`sub_val_eq_val_sub_add_one`), so
  `2·Σ_A T(m - ⟨s - φ⟩) = 2·Σ_A T·r + 2·Σ_A T` (`A` = maximal cells, `T(y) = d + |y|`).
  MaxCL and `2·Σ_D r = m(m-1)` (`r` is a bijection `D → [0, m)`) bound the first term by
  `(d+1)·m(m-1)`; `Σ_A T ≤ d·m` because in each direction `a` the maximal cells are `a`-tops and the
  `a`-columns have total length `m` (`card_eq_sum_columns`).
* (B) `maxCLAt_of_height_le_two : IsTile D p → (∀ x ∈ D, |x| ≤ 2) → MaxCLAt D p` ("Flat-MaxCL").
  Proof: `E = {x ∈ D : |x| = 2}`. For `e ∈ E`, `Σ_a e_a·ρ_a ≡ r(e) + ρ_0 (mod m)` with
  `ρ_a = r(e_a)`, `ρ_0 = r(0)`, whence `r(e) + ρ_0 ≤ Σ_a e_a ρ_a + m·[m ≤ r(e) + ρ_0]`
  (`le_add_ite_of_mod_eq`); the "wrapped" edges inject (via `r`) into `[m - ρ_0, m)`, so there are at
  most `ρ_0` of them. With `deg(a) = Σ_{e∈E} e_a ≤ d + 1` (nonzero only for non-maximal units) and
  `m ≤ 1 + d + |E|` this gives `Σ_E r ≤ (d+1)·(ρ_0 + Σ_{non-max units} ρ_a) ≤ (d+1)·Σ_{non-max} r`
  (`sum_edges_le`), and MaxCL follows since `(d + |y|) ≤ (d + 1) + [|y| = 2]`.
* (C) `wilf_of_factDownSet_height_le_two : (∀ x ∈ S.factDownSet, |x| ≤ 2) → c(S) ≤ e(S)·ℓ(S)`.
-/

namespace NumericalSemigroup

open Finset

/-! ## Statement of MaxCL -/

/-- **MaxCL** for one tile (subtraction-free form): for every `σ ∈ ℤ/m`,
`Σ_{y ∈ D maximal} (d + |y|)·⟨φ(y) - σ⟩ ≤ (d + 1)·Σ_{x ∈ D} ⟨φ(x) - σ⟩`, `⟨·⟩ = ZMod.val`. -/
def MaxCLAt {d m : ℕ} (D : Finset (Fin d → ℕ)) (p : Fin d → ZMod m) : Prop :=
  ∀ σ : ZMod m, ∑ y ∈ D.filter (IsMaxCell D), (d + ∑ a, y a) * (tilePhi p y - σ).val ≤
    (d + 1) * ∑ x ∈ D, (tilePhi p x - σ).val

/-! ## Basic facts about tiles -/

section TileFacts

variable {d m : ℕ} {D : Finset (Fin d → ℕ)} {p : Fin d → ZMod m}

/-- A tile is nonempty, so `m ≥ 1`. -/
theorem IsTile.pos (h : IsTile D p) : 0 < m := by
  obtain ⟨x, hx, -⟩ := h.2.2.2.2 (Set.mem_univ (0 : ZMod m))
  have : 0 < D.card := Finset.card_pos.2 ⟨x, hx⟩
  rwa [h.2.1] at this

/-- `x ↦ ⟨φ(x) - σ⟩` is injective on a tile. -/
theorem IsTile.injOn_val (h : IsTile D p) (σ : ZMod m) :
    Set.InjOn (fun x => (tilePhi p x - σ).val) (D : Set (Fin d → ℕ)) := by
  have : NeZero m := ⟨h.pos.ne'⟩
  intro x hx y hy hxy
  exact h.2.2.injOn hx hy (sub_left_injective (ZMod.val_injective m hxy))

/-- `2·Σ_{x∈D} ⟨φ(x) - σ⟩ = m(m-1)`: `x ↦ ⟨φ(x) - σ⟩` is a bijection `D → [0, m)`. -/
theorem IsTile.sum_val_mul_two (h : IsTile D p) (σ : ZMod m) :
    (∑ x ∈ D, (tilePhi p x - σ).val) * 2 = m * (m - 1) := by
  have : NeZero m := ⟨h.pos.ne'⟩
  have himg : D.image (fun x => (tilePhi p x - σ).val) = range m := by
    apply Finset.eq_of_subset_of_card_le
    · intro i hi
      obtain ⟨x, -, rfl⟩ := Finset.mem_image.1 hi
      exact Finset.mem_range.2 (ZMod.val_lt _)
    · rw [Finset.card_range, Finset.card_image_of_injOn (h.injOn_val σ), h.2.1]
  rw [← Finset.sum_range_id_mul_two, ← himg, Finset.sum_image (h.injOn_val σ)]

end TileFacts

/-! ## (A) MaxCL ⇒ Tile-TOP'' -/

/-- For `m ≥ 1`: `m - ⟨s - z⟩ = ⟨z - (s + 1)⟩ + 1`. -/
theorem sub_val_eq_val_sub_add_one {m : ℕ} [NeZero m] (s z : ZMod m) :
    m - (s - z).val = (z - (s + 1)).val + 1 := by
  have h1 := ZMod.val_lt (s - z)
  have h2 := ZMod.val_lt (z - (s + 1))
  have h3 : (((z - (s + 1)).val + (s - z).val + 1 : ℕ) : ZMod m) = 0 := by
    rw [Nat.cast_add, Nat.cast_add, ZMod.natCast_zmod_val, ZMod.natCast_zmod_val, Nat.cast_one]
    ring
  rw [ZMod.natCast_eq_zero_iff] at h3
  obtain ⟨k, hk⟩ := h3
  have hk1 : k = 1 := by
    rcases Nat.lt_trichotomy k 1 with hk0 | hk1 | hk2
    · have : k = 0 := by omega
      subst this
      simp at hk
    · exact hk1
    · have : m * 2 ≤ m * k := Nat.mul_le_mul_left m hk2
      omega
  subst hk1
  omega

/-- The final arithmetic step of (A). -/
theorem tileTOP_arith {d m X Y R : ℕ} (hm : 1 ≤ m) (hX : X ≤ (d + 1) * R)
    (hR : R * 2 = m * (m - 1)) (hY : Y ≤ d * m) : 2 * (X + Y) ≤ m * ((d + 1) * m + d - 1) := by
  obtain ⟨k, rfl⟩ : ∃ k, m = k + 1 := ⟨m - 1, by omega⟩
  simp only [Nat.add_sub_cancel] at hR
  have e : (d + 1) * (k + 1) + d - 1 = (d + 1) * k + 2 * d := by
    rw [show (d + 1) * (k + 1) = (d + 1) * k + d + 1 by ring]
    omega
  rw [e]
  have hR' : (d + 1) * R * 2 = (d + 1) * ((k + 1) * k) := by rw [mul_assoc, hR]
  nlinarith

/-- **(A) MaxCL ⇒ Tile-TOP''** for a single tile. -/
theorem tileTOPAt_of_maxCLAt {d m : ℕ} {D : Finset (Fin d → ℕ)} {p : Fin d → ZMod m}
    (_hd : 1 ≤ d) (hT : IsTile D p) (hM : MaxCLAt D p) : TileTOPAt D p := by
  have hm := hT.pos
  have : NeZero m := ⟨hm.ne'⟩
  intro s
  have hrw : ∀ y ∈ D.filter (fun y => ∀ a, y + Pi.single a 1 ∉ D),
      (d + ∑ a, y a) * (m - (s - tilePhi p y).val) =
        (d + ∑ a, y a) * (tilePhi p y - (s + 1)).val + (d + ∑ a, y a) := by
    intro y _
    rw [sub_val_eq_val_sub_add_one]
    ring
  rw [Finset.sum_congr rfl hrw, Finset.sum_add_distrib]
  have h1 := hM (s + 1)
  rw [← filter_isMaxCell] at h1
  have h2 := hT.sum_val_mul_two (s + 1)
  have h3 : ∑ y ∈ D.filter (fun y => ∀ a, y + Pi.single a 1 ∉ D), (d + ∑ a, y a) ≤ d * m := by
    have hT' : ∀ y ∈ D.filter (fun y => ∀ a, y + Pi.single a 1 ∉ D),
        d + ∑ a, y a = ∑ a, (y a + 1) := by
      intro y _
      rw [Finset.sum_add_distrib]
      simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, smul_eq_mul, mul_one]
      omega
    rw [Finset.sum_congr rfl hT', Finset.sum_comm]
    calc ∑ a, ∑ y ∈ D.filter (fun y => ∀ a, y + Pi.single a 1 ∉ D), (y a + 1)
        ≤ ∑ _a : Fin d, m := by
          refine Finset.sum_le_sum fun a _ => ?_
          rw [← hT.2.1, card_eq_sum_columns hT.1 a]
          refine Finset.sum_le_sum_of_subset fun y hy => ?_
          have hy' := Finset.mem_filter.1 hy
          exact Finset.mem_filter.2 ⟨hy'.1, hy'.2 a⟩
      _ = d * m := by simp
  exact tileTOP_arith hm h1 h2 h3

/-! ## (B) Flat-MaxCL: MaxCL for tiles of height `≤ 2` -/

section Flat

variable {d : ℕ}

/-- If `k ≤ x_b` and `|x| ≤ k` then `x = k·e_b`. -/
theorem eq_single_of_le_sum {x : Fin d → ℕ} {b : Fin d} {k : ℕ} (hb : k ≤ x b)
    (hs : ∑ a, x a ≤ k) : x = Pi.single b k := by
  funext c
  by_cases hc : c = b
  · subst hc
    have := Finset.single_le_sum (f := x) (fun _ _ => Nat.zero_le _) (Finset.mem_univ c)
    simp only [Pi.single_eq_same]
    omega
  · have := Finset.add_le_sum (f := x) (fun _ _ => Nat.zero_le _) (Finset.mem_univ c)
      (Finset.mem_univ b) hc
    rw [Pi.single_eq_of_ne hc]
    omega

/-- A vector of height `1` is a unit vector. -/
theorem exists_eq_single_of_sum_eq_one {x : Fin d → ℕ} (hs : ∑ a, x a = 1) :
    ∃ b, x = Pi.single b 1 := by
  obtain ⟨b, -, hb⟩ := Finset.exists_ne_zero_of_sum_ne_zero (by omega : ∑ a, x a ≠ 0)
  exact ⟨b, eq_single_of_le_sum (by omega) hs.le⟩

theorem eq_zero_of_sum_eq_zero {x : Fin d → ℕ} (hs : ∑ a, x a = 0) : x = 0 := by
  funext c
  exact (Finset.sum_eq_zero_iff.1 hs) c (Finset.mem_univ c)

theorem sum_single_apply (b : Fin d) (k : ℕ) : ∑ a, (Pi.single b k : Fin d → ℕ) a = k := by
  rw [Finset.sum_pi_single']
  simp

/-- `|x - e_a| + 1 = |x|` when `x_a ≥ 1`. -/
theorem sum_sub_single_add_one {x : Fin d → ℕ} {a : Fin d} (ha : 1 ≤ x a) :
    ∑ c, (x - Pi.single a 1 : Fin d → ℕ) c + 1 = ∑ c, x c := by
  have h := sub_single_add_single (a := a) ha
  calc ∑ c, (x - Pi.single a 1 : Fin d → ℕ) c + 1
      = ∑ c, (x - Pi.single a 1 : Fin d → ℕ) c + ∑ c, (Pi.single a 1 : Fin d → ℕ) c := by
        rw [sum_single_apply]
    _ = ∑ c, (x - Pi.single a 1 + Pi.single a 1 : Fin d → ℕ) c := by
        rw [← Finset.sum_add_distrib]; rfl
    _ = ∑ c, x c := by rw [h]

theorem single_le_of_one_le {x : Fin d → ℕ} {a : Fin d} (ha : 1 ≤ x a) :
    (Pi.single a 1 : Fin d → ℕ) ≤ x := by
  intro c
  by_cases hc : c = a
  · subst hc; simpa using ha
  · simp [Pi.single_eq_of_ne hc]

theorem single_one_injective : Function.Injective (fun a : Fin d => (Pi.single a 1 : Fin d → ℕ)) := by
  intro a b h
  have := congrFun h a
  simp only [Pi.single_eq_same] at this
  by_contra hab
  rw [Pi.single_eq_of_ne hab] at this
  exact one_ne_zero this

/-- `tilePhi` is additive. -/
theorem tilePhi_add {m : ℕ} (p : Fin d → ZMod m) (x y : Fin d → ℕ) :
    tilePhi p (x + y) = tilePhi p x + tilePhi p y := by
  simp [tilePhi, add_mul, Finset.sum_add_distrib]

theorem tilePhi_zero {m : ℕ} (p : Fin d → ZMod m) : tilePhi p 0 = 0 := by
  simp [tilePhi]

theorem tilePhi_single {m : ℕ} (p : Fin d → ZMod m) (a : Fin d) (k : ℕ) :
    tilePhi p (Pi.single a k) = k * p a := by
  rw [tilePhi, Finset.sum_eq_single a]
  · simp
  · intro b _ hb; simp [Pi.single_eq_of_ne hb]
  · simp

/-- If `A ≡ B (mod m)` and `B < 2m`, then `B ≤ A + m·[m ≤ B]`. -/
theorem le_add_ite_of_mod_eq {A B m : ℕ} (h : A % m = B % m) (hB : B < 2 * m) :
    B ≤ A + if m ≤ B then m else 0 := by
  have h1 := Nat.mod_le A m
  split_ifs with hmB
  · have : B % m = B - m := by
      rw [Nat.mod_eq_sub_mod hmB, Nat.mod_eq_of_lt (by omega)]
    omega
  · rw [Nat.mod_eq_of_lt (by omega : B < m)] at h
    omega

variable {m : ℕ} {D : Finset (Fin d → ℕ)} {p : Fin d → ZMod m}

/-- In a down-set of height `≤ 2`, a unit `e_a` with `deg(a) = Σ_{e∈E} e_a ≠ 0` is a non-maximal
cell of `D`. -/
theorem single_mem_not_max_of_deg_ne_zero (hD : IsDownSetFin D) (a : Fin d)
    (hdeg : ∑ e ∈ D.filter (fun x => ∑ c, x c = 2), e a ≠ 0) :
    Pi.single a 1 ∈ D ∧ ¬ IsMaxCell D (Pi.single a 1) := by
  obtain ⟨e, he, hea⟩ := Finset.exists_ne_zero_of_sum_ne_zero hdeg
  obtain ⟨heD, he2⟩ := Finset.mem_filter.1 he
  have hea1 : 1 ≤ e a := by omega
  have hs := sum_sub_single_add_one hea1
  obtain ⟨b, hb⟩ := exists_eq_single_of_sum_eq_one (x := e - Pi.single a 1) (by omega)
  have hsplit := sub_single_add_single (a := a) hea1
  rw [hb] at hsplit
  refine ⟨hD e heD _ (single_le_of_one_le hea1), fun hmax => hmax b ?_⟩
  rw [add_comm, hsplit]
  exact heD

/-- `deg(a) = Σ_{e∈E} e_a ≤ d + 1` in a down-set of height `≤ 2`. -/
theorem deg_le (a : Fin d) :
    ∑ e ∈ D.filter (fun x => ∑ c, x c = 2), e a ≤ d + 1 := by
  set E := D.filter (fun x => ∑ c, x c = 2) with hE
  have hsplit : ∀ e ∈ E, e a = (if 1 ≤ e a then 1 else 0) + (if 2 ≤ e a then 1 else 0) := by
    intro e he
    have h2 := (Finset.mem_filter.1 he).2
    have := Finset.single_le_sum (f := e) (fun _ _ => Nat.zero_le _) (Finset.mem_univ a)
    split_ifs <;> omega
  rw [Finset.sum_congr rfl hsplit, Finset.sum_add_distrib, Finset.sum_boole, Finset.sum_boole,
    Nat.cast_id, Nat.cast_id]
  have hc1 : (E.filter (fun e => 1 ≤ e a)).card ≤ d := by
    calc (E.filter (fun e => 1 ≤ e a)).card
        ≤ (Finset.univ.image (fun b : Fin d => (Pi.single b 1 : Fin d → ℕ))).card := by
          refine Finset.card_le_card_of_injOn (fun e => e - Pi.single a 1) ?_ ?_
          · intro e he
            obtain ⟨he1, hea⟩ := Finset.mem_filter.1 (Finset.mem_coe.1 he)
            have h2 := (Finset.mem_filter.1 he1).2
            have hs := sum_sub_single_add_one hea
            obtain ⟨b, hb⟩ := exists_eq_single_of_sum_eq_one (x := e - Pi.single a 1) (by omega)
            exact Finset.mem_coe.2 (Finset.mem_image.2 ⟨b, Finset.mem_univ _, hb.symm⟩)
          · intro e1 he1 e2 he2 h
            have h1 := sub_single_add_single (a := a)
              (Finset.mem_filter.1 (Finset.mem_coe.1 he1)).2
            have h2 := sub_single_add_single (a := a)
              (Finset.mem_filter.1 (Finset.mem_coe.1 he2)).2
            simp only at h
            rw [← h1, ← h2, h]
      _ ≤ (Finset.univ : Finset (Fin d)).card := Finset.card_image_le
      _ = d := by simp
  have hc2 : (E.filter (fun e => 2 ≤ e a)).card ≤ 1 := by
    calc (E.filter (fun e => 2 ≤ e a)).card ≤ ({Pi.single a 2} : Finset (Fin d → ℕ)).card := by
          refine Finset.card_le_card fun e he => ?_
          obtain ⟨he1, hea⟩ := Finset.mem_filter.1 he
          have h2 := (Finset.mem_filter.1 he1).2
          exact Finset.mem_singleton.2 (eq_single_of_le_sum hea h2.le)
      _ = 1 := Finset.card_singleton _
  omega

/-- `|D| ≤ 1 + d + |E|` for a down-set of height `≤ 2` (only `0`, the `d` units, and `E`). -/
theorem card_le_of_height_le_two (hh : ∀ x ∈ D, ∑ a, x a ≤ 2) :
    D.card ≤ d + 1 + (D.filter (fun x => ∑ c, x c = 2)).card := by
  have hsub : D ⊆ insert 0 ((Finset.univ.image (fun b : Fin d => (Pi.single b 1 : Fin d → ℕ))) ∪
      D.filter (fun x => ∑ c, x c = 2)) := by
    intro x hx
    have hx2 := hh x hx
    rcases (by omega : ∑ a, x a = 0 ∨ ∑ a, x a = 1 ∨ ∑ a, x a = 2) with h0 | h1 | h2
    · exact Finset.mem_insert.2 (Or.inl (eq_zero_of_sum_eq_zero h0))
    · obtain ⟨b, hb⟩ := exists_eq_single_of_sum_eq_one h1
      exact Finset.mem_insert.2 (Or.inr (Finset.mem_union.2 (Or.inl
        (Finset.mem_image.2 ⟨b, Finset.mem_univ _, hb.symm⟩))))
    · exact Finset.mem_insert.2 (Or.inr (Finset.mem_union.2 (Or.inr
        (Finset.mem_filter.2 ⟨hx, h2⟩))))
  calc D.card ≤ _ := Finset.card_le_card hsub
    _ ≤ _ + 1 := Finset.card_insert_le _ _
    _ ≤ (Finset.univ.image (fun b : Fin d => (Pi.single b 1 : Fin d → ℕ))).card +
          (D.filter (fun x => ∑ c, x c = 2)).card + 1 := by
        gcongr; exact Finset.card_union_le _ _
    _ ≤ d + (D.filter (fun x => ∑ c, x c = 2)).card + 1 := by
        gcongr
        calc _ ≤ (Finset.univ : Finset (Fin d)).card := Finset.card_image_le
          _ = d := by simp
    _ = _ := by ring

/-- **Edge bound.** For a tile of height `≤ 2` and `r(x) = ⟨φ(x) - σ⟩`:
`Σ_{e∈E} r(e) ≤ (d + 1)·Σ_{z ∈ D non-maximal} r(z)`, `E = {x ∈ D : |x| = 2}`. -/
theorem sum_edges_le (hT : IsTile D p) (hh : ∀ x ∈ D, ∑ a, x a ≤ 2) (σ : ZMod m) :
    ∑ e ∈ D.filter (fun x => ∑ c, x c = 2), (tilePhi p e - σ).val ≤
      (d + 1) * ∑ z ∈ D.filter (fun z => ¬ IsMaxCell D z), (tilePhi p z - σ).val := by
  have hm := hT.pos
  have : NeZero m := ⟨hm.ne'⟩
  have hD := hT.1
  set r : (Fin d → ℕ) → ℕ := fun x => (tilePhi p x - σ).val with hr
  set E := D.filter (fun x => ∑ c, x c = 2) with hE
  have hrlt : ∀ x, r x < m := fun x => ZMod.val_lt _
  -- Trivial case: no cells of height 2.
  rcases E.eq_empty_or_nonempty with hE0 | ⟨e0, he0⟩
  · rw [hE0, Finset.sum_empty]; exact Nat.zero_le _
  -- `0` is a non-maximal cell.
  obtain ⟨he0D, he02⟩ := Finset.mem_filter.1 he0
  obtain ⟨a0, -, ha0⟩ := Finset.exists_ne_zero_of_sum_ne_zero (by omega : ∑ c, e0 c ≠ 0)
  have h0D : (0 : Fin d → ℕ) ∈ D := hD e0 he0D 0 (fun _ => Nat.zero_le _)
  have h0max : ¬ IsMaxCell D 0 := fun h =>
    h a0 (by rw [zero_add]; exact hD e0 he0D _ (single_le_of_one_le (by omega)))
  -- Per-edge inequality `r(e) + ρ₀ ≤ Σ_a e_a ρ_a + m·[m ≤ r(e) + ρ₀]`.
  have hedge : ∀ e ∈ E, r e + r 0 ≤ (∑ a, e a * r (Pi.single a 1)) +
      if m ≤ r e + r 0 then m else 0 := by
    intro e he
    have he2 := (Finset.mem_filter.1 he).2
    apply le_add_ite_of_mod_eq _ (by have := hrlt e; have := hrlt 0; omega)
    rw [← ZMod.natCast_eq_natCast_iff']
    have h2 : ((∑ c, e c : ℕ) : ZMod m) = 2 := by rw [he2]; norm_num
    simp only [hr, Nat.cast_sum, Nat.cast_mul, Nat.cast_add, ZMod.natCast_zmod_val, tilePhi_single,
      tilePhi_zero, Nat.cast_one, one_mul, mul_sub, Finset.sum_sub_distrib, ← Finset.sum_mul] at h2 ⊢
    rw [h2]
    simp only [tilePhi]
    ring
  -- Summing the per-edge inequalities.
  have hsum1 : ∑ e ∈ E, r e + E.card * r 0 ≤
      ∑ e ∈ E, ∑ a, e a * r (Pi.single a 1) + m * (E.filter (fun e => m ≤ r e + r 0)).card := by
    have := Finset.sum_le_sum hedge
    rw [Finset.sum_add_distrib, Finset.sum_add_distrib, Finset.sum_const, smul_eq_mul,
      ← Finset.sum_filter, Finset.sum_const, smul_eq_mul] at this
    linarith
  -- At most `ρ₀` edges wrap around.
  have hwrap : (E.filter (fun e => m ≤ r e + r 0)).card ≤ r 0 := by
    calc (E.filter (fun e => m ≤ r e + r 0)).card ≤ (Finset.Ico (m - r 0) m).card := by
          refine Finset.card_le_card_of_injOn r ?_ ?_
          · intro e he
            have he' := Finset.mem_filter.1 (Finset.mem_coe.1 he)
            have := hrlt e
            exact Finset.mem_coe.2 (Finset.mem_Ico.2 ⟨by omega, this⟩)
          · intro e1 he1 e2 he2 h
            exact hT.injOn_val σ
              (Finset.mem_filter.1 (Finset.mem_filter.1 (Finset.mem_coe.1 he1)).1).1
              (Finset.mem_filter.1 (Finset.mem_filter.1 (Finset.mem_coe.1 he2)).1).1 h
      _ = r 0 := by rw [Nat.card_Ico]; have := hrlt 0; omega
  -- Degree bound.
  set N := Finset.univ.filter
    (fun a : Fin d => Pi.single a 1 ∈ D ∧ ¬ IsMaxCell D (Pi.single a 1)) with hN
  have hdeg : ∑ e ∈ E, ∑ a, e a * r (Pi.single a 1) ≤ (d + 1) * ∑ a ∈ N, r (Pi.single a 1) := by
    rw [Finset.sum_comm, Finset.mul_sum, Finset.sum_filter]
    refine Finset.sum_le_sum fun a _ => ?_
    rw [← Finset.sum_mul]
    split_ifs with ha
    · exact Nat.mul_le_mul_right _ (deg_le a)
    · have : ∑ e ∈ E, e a = 0 := by
        by_contra h
        exact ha (single_mem_not_max_of_deg_ne_zero hD a h)
      rw [this, zero_mul]
  -- Card bound.
  have hcard : m ≤ d + 1 + E.card := by
    rw [← hT.2.1]; exact card_le_of_height_le_two hh
  -- Non-maximal cells contain `0` and the units of `N`.
  have hnonmax : r 0 + ∑ a ∈ N, r (Pi.single a 1) ≤
      ∑ z ∈ D.filter (fun z => ¬ IsMaxCell D z), r z := by
    have h0N : (0 : Fin d → ℕ) ∉ N.image (fun a => (Pi.single a 1 : Fin d → ℕ)) := by
      intro h
      obtain ⟨a, -, ha⟩ := Finset.mem_image.1 h
      have := congrFun ha a
      simp at this
    have hsub : insert 0 (N.image (fun a => (Pi.single a 1 : Fin d → ℕ))) ⊆
        D.filter (fun z => ¬ IsMaxCell D z) := by
      intro z hz
      rcases Finset.mem_insert.1 hz with rfl | hz
      · exact Finset.mem_filter.2 ⟨h0D, h0max⟩
      · obtain ⟨a, ha, rfl⟩ := Finset.mem_image.1 hz
        exact Finset.mem_filter.2 (Finset.mem_filter.1 ha).2
    calc r 0 + ∑ a ∈ N, r (Pi.single a 1)
        = ∑ z ∈ insert 0 (N.image (fun a => (Pi.single a 1 : Fin d → ℕ))), r z := by
          rw [Finset.sum_insert h0N, Finset.sum_image single_one_injective.injOn]
      _ ≤ _ := Finset.sum_le_sum_of_subset hsub
  -- Combine.
  have hA := Nat.mul_le_mul_left m hwrap
  have hB := Nat.mul_le_mul_right (r 0) hcard
  have hC := Nat.mul_le_mul_left (d + 1) hnonmax
  nlinarith

/-- **(B) Flat-MaxCL**: every tile of height `≤ 2` satisfies MaxCL. -/
theorem maxCLAt_of_height_le_two (hT : IsTile D p) (hh : ∀ x ∈ D, ∑ a, x a ≤ 2) :
    MaxCLAt D p := by
  intro σ
  set r : (Fin d → ℕ) → ℕ := fun x => (tilePhi p x - σ).val with hr
  have hstep : ∑ y ∈ D.filter (IsMaxCell D), (d + ∑ a, y a) * r y ≤
      ∑ y ∈ D.filter (IsMaxCell D), ((d + 1) * r y + if ∑ a, y a = 2 then r y else 0) := by
    refine Finset.sum_le_sum fun y hy => ?_
    have hy2 := hh y (Finset.mem_filter.1 hy).1
    split_ifs with h2
    · rw [h2]; ring_nf; exact le_rfl
    · have : d + ∑ a, y a ≤ d + 1 := by omega
      simpa using Nat.mul_le_mul_right (r y) this
  rw [Finset.sum_add_distrib, ← Finset.mul_sum, ← Finset.sum_filter] at hstep
  have hsub : (D.filter (IsMaxCell D)).filter (fun y => ∑ a, y a = 2) ⊆
      D.filter (fun x => ∑ c, x c = 2) := by
    intro y hy
    obtain ⟨hy1, hy2⟩ := Finset.mem_filter.1 hy
    exact Finset.mem_filter.2 ⟨(Finset.mem_filter.1 hy1).1, hy2⟩
  have hE := (Finset.sum_le_sum_of_subset (f := r) hsub).trans (sum_edges_le hT hh σ)
  have hsplit := Finset.sum_filter_add_sum_filter_not D (IsMaxCell D) r
  show ∑ y ∈ D.filter (IsMaxCell D), (d + ∑ a, y a) * r y ≤ (d + 1) * ∑ x ∈ D, r x
  rw [← hsplit, mul_add]
  linarith

end Flat

/-! ## (C) Wilf for numerical semigroups whose factorization tile has height `≤ 2` -/

/-- **(C)** If every cell of the (lex-least) factorization down-set `D` of `S` has height `≤ 2`,
then `S` satisfies Wilf's inequality `c ≤ e·ℓ`. -/
theorem wilf_of_factDownSet_height_le_two (S : NumericalSemigroup)
    (h : ∀ x ∈ S.factDownSet, ∑ a, x a ≤ 2) : S.conductor ≤ S.embDim * S.ell := by
  by_cases hS : S = nat
  · subst hS; exact wilf_nat
  · have hd : 1 ≤ S.primitives'.card := by
      have := card_primitives'_add_one (S := S)
      have := S.two_le_embDim hS
      omega
    exact wilf_of_tileTOPAt (tileTOPAt_of_maxCLAt hd isTile_factDownSet
      (maxCLAt_of_height_le_two isTile_factDownSet h))

/-! ## (D) General factorization tiles and graded-lex factorizations

The reduction `Tile-TOP'' ⇒ Wilf` (`wilf_of_tileTOPAt`) only uses that `D = S.factDownSet` is a
finite down-set on which `w` is a bijection onto `Ap(S,m)`. `IsFactTile S D` records exactly this,
and `wilf_of_tileTOPAt_of_isFactTile` is the reduction for any such `D`. The graded-lex
factorization set `S.factDownSetG` (`n_G(w)` = least factorization of `w` over `P'` for the order
"degree first, then lex", `grKey`) is such a `D`; its cells have minimal degree, so
`wilf_of_apery_height_le_two` needs only *some* factorization of height `≤ 2` of each Apéry element. -/

/-- `D` is a *factorization tile* of `S`: a finite down-set in `ℕ^{P'}` on which
`w(x) = Σ_a x_a p_a` is a bijection onto `Ap(S, m)`. -/
def IsFactTile (S : NumericalSemigroup) (D : Finset (Fin S.primitives'.card → ℕ)) : Prop :=
  IsDownSetFin D ∧ Set.BijOn S.wt (D : Set (Fin S.primitives'.card → ℕ))
    (S.aperySet S.multiplicity : Set ℕ)

namespace IsFactTile

variable {S : NumericalSemigroup} {D : Finset (Fin S.primitives'.card → ℕ)}

theorem image_wt (hD : IsFactTile S D) : D.image S.wt = S.aperySet S.multiplicity := by
  ext w
  constructor
  · intro h
    obtain ⟨x, hx, rfl⟩ := Finset.mem_image.1 h
    exact hD.2.1 hx
  · intro h
    obtain ⟨x, hx, rfl⟩ := hD.2.2.2 h
    exact Finset.mem_image_of_mem _ hx

theorem card_eq (hD : IsFactTile S D) : D.card = S.multiplicity := by
  rw [← card_aperySet (S := S) S.multiplicity_pos, ← hD.image_wt,
    Finset.card_image_of_injOn hD.2.2.1]

theorem sum_wt (hD : IsFactTile S D) :
    ∑ x ∈ D, (S.wt x : ℤ) = ∑ w ∈ S.aperySet S.multiplicity, (w : ℤ) := by
  rw [← hD.image_wt, Finset.sum_image hD.2.2.1]

theorem isApery_wt (hD : IsFactTile S D) {x : Fin S.primitives'.card → ℕ} (hx : x ∈ D) :
    S.IsApery S.multiplicity (S.wt x) :=
  (mem_aperySet S.multiplicity_mem S.multiplicity_pos).1 (hD.2.1 hx)

theorem wt_le_aperyMax (hD : IsFactTile S D) {x : Fin S.primitives'.card → ℕ} (hx : x ∈ D) :
    S.wt x ≤ S.aperyMax S.multiplicity :=
  le_aperyMax (hD.2.1 hx)

/-- A factorization tile is a tile for the residues `p_a mod m`. -/
theorem isTile (hD : IsFactTile S D) : IsTile D S.genMod := by
  have hm := S.multiplicity_pos
  refine IsTile.mk' hD.1 hD.card_eq ?_ ?_
  · intro x hx y hy h
    rw [tilePhi_genMod, tilePhi_genMod, ZMod.natCast_eq_natCast_iff'] at h
    exact hD.2.2.1 hx hy
      (IsApery.eq_of_mod_eq S.multiplicity_mem hm (hD.isApery_wt hx) (hD.isApery_wt hy) h)
  · intro s
    have : NeZero S.multiplicity := ⟨hm.ne'⟩
    obtain ⟨x, hx, hxw⟩ := hD.2.2.2
      ((mem_aperySet S.multiplicity_mem hm).2 (isApery_apery hm s.val))
    refine ⟨x, hx, ?_⟩
    rw [tilePhi_genMod, hxw, ← ZMod.natCast_mod, S.apery_mod hm, ZMod.natCast_mod,
      ZMod.natCast_zmod_val]

/-- Column identity CH' for any factorization tile `D`. -/
theorem columnIdentity (hD : IsFactTile S D) :
    ∑ a, ∑ x ∈ D.filter (fun x => x + Pi.single a 1 ∉ D),
        ((x a : ℤ) + 1) * ((S.aperyMax S.multiplicity : ℤ) - S.wt x) =
      S.multiplicity * S.wilfDefect +
        ((S.embDim : ℤ) - 1 - 1) * ((S.multiplicity * (S.multiplicity - 1) / 2 : ℕ) : ℤ) := by
  have hcol : ∀ a : Fin S.primitives'.card,
      ∑ x ∈ D.filter (fun x => x + Pi.single a 1 ∉ D),
          ((x a : ℤ) + 1) * ((S.aperyMax S.multiplicity : ℤ) - S.wt x) =
        (S.multiplicity : ℤ) * S.aperyMax S.multiplicity -
          ∑ x ∈ D, ((S.wt x : ℤ) + (S.gen a : ℤ) * x a) := by
    intro a
    have h1 := sum_wt_add_eq_columns hD.1 a S.gen
    have h2 := card_eq_sum_columns hD.1 a
    rw [hD.card_eq] at h2
    have h2' : (S.multiplicity : ℤ) =
        ∑ y ∈ D.filter (fun y => y + Pi.single a 1 ∉ D), ((y a : ℤ) + 1) := by
      rw [h2]; push_cast; rfl
    simp only [← wt_cast] at h1
    rw [h1, h2', Finset.sum_mul, ← Finset.sum_sub_distrib]
    refine Finset.sum_congr rfl fun y _ => ?_
    ring
  rw [Finset.sum_congr rfl fun a _ => hcol a, Finset.sum_sub_distrib, Finset.sum_const,
    Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
  have hswap : ∑ a : Fin S.primitives'.card,
      ∑ x ∈ D, ((S.wt x : ℤ) + (S.gen a : ℤ) * x a) =
      (S.primitives'.card : ℤ) * ∑ x ∈ D, (S.wt x : ℤ) + ∑ x ∈ D, (S.wt x : ℤ) := by
    rw [Finset.sum_comm]
    simp only [Finset.sum_add_distrib, Finset.sum_const, Finset.card_univ, Fintype.card_fin,
      nsmul_eq_mul, Finset.mul_sum]
    congr 1
    refine Finset.sum_congr rfl fun x _ => ?_
    rw [wt_cast]
    exact Finset.sum_congr rfl fun a _ => mul_comm _ _
  rw [hswap, hD.sum_wt]
  have h := dmM_sub_sum_apery (S := S)
  have hd' : (S.embDim : ℤ) - 1 = S.primitives'.card := by
    have := card_primitives'_add_one (S := S); omega
  rw [hd']
  linear_combination h

/-- Column bound in direction `a` for any factorization tile (as `tileTop_column_bound`). -/
theorem column_bound (hD : IsFactTile S D) (a : Fin S.primitives'.card) :
    (S.multiplicity : ℤ) * S.multiplicity -
        ∑ y ∈ D.filter (fun y => ∀ b, y + Pi.single b 1 ∉ D),
          ((y a : ℤ) + 1) * ((S.multiplicity : ℤ) -
            ((((S.aperyMax S.multiplicity : ℕ) : ZMod S.multiplicity) -
              tilePhi S.genMod y).val : ℕ)) ≤
      ∑ x ∈ D.filter (fun x => x + Pi.single a 1 ∉ D),
        ((x a : ℤ) + 1) * ((S.aperyMax S.multiplicity : ℤ) - S.wt x) := by
  have h2 := card_eq_sum_columns hD.1 a
  rw [hD.card_eq] at h2
  have hmm : (S.multiplicity : ℤ) * S.multiplicity =
      ∑ x ∈ D.filter (fun x => x + Pi.single a 1 ∉ D), ((x a : ℤ) + 1) * S.multiplicity := by
    have h2' : (S.multiplicity : ℤ) =
        ∑ x ∈ D.filter (fun x => x + Pi.single a 1 ∉ D), ((x a : ℤ) + 1) := by
      rw [h2]; push_cast; rfl
    rw [← Finset.sum_mul, ← h2']
  have hmax : D.filter (fun y => ∀ b, y + Pi.single b 1 ∉ D) =
      (D.filter (fun x => x + Pi.single a 1 ∉ D)).filter
        (fun y => ∀ b, y + Pi.single b 1 ∉ D) := by
    rw [Finset.filter_filter]
    exact Finset.filter_congr fun y _ => ⟨fun h => ⟨h a, h⟩, fun h => h.2⟩
  rw [hmax, Finset.sum_filter, hmm, ← Finset.sum_sub_distrib]
  refine Finset.sum_le_sum fun x hx => ?_
  have hxD := (Finset.mem_filter.1 hx).1
  have hpos : (0 : ℤ) ≤ (x a : ℤ) + 1 := by positivity
  split_ifs with hxmax
  · have hval : (((((S.aperyMax S.multiplicity : ℕ) : ZMod S.multiplicity) -
        tilePhi S.genMod x).val : ℕ) : ℤ) ≤ (S.aperyMax S.multiplicity : ℤ) - S.wt x := by
      rw [val_aperyMax_sub_tilePhi]
      have hM : (S.wt x : ℤ) ≤ S.aperyMax S.multiplicity := by
        exact_mod_cast hD.wt_le_aperyMax hxD
      exact emod_le_self_of_nonneg (by linarith) (by exact_mod_cast S.multiplicity_pos)
    have := mul_le_mul_of_nonneg_left hval hpos
    linarith
  · have hle : (S.multiplicity : ℤ) ≤ (S.aperyMax S.multiplicity : ℤ) - S.wt x := by
      obtain ⟨b, hb⟩ := not_forall_not.1 hxmax
      have h1 := hD.wt_le_aperyMax hb
      rw [wt_add, wt_single, one_mul] at h1
      have h2 := multiplicity_lt_of_mem_primitives' (gen_mem (S := S) b)
      omega
    have := mul_le_mul_of_nonneg_left hle hpos
    linarith

/-- Summing the column bounds (as `tileTop_sum_columns`, for any finset `D`). -/
theorem sum_columns_max (D : Finset (Fin S.primitives'.card → ℕ)) (s : ZMod S.multiplicity) :
    ∑ a : Fin S.primitives'.card,
        ∑ y ∈ D.filter (fun y => ∀ b, y + Pi.single b 1 ∉ D),
          ((y a : ℤ) + 1) * ((S.multiplicity : ℤ) - ((s - tilePhi S.genMod y).val : ℕ)) =
      ((∑ y ∈ D.filter (fun y => ∀ a, y + Pi.single a 1 ∉ D),
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

end IsFactTile

/-- **`Tile-TOP'' ⇒ Wilf` for any factorization tile** `D` of `S` (a finite down-set on which `w` is a
bijection onto `Ap(S,m)`); `wilf_of_tileTOPAt` is the case `D = S.factDownSet`. -/
theorem wilf_of_tileTOPAt_of_isFactTile {S : NumericalSemigroup}
    {D : Finset (Fin S.primitives'.card → ℕ)} (hD : IsFactTile S D)
    (h : TileTOPAt D S.genMod) : S.conductor ≤ S.embDim * S.ell := by
  have hm := S.multiplicity_pos
  have hmZ : (0 : ℤ) < S.multiplicity := by exact_mod_cast hm
  have hTOP := h ((S.aperyMax S.multiplicity : ℕ) : ZMod S.multiplicity)
  have hTOPZ : (2 : ℤ) * ((∑ y ∈ D.filter (fun y => ∀ a, y + Pi.single a 1 ∉ D),
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
  have hlow := Finset.sum_le_sum fun a (_ : a ∈ (Finset.univ : Finset (Fin S.primitives'.card))) =>
    hD.column_bound a
  rw [Finset.sum_sub_distrib, IsFactTile.sum_columns_max, Finset.sum_const, Finset.card_univ,
    Fintype.card_fin, nsmul_eq_mul] at hlow
  have hCH := hD.columnIdentity
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
      2 * ∑ a, ∑ x ∈ D.filter (fun x => x + Pi.single a 1 ∉ D),
        ((x a : ℤ) + 1) * ((S.aperyMax S.multiplicity : ℤ) - S.wt x) -
      ((S.primitives'.card : ℤ) - 1) * ((S.multiplicity : ℤ) * ((S.multiplicity : ℤ) - 1)) := by
    linear_combination (-2) * hCH - ((S.primitives'.card : ℤ) - 1) * hH
  have hW : 0 ≤ (S.multiplicity : ℤ) * S.wilfDefect := by linarith
  have hW' : 0 ≤ S.wilfDefect := nonneg_of_mul_nonneg_right hW hmZ
  rw [wilfDefect] at hW'
  have : (S.conductor : ℤ) ≤ S.embDim * S.ell := by linarith
  exact_mod_cast this

/-- The lex-least factorization down-set is a factorization tile. -/
theorem isFactTile_factDownSet (S : NumericalSemigroup) : IsFactTile S S.factDownSet := by
  refine ⟨isDownSetFin_factDownSet, ?_, ?_, ?_⟩
  · intro x hx
    exact (mem_aperySet S.multiplicity_mem S.multiplicity_pos).2
      (isApery_wt_of_mem (Finset.mem_coe.1 hx)).1
  · intro x hx y hy h
    rw [← (isApery_wt_of_mem (Finset.mem_coe.1 hx)).2, ← (isApery_wt_of_mem (Finset.mem_coe.1 hy)).2,
      h]
  · intro w hw
    have hw' := (mem_aperySet S.multiplicity_mem S.multiplicity_pos).1 (Finset.mem_coe.1 hw)
    exact ⟨S.nf w, Finset.mem_coe.2 (mem_factDownSet.2 ⟨w, hw', rfl⟩), wt_nf hw'⟩

/-- Wilf for any factorization tile of height `≤ 2`. -/
theorem wilf_of_isFactTile_height_le_two {S : NumericalSemigroup}
    {D : Finset (Fin S.primitives'.card → ℕ)} (hD : IsFactTile S D)
    (hh : ∀ x ∈ D, ∑ a, x a ≤ 2) : S.conductor ≤ S.embDim * S.ell := by
  by_cases hS : S = nat
  · subst hS; exact wilf_nat
  · have hd : 1 ≤ S.primitives'.card := by
      have := card_primitives'_add_one (S := S)
      have := S.two_le_embDim hS
      omega
    exact wilf_of_tileTOPAt_of_isFactTile hD
      (tileTOPAt_of_maxCLAt hd hD.isTile (maxCLAt_of_height_le_two hD.isTile hh))

/-! ### Graded-lex factorizations -/

section GrLex

variable {d : ℕ}

/-- Graded-lex key of `x ∈ ℕ^d`: degree `|x|` first, then the lexicographic order. -/
def grKey (x : Fin d → ℕ) : ℕ ×ₗ Lex (Fin d → ℕ) := toLex (∑ a, x a, toLex x)

theorem grKey_injective : Function.Injective (grKey (d := d)) := by
  intro x y h
  have := congrArg (fun k => (ofLex k).2) h
  simpa [grKey] using this

theorem grKey_le_iff {x y : Fin d → ℕ} :
    grKey x ≤ grKey y ↔ ∑ a, x a < ∑ a, y a ∨ (∑ a, x a = ∑ a, y a ∧ toLex x ≤ toLex y) :=
  Prod.Lex.toLex_le_toLex

theorem sum_le_of_grKey_le {x y : Fin d → ℕ} (h : grKey x ≤ grKey y) : ∑ a, x a ≤ ∑ a, y a := by
  rcases grKey_le_iff.1 h with h | ⟨h, -⟩ <;> omega

/-- The graded-lex order is a monomial order: it is compatible with addition. -/
theorem grKey_add_le {x y : Fin d → ℕ} (u : Fin d → ℕ) (h : grKey x ≤ grKey y) :
    grKey (x + u) ≤ grKey (y + u) := by
  rw [grKey_le_iff] at h ⊢
  simp only [Pi.add_apply, Finset.sum_add_distrib]
  rcases h with h | ⟨h1, h2⟩
  · left; omega
  · right
    refine ⟨by omega, ?_⟩
    rw [toLex_add, toLex_add]
    exact add_le_add_left h2 _

end GrLex

variable (S : NumericalSemigroup)

/-- `n_G(w)`: the graded-lex-least factorization of `w` over `P'` (junk `0` if there is none). -/
noncomputable def nfG (w : ℕ) : Fin S.primitives'.card → ℕ :=
  if h : (S.factSet w).Nonempty then Classical.choose ((S.factSet w).exists_min_image grKey h)
  else 0

/-- The graded-lex factorization down-set `D_G = {n_G(w) | w ∈ Ap(S,m)}`. -/
noncomputable def factDownSetG : Finset (Fin S.primitives'.card → ℕ) :=
  (S.aperySet S.multiplicity).image S.nfG

variable {S}

theorem nfG_spec {w : ℕ} (hw : S.IsApery S.multiplicity w) :
    S.wt (S.nfG w) = w ∧ ∀ x, S.wt x = w → grKey (S.nfG w) ≤ grKey x := by
  have hne : (S.factSet w).Nonempty := by
    obtain ⟨x, hx⟩ := exists_wt_eq hw
    exact ⟨x, mem_factSet.2 hx⟩
  unfold nfG
  rw [dif_pos hne]
  obtain ⟨hmem, hmin⟩ := Classical.choose_spec ((S.factSet w).exists_min_image grKey hne)
  exact ⟨mem_factSet.1 hmem, fun x hx => hmin x (mem_factSet.2 hx)⟩

theorem wt_nfG {w : ℕ} (hw : S.IsApery S.multiplicity w) : S.wt (S.nfG w) = w := (nfG_spec hw).1

/-- Down-set property of graded-lex-least factorizations (as `nf_downward`). -/
theorem nfG_downward {w : ℕ} (hw : S.IsApery S.multiplicity w) {y : Fin S.primitives'.card → ℕ}
    (hy : y ≤ S.nfG w) : S.IsApery S.multiplicity (S.wt y) ∧ S.nfG (S.wt y) = y := by
  have hxyu : y + (S.nfG w - y) = S.nfG w := by
    funext b
    have hb : y b ≤ S.nfG w b := hy b
    simp only [Pi.add_apply, Pi.sub_apply]
    omega
  generalize S.nfG w - y = u at hxyu
  have hwx : S.wt (S.nfG w) = w := wt_nfG hw
  generalize hx : S.nfG w = x at hxyu hwx
  have hAp : S.IsApery S.multiplicity (S.wt y) :=
    hw.of_add (wt_mem y) (wt_mem u) (by rw [← wt_add, hxyu, hwx])
  refine ⟨hAp, ?_⟩
  set z := S.nfG (S.wt y) with hz
  obtain ⟨hzw, hzmin⟩ := nfG_spec hAp
  have h1 : grKey z ≤ grKey y := hzmin y rfl
  have h2 : grKey x ≤ grKey (z + u) := by
    rw [← hx]; exact (nfG_spec hw).2 (z + u) (by rw [wt_add, hzw, ← wt_add, hxyu, hwx])
  have h3 : grKey (z + u) ≤ grKey (y + u) := grKey_add_le u h1
  rw [hxyu] at h3
  have h5 : z + u = y + u := by rw [hxyu]; exact grKey_injective (le_antisymm h3 h2)
  exact add_right_cancel h5

theorem mem_factDownSetG {x : Fin S.primitives'.card → ℕ} :
    x ∈ S.factDownSetG ↔ ∃ w, S.IsApery S.multiplicity w ∧ S.nfG w = x := by
  rw [factDownSetG, Finset.mem_image]
  constructor
  · rintro ⟨w, hw, rfl⟩
    exact ⟨w, (mem_aperySet S.multiplicity_mem S.multiplicity_pos).1 hw, rfl⟩
  · rintro ⟨w, hw, rfl⟩
    exact ⟨w, (mem_aperySet S.multiplicity_mem S.multiplicity_pos).2 hw, rfl⟩

/-- The graded-lex factorization down-set is a factorization tile. -/
theorem isFactTile_factDownSetG : IsFactTile S S.factDownSetG := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro x hx y hy
    obtain ⟨w, hw, rfl⟩ := mem_factDownSetG.1 hx
    obtain ⟨hAp, hnf⟩ := nfG_downward hw hy
    exact mem_factDownSetG.2 ⟨_, hAp, hnf⟩
  · intro x hx
    obtain ⟨w, hw, rfl⟩ := mem_factDownSetG.1 (Finset.mem_coe.1 hx)
    rw [wt_nfG hw]
    exact (mem_aperySet S.multiplicity_mem S.multiplicity_pos).2 hw
  · intro x hx y hy h
    obtain ⟨w1, hw1, rfl⟩ := mem_factDownSetG.1 (Finset.mem_coe.1 hx)
    obtain ⟨w2, hw2, rfl⟩ := mem_factDownSetG.1 (Finset.mem_coe.1 hy)
    rw [wt_nfG hw1, wt_nfG hw2] at h
    rw [h]
  · intro w hw
    have hw' := (mem_aperySet S.multiplicity_mem S.multiplicity_pos).1 (Finset.mem_coe.1 hw)
    exact ⟨S.nfG w, Finset.mem_coe.2 (mem_factDownSetG.2 ⟨w, hw', rfl⟩), wt_nfG hw'⟩

/-- **(D)** If every element of `Ap(S,m)` has *some* factorization over `P'` of length `≤ 2`, then
Wilf holds for `S` (via the graded-lex factorization tile, whose cells have minimal length). -/
theorem wilf_of_apery_height_le_two (S : NumericalSemigroup)
    (h : ∀ w ∈ S.aperySet S.multiplicity,
      ∃ x : Fin S.primitives'.card → ℕ, S.wt x = w ∧ ∑ a, x a ≤ 2) :
    S.conductor ≤ S.embDim * S.ell := by
  refine wilf_of_isFactTile_height_le_two isFactTile_factDownSetG fun x hx => ?_
  obtain ⟨w, hw, rfl⟩ := mem_factDownSetG.1 hx
  obtain ⟨x', hx'w, hx'2⟩ := h w ((mem_aperySet S.multiplicity_mem S.multiplicity_pos).2 hw)
  exact (sum_le_of_grKey_le ((nfG_spec hw).2 x' hx'w)).trans hx'2

end NumericalSemigroup
