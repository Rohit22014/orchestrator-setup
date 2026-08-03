---
name: photo-acceptance-gate
description: Prove a photography-platform ticket meets every acceptance criterion before guarded publication or review. Use after implementation, after review fixes, after draft-PR publication, before claiming success, or whenever tests, links, evidence, privacy checks, or criterion traceability may be incomplete.
---

# Photo acceptance gate

Reject unsupported completion claims. Treat missing evidence as incomplete work.

## Workflow

1. Load the authoritative issue body and project fields read-only from
   `Rohit22014/photography-portfolio-platform-app`, then copy every criterion
   into a traceability table. Never read or mutate issues in the planning
   repository. A local issue snapshot may guide offline work but remains
   provisional until it is revalidated against the app repository on GitHub.
2. Inventory all work, including untracked files:

   ```text
   git status --short
   git diff
   git diff --cached
   git diff --check
   git ls-files --others --exclude-standard
   ```

   `git diff --check` does not inspect untracked files. Check each untracked candidate without staging it, for example with `git diff --no-index --check /dev/null <path>`; exit status `1` means a normal added-file diff, while whitespace diagnostics mean failure.
3. Resolve the ticket's authoritative integration branch from the Project. Fetch
   it, require it to be an ancestor of the candidate SHA, and inspect the exact
   review range even when the worktree is clean:

   ```text
   git fetch --no-tags origin <base>
   git merge-base --is-ancestor origin/<base> <candidate-sha>
   git diff --check origin/<base>...<candidate-sha>
   git diff --stat origin/<base>...<candidate-sha>
   git diff --name-status origin/<base>...<candidate-sha>
   git diff --name-only origin/<base>...<candidate-sha>
   ```

   Treat a deletion, unexpected rename/copy, protected local configuration, or
   file outside the ticket scope as a failure. For post-publication review, the
   candidate must be the full remote draft-PR head SHA, not an abbreviated or
   local-only reference.
4. Read every file in both the exact integration-branch range and the
   worktree/staged/untracked inventory. Identify the focused verification
   commands documented by the ticket or repository.
5. Run every safe, relevant automated check. Do not replace a failing command with a weaker command or silently omit it.
6. For UX-01, include `node scripts/verify-ux-01.mjs` and verify all referenced local resources exist.
7. Check:
   - broken links and missing assets;
   - lint, formatting, types, unit, integration, browser, accessibility, and contract checks where available;
   - privacy and authorization regressions;
   - generated contracts, migrations, documentation, observability, rollback notes, and runbooks where applicable;
   - deterministic synthetic fixtures and absence of secrets or private data.
8. Separate automated evidence from manual evidence. Never claim screen-reader, keyboard, visual, performance, or production-like evidence that was not actually collected.
9. Map each criterion to an artifact, command result, and manual observation.
10. For documentation or design tickets, interpret `production-like` as the issue-defined deterministic review environment, commands, headers, fixtures, viewport states, and interaction paths—not a deployed production runtime.
11. When a criterion requires linked follow-up issues, require resolvable GitHub issue URLs or recorded GitHub relationships. Plain ticket identifiers provide traceability but do not prove linkage.
12. Before publication, verify that the evidence artifact is among the exact
    intended change paths and that every substantive criterion already passes.
    The only permitted remaining gap for `READY_TO_PUBLISH` is the criterion
    requiring evidence to be attached to an issue or pull request.
13. After `photo-ticket-delivery` publishes, rerun the complete gate against the
    exact remote SHA, open draft PR, immutable evidence link, and stable issue
    comment. Do not reuse a pre-publication verdict.
14. Evidence comments and the Project transition to `In Review` are authorized
    only through `photography-ticket-delivery`. Merge, issue closure, `Done`,
    force-push, remote mutation, and deletion remain approval-gated.

Use this traceability shape:

| Criterion (verbatim) | Artifact or contract | Automated evidence | Manual evidence | Result |
|---|---|---|---|---|

## Independent review matrix

Before the final verdict, the orchestrator records which independent reviews
apply. Architecture review covers package direction, serialized contracts,
migrations, compatibility, rollback, and operability. Privacy/security review
covers authorization and protected-data flows. QA/accessibility review covers
acceptance coverage, regressions, user journeys, WCAG behavior, and evidence
limitations. Production engineering review loads only the applicable
`photo-platform-engineering` reference.

Give each reviewer the authoritative criteria, decision-complete brief, exact
diff or candidate SHA, and raw evidence without another reviewer's conclusions.
Reviewers report independently and never edit. Reconcile duplicate or
conflicting findings explicitly, then have the single assigned builder address
accepted findings before rerunning this complete gate.

## Verdict

Return:

- `PASS` only when every criterion has adequate evidence, all required checks
  pass, and the result is verified against the exact published draft-PR SHA;
- `READY_TO_PUBLISH` only when every substantive criterion and required local
  check passes and the sole remaining gap is attaching that already-tracked
  evidence through the guarded draft-PR workflow;
- `FAIL` when an implementation, artifact, or required check is concretely wrong;
- `BLOCKED` when no concrete implementation failure is known but required access, approval, environment, decision, or manual evidence is unavailable.

When both apply, return `FAIL` and list the independent blockers separately. An unavailable optional check is not a blocker; a required check without evidence is.

For `READY_TO_PUBLISH`, list the exact issue, ticket, integration branch,
evidence file, intended path manifest, current full SHA, and every verification
command. This makes the publication attestation decision-complete.

List the exact failing criterion, evidence gap, reproduction command, and
responsible builder action. Do not publish, merge, mark complete, or advance to
another ticket on `FAIL` or `BLOCKED`. Do not move to `In Review` on
`READY_TO_PUBLISH`; publish first, rerun this gate, and require `PASS`.
