---
name: photo-runtime-cleanup
description: Inventory and safely remove explicitly approved, ticket-owned Docker and local runtime resources for the photography platform. Use when a verification run hangs, leaks containers or processes, leaves stopped Compose resources, or the user asks to reclaim Docker space without disturbing retained data or another worktree.
---

# Photo Runtime Cleanup

Clean only resources whose ownership and disposal authority are proven. Treat cleanup as a separate operational action, not an automatic end-of-ticket step. A deterministic companion is launched by `opencode-photography-app`; inspect it first with `photography-runtime-supervisor status`.

## Automatic verifier recovery boundary

The companion may automatically send `SIGTERM` to one exact verifier without a
new approval only when all of these deterministic checks pass:

- the process is a descendant of the exact wrapper-launched OpenCode PID;
- it is the executable verifier leaf rather than a matching shell or pipeline
  wrapper;
- its PID, process start time, command, ancestry, and working directory under
  the implementation repository are revalidated immediately before signaling;
- a terminal failure marker and at least three post-failure connection refusals
  have persisted for at least sixty seconds, or a terminal success/leak marker
  has made no progress for at least five minutes;
- ticket identity is derived from the verifier worktree and all matching
  ticket-named Docker containers are already stopped.

If a previously observed leaf is reparented because its pipeline wrapper exits,
the companion may preserve ownership only while its PID/start time, process
group, exact command, worktree, ticket, and log path remain unchanged. Any
identity drift remains alert-only.

It sends only `SIGTERM` to the verifier PID and records its proof. It never
automatically sends `SIGKILL`, signals OpenCode, mutates Docker, deletes files,
or touches Git, branches, worktrees, evidence, or volumes. Any missing check,
running or ambiguous container, ordinary long runtime, or timeout without a
terminal proof remains alert-only and follows the approval sequence below.

The owner may launch OpenCode with `--auto`; do not treat that session flag as
approval for a cleanup target. Only the deterministic verifier `SIGTERM`
exception above may proceed without an exact cleanup approval.

## Required sequence

1. Confirm the implementation repository is `/home/rohit/photography-portfolio-platform-app` and the planning repository is out of scope.
2. Inventory before mutation:
   - active OpenCode, verifier, worker, browser, proxy, and test processes;
   - Docker containers, Compose projects, networks, images, volumes, and build-cache size;
   - Git worktrees and the current ticket-delivery phase when relevant.
3. Attribute each candidate using exact container or image ID, Compose labels, mounts, networks, creation time, state, and the originating ticket/worktree. A name substring alone is insufficient proof.
4. Classify every resource:
   - `ACTIVE_OR_REFERENCED`: retain;
   - `AMBIGUOUS_OWNER`: retain and report;
   - `RETAINED_DATA`: retain unless the user separately approves exact volumes;
   - `SAFE_CANDIDATE`: stopped or orphaned, ticket-owned, unreferenced, and within the approved scope.
5. Present an exact cleanup plan with names and IDs, why each target is safe, dependencies, recoverability, and estimated reclaimed space. State separately whether the plan stops a running process, deletes a container/network/image, or deletes persistent data.
6. Obtain explicit approval for the exact plan, except for the companion's narrow automatic verifier `SIGTERM` above. Volume removal requires its own explicit approval even when the user approved other Docker cleanup. A request to inspect, diagnose, or check status is not deletion approval.
7. Revalidate IDs, labels, state, mounts, references, and process identity immediately before each mutation. Stop on drift.
8. Execute only the approved exact targets in dependency order: graceful process/container stop, exact stopped-container removal, unused ticket network removal, then unreferenced ticket image removal. Remove an approved volume last.
9. Verify the targets are absent, retained resources are present, unrelated running services are unchanged, the Docker daemon is healthy, and reclaimed-space reporting is accurate.

## Hard stops

- Never run `docker system prune`, container/image/network/volume prune, builder or Buildx prune, or an equivalent daemon-wide cleanup.
- Never infer that an unused volume is disposable. Preserve database, object-storage, malware-signature, queue, backup, and named Compose volumes by default.
- Never stop or remove a resource used by an active harness, OpenCode writer, another worktree, or an unidentified user process.
- Never use broad `pkill`, `killall`, wildcard removal, unresolved variables, command substitution, or recursive filesystem deletion.
- Never remove Git branches, worktrees, repository files, evidence, attestations, or delivery state.
- Never clean the planning repository or resources outside the photography app scope.
- Never treat cleanup output as ticket acceptance evidence.

## Interrupted verification

For a hung verifier, identify its exact PID, parent pipeline, worktree, owned containers, and last observable phase. Prefer `SIGTERM` to the single recorded verifier process and allow its bounded cleanup handler to run. Use `SIGKILL` only after the grace period, after confirming the PID identity has not changed, and with explicit approval. Preserve the OpenCode parent and uncommitted worktree unless the user explicitly names them.

## Report

Return:

- inspected scope and ownership evidence;
- exact resources retained, stopped, and removed;
- volume decisions as a separate section;
- space before and after when measurable;
- any ambiguous resources or manual follow-up;
- proof that active worktrees and unrelated services were not disturbed.
