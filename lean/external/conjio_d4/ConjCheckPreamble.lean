import Mathlib

/-! Our own definitions of numerical semigroups and Wilf's inequality, written independently
of the (unpublished) `FormalConjectures/ResearchTargets/Math30.lean`, with exactly the API
names used by the conjectures.io proof. Every API lemma is proved here; nothing is assumed. -/

namespace Math30.Wilf

structure NumericalSemigroup where
  carrier : AddSubmonoid ℕ
  finite_gaps : Set.Finite {x : ℕ | x ∉ carrier}
  proper : carrier ≠ ⊤

namespace NumericalSemigroup

variable (S : NumericalSemigroup)

def IsConductor (c : ℕ) : Prop := ∀ x, c ≤ x → x ∈ S.carrier

theorem exists_isConductor : ∃ c, S.IsConductor c := by
  obtain ⟨N, hN⟩ := S.finite_gaps.bddAbove
  refine ⟨N + 1, fun x hx => ?_⟩
  by_contra h
  have := hN h
  omega

noncomputable def conductor : ℕ := by
  classical
  exact Nat.find S.exists_isConductor

theorem conductor_spec (x : ℕ) (hx : S.conductor ≤ x) : x ∈ S.carrier := by
  classical
  exact Nat.find_spec S.exists_isConductor x hx

theorem conductor_le {c : ℕ} (hc : S.IsConductor c) : S.conductor ≤ c := by
  classical
  exact Nat.find_min' S.exists_isConductor hc

theorem conductor_pos : 0 < S.conductor := by
  by_contra h
  apply S.proper
  ext x
  simp only [AddSubmonoid.mem_top, iff_true]
  exact S.conductor_spec x (by omega)

theorem exists_pos_mem : ∃ x, 0 < x ∧ x ∈ S.carrier :=
  ⟨S.conductor, S.conductor_pos, S.conductor_spec _ le_rfl⟩

noncomputable def multiplicity : ℕ := by
  classical
  exact Nat.find S.exists_pos_mem

theorem multiplicity_pos : 0 < S.multiplicity := by
  classical
  exact (Nat.find_spec S.exists_pos_mem).1

theorem multiplicity_mem : S.multiplicity ∈ S.carrier := by
  classical
  exact (Nat.find_spec S.exists_pos_mem).2

theorem multiplicity_le {x : ℕ} (hpos : 0 < x) (hx : x ∈ S.carrier) : S.multiplicity ≤ x := by
  classical
  exact Nat.find_min' S.exists_pos_mem ⟨hpos, hx⟩

/-- A minimal (primitive) generator: a positive element that is not a sum of two positive
elements of the semigroup. -/
def IsPrimitive (x : ℕ) : Prop :=
  x ∈ S.carrier ∧ 0 < x ∧
    ∀ a b, a ∈ S.carrier → b ∈ S.carrier → x = a + b → a = 0 ∨ b = 0

theorem multiplicity_isPrimitive : S.IsPrimitive S.multiplicity := by
  refine ⟨S.multiplicity_mem, S.multiplicity_pos, ?_⟩
  intro a b ha hb he
  by_contra h
  push Not at h
  have h1 := S.multiplicity_le (Nat.pos_of_ne_zero h.1) ha
  have h2 := S.multiplicity_le (Nat.pos_of_ne_zero h.2) hb
  omega

theorem primitive_lt {x : ℕ} (hx : S.IsPrimitive x) : x < S.conductor + S.multiplicity := by
  by_contra h
  push Not at h
  have hmem : x - S.multiplicity ∈ S.carrier := S.conductor_spec _ (by omega)
  have hc := S.conductor_pos
  rcases hx.2.2 (x - S.multiplicity) S.multiplicity hmem S.multiplicity_mem
      (by have := S.multiplicity_pos; omega) with h0 | h0
  · omega
  · exact absurd h0 (Nat.pos_iff_ne_zero.mp S.multiplicity_pos)

noncomputable def primitiveElements : Finset ℕ := by
  classical
  exact (Finset.range (S.conductor + S.multiplicity)).filter S.IsPrimitive

theorem mem_primitiveElements (x : ℕ) : x ∈ S.primitiveElements ↔ S.IsPrimitive x := by
  classical
  unfold primitiveElements
  simp only [Finset.mem_filter, Finset.mem_range]
  exact ⟨fun h => h.2, fun h => ⟨S.primitive_lt h, h⟩⟩

noncomputable def leftElements : Finset ℕ := by
  classical
  exact (Finset.range S.conductor).filter (· ∈ S.carrier)

theorem mem_leftElements (x : ℕ) : x ∈ S.leftElements ↔ x < S.conductor ∧ x ∈ S.carrier := by
  classical
  unfold leftElements
  simp

theorem zero_mem_leftElements : 0 ∈ S.leftElements :=
  (S.mem_leftElements 0).mpr ⟨S.conductor_pos, S.carrier.zero_mem⟩

/-- `ℓ(S) = |S ∩ [0, c)|`. -/
noncomputable def leftCount : ℕ := S.leftElements.card

/-- `e(S)` = number of minimal generators. -/
noncomputable def embeddingDimension : ℕ := S.primitiveElements.card

/-- Wilf's inequality `c ≤ e · ℓ`. -/
def SatisfiesWilf : Prop := S.conductor ≤ S.embeddingDimension * S.leftCount

theorem closure_primitives : AddSubmonoid.closure {n | S.IsPrimitive n} = S.carrier := by
  apply le_antisymm
  · rw [AddSubmonoid.closure_le]
    intro x hx
    exact hx.1
  · intro x
    induction x using Nat.strong_induction_on with
    | _ x ih =>
      intro hx
      by_cases h0 : x = 0
      · subst h0; exact AddSubmonoid.zero_mem _
      by_cases hp : S.IsPrimitive x
      · exact AddSubmonoid.subset_closure hp
      · have : ¬ ∀ a b, a ∈ S.carrier → b ∈ S.carrier → x = a + b → a = 0 ∨ b = 0 := by
          intro hall; exact hp ⟨hx, Nat.pos_of_ne_zero h0, hall⟩
        push Not at this
        obtain ⟨a, b, ha, hb, he, ha0, hb0⟩ := this
        rw [he]
        exact AddSubmonoid.add_mem _ (ih a (by omega) ha) (ih b (by omega) hb)

end NumericalSemigroup

-- Test fixture: the ordinary semigroup `{0} ∪ [m, ∞)`.
namespace Fixtures

def ordinaryCarrier (m : ℕ) : AddSubmonoid ℕ where
  carrier := {x | x = 0 ∨ m ≤ x}
  zero_mem' := Or.inl rfl
  add_mem' := by
    rintro a b (ha | ha) (hb | hb)
    · exact Or.inl (by simp [ha, hb])
    · exact Or.inr (by omega)
    · exact Or.inr (by omega)
    · exact Or.inr (by omega)

def ordinary (m : ℕ) (hm : 1 < m) : NumericalSemigroup where
  carrier := ordinaryCarrier m
  finite_gaps := by
    apply (Finset.range m).finite_toSet.subset
    intro x hx
    simp only [Set.mem_setOf_eq] at hx
    simp only [Finset.coe_range, Set.mem_Iio]
    by_contra h
    exact hx (Or.inr (by omega))
  proper := by
    intro h
    have h1 : (1 : ℕ) ∈ ordinaryCarrier m := h ▸ AddSubmonoid.mem_top 1
    have h2 : (1 : ℕ) = 0 ∨ m ≤ 1 := h1
    omega

theorem ordinary_conductor (m : ℕ) (hm : 1 < m) : (ordinary m hm).conductor = m := by
  apply le_antisymm
  · apply NumericalSemigroup.conductor_le
    intro x hx
    exact (Or.inr hx : x = 0 ∨ m ≤ x)
  · by_contra h
    push Not at h
    have h1 := (ordinary m hm).conductor_spec (m - 1) (by omega)
    have h2 : m - 1 = 0 ∨ m ≤ m - 1 := h1
    omega

theorem ordinary_multiplicity (m : ℕ) (hm : 1 < m) : (ordinary m hm).multiplicity = m := by
  apply le_antisymm
  · exact (ordinary m hm).multiplicity_le (by omega) (Or.inr le_rfl : m = 0 ∨ m ≤ m)
  · have h1 : (ordinary m hm).multiplicity = 0 ∨ m ≤ (ordinary m hm).multiplicity :=
      (ordinary m hm).multiplicity_mem
    have h2 := (ordinary m hm).multiplicity_pos
    omega

end Fixtures

end Math30.Wilf
