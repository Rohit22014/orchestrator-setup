---
name: photo-platform-engineering
description: Apply photography-platform engineering constraints for TypeScript workspaces, CI and dependencies, Fastify/OpenAPI contracts, PostgreSQL/PostGIS migrations, upload and media workers, observability, and performance. Use when a ticket creates or changes production code, package boundaries, automation, dependencies, API schemas, persistence, background jobs, media processing, telemetry, capacity, or recovery behavior.
---

# Photo platform engineering

Load only the reference files that match the selected ticket. Combine them when a change crosses domains; do not load every reference by default.

## Route the work

| Change area | Required reference |
|---|---|
| npm workspaces, TypeScript, dependencies, CI, build or release automation | [workspace-ci.md](references/workspace-ci.md) |
| Fastify routes, schemas, authorization, pagination, OpenAPI or generated clients | [fastify-contracts.md](references/fastify-contracts.md) |
| PostgreSQL, PostGIS, schema changes, backfills, retention or rollback | [postgres-postgis.md](references/postgres-postgis.md) |
| uploads, object storage, queues, Sharp/libvips, derivatives or quarantine | [media-workers.md](references/media-workers.md) |
| logging, metrics, traces, alerts, runbooks, capacity or performance | [observability-performance.md](references/observability-performance.md) |

Load "photo-adr-contract" as well when the ticket crosses a material boundary or leaves compatibility, ownership, migration, privacy, or rollback semantics unresolved. Load "photo-privacy-review" for protected-data flows.

## Workflow

1. Start from the authenticated ticket, accepted ADRs, and repository-owned commands. Do not invent framework or infrastructure scope that the ticket does not require.
2. Select the smallest relevant reference set and record why each one applies.
3. Map ownership, dependency direction, serialized contracts, data classification, failure states, rollback, observability, and acceptance evidence before writing.
4. Reuse repository patterns and pinned dependencies. Introduce a new tool or package only with an explicit need, ownership, compatibility policy, lockfile evidence, and removal or upgrade path.
5. Keep public DTOs, browser state, URLs, logs, metrics, traces, fixtures, and caches free of originals, source keys, complete metadata, private coordinates, credentials, and internal diagnostics.
6. Verify the narrow change first, then the affected workspace boundary. Never weaken or skip a failing required check.
7. Return the applied references, decisions, commands, evidence, limitations, rollback or recovery notes, and downstream follow-ups.

## Output

Use this compact matrix in the implementation brief and final evidence:

| Area | Owner and boundary | Failure or migration risk | Required check | Evidence |
|---|---|---|---|---|

Treat an unresolved destructive migration, public/private projection, media-delivery boundary, authorization rule, or recovery path as a blocker.
