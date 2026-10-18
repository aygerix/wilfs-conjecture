import Wilf.TileCL2

/-!
# Lemma B (corner–area bound), Lemma CHT (counting criterion) and Lemma T (type bound) in `ℕ³`

Formalization of `.research/PROOFS.md`, section "e = 4, asymptotic HT via the counting criterion
CHT" (2026-10-18), Lemmas B, CHT and T. Points are `Fin 3 → ℕ`, `e_a = Pi.single a 1`, down-sets are
`IsDownSetFin` (`Wilf.Carry`), `top_a x = colTop D a x` (`Wilf.TileCL2`), maximal cells are
`IsMaxCell` (`Wilf.TileTop`). Coordinates are 0-based.

**Lemma B** (`cornerArea`). Let `D ⊆ ℕ³` be a nonempty finite down-set, `m = |D|`. For `c ∈ Fin 3`
let `A_c = face D c = {x ∈ D : x c = 0}` and let `k_c = |faceCorners D c|`, the number of
`x ∈ A_c` with `x + e_a ∉ D` for both `a ≠ c`. With `C = k₀ + k₁ + k₂`:

    C² + 6 ≤ 6m + 3C.

Proof (as on paper). (1) Inclusion–exclusion over the three faces: the pairwise intersections are
the axis segments and the triple intersection is `{0}` (`card_union3`, `face_inter3`).
(2) A 2-D down-set with `k ≥ 1` corners and arms `L, L'` has at least `L + L' − 1 + T(k)` cells,
`2·T(k) = (k−1)(k−2)` (`Grid2.area`). Instead of sorting the corners we use pigeonhole
(`Grid2.exists_corner`): for `u < k` at most `u` corners have first coordinate `< u`, so at least
`k − u` have first coordinate `≥ u`; their second coordinates are distinct, so one is `≥ k − u − 1`.
Hence `(i+1, k−1−j) ∈ A` for `i < j < k−1`, an injective image of `Σ_{j<k−1} j` interior cells.
(3) Corners of a 2-D down-set have distinct coordinates, so `k ≤` each arm length
(`Grid2.card_corners_le_f`); the faces are paired cyclically with the axes
(`k₀ ≤ |A₀ ∩ A₂|`, `k₁ ≤ |A₀ ∩ A₁|`, `k₂ ≤ |A₁ ∩ A₂|`). (4) `(Σk)² ≤ 3Σk²` (`arith`).
The 2-D part is proved once for an abstract "grid" (`Grid2`: a finset with two coordinates and a
point constructor) and instantiated on each face (`grid_face`, `faceCorners_eq`).

**Lemma CHT** (`cht`). For `x ∈ D`: `ht(y) = max{|z| − |y| : z ∈ D, z ≥ y}` (`ht`, `|z| = Σ_a z_a`),
`h(x) = Σ_a ht(top_a x)` (`hsum`), `Max = maxSet D`, `t = |Max|`, `n(x) = #{a : top_a x ∈ Max}`
(`nTop`), `Tri = {x ∈ D ∖ Max : n(x) = 3}` (`triSet`), `Q' = {x ∈ D : n(x) = 2 ∧ h(x) = 1}` (`qSet`).
Then

    2m ≤ H + 2t + 2|Tri| + |Q'|,   H = Σ_{x∈D} h(x).

This holds for **every** finite `D ⊆ ℕ³` (no down-set or nonemptiness hypothesis is used, so the
statement is stronger than the one requested). Proof: pointwise `h(x) + 2[x∈Max] + 2[x∈Tri] +
[x∈Q'] ≥ 2`, because a non-maximal `y ∈ D` has `ht(y) ≥ 1` (`one_le_ht`).
Cross-checks of the definitions: `ht_eq_zero_of_mem_maxSet` (for a down-set, `ht = 0` on `Max`),
`ht_spec` (for `y ∈ D` the `sup` is attained, i.e. it is the max), `decide`-checked examples for
Lemma B's quantities (`D = {0}`: `C = 3`, `m = 1`, equality; `D = {0, e₀, e₁, e₂}`: `C = 6`, `m = 4`,
equality).

**Lemma T** (`typeBound`, type bound for the Loomis–Whitney class 𝒞). `LWClass D L₁ h F G` says
(0-based coordinates) `D = {x : x 0 < L₁, x 1 < h(x 0), x 2 < min(F(x 0), G(x 1))}` with
`dom h = dom F = [0, L₁)`, `dom G = [0, h 0)` (so `h(0) = #dom G`), `h, F, G` nonincreasing and
`≥ 1` on their domains, `L₁ ≥ 1`, `F(0) = G(0)`. Then, with `t = |Max|` and `C` as in Lemma B,

    t + 2 ≤ C      (i.e. t ≤ C − 2).

The proof is an explicit injection (`mapA_mem`, `mapF_mem`, `mapG_mem`, `branchF_aux`,
`branchG_aux`) of `Max` into `corners(A₂) ⊔ (corners(A₁) ∖ {cornerF}) ⊔ (corners(A₀) ∖ {cornerG})`,
a direct form of the paper's slice/telescoping argument (each maximal cell is charged to the level
at which its slice corner is born); see the docstring of `typeBound`.
-/

namespace NumericalSemigroup

open Finset

namespace CornerArea

section TwoD

variable {α : Type*} [DecidableEq α]

/-- A finite set `A` with two coordinates `f, g : α → ℕ` and a point constructor `mk` that make it
a 2-D down-set in coordinates. -/
structure Grid2 (A : Finset α) (f g : α → ℕ) (mk : ℕ → ℕ → α) : Prop where
  f_mk : ∀ u w, f (mk u w) = u
  g_mk : ∀ u w, g (mk u w) = w
  eta : ∀ x ∈ A, mk (f x) (g x) = x
  down : ∀ x ∈ A, ∀ u w, u ≤ f x → w ≤ g x → mk u w ∈ A

/-- Corners (maximal elements) of a 2-D grid set. -/
def corners2 (A : Finset α) (f g : α → ℕ) (mk : ℕ → ℕ → α) : Finset α :=
  A.filter (fun x => mk (f x + 1) (g x) ∉ A ∧ mk (f x) (g x + 1) ∉ A)

variable {A : Finset α} {f g : α → ℕ} {mk : ℕ → ℕ → α}

theorem Grid2.injOn_f (G : Grid2 A f g mk) : Set.InjOn f (corners2 A f g mk : Set α) := by
  intro x hx y hy hxy
  simp only [corners2, coe_filter, Set.mem_ofPred_eq] at hx hy
  have key : ∀ x y, y ∈ A → mk (f x) (g x + 1) ∉ A → f x = f y → g y ≤ g x := by
    intro x y hy hx' hxy
    by_contra h
    exact hx' (G.down y hy _ _ hxy.le (by omega))
  have h1 := key x y hy.1 hx.2.2 hxy
  have h2 := key y x hx.1 hy.2.2 hxy.symm
  rw [← G.eta x hx.1, ← G.eta y hy.1, hxy, le_antisymm h2 h1]

theorem Grid2.injOn_g (G : Grid2 A f g mk) : Set.InjOn g (corners2 A f g mk : Set α) := by
  intro x hx y hy hxy
  simp only [corners2, coe_filter, Set.mem_ofPred_eq] at hx hy
  have key : ∀ x y, y ∈ A → mk (f x + 1) (g x) ∉ A → g x = g y → f y ≤ f x := by
    intro x y hy hx' hxy
    by_contra h
    exact hx' (G.down y hy _ _ (by omega) hxy.le)
  have h1 := key x y hy.1 hx.2.1 hxy
  have h2 := key y x hx.1 hy.2.1 hxy.symm
  rw [← G.eta x hx.1, ← G.eta y hy.1, hxy, le_antisymm h2 h1]

/-- A finset of naturals of size `n` has an element `≥ n - 1`. -/
theorem exists_ge_card_sub_one {s : Finset ℕ} (hs : s.Nonempty) : ∃ i ∈ s, s.card - 1 ≤ i := by
  obtain ⟨i, hi, himax⟩ := s.exists_max_image id hs
  refine ⟨i, hi, ?_⟩
  have : s.card ≤ (range (i + 1)).card :=
    card_le_card fun j hj => mem_range.2 (Nat.lt_succ_of_le (himax j hj))
  rw [card_range] at this
  omega

/-- **Pigeonhole.** If `u < k` (`k` the number of corners), some corner `p` has `f p ≥ u` and
`g p ≥ k - u - 1`. -/
theorem Grid2.exists_corner (G : Grid2 A f g mk) {u : ℕ} (hu : u < (corners2 A f g mk).card) :
    ∃ p ∈ corners2 A f g mk, u ≤ f p ∧ (corners2 A f g mk).card - u - 1 ≤ g p := by
  set K := corners2 A f g mk with hK
  have hsmall : (K.filter (fun p => f p < u)).card ≤ u := by
    calc (K.filter (fun p => f p < u)).card ≤ (range u).card :=
          card_le_card_of_injOn f (fun p hp => mem_range.2 (mem_filter.1 hp).2)
            (G.injOn_f.mono (by simp only [coe_filter]; exact fun p hp => hp.1))
      _ = u := card_range u
  have hsplit := card_filter_add_card_filter_not (s := K) (fun p => f p < u)
  have himg : ((K.filter (fun p => ¬ f p < u)).image g).card =
      (K.filter (fun p => ¬ f p < u)).card :=
    card_image_of_injOn (G.injOn_g.mono (by simp only [coe_filter]; exact fun p hp => hp.1))
  have hne : ((K.filter (fun p => ¬ f p < u)).image g).Nonempty := by
    rw [← card_pos, himg]; omega
  obtain ⟨i, hi, hile⟩ := exists_ge_card_sub_one hne
  obtain ⟨p, hp, rfl⟩ := mem_image.1 hi
  have hp' := mem_filter.1 hp
  rw [himg] at hile
  exact ⟨p, hp'.1, by omega, by omega⟩

/-- The triangle cells `(i+1, k-1-j)`, `i < j < k-1`, lie in `A`. -/
theorem Grid2.tri_mem (G : Grid2 A f g mk) {i j : ℕ} (hj : j < (corners2 A f g mk).card - 1)
    (hi : i < j) : mk (i + 1) ((corners2 A f g mk).card - 1 - j) ∈ A := by
  obtain ⟨p, hp, h1, h2⟩ := G.exists_corner (u := i + 1) (by omega)
  exact G.down p (mem_filter.1 hp).1 _ _ h1 (by omega)

/-- The interior `{f ≠ 0, g ≠ 0}` has at least `T(k) = Σ_{j<k-1} j` cells. -/
theorem Grid2.sum_le_card_interior (G : Grid2 A f g mk) :
    ∑ j ∈ range ((corners2 A f g mk).card - 1), j ≤
      (A.filter (fun x => f x ≠ 0 ∧ g x ≠ 0)).card := by
  set n := (corners2 A f g mk).card - 1 with hn
  have hsig : ((range n).sigma (fun j => range j)).card = ∑ j ∈ range n, j := by
    rw [card_sigma]; simp
  rw [← hsig]
  refine card_le_card_of_injOn (fun q => mk (q.2 + 1) (n - q.1)) ?_ ?_
  · rintro ⟨j, i⟩ hq
    simp only [coe_sigma, Set.mem_sigma_iff, coe_range, Set.mem_Iio] at hq
    simp only [coe_filter, Set.mem_ofPred_eq]
    refine ⟨G.tri_mem hq.1 hq.2, ?_, ?_⟩
    · rw [G.f_mk]; omega
    · rw [G.g_mk]; omega
  · rintro ⟨j, i⟩ hq ⟨j', i'⟩ hq' h
    simp only [coe_sigma, Set.mem_sigma_iff, coe_range, Set.mem_Iio] at hq hq'
    have h1 := congrArg f h
    have h2 := congrArg g h
    simp only [G.f_mk, G.g_mk] at h1 h2
    have : j = j' := by omega
    subst this
    have : i = i' := by omega
    subst this
    rfl

/-- `|A| + 1 = L₁ + L₂ + |interior|` for a nonempty grid set. -/
theorem Grid2.card_decomp (G : Grid2 A f g mk) (hne : A.Nonempty) :
    A.card + 1 = (A.filter (fun x => g x = 0)).card + (A.filter (fun x => f x = 0)).card +
      (A.filter (fun x => f x ≠ 0 ∧ g x ≠ 0)).card := by
  have h00 : mk 0 0 ∈ A := by
    obtain ⟨x, hx⟩ := hne
    exact G.down x hx 0 0 (Nat.zero_le _) (Nat.zero_le _)
  have hint : A.filter (fun x => g x = 0) ∩ A.filter (fun x => f x = 0) = {mk 0 0} := by
    ext x
    simp only [mem_inter, mem_filter, mem_singleton]
    constructor
    · rintro ⟨⟨hx, hg⟩, -, hf⟩
      rw [← G.eta x hx, hf, hg]
    · rintro rfl
      exact ⟨⟨h00, G.g_mk 0 0⟩, h00, G.f_mk 0 0⟩
  have hunion : A.filter (fun x => g x = 0) ∪ A.filter (fun x => f x = 0) =
      A.filter (fun x => ¬ (f x ≠ 0 ∧ g x ≠ 0)) := by
    ext x
    simp only [mem_union, mem_filter]
    constructor
    · rintro (⟨hx, h⟩ | ⟨hx, h⟩) <;> exact ⟨hx, by omega⟩
    · rintro ⟨hx, h⟩
      by_cases hg : g x = 0
      · exact Or.inl ⟨hx, hg⟩
      · exact Or.inr ⟨hx, by omega⟩
  have h1 := card_union_add_card_inter (A.filter (fun x => g x = 0)) (A.filter (fun x => f x = 0))
  rw [hint, card_singleton, hunion] at h1
  have h2 := card_filter_add_card_filter_not (s := A) (fun x => f x ≠ 0 ∧ g x ≠ 0)
  omega

/-- **2-D area bound**: `2·L₁ + 2·L₂ + (k-1)(k-2) ≤ 2·|A| + 2`. -/
theorem Grid2.area (G : Grid2 A f g mk) (hne : A.Nonempty) :
    2 * (A.filter (fun x => g x = 0)).card + 2 * (A.filter (fun x => f x = 0)).card +
      ((corners2 A f g mk).card - 1) * ((corners2 A f g mk).card - 2) ≤ 2 * A.card + 2 := by
  have h1 := G.card_decomp hne
  have h2 := G.sum_le_card_interior
  have h3 := sum_range_id_mul_two ((corners2 A f g mk).card - 1)
  rw [show (corners2 A f g mk).card - 1 - 1 = (corners2 A f g mk).card - 2 by omega] at h3
  omega

/-- `k ≤ L₁` (corners have distinct `f`-coordinates). -/
theorem Grid2.card_corners_le_f (G : Grid2 A f g mk) :
    (corners2 A f g mk).card ≤ (A.filter (fun x => g x = 0)).card := by
  refine card_le_card_of_injOn (fun p => mk (f p) 0) ?_ ?_
  · intro p hp
    have hp' := mem_filter.1 hp
    simp only [coe_filter, Set.mem_ofPred_eq]
    exact ⟨G.down p hp'.1 _ _ le_rfl (Nat.zero_le _), G.g_mk _ _⟩
  · intro p hp q hq h
    exact G.injOn_f hp hq (by simpa only [G.f_mk] using congrArg f h)

/-- `k ≤ L₂` (corners have distinct `g`-coordinates). -/
theorem Grid2.card_corners_le_g (G : Grid2 A f g mk) :
    (corners2 A f g mk).card ≤ (A.filter (fun x => f x = 0)).card := by
  refine card_le_card_of_injOn (fun p => mk 0 (g p)) ?_ ?_
  · intro p hp
    have hp' := mem_filter.1 hp
    simp only [coe_filter, Set.mem_ofPred_eq]
    exact ⟨G.down p hp'.1 _ _ (Nat.zero_le _) le_rfl, G.f_mk _ _⟩
  · intro p hp q hq h
    exact G.injOn_g hp hq (by simpa only [G.g_mk] using congrArg g h)

/-- A nonempty grid set has a corner. -/
theorem Grid2.one_le_card_corners (G : Grid2 A f g mk) (hne : A.Nonempty) :
    1 ≤ (corners2 A f g mk).card := by
  obtain ⟨x, hx, hmax⟩ := A.exists_max_image (fun x => f x + g x) hne
  have : x ∈ corners2 A f g mk := by
    refine mem_filter.2 ⟨hx, fun h => ?_, fun h => ?_⟩
    · have := hmax _ h; rw [G.f_mk, G.g_mk] at this; omega
    · have := hmax _ h; rw [G.f_mk, G.g_mk] at this; omega
  exact card_pos.2 ⟨x, this⟩

end TwoD

section ThreeD

/-- Every index of `Fin 3` is one of three pairwise distinct indices. -/
theorem fin3_cases {a b c : Fin 3} (hab : a ≠ b) (hac : a ≠ c) (hbc : b ≠ c) (i : Fin 3) :
    i = a ∨ i = b ∨ i = c := by
  revert a b c i; decide

/-- The point `u·e_a + w·e_b`. -/
def mk2 (a b : Fin 3) (u w : ℕ) : Fin 3 → ℕ := Pi.single a u + Pi.single b w

variable {D : Finset (Fin 3 → ℕ)}

/-- The face `A_c = {x ∈ D : x c = 0}`. -/
def face (D : Finset (Fin 3 → ℕ)) (c : Fin 3) : Finset (Fin 3 → ℕ) := D.filter (fun x => x c = 0)

/-- The corners of the face `A_c`: the `x ∈ A_c` with `x + e_a ∉ D` for both `a ≠ c`
(the maximal elements of the 2-D down-set `A_c`). -/
def faceCorners (D : Finset (Fin 3 → ℕ)) (c : Fin 3) : Finset (Fin 3 → ℕ) :=
  (face D c).filter (fun x => ∀ a, a ≠ c → x + Pi.single a 1 ∉ D)

theorem grid_face (hD : IsDownSetFin D) {a b c : Fin 3} (hab : a ≠ b) (hac : a ≠ c)
    (hbc : b ≠ c) : Grid2 (face D c) (fun x => x a) (fun x => x b) (mk2 a b) where
  f_mk u w := by simp [mk2, Pi.single_eq_of_ne hab]
  g_mk u w := by simp [mk2, Pi.single_eq_of_ne hab.symm]
  eta x hx := by
    have hc := (mem_filter.1 hx).2
    funext i
    rcases fin3_cases hab hac hbc i with rfl | rfl | rfl
    · simp [mk2, Pi.single_eq_of_ne hab]
    · simp [mk2, Pi.single_eq_of_ne hab.symm]
    · simp [mk2, Pi.single_eq_of_ne hac.symm, Pi.single_eq_of_ne hbc.symm, hc]
  down x hx u w hu hw := by
    have hx' := mem_filter.1 hx
    refine mem_filter.2 ⟨hD x hx'.1 _ (fun i => ?_), ?_⟩
    · rcases fin3_cases hab hac hbc i with rfl | rfl | rfl
      · simpa [mk2, Pi.single_eq_of_ne hab] using hu
      · simpa [mk2, Pi.single_eq_of_ne hab.symm] using hw
      · simp [mk2, Pi.single_eq_of_ne hac.symm, Pi.single_eq_of_ne hbc.symm]
    · simp [mk2, Pi.single_eq_of_ne hac.symm, Pi.single_eq_of_ne hbc.symm]

theorem faceCorners_eq {a b c : Fin 3} (hab : a ≠ b) (hac : a ≠ c)
    (hbc : b ≠ c) :
    faceCorners D c = corners2 (face D c) (fun x => x a) (fun x => x b) (mk2 a b) := by
  unfold faceCorners corners2
  refine filter_congr fun x hx => ?_
  have hc := (mem_filter.1 hx).2
  have hA : mk2 a b (x a + 1) (x b) = x + Pi.single a 1 := by
    funext i
    rcases fin3_cases hab hac hbc i with rfl | rfl | rfl
    · simp [mk2, Pi.single_eq_of_ne hab]
    · simp [mk2, Pi.single_eq_of_ne hab.symm]
    · simp [mk2, Pi.single_eq_of_ne hac.symm, Pi.single_eq_of_ne hbc.symm, hc]
  have hB : mk2 a b (x a) (x b + 1) = x + Pi.single b 1 := by
    funext i
    rcases fin3_cases hab hac hbc i with rfl | rfl | rfl
    · simp [mk2, Pi.single_eq_of_ne hab]
    · simp [mk2, Pi.single_eq_of_ne hab.symm]
    · simp [mk2, Pi.single_eq_of_ne hac.symm, Pi.single_eq_of_ne hbc.symm, hc]
  have hmem : ∀ a', a' ≠ c → (x + Pi.single a' 1 ∈ face D c ↔ x + Pi.single a' 1 ∈ D) := by
    intro a' ha'
    simp [face, Pi.single_eq_of_ne ha'.symm, hc]
  rw [hA, hB, hmem a hac, hmem b hbc]
  constructor
  · intro h; exact ⟨h a hac, h b hbc⟩
  · rintro ⟨h1, h2⟩ a' ha'
    rcases fin3_cases hab hac hbc a' with rfl | rfl | rfl
    · exact h1
    · exact h2
    · exact absurd rfl ha'

theorem face_filter (D : Finset (Fin 3 → ℕ)) (c b : Fin 3) :
    (face D c).filter (fun x => x b = 0) = face D c ∩ face D b := by
  ext x; simp only [face, mem_filter, mem_inter]; tauto

theorem zero_mem (hD : IsDownSetFin D) (hne : D.Nonempty) : (0 : Fin 3 → ℕ) ∈ D := by
  obtain ⟨x, hx⟩ := hne
  exact hD x hx 0 (fun i => Nat.zero_le _)

/-- The 2-D bounds for one face `A_c` (with the two other axes `a, b`). -/
theorem face_bound (hD : IsDownSetFin D) (hne : D.Nonempty) {a b c : Fin 3} (hab : a ≠ b)
    (hac : a ≠ c) (hbc : b ≠ c) :
    2 * (face D c ∩ face D b).card + 2 * (face D c ∩ face D a).card +
        ((faceCorners D c).card - 1) * ((faceCorners D c).card - 2) ≤ 2 * (face D c).card + 2 ∧
      (faceCorners D c).card ≤ (face D c ∩ face D b).card ∧ 1 ≤ (faceCorners D c).card := by
  have G := grid_face hD hab hac hbc
  have hF : (face D c).Nonempty := ⟨0, mem_filter.2 ⟨zero_mem hD hne, rfl⟩⟩
  rw [faceCorners_eq hab hac hbc, ← face_filter, ← face_filter]
  exact ⟨G.area hF, G.card_corners_le_f, G.one_le_card_corners hF⟩

/-- Inclusion–exclusion for three finsets. -/
theorem card_union3 {β : Type*} [DecidableEq β] (F₀ F₁ F₂ : Finset β) :
    (F₀ ∪ F₁ ∪ F₂).card + (F₀ ∩ F₁).card + (F₀ ∩ F₂).card + (F₁ ∩ F₂).card =
      F₀.card + F₁.card + F₂.card + (F₀ ∩ F₁ ∩ F₂).card := by
  have h1 := card_union_add_card_inter F₀ F₁
  have h2 := card_union_add_card_inter (F₀ ∪ F₁) F₂
  rw [union_inter_distrib_right] at h2
  have h3 := card_union_add_card_inter (F₀ ∩ F₂) (F₁ ∩ F₂)
  have h4 : (F₀ ∩ F₂) ∩ (F₁ ∩ F₂) = F₀ ∩ F₁ ∩ F₂ := by
    ext x; simp only [mem_inter]; tauto
  rw [h4] at h3
  omega

theorem face_inter3 (hD : IsDownSetFin D) (hne : D.Nonempty) :
    face D 0 ∩ face D 1 ∩ face D 2 = {0} := by
  ext x
  simp only [face, mem_inter, mem_filter, mem_singleton]
  constructor
  · rintro ⟨⟨⟨-, h0⟩, -, h1⟩, -, h2⟩
    funext i; fin_cases i <;> simp [h0, h1, h2]
  · rintro rfl
    have := zero_mem hD hne
    simp [this]

theorem tri_identity {k : ℕ} (hk : 1 ≤ k) : (k - 1) * (k - 2) + 3 * k = k * k + 2 := by
  obtain ⟨j, rfl⟩ := Nat.exists_eq_add_of_le hk
  rcases j with _ | j
  · simp
  · rw [show 1 + (j + 1) - 1 = j + 1 by omega, show 1 + (j + 1) - 2 = j by omega]; ring

theorem arith {m U F₀ F₁ F₂ X₀₁ X₀₂ X₁₂ k₀ k₁ k₂ P₀ P₁ P₂ : ℕ} (hU : U ≤ m)
    (hie : U + X₀₁ + X₀₂ + X₁₂ = F₀ + F₁ + F₂ + 1)
    (b₀ : 2 * X₀₂ + 2 * X₀₁ + P₀ ≤ 2 * F₀ + 2) (b₁ : 2 * X₀₁ + 2 * X₁₂ + P₁ ≤ 2 * F₁ + 2)
    (b₂ : 2 * X₁₂ + 2 * X₀₂ + P₂ ≤ 2 * F₂ + 2)
    (l₀ : k₀ ≤ X₀₂) (l₁ : k₁ ≤ X₀₁) (l₂ : k₂ ≤ X₁₂)
    (e₀ : P₀ + 3 * k₀ = k₀ * k₀ + 2) (e₁ : P₁ + 3 * k₁ = k₁ * k₁ + 2)
    (e₂ : P₂ + 3 * k₂ = k₂ * k₂ + 2) :
    (k₀ + k₁ + k₂) ^ 2 + 6 ≤ 6 * m + 3 * (k₀ + k₁ + k₂) := by
  have key : ((k₀ + k₁ + k₂ : ℕ) : ℤ) ^ 2 ≤ 3 * ((k₀ : ℤ) * k₀ + k₁ * k₁ + k₂ * k₂) := by
    push_cast
    nlinarith [sq_nonneg ((k₀ : ℤ) - k₁), sq_nonneg ((k₀ : ℤ) - k₂), sq_nonneg ((k₁ : ℤ) - k₂)]
  zify at *
  linarith

/-- **Lemma B (corner–area bound).** For a nonempty finite down-set `D ⊆ ℕ³` with `m = |D|`, let
`k_c` be the number of corners of the face `A_c = {x ∈ D : x c = 0}` and `C = k₀ + k₁ + k₂`. Then
`C² + 6 ≤ 6m + 3C` (i.e. `C² − 3C + 6 ≤ 6m`). -/
theorem cornerArea (hD : IsDownSetFin D) (hne : D.Nonempty) :
    (∑ c, (faceCorners D c).card) ^ 2 + 6 ≤ 6 * D.card + 3 * ∑ c, (faceCorners D c).card := by
  obtain ⟨b₀, l₀, k₀⟩ := face_bound hD hne (a := 1) (b := 2) (c := 0) (by decide) (by decide)
    (by decide)
  obtain ⟨b₁, l₁, k₁⟩ := face_bound hD hne (a := 2) (b := 0) (c := 1) (by decide) (by decide)
    (by decide)
  obtain ⟨b₂, l₂, k₂⟩ := face_bound hD hne (a := 0) (b := 1) (c := 2) (by decide) (by decide)
    (by decide)
  rw [inter_comm (face D 1) (face D 0)] at b₁ l₁
  rw [inter_comm (face D 2) (face D 1), inter_comm (face D 2) (face D 0)] at b₂
  rw [inter_comm (face D 2) (face D 1)] at l₂
  have hie := card_union3 (face D 0) (face D 1) (face D 2)
  rw [face_inter3 hD hne, card_singleton] at hie
  have hU : (face D 0 ∪ face D 1 ∪ face D 2).card ≤ D.card :=
    card_le_card (union_subset (union_subset (filter_subset _ _) (filter_subset _ _))
      (filter_subset _ _))
  rw [Fin.sum_univ_three]
  exact arith hU hie b₀ b₁ b₂ l₀ l₁ l₂ (tri_identity k₀) (tri_identity k₁) (tri_identity k₂)

end ThreeD

/-! ## Sanity checks (kernel `decide`) for the conventions of Lemma B -/

/-- `D = {0}`: `C = 3` (`m = 1`; Lemma B is an equality: `9 + 6 = 6 + 9`). -/
example : (∑ c, (faceCorners ({0} : Finset (Fin 3 → ℕ)) c).card) = 3 := by decide

/-- `D = {0, e₀, e₁, e₂}`: `C = 6`, `m = 4` (Lemma B is an equality: `36 + 6 = 24 + 18`). -/
example : (∑ c, (faceCorners ({![0,0,0], ![1,0,0], ![0,1,0], ![0,0,1]} :
    Finset (Fin 3 → ℕ)) c).card) = 6 := by decide

example : ({![0,0,0], ![1,0,0], ![0,1,0], ![0,0,1]} : Finset (Fin 3 → ℕ)).card = 4 := by decide

section CHT

variable (D : Finset (Fin 3 → ℕ))

/-- `ht(y) = max {|z| − |y| : z ∈ D, z ≥ y}` with `|z| = Σ_a z_a` and `z ≥ y` pointwise
(`= 0` if no `z ∈ D` lies above `y`; it is only used at points `y ∈ D`, where the max is over a
nonempty set containing `z = y`). -/
def ht (y : Fin 3 → ℕ) : ℕ :=
  (D.filter (fun z => ∀ a, y a ≤ z a)).sup (fun z => (∑ a, z a) - ∑ a, y a)

/-- `h(x) = Σ_a ht(top_a x)`, where `top_a x = colTop D a x = x + s·e_a`, `s` maximal with
`x + s·e_a ∈ D`. -/
noncomputable def hsum (x : Fin 3 → ℕ) : ℕ := ∑ a, ht D (colTop D a x)

/-- `Max = {x ∈ D : x + e_a ∉ D ∀ a}`. -/
def maxSet : Finset (Fin 3 → ℕ) := D.filter (IsMaxCell D)

/-- `n(x) = #{a : top_a x ∈ Max}`. -/
noncomputable def nTop (x : Fin 3 → ℕ) : ℕ :=
  (univ.filter (fun a : Fin 3 => colTop D a x ∈ maxSet D)).card

/-- `Tri = {x ∈ D ∖ Max : n(x) = 3}`. -/
noncomputable def triSet : Finset (Fin 3 → ℕ) := (D \ maxSet D).filter (fun x => nTop D x = 3)

/-- `Q' = {x ∈ D : n(x) = 2 ∧ h(x) = 1}`. -/
noncomputable def qSet : Finset (Fin 3 → ℕ) := D.filter (fun x => nTop D x = 2 ∧ hsum D x = 1)

variable {D}

theorem colTop_mem {a : Fin 3} {x : Fin 3 → ℕ} (hx : x ∈ D) : colTop D a x ∈ D := colHt_spec hx

/-- `top_a x = x + s·e_a` with `s` maximal such that `x + s·e_a ∈ D` (for `x ∈ D`). -/
theorem colTop_spec {a : Fin 3} {x : Fin 3 → ℕ} (hx : x ∈ D) :
    ∃ s, colTop D a x = x + Pi.single a s ∧ x + Pi.single a s ∈ D ∧
      ∀ s', x + Pi.single a s' ∈ D → s' ≤ s :=
  ⟨colHt D a x, rfl, colHt_spec hx, fun _ h => le_colHt h⟩

/-- For `y ∈ D`, `ht D y` is the maximum of `|z| − |y|` over `z ∈ D`, `z ≥ y` (attained). -/
theorem ht_spec {y : Fin 3 → ℕ} (hy : y ∈ D) :
    (∃ z ∈ D, (∀ a, y a ≤ z a) ∧ ht D y = (∑ a, z a) - ∑ a, y a) ∧
      ∀ z ∈ D, (∀ a, y a ≤ z a) → (∑ a, z a) - ∑ a, y a ≤ ht D y := by
  constructor
  · obtain ⟨z, hz, hzeq⟩ := Finset.exists_mem_eq_sup (D.filter (fun z => ∀ a, y a ≤ z a))
      ⟨y, mem_filter.2 ⟨hy, fun a => le_rfl⟩⟩ (fun z => (∑ a, z a) - ∑ a, y a)
    exact ⟨z, (mem_filter.1 hz).1, (mem_filter.1 hz).2, hzeq⟩
  · intro z hz hle
    exact Finset.le_sup (f := fun z => (∑ a, z a) - ∑ a, y a)
      (s := D.filter (fun z => ∀ a, y a ≤ z a)) (mem_filter.2 ⟨hz, hle⟩)

/-- A non-maximal `y ∈ D` has `ht(y) ≥ 1`. -/
theorem one_le_ht {y : Fin 3 → ℕ} (hy : y ∈ D) (hmax : y ∉ maxSet D) : 1 ≤ ht D y := by
  have hnot : ¬ IsMaxCell D y := fun h => hmax (mem_filter.2 ⟨hy, h⟩)
  simp only [IsMaxCell, not_forall, not_not] at hnot
  obtain ⟨a, ha⟩ := hnot
  have hle : ∀ b, y b ≤ (y + Pi.single a 1 : Fin 3 → ℕ) b := fun b => by simp
  have hsum : ∑ b, (y + Pi.single a 1 : Fin 3 → ℕ) b = (∑ b, y b) + 1 := by
    simp only [Pi.add_apply, sum_add_distrib, sum_pi_single', mem_univ, if_true]
  have := Finset.le_sup (f := fun z => (∑ b, z b) - ∑ b, y b)
    (s := D.filter (fun z => ∀ b, y b ≤ z b)) (mem_filter.2 ⟨ha, hle⟩)
  simp only [hsum] at this
  unfold ht
  omega

/-- `ht(y) = 0` for `y ∈ Max` (cross-check of the definition; not needed for CHT). -/
theorem ht_eq_zero_of_mem_maxSet {y : Fin 3 → ℕ} (hy : y ∈ maxSet D) (hD : IsDownSetFin D) :
    ht D y = 0 := by
  have hmax := (mem_filter.1 hy).2
  refine le_antisymm (Finset.sup_le fun z hz => ?_) (Nat.zero_le _)
  have hz' := mem_filter.1 hz
  have hzy : z = y := by
    funext a
    by_contra hne
    have hlt : y a < z a := lt_of_le_of_ne (hz'.2 a) (Ne.symm hne)
    refine hmax a (hD z hz'.1 _ fun b => ?_)
    by_cases hb : b = a
    · subst hb; simp; omega
    · simp [Pi.single_eq_of_ne hb, hz'.2 b]
  simp [hzy]

/-- Pointwise form of CHT. -/
theorem cht_pointwise {x : Fin 3 → ℕ} (hx : x ∈ D) :
    2 ≤ hsum D x + 2 * (if x ∈ maxSet D then 1 else 0) + 2 * (if x ∈ triSet D then 1 else 0) +
      (if x ∈ qSet D then 1 else 0) := by
  by_cases hm : x ∈ maxSet D
  · simp only [hm, if_true]; omega
  by_cases ht3 : x ∈ triSet D
  · simp only [ht3, if_true]; omega
  by_cases hq : x ∈ qSet D
  · have := (mem_filter.1 hq).2.2
    simp only [hq, if_true]; omega
  simp only [hm, ht3, hq, if_false, mul_zero, add_zero]
  have hn3 : nTop D x ≠ 3 := fun h => ht3 (mem_filter.2 ⟨mem_sdiff.2 ⟨hx, hm⟩, h⟩)
  have hsplit := card_filter_add_card_filter_not (s := (univ : Finset (Fin 3)))
    (fun a => colTop D a x ∈ maxSet D)
  rw [card_univ, Fintype.card_fin] at hsplit
  have hN : (univ.filter (fun a : Fin 3 => colTop D a x ∉ maxSet D)).card ≤ hsum D x := by
    unfold hsum
    rw [← sum_filter_add_sum_filter_not univ (fun a => colTop D a x ∈ maxSet D)]
    calc (univ.filter (fun a : Fin 3 => colTop D a x ∉ maxSet D)).card
        = ∑ a ∈ univ.filter (fun a : Fin 3 => colTop D a x ∉ maxSet D), 1 := card_eq_sum_ones _
      _ ≤ ∑ a ∈ univ.filter (fun a : Fin 3 => colTop D a x ∉ maxSet D), ht D (colTop D a x) :=
          sum_le_sum fun a ha => one_le_ht (colTop_mem hx) (mem_filter.1 ha).2
      _ ≤ _ := Nat.le_add_left _ _
  have hn : nTop D x = (univ.filter (fun a : Fin 3 => colTop D a x ∈ maxSet D)).card := rfl
  by_cases h2 : nTop D x = 2
  · have h1 : hsum D x ≠ 1 := fun h => hq (mem_filter.2 ⟨hx, h2, h⟩)
    omega
  · omega

/-- **Lemma CHT (counting criterion).** For every finite `D ⊆ ℕ³` (no down-set hypothesis is
needed), with `m = |D|`, `H = Σ_{x∈D} h(x)`, `t = |Max|`:
`2m ≤ H + 2t + 2|Tri| + |Q'|`. -/
theorem cht (D : Finset (Fin 3 → ℕ)) :
    2 * D.card ≤ ∑ x ∈ D, hsum D x + 2 * (maxSet D).card + 2 * (triSet D).card +
      (qSet D).card := by
  have hsub : ∀ T : Finset (Fin 3 → ℕ), T ⊆ D → ∑ x ∈ D, (if x ∈ T then 1 else 0) = T.card := by
    intro T hT
    rw [sum_boole, Nat.cast_id, filter_mem_eq_inter, inter_eq_right.2 hT]
  have hM : maxSet D ⊆ D := filter_subset _ _
  have hT : triSet D ⊆ D := fun x hx => (mem_sdiff.1 (mem_filter.1 hx).1).1
  have hQ : qSet D ⊆ D := filter_subset _ _
  rw [← hsub _ hM, ← hsub _ hT, ← hsub _ hQ, mul_sum, mul_sum, ← sum_add_distrib,
    ← sum_add_distrib, ← sum_add_distrib, card_eq_sum_ones, mul_sum]
  exact sum_le_sum fun x hx => by simpa using cht_pointwise hx

end CHT

section TypeBound

/-- **Class 𝒞 (Loomis–Whitney sets)**, 0-based coordinates:
`D = {x : x 1 < h(x 0), x 2 < min(F(x 0), G(x 1))}` with `x 0 ∈ dom h = dom F = [0, L₁)`,
`dom G = [0, h 0)` (i.e. `h(0) = #dom G`), `h, F, G` nonincreasing and `≥ 1` on their domains,
`L₁ ≥ 1`, and `F(0) = G(0)`. Values of `h, F` outside `[0, L₁)` and of `G` outside `[0, h 0)` are
irrelevant. -/
structure LWClass (D : Finset (Fin 3 → ℕ)) (L₁ : ℕ) (h F G : ℕ → ℕ) : Prop where
  one_le : 1 ≤ L₁
  h_anti : ∀ i j, i ≤ j → j < L₁ → h j ≤ h i
  F_anti : ∀ i j, i ≤ j → j < L₁ → F j ≤ F i
  G_anti : ∀ i j, i ≤ j → j < h 0 → G j ≤ G i
  h_pos : ∀ i, i < L₁ → 1 ≤ h i
  F_pos : ∀ i, i < L₁ → 1 ≤ F i
  G_pos : ∀ j, j < h 0 → 1 ≤ G j
  F_zero : F 0 = G 0
  mem_iff : ∀ x, x ∈ D ↔ x 0 < L₁ ∧ x 1 < h (x 0) ∧ x 2 < min (F (x 0)) (G (x 1))

/-- `φ*(i, j)`: the height of the column of `D` over `(i, j)` (`0` off the base face). -/
def phiS (L₁ : ℕ) (h F G : ℕ → ℕ) (i j : ℕ) : ℕ :=
  if i < L₁ ∧ j < h i then min (F i) (G j) else 0

variable {D : Finset (Fin 3 → ℕ)} {L₁ : ℕ} {h F G : ℕ → ℕ}

theorem phiS_cases (i j : ℕ) :
    (i < L₁ ∧ j < h i ∧ phiS L₁ h F G i j = min (F i) (G j)) ∨
      (¬ (i < L₁ ∧ j < h i) ∧ phiS L₁ h F G i j = 0) := by
  unfold phiS
  split_ifs with hA
  · exact Or.inl ⟨hA.1, hA.2, rfl⟩
  · exact Or.inr ⟨hA, rfl⟩

/-- Membership in `faceCorners D c`, with the two directions `a ≠ c` listed. -/
theorem mem_faceCorners_iff {y : Fin 3 → ℕ} {c a b : Fin 3} (hab : a ≠ b) (hac : a ≠ c)
    (hbc : b ≠ c) :
    y ∈ faceCorners D c ↔ y ∈ D ∧ y c = 0 ∧ y + Pi.single a 1 ∉ D ∧ y + Pi.single b 1 ∉ D := by
  simp only [faceCorners, face, mem_filter]
  constructor
  · rintro ⟨⟨h1, h2⟩, h3⟩; exact ⟨h1, h2, h3 a hac, h3 b hbc⟩
  · rintro ⟨h1, h2, h3, h4⟩
    refine ⟨⟨h1, h2⟩, fun a' ha' => ?_⟩
    rcases fin3_cases hab hac hbc a' with rfl | rfl | rfl
    · exact h3
    · exact h4
    · exact absurd rfl ha'

theorem vec_add_e0 (i j k : ℕ) : (![i, j, k] : Fin 3 → ℕ) + Pi.single 0 1 = ![i + 1, j, k] := by
  funext t; fin_cases t <;> simp

theorem vec_add_e1 (i j k : ℕ) : (![i, j, k] : Fin 3 → ℕ) + Pi.single 1 1 = ![i, j + 1, k] := by
  funext t; fin_cases t <;> simp

theorem vec_add_e2 (i j k : ℕ) : (![i, j, k] : Fin 3 → ℕ) + Pi.single 2 1 = ![i, j, k + 1] := by
  funext t; fin_cases t <;> simp

theorem pos_phiS {i j : ℕ} (h0 : 0 < phiS L₁ h F G i j) : i < L₁ ∧ j < h i := by
  rcases phiS_cases (L₁ := L₁) (h := h) (F := F) (G := G) i j with ⟨h1, h2, -⟩ | ⟨-, h3⟩
  · exact ⟨h1, h2⟩
  · omega

theorem phiS_eq {i j : ℕ} (hi : i < L₁) (hj : j < h i) :
    phiS L₁ h F G i j = min (F i) (G j) := by
  unfold phiS; rw [if_pos ⟨hi, hj⟩]

/-- `r(x) = φ*(x₀ + 1, x₁)`: height of the column over the base cell right of `x`. -/
def rT (L₁ : ℕ) (h F G : ℕ → ℕ) (x : Fin 3 → ℕ) : ℕ := phiS L₁ h F G (x 0 + 1) (x 1)

/-- `u(x) = φ*(x₀, x₁ + 1)`: height of the column over the base cell above `x`. -/
def uT (L₁ : ℕ) (h F G : ℕ → ℕ) (x : Fin 3 → ℕ) : ℕ := phiS L₁ h F G (x 0) (x 1 + 1)

/-- The excluded corner of the face `A₁ = {x 1 = 0}`: the corner at the last column `L₁ − 1`. -/
def cornerF (L₁ : ℕ) (F : ℕ → ℕ) : Fin 3 → ℕ := ![L₁ - 1, 0, F (L₁ - 1) - 1]

/-- The excluded corner of the face `A₀ = {x 0 = 0}`: the corner at the last row `h 0 − 1`. -/
def cornerG (h G : ℕ → ℕ) : Fin 3 → ℕ := ![0, h 0 - 1, G (h 0 - 1) - 1]

namespace LWClass

variable (hC : LWClass D L₁ h F G)
include hC

theorem mem_iff' (x : Fin 3 → ℕ) : x ∈ D ↔ x 2 < phiS L₁ h F G (x 0) (x 1) := by
  rw [hC.mem_iff]
  rcases phiS_cases (L₁ := L₁) (h := h) (F := F) (G := G) (x 0) (x 1) with ⟨h1, h2, h3⟩ | ⟨h1, h3⟩
  · rw [h3]; tauto
  · rw [h3]; constructor
    · rintro ⟨a, b, -⟩; exact absurd ⟨a, b⟩ h1
    · intro h; omega

theorem mem_vec (i j k : ℕ) : (![i, j, k] : Fin 3 → ℕ) ∈ D ↔ k < phiS L₁ h F G i j := by
  rw [hC.mem_iff']; simp

theorem mem_e0 (x : Fin 3 → ℕ) :
    x + Pi.single 0 1 ∈ D ↔ x 2 < phiS L₁ h F G (x 0 + 1) (x 1) := by
  rw [hC.mem_iff']; simp

theorem mem_e1 (x : Fin 3 → ℕ) :
    x + Pi.single 1 1 ∈ D ↔ x 2 < phiS L₁ h F G (x 0) (x 1 + 1) := by
  rw [hC.mem_iff']; simp

theorem mem_e2 (x : Fin 3 → ℕ) :
    x + Pi.single 2 1 ∈ D ↔ x 2 + 1 < phiS L₁ h F G (x 0) (x 1) := by
  rw [hC.mem_iff']; simp

theorem mem_maxSet (x : Fin 3 → ℕ) :
    x ∈ maxSet D ↔ x 2 < phiS L₁ h F G (x 0) (x 1) ∧
      phiS L₁ h F G (x 0 + 1) (x 1) ≤ x 2 ∧ phiS L₁ h F G (x 0) (x 1 + 1) ≤ x 2 ∧
      phiS L₁ h F G (x 0) (x 1) ≤ x 2 + 1 := by
  simp only [maxSet, mem_filter, IsMaxCell]
  rw [hC.mem_iff']
  constructor
  · rintro ⟨h1, h2⟩
    have a0 := h2 0; have a1 := h2 1; have a2 := h2 2
    rw [hC.mem_e0] at a0; rw [hC.mem_e1] at a1; rw [hC.mem_e2] at a2
    omega
  · rintro ⟨h1, h2, h3, h4⟩
    refine ⟨h1, fun a => ?_⟩
    fin_cases a
    · show x + Pi.single 0 1 ∉ D; rw [hC.mem_e0]; omega
    · show x + Pi.single 1 1 ∉ D; rw [hC.mem_e1]; omega
    · show x + Pi.single 2 1 ∉ D; rw [hC.mem_e2]; omega

/-- `φ*` is antitone along the base face. -/
theorem phiS_anti {i j i' j' : ℕ} (hi : i ≤ i') (hj : j ≤ j') (hi' : i' < L₁) (hj' : j' < h i') :
    i < L₁ ∧ j < h i ∧ phiS L₁ h F G i' j' ≤ phiS L₁ h F G i j := by
  have h1 := hC.h_anti i i' hi hi'
  have h2 := hC.F_anti i i' hi hi'
  have h3 := hC.h_anti 0 i' (Nat.zero_le _) hi'
  have h4 := hC.G_anti j j' hj (by omega)
  have hA : i < L₁ ∧ j < h i := ⟨by omega, by omega⟩
  refine ⟨hA.1, hA.2, ?_⟩
  unfold phiS
  rw [if_pos ⟨hi', hj'⟩, if_pos hA]
  omega

/-- On the base face `φ* ≥ 1`. -/
theorem phiS_pos {i j : ℕ} (hi : i < L₁) (hj : j < h i) : 1 ≤ phiS L₁ h F G i j := by
  have h3 := hC.h_anti 0 i (Nat.zero_le _) hi
  have := hC.F_pos i hi
  have := hC.G_pos j (by omega)
  unfold phiS
  rw [if_pos ⟨hi, hj⟩]
  omega

/-- Maximal cells are determined by their first two coordinates. -/
theorem max_ext {x x' : Fin 3 → ℕ} (hx : x ∈ maxSet D) (hx' : x' ∈ maxSet D) (h0 : x 0 = x' 0)
    (h1 : x 1 = x' 1) : x = x' := by
  rw [hC.mem_maxSet] at hx hx'
  rw [h0, h1] at hx
  have h2 : x 2 = x' 2 := by omega
  funext t; fin_cases t
  · exact h0
  · exact h1
  · exact h2

theorem cornerF_mem : cornerF L₁ F ∈ faceCorners D 1 := by
  have hL := hC.one_le
  have hi : L₁ - 1 < L₁ := by omega
  have h1 := hC.h_pos _ hi
  have h2 := hC.F_pos _ hi
  have h3 := hC.F_anti 0 (L₁ - 1) (Nat.zero_le _) hi
  have h4 := hC.F_zero
  rw [mem_faceCorners_iff (a := 0) (b := 2) (by decide) (by decide) (by decide)]
  unfold cornerF
  refine ⟨?_, by simp, ?_, ?_⟩
  · rw [hC.mem_vec, phiS_eq hi (show 0 < h (L₁ - 1) by omega)]; omega
  · rw [vec_add_e0, hC.mem_vec, show L₁ - 1 + 1 = L₁ by omega]
    unfold phiS; rw [if_neg (by omega)]; omega
  · rw [vec_add_e2, hC.mem_vec, phiS_eq hi (show 0 < h (L₁ - 1) by omega)]; omega

theorem cornerG_mem : cornerG h G ∈ faceCorners D 0 := by
  have hL := hC.one_le
  have h1 := hC.h_pos 0 (by omega)
  have hj : h 0 - 1 < h 0 := by omega
  have h2 := hC.G_pos _ hj
  have h3 := hC.G_anti 0 (h 0 - 1) (Nat.zero_le _) hj
  have h4 := hC.F_zero
  rw [mem_faceCorners_iff (a := 1) (b := 2) (by decide) (by decide) (by decide)]
  unfold cornerG
  refine ⟨?_, by simp, ?_, ?_⟩
  · rw [hC.mem_vec, phiS_eq (show 0 < L₁ by omega) hj]; omega
  · rw [vec_add_e1, hC.mem_vec, show h 0 - 1 + 1 = h 0 by omega]
    unfold phiS; rw [if_neg (by omega)]; omega
  · rw [vec_add_e2, hC.mem_vec, phiS_eq (show 0 < L₁ by omega) hj]; omega

/-- Branch A: `r(x) = u(x) = 0`, so `(x₀, x₁, 0)` is a corner of the base face `A₂`. -/
theorem mapA_mem {x : Fin 3 → ℕ} (hx : x ∈ maxSet D) (hr : rT L₁ h F G x = 0)
    (hu : uT L₁ h F G x = 0) : (![x 0, x 1, 0] : Fin 3 → ℕ) ∈ faceCorners D 2 := by
  rw [hC.mem_maxSet] at hx
  unfold rT at hr; unfold uT at hu
  rw [mem_faceCorners_iff (a := 0) (b := 1) (by decide) (by decide) (by decide)]
  refine ⟨?_, by simp, ?_, ?_⟩
  · rw [hC.mem_vec]; omega
  · rw [vec_add_e0, hC.mem_vec]; omega
  · rw [vec_add_e1, hC.mem_vec]; omega

/-- Branch F: `r(x) ≠ 0`; then `F` drops at `x₀` and `(x₀, 0, F(x₀) − 1)` is a corner of the face
`A₁` other than `cornerF`. -/
theorem mapF_mem {x : Fin 3 → ℕ} (hx : x ∈ maxSet D) (hr : rT L₁ h F G x ≠ 0) :
    (![x 0, 0, F (x 0) - 1] : Fin 3 → ℕ) ∈ (faceCorners D 1).erase (cornerF L₁ F) := by
  rw [hC.mem_maxSet] at hx
  unfold rT at hr
  obtain ⟨hi1, hj1⟩ := pos_phiS (Nat.pos_of_ne_zero hr)
  obtain ⟨hi, hj⟩ := pos_phiS (show 0 < phiS L₁ h F G (x 0) (x 1) by omega)
  rw [phiS_eq hi1 hj1, phiS_eq hi hj] at hx
  have hFd : F (x 0 + 1) < F (x 0) := by omega
  have hh0 := hC.h_pos _ hi
  have hh1 := hC.h_pos _ hi1
  have hF0 := hC.F_pos _ hi
  have hFa := hC.F_anti 0 (x 0) (Nat.zero_le _) hi
  have hz := hC.F_zero
  rw [mem_erase, mem_faceCorners_iff (a := 0) (b := 2) (by decide) (by decide) (by decide)]
  refine ⟨fun heq => ?_, ?_, by simp, ?_, ?_⟩
  · have := congrFun heq 0
    simp [cornerF] at this
    omega
  · rw [hC.mem_vec, phiS_eq hi (show 0 < h (x 0) by omega)]; omega
  · rw [vec_add_e0, hC.mem_vec, phiS_eq hi1 (show 0 < h (x 0 + 1) by omega)]; omega
  · rw [vec_add_e2, hC.mem_vec, phiS_eq hi (show 0 < h (x 0) by omega)]; omega

/-- Branch G: `r(x) < u(x)`; then `G` drops at `x₁` and `(0, x₁, G(x₁) − 1)` is a corner of the face
`A₀` other than `cornerG`. -/
theorem mapG_mem {x : Fin 3 → ℕ} (hx : x ∈ maxSet D) (hru : rT L₁ h F G x < uT L₁ h F G x) :
    (![0, x 1, G (x 1) - 1] : Fin 3 → ℕ) ∈ (faceCorners D 0).erase (cornerG h G) := by
  rw [hC.mem_maxSet] at hx
  unfold rT uT at hru
  obtain ⟨hi1, hj1⟩ := pos_phiS (show 0 < phiS L₁ h F G (x 0) (x 1 + 1) by omega)
  obtain ⟨hi, hj⟩ := pos_phiS (show 0 < phiS L₁ h F G (x 0) (x 1) by omega)
  have hu := hx.2.2.1
  rw [phiS_eq hi1 hj1] at hu
  rw [phiS_eq hi hj] at hx
  have hGd : G (x 1 + 1) < G (x 1) := by omega
  have hL := hC.one_le
  have hha := hC.h_anti 0 (x 0) (Nat.zero_le _) hi
  have hG0 := hC.G_pos (x 1) (by omega)
  have hGa := hC.G_anti 0 (x 1) (Nat.zero_le _) (by omega)
  have hz := hC.F_zero
  rw [mem_erase, mem_faceCorners_iff (a := 1) (b := 2) (by decide) (by decide) (by decide)]
  refine ⟨fun heq => ?_, ?_, by simp, ?_, ?_⟩
  · have := congrFun heq 1
    simp [cornerG] at this
    omega
  · rw [hC.mem_vec, phiS_eq (show 0 < L₁ by omega) (show x 1 < h 0 by omega)]; omega
  · rw [vec_add_e1, hC.mem_vec]
    rcases phiS_cases (L₁ := L₁) (h := h) (F := F) (G := G) 0 (x 1 + 1) with
      ⟨-, -, h3⟩ | ⟨-, h3⟩ <;> rw [h3] <;> omega
  · rw [vec_add_e2, hC.mem_vec, phiS_eq (show 0 < L₁ by omega) (show x 1 < h 0 by omega)]
    omega

/-- Injectivity in branch F: two branch-F maximal cells with the same `x₀` have the same `x₁`. -/
theorem branchF_aux {x x' : Fin 3 → ℕ} (hx : x ∈ maxSet D) (hx' : x' ∈ maxSet D)
    (hr : rT L₁ h F G x ≠ 0) (hr' : rT L₁ h F G x' ≠ 0) (hur : uT L₁ h F G x ≤ rT L₁ h F G x)
    (h0 : x 0 = x' 0) : ¬ x 1 < x' 1 := by
  intro hlt
  rw [hC.mem_maxSet] at hx hx'
  unfold rT at hr hr'; unfold rT uT at hur
  obtain ⟨hi1, hj1⟩ := pos_phiS (Nat.pos_of_ne_zero hr)
  obtain ⟨hi1', hj1'⟩ := pos_phiS (Nat.pos_of_ne_zero hr')
  obtain ⟨hi, hj⟩ := pos_phiS (show 0 < phiS L₁ h F G (x 0) (x 1) by omega)
  obtain ⟨hi', hj'⟩ := pos_phiS (show 0 < phiS L₁ h F G (x' 0) (x' 1) by omega)
  rw [← h0] at hi1' hj1' hi' hj' hx'
  -- `u(x) ≥ φ*(x₀, x'₁)` since `(x₀, x₁ + 1) ≤ (x₀, x'₁)`
  obtain ⟨-, -, hmono⟩ := hC.phiS_anti (le_refl (x 0)) (show x 1 + 1 ≤ x' 1 by omega) hi' hj'
  rw [phiS_eq hi1 hj1, phiS_eq hi hj] at hx
  rw [phiS_eq hi1' hj1', phiS_eq hi' hj'] at hx'
  rw [phiS_eq hi1 hj1] at hur
  rw [phiS_eq hi' hj'] at hmono
  omega

/-- Injectivity in branch G: two branch-G maximal cells with the same `x₁` have the same `x₀`. -/
theorem branchG_aux {x x' : Fin 3 → ℕ} (hx : x ∈ maxSet D) (hx' : x' ∈ maxSet D)
    (hru : rT L₁ h F G x < uT L₁ h F G x) (hru' : rT L₁ h F G x' < uT L₁ h F G x')
    (h1 : x 1 = x' 1) : ¬ x 0 < x' 0 := by
  intro hlt
  rw [hC.mem_maxSet] at hx hx'
  unfold rT uT at hru hru'
  obtain ⟨hi1, hj1⟩ := pos_phiS (show 0 < phiS L₁ h F G (x 0) (x 1 + 1) by omega)
  obtain ⟨hi1', hj1'⟩ := pos_phiS (show 0 < phiS L₁ h F G (x' 0) (x' 1 + 1) by omega)
  obtain ⟨hi, hj⟩ := pos_phiS (show 0 < phiS L₁ h F G (x 0) (x 1) by omega)
  obtain ⟨hi', hj'⟩ := pos_phiS (show 0 < phiS L₁ h F G (x' 0) (x' 1) by omega)
  rw [← h1] at hj1' hj' hx' hru'
  -- `r(x) ≥ φ*(x'₀, x₁)` since `(x₀ + 1, x₁) ≤ (x'₀, x₁)`
  obtain ⟨hA1, hA2, hmono⟩ := hC.phiS_anti (show x 0 + 1 ≤ x' 0 by omega) (le_refl (x 1)) hi' hj'
  rw [phiS_eq hi1 hj1, phiS_eq hi hj] at hx
  rw [phiS_eq hi1' hj1', phiS_eq hi' hj'] at hx'
  rw [phiS_eq hi1 hj1, phiS_eq hA1 hA2] at hru
  rw [phiS_eq hA1 hA2, phiS_eq hi' hj'] at hmono
  omega

end LWClass

/-- **Lemma T (type bound) for the Loomis–Whitney class 𝒞.** If `D` is in class 𝒞 then
`t ≤ C − 2`, i.e. `|Max D| + 2 ≤ k₀ + k₁ + k₂` with `k_c = |faceCorners D c|` (as in Lemma B).

Proof (an explicit injection; equivalent to the "birth level" form of the paper's telescoping
argument). For a maximal `x` put `r = φ*(x₀ + 1, x₁)`, `u = φ*(x₀, x₁ + 1)`.
* `r = u = 0`: `x ↦ (x₀, x₁, 0)`, a corner of the base face `A₂`;
* `u ≤ r ≠ 0`: `x ↦ (x₀, 0, F(x₀) − 1)`, a corner of `A₁` (`F` drops at `x₀`), never the corner
  at the last column; injective since for fixed `x₀` a second cell higher in the column would give
  `u(x) > r(x)`;
* `r < u`: `x ↦ (0, x₁, G(x₁) − 1)`, a corner of `A₀` (`G` drops at `x₁`), never the corner at the
  last row; injective symmetrically. -/
theorem typeBound (hC : LWClass D L₁ h F G) :
    (maxSet D).card + 2 ≤ ∑ c, (faceCorners D c).card := by
  have hs1 := card_filter_add_card_filter_not (s := maxSet D)
    (fun x => rT L₁ h F G x < uT L₁ h F G x)
  have hs2 := card_filter_add_card_filter_not
    (s := (maxSet D).filter (fun x => ¬ rT L₁ h F G x < uT L₁ h F G x))
    (fun x => rT L₁ h F G x = 0)
  have hG : ((maxSet D).filter (fun x => rT L₁ h F G x < uT L₁ h F G x)).card ≤
      ((faceCorners D 0).erase (cornerG h G)).card := by
    refine card_le_card_of_injOn (fun x => ![0, x 1, G (x 1) - 1]) ?_ ?_
    · intro x hx
      have hx' := mem_filter.1 hx
      exact hC.mapG_mem hx'.1 hx'.2
    · intro x hx x' hx' heq
      have hx1 := mem_filter.1 hx
      have hx2 := mem_filter.1 hx'
      have e1 : x 1 = x' 1 := by
        have := congrFun heq 1; simpa using this
      have e0 : x 0 = x' 0 := by
        rcases lt_trichotomy (x 0) (x' 0) with hlt | heq' | hgt
        · exact absurd hlt (hC.branchG_aux hx1.1 hx2.1 hx1.2 hx2.2 e1)
        · exact heq'
        · exact absurd hgt (hC.branchG_aux hx2.1 hx1.1 hx2.2 hx1.2 e1.symm)
      exact hC.max_ext hx1.1 hx2.1 e0 e1
  have hA : (((maxSet D).filter (fun x => ¬ rT L₁ h F G x < uT L₁ h F G x)).filter
      (fun x => rT L₁ h F G x = 0)).card ≤ (faceCorners D 2).card := by
    refine card_le_card_of_injOn (fun x => ![x 0, x 1, 0]) ?_ ?_
    · intro x hx
      have hx' := mem_filter.1 hx
      have hx'' := mem_filter.1 hx'.1
      exact hC.mapA_mem hx''.1 hx'.2 (by omega)
    · intro x hx x' hx' heq
      have hx1 := mem_filter.1 (mem_filter.1 hx).1
      have hx2 := mem_filter.1 (mem_filter.1 hx').1
      have e0 : x 0 = x' 0 := by
        have := congrFun heq 0; simpa using this
      have e1 : x 1 = x' 1 := by
        have := congrFun heq 1; simpa using this
      exact hC.max_ext hx1.1 hx2.1 e0 e1
  have hF : (((maxSet D).filter (fun x => ¬ rT L₁ h F G x < uT L₁ h F G x)).filter
      (fun x => ¬ rT L₁ h F G x = 0)).card ≤ ((faceCorners D 1).erase (cornerF L₁ F)).card := by
    refine card_le_card_of_injOn (fun x => ![x 0, 0, F (x 0) - 1]) ?_ ?_
    · intro x hx
      have hx' := mem_filter.1 hx
      have hx'' := mem_filter.1 hx'.1
      exact hC.mapF_mem hx''.1 hx'.2
    · intro x hx x' hx' heq
      have hy1 := mem_filter.1 hx
      have hy2 := mem_filter.1 hx'
      have hx1 := mem_filter.1 hy1.1
      have hx2 := mem_filter.1 hy2.1
      have e0 : x 0 = x' 0 := by
        have := congrFun heq 0; simpa using this
      have e1 : x 1 = x' 1 := by
        rcases lt_trichotomy (x 1) (x' 1) with hlt | heq' | hgt
        · exact absurd hlt (hC.branchF_aux hx1.1 hx2.1 hy1.2 hy2.2 (by omega) e0)
        · exact heq'
        · exact absurd hgt (hC.branchF_aux hx2.1 hx1.1 hy2.2 hy1.2 (by omega) e0.symm)
      exact hC.max_ext hx1.1 hx2.1 e0 e1
  rw [card_erase_of_mem hC.cornerF_mem] at hF
  rw [card_erase_of_mem hC.cornerG_mem] at hG
  have h1 : 1 ≤ (faceCorners D 1).card := card_pos.2 ⟨_, hC.cornerF_mem⟩
  have h0 : 1 ≤ (faceCorners D 0).card := card_pos.2 ⟨_, hC.cornerG_mem⟩
  rw [Fin.sum_univ_three]
  omega

/-- Non-vacuity of the class: `D = {0}` (`L₁ = 1`, `h = F = G = 1`) is in 𝒞; there `t = 1`,
`C = 3`, so Lemma T is an equality (tight for boxes). -/
example : LWClass ({0} : Finset (Fin 3 → ℕ)) 1 (fun _ => 1) (fun _ => 1) (fun _ => 1) where
  one_le := le_rfl
  h_anti _ _ _ _ := le_rfl
  F_anti _ _ _ _ := le_rfl
  G_anti _ _ _ _ := le_rfl
  h_pos _ _ := le_rfl
  F_pos _ _ := le_rfl
  G_pos _ _ := le_rfl
  F_zero := rfl
  mem_iff x := by
    simp only [Finset.mem_singleton]
    constructor
    · rintro rfl; simp
    · rintro ⟨h0, h1, h2⟩
      funext i; fin_cases i <;> simp <;> omega

end TypeBound

end CornerArea

end NumericalSemigroup
