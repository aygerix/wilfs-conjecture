import Mathlib

/-!
# SYMMETRIC-RECTANGLE (codex P8): a cyclic packing bound with missing pairs

Let `V` be a finite set of labels in `ZMod m`, `G ⊆ V` the "good" labels, and `Mo` a set of ordered "missing" pairs
with both entries outside `G` (closure under swapping is not needed). Suppose that formal pairs that are not missing have distinct
sums: if `(a, b)` and `(a', b')` are not missing and `a + b = a' + b'`, then `{a, b} = {a', b'}`.
Then, with `h = #G` and `k = #V - 1`,

    2 h k + 1 ≤ m + h (h - 1) + 2 #Mo.

Since `#Mo ≤ 2 e` for `e` unordered missing pairs and `h = k - v + 1`, this is `m ≥ k(k+1) + 1 - v(v-1) - 4e`
(P8_REPORT §2). No residue completeness or upper-layer hypothesis is used, and `m` may be composite.

Proof: `D₁ = {g - b : g ∈ G, b ∈ V, g ≠ b}` has `h k` elements. `D₁ ∩ (-D₁)` consists of good-good differences
(at most `h(h-1)`) and, for each missing ordered pair `(b, b')`, at most two values `g - b` with `g + g' = b + b'`.
Finally `0 ∉ D₁ ∪ (-D₁)`.
-/

namespace NumericalSemigroup

open Finset

variable {m : ℕ} [NeZero m]

/-- `D₁ = {g - b : g ∈ G, b ∈ V, g ≠ b}`. -/
def rectDiff (G V : Finset (ZMod m)) : Finset (ZMod m) :=
  ((G ×ˢ V).filter (fun p => p.1 ≠ p.2)).image (fun p => p.1 - p.2)

/-- The SYMMETRIC-RECTANGLE bound. -/
theorem symmetric_rectangle (G V : Finset (ZMod m)) (Mo : Finset (ZMod m × ZMod m))
    (hGV : G ⊆ V)
    (hMo : ∀ p ∈ Mo, p.1 ∈ V ∧ p.2 ∈ V ∧ p.1 ∉ G ∧ p.2 ∉ G)
    (hinj : ∀ a ∈ V, ∀ b ∈ V, ∀ a' ∈ V, ∀ b' ∈ V, (a, b) ∉ Mo → (a', b') ∉ Mo → a + b = a' + b' →
      (a = a' ∧ b = b') ∨ (a = b' ∧ b = a')) :
    2 * #G * (#V - 1) + 1 ≤ m + #G * (#G - 1) + 2 * #Mo := by
  classical
  -- pairs with a good entry are never missing
  have hgood : ∀ a b, (a ∈ G ∨ b ∈ G) → (a, b) ∉ Mo := by
    intro a b hab hm
    obtain ⟨-, -, h1, h2⟩ := hMo _ hm
    rcases hab with h | h
    · exact h1 h
    · exact h2 h
  set D := rectDiff G V with hD
  -- |D₁| = h k
  have hDcard : #D = #G * (#V - 1) := by
    have hinjD : Set.InjOn (fun p : ZMod m × ZMod m => p.1 - p.2)
        ((G ×ˢ V).filter (fun p => p.1 ≠ p.2) : Set (ZMod m × ZMod m)) := by
      rintro ⟨g, b⟩ hp ⟨g', b'⟩ hp' heq
      simp only [coe_filter, mem_product, Set.mem_ofPred_eq] at hp hp'
      have hs : g + b' = g' + b := by
        have := congrArg (· + (b + b')) heq
        simp only at this
        linear_combination this
      rcases hinj g (hGV hp.1.1) b' hp'.1.2 g' (hGV hp'.1.1) b hp.1.2 (hgood _ _ (Or.inl hp.1.1))
          (hgood _ _ (Or.inl hp'.1.1)) hs with ⟨h1, h2⟩ | ⟨h1, h2⟩
      · rw [h1, h2]
      · exact absurd h1 hp.2
    rw [hD, rectDiff, card_image_of_injOn hinjD]
    have : (G ×ˢ V).filter (fun p => p.1 ≠ p.2) = (G ×ˢ V) \ (G.image fun g => (g, g)) := by
      ext ⟨g, b⟩
      simp only [mem_filter, mem_product, mem_sdiff, mem_image, Prod.mk.injEq, ne_eq]
      constructor
      · rintro ⟨⟨hg, hb⟩, hne⟩
        exact ⟨⟨hg, hb⟩, fun ⟨x, _, h1, h2⟩ => hne (h1.symm.trans h2)⟩
      · rintro ⟨⟨hg, hb⟩, hn⟩
        exact ⟨⟨hg, hb⟩, fun h => hn ⟨g, hg, rfl, h⟩⟩
    rw [this, card_sdiff_of_subset, card_product, card_image_of_injective _ (fun x y h => by
      simpa using congrArg Prod.fst h)]
    · rw [Nat.mul_sub_one]
    · intro p hp
      obtain ⟨g, hg, rfl⟩ := mem_image.1 hp
      exact mem_product.2 ⟨hg, hGV hg⟩
  -- good-good differences
  set GG := ((G ×ˢ G).filter (fun p => p.1 ≠ p.2)).image (fun p => p.1 - p.2) with hGG
  have hGGcard : #GG ≤ #G * (#G - 1) := by
    refine card_image_le.trans ?_
    have : (G ×ˢ G).filter (fun p => p.1 ≠ p.2) = G.offDiag := by
      ext ⟨a, b⟩; simp [mem_offDiag, and_assoc]
    rw [this, offDiag_card, Nat.mul_sub_one]
  -- the two exceptional values for each missing ordered pair
  set E : ZMod m × ZMod m → Finset (ZMod m) := fun p =>
    (G.filter (fun g => ∃ g' ∈ G, g + g' = p.1 + p.2)).image (fun g => g - p.1) with hE
  have hEcard : ∀ p ∈ Mo, #(E p) ≤ 2 := by
    intro p _
    refine card_image_le.trans ?_
    by_cases hne : (G.filter (fun g => ∃ g' ∈ G, g + g' = p.1 + p.2)).Nonempty
    · obtain ⟨g1, hg1⟩ := hne
      obtain ⟨hg1G, g1', hg1'G, hs1⟩ := mem_filter.1 hg1
      have hsub : G.filter (fun g => ∃ g' ∈ G, g + g' = p.1 + p.2) ⊆ {g1, g1'} := by
        intro g hg
        obtain ⟨hgG, g', hg'G, hs⟩ := mem_filter.1 hg
        rcases hinj g (hGV hgG) g' (hGV hg'G) g1 (hGV hg1G) g1' (hGV hg1'G) (hgood _ _ (Or.inl hgG))
            (hgood _ _ (Or.inl hg1G)) (hs.trans hs1.symm) with ⟨h1, _⟩ | ⟨h1, _⟩
        · simp [h1]
        · simp [h1]
      exact (card_le_card hsub).trans (card_insert_le _ _)
    · rw [not_nonempty_iff_eq_empty.1 hne]; simp
  -- D₁ ∩ (-D₁) ⊆ GG ∪ ⋃_{p ∈ Mo} E p
  have hint : D ∩ D.image (fun x => -x) ⊆ GG ∪ Mo.biUnion E := by
    intro x hx
    obtain ⟨hx1, hx2⟩ := mem_inter.1 hx
    obtain ⟨⟨g, b⟩, hp, rfl⟩ := mem_image.1 hx1
    obtain ⟨y, hy, hyx⟩ := mem_image.1 hx2
    obtain ⟨⟨g', b'⟩, hp', rfl⟩ := mem_image.1 hy
    simp only [mem_filter, mem_product] at hp hp'
    simp only at hyx
    -- g - b = b' - g', so g + g' = b + b'
    have hs : g + g' = b + b' := by linear_combination hyx.symm
    rw [mem_union]
    by_cases hbG : b ∈ G
    · left
      exact mem_image.2 ⟨(g, b), mem_filter.2 ⟨mem_product.2 ⟨hp.1.1, hbG⟩, hp.2⟩, rfl⟩
    · right
      by_cases hb'G : b' ∈ G
      · exfalso
        rcases hinj g (hGV hp.1.1) g' (hGV hp'.1.1) b hp.1.2 b' hp'.1.2 (hgood _ _ (Or.inl hp.1.1))
            (hgood _ _ (Or.inr hb'G)) hs with ⟨h1, _⟩ | ⟨_, h2⟩
        · exact hbG (h1 ▸ hp.1.1)
        · exact hbG (h2 ▸ hp'.1.1)
      · have hmiss : (b, b') ∈ Mo := by
          by_contra hn
          rcases hinj g (hGV hp.1.1) g' (hGV hp'.1.1) b hp.1.2 b' hp'.1.2 (hgood _ _ (Or.inl hp.1.1))
              hn hs with ⟨h1, _⟩ | ⟨_, h2⟩
          · exact hbG (h1 ▸ hp.1.1)
          · exact hbG (h2 ▸ hp'.1.1)
        refine mem_biUnion.2 ⟨(b, b'), hmiss, mem_image.2 ⟨g, mem_filter.2 ⟨hp.1.1, g', hp'.1.1, hs⟩, rfl⟩⟩
  have hintcard : #(D ∩ D.image (fun x => -x)) ≤ #G * (#G - 1) + 2 * #Mo := by
    refine (card_le_card hint).trans ((card_union_le _ _).trans ?_)
    have hb : #(Mo.biUnion E) ≤ 2 * #Mo := by
      refine card_biUnion_le.trans ?_
      calc ∑ p ∈ Mo, #(E p) ≤ ∑ _p ∈ Mo, 2 := sum_le_sum hEcard
        _ = 2 * #Mo := by rw [sum_const, smul_eq_mul, mul_comm]
    omega
  -- 0 ∉ D₁ ∪ (-D₁)
  have h0 : D ∪ D.image (fun x => -x) ⊆ univ.erase 0 := by
    intro x hx
    refine mem_erase.2 ⟨?_, mem_univ _⟩
    rcases mem_union.1 hx with hx | hx
    · obtain ⟨⟨g, b⟩, hp, rfl⟩ := mem_image.1 hx
      simp only [mem_filter] at hp
      exact sub_ne_zero.2 hp.2
    · obtain ⟨y, hy, rfl⟩ := mem_image.1 hx
      obtain ⟨⟨g, b⟩, hp, rfl⟩ := mem_image.1 hy
      simp only [mem_filter] at hp
      rw [neg_sub]; exact sub_ne_zero.2 (Ne.symm hp.2)
  have hneg : #(D.image (fun x => -x)) = #D := card_image_of_injective _ neg_injective
  have hU := card_union_add_card_inter D (D.image fun x => -x)
  have hUle := card_le_card h0
  rw [card_erase_of_mem (mem_univ _), card_univ, ZMod.card] at hUle
  have hm := NeZero.pos m
  have e2 : 2 * #G * (#V - 1) = 2 * (#G * (#V - 1)) := by ring
  rw [e2]
  omega

end NumericalSemigroup
