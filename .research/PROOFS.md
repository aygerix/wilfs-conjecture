# PROOFS.md — precise statements, proofs, dependency graph, status

> Current handoff: [STATE.md](STATE.md). Binding user rules: [DIRECTIVES.md](DIRECTIVES.md).

Status legend: PROVED (on paper, here) | CHECKED (exact computation, stated range) | CONJ | FALSE | LEAN (kernel-checked)

Notation. S ≠ ℕ numerical semigroup, multiplicity m ≥ 2, conductor c, F = c−1, genus g, n = ell = c − g,
P minimal generators, e = |P|, P' = P∖{m} = {p_1,…,p_d}, d = e − 1 ≥ 1.
Ap = Ap(S,m) = {w_0 = 0, …}, M = max Ap = F + m = c + m − 1 (Brauer–Shockley). W(S) = e·n − c.
For w ∈ Ap and a ∈ [d]: ν_a(w) = max{k ≥ 0 : w − k p_a ∈ S}.
Facts used (standard, elementary): (i) g = Σ_{w∈Ap} (w − (w mod m))/m = (Σ_{w∈Ap} w)/m − (m−1)/2 (Selmer);
(ii) M = F + m; (iii) if w ∈ Ap and w = x + y with x, y ∈ S then x, y ∈ Ap (summand closure);
(iv) every w ∈ Ap∖{0} is a sum of elements of P' (m cannot appear in a factorization of an Apéry element).

---------------------------------------------------------------------------------------------------
## Identity CH (chain identity) — PROVED 2026-10-17; CHECKED genus ≤ 18 (src/chains.py)

For a ∈ [d], call a maximal arithmetic progression with difference p_a contained in Ap a *p_a-chain*.
The p_a-chains partition Ap. Let Def_a = Σ_{C p_a-chain} |C|·(M − top(C)) and
E = Σ_{w∈Ap} E(w), E(w) = Σ_a p_a ν_a(w) − w. Then

    m·W(S) = Σ_{a=1}^{d} Def_a + E − (d−1)·m(m−1)/2,   with Def_a ≥ 0 and E ≥ 0.

Proof. (1) For a chain C = {b, b+p_a, …, b+(L−1)p_a}: b − p_a ∉ S (else b − p_a ∈ Ap by (iii) and C not
maximal), so ν_a(b + k p_a) = k by (iii). Hence Σ_{w∈C}(w + p_a ν_a(w)) = Σ_k (b + 2k p_a) = L(b+(L−1)p_a)
= |C|·top(C). Summing over chains: Σ_{w∈Ap} w + p_a Σ_w ν_a(w) = Σ_C |C| top(C), so
Def_a = mM − Σ_w w − p_a Σ_w ν_a(w) ≥ 0 since top(C) ≤ M.
(2) Σ_a Def_a + E = d mM − dΣw − Σ_w Σ_a p_aν_a(w) + Σ_wΣ_a p_aν_a(w) − Σw = d mM − (d+1)Σ_w w.
(3) By (i),(ii): W = e(c−g) − c = d c − (d+1) g, and c = M − m + 1, g = Σw/m − (m−1)/2, so
m W = d m(M − m + 1) − (d+1)Σw + (d+1)m(m−1)/2 = d mM − (d+1)Σw − (d−1)m(m−1)/2.
(4) E(w) ≥ 0: take any factorization w = Σ n_a p_a (by (iv)); then w − n_a p_a ∈ S so ν_a(w) ≥ n_a and
Σ p_a ν_a(w) ≥ w. ∎

### Corollary H (homogeneous / "continuous" Wilf) — PROVED
(d+1)·Σ_{w∈Ap} w ≤ d·m·M, i.e. mean(Ap) ≤ (d/(d+1))·max(Ap). Equivalently m·W ≥ −(d−1)m(m−1)/2,
i.e. Wilf holds up to the additive error (d−1)(m−1)/2:  e·n ≥ c − (e−2)(m−1)/2.
(Immediate from CH. This is a discrete divergence-theorem argument on the Apéry down-set; it shows
Wilf is exactly "homogeneous Chebyshev inequality + a discrete correction of size (d−1)m(m−1)/2".)
Novelty: **KNOWN** — this is Zhai, arXiv:1111.2779 (2011), Thm 1 (e·n ≥ c − (e−2)(m−1)/2); CH′ is Zhai's Lemmas 1+3
in exact form (per the 2026-10-18 audit; LITERATURE §3 item 12).

---------------------------------------------------------------------------------------------------
## Lemma A (top-layer reduction) — PROVED 2026-10-17

Let X_q = Ap ∩ [c, c+m) (top layer), π(u) = u − c + 1 ∈ [1, m] for u ∈ X_q, and
ℓ(u) = min{|n| : u = Σ n_a p_a, n ∈ ℕ^d} (shortest factorization over P'). Then

    m·W(S) ≥ m((d+1)m + d − 1)/2 − Σ_{u∈X_q} π(u)(d + ℓ(u))  +  Σ_{w∈Ap∖X_q} E(w).

Proof. Every u ∈ X_q is a chain top in every direction a (u + p_a ≥ c + m > M), and the p_a-chain
with top u has length ν_a(u) + 1. Every other chain top t lies in Ap∖X_q, so t < c and M − t ≥ m.
The chains of direction a have total length m. Hence, with Λ(u) = Σ_a (ν_a(u)+1) and
M − u = m − π(u):
  Σ_a Def_a ≥ Σ_{u∈X_q} Λ(u)(m − π(u)) + m(dm − Σ_{u∈X_q}Λ(u)) = dm² − Σ_{u∈X_q} π(u)Λ(u).
For u ∈ X_q fix a shortest factorization n (|n| = ℓ(u)); ν_a(u) ≥ n_a and π(u) ≤ m < p_a give
  π(u)Λ(u) − E(u) = d π(u) + Σ_a ν_a(u)(π(u) − p_a) + u ≤ d π(u) + Σ_a n_a(π(u) − p_a) + u = π(u)(d + ℓ(u)).
Insert in CH and use dm² − (d−1)m(m−1)/2 = m((d+1)m + d − 1)/2. ∎

### Conjecture TOP'' (top-layer inequality) — CONJ; CHECKED genus ≤ 18 (all 33,281 S ≠ ℕ),
### tight exactly on the 79 semigroups with W = 0 in that range; extended runs in EXPERIMENTS.md

    Σ_{u∈X_q} π(u)·(d + ℓ(u)) ≤ m((d+1)m + d − 1)/2.

Equivalent form: with Π = π(X_q) ⊆ [1,m] and Π^c = [1,m]∖Π (positions j with c−1+j−m ∈ S, i.e. the
left elements of the last level [c−m, c)):

    Σ_{u∈X_q} π(u)·ℓ(u) ≤ m(m−1)/2 + d·Σ_{j∈Π^c} j.

TOP'' ⇒ Wilf (Lemma A). Equality cases: e = 2 (X_q = {M}, ℓ(M) = m−1, Π^c = [1,m−1]) and
S = T_{m,q} = mℕ ∪ [qm,∞) (X_q = right primitives, ℓ = 1, Π^c = {1}).

---------------------------------------------------------------------------------------------------

## τ-criterion: Wilf when few pseudo-Frobenius numbers lie in [c−m, c) — PROVED 2026-10-18; **LEAN-CHECKED 2026-10-18**
## (lean/Wilf/TauCrit.lean: crossLemma, crossLemma_two_mul_P2, top2_of_tauCriterion, wilf_of_tauCriterion,
## wilf_of_tauCriterion_P2, wilf_of_embDim_four_tau_le_four (m ≥ 13), wilf_of_embDim_four_tau_le_five (m ≥ 19),
## wilf_of_tau_le_embDim_sub_one (m ≥ 3e−4); axioms propext, Classical.choice, Quot.sound; lake build OK, 0 sorryAx,
## verified by the lead). Every step also asserted on all 93,141 semigroups S ≠ ℕ of genus ≤ 20 (src/taucrit.py).
## Lean simplifications: (1)+(2) are one fact — distinct top-layer cells are incomparable (n(u) ≤ n(u') ⇒ u' ≥ u+p_a);
## any common cell of cross(y) ∩ cross(y') (y, y' incomparable) equals min(y, y'); the double count is the pointwise
## 2j ≤ 2 + j(j−1). TOP'' follows from the criterion for e ≥ 2. Lean `topPairs2` counts ORDERED pairs (= 2·P₂).
Notation: m, c, e, d = e − 1, P' = minimal generators other than m, X := X_q = Ap(S,m) ∩ [c, c+m),
τ := |X| = |{f ∈ PF(S) : f ≥ c − m}| (u ↦ u − m is a bijection X → PF ∩ [c−m, c); so 1 ≤ τ ≤ t(S)),
ℓ(u) = shortest factorization length over P', n(u) = grlex-least factorization (|n(u)| = ℓ(u)),
D = {n(w) : w ∈ Ap} (grlex factorization down-set, |D| = m, CH' (a),(b)).
**Cross Lemma.** Σ_{u∈X} (ℓ(u) + 1) ≤ m + P₂, where P₂ := #{{u,u'} ⊆ X : n(u), n(u') differ in exactly two coordinates}
≤ C(τ,2).
Proof. cross(y) := {y − k e_a : a ∈ [d], 0 ≤ k ≤ y_a} has |y| + 1 cells and lies in [0,y] ⊆ D for y ∈ D.
(1) For u ≠ u' in X no cell lies in cross(n(u)) ∩ cross(n(u')) through the same direction a: else n(u), n(u') lie on one
line x + ℕe_a, say n(u') = n(u) + j e_a (j ≥ 1), and u' = u + j·p_a ≥ c + p_a > c + m, contradicting u' ∈ X.
(2) Likewise n(u) ∉ cross(n(u')) (it would give n(u') = n(u) + k'e_b, k' ≥ 1). Hence a common cell x has
n(u) = x + k e_a, n(u') = x + k' e_b with a ≠ b, k, k' ≥ 1: n(u), n(u') differ exactly in coordinates a, b, and x is
determined by the pair (x_a = n(u')_a, x_b = n(u)_b, other coordinates common).
(3) With j(x) = #{u : x ∈ cross(n(u))}: Σ_u(ℓ(u)+1) = Σ_x j(x) = |∪ crosses| + Σ_x (j(x) − 1)⁺ ≤ m + Σ_x C(j(x),2) ≤ m + P₂,
since each pair has at most one common cell. ∎
**Theorem (τ-criterion).** If e ≥ 3 and (e−2)(m+1) ≥ 2(e−2)τ + 2P₂ — in particular if (e−2)(m+1) ≥ τ(τ + 2e − 5) —
then S satisfies Wilf (e·(c−g) ≥ c).
Proof. π(u) := u − c + 1 ≤ m on X, so by the Cross Lemma
  Σ_{u∈X} π(u)(d + ℓ(u)) ≤ m·Σ_u (ℓ(u) + 1 + (d−1)) ≤ m(m + P₂ + (d−1)τ) ≤ m((d+1)m + d − 1)/2,
the last step being the hypothesis (d − 1 = e − 2). This is TOP'' (Lean `TOP2`), and TOP'' ⇒ Wilf is Lemma A
(Lean `wilf_of_TOP2`). With P₂ ≤ τ(τ−1)/2 the hypothesis follows from (e−2)(m+1) ≥ τ(τ−1) + 2(e−2)τ. ∎
**Corollaries.**
(a) e = 4: Wilf whenever m + 1 ≥ τ(τ+3)/2. With 3e ≥ m ⇒ Wilf (Eliahou 2020, LITERATURE #21) for m ≤ 12:
    **Wilf holds for every S with e = 4 and τ ≤ 4** (no computer verification used). With m ≤ 19 (Kliem–Stump, #26,
    computational): **every S with e = 4 and τ ≤ 5**.
(b) Every e: if τ ≤ e − 1 then Wilf (if m ≥ 3e − 4: τ(τ+2e−5) ≤ 3(e−1)(e−2) ≤ (e−2)(m+1); else 3e > m, #21).
    Since τ ≤ t(S), this contains the whole FGH range t ≤ e − 1 (LITERATURE #2), and it applies to S of arbitrarily
    large type as long as few PF numbers lie in the last layer [c−m, c).
(c) Asymptotically: Wilf whenever τ ≤ √((e−2)(m+1)) − (e − 5/2) roughly.
Evidence/checks: src/taucrit.py G asserts, for every S of genus ≤ G: |n(u)| = independent shortest-length DP value;
each cross has |y|+1 cells inside D; overcount ≤ P₂; Cross Lemma; criterion ⇒ TOP''. G = 20: 93,141 semigroups, all
assertions pass; 68,221 satisfy the criterion, 195 of them with t ≥ e (outside the FGH range).
Novelty: UNVERIFIED. Limited search (Delgado survey 1610.08726, BGOW 1903.04342, Marashdeh 2608.12531, alphaXiv
discovery for type/PF-based Wilf criteria, 2026 e = 4 Apéry papers 2604.25653, 2609.04000) found no equivalent statement.
Marashdeh 2026 states no theorem in the literature takes t ≥ e as hypothesis.
Mechanism: top-layer Apéry elements are pairwise incomparable "far apart" points of the factorization down-set; their
crosses are almost disjoint (one common cell per pair at most), so Σ ℓ ≤ m + C(τ,2).

---------------------------------------------------------------------------------------------------
## Cylinder structure of 3-D tiles — PROVED 2026-10-18 (paper); CHECKED all 3-D tiles m ≤ 12 (src/scratch/cylinder.py)
Setting: D ⊂ ℕ³ a finite down-set that is a fundamental domain of a lattice Λ ⊂ ℤ³ (ℤ³ = ⊔_{λ∈Λ}(D+λ); e.g. every
e = 4 Apéry factorization tile, Λ = ker φ). G := minimal elements of ℕ³∖D; π_c = projection forgetting coordinate c;
L_c := |D ∩ ℕe_c|.
**Lemma.** (a) At most one q ∈ G has full support, and such q* lies in Λ. [KNOWN: Hellus–Rechenauer–Waldi, arXiv:1804.06141, Prop 2.6(b).]
(b) If q ∈ G has q_c = 0 < q_a, q_b ({a,b,c} = {1,2,3}) then q ≡ t·e_c (mod Λ) for a unique t with t·e_c ∈ D, and
    distinct such q (same c) have distinct t. Hence the slice π_c(D) (= D ∩ {x_c = 0}) has ≤ L_c non-axis inner corners.
(c) D = {x ∈ ℕ³ : π_c(x) ∈ π_c(D) for c = 1,2,3} ∖ (q* + ℕ³): a 3-D tile is the largest down-set with its three
    coordinate projections, minus at most one cone (a "cylindrical" set).
Proof. q ∈ G lies in a unique D + λ with λ ≠ 0. For each a with q_a ≥ 1, q − e_a ∈ D, so q − e_a ∉ D + λ (translates
are disjoint), i.e. q − λ − e_a ∉ D; as q − λ ∈ D and D is a down-set this forces (q − λ)_a = 0. (a): full support ⇒
q − λ = 0, q ∈ Λ; two such q ≠ q' give (q − e_1) − (q' − e_1) ∈ Λ∖0 with both in D, impossible. (b): q − λ = t e_c;
equal t for q ≠ q' gives the same contradiction with q − e_a, q' − e_a. (c): x ∉ D ⇔ x ≥ some q ∈ G; if q_c = 0 this
is π_c(x) ≥ π_c(q) ∉ π_c(D), i.e. π_c(x) ∉ π_c(D) (D down-set ⇒ π_c(D) = D ∩ {x_c = 0}); the only other case is q*. ∎
Consequences. (i) Column tops: t_a(x)_a + 1 = min(R_a^{(b)}(x_c), R_a^{(c)}(x_b), Q_a(x_b,x_c)), R_a^{(b)}(γ) = length of
the a-row at height γ in π_b(D), Q_a = q*_a if x_b ≥ q*_b and x_c ≥ q*_c (else ∞). (ii) Every horizontal slice
D ∩ {x_c = γ} = π_c(D) ∩ [0, R_a^{(b)}(γ)) × [0, R_b^{(a)}(γ)) minus a quadrant (if γ ≥ q*_c). (iii) Simplices Δ_k
(k ≥ 3) are not tiles (C(k,2) > 1 full-support generators): the reason top layers stay O(√m) (E101). (iv) Two-face ⇔
(1,1,0)-type corner: e_a + e_b ∉ D ⇔ π_c(D) ⊆ {x_a x_b = 0}, and then e_a + e_b ≡ t e_c, t e_c ∈ D.
Novelty: UNVERIFIED (likely known in the language of Artinian lattice ideals / Gomory group problems in 3 variables:

### Cylinder lemma in every dimension — PROVED 2026-10-18 (the 3-D proof is dimension-free); CHECKED 1,200 random tiles e = 4, 5, 6
Setting: D ⊂ ℕ^d a finite down-set that is a fundamental domain of a lattice Λ ⊂ ℤ^d; G = minimal elements of ℕ^d ∖ D.
**Lemma.** (a) For q ∈ G let y(q) be the cell of D with q − y(q) ∈ Λ. Then supp y(q) ∩ supp q = ∅.
(b) If q ≠ q′ ∈ G and supp q ∩ supp q′ ≠ ∅, then y(q) ≠ y(q′). Hence for every nonempty τ ⊆ [d]:
    #{q ∈ G : supp q ⊇ τ} ≤ |D ∩ {x : x_τ = 0}|. In particular at most one q* ∈ G has full support, and q* ∈ Λ.
(c) D = Cyl(D) ∖ (q* + ℕ^d) (no orthant removed if q* does not exist), where Cyl(D) = {x : x|_{x_c := 0} ∈ D ∀c}.
Proof. (a) As in 3-D: q − e_a ∈ D for a ∈ supp q, so q − λ − e_a ∉ D for λ = q − y(q) ≠ 0, which forces y(q)_a = 0.
(b) If y(q) = y(q′) and a ∈ supp q ∩ supp q′, then (q − e_a) − (q′ − e_a) ∈ Λ ∖ 0 with both in D. τ = [d] gives y = 0.
(c) x ∉ D ⇔ x ≥ some q ∈ G; if q_c = 0 this says x|_{x_c := 0} ∉ D; the only q with no zero coordinate is q*. ∎
Consequences. Every lattice tile is in class 𝒞_d (= Cyl) or the cone class Cyl ∖ (q* + ℕ^d), in every d. The facets
D ∩ {x_c = 0} are not tiles in general: they may have up to L_c full-support (in d − 1 coordinates) corners.
Simplices {|x| ≤ n} (n ≥ d) are not tiles. Two-face (e_a + e_b ∉ D) ⇔ y(e_a + e_b) is supported off {a, b}.
Novelty: UNVERIFIED (part (a) for d = 3 is HRW Prop 2.6(b); the general statement is likely folklore for Artinian
lattice ideals). Check: src/scratch/cyl_d.py.
"at most one Gröbner leading term of full support"); not searched yet.

---------------------------------------------------------------------------------------------------
## THEOREM (two-face e = 4): Wilf holds for every S with e = 4 whose factorization tile is two-face —
## PROVED 2026-10-18 (paper + exact finite check m ∈ [18, 74], src/scratch/tf_bounds2.py, logs/tf_bounds2.log);
## every intermediate inequality asserted on 26,779 two-face semigroups (src/scratch/tf_verify.py)
Setting. e = 4, P' = {p_a, p_b, p_c}, D = grlex factorization tile (CH'), "two-face": e_a + e_b ∉ D for some pair
(equivalently D ∩ {x_a ≥ 1, x_b ≥ 1} = ∅; sufficient: p_a + p_b − m ∈ S). Then D = F_1 ∪ F_2 with F_1 = D ∩ {x_b = 0},
F_2 = D ∩ {x_a = 0} (2-D down-sets), F_1 ∩ F_2 = axis {k e_c : k < L_3}; N_i = F_i ∖ axis, |N_1| + |N_2| = m − L_3.
X = Ap ∩ [c, c+m) (top layer), π(u) = u − c + 1, A_top = (L_3 − 1)p_c.
**Two-face identity (exact).** Call the rows of F_1 (direction a), rows of F_2 (direction b) and all c-columns the
*2-D runs* (total length 2m + L_3; each starts at coordinate 0 in its direction). With
Def2D = Σ_{2-D runs R} |R|(M − w(end R)) and Def2D' = the same sum without the axis c-column:
    3m·W + 3m(m−1) = (m − 4L_3)·M + 4·Def2D + 2p_c·L_3(L_3−1) = m·M + 4·Def2D' − 2p_c·L_3(L_3−1).
Proof. Columns of D: b-columns through N_1 and a-columns through N_2 are singletons; all other columns are 2-D runs.
CH' gives mW + m(m−1) = Σ_{x∈N_1∪N_2}(M − w(x)) + Def2D. The AP identity on each run (Σ_{x∈R}(w(x) + p_δ x_δ) =
|R|w(end)) summed over all 2-D runs gives 3Σ_D w + Σ_axis w = (2m + L_3)M − Def2D. Eliminate Σ_D w; Σ_axis w = p_c
L_3(L_3−1)/2; the axis column contributes L_3(M − A_top) to Def2D. ∎ (Algebraically it is CH' rewritten; the content
is that singleton columns make each face "2-dimensional": mean ≈ (2/3)·max on a face, not (3/4).)
**Combinatorial facts.** (F1) X ⊆ maximal cells; maximal cells of N_i are the outer corners of F_i (distinct rows and
columns); the axis top is maximal iff it is an outer corner of both faces (then no off-axis corner at height L_3 − 1).
Let x_i = |X ∩ N_i|, x_ax = [A_top ∈ X], τ = x_1 + x_2 + x_ax. Then x_i(x_i+1)/2 ≤ |N_i| (distinct column heights) and
x_i ≤ L_3 − x_ax. (F2) u ∈ X ∩ N_1 at (i,0,k) ends exactly two 2-D runs, of total length R(u) = |u| + 2; the axis top
ends runs of total length L_3 + 2 (2 without the axis column). (F3) crosses of X ∩ N_1 pairwise meet in exactly one
(non-axis) cell, no triple meets, and lie in N_1 ∪ {axis cells at their heights}: Σ_{X∩N_1}(|u|+2) ≤ |N_1| + 2x_1 + C(x_1,2).
(F4) runs ending below c have deficit ≥ m; runs ending at u ∈ X have deficit M − u = m − π(u), and these are distinct.
(F5) P₂ ≤ C(x_1,2) + C(x_2,2) + x_ax(x_1+x_2) + min(x_1,x_2) (cross-face pairs differ in exactly two coordinates
only at equal height).
**Four bounds** (each ⇒ W ≥ 0):
 A' (needs c > 3m, so M ≥ 4m; L_3 ≤ m/4): 3mW + 3m(m−1) ≥ 4m(m − 4L_3) + 2(m+1)L_3(L_3−1) + 4·Def2D with
    Def2D ≥ m(m + 2L_3 − 2(x_1+x_2) − C(x_1,2) − C(x_2,2) − x_ax(L_3+2)) + 3C(τ,2)    [F2–F4; positions distinct].
 B'' (m ≥ 2L_3): 3mW + 3m(m−1) ≥ (L_3−1)(m+1)(m − 2L_3) + 4·Def2D' (M ≥ A_top) with
    Def2D' ≥ m(m + L_3 − 2(x_1+x_2) − C(x_1,2) − C(x_2,2) − 2x_ax) + 2C(τ,2).
 C  (τ-criterion, LEAN): m + 1 ≥ 2τ + P₂, with F1, F5.
 D  (any L_3): rows of F_i at heights k ≥ H_i := height of column 1 of F_i are single axis cells with deficit
    ≥ (L_3−1−k)p_c, so 3mW + 3m(m−1) ≥ p_c·G, G = m(L_3−1) − 2L_3(L_3−1) + 2h(H_1) + 2h(H_2), h(H) = (L_3−H)(L_3−H−1)⁺,
    1 ≤ H_i, H_1 + H_2 ≤ m − L_3; W ≥ 0 if G ≥ 0 and (m+1)G ≥ 3m(m−1).
**Proof of the Theorem.** c ≤ 3m: Eliahou (LITERATURE #13, READ). m ≤ 17: BGOW m ≤ 18 (#25, READ). Otherwise, for
every (m, L_3) one of A', B'', C, D holds for ALL feasible (x_1, x_2, x_ax, H_1, H_2): exact check for 18 ≤ m ≤ 400
(tf_bounds2.py: no uncovered pair for m ≥ 18), and for m ≥ 75 analytically: L_3 ≤ m/4 by A' (already
m + 2L_3² − 18L_3 + 3 ≥ 0 for m ≥ 38); m/4 < L_3 ≤ m/2 − 4 by B'' (concave in L_3, endpoints need m ≥ 28 and m ≥ 35);
L_3 > m/2 − 4 by C (2τ + P₂ ≤ cap + 2.5(x_1+x_2) + 2 ≤ cap + 5√cap + 2 with cap = m − L_3 < m/2 + 4, ≤ m+1 for m ≥ 75). ∎
Scope: 36,279 of the e = 4 semigroups with m ≤ 18, generators < 4m, are two-face (all t = 0,1,2,...; boxes, L-shapes,
hook unions). Contains the box family ⟨a², a²+1, a²+a, a²+a+1⟩ (where the τ-criterion fails) and every e = 4 S with two
generators p_a + p_b ≥ c + m. Remaining for e = 4: NON-two-face tiles (all p_a + p_b ∈ Ap(S,m)).
Novelty: UNVERIFIED (limited check: not a gluing in general — Singh–Srinivasan #29 needs a gcd split; no e = 4
two-face statement in the literature notes).
Proof-relevant computer use: tf_bounds2.py (pure integer inequalities in (m, L_3, x, H), no semigroup enumeration).
Lean: not yet formalized (candidates: the identity — it is CH' plus AP sums — and the four bounds).

---------------------------------------------------------------------------------------------------
## Factorization down-set D and the column identity CH' — PROVED 2026-10-17
Fix a monomial order ≺ on ℕ^d. For w ∈ Ap let n(w) be the ≺-least factorization of w over P' (exists by (iv)).
D := {n(w) : w ∈ Ap}. Then (a) |D| = m and φ(n) := ⟨n,p⟩ mod m is a bijection D → ℤ/m;
(b) D is a down-set: if n = n(w), n' ≤ n then w' = ⟨n',p⟩ ∈ Ap by (iii), and n' = n(w') (else n'' ≺ n' with
⟨n'',p⟩ = w' gives n''+(n−n') ≺ n, a smaller factorization of w); (c) e_a ∈ D for all a (p_a minimal generator).
For direction a, the *a-columns* are the maximal sets {b, b+e_a, …, b+(L−1)e_a} ⊆ D (b_a = 0); top = b+(L−1)e_a.
Column identity: with w(n) = ⟨n,p⟩ (integers), Σ_{x∈C}(w(x) + p_a x_a) = |C|·w(top C) (sum of an AP), hence
    Σ_a Σ_{a-columns C} |C|·w(top C) = (d+1)·Σ_{w∈Ap} w,
    Σ_a Σ_C |C|·(M − w(top C)) = d m M − (d+1)ΣAp = m·W + (d−1)·m(m−1)/2.            (CH')
(Same algebra as CH step (3).)  Every term M − w(top C) ≥ 0.

## Conjecture CL (Carry Lemma) — **FALSE** (2026-10-17, E47: S = ⟨14,22,23,57,61,62,63⟩, LHS 441 < 455;
## examples/CL_counterexample.md). Previously CHECKED genus ≤ 24 (E13). CL ⇒ Wilf is PROVED (premise false).
## Surviving restricted form (CONJ): CL for S with 3e < m and c > 3m (0/1664 failures, E48); with LITERATURE #13, #21
## it would imply Wilf.
For S as above (any monomial order):
    Σ_a Σ_{a-columns C} |C|·((M − w(top C)) mod m)  ≥  (d−1)·m(m−1)/2.                  (CL)
Proof of CL ⇒ W(S) ≥ 0: x ≥ (x mod m) for x ≥ 0, so by CH' m·W + (d−1)m(m−1)/2 ≥ LHS(CL) ≥ (d−1)m(m−1)/2. ∎
Exact relation: m·W = m·Σ_aΣ_C|C|·⌊(M − w(top C))/m⌋ + [LHS(CL) − (d−1)m(m−1)/2]  (depth part + CL slack).
CL ⇒ TOP'' (slack(TOP'') = m·W − Σ_{low D-column tops}|C|(F − t), verified numerically; see NOTEBOOK).

### Tile-CL (the depth-free general form) — **FALSE** (E47: tile of the CL counterexample, slack −1 at s = 13; upper
### bound also fails, E47/E51). Previously CHECKED exhaustively for small tiles (E15: d=2 m≤15, d=3 m≤11, d=4 m≤8).
### PROVED for d = 2 (every 2-D tile, corner-sum proof, 2026-10-17 night 11, section below); PROVED for boxes in every d.
Data: d ≥ 1; D ⊆ ℕ^d a down-set with |D| = m; p ∈ (ℤ/m)^d with φ(n) = Σ n_a p_a mod m bijective on D
(equivalently D is a fundamental domain of the lattice Λ = ker φ). T(y) := Σ_{a : y+e_a ∉ D} (y_a + 1)
(= Σ over the columns topped by y of their lengths). Claim: for every s ∈ ℤ/m
    f(s) := Σ_{y∈D} T(y)·⟨s − φ(y)⟩  ≥  (d−1)·m(m−1)/2,      ⟨x⟩ := x mod m ∈ [0,m).        (Tile-CL)
CL for S is Tile-CL for (D, p mod m) at s = M mod m.  Directions a with D ⊆ {x_a = 0} add m(m−1)/2 to both sides.
Equivalent forms (all PROVED equivalent for tiles, using only Σ_y⟨σ+φ(y)⟩ = m(m−1)/2 and linear algebra):
 (II)  Σ_y T(y)·r(y) ≤ (d+1)·m(m−1)/2 for every labeling r = ⟨σ + φ⟩ (σ ∈ ℤ/m);   [r = m−1−R]
 (Diff) Σ_a Σ_{x∈D} (r(top_a x) − r(x)) ≤ Σ_{x∈D} r(x) = m(m−1)/2, top_a x = top of x's a-column;
 (Win) with c_a(y) = a-coordinate of φ^{-1}(y), Ȳ_a = mean of c_a, p̂_a ∈ [0,m) the residue of p_a:
       Φ(t) := Σ_a Σ_{j=1}^{p̂_a} (c_a(t+j) − Ȳ_a) ≥ −(m−1)/2 for all t   (f(t) − d m(m−1)/2 = m·Φ(t));
 (Wall) with N(y) = σ + ⟨y,p̂⟩, k = ⌊N/m⌋, r = N mod m:  Σ_y k(y) ≤ σ + Σ_y Σ_a y_a·[r(y) < p̂_a];
 (Walk) U(s) = Σ_{y=1}^{s}(T(φ^{-1}y) − d): max_s U − mean U ≤ (m−1)/2.
Two-sided corollary: applying Tile-CL to −φ gives |Φ(t)| ≤ (m−1)/2, so the residue-interval discrepancy
|Σ_{y∈I}(T(φ^{-1}y) − d)| ≤ m − 1 for every cyclic interval I (conditional on Tile-CL).
Local cell formula (PROVED): f(s) − (d−1)m(m−1)/2 = Σ_{z∈D} γ(z), γ(z) = (|z|+1)R(z) − Σ_a z_a R(z−e_a),
R = ⟨s − φ⟩ extended Λ-periodically; independent of shelling order.
Tightness families: e = 2 (single column); simplex tile {0, e_1..e_{m−1}} (T_{m,q}); "perfect" tiles where
⟨·,p̂⟩ maps D bijectively onto [0, m−1] (e.g. lex boxes) at s = −1.

### Ramp Lemma — PROVED 2026-10-17 (any down-set; no tiling hypothesis)
Let D ⊆ ℕ^d be a finite down-set, T(y) = Σ_{a: y+e_a∉D}(y_a+1), β = d+1−T, top_a x = top of x's a-column.
Call ρ: ℕ^d → ℝ *directionally convex* if Δ_aρ(u) := ρ(u+e_a) − ρ(u) is nondecreasing in every coordinate u_b
(b = a included). Then
    Σ_{y∈D} β(y)·ρ(y) ≤ |D|·ρ(0)        (≥ for directionally concave ρ; = for affine ρ).
Proof. Σ_y T(y)ρ(y) = Σ_aΣ_{x∈D} ρ(top_a x), so Σβρ = Σ_xρ(x) − Σ_aΣ_x(ρ(top_a x) − ρ(x)).
(1) With x^{(a)} = (x_1..x_a,0..0): ρ(x) − ρ(0) = Σ_a Σ_{i<x_a} Δ_aρ(x_1..x_{a−1},i,0..0)
    ≤ Σ_a Σ_{i<x_a} Δ_aρ(x_1..x_{a−1},i,x_{a+1}..x_d) = Σ_a (ρ(x) − ρ(x − x_a e_a))   (monotone in u_b, b>a).
(2) On an a-column with values ρ_0..ρ_{L−1} (convex in i): ρ_i + ρ_{L−1−i} ≤ ρ_0 + ρ_{L−1}, hence
    Σ_i(ρ_i − ρ_0) ≤ Σ_i(ρ_{L−1} − ρ_i). Summing: Σ_x(ρ(x) − ρ(0)) ≤ Σ_aΣ_x(ρ(top_a x) − ρ(x)). ∎
Instances: ρ = g(⟨y,q⟩), q ≥ 0, g convex. With g = (·−K)^+: Σ_{θ>K} β(H_θ) ≤ 0 where H_θ = {y∈D: ⟨y,q⟩ ≥ θ}.
Relation to Tile-CL: Tile-CL ⇔ Σ_y β(y)·k_σ(y) ∈ [σ−m+1, σ] with k_σ = ⌊(σ+⟨y,p̂⟩)/m⌋, a staircase that is
neither directionally convex nor concave; the lemma alone does not imply Tile-CL (see NOTEBOOK).

### Semigroup form of CL — PROVED equivalent 2026-10-17
With L = S ∩ [0,c), D the factorization tile, x(v) the D-cell of v mod m, δ(y) = ⌊(M − w(y))/m⌋ (left elements
in the class; Σδ = ell), κ(y) = ⌊w(y)/m⌋ (gaps in the class; Σκ = g):
    CL ⇔ W ≥ Σ_a Σ_{x∈D} δ(top_a x) ⇔ Σ_{y∈D} β(y)δ(y) ≥ c ⇔ Σ_{a=1}^{d} Σ_{v=c}^{c+n_a−1} x(v)_a ≥ g.
(Derivation: the left elements form the down-set 𝓛 = {(x,j): w(x)+jm < c} ⊆ D×ℕ; a good pair (s,a) is an
a-column of 𝓛 truncated by c rather than by D; counting truncated columns by their outer boundary cell
v ∈ [c, c+n_a) gives Σ_a Σ_v x(v)_a.)  Tile-CL at all s ⇔ the same with c replaced by any t ∈ ℤ.

### FALSE variants of CL (preserved)
- PDCL (per-direction: Σ_a min_s f_a(s) ≥ (d−1)m(m−1)/2): TRUE for d = 2 (m ≤ 12) but FALSE for d = 3,
  smallest D = {000,001,002,010,100,101}, p = (3,5,4), m = 6 (deficits 6+5+10 > 15).
- CL-inj (D a down-set with φ only injective, |D| < m): FALSE already for d = 1: D = {0,1,2}, p = 7, m = 10, σ = 3.

---------------------------------------------------------------------------------------------------
## FALSE strengthenings (preserved; see EXPERIMENTS.md)
- COV (H ⊆ union of e−1 sets f − L, f ∈ PF): FALSE whenever t > e−1 (each f ∈ PF is maximal, only
  f − L covers f). Smallest: ⟨7,9,10,15⟩.
- COV' (H ⊆ union of e−1 translates T − L, T ∈ ℤ arbitrary): FALSE; smallest found ⟨7,9,10,15⟩
  (e = 4, needs 4 translates, W = 2); 22 failures among t > e−1 cases with genus ≤ 16.
- S1 (Σ_a (C − Def_a)^+ ≤ C + E, C = m(m−1)/2): FALSE, ⟨7,11,12,20⟩ (W = 2).
- TOP_0 (Lemma A's predecessor without E): FALSE, e.g. ⟨9,13,14,15,16⟩.
- Downward / window payment schemes for the G-ID cells (2026-10-19), all FALSE in general (E222–E224):
  - OI: every order ideal L has Σ_L c ≥ 0. Fails from height 4.
  - Shift plus downward. Fails from height 6.
  - PREFIX: value-prefix sums ≥ 0. Fails from height 5.
  - Free choice of term order does not save them: for ⟨114, 305, 307, 310⟩ none of 200 weight orders admits OI or
    shift plus downward (W = 2161). The large-depth slack is not located below the deficient cells.
  - Still open: OI3 and SB3 at height ≤ 3.
- H_E (2026-10-19: every Eliahou semigroup, E < 0, has 3e ≥ m, which with Eliahou's 3e ≥ m theorem would give Wilf):
  FALSE. ⟨37, 47, 48⟩ ∪ [252, ∞) has m = 37, e = 12 (3 left, 9 right generators), E = −3, W = 492. The search was
  exhaustive over truncations ⟨m, a, b⟩ ∪ [C, ∞), m ≤ 40, a < b < 3m, C ≤ 8m: 1,001 Eliahou semigroups, 5 with
  3e < m, all of this one semigroup. Note the exact identity W = E + r(|L| − q), r = #right generators; Eliahou
  semigroups sampled so far have W/c ≥ 0.625.
- WQ (2026-10-19: for e ≥ 4, the unit cells plus the non-unit cells with residue in (μ, min(2μ, m−1)] pay every
  deficit of the G-ID cell decomposition). True on all 14.4M semigroups with e ≥ 4 of genus ≤ 30 (lex and grlex tiles).
  FALSE in general (E220). Cubic failure: ⟨15, 22, 24, 25⟩, μ = 13, five deficient crown cubics against window credit
  3. Higher degree: ⟨100, 125, 236, 287⟩ (μ = 1, degree 12, deficit 27 vs credit 9). Failures cluster at μ ≈ m − 1 or
  μ ≈ 1, where pairs with λ ≥ 1 below the deficient cells pay instead.

---------------------------------------------------------------------------------------------------
## Tile-CL / Base-CL special cases — PROVED 2026-10-17 (true theorems; reach only e = 3 resp. symmetric S)
Carry form of Base-CL (PROVED, basecheck.py 0 mismatches): base-slack(σ) = σ + Σ_{x∈D} G(x),
G(x) = #{a : ℓ_a(x) > r(x)} − C(x), ℓ_a(x) = ⟨x_a p_a⟩, r(x) = ⟨σ + φ(x)⟩, C(x) = ⌊(σ + Σ_a ℓ_a(x))/m⌋
(= #{a : C(base_a x) = C(x) − 1} − C(x)).  Base-CL: base-slack ∈ [0, m−1].
(B2) **Base-CL for d = 2, every tile.** With u = m − σ: G ∈ {−1,0,1}; G = 1 ⇔ ℓ_1,ℓ_2 < u ≤ ℓ_1+ℓ_2 (forces r ≤ u−2);
     G = −1 ⇔ ℓ_1,ℓ_2 ≥ u, ℓ_1+ℓ_2 < m+u (forces r ≥ u). r: D → ℤ/m is a bijection, so −σ ≤ ΣG ≤ u−1. ∎
(BR) **Box reflection (any d).** For a box D with far corner κ, x ↦ κ − x swaps tops and bases of every column:
     slack_Tile(s) = base-slack(s − φ(κ)). Hence Tile-CL ⇔ Base-CL on boxes; with (B2), Tile-CL holds for all rectangles.
(BH) **Base-CL (hence Tile-CL) for every box tile in every dimension** (uses Hajós's theorem — CITED: G. Hajós, Math. Z. 47
     (1941); group form: a factorization of a finite abelian group into cyclic subsets {0,g,…,(k−1)g} has a subgroup
     factor; e.g. Szabó–Sands, "Factoring Groups into Subsets", 2009, Ch. on Hajós; statement not re-read this session).
     Proof: ΣG = (d−1)Σ_D C − Σ_a k_aΣ_{x_a=0}C. Let factor 1 be the subgroup nℤ/mℤ, n = m/k_1. Then Hermite's identity
     Σ_{i<k}⌊(Z+in)/m⌋ = ⌊Z/n⌋ and reduction of the other coordinates mod n give
        ΣG(σ) = ΣG'(σ mod n) − n⌊σ/n⌋ + Σ_{x'}⌊⟨σ + Σ_{a≥2}ℓ_a(x')⟩_m / n⌋   (n terms, each in [0, k_1−1]),
     with G' the carry function of the box tile (k_2..k_d; p mod n) of ℤ/n. Induct on d (d = 1: G ≡ 0). ∎ (E50 checks it.)
     Scope: a box Apéry tile forces S symmetric (w ↦ w_κ − w preserves Ap).
(TC) **τ-class identity (any d).** τ(x) = (t_1(x),…,t_d(x)) with t_a(x) the a-coordinate of top_a x; X_τ = τ^{-1}(τ);
     slack(s) = Σ_τ [Σ_{x∈X_τ} Ĝ(x) + |X_τ|·⟨s − φ(τ)⟩/m], Ĝ(x) = #{a : ℓ'_a(x) > ρ_x} − ⌈(Σ_aℓ'_a(x) − ρ_x)/m⌉,
     ℓ'_a = ⟨(t_a − x_a)p_a⟩, ρ_x = ⟨s − φ(x)⟩ (tauclass.py, 0 mismatches). For d = 2 Tile-CL would follow from the
     class-discrepancy inequality CDL (CONJ, checked m ≤ 11), which is no longer pursued (CL is false; e = 3 is known Wilf).

---------------------------------------------------------------------------------------------------
## 2-D Tile-CL for EVERY 2-D tile — PROVED 2026-10-17 (night 11; corner-sum proof); **LEAN-CHECKED 2026-10-18**
## (lean/Wilf/TileCL2.lean: tileCLAt_of_two, tileCLAt_of_le_two, wilf_of_embDim_le_three; axioms propext,
## Classical.choice, Quot.sound; lake build OK, verified by the lead). Checked: all 2-D tiles m ≤ 22,
## every identity below asserted cell by cell (src/scratch/tilecl2d_proof.py).
Setting: D ⊂ ℕ² a down-set, |D| = m, φ(x) = x_1p_1 + x_2p_2 mod m bijective on D, Λ = ker φ (so ℤ² = ⊔_{λ∈Λ}(D+λ)).
For x ∈ D: t_1(x) = (τ_1, x_2) the end of its row, t_2(x) = (x_1, τ_2) the top of its column, τ(x) = (τ_1, τ_2) the
corner (τ(x) may lie outside D). r = r_s = ⟨φ − s⟩. X(s) := Σ_y T(y) r(y) = Σ_{x∈D} [r(t_1x) + r(t_2x)].
**Theorem.** For every s: 3M' − X(s) = m·Σ_{x∈D} ( [r(x) + r(τx) ≤ m−2] − ε(x) ) ≥ 0, where
ε(x) := (r(t_1x) + r(t_2x) − r(x) − r(τx))/m ∈ {−1,0,1}. In particular 2-D Tile-CL holds.

(L1) *Classification.* D has ≤ 2 outer corners: a rectangle [0,a)×[0,b) or an L-shape Ω = [0,a)×[0,b') ∪ [0,a')×[0,b)
  (0<a'<a, 0<b'<b, c := b−b', m = ab' + a'c), and then Λ = ⟨(a',b'), (a,−c)⟩ ∋ (a−a', −b).
  Proof. An inner corner q ∉ D with q−e_1, q−e_2 ∈ D lies in a unique D+λ; q−e_a ∉ D+λ (translates are disjoint and
  q−e_a ∈ D, λ ≠ 0), so q−λ ∈ D has no left/lower neighbour in D, i.e. q−λ = 0: q ∈ Λ. Two inner corners
  q_1 = (i_1,j_1), q_2 = (i_2,j_2), 1 ≤ i_1 < i_2, j_1 > j_2 ≥ 1 give q_2−q_1 = (i_2−i_1,0) − (0,j_1−j_2) ∈ D − D, a
  nonzero lattice vector with D ∩ (D+λ) ≠ ∅: impossible. For the L-shape, q = (a',b') ∈ Λ. The cell (a,0) ∉ D lies in
  D+λ with (a,0)−λ having no left neighbour in D, so λ = (a,−j), 0 ≤ j < b. If j < c then λ−(a',b') =
  (a−a',0) − (0,j+b') ∈ (D−D)∖0: impossible. If j > c then (a,b−j) (with 1 ≤ b−j < b') has left neighbour in D and lower
  neighbour (a,b−j−1) ∈ D+λ, and (a,b−j) ∉ D, D+λ (else (0,b) ∈ D); hence (a,b−j) ∈ Λ, so (0,b) ∈ Λ and
  (a',−c) = (a',b')−(0,b) ∈ Λ, but (a',−c) = (a',0)−(0,c) ∈ (D−D)∖0: impossible. So (a,−c) ∈ Λ; the index of
  ⟨(a',b'),(a,−c)⟩ is a'c + ab' = m = [ℤ²:Λ], so it is Λ. ∎
(L2) *Corner-sum bijection.* μ(x) := φ(x) + φ(τ(x)) is a bijection D → ℤ/m.
  Proof. Rectangle: τ ≡ (a−1,b−1), μ is a translate of φ. L-shape: the τ-classes are Q = [0,a')×[0,b') (τ = o :=
  (a−1,b−1)), R_1 = [a',a)×[0,b') (τ = (a−1,b'−1)), R_2 = [0,a')×[b',b) (τ = (a'−1,b−1)). μ(x) = φ(x+τ(x)) and, mod Λ,
  Q+o = o + [0,a')×[0,b');  R_1+(a−1,b'−1) − (a,−c) = o + [a'−a,0)×[0,b');  R_2+(a'−1,b−1) − (a'−a,b) = o + [0,a')×[−c,0).
  The union is o + ([a'−a,a')×[0,b') ∪ [0,a')×[−c,b')) = (o − (a−a',c)) + ((a−1,b−1) − D), a translate of −D, which is
  a fundamental domain of Λ = −Λ. ∎
(L3) *Proof of the Theorem.* t_1(x) + t_2(x) = x + τ(x) in ℤ², so the integer r(t_1)+r(t_2)−r(x)−r(τ) is ≡ 0 mod m and
  lies in [−2m+2, 2m−2]: ε ∈ {−1,0,1}, and ε = 1 forces r(x)+r(τ) = r(t_1)+r(t_2)−m ≤ m−2. Hence
  [r(x)+r(τx) ≤ m−2] − ε(x) ≥ 0 for every x. Summing the definition of ε: X = M' + Σ_x r(τx) + mΣ_x ε.
  Let u = r(x), v = r(τx), w(x) = ⟨u+v⟩ = ⟨μ(x) − 2s⟩; by (L2) w is a bijection D → [0,m). u+v = w + mω, ω ∈ {0,1},
  so Σω = (Σu + Σv − Σw)/m = Σ_x v/m; and w = m−1 ⇔ u+v = m−1. Thus [u+v ≤ m−2] = 1 − ω − [w = m−1] and
  Σ_x [u+v ≤ m−2] = m − 1 − Σ_x v/m. Therefore m·Σ_x([u+v ≤ m−2] − ε) = m(m−1) − Σ_x v − (X − M' − Σ_x v) = 3M' − X. ∎
Lean simplifications (found during formalization): (a) L3 base form is one line: ⟨s−φ(t_1x)⟩ + ⟨s−φ(t_2x)⟩ ≥
  ⟨2s − μ(x)⟩ (ZMod.val_add_le), and Σ_x ⟨2s − μ(x)⟩ = M' when μ is bijective. (b) L2 needs only (a,−c) ∈ Λ:
  Q–R_1 and Q–R_2 collisions are excluded by injectivity of φ on D alone; only R_1–R_2 uses (a,−c). (c) L1 case j > c:
  the side condition 1 ≤ b−j is unnecessary. Lean never formalizes translates or Λ: every step is injectivity or
  surjectivity of φ on D (coordinate form Tile2 P u v, Tile2.classify, shape_inj, cornerSum_injOn_of_two).
One-line form: r(t_1x)+r(t_2x) is an integer in [0,2m−2] that is ≡ μ(x)−2s, so X ≤ Σ_{w∈ℤ/m} max{y ≤ 2m−2 : y ≡ w} = 3M'.
Remarks. (i) Consequence via the Lean chain (Tile-CL ⇒ MaxCL ⇒ Tile-TOP'' ⇒ Wilf): Wilf for e ≤ 3, KNOWN (Fröberg–
  Gottlieb–Häggkvist 1987) — the value is the mechanism. (ii) It closes the 2-D input of the two-face reduction (R)
  above for L-shapes; that case still needs the bracket 2Σ_A r ≤ M' + dropped, which can fail (lshape_tc.py: min
  −0.025·4M'), so two-face L-shape tiles need the slack of this theorem, not just its sign. (iii) For d = 3 the same
  one-line bound with ν(x) = Σ_aφ(t_ax) gives only 5M' even if ν were bijective (target 4M'), μ(x) = φ(x)+φ(τx) is
  bijective on only ~1/3 of 3-D tiles (corner_bij.py), and pairwise 2-D sums E_a+E_b can exceed M' inside 3-D tiles
  (pairs3.py: max 1.055M' at m = 11) while the total stays ≤ M' — the 3-D mechanism must couple all three directions.

---------------------------------------------------------------------------------------------------
## Tile-TOP'' (lift-free, CONJ) — implication Tile-TOP'' ⇒ Wilf is LEAN-checked (lean/Wilf/TileTop.lean, 2026-10-17)
For a tile (D,p) (down-set, |D| = m, φ bijective), A = maximal cells (y + e_a ∉ D ∀a), π_s(y) = m − ⟨s − φ(y)⟩:
    (Tile-TOP'')  2·Σ_{y∈A} (d + |y|)·π_s(y) ≤ m((d+1)m + d − 1)   for every s ∈ ℤ/m.
Clean form (uses Σ_D π = m(m+1)/2): m + Σ_{y∈A}(|y| − 1)π(y) ≤ (d+1)·Σ_{z∈D∖A} π(z).
Proof of ⇒ Wilf: CH'; a non-maximal top t has M − w(t) ≥ n_b > m; a maximal top has M − w(t) ≥ ⟨s_M − φ(t)⟩ and tops
all d columns through it (total length d + |t|); total column length is dm per direction. ∎
LEAN: `TileTOPAt`, `TileTOP`, `wilf_of_tileTOPAt : TileTOPAt S.factDownSet S.genMod → c ≤ e·ℓ` (no S ≠ ℕ hypothesis),
`wilfConjecture_of_TileTOP : TileTOP → WilfConjecture`; axioms [propext, Classical.choice, Quot.sound], 0 sorry (verified
by the lead: lake build OK, PrintAxioms 124/124 standard).
Relations: Tile-CL ⇒ Tile-TOP'' ⇒ DR-CL ⇒ Wilf; Tile-TOP''(s_M) ⇒ TOP''. Wall form: Tile-TOP'' ⇔ Σ_yβ(y)W(y) ≤ π(0) − 1 +
(1/m)Σ_{y non-max}T(y)π(y), W(y) = ⌊(π(0) − 1 + ⟨y,p̂⟩)/m⌋ (Tile-CL is the same without the last term).
Status: CONJ; CHECKED all tiles d=2 m≤13, d=3 m≤10, d=4 m≤8, d=5 m≤7; 8008 adversarial Apéry tiles (E54, E55).
Proved special cases: boxes (all d; since d + |κ| = Σ k_a ≤ m + d − 1), d = 2 tiles for m ≥ 5 (crude bound).
FALSE strengthenings: R-TOP (rearranged), Box-TOP (|[0,y]| − 2 in place of |y| − 1), weight 2|y| − 2, semi-crude
(π(y) ↦ m on A; fails d=3 m=9: D = {000,001,002,010,011,020,100,101,200}, p = (1,3,4)).

---------------------------------------------------------------------------------------------------
## MaxCL (lift-free, CONJ, 2026-10-17) — MaxCL ⇒ Tile-TOP'' (PROVED, LEAN: tileTOPAt_of_maxCLAt) ⇒ Wilf (LEAN)
For a tile (D,p), A = maximal cells, N = D ∖ A, and every σ ∈ ℤ/m, with r = ⟨φ − σ⟩ (a bijection D → [0,m−1]):
    (MaxCL)  Σ_{y∈A} (|y| − 1)·r(y) ≤ (d+1)·Σ_{z∈N} r(z)   ⇔   Σ_{y∈A} (d + |y|)·r(y) ≤ (d+1)·m(m−1)/2.
Proof of MaxCL ⇒ Tile-TOP'': with r = π − 1 (r = ⟨φ − s − 1⟩), Tile-TOP'' ⇔ Σ_A T r ≤ (d+1)M' + Dep with
Dep = dm − Σ_A T(y) ≥ 0 (T(A) counts the cells of columns with maximal top, each direction ≤ m). ∎
Equivalence of the two forms: Σ_D r = M' and (d + |y|) = (|y| − 1) + (d+1). ∎
Wilf needs only σ = c mod m (r(x) = (w(x) − c) mod m).
Status: CONJ; CHECKED E58, E59 (all tiles d=2 m≤13, d=3 m≤10, d=4 m≤8, d=5 m≤7; 8008 adversarial tiles; 6800 random S, m ≤ 260).
Partial route (PROVED implication): Load Lemma (CONJ, E61) ⇒ MaxCL at σ = φ(0), via subadditivity r(u) + r(y−u) ≥ r(y)
when r(0) = 0. Open: general σ (bad-event bound m(B − P) ≤ (H + d + 1) r(0), unproved).

### Flat-MaxCL: MaxCL for tiles of height ≤ 2 — PROVED 2026-10-17; LEAN-checked (lean/Wilf/MaxCL.lean)
Statement. Let (D,p) be a tile with every cell of height |x| ≤ 2. Then MaxCL holds for every σ.
Notation: ρ_0 = r(0), ρ_a = r(e_a), ρ_ab = r(e_a+e_b); E = {ab : e_a+e_b ∈ D} (loops aa allowed);
deg(a) = #{b ≠ a : ab ∈ E} + 2[aa ∈ E] ≤ (d−1) + 2 = d+1. Cells: 0, the d unit vectors, the |E| height-2 cells, so
m = 1 + d + |E|. Every height-2 cell is maximal; e_a is maximal iff deg(a) = 0; 0 is non-maximal.
MaxCL reads Σ_{ab∈E} ρ_ab ≤ (d+1)(ρ_0 + Σ_{deg(a)≥1} ρ_a).
Proof. For ab ∈ E, ρ_a + ρ_b ≡ ρ_ab + ρ_0 (mod m) and both sides lie in [0, 2m−2], so ρ_a + ρ_b = ρ_ab + ρ_0 + mκ_ab
with κ_ab ∈ {−1,0,1}. Summing, Σ_E ρ_ab = Σ_a deg(a)ρ_a − |E|ρ_0 − mΣ_E κ_ab ≤ (d+1)Σ_{deg≥1}ρ_a − |E|ρ_0 + m·B,
B := #{ab : κ_ab = −1}. If κ_ab = −1 then ρ_ab = ρ_a + ρ_b + m − ρ_0 ≥ m − ρ_0, so the cells e_a+e_b with κ_ab = −1 have
pairwise distinct positions in [m − ρ_0, m − 1]; hence B ≤ ρ_0. Therefore Σ_E ρ_ab ≤ (d+1)Σ_{deg≥1}ρ_a + (m − |E|)ρ_0
= (d+1)Σ_{deg≥1}ρ_a + (d+1)ρ_0. ∎
Corollary (PROVED, via MaxCL ⇒ Tile-TOP'' ⇒ Wilf (LEAN)): Wilf holds for every numerical semigroup whose Apéry set
Ap(S,m) is contained in {0} ∪ P ∪ (P+P) (P = minimal generators other than m): every Apéry element has SOME factorization
of length ≤ 2, so the grlex factorization tile has height ≤ 2. This class contains reduction number ≤ 2 (max order of
Apéry elements ≤ 2), and is larger (an Apéry element may also lie in 3P). Checks: flat.py (400 S, all σ: proof inequalities deg ≤ d+1, B ≤ ρ_0 asserted).
Novelty: UNVERIFIED. Quick alphaXiv/web search found no such statement; but on 400 sampled height-2 S with q ≥ 4 Eliahou's
W_0 was always ≥ 0 and the class may be reachable by his method. 3 sampled height-2 S with 3e < m are outside every
condition implemented in src/known.py (e.g. ⟨33,69,70,71,74,80,81,82,85,87⟩, which misses Spirito #24 only by m).
Mechanism (the reusable part): **wrap events are confined to the top window [m − r(0), m−1]**, so they number ≤ r(0).
LEAN (2026-10-17, lean/Wilf/MaxCL.lean, 0 sorry, axioms propext/Classical.choice/Quot.sound; checked by lake build +
#print axioms by the lead): MaxCLAt (subtraction-free form Σ_A (d+|y|)⟨φ(y)−σ⟩ ≤ (d+1)Σ_D⟨φ−σ⟩);
tileTOPAt_of_maxCLAt; maxCLAt_of_height_le_two; wilf_of_factDownSet_height_le_two (lex tile);
wilf_of_apery_height_le_two: (∀ w ∈ Ap(S,m), ∃ x, wt x = w ∧ |x| ≤ 2) ⇒ c ≤ e·ℓ — the corollary exactly as stated above
(via a general IsFactTile reduction and the grlex factorization tile factDownSetG).

### Column-top lemma and the carry form of MaxCL — PROVED 2026-10-19 (paper; lemma LEAN-checked)
**Lemma (column-top).** For every finite down-set D ⊂ ℕ^d (no tile hypothesis) and every direction a,
    Φ_a(D) := Σ_{y∈A} (d + |y|)·y_a − (d+1)·Σ_{x∈D} x_a ≤ 0.
Equality holds iff every b-column top with t_a > 0 (b ≠ a), and every a-column top of length ≥ 2, is maximal.
Proof. d + |y| = Σ_b (y_b + 1). A maximal y tops its b-column, which has length y_b + 1.
- For b ≠ a, x_a is constant on b-columns, so Σ_{y∈A}(y_b + 1)y_a ≤ Σ_{b-tops}(len)·t_a = Σ_D x_a.
- For b = a, Σ_{a-tops}(y_a + 1)y_a = 2Σ_D x_a, by Gauss on each column.
- Summing gives at most (d − 1 + 2)Σ_D x_a. ∎
LEAN (2026-10-19, lean/Wilf/ColumnTop.lean, `column_top_lemma`, 0 sorry, axioms propext/Classical.choice/Quot.sound;
built with lake on fejer): Σ_{y ∈ D.filter (IsMaxCell D)} (d + Σ_b y b)·y a ≤ (d+1)·Σ_{x∈D} x a, for IsDownSetFin D.

**Carry form of MaxCL (exact, any height; checked on 1,844 (tile, σ) pairs, src/scratch/h3/maxcl_ident.py).**
Setup.
- r(x) = ⟨φ(x) − σ⟩, ρ_0 = r(0), δ_a = (r(e_a) − ρ_0) mod m ≥ 0.
- ℓ(x) = ρ_0 + x·δ, so r = ℓ − mK with K = ⌊ℓ/m⌋.
- Dep = dm − Σ_A (d+|y|) ≥ 0, and X_a = Σ_D x_a.
Then
    MaxCL(σ)  ⟺  −ρ_0(m + Dep) + Σ_a δ_a Φ_a ≤ m·Γ,    Γ := Σ_A (d+|y|) K(y) − (d+1) Σ_D K(x).
- K is monotone and nonnegative. Write U_j = {x ∈ D : ℓ(x) ≥ jm}; these are nested up-sets, and
  Γ = Σ_{j≥1} γ(U_j), where
    γ(U) = Σ_b (sh_b(U) − nm_b(U)) − |U|.
  - sh_b(U) counts the cells x ∉ U whose b-column meets U and has a maximal top.
  - nm_b(U) counts the cells of U whose b-column top is not maximal.
- Bijectivity gives Σ_D K = ρ_0 + Σ_a δ_a X_a/m − (m−1)/2.
Consequences.
- MaxCL holds at every height when no residue wraps (Γ = 0).
- The no-wrap equality cases are ρ_0 = 0 with every column topped by a maximal cell, i.e. simplex-like D. At height 3
  these are the postage-stamp (near-perfect B_3) bases: ⟨16,17,20,21⟩ has normalized MaxCL slack 0.0625, the
  minimum observed.
- So a MaxCL proof has only to pay the wrapped up-sets U_j.

**Column form for any lift, and phase-free NO-WRAP — PROVED 2026-10-19 (paper).** Checks: the identity was asserted at
every σ on 360 Apéry tiles (src/scratch/nowrap/wrap_identity.py); 6,000 no-wrap tiles gave 0 negatives
(src/scratch/nowrap/nowrap_maxcl.py).
Let f: D → ℤ be any function with f ≡ φ − σ (mod m), and K = (f − r)/m. For each direction b the b-columns C are the
maximal chains along e_b, with top t = t(C). Then, exactly,

    S(σ) = Σ_{b-cols, t ∉ A} |C|·r(t) + m·Σ_b Σ_{b-cols} Σ_{x∈C} (K(t) − K(x)) − (Φ(f) − M'),
    where Φ(f) := Σ_b Σ_{b-cols} Σ_{x∈C} (f(t) − f(x)).

Proof: Σ_b Σ_cols Σ_{x∈C} (r(t) − r(x)) = Σ_{all tops} |C|·r(t) − d·M'. The maximal tops give Σ_A (d+|y|) r(y). ∎
- For a linear lift f = ρ_0 + x·P with P ≡ p, Φ(f) = Σ_D x·P (Gauss on each column).
  - For the canonical lift P_a = ⟨p_a⟩ ∈ [1, m−1], Φ − M' = m·E with E := Σ_D ⌊x·P/m⌋ ≥ 0, because x·P mod m is the label.
  - If every P_b ≥ 0 then f is monotone on columns, so both column sums are ≥ 0.
  - Among linear lifts with P ≥ 0, the canonical lift minimizes Φ.
- The difference (column sums) − Φ(f) does not depend on f. The lift only decides which terms are visibly ≥ 0.
- Level form. Put U_j = {x·P ≥ jm} and U'_j = {ρ_0 + x·P ≥ jm}, so U_j ⊆ U'_j ⊆ U_{j−1}. Let B_b(U) be the set of cells
  outside U whose b-column meets U. Then

      S = Σ_{t ∉ A} |C|·r(t) + m·Σ_{j≥1} (Σ_b |B_b(U'_j)| − |U_j|).

- Semigroup lift P = n (the generators, f = ρ_0 + w). Then Φ − M' = m·g, where g is the genus. So MaxCL ⟺
  Σ_{t∉A} |C| r(t) + m·Σ_cols Σ_{x∈C} (K(t) − K(x)) ≥ m·g.

**Corollary (phase-free NO-WRAP).** Suppose the canonical lift satisfies x·P < m on D, i.e. v(x) = x·P is a bijection
D → [0, m). Then MaxCL holds at EVERY σ. Proof: E = 0 in the column form.

Second proof (elementary; the route to formalize). Write U = {x : v(x) ≥ m − ρ_0}, an up-set with |U| = ρ_0.
Then r = v + ρ_0 − m·1_U and Σ_D v = M'.
- (i) Gauss on columns gives (d+1)·Σ_D v = Σ_b Σ_{b-cols} |C|·v(t) exactly. Hence
  (d+1)Σ_D v − Σ_A (d+|y|) v(y) = Λ := Σ_{t ∉ A} |C| v(t).
- (ii) Each b-column meeting U has its top t in U, and |C ∩ U| ≤ |C|. Summing over b,
  d·|U| ≤ Σ_{y∈A∩U} (d+|y|) + Σ_{t∉A, t∈U} |C|.
- (iii) For t ∈ U, ρ_0 + v(t) ≥ m. So m·Σ_{t∉A, t∈U} |C| ≤ Σ_{t∉A} |C|(ρ_0 + v(t)) = Λ + ρ_0·Dep, where
  Dep = Σ_{t∉A} |C| = dm − Ω.
- Combining: Σ_A (d+|y|) r(y) = Σ_A (d+|y|) v + ρ_0Ω − m·Σ_{A∩U} (d+|y|)
  ≤ (d+1)M' − Λ + ρ_0Ω − m·d·ρ_0 + Λ + ρ_0·Dep = (d+1)M'. ∎
- Wilf corollary (paper). Suppose every Apéry element w_i has a factorization x with Σ_a x_a⟨n_a⟩_m = i exactly
  (no reduction mod m). Then W(S) ≥ 0. Reason: the least factorizations for the monomial order "weight x·⟨n⟩, then
  grlex" form a factorization tile, and by hypothesis it has no wrap. Then use wilf_of_tileTOPAt_of_isFactTile and
  tileTOPAt_of_maxCLAt.
  - Example: ⟨7, 8, 13⟩ is NOT in the class: w_5 = 26 = 2·13 is its only factorization, with residue sum 12.
  - Novelty vs the literature is UNVERIFIED (search 2026-10-19 night found nothing).
- **LEAN (2026-10-19 night, lean/Wilf/NoWrap.lean, 0 sorry; axioms propext, Classical.choice, Quot.sound; full
  `lake build` OK on fejer; written and checked by the lead):**
  - `maxCLAt_of_noWrap : IsTile D p → ∀ P : Fin d → ℕ, (∀ a, (P a : ZMod m) = p a) → (∀ x ∈ D, Σ_a x_a·P_a < m) →
    MaxCLAt D p`. Every phase, and ANY nonnegative lift, not only the canonical one.
  - `wilf_of_isFactTile_noWrap : IsFactTile S D → (∀ x ∈ D, Σ_a x_a·(n_a mod m) < m) → c ≤ e·ℓ`.
  - Formalized steps: Gauss (`sum_tileT_mul_linW`), Σ_D T = d·m, the up-set count (`card_filter_le_tops`), the window
    count (`card_window_le`, needing only injectivity of v), and a linear_combination certificate.
  - **Intrinsic form, also LEAN-checked:** `wilf_of_apery_noWrap : (∀ w ∈ Ap(S,m), ∃ x, wt x = w ∧
    Σ_a x_a·(n_a mod m) < m) → c ≤ e·ℓ`. In words: if every Apéry element has a factorization whose generator
    residues add up to exactly w mod m (no reduction), then Wilf holds.
    - It uses the weighted factorization tile `factDownSetW` (least factorizations for the monomial order
      "x·P, then grlex"; `isFactTile_factDownSetW`).
    - Same axioms, 0 sorry, full build OK.
- This strengthens "Γ = 0 ⇒ MaxCL" above, which needs ρ_0 + x·P < m and so depends on the phase.
- It covers:
  - postage-stamp tiles (grlex-min representations of 0..m−1 over a coin set containing 1);
  - mixed-radix products (DIGITAL-STAR);
  - columns, simplices and lex boxes;
  - spike lifts with spikes at labels ≥ the core size.

**LEAN (2026-10-19 late night, lean/Wilf/TileCLMax.lean, 0 sorry; axioms propext, Classical.choice, Quot.sound; full
`lake build` OK on fejer):** `maxCLAt_of_tileCLAt : IsTile D p → TileCLAt D p → MaxCLAt D p`, for any tile. Tile-CL is
exactly "S ≥ Λ_r" (PC). So H1′ (WRAP-MAX pure counting) is Tile-CL on WRAP-MAX tiles, and a Lean proof of it would give
MaxCL, then Tile-TOP'', then Wilf (via `wilf_of_tileTOPAt_of_isFactTile` and the weighted tile `factDownSetW`).
**UPDATE (2026-10-19, latest): H1′ is FALSE** (codex P7, independently re-checked by the lead; examples/
h1prime_sidon_counterexample.md, E269). Theorem SIDON-OBSTRUCTION: if a Sidon set A ⊂ [1, L] with |A| = k has
|3A∖A| > 2L + k(k+1)/2, then for every q ≥ 3L + 1 the tile (m = 2q; units q − a_i; all pairs; one cubic per s ∈ 3A∖A;
spikes on the missing labels) is a complete WRAP-MAX tile of height 3 with (S − Λ_r)/m = 2L + Q − |3A∖A| < 0 at
ρ = 2L. The explicit witness has k = 127 and slack −536. It is a factorization tile at its conductor phase, and MaxCL
and Wilf hold on it. PROVED pieces that survive:
- BOUNDARY: H1′, even in exit form, for θ ≤ min active unit weight (lead and codex, independently).
- The W-ID / SH-ID / LEVEL-ID / ONCE-ID identities (exact).
So Tile-CL ⇒ MaxCL (Lean, above) has no known infinite class of application beyond NO-WRAP and Flat. MaxCL on WRAP-MAX
tiles remains OPEN; in shadow form it is Λ_r/m + partial(U_θ) + Σ_{V_hi}|y| ≥ |V|, where the Λ_r term is necessary.

**FALSE extension (partial tiles), preserved.** MaxCL needs φ to be onto ℤ/m. A down-set with injective labels can
fail it. Example: D = {0, e_1, 2e_1} ⊂ ℕ¹ with p = 8 in ℤ/10 and σ = 7. Then r = (3, 1, 9), and
Σ_A (d+|y|) r = 27 > (d+1) Σ_D r = 26. So there is no induction by deleting cells.

**Unit form at height ≤ 3 (exact; checked on 1,158 (tile, σ) pairs, src/scratch/h3/unitform_h3.py).**
Notation.
- ℓ(x) = (1 − |x|)ρ_0 + Σ_a x_a ρ_a and K = ⌊ℓ/m⌋.
- For a non-maximal pair z, ψ(z) = Σ_{c : z+e_c ∈ D}(z_c + 1) ≤ d+2.
- deg(a) = Σ_{pairs z} z_a ≤ d+1.
Then
    RHS − LHS = Σ_{a non-max}(d+1−deg a)ρ_a + mρ_0 + Σ_{z∈N2}(d+2−ψ(z))ρ_z
                + m·[Σ_{A2}K + 2Σ_T K − Σ_{N2}(ψ(z)−1)K(z)].
Every residue coefficient is ≥ 0 (from 2Σ_T y_a = Σ_{N2} z_a ψ(z)). So height-3 MaxCL is exactly a carry inequality:
the bracket's negative terms must be paid by the nonnegative linear terms. The negative terms are:
- maximal pairs with ρ_a + ρ_b < ρ_0;
- cubics with Σ y_a ρ_a < 2ρ_0, which lie in the window [m − 2ρ_0, m);
- non-maximal pairs with ρ_a + ρ_b ≥ m + ρ_0, which cost ψ − 1 each.
Status: the reduction is PROVED; the carry inequality is OPEN.
FALSE strengthening, preserved: dropping L_+ and asking Br_0 ≥ −ρ_0 (H3-BR; all-height version G-BR,
Σ_{|y|≥2} Δ(y) ≥ −r(0)) is EQUIVALENT to Tile-CL (Abel/column form; PROPS "Tile-CL" forms Diff and Wall). It is FALSE on
the E47 tile ⟨14,22,23,57,61,62,63⟩ (height 3, d = 6): min ΣΔ + r(0) = −1. So any height-3 proof must spend L_+,
which is exactly the slack of MaxCL over Tile-CL coming from missing upper covers.

### Height-3 MaxCL: partial results (codex P6, 2026-10-19; src/scratch/gw/p6/P6_REPORT.md; reviewed by the lead)
Notation (tile of height ≤ 3): q pairs, of which p are non-maximal; t cubics; k non-maximal units; d−k spikes;
m = 1 + d + q + t.
- **PAIR-ZERO (PROVED, paper; lead re-derived).**
  - Hypothesis: K = 0 on N2 and K ≥ 0 on A2.
  - Conclusion: S ≥ L_+ + m(ρ_0 mod 2).
  - Key identity, CUBIC-LIFT: 2ℓ(y) + ρ_0 = Σ_a y_a ℓ(y − e_a). Hence negative cubics have K = −1 and residues in
    [m − ⌊ρ_0/2⌋, m).
- **CENTERED-PAIR (PROVED, paper; lead re-derived).** Write ℓ_1 = ℓ + (|x|−1)m and K1 = K + |x| − 1.
  - Then Br1 = Br0 + q + t and S = L_+ + m(d+1−ν) + m·Br1.
  - Conclusion: if ν ≤ d+1 and K1 = 0 on N2, then S ≥ L_+ + m(d+1−ν).
- **UNIT-LOAD-0 / PSI3 (PROVED, paper; lead re-derived).**
  - At ρ_0 = 0: MaxCL holds if 3·adeg(a) + 2·tc(a) ≤ 3(d+1) for every a.
  - In particular it holds if ψ ≤ 3 on N2.
  - It pays the E47 bracket exactly (S = 90).
- **MIN-PHASE (PROVED).** A slack-minimizing phase has its 0-residue cell in N and its (m−1)-residue cell in A.
- **FACE-EXTENSION / CONTAINER (PROVED).** Height-≤3 tiles = a pair face Q plus one eligible cubic per remaining
  residue. MaxCL for all extensions ⟺ COVER-PAY over feasible containers (MIN-COVER form).
- **H3-D5 (PROVED by finite certificate).**
  - Statement: MaxCL at every σ for every height-≤3 tile with ≤ 5 active directions (m ≤ C(d+3,3)).
  - Codex certificate: height3_certificate.c, two evaluation methods, plus an independent Python check for d ≤ 3.
  - **Lead independent re-check** (src/scratch/h3/h3_tiles_dfs.c: direct residue-by-residue DFS over actual tiles,
    no faces/containers/dominance, every σ):
    - d = 2, 3, 4 reproduce every count (sets 120 / 4,845 / 324,632; covered 40 / 549 / 9,601; height-3 faces
      36 / 854 / 34,457; flat faces 11 / 82 / 823);
    - d = 4: 58,722 height-3 tiles, 0 failures;
    - d = 5 also reproduces every count (32,468,436 / 229,082 / 2,443,823 / 13,820), with 7,605,820 height-3 tiles
      and 0 failures at every σ.
    So H3-D5 rests on two independent implementations (EXPERIMENTS E249).
  - **Corollary H3-E6:** Wilf for every S with e ≤ 6 whose Apéry elements all have a factorization of length ≤ 3.
    This includes e ≤ 6 with 4n_1 > c + m. Status: computer-assisted, not in Lean.
- **SPIKE-BOUND / H3-CORE2 (PROVED, paper plus a finite base for m ≤ 13).**
  - SPIKE-BOUND: (m−q−t)·C(1+k+p,2) ≥ (q−p+2t)(m−1) ⇒ MaxCL.
  - H3-CORE2: MaxCL at every σ when k ≤ 2, with arbitrarily many spikes.
- **H3-CORE3 (lead, 2026-10-19; PROVED, computer-assisted).** MaxCL holds at every σ for every height-≤3 tile with
  exactly 3 non-maximal unit directions and any number of spikes. Proof:
  1. Delete the spikes; the core C ⊂ ℕ³ (all units non-maximal) is one of 2,291 down-set shapes, all enumerated.
  2. Height-≤2 cores are Flat-MaxCL (LEAN). If d = 3 + s ≤ 5, use H3-D5.
  3. Otherwise, if CR holds for (C, s), MaxCL holds at every σ. CR is linear in s, with slope (2t+q−p) on the left
     and n(n+1)/2 on the right. For k = 3 no height-3 shape has a non-positive slope difference with CR failing, so
     CR fails exactly for s < s*(C).
  4. That leaves 11 (C, s) with s ≥ 3. Nine have injective labelings: 672 labelings, all checked at every σ by the
     spike form (k+s+1)Σ_N r − Σ_A(|y|−1)r: 10,200 checks, min slack 39, 0 failures. The other two have none.
  Script: src/scratch/h3/lcr3_exh.py 3 full. With H3-CORE2, height-3 MaxCL holds whenever k ≤ 3.
- **H3-CORE4 (lead, 2026-10-19; PROVED, computer-assisted).** The same for exactly 4 non-maximal units.
  - 2,134,621 height-3 core shapes in ℕ⁴; none fails CR for every s.
  - CR fails for s ≥ 2 on 11,712 (C, s), forming 710 S₄-orbit cases with m ≤ 42; 31 are realizable.
  - All 20,752 injective labelings of those, at every σ (524,072 checks): min slack 49, 0 failures.
  - Scripts: lcr_export.py 4 | lcr_check 4 (C). E252.
  - Every realizable CR failure is NEAR-FLAT: q = 8–10 of the 10 pairs, p = 1–3, t = 1–4.
  So **height-3 MaxCL holds whenever k ≤ 4 (any d) or d ≤ 5**.
- **Codex P6b (2026-10-19; src/scratch/gw/p6/P6B_REPORT.md; reviewed by the lead, E256).** Notation: Q_k = C(k+1,2),
  U_k = C(k+2,3), ε = U_k − t (missing cubics), j = Q_k − p, a = q − p, J = C(1+k+p,2), B = a + 2t.
  - **CR in m-linear form (PROVED):** S ≥ R(m) = (m−q−t)J − B(m−1) + t(t−1) + at + C(a,2), slope J − B > 0.
  - **PAIR-PACK (PROVED; lead re-derived):** all pairs on h directions present ⇒ m ≥ h² + h + 1 (off-diagonal
    differences are distinct). FALSE without the complete face (k = 2, m = 6, P = (1,4), C = {0,x,y,x²,xy,x³}).
  - **ROW-PACK (PROVED; lead re-derived):** m ≥ h²+h+1 + h·f_0 + (h−1)·f_1, where f_0, f_1 count successor-complete
    loops / ordinary pairs (z + e_i present for every i). Labels φ(z) − c, c ∈ {0} ∪ units, c ∉ supp z; a collision
    gives an equality of two PRESENT cells. **ROW-DEF:** m ≥ H(h+1) − 3(h−1)ε_I, H(h+1) = (h³+2h²+3h+2)/2.
    **RETAINED-PACK:** both apply to any sub-face I with all pairs present, for the original m.
  - **SHADOW-DEF (PROVED):** k·j ≤ 3ε and k·j − C(j,2) ≤ ε. **SHADOW-COVER (PROVED, algebraic; lead re-derived):** for
    any family E of quadratic monomials, |upper cubic shadow| ≥ k·τ(E) (τ = vertex-cover number with loops), via τ
    generic quadrics forming a regular sequence and the absence of linear Koszul syzygies. Sharp (τ loops).
  - **DENSE9 (PROVED analytically):** all pairs present and ε ≤ ⌊k²/9⌋ ⇒ MaxCL at every σ, any spikes.
  - **DENSE075 (PROVED analytically):** ε ≤ ⌊3k²/40⌋ ⇒ MaxCL at every σ (no face hypothesis). Shifted-polynomial
    certificates; the lead re-derived all four from the definitions (src/scratch/h3/p6b_poly_check.py).
  - **FLAT-CR (PROVED; lead re-derived):** S ≥ s·C(k,2) + (k+s+2)·C(p,2) − 3t(m−1) + t(t−1), from the identity
    S = U − tρ_0 + (d+2)Σ_{N2} r − 2Σ_T r + m(ρ_0 − b_− + b_+) (flat identity on all pairs; b_− ≤ ρ_0 by the window).
  - **FEW-CUBICS (PROVED):** all pairs present, k ≥ 19, t ≤ ⌊k²/16⌋ ⇒ MaxCL. **ONE-CUBIC** (all pairs, t = 1, any k)
    and **THREE-CUBICS** (all pairs, t ≤ 3, any k): analytic for large k plus finite bases (k = 4: m = 21–27;
    k = 5: m = 31, 32; k = 6: m = 43–45, no full-pair bases). The lead re-ran every base with lcr_check2 and an
    independent modular-B₂ counter: identical counts (one-cubic k = 4: 18,168 labelings, 475,080 phases, min 148;
    two-cubic: min 147 (k = 4), 420 (k = 5); none at k = 6).
  - Preserved: F3, the smallest CR- and FLAT-CR-unpaid core with k ≥ 4, d ≥ 6: k = 4, m = 16, P = (1,4,6,9), all
    pairs except x₂x₃ and x₄², T = {x₁³} (CR = −2, FLAT-CR = −33, true min S = 78). F4: R(21) = −5 for k = 4,
    t = p = 2 (an intermediate table claim; the base is now explicit).
- **Codex P6c (2026-10-19; src/scratch/gw/p6/P6C_REPORT.md; every proof below re-derived by the lead, E258).**
  Notation: δ_i = k+1−deg_Q(i) (so Σδ_i = 2e, e = Q_k − q), L_+ = Σ_i(s+δ_i)ρ_i + Σ_{N2}(d+2−ψ)r ≥ 0, W = [m−ρ_0, m).
  - **WINDOW-ID (PROVED, exact).** With κ_y = 2K(y) − Σ_i y_iK(y−e_i) (CUBIC-LIFT gives mκ_y = Σ y_i r(y−e_i) −
    2r(y) − ρ_0, so κ_y ≥ −2, and κ_y ≥ −1 outside W), b_y = κ_y + [r(y) ∈ W] ≥ −1, β = #{b_y = −1}:
    HC′ = L_+ + m(O_rest + P_+ + gain − β), O_rest ≥ 0. Hence **WINDOW-LOSS: HC′ ≥ L_+ − mβ ≥ L_+ − mt** at every
    phase, with no face or dimension hypothesis. A bad cubic costs at most one m.
  - **CONE-PHASE (PROVED).** If every cubic contains x_i, then at the zero phase of x_i, O_W + B ≥ 0 and HC′ ≥ L_+.
  - **One cubic (t = 1), all PROVED:** ONE-PAIR-PHASE (an N2 pair at residue 0 ⇒ HC′ ≥ L_+); ONE-DEFICIT
    (O_W + B < 0 only if K(y) = −1, r(y) ∈ W, all N2 carries 0, O_W = 1, and then m ≥ 17; sharp family preserved);
    **ONE-COVERED-ALL: MaxCL for every one-cubic tile whose missing-pair graph covers every core unit**, any k, any
    spikes; ONE-PARTIAL-COVER (≤ 1 complete quadratic row when k ≥ 12); ONE-LARGE-DEFECT (k ≥ 36, e² ≥ k³).
    With ONE-CUBIC (complete face), the one-cubic frontier is: incomplete face with a complete row, minimizing zero at
    a unit outside the cubic, ρ_0 ≥ 8, 2ρ_0 < m; s ≤ 3 when k ≥ 15.
  - **DEFECT-FLAT (PROVED):** FLAT-CR with the unit term improved by F_G = Σ_j j·δ_(j) ≥ 2e²/(k+1) − e.
  - **CUBIC-DEGREE (PROVED; t and k unbounded):** 2 ≤ t ≤ k/2 and δ_i ≥ t for every core unit ⇒ HC′ ≥ 0 ⇒ MaxCL.
  - **UPPER-ARC / UPPER-PAY (PROVED, phase-specific):** with G = {i : 2ρ_i ≥ m + ρ_0}, S ≥ L_+ + m(2g − d − 1 + η −
    cost), cost = a_1 + 2a_0 + 4t_2 + 6t_1 + 8t_0.
  - **DIGITAL-STAR (PROVED, every height):** mixed-radix products of stars satisfy MaxCL at every phase and every spike
    lift (PREFIX coupling + column-top lemma). They have s = 0, unbounded k, t/U_k → 2/9 and CR < 0 for r ≥ 11. So
    **a face-free packing bound m − |C| ≥ c·t²/k⁴ is FALSE**, and CR + packing cannot close the middle. Smallest zero-spike
    core with k ≥ 5, d ≥ 6: k = d = 6, m = 12, P = (3,1,4,7,2,8), Q = {00,12,23,45}, T = {000} (min S = 173).
  - **RECTANGLE-PACK (PROVED, every height, no face hypothesis):** for any set J of h directions and
    F_J = {z : z + e_i ∈ D ∀ i ∈ J}, the labels φ(z) and φ(z) − φ(e_c) (c ∈ J ∖ supp z) are distinct, so
    m ≥ Σ_{z∈F_J}(h + 1 − |supp z ∩ J|). Full-face B_H: m ≥ C(h+H−1,H−1) + h·C(h+H−2,H−1). Also CR_H, and the
    all-height identity FLAT-WINDOW-H: S = HC′_H + m·#{maximal pairs with K = +1}.
  - Preserved false: O_W + B ≥ 0 for one cubic (sharp family, smallest m = 17, k = 6, s = 1, σ = 9,
    P = (9,10,12,13,14,15), Q = {00,01,11,02,03,04,05,44}, T = {444}: L_+ = 133, S = HC′ = 116).
- **Remaining family:** k ≥ 5, d ≥ 6, R(m) < 0 and FLAT-CR < 0 (and DEFECT-FLAT < 0), ε > ⌊3k²/40⌋, outside
  CUBIC-DEGREE, ONE-COVERED-ALL, THREE-CUBICS and the dense/few-cubic classes. Every retained complete face must satisfy
  ROW-DEF below the CR threshold. Exact reduction: by WINDOW-ID, HC′ ≥ 0 ⟸ mβ ≤ L_+ + m(O_rest + P_+ + gain), i.e. the
  β "bad cubics" must be charged injectively. Next lemma (codex): ONE-RELAY (t = 1: at a zero unit outside the cubic,
  if O_W + B = −1 then L_+ + mP_A^+ ≥ m), then the injective relay charging of β in general.
- **Codex P6d (2026-10-19; src/scratch/gw/p6/P6D_REPORT.md, code in p6/d/; reviewed by the lead, E261).**
  - **ONE-CUBIC (PROVED).** HC′ ≥ 0, hence MaxCL, at EVERY phase for EVERY height-3 tile with exactly one cubic,
    in any dimension and with any number of spikes. Proof: ONE-RELAY (L_+ ≥ m at every ONE-DEFICIT phase). At
    other phases O_W + B ≥ 0. Ingredients:
    - DIFF-CENSUS (cyclic; valid at composite m): E_D ≤ Σ_F [4C(g_F,2) − 2ℓ_F(g_F−1) + C(ℓ_F,2)] and
      m − 1 ≥ n(n−1) − E_D. Consequence COARSE-PACK: m ≥ n(n−1) + 1 − 2e(e+1).
    - WEIGHTED-PACK (unwrapped fibres): WP gives A ≥ n(n−1) − m + 1 − e; WP2 (2 ∉ V) gives A ≥ n(n−1) − m + 1.
    - ONE-UNWRAP (P_A^+ = 0, A < m) and ONE-WEIGHTED. ONE-WEIGHTED pays the wrapped fibres by the two
      unavailable integer pairs {ρ, w−ρ} and {r, w−r}, where r is the least N2 residue and HOLES gives ρ ≥ 3r + 2.
    - Bounds (4)–(7): L_+ − m ≥ A + (s−1)Q_k + e + k − s − 4 for s ≥ 1. For s = 0 the bound is split by cube type,
      with the pure-cube, r = 2 case settled by WP2.
    - Small cases k = 3, 4, 5 are analytic. The last one, k = 5, e = 2, m = 20, ρ = 8, is excluded by collision
      counting.
    - The lead re-derived every step against the accepted ONE-DEFICIT classification (P6c).
    - Semigroup corollary: Wilf holds whenever some factorization tile has height ≤ 3 and at most one cubic.
  - **BAD-NARROW (PROVED).** At ρ = 0, if every core unit label lies in (m/2, 2m/3), then
    P_+ + gain + L_+/m ≥ β and HC′ ≥ 0. Proof: β = t; residues in (2b−m, a) are spikes, so s > m/6 − 1;
    k + t ≤ ⌊(m−1)/2⌋. The cases k ≥ 6 and k ≤ 5 are explicit (lead re-checked the k = 3, 4, 5 table: 1/5, 8/5, 5).
  - **Further PROVED payments.**
    - Origin bad-cubic classification: at ρ = 0, bad ⟺ carry 1 with three positive face carries. At least two
      factor copies exceed m/2; not all three need to (m = 8 example).
    - DEGREE-MOMENT and the Mcover bounds on A. GENERAL-SHAPE: HC′ ≥ M_shape + m(O_rest + P_+ + gain − β).
    - ONE-BAD-SHAPE (β ≤ 1 and Ξ ≥ 0 ⇒ MaxCL, any t) and ONE-BAD-LOWPAIR.
  - **WINDOW-H (PROVED, every height).** Lift (j−1)ℓ(y) + ρ = Σ y_i ℓ(y−e_i). The identity is
    HC_H = L_H + m[O_H + P_+ + Σ_{j≥3} Σ_{C_j} b_y], with b_y = κ_y + [r(y) ∈ W] ≥ −(j−2) and O_H ≥ 0.
    - Independently re-implemented by the lead from the report's definitions only
      (src/scratch/h3/p6d_review/windowH_check.py): exact at every phase on 744 Apéry tiles of heights 2–19.
    - The quartic lift is 3ℓ + ρ, not 3ℓ + 2ρ (the lead's earlier statement was wrong). A local quartic loss of 2m
      occurs (m = 7, P = 5, column, σ = 0).
  - **Preserved failed candidate.** ONE-DEFICIT does not need a spike: m = 17, ρ = 8, U = (0,1,3,5,7),
    Q = {00,01,02,03,11,12,13,33,34,44}, T = {333}, s = 0, S = HC′ = 30.
- **Remaining family after P6d.** k ≥ 5, d ≥ 6 and t ≥ 2, failing all old and new payment criteria. A violating phase
  needs β > O_rest + P_+ + gain + ⌊M_shape/m⌋; for β = 1 it also needs Ξ < 0. Next lemma (open), HIGH-ORIGIN:
  at ρ = 0 with every core unit > m/2, L_+/m + p + t ≥ 2β. BAD-NARROW is its case with all units below 2m/3.
- **Codex P6e (2026-10-19; src/scratch/gw/p6/P6E_REPORT.md, code in p6/e/; PARTIALLY reviewed by the lead).**
  Review status:
  - BAD-TWO: re-derived in full by the lead (all five K-cases).
  - DEFECT-CUBIC, LINKED-CUBIC, GENERAL-FEW80/72/40 and H-FEW40: logic re-derived by the lead. Every polynomial
    identity is checked symbolically (src/scratch/gw/p6/e_review/few40_check.py: LC, R increasing, FP40 and its
    k = 40t + 7 endpoint, FP72, the C − 2kt − 2t² − 2t margins). H-FEW40 additionally uses L_H ≥ A + s·C(k,2) at
    height H (unit and missing-pair terms of WINDOW-H), as asserted in the report.
  - HALF-ID, ORIGIN-ONE-LOW, SMALL-LOW-BAND and ZERO-EXTENSION: codex-proved, NOT yet re-derived by the lead.
  - **BAD-TWO (PROVED, lead-checked).** At any phase a cubic is bad (b_y = −1) iff it has one of two types:
    - A: K = +1, outside the window, all three face carries +1, all factor residues > ρ;
    - D: K = −1, inside the window, all face carries 0, all factor residues < ρ.
    Corollaries: BAD-ARCS (β_A ≤ ⌊ν/2⌋, β_D ≤ ⌊ρ/2⌋) and DEEP-HOLES (ρ ≥ 3r + 2 for a deep cubic's least face residue r).
  - **ORIGIN-EDGE (codex).** MaxCL at ρ = 0 for every t when at most one core unit is ≤ m/2. HC′ at ρ = 0 when at most
    one core unit is > m/2 (ORIGIN-ONE-HIGH). HC′ when β ≤ 5 at the origin (ORIGIN-THREE, HIGH-FIVE). HIGH-FEW: HC′
    when k ≥ 2t at an all-high origin.
  - **GENERAL-FEW40 (codex).** HC′ at every phase for every height-3 tile with t ≥ 2 and k ≥ 40t + 8. It uses
    LINKED-CUBIC, a height-independent bound A ≥ (4v⁴ − 16v² − 12v − 1)/(8(5v+4)) on the missing-pair mass.
    - **H-FEW40 (codex, every height):** HC_H at every phase when k ≥ 40B + 8, where B = Σ_{j≥3}(j−2)|C_j| ≥ 2.
  - Zero-unit relays: ZERO-EXTENSION and the weighted criterion (ZW).
  - Preserved false claims F1–F6. F1 is β ≤ P_+ at the origin (m = 14, U = (8,9), the binary quartet; S = 90).
  - Residual height-3 family: k ≥ 5, d ≥ 6, t ≥ 2, k < 40t + 8, failing all criteria. At the origin it has at least
    two high and two low core units and β ≥ 4. Codex's next lemma: ABSENT-ZERO (Λ_F + m·O_rest ≥ Σ_F (m − r(z))).
- **Codex P8 (2026-10-19; src/scratch/gw/p8/P8_REPORT.md, code in p8/; REVIEWED by the lead, see status per item).**
  Setting as in P6e: a height-3 core with k non-maximal units, q pairs (p covered), t cubics, s spikes; m = M0 − e + t + s
  with M0 = C(k+2,2) and e missing pairs on v defective directions. The accepted window bound is HC′ ≥ L − mβ ≥ L − mt.
  - **SYMMETRIC-RECTANGLE (SR; PROVED, lead re-derived).** If the origin, k units and a quadratic down-set have injective
    labels mod m (no completeness needed), then m ≥ k(k+1) + 1 − v(v−1) − 4e.
    - Proof: G = the zero label plus the h = k − v + 1 good units, V = the zero label plus all units, D₁ = {g − b : g ∈ G,
      b ∈ V, g ≠ b}. Then |D₁| = hk, |D₁ ∩ −D₁| ≤ h(h−1) + 4e, and 0 ∉ D₁ ∪ −D₁.
    - Height-independent. For v = e = 0 it is the Sidon-set bound m ≥ k(k+1) + 1.
    - **LEAN (kernel-checked 2026-10-19, lean/Wilf/SymRect.lean `symmetric_rectangle`; standard axioms only).**
      Abstract form over ZMod m: G ⊆ V, Mo a set of ordered missing pairs with both entries outside G; non-missing
      pairs have distinct sums. Conclusion: 2·#G·(#V − 1) + 1 ≤ m + #G(#G − 1) + 2·#Mo. With #Mo ≤ 2e and #G = k − v + 1
      this is (SR). No swap-closure, completeness or 0 ∈ G hypothesis is needed.
  - **RETAINED-MOMENT (lead re-derived).** A = Σ δ_i u_i ≥ F(v, e) = [C(q_D,2) + (v+1)(X²/(2v) − X/2)]/v, where
    q_D = v(v+1)/2 − e and X = 2e − v. Ingredients: the rank bound on the weights δ_i − 1 ≤ v, and distinct integer pair
    sums on the defective directions.
  - **SHADOW-RANK (lead re-derived).** Σ_{N2}(d+2−ψ)r ≥ (d+1)C(p,2) − w(p−1), with w = 3t − p, because Σ_{N2} ψ = 3t.
  - **NEGATIVE-CAPS (lead re-derived).** At a negative phase, with k ≥ 150 and t < k/4: s < k/2,
    m < k²/2 + 9k/4 + 1 − e, v ≥ k/2 − 5/4 + e/k, and (v+2)² + 3e ≥ k²/2.
  - **GENERAL-FEW21+240 (PROVED; lead re-derived both cases; (NL) checked independently).** HC′ ≥ 0 (hence MaxCL) at
    every phase for height-3 tiles with t ≥ 2 and k ≥ 21t + 240.
    - Together with FEW40, the threshold is k ≥ min(40t+8, 21t+240).
    - **H-FEW21+240**, every height: k ≥ 21B + 240 with B = Σ_{j≥3}(j−2)|C_j| ≥ 2.
  - **SHADOW-DENSE / SHADOW-225 (PROVED; finite part independently re-implemented by the lead).** HC′ ≥ 0 at every phase
    when t ≥ 2, p ≥ 9t/4 and k ≥ 255. Also p ≥ 11t/5 with k ≥ 6500, and p ≥ 13t/6 with k ≥ 162500.
  - **DISJOINT-CUBICS (PROVED; certificate re-run by the lead).** HC′ ≥ 0 at every phase, in every dimension, when the
    cubics are squarefree and pairwise share no quadratic divisor (p = 3t), t ≥ 2.
    Corollary: Wilf for every S with a height-≤3 factorization tile of this kind.
  - Lead checks (E274):
    - (NL) dense grid: minimum +1.36·10⁻⁴ near x = 0.584 on x² + 3y = 1/2.
    - SHADOW-225 finite part, re-implemented (src/scratch/gw/p8lead/p8_lead_check.py; F from its definition, exact
      quadratic fits): minimum G = 3278015777/25852500 at (k, v, e) = (255, 150, 3282), as reported.
    - symmetric.py, review.py, small_disjoint.py re-run: identical (585,036 domains, minimum 15355/507).
  - **FALSE, preserved:** L ≥ mt for arbitrary height-3 cores (m = 20, P = (12,3,5,9,19), σ = 18: L = 79 < 80, S = 99);
    the pair bound without the w(p−1) term (m = 6); f ≥ z/20 on (D) (x = 29/50, y = 409/7500).
  - Residual height-3 family: k ≥ 5, t ≥ 2, k < min(40t+8, 21t+240), p < 3t; p < 9t/4 above k = 255. Codex's next lemma:
    MAXMATCH-RESIDUAL, Λ_F + m·O_rest ≥ Σ_F (m − r(z)) + m(β_D − ν).
- **FALSE, preserved:** L-CR3 ("CR for every injective height-3 core with k + s ≥ 6"). Exhaustive k = 3: 9 realizable
  failures, e.g. all six pairs plus x³, m = 14, d = 6, p = (1,4,6). Maximal pairs defeat CR, so a CR proof needs the
  flat window for A2.
- Codex's other preserved failures:
  - the [−1,1] cubic carry range (it is [−2,2]);
  - "some origin lift removes all carries";
  - "the forced-pair intersection suffices" (m = 6, p = (1,5)).

### Two-face tiles: 2-D picture, reduction to 2-D Tile-CL, and the box theorem — PROVED 2026-10-17 (paper; finite part
### by exact computation, src/scratch/twoface_box.py; identities asserted in scratchpad box_ident.py, b ≤ a ≤ 10)
Setting: (D,p) a d = 3 tile with x_1x_2 = 0 on D ("two-face") and p_3 ≡ p_1 + p_2 (i.e. e_1 + e_2 ≡ e_3 mod Λ).
(P) **2-D picture.** ψ(i,j,k) = (i+k, j+k) is injective on {x_1x_2 = 0} (inverse k = min(s,v)), φ = φ'∘ψ with
    φ'(s,v) = s p_1 + v p_2, and |y| = max(s,v). Hence Ω' = ψ(D) is a fundamental domain of a lattice in ℤ² with linear
    positions. If Ω' is a 2-D down-set then D = ψ^{-1}(Ω') is a 3-D down-set, and y ∈ D is maximal iff ψ(y) = (s,v) is
    a row end with s > v, a column top with s < v, or both with s = v. Then T(y) = 3 + max(s,v) = λ(y) + 2, where λ(y)
    is the length of the row (resp. column) of Ω' that ends at ψ(y).
(R) **Reduction.** With X(σ) = Σ_{rows R of Ω'} |R|·r(end R) + Σ_{columns C} |C|·r(top C) (2-D Tile-CL says X ≤ 3M'):
        Σ_{y∈A} T(y) r(y) = X(σ) + 2Σ_{y∈A} r(y) − (row/column terms of non-maximal ends, ≥ 0).
    So MaxCL(D,σ) ⇐ [2-D Tile-CL for Ω' at σ] + [2Σ_A r ≤ M' + dropped terms].  Proof: assign each maximal y to the
    run it ends; distinct y get distinct runs; use T = λ + 2. ∎
(B) **Theorem (two-face box tiles).** If Ω' = [0,a)×[0,b) then MaxCL holds for every σ.
    Proof. WLOG a ≥ b (swap faces). Maximal cells: R = {(a−1,v) : v < b} (T = a+2) and C = {(s,b−1) : s < b−1}
    (T = b+2); exactly LHS = X + 2Σ_A r − bΣ_{s ≥ b−1} r(s,b−1) (a > b), resp. − a·r(a−1,a−1) (a = b).
    2-D Tile-CL holds for every rectangle tile ((B2) + (BR) above), so it suffices that 2Σ_A r ≤ M'.
    Hajós (CITED, as in (BH)) for ℤ/m = {s p_1} ⊕ {v p_2}: b p_2 ≡ 0 (type i: columns are cosets of the subgroup of order
    b) or a p_1 ≡ 0 (type ii: rows are cosets). Coset bound: the n elements of a coset of the subgroup of order n have
    Σ⟨x − σ⟩ = nρ + m(n−1)/2 ≤ n(m/n − 1) + m(n−1)/2; any k distinct residues have Σ ≤ k(m−1).
    Type i: 2Σ_A r ≤ 2b(a−1) + m(b−1) + 2(b−1)(m−1) < m(3b−1) ≤ M' when a ≥ 6.
    Type ii: 2Σ_A r ≤ 2(2b−1)(m−1) ≤ M' when a ≥ 8 (and a = b ≥ 6 by symmetry with type i).
    Remaining a ≤ 7 (b ≤ a): exact check of all (p_1,p_2) and σ (twoface_box.py: 0 failures; min slack 0 only at
    a = b = 2, the simplex m = 4). ∎
    Scope: e.g. ⟨36,37,42,43⟩ (a = b = 6). It is the first MaxCL family of unbounded height beyond boxes, and it lies in
    the class where the crude bound CR fails. The L-shape case: 2-D Tile-CL for L-shapes is now PROVED (section "2-D Tile-CL for EVERY 2-D tile"); the
    bracket part remains (it can be negative, so the proof must use the exact 2-D slack).

## Dependency graph
CH ⇒ Corollary H.  CH ⇒ Lemma A.  Lemma A + TOP'' ⇒ Wilf.  CH' + CL ⇒ Wilf (CL FALSE).  Tile-CL ⇒ CL ⇒ TOP''
(numerical; Tile-CL and CL FALSE, TOP'' survives E49).  MAIN ROUTE NOW: MaxCL ⇒ Tile-TOP'' ⇒ Wilf (LEAN) — prove MaxCL (Load Lemma + general σ). Also Lemma A + TOP'' ⇒ Wilf (LEAN).
SECONDARY: CL restricted to 3e < m, c > 3m, + LITERATURE #13, #21.
LEAN (kernel-checked, lean/Wilf/Chains.lean, axioms propext/choice/Quot.sound only, 0 sorry): CH, Corollary H,
Lemma A, TOP'' ⇒ Wilf (wilf_of_TOP2). lean/Wilf/Carry.lean (same axioms, 0 sorry): CH' (columnIdentity),
CL ⇒ Wilf (wilf_of_CL); Tile-CL stated as a Prop (TileCL), not proved.

## e = 4, asymptotic HT via the counting criterion CHT (2026-10-18, night 14 late) — pieces PROVED on paper

Notation. D ⊂ ℕ³ finite down-set, m = |D|. top_a(x) = end of the ray x + ℕe_a in D; ht(y) = max{|z| − |y| : z ∈ D, z ≥ y};
h(x) = Σ_a ht(top_a x); H(D) = Σ_x h(x); δ(D) = H − (m − 1). Max = maximal elements, t = |Max|; n(x) = #{a : top_a x ∈ Max};
Tri = {x ∉ Max : n(x) = 3}; Q' = {x : n(x) = 2, h(x) = 1}, split as qU (the non-maximal top is x itself) and qO (it is not).
Class 𝒞 (Loomis–Whitney sets): D = {x : x₂ < h(x₁), x₃ < min(F(x₁), G(x₂))}, h, F, G nonincreasing ≥ 1, h(0) = L₂ = #dom G,
F(0) = G(0) = L₃; faces A₃ = {x₂ < h(x₁)}, A₂ = {x₃ < F(x₁)}, A₁ = {x₃ < G(x₂)}; c(A) = #outer corners of a 2-D down-set A
(c(A₃) = #values of h, c(A₂) = #values of F, c(A₁) = #values of G); C = c(A₁) + c(A₂) + c(A₃).
Cone class: D = Cyl ∖ (q + ℕ³) with Cyl ∈ 𝒞, q ≥ (1,1,1), q ∈ Cyl (every non-two-face 3-D lattice tile is in 𝒞 or here).

**Lemma CHT (any D).** δ(D) ≥ m + 1 − (2t + 2|Tri| + |Q'|). **LEAN-CHECKED 2026-10-18** (lean/Wilf/CornerArea.lean `cht`, for
every finite D ⊆ ℕ³; the down-set hypothesis is not needed. Axioms propext, Classical.choice, Quot.sound; verified by the lead).
Proof. δ = 1 + Σ_x (h(x) − 1) (since H = Σ_x h(x)), h ≥ 0 integer, {h = 0} = Max ∪ Tri, {h = 1} = Q' (a non-maximal top has ht ≥ 1;
h = 1 forces two maximal tops and the third of height 1). So δ ≥ 1 − (t + Tri) + (m − t − Tri − Q'). ∎

**Level picture (𝒞).** φ(p) = min(F(p₁), G(p₂)) on A₃; U_v = {p ∈ A₃ : φ(p) ≥ v} = A₃ ∩ R_v, R_v = [0,a_v) × [0,b_v),
a_v = #{i : F(i) ≥ v}, b_v = #{j : G(j) ≥ v}; U₁ = A₃, U_{L₃+1} = ∅, U_{v+1} = U_v ∩ R_{v+1}. U_v is the slice x₃ = v − 1.
(i) (p, v−1) ∈ Max ⇔ p is a corner of U_v and p ∉ U_{v+1}. Write M_v for these p.
(ii) A corner p of U_{v+1} that is not a corner of U_v is the top cell of column a_{v+1} − 1 (then a_{v+1} < a_v) or the last
cell of row b_{v+1} − 1 (then b_{v+1} < b_v). [If p + e₁ ∈ U_v ∖ U_{v+1} then p + e₁ ∉ R_{v+1} ∋ p, so p₁ = a_{v+1} − 1 < a_v − 1.]

**Lemma T (type bound; 𝒞).** t ≤ C − 2. **LEAN-CHECKED 2026-10-18** (`typeBound`: (maxSet D).card + 2 ≤ Σ_c |faceCorners D c|
for every D in `LWClass`, the class 𝒞 with 0-based coordinates. The Lean proof is an explicit injection of Max into
corners(A₂) ⊔ (corners(A₁) ∖ {column-end corner}) ⊔ (corners(A₀) ∖ {row-end corner}), not the telescoping below).
Proof. Corners of U_v lying in U_{v+1} are corners of U_{v+1}; so |M_v| = κ(U_v) − κ(U_{v+1}) + ν_v with ν_v = #corners of U_{v+1}
that are not corners of U_v ≤ [a_{v+1} < a_v] + [b_{v+1} < b_v] by (ii), and ν_{L₃} = 0. Telescoping,
t = κ(A₃) + Σ_{v<L₃} ν_v ≤ c(A₃) + (c(A₂) − 1) + (c(A₁) − 1), because a drops at v exactly when v is a value of F, and the
value L₃ = F(0) is excluded (same for G). ∎ (Tight for boxes; exhaustive check: max(t − C) = −2 for every |D| ≤ 40, E125.)

**Lemma T' (cone class).** t ≤ C. **LEAN-CHECKED 2026-10-18** (lean/Wilf/ConeType.lean `typeBound_cone`: for Cyl in `LWClass`
and q ≥ (1,1,1), |Max(Cyl ∖ (q + ℕ³))| ≤ Σ_c |faceCorners|. q ∈ Cyl is not needed. `faceCorners_coneCut`: the faces are
unchanged, for any finite Cyl. `typeBound_cone_attained`: equality for the box [0,2)³ with q = (1,1,1). The Lean proof is an
injection with two exceptional cells: the top of column q₁ − 1 and the end of row q₂ − 1. Axioms propext, Classical.choice,
Quot.sound; verified by the lead.) Proof: as Lemma T; for v > q₃ the slices are U_v = (A₃ ∩ R_v) ∖ Q, Q = [q₁,∞) × [q₂,∞), and
U_{v+1} = U_v ∩ R_{v+1} for v ≠ q₃; at v = q₃ the removal of Q creates at most two further new corners (the top of column
q₁ − 1 and the end of row q₂ − 1). ∎ (Exhaustive: max(t − C) = 0, attained, union ≤ 34.)

**Lemma B (corner–area bound; 𝒞 and cone class).** C² − 3C + 6 ≤ 6m, i.e. C ≤ 3/2 + √(6m − 15/4).
**LEAN-CHECKED 2026-10-18** (`cornerArea`, for EVERY nonempty finite down-set D ⊆ ℕ³ with C = Σ_c #maximal elements of the
face D ∩ {x_c = 0}. This covers 𝒞 and the cone class, since there the faces are those of Cyl. Equality for D = {0}
and D = {0, e₁, e₂, e₃}).
Proof. A_c × {0}-type embeddings of the three faces lie in D (the cone misses the coordinate planes), so
m ≥ |A₁ ∪ A₂ ∪ A₃| = Σ|A_c| − (L₁ + L₂ + L₃) + 1. A 2-D down-set with k ≥ 1 corners and arms L, L' contains the two arms
(L + L' − 1 cells) and, for k ≥ 3, the triangle {(u,w) : u, w ≥ 1, u + w ≤ k − 1} (corner number s = u + 1 has coordinates
≥ (s − 1, k − s)); so |A| ≥ L + L' − 1 + T(k), T(k) = (k−1)(k−2)/2. Hence m ≥ Σ_c T(k_c) + L₁ + L₂ + L₃ − 2 with L₁ ≥ k₃,
L₂ ≥ k₁, L₃ ≥ k₂, and by convexity Σ T(k_c) ≥ 3T(C/3) = (C−3)(C−6)/6. ∎ (Tight for three staircase faces with q = (1,1,1).)

**Lemma F (forest; 𝒞).** |qU| ≤ t − 1. A qU cell x has x + e_a, x + e_b ∈ Max and x + e_c ∉ D ({a,b,c} = {1,2,3}): if
top_a x ∈ Max were x + s e_a with s ≥ 2 then ht(x) ≥ 2. Let G_U be the graph on Max with an edge {x + e_a, x + e_b} per qU
cell (simple: a pair y, y' = y + e_a − e_b determines x). Claim: G_U is a forest.
Proof. Edges with c = 3 join two consecutive corners of the same M_v (unit steps both ways, notch ∉ U_{v+1}); edges with
c = 1 join p ∈ M_{v+1} to p + e₂ ∈ M_v with p + e₁ ∉ U_v — then p₂ = b_{v+1} − 1 and p is the LEFTMOST corner of U_{v+1}
(the end of its top row); edges with c = 2 join the RIGHTMOST corner p of U_{v+1} to p + e₁ ∈ M_v. Build G_U by adding
levels from the top down: level v adds the vertices M_v, a linear forest of c = 3 edges inside M_v, and at most two edges
e_L (c = 1) and e_R (c = 2) to the levels above. A cycle can only be created if e_L, e_R both exist and their lower ends
p_L + e₂ (x₂ ≥ b_{v+1}, "top part") and p_R + e₁ (x₁ ≥ a_{v+1}, "right part") lie on the same c = 3 path of M_v. Walking
along that path from the top part to the right part needs either a consecutive unit-step pair ((a_{v+1}−1, b_{v+1}),
(a_{v+1}, b_{v+1}−1)) — its notch (a_{v+1}−1, b_{v+1}−1) lies in U_v ∩ R_{v+1} = U_{v+1}, so it is not a qU edge — or a corner
with x₁ ≥ a_{v+1} and x₂ ≥ b_{v+1}; then R_{v+1} ⊂ U_v, U_{v+1} = R_{v+1} has the single corner p_L = (a_{v+1}−1, b_{v+1}−1) and
p_L + e₁ ∈ U_v, so e_L does not exist. ∎ (Exhaustive: max(qU − t) = −1 on 𝒞, union ≤ 34; the cone class reaches 0.)

**Correction (2026-10-18, night 15).** The paragraph previously here proposed closing via Ω := 2|Tri| + |qO| ≤ C − 2
("data: union ≤ 34"). That bound is FALSE: simulated annealing finds Ω − C = +5 at m = 248 (E126). The single-peel
monotonicity of LHS − 4C fails at |D| = 17, 28–30, and (K) 2|Tri| + |Q'| ≤ 2t − 2 fails at m = 104 (E126). The refuted
items listed at the end of this section stand. The route below replaces Ω with two separate forest bounds.

Notation for the next lemmas (𝒞). φ(p) = min(F(p₁), G(p₂)) on A₃, so D = {(p, z) : p ∈ A₃, 0 ≤ z < φ(p)}. For p ∈ A₃ let
Π(p) = {q ∈ A₃ : q ≥ p, φ(q) = φ(p)} (the plateau of p) and γ(p) = max_{q ∈ Π(p)} |q − p|.
(P0) For x = (p, z) ∈ D: top₃(x) = (p, φ(p) − 1) and ht(top₃ x) = γ(p). [z ≥ φ(p) − 1 and φ(q) ≤ φ(p) for q ≥ p.]
So top₃(x) ∈ Max ⇔ γ(p) = 0 ("p is a peak"). If p + e₁ ∈ A₃ and γ(p) = 0 then F(p₁ + 1) < G(p₂) and F(p₁ + 1) < F(p₁).
[φ(p + e₁) = min(F(p₁+1), G(p₂)) < min(F(p₁), G(p₂)).] Symmetrically, p + e₂ ∈ A₃ and γ(p) = 0 give G(p₂ + 1) < F(p₁).
(P1) If p'' ≤ p and φ(p'') = φ(p) then Π(p) ⊆ Π(p''), so γ(p'') ≥ |p − p''| + γ(p).
Every tripod and every qO cell x satisfies x + e_d ∈ D for d = 1, 2, 3. [A maximal top of a non-maximal x is ≠ x;
the non-maximal top of a qO cell is ≠ x by definition of qO.] 𝒞 is invariant under permuting coordinates, and so are
the notions Max, Tri, qU, qO; "by symmetry" below refers to this.

**Lemma S (sharing; 𝒞).** Let x, x' ∈ D both satisfy x + e_d, x' + e_d ∈ D for all d. If top_a(x) = top_b(x') = y ∈ Max,
then a = b; hence x and x' lie on the a-line through y.
Proof. Suppose a ≠ b and let c be the third direction. Then x = y − i e_a, x' = y − i' e_b. The cells x + e_c and x' + e_c
lie in D. A set in 𝒞 is determined by its three coordinate projections: z ∈ D ⇔ π_d(z) ∈ π_d(D) for d = 1, 2, 3.
Here π_a(y + e_c) = π_a(x + e_c), π_b(y + e_c) = π_b(x' + e_c) and π_c(y + e_c) = π_c(y). So y + e_c ∈ D, contradicting
y ∈ Max. ∎

**Lemma P (projection chain; 𝒞).** Let x, x' be tripods and (a, b) two coordinates. It is impossible that
x_a < x'_a and x_b > x'_b.
Proof. By symmetry (a, b) = (1, 2). Write p = (x₁, x₂) = (X, Y) and p' = (X', Y') with X < X' and Y > Y'. Both p and p'
are peaks (top₃ ∈ Max). Also p + e₁ ∈ A₃ (since x + e₁ ∈ D) and p' + e₂ ∈ A₃ (since x' + e₂ ∈ D). By (P0),
F(X + 1) < G(Y) and G(Y' + 1) < F(X'). Monotonicity then gives F(X') ≤ F(X + 1) < G(Y) ≤ G(Y' + 1) < F(X'). ∎
(Checked: no violation for any D ∈ 𝒞 with |D| ≤ 17, src/scratch/chaincheck.py.)

**Lemma TF (tripod forest; 𝒞).** 2|Tri| ≤ t − 1.
Proof. List the tripods by decreasing |x|. Suppose tripod x shares a top with an earlier tripod x'. By Lemma S they share
it as top_a for one direction a, and x' lies on the a-line through x. Since |x'| > |x|, x' = x + i e_a with i ≥ 1. If this
happened for two directions a ≠ b, the tripods x + i e_a and x + i' e_b would violate Lemma P in the (a, b)-plane. So at
most one of x's three (distinct) tops occurs among the tops of earlier tripods. The first tripod contributes 3 new
maxima and each later one at least 2, so if Tri ≠ ∅ then 2|Tri| + 1 ≤ t. ∎

**Lemma QF (qO forest; 𝒞).** |qO| ≤ t − 1.
Proof. List the qO cells by increasing |x|. By Lemma S, an earlier qO cell sharing the maximal top top_a(x) is x − i e_a
with i ≥ 1. We claim this cannot happen for both maximal-top directions of x. Then each qO cell adds at least one new
maximum and the first adds two, so |qO| + 1 ≤ t.
By symmetry let the non-maximal top of x be top₃; its maximal tops are top₁ and top₂. Write x = (p, z) with p = (X, Y).
By (P0), γ(p) = 1. Also p + e₁, p + e₂ ∈ A₃.
(1) If x' = x − i e₁ (i ≥ 1) is a qO cell, then F(X) < G(Y). Its non-maximal direction c' is 2 or 3, since top₁ x' =
top₁ x ∈ Max. Put p' = p − i e₁.
 - If c' = 2, then top₃ x' ∈ Max, so γ(p') = 0. As p' + e₁ ≤ p lies in A₃, (P0) gives F(X − i + 1) < G(Y), and F(X)
   ≤ F(X − i + 1).
 - If c' = 3, then γ(p') = 1. If φ(p') = φ(p), (P1) would give γ(p') ≥ i + 1 ≥ 2. So φ(p') = min(F(X − i), G(Y))
   > min(F(X), G(Y)), which forces F(X) < G(Y).
(2) Symmetrically, if x'' = x − i' e₂ (i' ≥ 1) is a qO cell, then G(Y) < F(X).
(1) and (2) are incompatible. ∎

**LEAN-CHECKED 2026-10-18 (lean/Wilf/Forest.lean, verified by the lead; standard axioms, 0 sorry):** Lemma TF (`tripodForest`,
`tripodForest''`: 2|Tri| + 1 ≤ t), Lemma F (`qUForest`: |qU| + 1 ≤ t), Lemma QF (`qOForest`: |qO| + 1 ≤ t),
`forestBound` (LHS + 3 ≤ 5t) and **`deltaBound`: 2m + 13 ≤ H + 5C, i.e. δ ≥ m + 14 − 5C, for every D in `LWClass`**.
The proofs go through `IsLW` (a down-set determined by its three projections), so the paper's "by symmetry" is a
general frame (a, b, c). TF and QF are injections Σ_x N(x) → Max rather than elimination orders. Lemma F has a new short
proof: an explicit injection qU → Max ∖ {y*}. Not yet in Lean: the threshold arithmetic (5C ≤ m + 14 for m ≥ 131).
**Theorem C-HT (𝒞; proved on paper 2026-10-18 night 15).** Every D ∈ 𝒞 satisfies LHS = 2t + 2|Tri| + |qU| + |qO|
≤ 2t + 3(t − 1) = 5t − 3 ≤ 5C − 13 (Lemmas TF, F, QF, T). With Lemma CHT this gives δ(D) ≥ m + 14 − 5C. By Lemma B,
C ≤ ⌊3/2 + √(6m − 15/4)⌋ ≤ (m + 14)/5 for every m ≥ 131: checked exactly for 131 ≤ m < 2·10⁵, and for m ≥ 160 it holds
because 5(3/2 + √(6m)) − 14 ≤ m. Hence **δ(D) ≥ 0 (HT) for every D ∈ 𝒞 with |D| ≥ 131.**
Consequence for e = 4: every non-two-face tile in 𝒞 with m ≥ 131 satisfies the height criterion, so Wilf holds for the
corresponding semigroups.
**Integrality sharpening (chain referee 2026-10-18; checked by the lead).** The height criterion (m+1)H ≤ mW + m(m−1) with
W ∈ ℤ gives Wilf already when δ ≥ −1 (H ≥ m − 2): then mW ≥ (m+1)(m−2) − m(m−1) = −2, so W ≥ 0 for m ≥ 3. Hence C-HT
closes for m ≥ 130 (5C ≤ m + 15; the last failing m is 129), and the cone Corollary below for m ≥ 280 (6C + 28 ≤ m; at m = 280,
C_max = 42). The HT-failing tiles with δ = −1 (m = 17, 23) need no LP certificate. The tiles still uncovered are (i) 𝒞-tiles with m ≤ 130, handled by the exhaustive HT scan
(tile_scan_HM, complete so far for m ≤ 82, 91–95, 101–104, 109–111), and (ii) cone-class tiles, which need a separate
bound. [Superseded 2026-10-18: the scan is complete and area-certified for every m ≤ 280 (E140, E141), and Theorem cone
below supplies the cone bound.] In the lattice-free cone class LHS − 5C is unbounded above, and 2|Tri| − t reaches 8 at union ≤ 32.
Data (E127): on 𝒞 with |D| ≤ 32, max(2Tri − t) = max(qO − t) = max(qU − t) = −1 and max(LHS − 4C) = −10, so the sharper
(A4) LHS ≤ 4C − 10 (threshold m ≥ 85) remains OPEN.

Refuted on the way (E126): per-direction double-drop bound qO_c + Tri ≤ dd_c; Tri ≤ min(#top-only, #right-only maxima)
via a row-end injection (two tripods can share the row end when the apex rectangles shrink in one coordinate only);
o-pairs 3Tri + qO ≤ C − 2 (fails at |D| = 27); single-step peeling monotonicity of LHS − 4C (fails at |D| = 17, 28–30,
always on sets with slack ≥ 1); in the cone class LHS ≤ 4C + O(1) is FALSE (three staircase faces, q = (1,1,1):
LHS = 5C − 25), so cone tiles need lattice input or a 5C-type bound with a larger finite range.

## Cone tiles: wall and floor lemmas (PROVED 2026-10-18 night 15), defect localization (PROVED), status

Setting: D is a 3-D lattice tile (down-set fundamental domain of Λ ⊂ ℤ³) in the cone class, D = Cyl ∖ K with K = q* + ℕ³,
q* ≥ (1,1,1), q* ∈ Λ (cylinder lemma (a)). For c ∈ {1,2,3} with {a, b, c} = {1,2,3}: A_c = face x_c = 0, L_c = |D ∩ ℕe_c|.
An inner corner of a 2-D down-set S is w ∉ S with w − e_a, w − e_b ∈ S (w_a, w_b ≥ 1).

**Wall Lemma.** A_c has at most q_c inner corners w with w ≥ (q_a, q_b). Each such corner (as the point g = (w, 0)) satisfies
g ≡ t_w e_c (mod Λ) with L_c − q_c ≤ t_w ≤ L_c − 1, and the t_w are distinct.
Proof. g is a minimal non-element with g_c = 0 < g_a, g_b. By cylinder lemma (b), g ≡ t e_c with t e_c ∈ D, distinct t
for distinct g. The cell P := (w − (q_a, q_b), 0) lies in D, since it is ≤ g − e_a. Also P = g − q* + q_c e_c ≡ (t + q_c) e_c.
If t + q_c ≤ L_c − 1, then (t + q_c) e_c ∈ D is a second cell in the class of P, which is impossible (their c-coordinates
are 0 and ≥ 1). So t ≥ L_c − q_c. ∎

**Floor Lemma.** Let S be the slice of D at height x_c = q_c − 1 (a 2-D down-set). Then S has at most one inner corner
w ≥ (q_a, q_b). Hence the floor F_c := S ∩ ([q_a,∞) × [q_b,∞)) has at most two outer corners. The floor maxima
Fl_c ∩ Max = {y ∈ Max : y + e_c ∈ K} are exactly the cells of D at height q_c − 1 over those corners, so there are at most 2
for each c.
Proof. Let W be w placed at height q_c − 1. Then W ∉ D, W ∉ K (W_c < q_c), so W ∉ Cyl, while W − e_a, W − e_b ∈ D. Cyl is
cut out by its three projections, and π_a(W) = π_a(W − e_a), π_b(W) = π_b(W − e_b) are admissible. So w = π_c(W) ∉ A_c,
while w − e_a, w − e_b ∈ A_c. Thus w is an inner corner of A_c with w ≥ (q_a, q_b), and by the Wall Lemma w ≡ t_w e_c
with t_w ∈ [L_c − q_c, L_c − 1].
For 0 ≤ j ≤ q_c − 1 the cell P_j := (w − (q_a, q_b), j) is ≤ W − e_a, so it lies in D, and P_j ≡ (t_w + q_c + j) e_c.
Suppose there were two such corners w ≠ w' with t_w < t_{w'}. Then 1 ≤ d := t_{w'} − t_w ≤ q_c − 1. P_d (built from w)
and P'_0 (built from w') are distinct cells of D (c-coordinates d ≥ 1 and 0) in the same class (t_{w'} + q_c) e_c.
Contradiction. ∎ (Data: every cone tile with m ≤ 48 has 1 or 2 floor maxima per direction, logs via
src/scratch/cone_tile_floor.py.)

**Defect localization (cone class, no lattice needed).**
(S') If x, x' satisfy x + e_d, x' + e_d ∈ D for all d, and top_a(x) = top_b(x') = y ∈ Max with a ≠ b, then y + e_c ∈ K.
Proof: as Lemma S, y + e_c ∈ Cyl; it is not in D, so it is in K.
(P') If tripods u, u' satisfy u_a < u'_a and u_b > u'_b, then top_c(u) + e_a ∈ K or top_c(u') + e_b ∈ K.
Proof: in Lemma P the height is now ψ = min(F, G, Q) with Q = q*_c on the quadrant [q_a,∞) × [q_b,∞) and ∞ elsewhere.
The two peak inequalities used there fail only when the drop comes from Q. Such a drop at u's projection means top_c(u)
sits on the wall x_a = q_a − 1 at height ≥ q_c, i.e. top_c(u) + e_a ∈ K (symmetrically for u'). ∎
(Q') The qO argument (Lemma QF) breaks only through a Q-drop as well. Then one of top_c(x), top_c(x − i e_a),
top_c(x − i' e_b) is a cell y with y + e_d ∈ K for some d.
So every failure of the 𝒞 forest arguments is witnessed by cells adjacent to K. In a tile these cells lie in the three
floors, which have at most 2 outer corners each by the Floor Lemma.

**Status / data (E128).**
- Real cone tiles, m ≤ 48: tripod elimination excess is always 0, i.e. 2Tri ≤ t − 1. The qO elimination excess is ≤ 1
  (in ≤ 6 tiles per m), so qO ≤ t. The unit-notch graph has ≤ 1 cycle (the triangle around q* when all q* − e_a are
  maximal), so qU ≤ t. Also t ≤ C.
- Lattice-free cone class: 2Tri − t is unbounded (three staircases, q = (1,1,1)).
- Adding the proven Wall + Floor constraints ("RCON", union ≤ 32): 2Tri − t ≤ 2, qO − t ≤ 0, qU − t ≤ 0,
  LHS − 5C ≤ −6, LHS − 4C ≤ −2.
- Every RCON set with tripod excess that was tested is NOT a lattice tile: 200/200 checked by exhaustive search for
  r ∈ (ℤ/m)³ (src/scratch/is_tile.py). The obstruction is a global congruence chain, not a local one.
OPEN (needed for e = 4): a bound LHS ≤ 5C + β for cone tiles. With β = 2 and Lemma B the HT scan must reach m = 160
(thresholds: 5C − 6 → 148, 5C − 1 → 158, 5C + 2 → 161, 4C + 6 → 113).

### Lattice Corner Lemma (LCL) and the pairwise relaxation PW — PROVED 2026-10-18 night 16 (any 3-D lattice tile)
Setting as in the cylinder lemma; {a, b, c} = {1, 2, 3}; for a non-axis inner corner w of the face A_c (w ∉ A_c,
w − e_a, w − e_b ∈ A_c, w_a, w_b ≥ 1) let t_w ∈ [0, L_c) be the multiplier of cylinder lemma (b): (w, 0) ≡ t_w e_c.
**LCL.** Let w, w' be two such corners with w_a < w'_a (so w_b > w'_b), α = w'_a − w_a, β = w_b − w'_b, t = t_w, t' = t_{w'}.
If t' > t then β e_b + (t' − t) e_c ∉ D. If t' < t then α e_a + (t − t') e_c ∉ D.
Proof. λ = (w, 0) − t e_c and λ' = (w', 0) − t' e_c lie in Λ, so v = λ' − λ = α e_a − β e_b − (t' − t) e_c ∈ Λ ∖ {0}.
D is a fundamental domain and a down-set, so v⁺ and v⁻ are not both in D (else v⁺ ≠ v⁻ would be congruent elements of D).
If t' > t: v⁺ = α e_a, and α ≤ w'_a with (w'_a, w'_b − 1) ∈ A_c gives α e_a ∈ D; hence v⁻ = β e_b + (t' − t) e_c ∉ D.
If t' < t: v⁻ = β e_b ∈ D (β ≤ w_b, (w_a − 1, w_b) ∈ A_c); hence v⁺ = α e_a + (t − t') e_c ∉ D. ∎
In 𝒞/cone notation with c = 3: t' > t ⇒ t' − t ≥ G(β); t' < t ⇒ t − t' ≥ F(α).
(Checked: every tile m = 30, 40, 50, 60, all pairs, 0 violations; src/scratch/lcl_check.py.)
**Corollary (quadrant steps).** If moreover w, w' ≥ (q_a, q_b) (cone tile), both t, t' ∈ [L_c − q_c, L_c − 1] (Wall Lemma),
so G(β) ≤ q_c − 1 or F(α) ≤ q_c − 1 (in the c = 3 notation), according to the sign of t' − t.
**PW (pairwise relaxation).** Let V be the family of all vectors (w, −t_w e_c) over all faces and all non-axis inner
corners, together with q* if present. Then every v ∈ V and every v ± v' (v ≠ v' ∈ V) is a nonzero element of Λ, so it
satisfies NOT(v⁺ ∈ D ∧ v⁻ ∈ D). [Nonzero: each sum has a coordinate ≥ 2; each difference of distinct members has a
nonzero (a,b)-part or a c-coordinate ≤ −1.] LCL is the same-face difference case and the Wall Lemma is the v − q* case.
So "there exist multipliers t_w satisfying PW" is a shape-only necessary condition for D to be a tile
(src/scratch/lattice_pairwise.py; C version src/c/cone_pw.c). Data in E130: it removes every tripod-excess set of
the Wall+Floor class (union ≤ 30), and the PW class satisfies 2Tri ≤ t − 1, qO ≤ t − 2, qU ≤ t, LHS ≤ 5C − 6
(union ≤ 34, EXHAUSTIVE for that class).
**Threshold arithmetic.** If C ≤ 2√m + c and LHS ≤ 5C + β on cone tiles, then HT holds for m − 10√m − 5c − β + 1 ≥ 0.
OPEN pieces: (β) a corner–area bound C ≤ 2√m + c for cone tiles (𝒞 sketch in NOTEBOOK night 16); (α) forest-type bounds
2Tri ≤ t + β₁, qO ≤ t + β₂, qU ≤ t + β₃ for cone tiles, using Wall/Floor/PW input.

## Final-window criteria for all e (FW, FWx, FWy) — PARKED 2026-10-18 (advisor decision: finish the e = 4 tile route first)
Notation: see NOTEBOOK night 17 (cont.). T = term-order factorization ideal of Ap(S, m) in ℕ^d (d = e − 1);
u(x) = M − λ(x); lines ℓ with top t_ℓ; Z = {x : λ(x) ≥ c}; R_j(L) = Σ_{r<L} [r a_j]_m.
- **EXACT (KNOWN, Zhai Lemma 3 / CH′ form):** m·W = C(m,2) + Σ_ℓ Σ_{x∈ℓ} (u(t_ℓ) − [u(x)]_m).
- **FW (PROVED, any e; kseth (p:6) generalized):** m·W ≥ m·(P(T) − dτ) − (m−1)·E(Z).
- **FWx (PROVED as an inequality):** m·W ≥ C(m,2) + Σ_deep (m + C(L,2)) − Σ_final R_j(L).
- **FWy (PROVED as an inequality):** m·W ≥ C(m,2) + Σ_deep (m + C(L,2)) + Σ_final Σ_{x∈ℓ} (u(t_ℓ) − [u(x)]_m).
- **Conjecture FWx-deep (OPEN):** FWx ≥ 0 whenever c > 3m. Together with Eliahou's theorem (c ≤ 3m ⇒ Wilf,
  LITERATURE #13), this would prove Wilf for every numerical semigroup.
  Evidence (E134): no failure among the 429,544 S with genus ≤ 23 or about 40k random hard S. The only 2 failures found
  have c ≤ 3m: ⟨13,20,21,23,25⟩ and ⟨13,17,21,23,24⟩. Adversarial annealing restricted to c > 3m: min FWx/m = 7.8.
- **Conjecture FWy (OPEN, strengthens Wilf):** FWy ≥ 0 for every S. No failure anywhere tested.
- Known obstructions: shape-only weakenings fail even when c > 3m (FW3/FW3b: ⟨3,11,13⟩, ⟨25,34,43⟩), so a proof must use
  the residues [r a_j]_m. FW alone fails on simplex-like T whose top layer lies entirely in Z.
- **Next step when unparked:** bound Σ_final R_j(L) = Σ_{j,r} f_{j,r}[r a_j]_m (f_{j,r} = #{z ∈ Z : z_j ≥ r}) using
  |λ(z) − λ(z')| < m on Z and the distinctness of the axis residues. Test it on the two failures and the adversarial
  near-minima first.

## Cone tiles: QF-pair lemma, location corollary, Fiber Lemma, and qO ≤ 2t + 11 — PROVED 2026-10-18 night 17 (paper)
## ⇒ HT for every cone tile with m ≥ 281 (with TF-cone, F-cone, T′, B, CHT)
Setting: cone class D = Cyl ∖ K, Cyl ∈ 𝒞, K = q + ℕ³, q ≥ (1,1,1), q ∈ Cyl. Everything below is lattice-free except
|Y_d| ≤ 2 (Floor Lemma, cone tiles). 𝒞 and K are invariant under permutations of coordinates. So each statement is proved for
one labelling (nonmax direction 3, partner direction 1, third direction 2), and "mirror" swaps coordinates 1 and 2.
Notation (c = 3):
- D = {(p, z) : p ∈ A₃, z < ψ(p)}, where ψ(p) = min(F(p₁), G(p₂), Q(p)).
- Q(p) = q₃ on Quad = [q₁,∞) × [q₂,∞), and ∞ elsewhere. ψ is nonincreasing.
- Y_d = {y ∈ Max : y + e_d ∈ K}, Y = ∪ Y_d, and B_c = {x : x_a ≥ q_a, x_b ≥ q_b, x_c < q_c} (the cells directly under K).
- A qO cell has two maximal tops and a nonmaximal top of height 1 different from itself; then x + e_d ∈ D for all d.

(P0′) top₃(p, z) = (p, ψ(p) − 1) and ht(top₃) = γ(p) := max{|p′ − p| : p′ ≥ p, p′ ∈ A₃, ψ(p′) = ψ(p)}.
(P1′) If p″ ≤ p and ψ(p″) = ψ(p), then γ(p″) ≥ |p − p″| + γ(p).
(Peak′) If p + e₁ ∈ A₃ and γ(p) = 0, then F(p₁+1) < G(p₂), or [p₁ + 1 = q₁, p₂ ≥ q₂ and top₃(p, ·) + e₁ ∈ K].
Proof of (Peak′): γ(p) = 0 forces ψ(p + e₁) < ψ(p). Suppose F(p₁+1) ≥ G(p₂). Then ψ(p+e₁) = min(G(p₂), Q(p+e₁)) and
ψ(p) ≤ G(p₂). This forces Q(p + e₁) = q₃ < ψ(p) ≤ Q(p), so p + e₁ ∈ Quad ∌ p, and ψ(p) − 1 ≥ q₃. ∎ (The proofs of
(P0′) and (P1′) are those of P0 and P1 with ψ in place of φ; they use only that ψ is nonincreasing.)

**QF-pair Lemma.** Let v = (X, Y, z) be qO with nonmax direction 3, and u = v − i e₁ (i ≥ 1) qO with top₁(u) = top₁(v).
Put p = (X, Y) and p′ = (X − i, Y). Then F(X) < G(Y) unless
(α) u has nonmax direction 2 and top₃(u) + e₁ ∈ K, or
(β) u has nonmax direction 3, p ∈ Quad, p′ ∉ Quad and ψ(p) = q₃.
Proof. u's nonmax direction is not 1, since top₁(u) ∈ Max.
- If it is 2: γ(p′) = 0 and p′ + e₁ ≤ p ∈ A₃, so (Peak′) gives F(X−i+1) < G(Y) or (α). Then F(X) ≤ F(X−i+1).
- If it is 3: γ(p′) = γ(p) = 1, so ψ(p′) ≠ ψ(p) by (P1′); hence ψ(p′) > ψ(p). If F(X) ≥ G(Y), then
  ψ(p) = min(G(Y), Q(p)) < ψ(p′) ≤ min(G(Y), Q(p′)). This forces Q(p) = q₃ < Q(p′) = ∞ and ψ(p) = q₃, which is (β). ∎
Mirror: if u = v − i e₂ is qO with top₂(u) = top₂(v), then G(Y) < F(X) unless (α′) [u has nonmax direction 1 and
top₃(u) + e₂ ∈ K] or (β′) [u has nonmax direction 3, p ∈ Quad, p − ie₂ ∉ Quad and ψ(p) = q₃].

Definition. A qO cell x is **doubly-same (DS)** if, for both of its maximal directions d, some qO cell u ≠ x with
u_d < x_d has top_d(u) = top_d(x). (Such u is then x − i e_d.)

**Location Corollary.** A DS cell x with nonmax direction c lies in B_c.
Proof (c = 3). If neither the 1-partner pair nor the 2-partner pair is defective, then F(X) < G(Y) < F(X). Under (α),
top₃(u) = (X − i, Y, ψ(p′) − 1) ∉ K while +e₁ ∈ K. So X − i = q₁ − 1, Y ≥ q₂, and u + e₁ = (q₁, Y, z) ∈ D ∖ K forces
z < q₃ (u + e₁ ∈ D because u is a qO cell, so every u + e_d lies in D). Under (β), p ∈ Quad and z < ψ(p) = q₃. The
mirror cases are symmetric. ∎

**Fiber Lemma.** Two distinct DS cells never share a maximal top in the same direction.
Proof. Let x̂ = x + k e_a (k ≥ 1) with the same top_a, and let c, ĉ be their nonmax directions (both ≠ a).
- ĉ ≠ c: by the Location Corollary, x_ĉ ≥ q_ĉ (x ∈ B_c) and x̂_ĉ < q_ĉ (x̂ ∈ B_ĉ). But x̂_ĉ = x_ĉ. ✗
- ĉ = c = 3, a = 1: x = (X, Y, z) and x̂ = (X+k, Y, z), both in B₃, so p = (X, Y) and p̂ = (X+k, Y) lie in Quad.
  - γ(p) = γ(p̂) = 1, so by (P1′) ψ(p) > ψ(p̂). With Q = q₃ at both, this gives F(X+k) < min(F(X), G(Y), q₃).
    Hence (i) F(X+k) < G(Y), (ii) F(X+k) < q₃ and ψ(p̂) = F(X+k).
  - x̂ has a 2-partner û. By (i) and the mirror lemma, (α′) or (β′) holds. (β′) needs ψ(p̂) = q₃, contradicting (ii).
    (α′) gives top₃(û) = (X+k, q₂−1, ψ − 1) with ψ(X+k, q₂−1) = min(F(X+k), G(q₂−1)) ≥ q₃ + 1, contradicting (ii). ∎

**Theorem (qO-cone).** For every cone-class set, qO ≤ 2t − 1 + 2|Y|. For cone tiles (|Y| ≤ 6) this is qO ≤ 2t + 11.
(Correction 2026-10-18: this line first read "t − 1 + 2|Y|", a typo; the proof below gives 2t − 1 + 2|Y|. The typo'd bound is
FALSE lattice-free; do not revive it as a sharpening. Referee counterexample: h = (11, 11, 2×10), F = (11, 11, 10, 9, …, 1),
G = (11, 11, 9, 8, …, 1), q = (1, 1, 10), with m = 243, t = 21, |Y| = 3, qO = 27 > 26. Rechecked by the lead.)
Proof.
- Let G_O be the multigraph on Max with one edge {top_a x, top_b x} per qO cell. Then qO = t − comp(G_O) + rank(G_O),
  and rank = #cycle-closing edges when the cells are added in increasing |x|.
- A cycle-closing x has both maximal tops already used. For each such top y_d, either an earlier user uses it in
  direction d (then that user lies on the d-line below x), or every earlier user uses it in another direction. In the
  second case y_d ∈ Y by S′, and x is the first user of y_d in direction d. Each y is a top in ≤ 2 directions (three
  would put y in K), so the second case happens for ≤ |Y| cells. [The first user of y, in any direction, is not
  second-case at y, and in y's second direction only its first user is; so each y ∈ Y is second-case for ≤ 1 cell.]
- All other cycle-closers are DS. Map each DS cell x to top_{a(x)}(x), where a(x) is its smaller maximal direction.
  Collisions in the same direction are excluded by the Fiber Lemma. Collisions in different directions land in Y (S′),
  at most 2 per y. So #DS ≤ t + |Y|, rank ≤ 2|Y| + t, and qO ≤ t − 1 + rank ≤ 2t − 1 + 2|Y|. ∎
(Refinement: the image of DS lies in Max ∩ (B₁ ∪ B₂ ∪ B₃), so qO ≤ t − 1 + 2|Y| + |Max ∩ B|.)

**LEAN-CHECKED 2026-10-18 (lean/Wilf/ConeForest.lean, verified by the lead; standard axioms, 0 sorry).** For every
`ConeSet Cyl D q` (Cyl projection-determined, q ≥ (1,1,1), D = Cyl ∖ (q + ℕ³); q ∈ Cyl not needed), the Lean versions
are SHARPER than the paper's:
- `qU_cone`: |qU| ≤ t (paper F-cone: t + 2);
- `qO_cone`: |qO| + 1 ≤ 2t + |Y| (paper: 2t + 2|Y|; the DS fibres have size ≤ 2, so #DS ≤ t);
- `tf_cone`: 2|Tri| ≤ t + |Y| + 11 when every |Y_d| ≤ 2 (paper: t + 17);
- `coneDelta_sharp`: 2m ≤ H + 6t + 2|Y| + 10, hence 2m ≤ H + 6C + 22, i.e. **δ ≥ m − 6C − 21**.
The requested paper forms (`fCone`, `qOCone`, `tfCone`, `coneDeltaBound` with +30, `coneThreshold` m ≥ 281,
`coneThreshold'` m ≥ 280) are corollaries. The only lattice input left as a hypothesis is |Y_d| ≤ 2 (Floor Lemma).
**Sharper threshold:** with δ ≥ m − 6C − 21 and Lemma B, δ ≥ 0 for m ≥ 267 and δ ≥ −1 for m ≥ 266 (exact check
m < 2·10⁵, by the Lean agent and by the lead). The paper constants below are kept for the record.
**Corollary (HT for large cone tiles).** For every cone tile:
- Lemma CHT: δ(D) ≥ m + 1 − LHS.
- LHS = 2t + 2Tri + qU + qO ≤ 2t + (t + 17) + (t + 2) + (2t + 11) = 6t + 30, by TF-cone, F-cone and qO-cone (NOTEBOOK
  night 17).
- Lemma T′ (t ≤ C) and Lemma B (C ≤ ⌊3/2 + √(6m − 15/4)⌋) then give δ(D) ≥ m − 6C − 29 ≥ m − 6√(6m) − 38.
- So **δ(D) ≥ m − O(√m)** for all cone tiles, and HT (δ ≥ 0) holds for every cone tile with **m ≥ 281** (checked: the
  last m with 6⌊3/2 + √(6m − 15/4)⌋ + 30 > m + 1 is 280). With the integrality sharpening (above, after Theorem C-HT),
  δ ≥ −1 suffices for Wilf, and it holds for m ≥ 280.
- With Theorem C-HT (𝒞-tiles, m ≥ 131) and the complete HT scan for m ≤ 130, the only remaining range is cone tiles
  with 131 ≤ m ≤ 280. That is a finite computation (C scanner; MAXM must be raised from 255).
Checks (src/scratch/qo_fiber_check.py, qo_fiber_anneal.py, qo_fiber_exh.py):
- (A) location, (B) Fiber, (C) cross-only closers ⊆ Y, and rank/qO accounting: 0 violations on all cone tiles of
  m = 30, 40, 50, 60, 64 and on the RCON extremes.
- RCON anneals maximizing the fiber size never exceed 1.
- Exhaustive lattice-free cone sets: see EXPERIMENTS E135.
Status: PROVED on paper by the lead. **Independently reviewed 2026-10-18** by an adversarial referee agent. Verdict:
every lemma of this section, TF-cone, F-cone, T′, B, Wall, Floor and the Corollary's arithmetic is CORRECT, by argument and
by an independent checker. The checker (src/review/indep.py) found 0 violations on all lattice-free sets with lengths/values
≤ 5 (8,630,220 sets, 7,843,965 cone), on all 82,242 tiles in logs/tiles, on ~112k random sets and in 92 anneals. Wording
fixes are applied here and in NOTEBOOK night 17 (marked "referee edit"). Report: .research/reviews/cone_review_2026-10-18.md.
Lean (updated 2026-10-18): B, CHT, T, T′ (ConeType.lean), TF/F/QF (Forest.lean) and the cone bounds (ConeForest.lean) are kernel-checked; Wall/Floor are not (|Y_d| ≤ 2 is a hypothesis there).
**The coefficient 2 is the natural lattice-free answer (2026-10-18).** In the lattice-free cone class, qO − t is unbounded:
q = (1, 1, Q), F = (Q+3, Q+1, Q, Q−1, …, 1), G = (Q+3, Q+1, Q−1, Q−2, …, 1), h = (|G|, |G|, 2, …, 2) has t = 2Q + 2,
qO = 3Q − 3 and #DS = Q − 1 (Q = 4..12, src/scratch/ds_family.py; examples/qO_lattice_free_family.md). These sets violate the
Wall/Floor constraints, so they are not tiles. A bound qO ≤ t + O(1) therefore needs lattice input. The advisor's revised
plan (2026-10-18) needs only qO ≤ 2t + O(1) together with a proved sublinear bound on t. That bound is t ≤ C
(Lemma T′) and C ≤ 3/2 + √(6m − 15/4) (Lemma B), both proved on paper, so no sharper qO constant is pursued for now.

---------------------------------------------------------------------------------------------------
## Results of 2026-10-18 (late night): exact identities and the limits of shape-only criteria
**Column form of Wilf (any e; = CH′).** For every S with tile D ⊂ ℕ^d (d = e − 1), mW + (d−1)m(m−1)/2 = B, where
B = Σ_{(x,a) ∈ D×[d]} (Λ − λ(top_a x)) = dmΛ − (d+1)Σ_D λ. For ANY finite down-set D and positive weights w,
d|D|·max_D(x·w) − (d+1)Σ_D x·w = Σ_{(x,a)}(max − w·top_a x) ≥ 0. PROVED (column sums).
**Level/carry split (any e).** n_a = r_a + m k_a (1 ≤ r_a ≤ m − 1), x* = λ-argmax. Then W = Lev + Car with
Lev = dm(x*·k) − (d+1)Σ_D x·k and Car = d(x*·r) − (d+1)mean_D(x·r) − (d−1)(m−1)/2. Lev ≥ 0 if x* maximizes x·k on D.
PROVED (Kunz coordinates K(x) = x·k + ⌊x·r/m⌋, Selmer's g = ΣK, Σ_D (x·r mod m) = m(m−1)/2). CHECKED: 1,600+ random S.
**Shift lemma.** If n and n + km·(1,…,1) have the same tile and the λ-argmax lies at the maximal level N, then
mW(n + km·1) − mW(n) ≥ km·(dmN − (d+1)Σ_D|x|) ≥ 0. Level-≤ 2 tiles are preserved by such shifts. PROVED.
**Near-star formula.** D = {0, e_1..e_d} ∪ Q, Q = q level-2 non-square cells covering every e_b, m = d + 1 + q:
HCR(D) = [(m+1)(d(d+1) − 2q) + (d+2)q(q−1)/2] / [(d−1)m(m−1)/2]; = 112/117 for d = 4, q = 8 (the two m = 13 HCR failures);
→ 1 − 1/d + O(1/(βd²)) for q = βd². Hence no shape-only criterion of HCR/HCR+ type is universal. PROVED (direct count).
**Carry-free level 2.** If every n_a = m + r_a, every r_a < m/2 and Ap ⊆ {0} ∪ {n_a} ∪ {n_a + n_b}, then W = e(e+1) − 2m ≥ 0.
PROVED.
**Computational theorem (e = 5).** Every 4-D lattice tile with 14 ≤ m ≤ 39 has HCR ≥ 1 (E153: 9,532,388 tiles,
exact volume and facet certificates, checked through m = 39); with BGOW (m ≤ 18), Wilf holds for every S with e = 5 and m ≤ 39.
Independent re-check by 4ti2 + gfan (E160): agrees for m ≤ 27 so far, running to 36.

## Down-set Wilf (GW) — CONJECTURE; the equivalences and the box case are PROVED

**Setting.**
- D ⊂ ℕ^d is a finite down-set with |D| = m, and n ∈ ℤ^d is such that x ↦ x·n mod m is a bijection D → ℤ/m.
- Equivalently, D is a fundamental domain of the lattice Λ = {x : x·n ≡ 0 mod m}, and n is a unit-class element of
  Λ^∨ = ℤn + mℤ^d.
- Notation:
  - v(x) = x·n and M = max_D v;
  - κ = ⌊v/m⌋ and λ = ⌊(M − v)/m⌋;
  - B(D,n) = dmM − (d+1)Σ_D v and τ = (d−1)m(m−1)/2.

**Conjecture GW.** B(D,n) ≥ τ. Equivalently, (d+1)Σ_D κ ≤ d(M − m + 1).

**Lemma GW-1 (Apéry form for any element; PROVED).**
- Statement: let T be a numerical semigroup, 0 ≠ t ∈ T, and d ≥ e(T) − 1. Then (d+1)ℓ(T) ≥ c(T) holds iff
  dt·max Ap(T,t) − (d+1)ΣAp(T,t) ≥ (d−1)t(t−1)/2.
- Proof:
  - Selmer: F(T) = max Ap(T,t) − t and g(T) = ΣAp(T,t)/t − (t−1)/2.
  - Then (d+1)(c − g) ≥ c ⟺ dc ≥ (d+1)g. Substitute c = F + 1. □
- Wilf with e(T) implies the d+1 form for d + 1 ≥ e(T).

**Lemma GW-2 (GW ⟹ Wilf; PROVED).**
- Let S ≠ ℕ have multiplicity m and other minimal generators n_1, …, n_d, with d = e − 1. Fix a term order refining
  the weight n.
- The standard monomials of the residue map form a down-set D ⊂ ℕ^d.
  - They are the minimal factorization of each Apéry element: a divisor of a minimal monomial is minimal.
  - |D| = m, v(D) = Ap(S, m), and residues are bijective.
- By GW-1 with t = m, GW(D, n) is Wilf(S).
- It also covers Ap(T, t) for any element t, in particular the largest generator, where every n_a < t. □

**Lemma GW-3 (reformulations; PROVED).**
- Put Δ = v(D) + mℕ for n > 0. Then:
  - the gaps of Δ in the class of x are v(x) − jm for 1 ≤ j ≤ κ(x), so g(Δ) = Σκ;
  - c(Δ) = M − m + 1;
  - ℓ(Δ) = #{δ ∈ Δ : δ < c} = Σλ, because v(x) + jm ≤ M − m ⟺ j ≤ λ(x) − 1;
  - κ(x) + λ(x) = ⌊M/m⌋ − [v(x) mod m > M mod m], so g + ℓ = c.
- Since Σ_D (v mod m) = m(m−1)/2, Σv = mΣκ + m(m−1)/2.
- Hence B − τ = m[d(M − m + 1) − (d+1)Σκ], and
  GW ⟺ (d+1)ℓ(Δ) ≥ c(Δ) ⟺ dℓ(Δ) ≥ g(Δ). □

**Lemma GW-4 (column form; PROVED).**
- B(D,n) = Σ_{x∈D} Σ_a u(top_a x), with u = M − v and top_a x the top of the a-column through x.
- Proof: Σ_x v(top_a x) = Σ_D v + n_a Σ_D x_a. Sum over a and use dmM = Σ_{(x,a)} M. □

**Proposition GW-5 (boxes; PROVED; injectivity suffices).**
- Statement: if D = ∏_a [0, L_a) and v is injective on D, then B(D,n) = (d−1)mM/2 ≥ τ.
- Proof:
  - u(top_a x) = Σ_{b≠a} n_b(L_b − 1 − x_b), so Σ_a u(top_a x) = (d−1)u(x).
  - The reflection x ↦ L − 1 − x gives Σu = mM/2. Apply GW-4.
  - Injectivity gives M ≥ m − 1. □
- For boxes, Δ is symmetric: ℓ = g.

**Remark GW-6 (the hypotheses are needed).**
- Injectivity alone does not suffice for non-boxes. With d = 2, D = {(0,0),(0,1),(0,2),(1,0)}, n = (3,2):
  v(D) = {0,2,4,3} and B = 5 < τ = 6.
- So the complete residue system (the tiling D + Λ = ℤ^d) is essential.

**Remark GW-7 (GW is stronger than Wilf for the same weights).**
- Take d = 3, m = 10, n = (19,17,12), and D = {0, e3, e2, 2e2, 3e2, e1, e1+e2, e1+2e2, 2e1, 2e1+e2}.
- Residues are complete and d(M−m+1) − (d+1)Σκ = 165 − 108 − 27 = 30. The Apéry tile of ⟨10,12,17,19⟩ gives 46.
- So GW for non-minimal D is not a consequence of Wilf for ⟨m, n⟩.

**Status.** GW holds in every exhaustive range tested, including signed n (EXPERIMENTS E164–E168). It is OPEN in
general. The e = 2 case is GW with d = 1, where D = {0..m−1} and equality always holds.

### GW: corner reflection and dimension two — PROVED

Notation as in "Down-set Wilf (GW)", with n > 0. Put:
- U_i = {x ∈ D : κ(x) ≥ i} (up-sets of D);
- L_i = {x ∈ D : λ(x) ≥ i} = {x : v(x) ≤ M − im} (down-sets);
- t_i = #{maximal y ∈ D : κ(y) ≥ i} and t(D) = #maximal elements.

By GW-3, g(Δ) = Σ_{i≥1}|U_i| and ℓ(Δ) = Σ_{i≥1}|L_i|.

**Theorem GW-8 (corner reflection).** For every i ≥ 1, |U_i| ≤ t_i·|L_i|. Hence g ≤ Σ_i t_i|L_i| ≤ t(D)·ℓ.
- Proof:
  - Let x ∈ U_i and let y be a maximal element of D with y ≥ x. Then y ∈ U_i, because U_i is an up-set.
  - y − x ∈ D, since D is a down-set, and v(y − x) = v(y) − v(x) ≤ M − im. So y − x ∈ L_i.
  - For fixed y, the map x ↦ y − x is injective.
  - Choosing one such y for each x gives an injection U_i → {maximal y with κ(y) ≥ i} × L_i. □
- Exactness: for each maximal y, the map is a bijection {x ≤ y : κ(x) ≥ i} → {w ≤ y : v(w) ≤ v(y) − im}, with inverse
  w ↦ y − w.
- In gap language, the gap v(x) − im is sent to the element v(y) − m − (v(x) − im) of Δ below c, a reflection through
  (v(y) − m)/2.
- For a minimal tile the maximal cells are the maximal Apéry elements, so t(D) = type(S). The theorem is then
  Fröberg–Gottlieb–Häggkvist's g ≤ t·ℓ, here valid for every residue-complete down-set.

**Corollary GW-9.** GW holds whenever Σ_i t_i|L_i| ≤ d·Σ_i|L_i|, in particular whenever t(D) ≤ d. (GW ⟺ g ≤ dℓ.)

**Lemma GW-10 (two corners in dimension two).** Let D ⊂ ℕ² be a finite down-set with |D| = m, and let s ∈ ℤ² be such
that x ↦ x·s mod m is bijective on D. Then D has at most two maximal elements.
- Setup:
  - Write row j (0 ≤ j < N) as {(i,j) : i < λ_j}, with λ_0 ≥ … ≥ λ_{N−1} ≥ 1. The number of maximal elements is the
    number of distinct λ_j.
  - Put g = gcd(s_1, m) and A = m/g. Bijectivity forces gcd(s_1, s_2, m) = 1, so s_2 is a unit mod g.
- Fibres:
  - Modulo g the residue of (i,j) is j·s_2. So the rows with j ≡ c (mod g) carry exactly the A residues of the coset
    C_c = c·s_2 + gℤ/mℤ.
  - C_c is one cycle of r ↦ r + s_1. Identify it with ℤ/A by c·s_2 + gt ↦ t·u, where u = (s_1/g)^{−1} mod A; adding s_1
    becomes adding 1.
  - Row j = c + gi then occupies the arc [iβ, iβ + λ_j) with β = s_2·u mod A.
  - These arcs partition ℤ/A. So λ_{c+gi} is the gap after the point iβ in the cyclic order of
    P_c = {iβ : 0 ≤ i < N_c}, whose points are distinct.
- Three-distance theorem (Sós, Świerczkowski; indexed form):
  - If N_c ≥ 2, there are 1 ≤ a, b < N_c with a + b ≥ N_c such that the gap after iβ is
    - G_1 for i < N_c − a,
    - G_1 + G_2 for N_c − a ≤ i < b,
    - G_2 for i ≥ b,
    with G_1, G_2 > 0.
  - λ_{c+gi} is non-increasing in i and the first range is nonempty, so the middle range is empty.
  - Hence each fibre's gap sequence takes at most two values and depends only on (A, β, N_c).
- Two fibre sizes cannot coexist:
  - Write N = gq + r with 0 ≤ r < g. Every coset contains a cell, so q ≥ 1. N_c = q + 1 for c < r and N_c = q
    otherwise.
  - Suppose 0 < r. P_{c'} has q points for c' ≥ r, and P_c = P_{c'} ∪ {qβ} for c < r.
  - The new point splits exactly one gap, the one after i_0β, into strictly shorter gaps; all other gaps are unchanged.
  - Then for c < r ≤ c', λ_{c+gi_0} < λ_{c'+gi_0} although c + gi_0 < c' + gi_0. This contradicts monotonicity.
- Conclusion: r = 0. All fibres have the same two-valued gap sequence G(i), and λ_{c+gi} = G(i). □

**Theorem GW-11 (Down-set Wilf in dimension ≤ 2).** GW holds for d ≤ 2 and every n > 0.
- For d = 1, t = 1. For d = 2, t(D) ≤ 2 by GW-10. Apply GW-9. A down-set using fewer directions is covered by the
  smaller d, because d/(d+1) increases with d. □
- This contains Wilf for e ≤ 3 (FGH 1987). It adds every non-minimal residue-bijective L-shape, including those for
  generators below m (Apéry sets of the largest generator) and arbitrary lifts.

**Limits of the reflection method (EXPERIMENTS E171–E176).**
- For d ≥ 3, t(D) is unbounded (in 3-D, t = 4, 5 already for m = 7–12).
- The reflection graph alone needs capacity > d at δ = 0 whenever more than d corners have κ ≥ 1. Every corner's own
  gap v(y) − m reflects only to 0.
- GW-9 covers about half of the t > d instances for d = 3.

### Prefix (window) Wilf — PGW: CONJECTURE; the case t ≤ d, the low depths and P_1 are PROVED

Notation as in GW-8. For i ≥ 1 put

    (P_i)   Σ_{j=1}^{i} |U_j|  ≤  d · Σ_{j=1}^{i} |L_j|,   equivalently   Σ_{x∈D} min(i, κ(x)) ≤ d · Σ_{x∈D} min(i, λ(x)).

- For i ≥ max_x max(κ(x), λ(x)) this is g ≤ dℓ, i.e. GW. So the family runs from P_1 to GW.
- **Semigroup form.** On the minimal tile of S (multiplicity m, d = e − 1), with c the conductor:
  - Σ_x min(i, κ(x)) = #(gaps of S below im). The gaps of class r are r, r + m, …, w_r − m, and min(i, κ) of them lie
    below im.
  - Σ_x min(i, λ(x)) = #(S ∩ [c − im, c)) = |Ap(S, im) ∩ [0, c)|. The elements of class r below c are
    w_r, …, w_r + (λ−1)m, the last one in [c − m, c), so the top min(i, λ) of them lie in [c − im, c).
  - So P_i reads

        (WW_i)   #((ℕ∖S) ∩ [0, im))  ≤  (e − 1) · #(S ∩ [c − im, c)).

  - WW_i is FALSE for windows N that are not multiples of m: ⟨3,7,8⟩ has c = 6, gaps 1, 2, 4, 5; for N = 5 the left side
    is 3 and the right side is 2·#{3} = 2 (E189).
- **Matching form.** P_i holds for every i ⟺ the gaps (x, j), 1 ≤ j ≤ κ(x), can be assigned to the elements (w, h),
  1 ≤ h ≤ λ(w), with h ≤ j and every element used at most d times. (The neighbourhoods are nested in j, so Hall's
  condition reduces to the prefix inequalities.)
- **What P_i is not.**
  - The per-depth inequalities |U_j| ≤ d|L_j| are false (E183), and so is the suffix family (E187).
  - The increments |U_j| − d|L_j| are not single-crossing (E190), so P_i is not a formal consequence of GW by that route.
- **Evidence.**
  - Down-sets: 0 failures in 5,860,736,208 instances (d = 3, m ≤ 30; d = 4, m ≤ 20; d = 5, m ≤ 14; k ∈ {0,1,2}^d; E188).
  - Semigroups: WW_i for every i on all 280,235,190 semigroups of genus ≤ 36 (E189).
  - Tight cases: e = 2 (every i, by the symmetry z ↔ F − z) and maximal embedding dimension (e.g. ⟨3,8,10⟩ at i = 2).

**Theorem GW-12.** If t(D) ≤ d then P_i holds for every i. More precisely Σ_{j≤i}|U_j| ≤ Σ_{j≤i} t_j|L_j|.
- Proof: GW-8 is depth-preserving (|U_j| ≤ t_j|L_j| for each j). Sum over j ≤ i. □

**Lemma GW-13 (descent map).** Let j ≥ 1 and suppose n_a ≥ jm for every a. Then |U_j| ≤ d·|L_j|.
- Proof:
  - Let x ∈ U_j. Then x ≠ 0, because v(0) = 0 < jm. Choose a with x_a > 0 (say the least) and put φ(x) = x − e_a ∈ D.
  - φ(x) + e_a = x ∈ D, so v(φ(x)) = v(x) − n_a ≤ M − n_a ≤ M − jm. Hence φ(x) ∈ L_j.
  - Each w ∈ D has at most d preimages w + e_a. □
- No positivity of n is needed beyond n_a ≥ jm.

**Corollary GW-14.** Put k_min = min_a ⌊n_a/m⌋. Then

    g ≤ d · Σ_{j ≤ k_min} |L_j| + Σ_{j > k_min} t_j |L_j|.

- So GW holds whenever at most d maximal cells have κ > k_min. This strengthens GW-9, which needs t_j ≤ d at every
  depth j.
- P_i holds for every i ≤ k_min. In the multiplicity form (every k_a ≥ 1), P_1 holds.

**Corollary GW-15 (semigroups; elementary, probably known in some form — not claimed new).** Let S ≠ ℕ have
multiplicity m, embedding dimension e and type t. Then:
1. (e − 1)·|Ap(S, m) ∩ [0, c)| ≥ m − 1. This is WW_1.
   - Equivalently (e − 1)·#((ℕ∖S) ∩ [c − m, c)) ≤ (e − 2)m + 1. Every gap in [c − m, c) is pseudo-Frobenius.
2. (e − 1)·t ≤ (e − 2)m + 1, i.e. t ≤ m − (m − 1)/(e − 1). This is equality for maximal embedding dimension.
- Direct proof of 1:
  - Every nonzero w ∈ Ap(S, m) is w' + n with n a minimal generator other than m, and w' ∈ S. (m is not used, because
    w − m ∉ S.)
  - w' ∈ Ap(S, m): if w' − m ∈ S then w − m = (w' − m) + n ∈ S.
  - w' < c: w' + n = w ≤ F + m and n > m give w' < F.
  - Each w' arises from at most e − 1 values of n.
- Proof of 2, the corner bound:
  - For every finite nonempty down-set D ⊂ ℕ^d, the map φ of GW-13 sends D∖{0} into the non-maximal cells, at most d to
    one. So |D| − 1 ≤ d(|D| − t(D)), i.e. d·t(D) ≤ (d − 1)|D| + 1.
  - For the minimal tile, Max_{≤S} Ap(S, m) ⊂ v(Max D), since x + e_a ∈ D gives v(x) + n_a ∈ Ap. So t ≤ t(D).

**Theorem GW-16 (P_2 in the multiplicity form; no residue hypothesis) — KERNEL-CHECKED (Lean, `Window2.depth_two`).**
Let D ⊂ ℕ^d be a finite nonempty down-set (D = ∅ is the trivial 0 ≤ 0 under ℕ conventions), m = |D|,
and n ∈ ℤ^d with n_a > m for every a such that e_a ∈ D. Put v = x·n, M = max_D v, κ = ⌊v/m⌋, λ = ⌊(M − v)/m⌋. Then

    Σ_{x∈D} min(2, κ(x))  ≤  d · Σ_{x∈D} min(2, λ(x)).

- Notation:
  - Max = maximal cells of D, NonMax = D ∖ Max, A = {a : e_a ∈ D, n_a < 2m}.
  - T = {w ∈ NonMax : every upper cover w + e_a ∈ D is maximal and has a ∈ A}, and N = NonMax ∖ T.
  - Y = {y ∈ Max, y ≠ 0 : y − e_a ∈ T for every a with y_a > 0}.
- Step 1 (left side = 2(m − 1) − |A|).
  - κ(0) = 0, and κ(x) ≥ 1 for x ≠ 0 since v(x) ≥ n_a > m.
  - If |x|_1 ≥ 2 then x ≥ e_a + e_b for some a, b, so v(x) ≥ n_a + n_b > 2m and κ(x) ≥ 2.
  - For e_a ∈ D: κ(e_a) ≥ 2 iff a ∉ A. (The qualification e_a ∈ D is needed; Lean audit, `inactive_unit_counterexample`.)
- Step 2 (right side ≥ d(2|NonMax| − |T|)).
  - If w + e_a ∈ D then v(w) ≤ M − n_a < M − m, so λ(w) ≥ 1 on NonMax.
  - Let w ∈ N. Either some w + e_a ∈ D has a ∉ A, so v(w) ≤ M − n_a ≤ M − 2m. Or some w + e_a ∈ D is non-maximal,
    w + e_a + e_b ∈ D, so v(w) ≤ M − n_a − n_b < M − 2m. Either way λ(w) ≥ 2.
- Step 3 (reduction). By Steps 1–2 it suffices that d|T| − |A| ≤ 2(d|NonMax| − (m − 1)).
- Step 4 (descent avoiding T).
  - For each x ≠ 0 choose a lower cover φ(x) = x − e_a (x_a > 0), taking one outside T whenever possible.
  - Lower covers are non-maximal, and φ(x) = w forces x = w + e_a. So φ: D∖{0} → NonMax with |φ⁻¹(w)| ≤ d.
  - φ(x) ∈ T only if x ∈ Y:
    - if x is non-maximal, each lower cover has the non-maximal upper cover x, so it is not in T;
    - if x is maximal and x ∉ Y, some lower cover lies outside T.
  - Hence
    d|NonMax| − (m − 1) = Σ_{w∈NonMax}(d − |φ⁻¹(w)|) ≥ Σ_{w∈T}(d − |φ⁻¹(w)|) ≥ d|T| − |Y|.
  - So Step 3 follows from 2|Y| ≤ d|T| + |A|.
- Step 5 (counting Y).
  - (y, a) ↦ (y − e_a, a), for y ∈ Y and y_a > 0, is injective into {(w, a) : w ∈ T, w + e_a ∈ D}, and for w ∈ T these a
    lie in A. So Σ_{y∈Y} |supp y| ≤ |A|·|T|.
  - Let Y_1 = {y ∈ Y : |supp y| = 1}. Each is y = k e_a, and (k − 1)e_a ∈ T has the upper cover y in direction a, so
    a ∈ A. A maximal cell on the a-axis is unique, so |Y_1| ≤ |A|.
  - Therefore 2|Y| ≤ Σ_{y∈Y}|supp y| + |Y_1| ≤ |A|·|T| + |A| ≤ d|T| + |A|. □
- Residues are not used. Residues ARE needed from depth 3 on.
  - Without them P_3 fails: d = 2, D = {x : |x|_1 ≤ 2}, m = 6, n = (9,9). There Σ min(3, κ) = 11 > 2·5 (E191).
  - With residue completeness P_3 has no counterexample in E188.
- Checks (E191):
  - The counting lemma of Step 5 on every down-set and every A ⊂ [d]: d = 2 (m ≤ 9), d = 3 (m ≤ 9), d = 4 (m ≤ 8).
  - P_2 on every (D, n) with n_a ∈ (m, Km], no residue condition: 0 failures.

**Corollary GW-17 (window Wilf at depth 2) — KERNEL-CHECKED (Lean, `Window2.semigroup_depth_two`, library definitions).** For every numerical semigroup S with multiplicity m, embedding dimension e
and conductor c:

    #((ℕ∖S) ∩ [0, 2m))  ≤  (e − 1) · #(S ∩ [c − 2m, c)).

- Proof: apply GW-16 to the minimal (lex-largest factorization) tile of Ap(S, m) in ℕ^{e−1}. It is a down-set with
  v(D) = Ap(S, m) and n_a the generators other than m, all > m. Then use the semigroup form of P_i above.
- For c ≤ 2m both windows are everything, and this is Wilf: Kaplan's theorem (c ≤ 2m) is the special case.
- Lean (lean/Wilf/Window2.lean, codex audit lean/WINDOW2_REPORT.md):
  - Both statements were checked exactly as above; `depth_two_of_le` also allows n_a ≥ m.
  - Only the standard axioms [propext, Classical.choice, Quot.sound] are used, with no sorry.
  - The lead rebuilt the file on fejer and printed its axioms.
  - The audit's only substantive remark is the e_a ∈ D qualification in Step 1.
- Literature (item 20): no statement of the window inequality was found. Not claimed new until checked against Kaplan's
  paper and its citations.

**Lemma GW-PF (per-depth FGH with pseudo-Frobenius numbers; elementary).** Let S be a numerical semigroup with
multiplicity m, Kunz coordinates κ_r and λ_r = #{elements of class r below c}. Put U_j = {r : κ_r ≥ j} and
L_j = {r : λ_r ≥ j}. Then for every j ≥ 1:

    |U_j| ≤ #{f ∈ PF(S) : f ≥ (j − 1)m} · |L_j|.

- Proof:
  - Let r ∈ U_j, with Apéry element w_r, and z = w_r − jm, a gap.
  - Choose w_f maximal in (Ap(S, m), ≤_S) with w_r ≤_S w_f. Then f = w_f − m ∈ PF and w_f ≥ w_r > jm.
  - s := f − z = (w_f − w_r) + (j − 1)m. Here w_f − w_r ∈ Ap(S, m), since (w_f − w_r) − m ∈ S would give w_f − m ∈ S.
    So s is the j-th element of its class, and s ≤ f < c. Hence class(s) ∈ L_j.
  - For fixed f the map r ↦ class(w_f − w_r) is injective. □
- This is FGH's g ≤ tℓ refined by depth: only PF numbers ≥ (j − 1)m serve depth j.
- Check: 0 violations on all 712,373 semigroups of genus ≤ 24 (E195).

**Corollary GW-18 (a new sufficient condition for Wilf).** If at most e − 1 pseudo-Frobenius numbers of S are ≥ 2m,
then S satisfies Wilf's conjecture.
- Proof: g = Σ_j|U_j| ≤ (e−1)(|L_1| + |L_2|) + Σ_{j≥3} #{f ≥ (j−1)m}·|L_j| ≤ (e−1)Σ_j|L_j| = (e−1)ℓ. The first two
  depths use GW-17. The rest use GW-PF with #{f ≥ (j−1)m} ≤ #{f ≥ 2m} ≤ e − 1. And g ≤ (e−1)ℓ is Wilf. □
- Likewise (from GW-14): Wilf holds if at most e − 1 PF numbers are ≥ m.
- In general: once P_i is proved, Wilf holds whenever at most e − 1 PF numbers are ≥ im.
- Coverage (E195), genus ≤ 24:
  - classical t ≤ e − 1: 95.16%;
  - #PF ≥ m ≤ e − 1: 97.16%;
  - **GW-18: 99.86%**;
  - with P_3 (now GW-20): all but 32 of 712,373.
- Literature (2026-10-19): the known statement is e > t ⇒ Wilf (FGH). Marashdeh's reduction (2608.12531, Prop 5.1)
  involves the smallest t + 1 − e PF numbers and is a different mechanism. No statement of GW-18 was found. Novelty
  is UNVERIFIED beyond this search.

**Theorem GW-21 (P_4: partial; PROVED on paper 2026-10-19 by codex P4; every step re-checked by the lead, the
identities (4), (5) and the EF expansion verified by exact polynomial arithmetic, src/scratch/gw/p4/lead_identity_check.py).**
Same hypotheses as GW-19, with the target P_4: Σ min(4, κ) ≤ d Σ min(4, λ). Full proofs are in
src/scratch/gw/p4/P4_REPORT.md.
- **(H4) Residue-free, sharp.** For any scale q ≥ 1, any finite down-set, n_a > q on active directions and
  M ≥ 6q − 1: Σ min(4, ⌊v/q⌋) ≤ d Σ min(4, ⌊(M−v)/q⌋).
  - Proof as Theorem H. The deficits are the mixed quadratics (floors 1+1 → 3, 1+2 → 4) and the mixed cubics
    (B = 3, F(v) = 4), each of size 1.
  - Each deficit x chooses b = its largest-weight direction and the column (b, x with x_b zeroed). These columns are
    distinct.
  - Payment: either the cell z + j*e_b has surplus (table in P4_REPORT §7), or the column ends below j* and has
    slack ≥ 1.
  - Sharp: the degree-4 simplex in ℕ³ with q = m = 35 and n = (52,52,52) has M = 6q − 2 and 115 > 114.
- **(Band identity, primary regime 4m ≤ M < 5m.)**
  - Put ρ = 5m − 1 − M. The classes A, B, C, E are the bands of n_a. The types are those of the E200 table, with
    AAB split by the band of its AA divisor.
  - Exact identity W = dℓ − g = W_A + T + R, with T, R ≥ 0 explicit, where
    W_A = 3a(a+1) + (2a−2)q₂ + (a−3)(q₃+u₃) − 4(u₄+k).
  - Ingredients: weighted shadows, monomial capacities, and the joint short-residue lemma
    t₃ + BC + AAB₃ + ABB + BBB ≤ ρ (five families with residues in one cyclic interval of length ρ).
  - Also 3W_A = 18(Q − q₂ − q₃) − (a−1)q₃ + 4D₃ + 2D_low + 3D₄ with D_* ≥ 0 (shadow defects). So P_4 holds whenever
    18(Q − q₂ − q₃) ≥ (a−1)q₃.
- **(Signed B₃ packing.)** If an a-direction face contains every monomial of degree ≤ 3 (residue injective), then
  m ≥ C(a+3,3) + 2C(a+1,3).
  - Proof: the residues p + q − r, with p, q ∈ B₀ ∖ {r} and B₀ = {0, s_1, …, s_a}, are distinct and avoid B₀.
  - Quantitative form: m ≥ s(s(s−1)/2 + 1) − J_s r(r+1)/2, where r = the triple-collision excess and
    J_s = min(9, ⌊s²/4⌋).
  - Corollary: no residue-complete down-set is a full cubic simplex, nor a full cubic simplex minus one cubic.
- **(Primary regime, a ≤ 3: PROVED.)** a = #{a : n_a < 2m − ρ}.
  - For a ≤ 1, W_A ≥ 0.
  - For a = 2 or 3, W_A < 0 forces the face to be the full cubic simplex with every AA in I₃ and every AAA in I₄.
    W < 0 would then force T + R ≤ 3 (resp. = 0), which makes D a full cubic simplex minus ≤ 1 cubic.
    The packing corollary excludes this.
- **(Saturated EF face, any a, ρ = 0: PROVED.)** The packing gives d − a > (a−1)/3. Then
  W − W_A ≥ (d−a)·a(a+1)/2 > C(a+1,3) = −W_A.
- **(Quadratic down-sets: PROVED for every M.)**
- **Semigroup corollaries.**
  - **Wilf holds for every S with 3m < c ≤ 4m that has at most 3 minimal generators in (m, c − 2m).** Here
    2m − ρ = c − 2m. Genus ≤ 28: this covers 640,993 of the 642,239 such S.
  - Via H4 and GW-PF: Wilf holds if c ≥ 5m and at most e − 1 PF numbers are ≥ 4m.
- **OPEN (precise).**
  - RC4: (a−1)q₃ ≤ 18(Q − q₂ − q₃) + 4D₃ + 2D_low + 3D₄ + 3T + 3R for a ≥ 4. This is equivalent to the primary
    regime.
  - The window 5m ≤ M ≤ 6m − 2 when cubic cells are present.

**Conjecture H_i (uniform residue-free window theorem).** For every i ≥ 2, any scale q ≥ 1, any finite down-set
D ⊂ ℕ^d, and n_a > q on active directions: if M ≥ (2i−2)q − 1, then

    Σ_D min(i, ⌊v/q⌋) ≤ d Σ_D min(i, ⌊(M−v)/q⌋).

- PROVED: i = 2 (GW-16, all M), i = 3 (Theorem H), i = 4 (H4). The cutoff is sharp for i = 3, 4.
- Simplex evidence (E208): over full simplices {|x| ≤ t} ⊂ ℕ^k (k ≤ 8, t ≤ 13) with equal weights n ∈ (q, 3q],
  q ≤ 60, the failures have sup (M+1)/q equal to 2i − 2 for i = 3, 4, 5, 6. The extremal shape is n = 2q − 1 with
  degree ≈ i − 1. For i = 7, 8 the searched range only reaches 10 and 12.
- Exhaustive residue-free check (E208): no failure for d = 2, m ≤ 14, q ≤ 9, n ≤ 3q, i = 3, 4, 5. Larger runs are
  in progress.
- Conditional consequence (with GW-PF): Wilf holds whenever at most e − 1 PF numbers are ≥ i·m, with i = ⌊(K+2)/2⌋
  (K = ⌊maxAp/m⌋). That is FGH's type condition restricted to the upper half, uniformly in K. Its residual class is
  concentrated at K = 4, 5 (E206).
- Proof pattern (H, H4): each deficit (mixed carried cell of degree < i) picks b = its largest-weight direction and
  is paid by the first surplus cell up its b-column, or by that column's slack when the column ends early. M ≥
  (2i−2)q − 1 is exactly what makes the early-ending column have δ = M − v(top) ≥ q. For i ≥ 6 deficits can be ≥ 2,
  and a general-i payment table is needed.

**Reduction GW-22 (H_i ⟸ a one-dimensional per-column inequality; PROVED 2026-10-19).**
Setting:
- Scale q, truncation F(t) = min(i, ⌊t/q⌋), down-set D, n_a > q on active directions.
- For x ≠ 0 let b(x) be its largest-weight support direction (ties by index).
- x lies in exactly one *dominant column* C = (b, z) at index x_b ≥ 1. Here z is x with the b-coordinate zeroed,
  and every direction of supp(z) has weight ≤ n_b.

Write w = n_b, u = v(z), β = Σ_a F(z_a n_a), J = top index of C, δ = M − u − Jw ≥ 0. The *per-column inequality* is

    (PCI)   Σ_{j=1}^{J} F(u + jw) ≤ Jβ + Σ_{j=0}^{J} F(M − u − jw)
            ⟺ Σ_{j=1}^{J} [F(u + jw) − F(δ + jw)] ≤ Jβ + F(δ)
            ⟺ Σ_{k=1}^{i} #{1 ≤ j ≤ J : jw ∈ [kq − u, kq − δ)} ≤ Jβ + F(δ).

If PCI holds for every dominant column, then P_i holds at scale q.
- Proof:
  - By (H1), P_i ⟺ Σ_x [F(v(x)) − B(x)] ≤ Σ_{all columns} s(C).
  - Group the left side by dominant columns; B(z + j e_b) = B(z) + F(jw).
  - Drop the slack of non-dominant columns, which is ≥ 0 by reflection.
  - The F(jw) terms cancel and leave PCI. □

PCI for long columns, J ≥ i (PROVED, no cutoff needed):
- If β ≥ i, the left side is ≤ Ji ≤ Jβ.
- Otherwise every z_a < i, so β ≥ |z| =: s, and dominance gives u ≤ s·w.
- Each window [kq − u, kq − δ) then contains at most ⌈(u − δ)/w⌉ ≤ s multiples of w.
- So the left side is ≤ i·s ≤ Jβ. □

Status:
- H_i ⟸ PCI for short dominant columns (1 ≤ J ≤ i − 1) under M ≥ (2i−2)q − 1.
- Checked exhaustively (E209): q ≤ 14, n_b ∈ (q, 3q], bases with ≤ 3 components, i = 3, 4, 5, 6 at the cutoff
  (2i−2)q − 1. That is 1.0e8 cases, 0 failures.
- Dominance is NECESSARY: without it PCI fails, e.g. i = 3, q = 6, n_b = 8 with base component 11.
- Tight cases have one component equal to w, with J = i − 1 or i (e.g. i = 5, q = 4, w = 7, u = 7, J = 4).

**Theorem GW-23 (PCI for light columns, w ≤ 2q − 1; PROVED 2026-10-19).**
Hypotheses:
- Integers q ≥ 1, i ≥ 1, q < w ≤ 2q − 1, β ≥ 1, J ≥ 1, 0 ≤ u ≤ βw, δ ≥ 0, M = u + Jw + δ ≥ (2i−2)q − 1.
- F(t) = min(i, ⌊t/q⌋).

Then

    Σ_{j=1}^{J} [F(u + jw) − F(δ + jw)] ≤ Jβ        (no F(δ) term needed).

In particular PCI (GW-22) holds for every dominant column with n_b ≤ 2q − 1.
- Indeed u = v(z) = Σ z_a n_a ≤ (Σ z_a)·w ≤ βw by dominance, when β < i (else PCI is trivial).

Proof:
1. LHS = Σ_{k=1}^{i} c_k with c_k = #{j ∈ [1,J] : kq − u ≤ jw < kq − δ}.
   - Put a_k = ⌈(kq − δ)/w⌉. From u ≤ βw, every such j lies in [a_k − β, a_k − 1].
   - So c_k ≤ φ(a_k), where φ(a) = |[a − β, a − 1] ∩ [1, J]|.
   - φ is a trapezoid supported on [2, J + β], symmetric under a ↦ a* = J + β + 2 − a, with Σ_a φ(a) = Jβ.
2. Put m_a = #{k ≤ i : a_k = a}, the multiples of q in ((a−1)w + δ, aw + δ].
   - Since w < 2q, m_a ≤ 2. And m_a = 0 for a > A := a_i.
   - LHS ≤ Σ_a m_a φ(a). With R = J + β + 1 − A, the reflection maps [1, R] onto [A + 1, J + β + 1].
   - So Σ_{a>A} φ = Σ_{a≤R} φ, and LHS − Jβ ≤ Σ_{a ∈ (R, A]} (m_a − 1) φ(a).
   - This sum runs over the "middle region" (R, A], which is symmetric about a = (J + β + 2)/2, so φ is constant on it.
3. The middle region has length Λ = 2A − J − β − 1 < (2q + 1 − δ)/w + 1 < 3.
   - This uses A < (iq − δ)/w + 1 and (J + β)w ≥ T − δ.
   - Let X = ⌊(Rw + δ)/q⌋. The region holds i − X of the k's.
   - Λ = 1: i ≥ X + 2 together with 2Rw ≥ (2i−2)q − 1 − δ forces Rw + δ ≡ ρ (mod q) with 2ρ ≥ 2q − 1 + δ, impossible.
   - Λ = 2: (2R+1)w ≥ (2i−2)q − 1 − δ gives 2i − 2 ≤ 2X + (2ρ + w − δ + 1)/q < 2X + 4, so i ≤ X + 2.
   - Either way Σ_{mid}(m_a − 1)φ ≤ 0. □

Corollary GW-23c:
- P_i holds at scale q for every down-set (no residue hypothesis) all of whose active weights lie in (q, 2q), whenever
  M ≥ (2i−2)q − 1.
- Via GW-22 + GW-23. For example, on every A-face of the P_4 analysis (n_a < 2m − ρ) at every i.

**PCI fails for heavy columns (w ≥ 2q) when i ≥ 10 (E211).**
- Smallest found: i = 10, q = 9, w = 22, three base components of weight 17 = 2q − 1 (β = 3, u = 51), J = 5, M = 161 = T.
  Here LHS = 16 > Jβ + F(δ) = 15.
- Realizable as a dominant column. P_i itself holds on these instances, e.g. the box [0,1]³×[0,7] with weights
  (39,39,39,46), q = 20, i = 12 gives 562 ≤ 2248.
- So H_i for heavy weights needs the non-dominant column slack that GW-22 discards.
- For i ≤ 9, PCI holds for all w in the scanned range (E211).
- The row-pairing bound term_j + term_{J+1−j} ≤ 2β (w ≥ 2q) holds for i ≤ 8, q ≤ 12. It FAILS at i = 12: q = 20, w = 46,
  β = 3, u = 117, J = 7, j = 3 gives S = 7.

**Theorem GW-24 (P_4 primary regime for a ≤ 6; distinct-weight H4; packing lemmas. a ≤ 5 PROVED on paper,
a = 6 PROVED with two finite certificates; 2026-10-19, codex P4 §§12–19, every step re-checked by the lead; both a = 6
certificates and the a = 7 subcase re-implemented independently by the lead, src/scratch/gw/p4/lead/).**
Notation of GW-21 (bands I_j = [jm−ρ, (j+1)m−ρ), classes A, B, C, E, cell types q₂ … k, W = W_A + T + R).
Full proofs: src/scratch/gw/p4/P4_REPORT.md §§12–19.
- **Packing lemmas** (B₀ = {0, s_1, …, s_{s−1}} with injective unordered-pair residues; r = triple-collision excess;
  H_{s−1} = s(s(s−1)/2 + 1)).
  - (Linear, omitted family) If the represented triples and the omitted triples each have distinct residues, then
    m ≥ H_{s−1} − Σ_{omitted x} |supp x|·min(3, s − |supp x|). Holds when the omitted triples pairwise share a variable.
  - (LP) 2m ≥ 2H_{s−1} − 3s·r. (SP) m ≥ H_{s−1} − L_s r with L_s = 3s/2 (3 | s), 3(s−1)/2 otherwise (s ≥ 5); 1, 2, 4
    for s = 2, 3, 4. L_s is the exact max of Σ_{i<j} t_it_j/(g−1) over support partitions (checked s ≤ 100).
  - (HP, s = 3k ≥ 6) A fiber of k disjoint squarefree triples covering B₀ has residue R with kR ≡ Σ B₀ (mod m), so there
    are ≤ gcd(k, m) such fibers, and m ≥ H_{s−1} − (3s/2 − 3) r − 3(k−1) gcd(k, m).
  - Consequences: no residue-complete tile is (d ≥ 5) all quadratics + all but ≤ 4 cubics + ≤ 2 quartics, or (d ≥ 6)
    a full cubic simplex minus ≤ 6 cubics.
- **Uniform low-cost lemma (LC), any a ≥ 3.** For the low sub-ideal (degree counts q₂, u₃, k):
  (a+1)(q₂+u₃) − 4k ≥ min((a+1)q₂, C(a+1,3)). Proof: condensed Macaulay twice and the factorization
  ℓ_a(r) − F_a = (a−r)[r³ + 5r² + (5−a)r − a² + 1]/6 ≥ 0 on [a−2, a]. Consequence: W_A < 0 forces
  q₂ < a(a−1)/6 and 3(a+1)q₂ + (a+17)r_A < 3C(a+1,3).
- **AB-neighbor loss (any a).** If all AA are present, a B direction missing p_j ≥ 1 of its I₃ A-neighbors costs
  ≥ p_j(4a+3−3p_j)/2 ≥ 2a in p + D_v.
- **Primary regime, a = 4, 5: PROVED (paper).** W_A < 0 leaves 6 (a = 4) resp. 22 (a = 5) Macaulay profiles. In each,
  W < 0 forces c = e = 0 and an explicit near-simplex face, which the packing lemmas exclude (§§13, 16).
- **Primary regime, a = 6: PROVED (computer-assisted).** Analytic reductions:
  - W_A < 0 gives r_A ≤ 1, q₂ ≤ 4, c = e = 0. The one-missing-AA family reduces to one profile (A6.1): m = 74,
    ρ ∈ {0,1}.
  - For the full AA family, b ≥ 12 is excluded by packing polynomials 2d³ − 6d² − 118d − 74 > 0 and
    2d³ − 6d² − 115d + 40 > 0 (d ≥ 18).
  - Certificate 1 (A6.1 weights): the only lower-injective weight vector with ≥ 47 eligible cubics is
    t = (38,39,42,43,49,51) at ρ = 0 (omitted pair (1,4) or (2,3)). It leaves 18 residues uncovered.
  - Certificate 2 (count domain, b ≤ 11): 75 profiles and 36,389 count vectors. Exclusions: pure-A face 3,118; whole
    face (SP) 32,639; (HP) 65; deleted-endpoint face 564. The 3 survivors (b = 2, m = 148) are excluded on paper by a
    7-direction face with one missing cubic: m ≥ 221.5.
- **Distinct-weight H4.** If the active weights are pairwise distinct and > q and M ≥ 6q − 3, then P_4 holds at scale q
  with no residue hypothesis (the H4 table, with sharper early-column bounds). Hence the residue-complete P_4 holds
  for M ≥ 6m − 3.
- **a = 7 subcase (computer-assisted).** For b = c = e = 0, all AA present and q₂ = 0, W ≥ 0.
  (SP) and W < 0 leave m ∈ {107, 108}, and residue coverage fails in all 12 parameter sets (min 24 uncovered).
- **Semigroup corollary.** Wilf holds for every S with 3m < c ≤ 4m having at most 6 minimal generators in
  (m, c − 2m). On paper this holds for ≤ 5. (a = #{n_a < 2m − ρ} and 2m − ρ = c − 2m.)
- **OPEN.** Primary regime a ≥ 7 (the Macaulay profile list grows with a). Secondary window 5m ≤ M ≤ 6m − 4.

**Lemma GW-25a (arc lemma; PROVED 2026-10-19, elementary).** Let S be a numerical semigroup with multiplicity m,
conductor c and smallest generator n_1 > m. For k ≥ 1 let A_{≤k} = {w ∈ Ap(S,m) : w is 0 or a sum of at most k
minimal generators}. Then |A_{≤k}| ≥ min(m, (k+1)n_1 − c).
- Proof: each s ∈ [c, (k+1)n_1) lies in S, so s = w_r + jm with w_r ∈ Ap. Any factorization of w_r into generators
  ≠ m has length ≤ k, since a length-(k+1) sum is ≥ (k+1)n_1 > s ≥ w_r. An interval of length ≤ m meets distinct
  residues. □
- Consequence: if n_1 ≥ (c − m)/2 then c ≤ 3m + 2|A_{≤2}| (combine with k = 2), unless A_{≤2} = Ap.

**Theorem GW-25 (Wilf for the pure-A, upper-pair primary regime, every e; PROVED 2026-10-19 on paper).**
Hypotheses:
- 3m < c ≤ 4m;
- every minimal generator n ≠ m satisfies n < c − 2m (pure A);
- 2n_1 ≥ c − m.
Put a = e − 1 and p = #{w ∈ Ap : w is a sum of two minimal generators}. Then

    W(S) = e·ℓ − c ≥ a − 1 + 6(C(a+1,2) − p) ≥ e − 2,   and   h := c − 3m ≤ 2p + 2.

Proof.
1. Write n_i = m + t_i. Then t_i ∈ [L₀, h) with L₀ = n_1 − m ≥ h/2, and max Ap = c + m − 1 = 4m + h − 1.
2. Lengths are well defined and ≤ 3:
   - Every length-j sum is ≥ j(m + h/2), so j ≤ 3.
   - A pair has τ ∈ [h, 2h−2] and a triple has τ ∈ [3h/2, m+h−1] (value = jm + τ).
   - No element has factorizations of two lengths.
   - Let u = #{length 3}. Then m = 1 + a + p + u.
3. Write ρ = m − h. A residue ≥ h occurs only for pairs with τ < m (p_lo of them) and triples with τ < m (u_lo).
   Hence ρ = p_lo + u_lo. With g = a + 2p_lo + 3p_hi + 3u_lo + 4u_hi this gives
   g = c − 3a − p − 4, so ℓ = 3a + p + 4 and W = 3a² + 4a + 1 + (a−2)p − 3u − h (exact).
4. Arc bound h ≤ 2p + 2. The residues not attained by 0, units (τ ∈ [L₀, h)) or triples
   (τ ∈ [3L₀, m+h−1]) are:
   - [1, min(L₀, 3L₀−m)) ∪ [h, m) if 3L₀ ≥ m, of size ≥ 3L₀ − h − 1 or L₀ − 1 + m − h;
   - [h, 3L₀) otherwise.
   Either way there are ≥ h/2 − 1 of them, all occupied by pairs.
5. Cubic shadow (lex factorization tile): 3u ≤ (a+2)p.
6. Hence W ≥ 3a² + 4a − 1 − 6p = a − 1 + 6(C(a+1,2) − p). □
- Checked (E216): 35,907 random S in the class (m ≤ 120, a = 3..15). The arc bound, the W bound and the identity
  had 0 failures, and the W bound is attained (min slack 0).
- Relation to the literature: the hypothesis "every generator < c − 2m" excludes right generators (r = 0), so on
  this class Eliahou's number equals W, and GW-25 says E = W ≥ e − 2.
  - CORRECTION (2026-10-19): an earlier version of this entry claimed the class contains the Eliahou–Fromentin
    near-miss family (LITERATURE #30). It does not. W₀ = −C(n,3) < 0 forces right generators (W = E when r = 0).
  - Those near-misses lie in the GW-26 class: 2n_1 ≥ c − m with E directions allowed.
  - In P_4 terms (GW-21/24), GW-25 is the primary regime with b = c = e = 0 and q₂ = 0, for every a, including
    missing AA pairs. It supersedes the a = 7 computer certificate (GW-24) and codex's
  "uniform remaining claim" 4[C(a+2,3) − u₄] + ρ ≥ C(a+1,3).
- Mechanism: packing (LP/SP/HP) uses residues only, and loses a factor ≈ a. The arc uses the integer location of
  τ = v − deg·m inside its band: a whole residue arc of length ≈ h/2 is reachable only by pairs. This forces
  ρ = m − h ≥ m − 2p − 2, and ρ enters W with coefficient +1.
- Extension to B/C/E directions: Theorem GW-26 below. The case q₂ > 0 is reduced in GW-26b.

**Theorem GW-26 (Wilf for 3m < c ≤ 4m whenever 2n_1 ≥ c − m; PROVED 2026-10-19 on paper by codex P5; every
identity re-derived and checked symbolically by the lead, src/scratch/gw/p5/lead/).**
Statement (multiplicity form):
- Hypotheses: P4 hypotheses, primary regime 4m ≤ M < 5m, and every A unit satisfies 2t_a ≥ h (upper-unit (U)).
- If a ≥ 1:
      W ≥ (a−1)(b+1) + c(c+e+1) + e(3a+2b−1) + (c+e)(q₃+s₃+t₃).
- If a = 0: W ≥ c(c+1) + e(2b+c) + (c+e)t₃ ≥ 0.
- Semigroup form: **Wilf holds for every S with 3m < c ≤ 4m and 2n_1 ≥ c − m.**
  - Classes: A: n < c − 2m; B: [c−2m, c−m); C: [c−m, c); E: [c, c+m).
  - Use the lexicographic Apéry tile.
  - Hypothesis (U) for A generators is exactly 2n_1 ≥ c − m. It holds automatically outside A.
Proof (P5_REPORT §§2–7):
1. Refined arc (ARC): h ≤ 2(q₃ + b + c + e + s₄ + t₄) + 2.
   - Take Y = [h, min(⌈3h/2⌉, m)) ∪ [1, ⌈3h/2⌉ − m). Every residue in Y is occupied by an I₃ AA cell, a B/C/E unit,
     or an I₄ AB/BB cell. No cubic, AC, BC or A cell can occupy Y.
2. Exact identity (ID), λ ∈ [0,1]:
   - W = C_λ + k_λq₃ + j_λs₃ + l_λt₃ − 3(v₃+w+z) + G_λ + (nonnegative shadow and capacity slacks)
     + (1−λ)·SRslack + λ·ARCslack.
   - SR is the joint short-residue lemma (3). λ = 0 is the band identity and λ = 1 the arc.
3. Region I (a ≥ 2, b ≤ a² − a − 1, b(2a+b+1) ≤ 6a(a+1); contains a ≥ 3, b ≤ a+1, and (2,0), (2,1)):
   - Take λ = 1 with linear shadows and explicit rational multipliers (LIN).
   - This gives W ≥ (a−1)(b+1) + G₁.
4. Region II (a ≥ 2, b ≥ a+2, and (2,2), (2,3)):
   - Use the B-face curvature inequality 3z ≤ (b+2)t₃ − 2t₃(B−t₃)/(2b+1). It follows from condensed Macaulay
     z ≤ C(x+2,3) at t₃ = C(x+1,2), since the B units, I₃ BB and BBB cells form a multicomplex.
   - The endpoint certificates λ = 0 and λ = 1 give two concave quadratics in x = t₃/B, with values −F_a and
     (a−1)(b+1) at x = 1.
   - An analytic bridge shows max ≥ (a−1)(b+1). It reduces to the parameter inequality (S), proved by a 26-term
     polynomial with all coefficients positive in X = a−1, Y = b−a−2, plus 9 exact small cases.
5. a ≤ 1 directly from W = W_A + T + R.
- Lead's checks:
  - (ID) as an exact polynomial identity in all 20 variables;
  - all LIN identities; Region I certificate = first line;
  - both endpoint branches and EP;
  - the MC identity; POLY (26 monomials, min coefficient 6);
  - the 9-point table (exact match);
  - Region II grid, 63,905 parameter pairs, signs and (S): 0 failures;
  - weak bound W ≥ (a−1)(b+1) + c(c+e+1) + e(3a+2b−1) on 24,651 random semigroups (lead's own classifier):
    0 failures, min slack 6.
  - Codex additionally ran exhaustive d ≤ 4 down-sets, the genus ≤ 28 tree (580,615 upper-unit instances) and
    random checks.
- Contains the Eliahou–Fromentin c = 4m near-miss family (LITERATURE #30), all of whose generators lie in
  [(3m+1)/2, (5m−1)/3]. Uniform in e. No packing, no finite certificates.

**Reduction GW-26b (low units; PROVED, codex P5 §9, identities re-checked by the lead).** Drop (U). Put
L = min_A t_a, δ = max(0, h − 2L), K = q₃ + b + c + e + s₄ + t₄.
- Adaptive arc: h ≤ 2K + 2 + 3δ. (If 3L ≤ h this is trivial. Otherwise use Y_L = [h, min(3L, m)) ∪ [1, 3L − m).)
- (LOW), for a ≥ 3:
      W ≥ (a−1)(b+1) + G + min((a+1)q₂, C(a+1,3)) + b u₃ + (c+e)(2q₂+u₃) − max(0, 3δ − (b+2)q₂ − k).
  - Uses LC (GW-24); identity LOW-ID re-derived by the lead in both endpoint branches.
- Consequence: a counterexample to Wilf with 3m < c ≤ 4m must have a ≥ 7, δ > 0 (some generator with 2n < c − m),
  3δ > (a−1)(b+1) + G + L_min + (b+2)q₂ + b u₃ + k + (c+e)(2q₂+u₃), and GW-24's LC− conditions.

**Theorem GW-26c (one low unit; PROVED 2026-10-19 on paper by codex P5b, src/scratch/gw/p5/P5_REPORT.md §§12–14;
verified by the lead: algebra of OL, OL-res and the final remainder re-derived by hand; the η-substitution in LOW-ID
checked; every ingredient checked numerically, E221).** In the primary regime 4m ≤ M < 5m, if at most one A direction
has 2t < h, then W ≥ 0, for every b, c, e.
- Semigroup form: Wilf holds whenever 3m < c ≤ 4m and 2n_2 ≥ c − m, n_2 the second generator above m. No condition on
  n_1.
- Ingredients:
  - IARC: h ≤ 2(q₃+b+c+e+s₄+t₄) + 2 + 2J, where J counts the actual non-allowed occupants of the arc Y.
  - I-LOW (a ≥ 3): W ≥ A* − max(0, η − (b+2)q₂ − k) for any η with h ≤ 2K + 2 + η.
  - OL (a ≥ 6, one low unit x): 2J_A ≤ (a−1) + LC_actual + 2q₂ + k.
  - OL-out: J − J_A ≤ b(1+ε₂) + c.
  - Final remainder: b[a−1+q₂+u₃−2(1+ε₂)] + G − 2c ≥ 0.
  - For a ≤ 5, GW-24 (paper part) applies.
- Also proved there (§15), algebra re-derived by the lead:
  - ASR: ρ ≥ t₃ + I + v₃ + w + z + H₃, where H₃ counts AAA cells with τ ≥ 2h.
  - HIGH: W ≥ LC_actual + C(p+2,3) − C(a+1,3) + 5r_A + D₃ + T, with p = #{A units with 3t ≥ 2h}.
- Remaining frontier for 3m < c ≤ 4m (§17): a ≥ 7, at least two low units, δ > 0, LC−, LP-low, MAC−, and (F1) η > A*
  + (b+2)q₂ + k, (F2) W_A + T + H₃ < 0, (F3) HIGH < 0.
- False route, preserved: the unrestricted OL (any number of low units) fails on a relaxed, non-residue-complete full
  cubic simplex (a = 7, m = h = 5, offsets (2,2,3,3,3,3,3)).

**Theorem GW-26d (two low units; PROVED 2026-10-19 on paper by codex P5c, src/scratch/gw/p5/P5_REPORT.md §§20–23;
verified by the lead: MG2 and the ALT2 polynomial identities re-derived symbolically (sympy; MG2 also exhaustively
with exact Macaulay pseudo-powers for a ≤ 60); every displayed counting inequality checked numerically by an
independent implementation, E227).** In the primary regime 4m ≤ M < 5m, if at most two A directions have 2t < h, then
W ≥ 0, for every b, c, e.
- Semigroup form: Wilf holds whenever 3m < c ≤ 4m and 2n_3 ≥ c − m, n_3 the third generator above m.
- Ingredients (x, y the low directions, L = t_x ≤ t_y, p = a − 2, δ = h − 2L, H0 = h − L):
  - Structure: no I3 cubic and no quartic has two high factors, so u3 = u0 + u1, k = k0 + k1, q2 = n0 + l.
  - 2L-SH: 4k0 ≤ 5u0 and 3k1 ≤ 4u1. 2L-COUNT: J_A ≤ 6 + (p+1)n0 + k0 − u1 + C(l_x+1,2) + C(l_y+1,2).
  - 2L-ROUGH: P := (a−1) + LC + 2q2 + k − 2J_A ≥ a − 13 + (5−a)n0 + l_x(a+2−l_x) + l_y(a+2−l_y). Hence l ≥ 2 ⇒ P ≥ 2.
  - MG2 (Macaulay gap): a ≥ 4, 2 ≤ q < C(a+1,2) ⇒ (a+2)q − 3q^{⟨2⟩} ≥ 2a − 2. Hence r_A > 0 ⇒ P + D3 ≥ 0.
  - Full quadratic face (r_A = 0, l ≤ 1):
    - COLD2 and the fixed-arc count give 2L-FIX: P + D3 ≥ 4a − 4 + (a+1)l − 6R, R = #{high A : t < ⌈3h/2⌉ − 2L}.
    - The arc Y_{H0} gives 2L-HIGHARC: P_H ≥ δ − (2a−2) − (3a−5)l.
    - SIDON2: the R − l non-exceptional high offsets in [h − L, ⌈3h/2⌉ − 2L) have all pair residues present and
      distinct, so their differences are distinct and n(n−1) ≤ 2⌈δ/2⌉ − 2.
    - Together: ALT2, P + D3 ≥ 0 or P_H ≥ 0 (a ≥ 7).
  - Outside cells: OUT2 J − J_A ≤ b(2+n0) + 2c, OUT2b, HOUT2. They are paid in PAY2 through I-LOW with η = 2J or
    η = −δ + 2J_{H0}. The a = 7 boundary B7 (n0 = q2 = 3, l = u3 = 0) uses Macaulay (r_A ≤ 1) and HIGH.
- Residue injectivity enters beyond arc occupancy only in SIDON2 (distinct pair sums ⇒ Sidon set of offsets).
- Codex's continuation (§§24–27, three low units) is verified and recorded as GW-26e (a ≥ 13).

**Theorem GW-26e (three low units, a ≥ 13; PROVED 2026-10-19).** Sources: codex P5c, src/scratch/gw/p5/P5_REPORT.md
§§24–27 (T2.3-M, T2.3, T2.3F), plus two lead refinements that close 13 ≤ a ≤ 15. Verification by the lead: the
algebra symbolically (E230); the finite certificate by an independent implementation (E228); LSP exhaustively for
n ≤ 8 (E229); every inequality used, on 471,750 actual three-low semigroups (E232). Statement: in the primary regime
4m ≤ M < 5m, if exactly three A directions have 2t < h and a ≥ 13, then W ≥ 0, for every b, c, e.
- Semigroup form, together with GW-26d and GW-24: Wilf holds whenever 3m < c ≤ 4m and at most three minimal
  generators n satisfy 2n < c − m, unless exactly three do and 7 ≤ #{minimal generators n < c − 2m} ≤ 12.
- Notation: α = 3, p = a − 3, r = r_A, l = Σ_i l_i (low–high I2 pairs), n0 = present low–low pairs, θ = ⌈3h/2⌉,
  L = least low offset, δ = h − 2L, R = #{high A : t < θ − 2L}, t = t_A, ε = t − t_forced with t_forced = 0, a, 2a−1
  for r = 0, 1, 2.
- Uniform counts (any α), with P = (a−1) + LC + 2q2 + k − 2J_A as in GW-26d:
  - GEN-COUNT: J_A ≤ α + n0 + c0 + k0 + p·n0 − u1 + Σ C(l_i+1,2), and J − J_A ≤ b(α + n0) + αc.
  - GLOC: the fixed-arc I-LOW payment is ≥ Φ, by coefficient comparison.
  - Shadows 4k0 ≤ (α+3)u0 and 3k1 ≤ (α+2)u1. GEN-ROUGH: P ≥ 15 − 5a for α = 3, a ≥ 7.
- Cases:
  - r ≥ 3 (T2.3-M, a ≥ 13). MG6: a ≥ 13 and 6 ≤ q ≤ Q−3 ⇒ (a+2)q − 3q^{⟨2⟩} ≥ 6a − 18. Hence P + D3 ≥ a − 3.
  - l ≥ 6: 3L-STARS. l ≥ 5 − 2r: 3L-GAP-STARS (P + D3 ≥ 0, 10, 9). Both use NEAR-GAP D3 ≥ r(4a−3r−1)/2.
  - a ≥ 13, r ≤ 2 and c + e > 0: the C/E terms pay the rough loss, so c = e = 0 may be assumed. At a = 13 the b
    coefficient is max(1, B_f), via OUT3b (J − J_A ≤ b(3+β) + 3c) and the β = 6, u3 = 0 subcase.
  - r ≤ 2, l ≤ 4 − 2r, W_A < 0: FIN. The fixed-arc payment is ≥ K + b·B_f, and the H0-arc payment is
    ≥ δ − B + D3 + b·B_h. Both are combined with PSID (3L-PACK), WINDOW-SP, WINDOW-COUNT (LSP + LOC-DEF) and two
    lead refinements:
    - JOINT-SP (lead): all α + R offsets lie in [L, θ−2L), an interval of ⌈3δ/2⌉ integers. So
      3⌈3δ/2⌉ − 2 ≥ H(α+R−r) − λ·ε.
    - Retained cold-pair step (lead; codex reached the same independently): in F_cold keep D3 − 3t0 ≥ 3(t − t0max)
      − (a+2)r. When n0 = 6 the forced missing cubics contain a high, so t0max = min(10, t − t_forced).
  - No count profile survives for 13 ≤ a ≤ 40 (E228). For a ≥ 41 the analytic T2.3 applies (3L-POLY table,
    18 positive-coefficient polynomials, E230).
- Proof dependencies: the P4 SP lemma (GW-24; LSP is its interval form) and the GW-26/26c/26d framework (I-LOW,
  transfer, LC, LC-minus).
- Caveats:
  - The finite certificate is a computation over count profiles, re-implemented independently.
  - No instance with a ≥ 41 was sampled; the Sidon samplers cannot reach it for m < 6000.
- Open in this regime: α = 3 with 7 ≤ a ≤ 12, and α ≥ 4. The reduction of all α to the bounded-defect packing
  lemma LSP* is heuristic (NOTEBOOK 2026-10-19 night).

**Theorem GW-26f (a ≤ 13, every low population; PROVED 2026-10-19, computer-assisted).** Sources: codex P5d,
src/scratch/gw/p5/P5_REPORT.md §39 (T2-SMALL), with the lemmas of §§24–38. Verification by the lead: an independent
re-implementation of the certificate (E235), instance checks of every lemma it uses for α ∈ [3, 8] (E234), and a paper
check of U-SMALL/U-B0 (below). Statement: in the primary regime 4m ≤ M < 5m, if a ≤ 13 then W ≥ 0, for every α, b, c, e.
- Semigroup form: Wilf holds whenever 3m < c ≤ 4m and at most 13 minimal generators lie in (m, c − 2m). Since
  a ≤ d = e − 1, **Wilf holds for every S with e ≤ 14 and c ≤ 4m** (with GW-19, or Eliahou, for c ≤ 3m).
- Corollary (with an external input): **Wilf holds for every S with c ≤ 4m and m ≤ 45.** If e ≤ 14 this is the above;
  if e ≥ 15 then 3e ≥ 45 ≥ m, and Wilf follows from Eliahou's theorem for 3e ≥ m (LITERATURE; CITED, not re-proved).
- Cases: a ≤ 6 is GW-24; α ≤ 2 is GW-26/26c/26d; 7 ≤ a ≤ 13 with α ≥ 3 is a finite count certificate over
  (a, α, r, n0, l; t, u0, u1; c0; β ∈ {0, β_max}; R, b; δ), cut by:
  - W̄_A + Ĥ ≤ −1 (HOT-ALL; Ĥ = H_cold of COLD-HIGH if β ≥ 1, else 0), with quartic allowances
    K0 = min(u0^{⟨3⟩}, ⌊(α+3)u0/4⌋), K1 = ⌊(α+2)u1/3⌋;
  - f_R + b·B_f ≤ −1 (fixed arc: R-EXACT with S_min; β maximal under COLD-MAC dominates every β ≥ 1);
  - δ ≤ B − D3 − b·B_H − 1 (DELTA-UP) and LOW-FIN (I-LOW with η ≤ 3δ);
  - B-CUT and B-NEIGH on b; m_low ≤ m_up (global SP after endpoint deletion and PSP, against the cardinality bound with
    C/E counts limited by the retained transfer costs c(c+1+q+q2+u) + e(3a+2b+c+q+q2+u)); δ ≤ m_up − 2;
  - WINDOW-SP/COUNT, PSID, JOINT-SP/COUNT, joint PSP;
  - MIX-GAP completion (§38): if B0 < Γ(a+b, q, r) every AB/BB pair is in I3, and then the complete d0-direction face
    must pass SP/PSP against C(d0+3,3) − r(1+b) − t + K + c(d0+1) + e.
- What actually kills the profiles (E235): for a ≤ 12 the cardinality test or an empty δ range alone; at a = 13, 126
  profiles (α = 4, r = 0, n0 = 10, u = 0, β = 10, R = 9) need MIX-GAP. No window/joint packing test is needed for a ≤ 13.
- The C/E remainders in both arc payments are nonnegative on every base state, since q + q2 + 2 ≥ 2(α+E) there. Proof
  (lead): W_A < 0, LC ≥ 0 and a ≥ 4 give (a+17)r/3 < F, hence r < Q − 2a, so q > 2a ≥ 2(α+E). The inequality is FALSE
  without W_A < 0 (E234: m = 1217, a = 7, α = 3, r = 19, W_A = 208). The certificate code asserts it on every state.
- Also verified (paper, lead; algebra E230):
  - U-SMALL: α ≥ 4, r = l = 0, ε ≤ Q_α/4 ⇒ W ≥ 0 (every a). Gap noted and closed: A-LOW (a(a−1) > 3α(α+1)) is derived
    from LC ≥ (a+1)Q_α, which needs a ≥ α + 2; for a ∈ {α, α+1}, (a+1)u0 − 4k0 ≥ (a−α−2)u0 ≥ −2U_α gives W_A ≥ 0 directly,
    so A-LOW holds whenever W_A < 0.
  - U-B0: α ≥ 4, r = l = b = 0 and a ≤ 2α + 2 ⇒ W ≥ 0; otherwise MID-B0: Q_α/4 < ε ≤ [(a−2α−1)Q_α − 2a + 3α]/6.
  - The conditions r = l = 0 are tile conditions; no tile-free translation is asserted.
- Caveats: the certificate is over relaxed count profiles (necessary conditions), re-implemented independently. The
  MIX-GAP budget containment and completion accounting are paper lemmas of codex, checked on actual semigroups (E234),
  not re-derived line by line by the lead.

**Theorem GW-26g (a ≤ 18, every low population; PROVED 2026-10-19, computer-assisted).** Sources: codex P5e,
src/scratch/gw/p5/P5_REPORT.md §§42–50 (T2-SMALL16, T2-SMALL17, T2-SMALL18), on top of GW-26f. Verification by the lead: an
independent C re-implementation of the whole certificate from the report text (E237), and a paper check of every new
lemma (below). Statement: in the primary regime 4m ≤ M < 5m, if a ≤ 18 then W ≥ 0, for every α, b, c, e.
- Semigroup form: Wilf holds whenever 3m < c ≤ 4m and at most 18 minimal generators lie in (m, c − 2m). Hence **Wilf
  holds for every S with e ≤ 19 and c ≤ 4m**.
- Corollary (with an external input): **Wilf holds for every S with c ≤ 4m and m ≤ 60.** If e ≤ 19 this is the above;
  if e ≥ 20 then 3e ≥ 60 ≥ m, and Eliahou's 3e ≥ m theorem applies (LITERATURE; CITED, not re-proved).
- New lemmas used, each checked on paper by the lead:
  - PAIR-COVER (§43). For r distinct quadratic monomials G on d variables (loops allowed), F_G = dr − C(r,2) + D_G + T_G,
    and D_G + T_G ≥ C(τ(G),2).
  - PAIR-ID. ζ = t − dr + C(r,2) = D_G + T_G + v, where v counts the legal missing cubics.
  - LINKED-DEF. The actual minimum cover k has C(k,2) ≤ ζ − v_lower, and the legal-defect budget is
    e_k = min(ε_M, ζ − C(k,2)); for the A face v_lower = max(0, t0 − α·r_LL).
  - LINK-SP, LINK-Q, LINK-PSP. Packing on the N − k residues left after removing the cover; the same k must serve the
    global test and all three interval tests.
  - MIX-PACK (§44). A partial mixed face of size q_g with E_g = ⌊(D3 + M − Δ_g)/3⌋ and the linked cover k_g, tested
    against MIX-CARD; no ambient packing conjecture.
  - E-REPAIR (§50).
    - For the actual minimum cover k, the number of high units below h − L is at most
      E_k = min(p, l + min(r − r_LL, r − k + 1)) (E_0 = min(p, l)).
    - Reason: each such unit's pair with the least low unit L is present (≤ l) or an absent edge at L, and
      deg_G(L) ≤ r − τ(G) + 1.
    - In §34, E enters C_H, B_H and Ω_H only as that upper bound, each monotonically in the safe direction.
- What kills the profiles (E237):
  - a = 14 and 15: MIX-PACK (42 and 339 profiles, all r = 0, α = 4, n0 = 10, β = 10);
  - a = 16: MIX-GAP 108,405, LINK 105, MIX-PACK 12,031;
  - a = 17: without E-REPAIR exactly four matching rows survive (α = 7, n0 = q2 = 28, l = b = 0, (r, t, c0) =
    (4, 80, 84), (5, 85, 84), (5, 86, 83), (5, 86, 84)), identical to codex. With E-REPAIR, E_k = 1, so δ ≤ 201..205,
    while LOW-FIN needs δ ≥ 246. 0 survivors.
- Uniform consequences recorded with it (paper, re-derived by the lead; not needed for the theorem):
  - LOW-H(E). For α = A ≥ 4, all low pairs present and l = b = c = e = 0, a counterexample needs
    4a − 6A + 2(2A+1−a)Q_A + 4D3 − 6E_k[1 + A(a−A)] − 6C(E_k+2,3) ≤ 0.
  - MATCH-LOW. For a matching missing-pair graph, PAIR-ID gives t = ar + v and D3 = 2(a−1)r + 3v, so
    8(a−1)r + 12v + 4a − 6A − 12 + 2(2A+1−a)Q_A − 6A(a−A) ≤ 0.
- Further codex P5e results (checked by the lead as stated; NOT used above):
  - LARGE-A (§46, paper; constants checked in E238): for α ≥ 4, a ≥ 16·C(α+1,2)² ⇒ W ≥ 0, for arbitrary b, c, e, r, l.
  - P47-B0 (§45, CONDITIONAL on the ambient packing P(C†), C† ≈ 47.2296): the whole branch r = l = b = 0. The identity
    and certificates were checked symbolically (E238).
  - B-free strip (§47, finite): r = l = b = 0 with 4 ≤ α ≤ 14 is closed for every a (independent check, E238).
  - T2-SMALL18 (§50; codex: C enumeration plus a replay of 90 profile hulls with LOCAL-COVER/Ehat_k). LOCAL-COVER was
    checked on paper by the lead.
    - Lead's independent full-domain run (E237): 0 survivors at a = 18, with base/u counts identical to codex
      (26,725 / 71,891,624).
    - This holds with E-REPAIR alone (E_k = min(p, l + min(r − r_LL, r − k + 1)), flags MLPE) and with LOCAL-COVER
      added (MLPEH).
    - Codex's degree-only E = min(p, l + r − k + 1) left 90 hulls. The r − r_LL term already removes them.
    So a = 18 IS counted.
- Remaining in the primary regime: α ≥ 4 and 19 ≤ a < 10·C(α+1,2) (LARGE-A′, below), with all FRONTIER-41 and
  linked-cover conditions. For each fixed α this is a finite search, but α is unbounded.
- Caveats: as for GW-26f, these are finite certificates over relaxed count profiles (necessary conditions). The lead's
  re-implementation is independent code written from the report text, and it agrees with codex on every count column
  at a = 14..17.

**Theorem GW-26i (α = 5, every a; PROVED 2026-10-19 by the lead, computer-assisted).** In the primary regime
4m ≤ M < 5m, if α = 5 then W ≥ 0. With GW-26h, the primary regime is proved whenever α ≤ 5.
- Semigroup form: Wilf holds whenever 3m < c ≤ 4m and at most five minimal generators lie in (m, (c − m)/2).
- Proof, in three ranges.
  - a ≤ 18 is GW-26g.
  - a ≥ 150 = 10·C(6,2) is LARGE-A′.
  - 19 ≤ a ≤ 149 is the lead certificate (flags MLPEHG), restricted to α = 5 and run for every a: 0 survivors.
    Log: fejer ~/wilf/lead23/al_sweep_5f.log; summary line "alpha=5 a=19..149 total_survivors=0 time=5623s".
- Builds used during the sweep, each valid and with only necessary conditions as tests:
  - the fast build of E242;
  - from 12:41 UTC, the same build plus a survivor counter;
  - from 13:03 UTC, the quartic face cap k1 ≤ p·u0 (lines marked q1cap=1). This is a proved valid tightening: a
    3-low+1-high A-quartic is a 3-low I3 cubic plus a high unit (E246).
- Every line has krange>64 = 0 (no k-cover truncation).

**Theorem GW-26h (α = 4, every a; PROVED 2026-10-19 by the lead, computer-assisted).** In the primary regime
4m ≤ M < 5m, if α = 4 then W ≥ 0. With GW-26/26c/26d/26e/26f, the primary regime is therefore proved whenever α ≤ 4.
- Semigroup form: Wilf holds whenever 3m < c ≤ 4m and at most four minimal generators n satisfy m < 2n − m < c − 2m,
  i.e. at most four lie in (m, (c − m)/2).
- Proof, in three ranges.
  - a ≤ 18 is GW-26g.
  - a ≥ 100 = 10·C(5,2) is LARGE-A′.
  - 19 ≤ a ≤ 99 is the lead's certificate (E237 code, flags MLPEHG) restricted to α = 4, run for every a: 0 survivors
    (E241). It is the same exhaustive §39 necessary domain with all tests, restricted to α = 4. No domain assertion
    (q + q2 + 2 ≥ 2(α+E)) failed.
- Mechanism: for every a ∈ [19, 99] each profile dies at the global SP/PSP-versus-cardinality comparison or at an empty
  DELTA-UP/LOW-FIN δ range. No window, joint, LINK or MIX-PACK test is needed there.
- The early GLOC cap (flag G) used to make this fast is a necessary condition (§24). It leaves every profile count
  unchanged where both versions were run (a = 15, 16).
- Audit (2026-10-19, later): the k-cover arrays kE/klist[64] could silently truncate. Rerun with the fixed build
  (KCAP 4096 plus a counter): identical result, krange>64 = 0 for every a (E241).
- §39 domain audit for large a: every lemma used carries only LOWER bounds on a (a ≥ 3, 7, 13) or α ≥ 3/4, so the
  certificate is valid for all a ≥ 19. The bound "q > 2a ≥ 2(α+E) for a ≥ 7" uses E ≤ p = a − α.
- **Extension attempts (E242).** α = 5: CLOSED (GW-26i above). α ≥ 6 does NOT close with the current tests:
  - α = 6, a = 20, 21 leave 3 and 136 B-loop-like rows;
  - α = 8, a = 19, 20 leave 61 and 781 matching rows.
  These are finite relaxed-profile families, not semigroups.

**P5g packing results (codex, P5_REPORT §§60–67, 2026-10-19; counting lemmas reviewed by the lead).**
- PROVED:
  - DIFF2/REPEAT2: repeated cubics cost O(n²).
  - The CP signed-collision bound and SC.
  - SF0: 3s−2 ≥ H(n) − 9n² + 3n for pair-distinct sets with all squarefree triple sums distinct.
  - SG: P(45) with error 63n² when every squarefree fibre has ≤ 10 triples.
  - SM: P(45) with error (63 + M/2)n² when there are M heavy squarefree fibres.
  - RET-G: retained pairs with explicit degree/absent-sum costs; MATCH-P holds on the light class.
  - B0-CUT and B10-CUT (b < max(4a, 128), etc.) and B-RARE: the entire §57 B-loop template is excluded unconditionally.
  - BFREE-LIGHT (r = l = b = 0, α ≥ 1910, all undeleted joint squarefree fibres ≤ 10 ⇒ W ≥ 0) and BFREE-RARE
    (α ≥ 3618 and W < 0 ⇒ more than α/32 heavy joint fibres).
  - Lead check of §65 (2026-10-19): every rational constant and polynomial was recomputed exactly (sympy,
    fejer ~/wilf/lead23/p65_check.py). The checks were:
    - H(b−2) − 11(b−2)² = b³/2 − 29b²/2 + 53b − 52 > 3b³/8 for b ≥ 128;
    - (163/128)³/6 < 7/20, and the B0 upper sum 0.35004 < 3/8;
    - the B10 lower coefficient = 2959/12288 > 9/40, against an upper sum of 0.2105;
    - B-RARE: 2791/12288 > 9/40;
    - both BASE/SM polynomials are positive for N ≥ 480, and the MATCH margin is 877/800;
    - the g(w) square-completion identity;
    - the shifted cubics at A = 1910 + z and 3618 + z (real roots 1909.17 and 3617.38).
    The structural steps were also checked: the pigeonhole C(a,3) > C(a+1,3)/3 for a ≥ 4, and the 3s − 2 ≤ m − 2h
    interval capacity.
- Preserved false strengthening: ANTIPODAL, X = {±10^i}, refutes the SUPPORT form of MATCH-P even with quadratic error.
- Open:
  - ambient P(C) with linearly many heavy squarefree fibres;
  - ambient MATCH-P (needs the ambient diameter or primary geometry for concentrated absent-pair sums);
  - the finite small-a residual families above.
- These results are for integer/interval sets. A mod-m use needs DIFF2 re-proved mod m: three points pairwise ±d apart
  exist when 3d ≡ 0.

**Theorem LARGE-A′ (sharpened LARGE-A; PROVED 2026-10-19 by the lead, paper plus a small exact check).** Under the
primary hypotheses, if α ≥ 4 and a ≥ 10·C(α+1,2), then W ≥ 0, for arbitrary b, c, e, r, l, ε and high exceptions.
Codex's LARGE-A (P5_REPORT §46) needs a ≥ 16·C(α+1,2)². The new threshold is linear in R0 := C(α+1,2) ≈ α²/2.
- Proof. It follows the chain of §46, with K = R0 − 1, U0 = C(α+2,3), F = C(a+1,3). Assume W < 0. Two steps change,
  and the final comparison is made exact.
  1. **q ≥ C(R0+1,2).** Write q = C(j+1,2) + z with 0 ≤ z ≤ j < R0. By exact Macaulay, u3 + u4 ≤ q^{⟨2⟩} =
     C(j+2,3) + C(z+1,2). Then (a−3)q − 4q^{⟨2⟩} = C(j+1,2)[(a−3) − 4(j+2)/3] + [(a−3)z − 2z(z+1)], which is ≥ 0 when
     3(a−3) ≥ 4(R0+1) and a ≥ 2R0 + 3. So W_A ≥ 3a(a+1) > 0, contradicting W_A < 0 (transfer: W ≥ W_A).
  2. **LA-BUDGET (unchanged).** GLOC gives D3 < Ka and b < 2K. This needs a ≥ 2(1 + 2α + R0), a ≥ 2α + 1 and
     a + 1 ≥ 5(α+3)/4.
  3. **r ≤ K, already for a ≥ 2R0.** Let Δ = (a−j)C(j+1,2) + (a+2)z − 3C(z+1,2) ≤ D3 < Ka.
     - In the blocks R0 ≤ j ≤ a−2, Δ is concave in z and is a negative-leading cubic in j at both z-endpoints. Its
       minima are at j ∈ {R0, a−2}, and all four endpoint values are ≥ Ka for a ≥ 2R0.
     - In the block j = a−1, Δ = r(4a−3r−1)/2. At r = R0 it is ≥ Ka iff a ≥ R0(3R0+1)/(2R0+2); at r = a iff
       a ≥ 2R0 − 1.
     Hence ε_M = (D3 − Δ)/3 < Ka/3.
  4. **Exact comparison.**
     - Lower bound. Cyclic SP on n = a+1−r ≥ n0 := a+1−K pair-injective residues gives
       2m > n0³ − n0² + 2n0 − n0·Ka. The right side increases in n for n ≥ n0.
     - Upper bound. m ≤ C(d0+3,3) + k + c(d0+1) + e, where:
       - d0 = a+b ≤ a+2K−1;
       - k0 ≤ (α+3)U0/4;
       - k1 ≤ (α+2)u1/3 ≤ (α+2)R0·a/3, since u1 ≤ n0·p;
       - c(c+1) ≤ F − 1 and e ≤ (F−1)/(3a), by transfer.
     - Both bounds are monotone in K in the adverse direction. So for a ≥ 300 the worst case is K = a/10 − 1, and
       then 2m_lower − 2m_upper ≥ 0.639a³ − [0.576a³ + 1.023a^{5/2} + 0.125a²] > 0. Ingredients:
       - n0 ≥ 0.9a + 2 and n0² − n0 + 2 − Ka > 0.71a²;
       - C(1.2a,3) ≤ 0.288a³;
       - α ≤ √(a/5), so k0 ≤ 0.0062a², k1 ≤ 0.0188a^{5/2}, c(d0+1) ≤ 0.4925a^{5/2} and e ≤ 0.0562a².
       The bracket 0.063a − 1.023√a − 0.125 is positive for a > 268.
     - For a < 300 with a ≥ 10R0, only α ≤ 7 occurs. There the inequality and all side conditions were checked
       exactly for every a ∈ [10R0, 300] (E240).
  □
- Exact thresholds: the least a0(α) at which the whole chain closes, with every larger a then also checked, is
  97, 146, 203, 270, 346, 431, 525 for α = 4..10. The ratio a0/R0 decreases from 9.73 (α = 5) to 9.10 (α = 200);
  the leading-order limit is θ* ≈ 9.09, the root of (1 − 1/θ)[(1 − 1/θ)² − 1/θ] = (1 + 2/θ)³/3.
- Consequence. With T2-SMALL18 (GW-26g), a counterexample in the primary regime has α ≥ 4 and
  19 ≤ a < 10·C(α+1,2) (about 5α²). For α = 4 this is 19 ≤ a ≤ 99, against a < 1,600 before. The low population is still
  unbounded.

**Theorem GW-27 (Wilf for quadratic Apéry sets, every depth; PROVED on paper 2026-10-19 by the lead; every step
checked on all 61,985,800 quadratic semigroups of genus ≤ 33 and 104k random ones with m ≤ 200, E219).**
CORRECTION (2026-10-19, same day): this is NOT a new result of this project. It is the corollary of Flat-MaxCL
(PROOFS "Flat-MaxCL", proved 2026-10-17), already kernel-checked as `wilf_of_apery_height_le_two`
(lean/Wilf/MaxCL.lean). GW-27 is an independent second proof in Kunz coordinates (identity GW-27a), using the same
mechanism: wrapped cells sit at distinct positions of the top window. Additions over the 2026-10-17 entry:
- the explicit corollary 3n_1 > c + m ⇒ Wilf;
- the remark that Ap(S, n) may be taken for any minimal generator n;
- the cell identity G-ID for every degree (NOTEBOOK 2026-10-19 midday).
Down-set form. Let D ⊂ ℕ^d be a finite down-set with weights n_a > 0 and values v(x) = Σ x_a n_a. Assume D is
residue complete mod m (v is a bijection D → ℤ/m) and every cell has total degree ≤ 2. Put M = max v,
λ(x) = ⌊(M − v(x))/m⌋, κ(x) = ⌊v(x)/m⌋, ℓ = Σ λ, g = Σ κ. Then dℓ ≥ g.
Semigroup form. If every element of Ap(S, m) is 0, a minimal generator, or a sum of two minimal generators, then
e(S)·ℓ(S) ≥ c(S).
- Corollary: Wilf holds whenever 3n_1 > c + m, n_1 the least generator above m. (Each Apéry element is ≤ c + m − 1
  < 3n_1, so it has no factorization of length ≥ 3.) Spirito (arXiv:1710.09245, LITERATURE #24) proved this only
  under e ≥ 10 and m ≤ (8/25)e² + e/5 − 5/4. No condition on e, m or the depth ⌈c/m⌉ is needed here.

Notation. K = ⌊M/m⌋, μ = M − Km, r_a = n_a mod m (pairwise distinct, nonzero), κ_a, λ_a for x = e_a,
δ_a = [r_a > μ], D_hi = Σ δ_a, D_lo = d − D_hi. Each cell x = e_a + e_b (a ≤ b) has carry γ_x = [r_a + r_b ≥ m],
remainder ε_x = M − v(x) − mλ(x) ∈ [0, m) and bonus β_x = [ε_x + r_a ≥ m] + [ε_x + r_b ≥ m]. deg(a) = number of
degree-2 cells containing a, with 2e_a counted twice, and f_a = d + 1 − deg(a) ≥ 0.

Lemma GW-27a (exact identity).
    W := dℓ − g = Σ_a f_a λ_a + D_hi + Σ_{|x|=2} c_x,   c_x = (d+2)λ(x) + β_x − γ_x.
- Proof: λ_a + κ_a = K − δ_a. For x = e_a + e_b: κ(x) = κ_a + κ_b + γ_x. Also
  M − n_a = mλ(x) + ε_x + mκ_b + r_b, so λ_a = λ(x) + κ_b + [ε_x + r_b ≥ m], and symmetrically for b.
  Hence κ(x) = λ_a + λ_b − 2λ(x) − β_x + γ_x. Sum over D with ℓ = K + Σλ_a + Σλ(x). □

Lemma GW-27b (pair contributions). Let |x| = 2 with residue s = v(x) mod m (s ≠ 0).
- (a) c_x ≥ −1, with equality iff λ(x) = 0, γ_x = 1, β_x = 0 ("deficient").
- (b) A deficient x has s ≤ μ and r_a, r_b > μ, hence s = r_a + r_b − m ∈ [2μ + 2 − m, μ].
- (c) If μ < s ≤ 2μ, then c_x ≥ 1.
- Proof. (a) is immediate. Let λ(x) = 0. If s ≤ μ, then v(x) = Km + s and ε_x = μ − s. If s > μ, then
  v(x) = (K−1)m + s and ε_x = m + μ − s.
  - (b) If s > μ and γ_x = 1, then r_a + r_b = m + s and ε_x + r_b = 2m + μ − r_a ≥ m, so β_x ≥ 1. Hence s ≤ μ.
    Then ε_x + r_b = m + μ − r_a, and β_x = 0 forces r_a > μ; likewise r_b > μ.
  - (c) If λ(x) ≥ 1, then c_x ≥ d + 1. Otherwise ε_x = m + μ − s. With carry, both bonuses hold as in (b), so
    c_x = 1. Without carry, r_a + r_b = s ≤ 2μ, so (say) r_a ≤ μ, and ε_x + r_b = m + μ − r_a ≥ m. □

Proof of GW-27. Let U = #deficient cells. Each residue class holds exactly one cell.
- Case 2μ ≤ m − 1. The μ residues in (μ, 2μ] hold D_mid := #{a : μ < r_a ≤ 2μ} units and μ − D_mid pairs, each
  with c_x ≥ 1. Deficient cells lie in [1, μ], disjoint from the D_lo low units, so U ≤ μ − D_lo. Hence
  W ≥ F + D_hi + (μ − D_mid) − U ≥ F + d − D_mid ≥ 0, where F = Σ f_a λ_a.
- Case 2μ ≥ m. The m − 1 − μ residues in (μ, m) hold all D_hi high units and m − 1 − μ − D_hi pairs with c_x ≥ 1.
  Deficient cells lie in [2μ + 2 − m, μ], a set of m − 1 − μ residues. Hence W ≥ F + D_hi + (m − 1 − μ − D_hi) − U
  ≥ F ≥ 0. □
- Minimality of the generators is not used. The mechanism is that of Flat-MaxCL: carries are paid by residue occupancy
  of the window (μ, 2μ] just above the top residue μ = M mod m. Lean: already done for the semigroup form
  (`wilf_of_apery_height_le_two`).

**Corollary GW-20 (PROVED; from GW-19 + GW-PF).** If at most e − 1 pseudo-Frobenius numbers of S are ≥ 3m, then
S satisfies Wilf's conjecture.
- Proof: as GW-18, with P_3 (GW-19s) in place of P_2:
  g = Σ_j|U_j| ≤ (e−1)Σ_{j≤3}|L_j| + Σ_{j≥4} #{f ≥ (j−1)m}·|L_j| ≤ (e−1)ℓ. □
- Coverage: all but 32 of the 712,373 semigroups of genus ≤ 24; all but 1,794 of the 38,858,196 of genus ≤ 32
  (E198 run). Every remaining S has at least e PF numbers ≥ 3m.
- For e = 5 it reads: Wilf holds if at most 4 PF numbers are ≥ 3m.

**Conjecture CP (cover payment; local, uses residues essentially).** Multiplicity form, residue-complete D. Put
Δ(x) = Σ_b λ(R_b x) − κ(x), with R_b the reflection inside the b-column of x; Σ_x Δ(x) = dℓ − g. Then the deficits
can be routed along lower covers: there is a flow, with
- source x carrying capacity max(Δ(x), 0),
- sink y carrying demand max(−Δ(y), 0),
- edges x → y only for x = y − e_b,
that meets every demand. CP ⇒ GW.
- Evidence (E202): flow feasible on every residue-complete instance in d = 2, m ≤ 10, K ≤ 4; d = 3, m ≤ 10, K ≤ 3;
  d = 4, m ≤ 8, K ≤ 2; and on every semigroup of genus ≤ 17 (lex-min factorization tile).
- Evidence, 2026-10-19 (E225): 0 failures on ALL 38,858,195 semigroups of genus ≤ 32 (lex and grlex tiles), and on
  ≈ 260k random instances with m ≤ 220, including the near-arithmetic deep families (⟨80,291,292,293⟩,
  ⟨62,87,88,89⟩, ⟨114,305,307,310⟩, heights up to 31) on which downward payment of the G-ID cells is FALSE (E222–E224).
  - Per cell, Δ(x) = Σ_b ⌊(u_b(x) + x_b n_b)/m⌋ − ⌊v(x)/m⌋, with u_b(x) = M − v(top of the b-column through x) ≥ 0.
    For a corner (top in every direction) with λ = 0 this is #{b : (x_b n_b mod m) ≥ m − (M − v(x))} − carry(x).
  - Deficient cells are top corners in 99.8% of cases; deficits are ≤ 2 for genus ≤ 32 and ≤ 4 in all data.
  - The binding order ideals are principal: for 9,304 of 9,306 deficient y, min_{Z ∋ y} Σ_Z Δ = Σ_{x≤y} Δ.
- No-sharing form: deficit(y) ≤ Σ_b Δ⁺(y − e_b) holds on all semigroups of genus ≤ 32 but is FALSE in general
  (≈ 0.1% of random instances with m ≤ 220, mostly near-arithmetic generators).
- FALSE refinement FS (canonical fractional payment: each cell with Δ > 0 splits Δ equally among the deficient cells
  above it): ⟨14,15,23,24,26⟩, lex and grlex, genus 32 — the deficient corners (0,1,1,0), (0,1,0,1), (0,0,1,1) share
  the surplus cells 0 and e_2; FS gives (0,1,1,0) only 5/6. CP holds there.
- FALSE refinement: canonical corner regions (assign each cell to one corner above it by a fixed climbing or extreme
  rule; require every region sum ≥ 0) fail in 1.5–6% of random instances.
- FALSE refinements:
  - equal split among lower covers: ⟨5,8,9⟩; d = 3, m = 7, n = (8,11,12);
  - pay from y − e_b with b = argmax n_b (⟨5,8,9⟩) or b = argmin n_b (⟨8,9,13,14⟩).
- Residue-free, CP fails even where GW holds (d = 2, m = 9, n = (12,12), GW slack 2). So CP needs residues more than
  GW does.

**Layer-profile domination: Conjectures MAJ, RECT, STAIR (2026-10-19; intrinsic, tile-free).** Let S ≠ ℕ have
multiplicity m, conductor c, Frobenius number F = c − 1 and embedding dimension e = d + 1. For j ≥ 1 put

    a_j = #((ℕ∖S) ∩ [(j−1)m, jm)),     b_j = #(S ∩ [c − jm, c − (j−1)m)).

Both sequences are non-increasing (x ∉ S ⇒ x − m ∉ S; x ∈ S ⇒ x + m ∈ S), so they are partitions with |a| = g and
|b| = ℓ. In Apéry terms a_j = #{w ∈ Ap(S,m) : ⌊w/m⌋ ≥ j} and b_j = #{w : ⌊(M − w)/m⌋ ≥ j}, M = max Ap.
- **Exact identity (PROVED).** a_j = b_j + p_j with p_j = #{gaps x ∈ [(j−1)m, jm) : F − x is also a gap}.
  - Proof: x ↦ F − x maps the bottom layer [(j−1)m, jm) onto the top layer (F − jm, F − (j−1)m] = [c − jm, c − (j−1)m).
  - If s ∈ S lies in that top layer, F − s is a gap, because otherwise F ∈ S. So the gaps of the bottom layer are the
    b_j images of top-layer elements plus the p_j gaps whose mirror is a gap. □
  - Hence Wilf ⟺ Σ_j p_j ≤ (d − 1)ℓ, and e = 2 (symmetric) is p ≡ 0.
- **STAIR (conjecture).** For every non-increasing sequence z_1 ≥ z_2 ≥ … ≥ 0,

      Σ_j min(a_j, z_j) ≤ d · Σ_j min(b_j, z_j).

  - Equivalently (Hall), there is a map from the cells {(j,s) : s ≤ a_j} of the gap diagram to the cells
    {(j',s') : s' ≤ b_{j'}} of the left-element diagram that is at most d-to-1 and has j' ≤ j, s' ≤ s.
- **RECT** is STAIR for rectangles, z = (k,…,k,0,…) of length i: Σ_{j≤i} min(a_j,k) ≤ dΣ_{j≤i} min(b_j,k).
  - k ≥ m gives PGW (P_i); i ≥ K gives MAJ.
- **MAJ.** For every k, the sum of the k largest ⌊w/m⌋ over w ∈ Ap is ≤ d × the sum of the k largest ⌊(M − w)/m⌋.
  - This is exactly the condition for W to have a pointwise nonnegative localization Σ_x[Σ_b λ(σ_b x) − κ(x)] with d
    arbitrary bijections σ_b of Ap (fractional version, by weak majorization).
  - Corner reflection (FGH) gives MAJ with t (type) in place of d.
- **STAIR-p (conjecture; the sharpest form).** The gap-pair profile is (d−1)-dominated: for every non-increasing z,
  Σ_j min(p_j, z_j) ≤ (d − 1)·Σ_j min(b_j, z_j). Since min(b+p, z) ≤ min(b, z) + min(p, z), STAIR-p ⇒ STAIR.
  - In words: the integers x with x and F − x both gaps, arranged by layer and rank, map (e−2)-to-1 into the elements
    of S below c, arranged by layer from the top, without increasing the layer index or the rank.
  - The FGH maps x ↦ f − x (f ∈ PF ∖ {F}) send bottom layer j to top layer ≥ j, the wrong direction. So a proof needs
    descent along generators as well as reflection.
- For e = 3 even per-depth holds: the tile's corner reflection (GW-8) is depth-preserving and t(D) ≤ 2 in dimension
  two (GW-10). STAIR and STAIR-p are therefore e ≥ 4 statements.
- Implications: per-depth (a_j ≤ d b_j ∀j) ⇒ STAIR-p ⇒ STAIR ⇒ RECT ⇒ {PGW, MAJ} ⇒ Wilf.
- Status: per-depth is FALSE on semigroups (217,493 failures at genus ≤ 30). STAIR-p, STAIR, RECT and MAJ have 0
  failures on all semigroups of genus ≤ 30 and on ≈ 80k random instances with m ≤ 200 (E226). All are tight for e = 2.

**Identity GW-CR (column–residue decomposition; PROVED, exact, any down-set).** Let D be a finite down-set in
ℕ^d, n_a > 0, M = max v, and r(x) = v(x) mod m. For a b-column C = {z + j e_b : 0 ≤ j ≤ J} with top t, write
M − v(t) = mλ(t) + ε_t (0 ≤ ε_t < m) and ρ_b(j) = (j n_b) mod m. Then

    dℓ − g = Σ_x r(x)/m + Σ_b Σ_{b-columns C} Ψ_b(C),

with Ψ_b(C) = (J+1)λ(t) + #{0 ≤ j ≤ J : ρ_b(j) + ε_t ≥ m} − (1/m)Σ_{j=0}^{J} ρ_b(j).
If D is residue complete, Σ_x r(x)/m = (m−1)/2, so

    GW  ⟺  Σ_{b,C} Ψ_b(C) ≥ −(m−1)/2.

Proof:
- Column reflection gives dℓ = Σ_x Σ_b λ(R_b x).
- For x = z + j e_b, M − v(R_b x) = M − v(t) + j n_b, so λ(R_b x) = λ(t) + ⌊j n_b/m⌋ + [ε_t + ρ_b(j) ≥ m].
- κ(x) = Σ_b ⌊x_b n_b/m⌋ + (Σ_b ρ_b(x_b) − r(x))/m.
- Subtract and sum over x. □

Remarks:
- A column can be negative only if its top lies in the last band (λ(t) = 0). Then Ψ = Σ_j([ρ_b(j) ≥ m − ε_t] − ρ_b(j)/m).
- The tight cases have every per-cell term zero, e.g. ⟨5,6⟩ (one column, Ψ = −(m−1)/2) and T_{m,4} (Ψ = −s_b/m on
  the columns {0, e_b}).
- Residue completeness enters ONLY through the constant (m−1)/2 and through which column/residue patterns can
  coexist.
- FALSE refinement: the negative columns cannot always be paid from the bonuses r(x)/m of their own cells alone
  (column-bonus Hall). It fails in ≈ 10% of instances, e.g. ⟨5,7,9⟩ and d = 2, m = 5, n = (8,9). Positive columns
  must be used (E203).

**Conjecture CCP (carry–column payment; local).** Residue-complete D, multiplicity form. Write
carry(x) = κ(x) − Σ_a ⌊x_a n_a/m⌋ and let s(b, z) ≥ 0 be the slack of a column (H1). Then the carries can be routed:
- from each cell x to columns, in any direction, that pass through x or through a lower cover x − e_a;
- with each column receiving at most its slack.
CCP ⇒ GW.
- Evidence (E203): 0 failures on semigroups of genus ≤ 18 (33,281; lex-min tile), and on residue-complete down-sets
  d = 2, m ≤ 9, K ≤ 4; d = 3, m ≤ 9, K ≤ 3; d = 4, m ≤ 8, K ≤ 2.
- FALSE refinement: allowing only the columns through x itself fails in ≈ 25% of instances (⟨4,6,7⟩: the corner
  e_1 + e_2 has carry 1 and zero slack on both of its columns).
- Residue-free, CCP fails exactly where GW fails (d = 2, m = 6). It also fails at n = (12,12), m = 9, where GW holds:
  the same instance as for CP.

**Conjecture TR (uniform transfer to the small-generator face).** Multiplicity form at any level K = ⌊M/m⌋, with
ρ = (K+1)m − 1 − M. Let A = {a : n_a < 2m − ρ} (band-1 directions), F_A = D ∩ ℕ^A and
W_A := (|A|+1)Σ_{F_A}λ − K|F_A| (no ρ term). Then

    dℓ − g ≥ W_A.

So the cells using any other direction never make things worse than the pure A-face.
- For K = 4 this is (a version of) the codex P4 transfer lemma, PROVED there with explicit extra nonnegative terms.
- For A = ∅, W_A = 0 and TR is GW itself for "no generator in (m, 2m − ρ)". So TR at all K contains that case of
  Wilf.
- Evidence (E205):
  - holds for every K on all 5,311,726 semigroups of genus ≤ 28 (intrinsic face Ap ∩ ⟨A⟩);
  - holds on residue-complete down-sets d = 2, m ≤ 14, k ≤ 6 and d = 3, m ≤ 10, k ≤ 4.
- Where the face is deficient: W_A < 0 occurs only for K ≥ 5 in the semigroup data (EF-type faces need larger m at
  K = 4). There −W_A ≤ 2·(m − |F_A|), i.e. the deficit is at most twice the number of residues the face misses.
- Residue-free, TR failed in these ranges (d = 2, m ≤ 13, k ≤ 6; d = 3, m ≤ 8, k ≤ 4) only with A = ∅, i.e. only
  where GW itself fails (e.g. {|x| ≤ 2}, n = (9,9)).

**Conjecture PMC (top-d corner window family; stronger than PGW).**
Setting:
- D is a finite down-set in ℕ^d (multiplicity form, n_a > m on active directions).
- V_1 ≥ V_2 ≥ … ≥ V_t are the values of its maximal cells. For a semigroup tile, use instead the maximal Apéry elements
  for ≤_S, i.e. PF(S) + m.
- d′ = min(d, t) and λ_k(x) = ⌊(V_k − v(x))/m⌋₊.

For every i ≥ 1:

    (MC_i)   Σ_{x∈D} min(i, κ(x))  ≤  Σ_{k=1}^{d′} Σ_{x∈D} min(i, λ_k(x)).

Relations:
- MC_i ⟹ P_i, since λ_k ≤ λ_1 = λ.
- For t ≤ d, MC_i follows residue-free from per-depth corner reflection.
  - For x ∈ U_j, take a corner c ≥ x; then c − x ∈ L_j(v(c)), and x ↦ c − x is injective for each c.
- At i = K on the Apéry tile, MC_K is Marashdeh's Conj 5.2 (arXiv:2608.12531) in the equivalent form
  g ≤ Σ_{top e−1 PF f} |S ∩ [0, f]|, i.e. W(S) ≥ Σ_{top e−1 PF f} |S ∩ (f, F]|. So MC_K ⟹ Wilf.
- Semigroup form of MC_2: #(gaps < 2m) ≤ Σ_{top e−1 PF f} #(S ∩ (f − 2m, f]). This strengthens GW-17.

Evidence (E214):
- MC_i for all i ≤ K, with residues: 0 failures.
  - 75,362 random semigroups with t > d (m ≤ 40).
  - 3,814 random residue-complete down-sets with t > d.
  - Exhaustive down-sets d = 3, m ≤ 10, and d = 4, m ≤ 8, weights ≤ 3m (resp. 2m + 4): 6,576 residue-complete
    instances with t > d.
- Residue-free: MC_1 and MC_2 have 0 failures in the same exhaustive ranges (≈ 1.8M (D, n) pairs) and on random
  down-sets. MC_3 fails exactly alongside residue-free GW (e.g. d = 3, m = 10: 86 vs 88).
- So PMC has the residue profile of PGW: depths 1, 2 residue-free, residues needed from depth 3.

FALSE strengthening LMC (E214): each cell uses only its own top-d corners above it,
Σ min(i, κ) ≤ Σ_w Σ_{k≤d} min(i, h_k(w)). This would imply both LW and MC.
- It fails in 22 of 52,753 random semigroups. Smallest: m = 9, e = 4, t = 5, i = 3, with 18 > 16.
- LW and MC each hold on the same sample.

Reduction remark (induction on corners, residue-free scale-q form):
- Removing a non-top corner c (t > d) is valid whenever min(i, κ(c)) ≤ Σ_{k≤d} min(i, ⌊(V_k − v(c))/q⌋₊).
- This holds if V_d − v(c) ≥ iq. So the hard configurations for MC are those with all non-top corners within about
  iq of V_d: corners concentrated near the top, which is the hard PF class of E212.

**Conjecture LW (local Wilf; intrinsic, stronger than Wilf).** For every numerical semigroup S with multiplicity m and
Apéry poset (Ap(S, m), ≤_S), put H(w) = max(↑w) − w = max{u ∈ Ap : w + u ∈ Ap}. Then

    g(S) ≤ (e − 1) · Σ_{w ∈ Ap(S,m)} ⌊H(w)/m⌋,

and more generally Σ_w min(i, ⌊w/m⌋) ≤ (e − 1)Σ_w min(i, ⌊H(w)/m⌋) for every i (local window family).
- It is stronger than Wilf because ⌊H(w)/m⌋ ≤ λ(w) = ⌊(max Ap − w)/m⌋. It replaces the global top by the top of the
  up-set of w.
- It is the semigroup form of local GW (LP_∞) on the minimal tile, with intrinsic heights (sums inside Ap).
- Its depth-1 and depth-2 cases are proved: GW-14 and GW-16 use only upward paths.
- Evidence: 0 failures on all 1,950,429 semigroups of genus ≤ 26, also for the local window family; tight in 127 of
  them (E198).

**Local form and trapped cells (CONJECTURES, with the reduction PROVED).** Multiplicity form throughout.
- Local heights: h(w) = max{v(u) : w + u ∈ D} and λ_h(w) = ⌊h(w)/m⌋ ≤ λ(w).
- LP_i: Σ_x min(i, κ(x)) ≤ d·Σ_w min(i, λ_h(w)). LP_i implies P_i.
- Bands: T^{(j)} = {w non-maximal : jm ≤ h(w) < (j+1)m}. Trapped cells: Y^{(i)} = {x ≠ 0 : every lower cover w of x has
  h(w) < im}. Bottom deficit: β'_i = Σ_{x≠0}(i − κ(x))_+.
- **TCI_i:** i·|Y^{(i)}| ≤ d·Σ_{j<i} j·|T^{(j)}| + β'_i.
- **Reduction (proved): TCI_i ⇒ LP_i.**
  - LP_i ⟺ d·Σ_{j<i}(i − j)|T^{(j)}| ≤ i·(d|NonMax| − (m−1)) + β'_i, since min(i, λ_h) = i − (i − j) on T^{(j)} and 0 on
    corners. Use CL's slack identity.
  - The descent map, routed away from the shallow non-maximal cells, gives d|NonMax| − (m−1) ≥ dΣ_{j<i}|T^{(j)}| − |Y^{(i)}|.
    Substitute.
- TCI_2 is Lemma Y (proved, GW-16).
- TCI_∞ is equivalent to local GW (Σκ ≤ dΣλ_h): for large i, Y^{(i)} = D∖{0} and β'_i = i(m−1) − g. So the reduction
  is lossless in the limit.
- **Pair counting** (x, a) ↦ (x − e_a, a) gives i|Y^{(i)}| ≤ Σ_{w shallow, non-max} up_Y(w) + Σ_{x∈Y^{(i)}}(i − |supp x|)_+.
  Cells of support ≥ i are therefore free. What remains is the trapped cells on faces of dimension < i, against the
  unused upper-cover slots of the bands and β'_i.
  - The crude version with up_Y(w) ≤ #{a : k_a ≤ j} is FALSE (E194). The unused slots are needed.
- **Axis reflection.** On the a-axis, λ_h(j e_a) ≥ κ((K_a − j)e_a), where K_a e_a is the top of the axis. So the axis
  cells' top deficit is at most their bottom deficit. This is the mechanism of |Y_1| ≤ |A| in Lemma Y.
- Evidence: E193 (LP_i), E194 (TCI_i for every i).

**Theorem GW-19 (P_3; PROVED on paper 2026-10-18; proof by codex P3, every step re-checked by the lead).**
Let D ⊂ ℕ^d be a finite down-set, |D| = m. Let n_a > m for every a with e_a ∈ D. Assume x ↦ x·n mod m is a bijection
D → ℤ/m. Then

    Σ_{x∈D} min(3, κ(x)) ≤ d · Σ_{x∈D} min(3, λ(x)).

Inactive directions may be deleted, and D = {0} is trivial, so assume every e_a ∈ D. Three regimes:
- M < 3m: this is P_2 (GW-16).
- 3m ≤ M < 4m: here P_3 = GW (all κ, λ ≤ 3); use the band proof below. Residues are used only in this regime.
- M ≥ 4m: Theorem H below, with q = m. No residues are used.

*Theorem H (residue-free, any scale q).* Let q ≥ 1, D a finite nonempty down-set, n_a > q on active directions,
M = max_D x·n ≥ 4q − 1, and F(t) = min(3, ⌊t/q⌋). Then Σ_D F(v) ≤ d Σ_D F(M − v). The cutoff is sharp:
{|x|₁ ≤ 2} ⊂ ℕ², n = (2q−1, 2q−1), M = 4q − 2 fails (11 > 10 at q = 6).

Proof of Theorem H:
- (H1) *Column reflection.* Fix a direction b and a b-column z + j e_b (0 ≤ j ≤ J, z_b = 0) with top t, and put
  δ = M − v(t) ≥ 0. Reflecting j ↦ J − j gives Σ_j F(M − v(z) − j n_b) = Σ_j F(δ + j n_b) ≥ Σ_j F(j n_b).
  Call the difference s(b, z) ≥ 0. Summing over all columns of all d directions:
  d Σ_D F(M − v) = Σ_D B(x) + CS, where B(x) = Σ_a F(x_a n_a) and CS = Σ s(b, z).
- (H2) *Deficits.* B(x) ≥ F(v(x)) except on C, the mixed quadratics e_a + e_b (a ≠ b) with q < n_a, n_b < 2q and
  n_a + n_b ≥ 3q. There the deficit is exactly 1. For the other cells:
  - degree ≤ 1 and axis quadratics give equality;
  - a mixed quadratic with some F(n_a) ≥ 2 has B ≥ 3;
  - for |x| ≥ 3, B(x) ≥ Σ_a min(3, x_a) ≥ 3, since ⌊x_a n_a/q⌋ ≥ x_a.
  Hence Σ B − Σ F(v) = Σ_σ − |C|, where Σ_σ = Σ_x max(0, B(x) − F(v(x))).
- (H3) *Payments.* Orient each pair of C as (a, b) with n_b ≥ n_a, so 2n_b ≥ 3q.
  - If e_a + 2e_b ∈ D, that cubic has B = 1 + 3 = 4 > 3 ≥ F(v), so it contributes 1 to Σ_σ. The cubic determines
    (a, b).
  - Otherwise the b-column based at e_a is exactly {e_a, e_a + e_b}. Its slack is
    F(M − n_a) + F(M − n_a − n_b) − F(0) − F(n_b) ≥ 2 + 0 − 0 − 1 = 1, because M − n_a ≥ 4q − 1 − (2q − 1) = 2q. The
    column determines (a, b).
  - So |C| ≤ Σ_σ + CS, which is the claim.

*Band proof for 3m ≤ M < 4m.*
- Put ρ = 4m − 1 − M and I_j = [jm − ρ, (j+1)m − ρ), so λ = 3 − j on I_j. Split the directions by the band of n_a
  into A, B, C (I_1, I_2, I_3), with sizes a, b, c.
- Since n_a > m, every cell has degree ≤ 3, and the cells of degree ≥ 2 are exactly:
  - Q (quadratics in I_2; all A-supported), with |Q| = q;
  - R (AA in I_3), F (AB in I_3), T (BB in I_3), with sizes r, s, t;
  - U (cubics, all AAA, in I_3), with |U| = u.
  So m = 1 + d + q + r + s + t + u.
- Every quadratic divisor of a cubic lies in Q. The weighted shadow count (pairs (x, i) weighted by x_i) gives
  3u ≤ (a+2)q. Monomial counting gives q + r ≤ a(a+1)/2, s ≤ ab and t ≤ b(b+1)/2.
- The T-values are distinct integers in [4m − 2ρ, M], so t ≤ ρ.
- ℓ = 3 + 2a + b + q, and residue completeness gives g + ℓ = M − m + 1 = 3m − ρ. Then
  W := (d+1)ℓ − (3m − ρ) = H + b(3a + b + 1 + q) − 3(s + t) + c(2a + b + q) + ρ,
  where H = 2a(a+1) + (a−2)q − 3(r + u) ≥ a(a+1)/2 − q ≥ 0. With s ≤ ab and ρ − 3t ≥ −2t ≥ −b(b+1) this gives
  W ≥ H + bq + c(2a + b + q) ≥ 0. ∎

*Residue dependence.* Only two consequences are used: t ≤ ρ (distinct values) and g + ℓ = M − m + 1 (completeness).
Distinct values alone do not suffice: {|x| ≤ 2}, n = (9, 10), m = 6 has distinct values and P_3 fails (11 > 10).

*Corollary GW-19s (window WW_3 for every numerical semigroup).* #(gaps < 3m) ≤ (e − 1) · #(S ∩ [c − 3m, c)).
- Translation via the minimal tile, as in GW-17.
- For c ≤ 3m this is Wilf (Eliahou JEMS 2018, Cor. 6.5). Here it gets an elementary proof: no Macaulay theorem, only
  the weighted shadow count.

*Verification.*
- E199: exhaustive, every proof identity asserted. That covers 81,566,262 residue-complete instances (d = 2, m ≤ 24;
  d = 3, m ≤ 18; d = 4, m ≤ 14; k_a ≤ 3) and 6.0e9 residue-free Theorem-H instances.
- An independent Python verifier agreed on 628,452 instances.
- Not yet in Lean.

*Reformulation of GW suggested by (H1)* (untruncated, F(t) = ⌊t/m⌋): GW ⟺ Σ_x carry(x) ≤ CS. Here
- carry(x) = κ(x) − Σ_a ⌊x_a n_a/m⌋ = ⌊Σ_a ((x_a n_a) mod m)/m⌋ ∈ [0, |supp x| − 1];
- for a b-column with top t (δ = M − v(t) = mλ(t) + ε, 0 ≤ ε < m),
  s(b, z) = (J + 1)λ(t) + #{0 ≤ j ≤ J : (j n_b mod m) + ε ≥ m}.
So Wilf is "total carries ≤ total column slack". Carries live only on cells of support ≥ 2.

**Status.** PGW (all P_i on every residue-complete down-set, n > 0) is a CONJECTURE that strengthens GW. Proved:
- t ≤ d (GW-12);
- depths j ≤ k_min (GW-13/14);
- P_1 and P_2 in the multiplicity form, without residues (GW-14, GW-16).
- P_3 (GW-19): residues are needed only for 3m ≤ M < 4m. It contains Eliahou's c ≤ 3m theorem.
- P_4: PARTIAL (GW-21, GW-24, GW-25, GW-26). Proved: H4 for M ≥ 6m − 1 (residue-free, sharp), and M ≥ 6m − 3
  with residues (distinct weights). The primary regime 4m ≤ M < 5m is proved:
  - for a ≤ 5 on paper and a = 6 with two finite certificates;
  - for every a under the upper-unit hypothesis (GW-26; semigroups: 2n_1 ≥ c − m);
  - with at most one low unit (GW-26c; semigroups: 2n_2 ≥ c − m);
  - with at most two low units (GW-26d; semigroups: 2n_3 ≥ c − m);
  - with exactly three low units and a ≥ 13 (GW-26e);
  - whenever a ≤ 13, for every low population (GW-26f; semigroups: at most 13 minimal generators in (m, c − 2m));
  - whenever a ≤ 18, for every low population (GW-26g; semigroups: at most 18 minimal generators in (m, c − 2m));
  - whenever α ≥ 4 and a ≥ 10·C(α+1,2) (LARGE-A′);
  - whenever α ≤ 4, for every a (GW-26h); whenever α ≤ 5, for every a (GW-26i);
  - whenever LOW+ holds (GW-26b).
  - Semigroup corollary of GW-26g (superseding GW-26f's e ≤ 14): **Wilf holds for every S with e ≤ 19 and c ≤ 4m**,
    and, with Eliahou's 3e ≥ m theorem, for every S with c ≤ 4m and m ≤ 60.
  - Semigroup corollary of GW-26f (superseding the a ≤ 6 corollary for e ≤ 7): **Wilf holds for every S with e ≤ 14 and
    c ≤ 4m**. Earlier: the a ≤ 6 case gave Wilf for every S with e ≤ 7 and c ≤ 4m
    (with Eliahou, or our GW-19, for c ≤ 3m). More generally, it holds when 3m < c ≤ 4m and at most six minimal
    generators lie in (m, c − 2m).
  Also proved: quadratic down-sets and saturated EF faces. Full GW (every depth) for quadratic residue-complete
  down-sets: Flat-MaxCL (2026-10-17, LEAN) and GW-27 (second proof). Open: the primary regime for a ≥ 7 with a low unit
  violating LOW+, and 5m ≤ M ≤ 6m − 4. The primary
  regime is Wilf for 3m < c ≤ 4m, which is OPEN in the literature (LITERATURE item 22).
  - Theorem H does not extend to i = 4 without residues: {|x| ≤ 3} ⊂ ℕ², n = (16,17), m = 10, M = 51 ≥ 5m − 1
    gives 27 > 26.
  - The class-face splitting of the band proof also fails at K = 4 (E200).
- A proof by induction on i must move mass across depths, because the per-depth inequalities are false.

---------------------------------------------------------------------------------------------------
## Theorem LAYER-KNESER (LK) — PROVED 2026-10-19 (paper; exhaustive check genus ≤ 33, E271); (a) and prime-m (b) KERNEL-CHECKED
Setting. S a numerical semigroup with multiplicity m ≥ 2 and conductor c > m. Put D = ⌈c/m⌉, so (D−1)m < c ≤ Dm,
and c = (D−1)m + c′ with 1 ≤ c′ ≤ m. Let B = {0} ∪ {s − m : s ∈ S, m < s < 2m} ⊂ ℤ/m and k = |B| − 1, the number of
elements of S in (m, 2m). These are all primitive, so e ≥ k + 1. For H ≥ 0 let G_H = {r ∈ [0, m) : Hm + r ∉ S}
(the gap residues of band H) and g_H = |G_H|.

**Statement.**
- (a) Always: ℓ(S) ≥ D + (D−2)k.
- (b) If k ≥ 1 and gcd(m, B) = 1, then ℓ(S) ≥ D + (D−2)k + δ·⌊(D−3)²/4⌋, where δ = k if m is prime and
  δ = ⌈(k+1)/2⌉ otherwise.
- Hence Wilf holds whenever e·[D + (D−2)k + δ⌊(D−3)²/4⌋] ≥ c. In particular it holds whenever
  (k+1)·[D + (D−2)k + δ⌊(D−3)²/4⌋] ≥ Dm, asymptotically when D ≳ 8m/(k+1)² (general m) or D ≳ 4m/k² (m prime).

**Proof.**
1. G_{H+1} ⊆ G_H, since S + m ⊆ S. Also 0 ∉ G_H, g_0 = m − 1, g_1 = m − 1 − k. G_{D−1} ≠ ∅ (it contains the residue
   of the Frobenius number), and G_{D−1} ⊆ [1, c′), so g_{D−1} ≤ c′ − 1. G_H = ∅ for H ≥ D.
2. (Shift inclusion) G_{H+2} − B ⊆ G_H in ℤ/m. Let r ∈ G_{H+2} and b ∈ B. If r − b mod m were in R_H := [0,m) ∖ G_H,
   then Hm + ((r − b) mod m) ∈ S. Adding m + b ∈ S gives (H+1)m + r when r ≥ b, which is in S, so r ∈ R_{H+1} ⊆ R_{H+2};
   when r < b it gives (H+2)m + r ∈ S. Either way r ∉ G_{H+2}, a contradiction.
3. (Growth) If G_{H+2} ≠ ∅ (i.e. H + 2 ≤ D − 1), then g_H ≥ g_{H+2} + δ under the hypothesis of (b).
   - Put X = G_{H+2} and Y = −B. Then X + Y ⊆ G_H ⊊ ℤ/m, because 0 ∉ G_H.
   - m prime: Cauchy–Davenport gives |X + Y| ≥ min(m, |X| + k) = |X| + k.
   - General m: Kneser gives |X + Y| ≥ |X + K| + |Y + K| − |K|, with K = Stab(X + Y), a proper subgroup.
     - If K = {0}, the gain is |Y| − 1 = k.
     - Otherwise Y ⊄ K: B generates ℤ/m since gcd(m, B) = 1. As 0 ∈ Y, Y meets β ≥ 2 cosets of K, so
       |Y + K| − |K| = (β−1)|K| ≥ β|K|/2 ≥ |Y|/2 = (k+1)/2.
4. Chaining over odd indices from g_1, together with monotonicity (step 1): g_H ≤ m − 1 − k − ⌊(H−1)/2⌋·δ for
   1 ≤ H ≤ D − 1. For (a), use only g_H ≤ g_1 = m − 1 − k.
5. Then ℓ = c − Σ_{H=0}^{D−1} g_H ≥ (D−1)m + c′ − (m−1) − Σ_{H=1}^{D−2}(m − 1 − k − ⌊(H−1)/2⌋δ) − (c′ − 1)
   = D + (D−2)k + δ·Σ_{j=0}^{D−3}⌊j/2⌋ = D + (D−2)k + δ⌊(D−3)²/4⌋. ∎

**Priority correction (2026-10-19, latest++; LITERATURE item 46).** Part (a) is contained in Yang–Zhang, Preprints.org
202604.0551 (8 Apr 2026), Prop 3.1: ℓ ≥ q + (q−2)η + η_ρ, which is stronger by η_ρ = |S ∩ (m, 2m−ρ)|. Their Prop 2.4/5.2
is the exact band formula used in step 5. So (a) is NOT new. The growth step 3 and part (b) are not in their paper,
and neither is the combination LK+YZ below. The original text follows, unchanged.

**Relation to the literature** (search 2026-10-19, LITERATURE.md; part (a) SUPERSEDED by the correction above).
- Delgado–Kumar–Marion (arXiv 2501.04417v3, Thm 1.5) prove ℓ ≥ (d−2)k and conclude Wilf when k ≥ √(dm/(d−2)).
  (a) contains that count, so LK strictly contains their Theorem 1.5. The Kneser term is new as far as we can find:
  no Cauchy–Davenport or Kneser argument for Wilf turned up.
- Their open Problem 1.8 asks whether every S whose largest minimal generator is < 2m satisfies Wilf. LK settles
  the slow-growth (deep) part of that class.
- LK uses only the residues of S ∩ (m, 2m). It does not need the other generators to be < 2m.

Checks.
- Exhaustive: every numerical semigroup of genus ≤ 33 (24.9M at genus 33), src/scratch/p18/lk_tree.c. The step
  inequality and (b) have 0 failures, min(ℓ − bound) = 0 (sharp).
- Random: 2,549 S with m ≤ 150 (layer_kneser.py).
- New coverage (lk_novel.py): 60 of 398 structured S (generators m + A*, A* a random subset of a short interval,
  sometimes with extra higher generators) satisfy LK and none of c ≤ 3m, 3e ≥ m, m ≤ 18, DKM Thm 1.5 / Cor 1.6,
  Kaplan's 2g < 3m, the type bound t ≤ e − 1, or symmetry. Example: m = 150, gens 153–159, 161, 163, e = 10, c = 1803,
  type 10.
**LEAN (kernel-checked 2026-10-19, lean/Wilf/LayerKneser.lean; axioms propext, Classical.choice, Quot.sound; no sorry).**
The Lean statements hold for **any** m ∈ S with m > 0, not only the multiplicity. Band 0 then only satisfies g_0 ≤ m − 1,
which is all step 5 uses. With q = D − 1 ≥ 1, q·m < c ≤ (q+1)·m, k = #lowRes m = |S ∩ (m, 2m)|:
- `ell_ge_layer_basic`: q + 1 + (q−1)k ≤ ℓ. This is (a), with no primality assumption and no upper bound on c needed.
- `ell_ge_layer_prime` (m prime): q + 1 + (q−1)k + k·Σ_{j<q−1}⌊j/2⌋ ≤ ℓ. This is (b) with δ = k. For prime m,
  "k ≥ 1 and gcd(m, B) = 1" is automatic or vacuous: k = 0 makes the extra term 0.
- `wilf_of_layer_prime`: c ≤ e·(that bound) ⇒ Wilf. `ell_ge_layer_multiplicity`: the m = multiplicity instance.
- Ingredients: `shift_mem` (step 2) and `card_bandGaps_step` (step 3, via Mathlib `ZMod.cauchy_davenport`).
- The general-m Kneser case (δ = ⌈(k+1)/2⌉) is NOT formalized, because Kneser's theorem is not in Mathlib. It stays at
  "proved on paper; Kneser cited".


## Theorem LK-SUPER (band superadditivity, every band) — PROVED 2026-10-19 (paper; exhaustive genus ≤ 33, E275)
Setting: S any numerical semigroup, m ∈ S with m > 0 (e.g. the multiplicity), c > m, q = ⌈c/m⌉, ρ = qm − c.
R_j = {r < m : jm + r ∈ S}, u_j = |R_j|, G_j = [0, m) ∖ R_j, g_j = |G_j|, Θ_j = u_j − 1.

**Statement.**
- (a) (Shift inclusion, every band.) For all H, j ≥ 0: G_{H+j+1} − R_j ⊆ G_H in ℤ/m.
- (b) (Step.) If u_j ≥ 2, gcd(m, R_j) = 1 and G_{H+j+1} ≠ ∅, then g_H ≥ g_{H+j+1} + δ_j, where δ_j = u_j − 1 for
  m prime and ⌈u_j/2⌉ in general.
- (c) (Superadditivity, m prime.) Θ_{a+b+1} ≥ Θ_a + Θ_b whenever a + b + 1 ≤ q − 1. Hence Θ_t ≥ ⌊(t+1)/(j+1)⌋·Θ_j for
  every j and every t ≤ q − 1. For general m, with gcd(m, R_j) = 1, the same holds with the first copy Θ_j and later
  copies δ_j.
- (d) (Wilf criterion.) With the exact formula ℓ = q + Σ_{t=1}^{q−2} Θ_t + Θ_{q−1} − ρ (YZ): Wilf holds whenever
  e·[q + Σ_{t=1}^{q−2} θ_t + max(0, θ_{q−1} − ρ)] ≥ c, for any lower bounds θ_t ≤ Θ_t from (c).
  In particular with j_0 = the first band containing a nonzero residue, θ_t = Θ_{j_0} + (⌊(t+1)/(j_0+1)⌋ − 1)δ_{j_0}
  for t ≥ j_0.

**Proof.**
- (a) Let r ∈ G_{H+j+1} and b ∈ R_j. If r ≥ b and Hm + (r − b) ∈ S, then adding jm + b ∈ S gives (H+j)m + r ∈ S, and so
  (H+j+1)m + r ∈ S. If r < b and Hm + (m + r − b) ∈ S, then adding jm + b gives (H+j+1)m + r ∈ S. Both contradict
  r ∈ G_{H+j+1}.
- (b) Kneser/Cauchy–Davenport exactly as in LK step 3, with X = G_{H+j+1}, Y = −R_j and X + Y ⊆ G_H ≠ ℤ/m (0 ∉ G_H).
  In the periodic case Y ⊄ K, because R_j generates ℤ/m and K is proper.
- (c) For m prime, (b) with H = a, j = b reads Θ_{a+b+1} ≥ Θ_a + Θ_b. Induct on t.
- (d) is (c) inserted in the exact formula. ∎
- LK is the case j = 1. LK-SUPER also covers semigroups with S ∩ (m, 2m) = ∅, where the first-layer methods (YZ, DKM,
  LK) give nothing.

Checks (E275):
- Exhaustive: (b), for every j and every S of genus ≤ 33 (src/scratch/p18/super_check.c): 65,568,154 step checks,
  0 failures, in both the prime and the general Kneser form. The (d) bound never exceeds ℓ.
- Coverage: on 1161 deep (q ≥ 4) semigroups with empty first layer, S = ⟨m, jm + A*, …⟩ with j ∈ {2,3}, A* a non-AP
  subset of a short interval, sometimes with higher generators (super_novel.py):
  - (d) with j_0 alone covers 701;
  - 421 are covered by (d) and by none of YZ, Eliahou/LIT (c ≤ 3m, 3e ≥ m, m ≤ 18), Kaplan 2g < 3m, type ≤ e − 1, or
    symmetric.
  - Example: ⟨137, 275, 276, 278, 280, 281, 282⟩, c = 4658 (q = 34), e = 7, ℓ = 2206, bound 1156.
- Literature: first-layer methods (DKM, YZ) need S ∩ (m,2m) ≠ ∅. We found no Kneser/Cauchy–Davenport band argument
  (searches of 2026-10-19, LITERATURE).
- **LEAN (kernel-checked 2026-10-19, lean/Wilf/LayerKneser.lean; standard axioms only):**
  - `shift_mem_band`, which is (a) for any m ∈ S;
  - `card_bandGaps_step_band`, which is (b) for prime m: #G_{H+j+1} + #R_j ≤ #G_H + 1;
  - `band_superadditive`, which is (c) for prime m: Θ_a + Θ_b ≤ Θ_{a+b+1}.
  The general-m Kneser form is paper only.

## Proposition VOL (cube-volume near-Wilf, universal) — PROVED 2026-10-19 (paper; random check E277)
Setting: any S with multiplicity m and c > m. Let q = ⌈c/m⌉, ρ = qm − c, d = e − 1, n_1, …, n_d the non-m minimal
generators, N = Σ n_i, and u_t = #{r : x_r ≤ t}.

**Statement.** u_t ≥ m·((t+1)m/Λ)^d for 0 ≤ t ≤ q − 1, where Λ = c + m − 1 + N. Consequently
- e·ℓ ≥ qm·(1 + (m − 1 + N)/(qm))^{−(e−1)} − eρ, and hence
- **W(S) = eℓ − c ≥ −(e − 1)·(m − 1 + ρ + Σ_i n_i).**

**Proof.**
1. Let D ⊆ ℕ^d be an Apéry factorization tile: a down-set with |D| = m and v(x) = Σ x_i n_i bijective onto Ap(S, m).
   Put D̃ = ∪_{x∈D} (x + [0,1]^d).
2. D̃ is a down-set of ℝ^d_{≥0}. If y′ ≤ y ∈ x + [0,1]^d, take x′_i = x_i when y′_i ≥ x_i and x′_i = ⌊y′_i⌋ otherwise.
   Then x′ ≤ x, so x′ ∈ D, and y′ ∈ x′ + [0,1]^d.
3. Therefore D̃ is star-shaped from 0. So f(λ) = vol(D̃ ∩ {v < λ}) satisfies f(λ)/λ^d non-increasing (scale by λ/λ′).
4. The cube at x contributes 0 to f(λ) if v(x) ≥ λ, and at most 1 otherwise. So u_t ≥ f((t+1)m).
5. Also f(Λ) = m, since max_{D̃} v = max Ap + N = c − 1 + m + N. Hence u_t ≥ m((t+1)m/Λ)^d.
6. Sum with the YZ exact formula ℓ = Σ_{t<q} u_t − ρ, and use Σ_{s=1}^{q} s^d ≥ q^{d+1}/(d+1) and Λ ≤ qm + m − 1 + N.
   Bernoulli's inequality gives the linear form. ∎
- Meaning: Wilf holds up to an additive error (e−1)(Σ n_i + m − 1 + ρ). Relative to c this is O(e²κ/q) when every
  generator is ≤ κm.
- This is the continuous scaling argument made rigorous with unit cubes. It is never exact. The whole difficulty of
  Wilf is the discrete correction of that size.
- It is much weaker than Wilf. Its value is as a universal structural inequality, which beats D'Anna–Moscariello's
  c ≤ q·e·ℓ when q is large and the generators are small. It is nearly tight for e = 2 (E277: ratio 1.0105 at ⟨117, 599⟩).

## Lemma LK-SHARP (no lost band: the wrap goes to a short top window) — PROVED 2026-10-19 (paper; exhaustive genus ≤ 33, E276)
Setting as in LK-SUPER, m the multiplicity. Let β_j = max R_j, W_j = [m − β_j, m), and
a_H(j) = #{r ∈ W_j : x_r = H} (the residues of the window whose Kunz coordinate is exactly H).

**Statement.** For H ≥ 1 with H + j ≤ q − 1, if u_j ≥ 2 and gcd(m, R_j) = 1:

    g_H + a_H(j) ≥ g_{H+j} + δ_j       (δ_j = u_j − 1 for m prime, ⌈u_j/2⌉ in general).

Equivalently Θ_{H+j} ≥ Θ_H + δ_j − a_H(j). Along a chain H = j, 2j, …, the corrections add up to at most
#{r ∈ W_j : x_r ≥ 1} ≤ β_j. Hence, for m prime, Θ_{sj} ≥ s(u_j − 1) − β_j. This is growth u_j − 1 per j bands, against
per j + 1 bands in LK-SUPER, at a one-time cost β_j.

**Proof.** Let r ∈ G_{H+j} and b ∈ R_j.
- If b ≤ r and r − b ∈ R_H: adding jm + b gives (H+j)m + r ∈ S, a contradiction. So r − b ∈ G_H.
- If b > r: the residue r − b + m lies in [m − β_j, m) = W_j. If it were in R_{H−1}, then (H−1)m + (r − b + m) + jm + b
  = (H+j)m + r ∈ S, a contradiction. So it lies in G_{H−1} ∩ W_j.
- Hence G_{H+j} − R_j ⊆ G_H ∪ (G_{H−1} ∩ W_j). This target has g_H + a_H(j) elements and misses 0.
- Cauchy–Davenport (Kneser for general m, as in LK) finishes. ∎

P18 form (j = 1, β = max B): Θ_t ≥ max(k + δ⌊(t−1)/2⌋, k + (t−1)δ − β), inserted in the YZ exact formula.
For B in an interval [0, k] this gives Θ_t ≥ (t−1)k, against the true tk.

**LEAN (kernel-checked 2026-10-19, LayerKneser.lean; standard axioms only):**
- `shift_mem_sharp`: the inclusion, for any m > 0 (m ∈ S is not even needed).
- `card_bandGaps_step_sharp`: the step for prime m ∈ S, with any β ≥ max R_j, written with H + 1 in place of H:
  #G_{H+1+j} + #R_j ≤ #G_{H+1} + #{x ∈ G_H ∖ G_{H+1} : x ≥ m − β} + 1.

Checks (E276): exhaustive genus ≤ 33, every j, 65,568,154 checks, 0 failures (prime and general forms;
src/scratch/p18/super_check.c). Coverage on the 996 structured P18 S of E272: LK-SHARP+YZ covers 610 (LK+YZ 545);
29 S are covered by it and by none of LK+YZ, the YZ criteria, DKM, LIT, Kaplan, FGH, or symmetric.

## Theorem LK+YZ (Kneser growth combined with the Yang–Zhang staircase) — PROVED 2026-10-19 (paper; exhaustive genus ≤ 34, E272)
Setting as in LK, with q = D = ⌈c/m⌉ ≥ 3, ρ = qm − c, η = k = |S∩(m,2m)|, η_ρ = |S ∩ (m, 2m−ρ)|,
Θ_t = #{1 ≤ i < m : tm + i ∈ S} = m − 1 − g_t, and Θ_{t,ρ} the same count restricted to i ≤ m − ρ − 1.

**Statement.** If η ≥ 1 and gcd(m, B) = 1, with δ as in LK (δ = η for m prime, ⌈(η+1)/2⌉ in general):

    ℓ ≥ q + (q−2)η + δ·⌊(q−3)²/4⌋ + max(η_ρ, η + δ·⌊(q−2)/2⌋ − ρ).

Hence Wilf holds whenever e times the right-hand side is ≥ c.

**Proof.**
1. (Exact formula; Yang–Zhang Prop 2.4/5.2, re-derived.) ℓ = q + Σ_{t=1}^{q−2} Θ_t + Θ_{q−1,ρ}. Residue class i ≥ 1 has
   max(0, q − x_i) left elements if i ≤ m−ρ−1, and max(0, q − 1 − x_i) otherwise. Write each as a sum of indicators [x_i ≤ t].
2. (LK step 4.) Θ_t = m − 1 − g_t ≥ η + δ⌊(t−1)/2⌋ for 1 ≤ t ≤ q − 1. Hence Σ_{t=1}^{q−2} Θ_t ≥ (q−2)η + δ⌊(q−3)²/4⌋.
3. (Last band.) Θ_{q−1,ρ} ≥ Θ_{1,ρ} = η_ρ by monotonicity. Also every residue i ≥ m − ρ is present in band q − 1, since
   (q−1)m + i ≥ c. So Θ_{q−1,ρ} = Θ_{q−1} − ρ ≥ η + δ⌊(q−2)/2⌋ − ρ. ∎
- It contains Yang–Zhang Prop 3.1 (δ = 0) and LK (b), which drops the last-band term.
- Checks (E272): exhaustive over all S of genus ≤ 34 (src/scratch/p18/yz_check.c). The exact formula, YZ Prop 3.1,
  the identity Θ_{q−1,ρ} = Θ_{q−1} − ρ and the LK+YZ bound have 0 failures; min(ℓ − bound) = 0.
- Coverage: on 996 structured S (yz_novel.py), 129 are covered by LK+YZ and by none of YZ Cor 3.3/4.2/4.5, DKM 1.5,
  Cor 1.6, LIT, Kaplan, type ≤ e − 1, symmetric.
- **LEAN (kernel-checked 2026-10-19, lean/Wilf/LayerKneser.lean; standard axioms only).** Valid for any m ∈ S (prime
  where stated), with q_Lean = q − 1, so that q_Lean·m < c ≤ (q_Lean + 1)·m:
  - `ell_ge_staircase`: YZ Prop 3.1, for any m ∈ S.
  - `ell_ge_lkyz_prime`: LK+YZ with the η_ρ last-band term.
  - `ell_ge_lkyz_prime'`: LK+YZ with the Kneser last-band term η + δ⌊(q−2)/2⌋ − ρ, stated as ℓ + ρ ≥ ….
  - Helpers: `genus_le_bands_full` (g ≤ Σ_{H≤q} #G_H) and `card_bandGaps_last`.


## Codex P9 (Problem 1.8: offset-sumset criteria) — PROVED 2026-10-19 (codex; every proof re-derived by the lead; E279)
Source: src/scratch/gw/p9/P9_REPORT.md (code in p9/). Setting P18: S = ⟨m, m+b : b ∈ A*⟩, B = {0} ∪ A* ⊂ [0, m),
e = |B| = k + 1, β = max B, gcd(m, B) = 1, g = gcd(A*), a = β/g, s_2 = |2B ∩ [0,m)|, s_j* = |jB| (integer sumsets),
c = qm − ρ.
- **SPAN-CONDUCTOR (C1).** c ≥ m⌈(m−1)/a⌉ + (g−1)(m−1). Hence m ≤ qa + 1, and m ≤ (q−1)a + 1 when ρ > 0.
  - Proof: the Apéry element in residue −g has offset sum g·u with u ≡ −1 (mod m), so u ≥ m − 1, and it needs
    ≥ (m−1)/a generators.
- **Band inputs.** R_1 = B and R_2 = 2B ∩ [0,m) (band 2 uses exactly two generators). TRANSPORT is our LK-SUPER with
  j = 2: G_{H+3} − R_2 ⊆ G_H. With the Kneser generating gain this gives Θ_{H+3} ≥ Θ_H + ⌈s_2/2⌉, and hence
  Θ_t ≥ s_2 − 1 + ⌈s_2/2⌉⌊(t−2)/3⌋ for 2 ≤ t ≤ q − 1 (P4).
- **PAIR-QUADRATIC.** For q ≥ 4 and k ≥ 2: ℓ ≥ q + s_2 q(q−1)/12 if ρ > 0, and ℓ ≥ q + s_2 q²/12 if ρ = 0.
  Proof: insert P4 into the YZ exact formula, then do an exact case check over q mod 3.
- **Theorem PAIR-SPAN12.** If 12a ≤ e·s_2, then Wilf holds. For q ≥ 4 and k ≥ 2, moreover W ≥ kq + ρ.
  Proof: combine PQ with C1/C3, so that e·s_2 q(q−1)/12 ≥ aq(q−1) ≥ qm − q.
- **MAXGEN-BLOCK (modulus N = m + β).** Suppose m > (2j−1)β.
  - The j-fold generator sums give C_j ⊆ R_{j−1}^{(N)} with |C_j| = |jB|.
  - C_j ∋ 0 generates ℤ/N, and it lies in an arc of width jβ < N/2.
  - |R_0^{(N)}| = e.
- **SHORT-ARC.** If C ∋ 0 generates ℤ/n and a translate lies in an interval of width < n/2, then |X − C| ≥ |X| + |C| − 1
  whenever X ≠ ∅ and X − C ≠ ℤ/n. This is Kneser plus a coset count: each coset of K meets the arc in ≤ ⌈h/2⌉ points,
  and (r−1)h ≥ r⌈h/2⌉ − 1. Without the width hypothesis it is false (ℤ/6, C = {0,1,3,4}, X = {0,3}).
- **INTEGRATED-BLOCK.** With D = ⌈c/N⌉ and n = D − j ≡ b (mod j):
  ℓ ≥ e + n + (|jB| − 1)·{D(D−j) + b(j−b)}/(2j).
- **Theorem SUMSET-MODULUS.** Let j ≥ 2 and T_j = e(|jB| − 1).
  - If m > (2j−1)β and T_j{m(m−1) − ja(m+β)} ≥ 2ja(m+β)² (SM-Q), then W ≥ e(e + D − j) ≥ 0.
  - A conductor-free sufficient condition (SM-L) is T_j > 2ja and m ≥ ⌈2jβ(T_j + 3a)/(T_j − 2ja)⌉.
  - Pair table (lead-checked, E279):
    - T_2/a ≥ 8 ⇒ m ≥ 9β suffices;
    - T_2/a ≥ 6 ⇒ m ≥ 14β;
    - T_2/a ≥ 5 ⇒ m ≥ 24β;
    - T_2/a ≥ 128/27 ⇒ m ≥ 31β.
  - Meaning: for every fixed offset set B with k ≥ 2, jB fills its hull for large j (density → 1 > 2/e), so some j has
    T_j > 2ja. Hence **Wilf holds for all m ≥ C_B·β**, a threshold LINEAR in the span. The previous general shifted-family
    threshold is O'Neill–Pelayo's m > β² (arXiv 1708.09527, Cor 4.6), as cited by codex and not re-read by the lead.
- **Explicit carried Sidon classes.** B_p = {2pi + (i² mod p) : 0 ≤ i < p}, p prime, so β = 2p(p−1) + 1 and all pair
  sums are distinct. ET-31: Wilf for p ≥ 17 and m ≥ 31β. ET-2 (via PS12): p ≥ 47 and m > 2β.
  - The subfamily m = 100β + 1 has 100 ≤ q ≤ 161 and carries, and it is outside NO-WRAP, LK+YZ, e(k+2) ≥ 2m, 3e ≥ m
    and m > β².
  - Yang–Zhang's higher-layer (Q,t) tests DO recognize every computed member (codex records this).
- **FALSE, preserved:**
  - Θ_{H+3} ≥ Θ_H + s_2 − 1 for composite m. Witness ⟨14, 17, 21, 24⟩, where 2B ∩ [0,14) is a union of three cosets of
    {0,7}.
  - ℓ ≥ q + s_2 q(q−1)/4. Witnesses ⟨6, 8, 9⟩ and ⟨4, 7⟩.
- **OPEN (codex's next lemma):** the full pair gain |R_{H+2}^{(N)}| − |R_H^{(N)}| ≥ |2B| − 1 at modulus N = m + β without
  m > 3β. It passed every test, but the abstract short-arc statement is false, so a proof must use the semigroup.
- Scope limit (lead): every hypothesis needs |jB| ≳ 2ja/e, i.e. B dense in its hull at some scale j with m > (2j−1)β.
  Generic P18 sets with large span (β ≈ m) and k ≪ √m are untouched. That fast-growth, near-free core is the
  extremal regime for Wilf in general.

## Theorem VOL-CORNER and Corollary VOL-MINK (deep regime, every e) — PROVED 2026-10-19 (paper; checks E281)
Setting: S ≠ ℕ with multiplicity m, minimal generators m < n_1 < … < n_d (e = d + 1 ≥ 3), N = Σ n_i, M = max Ap = c + m − 1,
Λ := M + N, T_λ := {y ∈ ℝ^d_{≥0} : y·n ≤ λ}, V := vol T_Λ = Λ^d/(d!·Πn_i), μ := m/V, σ := (1 − μ)^{1/d}, and
g(σ) := 1/(σ^{−1} + σ^{−2} + … + σ^{−d}) (increasing on (0,1)).

**Theorem VOL-CORNER.** If g(σ)·Λ ≥ (d−1)(N + m − 1)/2, then W(S) ≥ 0.

**Corollary VOL-MINK.**
- Always σ ≥ σ*_d, the least root in (0,1) of σ + (β_d(1−σ^d))^{1/d} = 1, where β_d = 2^d/C(2d,d).
- Hence Wilf holds whenever c + m − 1 + N ≥ K_d·(N + m − 1), with K_d = (d−1)/(2g(σ*_d)).
- K_d = 15.0, 69.6, 232.8, 675, 1807, 4599 for e = 3, …, 8. Asymptotically K_d ≈ (d−1)2^d·O(d^{0.3}) (table: src/scratch/p18/volmink_const.py).

**Proof.**
1. (Cubes.) Let D be a factorization tile and K = ∪_{x∈D}(x + [0,1]^d).
   - K is a down-set of ℝ^d_{≥0} (Prop VOL), vol K = m, and K ⊆ T_Λ.
   - ∫_K v = Σ_{Ap} w + mN/2.
2. (Wilf in moment form.) Selmer and c = M − m + 1 give Wilf ⟺ (d+1)Σ_{Ap} w ≤ dmM − (d−1)m(m−1)/2.
   By step 1 this is ⟺ (d+1)∫_K v ≤ dmΛ − (d−1)m(N + m − 1)/2.
3. (Corner lemma.) Let U ⊆ T_Λ be an up-set relative to T_Λ (y ∈ U, y ≤ y′ ∈ T_Λ ⇒ y′ ∈ U) with vol U = s^d·V. Then
   ∫_U v ≥ ∫_C v = s^d·V·Λ(1 − s/(d+1)), where C is a corner simplex y_0 + T_{sΛ} with v(y_0) = (1−s)Λ.
   - Proof: slice by H_t = {v = t}. Since U_t + (t′−t)Δ_1 ⊆ U_{t′}, Brunn–Minkowski in dimension d − 1 shows that
     a(t) = (|U_t|/|Δ_1|)^{1/(d−1)} has a(t) − t non-decreasing once U_t ≠ ∅.
   - Against the corner profile a_C(t) = (t − (1−s)Λ)_+, equal volumes force the start t_0 ≥ (1−s)Λ and a single
     crossing: a ≤ a_C before the crossing and a ≥ a_C after it. So U's mass sits at larger t than C's.
4. Apply step 3 to U = T_Λ ∖ K (an up-set of T_Λ, of volume (1−μ)V = σ^dV):
   ∫_K v ≤ dΛV/(d+1) − σ^dVΛ(1 − σ/(d+1)), i.e. (d+1)∫_K v ≤ mΛ(d − g(σ)).
   Inserted in step 2, this proves the Theorem.
5. (Minkowski, for the Corollary.)
   - Let λ_0 = min{x·n : x ∈ ℕ^d ∖ D}. Every x ∈ ℕ^d with x·n < λ_0 lies in D.
   - So the open convex symmetric body Q = {z : z⁺·n < λ_0, z⁻·n < λ_0} meets L = {z ∈ ℤ^d : z·n ≡ 0 (mod m)} only
     in 0: if z ∈ Q ∩ L, then z⁺ and z⁻ are elements of D with equal residues, so z = 0.
   - L has index m and vol Q = C(2d,d)·vol T_{λ_0}. Minkowski's first theorem gives vol T_{λ_0} ≤ β_d·m.
   - K misses the open orthant x* + (0,∞)^d at a minimizer x*, since every x ∈ D has some x_i < x*_i. Hence
     σ^d = vol(U)/V ≥ (1 − λ_0/Λ)^d and (λ_0/Λ)^d ≤ β_dμ = β_d(1 − σ^d), i.e. σ + (β_d(1−σ^d))^{1/d} ≥ 1, so σ ≥ σ*_d. ∎
- Checks (E281):
  - 4,069 random S, e = 3–6: step 4 (as B_disc ≥ mΛg − (d−1)mN/2) and the Minkowski bound hold everywhere. The worst
    margin is 0.006·mΛ, so the corner bound is nearly tight; the worst Minkowski ratio is 0.96.
- Reach (honest):
  - The data-dependent Theorem covers every random e = 3 and 70–78% of random e = 4 sampled with q ≥ 5.
  - It covers NO random e ≥ 5: there Λ/(N+m) ≈ 2.8, while g ≤ 1/d forces Λ ≥ d(d−1)(N+m)/2.
  - The uniform corollary is a very-deep-regime theorem (c ≳ 233(N + m) for e = 5). The binding loss is the cube
    discretization (d−1)(N+m−1)/2, not the geometry.

## Criterion RC, Lemma CHAIN-RES, and Conjecture CHAIN-WILF (Apéry-only, tile-free) — 2026-10-19 (lead)
Setting: S, m, n_1..n_d, d = e − 1, M = max Ap = F + m. For w ∈ Ap and each a, the a-chain of w is the maximal
progression in Ap with difference n_a through w; top_a(w) is its largest element. Write need := (d−1)m(m−1)/2.
- **Identity (CH′, tile-free; PROVED).** B := dmM − (d+1)Σ_{Ap} w = mW + need. Equivalently B = Σ_{(x,a)}(M − v(top_a x))
  over tile columns. Asserted on all S of genus ≤ 30.
- **Lemma CHAIN-RES (PROVED).** For each a, distinct a-chains have distinct residues of M − w modulo n_a. Proof: if
  w < w′ in Ap with w′ − w = j·n_a, then every w + i·n_a (0 ≤ i ≤ j) is in Ap, since w + in_a − m ∈ S would give
  w′ − m ∈ S. So w and w′ lie in one chain.
- **Chain bound (PROVED).** Tile columns are sub-progressions of Apéry chains, so
  B ≥ B_chain := Σ_a Σ_{w∈Ap}(M − top_a(w)) ≥ R := Σ_a Σ_{w∈Ap}((M − w) mod n_a).
  The second step holds because the residue mod n_a is constant along a chain and M − top ≥ 0.
- **Criterion RC (PROVED): R ≥ need ⇒ W ≥ 0.** **Criterion CH-CHAIN (PROVED): B_chain ≥ need ⇒ W ≥ 0.**
  - Both are exact (equality) on the two Wilf-equality families: e = 2, and T_{m,q} = ⟨m, qm+1, …, qm+m−1⟩, where
    R = B_chain = need = m(m−1)(m−2)/2.
  - Algebraic form: B_chain ≥ need ⟺ d·m·ℓ + m(m−1)/2 ≥ Σ_a n_a·P_a, where
    P_a = #{(w, w′) ∈ Ap² : w′ − w ∈ n_a·ℤ_{>0}}. Wilf itself is the same inequality with tile columns in place of
    chains: Σ_a n_a P_a^{tile} = Σ_{Ap} w.
  - Equivalently Σ_{t∈Ap} τ(t)(M − t) ≥ need, with τ(t) = Σ_{a: t+n_a ∉ Ap} (length of the a-chain ending at t). This is
    Tile-TOP′′ with Apéry chains in place of tile columns, hence stronger than Tile-TOP′′ for every tile.
- **Conjecture CHAIN-WILF: B_chain ≥ need for every S with c > 3m.** With Eliahou (c ≤ 3m), it would imply Wilf.
  **FALSE (2026-10-19, lead; E284).** Interval semigroups ⟨m, 2m+a, …, 2m+b⟩ at q = 5 break it. The smallest found is
  ⟨23, 54, 55, …, 61⟩ (e = 9, c = 100, q = 5, W = 89, ratio 0.987). The Kunz annealer first hit ⟨36, 82, …, 95⟩
  (B_chain = 7893 < need = 8190, W = 341). Both were recomputed from the generators by independent Python
  (src/scratch/p18/chain_interval.py). The ratio decreases with m: 0.815 (m = 44), 0.766 (60), 0.717 (100), 0.706 (130).
  Every failing interval has width ≈ m/3, so 3e ≥ m, which is already covered by Eliahou. Wilf holds there with a large
  margin (W ≈ 6.5m): the loss is in the step B_tile ≥ B_chain. Apéry chains of intervals run through many
  factorizations, so they are much longer than tile columns. PACK-W, which implies CHAIN-WILF, is false there too.
- **Conjecture CHAIN-H3 (2026-10-19, lead; the preferred repair).** If some Apéry element has least factorization
  length ≥ 3 (equivalently Ap(S,m) ⊄ {0} ∪ P ∪ (P+P), P = minimal generators other than m), then B_chain ≥ need.
  - Consequence (PROVED implication): CHAIN-H3 + Flat-MaxCL (Ap ⊆ {0} ∪ P ∪ (P+P) ⇒ Wilf; LEAN
    `wilf_of_apery_height_le_two`) ⇒ **Wilf for every S**. No depth or 3e < m condition is needed, and Eliahou is not
    used.
  - Evidence (E286):
    - genus ≤ 33: exactly 4 CHAIN failures overall, all at q ≤ 3 and all of height 2. The 1,768,572 semigroups of height
      ≥ 3 have 0 failures at every q; min ratio 1.3708 at ⟨16, 17, 26, 27, 28, 30⟩, c = 42.
    - Every interval failure (169 with m ≤ 40) has height 2, and so do all 61 failing one-generator perturbations. Every
      perturbation that creates a length-3 element has ratio ≥ 1.32.
    - The annealer failures ⟨36, 82..95⟩ and ⟨36, 82..92, 97⟩, and the m = 61 near-miss (ratio 1.082), all have height 2.
    - Height-penalized Kunz annealing (chain_kunz4.c, m = 24, 36, any e, q ≥ 4/5): min 1.205 / 1.264, no failure.
    - Near-T truncations ⟨m, m+β_1..m+β_k⟩ ∪ [K, ∞), k = 1, 2, 3: height-≥3 minima 1.2018 / 1.1199 / 1.0737 for
      m = 36 / 60 / 100 (k = 1), ≈ 1 + 7.3/m. So CHAIN-H3 is asymptotically tight near T_{m,q} (slack Θ(m²) against need
      Θ(m³)). A proof must be exact there.
  - Why height matters (heuristic, not a proof):
    - All observed failures are height-2 sets with many coincident 2-fold sums (b + b′ = b″ + b‴), so Apéry chains run
      through many factorizations and B_chain ≪ B_tile.
    - For a pure level-k generator set, a length-3 Apéry element must sit at level ≥ 3k, which raises M by ≥ m and every
      chain value with it.
  - Status: **FALSE** (2026-10-19 latest: ⟨53, 85..95⟩, height 3, ratio 0.99956; see "CHAIN-H3, CHAIN-M3 and
    CHAIN-WILF(3e<m) are FALSE" below). The genus ≤ 33 evidence above stands; the counterexamples have c ≥ 223.
- **The n_1 dichotomy (PROVED, 2026-10-19).** Let n_1 be the least minimal generator > m.
  - If M < 3n_1, every Apéry element has a factorization of length ≤ 2, hence Wilf by Flat-MaxCL (LEAN
    `wilf_of_apery_height_le_two`).
    Proof: factorizations of Apéry elements never use m. An element all of whose factorizations have length ≥ 3 is
    ≥ 3n_1 > M. ∎
  - So it suffices to prove Wilf on the class A := {S : M ≥ 3n_1}, which contains every S of Apéry height ≥ 3.
  - Spirito's hypothesis n_1 > (c+m)/3 is the special case M + 1 < 3n_1 of the first branch, without his extra
    conditions (cf. LITERATURE #24).
- **Conjecture REST-M3 (2026-10-19, lead; plan line 1).** If M ≥ 3n_1, then
      REST := Σ_{w ∈ Ap∖{0}} con(w) ≤ 0.
  - Equivalent count form (exact): REST = Σ_a n_a N_a − m·d·ℓ′, where N_a = #{(w, j) : w ∈ Ap∖{0}, j ≥ 1,
    w + j n_a ∈ Ap} = Σ_{w≠0} k_{w,a}, and ℓ′ = #{x ∈ S ∩ (0, c) : m ∤ x} = Σ_{w≠0} λ(w).
    Proof: con_a(w) = k_{w,a} n_a − mλ(w), and Σ_{w≠0} λ(w) counts the left elements in nonzero residues. ∎
    So REST-M3 ⟺ Σ_a n_a N_a ≤ d·m·ℓ′ on the class A.
  - **Implication (PROVED): REST-M3 ⇒ Wilf for every numerical semigroup.**
    - M < 3n_1: the dichotomy above.
    - M ≥ 3n_1: Δ = con(0) + REST ≤ con(0) ≤ d·s_0 ≤ d(m − 1), which is ≤ C2 when d ≤ m/2. Hence B_chain ≥ need and
      W ≥ 0 (criterion CH-CHAIN).
    - If d > m/2, then 2e > m, and Wilf is Sammartano 2012 Th. 18 (also Eliahou's 3e ≥ m).
    - Only Flat-MaxCL (LEAN), CH′/CH-CHAIN (PROVED) and Sammartano or Eliahou (cited) are used.
  - con(0) bound without citation (partial, PROVED): if the d tops top_a(0) are pairwise distinct, then
    Σ_a y_{0,a} ≥ C(d,2) (distinct residues mod m). This gives con(0) ≤ d(m−1) − C(d,2) ≤ C2 for every d ≤ m − 1.
    Ties k_a n_a = k_b n_b do occur.
    - con(0) ≤ C2 had 0 failures on all 63,754,402 S of genus ≤ 33, of which 1,687,244 have tied tops.
    - A proof with ties would remove the citation (OPEN).
  - Weaker sufficient form: REST ≤ C2 − con(0) on A.
  - Evidence (E288):
    - Exhaustive genus ≤ 33: all 18,416,677 S with M ≥ 3n_1 have REST < 0.
      - max REST/C2 = −0.1978 with 3e ≥ m (⟨14,15,23,24,26⟩);
      - max REST/C2 = −0.4487 with 3e < m (⟨13,16,17,18⟩).
    - Recomputed in the count form, independently (Dijkstra): identical values.
    - Kunz annealing on A: no REST > 0 (the annealer is weak at maximizing REST).
  - FALSE nearby statements, all failing with M < 3n_1:
    - REST ≤ 0 for all S. Counterexamples: ⟨13,18..22⟩ (+0.96·C2, q = 3); ⟨18,25..31⟩ (+1.72·C2); the q = 5
      CHAIN-failing intervals; ⟨19,21,22,26,27,29⟩ (+0.316·C2, 3e < m); the m = 61 level-2 near-miss (+0.202·C2).
    - Per element (PW0′, ⟨5,9,12⟩).
    - Per direction: codex P11, m = 4k+1, ⟨m, m+1..m+k⟩, direction m+k gives +6k² (in A, with REST < 0).
    - SC (y ↦ m on chains ending below c): 2 failures in A.
  - **UPDATE (2026-10-19, latest): REST-M3 is FALSE** (lead, E289). Level-1 intervals S = ⟨m, m+a, …, m+a+L−1⟩:
    - ⟨28, 45..50⟩: e = 7, 3e < m, M = 145 ≥ 3n_1 = 135, q = 5, REST = +85 = +0.2249·C2.
    - Also ⟨32, 39..45⟩ (q = 4, +0.095·C2), ⟨33, 53..59⟩ (+0.409), ⟨38, 61..68⟩ (+0.643).
    - Computed twice: chain walks (rest_int.c) and the count form (rest_check.py, Dijkstra from the generators).
    - These lie beyond the genus ≤ 33 tree (c ≥ 103).
  - Status: FALSE. The failure is not repairable on the class A: CHAIN itself fails there (next item).
- **CHAIN-H3, CHAIN-M3 and CHAIN-WILF(3e<m) are FALSE (2026-10-19, lead, E289).**
  - Smallest counterexample found: S = ⟨53, 85, 86, …, 95⟩.
    - e = 12, so 3e = 36 < 53; Apéry height 3; M = 275 ≥ 3n_1 = 255; c = 223, q = 5.
    - B_chain = 13,774 < need = 13,780.
    - Wilf is not threatened: W = 485.
    - Recomputed independently by Dijkstra (chain_interval.py) and by the DP height (m3_pert.stats).
  - The family a ≈ 0.6m, L ≈ 0.21m keeps failing and gets worse with m:
    - ratio 0.9777 (m = 58), 0.9593 (m = 89, ⟨89, 141..159⟩, e = 20), 0.8792 (m = 128);
    - e/m stays ≈ 0.21–0.23, so 3e < m throughout, and every member has height 3 and M ≥ 3n_1.
  - Depth profile, level-1 intervals with m = 60–140 (chain_intq.c):
    - CHAIN fails at q = 3 (33,599 cases), q = 4 (185; min 0.9529, e/m = 0.214) and q = 5 (425; min 0.8738);
    - 0 failures for q = 6..31, with min ratio 1.49 (q = 7), rising with q.
  - MaxCL (grlex tile) holds with a large margin on the same family (maxcl_int.py). The min slack over σ is
    0.85·m² (m = 28), 1.70·m² (m = 53), 3.44·m² (m = 89).
    So the loss is specific to Apéry chains switching factorizations. Tile columns (B_col = B exactly) do not lose it.
  - Consequence: every "B_chain ≥ need" criterion is dead on height ≥ 3, on 3e < m and on M ≥ 3n_1. Plan line 1 pivots
    (STATE).
- **Chain deficit vs factorization overlap (2026-10-19, lead; answers "can multiplicity quantify the compensation E?").**
  Notation: Z(v) = factorizations of v ∈ Ap by n_1..n_d (no m); ∨Z(v) their componentwise max (join);
  depth_a(v) = max{j : v − j n_a ∈ S}; E := B − B_chain (B = mW + need, CH′).
  - **JOIN IDENTITY (PROVED).** depth_a(v) = max_{x∈Z(v)} x_a, and
        E = Σ_{v∈Ap} (n·∨Z(v) − v) = Σ_v n·(∨Z(v) − x_v)   for any choice x_v ∈ Z(v).
    Each term is ≥ 0, and it is > 0 iff |Z(v)| ≥ 2 (distinct factorizations of one value are incomparable).
    So Wilf ⟺ B_chain + Σ_v (n·∨Z(v) − v) ≥ need.
    Proof: Ap is closed under ≤_S-predecessors, so v − j n_a ∈ S gives an m-free factorization y and y + j e_a ∈ Z(v).
    B − B_chain = Σ_a n_a Σ_v depth_a(v) − Σ_v v. ∎
    Checked: E == B − B_chain on all 63,754,318 S of genus ≤ 33 with e ≥ 3, and on every interval scanned (E290).
  - **TRADE BOUND (PROVED).** Let T_min be the ≤_S-minimal Apéry elements with ≥ 2 factorizations.
    - For b ∈ T_min, distinct factorizations have disjoint supports.
    - Every v ∈ Ap with b ≤_S v has n·∨Z(v) − v ≥ b. Hence E ≥ E_β := Σ_v max{b ∈ T_min : b ≤_S v}.
    - **Insufficient:** B_chain + E_β < need for intervals from m = 41 (q = 3, a ≈ L ≈ 0.38m).
      - Up to 810 such S at m = 150, min ratio 0.739.
      - E_β captures only ≈ 25% of E there.
  - **LOWER-COVER BOUND (PROVED).** Let U(v) = {a : v − n_a ∈ S}. Then E(v) ≥ E_U(v) := (Σ_{a∈U(v)} n_a − v)⁺, since
    depth_a ≥ 1 on U(v).
    - On the CHAIN-failing intervals, E_U ≈ 0.95–0.98·E, and E_U ≥ 3.04·(need − B_chain) for every CHAIN failure with
      m ≤ 150.
    - On the genus ≤ 33 CHAIN failures, even E_β ≥ 6.8·deficit.
  - **LINK DECOMPOSITION (PROVED, exact; checked).**
    - Definitions: ρ_a(v) = s_{v−n_a} − s_v ∈ {b_a, b_a − m} (b_a = n_a mod m) for each link v − n_a → v in Ap;
      P(v) = Σ_a depth_a(v) ρ_a(v), the chain mass landing at v; Λ_top = Σ_{w,a} λ(top_a(w)).
    - Then Δ = Σ_v P(v) − m·Λ_top.
    - **LOCAL BALANCE:** P(v) − E(v) = v − m·L1(v), with L1(v) := Σ_a depth_a(v)(λ(v − n_a) − λ(v)).
      Proof: M − (v − n_a) = (M − v) + n_a, so s_{v−n_a} − s_v − n_a = −m(λ(v−n_a) − λ(v)). ∎
    - Since every layer drop is ≥ 1: E(v) − P(v) ≥ m·|∨Z(v)| − v, where |∨Z(v)| = Σ_a depth_a(v).
      - For a unique factorization x, |∨Z| = |x| < v/m.
      - Overlap makes |∨Z(v)| exceed v/m, and then v pays for all chain mass landing on it.
    - Every interval CHAIN failure examined has its positive P concentrated on such overlap-rich landing points:
      ⟨45, 62..78⟩: layer 1 con = +5265 and layer 0 E = 15514; 43 of 45 elements are rich.
  - **Criteria, each ⇒ Wilf.** Status: CONJECTURE, 0 failures so far (E290).
    - CHAIN-U: B_chain + E_U ≥ need.
    - CHAIN-POOR: Σ_{v : m L1(v) < v} P(v) − mΛ_top ≤ C2.
    - WILF+: Σ_v (v − m L1(v))⁺ − mΛ_top ≤ C2. Wilf is the same sum without the positive part.
    - Equality in all three at ⟨m, m+1..2m−1⟩.
    - Evidence: intervals k ≤ 3, m ≤ 41 (31,950 S, 715 CHAIN failures); intervals k ≤ 2, m ≤ 150 (CHAIN-U);
      genus ≤ 24 (all three); genus ≤ 33 (CHAIN-U); Kunz annealing that minimizes CHAIN-U (min 1.26).
  - **Structural conclusion.**
    - The chain obstruction (CHAIN-H3/REST-M3 counterexamples) is entirely a multiplicity effect, and overlap pays for
      it locally.
    - On multiplicity-free (UF) Apéry sets, E = 0 and every criterion above coincides with the tile-column inequality,
      i.e. with Wilf itself.
    - So the chain + overlap route reduces exactly to the multiplicity-free core. That core is the tile (MaxCL /
      Tile-TOP'') problem. It gives no route around it, but it says where the difficulty lives.
- **Θ-form of Wilf (2026-10-19, lead; PROVED identity, checked).**
  - Definition: for v ∈ Ap, Θ(v) := λ(v) + L1(v) + Σ_a λ(top_a(v)), with L1(v) = Σ_a depth_a(v)(λ(v−n_a) − λ(v)).
  - Identity: Σ_{v∈Ap} Θ(v) = (d+1)ℓ.
    Proof: Σ_v λ(v) = ℓ. In each direction, Σ_w λ(w) = Σ_w λ(top_a(w)) + Σ_v depth_a(v)(λ(v−n_a) − λ(v)), because
    the layers telescope along chains. ∎
  - Hence Wilf ⟺ Σ_v (mΘ(v) − c) ≥ 0. Exactly: Σ_v (mΘ(v) − c) = m·W.
  - The terms equal c − mΘ(v) = β(v) − (m−1−s_v) − mΣ_aλ(top_a(v)), with β(v) = v − mL1(v) the local balance.
  - **Generators and 0 are never deficient (PROVED).** Θ(0) ≥ λ(0) ≥ q. For a generator n_a, L1(n_a) = λ(0) − λ(n_a),
    so Θ(n_a) ≥ λ(0) ≥ q ≥ c/m.
  - Data, genus ≤ 26 (1,950,367 S): identity exact; 22% of S have a deficient element. Every deficient element is
    decomposable: 744,091 in layer 0 ([c, M]) and 9 in layers 1–2.
    - 0's surplus alone covers all deficits except in 760 S; worst ⟨6,11,43⟩.
    - So in Θ-form, Wilf says the decomposable elements of the top window [c, M] are paid by the surpluses of 0, the
      generators and the deeper elements.
    - This is the same population as Eliahou's D_q. A comparison with his W_0 is still to do.
  - Per-element candidates, FALSE:
    - β(v) ≤ m−1−s_v fails in 477,205 S (worst ⟨7,13,36,37⟩).
    - Σβ⁺ ≤ C2 without the m·Λ_top credit fails in 5,685 S (⟨7,11,38⟩).
    So the deep-top credit Λ_top is essential.
  - Local flows, genus ≤ 24 (712,316 S; theta_flow.c):
    - FALSE: each deficient v splits c − mΘ(v) equally among its lower covers v − n_a, and each cover pays from its own
      surplus. Fails in 155,833 S; worst ⟨7,13,29,30⟩.
    - Nearly true: for every v, the total positive surplus of its lower covers is ≥ its deficit, ignoring sharing.
      Fails in only 72 S.
    So the surplus sits next to the deficits but is shared. A proof needs a global routing (Hall-type) argument, which
    brings back the global problem. Branch closed, with no new lemma.
  - With c = qm − ρ and λ(0) = q: mW = (d+1)ρ + m·Σ_{v∈{0}∪P} Σ_b λ(top_b(v)) + Σ_{v∈D_A}(mΘ(v) − c), where D_A is the
    set of decomposable Apéry elements. This is an exact Eliahou-type split. Comparing it with W_0 = |P∩L||L| − q|D_q| + ρ
    is open.
- **Theorem (large second generator, unconditional) — LEAN-CHECKED 2026-10-19 (lean/Wilf/LargeSecondGen.lean).**
  If 3n_1 ≥ c + m (n_1 the least minimal generator > m), then e·ℓ ≥ c.
  - Lean statements:
    - `wilf_of_aperyMax_lt_three_mul`: ∀ p ∈ P′, aperyMax < 3p ⇒ c ≤ e·ℓ;
    - `wilf_of_conductor_add_mult_le_three_mul`: ∀ p ∈ P′, c + m − 1 < 3p ⇒ c ≤ e·ℓ.
  - Proof: a factorization of an Apéry element of length ≥ 3 has value ≥ 3n_1 > max Ap, so every Apéry element has a
    factorization of length ≤ 2. Then apply `wilf_of_apery_height_le_two` (Flat-MaxCL).
  - Kernel check: axioms [propext, Classical.choice, Quot.sound], 0 sorry, full `lake build` OK on fejer.
  - Comparison: Spirito (arXiv 1710.09245; abstract checked 2026-10-19) assumes the strict a_2 > (c+m)/3 and obtains
    Wilf only when the multiplicity is bounded by a quadratic function of the embedding dimension. Delgado's survey,
    Prop 3.25, gives this as e ≥ 10 and m ≤ (8/25)e² + e/5 − 5/4.
    - Ours has no condition on m or e, and it includes the boundary 3n_1 = c + m.
    - Novelty: no such statement found in the dated searches (LITERATURE 2026-10-19). Not externally reviewed.
- **The n_1 dichotomy, general height (PROVED).** If M < (h+1)·n_1, then every Apéry element has a factorization of
  length ≤ h, so the grlex factorization tile has height ≤ h.
  - Hence MaxCL for tiles of height ≤ h ⇒ Wilf for every S with (h+1)·n_1 > c + m − 1.
  - h = 2 is PROVED (Flat-MaxCL, LEAN). It gives Wilf whenever 3n_1 > c + m − 1, i.e. n_1 > (c+m−1)/3, with no
    further condition. Spirito's #24 needs n_1 > (c+m)/3 together with e ≥ 10 and m ≤ (8/25)e² + ….
  - h = 3 would give n_1 > (c+m−1)/4; MaxCL at height 3 is partly proved (codex P6 residual, above).
- **Repaired Conjecture CHAIN-WILF(3e<m): B_chain ≥ need whenever c > 3m and 3e < m.** Together with Eliahou's
  theorems for c ≤ 3m and for 3e ≥ m, it would still imply Wilf.
  - Evidence so far:
    - genus ≤ 33 (all q ≥ 4: 0 failures for every e);
    - interval semigroups restricted to 3e < m: min ratio 1.49, 1.40, 1.35, 1.34 for m = 60, 80, 100, 130;
    - all Kunz-annealing failures have 3e ≥ m (e = 13, 15 at m = 36).
  - The 3e < m boundary campaign is E284.
  - Status: **FALSE** (2026-10-19 latest: ⟨53, 85..95⟩ has 3e = 36 < 53, q = 5, ratio 0.99956). Earlier note, kept:
    weakly supported. The 3e = m boundary of the interval family looks structural: q = 5 for an interval needs
    1- and 2-fold sums to cover almost all residues, which forces 3w ≈ m. That boundary need not hold for other
    families.
  - Evidence (E280): exhaustive over all S of genus ≤ 30 (src/scratch/p18/rc_tree.c).
    - Exactly ONE failure overall: ⟨15, 21, 22, 23, 24, 25, 26⟩, c = 36 = q·m − 9 with q = 3, ratio 0.962, W = 27.
    - 0 failures at q = 4 and at q ≥ 5, for every e.
  - Annealing at q ≥ 4 (m = 25–150, e = 3, 4, 5, 7): min 2B_chain/need = 3.70, 3.07, 2.54, 2.00. No failure.
  - Random q ≥ 5, e = 4–6, spread or clustered offsets: 100% covered, min ratio 1.92.
- RC alone (E280):
  - genus ≤ 30, q ≥ 5: 14 failures, all with e ≤ 5 and m ≤ 11 (arithmetic-like generators); 0 for e ≥ 6. At q = 4
    there are failures only for e ≤ 7.
  - Random e ≥ 5 with spread generators: 100% covered (worst R/need 1.19).
  - Clustered generators (small offset span: slow growth, effective dimension ≈ 1): RC FAILS robustly, ratio down to
    0.35 (e.g. ⟨104, 111, 114, 115, 116⟩, q = 11, W = 1238). There the quotient part n_a⌊(M − top)/n_a⌋ carries the
    margin.
  - So RC is the residue analogue of the fast-growth regime, complementary to the band/Kneser tools (slow growth).

### CHAIN-WILF in deficit form; the w = 0 term; packing variants (2026-10-19, lead)
Notation as above. For w ∈ Ap: s_w := (M − w) mod m, λ(w) := ⌊(M − w)/m⌋ (co-level), y_{w,a} := M − top_a(w). Layer
λ is Ap ∩ [c − λm, c − λm + m − 1]; L0 = Ap ∩ [c, M]. C2 := m(m−1)/2. Since c ∈ ((q−1)m, qm], λ(0) = q and
s_0 = r0 := M − qm ∈ [0, m−1].
- **Deficit form (PROVED, an identity).** B_chain = d·C2 − Δ, where Δ := Σ_{w,a}(s_w − y_{w,a}) = Σ_a n_aP_a − dmℓ.
  So CHAIN-WILF ⟺ Δ ≤ C2. Write Δ = Σ_w con(w), con(w) := Σ_a(s_w − y_{w,a}) = Σ_a(k_{w,a}n_a − mλ(w)), where k_{w,a}
  is the number of chain steps from w to top_a(w).
  - Only pairs with top_a(w) ∈ L0 can have s_w − y_{w,a} > 0, since otherwise y_{w,a} ≥ m > s_w. On T_{m,q} the whole
    deficit sits at w = 0: con(0) = Σ_a b_a = C2, and con(w) = 0 for w ≠ 0.
- **Lemma W0 (PROVED).** con(0) = Σ_a(k_a n_a − qm) ≤ d·r0 ≤ d(m−1), where k_a n_a is the largest multiple of n_a in
  Ap. Proof: k_a n_a ≤ M = qm + r0.
- **Corollary (PROVED; conditional on PW0′).** Suppose con(w) ≤ 0 for every w ≠ 0 (PW0′). Then Δ ≤ d(m−1). So if
  d ≤ m/2, CHAIN-WILF holds and W ≥ 0. Since d > m/2 means 2e > m + 2, the case d > m/2 is Sammartano's theorem (Wilf
  for 2e ≥ m; LITERATURE). Hence PW0′ for all S with q ≥ 4, plus Eliahou for c ≤ 3m, would imply Wilf's conjecture.
- **PW0′ is FALSE.** The smallest counterexample at q = 4 is ⟨5, 9, 12⟩, c = 17, w = 9, con(w) = 1 (genus 10).
  - Genus ≤ 33 at q = 4: failures for every e ≤ 10 (e.g. 20/63 at e = 3, 51/987,032 at e = 9, 20/1,291,439 at e = 10);
    0 for 11 ≤ e ≤ 20.
  - At q ≥ 5: failures only for e ≤ 7.
  - So positive deficits at w ≠ 0 must be cancelled globally.
- **PACK (Δ⁺ := Σ_{w,a} max(0, s_w − y_{w,a}) ≤ C2) is FALSE.**
  - q = 4: ⟨5, 8, 12⟩, c = 20, Δ⁺ = 14 > 10. Ratio C2/Δ⁺ goes down to 0.42 at q = 4 and 0.23 at q ≤ 3 (genus ≤ 33).
  - Cancellation between directions at the same w is essential.
- **PACK-A (Σ_a max(0, C2 − B_chain,a) ≤ C2) is FALSE.** q = 5: ⟨7, 18, 19, 34⟩, c = 32, 22 > 21.
- **Conjecture PACK-W: PW := Σ_w max(0, con(w)) ≤ C2 for every S with q ≥ 4.** It implies CHAIN-WILF, so it is
  FALSE: interval semigroups at q = 5 (E284). The evidence below is restricted to its range. Evidence:
  - E283: genus ≤ 33, 0 failures at q ≥ 4 (8,515,046 semigroups with e ≥ 3: 7,096,029 at q = 4, 1,419,017 at q ≥ 5).
  - E282: Kunz annealing that maximizes PW/C2 (m ≤ 50, q ≥ 4/5), 0 failures. PW/C2 → 1 only near T_{m,q}. For 3e < m it
    stays ≤ 0.35.
  - PACK-W fails at q ≤ 3 (e = 6..14, genus ≤ 33).
- **Layer-1 identity (PROVED).** Let I = [c − m, c − 1], L1 = Ap ∩ I, and G = ℕ \ S. Then
  Σ_{w∈L1} con(w) = Σ_a n_a·E_a − m·d·|L1|, where E_a := #{x ∈ S ∩ I : x + (n_a − m) ∈ I ∩ G}
  (so E_a = 0 unless n_a < 2m).
  Proof:
  - For w ∈ L1, w + 2n_a > M. If w + n_a ∈ Ap, its top is w + n_a ∈ L0 and the term is n_a − m. Otherwise top_a(w) = w
    and the term is −m. Hence con(w) = Σ_{a: w+n_a∈Ap} n_a − md.
  - w + n_a ∈ Ap ⟺ w + n_a − m ∉ S, which forces n_a < 2m and w + n_a − m ≤ F.
  - Conversely, if x ∈ S ∩ I and x + n_a − m ∉ S, then x ∈ Ap, since x − m ∈ S would give x + n_a − m ∈ S. □
- **Layer sums are not separately signed (E283).** At q = 4 there are positive layer sums:
  - λ = 1: up to 0.31·C2 (⟨10, 17, 18, 19, 24⟩);
  - λ = 2: up to 0.50·C2 (⟨12, 14, 27, 31, 32, 35⟩);
  - λ = 3: up to 0.42·C2 (⟨9, 10, 32, 34⟩).
  All of these have e ≤ 6. Random q = 4 semigroups with 3e < m and m = 40–120 have Δ ≤ −5.28·C2 (CHAIN ratio far
  above 1), with con(0) ≤ 0.26·C2.
- **Depth mechanism of the q ≤ 3 failure ⟨15, 21..26⟩ (c = 36).**
  - Layer 1 is exactly the generators, and their pairwise sums 42..50 are Apéry elements in L0.
  - So each generator escapes into L0 in almost every direction (con(21) = 6 + 7 + 8 − 15 + 10 + 11 = 27).
  - At q ≥ 4, layer-1 elements lie above 2m and are sums. By the layer-1 identity, escaping requires gaps x + n_a − m ∈ I
    for many a.

## Codex P10 (e = 5): Theorems B4 and B2 — VERIFIED by the lead 2026-10-19
Source: src/scratch/gw/p10/P10_REPORT.md (code and logs in src/scratch/gw/p10/). Setting: S = ⟨m, n_1 < n_2 < n_3 < n_4⟩
with e = 5. D ⊂ ℕ⁴ is an Apéry factorization down-set (|D| = m, x ↦ x·n bijective onto Ap). N_s / t_s count the cells /
maximal cells of support size s. h(x) is the height of D above x, H = Σ_x Σ_a h(top_a x), and R is the rank term of the
maximal-cell weights 4 + |y|.
- **(HC) [PROVED; = HCR].** mW ≥ (m+1)H + R − (3/2)m(m−1). Hence H ≥ 3m/2 ⇒ W ≥ 3.
- **Lemma BH2 [PROVED].** If N_4 = 0, then H ≥ 2m − (5/2)t_1 − (10/3)t_2 − 6t_3.
  - Proof: bound Σ(2 − H_x)_+. Maximal cells cost 2 each.
  - A non-maximal cell of support r ≤ 2 pays by its missing directions whose tops are maximal. These incidences are
    injective into (maximal cell of support r+1, positive coordinate).
  - A support-3 non-maximal cell with H_x < 2 has h = 1 and three maximal upper covers; there are ≤ t_3 of them.
- **Lemma BH3 [PROVED].** If N_3 = N_4 = 0, then H ≥ 3m − (15/4)t_1 − 6t_2.
- Antichain tools [PROVED, self-contained]: LYM, GAUSS (Σ_{max}(r + |y|) ≤ rn), TYPE2 (n ≥ a(a+1)/2), TYPE3
  (6n ≥ a(√(8a+1) + 3)), FACE-TYPE (12N_2 ≥ t_2² + 6t_2, 6N_3 ≥ t_3(√(2t_3+1) + 3)), DEG-HEIGHT (rΣh ≥ Σ|x|), G3
  (3H ≥ D_3(N_3; 4) when N_4 = 0), G3-CONT (H ≥ (N_3/4)(3N_3/2)^{1/3} − N_3/2, by the bathtub principle on four octants).
- **Theorem B4 [PROVED, analytic].** If some Apéry tile D has (1,1,1,1) ∉ D and m ≥ 22³ = 10,648, then W ≥ 3.
  - Proof: if N_3 ≥ 3m/8, G3-CONT gives H > 4N_3 ≥ 3m/2. Otherwise BH2 + TYPE-WEAK gives
    H ≥ 2m − 10 − (35/3)√m − (33/4)m^{2/3} > 3m/2, since the loss is < (739/1500)m.
  - **Intrinsic corollary:** n_1 + n_2 + n_3 + n_4 ≥ c + m and m ≥ 10,648 ⇒ Wilf (no Apéry element has all four
    directions, since Σn_i > M).
- **Theorem B2 [PROVED, analytic + exact certificates].** If some Apéry tile has every cell of support ≤ 2 and m ≥ 60,
  then W ≥ 1.
  - m ≥ 144: analytic, via BH3, R ≥ 3t(t−1), t ≤ √(12m) − 3 and the polynomial A144-POLY with positive coefficients.
  - 64 ≤ m ≤ 143: count-profile certificate FIN64, using AXIS-FACE: H ≥ D_2(N_2; f) + J_12(3N_1 − N_2 − f).
  - 60 ≤ m ≤ 63: placed-face certificate (§10: axis lengths ℓ_i, maximal-axis set J, concavity of the rank term).
  - **Intrinsic corollary:** n_1 + n_2 + n_3 ≥ c + m and m ≥ 60 ⇒ Wilf.
  - Non-vacuous at unbounded m and height: S_N = ⟨N(N+2), 2m−N−1, 2m−1, (4N−4)m+1, (4N−4)m+1+N⟩ has q = 4N − 4,
    3e < m and NO-WRAP failing.
- **Lead verification (E285).**
  - Paper re-derivation of HC, BH2, BH3, LYM/TYPE2/TYPE3/FACE-TYPE, DH, G3, G3-CONT, the B4 arithmetic, AXIS-FACE and
    the A144 algebra. No gap found.
  - Independent re-implementations of FIN64 and of §10 reproduce codex's profile counts, minima and minimizing tuples
    exactly. sympy confirms A144-POLY.
  - 1,228 actual e = 5 lex tiles (237 support-two, 824 with N_4 = 0, codex's L-family): 0 violations.
- Novelty check (2026-10-19): the literature has e ≤ 4 and families. Spirito (1710.09245) needs e ≥ 10.
  Hellus–Rechenauer–Waldi (Semigroup Forum 97, 2018) construct one special e = 5 family of arbitrarily high type (full
  text not available to us). No hypothesis class of the B2/B4 form was found.
- Remaining e = 5 (after all project results): m ≥ 40, q ≥ 5, height ≥ 4, and one of:
  - (1,1,1,1) ∈ D for every tile (unbounded m);
  - a boundary tile with a positive three-face, 40 ≤ m ≤ 10,647;
  - support-two with 40 ≤ m ≤ 59 (828 relaxed profiles at m = 59).
  The next lemma, FULL-INTERIOR H(D) + 7|max D| ≥ 2|D| for lattice tiles, is OPEN. Its finite census is slack-positive
  (min 16, m ≤ 39) and it would imply Wilf for m ≥ 409,771 via TYPE4.

## Codex P11 (3m < c ≤ 4m, primary regime): Theorems A, A1, B, C — RECEIVED 2026-10-19, PARTIALLY reviewed
Source: src/scratch/gw/p11/P11_REPORT.md (code, results and checksums in p11/). Notation as in GW-21/24/26:
- α = number of low A directions, a = number of A directions, b = number of B directions;
- κ = size of a vertex cover of the absent A pairs, r_LL = missing low–low pairs, j_L, l as in the report;
- d_0 = max{l + j_L, b, ⌈(κ + r_LL + b)/2⌉};
- G = a bound on the number of squarefree triple-sum fibres of size ≥ 11 on the repaired offset set.
- Theorem A: α ≥ 6, n_0 ≥ C(α+1,2)/2 and a ≥ 13(α + d_0 + G + 22) ⇒ W ≥ 0.
- Corollary A1: with a ≥ 20 r_LL added, the condition on n_0 can be dropped (via LARGE-A′).
- Theorem B: α ≥ 1280(d_0 + G + 1) and a ≥ 3α ⇒ W ≥ 0.
- Theorem C: r_A = l = b = 0 and α ≥ 1140 + 9G ⇒ W ≥ 0. This improves BFREE-LIGHT from 1910 to 1140.
- Correction accepted: the co-Kunz RC term is n·Σ_s ⌈(λ(s)b − s)/n⌉ − bℓ. The indicator form is only a bound.
  Witness: ⟨5,9,12⟩, n = 9.
- Lead review so far: the margin polynomial in (18), (13(A−3)² + 51(A−3) + 20)/6; the completed square in (23); and
  the cubic certificate in (24) were re-derived by hand. The (19) packing argument was read and is plausible.
- NOT yet re-derived: the I-LOW substitutions (12)–(13), the localized bound C_H, and the GW-26 transfer W ≥ W_A.
  Status: RECEIVED; not to be cited as verified.
- Residual unchanged in shape: α ≥ 6, 19 ≤ a < 10·C(α+1,2), 3e < m, m ≥ 211, failing A, B and C.

## Codex P12 (REST-M3): REFUTED — received 2026-10-19, lead-checked numerically
- REST-M3 counterexample (agrees with the lead): ⟨32,39..45⟩, REST = 6095 − 32·7·27 = 47.
- Infinite family S_k = ⟨5k+2, 6k+3..7k+3⟩ (depth 4, height 3, 3e < m, M ≥ 3n_1). Codex proves:
  - REST > 0 for k ≥ 6;
  - Δ > C2 (CHAIN fails) for k ≥ 17;
  - W = 4k² − k + 7.
  Lead re-check, k = 4..21, via linkpay.py and chain_interval.py:
  - Δ − C2 = 178 at k = 17, and ≤ −62 for k ≤ 16;
  - the W formula holds at every k;
  - CHAIN-U ratio ≈ 2.0–2.1 throughout.
  Codex's symbolic certificate (gw/p12/certificate.py) has not been re-derived by the lead.
- Codex also proves: adding r generators just above m gives counterexamples with M ≥ 4n_1 for k ≥ 100(r+1).
  Scope (corrected by codex P13): these families have M/n_1 → 21/5, so they rule out every threshold M ≥ κ·n_1 with
  κ < 21/5 (in particular κ = 4), not every fixed κ.

## Codex P13 (depth four, 3m < c ≤ 4m): K-identity, MF-UNIT, critical classification — RECEIVED 2026-10-19; core VERIFIED by the lead
Source: src/scratch/gw/p13/P13_REPORT.md (code and results in p13/). Notation: M = 4m + h − 1, c = 3m + h, 1 ≤ h ≤ m,
ρ = m − h, λ(v) = ⌊(M − v)/m⌋, s(v) = (M − v) mod m, L1(v) = Σ_a depth_a(v)(λ(v − n_a) − λ(v)), Λ = Σ_{w,a} λ(top_a(w)).
Unit classes by co-level: A (m < n < m + h, λ = 3), B (λ = 2), C (λ = 1), E (c ≤ n ≤ M, λ = 0). UF/MF = one/several
factorizations over the non-m generators.
- **K-ID (PROVED, every depth; lead re-derived).** For any S with q = ⌈c/m⌉ and ρ = qm − c, put K(v) = q − λ(v) − L1(v).
  Then W = ρ + Λ − Σ_{v∈Ap} K(v). (Proof: Σ_v L1 = dℓ − Λ by telescoping each chain; Σ λ = ℓ.) K(0) = 0 and K = 0 at
  every primitive.
  - For UF v with factorization x of degree j, K(v) = (j−1)κ(x) − Σ_a x_a κ(x − e_a), where
    κ(y) = ⌊(Σ_a y_a s(n_a) − (|y|−1)s(0))/m⌋. This is the tile carry of WINDOW-H at the phase s(0) = M mod m (lead).
- **Theorem A (PROVED; lead re-derived every case).** At depth four K(v) ≤ 1 for every v ≠ 0, and every MF value has
  K ≤ −1 (MF-UNIT: λ + L1 ≥ 5, via disjoint remainders of degree ≥ 2 and the pair co-level table). K = 1 exactly at UF
  values of three types: a BB pair of co-level 1, a BC pair, or a cubic of co-level 0 all of whose pair divisors have
  co-level 1 (factors in A ∪ B).
- **Short arc (PROVED; lead re-derived).** Every critical value other than a pure-A cubic has s(v) < ρ, so R_out ≤ ρ.
- **Theorem B / Corollary C / Theorem C2 / Theorem D (PROVED; lead re-derived).** With R = #{K = 1}, Z = Σ(−K)⁺,
  C_U = Σ_{MF} max(1, λ + |U| − 4), F_M = #MF, p_A = #pair faces of critical pure-A cubics, a = #A:
  W = ρ + Λ − R + Z; W ≥ Λ + C_U + p_A − R_A; 3R_A ≤ (a+2)p_A; F_M + R_A + p_A ≤ m − 1 − d. Hence Wilf when
  R_A ≤ Λ + C_U + p_A, when 2(a+2)F_M ≥ (a−1)(m − e), or when m(R − Λ) ≤ ρ(m + h − 1)/2 (then also WILF+ = CHAIN-POOR).
- **Lead independent check (E292, src/scratch/p21/d4_check.c, own code).** Every statement above asserted on all
  4,408,415 depth-four semigroups of genus ≤ 32, on all 97,433 depth-four level-1 intervals with m ≤ 150, and on random
  Sidon-type A-offset families: 0 failures.
- Preserved failures (codex): E_U(v) ≥ P(v) per MF value fails at ⟨8,10,11,12⟩ (v = 33: E_U = 0, P = 15); MF-UNIT is
  sharp (two units per MF value fail there); T_{m,4} gives equality in all three criteria for every m.
- Open (codex's next lemma): UF-RELAY, R_A ≤ Λ + C_U + p_A, on the residual α ≥ 6, 19 ≤ a < 10·C(α+1,2), 3e < m,
  m ≥ 211. It would close c ≤ 4m.

### Corollary DEPTH4-EH (lead, 2026-10-19) — PROVED from Theorem A and K-ID
**Statement.** If 3m < c ≤ 4m, then W(S) ≥ e − (c − 3m) + Λ + Z. In particular **Wilf holds whenever c ≤ 3m + e.**
**Proof.** By Theorem A, Σ_v K(v) = R − Z with R the number of K = 1 values. Critical values are decomposable, and 0 and
the d primitives have K = 0, so R ≤ m − 1 − d. Then W = ρ + Λ − R + Z ≥ (m − h) − (m − 1 − d) + Λ + Z = e − h + Λ + Z. ∎
- Tight: W = e − h at m = 10, c = 32, ⟨10, 32..39, 41⟩ (W = 8, h = 2, Λ = Z = 0).
- Exact arc form (PROVED the same way, using the short arc and s ≤ m − 1 − ⌈h/2⌉ for critical pure-A cubics, from
  T = t_a + t_b + t_c ≥ ⌈3h/2⌉): W = Λ + Z + N_low − ⌊h/2⌋, N_low = #{v : K(v) ≤ 0, s(v) ≤ m − 1 − ⌈h/2⌉}.
- Per E-generator, Λ_E = ℓ − 4 exactly (its chains are {0, n_E} and singletons). So any E generator gives Λ ≥ ℓ − 4.
- Checks (E292): the bound, the arc identity and Λ_E = ℓ − 4 have 0 failures at genus ≤ 28 (642,239 depth-four S).
- Literature (dated search 2026-10-19, LITERATURE): no statement of Wilf for c ≤ 3m + e was found; Eliahou's q ≤ 3 is
  the nearest. Novelty UNVERIFIED beyond that search.
- With Eliahou (3e ≥ m), every depth-four counterexample needs e < min(m/3, c − 3m).
- **Elementary proof of the Wilf consequence (no Theorem A needed), KERNEL-CHECKED.** Statement proved: if c > 3m
  (any depth), then **e·ℓ ≥ 3m + e**; hence Wilf for 3m < c ≤ 3m + e. Lean: `three_mul_add_embDim_le`,
  `wilf_of_conductor_le_three_mul_add_embDim` (lean/Wilf/DepthFour.lean; axioms propext, Classical.choice, Quot.sound;
  no sorry). Proof: λ(w) = ⌊(M−w)/m⌋, ℓ = Σ_{Ap} λ.
  (1) Column: for p ∈ P', Σ_w ν_p(w)λ(w−p) ≤ ℓ + Σ_w ν_p(w)λ(w) (reindex w ↦ w−p on ν_p ≥ 1; ν_p(w) ≤ ν_p(w−p)+1).
  (2) Pointwise: for a factorization f of w of length J, Σ_p ν_p(w)(λ(w−p) − λ(w)) ≥ Σ_q f_q(λ(w−q) − λ(w)).
      J ≥ 3: every generator exceeds m, so each drop is ≥ 1. J ≤ 2: m⌊x/m⌋ + m − 1 ≥ x at x_q = M−w+q, with M ≥ 4m.
      Result: λ(w) + L1(w) ≥ 3 + N(w), and ≥ 4 + N(w) for w ∈ {0} ∪ P'.
  (3) Sum over Ap: ℓ + dℓ + ΣN ≥ 3m + (d+1) + ΣN. ∎  Only M ≥ 4m is used, so the bound holds at every depth q ≥ 4;
  it is the q = 4 case of GEN-EH (e·ℓ ≥ (q−1)m + e). The same scheme gives, at depth q, only
  λ(w) + L1(w) − N(w) ≥ max(λ(w) + J, q + 1 − J), which is short of q − 1 for 3 ≤ J ≤ q − 2.

### Conjecture GEN-EH (lead, 2026-10-19) — CONJ; 0 failures at genus ≤ 26 (E293)
For every S with q = ⌈c/m⌉ ≥ 2: W(S) ≥ e − (c − (q−1)m). Equivalently Σ_v K(v)⁺ ≤ (m − 1 − d) + Λ + Z. It would give
Wilf for c ∈ ((q−1)m, (q−1)m + e] at every depth.
- At depth ≥ 5 the bound K ≤ 1 is FALSE: UF cubics with K = 2 exist (first at q = 5, e.g. ⟨11,18,21,30,31,34,37,38⟩;
  K = 3 at q = 7, ⟨8,14,15⟩). There the proof must pay K ≥ 2 values. The stronger W ≥ e − h + Λ + Z FAILS (3 S at
  q = 7, genus ≤ 26), but W ≥ e − h holds on all 1,950,367 S (e ≥ 3) of genus ≤ 26.

### Conjecture T1 (lead, 2026-10-20) — the K-sum bound at every shift. CONJ; 0 failures (E294)
**STATUS 2026-10-20: T1 is FALSE, including at the true shift (codex P15; lead-verified, E297).** S = ⟨13,22,23,50,51,60⟩
(m = 13, e = 6, c = 57, g = 41, q = 5, p* = 5): Σ_Ap K_{p*} = 8 > 7 = m − e, so W = 39 < 40 = e − h + Λ. Ap is UF (binary
cubic simplex in 22, 23 plus primitive spikes 50, 51, 60). Unbounded families with excess C(H−1, 2) at the true shift
(T1-H, q = 2H − 1, e = (m+3)/2) and C(k+1, 3) at depth five (B_3 cores) are PROVED in src/scratch/gw/p15/P15_REPORT.md
and checked for H ≤ 5. The lead's annealing finds independent failures with e = 5, 6 (⟨71,73,89,182,439⟩, p = 1, excess 4).
None of them is a Wilf counterexample (W ≥ 27), and GEN-EH (W ≥ e − h) is not refuted. No failure is known for e ≤ 4.
T1 holds at q ≤ 4 at p* (pointwise K ≤ 1). Every consequence below that assumes T1 at p* for q ≥ 5 is void.
**Setting.** m = multiplicity, Ap = Ap(S, m), P' = minimal generators other than m, d = |P'|, e = d + 1,
ν_a(x) = max{k : x − k n_a ∈ S}. For an integer p ∈ [1, m] let C_p(y) = #{z ∈ (0, y] : z ≡ p (mod m)} =
⌊(y − p)/m⌋ + 1 (y ≥ 0), and
    K_p(x) = C_p(x) − Σ_{a ∈ P'} ν_a(x)·(C_p(x) − C_p(x − n_a))    (x ∈ Ap).
With M = max Ap = qm + μ and p* = μ + 1 = ((c − 1) mod m) + 1, one has C_{p*}(v) = q − λ(v) and
C_{p*}(v − n_a) − C_{p*}(v) = λ(v − n_a) − λ(v), so K_{p*} is the K of the K-ID.
**Conjecture T1.** For every S and every p ∈ [1, m]: Σ_{x ∈ Ap} K_p(x) ≤ m − e.
**Implications (PROVED from the K-ID W = ρ + Λ − Σ_v K(v)).** T1 at p* is equivalent to W ≥ e − h + Λ, h = c − (q−1)m.
Hence T1 ⇒ GEN-EH, and T1 ⇒ (Wilf holds whenever h ≤ e + Λ). Under T1, a Wilf counterexample needs Λ < h − e < m − e.
**Equivalent forms (identities, PROVED).** Put J(x) = Σ_{a : x + n_a ∉ Ap}(ν_a(x) + 1) − e, top_a(x) = top of the a-chain of x.
- (Abel) Σ_x K_p(x) = e Σ_x C_p(x) − Σ_a Σ_x C_p(top_a(x)); and Σ_x J(x)g(x) = Σ_a Σ_x g(top_a(x)) − e Σ_x g(x) for any g.
- (J-form) T1(p) ⟺ Σ_{x ∈ Ap\{0}} J(x)·⌊(x − p)/m⌋ ≥ 0. Here Σ_{x≠0} J(x) = e − m < 0, so T1 says J correlates with level.
- (moment identity) Σ_{x ∈ Ap} J(x)·x = E := Σ_x (Σ_a ν_a(x) n_a − x) ≥ 0.
- (Kunz form) with k(x) = ⌊x/m⌋: T1(p) ⟺ Σ_x J(x)k(x) ≥ S_p := Σ_{x ≠ 0, x mod m < p} J(x). T1(p+1) slack = T1(p) slack − J(w_p).
- (gap form) Σ_{x≠0} ⌊(x−p)/m⌋ = #{gaps ≥ p}; T1(p) ⟺ Σ_a Σ_x [L(top_a x) − L(x)] ≥ d + #{gaps ≥ p}, L(y) = ⌊(y−p)/m⌋.
- (residue form) T1(p) ⟺ Σ_{x≠0} J(x)·((x − p) mod m) ≤ (m − e)p + E.
- (UF case: Ap = {Σ f_a n_a : f ∈ F}, F ⊂ ℕ^d an order ideal) T1(p) ⟺ Σ_{f ∈ F\0} J(f)⌊(Σ_a f_a r_a − p)/m⌋ ≥ 0
  (r_a = n_a mod m); the k_a cancel because Σ_f J(f) f_b = 0. Only the residues and the shape of F enter.
**Proved cases.**
- q ≤ 4 at p = p*: K ≤ 1 on decomposables and K = 0 on {0} ∪ P' (the pointwise bound of DepthFour.lean; for J ≥ 3 the
  drops are ≥ 1, for J ≤ 2 the floor inequality). Lean: `three_mul_add_embDim_le` is T1(p*) with Λ dropped, at q = 4.
- e = 2, every p, and every down-set {0, n, …, jn} (T1-DOWN below). Proof: Σ_{i ≤ j} K_p(in) = 2Σ_{i<j} C(in) − (j−1)C(jn),
  and C(u) + C(v) ≤ C(u + v) + 1 (floor inequality, uses 1 ≤ p ≤ m); pair i with j − i. ∎
**Facts found while testing.**
- Residue bijectivity is essential: the UF form fails for order ideals whose residues do not cover ℤ_m (E294).
- The combinatorial UF form (no Kunz/realizability condition) holds for every order ideal with bijective residues, d = 2
  (m ≤ 16) and d = 3 (m ≤ 11).
- Pointwise K_p ≤ 1 is false (K up to 4). Deficits are paid inside down-sets:
  **Conjecture T1-DOWN.** For every down-set D of (Ap, ≤_S): Σ_{x ∈ D, x decomposable}(K_p(x) − 1) ≤ 0.
  **T1-DOWN is REFUTED (external review 2026-10-20; lead-verified, E296).** S = ⟨20,33,36⟩ (genus 112), p = 6,
  D = {0,33,36,66,69,72,99,102,105,108,144} (a down-set of Ap; lex-max shape with column heights (5,3,2,1)):
  Σ_D K_6 = 9 > 8 = #dec(D). Same D in ⟨20,33,36,147⟩ (e = 4): 9 > 8. T1 holds on both full Apéry sets
  (Σ_Ap K_6 = 7 and 4; max_p Σ_Ap K_p = 10 against m − e = 17 and 16). The earlier evidence (genus ≤ 25) was too small.
  T1-DOWN ⟺ the deficits (K − 1)⁺ can be matched to credits (1 − K)⁺ of decomposables below them (Hall). Cover-only
  matching FAILS (⟨7,10,32⟩, p* = 2: credit at 30 must pay both 40 and 50).

### Lemma U (lead, 2026-10-20) — combinatorial core of T1. CONJ for d ≥ 2; PROVED for d = 1; reduction PROVED
**STATUS 2026-10-20: REFUTED for d ≥ 2 (external review; lead-verified, E296).** m = 83, r = (19, 18), p = 2, D the
order ideal with column heights (9,9,8,7,5,5,2,1) (46 cells, R injective mod 83): Σ_D K = 44 > 43 = #{|f| ≥ 2}.
**The full-tile repair U-FULL (|D| = m, R bijective) is also REFUTED (lead, E296):** the lex-max factorization ideal of
S = ⟨23,25,59,61,124⟩ (generator order 25, 61, 59, 124) is an order ideal with bijective residues and
Σ_D K_2 − #dec = +1 (d = 4). T1 itself holds there with slack 6 (Ap is not UF). Consequence: no proof of T1 can pass
through a single factorization ideal; the gain from ν ≥ f (the term E ≥ 0 below) is needed. The reduction below remains
correct as an implication but its hypothesis is false.
**Statement.** Let m ≥ 2, d ≥ 1, r ∈ [1, m−1]^d, p ∈ [1, m], C(y) = #{z ∈ (0, y] : z ≡ p (mod m)}. For f ∈ ℕ^d put
R(f) = Σ_a f_a r_a and K(f) = C(R(f)) − Σ_a f_a·(C(R(f)) − C(R(f) − r_a)) (terms with f_a = 0 vanish). Let D ⊂ ℕ^d be a
finite order ideal on which R is injective mod m. Then Σ_{f ∈ D} K(f) ≤ #{f ∈ D : |f| ≥ 2}.
(K(0) = K(e_a) = 0, so the claim is Σ_{f ∈ D, |f| ≥ 2}(K(f) − 1) ≤ 0.)
**Reduction (PROVED): Lemma U ⇒ T1-DOWN ⇒ T1 for every numerical semigroup.** Let f(x) be the lexicographically largest
factorization of x ∈ Ap over P'. (i) {f(x) : x ∈ D} is an order ideal for every down-set D of (Ap, ≤_S): if g ≤ f(x) and
y = Σ g_a n_a had a lex-larger factorization g′, then g′ + (f(x) − g) would be a lex-larger factorization of x. And y ≤_S x
gives y ∈ D. (ii) R(f(x)) ≡ x (mod m), so R is injective on f(D). (iii) C(y + km) = C(y) + k, so with n_a = k_a m + r_a,
K_p(x) computed with f(x) in place of ν(x) equals K(f(x)) of Lemma U (the k_a cancel). (iv) ν_a(x) ≥ f_a(x) and
C(x) − C(x − n_a) ≥ 0 give K_p(x) ≤ K(f(x)). (v) f(n_a) = e_a and f(0) = 0, so the decomposables correspond. ∎
**d = 1 (PROVED).** D = {0, …, t}: Σ_s K(s) = 2Σ_{0<s<t} C(sr) − (t−1)C(tr) ≤ t − 1 because C(u) + C(v) ≤ C(u+v) + 1.
(No injectivity is needed for d = 1.)
**Evidence (E295).** All order ideals with injective residues: d = 2, m ≤ 11 (every size); d = 3, m ≤ 9; 0 failures.
Injectivity is essential: dropping it, the claim fails (m = 3, D = {|f| ≤ 3}, r = (2, 2), p = 1, slack −1; with
|D| ≤ m it still fails at m = 10, r = (6, 6)).
**Equivalent forms.** (a) Cut form: Q(z) = #{f ∈ D : R(f) ≥ z} − Σ_a Σ_{a-lines ℓ of D straddling z} #{f ∈ ℓ : R(f) < z}.
Q(0+) = #dec(D), Q jumps by J(f) at R(f), ∫_0^∞ Q = 0, and Lemma U ⟺ Σ_{z ∈ p+mℤ, z>0} Q(z) ≤ Q(0+): every m-periodic
sampling of Q sums to at most its initial value. (b) Carry form: with c(u, v) = C(u+v) − C(u) − C(v) ∈ {−1, 0, 1},
Lemma U ⟺ Σ_f γ(f) − Σ_{a,f} β_a(f) ≤ #dec(D), where γ(f) = C(R(f)) − Σ_a C(f_a r_a) (axis-decomposition carries) and
β_a(f) = c(R(f), j_a(f) r_a) (climb carries to the a-top, j_a(f) = steps from f to its a-top in D).
**Stronger forms seen in data (CONJ).** TAIL: for every y > m, Σ_{z ≡ p, z ≥ y} Q(z) ≤ 0 on real Apéry sets (genus ≤ 18,
every p); sampled Q is not monotone (MONO fails), so TAIL is not a monotonicity statement.

### T1 and Wilf in residue and walk form — identities PROVED 2026-10-20 (lead; asserted numerically, E296)
(The identities I1–I5 are unconditional. I6 is conditional on T1, which is now known to be FALSE for q ≥ 5; the B*, B_1 data stay as facts.)
Notation as in Conjecture T1; res(y) ∈ [0, m−1] is y mod m; w_i is the Apéry element with w_i ≡ i; k(y) = ⌊y/m⌋;
E = Σ_{x ∈ Ap}(Σ_a ν_a(x) n_a − x) ≥ 0 (E ≥ 0 because every factorization f of x has f ≤ ν(x)); slack(p) = (m − e) − Σ_Ap K_p.
J(x) = Σ_{a : x + n_a ∉ Ap}(ν_a(x) + 1) − e and S_p = Σ_{0 < i < p} J(w_i) for p ∈ [1, m] (S_1 = 0, S_m = e − m).
- (I1, top-residue identity) m·slack(p) = E + mp + e·m(m − 3)/2 − Σ_{a ∈ P'} Σ_{x ∈ Ap} res(top_a(x) − p).
  Proof: C_p(y) = (y − p − res(y − p))/m + 1 for y ≥ 0; insert into the Abel form Σ K_p = e Σ_x C_p(x) − Σ_a Σ_x C_p(top_a x),
  use Σ_a Σ_x top_a(x) − e Σ_x x = E (line reversal: Σ_x j_a(x) = Σ_x ν_a(x) on each a-line) and Σ_x res(x − p) = m(m−1)/2. ∎
- (I2, mean slack) (1/m) Σ_{p=1}^{m} slack(p) = m − e + E/m. (Sum I1 over p; Σ_p res(y − p) = m(m−1)/2.) So T1 holds
  on average over shifts for every S; the conjecture is about how the slack is distributed over p.
- (I3, walk form) slack(p) = ΣJk − S_p (the J-form), so ΣJk = mean_p S_p + m − e + E/m and
  **T1(p) ⟺ S_p − mean_p S_p ≤ m − e + E/m.** Also S_p = T_{<p} − e(p − 1), T_{<p} = #{(a, y) : res(top_a(y)) ∈ [1, p−1]}.
- (I4, Wilf walk identity) **W(S) = ρ + Λ + E/m + mean_p S_p − S_{p*}**, i.e. Wilf ⟺ S_{p*} − mean_p S_p ≤ ρ + Λ + E/m.
  (From the K-ID W = ρ + Λ − Σ K_{p*} and I3.) T1(p*) is the same walk bound with m − e in place of ρ + Λ.
- (I5) T1(1) ⟺ Σ_a Σ_{x ∈ Ap}(k(top_a x) − k(x)) ≥ g. (At p = 1 the residue terms of I1 collapse: top_a(x) ≢ 0.)
- (I6, all shifts) Under T1 at every p, W ≥ B* := e − h + Λ + Ω with Ω = max_p S_p − S_{p*} ≥ 0. Under T1(p*) and T1(1),
  W ≥ max(B_h, B_1) with B_h = e − h + Λ and B_1 = B_h − S_{p*}. Both identities follow from W = e − h + Λ + ΣJk − S_{p*}.
**Data (E296).** B* ≥ 0 and max(B_h, B_1) ≥ 0 on all 23,663,048 S (e ≥ 3) of genus ≤ 31. So T1(p*) ∧ T1(1) ⇒ Wilf
in that range; B_1 < 0 in 66 S, B_h < 0 in 37 (LOW), never both. A crude sufficient condition (Λ ≥ h − e or
Σ_{x ∈ Ap ∩ [qm, M]}(|ν(x)| + d) ≤ dh) fails once (⟨9,14,15,17⟩).

### Depth four: blocked-extension bound L2 (PROVED), conjectures C1/C2, and the B_3-simplex model (lead, 2026-10-20)
Setting q = 4: M = 4m + h − 1, c = 3m + h, ρ = m − h, λ(v) = ⌊(M − v)/m⌋, d = e − 1, K as in the K-ID (K ≤ 1 pointwise, P13),
R = #{K = 1}, Z = Σ(−K)⁺. τ(y) = #{a ∈ P' : y + n_a ∉ Ap}, U(v) = {a ∈ P' : v − n_a ∈ S}, α_0 = #Ap ∩ [c, M].
DEC-ID (P14 §2.1): W = ρ + Λ + Z − R = (e − h + Λ + Z) + (m − e − R).
**Lemma B (PROVED).**
- (B1) Λ ≥ Σ_{y ∈ Ap, y < c} τ(y): an a-top y < c contributes (ν_a(y) + 1)λ(y) ≥ 1.
- (B2) Σ_{y ∈ Ap} τ(y) = Σ_{v ∈ Ap}(d − |U(v)|). The a-lines of Ap are counted once by their tops and once by their bottoms
  (x is an a-bottom iff x − n_a ∉ S); Ap is closed under S-divisors, so lines stay in Ap. Every v ≥ c is a top in all d
  directions (v + n_a > c + m − 1 = M), so Σ_{y<c} τ(y) = d(m − α_0) − Σ_v |U(v)|.
- (B3) For a ∈ U(v): ν_a(v) ≥ 1 and λ(v − n_a) − λ(v) ≥ 1 (n_a > m), so K(v) ≤ 4 − λ(v) − |U(v)| and Z ≥ Σ_v (λ + |U| − 4)⁺.
- Hence **Λ + Z ≥ L2 := Σ_{y<c} τ(y) + Σ_v (λ(v) + |U(v)| − 4)⁺ = d(m − α_0) − Σ_v min(|U(v)|, 4 − λ(v)).**
**Conjecture C2.** At q = 4: R ≤ ρ + Σ_{y ∈ Ap, y < c} τ(y) + Z. **Conjecture C1 (stronger):** R ≤ ρ + L2.
Each implies Wilf at q = 4, by DEC-ID and (B1). C1 ⟺ L2 + (m − e − R) ≥ h − e.
**Data (E298).** C1: 0 failures on all 2,733,043 depth-four S (e ≥ 3) of genus ≤ 31. On ⟨m, m+B⟩: exhaustive |B| = 3, m ≤ 34;
exhaustive |B| = 4, m ≤ 40; random to m = 300. Min slack 4, 10, 24, 305. L2 ≥ h − e alone is false (genus ≤ 31: 26 S, all e ≤ 4;
annealing: ⟨41,42,46,50,51⟩, e = 5, L2 = 27 < 36, with R = 0). Λ + Z < h − e occurs once at genus ≤ 31 (⟨9,19,21,22⟩, R = 0)
and, under annealing, only at m ≤ 25.
**B_3-simplex model (PROVED computation).** Suppose Ap = {0} ∪ (m + B) ∪ (2m + 2B) ∪ (3m + 3B) with B a k-set, m = C(k+3, 3),
pair sums at co-level 1 and cube sums at co-level 0. Then Λ = 0 (every line tops out at a cube), every pair has K = −1
(two drops of 2), and every cube has K = 1. So Z = C(k+1, 2), R = C(k+2, 3) and **W = ρ − C(k+1, 3)**. Also
ℓ = 4 + 3k + C(k+1, 2), and m = C(k+3, 3) is a direct check. In the model, C2 ⟺ Wilf and C1 ⟺ ρ ≥ C(k+2, 3).
Every cube lies in [c, M], so #cubes ≤ m. Wilf in the model ⟺ 3·max B ≤ 2m − 1 − C(k+1, 3). Interval packing of the C(k+2, 3)
distinct 3-sums in [3 min B, 3 max B], with 2 min B ≥ h, yields this up to an error of k + 1.
No such simplex exists for k ≤ 4 (exhaustive, src/scratch/p22/simplex4.py). Real depth-four extremal configurations
are near-simplices plus fillers (codex P14 residual); C1 is suspect there.

### Depth five: K-classification and the shifted cubic relay (lead, 2026-10-20) — PROVED; transfer of P14's graph lemmas
**ATTRIBUTION CORRECTION (same day):** this is NOT new. codex P14 §8.1 (src/scratch/gw/p14/P14_REPORT.md, 2026-10-19)
already proves the complete depth-five classification (K ≤ 2; MF ⇒ K ≤ 0; K = 2 only at UF co-level-0 cubics with
co-level-1 faces and factors in (m+h, 2m); s(v) < ⌊(m−h)/2⌋). P14 §8.2 gives the GEN-EH payment
D5-PAY: W ≥ e − h + Λ + p_5 + F_M − β. The lead's derivation below is an independent re-derivation of §8.1 and serves as
its verification; the census check E299 is new data for it.
Setting q = 5: c = 4m + h, M = 5m + h − 1, λ(n) = j ⟺ n ∈ [(4−j)m + h, (5−j)m + h − 1]. GEN-EH (W ≥ e − h) ⟺
Σ_{v decomposable}(1 − K(v)) + Λ ≥ 0, since W = ρ + Λ − ΣK and K = 0 at 0 and at generators.
**Proposition Q5 (PROVED).** At q = 5, K(v) ≤ 2 for every v ∈ Ap. K(v) = 2 iff v is a *critical B-cubic*: λ(v) = 0,
Σ_a ν_a(v) = 3, every drop λ(v − n_a) − λ(v) (a ∈ U(v)) equals 1, and every generator dividing v lies in [m + h, 2m).
Such v is UF (ν(v) is its unique factorization). Its pair faces lie in Ap at co-level 1 and have K = 0.
- Proof: for decomposable v, K = 5 − λ − Σ_a ν_a Δ_a with Δ_a ≥ 1 and Σν ≥ 2. K ≥ 2 forces λ ≤ 1.
  - λ = 1 needs a pair with drops (1, 1). Both factors are then at co-level 2, i.e. ≥ 2m + h, so the sum is ≥ 4m + 2h > 4m + h − 1. Impossible.
  - λ = 0 with Σν = 2: drops (1,1) or (1,2) put the factors at co-level ≥ 1 and ≥ 2. The sum is ≥ 5m + 2h > M. For v = 2n_i
    the contribution is 2Δ_i = 2λ(n_i) ≥ 4. So λ = 0 needs Σν = 3 with all drops 1, which gives K = 2. Σν ≥ 4 gives K ≤ 1.
  - Each pair face v − n_a has co-level 1. A factor n_k = v − (face) lies in (0, 2m). Pair sums are ≥ 3m + h, so each
    factor is > m + h.
  - Every factorization f satisfies f ≤ ν, and a length-2 factorization is too small (< 4m). So f = ν: UF. The faces are
    UF, and K(face) = 5 − 1 − (2 + 2) = 0. ∎
- Data (E299): all 456,221 S (e ≥ 3) with q = 5 of genus ≤ 31 contain 10,051 K = 2 values; 0 violations of the
  classification or of the face statement.
**Corollary Q5-RELAY.** At q = 5, GEN-EH ⟺ R_B ≤ Σ_{v dec, K ≤ 0}(1 − K(v)) + Λ, where R_B = #critical B-cubics. Each
distinct pair face gives one credit, so R_B ≤ p_B + Λ suffices (p_B = #distinct faces).
- This is the depth-four UF-RELAY shape (codex P14) shifted up one level: A/h becomes B/(m+h); "low" means 2t < m + h, where n = m + t.
- P14's GRAPH-ID, PSEUDO-RELAY and GRAPH-MAC transfer verbatim. Their inputs are only UF critical cubics, distinct
  Apéry faces, and the rule that no critical cubic has two low factor copies.
- Hence: **if every component of the critical-B-cubic face graph is a pseudoforest (or the cubics are squarefree in
  ≤ 5 directions), then GEN-EH holds at q = 5, and Wilf holds whenever 4m < c ≤ 4m + e.**
  (Pending: an independent re-check of the P14 graph lemma statements in this setting.)
- The obstruction at depth five is the same as at depth four: dense face graphs (B_3 cores, codex P15 U3-SHARP, excess
  C(k+1, 3)), where only Λ can pay. A **cubic relay lemma** paying R − p from Λ would give Wilf for c ≤ 4m (with C2) *and*
  for 4m < c ≤ 4m + e.

### Depth four: face-blocking payment, CE-DIRECTIONS′, and the shape of the residual (lead, 2026-10-20)
Notation of codex P14 §1–2 (q = 4; A, B, C, E classes; R_A = UF critical pure-A cubics; p_A = #distinct faces; R_out ≤ ρ (P13);
faces are UF with K = −1 (P14 §2.1)).
- **Face-blocking bound (PROVED).** Λ ≥ Σ_{p ∈ F} τ(p), F = set of faces, τ(p) = #{a : p + n_a ∉ Ap}. Each pair (p, a) with p an
  a-top below c is its own term (ν_a(p) + 1)λ(p) ≥ 1 of Λ. Every generator n ≥ 2m blocks every face, since
  p + n ≥ (2m + h) + 2m > M.
- **Charging form (PROVED).** W ≥ Σ_{p∈F}(1 + τ(p) − load(p)), where load(p) = Σ_{critical x with face p} 1/f(x) and f(x) =
  #distinct faces of x ∈ {1, 2, 3}. Also load(p) ≤ (u+1)/3 for p = n_i + n_j (i ≠ j), load(p) ≤ (u+1)/2 for p = 2n_i, with
  u = #critical cubics above p. This is only a reorganisation of DEC-ID with Z ≥ |F| and R − R_A ≤ ρ. Checked on all
  2,733,043 depth-four S of genus ≤ 31 (every link asserted, 0 failures; E300).
- **CE-DIRECTIONS′ (PROVED; small extension of codex P14 §2.3).** With g′ = #{minimal generators ≥ 2m} (C, E and the B
  generators in [2m, 2m+h)): Λ ≥ g′·p_A, so P14's argument (3R_A ≤ (a+2)p_A) gives **a ≤ 3g′ + 1 ⇒ Wilf at depth four.**
  (P14 had g = γ + η; the B generators in [2m, 2m+h) also block every face.) The lead's cruder FACE-BIG
  (g′ ≥ (d−1)/3 ⇒ Wilf) is subsumed.
- **Shape of the remaining depth-four case.** A depth-four counterexample has a ≥ 3g′ + 2 and fails CE-DIRECTIONS, so most
  generators lie below 2m. Yang–Zhang Cor 4.2 (e(η+2) ≥ 2m ⇒ Wilf, η = |S ∩ (m, 2m)|) forces η < √(2m), so
  e ≤ η + g′ + 1 ≲ (4/3)√(2m). It is a small-e, nearly-P18 regime: the YZ staircase ℓ ≥ 4 + 2η + η_ρ falls short of 4m/e
  by a constant factor only. In pure P18 at depth four (g′ = 0) the open window is (24m)^{1/4} ≲ k < √(2m), with W = W_0
  (Eliahou) there.
- FACE-WILF (R ≤ ρ + Σ_F τ + Z, conjecture; sufficient for Wilf): 0 failures on 586 structured excess-regime S
  (363 with R_A > p_A). Filler annealing around dense high-A B_3 cores (m = 61, 101) gives min slack per excess cubic
  20.7 and 36.4 (E300). The truncation-tail construction always adds E primitives, so this probes η > 0 only.
- **LAM4 equivalence (PROVED, identity).** At q = 4, by DEC-ID: Λ + Z ≥ h − e ⟺ W ≥ m − e − R, i.e. Wilf with surplus equal to
  the number of decomposable Apéry elements with K ≤ 0. So "DEPTH4-EH suffices" is a strengthening of Wilf. It fails only
  at small m in all data (⟨9,19,21,22⟩, ⟨25,26,30,31⟩, annealing m ≤ 25). In pure P18 at depth four it holds on every S of
  E301 (k = 4, m ≤ 44; k = 5, m ≤ 34), except ⟨25,26,30,31⟩ (k = 3).

### Depth four: window identity, translator lemma, WIN and MATCH4 (lead, 2026-10-20)
Setting q = 4 as above. Hw = residues [h, 2h) mod m (|Hw| = h); W_1 = residues [h, h + ⌈h/2⌉), W_2 = the rest of Hw.
Y = {v ∈ Ap : K(v) = 1, residue in Hw}; N_< = #{v ∈ Ap : K(v) ≤ 0, residue ∉ Hw}.
- **Window identity (PROVED).** W = Λ + Z + N_< − |Y|. Every element of Y is a pure-A critical cubic with residue in W_2,
  and W_1 holds no critical value.
  - Proof: s(v) = (M − v) mod m = (h − 1 − r) mod m, so s(v) ≥ ρ ⟺ r ∈ Hw. By the short arc (P13), every critical value
    other than a pure-A cubic lies outside Hw. A pure-A critical cubic has three pair faces of offset sum ≥ h, so its
    offset sum is ≥ 3h/2 and its residue lies in W_2.
  - Count Hw: h = |Y| + #{K ≤ 0 in Hw}. Then N_< = m − R − h + |Y|, and DEC-ID W = ρ + Λ + Z − R gives the identity.
  - Corollaries: Y = ∅ ⇒ Wilf. Wilf ⟺ |Y| ≤ Λ + Z + N_<.
- **Translator lemma (PROVED).** Let y ∈ Y and t ∈ P', and let x be the residue of v_y − n_t. Then exactly one holds:
  (a) t is a factor of v_y, and w_x = v_y − n_t is a face (UF, K = −1);
  (b) t is not a factor, w_x is a t-top, and λ(w_x) ≥ 1. This is a *Λ-option*; the pair (x, t) is its own term
      (ν_t + 1)λ ≥ 1 of Λ;
  (c) t is not a factor and λ(w_x) = 0.
  - Proof: if w_x + n_t ∈ Ap, it has residue y, so it equals v_y; then n_t divides v_y, and UF makes t a factor.
  - Consequences: Λ ≥ Σ_{y∈Y} #{Λ-options of y}, since distinct (y, t) give distinct (x, t). For any single t,
    |Y| ≤ #{y : x_t(y) has K ≤ −1} + #{y : Λ-option at t} + C0(t), where C0(t) = #{y : λ(w_{x_t(y)}) = 0, K ≥ 0}.
  - If the least factor offset c_0 of the cubes in Y exceeds h/2, then t = n_{c_0} maps every source into W_1.
- **Window-filling form (PROVED).** Take t ∈ P' whose offset τ = n_t mod m avoids (−h/2, h/2) mod m.
  - Every K = 0 element of W_1 with λ ≥ 1 is then either a t-top (a Λ term) or has t-successor in Ap. That successor is
    non-critical (only faces extend to critical cubics) and lies in W_2 or outside Hw.
  - Hence W ≥ (Λ − Λ_t(W_1)) + (Z − Z_c(W_1)) + (N_< − N_<^img) − C0(W_1). Here C0(W_1) = #{v ∈ Ap ∩ [c, c + ⌈h/2⌉) : K(v) = 0}.
  - So the only obstruction is the co-level-0, K = 0 elements in the bottom half of the co-level-0 window. These are
    E generators (each pays Λ_E = ℓ − 4 in its own direction), carried BB pairs, and cubics with exactly one low face.
- **Conjecture WIN (CONJ).** At q = 4, |Y| ≤ Λ + Z. Equivalently **W ≥ N_<**. It implies Wilf at depth four.
  - At h = m (c = 4m) we have N_< = 0, so WIN at c = 4m IS Wilf at c = 4m. WIN therefore contains the open m | c slice and
    is not an easy strengthening.
  - In the perfect A-simplex model, WIN holds by window filling: W_1 holds only faces, so |Y| ≤ |W_2| ≤ |W_1| ≤ Z.
- **Conjecture MATCH4 (CONJ, implies WIN).** Assign each y ∈ Y either a Λ-option or a distinct K ≤ −1 source x_t(y),
  where a source x can serve −K(w_x) cubes. MATCH4 says such an assignment always exists (a Hall condition on the
  cubes without Λ-options). In P18, y lacks Λ-options iff 3m + s − b ∉ S for every non-factor offset b > s − h, where
  s is the offset sum of y. Equivalently, v_y + m has no non-factor divisor with cofactor below c.
- Data (E303): WIN, MATCH4 and the identity have 0 failures on all 18,284,363 depth-four S (e ≥ 3) of genus ≤ 35, on every
  truncation family of E302 with k = 4 and m = 23..34, and on random P18. The census never has |Y| > 1 with small Λ. The
  dense-core regime (P14 residual, m ≥ 211) is not reached by any of these, so WIN is untested exactly where it matters.
  The stronger explicit V1, |Y| ≤ L2 (Lemma B), also has 0 failures at genus ≤ 35 (max −1). But L2 = 0 in a perfect
  A-simplex, so V1 would forbid short cubes there; V1 is therefore suspect in the extremal regime.

### P18 at depth four: truncated condensed Macaulay and the CHAIN bound (lead, 2026-10-20)
Setting: S = ⟨m, m + B⟩ with B ⊂ [1, m − 1] (all generators below 2m, the DKM Problem 1.8 class), 3m < c ≤ 4m, h = c − 3m.
- Notation:
  - A = {0} ∪ B as integers, e = |A|; X_j = jA is the j-fold integer sumset; a = |A ∩ (0, h)|, b = e − 1 − a.
  - Level sets of residues: T_2 = X_2 ∩ [0, m), T_3 = (X_3 ∩ [0, m)) ∪ ((X_2 ∩ [m, 2m)) − m), τ_2 = |T_2|.
  - Depth four means [h, m) ⊂ T_3, h − 1 ∉ T_3, and [0, h) ⊂ (X_4 ∩ [0,h)) ∪ ((X_3 ∩ [m, m+h)) − m).
    Then x = |T_3 ∩ [0, h)|, and W = e(1 + e + τ_2 + x) − 3m − h.
- **Lemma TCM (truncated condensed Macaulay; PROVED from Eliahou JEMS 2018 Thm 5.11).** For every integer L ≥ 1 and j ≥ 2:
  j·|(X_j ∖ X_{j−1}) ∩ [0, L)| ≤ |A ∩ (0, L)|·|X_{j−1} ∩ [0, L)|.
  - Proof: let k[C] be the semigroup ring of the cone C generated by {(1, s) : s ∈ A}, and x_0 = u^{(1,0)}. The set
    {(j, s) ∈ C : s ≥ L} spans a monomial ideal I_L, since adding (1, s') with s' ≥ 0 keeps s ≥ L.
  - So R = k[C]/(x_0, I_L) is a standard graded algebra. It has basis {(j, s) : s ∈ X_j ∖ X_{j−1}, s < L} and
    Hilbert function h_j = |(X_j ∖ X_{j−1}) ∩ [0, L)|, with h_1 = |A ∩ (0, L)|.
  - Eliahou's condensed Macaulay inequality j·h_j ≤ h_1(h_0 + … + h_{j−1}) gives the claim, since X_{j−1} ⊂ X_j.
  - Numerically checked: 1,957,520 instances (random A, every L, j = 2..5), 0 violations (src/scratch/p23/trunc_mac_check.py).
- **Proposition P18-CHAIN (PROVED).** At depth four, define
  - E1 = e(e+1) − 2|X_2| ≥ 0;
  - E2 = a·y0 − 4|(X_4 ∖ X_3) ∩ [0, h)| ≥ 0 (TCM, j = 4, L = h), where y0 = |X_3 ∩ [0, h)|;
  - E3 = (e+2)|X_2 ∩ [0, m+h)| − 3|X_3 ∩ [0, m+h)| ≥ 0 (TCM, j = 3, L = m + h);
  - U1 = |X_3 ∩ [m, m+h)|, the carried cubes; P_lo = |X_2 ∩ [m, m+h)|, P_hi = |X_2 ∩ [m+h, 2m)|, the carried pairs;
  - C2^{<h} = ((X_2 ∩ [m, m+h)) − m) ∖ X_3 and δ = P_lo − |C2^{<h}| ≥ 0;
  - ν = |(X_4 ∖ X_3) ∩ C2^{<h}|.
  Then **W ≥ E1 + E2 + E3 − U1 + b·y0 − (e−4)δ − P_hi + 4ν.**
  - Proof: m = |T_3| + n_4 and h = x + n_4, where n_4 = |H4| and H4 = [0,h) ∖ T_3.
  - |T_3| = |X_3 ∩ [0,m)| + |C2|, with C2 = ((X_2 ∩ [m,2m)) − m) ∖ X_3; also x = y0 + |C2^{<h}|.
  - Split H4 = H4a ⊔ H4b with H4a = H4 ∩ X_4. Then |H4a| ≤ |(X_4∖X_3) ∩ [0,h)| − ν. Also H4b ⊂ (X_3 ∩ [m, m+h)) − m, and
    the P_lo carried pairs map into T_3, so |H4b| ≤ U1 − P_lo.
  - Substitute 3|X_3 ∩ [0,m)| = (e+2)(τ_2 + P_lo) − 3U1 − E3, e(e+1) − 2τ_2 = E1 + 2P_lo + 2P_hi and |C2 ∩ [h, m)| ≤ P_hi.
  - Asserted on every S below; never violated.
- **Model check.** All-A B_3 carried simplex (B ⊂ [h/2, h), pairs < m, cubes carried into [m, m+h)): every term but E2 and
  U1 vanishes, E2 = e(e−1), and the bound is EXACT: W = e(e−1) − U1. Window filling gives U1 = h − e ≤ e(e−1) + 1 − e, and
  Wilf follows. (W_1 = [h, 3h/2) contains no 3-sum, so h/2 ≤ |X_2 ∩ W_1| ≤ C(e+1,2) − e.)
- **Conjecture CHAIN-CONJ (CONJ; implies P18 Wilf at depth four).** U1 + P_hi + (e−4)δ ≤ E1 + E2 + E3 + b·y0 + 4ν.
  - It is a purely additive statement about A ⊂ [0, m) under the depth-four covering conditions.
  - The covering conditions are necessary. Without them, U1 ≤ E2 + E3 fails, e.g. m = 15, A = {0, 5, 7}, h = 7
    (U1 = 4, E2 + E3 = 2), because [h, m) is not covered.
  - Data (E304): 0 failures. Min slack 6 (k = 3, m ≤ 40), 17 (k = 4, m ≤ 32), 31 (k = 5, m ≤ 24). Random k = 5..8,
    m ≤ 160: ≥ 90. Even U1 ≤ E2 + E3 alone never failed. The tightest cases are all-A with h close to m (c ≈ 4m).
- The obstruction is the same in every formulation (K-ID window form, P13 arc form, this chain): carried 3-sums landing
  at height four, paid only through window filling [h, 3h/2) ⊂ T_3.

## Top-band growth: window lemma FWG (PROVED) and conjectures TOPBAND / TB2 / RC′ (every depth)
Notation: q = ⌈c/m⌉, α = (q−1)m, h = c − α ∈ [1, m], x = |S ∩ [α, c)|. Kunz coordinates k_i (w_i = k_i m + i);
T_l = {i : k_i ≤ l}; P′ = minimal generators other than m, |P′| = e − 1.
- **Lemma FWG (window growth; PROVED, elementary).** For every integer a ≥ 0:
  |S ∩ [a+m, a+2m)| ≤ (e−1)·|S ∩ [a, a+m)| + 1.
  - Proof: [a+m, a+2m) holds exactly one multiple of m. Every other z ∈ S in that window has a factorization using some
    p ∈ P′, so z − p ∈ S and z − p < a + m. Let s(z) be the element of S ∩ [a, a+m) congruent to z − p (it is z − p + jm
    for some j ≥ 0). The map z ↦ (p, s(z)) is injective, since (p, s) fixes the residue of z and the window fixes z. ∎
  - At a = jm it reads |T_{j+1}| ≤ (e−1)|T_j| + 1.
- **Corollary D1 (PROVED; a = c − m).** (e−1)·|S ∩ [c−m, c)| + 1 ≥ m. In particular e·|S ∩ [c−m, c)| ≥ m.
- **Conjecture TOPBAND (CONJ).** e·x ≥ h.
- **Conjecture TB2 (CONJ; stronger).** (e−1)·x + 1 ≥ h. Equivalently, with D = {i : k_i = q} (all of D lies in [1, h)
  and h − 1 = max D): |D| ≤ (e−2)·|[0,h) ∖ D| + 1. Kunz form: if N residues attain the maximal Kunz coordinate and f is
  the largest of them, then (e−1)N ≤ (e−2)(f+1) + 1.
  - Proved cases: q = 2 (all of S ∩ (m, c) and m + [h, m) are generators; the decomposable D-elements are sums of two
    elements of T′ ∖ 0, at most C(x, 2) of them; then (x−1)(x−2) ≥ 0 closes it); e = 2 (each Kunz level holds at most
    one residue); e = 3 (D ⊂ PF(S) and the type is ≤ 2).
  - Tight families: x = 1 with e = h (⟨m, 2m+1, …, 3m−1⟩-type, D = [1, h) all generators), and e = 2 for every x.
  - TB2 = FWG restricted to the first h residues. The trivial injection fails there: a decomposition w_i = p + w_j of a
    top element can send j into [h, m) ("wrap"). Example: Kunz vector (3,3,1,…,1), m = 10, h = 3: w_1 = 31 = 13 + 18,
    w_2 = 32 = 13 + 19, and every decomposition wraps. So D ⊂ T′ + R (mod m) is FALSE, and so is the Hall form
    (each generator charged at most x times by the top elements above it). Hall counterexample:
    ⟨13,20,21,25,30,31,32,35,36,37⟩, D = {1,2,3} with only 20, 21 below them. TB2 is a counting fact, not a covering.
- **Conjecture RC′ (CONJ; generalizes TB2 to every level).** For every level l ≥ 1 and L ∈ [1, m] such that every residue
  in [L, m) has k ≤ l − 1: #{i < L : k_i = l} ≤ (e−2)·#{i < L : k_i ≤ l−1} + 1. (l = q, L = h gives TB2; L = m is FWG
  at a = (l−1)m.) Window form: if [a+L, a+m) ⊂ S with a ∈ mZ, then |S ∩ [a+m, a+m+L)| ≤ (e−1)|S ∩ [a, a+L)| + 1.
  - FALSE for a ∈ S ∖ mZ: ⟨13,14,16,18,19⟩, a = 19, L = 7 (lower window {19}, upper window [32, 39) full: 7 > 5·1 + 1).
  - FALSE without the condition on [L, m): ⟨11,17,18,20,21⟩, l = 3, L = 6 (residues 1..5 all at level 3 via wraps,
    n_2(6) = 1).
- **Suffix family (PROVED equivalence).** Let SUF(j) be e·|S ∩ [jm, c)| ≥ c − jm (0 ≤ j ≤ q−1). SUF(0) is Wilf and
  SUF(q−1) is TOPBAND. Then (SUF(j) for all j) ⟺ Wilf ∧ TOPBAND. Proof: ℓ_j = |S ∩ [jm, (j+1)m)| is nondecreasing for
  j ≤ q−2, and SUF(j) − SUF(j+1) = eℓ_j − m. Let j* be the first j with eℓ_j ≥ m. For j ≥ j* every later band term is
  ≥ 0, so SUF(j) ≥ TOPBAND. For j < j* the dropped terms are negative, so SUF(j) ≥ W. ∎ So the family adds nothing beyond
  TOPBAND.
- **Leverage (honest).** W = [e·|S ∩ [0, α)| − α] + [e·x − h]. TB2 makes the second bracket ≥ x − 1, but the first can be
  negative (to −21 in P18 at depth four, E303), so TB2 alone does not give Wilf. In P18 it is much weaker than TCM
  (4·n_4 against (e−2)·x). It is a structural inequality valid at every depth, and its proof is open.
- Data: E305.

## Level-wise Wilf families (FALSE) and the order grading (LEN, order-Wilf: PROVED)
Notation: Kunz level k(w) = ⌊w/m⌋ on Ap = Ap(S, m); L(w) = longest factorization length of w (the order of t^w in
k[[S]]/(t^m)); ε(w) = k(w) − L(w) ≥ 0, the excess (carries plus generator excess); H_J = |S ∩ [Jm, (J+1)m)| = #{w : k(w) ≤ J}.
- **Exact level identity (PROVED, every S).** With q = ⌈c/m⌉, x = |S ∩ [(q−1)m, c)|, n_q = h − x:
  W = Σ_{J=0}^{q−2} M_J + M_top, where M_J = (e−1)H_J − (J+1)(H_{J+1} − H_J) and M_top = (e−1)x − q·n_q.
  Each M_J is a condensed-Macaulay slack in the Kunz-level grading. Partial sums Φ_J = e·|S ∩ [0, Jm)| − J·H_J.
- **BANDWILF (Φ_J ≥ 0 for all J ≤ q) — FALSE.** It survives the genus ≤ 26 census (5.7M instances), but:
  ⟨14,22,23⟩ (e = 3): Φ_4 = 39 − 40 = −1; ⟨27,68,70⟩ (e = 3): Φ_7 = −1; ⟨46,72,73,76⟩ (e = 4, q = 9, W = 232): Φ_4 = −4;
  also ⟨48,74,77,79⟩ and ⟨56,85,89,92⟩ (e = 4, Φ_4 = −4). Verified by independent pure-Python code (E308).
  Its continuous interpolations GBW (m·e·|S ∩ [0,N)| ≥ N·|S ∩ [N,N+m)|) and GBW″ (e·|S ∩ [0,N)| ≥ Σ_{z ∈ S∩[N,N+m)} ⌊z/m⌋,
  which is Wilf at N = c) are also FALSE: GBW″ fails at ⟨39,59,61,64,68⟩ (e = 5), N = 98, 35 < 41.
  - Mechanism: with generators clustered near αm (α ∈ (1, 2)), j-fold sums land at level ≈ αj, so levels are skipped
    (⟨46,72,73,76⟩ has H = 1, 4, 4, 10, 20, 20, 33, …). The level slacks M_J swing (0, 12, −6, −10, 60, −18, 71, 63) and
    are repaid only at later levels. **Any proof must couple payments across levels; no per-level or prefix inequality
    in the Kunz grading is true.** The Kunz level is the wrong clock.
- **Order O-sequence (classical; re-derived).** h(j) = #{w ∈ Ap : L(w) = j} is the Hilbert function of
  gr_𝔪(k[[S]]/(t^m)), a standard graded algebra with h(1) = e − 1. So Macaulay and condensed Macaulay hold with no
  Cohen–Macaulay hypothesis. Truncated form: for every value threshold T, h_T(j) = #{w ∈ Ap : w < T, L(w) = j} is an
  O-sequence. ((t^w : w ≥ T) is an ideal, and orders below T are unchanged in the quotient, since everything is graded
  by value.)
  - Consequence (condensed Macaulay, induction on J): Σ_w L(w) ≤ (1 − 1/e)(D+1)m, where D = max L.
- **Lemma LEN (PROVED, every S, every N ≥ 0).** e·|S ∩ [0, N)| ≥ Σ_{z ∈ S ∩ [N, N+m)} L(z).
  - Proof: fix a longest factorization f of each window element z. The triples (z, p, t), with 1 ≤ t ≤ f_p(z), map to
    the pairs (p, z − tp) ∈ P × (S ∩ [0, N)) (z − tp ∈ S, and z − p < N because p ≥ m). This map is injective: z ≡ s mod p,
    and the window has length m ≤ p. ∎
  - At N = c: **order-Wilf, (e−1)ℓ ≥ Σ_{w∈Ap} L(w).** Hence the exact split W = [(e−1)ℓ − Σ_w L(w)] − Σ_w ε(w):
    a proved-nonnegative order slack minus the total excess. Wilf ⟺ Σε ≤ the LEN slack.
  - Two-generator semigroups have W = 0 at every dilation b/a, so excess is benign when it is proportional to order.
    The harm is excess at low order relative to the top.
- Failed split (E309): order-Wilf at the virtual conductor c_0 = max(L(w)m + r(w)) − m + 1, together with
  e·Σε ≤ (e−1)(c − c_0). The first fails in 569 S and the second in 237,480 (genus ≤ 24), never both. Wrong reference.

## P18 depth four, all-A case: exact identity and the free part (FREE-A)
Setting: S = ⟨m, m+B⟩, A = {0} ∪ B, depth four (3m < c = 3m + h ≤ 4m), all-A: B ⊂ (0, h). Sumsets jA are integer sumsets;
y0 = |3A ∩ [0,h)|, U1 = |3A ∩ [m, m+h)| (carried pairs and cubes), P_lo = |2A ∩ [m, m+h)|,
δ = #{s ∈ 2A ∩ [m, m+h) : s − m ∈ 3A}, N4 = |(4A ∖ 3A) ∩ [0,h)|, ν = |{r ∈ (4A ∖ 3A) ∩ [0,h) : r + m ∈ 2A, r ∉ 3A}|,
H4b = residues r < h of Kunz level 4 with r ∉ 4A, Ω = U1 − P_lo − |H4b| ≥ 0; E1, E2, E3 as in P18-CHAIN (a = e − 1, b = 0).
- **Identity (PROVED; exact).** W = E1 + E2 + E3 − U1 − (e−4)δ + 4ν + 4Ω.
  - Proof: all-A gives 2A ⊂ [0, 2h) ⊂ [0, m+h), so P_hi = 0 and τ_2 = |2A| − P_lo. Coverage of [h, m) is by 3A alone, since
    carried pairs have residues below 2h − m ≤ h; so m − h = |3A ∩ [h, m)|. Then 3|3A ∩ [h,m)| = 3|3A ∩ [0, m+h)| − 3y0 − 3U1,
    3|3A ∩ [0, m+h)| = (e+2)|2A| − E3, e(e+1) − 2τ_2 = E1 + 2P_lo, x = y0 + P_lo − δ, and n_4 = (N4 − ν) + |H4b| with
    |H4b| = U1 − P_lo − Ω. Substitute into W = e(1+e+τ_2+x) − 3(m−h) − 4h. ∎
  - Checked: 0 mismatches on 7,035 all-A depth-four S (k = 3, m ≤ 40; k = 4, m ≤ 30; random k = 5, 7) (E311).
- **Conjecture FREE-A (CONJ).** 4h + e·δ ≤ (e+3)·y0 + 3·U1. Equivalently E2 + 4ν + 4Ω − U1 − (e−4)δ ≥ 0.
  - Then W = FREE-A slack + E1 + E3 with E1, E3 ≥ 0 (Macaulay slacks). **In the all-A case collisions never hurt**: the
    extremal sets are collision-free (B_3-like), which is exactly the near-simplex regime.
  - Data (E311): 0 failures; min slack 7 (k = 3), 9 (k = 4), 39 (k = 5 random), 46 (k = 7 random).
- **Conjecture FA2 (CONJ; stronger, drops Ω).** 4N4 + U1 + (e−4)δ ≤ (e−1)·y0, i.e. U1 + (e−4)δ ≤ E2. FA2 ⟹ FREE-A (from
  h ≤ y0 − δ + N4 + U1). Data: 0 failures, but TIGHT at ⟨15,22,24,25⟩ (A = {0,7,9,10}, h = 14, U1 = 12 = (e−1)y0). Treat
  as fragile: in the core regime B ⊂ [h/2, h) it amounts to U1 ≤ e(e−1), which sits at the window-filling (postage-stamp)
  constant.
- **Core regime B ⊂ [h/2, h) (reduction, PROVED).** Here y0 = e and N4 = 0. With h = e + (P_lo − δ) + |H4b|, FREE-A ⟺
  h ≤ e² − (e−3)δ + 3Ω. Window filling: [h, m+h) ∖ (A+m) ⊂ 2B ∪ 3B and 3B ≥ 3h/2, so |2B ∩ [h, 3h/2)| ≥ h/2 − (e′ − δ′),
  where e′ = |(A+m) ∩ [h, 3h/2)| ≤ |A ∩ [0, 3h/2 − m)| ≤ 1 (since m ≥ h and B ≥ h/2) and δ′ = |(A+m) ∩ [h,3h/2) ∩ 2B|.
  Hence h ≤ e(e−1) + 2(e′ − δ′) ≤ e(e−1) + 2. So FREE-A holds in the core regime whenever δ = 0 (then e² ≥ e(e−1) + 2 for
  e ≥ 2). The case δ ≥ 1 remains (needs (e−3)δ ≤ e − 2 + 3Ω + window slack).
  - [2026-10-20, later] Wilf in the whole core regime is now PROVED by Theorem CORE4 below, which does not go through
    FREE-A. FREE-A itself in the core regime with δ ≥ 1 is still open, and no longer needed.

## Theorem CORE4 (P18 depth four, core regime B ⊂ [⌈h/2⌉, h)) — PROVED 2026-10-20 (paper; checks E312)
Setting: m ≥ 2, B ⊂ [1, m−1], S = ⟨m, m + B⟩ a numerical semigroup, 3m < c = 3m + h ≤ 4m, A = {0} ∪ B, e = |A|,
h′ = ⌈h/2⌉, and **B ⊂ [h′, h)**. Integer sumsets: 2B, 3B, 2A = {0} ∪ B ∪ 2B, 3A = 2A ∪ 3B.
- Notation:
  - X = [h, m + h); W_1 = [h, 3h′); D = 2B ∩ (A + m), δ = |D| (carried pairs whose residue lies in A);
  - κ = |(A + m) ∩ (2B ∪ 3B)| ≥ δ; τ = |3B ∩ [m + h, ∞)|;
  - E1 = e(e+1) − 2|2A| = e² − e − 2|2B| ≥ 0; E3f = (e−1)|2A| − 3|3A ∖ 2A| ≥ 0 (TCM with L > 3h, i.e. Eliahou's condensed
    Macaulay inequality untruncated);
  - e′ = |(A + m) ∩ W_1|, ρ2 = |2B ∖ W_1|, δ1 = |D ∩ W_1|.
- **Statement.** W(S) = e·ℓ − c ≥ e − 2e′ + 3·[h odd] ≥ e − 2. More precisely
  W ≥ e − 2e′ + 3·[h odd] + E3f + 2ρ2 + 2δ1 + ½E1 (and + 2E1 when no carried pair has residue in B).
- **Step 1 (shape).** 2B ⊂ [2h′, 2h − 2] ⊂ [h, 2h − 2] and 3B ⊂ [3h′, 3h − 3]. Hence 3A ∩ [0, h) = A, and 2B < m + h.
- **Step 2 (coverage; exact).** For a residue r ∈ [h, m), r + 3m ∈ S iff r ∈ 3A, since r + m > 2h − 2 ≥ max 2A.
  For r ∈ [0, h), r + 4m ∈ S iff r ∈ 4A ∩ [0,h) = A or r + m ∈ 3A. Both must hold because c = 3m + h.
  So X ⊂ 2B ∪ 3B ∪ (A + m), and X contains all three sets except 3B ∩ [m+h, ∞). Counting X:
  m = |2B| + |3B ∖ 2B| − τ + e − κ.
- **Step 3 (ℓ; exact).** S ∩ [0, c) = {0} ∪ (m + A) ∪ (2m + 2A) ∪ (3m + A). The only overlaps are 2m + D = 3m + (D − m),
  so ℓ = 3e + 1 + |2B| − δ.
- **Step 4 (identity).** Substitute 3|3B ∖ 2B| = (e−1)(e + |2B|) − E3f into W = e·ℓ − 3m − h:
  **W = e² + E1 + E3f − eδ + 3τ + 3κ − h** (exact).
- **Step 5 (window).** For h ≥ 2, W_1 ⊂ X, and W_1 misses 3B, so W_1 ⊂ 2B ∪ (A + m).
  Since |W_1| = h/2 (h even) or (h+3)/2 (h odd): h ≤ 2|2B ∩ W_1| + 2e′ − 2δ1 − 3[h odd] = e² − e − E1 − 2ρ2 + 2e′ − 2δ1 − 3[h odd].
  - e′ ≤ 1 for h even (only m + 0 can lie in W_1, since m + b ≥ h + h′).
  - e′ ≤ 2 for h odd, with equality only if m = h and h′ ∈ B.
- **Step 6 (paying the carried pairs).** Write δ = δ_0 + k, with δ_0 = [m ∈ 2B] ≤ 1 and B′ = {s − m : s ∈ D, s ≠ m} ⊂ B, k = |B′|.
  - If m ∈ 2B, say m = b1 + b2, then m + b = b1 + b2 + b ∈ 3B, so κ = e.
  - For s ∈ D with s − m ∈ B and b ∈ B: s + b ∈ 3B and s + b ≥ m + 2h′ ≥ m + h. So τ ≥ |B′ + B|.
  - B′ + B is the image of the C(e,2) − C(e−k,2) = k(2e − k − 1)/2 multisets {x, y} ⊂ B meeting B′. Its deficiency is at
    most that of all of 2B, which is C(e,2) − |2B| = E1/2. So τ ≥ k(2e − k − 1)/2 − E1/2.
  - Hence, with k ≤ e − 1 and κ ≥ δ:
    - k = 0: 3τ + 3κ − eδ ≥ 0 (δ = 0), or ≥ 3e − e = 2e (δ = δ_0 = 1).
    - k ≥ 1, δ_0 = 0: 3τ + 3κ − eδ + (3/2)E1 ≥ (3/2)k(2e−k−1) − (e−3)k = k(2e + 3/2 − 3k/2) ≥ k(e+6)/2 > 0.
    - k ≥ 1, δ_0 = 1: 3τ + 3κ − eδ + (3/2)E1 ≥ (3/2)k(2e−k−1) + 3e − e(k+1) ≥ 2e + ke/2 > 0.
- **Step 7.** Steps 4 and 5 give W ≥ e − 2e′ + 3[h odd] + 2E1 + E3f + 2ρ2 + 2δ1 + (3τ + 3κ − eδ). Step 6 bounds the last
  term from below by −(3/2)E1 (k ≥ 1) or 0 (k = 0). The bound on e′ in Step 5 finishes the proof. ∎
- Dependencies: Lemma TCM (Eliahou JEMS 2018 Thm 5.11) with L > 3h, only for E3f ≥ 0; everything else is counting.
- Why it matters: this is the near-simplex (B_3) regime, where every earlier P18 bound was tight or failed. The carried
  pairs (δ) are paid by the carried 3-sums they force above m + h (τ), which is exactly the term the truncated chain
  (truncation at L = m + h) cannot see. It is the first complete payment of the face-sharing deficit in a nontrivial
  depth-four family.
- Coverage by known criteria: most core S are not covered by h ≤ e (DEPTH4-EH), e(e+1) ≥ 2m (Yang–Zhang),
  (e−1)² ≥ 2m (DKM) or 3e ≥ m (Eliahou). Examples: ⟨15,22,24,25⟩ (W = 17) and ⟨22,31,32,34,35⟩ (W = 36) (E311/E312).
- Lean: not yet formalized. Statement and proof are elementary apart from TCM. Good first candidate for the Lean agent.


## Lemma RTCM (relative condensed Macaulay) — PROVED 2026-10-20 (from Eliahou JEMS 2018 Thm 5.11; checks E313)
Setting: A ⊂ N finite, 0 ∈ A, e = |A|; jA integer sumsets; E3f = (e−1)|2A| − 3|3A ∖ 2A| ≥ 0.
- **Statement.** For every Q ⊂ 2A ∖ A: 3·|(3A ∖ 2A) ∖ (Q + A)| ≤ (e−1)(|2A| − |Q|). Equivalently
  3·|(Q + A) ∖ 2A| ≥ (e−1)|Q| − E3f, and so **3|Q + A| ≥ (e+2)|Q| − E3f** (since Q ⊂ (Q + A) ∩ 2A).
- Proof: R = k[C]/(x_0) (C the cone over {1} × A) has monomial basis {(j, s) : s ∈ jA ∖ (j−1)A}. Let J be the monomial
  ideal generated by (2, q), q ∈ Q. R/J is standard graded, with H(0) = 1, H(1) = e − 1, H(2) = |2A ∖ A| − |Q|.
  Also J_3 = R_1·J_2 is spanned by the nonzero monomials (3, q + a), i.e. by (Q + A) ∖ 2A, so H(3) = |3A∖2A| − |(Q+A)∖2A|.
  Eliahou's condensed Macaulay inequality 3H(3) ≤ H(1)(H(0) + H(1) + H(2)) is the claim. ∎
- The same proof works at every degree: for Q ⊂ jA ∖ (j−1)A,
  (j+1)|((j+1)A ∖ jA) ∖ (Q + A)| ≤ (e−1)(|jA| − |Q|). It is depth-independent.
- Meaning: a family Q of "shared" 2-sums cannot have a small A-shadow Q + A unless the global Macaulay slack E3f is spent.
  This is the quantitative coupling between face-sharing (collisions among the translates q + A) and compensation.
- Checked: random Q, and Q = wasted carried pairs, on every S of E313 (0 violations).

## P18 depth four: general exact identity, the residual V, and Conjecture RES4 (lead, 2026-10-20)
Setting: S = ⟨m, m + B⟩, B ⊂ [1, m−1], 3m < c = 3m + h ≤ 4m, A = {0} ∪ B. Notation as in P18-CHAIN, plus:
- τ = |3A ∩ [m+h, ∞)|; ω = #{v ∈ 3A ∩ [m, m+h) : v − m ∈ 4A};
- Dset = {s ∈ 2A ∩ [m, m+h) : s − m ∈ 3A}, δ = |Dset|; Pset_hi = 2A ∩ [m+h, 2m), P_hi = |Pset_hi|;
- δ_hi = #{s ∈ Pset_hi : s − m ∈ 3A}; Q = Dset ∪ Pset_hi (the wasted carried pairs);
- T = e·y0 − 3N4 − h; extra = τ + ω − |Q + A| ≥ 0 (since Q + A ⊂ (3A ∩ [m+h,∞)) ∪ {ω-positions}).
- **Identity (★) (PROVED; exact).** W = E1 + E3f + T + 3(τ + ω + δ_hi) − eδ − (e+3)P_hi.
  Equivalently W = E1 + E2 + E3f + b·y0 + 3τ + 4ω − U1 − eδ − (e+3)P_hi + 3δ_hi.
  - Proof: ℓ = 1 + e + |2A| − P_hi + y0 − δ. Coverage gives m − h = |3A ∩ [h,m)| + P_hi − δ_hi and h = y0 + N4 + U1 − ω.
    Then 3m + h = 3|3A| − 3τ + y0 + U1 + 3P_hi − 3δ_hi + 4N4 − 4ω. Substitute 3|3A| = (e+2)|2A| − E3f. ∎
  - Checked: 0 mismatches on every depth-four S of E313.
- **Split (PROVED).** With σ = 3|Q + A| − (e+2)|Q| + E3f ≥ 0 (Lemma RTCM): **W = V + σ**, where
  V = E1 + T + 2δ − P_hi + 3δ_hi + 3·extra.
  - Excess form (PROVED): V = E1 + E2 + b·y0 + 2δ + 2δ_hi + ν + 3·extra − Σε. Here Σε = (P_lo − δ) + (P_hi − δ_hi) + |H4b|
    is the total excess (residues whose Apéry element needs a carry); compare W = LENslack − Σε.
- **Conjecture RES4 (CONJ; implies P18 Wilf at depth four, with E3f no longer needed).** V ≥ 0.
  - SHARP: V = 0 at ⟨17,21,29,31,32⟩ (A = {0,4,12,14,15}, h = 7: T = 3, P_hi = 6, δ_hi = 1, E1 = δ = extra = 0); W = 27 = σ.
  - Data (E313): 0 failures on 514 + 12,166 + 129,866 exhaustive S (k = 3, 4, 5; m ≤ 60, 40, 28) and 50k random S.
    Annealing (6 runs, m ≤ 200, e ≤ 17): min V = 0, only at the example above. V − E1 < 0 occurs (−11), so E1 is needed.
- **CORE4 again, shorter.** In the core regime P_hi = 0, y0 = e, N4 = 0, so V = E1 + e² − h + 2δ + 3·extra. Step 5 of CORE4
  gives V ≥ e − 2e′ + 3[h odd] + 2E1 + 2δ + 2ρ2 + 2δ1 + 3·extra, and W = V + σ ≥ V. This replaces Step 6.
- **All-A case (b = 0).** V ≥ 2E1 + 2ρ + Z, with
  - ρ = |2A ∩ [3h′, ∞)|, W_1 = [h, 3h′), h_2 = |2A_{<h}| − e, h_3 = |3A_{<h}| − |2A_{<h}|;
  - t3w = |(3A∖2A) ∩ W_1|, e″ = |W_1 ∩ (m + 4A_{<h}) ∖ 3A|;
  - Z = (e+2)h_2 + e·h_3 + e + 3[h odd] − 2t3w − 3N4 − 2e″.
  - Z ≥ 0 held on all data (min 0, e.g. B = (2,4,6,8,10), m = 13, an arithmetic progression) and under annealing (min 2).
  - Pieces:
    - Z1: 2t3w ≤ (e+2)h_2 — 0 failures (CONJ).
    - Z2: 3N4 ≤ e·h_3 — 0 failures (CONJ; not a pure Macaulay consequence for e ≤ 5).
    - Z3: 2e″ ≤ e + 3[h odd] — FALSE (min −170): with many small elements e″ is large, but then Z1 and Z2 have room.
  - REFUTED split: D = 3τ + 3ω − eδ ≥ 0 fails (annealing: D = −273 at m = 49, B ∋ 1, 2). Small elements make δ large but
    y0 larger; the window part and the carried part must be coupled.
- **No-small case (B ⊂ [h′, m); a core, b high).** Free counting gives
  V ≥ (a+1)(b+1) − P_hi − 2π1 − 2β1 − 2e′ + 3[h odd] + 2δ + 3δ_hi + 3·extra + (collision savings), where
  - β1 = |B_h ∩ W_1|;
  - π1 = |((Pset_hi − m) ∩ W_1) ∖ 2A| (window cells covered only by high carried pairs).
  It is EXACT at the sharp example (8 − 6 − 8 + 3 + 3 = 0). Open: P_hi + 2π1 can exceed (a+1)(b+1) when b ≫ a. Then
  δ_hi, extra, E1 or σ must pay.
- **Split into two first-order statements (PROVED identity; both halves CONJ).** From W = V + σ:
  **W = (T + E1) + (σ − P_hi) + 2δ + 3δ_hi + 3·extra**, all of δ, δ_hi, extra ≥ 0. So P18 depth-four Wilf follows from
  - **Conjecture TB4 (top band at depth four):** h + 3N4 ≤ e·y0 + E1, equivalently h + 3N4 + 2|2B ∖ A| ≤ e(y0 + e − 1);
  - **Conjecture SIG1 (shadow surplus):** σ ≥ P_hi, i.e. 3|Q + A| + E3f ≥ (e+2)|Q| + P_hi for Q = Dset ∪ Pset_hi.
  - Data:
    - TB4: min 1, at ⟨20,24,25,27,33⟩ with h = 4, a covered case. Among uncovered S the min is 3. T alone dips to −1 (a = 0).
    - SIG1: min 0, only with P_hi = 0. When P_hi > 0, σ − (2a+1)P_hi ≥ 4, so the free-shadow surplus 2a·P_hi is realized.
    - Both: 0 failures on all of E313 and under annealing (`annV2` modes 5, 6, 7).
  - TB4 is NOT a consequence of local covering conditions (E314):
    - It fails under the window condition W_1 ⊂ 3A ∪ (Pset_hi − m) ∪ (m + 4A_{<h}) alone: worst −13 at m = 31,
      A = {0,25,26,28,30}, h = 20.
    - It still fails with the defining gap and the low covering [0,h) ⊂ 4A ∪ (3A − m) added: worst −4 at m = 39,
      A = {0,12,13,16,18,37}, h = 10.
    - It needs the covering of [h, m) as well. In both failures a = 0: all of B lies above h.
  - Window form: since h ≤ 2·#(window coverers) − 3[h odd], TB4 ⟸ 2(β1 + |(2B∖A) ∩ W_1| + t3w + π′ + e″) + 3N4 ≤
    e·y0 + E1 + 3[h odd]. In the core this is 4|2B ∩ W_1| ≤ … and holds by |2B| ≤ C(e,2).

## Token proof of degree-3 truncated Macaulay; overflow bound; reduction W ≥ T + E1 + (2 − a)δ (lead, 2026-10-20)
Setting: A ⊂ N finite, 0 ∈ A, B = A ∖ {0}, e = |A|; jA integer sumsets; for L ≥ 1,
E3_L = (e−1)|2A ∩ [0, L)| − 3|(3A ∖ 2A) ∩ [0, L)|.
- **Lemma TOK3 (PROVED, elementary; no Macaulay theory).** Tokens are pairs (s, x) ∈ (2A ∩ [0, L)) × B, so there are
  (e−1)|2A ∩ [0, L)| of them; the token (s, x) points to s + x. Each v ∈ (3A ∖ 2A) ∩ [0, L) receives 3 distinct tokens,
  and no token is given to two values. Hence 3|(3A∖2A) ∩ [0,L)| ≤ (e−1)|2A ∩ [0,L)|, i.e. E3_L ≥ 0 (TCM, j = 3), and
  **E3_L = number of unassigned tokens.**
  - Proof. Let v ∈ (3A ∖ 2A) ∩ [0, L). Every representation v = x + y + z with x, y, z ∈ A has x, y, z ∈ B (a zero summand
    would put v in 2A). Fix one, x ≤ y ≤ z. Every partial sum of two summands lies in 2A ∖ A (if, say, y + z ∈ A then
    v ∈ A + A) and is < v < L.
    - x < y < z: give v the tokens (y+z, x), (x+z, y), (x+y, z). They are distinct (different second coordinates).
    - x = y < z: give (x+z, x), (2x, z) and the token (x, z), whose first coordinate x lies in A.
    - x < y = z: give (y+z, x), (x+y, y) and the token (y, x), first coordinate y ∈ A.
    - x = y = z: give (2x, x) and the tokens (x, x) and (0, x), first coordinates in A.
    Tokens with first coordinate in 2A ∖ A point to v itself, so they are never shared between different v. A token
    (r, t) with r ∈ A is given only as follows: (r, t) with t ≠ r goes to the value with representation {r, r, t};
    (x, x) and (0, x) go to 3x. So each such token determines its receiver. ∎
- **Lemma OVF (PROVED).** E3_L ≥ OVF_L := #{(s, x) ∈ (2A ∩ [0, L)) × B : s + x ≥ L}.
  - Proof: every token handed out in TOK3 points to a value < L. Rep tokens point to v < L. The tokens (r, t) with r ∈ A
    point to r + t, which is x + z, x + y, 2x or x, all < v < L. So overflow tokens are never assigned. ∎
  - Checked: every A of E317 (k ≤ 9) at 8 values of L each, 0 violations.
  - Meaning: truncated Macaulay is lossy exactly where the A-shadow of a 2-sum leaves [0, L). This is a quantitative
    form of "large elements pay": each 2-sum s < L contributes |B ∩ [L − s, ∞)| to the slack.
- **Identity (★L) (PROVED; exact).** P18 at depth four (S = ⟨m, m+B⟩, B ⊂ [1, m−1], c = 3m + h, 0 < h ≤ m), L = m + h:
  **W = E1 + E3_L + T − P_hi − e·δ + 3δ_hi + 3ω**, with T = e·y0 − 3N4 − h and the notation of Identity (★).
  - Proof: as for (★). Write 3|3A ∩ [h, m)| = 3|2A ∩ [0, L)| + 3|(3A∖2A) ∩ [0,L)| − 3y0 − 3U1, use
    3|(3A∖2A) ∩ [0,L)| = (e−1)|2A ∩ [0,L)| − E3_L, e(e+1) − 2|2A| = E1, and h = y0 + N4 + U1 − ω. ∎
  - It uses only the low covering (C1) [0, h) ⊂ 4A ∪ ((3A ∩ [m, L)) − m) as an identity, and the covering of [h, m) only
    through its count m − h = |3A ∩ [h, m)| + P_hi − δ_hi. Checked: 0 mismatches (E317).
- **Proposition RED-A2 (PROVED).** At depth four, with a = |B ∩ [1, h)| and OP the number of ordered pairs
  (x, x′) ∈ B × B with x + x′ ≥ L:
  **W ≥ (T + E1) + (OP − P_hi) + (2 − a)·δ + (e−1−a)(P_lo − δ) + 3(ω − δ) + 3δ_hi**, all brackets except (2−a)δ ≥ 0.
  In particular **W ≥ T + E1 whenever a ≤ 2 or δ = 0**, so Conjecture TB4 implies P18 depth-four Wilf in those cases
  (with no need for SIG1).
  - Proof: OVF_L counts the tokens (x′, x) with x′ ∈ B and x + x′ ≥ L (that is OP), and for each of the P_lo elements
    s ∈ 2A ∩ [m, L) every token (s, x) with x ∈ B ∩ [h, m) (that is e − 1 − a of them). These classes are disjoint, so
    E3_L ≥ OP + (e−1−a)P_lo. OP ≥ P_hi: each s ∈ 2A ∩ [L, 2m) is x + x′ with x, x′ ∈ B (a zero summand gives s < m), and
    distinct s give distinct ordered pairs. Finally δ ≤ P_lo and δ ≤ ω (s ∈ Dset lies in 3A ∩ [m, L) with s − m ∈ 4A).
    Substitute into (★L). ∎
  - Checked: W ≥ T + E1 held on every real depth-four S with a ≤ 2 of E317 (0 violations).
- **Conjecture TOV (CONJ).** E1 + T + OVF_L + 3δ_hi + 3ω ≥ P_hi + e·δ. Then W = TOV + (E3_L − OVF_L) ≥ TOV.
  - Data (E317): 0 failures on real S (min 3, 4, 6, 15 for e = 3, 4, 5, 6; exhaustive k = 2..5, random k = 6, 9).
  - Unlike TB4 it also held on all random LOCAL fakes with e ≥ 5 (configurations satisfying (C1) and the defining gap,
    with m replaced by the count m_eff, but not the covering of [h, m)).

## Theorem A0 (P18 depth four, no element of B below h) — PROVED 2026-10-20 (paper; checks E317)
Setting: S = ⟨m, m + B⟩, B ⊂ [1, m−1], 3m < c = 3m + h ≤ 4m, A = {0} ∪ B, e = |A|, and **B ⊂ [h, m)** (a = 0).
**Statement: W(S) ≥ 1.** More precisely W ≥ 1 + E1 when 3h ≤ m.
- Notation: L = m + h; P_lo = |2A ∩ [m, L)|, P_hi = |2A ∩ [L, 2m)|; δ = [m ∈ 2A] (here 3A ∩ [0,h) = {0});
  H = B ∩ [L/2, m), η = |H|; B_1 = B ∩ [h, 2h), β1 = |B_1|; O = B ∩ [L/2, 2h) = H ∩ B_1.
- Step 1 (RED-A2 with a = 0). y0 = 1 and N4 = 0, since every element of B is ≥ h. So T = e − h and
  W ≥ e − h + E1 + (OP − P_hi) + (e−1)(P_lo − δ) + 2δ.
- Step 2 (OP − P_hi ≥ P_hi − η). Let U be the unordered pairs {x, x′} ⊂ B (x = x′ allowed) with x + x′ ≥ L. Then
  P_hi ≤ |U| and OP = 2|U| − η, since the pairs with x = x′ are exactly those with x ∈ H. So OP − P_hi ≥ 2|U| − η − |U| ≥ P_hi − η.
- Step 3 (h ≥ m/2). Then 3B ≥ 3h ≥ L, so no 3-sum lies in [m, L). The low covering puts r + m ∈ 3A for every
  r ∈ [1, h) (4A ∩ [1, h) = ∅), so those r + m lie in 2B, and P_lo ≥ h − 1. Also δ ≤ 1. Step 1 gives
  W ≥ e − h + (e−1)(h − 1 − δ) + 2δ ≥ (e−2)(h−1) + 1 ≥ 1 (h ≥ 2 because h − 1 ∉ 3A ∋ 0).
- Step 4 (2h ≤ m). [h, 2h) ⊂ [h, m) ⊂ R_3. Here 3A ∩ [h, 2h) = B_1 (2B ≥ 2h), and the carried part of R_3 ∩ [h,2h) is
  (2A ∩ [m+h, m+2h)) − m, which has at most P_hi elements. So h ≤ β1 + P_hi. With Steps 1 and 2:
  W ≥ e − β1 − η + E1 + (e−1)(P_lo − δ) + 2δ. Also β1 + η = |B ∩ ([h,2h) ∪ [L/2, m))| + |O| ≤ e − 1 + |O|, so
  **W ≥ 1 − |O| + E1 + (e−1)(P_lo − δ) + 2δ.**
  - 3h ≤ m: then 2h ≤ L/2, so O = ∅ and W ≥ 1 + E1.
  - m/3 < h < m/2, min B ≥ m − h: then 3B ≥ 3(m−h) ≥ L, and as in Step 3, P_lo ≥ h − 1 and W ≥ 1.
  - m/3 < h < m/2, μ = min B < m − h: each x ∈ O has x + μ ≥ L/2 + h > m (as 3h > m) and x + μ < 2h + m − h = L.
    So the |O| sums x + μ are distinct elements of 2A ∩ (m, L), and P_lo ≥ |O|. If δ = 0, W ≥ 1 + (e−2)|O| ≥ 1. If δ = 1,
    W ≥ 1 − |O| + (e−1)(|O| − 1) + 2 ≥ 2 when |O| ≥ 1, and W ≥ 1 + E1 + 2 when O = ∅. ∎
- Dependencies: Identity (★L) and Lemma OVF (both elementary). No Macaulay theory and no external theorem.
- Checks: a = 0 real S of E317 — 3h ≤ m: 0 violations of W ≥ 1 + E1 (exhaustive k ≤ 5, random k = 6, 8);
  m/3 < h: complete enumeration of every B ⊂ (m/3, m) for m ≤ 33 (`src/scratch/p27/a0mid.c`). The minimum W there
  is 41 (m = 13), and Eliahou's criterion 3e ≥ m fails for many of these S (676 at m = 31), so the band is not
  covered by known criteria.
- Leverage: a = 0 was the regime of every local-condition failure of TB4 (E314) and of the a = 0 refutation of
  "h > e ⇒ Yang–Zhang". With RED-A2, the remaining P18 depth-four cases all have a ≥ 1, and for a ∈ {1, 2} Wilf
  follows from TB4 alone.
- Lean: good candidate (elementary; needs the (★L) bookkeeping and the token lemma).

## Proposition RED-A (P18 depth four, every a) — PROVED 2026-10-20 (strengthens RED-A2; checks E318)
**W ≥ (T + E1) + (OP − P_hi) + 2δ + (e−1−a)(P_lo − δ) + 3δ_hi.** Every bracket except T + E1 is ≥ 0.
So **Conjecture TB4 alone implies P18 depth-four Wilf** (SIG1 is no longer needed, for any a).
- Proof. Start from (★L): W = E1 + E3_L + T − P_hi − eδ + 3δ_hi + 3ω, L = m + h. Classify the tokens of TOK3 whose
  first coordinate is s ∈ Dset (s ∈ 2A ∩ [m, L) with r = s − m ∈ 3A):
  - (s, x) with x ∈ B ∩ [h, m): s + x ≥ m + h = L, so it is an overflow token; e−1−a of them per s.
  - (s, u) with u ∈ B ∩ [1, h) (a of them per s) falls into one of three cases:
    - (a) s + u ≥ L: an overflow token;
    - (b) s + u < L and the token is unassigned;
    - (c) s + u < L and the token is assigned. Since s ≥ m > max A, s ∉ A, so (s, u) is a rep token of
      v = s + u ∈ (3A ∖ 2A) ∩ [m, L). Here v − m = r + u ∈ 3A + A ⊂ 4A, so v is counted by ω; and v ∉ 2A, so v ∉ Dset.
      Each v carries exactly 3 assigned tokens, so at most 3 tokens of type (c) point to the same v.
  - The overflow tokens (x′, x) with x′ ∈ B (OP of them) and (s′, x) with s′ ∈ 2A ∩ [m, L), x ∈ B ∩ [h, m) (that is
    (e−1−a)·P_lo) are disjoint from the tokens of types (a), (b) (different coordinates). Hence
    E3_L ≥ OP + (e−1−a)P_lo + #(a) + #(b).
  - ω counts Dset itself (u = 0) and the type-(c) values, which are distinct from Dset. So 3ω ≥ 3δ + #(c).
  - Since #(a) + #(b) + #(c) = a·δ: E3_L + 3ω ≥ OP + (e−1−a)P_lo + (a+3)δ. Substituting, the coefficient of δ is
    −e + (e−1−a) + a + 3 = 2. ∎
- Checked (E318): 0 violations on every real depth-four S of E317's ranges (exh k = 2..5; random k = 6, 8, 11).
- Third regime (3h ≤ m). The first window gives h ≤ t + β1·y0″ + p1. Here t = |3A_s ∩ [h, 2h)| with A_s = A ∩ [0, h),
  β1 = |B ∩ [h, 2h)|, y0″ = |2A_s ∩ [0, h)| and p1 ≤ P_hi. Also η ≤ β − β1, with β = e − 1 − a. With
  OP − P_hi ≥ P_hi − η this gives (PROVED):
  **W ≥ SP0 + (β − β1)(y0 − 1) + 2δ**, where SP0 = (a+1)·y0 − 3N4 − t + E1 (0 violations, E318).
  - SP0 ≥ 1 held on all real S and on all random local fakes.
  - But SP0 ≥ 0 is FALSE in the abstract: a B_3-like core C ⊂ [h/2, 2h/3) gives y0 = a + 1 and t ≈ C(a+1,2) + C(a+2,3).
  - So any proof must also use the high part, (β − β1)(y0 − 1), or the slack dropped in RED-A, namely
    G = E3_L − OVF_L (token collisions forced by one-dimensionality) and the other overflow tokens.

## Finite certificate: P18 depth four for e ≤ 6 (PROVED by complete enumeration, 2026-10-20; E319)
- **Bound (PROVED).** Depth four gives c ≤ 4m, so every Apéry element is < 5m. Hence it is a sum of at most 4 generators
  m + b, and its residue is the residue of a 4-fold sum of A. So m ≤ |4A| ≤ C(e+3, 4), and for fixed e the
  depth-four P18 semigroups form a finite list.
- Enumeration: src/scratch/p27/p18e.c (every B ⊂ [1, m−1] with |B| = e−1, gcd 1, Apéry set by Dijkstra; a 4-fold
  residue-cover prefilter, validated by reproducing the unfiltered counts).
  - e = 3: 26 S, min W = 7.
  - e = 4: 514 S, min W = 12.
  - e = 5: 12,184 S (m ≤ C(8,4) = 70; the largest m that occurs is 45), min W = 27.
  - e = 6: 367,234 S (m ≤ C(9,4) = 126 searched in full; m ∈ [76, 126] has none, the largest m is ≤ 75), min W = 37.
- So **P18 depth-four Wilf holds for e ≤ 6.** This is a checkable finite certificate (fejer ~/wilf/p25/p18e6_*.txt; 8 range
  jobs 7–60, 61–75, 76–85, 86–93, 94–100, 101–108, 109–117, 118–126).

## Near-simplex class NS is EMPTY (PROVED 2026-10-20); the formula below is vacuous
Class NS: P18 depth four with B ⊂ [1, h), 2B ⊂ [0, m) and 3B ⊂ [m, m + h).
- **Lemma NS0 (PROVED).** For m ≥ 4, no numerical semigroup S = ⟨m, m + B⟩ lies in NS.
  - Proof. Let b₋ = min B and b₊ = max B. From 3B ⊂ [m, m+h) and 2B ⊂ [0, m): 3b₋ ≥ m and 2b₊ < m.
  - (i) The Apéry element 4m + h − 1 = c + m − 1 is a sum of k generators m + b with b ∈ B (no generator m, since it
    is an Apéry element). So it equals km + s with s ∈ kB.
    - k ≤ 2 is impossible, since s < kh ≤ 2m.
    - k = 4 needs s = h − 1 ∈ 4B, but 4B ≥ 4m/3 > h.
    - k ≥ 5 gives s < 0.
    - So k = 3 and m + h − 1 ∈ 3B. Then m + h − 1 ≤ 3b₊ < 3m/2, i.e. h < m/2 + 1.
  - (ii) If h < m, the residue r = m − 1 has its Apéry element w ≤ 4m + h − 1, and w = km + s with s ∈ kB, s ≡ m − 1.
    - k = 1 is impossible, since B < h ≤ m − 1.
    - k = 3 would need s = 2m − 1 ∈ 3B ⊂ [m, m + h), i.e. h = m, which is excluded here.
    - k = 4 gives w = 4m + s with s ≡ −1 and s ≥ 4b₋ ≥ 4m/3, so s ≥ 2m − 1 and w > 4m + h − 1.
    - So k = 2 and m − 1 ∈ 2B ⊂ [2b₋, 2b₊]. Every residue of [h, m) has the same fate, so [h, m) ⊂ 2B, which forces
      h ≥ 2b₋ ≥ 2m/3. With (i), 2m/3 < m/2 + 1, i.e. m < 6. For m ∈ {4, 5} with h < m, direct check: none.
    - If h = m, (i) gives m < m/2 + 1, i.e. m < 2. ∎
  - Checked: random and constructed (B = x + U, 3U an initial interval) searches found no NS instance (E319).
- Consequence: the formula below concerns no semigroup. The "all-A carried near-simplex" model of the late-night
  NOTEBOOK heuristic (3B filling [m, m+h) with 2B < m) is therefore not realisable either. The additive-basis
  obstruction survives only in configurations where 2A meets [m, 2m) (carried pairs) or where B has high elements.
- (Original derivation, kept for the record:)
- Structure (PROVED): R_2 = R_3 = 2A, so [h, m) ⊂ 2B. The Apéry set is {0} ∪ (m + B) ∪ (2m + 2B) together with the layer-4
  elements 4m + r for r ∈ ((3B − m) ∖ 2A) ⊂ [0, h). Put N3 = |(3B − m) ∖ 2A|, ρ = m − h = |2A ∩ [h, m)|,
  ν = |2B ∩ [0, h)|, and assume 2B ∩ B = ∅ for simplicity. Then ℓ = 1 + e + |2A| + h − N3 and h = e + ν + N3, so
  **W = 3e(e−1) + (e−3)ρ + (2e−4)ν − 4N3.**
- Macaulay (TCM, j = 3): N3 ≤ |3B| ≤ (e−1)(e + ρ + ν)/3. This covers the e(e−1) and ν terms with room. The ρ term is
  not covered: the coefficient (4/3)(e−1) exceeds e − 3. So in NS, Wilf needs an additive input precisely when the
  interval [h, m) inside 2B is long (ρ ≳ 5e).
- The earlier "B_3-simplex model" (W = ρ − C(k+1,3)) is the extreme ρ = n2: a Sidon set whose sumset is an interval.
  That cannot exist, and the needed input is an **interval–collision principle**: a long interval I ⊂ 2A forces
  unused tokens (s, x), s ∈ I, since all of them point into I + B. Counting gives
  E3_L ≥ (e−1)ρ − 3|(I + B) ∩ (3A ∖ 2A)|, and |I + B| ≤ ρ + Σ_i min(g_i, ρ), with g_i the gaps of B.
  When the gaps are large, I can be covered by at most |B| pair sums, so ρ ≤ e. So the competition is elementary
  and needs no postage-stamp constants. (Heuristic; to be made a lemma.)
- Correction to the evening heuristic (NOTEBOOK): the "efficiency ≤ 3/4" requirement assumed 2B both Sidon and an
  interval. That assumption is self-contradictory, so the requirement does not follow.

## Order–level identity for generators in (m, 2m), every depth — PROVED 2026-10-20 (checks E320)
Setting: S = ⟨m, m + B⟩, B ⊂ [1, m−1], e = |B| + 1, c > m, depth q = ⌈c/m⌉ ≥ 2, h = c − (q−1)m ∈ (0, m].
For w ∈ Ap(S, m): level x(w) = ⌊w/m⌋. Order o(w) = the largest k with w a sum of k generators; no representation of an
Apéry element uses m, so o(w) = max{k : w − km ∈ kB}.
- H_j = #{w ∈ Ap : o(w) = j}. This is the Hilbert function of the standard graded algebra G = gr_𝔪(R/t^m R),
  R = k[[S]] (basis t^w, w ∈ Ap; t^w ∈ 𝔪^j + t^m R iff o(w) ≥ j). Here H_0 = 1 and H_1 = e − 1.
- E_k = (e−1)(H_0 + … + H_{k−1}) − k·H_k. These are ≥ 0 by the condensed Macaulay inequality
  (Eliahou JEMS 2018, Thm 5.11).
- T_c = Σ_{w ∈ Ap} (x(w) − o(w)) = g − Σ_w o(w) ≥ 0 is the total carry. It is 0 iff Eliahou's "true grading" holds
  up to level q.
- **Identity (PROVED; exact).** W = e(c − g) − c = Σ_{k=2}^{q−1} E_k + (e−1)·h − (e+q−1)·H_q − e·T_c.
  - Proof. Orders are ≤ levels ≤ q. So W = (e−1)c − e·g = (e−1)((q−1)Σ_j H_j + h) − e(Σ_j j·H_j + T_c).
  - Put n = e − 1. Telescoping gives Σ_{j ≤ q−1} H_j(n(q−1) − (n+1)j) = Σ_{k=1}^{q−1} E_k, with E_1 = n − H_1 = 0.
  - The j = q term is H_q(n(q−1) − (n+1)q) = −(n+q)H_q. ∎
  - At c = qm (h = m) it reads **W = Σ_{k=2}^{q} E_k − e·T_c**: the slack of condensed Macaulay minus e per unit of carry.
  - The free Hilbert function H_j = C(n+j−1, j) makes every E_k vanish. So "true grading ⇒ Wilf" is sharp there,
    and every carry costs exactly e.
- Carry-free case (recovers Eliahou Thm 7.1 inside this class). If T_c = 0, a nonzero product t^u·t^v in G has residue
  r_u + r_v with no wrap. So {t^w : r(w) ≥ h} spans an ideal, and the quotient has Hilbert function
  (#{w : o = j, r(w) < h})_j. Condensed Macaulay for the quotient at degree q gives q·H_q ≤ (e−1)(h − H_q), hence
  W ≥ 0. With carries this ideal property fails: **carries are exactly what breaks truncated Macaulay**, and the identity
  prices each unit of carry at e.
- Checked (E320, `src/scratch/p28/ordall.py`): 0 mismatches on 90k random S (e = 3, 4, 6; depths 3–59); E_k ≥ 0 on all.

## Depth four: the split W = J + σ and Conjecture J (lead, 2026-10-20; checks E320)
Depth four (q = 4). Carries are 0 or 1. Put:
- p = #{w : x = 3, o = 2} (carried pairs) and q₄ = #{w : x = 4, o = 3} (carried triples; residues < h);
- H4 = #{w : o = 4} (uncarried 4-sums; residues < h) and y = #{r < h : x_r ≤ 3}, so h = y + H4 + q₄;
- q_Q = #{carried triples w having a summand w − m − b (b ∈ B) that is a carried pair}.
- **Identity (PROVED).** W = E2 + E3 + (e−1)·y − 4·H4 − q₄ − e·p. This is the order–level identity with h = y + H4 + q₄.
- **RTCM on G (PROVED).** Let Q = the carried pairs in G_2. Their products with G_1 that are nonzero in G are Apéry
  elements of level ≥ 4 and order 3, i.e. carried triples, and each such product is counted in q_Q. Condensed Macaulay for
  G/(Q) at degree 3 gives σ := E3 − (e−1)p + 3q_Q ≥ 0.
- **Split:** W = J + σ with **J := E2 + (e−1)·y − 4·H4 − q₄ − 3·q_Q − p**.
- **Conjecture J (CONJ).** J ≥ 0 for every P18 depth-four S. It implies P18 depth-four Wilf and uses no degree-3 Macaulay.
  - Data (E320): 0 failures — exhaustive e = 4 (m ≤ 40), e = 5 (m ≤ 30); random e = 6, 9; annealing (anJ.c, m ≤ 300,
    e ≤ 21).
  - Sharp: J = 0 at ⟨15, 18, 19, 25⟩ (B = {3, 4, 10}, h = 3 ≤ e). For h > e the minimum found is J = 1 at
    ⟨9, 10, 16⟩ (h = 7), and J = 2 at ⟨17, 21, 29, 31, 32⟩ (h = 7, p = 7), the RES4-sharp example.
  - Meaning: after Macaulay, each carry costs about one unit. Carried pairs and carried triples each cost 1, plus 3 for a
    triple grown from a carried pair; uncarried order-4 elements cost 4. These are paid by the low window, (e−1) per
    residue below h of level ≤ 3, and by the pair-collision slack E2.
  - The weaker J0 (q_Q replaced by q₄) is FALSE: −10 at ⟨21, 25, 28, 30, 31⟩. Carried triples that do not grow from a
    carried pair must stay cheap.

## Power tokens: an elementary condensed Macaulay and the exact form W = U − e·T_c (every numerical semigroup) — PROVED 2026-10-20 (checks E320)
Setting: any numerical semigroup S ≠ N with multiplicity m and minimal generators m, g_1, …, g_{e−1}. Ap = Ap(S, m).
level x(w) = ⌊w/m⌋. Order o(w) = the largest number of minimal generators summing to w; m is never used, since w − m ∉ S.
H_j = #{w ∈ Ap : o(w) = j}. Carry t(w) = x(w) − o(w) ≥ 0 (every g_b has level ≥ 1) and T_c = Σ t(w) = g − Σ_w o(w).
c = (q−1)m + h with 0 < h ≤ m.
- **Lemma PT (power tokens; PROVED, elementary).** A power token is (u, b, k) with u ∈ Ap, b ∈ {1,…,e−1} and k > o(u).
  Its target is u + (k − o(u))·g_b. For each w ∈ Ap of order k, fix one maximal-order representation, with multiplicities
  a_b. Let w use the k tokens (w − j·g_b, b, k), 1 ≤ j ≤ a_b. Each first coordinate w − j·g_b is a summand of w, so it
  lies in Ap, and its order is exactly k − j (a longer representation would lengthen w's).
  - A token determines its target, so no token is used twice. Hence k·H_k ≤ (e−1)(H_0 + … + H_{k−1}). This is
    Eliahou's condensed Macaulay inequality for G = gr(R/t^m R), with a one-line proof.
  - **E_k = (e−1)Σ_{i<k}H_i − k·H_k is exactly the number of unused degree-k tokens.** In particular every dead token (target
    not an Apéry element of order k) is unused.
  - (The same map (u, b) ↦ u·x_b^{k−deg u} proves condensed Macaulay for any order ideal of monomials, hence, through an
    initial ideal, for every standard graded algebra.)
- **Theorem (exact form of Wilf).** W(S) = U − e·T_c. Here U is the number of unused power tokens of degrees
  2 ≤ k ≤ q−1, together with the unused degree-q tokens whose first coordinate has residue < h.
  - Proof: the order–level identity (previous section; its derivation never used P18) gives
    W = Σ_{k=2}^{q−1} E_k + (e−1)h − (e+q−1)H_q − e·T_c.
  - Every order-q element has level q, so it is uncarried with residue < h, and so are its token sources. Hence
    (e−1)h − (e+q−1)H_q = (e−1)·#{r < h : o(w_r) ≤ q−1} − q·H_q is the number of unused degree-q tokens from residues
    < h. ∎
- **Own dead tokens (PROVED).** Let u be carried, with order d and carry t. In each of t consecutive degrees, all e − 1
  tokens of u are dead. The degrees are k ∈ [q−t+1, q] if r(u) < h, and k ∈ [q−t, q−1] if r(u) ≥ h (then x(u) ≤ q−1).
  - Reason: levels are superadditive, so the target has level ≥ k + t. That is > q, or it equals q at a residue ≥ h.
  - Hence U ≥ U_unc + (e−1)·T_c, where U_unc counts unused tokens with uncarried first coordinate, and
    **W ≥ U_unc − T_c: after Macaulay, each unit of carry costs exactly one token.**
- Checked (E320, `src/scratch/p28/carry.py`): W = U − e·T_c and the own-token bound on 84k random semigroups
  (generators in (m, 4m) and P18; depths 2–140), 0 failures.
- The **Carry Lemma** T_c ≤ U_unc is FALSE in general. It fails often at depth ≥ 4 for general S, and at depth ≥ 7 in
  P18; e.g. e = 2, ⟨37, 144⟩ has W = 0 with U = 2T_c, so the carried elements own far more than (e−1)t dead tokens.
  At P18 depth four it held exhaustively (e ≤ 5, min slack 6, 10, 21) and under annealing (in progress).

## P18 depth four in token form (lead, 2026-10-20)
Notation: p = p_lo + p_hi carried pairs (level 3, order 2; residue < h or ≥ h); q carried triples (level 4, order 3);
H4 order-4 elements; y0 = |3A ∩ [0,h)| uncarried residues < h; U_k = unused degree-k tokens with uncarried first coordinate;
χ3 = degree-3 tokens with carried first coordinate that carried triples use.
- **Exact:** W = E2 + U3 + U4 − p − q + [(e−1)p_lo − χ3]. The bracket is ≥ 0, since every carried first coordinate of a
  degree-3 token used by a carried triple is a low carried pair, and each has e − 1 tokens.
  - Here U2 = E2, U4 = (e−1)y0 − 4H4, and U3 = E3 − (e−1)p + χ3.
- **Lemma C3hi (PROVED).** p_hi ≤ U3. Map a high carried pair with chosen representation {b ≤ b′} (b + b′ = m + r, r ≥ h)
  to the generator token (g_b, b′, 3). Its target 3m + b + 2b′ has residue r + b′ ≥ h at level 4, or level ≥ 5, so the
  token is dead; the map is injective.
  - The same token is dead for every carried pair once 2h ≤ m, since then b′ ≥ m/2 ≥ h. So **p ≤ U3 when 2h ≤ m.**
- **C4 alone is FALSE:** q + 4H4 ≤ (e−1)y0 fails at a = 0, e.g. m = 83, B = {20,21,22,25,28,31,34,37,39,81,82}, h = 18:
  y0 = 1, q = 17, C4 = −6, W = 441. The carried triples there are paid by degree-3 overflow (U3 − p = 407).
- **Conjecture CL4 (carry lemma at P18 depth four):** p + q ≤ E2 + U3 + U4. It implies Wilf, since W ≥ CL4 slack.
  - Exhaustive e ≤ 5: min slack 6, 10, 21; annealing in progress.
- **Conjecture M (inside matching; CONJ, 2026-10-20).** At P18 depth four there is an injection φ from the carried Apéry
  elements to unused power tokens such that:
  - the first coordinate of φ(v) is a proper sub-sum of v's chosen representation (0 allowed);
  - φ(v) is either a token with uncarried first coordinate, or a spare token of a carried sub-sum (or of v), i.e. one
    beyond the e − 1 forced dead tokens.
  - M implies CL4, hence P18 depth-four Wilf.
  - Data (E320, match4.py, bipartite matching): saturating on every S tested (exh e ≤ 5, random e = 7, 9, 12, the C4
    counterexamples).
  - Partial canonical choices (PROVED):
    - high carried pairs ↦ (g_b, b′, 3) (Lemma C3hi);
    - carried triples with a sub-pair b_i + b_j < h ↦ (u_{ij}, b_k, 4). Its target u_{ij} + 2g_{b_k} has level ≥ 5, and
      the map is injective because the token determines v = u_{ij} + g_{b_k}.
  - Open: low carried pairs whose token (g_b, b′, 3) is used (then b ≤ b′ < h and 2h > m), and carried triples with
    every sub-pair ≥ h.
  - For the latter, the overflow tokens (u_s, x, 3), s + x ≥ m + h, of a parent pair element u_s number
    |B ∩ [m − s + h, m)|, while the triples through u_s number at most |B ∩ [m − s, m − s + h)|. A Hall argument has to
    use the covering of [h, m) to rule out B clustering in such windows.
- **Lemma PI (all carried pairs; PROVED 2026-10-20).** P18 depth four. For a carried pair v with chosen representation
  {b ≤ b′} (b + b′ = m + r), put π(v) = (g_b, b′, 3) if b′ ≥ h, and π(v) = (g_b, b′, 4) if b′ < h.
  - π(v) is a dead token with uncarried first coordinate g_b, inside v, and π is injective.
  - Case b′ ≥ h: the target 3m + b + 2b′ has b + 2b′ = m + r + b′. Either it is ≥ 2m (level ≥ 5), or its residue
    r + b′ ≥ h sits at level 4. Neither is an Apéry element.
  - Case b′ < h: then b < h, so the degree-4 token is in the pool. Its target 4m + b + 3b′ has b + 3b′ ≥ m + 2b′ > m, so
    it has level ≥ 5.
  - Injectivity: the token determines (b, b′), hence the representation, hence v.
- So Conjecture M at depth four reduces to the **residual class R**: carried triples {b1 ≤ b2 ≤ b3} with b1 + b2 ≥ h.
  - Every other carried element is matched injectively and disjointly: pairs by π (generator first coordinates), triples
    with b1 + b2 < h by ρ = (u_{12}, b3, 4) (pair first coordinates).
  - **Conjecture M′ (CONJ):** R can be matched inside into the unused tokens and spares not in im π ∪ im ρ.
  - Data (E320, mres.py): π and ρ are always unused and distinct (0 failures). Residual Hall has 0 failures (exh e ≤ 5;
    random e = 9, 12); max |R| = 14.
  - The residual matching uses almost only first coordinate 0, the tokens (0, x, k), k = 2, 3, 4, with a few generator
    and pair tokens in core-like S.
  - Obstacle to a pure count: in the core regime |R| ≈ h − e can reach about e(e−1), so tokens determined by ≤ 2
    elements must be spread over triples. The natural per-pair charge (each triple to the overflow tokens of its largest
    sub-pair) fails exactly when B has more elements in [m − s, m − s + h) than in [m − s + h, m).

## Conjecture M (inside matching of the carry deficit), every numerical semigroup (lead, 2026-10-20; checks E321)
Setting: any S with multiplicity m and depth q. Use the Apéry orders, levels and carries t = level − order. Power tokens
(u, b, k), 2 ≤ k ≤ top(u), with top(u) = q if r(u) < h and q − 1 otherwise; chosen representations via parent pointers.
"Used" and "unused" are as in Lemma PT.
- Supply:
  - each unused token with uncarried first coordinate has capacity 1;
  - each carried u has spare(u) = #unused(u) − (e−1)·t(u) ≥ 0 (own-dead-token lemma).
- Demand: each carried v needs t(v).
- By W = U − e·T_c (PROVED), **total supply − total demand = W exactly**, so Wilf ⟺ supply ≥ demand.
- **Conjecture M:** there is a flow meeting every demand t(v) using only supply inside v. That means unused tokens whose
  first coordinate is an uncarried proper sub-sum of v's chosen representation, together with spares of carried proper
  sub-sums or of v itself. M ⟹ Wilf, and M is a local strengthening of it.
  - Data (E321):
    - P18: 0 failures, depths 2–37 (`matchq.py`, about 11k S).
    - Narrow form (first coordinates only 0 and the generators of v): 0 failures for P18 depth ≤ 12.
    - General S, generators in (m, 4m): 0 failures, depths 2–12 (`matchq.py` 5k S; C tool `genM.c`, max-flow, with the
      self-check supply − demand = W).
    - For e = 2 every S has W = 0, so the flow must be perfect, and it is.
  - Why it is plausible: the forced dead tokens of a carried element already pay e − 1 of each e units of carry. The
    remaining unit is found among the overflow and collision tokens of its own sub-sums.
  - Expected failure mode (to test): a large cluster of generators whose carried 3-sums outnumber the dead tokens of all
    its sub-sums. In P18 depth four the zero-token-only version (R3) already fails (third regime, e = 14: |R| = 49 > 23),
    yet the full residual Hall condition held there.

## (★★) for the P18 depth-four residual — FALSE (2026-10-20; E321)
- Statement: |R| + p ≤ (a+1)·#{x ∈ B : 3x ≥ h} + #{(b, x) ∈ B² : b + 2x ≥ m + h}.
- What is PROVED: W ≥ slack(★★). The G4 tokens (u, x, 4) with u ∈ {0} ∪ {g_b : b < h}, 3x ≥ h, and the D3 tokens
  (g_b, x, 3) with b + 2x ≥ m + h are dead, distinct, uncarried, disjoint from im ρ, and contain im π.
- Counterexample: m = 75, B = {7, 8, 9, 10, 11, 12, 19, 69}, h = 75 (c = 4m). Here a = 8, |R| = 5, p = 8, the G4 count is
  9 and D3 = 3, so slack = −1, while W = 501.

## Twin tokens and Conjecture DEAD, every numerical semigroup (lead, 2026-10-20; checks E322)
Setting as in "Power tokens".
- Notation:
  - top(u) = q if r(u) < h, else q − 1.
  - L_u = top(u) − x(u), the number of left elements in u's residue class; ℓ = Σ_u L_u.
  - λ(u, b) = max{j ≥ 0 : u + j·g_b ∈ Ap}, and μ_b(z) = max{j : z − j·g_b ∈ S}.
  - Λ = Σ_{u∈Ap} Σ_b λ(u, b) = Σ_{z∈Ap} Σ_b μ_b(z), by double counting the pairs u, u + j·g_b ∈ Ap. O = Σ_z o(z).
- **Lemma RAY (PROVED).** λ(u, b) ≤ L_u.
  - Put j = L_u + 1. Then u + j·g_b has level ≥ x(u) + j = top(u) + 1.
  - If r(u) < h, that level exceeds q.
  - If r(u) ≥ h, the level is ≥ q. Equality forces every step to raise the level by exactly 1, with no wrap, so the
    residue is ≥ r(u) ≥ h. Then the element is ≥ qm + h > max Ap.
  - Consequence: the dead tokens on the ray (u, b) are exactly j = k − o(u) ∈ (λ(u, b), top(u) − o(u)]. The top t(u)
    of them are u's forced dead tokens (own-dead lemma). The other s(u, b) := L_u − λ(u, b) ≥ 0 are **slots**.
- **Identities (PROVED).**
  - #dead pool tokens = (e−1)(c − O) − Λ.
  - #alive unused pool tokens = Λ − O ≥ 0. (A target z receives Σ_b μ_b(z) alive tokens and uses o(z) of them;
    generators contribute 0.)
  - With W = U − e·T_c this gives **W − (Λ − O) = #dead − e·T_c = Σ_{u,b} s(u, b) − T_c**.
  - Moreover Σ_u s(u, b) = ℓ − Λ_b, where Λ_b = Σ_z μ_b(z) = Σ_{j≥1} rank(x_b^j on k[S]/(t^m)). The g_b-chains in
    Ap are the Jordan blocks of multiplication by t^{g_b}.
- **Conjecture DEAD (CONJ; 0 failures for genus ≤ 34).** For every numerical semigroup S ≠ ℕ, **W(S) ≥ Λ − O**.
  Equivalent forms (equivalences PROVED above):
  - (i) the dead power tokens alone number ≥ e·T_c;
  - (ii) (e−1)·ℓ ≥ Λ + T_c, i.e. Σ_b (ℓ − Λ_b) ≥ T_c;
  - (iii) e·ℓ − c ≥ Σ_{z∈Ap} (Σ_b μ_b(z) − o(z)).
  - DEAD ⟹ Wilf, since Λ ≥ O.
- If every Apéry element has a unique factorization (staircase S), then μ_b = a_b, so Λ = O
  and **DEAD ⟺ Wilf** for that S. So DEAD adds exactly the collision count Λ − O.
  - Correction (2026-10-20): e ≤ 3 does NOT imply unique Apéry factorizations. In S = ⟨5, 6, 9⟩, 18 ∈ Ap(S, 5)
    (13 ∉ S) and 18 = 6+6+6 = 9+9, so μ_6(18) + μ_9(18) − o(18) = 3 + 2 − 3 and Λ − O = 2 (lead-verified).
    DEAD ⟺ Wilf is established only for staircase S, not for all e ≤ 3.
- **Symmetric S (PROVED).** μ_b(z) ≤ o(z) gives Λ ≤ (e−1)·O. Hence Λ − O ≤ (e−2)·O ≤ (e−2)·g = W.
  - Per direction, the reflection γ = z − km ↦ y = F + o(z)·m − γ = (M − z) + (o(z) + k − 1)·m (M = F + m) is an
    injection from high gaps (1 ≤ k ≤ t(z)) into the slots of every direction b. The slot condition holds because
    λ(M − z, b) = μ_b(z) ≤ o(z). So ℓ − Λ_b ≥ T_c for every b.
- Equality and sharpness (E322):
  - For e ≥ 3, equality occurs exactly d(g) − 1 times per genus up to 34. That count matches ⟨m, km+1, …, km+m−1⟩
    (W = 0, Λ = O).
  - Shifted intervals ⟨m, a, …, a+d⟩ with a ≈ 4m/3 and d ≈ m/3 have (Λ − O)/W → 1 (0.971 at m = 120) with
    W − (Λ − O) ≈ e + 3. So no inequality W ≥ (1+ε)(Λ − O) holds.
- Local refinements — all FALSE (E322):
  - PERB, (e−1)·min_b (ℓ − Λ_b) ≥ T_c;
  - CHAIN, the per-g_b-chain version Σ_C s ≥ Σ_C (t − t(base));
  - BASE, Σ_b Σ_z t(z − μ_b(z)g_b) ≤ (e−2)T_c;
  - reflection through the maximal Apéry elements, both as a fixed-offset matching and as a flow into the slot
    capacities;
  - monotonicity of W − (Λ − O) along the semigroup tree.
- **Lemma TW (twin tokens; PROVED).** Let v be carried, with carry t and forced degrees D(v). Let b ∈ supp(v)
  (chosen representation) and u = v − g_b.
  - For k ∈ D(v), the token (u, b, k) has the same target as (v, b, k), so it is dead.
  - It is a slot iff k ≤ top(u) and (t(u) = 0 or k ∉ D(u)).
  - The pair (u, b) determines v, so twins of distinct carried elements are distinct.
  - With the chosen b, v gets min(t(v), t(v) − t(u) + top(u) − top(v)) fresh slots.
  - At P18 depth four the twins reproduce ρ exactly, and π except on low carried pairs with b′ ≥ h. The residual R is
    where every twin leaves the pool (all sub-pair residues ≥ h) or lands in a carried pair's forced set.
  - In general the unit set Δ without a fresh twin is a large fraction of T_c at high depth. The slots DEAD needs come
    from excess jumps further along the rays: s(u_i, b) = top(u_i) − x(u_L) + Σ_{j>i} ex(u_j) on a g_b-chain
    u_0, …, u_L, where ex(v) = x(v) − x(v − g_b) − 1.

### DEAD: slot intervals, the degree-graded family DOWN, and the inside matching MD (lead, 2026-10-20; checks E322)
- **Interval picture (PROVED; restates Lemma RAY).** For u ∈ Ap put α(u) = top(u) − t(u) = o(u) + L_u, and for each
  direction b put A_b(u) = o(u) + λ(u, b) ≤ α(u).
  - The b-slots of u are the tokens of degrees k ∈ (A_b(u), α(u)].
  - u's forced dead tokens and its carry units are the degrees (α(u), top(u)].
  - Let u′ = u + g_b ∈ Ap with o(u′) = o(u) + 1. Then A_b(u′) = A_b(u), and (u, b, k), (u′, b, k) have the same target.
    So on a g_b-chain with unit order steps, all degree-k tokens share one target. They are dead iff k > A_b, and each is
    a slot or forced according as k ≤ α or not.
- **DEAD for c ≤ 2m (PROVED, elementary).** With c = m + h:
  - [h, m) ⊂ A (the level-one residues). Level-two Apéry elements have residue < h; they are pairs P (order 2) or
    generators G2 (carry 1). With a = |A ∩ [1, h)|, ℓ = 2 + a and e − 1 = a + (m − h) + |G2|.
  - Collisions come only from pairs of A_low, so Λ − O ≤ a² + a − 2|P|. With |P| + |G2| = h − 1 − a this gives
    **W − (Λ − O) ≥ (m − h)(1 + a) + a·|G2| ≥ 0.**
- **Reflection is degree-monotone (PROVED).** Let M ≥_S v be a maximal Apéry element and u = M − v. Then
  L_v ≥ x(u) ≥ o(u) and L_u ≥ x(v), because v + (x(u) − 1)m ≤ M − m < c.
  - Hence, if λ(u, b) ≤ o(v), the b-slots of u at degrees o(u) + o(v) + i (1 ≤ i ≤ t(v)) exist. Each lies at or
    below the degree o(v) + L_v + i of v's i-th carry unit.
  - Failures of reflection are therefore only the direction condition and collisions. Example: maximal carried
    elements all reflect to u = 0.
- **Conjecture DOWN (CONJ; 0 failures for genus ≤ 33).** For every K:
  #{slots of degree ≤ K} ≥ #{carry units of degree ≤ K}.
  - K = q is DEAD.
  - By nestedness, DOWN ⟺ there is an injection from carry units to slots that never raises the degree.
  - The per-degree and from-above versions are FALSE (E322). Twins are degree-preserving.
  - Analogy: PGW (prefix Wilf) is the level-graded analogue for gaps versus left elements.
- **Conjecture MD (CONJ; 0 failures for genus ≤ 19 and on random S).** Each carry unit (v, k) can be matched injectively
  to a slot (u, b, k′) with u a sub-sum of v's chosen factorization (u = 0 and u = v allowed) and k′ ≤ k.
  - TMD: the same after first fixing one fresh twin per unit; also 0 failures.
  - MD ⟹ DOWN ⟹ DEAD ⟹ Wilf.
  - This is a purely "descent" (inside) statement; the classical FGH reflection is not used.
  - In matchings found by search, leftover units mostly take the element's OWN lower slots (v, b, k′ ≤ α(v)). Elements
    with L_v = 0 (no left element in their class) take slots of v − g_b in other directions.

### Conductor-free versions: XWILF (CONJ, fragile) and XDEAD (FALSE) (lead, 2026-10-20; checks E322)
- **General reflection lemma (PROVED).** If u + w = v ∈ Ap, then L_u ≥ x(w), because u + (x(w) − 1)m ≤ v − m < c.
  So X(u) := max{x(w) : u + w ∈ Ap} ≤ L_u, and ℓ ≥ Σ_u X(u).
- **XWILF:** (e−1)·Σ_{u∈Ap} X(u) ≥ g. Equivalently e·g ≤ (e−1)·Ĉ with Ĉ = Σ_u max_{u+w∈Ap}(x(u) + x(w)) ≤ c. Wilf
  itself is e·g ≤ (e−1)·c, so XWILF replaces the conductor by an Apéry-poset surrogate. XWILF ⟹ Wilf.
  - PROVED when type ≤ e − 1. In the down-set D(M) of a maximal M, u ↦ M − u gives Σ_{D(M)} X ≥ Σ_{D(M)} x; then
    cover Ap by the t sets D(M). This is FGH in X-form, and it covers every e ≤ 3.
  - No cover by reflections can do better: each maximal M lies only in D(M), so 0 gets load t.
  - Data: every S of genus ≤ 32, 0 failures. Equality also OUTSIDE the Wilf-equality family: ⟨9, 14, 15, 17⟩ (type 5,
    XW = 0, W = 6).
  - Fragility. In the "all pairs wrap" regime S = ⟨m, m + R⟩, R ⊂ (m/2, m), {0} ∪ R ∪ (R + R − m) = ℤ/m, XWILF reads
    3(m − 1 − k) ≤ k² + 2k, i.e. m ≲ k²/3. That is a restricted 2-basis (postage-stamp, h = 2) bound. Known 2-bases reach
    about (2/7)k², and the best upper bound known is about 0.48k². So XWILF would imply a new additive-basis bound
    (UNVERIFIED citations, from memory). Wilf (m ≲ 2k²/3) and DEAD (m ≤ k² + k) are comfortable there.
  - Exhaustive in that regime: k ≤ 5 (m ≤ 40), k = 6, 7 (covering sets): 0 XWILF failures.
- **XDEAD: Σ_{u,b} (X(u) − λ(u, b)) ≥ T_c — FALSE.** Counterexample ⟨27, 41, 42, 43, 46, 49, 52, 53⟩ (genus 64): XDEAD
  slack −2, XWILF slack 6, DEAD slack 33. Confirmed by an independent brute-force script (`verify_xd.py`), which also
  re-confirms the DEAD identity slots − T_c = W − (Λ − O) there.
- XRAY, g ≤ Σ_b Σ_u x(λ(u,b)·g_b) (single-direction partners only), is FALSE (885/1837 random S).

### P18 depth four through DEAD: slot counts by first coordinate (lead, 2026-10-20; checks E324)
- Setting: P18 depth four, k = e − 1, a = |B ∩ [1, h)|. Slots of the level ≤ 2 elements:
  - of 0: Z = Σ_x (4 − λ(0, x));
  - of the generators: G = Σ_{b,x} (L_b − λ(g_b, x)), with L_b = 3 (b < h) or 2 (b ≥ h);
  - of the uncarried pairs: P = Σ_u Σ_x (L_u − λ(u, x)).
- These are disjoint sets of slots, and ρ injects the triples with a sub-pair < h into pair slots. Hence each of the
  following implies DEAD at P18 depth four, hence **Wilf for P18 depth four**:
  - S2: p + q ≤ G;
  - S3: p + q ≤ Z + G;
  - S5: p + q ≤ G + P;
  - ZG: p + |R| ≤ Z + G;
  - ZGP: p + q ≤ Z + G + P.
  No matching is needed: DEAD is a count.
- **Exact form of S2 (PROVED identity):**
  - G = k² + a·k + D1 − N2 − N3, with D1 = #{(b, x) : g_b + g_x ∉ Ap} and N_j = #{(b, x) : g_b + j·g_x ∈ Ap}.
  - So S2 ⟺ k² + a·k + D1 ≥ N2 + N3 + p + q.
  - N3 only counts b < h, since b + 3x < h is needed.
- Data (E324):
  - exhaustive e = 4 (m ≤ 50) and e = 5 (m ≤ 36): min slack S2 2, 3; S3 5, 9; S5 4, 11; ZG 6, 9; ZGP 8, 17;
  - random e = 9, 15: min S2 49, 222.
  - Annealing on G/(p+q) (p + q ≥ 10): best 1.56 at e = 20 (q ≈ 0.72k², G ≈ 1.42k²); larger m running.
  - FALSE: P2 (p + q ≤ P; −9, −14) and S4 (generator slots of dead pairs only).
- Heuristic risk: q can be ~k³ in principle, but carried triples need wraps, and the covering of [h, m) at level ≤ 3
  limits wrapped structure. Free (Sidon-like) B with 4·max B < m has no wraps at all, so T_c = 0.
- **Theorem BIG (PROVED 2026-10-20; P18 depth four with B ⊂ (m/2, m)).** Let S = ⟨m, m + B⟩ with B ⊂ (m/2, m) and
  3m < c ≤ 4m. Then G ≥ k² ≥ T_c, hence DEAD and Wilf hold (W ≥ Λ − O + k² − T_c).
  - Proof:
    1. Every pair sum lies in (m, 2m), so g_b + g_x = 3m + (b + x − m) has level 3. There are no level-two elements.
    2. Every triple sum lies in (3m/2, 3m). Level 4 occurs only for sums < 2m, with residue in (m/2, m). So every
       level-four residue lies in (m/2, h).
    3. Every residue r ∈ (0, m/2] is not in B and not of level 4, so it has level 3. That level holds only wrapped
       pairs, so r ∈ B + B − m. Hence ⌊m/2⌋ ≤ |B + B| ≤ k(k+1)/2, so m ≤ k(k+1) + 1.
    4. The nonzero non-generator Apéry elements are wrapped pairs (level 3, order 2) and triples (level 4, order 3).
       Four-fold sums have level ≥ 6. So each is carried once and T_c = m − 1 − k ≤ k².
    5. Each ordered pair (b, x) has a dead generator slot. If b ≥ h, g_b + 2g_x has b + 2x > m + h, so it is not
       Apéry (L_b = 2). If b < h, g_b + 3g_x has b + 3x > 2m, so it has level ≥ 5 (L_b = 3). Hence G ≥ k².
- **Decomposition (PROVED identity).** G = k² − F_full + E, where:
  - F_full = #{(b, x) : λ(g_b, x) = L_b} counts the rays with no slot;
  - E = Σ (L_b − λ − 1)^+ counts the extra slots.
  - So S2 ⟺ T_c + F_full ≤ k² + E.
- **Conjectures TF / TFZ.**
  - TF: T_c + F_full ≤ k². Fails once in the data, at k = 3: m = 15, B = {7, 9, 10}, h = 14, −1. Exhaustive k = 4:
    min 0. Random k = 9: min 48.
  - TFZ: T_c + F_full ≤ k² + Z. 0 failures (min 2, 4, 67).
  - TFZ ⟹ S3 ⟹ DEAD ⟹ Wilf at P18 depth four. P18 depth four is certified for e ≤ 6, so TF for k ≥ 6 would
    suffice.
  - Proof idea: inject carried elements and full rays into B × B. Full rays map to themselves and carried pairs to
    their π pair (non-full, injective). Open: carried triples.
- **S2, S3, TF, TFZ are FALSE for large e (2026-10-20; E325).** Construction sym(t, u):
  - D = [0, t) ∪ t·[0, t) ∪ t²·[0, u), with 2n = u·t².
  - X = D ∪ (2n − 1 − D), B = n + X, m = 4n.
  - Fillers: add the uncovered residues until depth ≤ 4. None were needed for t = u ≤ 50.
  - Then B ⊂ [m/4, 3m/4), so 4B ∩ [0, m) = ∅ and every level-four residue is a carried triple. T_c grows like m ≈ k³/108,
    while Z + G ≤ 4k + 3k².
  - t = u = 40: m = 128000, e = 237, h = 95959, T_c = 91983, Z + G = 86094, so S3 = −5889 and S2 = −6346.
    DEAD margin 2,598,811; W = 4,205,531.
  - t = u = 50: m = 250000, e = 297, S3 = −46342.
  - TFZ already fails at t = 30 (m = 54000): −8230.
  - Consequence: no argument using only the slots of 0 and of the generators can prove DEAD (or Wilf) at P18 depth four.
    Slots of higher elements, or a different mechanism, are required in the regime m ≫ k².

## P18 depth four: layer form, the universal inequality Q3, and the reduction to STAR (lead, 2026-10-20; checks E325)

Setting: S = ⟨m, m + B⟩, B ⊂ [1, m − 1], |B| = k, e = k + 1, A = {0} ∪ B.
- Layers: S_j = {r ∈ [0, m) : jm + r ∈ S}.
  - Exact recursion (every nonzero element of S minus some generator lies in S):
    S_{j+1} = S_j ∪ (S_j + B)_{<m} ∪ ((S_{j−1} + B)_{≥m} − m).
  - So S_1 = A, S_2 = (A + A) ∩ [0, m), and S_3 = S_2 ∪ (S_2 + B)_{<m} ∪ ((A + B)_{≥m} − m).
  - The level of residue r is min{j : r ∈ S_j}.
- Depth four (3m < c ≤ 4m) means S_4 = [0, m) ≠ S_3. Write h = c − 3m. Then h − 1 = max([0, m) ∖ S_3), and [h, m) ⊂ S_3.
- Notation:
  - U2 = S_2 ∖ S_1, N3 = S_3 ∖ S_2, D = [0, m) ∖ S_3 ⊂ [0, h).
  - d_j = |S_j ∖ S_{j−1}|, so d2 = |U2|, d3 = |N3|, d4 = |D|.
  - L3 = |S_3 ∩ [0, h)| = h − d4.
  - P_u, P_w = numbers of multisets {x, y} ⊂ B with x + y < m, resp. ≥ m. P_u + P_w = k(k+1)/2.
- **Identity (PROVED).**
  - ℓ = |S_0| + |S_1| + |S_2| + L3 = 2k + 3 + d2 + L3, and c = 3m + h with m = 1 + k + d2 + d3 + d4.
  - Hence W = Q3 + Q4, where Q3 = 2k² + 2k + (k − 2)·d2 − 3·d3 and Q4 = k·L3 − 4·d4.
  - Equivalently, Wilf ⟺ (k + 1)(|S_0| + |S_1| + |S_2| + |S_3|) + k·h ≥ (k + 4)·m. At depth q in general, P18 Wilf ⟺
    (k+1)·Σ_{j<q} |S_j| + k·h ≥ (k + q)·m.
- **Theorem Q3 (PROVED; no depth hypothesis; every B ⊂ [1, m−1]).** 3·d3 ≤ 2k(k+1) + (k − 2)·d2.
  - Proof.
    1. N3 = T ∪ R, where T = new unwrapped triples (3A ∩ [0, m)) ∖ S_2 and R = ((A + B)_{≥m} − m) ∖ S_2. Then |R| ≤ P_w.
    2. For t ∈ T, write t = x + y + z with x, y, z ∈ B. A zero summand would put t in S_2. The three pair sums are < m.
       They lie in U2: if x + y ∈ A, then t ∈ A + A.
    3. Let P(t) be the set of pair sums of a chosen representation. Each s ∈ P(t) gives an incidence (s, t − s) ∈ U2 × B,
       and incidences of different t are distinct. So Σ_t |P(t)| ≤ k·d2.
    4. Choose a representation with distinct summands when one exists. Then 3 − |P(t)| is 0; or 1 for t = 2x + z
       (x ≠ z), injectively to the ordered pair (x, z) with x + z < m; or 2 for t = 3x, injectively to x with 2x < m.
       So Σ_t (3 − |P(t)|) ≤ 2·P_u.
    5. Combining with d2 ≤ P_u: 3·d3 ≤ k·d2 + 2P_u + 3P_w = (k − 2)d2 + 2d2 + 2P_u + 3P_w ≤ (k − 2)d2 + 4P_u + 4P_w
       = (k − 2)d2 + 2k(k+1). ∎
  - Equality holds for free B (all sums distinct, no wrap). So Q3 is a sharp Plünnecke-type linear inequality.
- **Corollary (PROVED).** P18 depth four with 4·d4 ≤ k·L3 (equivalently d4 ≤ k·h/(k + 4)) satisfies Wilf.
  Q4 < 0 occurs: 44 of the 514 S with e = 4, and 127 of the 11,895 S with e = 5.
- **Exact four-term split (PROVED).** W = G_T + G_R + G_4 + F, where:
  - G_T = 4P_u − 2d2 + J_< − 3|T| ≥ 2(P_u − d2) + (2P_u − D1 − 2D0) + (J_< − Σ|P(t)|) ≥ 0;
  - G_R = 4P_w − 3|N3 ∖ T| ≥ P_w;
  - G_4 = J_≥ + k·|N3 ∩ [0, h)| − 4·d4;
  - F = k(1 + |B ∩ [0, h)| + |U2 ∩ [0, h)|);
  - J_≥ = #{(s, b) ∈ U2 × B : s + b ≥ m} and J_< = k·d2 − J_≥.
- **Conjecture STAR (0 failures; E325).** STAR := P_w + J_≥ + k·L3 − 4·d4 ≥ 0, i.e. (k + 4)·d4 ≤ k·h + J_≥ + P_w.
  - STAR is exactly the part of W that remains after the PROVED level-three slack: W = STAR + G_T + (G_R − P_w).
  - So **STAR ⟹ Wilf for P18 depth four** (DKM Problem 1.8 at depth four).
  - Why STAR is plausible: every level-four residue r < h lies in (N3 ∩ [0, h)) + B or in (U2 + B) − m. These are
    exactly the incidences counted by k·L3 and J_≥.
  - A wrapped-triple residue r + m = x + y + z has at most 3 such parents. So the deficit (≥ 1 per carried triple) must
    be paid by wasted incidences (from S_2 ∩ [0, h), from N3 ∩ [0, h), wrapped U2-incidences into S_3) and by P_w.
  - Local versions fail:
    - RESs (only incidences that land in D, plus F and P_w): −2 at m = 13, B = {3, 4, 5}.
    - LOC / LOC3 (local deficits against k(1 + a1) + P_w (+ W3)): −9 at m = 25, B = {1, 5, 6}.
    - So every waste term is needed somewhere.

## Theorem LAYER3 (every numerical semigroup) and the depth-four reduction W = Q3 + Q4 (lead, 2026-10-20; checks E326)

Setting: S is a numerical semigroup, m = m(S) ≥ 2, e = e(S).
- Layers: S_j = {r ∈ [0, m) : jm + r ∈ S}, s_j = |S_j| = |S ∩ [jm, (j+1)m)|. Then S_0 = {0} ⊂ S_1 ⊂ S_2 ⊂ ….
- New elements: N_j = S_j ∖ S_{j−1}.
- Generator layers: G_j = {r : jm + r is a minimal generator}, k_j = |G_j|, so e = 1 + Σ_{j≥1} k_j. Note G_1 = N_1.

**Theorem LAYER3 (PROVED on paper).** 3·|S ∩ [3m, 4m)| ≤ e·|S ∩ [0, 3m)|, i.e. 3·s_3 ≤ e·(s_0 + s_1 + s_2).
Equality holds for "free" S = ⟨m, m + B⟩ (all sums of ≤ 3 elements of B distinct and < m).

Proof.
1. **Decomposition.** Let r ∈ N_j, so n = jm + r ∈ S and n − m ∉ S. Either n is a minimal generator (r ∈ G_j), or
   n = g + s with g a minimal generator, g ≠ m, s ∈ S ∖ {0}.
   - s ≠ m, and s − m ∉ S; otherwise n − m ∈ S.
   - Write g = a′m + x with x ∈ G_{a′}, and s = am + u with a ≥ 1 and u ∈ N_a.
   - Then r = x + u with j = a + a′ (if x + u < m), or r = x + u − m with j = a + a′ + 1 (if x + u ≥ m).
2. **The new elements of layers 2 and 3.**
   - N_2 = G_2 ⊔ U2, with U2 ⊂ (G_1 + G_1)_{<m}. The union is disjoint because a pair sum is never a minimal generator.
     So |U2| =: u2 ≤ P_u, where P_u, P_w count the multisets {x, y} ⊂ G_1 with x + y < m, resp. ≥ m;
     P_u + P_w = k_1(k_1 + 1)/2.
   - N_3 ⊂ G_3 ∪ T_G ∪ T_U ∪ R, where:
     - T_G = (G_1 + G_2)_{<m}, so |T_G| ≤ k_1 k_2;
     - R = (G_1 + G_1)_{≥m} − m, so |R| ≤ P_w;
     - T_U = ((G_1 + U2)_{<m}) ∖ (S_2 ∪ T_G).
3. **The bound for T_U.** Each t ∈ T_U is x + y + z with x, y, z ∈ G_1.
   - Every pair sum is < m and lies in U2. If x + z ∈ S_1, then t ∈ G_1 + G_1 ⊂ S_2. A pair sum is never in G_2.
   - The incidence count and deficit count of Theorem Q3 apply verbatim: 3|T_U| ≤ k_1·u2 + 2P_u.
4. **Arithmetic.** Use 3s_3 = 3s_2 + 3|N_3|, s_1 = 1 + k_1 and s_2 = 1 + k_1 + k_2 + u2.
   - The P18 part:
     3(1 + k_1 + u2) + k_1 u2 + 2P_u + 3P_w ≤ (1 + k_1)(3 + 2k_1 + u2).
     Indeed, the difference is 2k_1(k_1+1) − 2u2 − 2P_u − 3P_w ≥ 2k_1(k_1+1) − 4(P_u + P_w) = 0.
   - The remaining terms on the left are 3k_2 + 3k_3 + 3k_1k_2 (from s_2, G_3 and T_G).
   - The remaining terms on the right are at least (1 + k_1)k_2 + (k_2 + k_3)(3 + 2k_1) ≥ 3k_2 + 3k_1k_2 + 3k_3. ∎

Remarks.
- The statement has the form of Eliahou's "condensed Macaulay" j·h_j ≤ h_1·Σ_{i<j} h_i for standard graded algebras
  (JEMS 2018, Thm 5.11). But the layers s_j are not such a Hilbert function: wrapped sums skip a layer.
- The analogue LAYER(j) for j ≥ 4 is FALSE in general. Example: P18, ⟨52, 80, 81⟩, LAYER(7) slack −3. LAYER(4) fails at
  ⟨35, 54, 55⟩. These are large-genus e = 3 cases. LAYER(j) has 0 failures for all j ≤ 9 at genus ≤ 36.
- For j ≥ depth q, LAYER(j) follows from Wilf.

**Identity (PROVED; every S of depth four, 3m < c ≤ 4m, h := c − 3m).**
- The layer facts: ℓ = s_0 + s_1 + s_2 + L3 with L3 = |S_3 ∩ [0, h)|; s_3 = m − d4, where d4 = #{w ∈ Ap(S, m) : w ≥ 4m}
  (these residues are all < h); and h = L3 + d4.
- Hence W = Q3 + Q4, where:
  - Q3 := e(s_0 + s_1 + s_2) − 3s_3 ≥ 0 (Theorem LAYER3);
  - Q4 := (e − 1)·L3 − 4·d4 = (e − 1)h − (e + 3)·d4.

**Corollary LAYER3-W (PROVED).** Every numerical semigroup with 3m < c ≤ 4m and (e + 3)·d4 ≤ (e − 1)·(c − 3m) satisfies
Wilf. In words: Wilf holds unless more than a fraction (e − 1)/(e + 3) of the residues below h have Kunz coordinate 4.

**Depth-four coverage.** Three proved results together: LAYER3-W, Wilf for c ≤ 3m + e (DEPTH4-EH, kernel-checked), and
Wilf for 3e ≥ m (Eliahou).
- They leave exactly 1 of 1,690,641 depth-four S of genus ≤ 30 uncovered: ⟨13, 16, 17, 19⟩.
- They leave 7 of 11,400,681 at genus ≤ 34, all with e ∈ {4, 5} and all generated below 2m:
  ⟨13,16,17,19⟩, ⟨13,18,19,22⟩, ⟨13,18,20,24⟩, ⟨15,17,21,22⟩, ⟨15,19,20,22⟩, ⟨16,19,22,23,24⟩, ⟨16,20,21,23,24⟩.
  (A census, not a proof.)
- Depth four with fixed e has m ≤ C(e + 3, 4), so it is a finite family for each e. P18 depth four for e ≤ 6 is already
  certified by complete enumeration (E319).
- Structural consequence: a depth-four counterexample must have h > e, e < m/3 and L3 < 4h/(e − 1). Almost every residue
  below h has Kunz coordinate 4.
- Literature (dated search 2026-10-20, web + LITERATURE.md): no statement of LAYER3 or LAYER3-W was found. The nearest
  are Eliahou's Macaulay-based q = 3 proof and his condensed Macaulay inequality. Novelty UNVERIFIED beyond that search.

### Conjectures DK = LASTWIN and HD1 (lead, 2026-10-20; checks E327)
- **LASTWIN (CONJ; 0 failures).** For every numerical semigroup of depth q = ⌈c/m⌉ ≥ 2, with h = c − (q−1)m:
  h ≤ e·|S ∩ [(q−1)m, c)|. Equivalently d_q ≤ (e − 1)·L_{q−1}, where d_q = #{residues of Kunz level q} (all < h) and
  L_{q−1} = |S ∩ [(q−1)m, c)|. This is Wilf restricted to the last, partial, window.
  - Data: tree to genus 30, every depth 2…21 (14.4M S): 0 failures, min slack 0.
  - Equality example: ⟨9, 37, …, 44⟩ (all generators in layer 4).
  - Depth two: PROVED (elementary). Gaps of the window are new generators or unwrapped pairs of generators below m + h.
  - At depth four the name is DK. Combined with the identity, W = Q3 − 3·d4 + DKslack, DKslack = (e − 1)L3 − d4.
- **COV (FALSE).** "Every level-four residue is a generator translate of a residue of S_3 ∩ [0, h)." It fails for 138,918
  of 642,239 depth-four S of genus ≤ 28. Example: m = 18, c = 56, d4 = 1. So DK is a counting statement, not a covering.
- **HD1 (CONJ; 0 failures; P18 depth four).** Let H_D be the set of r ∈ D with no parent in X = S_3 ∩ [0, h). This means
  r − b ∉ N3 for all b ≤ r, and r + m − b ∉ U2 ∩ [0, h) for all b > r.
  - Every representation r + m = x + y + z then has all three pair sums in U2 ∩ [h, m).
  - Claim: |H_D| ≤ k(1 + |B ∩ [0, h)|).
  - HD1 ⟹ DK. Proof: the other level-four residues inject into X × B through their parent incidence. The k(1 + a1)
    incidences from 0 and from B ∩ [0, h) never land in D.
  - Theorem A0 (PROVED earlier) settles B ∩ [0, h) = ∅ for Wilf. There, [h, 2h) must be covered by B and by wrapped pairs.
- **REFUTED (2026-10-20, same night; E328): LASTWIN, DK, HD1, HG1, SUMSET and SUMH are all FALSE.**
  - LASTWIN at large depth. S = ⟨55, 109, 159, 319⟩ (e = 4): c = 1381, q = 26, h = 6, |S ∩ [1375, 1381)| = 1, so
    e·1 = 4 < 6. Checked by brute-force membership DP (independent of the Apéry code).
  - DK at depth four, P18. S = ⟨302, 302 + B⟩ with B = {36, 37, 38, 41, 42, 43, 45, 51, 53, 63, 65, 71, 75, 97, 170, 171, 175,
    176, 178, 183, 185, 186}:
    - e = 23, c = 942, h = 36, |S ∩ [906, 942)| = 1 (only 3m), d4 = 35;
    - DK slack (e−1)·1 − 35 = −13;
    - B ⊂ [h, m), so HD1 and HG1 fail too (35 hard residues > k = 22). SUMH: |X + A*| = 23 < 36;
    - checks: brute force (lwfail.brute) and Dijkstra (dead.info) agree on c and e, and give W = 3014;
    - STAR = 827 still holds there. Theorem A0 (a = 0 ⟹ W ≥ 1) is consistent with it.
  - Lesson: the last window can be almost empty (D = [1, h), h > e). Then the layer-three Macaulay slack Q3 (here 3132)
    pays the whole depth-four deficit. A "last-window" argument alone cannot prove depth-four Wilf; Q3 must be used.

### Identity LAYER3-ALL and the all-depth corollary (lead, 2026-10-20; PROVED; checks E329)
- **Identity (PROVED; every S with c > 3m).** W = Q3 + (e − 1)·L − G − 3·D4, where:
  - Q3 = e·|S ∩ [0, 3m)| − 3·|S ∩ [3m, 4m)| ≥ 0 (Theorem LAYER3);
  - L = |S ∩ [3m, c)|, G = #gaps in [3m, c);
  - D4 = #{r : Kunz coordinate x_r ≥ 4} = m − s_3.
  - Proof: W = e(s_0 + s_1 + s_2 + L) − c, c = 3m + L + G, e(s_0 + s_1 + s_2) = 3s_3 + Q3, s_3 = m − D4.
- **Corollary LAYER3-W (all depths; PROVED).** If G + 3·D4 ≤ (e − 1)·L, then S satisfies Wilf. In words: Wilf holds
  unless the tail [3m, c) is gap-heavy. At depth four this is (e + 3)d4 ≤ (e − 1)h.
- **Census (genus ≤ 30, every depth ≥ 4, E329).** Every S with e ≥ 3 is covered by LAYER3-W, Eliahou's c ≤ 3m, or
  Eliahou's 3e ≥ m, except 7 semigroups.
  - All 7 have depth four and e = 4: ⟨13,15,16,19⟩, ⟨13,15,16,21⟩, ⟨13,15,18,19⟩, ⟨13,16,17,18⟩, ⟨13,16,17,19⟩,
    ⟨14,16,17,19⟩, ⟨14,16,19,20⟩.
  - Six of them have h ≤ e, so DEPTH4-EH covers them. ⟨13,16,17,19⟩ remains (W = 23).
  - The only other uncovered S are e = 2 (⟨7,10⟩, ⟨7,11⟩; Sylvester).
- So, structurally, a Wilf counterexample needs all of:
  - c > 3m and 3e < m;
  - a gap-heavy tail, G + 3·D4 > (e − 1)·|S ∩ [3m, c)|;
  - near-tightness of LAYER3: Q3 < G + 3·D4 − (e − 1)L.
  The last condition means the Macaulay-type layer-three bound is almost an equality, which happens only near "free"
  (B_3-like) configurations of the layer-one generators.
- **Prefix/tail form (identity; E330).** For c > 3m, W = P + T, where P = e·|S ∩ [0, 3m)| − 3m (prefix Wilf) and
  T = e·|S ∩ [3m, c)| − (c − 3m) (tail Wilf).
  - LAYER3 is the statement P ≥ −3·D4.
  - At P18 depth four: P = Q3 − 3d4 = 3δ3 − (e−3)δ2, where δ2 = C(e,2) − d2 and δ3 = C(e+1,3) − d3 − d4 (pair and
    triple redundancy), and T = (e−1)L3 − d4 (the DK slack). The free model has P = 0, so there Wilf ⟺ T ≥ 0.
  - Census (genus ≤ 30, e ≥ 3, every depth ≥ 4):
    - T < 0 never occurs. It does occur at larger genus: the DK counterexample has T = −13 and P = 3027.
    - P < 0 occurs: 34 S at depth four, more at greater depth. In every case T ≥ 1.67·(−P). Minimum ratios: 2.33 at
      depth 4 (⟨9,19,21,22⟩), 2.0 at depth 5, 1.67 at depth 6 (⟨7,23,24,43⟩).
  - So, empirically, the prefix and the tail are never deficient together.
  - Heuristic: at P18 depth four, P < 0 needs level-four residues beyond the triple count. Those are unwrapped 4-sums,
    whose four parents lie in X = S_3 ∩ [0, h); this pays T. A deficient tail (T < 0) needs carried triples outnumbering
    k·|S_2 ∩ [0, h)| plus waste, and then pair/triple collisions make P large.

## P18 depth four: STAR and J are FALSE; the carry identity CARRY-ID (PROVED) and its self-payments (lead, 2026-10-20; checks E331–E332)

Setting: P18 depth four as in "P18 depth four: layer form", with S = ⟨m, m + B⟩, |B| = k, h = c − 3m, A = {0} ∪ B.

**Refutations (both verified by two independent codes, E331).**
- **STAR is FALSE.** m = 47, B = {5, 6, 7, 8, 9, 12, 16, 17} (e = 9, h = 5, W = 205):
  - P_w = 0, J_≥ = 6, k·L3 = 8, d4 = 4, so STAR = 6 + 8 − 16 = −2.
  - The four level-four residues 1..4 are the carried triples 3·16, 2·16 + 17, 16 + 2·17, 3·17. Repeated summands
    leave them only 6 parent incidences.
  - W is paid by G_T, i.e. collisions of the AP {5, …, 9}.
- **Conjecture J is FALSE** (PROOFS "Depth four: the split W = J + σ"). m = 21, B = {2, 12, 14, 17, 18}, i.e. ⟨21, 23, 33, 35, 38, 39⟩
  (e = 6, h = 2, W = 43):
  - J = E2 + (e−1)y − 4H4 − q − 3q_Q − p = 4 + 5 − 0 − 1 − 0 − 9 = −1.
  - J charges the nine carried pairs, all with residue ≥ h, to E2 alone.
  - h ≤ e here, so Wilf is covered by DEPTH4-EH. "J for h > e" has no counterexample known, but the mechanism generalises.

**Notation.**
- T = (3A ∩ [0, m)) ∖ S_2 (new unwrapped triples).
- CP = N3 ∖ T (carried pairs: level 3, order 2), with p = |CP| and p_lo = |CP ∩ [0, h)|. So d3 = |T| + p.
- C = level-four residues not in 4A (carried triples; r + m ∈ 3B, r < h), q = |C|. H4 = level-four residues in 4A.
  So d4 = H4 + q. Also y = L3.
- δ2 = C(k+1, 2) − d2 − p ≥ 0 (pair redundancy: U2 ∪ CP are residues of distinct pair multisets).
- **Incidence pool** I = (U2 ∪ (m + CP_lo)) × B, |I| = k(d2 + p_lo).
- **Repeat pool** Δ = ordered pairs (x, z) ∈ B², x ≠ z, together with two copies of each x ∈ B; |Δ| = k(k + 1).
- For each t ∈ T (value t) and each r ∈ C (value m + r), fix one representation as a sum of three elements of B, with
  distinct summands when one exists.
  - It uses its pair-incidences (pair sum, third summand): 3, 2 (for 2x + z: (2x, z), (x + z, x)) or 1 (for 3x: (2x, x)).
  - It uses its repeat entries: (x, z) for 2x + z, both copies of x for 3x.
- sl_A := |I| + |Δ| − 3(|T| + q), and sl_A = incU + incC + defU (unused U2-incidences, unused CP-incidences, unused repeat
  entries).
- sl_B := k(y − p_lo) − 4·H4.

**Lemma (pools; PROVED).** Every used incidence lies in I. Distinct (value, incidence) choices give distinct incidences,
and distinct repeat entries. Hence sl_A ≥ 0. Also sl_B ≥ 0.
- Proof.
  1. T case. For t ∈ T, pair sums are < m and in U2: a pair sum in A puts t in 2A ⊂ S_2.
  2. C case, pair sum s < m. Then s ∈ U2. If s ∈ A, then (m+x) + (m+y) = m + (m + s) ∈ m + S, so 3m + r ∈ S, contradicting
     r ∉ S_3.
  3. C case, pair sum s ≥ m. Let u = s − m = r − z < h.
     - u ∉ S_2: otherwise 3m + u = m + (2m + u) ∈ m + S, so again 3m + r ∈ S.
     - u ∉ T: otherwise 3m + u is a sum of three generators, so r ∈ 4A, contradicting r ∈ C.
     So u ∈ CP_lo.
  4. An incidence (s, b) determines its value s + b. T-values are < m and C-values are ≥ m. Inside one representation the
     listed incidences are distinct. Repeat entries determine their value (2x + z, resp. 3x).
  5. sl_B ≥ 0 is the condensed-Macaulay token count restricted to uncarried sources in X. An order-four element 4m + r
     (r < h) uses the tokens (w − j(m + b), b), whose sources have residue < h and level = order ≤ 3. The only carried
     elements of S_3 are the carried pairs. ∎

**Identity CARRY-ID (PROVED; exact).** For every P18 S of depth four:

    W = 2·δ2 − p − q + sl_A + sl_B.

Hence **Wilf ⟺ p + q ≤ 2δ2 + sl_A + sl_B**. The total carry T_c = p + q must be paid, one unit each, by:
- twice the pair redundancy;
- unused triple incidences and repeat entries;
- unused degree-four tokens from uncarried sources below h.

Proof: substitute d3 = |T| + p, d4 = H4 + q, 3|T| = |I| + |Δ| − 3q − sl_A and 4H4 = k(y − p_lo) − sl_B into
W = 2k² + 2k + (k − 2)d2 + k·L3 − 3d3 − 4d4. ∎

**Self-payments (PROVED).**
- (i) **Carried pairs.** Let u ∈ CP have a pair representation x + y = m + u (x ≤ y) with u + y ≥ h. Then the repeat entry
  (y, x) (both copies of x if x = y) is unused: its value 2y + x = m + u + y ≥ m + h is neither a T-value nor a C-value.
  Distinct u give distinct entries. If p_res counts the carried pairs with u + y < h for every representation, then
  p_res > 0 forces m ≤ x + y ≤ 2y < 2h. **So p_res = 0 whenever 2h ≤ m.**
- (ii) **Carried triples.** Let r ∈ C have a representation x + y + z = m + r with a pair sum s = x + y < h.
  - Then s ∈ U2 ∩ [0, h) is an uncarried source in X.
  - Its token (s, z) has target (2m + s) + 2(m + z) = 5m + r + z, of level ≥ 5, so it is unused (counted in sl_B).
  - s + z = m + r, so distinct r give distinct tokens.
  - q_res counts the carried triples all of whose representations have all three pair sums ≥ h.
- Exact residual form: W = 2δ2 + incU + incC + (defU − n_i) + (sl_B − n_ii) − p_res − q_res, where n_i + p_res = p,
  n_ii + q_res = q, and both brackets are ≥ 0.
- **Corollary (PROVED).** P18 depth four with 2h ≤ m and q_res = 0 satisfies Wilf, indeed W ≥ 2δ2 + sl_A.

**Conjectures (0 failures; E332).**
- **L1:** q_res ≤ incU + incC (unused incidences pay the carried triples with only large pair sums). Minimum slack is 0 at
  m = 17, B = {2, 9, 11}; there the four residual triples 10, 12, 14, 16 are paid exactly by incidences landing on the
  old residue 13 and on the carried-pair residues 3, 5.
- **L2:** q_res + p_res ≤ incU + incC + 2δ2. **L2 ⟹ P18 depth-four Wilf; for 2h ≤ m, L1 ⟹ Wilf.**
- **K7:** p + q ≤ defU + sl_B (stronger than Wilf, since it drops 2δ2 + incU + incC). Minimum slack is 6, 13, 21 for
  e = 4, 5, 6.
- FALSE (E332):
  - L6, pure q_res ≤ incU: m = 13, B = {5, 7, 11}.
  - K5, p ≤ defU: m = 17, B = {2, 9, 11}.
  - K6 (defU + incC ≥ p + q), L3 (incU ≥ q_res), L5 (incC ≥ grown q_res).
  - "Wrap/high tokens pay all carries" (C3) fails at the DK counterexample: 22 − 35 − 24 < 0.

### CARRY-ID consequences: a short proof of Theorem A0, the window bound R2, and Conjectures LM, TB4-LOC (lead, 2026-10-20; checks E333)
Setting and notation as in "CARRY-ID". Write y0 = |3A ∩ [0, h)| = y − p_lo (uncarried X) and N4 = H4.

**Lemma 2ND (PROVED).** A carried pair u ≥ h has both repeat entries free. If its representation is x + y = m + u with
x < y, the entries (x, y) and (y, x) have values 2x + y and 2y + x, both ≥ m + h. If x = y, both copies of x are free.
- So defU ≥ n_i + p_hi.
- If 2h ≤ m, then n_i = p, so defU ≥ p + p_hi.

**Theorem A0 again (PROVED; new short proof).** If B ⊂ [h, m), then W ≥ 1.
- Facts when B ⊂ [h, m):
  - pair sums are ≥ 2h and triple sums are ≥ 3h, so 3A ∩ [0, h) = {0}, y0 = 1 and H4 = 0;
  - hence sl_B = k (the tokens (0, b));
  - q = h − 1 − p_lo;
  - every carried pair has max summand ≥ h, so self-payment (i) applies: n_i = p.
- **2h ≤ m.**
  - [h, 2h) ⊂ S_3, and 3A ∩ [h, 2h) = B ∩ [h, 2h), so h ≤ |B ∩ [h, 2h)| + |CP ∩ [h, 2h)| ≤ k + p_hi.
  - Then W ≥ sl_B + defU − p − q ≥ k + (p + p_hi) − p − (k − 1 + p_hi) = 1.
- **2h > m.** Then 3B ≥ 3h ≥ m + h, so q = 0 and W ≥ k + p_hi ≥ 1. ∎

**Proposition R2 (PROVED; regime 2h ≤ m).**

    W ≥ e·y0 − 3·N4 − |3A ∩ [h, 2h)| + 2δ2 + incU + incC + p_lo.

- Proof: in CARRY-ID use
  - defU ≥ p + p_hi (Lemma 2ND);
  - q = h − y0 − p_lo − N4;
  - the window covering h ≤ |3A ∩ [h, 2h)| + |CP ∩ [h, 2h)| (residues of the window covered by a wrapped pair that are
    not carried pairs lie in S_2 ⊂ 3A);
  - sl_B = k·y0 − 4N4. ∎
- Consequences:
  - |3A ∩ [h, 2h)| ≤ h and E1 ≤ 2δ2, so **TB4 ⟹ Wilf for 2h ≤ m directly** (RED-A is not needed).
  - In the core regime B ⊂ [h/2, h) with 2h ≤ m, the window lies in 3A, so R2 = e² + 2δ2 + … − h. This is ≥ 0 by
    CORE4's half-window bound h ≤ e² − e + 2.
- Witness scheme toward R2 ≥ 0. Every v ∈ 3A ∩ [h, 2h) has a witness (v − a, a) ∈ (3A ∩ [0, h)) × A, except the core
  triples (every representation is x + y + z with x + y ≥ h). Every element of N4 has ≥ 3 witnesses except repeated
  4-sums. The witnesses (u, 0) are never used. Open: pay the core triples and repeated 4-sums by E1 and unused witnesses.

**Conjecture LM (local matching; 0 failures, E333).** Every carry can be assigned injectively to an unused slack item
attached to one of its own representations:
- **Carried pair u = {x, y}:** its repeat entries; its incidences (m + u, b); the tokens (a, b) with a ∈ {0, x, y} ∩ X_unc and
  b ∈ {x, y}.
- **Carried triple {x, y, z}:** its pair tokens; the incidences in its pair rows; the entries among its summands; the tokens
  (a, b) with a ∈ {0, x, y, z} ∩ X_unc and b in the triple.
- Redundancy units (2δ2) are never needed (ablation, e = 4, 5 and random e = 10). So LM implies the stronger
  K1: p + q ≤ sl_A + sl_B.
- The degree condition (min carry degree ≥ max item degree) FAILS. So does uniform discharging (load 1.74). The
  per-largest-summand column split also FAILS (m = 17, B = {2, 9, 11}).

**Conjecture TB4-LOC (0 failures, E333).** Let A = {0} ∪ B ⊂ [0, m), 1 ≤ h ≤ m, S_3 = 3A_{<m} ∪ (2A_{≥m} − m), and assume
- (G) h − 1 ∉ S_3;
- (W) [h, min(2h, m)) ⊂ S_3;
- (L) [0, h) ⊂ 4A ∪ ((3A ∩ [m, m + h)) − m).
Then h + 3N4 ≤ e·y0 + E1 (TB4).
- Only the first window is required, not the covering of [2h, m). With the half window [h, 3h′) in place of (W),
  TB4 FAILS (E314).
- With RED-A and Theorem A0, TB4-LOC implies P18 depth-four Wilf.

### Exact six-component split of the LAYER3 surplus, and a necessity audit of who pays the tail (lead, 2026-10-20; checks E335)
Setting: every numerical semigroup, notation of "Theorem LAYER3". k1, k2, k3 = generator counts in layers 1, 2, 3;
k4p = generator count in layers ≥ 4; P_u, P_w = multisets {x, y} ⊂ G_1 with x + y < m, resp. ≥ m;
U2 = N_2 ∖ G_2, u2 = |U2|; T_G = (G_1 + G_2)_{<m}; T_U = ((G_1 + U2)_{<m}) ∖ (S_2 ∪ T_G); R = (G_1 + G_1)_{≥m} − m;
s012 = s_0 + s_1 + s_2 = 3 + 2k1 + k2 + u2.

**Proposition Q3-SPLIT (PROVED).** Put A_G = N_3 ∩ T_G and A_R = N_3 ∖ (G_3 ∪ A_G ∪ T_U). Then
N_3 = G_3 ⊔ A_G ⊔ T_U ⊔ A_R with A_R ⊂ R, and

    Q3 = σ_T + 3(P_w − |A_R|) + 2(P_u − u2) + P_w + Γ_23 + Γ_4,

where every term is ≥ 0:
- σ_T = k1·u2 + 2P_u − 3|T_U| (the incidence/deficit slack of LAYER3 step 3);
- Γ_4 = k4p·s012;
- Γ_23 = (1 + k1)k2 + (k2 + k3)·s012 − 3k2 − 3k3 − 3|A_G| ≥ k2 + 2k1k3, since |A_G| ≤ k1k2.
- Proof:
  - T_U ⊂ N_3, and N_3 ⊂ G_3 ∪ T_G ∪ T_U ∪ R (LAYER3, steps 1–2). So the four sets are disjoint by construction, and
    A_R ⊂ R gives |A_R| ≤ P_w.
  - Expand e = 1 + k1 + k2 + k3 + k4p in Q3 = e·s012 − 3(s_2 + |N_3|), with s_2 = 1 + k1 + k2 + u2.
  - The P18 part (1 + k1)(3 + 2k1 + u2) − 3(1 + k1 + u2) − 3|T_U| − 3|A_R| equals
    σ_T + 3(P_w − |A_R|) + 2(P_u − u2) + P_w, using k1(k1 + 1) = 2(P_u + P_w). ∎
- Asserted (split and nonnegativity) on every S of genus ≤ 34 with c > 3m (E335).
- For P18 at depth four this reads W = Q4 + σ_T + [3(P_w − p) + 2(P_u − u2) + P_w], with Q4 = k·L3 − 4d4.

**Necessity audit (OBSERVED, E335).** For c > 3m, W = Q3 + Q_tail with Q_tail = (e−1)L − G − 3D4 (Identity of E329).
Question: which components of Q3 are ever needed to keep W ≥ 0? Ablation over all 63 subsets of the six components:
- Depth four, every S of genus ≤ 32 (4,408,418 S):
  - the three pair-redundancy terms 3(P_w − |A_R|) + 2(P_u − u2) + P_w can be dropped together: 0 failures;
  - σ_T, Γ_23 and Γ_4 are each individually essential. Dropping one fails, e.g. ⟨13,16,17,18⟩ (σ_T, −3),
    ⟨12,18,31,…,35⟩ (Γ_23, −10), ⟨9,37,…,44⟩ (Γ_4, −24).
- Depths 5–60, e ≥ 3, genus ≤ 34 (2,190,813 S): pair redundancy and σ_T are both dispensable (0 failures). Γ_23
  (19 failures) and Γ_4 (827 failures) are essential. With e = 2, all of Q3 is needed (W = 0, e.g. ⟨4,7⟩).
- P18 depth four (k2 = k3 = k4p = 0, so only σ_T can pay), exhaustive e = 4, 5, 6 (m ≤ 40, 30, 24) and random e = 10:
  dropping σ_T fails (46 and 13 times at e = 5, 6), while dropping the pair terms never does.
  - Annealing (e ≤ 15, m ≤ 220): the needed σ_T ≥ 3.42·(−Q4) whenever Q4 < 0. In DK, σ_T = 2874 vs −Q4 = 118; in
    STAR, 179 vs 8.
  - On P18 fakes (B arbitrary, every residue below h of level ≤ 4, h − 1 of level 4), Q4 + σ_T ≥ 0 FAILS without
    covering above h (m = 40, B = {13,15,16}, h = 9: −2). It held (0 failures) when only the half window
    [h, h + ⌈h/2⌉) is at level ≤ 3.
  - It does not hold for general S: 801 failures at genus ≤ 22, e.g. ⟨6,25,…,29⟩ where Γ_4 pays.
- Reading: the tail deficit is paid by
  - (a) the unwrapped-triple incidence slack σ_T, for P18 at depth four;
  - (b) the generators sitting in layers ≥ 2 (Γ_23, Γ_4), otherwise.
  Wrapped/unwrapped pair redundancy is never needed for e ≥ 3 on these data. These are diagnostics for where a proof
  mechanism must live, not proof targets (FAILED.md, gate rule 4).
- P18 depth four, mechanism status of Q4 + σ_T ≥ 0 (equivalently 4d4 + 3|T| ≤ k(L3 + u2) + 2P_u):
  - every level-4 residue already owns disjoint units equal to its value: 4 tokens for a 4-sum, 3 pair-row incidences
    for a carried triple;
  - carried triples with a pair sum < h get a 4th unit free, because rows below h appear in both k·L3 and k·u2;
  - the residual 4th units come jointly from four classes: overflow tokens, overshoot incidences, extra
    representations of carried triples, and incidences landing on old residues. In the Sidon-type scaling family the
    extra representations pay. So no single-class lemma can work (cf. Z1, Z12, O1, O3, CT in FAILED.md).
  - No proof yet.

**Token-window observations, regime 2h ≤ m (OBSERVED; NOT proof targets).**
- PROVED: W ≥ sl_B − q + p_hi + 2δ2 + incU + incC, and sl_B ≥ OVF := #{(t, b) ∈ (3A ∩ [0, h)) × B : t + b ≥ h}.
  Also h = |3A ∩ [h, 2h)| + |CP ∩ [h, 2h)| exactly.
- Z1: q ≤ OVF + p_hi. Z12: |3A ∩ [h, 2h)| ≤ |3A ∩ [0, h)| + OVF. Z12 ⟹ Z1 ⟹ Wilf for 2h ≤ m.
  - Both have 0 failures (exh e ≤ 6, random e ≤ 13, annealing; Z12 also on 700k half-window fakes).
  - Z12 FAILS with no window covering (m = 47, B = {10,12,13}, h = 20).
- Scaling estimate (not a construction): take a B3-Sidon block D ⊂ (h/2, 2h/3) of size d, and cover the half window by
  carried pairs of ≈ √h large generators. This should break Z12 at d ≳ 26 (e ≈ 140), and Z1 later. There, overshoot
  incidences and extra representations pay, i.e. terms that Z1 and Z12 discard. Hence they are recorded as
  observations only.

## Depth-q window bookkeeping for P18 cores; the depth-free content of the depth-four theorem (lead, 2026-10-20; checks E336)
Setting (window model, as in the external depth-four proof):
- m > ρ ≥ 0, N = m − ρ, offsets O ⊂ [1, N) with |O| = K (strip-free), q ≥ 2, and
  T = ⟨m, m + b : b ∈ O⟩ ∪ [qm − ρ, ∞).
- Position u ∈ [0, m) carries the element km + u − ρ. λ(u) is the least level of an element of ⟨m, m + O⟩ at u.
  λ_Y(u) is the least t with u − ρ ∈ t·O′ (O′ = O ∪ {0}, sums in ℕ) and u ≥ ρ; λ_Y(u) = ∞ if there is none.
- h_t = #{u : λ_Y(u) = t}, so h_0 = 1 and h_1 = K. d_t = (K + t − 1)h_{t−1} − t·h_t.
- ℓ = Σ_u (q − λ(u))_+, d = #{u : λ(u) ≤ q}, W₀ = (K + 1)ℓ − q·d + ρ, p = m − d. Then W(T) = W₀ + p(ℓ − q)
  (Eliahou; this is the identity W = W₀ + p_q(|L| − q)).

**Identity (PROVED).** W₀ = ρ + Σ_{t=2}^{q} (q + 1 − t)·d_t + Σ_{u : λ(u) < λ_Y(u), λ(u) ≤ q} c(u), where
- c(u) = (K + 1)(λ_Y(u) − λ(u)) if λ_Y(u) ≤ q;
- c(u) = (K + 1)(q − λ(u)) − q if λ_Y(u) > q.

Proof.
- If every λ = λ_Y, then ℓ = Σ_{t<q}(q − t)h_t and d = Σ_{t≤q} h_t. Comparing coefficients of h_s:
  - for 2 ≤ s ≤ q − 1, (q − s)(K + s) − (q + 1 − s)s = (K + 1)(q − s) − q;
  - for s = q, −q;
  - the h_0 and h_1 terms agree, using h_0 = 1 and h_1 = K.
  This gives W₀ = ρ + Σ (q + 1 − t)d_t.
- A carried position (λ < λ_Y) changes ℓ by (min(λ_Y, q) − λ) and d by [λ_Y > q]. ∎

Remarks.
- d_t ≥ 0 is truncated Macaulay for the unwrapped multicomplex: an order ideal of monomials, Eliahou JEMS 2018
  Thm 5.11 / condensed Macaulay.
- The only negative costs are carried positions with λ_Y > q and (K + 1)(q − λ) < q. When K ≥ q − 1 these are
  exactly the **top-level carried positions** (λ = q, λ_Y > q), each costing −q.
- At q = 4 this is the external ID2 before regrouping: W₀ = ρ + 3d₂ + 2d₃ + d₄ + (K − 3)|Ẑ| + 4|Ẑ ∩ Y₄| − 4|Q|.
  The external proof then regroups with Lemma 6_ρ, Σ_q w(q) + A = (K + 2)|Ẑ|, so that only Q₃ (carried triples
  whose three parent pairs are all wrapped) stays negative. Q₃ is then paid by the anchor shell and the two
  injections.
- At depth q the same three steps would be needed:
  - (i) a parent-incidence identity for the top-level carried positions. These are (q − 1)-sums wrapped once,
    (q − 2)-sums wrapped twice, and so on, so it must handle multi-wraps;
  - (ii) the class left negative after regrouping;
  - (iii) an anchor shell for that class.
  None of this exists yet. The depth-four regrouping uses that a once-wrapped 3-sum has exactly three parent pairs.
- Check: E336 (`src/scratch/p32/carryq.py`). 0 mismatches on 3,000 random models, q = 4–7, random ρ, K ≤ 9. Every
  d_t ≥ 0. With K ≥ q − 1 the only negative class is λ = q.

**Corollary (depth-free layer-4 inequality; from the external anchor theorem, kernel-checked: see LITERATURE).**
- Let S = ⟨m, m + B⟩ with B ⊂ [1, m), some 2b ≥ m, and N_k = |S ∩ [km, (k + 1)m)|, at any depth.
- Then e·(N_0 + N_1 + N_2 + N_3) − 5N_4 + m + h_4 ≥ coll + 2d₃'' + d₄ ≥ 0, where e = |B| + 1 and
  h_4 = |4B′ ∩ [0, m)| − |3B′ ∩ [0, m)|.
- Equivalently Q_4 ≥ −D_5 − h_4, where Q_j := e·Σ_{k<j}N_k − j·N_j and D_5 = m − N_4.
- Proof. Apply `st_A29A` / `an_anchor_bound` to the model (m, 0, B). Every b < m is a window offset at ρ = 0, and
  that model is the truncation S ∪ [4m, ∞). Its ℓ = Σ_{k<4} N_k and d = N_4. All generators are below 2m, so each
  element of S ∩ [4m, 5m) is a sum of two elements below 4m.
- Compare LAYER(4) (Q_4 ≥ 0), which is FALSE (⟨35,54,55⟩, slack −1), and LAYER3 (Q_3 ≥ 0, every S, PROVED).
- With W = Q_j + (e − 1)L_j − G_j − j·D_{j+1} for every j with jm ≤ c, where L_j, G_j count elements and gaps in
  [jm, c), the corollary gives, for P18 with a high offset at depth ≥ 5:
  W ≥ (e − 1)L_4 − G_4 − 5D_5 − h_4.
  This is a last-window type bound. By FAILED.md pattern A it is not a proof target.
- Check: E336 (`anchor_layer4.py`). 0 failures on 17,864 random sets with a high offset, 12,722 of them of depth ≥ 5.
  The minimum of the left side was 5; LAYER(4) failed 49 times on the same sample.

### Identity ID-q: wraps paid by crossing incidences (every depth, every P18 model) — PROVED 2026-10-20 (checks E337)
Setting:
- m > ρ ≥ 0, B ⊂ [1, m) with |B| = K (strip offsets allowed), q ≥ 1, and T = ⟨m, m + b : b ∈ B⟩ ∪ [qm − ρ, ∞).
- Shifted position of v: u = (v + ρ) mod m; level ⌊(v + ρ)/m⌋. An element km + u − ρ sits at position u, level k.
- **Canonical representation** α_u of position u: the multiset of offsets (an element Σ α_i(m + b_i)) at position u
  minimizing (level, degree, code), with code = Σ α_i·B̂^i for a fixed base B̂ > q + 1. Write λ_u (level),
  t_u = |α_u| (degree), j_u = λ_u − t_u (wraps).
- **Divisor closure.** If α_i > 0 for y's representation α = α_y, then α − e_i = α_x for the position x of the parent
  element, and λ_y = λ_x + 1 + κ, where κ = [x + b_i ≥ m] (a "crossing").
  - Proof: let γ beat α − e_i at x. Elements at a common position differ by multiples of m, and adding m + b_i shifts
    every element at x to y by the same level step. So γ + e_i beats α at y. ∎
  - Consequently κ = [b_i > y]. The minimal element at a position never uses the generator m.
- **Incidences.** Each x with λ_x ≤ q has out-incidences (x, i) of weight α_x(i) + 1, total K + t_x. (x, i) is
  **used** if the child y = x + b_i mod m has λ_y ≤ q and α_y = α_x + e_i. Put
  - u(x) = unused weight of x;
  - c_y = Σ_{i : b_i > y} α_y(i), the crossing in-weight of y.
  By divisor closure each y with λ_y ≤ q receives used in-weight exactly t_y.

**Identity ID-q.** With ℓ = Σ_x (q − λ_x)_+, d = #{x : λ_x ≤ q} and W₀ = (K + 1)ℓ − q·d + ρ (so W(T) = W₀ + p(ℓ − q),
p = m − d):

  W₀ = ρ + Σ_{x : λ_x ≤ q} (q − λ_x)·u(x) + Σ_{y : λ_y ≤ q} (c_y − j_y).

Proof.
- W₀ − ρ = Σ_{λ_x ≤ q} f(x) with f(x) = (K + 1)(q − λ_x) − q.
- Algebra: f(x) = (q − λ_x)(K + t_x) − (q + 1 − λ_x)t_x − j_x, since λ = t + j.
- Split K + t_x into used and unused weight, and write Σ_y (q + 1 − λ_y)t_y as a sum over used incidences.
- Each used incidence x → y contributes (q − λ_x) − (q + 1 − λ_y) = κ ∈ {0, 1}. Summing κ over the in-incidences of y
  gives c_y. ∎

Remarks.
- Every term is ≥ 0 except the **deficit** DEF = Σ_y max(0, j_y − c_y), coming from positions with fewer crossing
  parents than wraps. Write EXC = Σ_y max(0, c_y − j_y). Unwrapped positions have j = c = 0. A once-wrapped pair
  (strip-free) has c = 2, j = 1.
- At q = 4, strip-free, this is exactly the external ID2:
  - DEF = |Q₃| (j = 1, c = 0);
  - EXC = |Ẑ| + |Q₁| + 2|Q₀| (+ strip terms);
  - the weight-3 pool is 6(P_u − h₂) + 6(P_w − |Ẑ|); the weight-2 pool is 2d₃''; the weight-1 pool is
    A + d₄ + 4|Ẑ ∩ Y₄|.
- It refines the power-token identity W = U − e·T_c. There each wrap costs e; here each wrap costs 1 and is refunded by
  every crossing parent incidence.
- Check (E337, `src/scratch/p32/idq.py`): 0 mismatches on 3,000 strip-free and 3,000 general models, q = 3–7.
  - Strip-free: DEF comes from (j, c) = (1, 0), plus (2, 0) and (2, 1) from q = 6 on.
  - With strips: (2, ·) from q = 5 and (3, ·) at q = 7.

### Conjecture ANCHOR-q (every depth; UNDER GATE, 2026-10-20; checks E337)
For every P18 model as above:

  DEF ≤ ρ + EXC + U_top + p,   with U_top = Σ_{λ_x = q−1} u(x) (the weight-1 pool) and p = #{x : λ_x > q}.

- With ID-q, ANCHOR-q gives W₀ + p ≥ Σ_{λ_x ≤ q−2} (q − λ_x)u(x) ≥ 0, i.e. CORE₁ (W₀ + p ≥ 0). CORE₁ implies Wilf
  for the model (W = W₀ + p(ℓ − q), ℓ ≥ q + 1); it is STRONGER than Wilf. That would give Wilf for every pure P18
  semigroup (p = 0, W = W₀), i.e. all of DKM Problem 1.8, and CORE₁ for every generalized core at every depth.
- **Necessity audit.** ANCHOR-q discards only the pool of weight ≥ 2 (levels ≤ q − 2).
  - At q = 4 the external anchor theorem gives DEF ≤ ρ + EXC + A + 4|Ẑ ∩ Y₄| + h₄ + p. That is ANCHOR-4 with h₄ in
    place of the weight-1 pool of M₃; the latter is ≥ d₄ ≥ h₄ under the external residual hypotheses.
  - On perfect-Sidon models (every incidence below level q − 1 used), the discarded pool is 0, and there
    ANCHOR-q ⟺ CORE₁.
  - CORRECTION (same day). CORE₁ (W₀ + p ≥ 0) is STRONGER than Wilf, not implied by it: W = W₀ + p(ℓ − q) with
    ℓ − q ≥ 1. So Sidon-type models are the adversarial family. Examples: the Eliahou–Fromentin B₃ family (q = 4,
    W₀ = −C(n,3), covered by the external theorem) and its q = 5 analogue (offsets in [m/3, m/2), dense 4-fold sums).
  - Back-of-envelope (ρ = 0, q = 5, offsets in [m/3, m/2); level 3 is empty):
    W₀ + p = (K+1)(5 + 4K + 3h₂ + T₃) − 6(1 + K + h₂ + T₃ + T₄) + m, where h₂ = |2O|, T₃ / T₄ count the new
    3- / 4-sum positions. A B₄-type set needs 2m/3 ≳ T₄/δ, with δ the 4-sum density in its range. CORE₁ then fails
    for δ above about 0.75 (K = 3), 0.83 (K = 5), 0.84 (K = 10); it cannot fail for K ≥ 20 (δ > 1 needed).
    Whether such dense configurations exist is the decisive gate question (E338).
- **Equality cases seen.**
  - m = 16, ρ = 5, B = {1,2,11,14}, q = 6: the 5 deficit positions are exactly [m − ρ, m), so DEF = ρ.
  - m = 26, ρ = 0, B = {2,3,10,17}, q = 6: DEF = EXC = 2.
- Status (E337): 0 failures in every test so far.
  - Exhaustive, true depth (λ(m−1) ≥ q, so c(T) = qm − ρ), K ≤ 5:
    - q = 5: m ≤ 30 strip-free, 234,400 models; m ≤ 26 with strips, 699,195 models;
    - q = 6, m ≤ 30: 101,801 models;
    - q = 7, m ≤ 30: 55,994 models.
    The minimum slack is 1–2. The minimum slack/DEF (DEF ≥ 4) is 0.29 (q = 7, m = 26, ρ = 2, B = {3,12,15}, DEF = 14,
    slack 4).
  - Random large models (m ≤ 200, K ≤ 30, offsets from random intervals): 16,585 true-depth models at q = 5–7, with
    and without strips. Minimum slack/DEF is 1.07.
  - The DK model (m = 302, ρ = 266): DEF = 255, slack 2,594. The STAR model (m = 47, ρ = 42): DEF = 38, slack 137.
  - The ID-q identity was asserted on all of these: 0 mismatches.
- The tested range is small (K ≤ 5 exhaustive). Annealing struggles under the true-depth constraint. Next gate step: a
  proof attempt, generalizing the external shell + PAYMENT. A deficit at depth q can sit at levels below q (for
  example, once-wrapped triples at level 4 with all sub-pairs wrapped, at q = 5), so the shell must handle every
  level.

### ID-q for every numerical semigroup; Conjectures ANCHOR and CORE₁ (lead, 2026-10-20; checks E338)
**ID-q holds for every numerical semigroup S** (PROVED, same proof). Let S have multiplicity m and conductor c > m.
Put q = ⌈c/m⌉ and ρ = qm − c. Let g_1, …, g_K be the left primitives other than m, with offsets b_i = g_i − m of
any size.
- Adding g_i to the element at position x raises the level by 1 + κ with κ = ⌊(x + b_i)/m⌋ ≥ 0, possibly several
  crossings at once.
- With c_y = Σ_i κ_i(y)·β_y(i) (the crossing multiplicity of y's canonical parent incidences), the telescoping proof
  gives verbatim:
  E(S) = W₀(S) = ρ + Σ_x (q − λ_x)·u(x) + Σ_y (c_y − j_y).
- Here p = #{x : λ_x > q} = r(S) is the number of right primitives. Positions beyond level q are exactly the
  elements of [c, c + m) that are not sums of left primitives.
- Check: asserted (with p = r) on all 14,396,307 S of genus ≤ 30 and on every S below. 0 mismatches.

**Conjecture CORE₁ (every S with c > m):** E(S) + r(S) ≥ 0. Equivalently W(S) ≥ r(S)·(|L| − q − 1).
- It implies Wilf, since W = E + r(|L| − q) and |L| ≥ q + 1 unless S ∩ [0, c) = {0, m, …, (q−1)m}. It is strictly
  stronger.
- Equality: e = 2 (E = W = 0, r = 0).
- Literature (2026-10-20): no statement of E + r ≥ 0 or E ≥ −r found. Checked by web search, Bacher 2604.25051
  (whose Conj 2.6 "r < ℓ ⇒ E ≥ 0" is different) and Delgado 1608.01353.

**Conjecture ANCHOR (every S with c > m):** DEF ≤ ρ + EXC + U_top + r, with DEF, EXC, U_top as in ID-q (crossing
multiplicities κ). By ID-q, ANCHOR gives E + r ≥ Σ_{λ_x ≤ q−2} (q − λ_x)u(x) ≥ 0, i.e. CORE₁.

**Gate status.**
- (1) Necessity. CORE₁ discards only r(|L| − q − 1). ANCHOR also discards the pool of weight ≥ 2.
- (2) Falsification, 0 failures in all of the following:
  - every S of genus ≤ 30 (14,396,307 S, depths 2–30);
  - e = 3 exhaustive: m ≤ 60 with generators < 5m (481,764 S); m ≤ 36 with generators < 12m (800,118 S; depths
    to 62);
  - e = 4 random, m ≤ 120 (277,368 S); general random S (18,808);
  - WQ's counterexamples ⟨15,22,24,25⟩ and ⟨100,125,236,287⟩: ANCHOR slack 17 and 52;
  - the P18 depth-four DK and STAR models;
  - exhaustive P18 models at q = 5–7 (E337);
  - optimizers on P18 truncations at q = 4, 5, 6: min E + r = 7, 19, 16.
- (3) Extremal families. CORE₁ held everywhere:
  - the Fromentin W₀ = −1 examples: E + r = 3, 5, 6, 6, 7;
  - ⟨30,44,48,49⟩₁₁₈: 8;
  - Eliahou–Fromentin B₃ family: margin ≥ K + 1 by the position count, attained at ⟨14,22,23⟩₅₆ (= 3);
  - minimal-span B₄ sets at q = 5: E + r = 24, 68, 178, 423 for K = 3–6. B₄ densities 0.71, 0.57, 0.42, 0.31 are
    far below the ≈ 0.84 that failure needs;
  - Delgado-type ⟨μ, γ, γ+1⟩_{pμ}, p ≤ 32, μ ≤ 300: the minimum over E < 0 is exactly p − 1 for every even
    p ≤ 26 (and larger for odd p). Delgado's E = −383 example ⟨4505,8798,8816⟩₄₀₉₈₆₇ has r = 3,329 (computed
    from E = kℓ + qr − c).
- (4) A proof attempt is open. The depth-four case of ANCHOR for strip-free cores is essentially the kernel-checked
  external anchor theorem.

**Why this matters.** CORE₁ is a depth-independent inequality, stronger than Wilf, that the depth-four proof
establishes on its core models. ID-q turns it into a single deficit-payment problem: wraps not refunded by crossing
parents must be paid by ρ, excess crossings, unused top incidences and holes.

### Exact reformulations of CORE₁: c ≤ nℓ + (q+1)r, the degree form, and the position form (lead, 2026-10-20; PROVED; checks E339)
Setting and notation as in "ID-q for every numerical semigroup": n = K + 1 left primitives, r right primitives,
q = ⌈c/m⌉, ρ = qm − c. Reached positions x (λ_x ≤ q), degree t_x, wraps j_x = λ_x − t_x, unused weight u(x).
Write J = Σ_x j_x and s_x = λ_x·m + x − ρ (the least element of ⟨A⟩ at x).

**(R1) CORE₁ ⟺ c ≤ n·ℓ + (q + 1)·r.** This is E + r = nℓ − q(m − r) + ρ + r = nℓ + (q+1)r − c. Compare Wilf,
c ≤ nℓ + r·ℓ: in CORE₁ each right primitive is worth q + 1 instead of ℓ ≥ q + 1.

**(R2) Degree form (every S).** E = ρ + Σ_x (q − t_x)·u(x) − (K + 1)·J.
- Proof: telescope with potential q − t over used incidences (each in-weight is t_y by divisor closure). This gives
  Σ_x (q − t_x)u(x) = (K + 1)Σ_x (q − t_x) − q·d. Then use ℓ = Σ_x (q − λ_x) = Σ_x (q − t_x) − J. ∎
- Equivalently, by a second telescoping with potential j (κ = j_y − j_x on a used incidence):
  Σ_y (c_y − j_y) = Σ_x j_x·(u(x) − K − 1). So ID-q and (R2) are the same identity.
- Each wrap costs K + 1, paid by unused incidences weighted by q − degree. CORE₁ ⟺
  (K + 1)·J ≤ ρ + r + Σ_x (q − t_x)·u(x).
- **Top-level positions pay for themselves.** If λ_x = q, all K + t_x incidences are unused and q − t_x = j_x, so the
  term is j_x(K + t_x) ≥ (K + 1)j_x. The whole cost sits at wrapped positions below the top whose incidences are used.
- This is the E-analogue of the power-token identity W = U − e·T_c.

**(R3) Position form (every S).** m·(E + r) = (m + ρ)r + Σ_{unused (x,i), λ_x<q} w·(c − s_x) + (K + 1)·Σ_{λ_x<q} x
− Σ_{λ_x = q} (t_x − 1)·x.
- Proof: telescope with potential c − s, which drops by g_i on a used incidence. This gives
  Σ_unused w(c − s_x) = K·c·d − (K + 1)·Σ_x s_x. Then substitute s_x. ∎
- Equivalently (the "centre-of-mass identity"): m·Σ_y (j_y − c_y) = Σ_unused w·x − (K + 1)·Σ_reached y + ρ·d.
- No wraps appear. CORE₁ becomes a first-moment inequality: Σ_{top}(t_x − 1)x ≤ (m + ρ)r + (K + 1)Σ_{λ<q} x + (lower
  unused incidences weighted by their distance to c).
- In the free unwrapped model (positions linear in the degree, ρ = 0) it holds with equality before r is added. Wraps
  move positions down, which lowers the (K + 1)Σ_{λ<q} x term.
- These are exact rewritings, not new inequalities. Any proof of CORE₁ needs an inequality that uses the injectivity of
  positions mod m (the space constraint) or their order (translation by an anchor), as the depth-four shell does.

**(R4) CORE₁ for all truncations ("layer CORE₁").** For a P18 model (m, ρ, B) and every j ≥ 1:
  (j + 1)·N_j ≤ (K + 1)·Σ_{k<j} N_k + m + ρ, with N_k = #{x : λ_x ≤ k}.
- For S = ⟨m, m + B⟩ this reads, with τ = jm − ρ (any τ ≥ 1, j = ⌈τ/m⌉):
  τ ≤ e·|S ∩ [0, τ)| + (j + 1)·|[τ, τ + m) ∖ S|   (SW_τ).
  SW_c is Wilf. SW_τ is CORE₁ of the truncation S ∪ [τ, ∞) when τ − 1 ∉ S and τ > 2m. So it is implied by CORE₁ and is
  not a new target.
- Check (E339): 0 negative values over all j ≤ q, on 2,943 random models (strips allowed, q ≤ 14).

**Correction (to STATE A0/A00).** "Strip-free q ≤ 5 has only j ≤ 1" is FALSE at q = 5. A twice-wrapped triple
(ρ + a + b + c ≥ 2m, level 5) occurs whenever m ≥ 2ρ + 3 allows it: 5,452 of 16,227 exhaustive true-depth models
(m ≤ 22, K ≤ 5). The j ≤ 1 form N − |U| ≤ 2p + U_top + C is exact only for strip-free q ≤ 4, which is settled. In the
j ≤ 1 world, C = K|U| − u(U) (unused weight at unwrapped positions), so CORE₁ ⟺
N + (q − 1)|U_q| ≤ (K + 1)|U_{<q}| + 2r + Σ_{x∈U, λ<q}(q − 1 − λ_x)u(x) + Σ_{x∈Wr}(q − λ_x)u(x).

**Component audit at q = 5, strip-free (E339; exhaustive m ≤ 22, K ≤ 5, and 4,979 random models).**
- Dropping one hole term from the j ≤ 1 form fails (2 cases).
- Dropping ρ from ANCHOR fails once: (m, ρ, B) = (19, 5, {7, 8}), slack −2.
- Wrapped-in-window bounds without U_top fail.

### Conjecture T1 (pool-free deficit bound) — FALSE; Conjecture WR1 (the wrapped region pays for itself) (lead, 2026-10-20; checks E340)
**T1 (FALSE).** Σ_y (j_y − c_y) ≤ ρ + r. Equivalently:
- E + r ≥ P, the whole ID-q pool;
- the column form Σ_x Σ_i y(top_i(x)) ≤ (K + 1)·Σ_x y_x + (m + ρ)r;
- Σ_{α∈M} (1 + j_α − c_α) ≤ m + ρ.

Evidence before the refutation: 0 failures, minimum slack 0, on every S of genus ≤ 30 (14.4M), e = 3 exhaustive
(800,568), e = 4 random (277,368), random general S, Delgado and Fromentin truncations (pool 0 there), and 20,000
random injective multiset ideals.

Refutation (true-depth annealer, then two independent codes):
- ⟨66, 67, 71, 72, 98, 103, 128⟩: c = 326, q = 5, ρ = 4, r = 0, J − C = 6, T1 = −2. CORE₁ = E = 451.
- ⟨61, 62, 63, 67, 88, 89, 112⟩: q = 5, T1 = −1.
- ⟨64, 65, 69, 75, 95, 100⟩: q = 6, T1 = −1.
- Mechanism: small offsets {1, 5, 6} collide (1 + 5 = 6). The collisions create a large pool at low levels, and that
  pool is what pays the slight excess of wraps.
- T0 (J − C ≤ ρ) fails already at ⟨14,22,23⟩₅₆.

Lessons:
- No pool-free deficit bound holds. Some unused incidences are needed.
- A statement that is tight on census data (minimum 0 everywhere) needs an adversarial search before it is trusted.

Two exact forms found on the way (both PROVED; used below):
- **Cut form.** J − C = Σ_{k≥1} μ(U_k), where μ(α) = K + 1 − u(α) and U_k = {α ∈ M : σ_α ≥ km}. Here M is the
  canonical family and σ_α = ρ + α·b. The measure μ has total mass |M| and Σ_α μ(α)σ_α = ρ|M|.
- **Per-element form.** j_α − c_α = Σ φ_α(δ) over δ ≡ σ_α (mod m), 0 ≤ δ ≤ σ_α − m, with
  φ_α(δ) = 1 − #{copies b ∈ α : b > δ}. Here φ_α is non-decreasing and Σ_{0≤δ<σ_α−ρ} φ_α(δ) = 0 for each α.

**Conjecture WR1 (every S; UNDER GATE).** J − C ≤ ρ + r + P_W, where P_W = Σ_{x wrapped} (q − λ_x)u(x).
- Equivalently, in degree form: (K + 1)J ≤ ρ + r + Σ_{x wrapped}(q − t_x)u(x).
- Equivalently: Σ_{x∈W} f(x) + ρ + r + Σ_{crossing edges U→W} w·(q + 1 − t_y) ≥ 0, where W is the wrapped region,
  U the unwrapped region, and f(x) = (K + 1)(q − λ_x) − q. So the wrapped positions' Eliahou deficit is paid by ρ, the
  holes, and the crossing edges that feed W.
- WR1 + (unwrapped pool PU ≥ 0) ⟹ CORE₁ ⟹ Wilf.
- Necessity audit:
  - WR1 discards only the unwrapped pool PU. In the negative-Eliahou families PU = 0, so there it is CORE₁.
  - Dropping ρ (WR0) fails, 444 times in the exhaustive run.
  - Dropping all of P_W is T1, which is FALSE.
- At q = 4, strip-free, WR1 reads |Q₃| ≤ ρ + r + |Ẑ| + |Q₁| + 2|Q₀| + A (+ strip terms). The external anchor theorem
  (shell + PAYMENT) proves this plus an extra +|N40| on the right. So WR1 at q = 4 is slightly stronger than the
  kernel-checked bound.
- Status:
  - 0 failures on exhaustive true-depth models, q = 5 and 6, m ≤ 20, K ≤ 5, strips allowed (92,257), and on random
    models.
  - Survives the T1 counterexamples with margins 130 to 182.
  - True-depth annealers at q = 5–7 are running (E340).

## Theorem CF-WILF (every collision-free h-regular numerical semigroup satisfies Wilf) — PROVED 2026-10-20 (paper; checks E341)
**Setting (Bacher, arXiv:2604.25051, Defs 3.1–3.2).**
- S is a numerical semigroup with multiplicity m and conductor c. Its left generators are m < γ_1 < … < γ_n
  (all minimal generators below c), and Γ = {γ_1, …, γ_n}. Put ℓ = n + 1, q = ⌈c/m⌉, ρ = qm − c, k = |L|,
  r = number of primitive elements ≥ c, and e = ℓ + r.
- **h-regular:** hΓ ⊂ [c, c + m), where hΓ is the set of sums of exactly h elements of Γ, with repetition.
- **Collision-free (CF):** every element of S below c + m has exactly one factorization over {m} ∪ Γ.
- For α ∈ ℕⁿ write α·Γ = Σ α_iγ_i and |α| = Σ α_i. Put s = C(n+h, h) and s′ = C(n+h−1, h−1).
- E = ℓk − q(m − r) + ρ is the Eliahou number. **Identity (every S):** W = ek − c = E + r(k − q).

**Theorem CF-WILF.** If S is h-regular and collision-free, then W(S) ≥ 0. More precisely:
- (i) r ≥ |H_h(n)| − s, where H_h(n) = {z ∈ ℤⁿ : |z⁺| ≤ ⌊h/2⌋, |z⁻| ≤ ⌈h/2⌉}. So r ≥ n(n²−1)/3 when h ≥ 3, and
  r ≥ n(n−1)/2 when h = 2.
- (ii) E > ρr/m − A, with A = n(h−1)s′/h.
- (iii) W > (s′ − 1)r − A.
- Hence W > 0 unless (n, r) = (1, 0), in which case S = ⟨m, γ_1⟩ and W = 0, or (h, n) = (2, 2) with r = 1, in which
  case W ≥ 0.

**Lemma 1 (structure).** Let n ≥ 1 and h ≥ 2. (For h = 1, h-regularity forces n = 0.)
- (a) c > (h − 1)m.
  - Proof: c ≤ hγ_1, since hγ_1 ∈ hΓ.
  - Also hγ_n < c + m and γ_n > m, so c > hγ_n − m > (h − 1)m.
- (b) Position of α·Γ by degree:
  - If |α| ≤ h − 1, then α·Γ ≤ (h−1)γ_n < (h−1)(c+m)/h ≤ c. The last step uses (a).
  - If |α| = h, then α·Γ ∈ [c, c + m).
  - If |α| ≥ h + 1, then α·Γ ≥ (h+1)γ_1 ≥ c + γ_1 > c + m.
- (c) Counting left elements. Every element of S below c is a combination of left generators.
  - By (b) and CF, L = {tm + α·Γ : |α| ≤ h−1, t ≥ 0, tm + α·Γ < c}, and these representations are distinct.
  - So k = Σ_{|α| ≤ h−1} κ_α with κ_α = ⌈(c − α·Γ)/m⌉ ≥ 1, and κ_0 = q.
- (d) The non-primitive elements of [c, c + m).
  - x ∈ [c, c + m) is non-primitive iff x = y + z with y, z ∈ S∖{0}. Then y, z ≤ x − m < c, so x ∈ ⟨m, Γ⟩.
  - Conversely, x ∈ ⟨m, Γ⟩ ∩ [c, c+m) exceeds γ_n, so it is not a generator.
  - By (b), these x are the elements y_α ∈ [c, c+m) with y_α ≡ α·Γ (mod m) and |α| ≤ h; note y_α ≥ α·Γ.
  - By CF they are pairwise distinct. So m − r = #{α : |α| ≤ h} = s.
  - Also e = ℓ + r, since no element ≥ c + m is primitive.
- (e) **Residue injectivity.** The residues α·Γ mod m, |α| ≤ h, are pairwise distinct. Proof: equal residues give
  y_α = y_β, an element below c + m with two factorizations.

**Lemma 2 (difference body; the standard difference-set bound for B_h sets).** Let k_1 + k_2 = h and
A_k = {α ∈ ℕⁿ : |α| ≤ k}.
- The map z ↦ z·Γ mod m is injective on A_{k_1} − A_{k_2} = H := {z : |z⁺| ≤ k_1, |z⁻| ≤ k_2}. Hence m ≥ |H|.
- Proof of injectivity:
  - Suppose (a − a′)·Γ ≡ (b − b′)·Γ.
  - Then (a + b′)·Γ ≡ (b + a′)·Γ, with a + b′, b + a′ ∈ A_h.
  - By Lemma 1(e), a + b′ = b + a′.
- Proof that A_{k_1} − A_{k_2} = H: z = a − a′ has z⁺ ≤ a and z⁻ ≤ a′ coordinatewise. Conversely, z = z⁺ − z⁻.

**Lemma 3 (count).** |H| = Σ_p C(n,p) C(k_1,p) C(n−p+k_2, k_2).
- Derivation: choose the support of z⁺ (size p), then z⁺ on it (a positive p-tuple with sum ≤ k_1, C(k_1, p)
  ways), then z⁻ ≥ 0 on the other n − p coordinates with sum ≤ k_2.
- Vandermonde gives s = C(n + h, n) = Σ_p C(k_1,p) C(n+k_2, n−p). Hence
  |H| − s = Σ_{p ≥ 1} C(k_1, p)·[C(n,p)·C(n−p+k_2, n−p) − C(n+k_2, n−p)].
- Each bracket is ≥ 0. Injection: an (n−p)-subset T of [n] ⊔ X with |X| = k_2 maps to (P, T), where P is the set
  of the p smallest elements of [n]∖T. Then T ⊆ ([n]∖P) ⊔ X.
- The p = 1 bracket equals C(n−1+k_2, k_2)·k_2(n−1)/(k_2+1).
- With k_1 = ⌊h/2⌋ and k_2 = ⌈h/2⌉, this gives:
  - h ≥ 3 (k_1 ≥ 1, k_2 ≥ 2): |H| − s ≥ C(n+1, 2)·2(n−1)/3 = n(n²−1)/3.
  - h = 2: |H| − s = n(n−1)/2 exactly, since C(1, p) = 0 for p ≥ 2.
- Then (i) follows from Lemma 1(d) and Lemma 2: r = m − s ≥ |H| − s.

**Lemma 4 (averaging).** Proof of (ii).
- By Lemma 1(c), k ≥ Σ_{|α|≤h−1} (c − α·Γ)/m.
- Moment sum: Σ_{|α|≤h−1} α_i = Σ_{u=0}^{h−2} C(n+u, u) = C(n+h−1, h−2) =: N for each i. Since γ_i < (c+m)/h,
  Σ_{|α|≤h−1} α·Γ < nN(c+m)/h.
- N/s′ = (h−1)/(n+1), so nN/h = θs′ with θ = n(h−1)/(h(n+1)).
- Therefore ℓk > (n+1)s′[(1−θ)c/m − θ] = s·c/m − A. This uses (n+1)s′(1−θ) = s′(n+h)/h = s and
  (n+1)s′θ = A.
- Hence E = ℓk − qs + ρ > s(c/m − q) + ρ − A = ρ(m − s)/m − A = ρr/m − A.

**Proof of (iii) and the theorem.**
- Bound (iii): k − q = Σ_{1≤|α|≤h−1} κ_α ≥ s′ − 1. So W = E + r(k − q) > (s′−1)r − A + ρr/m.
- W is an integer, so W ≥ 0 as soon as (s′−1)r ≥ A − 1.
- n ≥ 2, h ≥ 3: r ≥ n(n²−1)/3 ≥ n. Also (s′−1)n − A = n(s′/h − 1) ≥ 0, because s′ ≥ C(h+1, 2) ≥ h. So W > 0.
- n ≥ 3, h = 2: r ≥ n(n−1)/2 ≥ n and s′ = n + 1 ≥ h, so W > 0.
- n = 2, h = 2: s′ = 3, A = 3, and r ≥ 1, so 2r ≥ 2 = A − 1 and W ≥ 0.
- n = 1: s′ = h and A = h − 1.
  - If r ≥ 1, then W > 0.
  - If r = 0, then S = ⟨m, γ_1⟩: every element of [c, c+m) lies in ⟨m, γ_1⟩, hence so does every element ≥ c. Then
    W = 2(c − g) − c = 0 by symmetry. ∎

**Remarks.**
- Bacher's Theorem 3.5 (W ≥ 0 for CF h-regular S when r ≥ ℓ) and Conjecture 2.6 (r < ℓ ⇒ E ≥ 0) left the class
  open. His §3.3 gives the heuristic that packing a B_3 set mod m with only ℓ gaps is "probably impossible". Lemma 2
  makes that quantitative: r ≥ n(n²−1)/3 for h ≥ 3. Bound (iii) needs only r ≥ n, not r ≥ ℓ.
- For n ≥ 3 and h ≥ 3, r ≥ n(n²−1)/3 ≥ n + 1 = ℓ. So the hypothesis r < ℓ of Bacher's Conjecture 2.6 is impossible
  for CF h-regular S, except possibly when n ≤ 2 or h = 2.
- CORE₁ (E + r ≥ 0) does NOT follow from these crude bounds. For h = 3, |H| − s = n(n²−1)/3 < A = n(n+1)(n+2)/3.
  With Bacher's exact E = E₀ + ℓω + ρ, the difference body gives CORE₁ only for n ≥ 7 (E341).
- **Mechanism, for the general programme:**
  - first-order cancellation: (n+1)Σ_{|α|<h}(1 − |α|/h) = s, which is the centroid of the simplex;
  - the boundary loss A comes from the top layer γ < (c+m)/h;
  - the right primitives pay that loss, through W = E + r(k − q), and must be numerous because the B_h tile cannot
    tile ℤ/m (difference body).
  - Collisions break Lemma 2. A collision also removes elements of the canonical down-set below the simplex, which
    raises the centroid excess. The general programme is to trade these two effects (NOTEBOOK 2026-10-20, "CF-WILF").
- Dependencies: only elementary counting (Vandermonde, hockey stick) and the definitions. It uses neither Bacher's E₀
  formula nor his Thm 3.5, nor any computer search.

## Regular semigroups with collisions: Lemma CENTROID (PROVED) and the bound REG-BND (PROVED); REG-WILF open (lead, 2026-10-20; checks E342)
**Setting.**
- S is h-regular (hΓ ⊂ [c, c+m)), with collisions allowed.
- Lemma 1(a)–(d) of CF-WILF hold without CF, except for the distinctness statements.
- Each α with |α| ≤ h has α·Γ < c + m. The degree of an element below c + m is well defined, because the value
  intervals [tc/h, t(c+m)/h) of distinct degrees t ≤ h are disjoint when c > (h−1)m.
- M ⊆ Δ_h = {|α| ≤ h} is the set of lexicographically least factorizations of the Apéry elements of ⟨m, Γ⟩ below
  c + m. It is a down-set, |M| = d = m − r, and z ↦ z·Γ mod m is injective on M.
- Notation: d_t = #{α ∈ M : |α| = t}, N_t = C(n+t−1, t), x = c/m, and k = Σ_{α∈M, |α|<h} ⌈(c − α·Γ)/m⌉.

**Lemma CENTROID.**
- Statement: for every down-set M ⊆ Δ_h(n), X(M) := (n+1)Σ_{α∈M}(1 − |α|/h) − |M| ≥ 0.
- Exact form: X(M) = Σ_{t=1}^{h}(u_t − u_{t−1})T_t, where
  - u_t = 1 − d_t/N_t (nondecreasing in t);
  - f(t) = 1 − (n+1)(h−t)/h;
  - T_t = Σ_{s≥t} f(s)N_s ≥ 0, with T_0 = 0.
- Proof:
  - (Normalized matching.) Put the weight α_i + 1 on the edge α → α + e_i between degrees t and t+1 (t < h).
    Every α of degree t has total weight t + n, and every β of degree t+1 has total weight Σβ_i = t + 1.
  - Let U = Δ_h ∖ M, an up-set, with U_t its degree-t part. Its upper shadow lies in U_{t+1}. So
    (t+n)|U_t| ≤ (t+1)|U_{t+1}|, i.e. |U_t|/N_t ≤ |U_{t+1}|/N_{t+1}.
  - Σ_{Δ_h} f = 0. This is the simplex identity (n+1)Σ_{Δ_h}(1 − |α|/h) = C(n+h, h), from PROOFS CF-WILF Lemma 4.
    Hence X(M) = −Σ_M f = Σ_U f = Σ_t f(t)N_t u_t.
  - Apply Abel summation. f is increasing and has total sum 0, so every tail sum T_t is ≥ 0. ∎

**Bound REG-BND.** For every h-regular S:
  W > ρr/m + x·X(M) − B(M) + r(k − q), with B(M) = ((n+1)/h)·Σ_{t<h} t·d_t.
- Proof: as in CF-WILF Lemma 4, with sums over M.
  - k ≥ Σ_{α∈M, |α|<h}(c − α·Γ)/m.
  - α·Γ < |α|(c+m)/h.
  - (n+1)Σ_{M}(1 − |α|/h) = d + X.
  - W = E + r(k − q). ∎
- In the CF case, X = 0 and B = A; CF-WILF then follows from the difference body.

**Status of REG-WILF (Wilf for every h-regular S).** OPEN.
- REG-BND certifies W ≥ 0 (bound ≥ −1) except when r is small and X is small.
  - The exhaustive m ≤ 18 exceptions are two-generated S (W = 0), or h = 2 with r = 0 and one collision.
- Missing ingredient: a difference-body bound that survives collisions.
  - Each coincidence (a − a′)·Γ ≡ (b − b′)·Γ in H comes from a collision pair (a + b′, b + a′) in Δ_h.
  - Each collision pair costs at most splits(μ)·splits(ν) elements of H.
  - The collisions themselves raise X by Σ_U f ≥ n·u_h, through the factor x = c/m ≥ h − 1.
- For h ≤ 4, the regime q ≤ 4 is covered by the depth-four theorem (LITERATURE).

## Ray identity, one-step difference body, and Theorem P0-WILF — PROVED 2026-10-20 (paper; checks E344)
**Setting (every S with c > m).**
- Left generators m < γ_1 < … < γ_n < c, with Γ = (γ_i) and n ≥ 1. Write φ(α) = α·Γ.
- M ⊆ ℕⁿ is the set of lexicographically least Γ-factorizations of the Apéry elements of ⟨m, Γ⟩ (w.r.t. m) that are
  < c + m.
  - M is a down-set. If β ≤ α ∈ M, then φ(β) is an Apéry element, and a lex-smaller factorization of it would give
    one of φ(α).
  - z ↦ φ(z) mod m is injective on M.
  - |M| = d = m − r.
- Put x_α = (c − φ(α))/m and κ_α = ⌈x_α⌉. Then k = Σ_{α∈M, φ(α)<c} κ_α and κ_0 = q.
- M_< = M ∩ {φ < c} and Y = M ∩ {φ ≥ c} (the top). For y ∈ Y, θ_y = (φ(y) − c)/m ∈ [0, 1).
- Rays: for β ∈ M, the i-ray {β + t e_i} ∩ M is an initial segment. Its last point is end_i(β). Since γ_i > m, every
  y ∈ Y is the end of all its rays, and every lower neighbour of y lies in M_<.

**Ray identity (PROVED, every S).** E = ρr/m + G + P̃ − Λ, and hence W = ρr/m + G + P̃ − Λ + r(k − q), where
- G = ℓ Σ_{α∈M_<}(κ_α − x_α) ≥ 0 (ceiling gains);
- P̃ = (1/m) Σ_{z∈M_<} Σ_{i: z+e_i∉M} (z_i + 1)(c − φ(z)) ≥ 0 (rays ending below c);
- Λ = Σ_{y∈Y} (|y| − 1)θ_y ≥ 0 (top loss).

*Proof.*
- E = ℓk − qd + ρ and ℓk = G + (ℓ/m)Σ_{M_<}(c − φ).
- For a down-set, Σ_{α∈M} α_i = Σ_{β∈M} ℓ_i(β), where ℓ_i(β) = #{t ≥ 1 : β + te_i ∈ M}. Hence
  Ξ := ncd − (n+1)Σ_M φ = Σ_{β∈M} Σ_i [c − φ(end_i(β))].
- Group the rays by their end z. The point z is the end of the i-rays from z − te_i (0 ≤ t ≤ z_i), for every i with
  z + e_i ∉ M.
  - For z ∈ Y, every i qualifies, so Ξ receives −(|z| + n)(φ(z) − c).
  - For z ∈ M_<, Ξ receives m times its P̃-term.
- Then ℓΣ_{M_<}(c − φ) = cd + Ξ + ℓΣ_Y(φ − c), and the Y-terms combine to −Σ_Y(|z| − 1)(φ(z) − c).
- Finally d(c − qm)/m + ρ = ρr/m. ∎
- Checked exactly, with Fractions, on 3,000 random S plus all S of E344.
- This is the ray form of the position identity R3 (PROOFS "Exact reformulations of CORE₁"). Only the top elements of
  degree ≥ 2 are a loss.

**One-step difference body (PROVED, every S).** Let M_1 = {β ∈ M : β + e_i ∈ M for all i} (the interior). Then
  r ≥ R_gen := Σ_{z ∈ M∖M_1} (deg⁻_{M_1}(z) − 1), where deg⁻_{M_1}(z) = #{i : z_i ≥ 1, z − e_i ∈ M_1}.

*Proof.*
- Injectivity: M_1 + Δ_1 ⊆ M and M is injective mod m. So, as in CF-WILF Lemma 2, z ↦ φ(z) mod m is injective on
  M_1 − Δ_1. Hence m ≥ |M_1 − Δ_1| = |M_1| + Σ_i |F_i(M_1)|, where F_i(M_1) = {β ∈ M_1 : β_i = 0}. The points β − e_i
  with β_i = 0 are new and pairwise distinct.
- Counting: every i-ray of M_1 starting on F_i(M_1) leaves M_1 at a point z ∈ M ∖ M_1 with z − e_i ∈ M_1, and this
  is a bijection onto the pairs (z, i). So Σ_i |F_i(M_1)| = Σ_{z∈M∖M_1} deg⁻_{M_1}(z).
- Subtract |M| = |M_1| + |M ∖ M_1|. ∎

**Theorem P0-WILF.** Suppose P̃ = 0, that is, M_< + e_i ⊆ M for every i (no ray of M ends below c). If c ≥ 4m, then
W(S) ≥ 0. Together with the depth-four theorem (c ≤ 4m; LITERATURE, kernel-checked by us), every S with P̃ = 0
satisfies Wilf.

*Proof.*
- (a) Structure. M_1 = M_< and M ∖ M_1 = Y. Every lower neighbour of y ∈ Y lies in M_<, so deg⁻_{M_1}(y) = |supp y|.
  - The one-step difference body gives r ≥ R := Σ_{y∈Y}(|supp y| − 1).
  - If n ≥ 2, then R ≥ 1: the 1-ray from e_2 ∈ M_< ends at some e_2 + je_1 ∈ Y.
- (b) Bijection. (β, i) with β ∈ M_< and β_i ≥ 1 ↔ (y, t) with y the end of the i-ray from β and t = y_i − β_i,
  where 1 ≤ t ≤ y_i − 1. Hence Σ_{y∈Y}(|y| − 1) = Σ_{β∈M_<} |supp β| + R.
- (c) Exits. Count the pairs (β, i) with β ∈ M_<, i ∈ [n], weighted by |supp(end_i(β))| − 1.
  - Grouped by β, the weight is ≥ (n − 1)|supp β|: the end adds coordinate i to the support when i ∉ supp β.
  - Grouped by y, the weight is Σ_Y |y|(|supp y| − 1) ≤ D·R, where D = max_{y∈Y}|y| ≥ 2.
  - So (n − 1) Σ_{M_<} |supp β| ≤ D·R.
- (d) Depth of the chain. Let y* ∈ Y have |y*| = D, and take a saturated chain 0 ⋖ β_1 ⋖ … ⋖ β_{D−1} ⋖ y*. All
  β_t ∈ M_<.
  - Along an up-step inside M_<, x drops by γ_i/m > 1, so κ drops by ≥ 1. Hence κ_{β_t} ≥ D − t.
  - The other n − 1 unit vectors are in M_< and off the chain. So
    k − q = Σ_{M_<∖0} κ ≥ D(D−1)/2 + (|M_<| − D) ≥ D(D−1)/2 + n − 1.
  - Therefore k − q − 1 ≥ D/(n − 1) when n ≥ 3, and when n = 2 with D ≥ 3.
  - Case n = 2, D = 2. Then M_< = {0, e_1, e_2}, 2γ_1 ≥ c and γ_1 + γ_2 < c + m. So γ_i < c/2 + m and
    x_{e_i} > c/(2m) − 1 ≥ 1, which gives κ_{e_i} ≥ 2 and k − q − 1 ≥ 3 > D. This is the only use of c ≥ 4m.
- (e) n ≥ 2. Since P̃ = 0, G ≥ 0 and r ≥ R:
  W ≥ R(k − q) − Λ ≥ R(k − q) − Σ_Y(|y| − 1) = R(k − q − 1) − Σ_{M_<}|supp β| ≥ R·D/(n−1) − Σ_{M_<}|supp β| ≥ 0,
  using (b), (c) and (d).
- (f) n = 1. M_< = {0, e, …, (a−1)e} and Y = {ae}.
  - If r = 0, then S = ⟨m, γ_1⟩ and W = 0.
  - If r ≥ 1, then W ≥ (k − q) − (a − 1)θ ≥ Σ_{t=1}^{a−1} κ_{te} − (a − 1) ≥ 0. ∎

**Remarks.**
- Every collision-free h-regular S has P̃ = 0, since M = Δ_h and M_< = Δ_{h−1}. So P0-WILF contains CF-WILF for
  c ≥ 4m, with a shorter proof.
- P̃ = 0 holds for 388 of the 390 negative-Eliahou Delgado truncations ⟨μ, γ, γ+1⟩ ∪ [pμ, ∞) with p ≤ 12, μ ≤ 60
  (E344).
- The class is defined for every S. It asks for the gap {φ ∈ [c + m − γ_n, c)} ∩ ⟨Γ⟩ = ∅ and for no collision
  inside M_< + Δ_1.
- Open: the general case P̃ > 0. The ray identity and the one-step DB hold for every S.
  - Conjecture GDB: W with r replaced by max(R_gen, [r ≥ 1]) is > −1. 0 failures on 6,000 random S with q ≥ 2 and
    q ≥ 5 (E344).
  - Its r = 0 part is literally E ≥ 0.

## The full lex tile; leaves; Conjecture TOP0 — 2026-10-20
(Cross-reference: Lemmas T1 and T2 are CH′ and the Tile-TOP'' bookkeeping in ray form. TOP0 is MaxCL at the conductor
phase, restricted to the top window of a leaf. See PROOFS "MaxCL".)
**Setting.**
- g_1 < … < g_N are all minimal generators other than m, so N = e − 1. Right primitives are included.
- M̂ ⊆ ℕ^N is the set of lex-least factorizations (last coordinate compared first) of the m Apéry elements. It is a
  down-set and a complete residue system for L = ker(φ mod m), i.e. a lattice tile (HRW 2018, Prop. 2.3/2.5).
- Ŷ = {y ∈ M̂ : φ(y) ≥ c} (the top window). θ_y = (φ(y) − c)/m.
- end_i(β) is the last point of the i-ray from β in M̂.

**Lemma T1 (CH′ in ray form; every S).**
  mW = Σ_{β∈M̂} Σ_{i=1}^N (c + m − 1 − φ(end_i β)) − (N−1)m(m−1)/2
     = (N+1)m(m−1)/2 + Σ_{β,i} (c − φ(end_i β)).
*Proof.* For a down-set, Σ_{α∈M̂} α_i = Σ_β ℓ_i(β), where ℓ_i(β) is the number of further i-steps from β. So
Σ_{β,i} φ(end_i β) = (N+1)Σ_{M̂}φ. Also Σ_{M̂}φ = Σ Ap = mg + m(m−1)/2 and W = (N+1)(c−g) − c. ∎

**Lemma T2 (residue form; every S).** W = (N+1)(m−1)/2 + P̂ − Σ_{y∈Ŷ}(|y| + N)θ_y, where
  P̂ = (1/m)Σ_{z: φ(z)<c} Σ_{i: z+e_i∉M̂} (z_i+1)(c − φ(z)).
*Proof.* Group the terms of T1 by ray end z. The point z ends the i-rays from z − te_i (0 ≤ t ≤ z_i) for each i with
z + e_i ∉ M̂, and every i qualifies when z ∈ Ŷ (since g_i > m). ∎
- Equivalently, this is the ray identity on M̂: W = Ĝ + P̂ − Λ̂ with Ĝ = (N+1)Σ_{M̂_<}{(φ−c)/m}. The values
  {(φ−c)/m} over M̂ run over {0, 1/m, …, (m−1)/m}.
- Checked: 0 mismatches on 2,668 S (E345).

**Lemma T3 (every S).** Every Apéry element w ≥ c is maximal for ≤_S in Ap(S, m). So Ŷ ⊆ PF(S) + m and |Ŷ| ≤ t(S).
*Proof.* w + s ≥ c + m > max Ap for every s ∈ S∖{0}. ∎

**Lemma T4 (right-primitive directions; every S with n ≥ 1).** For the direction p of a right primitive,
B^p := Σ_β (c+m−1 − φ(end_p β)) ≥ m(m−1)/2.
*Proof.* end_p(β) = β for β ≠ 0, and end_p(0) = e_p. So B^p/m = (m−1)/2 + ℓ − p/m with ℓ = |L|. Moreover
p < c + m ≤ (q+1)m, and ℓ ≥ q + 1 because a left generator exists. ∎
(The analogous per-direction bound fails for left directions; ALL-BUT-ONE in FAILED.)

**Leaves.**
- S is a leaf of the semigroup tree ⟺ r = 0 ⟺ S = ⟨L(S)⟩ (Delgado 2019, Rem. 5.15). Then M̂ = M, N = n, and the ray
  identity reads W = G + P̃ − Λ with G = (n+1)[(m−1)/2 − Σ_{y∈Y}θ_y].
- **Threshold shift (leaves).** Write c = qm − ρ and W′ := (n+1)|S ∩ [0, qm)| − qm. Then W = W′ − nρ.
  - W′ obeys the same ray identity with threshold qm (the algebra needs only M ⊆ {φ < qm + m}).
  - Its top set is U = {u : x_u = q}, the residues of maximal Kunz coordinate, and there φ(y) − qm = u.

**Conjecture TOP0 (leaves, n ≥ 2).** Λ ≤ G, i.e. Σ_{y∈Y}(|y| + n)(φ(y) − c) ≤ (n+1)m(m−1)/2.
- It implies W ≥ P̃ ≥ 0, so Wilf for every leaf.
- Status: 0 failures on all 5,411,788 leaves with n ≥ 2 and genus ≤ 30; min m(G − Λ) = 2 at ⟨5,16,17⟩ (c = 30).
  Annealing min 0.4 (E345).
- It is false without r = 0: TOP fails on the P0 class with large r (FAILED).
- **Weaker form TOP0′ (threshold qm, ρ-free):** Σ_{u∈U}(deg w_u − 1)·u ≤ (n+1)Σ_{u∉U} u, with deg the lex degree.
  - Mechanism: ε := φ mod m is subadditive on M and satisfies ε(β) + ε(y−β) ≥ ε(y) for β ≤ y (box pairing).
  - So TOP0′ follows from SUBADD-TOP for the down-set ↓U.
  - SUBADD-TOP is FALSE for general down-sets with ≥ n+2 maximal elements (FAILED). No failure with ≤ n+1 (E345).
  - TOP0′ alone does not give Wilf when ρ > 0: it needs P̃′ ≥ nρ in addition.

## Conjecture TM (tile-max) — 2026-10-20: IDENTICAL TO MaxCL (2026-10-17), re-derived without consulting the record
**CORRECTION (2026-10-20, same day).** TM is exactly MaxCL (PROOFS "MaxCL (lift-free, CONJ, 2026-10-17)"), with d = n,
r = ε and σ = −λ. Consequences:
- MaxCL ⇒ Tile-TOP'' ⇒ Wilf is already LEAN-checked.
- The degree-≤2 case is Flat-MaxCL (LEAN), and the window argument below is the same one.
- The shape-only rearrangement is R-TOP (already FALSE). The partial-tile extension is already FALSE.
Nothing in this section is new except the data (E345, E346), the TOP0 census of leaves, and the HALL-TM check at λ = 0.
It is kept only as a cross-reference. The MaxCL line (height-3 residual, WRAP-MAX, general σ) is where work resumes.
**Statement (Conjecture TM).** Let n, m ≥ 1, let χ: ℤ^n → ℤ/m be a surjective homomorphism, let D ⊆ ℕ^n be a down-set
with |D| = m on which χ is injective (so D is a fundamental domain of ker χ), and let λ ∈ ℤ/m. Put
ε(α) ∈ {0, …, m−1}, the representative of χ(α) + λ. Then
  Σ_{y ∈ Max(D)} (|y| + n)·ε(y) ≤ (n+1)·m(m−1)/2,
where Max(D) is the set of componentwise-maximal elements and |y| = Σ y_i.
- Equivalent forms (ε is a bijection D → {0..m−1}):
  - Σ_{Max}(|y| − 1)ε(y) ≤ (n+1)Σ_{D∖Max} ε;
  - Σ_{(β,i): end_i(β) ∈ Max} ε(end_i β) ≤ (n+1)Σ_D ε.

**Theorem (TM ⇒ Wilf).** If TM holds for the full lex tile M̂ of S (n = N = e − 1, χ = φ mod m, λ = −c), then
W(S) ≥ P̂ + (1/m)Σ_{y∈Max(M̂), φ(y)<c} (|y| + N)·ε(y) ≥ 0.
*Proof.*
- Lemma T2: mW = (N+1)m(m−1)/2 + mP̂ − Σ_{y∈Ŷ}(|y| + N)(φ(y) − c).
- For y ∈ Ŷ we have φ(y) − c = ε(y), and Ŷ ⊆ Max(M̂), because y + e_i has φ ≥ c + g_i > c + m − 1 = max Ap.
- Since ε ≥ 0 on Max ∖ Ŷ, TM gives Σ_{Ŷ}(|y| + N)ε(y) ≤ (N+1)m(m−1)/2 − Σ_{Max∖Ŷ}(|y| + N)ε(y). ∎
- The restriction to Ŷ with λ = −c is TOPH ⟺ W ≥ P̂ ⟺ Λ ≤ Ĝ, where Ĝ = e·Σ_{w∈Ap, w<c}{(w−c)/m}.
- The restriction to leaves is TOP0.

**Status (E346).**
- Exhaustive, every down-set tile, every χ, every λ:
  - n = 2: m ≤ 13 with all λ, m ≤ 16 with λ = 0;
  - n = 3: m ≤ 8 with all λ, m ≤ 10 with λ = 0.
- Annealed: lex tiles of random S with every unit u and every λ (all affine relabellings).
  - Max ratio LHS/RHS: 1 at m ≤ 5 (equality); 0.962 for m ∈ [15, 50]; 0.939 for m ∈ [25, 60].
- Equality cases are sporadic and small:
  - chains (n = 1, χ = id, λ = 0), i.e. two-generated S;
  - Δ_1 = {0, e_1, …, e_n} (m = n+1, λ = 0), i.e. the family T_{m,k};
  - {0, e_1, …, e_{n−1}, e_n, 2e_n} (m = n+2, λ = 1).
- Not implied by anything weaker:
  - the shape-only version (residues replaced by the rearrangement bound) fails for n = 3 by ≤ 4%;
  - RISE (dropping Σ(n − |I(β)|)ε) fails;
  - λ = 0 plus P̂′ ≥ Nρ fails (PSHIFT, 41/2,165).

### SUPP-WILF: W ≥ Dep − κ₀ + N ≥ Dep − Σ_x(|supp x| − 1)⁺ for every S — PROVED 2026-10-20 (paper; elementary)
**Setting.**
- S is a numerical semigroup with multiplicity m and minimal generators m < g_1 < … < g_d (d = e − 1 ≥ 1).
- c is the conductor, ℓ = c − g, W = e·ℓ − c, M′ = m(m−1)/2.
- A *factorization tile* is a down-set D ⊂ ℕ^d such that x ↦ w(x) := x·g is a bijection D → Ap(S,m). The lex-least
  factorizations give one.
- δ_b = g_b mod m. ⟨u⟩ denotes u mod m ∈ [0, m).
- For x ∈ D and a direction b:
  - k_b(x) = max{k : x + k e_b ∈ D} and t_b(x) = x + k_b(x) e_b (the b-column top above x);
  - A = {x : x + e_b ∉ D for all b} (maximal cells);
  - Dep = #{(x,b) : t_b(x) ∉ A}.
- Conductor labels: r(x) = ⟨w(x) − c⟩.

**Theorem.** W ≥ Dep − κ₀ + N, where
    κ₀ = Σ_{x∈D} ⌊ Σ_b ⟨x_b δ_b⟩ / m ⌋,      N = #{(x,b) : k_b(x) ≥ 1, r(x) > r(t_b(x))}.
Corollaries:
- (i) W ≥ Dep − κ₀.
- (ii) Since ⌊Σ_b⟨x_bδ_b⟩/m⌋ ≤ |supp x| − 1 for x ≠ 0: **W ≥ Dep − Σ_{x∈D}(|supp x| − 1)⁺**.
- (iii) **Wilf holds whenever Σ_{x∈D}(|supp x| − 1)⁺ ≤ Dep** for some factorization tile. This is a condition on the
  shape of D only. More generally, Wilf holds whenever κ₀ ≤ Dep, which uses only D and the residues δ.

**Proof.**
1. *Selmer and Euler.*
   - Since w mod m is a bijection onto ℤ/m, Σ_D w = mg + M′.
   - On a b-column of length L, k_b takes the values L−1, …, 0, so Σ_x k_b(x) = Σ_x x_b.
   - Hence Σ_{(x,b)} w(t_b x) = dΣ_D w + Σ_b g_b Σ_x x_b = (d+1)Σ_D w.
   - Therefore mW = m(dc − (d+1)g) = (d+1)M′ − Σ_{(x,b)} (w(t_b x) − c). (This is CH′.)
2. *Sharp top bounds.*
   - Every Apéry element is ≤ c + m − 1, and w(t) − c ≡ r(t). So w(t) − c ≤ r(t).
   - If t ∉ A, then w(t) + g_a ∈ Ap for some a. So w(t) − c ≤ m − 1 − g_a < 0, hence w(t) − c ≤ r(t) − m.
   - Thus mW ≥ (d+1)M′ + m·Dep − Σ_{(x,b)} r(t_b x).
3. *Inversions.*
   - r(t_b x) − r(x) ∈ (−m, m) and ≡ k_b(x)δ_b. So r(t_b x) − r(x) = ⟨k_b(x)δ_b⟩ − m·[r(x) > r(t_b x)].
   - Summing, with Σ_{(x,b)} r(x) = dM′: Σ_{(x,b)} r(t_b x) = dM′ + Σ_{(x,b)}⟨k_b(x)δ_b⟩ − mN.
4. *Column reflection and the axis overflow.*
   - As in step 1, Σ_x ⟨k_b(x)δ_b⟩ = Σ_x ⟨x_bδ_b⟩.
   - Σ_b⟨x_bδ_b⟩ ≡ x·δ ≡ w(x), and x ↦ ⟨x·δ⟩ is a bijection onto ℤ/m. So Σ_{(x,b)}⟨x_bδ_b⟩ = M′ + mκ₀.
5. Combining: Σ_{(x,b)} r(t_b x) = (d+1)M′ + m(κ₀ − N), so mW ≥ m(Dep − κ₀ + N). ∎

**Remarks.**
- N and κ₀ are the two sides of the Tile-CL inversion identity V = N − κ₀ (NOTEBOOK night 11). The new ingredients are:
  - step 2's Dep term (DEP-CARRY);
  - the reading of κ₀ as an axis-overflow count, which makes the trivial bound N ≥ 0 usable.
- Checks:
  - wsupp.py asserts W ≥ Dep − κ₀ + N ≥ Dep − Σsupp with a brute-force W on 3,000 random S;
  - Σsupp ≤ Dep held for all of them (2,240 in the open regime 3e < m, c > 4m), minimum (Dep − Σsupp)/m = 0.118 in
    the open regime;
  - all 6,000 random tiles (δ and −δ) satisfy it.
- The criterion fails only for simplex-like tiles (near-perfect B_h bases). The CR-TILE counterexample
  ⟨19,39,41,50,52,53⟩ has Dep = 4 < Σsupp = 8; its mirror ⟨19,35,37,43,45,61⟩ has κ₀ = 5 > Dep = 4. There N ≥ 6 at
  every phase, and Tile-CL holds.
- Every known Tile-CL failure satisfies Dep ≥ Σsupp:
  - E47: 20 ≥ 3;
  - the E244 −3 tile: 183 ≥ 22;
  - ⟨70,73,104,110,223,299⟩: 189 ≥ 56;
  - ⟨33,53,60,67,69,88⟩: 99 ≥ 26;
  - ⟨27,43,56,68,72,87,119⟩: 50 ≥ 11.
- Residual for Wilf after SUPP-WILF: S all of whose factorization tiles have κ₀ > Dep, i.e. a simplex-like Apéry set.
  - CONJ TCL-DICHOTOMY: Tile-CL holds whenever Dep < Σsupp. It would close DEP-ALL, and with it Wilf.
- Novelty: web searches (2026-10-20) found no comparable support or column-top criterion. Zhai 1111.2779 has CH′ in crude
  form; Marashdeh 2608.12531 has a different identity.

## Dependency chain to full Wilf via SUPP-WILF — status of every link (2026-10-20)
**Chain.**
- Fix S with S ≠ ℕ and let D be its lex factorization tile (`S.factDownSet` in Lean).
- Case A (Σsupp ≤ Dep): Wilf by L4.
- Case B (Σsupp > Dep): Wilf follows from L7 (height ≤ 2) and then L5.
- So **Wilf ⇐ L7**, given L1–L5. L7 is the only open link. Its needed form is CASEB-FLAT-S, not the lattice form.
  - L0 shrinks the range in which L7 is needed.
  - L6 makes L7 quantitative.

| link | statement | status |
|---|---|---|
| L0 | Wilf for c ≤ 4m, and for 3e ≥ m | c ≤ 4m: external proof, kernel-checked by us (STATE item 0k). 3e ≥ m: Eliahou, cited. Not used by the chain, but L7 is needed only for c > 4m, 3e < m |
| L1 | CH′: mW = (d+1)M′ − Σ_{(x,b)}(w(t_b x) − c) for every factorization tile | PROVED (paper). Its ingredients (Selmer sum `sum_wt`, column identity `columnIdentity`) are in lean/Wilf/MaxCL.lean; CH′ in this form is not a separate Lean theorem |
| L2 | Sharp top bounds: w(t) − c ≤ r(t), and ≤ r(t) − m for t ∉ A | PROVED (paper; SUPP-WILF step 2) |
| L3 | Inversion and axis-overflow identities: Σ r(t_b x) = dM′ + Σ⟨k_bδ_b⟩ − mN; Σ_{(x,b)}⟨x_bδ_b⟩ = M′ + mκ₀ | PROVED (paper; steps 3–4); checked (invcheck.py, k0stat.py) |
| L4 | **SUPP-WILF**: W ≥ Dep − κ₀ + N ≥ Dep − Σsupp = m − 1 + Q − Σ_{y∈A}|y|, for every factorization tile | PROVED (paper); checked (wsupp.py). NOT formalized; Lean queued (codex from 2026-10-25) |
| L4′ | L1–L4 with Ap(S,n) for any minimal generator n, with Dep′_n counting a non-maximal top only if it has a witness g_a ≥ n or r(t) ≥ n − g_a | PROVED (paper, same proof; see below); checked (multin.py) |
| L5 | **Flat-MaxCL**: a lex tile of height ≤ 2 ⇒ Wilf | LEAN (`wilf_of_factDownSet_height_le_two`, lean/Wilf/MaxCL.lean; 0 sorry; standard axioms) |
| L6 | Height-2 margin identity: Σsupp − Dep = C(d,2) − 3k_mixed − 2k_loop + (d+1)z | PROVED (paper; below); checked (margcheck.py, 2,000 tiles) |
| L7 | **CASEB-FLAT-S**: if S has c > 4m and 3e < m and its lex factorization tile has Dep < Σsupp, that tile has height ≤ 2 | CONJ. 0 counterexamples. THREATENED at large d (L6 + sum-cover data) |

**L4′, proof.** Let D be a factorization tile for Ap(S,n), d = e − 1 directions (the generators other than n), and let
r = ⟨w − c⟩ mod n.
- Selmer for Ap(S,n), with the column identity, gives nW = (d+1)n(n−1)/2 − Σ_{(x,b)}(w(t_b x) − c) exactly as in L1.
- max Ap(S,n) = F + n gives w(t) − c ≤ r(t).
- Let t ∉ A have witness a (w(t) + g_a ∈ Ap(S,n)). Then w(t) − c ≤ n − 1 − g_a.
  - If g_a ≥ n, this is negative, so w(t) − c ≤ r(t) − n.
  - If g_a < n but r(t) ≥ n − g_a, then w(t) − c ≠ r(t), and again w(t) − c ≤ r(t) − n.
- Steps 3–5 of SUPP-WILF use only the tile property mod n. ∎
- Use. Case A at any one n (or for any one factorization tile, lex or not) gives Wilf.
  - ⟨19,35,37,43,45,61⟩ is in case B at n = m and in case A at n = 35.
  - ⟨19,39,41,50,52,53⟩ is in case B at every n. It has height 2, so L5 covers it.

**L6, proof.** Height ≤ 2 cells are 0, the e_a, and e_a+e_b for ab ∈ E (loops aa allowed).
- Notation. k_mixed and k_loop count the missing cells e_a+e_b (a < b) and 2e_a. Z = {a : no ab ∈ E} and z = |Z|.
- Σsupp: only the mixed cells count, so Σsupp = C(d,2) − k_mixed.
- Dep: tops of height-2 cells are maximal.
  - (0,b) counts iff bb ∉ E and b ∉ Z (then t_b(0) = e_b is non-maximal).
  - (e_a, b) with b ≠ a counts iff ab ∉ E and a ∉ Z.
  - (e_a, a) counts iff aa ∉ E and a ∉ Z.
  - So Dep = 2(k_loop − z) + 2k_mixed − 2C(z,2) − z(d − z) = 2k_mixed + 2k_loop − (d+1)z.
- Subtracting gives the identity. ∎
- With z = 0: case B ⟺ μ := C(d,2) − 3k_mixed − 2k_loop > 0.
- A height-2 tile is a set {0} ∪ δ of size d+1 whose pairwise sums (repetition allowed) cover ℤ/m. So m = C(d+2,2) − k,
  where k = k_mixed + k_loop.
- Case B (z = 0) needs 3k − k_loop < C(d,2) with k_loop ≤ d, hence **m > (d+1)(d+3)/3** (PROVED, from L6).
  - So m is about d²/3 or more: a near-maximal cyclic sum cover.
  - With Haanpää's n′(d+1), height-2 case B (z = 0) is impossible for d = 6, since n′(7) = 21 ≤ 7·9/3 = 21. This
    explains the empty d = 6 census.
  - Likewise impossible for d = 2 (n′(3) = 5).
  - Counting does not exclude it for d = 3, 4, 5 and 7 ≤ d ≤ 12. For d = 3 none was found (m ≤ 14). For d ≥ 13,
    n′ is not known to us.
- Data (LITERATURE 2026-10-20 B; Haanpää's n′(k), k = d+1). Every extremal cover forces the margin range:
  - d = 4, m = 13: μ ∈ [0, 2] (observed 1);
  - d = 5, m = 19: μ ∈ [4, 6] (observed 4);
  - d = 7, m = 30: μ ∈ [3, 9] (observed 5);
  - d = 11, m = 63: μ ∈ [10, 21];
  - d = 12, m = 67: μ ≤ 6.
  (CORRECTION 2026-10-20, same evening: first recorded as [10, 25] and ≤ 18, which forgot k_loop ≤ d.)
  Equivalent form (z = 0): μ = 3(m − 1 − d) − d(d+1) − u_l, with u_l = d − k_loop the number of loop cells used.
  So the largest height-2 margin at size m is 3m − (d+1)(d+3) − max(0, d − k).
  These ranges assume z = 0 and lifts that realize the height-2 tile.

**Why L7 is threatened, and what a proof must use.**
- If n′(k)/k² stays above 1/3 as k → ∞ (data: 0.40–0.47 for 7 ≤ k ≤ 13; no asymptotic constant found), then height-2
  case-B tiles have margin about (3n′/k² − 1)d², quadratic in d.
- Adding one height-3 cell costs about d − 1 of margin: it adds supports and removes maximality from about d tops.
- So for large d, counting alone does not exclude case-B tiles with a few height-3 cells. A proof of L7 must use
  something beyond the margin, e.g.:
  - the one-step difference body Σ_{z∈∂}(deg⁻_I(z) − 1) ≤ 0 (PROOFS "Ray identity");
  - or the Apéry minimality of the lifts, which lattice tiles lack.
- Necessity audit: the lattice form CASEB-FLAT ("every lattice tile with Dep < Σsupp has height ≤ 2") is STRONGER than
  L7 (Pattern B). The census of d ≤ 4 is over lattice tiles; the d ≥ 5 census is over S. Prefer L7 when proving.

**Fallbacks if L7 fails** (none proved):
- F1. MaxCL for tiles of height ≤ 2 plus h₃ height-3 cells, with h₃ bounded by the margin (extend Flat-MaxCL's
  wrap-window argument). CONJ, not attempted.
- F2. The full bound in case B: N ≥ κ₀ − Dep. N ≥ 4–20 on every case-B S seen. This is TCL-DICHOTOMY / DEP-ALL; open,
  0 failures.
- F3. Case A at some other minimal generator n (L4′), or for some non-lex factorization tile. Not a full fallback:
  ⟨19,39,41,50,52,53⟩ is in case B at every n. Non-lex tiles are untested.

### Chain update (2026-10-20, night): L7 is FALSE; the open link is now L7′ (case B ⇒ the full SUPP bound is ≥ 0)
- **L7 (CASEB-FLAT-S) is FALSE.**
  - S = ⟨63,239,282,295,318,333,379,386,390,400,405,407⟩ (c = 750, e = 12, open regime) has a lex tile of height 3
    (3·239 ∈ Ap), Dep = 42 < Σsupp = 44 and W = 1278.
  - It was built from Haanpää's sum cover of ℤ/63 by choosing the tile and the lifts jointly (E353). Both computations
    agree.
  - The lattice form fails already for the same δ (μ = 4 with one cubic).
  - L7 holds for every height-≤3 lattice tile with d ≤ 5 (exhaustive, E352). Records: FAILED Pattern D;
    examples/caseb_height3_counterexample.md.
- **L7′ (the needed statement):** if the lex tile of an open-regime S is in case B, then N(σ_c) + Dep ≥ κ₀.
  - Here σ_c = c mod m and N is the column-inversion count at the conductor phase.
  - Equivalently W ≥ Dep + V(σ_c) ≥ 0, i.e. Tile-CL at the conductor phase up to Dep. With L4 (case A) it gives Wilf.
  - Sufficient for L7′:
    - TCL-DICHOTOMY (Tile-CL at every phase in case B; 0 failures so far, including the counterexample above, V ≥ 11);
    - MaxCL restricted to case-B tiles (slack ≥ 1663 there);
    - DEP-ALL.
  - Flat-MaxCL (LEAN) gives L7′ on case-B tiles of height ≤ 2.
- **Status of the chain:** Wilf ⇐ L4 (PROVED, paper) + L7′ (CONJ). The case-B residue is still confined to
  near-perfect sum covers: case B needs a large flat margin, i.e. m > (d+1)(d+3)/3 at height 2 (L6). The closed form
  above bounds what the height-3 cells can cost.

### SUPP-WILF+ (level form): W ≥ Dep − Σsupp + Σ_{y∈A_<}(|y|+d)μ_y ≥ Dep − Σsupp + (d+1)|A_<| — PROVED 2026-10-20 (paper; checks E356)
**Setting.** As in SUPP-WILF. For x ∈ D put μ_x = ⌈(c − w(x))/m⌉⁺, the number of elements of S below c in the class of
w(x). Let om(x) = Σ_{b: x+e_b∉D}(x_b + 1), the total length of the columns topped at x. Let A_< = {y ∈ A : w(y) < c}.

**Theorem.**
- (i) (exact) W = N(σ_c) − κ₀ + Σ_{x∈D} om(x)·μ_x, and ℓ = Σ_{x∈D} μ_x.
- (ii) W ≥ Dep − κ₀ + N + Σ_{y∈A_<}(|y| + d)μ_y + Σ_{t∈D∖A, om(t)>0} om(t)(μ_t − 1) ≥ Dep − Σsupp + (d+1)|A_<|.
- (iii) Every Apéry element ≥ c is maximal, so |A_<| = #(S ∩ [c − m, c)) − |D ∖ A|. Equivalently
  |A_<| = |A| − #(gaps in [c − m, c)).
- Hence Wilf holds whenever Σsupp − Dep ≤ (d+1)|A_<|.

**Proof.**
- (i) Write w(t) − c = r(t) − m·μ_t. If w(t) ≥ c, then w(t) < c + m, so r(t) = w(t) − c and μ_t = 0. If w(t) < c,
  then r(t) = w(t) − c + m⌈(c − w(t))/m⌉.
  - So Σ_{(x,b)}(w(t_b x) − c) = Σ_{(x,b)} r(t_b x) − mΣ_t om(t)μ_t.
  - By SUPP-WILF steps 3–5, Σ_{(x,b)} r(t_b x) = (d+1)M′ + m(κ₀ − N).
  - Insert both into CH′.
  - The formula for ℓ counts, for each residue, the elements w(x) + jm < c.
- (ii) Non-maximal tops have w(t) < c (step 2), so μ_t ≥ 1 and Σ_{t∉A} om(t)μ_t ≥ Dep. Maximal y ∈ A_< have
  om(y) = |y| + d and μ_y ≥ 1. Finally N ≥ 0 and κ₀ ≤ Σsupp.
- (iii) If x + e_b ∈ D then w(x) ≤ c + m − 1 − g_b < c. Each residue class with w < c meets [c − m, c) exactly once.
  ∎

**Use for the chain.**
- Case B now only has to pay its margin μ = Σsupp − Dep from the maximal Apéry elements below the conductor.
- On every height-3 case-B semigroup found so far (99 S: the 24 μ-maximizing realizations, the small-lift ones with
  lifts in {2,3} and {3,4}, the min-W one), |A_<| ≥ 18 while μ ≤ 2 (E356).
- New candidate for the open link:
  - **CASEB-WINDOW (CONJ):** if the lex tile of S is in case B and has a cell of height ≥ 3, then
    (d+1)|A_<| ≥ Σsupp − Dep.
  - With SUPP-WILF+ and Flat-MaxCL (height ≤ 2), it implies Wilf.
  - It is weaker than L7′ in the regime that matters, and it is a statement about where the maximal Apéry elements
    sit.
- **Why it should hold (sketch, not a proof).** Suppose A_< is small. Then almost all maximal values lie in the top
  window [c, c + m).
  - For maximal pairs e_1 + e_y and e_y + e_z this gives g_z < g_1 + m. So the generators carried by maximal pairs lie
    in one window of width about m.
  - A cubic Apéry cell then has value about 3G against pair values about 2G (G the common generator size). Being
    < c + m forces G < 3m, i.e. lifts ≤ 3.
  - In that finite-lift regime the flat formula W = 2k·k_miss + d(ρ* + 1) − (d+1)κ̃ (equal lifts, NOTEBOOK) controls W.
  - Making this rigorous is the next proof task.

## Split certificates: the exact identity SPLIT, Theorem CERT, FLAT-U (new proof of L5), H3-HALL, and the unit-capacity obstruction — PROVED 2026-10-20 (paper; checks E360)
**Setting.**
- S has multiplicity m and minimal generators g_1, …, g_d other than m; e = d + 1; c = qm − ρ with q = ⌈c/m⌉ and
  0 ≤ ρ < m.
- D is any factorization tile: a down-set with x ↦ w(x) = x·g a bijection onto Ap(S, m).
- μ_x = ⌈(c − w(x))/m⌉⁺ and r_x = ⟨w(x) − c⟩. Then w(x) = c + r_x − mμ_x, ℓ = Σ_D μ_x, μ_0 = q and r_0 = ρ.
- r is a bijection D → [0, m). Write W_ρ = {z ∈ D : r_z ≥ m − ρ}; it has exactly ρ cells.

**Lemma K (exact Kunz relation).** Let z = x_1 + … + x_k with every x_i ∈ D ∖ {0} and k ≥ 2. Then
    Σ_i μ_{x_i} = (k − 1)q + μ_z + τ,   τ = (Σ_i r_{x_i} − r_z − (k−1)ρ)/m ∈ ℤ,   τ ≥ −⌊(r_z + (k−1)ρ)/m⌋.
For k = 2: τ ∈ {−1, 0, 1}, and τ = −1 forces z ∈ W_ρ.
- Proof: substitute w = c + r − mμ into w(z) = Σ w(x_i). The bounds follow from 0 ≤ r, ρ ≤ m − 1. ∎

**Identity SPLIT (exact, any weights).** Take a finite family of splits s, each s = (z_s; x_{s,1}, …, x_{s,k_s}) as in Lemma K,
and weights π_s ≥ 0. Put
- L_x = Σ_s π_s·#{i : x_{s,i} = x} (load);
- β_z = Σ_{s : z_s = z} π_s;
- Γ = Σ_s (k_s − 1)π_s − (m − e).
Then
    W = qΓ + ρ + Σ_s π_s τ_s + Σ_{x ∈ D∖{0}} (e + β_x − L_x)·μ_x.
- Proof: W = eℓ − c = e(q + Σ_{x≠0} μ_x) − qm + ρ. By Lemma K,
  Σ_x L_x μ_x = Σ_s π_s Σ_i μ_{x_{s,i}} = qΣ_s(k_s − 1)π_s + Σ_z β_z μ_z + Σ_s π_s τ_s. ∎

**Theorem CERT.** Suppose weights satisfy
- (i) L_x ≤ e + β_x for every x ≠ 0, and
- (ii) T := qΓ + ρ − Σ_s π_s ⌊(r_{z_s} + (k_s − 1)ρ)/m⌋ ≥ 0.

Then W ≥ T ≥ 0.
- Every part of a split lies below c, since w(x) = w(z) − w(y) < c + m − m. ∎

**Corollary FLAT-U (a short proof of chain link L5).** Suppose every Apéry element is 0, a minimal generator, or a sum of
two minimal generators, and choose D of height ≤ 2 with pair cells P. Then
    W = (e + 1)·Σ_{p∈P} μ_p + Σ_b (e − deg b)·μ_b + (ρ + Σ_{p∈P} τ_p) ≥ 0,
where deg b = Σ_{p∈P} p_b ≤ (d − 1) + 2 = e, and at most ρ pairs have τ_p = −1.
- Proof: split every pair e_a + e_b once into (e_a, e_b).
  - Then Γ = |P| − (m − e) = 0, L_{e_b} = deg b ≤ e, L_p = 0 and β_p = 1.
  - A pair with τ_p = −1 lies in W_ρ, so ρ + Σ τ_p ≥ 0. ∎
- This replaces MaxCL ⇒ Tile-TOP'' ⇒ Wilf (LEAN `wilf_of_apery_height_le_two`) by an argument using only the classes of
  0, the generators and the pairs.
- It is the Flat-MaxCL mechanism (wrap events confined to a window of ρ residues) in level form.
- Equality: ⟨13,14,16,18,19⟩ has W = 4 = Σ_b(e − deg b)μ_b.
- Checks (flatu.py, E360): the identity is exact on all 824 flat S among 3,000 random S; Lemma K holds on all 129,471
  binary splits of all 3,000 tiles.

**Corollary H3-HALL.** Let D have height ≤ 3, with pairs P and cubics R. Suppose there is a map φ: R → [d] with
φ(t) ∈ supp t and #φ⁻¹(b) ≤ e − deg_P(b) for every b. Then W ≥ 0.
- Note: e − deg_P(b) = (missing mixed pairs at b) + 2·[2e_b ∉ D].
- Proof: split pairs as in FLAT-U, and each cubic t as (e_{φ(t)}, t − e_{φ(t)}).
  - Then Γ = 0, unit loads are deg_P(b) + #φ⁻¹(b) ≤ e, and pair loads are ≤ d < e + 1.
  - Σ_s π_s·wloss ≤ #(W_ρ ∩ split cells) ≤ ρ. ∎
- By Hall's theorem, the condition is: for every set B of units, #{t ∈ R : supp t ⊆ B} ≤ Σ_{b∈B}(e − deg_P(b)).

**Obstruction (PROVED): certificates need m ≤ e² + ρ/q at height ≤ 3.**
- Every split of a cell of height ≤ 3 into k parts has at least k − 1 unit parts. Units have β = 0, so (i) gives
  L_b ≤ e.
- Hence Σ_s (k_s − 1)π_s ≤ Σ_b L_b ≤ ed, and Γ ≤ e(e − 1) − (m − e) = e² − m.
- With (ii), qΓ + ρ ≥ 0 forces m ≤ e² + ρ/q.
- Witness, open regime: S = ⟨37, 75, 78, 80, 88, 89⟩ (residues {1,4,6,14,15}, a postage-stamp B₃ basis; c = 222 = 6m,
  e = 6, m = 37 > e² = 36, W = 102). Its best Γ is −1, so there is no certificate (also with ternary splits).
- So **"every S with e ≥ 3 has a certificate" (CONJ SPLIT-CERT, stated and tested the same evening) is FALSE**
  (FAILED Pattern C).

**Unit-aware certificates (PROVED bound; existence CONJ).**
- Keep the unit levels μ_b exact, i.e. use the generator sizes.
- Overloading a cell x of height ≥ 2 costs at most ū_x = (Σ_b x_b μ_b − (|x| − 1)(q − 1))⁺ ≥ μ_x. This comes from Lemma K
  for the |x|-ary split of x into units.
- Then W ≥ qΓ + ρ − Σ_s π_s·wloss_s + Σ_b (e − L_b)μ_b − Σ_{|x|≥2} (L_x − e − β_x)⁺ ū_x.
- With π = 0 this is the unit truncation U (NOTEBOOK 2026-10-20), so it contains both U and Theorem CERT.
- **CONJ UNIT-CERT:** every S with e ≥ 3 has weights making this bound ≥ 0. Evidence (E360):
  - all 1,800 random S with e ≥ 3;
  - all 600 mixed-lift S on the postage-stamp residues mod 37 and 40;
  - the six certificate-free S above, where the bound often equals W exactly.
  Gating status: necessity audit pending, since UNIT-CERT is close to the exact identity.

**Where this leaves the programme.**
- Certificates without any μ information exist for every tested S with e ≥ 3 outside one regime: height-3 tiles with
  m > e², the near-B₃ simplices.
- That residual is the h-regular / REG-WILF regime, where generators have nearly equal levels. There the unit levels
  (CENTROID / REG-BND averaging) must enter.

## Signed certificates and the Kunz-face relaxations R ≤ RT ≤ UA ≤ AM ≤ W (RT ≤ FX ≤ W) — 2026-10-20 (late night; checks E362–E367)
**Setting.** As in "Split certificates", but over residues. A pair {i, j} of nonzero residues with s = i + j mod m ≠ 0 is
TIGHT if w_i + w_j = w_s. Every split of a cell of any factorization tile is a tight pair, but with several
factorizations there can be more tight pairs. Lemma K holds verbatim for every tight pair:
μ_i + μ_j = q + μ_s + τ with τ ∈ {−1, 0, 1}, and τ = −1 forces ε_s := [r_s ≥ m − ρ] = 1. For a non-tight pair,
w_i + w_j = w_s + Jm with J ≥ 1 and μ_i + μ_j − μ_s = q − J + τ. Both are asserted in src/scratch/p36/kunz_face.py.

**Theorem CERT± (PROVED).** Let π_p ∈ ℝ (either sign) be weights on tight pairs, with loads
L_x = Σ_p π_p·mult_p(x) and β_x = Σ_{p : s_p = x} π_p. If L_x ≤ e + β_x for every x ≠ 0, then
    W ≥ q·(Σ_p π_p − (m − e)) + ρ − Σ_{π_p > 0} π_p ε_{s_p} − Σ_{π_p < 0} |π_p|.
- Proof: Identity SPLIT is linear in the weights, so it holds for real π:
  W = qΓ + ρ + Σπτ + Σ_x (e + β_x − L_x)μ_x. Here μ ≥ 0 and e + β − L ≥ 0. For π_p > 0 use τ_p ≥ −ε_{s_p}; for π_p < 0
  use τ_p ≤ 1. ∎
- k-ary splits work the same way, with τ ≤ ⌊(Σ r_parts − r_z − (k−1)ρ)/m⌋ ≤ k − 1.
- Negative weights ("anti-splits") move load from the parts to the sum. They cost 1 each and lower Γ by 1.

**Proposition RT-DUAL (PROVED, LP duality).** Let
    RT(S) = min { e(q + Σ_{x≠0} y_x) − qm + ρ :  y ≥ 0,  q − ε_s ≤ y_i + y_j − y_s ≤ q + 1  for every tight pair }.
(a) RT ≤ W, since y = μ is feasible with value W.
(b) RT is the maximum of the CERT± bound over binary weights on all tight pairs. The two constraint families carry
    π⁺ and π⁻, and the dual constraint of y_x is exactly L_x − β_x ≤ e.
(c) Dropping the upper side gives R. R is the maximum over π ≥ 0, i.e. the robust certificate of splitlp.py on all
    tight pairs.
So RT ≥ 0 if and only if a signed binary certificate exists.
- Further relaxations, all lower bounds for W (kunz_face.py):
  - UA = RT + (y_g = μ_g on minimal generators);
  - AM = UA + Apéry minimality on non-tight pairs (y_i + y_j − y_s ≤ q − 1 + τ);
  - FX = the exact face at fixed q: tight pairs y_i + y_j − y_s = q + τ, non-tight ≤ q − 1 + τ.
- Order: R ≤ RT ≤ UA ≤ AM ≤ W and RT ≤ FX ≤ W. FX ⊂ RT because τ = −1 only where ε = 1.

**Proposition R-FAKE (PROVED): the dual obstruction of one-sided certificates.** If every Apéry element is a sum of at
most 3 minimal generators, then y = q·1_{minimal generators} is R-feasible, so R ≤ q(e² − m) + ρ.
- Proof: a tight pair with two non-generator parts sums to an element of height ≥ 4, so none exists.
  - Two generator parts: y_i + y_j − y_s = 2q ≥ q.
  - One generator part: q − 0 − 0 ≥ q − ε.
  - Value: e(q + (e−1)q) − qm + ρ. ∎
- This is the primal side of the proved obstruction m ≤ e² + ρ/q. RT cuts it whenever q ≥ 2, since 2q > q + 1.

**Proposition RT-ASYM (PROVED).** Fix the tight graph, ρ and ε, and treat q as a real parameter.
- Then q ↦ RT(q) is convex and piecewise linear. It is a maximum of affine functions over the q-independent dual
  polytope.
- Its final slope is
    lead = max_dual Γ = min { e(1 + Σ_x v_x) − m : v ≥ 0, v_i + v_j − v_s = 1 on tight pairs }.
- RT(q) ≥ q·lead − K∞ for every q, where K∞ = min{Σπ⁺ε + Σπ⁻ − ρ : Γ = lead}.
- lead ≥ 0: write v = 1 − u. Then u is additive on tight pairs, hence linear on any tile (u(z) = z·σ), and u ≤ 1.
  The column identity (CH′ for a linear functional) gives (d+1)Σ_D u ≤ dm, i.e. eΣu ≤ (e−1)m. ∎
- So the leading order of RT is the continuous Wilf / CH′ depth term. The discrete part is what the q-multiplier pays.
- FALSE shortcut (ASYM-RT, FAILED Pattern C): K∞ ≤ q·lead is not generally true at q = 5.
  ⟨13,17,27,29⟩ (c = 63, open regime) has lead 5.5 and K∞ 34.5 (asymptote −7), while RT = 9 via another dual (E366).

**Proposition Γ-CAP3 and the exchange law (PROVED).** Let D be a factorization tile of height ≤ 3, with d units, pairs P
and cubics C, so m = 1 + d + |P| + |C|. Take any CERT± certificate supported on tile splits:
- weights π_p on the pair splits;
- λ ≥ 0 on the cubic splits. Signed cubic weights only add cost; the cubic constraints are slack.
Then
    (i)  Γ ≤ e(|P| + 2d + 3)/3 − m        (= C(d+3,3) − m = #missing cubics M₃ when every pair is present),
    (ii) Σ_{π_p<0} |π_p| ≥ −Σ_p π_p ≥ Γ − (e² − m),
    (iii) hence the certificate value is ≤ (q − 1)Γ + ρ − (m − e²).
- Proof. Write Λ = Σλ and Π = Σπ_p.
  - Summing the pair constraints Σ_b λ_{p,b} − π_p ≤ e gives Λ − Π ≤ e|P|.
  - Summing the unit constraints Σλ(b) + Σ_p p_b π_p ≤ e gives Λ + 2Π ≤ ed.
  - Γ = Λ + Π − (m − e). Then (1/3)(Λ − Π) + (2/3)(Λ + 2Π) = Λ + Π ≤ e(|P| + 2d)/3, which gives (i).
  - The unit sum gives −Π ≥ Λ + Π − ed = Γ + m − e − ed = Γ + m − e², which gives (ii). ∎
- With π ≥ 0, (ii) is the old obstruction Γ ≤ e² − m. In general every unit of Γ beyond e² − m must be bought with one
  unit of anti-split mass.
- Necessary condition for a tile-split certificate: (q − 1)·Γ_cap + ρ ≥ m − e².
  - With all pairs present, m ≈ θ·C(d+3,3) and Γ_cap = (1 − θ)C(d+3,3), this reads θ ≲ (q−1)/q, which is 4/5 at q = 5.
  - So at height 3, signed certificates reduce to a THIN-BASIS question (CONJ THIN3 below).
- Observed (E364, E367): the LP lead equals the cap (i) exactly:
  - ⟨37,75,78,80,88,89⟩: |P| = 14, d = 5, lead 17;
  - every full-pair cover tested: lead = M₃ = 5, 11, 16, 18, 29 for d = 3, 4, 5, 5, 6.
- The optimal dual there is the "anti-split pairs, over-split cubics" pattern:
  - every pair weight negative, total −e(|P| − d)/3, which is −C(e,3) with all pairs;
  - cubic weight total e(2|P| + d)/3;
  - units and pairs saturated.

**CONJ RT-NONNEG.** Every S with e ≥ 3 and c > 4m has RT(S) ≥ 0.
- With the kernel-checked depth-four theorem (c ≤ 4m), RT-NONNEG implies Wilf.
- e = 2 is excluded: there W = 0 and RT < 0 occurs.
- It is level-free except for q, ρ and the window ε. It is stronger than UNIT-CERT, since UA ≥ RT.
- Gating:
  - Necessity audit: RT-NONNEG is sufficient and not necessary for Wilf. A failure would only kill this route.
  - Falsification attempts (E362–E367), with 0 negatives among e ≥ 3:
    - exact MILP minima of RT over genuine S (m ≤ 15, all r);
    - annealing over residues and lifts;
    - random S;
    - the negative-Eliahou families, where RT = W exactly, including m = 798;
    - Delgado S(p), Backelin, the T1 counterexamples;
    - the extremal full-pair height-3 covers for d = 3–6.
  - Smallest values: RT = 1 at ⟨8,11,23⟩ (c = 38 > 4m, but 3e > m); in the open regime RT = 5 at ⟨13,17,20⟩ (c = 76).
- Proof deadline: 2026-10-22. Either prove the height-3 case (via THIN3 + the Γ-CAP3 dual), or downgrade.

**CONJ THIN3 (additive combinatorics; what height 3 needs).**
- Statement: let s_1, …, s_d ∈ ℤ/m (d ≥ 2) have {0} ∪ {s_a} ∪ {s_a + s_b} pairwise distinct (a "Sidon set with 0"), and
  let every residue be a sum of at most 3 of the s_a. Then m ≤ θ·C(d+3,3) with θ ≤ 4/5.
- Exhaustive maxima (nearcov.c): m_max = 15, 24, 40 for d = 3, 4, 5, so θ = 0.750, 0.686, 0.714. For d = 6 the largest
  found is 55 (θ = 0.655), with the scan incomplete above 58.
- Δ_h itself never tiles (simptile.py: d = 2–4, h = 2–4, m ≤ 60).
- No external bound of this strength was found (LITERATURE search 2026-10-20 late night).

**Proposition H3-UNIF (PROVED): the explicit signed certificate for full-pair height-3 tiles, and its sharpness.**
Let D have height ≤ 3 and contain every pair, so deg_P(b) = e for every unit. Let λ_{z,c} ≥ 0 be weights on the cubic
splits (z = p + e_c), with Λ_z = Σ_c λ_{z,c}, X_p = Σ_c λ_{p+e_c, c}, and let s_p ≥ 0 be extra pair weights. Suppose
    (U) Σ_{z∈C} z_b Λ_z + Σ_p p_b s_p ≤ e(e+1) for every unit b,      (N) X_p + s_p ≤ e for every pair p.
Then
    W ≥ (2q+1)·ΣΛ − Σ_{z∈C∩W_ρ} Λ_z + (q+1)·Σs − (q+1)e|P| − q(m − e) + ρ.
- Proof: CERT± with π_p = X_p − e + s_p ≤ 0 on the pair splits and λ on the cubic splits.
  - Pair load X_p − π_p = e − s_p ≤ e.
  - Unit load Σ_z λ_{z,b} + Σ_p p_b π_p = Σ_z z_b Λ_z − e·deg_P(b) + Σ_p p_b s_p ≤ e by (U). This uses
    Σ_z λ_{z,b} + Σ_p p_b X_p = Σ_z z_b Λ_z.
  - Γ = 2ΣΛ + Σs − e|P| − (m − e) and cost = (e|P| − ΣΛ − Σs) + Σ_{C∩W_ρ} Λ_z. ∎
- Regular case: (U) is an equality with s = 0 (the all-e(e+1) vector lies in cone(C), e.g. every pure cube present).
  Then ΣΛ = de(e+1)/3 and
    W ≥ q·M₃ − C(e,3) + ρ − Σ_{z∈C∩W_ρ} Λ_z,       M₃ = C(d+3,3) − m (missing cubics).
  - Arithmetic: C(d+3,3) − C(d+1,3) = (d+1)² = e², so q·M₃ − C(e,3) = (q−1)M₃ + e² − m. So with no W_ρ cubics, this
    attains the Γ-CAP3 upper bound (iii) exactly.
  - So, when tight pairs = tile splits, it is the optimal tile-split certificate up to the W_ρ term.
- **Consequence (risk for RT-NONNEG).** In the worst window ρ = m − 2 (every cubic in W_ρ) with q = 5, the regular
  value is 20C(d+2,3) − 6eC(d+1,2) + 5d + 3 − 4m. This is ≥ 0 iff m ≤ m*(d) with
    θ*(d) = m*/C(d+3,3) = 0.806, 0.779, 0.756, 0.719, 0.692, 0.661 at d = 6, 7, 8, 10, 12, 15, and → 1/2 as d → ∞.
  - So RT-NONNEG at height 3 needs the full-pair cover density θ_d to stay below θ*(d). Data: θ_d = 0.75, 0.686,
    0.714, 0.655 for d = 3–6, and ≥ 0.642 for d = 7 (hill-climb, E368). The gap θ* − θ_d is 0.15 (d = 6) and 0.14
    (d = 7).
  - The exact semigroup is safe in the same window: with g_b ∈ (m, 2m) and c ≈ 4m, μ_b = 3 and μ_p ≥ 1, so
    eℓ ≳ d³/2 against c ≈ (2/3)θd³.
  - The level-free relaxation is the weak point. Its unit-aware version UA (y_g = μ_g) keeps more of the margin. On the
    two d = 6, m = 55, ρ ≈ 50 minimizers (E367): R/RT/UA/W = −15/55/90/167 and −7/63/98/147.

**Proposition TX (PROVED): the exact-τ signed certificate is Wilf's real-perturbation shadow.** Let
TX = min{e(q + Σy) − qm + ρ : y ≥ 0, y_i + y_j − y_s = q + τ_ij on tight pairs}. Here τ_ij = (r_i + r_j − r_s − ρ)/m and
r_x = (x − r − 1) mod m, so τ depends only on residues and the conductor residue r.
- (a) By LP duality, TX = max over real split weights of qΓ + ρ + Σ_p π_p τ_p subject to L_x ≤ e + β_x. This is Identity
  SPLIT with the μ-terms dropped and τ exact.
- (b) Fix a tile D and put Z = Σ_{z∈D} z. Let V = {σ ∈ ℝ^d : σ·(x + y − z) = 0 for every tight pair, in factorization
  coordinates}. Then
    TX = W − e·max{σ·Z : σ ∈ V, z·σ ≤ μ_z for all z ∈ D}.
  - Proof: feasible y are exactly μ + h with h additive on the tight graph, i.e. h(z) = z·σ with σ ∈ V. Then
    Σ_{x≠0} y_x = (ℓ − q) − σ·Z after σ ↦ −σ. ∎
- (c) Corollary (Farkas): TX = W iff Z lies in the cone generated by the cells with μ_z = 0, i.e. the Apéry elements
  ≥ c, modulo V⊥.
- Hence TX = W generically:
  - E367/E362 lists: TX = FX = W on ⟨37,75,…⟩, both d = 6 covers and the Fromentin S;
  - TX < W only when the top band fails to span Z, e.g. ⟨13,17,20⟩ 18.5 vs 29 and ⟨13,17,27,29⟩ 31 vs 41.
- "TX ≥ 0" is therefore NOT a reduction of Wilf. It is Wilf for real level perturbations.
- The genuine relaxations are RT (level-free) and UA (RT + generator levels).
- Ranking of single-lemma candidates for "split identity + one lemma ⇒ Wilf":
  - RT-NONNEG: strongest and cheapest; at risk only via THIN3 at large d.
  - Then UA-NONNEG.
  - Then TX-NONNEG, which is essentially Wilf.

### RT barriers are real; the one-cell upper window RT2; the exact UA dual (2026-10-21)
**Lemma τ-WINDOW (PROVED).** Every tight pair (i, j → s) satisfies:
- τ = −1 ⟹ r_s ≥ m − ρ (s ∈ W_ρ; this was already used in RT);
- τ = +1 ⟹ r_s ≤ m − ρ − 2.
- Proof: τ = (r_i + r_j − r_s − ρ)/m with 0 ≤ r_i, r_j ≤ m − 1. τ = −1 needs r_i + r_j = r_s + ρ − m ≥ 0. τ = +1 needs
  r_i + r_j = m + ρ + r_s ≤ 2m − 2. ∎
- So each tight relation is determined up to one unit by the position of its sum cell alone:
  - τ ∈ {−1, 0} on W_ρ;
  - τ = 0 at r_s = m − ρ − 1;
  - τ ∈ {0, 1} for r_s ≤ m − ρ − 2.
- Positions depend only on the residue and the conductor residue r (r_s = (s − r − 1) mod m), so this is level-free.
- Define ε⁺_s = [r_s ≤ m − ρ − 2] and
    RT2 = min{e(q + Σy) − qm + ρ : y ≥ 0, q − ε_s ≤ y_i + y_j − y_s ≤ q + ε⁺_s on tight pairs}.
  Then R ≤ RT ≤ RT2 ≤ UA2 ≤ W and RT2 ≤ TX.
- Its dual is CERT± with the anti-split cost refined to ε⁺_{s_p}: anti-splitting into a cell with r_s ≥ m − ρ − 1 is free.
- UA2 = RT2 + (y_g = μ_g on generators).

**Proposition FAKE3 (PROVED): explicit primal fakes, hence upper bounds for EVERY signed certificate.**
- Weak duality: a feasible y bounds every certificate, whatever the signs of the pair and cubic weights. This covers the
  advisor's point about signed cubic weights.
- Hypothesis H (graded height ≤ 3):
  - every Apéry element is a sum of ≤ 3 minimal generators;
  - all factorizations of each Apéry element have the same length h(s);
  - hence every tight pair has h(i) + h(j) = h(s).
  - Unique factorization is NOT required. Write P, C for the height-2 and height-3 elements; d = e − 1.
- (a) BASE: y = (2q+1)/3 on generators, (q−1)/3 on P, 0 on C is RT-feasible. Hence
    RT ≤ e(q + (2q+1)d/3 + (q−1)|P|/3) − qm + ρ = (q − 1)Γ_cap + ρ − (m − e²),   Γ_cap = e(|P| + 2d + 3)/3 − m.
  - It is RT2-feasible as soon as ε⁺_p = 1 for every p ∈ P.
  - Check: generator pairs give 2u − v = q + 1; (p, generator) pairs give u + v = q.
- (b) WINDOW (q ≥ 3): y = 2q/3 on generators, q/3 − δ_p on p ∈ P, 0 on C is RT-feasible.
  - Here δ_p = 1 iff every height-3 element above p lies in W_ρ (vacuously if there is none).
  - Hence RT ≤ e(q + 2qd/3 + Σ_p (q/3 − δ_p)) − qm + ρ.
  - It is NOT RT2-feasible once some p has δ_p = 1 and ε⁺_p = 0, since it needs τ_p = +1.
- (c) RT2-WINDOW (q ≥ 2): if every element of P ∪ C lies in W_ρ, then y = (2q−1)/3 on generators, (q−2)/3 on P, 0 on C
  is RT2-feasible (2u − v = q, u + v = q − 1). Hence
    RT2 ≤ (q − 1)Γ_cap + ρ − (m − e²) − e(2d + |P|)/3.
  - Proof by the two displayed constraint checks. No tested S yet has all of P ∪ C in W_ρ, so (c) has not been checked
    against an instance.
- Attained (rtobs3.py, E369):
  - RT = BASE on ⟨37,75,78,80,88,89⟩ (84) and ⟨16,17,20,21⟩ (5.333);
  - RT = WINDOW on the two d = 6 cover minimizers (55, 63);
  - RT = min(BASE, WINDOW) on 22 of the 33 graded height-3 S among 326 d = 6 cover semigroups.
- **So the RT barriers are genuine, not artefacts of H3-UNIF:**
  - small window: θ ≲ 4/5 at q = 5;
  - full window: θ → 1/2 (H3-UNIF and (b) coincide there).
  - An S with graded height 3, q = 5, all of P ∪ C in W_ρ, and density above θ*(d) would make RT < 0. No such S is
    known; the densest covers have θ_d = 0.655, ≥ 0.642, ≥ 0.612 for d = 6, 7, 8.
- **RT2 removes the full-window fake.** Its full-window bound (c) needs only θ ≲ 3/4 asymptotically. At ρ = m − 2, q = 5
  the threshold is m ≤ (4T + e² − 2 − e(2d + C(d+1,2))/3)/4 with T = C(d+3,3): θ ≤ 0.911, 0.896, 0.864, 0.815 for
  d = 6, 7, 10, 20.
  - The small-window base barrier (a) still applies to RT2: θ ≲ 4/5, exactly 5m ≤ 4T + e² + ρ at q = 5.
  - Observed on 326 d = 6 cover S: min RT 55, min RT2 = min UA = min UA2 = 90. RT2 ≥ UA on 237 of them.

**Proposition UA-DUAL (PROVED, LP duality).**
    UA = max_π  qΓ(π) + ρ − Σ_{π_p>0} π_p ε_{s_p} − Σ_{π_p<0} |π_p| + Σ_{g generator} (e − L_g(π))·μ_g
subject to L_x − β_x ≤ e for every NON-generator x. UA2 is the same with anti-split cost ε⁺_{s_p}.
- Generators are priced at μ_g instead of capped at load e.
- π = 0 gives exactly the unit truncation U = e(q + Σ_g μ_g) − c. So UA contains both U and RT.
- The window fake (b) is UA-feasible iff μ_g = 2q/3 for every generator. Generator sizes alone therefore do not exclude
  it in that case; τ-WINDOW does.
- Comparison for the target choice:
  - RT2 is level-free, with explicit fakes and duals. Its height-3 barrier is θ ≲ 3/4 (full window) and 4/5 (small
    window).
  - UA2 = RT2 + generator levels is weaker as a claim and has larger margins, e.g. d = 7: RT2 175, UA2 191. A uniform
    proof of it needs control of the generator levels.

**CONJ RT2-NONNEG** (supersedes RT-NONNEG as the level-free target): e ≥ 3 and c > 4m ⇒ RT2 ≥ 0.
- Fallback: CONJ UA2-NONNEG.
- RT-NONNEG is kept but deprioritized: its full-window barrier is proved (FAKE3(b)), and only the cover densities keep
  it alive.

### Exact τ formula, part types (RT3), corrections, and the two-mechanism picture (2026-10-21, later)
**Lemma τ-FORMULA (PROVED).** Let r be the conductor residue (w_r = max Ap). For a pair of nonzero residues i, j with
s = i + j mod m ≠ 0,
    τ_ij = [i + j > m] + [s > r] − [i > r] − [j > r],     and r_x < ρ ⟺ x > r  (r_x = ρ only for x = 0).
- Proof: μ_x = k_r − k_x − [x > r] for x ≠ 0, and the Kunz relation k_i + k_j + [i+j>m] = k_s + J give
  μ_i + μ_j − μ_s = q − J + ([i+j>m] + [s>r] − [i>r] − [j>r]).
- Positions: r_x = (x + ρ) mod m, since c ≡ −ρ. So r_x < ρ iff x + ρ ≥ m iff x > r = m − ρ − 1. ∎
- Asserted on every tight pair by rtexact.py.

**Lemma TYPE (PROVED).** τ = −1 forces both parts LOW (r_i, r_j < ρ, i.e. i, j > r). τ = +1 forces both parts HIGH
(r_i, r_j > ρ, i.e. i, j ≤ r).
- Proof: τ = −1 needs r_i + r_j = r_s + ρ − m ≤ ρ − 1. τ = +1 needs r_i + r_j = m + ρ + r_s ≥ m + ρ. ∎
- RT3 = RT2 with the lower allowance ε only on LL relations and the upper allowance ε⁺ only on HH relations. UA3 =
  RT3 + generator levels. So R ≤ RT ≤ RT2 ≤ RT3 ≤ TX ≤ W and RT3 ≤ UA3 ≤ W.
- RT3's dual is CERT± with costs only on monochromatic relations: positive weights on LL relations into W_ρ, negative
  weights on HH relations into low cells. The coloring is x ↦ [x > r].

**Correction to "RT2 removes the full-window fake".** The 3/4 threshold applies only when all of P ∪ C lies in W_ρ.
- FAKE3(b) is RT2-feasible whenever every height-2 element with δ_p = 1 has a low position (ε⁺_p = 1).
- RT2 attains it on 14 of 33 graded d = 6 cover S and 3 of 7 at d = 7. Certified exactly: ⟨55,71,78,79,93,97,99⟩,
  RT2 = 137 = (b).
- So in the configuration "pairs low, cubics in the window", RT2 has the same barrier θ*(d) → 1/2 as RT.
- Lemma TYPE kills (b) there. (b) needs τ = +1 on generator pairs (both generators HIGH) and τ = −1 on the cubic splits
  above them (the generator part LOW). A generator in both is impossible.
- Effect: RT3 = 172 vs RT2 = 137 on that S; 111 vs 90 on ⟨55,76,77,81,83,91,94⟩.

**Correction to Proposition TX ("TX = W generically").** This held on the tested shallow S (q ≤ 6). Deep S have TX ≪ W,
because the real level perturbation of Proposition TX(b) is large there. Certified exactly (rtexact.py):
- ⟨25,26,60,80,90,95⟩ (q = 7): TX = 35, UA = 221, W = 245;
- ⟨25,59,60,76,93,102⟩ (q = 13): TX = 116, UA3 = 546 = W;
- ⟨30,35,68,73⟩ (q = 10): TX = 118, UA3 = 110, W = 218.
So TX is not "Wilf in disguise" at depth. It ignores the generator levels, which block those perturbations.

**Two mechanisms (observed, E371).**
- (i) Shallow S (q = 5–6, near-simplex tiles, heights 3–5): the missing information is positional (part types / exact τ).
  - ⟨20,23,39,45⟩: RT2 21 → RT3 59;
  - ⟨15,21,29,32⟩: RT2 7 → RT3 29 = W;
  - ⟨13,17,27,36⟩: RT2 12 → RT3 20 = W.
- (ii) Deep S (q ≥ 7): positional information is exhausted (RT2 = RT3 = TX) and only the generator levels close the gap
  (UA ≈ W).
- UA3 combines both: min UA3/W ≈ 0.50 on the m = 20–30 annealing set, against RT2/W 0.132 and UA2/W 0.296.

**Height-3 status (exact).**
- (1) Exact reduction (PROVED). Under H (graded height ≤ 3), substitute y = 2q/3 + α (generators), q/3 + β (height 2),
  γ (height 3). Then
    RT2 = q·Γ_cap + ρ − e·K_q,   K_q = −min{Σα + Σβ + Σγ : α_a + α_b − β_p ∈ [−ε_p, ε⁺_p] (A),
          β_p + α_c − γ_z ∈ [−ε_z, ε⁺_z] (B), α ≥ −2q/3, β ≥ −q/3, γ ≥ 0}.
  - K_q ≥ 0 (α = β = γ = 0 is feasible) and is nondecreasing in q. So RT2 ≤ qΓ_cap + ρ, and RT2 ≥ 0 ⟺ e·K_q ≤
    qΓ_cap + ρ.
  - The same holds for RT and RT3 with their intervals.
- (2) Conditional theorem (PROVED, an instance of CERT± with RT2 costs). With all pairs present, unique factorization
  and a regular cubic weighting (H3-UNIF):
    W ≥ RT2 ≥ q·M₃ + ρ − Σ_{p: r_p ≤ m−ρ−2} (e − X_p) − Σ_{z ∈ C∩W_ρ} Λ_z.
- (3) Barriers (PROVED): FAKE3(a), (b), (c).
- (4) What needs a packing theorem: for RT2, θ_d ≤ θ*(d) (→ 1/2) in the configuration of (b); unproved. For RT3, (b) is
  excluded, and its own height-3 barrier is not yet derived. No unconditional height-3 theorem yet.

### Height 3 under part types: what TYPE removes, what survives, the typed H3-UNIF certificate (2026-10-21, later)
Setting: hypothesis H (graded height ≤ 3); HIGH/LOW as in Lemma TYPE (x HIGH ⟺ 1 ≤ x ≤ r ⟺ r_x > ρ).

**Proposition FAKE3(d) (PROVED): the TYPE-respecting window fake.** Let q ≥ 3. Let Δ ⊆ P be the height-2 elements p
such that:
- every factorization p = a + b has a and b HIGH;
- ε⁺_p = 1 and p is LOW;
- every tight pair (p, c → z) has c LOW and z ∈ W_ρ.
Then y = 2q/3 on generators, q/3 − [p ∈ Δ] on P and 0 on C is RT3-feasible. Hence RT3 ≤ q·Γ_cap + ρ − e|Δ|.
- Proof: the gen-pair relations into p ∈ Δ need the upper allowance (HH, ε⁺_p = 1). The relations (p, c → z) with
  p ∈ Δ need the lower allowance (p, c LOW, z ∈ W_ρ). Every other relation has value exactly q. ∎
- Counting (PROVED): let h = #HIGH generators. Then |Δ| ≤ C(h+1, 2).
  - If an all-HIGH cubic a + b + a′ is an Apéry element, then its split (a+b, a′) has a HIGH part. So a + b ∉ Δ.
  - Hence each p ∈ Δ forces h missing all-HIGH 3-multisets, and each multiset is counted ≤ 3 times. So
    h·|Δ| ≤ 3·#(missing all-HIGH cubic multisets).
- Compared with (b): in RT and RT2, δ_p = 1 for EVERY pair whose cubics all lie in W_ρ. Under RT3 only these HH pairs
  with LOW complements remain.
- Observed (rt3cov.py, E372): |Δ| ≤ 2 on all 568 graded height-3 cover S (d = 3–7). RT3 = FAKE3(d) on 359 of them.

**Proposition BASE-SURVIVES (PROVED): the small-window barrier is untouched by TYPE.** FAKE3(a) is RT3-feasible iff
every generator occurring in a height-2 factorization is HIGH and every p ∈ P has ε⁺_p = 1.
- Under full pairs this means: all generators HIGH and all pairs at positions ≤ m − ρ − 2.
- Then RT3 ≤ (q − 1)Γ_cap + ρ − (m − e²).
- Proof: FAKE3(a) uses the upper allowance only on gen-gen relations; all its (pair, gen) relations are exact. ∎
- Attained: on dense d = 6 covers (m = 55, levels (2,1,1,1,1,1), q = 5, ρ = 1, all 6 generators HIGH),
  RT2 = RT3 = BASE = 111, while W = 272 or 286 and UA3 = 195.
- Consequence: for every level-free relaxation RT ⊆ RT2 ⊆ RT3, the height-3 barrier at q = 5 is
  5m ≤ 4T + e² + ρ, i.e. θ ≲ 4/5, the CONJ THIN3 threshold.
  - The TYPE rule moves the RT3 window barrier from θ → 1/2 (RT, RT2: FAKE3(b)) to the |Δ|-restricted FAKE3(d).
  - So for RT3 the binding level-free height-3 obstruction is the 4/5 packing question, not the 1/2 one.
  - Only generator levels (UA3) can beat BASE if a full-pair cover with θ > 4/5 exists at large d.

**Proposition H3-TYPED (PROVED): H3-UNIF with typed costs.** Under the hypotheses of H3-UNIF (height ≤ 3, every pair
present, tight pairs = tile splits), with λ, s, X, Λ as there and (U), (N) holding,
    W ≥ RT3 ≥ q(2ΣΛ + Σs − e|P| − (m − e)) + ρ − Σ_{(p,c→z): p,c LOW, z∈W_ρ} λ_{z,c}
                                               − Σ_{p=a+b: a,b HIGH, ε⁺_p=1} (e − X_p − s_p).
- Proof: the H3-UNIF weights are a dual-feasible point of RT3. RT3 has the same dual constraints as RT, and only the
  costs change: lo on monochromatic LOW relations into W_ρ, up on monochromatic HIGH relations with ε⁺ = 1. ∎
- Regular case (s = 0, ΣΛ = de(e+1)/3): W ≥ q·M₃ + ρ − Σ_{HH pairs, ε⁺=1}(e − X_p) − Σ_{LL splits into W_ρ} λ_{z,c}.
- Freedom: a window cubic costs nothing if its weight sits on a split with a HIGH part. A pair costs nothing unless both
  its generators are HIGH.
- Sign-pattern test (E372): RT3H, the LP restricted to this pattern, equals RT3 on 430 of 568 graded height-3 cover S.
  - RT3H counts only anti-splits on pair relations and splits on cubic relations. On these S (full pairs, unique pair
    factorizations by the Sidon property, tight pairs = tile splits) its dual is exactly the H3-TYPED family over all
    admissible λ ≥ 0, s ≥ 0.
  - Min RT3H = 16.33 > 0.
  - Largest losses (≈ 30) occur when all generators are LOW and ρ ≈ 48 (m = 55). There the other signs, positive pair
    splits and cubic anti-splits, are free.

**Full-window realizability (E372).** The RT2-WINDOW fake FAKE3(c) needs P ∪ C ⊆ W_ρ.
- Cells outside W_ρ are exactly the residues r+1, …, 2r+1. So the condition is "these r+1 residues are generators".
- Scan: dense covers d = 3–8 and every unit rescaling. Of 389 residue configurations with this property, the lifts with
  levels in {1, 2, 3}, conductor residue r and c > 4m number 4865 (fullwin.py).
- Graded height ≤ 3 occurs only at m = 15, d = 3: ⟨15,32,33,37⟩ (q = 7), ⟨15,32,33,52⟩ (q = 9), ⟨15,47,48,52⟩ (q = 10),
  all with ρ = 13 = m − 2.
- On these three, RT2 = RT3 = FAKE3(c) = 5(q−2) + 3 = 28, 38, 43, exactly certified. So (c) is attained.
- The remaining full-window lifts have height 4–6 and RT2/W ≈ 0.7–0.85.
- No full-window graded S with q = 5 was found. At larger q the (c) bound grows like (q−2)Γ_cap, so the full-window
  regime is not the threat.

**Proposition BASE-FAMILY (PROVED identity; instances CHECKED).** Let S have graded height ≤ 3 with every pair present.
Assume:
- every generator is HIGH with μ_g = (2q+1)/3, so q ≡ 1 (mod 3) and k_g = (q−1)/3;
- every pair relation has τ = +1;
- every cubic has μ_z = 0.
Then μ_p = (q−1)/3 for every pair, and
    W(S) = FAKE3(a) = (q − 1)T − qm + ρ + e²,     T = C(d+3, 3).
So Wilf for S is exactly the packing inequality qm ≤ (q−1)T + e² + ρ.
- Proof: substitute μ into W = e(q + Σμ) − qm + ρ and use e(|P| + 2d + 3)/3 = T for full pairs. ∎
- Instances (basefam.py, E373): the residue sets {5,6,8}, {6,7,10}, {7,9,10} mod 15 (d = 3, θ = 3/4) with uniform levels
  k = 1, 2, 3 (q = 4, 7, 10). Examples: ⟨15,22,24,25⟩, ⟨15,37,39,40⟩, ⟨15,52,54,55⟩ with W = 17, 32, 47.
  - On these, RT = RT2 = RT3 = UA3 = TX = W exactly (rtexact).
  - Among 17770 graded full-pair height-3 lifts of the d = 3–5 covers, there are no other hits.
- Meaning: the BASE barrier of every level-free relaxation is attained by Wilf itself on this family. A height-3 proof
  must therefore contain the packing inequality there. At q = 4 it is a consequence of the kernel-checked depth-4
  theorem; on the checked chains q = 7, 10 reduce to q = 4 by Lemma DESCENT below (W grows by 3M₃ per level).

**Lemma DESCENT (PROVED on paper; CHECKED descent.py).** Let S have multiplicity m and Apéry set w. Let σ ∈ ℤ_{≥0}^{P′}
be such that h(w_s) := σ·n is the same for every factorization n of w_s over P′.
- Equivalently h is additive on tight pairs. Example: σ = 1 (factorization length) when S is graded.
- Write h* = max_s h_s and H = Σ_s h_s.
Let t ≥ 1 be an integer and w′_s = w_s − m·t·h_s. Suppose:
- (a) w′_s > m for s ≠ 0;
- (b) w′_i + w′_j ≥ w′_{(i+j) mod m} for all i, j;
- (c) max_s w′_s is attained at a residue with h_s = h*.
Then w′ is the Apéry set of the numerical semigroup S′ = ⟨m, w′⟩, e(S′) ≤ e(S), and
    W(S) − W(S′) ≥ t·[(e−1)·m·h* − e·H] ≥ 0     (e = e(S)).
Equality holds in the first inequality when e(S′) = e(S) and the argmax residue is unchanged.
- Proof.
  - (a) and (b) are the Kunz inequalities, so w′ = Ap(S′, m). Tight pairs of S stay tight, so the generators of S′
    are among those of S.
  - By Identity CH, m·W = (e−1)mM − eΣw − (e−2)m(m−1)/2 =: m·F_e(w), with M = max w.
  - ∂F_e/∂e = M − Σw/m − (m−1)/2 = c − g ≥ 0. So W(S′) = F_{e(S′)}(w′) ≤ F_e(w′).
  - F_e(w) − F_e(w′) = (e−1)(M − M′) − e·t·H. By (c), M′ = w′_{r′} with h_{r′} = h*, and w_{r′} ≤ M, so
    M − M′ ≥ m·t·h*.
  - The bracket is ≥ 0 by the chain identity applied to the additive functional h, with σ ≥ 0 (CH′, as in RT-ASYM).
    Each p_a-chain contributes |C|·(h* − h(top C)) ≥ 0, and Σ_a σ_a ν_a(w) ≥ h(w). This gives
    (d+1)·H ≤ d·m·h*. ∎
- Corollary (BASE family).
  - Statement: if a BASE-family S with k = (q−1)/3 satisfies (b) for t = k − 1 (σ = 1), then
    W(S) = W(S_{q=4}) + 3(k−1)M₃ ≥ 0 by the depth-4 theorem.
  - (a) holds since k′_g = 1. (c) holds since cubics drop by 3t and pairs by 2t.
  - Checked on the three chains q = 10 → 7 → 4 at m = 15: W = 47 → 32 → 17 with M₃ = 5.
  - Historical gap: (b) was not proved here. For the exact BASE hypotheses it is now proved below in
    "BASE-family deflation: the previously conditional Kunz step is automatic" (2026-10-22).
    The general DESCENT statement still requires (b) outside that profile.
- Scope (CHECKED, E373): among 400 random graded S with c > 4m (m = 10–30, levels 1–5):
  - descent applies (t ≥ 1) to 129;
  - the inequality held in all 129, with equality attained;
  - only 4 landed at c′ ≤ 4m. The usual blocker is (a), a generator at level 1.
- So DESCENT reduces uniformly deep graded S to shallower ones, but not in general.
- Novelty: unchecked. Related framework: BGOW 2020, Wilf on faces of the Kunz polyhedron and the "Wilf game" (LITERATURE
  §2.5); Zhai's CH′. Literature check pending before any claim.

### q = 5, height ≤ 3: the level budget and the level-1 count (2026-10-21, later) [SCOPE: Q5 only; no reduction to all S]
Let q = 5, so c = 5m − ρ = 4m + r + 1 and max Ap = w_r = 5m + r.

**Lemma LEVEL-BUDGET (PROVED).** Every Apéry element w_s = m k_s + s satisfies k_s ≤ 5, and k_s = 5 only for s ≤ r.
Consequences:
- If a generator g = m k + a has its pure cube 3g in Ap, then k = 1. (Advisor's observation: 3k ≤ k_{3g} ≤ 5.)
- Every generator that occurs in an Apéry element of height 3 has k ≤ 3.
- Proof: w_s ≤ w_r = 5m + r < 6m. ∎

**Lemma Q5-LEVEL1 (PROVED; CHECKED).** Suppose q = 5, every Apéry element is a sum of ≤ 3 minimal generators, and every
minimal generator other than m lies in (m, 2m). Then
    ℓ = 5 + Σ_{g} (4 − [g>r]) + Σ_{p∈P} (3 − carry_p − [p>r]) + Σ_{z∈C} (2 − carries_z − [z>r]),
where every summand is ≥ 0: generator terms are ≥ 3, pair terms ≥ 1, cubic terms ≥ 0. Hence ℓ ≥ 5 + 3d + |P|, and
    e(3d + |P| + 5) ≥ 4m + r + 1   ⟹   Wilf.
- Proof.
  - μ_s = 5 − k_s − [s > r] (Lemma K at q = 5) and μ_0 = 5.
  - With level-1 generators, k_s = h + carries for any factorization of length h. Carries are ≤ 1 for pairs and
    ≤ 2 for cubics, and the latter = 2 only if s ≤ r (Lemma LEVEL-BUDGET). ∎
- Full pairs (Sidon-with-0 covers): the condition reads exactly θ ≤ 3(d+5)/(4(d+3)) − (r+1)/(4T).
  - CORRECTION (advisor, 2026-10-21): an earlier version wrote "− O(1/T)". That is wrong, since r can be as large as
    m − 1, so the correction is up to ≈ θ/4.
  - Uniform in r (using r + 1 ≤ m): θ ≤ 3(d+5)/(5(d+3)), i.e. 0.80, 0.771, 0.75, 0.733, 0.709 for d = 3–6, 8, → 3/5.
  - Found densities 0.75, 0.686, 0.714, 0.655, ≥ 0.612 (d = 3–6, 8) are still below. The asymptotic margin at 3/5
    is thin.
- The r-uniform worst case discards the conductor-position credits. Taking r ≈ m makes c ≈ 5m, and the count then
  assumes every generator and pair cell is LOW.
  - But LOW residues are exactly the interval {r+1, …, m−1} of length ρ.
  - Generators and pairs crammed into a short top interval cannot generate a cover, since their sumsets span ≤ 6ρ
    residues.
  - So either ρ is large (c = 4m + r + 1 small, threshold → 3/4) or most cells are HIGH (credits [s ≤ r] large). An
    r-aware version of the count should interpolate between the two (next task).
- The bound is lossy only on the cubic terms. A failure of the condition needs almost every cubic cell to have μ_z = 0,
  i.e. almost all cubics in the top layer [c, c+m). That is the BASE-family profile.
- Checked (q5lev1.py, E376): all unit rescalings of the dense covers d = 3–7 with all levels 1, plus 30000 random
  residue sets (m = 12–60, d = 3–8); 5680 S with q = 5, height ≤ 3, level-1 generators. The identity and the bound
  were asserted on every S. The sufficient condition held on all 5680, so the lemma proves Wilf for each of them.
- Remaining at q = 5, height 3:
  - (i) level-1 configurations violating the condition (none found);
  - (ii) generators of level 2–3, to be charged against the cubics the level budget forbids (the advisor's
    principle).
- Novelty: unchecked. This is an elementary left-element count in the spirit of Eliahou's c ≤ 3m argument.
  Literature check pending.

**Lemma LEVEL1-THRESHOLD (PROVED; CHECKED).** Let every minimal generator other than m lie in (m, 2m); any depth q. For
each residue s, take any factorization of w_s, of length h_s and with integer residue sum σ_s (so w_s = h_s m + σ_s). Then
    μ_s = q − h_s − #{j ≥ 0 : σ_s > jm + r},       ℓ = qm − H − Σ_{j≥0} N(jm + r),
where H = Σ_s h_s and N(t) = #{s : σ_s > t}.
- Proof: k_s = h_s + ⌊σ_s/m⌋ and s = σ_s mod m. Also ⌊σ/m⌋ + [σ mod m > r] = #{j ≥ 0 : σ > jm + r}, checked on each
  interval [jm, jm + r] and (jm + r, (j+1)m). Then apply μ_s = q − k_s − [s > r]. ∎
- Checked on 20000 random S generated in (m, 2m), with depths q = 2–13 (lev1id.py).
- At q = 5 and height ≤ 3: N(2m + r) = 0, since a cell beyond that threshold would exceed max Ap. So the advisor's credits
  are exactly the cells whose residue sum stays below r or below m + r.
  - His top-layer criterion for cubics, a + b + c ≥ m + r + 1, is the second threshold.
- Corollary (graded, height ≤ 3, q = 5; via CH′, eH ≤ 3(e−1)m):
    N(r) + N(m + r) ≤ (2 − 1/e)·m − (r+1)/e   ⟹   Wilf.
  This is a sufficient condition and is lossy wherever CH′ is. Untested; the next C-enumeration target.
- All-LOW generators (PROVED): if every generator residue is > r, then generators lie in the interval {r+1, …, m−1} of
  length ρ. So A ∪ 2A ∪ 3A covers at most 6ρ − 3 residues. At height ≤ 3 this forces ρ ≥ (m+2)/6, i.e. c ≤ 5m − (m+2)/6.
  This is the first case of "the credits cannot all be small": c ≈ 5m and all generators LOW are incompatible.

### Residue descent: the identity ID-U, Lemma DESCENT-T, and the q = 5 window as Wilf for a truncated sumset (2026-10-21)
**Setting (every numerical semigroup S ≠ ℕ).**
- m = multiplicity; minimal generators m, g_1, …, g_d (e = d + 1), with g_i = k_i m + a_i and 1 ≤ a_i ≤ m − 1.
  (a_i ≠ 0, since a minimal generator ≠ m is not a multiple of m.)
- T := ⟨m, a_1, …, a_d⟩ is a numerical semigroup, because gcd(m, a) = gcd(m, g) = 1. It contains S, has multiplicity
  ≤ min a_i < m, and e(T) ≤ e.
- τ_s := min(T ∩ (s + mℤ)), so {τ_s} = Ap(T, m). Selmer's formulas hold for the Apéry set w.r.t. any nonzero
  element, so c(T) = max τ − m + 1 (= 0 iff T = ℕ) and g(T) = Σ⌊τ_s/m⌋.
- For a factorization n ∈ ℕ^d of w_s = min(S ∩ (s + mℤ)), put κ(n) = ⟨n, k⟩ (level-weighted length) and
  σ(n) = ⟨n, a⟩ (integer residue sum). So w_s = m·κ(n) + σ(n).
- D: for each s choose n(s) maximizing κ, ties broken by a fixed monomial order.
  - D is a down-set: a sub-factorization of an Apéry factorization is an Apéry factorization, and a better one would
    lift, by additivity of κ and of the order, to a better factorization of w_s.
  - Put κ_s = κ(n(s)), σ_s = σ(n(s)), K* = max κ_s, and U := {σ_s} + mℕ.
- U ⊆ T, since each σ_s is a sum of a_i's. U ∩ (s + mℤ) = σ_s + mℕ, so U is cofinite with c_U = max σ − m + 1,
  g_U = Σ⌊σ_s/m⌋, and ℓ_U = |U ∩ [0, c_U)| = c_U − g_U.
- Note: U + U ⊆ U ⟺ U = T. (⟸ is clear. ⟹: U is then a monoid containing m and A, so U ⊇ T ⊇ U.)

**Identity ID-U (PROVED, exact; every S and every factorization down-set D).**
    W(S) = Δ′ + W_e(U),   with   Δ′ := (e−1)(max w − max σ) − e·Σ_s κ_s   and   W_e(U) := e·ℓ_U − c_U.
- Proof: g(S) = Σ⌊w_s/m⌋ = Σκ_s + g_U and c(S) = max w − m + 1. Substitute into W = (e−1)c − e·g. ∎
- Column form (CH′ for S minus CH′ for U on the same D):
    m·Δ′ = Σ_i Σ_{i-columns C} |C|·[(max w − max σ) − m·κ(top C)].
- **Lemma CH′-κ (PROVED).** (d+1)·Σ_s κ_s ≤ d·m·K*, i.e. Δ := (e−1)mK* − eΣκ_s ≥ 0.
  - Proof: the column identity Σ_i Σ_C |C|·f(top C) = (d+1)·Σ_{x∈D} f(x) holds for every linear f on a finite down-set.
    Take f = κ and use κ(top) ≤ K*, Σ|C| = dm. ∎
- Δ′ = Δ − (e−1)·Gap, where Gap := mK* + max σ − max w ≥ 0. (max w ≤ mK* + max σ termwise.)

**Combined descent identity (bookkeeping; PROVED).** For every S, the max-κ down-set D, U = U_D ⊆ T:
    W(S) − W(T) = Δ′ − e·h + (e−1)·δc + (e − e(T))·ℓ(T),     h := |T∖U|,   δc := c(U) − c(T) ≥ 0.
- Proof: ID-U gives W(S) = Δ′ + W_e(U).
  - U ⊆ T with both cofinite, so g(U) − g(T) = |T∖U| = Σ_s (σ_s − τ_s)/m, and W_e(U) − W_e(T) = (e−1)δc − e·h.
  - W_e(T) − W(T) = (e − e(T))·ℓ(T). This also holds for T = ℕ, with c = ℓ = 0. ∎
- No new content: this is ID-U plus definitions. It is the accounting sheet for the three payers, Δ′,
  (e−1)δc and (e − e(T))ℓ(T), against the cost e·h.
  - Example ⟨34,42,53,54,56,57,67⟩: Δ′ = Δ_3 = 115, e·h = 7, δc = 0, e = e(T).

**Lemma DESCENT-T (PROVED on paper; CHECKED E379).** Suppose
- (U=T): σ_s = τ_s for every s, and
- (ALIGN): max w = m·K* + max τ.
Then
    W(S) = Δ + e·ℓ(T) − c(T) = Δ + W(T) + (e − e(T))·ℓ(T) ≥ W(T).
- Proof: Gap = 0 and U = T in ID-U, so W_e(U) = eℓ_T − c_T. Use e ≥ e(T) and ℓ_T ≥ 0. ∎
- Relation to Lemma DESCENT (above): this is DESCENT with t = 1 along the level-weighted length κ, pushed past the
  multiplicity.
  - DESCENT's hypothesis (a) w′_s > m is dropped. It was recorded as "the usual blocker (a level-1 generator)".
  - DESCENT's Kunz-validity (b) for w′ = σ becomes exactly U = T.
  - Gradedness is replaced by the max-κ down-set.
  - The new feature is that the multiplicity strictly drops: mult(T) ≤ min a_i < m.
- **Variant (PROVED, from ID-U alone).** If (U=T) and Δ′ ≥ 0, then W(S) = Δ′ + W_e(T) ≥ Δ′ + W(T) ≥ W(T).
  - (ALIGN) is a structural sufficient condition for Δ′ ≥ 0 (Δ′ = Δ there). Δ′ ≥ 0 itself is checkable.
  - Without (ALIGN), Δ′ ≥ 0 holds on all but 7 of the 208,532 U = T semigroups at genus 24 (E379).
- **Corollary (induction).** If Wilf holds for all numerical semigroups of multiplicity < m, it holds for every S of
  multiplicity m with (U=T) and Δ′ ≥ 0. So a minimal-multiplicity counterexample has U ≠ T, or U = T with Δ′ < 0.
  - Coverage (E379, genus 24, all 282,828 S): 208,529 S (≈ 74%).
    - 153,229 of them have T = ℕ (the NoWrap case).
    - 55,300 (≈ 20% of all S) have T ≠ ℕ. This is the new part.
  - Genus 36 (all 109,032,500 S): 70,549,557 S (64.7%).
    - 49,816,656 of them have T = ℕ.
    - 20,732,901 (19.0%) have T ≠ ℕ.
    - The share falls slowly with genus (71.8% at genus 26, 68.6% at 30, 66.5% at 33).
- **Corollary (unconditional).** (U=T) and (ALIGN) together with any known Wilf criterion for T imply Wilf for S.
  Examples of such criteria: mult(T) ≤ 19 (LITERATURE #26), 3e(T) ≥ mult(T) (#21), c(T) ≤ 4·mult(T)
  (depth four, kernel-checked).
  - Here mult(T) = least element of ⟨A⟩ ∪ {m} = min A, and c(T) = c(S) − mK*. So the class contains S of every
    multiplicity, e.g. any (U=T)&(ALIGN) S with a generator ≡ a (mod m), a ≤ 19.
- Under the retained hypothesis U=T, the case T=ℕ has σ_s=s and is the NoWrap corollary
  (2026-10-19, Lean, lean/Wilf/NoWrap.lean), without needing (ALIGN). **Clarification 2026-10-23:**
  T=ℕ alone is not the Lean NoWrap hypothesis; <10,17,41> has T=ℕ but w_4=34=2*17 has only
  the residue sum14>=10. The reference here concerns U=T=ℕ, not every S with a generator of residue1.
- Scope (E379, exhaustive genus ≤ 36): (U=T) holds on ≈ 74% of all S and (U=T)&(ALIGN) on ≈ 25%, with T ≠ ℕ in about
  half of the latter. The identity was asserted on every one.

**Level-1, height ≤ 3 (Problem 1.8 at height ≤ 3; PROVED).** Let all g_i ∈ (m, 2m) and let every Apéry element have all
factorizations of length ≤ 3. Then:
- (i) κ = length, and σ_s = min(3A′ ∩ (s + mℤ)), with A′ = A ∪ {0}. Hence U = 3A′ + mℕ.
  - Proof: let τ ∈ jA (j ≤ 3), τ ≡ s, τ < σ_s. Then jm + τ = w_s + k′m with k′ ≥ 0, and j > h_s + k′.
    - k′ = 0 gives a factorization of w_s longer than the maximum.
    - k′ ≥ 1 forces j = 3, h_s = 1, k′ = 1. Then τ = a_s − m < 0. ∎
- (ii) If q = 5, then Gap = 0 and K* = 3.
  - w_r = 5m + r forces h_r = 3 and σ_r = 2m + r = max σ.
  - Hence W(S) = Δ_3 + W_e(U), with c_U = m + r + 1 and ℓ_U = |X| + |Y|. So **E3 = −W_e(U)** exactly: the advisor's E3 ≤ 0 is
    Wilf's inequality for the truncated sumset U = 3A′ + mℕ, with e = |A′|.
  - The earlier tests used min-length or chain factorizations. Their E3 is ≥ the max-length E3, because E3 = Δ_3 − W
    and Δ_3 decreases as H increases. So those tests also check this version.
- (iii) If moreover U = T: W(S) ≥ Δ_3 + W(T) ≥ W(T), and c(T) = m + r + 1. This holds on 98–100% of the
  q = 5, height ≤ 3, level-1 S at d = 3, 4 (E378).
  - Wilf for S then follows from any known criterion for T, e.g. min A ≤ 19, or m + r + 1 ≤ 4·min A, or 3e(T) ≥ min A.
- (iii′) **Unconditional corollary (PROVED).** Let S be level-1, height ≤ 3, q = 5, with U = T, and suppose min A ≤ 19 or
  min A ≥ (m + r + 1)/4. Then S satisfies Wilf.
  - Proof: T has multiplicity min A and c(T) = m + r + 1.
    - If min A ≤ 19: Wilf is known for multiplicity ≤ 19.
      - EXTERNAL COMPUTATIONAL DEPENDENCY, not verified by us: BGOW m ≤ 18 (#27, read) and Kliem–Stump m = 19 (#26,
        secondary).
      - The c ≤ 4·mult branch below is kernel-checked.
    - Otherwise c(T) ≤ 4·mult(T), and Wilf holds by the depth-four theorem (kernel-checked).
    - So W(T) ≥ 0, and (iii) gives W(S) ≥ 0. ∎
  - In particular, every U = T member with m ≤ 39 is settled, since min A ≥ 20 implies min A ≥ m/2 > (m + r + 1)/4.
  - Combined with c ≤ 4m (q ≤ 4), Problem 1.8 at height ≤ 3 is now open only on:
    - the residual U ≠ T;
    - U = T with 19 < min A < (m + r + 1)/4, which forces m ≥ 40.
  - The E3-extremal family belongs here: every generator residue exceeds m/2.
    - Minimum −E3 = e(e+1) − (m + r + 1) = 2, 4, 8, 14 for e = 4–7, at ⟨13,22,23,25⟩, ⟨19,32,33,35,37⟩,
      ⟨25,42,43,45,47,49⟩, ⟨31,52,53,54,57,60,61⟩ (E378).
- (iv′) RESID-PAY (Δ₃ ≥ e·|T∖U|) is FALSE at e = 7: ⟨42,45,56,64,67,69,80⟩ (FAILED.md).
  - Together with the MONO*-Q5 counterexample, this shows that no single payer in the combined identity dominates on
    the residual.
  - TRUNC₃ held with slack ≥ 74 on both counterexamples.
- (iv) Residual: U ≠ T. Then some T-Apéry element needs ≥ 4 summands, so 4·min A ≤ max τ < 2m + r.
  - Observed: every U ≠ T example has a small residue and large E3 slack (≈ 30 at m = 14–20).
  - E3 there is Conjecture TRUNC₃ below.

**Conjecture TRUNC (CONJ; CHECKED E380).** Let A ⊆ [1, m−1], A′ = A ∪ {0}, and k ≥ the least k with kA′ ≡ ℤ/m. Then
U_k = kA′ + mℕ satisfies (|A| + 1)·ℓ(U_k) ≥ c(U_k).
- k → ∞ gives (|A|+1)ℓ(T) ≥ c(T), which Wilf for T implies (and which is weaker than Wilf). So TRUNC is a family of
  truncated analogues, not a reformulation of Wilf.
- TRUNC₃ for the q = 5, height ≤ 3 residual (iv) would finish Problem 1.8 at height ≤ 3, given Wilf below multiplicity m.
- Checked: all A with |A| = 2, 3, 4, m ≤ 40 (|A| = 2, 3: m ≤ 30), k = h … h+3. 0 failures; the minimum slack 0 is
  attained only where U_k = ℕ.

**Conjecture RD (CONJ; CHECKED E379, E380).** W(S) ≥ W(⟨m, g_1 mod m, …, g_d mod m⟩) for every S. 0 failures on every S of
genus ≤ 36 (≈ 2.8·10⁸ S).
- By induction on multiplicity, RD implies Wilf. So it is at least as strong as Wilf. The evidence is thin, because
  W(T) > 0 for only ≈ 1% of S.
- RD′ (the stronger W(S) ≥ eℓ_T − c_T) is FALSE: ⟨7,11,13,23⟩ has W = 4, eℓ_T − c_T = 6.
- Single-generator level drops are not monotone (FALSE): low drops of ⟨m, m+1, …, 2m−1⟩, and high drops such as
  ⟨15,18,…,29,31,32⟩ with 31 → 16 (W = 12 → 24).
- Δ′ ≥ 0 under U = T is FALSE (7 cases at genus ≤ 24, min −6), but RD held on every one, through the (e − e_T)ℓ_T term.
- On the residual U ≠ T, neither half of W(S) = Δ′ + W_e(U) dominates W(T) on its own.
  - Δ′ < 0 on ≈ 2% of it.
  - MONO* W_e(U) ≥ W(T) first fails at ⟨8,14,23,29⟩ (genus 26).
  - RD survives, each half paying for the other's deficit. A proof of RD must couple them.
- At q = 5, height ≤ 3, level 1, the residual needs only MONO* (Δ_3 ≥ 0 there). MONO*-Q5 is FALSE.
  - At e = 7: ⟨34,42,53,54,56,57,67⟩ has W_e(U) = 74 < W(T) = 81 (FAILED.md). It held at e = 5, 6.
  - E3 ≤ 0 itself survives there and on all 10,663 residual S at e = 7 (E378). So the residual must be done by
    TRUNC₃ directly.

### TRUNC₃: the low regime is settled; the open regime carries Wilf content (2026-10-21)
**Setting.**
- A ⊆ [1, m−1] nonempty, A′ = A ∪ {0}, P = A ∪ {m} (so |P| = e = |A| + 1), μ = min A = min P.
- For k ≥ 1, U_k = kA′ + mℕ (kA′ = integer sums of at most k elements of A). Covering hypothesis: kA′ ≡ ℤ/m.
- T = ⟨P⟩ = ⟨m, A⟩, a numerical semigroup of multiplicity μ.
- c = c(U_k), ℓ = ℓ(U_k) = |U_k ∩ [0, c)|. TRUNC_k is the statement e·ℓ ≥ c.

**Lemma DOWN (PROVED).** U_k is P-downward closed: every u ∈ U_k ∖ {0} can be written u = p + u′ with p ∈ P and
u′ ∈ U_k.
- Proof: write u = σ + jm with σ ∈ kA′.
  - If j ≥ 1, take p = m.
  - Otherwise σ ≠ 0; remove one A-summand, which leaves an element of (k−1)A′ ⊆ U_k. ∎

**Lemma LOW-AGREE (PROVED; CHECKED lowagree.py).** U_k ∩ [0, (k+1)μ) = T ∩ [0, (k+1)μ). Hence if c(U_k) ≤ (k+1)μ,
then U_k = T.
- Proof:
  - An element of T below (k+1)μ is a sum of at most k elements of P, since every element of P is ≥ μ. Of these
    summands, j ≤ k come from A and the rest are copies of m. So the element lies in kA′ + mℕ = U_k.
  - Conversely U_k ⊆ T.
  - If c(U_k) ≤ (k+1)μ, every gap of U_k lies below (k+1)μ, so it is a gap of T. Hence U_k = T. ∎
- Check: 16,242 random covering instances, with k ∈ {2,3,4}, m ≤ 70, |A| ≤ 9. U_k is built from the explicit sumset
  and T by a membership DP.
  - The sets agree below (k+1)μ on all 16,242.
  - U_k = T on all 10,071 instances with c ≤ (k+1)μ.

**Theorem KAPLAN-U (PROVED, self-contained; CHECKED).** Let U ⊆ ℕ satisfy:
- 0 ∈ U, U is cofinite, and P ⊆ U with |P| = e;
- μ = min P = min(U ∖ {0});
- U is P-downward closed (as in Lemma DOWN).

If c(U) ≤ 2μ, then e·ℓ(U) ≥ c(U). In particular TRUNC_k holds whenever c(U_k) ≤ 2·min A.

Proof (Kaplan's c ≤ 2m argument, with closure replaced by downward closure). Let L = U ∩ [0, c) and P_< = P ∩ (0, c).
- (F1) U ∩ (0, 2μ) ⊆ P.
  - Write u = p + u′. If u′ ≠ 0, then u ≥ 2μ.
- (F2) Every y ∈ [c, c + μ) ∖ P is the sum of two elements of P_<.
  - Write y = p + u′ with u′ ≠ 0, so u′ ≥ μ. Then p = y − u′ < c and u′ = y − p ≤ y − μ < c.
  - By (F1) and c ≤ 2μ, we get u′ ∈ L ∖ {0} ⊆ P.
- So L ∖ {0} = P_<. Put k′ := |P_<| = ℓ − 1.
- The window [c, c + μ) lies in U and has μ elements. By (F2), μ ≤ (e − k′) + k′(k′+1)/2, so e ≥ μ − k′(k′−1)/2.
  Also e ≥ k′.
- Case k′ = 0: then U ∩ (0, c) = ∅, so c ≤ μ ≤ e.
- Case k′ = 1: then e ≥ μ, so eℓ = 2e ≥ 2μ ≥ c.
- Case k′ ≥ 2:
  - If k′(k′+1) ≥ 2μ, then eℓ ≥ k′(k′+1) ≥ 2μ ≥ c.
  - Otherwise μ > k′(k′+1)/2, and
    eℓ ≥ (k′+1)(μ − k′(k′−1)/2) = 2μ + (k′−1)(μ − k′(k′+1)/2) > 2μ ≥ c. ∎
- Answer to the advisor's question "what needs closure": Kaplan's argument needs only downward closure (F2), which
  truncated sumsets have. Upward closure (x, y ∈ U ⟹ x + y ∈ U) is not used.

**Corollary TRUNC-LOW (PROVED; uses the kernel-checked depth-four theorem).** If k ≥ 3 and c(U_k) ≤ 4·min A, then
U_k = T, and e·ℓ(U_k) ≥ e(T)·ℓ(T) ≥ c(T) = c(U_k).
- Proof: LOW-AGREE gives U_k = T, since 4μ ≤ (k+1)μ.
- Then c(T) ≤ 4·mult(T), and Wilf holds for T by the depth-four theorem (conjectures.io proof, kernel-checked by us).
- Finally e ≥ e(T). ∎
- Variant for c ≤ 3μ: the same argument with Eliahou's c ≤ 3m theorem (LITERATURE #13, read).

**Consequences for the q = 5, height ≤ 3, level-1 residual (PROVED).**
- The residual U ≠ T forces c(U) > 4·min A, by LOW-AGREE.
- Case A (U = T) with c(T) ≤ 4·min A is settled unconditionally. This strengthens (iii′) above: the depth-four
  branch now covers every U = T member with min A ≥ c(T)/4.

**Remark WILF-CONTENT (PROVED).** In the regime c(U₃) > 4μ, TRUNC₃ contains Wilf for the following class:
    H3max := {numerical semigroups T whose Apéry set with respect to their largest minimal generator g lies in
               3(G ∖ {g})′, where G is the set of minimal generators}.
- Proof: given T ∈ H3max, take m = g and A = G ∖ {g}. Every element of A is < m, and distinct elements of A are
  distinct mod m.
  - Then σ_s = τ_s, so U₃ = T, and e = |A| + 1 = e(T).
  - So TRUNC₃ for this A is exactly Wilf for T. ∎
- No known theorem covers H3max with c(T) > 4·mult(T) (search 2026-10-21, LITERATURE). The covering property alone
  therefore cannot give TRUNC₃ in this regime without Wilf-type content at depth ≥ 5 relative to the multiplicity.
- Here c(T) < 2g, so the depth relative to g is below 2. The difficulty is the two scales μ ≪ m.

**Status of TRUNC₃ (unrestricted; CHECKED, E381).**
- 0 failures, sharp: equality at A = {m−d, …, m−1}.
  - Exhaustive for |A| = 4, 5, 6, 7, up to the covering limit. A covering A exists only for m ≤ 25, 40, 57, 81.
  - At |A| = 7 the U ≠ T minimum is 1.5, at A = {7,19,32,…,36}, m = 37 (c = 32 ≤ m). This is below F_≠, so F_≠ is not the
    U ≠ T minimizer from |A| = 7 on.
  - Hill climbing restricted to U₃ ≠ T for |A| = 8 and 10 (m ≤ 200).
- Near-equality in the proved regime c ≤ 2μ: A = {μ, 2μ−1} ∪ [2μ+1, m−1] with m = 3μ − 2, c = 2μ − 1, ℓ = 2.
- Minimum ratio e·ℓ/c by t = ⌈c/μ⌉ (|A| = 6, exhaustive): 1.0, 1.08, 1.17, 1.22, 1.35, 1.40, 1.53, 1.75, …
- The open regime has ratio → 1 (family F_T below). A lower bound by a constant > 1 there is FALSE.
- Open: TRUNC₃ for c(U₃) > 4·min A.
  - If U₃ = T, it is Wilf for an H3max-type T (when e(T) = e).
  - If U₃ ≠ T, the set is genuinely truncated: T ∖ U₃ ⊆ [4μ, c(U₃)) by LOW-AGREE.

### TRUNC₃ split by U = T and U ≠ T (2026-10-21)
**Remark TARGET (PROVED).** For the q = 5, height ≤ 3, level-1 residual, TRUNC₃ is needed only when U ≠ T.
- If U = T, then (iii) gives W(S) ≥ Δ₃ + W(T) ≥ W(T), and mult(T) = min A < m. So Wilf for multiplicities < m gives
  W(S) ≥ 0, with no TRUNC₃.
- Hence the exact target is **TRUNC₃^≠**: if 3A′ covers ℤ/m and U₃ ≠ T, then e·ℓ(U₃) ≥ c(U₃).
- By LOW-AGREE, TRUNC₃^≠ lives in the regime c(U₃) > 4μ.
- In the residual itself c(U) = m + r + 1 > m, the case of Lemma C>M below.
- Remark WILF-CONTENT concerns U = T only, so it does not obstruct TRUNC₃^≠. Family F_≠G below shows that the
  covering property alone does not prove TRUNC₃^≠ either.

**Family F_T (U = T; CHECKED fam*.py, μ = 4…15).**
- Data: μ ≥ 4, A = {μ, 3μ, 5μ} ∪ [5μ+1, 6μ−2], m = 6μ − 1, so |A| = μ + 1 and e = μ + 2.
- Then U₃ = T = ⟨μ, 5μ+1, …, 6μ−1⟩, the Wilf-equality semigroup of depth 5; 3μ and 5μ are redundant padding.
- c = 5μ, ℓ = 5, e·ℓ − c = 10, ratio (μ+2)/μ = (d+1)/(d−1) → 1.
- These are the open-regime minimizers found for |A| = 7, 8.

**Family F_≠ (U ≠ T; CHECKED, minimizer over U ≠ T for |A| = 4, 5, 6 exhaustive, verified for d = 4…15).**
- Data: d ≥ 4, A = {1, 3d, 3d+2, 3d+5, …, 3d+2+3(d−3)}, m = 6d − 4.
- Then T = ℕ, U₃ ∩ [0, c) = {0, 1, 2, 3}, c = 3d, ℓ = 4.
- So e·ℓ − c = d + 4, and the ratio is 4(d+1)/(3d) → 4/3.

**Family F_≠G (U ≠ T; PROVED by hand for μ ≥ 3, CHECKED famG.py and trunc3n at μ = 7, 8, 9, 12, 16, 24).**
- Data: μ ≥ 3, m = 5μ + 1, A = {μ, 3μ+1} ∪ [4μ+2, 5μ], e = μ + 2.
- T = ⟨μ, 3μ+1, 4μ+2, …, 5μ−1⟩ with e(T) = μ, since 5μ = 5·μ and m = 2μ + (3μ+1) are redundant.
- Covering: mod m, A′ = {0, μ, 3μ+1, −1, …, −(μ−1)}.
  - x − j (x ∈ 2{0, μ, 3μ+1}, 1 ≤ j < μ) covers [1, μ−1], [μ+1, 2μ−1], [2μ+2, 3μ], [3μ+2, 4μ].
  - (3μ+1) − j₁ − j₂ gives 2μ+1, and the block gives [4μ+2, 5μ].
- Lifts:
  - s + m ∈ 3A′ for every s ∈ [1, 4μ] ∖ {μ, 2μ, 3μ, 3μ+1}, e.g. 4μ + m = (3μ+1) + μ + 5μ.
  - 4μ ∉ 3A′.
- Hence c(U₃) = 4μ + 1, L(U₃) = {0, μ, 2μ, 3μ, 3μ+1}, T ∖ U₃ = {4μ}, c(T) = 4μ and ℓ(T) = 5, so h = δc = 1.
- W(T) = μ, W_e(T) = μ + 10, W_e(U₃) = μ + 9 = W_e(T) − 1.
- Ratio 5(μ+2)/(4μ+1) → 5/4 (T's own Wilf ratio). It lies below F_≠ for d = μ + 1 ≥ 13.
- Here TRUNC₃^≠ is exactly W_e(T) ≥ 1. A proof of TRUNC₃^≠ must therefore use T's Wilf slack quantitatively, via the
  identity TRUNC₃ ⟺ e·h ≤ W_e(T) + (e−1)δc.

**Observation (the residual's regime; E381).** On U ≠ T with c(U₃) > m, the case the residual needs, the margin is
large.
- Exhaustive minimum ratio for |A| = 3, 4, 5, 6: 1.882, 1.667, 1.714, 1.653. Minimum slack e·ℓ − c: 15, 20, 31, 40.
  - Minimizers: A = {4,9,10}, m = 13; {7,16,17,19}, m = 23; {12,25,26,28,30}, m = 31; {17,36,38,39,43,44}, m = 46.
- On U = T with c > m the minimum ratio is 1.111, 1.154, 1.200, 1.333 (minimum slack 2, 4, 8, 14).
- Both U ≠ T near-tight families, F_≠ and F_≠G, have c ≤ m.
- Every one of these U ≠ T, c > m minimizers (and the minimum-slack ones) has T ∖ U = {4μ} and δc ∈ {0, 1}.
  - So W_e(U) = W_e(T) − e + (e−1)δc: the slack is T's Wilf slack, and T there is far from Wilf-tight. Examples:
    - ⟨17,36,38,39,43,44,46⟩: W(T) = 54, c(T) = 72;
    - ⟨12,25,26,28,30,31⟩: W(T) = 36, c(T) = 48.
  - Checked by inspect.py (independent).
- So in the residual's regime the observed minimum of e·ℓ/c is ≈ 1.65 (|A| ≤ 6). Elsewhere families push it → 1
  (U = T) and → 5/4 (U ≠ T, c ≤ m).

**Lemma C>M (PROVED).** Suppose c = c(U₃) > m. Then:
- max σ = 2m + r for a unique class r, and c = m + r + 1.
- With z := |3A′ ∩ [0, m)| and t := #{s : σ_s ≥ 2m} (all such s satisfy s ≤ r):

      e·ℓ(U₃) − c(U₃) = e(z − t) + (e − 1)(r + 1) − m.

- So TRUNC₃ ⟺ m + e·t ≤ e·z + (e−1)(r+1).

Proof.
- Let M = max σ = c + m − 1. Then 2m ≤ M < 3m, so r := M − 2m ∈ [0, m).
- For s > r: s + m ≥ c, so s + m ∈ U and σ_s < 2m. So every class with σ_s ≥ 2m has s ≤ r.
- Left elements below m are the s with σ_s < m, that is 3A′ ∩ [0, m) (z of them).
- The left elements in [m, c) are s + m with s ≤ r and σ_s < 2m (r + 1 − t of them).
- So ℓ = z + r + 1 − t. ∎

**Identity ID-TOP (PROVED; CHECKED topid.c, every covering A with |A| ≤ 6, 0 mismatches).** Setting:
- U ⊆ ℕ cofinite with 0 ∈ U and U + m ⊆ U; A ⊆ [1, m−1]; e = |A| + 1.
- c = c(U) ≥ 1, L = U ∩ [0, c), ℓ = |L|. The window W := [c, c + m) holds one element of each class.

Pieces:
- TypeM := {y ∈ W : y − m ∈ U}. The map y ↦ y − m is a bijection TypeM → L ∩ [c − m, c).
- Top := W ∖ TypeM. For U = U₃, Top = {σ_s : σ_s ≥ c} ⊆ 3A′.
- Top₁ := Top ∩ (A + L) and Top₂ := Top ∖ Top₁.
- N_< := #{(a, x) ∈ A × L : a + x < c}.
- Π := {(a, x) ∈ A × L : a + x ≥ c}. Then a + x < c + m always, so |Π| = (e−1)ℓ − N_<.
- Π_M := {(a, x) ∈ Π : a + x ∈ TypeM}, and Ov := |Π ∖ Π_M| − |Top₁| ≥ 0.
- G₀ := [0, c − m) ∖ U (empty if c ≤ m).

Then

    e·ℓ − c = N_< + |Π_M| + Ov + (m − c)⁺ − |G₀| − |Top₂|.

Proof: m = |TypeM| + |Top₁| + |Top₂| = |L ∩ [c−m, c)| + |Π ∖ Π_M| − Ov + |Top₂|. Substitute |Π| and use
ℓ − |L ∩ [c−m, c)| + (m − c) = (m − c)⁺ − |G₀|. ∎

Remarks:
- Compare a numerical semigroup S with multiplicity m and A its other minimal generators. Now A ⊆ (m, c+m), so
  |Π| also loses the pairs with a + x ≥ c + m. There Top₂ = ∅: a top element y has y − m ∉ S, so y = a + x with
  a ∈ A and x ≤ y − m < c.
- For U₃, Top₂ ≠ ∅ is possible because min A < m. A Top₂ element is a 3-sum a₁ + a₂ + a₃ all of whose pairwise sums
  are ≥ c, so y ≥ 3c/2. This is where the two scales μ ≪ m enter.
- Data, c > m (the residual's case):
  - K2 := N_< + Ov − |Top₂| ≥ 0 on every instance, U = T and U ≠ T alike. Minima 3, 7, 10 for |A| = 4, 5, 6.
  - K1 := |Π_M| − |G₀| is negative on 11, 60, 291 U = T and 0, 0, 2 U ≠ T instances. Minimum −10 at
    A = {17,34,41,43,44,48}, m = 49; for U ≠ T, −1 at A = {15,32,34,36,41,43}, m = 44.
  - The crude form |Top₂| + |G₀| ≤ N_< + (m−c)⁺ fails (FAILED.md).
  - So, with c > m, the deficit G₀ must be paid jointly by Π_M and the multiplicity Ov.
- Open (precise obstruction): an injection, valid for c > m, of G₀ ∪ Top₂ into the pairs counted by N_< + |Π_M| + Ov.
  The F_≠G family shows that it must use T's Wilf slack when U ≠ T.

### The residual through T: relative Wilf (PAY2) (2026-10-21)
**Setting.** Q5 is the class of S that are level 1 (all g_i ∈ (m, 2m)), have height ≤ 3 (every factorization of every
Apéry element has length ≤ 3) and q = 5.
- T = ⟨m, A⟩ with Ap(T, m) = {τ_s}; λ_s := (w_s − τ_s)/m ∈ ℕ.
- On the residual, U ≠ T.

**Identity ID-T (PROVED, exact; every S).** W(S) = Δ′_T + W_e(T), where

    Δ′_T := (e−1)(max w − max τ) − e·Σ_s λ_s,   W_e(T) := e·ℓ(T) − c(T) = W(T) + (e − e(T))·ℓ(T).

- Proof: g(S) = Σ⌊w_s/m⌋ = Σλ_s + g(T) and c(S) − c(T) = max w − max τ. Substitute into W = (e−1)c − e·g. ∎
- Equivalent forms:
  - Δ′_T = (e−1)Δc − e·Δg = e·Δℓ − Δc, with Δx := x(S) − x(T).
  - On Q5, max w − max σ = 3m and λ_s = h_s + j_s, with j_s := (σ_s − τ_s)/m. So Δ′_T = Δ₃ + (e−1)δc − e·h, which is
    the combined identity.

**Conjecture PAY2 = relative Wilf on Q5 (CONJ; CHECKED E381).** Every S ∈ Q5 satisfies

    e(S)·(ℓ(S) − ℓ(T)) ≥ c(S) − c(T),   i.e.   Δ′_T ≥ 0,   i.e.   Δ₃ + (e−1)·δc ≥ e·|T∖U|.

- On U = T it is Δ₃ ≥ 0 (CH′-κ, PROVED). So PAY2 is open only on the residual.
- PAY2 + induction on multiplicity ⟹ Wilf on Q5. Indeed W(S) ≥ W_e(T) ≥ W(T) ≥ 0, since mult(T) = min A < m.
  - This needs W(T) ≥ 0 only, not T's slack. That is the advantage over TRUNC₃^≠, which needs T's slack (F_≠G).
- It discards W(T) and (e − e(T))ℓ(T) from RD (= PAY3). It keeps the δc term that RESID-PAY dropped; RESID-PAY is FALSE
  at e = 7.
- RD′ in general (W(S) ≥ W_e(T) for every S) is FALSE (⟨7,11,13,23⟩, not level 1). PAY2 is RD′ restricted to Q5.
- Evidence: every residual S with e = 5, 6, 7, 8 (22, 454, 10,663 and 269,663 S; exhaustive at fixed e, all m; E381,
  E382), with the combined identity asserted on each.
  - 0 failures. Minimum Δ′_T = 35, 29, 55, 78, at ⟨20,24,29,37,38⟩, ⟨40,49,54,63,65,78⟩, ⟨47,50,65,80,86,88,89⟩,
    ⟨62,65,80,95,110,116,118,119⟩.
  - At e = 8 the adversarial slices h ≥ 2 (177,037 S) and δc = 0 (137,143 S) both have minimum 78.
  - Annealing at e = 9–15 (q5ann, not exhaustive): 0 failures.
  - The RESID-PAY counterexample ⟨42,45,56,64,67,69,80⟩ has Δ′_T = 98 + 162 − 105 = 155.
- Obstruction to the CH′-type proof:
  - CH′-κ uses a linear level κ on a factorization down-set. Here λ_s is not linear on any down-set of
    T-factorizations of τ_s.
  - In Q5 a T-factorization of τ_s with U ≠ T has length k ≥ λ_s + 1 ≥ 4. Otherwise k = λ_s would give a factorization
    of w_s of length ≥ 4, and k < λ_s gives w_s − m ∈ S.
  - So the column bound with f = k overshoots. A proof must charge the excess k − λ_s, or the j_s, to columns of the
    max-κ tile D whose top has level < 3. Each such column contributes |C|·(3 − κ(top)) to Δ₃.

### PAY2: tile structure of the residual (2026-10-21)
**Setting.**
- S ∈ Q5. D is the tile of lex-largest max-length factorizations: one vector x_s ∈ ℕ^d per class, a down-set. Then
  |x_s| = h_s and σ(x_s) = σ_s.
- τ_s, λ_s, j_s = (σ_s − τ_s)/m as above. k_s := least length of a T-factorization of τ_s over A (τ_s ∈ ⟨A⟩).
- Classes split into EQ (j_s = 0), NE2 (j_s ≥ 1, h_s = 2) and NE3 (j_s ≥ 1, h_s = 3). h := |T∖U| = Σ_s j_s.

**Lemma NE-LEVELS (PROVED).**
- (a) s is NE ⟺ k_s ≥ 4.
- (b) EQ ⟹ h_s = k_s.
- (c) NE ⟹ λ_s ≤ k_s − 1.
- (d) NE ⟹ h_s ∈ {2, 3}, and h_s = 2 ⟹ j_s = 1.
- (e) NE3 ⟹ k_s ≥ 5.
- (f) If NE3 ≠ ∅ then NE2 ≠ ∅, and h ≥ 2.

Proof.
- (a) σ_s = min(3A′ ∩ (s + mℤ)), by Q5 (i). If k_s ≤ 3 then τ_s ∈ 3A′, so σ_s ≤ τ_s ≤ σ_s. If k_s ≥ 4 then
  τ_s ∉ 3A′, so σ_s ≠ τ_s.
- (b) The D-vector x_s is a T-factorization of τ_s = σ_s of length h_s, so k_s ≤ h_s. Any T-factorization of length k
  gives km + τ_s ∈ S in class s, so km + τ_s ≥ w_s = h_s m + τ_s.
- (c) Let z be a T-factorization of τ_s of length k. Then km + τ_s ∈ S.
  - If k < λ_s, then w_s − m = (km + τ_s) + (λ_s − 1 − k)m ∈ S, which is impossible.
  - If k = λ_s, then km + τ_s = w_s is a factorization of w_s of length k ≥ 4, against height ≤ 3.
- (d) j_s ≥ 1 gives σ_s ≥ m + τ_s > m. Also σ_s ≤ h_s(m−1), so h_s ≥ 2. If h_s = 2 then σ_s < 2m, so j_s = 1.
- (e) λ_s = 3 + j_s ≥ 4 and (c).
- (f) Take a least-length T-factorization z of τ_y for some y ∈ NE3, so |z| ≥ 5, and a sub-multiset z′ of size 4.
  - σ(z′) is T-Apéry: otherwise τ_y − m ∈ T.
  - σ(z′) has least length 4: otherwise z is not least.
  - So its class has k = 4. By (a), (c), (d) it is NE2 (λ ≤ 3, j ≥ 1). ∎

**Column-top form (PROVED).** Δ₃ = Σ_{x∈D} P(x), where

    P(x) := Σ_{i : x + e_i ∉ D} (x_i + 1)(3 − |x|) ≥ 0.

- Proof: CH′-κ's column identity gives Δ₃ = Σ_i Σ_{i-columns C} |C|(3 − |top C|).
- An i-column is determined by its top t (t ∈ D, t + e_i ∉ D), and it has |C| = t_i + 1 elements, because D is a
  down-set. ∎
- Level-3 elements have P = 0.
- For a level-2 element x, write out(x) := {i : x + e_i ∈ D}. Then P(x) = (e + 1) − Σ_{i∈out(x)} (x_i + 1), since
  Σ_i (x_i + 1) = |x| + d.

**Lemma OUT (PROVED).** If x = x_s with s ∈ NE2 and i ∈ out(x), then x + e_i = x_{s′} with s′ ∈ NE3.
- Proof: h_{s′} = 3 and σ_{s′} = σ_s + a_i = τ_s + m + a_i.
- τ_s + a_i ∈ T lies in class s′, so τ_{s′} ≤ σ_{s′} − m and j_{s′} ≥ 1. ∎

**Lemma SUPP (PROVED).** Let s ∈ NE, y := x_s, and let z be a least-length T-factorization of τ_s. Then
|z − min(y, z)| ≥ 4, where min is taken componentwise. In particular, if k_s = 4 then y and z have disjoint supports.
- Proof: put g = min(y, z), p = y − g and q = z − g. Then σ(p) − σ(q) = σ(y) − σ(z) = j_s·m ≥ m.
- Suppose |q| ≤ 3. As a sub-factorization of z:
  - σ(q) is T-Apéry, since otherwise τ_s − m ∈ T;
  - q has least length, since otherwise z is not least.
  So its class t has k_t = |q| ≤ 3. By NE-LEVELS (a), (b), t is EQ with σ_t = σ(q).
- p ≤ y ∈ D and D is a down-set, so p = x_{t′} with σ(p) = σ_{t′}. Here t′ is the class of σ(p) ≡ σ(q), so t′ = t.
- Hence σ(p) = σ_t = σ(q), contradicting σ(p) − σ(q) ≥ m. ∎
- Example: if τ_s = 4μ with z = 4e_μ, then σ_s = 4μ + m is a sum of two residues, neither of them μ.

**Lemma NE2-ONLY (PROVED).** If NE3 = ∅, then Δ₃ ≥ (e + 1)·|T∖U|. Hence RESID-PAY and PAY2 hold, and W(S) ≥ W(T).
- Proof: by OUT, out(x_s) = ∅ for s ∈ NE2, so P(x_s) = e + 1.
- By (d), h = Σ_s j_s = |NE2|.
- So Δ₃ ≥ Σ_{NE2} P = (e + 1)h. ∎
- **Corollary (PROVED).** PAY2 holds on Q5 when |T∖U| = 1, by (f). It also holds when every element of Ap(T, m) is a
  sum of at most 4 elements of A, by (e).
  - In either case W(S) ≥ W(T) + (e − e(T))ℓ(T). So Wilf for T implies Wilf for S.
- Coverage (E382): 2 / 22, 78 / 454, 3,013 / 10,663, 100,843 / 269,663 residual S at e = 5, 6, 7, 8 have NE3 = ∅ (9%, 17%, 28%, 37%).

**Identity ID-NE (PROVED; CHECKED q5d6, 0 mismatches).** With Peq := Σ_{x ∈ EQ} P(x) and
π(y) := Σ_{i : y − e_i ∈ NE2} y_i ≤ 3 for y ∈ NE3:

    PAY2 = Peq + |NE2| + (e−1)·δc − Σ_{y∈NE3} (e·j_y + π(y)).

- Proof: Δ₃ = Peq + Σ_{NE2} P. Then Σ_{NE2} P = (e+1)|NE2| − Σ_{(x,i): i ∈ out(x)} (x_i + 1).
- By OUT and the down-set property, (x, i) ↦ (x + e_i, i) is a bijection onto {(y, i) : y ∈ NE3, y − e_i ∈ NE2},
  with x_i + 1 = y_i.
- Finally h = |NE2| + Σ_{NE3} j_y. ∎
- So the NE3 classes are the only cost: e·j_y + π(y) each, against the EQ tops Peq, one unit per NE2 class, and
  (e−1)δc.

**Lemma ABOVE (PROVED).** Every class with σ_s > max τ is NE, and there are at most δc of them.
- Proof: τ_s ≤ max τ < σ_s.
- The σ_s are distinct integers in (max τ, max σ], and that interval has δc = max σ − max τ elements. ∎

**Reduction PAY2 ⟸ C* (PROVED).** Let Ab := {y ∈ NE3 : σ_y > max τ}. Then PAY2 ≥ Peq + |NE2| − cost*, where

    cost* := Σ_{y ∈ Ab} (e(j_y − 1) + 1 + π(y)) + Σ_{y ∈ NE3∖Ab} (e·j_y + π(y)).

- Proof: ID-NE, together with (e−1)δc ≥ (e−1)|Ab| (ABOVE). ∎

**Conjecture C* (CONJ; CHECKED E382): Peq + |NE2| ≥ cost*.** A joint tile-and-residue statement: the EQ column tops
pay for the level-3 NE classes. The EQ/NE labels depend on T's arithmetic, so this is not a pure down-set theorem
(advisor's correction).

**Conjecture A1 (CONJ; CHECKED E382), the parallel target.** Δ₃ ≥ e·h_lo + h_hi, where h_lo (resp. h_hi) counts
T∖U below c(T) (resp. in [c(T), c(U))).
- A1 ⟹ PAY2, since PAY2 = A1-slack + (e−1)u′ with u′ = |U ∩ [c(T), c(U))| ≥ 0.
- With j = 1, T∖U = {τ_s : s ∈ NE}. So A1 reads

      Σ_{x∈D} P(x) ≥ e·#{s ∈ NE : τ_s < c(T)} + #{s ∈ NE : τ_s ≥ c(T)}.

  An NE class costs e or 1 according to where its T-element sits relative to the old conductor.
- NE2-ONLY is the case NE3 = ∅, with the stronger cost e + 1 for every class.
- Minimum slack 22, 29, 51, 55 at e = 5–8. That is larger than C*'s (22, 29, 42, 37) in the worst case.
- 0 failures on every residual S at e = 5, 6, 7, 8. Minimum slack 22, 29, 42, 37 (e = 8: ⟨54,57,77,90,96,97,102,107⟩).
- Observed j_s ≤ 1 for every class (no j = 2 at e ≤ 8). If that holds, cost* = Σ_{Ab}(1 + π) + Σ_{NE3∖Ab}(e + π).
- Scaling (E383): max over the residual of (e·h_lo + h_hi)/Δ₃ is 0.353, 0.413, 0.490, 0.633 at e = 5–8. The
  ratio annealer finds 0.443 at e = 10 (h_lo = 14). So A1, and C* which implies it when j ≤ 1, is expected to fail
  near e ≈ 10–12. Not a proof target; superseded by A1-eT/DESC below.
- Charging every column top to the class it lands in fails (TGT, FAILED.md).
- Ablations (FAILED.md):
  - NE2 classes paying for themselves (H2: Σ_{NE2} P ≥ e|NE2|) fails 1 / 93 / 2,903 times (e = 6 / 7 / 8).
  - δc ≥ Σ_{NE3} j (B1) fails 27 / 1,155 / 39,827 times.
  - Peq + |NE2| ≥ Σ_{NE3}(j + π) (B2) holds, with minimum 22, 29, 53, 72.

**Identity DESC (PROVED).** On the Q5 residual put ρ := e − e(T), the number of elements of A ∪ {m} that are not
minimal generators of T, and u′ := |U ∩ [c(T), c(U))|. Then

    W(S) − W(T) = PAY2 + ρ·ℓ(T) = Δ₃ + (e−1)·u′ + ρ·|U ∩ [0, c(T))| − e(T)·h_lo − h_hi.

- Proof:
  - W(S) − W_e(T) = PAY2 and W_e(T) − W(T) = (e − e(T))·ℓ(T).
  - T∖U ⊂ [0, c(U)), and [c(T), c(U)) ⊂ T. So δc = h_hi + u′ and h = h_lo + h_hi, for any j.
  - U ⊂ T gives ℓ(T) = h_lo + |U ∩ [0, c(T))|.
  - Substitute into PAY2 = Δ₃ + (e−1)δc − e·h; note e − ρ = e(T). ∎
- Use: W(T) ≥ 0 by induction on multiplicity (m(T) = μ < m), so DESC := W(S) − W(T) ≥ 0 is all the descent needs.
  PAY2 is the special case that ignores ρ.
- e(T) ≤ m(T) = μ, because minimal generators other than μ have distinct nonzero residues mod μ. So a low NE
  element costs at most min(e, μ) in DESC, against e in PAY2/A1.

**Conjecture A1-eT (CONJ; CHECKED e ≤ 7, E383).** Δ₃ + ρ·|U ∩ [0, c(T))| ≥ e(T)·h_lo + h_hi.
- It implies DESC, the difference being (e−1)u′ ≥ 0.
- Exhaustive e = 5–8: min slack 36, 47, 88, 119. Max of (e(T)h_lo + h_hi − ρ|U ∩ [0,c(T))|)/Δ₃ is 0.000, 0.016,
  0.137, 0.173, against 0.353, 0.413, 0.490, 0.633 for A1.
- min DESC = 55, 47, 96, 128 (PAY2: 35, 29, 55, 78).
- ρ ≥ 1 on every residual S at e ≤ 6, and on all but 10 / 287 at e = 7 / 8. Where ρ = 0: h_lo ≤ 3 and A1 ratio ≤ 0.154.

**Conjecture C*-eT (CONJ; CHECKED e ≤ 7, E383).** Peq + |NE2| ≥ Σ_{NE3∖Ab} (e(T) + π(y)) + Σ_{NE3∩Ab} (1 + π(y)).
- This is C* with the per-class cost e replaced by e(T).
- C*-eT ⟹ DESC. By ID-NE, ABOVE and J1, DESC ≥ (C*-eT slack) + ρ·(#NE2 below + |U ∩ [0, c(T))|)
  + (e−1)(#NE2 above + u′), since ρ·ℓ(T) ≥ ρ·h_lo and every NE3 below contributes τ_y < c(T) to h_lo.
- Exhaustive e = 5, 6, 7: 0 failures; min slack 22, 29, 50; worst ratio cost/(Peq + |NE2|) is 0.233, 0.302, 0.320
  (C*: 0.267, 0.377, 0.432).

**Conjecture D6 (CONJ; CHECKED e ≤ 8, E383).** On the Q5 residual, Δ₃ ≥ 6·|T∖U| = 6·|NE|.
- Exhaustive e = 5–8: min Δ₃/|NE| = 6.67, 6.30, 6.53, 6.86, flat in e.
- The minimum grows with μ = min A: at e = 8 it is ≥ 9.38 for μ ≥ 6 and ≥ 11.5 for μ ≥ 8.
- D6 ⟹ A1-eT, hence DESC, whenever e(T) ≤ 6, in particular whenever μ ≤ 6, because then
  e(T)·h_lo + h_hi ≤ 6·h ≤ Δ₃.
- Equivalent local form (by the column-top form and OUT): Peq + (e − 5)|NE2| ≥ Σ_{NE3} (6 + π(y)).

**Counting form of PAY2 (PROVED).** Let n₂ (resp. n₂^EQ) be the number of classes at tile level 2 (resp. EQ classes at
level 2, i.e. k_s = 2). Then:

    Δ₃ = e(2e + 1 + n₂) − 3m,
    PAY2 = e(2e + 1 + n₂^EQ − Σ_{y∈NE3} j_y) − 3m + (e−1)·δc.

So PAY2 ⟺ 3m ≤ e·(2e + 1 + n₂^EQ − Σ_{NE3} j) + (e−1)·δc.

- Proof:
  - Levels 0 and 1 hold 1 + d = e classes, every generator being its own level-1 class. So H = d + 2n₂ + 3n₃ with
    m = e + n₂ + n₃, and Δ₃ = 3(e−1)m − eH = e(2e + 1 + n₂) − 3m.
  - Then use n₂ = n₂^EQ + |NE2| and h = |NE2| + Σ_{NE3} j. ∎
- CH′-κ for S is the same inequality with n₂ in place of n₂^EQ − Σ_{NE3} j and without δc. PAY2 trades the NE2 credits
  and one level-2 credit per unit of j on NE3 for the conductor gain.
- **EQ sub-tile (PROVED).** The EQ elements form a down-set D^EQ ⊆ D. Sub-sums of T-Apéry elements are T-Apéry, so a
  sub-vector of an EQ vector has σ = τ.
  - CH′-κ on D^EQ gives Δ^EQ := e(2e + 1 + n₂^EQ) − 3|D^EQ| ≥ 0.
  - Exactly: PAY2 = Δ^EQ + (e−1)δc − 3|NE2| − Σ_{y∈NE3} (e·j_y + 3).
  - Equivalently, Δ^EQ = Peq + 4|NE2| + Σ_{y∈NE3} (3 − π(y)) (boundary columns of D^EQ), which recovers ID-NE.
  - So each NE2 class costs 3, and each NE3 class costs e + 3, against the CH′ slack of the 3-truncated T-tile and
    the conductor gain.

**Lemma J1 (PROVED; supersedes J-BOUND).** On Q5, j_s ≤ 1 for every class s. Hence T∖U = {τ_s : s ∈ NE},
h = |T∖U| = |NE|, and λ_s := h_s + j_s ∈ {3, 4} for s ∈ NE (3 for NE2, 4 for NE3).
- Proof:
  - j_s ≥ 3 is impossible, because σ_s ≤ max σ = 2m + r < 3m. Suppose some class has j_s = 2, and choose one with
    least T-length k := k_s. Then σ_s ≥ 2m, so h_s = 3 and λ_s = 5, i.e. w_s = 5m + τ_s. Also k ≥ 4 (NE-LEVELS (a)).
  - Let z be a least-length T-factorization of τ_s, pick i with z_i ≥ 1, and let t be the class of σ(z − e_i).
    Then z − e_i is a least-length T-factorization of the T-Apéry element τ_t = τ_s − a_i, so k_t = k − 1.
  - The element w_t + (m + a_i) = (λ_t + 1)m + τ_s lies in S and in class s. Since w_s is least in S in its class,
    λ_t ≥ 4.
  - Suppose λ_t = 4. Then w_s = w_t + (m + a_i). A max-length factorization of w_t has h_t generators m + a with
    Σ a = σ_t, so w_s has a factorization of length h_t + 1. Height ≤ 3 gives h_t ≤ 2. Then j_t ≤ 1 (EQ, or
    NE-LEVELS (d)), so λ_t ≤ 3, a contradiction.
  - So λ_t ≥ 5. Since h_t ≤ 3 and j_t ≤ 2, this forces h_t = 3 and j_t = 2. But k_t = k − 1 < k contradicts the
    choice of s. ∎
- Consequences: wherever j appears it may be set to 1. In ID-NE and C*, cost* = Σ_{Ab}(1 + π) + Σ_{NE3∖Ab}(e + π).
  In the counting form, Σ_{NE3} j = |NE3|. The q5ann J2 hard stop (E383f) can never fire.

**Lemma NE3-PRED (PROVED).** Let s ∈ NE3, let z be a least-length T-factorization of τ_s, take i with z_i ≥ 1, and let
t be the class of τ_s − a_i. Then t ∈ NE. If t ∈ NE2, the vector y_t + e_i (y_t := x_t) is a max-length factorization
of w_s. So either y_t + e_i = x_s (the out-edge (y_t, i) is used and counts in π(x_s)), or y_t + e_i ∉ D is a
level-3 collision with x_s (an unused slot at y_t, worth (y_t)_i + 1 in P(y_t)).
- Proof: k_t = k_s − 1 ≥ 4 (NE-LEVELS (e)), so t ∈ NE by NE-LEVELS (a).
- If t ∈ NE2, then by J1 λ_t = 3 and λ_s = 4. So w_t + (m + a_i) = 4m + τ_s = w_s, and y_t + e_i has σ(y_t + e_i) =
  σ_t + a_i = τ_s + m = σ_s with |y_t + e_i| = 3 = h_s. ∎

**Lemma J-BOUND (partial; PROVED; superseded by J1 above).** On Q5, a class with j_s = 2 has τ_s ≤ r and least
T-length k_s ≥ 7.
- Proof:
  - j_s = 2 forces σ_s ≥ 2m, so h_s = 3 and w_s = 5m + τ_s ≤ max w = 5m + r.
  - By NE-LEVELS (c), k_s ≥ λ_s + 1 = 6.
  - If k_s = 6, split a least factorization z into a 4-sub-multiset z⁴ (an NE2 class, w = 3m + σ(z⁴), with a
    factorization of length 2) and a 2-sub-multiset (an EQ class, w = 2m + σ, a factorization of length 2).
  - Their sum lies in S, in class s, and equals 5m + τ_s = w_s. So w_s has a factorization of length 4,
    contradicting height ≤ 3. ∎

### D6 in counting form; the μ-split of W_e(T) and Conjecture MU-LO (2026-10-21)
**Setting.** S ∈ Q5. D is the U-tile in L≤3 := {x ∈ ℕ^d : |x| ≤ 3}. L_k is level k, N_k = |L_k|, N₂ = d(d+1)/2,
N₃ = d(d+1)(d+2)/6. M_k := |L_k ∖ D|. b₂ = |NE2|, b₃ = |NE3|, h = b₂ + b₃. a_k := #{classes of least T-length k}.
For EQ classes x_s is the T-rep, so D ∩ L≤3 ∖ {NE reps} = D^EQ and a₂ = n₂ − b₂, a₃ = n₃ − b₃.

**Identity D3-MISS (PROVED).** Δ₃ = 3M₃ − (e−3)M₂ = 4M₂ + B₂, with B₂ = Σ_{v ∈ L₃∖D} #{i : v − e_i ∈ D, weighted by v_i}.
- Proof: Δ₃ = 2e(e−1) + (e−3)n₂ − 3n₃. Substitute n_k = N_k − M_k and use 2e(e−1) + (e−3)N₂ − 3N₃ = 0. The second form
  is the column-top form: Σ_{u ∈ L₂∖D} Σ_l (u_l + 1) = (e+1)M₂. ∎
- So CH′-κ is the weighted upper-shadow bound 3|∇X| ≥ (e+1)|X| for X = L₂ ∖ D, plus B₂ ≥ 0.

**Equivalent forms of D6 (PROVED equivalences).** Each of the following is equivalent to Δ₃ ≥ 6h:
- (M) M₃ ≥ ((e−3)/3)·M₂ + 2h;
- (m) m + 2h + (e/3)·M₂ ≤ C(e+2, 3) (an upper bound on the multiplicity; C(e+2,3) = |L≤3|);
- (H) 2e(e−1) + (e−3)a₂ ≥ 3a₃ + 9b₃ + (9−e)b₂ (the T-Hilbert function (1, d, a₂, a₃, a₄, …) with its tail
  h = Σ_{k≥4} a_k split into b₂ ≥ a₄ and b₃ ≤ Σ_{k≥5} a_k);
- (J) |J₃| ≥ 3b₃ + (e/3 − 1)(|J₂| − b₂) + 2b₂, with J = T-nonstandard monomials (|J_k| = M_k + b_k).
- Proof: Δ₃ = e(2e + 1 + n₂) − 3m with m = e + n₂ + n₃; substitute. ∎
- (H) is not a Macaulay consequence. The O-sequences H_T = (1, d, N₂ − 1, N₃ − (K−4), 1, …, 1) and
  H_U = (1, d, N₂, N₃) satisfy every numerical constraint above with Δ₃ = 0 and h = K − 3. The arithmetic of the
  U-cover (τ + m ∈ 3A′ for every T-Apéry τ of T-length ≥ 4) has to enter.

**Lemma MU-SPLIT (PROVED; any numerical semigroup T of multiplicity μ, any integer e).**
    e·ℓ(T) − c(T) = (e − μ)·ℓ_μ + e·(ℓ(T) − ℓ_μ) + θ,   ℓ_μ := ⌈c(T)/μ⌉ = |μℕ ∩ [0, c(T))|,   θ := μℓ_μ − c(T) ∈ [0, μ).
- Proof: μℕ ⊂ T, so the multiples of μ below c(T) are left elements. ∎

**Identity W-μ (PROVED; Q5).** Write c_T = c(T), and
- h_lo^μ := |μℕ ∩ (T∖U) ∩ [0, c_T)|, h_hi := |(T∖U) ∩ [c_T, ∞)|;
- U_μ := |μℕ ∩ U ∩ [0, c_T)|, U′ := |(U ∖ μℕ) ∩ [0, c_T)|, u′ := |U ∩ [c_T, c_U)|.
Then

    W(S) = Δ₃ − μ·h_lo^μ − h_hi + (e−1)·u′ + (e−μ)·U_μ + e·U′ + θ.

- Proof: by ID-T and J1, W(S) = Δ₃ − e·h + (e−1)δc + e·ℓ(T) − c(T). Apply MU-SPLIT with ℓ_μ = h_lo^μ + U_μ and
  ℓ(T) − ℓ_μ = (h_lo − h_lo^μ) + U′. Then use δc = h_hi + u′ and h = h_lo + h_hi. ∎
- The NE elements below c(T) that are not multiples of μ cancel exactly: each costs e and is paid e by T's left count.
- Equivalently W(S) = Δ₃ + W_e(U) (ID-U), split along μ.

**Corollary MU-RED (PROVED).** If μ := min A ≤ e, then W(S) ≥ Δ₃ − μ·h_lo^μ − h_hi. So Wilf holds for every
S ∈ Q5 with μ ≤ e that satisfies

    MU-LO:   Δ₃ ≥ μ·h_lo^μ + h_hi,

and this needs no induction on multiplicity.
- D6 implies MU-LO when μ ≤ 6.
- For μ > e the term (e−μ)U_μ is negative; there the descent through W(T) (A1-eT, DESC) is still needed.

**Conjecture MU-LO (CONJ; CHECKED e ≤ 8, E384).** On the Q5 residual with μ ≤ e:
- max (μh_lo^μ + h_hi)/Δ₃ = 0.353, 0.349, 0.387, 0.366 at e = 5–8 (flat), against 0.353, 0.317, 0.394, 0.500 for
  the coarser bonus (e−μ)ℓ(T) (E383g);
- min (Δ₃ − μh_lo^μ − h_hi) = 22, 41, 57, 91.
The extremal shape is the pure ray T∖U = {4μ, …, Kμ} with μ ≈ e (e = 8: m = 61, A = [8,21,37,44,47,49,50]).

**Remark QA-FALSE (the two halves of W-μ are not separately nonnegative).** Write W(S) = Qa + Qb + θ = P1 + Qb with
- Qa := (e−μ)U_μ + e·U′ − μ·h_lo^μ;
- P1 := Qa + θ = e·|U ∩ [0, c_T)| − c_T = W_e(T) − e·h_lo;
- Qb := Δ₃ + (e−1)u′ − h_hi.
Then:
- On the exhaustive residual (e = 5–8), min P1 = 6, 6, 5, 5 (all μ) and min Qa = 5, 6, 4, 4 (μ ≤ e). Also
  min Qb = 40, 35, 82, 113 (all μ) and min (Δ₃ − h_hi) = 30, 35, 81, 113.
- Nevertheless **Qa ≥ 0 and P1 ≥ 0 are FALSE** (FAILED.md, E385). Example: e = 11, μ = 3, m = 85,
  A = [3,46,47,50,52,58,59,65,76,83]. There:
  - c_T = 45, U ∩ [0, c_T) = {0, 3, 6, 9}, and P1 = Qa = −1;
  - W = 677, Δ₃ = 460, Qb = 678, h = 33 (h_lo^μ = 11, h_hi = 22);
  - checked by two independent programs (verifyF0.py, by brute-force factorization lengths; rayU0.evalS).
- The counterexamples lie in **family F0**: A = {μ} ∪ B with B ⊂ [c_T, m) ∖ μℕ ⊇ the non-multiples of μ in [c_T, c_T+μ).
  - There T = μℕ ∪ [c_T, ∞) and U ∩ [0, c_T) = {0, μ, 2μ, 3μ}, so P1 = 4e − c_T.
  - Annealing over B (f0ann.c) shows min |B| growing by about 1 per 4.5 units of c_T: c_T = 33, 44, 45, 47, 50 are reached
    with e = 9, 11, 11, 11, 12.
- The deficit is paid by (e−1)u′ (240 in the example), which is TRUNC₃'s term above c_T. So TRUNC₃ and MU-LO are the
  right granularity; the cut at c_T is not.
- MU-LO on these examples: ratio (μh_lo^μ + h_hi)/Δ₃ = 0.120, 0.124, 0.102.

### Robust forms of MU-LO; the pure ray; what pays (2026-10-21, E386)
**Identity Δ₃-MULT (PROVED).** Δ₃ = 3·(C(e+2,3) − m) − e·M₂.
- Proof: Δ₃ = 3M₃ − (e−3)M₂, and M₂ + M₃ = C(e+2,3) − m (each class has one standard monomial of degree ≤ 3). ∎
- So MU-LO is the multiplicity bound m + (e·M₂ + μh_lo^μ + h_hi)/3 ≤ C(e+2,3).
- In the e = 8 MU-LO extremum (m = 61, A = [8,21,37,44,47,49,50]), Δ₃ = 153 splits as 4M₂ = 12 plus 141 from
  standard squares; 133 of the 141 come from EQ squares.
  - The local collisions that RUN-PAIR forces along the ray give only about 9.
  - So MU-LO is paid by the generic waste of a small m, not by NE-specific collisions.

**Lemma RES-SMALL (PROVED).** On the Q5 residual, some NE2 class has τ = v < m with v + m ∈ 2A; hence 4μ ≤ v < m.
- Proof: NE-LEVELS (f) gives NE2 ≠ ∅. For s ∈ NE2, σ_s = τ_s + m is a 2-sum < 2m, so τ_s < m.
- k_s ≥ 4 gives τ_s ≥ 4μ. ∎
- Consequence: if A ⊆ (m/2, m) then U = T, because every 4-sum is ≥ 2m. Random searches in that regime (tophalf.py,
  e = 6–10) found only U = T, as predicted.

**Lemma RAY-W (PROVED).** Suppose T∖U = {jμ : 4 ≤ j ≤ K} (the pure ray). Put ℓ_μ = ⌈c_T/μ⌉ and θ = μℓ_μ − c_T. Then

    W(S) = Δ₃ + P1 + β,   with β := (e−1)u′ − h_hi ≥ −1,

where β = −1 only if t := K − ℓ_μ + 1 = 1 and θ = 0.
- Proof:
  - If K ≤ ℓ_μ − 1, then c_U = c_T and u′ = h_hi = 0.
  - Otherwise c_U = Kμ + 1, h_hi = t and u′ = (t−1)(μ−1) + θ. Then β ≥ (e−1)(t−1) − t ≥ 0 for t ≥ 2 and e ≥ 3, and
    β = (e−1)θ − 1 for t = 1. ∎
- So pure-ray Wilf (8,044 of the 10,663 residual S at e = 7) needs only Δ₃ + P1 ≥ 1:
  - immediate when P1 ≥ 1 (T-rich; no induction);
  - in the T-sparse case P1 ≤ 0 it needs Δ₃ ≥ |P1| + 1.
- In F0 (P1 < 0 from e = 11) one has Δ₃ ≈ e³/2 against |P1| ≤ 12.

**Conjecture MU-LO′ (CONJ; CHECKED e ≤ 8).** For μ ≤ e:

    Δ₃ + e·U′ + (e−1)·u′ ≥ μ·h_lo^μ + h_hi.

- This is W-μ with only (e−μ)U_μ + θ ≥ 0 discarded, so it implies Wilf for μ ≤ e with no induction.
- Data:
  - max ratio = 0.128, 0.152, 0.150, 0.144 at e = 5–8;
  - min slack = 53, 87, 128, 177.
  For comparison, MU-LO has ratio 0.35–0.39.
- The U′ = 0 slice is easy for Δ₃ alone: MU-LO ratio ≤ 0.200, 0.154, 0.168, 0.138.
- The hard MU-LO cases have large U′ (e = 8 extremum of MU-LO′: m = 52, A = [7,24,31,40,44,47,51], U′ = 29).
- **Two payers:**
  - collisions Δ₃, when T is μ-sparse below c_T (F0);
  - T-density e·U′, when T has many non-multiples of μ below c_T.
  A proof has to interpolate between them.

**Conjectures H1, H2 (CONJ; CHECKED e ≤ 8, μ ≤ e).** H1 and H2 together imply MU-LO′:
- H1: Δ₃/2 + e·U′ ≥ μ·h_lo^μ. Max ratio 0.175, 0.231, 0.232, 0.262 (slowly rising).
  - The e = 8 extremum is F0-like: m = 59, A = [4,33,37,39,42,47,54], U′ = 2.
  - In F0 at e = 11–15 the MU-LO ratio is ≤ 0.12.
- H2: Δ₃/2 + (e−1)·u′ ≥ h_hi. Max ratio 0.120, 0.092, 0.090, 0.089.
  - H2 follows from D2 (Δ₃ ≥ 2h), whose margin is 3.4× at e = 8.
- The interval form LOC (|I| − e|U ∩ I| ≤ Δ₃/2 for every interval I ⊆ [0, c_U)) contains H1/H2-type cuts.
  - But its maximizer is the initial gap [1, μ) (max ratio 0.118, 0.222, 0.151, 0.172), which is irrelevant to Wilf.
  - So only the two cuts [0, c_T) and [c_T, c_U) are kept.

**Conjecture CU (CONJ; CHECKED on the residual, e ≤ 8).** Δ₃ ≥ c_U − 3μ.
- CU implies MU-LO for μ ≤ e, since μh_lo^μ + h_hi ≤ c_U − 3μ. It has no NE or T terms.
- Max ratio (c_U − 3μ)/Δ₃ = 0.618, 0.759, 0.855, 0.802 at e = 5–8 (residual). The q5annCU annealer (all Q5) found
  0.852 on U = T at e = 7.
- Extremal family L_k: A = {3} ∪ {3 + 15j : 1 ≤ j ≤ k} ∪ {m−8, m−6, m−5}, m = 15k + 17.
  - Ratio 0.759, 0.855, 0.802, 0.716, 0.634, 0.563, 0.505, 0.456 for k = 1–8 (famL.py); it peaks at k = 2 because Δ₃
    grows quadratically and c_U linearly.
- C1 (Δ₃ ≥ (c_T − 3μ)⁺ + h_hi) has the same maxima.
- Risk: by Δ₃-MULT, CU can fail only if m ≳ 0.6·C(e+2,3) with c_U ≈ 2m.

**Observation A1 for μ > e.** Δ₃ ≥ e·h_lo + h_hi restricted to μ > e:
- max ratio 0.317, 0.308, 0.500 at e = 6, 7, 8;
- e = 8 extremum: m = 62, A = [12,13,36,46,48,56,57].
This is the induction-based half of the split (MU-LO′ for μ ≤ e, A1 for μ > e).

**Charging flows (flowdiv.py).**
- Supply: P(x) on standard squares and 4 per missing square (exactly Δ₃).
- Demand: μ per NE multiple of μ below c_T (μ ≤ e), e per NE below c_T (μ > e), 1 per NE above c_T.
- R = 1 (an NE3 class draws only from the square divisors of its rep) fails: 1 / 22 and 29 / 454 at e = 5, 6.
  - Typical failure: the NE2 class 21² spends its P = e on itself while its NE3 child 5 + 21² needs μ more.
- R = 2 (any square sharing a variable with the rep) saturates on every residual S at e ≤ 8 (269,663 at e = 8).
  - By Hall this is equivalent to the V-local inequalities Σ_{s: supp x_s ⊆ V} dem(s) ≤ Σ_{squares meeting V} cap,
    for every V ⊆ A.

### ZW: Wilf on Q5 from the covering set alone (2026-10-21, E387) [SCOPE: Q5 only; no reduction to all S; NOT a target]
Notation: z := #{s : σ_s < m} = |3A′ ∩ [0, m)|.

**Lemma ZW-RED (PROVED).** On Q5, W(S) ≥ Δ₃ + e·z − c_U ≥ Δ₃ + e·z − 2m.
- Proof: ID-U gives W = Δ₃ + e·ℓ(U) − c_U, and Lemma C>M gives ℓ(U) = z + r + 1 − t ≥ z. Also c_U = m + r + 1 ≤ 2m. ∎
- So Wilf on all of Q5, residual or not, needs no induction given:
  - **Conjecture ZW:** Δ₃ + e·z ≥ c_U;
  - or **Conjecture ZW2:** Δ₃ + e·z ≥ 2m.
- ZW discards only e·|U ∩ [m, c_U)|.

**Identity PAIR (PROVED; asserted by zwid.py on every residual S, e ≤ 7).** Let Z be the small classes and map
Z × A → ℕ by (t, a) ↦ σ_t + a. Put:
- N_< := #pairs with value < m;
- N_ns := #pairs with value v ≥ m but v ≠ σ_{v mod m};
- for each large class s (σ_s ≥ m), hit(s) := #pairs with value σ_s; Ov := Σ_s (hit(s) − 1)⁺;
- Q′ := large classes with hit(s) = 0.
Then e·z − m = N_< + N_ns + Ov − |Q′|. Hence ZW ⟺ Δ₃ + N_< + N_ns + Ov ≥ (c_U − m) + |Q′|.
- Proof: count the (e−1)·z pairs by where they land. ∎

**Lemma DOM (PROVED).** Let v be a sum of four elements of A.
- If m ≤ v < 2m, then σ_{v−m} ∈ {v − m, v}: either v − m ∈ Z, or v is itself a ≤3-sum standard in its class.
- If v < m, then v ∈ Z, or σ_v = v + m with h_v = 2 (NE2).
- Proof: 4m + v ∈ S lies in class v mod m, so w ≤ 4m + v. Height ≤ 3 forbids equality. Hence h·m + σ < 4m + v with
  h ≤ 3. Here σ = v + m (≥ 2m) needs h = 3 and gives equality, and σ ≥ 3m is impossible. ∎
- For v ≥ 2m there is no constraint, since 4m + v ≥ 6m > max w.

**Per-class form of ZW2 (PROVED).** Δ₃ + e·z − 2m = Σ_s φ(s), with
- φ = 4e − 5 (level 0) and 3e − 5 (level 1);
- φ = 2e − 5 (level 2, σ < m);
- φ = e − 5 (level 2 with σ ≥ m, or level 3 with σ < m);
- φ = −5 (level 3 with σ ≥ m).
So ZW2 says 5·L₃ ≤ 3e² − 4e + (2e−5)·S₂ + (e−5)·(L₂ + S₃), with S/L = small/large and the index = level.
Checked by zw2cls.py.

**Data (E387, exhaustive residual).**
- ZW: 0 failures at e ≤ 8.
  - Max (c_U − e·z)/Δ₃ over all μ: −0.118, 0.033, 0.202, 0.299 (rising). The extremals have μ ≈ 2e > e.
  - Restricted to μ ≤ e: −0.118, −0.100, 0.031, 0.053. e·z ≥ c_U alone fails on only 0, 0, 2, 7 of these S.
- ZW2: 0 failures. Min slack 30, 32, 68, 82 (all μ) and 30, 55, 87, 132 (μ ≤ e).
- Z1 (e·z ≥ m): 0 failures, min slack 18, 18, 22, 18.
- Pieces of PAIR (μ ≤ e):
  - Δ₃ ≥ |Q′| always (slack ≥ 29, 46, 70);
  - N_< + Ov ≥ (c_U − m) + |Q′| fails 0, 2, 26 times.
  So the deficit c_U − m needs N_ns or Δ₃.
- The threatening regime (A = {μ} ∪ B, B Sidon-like in (m/2, m), m ~ e³) is excluded by DOM. zwthreat.py found
  323 non-Q5 hits against 5 residual Q5 hits, all with ZW slack ≥ 334.
- Z1 cannot hold on non-residual Q5 for large e (A ⊂ (m/2, m) gives z = e), so a proof must use the residual
  (RES-SMALL).

**Conjecture MURUN (CONJ; CHECKED e ≤ 8).** Δ₃ ≥ μ·R₀ + h, where R₀ := |μℕ ∩ (T∖U)|. It implies MU-LO, since
h_lo^μ ≤ R₀ and h_hi ≤ h − h_lo^μ.
- max (μR₀ + h)/Δ₃ = 0.706, 0.571, 0.638, 0.704 at e = 5–8, over all μ (μ ≤ e: 0.706, 0.571, 0.593, 0.535).

**Conjecture WRAPM (CONJ; CHECKED e ≤ 7).** #{v ∈ L₃ : σ(v) ≥ σ_{class(v)} + m} ≥ h.
- Equality occurs (e = 5: m = 20, A = [3,7,14,18]; e = 6: m = 34, A = [5,7,19,26,28]; e = 7: m = 28,
  A = [3,8,11,16,19,24]).
- The value version (distinct wrap values ≥ h) is FALSE (FAILED.md).
- In the e = 7 equality case every wrapping cube has σ ≥ 2m, and the count is #{v ∈ L₃ : σ(v) ≥ 2m} − 1.

**Lemma RUN-PAIR (PROVED).** Let s, s′ = s + μ be NE classes with τ_{s′} = τ_s + μ, and U-reps x, x′, so that
σ(x′) = σ(x) + μ.
- (a) If |x| = 2, then x + e_1 is either x′ or a missing level-3 monomial with value σ(x′).
- (b) If |x| = |x′| = 3 and j ∈ supp x ∩ supp x′, then x − e_j + e_1 is a missing level-3 monomial with value
  σ(x′ − e_j).
- (c) If s is the last class of its run (τ_s + μ ∈ U) and |x| = 2, then x + e_1 is a missing level-3 monomial with
  σ ≥ σ_{class} + m.
- Proof:
  - (a) Both monomials have value σ(x′), and D has one element per class.
  - (b) x − e_j has level 2, and x′ − e_j ∈ D is the class rep of value σ(x′ − e_j). If x − e_j + e_1 = x′ − e_j, then
    x′ = x + e_1 has level 4.
  - (c) τ_s + μ ≥ σ_{class}, so σ(x) + μ = τ_s + μ + m ≥ σ_{class} + m. ∎
- In case (b) with disjoint supports no collision is forced. Example: e = 8, m = 54, 33+33+41 → 18+44+52. There the
  collision 7+33+41 = 29+52 comes from the level-2 relation 18+44 = 29+33.

### The height split of W on Q5: W = Δ₃ + [e·z − (m − t)] + [(e−1)(r+1) − (e+1)t] (2026-10-21, E388) [SCOPE: Q5 only; no reduction to all S; NOT a target]
Notation (S ∈ Q5): for a class c ∈ [0, m) put η(c) := ⌊σ_c/m⌋ ∈ {0, 1, 2}.
- Z := {c : η = 0} (so z = |Z|), M₁ := {c : η = 1}, M₂′ := {c : η = 2}, t := |M₂′|.
- max σ = 2m + r, and r is itself the class of max σ (Lemma C>M). U = {x : x ≥ σ_{x mod m}}.

**Lemma U-CLOSE (PROVED).** If x ∈ U, x ≥ m and a ∈ A, then x + a ∈ U.
- Write x = σ_s + km and v := σ_s + a, a ≤4-sum in class s + a.
- If h_s ≤ 2, v is a ≤3-sum, so σ_{s+a} ≤ v and x + a ∈ U.
- If h_s = 3, height ≤ 3 gives w_{s+a} ≤ 3m + v, i.e. h′m + σ′ ≤ 3m + v for (h′, σ′) of class s + a.
  - If v ≥ m: h′ = 3 gives σ′ ≤ v. For h′ ≤ 2, σ′ < 2m ≤ v + m, and σ′ ≡ v forces σ′ ≤ v.
  - If v < m: k ≥ 1 because x ≥ m, and σ′ ≤ v + m (h′ ≥ 2) or σ′ = v (h′ ≤ 1). So v + m ∈ U and x + a ∈ U. ∎

**Lemma DOWN (PROVED).** If h_s = 3 and a ∈ A, then σ_{s−a} ≥ σ_s − a.
- Proof: u := σ_{s−a} + a is a ≤4-sum in class s.
  - If h_{s−a} ≤ 2, u is a ≤3-sum, so u ≥ σ_s.
  - If h_{s−a} = 3, height ≤ 3 gives 3m + σ_s = w_s ≤ 4m + u − m. ∎

**Lemma M2-DOWN (PROVED).**
- 0 ∉ M₂′ ⊆ [1, r].
- If c ∈ M₂′ and a ∈ A with a ≤ c, then c − a ∈ M₂′.
- Consequences: M₂′ ∩ T = ∅, and r − (T ∩ [0, r]) ⊆ M₂′, so |T ∩ [0, r]| ≤ t ≤ r + 1 − |T ∩ [0, r]|.
- Proof: if c − a ∉ M₂′, then c − a + m ∈ U and U-CLOSE gives c + m ∈ U, so σ_c ≤ c + m. ∎

**Lemma Q′-CLASS (PROVED; asserted by qsrc.py, qsplit.py on every residual S at e ≤ 7).** Q′ := {large s : σ_s − a ∉ Z
for all a ∈ A} (Identity PAIR) equals ℤ_m ∖ (Z + A′) as a set of residues. Moreover:
- **M₂′ ⊆ Q′.**
- Q1 := Q′ ∖ M₂′ = Q′ ∩ M₁ consists of level-3 classes with σ ∈ [3m/2, 2m) whose rep has all three pairwise sums ≥ m.
Proof:
- Q′ is contained in the level-3 large classes: a large level-2 class with rep (i, j) has σ − a_i = a_j ∈ Z.
- For a level-3 s ∈ Q′ and a ∈ A: if σ_s − a ≥ m, DOWN gives σ_{s−a} ≥ m. If σ_s − a < m, it is not in Z, and DOWN gives
  σ_{s−a} ≥ σ_s − a + m ≥ m. Either way s − a is large, so s ∉ Z + A′. The converse is immediate.
- M₂′ ⊆ Q′: let c ∈ M₂′ with c ≡ z′ + a, where z′ ∈ Z and a ∈ A.
  - If z′ + a < m, then c − a = z′ ∈ Z, against M2-DOWN.
  - If z′ + a ≥ m, then z′ + a = c + m is a ≤4-sum ≥ m in class c. U-CLOSE (case v ≥ m) gives σ_c ≤ c + m < 2m.
- Q1: the rep of s ∈ Q′ ∩ M₁ is a cube with every σ_s − a_i ≥ m, and its pairwise sums add to 2σ_s ≥ 3m. ∎

**Identity SPLIT (PROVED; asserted with W computed from the Apéry set by idq.py on all 280,326 residual S, e = 5–8).**

    W(S) = Δ₃ + [e·z − (m − t)] + [(e−1)(r+1) − (e+1)·t]
         = Δ₃ + (e·z + t − m) + (e−1)(r + 1 − t) − 2t.

- Proof: c(S) = 4m + r + 1 and g(S) = Σ(h_s + η_s) = Σh_s + m − z + t. Substitute into W = (e−1)c − e·g and subtract
  Δ₃ = 3(e−1)m − eΣh_s. ∎
- With Identity PAIR and Q′-CLASS: e·z + t − m = N_< + N_ns + Ov − |Q1|.
- r + 1 − t = |[0, r] ∖ M₂′| ≥ |T ∩ [0, r]| ≥ 1.

**Lemma ZT-RED (PROVED; asserted by zttest.py).** W ≥ Δ₃ + (e·z − m) + (e·|T ∩ [0, r+1)| − (r+1)).
- Proof: SPLIT with r + 1 − t ≥ |T ∩ [0, r]|. Equivalently, by J1, m + T ⊆ U.
- **ZM-RED.** If μ ≤ e, then W ≥ Δ₃ + e·z − m ≥ Δ₃ − |Q′| = Δ₃ − t − |Q1|.

**Conjecture ZT1 (CONJ; CHECKED, exhaustive residual e ≤ 8).** e·z ≥ m − t, i.e.

    #{s : m ≤ σ_s < 2m} ≤ (e − 1)·#{s : σ_s < m}.

- Pair form: every pair (z′, a) ∈ Z × A has value < 2m. It lands below m (N_<), on Z + m, or exactly on σ of an
  M₁ class. So ZT1 ⟺ |Q1| ≤ N_< + #{pairs on Z + m} + Σ_{c∈M₁}(hit(c) − 1)⁺.
- Data: min slack 19, 25, 32, 36 at e = 5–8 (rising). It also holds on U = T at e = 6 (annealer min 5).

**Conjecture TRΔ (CONJ; CHECKED, exhaustive residual e ≤ 8).** Δ₃ + (e−1)(r + 1 − t) ≥ 2t, i.e. E ≤ Δ₃ with
E := (e+1)t − (e−1)(r+1).
- Max E/Δ₃ = −0.047, −0.036, 0.000, 0.019 at e = 5–8.
- Sufficient: Δ₃ ≥ 2t. Max 2t/Δ₃ ≈ 0.37 at e = 7.
- The pure form TR (E ≤ 0) is FALSE (FAILED.md "TR").

**ZT1 + TRΔ ⟹ Wilf on Q5, for every μ and with no induction** (by SPLIT, since Δ₃ ≥ 0 is proved).

**Data (E388).**
- Max |Q′|/Δ₃ (exhaustive residual):
  - μ ≤ e: 0.147, 0.150, 0.157, 0.143 at e = 5–8 (flat);
  - μ > e: 0.167, 0.194, 0.209 at e = 6–8.
- Annealing at e = 10: |Q′|/Δ₃ ≤ 0.082 (μ ≤ e).
- Q2 = M₂′ on every S. |Q1| ≤ 9, and min (N − |Q1|) = 19, 25, 32, 36.
- Payment of Q′ is not local: 3P(x) ≥ c(x) per standard square fails on 16 / 454 and 88 / 10,663 S. Globally the large
  squares' missing children P_L pay |Q′| with ratio ≤ 0.29.

**Identity SPLIT-Q3 (PROVED; asserted by q3t.py on all 280,326 residual S, e = 5–8, with W from the Apéry set).**
Let D be the tile and D_s its small part (σ < m, so |D_s| = z). Classify the (e−1)z pairs (x, l) ∈ D_s × [1, e−1]:
- N_<: σ(x) + a_l < m;
- n₂: x + e_l ∈ D, which forces σ ∈ [m, 2m);
- n₃: the rest.
For c ∈ M₁ put hit(c) := #{distinct parts l of rep(c) with a_l > c}, i.e. the parts whose removal leaves a small monomial.
Then n₂ = Σ_{c∈M₁} hit(c). Let Q1′ := {c ∈ M₁ : hit(c) = 0} and ov := Σ_{c∈M₁} (hit(c) − 1)⁺. Then:
- e·z + t − m = N_< + n₃ + ov − |Q1′|;
- **W = (Δ₃ − |Q3| − t) + N_< + n₃ + ov + (e−1)(r + 1 − t)**, where Q3 := Q1′ ⊔ M₂′ is the set of level-3 classes whose
  rep has all three pairwise sums ≥ m. (Every M₂′ rep has this property: a part < m and value ≥ 2m.)

**Conjecture Q3T (CONJ; CHECKED, exhaustive residual e ≤ 8).** On the Q5 residual, Δ₃ ≥ |Q3| + t. Equivalently

    3n₃ + |Q3| + t ≤ 2e(e − 1) + (e − 3)·n₂.

- By SPLIT-Q3, **Q3T ⟹ Wilf on Q5, for every μ and with no induction.**
- Data: max (|Q3| + t)/Δ₃ = 0.294, 0.300, 0.376, 0.390 at e = 5–8 (μ ≤ e: 0.294, 0.267, 0.289, 0.284). Min slack
  24, 29, 57, 81. e = 8 extremum: m = 64, A = [15,29,43,58,59,61,63], Δ₃ = 136, |Q3| = 27, t = 26.
- It fails on U = T: the annealer found ratio 1.08 at e = 6, ⟨40,65,67,72,73,78⟩. So a proof must use the residual
  (RES-SMALL, DOM). U = T is covered by PAY2 = (Δ₃ ≥ 0) and induction.
- The crude forms Δ₃ ≥ 2n₃ and Δ₃ ≥ 2L₃ are FALSE (FAILED.md "N3"). Δ₃ ≥ L₃ + t holds at e ≤ 7 with ratio ≤ 0.61.
- Sub-route: ZT1 ⟸ Q1R (|Q1′| ≤ N_< + ov; min slack 11, 13, 16 at e = 5–7). Q1N (|Q1′| ≤ N_<) has slack 8, 7, 7, 4 and
  is too lossy.

**Conjecture K2 (CONJ; CHECKED, exhaustive residual e ≤ 8).** On the Q5 residual, K₂ ≥ 2t, where K₂ := #{3-multisets of
A with sum ≥ 2m}.
- Min K₂ − 2t is 0 at e = 5, 7 and 8, so equality occurs.
- The tight cases have t = 1, K₂ = 2 and 3a_max = 2m + 1, 2a_max + a_{max−1} = 2m. Examples: m = 52,
  A = [4,20,23,28,31,34,35]; m = 46, A = [3,15,18,25,27,30,31].
- Use for Q3T:
  - Δ₃ ≥ 4M₂ + Σ_{y ∈ K∖R} w_D(y), where R is the set of reps of M₂′ and w_D(y) is the weighted number of standard
    parents of y.
  - If no large square is missing, then w_D = 3 on K, and K2 gives Δ₃ ≥ 3(K₂ − t) ≥ 3t.
  - The weighted form "missing wrap slots ≥ 2t" is FALSE (38 S at e = 7–8, min −6; e = 7: m = 34,
    A = [3,15,18,27,30,31]), because missing large squares lower w_D. Their 4M₂ has to be used.
- **Fact (PROVED), the step behind K2 when t = 1.** If t = 1 (so M₂′ = {r} and r < μ by M2-DOWN), then for every
  a ∈ A the class r − a + m has σ = σ_r − a exactly.
  - Proof: DOWN gives σ ≥ σ_r − a; σ < 2m since the class is not in M₂′; and 2m + r − a is the only value in
    [2m + r − a, 2m) congruent to r − a. ∎
  - Hence, if some σ_r − a with a ∉ parts(y_r) is a square value x, then x + e_a is a second cube ≥ 2m in class r.

**Refined target QE.** By SPLIT, W = Δ₃ + (e·z + t − m) + [(e−1)(r+1) − (e+1)t] and e·z + t − m = N_< + n₃ + ov − |Q1′|.
So Wilf on Q5 follows from Δ₃ ≥ |Q1′| + E⁺ with E := (e+1)t − (e−1)(r+1). This is weaker than Q3T, since E ≤ 2t.
- E > 0 needs t > (e−1)(r+1)/(e+1), so |I ∩ [0, r]| < 2(r+1)/(e+1). In particular μ > (e+1)/2 or r < μ.
- For μ ≤ (e+1)/2, E ≤ 0 is PROVED: |T ∩ [0, r]| ≥ ⌈(r+1)/μ⌉, and r + 1 − t ≥ |T ∩ [0, r]|. The target is then only
  Δ₃ ≥ |Q1′| (data: |Q1′|/Δ₃ ≤ 0.1).

**Charging form of Q3T (CHECKED; sibflow.py).** Demand is 1 per Q1′ class and 2 per M₂′ class, a total of |Q3| + t.
Supply is the missing slots (x, l) of standard squares (capacity x_l + 1) and the missing squares (capacity 4); the total
supply is Δ₃.
- **SIB3** lets a Q3 class with rep y draw from slots of any square x with supp x ∩ supp y ≠ ∅, and from missing squares
  meeting supp y. It saturates on every residual S at e = 5, 6, 7 (22 / 454 / 10,663). e = 8 is running.
- By Hall, SIB3 ⟺ the **V-local Q3T inequalities**: for every V ⊆ [d],

      Σ_{s ∈ Q3, supp y_s ⊆ V} dem(s) ≤ Σ_{std squares x meeting V} P(x) + 4·#{missing squares meeting V}.

  V = [d] is Q3T itself.
- Narrower rules fail:
  - SIB (only slots of the parents of y): 7 / 454 and 41 / 10,663;
  - SIB2 (SIB + missing squares meeting y): 1 / 454 (m = 40, A = [9,14,23,25,38]) and 1 / 10,663.
- Class-local payment fails badly (classmate.py). Most Q3 classes contain no other cube monomial with a standard parent:
  7,712 / 10,663 S at e = 7 have such a class. Δ₃ pays Q3 through other classes.

## Upper-side closure and exact repair form of UA3 (2026-10-22; PROVED, E390)

**Scope:** every numerical semigroup with c > m; no height, depth or embedding-dimension restriction.
This is a lower-bound computation and an exact reformulation of the existing UA3 certificate, not a proof of
its universal nonnegativity. Novelty is not claimed. It provides a proved filter for the full backwards search.

Use the notation of TYPE / UA3. For every tight pair p = (i,j -> s), set
L_p = q - lo_p, U_p = q + up_p, with the typed allowances lo_p, up_p in {0,1}.
Let A_p z = z_i + z_j - z_s. Let G be the nonzero generator residues. In increasing order of w_s define

    b_g = mu_g                          (g in G),
    b_s = max(0, max_{p -> s}(b_i + b_j - U_p))  (s not in G).

Put b_0 = q and B(S) = e sum_{s=0}^{m-1} b_s - c.

**Proposition (upper-side closure).**
1. b is the coordinatewise least vector satisfying z >= 0, z_g = mu_g, A_p z <= U_p on every tight pair.
2. Every b_s is integral, 0 <= b_s <= mu_s, and B(S) <= UA3(S) <= W(S).
3. Consequently any counterexample to Wilf must have B(S) < 0. B >= 0 is already a complete certificate
   for that S; proving the remaining B < 0 case would cover all S, not merely a chosen family.

*Proof.* In a tight pair w_i,w_j < w_s, so the recurrence is acyclic. Each constraint is
z_s >= z_i + z_j - U_p. Induction in increasing w shows that every feasible z dominates b.
The recurrence itself satisfies each such inequality, and generator residues have no incoming tight pair;
thus b is feasible and least. The data are integral. The true mu is feasible by TYPE, so b <= mu.
UA3 adds the lower inequalities A_p z >= L_p and hence its minimum is at least B. Its feasible point mu
has objective W. The final assertion follows immediately. QED.

The recurrence is O(m + number of tight pairs) once the ordered Apéry set and incoming-pair lists are known.
It is also the exact minimum of the generator-aware certificate restricted to upper-side rows, with all
other dual multipliers zero. A dual can be constructed without an LP: process non-generator cells in decreasing
w; at b_s > 0 choose a maximizing parent pair, send that cell's objective mass to the two parents, and use
the negative of that mass as the upper-row multiplier. Zero cells retain nonnegative reduced costs; generators
use their fixed-level equality multipliers. This is the usual backwards substitution on the acyclic inequalities.

**Proposition (repair form, exact).** Define d_p = L_p - A_p b and u_p = U_p - A_p b >= 0. Then

    UA3(S) = B(S) + e * min sum_{s != 0} t_s,
    subject to t >= 0, t_g = 0 (g in G), d_p <= A_p t <= u_p (every tight pair).

*Proof.* Every UA3-feasible y dominates b by part 1, so set t = y - b >= 0. Substitution gives exactly the
stated inequalities and objective. Conversely such a t gives a UA3-feasible y = b+t. The true vector mu-b
is an integral feasible repair, so the repair LP is nonempty. QED.

**What this does and does not isolate.** For B < 0, a sufficient missing lemma is
min sum t >= -B/e. This is equivalent to UA3 >= 0 on the residual, still stronger than Wilf and unproved.
For the actual semigroup W = B + e sum(mu-b), exactly. No finite check establishes either universal inequality.

**The upper-side-only universal positivity claim is FALSE.** S = <20,21,22> has c=200, g=100, e=3,
q=10, rho=0, W=100, but sum b=60 and B=-20. Full RT3=UA3=TX=AM3=FACE=100, all optima certified
by rational primal/dual checks and the invariants reconstructed independently by membership (E390).
Thus discarding all lower-side split constraints fails even on a genuine S in c > 4m, 3e < m.
This example is in the known e=3 Wilf case; it refutes the certificate shortcut, not Wilf.

### Assignment correction to upper-side closure (2026-10-22; PROVED)

Keep the preceding notation. Let V be the non-generator nonzero residues (|V|=m-e). For each tight pair
p=(i,j -> s) with positive repair demand d_p=L_p-A_p b, form a constraint on V as follows:
- i,j in V: t_i+t_j >= d_p, with multiplicity 2 if i=j;
- one part a in V, the other a generator: 2t_a >= 2d_p;
- two generator parts cannot have positive demand, since b_g=mu_g and b_s<=mu_s.
These constraints follow from A_p t>=d_p by dropping the nonnegative t_s from the right side.

Make a symmetric nonnegative integer matrix H on V. For two distinct parts use H_ij=H_ji=max d_p over
that part pair; for a repeated part use H_ii=max d_p; for one variable and one generator also impose
H_aa>=2d_p. Zero entries impose only t_i+t_j>=0. Let

    M = max_{permutations pi of V} sum_i H_{i,pi(i)}.

**Theorem (general certificate bound).**

    W(S) >= B(S) + e ceil(M/2),
    UA3(S) >= B(S) + e M/2.

*Proof.* Every feasible repair satisfies t_i+t_j>=H_ij. Summing the |V| inequalities indexed by any
permutation pi gives 2 sum_i t_i >= sum_i H_{i,pi(i)}. Maximize over pi and substitute the exact repair
form of UA3. For the actual repair t=mu-b, sum t is integral, giving the rounded W bound. QED.

The assignment is an exact solution of the relaxed repair problem that keeps only these pair-cover constraints.
Indeed, assignment dual potentials alpha_i+beta_j>=H_ij with total M give a feasible pair cover
v_i=(alpha_i+beta_i)/2: it is nonnegative by H_ii>=0, and symmetry of H gives v_i+v_j>=H_ij.
Its total is M/2, matching the preceding lower bound. Thus it suffices to export/check a permutation and
integer assignment dual potentials of equal value; no floating-point LP is involved in this correction.

**Necessity audit.** The bound retains the upper-side generator-aware closure and one optimal fractional
packing of lower-side repair demands. It discards the target-repair charges t_s and all upper residual
capacities u_p. Its nonnegativity is NOT established universally. A failure refutes this restricted
certificate only. Any counterexample to Wilf must make this corrected bound negative, so searching that
residual is justified by a proved reduction from the full target.

**Verified example (E392).** S=<64,67,69,77,129>, c=448,g=265,e=5,q=7,rho=0,height=7,W=467.
The baseline is B=-33. Assignment M=152 gives W>=-33+5*76=347. The full UA3=AM3=452, and TX=FACE=467.
All five LP optima and the semigroup invariants were independently certified; a separate integer checker verifies
H, the assignment/permutation, both assignment dual potentials and equality of primal/dual objectives.
For <20,21,22>, B=-20,M=80, the correction gives exactly W>=100, equal to W and UA3.

### BASE-family deflation: the previously conditional Kunz step is automatic (2026-10-22; PROVED on paper)

This closes condition (b) in the BASE-family corollary of DESCENT above. It is an ingredient in the universal
counterexample analysis, not a replacement research target: the general S outside this profile remain open.

Assume precisely BASE-FAMILY: graded Apéry height <=3, a factorization tile containing every quadratic monomial,
all generators HIGH, mu_g=(2q+1)/3, every quadratic relation tau=+1, and every cubic Apéry element has mu=0.
Write q=3k+1, k>=1, g_i=km+a_i with 1<=a_i<=r, where r is the conductor residue, so

    c=3km+r+1,       max Ap=(3k+1)m+r.

Let T=<m,m+a_1,...,m+a_d>. Then T has the same factorization tile, with

    w'_s = w_s-(k-1)m h_s,
    e(T)=e(S),       c(T)=3m+r+1 <=4m,
    W(S)=W(T)+3(k-1)(binom(d+3,3)-m) >=0.

*Proof.* A quadratic cell has mu=k by Lemma K and tau=1. Writing its offset sum as a_i+a_j gives

    r < a_i+a_j <= m+r.

In particular, all squares being present implies 2a_i>r for every i. A cubic Apéry cell has mu=0, so its offset
sum is also in (r,m+r], from c<=w_s<=c+m-1. The deflated candidates therefore have these upper bounds:

    degree 1: w'<=m+r;    degree 2: w'<=3m+r;    degree 3: w'<=4m+r.

Every a_i>r/2. Thus a competing sum of h>j non-m generators, where the candidate has degree j=1,2,3,
is strictly above that candidate: for j=1, any h>=2 has value >2m+r; for j=2, any h>=3 has value >3m+r;
for j=3, any h>=4 has value >4m+r. The same bounds handle sums of still greater length.

A competing shorter-degree sum that was smaller after deflation would also be smaller before deflation,
since lifting adds (k-1)m per summand; this contradicts the original Apéry minimality. For equal degrees,
the comparison is unchanged. Hence each candidate remains the least non-m-generated value of its residue.
Adding copies of m cannot improve a residue minimum. The candidates form a complete residue system, so they
are exactly Ap(T,m). This proves all Kunz inequalities of the deflated set, without assuming condition (b).

Every m+a_i lies in (m,2m), hence is primitive in T. Since max Ap has mu=0 whereas the generator and quadratic
levels are positive, a cubic exists and attains max Ap. The degree-three candidates dominate degrees one and two,
so their same largest offset sum gives max Ap(T,m)=4m+r and c(T)=3m+r+1.
Let P=binom(d+1,2), C=m-1-d-P, H=d+2P+3C. Then g(S)-g(T)=(k-1)H, and

    W(S)-W(T)=(k-1)(3(e-1)m-eH)
             =3(k-1)(binom(d+3,3)-m).

The final parenthesis is nonnegative because the tile is a subset of all monomials of degree <=3.
Wilf for T follows from the previously kernel-checked c<=4m theorem. QED.

**Literature comparison.** Bacher v9 section 4.3 studies forward inflation
<m,Gamma>_c -> <m,Gamma+m>_{c+hm} for h-regular truncations (Lemma 4.7). The present argument supplies the
inverse Apéry-minimality step under the exact BASE hypotheses, allowing missing cubic monomials; it does not
assert an arbitrary inverse to Bacher's construction. No novelty claim is made beyond closing this project's
previously explicit proof obligation. This does not prove RT3/UA3 nonnegativity for general S.

For this genuine BASE profile, the upper closure is exactly mu: generator values are fixed, every quadratic
upper row has its exact tau=+1 and yields b_p=k, and every cubic has b_s=0. Thus B=W and M=0. The deflation
argument proves the matching criterion nonnegative on that profile, rather than merely certifying W by an
unrelated bound. Fractional BASE-shaped optima at non-BASE semigroups are not covered by this observation.

**Lean status of the matching component (E394).** `lean/Wilf/RepairMatching.lean` kernel-checks
`Wilf.assignment_repair_sum_bound` (the real-valued permutation sum inequality) and
`Wilf.rounded_assignment_repair_bound` (the integer rounding implication), Lean4.33.1 with the project's Mathlib.
Both depend only on propext, Classical.choice and Quot.sound. The semigroup construction of b/H and the BASE
deflation theorem have NOT been formalized here. Thus these component checks do not constitute a Lean proof
of the full semigroup certificate or of Wilf. Reproduce on fejer from ~/wilf/lean with
`~/.elan/bin/lake env lean ../p39/RepairMatching.lean`; the exact source is also saved under lean/Wilf/ locally.

### Exact unit-penalty description of upper closure (2026-10-22; PROVED on paper, E396)

This is an ingredient in the universal backwards target, with the same unrestricted semigroup scope as the
upper-closure theorem. Keep its notation and let kappa_p = up_p - tau_p for a tight pair p. TYPE and WINDOW
give kappa_p in {0,1}: tau=-1 forces up=0; tau=1 forces up=1; tau=0 allows either.
Define D_g=0 at non-m generators and, in increasing Apéry value, define

    D_s = min_{tight i+j -> s} (D_i+D_j+kappa_p).

Then, writing h_min(s) for the minimum number of non-m generators in a factorization of w_s,

    b_s = max(0, mu_s-D_s),
    delta_s := mu_s-b_s = min(mu_s,D_s),
    0 <= D_s <= h_min(s)-1                 (s != 0).

Set D_0=delta_0=0 and b_0=mu_0=q. Equivalently, D_s is the minimum sum of zero-or-one penalties over all
tight binary factorization trees of w_s. This does not require equal factorization lengths or uniqueness.

*Proof.* Induct in w_s. For a tight pair, the exact level identity gives

    (mu_i-D_i)+(mu_j-D_j)-(q+up_p)
      = mu_s-(D_i+D_j+kappa_p).

Taking positive parts at the two parents does not change the positive part of this expression. If a parent
is clipped to zero, the other parent's b is at most mu_j<=q-1, while q+up_p>=q, so the candidate remains
negative. If neither is clipped the equality applies directly. Maximizing the recurrence for b proves the
formula. Any minimum-length factorization has a tight binary tree: each proper partial sum is Apéry, since
otherwise subtracting m there would subtract m from w_s. Its h_min(s)-1 internal nodes each cost at most one.
This proves the length bound. QED.

Consequently the precise loss of the assignment certificate is

    B = W-e sum_s delta_s,
    W-(B+e ceil(M/2)) = e (sum_s delta_s-ceil(M/2)),
    0 <= W-(B+e ceil(M/2)) <= e sum_{s!=0} min(mu_s,h_min(s)-1).

The residual row data also have an exact description:

    d_p = delta_i+delta_j-delta_s-(tau_p+lo_p),
    u_p = delta_i+delta_j-delta_s+(up_p-tau_p).

Both tau_p+lo_p and up_p-tau_p lie in {0,1}; u_p-d_p=up_p+lo_p<=1. These identities isolate losses
from dropped unit allowances. They do NOT prove that enough total payment is available. In particular,
M>=sum delta is FALSE: <34,42,53,54,56,57,67> has c=140,g=93,e=7,W=189,B=133,sum delta=8,M=0.
Here b itself is UA3-feasible and UA3=133, independently rationally certified; not every difference from
the actual mu needs repair. Also <20,25,61,102,143,184> has sum delta=22 but M=10.

### Rational interval propagation and matrix-free assignment upper certificates (E397)

**Interval bounds (PROVED, elementary elimination).** Initialize l=b. Initialize upper bounds at generators
by u_g=mu_g and at a composite s by u_s=min_tight(u_i+u_j-L_p), in increasing w. These are finite valid
coordinate bounds on every UA3-feasible vector. For i!=j each row L<=y_i+y_j-y_s<=U implies

    l_i >= L+l_s-u_j,     l_j >= L+l_s-u_i,     u_s <= u_i+u_j-L,
    l_s >= l_i+l_j-U,     u_i <= U+u_s-l_j,     u_j <= U+u_s-l_i.

Read these as max/min updates of the old bounds, not as fresh inequalities about arbitrary l/u. For i=j use
l_i >= (L+l_s)/2, u_i <= (U+u_s)/2, l_s >= 2l_i-U, u_s <= 2u_i-L. Every finite sequence of these rational
updates is sound, and e sum l-c<=UA3. No ceiling/floor of individual coordinates is allowed for this real LP.
Convergence in finitely many sweeps is not asserted. On <146,155,175,184>, successive lower bounds start
-526,421,599,1337/2; the full rationally certified UA3=W=1130, so coordinate propagation does not explain
the whole payment. On the two older stress cases it reaches UA3=968 and 234 respectively.

**A matrix-free falsification certificate (PROVED).** Split the non-generator residues into low cells
2w_s<=max Ap and high cells 2w_s>max Ap. High cells cannot occur together in a tight pair. Start a cover v
at delta on low cells and zero on high cells. Raise each variable to every demand from a generator-variable
pair; then raise the low endpoint of each low/high tight pair to d_p-v_high if necessary. Low/low pairs
were covered by delta already. This produces a nonnegative integer pair cover, hence

    M <= 2 sum v,     B+e ceil(M/2) <= B+e sum v.

The right-hand side is an UPPER bound on the matching certificate, not a lower bound on W. A negative
value would rigorously refute universal nonnegativity of this restricted certificate. It avoids a dense
assignment matrix; the independent checker streams all tight pairs and verifies the cover inequalities.

**A diagnostic closed-form cover (PROVED).** If, additionally, rho=0, every non-m generator is in (m,2m),
and all factorizations of each Apéry element have the same length h_s, then

    b_s=max(0,q+1-2h_s)  (s!=0),
    v_s=2h_s-2 if 2h_s<=q, and v_s=1 otherwise.

Here v_g=0, so it is a pair cover on the variables. For a non-top target the upper allowance is 1 and the
graded recurrence gives the formula for b. At the top residue r=m-1, w_r=(q+1)m-1<2mh_r, so its displayed
positive part is zero as required. All h_s<=q. Two high-degree parents therefore cannot form a tight pair.
A low/high pair has demand 2h_low-1, paid exactly by the proposed v. A low/low pair has demand -1 if its
target has positive b, otherwise 2(h_i+h_j)-q-2<=2(h_i+h_j)-4. Generator pairs and repeated parents satisfy
the same cover inequalities. Thus, if N_low counts the nonzero cells with 2h_s<=q,

    B+e ceil(M/2) <= e(q+m-1+(q-2)N_low)-qm.

A negative right side would refute the general matching claim using a genuine S; it would not refute Wilf.
This conditional diagnostic is NOT a replacement family target. E398 checks one attempted construction
against its hypotheses and finds no rho=0 realization there.

### Finite lattice-tile realization check used in E398 (on-paper certificate argument)

For an integer matrix L with positive diagonal, nonpositive off-diagonal entries and positive row sums,
call x>=0 parking if x-L*1_U is not nonnegative for every nonempty coordinate subset U. Suppose a finite
list T contains exactly these configurations, a^T L is divisible by m, labels a dot x mod m biject T onto
Z/m, and g_i=m+(a_i mod m) satisfies g^T L>0 coordinatewise. Then

    Ap(<m,g_1,...,g_d>,m) = {g dot x : x in T}.

Indeed any non-parking configuration admits a nonnegative reduction x -> x-L*1_U, decreasing g dot x by
a positive multiple of m and preserving the residue. Repetition terminates at the unique parking configuration
of that residue. Thus it is the unique least-cost factorization. All parking coordinates are smaller than
the corresponding diagonal of L, since singleton U is among the tests, so the finite check is exhaustive.
This is a direct certificate argument for the experiment, not a novelty claim about parking-function theory.
The relation to z-superstability and M-matrix energy minimization is recorded in LITERATURE.

### Actual repair capacities: exact assignment reduction and a failed normal form (2026-10-22; E399)

**Graph lemma (PROVED on paper).** Let H be any symmetric nonnegative integer matrix and let delta>=0 be an
integer feasible pair cover: delta_i+delta_j>=H_ij, including diagonal constraints. Define

    a_i=max(0,max_j(H_ij-delta_j)),
    H'_ij=max(0,H_ij-a_i-a_j),
    M'=maximum assignment weight for H'.

Then the minimum of sum t subject to 0<=t<=delta and t_i+t_j>=H_ij is exactly

    sum a + M'/2.

*Proof.* Every bounded cover has t_i>=H_ij-delta_j, hence t>=a. After subtracting a, the pair constraints
are precisely the ordinary nonnegative cover problem for H', whose optimum is M'/2 by the symmetric
assignment argument already proved above. The upper caps do not raise this shifted optimum. Indeed, for
ANY cover t>=a, clipping it to min(t,delta) preserves all pair constraints: if only i is clipped, the other
endpoint is at least a_j>=H_ij-delta_i; if both are clipped use feasibility of delta. Also delta>=a, so the
clipped vector remains >=a. Thus an optimum cannot exceed delta in any coordinate, since clipping would
strictly reduce its cost. This proves equality. QED.

Apply this with the actual repair delta=mu-b. It gives the general valid Wilf bound

    W >= B+e(sum a+ceil(M'/2)).

It is NOT automatically a lower bound on unrestricted UA3: a general UA3 repair was not proved <=delta.
Any Wilf counterexample must make this bound negative, so it is a valid residual within the universal target.
Its universal nonnegativity remains unproved. The C audit uses two exact integer assignments, with independent
primal/dual checks; the bounded primal is reconstructed as a_i+(alpha'_i+beta'_i)/2 and checked <=delta.

**FALSE normal form.** The original (uncapped) cover need not have an optimum <=delta. For
S=<66,67,71,72,98,103,128>, m66,c326,g215,e7,W451,B115,sum delta48, original M82:

    unrestricted cover optimum =41,
    bounded cover optimum =42 (sum a41, M'=2).

Thus EVERY original optimum exceeds actual repair at some coordinate. The saved original symmetric-dual
cover assigns 2 to residues2,7,10,12 and3/2 to residues11,42, each with actual delta1. Its total still is41.
The bounded optimum raises the Wilf bound from402 to409, both below actual W451. This refutes a proposed
per-cell nonnegative-unpaid interpretation of the original optimum, not the matching theorem or Wilf.

### Exact position of unit penalties and a generator-count loss bound (E401)

Keep m,r,up,tau and exclude zero parent/sum residues. The exact closed form is

    kappa(i,j)=up(i,j)-tau(i,j)
       = [i<=r and j<=r and i+j<=2r-m]
         +[i>r and j>r and i+j<=m+r].

**PROVED.** Mixed types have tau=up=0. For HH, the tau=1 cases have up=1; in a tau=0 case, up=1 exactly
when the unwrapped sum is <=2r-m. For LL, up=0 and tau=-1 exactly when i+j<=m+r. These are exhaustive,
using the previously proved tau formula. The two displayed regions are disjoint.

**Lean status:** `Wilf.upper_penalty_position` in `lean/Wilf/RepairMatching.lean` kernel-checks the exact
integer identity for arbitrary admissible m,r,i,j, with explicit definitions of the sum/shifted residues.
Only propext,Classical.choice,Quot.sound; no sorry or added axioms. This formalizes the position identity,
NOT its semigroup interpretation or the following loss bound. The C identity audit also checks33,375,552
nonzero residue pairs over every 2<=m<=128 and every r (diagnostic redundancy, not the universal proof).

Let Z be the non-m primitive residues in the sufficient zero-penalty region

    {a : max(1,2r-m)<=a<=r} union {m-1}.

Adding a primitive with residue in the interval always has kappa=0. Adding one at m-1 can have kappa=1
only when its target is r, where mu_r=delta_r=0. Therefore every tight primitive addition by g in Z satisfies

    delta_(s+g) <= delta_s.

For a general tight pair, the upper recurrence gives delta_s<=delta_i+delta_j+kappa(i,j). Let eta_s be the
minimum number of primitive occurrences OUTSIDE Z among all factorizations of w_s. Then, for EVERY S,

    delta_s <= min(mu_s,max(0,eta_s-1)).

*Proof.* Choose a factorization realizing eta. All partial sums are Apéry. Combine the eta outside-Z leaves
first, costing at most eta-1 unit penalties, then add the Z leaves one at a time without increasing delta.
If eta=0 or1, start with a single primitive (delta=0), then add the Z leaves. The top-target exception has
delta=0 and causes no problem. This proves the bound without gradedness, uniqueness, or a depth restriction.
It is a statement about delta, not D_r: the latter can be positive while mu_r=0.

The same nonincrease holds for ANY Apéry summand a in the displayed residue region with delta_a=0, not
just primitives. Thus zero-loss composite summands can provide downward closure of positive delta-level
sets even when Z contains no primitive. This is the next residue-counting mechanism to test. Its ability
to pay the full Wilf deficit is NOT proved. The independently reconstructed shortest-path eta bound passes
the saved matching/cover data; e.g. <43,155,184,193> has two qualifying primitives, loss8 and eta-bound sum20.

### Failed constant-margin dichotomy and direct actual-W search (E400)

The candidate statement, on e>=4,c>4m,3e<m,

    B>=0 OR 2W>=c,

would imply Wilf together with the known e<=3 case, but is FALSE. A single generator lift gives

    <60,61,67,71>: c420,W260,B-144
       -> <60,67,71,121>: c480,g301,W236,B-164,M156,matching bound148.

Here 2W472<c480. Exact UA3=AM3=180, TX=FACE=W236, all rationally certified. Continuing actual W/c
descent while retaining B<0 reaches <60,71,121,143>, c655,g432,W237,B-111,M150,bound189,UA3=W237.
Do not replace 1/2 by another empirically chosen constant. These are finite local-search outcomes only.

### Individual repair payments and their exact remainder (2026-10-22; E402)

Keep the actual integer repair delta and pair matrix H. Define

    F_i=max(0,max_j(H_ij-delta_j),ceil(H_ii/2)).

Every INTEGER bounded pair cover satisfies t_i>=F_i. Consequently

    I(S)=B+e sum_i F_i <= W.

The ceilings are justified by actual integrality; I is not asserted to bound unrestricted real UA3 or even
the real capped pair-cover LP. Universal I>=0 is unproved. Reusing the E392 sample (10000 candidates,
8592 accepted,34 B-negative) and three finite local descents found no failure; these checks are not a proof.

There is an exact cellwise expression. For a tight pair p=(i,j->s) put alpha_p=tau_p+lo_p in {0,1} and
C_p=delta_s+alpha_p. For a non-generator i, its remainder R_i=delta_i-F_i equals

    min( {delta_i}
         union {C_p : tight i+j->s, j!=i}
         union {floor(C_p/2) : tight i+i->s} ).

An empty successor set contributes no extra minimum. This follows by substituting
d_p=delta_i+delta_j-C_p into the cap-induced lower bound, and treating a generator partner (fixed repair0)
and a repeated variable separately. Nonpositive demands do not affect the minimum. Thus

    I(S)=W-e sum_i R_i.

This describes exactly what one-step individual payments leave unpaid, rather than assuming all unpaid
cells are maximal. The latter inference is not justified.

### Target-repair transport as a certified shortest-path relaxation (E403; PROVED on paper)

Write an admissible repair as t and define unpaid variables x=delta-t. For the bounded repair system,
0<=x<=delta. The two tight rows are exactly

    -kappa_p <= x_i+x_j-x_s <= alpha_p,
    alpha_p=tau_p+lo_p,       kappa_p=up_p-tau_p.

Both costs are0/1 and alpha_p+kappa_p<=1. Three DIFFERENT relaxations are implemented:

1. **Generator summands.** If j is a generator then x_j=0, even for unrestricted UA3. Hence
   x_i<=x_s+alpha_p and x_s<=x_i+kappa_p. Use only these edges and x<=delta.
2. **Zero-loss summands.** Under the actual caps, delta_j=0 implies x_j=0, giving the same two edges
   for composite j as well. These extra rows produced NO improvement on the27 saved examples.
3. **All capped pairs.** For any partner j, nonnegativity and its cap give

       x_i<=x_s+alpha_p,      x_s<=x_i+delta_j+kappa_p.

   Add both parent orientations of every tight pair. This retains target-repair transport that ordinary
   pair cover drops. A repeated parent is relaxed by the same valid bounds; halving is not imposed here.

In each graph an edge u->v of cost c means x_v<=x_u+c. Initialize distance at every vertex i by delta_i.
The distance envelope U_i=min_j(delta_j+shortest-path-cost(j,i)) is the coordinatewise greatest feasible
vector for that difference-constraint relaxation. All costs/caps are nonnegative integers, so U>=0, U<=delta
and U is integral. Proof: every path gives the indicated upper bound for any feasible x; conversely the
distance vector obeys each edge inequality and each cap. Therefore the relaxation's maximum sum x is sum U.

It follows that T=W-e sum U is a lower bound on UA3 in mode1, and a lower bound on actual W in modes2/3.
Modes2/3 are not claimed to lower-bound unrestricted UA3. A negative W necessarily makes all these valid W
lower bounds negative, so they remain within the proved reduction of the universal backwards target.
Universal nonnegativity of any such T is NOT proved.

The C routine exports U and a predecessor forest. The independent checker reconstructs membership, Apéry,
all edges and caps, verifies every edge inequality, and checks that each predecessor path terminates at a
cap with exact total distance. This certifies the envelope, not just feasibility. Generator-mode bounds
were also checked against all27 independently rationally audited UA3 optima.

Examples: <146,155,175,184> gives generator/zero-loss374, all-pairs602, versus UA3=W1130. For
<60,71,121,143>, generator221 and all-pairs237=W. For <64,67,69,77,129>, both give452=UA3<W467.
The failed expectation was that zero-loss COMPOSITE SUMMANDS explained the gap; in the saved examples
they did not. Nonzero partner caps and target rows do explain an additional part, but do not finish Wilf.

### Exact zero targets and top-divisor rigidity; no uniform size for one top ideal (E404)

In any bounded repair, if a tight target has x_s=0 and alpha_p=0, then nonnegativity forces x_i=x_j=0.
For the largest Apéry residue r this applies to EVERY tight split: its shifted residue is m-1, and

    alpha_(i,j->r)=tau+lo=0.

Proof: i+j=r implies both parents<=r and tau=lo=0. If i+j=r+m, both parents>r, tau=-1 and lo=1.
Thus, for A={i : w_r-w_i in S}, every admissible capped unpaid vector vanishes on A. In particular the
all-pairs distance envelope has U_i=0 on A. The arithmetic allowance identity and the abstract nonnegative
zero-split implication are kernel-checked in RepairMatching.lean; the semigroup construction remains on paper.

This rigidity does not give a uniform lower bound |A|>=m/e. An arbitrarily large genuine counterexample
to that COUNTING CLAIM is obtained as follows (not a counterexample to Wilf). For n>=7 put m=2n and

    T=<m,m+1,m+2>,       f=nm-1,       S=T union{f}=<m,m+1,m+2,f>.

The Apéry representatives of T are w_(2k)=k(m+2) and w_(2k+1)=m+1+k(m+2),0<=k<n. These follow by
minimizing the number of1/2 offsets; wrapping adds at least n extra generators and cannot improve them.
Hence c(T)=nm and g(T)=n^2. Since f is its Frobenius number, adjoining it adds just that one element.
Only w_(m-1) drops, by m, to f; the next largest representative is nm-2. Consequently

    c(S)=(n-1)m,  g(S)=n^2-1,  e(S)=4,  W(S)=2(n-1)(n-2),  A={0,m-1}.

The new largest Apéry element f is primitive, so |A|=2 while m/e=n/2 is unbounded. These S satisfy
c>4m,3e<m for n>=7. The n10 instance <20,21,22,199> was independently checked: c180,W144, matching
and all transport bounds144. It cannot be ignored as a finite small-m anomaly. Any global counting proof
must use other maximal Apéry elements or further structure, rather than the size of the single top ideal.
No novelty is claimed for Frobenius adjunction or elementary Apéry symmetry.

**Exact-zero closure (general paper lemma).** Start K={s:delta_s=0}. Repeat the following two implications
over all tight pairs until no new coordinate is added:

    alpha_p=0 and s in K  => i,j in K;
    kappa_p=0 and i,j in K => s in K.

Every capped full-repair unpaid vector x vanishes on K. The first rule follows from
x_i+x_j<=x_s=0; the second from x_s<=x_i+x_j=0. Nonnegativity is essential in both. Finite induction proves
the claim, and closure terminates after at most m new-coordinate additions. If CapUA3 denotes the minimum
of the full tight-pair UA3 system with the added caps y<=mu, then

    W >= CapUA3 >= B+e sum_{s in K} delta_s = W-e sum_{s outside K} delta_s.

This is the bound obtained by fixing these repairs and dropping the rest. If K contains every coordinate, the
bounded full-repair system has the unique vector x=0 and value W. This is a structural equality statement,
not a positivity proof for W. It does not establish the same equality for unrestricted UA3.

For <146,155,175,184>, initial K has10 cells; four sweeps fix146/146. For <60,71,121,143>,11 initially,
then60/60 in three sweeps. For <64,67,69,77,129>,10 initially, then61/64, leaving residues2,7,62 with
actual deltas1,2,1. The e4 example <60,67,71,121> leaves15 coordinates, so a core-size bound by e-2
cannot be assumed. These are exact finite diagnostics of the general closure, not a universal bounded-core
theorem. Future counting must retain the full residue bijection: deleting paid cells does not preserve the
tile hypotheses (see the recorded FALSE partial-tile extensions).

### The exact unpaid tangent cone and a weighted-core obstruction (E405/E406)

**Status: general lemmas proved on paper; finite LP witnesses independently checked over Q.**
The full normalized-direction scaling construction (caps and all pair inequalities) is kernel checked
as `normalized_unpaid_direction_feasible` in RepairMatching.lean. Its support/cap assumptions are explicit;
the semigroup translation and support equivalence remain on paper. Only propext,Classical.choice,Quot.sound,
no sorry or additional axioms; see data/unpaid_cone_lean.log.
Keep the full capped unpaid polytope

    P={x: 0<=x<=delta, -kappa_p<=A_p x<=alpha_p for every tight pair},
    A_p x=x_i+x_j-x_s.

The coordinates in the exact-zero closure K vanish throughout P. Define the homogeneous cone

    C={v>=0: v_K=0, A_p v<=0 if alpha_p=0, A_p v>=0 if kappa_p=0}.

Then P contains a nonzero point if and only if C does. More precisely, every v in C with all
coordinates <=1 has v/2 in P. On a zero allowance side this follows from the cone inequality. On
an alpha=1 side, A_p(v/2)<=(v_i+v_j)/2<=1, including repeated parents. On a kappa=1 side,
-A_p(v/2)<=(v_s)/2<=1/2. Outside K the integer delta_s is at least1, and v_K=0, so all caps hold.
Conversely any point in P satisfies all homogeneous zero-side constraints. An arbitrary nonzero
cone vector can be normalized into the unit box, proving the equivalence.

There exists a point of P positive at EVERY coordinate outside K if and only if the LP

    maximize epsilon; 0<=v<=1, v in C, v_s>=epsilon for s outside K

has positive optimum. One implication follows from v/2. For the reverse implication normalize a
point positive on the finite core. Also, if each core coordinate is positive in some feasible point,
their average is positive on all of the core. Thus epsilon=0 for a nonempty core would certify
additional forced zeros beyond Boolean closure; epsilon>0 certifies that none remain in that instance.
This is a support test, not a proof of any uniform bound on core size, coordinate weights or W.

On the27 previously saved S,15 have complete K and12 have nonempty cores. All12 have epsilon>0:
ten optima1 and two optima1/2, the latter at <60,61,67,71> and <60,67,71,121>. The largest core
in this dataset has42 cells at <146,147,155,185>. All27 exported primal/dual pairs are exactly
audited in data/cone_survey.jsonl.gz. Hence trying to force more coordinates to zero cannot improve
these12 capped models. No claim is made that Boolean closure is universally complete.

**A useful upper propagation, without integrality leakage.** Start U=delta. For each tight pair
repeatedly decrease the three indicated bounds as follows, using the current entries:

    U_i <- min(U_i,U_s+alpha), U_j <- min(U_j,U_s+alpha),
    U_s <- min(U_s,U_i+U_j+kappa).

Every real point x of P satisfies x<=U at every step: the first two rules drop the nonnegative
other parent from A_p x<=alpha; the third is the other side of the same pair constraint. This
also holds for repeated parents; the rule deliberately forgoes the stronger division by2, so
no floor is imposed on a real LP variable. Entries stay nonnegative integers and decrease only
finitely often. Its zero set is exactly K. The only ways to create a zero are a zero target with
alpha0 or two zero parents with kappa0; these are precisely the Boolean rules. At termination
the zero set is closed under those rules, giving the reverse inclusion as well. Therefore

    W >= CapUA3 >= W-e sum U.

This U need not itself lie in P; summing its entries is a relaxation. It is a cheap diagnostic,
not an exact replacement for the full LP. C --unit-search stops when this envelope exceeds1;
only the following exact full-model witness refutes the unit-coordinate claim.

**FALSE: every capped unpaid coordinate is <=1.** The genuine semigroup

    S=<153,166,170,317,325,474,617,766,921,925,1080>

has e11,c1683,g1013,W5687,q11,rho0 and a51-coordinate core. In its full capped model,
max x_23=2. The cap delta_23=2 gives the matching upper certificate; a feasible integer x has
x_23=2 and x_s=1 at

    {10,12,18,21,22,25,29,31,33,35,40,42,44,46,48,59,61,72,89,106,
     123,130,134,138,140,143,145,147,149,151},

with every other coordinate0. Its total unpaid mass is32, hence its repair objective is5335.
This is a feasible objective for this coordinate LP, NOT the minimum of the sum-objective
capped model and NOT an upper bound on actual W. Independent membership reconstruction and exact
checking of every tight row/cap and primal-dual equality are in data/capped_core_probe.jsonl.gz.

Here w_23=1400 is maximal in the Apéry poset. Its four incoming tight pairs are(1,22),(5,18),
(10,13),(11,12), all with alpha0,kappa1. There is no tight outgoing pair. Thus a zero-cost
relation to a rigid successor cannot impose a unit bound. The five preceding coordinate LP checks
on the saved data all had maximum1; an additional sum-objective optimum used only unit values.
Those checks were insufficient
to establish the universal shortcut. This counterexample satisfies c>4m,3e<m and is relevant
to the remaining universal domain. It does not violate Wilf.

**Strategic implication.** Both a cardinality-only treatment of residual coordinates and a
single-top-ideal argument are now excluded. The missing general statement must pay for weighted
unpaid mass as well as the fixed boundary, retaining all maximal elements and residue completeness.
The cone support lemma does not supply that counting statement. Universal nonnegativity of the
existing matching, propagated or full capped certificates remains unproved.

### Propagated residual matching and the real/integer distinction (E408/E409)

**General paper result; existing assignment/rounding Lean components apply. Positivity UNPROVED.**
For the no-floor recurrence in E406 define the weak polytope Q by0<=x<=delta and, for every tight pair,

    x_i<=x_s+alpha, x_j<=x_s+alpha, x_s<=x_i+x_j+kappa.

The stabilized U is its greatest feasible vector, including over R. Indeed each update preserves
x<=U for every x in Q; integer initial bounds and updates terminate. At termination U itself satisfies
every defining inequality of Q. Therefore max_Q sum x=sum U. This is exact for Q, NOT the full P.
Adding both parents on the alpha side is essential; Q only retains each separate parent bound.

Let J={s:U_s>0}. On this fixed point, every positive overflow

    h_p=U_i+U_j-U_s-alpha_p >0

has both i,j in J: if U_j=0, then h_p=U_i-U_s-alpha_p<=0 by the fixed-point inequality. The same
argument applies with i and j reversed. Build a symmetric matrix H on J, setting H_ij to the maximum
positive overflow of that pair (zero if none), with repeated-parent demands on the diagonal. Let M_U
be its maximum assignment weight. For any feasible full capped x, z=U-x>=0 and the original alpha row gives

    z_i+z_j-z_s >= h_p, hence z_i+z_j >= h_p when h_p>0.

For h_p<=0, only the latter inequality with demand0 is asserted. In particular, replacing h_p by
max(0,h_p) in the THREE-variable inequality is not valid in general. Summing along an optimal
assignment uses each z twice and proves the real bound

    CapUA3 >= W-e sum U+e M_U/2.

The actual point x=0 has z=U integral, so the recorded rounded-assignment argument proves

    W >= Phi(S):=W-e sum U+e ceil(M_U/2).

Phi need not bound the real capped LP after rounding. Universal Phi>=0 is unproved and would imply
Wilf in the remaining domain, together with the recorded complement theorems. Exactness on examples
does not establish its sign universally.

**Integer propagation is a different model.** Define P_Z=P intersect Z^m, and IntCap=min_{x in P_Z}
(W-e sum x). This set contains x=0, so W>=IntCap. Repeated parents permit
U_i<-min(U_i,floor((U_s+alpha)/2)) for this model. All updates then preserve x<=U for every x in P_Z;
termination is finite. This U is the greatest INTEGER vector in the weak system augmented with its
repeated-parent alpha rows. Residual assignment yields

    W >= IntCap >= Phi_Z(S):=W-e sum U+e ceil(M_U/2).

No real CapUA3 bound follows from the floored envelope. Concrete distinction: <60,61,67,71> has
real CapUA3=234 (real residual bound232+4/2), while integer propagation and rounded matching give236.
The positive real cone directions of E405 do NOT preclude further integer forced zeros. On
<60,67,71,121> the integer recurrence cuts unpaid mass15->14, raising176->180; on the preceding
60case it cuts7->6, raising232->236. These are examples of useful integer zeros beyond Boolean closure.

**User-supplied coupling obstruction independently verified.** S=<65,82,214,217,265> has
m65,e5,c1108,g596,W1452 and the tight pair w41+w55=431+510=941=w31,alpha1,kappa0.
Both envelopes have U41=U55=1,U31=0, so neither is feasible in P. The no-floor envelope has mass11,
bound1397,M_U4,Phi1407. The integer envelope has mass10,bound1402,M_U2,Phi_Z1407. An independently
audited full real capped LP has maximum unpaid9, hence CapUA3=1407 exactly. This validates the
supplied example and its integer values; it is not a counterexample to Wilf or to Phi_Z>=0.

The28 earlier saved S plus this new S have both envelopes and exact assignment/dual certificates.
On the earlier28, residual matching improves only two no-floor values:232->236 and176->180. Both
improvements are already captured by integer propagation, so their integer residual assignment is0.
The supplied65case has a genuine residual pair coupling after integer propagation (1402->1407).
Do not describe the new matching stage as recovering a missing global counting theorem.

**Next exact research target:** prove or falsify Phi_Z>=0 for every S with c>4m,3e<m. Any true Wilf
counterexample makes this valid lower bound negative. The unchanged universal backwards scope applies.
The missing proof must use arithmetic/residue completeness to compare the propagated baseline and
remaining pair cost to c; more exact reconstruction of an individual W does not supply that comparison.

### Counting forced-equal unpaid coordinates together (E410/E411)

**General on-paper payment lemma, not a universal positivity theorem.** Let U be the integer
propagation envelope from E409. All following claims concern P_Z; no real-LP validity is inferred
from integer floors. If a tight pair has alpha=kappa=0 and U_i=0, then every feasible unpaid vector
satisfies x_j=x_s. The analogous rule holds with i,j reversed. Form the equivalence classes generated
by these equalities on J={s:U_s>0}. The propagated U is constant on each class: its zero-cost rules give
both U_j<=U_s and U_s<=U_j+U_i=U_j. Hence z=U-x is also constant on each class.

Write n_C=|C|, u_C=U_s for s in C. These n_C count distinct Apéry RESIDUES; nothing is deleted
from the semigroup. Let H be the positive-overflow matrix from E409, and define

    G_CD=max{H_ij : i in C,j in D},
    H_eq(i,j)=G_[i],[j].

The exact row that supplies each H_ij and equality within C,D imply z_C+z_D>=G_CD. Thus the
following weighted pair-cover problem gives a lower bound on the total remaining repair:

    min sum_C n_C z_C; z_C>=0, z_C+z_D>=G_CD for every C,D.

Its fractional optimum is M_eq/2, where M_eq is the maximum assignment weight of H_eq on the
original J coordinates. Proof: an assignment uses every coordinate twice, giving the lower bound.
Conversely the symmetric assignment dual supplies a feasible cover on the expanded matrix of cost
M_eq/2 (E392). Average its entries within each class. Because the completed matrix is constant on
class pairs, averaging every pair inequality preserves feasibility, including C=D; the total objective
is unchanged. This produces a feasible class-constant cover of the same cost. This is an elementary
symmetry reduction of weighted pair cover; no novelty is claimed for assignment duality.

The fixed-point bounds also give H_ij<=min(U_i,U_j): subtract U_s+alpha from either parent bound.
Thus G_CD<=min(u_C,u_D). Clipping any class cover at u_C preserves every demand, so the same
fractional optimum is achievable with0<=z_C<=u_C. This does NOT assert feasibility of that cover
for all full target rows. Actual integer unpaid vectors satisfy integer z_C, and their total
sum_C n_C z_C is an integer. Therefore

    W >= IntCap >= W-e sum U+e ceil(M_eq/2) >= Phi_Z.

The last inequality follows from H_eq>=H. A single demand between distinct classes already forces
cost at least min(n_C,n_D)G_CD. A self-class demand forces n_C G_CC/2 in the real cover and
n_C ceil(G_CC/2) for integer class repair. Such residue multiplicities are lost when equal coordinates
are treated as unrelated vertices. No uniform lower bound on class sizes is assumed.

**Diagnostic from backwards descent, independently verified.** The three E410 searches retain B<0,
actual e, c>4m,3e<m and the previous one-coordinate neighborhood (m>=20; other generator candidates
m+1 through8m; no new parameter box). They minimize Phi_Z/c, with actual W/c as tie breaker.
From <60,67,71,121> they reach the existing <60,71,121,143> (Phi_Z237,c655); from
<64,67,69,77,129> they reach <64,69,77,129,149> (c446,g300,e5,W284,Phi_Z274); from
<146,155,175,184> they reach <146,155,184,535> (c2334,g1417,e4,W1334).
All are LOCAL optima only; no negative Phi_Z found. The final146case has unpaid envelope mass95,
propagation954,residual assignment18, hence Phi_Z990. A full capped LP certifies maximum unpaid84,
value998. This is not a genuine Wilf counterexample.

In that case J has73 residues, and there is one nontrivial equality class

    C={76,85,94,103,114,123,132,141}, all with U=1.

There are65 other singleton classes. Equality completion raises the exact assignment value18->22,
giving954+4*11=998, coinciding with the independent full real capped optimum in this instance.
Integer equality completion is not claimed to bound that real optimum in general. The full capped
optimum has a feasible integer witness here; therefore IntCap=998 as well. Its maximum unpaid
coordinate is3, reinforcing that arbitrary unit/two-unit caps are unjustified. The class construction,
completed matrix and assignment dual are independently reconstructed in verify_matching.py, using
undirected reachability rather than the C union-find implementation.

**Remaining global obligation.** Class multiplicity supplies a genuine local counting/payment
ingredient. It does not imply that the propagated baseline plus this payment reaches c/e in general.
That comparison must still use the full arithmetic/residue structure and the primitive count. The
original Phi_Z positivity target has not been proved or falsified; replacing it by its stronger
equality-completed bound is not automatically a proof. No further box enlargement or guessed
W/c threshold is justified by these three local searches.

### Exact allowance positions and a limit of zero-anchor equality completion (E412)

**Universal arithmetic formula kernel checked; semigroup consequences proved on paper.** For all
admissible residues, with t=i+j and L={1,...,r}, H={r+1,...,m-1},

    alpha(i,j)=[i,j in L and t>r]+[i,j in H and t>m+2r+1],
    kappa(i,j)=[i,j in L and t<=2r-m]+[i,j in H and t<=m+r].

The second identity is E401; the first follows by splitting the same carry/shift cases in
tau+lo. Both are Lean checked, with no sorry or extra axioms (RepairMatching.lean,
lower_allowance_position / upper_penalty_position). In particular ALL mixed-side tight pairs have
alpha=kappa=0. The other exact rows have

    LL: 2r-m < i+j <= r;        HH: m+r < i+j <= m+2r+1.

This is an exact classification, not a restriction to semigroups whose pairs have a selected form.

If rho=0, then r=m-1 and every nonzero residue is low. The only rows with BOTH allowances zero
target s=m-1. The simplified carry/upper-flag arithmetic implication is separately kernel checked
as zero_shift_exact_target. That target has mu_s=U_s=0, and alpha=0 forces both parent bounds0.
Consequently NO equality edge in the E411 zero-anchor construction can meet J={s:U_s>0}: all of
its active classes are singletons and H_eq=H. The equality-completed bound equals Phi_Z.

This limitation concerns the specific E411 construction; it does not rule out additional equalities
derivable from combinations of other constraints. It does not prove or disprove Wilf at rho0 and
does not activate a restricted-family research target. It rules out relying on this particular
class-merging step as the sole new universal counting mechanism. The saved <60,67,71,121> has rho0,
integer unpaid mass14 and all active classes singleton, so residual loss persists there without
any E411 merge. General positivity still requires a principle that also covers this situation.

C independently checks both allowance formulas, the mixed-side identity and the rho0 implication
on all33,375,552 admissible unordered residue pairs for2<=m<=128 and every r. This finite audit is
separate from the universal kernel-checked arithmetic statements.

### A collision-only repair budget fails; the exact global chain budget (E413)

Return to the recorded CH identity (KNOWN, Zhai-equivalent; no novelty claimed): for every primitive
g other than m let nu_g(w)=max{k:w-kg in S}; define

    D_g=m*max(Ap)-sum_w w-g*sum_w nu_g(w),
    E=sum_w(sum_g g*nu_g(w)-w),
    C=(e-2)m(m-1)/2.

Then D_g>=0,E>=0 and mW=sum_g D_g+E-C. For the integer propagated/assignment remainder
R=sum U-ceil(M_U/2), exact substitution yields

    m Phi_Z=sum_g D_g+E-C-e*m*R.

The analogous identity holds for the completed assignment, using its M_eq. This is an identity,
not a new positivity theorem: the missing inequality is sum D_g+E>=C+e*m*R.

**FALSE candidate funding rule: E>=e*m*R.** In the genuine remaining-domain semigroup
S=<13,17,27,29>, c63,g37,e4,W41, the Apéry representatives (residue order) are

    [0,27,54,29,17,44,58,46,34,61,75,63,51].

Every one has a unique factorization in17,27,29, so E=0. Independent generator-order coin DP
counts those factorizations; subtraction by multiples of each primitive independently computes nu.
The integer envelope has only U_2=1 and residual assignment0. Its singleton class cannot merge,
so R=1 for either original or completed assignment. Thus the proposed E payment is0 versus52.
The three chain deficits are195,281,213; their sum689, correction156, and

    13*41=689-156,          13*37=689-156-52.

All original semigroup/LP/assignment data were independently audited; these calculations reconstruct
the known CH quantities exactly. The larger saved <146,147,155,185> also has unique Apéry
factorizations and R42, so the issue is not confined to small multiplicity. No Wilf failure occurs.

**Strategic consequence.** Unpaid loss is not synonymous with factorization collisions. Any budget
argument based on CH must allow primitive-chain end deficits to pay part of the residual loss,
while also retaining the discrete correction C and the complete residue count. The E-only charging
rule and E411-merging-only global route are discontinued. The next universal obligation is an
actual allocation of those boundary deficits, not another accurate reconstruction of individual W.

### A joint, unbounded-depth nonnegativity test (E414)

**Model equivalence on integer actual coordinates proved on paper;31 continuous LP optima exactly
certified. Not a universal Wilf proof and not a proof of Phi_Z>=0.** Fix a seed's multiplicity m,
largest-Apéry residue r, exact tight-pair set T, and primitive residues G. Write rho=m-r-1 and
e=1+|G|. The carry tau and typed allowances depend only on the residue labels and r.

Use variables q, a_s (actual mu), y_s (capped certificate),1<=s<m. Both a_0 and y_0 mean q.
The actual-coordinate constraints are

    q>=5, a>=0, a_r=0, a_s<=q-1-[s>r];
    a_i+a_j-a_s-q=tau_p                  if p in T;
    a_i+a_j-a_s-q<=tau_p-1               otherwise.

All pairs here have nonzero parents and nonzero sum residue. The certificate constraints are

    0<=y_s<=a_s, y_g=a_g for g in G;
    -lo_p<=y_i+y_j-y_s-q<=up_p          for p in T.

Minimize J=rho+(e-m)q+e sum_{s>0}y_s, with NO upper bound on q or any Kunz coordinate.

For integral q,a, set k_s=q-a_s-[s>r] and v_s=mk_s+s. The bounds give k_s>=1. The pair rows are
exactly the positive-Kunz closure inequalities, with the seed's equalities and all other slacks>=1.
The top bounds and a_r0 make v_r the unique largest representative; hence c=mq-rho. Conversely every
genuine S with this tight pattern/top residue and c>4m yields these integer coordinates. The fixed
pattern gives exactly e primitive generators. Thus this is an exact description of the integer
actual-side domain; it is not bounded genus/height enumeration.

The implementation solves the CONTINUOUS relaxation in q,a,y. A fractional optimum is not a numerical
semigroup. Its exact feasible dual is nevertheless a lower bound for every genuine integer S in the
profile, since every such S and its capped certificate are feasible. If J_*=min LP, then

    W(S)>=CapUA3(S)>=J_*     for every S in this one profile/top-residue domain.

Positive J_* does NOT prove the weaker Phi_Z lower bound positive. An all-integral negative primal
would refute integer capped-certificate positivity (and hence Phi_Z positivity); a fractional negative
point would require further integer reconstruction/search. No negative primal or ray occurred here.

All31 DISTINCT saved profiles have positive exact minima. Examples:60dichotomy180;64e5case452;
hard146case3070/3 with fractional actual q46/3;new146case998;13unique case31;supplied65case60673/44;
153weighted case5027. Seven actual-coordinate optima are fractional. The24 integral actual optima
are independently reconstructed by membership from their resulting generators; four differ from
their seed and have independently checked integer Phi values281,128,22,5027. These regional
certificates are diagnostics toward a uniform rule, not newly adopted family targets.

The exact dual budget is

    J_*=rho+A+N+K+Q-P,

where A is the SIGNED contribution from tight actual-coordinate equalities, N>=0 from non-tight
unit-gap rows, K>=0 from positive Kunz lower bounds, Q=5*rc_q>=0, and P>=0 the total typed-certificate
allowance cost. Generator links, caps and a_r0 have zero RHS and transfer coefficient load. The
independent verifier checks every row, sign, coefficient balance, q lower-bound contribution and
primal=dual over Q. The missing global theorem is a uniform choice of dual weights with J>=0 over
all realizable profiles; no such choice has been proved. Face-based polyhedral verification and
poset games are already in BGOW [1903.04342](https://arxiv.org/abs/1903.04342),Sections4/6. No novelty
is claimed for face decomposition or LP duality; our added variables retain the coupled capped repair.

### Primitive edges suffice for the actual-side domain (E415)

**General paper equivalence; five full/reduced LP minima exactly compared.** In E414's ACTUAL-side
constraints it suffices to retain pair rows having at least one primitive parent g in G, together
with positive Kunz bounds only for g in G. All coupled CERTIFICATE rows are retained: this lemma
does not justify dropping targets or composite-parent constraints on y.

Proof in real labeled weights v_s= m(q-a_s-[s>r])+s, v_0=0. In the seed choose, for each s, a word
in primitive generators factoring w_s. Every prefix is in its Apéry set by summand closure. The
corresponding primitive edges are tight in the seed, so the retained equations imply
v_s=sum of v_g along that word, also for arbitrary real actual-side variables. Each primitive
v_g>=m+g>m. Thus every nonprimitive v_s, being a sum of at least two primitives, is>=2m+2>=m+s;
this recovers all omitted positive Kunz bounds.

For any pair i,j->s, append the chosen word for j to residue i. The telescoping identity is

    v_i+v_j-v_s=sum_along_path(v_previous+v_g-v_next).

Edges out of0 have gap0. Edges into0 have gap>=m by positivity; every other edge has gap0 or>=m
as prescribed by the seed's primitive-edge pattern. If the seed pair is tight, all its appended
prefixes are Apéry divisors of w_s, so every edge is tight and the sum is0. If the seed pair is
non-tight, its seed path has positive total gap, so at least one edge is a strict primitive exit
(or an edge into0). In the new real vector that edge still contributes>=m, and all others contribute
nonnegatively. Hence the omitted non-tight pair gap is>=m. This proves every omitted actual row,
over R as well as over the integer domain. The converse is immediate by taking a subset of rows.

These strict primitive exits are exactly the ends of primitive Apéry chains. The reduction therefore
connects E414's nonnegative arithmetic budget to the boundary terms sought in E413. It uses at most
O(e*m) actual pair rows and e-1 positive-generator bounds; the full tight certificate system can
still have O(m^2) rows. It is a shortest-path/telescoping characterization, not a claimed new general
Kunz theorem. The independent checker verifies every omitted row even at fractional reduced-model
optima. The five reduced minima equal180,452,3070/3,998,31 exactly, matching the full models.

The remaining task is genuinely global: construct a uniform nonnegative dual budget from primitive
boundary exits, positive primitive weights and coupled certificate rows, or find an independently
decoded negative integer witness. Neither31 regional duals nor this encoding equivalence supplies
that uniform construction. Do not replace the universal goal with further face enumeration.

### Strict positivity at infinity of the full joint model (E416)

**PROVED on paper; deduction and decisive equality-case counting argument supplied by the user's
advisor on 2026-10-23. Not a finite-minimum positivity theorem or a novelty claim.** For any fixed
realizable E414 profile with 3<=e<m, every nonzero recession direction has strictly positive objective
slope. Every objective sublevel set is therefore bounded and the nonempty LP attains its finite minimum.

Write a recession direction as (Q,A,Y). Tight actual equations give A_i+A_j-A_s=Q; both finite
certificate sides give Y_i+Y_j-Y_s=Q. Generator links make A_g-Y_g=0. Induction along a primitive
factorization with tight prefixes gives A_s=Y_s for every s. In particular unpaid mass has no recession
component. At finite points, the same induction using x_s<=x_i+x_j+kappa gives
x_s<=h_min(s)-1 independently of depth (already implicit in E396).

Set h_0=0,h_s=Q-A_s. Homogeneous actual bounds give 0<=h_s<=Q,h_r=Q; tight additions make h additive.
Choose the seed's lex-least factorization down-set D in N^d, d=e-1. It has m cells, contains each unit
vector, and maps bijectively onto Z/m. On D, h(z)=z.sigma with sigma_j>=0. The slope is

    dot J=d*m*Q-(d+1)*sum_D h
         =sum_j sum_{j-columns C} |C|*(Q-h(top C)) >=0.

The equality is the already recorded CH' column identity, equivalently Zhai's homogeneous inequality.
This application adds the fact that the coupled certificate has no recession loss.

If dot J=0 and the direction is nonzero, Q>0: Q=0 would force A=Y=0. All column tops must have weight Q.
Let n_j e_j be the last point on the j-axis. Then n_j sigma_j=Q, hence each sigma_j>0. At the point
(n_i-1)e_i, the j-column top has weight (n_i-1)sigma_i+k sigma_j=Q=n_i sigma_i, with integer k>=1.
Thus sigma_i/sigma_j is a positive integer; exchanging i,j forces all primitive weights equal. Every
column ends at the same total degree H. Downward closure gives D=Delta_H={z:|z|<=H}: a minimal missing
point of degree<=H would have a predecessor whose column ends below H. No point of degree>H can occur
because h<=Q.

For d,H>=2 this is incompatible with residue injectivity. Put E=Delta_1-Delta_{H-1}. If two elements
u-v,u'-v' have equal residues, then u+v',u'+v are in Delta_H with equal residues. Injectivity there
forces equality of these vectors, hence equality of the two differences. Thus E also injects into Z/m.
Its nonpositive vectors number binom(H+d-1,d); the vectors whose unique positive coordinate is1 number
 d*binom(H+d-2,d-1). Therefore

    |E|=binom(H+d-1,d)+d*binom(H+d-2,d-1)
       >binom(H+d-1,d)+binom(H+d-1,d-1)=|Delta_H|=m,

since the strict comparison is exactly (d-1)(H-1)>0. Contradiction. The remaining possibilities d=1
or H=1 mean e=2 or e=m, excluded by the statement. Hence dot J>0. An unbounded nonempty sublevel of a
polyhedron would have a nonzero recession direction with dot J<=0, proving the conclusion.

This supplies no uniform depth bound, no integrality of the minimizer and no sign of the finite minimum.
Absence of negative rays in full joint LP experiments is consequently not additional empirical evidence
for positivity. The proof does NOT apply to diagnostic models that drop a side of a certificate relation
or replace an actual tight equality by an inequality. It is not yet Lean formalized.

### Primitive projection and affine boundary margins (E417)

**General equivalence proved on paper; primitive objective/cap identities and explicit boundary
rewriting certificates independently audited at all saved joint optima.** The advisor proposed
eliminating actual variables completely. Here is an affine version using canonical factorization
boundaries; it does not assume that an arbitrary homogeneous facet reduction preserves unit margins.

Let z_s be the lex-least factorization of seed w_s in primitive generators p_1,...,p_d other than m.
D={z_s} is the down-set in CH', with z_0=0 and z_g a unit vector. Set

    H=d*m*z_r-e*sum_s z_s,        C=(e-2)*m*(m-1)/2,
    d_s=[r-s]_m,                w_s=z_s.p.

Eliminating q=(w_r-r)/m and a_s=(w_r-w_s-d_s)/m, the full joint objective is exactly

    m*J=H.p-C-e*m*sum_s x_s,       x_s=a_s-y_s.

The projected constraints are positive primitive bounds p_j>=m+g_j; depth w_r>=5m+r; actual tight
trades and strict gaps; and

    x>=0, x_g=0,
    w_r-w_s>=d_s+m*x_s,
    -kappa<=x_i+x_j-x_s<=alpha                 (all original tight pairs).

The displayed top/cap inequality includes the actual a_s>=0 bound and the y_s>=0 bound together.
The all-tight-pair certificate system is retained. These equations are equivalent over R to E414;
integer semigroups additionally require p_j congruent to g_j modulo m. Fractional p are not semigroups.
Actual tight trades now have RHS0. Their signed RHS contribution in the earlier a,q dual is a coordinate
artifact, not an intrinsic source of arithmetic credit. The finite negative terms are C and certificate
allowances, while strict exits, primitive positivity, depth and residue/cap distances provide credit.
No inequality asserting those credits suffice has been proved.

There is a general affine boundary reduction. Let B be the componentwise minimal vectors outside D.
For b in B, put t=its residue, and retain just

    (b-z_t).p=0       if seed b.p=w_t,
    (b-z_t).p>=m      otherwise.

This is a finite set with at most d*m members, constructed from primitive translations z_s+e_j. Each
row with nonzero target is an actual primitive-edge row, since every predecessor b-e_j is in D.
Rows with target0 have positive gap and follow already from p_j>=m+g_j. Thus the full actual model
implies all these boundary rows.

Conversely, start with any word v outside D. Choose b in B with b<=v and replace

    v -> v-b+z_t.

This replacement preserves residue. If b is a strict boundary word it decreases the seed weight by
at least m. If it is a tight boundary word it preserves seed weight but decreases lexicographic order,
since z_t is the lex-least factorization. Seed primitive weights are positive, so only finitely many
words lie below the starting seed weight. Rewriting terminates in the unique word z_s of the same
residue. Telescoping the replacement vectors yields an INTEGER nonnegative combination of the retained
boundary vectors equal to v-z_s. If v is tight in the seed, every replacement is tight; if v is non-tight,
at least one replacement is strict. Thus the retained equations give gap0 on every seed tight word and
the retained strict inequalities give gap>=m on every seed non-tight word. In particular every original
primitive or composite actual pair row, with its affine unit margin, follows. No coefficient-sum loss
is hidden in a homogeneous Farkas reduction.

This is a canonical monomial-boundary/Groebner rewriting argument, not a novelty claim. The boundary
set need not be a minimal presentation or exactly the outer Betti set. Brower-McDonough-O'Neill,
arXiv:2401.06025v3, Theorems4.8/4.9 describe the homogeneous projection through inner trades/outer Betti
inequalities. Compressing further to that set must still preserve the affine margins; no such additional
compression is claimed here. Their Proposition4.6 explicitly needs strict feasibility, and Example4.7
warns against omitting it.

verify_probe.py now independently constructs D, checks down-closure, all primitive-coordinate identities,
the column surplus H.p, every residue/cap distance, and full-certificate depth-independent loss bounds.
It also constructs B and audits a terminating rewriting decomposition of EVERY primitive translation,
including the number of strict steps and its full margin at fractional actual optima. It computes the
actual objective AT the joint optimum; this is not a separately minimized actual objective.

### A failed sourcewise sign rule and the next allocation question (E418)

**Exact diagnostic; not a counterexample to Wilf, full CapUA3 or Phi_Z.** Before receiving the latest
advisor message, the working test was whether every allowance-cost certificate side could be discarded
and actual tight rows used only in orientations contributing nonnegative a,q-coordinate dual budget.

First remove certificate sides with nonzero allowance RHS, retaining all other joint constraints.
The31 existing profiles have positive exact minima in this weaker model; e.g.60case180,64case432,
hard146case3058/3,new146case922,supplied65case76371/88. The boundary check <13,17> has minimum0.
These are falsification tests of one proposed simplification, not a new profile catalogue or a theorem.

Next, for each retained actual tight row with RHS tau, retain equality if tau=0, the >= orientation if
tau>0, and the <= orientation if tau<0. In this still weaker model every allowed actual-row RHS dual
contribution is nonnegative. Every remaining certificate-row RHS is0, so boundedness would supply a
sourcewise nonnegative dual. This simplification is FALSE.

For S=<19,26,27,48>, m19,e4,r13,q5,c90,g62,W22, the full joint minimum and the zero-allowance-cost minimum
are both22. But the additionally oriented model has the exact ray

    Q=1, A=Y=1 on {7,8,10}, A=Y=0 elsewhere,
    dot J=(4-19)*1+4*3=-3.

The actual tight row 7+7->14 has tau1 and ray value A7+A7-A14-Q=1, violating its original equality.
The retained oriented >= row permits that value. Other original tight equalities are also lost.
Adding eight copies of the ray to the seed gives objective22-24=-2 in the diagnostic model, not a
semigroup in the original profile. The independent verifier checks every retained row and the ray
exactly and deliberately disables semigroup reconstruction for this oriented relaxation.
The65case has a second negative ray, slope -265/2. Three controls remain bounded:20case190/3,
new146case922,60case180. Canonical data: allowance_source_probe.jsonl.gz (35 exact optima and2 exact
rays in37 model records, including the two-generator boundary check).

**Project review / decision.** The strict recession theorem eliminates a structural uncertainty but
leaves the finite correction entirely open. Better propagation and another list of positive profiles
will not settle it. Discontinue the sourcewise a,q sign rule; its failure is consistent with the advisor's
observation that signed tight costs are coordinate artifacts. Keep the full coupled model as a sufficient
universal target, not as an indispensable conjecture. Adopt E417 primitive coordinates, retain ALL tight
certificate rows, and seek an adaptive allocation from affine primitive boundaries and residue/cap
credits paying C plus weighted certificate loss. Do not require individual chains or rows to pay for
themselves. When a negative certificate appears, compare separately minimized actual and joint objectives
on the SAME domain before deciding whether integrality or certificate coupling is responsible. No such
negative full-model point or universal allocation has yet been found.

### An exact primitive-coordinate dual budget (E419)

**General affine dual transfer proved by substitution; full coefficient balance audited over Q.**
This implements the E417 parametrization on existing dual certificates without dropping any load.
Let pi be the old row duals and rc_a,rc_q,rc_y the nonnegative lower-bound reduced costs in a,q,y.
All formulas below use the unscaled objective J. Define

    N = sum_{non-tight actual rows} (-pi),
    K = sum_{positive primitive rows at g} (-pi)*(m+g)/m,
    Q = rc_q*(5m+r)/m,
    R_a = sum_{s>0} rc_a(s)*[r-s]_m/m,
    R_y = sum_{s>0} rc_y(s)*[r-s]_m/m,
    P = sum_{tight certificate lower sides} pi*alpha
        +sum_{tight certificate upper sides} (-pi)*kappa,
    C'=(e-2)(m-1)/2.

Then the same dual gives exactly

    J=N+K+Q+R_a+R_y-P-C'.

For a full actual model that includes redundant nonprimitive positive bounds, their analogous credits
are (-pi)*(m+s)/m. They vanish at optima: a nonprimitive value is at least2m+2>m+s, so complementary
slackness makes its positive-bound multiplier0. The checker retains/audits the term rather than relying
on this simplification. All displayed credits are nonnegative, P>=0. Actual tight trade loads remain
in the coefficient balance but have RHS0. This is a coordinate conversion, NOT a positivity theorem.

Proof: substitute a_s=((z_r-z_s).p-[r-s]_m)/m, q=(z_r.p-r)/m and y_s=a_s-x_s into every old row and
variable lower bound. Actual tight RHS becomes0, non-tight RHS-1, positive bounds become -p_g/m<=
-(m+g)/m, and q>=5 becomes z_r.p/m>=(5m+r)/m. Bounds a_s>=0 and y_s>=0 become top/residue inequalities,
respectively without and with unpaid mass. Certificate lower sides become -(x_i+x_j-x_s)>=-alpha
and upper sides become -(x_i+x_j-x_s)<=kappa, modulo zero-RHS actual trades. The objective constant
is -C'. Summing with the old duals and reduced costs proves the identity and coefficient stationarity.

The independently checked five reduced duals give the following contributions:

| Seed | N | K | Q | R_a+R_y | P | C' | J |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| <60,67,71,121> | 0 | 11068/75 | 0 | 8297/75 | 96/5 | 59 | 180 |
| <64,67,69,77,129> | 15 | 16903/32 | 0 | 585/32 | 15 | 189/2 | 452 |
| <146,155,175,184> | 0 | 0 | 0 | 3505/3 | 0 | 145 | 3070/3 |
| <146,155,184,535> | 0 | 69565/73 | 0 | 19130/73 | 72 | 145 | 998 |
| <13,17,27,29> | 0 | 0 | 175/13 | 384/13 | 0 | 12 | 31 |

These are not canonical/universal weights. In particular cap credit alone does not pay C' in the64
certificate, whereas the hard146 certificate uses cap credit alone. Neither individual-source funding
rule is inferred. P here uses alpha/kappa, NOT the lo/up cost of E414's a,q budget. Discarding sides
with zero old allowance RHS is consequently different from discarding zero-unpaid-cost sides.

A diagnostic `--face-zero-unpaid` retains only alpha0 lower and kappa0 upper sides, with the complete
primitive actual domain/caps. Five saved profiles have exact minima176,432,870,42903/44,22 (60,64,
new146,65,19 respectively). The putative universal zero-unpaid-cost certificate was not disproved or
proved. Stop expanding this positive sample. Raw data is consolidated in allowance_source_probe.jsonl.gz.

### Interior residue injection and the limit of a boundary-count allocation (E420)

**General paper counting lemma; the difference-set principle is standard, not a novelty claim.**
For the canonical factorization down-set D define

    T={v in D : v+e_j in D for every j},
    F={(j,v):v in T, v_j=0}.

Map (j,v) to the unique canonical word u in D with residue phi(u)=phi(v)-g_j. This map is injective
and its image I is contained in D\T. To prove injectivity, equality for two sources gives equal
residues of v+e_k and v'+e_j, both in D. Their vectors are equal by residue injectivity. If j!=k,
the j-coordinate is0 on the first and positive on the second, impossible. Thus j=k and v=v'. If the
image u lay in T, u+e_j and v would be equal vectors, again contradicting v_j=0. Therefore

    |T|+sum_j |{v in T:v_j=0}| <= m.

This extends the full-simplex difference count in E416 to arbitrary canonical D. It does not require
unique factorizations. A matched canonical exit u+e_j may nevertheless be a TIGHT actual relation;
being outside a canonical down-set is different from being outside the actual Apéry set.

For example S=<11,12,18> has multiplicity11 and primitive values12,18. Its lex down-set has v=(0,2)
(weight36) in T, since36+12=48 and36+18=54 are both Apéry values. The source j=1 maps to u=(2,0),
weight24. Thus u+e_1=(3,0) is outside D but 3*12=2*18 is a zero-gap trade. Treating every injected
source as a positive primitive exit is FALSE. The exact joint optimum31 is only a control, not a new
family target. A further payment construction must retain these zero-RHS trades.

There is a valid partial finite-credit consequence. Write gamma_s=sum_{j:z_s+e_j notin D}(z_{s,j}+1),
the actual column multiplicity at a boundary cell. CH' gives H.p=sum_s gamma_s*(M-w_s). For the image
I above, L=|I| and gamma_s>=1. Distinct residues give distinct d_s=[r-s]_m, so

    H.p >= sum_{s in I} gamma_s*d_s + m*sum_{s in I} gamma_s*x_s
         >= sum_{k=0}^{L-1} k*gamma_(k) + m*sum_{s in I} gamma_s*x_s,

where gamma_(k) are sorted in decreasing order. The second inequality is elementary rearrangement:
distinct nonnegative integer distances minimize the weighted sum at0,...,L-1, paired oppositely to
weights. In particular H.p>=binom(L,2)+m*sum_I x_s. These statements pay a finite amount plus weighted
mass on I, but do NOT pay C+em*sum_ALL x. They cannot be promoted to full Wilf.

**Duplication review / decision:** the rank estimate is dominated by the corresponding old estimate
using the entire boundary (see the failed CR-TILE shape-only criterion, E349). Do not market it as a
new positivity mechanism or repeat that failed criterion. The injection makes sharing explicit but
leaves the essential weighted transport of interior mass unresolved. A proposed aggregate transport
inequality sum_F(x_v-x_u)<=sum_{strict matches}(J-1)+sum_{tight matches}kappa was too weak to discriminate
on saved S:30 seeds pass already by the delta box, and the remaining hard146 seed has full zero
closure. No additional LPs were run for that loose aggregate. Three sharper coordinate tests at64/6,
new64/26,new146/75 all have maximum0; these are diagnostics, not a transport theorem.

### Weighted unpaid mass occurs even in the fully extendible interior (E421)

**FALSE universal shortcut, for real AND integer repairs:** x_s<=1 whenever w_s+p is Apéry for every
primitive p other than the multiplicity. This is a different hypothesis from the already false global
unit bound E406; it too fails. A fresh genuine semigroup is

    S=<104,420,453,509>,     e=4, c=4784=46m, g=2647, ell=2137, W=3764.

It lies in the remaining domain c>4m,3e<m. Here w_81=2265=5*453, and

    w_81+420=2685=w_85,
    w_81+453=2718=w_14,
    w_81+509=2774=w_70.

Thus this cell is fully extendible by all non-multiplicity primitives; its canonical word is(0,5,0).
Independent generator-order coin DP confirms that EVERY Apéry representative has a unique factorization
in420,453,509. This is not a factorization-collision phenomenon or an unpaid weight confined to maximal
cells. The exact real capped coordinate maximum is7/3, certified by rational primal and dual vectors.
The integer maximum is EXACTLY2: the real upper bound gives x_81<=floor(7/3)=2 for integer x, and the
following integer full-capped witness attains2.

    x_s=2 on {51,55,66,77,81,85,88,92,96},
    x_s=1 on {3,14,18,29,33,40,44,48,59,61,62,65,67,69,70,73,74,78,89,100},
    x_s=0 elsewhere.

The independently reconstructed semigroup and every cap/tight inequality pass exactly over Z.
The witness has total mass38 and objective W-e*38=3612. This is a FEASIBLE objective, not a separately
minimized IntCap value. MIP status supplies no mathematical upper bound here: integer optimality follows
only from the separate exact real LP bound and this exact integer witness. There is no Wilf failure.

Discovery: the existing pure C scanner with new `--interior-unit-search 10000 421 4` tests the real
propagated upper bound only on cells whose addition by every primitive stays Apéry. It stops at sample2045,
1798 accepted, with U_81=3. This is only an upper bound, not a feasible assignment. `--cap-max 81` then
certifies7/3; naive rounding did not produce an integer witness. The C API `--cap-int-max 81` finds the
integer witness, independently checked with no dual/optimality claim from MIP. The combined verifier
uses the real bound to certify integer maximum2. Raw data: allowance_source_probe.jsonl.gz; scanner
candidate/provenance: interior_unit_candidate.jsonl. The scanner's interior condition is independently
checked from membership-reconstructed Apéry values.

A prior targeted construction inflated the tile of<13,17,27,29> by coprime radix factors(2,5,3) and a
residue-preserving primitive scale53. The resulting genuine<390,9010,9222,21465> makes the chosen old
cell fully extendible, but its full capped core is empty. That attempt did not preserve positive unpaid
mass; discontinue that construction as evidence for a unit bound. It was a diagnostic, not a family proof.

**Project-level decision:** stop all global or interior unit-cap hypotheses; do not replace1 by a guessed2
(the real interior maximum already exceeds2). Keep the full primitive-coordinate weighted objective
and the exact source budget E419. The next allocation must transport genuinely weighted interior mass
through coupled tight relations while retaining primitive boundary gaps and zero-RHS trades. The new104
example is an adversarial diagnostic for that universal rule, not a new regional-proof catalogue target.
The original full Wilf theorem and universal joint/Phi positivity remain unproved.

### Weighted column reflection and axis recombination (E422)

**PROVED ON PAPER, general; not Lean checked. 2026-10-23.** This is a transport inequality for
arbitrarily weighted REAL unpaid repairs, not a unit/interior cap or a Wilf positivity theorem.
Dependencies: E390/E396 capped repair, E417 canonical down-set, CH'. Scope: every proper numerical
semigroup, with no depth/height/embedding-dimension cutoff. Uniform positivity of the bound below
would imply full capped positivity, hence Wilf; its original baseline version is FALSE (E423).

Put d=e-1. Choose the lex-least primitive factorization z_s of each w_s; D={z_s} is a down-set,
contains 0 and all d unit vectors, and maps bijectively to residues. Write x(v)=x_s for v=z_s,
x(0)=0, and A_p(x)=x_i+x_j-x_s for a tight pair p=(i,j->s). Then

    -kappa_p <= A_p(x) <= alpha_p,  alpha_p,kappa_p in {0,1}.

For each j-column C, let t(C) be its top, and define

    Gamma_s=sum_{j,C:t(C)=z_s}|C|,    sum Gamma=d*m,    Gamma_0=0.

Reflect v in its column: a=(t_j-v_j)e_j, so v+a=t. Summing its tight inequality over every column
and every v gives a row multiset R with exact coefficient identity

    sum_p R_p A_p(x) = d*sum_D x(v) + sum_{v,j}x(v_j e_j) - sum_s Gamma_s x_s.

When a=0 or v=0 the row is the identity0 and is omitted. Reflection on a column permutes its
j-coordinates, which proves the axis-sum term. Choose ANY binary recombination of the nonzero axis
blocks v_j e_j of each mixed word v (support at least2). Every intermediate word is <=v, hence in D,
and its primitive values add tightly. Summing the reversed rows over these trees gives B with

    -sum_p B_p A_p(x) = sum_D x(v) - sum_{v,j}x(v_j e_j).

Thus nu=R-B satisfies, coefficient by coefficient on every nonzero residue,

    sum_p nu_p A_p = sum_s(e-Gamma_s)x_s,
    e*sum_s x_s <= sum_s Gamma_s x_s + P(nu),
    P(nu)=sum_p (nu_p)_+ alpha_p + (-nu_p)_+ kappa_p.                 (T)

Cancelling shared reflection/recombination rows BEFORE charging P is essential. The statement is
valid for arbitrary real weights satisfying the tight inequalities; no integrality or x<=1 is used.
For nonnegative capped repairs y=mu-x>=b, CH' and M-w_s=m*mu_s+[r-s]_m give

    J=W-e*sum x >= (sum_s Gamma_s [r-s]_m-C)/m + sum_s Gamma_s b_s - P(nu),
    C=(e-2)m(m-1)/2.                                               (TB)

The numerator is divisible by m for a genuine seed semigroup. If cost is instead written in old
certificate allowances P_old=sum nu_+ lo+sum(-nu)_+ up, then

    sum nu=m-e,
    sum Gamma_s [r-s]_m-C-m*P(nu)=m*(rho-P_old),
    (TB)=rho+sum Gamma_s b_s-P_old.

Indeed each tight row has distance coboundary d_i+d_j-d_s=r-m*tau_p. Apply it to the exact load
identity and use alpha=tau+lo, kappa=up-tau. These identities are independently audited in code.
This is a weighted extension/combination of the established column method; no novelty claim about
column reflection, binary tree summation or network optimization is made.

### Global axis-adding recombination is an exact integer min-cost flow (E423)

**PROVED ON PAPER for the specified transport subclass, with exact audited examples.** This is
NOT optimization over every binary factorization tree or over the full capped LP. It applies in
all d, even though several adversarial inputs have e4. Pure C implementation: upper_scan.c
`--axis-flow FILE`; independent membership/row/primal-dual checker: verify_probe.py.

Restrict recombination paths to adding one entire axis block at each step. The nodes are mixed
words in D, a source and a sink. For each support2 word, an edge from source represents its unique
split into two axis blocks. For each larger-support word v and each j in its support, an edge
v-v_j e_j -> v represents adding that axis block. Every mixed word absorbs one unit through a
capacity1 edge to the sink. Source supplies N=number of mixed words. This is a DAG before residual
arcs are added. Incoming minus outgoing equals1 at each mixed word. Decomposing integer flow into
source-sink paths supplies one axis-adding decomposition per mixed word; conversely such choices
supply a feasible flow. Intermediate words can carry many paths.

For a merge row p, if its total flow is B_p, its signed net cost is

    lo_p*max(R_p-B_p,0)+up_p*max(B_p-R_p,0).

There is at most one merge edge for a given tight pair: residue injectivity on D identifies both
parent words, their sum, and the unique added axis block (support2 has only its single source edge).
Use a constant sum R_p lo_p, an edge of capacity R_p and cost -lo_p, followed by an overflow edge
of capacity N and cost up_p. Other reflection rows contribute only the constant. Since lo,up>=0,
this linear network has exactly the convex net cost above at optimum. All paths use at most d-1
merge edges, and N is a sufficient overflow capacity. Integral capacities imply an integral optimum;
this is standard min-cost-flow integrality, not a new theorem about arbitrary tree optimization.

The C solver uses integer shortest augmenting paths and exports a residual potential pi. The separate
checker reconstructs all arcs from independently checked membership/Apéry data, verifies flow balances,
capacities and residual reduced costs, then checks the exact equality

    cost=N*(pi_sink-pi_source)+sum_arcs capacity*min(0,cost_arc+pi_u-pi_v).

Weak duality proves optimality even without trusting the solver algorithm/status. It also rebuilds
nu and checks every residue coefficient and the E422 distance/cost identity.

**A genuine obstruction to the original proposed funding rule:** even optimal axis transport can
have negative (TB). For <60,67,71,121>, optimum P_old=27 while rho+Gamma.b=14, hence (TB)=-13.
For <60,61,67,71>, cost26 versus credit16 gives-10. For <146,147,155,185>, cost115 versus credit82
gives-33. These are exact integer flow optima with dual certificates, not failures of Wilf or CapUA3.
Improving the allocation WITHIN this network cannot prove the original baseline payment claim.
Data: p39/data/axis_transport.jsonl.gz. Stop tuning this original baseline.

### Known-zero-aware weighted transport and the remaining payment lemma (E424)

**PROVED ON PAPER inequality; nonnegativity CONJECTURAL/UNKNOWN. Not Lean checked.** This correction
uses only already forced zero coordinates; it does not postulate a new cap or discard target coupling.
Let K begin at {s:delta_s=0} and close under the two valid rules

    alpha_p=0 and s in K => i,j in K;
    kappa_p=0 and i,j in K => s in K.

Every feasible nonnegative real repair has x_s=0 on K, by the tight inequalities and induction.
Delete a reflection row whenever its coefficient vector restricted to residues outside K is
coordinatewise nonpositive. Its value is then <=0, so deleting it INCREASES the remaining row load
on nonnegative repairs. Require sink demand1 only at mixed words outside K; mixed words in K may
still be intermediate routing nodes. Reflection deletion and removal of K-word recombinations imply

    load_s >= e-Gamma_s for s outside K.

For the latter assertion, omitting the decomposition of a K-word removes its target term (zero)
and leaves its nonnegative axis-block terms as surplus. Flow conservation proves the same identity
for shared paths, including K intermediate nodes. Reconstruct nu=R'-B' as before and charge

    P_K(nu)=sum nu_+ alpha+sum(-nu)_+ kappa.

Now use literal alpha/kappa costs, NOT old lo/up, since the load is no longer an equality on all
residues. The flow construction uses constant sum R'_p alpha_p, cheap capacity R'_p cost-alpha_p,
overflow capacity N cost kappa_p. It has the same standard integral optimality/certificate proof.
For x>=0 with x_K=0, load domination yields

    e*sum x <= Gamma.x+P_K.

Put l_s=mu_s for s in K and l_s=b_s otherwise. Then every full capped certificate satisfies

    J >= Omega := (Gamma.dist-C)/m + Gamma.l - P_K.                 (ZTB)

The immediate sufficient universal theorem is Omega>=0 on EVERY semigroup in the remaining domain,
for the cost-minimizing flow above (or a more flexible valid transport). It is NOT established by
the construction. In particular, if K is all residues, demand and cost vanish and Omega=W: exact
reconstruction alone has returned the original sign problem, precisely the advisor's warning.
Do not count that degeneracy as a positivity proof or demand that each column pay separately.

On the saved adversarial cases, (TB)->(ZTB) is -13->144 for60/67/71/121, -10->198 for60/61/67/71,
-33->551 for146/147/155/185, and2645->3107 for the weighted-interior104case. These are diagnostic
instances, not a theorem about the sign. Two-generator/zero-demand controls are included. All16 flows
have independent integer optimality and row certificates. The diagnostic quantity W-P_K is also
exported as `actual_bound`; it is NOT the minimum of J and is NOT (ZTB), since it substitutes mu for
all certificate coordinates. No inference of Phi_Z positivity is made.

**Next proof obligation:** allocate primitive-boundary and cyclic-residue credit to the finite
transport cost in (ZTB), allowing compensation between columns and genuinely weighted interior mass.
A min-cost-flow dual can expose the necessary level-set/cut deficits, but duality alone is not the
missing arithmetic inequality. Keep actual integrality/descent as a distinct universal line.

#### Finite allocation as a precise potential/cut obligation (E424 continuation)

The E424 flow cost has the following exact dual form. Let V be its mixed nodes plus source o;
T be the demanded mixed words outside K, N=|T|; and E its merge edges. A merge edge a=(u,v)
represents row p(a). Write R_a=R'_p(a). Rows with no merge edge contribute to the constant only.
Define A=(Gamma.dist-C)/m+Gamma.l. Then

    P_K^* = sum_p R'_p alpha_p + max_pi [sum_{v in T}(pi_v-pi_o)
                    -sum_{a in E} R_a (pi_v-pi_u+alpha_p(a))_+],
    subject to pi_v-pi_u<=kappa_p(a) for every merge edge a.         (FD)

Proof: eliminate sink arcs, whose total capacity is N and hence are all saturated. At each mixed
node prescribe net inflow1 on T and0 elsewhere; source supply N. For each merge edge keep the cheap
capacity R_a cost-alpha, and make its overflow edge unlimited with cost kappa. Removing the overflow
bound N does not change the minimum: the graph is a DAG, every feasible flow decomposes into N
source-to-demand paths, and each edge carries <=N. The ordinary potential dual gives (FD), with the
cheap-capacity term -R_a(pi_v-pi_u+alpha)_+ and the displayed overflow constraint. Finite network
strong duality proves equality; integer costs admit an integer maximizing potential, obtained from
shortest distances in an optimal residual network with unlimited overflow forward arcs. Additive
normalization pi_o=0 is optional. For N0 the same argument covers the zero-demand network.

Consequently the still-UNPROVED universal finite payment lemma for this construction is EXACTLY

    sum_{v in T}(pi_v-pi_o)
      <= A-sum_p R'_p alpha_p
         +sum_{a in E}R_a(pi_v-pi_u+alpha_p(a))_+                  (PAY)

for every feasible integer potential pi. This is not a positivity theorem: (FD) alone merely
identifies what a global arithmetic allocation must establish. It retains residue labels through
A and the actual tight-pair pattern, as well as weighted repeated use of each row through R_a.

There is an explicit layered-cut interpretation, which prevents an unjustified ordinary-Hall
simplification. Put T_h={v:pi_v>=h}, including source membership. The objective's first term is the
sum over integer levels h of |T intersect T_h|-N*1_{o in T_h}. An alpha0 penalty counts merge edges
entering T_h, with capacity R_a. An alpha1 penalty counts head v in T_h and tail u outside T_{h+1}.
The kappa0 constraint forces v in T_h => u in T_h; kappa1 forces v in T_h => u in T_{h-1}.
Sum over the finite range containing min pi-1 through max pi+1. These follow directly from
(pi_v-pi_u+alpha)_+=#{h:pi_u-alpha<h<=pi_v}. Thus one must pay interacting adjacent levels, not
merely one unweighted cut or each column independently. Next attempt: use strict primitive exits,
zero-RHS trades and complete cyclic residues to prove (PAY), or exhibit an exact violating potential
on a genuine low-W input before trying another transport refinement.

### Primitive orbit surplus and a constructive unit-row allocation (E425)

**PROVED ON PAPER; elementary permutation accounting, no novelty claim; not Lean checked.** Scope:
every proper numerical semigroup, no parameter restriction. This organizes actual strict-boundary
credit for the universal finite-payment question. It does not pay arbitrary certificate row weights
or the discrete correction, and is not asserted to prove (PAY).

Fix a primitive p!=m, g=p mod m, h=gcd(m,g), and the permutation s->s+g of residues. Its h orbits O
have n=m/h cells. For every edge define the actual nonnegative INTEGER gap

    J_s=(w_s+p-w_{s+g})/m.

If J_s=0 and s!=0, charge the combined two oriented repair allowances

    a_s=alpha_(s,g)+kappa_(s,g) in {0,1}.

At the trivial tight edge0->g set a_0=0; its unpaid row is identically zero. At strict edges define
supply J_s-1>=0. Let F_O be the number of tight edges with a_s=0. Then the exact cycle identity is

    sum_{s in O:J_s>0}(J_s-1) - sum_{s in O:J_s=0}a_s
      = (p-m)/h + F_O >0.                                        (OC)

Proof: telescope w around the residue orbit to get sum_O J_s=p/h. If k strict edges occur, their
excess sum is p/h-k. There are n-k tight edges, and their charge is n-k-F_O. Subtract. Since
p>=m+g and h divides p,m,g, (p-m)/h is a positive integer. This proves (OC). No unpaid coordinate
has been bounded by1: the bounded objects here are the exact ROW ALLOWANCES alpha+kappa.

There is a constructive nonnegative allocation around the orbit. Give strict edges supply J_s-1
and tight edges demand a_s. Cut the cyclic list immediately after a minimum of its cumulative
balance. Every prefix of the rotated list has nonnegative balance; forward transport from previous
supplies pays every demand and leaves the surplus in (OC). This is the standard cycle-prefix
argument. It genuinely pays all primitive unit-row coupons ONCE, allowing negative individual
local balances; arbitrary repeated row usage is not covered.

The same resource is organized by the canonical factorization columns, without confusing canonical
exits with actual strict exits. For a p-direction column C of length L_C, append e_j to its top
and let b_sigma(C) be the canonical word with that residue. Then b_sigma(C) has j-coordinate0:
otherwise b_sigma(C)-e_j lies in D with the top's residue, so residue injectivity makes it the top,
contradicting maximality of the column. Thus sigma permutes the column bases. Each column cycle
concatenates exactly one residue orbit, so

    sum_cycle L_C=m/h,   sum_cycle J_C=p/h,
    J_C=(L_C*p+w_base(C)-w_base(sigma(C)))/m,
    sum_cycle(J_C-L_C)=(p-m)/h.

All strict primitive edges occur among these column exits. Some exits are tight zero-RHS trades;
they are included among the tight unit-row charges, not misclassified as strict sources. This
makes (OC) an explicit global balance for E417 primitive boundaries. It is an organization of
existing arithmetic constraints, not an extra independent continuous inequality.

**Integer strengthening:** each primitive orbit contains an edge with J_s>=2. Otherwise every J_s
would be0 or1 and sum J_s<=m/h, contradicting p/h>m/h. Hence all genuine integer semigroups are
covered by the finite disjunction, for EACH primitive and EACH orbit,

    there exists s in O with (z_s+e_j-z_{s+g}).p >=2m.              (DEEP)

This does not specify which edge and supplies no multiplicity-independent finite profile list.
A continuous profile need only have some J_s>1; rounding that to2 is unjustified for fractional
actual coordinates. (DEEP) is a valid universal integer boundary condition, not a proved positivity
mechanism. A potential route is to use the selected deep exits to anchor a weighted allocation;
its obligations are still to pay repeated composite-parent costs and C without double spending.
The present cycle allocation alone cannot do either.

Qualification on (DEEP): the orbit containing0 already has J_(m-g)>=3 even at a continuous actual
point satisfying positive Kunz bounds, since w_(m-g)>=m+(m-g) and p>=m+g. For p>=2m, the orbit mean
p/m itself forces max J>=2 over the reals. Thus a NEW integrality restriction can occur only on
orbits away from0, for gcd(m,g)>1 and m<p<2m. If every primitive is coprime to m, (DEEP) adds nothing
to the current continuous domain. Do not advertise it as a general repair of the real relaxation.

The allocation in (OC) is a scalar allocation of actual gap EXCESSES, not yet a dual certificate
for J. E419 fixes primitive/boundary multipliers by an objective coefficient identity; (OC) does
not prove those multipliers can all be1 or constant on cycles. Any use in the Wilf proof must match
H and all certificate-coordinate coefficients and reserve C. This coefficient obligation is in
addition to the scalar budget, and prevents double spending of primitive value credit.

### Natural column-length scaling of the orbit allocation fails after zero closure (E426)

**FALSE weighted extension; exact genuine remaining-domain obstruction.** The E425 scalar allocation
cannot simply be multiplied by the column lengths appearing in CH'. A precise attempted extension
was, on each primitive orbit O,

    sum_{strict s in O} L(s)*(J_s-1)
       >= sum_{tight s in O, not both s,s+g in K} L(s)*(alpha_s+kappa_s),           (WOC)

where L(s) is the length of the canonical p-direction column through z_s, and K is full E424
known-zero closure. Charges with both unpaid endpoints forced zero are correctly omitted. (WOC)
is FALSE even with that correction; this is not an assertion about arbitrary invented weights.

Use the independently verified E406 semigroup

    S=<153,166,170,317,325,474,617,766,921,925,1080>, c1683,g1013,e11,W5687.

For primitive p170,g17,h17, the orbit starting4 has the following exact data. Every listed tight
edge has alpha0,kappa1. K contains4 but none of21,38,55,72,89,106,123,140.

| s | w_s | L(s) | s+17 mod153 | J_s |
|---:|---:|---:|---:|---:|
|4|1687|1|21|2|
|21|1551|1|38|7|
|38|650|7|55|0|
|55|820|7|72|0|
|72|990|7|89|0|
|89|1160|7|106|0|
|106|1330|7|123|0|
|123|1500|7|140|0|
|140|1670|7|4|1|

Thus weighted supply is1*(2-1)+1*(7-1)+7*(1-1)=7, while all six active tight allowances cost7,
for demand42. Unweighted supply7 and demand6 still satisfy E425 with surplus1=(170-153)/17.
The orbit starting2 gives a second deficit: weighted supply8,demand24. Source excess lies in short
columns, while repeated charges lie in long columns. Known-zero closure does not remove this
obstruction. The complete corrected E424 flow bound on S is4419>0, so this is NOT a failure of
Wilf, of the full capped model, or of E424's corrected global certificate.

The checker reconstructs these numbers from the existing seed and canonical words; run_checks.sh
asserts the7-versus42 obstruction. Stop the column-scaled per-orbit payment rule. As the advisor
warned, compensating credit must cross the chosen pieces. A global primitive-boundary allocation
may use the orbit identities but cannot require each orbit, column or direction to fund itself.
The next obligation is a globally coupled weighted allocation with the E419 objective coefficients,
not another local self-payment refinement or a larger positive sample.

### Nonnegative primitive circulations cannot create finite dual credit (E427)

**PROVED ON PAPER; elementary coefficient comparison, not a Wilf positivity theorem.** This is a
reason to stop treating E425's scalar orbit surplus as additional free credit. It applies across
orbits and directions, not just to the E426 local weighting.

Use unscaled primitive-edge rows G_(s,j)=w_s+p_j-w_(s+g_j)>=m*b_(s,j), with b=1 on actual strict
edges and b=0 on tight edges. The positive primitive bounds are p_j>=m+g_j. Take any nonzero
nonnegative edge flow lambda with balanced vertex divergence at every residue. Let

    T_j=sum_s lambda_(s,j).

The w-loads cancel, leaving sum lambda G=sum_j T_j p_j. Thus adding these edge multipliers to a
dual without changing its objective coefficients requires decreasing its primitive-bound
multipliers by T_j (assuming those decreases remain nonnegative). The exact change in its
constant lower bound is

    m*sum_edges lambda*b - sum_j T_j*(m+g_j)
       = -m*sum_tight lambda - sum_j T_j*g_j <0.                  (NC)

Every g_j lies in1..m-1, which proves strictness. Even permitting cross-direction nonnegative
circulations therefore cannot increase the finite budget through this replacement. On one orbit,
summing primitive rows only says p>=h*(number of strict exits), which is strictly weaker than the
existing primitive bound p>=m+g. The positive gap-excess resource in E425 depends on that primitive
value credit; it cannot be counted a second time as a new Farkas source.

Limitations: this does NOT prohibit adaptive changes of cap/residue multipliers, signed tight trade
multipliers, or unbalanced flows whose divergence is paid by the objective/cap loads. Those are
precisely where a useful global allocation would have to act. It does not disprove Wilf or full
capped positivity. Stop extending the scalar orbit allocation by nonnegative balanced flow alone;
match the complete objective and track which primitive credits have already been spent.

### Restricting a joint dual gives a certified actual-objective bound (E428)

**PROVED ON PAPER; ordinary LP restriction/duality, no novelty claim.** Fix the complete E414 actual
coordinate domain (or the E415 equivalent primitive domain), and a feasible optimal joint primal
(a,q,y) and exact dual (pi,rc). Let V be the joint optimum and x=a-y. Put

    P=sum_certificate_lower pi*alpha +sum_certificate_upper(-pi)*kappa >=0.

There is a feasible dual for the ACTUAL objective on exactly that actual domain with value V+P.
Moreover, at the joint actual point,

    J_actual(a,q)-(V+P)=sum_{s>0}rc_y(s)*a_s
                      =sum_{s>0}rc_y(s)*x_s >=0.                 (AT)

A zero gap in (AT) certifies the actual minimum as V+P without a new optimizer. With a nonzero
gap, the transfer alone gives a lower bound. The actual minimum might still equal V+P at another
point, but this calculation does not establish that equality.

Proof: substitute y=a into all joint rows and the objective. Cap/link rows collapse to0. Each typed
certificate row now has the same left side as an actual tight equality; replace its RHS -lo or up
by tau. Its dual RHS gains pi*(tau+lo) or(-pi)*(up-tau). Actual tight equality multipliers have free
sign, so these replacements are dual-feasible. The new reduced cost at a_s is rc_a(s)+rc_y(s)>=0;
q's reduced cost and lower bound5 are unchanged. Every actual-objective coefficient is matched.
The actual primal at the joint point is feasible. Joint complementarity kills old actual-row,
cap/link and reduced-cost slacks; the remaining gap is sum rc_y*a. Since rc_y*y=0, (AT) follows.
Equivalently multiply the original y-stationarity equations by x.

verify_probe.py audits the complete substituted coefficient vector over Q. On the31 saved full
joint profiles,20 actual minima are now certified this way;11 have a positive gap and remain only
bracketed. For example60/67/71/121 gives actual lower bound198 and value236 at the joint point;
new146 gives1074 and1334. Those upper values must not be relabelled actual minima. Different joint
duals can give different transferred lower bounds. These are regional certificates, not a uniform
sign theorem, and no new LP solve is counted for this transfer.

### A profile-wide global allocation model and its boxed dual (E429)

**General paper reduction/normal form; positivity UNKNOWN.** Scope remains all S in the approved
remaining domain, with the recorded complement. There is no reduction to the three tested profiles.
This replaces the failed balanced-circulation funding idea by a budget which matches the full
primitive-coordinate objective and permits compensation across all orbits/directions.

Fix ANY realizable profile, canonical D,z_s, primitive residues g_j, largest residue r, d=e-1.
Let v_s=z_r-z_s, d_s=[r-s]_m, and a_s=(v_s.p-d_s)/m, q=(z_r.p-r)/m. Let T_s be E396's minimum sum
of kappa over tight binary factorization trees (T_g=0). For every real actual point in the profile,

    b_s=max(0,a_s-T_s).

This remains true over the real actual domain: positive Kunz bounds give a_s<=q-1 for s!=0.
In the upper-closure recursion, if a parent is truncated to0, its candidate is <=0 because the
other parent is <=q-1. Every positive candidate therefore has both parents untruncated; induction
and the tight identity a_i+a_j-a_s=q+tau give exactly the minimum kappa-tree formula.

Let K_0 begin with all T_s=0 and the top residue r, then close under E424's zero rules. This is a
PROFILE-FORCED subset of zero unpaid coordinates, valid on the entire actual domain. It need not
include the additional zero anchors supplied by a particular point's other a_s=0. One way to
compute precisely K_0 is to scale seed primitive values by2: all non-top a_s become positive,
while the tight pattern/penalties stay fixed. This is a real model calculation, not a semigroup
reconstruction.

Build E424's flow using ONLY K_0 (permitted since every such coordinate really is forced zero),
and let P_0 be its exact minimum unpaid cost. Gamma and P_0 are profile constants. Define

    Omega_0(p)=(Gamma.dist-C)/m +sum_{s in K_0}Gamma_s*a_s
                      +sum_{s outside K_0}Gamma_s*max(0,a_s-T_s)-P_0,
    C=(e-2)m(m-1)/2.                                             (PB)

Every full capped objective is >=Omega_0(p), for every real actual point. Unlike choosing the
point's complete zero closure, this certificate varies continuously with p on the entire profile.
It is a valid lower bound even at extra zero coordinates; no monotonic comparison with the
point-adaptive Omega is assumed. A uniform proof Omega_0>=0 for ALL realizable profiles would
prove Wilf. That stronger statement is not established. It includes both a real-domain and a
certificate strengthening of Wilf.

Minimizing (PB) is an explicit continuous LP, with no depth upper bound. Use primitive variables p,
and a nonnegative b_s only when s is outside K_0 and Gamma_s>0. Impose the full primitive actual
rows from E415, p_j>=m+g_j, z_r.p>=5m+r, v_s.p>=d_s, and

    m*b_s-v_s.p >= -d_s-m*T_s.

The objective m*Omega_0 has p-coefficient sum_{K_0}Gamma_s v_s, b_s-coefficient m*Gamma_s, and
constant sum_{s outside K_0}Gamma_s*d_s-C-m*P_0. A positive diagnostic floor epsilon can optionally
replace v_s.p>=d_s by >=d_s+m*epsilon (s!=r); epsilon0 is the COMPLETE actual-coordinate domain.
All model coefficients are integral after multiplying floor rows by its denominator. Nonemptiness
follows by scaling the seed primitive values by m+1; this also preserves genuine congruences.
The objective differs from the actual W by a bounded profile-dependent amount, so E416 controls
its recession behavior for e>=3. Finite LP minima admit standard dual certificates.

**Global boxed allocation identity.** Write xi for primitive actual-row duals (nonnegative on
strict rows; signed on tight trades), eta_j>=0 for positive primitive bounds, beta>=0 for depth,
nu_s>=0 for v_s.p>=d_s, and lambda_s for the baseline rows. Stationarity at b_s forces

    0<=lambda_s<=Gamma_s.

Set theta_s=Gamma_s on K_0 and theta_s=lambda_s otherwise. At an optimum p_j>0 makes its lower-bound
reduced cost0. The exact remaining coefficient identity is

    sum_s theta_s v_s
       =sum_primitive_rows xi_(ij->t)(z_i+z_j-z_t)
          +sum_j eta_j e_j +beta*z_r +sum_s nu_s v_s.              (BC)

It uses all signed zero-RHS trades and global residue/cap loads. The dual constant is

    Omega_0^* = sum_strict xi +sum_j eta_j*(m+g_j)/m
        +beta*(5m+r)/m +sum_s nu_s*d_s/m
        +sum_{s outside K_0}(Gamma_s-lambda_s)*d_s/m
        -C/m-P_0-sum_{s outside K_0}lambda_s*T_s.                 (BB)

All five displayed credit terms are nonnegative; the correction, transport and tree costs must
still be paid. Equation (BB) alone is NOT a positivity theorem. The new exact target is a
profile-adaptive construction satisfying (BC) and making the budget (BB) nonnegative, rather than
requiring any column or primitive orbit to pay on its own. The verifier audits all coefficients,
every rational primal/dual constraint, the row-transport certificate, and (BB).

**At most e-1 partially used baseline coordinates suffice (general paper LP lemma).** There exists
an optimal dual with at most d=e-1 coordinates satisfying0<lambda_s<Gamma_s. Proof: fix the other
optimal dual multipliers. Feasible lambda lie in a box with d coefficient equations (BC). Maximize
the linear dual budget on that compact polytope and choose an extreme maximizer. If more than d
coordinates were strictly inside their bounds, the corresponding v_s would be linearly dependent,
allowing two opposite small feasible perturbations, contradicting extremality. Adjust baseline
reduced costs to m*(Gamma_s-lambda_s). Global optimality is preserved by weak duality. No claim
that lambda is integral or that ANY partially used coordinate's unpaid mass is<=1 follows.
This is standard extreme-point structure, not a novelty claim or an explanation of the sign.
It reduces the global allocation choice to fully used/unused coordinates plus at most e-1 partial
ones; proving their complete finite budget remains the mathematical task.

**Closed discriminating tests, not universal evidence:** the complete epsilon0 profile minima are
100,300,312 for seeds60/67/71/121,146/155/184/535,146/147/155/185, respectively. They are attained at
the original integer primitives; membership is independently reconstructed. Three preliminary
epsilon1/1000 chamber minima were12543/125,639223/2125,31201/100 and were fractional model points.
No reduction from all profiles to these3 is claimed, and this positive diagnostic is closed.

**Stronger trade-quotient version of the partial-weight bound.** Let L be the linear span in R^d
of the inner tight-trade vectors z_i+z_j-z_t appearing in the primitive actual rows, and put
k=d-dim(L). An optimal E429 dual can be chosen with at most k partially used baseline coordinates.
Project (BC) to R^d/L, fix every other inequality multiplier, and optimize lambda in its box with
these at most k equations. Choose an extreme maximizer as above. The remaining coefficient error
lies in L and is absorbed by adjusting the SIGNED zero-RHS tight multipliers, without changing any
finite credit. Thus dual feasibility and the optimum are preserved. The claim concerns the trade
quotient; it removes no strict affine margins and assumes no outer-Betti minimal presentation.
This is a concrete use of inner trades in the global allocation, but still gives no sign for (BB).
Collision-free profiles may have L=0, so k=d; no collision-only payment principle is inferred.

## E430 — full-certificate order ideals; support audit and the remaining counting gap (2026-10-23)

**Scope.** Proves Wilf for: every numerical semigroup if the finite payment inequality is proved
on the remaining domain c>4m,3e<m. Proved reduction from all S to this case: yes (the recorded
c<=4m and 3e>=m complements). The following order lemma is general; the counting targets below
are sufficient intermediate claims, NOT established positivity theorems.

### Strict decrease along primitive additions — PROVED on paper

Use E414's actual/certificate coordinates a,y with y_0=a_0=q. For a genuine seed a=mu.
For every nonzero primitive residue g, the generator link and positive primitive bound give

    y_g=a_g <= q-1-[g>r].

If w_s+w_g=w_t, the lower tight certificate row gives

    y_s+y_g-y_t >= q-lo_(s,g).

Here lo_(s,g) can be1 only if g>r (and s>r). Therefore

    y_s-y_t >= q-y_g-lo_(s,g) >= 1+[g>r]-lo_(s,g) >= 1.       (ORDER)

For s=0 the same conclusion is the primitive bound itself. This proof also applies throughout
the full REAL actual profile domain, not only at integer semigroups. It requires the lower
tight rows and the generator links; no integrality assumption on y was used.

Every Apéry-poset comparison factors into tight primitive steps. Indeed, factor the positive
semigroup difference into minimal generators; multiplicity m cannot occur, and each prefix
stays Apéry, or the endpoint would cease to be Apéry. Iterating (ORDER) shows y is antitone
on this poset, with a drop at least the length of any such path. In any canonical tile D,
y(z)+|z| is antitone under coordinatewise order, since every intervening subword is in D.
Consequently every superlevel set of y is a down-set. For integer y, the diagram
{(z,k):z in D,0<=k<y(z)} is a down-set and is closed under replacing one primitive occurrence
by one multiplicity occurrence. No assertion that its complement is a semigroup follows.

This is a structural consequence of existing full rows, not a claim of a new propagation
principle or a universal sign proof. It identifies a hypothesis needed for level-set counting.

### The cheaper baselines need not have this order — REFUTED

For S=<60,67,71,121>, use the E429 profile-forced zero set K_0, and put l_s=mu_s on K_0,
l_s=b_s elsewhere. Then

    w_55=355, w_11=71 (primitive), w_6=426,
    w_55+w_11=w_6, l_55=0, l_6=1.

Thus even weak antitonicity fails for the patched baseline. Every feasible full certificate
has y_6=mu_6=1 and y_55>=2 by (ORDER). Even the RAW baseline can fail weak antitonicity:
in <66,67,71,72,98,103,128>, b_34=0<b_35=1 along the tight primitive67 edge.
The exact saved audit finds8 offending primitive-edge comparisons over36 seeds (counting
raw/profile baselines separately). Do not apply an order-ideal argument to b or l without
establishing the needed property for that replacement.

### Old support theorem must filter the research anchors — EXACT AUDIT

Let Gamma_s be the sum of canonical column lengths ending at z_s; let Dep=sum Gamma_s over
nonmaximal cells; write T=sum_z(max(support(z)-1,0)). The already proved SUPP-WILF gives

    W = N-kappa_0+Gamma.mu >= Dep-kappa_0+N >= Dep-T.

ALL36 saved seeds in data/axis_transport_zero.jsonl.gz have Dep>=T. They are therefore
already excluded by a proved shape criterion, irrespective of the later certificate models.
This does not invalidate their exact LP certificates, but those certificates were not evidence
from resistant actual Wilf cases. Further positive optimization on those profiles is closed.
The C checker now exports these counts; an independent checker enumerates whole columns,
checks the inversion/overflow identity and reconstructs genuine membership.

### Cycle interpretation and a sufficient weighted target — mixed status

The canonical Hasse graph has m vertices, sum_z support(z) edges and is connected (remove
coordinates to reach0). Its cycle rank is exactly

    sum_z support(z)-m+1 = T.                                (CYCLE, PROVED)

Thus Delta=T-Dep is a cycle count minus nonmaximal column payment. A proposed intermediate
bound Delta<=binom(d,2), d=e-1, is CONJECTURED for canonical numerical-semigroup tiles. It
is false for abstract down-sets: the full two-variable simplex of height3 has Delta3>1.
Residue completeness and possibly coherence are essential. No injection of these cycles into
torus homology has been constructed, and homology dimension alone is NOT such a proof.
Even a proof of this bound would not pay the finite correction by itself.

A stronger-than-necessary sufficient target, retaining weights, is

    Gamma.mu >= T

on shape-case-B tiles (Dep<T) of canonical height>=3. With SUPP-WILF and Flat-MaxCL on the
complement, it would prove Wilf: W=N-kappa_0+Gamma.mu>=N>=0. Its sign is UNKNOWN. It is not
claimed equivalent to Wilf, and its failure would not be a Wilf counterexample. Unlike the
older CASEB-WINDOW, it does not discard the nonmaximal depth credit or maximal heights.

Two bounded C descents from the genuine63 example found no failure. The weighted endpoint
has m63,e12,c754,g641,W602,Dep42,T44,Gamma.mu587, hence a weighted margin543. The cycle run
ended at a height2 tile, already covered by Flat-MaxCL. Both diagnostics are CLOSED; neither
is a general theorem or justification to enlarge the sample. Crucially even the initial63
seed has kappa_0=8<Dep42: it survives only the SHAPE criterion, not the stronger residue-aware
SUPP exclusion. Calling it a surviving actual counterexample candidate would be incorrect.

**Strategic review.** The main mathematical gap is still finite global payment. Discontinue
more positive regional minima, baseline level-set counting without (ORDER), and the simple
lo-only payment route refuted below. Keep three distinct questions: actual residue/primitive
boundary payment, full weighted certificate coupling, and integrality of the real actual
domain. Before a genuine search labels a point resistant, report the shape criterion, the
residue-aware Dep-kappa_0+N criterion and Flat-MaxCL separately. The exact remaining sufficient
support payment is Gamma.mu>=kappa_0-N; (ORDER) may aid a full-certificate argument but cannot
be assumed for its cheaper baseline. The cycle bound has no established global allocation yet.

### A simple lo-only transport payment is FALSE

In the ordinary E422 axis network, set every positive arc price to0 and leave negative lo
prices unchanged. The reflection constant plus this minimum flow cost is the uncovered
lo cost L. The attractive estimate L<=rho fails on genuine remaining-domain semigroups:

| generators | L | rho |
| --- | ---: | ---: |
| 114,305,307,310 | 183 | 111 |
| 62,87,88,89 | 52 | 49 |
| 65,82,214,217,265 | 79 | 62 |

These are exact integer flow optima with residual-potential dual audits, not approximate
optimizer statuses. They refute this simple decomposition only. The larger conjectural
ordinary cost bound P<=rho+T was not refuted by the36 saved examples, but has NO proof and
the failed L<=rho argument cannot establish it. Do not turn the positive sample into a claim.
Reproduction, data and the closed search neighborhoods are in EXPERIMENTS E430.

## E431 — integer realization of primitive tangent directions and a descent audit (2026-10-23)

**Scope.** Proves Wilf for: every numerical semigroup if the general finite allocation, or RD
on the remaining domain, is proved. Proved reduction from all S to this case: yes (E417/E429
and the recorded complements; RD implies Wilf by induction on multiplicity). This section
audits arithmetic/descent ingredients for those universal targets. It proves a general
realization lemma and refutes primitive-value monotonicity, NOT Wilf or RD. No fixed-height,
fixed-e or Q5 proof target is activated; concrete examples below falsify universal shortcuts.

### A direct, unsplit residue-descent budget — PROVED identity, sign UNKNOWN

For a proper S let m,e,p_j be its multiplicity, embedding dimension and other MINIMAL
generators. Put T=<m,p_j mod m>, e_T=e(T), and use Apéry representatives w_s of S and tau_s
of T with respect to the SAME element m (which need not be T's multiplicity). Define

    K_s=(w_s-tau_s)/m,   Delta_c=c(S)-c(T).

Then K_0=0, K_s>=1 for s!=0, g(S)-g(T)=sum K_s, and

    W(S)-W(T)=(e-1)*Delta_c-e*sum K_s+(e-e_T)*ell(T).       (RD-DIRECT)

Proof: S subset T and both contain m, so the shifts are nonnegative integers. Any factorization
of w_s over p_j has positive level sum and residue sum at least tau_s, giving K_s>=1. Selmer's
formula at the common modulus m gives the genus difference; substitute into W=(e-1)c-e*g.
This is the earlier combined RD identity with the auxiliary U eliminated, not a new sign bound.
Its advantage is that it cannot silently require either of the previously refuted separate
payers to be nonnegative. T has smaller multiplicity and e_T<=e, so RD on the remaining domain
would imply universal Wilf by induction and the proved complements. It remains CONJECTURED.

**Necessary failure filter.** For any numerical semigroup V, ell(V)<=c(V)/2: for each n in
[0,c-1], n and c-1-n cannot both belong to V, or c-1 would. Thus

    2W(T) <= (e_T-2)c(T).

A failure of RD with W(T)>0 must have 2W(S)<(e_T-2)c(T). This excludes12 of the13 saved
transport anchors with W(T)>0 from failing RD by this generic bound alone. It is not a new
Wilf theorem. One corrected bounded C diagnostic from the sole surviving anchor77 has no
accepted neighbor and is CLOSED. A preliminary19 run was already covered by this generic
bound. Neither diagnostic supports a general sign claim; do not enlarge them.

Taking residues of REDUNDANT input generators is incorrect. For <19,26,27,48,96>, first remove
96=2*48; the proper T is <7,8,10,19>, with W(T)=2. Reducing96 as if it were primitive would
add residue1 and produce a spurious T=ℕ. The new C path extracts minimal generators first.

### Integer realization of zero-trade directions — PROVED on paper

Let S be any proper numerical semigroup of multiplicity m>=2, with primitives p_1,...,p_d
other than m, d=e-1. Choose a canonical factorization tile z_s, s=0,...,m-1, with z_0=0 and
w_s=z_s.p. Let r be the largest-Apéry residue. Take an INTEGER vector v in Z^d, and put

    h_s=z_s.v,  V=max_j |v_j|.

Assume v annihilates every INNER PRIMITIVE trade:

    (z_s+e_j-z_t).v=0 whenever w_s+p_j=w_t.                (TANGENT)

For every integer L congruent1 modulo m with L>2m(m-1)V, the two generator sets

    S_L=<m,Lp_1,...,Lp_d>,
    S_(L,v)=<m,Lp_1+mv_1,...,Lp_d+mv_d>

are genuine numerical semigroups of multiplicity m and embedding dimension e. They have
exactly the original tight-pair pattern, the same canonical tile and largest residue r, and

    w_s(S_L)=Lw_s,       w_s(S_(L,v))=Lw_s+mh_s.           (REALIZE)

If H=d*m*z_r-e*sum_s z_s (E417), then exactly

    W(S_(L,v))-W(S_L)=H.v.                               (CHANGE)

**Proof.** Every minimum positive-weight word in a nonzero residue has length<=m-1. Otherwise
two prefix residues repeat; removing their positive-cost cycle produces a cheaper word in
the same residue. This remains true for the perturbed positive primitive costs. Consequently
it suffices to compare words in the finite set of length<=m-1 in each residue.

Every factorization of w_s has tight primitive prefixes. Induction on those prefixes and
(TANGENT) shows its v-weight equals h_s. In particular all equal-cost seed words stay tied;
this also proves h_i+h_j=h_t for EVERY tight pair, including composite parents.
Every other candidate word z has seed cost at least w_s+m. Its perturbed excess over z_s is

    L*(z.p-w_s)+m*(z.v-h_s) >= Lm-2m(m-1)V >0.

All costs Lp_j+mv_j exceed m under the stated bound. Thus (REALIZE) follows, and all minimum
factorizations (hence the canonical tile) are unchanged. A non-tight pair has perturbed gap
at least m*(L-3(m-1)V)>0, while tight gaps stay0. This preserves minimal primitive residues
and embedding dimension. Residues are unchanged because L=1 mod m, so gcd remains1.
For s!=r, the largest-value gap is at least

    L*(w_r-w_s)+m*(h_r-h_s) >= L-2m(m-1)V >0.

Thus r stays largest. Substitute (REALIZE) into E417's exact formula mW=H.p-C; the perturbation
of p is mv, giving (CHANGE). All quantifiers allow arbitrary m,e,height and depth. The coarse
bound is sufficient, not necessary; smaller L may be verified directly. No novelty claim is made.

### Feasible unpaid repairs persist — PROVED consequence

Under the same bound, each actual coordinate mu_s of BOTH constructed semigroups is at least
its seed value. The unperturbed scaling is immediate. For the perturbation, writing M=w_r,

    mu'_s-mu_s=(L-1)*(M-w_s)/m+h_r-h_s.

This is0 for s=r. Otherwise M-w_s>=1, |h_r-h_s|<=2(m-1)V, and L-1>=2m(m-1)V, proving
nonnegativity. The unpaid tight-row allowances alpha,kappa depend only on m,r, and the tight
pattern is unchanged. Therefore EVERY real feasible seed unpaid vector x remains feasible
for both actual integer semigroups, with certificate y'=mu'-x. In particular

    J(S_(L,v),x)-J(S_L,x)=H.v.

This realizes finite directional differences and existing weighted repairs at arbitrarily
large depth. It does NOT preserve the SIGN of a fractional actual/certificate objective under
scaling: the actual objective acquires a large homogeneous contribution. A negative real
finite LP minimum still cannot be called a genuine counterexample by clearing denominators.
In fact mW(S_L)=L*(mW(S)+C)-C, with C=(e-2)m(m-1)/2. The affine correction is not multiplied
by L, which is exactly why scaling is not a sign-preserving integrality argument.

### Common positive primitive shifts need not increase W — REFUTED, unbounded drops

Use the genuine seed <10,17,41>. In increasing primitive RESIDUE order p=(41,17), its canonical
tile has largest residue r=3, z_r=(3,0), sum z_s=(12,9), so H=(24,-27). All Apéry factorizations
are unique. For v=(1,1), h=(0,1,2,3,2,3,4,1,2,3) and H.v=-3.

The small directly checked realization L11 gives

    <10,187,451>: c1344,g705,e3,W573,
    <10,197,461>: c1374,g726,e3,W570.

Both nonmultiplicity primitives increased by10 while W decreased by3, with the tight pattern
and largest residue unchanged. The coarse theorem applies at L181, giving W9498->9495.
More generally take v=(N,N), L=180N+1 for ANY N>=1. The theorem gives genuine pairs with

    before W=9450N+48,     after W=9447N+48,

an arbitrarily large decrease -3N. Both numbers are positive. These examples are diagnostics
for a universal monotonicity assertion, not resistant Wilf cases (e3 is already known).
The direction eventually leaves the fixed-largest-residue region: h_6=4>h_r=3. Hence a
negative finite direction does not contradict E416's positive recession theorem.

The primitive affine objective can therefore have negative coefficients and decrease when
ALL primitive values increase. An allocation must retain the other largest-value/residue
constraints; neither positive primitive lower bounds alone nor a monotone lift argument pays
the finite correction. This does not refute RD, whose full residue reduction is a different
comparison. Do not turn the failed monotonicity into an unsupported claim that RD is impossible.

### A necessary cap load in an actual-coordinate allocation — PROVED linear consequence

Write a primitive actual-domain coefficient certificate as

    H=sum_strict lambda_b*n_b+sum_tight lambda_b*n_b
        +sum_j eta_j*e_j+beta*z_r+sum_s nu_s*(z_r-z_s),

where strict lambda,eta,beta,nu are nonnegative and tight lambda are signed. Let v annihilate
the tight trades and satisfy v_j>=0, n_b.v>=0 on strict primitive exits, z_r.v>=0. Taking
the dot product with v gives the necessary inequality

    sum_s nu_s*max(0,(z_s-z_r).v) >= -H.v.

Every other contribution is nonnegative; retain the negative cap terms on the left. This is
a necessary coefficient test, not a proof that any finite constants are paid. For the10seed
and v=(1,1), every strict primitive row has nonnegative dot product, and the ONLY negative
cap direction is residue6, with (z_6-z_r).v=1. Thus every such actual-domain certificate
requires nu_6>=3. A source-only allocation omitting these cap rows cannot even match H.
The checker independently reports all negative strict/cap directions. This concrete obstruction
explains why primitive positivity/strict exits must be coupled to other maximal Apéry residues;
it does not supply the still-missing uniform allocation or a new regional sign theorem.

**Checks/status.** Nine independent membership-based residue comparisons and four tangent
realizations are saved, including a signed v and a nonzero seed repair x_2=1 for <13,17,27,29>.
The last persists at L313 and after shifting all three primitives by13; its mass is1 in both.
Paper statements are not Lean checked. Reproduction and exact data are in EXPERIMENTS E431.

## E432 — a global closure/Hall formulation of finite support payment (2026-10-23)

**Scope.** Proves Wilf for: every numerical semigroup if the capacity inequality below holds
for every genuine canonical tile at its conductor phase in c>4m,3e<m. Proved reduction from
all S to this case: yes (SUPP-WILF and the recorded c<=4m/3e>=m complements). This is a
SUFFICIENT unproved target, stronger than Wilf. The graph identities and reductions below
are proved; their universal NONNEGATIVE SIGN is not. No reduction to the41 checked tiles exists.
The boundary S=ℕ has c=0 and W=0 separately; the tile discussion concerns proper S.

### Definitions and the completion claim — CONJECTURED

Use a canonical tile D subset N^d, |D|=m, d=e-1>=1, primitive residues delta_j in[1,m-1].
The residue map phi(z)=z.delta mod m is bijective. Fix the ACTUAL conductor phase rho=(-c) mod m,
and set r(z)=(phi(z)+rho) mod m. For any down-set E subset D, including the empty set, define

    kappa(z)=floor(sum_j <z_j*delta_j>_m/m),
    kappa(E)=sum_(z in E) kappa(z),
    Dep(E)=sum of lengths of coordinate columns whose top is nonmaximal in E,
    N(E)=sum_(coordinate columns C of E) #{z in C:r(z)>r(top C)}.

The proposed completion inequality is

    Q(E):=Dep(E)+N(E)-kappa(E)+m-|E| >=0.                  (COMP, UNKNOWN)

It allows one credit per MISSING residue; it does not require positivity of each partial tile.
At E=D, COMP implies W>=Dep(D)+N(D)-kappa(D)>=0 by SUPP-WILF. A failure for proper E would
refute COMP, not Wilf or necessarily even the complete-tile support inequality. An arbitrary
injective partial tile need not be a genuine canonical tile; that hypothesis is not discarded.

### Inversion linearization — PROVED for every down-set E subset D

Define the prefix inversion potential, with I_j(z-e_j)=0 when z_j=0,

    I_j(z)=#{1<=k<=z_j:r(z-k*e_j)>r(z)},
    eta(z)=sum_j (I_j(z)-I_j(z-e_j)).

Then exactly

    N(E)=sum_(z in E) eta(z).                             (INV-LIN)

Proof: the top indicator of z in its j-column of E is b_z-b_(z+e_j), with b=1_E and an absent
successor interpreted as0. A column whose top is z contributes I_j(z). Expanding the top
indicators and reindexing telescopes to INV-LIN. Every E-column is a prefix of a D-column,
so I_j is the same potential for every sub-tile, not recomputed at a missing prefix.

Let omega(z)=d+|z|. Since each maximal cell of E ends d columns of total length d+|z|,

    Dep(E)=d|E|-sum_(z maximal in E) omega(z).

Consequently

    Q(E)=m+sum_(z in E) c(z)+sum_(z nonmaximal in E) omega(z),
    c(z)=eta(z)-kappa(z)-|z|-1.                           (CLOSURE)

Only the nonmaximal indicator is nonlinear. It is the OR of the selected immediate successors;
thus the full expression is a minimum-weight closure, not an exponential down-set enumeration.

### Every cell benefit is positive: a useful exact simplification — PROVED

Put K(z)=floor(z.delta/m). Translation of two residues around the circle gives

    I_j(z)-I_j(z-e_j)=z_j*[delta_j>r(z)]-floor(z_j*delta_j/m).

For completeness, compare the pairs <k*delta_j> and r(z) with their simultaneous predecessors
< (k-1)*delta_j > and r(z-e_j). The change in the strict-order indicator is the wrap of the
second residue minus the wrap of the first. Summing k=1,...,z_j yields the displayed formula;
the k=0 indicator is0 and the axis wrap counts telescope. Also
kappa(z)=K(z)-sum_j floor(z_j*delta_j/m). Therefore

    beta(z):=-c(z)
      =1+K(z)+sum_(j:delta_j<=r(z)) z_j >=1.               (BETA)

The implementation derives c from column inversions; the independent checker ALSO verifies
this closed formula. No nonnegative sign theorem for Q follows just from beta>=1.

### Exact minimum-cut and weighted Hall reductions — PROVED

Let B=sum_D beta(z). Make cell nodes b_z of benefit beta(z) and auxiliary nodes o_z of cost
omega(z). For every immediate edge z->t=z+e_j in D add implications

    b_t -> b_z,       b_t -> o_z.

Closure-selected cell nodes form a down-set E. Because omega>0, an optimal closure selects
o_z exactly when z is nonmaximal in E. Thus its minimum cost is min_E(Q(E)-m).

Equivalently construct a flow network with source->b_z capacity beta(z), o_z->sink capacity
omega(z), and the implication arcs of capacity B+1. A cut of capacity<=B always exists,
so a minimum cut cannot cross an implication. If F_max is the exact maximum flow, then

    min_(E down-set of D) Q(E)=m+F_max-B.                 (CUT)

The closure-to-cut step is standard (Picard, Management Science22(11),1976,1268-1272,
doi:10.1287/mnsc.22.11.1268); the argument above is self-contained. No novelty is claimed
for that algorithm. The inversion/benefit formulation retains the actual cyclic labels.

The sparse network is also equivalent to a bipartite network from each cell z to every
PROPER divisor u<z, with cell demand beta(z) and divisor capacity omega(u). Unlimited paths
through the b nodes give exactly these reachable sinks. For X subset D put
P(X)={u in D:u<z for some z in X}. The generalized Hall deficiency is

    Delta_H=max_(X subset D) (sum_X beta-sum_(u in P(X)) omega).

Adding every missing proper divisor to X never adds a new neighbor and increases benefit,
so this maximum is attained at a down-set E, whose neighbor set is precisely its nonmaximal
cells. Max-flow/min-cut gives Delta_H=B-F_max and hence

    COMP <=> Delta_H<=m.                                 (HALL, SIGN UNKNOWN)

This is the precise uniform finite capacity theorem that would prove Wilf through this
route. Matching coefficients or computing F_max for individual profiles is not its proof.

An immediate necessary restriction on a bad cut is worth retaining: it cannot have height<=1.
For E={0} plus k primitive cells, beta(0)=1 and every primitive benefit is at most2. If k>0,
the only neighbor is0, of capacity d, so its deficiency is at most1+2k-d<=d+1=e<=m. The
empty and singleton cases are also harmless. Thus the numerous shallow positive cuts in the
saved diagnostic are elementary, not evidence from hard cases. This restricts a hypothetical
violating CUT, not the height or embedding dimension of the semigroups under investigation.

### What a constructive flow can already pay — PROVED identities, incomplete allocation

The degree contribution has a canonical allocation: cell z sends z_j units toward its parent
z-e_j's auxiliary node. The total potential incoming degree at u is

    sum_(j:u+e_j in D) (u_j+1) <= d+|u|=omega(u).

Its unused amount is Gamma_D(u)=sum_(j:u+e_j notin D)(u_j+1). Only NONMAXIMAL auxiliary
nodes have incoming paths, so the corresponding total available boundary reserve is Dep(D).
This is a parent-capacity identity, not necessarily a feasible flow under the actual beta:
some cell benefits are smaller than their degrees and require redistribution.

There is also an exact inversion redistribution along cell arcs: assign I_j(u) to the arc
b_(u+e_j)->b_u. At cell z its incoming minus outgoing amount is

    eta(z)-sum_(j:z+e_j notin D) I_j(z).

After the degree allocation, the remaining signed cell balance is therefore

    1+kappa(z)-sum_(j:z+e_j notin D) I_j(z).

These balances may be negative; this preflow is NOT asserted feasible. A global rule must
resolve them using the actual residual capacities while leaving at most m units unrouted.
No column, cell or direction is assumed to pay separately. This is the next constructive
obligation, rather than another positive-instance optimization.

### One free unit fixed at each cell is insufficient — EXACT obstruction

In the saved genuine S=<114,305,307,310>, the exact optimal cut contains34 cells and has
Q=75, so Dep(E)+N(E)-kappa(E)=-5. Its Hall demand exceeds its divisor capacity by39 units.
Allowing ONE unmatched unit at each selected cell would permit only34 units; that local
allocation fails by5. The proposed GLOBAL budget m=114 allows it. This refutes the stronger
cellwise allocation, not COMP or Wilf. Exact source weights, cut and integer flow are saved.

**Closed diagnostic/status.** Principal-upset/value-prefix testing on41 existing seeds found no
failure. Exact cuts on the SAME41 seeds then optimized over ALL their down-sets; all minima
were nonnegative, and independent exhaustive ideal enumeration agreed on the13-point tiles
(14,52,166 ideals respectively). These are algorithm/certificate checks, NOT a new unresolved
semigroup census or a universal sign argument. The diagnostic is CLOSED; do not enlarge it.
The general identities/reductions are paper-proved, not Lean checked. The finite Hall inequality
remains unproved, and may be stronger than necessary even if Wilf is true.

## E433 — critical cuts, phase drift, and a falsified interior payment (2026-10-23)

**Scope.** Proves Wilf for: every numerical semigroup IF the E432 Hall bound holds throughout
c>4m,3e<m. Proved reduction from all S to this case: yes, E432/SUPP-WILF and the recorded
complement theorems. The results below constrain that universal allocation; they do not prove
its sign. No restriction to the four checked semigroups, embedding dimension or height is made.
All general assertions here are paper proofs, not Lean checked. No novelty claim is made.

### Deleting a critical cut — PROVED necessary conditions

Write h(E)=sum_E beta-sum_(nonmax E) omega. Choose an inclusion-minimal maximizer E of h
among down-sets. Such E is the cell set reachable from the source in the residual network of
an E432 maximum flow: residual reachability is contained in every minimum source-side cut.
Alternatively, in a contradiction proof choose an inclusion-minimal E with h(E)>m. The
following strict deletion inequality holds in either situation.

If V is a nonempty upper ideal of E, then E\V is a down-set and

    sum_V beta > sum_(u in nonmax(E) \ nonmax(E\V)) omega(u).       (CRIT)

Indeed the difference of the two sides is h(E)-h(E\V), which is strictly positive by the
choice of E. For a maximal cell z, let P_z consist of its immediate parents whose ONLY
immediate child in E is z. Exactly those parents become maximal on deleting z. Thus

    beta(z) > sum_(u in P_z) (d+|u|).                           (PRIVATE)

For n=|z|>0, K=floor(z.delta/m)<=n-1, hence beta(z)<=2n. Every member of P_z has
capacity d+n-1. If d>=2, there can be at most one private parent. If there is one, put
T=sum_(j:delta_j>r(z)) z_j. Since beta=1+K+n-T, PRIVATE implies

    K-T >= d-1,             n>=d.                             (CARRY-PRIVATE)

These are restrictions on a potentially bad CUT, not a restriction of the semigroup domain.
They are not sufficient for a violation: the saved114 cut has14 maximal degree4 cells,
all with NO private parent, and still h=39<m114. Replacing the global problem by leaf removal
would discard this shared-parent core.

### Moving the phase — PROVED exact identities, not a semigroup construction

Keep E,D,delta fixed and replace rho by any rho in Z/m. Let h_rho(E) be its deficiency and
Gamma_E(v)=sum_(j:v+e_j notin E)(v_j+1). Let v be the unique cell in D with
phi(v)=m-1-rho modulo m. Then

    h_(rho+1)(E)-h_rho(E) = d-Gamma_E(v) if v in E, else 0.    (PHASE)

To prove this, the indicator [delta_j<=r(z)] gains1 only at r(z)=delta_j-1 and loses1
at r(z)=m-1. The first event has parent v=z-e_j, so its total positive contribution is
sum_(j:v+e_j in E)(v_j+1). The negative contribution is |v| when v belongs to E.
Their difference is d-Gamma_E(v). A parent outside E has no child inside a down-set.

For each cell, averaging the BETA formula over phases gives

    mean_rho beta_rho(z)=1+|z|-phi(z)/m.

Using Dep(E)=d|E|-sum_max(E)(d+|z|), it follows that

    sum_(rho=0)^(m-1) h_rho(E)=m(|E|-Dep(E))-sum_(z in E)phi(z). (MEAN)

In particular the mean completion budget is m-|E|+Dep(E)+sum_E phi/m>=0. This does NOT
bound its phase minimum. For E=D the mean deficiency is (m+1)/2-Dep(D), a rewriting of the
older column/carry averaging identity; the extension here keeps a fixed proper cut. Other
phases are not asserted to be realizable conductor phases with the same actual generators.

### Interior-only payment — FALSE, including a zero-carry obstruction

For the active coordinates J of E put Delta_J={0} union {e_j:j in J}, and
A={u:u+Delta_J subset E}. The standard cross-sum argument proves that the residue map is
injective on A-Delta_J: equal residues of u-v and u'-v' imply equal residues of u+v' and
u'+v, both in E. Consequently

    L(E):=|A-Delta_J|=|A|+sum_(j in J)|{u in A:u_j=0}| <=m.

The tempting allocation claim h(E)<=L(E) is FALSE. A fully checked cut in
S=<40,41,42,43>, m40,e4,c520,g273,W468, has canonical words

    E={0,e_1,e_2,e_3,2e_2,e_2+e_3,2e_3},  delta=(1,2,3), rho=0.

Its benefits in that order are 1,2,2,2,3,3,3 (total16). The nonmaximal cells are
0,e_2,e_3 with capacities3,4,4 (total11). Hence h(E)=5. But A={0}, so L(E)=4.
Direct columns give Dep=2,N=0,kappa=0. Thus the missing unit is NOT caused by modular
carry loss: the joint interior misses boundary contributions even in a zero-carry cut.
This is a counterexample in the actual remaining domain, not a Wilf failure (W468>0).

An independently audited62 cut in <62,87,88,89> has h30,L16. A discovery pass through the
same41 old selected cuts found five failures; only these two are used as the audited
falsifications. No new semigroup population was enumerated. Stop interior-only payment.

### A directional residue pool — explicit replacement target, UNKNOWN

The failed joint interior required every primitive successor. Retain direction-specific
boundary starts instead. For every E define the set of RESIDUES

    U(E)={0} union phi(nonmax E)
             union {phi(u)-delta_j mod m:u in E,u_j=0,u+e_j in E}.

Coincident residues are counted ONCE. The new sufficient claim is

    h(E)<=|U(E)| for every genuine D and every down-set E.     (POOL, UNKNOWN)

Since U(E) subset Z/m, POOL implies the E432 Hall bound. It is a global residue allocation,
not one credit fixed at each selected cell. Height<=1 cuts satisfy it: for k active unit
cells U={0,-delta_j}, so |U|=k+1, whereas h<=1+2k-d<=k+1. This checks a necessary boundary,
not a reduction of the research domain.

There is an exact min-cut falsification test. Extend E432's graph by pool nodes p_s, with
p_s->sink capacity1 for s!=0 and capacity0 for s=0. For every canonical edge u->z=u+e_j,
add implications b_z->p_(phi(u)) and, if u_j=0, b_z->p_(phi(u)-delta_j). The first implication
activates precisely nonmaximal residues, and the second activates the directional starts.
Thus selected pool nodes of positive cost are exactly U(E)\{0}, and

    min_E (|U(E)|-h(E)) = 1+maxflow-sum_D beta.              (POOL-CUT, PROVED)

This is another standard closure reduction, not a proof of POOL. Since b_0 has benefit1
and no outgoing implication, its unit cannot be routed. POOL is equivalently the assertion
that ALL nonzero cell sources can be routed simultaneously using divisor capacities and
the permitted nonzero pool units. This makes the constructive obligation explicit.

Simple maximal-cell induction is insufficient: adding a cell with already-nonmaximal
parents can add positive beta without adding any pool residue. Earlier slack must be
retained and redistributed; no individual step is assumed to pay for itself.

Selected old maximum-h cuts pass POOL on the41 saved fixtures, which does NOT check every
cut for this different objective. Exact POOL-CUT then checks ALL cuts of just the40 and114
tiles; both have minimum0, attained at E={0}. Integer flow/cut and independent membership
audits verify these two regional statements. They are CLOSED diagnostics, not a uniform
sign theorem. Do not launch another positive-profile list. The next proof task is the
simultaneous routing construction above, retaining the weaker E432 target if POOL fails.

### Global review / stopped approaches

An unspecified supported matrix with nullity<=m is not a mechanism: after expanding the
integer source/sink capacities into unit copies, existence of rank>=sum beta-m is equivalent
to the same Hall bound (a nonzero minor gives a matching; a matching gives such a matrix).
No arithmetic operator with that rank was constructed. Stop this restatement unless an
explicit operator and a new kernel proof are supplied. Stop joint-interior-only credit,
which fails even with kappa=N=0. Continue the directional/global residue routing problem,
not additional reconstruction accuracy. Weighted repair coupling and actual arithmetic/
integrality remain the other two universal lines; no restricted-family programme is opened.
The two pool certificate bundles are saved as data/completion_pool_probe.jsonl.gz.

## E434 — a nonnegative partial allocation and a joint carry/alias budget (2026-10-23)

**Scope.** Proves Wilf for: every numerical semigroup IF the fixed partial allocation below
can always be extended in the remaining domain c>4m,3e<m. Proved reduction from all S to
this case: yes, extension implies E433 POOL, then E432/SUPP and the recorded complements.
The extension is a STRONGER, UNKNOWN claim. This section proves the partial allocation and
its exact residual identities, not extension or Wilf. No fixed height/e family is a target.

### A genuinely feasible partial flow — PROVED

Use E432's genuine canonical D, delta, phase rho, labels r, benefit beta and omega=d+degree.
Put K_z=floor(z.delta/m). On an edge u->z=u+e_j call the edge nonwrapping when

    r(u)+delta_j<m, equivalently delta_j<=r(z).

Assign u_j+1=z_j units from source z directly to its proper-parent auxiliary u on every
such edge. At source z this consumes exactly

    A_z=sum_(j:delta_j<=r(z)) z_j,

so beta_z-A_z=1+K_z is positive. At parent u the consumed components are a subset of
the disjoint components u_j+1 whose total is omega_u. Thus every source and sink capacity
is respected; this is a feasible PARTIAL flow, unlike the signed preflows in E432. The
origin's unit is reserved separately and has no outgoing proper-divisor arc.

Define capacities on the WHOLE D,

    Gamma_u=sum_(j:u+e_j notin D)(u_j+1),
    V_u=sum_(j:u+e_j in D, r(u)+delta_j>=m)(u_j+1),
    R_u=omega_u-sum_(nonwrapping children)(u_j+1)=Gamma_u+V_u>=0.

The remaining nonzero source demands are d_z=1+K_z (d_0=0). Keep E433's parent implications
and directional pool with unit capacities at nonzero residues. A flow meeting all d_z extends
the partial allocation; prescribed nonwrap amounts may not be reversed in this stronger
model. No claim that this freezing is without loss is made.

### Residual cuts, leakage and required wrap use — PROVED

For any nonempty down-set E, P=nonmax(E), S_E=sum_(z in E\{0})(1+K_z), define

    F_res(E)=sum_(u in P) R_u+|U(E)|-1-S_E.

For E empty set F_res=0. The residual network's exact minimum is maxflow-sum_(z!=0)d_z.
All source demands can be met iff F_res(E)>=0 for every E. This sign remains UNKNOWN.

The new claim is stronger than POOL by an explicit boundary term:

    F_res(E)=|U(E)|-h(E)-Leak(E),
    Leak(E)=sum_(u in P,j:u+e_j in D\E, nonwrapping)(u_j+1)>=0.

Proof: internal nonwrap assignments with children in E are exactly sum_E A_z. Residual
sink capacities at P subtract those assignments AND the assignments to outside children,
whereas the source demands subtract only the internal ones. beta_0=1 cancels the reserved
origin unit. This gives the identity. At E empty the pool margin is1 and the residual
margin0; do not apply the nonempty formula there.

Any residual allocation must use at least

    max(0,S_E-sum_P Gamma_u-(|U(E)|-1))                    (WRAP-LOAD)

wrapped capacity for sources in E. Their parent paths stay inside E; all accessible auxiliary
nodes lie in P and all accessible free residues lie in U(E). Missing-direction and pool
capacities cover at most the two subtracted amounts. This is necessary, not sufficient.

### Why aliases cannot be paid separately — exact remaining-domain obstruction

Take the recorded S=<19,39,41,50,52,53>, m19,e6,c88,g68,W32, rho7. Its unique canonical tile
has height2:0, all5 units, and13 pairs. The missing pairs are e_1+e_4 and e_2+e_3 in residue
order delta=(1,3,12,14,15). All5 squares occur. Thus P has6 cells and Gamma_D(P)=Dep4.

Let F be the set of directional starts (u,j) with u_j=0 and u+e_j in D. There are5 origin
starts and2 for each of the8 mixed pairs, so |F|=21. The formal Laurent monomials indexed
by P together with u-e_j for these starts are27 distinct words. Their map to k[Z/19],
sending a word to its residue basis vector, has image U(D), of cardinality15:

    U(D)={0,1,2,3,4,5,7,8,11,12,14,15,16,17,18}.

Its kernel therefore has dimension12. A proposed injection of ALL these alias relations
into the4 missing-direction slots is impossible. Even all11 residual auxiliary slots
would not inject that12-dimensional kernel. This refutes that SEPARATE rank payer, not the
residual allocation: the formal27 credits also exceed the actual expanded demand25 by2.
One cannot treat each formal relation as an independent additional debt.

The exact actual residual accounting is

    sum K=6,  nonzero demand=18+6=24,
    sum_P Gamma=4,  sum_P V=7,  |U|-1=14,
    whole-tile residual margin=4+7+14-24=1.

WRAP-LOAD forces at least6 of the7 wrapped units to be used. The missing-direction, carry
and cyclic-alias contributions must therefore be coupled. This example is an already
settled Wilf case, selected as a sharp auxiliary-budget obstruction, not presented as a
new resistant semigroup or a proof for a restricted family.

### Checks, duplicate shortcut and next proof obligation

Pure C --support-frozen-cut exports exact residual flows/cuts. Independent membership and
definition-level audits certify extension on ALL cuts of the existing40 and114 tiles.
The19 tile above was added ONLY to test the separate-alias obstruction; its all-cut residual
minimum is also0. In all three residual certificates the smallest optimal cut is EMPTY,
unlike the original POOL minimum at {0}. The full19 cut has margin1, not0. These three
diagnostics are CLOSED. No positive-profile census is warranted.

Residual charges can be indexed by nonnegative integers z.delta-km, 0<=k<=K_z, with the
origin removed. Distinct residue classes make this representation injective. Even after
adding back0, the lift set need not be closed under subtracting an arbitrary primitive residue. Such closure is
equivalent to z_s.delta being the actual Apéry values of T=<m,delta>, the earlier U=T
hypothesis, not a consequence of a genuine S. In the old <10,17,41> example the raw values
in residue order are(0,1,2,3,14,15,16,7,8,9);14 occurs among the lifts but13=14-1 does not.
Do not reuse numerical-semigroup closure arguments on this lift set without that hypothesis.

**Global review.** The positive partial flow removes the old signed source debt and isolates
the exact joint target S_E<=Gamma_D(P)+V_D(P)+|U(E)|-1. It does not explain that sign.
Stop the phase-insensitive alias payer and the duplicate U=T shortcut. The next proof task
is a SINGLE joint allocation of the actual lift charges using wrapped capacities and residue
aliases together; do not give each alias relation, column or phase layer its own budget.
No more positive instances are next. If freezing proves too strong, retain the unfrozen
E433 pool or weaker E432 allowance. Full weighted coupling and actual arithmetic/integrality
remain the other universal lines. All general proofs here are on paper, not Lean checked.

## E435 — internal aliases have distinct slots; the remaining joint defect (2026-10-23)

**Scope.** Proves Wilf for: every numerical semigroup IF the joint inequality below holds
for every cut of every genuine tile in c>4m,3e<m. Proved reduction from all S to this case:
yes, it is exactly E434's residual sign after a proved cancellation, followed by E433/E432
and the recorded complements. The uniform sign is UNKNOWN. The zero-resource result below
excludes certain CUTS from a counterexample; it is not a restricted semigroup programme or
a proved reduction of all S to those easy cuts. No novelty claim or Lean verification.

### Internal aliases consume distinct canonical-exit slots — PROVED

Fix a down-set E inside D with |E|>=2 and put P=nonmax(E), A=max(E). Write

    F={(v,j):v in E,v_j=0,v+e_j in E},
    psi(v,j)=phi(v)-delta_j mod m,
    F_in={(v,j) in F:psi(v,j) in phi(P)}.

Here every base v in F belongs to P. Residue injectivity identifies cells with their
residues when forming U(E)=phi(P) union psi(F);0 already lies in P. For (v,j) in F_in,
let u in P have phi(u)=psi(v,j). Then u+e_j is NOT in D: if it were, its residue would
equal phi(v), forcing u+e_j=v, contrary to v_j=0. Assign this start the missing-direction
slot (u,j,0), among the u_j+1 slots of that canonical exit.

This assignment is INJECTIVE. Equal slots give equal u and j, hence equal residues of v
and then equal v. Therefore

    |F_in| <= number of missing directions at P <= Gamma_D(P).

This pays the internal alias subspace by explicit distinct slots. It is not an assertion
that all aliases are paid, or an extension of the actual source flow. Nor is a canonical
exit assumed a strict actual semigroup gap: a different word may give a zero-gap trade,
as in the old E420 example. The slot injection uses only absence of the CANONICAL word.

Formally, use Laurent-monomial basis vectors indexed by P and v-e_j for F. They are all
distinct. Evaluation into k[Z/m] sends them to their residue basis vectors. For each
internal start the kernel vector e_(v-e_j)-e_u is independent of the others, and the slot
map above gives an injective linear map on this internal kernel subspace. This is a
constructed map, unlike an unspecified matrix with an assumed rank bound.

### Nonnegative surplus and exterior debt — PROVED exact reformulation

Group the remaining starts by their image outside phi(P), with group sizes q_b, and set

    L_out=sum_(b outside phi(P),q_b>0)(q_b-1),
    K(E)=sum_(z in E) floor(z.delta/m),
    C(E)=|F|-|A|,             G_rem(E)=Gamma_D(P)-|F_in|.

Both C and G_rem are nonnegative. For C, choose any positive coordinate j of each maximal
cell z and assign it its j-column start (z-z_j e_j,j). This belongs to F. Distinct maximal
cells cannot be tops of the same j-column, so these choices are injective. The complement
consists of C unused starts. Nonnegativity of G_rem follows from the slot injection.

The complete alias rank loss is |F_in|+L_out: starts landing in P each add one relation;
an exterior group of size q contributes q-1. Also

    |U(E)|=|P|+|F|-|F_in|-L_out,
    S_E=|P|+|A|-1+K(E).

Substitution in E434 gives the EXACT identity

    F_res(E)=C(E)+G_rem(E)+V_D(P)-L_out-K(E).                (JD)

Thus the universal target is now

    L_out+K(E) <= C(E)+G_rem(E)+V_D(P).                    (JD+, UNKNOWN)

Every displayed debt and resource is nonnegative. This isolates a uniform valid payment
for internal aliases, but JD itself is an accounting identity, not a reason for JD+.
A proof by an injective map must actually construct the remaining map from exterior alias
relations AND raw carry copies to unused starts and the remaining missing/wrapped slots.
Their dimension inequality alone would only restate the unknown sign.

### A safe-cut lemma and zero-resource base — PROVED for all genuine tiles

If Gamma_D(P)=0, every cell of P has every primitive successor in D. Then psi is injective
on ALL of F, and its image is disjoint from phi(P). Disjointness follows from the internal
slot argument. For two distinct directions j,k, equality psi(v,j)=psi(v',k) would give
equal residues for v+e_k and v'+e_j, both in D. They cannot be equal vectors: their
j-coordinates are0 and at least1, respectively. For equal directions injectivity of phi
already forces v=v'. This is the standard E420 cross-sum argument, not a new difference
principle. Consequently F_in=L_out=0.

It follows that ANY cut with Gamma_D(P)=0 AND K(E)=0 satisfies

    F_res(E)=C(E)+V_D(P)>=0.                               (SAFE)

In particular, if the TOTAL residual parent resource Gamma_D(P)+V_D(P) is0, then K(E)=0
as well. All internal E edges are nonwrapping; along a word path from0, phase labels
increase by delta_j without wrapping. Hence rho+z.delta<m for every z in E, so raw carry
vanishes. Therefore such a cut has F_res(E)=C(E)>=0. Empty and singleton cuts are harmless
separately. A putative negative cut must leave this regime. This is a proved cut exclusion,
not a universal proof or an instruction to study only zero-carry semigroups.

### Two incompatible fixed splits — exact existing-cut obstructions

On the full19 tile <19,39,41,50,52,53>, the independent decomposition gives

    F_in4, L_out8, K6;     C8, G_rem0, V7.

The joint margin is15-14=1. If unused starts were reserved ONLY for carries, exterior
debt8 would have only G_rem+V=7 available. Thus that fixed rule fails by at least1.

On the OLD34-cell optimal h-cut of <114,305,307,310>, it gives

    F_in2, L_out2, K54;    C15, G_rem2, V45.

The joint margin is62-56=6. If unused starts were reserved ONLY for exterior aliases,
raw carries54 would have only G_rem+V=47 available, a shortfall7. Wrapped capacity ALONE
is also insufficient,54>45. These are counterexamples to proposed separate type budgets,
not to JD+, the residual flow or Wilf. In this accounting at least9 of the15 unused starts
are needed in total on the114 cut. An actual construction must allow their use to adapt.

### Operator trial / global review

A scalar cyclic-lowering trial cannot supply the missing rank theorem. Let X_j be the
cyclic residue shift, Z_j the diagonal canonical coordinate, and M_j the diagonal indicator
of a j-successor in E. The explicit map T=sum_j c_j X_j^(-1)(Z_j+M_j) has image in the
formal residue pool. But on E={0,e_1,...,e_d}, every unit maps to c_j e_0; only the origin
adds one more image vector. Its rank is2 for nonzero generic c, whereas |E|=d+1 and
Gamma_D(P)=0. For d>=2 this refutes the hoped-for nullity<=Gamma bound, even on the safe
40-tile control. Tuning its scalar weights cannot cure that symbolic obstruction.

The valid advance is the internal slot map and safe-cut exclusion, not a general positivity
claim. Stop scalar-lowering rank tuning and either fixed type budget. Continue the JOINT
exterior-alias/carry construction with the explicit nonnegative resources in JD. This is
still the actual boundary/residue line; weighted full repair and arithmetic/integrality
remain active alternatives. No larger profile census or narrower-family programme is opened.
Existing flow certificates were reused only to audit the new decomposition on three full
tiles, their old selected cuts and two zero-resource controls. These are closed checks.

## E436 — sum-dominant sets refute a staged exterior payment (2026-10-23)

**Scope.** Proves Wilf for: every numerical semigroup IF exterior aliases can be paid from
C first and the remaining joint carry budget can then be paid universally. Proved reduction
from all S to the COMBINED claims: yes, their sum gives E435 JD+, then E434/E433/E432/SUPP
and the complements. This section REFUTES the first intermediate claim L_out<=C on genuine
semigroups in the remaining domain. It does not refute JD+ or Wilf, and does not activate a
sum-dominant-family proof target. The new proof attempt is the cross-exit map below; its
capacity collision is exhibited, so independent least-root choices are stopped too.

### A general genuine-semigroup lift — PROVED obstruction theorem

Let H subset [0,R] be finite, R>=1,0 in H,gcd(H)=1, d=|H|. Put

    T=R+1, B=T+H, m=4max(B)+2=8R+6,
    S=<m, m+b (b in B)>, s=|H+H|, t=|H-H|.

Every generator m+b lies strictly between m and2m and is minimal. Thus multiplicity is m
and embedding dimension d+1. The generator gcd is1, since common divisors divide all
differences H and hence1. Therefore S is a numerical semigroup. Also3(d+1)<=3R+6<m.
The integer5m-1 is a gap: a representation below5m uses at most4 positive generators;
its sum of non-multiplicity residues is at most4max(B)=m-2, so cannot have residue m-1.
Consequently c>=5m>4m. This verifies the genuine remaining-domain hypotheses uniformly.

Every value2m+b+b' is Apéry. Its residue b+b' lies below m and above max(B), so it is
neither0 nor a primitive residue. Subtracting m gives a number below2m which is not a
generator. Equivalently a representation with3 positive generators is too large. Choose
canonical pair words for the s distinct pair values and form the down-set E consisting
of0, all d units and those pair words. This is a cut of the actual canonical D, for ANY
monomial tie order. It has at least s maximal cells, and all its raw carries are0.

Every negative start image belongs to

    (-B mod m) union ((H-H)\{0} mod m).

Indeed origin starts give -b; a mixed pair gives a difference b-b'. These sets are
disjoint from0 and B: B lies in[R+1,2R+1], differences in[-R,R], and m=8R+6 prevents
modular overlap. Thus F_in=0 for every choice of representatives and

    |psi(F)|<=d+t-1,
    L_out-C = |max(E)|-|psi(F)| >= s-d-t+1.                 (MSTD-OBSTRUCTION)

In particular ANY normalized set with s-t>=d refutes the proposed exterior stage. The
lower bound does not depend on the canonical tie order. One cannot rescue this all-S
stage simply by selecting different pair representatives. This is a general obstruction
to an intermediate claim, not a universal Wilf theorem or a new MSTD construction.

### Explicit witness and independent verification

Use the classical seed H0={0,2,3,4,7,11,12,14} and

    H={a+29b+29^2 c:a,b,c in H0}.

The seed and base-expansion method are standard; see [Hegarty, introduction](https://arxiv.org/html/math/0611582v2)
and [Chu–McNew–Miller–Xu–Zhang, section3.1](https://cs.uwaterloo.ca/journals/JIS/VOL21/Miller/miller8.pdf).
No novelty is claimed for these sets. Directly H0+H0=[0,28]\{1,20,27}, while
H0-H0=[-14,14]\{-13,-6,6,13}. Base29 encodes sum digits uniquely. Difference digits
are also unique: subtracting two digit representations has coefficients in[-28,28],
so reduction modulo29 forces each coefficient0 successively. Hence

    d=8^3=512, s=26^3=17576, t=25^3=15625, R=12194,
    T=12195, m=97558, e=513, s-d-t+1=1440.

One genuine S is therefore specified by just this formula and m, without a generator-list
ambiguity. Independent residue shortest paths (C++) and unbounded-coin membership DP
(Python stdlib bitset) agree on ALL97558 Apéry entries and give

    c623660, g383166, ell240494, W122749762>0, rho59246.

For the project's first-coordinate lex convention all squares are canonical: among pair
words for2b_i, any other pair has a smaller least generator index and a larger earlier
coordinate. Thus all units are nonmaximal in E, and the exact cut counts are

    |E|18089, |nonmax E|513, |max E|17576,
    |F|34640, |psi(F)|3652, F_in=K=0,
    L_out30988, C17064, L_out-C13924>0.

The stronger representative-independent lower bound is1440;13924 is the checked LEX value,
not a claim to have enumerated all monomial orders. JD on THIS PAIR CUT is not violated:

    Gamma_D(P)=227504, V_D(P)=14090,
    C+Gamma+V-L_out=227670>0.

At this ACTUAL phase C+V-L_out=166 as well, so the witness does not establish that Gamma
is individually necessary. It establishes that exterior aliases cannot be restricted to
C alone: missing OR wrapped resources must remain available to the joint argument.
No optimization over all down-sets of this large D was performed or claimed.

Here Gamma=d(d+1)-2s counts noncanonical ordered pairs. Every one of those missing canonical
pair directions is a ZERO actual-gap trade to a different pair word of the same weight.
Do not read this combinatorial capacity as a positive strict-exit margin. The cut disproves
the staged C-only claim even without carries, but provides no Wilf counterexample. It also
does not refute a differently stated claim with extra hypotheses from proved Wilf exclusions.

### A corrected cross-exit association — PROVED, not injective

For an exterior image group of starts (v,j), order the signed words v-e_j by actual weight
v.p-p_j, then by the project's monomial tie order. Choose its least root (w,k). For every
other start (v,j), j!=k and

    v+e_k is a canonical exit at v in P.

Proof: the root signed word is strictly smaller. Adding e_j+e_k preserves that order,
so w+e_j is a strictly better word than v+e_k in the same residue. This excludes v+e_k
from the canonical Apéry basis, whether the improvement is in actual weight or just the
tie order. This constructs an association to a missing-direction slot family. It does
NOT prove that distinct relations fit into distinct available slots.

In the SAME witness let u_a denote the unit corresponding to residue T+a. The starts

    (u_14,j_12), (u_14,j_11)

have images2 and3, with least roots (u_2,j_0) and (u_3,j_0), respectively. The four relevant
mixed pairs are canonical; within each group all actual signed weights are equal, and the
root has the negative coordinate at the earliest index0. Both nonroot relations therefore
map to the SAME exit u_14+e_(j_0), of capacity1. Its canonical replacement is2u_7, since
14+0=7+7. Thus two relations compete for one slot. This is explicitly checked by the audit;
independent least-root selection is not a capacity-respecting injection.

### Global review / next obligation

Stop the C-only exterior stage and independent least-root charging. The connection with
sum/difference sets explains why that stage fails globally; it is not evidence against
the full joint target. The corrected root association uses actual primitive weight/tie
comparisons and locates real canonical exits, but needs a GLOBAL exchange rule to resolve
collisions using unused starts, unreserved missing slots and wrapped capacity together,
while retaining the raw carry charges. No such rule is proved here. Do not repeat this
witness as a positive census or implement another numerical root optimizer without a new
uniform lemma. Keep JD+/unfrozen POOL/E432 and the other two universal lines available.
All general statements are paper proofs, not Lean checked; novelty of this application
has not been established. Exact code/data and reproduction are in EXPERIMENTS E436/STATE.

## E437 — a forest exchange and the cycle remainder (2026-10-23)

**Scope.** Proves Wilf for: every numerical semigroup IF the remaining cycle-and-carry
budget below holds for every genuine tile cut in the remaining domain. Proved reduction
from all S to this case: yes, exact cancellation gives E435 JD+, followed by
E434/E433/E432/SUPP and the recorded complements. The forest payment is PROVED on paper;
the sign of the remaining budget is UNKNOWN. This is a constructive partial allocation,
not a new positivity bound, proof of Wilf, or claim that each component pays itself.
Spanning-tree orientation and cycle rank are elementary graph facts; no novelty is claimed.

### Cross-word graph with the internal reservations retained

Keep D,E,P,F,F_in,L_out,C,Gamma,V,K as in E435; |E|>=2. For each exterior image group
choose the least signed word w-e_k by actual primitive weight, then lex, as in E436.
For every other start (v,j) in that group, put one labeled edge between the positive words

    n=v+e_k,             n'=w+e_j.

These words are distinct, have the same cyclic residue, and j!=k. Indeed j=k would imply
phi(v)=phi(w), hence v=w. The j-coordinate is0 on n and positive on n'. E436 proves n
noncanonical. Both endpoints have a canonical parent in P: v and w are negative-start
bases, so each has a successor in E. Edges with the same endpoints are RETAINED separately.
There are exactly L_out edges. Vertices are words, not residue labels; merging by residue
would destroy the capacity information.

For a noncanonical graph word n, its available slots are

    (u,j,h), where u in P, n=u+e_j, 0<=h<=u_j,

excluding E435's reserved internal slots. A canonical word has no such slot. Slots belonging
to distinct positive words are disjoint, since a slot determines u+e_j. Write cap(n) for
their number, and q_B for the number of zero-capacity vertices in component B. Let

    beta_1(G)=number_of_edges-number_of_vertices+number_of_components.

Choose a spanning tree in each component, root at a zero-capacity vertex if one exists,
and otherwise at any vertex. Each positive-capacity nonroot vertex pays its parent edge
with ONE of its slots. Distinct vertices use distinct slots; each tree edge has only one
child. The only unpaid tree edges are those with zero-capacity nonroot child, exactly
(q_B-1)_+. All nonforest edges remain unpaid. Thus this construction leaves EXACTLY

    R_ext=beta_1(G)+sum_B(q_B-1)_+

exterior relations unpaid. With p=L_out-R_ext paid slots, p<=Gamma-F_in and JD+ becomes

    K+R_ext <= C+(Gamma-F_in-p)+V.                         (FOREST-BUDGET, UNKNOWN)

Both sides lose p from the original JD inequality. This is an equivalent accounting
after a specific valid cancellation; the forest construction alone proves no sign.
Unused capacity at an individual word is not assumed to pay arbitrary other edges.

### Including internal aliases removes the exhausted-vertex term

There is a cleaner alternative normal form. Undo all internal reservations and add their
relations to the same graph. For an internal start (v,j) with image u=phi(v)-delta_j in P,
add the edge between noncanonical word u+e_j and canonical word v. Its first endpoint is
noncanonical by E435. The all-alias graph G_* has F_in+L_out labeled edges.

Give every noncanonical vertex ALL its Gamma slots. Every such vertex has at least one
parent in P, so has positive capacity. Every component has a single cyclic residue,
and D contains at most one canonical word of that residue. Therefore a component has
at most one zero-capacity vertex. Root a spanning tree there if present; otherwise root
anywhere. The same assignment now pays EVERY forest edge. In particular, with

    p_*=|vertices(G_*)|-|components(G_*)|,
    beta_*=F_in+L_out-p_*,

we have an explicit injection of p_* alias relations into distinct Gamma slots and

    JD+ <=> K+beta_* <= C+(Gamma-p_*)+V.                   (CYCLE-BUDGET, UNKNOWN)

This does not make beta_* free or discard it as a dependence. Each nonforest edge is
still one unpaid alias unit. Edges can connect words of different actual weights; no
tightness or positive strict-exit margin is assumed. The normal form is valid even in
the presence of zero actual-gap factorization trades. It can pay fewer aliases than
the original internal injection; neither construction is claimed optimal or stronger
in numerical margin. Their value here is to locate the residual obstruction as cycles
jointly with carries, rather than call exhausted reserved slots an intrinsic obstacle.

### Repair of the E436 collision and its limitation

In the SAME saved MSTD witness, the two relations have positive-word endpoints

    u_14+u_0 -- u_2+u_12,
    u_14+u_0 -- u_3+u_11.

The three words all represent the sum14 in H; their canonical pair is2u_7. Root this
two-edge tree at u_14+u_0. The first edge uses slot(u_2,j_12,0), the second uses
slot(u_3,j_11,0). Both parents are nonmaximal in E, both words are noncanonical, and the
slots are distinct and unreserved because F_in=0. Thus the previous two-to-one capacity
collision is repaired constructively, without changing the semigroup or optimizing roots.
Only this two-edge block of the large witness is audited; no full large graph is claimed.

On the three OLD selected cuts the reserved-graph exchange pays0 of8 exterior relations
at19,1 of1 at40, and1 of2 at114. At19 the graph has3 exhausted vertices and cycle rank6,
so all8 remain. This is not a failure of the lemma or of JD: its original margin is1.
The other margins remain2 and6. These checks audit the construction, not universal sign.

### Global review / stop refinement here

The prior concrete collision is resolved, and the all-alias forest has no exhausted-child
obstruction. But neither normal form supplies a parameter-independent source for the
remaining finite budget. Do NOT build a graph/root/matching optimizer merely to pay more
individual edges, or enlarge the closed profile list. The exact next proof question is
whether cyclic residue completeness and the actual conductor phase force C+Gamma-p_*+V
to cover K+beta_* globally, allowing compensation between components and debt types.
It is the SAME unresolved JD sign in a constructive normal form. The old19 and114 cuts
still require adaptive sharing of unused starts. If this stronger frozen target fails,
retain unfrozen POOL or E432, and keep weighted full repair and actual arithmetic/integrality
as the other universal lines. All general assertions here are paper-proved, not Lean checked.

## E438 — one depth-credit discriminator, closed (2026-10-23)

**Scope.** Proves Wilf for: every S if E432 completion / E435 JD+ holds universally in the
remaining domain. Proved reduction from all S to this case: yes, the recorded implication
chain and complements. To test whether that depth-free auxiliary claim discards necessary
credit, reused ONLY E393's existing S=<15,37,39,40>. Its exact data are c104,g70,e4,W32,
Dep10,T7,kappa5,N7,Gamma.mu30. Thus the full support bound is12 and even Dep>=T already
excludes it. This attempt yields no new positivity evidence. It is CLOSED; do not expand
the BASE examples or test a sharper wrapped-height envelope on these already excluded cases.

The contemplated actual-side envelope follows from a canonical edge u->u+e_j:
mu_u-mu_(u+e_j)=floor(p_j/m)+[conductor-phase edge wraps]>=1+[wrap]. Thus mu dominates
the longest-path sum of these unit/wrap costs, with maximal cells initialized at0.
This is a consequence of existing positive primitive bounds, not a new sign theorem.
Its positivity has not been proved and no new optimizer or envelope census was run.

## E439 — exact common-divisor descent of actual semigroups (2026-10-23)

**Scope.** Proves Wilf for: every numerical semigroup IF Wilf holds for every proper S
whose minimal generator set P satisfies gcd(P\{n})=1 for EVERY n in P. Proved reduction
from all S to this case: yes, the strict genus descent below and the N boundary. No height,
depth, multiplicity or embedding-dimension cutoff. This is part of the actual arithmetic
line of the backwards approach, not a restricted-family proof target. It does not settle
the remaining gcd1 class. No novelty claim: the rank-one invariant formulas appear in
[Ojeda–Rosales 2605.14775, Theorem4.14](https://arxiv.org/html/2605.14775), with the primitive
accounting in Proposition4.9. The application to a minimal counterexample is given explicitly.

Let S be proper with minimal generators P={n,p_1,...,p_d}. The distinguished n may be ANY
primitive; it need not be the multiplicity. Suppose k=gcd(p_1,...,p_d)>1, and put

    T=<n,p_1/k,...,p_d/k>.

Then gcd(n,k)=1, T is numerical, and T=S/k={x:kx in S}. For the reverse quotient inclusion,
write kx=A*n+sum B_i*p_i. Coprimality forces k|A, yielding x in T. The other inclusion is
immediate by multiplying generators. This is an actual integer semigroup operation.

### Apéry, genus and the exact defect — PROVED on paper

Using Apéry sets relative to n, even when n is not T's multiplicity, we have the SET identity

    Ap(S,n)=k*Ap(T,n).

Proof: an Apéry minimum cannot use n. Among sums of the other generators, multiplication
by k scales all values and permutes residues modulo n. Thus the minimum of each residue
is the scaled old minimum. In particular, the usual Apéry maximum/genus formulas give

    c(S)=k*c(T)+(k-1)(n-1),
    g(S)=k*g(T)+(k-1)(n-1)/2,
    ell(S)=k*ell(T)+(k-1)(n-1)/2.                         (DIV)

Every p_i/k remains primitive in T: a decomposition into two positive T elements would,
after multiplication by k, decompose the primitive p_i in S. Since the displayed list
generates T, only n can become redundant. Therefore e(T) is e(S) or e(S)-1. With E=e(S),

    W(S)=k*W(T)+k*(E-e(T))*ell(T)
                    +(k-1)*(E-2)*(n-1)/2.              (DIV-W)

All corrections after kW(T) are nonnegative. This includes T=N, using c=g=ell=W=0 and
e=1. Also g(T)<g(S), since n,k>=2 and the second term in (DIV) is positive. Thus any
negative actual W(S) would descend to a negative W(T) of strictly smaller genus.

Strong induction on genus proves the scope reduction. Equivalently, a least-genus Wilf
counterexample must have gcd(P\{n})=1 for every primitive n. Termination reaches N or a
semigroup satisfying that condition; no unproved reduction to a fixed e or profile is used.
This descent supplies real positive finite corrections, unlike the failed arbitrary
common-positive-shift monotonicity in E431. The operations and hypotheses are different.

### Checks and limit

Existing C residue reconstruction and independent membership agree on four controls:

| S | Distinguished n,k | T | Contributions in DIV-W |
| --- | --- | --- | --- |
|<5,6,8>|5,2|<3,4,5>|0+0+2=2|
|<17,18,21,33>|17,3|<6,7,11>|12+21+32=65|
|<18,21,29,33>|29,3|<6,7,11>|12+21+56=89|
|<5,7>|5,7|N|0+0+0=0|

The third pivot is NOT the multiplicity. All Apéry entries relative to the pivot are
compared, including the N boundary. These are checks of a general proof, not a family
enumeration or a novelty claim. Generic leave-one-out-gcd1 semigroups remain untouched.

## E440 — parity exposes a primitive-loss correction (2026-10-23)

**Scope.** Proves Wilf for: every numerical semigroup IF Wilf transfers from T=S/2 to S
for every proper S. Proved reduction from all S to this case: yes, g(T)<g(S), since all
gaps of T correspond to EVEN gaps of S and1 is an ODD gap of every proper S. The N boundary
starts strong induction. The universal transfer is UNKNOWN and is equivalent in strength
to Wilf; merely stating it is no advance. The stronger proposed payer W(S)>=2W(T) is FALSE,
including inside the remaining domain and after E439's cofactor restriction.

The representation below is standard numerical duplication with a relative ideal:
[Strazzanti 1404.4959, Proposition3.3 and Lemma4.8](https://arxiv.org/html/1404.4959).
It is written here in normalized form to retain exact genus, primitive-loss and defect
terms; no novelty claim for duplication or the elementary identities.

### Normalized odd ideal and exact identities — PROVED on paper

For ANY proper S, let a=2b+1 be its least odd element, T=S/2, and

    I={i>=0:a+2i in S}.

Then0 in I, T subset I, I+T subset I, a in T, and a+I+I subset T. Conversely these
conditions, with T numerical and a positive odd element of T, make

    S=2T union (a+2I)

a numerical semigroup with quotient T. Both parity classes are cofinite and all three
addition cases are covered. Thus this construction retains ALL S, not only proper ideals
I subset T or almost symmetric duplications. Here I is normalized to contain T.

Write C=c(T), h=g(I)=|N\I|, c_I=min{c:[c,infinity) subset I}, with c_I=0 if I=N. Counting
even and odd gaps gives

    g(S)=g(T)+h+b,
    c(S)=max(2C-1,a+2c_I-1).                            (PAR)

For odd gaps, the b positive odds below a are missing and the rest correspond to N\I.
For the conductor take the larger of the last even and odd gaps, with the usual negative
boundary conventions when a parity class has no nonnegative gaps. Put

    v=g(T)-h>=0,             t=c(S)-2C in {-1,0,2,4,...}.

Then ell(S)=2ell(T)+v-b+t.

Let r be the number of ODD primitives of S and q the number of primitives p of T for
which2p is NOT primitive in S. Every even primitive of S is twice a primitive of T.
Here r,q are LOCAL primitive counts, not the earlier top residue and conductor depth.
Further, a lost2p must be the sum of TWO odd primitives of S. Indeed a decomposition
into evens would decompose p in T. Factoring an odd summand into one odd primitive and
an even remainder shows that any nonzero remainder would again decompose p in T.
Consequently

    e(S)=e(T)+r-q,             q<=binom(r+1,2).

The normalized offsets of the odd primitives are exactly the minimal T-ideal generators
of I: every odd S element is one odd primitive plus an even S element. With E=e(S),
direct substitution yields

    W(S)=2W(T)+2(r-q)*ell(T)+E*(v-b)+(E-1)*t.            (PAR-W)

This formula retains a potentially NEGATIVE primitive-loss term. There is no permission
to discard it or assume q<=r. The upper bound by binom(r+1,2) is a structural count, not
the missing global payment of q-r copies of ell(T).

### Two exact monotone-transfer obstructions

First take S=<17,18,21,33>. It has m17,e4,c83,g46,ell37,W65, so c>4m and3e<m.
Pairing its odd generators and halving its even generators gives

    T=<9,17,19,21,25,33>, c42,g23,ell19,e6,W72.

Here a17,b8,I=(0+T) union (2+T) union (8+T), c_I32,h15,v8,r3,q5,t=-1. The five lost
quotient primitives are17,19,21,25,33, with odd-pair witnesses(17,17),(17,21),(21,21),
(17,33),(33,33). The exact correction in (PAR-W) is

    -76+0-3=-79,           W(S)=2*72-79=65.

This S is itself reducible under E439 (factor3 after omitting17), so it alone would not
refute a version restricted by that reduction. Use the SINGLE cofactor1 variant

    S=<17,18,21,37>, m17,e4,c84,g48,ell36,W60;
    T=S/2=<9,17,19,21,29>, c42,g24,ell18,e5,W48.

Every gcd(P\{n}) is1. Also c>4m and3e<m. Here I=(0+T) union (2+T) union (10+T), c_I34,
h16,v8,b8,r3,q4,t0. Lost primitives17,19,21,29 have pair witnesses(17,17),(17,21),
(21,21),(21,37). Thus

    correction=-36+0+0=-36,       W(S)=2*48-36=60<96.

The second obstruction survives the cofactor restriction; both W values remain positive.
Neither is a Wilf counterexample or a refutation of conditional transfer of NONNEGATIVITY.
The initial hand prediction W56 for the variant missed a17-unit improvement of one Apéry
entry; exact C and independent membership give genus48 and W60. The saved data use only
the corrected values. This is not a search over variants.

### Global review / next mathematical obligation

The common-divisor descent is a valid universal normalization with a positive finite
correction, already based on known rank-one formulas. It does not resolve the generic
cofactor1 case. Numerical duplication also predates this work; its universal representation
must not be presented as a new reduction theorem. The concrete deduction here is that
even in the remaining cofactor1 domain the simple monotone quotient payer is false, and
PAR-W identifies its primitive-loss cost exactly. Stop that payer and do not expand a
duplication/profile census or retreat to a fixed number of odd generators.

Within the standing actual-arithmetic line, the next testable proof task is to use the
structured odd-pair relations together with the filled-gap mass v to bound the loss of
q-r quotient primitives, RETAINING the surplus W(T). Requiring the correction alone to
be nonnegative is refuted. A successful general conditional transfer, or a weaker argument
for a least-genus counterexample, must cover all r and all normalized admissible I.
The full finite positivity statement remains UNKNOWN. E435/E437's cyclic boundary route
and the genuinely weighted full-certificate route remain available; no exclusive switch
to a narrower family has been made. All new proof applications are on paper, not Lean checked.

## E441 — odd-ideal additive closure: generator-controlled descent and mixed Apéry budget

2026-10-23. Status: the closure construction, genus descent, mixed Apéry identity and
budget below are PROVED ON PAPER. Conditional transfer and both proposed sign inequalities
are NOT proved. No Lean verification or novelty claim. Scope: Proves Wilf for every S IF
W(U)>=0 implies W(S)>=0 for this construction; proved reduction to all S: YES, induction
on genus, with N the base. The stronger W(S)>=W(U) would suffice. No restriction to a
fixed embedding dimension, parity count, height or depth is imposed.

### 1. A smaller-genus descendant with e(U)<=e(S)

Let S be proper, P its minimal positive generators, E=|P|, and a=2b+1 its least odd
element. This a belongs to P: any decomposition of a would contain a smaller odd
positive summand. Define

    H={p/2:p in P even},
    A0={(p-a)/2:p in P odd},       A+=A0 minus {0},
    T=S/2,       I={i>=0:a+2i in S},
    U=<a,H,A+>.

All entries of the displayed list for U are positive, and its length is E. From E440,
I=A0+T, T subset I, I+T subset I, and a+I+I subset T. Pair the odd terms in any primitive
factorization of an even S element. It follows that T is generated by H and the numbers
a+alpha+beta, alpha,beta in A0. Therefore

    U=<T,A0>=<I>.

For the first equality, every paired generator is in <a,H,A+>; conversely a is the pair
(a+a)/2 in T, while H subset T. For the second, T and A0 are subsets of I, and I=A0+T.
Also S subset T subset U, so U is numerical. In particular

    e(U)<=E,          g(U)<=g(T)<g(S).                 (OC-DESC)

The strict genus inequality holds because S subset T and 1 is an odd gap of every proper
S, while gaps of T correspond to even gaps of S. More explicitly g(S)=g(T)+g(I)+b,
and b>=1. This proof includes U=N. It does NOT assert monotonicity of W under closure.

This closure is standard ideal blowup in this normalization, not a new representation.
Indeed 0 in I makes nI ascending; all nI contain T, so finite complements imply eventual
stabilization at their union U. For stable n, nI=U and nI-nI=U, where ideal subtraction
means {z:z+nI subset nI}. Every earlier nI-nI is contained in U since 0 in nI. Thus
union_n(nI-nI)=U, the BlowUp definition in the official NumericalSgps documentation,
Chapter7 section7.3-3. Neither that definition nor OC-DESC supplies a Wilf sign theorem.

### 2. Mixed Apéry representatives modulo the least odd element

The modulus here is a, which need NOT be any semigroup's multiplicity. For residues
s in Z/a write u_s,t_s,i_s for the least elements of U,T,I in that residue, respectively.
These exist, and all three sets are closed under addition by a. Since

    U contains I contains T,         a+I subset T,

we have i_s<=t_s<=i_s+a, hence t_s-i_s is either0 or a. Let v_j be the Apéry representative
of S modulo a in residue j. Its even option in residue2s is2t_s, and its odd option is
a+2i_s. Taking the smaller in the two possible cases proves the exact identity

    v_(2s mod a)=min(2t_s,a+2i_s)=t_s+i_s.            (MIX-AP)

Multiplication by2 permutes Z/a because a is odd. Define integers

    K_s=(t_s-u_s)/a,       L_s=(i_s-u_s)/a,
    epsilon_s=K_s-L_s in {0,1},       lambda_s=K_s+L_s.

Then 0<=L_s<=K_s<=L_s+1 and v_(2s)=2u_s+a*lambda_s. The usual residue gap count applies
also to the normalized ideal I: g(I)=sum_s floor(i_s/a). Consequently

    sum K=g(T)-g(U),        sum L=g(I)-g(U),
    g(S)=2g(U)+b+sum_s lambda_s.                      (MIX-G)

Only epsilon is binary. A common height L, or the total lambda, must NOT be replaced by
a count of nonzero residues. For example S=<5,7>, a5,U=N gives

    K=[0,1,1,2,2], L=[0,0,1,1,2], lambda=[0,1,2,3,4].

### 3. Exact finite correction; the sign is the missing theorem

Let e_U=e(U), ell_U=c(U)-g(U). Substitution of MIX-G into W=(E-1)c-Eg gives

    W(S)=2W(U)+2(E-e_U)*ell_U
         +(E-1)*(c(S)-2c(U))-E*(b+sum lambda).         (OC-W)

Also c(S)=max_s(2u_s+a*lambda_s)-a+1. Thus all quantities in OC-W retain the arithmetic
residue labels and the common lift heights. The nonnegative embedding correction removes
the specific lost-primitive cost of E440, but the remaining correction can be negative.

Two logically distinct goals are:

    MON1: W(S)>=W(U);                                FALSE unrestricted (E442).
    TRANSFER: W(U)>=0 implies W(S)>=0;                UNKNOWN.

Either, if true universally, would prove Wilf by OC-DESC and genus induction. MON1 is stronger than
necessary. In OC-W, proving TRANSFER may use BOTH copies of W(U); there is no reason to
require the other three terms to be nonnegative separately. The still stronger
W(S)>=2W(U) is FALSE even on the old cofactor1 remaining-domain example

    S=<19,39,41,50,52,53>, E6,c88,g68,W32,
    U=<10,11,17,19,25,26>, e_U6,c25,g17,W23.

OC-W's four terms are46,0,190,-204. Thus the standalone correction is-14, whereas
W(S)-W(U)=9. This refutes neither MON1 nor Wilf.

### 4. Typed primitive constraints retain the common heights — paper lemma

Keep ALL original H/A+ inputs, even when redundant in U. For a primitive input g and
an edge s->t with t=s+g mod a, put J=(u_s+g-u_t)/a>=0. The actual ideal containments give:

    g in H:    K_t<=K_s+J,       L_t<=L_s+J;
    g in A+:   L_t<=K_s+J,       K_t<=L_s+J+1.

For H use T+H subset T and I+H subset I. For A+ use T+A+ subset I and
a+I+A+ subset T. In particular lambda_t<=lambda_s+2J+tau_g, with tau0 on H and tau1
on A+. If an input value occurs with both types, both inequalities hold. These constraints
are consequences, not a positivity mechanism: their local upper bounds alone have not
paid the sum of common heights in OC-W. No new shortest-path optimizer is proposed.

### 5. One bounded falsification, closed; next exact obligation

Pure C on Fejer tested MON1 starting ONLY at the old19 example. One improving normalized
score move reached S=<19,41,50,52,53,58>, W46 and U=<11,17,19,25,26,29>, W36. It stopped
at a local optimum after1392 candidate comparisons (1361 eligible); no negative margin.
The raw margin changed9->10 while margin/c(S) decreased9/88->10/98. Both sources have
all leave-one-out primitive gcds1. This is not evidence of a universal sign theorem.
Independent membership audits verify every modulo-a entry for these two cases and controls
<5,7> (U=N) and <6,7,11> (a7 is not the multiplicity). ASan/UBSan reproduces the SAME
bounded search byte-for-byte. See EXPERIMENTS and STATE for code/data and exact bounds.
The search is CLOSED; no more seeds, variants or a positive-profile census are next.

The next mathematical task is a global bound on sum(K+L), using the typed source relations,
the complete residue system and the ACTUAL W(U) surplus, sufficient for TRANSFER in OC-W.
A proof that merely reconstructs lambda exactly would leave its sign unexplained. Retain
the weaker transfer if MON1 fails; retain E435/E437 cyclic payment and the full weighted
certificate line as the other universal approaches. No universal proof or genuine Wilf
counterexample has been obtained.

## E442 — full monotonicity fails; ideal-power algebra retains a different generator count

2026-10-23. Scope: Proves Wilf for every S IF E441's full nonnegativity transfer holds;
proved reduction from all S: YES, OC-DESC and genus induction. This section refutes an
OPTIONAL strengthening and proves a structural ingredient for paying the full OC-W budget.
It does not establish that budget's sign. General arguments are ON PAPER, not Lean checked.

### 1. Unrestricted MON1 is FALSE, with an unbounded deficit

For m=2b+1>=3 and t>=2 take the classical Wilf-equality semigroup

    S=<m,2tm+1,2tm+2,...,2tm+m-1>.

Its least odd element is m, e(S)=m,c(S)=2tm,ell(S)=2t,W(S)=0. These source invariants are
standard (e.g. Eliahou1703.01761 introduction; Marashdeh2608.12531 Lemma2.3). E441 gives

    U=<m,tm-b,...,tm-1,tm+1,...,tm+b>.

The non-m generators occupy all nonzero residues, and any sum of two is larger than the
largest one since tm>3b. Thus they are exactly U's nonzero Apéry representatives modulo m,
are all primitive, and

    e(U)=m, c(U)=tm-b, g(U)=(2t-1)b, ell(U)=t, W(U)=b.

Hence W(S)-W(U)=-b is unbounded below. Every positive-multiple payer W(S)>=eta*W(U),
eta>0, fails on ALL S. The example m5,t2 is independently audited:

    S=<5,21,22,23,24>, c20,g16,e5,W0;
    U=<5,8,9,11,12>, c8,g6,e5,W2.

All five leave-one-out primitive gcds are1. This is NOT a Wilf counterexample. These
witnesses have e=m, so they do NOT refute MON1 restricted to the remaining domain3e<m.
For t>=3 they do have c>4m; density, not depth, is the excluded hypothesis.
No fixed-family proof programme or new search is activated by this falsification.

In fact I=U here, since I contains each U Apéry representative, so L_s=0 and sum K=b.
OC-W has terms 2b,0,2b(m-1),-2bm, summing to0. Even with NO common lift L, the full
surplus2W(U) is spent. The target must retain the binary part as well as common height;
closure rigidity or a unit cap by itself cannot prove the needed sign.

### 2. The ideal-power layers form a finite standard graded algebra

Use E441's T,I,U and set 0I=T (the identity for relative-ideal sums). For n>=1 define

    H_n=nI minus (n-1)I,          h_n=|H_n|.

These layers are finite, disjoint and eventually empty; their union is U minus T. Put
F_n=span_k{t^u:u in nI} inside k[t], with F_0=k[T]. These are vector spaces, not
necessarily subrings. Products satisfy F_n F_j subset F_(n+j), so

    B=k plus direct_sum_(n>=1) F_n/F_(n-1)

is a graded k-algebra, with the evident scalar identity. Multiplication of positive
classes is well-defined because F_(n-1)F_j subset F_(n+j-1). It is associative for the
same reason. It is finite-dimensional since the ideal sums stabilize at U.

Moreover B is generated in degree1. Each monomial of F_n factors into n monomials of F_1.
In each factor separate its k[T] part from the span of the gaps H_1. Any product containing
a k[T] factor belongs to F_(n-1), since the other n-1 ideals are T-stable. Therefore the
degree-n quotient is spanned by products of n gap classes from H_1. In particular

    Hilbert(B)=(1,h_1,h_2,...),
    h_n<=binom(h_1+n-1,n),
    sum h_n=g(T)-g(U),
    sum_(n>=2) h_n=g(I)-g(U),
    sum_s(K_s+L_s)=h_1+2*sum_(n>=2)h_n.              (LAYER-COST)

Standard Macaulay theory consequently applies to THIS algebra with embedding dimension
h_1=|I minus T|. It does NOT apply with e(S)-1 substituted. No novelty is claimed for
associated graded constructions or Macaulay's theorem; the construction and exact cost
are proved here to keep the relevant dimensions explicit.

The two-step arithmetic constraint is also retained: a+I subset T and, for n>=2,

    a+nI subset (n-2)I.

It follows by grouping two I factors and using a+I+I subset T. This is a relation between
the VALUE labels of layers, not monotonicity of their cardinalities. For example the
admissible data T={0} union[10,infinity), I={0,1,3}+T,a11 give h=(2,3,3,1). This is a
paper set calculation below10; E440 ensures a genuine S. There was no computation or
search on this example. Thus later layer growth need not be bounded by the first layer.

### 3. Why replacing the original generator count by a Hilbert dimension is unsafe

The OLD boundary control S=<5,7> already exposes the issue. Here a5,T=<5,6,7>,
I={0,1}+T,U=N. The layers are

    H_1={1,8}, H_2={2,9}, H_3={3}, H_4={4}.

So B has Hilbert function(1,2,2,1,1), despite e(S)-1=1 and just ONE nonzero odd-ideal
generator. A polynomial ring in that one generator cannot have this Hilbert function.
The missing action is a genuine quotient primitive: 7=a+1+1 acts nontrivially in degree1,
sending the gap class1 to8. Therefore the paired quotient primitives cannot simply be
discarded from the coefficient action on the layers, even though the closure U has no
more generators than S. The analogous degree2 action sends2 to9.

The discrepancy is unbounded at FIXED source embedding dimension, not just a small
off-by-one. This is a calibration of the universal payment, not a two-generator target.
For the classical equality source S=<a,a+2>, a=2b+1, we have T=<a,a+1,a+2>,
I={0,1}+T,U=N. Its ideal-power representatives for 0<=s<a are

    w_(nI,s)=s+a*ceil(max(0,s-n)/2),   n>=0.

For T, using residues1 and2 minimizes the number of generators to ceil(s/2); wrapping
adds a and cannot lower the cost. For nI=T+[0,n], the cheapest k is min(n,s). Choices
k>s wrap and cost at least s+a, whereas k=s costs s. This proves the displayed formula.
Its successive genus differences give

    h_n=b+1-ceil(n/2), 1<=n<=2b;      h_n=0 after2b.

In particular h_1=b with e(S)=2, and H_n={n+j(a+2):0<=j<h_n}. The latter formula
follows by taking the residues s=n,n+2,... that lose one a-unit at step n. Multiplication
by the paired quotient primitive a+2 gives ONE nilpotent chain through each H_n; it is
not a new degree-one algebra generator for every point in that chain. Finally

    h_1+2*sum_(n>=2)h_n=ab,
    E*(b+ab)=2b(a+1)=a^2-1=c(S).

Thus the conductor term pays the entire cost exactly, with W(U)=0. This explicitly
identifies the missing ingredient as a VALUE-SENSITIVE allocation of these operator
orbits; a cardinality bound in terms of e(S) alone cannot replace it. For multiple
primitive actions the orbits can overlap, and no universal disjoint allocation has been
constructed. No new experiment or claim of a new two-generator Wilf theorem is made.

One may represent these actions by retaining addition by H, addition by the A offsets,
and the physical a-shift that drops ideal-power degree. This is an EXACT operator
description, not a rank/positivity theorem. Merely applying Macaulay with h_1 in place
of e(S)-1 would lose the generator budget the descent was designed to control.

### 4. Verification, review and next action

Fejer used existing C --odd-audit plus independent stdlib membership. The new
--odd-layer-check audits ONLY the two saved E441 cases, the two old controls, and the
single predicted MON1 witness. For each it checks all modulo-a ideal-power entries by
convolution AND finite membership, product spanning of every layer, the a-shift, and
LAYER-COST. Hilbert functions are respectively(1,7,6,3),(1,7,3,2),(1,2,2,1,1),
(1,3,1),(1,2); the first two stabilize at power3. No new C search, solver or census.
The existing E441 mixed-identity audit also passes. Data and reproduction are in STATE
and EXPERIMENTS. Neither these finite checks nor the standard algebra is a sign proof.

Decision: stop unrestricted MON1 and any scalar first-layer/Macaulay substitution of
e(S)-1 for h_1. Do not enlarge the layer table or classify its O-sequences. The next
arithmetic proof must retain the original-source coefficient actions and their value labels
to pay h_1+2*sum_(n>=2)h_n from the FULL OC-W budget. The concrete missing lemma is a
uniform joint bound involving those actions, conductor growth and actual W(U), not
exact reconstruction of the powers. If that ingredient supplies no finite sign, return
to E435/E437 cyclic payment or the full weighted-certificate alternative, without another
local-accuracy optimizer. All three universal lines remain active; Wilf remains unproved.

## E443 — a conductor differential target and a failed reflection mechanism

2026-10-23. Scope: Proves Wilf for EVERY S if dim_Q(Omega_R/C*Omega_R)>=c, R=Q[S],
C=t^c Q[t]. Proved reduction: YES, this module is a quotient of (R/C)^e, of dimension
e*ell. The proposed lower bound is UNKNOWN and stronger than Wilf. The following
presentations/identities are paper-proved; the three fixed tests are not universal evidence.

For P=(p_j), the standard differential presentation is R^e modulo differentiated binomial
relations. At weighted degree N, let A_N={j:N-p_j in S and 0<=N-p_j<c}. A trade
z.P=z'.P=N gives the row (z_j-z'_j) projected to A_N. All such rows span the degree-N
relation space after tensoring with R/C. Multiples of lower relations are included by
adding a common factorization. No active columns remain at N>=c+max(P). Thus, writing
r_N for the rational row rank,

    dim(Omega_R/C*Omega_R)=e*ell-sum_N r_N.

This standard presentation follows from Stacks00RM Lemma10.131.9/14; no new differential
theory is claimed. The initial Euler map to R/C only gives ell-1 image dimensions and
does not prove the proposed bound. A more useful exact version is as follows.

Let M=(t^p:p in P), and Tors=ker(Omega_R -> M) under Euler contraction
d(t^p)->p*t^p. In characteristic0 this kernel is precisely differential torsion, since
the map is an isomorphism after passing to the fraction field. It is surjective onto M.
Moreover C*M=t^(c+m)Q[t]. Taking quotients gives an exact sequence

    0 -> Tors/(Tors intersect C*Omega_R) -> Omega_R/C*Omega_R -> M/(C*M) -> 0.

To check its kernel, lift each summand c_i*m_i of an image in C*M to c_i*omega_i;
subtracting those lifts leaves torsion. Counting monomials gives dim(M/C*M)=ell+m-1.
Consequently the missing global lower bound is exactly

    dim(Tors/(Tors intersect C*Omega_R)) >= g-m+1.       (DIFF-GAP, UNKNOWN)

The right side equals rank(t^m:Q[t]/R -> Q[t]/R): every gap>=m is m plus another gap,
and the m-1 initial gap chains are the kernel. This identifies a candidate source of
dimensions; it does NOT construct an injection or establish the inequality.

The optional single-shift graded reflection mechanism is FALSE. For OLD
S=<19,39,41,50,52,53>, complete independent rational calculation gives differential
dimension101, Euler image38, torsion quotient63, while g-m+1=50. Yet no integer shift D
has a torsion component at EVERY D-n for gaps n>=m. The only possible shifts are145..152,
and every one fails; exact missing degrees are saved. Thus even a graded VECTOR-SPACE
reflection injection with one common shift is impossible. This does not refute DIFF-GAP.

The OLD5/7 control has dimensions24=16+8, required gap rank8, and reflection shift35.
The OLD6/7/11 control has18=12+6, required5, but again no common reflection shift.
Three C trade audits are verified independently by coin DP enumerating ALL factorizations
in the required degree ranges and exact Fraction row ranks. Their relation ranks are19,0,3.
New C ASan/UBSan outputs match normal outputs byte-for-byte. No new search or census.
See STATE/EXPERIMENTS for code/data. These standard-algebra identities are not Lean checked.

Decision after advisor review: diagnostics CLOSED, no expansion of this stronger bound
without a new sign argument. No all-pairs rank/accuracy optimizer. Preserve the exact
identities and reflection obstruction; prioritize the existing source-parity and weaker
full-tile Hall payment in E444. DIFF-GAP is not treated as an established route to Wilf.

## E444 — advisor audit: source parity multiplication and restoring the Hall reserves

2026-10-23. Credit: user's advisor for the four-generator family, source-algebra
decomposition and explicit reserve recommendation. Scope: Proves Wilf for EVERY S if the
parity value inequality below holds. Proved reduction: YES, its difference is exactly W.
This section verifies the proposal and derives a multiplication consequence. It supplies
NO universal finite sign theorem. All general arguments remain paper proofs, not Lean checked.

### Four-generator obstruction, all parameters — advisor calculation verified on paper

Put a=6k+1,k>=2,S=<a,a+2,a+4,a+6>. All four values are primitive, and every leave-one-out
gcd is1. The parity data are T=<a,a+1,...,a+6>, I=[0,3]+T,U=N. With 0I=T,

    w_(nI,s)=s+a*ceil(max(0,s-3n)/6), 0<=s<a,
    h_n=3*(k+1-ceil(n/2)), 1<=n<=2k, then0,
    cS=(2k+1)a-1=12k^2+8k, gS=6k(k+1), WS=12k^2.

For T an offset s uses ceil(s/6) generators; adding a wrap increases both offset and
cost. For nI=[0,3n]+T, choose offset min(s,3n); wrapped choices again cost more. Summing
the representatives and taking successive differences gives the formulas. Thus h_1=3k
is unbounded while eS-1=3, even with c>4m,3e<m and the E439 cofactor normalization.

H_1={r+j(a+6):r1..3,j0..k-1}, three coefficient chains under paired primitive a+6.
This is a calibration, not a new difficult Wilf family. The lex canonical tile consists
of (0,0,j),j0..2k; (0,1,j),j0..2k-1; (0,2,j),j0..2k-2; and(1,0,0).
The support sum is(2k-1)+(2k-2)=4k-3. Its four maximal cells have total omega6k+13,
so Dep=3(6k+1)-(6k+13)=12k-10. It is already shape-excluded with margin8k-7.
ONLY k2 was computed: c64,g36,W48,h=(6,6,3,3),Dep14,support5. No family enumeration.

### Correct source algebra — advisor construction verified

Over any field, put x=t^2,z=t^a,R=k[x^T],M=span{x^i:i in I}. Then k[S]=R plus zM,
and its ideal generated by z is x^aM plus zR. Hence the source quotient A=k[S]/(t^a) has

    A_even=R/x^aM,       A_odd=z(M/R),
    dim A_even=a-h_1,    dim A_odd=h_1,      dim A=a.

Here a+I subset T ensures x^aM subset R; counting T minus(a+I) gives a+gI-gT=a-h_1.
The original primitives other than a generate A, and remain independent modulo its
maximal ideal squared, so the algebra generator count is exactly e(S)-1. It is the
original Apéry algebra, not a newly smaller object. It is positively VALUE-graded and
Z/2-graded; a standard grading by factorization length is NOT automatic. Passing to a
standard associated graded algebra would require tracking the value information again.
Although the class of z is zero, not every z*x^i is zero: x^i need not lie in R.

Let V_n be the span of products of n elements of A_odd. Then precisely

    basis(V_n)={t^(n*a+2u):u in H_n, n*a+2u in Ap(S,a)}. (ODD-PRODUCT)

Proof: sums of n I exponents give nI. If a sum belongs to(n-1)I, subtracting one a from
its source value leaves an S element, using a+qI subset(q-2)I and the n1/2 boundary
conditions; the product vanishes. Conversely any u in H_n factors into n elements of
I minus T, since a T factor would put it in(n-1)I. It survives exactly when its source
value is Apéry. For n1 this is all H_1. For n2, a+H_2 subset T but H_2 disjoint I, so
all survive. Therefore dim V_1=h_1 and dim V_2=h_2. Also V_(n+2) subset V_n: odd times
odd is even, and V_n is stable under multiplication by A_even.

Higher scalar layers can be killed. On OLD19, h=(7,6,3) but dim V=(7,6,0): u31,32,33
would give source values119,121,123 above its maximum Apéry value106. Their products
are divisible by t^a. These are actual arithmetic relations involving the pivot; they
are NOT automatically payments for the lost scalar-layer mass. Distinct such relations
can still share resources. For the advisor's k2 and OLD5/7 controls all recorded layers
survive. Exact basis-product audits cover169,361,25 ordered products respectively.

Writing Mv=max Ap(S,a), meanv=(sum Ap)/a, the exact target remains

    W=(e-1)Mv-e*meanv-(e-2)(a-1)/2 >=0.

Zhai's weighted-downset lemma gives only e*meanv<=(e-1)Mv. Correct multiplication and
generator count do not yet supply the missing finite improvement. Choosing a>m increases
that correction; parity must earn its use. The new consequence ODD-PRODUCT identifies
compatibility that can be quantified, not a proof that it is sufficient.

### Hall route: restore BOTH reserves; frozen allocation is optional

For any nonempty cut E let F_res be its E434 frozen margin, U_pool its directional
residue pool, and Leak the nonnegative capacity frozen to outside children. The E432
completion budget and E434 identity give EXACTLY

    Q(E)=F_res(E)+Leak(E)+m-|U_pool(E)|.

E437's all-alias forest rewrites F_res=C+(Gamma-p_*)+V-K-beta_* without changing its
value. Thus the original completion claim allows both reserves; imposing F_res>=0
discards them. At E=D, Leak=0 and Q(D)>=0 alone suffices for the support proof of Wilf;
requiring every down-set or discarding omitted residue units is a stronger optional target.
Q(D)>=0 itself is still a SUFFICIENT strengthening of Wilf, not an established theorem.
The empty cut is separate and has Q=m; do not apply the nonempty forest formula there.

Audits reuse old19/40/114 whole tiles and selected cuts. On whole19 frozen margin1 becomes
original budget5 because four residue units were omitted. On selected114 it is6+69=75;
on selected40 it is2+33=35. The old40 two-cell control checks positive Leak2 as well.
No new flow solve or census. The uniform sign remains UNKNOWN.

Current priority: derive a quantitative value inequality from source odd/even multiplication,
with E439 as a normalization. Keep full-tile Q with both reserves as the Hall alternative.
Stop repairing optional monotonicity, scalar Hilbert counts or forest cancellation merely
to make them more exact. User's advisor is not credited with the ODD-PRODUCT deduction;
the general identity/proof and finite audit were developed here in response to the advice.

## E445 — source odd-parent credit, necessary reserve and arbitrary-modulus depth

2026-10-23. Scope: Proves Wilf for EVERY S if E444's finite source value gain is paid.
Proved reduction: YES, that difference is exactly W. The lemmas below are universal
components; they do NOT themselves imply its sign. The stronger primitive-only stage is
refuted on the OLD remaining-domain19 example. No restricted family, search or optimizer.
All statements recorded as proved here are on paper, not Lean checked. No novelty claim
for elementary module generation, parent counting or the ceiling identity.

### 1. An injective odd-parent assignment using the original generators

Let a be the least odd S element, A=Ap(S,a), M=max A, E=e(S). Write B_0,B_1 for its
even and odd value sets. Let q be the number of ODD primitives other than a (not conductor
depth). Every v in B_1 has v=p+u for such a primitive p and an even u in B_0. Indeed take
a primitive factorization of v; it contains an odd primitive, cannot contain a, and the
remaining even S value u is Apéry or else v-a would belong to S.

Choose one such p per v. Different v give different pairs(u,p), since the sum determines
v. This is an explicit injection B_1 -> B_0 times P_odd_other. Thus with h_1=|B_1|,

    h_1<=q*(a-h_1),        h_1<=floor(q*a/(q+1)).

Define D_i=sum_(v in B_i)(M-v). Give every even parent q labeled copies; call those not
used by the injection unmatched. Let P_par=sum_(assigned children) p and
R_par=sum_(unmatched (u,p))(M-u). Then EXACTLY

    q*D_0-D_1=P_par+R_par >=(a+2)*h_1.                (ODD-PARENT)

Each assigned parent deficit is M-u=M-v+p; the rest is R_par. All right-side terms are
nonnegative. The source count q is retained, unlike replacing it by h_1. This is a
positive TYPED functional with coefficients(q,-1), not yet the total-deficit inequality.

### 2. The unmatched copy reserve cannot be discarded

Put C_a=(E-2)(a-1)/2. For q>0 the main target rewrites exactly as

    q*a*W=E*(q+1)*D_1+E*(P_par+R_par)-q*a*(M+C_a).     (PAR-BUDGET)

This follows by substituting q*D_0=D_1+P_par+R_par into aW=E(D_0+D_1)-a(M+C_a).
If q=0 all other source primitives are even, so E439's factor2 descent applies; no
division by q is used. For a least-genus counterexample after E439, q>=1.

A tempting stronger stage drops R_par and hopes the rest pays universally, perhaps after
choosing different parents. This is FALSE even in c>4m,3e<m and cofactor1. For OLD
S=<19,39,41,50,52,53> we have

    E6,a19,q3,M106,C_a36,D_0=332,D_1=219,
    P_par319,R_par458,
    reserve-free numerator=-924,
    full numerator=-924+6*458=1824=3*19*W, W32.

All seven odd children have UNIQUE permissible primitive parents; the full witnesses
are saved. Hence even maximum possible P_par is319, and parent selection cannot rescue
the reserve-free stage. This refutes only that payer, not Wilf or source parity. With
R_par retained, changing the parent rule only redistributes P_par versus R_par; their
sum is the fixed functional qD_0-D_1. Do not launch a parent-choice optimizer.

### 3. The multiplicity strict-drop rule does not transfer unchanged to modulus a

Use a canonical factorization down-set D for Ap(S,a) over the E-1 primitives other than a.
Here some EVEN primitives p may be LESS than a. Put

    mu(v)=floor((M-v)/a)=max(0,ceil((c-v)/a)).

On every tight primitive step v->v+p within the Apéry set,

    mu(v)-mu(v+p)=floor(p/a)+[ ((v-c) mod a)+(p mod a)>=a ].

This is an integer ceiling identity, extending the multiplicity formula already recorded
in E438. It yields unit drop for p>=a, including every nonpivot odd primitive. A smaller
even primitive may give zero drop. This does NOT refute E430, whose modulus was the
multiplicity; it prevents reusing that theorem under changed hypotheses.

For each cell v let b(v)=max floor(p/a) over its canonical primitive children, or0 if
there are none. Then mu(v)>=b(v). Let gamma(v) be the sum of lengths of coordinate columns
ending at v, N their phase-inversion count, and kappa the same residue carry count as
E429/E432 but modulo a. The CH/residue identities remain valid for arbitrary a:

    W=sum_v gamma(v)*mu(v)+N-kappa
      >=sum_v gamma(v)*b(v)+N-kappa.                   (WEIGHTED-DEP)

Proof: the canonical column identity uses positive primitive values and a complete
residue system, without assuming p>=a. Splitting M-v into a*mu plus its residue gives
the same N-kappa term. The final inequality uses nonnegative gamma and mu>=b. The
unweighted Dep bound requires p>=a on an available child; that extra hypothesis cannot
be silently reinstated when a differs from m(S).

The OLD control S=<6,7,11>, a7, has Apéry values{0,6,11,12,17,22,23}. The tight p6
step17->23 has mu0->0. Direct columns give unweighted Dep5, corrected weighted depth3,
and N-kappa=1. Thus the naive transplanted bound6 exceeds the actual W4, while
WEIGHTED-DEP gives4. No original multiplicity theorem is contradicted.

### Verification and decision

Existing C --odd-audit plus independent membership/modulo-a column enumeration checks
ONLY old6/7/11, old19 and advisor k2. It verifies every parent, ceiling drop, weighted
column identity, primitive/reserve budget and all possible parent choices via independent
per-child maxima (no search). The old advisor/source-multiplication/reserve audit also
passes. No new C code, sanitizer path, LP, source family or positive-profile census.
Data/modes are inventoried in STATE; no numerical improvement is counted as a sign proof.

Global review: ODD-PARENT is a genuine original-generator bound, but its coefficients
do not directly pay the total deficit. Primitive-only funding fails, and preserving the
full reserve merely recovers PAR-BUDGET until a new uniform lower bound is proved. Stop
that stage and selector refinement. The next proof must couple R_par, D_1 and the
higher odd-product relations (or use the full-tile Hall alternative with its reserves),
retaining WEIGHTED-DEP when a>m. The finite sign remains UNKNOWN.

One more proposed shortcut is ruled out on paper: higher scalar-layer deaths do not
require an ORIGINAL even primitive. For S=<13,15,47>, all three displayed generators
are odd and primitive (47 is not generated by13,15), with a13 and A0={0,1,17}.
The half T has no positive element below13. Thus nI below13 is exactly{0,...,n} for
n<=4, so4 belongs to H_4. But4*15=13+47, so the corresponding odd product vanishes
modulo t^13. This is a hand-verified refutation of a universal shortcut, not a new
three-generator target or compute seed. No c,g,W or family-wide claim is used for it.

## E446 — an explicit bound on every nonpositive sublevel, uniform over profiles

2026-10-23. **Scope.** Proves Wilf for every S once the residual bounded-conductor
domain below is proved uniformly over ALL multiplicities. Proved reduction: YES; the
theorem below excludes every larger conductor, and the recorded e=2/e=m/complement
theorems cover the excluded parameters. This is a quantitative reduction, NOT a proof
of the remaining finite sign or authorization for bounded enumeration. The constants
depend on m,e and grow quickly. No multiplicity-independent depth bound is claimed.

The user's advisor supplied E416's strict equality obstruction. Here it is made effective
by an elementary rational-vertex argument, with no profile enumeration. The first
user-authorized Sol6.1-high agent independently audited the equality and denominator
steps and sharpened the word-length bound. All proof status here is PAPER / independently
agent-reviewed, not Lean checked; no novelty claim for Zhai's identity, Hadamard's bound,
rational LP geometry, or fixed-multiplicity decidability.

### 1. A quantitative cyclic-tile inequality — PROVED on paper

Let D be a finite down-set in N^d containing 0 and all d unit vectors. Assume |D|=n,
d>=2, n>d+1, and that a linear residue map D -> Z/n is bijective. Put

    L=n-d=n-e+1,             e=d+1.

For every nonnegative weight vector p, with Q=max_(z in D) z.p>0, one has

    d*n*Q-(d+1)*sum_(z in D) z.p >= Q/L^d.             (EFFECTIVE-CH)

This statement uses residue injectivity and a down-set, not semigroup integrality or
primitive values>=n. It therefore also applies at a nonmultiplicity primitive modulus.

**Word-length bound.** A monotone path from0 to a NONZERO word z has |z|+1 distinct cells of D.
Exactly one is a unit vector. The other d-1 unit vectors are additional cells, so
n>=|z|+d. Consequently |z|<=L and ||z||_2<=L for every z in D. In particular L>=2.

**Normalization and strictness.** Choose r in D attaining Q and consider the polytope

    P_r={sigma>=0: r.sigma=1, z.sigma<=1 for every z in D}.

It is nonempty (p/Q belongs), closed, and contained in [0,1]^d because the unit vectors
belong to D. The column identity gives, throughout P_r,

    f(sigma)=d*n-(d+1)*sum_D z.sigma
            =sum_j sum_(j-columns C) |C|*(1-top(C).sigma)>=0.

In fact f>0. Here is the equality audit, including zero coordinates. If f=0, every column
top has weight1. If n_i e_i is the i-axis top, n_i*sigma_i=1, hence ALL sigma_i>0.
The j-column above (n_i-1)e_i has top (n_i-1)e_i+k e_j for an integer k>=1, because its
base weight is less than1. Thus k*sigma_j=sigma_i. Reversing i,j forces all sigma_i equal.
Every column then ends at the same degree H, so D is the full simplex Delta_H: if a
minimal missing word of degree<=H existed, one predecessor's column would end below H.
No word of larger degree is possible. Since n>d+1 and d>=2, H>=2.

As in E416, E=Delta_1-Delta_(H-1) must also inject into Z/n. Equal residues of u-v and
u'-v' imply equal residues, hence equal words, of u+v' and u'+v in Delta_H. But

    |E|=binom(H+d-1,d)+d*binom(H+d-2,d-1)
       >binom(H+d-1,d)+binom(H+d-1,d-1)=|Delta_H|=n,

where the strict inequality is (d-1)(H-1)>0. This is impossible. Therefore f>0 on P_r.

**Denominator bound.** At a vertex of P_r the active normals span R^d, even if P_r has
smaller affine dimension. Choose d independent active equations. Their rows are words
of D (RHS1), or signed coordinate units from sigma_j=0 (RHS0). They form a nonsingular
integer matrix A; every row has Euclidean norm<=L. Hadamard gives

    1<=|det A|<=L^d.

Cramer's rule makes every coordinate denominator divide det A. The objective f has
integer coefficients and integer constant, so the STRICTLY positive f at that vertex
is at least1/|det A|>=1/L^d. A linear functional attains its minimum at a vertex of a
nonempty compact polytope. Hence f>=1/L^d throughout P_r. Scaling back by Q proves
EFFECTIVE-CH. No claim that a vertex is a semigroup or that a finite minimum is integral
is made or needed.

### 2. Effective conductor reduction for ALL semigroups — PROVED on paper

Let S have multiplicity m and embedding dimension3<=e<m. Choose its canonical primitive
factorization tile for Ap(S,m), put d=e-1 and M=c+m-1, and write

    C_m=(e-2)*m*(m-1)/2,            L=m-e+1.

Selmer and CH' give EXACTLY

    m*W+C_m=d*m*M-e*sum_(w in Ap(S,m)) w.

EFFECTIVE-CH therefore yields the uniform inequality

    m*W+C_m >= M/L^(e-1).                              (EFF-W)

In particular every S in this domain with W<=0 satisfies

    c+m-1 <= C_m*(m-e+1)^(e-1).                        (EFF-C)

For larger conductor W is strictly positive. This applies simultaneously to every
realizable profile and every multiplicity, not just a fixed saved face. For each fixed
m,e it makes the remaining nonpositive domain finite. It does NOT bound m, prove the
sign in that domain, or make its enumeration an efficient or approved next action.

The same proof with ANY primitive modulus a and3<=e<a gives

    a*W+(e-2)*a*(a-1)/2 >= (c+a-1)/(a-e+1)^(e-1).

This does not assume the other primitives exceed a. The multiplicity version is the
stronger conductor exclusion; the arbitrary-modulus statement checks compatibility
with E445's warning about even primitives below the least odd pivot.

The exceptions are necessary: e=2 permits a chain D and zero homogeneous deficit;
e=m permits D=Delta_1 and zero deficit. Both already satisfy Wilf by known theorems.
The argument is thus a genuine reduction from all S, with those exceptions handled.

### 3. The full joint certificate has an explicit nonpositive-depth bound too

Use ONLY the original multiplicity-based E414/E417 model here, with x=a-y. There are
k=m-e composite nonzero residues; x_0=x_g=0 on0 and primitive residues. A tight
factorization tree gives x_s<=h_min(s)-1<=|z_s|-1, as in E416.

Order the k nonunit words by nondecreasing degree. For the i-th word of degree h,
its h-2 strict composite prefixes of degrees2,...,h-1 all occur earlier. Thus
|z_i|-1<=i and

    sum_s x_s <= sum_(nonunit z in D)(|z|-1) <= k*(k+1)/2.

Since J=W-e*sum x, EFF-W yields

    m*J >= M/L^(e-1)-C_m-e*m*k*(k+1)/2.                (EFF-J)

Consequently J<=0 forces

    M <= L^(e-1)*(C_m+e*m*k*(k+1)/2).

This holds also for real actual/certificate points in a realizable profile: its fixed
tile still reconstructs all weights, and the x tree bound uses no integrality. It is
not a proof that the joint real minimum, integer capped minimum or cheaper assignment
bound is nonnegative. It supplies an explicit all-profile bound on where a failure
of the full model can occur, not permission to discard composite certificate rows.

### 4. Closed compute gate and research decision

Before this proof, one proposed60-second direct full-tile falsification used the OLD
mirror19 seed. It STOPPED at eligibility in0.00seconds, before ANY neighborhood
comparison: its canonical height is2, already covered by Flat-MaxCL. The independent
baseline is m19,e6,c104,g64,W136,Dep4,kappa5,N20,phase15,Q_full19. It is not a resistant
case. The temporary search-mode change was removed; only explicit Q_full/phase audit
fields are retained. No replacement seed, larger search or positive census was run.

Global review: EFF-W/EFF-J turn strict recession into an explicit, residue-aware growth
bound; they do not pay the finite correction at small coordinates. The finite parity
budget with FULL reserve, weakest useful full-tile Hall budget with both reserves,
and full weighted coupling remain the three universal lines. Do not turn EFF-C into a
fixed-multiplicity project or a giant conductor census. The next decisive result must
control the finite affine budget uniformly, rather than improve this coarse cutoff.

## E447 — first vanishing edges do not injectively account for scalar deaths

2026-10-23. **Scope.** Proves Wilf for EVERY S if the E444 finite source value gain is
paid; reduction YES, its difference is exactly W. This section tests one proposed
component map in that universal allocation. It does not start a three-generator proof
programme or claim the component alone would prove Wilf. The second user-authorized
Sol6.1-high agent supplied the proof below; root checked the arithmetic and membership.
Paper proof only, no numerical work, Lean or novelty claim.

Let A=k[S]/(t^a). For each odd nonpivot primitive p, multiplication has TWO kernels,

    K_p^0=ker(A_even --t^p--> A_odd),
    K_p^1=ker(A_odd  --t^p--> A_even).

A proposed way to control the killed scalar classes in E444 is to follow their chosen
odd-factor word and charge each class to its first vanishing edge. That map need NOT
be injective, and its edge need not have the even parent counted by E445's reserve.

Use ONLY the already recorded S=<13,15,47>, a13. All displayed generators are primitive
and odd; T=S/2 has no positive element below13. With I={0,1,17}+T, for1<=n<=12,

    nI intersect[0,12]={0,...,n}.

Therefore n belongs to H_n=nI minus(n-1)I for every4<=n<=12. These are nine DISTINCT
scalar-layer classes. Their source products are the words(t^15)^n, and all vanish:

    15n-13=47+15(n-4) belongs to S.

The first three powers survive:15-13=2,30-13=17 and45-13=32 do not belong to S.
For32 the only possible generators are13,15; subtracting one of them leaves19 or17,
and no combination gives32. Thus all nine words have the SAME first vanishing edge

    t^45 --t^15--> t^60=0,                 60-13=47 in S.

The indicated first-death map sends nine classes to one slot. This edge has an ODD
parent and EVEN target: its kernel element is in K_15^1, not an even-parent copy in
E445's R_par. So even a two-sided kernel construction must control descendants of a
kernel edge; counting or reserving it just once does not pay every scalar class.

This proves failure of THIS specified map. No comparison between the total number of
scalar deaths and the dimensions of ALL kernels has been computed or refuted. A different
global allocation or weighted descendant estimate remains possible. The exact full
budget requiring payment is still E441/E444/E445; no new sign inequality was proved by
the two-sided-kernel pivot. Stop the first-death injection and rank-only substitution,
not the source parity strategy. The conductor/closure surplus and FULL even-parent
reserve remain available, and no requirement that individual kernel modules pay for
themselves is introduced.

## E448 — advisor's linear stability bound and the correct odd-ideal Hilbert sequence

2026-10-23. **Scope.** Proves Wilf for EVERY S once the finite arithmetic budget is
proved uniformly; reduction YES, E444's identity and the recorded complements. The
quantitative column theorem below is a proved uniform reduction, not that finite sign.
The all-odd specialization has NO proved reduction from all semigroups and is used
only as a specialization/calibration of the general filtration. The four-generator
family falsifies a proposed UNIVERSAL charging rule; it is not a new Wilf family target.

All three main deductions below were supplied by the user's advisor in the review of
318a08b. Root checked them, and the SAME two user-authorized Sol6.1-high agents
independently audited the geometric and algebraic arguments. PAPER PROOFS, not Lean
checked or externally peer reviewed; no novelty claim. E446 remains a valid historical
proof but its denominator bound is superseded by this stronger argument.

### 1. The cyclic-tile gap is Q/(n-d), not merely Q/(n-d)^d — PROVED

Use E446's finite down-set D in N^d, containing0 and every unit vector, with
|D|=n>d+1,d>=2 and a linear residue bijection onto Z/n. Put L=n-d. For every
nonnegative p with Q=max_D z.p>0,

    d*n*Q-(d+1)*sum_D z.p >= Q/L.                       (LINEAR-CH)

Normalize sigma=p/Q, so the MAXIMUM CELL weight is1. Write

    F=d*n-(d+1)*sum_D z.sigma
     =sum_j sum_(j-columns C) |C|*(1-top(C).sigma)>=0.

Suppose F<1/L. Let N_i e_i be the i-axis top and delta_i=1-N_i*sigma_i. The axis
column plus the other d-1 unit vectors gives1<=N_i<=L. Axis contributions are distinct
terms of the column sum, so

    F>=sum_i(N_i+1)*delta_i.                            (AX)

This already excludes sigma_i=0, which would contribute at least2. Positivity has
not been assumed.

For i!=j, the word(N_i-1)e_i MUST extend by e_j. If N_i=1 this is the existing unit
e_j. If N_i>1 and its j-column were a singleton, that column is distinct from EVERY
axis column: its direction is j and its base has positive i-coordinate. Its contribution
delta_i+sigma_i can therefore be added without double counting to the i-axis term:

    F>=(N_i+2)*delta_i+sigma_i
      =1/N_i+(N_i+2-1/N_i)*delta_i>=1/N_i>=1/L,

a contradiction. The required extension has weight at most1, giving

    sigma_j-sigma_i<=delta_i for all i!=j.              (EXT)

All N_i are equal. Indeed, if a=N_i<b=N_j, the exact identity and reversed EXT give

    b-a=b*delta_i-a*delta_j+a*b*(sigma_i-sigma_j)
        <=b*delta_i+a*(b-1)*delta_j
        <=L*((a+1)*delta_i+(b+1)*delta_j)<=L*F<1.

The coefficient comparison uses a,b<=L and nonnegative deficits. It contradicts the
positive integer b-a. Write the common axis length H. From AX,

    (1-F/(H+1))/H<=sigma_i<=1/H.                       (WEIGHTS)

A column top of degree at most H-1 has weight<=(H-1)/H, so that column alone
contributes at least1/H>=1/L>F. A top of degree at least H+1 has, by WEIGHTS, weight
at least(H+1-F)/H>1, since F<1. Both are impossible. Thus EVERY column top has degree H.

Every cell consequently has degree<=H. A minimal missing word of degree<=H would
have a predecessor whose corresponding column ends below H. Therefore D=Delta_H.
H=1 contradicts n>d+1; for H>=2 the E416 injection of Delta_1-Delta_(H-1) into Z/n
contradicts its cardinality greater than|Delta_H|. This finishes the contradiction
and proves LINEAR-CH. No rational-vertex or denominator estimate is needed.

### 2. Polynomial conductor reduction — PROVED

For EVERY numerical semigroup with3<=e<m, put

    M=c+m-1, C_m=(e-2)*m*(m-1)/2, L=m-e+1.

The exact E446 identity and LINEAR-CH give

    m*W+C_m >= M/L,
    W >= (c+m-1)/(m*(m-e+1))-(e-2)*(m-1)/2.             (LIN-W)

Thus every such S with W<=0 satisfies

    c+m-1<=C_m*(m-e+1)
          <=m*(m-1)/2*floor((m-1)^2/4)
          <=m*(m-1)^3/8.                               (QUARTIC-C)

The optimization is elementary: (e-2)+(m-e+1)=m-1 and their product is at most the
displayed integer square bound. This is a quartic cutoff in m for ACTUAL nonpositive W.
It leaves m unbounded. Along every sequence with fixed m,e and c tending to infinity,
liminf W/c>=1/(m*(m-e+1)). The e=2/e=m exceptions are necessary and already satisfy
Wilf. No bounded-conductor census or further cutoff refinement is activated.

For any other primitive modulus a with3<=e<a, the same geometric proof gives

    a*W+(e-2)*a*(a-1)/2 >= (c+a-1)/(a-e+1).

It does not require the other primitives to exceed a. For the ORIGINAL full
multiplicity-based E414 joint model, keep k=m-e and E446's sum x<=k(k+1)/2:

    m*J>=M/L-C_m-e*m*k*(k+1)/2.                         (LIN-J)

Hence J<=0 implies M<=L*(C_m+e*m*k*(k+1)/2), also for real actual/certificate points.
This second bound is not claimed quartic uniformly in e, and does not imply minimizer
integrality or a finite-minimum sign. Composite certificate rows remain necessary.

### 3. The odd ideal gives a genuine associated graded algebra — PROVED

Let A=k[S]/(t^a), a the least odd primitive. Let V_n span products of n odd classes,
with V_0=A_even, and put o=(A_odd). E444 gives V_(n+2) subset V_n and v_i=h_i for i1,2.
Even multiplication preserves V_n and odd multiplication takes it to V_(n+1).
Consequently o=V_1 directsum V_2 and, for EVERY n>=0,

    o^n=V_n directsum V_(n+1),
    gr_o(A)_n isomorphic V_n/V_(n+2).                  (ODD-GR)

The two direct summands have opposite parity. Expanding(V_1+V_2)^n gives V_j for
n<=j<=2n, and nesting reduces them to the two stated parity pieces. For n0 the formula
is A=V_0 directsum V_1. The quotient isomorphisms preserve VALUE grading; taken together
they preserve multiplication. This is not an assertion that A has a standard grading
by original factorization length.

Put B=A/o, v_n=dim V_n and b_n=v_n-v_(n+2). Nilpotence and telescoping give

    b_n>=0, sum_(n>=0)b_n=a,
    b_0=dim B=a-h_1-h_2, B isomorphic A_even/V_2.

The q ORIGINAL nonpivot odd primitive classes generate o. Therefore there is a
value-graded surjection B[Y_1,...,Y_q] -> gr_o(A), where Y_j has o-degree1 and
value degree p_j. For n>=1,

    b_n<=binom(q+n-1,n)*b_0,
    v_3>=h_1-q*(a-h_1-h_2).                            (MODULE)

For q0 read positive-degree dimensions as0; E439 separately handles that source case.
The value-resolved version, retaining the original primitive VALUES, is

    dim(gr_o A)_(n,w)
      <=sum_(alpha in N^q, |alpha|=n) dim B_(w-alpha.p). (VALUE-MODULE)

This is the graded surjection's degreewise dimension bound, not freeness or a sign
theorem. Original even primitive classes survive indecomposably in B: vanishing or
decomposing one would decompose that source primitive as a sum of positive S elements.
Thus their original actions remain in the coefficient ring rather than being counted
as independent new odd generators.

If ALL original primitives are odd, B=k, o is A's maximal ideal, q=e-1 and

    b_0=1, b_1=q, h_1+h_2=a-1,
    v_3=h_1-q, h_1-h_3<=q.

Here gr_o(A) is a standard graded k-algebra, so ordinary Macaulay theory applies to b.
For mixed parity B can have dimension greater than1: use MODULE/VALUE-MODULE instead
of silently applying ordinary field-based Macaulay with q generators. There is no
proved reduction from all S to the all-odd specialization.

For the EXISTING13/15/47 control, x=t^15,y=t^47 gives

    A isomorphic k[x,y]/(x^4,x*y^3,y^4).

The three monomials vanish since60-13=47,156-13=143=11*13, and
188-13=175=10*13+3*15. The quotient has13 standard monomials (the4-by3 rectangle
plus y^3), so its surjection to the13-dimensional A is an isomorphism. Their ordinary
degrees give b=(1,2,3,4,2,1). This control's grading is not assumed for general A.

### 4. Surviving degree moment plus killed scalar mass — EXACT

Let eta_n=h_n-v_n>=0. E444 gives eta_1=eta_2=0. Since all sums are finite,

    sum_(n>=1)n*b_n=v_1+2*sum_(n>=2)v_n,
    h_1+2*sum_(n>=2)h_n
      =sum_(n>=1)n*b_n+2*sum_(n>=3)eta_n.              (SURVIVE-DEATH)

The left side is E442's exact lift mass sum lambda. Substitution into E441 retains
the FULL budget:

    W(S)=2W(U)+2(e-e_U)*ell_U+(e-1)*(c(S)-2c(U))
         -e*(b+sum_(n>=1)n*b_n+2*sum_(n>=3)eta_n),

where the isolated b=(a-1)/2 is NOT the sequence b_n. No summand is assumed to pay
itself. Correct Hilbert structure controls the surviving moment; it does not by itself
bound the killed mass. The actual values, coefficient actions, conductor/closure surplus
and full parent reserve remain required for a quantitative finite payment.

### 5. Unbounded first-death multiplicity in the remaining domain — PROVED

For EVERY odd a>=15, let S_a=<a,a+2,3a+8,3a+10>. All four generators are primitive:
the high ones are below4a and cannot be sums of one or three low generators (three low
offsets are at most6), while their difference2 is below the least positive element.
Every leave-one-out gcd is1. Omitting a leaves gcd(a+2,2,4)=1; omitting a+2 leaves
gcd(a,8,10)=1; omitting either high generator leaves a,a+2.

The even number5a-1 is a gap. A representation would have two or four odd generators;
six are too large. Two low generators are too small, two high too large, and high+low
is at most4a+12<5a-1. Four low generators total at most4a+8<5a-1, while one high plus
three low is already at least6a+8. Thus m=a,e4,3e<m and c>=5a>4m.

Here T=S_a/2 has least positive element a and I={0,1,a+4,a+5}+T. Below a, nI={0,...,n}
for1<=n<=a-1, so n belongs to H_n throughout that range. With p=a+2, the first three
powers survive modulo t^a:2,a+4 and2a+6 are gaps. But4p=a+(3a+8), and for4<=n<=a-1,

    n*p-a=(3a+8)+(n-4)*p belongs to S_a.

Thus a-4 DISTINCT scalar classes share the SAME first vanishing edge3p->4p. Its
parent is odd and formal target even. Their weighted killed contribution is at least
2(a-4), unbounded even with fixed source e4 and all recorded sparse/deep/cofactor
restrictions. This refutes any capacity bounded independently of a on THAT natural map,
not value-dependent capacities, a global descendant allocation or Wilf. No family
enumeration or family-W theorem is a target.

### Review / next finite obligation

The advisor's strengthened stability theorem is substantive and its proof is sound.
Treat the polynomial conductor exclusion as completed; do not spend the next cycle
optimizing its constant. ODD-GR and SURVIVE-DEATH identify the correct algebra and the
unpaid killed mass. VALUE-MODULE is retained so that a future allocation can use actual
primitive increments and the coefficient ring, not only dimensions. The universal
finite value gain remains unproved; neither Macaulay nor the unbounded countermap
family is represented as a proof of it. The differential branch remains secondary:
its proposed inequality is exactly W>=R_rel, a stronger demand needing its own payment.

## E449 — primitive-preserving rounding, and its unavoidable finite sign cost

2026-10-23. This paper component was obtained in the E448 arithmetic task BEFORE the
advisor's latest steering, then preserved/deferred while the advisor audit took priority.
Scope: Proves Wilf for every S IF the full real actual domain is nonnegative; reduction
YES, E414/E417 and complements. A negative real point would refute this stronger route,
not Wilf. The lemma below realizes real points arithmetically but does NOT transfer their
sign. Supplied by the first already-authorized agent; root audited it. No new computation,
optimization, profile census, additional agent or novelty/Lean claim.

### Primitive ceilings retain exactly e generators — PROVED

Let p be a real point of a realizable E414/E417 actual profile, with original primitive
residues g_j, multiplicity m and d=e-1. Set

    p'_j=m*ceil((p_j-g_j)/m)+g_j,
    delta_j=p'_j-p_j in[0,m),
    S'=<m,p'_1,...,p'_d>.

The displayed E generators are EXACTLY the minimal generators of S'. All exceed m
except m itself, and their residues have gcd1 with m because the profile is realizable.
For any non-m word z!=e_j of residue g_j, seed primitiveness makes it strict. E417's
affine rewriting then gives z.p-p_j>=m, including words outside the canonical tile.
Therefore

    z.p'-p'_j=(z.p-p_j)+z.delta-delta_j>=m-delta_j>0.

A representation using extra copies of m is even larger. No displayed p'_j decomposes;
the generating set admits no additional minimal generator. Thus S' is numerical with
m(S')=m,e(S')=e. Every word value weakly increases, so its genuine Apéry values satisfy
w'_s>=w_s and c(S')>=c_real. In particular q>=5 and3e<m survive. The tight profile and
top residue need NOT survive.

The exact remaining rounding payment is

    W(S')-W_real=(e-1)*(M'-M)-(e/m)*sum_s(w'_s-w_s).     (CEIL-COST)

Both increments are nonnegative. The lemma proves preservation of the ORIGINAL
generator count, not a favorable sign of their difference.

### The cost can have either sign in the remaining domain — PAPER witness

The OLD19 profile has the five primitive words for39,41,50,52,53 and all degree2 words
EXCEPT39+52 and41+50. The two omitted sums are91, above their canonical53 by38.
These1+5+13 words have every residue modulo19 once; all higher-degree words exceed the
largest106. The top word is2*53. Coordinate sums are(6,6,6,6,7), giving

    H=5*19*z_top-6*sum z=(-36,-36,-36,-36,148).

Take integer primitives P*=(799,839,1019,1059,1079)=20*(39,41,50,52,53)+19, with m19.
The same tile remains genuine: all triples have value>=2397>M2158; the omitted pairs
have value1858, above canonical1079; residues are unchanged since20=1 modulo19.
Every leave-one-out primitive gcd is1: gcd(799,839)=1 handles deletion of m, while retaining
prime19 handles each other deletion. Exact sums give c2140,g1562,W1328, e6,3e<m.

Lower ONLY799 by1/2 to obtain real point A, or ONLY1079 by1/2 to obtain real point B.
Both obey the FULL same actual profile. Tight rows are word identities. Strict primitive
rows from omitted pairs retain gap>=778.5; triple rows retain gap>=237.5, both>m.
Distinct integer Apéry values for P* are at least20 apart; a perturbation changes any
word of degree<=2 by at most1, so top differences remain>=19>any required residue
distance18. Primitive positivity and q>=5 have ample slack. The top residue stays11,
with q_A113 and q_B113-1/19. The primitive ceilings of BOTH points are exactly P*.

Consequently

    W(P*)-W(A)=H_799/(2*19)=-18/19,
    W(P*)-W(B)=H_1079/(2*19)=74/19.

These are two real points in ONE existing realizable profile, not new optimized profiles.
Both real defects are positive. They refute either proposed monotonicity of CEIL-COST,
not real actual positivity or Wilf. The exact examples and all real constraints were
independently checked on paper by the same authorized reviewer; no numerical run is claimed.

### Rounding every Kunz coordinate has a separate generator-count cost

For real actual Kunz coordinates xi_s and top q, shared ceilings
k_s(t)=ceil(xi_s+t), q_t=ceil(q+t),0<t<1 preserve closure, strict non-tight rows and
the top residue. They can CREATE primitive residues. With fixed-e pseudo-defect V_t,

    integral_0^1 V_t dt=W_real+e-m,
    integral_0^1 W(S_t)dt
      =W_real+e-m+integral_0^1(e_t-e)*ell_t dt.

This extra term cannot generally be bounded by m-e: starting at ANY integer Kunz
vector, all nonzero coordinates increase by1, every nonzero tight pair gains a unit
gap, e_t=m and ell_t=ell+1. On OLD19 the term is13*21=273, not13. This stops that
rounding shortcut. A rowwise floor argument also cannot assume closure from a tight
row alone: fractional parts(.6,.6,.2) give rounded slack-1 for0<t<.4; this is a local
row obstruction, not an asserted full-profile counterexample.

Decision: preserve primitive rounding as an arithmetic bridge with controlled e, while
keeping CEIL-COST unpaid. No rounding or regional LP expansion is prioritized over the
advisor's finite value/descendant payment. A real witness, if sought later, must satisfy
ALL actual rows and depth/sparse restrictions, not just one fractional closure row.


## E450 — exact batched Apéry scans and phase witnesses; bounded GPU pilot

2026-10-23. Proves Wilf for: EVERY numerical semigroup IF a uniform full-budget
payment or realizability theorem is extracted. Proved reduction from all S to this
case: yes, E430/E432 SUPP-WILF plus the recorded c<=4m and3e>=m complements.
The engine and finite pilot are diagnostic prerequisites, not a proof of that theorem.
The scan/phase proposals came from the user's advisor. No novelty claim or Lean claim.

**SCAN (proved).** Fix m>=1, positive supplied generators, and exact old distances
w in residues modulo m, allowing infinity for unreachable residues. On adjoining p,
put delta=p mod m, g=gcd(m,delta), h=m/g. For each cycle choose a representative b
in0,...,g-1 and let r_t=b+t*delta mod m,0<=t<h. With A_t=w_(r_t)-t*p,

    w'_(r_t)=t*p+min(min_(s<=t) A_s, h*p+min_(s>t) A_s).

The second minimum is infinity if its index set is empty; infinity is tested explicitly
before arithmetic. Any enlarged factorization is an old factorization followed by j
copies of p. If j>=h, removing h copies preserves the residue and lowers the value,
so a minimum has0<=j<h. For a start s<=t use j=t-s; for s>t use j=t-s+h.
This gives the formula, including noncoprime intermediate stages. Prefix and suffix
minima give O(m) work per generator and O(mk) total work, with O(m) CPU workspace.
The CUDA implementation uses flagged segmented minima on all residue cycles.
The flagged operation (v,a)*(w,b)=(b?w:min(v,w),a OR b) is associative: it selects the
minimum after the last marked segment start. Threads outside m use an isolated
infinite entry and execute the same barriers as every active thread.

**DISTANCE-WITNESS (proved).** A finite proposed array is exact if w_0=0, all entries
are nonnegative with w_r congruent r mod m, every supplied-generator edge satisfies
w_(s+delta)<=w_s+p, and every nonzero residue has a tight predecessor with smaller
value. Predecessors terminate at0, proving attainability. Conversely, summing edge
inequalities from0 bounds w_r by every attaining path length. Together these give
equality with the shortest distance. For partial arrays, finite-source edges also
verify that no reachable residue was declared infinite; each finite nonzero entry
still has its strictly decreasing predecessor. Verification costs O(mk).

**PRIMITIVE-EDGE (proved).** Assume all supplied p>m and gcd(m,p_1,...,p_k)=1, so m
is the actual multiplicity. A nonzero Apéry value w_t is composite iff
w_t=w_s+p_j for a supplied generator and s!=0. The forward implication uses an
attaining factorization of w_t: it cannot contain m. If it is composite, a minimal
factorization has at least two supplied generators. Remove one; the remainder must
be its residue's Apéry representative, since replacing it by a smaller one would
contradict minimality of w_t. Its remainder residue cannot be0, since a positive
multiple of m in such a factorization would make w_t-m belong to S. The converse
is a positive two-summand decomposition. Hence scanning only mk generator edges
finds the ACTUAL embedding dimension. This does not remove composite-parent rows
from certificate models. The m=1 convention is handled separately with c=g=W=0.

**PHASE-SWEEP (proved from the support identity).** Keep the residue-labelled canonical
lex tile and its primitive residues fixed, and write d=e-1, C=(e-2)m(m-1)/2. For a
proposed TOP RESIDUE r (not rho=(-c) mod m), define

    m Q(r)=m Dep+sum_s Gamma_s*((r-s) mod m)-C.

Since sum Gamma=d*m, advancing r by1 increases every cyclic distance by1 except
at s=r+1, where it decreases by m-1. Thus

    Q(r+1)-Q(r)=d-Gamma_(r+1).

One direct phase and a sweep score all m phases in O(m) work. These are abstract
scores unless the specified top/tile/primitive residues are simultaneously realized.
On an actual semigroup the support identity is exactly

    W=Q+R,  Q=Dep+N-kappa,  R=Gamma.mu-Dep>=0.

Changing generator heights within a region retaining those data cannot change Q.
Any optimization of Q must cross a structural boundary. The actual W<=0 conductor
cutoff from E448 does NOT exclude a possible Q<0<W and was not applied to this pilot.

**Exactness/implementation limits.** src/apery_scan uses signed64 weights, with host128
validation8*m*m*max(p)<2^60 and a separate infinity sentinel. A shortest finite residue
path can be made simple, so it uses at most m-1 edges. This bounds intermediate
finite weights and scan arithmetic by a few m*max(p), and invariant arithmetic by
a few m^2*max(p). Supplied values may be redundant or repeated; actual primitives
are reconstructed. CPU m<=8192; the present CUDA block implementation supports m<=1024.
Canonical words resolve lexicographic ties on primitive residues in ascending order.
The shortest-path predecessor witness alone does not certify those tie choices;
the independent verifier reconstructs them and enumerates columns explicitly.

**Outcome / strategic decision.** CUDA passed every tested prefix and the full finite
batches, and compute-sanitizer reported0 memory errors. All36860 eligible inputs in
the36864-candidate pilot were already residue-support excluded. Therefore this sampler
provided NO resistant profile, negative Q, allocation obstruction or new Wilf evidence.
It is CLOSED; do not enlarge its sample count or extend the rental. Kernel speed did
not translate to a pipeline gain at these batches because allocation/transfers and
CPU canonical analysis dominate. Retain the exact engine and compact witnesses.
Before another compute campaign, derive a construction that can satisfy Dep<kappa,
height>=3 and the intended realizability conditions, and state the allocation lemma
it would distinguish. E448 parity/Hall finite-budget work remains the mathematics.
The exact parameters, timings, checked records and cleanup evidence are in E450 of
EXPERIMENTS.md and src/apery_scan/data; they establish finite checks only.


## E451 — exact mirror phases and residue-column scalar deaths

2026-10-23 14:40 EDT. Proves Wilf for: EVERY numerical semigroup IF the remaining finite
full-tile or parity payment holds. Proved reduction from all S to this case: yes,
SUPP-WILF/E432 and E444/E448 plus complements. These are proved STRUCTURAL COMPONENTS,
not finite positivity. No new computation, restriction to all-odd sources, manuscript,
Lean or novelty claim. Same two user-authorized agents supplied independent proof work;
root checked the arguments below. The user's next steering moved engineering to E452.

### 1. Mirror phase pairing at the same maximal cell

Let m>=2 and let D be a full residue-injective factorization tile of size m in
dimension d, with primitive residue map delta. Fix a maximal cell a of D and evaluate Q with
TOP CELL a in both orientations delta and -delta. Then exactly

    Q_delta(a)+Q_(-delta)(a)=2Dep+m-1-|a|.             (MIRROR-Q)

Proof: E450 gives mQ=mDep+sum_z Gamma_z*[(phi(a)-phi(z)) mod m]-C,
C=(d-1)m(m-1)/2. At z=a both mirrored distances are0; at every other z they sum to m,
by residue injectivity. Thus the sum is2mDep+m(dm-Gamma_a)-2C. A maximal cell has
Gamma_a=d+|a|. Divide by m and simplify. More generally at any cell a the right side
is2Dep+m+d-1-Gamma_a, but only maximal cells can be actual tops with positive weights.
This identity does not transfer nonnegativity between orientations.

The mirror with the SAME tile and top is genuinely realizable from an actual seed:
replace each nonmultiplicity primitive p_j by (m-1)p_j, retaining m. Every residue
path weight scales by m-1, and the residue map is negated bijectively. Hence the
Apéry values scale, the canonical tile and top cell persist, and exactly the original
e is retained. More generally any positive L coprime to m does this unit relabelling.
Selmer/conductor formulas give

    W_L=L*W+(L-1)*(e-2)*(m-1)/2.                      (INFLATE-W)

For L=m-1, write B=(e-2)(m-1)/2 and K=2Dep+m-1-|a|. Using W=Q+R and the actual
inflated identity W_L=(K-Q)+R_L yields

    mW=K+R+R_L-(m-2)B >= K+R-(m-2)B.                (MIRROR-R)

The subtraction remains and is not known to be paid. No sign theorem follows.
Old19 and its recorded mirror give Q5+Q19=24=2*4+18-2, a consistency check already
available in the record, not a new search. Positive inflation also raises the genus;
it does not descend a hypothetical minimal counterexample.

For a different proposed maximal top, E431 supplies a sufficient realizability test:
a rational positive primitive direction q annihilates all tight factorization trades,
is nonnegative on strict boundary differences (strict positivity also suffices), and
has (a-z).q>0 for every z!=a. Clear denominators and use p+mKq. Old strict affine margins
are preserved and the proposed top dominates for large K. This can turn an abstract
negative phase into a genuine Q-bound counterexample if such a phase/direction is
found; it does not assert that every maximal cell passes the test.

### 2. Killed scalar classes are initial segments, pointwise lift identity

Use E441 notation at the least odd primitive a: T=S/2, I={u:a+2u in S}, U=<I>.
For a residue s modulo a let u_s,t_s,i_s be their least representatives and put

    K_s=(t_s-u_s)/a, L_s=(i_s-u_s)/a,
    epsilon_s=K_s-L_s in{0,1}, lambda_s=K_s+L_s.

For0<=k<K_s define u(s,k)=u_s+k*a and the scalar birth

    n_s(k)=min{n>=1:u(s,k) in nI}.

Each u(s,k) belongs to exactly H_(n_s(k)); these are ALL scalar classes in U minus T.
For two successive positions that are BOTH outside T,

    n_s(k+1)<=n_s(k)-2.                              (BIRTH-DROP)

Indeed n_s(k)>=2 in that situation: if it were1, a+I subset T would put the next
position in T. Now a+nI subset(n-2)I implies the displayed drop. The last transition
to T is excluded: a birth1 can drop to0, so do not assert the inequality there.

The product for u(s,k) has source value

    n_s(k)*a+2u(s,k)=2u_s+a*(n_s(k)+2k).

E441 gives the source Apéry value in residue2s as2u_s+a*lambda_s. Since the product
belongs to S, its excess

    E_s(k)=n_s(k)+2k-lambda_s

is a NONNEGATIVE integer. It is nonincreasing along k while outside T by BIRTH-DROP.
A scalar class survives in A=k[S]/(t^a) exactly when E_s(k)=0; otherwise it is killed.
Therefore killed positions form an INITIAL segment0,...,D_s-1 and surviving positions
form the remaining TERMINAL segment. There cannot be alternating surviving/dead holes
in a column. This statement uses actual multiplication/value labels, not a Hilbert
function with an assumed source generator count.

Let nu_s be the largest number of nonpivot odd primitives in ANY factorization of the
source Apéry value in residue2s. Equivalently it is its largest odd-ideal filtration
degree; set nu_s=0 if that value is in no positive odd-product space. From E444, all
surviving scalar representations are exactly those products. On the surviving tail,
n_s(k)+2k=lambda_s, so its degrees are nu_s,nu_s-2,..., down to1 if epsilon_s=1,
and down to2 if epsilon_s=0 and nu_s>0. If the tail is empty then epsilon_s=0:
otherwise the last gap position lies in I and gives a surviving degree1 product.
Consequently, POINTWISE,

    lambda_s=nu_s+2D_s,
    K_s=ceil(nu_s/2)+D_s,
    L_s=floor(nu_s/2)+D_s.                            (POINTWISE-DEATH)

Also nu_s mod2=epsilon_s. This includes s=0 and columns with K_s=0. The nu_s are
filtration degrees, not an assumption that the original value grading is standard.
Summing recovers E448's moment/death identity because b_n counts source Apéry values
whose largest filtration degree is n, and sum D_s=sum_(n>=3)eta_n.

This refinement retains WHERE the killed mass sits. It does not bound sum D_s by a
paid resource. In particular first-death edges still have unbounded descendants, and
there is no bound assumed on the number of minimal kernel generators. The next
parity inequality must pay the full surviving moment AND these initial-segment lengths
using actual values, full W(U), coefficient ring B and parent reserves together.


### 3. A value-sensitive bound on the ENTIRE killed mass; standalone payer fails

For q>0 original nonpivot odd primitives, define alpha=min(p-a)/2>0 over those
primitives and J=#{s:D_s>0}. Then the pointwise column structure gives

    alpha*(nu_s+2D_s+1_(D_s>0))<=u_s,
    2sum D_s<=sum_s floor(u_s/alpha)-sum_s nu_s-J.     (VALUE-DEATH)

Proof: if K_s=0 both nu_s,D_s vanish. Otherwise u_s is in H_(n_s(0)). Every nI
representation of an element of H_n has all n factors outside T: a T factor could
be absorbed into the remaining ideal factors, placing it in(n-1)I. Since I=A0+T,
every outside-T factor is at least alpha. Thus u_s>=alpha*n_s(0). If D_s=0, the
first class survives and n_s(0)=lambda_s=nu_s. If D_s>0, it is killed, giving
n_s(0)>=lambda_s+1=nu_s+2D_s+1. Sum after dividing by alpha and taking floors.
This uses actual closure values and original primitive increments, with no assumed
bound on kernel roots or constant capacity on first-death edges. q=0 is separate:
all primitives except a are even, so the E439 normalization applies (or e=1/N).

This controls the full descendant count but is TOO WEAK as a stand-alone payer.
Writing A_alpha=sum floor(u_s/alpha), OC-W gives the valid bound

    W(S)>=2W(U)+2(e-e_U)ell(U)+(e-1)(cS-2cU)
          -e*(b+A_alpha-J).

On the ALREADY recorded k2 control S=<13,15,17,19>, a13,U=N,alpha1,A_alpha78,
b6,c64,e4, J<=12 makes the displayed lower bound at most-96, although W48.
No new numerical run: all invariants are from E444's fixed calibration. It is sharp
on the old equality calibration<5,7>, but those positive calibrations cannot prove
its sign. STOP any claim that this bound alone pays OC-W. The next refinement must
use the distribution of the ORIGINAL odd increments/value-graded module, retaining
both W(U) copies and full reserves; the minimum alpha discards too much information.
