---
name: photo-ticket-intake
description: Validate a photography-platform roadmap ticket before planning or implementation. Use for every new ticket, resumed ticket, dependency check, stale local snapshot, milestone transition, or branch handoff that requires current private GitHub issue and project metadata.
---

# Photo ticket intake

Establish one authoritative, dependency-aware ticket brief before any writes.

## Workflow

1. Identify the ticket number and current branch.
2. Run `gh auth status`. Stop and report an authentication blocker if it
   fails. Project reads require `read:project`; this full delivery setup
   intentionally retains the stronger `project` scope so the guarded helper can
   perform the final `In Review` transition. Do not downgrade or refresh scopes
   during ordinary ticket intake.
3. Read the issue without mutation:

   ```text
   gh issue view <number> --repo Rohit22014/photography-portfolio-platform-app \
     --json number,title,state,body,labels,milestone,url
   ```

4. Read Project 1 without mutation:

   ```text
   gh project item-list 1 --owner Rohit22014 --format json --limit 100
   ```

5. Extract and preserve verbatim:
   - outcome and scope;
   - acceptance criteria and definition of done;
   - state, milestone, lane, priority, estimate, and integration branch;
   - formal dependencies and any accepted waivers.
6. Compare current data with `docs/project/ROADMAP.md`, `docs/project/STATUS.md`, the current branch, and existing ticket artifacts.
7. Treat GitHub drift as a blocker until the brief records the current value. Never silently prefer a stale snapshot.
8. Mark the ticket ready only when every dependency is accepted or explicitly waived by an accepted ADR or issue update.

## Output

Return a compact intake record containing:

- capture timestamp and authoritative URLs;
- ticket identity and metadata;
- verbatim criteria;
- dependency evidence;
- current branch and expected integration branch;
- drift from local documents;
- `ready`, `blocked`, or `needs-decision`;
- the exact next safe action.

Use stable sections for metadata, verbatim criteria, dependencies, drift, decisions, and next action. For dependency evidence, use:

| Dependency | Required state | Evidence URL | Result |
|---|---|---|---|

Do not edit GitHub, add labels, change project status, configure remotes, or
access the planning checkout or its GitHub issues. All ticket authority belongs
to `Rohit22014/photography-portfolio-platform-app`. A builder may persist an
approved snapshot in the implementation repository only as the single writing
agent.
