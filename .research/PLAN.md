# PLAN.md — the plan to prove Wilf when work resumes (written 2026-10-21, 18:10 EDT; status: PROPOSED, needs the user's go)

## Target and scope line
**Target: ANCHOR, for every S with c > 4m and 3e < m:**

    DEF ≤ ρ + EXC + U_top + r.

All terms are from Identity ID-q (PROOFS "ID-q for every numerical semigroup"):
- DEF = Σ_y max(0, j_y − c_y): wraps not refunded by crossing parents;
- EXC = Σ_y max(0, c_y − j_y);
- U_top = the unused incidence weight at positions of level q − 1;
- r = the number of right primitives;
- ρ = qm − c.

**Proves Wilf for: every numerical semigroup.**

**Reduction to all S: yes. Every link is already proved:**
- ID-q is an exact identity for every S (PROVED; asserted on 14.4M S).
- ANCHOR ⟹ CORE₁ (E + r ≥ 0), by the ID-q algebra (PROVED).
- CORE₁ ⟹ Wilf, since W = E + r(ℓ − q) and ℓ ≥ q + 1 (PROVED).
- Wilf is already settled outside this domain:
  - c ≤ 4m by the external proof, which we kernel-checked;
  - 3e ≥ m by Eliahou.

So ANCHOR on this domain alone gives Wilf for every S.

**Fallback chain.** Each fallback is still universal. Take the next one only if the previous one is refuted:
1. ANCHOR;
2. CORE₁, which keeps the weight-≥2 pool as credit;
3. the exact Wilf form W = E + r(ℓ − q) ≥ 0, which also keeps the credit r(ℓ − q − 1).

Never replace the target by a sub-family (fixed height, fixed level, fixed depth, fixed e). Data may be sliced by q for
diagnosis only. Every lemma is stated for all S in the domain.

## Tools
- **C only for enumeration and checking.**
  - Enumerator: `src/scratch/p37/enumh4.c`. It covers fixed m and e, Kunz coordinates ≤ K, c ≥ 4m + 1 and 3e < m, and
    generates each S exactly once. The height-≥4 filter will be removed.
  - ID-q / ANCHOR / CORE₁ evaluation: `src/scratch/p32/anchgen.c`, which computes the canonical representations and
    asserts ID-q.
  - T2 evaluation: `src/scratch/p32/anchgen_t2.c`.
- **Gurobi ONLY in step C3,** through the C API in the pattern of `src/scratch/p37/enumlp.c`.
- **Not allowed without the user's approval:** Python Gurobi MILPs, annealers and subagents.
- All compute runs on fejer. SCOPE.md must be ACTIVE with the user's quote (the hooks enforce this).

## Phase A — setup and validation (about 2 h of work, minutes of compute)
- A1. **Restart and activate.** The user restarts fejer, or approves a restart:
  `gcloud compute instances start fejer --zone us-east1-b`. Set SCOPE.md ACTIVE with the user's exact words.
- A2. **Literature check, 15 min, dated in LITERATURE.md.**
  - Search conjectures.io first (the c ≤ 4m proof came from there): anything at c ≤ 5m or general depth.
  - Then arXiv and GitHub for "E + r ≥ 0" / Eliahou number plus right primitives / ANCHOR-type deficit bounds.
  - If a depth-5 or general proof exists, stop and report it to the user.
- A3. **Read the depth-four payment mechanism**
  (`lean/external/conjio_d4`: `st_A29A`, `an_anchor_bound`, the shell and the two injections). ANCHOR at q = 4 is that
  theorem. Write down exactly which credit pays each Q₃ deficit there. That is the template for step C1.
- A4. **Write `src/scratch/p39/enumanc.c`.**
  - It is the enumh4 enumeration without the height filter, plus the anchgen canon() / ID-q evaluation per S.
  - Per S it computes: W (independently, from a membership bitset), E, r, q, ρ, DEF, EXC, U_top, the pool, and the
    ANCHOR, CORE₁ and T2 slacks.
  - It asserts ID-q exactly and aborts on any mismatch.
  - Outputs:
    - per (m, e, q): the minimum of each slack, with generators;
    - a slack histogram for values ≤ 3;
    - a full record of every S with ANCHOR slack ≤ 2 (the TIGHT set): the positions of every deficit unit and every
      credit unit.
- A5. **Validate.**
  - m = 13–16: on the S that overlap with anchgen's genus-≤30 run, the slacks and failure counts must match exactly.
  - W must match enumlp's W on the same (m, e).
  - Checkpoint to the user.

## Phase B — exhaustive backward search (C only)
- B1. **Run** `enumanc` for m = 13–21, every e with 3e < m, K = 12, on 8 processes.
  - ETA: E375 covered m = 16–20 with the height filter in 48 min on 6 processes (106M S). Without the filter, and with
    the ID-q evaluation, I estimate 3–5 h in total, with a ceiling of 8 h.
  - I time m = 16 first, report a revised ETA, and checkpoint after each m.
  - This is exhaustive only within Kunz ≤ 12 (c < 12m) and m ≤ 21. It is evidence, not a proof.
- B2. **Decision rules.**
  - ANCHOR < 0 on some S:
    - verify with the Python ID-q code (`src/scratch/p38/idq.py`) and with anchgen;
    - if it is confirmed, ANCHOR is FALSE: record it in FAILED.md, tell the user, and switch the target to CORE₁.
  - CORE₁ < 0: same procedure, switching to the exact Wilf form.
  - W < 0: a counterexample to Wilf. Verify independently twice from the generators, report it to the user at once,
    and stop.
- B3. **Deliverable:** the TIGHT set (ANCHOR slack ≤ 2) with full deficit/credit records, and the minimum slack per
  (m, q).

## Phase C — extract the payment rule (the backward step: from tight constraints to a lemma)
A deficit unit at position y must be matched to a distinct credit unit. Candidate edge classes, all defined from the
additive structure of S (positions mod m, generator offsets b_i):
- (P) **parent / child:** x = y ∓ b_i along a canonical incidence;
- (T) **translate:** x = y + b_i − b_j;
- (W) **conductor window:** a ρ-unit pays a deficit at a position in [m − ρ, m). There is an equality case:
  m = 16, ρ = 5, B = {1,2,11,14}, q = 6, where DEF = ρ.
- (R) **right primitive:** a right primitive at z pays y when z = y + b_i, i.e. the child of y overflows past level q;
- (U) **top unused:** an unused incidence (x, i) with λ_x = q − 1 pays y when x + b_i ≡ y.

Steps:
- C1. **0/1 rules (C only).** For each subset of edge classes, run a bipartite max-flow per S (Dinic, in C) over the
  TIGHT set, then over all S of the B1 domain. Find the minimal subsets that pay every S. A rule fails on S exactly
  when Hall fails; record the violating Hall set.
- C2. If a 0/1 rule pays every S: go to Phase D with that rule.
- C3. **Weighted rules (the only Gurobi use).**
  - If no 0/1 rule pays every S, solve one LP, built with the Gurobi C API from the TIGHT set.
  - Variables: one nonnegative weight per edge class, shared across all S.
  - Constraints: for every S and every Hall-violating deficit set, the weighted credit available ≥ the deficit.
  - The optimum gives the best class weighting. The dual gives an exact obstruction: a weighted family of semigroups
    that no class weighting can pay.
  - Then either refine the classes using the obstruction's structure and repeat C1, or conclude that ANCHOR needs
    non-local credit and move to the next target in the fallback chain.
- C4. **Deliverable:** the rule R* (classes, and weights if any) with its exact statement, or the dual obstruction.
  Checkpoint to the user.

## Phase D — state and gate the lemma
- D1. **Write PAYMENT(R\*) in PROOFS.md.** For every S with c > 4m, 3e < m, the deficit units inject into the credit
  units along R*. Show explicitly that PAYMENT(R*) implies ANCHOR, which implies Wilf.
- D2. **Gate** (FAILED.md registry, necessity audit).
  - Max-flow check of R* on every S of the B1 domain and on anchgen's genus ≤ 30 (14.4M S).
  - The extremal families already on record: Delgado ⟨μ,γ,γ+1⟩, Eliahou–Fromentin B₃, minimal-span B₄, DK, STAR, and
    the E343 collision-free family.
  - The exact payment structure at q = 4 must reproduce the external proof's injections.

## Phase E — prove PAYMENT(R*) on paper
- E1. **Construct the injection explicitly.** Generalize the depth-four shell:
  - choose an anchor position (minimizing rank plus |D(y)|, as in depth four);
  - send each deficit unit to its R*-credit;
  - prove injectivity from distinct residues mod m and from the canonical-representation order (divisor closure).
- E2. **Timebox: 6 hours of proof work per candidate rule.**
  - If a step fails, the failing step is a precise inequality. Add it as a constraint, re-run C1/C3 on that
    inequality, and report to the user.
  - Do not narrow the domain to make the step go through.
- E3. If the proof is complete, hand it to the user as a PROOFS.md section with every dependency listed.

## Phase F — kernel check
Formalize in Lean 4, against our own definitions in `lean/`:
- ID-q;
- ANCHOR ⟹ CORE₁ ⟹ Wilf;
- PAYMENT(R*).

Use subagents only if the user approves each launch.

## Never
- Restrict the target to a sub-family.
- Endorse a proposed direction without stating its scope line.
- Use Gurobi outside step C3, or run annealers or bigger enumerations as a substitute for Phase C/E.
- Launch a subagent without the user's approval.
- Go 45 minutes without a checkpoint.
- Leave commits unpushed.
