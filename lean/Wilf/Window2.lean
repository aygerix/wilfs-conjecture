import Wilf.MaxCL

/-!
# The depth-two window inequality (GW-16 and GW-17)

The combinatorial argument does not use residues. All divisions in GW-16 are natural-number
divisions, including on the empty down-set. The semigroup application uses the existing
lex-least factorization down-set.
-/

namespace NumericalSemigroup

open Finset

namespace Window2

variable {d : ℕ} {D : Finset (Fin d → ℕ)}

noncomputable def nonMax (D : Finset (Fin d → ℕ)) : Finset (Fin d → ℕ) :=
  D.filter (fun x => ¬ IsMaxCell D x)

noncomputable def terminal (D : Finset (Fin d → ℕ)) (A : Finset (Fin d)) :
    Finset (Fin d → ℕ) :=
  (nonMax D).filter (fun w => ∀ a, w + Pi.single a 1 ∈ D →
    IsMaxCell D (w + Pi.single a 1) ∧ a ∈ A)

/-- Nonzero cells all of whose lower covers belong to `terminal D A`. Such cells are maximal. -/
noncomputable def trapped (D : Finset (Fin d → ℕ)) (A : Finset (Fin d)) :
    Finset (Fin d → ℕ) :=
  (D.erase 0).filter (fun y => ∀ a, 0 < y a → y - Pi.single a 1 ∈ terminal D A)

def support (y : Fin d → ℕ) : Finset (Fin d) := univ.filter (fun a => 0 < y a)

theorem erase_zero_dim_zero (D : Finset (Fin 0 → ℕ)) : D.erase 0 = ∅ := by
  classical
  apply eq_empty_iff_forall_notMem.2
  intro x hx
  exact (mem_erase.1 hx).1 (Subsingleton.elim _ _)

theorem support_nonempty {y : Fin d → ℕ} (hy : y ≠ 0) : (support y).Nonempty := by
  classical
  by_contra h
  apply hy
  funext a
  have ha : a ∉ support y := fun ha => h ⟨a, ha⟩
  simp only [support, mem_filter, mem_univ, true_and, not_lt] at ha
  exact Nat.eq_zero_of_le_zero ha

theorem mem_nonMax_of_upper {w : Fin d → ℕ} {a : Fin d}
    (hD : IsDownSetFin D) (h : w + Pi.single a 1 ∈ D) : w ∈ nonMax D := by
  classical
  refine mem_filter.2 ⟨hD _ h _ (fun i => by simp), ?_⟩
  exact fun hm => hm a h

theorem trapped_max {A : Finset (Fin d)} {y : Fin d → ℕ}
    (hy : y ∈ trapped D A) : IsMaxCell D y := by
  classical
  have hy' := mem_filter.1 hy
  obtain ⟨a, ha⟩ := support_nonempty (mem_erase.1 hy'.1).1
  have ha' : 0 < y a := (mem_filter.1 ha).2
  have ht := (mem_filter.1 (hy'.2 a ha')).2 a
    (by rw [sub_single_add_single (a := a) ha']; exact (mem_erase.1 hy'.1).2)
  simpa only [sub_single_add_single (a := a) ha'] using ht.1

theorem max_eq_of_le (hD : IsDownSetFin D) {x y : Fin d → ℕ}
    (hx : IsMaxCell D x) (hy : y ∈ D) (hxy : x ≤ y) : x = y := by
  funext a
  by_contra hne
  have hle : x a ≤ y a := hxy a
  have ha : x a + 1 ≤ y a := by omega
  apply hx a
  apply hD _ hy
  intro b
  by_cases hb : b = a
  · subst hb; simpa using ha
  · simpa [Pi.single_eq_of_ne hb] using hxy b

/-- Routing every nonzero cell outside `trapped` to a lower cover outside `terminal`.
This is the subtraction-free cardinal version of Step 4. -/
theorem routing (hD : IsDownSetFin D) (A : Finset (Fin d)) :
    (D.erase 0).card ≤ d * (nonMax D \ terminal D A).card + (trapped D A).card := by
  classical
  by_cases hd : d = 0
  · subst d
    rw [erase_zero_dim_zero]
    simp
  have : Nonempty (Fin d) := ⟨⟨0, Nat.pos_of_ne_zero hd⟩⟩
  let X := D.erase 0 \ trapped D A
  have hex : ∀ x ∈ X, ∃ a : Fin d, 0 < x a ∧ x - Pi.single a 1 ∉ terminal D A := by
    intro x hx
    have hx' := mem_sdiff.1 hx
    by_contra h
    push Not at h
    exact hx'.2 (mem_filter.2 ⟨hx'.1, h⟩)
  let a : (Fin d → ℕ) → Fin d := fun x =>
    if hx : x ∈ X then (hex x hx).choose else Classical.arbitrary _
  have ha : ∀ x ∈ X, 0 < x (a x) ∧ x - Pi.single (a x) 1 ∉ terminal D A := by
    intro x hx
    simpa only [a, dif_pos hx] using (hex x hx).choose_spec
  have hc : X.card ≤ ((nonMax D \ terminal D A) ×ˢ (univ : Finset (Fin d))).card := by
    refine card_le_card_of_injOn (fun x => (x - Pi.single (a x) 1, a x)) ?_ ?_
    · intro x hx
      have hp := ha x hx
      have hxD := (mem_erase.1 (mem_sdiff.1 hx).1).2
      apply mem_product.2
      refine ⟨mem_sdiff.2 ⟨?_, hp.2⟩, mem_univ _⟩
      apply mem_nonMax_of_upper hD
      rwa [sub_single_add_single (a := a x) hp.1]
    · intro x hx y hy hxy
      have h1 := congrArg Prod.fst hxy
      have h2 := congrArg Prod.snd hxy
      have h3 := sub_single_add_single (a := a x) (ha x hx).1
      have h4 := sub_single_add_single (a := a y) (ha y hy).1
      dsimp only at h1 h2
      rw [← h3, ← h4, h1, h2]
  have ht : trapped D A ⊆ D.erase 0 := filter_subset _ _
  have hs := card_sdiff_add_card_eq_card ht
  simp only [card_product, card_univ, Fintype.card_fin] at hc
  dsimp only [X] at hc
  nlinarith

/-- Corner/lower-cover pairs, including the extra allowance for corners on an axis (Step 5). -/
theorem corner_count (hD : IsDownSetFin D) (A : Finset (Fin d)) :
    2 * (trapped D A).card ≤ A.card * (terminal D A).card + A.card := by
  classical
  by_cases hd : d = 0
  · subst d
    have he : trapped D A = ∅ := by
      unfold trapped
      rw [erase_zero_dim_zero]
      simp
    simp [he]
  have : Nonempty (Fin d) := ⟨⟨0, Nat.pos_of_ne_zero hd⟩⟩
  let Y := trapped D A
  let Y₁ := Y.filter (fun y => (support y).card = 1)
  have hpair : (∑ y ∈ Y, (support y).card) ≤ (terminal D A).card * A.card := by
    rw [← card_sigma]
    have hc : (Y.sigma support).card ≤ (terminal D A ×ˢ A).card := by
      refine card_le_card_of_injOn (fun p => (p.1 - Pi.single p.2 1, p.2)) ?_ ?_
      · rintro ⟨y, a⟩ hp
        obtain ⟨hy, ha⟩ := mem_sigma.1 hp
        have ha' := (mem_filter.1 ha).2
        have ht := (mem_filter.1 hy).2 a ha'
        refine mem_product.2 ⟨ht, ?_⟩
        have hu : y - Pi.single a 1 + Pi.single a 1 ∈ D := by
          rw [sub_single_add_single (a := a) ha']
          exact (mem_erase.1 (mem_filter.1 hy).1).2
        exact ((mem_filter.1 ht).2 a hu).2
      · rintro ⟨y, a⟩ hp ⟨z, b⟩ hq heq
        have h1 := congrArg Prod.fst heq
        have h2 := congrArg Prod.snd heq
        dsimp only at h1 h2
        subst b
        have ha := (mem_filter.1 (mem_sigma.1 hp).2).2
        have hb := (mem_filter.1 (mem_sigma.1 hq).2).2
        change 0 < y a at ha
        change 0 < z a at hb
        have hyz : y = z := by
          rw [← sub_single_add_single (a := a) ha,
            ← sub_single_add_single (a := a) hb, h1]
        subst z
        rfl
    simpa only [card_product] using hc
  have haxis : Y₁.card ≤ A.card := by
    have hex : ∀ y ∈ Y₁, ∃ a : Fin d, support y = {a} := by
      intro y hy
      exact card_eq_one.1 (mem_filter.1 hy).2
    let a : (Fin d → ℕ) → Fin d := fun y =>
      if hy : y ∈ Y₁ then (hex y hy).choose else Classical.arbitrary _
    have ha : ∀ y ∈ Y₁, support y = {a y} := by
      intro y hy
      simpa only [a, dif_pos hy] using (hex y hy).choose_spec
    have hpos : ∀ y ∈ Y₁, 0 < y (a y) := by
      intro y hy
      have : a y ∈ support y := by rw [ha y hy]; simp
      exact (mem_filter.1 this).2
    have hzero : ∀ y ∈ Y₁, ∀ b, b ≠ a y → y b = 0 := by
      intro y hy b hb
      have : b ∉ support y := by rw [ha y hy]; simpa using hb
      simp only [support, mem_filter, mem_univ, true_and, not_lt] at this
      omega
    refine card_le_card_of_injOn a ?_ ?_
    · intro y hy
      have hyY := (mem_filter.1 hy).1
      have ht := (mem_filter.1 hyY).2 (a y) (hpos y hy)
      exact ((mem_filter.1 ht).2 (a y) (by
        rw [sub_single_add_single (a := a y) (hpos y hy)]
        exact (mem_erase.1 (mem_filter.1 hyY).1).2)).2
    · intro y hy z hz heq
      have hyY := (mem_filter.1 hy).1
      have hzY := (mem_filter.1 hz).1
      have hyD := (mem_erase.1 (mem_filter.1 hyY).1).2
      have hzD := (mem_erase.1 (mem_filter.1 hzY).1).2
      rcases le_total (y (a y)) (z (a y)) with hle | hle
      · apply max_eq_of_le hD (trapped_max hyY) hzD
        intro b
        by_cases hb : b = a y
        · simpa [hb] using hle
        · rw [hzero y hy b hb]; exact Nat.zero_le _
      · symm
        apply max_eq_of_le hD (trapped_max hzY) hyD
        intro b
        by_cases hb : b = a y
        · simpa [hb] using hle
        · rw [hzero z hz b (by simpa only [← heq] using hb)]; exact Nat.zero_le _
  have htwo : 2 * Y.card ≤ (∑ y ∈ Y, (support y).card) + Y₁.card := by
    have h := sum_le_sum (s := Y) (fun y hy => show
        2 ≤ (support y).card + if (support y).card = 1 then 1 else 0 from by
      have hp := card_pos.2 (support_nonempty (mem_erase.1 (mem_filter.1 hy).1).1)
      split_ifs <;> omega)
    simpa [sum_add_distrib, Y₁, sum_boole, Nat.mul_comm] using h
  dsimp only [Y] at htwo haxis hpair
  nlinarith

/-- The key combinatorial inequality in subtraction-free form, valid even for empty `D`. -/
theorem counting (hD : IsDownSetFin D) (A : Finset (Fin d)) :
    2 * (D.erase 0).card + d * (terminal D A).card ≤
      2 * d * (nonMax D).card + A.card := by
  classical
  have hroute := routing hD A
  have hcorner := corner_count hD A
  have ht : terminal D A ⊆ nonMax D := filter_subset _ _
  have hsplit := card_sdiff_add_card_eq_card ht
  have hA : A.card ≤ d := by simpa using card_le_card (subset_univ A)
  have hmul := Nat.mul_le_mul_right (terminal D A).card hA
  nlinarith

def value (n : Fin d → ℕ) (x : Fin d → ℕ) : ℕ := ∑ a, x a * n a

theorem value_add (n : Fin d → ℕ) (x y : Fin d → ℕ) :
    value n (x + y) = value n x + value n y := by
  simp [value, Pi.add_apply, add_mul, sum_add_distrib]

theorem value_single (n : Fin d → ℕ) (a : Fin d) : value n (Pi.single a 1) = n a := by
  simp [value, Pi.single_apply]

theorem value_zero (n : Fin d → ℕ) : value n 0 = 0 := by simp [value]

noncomputable def small (D : Finset (Fin d → ℕ)) (n : Fin d → ℕ) : Finset (Fin d) :=
  univ.filter (fun a => Pi.single a 1 ∈ D ∧ n a < 2 * D.card)

theorem active_of_upper (hD : IsDownSetFin D) {w : Fin d → ℕ} {a : Fin d}
    (h : w + Pi.single a 1 ∈ D) : Pi.single a 1 ∈ D :=
  hD _ h _ (fun i => by simp)

theorem value_nonzero (hD : IsDownSetFin D) (n : Fin d → ℕ)
    (hn : ∀ a, Pi.single a 1 ∈ D → D.card ≤ n a)
    {x : Fin d → ℕ} (hx : x ∈ D) (hx0 : x ≠ 0) : D.card ≤ value n x := by
  classical
  obtain ⟨a, ha⟩ := support_nonempty hx0
  have ha' := (mem_filter.1 ha).2
  have hu := hD _ hx _ (single_le_of_one_le ha')
  have h1 := hn a hu
  have h2 := single_le_sum (f := fun b => x b * n b) (fun _ _ => Nat.zero_le _)
    (mem_univ a)
  have h3 := Nat.mul_le_mul_right (n a) ha'
  dsimp only [value]
  nlinarith

/-- Step 1, with no truncated subtraction: the left sum plus `|A|` is `2|D \ {0}|`. -/
theorem left_sum (hD : IsDownSetFin D) (n : Fin d → ℕ)
    (hn : ∀ a, Pi.single a 1 ∈ D → D.card ≤ n a) :
    (∑ x ∈ D, min 2 (value n x / D.card)) + (small D n).card = 2 * (D.erase 0).card := by
  classical
  let A := small D n
  let U := A.image (fun a => (Pi.single a 1 : Fin d → ℕ))
  have hU : U ⊆ D.erase 0 := by
    intro x hx
    obtain ⟨a, ha, rfl⟩ := mem_image.1 hx
    have ha' := (mem_filter.1 ha).2
    refine mem_erase.2 ⟨?_, ha'.1⟩
    intro h
    have := congrFun h a
    simp at this
  have hc : U.card = A.card := card_image_of_injOn single_one_injective.injOn
  have hterm : ∀ x ∈ D.erase 0,
      min 2 (value n x / D.card) + (if x ∈ U then 1 else 0) = 2 := by
    intro x hx
    obtain ⟨hx0, hxD⟩ := mem_erase.1 hx
    have hm : 0 < D.card := card_pos.2 ⟨x, hxD⟩
    have hv := value_nonzero hD n hn hxD hx0
    have hk1 : 1 ≤ value n x / D.card :=
      (Nat.le_div_iff_mul_le hm).2 (by omega)
    by_cases hxU : x ∈ U
    · obtain ⟨a, ha, rfl⟩ := mem_image.1 hxU
      have hlt : value n (Pi.single a 1) < 2 * D.card := by
        rw [value_single]; exact (mem_filter.1 ha).2.2
      have hk2 : value n (Pi.single a 1) / D.card < 2 :=
        (Nat.div_lt_iff_lt_mul hm).2 hlt
      simp only [if_pos hxU]
      omega
    · have hv2 : 2 * D.card ≤ value n x := by
        obtain ⟨a, ha⟩ := support_nonempty hx0
        have ha' := (mem_filter.1 ha).2
        have hpred : x - Pi.single a 1 ∈ D := hD _ hxD _ (fun i => Nat.sub_le _ _)
        have hsplit := sub_single_add_single (a := a) ha'
        have hval := congrArg (value n) hsplit
        rw [value_add, value_single] at hval
        change value n (x - Pi.single a 1) + n a = value n x at hval
        by_cases heq : x = Pi.single a 1
        · have hactive := hD _ hxD _ (single_le_of_one_le ha')
          have hna : 2 * D.card ≤ n a := by
            by_contra h
            apply hxU
            exact mem_image.2 ⟨a, mem_filter.2 ⟨mem_univ _, hactive, by omega⟩, heq.symm⟩
          simpa only [heq, value_single] using hna
        · have hp0 : x - Pi.single a 1 ≠ 0 := by
            intro hp
            rw [hp, zero_add] at hsplit
            exact heq hsplit.symm
          have hpv := value_nonzero hD n hn hpred hp0
          have hna := hn a (hD _ hxD _ (single_le_of_one_le ha'))
          omega
      have hk2 : 2 ≤ value n x / D.card := (Nat.le_div_iff_mul_le hm).2 hv2
      simp only [if_neg hxU]
      omega
  have hs := sum_congr rfl hterm
  have hf : (D.erase 0).filter (fun x => x ∈ U) = U := filter_mem_eq_inter |>.trans
    (inter_eq_right.mpr hU)
  simp only [sum_add_distrib, sum_boole, hf, sum_const, smul_eq_mul, hc, Nat.cast_id] at hs
  have hz : ∑ x ∈ D.erase 0, min 2 (value n x / D.card) =
      ∑ x ∈ D, min 2 (value n x / D.card) := by
    exact sum_erase D (by simp [value_zero])
  rw [hz] at hs
  simpa only [Nat.mul_comm, A] using hs

/-- Step 2: one layer on nonmaximal cells, and a second layer outside `terminal`. -/
theorem right_sum (hD : IsDownSetFin D) (n : Fin d → ℕ)
    (hn : ∀ a, Pi.single a 1 ∈ D → D.card ≤ n a) :
    2 * (nonMax D).card ≤
      (∑ x ∈ D, min 2 ((D.sup (value n) - value n x) / D.card)) +
        (terminal D (small D n)).card := by
  classical
  let A := small D n
  let f := fun x => min 2 ((D.sup (value n) - value n x) / D.card)
  have hterm : ∀ w ∈ nonMax D, 2 ≤ f w + if w ∈ terminal D A then 1 else 0 := by
    intro w hw
    have hw' := mem_filter.1 hw
    have hm : 0 < D.card := card_pos.2 ⟨w, hw'.1⟩
    have hex : ∃ a, w + Pi.single a 1 ∈ D := by
      by_contra h
      push Not at h
      exact hw'.2 h
    obtain ⟨a, ha⟩ := hex
    have hna := hn a (active_of_upper hD ha)
    have hmax := le_sup (f := value n) ha
    rw [value_add, value_single] at hmax
    have hk1 : 1 ≤ (D.sup (value n) - value n w) / D.card :=
      (Nat.le_div_iff_mul_le hm).2 (by omega)
    by_cases hwT : w ∈ terminal D A
    · simp only [if_pos hwT]
      dsimp only [f]
      omega
    · have hex' : ∃ a, w + Pi.single a 1 ∈ D ∧
          ¬ (IsMaxCell D (w + Pi.single a 1) ∧ a ∈ A) := by
        by_contra h
        push Not at h
        exact hwT (mem_filter.2 ⟨hw, h⟩)
      obtain ⟨b, hb, hbad⟩ := hex'
      have hnb := hn b (active_of_upper hD hb)
      have hv2 : value n w + 2 * D.card ≤ D.sup (value n) := by
        by_cases hbA : b ∈ A
        · have hnm : ¬ IsMaxCell D (w + Pi.single b 1) := fun h => hbad ⟨h, hbA⟩
          have hex'' : ∃ c, w + Pi.single b 1 + Pi.single c 1 ∈ D := by
            by_contra h; push Not at h; exact hnm h
          obtain ⟨c, hc⟩ := hex''
          have hnc := hn c (active_of_upper hD hc)
          have htop := le_sup (f := value n) hc
          simp only [value_add, value_single] at htop
          omega
        · have hnb2 : 2 * D.card ≤ n b := by
            by_contra h
            exact hbA (mem_filter.2 ⟨mem_univ _, active_of_upper hD hb, by omega⟩)
          have htop := le_sup (f := value n) hb
          rw [value_add, value_single] at htop
          omega
      have hk2 : 2 ≤ (D.sup (value n) - value n w) / D.card :=
        (Nat.le_div_iff_mul_le hm).2 (by omega)
      simp only [if_neg hwT]
      dsimp only [f]
      omega
  have hs := sum_le_sum hterm
  have ht : terminal D A ⊆ nonMax D := filter_subset _ _
  have hf : (nonMax D).filter (fun w => w ∈ terminal D A) = terminal D A :=
    filter_mem_eq_inter |>.trans (inter_eq_right.mpr ht)
  simp only [sum_add_distrib, sum_boole, hf, sum_const, smul_eq_mul, Nat.cast_id] at hs
  have hsub : ∑ w ∈ nonMax D, f w ≤ ∑ w ∈ D, f w :=
    sum_le_sum_of_subset (filter_subset _ _)
  dsimp only [A, f] at hs hsub
  omega

/-- A strengthening of GW-16: non-strict active weights `m ≤ n_a` already suffice. -/
theorem depth_two_of_le (D : Finset (Fin d → ℕ)) (hD : IsDownSetFin D) (n : Fin d → ℕ)
    (hn : ∀ a, Pi.single a 1 ∈ D → D.card ≤ n a) :
    (∑ x ∈ D, min 2 ((∑ a, x a * n a) / D.card)) ≤
      d * ∑ x ∈ D, min 2 ((D.sup (fun y => ∑ a, y a * n a) -
        (∑ a, x a * n a)) / D.card) := by
  have hleft := left_sum hD n hn
  have hright := right_sum hD n hn
  have hcount := counting hD (small D n)
  have hmul := Nat.mul_le_mul_left d hright
  change (∑ x ∈ D, min 2 (value n x / D.card)) ≤
    d * ∑ x ∈ D, min 2 ((D.sup (value n) - value n x) / D.card)
  nlinarith

/-- **GW-16**, exactly the requested natural-number statement, without nonemptiness or residues. -/
theorem depth_two (D : Finset (Fin d → ℕ)) (hD : IsDownSetFin D) (n : Fin d → ℕ)
    (hn : ∀ a, Pi.single a 1 ∈ D → D.card < n a) :
    (∑ x ∈ D, min 2 ((∑ a, x a * n a) / D.card)) ≤
      d * ∑ x ∈ D, min 2 ((D.sup (fun y => ∑ a, y a * n a) -
        (∑ a, x a * n a)) / D.card) :=
  depth_two_of_le D hD n (fun a ha => (hn a ha).le)

end Window2

namespace Window2

variable (S : NumericalSemigroup)

/-- Exact gap-prefix count on the Apéry set, for every integral multiple of the multiplicity. -/
theorem apery_gap_count (K : ℕ) :
    (∑ w ∈ S.aperySet S.multiplicity, min K (w / S.multiplicity)) =
      (S.gaps.filter (fun x => x < K * S.multiplicity)).card := by
  classical
  let m := S.multiplicity
  have hm : 0 < m := S.multiplicity_pos
  rw [sum_aperySet hm]
  symm
  rw [card_eq_sum_card_fiberwise (f := fun x => x % m) (t := range m)
    (fun x _ => mem_range.2 (Nat.mod_lt x hm))]
  apply sum_congr rfl
  intro i hi
  have hi' : i < m := mem_range.1 hi
  let w := S.apery m i
  have hwmod : w % m = i := by simp only [w, S.apery_mod hm, Nat.mod_eq_of_lt hi']
  have hwdecomp : w = i + m * (w / m) := by
    have := Nat.div_add_mod w m
    rw [hwmod] at this
    omega
  have hfib : (S.gaps.filter (fun x => x < K * m)).filter (fun x => x % m = i) =
      (range (min K (w / m))).map ⟨fun k => i + m * k, fun a b h => by
        exact Nat.eq_of_mul_eq_mul_left hm (by simpa only [Nat.add_left_cancel_iff] using h)⟩ := by
    ext x
    simp only [mem_filter, mem_gaps, mem_map, mem_range]
    rw [S.mem_iff_apery_le S.multiplicity_mem hm (x := x)]
    constructor
    · rintro ⟨⟨hlt, hN⟩, hxi⟩
      have hax : S.apery m x = w := by
        dsimp only [w]
        rw [← S.apery_mod_self m x, hxi]
      rw [hax] at hlt
      have hxdec := Nat.div_add_mod x m
      rw [hxi] at hxdec
      have hkK : x / m < K := (Nat.div_lt_iff_lt_mul hm).2 hN
      have hkw : x / m < w / m := by
        by_contra h
        have hle : w / m ≤ x / m := by omega
        have hmul := Nat.mul_le_mul_left m hle
        omega
      refine ⟨x / m, lt_min hkK hkw, ?_⟩
      change i + m * (x / m) = x
      omega
    · rintro ⟨k, hk, hkx⟩
      change i + m * k = x at hkx
      subst x
      have hmod : (i + m * k) % m = i := by
        rw [Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt hi']
      have hax : S.apery m (i + m * k) = w := by
        dsimp only [w]
        rw [← S.apery_mod_self m (i + m * k), hmod]
      have hkK := (lt_min_iff.1 hk).1
      have hkw := (lt_min_iff.1 hk).2
      have hmul1 := Nat.mul_lt_mul_of_pos_left hkw hm
      have hmul2 := Nat.mul_le_mul_left m (show k + 1 ≤ K by omega)
      refine ⟨⟨?_, ?_⟩, hmod⟩
      · rw [hax]
        omega
      · nlinarith
  rw [hfib, card_map, card_range]

/-- Arithmetic of the last `K` entries of an Apéry column; all endpoints are half-open. -/
theorem chain_window {m M c w k K : ℕ} (hm : 0 < m) (hM : M + 1 = c + m)
    (hw : w ≤ M) :
    (c - K * m ≤ w + m * k ∧ w + m * k < c) ↔
      (M - w) / m - K ≤ k ∧ k < (M - w) / m := by
  have hs : M - w + w = M := Nat.sub_add_cancel hw
  have htop : w + m * k < c ↔ k < (M - w) / m := by
    constructor
    · intro h
      have hmul : (k + 1) * m ≤ M - w := by nlinarith
      have hdiv := (Nat.le_div_iff_mul_le hm).2 hmul
      omega
    · intro h
      have hdiv : k + 1 ≤ (M - w) / m := by omega
      have hmul := (Nat.le_div_iff_mul_le hm).1 hdiv
      nlinarith
  have hbottom : c - K * m ≤ w + m * k ↔ (M - w) / m - K ≤ k := by
    constructor
    · intro h
      have hc : c ≤ w + m * k + K * m := (Nat.sub_le_iff_le_add).1 h
      have hlt : (M - w) / m < k + K + 1 :=
        (Nat.div_lt_iff_lt_mul hm).2 (by nlinarith)
      omega
    · intro h
      have hlt : (M - w) / m < k + K + 1 := by omega
      have hmul := (Nat.div_lt_iff_lt_mul hm).1 hlt
      apply (Nat.sub_le_iff_le_add).2
      nlinarith
  exact and_congr hbottom htop

/-- Exact terminal-window count on the Apéry set, also when `c < K*m` or `S = ℕ`. -/
theorem apery_left_count (K : ℕ) :
    (∑ w ∈ S.aperySet S.multiplicity,
      min K ((S.aperyMax S.multiplicity - w) / S.multiplicity)) =
      (S.left.filter (fun x => S.conductor - K * S.multiplicity ≤ x)).card := by
  classical
  let m := S.multiplicity
  let M := S.aperyMax m
  have hm : 0 < m := S.multiplicity_pos
  have hM : M + 1 = S.conductor + m := by
    change S.aperyMax S.multiplicity + 1 = S.conductor + S.multiplicity
    rw [S.aperyMax_eq S.multiplicity_mem S.multiplicity_pos]
    have := S.multiplicity_pos
    omega
  rw [sum_aperySet hm]
  symm
  rw [card_eq_sum_card_fiberwise (f := fun x => x % m) (t := range m)
    (fun x _ => mem_range.2 (Nat.mod_lt x hm))]
  apply sum_congr rfl
  intro i hi
  have hi' : i < m := mem_range.1 hi
  let w := S.apery m i
  let L := (M - w) / m
  have hwmod : w % m = i := by simp only [w, S.apery_mod hm, Nat.mod_eq_of_lt hi']
  have hwdecomp : w = i + m * (w / m) := by
    have := Nat.div_add_mod w m
    rw [hwmod] at this
    omega
  have hwM : w ≤ M := le_aperyMax (mem_image.2 ⟨i, hi, rfl⟩)
  have hfib : (S.left.filter (fun x => S.conductor - K * m ≤ x)).filter
      (fun x => x % m = i) =
      (Ico (L - K) L).map ⟨fun k => w + m * k, fun a b h => by
        exact Nat.eq_of_mul_eq_mul_left hm (by simpa only [Nat.add_left_cancel_iff] using h)⟩ := by
    ext x
    simp only [mem_filter, mem_left, mem_map, mem_Ico]
    constructor
    · rintro ⟨⟨⟨hxS, hxc⟩, hxlow⟩, hxi⟩
      have hax : S.apery m x = w := by
        dsimp only [w]
        rw [← S.apery_mod_self m x, hxi]
      have hle : w ≤ x := by
        rw [← hax]
        exact (S.mem_iff_apery_le S.multiplicity_mem hm).1 hxS
      have hq : w / m ≤ x / m := Nat.div_le_div_right hle
      have hxdec := Nat.div_add_mod x m
      rw [hxi] at hxdec
      have hqsum : x / m - w / m + w / m = x / m := Nat.sub_add_cancel hq
      have hmul := congrArg (fun t => m * t) hqsum
      simp only [mul_add] at hmul
      have hxrep : w + m * (x / m - w / m) = x := by omega
      have hwin := (chain_window (k := x / m - w / m) (K := K) hm hM hwM).1
        (by rw [hxrep]; exact ⟨hxlow, hxc⟩)
      exact ⟨x / m - w / m, hwin, hxrep⟩
    · rintro ⟨k, hk, hkx⟩
      change w + m * k = x at hkx
      subst x
      have hmod : (w + m * k) % m = i := by rw [Nat.add_mul_mod_self_left, hwmod]
      have hax : S.apery m (w + m * k) = w := by
        change S.apery m (w + m * k) = S.apery m i
        rw [← S.apery_mod_self m (w + m * k), hmod]
      have hwin := (chain_window (k := k) (K := K) hm hM hwM).2 hk
      refine ⟨⟨⟨?_, hwin.2⟩, hwin.1⟩, hmod⟩
      apply (S.mem_iff_apery_le S.multiplicity_mem hm).2
      rw [hax]
      omega
  rw [hfib, card_map, Nat.card_Ico]
  change L - (L - K) = min K L
  have hcount (l k : ℕ) : l - (l - k) = min k l := by omega
  exact hcount L K

/-- Reindex any sum on the existing minimal factorization tile by its Apéry weights. -/
theorem sum_fact (f : ℕ → ℕ) :
    (∑ x ∈ S.factDownSet, f (S.wt x)) = ∑ w ∈ S.aperySet S.multiplicity, f w := by
  rw [factDownSet, sum_image nf_injOn]
  apply sum_congr rfl
  intro w hw
  rw [wt_nf ((mem_aperySet S.multiplicity_mem S.multiplicity_pos).1 hw)]

theorem fact_sup : S.factDownSet.sup (value S.gen) = S.aperyMax S.multiplicity := by
  apply le_antisymm
  · apply Finset.sup_le
    intro x hx
    exact wt_le_aperyMax hx
  · unfold aperyMax
    apply Finset.sup_le
    intro w hw
    have hw' := (mem_aperySet S.multiplicity_mem S.multiplicity_pos).1 hw
    have hnf : S.nf w ∈ S.factDownSet := mem_factDownSet.2 ⟨w, hw', rfl⟩
    have h := le_sup (f := value S.gen) hnf
    change S.wt (S.nf w) ≤ S.factDownSet.sup (value S.gen) at h
    rwa [wt_nf hw'] at h

/-- The first required translation equality, on the library's actual factorization tile. -/
theorem tile_gap_count (K : ℕ) :
    (∑ x ∈ S.factDownSet, min K (S.wt x / S.multiplicity)) =
      (S.gaps.filter (fun x => x < K * S.multiplicity)).card :=
  (sum_fact S _).trans (apery_gap_count S K)

/-- The second required translation equality, on the library's actual factorization tile. -/
theorem tile_left_count (K : ℕ) :
    (∑ x ∈ S.factDownSet,
      min K ((S.aperyMax S.multiplicity - S.wt x) / S.multiplicity)) =
      (S.left.filter (fun x => S.conductor - K * S.multiplicity ≤ x)).card :=
  (sum_fact S _).trans (apery_left_count S K)

/-- **GW-17**, with the library's `gaps`, `left`, conductor, multiplicity and embedding dimension.
The natural lower endpoint `c - 2*m` implements intersection of the integer window with `ℕ`. -/
theorem semigroup_depth_two :
    (S.gaps.filter (fun x => x < 2 * S.multiplicity)).card ≤
      (S.embDim - 1) *
        (S.left.filter (fun x => S.conductor - 2 * S.multiplicity ≤ x)).card := by
  have h := depth_two S.factDownSet isDownSetFin_factDownSet S.gen (fun a _ => by
    rw [card_factDownSet]
    exact multiplicity_lt_of_mem_primitives' (gen_mem a))
  change (∑ x ∈ S.factDownSet, min 2 (S.wt x / S.factDownSet.card)) ≤
    S.primitives'.card * ∑ x ∈ S.factDownSet,
      min 2 ((S.factDownSet.sup (value S.gen) - S.wt x) / S.factDownSet.card) at h
  rw [card_factDownSet, fact_sup, tile_gap_count, tile_left_count] at h
  simpa only [card_primitives'] using h

/-- The last sentence of paper Step 1 needs the qualification `e_a ∈ D`.
For `D = {0}`, an inactive direction of weight zero is outside `A` but has `κ(e_a) = 0`. -/
theorem inactive_unit_counterexample :
    Pi.single (0 : Fin 1) 1 ∉ ({0} : Finset (Fin 1 → ℕ)) ∧
      (0 : Fin 1) ∉ small ({0} : Finset (Fin 1 → ℕ)) 0 ∧
      ¬ 2 ≤ value (0 : Fin 1 → ℕ) (Pi.single 0 1) /
        ({0} : Finset (Fin 1 → ℕ)).card := by
  have hunit : Pi.single (0 : Fin 1) 1 ∉ ({0} : Finset (Fin 1 → ℕ)) := by
    intro h
    have hcoord := congrFun (mem_singleton.1 h) (0 : Fin 1)
    simp at hcoord
  refine ⟨hunit, ?_, ?_⟩
  · intro h
    exact hunit (mem_filter.1 h).2.1
  · simp [value]

end Window2

end NumericalSemigroup
