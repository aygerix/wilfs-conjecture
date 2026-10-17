# CLAUDE.md — Wilf's Conjecture (Numerical Semigroups)

## Mission: sustained original mathematical research

This is an open-ended, **30-day mathematical research project** whose primary objective is to **prove Wilf's conjecture for every numerical semigroup**. It is **not** a one-session attempt, a literature survey, a request for another bounded verification, or a request for a polished explanation of why the conjecture is difficult.

Problem reference: https://epoch.ai/frontiermath/open-problems/numerical-semigroups

**Important distinction:** Epoch's automatically verifiable challenge emphasizes finding a counterexample. This project instead prioritizes a *universal proof*. Do not assume the conjecture is true: if a genuine counterexample appears, independently verify it and report it immediately. Neither a search nor a collection of special-case proofs establishes the universal statement.

Treat literature review, formal definitions, reproduction of published proofs, and baseline enumeration as **Phase 0 only**. These are prerequisites to research, not its completion.

## Primary objective: a rigorous universal proof

A **numerical semigroup** `S` is a cofinite additive submonoid of the nonnegative integers containing `0`. For a proper numerical semigroup define:

- `c(S)` (conductor): the least integer `c` such that every integer `n >= c` belongs to `S`.
- `g(S)` (genus): the number of nonnegative integers not in `S`.
- `L(S) = S ∩ {0, ..., c(S)-1}` (left elements); `ell(S) = |L(S)| = c(S) - g(S)`.
- `e(S)` (embedding dimension): the number of minimal positive generators of `S`.

**Wilf's conjecture** is

    e(S) * ell(S) >= c(S)

for every numerical semigroup `S` (with `S = N` treated separately or covered by a consistent `c=0` convention). Equivalently,

    W(S) := e(S) * (c(S) - g(S)) - c(S) >= 0.

The objective is a finite, rigorous argument valid for **all** numerical semigroups, regardless of multiplicity, embedding dimension, genus, or conductor. Every reduction must preserve the exact quantifiers and definitions.

A computational verification to a large bound, a heuristic probabilistic argument, or a result for almost all semigroups is **not** a proof of Wilf's conjecture.

### What counts as success

Produce a complete proof with every nontrivial lemma stated precisely, hypotheses checked, and dependencies explicit; include a self-contained mathematical manuscript. Seek independent checking, ideally **Lean 4/mathlib formalization** of the main argument. A claimed proof is *provisional* until all gaps and external proof obligations are resolved.

If the conjecture is false, an explicit semigroup with independently verified generators, conductor, left-element count, and `e * ell < c` is a valid decisive discovery. Do not silently change the mission to counterexample hunting; proof remains the primary direction.

## Secondary objectives

Discover reusable structural inequalities for numerical semigroups; prove reductions from all semigroups to more constrained families; discover relationships among Apéry sets, minimal generators, conductor, and genus; strengthen existing special-case theorems; or find new principles that plausibly imply Wilf's inequality.

A strong, independently verified partial theorem is worthwhile even if it does not solve the conjecture. Distinguish **observed**, **conjectured**, **proved on paper**, **kernel-checked**, and **externally reviewed**. Do not claim novelty without comparing exact hypotheses to the literature.

## Research directions: maintain at least three genuinely distinct lines

1. **Apéry sets and Kunz coordinates.** For multiplicity `m`, write `Ap(S,m) = {w_0,...,w_{m-1}}`, with `w_i` the least semigroup element congruent to `i (mod m)` and `w_0=0`. Study Kunz coordinates `x_i=(w_i-i)/m` for `1 <= i < m`, their closure inequalities, and the exact identities `g = sum x_i` and `c = max_i w_i - m + 1`. Derive inequalities connecting their distribution to `e` and `ell`. Do not mistake the number of small Kunz coordinates for the embedding dimension; compute minimal generators correctly.
2. **Primitive elements, Apéry posets, and additive structure.** Analyze how the partial order `u <=_S v` iff `v-u ∈ S` controls primitive generators, decomposable elements, and the left interval. Seek an injection, disjoint packing, covering, or charging argument proving `c <= e*ell`.
3. **Conductor layers and interval decompositions.** Partition the nonnegative integers into intervals of length `m`, compare populated and missing layers near the conductor, and investigate whether local density and the distribution of primitives force the global inequality. Test proposed inequalities on semigroups with highly uneven layers, not only typical examples.
4. **Commutative algebra and Hilbert-function methods.** Investigate semigroup rings, graded structures, type, Betti numbers, Hilbert functions, and multiplicity. Seek a general inequality or reduction whose semigroup specialization is Wilf. Confirm every translation back to the original combinatorial invariants.
5. **Reductions and extremal counterexample analysis.** Assume a counterexample with minimal genus, conductor, multiplicity, or another well-founded measure, then derive restrictions and attempt to rule it out. Investigate surgery operations on numerical semigroups and precisely track `e`, `ell`, and `c` under those operations. Avoid assuming that an operation preserves Wilf's defect without proof.
6. **New structural mechanisms.** Develop approaches beyond established Apéry/Kunz/semigroup-ring frameworks: inequalities via additive bases, poset decompositions, extremal combinatorics, or another representation. The goal is to uncover a principle that applies to *all* semigroups, including exceptional cases missed by density heuristics.

Do not allow incremental verification of known special families to crowd out attempts at a universal mechanism. Maintain at least three active lines until clear mathematical evidence justifies changing the allocation.

## Scientific workflow: proof-first, conjecture-driven

Repeat this cycle throughout the project:

1. Formulate a precise candidate theorem or reduction; write its quantified statement and explain exactly how it would advance Wilf.
2. Try to prove it **before** relying on large-scale experimentation. Identify the missing implication, not just a list of difficult cases.
3. Stress-test it using small exact examples, adversarial semigroups, and computer-generated counterexamples to overly strong intermediate claims.
4. If it survives, seek a complete proof and pass its statement and dependencies to the Lean formalization agent.
5. If it fails, preserve the smallest counterexample, diagnose the invalid hypothesis, and attempt a corrected, stronger-useful formulation or a different mechanism.
6. Record the result and move to the next mathematical question. Continue.

**Do not replace this loop with repeated literature summaries, large enumerations, or final-looking explanations of known obstacles.** Literature establishes the boundary of known work; the mission is to go beyond it.

## Computation: modest and targeted

The primary bottleneck should be *mathematical ideas*, not the size of a brute-force search. Use Python/SageMath and small exact enumerators to test lemmas, generate counterexamples to proposed reductions, and discover patterns. Use SMT/ILP/Kunz-cone calculations where they directly test a mathematical hypothesis. Do not assume huge CPU/GPU workloads are necessary.

- Build two independent small-semigroup checkers when practical, computing `c`, `g`, `ell`, multiplicity, embedding dimension, Apéry set, and Wilf defect `W`.
- Test definition and boundary cases: `S = N`, two-generator semigroups, symmetric and pseudo-symmetric cases, maximal embedding dimension, small multiplicity, and examples near equality.
- Record exact integer results, tested parameter bounds, search completeness, runtimes, and seeds. No approximate arithmetic is needed for the central inequality.
- Prefer experiments that distinguish competing structural hypotheses to experiments that merely increase the largest checked genus or conductor.
- Distinguish **a proved general statement**, **an exhaustive finite range**, **a heuristic pattern**, and **a time- or memory-limited search**.
- If a computation supports a claimed universal theorem, extract an explicit symbolic argument or a checkable finite certificate and explain why it covers all cases.

## Lean 4 formalization and adversarial review

The research agent and the Lean agent serve different roles. The research agent discovers and proves on paper; the Lean agent audits statements, checks dependencies, finds omitted hypotheses, and formalizes mature results.

For each proposed lemma provide:

- Its exact original statement, with all quantifiers and edge cases.
- A complete human-readable proof and a dependency list.
- A clear explanation of how it advances the universal Wilf inequality.
- Known examples, attempted counterexamples, and proof obligations.

The formalization agent must **not silently weaken the original claim** by adding assumptions, changing strictness, restricting a range, or replacing the embedding dimension with an easier surrogate. If a repaired version is provable, report both versions and the exact difference.

Track `sorry`, added axioms, opaque external calculations, and admitted computational certificates explicitly. Only describe a theorem as Lean-verified when its exact intended statement is kernel-checked under acceptable stated axioms, without unreported gaps. The research agent should not wait for every speculative idea to be formalized; formalize foundational and high-leverage results first.

If Lean reveals a gap, feed it back to the research agent immediately. A proof failure is a research event, not merely an implementation inconvenience.

## Persistent research record

Keep the work resumable after every execution session. Maintain, at minimum:

    .research/NOTEBOOK.md        # Dated conjectures, proofs, failed claims, and new questions
    .research/STATE.md           # Current best approach, verified facts, open obligations, next action
    .research/PROOFS.md          # Precise statements, arguments, dependency graph, proof status
    .research/EXPERIMENTS.md     # Exact finite tests, parameters, counterexamples, reproducibility
    .research/LITERATURE.md      # Prior results and accurate comparison of hypotheses
    lean/                        # Lean 4/mathlib definitions, lemmas, checked proofs
    src/                         # Small semigroup enumerators, exact checkers, exploration tools
    examples/                    # Extremal families and counterexamples to intermediate conjectures

Commit or otherwise persist important changes. Do not overwrite a failed conjecture with its repaired version without preserving the correction history. Keep an explicit list of unresolved proof gaps and prevent downstream results from treating them as settled.

At each session boundary, save a **handoff** specifying (a) proved or formally checked facts; (b) conjectures and gaps; (c) experiments and how to reproduce them; (d) the three most promising active approaches; and (e) the first precise task for the next session.

## Continuation and reporting

The intended research horizon is **30 days**, within available compute, time, and financial budgets and platform execution limits. A session ending is **not** the research project ending. If an external controller must restart the agent, save a full checkpoint and handoff; do not imply work will continue automatically when the environment does not support it.

Report concise periodic progress centered on **new mathematical insights**, proof attempts, genuine counterexamples to intermediate claims, verified lemmas, and next steps. Do not repeatedly report that Wilf remains open or that existing techniques do not prove it. That is already known.

Do **not** declare the investigation complete because several approaches fail or because a universal proof has not yet emerged. Stop only on explicit instruction, exhaustion of the authorized 30-day/resource budget, or session constraints requiring a handoff. Do not claim to have exhausted the possible mathematics.

## Immediate next task

1. Formalize and cross-check the exact Wilf statement and all invariants, using two independent small examples and one boundary example to catch `c`, `g`, and `ell` convention errors.
2. Read only enough of the strongest existing theorems and standard reductions to avoid rediscovering them. Create a concise dependency map and identify the precise gaps preventing a universal proof.
3. Propose **at least five genuinely different proof strategies**, ranking them by logical leverage, falsifiability, and ability to cover the currently resistant semigroups.
4. Keep at least three strategies active. Choose the strongest new lemma or reduction and **begin trying to prove it immediately**. Send the initial precise statement to the Lean agent for adversarial review.
5. Do not finish the session by merely delivering the map or a strategic report. Start a new research cycle.

## Non-negotiable research attitude

**Do not respond with generic explanations of why Wilf's conjecture is difficult.**

Those difficulties are already familiar. **I WOULD NOT BE HERE IF IT WAS EASY.**

Your assignment is to conduct mathematical research **beyond** the current frontier.

An explanation of why an existing approach fails is an intermediate research finding, **not** the completion of the investigation.

**Identify the missing ingredient. Attempt to derive it. If that attempt fails, investigate a different mechanism.**

**Do not confuse understanding the current mathematical frontier with exhausting the mathematics beyond it.**
