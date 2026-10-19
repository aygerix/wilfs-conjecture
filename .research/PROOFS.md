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
- Relation to the literature: the class contains the Eliahou–Fromentin near-miss family (LITERATURE #30: c = 4m,
  A ⊂ [(3m+1)/2, (5m−1)/3] a B₃-set, W₀ = −C(n,3)). For that family they prove W ≥ 9; GW-25 proves W ≥ e − 2 for
  the whole class, uniformly in e. In P_4 terms (GW-21/24), GW-25 is the primary regime with b = c = e = 0 and
  q₂ = 0, for every a, including missing AA pairs. It supersedes the a = 7 computer certificate (GW-24) and codex's
  "uniform remaining claim" 4[C(a+2,3) − u₄] + ρ ≥ C(a+1,3).
- Mechanism: packing (LP/SP/HP) uses residues only, and loses a factor ≈ a. The arc uses the integer location of
  τ = v − deg·m inside its band: a whole residue arc of length ≈ h/2 is reachable only by pairs. This forces
  ρ = m − h ≥ m − 2p − 2, and ρ enters W with coefficient +1.
- OPEN extension: the same class with B/C/E directions or with q₂ > 0. A crude count of intruders into the arc fails
  when a B direction carries many AAB cells. Those configurations are where packing is strong, so an interpolation
  is needed.

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
- No-sharing form: deficit(y) ≤ Σ_b Δ⁺(y − e_b) holds on all data.
- FALSE refinements:
  - equal split among lower covers: ⟨5,8,9⟩; d = 3, m = 7, n = (8,11,12);
  - pay from y − e_b with b = argmax n_b (⟨5,8,9⟩) or b = argmin n_b (⟨8,9,13,14⟩).
- Residue-free, CP fails even where GW holds (d = 2, m = 9, n = (12,12), GW slack 2). So CP needs residues more than
  GW does.

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
- P_4: PARTIAL (GW-21, GW-24). Proved: H4 for M ≥ 6m − 1 (residue-free, sharp), and M ≥ 6m − 3 with residues
  (distinct weights). The primary regime 4m ≤ M < 5m is proved for a ≤ 5 on paper and for a = 6 with two finite
  certificates. Also proved: quadratic down-sets and saturated EF faces. Open: the primary regime for a ≥ 7, and
  5m ≤ M ≤ 6m − 4. The primary
  regime is Wilf for 3m < c ≤ 4m, which is OPEN in the literature (LITERATURE item 22).
  - Theorem H does not extend to i = 4 without residues: {|x| ≤ 3} ⊂ ℕ², n = (16,17), m = 10, M = 51 ≥ 5m − 1
    gives 27 > 26.
  - The class-face splitting of the band proof also fails at K = 4 (E200).
- A proof by induction on i must move mass across depths, because the per-depth inequalities are false.
