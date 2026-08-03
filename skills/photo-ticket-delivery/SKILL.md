---
name: photo-ticket-delivery
description: Publish a locally accepted photography-platform ticket through a guarded commit, non-force push, draft pull request, immutable evidence comment, and In Review transition. Use only after photo-acceptance-gate returns READY_TO_PUBLISH, and again after the published commit receives an exact-head PASS.
---

# Photo Ticket Delivery

Publish through `photography-ticket-delivery`; do not reproduce its GitHub or Git
mutations with raw commands. The helper is bound exclusively to the independent
application repository for source, tickets, and evidence, plus the private
GitHub Project. It must never read or mutate the planning repository.

Invoke the helper from the ticket's active Git worktree. It accepts the canonical
application checkout and registered linked worktrees that share its common Git
directory; an invocation from outside Git falls back to the canonical checkout.
It rejects another repository, an unregistered worktree, and Git directory,
worktree, index, namespace, or object-store environment overrides. Delivery
attestations and the process lock live in the shared Git directory, while file,
branch, status, staging, commit, and hook checks use the selected worktree.

## Required sequence

1. Run the local acceptance gate. Continue only on `READY_TO_PUBLISH`.
   `FAIL` and `BLOCKED` stop delivery.
2. Inspect the live guardrails:

   ```bash
   photography-ticket-delivery doctor
   photography-ticket-delivery status --issue <number>
   ```

3. Bind the verdict to the exact worktree snapshot. List each intended file or
   directory as a separate `--path`. Do not use the repository root:

   ```bash
   photography-ticket-delivery attest \
     --issue <number> \
     --ticket <TICKET-ID> \
     --base <main|frontend|backend> \
     --evidence <relative-evidence-file> \
     --path <relative-change-area> \
     --gate READY_TO_PUBLISH
   ```

   `--title` and `--commit-message` are optional. Omit `--path` only when
   adopting an already clean, already committed ticket.

4. Publish the attested snapshot:

   ```bash
   photography-ticket-delivery publish \
     --issue <number> \
     --ticket <TICKET-ID> \
     --base <main|frontend|backend>
   ```

   The helper stages only the attested paths, creates at most one normal commit,
   performs an explicit non-force push, creates or reuses one matching draft PR,
   and creates or updates one stable evidence comment. It deliberately leaves
   the Project status unchanged.

5. Rerun every acceptance check against the exact published SHA and immutable
   evidence URLs. Continue only when `photo-acceptance-gate` returns `PASS`.
   When resuming a session, run `status --issue <number>` first. If its
   attestation phase is `COMMITTED_AWAITING_PUBLICATION`, rerun `publish` to
   finish the same exact commit. If it is `PUBLISHED_AWAITING_FINAL_GATE`, do
   not attest; resume at this post-publication gate.
6. Move that exact published SHA to review:

   ```bash
   photography-ticket-delivery mark-review \
     --issue <number> \
     --ticket <TICKET-ID> \
     --base <main|frontend|backend> \
     --commit <full-40-character-sha> \
     --verdict PASS
   ```

7. Report the draft PR, evidence-comment URL, exact commit, checks, and current
   Project status. Stop; do not begin another ticket in the same session.

## Non-negotiable boundaries

- Builders edit and test; only the orchestrator invokes this delivery helper.
- Never stage or publish paths not covered by the attestation.
- Never use raw `git add`, `git commit`, `git push`, `gh pr create`,
  `gh issue comment`, `gh project item-edit`, or mutating `gh api` as a
  substitute.
- A changed snapshot, divergent remote branch, non-draft or ambiguous PR,
  missing evidence, unknown status, deletion, rename, copy, conflict operation,
  protected configuration, escaping symlink, active Git hook, custom push
  option, or pre-existing unpublished commit is a hard stop.
- Builders leave accepted ticket changes uncommitted. For a new remote ticket
  branch, the attested HEAD must equal `origin/<base>`; for an existing branch,
  it must equal that remote ticket head. The helper owns the next exact commit.
- Merge, issue closure, Done status, force-push, remote creation or mutation,
  branch deletion, file deletion, reset, clean, and history rewriting always
  require explicit user approval and are outside this helper.
- Do not use `--auto`; the exact helper commands are locally allowlisted.
