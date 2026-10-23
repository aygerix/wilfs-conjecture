# LIT_CL.md — literature scout for Corollary H, Tile-CL, and depth-free reductions (2026-10-17)

> Current handoff: [STATE.md](STATE.md). Binding user rules: [DIRECTIVES.md](DIRECTIVES.md).

Scope: three targeted questions (Q1–Q3) from PROOFS.md ("Corollary H", "CH'", "CL", "Tile-CL").
Does not repeat LITERATURE.md. Budget about 40 tool calls; search NOT exhaustive (alphaXiv index, web search,
primary PDFs listed below). Status labels are the same as LITERATURE.md:
READ = statement read in the source text; SECONDARY = seen quoted elsewhere; ABSTRACT = abstract/summary only;
UNVERIFIED = memory or search snippet; OURS = derivation made here (not from a source; check before use).

---------------------------------------------------------------------------------------------------
## Short answers

- **Q1 (is Corollary H known?) NOT FOUND.** No source examined states (d+1)·ΣAp ≤ d·m·max Ap, the
  equivalent e·n ≥ c − (e−2)(m−1)/2, or any bound of the form e·n ≥ c − C·(e−2)(m−1). The closest published
  items are listed in §1.2. Two facts frame it: (a) in BGOW coordinates Corollary H is exactly the
  *homogeneous (leading-order) part* of BGOW's face-wise Wilf inequality (4.2), plus an additive error;
  (b) BGOW's Wilf-game proof (Thm 6.5) handles exactly this linear functional, but only face by face and
  only when a winning move sequence exists. Treat Corollary H as **apparently new, not confirmed**.
- **Q2 (anything like Tile-CL?) The objects are classical. NO such inequality FOUND.** Tile-CL's tiles D
  are, under other names: standard-monomial sets of initial ideals of the lattice ideal I_L
  (BMO "Polyhedra and posets IV", Remark 5.7), "staircase" Kunz nilsemigroups / Apéry sets of unique
  expression, L-shapes / minimum distance diagrams (MDDs) of weighted multi-loop networks, and Nakamura
  G-graphs for G = ℤ/m. The literature on these objects bounds *max versus cardinality* (diameter versus
  order: "solid density"). It also counts L-shapes and describes Gröbner/Kunz fans. Nothing found bounds
  a first moment or a discrepancy of column-top masses against the cyclic order of residues.
- **Q3 (depth-free reductions?) Only one is published, and it is only sufficient: the BGOW "Wilf game"
  (Def 6.2, Thm 6.5).** It depends only on the Apéry/Kunz poset P and a maximal element f. BGOW's main
  reduction (Algorithm 4.1, Thm 4.3, Conj 4.4) is face-wise but **point-dependent**: the region tested
  involves x_f and Σx_i, so depth enters. Structurally the Wilf game is the closest published analogue of
  CL; its score item (ii) (+1 for a "wrap-around" move, k < i) is a carry count (§3.3).

---------------------------------------------------------------------------------------------------
## 1. Q1 — Corollary H

Statement (PROOFS.md): (d+1)·Σ_{w∈Ap(S,m)} w ≤ d·m·max Ap(S,m), d = e−1; equivalently e·n ≥ c − (e−2)(m−1)/2.

### 1.1 Corollary H in the standard coordinates (OURS, elementary algebra)
- Kunz coordinates x_i = (w_i − i)/m, max Ap = m·x_f + f (BGOW Lemma 3.2, READ): Corollary H ⇔
      e·Σx_i − m(e−1)·x_f ≤ (e−1)·f − e(m−1)/2.
  BGOW's Wilf inequality on a face is (READ, proof of Thm 6.5):
      e·Σx_i − m(e−1)·x_f ≤ (e−1)·f − (e−1)(m−1).
  The right-hand sides differ by exactly (e−2)(m−1)/2. So Corollary H confines every BGOW "bad region"
  R_f (Algorithm 4.1) to a slab of that width in the functional e·Σx − m(e−1)x_f.
- In Apéry-point coordinates (Kaplan–O'Neill group cone C(ℤ_m), §2.4), Corollary H is **homogeneous of
  degree 1**: (d+1)·Σ_i a_i ≤ d·m·max_i a_i, with d = number of atoms of the Kunz poset (BGOW Cor 3.11,
  READ). Hence it is equivalent to "homogeneous Wilf on every face of the group cone that contains Apéry
  points", up to the closure and scaling argument (OURS, not checked in detail).
- BGOW observe (READ, §4 "Implementation" + Thm 4.3) that every region R_f is *rationally* infeasible for
  m ≤ 18. That implies the homogeneous inequality on all faces for m ≤ 18 (OURS: take recession directions).
  Corollary H gives the homogeneous inequality for **all** m. Not found anywhere for general m.
  (The v2 text also says "each region tested in Algorithm 4.1 for m ≤ 87 is in fact empty". This looks like
  a typo for 18; not relied on.)

### 1.2 Closest published statements found (none is Corollary H)
| Source | What it proves / uses | Relation to Corollary H | Status |
|---|---|---|---|
| Sammartano, Semigroup Forum 85 (2012), arXiv:1111.1863 | Prop 10: Wilf ⇔ Σ_{k<L}(n_kν − m) + (n_Lν − ρ) ≥ 0 (levels I_k = [km,(k+1)m−1]); Prop 13: η_j = ⌊w_j/m⌋ − ⌊w_{j−1}/m⌋ (w_j sorted Apéry); Thm 18 (2ν ≥ m) | Level/floor reformulation through sorted Apéry elements; no Σw vs max w inequality | READ |
| Moscariello–Sammartano, Math. Z. 280 (2015), arXiv:1408.5331 | Prop 3: Δ = Σ_j ε_j(jd − a_1) + (n_Q d − R) = W; Lemmas 4–7 (Apéry poset bounds ω_x ≤ xω_1 etc.); Thm 1 | Same level formalism; no mean/max bound | READ |
| D'Anna–Moscariello, Math. Z. 304 (2023) | m − 1 ≤ (e−1)n; c ≤ q·e·n | Different (multiplicity and depth bounds) | READ in LITERATURE.md |
| BGOW, IJAC 30 (2020), arXiv:1903.04342 | (4.1)/(4.2), Thm 6.5 proof: e·Σx − m(e−1)x_f + (e−1)(m−1−f) ≤ 0 is certified by face equalities | Same functional; proved only per winnable face | READ |
| Delgado survey, arXiv:1902.03461 | Full survey through 2019 | No Apéry-mean inequality listed | READ (pp. 1–13) |
| Kaplan, JPAA 216 (2012), author PDF | §5: "there is no obvious relationship between e(S) and its Apéry set or genus" | Explicitly notes the missing link | READ |
| Fiduccia–Forcade–Zito, SIAM J. DM 11 (1998); Forcade–Lamoreaux, SIAM J. DM 13 (2000); Aguiló–Zaragozá arXiv:1806.03899 | "Solid density" δ = n/(k+d)^d of an MDD; Δ_2 = 1/3, conjectured Δ_3 = 21/250 | Max-vs-cardinality (volume) bound for the same tiles; no mean-vs-max bound | READ (1806.03899); FFZ and FL SECONDARY |
| Cisto, arXiv:2209.05803 | Transform A fixes F, g, n; reduces Wilf to leaves of trees T'_{g,n} (Cor 6.8, Prop 6.9) | Unrelated mechanism | READ |

Heuristic remark (OURS, not from the literature): Corollary H is the discrete analogue of the fact that for a
down-closed (hence star-shaped) body K ⊂ ℝ^d_+, the mean of a positive linear form ℓ over K is at most
(d/(d+1))·max_K ℓ. The slice measure of {ℓ = t} divided by t^{d−1} is non-increasing, and the simplex
attains equality. The (d−1)m(m−1)/2 term in CH is the discretisation error.

### 1.3 Queries used (Q1)
WebSearch: "Wilf's conjecture Apéry set sum inequality embedding dimension mean of Apéry set maximum Frobenius
number" (extended); "numerical semigroup genus upper bound in terms of Frobenius number, multiplicity and
embedding dimension Wilf (m-1)/2 Apéry set average" (extended); "subadditive function on cyclic group Z_m
average value at most d/(d+1) times maximum ... mean of Apéry set versus Frobenius number embedding dimension"
(extended); "abelian Cayley digraph minimum distance diagram average distance at most d/(d+1) diameter
inequality" (extended). alphaXiv discover: [Wilf's conjecture, Apéry set, embedding dimension] "inequalities
bounding the sum or average of the Apéry set ... error term depending on multiplicity". PDFs queried:
1902.03461, 1111.1863, 1408.5331, 1903.04342, 2209.05803, 1806.03899, Kaplan JPAA author PDF.
**Not accessed:** Eliahou "Wilf's conjecture and Macaulay's theorem" (already READ for LITERATURE.md; no such
statement recorded there), FGH 1987, Dobbs–Matthews 2006, Zhai 2013, Kunz–Waldi "Geometrical illustration of
numerical semigroups..." (Semigroup Forum 89 (2014) 664–691; full text not accessible; abstract says they draw
semigroups containing p, q as lattice paths). A Corollary-H-type statement could still be hidden in those.

### 1.4 Side result: Kaplan numbering (resolves LITERATURE.md Note A) — READ, author PDF
- **Theorem 24**: "Let S be a semigroup such that 2g < 3m or such that F < 2m. Then Conjecture 4 [Wilf] holds."
- **Proposition 26**: "Suppose S is a semigroup with F < 2m. Then Conjecture 4 holds. Moreover, equality holds
  if and only if S = ⟨m, m+1, …, 2m−1⟩, or S = ⟨3,4⟩."
  The equality clause is wrong: T_{m,2} = ⟨m, 2m+1, …, 3m−1⟩ has F = 2m−1 < 2m and W = 0. This agrees with
  LITERATURE.md (F4) / Marashdeh. (Kaplan himself uses this example in the text before Prop 26, for g ≥ 3m/2.)
  So both Delgado and DKM are partly right: Thm 24 covers both hypotheses; Prop 26 is the c ≤ 2m case.

---------------------------------------------------------------------------------------------------
## 2. Q2 — Tile-CL (down-set fundamental domains of Λ = ker(ℤ^d → ℤ/m))

### 2.1 The same objects in the literature
1. **Lattice ideals / Gröbner fans.** Brower–McDonough–O'Neill, "Numerical semigroups, polyhedra, and posets IV:
   walking the faces of the Kunz cone", arXiv:2401.06025 (READ):
   - Def 3.2: a *staircase* nilsemigroup is one where every non-nil element factors uniquely. S is staircase iff
     every Apéry element factors uniquely ("Apéry set of unique expression", Rosales, J. Algebra 226 (2000)).
   - Thm 3.8 / Cor 3.9: the Kunz fan G(m;A) is a pure fan. Its chambers are exactly the faces with a staircase
     Kunz nilsemigroup.
   - Prop 3.4: Kunz/Apéry values are y_i = min{c·x : c ∈ ℤ^k_{≥0}, Σ c_j p_j ≡ i mod m}. This is a
     group-relaxation value function.
   - **Remark 5.7**: G(m;A) is a portion of the Gröbner fan of the lattice ideal I_L, L = {z : Σ a_j z_j ∈ mℤ}
     (rank k, index m). Each chamber's initial ideal consists of the monomials that are not "optimal" for a
     weight vector in the chamber. The paper cites Miller–Sturmfels Cor 7.29.
   - Thm 6.2: every Kunz nilsemigroup refines a staircase one with the same atoms.
   - Remark 6.6 / Question 6.7 / Conj 6.8: facet counts of Gröbner-fan chambers of I_L for index-m lattices in ℤ^3.
   **Consequence for the project (OURS, short proof):** the PROOFS.md down-set D(≺) is the standard-monomial set
   of in_{p,≺}(I_L), using the *actual generator values* p = (p_1,…,p_d) as the weight vector and ≺ to break ties.
   Reason: in each residue fiber, min⟨n,p⟩ is the Apéry element, because the least element of S in a residue class
   never uses m. Hence **CL needs Tile-CL only for coherent tiles** (initial ideals of I_L), and only for weights in
   the Kunz-fan region (positive weights ≡ p̂ mod m). Tile-CL as written, over all down-set fundamental domains,
   may include non-coherent tiles. Non-coherent monomial A-graded ideals exist in the toric Hilbert scheme setting
   (Maclagan–Thomas; Peeva–Stillman). That statement is UNVERIFIED here and is from memory. If Tile-CL fails, look
   first for a non-coherent counterexample; a proof may use the weight vector.
2. **Minimum distance diagrams / L-shapes.** Aguiló-Gost–García-Sánchez–Llena, arXiv:1505.01464 (READ):
   - Def 1: L ⊂ ℕ^k is an L-shape for a closed set C ⊆ S if x ↦ Ax is a bijection L → C and L is down-closed.
   - For C = Ap(S, n_k), L-shapes are exactly the MDDs of the weighted circulant digraph C(n_k; n_1..n_{k−1};
     n_1..n_{k−1}).
   - For e = 3 at most two L-shapes; Thm 16: for e = 4 the number of L-shapes is unbounded (family
     ⟨n, 3n−2, 3n−1, F(T)⟩).
   - So D(≺) can vary a great deal with ≺ once d ≥ 3. Tile-CL must hold for each of them, which is a useful stress
     family.
   Aguiló–Zaragozá arXiv:1806.03899 (READ):
   - Def 1 (MDD): n unit cubes, down-closed, ℓ1-minimal in each class.
   - MDDs tessellate ℝ^d by d translation vectors; L-shape parametrisation L(l,h,w,y) with n = lh − wy (d = 2).
   - Diameter and solid density results: Δ_2 = 1/3, conjecture Δ_3 = 21/250.
   - Earlier sources: Wong–Coppersmith 1974, Fiol–Yebra–Alegre–Valero 1987, Rødseth 1996 (weighted),
     Sabariego–Santos 2009 (unified MDD definition; arbitrarily many MDDs for triple-loop). All SECONDARY.
3. **G-graphs.** Nakamura, "Hilbert schemes of abelian group orbits", J. Alg. Geom. 10 (2001). A G-graph is a
   down-closed set of monomials with one monomial in each character class of an abelian G ⊂ GL_n. For G = ℤ/m
   with weights p̂ this is exactly a Tile-CL tile. Exact definition text was NOT read (UNVERIFIED wording).
   Morita, arXiv:0712.2892 (READ intro/§2–4): the normalisation of Hilb^G is the toric variety of a Gröbner fan.
   Related sources (titles only): Craw–Reid, "How to calculate A-Hilb C^3"; Craw–Maclagan–Thomas, "Moduli of
   McKay quiver representations".
4. **Group cone.** Kaplan–O'Neill, "Numerical semigroups, polyhedra, and posets I: the group cone",
   arXiv:1912.03741 (READ):
   - Def 3.1: C(G) = {x ≥ 0 : x_a + x_b ≥ x_{a+b}}, the cone of subadditive functions on G (Gomory 1969;
     Richard–Dey 2010).
   - Thm 4.7: P_m is a translate of C(ℤ_m). Cor 4.8: Apéry points are characterised.
   - Prop 3.10: cover relations are labelled by atoms.
5. **Gröbner computation of Apéry sets.** Márquez-Campos–Ojeda–Tornero arXiv:1907.01222; Morales–Dung
   arXiv:1510.01973. Found; content not read (UNVERIFIED that they describe Apéry sets as standard monomials).
6. **Hilbert function of k[S]/(t^m)** (= k[x_1..x_d]/(image of I_S), whose standard monomials are a D):
   no Wilf-type moment statement was found. Time was not spent on Cortadellas–Zarzuela's "Apéry table"
   (UNVERIFIED relevance).

### 2.2 What was NOT found
- No inequality for these tiles of the form Σ_y T(y)·⟨s − φ(y)⟩ ≥ (d−1)m(m−1)/2, nor any of the equivalent
  forms (II), (Diff), (Win), (Wall), (Walk).
- No residue-interval discrepancy bound |Σ_{y∈I}(T(φ^{-1}y) − d)| ≤ m − 1.
- No first-moment bound (mean ≤ d/(d+1)·max, weighted or unweighted).
- The MDD/degree–diameter literature has only volume-type bounds (solid density).
- The G-Hilb literature uses "age" Σ_a⟨k p̂_a⟩/m; it is reminiscent of the ⟨·⟩ sums in Tile-CL, but no link was found.

### 2.3 Queries used (Q2)
WebSearch: "Nakamura G-graph abelian group Hilbert scheme monomials one in each character class closed under
division fundamental domain lattice"; "Kunz Waldi Geometrical illustration of numerical semigroups ... Wilf
lattice points Apéry set"; "Apéry set numerical semigroup Gröbner basis standard monomials ... Márquez-Campos
Ojeda Tornero"; the extended MDD average-distance query (§1.3). alphaXiv discover: [Kunz cone, Kunz polyhedron,
Apéry poset, Wilf's conjecture]. PDFs: 2401.06025 (twice), 0712.2892, 1505.01464, 1806.03899, 1912.03741.
**Not searched:** "Hilbert function of k[S]/(t^m)" as its own query; Fiedler; Aguiló–García-Sánchez
"Factoring in embedding dimension three" (EJC 2010); Rødseth 1978. Budget ran out; these are leads only.

---------------------------------------------------------------------------------------------------
## 3. Q3 — depth-free reductions

### 3.1 BGOW (arXiv:1903.04342 v2; IJAC 30 (2020) 861–882) — READ
- Def 3.3: relaxed Kunz polyhedron P'_m and Kunz cone C_m. Prop 3.4: P'_m = v + C_m with v = (−i/m)_i.
- Thm 3.10: semigroups S, T lie in the interior of the same face of P'_m iff they have the same Apéry poset.
  Cor 3.11: e − 1 = number of minimal elements and t = number of maximal elements are constant on a face interior.
- Algorithm 4.1: for each face F and each maximal f, test whether the integer points of F° satisfying (4.1)
  m x_i + i ≤ m x_f + f and ¬(4.2) m x_f + f − m + 1 ≤ e(m x_f + f − m − Σx_i + 1) form a nonempty set.
  **This is point-dependent**: x_f and Σx_i carry the depth.
- Skipped faces: e(F) ≥ t(F)+1 (FGH) and 2e(F) ≥ m (Sammartano). The remaining faces are called "bad".
- Thm 4.3: for m ≤ 18 every tested region is empty. Implementation note: each region is even rationally infeasible.
- **Conj 4.4**: for each m ≥ 3 every region considered in Algorithm 4.1 is empty. This implies Wilf.
- Cor 4.5: m − e ≤ 9 ⇒ Wilf. Cor 4.6: m − e ≤ 12, using Eliahou's 3e ≥ m.
- Remark 4.7: no new equality cases for m ≤ 15.

### 3.2 The Wilf game (BGOW §6) — the only depth-free criterion found
- Def 6.2. Data: an m-Kunz poset P, a maximal element f, and e − 1 = number of minimal elements.
  - Start from e·x_1 + … + e·x_{m−1} with initial score m−1−f.
  - A move replaces x_i + x_{k−i} by x_k, for i ≺ k.
  - Move score: (i) the net change in the number of summands with index > f; (ii) **+1 if k < i**; (iii) +2 for
    each move beyond the first m − e.
  - A sequence of at least m − e moves wins if the net score is ≥ 0.
- Thm 6.5: if P has a winning sequence for every maximal f, then Wilf holds for every semigroup in F°.
  The proof shows e·Σx − m(e−1)x_f + (e−1)(m−1−f) ≤ 0 using the face equalities x_i + x_j = x_{i+j} or
  = x_{i+j−m} − 1, and the bounds x_i ≤ x_f (i < f), x_i ≤ x_f − 1 (i > f).
- Cor 6.6: the game is winnable for symmetric S and for MED. Remark 6.1: any counterexample lies in a face whose
  game is unwinnable.
- **No later paper was found that proves winnability for a general class** (WebSearch "Wilf game" Apéry poset).

### 3.3 Comparison with CL / Tile-CL (OURS; observations, not proved)
- Both are depth-free. The Wilf game uses (P, f). Tile-CL uses (D, p̂ mod m, s = M mod m), with D refining the
  same poset data by Thm 6.2 of paper IV.
- The game's score (ii), "+1 if k < i", counts wrap-around moves where i + (k−i) exceeds m in residues. These are
  the moves that use the inhomogeneous face equation x_i + x_j = x_{i+j−m} − 1. This is the same carry mechanism
  that CL measures with ⟨·⟩ = (· mod m).
- A natural candidate link: CL may be a *fractional/averaged* Wilf game in which the canonical "moves" are the
  columns of D (column identity CH'). If so, CL would give a uniform winning strategy that BGOW lack. Worth
  formalising. One test: on BGOW Example 6.4 (S = ⟨6,9,20⟩, f = 1), compare their winning sequence with the CH'
  column decomposition.
- Other reductions checked, none depth-free:
  - Marashdeh Conj 5.2 (LITERATURE.md): c-free and n-free, but uses λ(f_i).
  - Eliahou graph/divset reductions: τ(X) uses depths.
  - Cisto's tree reductions (arXiv:2209.05803 Cor 6.8, Prop 6.9: Wilf for all leaves of T'_{g,n} ⇒ Wilf on N_{g,n}).

### 3.4 Queries used (Q3)
alphaXiv discover: [Kunz cone, Kunz polyhedron, Apéry poset, Wilf's conjecture]. WebSearch: "Wilf game" Apéry
poset numerical semigroup winnable. PDFs: 1903.04342, 2401.06025, 1912.03741.

---------------------------------------------------------------------------------------------------
## 4. Suggested uses (for the lead; not done here)
1. Record in PROOFS.md that Corollary H = the homogeneous BGOW inequality on all group-cone faces, together with
   the (e−2)(m−1)/2 slab statement. Keep "novelty unconfirmed" until Kunz–Waldi 2014 and FGH 1987 are checked.
2. Restrict Tile-CL to coherent tiles (standard sets of in_w(I_L)). This is all that CL ⇒ Wilf needs. Check
   whether the exhaustive E15 runs included non-coherent tiles.
3. Use the e = 4 family ⟨n, 3n−2, 3n−1, F(T)⟩ (1505.01464) to stress-test CL across many ≺ (many L-shapes).
4. Try to derive a Wilf-game winning strategy from the CH' column decomposition (§3.3).
