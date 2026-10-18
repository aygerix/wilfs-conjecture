import Wilf.CornerArea

/-!
# Lemma T′ (type bound for the cone class)

Formalization of `.research/PROOFS.md`, "Lemma T' (cone class)". Notation as in
`Wilf.CornerArea` (`maxSet`, `faceCorners`, `LWClass`, `phiS`, `cornerF`, `cornerG`).

Let `Cyl` be in the Loomis–Whitney class 𝒞 (`LWClass Cyl L₁ h F G`) and `q : Fin 3 → ℕ` with
`q i ≥ 1` for all `i`. Put `D = coneCut Cyl q = Cyl ∖ (q + ℕ³)`. Then

* `faceCorners_coneCut`: `faceCorners D c = faceCorners Cyl c` for every `c` (this needs only
  `q ≥ (1,1,1)`, not the class hypothesis);
* `typeBound_cone` (**Lemma T′**): `|Max D| ≤ Σ_c |faceCorners D c|`, i.e. `t ≤ C`.

The hypothesis `q ∈ Cyl` of the paper is not needed (if `q ∉ Cyl` then `D = Cyl` and Lemma T
already gives `t ≤ C − 2`); `typeBound_cone'` restates the theorem with it.

Proof. `D` is a column set: `x ∈ D ↔ x₂ < ψ(x₀, x₁)` with `ψ = psiC`, `ψ(p) = min(φ*(p), q₂)` on the
quadrant `Q = [q₀,∞) × [q₁,∞)` and `ψ = φ*` elsewhere; `ψ` is antitone. For a maximal `x` put
`r = ψ(x₀+1, x₁)`, `u = ψ(x₀, x₁+1)` (then `r, u ≤ x₂ < ψ(x₀, x₁)`). As in Lemma T, `x` is charged to
the level at which its slice corner is born, with two extra possible births caused by `Q`:
* `r = u = 0`: `x ↦ (x₀, x₁, 0)`, a corner of the base face;
* `u ≤ r ≠ 0`, not (`x₀ + 1 = q₀`, `x₁ ≥ q₁`, `r = q₂`): then `r = F(x₀+1) < F(x₀)` and
  `x ↦ (x₀, 0, F(x₀) − 1) ∈ corners(A₁) ∖ {cornerF}` (injective as in Lemma T);
* `u ≤ r`, `x₀ + 1 = q₀`, `x₁ ≥ q₁`, `r = q₂` (the top of column `q₀ − 1`): at most one such `x`;
* `r < u`, not (`x₁ + 1 = q₁`, `x₀ ≥ q₀`, `u = q₂`): `u = G(x₁+1) < G(x₁)` and
  `x ↦ (0, x₁, G(x₁) − 1) ∈ corners(A₀) ∖ {cornerG}`;
* `r < u`, `x₁ + 1 = q₁`, `x₀ ≥ q₀`, `u = q₂` (the end of row `q₁ − 1`): at most one such `x`.
Hence `t ≤ k₂ + (k₁ − 1) + 1 + (k₀ − 1) + 1 = C`.
-/

namespace NumericalSemigroup

open Finset

namespace CornerArea

section ConeType

/-- `Cyl ∖ (q + ℕ³)`: remove the orthant above `q`. -/
def coneCut (Cyl : Finset (Fin 3 → ℕ)) (q : Fin 3 → ℕ) : Finset (Fin 3 → ℕ) :=
  Cyl.filter (fun x => ¬ ∀ i, q i ≤ x i)

theorem forall_fin3_le {q x : Fin 3 → ℕ} :
    (∀ i, q i ≤ x i) ↔ q 0 ≤ x 0 ∧ q 1 ≤ x 1 ∧ q 2 ≤ x 2 :=
  ⟨fun h => ⟨h 0, h 1, h 2⟩, fun ⟨h0, h1, h2⟩ i => by fin_cases i <;> assumption⟩

/-- **The faces of `Cyl ∖ (q + ℕ³)` and their corners are those of `Cyl`** when `q ≥ (1,1,1)`
(any finite `Cyl`). -/
theorem faceCorners_coneCut (Cyl : Finset (Fin 3 → ℕ)) {q : Fin 3 → ℕ} (hq : ∀ i, 1 ≤ q i)
    (c : Fin 3) : faceCorners (coneCut Cyl q) c = faceCorners Cyl c := by
  have key : ∀ y : Fin 3 → ℕ, y c = 0 → (y ∈ coneCut Cyl q ↔ y ∈ Cyl) := by
    intro y hy
    simp only [coneCut, mem_filter, and_iff_left_iff_imp]
    intro _ hall
    have := hall c; have := hq c; omega
  have hface : face (coneCut Cyl q) c = face Cyl c := by
    ext x
    simp only [face, mem_filter]
    constructor
    · rintro ⟨hx, hc⟩; exact ⟨(key x hc).1 hx, hc⟩
    · rintro ⟨hx, hc⟩; exact ⟨(key x hc).2 hx, hc⟩
  unfold faceCorners
  rw [hface]
  refine filter_congr fun x hx => ?_
  have hc := (mem_filter.1 hx).2
  refine forall_congr' fun a => imp_congr_right fun ha => not_congr (key _ ?_)
  simp [Pi.single_eq_of_ne (Ne.symm ha), hc]

/-- `|faceCorners| ` of the cut equals that of `Cyl`, summed. -/
theorem sum_faceCorners_coneCut (Cyl : Finset (Fin 3 → ℕ)) {q : Fin 3 → ℕ} (hq : ∀ i, 1 ≤ q i) :
    ∑ c, (faceCorners (coneCut Cyl q) c).card = ∑ c, (faceCorners Cyl c).card := by
  simp only [faceCorners_coneCut Cyl hq]

/-! ### Column sets -/

section Col

variable {D : Finset (Fin 3 → ℕ)} {ψ : ℕ → ℕ → ℕ}

theorem col_mem_e0 (hψ : ∀ x, x ∈ D ↔ x 2 < ψ (x 0) (x 1)) (x : Fin 3 → ℕ) :
    x + Pi.single 0 1 ∈ D ↔ x 2 < ψ (x 0 + 1) (x 1) := by
  rw [hψ]; simp

theorem col_mem_e1 (hψ : ∀ x, x ∈ D ↔ x 2 < ψ (x 0) (x 1)) (x : Fin 3 → ℕ) :
    x + Pi.single 1 1 ∈ D ↔ x 2 < ψ (x 0) (x 1 + 1) := by
  rw [hψ]; simp

theorem col_mem_e2 (hψ : ∀ x, x ∈ D ↔ x 2 < ψ (x 0) (x 1)) (x : Fin 3 → ℕ) :
    x + Pi.single 2 1 ∈ D ↔ x 2 + 1 < ψ (x 0) (x 1) := by
  rw [hψ]; simp

/-- Maximal cells of a column set `{x : x₂ < ψ(x₀, x₁)}`. -/
theorem col_mem_maxSet (hψ : ∀ x, x ∈ D ↔ x 2 < ψ (x 0) (x 1)) (x : Fin 3 → ℕ) :
    x ∈ maxSet D ↔ x 2 < ψ (x 0) (x 1) ∧ ψ (x 0 + 1) (x 1) ≤ x 2 ∧ ψ (x 0) (x 1 + 1) ≤ x 2 ∧
      ψ (x 0) (x 1) ≤ x 2 + 1 := by
  simp only [maxSet, mem_filter, IsMaxCell]
  rw [hψ]
  constructor
  · rintro ⟨h1, h2⟩
    have a0 := h2 0; have a1 := h2 1; have a2 := h2 2
    rw [col_mem_e0 hψ] at a0; rw [col_mem_e1 hψ] at a1; rw [col_mem_e2 hψ] at a2
    omega
  · rintro ⟨h1, h2, h3, h4⟩
    refine ⟨h1, fun a => ?_⟩
    fin_cases a
    · show x + Pi.single 0 1 ∉ D; rw [col_mem_e0 hψ]; omega
    · show x + Pi.single 1 1 ∉ D; rw [col_mem_e1 hψ]; omega
    · show x + Pi.single 2 1 ∉ D; rw [col_mem_e2 hψ]; omega

/-- Maximal cells of a column set are determined by their first two coordinates. -/
theorem col_max_ext (hψ : ∀ x, x ∈ D ↔ x 2 < ψ (x 0) (x 1)) {x x' : Fin 3 → ℕ}
    (hx : x ∈ maxSet D) (hx' : x' ∈ maxSet D) (h0 : x 0 = x' 0) (h1 : x 1 = x' 1) : x = x' := by
  rw [col_mem_maxSet hψ] at hx hx'
  rw [h0, h1] at hx
  have h2 : x 2 = x' 2 := by omega
  funext t; fin_cases t
  · exact h0
  · exact h1
  · exact h2

/-- Branch A of a column set: if `ψ(x₀+1, x₁) = ψ(x₀, x₁+1) = 0`, then `(x₀, x₁, 0)` is a corner of
the base face. -/
theorem col_mapA_mem (hψ : ∀ x, x ∈ D ↔ x 2 < ψ (x 0) (x 1)) {x : Fin 3 → ℕ}
    (hx : x ∈ maxSet D) (hr : ψ (x 0 + 1) (x 1) = 0) (hu : ψ (x 0) (x 1 + 1) = 0) :
    (![x 0, x 1, 0] : Fin 3 → ℕ) ∈ faceCorners D 2 := by
  rw [col_mem_maxSet hψ] at hx
  rw [mem_faceCorners_iff (a := 0) (b := 1) (by decide) (by decide) (by decide)]
  refine ⟨?_, by simp, ?_, ?_⟩
  · rw [hψ]; simp; omega
  · rw [vec_add_e0, hψ]; simp; omega
  · rw [vec_add_e1, hψ]; simp; omega

end Col

/-! ### The cut of a class-𝒞 set is a column set -/

/-- Column height of `Cyl ∖ (q + ℕ³)`: `min(φ*, q₂)` on the quadrant `[q₀,∞) × [q₁,∞)`, `φ*`
elsewhere. -/
def psiC (L₁ : ℕ) (h F G : ℕ → ℕ) (q : Fin 3 → ℕ) (i j : ℕ) : ℕ :=
  if q 0 ≤ i ∧ q 1 ≤ j then min (phiS L₁ h F G i j) (q 2) else phiS L₁ h F G i j

variable {Cyl : Finset (Fin 3 → ℕ)} {L₁ : ℕ} {h F G : ℕ → ℕ} {q : Fin 3 → ℕ}

theorem psiC_le (i j : ℕ) : psiC L₁ h F G q i j ≤ phiS L₁ h F G i j := by
  unfold psiC; split_ifs <;> omega

namespace LWClass

variable (hC : LWClass Cyl L₁ h F G)
include hC

theorem mem_coneCut (x : Fin 3 → ℕ) :
    x ∈ coneCut Cyl q ↔ x 2 < psiC L₁ h F G q (x 0) (x 1) := by
  simp only [coneCut, mem_filter, forall_fin3_le]
  rw [hC.mem_iff']
  unfold psiC
  split_ifs with hQ <;> omega

/-- `φ*` is antitone on all of `ℕ²`. -/
theorem phiS_anti' {i j i' j' : ℕ} (hi : i ≤ i') (hj : j ≤ j') :
    phiS L₁ h F G i' j' ≤ phiS L₁ h F G i j := by
  rcases phiS_cases (L₁ := L₁) (h := h) (F := F) (G := G) i' j' with ⟨hi', hj', -⟩ | ⟨-, h0⟩
  · exact (hC.phiS_anti hi hj hi' hj').2.2
  · rw [h0]; exact Nat.zero_le _

/-- `ψ` is antitone. -/
theorem psiC_anti {i j i' j' : ℕ} (hi : i ≤ i') (hj : j ≤ j') :
    psiC L₁ h F G q i' j' ≤ psiC L₁ h F G q i j := by
  have := hC.phiS_anti' hi hj
  unfold psiC
  split_ifs <;> omega

/-- `(i, 0, F(i) − 1)` is a corner of `A₁` other than `cornerF` when `F` drops at `i < L₁ − 1`. -/
theorem cornerAtF_mem {i : ℕ} (hi1 : i + 1 < L₁) (hFd : F (i + 1) < F i) :
    (![i, 0, F i - 1] : Fin 3 → ℕ) ∈ (faceCorners Cyl 1).erase (cornerF L₁ F) := by
  have hi : i < L₁ := by omega
  have hh0 := hC.h_pos _ hi
  have hh1 := hC.h_pos _ hi1
  have hF0 := hC.F_pos _ hi
  have hFa := hC.F_anti 0 i (Nat.zero_le _) hi
  have hz := hC.F_zero
  rw [mem_erase, mem_faceCorners_iff (a := 0) (b := 2) (by decide) (by decide) (by decide)]
  refine ⟨fun heq => ?_, ?_, by simp, ?_, ?_⟩
  · have := congrFun heq 0
    simp [cornerF] at this
    omega
  · rw [hC.mem_vec, phiS_eq hi (show 0 < h i by omega)]; omega
  · rw [vec_add_e0, hC.mem_vec, phiS_eq hi1 (show 0 < h (i + 1) by omega)]; omega
  · rw [vec_add_e2, hC.mem_vec, phiS_eq hi (show 0 < h i by omega)]; omega

/-- `(0, j, G(j) − 1)` is a corner of `A₀` other than `cornerG` when `G` drops at `j` with
`j + 1 < h i` for some `i < L₁`. -/
theorem cornerAtG_mem {i j : ℕ} (hi : i < L₁) (hj1 : j + 1 < h i) (hGd : G (j + 1) < G j) :
    (![0, j, G j - 1] : Fin 3 → ℕ) ∈ (faceCorners Cyl 0).erase (cornerG h G) := by
  have hL := hC.one_le
  have hha := hC.h_anti 0 i (Nat.zero_le _) hi
  have hG0 := hC.G_pos j (by omega)
  have hGa := hC.G_anti 0 j (Nat.zero_le _) (by omega)
  have hz := hC.F_zero
  rw [mem_erase, mem_faceCorners_iff (a := 1) (b := 2) (by decide) (by decide) (by decide)]
  refine ⟨fun heq => ?_, ?_, by simp, ?_, ?_⟩
  · have := congrFun heq 1
    simp [cornerG] at this
    omega
  · rw [hC.mem_vec, phiS_eq (show 0 < L₁ by omega) (show j < h 0 by omega)]; omega
  · rw [vec_add_e1, hC.mem_vec]
    rcases phiS_cases (L₁ := L₁) (h := h) (F := F) (G := G) 0 (j + 1) with
      ⟨-, -, h3⟩ | ⟨-, h3⟩ <;> rw [h3] <;> omega
  · rw [vec_add_e2, hC.mem_vec, phiS_eq (show 0 < L₁ by omega) (show j < h 0 by omega)]
    omega

/-- **F-drop.** A maximal cell of the cut with `0 ≠ r ≥ u`, outside the exceptional case
(`x₀ + 1 = q₀`, `x₁ ≥ q₁`, `r = q₂`), has `x₀ + 1 < L₁`, `F(x₀+1) < F(x₀)` and `r = F(x₀+1)`. -/
theorem coneCut_Fdrop {x : Fin 3 → ℕ} (hx : x ∈ maxSet (coneCut Cyl q))
    (hr : psiC L₁ h F G q (x 0 + 1) (x 1) ≠ 0)
    (hex : ¬ (x 0 + 1 = q 0 ∧ q 1 ≤ x 1 ∧ psiC L₁ h F G q (x 0 + 1) (x 1) = q 2)) :
    x 0 + 1 < L₁ ∧ F (x 0 + 1) < F (x 0) ∧ psiC L₁ h F G q (x 0 + 1) (x 1) = F (x 0 + 1) := by
  rw [col_mem_maxSet hC.mem_coneCut] at hx
  have hr1 := psiC_le (L₁ := L₁) (h := h) (F := F) (G := G) (q := q) (x 0 + 1) (x 1)
  have hp1 := psiC_le (L₁ := L₁) (h := h) (F := F) (G := G) (q := q) (x 0) (x 1)
  obtain ⟨hi1, hj1⟩ := pos_phiS (show 0 < phiS L₁ h F G (x 0 + 1) (x 1) by omega)
  obtain ⟨hi, hj⟩ := pos_phiS (show 0 < phiS L₁ h F G (x 0) (x 1) by omega)
  have e1 := phiS_eq (F := F) (G := G) hi1 hj1
  have e0 := phiS_eq (F := F) (G := G) hi hj
  refine ⟨hi1, ?_⟩
  unfold psiC at hx hr hex ⊢
  rw [e1, e0] at hx
  rw [e1] at hr hex ⊢
  split_ifs at hx hr hex ⊢ <;> omega

/-- **G-drop.** A maximal cell of the cut with `r < u`, outside the exceptional case
(`x₁ + 1 = q₁`, `x₀ ≥ q₀`, `u = q₂`), has `x₁ + 1 < h(x₀)`, `G(x₁+1) < G(x₁)` and `u = G(x₁+1)`. -/
theorem coneCut_Gdrop {x : Fin 3 → ℕ} (hx : x ∈ maxSet (coneCut Cyl q))
    (hru : psiC L₁ h F G q (x 0 + 1) (x 1) < psiC L₁ h F G q (x 0) (x 1 + 1))
    (hex : ¬ (x 1 + 1 = q 1 ∧ q 0 ≤ x 0 ∧ psiC L₁ h F G q (x 0) (x 1 + 1) = q 2)) :
    x 0 < L₁ ∧ x 1 + 1 < h (x 0) ∧ G (x 1 + 1) < G (x 1) ∧
      psiC L₁ h F G q (x 0) (x 1 + 1) = G (x 1 + 1) := by
  rw [col_mem_maxSet hC.mem_coneCut] at hx
  have hu1 := psiC_le (L₁ := L₁) (h := h) (F := F) (G := G) (q := q) (x 0) (x 1 + 1)
  have hp1 := psiC_le (L₁ := L₁) (h := h) (F := F) (G := G) (q := q) (x 0) (x 1)
  obtain ⟨hi1, hj1⟩ := pos_phiS (show 0 < phiS L₁ h F G (x 0) (x 1 + 1) by omega)
  obtain ⟨hi, hj⟩ := pos_phiS (show 0 < phiS L₁ h F G (x 0) (x 1) by omega)
  have e1 := phiS_eq (F := F) (G := G) hi1 hj1
  have e0 := phiS_eq (F := F) (G := G) hi hj
  refine ⟨hi, hj1, ?_⟩
  have hu := hx.2.2.1
  have hlt := hx.1
  unfold psiC at hu hlt hru hex ⊢
  rw [e1] at hu hru hex ⊢
  rw [e0] at hlt
  split_ifs at hu hlt hru hex ⊢ <;> omega

/-- Injectivity in the F-branches: two maximal cells of the cut with the same `x₀`, the same `r`
and `u(x) ≤ r(x)` have the same `x₁`. -/
theorem coneCut_F_aux {x x' : Fin 3 → ℕ} (hx' : x' ∈ maxSet (coneCut Cyl q)) (h0 : x 0 = x' 0)
    (hrr : psiC L₁ h F G q (x 0 + 1) (x 1) = psiC L₁ h F G q (x' 0 + 1) (x' 1))
    (hur : psiC L₁ h F G q (x 0) (x 1 + 1) ≤ psiC L₁ h F G q (x 0 + 1) (x 1)) :
    ¬ x 1 < x' 1 := by
  intro hlt
  rw [col_mem_maxSet hC.mem_coneCut] at hx'
  have := hC.psiC_anti (q := q) (le_refl (x 0)) (show x 1 + 1 ≤ x' 1 by omega)
  rw [h0] at this hur hrr
  omega

/-- Injectivity in the G-branches: two maximal cells of the cut with the same `x₁`, the same `u`
and `r(x) < u(x)` have the same `x₀`. -/
theorem coneCut_G_aux {x x' : Fin 3 → ℕ} (hx' : x' ∈ maxSet (coneCut Cyl q)) (h1 : x 1 = x' 1)
    (huu : psiC L₁ h F G q (x 0) (x 1 + 1) = psiC L₁ h F G q (x' 0) (x' 1 + 1))
    (hru : psiC L₁ h F G q (x 0 + 1) (x 1) < psiC L₁ h F G q (x 0) (x 1 + 1)) :
    ¬ x 0 < x' 0 := by
  intro hlt
  rw [col_mem_maxSet hC.mem_coneCut] at hx'
  have := hC.psiC_anti (q := q) (show x 0 + 1 ≤ x' 0 by omega) (le_refl (x 1))
  rw [h1] at this hru huu
  omega

end LWClass

/-- **Lemma T′ (type bound, cone class).** If `Cyl` is in class 𝒞 and `q ≥ (1,1,1)`, then
`D = Cyl ∖ (q + ℕ³)` satisfies `t ≤ C`: `|Max D| ≤ Σ_c |faceCorners D c|`. -/
theorem typeBound_cone (hC : LWClass Cyl L₁ h F G) (hq : ∀ i, 1 ≤ q i) :
    (maxSet (coneCut Cyl q)).card ≤ ∑ c, (faceCorners (coneCut Cyl q) c).card := by
  have hψ := hC.mem_coneCut (q := q)
  -- abbreviations for the predicates
  let r : (Fin 3 → ℕ) → ℕ := fun x => psiC L₁ h F G q (x 0 + 1) (x 1)
  let u : (Fin 3 → ℕ) → ℕ := fun x => psiC L₁ h F G q (x 0) (x 1 + 1)
  let M := maxSet (coneCut Cyl q)
  let MG := M.filter (fun x => r x < u x)
  let MN := M.filter (fun x => ¬ r x < u x)
  let MA := MN.filter (fun x => r x = 0)
  let MF := MN.filter (fun x => ¬ r x = 0)
  let QG := MG.filter (fun x => x 1 + 1 = q 1 ∧ q 0 ≤ x 0 ∧ u x = q 2)
  let GD := MG.filter (fun x => ¬ (x 1 + 1 = q 1 ∧ q 0 ≤ x 0 ∧ u x = q 2))
  let QF := MF.filter (fun x => x 0 + 1 = q 0 ∧ q 1 ≤ x 1 ∧ r x = q 2)
  let FD := MF.filter (fun x => ¬ (x 0 + 1 = q 0 ∧ q 1 ≤ x 1 ∧ r x = q 2))
  have hs1 : MG.card + MN.card = M.card := card_filter_add_card_filter_not _
  have hs2 : MA.card + MF.card = MN.card := card_filter_add_card_filter_not _
  have hs3 : QG.card + GD.card = MG.card := card_filter_add_card_filter_not _
  have hs4 : QF.card + FD.card = MF.card := card_filter_add_card_filter_not _
  -- membership unpacking
  have memMG : ∀ {x}, x ∈ MG → x ∈ M ∧ r x < u x := fun hx => mem_filter.1 hx
  have memMN : ∀ {x}, x ∈ MN → x ∈ M ∧ ¬ r x < u x := fun hx => mem_filter.1 hx
  -- branch A
  have hA : MA.card ≤ (faceCorners (coneCut Cyl q) 2).card := by
    refine card_le_card_of_injOn (fun x => ![x 0, x 1, 0]) ?_ ?_
    · intro x hx
      obtain ⟨hxN, hr0⟩ := mem_filter.1 hx
      obtain ⟨hxM, hnru⟩ := memMN hxN
      exact col_mapA_mem hψ hxM hr0 (by simp only [r, u] at hr0 hnru ⊢; omega)
    · intro x hx x' hx' heq
      have hxM := (memMN (mem_filter.1 hx).1).1
      have hxM' := (memMN (mem_filter.1 hx').1).1
      have e0 : x 0 = x' 0 := by have := congrFun heq 0; simpa using this
      have e1 : x 1 = x' 1 := by have := congrFun heq 1; simpa using this
      exact col_max_ext hψ hxM hxM' e0 e1
  -- branch F, exceptional part: at most one cell
  have hQF : QF.card ≤ 1 := by
    refine card_le_one.2 fun x hx x' hx' => ?_
    obtain ⟨hxF, hex⟩ := mem_filter.1 hx
    obtain ⟨hxF', hex'⟩ := mem_filter.1 hx'
    obtain ⟨hxM, hnru⟩ := memMN (mem_filter.1 hxF).1
    obtain ⟨hxM', hnru'⟩ := memMN (mem_filter.1 hxF').1
    have e0 : x 0 = x' 0 := by omega
    have hrr : r x = r x' := by simp only [r] at hex hex' ⊢; omega
    have e1 : x 1 = x' 1 := by
      rcases lt_trichotomy (x 1) (x' 1) with hlt | heq' | hgt
      · exact absurd hlt (hC.coneCut_F_aux hxM' e0 hrr (by simp only [r, u] at hnru; omega))
      · exact heq'
      · exact absurd hgt (hC.coneCut_F_aux hxM e0.symm hrr.symm
          (by simp only [r, u] at hnru'; omega))
    exact col_max_ext hψ hxM hxM' e0 e1
  -- branch F, drop part
  have hFD : FD.card ≤ ((faceCorners Cyl 1).erase (cornerF L₁ F)).card := by
    refine card_le_card_of_injOn (fun x => ![x 0, 0, F (x 0) - 1]) ?_ ?_
    · intro x hx
      obtain ⟨hxF, hex⟩ := mem_filter.1 hx
      obtain ⟨hxN, hr0⟩ := mem_filter.1 hxF
      obtain ⟨hxM, -⟩ := memMN hxN
      obtain ⟨hi1, hFd, -⟩ := hC.coneCut_Fdrop hxM hr0 hex
      exact hC.cornerAtF_mem hi1 hFd
    · intro x hx x' hx' heq
      obtain ⟨hxF, hex⟩ := mem_filter.1 hx
      obtain ⟨hxF', hex'⟩ := mem_filter.1 hx'
      obtain ⟨hxN, hr0⟩ := mem_filter.1 hxF
      obtain ⟨hxN', hr0'⟩ := mem_filter.1 hxF'
      obtain ⟨hxM, hnru⟩ := memMN hxN
      obtain ⟨hxM', hnru'⟩ := memMN hxN'
      have e0 : x 0 = x' 0 := by have := congrFun heq 0; simpa using this
      obtain ⟨-, -, hrx⟩ := hC.coneCut_Fdrop hxM hr0 hex
      obtain ⟨-, -, hrx'⟩ := hC.coneCut_Fdrop hxM' hr0' hex'
      have hrr : r x = r x' := by simp only [r]; rw [hrx, hrx', e0]
      have e1 : x 1 = x' 1 := by
        rcases lt_trichotomy (x 1) (x' 1) with hlt | heq' | hgt
        · exact absurd hlt (hC.coneCut_F_aux hxM' e0 hrr (by simp only [r, u] at hnru; omega))
        · exact heq'
        · exact absurd hgt (hC.coneCut_F_aux hxM e0.symm hrr.symm
            (by simp only [r, u] at hnru'; omega))
      exact col_max_ext hψ hxM hxM' e0 e1
  -- branch G, exceptional part
  have hQG : QG.card ≤ 1 := by
    refine card_le_one.2 fun x hx x' hx' => ?_
    obtain ⟨hxG, hex⟩ := mem_filter.1 hx
    obtain ⟨hxG', hex'⟩ := mem_filter.1 hx'
    obtain ⟨hxM, hru⟩ := memMG hxG
    obtain ⟨hxM', hru'⟩ := memMG hxG'
    have e1 : x 1 = x' 1 := by omega
    have huu : u x = u x' := by simp only [u] at hex hex' ⊢; omega
    have e0 : x 0 = x' 0 := by
      rcases lt_trichotomy (x 0) (x' 0) with hlt | heq' | hgt
      · exact absurd hlt (hC.coneCut_G_aux hxM' e1 huu hru)
      · exact heq'
      · exact absurd hgt (hC.coneCut_G_aux hxM e1.symm huu.symm hru')
    exact col_max_ext hψ hxM hxM' e0 e1
  -- branch G, drop part
  have hGD : GD.card ≤ ((faceCorners Cyl 0).erase (cornerG h G)).card := by
    refine card_le_card_of_injOn (fun x => ![0, x 1, G (x 1) - 1]) ?_ ?_
    · intro x hx
      obtain ⟨hxG, hex⟩ := mem_filter.1 hx
      obtain ⟨hxM, hru⟩ := memMG hxG
      obtain ⟨hi, hj1, hGd, -⟩ := hC.coneCut_Gdrop hxM hru hex
      exact hC.cornerAtG_mem hi hj1 hGd
    · intro x hx x' hx' heq
      obtain ⟨hxG, hex⟩ := mem_filter.1 hx
      obtain ⟨hxG', hex'⟩ := mem_filter.1 hx'
      obtain ⟨hxM, hru⟩ := memMG hxG
      obtain ⟨hxM', hru'⟩ := memMG hxG'
      have e1 : x 1 = x' 1 := by have := congrFun heq 1; simpa using this
      obtain ⟨-, -, -, hux⟩ := hC.coneCut_Gdrop hxM hru hex
      obtain ⟨-, -, -, hux'⟩ := hC.coneCut_Gdrop hxM' hru' hex'
      have huu : u x = u x' := by simp only [u]; rw [hux, hux', e1]
      have e0 : x 0 = x' 0 := by
        rcases lt_trichotomy (x 0) (x' 0) with hlt | heq' | hgt
        · exact absurd hlt (hC.coneCut_G_aux hxM' e1 huu hru)
        · exact heq'
        · exact absurd hgt (hC.coneCut_G_aux hxM e1.symm huu.symm hru')
      exact col_max_ext hψ hxM hxM' e0 e1
  rw [card_erase_of_mem hC.cornerF_mem] at hFD
  rw [card_erase_of_mem hC.cornerG_mem] at hGD
  have h1 : 1 ≤ (faceCorners Cyl 1).card := card_pos.2 ⟨_, hC.cornerF_mem⟩
  have h0 : 1 ≤ (faceCorners Cyl 0).card := card_pos.2 ⟨_, hC.cornerG_mem⟩
  rw [Fin.sum_univ_three, faceCorners_coneCut Cyl hq 0, faceCorners_coneCut Cyl hq 1]
  show M.card ≤ _
  omega

/-- **Lemma T′** with exactly the hypotheses of `.research/PROOFS.md` (`q ∈ Cyl` is not used). -/
theorem typeBound_cone' (hC : LWClass Cyl L₁ h F G) (hq : ∀ i, 1 ≤ q i) (_hqC : q ∈ Cyl) :
    (maxSet (Cyl.filter (fun x => ¬ ∀ i, q i ≤ x i))).card ≤
      ∑ c, (faceCorners (Cyl.filter (fun x => ¬ ∀ i, q i ≤ x i)) c).card :=
  typeBound_cone hC hq

/-! ### Sharpness: `t = C` is attained -/

/-- The box `[0,2)³`. -/
def box2 : Finset (Fin 3 → ℕ) :=
  (range 2 ×ˢ range 2 ×ˢ range 2).image (fun p => ![p.1, p.2.1, p.2.2])

/-- The box `[0,2)³` is in class 𝒞 (`L₁ = 2`, `h = F = G = 2`). -/
theorem box2_class : LWClass box2 2 (fun _ => 2) (fun _ => 2) (fun _ => 2) where
  one_le := by norm_num
  h_anti _ _ _ _ := le_rfl
  F_anti _ _ _ _ := le_rfl
  G_anti _ _ _ _ := le_rfl
  h_pos _ _ := by norm_num
  F_pos _ _ := by norm_num
  G_pos _ _ := by norm_num
  F_zero := rfl
  mem_iff x := by
    simp only [box2, mem_image, mem_product, mem_range, Prod.exists]
    constructor
    · rintro ⟨a, b, c, ⟨ha, hb, hc⟩, rfl⟩
      simp; omega
    · rintro ⟨h0, h1, h2⟩
      refine ⟨x 0, x 1, x 2, ⟨h0, h1, by simpa using h2⟩, ?_⟩
      funext i; fin_cases i <;> rfl

theorem one_mem_box2 : (![1, 1, 1] : Fin 3 → ℕ) ∈ box2 := by decide

/-- **Lemma T′ is sharp**: for `Cyl = [0,2)³` and `q = (1,1,1)` (so `D` is the box minus its top
cell), `t = C = 3` (kernel `decide`). -/
theorem typeBound_cone_attained :
    (maxSet (coneCut box2 ![1, 1, 1])).card = ∑ c, (faceCorners (coneCut box2 ![1, 1, 1]) c).card ∧
      (maxSet (coneCut box2 ![1, 1, 1])).card = 3 := by
  decide

end ConeType

end CornerArea

end NumericalSemigroup
