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
line x + ℕe_a, say n(u') = n(u) + j e_a (j ≥ 1), and u' = u + j·n_a ≥ c + n_a > c + m, contradicting u' ∈ X.
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

**Lemma CHT (any D).** δ(D) ≥ m + 1 − (2t + 2|Tri| + |Q'|).
Proof. δ = 1 + Σ_x (h(x) − 1) (since H = Σ_x h(x)), h ≥ 0 integer, {h = 0} = Max ∪ Tri, {h = 1} = Q' (a non-maximal top has ht ≥ 1;
h = 1 forces two maximal tops and the third of height 1). So δ ≥ 1 − (t + Tri) + (m − t − Tri − Q'). ∎

**Level picture (𝒞).** φ(p) = min(F(p₁), G(p₂)) on A₃; U_v = {p ∈ A₃ : φ(p) ≥ v} = A₃ ∩ R_v, R_v = [0,a_v) × [0,b_v),
a_v = #{i : F(i) ≥ v}, b_v = #{j : G(j) ≥ v}; U₁ = A₃, U_{L₃+1} = ∅, U_{v+1} = U_v ∩ R_{v+1}. U_v is the slice x₃ = v − 1.
(i) (p, v−1) ∈ Max ⇔ p is a corner of U_v and p ∉ U_{v+1}. Write M_v for these p.
(ii) A corner p of U_{v+1} that is not a corner of U_v is the top cell of column a_{v+1} − 1 (then a_{v+1} < a_v) or the last
cell of row b_{v+1} − 1 (then b_{v+1} < b_v). [If p + e₁ ∈ U_v ∖ U_{v+1} then p + e₁ ∉ R_{v+1} ∋ p, so p₁ = a_{v+1} − 1 < a_v − 1.]

**Lemma T (type bound; 𝒞).** t ≤ C − 2.
Proof. Corners of U_v lying in U_{v+1} are corners of U_{v+1}; so |M_v| = κ(U_v) − κ(U_{v+1}) + ν_v with ν_v = #corners of U_{v+1}
that are not corners of U_v ≤ [a_{v+1} < a_v] + [b_{v+1} < b_v] by (ii), and ν_{L₃} = 0. Telescoping,
t = κ(A₃) + Σ_{v<L₃} ν_v ≤ c(A₃) + (c(A₂) − 1) + (c(A₁) − 1), because a drops at v exactly when v is a value of F, and the
value L₃ = F(0) is excluded (same for G). ∎ (Tight for boxes; exhaustive check: max(t − C) = −2 for every |D| ≤ 40, E125.)

**Lemma T' (cone class).** t ≤ C. Proof: as Lemma T; for v > q₃ the slices are U_v = (A₃ ∩ R_v) ∖ Q, Q = [q₁,∞) × [q₂,∞), and
U_{v+1} = U_v ∩ R_{v+1} for v ≠ q₃; at v = q₃ the removal of Q creates at most two further new corners (the top of column
q₁ − 1 and the end of row q₂ − 1). ∎ (Exhaustive: max(t − C) = 0, attained, union ≤ 34.)

**Lemma B (corner–area bound; 𝒞 and cone class).** C² − 3C + 6 ≤ 6m, i.e. C ≤ 3/2 + √(6m − 15/4).
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

**Theorem C-HT (𝒞; proved on paper 2026-10-18 night 15).** Every D ∈ 𝒞 satisfies LHS = 2t + 2|Tri| + |qU| + |qO|
≤ 2t + 3(t − 1) = 5t − 3 ≤ 5C − 13 (Lemmas TF, F, QF, T). With Lemma CHT this gives δ(D) ≥ m + 14 − 5C. By Lemma B,
C ≤ ⌊3/2 + √(6m − 15/4)⌋ ≤ (m + 14)/5 for every m ≥ 131: checked exactly for 131 ≤ m < 2·10⁵, and for m ≥ 160 it holds
because 5(3/2 + √(6m)) − 14 ≤ m. Hence **δ(D) ≥ 0 (HT) for every D ∈ 𝒞 with |D| ≥ 131.**
Consequence for e = 4: every non-two-face tile in 𝒞 with m ≥ 131 satisfies the height criterion, so Wilf holds for the
corresponding semigroups. The tiles still uncovered are (i) 𝒞-tiles with m ≤ 130, handled by the exhaustive HT scan
(tile_scan_HM, complete so far for m ≤ 82, 91–95, 101–104, 109–111), and (ii) cone-class tiles, which need a separate
bound. In the lattice-free cone class LHS − 5C is unbounded above, and 2|Tri| − t reaches 8 at union ≤ 32.
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
z < q₃. Under (β), p ∈ Quad and z < ψ(p) = q₃. The mirror cases are symmetric. ∎

**Fiber Lemma.** Two distinct DS cells never share a maximal top in the same direction.
Proof. Let x̂ = x + k e_a (k ≥ 1) with the same top_a, and let c, ĉ be their nonmax directions (both ≠ a).
- ĉ ≠ c: by the Location Corollary, x_ĉ ≥ q_ĉ (x ∈ B_c) and x̂_ĉ < q_ĉ (x̂ ∈ B_ĉ). But x̂_ĉ = x_ĉ. ✗
- ĉ = c = 3, a = 1: x = (X, Y, z) and x̂ = (X+k, Y, z), both in B₃, so p = (X, Y) and p̂ = (X+k, Y) lie in Quad.
  - γ(p) = γ(p̂) = 1, so by (P1′) ψ(p) > ψ(p̂). With Q = q₃ at both, this gives F(X+k) < min(F(X), G(Y), q₃).
    Hence (i) F(X+k) < G(Y), (ii) F(X+k) < q₃ and ψ(p̂) = F(X+k).
  - x̂ has a 2-partner û. By (i) and the mirror lemma, (α′) or (β′) holds. (β′) needs ψ(p̂) = q₃, contradicting (ii).
    (α′) gives top₃(û) = (X+k, q₂−1, ψ − 1) with ψ(X+k, q₂−1) = min(F(X+k), G(q₂−1)) ≥ q₃ + 1, contradicting (ii). ∎

**Theorem (qO-cone).** For every cone-class set, qO ≤ 2t − 1 + 2|Y|. For cone tiles (|Y| ≤ 6) this is qO ≤ 2t + 11.
(Correction 2026-10-18: this line first read "t − 1 + 2|Y|", a typo; the proof below gives 2t − 1 + 2|Y|.)
Proof.
- Let G_O be the multigraph on Max with one edge {top_a x, top_b x} per qO cell. Then qO = t − comp(G_O) + rank(G_O),
  and rank = #cycle-closing edges when the cells are added in increasing |x|.
- A cycle-closing x has both maximal tops already used. For each such top y_d, either an earlier user uses it in
  direction d (then that user lies on the d-line below x), or every earlier user uses it in another direction. In the
  second case y_d ∈ Y by S′, and x is the first user of y_d in direction d. Each y is a top in ≤ 2 directions (three
  would put y in K), so the second case happens for ≤ |Y| cells.
- All other cycle-closers are DS. Map each DS cell x to top_{a(x)}(x), where a(x) is its smaller maximal direction.
  Collisions in the same direction are excluded by the Fiber Lemma. Collisions in different directions land in Y (S′),
  at most 2 per y. So #DS ≤ t + |Y|, rank ≤ 2|Y| + t, and qO ≤ t − 1 + rank ≤ 2t − 1 + 2|Y|. ∎
(Refinement: the image of DS lies in Max ∩ (B₁ ∪ B₂ ∪ B₃), so qO ≤ t − 1 + 2|Y| + |Max ∩ B|.)

**Corollary (HT for large cone tiles).** For every cone tile:
- Lemma CHT: δ(D) ≥ m + 1 − LHS.
- LHS = 2t + 2Tri + qU + qO ≤ 2t + (t + 17) + (t + 2) + (2t + 11) = 6t + 30, by TF-cone, F-cone and qO-cone (NOTEBOOK
  night 17).
- Lemma T′ (t ≤ C) and Lemma B (C ≤ ⌊3/2 + √(6m − 15/4)⌋) then give δ(D) ≥ m − 6C − 29 ≥ m − 6√(6m) − 38.
- So **δ(D) ≥ m − O(√m)** for all cone tiles, and HT (δ ≥ 0) holds for every cone tile with **m ≥ 281** (checked: the
  last m with 6⌊3/2 + √(6m − 15/4)⌋ + 30 > m + 1 is 280).
- With Theorem C-HT (𝒞-tiles, m ≥ 131) and the complete HT scan for m ≤ 130, the only remaining range is cone tiles
  with 131 ≤ m ≤ 280. That is a finite computation (C scanner; MAXM must be raised from 255).
Checks (src/scratch/qo_fiber_check.py, qo_fiber_anneal.py, qo_fiber_exh.py):
- (A) location, (B) Fiber, (C) cross-only closers ⊆ Y, and rank/qO accounting: 0 violations on all cone tiles of
  m = 30, 40, 50, 60, 64 and on the RCON extremes.
- RCON anneals maximizing the fiber size never exceed 1.
- Exhaustive lattice-free cone sets: see EXPERIMENTS E135.
Status: PROVED on paper by the lead. Not yet independently reviewed or formalized.
**The coefficient 2 is the natural lattice-free answer (2026-10-18).** In the lattice-free cone class, qO − t is unbounded:
q = (1, 1, Q), F = (Q+3, Q+1, Q, Q−1, …, 1), G = (Q+3, Q+1, Q−1, Q−2, …, 1), h = (|G|, |G|, 2, …, 2) has t = 2Q + 2,
qO = 3Q − 3 and #DS = Q − 1 (Q = 4..12, src/scratch/ds_family.py; examples/qO_lattice_free_family.md). These sets violate the
Wall/Floor constraints, so they are not tiles. A bound qO ≤ t + O(1) therefore needs lattice input. The advisor's revised
plan (2026-10-18) needs only qO ≤ 2t + O(1) together with a proved sublinear bound on t. That bound is t ≤ C
(Lemma T′) and C ≤ 3/2 + √(6m − 15/4) (Lemma B), both proved on paper, so no sharper qO constant is pursued for now.
