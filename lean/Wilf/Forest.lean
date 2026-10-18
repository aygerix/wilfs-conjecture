import Wilf.CornerArea

/-!
# The three forest bounds of Theorem C-HT on the Loomis–Whitney class 𝒞

Formalization of `.research/PROOFS.md`, section "e = 4, asymptotic HT via the counting criterion
CHT": Lemmas TF, F, QF and the counting part of Theorem C-HT. Notation as in `Wilf.CornerArea`:
`maxSet` (`Max`, `t = |Max|`), `triSet` (`Tri`), `qSet` (`Q'`), `nTop`, `hsum` (`h`), `ht`, `colTop`.
New: `qU D = {x ∈ Q' : ∃ c, top_c x ∉ Max ∧ top_c x = x}` and `qO D = Q' ∖ qU D`.

The proofs work for every `D` with `IsLW D`: a down-set determined by its three coordinate
projections (`z ∈ D` as soon as `update z d 0 ∈ D` for all `d`). This hypothesis is symmetric
in the coordinates, which replaces the paper's "by symmetry" steps. Class 𝒞 implies it
(`LWClass.isLW`). Points are handled in a frame `(a, b, c)` of distinct directions (`Frame`, `pt`).

* `lemmaS` (Lemma S) and `share_top`: a maximal top shared by two cells all of whose `+e_d` lie in
  `D` is shared in one direction `a`, and the cells agree off `a`.
* `lemmaP` (Lemma P), stated with projections only.
* **Lemma TF** (`tripodForest`, `tripodForest'`, `tripodForest''`). Proved as an elimination order
  turned into an injection `Σ_{x ∈ Tri} N(x) → Max`, `(x, a) ↦ top_a x`, where `N(x)` is the set of
  tops not shared with a tripod of larger `|·|`; `|N(x)| ≥ 2` by Lemmas S and P, and `|N| = 3` at a
  tripod of maximal `|·|`.
* **Lemma QF** (`qOForest`): the same with `|·|` increasing; `qO_claim` is the paper's (1)/(2),
  stated with face points `pt a b c (x_a) 0 k`, `pt a b c 0 (x_b) k`, so that (1) and (2) clash
  (`qO_contra`).
* **Lemma F** (`qUForest`). Proved by an explicit injection `gU : qU → Max ∖ {y*}` instead of the
  paper's level-by-level acyclicity argument:
  - non-maximal direction 0: `x ↦ x + e₁`;
  - non-maximal direction 1: `x ↦ x + e₀`;
  - non-maximal direction 2: `x ↦ x + e₀` if `(0, x₁, x₂+1) ∈ D`, else `x ↦ x + e₁`.

  `y* = top₁(top₀(top₂ 0))` is never hit (`gU_ne_yStar`). Injectivity reduces to `gU_mixed`.
* `forestBound`: `2t + 2|Tri| + |qU| + |qO| + 3 ≤ 5t`; with `cht` (`chtForest`): `2m + 3 ≤ H + 5t`;
  with `typeBound` (`deltaBound`): `2m + 13 ≤ H + 5C`, i.e. `δ = H − (m − 1) ≥ m + 14 − 5C`.
-/

namespace NumericalSemigroup

open Finset Function

-- The frame computations below call `simp` with one fixed list of direction facts on several goals.
set_option linter.unusedSimpArgs false
set_option linter.unnecessarySeqFocus false

namespace CornerArea

section Forest

/-! ### Loomis–Whitney sets in symmetric form, frames -/

/-- `D` is a down-set determined by its three coordinate projections:
`z ∈ D` as soon as `update z d 0 ∈ D` for every direction `d`. -/
def IsLW (D : Finset (Fin 3 → ℕ)) : Prop :=
  IsDownSetFin D ∧ ∀ z : Fin 3 → ℕ, (∀ d, update z d 0 ∈ D) → z ∈ D

/-- Three pairwise distinct directions. -/
structure Frame (a b c : Fin 3) : Prop where
  hab : a ≠ b
  hac : a ≠ c
  hbc : b ≠ c

variable {a b c : Fin 3}

theorem Frame.swap (fr : Frame a b c) : Frame b a c := ⟨fr.hab.symm, fr.hbc, fr.hac⟩

theorem exists_third {a b : Fin 3} (h : a ≠ b) : ∃ c, a ≠ c ∧ b ≠ c := by
  revert a b; decide

theorem Frame.le_iff (fr : Frame a b c) {y z : Fin 3 → ℕ} :
    y ≤ z ↔ y a ≤ z a ∧ y b ≤ z b ∧ y c ≤ z c := by
  constructor
  · intro h; exact ⟨h a, h b, h c⟩
  · rintro ⟨h1, h2, h3⟩ i
    rcases fin3_cases fr.hab fr.hac fr.hbc i with rfl | rfl | rfl <;> assumption

theorem Frame.ext (fr : Frame a b c) {y z : Fin 3 → ℕ} (h1 : y a = z a) (h2 : y b = z b)
    (h3 : y c = z c) : y = z := by
  funext i
  rcases fin3_cases fr.hab fr.hac fr.hbc i with rfl | rfl | rfl <;> assumption

theorem Frame.sum (fr : Frame a b c) (z : Fin 3 → ℕ) : ∑ i, z i = z a + z b + z c := by
  obtain ⟨hab, hac, hbc⟩ := fr
  rw [Fin.sum_univ_three]
  fin_cases a <;> fin_cases b <;> fin_cases c <;> simp_all <;> omega

theorem sum_agree {x x' : Fin 3 → ℕ} {a : Fin 3} (h : ∀ i, i ≠ a → x i = x' i) :
    (∑ i, x i) + x' a = (∑ i, x' i) + x a := by
  have h1 := add_sum_erase univ x (mem_univ a)
  have h2 := add_sum_erase univ x' (mem_univ a)
  have h3 : ∑ i ∈ univ.erase a, x i = ∑ i ∈ univ.erase a, x' i :=
    sum_congr rfl fun i hi => h i (ne_of_mem_erase hi)
  omega

/-- The point with `a`-coordinate `u`, `b`-coordinate `w` and `c`-coordinate `k`. -/
def pt (a b c : Fin 3) (u w k : ℕ) : Fin 3 → ℕ := Pi.single a u + Pi.single b w + Pi.single c k

theorem Frame.pt_a (fr : Frame a b c) (u w k : ℕ) : pt a b c u w k a = u := by
  simp [pt, Pi.single_eq_of_ne fr.hab, Pi.single_eq_of_ne fr.hac]

theorem Frame.pt_b (fr : Frame a b c) (u w k : ℕ) : pt a b c u w k b = w := by
  simp [pt, Pi.single_eq_of_ne fr.hab.symm, Pi.single_eq_of_ne fr.hbc]

theorem Frame.pt_c (fr : Frame a b c) (u w k : ℕ) : pt a b c u w k c = k := by
  simp [pt, Pi.single_eq_of_ne fr.hac.symm, Pi.single_eq_of_ne fr.hbc.symm]

theorem pt_swap (a b c : Fin 3) (u w k : ℕ) : pt b a c w u k = pt a b c u w k := by
  simp only [pt]; abel

theorem Frame.pt_le (fr : Frame a b c) {u w k u' w' k' : ℕ} (h1 : u ≤ u') (h2 : w ≤ w')
    (h3 : k ≤ k') : pt a b c u w k ≤ pt a b c u' w' k' := by
  rw [fr.le_iff, fr.pt_a, fr.pt_b, fr.pt_c, fr.pt_a, fr.pt_b, fr.pt_c]
  exact ⟨h1, h2, h3⟩

variable {D : Finset (Fin 3 → ℕ)}

theorem IsLW.mem_frame (hLW : IsLW D) (fr : Frame a b c) {z : Fin 3 → ℕ}
    (ha : update z a 0 ∈ D) (hb : update z b 0 ∈ D) (hc : update z c 0 ∈ D) : z ∈ D := by
  refine hLW.2 z fun d => ?_
  rcases fin3_cases fr.hab fr.hac fr.hbc d with rfl | rfl | rfl <;> assumption

theorem IsLW.mem_of_le (hLW : IsLW D) {y z : Fin 3 → ℕ} (hz : z ∈ D) (h : y ≤ z) : y ∈ D :=
  hLW.1 z hz y h

/-! ### Column tops -/

theorem colTop_apply_self (x : Fin 3 → ℕ) (a : Fin 3) : colTop D a x a = x a + colHt D a x := by
  simp [colTop]

theorem colTop_apply_ne {x : Fin 3 → ℕ} {a i : Fin 3} (h : i ≠ a) : colTop D a x i = x i := by
  simp [colTop, Pi.single_eq_of_ne h]

theorem colTop_succ_not_mem (x : Fin 3 → ℕ) (a : Fin 3) : colTop D a x + Pi.single a 1 ∉ D := by
  intro h
  have h' : x + Pi.single a (colHt D a x + 1) ∈ D := by
    rw [Pi.single_add, ← add_assoc]; exact h
  have := le_colHt h'
  omega

theorem succ_mem_of_colTop_ne (hD : IsDownSetFin D) {x : Fin 3 → ℕ} (hx : x ∈ D) {a : Fin 3}
    (h : colTop D a x ≠ x) : x + Pi.single a 1 ∈ D := by
  apply mem_of_le_colHt hD hx
  by_contra h'
  apply h
  simp [colTop, show colHt D a x = 0 by omega]

theorem colTop_of_maxSet (hD : IsDownSetFin D) {x : Fin 3 → ℕ} (hx : x ∈ maxSet D) (a : Fin 3) :
    colTop D a x = x := by
  have hx' := mem_filter.1 hx
  by_contra h
  exact hx'.2 a (succ_mem_of_colTop_ne hD hx'.1 h)

theorem sum_add_single (x : Fin 3 → ℕ) (a : Fin 3) (s : ℕ) :
    ∑ i, (x + Pi.single a s : Fin 3 → ℕ) i = (∑ i, x i) + s := by
  simp only [Pi.add_apply, sum_add_distrib, sum_pi_single', mem_univ, if_true]

theorem maxSet_nonempty (hne : D.Nonempty) : (maxSet D).Nonempty := by
  obtain ⟨x, hx, hmax⟩ := D.exists_max_image (fun z => ∑ i, z i) hne
  refine ⟨x, mem_filter.2 ⟨hx, fun a h => ?_⟩⟩
  have := hmax _ h
  rw [sum_add_single] at this
  omega

/-! ### Structure of `Tri`, `Q'`, `qU`, `qO` -/

/-- `qU = {x ∈ Q' : the non-maximal top of `x` is `x` itself}`. -/
noncomputable def qU (D : Finset (Fin 3 → ℕ)) : Finset (Fin 3 → ℕ) :=
  (qSet D).filter (fun x => ∃ c, colTop D c x ∉ maxSet D ∧ colTop D c x = x)

/-- `qO = Q' ∖ qU`. -/
noncomputable def qO (D : Finset (Fin 3 → ℕ)) : Finset (Fin 3 → ℕ) := qSet D \ qU D

theorem qSet_dir {x : Fin 3 → ℕ} (hx : x ∈ qSet D) :
    ∃ c, colTop D c x ∉ maxSet D ∧ ∀ d, d ≠ c → colTop D d x ∈ maxSet D := by
  have hn := (mem_filter.1 hx).2.1
  have hsplit := card_filter_add_card_filter_not (s := (univ : Finset (Fin 3)))
    (fun a => colTop D a x ∈ maxSet D)
  rw [card_univ, Fintype.card_fin] at hsplit
  unfold nTop at hn
  have h1 : (univ.filter (fun a : Fin 3 => colTop D a x ∉ maxSet D)).card = 1 := by omega
  obtain ⟨c, hc⟩ := card_eq_one.1 h1
  have hcm : c ∈ univ.filter (fun a : Fin 3 => colTop D a x ∉ maxSet D) := by
    rw [hc]; exact mem_singleton_self c
  refine ⟨c, (mem_filter.1 hcm).2, fun d hd => ?_⟩
  by_contra hdm
  have : d ∈ univ.filter (fun a : Fin 3 => colTop D a x ∉ maxSet D) := mem_filter.2 ⟨mem_univ _, hdm⟩
  rw [hc, mem_singleton] at this
  exact hd this

theorem qSet_ht (hD : IsDownSetFin D) {x : Fin 3 → ℕ} (hx : x ∈ qSet D) {c : Fin 3}
    (hd : ∀ d, d ≠ c → colTop D d x ∈ maxSet D) : ht D (colTop D c x) = 1 := by
  have h1 := (mem_filter.1 hx).2.2
  unfold hsum at h1
  rwa [Finset.sum_eq_single_of_mem c (mem_univ c)
    (fun d _ hdc => ht_eq_zero_of_mem_maxSet (hd d hdc) hD)] at h1

/-- The definition of `qU` does not depend on how "the non-maximal top" is read: for `x ∈ Q'`
(on a down-set) the following are equivalent: some non-maximal top of `x` is `x`; every
non-maximal top of `x` is `x`; the top with `ht = 1` is `x`. -/
theorem qU_def_equiv (hD : IsDownSetFin D) {x : Fin 3 → ℕ} (hx : x ∈ qSet D) :
    ((∃ c, colTop D c x ∉ maxSet D ∧ colTop D c x = x) ↔
      (∀ c, colTop D c x ∉ maxSet D → colTop D c x = x)) ∧
    ((∃ c, colTop D c x ∉ maxSet D ∧ colTop D c x = x) ↔
      (∃ c, ht D (colTop D c x) = 1 ∧ colTop D c x = x)) := by
  obtain ⟨c₀, hc₀, hd₀⟩ := qSet_dir hx
  have huniq : ∀ c, colTop D c x ∉ maxSet D → c = c₀ := fun c hc => by
    by_contra h; exact hc (hd₀ c h)
  refine ⟨⟨fun ⟨c, hc, hcx⟩ c' hc' => ?_, fun h => ⟨c₀, hc₀, h c₀ hc₀⟩⟩,
    ⟨fun ⟨c, hc, hcx⟩ => ?_, fun ⟨c, hc, hcx⟩ => ⟨c, fun hm => ?_, hcx⟩⟩⟩
  · rw [huniq c' hc', ← huniq c hc]; exact hcx
  · obtain rfl := huniq c hc
    exact ⟨c, qSet_ht hD hx hd₀, hcx⟩
  · rw [ht_eq_zero_of_mem_maxSet hm hD] at hc
    exact absurd hc (by decide)

theorem qSet_not_max (hD : IsDownSetFin D) {x : Fin 3 → ℕ} (hx : x ∈ qSet D) : x ∉ maxSet D := by
  intro hm
  obtain ⟨c, hc, -⟩ := qSet_dir hx
  rw [colTop_of_maxSet hD hm] at hc
  exact hc hm

theorem qSet_succ_mem (hD : IsDownSetFin D) {x : Fin 3 → ℕ} (hx : x ∈ qSet D) {d : Fin 3}
    (hd : colTop D d x ∈ maxSet D) : x + Pi.single d 1 ∈ D :=
  succ_mem_of_colTop_ne hD (mem_filter.1 hx).1 (fun h => qSet_not_max hD hx (h ▸ hd))

theorem qO_succ_mem (hD : IsDownSetFin D) {x : Fin 3 → ℕ} (hx : x ∈ qO D) (d : Fin 3) :
    x + Pi.single d 1 ∈ D := by
  obtain ⟨hq, hnu⟩ := mem_sdiff.1 hx
  by_cases hd : colTop D d x ∈ maxSet D
  · exact qSet_succ_mem hD hq hd
  · exact succ_mem_of_colTop_ne hD (mem_filter.1 hq).1 (fun h => hnu (mem_filter.2 ⟨hq, d, hd, h⟩))

theorem triSet_top {x : Fin 3 → ℕ} (hx : x ∈ triSet D) (d : Fin 3) : colTop D d x ∈ maxSet D := by
  have hn := (mem_filter.1 hx).2
  unfold nTop at hn
  by_contra hd
  have hsub : univ.filter (fun a : Fin 3 => colTop D a x ∈ maxSet D) ⊆ univ.erase d :=
    fun a ha => mem_erase.2 ⟨fun h => hd (h ▸ (mem_filter.1 ha).2), mem_univ _⟩
  have := card_le_card hsub
  rw [card_erase_of_mem (mem_univ d), card_univ, Fintype.card_fin] at this
  omega

theorem triSet_succ_mem (hD : IsDownSetFin D) {x : Fin 3 → ℕ} (hx : x ∈ triSet D) (d : Fin 3) :
    x + Pi.single d 1 ∈ D := by
  have hx' := mem_sdiff.1 (mem_filter.1 hx).1
  exact succ_mem_of_colTop_ne hD hx'.1 (fun h => hx'.2 (h ▸ triSet_top hx d))

/-! ### Lemma S (sharing) and Lemma P (projection chain) -/

/-- **Lemma S.** If `top_a(x) = top_b(x') ∈ Max` with `a ≠ b` and `c` the third direction, then
`x + e_c` and `x' + e_c` cannot both lie in `D`. -/
theorem lemmaS (hLW : IsLW D) (fr : Frame a b c) {x x' : Fin 3 → ℕ}
    (hx : x + Pi.single c 1 ∈ D) (hx' : x' + Pi.single c 1 ∈ D)
    (h : colTop D a x = colTop D b x') (hy : colTop D a x ∈ maxSet D) : False := by
  have e1 : colTop D a x b = x b := colTop_apply_ne fr.hab.symm
  have e2 : colTop D a x c = x c := colTop_apply_ne fr.hac.symm
  have e3 : colTop D a x a = x' a := by rw [h]; exact colTop_apply_ne fr.hab
  have e4 : colTop D a x c = x' c := by rw [h]; exact colTop_apply_ne fr.hbc.symm
  have hyD := (mem_filter.1 hy).1
  apply (mem_filter.1 hy).2 c
  have hca := fr.hac.symm; have hcb := fr.hbc.symm; have hba := fr.hab.symm
  apply hLW.mem_frame fr
  · refine hLW.mem_of_le hx (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
      simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba, e1, e2]
  · refine hLW.mem_of_le hx' (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
      simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba, e3, e4]
  · refine hLW.mem_of_le hyD (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
      simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba]

/-- Consequence of Lemma S: a shared maximal top of two cells all of whose `+e_d` lie in `D` is
shared in the same direction `a`, and the two cells agree off `a`. -/
theorem share_top (hLW : IsLW D) {x x' : Fin 3 → ℕ} (hx : ∀ d, x + Pi.single d 1 ∈ D)
    (hx' : ∀ d, x' + Pi.single d 1 ∈ D) {a a' : Fin 3} (h : colTop D a x = colTop D a' x')
    (hy : colTop D a x ∈ maxSet D) : a = a' ∧ ∀ i, i ≠ a → x i = x' i := by
  have haa : a = a' := by
    by_contra hne
    obtain ⟨c, hac, ha'c⟩ := exists_third hne
    exact lemmaS hLW ⟨hne, hac, ha'c⟩ (hx c) (hx' c) h hy
  subst haa
  refine ⟨rfl, fun i hi => ?_⟩
  have := congrFun h i
  rwa [colTop_apply_ne hi, colTop_apply_ne hi] at this

/-- **Lemma P.** If `top_c(x), top_c(x') ∈ Max`, `x + e_a ∈ D`, `x' + e_b ∈ D`, then it is impossible
that `x_a < x'_a` and `x'_b < x_b`. -/
theorem lemmaP (hLW : IsLW D) (fr : Frame a b c) {x x' : Fin 3 → ℕ}
    (hy : colTop D c x ∈ maxSet D) (hy' : colTop D c x' ∈ maxSet D)
    (hxa : x + Pi.single a 1 ∈ D) (hxb : x' + Pi.single b 1 ∈ D) (h1 : x a < x' a)
    (h2 : x' b < x b) : False := by
  have ya : colTop D c x a = x a := colTop_apply_ne fr.hac
  have yb : colTop D c x b = x b := colTop_apply_ne fr.hbc
  have ya' : colTop D c x' a = x' a := colTop_apply_ne fr.hac
  have yb' : colTop D c x' b = x' b := colTop_apply_ne fr.hbc
  have hyD := (mem_filter.1 hy).1
  have hyD' := (mem_filter.1 hy').1
  have hca := fr.hac.symm; have hcb := fr.hbc.symm; have hba := fr.hab.symm
  have hP : update (colTop D c x + Pi.single a 1) b 0 ∉ D := by
    intro hP
    apply (mem_filter.1 hy).2 a
    apply hLW.mem_frame fr
    · refine hLW.mem_of_le hyD (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
        simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba]
    · exact hP
    · refine hLW.mem_of_le hxa (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
        simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba, ya, yb]
  have hP' : update (colTop D c x' + Pi.single b 1) a 0 ∉ D := by
    intro hP'
    apply (mem_filter.1 hy').2 b
    apply hLW.mem_frame fr
    · exact hP'
    · refine hLW.mem_of_le hyD' (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
        simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba]
    · refine hLW.mem_of_le hxb (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
        simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba, ya', yb']
  have hk1 : colTop D c x' c < colTop D c x c := by
    by_contra hle
    push Not at hle
    apply hP
    refine hLW.mem_of_le hyD' (fr.le_iff.2 ⟨?_, ?_, ?_⟩)
    · simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba, ya, ya']; omega
    · simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba]
    · simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba]; omega
  have hk2 : colTop D c x c < colTop D c x' c := by
    by_contra hle
    push Not at hle
    apply hP'
    refine hLW.mem_of_le hyD (fr.le_iff.2 ⟨?_, ?_, ?_⟩)
    · simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba]
    · simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba, yb, yb']; omega
    · simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba]; omega
  omega

/-! ### Lemma TF (tripod forest) -/

/-- Some `x' ∈ T` with `|x'| > |x|` has a top equal to `top_a x`. -/
def sharedAbove (D T : Finset (Fin 3 → ℕ)) (x : Fin 3 → ℕ) (a : Fin 3) : Prop :=
  ∃ x' ∈ T, (∑ i, x i) < (∑ i, x' i) ∧ ∃ b, colTop D b x' = colTop D a x

/-- Some `x' ∈ T` with `|x'| < |x|` has a top equal to `top_a x`. -/
def sharedBelow (D T : Finset (Fin 3 → ℕ)) (x : Fin 3 → ℕ) (a : Fin 3) : Prop :=
  ∃ x' ∈ T, (∑ i, x' i) < (∑ i, x i) ∧ ∃ b, colTop D b x' = colTop D a x

noncomputable instance (D T : Finset (Fin 3 → ℕ)) (x : Fin 3 → ℕ) :
    DecidablePred (sharedAbove D T x) := fun a => by unfold sharedAbove; infer_instance

noncomputable instance (D T : Finset (Fin 3 → ℕ)) (x : Fin 3 → ℕ) :
    DecidablePred (sharedBelow D T x) := fun a => by unfold sharedBelow; infer_instance

/-- At most one top of a tripod is shared with a tripod of larger `|·|` (Lemmas S and P). -/
theorem triSet_shared_le_one (hLW : IsLW D) {x : Fin 3 → ℕ} (hx : x ∈ triSet D) :
    (univ.filter (sharedAbove D (triSet D) x)).card ≤ 1 := by
  refine card_le_one.2 fun a ha b hb => ?_
  by_contra hab
  obtain ⟨c, hac, hbc⟩ := exists_third hab
  have fr : Frame a b c := ⟨hab, hac, hbc⟩
  obtain ⟨x', hx', hs', a', ht'⟩ := (mem_filter.1 ha).2
  obtain ⟨x'', hx'', hs'', b', ht''⟩ := (mem_filter.1 hb).2
  have hxs := triSet_succ_mem hLW.1 hx
  obtain ⟨-, hag'⟩ := share_top hLW hxs (triSet_succ_mem hLW.1 hx') ht'.symm (triSet_top hx a)
  obtain ⟨-, hag''⟩ := share_top hLW hxs (triSet_succ_mem hLW.1 hx'') ht''.symm (triSet_top hx b)
  have e' := sum_agree hag'
  have e'' := sum_agree hag''
  have h1 : x'' a < x' a := by rw [← hag'' a hab]; omega
  have h2 : x' b < x'' b := by rw [← hag' b (Ne.symm hab)]; omega
  exact lemmaP hLW fr (triSet_top hx'' c) (triSet_top hx' c) (triSet_succ_mem hLW.1 hx'' a)
    (triSet_succ_mem hLW.1 hx' b) h1 h2

/-- **Lemma TF (tripod forest), general form.** For `D` determined by its projections, if
`Tri ≠ ∅` then `2·|Tri| + 1 ≤ t`. -/
theorem tripodForest_of_isLW (hLW : IsLW D) (hT : (triSet D).Nonempty) :
    2 * (triSet D).card + 1 ≤ (maxSet D).card := by
  have hN : ∀ x ∈ triSet D, 2 ≤ (univ.filter (fun a => ¬ sharedAbove D (triSet D) x a)).card := by
    intro x hx
    have h1 := triSet_shared_le_one hLW hx
    have h2 := card_filter_add_card_filter_not (s := (univ : Finset (Fin 3)))
      (sharedAbove D (triSet D) x)
    rw [card_univ, Fintype.card_fin] at h2
    omega
  obtain ⟨x₀, hx₀, hmax⟩ := (triSet D).exists_max_image (fun x => ∑ i, x i) hT
  have hN0 : (univ.filter (fun a => ¬ sharedAbove D (triSet D) x₀ a)).card = 3 := by
    rw [filter_true_of_mem, card_univ, Fintype.card_fin]
    rintro a - ⟨x', hx', hlt, -⟩
    have := hmax x' hx'
    omega
  have hsum : 2 * (triSet D).card + 1 ≤
      ∑ x ∈ triSet D, (univ.filter (fun a => ¬ sharedAbove D (triSet D) x a)).card := by
    rw [← add_sum_erase _ _ hx₀, hN0]
    have h := sum_le_sum (s := (triSet D).erase x₀) fun x hx => hN x (mem_of_mem_erase hx)
    rw [sum_const, card_erase_of_mem hx₀, smul_eq_mul] at h
    have := card_pos.2 hT
    omega
  have hcard : ((triSet D).sigma (fun x => univ.filter (fun a => ¬ sharedAbove D (triSet D) x a))).card
      ≤ (maxSet D).card := by
    refine card_le_card_of_injOn (fun p => colTop D p.2 p.1) ?_ ?_
    · rintro ⟨x, a⟩ hp
      exact triSet_top (mem_sigma.1 hp).1 a
    · rintro ⟨x, a⟩ hp ⟨x', a'⟩ hp' heq
      have hx : x ∈ triSet D := (mem_sigma.1 hp).1
      have hx' : x' ∈ triSet D := (mem_sigma.1 hp').1
      have ha : a ∈ univ.filter (fun a => ¬ sharedAbove D (triSet D) x a) := (mem_sigma.1 hp).2
      have ha' : a' ∈ univ.filter (fun a => ¬ sharedAbove D (triSet D) x' a) := (mem_sigma.1 hp').2
      simp only at heq
      have hna := (mem_filter.1 ha).2
      have hna' := (mem_filter.1 ha').2
      rcases lt_trichotomy (∑ i, x i) (∑ i, x' i) with hlt | heq' | hgt
      · exact absurd ⟨x', hx', hlt, a', heq.symm⟩ hna
      · obtain ⟨rfl, hag⟩ := share_top hLW (triSet_succ_mem hLW.1 hx)
          (triSet_succ_mem hLW.1 hx') heq (triSet_top hx a)
        have e := sum_agree hag
        have : x = x' := funext fun i => by
          by_cases hi : i = a
          · rw [hi]; omega
          · exact hag i hi
        subst this; rfl
      · exact absurd ⟨x, hx, hgt, a, heq⟩ hna'
  rw [card_sigma] at hcard
  omega

/-- Lemma TF, unconditional form: `2·|Tri| ≤ t`. -/
theorem tripodForest_of_isLW' (hLW : IsLW D) : 2 * (triSet D).card ≤ (maxSet D).card := by
  rcases (triSet D).eq_empty_or_nonempty with h | h
  · rw [h, card_empty]; omega
  · have := tripodForest_of_isLW hLW h; omega

/-! ### Lemma QF (qO forest) -/

/-- **QF claim.** Let `x ∈ Q'` have non-maximal direction `c` and maximal direction `a` (with `b` the
third), and let `x' ∈ Q'` share `top_a x` and lie below `x` on the `a`-line. Then the `(a,c)`-face
is lower than the `(b,c)`-face at `(x_a, x_b)`: some level `k` has `(x_a, 0, k) ∉ D ∋ (0, x_b, k)`. -/
theorem qO_claim (hLW : IsLW D) (fr : Frame a b c) {x x' : Fin 3 → ℕ} (hx : x ∈ qSet D)
    (hxd : ∀ d, d ≠ c → colTop D d x ∈ maxSet D)
    (hx' : x' ∈ qSet D) (htop : colTop D a x' ∈ maxSet D)
    (hagree : ∀ i, i ≠ a → x' i = x i) (hlt : x' a < x a) :
    ∃ k, pt a b c (x a) 0 k ∉ D ∧ pt a b c 0 (x b) k ∈ D := by
  have hca := fr.hac.symm; have hcb := fr.hbc.symm; have hba := fr.hab.symm
  have hxD := (mem_filter.1 hx).1
  have hb' : x' b = x b := hagree b hba
  obtain ⟨c', hc'm, hd'⟩ := qSet_dir hx'
  rcases fin3_cases fr.hab fr.hac fr.hbc c' with h | h | h
  · rw [h] at hc'm; exact absurd htop hc'm
  · -- the non-maximal direction of `x'` is `b`, so `top_c x'` is maximal
    rw [h] at hd'
    have hy' := hd' c hcb
    have hy'D := (mem_filter.1 hy').1
    have ya : colTop D c x' a = x' a := colTop_apply_ne fr.hac
    have yb : colTop D c x' b = x' b := colTop_apply_ne fr.hbc
    refine ⟨colTop D c x' c, fun hP => ?_, ?_⟩
    · apply (mem_filter.1 hy').2 a
      apply hLW.mem_frame fr
      · refine hLW.mem_of_le hy'D (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
          simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba]
      · refine hLW.mem_of_le hP (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
          simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba, fr.pt_a,
            fr.pt_b, fr.pt_c, ya] <;> omega
      · refine hLW.mem_of_le hxD (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
          simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba, ya, yb] <;>
          omega
    · refine hLW.mem_of_le hy'D (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
        simp [fr.pt_a, fr.pt_b, fr.pt_c, yb] <;> omega
  · -- the non-maximal direction of `x'` is `c`: compare the two plateaus
    rw [h] at hd'
    have hht' := qSet_ht hLW.1 hx' hd'
    have hht := qSet_ht hLW.1 hx hxd
    have hyD : colTop D c x ∈ D := colTop_mem hxD
    have hy'D : colTop D c x' ∈ D := colTop_mem (mem_filter.1 hx').1
    have ya : colTop D c x a = x a := colTop_apply_ne fr.hac
    have yb : colTop D c x b = x b := colTop_apply_ne fr.hbc
    have ya' : colTop D c x' a = x' a := colTop_apply_ne fr.hac
    have yb' : colTop D c x' b = x' b := colTop_apply_ne fr.hbc
    have hk : colTop D c x c < colTop D c x' c := by
      by_contra hle
      push Not at hle
      obtain ⟨⟨z, hzD, hzy, hzeq⟩, -⟩ := ht_spec hyD
      have hle' : colTop D c x' ≤ colTop D c x := fr.le_iff.2 ⟨by omega, by omega, hle⟩
      have h2 := (ht_spec hy'D).2 z hzD (fun i => le_trans (hle' i) (hzy i))
      rw [hht', fr.sum z, fr.sum (colTop D c x')] at h2
      rw [hht, fr.sum z, fr.sum (colTop D c x)] at hzeq
      omega
    refine ⟨colTop D c x' c, fun hP => ?_, ?_⟩
    · have hw : update (colTop D c x) c (colTop D c x' c) ∈ D := by
        apply hLW.mem_frame fr
        · refine hLW.mem_of_le hy'D (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
            simp [update_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba, yb, yb'] <;> omega
        · refine hLW.mem_of_le hP (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
            simp [update_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba, ya, fr.pt_a, fr.pt_b,
              fr.pt_c]
        · refine hLW.mem_of_le hyD (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
            simp [update_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba]
      apply colTop_succ_not_mem (D := D) x c
      refine hLW.mem_of_le hw (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
        simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba] <;> omega
    · refine hLW.mem_of_le hy'D (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
        simp [fr.pt_a, fr.pt_b, fr.pt_c, yb'] <;> omega

/-- The two QF claims (for `a` and for `b`) are incompatible. -/
theorem qO_contra (hD : IsDownSetFin D) (fr : Frame a b c) {u w k₁ k₂ : ℕ}
    (h1 : pt a b c u 0 k₁ ∉ D) (h2 : pt a b c 0 w k₁ ∈ D)
    (h3 : pt b a c w 0 k₂ ∉ D) (h4 : pt b a c 0 u k₂ ∈ D) : False := by
  rw [pt_swap] at h3 h4
  rcases le_total k₁ k₂ with h | h
  · exact h1 (hD _ h4 _ (fr.pt_le le_rfl le_rfl h))
  · exact h3 (hD _ h2 _ (fr.pt_le le_rfl le_rfl h))

/-- At most one maximal top of a `qO` cell is shared with a `qO` cell of smaller `|·|`. -/
theorem qO_shared_le_one (hLW : IsLW D) {x : Fin 3 → ℕ} (hx : x ∈ qO D) :
    ((univ.filter (fun a => colTop D a x ∈ maxSet D)).filter (sharedBelow D (qO D) x)).card ≤ 1 := by
  refine card_le_one.2 fun a ha b hb => ?_
  by_contra hab
  obtain ⟨c, hac, hbc⟩ := exists_third hab
  have fr : Frame a b c := ⟨hab, hac, hbc⟩
  obtain ⟨ha1, x', hx', hs', a', ht'⟩ := mem_filter.1 ha
  obtain ⟨hb1, x'', hx'', hs'', b', ht''⟩ := mem_filter.1 hb
  have ham := (mem_filter.1 ha1).2
  have hbm := (mem_filter.1 hb1).2
  have hxq := (mem_sdiff.1 hx).1
  have hxs := qO_succ_mem hLW.1 hx
  obtain ⟨rfl, hag'⟩ := share_top hLW hxs (qO_succ_mem hLW.1 hx') ht'.symm ham
  obtain ⟨rfl, hag''⟩ := share_top hLW hxs (qO_succ_mem hLW.1 hx'') ht''.symm hbm
  obtain ⟨c₀, hc₀, hd₀⟩ := qSet_dir hxq
  have hc₀c : c₀ = c := by
    rcases fin3_cases fr.hab fr.hac fr.hbc c₀ with h | h | h
    · rw [h] at hc₀; exact absurd ham hc₀
    · rw [h] at hc₀; exact absurd hbm hc₀
    · exact h
  rw [hc₀c] at hd₀
  have e' := sum_agree hag'
  have e'' := sum_agree hag''
  obtain ⟨k₁, hk1, hk2⟩ := qO_claim hLW fr hxq hd₀ (mem_sdiff.1 hx').1 (ht' ▸ ham)
    (fun i hi => (hag' i hi).symm) (by omega)
  obtain ⟨k₂, hk3, hk4⟩ := qO_claim hLW fr.swap hxq hd₀ (mem_sdiff.1 hx'').1 (ht'' ▸ hbm)
    (fun i hi => (hag'' i hi).symm) (by omega)
  exact qO_contra hLW.1 fr hk1 hk2 hk3 hk4

/-- **Lemma QF (qO forest), general form.** `|qO| + 1 ≤ t` for nonempty `D` determined by its
projections. -/
theorem qOForest_of_isLW (hLW : IsLW D) (hne : D.Nonempty) : (qO D).card + 1 ≤ (maxSet D).card := by
  rcases (qO D).eq_empty_or_nonempty with hQ | hQ
  · rw [hQ, card_empty]; have := card_pos.2 (maxSet_nonempty hne); omega
  let N : (Fin 3 → ℕ) → Finset (Fin 3) := fun x =>
    (univ.filter (fun a => colTop D a x ∈ maxSet D)).filter (fun a => ¬ sharedBelow D (qO D) x a)
  have hmd : ∀ x ∈ qO D, (univ.filter (fun a => colTop D a x ∈ maxSet D)).card = 2 :=
    fun x hx => (mem_filter.1 (mem_sdiff.1 hx).1).2.1
  have hN : ∀ x ∈ qO D, 1 ≤ (N x).card := by
    intro x hx
    have h1 := qO_shared_le_one hLW hx
    have h2 := card_filter_add_card_filter_not
      (s := univ.filter (fun a => colTop D a x ∈ maxSet D)) (sharedBelow D (qO D) x)
    have := hmd x hx
    simp only [N]
    omega
  obtain ⟨x₀, hx₀, hmin⟩ := (qO D).exists_min_image (fun x => ∑ i, x i) hQ
  have hN0 : (N x₀).card = 2 := by
    simp only [N]
    rw [filter_true_of_mem, hmd x₀ hx₀]
    rintro a - ⟨x', hx', hlt, -⟩
    have := hmin x' hx'
    omega
  have hsum : (qO D).card + 1 ≤ ∑ x ∈ qO D, (N x).card := by
    rw [← add_sum_erase _ _ hx₀, hN0]
    have h := sum_le_sum (s := (qO D).erase x₀) fun x hx => hN x (mem_of_mem_erase hx)
    rw [sum_const, card_erase_of_mem hx₀, smul_eq_mul] at h
    have := card_pos.2 hQ
    omega
  have hcard : ((qO D).sigma N).card ≤ (maxSet D).card := by
    refine card_le_card_of_injOn (fun p => colTop D p.2 p.1) ?_ ?_
    · rintro ⟨x, a⟩ hp
      exact (mem_filter.1 (mem_filter.1 (mem_sigma.1 hp).2).1).2
    · rintro ⟨x, a⟩ hp ⟨x', a'⟩ hp' heq
      have hx : x ∈ qO D := (mem_sigma.1 hp).1
      have hx' : x' ∈ qO D := (mem_sigma.1 hp').1
      have ha : a ∈ N x := (mem_sigma.1 hp).2
      have ha' : a' ∈ N x' := (mem_sigma.1 hp').2
      simp only at heq
      have ham := (mem_filter.1 (mem_filter.1 ha).1).2
      have hna := (mem_filter.1 ha).2
      have hna' := (mem_filter.1 ha').2
      rcases lt_trichotomy (∑ i, x i) (∑ i, x' i) with hlt | heq' | hgt
      · exact absurd ⟨x, hx, hlt, a, heq⟩ hna'
      · obtain ⟨rfl, hag⟩ := share_top hLW (qO_succ_mem hLW.1 hx) (qO_succ_mem hLW.1 hx') heq ham
        have e := sum_agree hag
        have : x = x' := funext fun i => by
          by_cases hi : i = a
          · rw [hi]; omega
          · exact hag i hi
        subst this; rfl
      · exact absurd ⟨x', hx', hgt, a', heq.symm⟩ hna
  rw [card_sigma] at hcard
  omega

/-! ### Lemma F (qU forest) -/

/-- Structure of a `qU` cell with non-maximal direction `c`: `x + e_c ∉ D`, and `x + e_d ∈ Max`
for the two other directions (a farther maximal top would give `ht(x) ≥ 2`). -/
theorem qU_struct (hD : IsDownSetFin D) {x : Fin 3 → ℕ} (hx : x ∈ qU D) {c : Fin 3}
    (hd : ∀ d, d ≠ c → colTop D d x ∈ maxSet D) :
    x + Pi.single c 1 ∉ D ∧ ∀ d, d ≠ c → x + Pi.single d 1 ∈ maxSet D := by
  obtain ⟨hq, c₁, hc₁, hc₁x⟩ := mem_filter.1 hx
  have hcc : c₁ = c := by
    by_contra h; exact hc₁ (hd c₁ h)
  subst hcc
  have hxD := (mem_filter.1 hq).1
  have hht := qSet_ht hD hq hd
  rw [hc₁x] at hht
  refine ⟨fun h => ?_, fun d hdc => ?_⟩
  · have := colTop_succ_not_mem (D := D) x c₁
    rw [hc₁x] at this
    exact this h
  · have hne : colTop D d x ≠ x := fun h => qSet_not_max hD hq (h ▸ hd d hdc)
    have hs1 : 1 ≤ colHt D d x := by
      by_contra h1
      apply hne
      simp [colTop, show colHt D d x = 0 by omega]
    have hs2 : colHt D d x ≤ 1 := by
      by_contra h2
      push Not at h2
      have hm := mem_of_le_colHt hD hxD (show 2 ≤ colHt D d x by omega)
      have := (ht_spec hxD).2 _ hm (fun i => Nat.le_add_right _ _)
      rw [sum_add_single, hht] at this
      omega
    have : colTop D d x = x + Pi.single d 1 := by
      simp [colTop, le_antisymm hs2 hs1]
    rw [← this]
    exact hd d hdc

/-- The injection `qU → Max`: for non-maximal direction `0` use `x + e₁`, for `1` use `x + e₀`,
for `2` use `x + e₀` if `(0, x₁, x₂ + 1) ∈ D` and `x + e₁` otherwise. -/
noncomputable def gU (D : Finset (Fin 3 → ℕ)) (x : Fin 3 → ℕ) : Fin 3 → ℕ :=
  if colTop D 0 x ∈ maxSet D then
    (if colTop D 1 x ∈ maxSet D then
      (if update (x + Pi.single 2 1) 0 0 ∈ D then x + Pi.single 0 1 else x + Pi.single 1 1)
    else x + Pi.single 0 1)
  else x + Pi.single 1 1

theorem frame012 : Frame 0 1 2 := ⟨by decide, by decide, by decide⟩

theorem gU_spec (hD : IsDownSetFin D) {x : Fin 3 → ℕ} (hx : x ∈ qU D) :
    gU D x ∈ maxSet D ∧
    ((gU D x = x + Pi.single 1 1 ∧ (x + Pi.single 2 1 ∈ D ∨
        (x + Pi.single 0 1 ∈ D ∧ update (x + Pi.single 2 1) 0 0 ∉ D))) ∨
      (gU D x = x + Pi.single 0 1 ∧ update (x + Pi.single 2 1) 0 0 ∈ D)) := by
  obtain ⟨c, hc, hd⟩ := qSet_dir (mem_filter.1 hx).1
  have hs := qU_struct hD hx hd
  have hdir : ∀ c', colTop D c' x ∉ maxSet D → c' = c := fun c' h' => by
    by_contra h; exact h' (hd c' h)
  unfold gU
  have hc2 : colTop D 0 x ∈ maxSet D → colTop D 1 x ∈ maxSet D → c = 2 := fun h0 h1 => by
    rcases fin3_cases frame012.hab frame012.hac frame012.hbc c with h | h | h
    · rw [h] at hc; exact absurd h0 hc
    · rw [h] at hc; exact absurd h1 hc
    · exact h
  split_ifs with h0 h1 h2
  · obtain rfl := hc2 h0 h1
    exact ⟨hs.2 0 (by decide), Or.inr ⟨rfl, h2⟩⟩
  · obtain rfl := hc2 h0 h1
    exact ⟨hs.2 1 (by decide), Or.inl ⟨rfl, Or.inr ⟨(mem_filter.1 (hs.2 0 (by decide))).1, h2⟩⟩⟩
  · obtain rfl := hdir 1 h1
    refine ⟨hs.2 0 (by decide), Or.inr ⟨rfl, ?_⟩⟩
    exact hD _ (mem_filter.1 (hs.2 2 (by decide))).1 _ fun i => by
      simp only [update_apply]; split_ifs <;> simp
  · obtain rfl := hdir 0 h0
    exact ⟨hs.2 1 (by decide), Or.inl ⟨rfl, Or.inl (mem_filter.1 (hs.2 2 (by decide))).1⟩⟩

/-- No collision between an `x + e₁` image and an `x' + e₀` image. -/
theorem gU_mixed (hLW : IsLW D) {x x' : Fin 3 → ℕ}
    (h1 : x + Pi.single 2 1 ∈ D ∨ (x + Pi.single 0 1 ∈ D ∧ update (x + Pi.single 2 1) 0 0 ∉ D))
    (hy : x + Pi.single 1 1 ∈ maxSet D) (h0 : update (x' + Pi.single 2 1) 0 0 ∈ D)
    (heq : x + Pi.single 1 1 = x' + Pi.single 0 1) : False := by
  have e0 := congrFun heq 0
  have e1 := congrFun heq 1
  have e2 := congrFun heq 2
  simp [Pi.single_apply] at e0 e1 e2
  have fr := frame012
  rcases h1 with h1 | ⟨-, h1⟩
  · apply (mem_filter.1 hy).2 2
    apply hLW.mem_frame fr
    · refine hLW.mem_of_le h0 (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;> simp [update_apply, Pi.single_apply] <;>
        omega
    · refine hLW.mem_of_le h1 (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;> simp [update_apply, Pi.single_apply]
    · refine hLW.mem_of_le (mem_filter.1 hy).1 (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
        simp [update_apply, Pi.single_apply]
  · apply h1
    refine hLW.mem_of_le h0 (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;> simp [update_apply, Pi.single_apply] <;>
      omega

theorem gU_injOn (hLW : IsLW D) : Set.InjOn (gU D) (qU D : Set (Fin 3 → ℕ)) := by
  intro x hx x' hx' heq
  obtain ⟨hm, h | h⟩ := gU_spec hLW.1 hx <;> obtain ⟨hm', h' | h'⟩ := gU_spec hLW.1 hx'
  · rw [h.1, h'.1] at heq; exact add_right_cancel heq
  · rw [h.1, h'.1] at heq; exact (gU_mixed hLW h.2 (h.1 ▸ hm) h'.2 heq).elim
  · rw [h.1, h'.1] at heq; exact (gU_mixed hLW h'.2 (h'.1 ▸ hm') h.2 heq.symm).elim
  · rw [h.1, h'.1] at heq; exact add_right_cancel heq

/-- The maximal cell `y* = top₁(top₀(top₂ 0))` (the last corner of the top slice). -/
noncomputable def yStar (D : Finset (Fin 3 → ℕ)) : Fin 3 → ℕ :=
  colTop D 1 (colTop D 0 (colTop D 2 0))

theorem yStar_coords :
    (colTop D 2 (0 : Fin 3 → ℕ)) 0 = 0 ∧ (colTop D 2 (0 : Fin 3 → ℕ)) 1 = 0 ∧
    (colTop D 0 (colTop D 2 0)) 1 = 0 ∧
    (colTop D 0 (colTop D 2 0)) 2 = (colTop D 2 (0 : Fin 3 → ℕ)) 2 ∧
    yStar D 0 = (colTop D 0 (colTop D 2 0)) 0 ∧ yStar D 2 = (colTop D 2 (0 : Fin 3 → ℕ)) 2 := by
  have h20 : (0 : Fin 3) ≠ 2 := by decide
  have h21 : (1 : Fin 3) ≠ 2 := by decide
  have h10 : (1 : Fin 3) ≠ 0 := by decide
  have h01 : (0 : Fin 3) ≠ 1 := by decide
  have h20' : (2 : Fin 3) ≠ 0 := by decide
  have h21' : (2 : Fin 3) ≠ 1 := by decide
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · rw [colTop_apply_ne h20]; rfl
  · rw [colTop_apply_ne h21]; rfl
  · rw [colTop_apply_ne h10, colTop_apply_ne h21]; rfl
  · rw [colTop_apply_ne h20']
  · unfold yStar; rw [colTop_apply_ne h01]
  · unfold yStar; rw [colTop_apply_ne h21', colTop_apply_ne h20']

theorem yStar_mem (hLW : IsLW D) (hne : D.Nonempty) : yStar D ∈ maxSet D := by
  have h0 := zero_mem hLW.1 hne
  obtain ⟨w0, w1, u1, u2, ys0, ys2⟩ := yStar_coords (D := D)
  have fr := frame012
  refine mem_filter.2 ⟨colTop_mem (colTop_mem (colTop_mem h0)), fun d => ?_⟩
  fin_cases d
  · intro h
    apply colTop_succ_not_mem (D := D) (colTop D 2 0) 0
    refine hLW.mem_of_le h (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;> simp [Pi.single_apply, u1] <;> omega
  · exact colTop_succ_not_mem (D := D) _ 1
  · intro h
    apply colTop_succ_not_mem (D := D) (0 : Fin 3 → ℕ) 2
    refine hLW.mem_of_le h (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;> simp [Pi.single_apply, w0, w1] <;>
      omega

theorem gU_ne_yStar (hLW : IsLW D) {x : Fin 3 → ℕ} (hx : x ∈ qU D) : gU D x ≠ yStar D := by
  obtain ⟨w0, w1, u1, u2, ys0, ys2⟩ := yStar_coords (D := D)
  have fr := frame012
  intro heq
  obtain ⟨-, ⟨hg, h | ⟨h, -⟩⟩ | ⟨hg, h⟩⟩ := gU_spec hLW.1 hx
  · rw [hg] at heq
    have e2 := congrFun heq 2
    simp [Pi.single_apply] at e2
    apply colTop_succ_not_mem (D := D) (0 : Fin 3 → ℕ) 2
    refine hLW.mem_of_le h (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;> simp [Pi.single_apply, w0, w1] <;>
      omega
  · rw [hg] at heq
    have e0 := congrFun heq 0
    have e2 := congrFun heq 2
    simp [Pi.single_apply] at e0 e2
    apply colTop_succ_not_mem (D := D) (colTop D 2 0) 0
    refine hLW.mem_of_le h (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;> simp [Pi.single_apply, u1] <;> omega
  · rw [hg] at heq
    have e2 := congrFun heq 2
    simp [Pi.single_apply] at e2
    apply colTop_succ_not_mem (D := D) (0 : Fin 3 → ℕ) 2
    refine hLW.mem_of_le h (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
      simp [update_apply, Pi.single_apply, w0, w1] <;> omega

/-- **Lemma F (qU forest), general form.** `|qU| + 1 ≤ t` for nonempty `D` determined by its
projections. -/
theorem qUForest_of_isLW (hLW : IsLW D) (hne : D.Nonempty) : (qU D).card + 1 ≤ (maxSet D).card := by
  have hys := yStar_mem hLW hne
  have h := card_le_card_of_injOn (gU D) (s := qU D) (t := (maxSet D).erase (yStar D))
    (fun x hx => mem_erase.2 ⟨gU_ne_yStar hLW hx, (gU_spec hLW.1 hx).1⟩) (gU_injOn hLW)
  rw [card_erase_of_mem hys] at h
  have := card_pos.2 ⟨_, hys⟩
  omega

/-! ### On the Loomis–Whitney class 𝒞 -/

/-- Every set of class 𝒞 is a down-set determined by its three projections. -/
theorem LWClass.isLW {L₁ : ℕ} {h F G : ℕ → ℕ} (hC : LWClass D L₁ h F G) : IsLW D := by
  refine ⟨fun x hx y hy => ?_, fun z hz => ?_⟩
  · rw [hC.mem_iff] at hx ⊢
    have h0 : y 0 ≤ x 0 := hy 0
    have h1 : y 1 ≤ x 1 := hy 1
    have h2 : y 2 ≤ x 2 := hy 2
    have e1 := hC.h_anti (y 0) (x 0) h0 hx.1
    have e2 := hC.F_anti (y 0) (x 0) h0 hx.1
    have e3 := hC.h_anti 0 (x 0) (Nat.zero_le _) hx.1
    have e4 := hC.G_anti (y 1) (x 1) h1 (by omega)
    omega
  · have h0 := hz 0
    have h1 := hz 1
    have h2 := hz 2
    rw [hC.mem_iff] at h0 h1 h2 ⊢
    simp [update_apply] at h0 h1 h2
    omega

theorem LWClass.nonempty {L₁ : ℕ} {h F G : ℕ → ℕ} (hC : LWClass D L₁ h F G) : D.Nonempty := by
  refine ⟨0, ?_⟩
  rw [hC.mem_iff]
  have := hC.one_le
  have := hC.h_pos 0 (by omega)
  have := hC.F_pos 0 (by omega)
  have := hC.G_pos 0 (by omega)
  simp only [Pi.zero_apply]
  omega

variable {L₁ : ℕ} {h F G : ℕ → ℕ}

/-- **Lemma TF (tripod forest; 𝒞).** If `Tri ≠ ∅` then `2·|Tri| + 1 ≤ t`. -/
theorem tripodForest (hC : LWClass D L₁ h F G) (hT : (triSet D).Nonempty) :
    2 * (triSet D).card + 1 ≤ (maxSet D).card :=
  tripodForest_of_isLW hC.isLW hT

/-- **Lemma TF**, unconditional form `2·|Tri| ≤ t`. -/
theorem tripodForest' (hC : LWClass D L₁ h F G) : 2 * (triSet D).card ≤ (maxSet D).card :=
  tripodForest_of_isLW' hC.isLW

/-- On 𝒞 (where `t ≥ 1`), `2·|Tri| + 1 ≤ t` holds also when `Tri = ∅`. -/
theorem tripodForest'' (hC : LWClass D L₁ h F G) : 2 * (triSet D).card + 1 ≤ (maxSet D).card := by
  rcases (triSet D).eq_empty_or_nonempty with hT | hT
  · rw [hT, card_empty]
    have := card_pos.2 (maxSet_nonempty hC.nonempty)
    omega
  · exact tripodForest hC hT

/-- **Lemma F (qU forest; 𝒞).** `|qU| ≤ t − 1`, i.e. `|qU| + 1 ≤ t`. -/
theorem qUForest (hC : LWClass D L₁ h F G) : (qU D).card + 1 ≤ (maxSet D).card :=
  qUForest_of_isLW hC.isLW hC.nonempty

/-- **Lemma QF (qO forest; 𝒞).** `|qO| ≤ t − 1`, i.e. `|qO| + 1 ≤ t`. -/
theorem qOForest (hC : LWClass D L₁ h F G) : (qO D).card + 1 ≤ (maxSet D).card :=
  qOForest_of_isLW hC.isLW hC.nonempty

/-- `|qU| + |qO| = |Q'|`. -/
theorem card_qU_add_card_qO (D : Finset (Fin 3 → ℕ)) :
    (qU D).card + (qO D).card = (qSet D).card := by
  rw [add_comm]
  exact card_sdiff_add_card_eq_card (filter_subset _ _)

/-- **Theorem C-HT, counting part (𝒞).** `LHS = 2t + 2|Tri| + |qU| + |qO| ≤ 5t − 3`. -/
theorem forestBound (hC : LWClass D L₁ h F G) :
    2 * (maxSet D).card + 2 * (triSet D).card + (qU D).card + (qO D).card + 3 ≤
      5 * (maxSet D).card := by
  have := tripodForest'' hC
  have := qUForest hC
  have := qOForest hC
  omega

/-- CHT + the forest bounds: `2m + 3 ≤ H + 5t` on 𝒞. -/
theorem chtForest (hC : LWClass D L₁ h F G) :
    2 * D.card + 3 ≤ ∑ x ∈ D, hsum D x + 5 * (maxSet D).card := by
  have h1 := cht D
  have h2 := forestBound hC
  have h3 := card_qU_add_card_qO D
  omega

/-- **Theorem C-HT, final integer form (𝒞).** With CHT, the forest bounds and Lemma T
(`t + 2 ≤ C`): `2m + 13 ≤ H + 5C`, i.e. `δ = H − (m − 1) ≥ m + 14 − 5C`. -/
theorem deltaBound (hC : LWClass D L₁ h F G) :
    2 * D.card + 13 ≤ ∑ x ∈ D, hsum D x + 5 * ∑ c, (faceCorners D c).card := by
  have h1 := chtForest hC
  have h2 := typeBound hC
  omega

end Forest

end CornerArea

end NumericalSemigroup
