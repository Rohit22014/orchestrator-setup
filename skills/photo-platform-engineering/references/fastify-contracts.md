# Fastify, OpenAPI, and generated contracts

## Ownership

- Keep "/api/v1" Fastify schemas as the serialized contract source of truth.
- Generate public types and the web client into "packages/contracts"; do not hand-maintain duplicate wire types.
- Keep domain and persistence models private to server packages. Public, creator, administrator, and internal projections are distinct types.
- Put authorization at the server boundary and re-check resource ownership inside the domain operation.

## Route requirements

For each route define actors, authentication, ownership, request schema, public or private response schema, lifecycle eligibility, errors, pagination, idempotency, rate limits, caching, audit behavior, and observability.

- Reject unknown or malformed input through schemas before domain work.
- Return stable safe error codes without stack traces, object keys, queries, worker diagnostics, or existence leaks.
- Use deterministic cursor pagination with a stable tie-breaker; bind cursors to the relevant filter and authorization context.
- Make retryable mutations idempotent and scope keys to actor plus operation.
- Keep image decoding and transformation out of request handlers.
- Project only allowlisted public metadata and eligible derivatives. Never serialize an internal entity and subtract fields afterward.

## Compatibility and verification

- Treat removing, renaming, narrowing, or changing semantics of a serialized field as a compatibility decision.
- Regenerate OpenAPI, types, and clients in the same ticket and fail CI on drift.
- Test schema rejection, authentication, ownership, lifecycle transitions, public-data projection, pagination stability, idempotency, and safe errors.
- Add negative assertions that originals, storage keys, complete metadata, GPS, private geography, moderation fields, and internal job data are absent.
