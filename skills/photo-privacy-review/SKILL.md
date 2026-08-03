---
name: photo-privacy-review
description: Review photography-platform changes for authorization, private originals, metadata, EXIF GPS, public geography, uploads, derivatives, caching, deletion, logs, and fixture disclosure. Use for any issue or diff that reads, stores, transforms, serializes, displays, logs, caches, moderates, or deletes user or media data.
---

# Photo privacy review

Trace protected data through the complete affected flow and report evidence without editing.

## Review

1. Identify actors, resource ownership, lifecycle states, trust boundaries, and public/private/admin classifications.
2. Trace inputs through upload, storage, database, queues, workers, API projection, browser state, URLs, caches, logs, backups, moderation, and deletion as applicable.
3. Verify these independent protected domains:
   - originals and source delivery;
   - complete EXIF/IPTC and device identifiers;
   - EXIF GPS and exact private coordinates;
   - storage keys, signed URLs, internal jobs, scanner output, and operational diagnostics.
4. Confirm public geography is separately persisted and explicitly creator-approved:
   - exact exposes only an approved exact point;
   - approximate follows an accepted algorithm and cannot be inferred ad hoc;
   - country-only exposes no individual pin or coordinate;
   - hidden is absent from geographic discovery.
5. Confirm discovery uses clean responsive derivatives and intentional photo details use watermarked derivatives only after interaction.
6. Verify authorization for anonymous, unverified, pending, rejected, active, suspended, owner, non-owner, and administrator states. A product-specific alias counts only when the artifact explicitly maps it to one of these states and preserves the same authorization semantics.
7. Check that draft, processing, failed, quarantined, removed, expired, unauthorized, and stale states cannot imply publication eligibility. Exercise direct transitions from an eligible state and require every readiness message, action, announcement, and derived view to update fail-closed.
8. Verify fixtures are synthetic or approved public data and contain no real coordinates, credentials, storage paths, source metadata, or private identifiers.
9. Check cache invalidation, delayed jobs, restoration, soft deletion, final destruction, audit records, and logs for disclosure or resurrection.

## Findings

Report findings by severity with file or contract evidence, affected criterion, failure or exploit path, and concrete remediation. State explicitly when a reviewed category has no finding. Treat unresolved approximate-location, publication, derivative-delivery, or deletion semantics as blockers rather than inventing behavior.

Use this finding shape:

| Severity | Evidence | Criterion or invariant | Failure or exploit path | Remediation | Owner |
|---|---|---|---|---|---|

For a documentation or design ticket, a decision may be deferred without failing the current ticket only when the issue permits deferral, the artifact does not make the behavior authoritative, and it names the owning downstream issue and safe interim constraint. That decision remains a blocker for downstream implementation. If any of those conditions is absent, it blocks the current ticket too.
