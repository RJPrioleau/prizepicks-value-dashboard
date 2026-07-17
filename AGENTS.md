# Repository Instructions

## End-of-session workflow

When the user indicates they are finished, asks to wrap up, or says they are switching computers:

1. Summarize the work completed and note any unfinished items or known issues.
2. Run the relevant tests or checks when practical, and report anything that was not verified.
3. Review `git status --short` and identify the files changed during the session without altering unrelated user changes.
4. Ask whether the user wants the session changes committed and pushed to `origin`. Never commit or push without explicit approval.
5. After an approved push, report the branch, commit hash, and whether the local branch is synchronized with its upstream.
6. Provide a short continuation note the user can use on another computer, including the latest commit and the next task when work remains.

