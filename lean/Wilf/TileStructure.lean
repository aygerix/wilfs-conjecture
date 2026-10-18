import Wilf.ConeForest

/-!
# Structure of 3-D lattice tiles and HT for large tiles

Formalization of `.research/PROOFS.md`, "Cylinder structure of 3-D tiles" (parts (a)–(c);
Hellus–Rechenauer–Waldi, Prop 2.6) and "Cone tiles: wall and floor lemmas".
-/

namespace NumericalSemigroup

open Finset Function

-- The frame computations below call `simp` with one fixed list of direction facts on several goals.
set_option linter.unusedSimpArgs false
set_option linter.unnecessarySeqFocus false

namespace CornerArea

section TileStructure

/-! ### Minimal non-elements and their representatives (any dimension) -/

variable {d m : ℕ}

/-- `q` is a **minimal non-element** of `D`: `q ∉ D`, and `q − e_a ∈ D` whenever `q_a ≥ 1`. -/
def IsMinNon (D : Finset (Fin d → ℕ)) (q : Fin d → ℕ) : Prop :=
  q ∉ D ∧ ∀ a, 1 ≤ q a → q - Pi.single a 1 ∈ D

theorem sub_single_add {x : Fin d → ℕ} {a : Fin d} (ha : 1 ≤ x a) :
    x - Pi.single a 1 + Pi.single a 1 = x := by
  funext i
  by_cases hi : i = a
  · subst hi; simp; omega
  · simp [Pi.single_eq_of_ne hi]

theorem sub_single_le (x : Fin d → ℕ) (a : Fin d) : x - Pi.single a 1 ≤ x := fun i => by simp

theorem sub_single_inj {x y : Fin d → ℕ} {a : Fin d} (hx : 1 ≤ x a) (hy : 1 ≤ y a)
    (h : x - Pi.single a 1 = y - Pi.single a 1) : x = y := by
  rw [← sub_single_add hx, ← sub_single_add hy, h]

theorem tilePhi_sub_single (p : Fin d → ZMod m) {x : Fin d → ℕ} {a : Fin d} (ha : 1 ≤ x a) :
    tilePhi p (x - Pi.single a 1) = tilePhi p x - p a := by
  have h := tilePhi_add p (x - Pi.single a 1) (Pi.single a 1)
  rw [sub_single_add ha, tilePhi_single] at h
  rw [h]; simp

variable {D : Finset (Fin d → ℕ)} {p : Fin d → ZMod m}

theorem exists_rep (hT : IsTile D p) (s : ZMod m) : ∃ r ∈ D, tilePhi p r = s := by
  obtain ⟨r, hr, h⟩ := hT.2.2.surjOn (Set.mem_univ s)
  exact ⟨r, hr, h⟩

theorem IsTile.inj (hT : IsTile D p) {x y : Fin d → ℕ} (hx : x ∈ D) (hy : y ∈ D)
    (h : tilePhi p x = tilePhi p y) : x = y :=
  hT.2.2.injOn hx hy h

/-- **Cylinder lemma, first step.** The representative `r ∈ D` of the class of a minimal
non-element `q` (`φ(r) = φ(q)`, i.e. `r = q − λ` with `λ ∈ Λ = ker φ`) vanishes on the support of
`q`. -/
theorem rep_support (hT : IsTile D p) {q r : Fin d → ℕ} (hq : IsMinNon D q) (hr : r ∈ D)
    (hφ : tilePhi p r = tilePhi p q) {a : Fin d} (ha : 1 ≤ q a) : r a = 0 := by
  by_contra hra
  have hra' : 1 ≤ r a := by omega
  have h1 : r - Pi.single a 1 ∈ D := hT.1 _ hr _ (sub_single_le r a)
  have h2 := hq.2 a ha
  have heq : tilePhi p (r - Pi.single a 1) = tilePhi p (q - Pi.single a 1) := by
    rw [tilePhi_sub_single p hra', tilePhi_sub_single p ha, hφ]
  have := hT.inj h1 h2 heq
  rw [sub_single_inj hra' ha this] at hr
  exact hq.1 hr

/-- **Cylinder lemma (a), first half.** A full-support minimal non-element lies in `Λ = ker φ`. -/
theorem minNon_full_phi (hT : IsTile D p) {q : Fin d → ℕ} (hq : IsMinNon D q)
    (hfull : ∀ i, 1 ≤ q i) : tilePhi p q = 0 := by
  obtain ⟨r, hr, hφ⟩ := exists_rep hT (tilePhi p q)
  have : r = 0 := funext fun i => rep_support hT hq hr hφ (hfull i)
  rw [← hφ, this, tilePhi_zero]

/-- **Cylinder lemma (a), second half.** There is at most one full-support minimal non-element
(`d ≥ 1`). -/
theorem minNon_full_unique (hT : IsTile D p) (i₀ : Fin d) {q q' : Fin d → ℕ} (hq : IsMinNon D q)
    (hq' : IsMinNon D q') (hfull : ∀ i, 1 ≤ q i) (hfull' : ∀ i, 1 ≤ q' i) : q = q' := by
  have h1 := hq.2 i₀ (hfull i₀)
  have h2 := hq'.2 i₀ (hfull' i₀)
  have heq : tilePhi p (q - Pi.single i₀ 1) = tilePhi p (q' - Pi.single i₀ 1) := by
    rw [tilePhi_sub_single p (hfull i₀), tilePhi_sub_single p (hfull' i₀),
      minNon_full_phi hT hq hfull, minNon_full_phi hT hq' hfull']
  exact sub_single_inj (hfull i₀) (hfull' i₀) (hT.inj h1 h2 heq)

/-- **Cylinder lemma (b).** A minimal non-element `q` whose support contains every direction except
possibly `c` is congruent to `t·e_c` for some `t` with `t·e_c ∈ D`. -/
theorem minNon_face_rep (hT : IsTile D p) {q : Fin d → ℕ} (hq : IsMinNon D q) {c : Fin d}
    (hsupp : ∀ i, i ≠ c → 1 ≤ q i) : ∃ t, Pi.single c t ∈ D ∧ tilePhi p q = t * p c := by
  obtain ⟨r, hr, hφ⟩ := exists_rep hT (tilePhi p q)
  have key : Pi.single c (r c) = r := funext fun i => by
    by_cases hi : i = c
    · subst hi; simp
    · rw [Pi.single_eq_of_ne hi]; exact (rep_support hT hq hr hφ (hsupp i hi)).symm
  refine ⟨r c, by rw [key]; exact hr, ?_⟩
  rw [← hφ, ← tilePhi_single, key]

/-- **Cylinder lemma (b), distinctness.** Two minimal non-elements with a common direction `a` in
their supports and the same class are equal. -/
theorem minNon_class_unique (hT : IsTile D p) {q q' : Fin d → ℕ} (hq : IsMinNon D q)
    (hq' : IsMinNon D q') {a : Fin d} (ha : 1 ≤ q a) (ha' : 1 ≤ q' a)
    (h : tilePhi p q = tilePhi p q') : q = q' := by
  have heq : tilePhi p (q - Pi.single a 1) = tilePhi p (q' - Pi.single a 1) := by
    rw [tilePhi_sub_single p ha, tilePhi_sub_single p ha', h]
  exact sub_single_inj ha ha' (hT.inj (hq.2 a ha) (hq'.2 a ha') heq)

/-- Every non-element of a down-set lies above a minimal non-element. -/
theorem exists_minNon_le (hD : IsDownSetFin D) {x : Fin d → ℕ} (hx : x ∉ D) :
    ∃ q, IsMinNon D q ∧ q ≤ x := by
  let S := (Fintype.piFinset fun i => range (x i + 1)).filter (fun y => y ∉ D)
  have hxS : x ∈ S := mem_filter.2 ⟨Fintype.mem_piFinset.2 fun i => mem_range.2 (by omega), hx⟩
  obtain ⟨q, hqS, hmin⟩ := S.exists_min_image (fun y => ∑ i, y i) ⟨x, hxS⟩
  obtain ⟨hqbox, hqD⟩ := mem_filter.1 hqS
  have hqx : q ≤ x := fun i => by
    have := mem_range.1 (Fintype.mem_piFinset.1 hqbox i); omega
  refine ⟨q, ⟨hqD, fun a ha => ?_⟩, hqx⟩
  by_contra hn
  have hS : q - Pi.single a 1 ∈ S := mem_filter.2 ⟨Fintype.mem_piFinset.2 fun i => mem_range.2 (by
    have := hqx i; have := sub_single_le q a i; omega), hn⟩
  have h1 := hmin _ hS
  have h2 := congrArg (fun y : Fin d → ℕ => ∑ i, y i) (sub_single_add ha)
  simp only [Pi.add_apply, sum_add_distrib, sum_pi_single', mem_univ, if_true] at h2
  omega

end TileStructure

section TileStructure3

variable {m : ℕ} {D : Finset (Fin 3 → ℕ)} {p : Fin 3 → ZMod m}

/-! ### The cylinder of a 3-D down-set -/

/-- The cylinder of `D`: all `z` whose three coordinate projections `update z c 0` lie in `D`. For
a down-set `D`, `update z c 0 ∈ D` is the same as `π_c(z) ∈ π_c(D)` (`π_c(D) = D ∩ {x_c = 0}`).
The box only makes it a finset. -/
noncomputable def projCyl (D : Finset (Fin 3 → ℕ)) : Finset (Fin 3 → ℕ) :=
  (Fintype.piFinset fun _ => range (D.sup (fun x => ∑ i, x i) + 1)).filter
    (fun z => ∀ c, update z c 0 ∈ D)

theorem mem_projCyl {z : Fin 3 → ℕ} : z ∈ projCyl D ↔ ∀ c, update z c 0 ∈ D := by
  constructor
  · intro hz; exact (mem_filter.1 hz).2
  · intro hz
    refine mem_filter.2 ⟨Fintype.mem_piFinset.2 fun i => mem_range.2 ?_, hz⟩
    obtain ⟨c, hc⟩ : ∃ c : Fin 3, c ≠ i := by revert i; decide
    have h1 := le_sup (f := fun x : Fin 3 → ℕ => ∑ i, x i) (hz c)
    have h2 : (update z c 0) i ≤ ∑ j, (update z c 0) j :=
      single_le_sum (fun j _ => Nat.zero_le _) (mem_univ i)
    rw [update_of_ne (Ne.symm hc)] at h2
    simp only at h1
    omega

theorem update_le (z : Fin 3 → ℕ) (c : Fin 3) : update z c 0 ≤ z := fun i => by
  by_cases hi : i = c <;> simp [update_apply, hi]

/-- The cylinder of a down-set is a down-set determined by its projections. -/
theorem projCyl_isLW (hD : IsDownSetFin D) : IsLW (projCyl D) := by
  refine ⟨fun z hz y hy => ?_, fun z hz => ?_⟩
  · rw [mem_projCyl] at hz ⊢
    intro c
    exact hD _ (hz c) _ (fun i => by by_cases hi : i = c <;> simp [update_apply, hi, hy i])
  · rw [mem_projCyl]
    intro c
    have := mem_projCyl.1 (hz c) c
    rwa [update_idem] at this

/-! ### The cylinder lemma: 𝒞 or cone -/

/-- **Cylinder lemma (c), (c′).** A 3-D tile is either determined by its projections (no
full-support minimal non-element), or it has exactly one full-support minimal non-element `q`;
then `q ≥ (1,1,1)`, `q ∈ Λ` (`φ(q) = 0`) and `D = projCyl D ∖ (q + ℕ³)` is a cone set. -/
theorem tile_cases (hT : IsTile D p) :
    IsLW D ∨ ∃ q, IsMinNon D q ∧ (∀ i, 1 ≤ q i) ∧ tilePhi p q = 0 ∧ ConeSet (projCyl D) D q := by
  by_cases hex : ∃ q, IsMinNon D q ∧ ∀ i, 1 ≤ q i
  · obtain ⟨q, hq, hfull⟩ := hex
    right
    refine ⟨q, hq, hfull, minNon_full_phi hT hq hfull, projCyl_isLW hT.1, hfull, fun z => ?_⟩
    constructor
    · intro hz
      exact ⟨mem_projCyl.2 fun c => hT.1 _ hz _ (update_le z c),
        fun hle => hq.1 (hT.1 _ hz _ hle)⟩
    · rintro ⟨hz, hK⟩
      by_contra hn
      obtain ⟨q', hq', hle⟩ := exists_minNon_le hT.1 hn
      by_cases hf : ∀ i, 1 ≤ q' i
      · rw [minNon_full_unique hT 0 hq' hq hf hfull] at hle
        exact hK hle
      · push Not at hf
        obtain ⟨c, hc⟩ := hf
        apply hq'.1
        refine hT.1 _ (mem_projCyl.1 hz c) _ (fun i => ?_)
        by_cases hi : i = c
        · subst hi; simp; omega
        · simp [update_apply, hi]; exact hle i
  · left
    push Not at hex
    refine ⟨hT.1, fun z hz => ?_⟩
    by_contra hn
    obtain ⟨q', hq', hle⟩ := exists_minNon_le hT.1 hn
    obtain ⟨c, hc⟩ := hex q' hq'
    apply hq'.1
    refine hT.1 _ (hz c) _ (fun i => ?_)
    by_cases hi : i = c
    · subst hi; simp; omega
    · simp [update_apply, hi]; exact hle i

/-! ### Projection-determined sets are in class 𝒞 -/

theorem colHt_anti (hD : IsDownSetFin D) {x y : Fin 3 → ℕ} (hy : y ∈ D) (hle : x ≤ y)
    (a : Fin 3) : colHt D a y ≤ colHt D a x :=
  le_colHt (hD _ (colHt_spec (a := a) hy) _ (add_le_add_right hle _))

/-- A nonempty down-set determined by its projections is in class 𝒞, with `L₁ = |D ∩ ℕe₀|`,
`h(i)` the `e₁`-length of the base face over `i`, `F(i)` and `G(j)` the heights of the faces
`x₁ = 0` and `x₀ = 0`. -/
theorem lwClass_of_isLW (hLW : IsLW D) (hne : D.Nonempty) :
    LWClass D (colHt D 0 0 + 1) (fun i => colHt D 1 (Pi.single 0 i) + 1)
      (fun i => colHt D 2 (Pi.single 0 i) + 1) (fun j => colHt D 2 (Pi.single 1 j) + 1) := by
  have hD := hLW.1
  have h0 := zero_mem hD hne
  have he0 : ∀ i, i ≤ colHt D 0 0 → (Pi.single 0 i : Fin 3 → ℕ) ∈ D := fun i hi => by
    simpa using mem_of_le_colHt (a := 0) hD h0 hi
  have hp01 : ∀ i j, i ≤ colHt D 0 0 → j ≤ colHt D 1 (Pi.single 0 i) →
      (Pi.single 0 i + Pi.single 1 j : Fin 3 → ℕ) ∈ D := fun i j hi hj =>
    mem_of_le_colHt hD (he0 i hi) hj
  have he1 : ∀ j, j ≤ colHt D 1 (Pi.single 0 0) → (Pi.single 1 j : Fin 3 → ℕ) ∈ D := fun j hj => by
    simpa using hp01 0 j (Nat.zero_le _) hj
  have hsle : ∀ i i' : ℕ, i ≤ i' → ∀ a : Fin 3, (Pi.single a i : Fin 3 → ℕ) ≤ Pi.single a i' :=
    fun i i' h a k => by by_cases hk : k = a <;> simp [Pi.single_apply, hk, h]
  refine
    { one_le := by omega
      h_anti := fun i j hij hj => ?_
      F_anti := fun i j hij hj => ?_
      G_anti := fun i j hij hj => ?_
      h_pos := fun _ _ => by omega
      F_pos := fun _ _ => by omega
      G_pos := fun _ _ => by omega
      F_zero := by simp
      mem_iff := fun x => ?_ }
  · have := colHt_anti hD (he0 j (by omega)) (hsle i j hij 0) 1; omega
  · have := colHt_anti hD (he0 j (by omega)) (hsle i j hij 0) 2; omega
  · have h00 : (Pi.single 0 0 : Fin 3 → ℕ) = 0 := by simp
    have := colHt_anti hD (he1 j (by rw [h00] at hj ⊢; omega)) (hsle i j hij 1) 2; omega
  · have fr := frame012
    constructor
    · intro hx
      have l0 : (0 : Fin 3 → ℕ) + Pi.single 0 (x 0) ∈ D := hD _ hx _ (fr.le_iff.2 ⟨by simp,
        by simp, by simp⟩)
      have l1 : (Pi.single 0 (x 0) + Pi.single 1 (x 1) : Fin 3 → ℕ) ∈ D := hD _ hx _
        (fr.le_iff.2 ⟨by simp, by simp, by simp⟩)
      have l2 : (Pi.single 0 (x 0) + Pi.single 2 (x 2) : Fin 3 → ℕ) ∈ D := hD _ hx _
        (fr.le_iff.2 ⟨by simp, by simp, by simp⟩)
      have l3 : (Pi.single 1 (x 1) + Pi.single 2 (x 2) : Fin 3 → ℕ) ∈ D := hD _ hx _
        (fr.le_iff.2 ⟨by simp, by simp, by simp⟩)
      have := le_colHt l0
      have := le_colHt l1
      have := le_colHt l2
      have := le_colHt l3
      omega
    · rintro ⟨hx0, hx1, hx2⟩
      have hm0 := he0 (x 0) (by omega)
      have p2 : (Pi.single 0 (x 0) + Pi.single 1 (x 1) : Fin 3 → ℕ) ∈ D :=
        mem_of_le_colHt hD hm0 (by omega)
      have p1 : (Pi.single 0 (x 0) + Pi.single 2 (x 2) : Fin 3 → ℕ) ∈ D :=
        mem_of_le_colHt hD hm0 (by omega)
      have hm1 : (Pi.single 1 (x 1) : Fin 3 → ℕ) ∈ D := hD _ p2 _ (fr.le_iff.2 ⟨by simp, by simp,
        by simp⟩)
      have p0 : (Pi.single 1 (x 1) + Pi.single 2 (x 2) : Fin 3 → ℕ) ∈ D :=
        mem_of_le_colHt hD hm1 (by omega)
      apply hLW.mem_frame fr
      · convert p0 using 1
        funext i; fin_cases i <;> simp
      · convert p1 using 1
        funext i; fin_cases i <;> simp
      · convert p2 using 1
        funext i; fin_cases i <;> simp

end TileStructure3

end CornerArea

end NumericalSemigroup
