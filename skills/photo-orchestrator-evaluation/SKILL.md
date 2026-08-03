---
name: photo-orchestrator-evaluation
description: Validate and score the local photography OpenCode orchestrator, agents, skills, models, permission boundaries, and repository isolation. Use after any local agent, skill, workflow, wrapper, helper, or opencode.json change; before trusting a newly installed OpenCode version; or when model, recursion, write ownership, external-directory, or GitHub mutation behavior may have drifted.
---

# Photo orchestrator evaluation

Run the deterministic local doctor before behavioral sampling:

    photography-orchestrator-doctor validate
    photography-orchestrator-doctor evaluate

## Workflow

1. Treat any validation failure as a hard stop. Do not compensate by broadening a permission or bypassing a helper.
2. Review every skill score and fix placeholders, broken references, missing trigger language, excessive eager context, or absent verification and safety guidance. A score is a maintenance signal, not acceptance evidence for an application ticket.
3. Run the resolved OpenCode checks documented in "WORKFLOW.md" and confirm exact Sol, Terra, and Luna assignments after upgrades.
4. Exercise one read-only delegation to the scout and one role-appropriate skill load. Confirm the named specialist runs, cannot edit, cannot access external directories, and cannot spawn a task.
5. Verify exactly one builder can edit while reviewers cannot. Use a dry-run or existing disposable fixture; never create a file that would require unapproved deletion.
6. Confirm raw Git/GitHub mutations remain denied and the guarded delivery helper is the only automatic publication path.
7. Record OpenCode version, configuration hash, doctor output, behavioral prompt, observed model and agent, permission denials, limitations, and date.

Never put evaluation configuration or artifacts into either repository. Never use the planning repository as a test target. Do not run "--auto", merge, close issues, mark Done, change remotes, force-push, delete, or weaken the single-writer rule during evaluation.
