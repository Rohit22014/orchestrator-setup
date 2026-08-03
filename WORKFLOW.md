# Local OpenCode implementation workflow

The implementation repository is `/home/rohit/photography-portfolio-platform-app`. All OpenCode configuration in this directory is local-only and excluded from the repository.

## Start

Always launch from the dedicated wrapper:

```bash
opencode-photography-app
```

Do not use plain `opencode` for this project and do not pass `--auto`.

Before starting a ticket that reads the private roadmap, verify GitHub authentication:

```bash
gh auth status
```

If it fails, run `gh auth login -h github.com` interactively before continuing.
Full delivery requires the Project write scope:

```bash
gh auth refresh -h github.com -s project
```

The first implementation run can be started non-interactively with:

```bash
opencode-photography-app run --agent orchestrator \
  "Begin delivery of the complete 44-ticket photography platform. Select exactly one dependency-ready ticket, verify its authoritative metadata and integration readiness, delegate read-only analysis, load only applicable platform-engineering references, assign exactly one builder, run applicable independent reviews, address findings, and apply both acceptance gates. On READY_TO_PUBLISH use the guarded ticket-delivery helper to commit, non-force push, create a draft PR, and attach evidence. Rerun integration readiness and acceptance against the published SHA; on PASS move the ticket to In Review. Never merge, close an issue, force-push, change a remote, delete, or mark Done. Stop after the ticket handoff."
```

Each later run should name one dependency-ready ticket. The full project remains the objective even though each implementation session stays ticket-sized.

## Verify configuration and models

```bash
jq -e /home/rohit/.config/opencode/photography-portfolio-platform-app/opencode.json
opencode-photography-app debug config
opencode-photography-app agent list
opencode-photography-app debug agent orchestrator
opencode-photography-app debug agent frontend-builder
opencode-photography-app debug agent backend-builder
photography-orchestrator-doctor validate
photography-orchestrator-doctor evaluate
```

Confirm the resolved models:

- `orchestrator`: `openai/gpt-5.6-sol`, `xhigh`
- `platform-architect`: `openai/gpt-5.6-terra`, `xhigh`
- `frontend-builder`: `openai/gpt-5.6-terra`, `high`
- `backend-builder`: `openai/gpt-5.6-terra`, `high`
- `privacy-security-reviewer`: `openai/gpt-5.6-terra`, `xhigh`
- `repo-scout`: `openai/gpt-5.6-luna`, `low`
- `qa-accessibility-reviewer`: `openai/gpt-5.6-luna`, `high`

## Permission expectations

- Some repository planning snapshots still describe commit and push as
  individually approved. The user's newer standing authorization is recorded
  here and in `AGENTS.md`; only the guarded helper receives that exception.
- The orchestrator must request approval before direct edits or non-read-only
  shell work except the six exact `photography-ticket-delivery` commands.
- Builders can edit only inside the implementation worktree and cannot launch subagents.
- Reviewers, the architect, and the scout cannot edit.
- All agents are denied external-directory access.
- Raw commit, push, PR creation, issue-comment, Project-write, and mutating API
  commands are denied. The guarded helper alone can perform automatic commit,
  non-force push, draft-PR creation, evidence attachment, and In Review.
- Merge, issue closure, Done, force-push, remote mutation, deletion, reset,
  clean, and history rewriting remain approval-gated. The guarded `complete`
  command may close and mark Done only after explicit ticket-specific approval;
  it never merges or deletes the retained ticket branch.
- Sharing is disabled.
- As repository-owned test commands are introduced, add exact builder and QA allowlist entries ticket by ticket; do not replace them with a broad shell wildcard.

## Quality skills

The external configuration provides:

- `photo-ticket-intake`
- `photo-acceptance-gate`
- `photo-privacy-review`
- `photo-browser-evidence`
- `photo-adr-contract`
- `photo-ticket-delivery`
- `photo-platform-engineering`
- `photo-integration-readiness`
- `photo-orchestrator-evaluation`

Use ticket intake before work and the acceptance gate before publication and
again after publication. Use the domain skills only when their triggers apply.
Browser evidence uses `playwright-cli`; it complements rather than replaces
repository-owned Playwright tests. Platform engineering uses progressive
disclosure: load only the reference for the touched workspace/CI, Fastify
contract, PostGIS migration, media-worker, or observability/performance area.
Run integration readiness before dependent implementation and again before
publication.

## Local orchestrator evaluation

`photography-orchestrator-doctor validate` is a hard structural gate. It
checks the exact seven-agent roster and models, one-level delegation, one-writer
permissions, external-directory denial, skill allowlists, app-only repository
isolation, raw mutation denial, helper presence, skill metadata, and reference
integrity.

`photography-orchestrator-doctor evaluate` produces a deterministic skill
quality score for trigger precision, context size, procedure, verification,
safety, references, and UI metadata. Treat scores as maintenance signals, not
ticket acceptance evidence. After an OpenCode upgrade, also run the resolved
agent/model commands above and a read-only scout delegation because static
configuration cannot prove runtime provider behavior.

## Ticket-to-draft-PR handoff

The helper is intentionally two-phase so a local verdict cannot certify links
or remote state that do not yet exist.

Run every helper command from the ticket's registered implementation-repository
worktree. The helper resolves that worktree from the invocation directory and
uses the repository's shared Git directory for attestations and locking. It
rejects Git environment overrides and worktrees from any other repository. An
invocation outside Git retains the canonical primary-worktree default.

```bash
photography-ticket-delivery doctor
photography-ticket-delivery status --issue <number>

photography-ticket-delivery attest \
  --issue <number> \
  --ticket <TICKET-ID> \
  --base <main|frontend|backend> \
  --evidence <relative-evidence-file> \
  --path <relative-change-area> \
  --gate READY_TO_PUBLISH

photography-ticket-delivery publish \
  --issue <number> \
  --ticket <TICKET-ID> \
  --base <main|frontend|backend>
```

After publication, rerun all acceptance checks against the full SHA and
immutable evidence URLs. Only then:

```bash
photography-ticket-delivery mark-review \
  --issue <number> \
  --ticket <TICKET-ID> \
  --base <main|frontend|backend> \
  --commit <full-40-character-sha> \
  --verdict PASS
```

After the user merges the PR, start a separate approval turn. Only when the
user explicitly approves completion for that exact ticket:

```bash
photography-ticket-delivery complete \
  --issue <number> \
  --ticket <TICKET-ID> \
  --base <main|frontend|backend> \
  --pr <merged-pr-number> \
  --approval APPROVE_CLOSE_AND_MARK_DONE
```

This verifies the merged PR against the accepted publication commit, changes
the managed evidence record from draft to merged, moves the Project item from
In Review to Done, closes the app issue as completed, and verifies that the
ticket branch remains available. It is idempotent and must not be called merely
because a merge is visible.

When resuming, start with `photography-ticket-delivery status --issue
<number>`. If the attestation phase is `COMMITTED_AWAITING_PUBLICATION`, rerun
`publish` to complete the same guarded commit. If it is
`PUBLISHED_AWAITING_FINAL_GATE`, do not attest; rerun the post-publication
acceptance gate and continue with `mark-review`. If it is `IN_REVIEW`, verify
and report the existing handoff.

The helper refuses pre-staged or changed-after-attestation work, deletions,
renames, copies, protected local configuration, escaping symlinks, divergent
remote branches, active Git hooks, custom push options, pre-existing unpublished
commits, ambiguous or non-draft PRs, and unknown Project states. Builders leave
accepted changes uncommitted so the helper owns the exact publication commit.
It never merges, force-pushes, changes remotes, or deletes. Its separate
post-merge completion command closes and marks Done only with the exact explicit
approval token after verifying the merged PR and retained branch.

No MCP server is enabled initially. Add one only when a concrete ticket needs capabilities that the local skills, GitHub CLI, and repository tooling cannot provide, and grant only the required tools.

OpenCode permissions are workflow controls, not an operating-system sandbox. Verify Git status and remotes before and after every session.
