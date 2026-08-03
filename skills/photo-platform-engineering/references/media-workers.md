# Upload, storage, and media workers

## Trust boundaries

- Treat every upload as hostile until validation completes.
- Store originals in private S3-compatible storage under opaque keys. Never expose source buckets, keys, URLs, or originals through public contracts.
- Keep request handlers responsible for authorization and transfer setup; perform validation, metadata extraction, decoding, and transformation asynchronously.
- Reject RAW and SVG unless a separately accepted issue defines a secure pipeline.

## Processing state machine

Define explicit states and legal transitions for transfer, validation, quarantine, processing, ready, failed, removed, and deletion. Every job must be idempotent, retry-aware, observable, and safe under duplicate or out-of-order delivery.

Before decode:

1. Verify magic bytes independently of extension and declared MIME type.
2. Enforce byte, pixel, dimension, frame, codec, and decompression limits.
3. Quarantine unsupported, malformed, or scanner-rejected content.
4. Extract metadata into private structured storage and isolate EXIF GPS.
5. Strip metadata from public derivatives and normalize output safely.

## Derivatives and delivery

- Use immutable, content-addressed or versioned derivative identities and record their provenance.
- Serve clean responsive discovery derivatives. Request watermarked lightbox derivatives only after deliberate interaction.
- Make publication eligibility depend on approved creator state, media readiness, event state, moderation state, and derivative availability.
- Revoke cached delivery when eligibility changes and prevent stale jobs from republishing removed content.
- Keep originals, complete EXIF/IPTC, GPS, private coordinates, scanner output, and job diagnostics out of URLs, logs, metrics, events, and fixtures.

## Verification

Test signature/MIME mismatch, oversize and decompression cases, corrupt images, duplicate jobs, retries, stale transitions, quarantine, authorization, derivative provenance, metadata stripping, cache revocation, removal, and restore. Use only synthetic fixtures.
