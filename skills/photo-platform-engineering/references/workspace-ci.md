# Workspace, dependencies, and CI

## Workspace boundary

- Keep one root lockfile and reproducible root installation with "npm ci".
- Pin the supported Node and npm versions in repository-owned metadata and CI.
- Keep workspace dependencies explicit. Do not reach across package source directories or duplicate generated contracts.
- Preserve server/client boundaries: browser packages never import database, storage, queue, worker, or private domain code.
- Give every package an owner, public entry point, build contract, test command, and compatibility expectation.

## Dependency changes

1. State the capability gap and compare use of existing dependencies before adding one.
2. Check maintenance, license, release cadence, transitive risk, browser or server footprint, and compatibility with the pinned runtime.
3. Pin integrations whose behavior affects privacy, media delivery, accessibility, or public contracts.
4. Review the complete lockfile diff. Never hide an unrelated upgrade in a ticket.
5. Record upgrade, rollback, and removal paths. Treat an audit finding by exploitability and reachable use, not severity text alone.

## CI design

- Use least-privilege tokens, pinned action or tool versions, protected secrets, and explicit permissions.
- Run formatting or lint, types, unit tests, contract tests, and ticket-specific integration or browser checks at the narrowest useful scope.
- Key caches by lockfile, runtime, platform, and relevant configuration; never cache secrets or private media.
- Keep generated artifacts reproducible and fail when committed output drifts from its source.
- Make skipped checks visible. A required unavailable service is a blocker, not a silent pass.
- Keep deployment and destructive migration steps outside ordinary pull-request validation.

## Evidence

Record runtime versions, install command, affected workspace scripts, lockfile review, CI permission changes, cache behavior, generated-output check, and all skipped or environment-dependent checks.
