import Wilf.Forest
import Wilf.ConeType

/-!
# The C-HT threshold and the forest bounds for the cone class

Formalization of `.research/PROOFS.md`, "Cone tiles: QF-pair lemma, location corollary, Fiber Lemma,
and qO ≤ 2t + 11" and NOTEBOOK night 17 (Lemmas TF-cone, F-cone). Notation as in
`Wilf.CornerArea`, `Wilf.Forest` and `Wilf.ConeType`: `m = |D|`, `H = Σ_{x∈D} hsum D x`,
`t = |maxSet D|`, `C = Σ_c |faceCorners D c|`, `δ = H − (m − 1)`.

* **C-HT threshold** on 𝒞 (`chtThreshold`, `chtThreshold'`): from `deltaBound` and `cornerArea`,
  `m ≥ 131 ⇒ m ≤ H + 1` and `m ≥ 130 ⇒ m ≤ H + 2`.
* **Cone sets** (`ConeSet Cyl D q`): `D = Cyl ∖ K`, `K = q + ℕ³`, `Cyl` determined by its projections
  (`IsLW`), `q ≥ (1,1,1)`. Every `coneCut Cyl q` with `Cyl` in 𝒞 is one (`coneSet_coneCut`). The
  projection rule becomes "`z ∈ D` or `z ∈ K`" (`ConeSet.mem_or_K`), which gives Lemma S′ (`coneS`),
  no-three-directions (`coneNoThree`) and Lemma P′ (`coneP`).
* `Yset D q d = {y ∈ Max : y + e_d ≥ q}` (`Y_d`) and `Yall D q = ⋃_d Y_d` (`Y`).
* Elimination orders use the injective key `key x = ⟪x₀, ⟪x₁, x₂⟫⟫` (Cantor pairing), which is
  strictly increasing along every coordinate line; Lemma S fails in the cone class, so `|·|` cannot
  be used.
* **(a) F-cone** (`qU_cone`: `|qU| ≤ t` for every cone set; `fCone`: `|qU| ≤ t + 2`). The injection
  `gU` of `Wilf.Forest` works off a set `E` of at most one cell.
* **(b) qO-cone** (`qO_cone`: `|qO| + 1 ≤ 2t + |Y|`; `qOCone`: `|qO| + 1 ≤ 2t + 2|Y|`). Uses the
  cone QF-pair lemma (`qO_claim_cone`), the Location Corollary (`location_cone`) and the Fiber Lemma
  (`fiber`).
* **(c) TF-cone** (`tf_cone`: `2|Tri| ≤ t + |Y| + 11` if all `|Y_d| ≤ 2`; `tfCone`: `2|Tri| ≤ t + 17`).
  Uses the sets `Φ(a, b)` (`phiSet`) and the paper's claims (iii) `phi_iii`, (iv) `phi_iv`,
  (v) `phi_v1`, `phi_card`.
* **(d) Cone δ-bound** (`coneDelta_sharp`: `2m ≤ H + 6t + 2|Y| + 10`; `coneDeltaBound`:
  `2m ≤ H + 6C + 30`) and the thresholds `coneThreshold` (`m ≥ 281 ⇒ m ≤ H + 1`) and
  `coneThreshold'` (`m ≥ 280 ⇒ m ≤ H + 2`).
-/

namespace NumericalSemigroup

open Finset Function

-- The frame computations below call `simp` with one fixed list of direction facts on several goals.
set_option linter.unusedSimpArgs false
set_option linter.unnecessarySeqFocus false

namespace CornerArea

section ConeForest

variable {D : Finset (Fin 3 → ℕ)} {L₁ : ℕ} {h F G : ℕ → ℕ}

/-! ### The C-HT threshold on 𝒞 -/

/-- **C-HT threshold (δ ≥ 0).** On class 𝒞, `|D| ≥ 131` implies `|D| ≤ H + 1`, i.e.
`δ = H − (m − 1) ≥ 0`. -/
theorem chtThreshold (hC : LWClass D L₁ h F G) (hm : 131 ≤ D.card) :
    D.card ≤ ∑ x ∈ D, hsum D x + 1 := by
  have h1 := deltaBound hC
  have h2 := cornerArea hC.isLW.1 hC.nonempty
  set C := ∑ c, (faceCorners D c).card
  have h5 : 5 * C ≤ D.card + 14 := by
    by_contra hcon
    have h30 : 30 ≤ C := by omega
    nlinarith
  omega

/-- **C-HT threshold (δ ≥ −1).** On class 𝒞, `|D| ≥ 130` implies `|D| ≤ H + 2`. -/
theorem chtThreshold' (hC : LWClass D L₁ h F G) (hm : 130 ≤ D.card) :
    D.card ≤ ∑ x ∈ D, hsum D x + 2 := by
  have h1 := deltaBound hC
  have h2 := cornerArea hC.isLW.1 hC.nonempty
  set C := ∑ c, (faceCorners D c).card
  have h5 : 5 * C ≤ D.card + 15 := by
    by_contra hcon
    have h30 : 30 ≤ C := by omega
    nlinarith
  omega

/-! ### Cone sets -/

/-- A **cone set**: `D = Cyl ∖ (q + ℕ³)` where `Cyl` is a down-set determined by its projections and
`q ≥ (1,1,1)`. Every `coneCut Cyl q` with `Cyl` in 𝒞 is one (`coneSet_coneCut`). -/
structure ConeSet (Cyl D : Finset (Fin 3 → ℕ)) (q : Fin 3 → ℕ) : Prop where
  lw : IsLW Cyl
  q_pos : ∀ i, 1 ≤ q i
  mem_iff : ∀ z, z ∈ D ↔ z ∈ Cyl ∧ ¬ q ≤ z

variable {Cyl : Finset (Fin 3 → ℕ)} {q : Fin 3 → ℕ} {a b c : Fin 3}

theorem coneSet_coneCut (hC : LWClass Cyl L₁ h F G) (hq : ∀ i, 1 ≤ q i) :
    ConeSet Cyl (coneCut Cyl q) q :=
  ⟨hC.isLW, hq, fun z => by simp only [coneCut, mem_filter]; exact Iff.rfl⟩

namespace ConeSet

variable (hc : ConeSet Cyl D q)
include hc

theorem sub {z : Fin 3 → ℕ} (hz : z ∈ D) : z ∈ Cyl := ((hc.mem_iff z).1 hz).1

theorem not_K {z : Fin 3 → ℕ} (hz : z ∈ D) : ¬ q ≤ z := ((hc.mem_iff z).1 hz).2

theorem down : IsDownSetFin D := by
  intro x hx y hy
  rw [hc.mem_iff] at hx ⊢
  exact ⟨hc.lw.mem_of_le hx.1 hy, fun hq => hx.2 (le_trans hq hy)⟩

theorem K_of_not_mem {z : Fin 3 → ℕ} (hz : z ∈ Cyl) (hn : z ∉ D) : q ≤ z := by
  by_contra h'
  exact hn ((hc.mem_iff z).2 ⟨hz, h'⟩)

theorem cyl_of_proj (fr : Frame a b c) {z : Fin 3 → ℕ} (ha : update z a 0 ∈ D)
    (hb : update z b 0 ∈ D) (hcc : update z c 0 ∈ D) : z ∈ Cyl :=
  hc.lw.mem_frame fr (hc.sub ha) (hc.sub hb) (hc.sub hcc)

/-- The projection rule of a cone set: if the three projections of `z` lie in `D`, then `z ∈ D` or
`z ∈ K = q + ℕ³`. -/
theorem mem_or_K (fr : Frame a b c) {z : Fin 3 → ℕ} (ha : update z a 0 ∈ D)
    (hb : update z b 0 ∈ D) (hcc : update z c 0 ∈ D) : z ∈ D ∨ q ≤ z := by
  by_cases h' : z ∈ D
  · exact Or.inl h'
  · exact Or.inr (hc.K_of_not_mem (hc.cyl_of_proj fr ha hb hcc) h')

end ConeSet

/-! ### Lemma S′, no three directions, Lemma P′ -/

/-- **Lemma S′.** If `x + e_c, x' + e_c ∈ D` and `top_a(x) = top_b(x') = y ∈ Max` with `(a, b, c)` a
frame, then `y + e_c ∈ K`. -/
theorem coneS (hc : ConeSet Cyl D q) (fr : Frame a b c) {x x' : Fin 3 → ℕ}
    (hx : x + Pi.single c 1 ∈ D) (hx' : x' + Pi.single c 1 ∈ D)
    (h : colTop D a x = colTop D b x') (hy : colTop D a x ∈ maxSet D) :
    q ≤ colTop D a x + Pi.single c 1 := by
  have e1 : colTop D a x b = x b := colTop_apply_ne fr.hab.symm
  have e2 : colTop D a x c = x c := colTop_apply_ne fr.hac.symm
  have e3 : colTop D a x a = x' a := by rw [h]; exact colTop_apply_ne fr.hab
  have e4 : colTop D a x c = x' c := by rw [h]; exact colTop_apply_ne fr.hbc.symm
  have hyD := (mem_filter.1 hy).1
  have hca := fr.hac.symm; have hcb := fr.hbc.symm; have hba := fr.hab.symm
  have hD := hc.down
  have p1 : update (colTop D a x + Pi.single c 1) a 0 ∈ D := by
    refine hD _ hx _ (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
      simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba, e1, e2]
  have p2 : update (colTop D a x + Pi.single c 1) b 0 ∈ D := by
    refine hD _ hx' _ (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
      simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba, e3, e4]
  have p3 : update (colTop D a x + Pi.single c 1) c 0 ∈ D := by
    refine hD _ hyD _ (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
      simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba]
  rcases hc.mem_or_K fr p1 p2 p3 with h' | h'
  · exact absurd h' ((mem_filter.1 hy).2 c)
  · exact h'

/-- **No three directions.** A maximal cell is not the top, in three distinct directions, of three
cells all of whose `+e_d` lie in `D` (it would lie in `K`). -/
theorem coneNoThree (hc : ConeSet Cyl D q) (fr : Frame a b c) {x x' x'' : Fin 3 → ℕ}
    (hx : ∀ d, x + Pi.single d 1 ∈ D) (hx' : ∀ d, x' + Pi.single d 1 ∈ D)
    (hx'' : ∀ d, x'' + Pi.single d 1 ∈ D)
    (h1 : colTop D a x = colTop D b x') (h2 : colTop D a x = colTop D c x'')
    (hy : colTop D a x ∈ maxSet D) : False := by
  have k1 := coneS hc fr (hx c) (hx' c) h1 hy
  have k2 := coneS hc ⟨fr.hac, fr.hab, fr.hbc.symm⟩ (hx b) (hx'' b) h2 hy
  apply hc.not_K (mem_filter.1 hy).1
  have hca := fr.hac.symm; have hcb := fr.hbc.symm; have hba := fr.hab.symm
  rw [fr.le_iff] at k1 k2 ⊢
  simp [Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba] at k1 k2
  omega

/-- **Lemma P′.** If `top_c(x), top_c(x') ∈ Max`, `x + e_a ∈ D`, `x' + e_b ∈ D`, `x_a < x'_a` and
`x'_b < x_b`, then `top_c(x) + e_a ∈ K` or `top_c(x') + e_b ∈ K`. -/
theorem coneP (hc : ConeSet Cyl D q) (fr : Frame a b c) {x x' : Fin 3 → ℕ}
    (hy : colTop D c x ∈ maxSet D) (hy' : colTop D c x' ∈ maxSet D)
    (hxa : x + Pi.single a 1 ∈ D) (hxb : x' + Pi.single b 1 ∈ D) (h1 : x a < x' a)
    (h2 : x' b < x b) :
    q ≤ colTop D c x + Pi.single a 1 ∨ q ≤ colTop D c x' + Pi.single b 1 := by
  by_contra hcon
  obtain ⟨n1, n2⟩ := not_or.1 hcon
  have hD := hc.down
  have ya : colTop D c x a = x a := colTop_apply_ne fr.hac
  have yb : colTop D c x b = x b := colTop_apply_ne fr.hbc
  have ya' : colTop D c x' a = x' a := colTop_apply_ne fr.hac
  have yb' : colTop D c x' b = x' b := colTop_apply_ne fr.hbc
  have hyD := (mem_filter.1 hy).1
  have hyD' := (mem_filter.1 hy').1
  have hca := fr.hac.symm; have hcb := fr.hbc.symm; have hba := fr.hab.symm
  have hP : update (colTop D c x + Pi.single a 1 : Fin 3 → ℕ) b 0 ∉ D := by
    intro hP
    have p1 : update (colTop D c x + Pi.single a 1 : Fin 3 → ℕ) a 0 ∈ D := by
      refine hD _ hyD _ (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
        simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba]
    have p3 : update (colTop D c x + Pi.single a 1 : Fin 3 → ℕ) c 0 ∈ D := by
      refine hD _ hxa _ (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
        simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba, ya, yb]
    rcases hc.mem_or_K fr p1 hP p3 with h' | h'
    · exact (mem_filter.1 hy).2 a h'
    · exact n1 h'
  have hP' : update (colTop D c x' + Pi.single b 1 : Fin 3 → ℕ) a 0 ∉ D := by
    intro hP'
    have p2 : update (colTop D c x' + Pi.single b 1 : Fin 3 → ℕ) b 0 ∈ D := by
      refine hD _ hyD' _ (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
        simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba]
    have p3 : update (colTop D c x' + Pi.single b 1 : Fin 3 → ℕ) c 0 ∈ D := by
      refine hD _ hxb _ (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
        simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba, ya', yb']
    rcases hc.mem_or_K fr hP' p2 p3 with h' | h'
    · exact (mem_filter.1 hy').2 b h'
    · exact n2 h'
  have hk1 : colTop D c x' c < colTop D c x c := by
    by_contra hle
    push Not at hle
    apply hP
    refine hD _ hyD' _ (fr.le_iff.2 ⟨?_, ?_, ?_⟩)
    · simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba, ya, ya']; omega
    · simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba]
    · simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba]; omega
  have hk2 : colTop D c x c < colTop D c x' c := by
    by_contra hle
    push Not at hle
    apply hP'
    refine hD _ hyD _ (fr.le_iff.2 ⟨?_, ?_, ?_⟩)
    · simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba]
    · simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba, yb, yb']; omega
    · simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba]; omega
  omega

/-! ### General helpers -/

/-- A maximal cell below a cell of a down-set is that cell. -/
theorem maxSet_le_eq (hD : IsDownSetFin D) {y z : Fin 3 → ℕ} (hy : y ∈ maxSet D) (hz : z ∈ D)
    (hle : y ≤ z) : y = z := by
  by_contra hne
  obtain ⟨i, hi⟩ := Function.ne_iff.1 hne
  have hlt : y i < z i := lt_of_le_of_ne (hle i) hi
  apply (mem_filter.1 hy).2 i
  refine hD _ hz _ fun j => ?_
  by_cases hj : j = i
  · subst hj; simp; omega
  · simp [Pi.single_eq_of_ne hj]; exact hle j

/-- Two cells with the same `d`-top agree off `d`. -/
theorem colTop_agree {x u : Fin 3 → ℕ} {d : Fin 3} (h : colTop D d u = colTop D d x) :
    ∀ i, i ≠ d → u i = x i := fun i hi => by
  have := congrFun h i
  rwa [colTop_apply_ne hi, colTop_apply_ne hi] at this

/-- A top different from the cell determines its direction. -/
theorem colTop_dir_eq {x : Fin 3 → ℕ} {d d' : Fin 3} (hne : colTop D d x ≠ x)
    (h : colTop D d x = colTop D d' x) : d = d' := by
  by_contra hdd
  have e := congrFun h d
  rw [colTop_apply_self, colTop_apply_ne hdd] at e
  apply hne
  simp [colTop, show colHt D d x = 0 by omega]

/-- `z c ≤ top_c(x)_c` for every `z ∈ D` on the `c`-line of `x` above `x`. -/
theorem le_colTop_c {x z : Fin 3 → ℕ} {c : Fin 3} (hz : z ∈ D)
    (hagree : ∀ i, i ≠ c → z i = x i) (hle : x c ≤ z c) : z c ≤ colTop D c x c := by
  have hz' : x + Pi.single c (z c - x c) ∈ D := by
    have : x + Pi.single c (z c - x c) = z := funext fun i => by
      by_cases hi : i = c
      · subst hi; simp; omega
      · simp [Pi.single_eq_of_ne hi, hagree i hi]
    rw [this]; exact hz
  have := le_colHt hz'
  rw [colTop_apply_self]
  omega

/-! ### Lemma F-cone (qU) -/

theorem yStar_mem' (hD : IsDownSetFin D) (hne : D.Nonempty) : yStar D ∈ maxSet D := by
  have h0 := zero_mem hD hne
  obtain ⟨w0, w1, u1, u2, ys0, ys2⟩ := yStar_coords (D := D)
  have fr := frame012
  refine mem_filter.2 ⟨colTop_mem (colTop_mem (colTop_mem h0)), fun d => ?_⟩
  fin_cases d
  · intro h
    apply colTop_succ_not_mem (D := D) (colTop D 2 0) 0
    refine hD _ h _ (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;> simp [Pi.single_apply, u1] <;> omega
  · exact colTop_succ_not_mem (D := D) _ 1
  · intro h
    apply colTop_succ_not_mem (D := D) (0 : Fin 3 → ℕ) 2
    refine hD _ h _ (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;> simp [Pi.single_apply, w0, w1] <;>
      omega

theorem gU_ne_yStar' (hD : IsDownSetFin D) {x : Fin 3 → ℕ} (hx : x ∈ qU D) :
    gU D x ≠ yStar D := by
  obtain ⟨w0, w1, u1, u2, ys0, ys2⟩ := yStar_coords (D := D)
  have fr := frame012
  intro heq
  obtain ⟨-, ⟨hg, h | ⟨h, -⟩⟩ | ⟨hg, h⟩⟩ := gU_spec hD hx
  · rw [hg] at heq
    have e2 := congrFun heq 2
    simp [Pi.single_apply] at e2
    apply colTop_succ_not_mem (D := D) (0 : Fin 3 → ℕ) 2
    refine hD _ h _ (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;> simp [Pi.single_apply, w0, w1] <;>
      omega
  · rw [hg] at heq
    have e0 := congrFun heq 0
    have e2 := congrFun heq 2
    simp [Pi.single_apply] at e0 e2
    apply colTop_succ_not_mem (D := D) (colTop D 2 0) 0
    refine hD _ h _ (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;> simp [Pi.single_apply, u1] <;> omega
  · rw [hg] at heq
    have e2 := congrFun heq 2
    simp [Pi.single_apply] at e2
    apply colTop_succ_not_mem (D := D) (0 : Fin 3 → ℕ) 2
    refine hD _ h _ (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
      simp [update_apply, Pi.single_apply, w0, w1] <;> omega

/-- Cone version of `gU_mixed`: a collision between an `x + e₁` image and an `x' + e₀` image
forces `x + e₂ ∈ D`, `x₁ + 1 = q₁` and `x₂ + 1 = q₂`. -/
theorem gU_mixed_cone (hc : ConeSet Cyl D q) {x x' : Fin 3 → ℕ}
    (h1 : x + Pi.single 2 1 ∈ D ∨ (x + Pi.single 0 1 ∈ D ∧ update (x + Pi.single 2 1) 0 0 ∉ D))
    (hy : x + Pi.single 1 1 ∈ maxSet D) (h0 : update (x' + Pi.single 2 1) 0 0 ∈ D)
    (heq : x + Pi.single 1 1 = x' + Pi.single 0 1) :
    x + Pi.single 2 1 ∈ D ∧ x 1 + 1 = q 1 ∧ x 2 + 1 = q 2 := by
  have e0 := congrFun heq 0
  have e1 := congrFun heq 1
  have e2 := congrFun heq 2
  simp [Pi.single_apply] at e0 e1 e2
  have fr := frame012
  have hD := hc.down
  rcases h1 with h1 | ⟨-, h1⟩
  · have p0 : update (x + Pi.single 1 1 + Pi.single 2 1) 0 0 ∈ D := by
      refine hD _ h0 _ (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;> simp [update_apply, Pi.single_apply] <;>
        omega
    have p1 : update (x + Pi.single 1 1 + Pi.single 2 1) 1 0 ∈ D := by
      refine hD _ h1 _ (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;> simp [update_apply, Pi.single_apply]
    have p2 : update (x + Pi.single 1 1 + Pi.single 2 1) 2 0 ∈ D := by
      refine hD _ (mem_filter.1 hy).1 _ (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
        simp [update_apply, Pi.single_apply]
    rcases hc.mem_or_K fr p0 p1 p2 with hz | hz
    · exact absurd hz ((mem_filter.1 hy).2 2)
    · have hK := fr.le_iff.1 hz
      have n1 := hc.not_K (mem_filter.1 hy).1
      have n2 := hc.not_K h1
      rw [fr.le_iff] at n1 n2
      simp [Pi.single_apply] at hK n1 n2
      refine ⟨h1, ?_, ?_⟩
      · by_contra hne
        have := n2 hK.1 (by omega)
        omega
      · by_contra hne
        have := n1 hK.1 hK.2.1
        omega
  · exfalso
    apply h1
    refine hD _ h0 _ (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;> simp [update_apply, Pi.single_apply] <;>
      omega

/-- Two `qU` cells `x ≠ x'` with `x + e₂ ∈ D` and equal coordinates `1, 2` do not exist. -/
theorem qU_row_unique (hD : IsDownSetFin D) {x x' : Fin 3 → ℕ} (hx : x ∈ qU D) (hx' : x' ∈ qU D)
    (h2 : x + Pi.single 2 1 ∈ D) (e1 : x 1 = x' 1) (e2 : x 2 = x' 2) (hlt : x 0 < x' 0) :
    False := by
  obtain ⟨c, hcm, hd⟩ := qSet_dir (mem_filter.1 hx).1
  have hs := qU_struct hD hx hd
  have hx'D := (mem_filter.1 (mem_filter.1 hx').1).1
  have hle : x + Pi.single 0 1 ≤ x' := frame012.le_iff.2 ⟨by simp; omega, by simp; omega,
    by simp; omega⟩
  have h0 : x + Pi.single 0 1 ∈ D := hD _ hx'D _ hle
  rcases fin3_cases frame012.hab frame012.hac frame012.hbc c with hc | hc | hc
  · rw [hc] at hs; exact hs.1 h0
  · rw [hc] at hs
    have hm := hs.2 0 (by decide)
    have := maxSet_le_eq hD hm hx'D hle
    exact qSet_not_max hD (mem_filter.1 hx').1 (this ▸ hm)
  · rw [hc] at hs; exact hs.1 h2

/-- **Lemma F-cone (qU), sharp form.** For every cone set, `|qU| ≤ t`. -/
theorem qU_cone (hc : ConeSet Cyl D q) : (qU D).card ≤ (maxSet D).card := by
  have hD := hc.down
  rcases D.eq_empty_or_nonempty with hD0 | hne
  · have : qU D = ∅ := by
      ext x
      simp only [notMem_empty, iff_false]
      intro hx
      have := (mem_filter.1 (mem_filter.1 hx).1).1
      rw [hD0] at this
      simp at this
    rw [this, card_empty]; exact Nat.zero_le _
  set E := (qU D).filter (fun x => x + Pi.single 2 1 ∈ D ∧ x 1 + 1 = q 1 ∧ x 2 + 1 = q 2)
  have hE : E.card ≤ 1 := by
    refine card_le_one.2 fun x hx x' hx' => ?_
    obtain ⟨hxU, hx2, hx1q, hx2q⟩ := mem_filter.1 hx
    obtain ⟨hxU', hx2', hx1q', hx2q'⟩ := mem_filter.1 hx'
    have e1 : x 1 = x' 1 := by omega
    have e2 : x 2 = x' 2 := by omega
    rcases lt_trichotomy (x 0) (x' 0) with hlt | heq | hgt
    · exact (qU_row_unique hD hxU hxU' hx2 e1 e2 hlt).elim
    · exact frame012.ext heq e1 e2
    · exact (qU_row_unique hD hxU' hxU hx2' e1.symm e2.symm hgt).elim
  have hys := yStar_mem' hD hne
  have hR := card_le_card_of_injOn (gU D) (s := qU D \ E) (t := (maxSet D).erase (yStar D))
    (fun x hx => mem_erase.2 ⟨gU_ne_yStar' hD (mem_sdiff.1 hx).1,
      (gU_spec hD (mem_sdiff.1 hx).1).1⟩) (by
      intro x hx x' hx' heq
      have hxU := (mem_sdiff.1 hx).1
      have hxU' := (mem_sdiff.1 hx').1
      have hxE := (mem_sdiff.1 hx).2
      have hxE' := (mem_sdiff.1 hx').2
      obtain ⟨hm, hh | hh⟩ := gU_spec hD hxU <;> obtain ⟨hm', hh' | hh'⟩ := gU_spec hD hxU'
      · rw [hh.1, hh'.1] at heq; exact add_right_cancel heq
      · rw [hh.1, hh'.1] at heq
        exact (hxE (mem_filter.2 ⟨hxU, gU_mixed_cone hc hh.2 (hh.1 ▸ hm) hh'.2 heq⟩)).elim
      · rw [hh.1, hh'.1] at heq
        exact (hxE' (mem_filter.2 ⟨hxU', gU_mixed_cone hc hh'.2 (hh'.1 ▸ hm') hh.2
          heq.symm⟩)).elim
      · rw [hh.1, hh'.1] at heq; exact add_right_cancel heq)
  rw [card_erase_of_mem hys] at hR
  have hsplit : (qU D \ E).card + E.card = (qU D).card :=
    card_sdiff_add_card_eq_card (filter_subset _ _)
  have := card_pos.2 ⟨_, hys⟩
  omega

/-- **Lemma F-cone (qU).** For `Cyl` in 𝒞 and `q ≥ (1,1,1)`, `D = Cyl ∖ (q + ℕ³)` satisfies
`|qU D| ≤ t + 2` (the sharp form `|qU D| ≤ t` is `qU_cone`). -/
theorem fCone (hC : LWClass Cyl L₁ h F G) (hq : ∀ i, 1 ≤ q i) :
    (qU (coneCut Cyl q)).card ≤ (maxSet (coneCut Cyl q)).card + 2 := by
  have := qU_cone (coneSet_coneCut hC hq)
  omega

/-! ### A strict total order compatible with lines -/

/-- An injective key, strictly increasing along every coordinate line (in the cone class, cells of
equal `|·|` can share tops, so the elimination orders use this key instead of `|·|`). -/
def key (x : Fin 3 → ℕ) : ℕ := Nat.pair (x 0) (Nat.pair (x 1) (x 2))

theorem key_inj {x y : Fin 3 → ℕ} (h : key x = key y) : x = y := by
  unfold key at h
  obtain ⟨h0, h12⟩ := Nat.pair_eq_pair.1 h
  obtain ⟨h1, h2⟩ := Nat.pair_eq_pair.1 h12
  exact frame012.ext h0 h1 h2

theorem key_lt_of_line {x y : Fin 3 → ℕ} {a : Fin 3} (h : ∀ i, i ≠ a → x i = y i)
    (hlt : x a < y a) : key x < key y := by
  unfold key
  fin_cases a
  · rw [h 1 (by decide), h 2 (by decide)]
    exact Nat.pair_lt_pair_left _ hlt
  · rw [h 0 (by decide), h 2 (by decide)]
    exact Nat.pair_lt_pair_right _ (Nat.pair_lt_pair_left _ hlt)
  · rw [h 0 (by decide), h 1 (by decide)]
    exact Nat.pair_lt_pair_right _ (Nat.pair_lt_pair_right _ hlt)

theorem key_lt_iff_line {x y : Fin 3 → ℕ} {a : Fin 3} (h : ∀ i, i ≠ a → x i = y i) :
    key x < key y ↔ x a < y a := by
  refine ⟨fun hk => ?_, key_lt_of_line h⟩
  rcases lt_trichotomy (x a) (y a) with hlt | heq | hgt
  · exact hlt
  · have : x = y := funext fun i => by
      by_cases hi : i = a
      · rw [hi]; exact heq
      · exact h i hi
    rw [this] at hk; exact absurd hk (lt_irrefl _)
  · have := key_lt_of_line (fun i hi => (h i hi).symm) hgt; omega

/-! ### Lemma qO-cone: the QF-pair lemma, Location, Fiber -/

/-- Two `Q'` cells with non-maximal direction `c` on one `a`-line: the higher one has the lower
`c`-top (the plateau argument of Lemma QF; down-sets only). -/
theorem plateau_lt (hD : IsDownSetFin D) (fr : Frame a b c) {x x' : Fin 3 → ℕ} (hx : x ∈ qSet D)
    (hxd : ∀ d, d ≠ c → colTop D d x ∈ maxSet D) (hx' : x' ∈ qSet D)
    (hxd' : ∀ d, d ≠ c → colTop D d x' ∈ maxSet D)
    (hagree : ∀ i, i ≠ a → x' i = x i) (hlt : x' a < x a) :
    colTop D c x c < colTop D c x' c := by
  have hht' := qSet_ht hD hx' hxd'
  have hht := qSet_ht hD hx hxd
  have hxD := (mem_filter.1 hx).1
  have hyD : colTop D c x ∈ D := colTop_mem hxD
  have hy'D : colTop D c x' ∈ D := colTop_mem (mem_filter.1 hx').1
  have ya : colTop D c x a = x a := colTop_apply_ne fr.hac
  have yb : colTop D c x b = x b := colTop_apply_ne fr.hbc
  have ya' : colTop D c x' a = x' a := colTop_apply_ne fr.hac
  have yb' : colTop D c x' b = x' b := colTop_apply_ne fr.hbc
  have hb' : x' b = x b := hagree b fr.hab.symm
  by_contra hle
  push Not at hle
  obtain ⟨⟨z, hzD, hzy, hzeq⟩, -⟩ := ht_spec hyD
  have hle' : colTop D c x' ≤ colTop D c x := fr.le_iff.2 ⟨by omega, by omega, hle⟩
  have h2 := (ht_spec hy'D).2 z hzD (fun i => le_trans (hle' i) (hzy i))
  rw [hht', fr.sum z, fr.sum (colTop D c x')] at h2
  rw [hht, fr.sum z, fr.sum (colTop D c x)] at hzeq
  omega

/-- **QF-pair lemma (cone class).** Let `x ∈ Q'` have non-maximal direction `c`, and let `x' ∈ Q'`
lie below `x` on the `a`-line with `top_a x' ∈ Max`. Then the face witness of Lemma QF exists, or
(α) `x'` has non-maximal direction `b` and `top_c(x') + e_a ∈ K`, or
(β) `x'` has non-maximal direction `c`, `x_a ≥ q_a`, `x_b ≥ q_b`, `x'_a < q_a` and the column of `x`
in direction `c` has height `q_c` (`top_c(x)_c + 1 = q_c`). -/
theorem qO_claim_cone (hc : ConeSet Cyl D q) (fr : Frame a b c) {x x' : Fin 3 → ℕ}
    (hx : x ∈ qSet D) (hxd : ∀ d, d ≠ c → colTop D d x ∈ maxSet D)
    (hx' : x' ∈ qSet D) (htop : colTop D a x' ∈ maxSet D)
    (hagree : ∀ i, i ≠ a → x' i = x i) (hlt : x' a < x a) :
    (∃ k, pt a b c (x a) 0 k ∉ D ∧ pt a b c 0 (x b) k ∈ D) ∨
    (colTop D b x' ∉ maxSet D ∧ q ≤ colTop D c x' + Pi.single a 1) ∨
    (colTop D c x' ∉ maxSet D ∧ q a ≤ x a ∧ q b ≤ x b ∧ x' a < q a ∧
      colTop D c x c + 1 = q c) := by
  have hD := hc.down
  have hca := fr.hac.symm; have hcb := fr.hbc.symm; have hba := fr.hab.symm
  have hxD := (mem_filter.1 hx).1
  have hb' : x' b = x b := hagree b hba
  obtain ⟨c', hc'm, hd'⟩ := qSet_dir hx'
  rcases fin3_cases fr.hab fr.hac fr.hbc c' with h | h | h
  · rw [h] at hc'm; exact absurd htop hc'm
  · rw [h] at hd' hc'm
    have hy' := hd' c hcb
    have hy'D := (mem_filter.1 hy').1
    have ya : colTop D c x' a = x' a := colTop_apply_ne fr.hac
    have yb : colTop D c x' b = x' b := colTop_apply_ne fr.hbc
    by_cases hP : pt a b c (x a) 0 (colTop D c x' c) ∈ D
    · right; left
      refine ⟨hc'm, ?_⟩
      have p1 : update (colTop D c x' + Pi.single a 1 : Fin 3 → ℕ) a 0 ∈ D := by
        refine hD _ hy'D _ (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
          simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba]
      have p2 : update (colTop D c x' + Pi.single a 1 : Fin 3 → ℕ) b 0 ∈ D := by
        refine hD _ hP _ (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
          simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba, fr.pt_a,
            fr.pt_b, fr.pt_c, ya] <;> omega
      have p3 : update (colTop D c x' + Pi.single a 1 : Fin 3 → ℕ) c 0 ∈ D := by
        refine hD _ hxD _ (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
          simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba, ya, yb] <;>
          omega
      rcases hc.mem_or_K fr p1 p2 p3 with hz | hz
      · exact absurd hz ((mem_filter.1 hy').2 a)
      · exact hz
    · left
      refine ⟨colTop D c x' c, hP, ?_⟩
      refine hD _ hy'D _ (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
        simp [fr.pt_a, fr.pt_b, fr.pt_c, yb] <;> omega
  · rw [h] at hd' hc'm
    have hk := plateau_lt hD fr hx hxd hx' hd' hagree hlt
    have hyD : colTop D c x ∈ D := colTop_mem hxD
    have hy'D : colTop D c x' ∈ D := colTop_mem (mem_filter.1 hx').1
    have ya : colTop D c x a = x a := colTop_apply_ne fr.hac
    have yb : colTop D c x b = x b := colTop_apply_ne fr.hbc
    have ya' : colTop D c x' a = x' a := colTop_apply_ne fr.hac
    have yb' : colTop D c x' b = x' b := colTop_apply_ne fr.hbc
    by_cases hP : pt a b c (x a) 0 (colTop D c x' c) ∈ D
    · right; right
      have p1 : update (update (colTop D c x) c (colTop D c x' c)) a 0 ∈ D := by
        refine hD _ hy'D _ (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
          simp [update_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba, yb, yb'] <;> omega
      have p2 : update (update (colTop D c x) c (colTop D c x' c)) b 0 ∈ D := by
        refine hD _ hP _ (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
          simp [update_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba, ya, fr.pt_a, fr.pt_b,
            fr.pt_c]
      have p3 : update (update (colTop D c x) c (colTop D c x' c)) c 0 ∈ D := by
        refine hD _ hyD _ (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
          simp [update_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba]
      have hwC := hc.cyl_of_proj fr p1 p2 p3
      have hw : update (colTop D c x) c (colTop D c x' c) ∉ D := by
        intro hw
        apply colTop_succ_not_mem (D := D) x c
        refine hD _ hw _ (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
          simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba] <;> omega
      have hKw := fr.le_iff.1 (hc.K_of_not_mem hwC hw)
      have wa : update (colTop D c x) c (colTop D c x' c) a = x a := by
        simp [update_apply, fr.hac, ya]
      have wb : update (colTop D c x) c (colTop D c x' c) b = x b := by
        simp [update_apply, fr.hbc, yb]
      have wc : update (colTop D c x) c (colTop D c x' c) c = colTop D c x' c := by simp
      rw [wa, wb, wc] at hKw
      have hsC : colTop D c x + Pi.single c 1 ∈ Cyl := by
        refine hc.lw.mem_of_le hwC (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
          simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb, hba] <;> omega
      have hKs := (fr.le_iff.1 (hc.K_of_not_mem hsC (colTop_succ_not_mem x c))).2.2
      have sc : (colTop D c x + Pi.single c 1 : Fin 3 → ℕ) c = colTop D c x c + 1 := by simp
      rw [sc] at hKs
      have nK : ¬ (q a ≤ x a ∧ q b ≤ x b ∧ q c ≤ colTop D c x c) := fun hh =>
        hc.not_K hyD (fr.le_iff.2 ⟨by rw [ya]; exact hh.1, by rw [yb]; exact hh.2.1, hh.2.2⟩)
      have nK' : ¬ (q a ≤ x' a ∧ q b ≤ x' b ∧ q c ≤ colTop D c x' c) := fun hh =>
        hc.not_K hy'D (fr.le_iff.2 ⟨by rw [ya']; exact hh.1, by rw [yb']; exact hh.2.1, hh.2.2⟩)
      refine ⟨hc'm, hKw.1, hKw.2.1, ?_, ?_⟩
      · by_contra hh
        exact nK' ⟨by omega, by omega, hKw.2.2⟩
      · by_contra hh
        exact nK ⟨hKw.1, hKw.2.1, by omega⟩
    · left
      refine ⟨colTop D c x' c, hP, ?_⟩
      refine hD _ hy'D _ (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
        simp [fr.pt_a, fr.pt_b, fr.pt_c, yb'] <;> omega

/-- **Location Corollary.** A `qO` cell `x` with non-maximal direction `c` that has a `qO` partner
below it on both maximal lines (with the same tops) lies in `B_c`: `x_a ≥ q_a`, `x_b ≥ q_b`,
`x_c < q_c`. -/
theorem location_cone (hc : ConeSet Cyl D q) (fr : Frame a b c) {x u u' : Fin 3 → ℕ} (hx : x ∈ qO D)
    (hxd : ∀ d, d ≠ c → colTop D d x ∈ maxSet D)
    (hu : u ∈ qO D) (hua : colTop D a u = colTop D a x) (hlu : u a < x a)
    (hu' : u' ∈ qO D) (hub : colTop D b u' = colTop D b x) (hlu' : u' b < x b) :
    q a ≤ x a ∧ q b ≤ x b ∧ x c < q c := by
  have hD := hc.down
  have hca := fr.hac.symm; have hcb := fr.hbc.symm; have hba := fr.hab.symm
  have hxq := (mem_sdiff.1 hx).1
  have ag := colTop_agree hua
  have ag' := colTop_agree hub
  have hxc : x c ≤ colTop D c x c := by rw [colTop_apply_self]; omega
  have R1 := qO_claim_cone hc fr hxq hxd (mem_sdiff.1 hu).1 (by rw [hua]; exact hxd a fr.hac) ag
    hlu
  have R2 := qO_claim_cone hc fr.swap hxq hxd (mem_sdiff.1 hu').1 (by rw [hub]; exact hxd b fr.hbc)
    ag' hlu'
  rcases R1 with ⟨k1, hk1, hk2⟩ | ⟨-, hK⟩ | ⟨-, h1, h2, -, h4⟩
  · rcases R2 with ⟨k2, hk3, hk4⟩ | ⟨-, hK⟩ | ⟨-, h1, h2, -, h4⟩
    · exact (qO_contra hD fr hk1 hk2 hk3 hk4).elim
    · -- (α) for the `b`-partner
      have hK' := fr.le_iff.1 hK
      have ua : (colTop D c u' + Pi.single b 1 : Fin 3 → ℕ) a = x a := by
        simp [Pi.single_apply, fr.hab, colTop_apply_ne fr.hac, ag' a fr.hab]
      have ub : (colTop D c u' + Pi.single b 1 : Fin 3 → ℕ) b = u' b + 1 := by
        simp [Pi.single_apply, colTop_apply_ne fr.hbc]
      rw [ua, ub] at hK'
      have hs := hc.not_K (qO_succ_mem hD hu' b)
      have hsc : ¬ (q a ≤ x a ∧ q b ≤ u' b + 1 ∧ q c ≤ x c) := fun hh => hs (fr.le_iff.2
        ⟨by simp [Pi.single_apply, fr.hab, ag' a fr.hab]; exact hh.1,
         by simp; exact hh.2.1, by simp [Pi.single_apply, hca, hcb, ag' c hcb]; exact hh.2.2⟩)
      refine ⟨hK'.1, by omega, ?_⟩
      by_contra hh
      exact hsc ⟨hK'.1, hK'.2.1, by omega⟩
    · exact ⟨h2, h1, by omega⟩
  · -- (α) for the `a`-partner
    have hK' := fr.le_iff.1 hK
    have ua : (colTop D c u + Pi.single a 1 : Fin 3 → ℕ) a = u a + 1 := by
      simp [Pi.single_apply, colTop_apply_ne fr.hac]
    have ub : (colTop D c u + Pi.single a 1 : Fin 3 → ℕ) b = x b := by
      simp [Pi.single_apply, hba, colTop_apply_ne fr.hbc, ag b hba]
    rw [ua, ub] at hK'
    have hs := hc.not_K (qO_succ_mem hD hu a)
    have hsc : ¬ (q a ≤ u a + 1 ∧ q b ≤ x b ∧ q c ≤ x c) := fun hh => hs (fr.le_iff.2
      ⟨by simp; exact hh.1, by simp [Pi.single_apply, hba, ag b hba]; exact hh.2.1,
       by simp [Pi.single_apply, hca, ag c hca]; exact hh.2.2⟩)
    refine ⟨by omega, hK'.2.1, ?_⟩
    by_contra hh
    exact hsc ⟨hK'.1, hK'.2.1, by omega⟩
  · exact ⟨h1, h2, by omega⟩

/-- `x` is **doubly-same (DS)**: `x ∈ qO`, and for each maximal direction `d` some `qO` cell below `x`
on the `d`-line has the same `d`-top. -/
def IsDS (D : Finset (Fin 3 → ℕ)) (x : Fin 3 → ℕ) : Prop :=
  x ∈ qO D ∧ ∀ d, colTop D d x ∈ maxSet D → ∃ u ∈ qO D, u d < x d ∧ colTop D d u = colTop D d x

theorem IsDS.location (hc : ConeSet Cyl D q) (fr : Frame a b c) {x : Fin 3 → ℕ} (hx : IsDS D x)
    (hxd : ∀ d, d ≠ c → colTop D d x ∈ maxSet D) : q a ≤ x a ∧ q b ≤ x b ∧ x c < q c := by
  obtain ⟨u, hu, hlu, hua⟩ := hx.2 a (hxd a fr.hac)
  obtain ⟨u', hu', hlu', hub⟩ := hx.2 b (hxd b fr.hbc)
  exact location_cone hc fr hx.1 hxd hu hua hlu hu' hub hlu'

theorem fiber_aux (hc : ConeSet Cyl D q) {x x' : Fin 3 → ℕ} (hx : IsDS D x) (hx' : IsDS D x')
    {a : Fin 3} (ha : colTop D a x ∈ maxSet D) (heq : colTop D a x = colTop D a x')
    (hlt : x a < x' a) : False := by
  have hD := hc.down
  have ag := colTop_agree heq
  have hxq := (mem_sdiff.1 hx.1).1
  have hxq' := (mem_sdiff.1 hx'.1).1
  obtain ⟨c, hcm, hd⟩ := qSet_dir hxq
  obtain ⟨c', hcm', hd'⟩ := qSet_dir hxq'
  have hac : a ≠ c := fun h => hcm (h ▸ ha)
  have ha' : colTop D a x' ∈ maxSet D := heq ▸ ha
  have hac' : a ≠ c' := fun h => hcm' (h ▸ ha')
  obtain ⟨b, hab, hcb⟩ := exists_third hac
  have fr : Frame a b c := ⟨hab, hac, hcb.symm⟩
  have hca := fr.hac.symm; have hcb' := fr.hbc.symm; have hba := fr.hab.symm
  have Lx := hx.location hc fr hd
  have xb : x b = x' b := ag b hba
  rcases fin3_cases fr.hab fr.hac fr.hbc c' with h | h | h
  · exact hac' h.symm
  · -- different non-maximal directions: Location for both cells clashes
    rw [h] at hd'
    have Lx' := hx'.location hc ⟨fr.hac, fr.hab, fr.hbc.symm⟩ hd'
    omega
  · rw [h] at hd' hcm'
    have hk := plateau_lt hD fr hxq' hd' hxq hd ag hlt
    have hyD : colTop D c x ∈ D := colTop_mem (mem_filter.1 hxq).1
    have hxD' := (mem_filter.1 hxq').1
    have ya : colTop D c x a = x a := colTop_apply_ne fr.hac
    have yb : colTop D c x b = x b := colTop_apply_ne fr.hbc
    have ya' : colTop D c x' a = x' a := colTop_apply_ne fr.hac
    have yb' : colTop D c x' b = x' b := colTop_apply_ne fr.hbc
    have hTq : colTop D c x c < q c := by
      by_contra hh
      exact hc.not_K hyD (fr.le_iff.2 ⟨by rw [ya]; exact Lx.1, by rw [yb]; exact Lx.2.1,
        by omega⟩)
    -- the column of `x'` in direction `c` is cut by the `(a, c)`-face
    have hproj : pt a b c (x' a) 0 (colTop D c x' c + 1) ∉ D := by
      intro hP
      have p1 : update (colTop D c x' + Pi.single c 1 : Fin 3 → ℕ) a 0 ∈ D := by
        refine hD _ hyD _ (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
          simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb', hba, ya, yb,
            yb', xb] <;> omega
      have p2 : update (colTop D c x' + Pi.single c 1 : Fin 3 → ℕ) b 0 ∈ D := by
        refine hD _ hP _ (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
          simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb', hba, fr.pt_a,
            fr.pt_b, fr.pt_c, ya']
      have p3 : update (colTop D c x' + Pi.single c 1 : Fin 3 → ℕ) c 0 ∈ D := by
        refine hD _ hxD' _ (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
          simp [update_apply, Pi.single_apply, fr.hab, fr.hac, fr.hbc, hca, hcb', hba, ya', yb']
      rcases hc.mem_or_K fr p1 p2 p3 with hz | hz
      · exact colTop_succ_not_mem x' c hz
      · have := (fr.le_iff.1 hz).2.2
        simp at this
        omega
    obtain ⟨u, hu, hlu, hub⟩ := hx'.2 b (hd' b fr.hbc)
    have agu := colTop_agree hub
    rcases qO_claim_cone hc fr.swap hxq' hd' (mem_sdiff.1 hu).1 (by rw [hub]; exact hd' b fr.hbc)
        agu hlu with ⟨k, hk1, hk2⟩ | ⟨-, hK⟩ | ⟨-, -, -, -, h4⟩
    · rw [pt_swap] at hk1
      rw [pt_swap] at hk2
      have hkl : k < colTop D c x' c + 1 := by
        by_contra hh
        exact hproj (hD _ hk2 _ (fr.pt_le le_rfl le_rfl (by omega)))
      apply hk1
      refine hD _ hyD _ (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
        simp [fr.pt_a, fr.pt_b, fr.pt_c, ya, yb, xb] <;> omega
    · have hK' := fr.le_iff.1 hK
      have hua : colTop D c u a = x' a := by rw [colTop_apply_ne fr.hac]; exact agu a fr.hab
      have huc : (colTop D c u + Pi.single b 1 : Fin 3 → ℕ) c = colTop D c u c := by
        simp [Pi.single_apply, hcb']
      rw [huc] at hK'
      have huD : colTop D c u ∈ D := colTop_mem (mem_filter.1 (mem_sdiff.1 hu).1).1
      apply hproj
      refine hD _ huD _ (fr.le_iff.2 ⟨?_, ?_, ?_⟩) <;>
        simp [fr.pt_a, fr.pt_b, fr.pt_c, hua] <;> omega
    · omega

/-- **Fiber Lemma.** Two DS cells with the same maximal top in the same direction are equal. -/
theorem fiber (hc : ConeSet Cyl D q) {x x' : Fin 3 → ℕ} (hx : IsDS D x) (hx' : IsDS D x')
    {a : Fin 3} (ha : colTop D a x ∈ maxSet D) (heq : colTop D a x = colTop D a x') : x = x' := by
  have ag := colTop_agree heq
  rcases lt_trichotomy (x a) (x' a) with hlt | he | hgt
  · exact (fiber_aux hc hx hx' ha heq hlt).elim
  · funext i
    by_cases hi : i = a
    · rw [hi]; exact he
    · exact ag i hi
  · exact (fiber_aux hc hx' hx (heq ▸ ha) heq.symm hgt).elim

/-! ### The sets `Y_d` and the elimination predicates -/

/-- `Y_d = {y ∈ Max : y + e_d ≥ q}` (the maximal cells under the floor of `K` in direction `d`). -/
def Yset (D : Finset (Fin 3 → ℕ)) (q : Fin 3 → ℕ) (d : Fin 3) : Finset (Fin 3 → ℕ) :=
  (maxSet D).filter (fun y => ∀ i, q i ≤ (y + Pi.single d 1 : Fin 3 → ℕ) i)

/-- `Y = Y₀ ∪ Y₁ ∪ Y₂`. -/
def Yall (D : Finset (Fin 3 → ℕ)) (q : Fin 3 → ℕ) : Finset (Fin 3 → ℕ) :=
  univ.biUnion (Yset D q)

theorem mem_Yall {y : Fin 3 → ℕ} {d : Fin 3} (hy : y ∈ maxSet D) (hK : q ≤ y + Pi.single d 1) :
    y ∈ Yall D q :=
  mem_biUnion.2 ⟨d, mem_univ _, mem_filter.2 ⟨hy, hK⟩⟩

theorem card_Yall_le (hY : ∀ d, (Yset D q d).card ≤ 2) : (Yall D q).card ≤ 6 :=
  calc (Yall D q).card ≤ ∑ d, (Yset D q d).card := card_biUnion_le
    _ ≤ ∑ _d : Fin 3, 2 := sum_le_sum fun d _ => hY d
    _ = 6 := by simp

/-- The maximal directions of `x`. -/
noncomputable def maxDirs (D : Finset (Fin 3 → ℕ)) (x : Fin 3 → ℕ) : Finset (Fin 3) :=
  univ.filter (fun d => colTop D d x ∈ maxSet D)

/-- Some `u ∈ T` with smaller key has a top (in any direction) equal to `top_d x`. -/
def shBelow (D T : Finset (Fin 3 → ℕ)) (x : Fin 3 → ℕ) (d : Fin 3) : Prop :=
  ∃ u ∈ T, key u < key x ∧ ∃ d', colTop D d' u = colTop D d x

/-- Some `u ∈ T` with smaller key has the same `d`-top as `x`. -/
def ssBelow (D T : Finset (Fin 3 → ℕ)) (x : Fin 3 → ℕ) (d : Fin 3) : Prop :=
  ∃ u ∈ T, key u < key x ∧ colTop D d u = colTop D d x

/-- Some `u ∈ T` with larger key has a top (in any direction) equal to `top_d x`. -/
def shAbove (D T : Finset (Fin 3 → ℕ)) (x : Fin 3 → ℕ) (d : Fin 3) : Prop :=
  ∃ u ∈ T, key x < key u ∧ ∃ d', colTop D d' u = colTop D d x

/-- Some `u ∈ T` with larger key has the same `d`-top as `x`. -/
def ssAbove (D T : Finset (Fin 3 → ℕ)) (x : Fin 3 → ℕ) (d : Fin 3) : Prop :=
  ∃ u ∈ T, key x < key u ∧ colTop D d u = colTop D d x

noncomputable instance (D T : Finset (Fin 3 → ℕ)) (x : Fin 3 → ℕ) :
    DecidablePred (shBelow D T x) := fun _ => by unfold shBelow; infer_instance

noncomputable instance (D T : Finset (Fin 3 → ℕ)) (x : Fin 3 → ℕ) :
    DecidablePred (ssBelow D T x) := fun _ => by unfold ssBelow; infer_instance

noncomputable instance (D T : Finset (Fin 3 → ℕ)) (x : Fin 3 → ℕ) :
    DecidablePred (shAbove D T x) := fun _ => by unfold shAbove; infer_instance

noncomputable instance (D T : Finset (Fin 3 → ℕ)) (x : Fin 3 → ℕ) :
    DecidablePred (ssAbove D T x) := fun _ => by unfold ssAbove; infer_instance

theorem coneCut_nonempty (hC : LWClass Cyl L₁ h F G) (hq : ∀ i, 1 ≤ q i) :
    (coneCut Cyl q).Nonempty := by
  refine ⟨0, mem_filter.2 ⟨zero_mem hC.isLW.1 hC.nonempty, fun hh => ?_⟩⟩
  have h0 := hh 0
  have := hq 0
  simp only [Pi.zero_apply] at h0
  omega

/-! ### Theorem qO-cone -/

/-- **Theorem qO-cone, sharp form.** For every nonempty cone set, `|qO| + 1 ≤ 2t + |Y|`.

Proof: eliminate `qO` cells by increasing key. The pairs `(x, d)` (`d` maximal for `x`, `top_d x`
not shared with a `qO` cell of smaller key) inject into `Max`, and the cell of least key has two.
A cell with no such pair either has a cross pair (`top_d x` shared below, never in direction `d`),
and these pairs inject into `Y` by Lemma S′ and no-three, or it is DS; the DS pairs `(x, d)` map to
`Max` with fibres of size `≤ 2` (Fiber Lemma, no-three), so `#DS ≤ t`. -/
theorem qO_cone (hc : ConeSet Cyl D q) (hne : D.Nonempty) :
    (qO D).card + 1 ≤ 2 * (maxSet D).card + (Yall D q).card := by
  have hD := hc.down
  have ht1 := card_pos.2 (maxSet_nonempty hne)
  rcases (qO D).eq_empty_or_nonempty with hO | hO
  · rw [hO, card_empty]; omega
  have hsucc : ∀ x ∈ qO D, ∀ d, x + Pi.single d 1 ∈ D := fun x hx d => qO_succ_mem hD hx d
  have hmd : ∀ x ∈ qO D, (maxDirs D x).card = 2 := fun x hx =>
    (mem_filter.1 (mem_sdiff.1 hx).1).2.1
  have hdir : ∀ x ∈ qO D, ∀ d d', colTop D d x ∈ maxSet D → colTop D d x = colTop D d' x →
      d = d' := fun x hx d d' hd hh =>
    colTop_dir_eq (fun he => qSet_not_max hD (mem_sdiff.1 hx).1 (by rw [he] at hd; exact hd)) hh
  let N : (Fin 3 → ℕ) → Finset (Fin 3) := fun x =>
    (maxDirs D x).filter (fun d => ¬ shBelow D (qO D) x d)
  -- Step 1: the non-shared pairs inject into `Max`.
  have h1 : ((qO D).sigma N).card ≤ (maxSet D).card := by
    refine card_le_card_of_injOn (fun p => colTop D p.2 p.1) ?_ ?_
    · rintro ⟨x, d⟩ hp
      exact (mem_filter.1 (mem_filter.1 (mem_sigma.1 hp).2).1).2
    · rintro ⟨x, d⟩ hp ⟨x', d'⟩ hp' heq
      have hx : x ∈ qO D := (mem_sigma.1 hp).1
      have hx' : x' ∈ qO D := (mem_sigma.1 hp').1
      have hd : d ∈ N x := (mem_sigma.1 hp).2
      have hd' : d' ∈ N x' := (mem_sigma.1 hp').2
      simp only at heq
      have hdm := (mem_filter.1 (mem_filter.1 hd).1).2
      have hna := (mem_filter.1 hd).2
      have hna' := (mem_filter.1 hd').2
      rcases lt_trichotomy (key x) (key x') with hlt | hk | hgt
      · exact absurd ⟨x, hx, hlt, d, heq⟩ hna'
      · obtain rfl := key_inj hk
        obtain rfl := hdir x hx d d' hdm heq
        rfl
      · exact absurd ⟨x', hx', hgt, d', heq.symm⟩ hna
  -- Step 2: `|qO| + 1 ≤ Σ |N| + #{x : N x = ∅}`.
  obtain ⟨x₀, hx₀, hmin⟩ := (qO D).exists_min_image key hO
  have hN0 : (N x₀).card = 2 := by
    simp only [N]
    rw [filter_true_of_mem, hmd x₀ hx₀]
    rintro d - ⟨u, hu, hlt, -⟩
    have := hmin u hu
    omega
  have h2 : (qO D).card + 1 ≤ ((qO D).sigma N).card + ((qO D).filter (fun x => N x = ∅)).card := by
    rw [card_sigma, card_filter, ← sum_add_distrib, ← add_sum_erase _ _ hx₀]
    have hle : ∀ x ∈ (qO D).erase x₀, 1 ≤ (N x).card + if N x = ∅ then 1 else 0 := by
      intro x _
      by_cases hN : N x = ∅
      · simp [hN]
      · rw [if_neg hN]
        have := card_pos.2 (nonempty_iff_ne_empty.2 hN)
        omega
    have hs := sum_le_sum hle
    rw [sum_const, card_erase_of_mem hx₀, smul_eq_mul, mul_one] at hs
    have hx0 : 2 ≤ (N x₀).card + (if N x₀ = ∅ then 1 else 0) := by rw [hN0]; omega
    have := card_pos.2 hO
    omega
  -- Step 3: the cross pairs inject into `Y`.
  let CO := (qO D).sigma (fun x =>
    (maxDirs D x).filter (fun d => shBelow D (qO D) x d ∧ ¬ ssBelow D (qO D) x d))
  have key_case : ∀ x x' : Fin 3 → ℕ, ∀ d d' : Fin 3, x ∈ qO D → x' ∈ qO D →
      colTop D d x ∈ maxSet D → (shBelow D (qO D) x d ∧ ¬ ssBelow D (qO D) x d) →
      (shBelow D (qO D) x' d' ∧ ¬ ssBelow D (qO D) x' d') →
      colTop D d x = colTop D d' x' → key x < key x' → False := by
    intro x x' d d' hx hx' hdm hd hd' heq hlt
    obtain ⟨⟨u, hu, hku, d'', hud⟩, hns⟩ := hd
    by_cases e1 : d = d'
    · rw [e1] at heq
      exact hd'.2 ⟨x, hx, hlt, heq⟩
    by_cases e2 : d'' = d'
    · rw [e2] at hud
      exact hd'.2 ⟨u, hu, lt_trans hku hlt, hud.trans heq⟩
    have e3 : d'' ≠ d := fun hh => hns ⟨u, hu, hku, by rw [hh] at hud; exact hud⟩
    exact coneNoThree hc ⟨e1, Ne.symm e3, Ne.symm e2⟩ (hsucc x hx) (hsucc x' hx') (hsucc u hu)
      heq hud.symm hdm
  have h3 : CO.card ≤ (Yall D q).card := by
    refine card_le_card_of_injOn (fun p => colTop D p.2 p.1) ?_ ?_
    · rintro ⟨x, d⟩ hp
      have hx : x ∈ qO D := (mem_sigma.1 hp).1
      have hd := mem_filter.1 (mem_sigma.1 hp).2
      have hdm : colTop D d x ∈ maxSet D := (mem_filter.1 hd.1).2
      obtain ⟨⟨u, hu, hku, d', hud⟩, hns⟩ := hd.2
      have hdd : d' ≠ d := fun hh => hns ⟨u, hu, hku, by rw [hh] at hud; exact hud⟩
      obtain ⟨c, hdc, hd'c⟩ := exists_third hdd.symm
      exact mem_Yall hdm (coneS hc ⟨hdd.symm, hdc, hd'c⟩ (hsucc x hx c) (hsucc u hu c) hud.symm hdm)
    · rintro ⟨x, d⟩ hp ⟨x', d'⟩ hp' heq
      simp only at heq
      have hx : x ∈ qO D := (mem_sigma.1 hp).1
      have hx' : x' ∈ qO D := (mem_sigma.1 hp').1
      have hd := mem_filter.1 (mem_sigma.1 hp).2
      have hd' := mem_filter.1 (mem_sigma.1 hp').2
      have hdm : colTop D d x ∈ maxSet D := (mem_filter.1 hd.1).2
      rcases lt_trichotomy (key x) (key x') with hlt | hk | hgt
      · exact (key_case x x' d d' hx hx' hdm hd.2 hd'.2 heq hlt).elim
      · obtain rfl := key_inj hk
        obtain rfl := hdir x hx d d' hdm heq
        rfl
      · exact (key_case x' x d' d hx' hx (heq ▸ hdm) hd'.2 hd.2 heq.symm hgt).elim
  -- Step 4: DS cells.
  let DS := (qO D).filter (fun x => ∀ d ∈ maxDirs D x, ssBelow D (qO D) x d)
  have hDS_is : ∀ x ∈ DS, IsDS D x := by
    intro x hx
    obtain ⟨hxO, hall⟩ := mem_filter.1 hx
    refine ⟨hxO, fun d hd => ?_⟩
    obtain ⟨u, hu, hku, hud⟩ := hall d (mem_filter.2 ⟨mem_univ _, hd⟩)
    exact ⟨u, hu, (key_lt_iff_line (colTop_agree hud)).1 hku, hud⟩
  have h4 : 2 * DS.card ≤ 2 * (maxSet D).card := by
    have hP : (DS.sigma (maxDirs D)).card = 2 * DS.card := by
      rw [card_sigma, sum_const_nat (fun x hx => hmd x (mem_filter.1 hx).1), mul_comm]
    rw [← hP]
    refine card_le_mul_card_image_of_maps_to (f := fun p => colTop D p.2 p.1) ?_ 2 ?_
    · rintro ⟨x, d⟩ hp
      exact (mem_filter.1 (mem_sigma.1 hp).2).2
    · intro y _
      have hdist : ∀ p ∈ DS.sigma (maxDirs D), ∀ p' ∈ DS.sigma (maxDirs D),
          colTop D p.2 p.1 = colTop D p'.2 p'.1 → p ≠ p' → p.2 ≠ p'.2 := by
        rintro ⟨x, d⟩ hp ⟨x', d'⟩ hp' heq hne hdd
        simp only at heq hdd
        subst hdd
        have hx := hDS_is x (mem_sigma.1 hp).1
        have hx' := hDS_is x' (mem_sigma.1 hp').1
        have hdm : colTop D d x ∈ maxSet D := (mem_filter.1 (mem_sigma.1 hp).2).2
        obtain rfl := fiber hc hx hx' hdm heq
        exact hne rfl
      by_contra hcon
      obtain ⟨p1, hp1, p2, hp2, p3, hp3, h12, h13, h23⟩ := two_lt_card.1 (not_le.1 hcon)
      have m1 := mem_filter.1 hp1
      have m2 := mem_filter.1 hp2
      have m3 := mem_filter.1 hp3
      have e1 : colTop D p1.2 p1.1 = y := m1.2
      have e2 : colTop D p2.2 p2.1 = y := m2.2
      have e3 : colTop D p3.2 p3.1 = y := m3.2
      have d12 := hdist _ m1.1 _ m2.1 (e1.trans e2.symm) h12
      have d13 := hdist _ m1.1 _ m3.1 (e1.trans e3.symm) h13
      have d23 := hdist _ m2.1 _ m3.1 (e2.trans e3.symm) h23
      have hO1 := (mem_filter.1 (mem_sigma.1 m1.1).1).1
      have hO2 := (mem_filter.1 (mem_sigma.1 m2.1).1).1
      have hO3 := (mem_filter.1 (mem_sigma.1 m3.1).1).1
      exact coneNoThree hc ⟨d12, d13, d23⟩ (hsucc _ hO1) (hsucc _ hO2) (hsucc _ hO3)
        (e1.trans e2.symm) (e1.trans e3.symm) (mem_filter.1 (mem_sigma.1 m1.1).2).2
  -- Step 5: a cell with `N x = ∅` is DS or has a cross pair.
  have h5 : ((qO D).filter (fun x => N x = ∅)).card ≤ DS.card + CO.card := by
    calc ((qO D).filter (fun x => N x = ∅)).card ≤ (DS ∪ CO.image (fun p => p.1)).card := by
          apply card_le_card
          intro x hx
          obtain ⟨hxO, hN⟩ := mem_filter.1 hx
          rw [mem_union]
          by_cases hall : ∀ d ∈ maxDirs D x, ssBelow D (qO D) x d
          · exact Or.inl (mem_filter.2 ⟨hxO, hall⟩)
          · push Not at hall
            obtain ⟨d, hd, hns⟩ := hall
            have hsb : shBelow D (qO D) x d := by
              by_contra hsb
              have : d ∈ N x := mem_filter.2 ⟨hd, hsb⟩
              rw [hN] at this
              simp at this
            exact Or.inr (mem_image.2 ⟨⟨x, d⟩, mem_sigma.2 ⟨hxO, mem_filter.2 ⟨hd, hsb, hns⟩⟩, rfl⟩)
      _ ≤ DS.card + (CO.image (fun p => p.1)).card := card_union_le _ _
      _ ≤ DS.card + CO.card := Nat.add_le_add_left card_image_le _
  omega

/-- **Theorem qO-cone.** For `Cyl` in 𝒞 and `q ≥ (1,1,1)`, `D = Cyl ∖ (q + ℕ³)` satisfies
`|qO D| + 1 ≤ 2t + 2|Y|` (the sharp form `|qO D| + 1 ≤ 2t + |Y|` is `qO_cone`). -/
theorem qOCone (hC : LWClass Cyl L₁ h F G) (hq : ∀ i, 1 ≤ q i) :
    (qO (coneCut Cyl q)).card + 1 ≤
      2 * (maxSet (coneCut Cyl q)).card + 2 * (Yall (coneCut Cyl q) q).card := by
  have := qO_cone (coneSet_coneCut hC hq) (coneCut_nonempty hC hq)
  omega

/-! ### Lemma TF-cone -/

/-- The pairs `a < b` of elements of `S ⊆ {0,1,2}`. -/
def pairsOf (S : Finset (Fin 3)) : Finset (Fin 3 × Fin 3) :=
  (univ : Finset (Fin 3 × Fin 3)).filter (fun p => p.1 < p.2 ∧ p.1 ∈ S ∧ p.2 ∈ S)

/-- The three pairs `a < b` of directions. -/
def pairs3 : Finset (Fin 3 × Fin 3) := (univ : Finset (Fin 3 × Fin 3)).filter (fun p => p.1 < p.2)

theorem fin3_pairs : ∀ S : Finset (Fin 3), S.card ≤ min 1 S.card + (pairsOf S).card := by
  unfold pairsOf; decide

theorem pairs3_card : pairs3.card = 3 := by decide

theorem third_unique : ∀ {a b c c' : Fin 3}, a ≠ b → a ≠ c → b ≠ c → a ≠ c' → b ≠ c' → c = c' := by
  decide

/-- `Φ(a, b)`: tripods `x` with a tripod partner of larger key with the same `a`-top, and a tripod
partner `u` of larger key with the same `b`-top such that `top_c(u) + e_a ∈ K` (`c` the third
direction). -/
noncomputable def phiSet (D : Finset (Fin 3 → ℕ)) (q : Fin 3 → ℕ) (a b : Fin 3) :
    Finset (Fin 3 → ℕ) :=
  (triSet D).filter (fun x => ∃ c, a ≠ c ∧ b ≠ c ∧ ssAbove D (triSet D) x a ∧
    ∃ u ∈ triSet D, key x < key u ∧ colTop D b u = colTop D b x ∧
      ∀ i, q i ≤ (colTop D c u + Pi.single a 1 : Fin 3 → ℕ) i)

theorem mem_phiSet (fr : Frame a b c) {x : Fin 3 → ℕ} (hx : x ∈ phiSet D q a b) :
    x ∈ triSet D ∧ (∃ u ∈ triSet D, key x < key u ∧ colTop D a u = colTop D a x) ∧
      ∃ u ∈ triSet D, key x < key u ∧ colTop D b u = colTop D b x ∧
        q ≤ colTop D c u + Pi.single a 1 := by
  obtain ⟨hxT, c', h1, h2, hss, u, hu, hk, hb, hK⟩ := mem_filter.1 hx
  obtain rfl := third_unique fr.hab h1 h2 fr.hac fr.hbc
  exact ⟨hxT, hss, u, hu, hk, hb, hK⟩

/-- A partner of larger key with the same `a`-top lies above `x` on the `a`-line. -/
theorem partner_line {x u : Fin 3 → ℕ} {a : Fin 3} (hk : key x < key u)
    (h : colTop D a u = colTop D a x) : (∀ i, i ≠ a → u i = x i) ∧ x a < u a :=
  ⟨colTop_agree h, (key_lt_iff_line (fun i hi => (colTop_agree h i hi).symm)).1 hk⟩

/-- (iii) `x ∈ Φ(a, b)` has `x_a + 1 = q_a` and `x_c < q_c`. -/
theorem phi_iii (hc : ConeSet Cyl D q) (fr : Frame a b c) {x : Fin 3 → ℕ}
    (hx : x ∈ phiSet D q a b) : x a + 1 = q a ∧ x c < q c := by
  obtain ⟨-, -, u, hu, hk, hb, hK⟩ := mem_phiSet fr hx
  obtain ⟨ag, -⟩ := partner_line hk hb
  have hD := hc.down
  have hca := fr.hac.symm; have hcb := fr.hbc.symm; have hba := fr.hab.symm
  have hyD : colTop D c u ∈ D := (mem_filter.1 (triSet_top hu c)).1
  have ya : colTop D c u a = x a := by rw [colTop_apply_ne fr.hac]; exact ag a fr.hab
  have yb : colTop D c u b = u b := colTop_apply_ne fr.hbc
  have hK' := fr.le_iff.1 hK
  have ka : (colTop D c u + Pi.single a 1 : Fin 3 → ℕ) a = x a + 1 := by simp [ya]
  have kb : (colTop D c u + Pi.single a 1 : Fin 3 → ℕ) b = u b := by
    simp [Pi.single_apply, hba, yb]
  have kc : (colTop D c u + Pi.single a 1 : Fin 3 → ℕ) c = colTop D c u c := by
    simp [Pi.single_apply, hca]
  rw [ka, kb, kc] at hK'
  have n1 : ¬ (q a ≤ x a ∧ q b ≤ u b ∧ q c ≤ colTop D c u c) := fun hh =>
    hc.not_K hyD (fr.le_iff.2 ⟨by rw [ya]; exact hh.1, by rw [yb]; exact hh.2.1, hh.2.2⟩)
  have hs := triSet_succ_mem hD hu a
  have n2 : ¬ (q a ≤ x a + 1 ∧ q b ≤ u b ∧ q c ≤ x c) := fun hh =>
    hc.not_K hs (fr.le_iff.2 ⟨by simpa [ag a fr.hab] using hh.1,
      by simpa [Pi.single_apply, hba] using hh.2.1,
      by simpa [Pi.single_apply, hca, ag c hcb] using hh.2.2⟩)
  refine ⟨?_, ?_⟩
  · by_contra hh
    exact n1 ⟨by omega, hK'.2.1, hK'.2.2⟩
  · by_contra hh
    exact n2 ⟨hK'.1, hK'.2.1, by omega⟩

theorem phi_iv_aux (hc : ConeSet Cyl D q) (fr : Frame a b c) {x x' : Fin 3 → ℕ}
    (hx : x ∈ phiSet D q a b) (hx' : x' ∈ phiSet D q a b) (hlt : x c < x' c) : False := by
  obtain ⟨-, ⟨u, hu, hk, ha⟩, -⟩ := mem_phiSet fr hx
  obtain ⟨hxT', -, -⟩ := mem_phiSet fr hx'
  obtain ⟨ag, hlu⟩ := partner_line hk ha
  have i1 := phi_iii hc fr hx
  have i2 := phi_iii hc fr hx'
  have hD := hc.down
  have hca := fr.hac.symm; have hcb := fr.hbc.symm; have hba := fr.hab.symm
  have fr' : Frame a c b := ⟨fr.hac, fr.hab, fr.hbc.symm⟩
  have uc : u c = x c := ag c hca
  rcases coneP hc fr' (x := x') (x' := u) (triSet_top hxT' b) (triSet_top hu b)
      (triSet_succ_mem hD hxT' a) (triSet_succ_mem hD hu c) (by omega) (by omega) with hK | hK
  · have := (fr'.le_iff.1 hK).2.1
    simp [Pi.single_apply, hca, colTop_apply_ne fr.hbc.symm] at this
    omega
  · have hK' := fr'.le_iff.1 hK
    have yD : colTop D b u ∈ D := (mem_filter.1 (triSet_top hu b)).1
    have ka : (colTop D b u + Pi.single c 1 : Fin 3 → ℕ) a = u a := by
      simp [Pi.single_apply, fr.hac, colTop_apply_ne fr.hab]
    have kc : (colTop D b u + Pi.single c 1 : Fin 3 → ℕ) c = x c + 1 := by
      simp [colTop_apply_ne hcb, uc]
    have kb : (colTop D b u + Pi.single c 1 : Fin 3 → ℕ) b = colTop D b u b := by
      simp [Pi.single_apply, fr.hbc]
    rw [ka, kc, kb] at hK'
    have n1 : ¬ (q a ≤ u a ∧ q c ≤ x c ∧ q b ≤ colTop D b u b) := fun hh =>
      hc.not_K yD (fr'.le_iff.2 ⟨by rw [colTop_apply_ne fr.hab]; exact hh.1,
        by rw [colTop_apply_ne hcb, uc]; exact hh.2.1, hh.2.2⟩)
    by_cases hh : q c ≤ x c
    · exact n1 ⟨hK'.1, hh, hK'.2.2⟩
    · omega

/-- (iv) All members of `Φ(a, b)` have the same `c`-coordinate. -/
theorem phi_iv (hc : ConeSet Cyl D q) (fr : Frame a b c) {x x' : Fin 3 → ℕ}
    (hx : x ∈ phiSet D q a b) (hx' : x' ∈ phiSet D q a b) : x c = x' c := by
  rcases lt_trichotomy (x c) (x' c) with hlt | he | hgt
  · exact (phi_iv_aux hc fr hx hx' hlt).elim
  · exact he
  · exact (phi_iv_aux hc fr hx' hx hgt).elim

/-- (v), first part: for members `x <_b x'` of `Φ(a, b)`, `x'_b ≥ q_b` or `x_b + 1 = q_b`. -/
theorem phi_v1 (hc : ConeSet Cyl D q) (fr : Frame a b c) {x x' : Fin 3 → ℕ}
    (hx : x ∈ phiSet D q a b) (hx' : x' ∈ phiSet D q a b) (hlt : x b < x' b) :
    q b ≤ x' b ∨ x b + 1 = q b := by
  obtain ⟨-, ⟨u, hu, hk, ha⟩, -⟩ := mem_phiSet fr hx
  obtain ⟨hxT', -, -⟩ := mem_phiSet fr hx'
  obtain ⟨ag, hlu⟩ := partner_line hk ha
  have i1 := phi_iii hc fr hx
  have i2 := phi_iii hc fr hx'
  have hD := hc.down
  have hca := fr.hac.symm; have hcb := fr.hbc.symm; have hba := fr.hab.symm
  have ub : u b = x b := ag b hba
  rcases coneP hc fr (x := x') (x' := u) (triSet_top hxT' c) (triSet_top hu c)
      (triSet_succ_mem hD hxT' a) (triSet_succ_mem hD hu b) (by omega) (by omega) with hK | hK
  · left
    have := (fr.le_iff.1 hK).2.1
    simpa [Pi.single_apply, hba, colTop_apply_ne fr.hbc] using this
  · right
    have hK' := fr.le_iff.1 hK
    have yD : colTop D c u ∈ D := (mem_filter.1 (triSet_top hu c)).1
    have ka : (colTop D c u + Pi.single b 1 : Fin 3 → ℕ) a = u a := by
      simp [Pi.single_apply, fr.hab, colTop_apply_ne fr.hac]
    have kb : (colTop D c u + Pi.single b 1 : Fin 3 → ℕ) b = x b + 1 := by
      simp [colTop_apply_ne fr.hbc, ub]
    have kc : (colTop D c u + Pi.single b 1 : Fin 3 → ℕ) c = colTop D c u c := by
      simp [Pi.single_apply, hcb]
    rw [ka, kb, kc] at hK'
    have n1 : ¬ (q a ≤ u a ∧ q b ≤ x b ∧ q c ≤ colTop D c u c) := fun hh =>
      hc.not_K yD (fr.le_iff.2 ⟨by rw [colTop_apply_ne fr.hac]; exact hh.1,
        by rw [colTop_apply_ne fr.hbc, ub]; exact hh.2.1, hh.2.2⟩)
    by_cases hh : q b ≤ x b
    · exact (n1 ⟨hK'.1, hh, hK'.2.2⟩).elim
    · omega

/-- (v) `|Φ(a, b)| ≤ 2` when `|Y_a| ≤ 2`. -/
theorem phi_card (hc : ConeSet Cyl D q) (fr : Frame a b c) (hY : (Yset D q a).card ≤ 2) :
    (phiSet D q a b).card ≤ 2 := by
  have hD := hc.down
  have hca := fr.hac.symm; have hcb := fr.hbc.symm; have hba := fr.hab.symm
  have hsplit := card_filter_add_card_filter_not (s := phiSet D q a b) (fun x => x b < q b)
  -- members with `x_b < q_b`: at most one
  have hM1 : ((phiSet D q a b).filter (fun x => x b < q b)).card ≤ 1 := by
    refine card_le_one.2 fun x hx x' hx' => ?_
    obtain ⟨hx, hxb⟩ := mem_filter.1 hx
    obtain ⟨hx', hxb'⟩ := mem_filter.1 hx'
    have i1 := phi_iii hc fr hx
    have i2 := phi_iii hc fr hx'
    have e4 := phi_iv hc fr hx hx'
    rcases lt_trichotomy (x b) (x' b) with hlt | he | hgt
    · rcases phi_v1 hc fr hx hx' hlt with hh | hh <;> omega
    · exact fr.ext (by omega) he e4
    · rcases phi_v1 hc fr hx' hx hgt with hh | hh <;> omega
  -- members with `x_b ≥ q_b`: their `c`-tops lie in `Y_a`, minus one point
  have hM2 : ((phiSet D q a b).filter (fun x => ¬ x b < q b)).card ≤ 1 := by
    rcases ((phiSet D q a b).filter (fun x => ¬ x b < q b)).eq_empty_or_nonempty with h0 | hne
    · rw [h0, card_empty]; omega
    obtain ⟨x₀, hx₀, hmax⟩ := ((phiSet D q a b).filter (fun x => ¬ x b < q b)).exists_max_image
      (fun x => x b) hne
    obtain ⟨hx₀Φ, -⟩ := mem_filter.1 hx₀
    obtain ⟨-, -, u₀, hu₀, hk₀, hb₀, hK₀⟩ := mem_phiSet fr hx₀Φ
    obtain ⟨-, hl₀⟩ := partner_line hk₀ hb₀
    have hy₀ : colTop D c u₀ ∈ Yset D q a := mem_filter.2 ⟨triSet_top hu₀ c, hK₀⟩
    have hcard := card_le_card_of_injOn (fun x => colTop D c x)
      (s := (phiSet D q a b).filter (fun x => ¬ x b < q b)) (t := (Yset D q a).erase (colTop D c u₀))
      (by
        intro x hx
        obtain ⟨hxΦ, hqb⟩ := mem_filter.1 hx
        obtain ⟨hxT, -, u, hu, hk, hb, hK⟩ := mem_phiSet fr hxΦ
        obtain ⟨ag, hl⟩ := partner_line hk hb
        have i1 := phi_iii hc fr hxΦ
        refine mem_erase.2 ⟨fun he => ?_, mem_filter.2 ⟨triSet_top hxT c, ?_⟩⟩
        · have e := congrFun (show colTop D c x = colTop D c u₀ from he) b
          rw [colTop_apply_ne fr.hbc, colTop_apply_ne fr.hbc] at e
          have := hmax x hx
          omega
        · have hK' := (fr.le_iff.1 hK).2.2
          have kc : (colTop D c u + Pi.single a 1 : Fin 3 → ℕ) c = colTop D c u c := by
            simp [Pi.single_apply, hca]
          rw [kc] at hK'
          have huD : colTop D c u ∈ D := (mem_filter.1 (triSet_top hu c)).1
          have hz : update x c (colTop D c u c) ∈ D := by
            refine hD _ huD _ (fr.le_iff.2 ⟨?_, ?_, ?_⟩)
            · simp [update_apply, fr.hac, colTop_apply_ne fr.hac, ag a fr.hab]
            · simp [update_apply, fr.hbc, colTop_apply_ne fr.hbc]; omega
            · simp
          have hxc : x c ≤ colTop D c u c := by
            rw [colTop_apply_self, ag c hcb]; omega
          have hle := le_colTop_c (x := x) (c := c) hz (fun i hi => by simp [update_apply, hi])
            (by simpa using hxc)
          simp only [update_self] at hle
          show q ≤ colTop D c x + Pi.single a 1
          refine fr.le_iff.2 ⟨?_, ?_, ?_⟩
          · simp [colTop_apply_ne fr.hac]; omega
          · simp [Pi.single_apply, hba, colTop_apply_ne fr.hbc]; omega
          · simp [Pi.single_apply, hca]; omega)
      (by
        intro x hx x' hx' he
        have hxΦ := (mem_filter.1 hx).1
        have hxΦ' := (mem_filter.1 hx').1
        have ag := colTop_agree (D := D) (x := x') (u := x) he
        exact fr.ext (ag a fr.hac) (ag b fr.hbc) (phi_iv hc fr hxΦ hxΦ'))
    rw [card_erase_of_mem hy₀] at hcard
    omega
  omega

/-- Two same-direction shares of a tripod in directions `a ≠ b` put it into `Φ(a, b)` or `Φ(b, a)`
(Lemma P′). -/
theorem ss_pair_phi (hc : ConeSet Cyl D q) (fr : Frame a b c) {x : Fin 3 → ℕ}
    (hx : x ∈ triSet D) (ha : ssAbove D (triSet D) x a) (hb : ssAbove D (triSet D) x b) :
    x ∈ phiSet D q a b ∨ x ∈ phiSet D q b a := by
  obtain ⟨u, hu, hku, hua⟩ := ha
  obtain ⟨u', hu', hku', hub⟩ := hb
  obtain ⟨ag, hl⟩ := partner_line hku hua
  obtain ⟨ag', hl'⟩ := partner_line hku' hub
  have hD := hc.down
  rcases coneP hc fr (x := u') (x' := u) (triSet_top hu' c) (triSet_top hu c)
      (triSet_succ_mem hD hu' a) (triSet_succ_mem hD hu b) (by rw [ag' a fr.hab]; exact hl)
      (by rw [ag b fr.hab.symm]; exact hl') with hK | hK
  · left
    exact mem_filter.2 ⟨hx, c, fr.hac, fr.hbc, ⟨u, hu, hku, hua⟩, u', hu', hku', hub, hK⟩
  · right
    exact mem_filter.2 ⟨hx, c, fr.hbc, fr.hac, ⟨u', hu', hku', hub⟩, u, hu, hku, hua, hK⟩

/-- **Lemma TF-cone, sharp form.** For a cone set with `|Y_d| ≤ 2` for every `d`:
`2|Tri| ≤ t + |Y| + 11`.

Proof: eliminate tripods by decreasing key. With `N(x)` the tops of `x` not shared with a tripod
of larger key, `Σ |N| ≤ t`. A shared top is a cross share (never in the same direction; these
inject into `Y` by Lemma S′ and no-three) or a same share. Two same shares in directions `a ≠ b`
put `x` into `Φ(a, b)` or `Φ(b, a)` (Lemma P′), so `|same shares of x| ≤ [≠ ∅] + #pairs`, the tripod
of largest key has none, and `Σ_x #pairs ≤ Σ_{a<b} (|Φ(a,b)| + |Φ(b,a)|) ≤ 12`. -/
theorem tf_cone (hc : ConeSet Cyl D q) (hY : ∀ d, (Yset D q d).card ≤ 2) :
    2 * (triSet D).card ≤ (maxSet D).card + (Yall D q).card + 11 := by
  have hD := hc.down
  rcases (triSet D).eq_empty_or_nonempty with hT | hT
  · rw [hT, card_empty]; omega
  have hsucc : ∀ x ∈ triSet D, ∀ d, x + Pi.single d 1 ∈ D := fun x hx d =>
    triSet_succ_mem hD hx d
  have hdir : ∀ x ∈ triSet D, ∀ d d', colTop D d x = colTop D d' x → d = d' :=
    fun x hx d d' hh => colTop_dir_eq (fun he => (mem_sdiff.1 (mem_filter.1 hx).1).2
      (by have := triSet_top hx d; rw [he] at this; exact this)) hh
  let Nt : (Fin 3 → ℕ) → Finset (Fin 3) := fun x =>
    univ.filter (fun d => ¬ shAbove D (triSet D) x d)
  let SS : (Fin 3 → ℕ) → Finset (Fin 3) := fun x => univ.filter (fun d => ssAbove D (triSet D) x d)
  let SC : (Fin 3 → ℕ) → Finset (Fin 3) := fun x =>
    univ.filter (fun d => shAbove D (triSet D) x d ∧ ¬ ssAbove D (triSet D) x d)
  have hper : ∀ x, 3 ≤ (Nt x).card + (SS x).card + (SC x).card := by
    intro x
    have hsub : (univ : Finset (Fin 3)) ⊆ Nt x ∪ SS x ∪ SC x := by
      intro d _
      by_cases h1 : shAbove D (triSet D) x d
      · by_cases h2 : ssAbove D (triSet D) x d
        · exact mem_union_left _ (mem_union_right _ (mem_filter.2 ⟨mem_univ _, h2⟩))
        · exact mem_union_right _ (mem_filter.2 ⟨mem_univ _, h1, h2⟩)
      · exact mem_union_left _ (mem_union_left _ (mem_filter.2 ⟨mem_univ _, h1⟩))
    have h0 := card_le_card hsub
    have h2 := card_union_le (Nt x ∪ SS x) (SC x)
    have h3 := card_union_le (Nt x) (SS x)
    rw [card_univ, Fintype.card_fin] at h0
    omega
  -- Step 1: non-shared tops inject into `Max`.
  have h1 : ((triSet D).sigma Nt).card ≤ (maxSet D).card := by
    refine card_le_card_of_injOn (fun p => colTop D p.2 p.1) ?_ ?_
    · rintro ⟨x, d⟩ hp
      exact triSet_top (mem_sigma.1 hp).1 d
    · rintro ⟨x, d⟩ hp ⟨x', d'⟩ hp' heq
      have hx : x ∈ triSet D := (mem_sigma.1 hp).1
      have hx' : x' ∈ triSet D := (mem_sigma.1 hp').1
      have hna := (mem_filter.1 (mem_sigma.1 hp).2).2
      have hna' := (mem_filter.1 (mem_sigma.1 hp').2).2
      simp only at heq
      rcases lt_trichotomy (key x) (key x') with hlt | hk | hgt
      · exact absurd ⟨x', hx', hlt, d', heq.symm⟩ hna
      · obtain rfl := key_inj hk
        obtain rfl := hdir x hx d d' heq
        rfl
      · exact absurd ⟨x, hx, hgt, d, heq⟩ hna'
  -- Step 2: cross shares inject into `Y`.
  have key_case : ∀ x x' : Fin 3 → ℕ, ∀ d d' : Fin 3, x ∈ triSet D → x' ∈ triSet D →
      (shAbove D (triSet D) x d ∧ ¬ ssAbove D (triSet D) x d) →
      (shAbove D (triSet D) x' d' ∧ ¬ ssAbove D (triSet D) x' d') →
      colTop D d x = colTop D d' x' → key x < key x' → False := by
    intro x x' d d' hx hx' hd hd' heq hlt
    obtain ⟨⟨u, hu, hku, d'', hud⟩, hns'⟩ := hd'
    by_cases e1 : d = d'
    · rw [← e1] at heq
      exact hd.2 ⟨x', hx', hlt, heq.symm⟩
    by_cases e2 : d'' = d
    · rw [e2] at hud
      exact hd.2 ⟨u, hu, lt_trans hlt hku, hud.trans heq.symm⟩
    have e3 : d'' ≠ d' := fun hh => hns' ⟨u, hu, hku, by rw [hh] at hud; exact hud⟩
    exact coneNoThree hc ⟨e1, Ne.symm e2, Ne.symm e3⟩ (hsucc x hx) (hsucc x' hx') (hsucc u hu)
      heq (heq.trans hud.symm) (triSet_top hx d)
  have h2 : ((triSet D).sigma SC).card ≤ (Yall D q).card := by
    refine card_le_card_of_injOn (fun p => colTop D p.2 p.1) ?_ ?_
    · rintro ⟨x, d⟩ hp
      have hx : x ∈ triSet D := (mem_sigma.1 hp).1
      obtain ⟨⟨u, hu, hku, d', hud⟩, hns⟩ := (mem_filter.1 (mem_sigma.1 hp).2).2
      have hdd : d' ≠ d := fun hh => hns ⟨u, hu, hku, by rw [hh] at hud; exact hud⟩
      obtain ⟨c, hdc, hd'c⟩ := exists_third hdd.symm
      exact mem_Yall (triSet_top hx d) (coneS hc ⟨hdd.symm, hdc, hd'c⟩ (hsucc x hx c)
        (hsucc u hu c) hud.symm (triSet_top hx d))
    · rintro ⟨x, d⟩ hp ⟨x', d'⟩ hp' heq
      simp only at heq
      have hx : x ∈ triSet D := (mem_sigma.1 hp).1
      have hx' : x' ∈ triSet D := (mem_sigma.1 hp').1
      have hd := (mem_filter.1 (mem_sigma.1 hp).2).2
      have hd' := (mem_filter.1 (mem_sigma.1 hp').2).2
      rcases lt_trichotomy (key x) (key x') with hlt | hk | hgt
      · exact (key_case x x' d d' hx hx' hd hd' heq hlt).elim
      · obtain rfl := key_inj hk
        obtain rfl := hdir x hx d d' heq
        rfl
      · exact (key_case x' x d' d hx' hx hd' hd heq.symm hgt).elim
  -- Step 3: same shares.
  obtain ⟨x₀, hx₀, hmax⟩ := (triSet D).exists_max_image key hT
  have hSS0 : SS x₀ = ∅ := by
    simp only [SS]
    rw [filter_eq_empty_iff]
    rintro d - ⟨u, hu, hlt, -⟩
    have := hmax u hu
    omega
  have h3a : ∑ x ∈ triSet D, min 1 (SS x).card ≤ (triSet D).card - 1 := by
    rw [← add_sum_erase _ _ hx₀, hSS0, card_empty]
    have := sum_le_sum (s := (triSet D).erase x₀) (fun x _ => min_le_left 1 (SS x).card)
    rw [sum_const, card_erase_of_mem hx₀, smul_eq_mul, mul_one] at this
    omega
  have h3b : ((triSet D).sigma (fun x => pairsOf (SS x))).card ≤ 12 := by
    refine le_trans (card_le_card_of_injOn
      (fun p : (Σ _ : Fin 3 → ℕ, Fin 3 × Fin 3) => (⟨p.2, p.1⟩ : Σ _ : Fin 3 × Fin 3, Fin 3 → ℕ))
      (t := pairs3.sigma (fun p => phiSet D q p.1 p.2 ∪ phiSet D q p.2 p.1)) ?_ ?_) ?_
    · rintro ⟨x, p⟩ hp
      have hx : x ∈ triSet D := (mem_sigma.1 hp).1
      obtain ⟨-, hlt, h1, h2⟩ := mem_filter.1 (mem_sigma.1 hp).2
      have hne : p.1 ≠ p.2 := ne_of_lt hlt
      obtain ⟨c, hc1, hc2⟩ := exists_third hne
      refine mem_sigma.2 ⟨mem_filter.2 ⟨mem_univ _, hlt⟩, mem_union.2 ?_⟩
      exact ss_pair_phi hc ⟨hne, hc1, hc2⟩ hx (mem_filter.1 h1).2 (mem_filter.1 h2).2
    · rintro ⟨x, p⟩ - ⟨x', p'⟩ - heq
      simp only [Sigma.mk.inj_iff, heq_eq_eq] at heq ⊢
      exact ⟨heq.2, heq.1⟩
    · rw [card_sigma]
      calc ∑ p ∈ pairs3, (phiSet D q p.1 p.2 ∪ phiSet D q p.2 p.1).card
          ≤ ∑ _p ∈ pairs3, 4 := by
            apply sum_le_sum
            intro p hp
            have hne : p.1 ≠ p.2 := ne_of_lt (mem_filter.1 hp).2
            obtain ⟨c, h1, h2⟩ := exists_third hne
            have := card_union_le (phiSet D q p.1 p.2) (phiSet D q p.2 p.1)
            have := phi_card hc ⟨hne, h1, h2⟩ (hY p.1)
            have := phi_card hc ⟨hne.symm, h2, h1⟩ (hY p.2)
            omega
        _ = 12 := by rw [sum_const, pairs3_card]; rfl
  have h3 : ∑ x ∈ triSet D, (SS x).card ≤ (triSet D).card - 1 + 12 := by
    have hle : ∀ x ∈ triSet D, (SS x).card ≤ min 1 (SS x).card + (pairsOf (SS x)).card :=
      fun x _ => fin3_pairs (SS x)
    have := sum_le_sum hle
    rw [sum_add_distrib] at this
    have hc3 : ((triSet D).sigma (fun x => pairsOf (SS x))).card =
        ∑ x ∈ triSet D, (pairsOf (SS x)).card := card_sigma _ _
    omega
  have hsum3 : 3 * (triSet D).card ≤
      ∑ x ∈ triSet D, ((Nt x).card + (SS x).card + (SC x).card) := by
    have := sum_le_sum (fun x (_ : x ∈ triSet D) => hper x)
    rwa [sum_const, smul_eq_mul, mul_comm] at this
  rw [sum_add_distrib, sum_add_distrib] at hsum3
  have e1 : ((triSet D).sigma Nt).card = ∑ x ∈ triSet D, (Nt x).card := card_sigma _ _
  have e2 : ((triSet D).sigma SC).card = ∑ x ∈ triSet D, (SC x).card := card_sigma _ _
  have := card_pos.2 hT
  omega

/-- **Lemma TF-cone.** For `Cyl` in 𝒞, `q ≥ (1,1,1)` and `|Y_d| ≤ 2` for every `d`,
`D = Cyl ∖ (q + ℕ³)` satisfies `2|Tri| ≤ t + 17`. -/
theorem tfCone (hC : LWClass Cyl L₁ h F G) (hq : ∀ i, 1 ≤ q i)
    (hY : ∀ d, (Yset (coneCut Cyl q) q d).card ≤ 2) :
    2 * (triSet (coneCut Cyl q)).card ≤ (maxSet (coneCut Cyl q)).card + 17 := by
  have h1 := tf_cone (coneSet_coneCut hC hq) hY
  have h2 := card_Yall_le hY
  omega

/-! ### The cone δ-bound -/

/-- **Cone δ-bound, sharp form.** For a nonempty cone set with `|Y_d| ≤ 2` for every `d`:
`2m ≤ H + 6t + 2|Y| + 10`. -/
theorem coneDelta_sharp (hc : ConeSet Cyl D q) (hne : D.Nonempty)
    (hY : ∀ d, (Yset D q d).card ≤ 2) :
    2 * D.card ≤ ∑ x ∈ D, hsum D x + 6 * (maxSet D).card + 2 * (Yall D q).card + 10 := by
  have h1 := cht D
  have h2 := card_qU_add_card_qO D
  have h3 := qU_cone hc
  have h4 := qO_cone hc hne
  have h5 := tf_cone hc hY
  omega

/-- **Cone δ-bound.** For `Cyl` in 𝒞, `q ≥ (1,1,1)` and `|Y_d| ≤ 2` for every `d`,
`D = Cyl ∖ (q + ℕ³)` satisfies `2m ≤ H + 6C + 30`, i.e. `δ = H − (m − 1) ≥ m − 6C − 29`. -/
theorem coneDeltaBound (hC : LWClass Cyl L₁ h F G) (hq : ∀ i, 1 ≤ q i)
    (hY : ∀ d, (Yset (coneCut Cyl q) q d).card ≤ 2) :
    2 * (coneCut Cyl q).card ≤ ∑ x ∈ coneCut Cyl q, hsum (coneCut Cyl q) x +
      6 * ∑ c, (faceCorners (coneCut Cyl q) c).card + 30 := by
  have h1 := coneDelta_sharp (coneSet_coneCut hC hq) (coneCut_nonempty hC hq) hY
  have h2 := typeBound_cone hC hq
  have h3 := card_Yall_le hY
  omega

/-- **Cone threshold (δ ≥ 0).** Under the hypotheses of `coneDeltaBound`, `m ≥ 281` implies
`m ≤ H + 1`. -/
theorem coneThreshold (hC : LWClass Cyl L₁ h F G) (hq : ∀ i, 1 ≤ q i)
    (hY : ∀ d, (Yset (coneCut Cyl q) q d).card ≤ 2) (hm : 281 ≤ (coneCut Cyl q).card) :
    (coneCut Cyl q).card ≤ ∑ x ∈ coneCut Cyl q, hsum (coneCut Cyl q) x + 1 := by
  have h1 := coneDeltaBound hC hq hY
  have h2 := cornerArea (coneSet_coneCut hC hq).down (coneCut_nonempty hC hq)
  set C := ∑ c, (faceCorners (coneCut Cyl q) c).card
  have h6 : 6 * C + 29 ≤ (coneCut Cyl q).card := by
    by_contra hcon
    have h43 : 43 ≤ C := by omega
    nlinarith
  omega

/-- **Cone threshold (δ ≥ −1).** Under the hypotheses of `coneDeltaBound`, `m ≥ 280` implies
`m ≤ H + 2`. -/
theorem coneThreshold' (hC : LWClass Cyl L₁ h F G) (hq : ∀ i, 1 ≤ q i)
    (hY : ∀ d, (Yset (coneCut Cyl q) q d).card ≤ 2) (hm : 280 ≤ (coneCut Cyl q).card) :
    (coneCut Cyl q).card ≤ ∑ x ∈ coneCut Cyl q, hsum (coneCut Cyl q) x + 2 := by
  have h1 := coneDeltaBound hC hq hY
  have h2 := cornerArea (coneSet_coneCut hC hq).down (coneCut_nonempty hC hq)
  set C := ∑ c, (faceCorners (coneCut Cyl q) c).card
  have h6 : 6 * C + 28 ≤ (coneCut Cyl q).card := by
    by_contra hcon
    have h43 : 43 ≤ C := by omega
    nlinarith
  omega

/-- The hypotheses of `tfCone` and `coneDeltaBound` can be met: for `Cyl = [0,2)³` and
`q = (1,1,1)`, `|Y_d| ≤ 2` for every `d` (kernel `decide`). -/
theorem box2_Yset_le : ∀ d, (Yset (coneCut box2 ![1, 1, 1]) ![1, 1, 1] d).card ≤ 2 := by decide

end ConeForest

end CornerArea

end NumericalSemigroup
