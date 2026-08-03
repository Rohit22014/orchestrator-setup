---
name: photo-adr-contract
description: Settle photography-platform architecture, privacy, API, event, storage, queue, deletion, media, location, cache, and package-boundary decisions before dependent implementation. Use for ARCH-01, new cross-package contracts, unresolved product semantics, dependency gates, migrations, or changes to accepted invariants.
---

# Photo ADR and contract gate

Turn material uncertainty into an accepted decision before dependent code proceeds.

## Decision authority and precedence

- Treat the authenticated GitHub issue and its recorded dependencies as the delivery authority. Repository engineering rules and accepted ADRs are authoritative implementation constraints.
- When those sources conflict, stop at the conflict, name every affected source, and request a human decision. Do not silently choose a winner.
- Only a repository owner or issue assignee explicitly authorized by the owner may mark an ADR `accepted`. Agent-authored ADRs remain `proposed` until that approval is recorded in both the ADR and the authoritative issue.
- A decision is material when getting it wrong could expose private data, weaken authorization, break a serialized or public contract, cause irreversible loss, change deployable/package ownership, or force costly migration. Material uncertainty blocks dependent implementation.

## Workflow

1. Read the authenticated issue, `docs/project/ENGINEERING-RULES.md`, existing ADRs, affected contracts, and dependent tickets.
2. Identify the smallest independent decisions that collectively satisfy the issue. Use one ADR per unrelated choice and report every required ADR path.
3. Record:
   - status, date, author, explicit human acceptor, and linked issue;
   - context and non-negotiable constraints;
   - decision and explicit invariants;
   - alternatives and reasons rejected;
   - package/service ownership and dependency direction;
   - public/private DTO or event boundaries;
   - failure, retry, idempotency, cache, retention, migration, rollback, and observability consequences;
   - security, privacy, accessibility, and operational implications;
   - verification evidence and tickets unlocked.
   Mark a category `N/A` only with a concrete reason.
4. Check that web code cannot import private database, storage, queue, worker, or domain entities.
5. Keep request handlers free of image decoding and keep workers free of public authorization decisions.
6. Separate private location from creator-approved public geography and private source metadata from public allowlisted metadata.
7. Define compatibility and explicit versioning for serialized REST, job, event, storage, and public contracts. For in-process TypeScript APIs, define package ownership and compatibility policy; a wire-version number is optional unless the API crosses a release or runtime boundary.
8. Verify decision-only work with issue-criteria traceability, contradiction searches, import/dependency diagrams where relevant, contract examples, and recorded human review. Do not claim runtime evidence for documentation-only work.
9. Distinguish directly unlocked tickets from transitive downstream tickets, using the authenticated issue dependency graph as the source.
10. Mark unresolved choices explicitly. A provisional note is not an accepted decision and cannot unblock a dependent ticket.
11. If an accepted ADR supersedes an issue statement or engineering rule, update that authoritative source or explicitly mark the conflicting statement superseded as part of acceptance. A link alone does not resolve the contradiction; otherwise report it as blocking.

## Output

Return all proposed ADR paths, decision summaries, invariants, affected contracts, migration and rollback implications, verification evidence, unresolved questions, acceptance authority, and exact directly versus transitively blocked or unlocked tickets. Do not implement across an unresolved material boundary.
