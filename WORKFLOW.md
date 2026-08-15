# Local OpenCode implementation workflow

The implementation repository is `/home/rohit/photography-portfolio-platform-app`. All OpenCode configuration in this directory is local-only and excluded from the repository.

## Start

Always launch from the dedicated wrapper:

```bash
opencode-photography-app --auto
```

Do not use plain `opencode` for this project. The owner authorizes `--auto`
through the dedicated wrapper; it auto-approves permissions that are not
explicitly denied. Explicit deny rules remain enforced, and `--auto` is not
ticket-specific authorization for merge, closure, Done, deletion, force-push,
history rewriting, or Docker and volume removal.
The wrapper exports `OPENCODE_ENABLE_EXA=1`; together with the orchestrator's
`websearch: allow` permission, this makes Exa WebSearch available automatically
in every newly launched photography session.

The wrapper also launches `photography-runtime-supervisor` in a separate
background session before replacing itself with OpenCode. The companion is
bound to the exact OpenCode PID and start time, follows only descendants whose
working directories are inside the implementation repository, writes state to
`/home/rohit/.local/state/opencode-photography-app/runtime-supervisor/`, and
exits when OpenCode exits. Check it with:

```bash
photography-runtime-supervisor status
```

It automatically sends only `SIGTERM` to an exact verifier when a terminal
failure plus repeated connection refusals has lingered for at least sixty
seconds, or a terminal success/leak marker has lingered without progress for at
least five minutes, and every matching ticket container is already stopped.
It revalidates ancestry, worktree, PID, and process start time immediately
before signaling and records the proof. It selects the executable verifier leaf
instead of a shell pipeline wrapper. If that exact leaf is reparented after its
wrapper exits, it may retain ownership only when PID/start time, process group,
command, worktree, ticket, and log identity remain unchanged from its earlier
observation as an OpenCode descendant. Missing or ambiguous evidence is
alert-only. It never uses `SIGKILL`, signals OpenCode, mutates Docker, deletes a
volume, or touches Git, branches, worktrees, or evidence.

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
opencode-photography-app debug agent post-merge-coordinator
opencode-photography-app debug agent runtime-cleanup-coordinator
opencode-photography-app debug agent frontend-builder
opencode-photography-app debug agent backend-builder
photography-runtime-supervisor doctor
photography-runtime-supervisor status
photography-orchestrator-doctor validate
photography-orchestrator-doctor evaluate
```

Confirm the resolved models:

- `orchestrator`: `opencode-go/deepseek-v4-pro`, `max`
- `platform-architect`: `opencode-go/deepseek-v4-flash`, `high`
- `frontend-builder`: `opencode-go/deepseek-v4-flash`, `high`
- `backend-builder`: `opencode-go/deepseek-v4-flash`, `high`
- `privacy-security-reviewer`: `opencode-go/deepseek-v4-flash`, `high`
- `repo-scout`: `opencode-go/deepseek-v4-flash`, `high`
- `qa-accessibility-reviewer`: `opencode-go/deepseek-v4-flash`, `high`
- `post-merge-coordinator`: `opencode-go/deepseek-v4-flash`, `high`
- `runtime-cleanup-coordinator`: `opencode-go/deepseek-v4-flash`, `high`

## Permission expectations

- Some repository planning snapshots still describe commit and push as
  individually approved. The user's newer standing authorization is recorded
  here and in `AGENTS.md`; only the guarded helper receives that exception.
- The orchestrator must request approval before direct edits or non-read-only
  shell work except the publication-phase `photography-ticket-delivery`
  commands. It cannot mark a PR ready, merge, or invoke `complete`; those
  operations belong only to the post-merge coordinator after explicit
  ticket-specific approval.
- Builders can edit only inside the implementation worktree and cannot launch subagents.
- Reviewers, the architect, and the scout cannot edit.
- All agents are denied external-directory access.
- The runtime cleanup coordinator cannot edit or delegate. Inventory is
  read-only; exact process signals and Docker removals require approval, global
  prune commands are denied, and volume removal requires separate explicit
  approval. The only automatic signal is the deterministic supervisor's exact
  verifier `SIGTERM` after every high-confidence gate passes; that exception
  does not extend to any LLM agent.
- `gh api`, direct REST, and direct GraphQL are denied. GitHub reads use
  high-level `gh` commands. Direct mutating high-level CLI commands require
  approval and are reserved for explicitly authorized operations outside the
  helper's automatic ticket workflow. The guarded helper alone can perform
  automatic commit, non-force push, draft-PR creation, evidence attachment,
  and In Review, and it also uses only high-level `gh` commands.
- The integration helper cannot publish merge commits, so AUTH-02 readiness has
  one exact local exception: commit the already staged reviewed merge with
  `integration-02: synchronize backend into frontend for AUTH-02`, then
  non-force push only `INTEGRATION/backend-into-frontend-for-auth-02` with
  upstream tracking, create only its draft PR into `frontend`, poll its checks,
  and comment only on AUTH-02 #10 with readiness evidence. This is not a
  reusable ticket-publication permission and never permits the integration PR
  to be merged automatically.
- Merge, issue closure, Done, force-push, remote mutation, deletion, reset,
  clean, and history rewriting remain approval-gated. With explicit
  ticket-specific approval, `post-merge-coordinator` may mark only the named PR
  ready, perform a normal non-auto merge, prove the accepted SHA is contained,
  and invoke the guarded `complete` command. It retains the ticket branch and
  worktree and returns a prompt for, but does not start, the next ticket.
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
- `photo-runtime-cleanup`

Use ticket intake before work and the acceptance gate before publication and
again after publication. Use the domain skills only when their triggers apply.
Browser evidence uses `playwright-cli`; it complements rather than replaces
repository-owned Playwright tests. Platform engineering uses progressive
disclosure: load only the reference for the touched workspace/CI, Fastify
contract, PostGIS migration, media-worker, or observability/performance area.
Run integration readiness before dependent implementation and again before
publication. The frontend builder also treats test harness lifecycle as a hard
quality boundary: asynchronous child execution, bounded phases, live progress,
idempotent cleanup, exact resource ownership, and post-run leak checks are
required for browser, server, proxy, and container verification.

## Runtime cleanup

Every wrapper-launched session includes the background runtime supervisor. It
is deterministic rather than model-backed, so it consumes no model tokens and
continues observing while the orchestrator is synchronously waiting on a
verifier. Inspect its recorded proof before diagnosing or rerunning a failed
harness.

Delegate cleanup to `runtime-cleanup-coordinator` only after a user cleanup
request or approval of an exact leak-recovery plan. The coordinator first
inventories processes, Docker resources, Compose labels, mounts, networks, and
worktree ownership. It retains active, referenced, shared, or ambiguous
resources.

Stopping a process or container and removing a container, network, or image are
approval-gated. Persistent volume removal is a separate approval that must name
every volume and acknowledge data loss. Daemon-wide prune, Compose down, broad
process kills, filesystem deletion, Git cleanup, branch/worktree removal, and
repository edits remain denied. Revalidate every target immediately before
mutation and verify unrelated resources after cleanup.

## Local orchestrator evaluation

`photography-orchestrator-doctor validate` is a hard structural gate. It
checks the exact nine-agent roster and models, one-level delegation, one-writer
permissions, external-directory denial, skill allowlists, app-only repository
isolation, approval-gated high-level GitHub CLI mutation, direct-API denial,
helper presence, skill metadata, and reference integrity.

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

If a reviewed fix commit is pushed after publication but before `In Review`,
preserve the original attestation and append an exact-head amendment only after
the full gate passes at the new head:

```bash
photography-ticket-delivery amend \
  --issue <number> \
  --ticket <TICKET-ID> \
  --base <main|frontend|backend> \
  --commit <full-40-character-sha> \
  --verdict PASS
```

`amend` requires a clean strict descendant that exactly matches the remote
branch and open draft-PR head. Its delta may only modify paths in the original
manifest, may not add, delete, copy, or rename, and must preserve the exact
acceptance-evidence blob. It appends both commits and immutable evidence URLs to
the managed evidence record; it never replaces the original history.

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

After an In Review handoff, start a separate approval turn. Only when the user
explicitly approves merge and completion for that exact ticket, delegate to
`post-merge-coordinator`. It verifies and merges the PR before running:

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
acceptance gate and continue with `mark-review`, using `amend` first only when a
new reviewed exact head exists. If it is `IN_REVIEW`, verify and report the
existing handoff.

The helper refuses pre-staged or changed-after-attestation work, deletions,
renames, copies, protected local configuration, escaping symlinks, divergent
remote branches, active Git hooks, custom push options, pre-existing unpublished
commits, ambiguous or non-draft PRs, and unknown Project states. Builders leave
accepted changes uncommitted so the helper owns the exact publication commit.
Because high-level `gh issue comment --edit-last` is the only identity-safe CLI
edit operation, the helper also stops if its managed evidence comment is no
longer the authenticated owner's latest comment; it never falls back to an API
edit by comment ID.
It never merges, force-pushes, changes remotes, or deletes. Its separate
post-merge completion command closes and marks Done only with the exact explicit
approval token after verifying the merged PR and retained branch.

No MCP server is enabled initially. Add one only when a concrete ticket needs capabilities that the local skills, GitHub CLI, and repository tooling cannot provide, and grant only the required tools.

OpenCode permissions are workflow controls, not an operating-system sandbox. Verify Git status and remotes before and after every session.
