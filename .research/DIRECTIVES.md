# DIRECTIVES.md — the user's standing orders

Hooks inject this file at every session start, resume and compaction. Read it before doing anything. It overrides the
historical notes and any compaction summary. Then read [STATE.md](STATE.md), the single current handoff.

## Goal
A proof of Wilf's inequality e·ℓ ≥ c for EVERY numerical semigroup. Nothing else counts as progress.

## Hard rules
1. **Scope line before any target.** Write it in `.research/SCOPE.md`:
   "Proves Wilf for: ___. Proved reduction from all S to this case: yes (cite) / none."
   If the answer is "none", do not start. Tell the user and ask.
2. **Proposals get a scope line first.** When the user or the advisor proposes a direction, my first reply states its
   scope line. I never endorse a sub-case without saying whether it reduces to all S.
3. **No subagents** (Agent tool, codex, workflows, anything else) unless the user approves that specific launch in
   chat. A hook makes every launch prompt the user.
4. **Wait means wait.** If I said I would wait, I do nothing until the user explicitly says go. A question or a
   complaint is not a go.
5. **No compute without an approved target.**
   - Compute needs `ACTIVE: yes` in SCOPE.md, with an approval quote taken verbatim from the user's own message.
   - The hook checks the quote against the log of user prompts. Background launches also prompt the user.
   - Prefer fejer. User authorized laptop calculations in the current Codex conversation if fejer cannot run:
     "if that doesnt work perform the calculations on my laptop". Give an ETA at launch.
   - Stop jobs on any line that loses relevance.
6. **Checkpoints.** Report to the user after every real result, and at least every 30–45 minutes. A hook reminds me
   every 30 minutes. Logging something in .research/ does not count as telling the user.
7. **Push right after every commit.** A Stop hook blocks stopping while commits are unpushed. Before committing, run
   `git reset -q CLAUDE.md .claude`.
8. **Check before working on any case.**
   - Search the literature: arXiv, GitHub, preprint servers, conjectures.io.
   - Grep PROOFS / LITERATURE / FAILED for the same statement.
9. **No manuscripts or write-ups unless asked.** Dates come from `date` (local time, EDT).
10. **Never trust a compaction summary for what the user ordered or approved.** When it matters, read the user's own
    messages in the transcript (`~/.claude/projects/<project>/<session>.jsonl`).

## Work backwards and reuse the existing C implementations
The user confirmed the work-backwards requirement in the current Codex conversation and expressed this preference:
> ideally c or cpp since its faster thang gurobi, i think the repo already have a c or cpp version unless im mistaken

Use genuine semigroups with small actual W and difficult certificate margins to identify tight constraints;
optimize admissible splitting weights and obtain exact dual obstructions when the certificate framework fails.
Extract a parameter-independent lemma with a complete proof and an explicit implication chain to full Wilf.
Prefer existing C/C++ search and checking code; retain solver-based weight optimization where needed.
The implementation inventory, current status and next action are maintained only in [STATE.md](STATE.md).
The C preference does not activate a target or authorize compute, agents or a different research strategy.

## Current research directive
2026-10-23: the user STOPPED the transport/Hall/cofactor/GPU programme and paused
its earlier autonomous goal. Those auxiliary programmes remain suspended.

2026-10-24 00:34 EDT: the user created a NEW ACTIVE goal, explicitly ordering
continued work ONLY on the universal argument. The exact approval is in SCOPE.md.
This revokes the paused status for the main research objective, but does not
revive the stopped programmes, agent permissions or numerical campaigns.

The user's subsequent direct instruction is:
> Change the mathematical priority.
> The central target must be the actual Wilf number, not the positivity of a stronger auxiliary bound such as \(Q\).

Current direct task: attack the EXACT Apéry mean/maximum inequality through the
costed cyclic reachability sets A_t={r:w_r<=t}, retaining actual generator costs,
residue congruences and the full cumulative area. Scope/authorization is in SCOPE.md;
STATE.md remains the single handoff/inventory. Old transport, Hall, cofactor,
protected-prefix and GPU programmes are SUSPENDED, not automatic next steps.
No new numerical campaign, worker launch or background job follows from a paper
identity. The earlier backwards/C preference is used only within this actual-W
priority and does not activate the suspended programmes.

For reference, the last research directions the user gave or approved:
- 2026-10-20 23:13 EDT. Backward strategy: an exact Kunz MILP in Gurobi minimizing W; the height-3 obstruction first;
  optimize the splitting weights (primal and dual); extract a lemma with a complete proof.
- 2026-10-21 01:04 EDT. Advisor steps 1 and 2: an adversarial RT2/UA2 search at heights 4–5, and a height-3 RT2
  theorem.
- 2026-10-21 02:46–12:12 EDT. Advisor proposals approved by the user:
  - q = 5 counting;
  - TRUNC₃ ("Go ahead with your revised order", 04:44);
  - PAY2 ("Make sure its documented, then GO", 12:12).
  These are Q5-only. No reduction connects them to all S.
