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
- Keep sharing disabled and never start OpenCode with `--auto`.

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
16. Only an exact-head `PASS` lets the helper move Todo or In Progress to
    `In Review`. Report the handoff and stop before selecting another ticket.

Run only one writing agent in a worktree. Separate frontend and backend writers require separate worktrees created from this implementation repository after an approved baseline commit and settled shared contracts.

## Git boundaries

- Ticket branches use `<ticket-id>/<short-description>`.
- The user's standing authorization in this local-only file supersedes older
  repository snapshot text that requires a separate approval for commit, push,
  draft-PR creation, evidence attachment, or `In Review`. That exception exists
  only inside `photography-ticket-delivery`.
- The orchestrator may automatically commit, non-force push, create or reuse a
  matching draft pull request, attach one stable evidence comment, and move the
  ticket to `In Review` only through `photography-ticket-delivery`.
- Builders and reviewers never commit, push, create PRs, comment, or update
  Project fields. They return implementation and evidence to the orchestrator.
- Merge, issue closure, `Done`, force-push, remote creation or mutation,
  rebasing or rewriting shared history, branch deletion, and file deletion
  require explicit user approval. After a merge, the delivery helper may close
  the app issue and mark `Done` only through its explicit ticket-specific
  `complete` command; it never merges or deletes the retained branch.
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
- `photo-ticket-delivery`: orchestrator only, after `READY_TO_PUBLISH` and after
  the published SHA receives `PASS`.
- `photo-platform-engineering`: architect, builders, and reviewers for production engineering; load only applicable references.
- `photo-integration-readiness`: orchestrator and scout before dependent work and publication.
- `photo-orchestrator-evaluation`: orchestrator after local setup or OpenCode changes.

Skills live only in the external OpenCode configuration. Do not copy them into the repository.

## Local setup quality

- Run `photography-orchestrator-doctor validate` after any local agent, skill, permission, wrapper, helper, or OpenCode change.
- Run `photography-orchestrator-doctor evaluate` to score skill trigger quality, progressive disclosure, safety, verification guidance, references, and UI metadata.
- Static scores are maintenance signals. They never replace issue acceptance evidence or the two publication gates.

## Initial sequence

`ARCH-01` and `UX-01` are both unblocked. Use `UX-01` as the first workflow pilot unless the user selects `ARCH-01`; complete `ARCH-01` before `FND-01` and complete `UX-01` before `UX-02`. Continue through the next dependency-ready ticket until `LAUNCH-01`.
