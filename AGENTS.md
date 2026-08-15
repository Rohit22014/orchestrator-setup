# Local implementation rules

This file is intentionally outside the Git repository. It governs OpenCode sessions started by `opencode-photography-app`.

## Objective and scope

- Build the complete photography portfolio platform represented by all 44 roadmap issues and five milestones.
- `UX-01` is the first workflow pilot, not the project boundary.
- Use `/home/rohit/photography-portfolio-platform-app` as the sole implementation repository.
- Never edit, branch, worktree, clone, or mutate `/home/rohit/photography-portfolio-platform`.
- Never read or write tickets, comments, milestones, or Project items backed by
  `Rohit22014/photography-portfolio-platform`. The authoritative ticket
  repository is `Rohit22014/photography-portfolio-platform-app`.
- Do not access any external directory; the implementation repository contains the required handoff context.
- Do not add `.opencode`, `opencode.json`, `AGENTS.md`, or other agent configuration to the repository.
- Keep sharing disabled. The owner authorizes launching the dedicated wrapper
  with `--auto`; it does not override explicit deny rules or replace any
  ticket-specific approval required by this workflow.

## Issue-driven delivery

1. Maintain the complete dependency graph through `LAUNCH-01`.
2. Load `photo-ticket-intake` and revalidate the selected ticket through authenticated, read-only GitHub access.
3. Load `photo-integration-readiness` and prove the required integration branch contains every accepted dependency.
4. Select exactly one dependency-ready ticket for implementation.
5. Confirm its authoritative outcome, scope, acceptance criteria, milestone, lane, estimate, and dependencies.
6. Delegate repository orientation and architecture analysis in parallel when useful.
7. Select independent architecture, privacy/security, and QA/accessibility reviews from an explicit domain matrix.
8. Load `photo-platform-engineering` for production work and pass only the applicable reference constraints into the brief.
9. Produce a decision-complete brief before writing.
10. Assign exactly one builder to own every write in the current worktree.
11. Review the diff independently without reviewer edits.
12. Have the same builder address findings and run proportionate verification.
13. Rerun `photo-integration-readiness`, then load `photo-acceptance-gate` and map local evidence to every issue criterion.
14. On `READY_TO_PUBLISH`, load `photo-ticket-delivery`, attest the exact
    snapshot, and let its guarded helper commit, non-force push, create a draft
    PR, and attach immutable acceptance evidence.
15. Rerun the full acceptance gate against the exact published SHA and URLs.
16. If a reviewed fix commit strictly advances the draft PR before review,
    append it through `photography-ticket-delivery amend` only after exact-head
    `PASS`; preserve the original publication and evidence history.
17. Only an exact-head `PASS` lets the helper move Todo or In Progress to
    `In Review`. Report the handoff and stop before selecting another ticket.
18. In a later turn with explicit approval for the exact ticket and pull
    request, delegate merge, guarded completion, and next-ticket prompt creation
    to `post-merge-coordinator`. It verifies the accepted SHA, retains the
    branch and worktree, and never starts the next ticket.

Run only one writing agent in a worktree. Separate frontend and backend writers require separate worktrees created from this implementation repository after an approved baseline commit and settled shared contracts.

## Runtime cleanup boundaries

- Delegate cleanup only to `runtime-cleanup-coordinator` after the user asks for
  cleanup or approves an exact recovery plan. Read-only inventory is not
  cleanup authorization.
- Never clean resources used by an active builder, verifier, OpenCode writer,
  or another worktree. Serialize cleanup after the affected run stops.
- Every process signal and Docker removal remains approval-gated except the
  wrapper-launched deterministic supervisor's narrow standing authorization to
  send `SIGTERM` to an exact verifier after its high-confidence terminal,
  connection-failure, stopped-container, ancestry, worktree, age, and
  PID/start-time gates all pass. It never sends `SIGKILL` or mutates Docker.
  It targets the executable verifier leaf, not its shell pipeline; a reparented
  leaf remains eligible only through an unchanged, previously observed
  descendant identity fingerprint.
  Global prune commands are forbidden. Persistent volumes require separate
  approval naming each exact volume and acknowledging data loss.
- Cleanup never removes Git branches, worktrees, repository files, acceptance
  evidence, attestations, or delivery state.

## Git boundaries

- Ticket branches use `<ticket-id>/<short-description>`.
- The user's standing authorization in this local-only file supersedes older
  repository snapshot text that requires a separate approval for commit, push,
  draft-PR creation, evidence attachment, or `In Review`. That exception exists
  only inside `photography-ticket-delivery`.
- The orchestrator may automatically commit, non-force push, create or reuse a
  matching draft pull request, attach one stable evidence comment, and move the
  ticket to `In Review` only through `photography-ticket-delivery`.
- GitHub access uses high-level `gh` commands only. `gh api`, direct REST, and
  direct GraphQL are prohibited. The guarded helper also uses only high-level
  GitHub CLI commands.
- Direct mutating `gh` commands remain approval-required and are limited to
  explicitly authorized operations outside the helper's automatic ticket
  workflow, such as owner decision comments or an approved merge.
- The reviewed AUTH-02 cross-lane integration has one narrow publication
  exception: the orchestrator may run only the exact approved integration-02
  commit command and the exact non-force upstream push for
  `INTEGRATION/backend-into-frontend-for-auth-02`. General commit and push
  commands remain denied. The same exception permits only a draft PR from that
  branch into `frontend`, read-only PR-check polling, and an AUTH-02 #10
  readiness comment; it does not permit merge, closure, Done, or implementation.
- Builders and reviewers never commit, push, create PRs, comment, or update
  Project fields. They return implementation and evidence to the orchestrator.
- Merge, issue closure, `Done`, force-push, remote creation or mutation,
  rebasing or rewriting shared history, branch deletion, and file deletion
  require explicit user approval. After that approval, only the
  `post-merge-coordinator` may mark the named PR ready, perform its normal
  non-auto merge, and invoke the delivery helper's explicit ticket-specific
  `complete` command. The helper closes the app issue and marks `Done`; neither
  the agent nor helper deletes the retained branch or worktree.
- Never configure or use the planning repository's remote here.
- Never discard user changes with reset, clean, checkout, or restore.
- Preserve unrelated or pre-existing worktree changes.

## Product and architecture rules

- Planning documents and accepted ADRs are authoritative.
- The application remains a TypeScript npm-workspace monorepo with Next.js App Router, Fastify, PostgreSQL/PostGIS, BullMQ/Redis, Sharp/libvips, tus, S3-compatible storage, MapLibre, and independently containerized services unless an accepted ADR changes a choice.
- Keep synchronous API work separate from asynchronous media processing.
- Keep package ownership and dependency directions explicit.
- Generate versioned public contracts and clients; do not duplicate wire types by hand.
- Keep Grid semantic and SSR-safe, and isolate Globe code from the initial Grid bundle.
- Integrate the lightbox through one pinned release and one central `PublicPhoto` adapter.

## Privacy and security rules

- Originals, original URLs or keys, complete EXIF/IPTC, EXIF GPS, private coordinates, internal jobs, and storage paths stay private.
- Extracted GPS never becomes public geography automatically.
- Private location and creator-approved public geography are separate.
- Exact, approximate, country-only, and hidden location behavior is deterministic and creator-controlled.
- Country-only data exposes no pin; hidden geography is excluded from discovery.
- Discovery uses clean derivatives; lightbox assets are watermarked and requested only after interaction.
- Reject RAW and SVG without a separately reviewed secure ingestion issue.
- Verify magic bytes and enforce codec, size, pixel, and decompression limits before decoding.
- Use synthetic or explicitly approved public fixtures.

## Quality gates

- WCAG 2.2 AA applies to every primary journey.
- Cover keyboard, screen-reader, focus restoration, reduced motion, zoom/reflow, touch, responsive, loading, empty, success, error, disabled, permission, processing, failed, and quarantine behavior where relevant.
- Public routes have canonical metadata; private and internal routes are not indexable.
- Tests cover public-data projection and authorization boundaries.
- Migrations, generated contracts, observability, runbooks, and rollback notes stay current.
- Production engineering briefs load only the relevant workspace/CI, Fastify contract, PostGIS migration, media-worker, or observability/performance reference.
- A ticket is not complete until its acceptance criteria are traceable to evidence.

## Local skill routing

- `photo-ticket-intake`: orchestrator and scout at the start of every ticket.
- `photo-adr-contract`: architect and relevant builder before material architecture or contract changes.
- `photo-privacy-review`: privacy reviewer and relevant builder for protected-data flows.
- `photo-browser-evidence`: frontend builder for browser evidence; QA reviewer inspects the resulting evidence.
- `photo-acceptance-gate`: orchestrator, builder, and QA reviewer before
  publication and again against the exact published SHA.
- `photo-ticket-delivery`: orchestrator for publication after
  `READY_TO_PUBLISH` and exact-head `PASS`; post-merge coordinator for the
  approval-gated `complete` command only.
- `photo-platform-engineering`: architect, builders, and reviewers for production engineering; load only applicable references.
- `photo-integration-readiness`: orchestrator and scout before dependent work and publication.
- `photo-orchestrator-evaluation`: orchestrator after local setup or OpenCode changes.
- `photo-runtime-cleanup`: runtime cleanup coordinator for inventory, hung-run recovery, and explicitly approved ticket-owned cleanup.

Skills live only in the external OpenCode configuration. Do not copy them into the repository.

## Local setup quality

- Run `photography-orchestrator-doctor validate` after any local agent, skill, permission, wrapper, helper, or OpenCode change.
- Run `photography-orchestrator-doctor evaluate` to score skill trigger quality, progressive disclosure, safety, verification guidance, references, and UI metadata.
- The doctor must also prove that the helper and QA reviewer cannot use
  `gh api`, REST, GraphQL, or GitHub web access.
- Static scores are maintenance signals. They never replace issue acceptance evidence or the two publication gates.

## Initial sequence

`ARCH-01` and `UX-01` are both unblocked. Use `UX-01` as the first workflow pilot unless the user selects `ARCH-01`; complete `ARCH-01` before `FND-01` and complete `UX-01` before `UX-02`. Continue through the next dependency-ready ticket until `LAUNCH-01`.
