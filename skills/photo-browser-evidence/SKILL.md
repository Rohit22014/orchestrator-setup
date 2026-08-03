---
name: photo-browser-evidence
description: Exercise photography-platform web journeys with Playwright CLI and collect reproducible responsive, keyboard, focus, console, network, and screenshot evidence. Use for UX prototypes, Next.js routes, browser regressions, accessibility journeys, responsive states, Globe/list parity, lightbox behavior, or acceptance evidence.
---

# Photo browser evidence

Use `playwright-cli` for efficient exploratory evidence. Keep durable CI behavior in repository-owned Playwright tests.

## Preconditions

1. Confirm the target is a local, synthetic test environment.
2. Start the documented local server and record its command and URL.
3. Use a named, non-persistent browser session. Never load personal profiles, production credentials, real media, or private location data.
4. Keep browser requests on expected localhost origins unless the ticket explicitly requires an approved external dependency.
5. Only the assigned writing builder runs the CLI. Use an approved ticket-specific temporary directory, or the worktree's ignored `.playwright-cli/` directory, and copy only approved durable evidence into the repository. Read-only reviewers use this skill as an evidence-review checklist and do not create browser artifacts.

## Evidence loop

1. Open the target with `playwright-cli -s=<ticket> open <url>`.
2. Capture a structural snapshot before interacting.
3. Exercise the primary journey using semantic references and keyboard input.
4. Use the ticket's required evidence sizes. When none are specified, cover 320, 375, 768, and 1440 CSS pixels. Treat these as evidence sizes, not final design tokens.
5. Check:
   - landmarks, headings, names, roles, states, and announcements;
   - tab order, visible focus, forward and reverse dialog wrapping, Escape behavior, and invoker restoration; focus must never fall to `BODY` while a modal remains open;
   - reduced motion, reflow, touch-sized controls, native checkbox/radio sizing, label readability, portrait, landscape, and panoramic content where applicable;
   - loading, empty, success, validation, network, authorization, processing, quarantine, conflict, removal, and recovery;
   - direct transitions between safe and unsafe lifecycle states, confirming every status, readiness message, action, and announcement updates exhaustively;
   - Grid/Globe eligible-set parity and the semantic list fallback;
   - deferred Globe and lightbox loading;
   - console errors, failed requests, unexpected origins, and private data in URLs or payloads.
6. Do not treat a narrow viewport as proof of browser zoom. If 200% or 400% zoom is required, perform a real manual browser-zoom review or record it as unavailable required evidence.
7. Save concise screenshots or recordings only when they prove a criterion. Name evidence by ticket, viewport, journey, and state.
8. Close the named browser session, stop a server started for the review, and remove temporary CLI artifacts after recording the approved evidence paths.

## Handoff

Record a durable evidence manifest with the server command, browser commands, viewport, journey, expected result, observed result, console/network outcome, artifact path, reviewer, date, and limitations. Do not claim automated WCAG conformance, real zoom, or manual screen-reader completion from CLI evidence alone. The writing builder owns evidence files; read-only reviewers inspect them without modifying the worktree.

Use this manifest shape:

| Viewport | Journey and state | Commands | Expected | Observed | Console and network | Artifact | Result |
|---|---|---|---|---|---|---|---|

End with explicit limitations and confirmation that temporary files, browser sessions, and any review-only server were cleaned up.
