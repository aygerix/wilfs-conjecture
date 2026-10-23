# LITERATURE.md — what is PROVED about Wilf's conjecture (as of 2026-10-17; e = 4 corrections 2026-10-18)

> Current handoff: [STATE.md](STATE.md). Binding user rules: [DIRECTIVES.md](DIRECTIVES.md).

Scope: bounded literature check (Phase 0). Goal: exact hypotheses of every known result, the
standard tools, the known-false strengthenings, and the precise uncovered region.

Notation (project convention, = CLAUDE.md): m multiplicity, e embedding dimension, c conductor,
g genus, n = ell = |L| = c - g, L = S ∩ [0,c), P primitives (minimal generators), t type,
PF pseudo-Frobenius set. Eliahou's constants: q = ceil(c/m) ("depth"), rho = qm - c ∈ [0,m),
I_j = [jm - rho, (j+1)m - rho), S_j = S ∩ I_j, P_j = P ∩ S_j, p_j = |P_j|, D_j = S_j \ P_j,
d_j = |D_j|. I_q = [c, c+m) ("threshold/critical interval"). X = Ap(S,m)\{0}, X_j = X ∩ S_j.
Wilf number W(S) = e·n - c.

Verification-status legend used below:
- READ = theorem statement read in the paper's own text (arXiv version unless noted; arXiv theorem
  numbers may differ from the journal version).
- SECONDARY = statement read in the text of another paper/survey that cites it; primary not opened.
- ABSTRACT = only abstract/slide text seen.
- RECOMPUTED = numerical example re-checked by us (scripts in session scratchpad, exact integer
  arithmetic; not saved to repo).
- UNVERIFIED = from memory or a search snippet only.

---------------------------------------------------------------------------------------------------

## 1. Table of proved results

| # | Result (Wilf holds / stated inequality) | Exact hypothesis | Authors, year, venue, id | Thm no. | Status |
|---|---|---|---|---|---|
| 1 | W(S) = 0 | e = 2 | Sylvester (1884) | — | SECONDARY (Delgado survey §2.3; Marashdeh L.2.1(vii)) |
| 2 | c ≤ (t+1)·n (FGH inequality) ⇒ Wilf whenever t ≤ e-1 | none (all S) | Fröberg–Gottlieb–Häggkvist, Semigroup Forum 35 (1987) 63–83 | Thm 20 | SECONDARY (Delgado Prop 3.1; Marashdeh eq.(1)); re-derived by us via identity in §2.6 |
| 3 | Wilf | e ≤ 3 (FGH: t ≤ 2 when e = 3, plus c ≥ 2n) | FGH 1987 (Th.11, Th.20); Dobbs–Matthews, Focus on Comm. Rings Research (2006) 193–202 | FGH Th.11/20; DM Cor 2.6, Th 2.11 | SECONDARY (Delgado Thm 3.2) |
| 4 | Wilf | S irreducible (symmetric or pseudo-symmetric) | Dobbs–Matthews 2006 | Prop 2.2 | SECONDARY |
| 5 | Wilf | S almost symmetric | Barucci, in "Commutative Algebra and its Applications", de Gruyter 2009, 49–60; alt. proof D'Anna–Moscariello, Math. Z. 304 (2023) Paper 35, arXiv:2208.14090 | DM Cor 4 | READ (D'Anna–Moscariello); Barucci SECONDARY |
| 6 | Wilf | S positioned (F - x + m ∈ S for all gaps x) | Branco–Faria–Rosales, Quaest. Math. 44 (2021) 679–691 | — | SECONDARY (D'Anna–Moscariello arXiv:2502.17989 §2) |
| 7 | Wilf | c ≤ 4n (equivalently c ≥ 4g/3) | Dobbs–Matthews 2006 Cor 2.7; DEF 2025 Prop 3.6 (proof: e ≥ 4 ⇒ en ≥ 4n ≥ c; e ≤ 3 by #3) | — | READ (DEF Prop 3.6) |
| 8 | Wilf | P = generalized arithmetic sequence ⟨m, hm+d, …, hm+ℓd⟩ | Sammartano, Semigroup Forum 85 (2012) 439–447 | Prop 20 | SECONDARY |
| 9 | t ≤ e-1 (hence Wilf) | e ≥ 3 and ∃ two distinct primitives p, p' with every sum of two primitives in (p+S) ∪ (p'+S) | Kunz–Waldi, J. Algebra 478 (2017) 397–409 | Cor 3.1 | SECONDARY (Delgado Prop 3.6) |
| 10 | Wilf; moreover W_0 ≥ rho | c ≤ 2m (q ≤ 2) | Kaplan, J. Pure Appl. Algebra 216 (2012) 1016–1032; short proof Eliahou JEMS 2018 | Kaplan Thm 24 or Prop 26 (sources conflict, see note A); Eliahou arXiv:1703.01761 Prop 3.13 | READ (Eliahou Prop 3.13); Kaplan SECONDARY |
| 11 | Wilf | 2g < 3m | Kaplan 2012 | Thm 24 (per Delgado–Kumar–Marion) | SECONDARY |
| 12 | Wilf | g < 2m - sqrt(2m) | Delgado–Kumar–Marion, arXiv:2501.04417 (v3, Oct 2026) | Cor 1.6 | READ |
| 13 | **W_0(S) ≥ 0, hence Wilf** | **c ≤ 3m (q ≤ 3)** | **Eliahou, JEMS 20 (2018) 2105–2129, arXiv:1703.01761** | **Thm 6.4 + Prop 6.2 ⇒ Cor 6.5** | READ |
| 14 | W_0 ≥ rho ≥ 0 | "true grading": S_i + S_j = S_{i+j} for all i + j ≤ q-1 | Eliahou JEMS 2018 | Thm 7.1 | READ |
| 15 | Wilf | q ≥ 4 and P ∩ L ⊆ [m, m + (m-rho)/(q-1)) | Eliahou JEMS 2018 | Cor 7.2 | READ |
| 16 | Wilf | gcd(L) ≥ 2 (⇔ subtree of S in the semigroup tree is infinite); includes inductive semigroups | Eliahou JEMS 2018 (via Sammartano) | Prop 7.6 | READ |
| 17 | Wilf | n = |L| ≤ 4 / ≤ 6 / ≤ 10 | DM 2006 Th 2.11 / Eliahou Prop 7.4 ("informally") / Eliahou Thm 7.5 (announced; W_0 ≥ rho except profile (1,0,1,0) where W_0 ≥ rho-1) | — | READ (Eliahou arXiv v1) |
| 18 | **W_0 ≥ 0, hence Wilf** | **n = |L| ≤ 12** (sharp for the W_0 method: |L| = 13 counterexample, see §4) | Eliahou–Marín-Aragón, Comm. Algebra 49 (2021) 2402–2422 | — | SECONDARY (Delgado Prop 3.15; DEF Thm 1.1(4)) |
| 19 | Wilf | 2e ≥ m; in particular m ≤ 8 | Sammartano 2012 | Th 18, Cor 19 | SECONDARY |
| 20 | Wilf | (2 + 1/q)·e ≥ m; also m - e ≤ 5; m ≤ 9 | Dhayni, Palest. J. Math. 7 (2018) 385–396 (thesis Angers 2017) | Th 4.12, Th 4.9, Cor 4.10 | SECONDARY |
| 21 | **Wilf** | **3e ≥ m** | **Eliahou, Electron. J. Combin. 27(2) (2020) P2.15, arXiv:1909.03699** | **Thm 1.1** | READ |
| 22 | **Wilf**; general part: e·n ≥ c - m + rho = (q-1)m | **4e ≥ m AND m \| c ("special")**; general part needs only 4e ≥ m | **Eliahou, "Divsets, numerical semigroups and Wilf's conjecture", Comm. Algebra 53 (2025) 2025–2048, HAL hal-04234167** | (DEF Thm 4.2 quotes it) | SECONDARY (DEF 2310.07742 Thm 4.2) + ABSTRACT (Eliahou IMNS 2024 abstract). Primary text not accessible (HAL bot-block) |
| 23 | Wilf | ρ' := ceil(m/e) > 3, m ≥ ρ'(3ρ'^2-ρ'-4)(3ρ'^2-ρ'-2)/(8(ρ'-2)), gcd(m, φ) = 1 where φ = product of primes dividing ρ' | Moscariello–Sammartano, Math. Z. 280 (2015) 47–53 | Th 1 | SECONDARY (Delgado Prop 3.22) |
| 24 | Wilf | e ≥ 10, second generator r > (c+m)/3, m ≤ (8/25)e^2 + e/5 - 5/4 (d ≤ 9 restriction removable via #21) | Spirito, J. Algebra Appl. 20 (2021) 2150197, arXiv:1710.09245 | Prop 4.6 | SECONDARY (Delgado Prop 3.25) |
| 25 | Wilf (computer + polyhedral) | m ≤ 18 | Bruns–García-Sánchez–O'Neill–Wilburne, IJAC 30 (2020) 861–882, arXiv:1903.04342 | Thm 4.3 | READ |
| 26 | Wilf | m ≤ 19 | Kliem–Stump, Discrete Comput. Geom. 67 (2022) 1147–1173 (face iterator applied to Kunz cone) | — | SECONDARY (DEF Thm 1.1(5), Marashdeh, Delgado–Kumar, Bacher all cite m ≤ 19) |
| 27 | Wilf | m - e ≤ 9 (BGOW Cor 4.5); m - e ≤ 12 (BGOW Cor 4.6 using 3e ≥ m); with m ≤ 19 + 3e ≥ m one gets m - e ≤ 13 | BGOW; last item our derivation: if m ≤ 19 use #26; if m ≥ 20 and e ≥ m-13 then 3e ≥ 3m-39 ≥ m (as 2m ≥ 40 > 39), use #21 | Cor 4.5, 4.6 | READ / derived |
| 28 | Wilf | S·dilation: S Wilf ⇒ D(S,a) = {0} ∪ (S\{0} + a) Wilf | Barucci–Strazzanti, Semigroup Forum 98 (2019) 251–260 | — | SECONDARY |
| 29 | Wilf | S = gluing k1·A ⊔ k2·B of two Wilf semigroups | Singh–Srinivasan, arXiv:2306.09876 | Thm 2.3 | READ |
| 30 | W ≥ 9 (although W_0 = -C(n,3)) | S = ⟨{m} ∪ A⟩_{4m}, A ⊂ [(3m+1)/2, (5m-1)/3], |A| = n-1, A a B_3-set mod m | Eliahou–Fromentin, Semigroup Forum 98 (2019) 285–298, arXiv:1710.03623 | Prop 3.3, Prop 4.1 | READ |
| 31 | W > 0 | Delgado's families S(p) = ⟨μ, γ, γ+1⟩_{pμ} (unbounded depth, negative W_0) | Delgado, Math. Z. 288 (2018) 595–627, arXiv:1608.01353 | Prop 6 | SECONDARY |
| 32 | W ≥ 0 | S h-regular, collision-free, and r ≥ ℓ (r = #right primitives, ℓ = |P∩L|) | Bacher, arXiv:2604.25051 (Apr 2026) | Thm 3.5 in v9 (Thm 15 in an earlier version) | READ; SUPERSEDED by our Theorem CF-WILF (no hypothesis on r) |
| 33 | Wilf | q > 2 and |S ∩ (m,2m)| ≥ sqrt(qm/(q-2)); in particular |S ∩ (m,2m)| ≥ sqrt(2m) | Delgado–Kumar–Marion arXiv:2501.04417 | Thm 1.5 | READ |
| 34 | m ≤ (e-1)n + 1; c ≤ q·e·n; c ≤ e·n^2; t ≤ (e-2)(n-q+1) + 2 | all S | D'Anna–Moscariello, Math. Z. 304 (2023), arXiv:2208.14090 | Thm 2, Thm 1, Thm 3 | READ |
| 35 | Exact identity W = (e-t-1)n + σ + Θ; t ≤ Σ_{p∈P\{m}} ν(p-m) ≤ e-1+Ξ ≤ e-1+Θ; g + σ ≤ e-1 + t(n-1); W ≥ Θ - Σ_{i≤d} λ(f_i) when t ≥ e | all S | Marashdeh, arXiv:2608.12531 (Aug 2026, not refereed) | Prop 3.2, Thm 1.2/4.4, Cor 4.8, Prop 5.1 | READ |
| 36 | W = 0 ⇔ e = 2 or S = T_{m,k} | e ≥ t+1 (FGH range); separately for c ≤ 2m: W = 0 ⇔ S ∈ {T_{m,1}, T_{m,2}, ⟨3,4⟩} | Marashdeh 2026 | Thm 1.3 (=6.4), Thm 1.4 (=7.3) | READ |
| 37 | W = 0 only for known families | c ≤ 3m | Sammartano, in Eliahou JEMS Remark 6.6 | Rem 6.6 | READ |
| 38 | e(c) ≤ ν·ℓ(R/c) (ring analogue of Wilf) | R 1-dim, analytically unramified, CM, local, infinite residue field, almost Gorenstein | D'Anna–Moscariello, arXiv:2502.17989 | Thm 9 | READ |
| 39 | Computer: Wilf for g ≤ 50 / 60 / 65 / 66 / **100** | genus bound | Bras-Amorós SF 76 (2008) / Fromentin–Hivert Math. Comp. 85 (2016) / Bras-Amorós–Marín Rodríguez (MDAI 2021, arXiv:2307.10682) / Bras-Amorós Math. Comp. 93 (2024) / **Delgado–Eliahou–Fromentin, J. Algebra 664 (2025) 150–163, arXiv:2310.07742** | DEF Thm 3.5 | READ (DEF) |
| 40 | Computer: Wilf for special S (m \| c) with g ≤ 120 | m \| c, g ≤ 120 | DEF 2025 | Thm 4.4 | READ |
| 41 | Computer: Wilf for max primitive ≤ 60 | max P ≤ 60 | Delgado–Kumar, arXiv:2512.23891 | Thm 3 | READ |
| 42 | Computer, CONDITIONAL: all Eliahou semigroups (W_0 < 0) with c ≤ 320 listed (17,064, all Wilf) ⇒ Wilf for c ≤ 320 (⇒ g ≤ 160) **if** Bacher's Conjecture 20 holds (Conj 2.6 in v9) | c ≤ 320 | Bacher arXiv:2604.25051 | §5 | READ (conditional) |
| 43 | Asymptotic: proportion of S of genus g that are Wilf → 1 | counting by genus | Zhai, Semigroup Forum 86 (2013) (prop. with c ≤ 3m → 1) + #13; alternatively Kaplan–Singhal, Enum. Comb. Appl. 3 (2023) Cor 7 (prop. with e ≥ m/2 → 1) + #19 | — | SECONDARY (DKM Prop 2.11, 2.12, Cor 2.16) |
| 44 | Asymptotic: proportion of S with Frobenius number F that are Wilf → 1 | counting by F | Backelin, Math. Scand. 66 (1990) Prop 2 (m ≈ F/2) + #13 | DKM Cor 2.17 | READ (in DKM) |
| 45 | Asymptotic: proportion of S with max primitive N that are Wilf → 1 | counting by max primitive | Delgado–Kumar–Marion | Thm 1.7 | READ |
| 46 | (a) Exact identity ℓ = q + Σ_{t=1}^{q−2} Θ_t + Θ_{q−1,ρ}, Θ_t = #{1≤i<m : x_i ≤ t}, Θ_{t,ρ} = same with i ≤ m−ρ−1; (b) staircase bound ℓ ≥ q + (q−2)η + η_ρ, η = |S∩(m,2m)|, η_ρ = |S∩(m,2m−ρ)|; (c) e(η+2) ≥ 2m ⇒ Wilf, so (η+1)(η+2) ≥ 2m ⇒ Wilf; (d) m | c and e(3η+4) ≥ 4m ⇒ Wilf; (e) (Q,t)-criteria from monotonicity Θ_s ≥ Θ_t only; (f) interval family ⟨m, m+1, …, m+⌈√m⌉−1⟩ | all S ((c), (d) use Eliahou for q ≤ 3) | Yang–Zhang, "Wilf's Conjecture from the First Kunz Layer", Preprints.org 202604.0551 v1 (posted 8 Apr 2026, not peer-reviewed), doi 10.20944/preprints202604.0551.v1 | Prop 2.4/5.2, Prop 3.1, Cor 4.2/4.3, Cor 4.5, Thm 5.6/5.8, Thm 6.4 | READ 2026-10-19 (user-supplied link); proofs re-derived by the lead; (a), (b) checked exhaustively genus ≤ 34 (E272) |

Note A (Kaplan numbering): Delgado's survey says Kaplan Th. 24 = "c ≤ 2m ⇒ Wilf" and Prop. 26 = equality
case for m ≥ c/2; Delgado–Kumar–Marion say Th. 24 = "2g < 3m ⇒ Wilf" and Prop. 26 = depth ≤ 2;
Marashdeh says Th. 24 = c ≤ 2m and Prop. 26 = equality claim. The primary paper was not accessible in
this session (not on alphaXiv). Treat numbering as UNVERIFIED; both statements (c ≤ 2m; 2g < 3m) are
true and the c ≤ 2m case is independently re-proved in Eliahou Prop 3.13 (READ).

Note B (2406.13580, "Wilf's question in numerical semigroups S_3 revisited"): seen only as a search
hit; content not read (UNVERIFIED). e ≤ 3 is in any case settled (#3).

---------------------------------------------------------------------------------------------------

## 2. Precise statements of the key tools

### 2.1 Eliahou's partition and level structure (JEMS 2018, §3; READ)
- I_j = [jm - rho, (j+1)m - rho), S_j = S ∩ I_j; L = S_0 ⊔ … ⊔ S_{q-1}; S_0 = {0}; S_j = I_j for j ≥ q.
- m + S_j ⊆ S_{j+1}, so 1 = |S_0| ≤ |S_1| ≤ … ≤ |S_{q-1}| (Lemma 3.4).
- Weak grading (Prop 3.5): S_1 + S_j ⊆ S_{1+j} ∪ S_{2+j}; S_i + S_j ⊆ S_{i+j-1} ∪ S_{i+j} ∪ S_{i+j+1} (i,j ≥ 2).
  If rho = 0: S_i + S_j ⊆ S_{i+j} ∪ S_{i+j+1} (graph paper Prop 2.4).
- "Deficit" bound (Prop 3.6): |(S_i+S_j) ∩ S_{i+j-1}| ≤ rho and |(S_i+S_j) ∩ S_{i+j+1}| ≤ m - rho - 1.
- P ⊆ [m, c+m); D_1 = ∅; P_q = I_q \ D; S = ⟨P∩L⟩ ∪ [c,∞) (eq. (1)). Profile = (p_1,…,p_{q-1}).

### 2.2 W_0 (Eliahou number E(S)) and Apéry formulas (READ)
- Definition 3.10: **W_0(S) = |P∩L|·|L| - q·d_q + rho**, d_q = |D ∩ [c, c+m)|.
  Equivalent (Bacher): E = k·ℓ + q·r - c with k = |L|, ℓ = |P∩L|, r = p_q.
- Identity (2): **W(S) = p_q·(|L| - q) + W_0(S)**; since |L| ≥ q, W ≥ W_0 (Prop 3.11). Re-derived by us.
- With α_i = |X_i| (i ≤ q-1), α_q = |X_q \ P| (Prop 4.5): **d_q = Σ_{i=0}^{q} α_i**, **|L| = Σ_{i=0}^{q-1} (q-i)·α_i**.
- Graph-paper form (EJC 2020, Prop 2.9 / Cor 2.10): depth δ(x) defined by x + δ(x)m ∈ [c, c+m),
  τ(X) = Σ_{x∈X} δ(x). Then **|L| = q + τ(X)**, **m = e + |X ∩ D|**, **W = e·τ(X) - |X∩D|·q + rho**.
- Summand-closure (Lemma 2.12): any summand of a decomposable Apéry element is an Apéry element
  (X is a "downset"/divset in multiplicative notation).

### 2.3 q = 2 and q = 3 proofs (READ)
- q = 2 (Prop 3.13): k = p_1, |L| = 1+k, every element of D_2 is a sum of two elements of P_1, so
  d_2 ≤ k(k+1)/2 and W_0 - rho = k(1+k) - 2d_2 ≥ 0.
- q = 3: Prop 6.2 reduces to profile (k,0): with S' = ⟨P_1⟩_c, W_0(S) ≥ W_0(S') - rho (uses Prop 3.6 to
  cap |2P_2 ∩ I_3| by rho). Lemma 6.3 (Macaulay): if |2X_1 ∩ X_2| = C(x,2) (x ≥ 1 real) then
  |3X_1 ∩ X_3| ≤ C(x+1,3), proved by building the standard graded algebra R' = K[t^{a_i}u]/J with
  dim R'_i = |iX_1 ∩ X_i| for i = 2,3 and applying Macaulay's bound h_{i+1} ≤ h_i^{⟨i⟩}.
  Thm 6.4: W_0 - rho ≥ C(k,2) + (k-x-1)C(x,2) ≥ (k-x)C(x,2) ≥ 0.
- Condensed Macaulay used in Thm 7.1 (true grading): **q·h_q ≤ h_1(1 + h_1 + … + h_{q-1})** for a
  standard graded algebra (Eliahou Thm 5.11, statement quoted in proof of Thm 7.1).
- Equality for q = 3 (Rem 6.6): only profiles (1,0) and (1,1) with p_3 = 0.

### 2.4 The 3e ≥ m proof (EJC 2020, READ)
- Reduction (Lemma 5.2): if e ≥ m/3 and |L| ≥ 3q then e|L| ≥ mq ≥ c. General principle:
  **e ≥ m/k and |L| ≥ kq ⇒ Wilf.** So only τ(X) ≤ 2q-1 remains.
- Graph G(S): vertices/edges on X with edge {x,y} (loops allowed) iff x+y ∈ X; weight map
  E(G) → X∩D, {x,y} ↦ x+y is onto (Prop 3.11), so |X∩D| ≤ |E(G)|.
- Edges are "weak" if δ(x)+δ(y) = q-1 (possible only in ≤ rho residue classes: Prop 3.20 |X_0| ≤ rho),
  "normal" if ≥ q. Thm 3.24: **τ(X) ≥ (k(q-1) + ν)/2 + (n_V - k)**, k = vertex-maximal matching
  number vm(G), ν = normality number, n_V = |V(G)|.
- With τ(X) ≤ 2q-1 and q ≥ 4 ⇒ k ≤ 4 (Prop 5.3); finite case analysis on loopy graphs with vm ≤ 4.
- Divsets (Comm. Algebra 2025, ABSTRACT/SECONDARY): for 4e ≥ m and c ∈ mN it suffices to analyse
  divsets X with vm(X) ≤ 5.

### 2.5 Kunz polyhedron / Apéry posets (BGOW 2020, READ)
- Kunz coordinates x_i = (w_i - i)/m (w_i ∈ Ap(S,m), w_i ≡ i): integer points of P_m:
  x_i ≥ 1; x_i + x_j ≥ x_{i+j} (i+j < m); x_i + x_j + 1 ≥ x_{i+j-m} (i+j > m).
  g = Σ x_i; F = max_i (m x_i + i) - m (Lemma 3.2).
- Faces of the relaxed polyhedron P'_m ↔ Apéry posets (Thm 3.10); on a face interior e and t are
  constant: **e - 1 = #minimal elements, t = #maximal elements of the Apéry poset** (Cor 3.11).
- Wilf on a face interior ⇔ for each maximal f, the system "(4.1) m x_i + i ≤ m x_f + f ∀i" ∧
  "¬(4.2) m x_f + f - m + 1 ≤ e(m x_f + f - m - Σ x_i + 1)" has no integer point. For m ≤ 18 every
  such region is even rationally infeasible. **Conjecture 4.4: every region is empty for all m ⇒ Wilf.**
- "Wilf game" (Thm 6.5): a winning sequence of moves using face equalities certifies the face.
- Face counts explode: m = 18 has 2.8·10^10 faces (1.0·10^8 "bad"); m = 19 handled by Kliem–Stump.

### 2.6 Type-based tools (READ: Marashdeh 2026; D'Anna–Moscariello 2023)
- FGH: every gap x has some f ∈ PF with f - x ∈ S (hence f - x ∈ L), so the sets f - (L ∩ [0,f])
  cover the gaps: g ≤ Σ_f λ(f) ≤ t·n, i.e. c ≤ (t+1)n.
- Exact version (Marashdeh Prop 3.2): with λ(y) = |S ∩ [0,y]|, ν(x) = #{f ∈ PF : f - x ∈ S},
  σ = Σ_f |S ∩ (f, F]| = tn - Σ_f λ(f), Θ = Σ_{gaps x} (ν(x) - 1):
  **W = (e - t - 1)·n + σ + Θ**, σ, Θ ≥ 0. (Re-derived by us: g = Σ_f λ(f) - Θ.)
  Outside FGH range Wilf ⇔ σ + Θ ≥ (t+1-e)·n; proven: Θ ≥ t + 1 - e only.
- Apéry poset Q(S) = (Ap(S,m)\{0}, ≤_S): minimal elements = P \ {m}; maximal = PF + m.
- D'Anna–Moscariello injection (Thm 2): φ(ω) = {(ω - g_i, g_i) : ω - g_i ∈ S}, ω ∈ X, are nonempty
  and pairwise disjoint subsets of L × (P\{m}) ⇒ **m - 1 ≤ (e-1)·n**. (A charging argument giving
  Wilf up to the factor q: c ≤ qm ≤ q((e-1)n + 1) ≤ qen.)
- Trivial bounds: n ≥ q (0, m, …, (q-1)m ∈ L); c ≤ qm; hence **m·n ≥ c always** (equality iff
  S = T_{m,q}); c ≥ 2n (g ≥ c/2) with equality iff symmetric.

### 2.7 Verification machinery (READ: DEF 2025)
- Tree T: children of S are S \ {a}, a a right primitive (a > F). Along descendants (S ≠ O_m):
  m constant, e_l = |P∩L| nondecreasing, e drops by ≤ 1 per generation (Prop 3.2).
- Trimming: if e_l ≥ m/3, or e ≥ m/3 + (G - g), all descendants of genus ≤ G are Wilf (Cor 3.3, 3.4);
  if |L| ≥ G/3 then descendants of genus ≤ G are Wilf (Cor 3.7). T_100(3) has 4.55·10^15 nodes.

---------------------------------------------------------------------------------------------------

## 3. 2021–2026 developments (newer than Delgado's survey, arXiv:1902.03461 / INdAM 40, 2020)

1. Eliahou–Marín-Aragón (Comm. Algebra 2021): |L| ≤ 12 ⇒ W_0 ≥ 0 ⇒ Wilf. (SECONDARY)
2. Kliem–Stump (DCG 2022): multiplicity bound pushed to **m ≤ 19**. No later extension (m ≥ 20)
   found in this search (searched alphaXiv + web, 2020–2026). (SECONDARY)
3. D'Anna–Moscariello (Math. Z. 2023): first unconditional bounds c ≤ q e n, c ≤ e n^2, m ≤ (e-1)n+1. (READ)
4. Bras-Amorós–Marín Rodríguez (2021, g ≤ 65), Bras-Amorós (Math. Comp. 2024, g ≤ 66; seeds
   algorithm); **DEF (J. Algebra 2025): g ≤ 100; special case m | c: g ≤ 120.** n_g known to g = 75
   (DEF) / 76 (Bras-Amorós arXiv:2503.14664, per Delgado–Kumar). (READ DEF)
5. **Eliahou, Divsets (Comm. Algebra 2025): 4e ≥ m and m | c ⇒ Wilf; 4e ≥ m ⇒ e n ≥ (q-1)m.**
   The general 4e ≥ m case is NOT proved (only with m | c). (SECONDARY)
6. Singh–Srinivasan (arXiv 2023): gluing preserves Wilf. (READ)
7. D'Anna–Moscariello (arXiv:2502.17989, 2025): ring version e(c) ≤ ν ℓ(R/c) for almost Gorenstein
   1-dim rings; Question 8 asks it for all analytically unramified 1-dim CM local rings. (READ)
8. Delgado–Kumar–Marion (arXiv:2501.04417, v3 Oct 2026): |S∩(m,2m)| ≥ sqrt(2m) ⇒ Wilf;
   g < 2m - sqrt(2m) ⇒ Wilf; almost all by max primitive; **Problem 1.8: is every S with max primitive
   < 2m Wilf?** (open; such S can have e < m^{1/k}). Delgado–Kumar (arXiv:2512.23891): max primitive ≤ 60. (READ)
9. Bacher (arXiv:2604.25051, Apr 2026): structure theory of Eliahou semigroups via h-Farey intervals,
   B_h-sets; 17,064 Eliahou semigroups with c ≤ 320 (complete modulo Conjecture 20); all Wilf;
   Thm 15 (collision-free, r ≥ ℓ ⇒ W ≥ 0); Eliahou semigroups exist with rho/m arbitrarily close to 1. (READ)
10. Marashdeh (arXiv:2608.12531, Aug 2026, unrefereed): exact defect identity W = (e-t-1)n + σ + Θ;
    type bound t ≤ e - 1 + Ξ ≤ e - 1 + Θ; reduction of Wilf to a c-free, n-free inequality
    (Conj 5.2: t ≥ e ⇒ Θ ≥ Σ_{i=1}^{t+1-e} λ(f_i), f_1 < … < f_t the PF numbers; verified g ≤ 35,
    slack ≥ 2; Prop 5.3: Conj 5.2 ⇒ Wilf; Remark 5.4: Conj 5.2 is pointwise at least as strong as Wilf);
    equality case W = 0 settled on the FGH range; correction of Kaplan's equality classification
    for c ≤ 2m. Computation: every S with g ≤ 31 and e ≤ t has W ≥ 2 (attained by ⟨7,8,10,19⟩,
    ⟨7,9,10,15⟩: e = t = 4, n = 4, c = 14 — RECOMPUTED). (READ)

11. **kseth/wilf-e4 (GitHub, https://github.com/kseth/wilf-e4; repo created 2026-09-18, commits 2026-09-11 … 2026-09-24,
    HEAD caa574d; K. Sethuraman; no formalization).** Gives a complete computer-assisted proof of
    **Wilf for e = 4**. The main theorem (manuscript/introduction.tex:17–22) has no extra hypotheses. The proof was generated
    with AI models ("GPT-6 Astra", then "GPT-5.6 Sol via Codex", per manuscript/construction.tex).
    - Method: lex factorization ideal T (Zhai); identity m·W₄ = A·D₀ − m(m−1); mass-transport lemma; final-window
      projection inequality m·W ≥ m·Φ(T,Z) + E(Z); continuous κ-bounds plus box thickening; a case split by the unique
      full-support corner p; 7 finite lemmas checked by two implementations each (Python + C++).
    - Audit 2026-10-18 (subagent; report in session scratchpad, kseth_wilf_e4_report.md): analytic steps traced, no error
      found; strip lemma 2.7 reproduced independently. Lemmas 2.2–2.6, 2.8 and C.3.1/C.4.1 NOT verified, and repo code NOT run.
    - Status: treated as a real result. Our independent verification is PARTIAL: analytic chain traced, Lemma 2.7
      recomputed, no error found. Lemmas 2.2–2.6, 2.8 and C.3.1/C.4.1 are not yet checked by us. The lead spot-checked the
      theorem statement, dates, AI provenance and the absence of Lean files.
    - Also archived (not in the manuscript): a fixed-e finiteness claim (m ≥ B_e ⇒ W_e > 0, astronomically large B_e). UNCHECKED.
12. **Earlier e = 4 sources MISSED by the Phase-0 search (found by the 2026-10-18 audit):**
    - **Zhai, arXiv:1111.2779 (2011): Thm 1, e·n ≥ c − (e−2)(m−1)/2. This is our Corollary H.** Lemmas 1 and 3 are our CH′
      in exact form. Thm 2: for fixed e, all but finitely many S have n/c > 1/e − ε.
    - **Hellus–Rechenauer–Waldi, arXiv:1804.06141 (2018):**
      - Prop 2.3/2.5: the lex ideal is an initial ideal and tessellates.
      - **Prop 2.6(b) = our cylinder lemma (a)** (at most one full-support minimal excluded point, and it lies in Λ).
      - Remark 2.9: Wilf for e = 4 when the ideal is the double staircase B_n (a two-face family).
    - HRW, Semigroup Forum 97 (2018) 64–74 ("Note on a theorem of Eliahou"): the family ⟨n², n²+1, n²+n, n²+n+1⟩. NOT read.
    - HRW arXiv:2107.06752 (2021): n/c ≥ 2/(e² − e + 2). HRW arXiv:2106.07246: a weaker explicit bound. Abstracts only.
    - Chomicz arXiv:2604.25653 and 2609.04000 (2026): Apéry sets / type for e = 4; no Wilf statement. Abstracts only.
    (Statements in item 12 are as reported by the audit agent, which read Zhai and HRW 2018 in full; not re-read by the lead.)

No claimed full proof or counterexample of Wilf's conjecture (all e) was found in 2021–2026 sources examined. For e = 4 there
is a complete computer-assisted proof (item 11), which we have only partly verified. Epoch AI (2026) still lists the conjecture as unsolved (§5).

13. **GitHub sweep 2026-10-18.** Searched with `gh search repos`: "wilf conjecture", "wilf's conjecture", "wilf numerical
    semigroup", "numerical semigroup(s)", "Apery set", "wilf inequality", "wilf multiplicity" (repos updated since 2025-06).
    Wilf-relevant results (README level only; CLAIMED, UNCHECKED):
    - **JC8267/wilf-multiplicity-23** (J. Collier, manuscript dated 2026-10-05, AI-assisted, arXiv submission prepared):
      computer-assisted proof of **Wilf for m ≤ 23**, extending Kliem–Stump m ≤ 19. Uses a "path certificate" and the shape
      inequality W ≥ PC ≥ R0 − D, with one exceptional shape at (d, m) = (3, 21). It says it does not rely on "an
      unrestricted e = 4 claim".
    - alhafs-hue/wilf-verification (2026-08-12): verification code for Marashdeh's type bound / reduction (item 10).
    - wytyKen/ai4math-width-bounds (2026-10-06): width bounds for four-generated semigroups and Lean formalization of
      three-variable lex ideals (Tor/Betti). Not a Wilf statement.
    - Not Wilf: benkeene/semigroup-betti (Lean, Betti numbers e = 4), stksk310/* (Lean, nearly Gorenstein e = 4),
      Flaman55/NumericalSemigroups (Huang's quadratic form), michaeliu4/bras-amoros-monotonicity, AxiomMath/fel-polynomial.
    - aygerix/wilfs-conjecture is THIS project's own remote (origin); its last pushed commit is 73b2c86 (2026-10-18 06:53Z).
    Observation: many AI-assisted numerical-semigroup projects have appeared on GitHub since Sept 2026. Re-run this sweep
    before every change of sub-target.

14. **Literature check for the general-e final-window (FW) sub-target, 2026-10-18.**
    - kseth manuscript/extensions.tex: for e > 4 it states only the moment identity mW_e = A·D_e − ((e−2)/2)m(m−1), a
      conditional mesh-transfer principle, and an obstruction to the three-horn decomposition (⟨9,19,12,20,15⟩). It does
      NOT state the final-window inequality (p:6) for general e. Neither our sharpened FWx/FWy nor the c > 3m conjecture
      appears there.
    - alphaXiv (recency-ranked: Wilf, Apéry, embedding dimension): nothing new for e ≥ 5 or on line/residue criteria
      beyond items already listed. Newest hits: 2608.12531 (item 10) and 2609.18136 / 2609.39218 (determinantal
      presentations, not Wilf).
    - GitHub: repo searches "wilf semigroup proof", "wilf conjecture lean", "numerical semigroup wilf five generators",
      "apery wilf" found nothing new. Lean code search "Wilf" found only Fine–Wilf, Stanley–Wilf and Calkin–Wilf.
    - The exact identity is Zhai's Lemma 3 (KNOWN). The FW inequality for general e is an immediate generalization of
      kseth (p:6). FWx/FWy and "FWx for c > 3m" were not found anywhere searched (novelty still not claimed).

15. **Sethuraman's foundational geometry, read 2026-10-18 by the lead (manuscript/proof.tex §2.1, 2.5, 2.7, 2.9, 2.10).**
    Facts relevant to our tile route:
    - Collision rules (= HRW Prop 2.6): a corner and its representative have disjoint supports; two distinct corners
      sharing a positive coordinate have distinct residues. Hence there is ≤ 1 full-support corner p, with
      representative 0. (Our cylinder lemma (a) and (b).)
    - (p:11) T = U ∖ (p + ℕ³), with U a finite no-full-corner ideal (= our cone class: U = Cyl ∈ 𝒞, p = q*).
    - Thm A.1.1: every finite no-full-corner ideal is a central box [0, z] plus at most three nonincreasing horns. This is
      a structure theorem for our class 𝒞, proved via a chordal compatibility graph.
    - §2.7, p = (1,1,1): each plane has ≤ 1 mixed corner, with representative h_k e_k. (Our Wall Lemma with q* = (1,1,1).)
    - **(p:19)** each ij-plane has ≤ (p_i − 1) + (p_j − 1) + p_k = |p| − 2 mixed corners. Corners with q_i < p_i are an
      antichain with distinct i-coordinates; corners ≥ (p_i, p_j) are bounded by collision with the k-axis.
      (Our Wall Lemma plus the antichain count; matches our "refined Wall count".)
    - **(p:20)** for every residue-bijective lower ideal (any 3-D lattice tile), |F_i ∩ F_j| ≤ 2 n_k, where
      F_i = {x : x + e_i ∉ T} and n_k = L_k. Proof: the h_s − 1 inner corners of each k-slice are excluded points whose
      representatives lie on the k-axis, distinct for distinct corners. So Σ_s (h_s − 1) ≤ L_k. Consequence: t ≤ 2 min_k L_k.
      **NEW TO US; a reusable tool.**
    - (p:17) for p a permutation of (2,1,1), |T| ≤ 2r² − r + 3.
    - Not used by Sethuraman: forest/elimination arguments, tripod/qO/qU graphs, LCL/PW, the height criterion HT. Our
      cone-tile route remains a different mechanism.

**Search-scope failure (2026-10-18).** The Phase-0 search covered journals, arXiv/alphaXiv and the web, but NOT GitHub. It
missed item 11 (public since 2026-09-18) and the e = 4 papers in item 12. STATE.md then called e = 4 "open in the
literature" from 2026-10-17 to 2026-10-18, and nights 13–17 were spent on it. Rule from now on: before any sub-target
becomes the focus, search GitHub + arXiv (newest first) + the reference page for that exact statement, and record the
scope and date here.

16. **Search for Wilf with e = 5, and for m | c (2026-10-18, afternoon).**
    - Scope: alphaXiv discovery, newest first ("Wilf's conjecture", "embedding dimension", "numerical semigroup"; results
      through 2026-09-30), plus web searches including site:github.com.
    - e = 5: no proof found. The newest relevant items are e = 4 papers (2604.25653, 2609.04000, kseth/wilf-e4) and the
      type bound and reduction 2608.12531.
    - github.com/michelfgaspar-spec/Wilfs13: an archival manuscript with a Lean proof of Wilf for |L| = 13 left
      elements. This extends Eliahou–Marín-Aragón (#18, |L| ≤ 12). Not read in detail; status unverified by us.
    - The-Last-Math-Competition PRs #169/#714: claimed disproofs of a "Wilf surplus/Frobenius ratio → 0" conjecture for
      e = 3. That is a different statement, not Wilf itself. Unverified.
    - m | c: no result beyond #22 (Eliahou divsets: 4e ≥ m and m | c) was found in this search. So Wilf for all S with
      m | c is treated as open.

17. **Search for e = 5, c ≤ 4m, and new 2026 results (2026-10-19, late).** Scope: two web searches ("Wilf conjecture
    numerical semigroups 2026 embedding dimension five"; "Wilf's conjecture" with conductor 4m / four times the
    multiplicity, 2026). Every hit is already listed: 2608.12531 (item 10), 2501.04417 (DKM), Yang–Zhang 202604.0551
    (#46), DEF g ≤ 100, and Eliahou divsets (m | c and 4e ≥ m). No proof for e = 5 and no theorem for c ≤ 4m was found.

---------------------------------------------------------------------------------------------------

## 4. Known-FALSE strengthenings / generalizations (and open stronger conjectures)

FALSE:
- **(F1) "W_0(S) ≥ 0 for all S" (Eliahou number nonnegative) — FALSE.** Fromentin (exhaustive, g ≤ 60):
  exactly 5 exceptions, all c = 4m, W_0 = -1: ⟨14,22,23⟩_56 (g=43), ⟨16,25,26⟩_64 (g=51),
  ⟨17,26,28⟩_68, ⟨17,27,28⟩_68 (g=55), ⟨18,28,29⟩_72 (g=59). Smallest: **⟨14,22,23⟩_56** =
  ⟨14,22,23,57,61,62,63⟩: m=14, c=56, g=43, n=13, e=7, q=4, rho=0, W_0=-1, W=35, t=8 (RECOMPUTED).
  W_0 takes every integer value infinitely often (Delgado 2018); W_0 = -C(n,3) with q = 4,
  |P∩L| = n (Eliahou–Fromentin Prop 3.3); unbounded depth (Delgado S(p)); rho/m → 1 (Bacher Prop 18).
  Second example checked: ⟨30,44,48,49⟩_118: W_0 = -2, W = 148 (RECOMPUTED).
- **(F2) "|L| ≤ N ⇒ W_0 ≥ 0" fails for N = 13** (same example, |L| = 13); 12 is optimal for the W_0 route.
- **(F3) "t ≤ e - 1" (FGH range covers everything) — FALSE**: type is unbounded for e ≥ 4 (Backelin's
  example in FGH p.75). Explicit: ⟨213,216,226,227⟩ has e = 4, t = 14 (Almirón–Moyano-Fernández
  Rem 2.3; RECOMPUTED: m=213, F=3419, t=14). FGH's claimed type formula t = 2n+3 for their family
  Γ_{s,n} = ⟨s, s+3, s+3n+1, s+3n+2⟩ is wrong (Stamate; same remark).
- **(F4) Kaplan's equality classification for c ≤ 2m (only ⟨m,…,2m-1⟩ and ⟨3,4⟩) — claimed
  incomplete by Marashdeh (Thm 7.3/Rem 7.4)**: T_{m,2} = ⟨m, 2m+1, …, 3m-1⟩ also has W = 0 and c = 2m.
  Smallest ⟨3,7,8⟩: c = 6, n = 2, e = 3, W = 0 (RECOMPUTED). Kaplan's original text not read.
- **(F5) Monotonicity "adding a left generator does not lower E"**: false, ⟨23,39,40,42⟩_77 has E = 15,
  ⟨23,39,40,42,54⟩_77 has E = 14 (Bacher; RECOMPUTED). Also "E + |L| - q ≥ 0" (would give Wilf with
  ≥ 1 right primitive) fails in general: a uniform collision-free semigroup with h = 3, a/b = 5/3,
  ℓ = 8 has E + k - q = -7 (Bacher §3.3; no explicit generators given; not recomputed).
- **(F6) Natural Wilf for semimodules, W_Δ(e(Δ)) ≥ 0 — FALSE** (Almirón–Moyano-Fernández,
  arXiv:2012.01358 §4.2). Our recomputation with Γ = ⟨6,8,35⟩, Δ = Γ ∪ (10 + Γ): e(Δ) = 2, c(Δ) = 40,
  δ(Δ) = 19, 2·19 - 40 = -2 < 0. (Their Table 2 appears to use the opposite sign convention; under
  either convention negative values occur.)
- **(F7) Pure degree/density heuristics**: W(S) ≥ ρ-type statements fail (Eliahou Thm 7.5: profile
  (1,0,1,0) has W_0 = rho - 1, e.g. ⟨5,13⟩_22: W_0 = 2, rho = 3 — RECOMPUTED).

OPEN stronger statements (true so far, each implies or refines Wilf):
- Moscariello–Sammartano Question 8 / Delgado Problem 2.5 ("Frögohämosa"): W = 0 ⇔ e = 2 or S = T_{m,k}.
  Proved for c ≤ 3m, for e ≥ t+1 (Marashdeh), computationally for m ≤ 15 (BGOW) and g ≤ 31 (Marashdeh).
- BGOW Conjecture 4.4 (all Kunz regions empty; rationally infeasible observed for m ≤ 18).
- Eliahou–Fromentin Conj 4.2: q = 4 and |P∩L| = n ⇒ W_0 ≥ -C(n,3).
- Marashdeh Conj 4.9: t ≤ e - 1 + σ (sharp, g ≤ 35); Conj 5.2 (⇒ Wilf); Conj 7.6.
- Bacher Conj 20 (pruning) and belief that no h-regular collision-free counterexample exists.
- Almirón–Moyano-Fernández "Bound conjecture" min_g W(g) ≥ -W_Γ(e) (⇒ Wilf).
- Delgado–Kumar–Marion Problem 1.8 (max primitive < 2m ⇒ Wilf?).
- Ring version (D'Anna–Moscariello Question 8); Generalized Wilf for generalized numerical semigroups
  (Cisto–DiPasquale–Failla–Flores–Peterson–Utano, Semigroup Forum 101 (2020), arXiv:1909.13120);
  Extended Wilf for C-semigroups (García-García–Marín-Aragón–Vigneron-Tenorio, Semigroup Forum 96
  (2018)); Unipotent Wilf (Can–Sakran arXiv:2306.05530). No counterexample to these found in this
  search (search was not exhaustive; status UNVERIFIED beyond the sources read).

---------------------------------------------------------------------------------------------------

## 5. Epoch AI page (https://epoch.ai/frontiermath/open-problems/numerical-semigroups), fetched 2026-10-17

- Title "A counterexample to Wilf's Conjecture"; FrontierMath: Open Problems; tags Unsolved, Number
  theory, Construction-Finite, Counterexample. No difficulty number shown.
- Statement: (F+1-G)/(F+1) ≥ 1/E, i.e. e·n ≥ c with n = c - g, c = F + 1.
- What counts: a single explicit S with e·n < c. Generators positive, gcd 1, smallest ≥ 2, exact
  arithmetic. Certificate: JSON {"generators": [...]}; if m ≤ 200000 the verifier builds S directly;
  for larger m the submission must include the Apéry set and, for each Apéry element, a predecessor
  chain through submitted generators back to 0. No other size limit stated. Example given:
  ⟨5,7,9⟩: g = 8, F = 13, c = 14, m = 5, e = 3, n = 6.
- It asks only for a counterexample (not a proof); cites no partial results.

---------------------------------------------------------------------------------------------------

## 6. Dependency map and exact gaps

Proved regions (any one suffices):
- q ≤ 3 (c ≤ 3m)  [W_0 ≥ 0 there]
- e ≥ m/3 (3e ≥ m); e ≥ m/4 only together with m | c
- m ≤ 19; m - e ≤ 13 (derived from m ≤ 19 + 3e ≥ m)
- e ≤ 3; t ≤ e - 1 (includes symmetric, pseudo-symmetric, MED); almost symmetric; positioned
- n ≤ 12; c ≤ 4n; g ≤ 100; (m | c and g ≤ 120); max P ≤ 60; g < 2m - sqrt(2m)
- |S ∩ (m,2m)| ≥ sqrt(qm/(q-2)); gcd(L) ≥ 2; true grading up to level q-1;
  P∩L ⊆ [m, m+(m-rho)/(q-1)) with q ≥ 4; Moscariello–Sammartano arithmetic condition;
  Spirito large-ratio condition; gluings/dilations of Wilf semigroups.

Hence a counterexample S must satisfy simultaneously (all READ/SECONDARY above):
  **q ≥ 4 (c > 3m), m ≥ 20, 4 ≤ e < m/3 (and e < m/4 if m | c), t ≥ e, n ≥ 13, c > 4n
  (i.e. g > 3c/4), g ≥ 101, gcd(L) = 1, |S ∩ (m,2m)| < sqrt(qm/(q-2)) ≤ sqrt(2m),
  g ≥ 2m - sqrt(2m), not almost symmetric, max primitive ≥ 61.**
  Also by Marashdeh's identity: σ + Θ < (t+1-e)·n. From n ≥ q and e·n < c ≤ qm: q ≤ n < qm/e,
  so a counterexample has fewer than m/e left elements per "level" on average (|L|/q < m/e).

Exact gaps (what a universal proof must supply):
- G1 (depth): no argument for general q ≥ 4. W_0 ≥ 0 FAILS at q = 4, so any proof for q ≥ 4 must use
  the right primitives p_q (term p_q(|L|-q)) — W_0 alone is insufficient. Lemma 5.2-type reductions
  show the hard case for e ≈ m/k is |L| < kq, i.e. very "thin" L (few left elements per level).
- G2 (e/m ratio): proven for e/m ≥ 1/3 (and ≥ 1/4 when m | c). Gap: e < m/3. The graph/divset
  method's case analysis grows with vm (≤ 4 for 1/3, ≤ 5 for 1/4 special); no uniform mechanism.
- G3 (type): FGH covers t < e; outside, only Θ ≥ t+1-e is known, short of the needed (t+1-e)·n by a
  factor ~n/2 (Marashdeh §9).
- G4 (charging): D'Anna–Moscariello's injection gives m - 1 ≤ (e-1)n (sharp form loses factor q
  relative to Wilf). A charging argument that gains the factor q (e.g. injecting X × levels into
  L × P) is exactly the missing ingredient for a direct proof.
- G5 (Kunz): fixed-m reduction is finite per m but face counts explode (m = 18: 2.8·10^10 faces);
  no structural proof of Conj 4.4 for general m.

---------------------------------------------------------------------------------------------------

## 7. Sources consulted / not accessible
Read (text): arXiv 1703.01761 (Eliahou JEMS), 1909.03699 (Eliahou EJC), 1902.03461 (Delgado survey),
1903.04342 (BGOW), 1710.03623 (Eliahou–Fromentin), 2310.07742 (DEF genus 100), 2208.14090 and
2502.17989 (D'Anna–Moscariello), 2501.04417 (DKM), 2512.23891 (Delgado–Kumar), 2604.25051 (Bacher),
2608.12531 (Marashdeh), 2012.01358 (Almirón–Moyano-Fernández), 2306.05530 (Can–Sakran),
2306.09876 (Singh–Srinivasan); Eliahou IMNS 2024 abstract (pdf); Epoch AI page.
Not accessed: Kaplan JPAA 2012 (not indexed), Eliahou Divsets full text (HAL bot-blocked),
Eliahou–Marín-Aragón 2021, Kliem–Stump 2022, Sammartano 2012, Dhayni 2018, Spirito 2021,
Moscariello–Sammartano 2015, FGH 1987, Dobbs–Matthews 2006, Zhai 2013, Kaplan–Singhal 2023,
Barucci 2009, Bras-Amorós papers, Cisto et al. 2020, García-García et al. 2018, arXiv:2406.13580.
Statements from these are SECONDARY (quoted from papers that were read) or UNVERIFIED as marked.

### Night-12 additions (2026-10-18)
- Nakamura, "Hilbert schemes of abelian group orbits", J. Algebraic Geom. 10 (2001): our tiles = Nakamura's G-graphs for
  G = ℤ/m ⊂ GL(d) diagonal with weights p; for abelian G ⊂ GL(3) the cones σ(Γ) form a fan (normalization of G-Hilb).
  SECONDARY (via web summary). Craw–Reid / Craw–Maclagan–Thomas for SL(3) structure. Not read in full.
  **Primary-source qualification, 2026-10-23:** the G-graph identification is correct, but a
  general coherence assertion must not be inferred. Craw–Maclagan–Thomas,
  [Moduli of McKay quiver representations II](https://arxiv.org/html/math/0611840v2),
  Corollary1.2/Proposition4.10 and Example4.12, characterize monomial points on the coherent
  component by initial ideals and exhibit a monomial G-cluster outside it. Their introduction
  explicitly corrects Nakamura Corollary2.4/Theorem2.11. Our positive-weight canonical Apéry
  tiles are coherent by their minimum-weight construction with monomial tie-breaking; arbitrary
  residue-complete down-sets need not be. No general cycle-excess bound or Wilf payment theorem
  follows from these results. This primary correction supersedes an overbroad reading of the
  earlier secondary summary; no new G-Hilbert bridge is claimed.
- Gomory group problem: coherent tiles = solution sets of min w·x, Σ x_a p_a ≡ g (mod m) (standard; our observation
  that all tiles d ≤ 3, m ≤ 9 are coherent is OURS, computational).
- Marashdeh 2608.12531 re-checked: Θ(S) = Σ_{gaps}(ν_S(x) − 1); Prop 5.1 W ≥ Θ − Σ_{i≤t+1−e} λ_S(f_i) for t ≥ e;
  Conj 5.2 Θ ≥ Σ λ_S(f_i) (open, checked g ≤ 35). Different mechanism from our τ-criterion.
- 2604.25653 (Apéry sets for e = 4, geometric procedure), 2609.04000 (type vs minimal presentations, e = 4): found by
  discovery search, not read; no Wilf statement in abstracts.
- τ-criterion novelty search (limited): nothing equivalent found.

### 17. Dated search, 2026-10-18 (night): column-height and residue criteria (HCR); e = 5
Scope: alphaXiv discover (newest first; keywords Wilf conjecture, numerical semigroup, Apéry set, embedding dimension);
web search for an e = 5 proof (2026); web search for GitHub or Lean repositories.
- Nothing found that combines Zhai's column identity with heights of column tops and distinctness of residues (HCR,
  HCR+, HCR++). Novelty is UNVERIFIED beyond this scope.
- No proof of Wilf for e = 5 found.
- New references:
  - M. F. Marashdeh, arXiv:2608.12531 (2026-08). Type bound t ≤ e − 1 + Ξ(S), genus bound g ≤ e − 1 + t(n − 1), and a
    reduction of Wilf to an inequality free of c and n. It also corrects Kaplan's c ≤ 2m equality list. Its survey
    credits Kliem–Stump with extending BGOW to **m ≤ 19**, so our small range is m ≤ 19.
  - arXiv:2604.25653 (2026-04): a geometric procedure for Apéry sets in e = 4. It is not a Wilf proof.
  - preprints202604.0551 (prereview, 2026): a first-Kunz-layer bound claimed to imply Wilf under an inequality. Not
    checked [later READ in full 2026-10-19: item 46].

18. **Search before making "HCR / the height functional for 4-D tiles (e = 5)" the focus, 2026-10-18 (late night).**
    - Web, extended: "Wilf conjecture numerical semigroups embedding dimension five". Found only known items:
      Sammartano 1111.1863 (2e ≥ m, m ≤ 8), Dobbs–Matthews 1610.08726 (m − e = 5), Marashdeh 2608.12531 (#35),
      Singh–Srinivasan (gluing, #29), DEF genus 100 (#39).
    - Web: Wilf with reduction number, or with Apéry elements that are sums of two generators. Nothing.
    - GitHub, `gh search repos` "wilf conjecture" and "numerical semigroup", sorted by update. New since #13:
      Flaman55/NumericalSemigroups (Huang's quadratic form, not Wilf); Aurantium-47 (shifted semigroups, endpoint
      residues); methodtrace/2026-numerical-semigroup-mass (no README).
    - Result: no e = 5 proof, no height or column criterion, and no statement that shape-only criteria fail for large e.
19. **Search before making Down-set Wilf (GW) the focus (2026-10-18, late night).**
    - Queries (web, arXiv-weighted):
      - Wilf + monomial ideal / standard monomials / complete residue system / non-minimal Apéry set;
      - Wilf + order ideal / lattice tile / fundamental domain (2025–2026);
      - Wilf + Apéry set of the largest generator.
    - Hits: only items already listed. These are:
      - the generalized numerical semigroups of Cisto et al. (1909.13120);
      - the semimodule extension (2012.01358, false, F6);
      - BGOW (1903.04342), the graph approach (1909.03699), DKM (2501.04417), Marashdeh (2608.12531), and Eliahou's
        Macaulay paper (1703.01761).
    - None states Wilf for arbitrary residue-complete down-sets (non-minimal factorization domains), nor the
      lattice-tile/dual-lattice form.
    - Background fact used: Selmer's formulas for Ap(T, t) hold for every t ∈ T, so Wilf has the same Apéry form for every
      element (standard).
    - Absence of hits is not proof of novelty. GitHub was not searched in this pass.

20. **Search before making the prefix/window family (PGW, WW_i) the focus (2026-10-19, early).**
    - Queries:
      - web: Wilf + gaps below km + elements in [c − km, c) + Apéry set of km;
      - web: Wilf + "for every k" + windows below the conductor;
      - arXiv API: abs:Wilf AND abs:semigroup, newest first (through 2609.32078, submitted 2026-09-25);
      - GitHub: repositories "wilf conjecture", "numerical semigroups", "wilf inequality", "kunz polyhedron".
    - GitHub: Delgado's bibliography repository ManuelAFDelgado/NumericalS-bib, last commit 2026-10-12, read as data.
      Its numericals.bib and preprints.bib were scanned for Wilf titles.
    - The semimodule paper 2012.01358 was read (ar5iv). Its "Wilf function" is W_Δ(k) = k·δ(Δ) − c(Δ): a family in the
      multiplier k, not in the window. It does not state WW_i.
    - No source found states WW_i, P_i, or any window/prefix interpolation between WW_1 and Wilf. WW_1 itself is
      elementary (GW-15) and may be folklore.
    - New items seen, NOT READ (metadata/abstract only):
      - Chatterjee–Narula, "A note on Wilf's Conjecture", Semigroup Forum 113 (2026) 387–396,
        doi 10.1007/s00233-026-10640-8. Springer is behind a login; no arXiv version found.
      - Gaspar, arXiv:2609.32078 (2026-09-25): forcing results plus Wilf for semigroups with 13 left elements.
        Unverified.
      - Hellus–Hübl–Rechenauer, arXiv:2604.21948: semigroups with largest generator 2g + 1.
      - Ojeda–Rosales, arXiv:2605.14775: semigroups with a fixed quotient.
      - Almirón–Moyano-Fernández, arXiv:2104.03793 (Quaest. Math. 46 (2023)): Eliahou number, Wilf function,
        concentration.
    - Absence of hits is not proof of novelty.
21. **Search for the PF-count criterion GW-18 (2026-10-19, night).** Query: Wilf + number of pseudo-Frobenius numbers
    above the multiplicity / above km + embedding dimension (web, extended).
    - Found: e > t ⇒ Wilf (FGH 1987, as quoted in BGOW 1903.04342); Sammartano 2e ≥ m; Dhayni (2 + 1/q)e ≥ m;
      Marashdeh 2608.12531 (smallest t + 1 − e PF numbers, Prop 5.1).
    - Not found: any criterion that counts only PF numbers ≥ 2m (GW-18) or ≥ m.
    - Absence of hits is not proof of novelty.
22. **Search before making "Wilf for c ≤ 4m (K = 4 band counting)" the focus (2026-10-18).**
    - Queries:
      - web, extended: Wilf + conductor c ≤ 4m / depth 4 / q = 4;
      - web: GitHub + Lean + "4m";
      - `gh search repos` "wilf semigroup" and "numerical semigroups wilf" (no public hits).
    - Found:
      - Eliahou JEMS 2018 (c ≤ 3m, via Macaulay; W_0 counterexamples sit at c = 4m);
      - Eliahou divsets (m | c, 4e ≥ m);
      - DEF g ≤ 100 (computer);
      - preprints202604.0551 (first Kunz layer, item 19);
      - Marashdeh 2608.12531 (item 10).
    - Not found: any proof of Wilf for all S with c ≤ 4m (3m < c ≤ 4m open as far as searched).
    - Absence of hits is not proof of novelty.

## Search 2026-10-19 (scope: GW-25, Wilf for 3m < c ≤ 4m with generators in [(c−m)/2, c−2m))
- Queries: web (arXiv/preprints) "Wilf conjecture conductor 4m Apéry", "Wilf second generator large Apéry length",
  2026 items. Found: Spirito 1710.09245 (#24; needs n_1 > (c+m)/3, e ≥ 10, m ≤ (8/25)e² + …); Eliahou–Fromentin
  1710.03623 (#30; the c = 4m B₃ near-miss family, W ≥ 9 proved for it); Eliahou divsets (#22; m | c, 4e ≥ m);
  preprints.org 202604.0551 (abstract only: m | c and e(3η+4) ≥ 4m with η = #S∩(m,2m); not read) [later READ in full
  2026-10-19: item 46].
- None states the GW-25 class result.
  - CORRECTION (same day): GW-25 has r = 0, so it does not contain the Eliahou–Fromentin near-misses (#30), which
    need r > 0.
  - Bacher (v9, Oct 2026) numbering: the class result is Thm 3.5 (h-regular, collision-free, r ≥ ℓ ⇒ W ≥ 0). The
    complementary case is Conj 2.6 (r < ℓ ⇒ E ≥ 0), which is open.
  - Bacher's Table 1 has a "not h-regular" row, so Eliahou semigroups are not all h-regular.
  - Bacher v9 reports Wilf proved for c ≤ 200 (a search with no conjectures) and a list conjecturally complete to
    c ≤ 400 (104,569 Eliahou semigroups). Spirito's hypothesis n_1 > (c+m)/3 implies Ap = A_{≤2} (GW-25a with k = 2).
  For c ≤ 5m, the GW-25 hypothesis n_1 ≥ (c−m)/2 is the weaker one, but GW-25 also assumes pure A and 3m < c ≤ 4m.
  GW-25 covers e of every size, whereas Spirito's needs m ≤ (8/25)e² + …, which fails here since m can be ≈ e³/6.
- The arc lemma GW-25a is elementary and may be folklore. No priority is claimed for it.


## Search 2026-10-19 (scope: Wilf for 3m < c ≤ 4m, before making the low-unit case the focus)
- Web search (extended) for Wilf with c ≤ 4m / conductor at most 4m / depth 4, 2025–2026. Found only:
  - c ≤ 3m (Eliahou; re-proved in DKM 2501.04417);
  - m | c with 4e ≥ m (divsets);
  - genus ≤ 100/120 verifications;
  - Spirito (large second generator).
- No proof of Wilf for c ≤ 4m was found. Our GW-24/25/26/26b are therefore beyond the known frontier, subject to
  the usual caveat that the absence of a hit is not proof of absence.

## Search 2026-10-19 (scope: Wilf for quadratic Apéry sets, Ap ⊆ {0} ∪ P ∪ (P+P), before making it the focus)
- Web (extended): Wilf + Apéry set + "sum of at most two generators"; Wilf + Apéry poset depth/height two, 2025–2026;
  Wilf + "reduction number"; Wilf + Apéry + "sum of two" minimal generators 2026.
- GitHub: `gh search repos "wilf conjecture"` sorted by update (only our own repository).
- Hits: only known items. These are Spirito 1710.09245 (#24: needs e ≥ 10 and m ≤ (8/25)e² + e/5 − 5/4 under
  n_1 > (c+m)/3), DKM 2501.04417 (depth ≤ 3), BGOW 1903.04342, Marashdeh 2608.12531, Dhayni 1610.08726, Sammartano
  1111.1863, preprints202604.0551. New (not read): arXiv 2605.14775 (fixed quotient; says Wilf is known for depth ≤ 3).
- No statement of Wilf for every S with quadratic Apéry set, or for n_1 > (c+m)/3 without Spirito's conditions.
  GW-27 is therefore beyond what we found, with the usual caveat that a missing hit is not proof of absence.


## Search 2026-10-19 (scope: Wilf for height-3 Apéry sets, Ap ⊆ {0} ∪ P ∪ 2P ∪ 3P, e.g. 4n_1 > c + m)
- Web (extended): Wilf + Apéry elements as sums of at most three generators; Wilf + second generator > (c+m)/4.
- Our own record: GW-25 and GW-26 are height-3 statements, but only for 3m < c ≤ 4m. Flat-MaxCL covers height ≤ 2.
  The NOTEBOOK "Height-3 natural scheme" of 2026-10-17 has no proof.
- Hits: only Spirito 1710.09245 (n_1 > (c+m)/3), Eliahou 3e ≥ m, Sammartano 2e ≥ m, and the c ≤ 3m results.
- No statement for height 3 at every depth was found.

### Search 2026-10-19 (evening): additive combinatorics / Kunz-layer growth and Wilf
- Queries (web, extended): "Wilf conjecture numerical semigroup prime multiplicity Cauchy-Davenport Kneser sumset";
  "numerical semigroup Kneser theorem Apéry set sumset lower bound"; "arXiv 2026 Wilf's conjecture numerical
  semigroups". GitHub repository search: "wilf conjecture", "wilf numerical semigroup", "wilf-e4", "wilf semigroup
  lean", "numerical semigroups wilf conjecture proof"; code search "wilf semigroup conductor".
- Found, closest:
  - Y. Yang, Y. Zhang, "Wilf's Conjecture from the First Kunz Layer", Preprints.org 202604.0551 (April 2026, not
    peer reviewed; abstract only — full text returned 403). Claimed: |L| ≥ q + (q−2)η + ηρ with η = |S ∩ (m,2m)|,
    c = qm − ρ, hence Wilf when e(η+2) ≥ 2m (and e(3η+4) ≥ 4m when m | c). Linear in q; no sumset-growth theorem.
  - Delgado–Kumar–Marion, arXiv:2501.04417 (Wilf when |S ∩ (m,2m)| is large; counting by maximum primitive);
    Delgado–Kumar, arXiv:2512.23891 (algorithms, no counterexample with maximum primitive ≤ 60).
  - GitHub: only kseth/wilf-e4 (known) and our own repo.
- No source applies Cauchy–Davenport / Kneser growth of the Kunz layers B_j = {r : κ_r ≤ j} ⊂ ℤ/m to Wilf.
- Follow-up (same day): "Wilf's conjecture "prime multiplicity" numerical semigroup" (extended web search). No result
  on Wilf for prime multiplicity. Kaplan (counting by genus) uses prime m only inside his small-genus counting
  argument. Other hits are the known e ≥ m/2 (Sammartano), e ≥ m/3 (Eliahou, EJC 2020), m/4 when m | c
  (Comm. Algebra 2024), Spirito (large second generator), m − e ≤ 5 (PJM 2018), genus < 2m − √(2m) (arXiv:2501.04417).

### Search 2026-10-19 (night): packing of pair-distinct sets with few triple-sum coincidences (for JOINT-SP / P5d)
Question: if n integers in an interval of s integers have distinct pair sums (loops included) and triple-collision
excess ε, how small can s be? Our LSP/SP gives 3s − 2 ≥ n(C(n,2)+1) − λ_n ε, with λ_n ≈ 3n/2. Searched the web
(B_3 sets, B_h[g] sets, signed sums a+b−c, Sidon sets with few 3-fold coincidences, additive energy T_3).
- B_3 sets (no coincidences): f(N) ≤ ((7/2)^{1/3} + o(1)) N^{1/3}, Green, Acta Arith. 100 (2001) 365–390, as cited
  on erdosproblems.com thread 241; Bose–Chowla gives a matching N^{1/3} order. Our SP is the classical signed-sum
  bound n³ ≲ 6s, weaker than Green's constant.
- B_3[g] sets (≤ g representations): |A| ≤ (14.3 g N)^{1/3} (Timmons 2016), improving (16 g N)^{1/3} (Cilleruelo,
  Ruzsa, Trujillo). General B_h[g] bounds: Johnston, Tait, Timmons.
- Erazo, López, Trujillo, Rev. Colombiana Mat. 2019: counts triples with a+b−c out of range (related to signed sums).
- NOT FOUND: a bound for Sidon sets in terms of the TOTAL excess ε with a defect cost independent of n, or a
  bound on heavy triple fibers (many disjoint triples with one common sum) in Sidon sets. Per-sum bounds (B_3[g]) do
  not give it, since they degrade as g^{1/3} instead of linearly in ε. Searching found no such result, which does
  not show that none exists.

### Search 2026-10-19 (night): Apéry-factorization-length / reduction-number classes; newest arXiv
- Queries:
  - "Wilf conjecture numerical semigroup Apéry set elements factorization length at most two";
  - "Wilf ... reduction number Apéry elements order";
  - "arXiv 2026 Wilf's conjecture numerical semigroups new result".
- No source states Wilf for "every Apéry element has a factorization of length ≤ 2" (our Lean-checked Flat-MaxCL
  corollary), for reduction number ≤ 2, or for the no-wrap class. The nearest results are:
  - Apéry half-factoriality for e = 2 or e ≥ m − 1 (elasticity paper);
  - e ≥ m/3 (Eliahou), which already covers much of the class.
  Absence of a hit is not proof of novelty.
- New since the last search: Hellus–Hübl–Rechenauer, "Numerical Semigroups with a_e = 2g+1", arXiv:2604.21948
  (22 Apr 2026). Per the abstract, Wilf holds for semigroups with a generator equal to 2g+1 and for some semigroups
  derived from them. Only the abstract was read; exact hypotheses are UNREAD.
- Marashdeh arXiv:2608.12531 and Delgado–Kumar–Marion arXiv:2501.04417 v3 were already READ (rows 12, 33, 35, 36).
- e = 5 status check (2026-10-19 night): a web search ("Wilf conjecture embedding dimension 5") and GitHub
  (`gh search repos`) found no e = 5 proof. kseth/wilf-e4 (last push 2026-10-05) is e = 4 only. Nearest results:
  Sammartano 2ν ≥ m and m ≤ 8; Eliahou e ≥ m/3; Dhayni m − ν = 5 and m = 9 (a different invariant). So e = 5 is OPEN
  as of this search.
- **Search 2026-10-19 (late night), before making WRAP-MAX / H1′ a sub-target.** GitHub (`gh search repos`, updated
  after 2026-10-12: "wilf conjecture", "numerical semigroup", "apery set"): only our repo, Flaman55/NumericalSemigroups
  and Aurantium-47/numerical-semigroup-endpoint-residues (shifted-semigroup endpoint residues; not Wilf). alphaXiv
  (recency): no new Wilf result. Newest relevant items are 2608.12531 (item 10), the e = 4 papers, and 2610.06426
  (reflexive ideals; not Wilf). No statement resembling NO-WRAP, WRAP-MAX or H1′ was found.

### Search 2026-10-19 (latest): generators < 2m (Problem 1.8), Kneser/Cauchy–Davenport and Wilf, shifted families
- Delgado, Kumar, Marion, "On counting numerical semigroups by maximum primitive and Wilf's conjecture",
  arXiv 2501.04417 (v1 Jan 2025; v3 1 Oct 2026).
  - Thm 1.5: depth d > 2 and |S∩(m,2m)| ≥ √(dm/(d−2)) ⇒ Wilf. The proof is the disjointness count ℓ ≥ (d−2)·k, with
    Eliahou for d ≤ 3.
  - Cor 1.6: g < 2m − √(2m) ⇒ Wilf.
  - Thm 1.7: asymptotic, almost all S by maximum primitive.
  - **Problem 1.8 (open): if the maximum primitive is < 2m, does S satisfy Wilf?**
  - Remark 5.2: S ∩ (m, 2m) consists of primitives.
- No Wilf result using Kneser's theorem or Cauchy–Davenport was found. Web searches: "Wilf conjecture Kneser theorem",
  "Cauchy–Davenport numerical semigroup Wilf", "generators in short interval Wilf".
- Nearby results with different hypotheses:
  - Sammartano (arXiv 1111.1863): 2e ≥ m; m ≤ 8; generalized arithmetic sequences.
  - Dhayni (arXiv 1610.08726): w_{m−1} ≥ w_1 + w_α and (2 + (α−3)/q)ν ≥ m.
  - Spirito (arXiv 1710.09245): large second generator.
  - Stamate–Strazzanti (arXiv 2601.19629, 2026): PF sets of shifted families ⟨n, n+r_1, …⟩; not Wilf.
  - BGOW (arXiv 1903.04342): m ≤ 18.
- [SUPERSEDED IN PART 2026-10-19, see the correction below] Conclusion: LAYER-KNESER (PROOFS) appears new. It strictly contains DKM Thm 1.5. It was checked against the exact
  hypotheses above, but not against every paper in the field. Before any public claim, ask Delgado or Eliahou.


### Correction 2026-10-19 (latest++): Yang–Zhang, Preprints.org 202604.0551 (item 46; link supplied by the user)
- This search missed it: it is on Preprints.org (MDPI), not arXiv. Posted 8 April 2026, before our LAYER-KNESER work.
- Yang–Zhang Prop 3.1 (ℓ ≥ q + (q−2)η + η_ρ) CONTAINS LK part (a) (ℓ ≥ D + (D−2)k, D = q, k = η) and is stronger by η_ρ.
  Their Prop 2.4/5.2 is the exact band formula we use (Θ_t = m − 1 − g_t). So **LK (a) is NOT new**, and the
  claim "LK strictly contains DKM Thm 1.5" belongs to Yang–Zhang, not to us.
- Yang–Zhang use only the monotonicity Θ_{t+1} ≥ Θ_t. They have no growth estimate for Θ_t, no Kneser or Cauchy–Davenport.
  **LK (b), the growth Θ_{t+2} ≥ Θ_t + δ, is still not in the literature found so far**, nor is its combination with
  their staircase (PROOFS "LK+YZ"). Their concluding remark asks for a finer analysis of the layer interactions.
- Verification (ours): every proof in §§2–5 re-derived by hand; (a), (b) exhaustively over genus ≤ 34 (E272).
- Coverage (E272, 996 structured S with q ≥ 3): LK+YZ covers 545 and YZ's first-layer criteria (Cor 3.3/4.2/4.5) about 285.
  129 S are covered by LK+YZ and by none of: YZ 3.3/4.2/4.5, DKM 1.5, Cor 1.6, LIT, Kaplan, type ≤ e−1, symmetric.

**Search 2026-10-19 (latest), before recording codex P10's e = 5 classes and the CHAIN-WILF repair.** Queries: "Wilf
conjecture numerical semigroups embedding dimension five 2025 2026 arXiv"; "Wilf conjecture sum of generators conductor
Apéry factorization support". Hits were only known items: Sammartano 1111.1863 (2e ≥ m, m ≤ 8), Dhayni 1610.08726
(m − e = 5), Spirito 1710.09245 (e ≥ 10, large second generator), Eliahou 1703.01761, near-misses 1710.03623, and Cisto–Utano
2024 (a family).
- Correction to item 12: Hellus–Rechenauer–Waldi, "Note on a theorem of Eliahou", Semigroup Forum 97 (2018) 64–74. Per the
  abstract (Regensburg repository), it constructs one class of embedding dimension FIVE with arbitrarily high type
  satisfying Wilf. The full text was not available. This is a constructed family, not a hypothesis class like B2/B4.
- No result of the form "Σ of three (or four) generators ≥ c + m ⇒ Wilf" was found.

### Search 2026-10-19 (latest): Apéry height ≤ 3 / large second generator (before height-3 MaxCL becomes line 1)
- Queries: web (Wilf + Apéry set + sums of at most three generators / reduction number / depth / height; second
  generator > (c+m)/4 or (c+m)/3).
- Hits, all known except two:
  - Spirito 1710.09245 (#24): n_1 > (c+m)/3 with extra conditions.
  - Eliahou EJC 2020 (3e ≥ m); Eliahou IMNS 2024 slides (m | c, 4e ≥ m); Dhayni 1610.08726; Sammartano 1111.1863.
  - NEW: Llena–Rosales, "Second-level numerical semigroups", Mathematics 13(4) (2025) 593 (abstract only).
    - S is second-level if x + y + z − m ∈ S for all nonzero x, y, z ∈ S. This is equivalent to every Apéry element
      having ALL its factorizations of length ≤ 2 (max order ≤ 2).
    - The abstract claims Wilf for the minimal second-level semigroups they construct; whether it claims all
      second-level S was not verified (abstract only).
    - Our Flat-MaxCL corollary (SOME factorization of length ≤ 2) contains every second-level S.
  - NEW: Marashdeh, arXiv 2608.12531 (Aug 2026). Type bound t ≤ e − 1 + Ξ(S), and the reduction
    g ≤ e − 1 + t(n − 1) of Wilf (abstract only). Not about Apéry height.
- No statement found of Wilf for Apéry height ≤ 3, or for n_1 > (c+m)/4. Absence of a hit is not proof of novelty.
- Addendum (same date): Spirito's arXiv abstract was checked directly. The hypothesis is the strict
  a_2 > (c(S)+μ(S))/3, and Wilf is concluded "when the multiplicity is bounded by a quadratic function of the embedding
  dimension". Our Lean theorem `wilf_of_conductor_add_mult_le_three_mul` (3n_1 ≥ c + m ⇒ Wilf) removes that bound.

### Search 2026-10-19 (latest), before recording DEPTH4-EH (Wilf for c ≤ 3m + e)
- Queries: web, "Wilf conjecture conductor 3m embedding dimension c ≤ 3m + e / depth four / c ≤ 4m" (standard and
  extended), "Wilf's conjecture depth four conductor at most four times multiplicity 2025 2026".
- Hits are known: Eliahou JEMS (q ≤ 3), Sammartano 1111.1863, Dhayni 1610.08726, Spirito 1710.09245, Delgado
  1910.12377 (trimming the tree; cites 3e ≥ m), Eliahou–Fromentin 2006.01480 (≤ 12 left elements), Marashdeh 2608.12531,
  Yang–Zhang Preprints 202604.0551.
- Tôledo, UFG master's thesis (2022), "A conjectura de Wilf do ponto de vista da profundidade…": exposition of
  Eliahou's q ≤ 3. Abstract and front matter read; no depth-four theorem.
- No statement of Wilf for c ≤ 3m + e, or of any depth-four band, was found. Absence of a hit is not proof of novelty.

### Search 2026-10-20 (afternoon), before making the P18 depth-four core regime / all-A case a sub-target
- Web: "Wilf conjecture numerical semigroups conductor at most 4m depth four generators less than 2m"; "arXiv 2026 Wilf
  conjecture maximal primitive 2m Delgado Kumar Marion problem". Hits: DKM 2501.04417 (Problem 1.8 still stated open),
  Delgado–Kumar 2512.23891 (max primitive ≤ 60), Yang–Zhang Preprints 202604.0551 (item 46), near-misses 1710.03623,
  Dhayni 1610.08726, divsets HAL-04234167. All already listed.
- Nothing addresses depth four (3m < c ≤ 4m) for generators below 2m, the window B ⊂ [h/2, h), or untruncated-Macaulay
  payment of carried pairs. Theorem CORE4 appears new relative to these. Not checked against every paper in the field.


## 2026-10-20 — search for Conjecture DEAD (W ≥ Λ − O; collisions of factorizations in Ap)
- Three standard web searches: Wilf + factorizations/"unique expression"/Apéry; Wilf + Jordan type/nilpotent
  multiplication; Wilf + staircase/Kunz nilsemigroup. Hits were only the known background: Sammartano (2ν ≥ m),
  Eliahou (c ≤ 3m, 3e ≥ m), Bruns–García-Sánchez–O'Neill–Wilburne (m ≤ 18 via Kunz faces, Apéry posets), Spirito
  (large second generator), Dhayni, and the Epoch problem page.
- NO statement bounding W from below by a factorization/collision count was found. Status of DEAD: ours, unverified
  novelty (a search, not a proof of novelty). Closest known structure: Brower–McDonough–O'Neill (staircase =
  Apéry set of unique expression = Kunz-fan chambers; LIT_CL.md §2.1). There DEAD reduces to Wilf.

### Found by the user 2026-10-20: conjectures.io, Lean proof of Wilf for c ≤ 4m (NOT yet verified by us)
- URL: https://conjectures.io/results/fd12daa7-2b0e-460f-a805-f9ba6d9fede4 (solution page …/solution; source download
  …/solution/download, Main.lean, ≈1.1 MB, 22,763 lines). Problem page /problems/math30catalog-source23, citing arXiv
  1703.01761.
- Claim: "Every proper numerical semigroup with conductor c at most four times its multiplicity satisfies c ≤ e·L."
  Solver "Elias".
  - Status shown: Lean verification Passed (kernel only; Nanoda not run). Review Approved. Verified 10 Oct, certified
    14 Oct 2026.
  - Policy shown: no imports, no axiom declarations, no sorry, no native_decide. Axioms: propext, Quot.sound,
    Classical.choice.
- Review text: "the universal depth-four case is closed by the general core/window/strip argument".
- Discrepancy to resolve:
  - The displayed file header says "Incomplete challenge 23" and "Each `sorry` below is an open blueprint node".
  - The verifier reports no sorry.
  - Only the first 500 lines are viewable: Kaplan c ≤ 2m and Apéry infrastructure.
- If confirmed, this settles depth four for ALL S, superseding our P18 depth-four program (A0, CARRY-ID, SIG). Per
  [status = verification], it counts only after our own audit: statement and definitions match, kernel check on fejer,
  no sorry/axioms.
- Why our searches missed it: we searched arXiv, the web, GitHub and Preprints.org. We never queried proof/bounty
  platforms. Memory rule updated.

### conjectures.io c ≤ 4m proof: our audit (2026-10-20, lead)
**Statement checked.** For every numerical semigroup S with c(S) ≤ 4·m(S): c ≤ e·ℓ, with c = least c such that
[c, ∞) ⊆ S, m = least positive element, e = number of minimal generators, ℓ = |S ∩ [0, c)|.

**How we checked it.**
- Source: Main.lean, 22,763 lines, SHA-256 b1bdde55…986447 (the same as the page). Task bundle: manifest target
  `Math30Catalog.source23`, formal-conjectures commit 4b69a7dc, toolchain v4.35.0-rc2, permitted axioms propext,
  Quot.sound, Classical.choice.
- The statement file `FormalConjectures/ResearchTargets/Math30.lean` at 4b69a7dc is not public. So we did not rely
  on it. We wrote our own definitions with the API names the proof uses, and proved every API lemma ourselves:
  - `conductor` via Nat.find;
  - `multiplicity`;
  - `IsPrimitive x := x ∈ S ∧ 0 < x ∧ ∀ a b ∈ S, x = a + b → a = 0 ∨ b = 0`;
  - `primitiveElements`, `leftElements`;
  - `SatisfiesWilf := conductor ≤ embeddingDimension * leftCount`;
  - `closure_primitives`, `primitive_lt`, and a test fixture `{0} ∪ [m, ∞)`.
  We then replaced `fcTypeOfName% "Math30Catalog.source23"` with our own statement and compiled the unmodified proof
  body under Lean v4.35.0-rc2 + Mathlib tag v4.35.0-rc2 (fejer ~/wilf/ext/cc35, files ConjCheckPreamble.lean and
  ConjCheck.lean).
- Static scan: no `sorry`, `axiom`, `set_option`, `native_decide`, `unsafe`, `macro`/`elab`/`syntax`, or `#eval`.
  There are two `decide +kernel` certificates (qpa_*). The header line "Each `sorry` below is an open blueprint node"
  is stale.
- A first build on our v4.33.1/Mathlib 0df444a project failed on renamed lemmas (`dite_eq_left`, `ite_eq_left`,
  `Finset.sum_le_sum_of_injOn`) and one heartbeat timeout. Toolchain drift, not a gap.
- **Result:** **PASS (2026-10-20).** 0 errors, exit status 0, 6 min 45 s, 10.8 GB. `#print axioms wilf_conductor_le_four_mul_multiplicity` (our elementary restatement, ∀ S, c ≤ 4m → c ≤ |primitiveElements|·|leftElements|) = [propext, Classical.choice, Quot.sound]. The same holds for `an_anchor_bound` and `t11_reduce_to_pruned`.
  - Checked file: SHA-256 bdf6937b…; our preamble: ac011f0d…. Both are reproducible with `lean/external/conjio_d4/assemble.py`.
  - The exact toolchain still needed one fix. Three Mathlib notations glue to identifiers in the proof text and change its tokenization when imported: `≤m` and `≤r` (Matroid minors), `→g` (SimpleGraph.Maps). For example `x≤m3_value` lexes as `≤m` + `3_value`. The original build imported only a subset of Mathlib. We dropped the 364 modules that import those files and did not edit the proof text.
  - **Verdict: Wilf's conjecture holds for every numerical semigroup with c ≤ 4m.** It is kernel-checked under our own definitions with standard axioms. We read the architecture (below); we did not referee every lemma by hand. The kernel check is the guarantee.

**Proof architecture** (dispatch in `target`; names are Lean declarations):
1. q ≤ 2: Kaplan. q = 3: Eliahou, formalized through a truncated Macaulay bound for the 3-fold sumset (`W23_M3`,
   multicomplex shadows and compression).
2. q = 4, preparation:
   - Write c = 4m − ρ, n = number of left primitives, d = |D ∩ [c, c+m)|, p = m − d. Then W = W₀ + p(ℓ − 4), with
     W₀ = nℓ − 4d + ρ (the Eliahou number).
   - Pruning (`t11_*`). A late left primitive g has g ≥ c − m and g + a ≥ c + m for every left primitive a ≠ m. It can
     be deleted: c, m unchanged, ℓ drops by 1, e does not rise. Wilf of the child implies Wilf with slack e. So
     only late-pruned S remain.
   - About fifteen quantitative slices close the regimes where W₀ ≥ 0 can be forced by counting. Each ends in a
     polynomial certificate (q4_low/high/lowhalf, gen_*, core_band24, core_quarter).
3. Residual = Eliahou-type S (W₀ < 0 possible), reduced to a **generalized core** T° = ⟨A⟩ ∪ [c, ∞), where A = P(S) ∩
   [m, 2m).
   - Theorem A (`cr_thmA`): if W₀(S) < 0 and S has a level-2 ordinary or level-3 primitive, then
     23(d_S − d_T) ≤ 13(W₀(S) − W₀(T°)).
   - Since d + p = m on both sides, 13W₀ + 23p does not decrease from T° to S. So CORE°: 13W₀(T°) + 23p(T°) ≥ 0
     implies Wilf for S (ℓ ≥ 6).
4. Cores, in the window model (m, ρ, B): T = ⟨m, m + b : b ∈ B⟩ ∪ [4m − ρ, ∞), window N = m − ρ = c − 3m. Positions are
   u = x + ρ mod m, with levels.
   - Y_t = unwrapped ≤ t-sums of window offsets.
   - Ẑ = carried pairs (once-wrapped 2-sums not in Y₃).
   - Q = carried triples (once-wrapped 3-sums new at level 4), split as Q_j by w(q) = the number of wrapped parent
     pairs of the canonical cubic β_q.
   - **ID2** (exact, every strip-free model): W₀ = ρ + |Ẑ| + Σ − |Q₃|, with
     Σ = |Q₁| + A + 2|Q₀| + 6(P_w − |Ẑ|) + 6(P_u − h₂) + 4|Ẑ ∩ Y₄| + 2·d₃'' + d₄ ≥ 0, where A = weight of unused
     incidences (z, i), z ∈ Ẑ. The only negative term is Q₃ (carried triples all of whose parent pairs are wrapped).
   - Lemma 6_ρ: Σ_q w(q) + A = (K + 2)|Ẑ|.
   - **Anchor.** "Highs" are offsets b with 2b ≥ N. The anchor y is a high minimizing rank(y) + |D(y)|, where
     D(y) = {v : v + y < N} (BAL-LEFT / BAL-RIGHT / COL-RANK).
   - **Shell.** With I = [0, N − y) and J = [y, m), translation by y injects Y₃ ∩ I into J. So
     |Q₃| + |F| ≤ |R| + |P| + ρ + |Ẑ| + |N40| + |Q₀| + |Q₁ ∩ I| + #holes, where P = Q₂ ∩ I, R = Q₃ ∩ [0, y),
     F = J ∖ (Q₃ ∪ (y + Y₃ ∩ I)).
   - **PAYMENT** (two injections built from the anchor: a lower-cubic map on R, a prefix-edge map on P):
     |P| + |R| ≤ A + |F| + |Q₁ ∖ I|.
   - Adding these, with #holes = p and |N40| ≤ h₄, gives the **anchor theorem** (`an_anchor_bound`, `st_A29A` with
     strips): for every model with a high window offset, with no residual hypothesis and no conductor condition,
     W₀ + p ≥ coll + 2d₃'' + d₄ − h₄.
   - Under the residual hypotheses, d₄ ≥ h₄ (`wm_quartic`), so CORE₁: W₀ + p ≥ 0.
   - Strip offsets (b ≥ N) are handled by Theorem A29-A (`st_*`).

**What this settles, and what it does not.**
- Settled (kernel-checked by us): Wilf for every S with c ≤ 4m.
- The architecture is depth-four specific:
  - W₀ uses q = 4;
  - the model has levels ≤ 4 and only once-wrapped sums. At depth ≥ 5, twice-wrapped triples and carried
    quadruples enter;
  - λ = 23/13 comes from a depth-four fibre bound (CL_{23/13});
  - the slices are depth-four certificates.
- Depth-free ingredients:
  - the split W = W₀ + p(ℓ − q) (Eliahou, known);
  - pruning of late primitives;
  - the anchor theorem read as a statement about the first four layers. With ρ = 0, every P18 set
    S = ⟨m, m + B⟩, B ⊂ [1, m), with some 2b ≥ m, at any depth, satisfies e·|S ∩ [0, 4m)| − 5N₄ + m + h₄ ≥ 0, where
    N₄ = |S ∩ [4m, 5m)|. Equivalently Q₄ ≥ −D₅ − h₄, with Q₄ = e·Σ_{k<4}N_k − 4N₄. Our check E336: 0 failures on
    17,864 sets, 12,722 of depth ≥ 5. Plain LAYER(4) (Q₄ ≥ 0) fails 49 times on the same sample.
- The core reduction is not a general monotonicity. W(S) ≥ W(⟨A⟩ ∪ [c, ∞)) fails at every depth 3…15, already at
  genus ≤ 16 (E336). It needs W₀(S) < 0 and the residual hypotheses.

**Novelty of our results against this proof:**
- It contains no pseudo-Frobenius argument, so the τ-criterion is independent of it.
- It has no statement of LAYER3 for general S. Its d₃'' ≥ 0 is a Macaulay inequality inside the core model. LAYER3
  for every S at every depth (3|S ∩ [3m, 4m)| ≤ e·|S ∩ [0, 3m)|) remains ours. Web search (2026-10-20, two extended
  queries) found no prior statement.
- Search of conjectures.io (2026-10-20): its only Wilf items are source23 (c ≤ 4m, solved) and source22 (e = 4,
  withdrawn as already solved). No c ≤ 5m, full-Wilf or Problem 1.8 item was visible; the catalog listing was
  truncated, so this is not exhaustive.

## Search 2026-10-20 (scope: Wilf for collision-free h-regular semigroups; B_h difference bounds)
- Sources: Bacher arXiv:2604.25051 v9, read verbatim by the fetch agent; web searches (extended), arXiv, conjectures.io.
- Bacher v9, exact statements:
  - Def 3.1: h-regular means hΓ ⊂ [c, c+m).
  - Def 3.2: collision-free means every element below c+m has a unique factorization. Equivalently, Γ is B_h and
    the sumsets iΓ are pairwise disjoint mod m.
  - Thm 3.3: for collision-free S, E = E₀(h, a/b, ℓ) + ℓω + ρ.
  - Thm 3.5: h-regular, collision-free and r ≥ ℓ ⇒ W ≥ 0.
  - Conj 2.6: r < ℓ ⇒ E ≥ 0, with no further hypotheses. Bacher notes that it would give Wilf for every CF h-regular S.
  - §3.3: "packing a B_3 set modulo m of cardinality ℓ ≥ 3 with only ℓ gaps is probably already impossible". He
    infers that there is "no collision-free h-regular counterexample". This is heuristic only.
  - No difference-set, Minkowski or lattice-packing bound on r appears. Kovačević–Tan is not cited. The only B_h
    reference is O'Bryant 2024 (thick B_h sets).
- Def 4.4 as transcribed: m̂ = [(b+b′)h − bb′]δ + b + b′, Γ̂ = [(a+a′)h − ab′]δ + a + a′ + Δ, ĉ = h·maxΓ̂ + 1.
  - This is inconsistent with h-regularity, since ĉ − 1 ∈ hΓ̂ ⊂ S. Not used by us.
- No paper or platform proves Wilf for collision-free h-regular semigroups.
- The injectivity of differences of ⌊h/2⌋- and ⌈h/2⌉-fold sums of a B_h set is the classical route to upper bounds
  for B_h sets: a B_{2k} set A gives |kA − kA| distinct differences. We claim only its application here.
- Kovačević–Tan (arXiv 1409.5276, 1610.01341) link B_h sets mod m to lattice packings of simplices. That is the
  geometric form of Lemma 2.
- Status of our Theorem CF-WILF (PROOFS): new as far as this search shows. It removes the hypothesis r ≥ ℓ from
  Bacher's Thm 3.5 and needs neither Thm 3.3 nor Conj 2.6.
- 2026-10-20: no literature statement found for the class "no Apéry ray ends below c" (P̃ = 0) or for the ray identity
  in this form. The ray identity is equivalent to our own R3 (position form of ID-q). The external c ≤ 4m proof
  (conjectures.io) uses pruning and shells, not this class. Status of P0-WILF: new as far as our searches show; not
  separately searched beyond the 2026-10-20 Bacher/B_h search.


## 2026-10-20 search: Wilf for leaves of the semigroup tree (r = 0, S = ⟨L(S)⟩)
- Queries: web (extended) "Wilf conjecture leaves of the semigroup tree"; "Wilf reduces to leaves".
  - Read: Delgado arXiv:1910.12377 (Trimming), §5–6.
  - Read via agent: Chappelon–Ramírez Alfonsín–Stamate arXiv:2507.15006, §4.1.
  - Inaccessible (403 or Anubis challenge): Fromentin–Hivert "Exploring the tree" (ResearchGate, HAL); "On a question
    of Wilf" (ResearchGate).
- Delgado, Remark 5.15: S is a leaf ⟺ S = ⟨L(S)⟩ ⟺ every primitive is left. Prop. 5.16: if gcd L(S) = 1, then
  T = ⟨L(S)⟩ is a descendant of S.
  - No Wilf statement for leaves.
  - "Cutting semigroups" use hereditary properties, which leaves do not give.
- 2507.15006: non-hyperelliptic symmetric semigroups are leaves; type bounds for leaves. No Wilf content.
- A search-summary claim that "Wilf reduces to the leaves of the tree" was NOT confirmed in any source read. Treat it as
  unsupported.
- Status: Wilf for leaves is not known to us. For leaves, W equals Eliahou's W₀. Leaves include generic e = 4
  semigroups (cf. kseth e = 4, which is computer-assisted).
- 2026-10-20 (TM check): searched "Hellus Rechenauer Waldi Wilf tessellation lex ideal Apéry set inequality".
  - Found again: HRW arXiv:1804.06141 (already in item 12) and Spirito, "Wilf's conjecture for numerical semigroups
    with large second generator" (a_2 > (c+μ)/3; already in our LargeSecondGen line).
  - No inequality over the maximal elements (socle) of the tessellating staircase, weighted by degree and residue (our
    Conjecture TM), was found.
  - preprints.org 202604.0551: HTTP 403, NOT checked [already READ in full 2026-10-19 via the user's link: item 46].

## 2026-10-20 (night) search: DEP-CARRY / CR_DEP (column-top rearrangement on the factorization tile)
- Queries: "Wilf conjecture numerical semigroup Apéry set factorization down-set lattice tile inequality" (extended);
  "Wilf conjecture Gröbner / standard monomials Apéry set maximal embedding arXiv 2025 2026 proof".
- Hits: Dobbs–Matthews 1610.08726, BGOW 1903.04342, Sammartano 1710.09245, graph approach 1909.03699, Marashdeh
  2608.12531 (item 10), Delgado–Kumar 2512.23891 (max primitive ≤ 60), DKM 2501.04417, Yang–Zhang preprints.org
  202604.0551, Wilf and Macaulay (EMS). All already listed. No statement of a rearrangement bound over column-top weights
  of a factorization tile, or of the sharp non-maximal-top bound w − c ≤ r − m, was found.
- 2026-10-20 (night, latest) search before recording SUPP-WILF (W ≥ Dep − κ₀ + N ≥ Dep − Σ(|supp|−1)⁺): two web searches
  (extended + standard) on Apéry-set factorization support / column-top / Kunz-coordinate sufficient conditions. Hits:
  1610.08726, 1710.09245, 1909.03699, 1111.1863, 1903.04342, 2608.12531 (#35), 1703.01761, PJM 2018 (Dhayni),
  Math. Z. 2023, 1710.03623, 2012.01358, preprints.org 202604.0551. All already listed; none states a support or
  non-maximal-top criterion.

## 2026-10-20 (evening, machine date) search: SUPP-WILF novelty; modular order-2 bases (sum covers) and CASEB-FLAT
**A. SUPP-WILF (W ≥ Dep − κ₀ + N ≥ Dep − Σ_x(|supp x| − 1)⁺ = m − 1 + Q − Σ_{y∈A}|y|).**
- arXiv API, query abs:wilf AND abs:semigroup, newest first (15 entries back to 2306.09876). Entries from 2026:
  - 2609.32078 (Oracle-tree forcing, |L| = 13);
  - 2608.12531 (Marashdeh, type bound);
  - 2605.14775 (fixed quotient);
  - 2604.25051 (Eliahou semigroups, Farey intervals);
  - 2604.21948 (a_e = 2g+1).
  All were already listed. None states a bound over factorization supports, column tops or maximal cells of an Apéry
  factorization down-set.
- Web (extended + standard): "Wilf's conjecture numerical semigroups arXiv 2026"; preprints.org Wilf 2026; "Apéry maximal
  elements support factorizations pseudo-Frobenius bound". Hits:
  - 2208.14090, 2104.03793, 1903.04342, 2608.12531, 2103.16723, 1610.08726, 2306.09876, 2310.07742;
  - preprints.org 202604.0551 (first-Kunz-layer criterion e(η+2) ≥ 2m; abstract only here, READ in full: item 46);
  - 1111.2779, 1703.01761, Spirito, 1710.09245.
  All were already listed. The closest in spirit is the m − e = 5 paper's Apéry lemma (non-minimal Apéry elements
  bounded by a binomial in α). It is a near-maximal-embedding-dimension count, not a support criterion.
- GitHub (gh search code/repos "Wilf" + semigroup): nsgtree, gap-packages/numericalsgps,
  conjectures-io/conjectures-validator, kseth/wilf-e4, bespokelabsai/conjecture-bench-old, aciderix/Graph-Systems-Exploration.
  - The last one was read (as data): numerical_semigroups/wilf_paper.tex, "Sharp lower bounds for the Wilf number of
    numerical semigroups with small defect", plus the THEOREM_A, THEOREM_B and CONJECTURES notes.
    - Content: W ≥ m − 3 for m − e = 1; W ≥ 2m − 8 for m − e = 2 (m ≥ 4); W ≥ 2m − 12 for m − e = 3 (m ≥ 7); a unified
      conjectured bound per defect d = m − e. Kunz-level case analysis.
    - This regime (e ≥ m − 3) is inside 3e ≥ m (Eliahou), so it is not new for Wilf itself; its sharp constants are a
      different question.
    - No support, column-top or factorization-tile argument (grep: 0 hits for support / factori / maximal element).
- conjectures.io:
  - solved: "Wilf inequality … conductor at most four times multiplicity" (https://conjectures.io/results/fd12daa7-2b0e-460f-a805-f9ba6d9fede4);
  - rejected as already solved: "… embedding dimension 4" (https://conjectures.io/results/487cb5cc-804d-4a17-963a-c938408637a5).
  No open Wilf problem was seen in the part of /problems that was read.
- Status: no prior statement of SUPP-WILF, of its semigroup form, or of the shape-only criterion Σsupp ≤ Dep was found.
  Zhai 1111.2779 has CH′ in crude form. Novelty is "not found in these searches", not established.

**B. Modular order-2 bases (sum covers) — the case-B question.**
- A height-2 lattice tile in ℕ^d is the same thing as a set A = {0} ∪ δ ⊂ ℤ/m with |A| = d+1 whose sums a + a′ (a ≤ a′,
  repetition allowed) cover ℤ/m, using only the pairs of E. Its case-B margin is μ = C(d,2) − 3k_mixed − 2k_loop (PROOFS
  "Dependency chain", link L6). So the size of near-maximal cyclic sum covers decides how large case B can be.
- Haanpää, "Minimum sum and difference covers of abelian groups", J. Integer Seq. 7 (2004), Article 04.2.6
  (https://cs.uwaterloo.ca/journals/JIS/VOL7/Haanpaa/haanpaa.tex), read via a fetch agent.
  - The largest n such that ℤ/n has a k-element sum cover (A + A = ℤ/n, repetition allowed) is
    n′(k) = 3, 5, 9, 13, 19, 21, 30, 35, 43, 51, 63, 67 for k = 2..13 (exhaustive search).
  - Trivially n′(k) ≤ C(k+1,2), strict for k ≥ 3. No asymptotic lower constant is stated.
  - Ratios n′(k)/k² are 0.40–0.47 for 7 ≤ k ≤ 13 (0.53 at k = 6), above the case-B threshold ≈ 1/3 (L6).
  - Translation invariance (A − a₀ is a cover of A + A − 2a₀) makes 0 ∈ A WLOG, matching our A = {0} ∪ δ.
- Weltge–Zyhalko arXiv:2605.19449 (integer 2-bases, size about √n): no explicit cyclic constant usable here.
- Bajnok, "Additive combinatorics: a menu of research problems", arXiv:1705.07444: not readable by the fetch agent;
  NOT checked.
- What Haanpää's table predicts, and what we checked (sumcover.py, fejer, 2026-10-20). Restriction: δ ∋ 1, which is WLOG
  only when δ contains a unit. Two lift choices per δ.
  - k = 5 (d = 4), m = 13: 5 covers; 5 case-B tiles, all height 2, best margin 1, e.g. ⟨13,19,22,27,28⟩ (c = 44).
  - k = 6 (d = 5), m = 19: 5 covers; 4 case-B tiles, all height 2, margin 4, e.g. ⟨19,31,33,34,39,41⟩ (c = 64).
  - k = 7 (d = 6), m = 21: 88 covers; no case-B tile.
  - k = 8 (d = 7), m = 30: 2 covers; 1 case-B tile, height 2, margin 5, ⟨30,45,49,50,52,58,61,65⟩ (c = 97, not open).
  - m = 31 (≤ 2 residues missed): 364 near-covers; no case-B tile.
  - m = 32 (≤ 3 missed): 308; no case-B tile.
  Every case-B tile found so far is a near-maximal sum cover of height 2. No height-≥3 case-B tile has appeared.
- Consequence for CASEB-FLAT (recorded in PROOFS "Dependency chain", L6):
  - If n′(k)/k² stays above 1/3 asymptotically, height-2 case-B tiles have margin of order (3·n′/k² − 1)·d², which is
    quadratic in d.
  - A height-3 cell costs about d − 1 of margin, so for large d a case-B tile with a few height-3 cells is not excluded
    by counting alone.
  - At the extremal sizes the margin is forced: k = 12 (d = 11, m = 63, 15 missing pairs) gives μ ∈ [10, 21] for EVERY
    such cover (when no direction is isolated, z = 0); k = 13 (d = 12, m = 67, 24 missing) gives μ ≤ 6. (Corrected the
    same evening from [10, 25] and ≤ 18, which forgot k_loop ≤ d; PROOFS L6.) So d = 11 is the first size worth testing. CASEB-FLAT is therefore
    THREATENED, not supported, at large d. The counting argument cannot prove it, and a proof must use more than the
    margin.
- 2026-10-20 (night) follow-up search, before the H3-CASEA work: web searches "additive basis of order 3 cyclic group
  maximum n, 3A = Z_n" and "lattice tiling of Z^n by a simplex down-set / semicross / quasi-cross".
  - Hits: Dukes–Hegarty–Herke, EJC 17 (2010) R79 (possible orders of a basis of Z_n); Hegarty arXiv:0906.5484;
    OEIS A004136 (cyclic Sidon-type sums); Stein–Szabó, *Algebra and Tiling* (semicross and cross tilings);
    Schwartz arXiv:1211.0658 (no lattice tilings by quasi-crosses).
  - None gives maximal 3-fold sum covers of Z_n or tilings by simplex-shaped down-sets. The semicross {0, e_i, …, ke_i}
    is a different shape (arms, not a simplex).
  - So no external bound for scenario (b) (dense height-3 tiles) is known to us.

### 2026-10-20 (night): unit truncation, FLAT-U and split certificates — literature check
- Searches (web, standard and extended):
  - "Wilf conjecture" with e(e+1)/2 and embedding dimension;
  - generators below half the Frobenius number;
  - recent arXiv results 2025–2026;
  - Apéry sets of sums of two generators with reduction number 2;
  - Kunz-coordinate LP certificates.
- Hits:
  - [Sammartano 1111.1863](https://arxiv.org/pdf/1111.1863) (2e ≥ m, m ≤ 8).
  - [Spirito 1710.09245](https://arxiv.org/pdf/1710.09245), #24. Its hypothesis is the opposite of HALF: all generators
    LARGE, n_1 > (c+m)/3, with m ≤ (8/25)e² + ….
  - [Dhayni 1610.08726](https://arxiv.org/pdf/1610.08726): Apéry criteria with sums w_1 + w_α.
  - [Bruns–García-Sánchez–O'Neill–Wilburne 1903.04342](https://arxiv.org/pdf/1903.04342) (Kunz polyhedron, faces,
    m ≤ 18) and the m = 19 follow-up ([Springer s00454-021-00344-x](https://link.springer.com/article/10.1007/s00454-021-00344-x)).
  - [Delgado–Eliahou–Fromentin 2310.07742](https://arxiv.org/abs/2310.07742) (g ≤ 100).
  - [Marashdeh 2608.12531](https://arxiv.org/abs/2608.12531) (type bound and a reduction).
  - Yang–Zhang, "Wilf's Conjecture from the First Kunz Layer", Preprints.org 202604.0551: **ALREADY READ — item 46,
    read in full 2026-10-19 from the user's link, proofs re-derived, (a) and (b) checked exhaustively to genus ≤ 34
    (E272; PROOFS "LK+YZ").**
    - CORRECTION 2026-10-20: this entry first called it "new to us, full text NOT READ (HTTP 403)". That was wrong. The
      check grepped LITERATURE.md for Spirito only, not for Yang/Zhang/202604.0551. Pointed out by the user, who notes
      the paper has been re-found about eight times.
- Comparison with our statements:
  - Yang–Zhang item 46(a) is the exact level formula ℓ = q + Σ_t Θ_t + Θ_{q−1,ρ}. It is our ℓ = Σ_x μ_x counted by levels
    instead of by classes. Their staircase (b) truncates to the classes with Kunz coordinate 1, i.e. Apéry element in
    (m, 2m). Our unit truncation U truncates instead to the classes of the minimal generators, of any size. Their
    proofs use only the monotonicity Θ_{t+1} ≥ Θ_t, never the pair Kunz relations or the wrap window used in FLAT-U.
  - HALF (all generators ≤ (c+m−1)/2 ⇒ W ≥ q(C(e+1,2) − m) − …) is not among item 46 (a)–(f). Their criteria need many
    elements in (m, 2m) (e(η+2) ≥ 2m). HALF instead bounds every generator by (c+m−1)/2 and needs m ≲ C(e+1,2).
  - No hit has the exact split identity, Theorem CERT, FLAT-U or H3-HALL. FLAT-U (Apéry height ≤ 2 ⇒ Wilf, via the
    pair Kunz relations and the ρ-cell wrap window) re-proves our LEAN corollary of Flat-MaxCL. Its novelty against
    Eliahou-type and Kunz-face arguments is UNVERIFIED; the Kunz-face method of BGOW is computational and per face.

### Search 2026-10-21: residue reduction T = ⟨m, g_i mod m⟩, descent below the multiplicity, truncated sumsets
- Rechecked 2026-10-23 for E431: exact residue-reduction/primitive-monotonicity queries and
  Wilf plus blowup/Lipman/shifted-family queries supplied no theorem used to establish RD.
  Ordinary shifted-family results cannot be substituted for the fixed-m operation which
  shifts only the OTHER primitives. The E431 identity, integer tangent realization and
  counterexample are checked directly; no novelty or exhaustive-literature claim is made.
- Queries: "Wilf conjecture numerical semigroup generators reduced modulo multiplicity"; "Wilf shifted family
  ⟨n, n+r_1, …⟩"; "Wilf induction on multiplicity, smaller multiplicity, oversemigroup"; site:conjectures.io OR
  site:preprints.org "Wilf 2026"; GitHub `gh search repos "wilf conjecture"` (only our own private repo).
- Found nothing that states W(S) ≥ W(⟨m, g_i mod m⟩), Lemma DESCENT-T, ID-U, or a Wilf-type inequality for truncated
  sumsets kA′ + mℕ.
- Results returned, all already listed:
  - Sammartano 1111.1863, Dhayni 1610.08726, Spirito 1710.09245, Eliahou 1909.03699, BGOW 1903.04342.
  - DKM 2501.04417 (Problem 1.8 still open in v3).
  - Delgado–Kumar 2512.23891.
  - Yang–Zhang Preprints 202604.0551 (item 46).
- Closest internal relatives: NoWrap (the T = ℕ case, ours, 2026-10-19), Lemma DESCENT (ours, 2026-10-21), Zhai's CH′.
- Status: novelty plausible but unconfirmed. Before any public claim, ask an expert (Delgado or Eliahou).

### Search 2026-10-21 (later): Wilf for Apéry sets w.r.t. the largest generator; truncated sumsets
- Queries:
  - "Wilf conjecture numerical semigroup Apéry set with respect to the largest minimal generator sums of at most three
    generators";
  - "truncated sumset Wilf numerical semigroup 3A residues modulo m left elements conductor".
- No result on H3max (Apéry height ≤ 3 w.r.t. the largest generator) or on truncated sumsets kA′ + mℕ.
- Returned, already listed: Eliahou 1703.01761 (c ≤ 3m via Macaulay), Spirito 1710.09245 (sumsets of residues mod
  the multiplicity: ℤ/μ = A ∪ (A₁+A₁) ∪ (A₁+A₂), a different decomposition), BGOW 1903.04342, Sammartano 1111.1863,
  Eliahou EJC 2020, divsets (HAL hal-04234167), Yang–Zhang 202604.0551.

### Search 2026-10-21 (later still): relative Wilf between S and T = ⟨m, g_i mod m⟩ (PAY2), level-1 generators
- Queries (web, standard):
  - "Wilf conjecture numerical semigroup generators in (m,2m) Apéry set reduction modulo multiplicity semigroup
    ⟨m, a_1,...,a_d⟩ induction";
  - "numerical semigroup Wilf inequality comparing S and the semigroup generated by residues of generators modulo the
    multiplicity".
- Hits:
  - Dhayni arXiv 1610.08726 (Apéry special cases);
  - Eliahou JEMS 807 (c ≤ 3m);
  - Yang–Zhang Preprints 202604.0551 (item 46, READ 2026-10-19; first Kunz layer η = |S ∩ (m, 2m)|, e(η+2) ≥ 2m);
  - Spirito (large second generator);
  - Cisto et al. 1909.13120 (generalized numerical semigroups);
  - 1903.04342 (fixed multiplicity);
  - 1111.2779, 1111.1863.
- None compares S with the residue semigroup T, or states e(ℓ(S) − ℓ(T)) ≥ c(S) − c(T). No match for PAY2 or for
  TRUNC₃^≠. Novelty is unclaimed: the search is shallow, and the statement is internal to our residue-descent program.

### Search 2026-10-21 (14:07 EDT): before gating D6 / A1-eT (Q5 residual)
- Queries (web):
  - "Wilf conjecture ⟨m, m+a_1, …⟩ shifted generators W(S) ≥ W(T) descent embedding dimension";
  - "Rohrbach problem thin basis of order 3 lower bound collisions arithmetic progression".
- Results:
  - Only the known general results: Sammartano 1111.1863, Dhayni 1610.08726 (Apéry-set lemma relating m − ν to
    non-minimal Apéry elements), Spirito 1710.09245.
  - Thin-basis literature: Cassels, Raikov–Stöhr, Blomer, Nathanson 0905.3144.
- No statement comparing W(⟨m, m+A⟩) with W(⟨m, A⟩). No bound on the collision count of a 3-fold sumset containing
  a long AP with the constant needed for D6.
- Thin bases of order 3 force a constant fraction of collisions, but that constant is far below what D6 needs. So
  D6 is not available off the shelf.

### 2026-10-22 — bounded refresh for backwards certificates and repair matching
- Reopened the primary depth-four result: https://conjectures.io/results/fd12daa7-2b0e-460f-a805-f9ba6d9fede4 .
  Its review still states the full c<=4m target, accepted with Lean verification. Our previous local kernel audit
  remains the project's evidence; this refresh is not a new compilation.
- Reopened Bacher v9, dated 14 Oct 2026: https://arxiv.org/abs/2604.25051 and
  https://arxiv.org/html/2604.25051v9 . The abstract concerns bounded verification and Farey-interval families;
  it does not supply the missing general certificate theorem.
- Reopened DKM v3: https://arxiv.org/abs/2501.04417 (last revision 1 Oct 2026), already in this record.
- Exact searches for Wilf/Kunz linear programming, splitting certificates, generator levels and fractional matching
  did not locate a source establishing universal nonnegativity of the new repair-assignment bound. This is only
  a bounded search, not a novelty claim. The bipartite-double-cover idea is standard matching theory (e.g.
  https://arxiv.org/abs/2303.05250 ); PROOFS gives a direct permutation/dual proof for the weighted matrix used here,
  including the generator and repeated-parent diagonal cases, so no unverified matching theorem is an input.
- Compared the matching step with Eliahou's graph theorem (already recorded in section 2.4):
  https://arxiv.org/html/1909.03699 , Theorem 3.24. That bound matches raw depth demands q-1/q and counts unmatched
  vertices at depth>=1. Our elementary certificate applies matching to residual demands after a generator-aware
  upper-side closure, allows fractional packing, and does not claim dominance over Eliahou's bound.
- Compared BASE deflation with Bacher section 4.3, Lemma 4.7 (forward inflation of h-regular truncations):
  https://arxiv.org/html/2604.25051v9#S4.SS3 . The exact inverse Apéry-minimality argument under BASE hypotheses is
  written in PROOFS; the earlier conditional obligation is closed. This does not establish an arbitrary inverse
  inflation or universal certificate nonnegativity.
- E398 consulted Guzmán–Klivans, *Chip-firing and energy minimization on M-matrices*,
  https://arxiv.org/abs/1403.1635 , and Postnikov–Shapiro on parking ideals,
  https://math.mit.edu/~apost/papers/monomial.pdf . General M-matrix z-superstability must not be silently
  identified with the subset-toppling test. Our finite tile certificate instead verifies every subset test,
  complete residue bijection and strictly positive reduction cost, then proves termination/minimality directly
  (PROOFS). No parking theorem or novelty claim is assumed. The gluing theorem arXiv:2306.09876 remains already
  recorded as #29; gluing was considered as an adversarial construction, not activated as a separate target.

### 2026-10-23 — joint profile/certificate duals and primitive-edge reduction

- Re-read the primary [BGOW paper](https://arxiv.org/html/1903.04342), Sections3,4,6. Its Kunz-face
  verification and poset-game framework already use linear combinations of face constraints to prove
  Wilf regionally. E414 does not claim novelty for that method or a proof of BGOW's universal conjecture;
  it adds separate coupled capped-certificate variables and keeps actual depth unbounded. Our unit
  non-tight margins are valid for integer Kunz coordinates; fractional optima are proof relaxations.
- [Brower–McDonough–O'Neill](https://arxiv.org/abs/2401.06025) studies faithful projections of Kunz faces
  and the Kunz fan. E415's specific implication is proved directly by primitive-factorization paths;
  no new general projection theorem or novelty claim is inferred from a similarity of terminology.
- The31 regional certificates do not exhaust all faces/multiplicities. The missing theorem is a
  uniform nonnegative budget for all realizable profiles; no new external theorem is assumed for it.

### 2026-10-23: advisor strict recession deduction and primitive boundary source check

Re-read Zhai [1111.2779v1](https://arxiv.org/html/1111.2779v1), Lemma3/Thm1, and BGOW
[1903.04342](https://arxiv.org/html/1903.04342), Sections4/6. The homogeneous column bound is known;
E416's application to the coupled model and strict equality-case proof are credited to the user's
advisor, not claimed novel. The factorization simplex obstruction uses Delta_1-Delta_{H-1}, with a
self-contained count in PROOFS; no classification of perfect codes is required.

Read Brower–McDonough–O'Neill [2401.06025v3](https://arxiv.org/html/2401.06025v3), Definitions4.1,
Lemma4.5, Proposition4.6, Example4.7 and Theorems4.8/4.9. The latter do give a homogeneous primitive
projection through inner trades and outer Betti inequalities, with strict feasibility characterizing
Kunz realizability. They do not by statement alone preserve each affine gap>=m. E417 supplies a
separate canonical monomial-boundary rewriting proof retaining those margins; it does not claim that
its boundary is a minimal presentation/outer Betti set. Generic Groebner/LP methodology is not a
novelty claim. Searches on arXiv, GitHub and conjectures.io for primitive duals/poset games did not
supply a uniform finite-correction payment theorem; this limited search is not a nonexistence claim.

### 2026-10-23: primitive dual budgets / interior residue matching

Focused arXiv/GitHub/conjectures.io searches for primitive duals and residue-boundary allocations found
no source used for a new positivity claim. E419 is ordinary affine LP-dual transfer, no novelty claimed.
E420 uses the standard cross-sum difference-set injection already present in the earlier B_h notes
(PROOFS, difference-body lemma) and in the advisor's E416 proof. Its simple rank-credit consequence is
dominated by the old whole-boundary rearrangement estimate; the false CR-TILE criterion is not revived.
The E421 counterexample and all its semigroup/repair invariants are independently computed repository
results, not attributed to an external paper.

### 2026-10-23: weighted column transport / exact axis flow

Rechecked [Zhai 1111.2779v1](https://arxiv.org/html/1111.2779v1), Section3/Lemma3: the down-set
column inequality is established prior work. E422 combines the existing column identity with
signed tight repair rows and arbitrary weighted unpaid coordinates. Binary-tree telescoping,
min-cost-flow integrality and residual-potential optimality are standard; no novelty is claimed
for those ingredients. Internal review includes CH', Ramp Lemma, GW-CR, CP/CCP and failed local
column-payment refinements. E423's negative optimal baselines prohibit another sourcewise funding
claim. A focused search for Wilf/Apéry tight transport supplied no external theorem used to assert
its corrected sign; absence of a hit is not a novelty/nonexistence claim. Reopened
[Marashdeh 2608.12531](https://arxiv.org/html/2608.12531), already in this record: its defect/type
reduction does not state the needed weighted transport payment theorem. No new result from it is
assumed here.

E425 uses ordinary permutation telescoping and the standard minimum-prefix cycle allocation;
no novelty claim. Focused searches on primitive/column cycles and minimum-distance diagrams did
not provide a cited weighted Wilf payment theorem. The Cayley degree/diameter literature (e.g.
Dougherty–Faber, arXiv:math/9412223) concerns a related setting, not a result invoked to pay the finite
correction here. No inference from its abstract to the needed weighted inequality is made. The
primitive orbit count in PROOFS is proved directly and adds no independent continuous constraint;
the disjunctive integer exit condition has the limitations stated there.

### 2026-10-23: coefficient-preserving circulation, actual dual restriction, boxed allocation

Internal comparison includes E419, failed per-chain/direction funding, and E425/E426. E427 is an
elementary dominance calculation: balanced nonnegative primitive rows are weaker than the existing
positive primitive bounds. E428 is ordinary restriction of an LP dual; E429 uses an epigraph for
max(0,a-T) and standard box-polytope extreme-point reasoning. No novelty is claimed for these
optimization ingredients. The exact coefficient/budget identities are proved directly in PROOFS.
Focused arXiv/GitHub/conjectures.io searches yielded no theorem invoked to assert their universal
finite-budget sign; this is not a claim that no such result exists. BGOW1903.04342 and the existing
primitive Kunz-face literature remain the comparison for regional polyhedral certificates.

Opened [Montgomery, The honest embedding dimension of a numerical semigroup](https://link.springer.com/article/10.1007/s00233-026-10637-3)
(2026), abstract/Definition3.1: its dimension concerns analytic curve realizations and differs from
the number of minimal semigroup generators used here. It is not used to replace Wilf's e or to
claim an additional universal reduction. No work on that separate classification problem is activated.


### E432 closure reduction: prior algorithm versus the unproved Wilf capacity claim (2026-10-23)

Jean-Claude Picard, [Maximal Closure of a Graph and Applications to Combinatorial Problems](https://pubsonline.informs.org/doi/pdf/10.1287/mnsc.22.11.1268),
Management Science22(11)(1976),1268-1272, DOI10.1287/mnsc.22.11.1268. Primary publisher
metadata/abstract checked. The closure/minimum-cut construction is standard; E432 gives a
self-contained conversion for the support functional. No novelty is claimed for max-flow or
closure optimization. No external theorem is used to assert Delta_H<=m: that new sufficient
capacity target remains unproved. Exact searches for the Wilf column/carry/partial-tile
statement supplied no theorem used in the proof; absence of a search hit is not a priority claim.

### E433 allocation check (2026-10-23)

Searched the existing record for interior/difference-body/matrix-rank arguments before
using them. The one-step cross-sum injection is already proved in Ray identity/E344 and
E420, so no novelty is attributed to it. The new joint-interior PAYMENT claim is false;
PROOFS/FAILED E433 give exact counterexamples. The full-tile phase averaging identity is
also older; E433 derives its fixed-partial-cut version and critical deletion conditions.
Web searches for Wilf with linear algebra, Hall/monomial matching, and negative boundary
residue matching supplied no theorem USED to prove the proposed directional-pool allocation.
This is not a priority claim or an exhaustive literature exclusion. The new closure test
uses the same standard Picard reduction cited above. Its universal sign remains UNKNOWN.

### E434 bookkeeping and duplication check (2026-10-23)

Searched PROOFS/FAILED for wrapped-parent allocations, power tokens, residue descent and
boundary rank arguments. The E320 power-token carry mechanisms use actual levels/orders;
they do not prove the new raw-carry residual sign. E434's fixed nonwrap allocation and
leakage identity are proved directly, without an external theorem or a novelty claim.
The attempted all-primitive closure of the lift set is precisely the earlier U=T assumption
from E379/E431; it is not a new reduction and is false without that hypothesis. A separate
boundary-alias kernel payer is refuted by the existing19 tile, not justified by E420's
valid joint-interior injection. Broad Wilf/Hall/monomial-boundary/differential searches
supplied no theorem USED to infer universal extendability. No priority claim follows.

### E435 scope and prior principle (2026-10-23)

The safe-cut proof uses the standard cross-sum injection already recorded in E420 and
the earlier one-step difference body. No new difference-set theorem is claimed. The
internal-alias slot injection, surplus-column selection and joint defect identity are
proved directly in E435. Searches of the record for internal/exterior aliases and broad
Wilf/column/matching queries supplied no external result USED to prove the remaining
joint inequality. No priority or exhaustive-literature claim is made. The scalar-lowering
trial is refuted by a self-contained height1 rank calculation, without a numerical search.

### E436: classical special sum-dominant sets versus the new stage obstruction (2026-10-23)

Peter Hegarty, [Some explicit constructions of sets with more sums than differences](https://arxiv.org/html/math/0611582v2),
introduction, observation2: the base-expansion method and the classical8-point set are
explicitly recorded. Hùng Việt Chu, Nathan McNew, Steven J. Miller, Victor Xu, Sean Zhang,
[When Sets Can and Cannot Have Sum-Dominant Subsets](https://cs.uwaterloo.ca/journals/JIS/VOL21/Miller/miller8.pdf),
Journal of Integer Sequences21(2018),Article18.8.2, Definition3/section3.1, calls a set special
when its sum/difference cardinality gap is at least its size and uses the8-point cube.
Both PRIMARY full texts were opened. No novelty is claimed for the set or product method.
Base29 suffices here by a direct digit argument; the semigroup lift and its representative-
independent obstruction to L_out<=C are proved in E436. Novelty of that application has
not been established. The failed ETH mirror returned404; the official journal PDF was read.
The source is used for the classical construction, not to assert Wilf or JD+ positivity.

### E437: elementary forest payment, no external positivity theorem (2026-10-23)

The spanning-forest orientation, cycle count edges-vertices+components and distinct-slot
argument are elementary and proved directly in PROOFS E437. No novelty is claimed for
these graph principles. Record searches for forest/cycle/cross-word statements found the
older restricted-dimensional forest work and E430's DIFFERENT canonical Hasse-graph cycle
count; neither is substituted for the present all-alias graph. Web queries covered Wilf
boundary/difference-set/forest and monomial-order-ideal formulations, plus GitHub, arXiv
and conjectures.io discovery. They supplied no external theorem USED for the remaining
cycle-and-carry sign. This is not an exhaustive-search or absence-of-literature claim.
The general partial allocation and its limitations are self-contained; the classical
MSTD construction remains attributed in E436 above.

### E439/E440: fixed quotients and numerical duplication (2026-10-23)

Opened primary full texts [Ojeda–Rosales, On Numerical Semigroups with Fixed Quotient,
2605.14775](https://arxiv.org/html/2605.14775), Proposition4.9, Theorems4.12/4.14/4.15
and Corollary3.6; also [Singh–Srinivasan2306.09876](https://arxiv.org/html/2306.09876v1),
Definition2.1, to distinguish ordinary gluing from the more general rank-one case.
The rank-one formulas F(S)=kF(T)+(k-1)n and g(S)=kg(T)+(k-1)(n-1)/2 are PRIOR results,
with n in T and gcd(n,k)=1. E439's Apéry proof reproduces them and includes T=N directly.
The positive Wilf correction/minimal-counterexample gcd condition is a direct application;
no claim that the underlying genus/Frobenius formulas are new. Corollary3.6 concerns the
paper's different Delta_d(a) construction; it is not misquoted as the general rank-one
Wilf identity. The supplied E439 proof separately checks primitive survival and e(T).

Opened [D'Anna–Strazzanti1211.3693](https://arxiv.org/html/1211.3693), introduction, and
[Strazzanti1404.4959](https://arxiv.org/html/1404.4959), Proposition3.3, the following
Frobenius discussion and Lemma4.8. Every numerical semigroup being a duplication of its
half using a relative ideal is KNOWN. Normalizing that ideal to minimum0 is also KNOWN.
E440's parity count and primitive-pair accounting are self-contained applications of this
representation, not a newly discovered parametrization. Neither paper is invoked as
proving the universal conditional Wilf transfer. E440's false monotone payer and concrete
cofactor1 obstruction are independently checked repository calculations; novelty of that
particular observation is unassessed. Searches covered Wilf/gcd/scaling/quotient/duplication,
arXiv, GitHub and conjectures.io. Search absence supplies no priority or nonexistence claim.
