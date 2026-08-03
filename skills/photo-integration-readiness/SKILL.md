---
name: photo-integration-readiness
description: Assess photography-platform ticket branches, integration branches, dependency commits, pull requests, and exact review ranges without merging or rewriting history. Use before starting a dependent ticket, before implementation after a branch handoff, before publication, after an integration branch advances, or when main, frontend, backend, and ticket branches may have drifted.
---

# Photo integration readiness

Prove that the selected ticket is based on the correct integration state. This is a read-only decision gate, not authorization to merge, rebase, cherry-pick, push, delete, or change remotes.

## Workflow

1. Resolve the ticket's authoritative integration branch and formal dependencies from the app issue and Project.
2. Verify the repository path and "origin" refer only to "Rohit22014/photography-portfolio-platform-app". Stop on any planning-repository reference or unexpected remote.
3. Record the current branch, clean/dirty state, full "HEAD", remote ticket head when present, and current integration-branch head. Fetching remote refs requires the existing command approval; never broaden permissions to make this automatic.
4. Prove every required dependency commit is an ancestor of the candidate integration branch or record the accepted PR/merge evidence that establishes it.
5. Calculate ahead/behind and the exact range with merge-base, rev-list, log, and diff. Inspect changed paths, generated outputs, migrations, contracts, and cross-lane effects.
6. Check for an existing pull request and confirm its head, base, draft state, issue link, and accepted evidence SHA agree with the candidate.
7. If the base advanced, rerun affected checks against the new exact range. The assigned builder resolves integration conflicts; reviewers remain read-only.
8. Return one verdict with commands and immutable identifiers.

Useful read-only commands include:

    git status --short
    git remote -v
    git rev-parse HEAD
    git merge-base origin/<base> HEAD
    git merge-base --is-ancestor <dependency-sha> HEAD
    git rev-list --left-right --count origin/<base>...HEAD
    git diff --name-status origin/<base>...HEAD
    gh pr view <number> --repo Rohit22014/photography-portfolio-platform-app --json baseRefName,headRefName,isDraft,mergeStateStatus,statusCheckRollup,url

## Verdicts

- "READY": correct repository and base, all dependencies present, exact range known, no unexplained drift, and required checks pass.
- "STALE": the correct base advanced or dependency evidence changed; return the exact builder action and checks to rerun.
- "DIVERGED": local, remote, PR, evidence, or integration histories disagree and require an explicit integration decision.
- "BLOCKED": authentication, remote state, dependency merge, accepted ADR, or authoritative metadata is unavailable.

Report repository, branch, full SHAs, ahead/behind, dependency ancestry, PR state, changed paths, cross-lane effects, checks, and next safe action. Never report "READY" from stale local refs without labeling that limitation.
