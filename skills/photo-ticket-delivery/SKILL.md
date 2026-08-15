---
name: photo-ticket-delivery
description: Publish or append an exact-head amendment to a locally accepted photography-platform ticket through guarded review delivery, or complete an explicitly approved merged ticket. Use after photo-acceptance-gate returns READY_TO_PUBLISH, after a published or amended commit receives exact-head PASS, or for ticket-specific post-merge completion.
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

### Post-publication exact-head amendment

If an independently reviewed fix commit is pushed after publication and the
full acceptance gate returns `PASS` at that new exact head, append it without
replacing the original attestation:

```bash
photography-ticket-delivery amend \
  --issue <number> \
  --ticket <TICKET-ID> \
  --base <main|frontend|backend> \
  --commit <full-40-character-sha> \
  --verdict PASS
```

This is valid only in `PUBLISHED_AWAITING_FINAL_GATE`. The helper requires a
clean strict descendant with local HEAD, remote ticket branch, and open draft-PR
head all equal. Every changed path must already be in the original attested
manifest, only modifications are allowed, and the acceptance-evidence blob must
be identical. The managed comment and local state retain an append-only chain
from the original publication through every amendment. Then run `mark-review`
for the amended exact head.

## Explicitly approved post-merge completion

The post-merge coordinator may use this skill only after it receives the user's
explicit approval for the exact ticket and pull request. It first performs and
verifies the approved normal merge using high-level GitHub CLI, including proof
that the merge contains the accepted publication SHA. It then runs:

```bash
photography-ticket-delivery complete \
  --issue <number> \
  --ticket <TICKET-ID> \
  --base <main|frontend|backend> \
  --pr <merged-pr-number> \
  --approval APPROVE_CLOSE_AND_MARK_DONE
```

The helper changes its managed evidence record from draft to merged, moves the
Project item to Done, closes the app issue as completed, and verifies the
ticket branch remains available. The coordinator verifies the retained
worktree separately and then prepares, but does not execute, the next-ticket
prompt.

## Non-negotiable boundaries

- Builders edit and test. Only the orchestrator invokes `attest`, `publish`,
  `amend`, or `mark-review`; only the post-merge coordinator invokes `complete`, and only
  with exact ticket-specific user approval delegated by the orchestrator.
- Never stage or publish paths not covered by the attestation.
- Never use raw `git add`, `git commit`, `git push`, `gh pr create`,
  `gh issue comment`, `gh project item-edit`, or mutating `gh api` as a
  substitute.
- The helper itself uses only high-level GitHub CLI commands. Direct REST,
  GraphQL, `api.github.com`, and `gh api` are prohibited.
- If another owner-authored issue comment follows the managed evidence comment,
  stop before editing it: CLI-only delivery will not use a comment-ID API
  fallback. Record a new owner decision before publication, or obtain an
  explicit workflow decision if this occurs after publication.
- A changed snapshot, divergent remote branch, non-draft or ambiguous PR,
  missing evidence, unknown status, deletion, rename, copy, conflict operation,
  protected configuration, escaping symlink, active Git hook, custom push
  option, or pre-existing unpublished commit is a hard stop.
- Builders leave accepted ticket changes uncommitted. For a new remote ticket
  branch, the attested HEAD must equal `origin/<base>`; for an existing branch,
  it must equal that remote ticket head. The helper owns the next exact commit.
- Merge, issue closure, and Done status require explicit user approval. Merge
  remains outside this helper; `complete` may perform only the approved issue
  closure and Done transition after verifying the merge. Force-push, remote
  creation or mutation, branch deletion, file deletion, reset, clean, and
  history rewriting remain prohibited.
- The session may run with the owner's authorized `--auto`; do not treat the
  flag as authority beyond the exact locally allowlisted helper commands.
