import Wilf.MaxCL

/-!
# 2-D Tile-CL for every 2-dimensional tile

Formalization of `.research/PROOFS.md`, section "2-D Tile-CL for EVERY 2-D tile" (2026-10-17).

Setting: `D ⊆ ℕ²` a finite down-set with `|D| = m` on which `φ(x) = x₀p₀ + x₁p₁ ∈ ℤ/m` is a bijection
(`IsTile D p`, `d = 2`). For `x ∈ D` let `t_a(x) = colTop D a x` be the top of the `a`-column
through `x` (`t₀(x)` = end of the row of `x`, `t₁(x)` = top of the column of `x`), and let
`μ(x) = φ(t₀ x) + φ(t₁ x)` (`cornerSum`; `= φ(x) + φ(τ x)` with `τ(x)` the corner of `x`).

* (L3, `tileCLAt_two_of_injOn`) **If `μ` is injective on `D` then `TileCLAt D p`.**
  Proof (base form): `Σ_y T(y)·⟨s - φ y⟩ = Σ_{x∈D} (⟨s - φ(t₀x)⟩ + ⟨s - φ(t₁x)⟩)`
  (`sum_tileT_mul_colTop`, each column top counted once per cell of its column), and
  `⟨A⟩ + ⟨B⟩ ≥ ⟨A + B⟩ = ⟨2s - μ(x)⟩`; since `x ↦ 2s - μ(x)` is a bijection `D → ℤ/m`, the right
  side sums to `Σ_{w<m} w = m(m-1)/2`.
* (L1, `Tile2.classify`) A 2-D tile is a rectangle `[0,a)×[0,b)` or an L-shape
  `[0,a)×[0,b') ∪ [0,a')×[0,b)` (`a' < a`, `b' < b`) with `a·p₀ + b'·p₁ = b·p₁`
  (the lattice relation `(a, -c) ∈ Λ`, `c = b - b'`). Proved by pure injectivity/surjectivity
  arguments on `φ` (inner corners have `φ = 0`, at most one inner corner, boundary cells).
* (L2, `shape_inj`, `cornerSum_injOn_of_two`) For these shapes `μ` is injective on `D`.
* **`tileCLAt_of_two : IsTile D p → TileCLAt D p`** for every `D : Finset (Fin 2 → ℕ)`.
* `tileCLAt_of_le_two` (`d ≤ 2`, any index type `Fin d`) and the corollary
  **`wilf_of_embDim_le_three : S.embDim ≤ 3 → S.conductor ≤ S.embDim * S.ell`**
  (a known theorem, Fröberg–Gottlieb–Häggkvist 1987; here obtained through Tile-CL ⇒ CL ⇒ Wilf).
-/

namespace NumericalSemigroup

open Finset

/-! ## Column tops and `Σ_y T(y)·g(y) = Σ_a Σ_{x∈D} g(t_a x)` -/

section ColTop

variable {d : ℕ} {D : Finset (Fin d → ℕ)} {a : Fin d}

/-- The top of the `a`-column of `D` through `x`: `x + colHt D a x · e_a`. -/
noncomputable def colTop (D : Finset (Fin d → ℕ)) (a : Fin d) (x : Fin d → ℕ) : Fin d → ℕ :=
  x + Pi.single a (colHt D a x)

/-- If `x + k·e_a ∈ D ↔ k ≤ K` for all `k`, then `colHt D a x = K`. -/
theorem colHt_eq_of_iff {x : Fin d → ℕ} {K : ℕ} (h : ∀ k, x + Pi.single a k ∈ D ↔ k ≤ K) :
    colHt D a x = K := by
  have hK : x + Pi.single a K ∈ D := (h K).2 le_rfl
  have hx : x ∈ D := by simpa using (h 0).2 (Nat.zero_le _)
  exact le_antisymm ((h _).1 (colHt_spec hx)) (le_colHt hK)

/-- For an `a`-top `y` of `D` and `k ≤ y_a`: `t_a(y - k·e_a) = y`. -/
theorem colTop_sub_single (hD : IsDownSetFin D) {y : Fin d → ℕ} (hy : y ∈ D)
    (hy' : y + Pi.single a 1 ∉ D) {k : ℕ} (hk : k ≤ y a) :
    colTop D a (y - Pi.single a k) = y := by
  have hadd := sub_single_add_single (a := a) hk
  have hxD : y - Pi.single a k ∈ D := hD _ hy _ (fun b => Nat.sub_le _ _)
  have h1 : k ≤ colHt D a (y - Pi.single a k) := le_colHt (by rw [hadd]; exact hy)
  have h2 : colHt D a (y - Pi.single a k) ≤ k := by
    by_contra hlt
    have := mem_of_le_colHt hD hxD (show k + 1 ≤ colHt D a (y - Pi.single a k) by omega)
    rw [Pi.single_add, ← add_assoc, hadd] at this
    exact hy' this
  rw [colTop, le_antisymm h2 h1, hadd]

/-- `Σ_{x∈D} g(t_a x) = Σ_{a-tops y} (y_a + 1)·g(y)`. -/
theorem sum_colTop (hD : IsDownSetFin D) (a : Fin d) (g : (Fin d → ℕ) → ℕ) :
    ∑ x ∈ D, g (colTop D a x) =
      ∑ y ∈ D.filter (fun y => y + Pi.single a 1 ∉ D), (y a + 1) * g y := by
  rw [sum_columns hD a]
  refine Finset.sum_congr rfl fun y hy => ?_
  have hy' := Finset.mem_filter.1 hy
  rw [Finset.sum_congr rfl fun k hk =>
    by rw [colTop_sub_single hD hy'.1 hy'.2 (by have := Finset.mem_range.1 hk; omega)]]
  simp

/-- **Column form of the Tile-CL sum**: `Σ_{y∈D} T(y)·g(y) = Σ_a Σ_{x∈D} g(t_a x)`. -/
theorem sum_tileT_mul_colTop (hD : IsDownSetFin D) (g : (Fin d → ℕ) → ℕ) :
    ∑ y ∈ D, tileT D y * g y = ∑ a, ∑ x ∈ D, g (colTop D a x) := by
  simp_rw [sum_colTop hD, tileT, Finset.sum_filter]
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun y _ => ?_
  rw [Finset.sum_mul]
  refine Finset.sum_congr rfl fun a _ => ?_
  split_ifs <;> simp

end ColTop

/-! ## (L3) Corner-sum bijectivity implies 2-D Tile-CL -/

/-- If `F` is injective on `D` and `|D| = m`, then `2·Σ_{x∈D} ⟨F x⟩ = m(m-1)`. -/
theorem sum_val_mul_two_of_injOn {d m : ℕ} [NeZero m] {D : Finset (Fin d → ℕ)}
    (hcard : D.card = m) {F : (Fin d → ℕ) → ZMod m} (hF : Set.InjOn F (D : Set (Fin d → ℕ))) :
    (∑ x ∈ D, (F x).val) * 2 = m * (m - 1) := by
  have hinj : Set.InjOn (fun x => (F x).val) (D : Set (Fin d → ℕ)) :=
    fun x hx y hy h => hF hx hy (ZMod.val_injective m h)
  have himg : D.image (fun x => (F x).val) = range m := by
    apply Finset.eq_of_subset_of_card_le
    · intro i hi
      obtain ⟨x, -, rfl⟩ := Finset.mem_image.1 hi
      exact Finset.mem_range.2 (ZMod.val_lt _)
    · rw [Finset.card_range, Finset.card_image_of_injOn hinj, hcard]
  rw [← Finset.sum_range_id_mul_two, ← himg, Finset.sum_image hinj]

/-- The corner sum `μ(x) = φ(t₀ x) + φ(t₁ x)` (`= φ(x) + φ(τ x)`, `τ(x)` the corner of `x`). -/
noncomputable def cornerSum {m : ℕ} (D : Finset (Fin 2 → ℕ)) (p : Fin 2 → ZMod m)
    (x : Fin 2 → ℕ) : ZMod m :=
  tilePhi p (colTop D 0 x) + tilePhi p (colTop D 1 x)

/-- **(L3)** If the corner sum `μ` is injective on a 2-D tile `D`, then `D` satisfies Tile-CL. -/
theorem tileCLAt_two_of_injOn {m : ℕ} {D : Finset (Fin 2 → ℕ)} {p : Fin 2 → ZMod m}
    (h : IsTile D p) (hμ : Set.InjOn (cornerSum D p) (D : Set (Fin 2 → ℕ))) : TileCLAt D p := by
  intro s
  have : NeZero m := ⟨h.pos.ne'⟩
  rw [sum_tileT_mul_colTop h.1 (fun y => (s - tilePhi p y).val), Fin.sum_univ_two,
    ← Finset.sum_add_distrib]
  have hF : Set.InjOn (fun x => (s - tilePhi p (colTop D 0 x)) + (s - tilePhi p (colTop D 1 x)))
      (D : Set (Fin 2 → ℕ)) := by
    intro x hx y hy hxy
    apply hμ hx hy
    simp only [cornerSum]
    linear_combination -hxy
  have h2 := sum_val_mul_two_of_injOn h.2.1 hF
  have hle : ∑ x ∈ D, ((s - tilePhi p (colTop D 0 x)) + (s - tilePhi p (colTop D 1 x))).val ≤
      ∑ x ∈ D, ((s - tilePhi p (colTop D 0 x)).val + (s - tilePhi p (colTop D 1 x)).val) :=
    Finset.sum_le_sum fun x _ => ZMod.val_add_le _ _
  generalize m * (m - 1) = K at h2 ⊢
  omega

/-! ## Coordinates: 2-D tiles as predicates on `ℕ × ℕ` -/

section Coord

variable {m : ℕ}

/-- `Φ(i, j) = i·u + j·v ∈ ℤ/m`. -/
def phi2 (u v : ZMod m) (i j : ℕ) : ZMod m := (i : ZMod m) * u + (j : ZMod m) * v

/-- A 2-D tile in coordinates: `P` (the cells) is a bounded down-set of `ℕ²` on which
`Φ(i, j) = i·u + j·v` is injective and onto `ℤ/m`. -/
structure Tile2 (P : ℕ → ℕ → Prop) (u v : ZMod m) : Prop where
  down : ∀ {i j i' j' : ℕ}, P i j → i' ≤ i → j' ≤ j → P i' j'
  inj : ∀ {i j k l : ℕ}, P i j → P k l → phi2 u v i j = phi2 u v k l → i = k ∧ j = l
  surj : ∀ z : ZMod m, ∃ i j, P i j ∧ phi2 u v i j = z
  bdd : ∃ N, ∀ i j, P i j → i < N ∧ j < N

variable {P : ℕ → ℕ → Prop} {u v : ZMod m}

theorem Tile2.zero (T : Tile2 P u v) : P 0 0 := by
  obtain ⟨i, j, h, -⟩ := T.surj 0
  exact T.down h (Nat.zero_le _) (Nat.zero_le _)

/-- Every row of a 2-D tile is an initial segment `[0, L)`. -/
theorem Tile2.row (T : Tile2 P u v) (j : ℕ) : ∃ L, ∀ i, P i j ↔ i < L := by
  classical
  obtain ⟨N, hN⟩ := T.bdd
  have hex : ∃ i, ¬ P i j := ⟨N, fun h => by have := (hN _ _ h).1; omega⟩
  refine ⟨Nat.find hex, fun i => ⟨fun h => ?_, fun h => ?_⟩⟩
  · by_contra hi
    exact Nat.find_spec hex (T.down h (by omega) le_rfl)
  · by_contra hP
    have := Nat.find_min' hex hP
    omega

/-- Every column of a 2-D tile is an initial segment `[0, L)`. -/
theorem Tile2.col (T : Tile2 P u v) (i : ℕ) : ∃ L, ∀ j, P i j ↔ j < L := by
  classical
  obtain ⟨N, hN⟩ := T.bdd
  have hex : ∃ j, ¬ P i j := ⟨N, fun h => by have := (hN _ _ h).2; omega⟩
  refine ⟨Nat.find hex, fun j => ⟨fun h => ?_, fun h => ?_⟩⟩
  · by_contra hj
    exact Nat.find_spec hex (T.down h le_rfl (by omega))
  · by_contra hP
    have := Nat.find_min' hex hP
    omega

/-- **Neighbour lemma (direction 0).** If `(q+1, r) ∉ D`, `(q, r) ∈ D` and the cell `(i, j)` has
`Φ(i, j) = Φ(q+1, r)`, then `i = 0` (else `(i-1, j)` and `(q, r)` would collide). -/
theorem Tile2.nbr0 (T : Tile2 P u v) {q r i j : ℕ} (hq : ¬ P (q + 1) r) (hq' : P q r)
    (hij : P i j) (he : phi2 u v i j = phi2 u v (q + 1) r) : i = 0 := by
  rcases i with _ | i
  · rfl
  · exfalso
    have h1 : P i j := T.down hij (Nat.le_succ i) le_rfl
    have h2 : phi2 u v i j = phi2 u v q r := by
      simp only [phi2] at he ⊢; push_cast at he; linear_combination he
    obtain ⟨rfl, rfl⟩ := T.inj h1 hq' h2
    exact hq hij

/-- **Neighbour lemma (direction 1).** -/
theorem Tile2.nbr1 (T : Tile2 P u v) {q r i j : ℕ} (hq : ¬ P r (q + 1)) (hq' : P r q)
    (hij : P i j) (he : phi2 u v i j = phi2 u v r (q + 1)) : j = 0 := by
  rcases j with _ | j
  · rfl
  · exfalso
    have h1 : P i j := T.down hij le_rfl (Nat.le_succ j)
    have h2 : phi2 u v i j = phi2 u v r q := by
      simp only [phi2] at he ⊢; push_cast at he; linear_combination he
    obtain ⟨rfl, rfl⟩ := T.inj h1 hq' h2
    exact hq hij

/-- **Inner corners lie in the lattice**: if `(i+1, j+1) ∉ D` but `(i, j+1), (i+1, j) ∈ D`, then
`Φ(i+1, j+1) = 0`. -/
theorem Tile2.corner (T : Tile2 P u v) {i j : ℕ} (h : ¬ P (i + 1) (j + 1)) (h0 : P i (j + 1))
    (h1 : P (i + 1) j) : phi2 u v (i + 1) (j + 1) = 0 := by
  obtain ⟨k, l, hkl, he⟩ := T.surj (phi2 u v (i + 1) (j + 1))
  have hk := T.nbr0 h h0 hkl he
  have hl := T.nbr1 h h1 hkl he
  subst hk hl
  rw [← he]
  simp [phi2]

/-- Two inner corners `(i₁+1, j₁+1)`, `(i₂+1, j₂+1)` with `i₁ < i₂` cannot coexist. -/
theorem Tile2.corner_lt (T : Tile2 P u v) {i₁ j₁ i₂ j₂ : ℕ}
    (c₁ : ¬ P (i₁ + 1) (j₁ + 1)) (c₁0 : P i₁ (j₁ + 1)) (c₁1 : P (i₁ + 1) j₁)
    (c₂ : ¬ P (i₂ + 1) (j₂ + 1)) (c₂0 : P i₂ (j₂ + 1)) (c₂1 : P (i₂ + 1) j₂)
    (hlt : i₁ < i₂) : False := by
  have hj : j₂ < j₁ := by
    by_contra hj
    exact c₁ (T.down c₂0 (by omega) (by omega))
  have e₁ := T.corner c₁ c₁0 c₁1
  have e₂ := T.corner c₂ c₂0 c₂1
  obtain ⟨α, rfl⟩ : ∃ α, i₂ = i₁ + 1 + α := ⟨i₂ - i₁ - 1, by omega⟩
  obtain ⟨β, rfl⟩ : ∃ β, j₁ = j₂ + 1 + β := ⟨j₁ - j₂ - 1, by omega⟩
  have hA : P (α + 1) 0 := T.down c₂0 (by omega) (Nat.zero_le _)
  have hB : P 0 (β + 1) := T.down c₁0 (Nat.zero_le _) (by omega)
  have he : phi2 u v (α + 1) 0 = phi2 u v 0 (β + 1) := by
    simp only [phi2] at e₁ e₂ ⊢; push_cast at e₁ e₂ ⊢; linear_combination e₂ - e₁
  have := T.inj hA hB he
  omega

/-- **At most one inner corner.** -/
theorem Tile2.corner_unique (T : Tile2 P u v) {i₁ j₁ i₂ j₂ : ℕ}
    (c₁ : ¬ P (i₁ + 1) (j₁ + 1)) (c₁0 : P i₁ (j₁ + 1)) (c₁1 : P (i₁ + 1) j₁)
    (c₂ : ¬ P (i₂ + 1) (j₂ + 1)) (c₂0 : P i₂ (j₂ + 1)) (c₂1 : P (i₂ + 1) j₂) :
    i₁ = i₂ ∧ j₁ = j₂ := by
  rcases lt_trichotomy i₁ i₂ with h | rfl | h
  · exact (T.corner_lt c₁ c₁0 c₁1 c₂ c₂0 c₂1 h).elim
  · refine ⟨rfl, ?_⟩
    rcases lt_trichotomy j₁ j₂ with hj | hj | hj
    · exact (c₁ (T.down c₂1 le_rfl (by omega))).elim
    · exact hj
    · exact (c₂ (T.down c₁1 le_rfl (by omega))).elim
  · exact (T.corner_lt c₂ c₂0 c₂1 c₁ c₁0 c₁1 h).elim

/-- **(L1) Classification of 2-D tiles.** The cells of a 2-D tile are
`[0,a)×[0,b') ∪ [0,a')×[0,b)` with `a' ≤ a`, `b' ≤ b` (a rectangle when `a' = a`, `b' = b`), and in
the L-shape case (`a' < a`, `b' < b`) `Φ(a, b') = Φ(0, b)`, i.e. `a·u = (b - b')·v`
(the lattice vector `(a, -c)`, `c = b - b'`).

Proof: `a`, `b` are the lengths of row `0` and column `0`; if `(a-1, b-1)` is a cell, `D` is the
rectangle. Otherwise let `b'` be the height of column `a-1` and `a'` the length of row `b-1`; then
`(a', h(a'))` and `(ℓ(b'), b')` are inner corners, hence equal (`corner_unique`), so `(a', b')` is
the unique inner corner and `Φ(a', b') = 0` (`corner`). The cell `(a, 0) ∉ D` has
`Φ(a, 0) = Φ(0, j)` for a cell `(0, j)` (`nbr0`). If `j < c`, the cells `(a - a', 0)` and
`(0, j + b')` collide. If `j > c`, `Φ(a, b - j) = Φ(0, b) = Φ(k, 0)` for a cell `(k, 0)` (`nbr1`),
and `nbr0` at `(a, b - j)` gives `k = 0`, so `Φ(0, b) = 0` and `(a', 0)`, `(0, c)` collide. Hence
`j = c`. -/
theorem Tile2.classify (T : Tile2 P u v) :
    ∃ a b a' b' : ℕ, a' ≤ a ∧ b' ≤ b ∧
      (∀ i j, P i j ↔ (i < a ∧ j < b') ∨ (i < a' ∧ j < b)) ∧
      (a' < a → b' < b → phi2 u v a b' = phi2 u v 0 b) := by
  obtain ⟨a, hA⟩ := T.row 0
  obtain ⟨b, hB⟩ := T.col 0
  have h00 := T.zero
  have ha1 : 0 < a := (hA 0).1 h00
  have hb1 : 0 < b := (hB 0).1 h00
  have hcell : ∀ {i j}, P i j → i < a ∧ j < b := fun h =>
    ⟨(hA _).1 (T.down h le_rfl (Nat.zero_le _)), (hB _).1 (T.down h (Nat.zero_le _) le_rfl)⟩
  by_cases hc : P (a - 1) (b - 1)
  · -- the rectangle `[0,a)×[0,b)`
    refine ⟨a, b, a, b, le_rfl, le_rfl, fun i j => ⟨fun h => Or.inl (hcell h), fun h => ?_⟩,
      fun h => absurd h (lt_irrefl _)⟩
    rcases h with ⟨hi, hj⟩ | ⟨hi, hj⟩ <;> exact T.down hc (by omega) (by omega)
  · -- an L-shape
    obtain ⟨b', hB'⟩ := T.col (a - 1)
    obtain ⟨a', hA'⟩ := T.row (b - 1)
    have hb'0 : 0 < b' := (hB' 0).1 ((hA _).2 (by omega))
    have hb'b : b' < b := by
      by_contra h; exact hc ((hB' _).2 (by omega))
    have ha'0 : 0 < a' := (hA' 0).1 ((hB _).2 (by omega))
    have ha'a : a' < a := by
      by_contra h; exact hc ((hA' _).2 (by omega))
    obtain ⟨j₁, hJ⟩ := T.col a'
    obtain ⟨i₂, hI⟩ := T.row b'
    have hj₁0 : 0 < j₁ := (hJ 0).1 ((hA _).2 ha'a)
    have hj₁b : j₁ ≤ b - 1 := by
      by_contra h; exact absurd ((hA' a').1 ((hJ _).2 (by omega))) (lt_irrefl _)
    have hi₂0 : 0 < i₂ := (hI 0).1 ((hB _).2 hb'b)
    have hi₂a : i₂ ≤ a - 1 := by
      by_contra h; exact absurd ((hB' b').1 ((hI _).2 (by omega))) (lt_irrefl _)
    obtain ⟨A, rfl⟩ : ∃ A, a' = A + 1 := ⟨a' - 1, by omega⟩
    obtain ⟨B, rfl⟩ : ∃ B, b' = B + 1 := ⟨b' - 1, by omega⟩
    obtain ⟨J, rfl⟩ : ∃ J, j₁ = J + 1 := ⟨j₁ - 1, by omega⟩
    obtain ⟨I, rfl⟩ : ∃ I, i₂ = I + 1 := ⟨i₂ - 1, by omega⟩
    -- the inner corners `(a', j₁)` and `(i₂, b')`
    have c₁ : ¬ P (A + 1) (J + 1) := fun h => absurd ((hJ _).1 h) (lt_irrefl _)
    have c₁0 : P A (J + 1) := T.down ((hA' A).2 (by omega)) le_rfl (by omega)
    have c₁1 : P (A + 1) J := (hJ J).2 (by omega)
    have c₂ : ¬ P (I + 1) (B + 1) := fun h => absurd ((hI _).1 h) (lt_irrefl _)
    have c₂0 : P I (B + 1) := (hI I).2 (by omega)
    have c₂1 : P (I + 1) B := T.down ((hB' B).2 (by omega)) (by omega) le_rfl
    obtain ⟨hAI, -⟩ := T.corner_unique c₁ c₁0 c₁1 c₂ c₂0 c₂1
    have hAB : ¬ P (A + 1) (B + 1) := by rw [hAI]; exact c₂
    have hAB0 : P A (B + 1) := by rw [hAI]; exact c₂0
    have hAB1 : P (A + 1) B := by rw [hAI]; exact c₂1
    have hcorner : phi2 u v (A + 1) (B + 1) = 0 := T.corner hAB hAB0 hAB1
    refine ⟨a, b, A + 1, B + 1, by omega, by omega,
      fun i j => ⟨fun h => ?_, fun h => ?_⟩, fun _ _ => ?_⟩
    · obtain ⟨hi, hj⟩ := hcell h
      by_contra hn
      exact hAB (T.down h (by omega) (by omega))
    · rcases h with ⟨hi, hj⟩ | ⟨hi, hj⟩
      · exact T.down ((hB' B).2 (by omega)) (by omega) (by omega)
      · exact T.down ((hA' A).2 (by omega)) (by omega) (by omega)
    · -- the lattice relation `Φ(a, b') = Φ(0, b)`
      obtain ⟨a₀, rfl⟩ : ∃ a₀, a = a₀ + 1 := ⟨a - 1, by omega⟩
      obtain ⟨c, rfl⟩ : ∃ c, b = B + 1 + c := ⟨b - (B + 1), by omega⟩
      obtain ⟨i, j, hij, he⟩ := T.surj (phi2 u v (a₀ + 1) 0)
      have hi0 : i = 0 := T.nbr0 (q := a₀) (r := 0)
        (fun h => by have := (hA _).1 h; omega) ((hA _).2 (by omega)) hij he
      subst hi0
      have hjb : j < B + 1 + c := (hcell hij).2
      rcases lt_trichotomy j c with hjc | hjc | hjc
      · -- `j < c`: the cells `(a - a', 0)` and `(0, j + b')` collide
        exfalso
        obtain ⟨δ, rfl⟩ : ∃ δ, a₀ = A + 1 + δ := ⟨a₀ - (A + 1), by omega⟩
        have hP1 : P (δ + 1) 0 := (hA _).2 (by omega)
        have hP2 : P 0 (j + (B + 1)) := (hB _).2 (by omega)
        have := T.inj hP1 hP2 (by
          simp only [phi2] at he hcorner ⊢; push_cast at he hcorner ⊢
          linear_combination -he - hcorner)
        omega
      · -- `j = c`: the relation
        subst hjc
        simp only [phi2] at he ⊢; push_cast at he ⊢; linear_combination -he
      · -- `j > c`: then `Φ(0, b) = 0`, and the cells `(a', 0)`, `(0, c)` collide
        exfalso
        obtain ⟨k, l, hkl, he'⟩ := T.surj (phi2 u v 0 (B + 1 + c))
        have hl0 : l = 0 := T.nbr1 (q := B + c) (r := 0)
          (fun h => by have := (hB _).1 h; omega) ((hB _).2 (by omega)) hkl
          (by rw [he', show B + 1 + c = B + c + 1 by omega])
        subst hl0
        obtain ⟨t, ht⟩ : ∃ t, B + 1 + c = j + t := ⟨B + 1 + c - j, by omega⟩
        have hk0 : k = 0 := T.nbr0 (q := a₀) (r := t)
          (fun h => by have := (hcell h).1; omega)
          (by simpa using (hB' t).2 (by omega)) hkl (by
            have ht' : ((B + 1 + c : ℕ) : ZMod m) = ((j + t : ℕ) : ZMod m) := by rw [ht]
            simp only [phi2] at he he' ⊢; push_cast at he he' ht' ⊢
            linear_combination he' + ht' * v + he)
        subst hk0
        have hb0 : phi2 u v 0 (B + 1 + c) = 0 := by rw [← he']; simp [phi2]
        have hP1 : P (A + 1) 0 := (hA _).2 (by omega)
        have hP2 : P 0 c := (hB _).2 (by omega)
        have := T.inj hP1 hP2 (by
          simp only [phi2] at hb0 hcorner ⊢; push_cast at hb0 hcorner ⊢
          linear_combination hcorner - hb0)
        omega

/-- **(L2) The corner sum is injective on the shapes of (L1).** With row lengths
`R(j) = if j < b' then a else a'` and column heights `C(i) = if i < a' then b else b'`, the map
`(i, j) ↦ Φ(R(j) + i, C(i) + j)` (which is `μ + u + v`) is injective on the cells. Only the
L-shape relation `Φ(a, b') = Φ(0, b)` is used (for one end of the row-end/column-top pairs). -/
theorem shape_inj
    (inj : ∀ {i j k l : ℕ}, P i j → P k l → phi2 u v i j = phi2 u v k l → i = k ∧ j = l)
    {a b a' b' : ℕ} (ha : a' ≤ a) (hb : b' ≤ b)
    (hmem : ∀ i j, P i j ↔ (i < a ∧ j < b') ∨ (i < a' ∧ j < b))
    (hrel : a' < a → b' < b → phi2 u v a b' = phi2 u v 0 b)
    {i j k l : ℕ} (hij : P i j) (hkl : P k l)
    (he : phi2 u v ((if j < b' then a else a') + i) ((if i < a' then b else b') + j) =
      phi2 u v ((if l < b' then a else a') + k) ((if k < a' then b else b') + l)) :
    i = k ∧ j = l := by
  obtain ⟨α, rfl⟩ : ∃ α, a = a' + α := ⟨a - a', by omega⟩
  obtain ⟨β, rfl⟩ : ∃ β, b = b' + β := ⟨b - b', by omega⟩
  have hij' := (hmem i j).1 hij
  have hkl' := (hmem k l).1 hkl
  have cell : ∀ x y, (x < a' + α ∧ y < b') ∨ (x < a' ∧ y < b' + β) → P x y :=
    fun x y h => (hmem x y).2 h
  have key : ∀ {x y z w : ℕ}, P x y → P z w →
      (x : ZMod m) * u + (y : ZMod m) * v = (z : ZMod m) * u + (w : ZMod m) * v → x = z ∧ y = w :=
    fun h1 h2 h => inj h1 h2 (by simpa only [phi2] using h)
  simp only [phi2] at he hrel
  by_cases hi : i < a' <;> by_cases hj : j < b' <;> by_cases hk : k < a' <;>
    by_cases hl : l < b' <;> simp only [hi, hj, hk, hl, ↓reduceIte] at he
  -- (Q, Q)
  · exact key hij hkl (by push_cast at he; linear_combination he)
  -- (Q, R₂)
  · have := key (cell (α + i) j (by omega)) hkl (by push_cast at he ⊢; linear_combination he)
    omega
  -- (Q, R₁)
  · have := key (cell i (β + j) (by omega)) hkl (by push_cast at he ⊢; linear_combination he)
    omega
  -- (Q, ∅)
  · omega
  -- (R₂, Q)
  · have := key hij (cell (α + k) l (by omega)) (by push_cast at he ⊢; linear_combination he)
    omega
  -- (R₂, R₂)
  · exact key hij hkl (by push_cast at he; linear_combination he)
  -- (R₂, R₁): uses the lattice relation
  · obtain ⟨k', rfl⟩ : ∃ k', k = a' + k' := ⟨k - a', by omega⟩
    have hr := hrel (by omega) (by omega)
    have := key hij (cell k' l (by omega)) (by
      push_cast at he hr ⊢; linear_combination he + hr)
    omega
  -- (R₂, ∅)
  · omega
  -- (R₁, Q)
  · have := key hij (cell k (β + l) (by omega)) (by push_cast at he ⊢; linear_combination he)
    omega
  -- (R₁, R₂): uses the lattice relation
  · obtain ⟨i', rfl⟩ : ∃ i', i = a' + i' := ⟨i - a', by omega⟩
    have hr := hrel (by omega) (by omega)
    have := key (cell i' j (by omega)) hkl (by
      push_cast at he hr ⊢; linear_combination he - hr)
    omega
  -- (R₁, R₁)
  · exact key hij hkl (by push_cast at he; linear_combination he)
  -- (R₁, ∅)
  · omega
  -- (∅, ·)
  all_goals omega

end Coord

/-! ## From `Finset (Fin 2 → ℕ)` to coordinates, and the assembly -/

section Assembly

/-- The point `(i, j) ∈ ℕ²` as a vector `Fin 2 → ℕ`. -/
def pt (i j : ℕ) : Fin 2 → ℕ := ![i, j]

theorem pt_eta (x : Fin 2 → ℕ) : pt (x 0) (x 1) = x := by
  funext k; fin_cases k <;> rfl

theorem tilePhi_eq_phi2 {m : ℕ} (p : Fin 2 → ZMod m) (x : Fin 2 → ℕ) :
    tilePhi p x = phi2 (p 0) (p 1) (x 0) (x 1) := by
  simp [tilePhi, phi2, Fin.sum_univ_two]

variable {m : ℕ} {D : Finset (Fin 2 → ℕ)} {p : Fin 2 → ZMod m}

/-- A 2-D tile `(D, p)` gives a coordinate tile with cells `{(i, j) : (i, j) ∈ D}`. -/
theorem tile2_of_isTile (h : IsTile D p) : Tile2 (fun i j => pt i j ∈ D) (p 0) (p 1) where
  down := fun hij hi hj => h.1 _ hij _ (fun k => by fin_cases k <;> simpa [pt])
  inj := fun h1 h2 he => by
    have := h.2.2.injOn h1 h2 (by rw [tilePhi_eq_phi2, tilePhi_eq_phi2]; simpa [pt] using he)
    exact ⟨by simpa [pt] using congrFun this 0, by simpa [pt] using congrFun this 1⟩
  surj := fun z => by
    obtain ⟨x, hx, hxz⟩ := h.2.2.2.2 (Set.mem_univ z)
    exact ⟨x 0, x 1, by rw [pt_eta]; exact hx, by rw [← hxz, tilePhi_eq_phi2]⟩
  bdd := ⟨D.sup (fun x => x 0 + x 1) + 1, fun i j hij => by
    have := Finset.le_sup (f := fun x : Fin 2 → ℕ => x 0 + x 1) hij
    simp [pt] at this
    omega⟩

/-- **(L2) The corner sum `μ(x) = φ(t₀ x) + φ(t₁ x)` is injective on every 2-D tile.** -/
theorem cornerSum_injOn_of_two (h : IsTile D p) :
    Set.InjOn (cornerSum D p) (D : Set (Fin 2 → ℕ)) := by
  have T := tile2_of_isTile h
  obtain ⟨a, b, a', b', ha, hb, hmem, hrel⟩ := T.classify
  have hmemD : ∀ x : Fin 2 → ℕ, x ∈ D ↔ (x 0 < a ∧ x 1 < b') ∨ (x 0 < a' ∧ x 1 < b) :=
    fun x => by have := hmem (x 0) (x 1); rwa [pt_eta] at this
  have key : ∀ x ∈ D, cornerSum D p x + (p 0 + p 1) =
      phi2 (p 0) (p 1) ((if x 1 < b' then a else a') + x 0)
        ((if x 0 < a' then b else b') + x 1) := by
    intro x hx
    have hx' := (hmemD x).1 hx
    have h0 : colHt D 0 x = (if x 1 < b' then a else a') - 1 - x 0 := by
      apply colHt_eq_of_iff
      intro k
      rw [hmemD]
      simp
      split_ifs <;> omega
    have h1 : colHt D 1 x = (if x 0 < a' then b else b') - 1 - x 1 := by
      apply colHt_eq_of_iff
      intro k
      rw [hmemD]
      simp
      split_ifs <;> omega
    have e0 : x 0 + colHt D 0 x + 1 = (if x 1 < b' then a else a') := by
      rw [h0]; split_ifs <;> omega
    have e1 : x 1 + colHt D 1 x + 1 = (if x 0 < a' then b else b') := by
      rw [h1]; split_ifs <;> omega
    have t0 : tilePhi p (colTop D 0 x) = phi2 (p 0) (p 1) (x 0 + colHt D 0 x) (x 1) := by
      rw [tilePhi_eq_phi2]; simp [colTop]
    have t1 : tilePhi p (colTop D 1 x) = phi2 (p 0) (p 1) (x 0) (x 1 + colHt D 1 x) := by
      rw [tilePhi_eq_phi2]; simp [colTop]
    rw [cornerSum, t0, t1, ← e0, ← e1]
    simp only [phi2]
    push_cast
    ring
  intro x hx y hy hxy
  have hx' : pt (x 0) (x 1) ∈ D := by rw [pt_eta]; exact hx
  have hy' : pt (y 0) (y 1) ∈ D := by rw [pt_eta]; exact hy
  have := shape_inj T.inj ha hb hmem hrel hx' hy' (by rw [← key x hx, ← key y hy, hxy])
  funext k
  fin_cases k
  · exact this.1
  · exact this.2

/-- **2-D Tile-CL**: every 2-dimensional tile satisfies `TileCLAt`. -/
theorem tileCLAt_of_two {m : ℕ} (D : Finset (Fin 2 → ℕ)) (p : Fin 2 → ZMod m)
    (h : IsTile D p) : TileCLAt D p :=
  tileCLAt_two_of_injOn h (cornerSum_injOn_of_two h)

end Assembly

/-! ## Tile-CL for `d ≤ 2` and Wilf for embedding dimension `≤ 3` -/

/-- Tile-CL holds for every tile of dimension `d ≤ 2` (for `d ≤ 1` the bound `(d-1)·m(m-1)/2` is
`0`). -/
theorem tileCLAt_of_le_two {d m : ℕ} (hd : d ≤ 2) (D : Finset (Fin d → ℕ)) (p : Fin d → ZMod m)
    (h : IsTile D p) : TileCLAt D p := by
  rcases Nat.lt_or_ge d 2 with hd' | hd'
  · intro s
    have : d - 1 = 0 := by omega
    rw [this, zero_mul]
    exact Nat.zero_le _
  · obtain rfl : d = 2 := le_antisymm hd hd'
    exact tileCLAt_of_two D p h

/-- **Wilf's conjecture for embedding dimension `≤ 3`** (known: Fröberg–Gottlieb–Häggkvist 1987),
via 2-D Tile-CL ⇒ CL ⇒ Wilf: `d = |P'| = e - 1 ≤ 2`. -/
theorem wilf_of_embDim_le_three (S : NumericalSemigroup) (he : S.embDim ≤ 3) :
    S.conductor ≤ S.embDim * S.ell := by
  have hd : S.primitives'.card ≤ 2 := by
    have := card_primitives'_add_one (S := S)
    omega
  exact wilf_of_CL (CL_of_tileCLAt (tileCLAt_of_le_two hd _ _ isTile_factDownSet))

end NumericalSemigroup
