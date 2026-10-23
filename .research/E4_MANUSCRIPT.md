# Wilf's conjecture in embedding dimension four, via three-dimensional lattice tiles

> Current handoff: [STATE.md](STATE.md). Binding user rules: [DIRECTIVES.md](DIRECTIVES.md).

*Self-contained manuscript. It consolidates the project record as of 2026-10-18: `.research/STATE.md` (links 1–7),
`.research/PROOFS.md`, `.research/NOTEBOOK.md`, the two referee reports in `.research/reviews/`, `lean/`, `logs/` and
`.research/EXPERIMENTS.md`. No new mathematics is introduced. Where the record is incomplete or unclear, the text says
so in the form **[GAP: …]**. All gaps and source inconsistencies are collected in Appendix A.*

---

## Status (read first)

- **Claim.** Every numerical semigroup S with embedding dimension e(S) = 4 satisfies Wilf's inequality e·ℓ ≥ c.
- **What the proof uses.**
  - (E1) Eliahou's theorem: c ≤ 3m implies Wilf. Cited, not rechecked.
  - (E2) Bruns–García-Sánchez–O'Neill–Wilburne: m ≤ 18 implies Wilf. Cited, not rechecked; it is itself computer-assisted.
  - (FC) A finite computation: every non-two-face lattice tile with 19 ≤ m ≤ 279 satisfies δ ≥ −1, except three tiles at
    m ∈ {19, 20}, which are certified by a linear program.
  - Everything else is proved on paper in §§3–9.
- **Status of (FC).** Complete. The certified 16-bit enumeration covers every m ∈ [4, 280], and every lattice passed
  the area certificate (EXPERIMENTS E140, E141; §10.5).
  - Three gaps were flagged while this manuscript was drafted: G1, m = 236–255 had no log; G2, the area certification
    of m = 41–45 was undocumented; G3, m = 120–235 had no per-lattice certificate.
  - All three were **closed on 2026-10-18** by `logs/tsv16_4_119_fejer.log` and `logs/tsv16_120_255_fejer.log` (E141).
    I parsed both logs independently (§10.5).
- **Verdict.** No mathematical gap remains in the record.
  - The theorem is proved on paper modulo (E1), (E2) and (FC).
  - It is still **provisional** in the project's sense, because (E1) and (E2) are cited without being rechecked, (FC)
    rests on code trust, and the Lean coverage is partial.
  - The one remaining flag, G4, is documentation only.
- **Checking.**
  - Every lemma below was reviewed by one of two independent adversarial referee agents (AI agents, not human peer
    review) on 2026-10-18, or is kernel-checked in Lean, or both.
  - The referees found no false step in the arguments used. They did find a false theorem headline (a typo, §9.7),
    several wording fixes, and the 8-bit scan bug (§10.4).
  - The lattice-free counting is kernel-checked in Lean 4 for class 𝒞 and for the cone class. The lattice input
    (|𝒴_d| ≤ 2) is a hypothesis there.
  - The cylinder lemma, the Wall and Floor Lemmas, the height criterion, the two-face theorem and (FC) are not in Lean.
    The per-item status is in §12.
- **Priority.** A different, earlier, computer-assisted proof of the same theorem exists: K. Sethuraman, GitHub
  `kseth/wilf-e4`, September 2026. The overlap is described in §2.3.

---

## 1. Abstract

Let S be a numerical semigroup with multiplicity m and minimal generators m, p₁, p₂, p₃.

**The tile.** The graded-lexicographically least factorizations of the Apéry set Ap(S, m) over {p₁, p₂, p₃} form a
down-set D ⊂ ℕ³ with |D| = m. It is a fundamental domain of the lattice Λ = {x ∈ ℤ³ : Σ x_a p_a ≡ 0 (mod m)}.

**The height criterion.** A column identity, known from Zhai, writes mW + m(m − 1) as a sum of column deficits, where
W = e·ℓ − c. Bounding each deficit below by (m + 1) times the height of D above the column top gives the shape-only
inequality

    (m + 1)·H(D) ≤ mW + m(m − 1).

Since W is an integer, H(D) ≥ m − 2 already implies Wilf.

**Two-face tiles.** These are the tiles with e_a + e_b ∉ D for some pair a, b. They are handled by an exact identity,
four inequalities, the τ-criterion and the cited theorems (E1) and (E2).

**The other tiles.** Every other tile is either a Loomis–Whitney set (class 𝒞: a set cut out by its three coordinate
projections), or such a set minus one orthant q* + ℕ³ (the cone class). Write t for the number of maximal cells.
- A counting criterion reduces H ≥ m − 1 to the inequality 2t + 2|Tri| + |Q′| ≤ m + 1, where Tri is the set of tripod
  cells and Q′ the set of cells of total height 1.
- Elimination and forest arguments bound the left side by 5t − 3 on 𝒞.
- On cone tiles they bound it by 6t + 30. This step uses two lattice lemmas: a cone tile has at most two maxima under
  each face of the removed orthant.
- With t ≤ C ≤ 3/2 + √(6m − 15/4), where C is the number of corners of the three coordinate faces, the height
  criterion follows for 𝒞-tiles with m ≥ 130 and for cone tiles with m ≥ 280.

**The finite range.** The rest is a complete enumeration of the 3-D tiles, by facet flips in the Gröbner fan of each
lattice, with a per-lattice area certificate of completeness. For m ≥ 19, exactly four tiles fail the criterion
(m = 19, 20, 20, 23). The three at m = 19 and 20 are handled by a linear-programming certificate, and the one at m = 23
(δ = −1) by integrality. Failures with m ≤ 18 are covered by (E2).

**Coverage.** The enumeration covers every m ≤ 280, with a per-lattice area certificate for each m. Gap G1 (m = 236–255
missing), flagged in an earlier draft, is closed (E141; §10.7).

---

## 2. Introduction

### 2.1 The statement

A *numerical semigroup* is an additive submonoid S ⊆ ℕ = {0, 1, 2, …} with finite complement. For S ≠ ℕ:
- m = m(S) := min(S ∖ {0}) is the *multiplicity*;
- c = c(S) := min{c : n ∈ S for all n ≥ c} is the *conductor*, and F := c − 1 is the Frobenius number;
- g = g(S) := |ℕ ∖ S| is the *genus*;
- ℓ = ℓ(S) := |S ∩ [0, c)| = c − g is the number of *left elements*;
- e = e(S) is the *embedding dimension*, the number of minimal generators (atoms).

Wilf [Wil78] asked whether

    W(S) := e(S)·ℓ(S) − c(S) ≥ 0                                                       (Wilf)

holds for every S. (For S = ℕ, with c = 0 and ℓ = 0, it holds trivially. It does not arise here, because e = 4 forces
m ≥ 4, see Fact N5.)

**Theorem A.** Every numerical semigroup S with e(S) = 4 satisfies W(S) ≥ 0.

The proof is assembled in §11. The status is given at the top of the document.

### 2.2 Prior work used or related (exact citations; see `.research/LITERATURE.md`)

**Used as external results.** We do not reprove these.
- **[Eli18] (E1).** S. Eliahou, *Wilf's conjecture and Macaulay's theorem*, J. Eur. Math. Soc. 20 (2018) 2105–2129,
  arXiv:1703.01761. Thm 6.4 and Prop 6.2 give Cor 6.5: W₀(S) ≥ 0, and hence Wilf, whenever c ≤ 3m. The project read
  the paper (LITERATURE §1 #13).
- **[BGOW20] (E2).** W. Bruns, P. A. García-Sánchez, C. O'Neill, D. Wilburne, *Wilf's conjecture in fixed
  multiplicity*, Internat. J. Algebra Comput. 30 (2020) 861–882, arXiv:1903.04342. Thm 4.3: Wilf holds for every S with
  m ≤ 18. This is a computer-assisted proof (polyhedral geometry plus computation). The project read the paper
  (LITERATURE #25).

**Known results that this route re-derives or relies on in proved form.**
- **[Zhai11].** A. Zhai, arXiv:1111.2779 (2011).
  - Thm 1: e·ℓ ≥ c − (e − 2)(m − 1)/2. This is the project's "Corollary H".
  - Lemmas 1 and 3 are the column identity CH′ (Prop 3.2 below) in exact form.
  - We prove CH′ here, and it is also kernel-checked (§12). As reported by the 2026-10-18 audit agent, LITERATURE §3
    item 12.
- **[HRW18].** M. Hellus, A. Rechenauer, R. Waldi, arXiv:1804.06141 (2018). As reported by the same audit:
  - Prop 2.3/2.5: the lex factorization ideal is an initial ideal and tessellates.
  - Prop 2.6(b): at most one full-support minimal excluded point, and it lies in the lattice. This is our Cylinder
    Lemma 6.1(a).
  - Remark 2.9: Wilf for e = 4 when the ideal is the "double staircase" B_n, a two-face family.
- **[FGH87].** Wilf holds for e ≤ 3 (Fröberg–Gottlieb–Häggkvist; Dobbs–Matthews). Not used.
- **[Eli20, KS22].** These give 3e ≥ m ⇒ Wilf (Eliahou, Electron. J. Combin. 27(2) (2020) P2.15) and m ≤ 19 ⇒ Wilf
  (Kliem–Stump, Discrete Comput. Geom. 67 (2022) 1147–1173). Not used.

**The earlier complete proof for e = 4.**
- **[Set26].** K. Sethuraman, GitHub `kseth/wilf-e4`: https://github.com/kseth/wilf-e4, repository created 2026-09-18,
  commits 2026-09-11 to 2026-09-24, HEAD caa574d.
- It gives a complete computer-assisted proof of Wilf for e = 4, with no extra hypotheses (manuscript/introduction.tex
  lines 17–22). According to manuscript/construction.tex, the proof was generated with AI models.
- Method (LITERATURE §3 item 11):
  - the lex factorization ideal T (as in Zhai);
  - the identity m·W₄ = A·D₀ − m(m − 1);
  - a mass-transport lemma;
  - a final-window projection inequality m·W ≥ m·Φ(T, Z) + E(Z);
  - continuous κ-bounds with box thickening;
  - a case split by the unique full-support corner;
  - seven finite lemmas, each checked by two implementations (Python and C++).
- The project's audit (2026-10-18) traced the analytic steps and found no error. It reproduced Lemma 2.7. It did not
  verify Lemmas 2.2–2.6, 2.8, C.3.1 or C.4.1, and it did not run the repository's code.
- We treat [Set26] as a real result whose independent verification by us is partial.

**Other.** JC8267/wilf-multiplicity-23 (J. Collier, 2026-10-05) claims a computer-assisted proof of Wilf for m ≤ 23.
This is claimed and unchecked (LITERATURE §3 item 13). It is not used.

### 2.3 What is specific to this route, and how it relates to [Set26] and [HRW18]

The route below was developed in this project on 2026-10-17/18 (NOTEBOOK nights 12–17). The project found [Set26]
only on 2026-10-18 (NOTEBOOK "night 17, cont."; LITERATURE "search-scope failure").
- Links 1–5 of §2.4, the Wall and Floor Lemmas, and the cone lemmas TF-cone and F-cone all precede that entry in the
  NOTEBOOK. The exception is the integrality sharpening (Cor 4.3), which the referee added later the same day.
- The QF-pair, Location, Fiber and qO-cone lemmas (§9.6–9.7) come after it in the NOTEBOOK's order.
- The lead then read the foundational sections §2.1, 2.5, 2.7, 2.9 and 2.10 of Sethuraman's `manuscript/proof.tex`
  (LITERATURE §3 item 15).
- STATE.md records the project's position: "kseth/wilf-e4 … has a different, complete proof. We have read it; our
  argument is independent."

**Overlap with [Set26] and [HRW18]** (LITERATURE §3 items 12 and 15):
- The column identity CH′ (Prop 3.2). It is Zhai's Lemma 3, and Sethuraman also uses it.
- The "collision rules": a minimal excluded point and its representative have disjoint supports. Distinct ones that
  share a positive coordinate have distinct residues, so there is at most one full-support corner. These are our
  Cylinder Lemma 6.1(a), (b); (a) is [HRW18, Prop 2.6(b)].
- The decomposition T = U ∖ (p + ℕ³) of a tile into a finite "no-full-corner ideal" U minus one orthant
  (Sethuraman (p:11)). This is our cone class, with U = Cyl ∈ 𝒞 and p = q*.
- Sethuraman's Thm A.1.1 is a structure theorem for class 𝒞: every finite no-full-corner ideal is a central box plus at
  most three nonincreasing horns. We do not use it.
- Sethuraman §2.7 (for p = (1,1,1)): each coordinate plane has at most one mixed corner. This is the special case
  q* = (1,1,1) of our Wall Lemma 9.2. His (p:19) count of mixed corners is our Wall Lemma plus an antichain count.
- Sethuraman (p:20): |F_i ∩ F_j| ≤ 2·L_k for every tile, hence t ≤ 2 min_k L_k. It is new to the project, recorded in
  LITERATURE, and not used here.

**Ingredients of this route that do not occur in [Set26].** LITERATURE §3 item 15: "Not used by Sethuraman:
forest/elimination arguments, tripod/qO/qU graphs, LCL/PW, the height criterion HT." In detail:
- the height criterion (Theorem 4.2) and its integrality sharpening;
- the two-face theorem (Theorem 5.7);
- the counting criterion CHT and the type and corner bounds T, T′ and B;
- the forest and elimination lemmas S, P, TF, QF and F for 𝒞;
- their cone versions S′, P′, TF-cone, F-cone, QF-pair, Location, Fiber and qO-cone;
- the Floor Lemma;
- the finite computation, a complete Gröbner-fan enumeration of all 3-D tiles with an area certificate. Sethuraman
  instead checks seven targeted finite lemmas.

We also use the *graded* lex tile rather than the lex tile, because the Cross Lemma needs |n(u)| = shortest
factorization length.

Novelty is claimed only in the sense "not found in the sources searched" (LITERATURE).

### 2.4 Plan of the proof (the seven links of STATE.md)

Let S have e = 4 and multiplicity m. Let D = D(S) ⊂ ℕ³ be its graded-lex factorization tile, and put
δ(D) := H(D) − (m − 1).

1. **Link 1.** D is a down-set, |D| = m, and D is a fundamental domain of a lattice Λ ⊂ ℤ³ (Prop 3.1, Lemma 4.1). The
   column identity holds: mW + m(m − 1) = Σ (column deficits) (Prop 3.2).
2. **Link 2.** (m + 1)·H(D) ≤ mW + m(m − 1) (Theorem 4.2). Hence δ(D) ≥ −1 implies W ≥ 0 (Cor 4.3). Separately, a
   per-tile LP certificate proves W ≥ 0 for every S with a given tile (Prop 4.5).
3. **Link 3.** If D is two-face, then W ≥ 0 (Theorem 5.7; uses (E1), (E2), the τ-criterion and a finite check
   m ≤ 74).
4. **Link 4.** Otherwise D ∈ 𝒞, or D is a cone tile (Cor 6.5).
5. **Link 5.** If D ∈ 𝒞, then δ(D) ≥ m + 14 − 5C (Theorem 8.7), and this is ≥ −1 when m ≥ 130 (Cor 8.8).
6. **Link 6.** If D is a cone tile, then δ(D) ≥ m − 6C − 29 (Theorem 9.12), and this is ≥ −1 when m ≥ 280.
7. **Link 7.** The finite range is covered as follows.
   - m ≤ 18: (E2).
   - 19 ≤ m ≤ 279: the enumeration (§10) shows δ ≥ −1 for every non-two-face tile, except three tiles at m = 19 and 20.
     These are LP-certified.
   - The enumeration is area-certified for every m ≤ 280 (E140, E141). Gap G1 (m = 236–255), flagged in an earlier
     draft, is closed.

---

## 3. Notation and conventions

### 3.1 Numerical semigroups

Let S ≠ ℕ have multiplicity m. The *Apéry set* is Ap = Ap(S, m) := {w ∈ S : w − m ∉ S}. We use the following
standard facts. Proofs are included to keep the text self-contained (see also [RGS09, Ch. 2], [Sel77], [BS62]).

- **N1.** Ap has exactly one element w_i in each residue class i mod m, namely w_i = min{s ∈ S : s ≡ i (mod m)}.
  *Proof.* S is cofinite, so each class meets S; let w_i be its minimum. Then w_i − m ∉ S.
  If s ∈ S, s ≡ i and s > w_i, then s − m ≥ w_i and s − m ≡ w_i, so s − m = w_i + km ∈ S and s ∉ Ap. ∎
- **N2 (Selmer).** g = (1/m)·Σ_{w∈Ap} w − (m − 1)/2.
  *Proof.* The gaps in the class of w_i are w_i − m, w_i − 2m, …, down to the least nonnegative member i. There are
  (w_i − i)/m of them. Summing over i = 0, …, m − 1 gives the formula. ∎
- **N3 (Brauer–Shockley).** M := max Ap = F + m = c + m − 1.
  *Proof.* M − m ∉ S, because it lies below the minimum of its class. If n > M − m and n ≡ w_i, then n > w_i − m, so
  n ≥ w_i and n ∈ S. Hence F = M − m. ∎
- **N4 (summand closure).** If w ∈ Ap and w = x + y with x, y ∈ S, then x, y ∈ Ap.
  *Proof.* If x − m ∈ S, then w − m = (x − m) + y ∈ S. ∎
- **N5.** Let e = 4 and write the minimal generators as m < p₁, p₂, p₃ (up to order).
  - Each p_a lies in Ap. Otherwise p_a = m + (p_a − m) would be decomposable.
  - The residues r_a := p_a mod m are nonzero and pairwise distinct. If p_a ≡ 0 then p_a = km with k ≥ 2. If p_a ≡ p_b
    with p_a > p_b, then p_a = p_b + km. Both contradict minimality.
  - Hence p_a ≥ m + 1 and m ≥ 4.
  - Every w ∈ Ap is a sum of elements of P′ := {p₁, p₂, p₃}: write w as a sum of generators; if m occurred, then
    w − m ∈ S.
- **W for e = 4.** W = 4(c − g) − c = 3c − 4g. By N2 and N3:

      mW = 3m(M − m + 1) − 4Σ_{w∈Ap} w + 2m(m − 1) = 3mM − 4Σ_{w∈Ap} w − m(m − 1).            (3.1)

The letter c denotes the conductor in §§3–5, 10 and 11. In §§6–9, where the conductor does not occur, {a, b, c} denotes
the three coordinate directions.

### 3.2 Lattice-point conventions

- ℕ³ ⊂ ℤ³, with unit vectors e₁, e₂, e₃.
- For x ∈ ℕ³, |x| := x₁ + x₂ + x₃, and x ≤ y means coordinatewise.
- pr_c : ℤ³ → ℤ³ sets coordinate c to 0.
- A *down-set* is a finite D ⊂ ℕ³ such that x ∈ D, x′ ∈ ℕ³ and x′ ≤ x imply x′ ∈ D. In §§3–11, "D" always denotes a
  nonempty down-set.

For a down-set D, a direction a and a cell x ∈ D:
- **Columns and tops.** The *a-column* through x is D ∩ (x + ℤe_a) = {x + k e_a : −x_a ≤ k ≤ s}, where
  s := max{s ≥ 0 : x + s e_a ∈ D}. Its *top* is top_a(x) := x + s e_a. A column starts at coordinate 0 in its direction,
  so its length is top_a(x)_a + 1. The a-columns partition D.
- **Maximal cells.** Max(D) := {y ∈ D : y + e_a ∉ D for a = 1, 2, 3}, and t = t(D) := |Max(D)|.
- **Height.** ht(y) := max{|z| − |y| : z ∈ D, z ≥ y} for y ∈ D. We have ht(y) = 0 iff y ∈ Max(D): if z ∈ D, z ≥ y and
  z ≠ y, then y + e_a ≤ z for some a, so y + e_a ∈ D.
- **Faces.** The *face* A_c := D ∩ {x_c = 0} is a 2-D down-set in the coordinates {a, b} = {1, 2, 3} ∖ {c}. Since D is a
  down-set, pr_c(D) = A_c.
- **Arms.** L_c := |D ∩ ℕe_c| is the length of the c-axis of D.

For a 2-D down-set A in coordinates (a, b):
- its *corners* (outer corners) are its maximal elements, cor(A);
- a (non-axis) *inner corner* is a point w ∉ A with w_a, w_b ≥ 1 and w − e_a, w − e_b ∈ A;
- the standard staircase fact: a nonempty A with k corners has exactly k − 1 inner corners, one between each pair of
  consecutive corners;
- if A = {u_b < f(u_a)} with f nonincreasing, then |cor(A)| is the number of distinct values of f.

**Corner count.** k_c := |cor(A_c)| and C = C(D) := k₁ + k₂ + k₃.

**Binomials.** binom(n, 2) := n(n − 1)/2. The letter C is reserved for the corner count.

### 3.3 The factorization tile (link 1) and the column identity

Let ≺ be the graded lexicographic order on ℕ³: x ≺ y iff |x| < |y|, or |x| = |y| and x precedes y lexicographically.
- It is a monomial order: a well-order, compatible with addition (x ≺ y ⇒ x + z ≺ y + z), with 0 minimal.
- Put p := (p₁, p₂, p₃) and w(x) := p·x = Σ_a x_a p_a.
- For w ∈ Ap let n(w) be the ≺-least x ∈ ℕ³ with w(x) = w. It exists by N5.
- Define D = D(S) := {n(w) : w ∈ Ap}.

**Proposition 3.1 (link 1).** Let S have e = 4.
- (a) |D| = m. The map x ↦ w(x) is a bijection D → Ap, and ρ(x) := r·x mod m (r = p mod m) is a bijection D → ℤ/m.
- (b) D is a down-set.
- (c) e_a ∈ D for a = 1, 2, 3.
- (d) |n(w)| = min{|x| : x ∈ ℕ³, w(x) = w}. This is the shortest factorization length ℓ(w) of w over P′.
- (e) M = max_{x∈D} w(x).

*Proof.*
- (a) w ↦ n(w) is injective, with inverse x ↦ w(x). By N1, |Ap| = m, and the elements of Ap are pairwise incongruent
  mod m. Also w(x) ≡ r·x (mod m).
- (b) Let x = n(w), x′ ∈ ℕ³ with x′ ≤ x, and w′ := w(x′). Then w = w′ + w(x − x′) with both summands in S, so w′ ∈ Ap
  by N4.
  If n(w′) ≠ x′, there is x″ ≺ x′ with w(x″) = w′. Then x″ + (x − x′) ≺ x and w(x″ + x − x′) = w, which contradicts
  the minimality of x. So x′ = n(w′) ∈ D.
- (c) p_a ∈ Ap by N5. Since p_a is an atom, e_a is its only factorization over P′. So n(p_a) = e_a.
- (d) ≺ compares degrees first.
- (e) Follows from (a). ∎

*Source and status.* PROOFS "Factorization down-set D and the column identity CH′"; reviewed (chain referee, link 1).
Lean: `isFactTile_factDownSetG` (D is a down-set and `S.wt` is a bijection D → Ap) and `IsFactTile.isTile` (D is a
down-set, |D| = m, and the residue map is bijective), in `lean/Wilf/MaxCL.lean`. Item (c) is not in Lean.
(`TileReduction.lean`'s `isTile_factDownSet` concerns the *lex* tile; it is not the one used here.)

**Proposition 3.2 (column identity CH′, e = 4).**

    Σ_{x∈D} Σ_{a=1}^{3} (M − w(top_a(x))) = mW + m(m − 1).                                      (CH′)

Equivalently, Σ_a Σ_{a-columns K} |K|·(M − w(top K)) = mW + m(m − 1). Every term is ≥ 0, by Prop 3.1(e).

*Proof.* Let K = {b, b + e_a, …, b + (L − 1)e_a} be an a-column, with b_a = 0. Then

    Σ_{x∈K} (w(x) + p_a x_a) = Σ_{k<L} (w(b) + 2k p_a) = L·(w(b) + (L − 1)p_a) = |K|·w(top K).

Sum over the a-columns, then over a, and use Σ_a p_a x_a = w(x):

    Σ_a Σ_K |K|·w(top K) = 3Σ_D w + Σ_D w = 4Σ_{w∈Ap} w.

There are 3m incidences (x, a). So the left side of (CH′) equals 3mM − 4Σ_{Ap} w, which is mW + m(m − 1) by (3.1). ∎

*Source and status.*
- KNOWN: [Zhai11, Lemmas 1 and 3].
- PROOFS "CH′"; reviewed (chain referee).
- Lean: `IsFactTile.columnIdentity` (`lean/Wilf/MaxCL.lean`), stated for any factorization tile. It reads
  Σ_a Σ_{x∈D, x+e_a∉D} (x_a + 1)(M − w(x)) = mW + (e − 2)·binom(m, 2).

### 3.4 Worked examples (convention check; computed with a scratch script, not part of the proof)

| S | m | c | g | ℓ | W | tile | t | C | H | δ |
|---|---|---|---|---|---|---|---|---|---|---|
| ⟨4, 5, 6, 7⟩ | 4 | 4 | 3 | 1 | 0 | two-face | 3 | 6 | 0 | −3 |
| ⟨8, 9, 10, 11⟩ | 8 | 24 | 12 | 12 | 24 | two-face | 3 | 6 | 11 | 4 |
| ⟨36, 37, 42, 43⟩ | 36 | 180 | 125 | 55 | 40 | two-face (box family) | 11 | 14 | 40 | 5 |
| ⟨19, 20, 25, 27⟩ | 19 | 69 | 45 | 24 | 27 | 𝒞 (no q*) | 7 | 10 | 14 | −4 |
| ⟨23, 25, 28, 35⟩ | 23 | 91 | 62 | 29 | 25 | cone, q* = (3, 1, 1) | 8 | 10 | 21 | −1 |

- In every row the script asserted the following: N2 and N3; that D is a down-set with |D| = m; (CH′); and Theorem 4.2.
- ⟨4, 5, 6, 7⟩ is the boundary case W = 0.
- ⟨19, 20, 25, 27⟩ has residues r = (1, 6, 8), which is the lattice of the unique m = 19 HT failure of the scan
  (`logs/tile_scan_H.log`). It is covered by the LP certificate of Prop 4.5.
- ⟨23, 25, 28, 35⟩ lies on the lattice (1, 4, 10), after multiplying by the unit 2. Its tile has δ = −1, and the scan
  lists exactly one HT failure at m = 23, on that lattice. It is covered by Cor 4.3.

---

## 4. Reduction to tiles and the height criterion (links 1 and 2)

### 4.1 Lattice tiles

**Definition 4.0.** A *(3-D) lattice tile* is a down-set D ⊂ ℕ³ together with a lattice Λ ⊆ ℤ³ such that the
translates D + λ (λ ∈ Λ) are pairwise disjoint and cover ℤ³. Equivalently, D is a complete set of representatives of
ℤ³/Λ, and m := |D| = [ℤ³ : Λ].
- For x ∈ ℤ³, rep(x) ∈ D denotes the unique element with x − rep(x) ∈ Λ.
- 𝒢(D) denotes the finite set of minimal elements of ℕ³ ∖ D. Since D is a down-set,
  ℕ³ ∖ D = ⋃_{q∈𝒢(D)} (q + ℕ³).

**Lemma 4.1.** Let S have e = 4, D = D(S), and Λ = Λ_S := {x ∈ ℤ³ : r·x ≡ 0 (mod m)}.
- (a) (D, Λ) is a lattice tile, and [ℤ³ : Λ] = m.
- (b) (closed-cone inequality) For every x ∈ ℕ³, w(x) ≥ w(rep(x)), and w(rep(x)) is the Apéry element in the residue
  class of w(x). In particular p·(q − rep(q)) ≥ 0 for every q ∈ 𝒢(D).

*Proof.*
- (a) ρ : ℤ³ → ℤ/m, x ↦ r·x mod m, is a homomorphism, and its restriction to D is bijective (Prop 3.1(a)). So ρ is
  onto, Λ = ker ρ has index m, and D is a transversal of ℤ³/Λ.
- (b) w(x) ∈ S, and w(x) ≡ r·x ≡ r·rep(x) ≡ w(rep(x)) (mod m). By Prop 3.1(a) and N1, w(rep(x)) ∈ Ap is the least
  element of S in that class. ∎

*Status.* Paper; reviewed (chain referee, link 1). Lean's `IsTile` (down-set, |D| = m, residue map bijective) is
equivalent to (a), but the translate formulation and (b) are not formalized.

### 4.2 The height criterion

For a down-set D ⊂ ℕ³ with |D| = m, put

    H(D) := Σ_{x∈D} Σ_{a=1}^{3} ht(top_a(x)),        δ(D) := H(D) − (m − 1).

We say *HT holds* for D if δ(D) ≥ 0.

**Theorem 4.2 (height criterion).** Let S have e = 4 and D = D(S). Then

    (m + 1)·H(D) ≤ mW(S) + m(m − 1).

*Proof.* Fix an incidence (x, a), put y := top_a(x), and let z ∈ D with z ≥ y. By Prop 3.1(e), M ≥ w(z). Since
z − y ∈ ℕ³ and every p_a ≥ m + 1 (N5),

    w(z) − w(y) = p·(z − y) ≥ (m + 1)|z − y|.

Hence M − w(y) ≥ (m + 1)·ht(y). Summing over the 3m incidences and using (CH′) gives the claim. ∎

*Source and status.* NOTEBOOK "2026-10-18 (night 13, cont.)" ("Height criterion (PROVED, elementary, any e = 4)").
Reviewed (chain referee, link 2), and asserted on about 50,000 e = 4 semigroups by the referee. Not in Lean.

**Corollary 4.3 (integrality sharpening).**
- If δ(D(S)) ≥ −1, i.e. H(D) ≥ m − 2, then W(S) ≥ 0.
- If δ(D(S)) ≥ 0, then W(S) ≥ 1.

*Proof.* By Theorem 4.2, mW ≥ (m + 1)H − m(m − 1).
- If H ≥ m − 2, then mW ≥ (m + 1)(m − 2) − m(m − 1) = −2. So W ≥ −2/m > −1, because m ≥ 4. As W ∈ ℤ, W ≥ 0.
- If H ≥ m − 1, then mW ≥ m − 1 > 0, so W ≥ 1. ∎

*Source.* Proposed by the chain referee (2026-10-18) and checked by the lead (STATE link 2; PROOFS, paragraph after
Theorem C-HT).

### 4.3 The per-tile LP certificate

For a lattice tile (D, Λ), put Tops(D) := Σ_{x∈D} Σ_a top_a(x) ∈ ℕ³. For π ∈ ℝ³_{≥0}, define

    M_D(π) := max_{x∈D} π·x,      Def_D(π) := 3m·M_D(π) − π·Tops(D)  (≥ 0, since every top lies in D),

    C̄_D := {π ∈ ℝ³_{≥0} : π·(q − rep(q)) ≥ 0 for all q ∈ 𝒢(D)}          (closed cone of D),

    κ_D := inf { Def_D(π) / min_a π_a : π ∈ C̄_D, π₁ + π₂ + π₃ = 1, min_a π_a > 0 }.

**Proposition 4.5 (LP certificate).** Let S have e = 4 and tile D = D(S). If (m + 1)·κ_D ≥ m(m − 1), then W(S) ≥ 0.

*Proof.* By Lemma 4.1(b), p ∈ C̄_D. By Prop 3.1(e), M_D(p) = M, so

    Def_D(p) = 3mM − Σ_{(x,a)} w(top_a x) = mW + m(m − 1)

by (CH′). Def_D is positively homogeneous of degree 1. Hence Def_D(p) ≥ κ_D·min_a p_a ≥ (m + 1)κ_D ≥ m(m − 1),
because κ_D ≥ 0 and min_a p_a ≥ m + 1. So mW ≥ 0. ∎

*Computing κ_D.*
- Def_D is convex, since M_D is a maximum of linear functions, and the maximum may be taken over Max(D) because π ≥ 0.
- Consider the arrangement formed by the lines {π·x = π·x′ : x, x′ ∈ Max(D)}, the lines {π_a = π_b}, and the edges of
  the polygon C̄_D ∩ {Σπ_a = 1}. On each of its cells, Def_D(π)/min_a π_a is linear-fractional. So the minimum over the
  polygon is attained at a vertex of the arrangement.
- `src/tile_lp.py` enumerates these vertices in exact rational arithmetic.
- The chain referee recomputed κ by a different method (three LPs in HiGHS, with its own cone constraints) for every
  realizable failing pair (D, r). It reproduced the logged values:

| m | κ_D | (m + 1)κ_D vs m(m − 1) |
|---|---|---|
| 8 | 4 | 36 < 56 (fails) |
| 15 | 15 | — |
| 16 | 22.67; 28 | — |
| 17 | 23.33; 26 | — |
| 19 | 32.5 | 650 ≥ 342 |
| 20 | 33.33; 44.5 | 700 ≥ 380; 934.5 ≥ 380 |
| 23 | 40 | — |

- m = 8 fails, and it is covered by (E2).
- In the proof of Theorem A the certificate is needed only at m = 19 (one tile) and m = 20 (two tiles). For m ≤ 18,
  (E2) applies. At m = 23, δ = −1, so Cor 4.3 applies.

*Status.* Paper (docstring of `src/tile_lp.py`; NOTEBOOK "night 13, late"); reviewed ("LP certificate (tile_lp.py):
sound"); computational. Not in Lean, because Lean lacks the closed-cone inequality.

---

## 5. Two-face tiles (link 3)

### 5.1 The top layer and the τ-criterion for e = 4

Let X := Ap ∩ [c, c + m). By N3 this equals Ap ∩ [c, ∞). Put τ := |X|, and π(u) := u − c + 1 ∈ [1, m] for u ∈ X.
We identify u ∈ X with its cell n(u) ∈ D, and define

    P₂ := #{ {u, u′} ⊆ X : n(u) and n(u′) differ in exactly two coordinates }.

**Lemma 5.1 (top layer).**
- (a) Every u ∈ X is a maximal cell of D.
- (b) (TOP″ ⇒ Wilf, e = 4) If Σ_{u∈X} π(u)·(ℓ(u) + 3) ≤ m(2m + 1), then W ≥ 0.

*Proof.*
- (a) w(n(u) + e_a) = u + p_a ≥ c + m + 1 > M, so n(u) + e_a ∉ D by Prop 3.1(e).
- (b) In (CH′), group the 3m incidences (x, a) by their top y = top_a(x).
  - If y = n(u) with u ∈ X, then y is maximal. So it is the top of its a-column for every a, and that column has
    length y_a + 1. Thus y carries Σ_a (y_a + 1) = ℓ(u) + 3 incidences (Prop 3.1(d)), each with deficit M − u = m − π(u).
  - Every other top y has w(y) ∈ Ap ∖ X, so w(y) ≤ c − 1 and its deficit is ≥ m.
  - Hence mW + m(m − 1) ≥ m(3m − Σ_u (ℓ(u) + 3)) + Σ_u (ℓ(u) + 3)(m − π(u)) = 3m² − Σ_u π(u)(ℓ(u) + 3).
  - Under the hypothesis, mW ≥ 3m² − m(2m + 1) − m(m − 1) = 0. ∎

*Source and status.* This is "Lemma A + TOP″ ⇒ Wilf" of PROOFS at d = 3, where m((d + 1)m + d − 1)/2 = m(2m + 1).
- Lean `wilf_of_TOP2` (`lean/Wilf/Chains.lean`) proves it via the chain identity CH.
- The argument above is the specialization to the graded-lex tile of the Tile-TOP″ argument, Lean
  `wilf_of_tileTOPAt_of_isFactTile` (`lean/Wilf/MaxCL.lean`, `TileTop.lean`).

**Lemma 5.2 (Cross Lemma).** Σ_{u∈X} (ℓ(u) + 1) ≤ m + P₂.

*Proof.* For y ∈ D, put cross(y) := {y − k e_a : a = 1, 2, 3, 0 ≤ k ≤ y_a}. It has |y| + 1 cells and lies in [0, y] ⊆ D.

Let u ≠ u′ in X, with y = n(u) and y′ = n(u′), and let z ∈ cross(y) ∩ cross(y′), say z = y − k e_a = y′ − k′ e_b.
- If a = b, or k = 0, or k′ = 0, then y and y′ lie on one coordinate line. Say y′ = y + j e_d with j ≥ 1. Then
  u′ = u + j p_d ≥ c + m + 1 > M, a contradiction.
- Hence a ≠ b and k, k′ ≥ 1. Then y and y′ differ exactly in coordinates a and b, and z is determined by the pair
  (z_a = y′_a, z_b = y_b, third coordinate common).

So two crosses meet in at most one cell, and only for a pair counted in P₂. With j(z) := #{u ∈ X : z ∈ cross(n(u))},

    Σ_u (ℓ(u) + 1) = Σ_z j(z) = |⋃ crosses| + Σ_z (j(z) − 1)⁺ ≤ m + Σ_z binom(j(z), 2) ≤ m + P₂. ∎

*Source and status.* PROOFS "τ-criterion". The line there "u′ = u + j·n_a" should read p_a (Appendix A). Lean:
`crossLemma_two_mul_P2` (`lean/Wilf/TauCrit.lean`); `topPairs2` counts ordered pairs, so it equals 2P₂.

**Corollary 5.3 (τ-criterion, e = 4).** If 2τ + P₂ ≤ m + 1, then W ≥ 0. In particular this holds if
τ(τ + 3)/2 ≤ m + 1.

*Proof.* Since π(u) ≤ m, Lemma 5.2 gives

    Σ_u π(u)(ℓ(u) + 3) ≤ m·Σ_u (ℓ(u) + 1 + 2) ≤ m(m + P₂ + 2τ) ≤ m(2m + 1).

Apply Lemma 5.1(b). The second statement uses P₂ ≤ binom(τ, 2). ∎

*Status.* Lean: `wilf_of_tauCriterion_P2`. Its hypothesis 2(e − 2)τ + 2P₂ ≤ (e − 2)(m + 1) reads 2τ + P₂ ≤ m + 1 for
e = 4.

### 5.2 Structure of two-face tiles and the two-face identity

**Definition.** D is *two-face* if e_a + e_b ∉ D for some a ≠ b; otherwise D is *non-two-face*. In this section we
relabel so that e₁ + e₂ ∉ D. (The statements are symmetric in the labelling of p₁, p₂, p₃.)
- Since D is a down-set, D ∩ {x₁ ≥ 1, x₂ ≥ 1} = ∅. So D = F₁ ∪ F₂, where F₁ := D ∩ {x₂ = 0} and F₂ := D ∩ {x₁ = 0}.
- F₁ ∩ F₂ = axis := {k e₃ : 0 ≤ k < L₃}.
- Put N_i := F_i ∖ axis. Then |N₁| + |N₂| = m − L₃.
- A_top := w((L₃ − 1)e₃) = (L₃ − 1)p₃ is the value of the axis top.

The *2-D runs* are:
- the 1-columns of D through F₁ ("rows of F₁");
- the 2-columns through F₂ ("rows of F₂");
- all 3-columns.

Every other column of D is a singleton. The 1-column through x ∈ N₂ is {x}, because x + e₁ has x₁ = 1 and x₂ ≥ 1.
Likewise the 2-column through x ∈ N₁ is {x}.
- The total run length is |F₁| + |F₂| + m = 2m + L₃.
- A cell of N₁ ∪ N₂ lies in exactly two runs, and an axis cell in three.
- Def2D := Σ_{runs R} |R|·(M − w(end R)), where end R is the top of R. Def2D′ is the same sum without the axis
  3-column.

**Lemma 5.4 (two-face identity).**

    3mW + 3m(m − 1) = (m − 4L₃)·M + 4·Def2D + 2p₃L₃(L₃ − 1) = m·M + 4·Def2D′ − 2p₃L₃(L₃ − 1).

*Proof.* For each run R in direction d, Σ_{x∈R} (w(x) + p_d x_d) = |R|·w(end R) (the AP sum of Prop 3.2). Sum over all
runs.
- Σ_R Σ_{x∈R} w(x) = 2Σ_D w + Σ_axis w.
- Σ_R Σ_{x∈R} p_d x_d = Σ_D w. For x ∈ N₁ the two runs give p₁x₁ + p₃x₃ = w(x), and similarly on N₂; on the axis the
  three runs give 0 + 0 + p₃x₃ = w(x).
- Hence 3Σ_D w + Σ_axis w = (2m + L₃)M − Def2D, with Σ_axis w = p₃L₃(L₃ − 1)/2.

By (3.1), 3(mW + m(m − 1)) = 9mM − 4·3Σ_D w. Substituting gives the first form. For the second form, use
Def2D = Def2D′ + L₃(M − A_top). ∎

(Remark from the record: algebraically this is CH′ rewritten. Its content is that the singleton columns make each face
"two-dimensional", with mean ≈ (2/3)·max rather than (3/4)·max.)

### 5.3 Combinatorial facts

Put x₁ := |X ∩ N₁| and x₂ := |X ∩ N₂|, and x_ax := 1 if the axis top (L₃ − 1)e₃ lies in X, else 0. Let η_i (i = 1, 2)
be the number of cells of the 3-column over e_i.

**Lemma 5.5.**
- (F1) X ⊆ Max(D) ∩ (N₁ ∪ N₂ ∪ {(L₃ − 1)e₃}), and τ = x₁ + x₂ + x_ax. The cells of X ∩ N_i are corners of the 2-D
  down-set F_i, with pairwise distinct heights x₃. Moreover x_i(x_i + 1)/2 ≤ |N_i| and x_i ≤ L₃ − x_ax.
- (F2) A cell u ∈ X ∩ N_i ends exactly two runs, of total length |u| + 2. If the axis top is in X, it ends three runs
  of total length L₃ + 2. Two of these, of total length 2, are not the axis column.
- (F3) Σ_{u∈X∩N_i} (|u| + 2) ≤ |N_i| + 2x_i + binom(x_i, 2).
- (F4) A run whose end has w < c has deficit ≥ m. A run ending at u ∈ X has deficit m − π(u). The numbers m − π(u),
  u ∈ X, are distinct integers in [0, m − 1].
- (F5) P₂ ≤ binom(x₁, 2) + binom(x₂, 2) + x_ax(x₁ + x₂) + min(x₁, x₂).
- Also 1 ≤ η_i ≤ L₃ and η₁ + η₂ ≤ m − L₃.

*Proof.*
- **(F1).**
  - X ⊆ Max by Lemma 5.1(a). The only maximal axis cell is the axis top, and 0 ∉ X.
  - A maximal cell of N₁ satisfies x + e₁, x + e₃ ∉ D, so it is a corner of F₁ in the coordinates (1, 3), with first
    coordinate ≥ 1. Corners of a 2-D down-set have distinct coordinates in each direction.
  - Order the corners in X ∩ N₁ as (i_j, 0, k_j) with 1 ≤ i₁ < ⋯ < i_{x₁} and k₁ > ⋯ > k_{x₁} ≥ 0. The 3-column over
    (i_j, 0) lies in N₁ and has ≥ k_j + 1 ≥ x₁ − j + 1 cells. Summing gives x₁(x₁ + 1)/2 ≤ |N₁|.
  - The heights lie in [0, L₃ − 1]. If x_ax = 1, the axis top is maximal, so (1, 0, L₃ − 1) ∉ D and no cell of N₁ has
    height L₃ − 1. Hence x₁ ≤ L₃ − x_ax.
  - The same argument applies to N₂.
- **(F2).** A maximal u = (i, 0, k) ∈ N₁ ends its row of F₁ (length i + 1) and its 3-column (length k + 1). Its
  2-column is a singleton, not a run. The axis top ends its rows in F₁ and in F₂ (length 1 each) and the axis column
  (length L₃).
- **(F3).**
  - For u = (i, 0, k) ∈ X ∩ N₁, let cr(u) be the row of F₁ through u, together with the 3-column through u, minus the
    axis cell (0, 0, k). It has i + k = |u| cells, all in N₁.
  - Let u = (i, 0, k) and u′ = (i′, 0, k′) with i < i′ and k > k′. Their rows are disjoint and their columns are
    disjoint. The row of u′ meets the column of u in (i, 0, k′) ∈ N₁. The row of u meets the column of u′ only in
    (i′, 0, k), which is ∉ D because u is a corner.
  - A cell common to two such sets fixes the column of one and the row of the other, so it lies in at most two of them.
  - Hence Σ|u| ≤ |N₁| + binom(x₁, 2). Add 2x₁.
- **(F4).** M = c + m − 1. If w(end) ≤ c − 1 the deficit is ≥ m. If the end is u ∈ X, the deficit is M − u = m − π(u),
  and distinct u give distinct π(u).
- **(F5).**
  - Pairs inside N₁ number ≤ binom(x₁, 2), pairs inside N₂ ≤ binom(x₂, 2), and pairs with the axis top ≤ x_ax(x₁ + x₂).
  - A cross pair (i, 0, k) ∈ N₁, (0, j, k′) ∈ N₂ (i, j ≥ 1) differs in coordinates 1 and 2, and also in coordinate 3
    unless k = k′. Heights are distinct within each face, so at most min(x₁, x₂) cross pairs count.
- **(η).** e_i ∈ D (Prop 3.1(c)) gives η_i ≥ 1. The down-set property gives η_i ≤ L₃. The columns over e₁ and e₂ are
  disjoint subsets of N₁ and N₂. ∎

### 5.4 Four bounds

**Lemma 5.6.** Let D be two-face (e₁ + e₂ ∉ D). Each of the following four conditions implies W ≥ 0.
- **(A′)** Assume c > 3m and 4L₃ ≤ m. The condition is

      4m(m − 4L₃) + 2(m + 1)L₃(L₃ − 1) + 4Δ_A ≥ 3m(m − 1),

  where Δ_A := max(0, m(m + 2L₃ − 2(x₁ + x₂) − binom(x₁, 2) − binom(x₂, 2) − x_ax(L₃ + 2))) + 3·binom(τ, 2).
- **(B″)** Assume m ≥ 2L₃. The condition is

      (L₃ − 1)(m + 1)(m − 2L₃) + 4Δ_B ≥ 3m(m − 1),

  where Δ_B := max(0, m(m + L₃ − 2(x₁ + x₂) − binom(x₁, 2) − binom(x₂, 2) − 2x_ax)) + 2·binom(τ, 2).
- **(C)** 2τ + binom(x₁, 2) + binom(x₂, 2) + x_ax(x₁ + x₂) + min(x₁, x₂) ≤ m + 1.
- **(D)** G ≥ 0 and (m + 1)·G ≥ 3m(m − 1), where

      G := m(L₃ − 1) − 2L₃(L₃ − 1) + 2σ(η₁) + 2σ(η₂),   σ(η) := (L₃ − η)(L₃ − η − 1).

*Proof.*
- **(A′).** First, Def2D ≥ Δ_A.
  - The runs have total length 2m + L₃.
  - Let R_X be the total length of the runs ending in X. By (F2) and (F3),
    R_X ≤ Σ_A := m − L₃ + 2(x₁ + x₂) + binom(x₁, 2) + binom(x₂, 2) + x_ax(L₃ + 2).
  - By (F4), the runs ending below c contribute ≥ m(2m + L₃ − R_X) ≥ max(0, m(2m + L₃ − Σ_A)).
  - A cell u ∈ X ends runs of total length R(u) ≥ 3, each with deficit m − π(u). So
    Σ_u R(u)(m − π(u)) ≥ 3(0 + 1 + ⋯ + (τ − 1)) = 3·binom(τ, 2), by (F4).

  Now use the first form of Lemma 5.4.
  - c ≥ 3m + 1 gives M ≥ 4m. With m − 4L₃ ≥ 0, this gives (m − 4L₃)M ≥ 4m(m − 4L₃).
  - p₃ ≥ m + 1 (N5).
  - So 3mW + 3m(m − 1) ≥ 4m(m − 4L₃) + 2(m + 1)L₃(L₃ − 1) + 4Δ_A ≥ 3m(m − 1).
- **(B″).**
  - The runs other than the axis column have total length 2m.
  - Those ending in X have total length ≤ m − L₃ + 2(x₁ + x₂) + binom(x₁, 2) + binom(x₂, 2) + 2x_ax.
  - Each u ∈ X ends such runs of total length ≥ 2. As in (A′), this gives Def2D′ ≥ Δ_B.
  - Second form of Lemma 5.4: M ≥ A_top = (L₃ − 1)p₃ and m ≥ 2L₃ give
    mM − 2p₃L₃(L₃ − 1) ≥ (L₃ − 1)p₃(m − 2L₃) ≥ (L₃ − 1)(m + 1)(m − 2L₃).
- **(C).** By (F5), 2τ + P₂ is at most the left side of (C). Apply Cor 5.3.
- **(D).**
  - For η₁ ≤ k ≤ L₃ − 1 we have (1, 0, k) ∉ D. So the row of F₁ at height k is the single axis cell k e₃, a run of
    length 1 with deficit M − kp₃ ≥ A_top − kp₃ = (L₃ − 1 − k)p₃.
  - Σ_{k=η₁}^{L₃−1} (L₃ − 1 − k) = σ(η₁)/2. The same holds for F₂. These rows are distinct runs, and none of them is the
    axis column. Hence 4·Def2D′ ≥ 2p₃(σ(η₁) + σ(η₂)).
  - The second form of Lemma 5.4 with M ≥ (L₃ − 1)p₃ gives 3mW + 3m(m − 1) ≥ p₃·G.
  - If G ≥ 0, then p₃G ≥ (m + 1)G ≥ 3m(m − 1). ∎

### 5.5 The two-face theorem

**Theorem 5.7 (two-face, e = 4).** Every S with e = 4 whose tile D(S) is two-face satisfies W(S) ≥ 0.

*Proof.* If c ≤ 3m, (E1) applies. If m ≤ 18, (E2) applies. So assume m ≥ 19 and c > 3m.
- 2 ≤ L₃ ≤ m − 2, because e₃ ∈ D and e₁, e₂ ∈ D lie off the axis.
- Call a tuple (x₁, x₂, x_ax, η₁, η₂) *feasible* if x_ax ∈ {0, 1}, x_i ≤ L₃ − x_ax, x₁(x₁ + 1)/2 + x₂(x₂ + 1)/2 ≤ m − L₃,
  1 ≤ η_i ≤ L₃ and η₁ + η₂ ≤ m − L₃. The tuple of S is feasible by Lemma 5.5.
- It suffices to show: **for every (m, L₃) with m ≥ 18 and 2 ≤ L₃ ≤ m − 2, one of (A′) (if 4L₃ ≤ m), (B″) (if
  2L₃ ≤ m), (C), (D) holds for all feasible tuples.** This is a strictly stronger statement than "for each tuple, some
  bound". Lemma 5.6 then gives W ≥ 0.

**Case 18 ≤ m ≤ 74: exact finite check.**
- `src/scratch/tf_bounds2.py` performs a pure integer computation in (m, L₃, x, η), with no semigroup enumeration.
  For m ≥ 18 it finds no uncovered (m, L₃). The uncovered pairs, all with m ≤ 17, are listed in `logs/tf_bounds2.log`.
- PROOFS records the check for 18 ≤ m ≤ 400. The chain referee reran it independently (`src/review2/tf_check.py`,
  5 ≤ m ≤ 500, both quantifier forms) and got the same uncovered list.
- [GAP G4 (documentation only): `logs/tf_bounds2.log` does not record the range that was run. It records only "largest
  uncovered m in range: 17".]

**Case m ≥ 75: analytic.**
- **(I) L₃ ≤ m/4. Use (A′), with Δ_A ≥ 0.**

      4m(m − 4L₃) + 2(m + 1)L₃(L₃ − 1) − 3m(m − 1) = m(m + 2L₃² − 18L₃ + 3) + 2L₃(L₃ − 1) ≥ m(m − 37) ≥ 0,

  since 2L₃² − 18L₃ ≥ −40 for integers L₃. (PROOFS says "m ≥ 38" here. The sharp value is 37, as the referee notes.
  Both suffice.)
- **(II) m/4 < L₃ ≤ m/2 − 4. Use (B″), with Δ_B ≥ 0.**
  - We need f(L₃) := (L₃ − 1)(m + 1)(m − 2L₃) ≥ 3m(m − 1). Here m ≥ 2L₃ holds.
  - f is a concave quadratic in L₃, so it suffices to check the endpoints of the real interval [m/4, m/2 − 4].
  - At L₃ = m/4 the condition reads m² − 27m + 20 ≥ 0, which holds for m ≥ 27.
  - At L₃ = m/2 − 4 it reads m² − 33m − 40 ≥ 0, which holds for m ≥ 35.
  - (PROOFS gives the endpoints as "28 and 35", the referee as "27 and 35".)
- **(III) L₃ > m/2 − 4. Use (C).**
  - Put cap := m − L₃ < m/2 + 4 and s := x₁ + x₂.
  - Feasibility gives binom(x₁, 2) + binom(x₂, 2) ≤ cap − s and x₁² + x₂² ≤ 2·cap. So s ≤ 2√cap.
  - With x_ax ≤ 1 and min(x₁, x₂) ≤ s/2, the left side of (C) is ≤ 2(s + 1) + (cap − s) + s + s/2 = cap + 2.5s + 2
    ≤ cap + 5√cap + 2.
  - This is increasing in cap. At cap = y := m/2 + 4 it is ≤ m + 1 iff y − 5√y − 9 ≥ 0, i.e. √y ≥ (5 + √61)/2, i.e.
    m ≥ 74.06. ∎

*Scope (from the record).*
- The class contains the box family ⟨a², a² + 1, a² + a, a² + a + 1⟩, on which the τ-criterion fails. Example:
  ⟨36, 37, 42, 43⟩ in §3.4.
- 36,279 of the e = 4 semigroups with m ≤ 18 and generators < 4m are two-face.

*Source and status.*
- PROOFS "THEOREM (two-face e = 4)"; NOTEBOOK "2026-10-18 (night 13)".
- Reviewed (chain referee, link 3). The referee re-derived the identity, F1–F5, the bounds A′, B″, C and D with their
  max(0, ·) relaxations and hypotheses, the feasibility superset and the analytic tail.
- The referee asserted the inequalities on about 16,800 random two-face semigroups and on all 1,555 two-face e = 4
  semigroups of genus ≤ 20. Each one's actual tuple was covered.
- The project asserted every intermediate inequality on 26,779 two-face semigroups (`src/scratch/tf_verify.py`).
- Not in Lean, except Cor 5.3.

---

## 6. Cylinder structure of 3-D lattice tiles (link 4)

In §§6–9, {a, b, c} = {1, 2, 3} denotes the three coordinate directions.

**Lemma 6.1 (cylinder lemma).** Let (D, Λ) be a lattice tile.
- (a) At most one q ∈ 𝒢(D) has full support (q ≥ (1, 1, 1)). If q* is such an element, then q* ∈ Λ.
- (b) Let q ∈ 𝒢(D) with q_c = 0 < q_a, q_b. Then q ≡ μ e_c (mod Λ) for a unique μ with μ e_c ∈ D, i.e.
  0 ≤ μ ≤ L_c − 1, and distinct such q (for the same c) have distinct μ. Consequently every non-axis inner corner w of
  the face A_c (viewed as a point with w_c = 0) lies in 𝒢(D) and has a *multiplier* μ_w ∈ [0, L_c) with w ≡ μ_w e_c.
  Distinct corners have distinct multipliers, and A_c has at most L_c non-axis inner corners.
- (c) D = Cyl ∖ (q* + ℕ³), where Cyl := {x ∈ ℕ³ : pr_c(x) ∈ D for c = 1, 2, 3}. If there is no q*, read q* + ℕ³ as ∅.

*Proof.* Let q ∈ 𝒢(D). Then q ∉ D, so q ∈ D + λ for a unique λ ∈ Λ, and λ ≠ 0.
- For each a with q_a ≥ 1, minimality gives q − e_a ∈ D. Since the translates are disjoint, q − e_a ∉ D + λ, i.e.
  q − λ − e_a ∉ D.
- As q − λ ∈ D and D is a down-set, this forces (q − λ)_a = 0. Hence q − λ ∈ D, and its support is disjoint from that
  of q.

Now the three parts.
- (a) If q has full support, then q − λ = 0, so q ∈ Λ. If q ≠ q′ both had full support, then q − e₁ and q′ − e₁ would
  be distinct elements of D whose difference q − q′ lies in Λ. Impossible.
- (b) q − λ ∈ D is supported in {c}, so q − λ = μ e_c ∈ D. If q ≠ q′ had the same μ, then q − q′ ∈ Λ, and q − e_a,
  q′ − e_a ∈ D would be distinct and congruent. For an inner corner w: w ∉ D, w − e_a and w − e_b lie in D, and w has
  no c-predecessor. So w ∈ 𝒢(D).
- (c) x ∉ D iff x ≥ q for some q ∈ 𝒢(D).
  - Suppose q_c = 0. If x ≥ q, then pr_c(x) ≥ q = pr_c(q) ∉ D, so pr_c(x) ∉ D because D is a down-set.
  - Conversely, if pr_c(x) ∉ D then x ∉ D, because pr_c(x) ≤ x.
  - Every q ∈ 𝒢(D) other than q* has a zero coordinate. ∎

*Source and status.*
- PROOFS "Cylinder structure of 3-D tiles".
- Part (a) is KNOWN, [HRW18, Prop 2.6(b)]. The collision rules behind (a) and (b) also appear in [Set26]
  (LITERATURE §3 item 15).
- Reviewed (chain referee, link 4), and checked on all 3-D tiles with m ≤ 12 (`src/scratch/cylinder.py`).
- Not in Lean.

**Definition 6.2 (class 𝒞, Loomis–Whitney sets).** A set D ⊂ ℕ³ is in 𝒞 if there are an integer L₁ ≥ 1 and
nonincreasing functions h : [0, L₁) → ℤ_{≥1}, F : [0, L₁) → ℤ_{≥1} and G : [0, h(0)) → ℤ_{≥1}, with F(0) = G(0), such that

    D = {x ∈ ℕ³ : x₁ < L₁, x₂ < h(x₁), x₃ < min(F(x₁), G(x₂))}.

Then:
- L₂ = h(0) and L₃ = F(0) = G(0);
- the faces are A₃ = {x₂ < h(x₁)}, A₂ = {x₃ < F(x₁)} and A₁ = {x₃ < G(x₂)};
- k₃, k₂ and k₁ are the numbers of distinct values of h, F and G.

In Lean this is the structure `LWClass` (0-based coordinates).

**Lemma 6.3 (𝒞 = projection-determined down-sets).** A nonempty down-set D is in 𝒞 iff

    (∗)  for all z ∈ ℕ³:  z ∈ D  ⟺  pr₁(z), pr₂(z), pr₃(z) ∈ D.

Condition (∗) is symmetric in the coordinates. So 𝒞 is invariant under permutations of coordinates, and every D ∈ 𝒞
has a description as in Def 6.2 with any coordinate as the "vertical" one.

*Proof.*
- (⇒) Since h, F, G ≥ 1 and F(x₁) ≤ F(0) = G(0) ≥ G(x₂), we get (x₁, x₂, 0) ∈ D ⟺ x₂ < h(x₁) (with x₁ < L₁),
  (x₁, 0, x₃) ∈ D ⟺ x₃ < F(x₁), and (0, x₂, x₃) ∈ D ⟺ x₃ < G(x₂). The defining condition of D is then exactly
  pr₃(x) ∈ A₃ ∧ pr₂(x) ∈ A₂ ∧ pr₁(x) ∈ A₁.
- (⇐) The faces are 2-D down-sets. Write them as A₃ = {x₂ < h(x₁)} and A₂ = {x₃ < F(x₁)} on the common 1-arm
  [0, L₁), and A₁ = {x₃ < G(x₂)} on [0, L₂). Then F(0) = G(0) = L₃ and h(0) = L₂, and (∗) is the formula of Def 6.2. ∎

*Status.* Lean `LWClass.isLW` (`lean/Wilf/Forest.lean`) proves (⇒). The Lean predicate `IsLW` is "down-set and (∗)";
the Forest and ConeForest results are stated for `IsLW` sets.

**Definition 6.4 (cone class, cone tiles).**
- D is in the *cone class* if D = Cyl ∖ K with Cyl ∈ 𝒞, K = q + ℕ³, q ≥ (1, 1, 1) and q ∈ Cyl.
- Such a D is a down-set, because Cyl is a down-set and K is an up-set.
- K misses the coordinate planes, so the faces of D equal those of Cyl. Hence k_c, C and L_c agree for D and Cyl.
- A *cone tile* is a lattice tile in the cone class. For a cone tile, q ∈ 𝒢(D): we have q ∉ D, and q − e_a lies in Cyl
  but not in K. So q has full support, and q = q* ∈ Λ by Lemma 6.1(a).

**Corollary 6.5 (link 4).** Every lattice tile is in 𝒞 or is a cone tile. Every two-face tile is in 𝒞.

*Proof.*
- Cyl is a finite down-set and satisfies (∗): if pr_c(z) ∈ Cyl, then pr_c(z) = pr_c(pr_c(z)) ∈ D. So Cyl ∈ 𝒞 by
  Lemma 6.3.
- If there is no q*, then D = Cyl.
- Otherwise D = Cyl ∖ (q* + ℕ³) with q* ≥ (1, 1, 1). Also q* ∈ Cyl, since pr_c(q*) ≤ q* − e_c ∈ D for each c.
- If e_a + e_b ∉ D, no full-support q can be minimal in ℕ³ ∖ D, because q ≥ e_a + e_b and q ≠ e_a + e_b. ∎

*Status.* Reviewed (chain referee: "the dichotomy is exhaustive"; the classification was asserted on every tested tile:
24,707 in 𝒞, 8,734 cone, 0 other).

---

## 7. The counting criterion and the corner and type bounds

### 7.1 The counting criterion CHT

Let D ⊂ ℕ³ be a finite down-set, m = |D|. Define:
- hs(x) := Σ_a ht(top_a(x)) for x ∈ D, so that H(D) = Σ_{x∈D} hs(x);
- N(x) := #{a : top_a(x) ∈ Max(D)};
- Tri := {x ∈ D ∖ Max : N(x) = 3}, the *tripods*;
- Q′ := {x ∈ D : N(x) = 2 and hs(x) = 1}. For x ∈ Q′, its *non-maximal direction* is the unique c with
  top_c(x) ∉ Max;
- qU := {x ∈ Q′ : top_c(x) = x}, and qO := Q′ ∖ qU;
- LHS(D) := 2t + 2|Tri| + |Q′| = 2t + 2|Tri| + |qU| + |qO|.

**Lemma 7.1 (CHT).** δ(D) ≥ m + 1 − LHS(D).

*Proof.*
- δ(D) = H(D) − m + 1 = 1 + Σ_{x∈D} (hs(x) − 1), and each hs(x) is a nonnegative integer.
- By §3.2, ht(y) = 0 ⟺ y ∈ Max. So hs(x) = 0 ⟺ N(x) = 3. A maximal x has all three tops equal to x. Hence
  {hs = 0} = Max ⊔ Tri.
- hs(x) = 1 iff one top has ht 1 and the other two have ht 0, i.e. iff x ∈ Q′.
- Therefore δ ≥ 1 − (t + |Tri|) + (m − t − |Tri| − |Q′|). ∎

*Status.* Lean `cht` (`lean/Wilf/CornerArea.lean`): 2|D| ≤ H + 2t + 2|Tri| + |Q′| for every finite D ⊆ ℕ³; the
down-set hypothesis is not needed there. Reviewed (both referees).

**Lemma 7.2 (structure of Tri, qU, qO).**
- (a) If x ∈ Tri ∪ qO, then x + e_d ∈ D for d = 1, 2, 3.
- (b) If x ∈ qU has non-maximal direction c, then x + e_c ∉ D and x + e_a, x + e_b ∈ Max.
- (c) If x ∈ Q′ has non-maximal direction c, then ht(top_c(x)) = 1.

*Proof.* Cells of Tri ∪ Q′ are not maximal.
- (a) A maximal top of a non-maximal x is ≠ x, so x + e_d ∈ D in that direction. For qO, the non-maximal top is ≠ x by
  definition.
- (c) hs(x) = 1, and the two maximal tops have ht 0.
- (b) top_c(x) = x gives x + e_c ∉ D, and ht(x) = 1 by (c). Write top_a(x) = x + s e_a. Then s ≥ 1, since otherwise x
  would be maximal. And s ≤ 1, since otherwise ht(x) ≥ 2. So top_a(x) = x + e_a ∈ Max. The same holds for b. ∎

*Status.* Lean `qU_struct`, `triSet_succ_mem`, `qO_succ_mem` (`Forest.lean`).

### 7.2 The level picture for class 𝒞

Let D ∈ 𝒞, with data (h, F, G) as in Def 6.2, and A₃ = {p ∈ ℕ² : p₁ < L₁, p₂ < h(p₁)}.
- For p ∈ A₃, φ(p) := min(F(p₁), G(p₂)). Then D = {(p, z) : p ∈ A₃, 0 ≤ z < φ(p)}, and φ ≥ 1 is nonincreasing on A₃.
- For v ≥ 1:
  - a_v := #{i < L₁ : F(i) ≥ v} and b_v := #{j < L₂ : G(j) ≥ v};
  - R_v := [0, a_v) × [0, b_v);
  - U_v := {p ∈ A₃ : φ(p) ≥ v}.

**Lemma 7.3 (level picture).**
- (i) U_v = A₃ ∩ R_v, U₁ = A₃, U_{L₃+1} = ∅ and U_{v+1} = U_v ∩ R_{v+1}. Also (p, v − 1) ∈ D ⟺ p ∈ U_v.
- (ii) (p, v − 1) ∈ Max(D) ⟺ p ∈ cor(U_v) ∖ U_{v+1}. Put M_v := cor(U_v) ∖ U_{v+1}; then t = Σ_{v=1}^{L₃} |M_v|.
- (iii) Let p ∈ cor(U_{v+1}) ∖ cor(U_v). Then either p is the top cell of column a_{v+1} − 1 of U_{v+1} and
  a_{v+1} < a_v, or p is the last cell of row b_{v+1} − 1 of U_{v+1} and b_{v+1} < b_v. Hence
  ν_v := |cor(U_{v+1}) ∖ cor(U_v)| ≤ [a_{v+1} < a_v] + [b_{v+1} < b_v].

*Proof.*
- (i) Since F is nonincreasing, F(p₁) ≥ v ⟺ p₁ < a_v; the same holds for G. Also φ ≥ 1 on A₃ and φ ≤ F(0) = L₃.
- (ii) (p, v − 1) + e₃ ∈ D ⟺ p ∈ U_{v+1}, and (p, v − 1) + e_i ∈ D ⟺ p + e_i ∈ U_v for i = 1, 2.
- (iii)
  - p ∈ U_{v+1} ⊆ U_v is not a corner of U_v, so p + e₁ ∈ U_v or p + e₂ ∈ U_v. That neighbour is ∉ U_{v+1}, because p
    is a corner of U_{v+1}.
  - If p + e₁ ∈ U_v ∖ U_{v+1}, then p + e₁ ∉ R_{v+1} while p ∈ R_{v+1}, so p₁ = a_{v+1} − 1. Also p + e₁ ∈ U_v ⊆ R_v,
    so a_{v+1} < a_v. Since p + e₂ ∉ U_{v+1}, p is the top of its column. Such a p is unique.
  - The case of e₂ is symmetric. ∎

### 7.3 The type bounds

**Lemma 7.4 (Lemma T).** If D ∈ 𝒞, then t ≤ C − 2.

*Proof.*
- U_{v+1} ⊆ U_v, so a corner of U_v lying in U_{v+1} is a corner of U_{v+1}. Hence
  |M_v| = |cor(U_v)| − |cor(U_{v+1})| + ν_v.
- Sum over v = 1, …, L₃, using U_{L₃+1} = ∅ (so ν_{L₃} = 0): t = |cor(A₃)| + Σ_{v=1}^{L₃−1} ν_v.
- a_{v+1} < a_v iff v is a value of F. The values of F lie in [1, L₃], and L₃ = F(0) is one of them. So
  Σ_{v<L₃} [a_{v+1} < a_v] ≤ k₂ − 1. Similarly Σ_{v<L₃} [b_{v+1} < b_v] ≤ k₁ − 1, using the values of G.
- With |cor(A₃)| = k₃: t ≤ k₃ + (k₂ − 1) + (k₁ − 1) = C − 2. ∎

*Status.*
- Lean `typeBound` (`CornerArea.lean`): t + 2 ≤ C on `LWClass`. The Lean proof is a different one: an explicit
  injection of Max into the face corners with two exceptional corners removed.
- Tight for boxes. Exhaustively, max(t − C) = −2 for every |D| ≤ 40 (E125).
- Reviewed.

**Lemma 7.5 (Lemma T′, cone class).** Let D = Cyl ∖ (q + ℕ³) with Cyl ∈ 𝒞 and q ≥ (1, 1, 1); q ∈ Cyl is not needed.
Then t(D) ≤ C(D).

*Proof.* Let Quad := [q₁, ∞) × [q₂, ∞).
- If q₃ ≥ L₃, then D = Cyl and Lemma 7.4 applies. So assume q₃ < L₃.
- The slices U_v := {p : (p, v − 1) ∈ D} are U_v = A₃ ∩ R_v for v ≤ q₃, and U_v = (A₃ ∩ R_v) ∖ Quad for v ≥ q₃ + 1.
- They are nested 2-D down-sets. Lemma 7.3(ii) holds verbatim, because maximality is computed inside D, and so does
  the telescoping identity of Lemma 7.4.
- For v ≠ q₃ we still have U_{v+1} = U_v ∩ R_{v+1} and U_v ⊆ R_v, so Lemma 7.3(iii) holds.
- For v = q₃ we have U_{v+1} = (U_v ∩ R_{v+1}) ∖ Quad. Let p be a new corner with p + e₁ ∈ U_v ∖ U_{v+1}. Either
  p + e₁ ∉ R_{v+1}, as before, or p + e₁ ∈ Quad ∌ p. The second case forces p₁ = q₁ − 1 and p₂ ≥ q₂, and then p is the
  top cell of column q₁ − 1 of U_{v+1}. The case of e₂ is symmetric: the last cell of row q₂ − 1.
- So ν_{q₃} ≤ [a drop] + [b drop] + 2. Since the faces of D are those of Cyl, the drop count is as in Lemma 7.4.
  Hence t ≤ C. ∎

*Status.*
- Lean `typeBound_cone` and `typeBound_cone'` (`lean/Wilf/ConeType.lean`). Also `faceCorners_coneCut` (the faces are
  unchanged) and `typeBound_cone_attained` (t = C = 3 for [0, 2)³ with q = (1, 1, 1)).
- Exhaustively, max(t − C) = 0, attained, for union ≤ 34. Reviewed (cone referee).

### 7.4 The corner–area bound

**Lemma 7.6 (Lemma B).** For every nonempty down-set D ⊂ ℕ³ with m = |D|: C² − 3C + 6 ≤ 6m. Equivalently,

    C ≤ C_max(m) := ⌊3/2 + √(6m − 15/4)⌋.

(For integers C ≥ 0, the two forms are equivalent, because the roots of C² − 3C + 6 − 6m are (3 ± √(24m − 15))/2 and
the smaller one is ≤ 0.)

*Proof.*
- The three faces lie in D. Pairwise they meet in the axes, and all three meet in {0}. So

      m ≥ |A₁ ∪ A₂ ∪ A₃| = Σ_c |A_c| − (L₁ + L₂ + L₃) + 1.

- Let A be a 2-D down-set with k ≥ 1 corners and arms (axis lengths) L and L′.
  - A contains its two arms, which have L + L′ − 1 cells.
  - List the corners by increasing first coordinate. Corner number s (1 ≤ s ≤ k) has coordinates ≥ (s − 1, k − s).
  - So A contains the triangle {(u, w) : u, w ≥ 1, u + w ≤ k − 1}: the point (u, w) lies below corner number u + 1.
  - The triangle avoids the arms and has T(k) := (k − 1)(k − 2)/2 cells.
  - Hence |A| ≥ L + L′ − 1 + T(k).
- Applying this to the three faces: m ≥ 2ΣL − 3 + Σ_c T(k_c) − ΣL + 1 = ΣL − 2 + Σ_c T(k_c).
- The corners of a face have distinct coordinates, so L₁ ≥ k₃, L₂ ≥ k₁ and L₃ ≥ k₂. Hence ΣL ≥ C.
- T is a convex real quadratic. By Jensen, Σ T(k_c) ≥ 3T(C/3) = (C − 3)(C − 6)/6.
- So 6m ≥ 6C − 12 + (C − 3)(C − 6) = C² − 3C + 6. ∎

*Status.*
- Lean `cornerArea` (`CornerArea.lean`): C² + 6 ≤ 6|D| + 3C for every nonempty finite down-set D ⊆ ℕ³.
- Equality holds for D = {0} and for D = {0, e₁, e₂, e₃}. The bound is tight for three staircase faces with
  q = (1, 1, 1), e.g. (5, 4, 3, 2, 1)³ with m = 31.
- The lemma applies to the cone class directly, because D is a down-set with the faces of Cyl. Reviewed (both
  referees).

---

## 8. Forest lemmas and Theorem C-HT (link 5)

Throughout this section D ∈ 𝒞. By Lemma 6.3, each statement proved for one labelling of the coordinates holds for all
labellings. The notions Max, Tri, qU and qO are equivariant under coordinate permutations.

**Lemma 8.1 ((P0) and (P1)).** Use the vertical direction 3, as in §7.2. For p ∈ A₃ put
Π(p) := {p′ ∈ A₃ : p′ ≥ p, φ(p′) = φ(p)} (the *plateau* of p) and γ(p) := max_{p′∈Π(p)} |p′ − p|.
- **(P0)** For (p, z) ∈ D: top₃(p, z) = (p, φ(p) − 1) and ht(top₃(p, z)) = γ(p). Hence top₃(p, z) ∈ Max ⟺ γ(p) = 0,
  and we then call p a *peak*.
  - If γ(p) = 0 and p + e₁ ∈ A₃, then F(p₁ + 1) < G(p₂) (and F(p₁ + 1) < F(p₁)).
  - If γ(p) = 0 and p + e₂ ∈ A₃, then G(p₂ + 1) < F(p₁).
- **(P1)** If p″ ≤ p in A₃ and φ(p″) = φ(p), then Π(p) ⊆ Π(p″), so γ(p″) ≥ |p − p″| + γ(p).

*Proof.*
- **(P0), the top and its height.** Let y = (p, φ(p) − 1), and let z′ = (p′, z″) ∈ D with z′ ≥ y. Then p′ ≥ p and
  φ(p) − 1 ≤ z″ < φ(p′) ≤ φ(p). So z″ = φ(p) − 1 and p′ ∈ Π(p), and |z′| − |y| = |p′ − p|.
- **(P0), the peak inequalities.** If γ(p) = 0 then p + e₁ ∉ Π(p), so φ(p + e₁) < φ(p). Here
  φ(p + e₁) = min(F(p₁ + 1), G(p₂)). If F(p₁ + 1) ≥ G(p₂), then φ(p + e₁) = G(p₂) ≥ φ(p), a contradiction. So
  F(p₁ + 1) < G(p₂), and φ(p + e₁) = F(p₁ + 1) < φ(p) ≤ F(p₁). The case of e₂ is symmetric.
- **(P1)** For p′ ∈ Π(p): p′ ≥ p ≥ p″, φ(p′) = φ(p″), and |p′ − p″| = |p′ − p| + |p − p″|. ∎

**Lemma 8.2 (Lemma S, sharing).** Let x, x′ ∈ D with x + e_d, x′ + e_d ∈ D for all d. If top_a(x) = top_b(x′) = y ∈ Max,
then a = b. Hence x and x′ lie on the a-line through y.

*Proof.* Suppose a ≠ b, and let c be the third direction. Then x = y − i e_a and x′ = y − i′ e_b, and x + e_c,
x′ + e_c ∈ D. We have:
- pr_a(y + e_c) = pr_a(x + e_c) ∈ D;
- pr_b(y + e_c) = pr_b(x′ + e_c) ∈ D;
- pr_c(y + e_c) = pr_c(y) ∈ D.

By (∗), y + e_c ∈ D, which contradicts y ∈ Max. ∎ (Lean `lemmaS`, for `IsLW` sets.)

**Lemma 8.3 (Lemma P, projection chain).** Let x, x′ be tripods and a ≠ b. It is impossible that x_a < x′_a and
x_b > x′_b.

*Proof.* Take (a, b) = (1, 2) and write p = (X, Y) and p′ = (X′, Y′) for the projections, with X < X′ and Y > Y′.
- Both p and p′ are peaks, since top₃ is maximal.
- p + e₁ ∈ A₃ because x + e₁ ∈ D, and p′ + e₂ ∈ A₃ because x′ + e₂ ∈ D (Lemma 7.2(a)).
- By (P0), F(X + 1) < G(Y) and G(Y′ + 1) < F(X′).
- By monotonicity, F(X′) ≤ F(X + 1) < G(Y) ≤ G(Y′ + 1) < F(X′), a contradiction. ∎ (Lean `lemmaP`.)

**Lemma 8.4 (Lemma TF, tripod forest).** 2|Tri| + 1 ≤ t.

*Proof.* List the tripods by decreasing |x|.
- Suppose a tripod x shares one of its tops with an earlier tripod x′. By Lemmas 7.2(a) and 8.2, they share it as
  top_a for one direction a, and x′ lies on the a-line through x.
- Since |x′| ≥ |x| and x′ ≠ x, we get x′ = x + i e_a with i ≥ 1.
- If this happened for two directions a ≠ b, with x′ = x + i e_a and x″ = x + i′ e_b, then x″_a < x′_a and x″_b > x′_b,
  which contradicts Lemma 8.3.
- So at most one of the three distinct tops of x is a top of an earlier tripod. The first tripod contributes 3 new
  maxima and each later one at least 2.
- Hence t ≥ 2|Tri| + 1 if Tri ≠ ∅. If Tri = ∅ the claim is trivial, since t ≥ 1. ∎

*Status.* Lean `tripodForest`, `tripodForest'` and `tripodForest''`.

**Lemma 8.5 (Lemma QF, qO forest).** |qO| + 1 ≤ t.

*Proof.* List the qO cells by increasing |x|. By Lemmas 7.2(a) and 8.2, an earlier qO cell sharing the maximal top
top_a(x) shares it as top_a, so it is x − i e_a with i ≥ 1. We claim this cannot happen for both maximal directions of
x. Then each qO cell brings at least one new maximum and the first brings two, so |qO| + 1 ≤ t.

By symmetry, let the non-maximal direction of x be 3, so that its maximal tops are top₁ and top₂. Write x = (p, z) with
p = (X, Y). Then γ(p) = 1, by Lemma 7.2(c) and (P0), and p + e₁, p + e₂ ∈ A₃.

(1) Suppose x′ = x − i e₁ (i ≥ 1) is a qO cell with top₁(x′) = top₁(x). Then F(X) < G(Y). Its non-maximal direction c′
is 2 or 3, because top₁(x′) ∈ Max. Put p′ = p − i e₁.
- c′ = 2: then top₃(x′) ∈ Max, so γ(p′) = 0. Since p′ + e₁ ≤ p ∈ A₃, (P0) gives F(X − i + 1) < G(Y), and
  F(X) ≤ F(X − i + 1).
- c′ = 3: then γ(p′) = 1. If φ(p′) = φ(p), then (P1) would give γ(p′) ≥ i + 1 ≥ 2. So φ(p′) > φ(p), i.e.
  min(F(X − i), G(Y)) > min(F(X), G(Y)). This is impossible if F(X) ≥ G(Y). So F(X) < G(Y).

(2) Symmetrically, if x″ = x − i′ e₂ is a qO cell with top₂(x″) = top₂(x), then G(Y) < F(X).

(1) and (2) are incompatible. ∎

*Status.* Lean `qOForest`.

**Lemma 8.6 (Lemma F, qU forest).** |qU| + 1 ≤ t.

*Proof.* Let G_U be the graph on Max with one edge {x + e_a, x + e_b} for each x ∈ qU, where c is the non-maximal
direction of x (Lemma 7.2(b)). This graph is simple: an unordered pair {y, y′} with y − y′ = e_a − e_b determines
x = y − e_a. We show that G_U is a forest; then |qU| ≤ t − 1.

Use the level picture (direction 3) and classify the edges by c.
- **c = 3.** Here x = (p, v − 1) with p + e₁, p + e₂ ∈ M_v and p ∉ U_{v+1}. The edge joins two corners of U_v that
  differ by e₁ − e₂ ("consecutive corners with unit steps"), and their *notch* p is not in U_{v+1}.
- **c = 1.**
  - Here x + e₁ ∉ D, x + e₂ = (p + e₂, v − 1) ∈ Max and x + e₃ = (p, v) ∈ Max. So p ∈ M_{v+1}, p + e₂ ∈ M_v and
    p + e₁ ∉ U_v.
  - Since p + e₂ ∈ U_v ∖ U_{v+1} = U_v ∖ R_{v+1} and p ∈ R_{v+1}, we get p₂ = b_{v+1} − 1. Thus p is the corner of
    U_{v+1} in its top row, i.e. the *leftmost* corner p_L of U_{v+1}.
  - So between levels v and v + 1 there is at most one such edge e_L = {p_L + e₂ (level v), p_L (level v + 1)}.
- **c = 2.** Symmetrically, there is at most one edge e_R = {p_R + e₁, p_R}, where p_R is the *rightmost* corner of
  U_{v+1}.

Build G_U from the top level down.
- Assume the levels above v span a forest. Add level v: the vertices M_v, the c = 3 edges inside M_v, then e_L and e_R.
- Along the staircase each corner has at most one c = 3 neighbour on each side, so the c = 3 edges inside M_v form
  disjoint paths.
- Adding e_L attaches one path to the old forest, so it creates no cycle.
- Adding e_R creates a cycle only if its lower end p_R + e₁ lies on the same c = 3 path as the lower end p_L + e₂ of
  e_L. Suppose it does.
  - Along a c = 3 path, consecutive vertices differ by ±(e₁ − e₂). So x₁ increases by one exactly when x₂ decreases by
    one.
  - The vertex p_L + e₂ has x₂ = b_{v+1} and x₁ ≤ a_{v+1} − 1. The vertex p_R + e₁ has x₁ = a_{v+1} and
    x₂ ≤ b_{v+1} − 1.
  - Every path vertex lies in M_v, which is disjoint from U_{v+1} = U_v ∩ R_{v+1}, so it lies outside R_{v+1}: it has
    x₁ ≥ a_{v+1} or x₂ ≥ b_{v+1}.
  - Walk from p_L + e₂ to p_R + e₁, and look at the step where x₁ first reaches a_{v+1}. It goes from (a_{v+1} − 1, s)
    to (a_{v+1}, s − 1), and s ≥ b_{v+1} because the first vertex lies outside R_{v+1}.
    - If s = b_{v+1}: the notch of this pair is (a_{v+1} − 1, b_{v+1} − 1) ∈ U_v ∩ R_{v+1} = U_{v+1}, so this pair is
      not a c = 3 edge. Contradiction.
    - If s ≥ b_{v+1} + 1: the vertex (a_{v+1}, s − 1) ≥ (a_{v+1}, b_{v+1}) lies in U_v. Then R_{v+1} ⊆ U_v, so
      U_{v+1} = R_{v+1}, whose only corner is p_L = (a_{v+1} − 1, b_{v+1} − 1). But then p_L + e₁ ∈ U_v, so e_L does
      not exist. Contradiction. ∎

*Remarks.* The record (PROOFS, Lemma F) states the two crossing cases s = b_{v+1} and s > b_{v+1}. The case where the
walk passes through a vertex inside R_{v+1} is excluded by M_v ∩ U_{v+1} = ∅. We spell out this third case here; it is
a completion of the exposition, not a gap.

*Status.* Lean `qUForest`, with a different short proof: an explicit injection qU → Max ∖ {y*}. Reviewed.

**Theorem 8.7 (Theorem C-HT).** For every D ∈ 𝒞 with m = |D|:

    LHS(D) ≤ 5t − 3 ≤ 5C − 13,       δ(D) ≥ m + 14 − 5C.

*Proof.*
- LHS = 2t + 2|Tri| + |qU| + |qO| ≤ 2t + 3(t − 1), by Lemmas 8.4, 8.6 and 8.5.
- t ≤ C − 2 by Lemma 7.4, so LHS ≤ 5C − 13.
- Lemma 7.1 then gives δ ≥ m + 1 − LHS ≥ m + 14 − 5C. ∎

*Status.* Lean `forestBound` (LHS + 3 ≤ 5t), `chtForest` and **`deltaBound`** (2m + 13 ≤ H + 5C). Reviewed.

**Corollary 8.8 (threshold for 𝒞).** For D ∈ 𝒞 with m = |D|: δ(D) ≥ 0 if m ≥ 131, and δ(D) ≥ −1 if m ≥ 130.

*Proof.* By Theorem 8.7 and Lemma 7.6, δ ≥ m + 14 − 5·C_max(m).
- **Large m.** For m ≥ 160, C_max(m) ≤ 3/2 + √(6m), so 5C_max ≤ 15/2 + 5√(6m) ≤ m + 14. Indeed, m − 5√(6m) + 13/2 is
  increasing for m > 37.5 and positive at m = 160 (≈ 11.6).
- **Small m.** For 130 ≤ m ≤ 159, C_max(m) is 29 on [127, 135], 30 on [136, 145], 31 on [146, 155] and 32 on
  [156, 165]. So 5C_max(m) ≤ m + 14 for 131 ≤ m ≤ 159 (equality at m = 131 and m = 136), and 5C_max(130) = 145 = 130 + 15.
- **Exact check.** The project and the referee also checked the inequality exactly for 131 ≤ m ≤ 2·10⁵. I rechecked it
  for m ≤ 10⁶. ∎

*Status.* Lean `chtThreshold` and `chtThreshold'` (`lean/Wilf/ConeForest.lean`, with `nlinarith`). The last m with
5C_max(m) > m + 14 is 130, and the last with 5C_max(m) > m + 15 is 129.

---

## 9. Cone tiles (link 6)

### 9.1 Setting and notation

D = Cyl ∖ K is in the cone class: Cyl ∈ 𝒞 with data (h, F, G) (vertical direction 3), K = q + ℕ³, q ≥ (1, 1, 1),
q ∈ Cyl.
- Quad := {p ∈ ℕ² : p₁ ≥ q₁, p₂ ≥ q₂}, and Q(p) := q₃ if p ∈ Quad, Q(p) := ∞ otherwise.
- ψ(p) := min(F(p₁), G(p₂), Q(p)) for p ∈ A₃. Then

      D = {(p, z) : p ∈ A₃, 0 ≤ z < ψ(p)}.

  ψ ≥ 1 on A₃ (because q₃ ≥ 1), and ψ is nonincreasing (because Quad is an up-set).
- 𝒴_d := {y ∈ Max(D) : y + e_d ∈ K} for d = 1, 2, 3, and 𝒴 := 𝒴₁ ∪ 𝒴₂ ∪ 𝒴₃. (The record writes Y_d and Y.)
- B_c := {x ∈ ℕ³ : x_a ≥ q_a, x_b ≥ q_b, x_c < q_c}, the cells directly under K in direction c.
- Symmetry: permuting coordinates maps the cone class to itself, with q permuted (Lemma 6.3). Every statement below
  is invariant, so each is proved for one labelling: non-maximal direction 3, "partner" direction 1, third
  direction 2. *Mirror* means swapping coordinates 1 and 2.

**Lemma 9.1 ((P0′), (P1′), (Peak′)).** For p ∈ A₃ put Π′(p) := {p′ ∈ A₃ : p′ ≥ p, ψ(p′) = ψ(p)} and
γ(p) := max_{p′∈Π′(p)} |p′ − p|.
- **(P0′)** top₃(p, z) = (p, ψ(p) − 1), and ht(top₃(p, z)) = γ(p).
- **(P1′)** If p″ ≤ p and ψ(p″) = ψ(p), then γ(p″) ≥ |p − p″| + γ(p).
- **(Peak′)** If p + e₁ ∈ A₃ and γ(p) = 0, then either F(p₁ + 1) < G(p₂), or [p₁ + 1 = q₁, p₂ ≥ q₂, ψ(p) ≥ q₃ + 1 and
  top₃(p, ·) + e₁ ∈ K]. Mirror: if p + e₂ ∈ A₃ and γ(p) = 0, then either G(p₂ + 1) < F(p₁), or [p₂ + 1 = q₂, p₁ ≥ q₁ and
  top₃(p, ·) + e₂ ∈ K].

*Proof.*
- (P0′) and (P1′) are the proofs of (P0) and (P1) with ψ in place of φ. They use only that ψ is nonincreasing.
- (Peak′):
  - γ(p) = 0 forces ψ(p + e₁) < ψ(p).
  - Suppose F(p₁ + 1) ≥ G(p₂). Then ψ(p + e₁) = min(G(p₂), Q(p + e₁)) and ψ(p) ≤ G(p₂). So
    min(G(p₂), Q(p + e₁)) < ψ(p) ≤ G(p₂), which forces Q(p + e₁) = q₃ < ψ(p) ≤ Q(p).
  - Hence p + e₁ ∈ Quad ∌ p, i.e. p₁ + 1 = q₁ and p₂ ≥ q₂.
  - Also ψ(p) − 1 ≥ q₃, so top₃(p, ·) + e₁ = (p + e₁, ψ(p) − 1) ∈ K. ∎

*Source.* PROOFS "Cone tiles: QF-pair lemma, …" (notation and (P0′), (P1′), (Peak′)). Reviewed. In Lean as part of
`ConeForest.lean` (`plateau_lt`, `qO_claim_cone`).

### 9.2 The lattice input: Wall and Floor Lemmas

**Lemma 9.2 (Wall Lemma).** Let D be a cone tile, so q = q* ∈ Λ, and let {a, b, c} = {1, 2, 3}. Every non-axis inner
corner w of A_c with w ≥ (q_a, q_b) has multiplier μ_w ∈ [L_c − q_c, L_c − 1] (Lemma 6.1(b)). Consequently A_c has at
most q_c such inner corners.

*Proof.* Let g := (w, 0) be the point with (a, b)-coordinates w and c-coordinate 0. By Lemma 6.1(b), g ≡ μ_w e_c with
0 ≤ μ_w ≤ L_c − 1, and the multipliers are distinct.
- Put P := g − q + q_c e_c. Its (a, b)-coordinates are w − (q_a, q_b) ≥ 0 and its c-coordinate is 0.
- P ≤ g − e_a (as q_a ≥ 1), and g − e_a ∈ A_c ⊆ D, so P ∈ D.
- Since q ∈ Λ, P ≡ g + q_c e_c ≡ (μ_w + q_c)e_c.
- If μ_w + q_c ≤ L_c − 1, then (μ_w + q_c)e_c ∈ D would be a second cell in the class of P. It is distinct from P,
  because its c-coordinate is ≥ 1. This is impossible, so μ_w ≥ L_c − q_c.
- The multipliers are distinct and lie in an interval of length q_c. ∎

**Lemma 9.3 (Floor Lemma).** Let D be a cone tile, and let Sl_c := {u ∈ ℕ² : (u at height x_c = q_c − 1) ∈ D}, the
slice of D at height q_c − 1, a 2-D down-set in the coordinates (a, b).
- Sl_c has at most one inner corner w with w ≥ (q_a, q_b).
- Consequently the *floor* Fl_c := Sl_c ∩ ([q_a, ∞) × [q_b, ∞)) has at most two corners.
- 𝒴_c consists exactly of the cells of D at height q_c − 1 over the corners of Fl_c. In particular |𝒴_c| ≤ 2 for
  each c, and |𝒴| ≤ 6.

*Proof.*
- **The corner is a face corner.** Let w ≥ (q_a, q_b) be an inner corner of Sl_c, and let ŵ be the point with
  (a, b)-coordinates w and c-coordinate q_c − 1.
  - ŵ ∉ D, and ŵ ∉ K (since ŵ_c < q_c), so ŵ ∉ Cyl.
  - ŵ − e_a and ŵ − e_b lie in D. Cyl satisfies (∗), and pr_a(ŵ) = pr_a(ŵ − e_a) ∈ Cyl and
    pr_b(ŵ) = pr_b(ŵ − e_b) ∈ Cyl. Hence pr_c(ŵ) = (w, 0) ∉ Cyl, i.e. w ∉ A_c.
  - Meanwhile (w − e_a, 0) = pr_c(ŵ − e_a) ∈ A_c and (w − e_b, 0) ∈ A_c.
  - So w is a non-axis inner corner of A_c with w ≥ (q_a, q_b), and μ_w ∈ [L_c − q_c, L_c − 1] by Lemma 9.2.
- **At most one such corner.**
  - For 0 ≤ j ≤ q_c − 1, let P_j be the point with (a, b)-coordinates w − (q_a, q_b) and c-coordinate j. Then
    P_j ≤ ŵ − e_a ∈ D, so P_j ∈ D. Also P_j = (w, 0) − q + (q_c + j)e_c ≡ (μ_w + q_c + j)e_c.
  - Suppose there were two such corners w ≠ w′ with μ_w < μ_{w′}, and put d := μ_{w′} − μ_w ∈ [1, q_c − 1].
  - Then P_d (built from w) and P′₀ (built from w′) are distinct cells of D (their c-coordinates are d ≥ 1 and 0) in
    the same class (μ_{w′} + q_c)e_c. Contradiction.
- **The floor.** Fl_c − (q_a, q_b) is a 2-D down-set. Its non-axis inner corners are inner corners of Sl_c that are
  ≥ (q_a + 1, q_b + 1). So it has at most one, hence at most two corners (the staircase fact of §3.2).
- **The floor maxima.**
  - y + e_c ∈ K and y ∉ K hold iff y_a ≥ q_a, y_b ≥ q_b and y_c = q_c − 1.
  - Such a y is maximal iff in addition y + e_a, y + e_b ∉ D. (y + e_c ∈ K already gives y + e_c ∉ D.) This says that
    its (a, b)-part u satisfies u + e_a, u + e_b ∉ Sl_c, i.e. that u is a corner of Fl_c. ∎

*Source and status.*
- PROOFS "Cone tiles: wall and floor lemmas (PROVED 2026-10-18 night 15)".
- Data: every cone tile with m ≤ 48 has 1 or 2 floor maxima per direction.
- Reviewed by the cone referee. On all 13,299 cone tiles in `logs/tiles` it checked: μ ∈ [L_c − q_c, L_c − 1], μ
  distinct, ≤ q_c quadrant corners, ≤ 1 floor inner corner, |𝒴_d| ≤ 2.
- **Not in Lean.** This is the only lattice input of §9: everything below uses the lattice only through |𝒴_d| ≤ 2.

### 9.3 Defect localization

**Lemma 9.4 (S′ and consequences; cone class, no lattice).**
- (a) **(S′)** Let x, x′ ∈ D satisfy x + e_d, x′ + e_d ∈ D for all d, and let top_a(x) = top_b(x′) = y ∈ Max with
  a ≠ b. Then y + e_c ∈ K (c the third direction), i.e. y ∈ 𝒴_c.
- (b) Among cells x with x + e_d ∈ D for all d, a maximal cell y is a top in at most two directions. The sets 𝒴₁, 𝒴₂
  and 𝒴₃ are pairwise disjoint.

*Proof.*
- (a) As in Lemma 8.2: pr_a(y + e_c) = pr_a(x + e_c) ∈ Cyl, pr_b(y + e_c) = pr_b(x′ + e_c) ∈ Cyl and
  pr_c(y + e_c) = pr_c(y) ∈ Cyl. So y + e_c ∈ Cyl by (∗). Since y ∈ Max(D), y + e_c ∉ D, so y + e_c ∈ K.
- (b) If y were a top in all three directions, then (a) applied to the direction pairs {a, b} and {b, c} would give
  y + e_c ∈ K and y + e_a ∈ K.
  - y + e_c ∈ K gives y_a ≥ q_a and y_b ≥ q_b; y + e_a ∈ K gives y_c ≥ q_c. Then y ∈ K, a contradiction.
  - The same computation shows that 𝒴_a ∩ 𝒴_c = ∅. ∎

*Status.* PROOFS "Defect localization (S′)"; reviewed. The referee asserted S′ for *all* cells with every x + e_d ∈ D.
Lean `coneS`, `coneNoThree`.

**Lemma 9.5 (P′).** Let D be in the cone class. If tripods u, u′ and directions a ≠ b satisfy u_a < u′_a and
u_b > u′_b, then top_c(u) + e_a ∈ K or top_c(u′) + e_b ∈ K.

*Proof.* Take (a, b, c) = (1, 2, 3), p = (X, Y) = (u₁, u₂) and p′ = (X′, Y′) = (u′₁, u′₂), with X < X′ and Y > Y′.
- Both p and p′ are peaks (γ = 0), and p + e₁, p′ + e₂ ∈ A₃ (Lemma 7.2(a)).
- (Peak′) at p gives F(X + 1) < G(Y), or top₃(u) + e₁ ∈ K.
- The mirror of (Peak′) at p′ gives G(Y′ + 1) < F(X′), or top₃(u′) + e₂ ∈ K.
- If neither alternative involving K holds, then F(X′) ≤ F(X + 1) < G(Y) ≤ G(Y′ + 1) < F(X′), a contradiction. ∎

*Status.* PROOFS "(P′)"; reviewed (all ordered tripod pairs × 6 planes, EXH4/5, TILES). Lean `coneP`.

### 9.4 Lemma TF-cone

**Lemma 9.6 (TF-cone).** Let D be in the cone class with |𝒴_d| ≤ 2 for d = 1, 2, 3. Then 2|Tri| ≤ t + 17.

*Proof.* This is NOTEBOOK "night 17", with the two referee edits marked there.

*Elimination budget.* Process the tripods by decreasing |x|. For a tripod x and direction d, the top top_d(x) is
*used* if it is a top of an earlier tripod.
- It is a *same share* if some earlier tripod has it as its d-top. Such a partner lies in the d-column of x, above x:
  it is x + i e_d with i ≥ 1.
- It is a *cross share* if it is used, but no earlier tripod has it as its d-top.
- Write s(x), s_same(x) and s_cross(x) for the numbers of used tops, same shares and cross shares of x.

Each tripod brings 3 − s(x) new maxima, so t ≥ 3|Tri| − Σ_x s(x), i.e. 2|Tri| − t ≤ Σ_x (s(x) − 1). The first tripod
has s = 0. For the others, s − 1 ≤ s_cross + (s_same − 1)⁺. Hence, if Tri ≠ ∅ (otherwise there is nothing to prove),

    2|Tri| − t ≤ −1 + Σ_x s_cross(x) + Σ_x (s_same(x) − 1)⁺.                                     (9.1)

**(i) Cross shares.**
- If y is a cross share of x in direction d, then some earlier tripod has y as a top in a direction d′ ≠ d. So y ∈ 𝒴
  by Lemma 9.4(a).
- By Lemma 9.4(b), y is a tripod top in at most two directions: d₁, that of its first user, and possibly d₂. A cross
  share at y can occur only for the first d₂-user.
- So each y ∈ 𝒴 gives at most one cross share, and Σ s_cross ≤ |𝒴| ≤ 6.

**(ii) Same shares in two directions.** Let x have same shares in directions a ≠ b, with partners u = x + i e_a and
u′ = x + i′ e_b (earlier tripods with top_a(u) = top_a(x) and top_b(u′) = top_b(x)).
- Then u′_a = x_a < u_a and u′_b > x_b = u_b.
- Lemma 9.5 applied to (u′, u) gives top_c(u′) ∈ 𝒴_a or top_c(u) ∈ 𝒴_b. (Both are maximal, being tripod tops.)

For an ordered pair (a, b) of distinct directions, with c the third, define

    Φ(a, b) := {tripods x with same shares in BOTH a and b, such that some b-partner u′ of x has top_c(u′) ∈ 𝒴_a}.

(Referee edit: the words "in both a and b" are needed, because (iv) and (v) use an a-partner of x.) By (ii), every
tripod with same shares in a and b lies in Φ(a, b) ∪ Φ(b, a).

**(iii) If x ∈ Φ(a, b), then x_a = q_a − 1 and x_c < q_c.**
- y := top_c(u′) satisfies y + e_a ∈ K and y ∉ K. Hence y_a = q_a − 1 and y_b ≥ q_b, and y_a = u′_a = x_a.
- u′ + e_a ∈ D, because u′ is a tripod. Its a-coordinate is q_a and its b-coordinate is u′_b = y_b ≥ q_b, so
  u′ + e_a ∉ K forces u′_c < q_c. And x_c = u′_c.

**(iv) All members of Φ(a, b) have the same c-coordinate.** Hence Φ(a, b) lies on one b-line
ℓ = {(q_a − 1, ·, z₀)} in the coordinates (a, b, c).
- Let x, x̃ ∈ Φ(a, b) with x̃_c > x_c, and let u = x + i e_a be an a-partner of x. Then x̃_a = q_a − 1 < u_a and
  x̃_c > x_c = u_c.
- Lemma 9.5 in the (a, c)-plane (third direction b), applied to (x̃, u), gives top_b(x̃) + e_a ∈ K or
  top_b(u) + e_c ∈ K.
- The first is impossible, because top_b(x̃) has c-coordinate x̃_c < q_c by (iii).
- So top_b(u) + e_c ∈ K, which gives x_c + 1 = u_c + 1 ≥ q_c, i.e. x_c = q_c − 1. Then x̃_c ≥ q_c, contradicting (iii).

**(v) |Φ(a, b)| ≤ 2.**
- *At most one member has x_b < q_b.*
  - Let x, x̃ ∈ Φ(a, b) with x_b < x̃_b, and let u = x + i e_a be an a-partner of x. Then x̃_a < u_a and x̃_b > u_b.
  - Lemma 9.5 applied to (x̃, u) gives top_c(x̃) + e_a ∈ K, which needs x̃_b ≥ q_b, or top_c(u) + e_b ∈ K, which needs
    x_b + 1 ≥ q_b.
  - So x̃_b ≥ q_b or x_b ≥ q_b − 1. If both x_b and x̃_b were < q_b, then x_b = q_b − 1 < x̃_b < q_b, which is
    impossible.
  - (Referee edit: the record first read "or x_b = q_b − 1"; P′ only gives x_b ≥ q_b − 1.)
- *At most |𝒴_a| − 1 ≤ 1 members have x_b ≥ q_b.*
  - For such a member x, take a b-partner u′ = x + i′ e_b with top_c(u′) ∈ 𝒴_a. That top is (q_a − 1, x_b + i′, h′)
    with h′ ≥ q_c.
  - The c-column of D over (q_a − 1, x_b) is at least as tall as the one over (q_a − 1, x_b + i′), which reaches height
    h′ ≥ q_c.
  - So top_c(x) has c-coordinate ≥ q_c, and top_c(x) + e_a ∈ K since x_b ≥ q_b. As top_c(x) ∈ Max, top_c(x) ∈ 𝒴_a.
  - These tops are distinct for distinct members, since their b-coordinates differ. They are also distinct from
    top_c(u′_top), where u′_top is the partner of the member with the largest b-coordinate: that top lies in 𝒴_a and
    its b-coordinate exceeds every member's.
  - Hence #{members with x_b ≥ q_b} + 1 ≤ |𝒴_a| ≤ 2.

**(vi) Accounting.**
- A tripod with s_same = 2 (in directions a, b) lies in Φ(a, b) ∪ Φ(b, a).
- A tripod with s_same = 3 lies, for each of the three unordered pairs, in one of the two corresponding families, so in
  at least three of the six families.
- Hence Σ_x (s_same(x) − 1)⁺ ≤ Σ_{(a,b)} |Φ(a, b)| ≤ 6·2 = 12.

By (9.1), (i) and (vi): 2|Tri| − t ≤ −1 + 6 + 12 = 17. ∎

*Status.*
- Paper: NOTEBOOK "2026-10-18 (night 17)", referee-corrected wording.
- Reviewed (cone referee, "CORRECT (two wording fixes)"). Claims (i)–(v) and the budget (9.1) were asserted separately
  on EXH4/5 and on all cone tiles. On tiles: 2Tri − t ≤ −2, s_cross ≤ 1, excess ≤ 1, |Φ| ≤ 1.
- Lean: `tfCone` (`lean/Wilf/ConeForest.lean`): 2|Tri| ≤ t + 17 under |𝒴_d| ≤ 2. Also the sharper `tf_cone`:
  2|Tri| ≤ t + |𝒴| + 11.

### 9.5 Lemma F-cone

**Lemma 9.7 (F-cone).** For every D in the cone class, |qU| ≤ t + 2.

*Proof.*
- Let G_U be the simple graph of Lemma 8.6, which is defined for any down-set by Lemma 7.2(b). Use the slices U_v of
  Lemma 7.5 (direction 3).
- **Levels v ≠ q₃.** Here U_{v+1} = U_v ∩ R_{v+1} and U_v ⊆ R_v. The proof of Lemma 8.6 at level v uses only these two
  facts, the down-set property of U_v, and the fact that the notch of two consecutive corners of U_v lies in U_v.
  So such a level adds at most one c = 1 edge and one c = 2 edge, and no cycle.
- **Level v = q₃.** Here U_{v+1} = (U_v ∩ R_{v+1}) ∖ Quad. A c = 1 edge at this level has upper end p ∈ M_{v+1} and
  lower end p + e₂ ∈ M_v ⊆ U_v ∖ U_{v+1}. There are two cases.
  - p + e₂ ∉ R_{v+1}. Then p is the leftmost corner of U_{v+1}, as before.
  - p + e₂ ∈ Quad. Here p ∉ Quad, since p ∈ U_{v+1}. So p₂ = q₂ − 1 and p₁ ≥ q₁, and p, being a corner of U_{v+1}, is
    the end of row q₂ − 1 of U_{v+1}. (It is also the end of that row in U_{q₃}, since p + e₁ ∉ U_v.)
  - Each case determines p, so there are at most two c = 1 edges at this level, and symmetrically at most two c = 2
    edges.
  - The c = 3 edges of M_{q₃} again form disjoint paths. The first cross edge added joins a new component, so the at
    most four cross edges create at most three independent cycles.
- **Conclusion.** rank(G_U) ≤ 3, and |qU| = t − comp(G_U) + rank(G_U) ≤ t − 1 + 3 = t + 2. ∎

*Status.*
- Paper: NOTEBOOK "night 17" (Lemma F-cone).
- Reviewed (cone referee, item (d): per-level counts asserted, no cycle at a level ≠ q₃, max rank(G_U) = 1 in every
  range).
- Lean: `fCone` (qU ≤ t + 2), and the sharper `qU_cone`: |qU| ≤ t.

### 9.6 The QF-pair Lemma, DS cells, Location and Fiber

**Lemma 9.8 (QF-pair Lemma).** Let v = (X, Y, z) be a qO cell with non-maximal direction 3, and let u = v − i e₁ (i ≥ 1)
be a qO cell with top₁(u) = top₁(v). Put p = (X, Y) and p′ = (X − i, Y). Then F(X) < G(Y), unless
- (α) u has non-maximal direction 2 and top₃(u) + e₁ ∈ K, or
- (β) u has non-maximal direction 3, p ∈ Quad, p′ ∉ Quad, and ψ(p) = q₃.

Mirror: if u = v − i e₂ is a qO cell with top₂(u) = top₂(v), then G(Y) < F(X), unless
- (α′) u has non-maximal direction 1 and top₃(u) + e₂ ∈ K, or
- (β′) u has non-maximal direction 3, p ∈ Quad, p − i e₂ ∉ Quad, and ψ(p) = q₃.

*Proof.* The non-maximal direction of u is not 1, because top₁(u) ∈ Max.
- **Direction 2.** Then top₃(u) ∈ Max, so γ(p′) = 0. Also p′ + e₁ ≤ p ∈ A₃, so p′ + e₁ ∈ A₃. (Peak′) gives
  F(X − i + 1) < G(Y), or (α). In the first case F(X) ≤ F(X − i + 1) < G(Y).
- **Direction 3.**
  - γ(p′) = γ(p) = 1, by Lemma 7.2(c) and (P0′). So ψ(p′) ≠ ψ(p) by (P1′), and hence ψ(p′) > ψ(p).
  - Suppose F(X) ≥ G(Y). Then ψ(p) = min(G(Y), Q(p)) < ψ(p′) ≤ min(G(Y), Q(p′)).
  - This forces Q(p) = q₃ < Q(p′) = ∞ and ψ(p) = q₃, which is (β). ∎

*Status.* Reviewed: every pair (v, u) and all 6 orientations, EXH4/5, TILES and the DS family. Lean (`qO_claim_cone`).

**Definition (DS).** A qO cell x is *doubly-same* (DS) if, for both of its maximal directions d, some qO cell u ≠ x with
u_d < x_d has top_d(u) = top_d(x). (Such a u is x − i e_d with i ≥ 1.) This is Lean `IsDS`.

**Corollary 9.9 (Location).** A DS cell x with non-maximal direction c lies in B_c.

*Proof.* Take c = 3 and x = (X, Y, z). x has a 1-partner u and a 2-partner u″ as in Lemma 9.8. If neither pair is
defective, then F(X) < G(Y) < F(X), which is impossible. So one case of (α), (β), (α′), (β′) holds.
- **(α).**
  - top₃(u) = (X − i, Y, ψ(p′) − 1) is ∉ K, while top₃(u) + e₁ ∈ K. So X − i = q₁ − 1 and Y ≥ q₂, and also X ≥ q₁.
  - u + e₁ ∈ D, because u is a qO cell, so all its forward neighbours lie in D (Lemma 7.2(a)). (Referee edit: this
    justification was added.)
  - u + e₁ = (q₁, Y, z) ∉ K, with (q₁, Y) ∈ Quad. This forces z < q₃. So x ∈ B₃.
- **(β).** p ∈ Quad, and z < ψ(p) = q₃. So x ∈ B₃.
- **(α′) and (β′).** These are the mirror cases. ∎

*Status.* Lean `location_cone`, `IsDS.location`.

**Lemma 9.10 (Fiber Lemma).** Two distinct DS cells never share a maximal top in the same direction.

*Proof.* Let x and x̂ = x + k e_a (k ≥ 1) be DS cells with the same top_a. Let c and ĉ be their non-maximal directions;
both are ≠ a.
- **ĉ ≠ c.** By Cor 9.9, x ∈ B_c gives x_ĉ ≥ q_ĉ, and x̂ ∈ B_ĉ gives x̂_ĉ < q_ĉ. But x̂_ĉ = x_ĉ, since ĉ ≠ a.
  Contradiction.
- **ĉ = c**, say c = 3 and a = 1 (a = 2 is the mirror). Then x = (X, Y, z) and x̂ = (X + k, Y, z) both lie in B₃, so
  p = (X, Y) and p̂ = (X + k, Y) lie in Quad.
  - γ(p) = γ(p̂) = 1, so by (P1′), ψ(p) > ψ(p̂).
  - Q = q₃ at both points, so ψ(p̂) = min(F(X + k), G(Y), q₃) < min(F(X), G(Y), q₃). This forces:
    (i) F(X + k) < G(Y); and (ii) F(X + k) < q₃, with ψ(p̂) = F(X + k).
  - x̂ has a 2-partner û = x̂ − i′ e₂. By (i), G(Y) < F(X + k) fails. So by the mirror of Lemma 9.8, (α′) or (β′) holds
    for x̂.
  - (β′) needs ψ(p̂) = q₃, which contradicts (ii).
  - (α′) gives top₃(û) ∉ K and top₃(û) + e₂ ∈ K. So Y − i′ = q₂ − 1, and the height satisfies
    ψ(X + k, q₂ − 1) − 1 ≥ q₃. Since (X + k, q₂ − 1) ∉ Quad, ψ(X + k, q₂ − 1) = min(F(X + k), G(q₂ − 1)) ≥ q₃ + 1, which
    contradicts (ii). ∎

*Status.* Reviewed (cone referee, (b)). Stress test: the lattice-free DS family has Q − 1 DS cells at
p = (q₁, q₂), none sharing a maximal top in the same direction (Q = 4..14). Lean `fiber`, `fiber_aux`.

### 9.7 The qO bound

**Theorem 9.11 (qO-cone).** For every D in the cone class, |qO| ≤ 2t − 1 + 2|𝒴|. For cone tiles, |𝒴| ≤ 6 (Lemma 9.3),
so |qO| ≤ 2t + 11.

*Proof.* Let G_O be the multigraph on Max(D) with one edge {top_a(x), top_b(x)} for each x ∈ qO, where a and b are the
maximal directions of x. Tops in distinct directions are distinct, so there are no loops. Then

    |qO| = t − comp(G_O) + rank(G_O).

Add the edges in order of increasing |x|. Then rank(G_O) is the number of *closing* cells, i.e. cells whose edge joins
two vertices already in one component.

1. **Both tops of a closer are used.** If x is closing, its two (distinct) endpoints are joined by a nonempty path of
   earlier edges. So both maximal tops of x are already tops of earlier qO cells.
2. **The two cases.** Let d be a maximal direction of a closing x, and y_d := top_d(x). Either
   - *case 1:* some earlier qO cell u has top_d(u) = y_d, and then u = x − i e_d with i ≥ 1; or
   - *case 2:* every earlier user of y_d uses it in a direction ≠ d. Then y_d ∈ 𝒴 by Lemma 9.4(a), since qO cells
     satisfy its hypothesis (Lemma 7.2(a)), and x is the first user of y_d in direction d.
3. **Counting case 2.** By Lemma 9.4(b), y is a qO top in at most two directions: d₁, that of its first user, and
   possibly d₂.
   - The first user of y is not case 2 at y, since it has no earlier users.
   - Later d₁-users have the first user as an earlier d₁-user, so they are not case 2 at y.
   - Among the d₂-users, only the first can be case 2 at y.
   - So each y ∈ 𝒴 is a case-2 top for at most one cell. Hence at most |𝒴| closing cells have a case-2 top. (Referee
     edit: these three sentences make the count explicit.)
4. **The other closers are DS.** A closing cell whose two tops are both case 1 is DS.
5. **#DS ≤ t + |𝒴|.** Map each DS cell x to top_{a(x)}(x), where a(x) is the smaller of its two maximal directions.
   - If two distinct DS cells have the same image y with the same direction, this contradicts Lemma 9.10.
   - If the directions differ, then y ∈ 𝒴 by Lemma 9.4(a). By Lemma 9.4(b) and Lemma 9.10, at most two DS cells map to
     such a y.
   - So #DS ≤ t + |𝒴|.
6. **Conclusion.** rank(G_O) ≤ |𝒴| + t + |𝒴|, and comp(G_O) ≥ 1. So |qO| ≤ t − 1 + t + 2|𝒴|. ∎

*Correction preserved from the record.* The headline of this theorem once read "qO ≤ t − 1 + 2|Y|". That was a typo,
and the bound is **false** lattice-free. The referee's counterexample: h = (11, 11, 2 × 10), F = (11, 11, 10, 9, …, 1),
G = (11, 11, 9, 8, …, 1), q = (1, 1, 10), with m = 243, t = 21, |𝒴| = 3 and qO = 27 > 26. The proof gives only
2t − 1 + 2|𝒴|, and only that form is used.

*Remark (not used).* The image of the DS map lies in Max ∩ (B₁ ∪ B₂ ∪ B₃), so qO ≤ t − 1 + 2|𝒴| + |Max ∩ B|.

*Status.*
- Paper: PROOFS "Theorem (qO-cone)".
- Reviewed (cone referee). Every sub-claim was asserted separately, with exact counts: the graph identity, the case
  classification, the case-2 count ≤ |𝒴|, the DS collision structure, #DS ≤ t + |𝒴|, and a second tie-breaking order.
- Lean: `qOCone` (|qO| + 1 ≤ 2t + 2|𝒴|). Also the sharper `qO_cone`: |qO| + 1 ≤ 2t + |𝒴|. The Lean proof shows that
  the DS fibres have size ≤ 2, so #DS ≤ t.

### 9.8 The cone corollary

**Theorem 9.12 (cone tiles).** For every cone tile D with m = |D|:

    LHS(D) ≤ 6t + 30,        δ(D) ≥ m − 6t − 29 ≥ m − 6C − 29 ≥ m − 6√(6m) − 38.

Consequently δ(D) ≥ 0 for m ≥ 281, and δ(D) ≥ −1 for m ≥ 280.

*Proof.*
- By Lemma 9.3, |𝒴_d| ≤ 2 and |𝒴| ≤ 6.
- By Lemmas 9.6 and 9.7 and Theorem 9.11, LHS = 2t + 2|Tri| + |qU| + |qO| ≤ 2t + (t + 17) + (t + 2) + (2t + 11) = 6t + 30.
- Lemma 7.1 gives δ ≥ m + 1 − LHS ≥ m − 6t − 29.
- Lemma 7.5 gives t ≤ C, and Lemma 7.6 gives C ≤ C_max(m) < 3/2 + √(6m).

*Thresholds.*
- **Large m.** m − 6C_max(m) − 29 ≥ m − 6√(6m) − 38. The right side is increasing for m ≥ 54 and positive at m = 287
  (≈ 0.018).
- **Small m.** For 280 ≤ m ≤ 287, C_max(m) = 42 (C_max jumps to 42 at m = 274 and to 43 at m = 288). So
  6·42 + 29 = 281 ≤ m for m ≥ 281, and 6·42 + 28 = 280 ≤ m for m ≥ 280.
- **Exact check.** The referee checked exactly that the last m with 6C_max(m) + 29 > m is 280, for m ≤ 2·10⁵, and I
  rechecked this for m ≤ 10⁶. ∎

*Status.*
- Paper: PROOFS "Corollary (HT for large cone tiles)".
- Reviewed (cone referee, (g)). LHS ≤ 6t + 30 was asserted on every lattice-free set with all |𝒴_d| ≤ 2.
- Lean: `coneDeltaBound` (2m ≤ H + 6C + 30), `coneThreshold` (m ≥ 281 ⇒ δ ≥ 0) and `coneThreshold'` (m ≥ 280 ⇒ δ ≥ −1).
  All three take |𝒴_d| ≤ 2 as a hypothesis.

**Remark 9.13 (sharper constant, Lean only; not used).**
- `coneDelta_sharp` gives 2m ≤ H + 6t + 2|𝒴| + 10, i.e. δ ≥ m − 6C − 21 when |𝒴| ≤ 6. With Lemma B this gives HT for
  m ≥ 267 and δ ≥ −1 for m ≥ 266. (PROOFS records this; I rechecked the thresholds.)
- The record contains no paper proof of the three sharper ingredients (qU ≤ t; qO + 1 ≤ 2t + |𝒴|;
  2Tri ≤ t + |𝒴| + 11). They exist only as Lean proofs. This is not a gap, because §11 uses only Theorem 9.12.
- The sharper constant would shorten the finite range for cone tiles from m ≤ 279 to m ≤ 265. This is not needed,
  because (FC) is complete and certified to m = 280.

---

## 10. The finite computation (link 7)

### 10.1 What has to be computed

By §11, Theorem A follows from §§3–9, (E1) and (E2), together with the following statement.

**(FC)** For every m with 19 ≤ m ≤ 279, and every S with e(S) = 4, m(S) = m and non-two-face tile D = D(S), either
δ(D) ≥ −1 or (m + 1)κ_D ≥ m(m − 1).

For 130 ≤ m ≤ 279 only cone tiles need checking, by Cor 8.8. The enumeration below proves a shape statement that is
stronger: for every non-two-face tile of every relevant lattice, it computes δ.

### 10.2 Enumeration: lattices, open cones, coverage

**Lattices.**
- For S as above, r = p mod m has distinct nonzero entries (N5), and the r_a generate ℤ/m (Lemma 4.1(a)).
- A unit u ∈ (ℤ/m)^× gives Λ_{ur} = Λ_r. A coordinate permutation σ gives Λ_{σr} = σΛ_r, and tiles are permuted
  accordingly.
- The scan takes one canonical r per orbit: sorted, distinct, nonzero, gcd(r, m) = 1, and lexicographically minimal
  among sorted(u·r) (chain referee's reading of the code).
- HT, δ and the two-face property are invariant under σ.

**Open cones.** For a lattice tile (D, Λ), put Cone(D) := {π ∈ ℝ³_{>0} : π·(q − rep(q)) > 0 for all q ∈ 𝒢(D)}, and
let Δ := {π ∈ ℝ³_{>0} : π₁ + π₂ + π₃ = 1}.

**Lemma 10.2.** Fix Λ = Λ_r.
- (a) If π ∈ Cone(D), then D is the set of π-weight-minimal elements of the classes of ℤ³/Λ in ℕ³, and each minimum is
  unique.
- (b) Open cones of distinct tiles are disjoint.
- (c) If π ∈ Δ and π·y ≠ 0 for every y ∈ Λ ∖ {0}, then the set D_π of π-minimal representatives is a lattice tile
  and π ∈ Cone(D_π). Such π form a set of full measure in Δ.
- (d) (coverage) For S with e = 4 and residue vector r, D(S) is the set of minimal representatives for the term order
  ≻ "compare p·x, then |x|, then lex". There is π ∈ Cone(D(S)) arbitrarily close to p. In particular D(S) is an
  open-cone tile of Λ_r.

*Proof.*
- (a) Let x ∈ ℕ³ ∖ D. Then x ≥ q for some q ∈ 𝒢(D). The point x − q + rep(q) ∈ ℕ³ is congruent to x and has strictly
  smaller π-weight. Iterating terminates, because {y ∈ ℕ³ : π·y ≤ π·x} is finite for π > 0, and it can stop only in
  D. So all class minima lie in D. As D has exactly one element per class, the claim follows.
- (b) Follows from (a).
- (c) Distinct elements of a class have distinct weights, so each class has a unique minimum.
  - D_π is a down-set. If x′ ≤ x ∈ D_π and y ≡ x′ had smaller weight, then y + (x − x′) ≡ x would have smaller weight
    than x.
  - For q ∈ 𝒢(D_π), the representative rep(q) has strictly smaller weight than q.
  - The excluded π lie on countably many lines.
- (d) By N1 and Prop 3.1, the minimum of p·x over a class is its Apéry element, and the grlex tie-break selects n(w).
  - Each of the finitely many y = q − rep(q), q ∈ 𝒢(D(S)), is ≻-positive: p·y > 0, or p·y = 0 and |y| > 0, or
    p·y = |y| = 0 and y is lex-positive.
  - Choose u with u·y > 0 for the y of the last kind. For example u = (N², N, 1) with N large, for the convention that
    x₁ is compared first.
  - Then π := p + ε(1, 1, 1) + ε²u lies in Cone(D(S)) for all small ε > 0. ∎

*Source.* `src/tile_enum.py` docstring and the chain referee's coverage argument ("D is the standard set of the term
order (p, degree, lex) … so D is an open-cone tile of Λ_{r(S)}"). Parts (a)–(c) spell out the "standard Gröbner-fan
facts" the record relies on. The reduction step in (a) is the referee's "for p in it, reduction n → n − q + rep q
terminates in D".

**Traversal.**
- Start from an interior point of Δ, compute D_π and the polygon Cone(D) ∩ Δ in exact arithmetic, and flip across
  each edge into the neighbouring cone.
  - The Python version moves the facet midpoint out by ε and halves ε with exact Fractions.
  - The C version uses the lexicographic order (mid·x, −n·x, |x|, lex x).
  - Both assert that the new cone's closure contains the midpoint.
- Continue until no new tile appears.
- For every tile containing all three e_a + e_b (non-two-face), compute H(D) and δ(D).

### 10.3 The completeness certificate

**Lemma 10.3.** Let 𝒯 be a finite list of distinct tiles of Λ with nonempty open cones. Then 𝒯 contains every such
tile iff Σ_{D∈𝒯} area(Cone(D) ∩ Δ) = area(Δ).

*Proof.*
- The cones are disjoint (Lemma 10.2(b)), and their union covers Δ up to measure zero (Lemma 10.2(c)).
- Each nonempty open cone is closed under positive scaling, so it meets Δ in a nonempty relatively open set of positive
  area. ∎

*Implementation.*
- `src/c/tile_scan_v.c` sums the doubled areas of all traversed cone polygons mod 2⁶¹ − 1 and reports
  "AREACHECK … area-defects 0" when the sum equals the simplex for every lattice.
- Being a mod-p test, it misses a wrong exact sum only if that sum happens to be congruent to the correct one mod
  2⁶¹ − 1 (trust note).
- The referee's Python check for m ≤ 40 is exact.
- The certificate establishes completeness of the tile list. It does not check the per-tile computation of H, δ and
  the two-face test, which remains code trust.

### 10.4 Implementations, and the 8-bit coordinate bug

**Implementations.**
- **Python.**
  - `src/tile_enum.py` does the enumeration. It was validated by finding every grlex tile of every e = 4 semigroup with
    generators < 5m for m = 5..13 (≈ 36,000 semigroups, 0 missing; `logs/tile_enum_validate.log`).
  - `src/scratch/tile_scan_H.py` and `tile_scan_HM.py` do the HT scan, with LP certification of failures by
    `src/tile_lp.py`.
- **C.** `src/c/tile_scan.c` (E132) is a port of `tile_scan_HM.py`. It uses int64 integer normals, the lexicographic
  flip, threads, and prints HT failures as "LP-pending". Its output is identical to the Python on 188 lines over 119
  values of m ≤ 130 (E133). It is the same algorithm, not a method-independent check.
- **C, fixed.** `src/c/tile_scan_v.c` (E140) is the referee's patch: coordinate type `-DCT=uint16_t`, `-DMAXM=300`,
  and the area certificate. It was built with gcc 13.3 on fejer.

**The uint8 bug (found by the chain referee, 2026-10-18).**
- In `tile_scan.c` the coordinate storage (`Key.x`, the tile array `T`, the hash arena) is `uint8_t`, and
  MAXM = 255.
- A build with MAXM raised to 300, which is the private build E136 used for m ≥ 256, silently wraps every
  coordinate ≥ 256.
- Long-axis tiles near the boundary of Δ have coordinates up to m − 1. For example, if r₁ is a unit, the axis
  {k e₁ : k < m} is a tile. So for m ≥ 257 the traversal is corrupted, yet the program exits normally.
- Demonstrations on a copy:
  - m = 257, 1/500 sample: 1 of 22 lattices has a wrong cone area.
  - m = 280, 1/150 sample: 61,277 tiles instead of 61,279, and 42 of 219 lattices with area defects, exit code 0.
- Confirmation by the lead on fejer: at m = 257 the 8-bit build has 127 area-defective lattices out of 10,795, with the
  same totals and HT result by chance; the 16-bit build has 0.
- **Fix.** `tile_scan_v.c` with 16-bit coordinates. Its output is identical to the old build at m = 131 and 200 (and in
  totals at 257), with every lattice certified.
- **Consequence.** The whole range was rerun with the certified 16-bit build: m = 256–280 (E140), and m = 4–119 and
  120–255 (E141).
  - The record had asserted that the 8-bit build is valid for m ≤ 255 (STATE, E140). This is consistent with all
    stored coordinates being < m ≤ 255.
  - The rerun confirms it on every overlap. For all 113 values m = 7–119 and all 116 values m = 120–235 that also
    appear in the earlier Python, uint8 and C logs, tiles, non-two-face count, HT failures and min δ are identical
    (my comparison of the parsed logs).

### 10.5 Results

I parsed the per-m lines of the three certified 16-bit logs:
- `logs/tsv16_4_119_fejer.log` (E141);
- `logs/tsv16_120_255_fejer.log` (E141);
- `logs/tsv16_256_280_fejer.log` (E140).

Every m ∈ [4, 280] appears exactly once, with an "AREACHECK … area-defects 0" line. Tile counts are per canonical
lattice, i.e. up to units and permutations. The last column lists the earlier, uncertified logs, which agree line by
line on every m they contain (§10.4).

| m range | lattices | tiles | non-two-face | HT fails | min δ | earlier logs (identical) |
|---|---|---|---|---|---|---|
| 4–6 | 8 | 62 | 0 | 0 | — | — |
| 7–18 | 413 | 7,501 | 728 | 7 (m = 8: 1; 15: 2; 16: 2; 17: 2) | −4 (m = 15) | `tile_scan_H.log` (Python) |
| 19–23 | 456 | 12,299 | 1,888 | 4 (m = 19: 1; 20: 2; 23: 1) | −4 (m = 19) | `tile_scan_H.log` |
| 24–60 | 18,644 | 940,417 | 307,102 | 0 | 2 (m = 25) | `tile_scan_H.log` |
| 61–130 | 185,740 | 18,810,000 | 8,688,585 | 0 | 55 (m = 62) | `tile_scan_H.log`, `tile_scan_H_68.log`, `tile_scan_HM_{71,91,101,109,116,123,127}.log`, `tile_scan_C_118_130.log`, `tile_scan_C_gaps.log` |
| 131–235 | 1,026,725 | 175,608,284 | 95,107,612 | 0 | 273 (m = 144) | `tile_scan_C_131_280.log` (131–229), `tile_scan_C_226_280_fejer_uint8.log` (226–235) (C, uint8) |
| 236–255 | 346,299 | 72,524,209 | 41,076,104 | 0 | 712 (m = 240) | none (first computed in E141) |
| 256–280 | 518,751 | 116,436,620 | 66,922,365 | 0 | 845 (m = 264) | — |
| **4–280** | **2,097,036** | **384,339,392** | **212,104,384** | **11** | | |

The 11 failing tiles listed in `tsv16_4_119_fejer.log` ("HT-fail (LP-pending)") have exactly the δ values and lattice
vectors r of the table below.

**The HT failures** (from `tile_scan_H.log`; the same 11 tiles appear in `tsv16_4_119_fejer.log`):

| m | tiles | δ | lattice r | κ_D | covered by |
|---|---|---|---|---|---|
| 8 | 1 | −3 | (1, 2, 5) | 4 (LP fails) | (E2) |
| 15 | 2 | −4, −4 | (1, 4, 6), (1, 10, 12) | 15, 15 | (E2) (also LP) |
| 16 | 2 | −2, −2 | (1, 3, 7) | 28, 22.67 | (E2) (also LP) |
| 17 | 2 | −1, −1 | (1, 3, 11), (1, 4, 10) | 26, 23.33 | (E2) (also Cor 4.3, LP) |
| 19 | 1 | −4 | (1, 6, 8) | 32.5 | **Prop 4.5**: 20·32.5 = 650 ≥ 342 |
| 20 | 2 | −2, −2 | (1, 13, 15) | 44.5, 33.33 | **Prop 4.5**: ≥ 700 ≥ 380 |
| 23 | 1 | −1 | (1, 4, 10) | 40 | **Cor 4.3** (also LP) |

Example semigroups for the m = 19 and m = 23 failures are given in §3.4.

### 10.6 Independent checks (chain referee, E139)

- **Fan-free, shape-first enumeration** (`src/review2/shapes.py`). For m = 7–26, it lists every non-two-face down-set
  of size m, up to 815,620 per m; the generator was validated against brute force. For each with δ < 0, it tests
  realizability as a tile over all r ∈ (ℤ/m)³ and computes the open-cone area exactly. The realizable δ < 0 tiles are
  exactly the scan's list. This check is independent of the fan traversal.
- **Area certificates.**
  - Exact, Python traversal, every lattice, m = 7–40.
  - Mod 2⁶¹ − 1, C traversal, every lattice, m = 19–30 and 46–119: 0 defects. The counts are identical to the project
    logs for 19–45 and 46–119.
  - 1/40 lattice samples at m ∈ {120, 125, 130, 150, 175, 189, 230, 256, 270}: 0 defects, 0 HT failures.
  - These were superseded for completeness purposes by the project's own certified 16-bit rerun of every lattice, every
    m ≤ 280 (E140, E141; §10.5), which uses the referee's certificate code.
- **κ** recomputed with HiGHS for every realizable failing (D, r) (§4.3).
- **End-to-end.** About 48,400 random e = 4 semigroups (m = 19–130, generators up to 10⁴·m, including skewed ones) and
  all 1,624 e = 4 semigroups of genus ≤ 20. All assertions of links 1–5 held. HT failures occurred only at m = 19, 20
  and 23, and at m = 8 in the genus ≤ 20 set.

### 10.7 Coverage summary

- **Needed:** non-two-face tiles for 19 ≤ m ≤ 279. 𝒞-tiles are needed only for m ≤ 129, cone tiles up to 279.
- **Present in the repository:** every m ∈ [4, 280], from the certified 16-bit build, with 0 area defects for every m.
  The only HT failures are the 11 tiles at m ≤ 23 in the table above.
- **History of three gaps flagged while drafting.** All three are now **CLOSED** by E141. I preserve them here because
  the record overstated coverage before the rerun finished.
  - **G1 (closed).** Before E141, no log covered m = 236–255, so cone tiles there were covered by no argument.
    - STATE.md said "m = 131–255: HT 0 failures", but the two logs it cited end at m = 229 and m = 235.
    - The sharper Lean constant of Remark 9.13 would not have closed this, since 266 > 255.
    - Closed by `logs/tsv16_120_255_fejer.log`: m = 236–255 give HT fails 0, area-defects 0 and min δ = 712.
  - **G2 (closed; documentation).** The referee report lists per-lattice area certification for m = 7–40 (exact) and
    m = 19–30, 46–119 (mod p), while STATE.md said "m = 19–119". The range m = 41–45 was not explicitly certified.
    Closed by `logs/tsv16_4_119_fejer.log`, which area-certifies every lattice for m = 4–119.
  - **G3 (closed; trust item).** For 120 ≤ m ≤ 235, completeness rested on the uncertified uint8 traversal. The
    supporting evidence was identical outputs at m = 131 and 200 and the referee's 1/40 samples.
    - Closed by `logs/tsv16_120_255_fejer.log`, which is area-certified and identical to the uint8 lines on all 116
      overlapping m.
    - While drafting I had read a partial copy of this log on fejer, ending at m = 199 at 16:36 UTC. The complete log
      reached the repository at 17:12 UTC (13:12 EDT) on 2026-10-18.
- **Trust base.** Correctness of the code (tile computation, polygon areas, H, the two-face test) and the mod-p area
  test. The C and Python versions are the same algorithm. A method-independent enumeration exists only for m ≤ 26.
  Sethuraman's enumeration, which uses a different method, has not been run by the project.

---

## 11. Main theorem and proof assembly

**Theorem 11.1 (= Theorem A).** Every numerical semigroup S with e(S) = 4 satisfies e(S)·ℓ(S) ≥ c(S).

*Proof.* Let m = m(S). Then m ≥ 4 by N5. Let D = D(S), a lattice tile of size m (Prop 3.1, Lemma 4.1).
1. **m ≤ 18.** W ≥ 0 by (E2).
2. **D two-face.** W ≥ 0 by Theorem 5.7, which uses (E1) and (E2).
3. **Otherwise** m ≥ 19 and D is non-two-face. By Cor 6.5, D ∈ 𝒞 or D is a cone tile.
   - (a) D ∈ 𝒞 and m ≥ 130: δ(D) ≥ −1 by Cor 8.8, so W ≥ 0 by Cor 4.3.
   - (b) D a cone tile and m ≥ 280: δ(D) ≥ −1 by Theorem 9.12, so W ≥ 0 by Cor 4.3.
   - (c) The remaining cases are 19 ≤ m ≤ 129 (any non-two-face D) and 130 ≤ m ≤ 279 (cone tiles).
     - By Lemma 10.2(d), D is an open-cone tile of Λ_{r(S)}. After the normalization by units and permutations it is
       one of the tiles enumerated for the canonical lattice, up to a permutation σ, and δ and the two-face property
       are σ-invariant.
     - The certified scan (§10.5) gives δ ≥ 0 for all such tiles with 24 ≤ m ≤ 279, and for 19 ≤ m ≤ 23 except the four
       listed tiles.
     - Among these: at m = 23, δ = −1 and Cor 4.3 applies. At m = 19 and m = 20, Prop 4.5 applies with the certified
       κ. The referee computed κ for every realizable (D, r), not only the canonical r; κ is invariant under units and
       equivariant under σ. ∎
     - (An earlier draft flagged [GAP G1] here, for cone tiles with 236 ≤ m ≤ 255. It is closed by E141; see §10.7.)

**Dependencies of Theorem 11.1.**
- External results: (E1) [Eli18]; (E2) [BGOW20].
- Computation: (FC), complete and area-certified for every m ≤ 280 (E140, E141). Trust base as in §10.7.
- Paper lemmas: §§3–9, all reviewed.
- Lean: the items marked in §12.

---

## 12. Verification status

Legend:
- *Paper*: a complete proof appears in this manuscript, taken from the record.
- *Review*: CR is the cone referee (`.research/reviews/cone_review_2026-10-18.md`) and ChR the chain referee
  (`.research/reviews/e4_chain_review_2026-10-18.md`). Both were independent adversarial AI agents, 2026-10-18; this is
  not human peer review.
- *Lean*: kernel-checked in Lean 4 / mathlib, with 0 `sorry` and only the axioms `propext`, `Classical.choice` and
  `Quot.sound`, per `lean/README.md` and PROOFS.
  - `lean/Wilf/ConeForest.lean` was added on 2026-10-18 while this manuscript was being written. PROOFS records it as
    "verified by the lead".
  - For that file I checked only that it contains no `sorry` and that a compiled `.olean` at least as new as the source
    exists. I did not rerun the axiom audit.
- *Comp.*: exact computational evidence. This is not part of the proof unless the row says so.

| § | Item | Paper | Review | Lean (theorem names) | Comp. / note |
|---|---|---|---|---|---|
| 3.1 | Facts N1–N5 | yes (classical) | — | N2 `genus_eq_sum_apery` (Basic.lean), N3 `aperyMax_eq` (Chains.lean) | — |
| 3.3 | Prop 3.1 (link 1: D down-set, \|D\| = m, bijections, e_a ∈ D) | yes | ChR | `isFactTile_factDownSetG`, `IsFactTile.isTile` (MaxCL.lean); (c) e_a ∈ D **not** in Lean | asserted on ≈ 50,000 S (ChR) |
| 3.3 | Prop 3.2 (CH′) | yes; KNOWN [Zhai11] | ChR | `IsFactTile.columnIdentity` | asserted (ChR) |
| 4.1 | Lemma 4.1 (lattice tile; closed-cone inequality) | yes | ChR | (a) as `IsTile`; (b) **not** in Lean | — |
| 4.2 | Thm 4.2 (height criterion), Cor 4.3 (δ ≥ −1 ⇒ Wilf) | yes | ChR (proposed Cor 4.3) | not in Lean | asserted on ≈ 50,000 S |
| 4.3 | Prop 4.5 (LP certificate) | yes | ChR (κ recomputed with HiGHS) | not in Lean | used at m = 19, 20 |
| 5.1 | Lemma 5.1 (top layer; TOP″ ⇒ Wilf) | yes | ChR | `wilf_of_TOP2` (Chains.lean); `wilf_of_tileTOPAt_of_isFactTile` | — |
| 5.1 | Lemma 5.2 (Cross Lemma) | yes | — | `crossLemma_two_mul_P2` (TauCrit.lean) | genus ≤ 20 (src/taucrit.py) |
| 5.1 | Cor 5.3 (τ-criterion, e = 4) | yes | ChR | `wilf_of_tauCriterion_P2` | — |
| 5.2 | Lemma 5.4 (two-face identity) | yes | ChR | not in Lean | 26,779 two-face S |
| 5.3 | Lemma 5.5 (F1–F5) | yes | ChR | not in Lean | as above |
| 5.4 | Lemma 5.6 (bounds A′, B″, C, D) | yes | ChR | (C) via `wilf_of_tauCriterion_P2`; rest not in Lean | as above |
| 5.5 | Thm 5.7 (two-face) | yes + finite check | ChR (reran m ≤ 500) | not in Lean | **computational part**: tf_bounds2.py, m = 18–74 needed; uses (E1), (E2) |
| 6 | Lemma 6.1 (cylinder lemma) | yes; (a) KNOWN [HRW18] | ChR | not in Lean | all tiles m ≤ 12 |
| 6 | Lemma 6.3 (𝒞 = projection-determined) | yes | ChR (link 4: "Cyl … is exactly class 𝒞") | (⇒) `LWClass.isLW` | — |
| 6 | Cor 6.5 (link 4: 𝒞 or cone tile) | yes | ChR | not in Lean | classification asserted on all tested tiles |
| 7.1 | Lemma 7.1 (CHT) | yes | CR, ChR | `cht` (CornerArea.lean; any finite D) | EXH4/5, TILES |
| 7.1 | Lemma 7.2 (Tri, qU, qO structure) | yes | CR | `qU_struct`, `triSet_succ_mem`, `qO_succ_mem` | — |
| 7.2 | Lemma 7.3 (level picture) | yes | CR, ChR | used inside `typeBound` | — |
| 7.3 | Lemma 7.4 (T: t ≤ C − 2) | yes | CR, ChR | `typeBound` | \|D\| ≤ 40 exhaustive |
| 7.3 | Lemma 7.5 (T′: t ≤ C) | yes | CR | `typeBound_cone`, `typeBound_cone'`, `faceCorners_coneCut`, `typeBound_cone_attained` (ConeType.lean) | union ≤ 34 |
| 7.4 | Lemma 7.6 (B: C² − 3C + 6 ≤ 6m) | yes | CR, ChR | `cornerArea` | tight examples |
| 8 | Lemma 8.1 ((P0), (P1)) | yes | CR, ChR | inside Forest.lean | — |
| 8 | Lemma 8.2 (S) | yes | CR, ChR | `lemmaS` | — |
| 8 | Lemma 8.3 (P) | yes | CR, ChR | `lemmaP` | \|D\| ≤ 17 |
| 8 | Lemma 8.4 (TF) | yes | CR, ChR | `tripodForest''` (also `tripodForest`, `tripodForest'`) | — |
| 8 | Lemma 8.5 (QF) | yes | CR, ChR | `qOForest` | — |
| 8 | Lemma 8.6 (F) | yes | CR, ChR | `qUForest` (different proof) | — |
| 8 | Thm 8.7 (C-HT: δ ≥ m + 14 − 5C) | yes | ChR | `forestBound`, `chtForest`, `deltaBound` | \|D\| ≤ 20 all down-sets (ChR) |
| 8 | Cor 8.8 (thresholds 131 / 130) | yes | ChR | `chtThreshold`, `chtThreshold'` (ConeForest.lean) | exact to 2·10⁵ (ChR), 10⁶ (here) |
| 9.1 | Lemma 9.1 ((P0′), (P1′), (Peak′)) | yes | CR | inside ConeForest.lean (`plateau_lt`, `qO_claim_cone`) | — |
| 9.2 | Lemma 9.2 (Wall) | yes | CR | **not** in Lean | all 13,299 cone tiles in logs/tiles |
| 9.2 | Lemma 9.3 (Floor; \|𝒴_d\| ≤ 2) | yes | CR | **not** in Lean (it is the Lean hypothesis) | same |
| 9.3 | Lemma 9.4 (S′, at most two directions) | yes | CR | `coneS`, `coneNoThree` | — |
| 9.3 | Lemma 9.5 (P′) | yes | CR | `coneP` | — |
| 9.4 | Lemma 9.6 (TF-cone: 2Tri ≤ t + 17) | yes | CR (2 wording fixes) | `tfCone`; sharper `tf_cone` | EXH5, TILES |
| 9.5 | Lemma 9.7 (F-cone: qU ≤ t + 2) | yes | CR | `fCone`; sharper `qU_cone` (qU ≤ t) | — |
| 9.6 | Lemma 9.8 (QF-pair) | yes | CR | `qO_claim_cone` | — |
| 9.6 | Cor 9.9 (Location) | yes | CR | `location_cone`, `IsDS.location` | — |
| 9.6 | Lemma 9.10 (Fiber) | yes | CR | `fiber`, `fiber_aux` | DS family Q = 4..14 |
| 9.7 | Thm 9.11 (qO-cone: qO ≤ 2t − 1 + 2\|𝒴\|) | yes | CR (all sub-claims) | `qOCone`; sharper `qO_cone` | EXH5, TILES |
| 9.8 | Thm 9.12 (cone: δ ≥ m − 6C − 29; 281 / 280) | yes | CR | `coneDeltaBound`, `coneThreshold`, `coneThreshold'` (hypothesis \|𝒴_d\| ≤ 2) | exact arithmetic to 2·10⁵ / 10⁶ |
| 9.8 | Remark 9.13 (δ ≥ m − 6C − 21; 267 / 266) | **no** (Lean only) | — | `coneDelta_sharp` | not used |
| 10 | Lemma 10.2, 10.3 (coverage, area certificate) | yes | ChR (coverage argument) | not in Lean | — |
| 10 | (FC) finite computation | — | ChR (method, bug, samples; fan-free check m ≤ 26) | not in Lean | **computational**; complete and area-certified for m = 4–280 (E140, E141); G1–G3 closed |
| 11 | Theorem A | assembly | — | not in Lean as a whole | **provisional** (E1, E2 cited; code trust); no open mathematical gap |

Not in Lean, and needed for a fully formal proof: Lemma 4.1(b), e_a ∈ D, Theorem 4.2, Cor 4.3, Prop 4.5, §5 (except
Cor 5.3), Lemma 6.1, Cor 6.5, Lemmas 9.2 and 9.3, §10, and the assembly. STATE.md's G-Lean lists the cylinder lemma and
Wall/Floor from `IsTile`, then the height criterion, as the next targets.

---

## 13. References

**External literature.**
- [Wil78] H. S. Wilf, A circle-of-lights algorithm for the "money-changing problem", Amer. Math. Monthly 85 (1978)
  562–565.
- [Eli18] S. Eliahou, Wilf's conjecture and Macaulay's theorem, J. Eur. Math. Soc. 20 (2018) 2105–2129;
  arXiv:1703.01761. Used: Thm 6.4 + Prop 6.2 ⇒ Cor 6.5 (c ≤ 3m ⇒ W₀ ≥ 0 ⇒ Wilf).
- [BGOW20] W. Bruns, P. A. García-Sánchez, C. O'Neill, D. Wilburne, Wilf's conjecture in fixed multiplicity, Internat.
  J. Algebra Comput. 30 (2020) 861–882; arXiv:1903.04342. Used: Thm 4.3 (m ≤ 18 ⇒ Wilf).
- [Zhai11] A. Zhai, arXiv:1111.2779 (2011). Thm 1; Lemmas 1 and 3 (= CH′). Known; not used as a black box.
- [HRW18] M. Hellus, A. Rechenauer, R. Waldi, arXiv:1804.06141 (2018). Prop 2.6(b) (= Lemma 6.1(a)), Prop 2.3/2.5,
  Remark 2.9. Known; not used as a black box.
- [Set26] K. Sethuraman, `kseth/wilf-e4`, GitHub, https://github.com/kseth/wilf-e4 (Sept 2026; HEAD caa574d). An
  earlier, different, computer-assisted proof of Theorem A. Partially audited by the project (LITERATURE §3 item 11).
- [Eli20] S. Eliahou, Electron. J. Combin. 27(2) (2020) P2.15; arXiv:1909.03699 (3e ≥ m ⇒ Wilf). Not used.
- [KS22] J. Kliem, C. Stump, Discrete Comput. Geom. 67 (2022) 1147–1173 (m ≤ 19 ⇒ Wilf; secondary). Not used.
- [FGH87] R. Fröberg, C. Gottlieb, R. Häggkvist, On numerical semigroups, Semigroup Forum 35 (1987) 63–83. Not used.
- [Sel77] E. S. Selmer, On the linear Diophantine problem of Frobenius, J. Reine Angew. Math. 293/294 (1977) 1–17
  (Fact N2).
- [BS62] A. Brauer, J. E. Shockley, On a problem of Frobenius, J. Reine Angew. Math. 211 (1962) 215–220 (Fact N3).
- [RGS09] J. C. Rosales, P. A. García-Sánchez, Numerical Semigroups, Developments in Mathematics 20, Springer, 2009
  (Ch. 2: Apéry sets).

**Project record** (all paths relative to the repository root).
- `.research/STATE.md`, section "The e = 4 argument (our route) and the status of each link".
- `.research/PROOFS.md`, sections:
  - "Factorization down-set D and the column identity CH′";
  - "Cylinder structure of 3-D tiles";
  - "THEOREM (two-face e = 4)";
  - "τ-criterion";
  - "e = 4, asymptotic HT via the counting criterion CHT";
  - "Cone tiles: wall and floor lemmas …";
  - "Cone tiles: QF-pair lemma, location corollary, Fiber Lemma, and qO ≤ 2t + 11".
- `.research/NOTEBOOK.md`: "2026-10-18 (night 13, cont.)" (height criterion); "2026-10-18 (night 17)" (TF-cone,
  F-cone; referee edits).
- `.research/reviews/cone_review_2026-10-18.md` and `.research/reviews/e4_chain_review_2026-10-18.md`.
- `lean/README.md`, and `lean/Wilf/{MaxCL, TauCrit, Chains, CornerArea, ConeType, Forest, ConeForest}.lean`.
- `.research/EXPERIMENTS.md`: E125, E132, E133, E136, E139, E140, E141.
- Logs:
  - certified: `logs/tsv16_4_119_fejer.log`, `tsv16_120_255_fejer.log` and `tsv16_256_280_fejer.log`;
  - earlier: `tile_scan_H.log`, `tile_scan_H_68.log`, `tile_scan_HM_*.log`, `tile_scan_C_118_130.log`,
    `tile_scan_C_gaps.log`, `tile_scan_C_131_280.log` and `tile_scan_C_226_280_fejer_uint8.log`;
  - other: `tf_bounds2.log` and `tile_enum_validate.log`.
- Code: `src/tile_enum.py`, `src/tile_lp.py`, `src/scratch/tf_bounds2.py`, `src/c/tile_scan.c`, `src/c/tile_scan_v.c`,
  `src/review2/`.
- `.research/LITERATURE.md` §1 (#13, #25) and §3 (items 11–15).

---

## Appendix A. Flagged gaps and inconsistencies between sources

### A.1 Gaps flagged in the text

- **G1 (§10.7, §11): CLOSED by E141.** Before the rerun, no enumeration in the record covered m = 236–255.
  - `logs/tile_scan_C_131_280.log` ends at m = 229, `logs/tile_scan_C_226_280_fejer_uint8.log` covers only 226–235,
    and the 16-bit log of E140 starts at 256.
  - So cone tiles with 236 ≤ m ≤ 255 were covered by no argument; this was the only mathematical gap.
  - `logs/tsv16_120_255_fejer.log` covers this range: HT fails 0, area-defects 0, min δ = 712.
- **G2 (§10.7, documentation): CLOSED by E141.** The referee report lists area certification for m = 7–40 (exact) and
  m = 19–30, 46–119 (mod p); m = 41–45 was not listed. `logs/tsv16_4_119_fejer.log` area-certifies every lattice for
  m = 4–119.
- **G3 (§10.7, trust): CLOSED by E141.** For 120 ≤ m ≤ 235, traversal completeness rested on the uint8 build without a
  per-lattice certificate. `logs/tsv16_120_255_fejer.log` certifies it, with identical lines on all 116 overlapping m.
- **G4 (§5.5, documentation): OPEN.** `logs/tf_bounds2.log` does not state the range of m that was run. PROOFS says 18–400;
  the referee independently reran 5–500 with the same result.

### A.2 Inconsistencies between sources

1. **STATE.md, link 7, and NOTEBOOK "2026-10-18 (midday)" overstated the scan before E141.**
   - STATE said "m = 131–255: HT 0 failures" and "every link 1–7 is now in place". NOTEBOOK says "every non-two-face
     tile with m ≤ 280 satisfies HT". Commit d969d2d says "all links of our e=4 route in place".
   - At that time the cited logs ended at m = 235 (G1).
   - The claim is now true by E141. But STATE link 7 still contains the superseded bullet "m = 131–255: HT 0 failures
     (… 131–229; … 226–235). The 8-bit build is valid for m ≤ 255", next to the new "Re-certification COMPLETE"
     sentence.
   - STATE's "Open gaps" still lists "G-scan: … (running)", and its "Next precise task" still says to wait for the
     scan. NOTEBOOK's last mention (line ≈1399) still says "The re-certification of m = 120–255 is still running"; the
     NOTEBOOK has no entry for E141.
2. **EXPERIMENTS E136** says "m = 131–280: RUNNING; … through m = 215". This is superseded: the local log ends at
   m = 229, the uint8 runs were not continued past 235, and E140 and E141 replace them. Also, E140's sentence "Old
   uint8 results stand for m ≤ 255" referred to results that existed only up to m = 235.
3. **PROOFS, end of the qO-cone section,** reads "Not formalized (Lemma B, CHT and T are in Lean; T′ and the forest
   lemmas are not)". This is stale: T′ (`typeBound_cone`), TF/F/QF (`Forest.lean`) and the cone lemmas
   (`ConeForest.lean`) are now in Lean, according to the same file's later paragraph, STATE and README.
4. **PROOFS, "Integrality sharpening" paragraph** (after Theorem C-HT). It says the HT scan is "complete so far for
   m ≤ 82, 91–95, 101–104, 109–111", and that cone tiles "need a separate bound". Both are stale: the scan is complete
   to 130, and Theorem 9.12 now supplies the bound.
5. **STATE.md "Open gaps"** still lists "G-review: the adversarial review of TF-cone, F-cone, qO-cone, T′, B and the
   threshold arithmetic", while the same file reports both reviews as COMPLETE.
6. **NOTEBOOK "midday"** says "The cone forest bounds are in progress" in Lean. STATE, PROOFS and README now report
   them kernel-checked (`ConeForest.lean`).
7. **Two-face analytic constants.**
   - PROOFS: region (I) needs "m ≥ 38", and region (II)'s endpoints "need m ≥ 28 and m ≥ 35".
   - Chain referee: 37, and 27 and 35.
   - My recomputation agrees with the referee: m + 2L² − 18L + 3 ≥ m − 37, and m² − 27m + 20 ≥ 0 for m ≥ 27.
   - Both versions suffice for m ≥ 75; PROOFS's constants are valid but not sharp.
8. **Two-face finite range.** STATE and the PROOFS header say "exact finite check m ∈ [18, 74]", and the PROOFS body
   says "18 ≤ m ≤ 400". These are consistent: the range needed is [18, 74], and it was checked to 400. The log does not
   record either range (G4).
9. **`src/scratch/tf_bounds2.py`.** The header comment for A′ says "Def2D ≥ m(2m + L3 − …)", while the code and PROOFS
   use m(m + 2L₃ − …). The code is correct; the comment is a typo.
10. **PROOFS, Cross Lemma (τ-criterion section),** step (1) reads "u′ = u + j·n_a ≥ c + n_a > c + m". Here n_a should be
    p_a, the generator.
11. **Area-certified range (referee).** STATE says the referee certified "m = 19–119 (C, mod p)"; the referee report
    says "m = 19–30 and 46–119" (G2). This is now moot, since E141 certifies every m ≤ 119.
12. **Cone constants.** The paper chain (PROOFS Corollary, STATE link 6, this manuscript) uses δ ≥ m − 6C − 29 and
    thresholds 281/280. Lean also proves the sharper δ ≥ m − 6C − 21 with thresholds 267/266 (PROOFS, STATE); README
    lists `coneThreshold` at m ≥ 281. These are consistent, but the record has no paper proof of the sharper form
    (Remark 9.13).
13. **Theorem qO-cone headline typo** "t − 1 + 2|Y|". It has been corrected to 2t − 1 + 2|Y|, and the false version
    (counterexample m = 243) is preserved in the record and here.
14. **examples/qO_lattice_free_family.md vs src/scratch/ds_family.py** (reported by the cone referee): G has length
    Q + 2 vs Q + 1, and h(0) = Q + 2 vs Q + 1. The table matches the code. This family is outside the proof chain, and I
    did not recheck it.
15. **Attribution of the cylinder lemma** (chain referee): "(b) is HRW Prop 2.6" (old STATE) vs "(a) = HRW Prop 2.6(b)"
    (PROOFS). This is resolved in the current STATE, which says "its part (a) is HRW Prop 2.6(b)". Per LITERATURE item
    15, the collision rule behind (b) also appears in HRW and in Sethuraman.

