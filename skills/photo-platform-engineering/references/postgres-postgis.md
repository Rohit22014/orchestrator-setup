# PostgreSQL and PostGIS migrations

## Migration discipline

1. Define the invariant, affected readers and writers, data volume, lock risk, compatibility window, backup prerequisite, and rollback or forward-fix plan.
2. Prefer expand, migrate, verify, then contract. Keep old and new application versions compatible during rollout when deployment is not atomic.
3. Make migrations versioned, deterministic, non-interactive, and safe to rerun only when their framework guarantees that behavior.
4. Separate schema changes from large backfills. Batch, checkpoint, observe, and make backfills resumable.
5. Do not combine irreversible deletion with an unproven restore process.

## Data and geography boundaries

- Store private extracted coordinates separately from creator-approved public geography, with separate access paths and authorization.
- Enforce the accepted SRID and geometry type with database constraints. Validate latitude/longitude ordering at boundaries.
- Country-only exposes a country identifier and no point. Hidden location has no public discovery geometry.
- Do not invent approximate-location storage or generalization before its ADR is accepted.
- Use foreign keys, uniqueness, checks, and lifecycle constraints to enforce invariants that must survive every application path.

## Safety and evidence

- Assess locks with production-like row counts and state whether DDL is transactional.
- Test a clean migration, upgrade from the previous schema, application compatibility, constraint failures, and rollback or documented forward recovery.
- Verify public queries cannot join or project private coordinates or source metadata.
- Record migration duration, lock observations, row counts, checksum or invariant checks, backup/restore prerequisite, and operator runbook.
