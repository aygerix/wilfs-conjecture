# PROOFS.md — precise statements, proofs, dependency graph, status

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
