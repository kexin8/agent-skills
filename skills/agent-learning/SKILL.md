---
name: agent-learning
description: Review a Coding Agent development session to prevent repeated mistakes and incomplete changes that lead to rework. Use when the user asks the agent to learn from a fix, capture conventions identified by the user or agent, or propose updates to AGENTS.md. Skip routine summaries and status reports.
---

# Agent Learning

[简体中文](SKILL.zh.md) is the Chinese edition of this skill. Use this English entry by default.

## Learn from rework and corrections

1. Start with the visible session and user-provided material. Inspect relevant project instructions, diffs, callers, or verification results when they help establish what happened. Reconstruct the original requirement, what the first attempt missed, what prompted rework, and which correction was verified. Separate observed facts from suspected causes. Look for disconfirming evidence and distinguish a skipped existing rule, a gap in the workflow, and an implementation defect. Treat recurrence as established only when the evidence shows it.
2. Turn each reusable lesson into a concrete action and a check. State when it applies, what to do before or during the change, and how to verify the original request end to end before reporting completion. For an incomplete fix, identify the missed entry point, caller, case, or acceptance criterion, and choose a check that would have caught the omission. Tie each completion claim to a check run against the final change on the affected path. When practical, verify that the regression check detects the original failure as well as passing after the fix. Report checks that were skipped or unavailable. Preserve a successful recovery step or a failed approach only when knowing it would change the next attempt.
3. Capture lasting conventions identified by either the user or the agent. Use explicit user requirements, existing authoritative project guidance, or relevant verification as evidence. An agent's suggestion or a single successful implementation does not establish a project-wide rule. Keep uncertain conventions as proposals and omit one-off instructions, raw transcripts, secrets, and lessons already enforced by the project. Weigh repeated observations and evidence against the proposed rule, keeping project-specific patterns within their scope. Before saving, ask whether someone following the current code, tests, and docs could still repeat the mistake or need to rediscover the reasoning. If those artifacts already answer it, skip the extra record.

## Route and review the proposal

- Match the remedy to what allowed the failure. Propose a regression test or automated check for mechanically detectable behavior, a runbook or Skill for a repeatable procedure, or a concise instruction for a durable project constraint that needs to be visible before work starts. If an existing rule was missed, identify why it was missed before proposing a second rule.
- Use the smallest applicable scope. Look for an equivalent rule by meaning before drafting an addition. Update the existing source when an approved change clarifies or replaces it. Check older guidance against current project evidence and propose updating stale instructions in place. Surface unresolved conflicts. Follow established decision-record practices, including `agent-notes` where the project uses it.
- A retrospective or bare skill invocation is read-only. A request to save authorizes verified lessons in appropriate existing project documentation within scope, subject to the review step below. Changes to code, tests, CI, user-level instructions, or skills require authorization for those changes.
- **Get separate human approval before changing any `AGENTS.md`.** Show the target path, exact proposed wording or diff, intended scope, and supporting evidence. Ask the user to approve that draft in a subsequent reply. Even an initial request to update `AGENTS.md` starts with this review. Leave root and nested `AGENTS.md` files untouched while approval is pending, including edits made by tools or scripts. Do not put the pending convention into effect through another instruction file.
- Apply only the approved changes. Recheck the target for conflicts with intervening edits. If the proposed wording, scope, or target needs to change substantively, show the revised draft and obtain approval again.

## Close the review

Report the observed failure or convention, the preventive action and verification, and any proposed rules awaiting approval. After writing approved changes, reread the affected files and check scope, duplication, and links. Report what was actually saved and where. When several improvements qualify, identify the one most likely to prevent another round of rework and explain how its effect can be checked on the next relevant task. If there is no reusable lesson, say so.
