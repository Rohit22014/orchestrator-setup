# Photography Portfolio OpenCode Orchestrator

This private repository version-controls the local OpenCode orchestration setup used to deliver the photography portfolio platform. It contains the primary orchestrator, specialist agents, reusable skills, guarded GitHub delivery tooling, deterministic runtime supervision, and validation tests.

The setup is deliberately separate from the application repository. Install it under the local OpenCode configuration directory and launch it through the dedicated wrapper; never copy these files into the application or planning repositories.

## What this repository provides

- A primary orchestrator that owns ticket selection, delegation, acceptance, and publication.
- Eight narrowly scoped subagents for architecture, implementation, review, post-merge completion, repository orientation, and runtime cleanup.
- Ten reusable skills covering ticket intake, ADR decisions, privacy, browser evidence, platform engineering, integration readiness, acceptance, delivery, evaluation, and runtime cleanup.
- A guarded ticket-delivery helper that owns commits, non-force pushes, draft pull requests, immutable evidence, amendments, review transitions, and explicitly approved completion.
- A deterministic runtime supervisor that detects narrowly proven lingering verifier processes without granting an LLM broad process-control authority.
- A dedicated launcher that binds OpenCode to the correct configuration and application checkout.
- Structural validation, static skill evaluation, and regression tests for the delivery helper.

## Repository boundaries

Three locations have distinct responsibilities:

| Location | Purpose | May contain orchestrator configuration? |
| --- | --- | --- |
| `/home/rohit/orchestrator-setup` | Private, version-controlled source for this setup | Yes |
| `/home/rohit/.config/opencode/photography-portfolio-platform-app` | Installed local OpenCode configuration | Yes |
| `/home/rohit/photography-portfolio-platform-app` | Application implementation repository | No |
| `/home/rohit/photography-portfolio-platform` | Planning-only repository | No; never access it from this workflow |

The authoritative GitHub issue and Project repository is `Rohit22014/photography-portfolio-platform-app`. Ticket automation must never read from or mutate the planning repository.

## Directory layout

```text
orchestrator-setup/
├── AGENTS.md
├── WORKFLOW.md
├── opencode.json
├── package.json
├── agents/
│   ├── orchestrator.md
│   ├── backend-builder.md
│   ├── frontend-builder.md
│   ├── platform-architect.md
│   ├── post-merge-coordinator.md
│   ├── privacy-security-reviewer.md
│   ├── qa-accessibility-reviewer.md
│   ├── repo-scout.md
│   └── runtime-cleanup-coordinator.md
├── skills/
│   ├── photo-acceptance-gate/
│   ├── photo-adr-contract/
│   ├── photo-browser-evidence/
│   ├── photo-integration-readiness/
│   ├── photo-orchestrator-evaluation/
│   ├── photo-platform-engineering/
│   ├── photo-privacy-review/
│   ├── photo-runtime-cleanup/
│   ├── photo-ticket-delivery/
│   └── photo-ticket-intake/
├── bin/
│   ├── opencode-photography-app
│   ├── photography-orchestrator-doctor
│   ├── photography-runtime-supervisor
│   └── photography-ticket-delivery
└── tests/
    └── test_photography_ticket_delivery.py
```

`NEXT-TICKET.md` is intentionally absent. It is a local, replaceable handoff generated from live Project state and must not be treated as durable repository configuration.

## Prerequisites

The current setup assumes:

- Linux or WSL with Bash.
- Git.
- Node.js and npm.
- Python 3.12 or a compatible Python 3 release.
- Docker with Compose support for application runtime gates.
- `jq`, `rsync`, and standard process-inspection utilities.
- GitHub CLI authenticated as an account that can access the private application repository and Project.
- OpenCode installed at `/home/rohit/.npm-global/bin/opencode`.
- The application checkout at `/home/rohit/photography-portfolio-platform-app`.

Verify GitHub authentication and Project scope:

```bash
gh auth status
gh auth refresh -h github.com -s project
```

The scripts are intentionally path-bound to the current account and checkout. If either location changes, update the wrapper, configuration instruction paths, helper constants, tests, and doctor expectations together, then rerun every validation gate.

## Installation

Clone the private setup repository:

```bash
git clone https://github.com/Rohit22014/orchestrator-setup.git /home/rohit/orchestrator-setup
cd /home/rohit/orchestrator-setup
```

Install the OpenCode configuration outside the application repository:

```bash
orchestrator_source=/home/rohit/orchestrator-setup
orchestrator_config=/home/rohit/.config/opencode/photography-portfolio-platform-app

install -d -m 700 "${orchestrator_config}"
rsync -a "${orchestrator_source}/agents" "${orchestrator_config}/"
rsync -a "${orchestrator_source}/skills" "${orchestrator_config}/"
install -m 0644 "${orchestrator_source}/AGENTS.md" "${orchestrator_config}/AGENTS.md"
install -m 0644 "${orchestrator_source}/WORKFLOW.md" "${orchestrator_config}/WORKFLOW.md"
install -m 0644 "${orchestrator_source}/opencode.json" "${orchestrator_config}/opencode.json"
install -m 0644 "${orchestrator_source}/package.json" "${orchestrator_config}/package.json"
```

Install the executable helpers:

```bash
install -d -m 755 /home/rohit/.local/bin
install -m 0755 bin/opencode-photography-app /home/rohit/.local/bin/opencode-photography-app
install -m 0755 bin/photography-orchestrator-doctor /home/rohit/.local/bin/photography-orchestrator-doctor
install -m 0755 bin/photography-runtime-supervisor /home/rohit/.local/bin/photography-runtime-supervisor
install -m 0755 bin/photography-ticket-delivery /home/rohit/.local/bin/photography-ticket-delivery
```

Install the OpenCode plugin dependency locally:

```bash
cd /home/rohit/.config/opencode/photography-portfolio-platform-app
npm install
```

Do not install `node_modules`, lockfiles, logs, runtime state, or `NEXT-TICKET.md` into this source repository as part of the deployment process.

## Starting OpenCode

Always use the dedicated wrapper:

```bash
opencode-photography-app --auto
```

Resume the most recent session with:

```bash
opencode-photography-app --auto --continue
```

The wrapper:

1. Confirms the application checkout exists.
2. Exports `OPENCODE_CONFIG` and `OPENCODE_CONFIG_DIR`.
3. Enables Exa-backed WebSearch with `OPENCODE_ENABLE_EXA=1`.
4. Starts the deterministic runtime supervisor in a separate session.
5. Changes to the application repository.
6. Replaces itself with OpenCode.

`--auto` approves operations whose configuration is `ask`; it does not override explicit denies and does not authorize merge, closure, Project Done, deletion, force-push, history rewriting, or Docker and volume removal.

## Agent topology

OpenCode permits one level of delegation. The primary orchestrator can delegate to specialists; specialists cannot recursively create more agents.

| Agent | Mode | Model | Reasoning | Responsibility | Writes? |
| --- | --- | --- | --- | --- | --- |
| `orchestrator` | Primary | `opencode-go/deepseek-v4-pro` | `max` | Ticket selection, decisions, delegation, acceptance, publication | Only guarded orchestration actions |
| `platform-architect` | Subagent | `opencode-go/deepseek-v4-flash` | `high` | Architecture, boundaries, ADR and contract analysis | No |
| `backend-builder` | Subagent | `opencode-go/deepseek-v4-flash` | `high` | Backend, data, media, platform implementation | Yes, sole writer when assigned |
| `frontend-builder` | Subagent | `opencode-go/deepseek-v4-flash` | `high` | Web, UI, accessibility, SEO, Globe and lightbox implementation | Yes, sole writer when assigned |
| `privacy-security-reviewer` | Subagent | `opencode-go/deepseek-v4-flash` | `high` | Privacy, authorization, protected media and metadata review | No |
| `qa-accessibility-reviewer` | Subagent | `opencode-go/deepseek-v4-flash` | `high` | Acceptance, regression and accessibility review | No |
| `repo-scout` | Subagent | `opencode-go/deepseek-v4-flash` | `high` | Read-only repository orientation and evidence discovery | No |
| `post-merge-coordinator` | Subagent | `opencode-go/deepseek-v4-flash` | `high` | Explicitly approved normal merge, completion and next-ticket prompt | Guarded GitHub actions only |
| `runtime-cleanup-coordinator` | Subagent | `opencode-go/deepseek-v4-flash` | `high` | Read-only inventory and explicitly approved exact cleanup | No repository writes |

Exactly one builder owns all writes in a ticket worktree. Architects and reviewers remain independent and read-only. Accepted findings return to the same builder for correction.

## Skills

| Skill | Purpose |
| --- | --- |
| `photo-ticket-intake` | Capture authoritative issue, Project, milestone, lane and dependency state before work |
| `photo-integration-readiness` | Prove base, branch, PR and dependency ancestry without rewriting history |
| `photo-adr-contract` | Surface and record material owner decisions before implementation |
| `photo-platform-engineering` | Load only domain-relevant engineering references |
| `photo-privacy-review` | Apply protected-data, EXIF/GPS and public-projection constraints |
| `photo-browser-evidence` | Collect browser and accessibility evidence for Web tickets |
| `photo-acceptance-gate` | Map implementation and evidence to every issue criterion |
| `photo-ticket-delivery` | Publish, amend, mark review, and complete through guarded state transitions |
| `photo-runtime-cleanup` | Inventory ownership and execute only explicitly approved exact cleanup |
| `photo-orchestrator-evaluation` | Validate skill quality and orchestration configuration |

Skills are progressively disclosed. Load only the skills and reference files required by the current ticket.

## Ticket lifecycle

The workflow delivers one dependency-ready ticket at a time:

```text
Todo
  -> authoritative intake and dependency proof
  -> owner decisions and decision-complete brief
  -> one builder implements
  -> independent architecture, privacy/security and QA reviews
  -> builder addresses findings
  -> local acceptance: READY_TO_PUBLISH
  -> guarded commit, non-force push and draft PR
  -> exact-head acceptance: PASS
  -> In Review
  -> separate owner-approved normal merge
  -> guarded evidence update, issue closure and Project Done
  -> next-ticket prompt only
```

The orchestrator stops at the draft-PR `In Review` boundary. Merge and completion require a later request naming the exact ticket and pull request.

## Guarded ticket delivery

Run the helper only from the application repository or a registered application worktree.

Inspect readiness:

```bash
photography-ticket-delivery doctor
photography-ticket-delivery status --issue <issue-number>
```

Bind an accepted local snapshot:

```bash
photography-ticket-delivery attest \
  --issue <issue-number> \
  --ticket <TICKET-ID> \
  --base <main|frontend|backend> \
  --evidence <relative-evidence-path> \
  --path <first-intended-path> \
  --path <second-intended-path> \
  --gate READY_TO_PUBLISH
```

Publish the attested snapshot:

```bash
photography-ticket-delivery publish \
  --issue <issue-number> \
  --ticket <TICKET-ID> \
  --base <main|frontend|backend>
```

Append a reviewed strict-descendant fix after exact-head acceptance:

```bash
photography-ticket-delivery amend \
  --issue <issue-number> \
  --ticket <TICKET-ID> \
  --base <main|frontend|backend> \
  --commit <full-40-character-sha> \
  --verdict PASS
```

Move the exact published head to review:

```bash
photography-ticket-delivery mark-review \
  --issue <issue-number> \
  --ticket <TICKET-ID> \
  --base <main|frontend|backend> \
  --commit <full-40-character-sha> \
  --verdict PASS
```

After an explicitly approved and independently proven merge, the post-merge coordinator runs:

```bash
photography-ticket-delivery complete \
  --issue <issue-number> \
  --ticket <TICKET-ID> \
  --base <main|frontend|backend> \
  --pr <pull-request-number> \
  --approval APPROVE_CLOSE_AND_MARK_DONE
```

The helper rejects mismatched repositories, unexpected remotes, dirty or pre-staged snapshots, divergent branches, escaping symlinks, hooks, custom push options, ambiguous PRs, changed evidence, unapproved deletions and renames, and invalid Project transitions.

It uses high-level GitHub CLI commands only. Direct REST, GraphQL, `gh api`, force-pushes, remote changes, branch deletion and history rewriting are prohibited.

## Runtime supervisor

The wrapper automatically launches `photography-runtime-supervisor monitor` for the exact OpenCode PID. Useful commands are:

```bash
photography-runtime-supervisor status
photography-runtime-supervisor snapshot
photography-runtime-supervisor doctor
```

The supervisor records state under:

```text
/home/rohit/.local/state/opencode-photography-app/runtime-supervisor/
```

It may automatically send only `SIGTERM` to an exact executable verifier leaf after every configured high-confidence gate passes. It never:

- sends `SIGKILL`;
- signals OpenCode itself;
- targets a shell wrapper merely because it contains `sleep`;
- mutates Docker;
- removes containers, volumes, networks or images;
- edits or cleans Git state;
- removes branches, worktrees, evidence or delivery state.

Missing, ambiguous or changed process identity is alert-only.

## Runtime cleanup

Runtime cleanup is separate from automatic verifier supervision.

The cleanup coordinator begins with read-only inventory and must prove ticket ownership through labels, mounts, worktree paths, process ancestry and current usage. Names alone are insufficient.

The following always require explicit approval:

- sending a signal to a process not covered by the deterministic supervisor;
- stopping or removing a container;
- removing a network or image;
- any persistent-volume removal, naming every volume and acknowledging data loss.

Global prune, broad process kills, Compose `down`, filesystem deletion, Git cleanup, branch removal and worktree removal are denied.

## Safety model

| Action | Default policy |
| --- | --- |
| Read repository, issue, PR and Project metadata | Allowed through scoped tools |
| Edit application code | Exactly one assigned builder |
| Commit, non-force push, draft PR and evidence | Guarded delivery helper only |
| Post-publication amendment | Guarded helper after exact-head PASS |
| Move ticket to In Review | Guarded helper after exact-head PASS |
| Mark PR ready and merge | Post-merge coordinator after exact user approval |
| Close issue and mark Project Done | Guarded completion after proven merge and exact approval |
| Force-push, rebase or rewrite history | Denied |
| Delete branch, worktree, evidence or retained resources | Denied unless a separate exact cleanup authority exists |
| Direct GitHub REST, GraphQL or `gh api` | Denied |
| Read environment-secret files | Denied |
| Share OpenCode sessions | Disabled |

## Validation

Validate the installed configuration:

```bash
photography-orchestrator-doctor validate
photography-orchestrator-doctor evaluate
photography-orchestrator-doctor all
```

Validate the supervisor:

```bash
photography-runtime-supervisor doctor
photography-runtime-supervisor status
```

Run source-repository syntax and regression checks:

```bash
jq -e . opencode.json >/dev/null
bash -n bin/opencode-photography-app
PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile \
  bin/photography-ticket-delivery \
  bin/photography-runtime-supervisor
node --check bin/photography-orchestrator-doctor
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
git diff --check
```

At the time of this README, the expected validated baseline is:

- 348 structural checks passing;
- 10 skills scoring 100/100;
- 12 ticket-delivery regression tests passing;
- runtime-supervisor doctor passing.

These results validate the orchestration setup, not an application ticket.

## Troubleshooting

### OpenCode cannot find the configuration

Confirm that the wrapper exports the expected paths:

```bash
opencode-photography-app debug config
```

Then validate the installed JSON:

```bash
jq -e /home/rohit/.config/opencode/photography-portfolio-platform-app/opencode.json
```

### GitHub or Project reads fail

Check authentication:

```bash
gh auth status
gh auth refresh -h github.com -s project
```

Do not work around authentication failures with direct REST, GraphQL or `gh api` calls.

### A verifier appears stuck

Inspect deterministic state first:

```bash
photography-runtime-supervisor status
photography-runtime-supervisor snapshot
```

Then inspect only the ticket-specific log under `/tmp/opencode/`, the exact verifier PID and descendants, ticket-owned containers, and the retained worktree. A failed Node verifier may already have exited while a shell wrapper remains in an explicit sleep. Do not treat that wrapper as proof that the verifier is still running.

Never use broad `pkill`, `killall`, process-group signaling, global Docker prune, Compose `down`, `git clean`, or worktree deletion. Revalidate PID, start time, command, working directory and ownership immediately before any explicitly approved signal.

### The supervisor reports an alert but does not terminate

This is expected when evidence is incomplete or ambiguous. Check:

- whether the executable verifier remains alive;
- whether terminal success or failure evidence is present;
- whether the log is still changing;
- whether ticket-owned containers are stopped;
- whether PID/start-time and descendant continuity still match;
- whether the linger threshold has elapsed.

Do not weaken the supervisor gates to make an individual run terminate faster.

### A delivery command refuses the worktree

Run it from the application checkout or a registered worktree belonging to the same Git common directory. Confirm:

```bash
git remote -v
git branch --show-current
git status --short
git worktree list
photography-ticket-delivery status --issue <issue-number>
```

Resolve drift rather than bypassing a guard.

## Updating this setup

Keep the installed configuration and this private source repository synchronized intentionally:

1. Make or adopt the reviewed setup changes on a dedicated branch.
2. Ensure application-ticket changes and runtime state are not present.
3. Update both configuration files and executable helpers together when their contracts change.
4. Run every validation command above.
5. Inspect the exact diff and scan for credentials.
6. Commit and push a dedicated branch.
7. Open a draft pull request.
8. Merge only after confirming the exact validated head and clean merge state.

Never copy the setup into `photography-portfolio-platform-app` or the planning repository. Never commit `NEXT-TICKET.md`, state files, logs, `node_modules`, Python bytecode or authentication material.

## Further documentation

- [`AGENTS.md`](AGENTS.md) defines global orchestration and safety rules.
- [`WORKFLOW.md`](WORKFLOW.md) documents the operational delivery flow.
- [`agents/`](agents/) contains exact agent permissions and responsibilities.
- [`skills/`](skills/) contains reusable procedures and engineering references.
- [`bin/`](bin/) contains the wrapper, doctor, supervisor and guarded delivery helper.
- [`tests/`](tests/) contains source-level regression tests.

## License and distribution

This repository is private and tailored to a specific local environment and application repository. No public license or general redistribution grant is provided. Review hard-coded paths, private-repository assumptions and authentication requirements before adapting it elsewhere.
