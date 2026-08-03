# Observability, performance, and operability

## Telemetry

- Emit structured logs with stable event names, severity, safe correlation IDs, outcome, and duration.
- Never log credentials, session tokens, signed URLs, object keys, originals, complete metadata, EXIF GPS, private coordinates, request bodies, or unredacted errors.
- Keep metric labels bounded. Do not use user IDs, photo IDs, URLs, filenames, coordinates, or error messages as labels.
- Propagate trace context through API, queues, and workers without putting protected data into spans.
- Audit privileged state changes separately with actor, target, reason, outcome, and safe immutable identifiers.

## Service signals

Define measurable service objectives or explicit ticket budgets before optimizing. Cover:

- API latency, error rate, saturation, database pool and query health;
- upload throughput and failure rate;
- queue depth, oldest-job age, attempts, dead letters, worker duration and memory;
- derivative generation failures and cache-revocation delay;
- web Core Web Vitals, JavaScript and image weight, SSR success, hydration errors, and route-level failures.

## Performance boundaries

- Measure before and after with reproducible fixtures and environment notes.
- Keep Classic Grid semantic and SSR-safe. Load Globe and lightbox code only when requested.
- Bound database queries, response sizes, image dimensions, concurrency, retries, queue payloads, and in-memory work.
- Test degraded dependencies, slow storage, worker backlog, cache failure, and recovery without disclosing protected state.

## Alerts and runbooks

Every actionable alert names the symptom, threshold, duration, owner, dashboard, first safe diagnostic, mitigation, recovery verification, and escalation path. Avoid alerts that require access to private media for diagnosis. Record limitations when production-like load or hosted telemetry is unavailable.
