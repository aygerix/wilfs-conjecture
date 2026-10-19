import Wilf.Basic
import Mathlib.Combinatorics.Additive.CauchyDavenport

/-!
# LAYER-KNESER: gap residues shrink across bands of length `m`

Fix any `m ∈ S`, `m > 0` (for example the multiplicity). For `H ≥ 0`, `bandGaps m H` is the set of
residues `r < m` with `H m + r ∉ S`, and `k = #lowRes m` is the number of elements of `S` in `(m, 2m)`.

* `bandGaps m (H+1) ⊆ bandGaps m H`, `#bandGaps m 0 ≤ m - 1`, `#bandGaps m 1 + k + 1 = m`.
* Shift inclusion: `r ∈ bandGaps m (H+2)`, `b ∈ {0} ∪ lowRes m` ⇒ `(r + m - b) % m ∈ bandGaps m H`.
* For prime `m`, Cauchy–Davenport turns the shift inclusion into
  `#bandGaps m (H+2) + k ≤ #bandGaps m H` (when `bandGaps m (H+2)` is nonempty).
* Counting: if `q m < c ≤ (q+1) m` (so `D = q + 1 = ⌈c/m⌉`) and `q ≥ 1`, then
  `ℓ ≥ q + 1 + (q-1) k` always, and, for prime `m`,
  `ℓ ≥ q + 1 + (q-1) k + k · ∑_{j < q-1} ⌊j/2⌋`.
  (`∑_{j<n} ⌊j/2⌋ = ⌊(n-1)²/4⌋`, giving `ℓ ≥ D + (D-2)k + k⌊(D-3)²/4⌋`.)
* Consequently Wilf holds whenever `c ≤ e · (that bound)`.
* Last band (Yang–Zhang staircase, Preprints.org 202604.0551, Prop 3.1), for any `m ∈ S`:
  `ℓ ≥ D + (D-2) k + η_ρ` with `η_ρ = #{r ∈ lowRes : r < c - q m}` (`ell_ge_staircase`); combined with the
  Cauchy–Davenport growth for prime `m` (`ell_ge_lkyz_prime`, `ell_ge_lkyz_prime'`).

The general-modulus version with `⌈(k+1)/2⌉` uses Kneser's theorem, which is not in Mathlib;
it is proved on paper (PROOFS "Theorem LAYER-KNESER").
-/

namespace NumericalSemigroup

open Finset
open scoped Pointwise Classical

variable (S : NumericalSemigroup)

/-- Gap residues of the band `[H m, (H+1) m)`. -/
noncomputable def bandGaps (m H : ℕ) : Finset ℕ :=
  (range m).filter (fun r => H * m + r ∉ S)

/-- Residues `0 < r < m` with `m + r ∈ S`: the elements of `S ∩ (m, 2m)`, shifted by `m`. -/
noncomputable def lowRes (m : ℕ) : Finset ℕ :=
  (range m).filter (fun r => 0 < r ∧ m + r ∈ S)

variable {S} {m : ℕ}

theorem mul_mem_of_mem (hmS : m ∈ S) (H : ℕ) : H * m ∈ S := by
  have := nsmul_mem hmS H
  simpa [smul_eq_mul] using this

theorem bandGaps_succ_subset (hmS : m ∈ S) (H : ℕ) :
    S.bandGaps m (H + 1) ⊆ S.bandGaps m H := by
  intro r hr
  simp only [bandGaps, mem_filter, mem_range] at hr ⊢
  refine ⟨hr.1, fun h => hr.2 ?_⟩
  have := add_mem h hmS
  have e : (H + 1) * m + r = H * m + r + m := by ring
  rw [e]; exact this

theorem bandGaps_antitone (hmS : m ∈ S) {H H' : ℕ} (h : H ≤ H') :
    S.bandGaps m H' ⊆ S.bandGaps m H := by
  induction h with
  | refl => exact Subset.refl _
  | step _ ih => exact (bandGaps_succ_subset hmS _).trans ih

theorem zero_not_mem_bandGaps (hmS : m ∈ S) (H : ℕ) : 0 ∉ S.bandGaps m H := by
  intro h
  exact (mem_filter.1 h).2 (by simpa using mul_mem_of_mem hmS H)

theorem bandGaps_subset_erase (hmS : m ∈ S) (H : ℕ) :
    S.bandGaps m H ⊆ (range m).erase 0 := fun _ hr =>
  mem_erase.2 ⟨fun h => zero_not_mem_bandGaps hmS H (h ▸ hr), (mem_filter.1 hr).1⟩

theorem card_bandGaps_le (hmS : m ∈ S) (hm : 0 < m) (H : ℕ) : #(S.bandGaps m H) ≤ m - 1 := by
  have h := card_le_card (bandGaps_subset_erase hmS H)
  rwa [card_erase_of_mem (mem_range.2 hm), card_range] at h

theorem zero_not_mem_lowRes : 0 ∉ S.lowRes m := by
  simp [lowRes]

theorem insert_lowRes_subset (hm : 0 < m) : insert 0 (S.lowRes m) ⊆ range m := by
  intro r hr
  rw [mem_insert] at hr
  rcases hr with rfl | hr
  · exact mem_range.2 hm
  · exact (mem_filter.1 hr).1

theorem card_bandGaps_one (hmS : m ∈ S) (hm : 0 < m) :
    #(S.bandGaps m 1) + #(S.lowRes m) + 1 = m := by
  have hsplit : S.bandGaps m 1 = range m \ insert 0 (S.lowRes m) := by
    ext r
    simp only [bandGaps, lowRes, mem_filter, mem_range, one_mul, mem_sdiff, mem_insert]
    constructor
    · rintro ⟨h1, h2⟩
      refine ⟨h1, ?_⟩
      rintro (rfl | ⟨_, _, h⟩)
      · exact h2 (by simpa using hmS)
      · exact h2 h
    · rintro ⟨h1, h2⟩
      refine ⟨h1, fun h => h2 ?_⟩
      rcases Nat.eq_zero_or_pos r with rfl | hr
      · exact Or.inl rfl
      · exact Or.inr ⟨h1, hr, h⟩
  have hsub := insert_lowRes_subset (S := S) hm
  have h1 := card_sdiff_of_subset hsub
  have h2 := card_le_card hsub
  rw [card_insert_of_notMem zero_not_mem_lowRes, card_range] at h1 h2
  rw [hsplit, h1]
  omega

/-- **Shift inclusion.** `G_{H+2} - B ⊆ G_H` (mod `m`), with `B = {0} ∪ lowRes`. -/
theorem shift_mem (hmS : m ∈ S) (hm : 0 < m) (H r b : ℕ) (hr : r ∈ S.bandGaps m (H + 2))
    (hb : b ∈ insert 0 (S.lowRes m)) :
    (r + m - b) % m ∈ S.bandGaps m H := by
  have hbm : b < m := mem_range.1 (insert_lowRes_subset hm hb)
  have hgen : m + b ∈ S := by
    rcases mem_insert.1 hb with rfl | h
    · simpa using hmS
    · exact (mem_filter.1 h).2.2
  simp only [bandGaps, mem_filter, mem_range] at hr ⊢
  refine ⟨Nat.mod_lt _ hm, fun hmem => hr.2 ?_⟩
  have e2 : (H + 2) * m = H * m + m + m := by ring
  by_cases hrb : b ≤ r
  · have he : (r + m - b) % m = r - b := by
      rw [show r + m - b = (r - b) + m by omega, Nat.add_mod_right, Nat.mod_eq_of_lt (by omega)]
    rw [he] at hmem
    have := add_mem (add_mem hmem hgen) hmS
    have e : (H + 2) * m + r = H * m + (r - b) + (m + b) + m := by rw [e2]; omega
    rw [e]; exact this
  · have he : (r + m - b) % m = r + m - b := Nat.mod_eq_of_lt (by omega)
    rw [he] at hmem
    have := add_mem hmem hgen
    have e : (H + 2) * m + r = H * m + (r + m - b) + (m + b) := by rw [e2]; omega
    rw [e]; exact this

/-- **Cauchy–Davenport step** (prime `m`): `#G_{H+2} + k ≤ #G_H` when `G_{H+2} ≠ ∅`. -/
theorem card_bandGaps_step (hp : m.Prime) (hmS : m ∈ S) (H : ℕ)
    (hne : (S.bandGaps m (H + 2)).Nonempty) :
    #(S.bandGaps m (H + 2)) + #(S.lowRes m) ≤ #(S.bandGaps m H) := by
  have hm := hp.pos
  have hinj : Set.InjOn (Nat.cast : ℕ → ZMod m) (range m : Set ℕ) := by
    intro a ha b hb hab
    simp only [coe_range, Set.mem_Iio] at ha hb
    have := (ZMod.natCast_eq_natCast_iff' a b m).1 hab
    rwa [Nat.mod_eq_of_lt ha, Nat.mod_eq_of_lt hb] at this
  have hBsub := insert_lowRes_subset (S := S) hm
  have hXc : #((S.bandGaps m (H + 2)).image (Nat.cast : ℕ → ZMod m)) =
      #(S.bandGaps m (H + 2)) :=
    card_image_of_injOn (hinj.mono (by
      intro r hr; exact mem_coe.2 (mem_filter.1 (mem_coe.1 hr)).1))
  have hYc : #((insert 0 (S.lowRes m)).image (fun b : ℕ => -(b : ZMod m))) =
      #(S.lowRes m) + 1 := by
    rw [card_image_of_injOn, card_insert_of_notMem zero_not_mem_lowRes]
    intro a ha b hb hab
    exact hinj (hBsub (mem_coe.1 ha)) (hBsub (mem_coe.1 hb)) (neg_inj.1 hab)
  have hsub : (S.bandGaps m (H + 2)).image (Nat.cast : ℕ → ZMod m) +
      (insert 0 (S.lowRes m)).image (fun b : ℕ => -(b : ZMod m)) ⊆
      (S.bandGaps m H).image Nat.cast := by
    intro z hz
    obtain ⟨x, hx, y, hy, rfl⟩ := mem_add.1 hz
    obtain ⟨r, hr, rfl⟩ := mem_image.1 hx
    obtain ⟨b, hb, rfl⟩ := mem_image.1 hy
    refine mem_image.2 ⟨(r + m - b) % m, shift_mem hmS hm H r b hr hb, ?_⟩
    have hbm : b ≤ r + m := by
      have := mem_range.1 (hBsub hb); omega
    rw [ZMod.natCast_mod, Nat.cast_sub hbm, Nat.cast_add, ZMod.natCast_self]
    ring
  have hcd := ZMod.cauchy_davenport hp (hne.image (Nat.cast : ℕ → ZMod m))
    ((insert_nonempty 0 (S.lowRes m)).image (fun b : ℕ => -(b : ZMod m)))
  have hle := (card_le_card hsub).trans card_image_le
  have hlt := card_bandGaps_le hmS hm H
  rw [hXc, hYc] at hcd
  omega

/-- The Frobenius residue lies in band `q` when `q m < c ≤ (q+1) m`. -/
theorem bandGaps_last_nonempty {q : ℕ} (hqc : q * m < S.conductor)
    (hcq : S.conductor ≤ (q + 1) * m) :
    (S.bandGaps m q).Nonempty := by
  refine ⟨S.conductor - 1 - q * m, ?_⟩
  simp only [bandGaps, mem_filter, mem_range]
  have e : (q + 1) * m = q * m + m := by ring
  refine ⟨by omega, ?_⟩
  have : q * m + (S.conductor - 1 - q * m) = S.conductor - 1 := by omega
  rw [this]
  exact S.conductor_sub_one_not_mem (by omega)

/-- Gaps are covered by the bands `0, …, q-1` and the interval `(q m, c)`. -/
theorem genus_le_bands (hmS : m ∈ S) (hm : 0 < m) {q : ℕ} :
    S.genus ≤ (∑ H ∈ range q, #(S.bandGaps m H)) + (S.conductor - q * m - 1) := by
  have hcov : S.gaps ⊆ ((range q).biUnion fun H => (S.bandGaps m H).image (fun r => H * m + r)) ∪
      Ioo (q * m) S.conductor := by
    intro n hn
    rw [mem_gaps] at hn
    have hnc := S.lt_conductor_of_not_mem hn
    rw [mem_union]
    by_cases hq : n / m < q
    · left
      rw [mem_biUnion]
      refine ⟨n / m, mem_range.2 hq, mem_image.2 ⟨n % m, ?_, ?_⟩⟩
      · simp only [bandGaps, mem_filter, mem_range]
        refine ⟨Nat.mod_lt _ hm, ?_⟩
        rw [mul_comm, Nat.div_add_mod]; exact hn
      · rw [mul_comm, Nat.div_add_mod]
    · right
      rw [mem_Ioo]
      refine ⟨?_, hnc⟩
      have h1 : q * m ≤ n := by
        have := Nat.div_mul_le_self n m
        have h2 : q * m ≤ n / m * m := Nat.mul_le_mul_right m (by omega)
        omega
      rcases Nat.eq_or_lt_of_le h1 with h | h
      · exact absurd (h ▸ mul_mem_of_mem hmS q) hn
      · exact h
  calc S.genus = #S.gaps := rfl
    _ ≤ #(((range q).biUnion fun H => (S.bandGaps m H).image (fun r => H * m + r)) ∪
          Ioo (q * m) S.conductor) := card_le_card hcov
    _ ≤ #((range q).biUnion fun H => (S.bandGaps m H).image (fun r => H * m + r)) +
          #(Ioo (q * m) S.conductor) := card_union_le _ _
    _ ≤ (∑ H ∈ range q, #(S.bandGaps m H)) + (S.conductor - q * m - 1) := by
        gcongr
        · exact card_biUnion_le.trans (sum_le_sum fun H _ => card_image_le)
        · exact (Nat.card_Ioo _ _).le

/-- **Abstract counting.** If every band `1 ≤ H ≤ q-1` satisfies
`#G_H + k + δ·⌊(H-1)/2⌋ ≤ m - 1`, then `ℓ ≥ q + 1 + (q-1) k + δ ∑_{j<q-1} ⌊j/2⌋`. -/
theorem ell_ge_of_band_bounds (hmS : m ∈ S) (hm : 0 < m) {q k δ : ℕ} (hq : 1 ≤ q)
    (hqc : q * m < S.conductor)
    (hb : ∀ H, 1 ≤ H → H ≤ q - 1 → #(S.bandGaps m H) + k + δ * ((H - 1) / 2) ≤ m - 1) :
    q + 1 + (q - 1) * k + δ * ∑ j ∈ range (q - 1), j / 2 ≤ S.ell := by
  have hg := genus_le_bands (S := S) (q := q) hmS hm
  have hell := S.ell_add_genus
  have h0 := card_bandGaps_le (S := S) hmS hm 0
  obtain ⟨q', rfl⟩ : ∃ q', q = q' + 1 := ⟨q - 1, by omega⟩
  simp only [Nat.add_sub_cancel] at hb ⊢
  rw [sum_range_succ'] at hg
  have hsum : (∑ i ∈ range q', #(S.bandGaps m (i + 1))) + q' * k +
      δ * ∑ j ∈ range q', j / 2 ≤ q' * (m - 1) := by
    have := sum_le_sum (s := range q') (fun i hi =>
      hb (i + 1) (by omega) (by have := mem_range.1 hi; omega))
    simp only [Nat.add_sub_cancel, sum_add_distrib, sum_const, card_range, smul_eq_mul,
      ← mul_sum] at this
    linarith
  have hmm : (q' + 1) * m = q' * (m - 1) + (m - 1) + q' + 1 := by
    obtain ⟨m', rfl⟩ : ∃ m', m = m' + 1 := ⟨m - 1, by omega⟩
    simp only [Nat.add_sub_cancel]; ring
  omega

/-- **Part (a)** (any `m ∈ S`): `ℓ ≥ D + (D-2) k` with `D = q + 1`. For `m` the multiplicity this
contains the count behind Delgado–Kumar–Marion's Theorem 1.5. -/
theorem ell_ge_layer_basic (hmS : m ∈ S) (hm : 0 < m) {q : ℕ} (hq : 1 ≤ q)
    (hqc : q * m < S.conductor) :
    q + 1 + (q - 1) * #(S.lowRes m) ≤ S.ell := by
  have := ell_ge_of_band_bounds (δ := 0) (k := #(S.lowRes m)) hmS hm hq hqc
    (fun H h1 _ => by
      have h := card_le_card (bandGaps_antitone (S := S) hmS h1)
      have h' := card_bandGaps_one hmS hm
      simp only [zero_mul, add_zero]
      omega)
  simpa using this

/-- **Band bound** (prime `m`): `#G_H + k + k·⌊(H-1)/2⌋ ≤ m - 1` for `1 ≤ H ≤ q`. -/
theorem band_bound_prime (hp : m.Prime) (hmS : m ∈ S) {q : ℕ}
    (hqc : q * m < S.conductor) (hcq : S.conductor ≤ (q + 1) * m) :
    ∀ H, 1 ≤ H → H ≤ q →
      #(S.bandGaps m H) + #(S.lowRes m) + #(S.lowRes m) * ((H - 1) / 2) ≤ m - 1 := by
  have hm := hp.pos
  have h1 := card_bandGaps_one hmS hm
  intro H
  induction H using Nat.strong_induction_on with
  | _ H ih =>
    intro hH hHq
    rcases (show H = 1 ∨ H = 2 ∨ 3 ≤ H by omega) with rfl | rfl | h3
    · simp only [Nat.sub_self, Nat.zero_div, mul_zero, add_zero]; omega
    · have := card_le_card (bandGaps_antitone (S := S) hmS (show 1 ≤ 2 by norm_num))
      simp only [show (2 - 1) / 2 = 0 by rfl, mul_zero, add_zero]; omega
    · have hne : (S.bandGaps m ((H - 2) + 2)).Nonempty := by
        rw [show H - 2 + 2 = H by omega]
        obtain ⟨x, hx⟩ := bandGaps_last_nonempty (S := S) hqc hcq
        exact ⟨x, bandGaps_antitone hmS hHq hx⟩
      have hstep := card_bandGaps_step hp hmS (H - 2) hne
      rw [show H - 2 + 2 = H by omega] at hstep
      have hih := ih (H - 2) (by omega) (by omega) (by omega)
      have e : (H - 1) / 2 = (H - 2 - 1) / 2 + 1 := by omega
      rw [e, mul_add, mul_one]
      omega

/-- **LAYER-KNESER, prime modulus** (kernel-checked form): for prime `m ∈ S`, with
`D = q + 1 = ⌈c/m⌉`, `ℓ ≥ D + (D-2) k + k ∑_{j<D-2} ⌊j/2⌋`. -/
theorem ell_ge_layer_prime (hp : m.Prime) (hmS : m ∈ S) {q : ℕ} (hq : 1 ≤ q)
    (hqc : q * m < S.conductor) (hcq : S.conductor ≤ (q + 1) * m) :
    q + 1 + (q - 1) * #(S.lowRes m) + #(S.lowRes m) * ∑ j ∈ range (q - 1), j / 2 ≤ S.ell :=
  ell_ge_of_band_bounds hmS hp.pos hq hqc
    (fun H h1 h2 => band_bound_prime hp hmS hqc hcq H h1 (by omega))

/-- **Wilf from LAYER-KNESER** (prime `m ∈ S`). -/
theorem wilf_of_layer_prime (hp : m.Prime) (hmS : m ∈ S) {q : ℕ} (hq : 1 ≤ q)
    (hqc : q * m < S.conductor) (hcq : S.conductor ≤ (q + 1) * m)
    (hW : S.conductor ≤ S.embDim * (q + 1 + (q - 1) * #(S.lowRes m) +
      #(S.lowRes m) * ∑ j ∈ range (q - 1), j / 2)) :
    S.conductor ≤ S.embDim * S.ell :=
  hW.trans (Nat.mul_le_mul_left _ (ell_ge_layer_prime hp hmS hq hqc hcq))

/-! ### The last band (Yang–Zhang staircase) and the combined LK+YZ bound

With `c ≤ (q+1) m`, every gap lies in a band `H ≤ q`, so `g = ∑_{H ≤ q} #G_H`. In band `q` the gaps are residues
`1 ≤ r < c - q m` that are not in `lowRes` (a residue in `lowRes` is present in every band `≥ 1`). This gives the
staircase term `η_ρ = #{r ∈ lowRes : r < c - q m}` of Yang–Zhang (Preprints.org 202604.0551, Prop 3.1), for any `m ∈ S`.
-/

/-- Every gap lies in the bands `0, …, q` when `c ≤ (q+1) m`. -/
theorem genus_le_bands_full (hm : 0 < m) {q : ℕ} (hcq : S.conductor ≤ (q + 1) * m) :
    S.genus ≤ ∑ H ∈ range (q + 1), #(S.bandGaps m H) := by
  have hcov : S.gaps ⊆ (range (q + 1)).biUnion fun H => (S.bandGaps m H).image (fun r => H * m + r) := by
    intro n hn
    rw [mem_gaps] at hn
    have hnc := S.lt_conductor_of_not_mem hn
    rw [mem_biUnion]
    have hq : n / m < q + 1 := by
      rw [Nat.div_lt_iff_lt_mul hm]; omega
    refine ⟨n / m, mem_range.2 hq, mem_image.2 ⟨n % m, ?_, ?_⟩⟩
    · simp only [bandGaps, mem_filter, mem_range]
      refine ⟨Nat.mod_lt _ hm, ?_⟩
      rw [mul_comm, Nat.div_add_mod]; exact hn
    · rw [mul_comm, Nat.div_add_mod]
  calc S.genus = #S.gaps := rfl
    _ ≤ #((range (q + 1)).biUnion fun H => (S.bandGaps m H).image (fun r => H * m + r)) := card_le_card hcov
    _ ≤ ∑ H ∈ range (q + 1), #(S.bandGaps m H) :=
        card_biUnion_le.trans (sum_le_sum fun H _ => card_image_le)

/-- Gaps of the last band avoid `0`, the residues `≥ c - q m`, and `lowRes`. -/
theorem card_bandGaps_last (hmS : m ∈ S) {q : ℕ} (hq : 1 ≤ q) (hqc : q * m < S.conductor) :
    #(S.bandGaps m q) + #((S.lowRes m).filter (· < S.conductor - q * m)) ≤ S.conductor - q * m - 1 := by
  have hsub : S.bandGaps m q ∪ (S.lowRes m).filter (· < S.conductor - q * m) ⊆
      Ico 1 (S.conductor - q * m) := by
    intro r hr
    rw [mem_union] at hr
    rw [mem_Ico]
    rcases hr with hr | hr
    · refine ⟨Nat.pos_of_ne_zero fun h => zero_not_mem_bandGaps hmS q (h ▸ hr), ?_⟩
      have h := (mem_filter.1 hr).2
      have := S.lt_conductor_of_not_mem h
      omega
    · obtain ⟨h1, h2⟩ := mem_filter.1 hr
      exact ⟨(mem_filter.1 h1).2.1, h2⟩
  have hdisj : Disjoint (S.bandGaps m q) ((S.lowRes m).filter (· < S.conductor - q * m)) := by
    rw [disjoint_left]
    intro r hr hr'
    have hlow := (mem_filter.1 (mem_filter.1 hr').1).2.2
    apply (mem_filter.1 hr).2
    have h := add_mem hlow (mul_mem_of_mem hmS (q - 1))
    have e : q * m + r = m + r + (q - 1) * m := by
      obtain ⟨q', rfl⟩ : ∃ q', q = q' + 1 := ⟨q - 1, by omega⟩
      simp only [Nat.add_sub_cancel]; ring
    rw [e]; exact h
  have := card_le_card hsub
  rw [card_union_of_disjoint hdisj, Nat.card_Ico] at this
  omega

/-- **Abstract counting with the last band.** If the bands `1 ≤ H ≤ q-1` satisfy
`#G_H + k + δ·⌊(H-1)/2⌋ ≤ m - 1`, then `ℓ + #G_q ≥ (q + 1) + (q-1) k + δ ∑_{j<q-1} ⌊j/2⌋ + (c - q m - 1)`. -/
theorem ell_add_last_ge (hmS : m ∈ S) (hm : 0 < m) {q k δ : ℕ} (hq : 1 ≤ q)
    (hqc : q * m < S.conductor) (hcq : S.conductor ≤ (q + 1) * m)
    (hb : ∀ H, 1 ≤ H → H ≤ q - 1 → #(S.bandGaps m H) + k + δ * ((H - 1) / 2) ≤ m - 1) :
    q + 1 + (q - 1) * k + δ * ∑ j ∈ range (q - 1), j / 2 + (S.conductor - q * m - 1) ≤
      S.ell + #(S.bandGaps m q) := by
  have hg := genus_le_bands_full (S := S) hm hcq
  have hell := S.ell_add_genus
  have h0 := card_bandGaps_le (S := S) hmS hm 0
  obtain ⟨q', rfl⟩ : ∃ q', q = q' + 1 := ⟨q - 1, by omega⟩
  simp only [Nat.add_sub_cancel] at hb ⊢
  rw [sum_range_succ, sum_range_succ'] at hg
  have hsum : (∑ i ∈ range q', #(S.bandGaps m (i + 1))) + q' * k +
      δ * ∑ j ∈ range q', j / 2 ≤ q' * (m - 1) := by
    have := sum_le_sum (s := range q') (fun i hi =>
      hb (i + 1) (by omega) (by have := mem_range.1 hi; omega))
    simp only [Nat.add_sub_cancel, sum_add_distrib, sum_const, card_range, smul_eq_mul,
      ← mul_sum] at this
    linarith
  have hmm : (q' + 1) * m = q' * (m - 1) + (m - 1) + q' + 1 := by
    obtain ⟨m', rfl⟩ : ∃ m', m = m' + 1 := ⟨m - 1, by omega⟩
    simp only [Nat.add_sub_cancel]; ring
  omega

/-- **Yang–Zhang staircase** (Preprints.org 202604.0551, Prop 3.1), for any `m ∈ S`: with `D = q + 1`,
`ℓ ≥ D + (D-2) k + η_ρ`, where `η_ρ = #{r ∈ lowRes : r < c - q m}`. -/
theorem ell_ge_staircase (hmS : m ∈ S) (hm : 0 < m) {q : ℕ} (hq : 1 ≤ q)
    (hqc : q * m < S.conductor) (hcq : S.conductor ≤ (q + 1) * m) :
    q + 1 + (q - 1) * #(S.lowRes m) + #((S.lowRes m).filter (· < S.conductor - q * m)) ≤ S.ell := by
  have h := ell_add_last_ge (δ := 0) (k := #(S.lowRes m)) hmS hm hq hqc hcq
    (fun H h1 _ => by
      have h := card_le_card (bandGaps_antitone (S := S) hmS h1)
      have h' := card_bandGaps_one hmS hm
      simp only [zero_mul, add_zero]
      omega)
  have hl := card_bandGaps_last (S := S) hmS hq hqc
  simp only [zero_mul, add_zero] at h
  omega

/-- **LK+YZ, prime modulus, staircase form**: `ℓ ≥ D + (D-2) k + k ∑_{j<D-2} ⌊j/2⌋ + η_ρ`. -/
theorem ell_ge_lkyz_prime (hp : m.Prime) (hmS : m ∈ S) {q : ℕ} (hq : 1 ≤ q)
    (hqc : q * m < S.conductor) (hcq : S.conductor ≤ (q + 1) * m) :
    q + 1 + (q - 1) * #(S.lowRes m) + #(S.lowRes m) * ∑ j ∈ range (q - 1), j / 2 +
      #((S.lowRes m).filter (· < S.conductor - q * m)) ≤ S.ell := by
  have h := ell_add_last_ge hmS hp.pos hq hqc hcq
    (fun H h1 h2 => band_bound_prime hp hmS hqc hcq H h1 (by omega))
  have hl := card_bandGaps_last (S := S) hmS hq hqc
  omega

/-- **LK+YZ, prime modulus, Kneser form of the last band**: with `ρ = (q+1) m - c`,
`ℓ + ρ ≥ D + (D-2) k + k ∑_{j<D-2} ⌊j/2⌋ + k + k ⌊(D-2)/2⌋`. -/
theorem ell_ge_lkyz_prime' (hp : m.Prime) (hmS : m ∈ S) {q : ℕ} (hq : 1 ≤ q)
    (hqc : q * m < S.conductor) (hcq : S.conductor ≤ (q + 1) * m) :
    q + 1 + (q - 1) * #(S.lowRes m) + #(S.lowRes m) * ∑ j ∈ range (q - 1), j / 2 +
      (#(S.lowRes m) + #(S.lowRes m) * ((q - 1) / 2)) ≤ S.ell + ((q + 1) * m - S.conductor) := by
  have h := ell_add_last_ge hmS hp.pos hq hqc hcq
    (fun H h1 h2 => band_bound_prime hp hmS hqc hcq H h1 (by omega))
  have hlast := band_bound_prime hp hmS hqc hcq q hq le_rfl
  have e : (q + 1) * m = q * m + m := by ring
  omega

/-- The multiplicity case of LAYER-KNESER (prime multiplicity). -/
theorem ell_ge_layer_multiplicity (hp : S.multiplicity.Prime) {q : ℕ} (hq : 1 ≤ q)
    (hqc : q * S.multiplicity < S.conductor) (hcq : S.conductor ≤ (q + 1) * S.multiplicity) :
    q + 1 + (q - 1) * #(S.lowRes S.multiplicity) +
      #(S.lowRes S.multiplicity) * ∑ j ∈ range (q - 1), j / 2 ≤ S.ell :=
  ell_ge_layer_prime hp S.multiplicity_mem hq hqc hcq

end NumericalSemigroup
