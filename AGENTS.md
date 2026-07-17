# Repository Instructions

## Collaboration context

Read `docs/COLLABORATION_WORKFLOW.md` before beginning substantial work. It describes the user's learning goals, preferred teaching style, division of responsibilities between PyCharm and PowerShell, and the relationship between this project and the independent Developer Playbook repository.

## End-of-session workflow

When the user indicates they are finished, asks to wrap up, or says they are switching computers:

1. Summarize the work completed and note any unfinished items or known issues.
2. Run the relevant tests or checks when practical, and report anything that was not verified.
3. Review `git status --short` and identify the files changed during the session without altering unrelated user changes.
4. Add a concise, self-contained entry to **Handoff details and continuity log** below. This entry is the standard handoff for the next AI agent and must include the local date, time, and time zone; completed work; important decisions or architectural direction; unfinished work and the exact next task; known issues; and verification performed. Preserve useful information from earlier entries and avoid repeating unchanged details.
5. Ask whether the user wants the session changes, including the continuity entry, committed and pushed to `origin`. Never commit or push without explicit approval.
6. After an approved push, report the branch, commit hash, and whether the local branch is synchronized with its upstream.
7. Provide a short continuation note the user can use on another computer, including the latest commit and the next task when work remains.

## Machine-switch handoff

The repository documents must contain the handoff context; do not rely on the user remembering details from the previous chat or carrying a separate continuation note.

Before leaving the current computer:

1. Complete the end-of-session workflow above.
2. Ensure the newest handoff entry is self-contained and contains the decisions, unfinished work, exact next task, known issues, and verification needed to resume without the old transcript.
3. After the user approves the commit and push, verify the active branch is synchronized with its upstream.

On the receiving computer, before beginning new work:

1. Ask the user to confirm that the latest changes have been pulled from `origin` if the local repository is behind or synchronization has not been established.
2. Read this file and `docs/COLLABORATION_WORKFLOW.md`.
3. Inspect the newest handoff entry, the current branch, `git status --short`, and the latest commit.
4. Briefly summarize the recovered context, current repository state, and proposed next task so the user can confirm that the handoff succeeded.
5. Do not overwrite uncommitted work or assume that machine-specific environments, secrets, ignored files, or PyCharm settings transferred through Git.

The user should only need to pull the repository and tell the receiving agent:

> Read the latest handoff details in `AGENTS.md` and continue from there.

## Handoff details and continuity log

This is the authoritative continuing handoff record for AI agents working on this repository from different computers. At every session end or computer switch, add a new entry directly below this explanation, with the newest entry first. The newest entry is the active handoff; older entries preserve useful decision history. Keep entries concise but preserve decisions and context that cannot be recovered from the code alone. Do not use this section as a general development diary or duplicate information already clear from Git history.

### 2026-07-17 17:45 EDT — Establish cross-machine collaboration workflow

- Completed: Expanded the end-of-session and machine-switch procedures, created `docs/COLLABORATION_WORKFLOW.md`, and linked it from this file so future agents load the user's learning and collaboration preferences.
- Decisions and architecture: Use Git plus this continuity log to hand work between the Surface Pro and desktop. Use PyCharm primarily for coding and debugging and PowerShell for application/code interrogation. Default to a beginner-friendly "teach me as we go" style while the user learns Python, command-line skills, and PyCharm together. Keep the Developer Playbook as a separate portable repository; add material only after repeated real-world use proves its value.
- Next steps: Commit and push these documentation changes, pull them on the other computer, and verify that its AI agent reads both documents. The user also plans to provide PDF exports of earlier browser chats so durable project context can be recovered.
- Known issues: Chat transcripts do not automatically transfer between the user's computers; uncommitted or unpushed work will not be included in a Git handoff.
- Verification: Ran `git diff --check`; no whitespace errors were reported. No application tests were needed because only Markdown instructions and documentation changed.

### Entry format

```text
### YYYY-MM-DD HH:MM TZ — Short session title

- Completed:
- Decisions and architecture:
- Next steps:
- Known issues:
- Verification:
```

