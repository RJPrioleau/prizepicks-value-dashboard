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

### 2026-07-21 10:14 EDT — Bound Sprint 3 Evidence Profile scope

- Completed: Graded the July 20 WNBA slate at 3-7 and established the updated pre-Sprint-3 replay baseline of 62-70-1 at 46.62%, with production and simulation identical and zero changed recommendations. Built and independently tested the pure `build_evidence_profile` metadata helper in `analysis/historical_analysis.py`; Git showed that helper was still uncommitted when this entry was added.
- Decisions and architecture: **The Evidence Profile is intentionally descriptive only. It reports factual metadata about the evidence used during analysis and does not evaluate, score, or influence recommendations. Future confidence work will consume this metadata rather than having the Evidence Profile assign quality labels directly.** Sprint 3 remains non-behavioral and is the final sprint before this repository is temporarily put on the shelf while the user begins a different project in a new repository. Complete the agreed deliverables without expanding the sprint into reliability scoring, confidence redesign, new configuration, or unrelated cleanup.
- Next steps: Commit the pure Evidence Profile builder first. Then attach the profile additively to the WNBA analysis object without passing it to `get_basic_recommendation`; verify profile population and the unchanged 62-70-1 replay baseline; update architecture documentation; and finish the sprint with a concise final handoff suitable for shelving and later resumption.
- Known issues: The builder and this continuity entry were uncommitted when the entry was written. Existing replay look-ahead, Goblin/Demon replay divergence, fixed WNBA season, and player-name matching concerns remain out of scope unless they directly block Sprint 3 verification.
- Verification: The builder compiled and passed `git diff --check` plus isolated tests covering valid/missing stat rows, full/short recent windows, opponent and home/away counts, missing optional columns, date normalization, invalid/missing dates, and season passthrough. No recommendation path calls the builder yet.

### 2026-07-20 14:54 EDT — Complete configuration sprints and prepare Evidence Profile foundation

- Completed: Finished and separately committed configurable hit-rate thresholds across the replay, WNBA, and recommendation layers; named the production threshold defaults; added current/simulated threshold reporting; and renamed the simulation entry point to `run_engine_simulation`. Default replay remained 59-63-1 at 47.97% with zero recommendation changes; a 70/40 threshold simulation changed three recommendations. Imported and analyzed the July 20 WNBA slate, added the `SKIPPED` paper-bet status, and retired all 15 ungraded June 19 rows. Added the browser ChatGPT update workflow. Performed read-only inventories of recommendation rules and Evidence Quality opportunities.
- Decisions and architecture: Configurable Weights and Configurable Thresholds are complete. Replay remains the translation boundary, while sport analysis and `get_basic_recommendation` receive only explicit values. The next sprint is **Sprint 3: Evidence Profile Foundation**, an intentionally non-behavioral metadata sprint. Evidence Profile belongs in the existing analysis layer, will be returned as part of the analysis object, and must remain independent from recommendation scoring, confidence, market rules, replay logic, and `engine_config`. Begin with factual metadata only—no reliability score or HIGH/MEDIUM/LOW label. The future pipeline is signal values to recommendation scoring, evidence facts to a separate Evidence Quality evaluator, and both feeding a later independent confidence engine.
- Next steps: No Sprint 3 code has been written yet. Start by adding a pure `build_evidence_profile` skeleton at the bottom of `analysis/historical_analysis.py` with parameters `player_logs`, `stat_type`, optional `opponent`, `recent_game_window=10`, `location_column="team_location"`, `opponent_column="opponent"`, and optional `data_season`; add a factual-only docstring and temporary `pass`. Then populate and independently verify total rows, valid/missing stat rows, requested/available recent games, opponent count, home/away counts, earliest/latest game dates, and data season. Commit the pure builder before attaching it to the WNBA analysis return object. After integration, prove recommendation, confidence, and the 59-63-1 replay baseline remain identical, then document the architecture.
- Known issues: Historical replay does not pass the historical prop date into WNBA analysis and may have look-ahead leakage. Replay bypasses the production Goblin/Demon MORE-only override in `compare_props`. WNBA uses fixed season `2025`, exact player-name matching, and currently misses some players. Evidence sample counts, missingness, provenance, and opponent matchup counts are not yet retained. Local `main` was nine commits ahead of `origin/main` before this handoff entry.
- Verification: Configuration-layer Python files compiled; `git diff --check` passed; mocked router/report checks proved explicit configuration translation and both unchanged/changed threshold reporting; full default replay matched production exactly; alternate 70/40 replay produced the expected controlled changes. July 20 import produced 20 valid WNBA rows and saved 15 analyses; June 19 verification showed 0 pending and 15 skipped. Sprint 3 remained read-only, so no Evidence Profile behavior has been tested yet.

### 2026-07-18 16:24 EDT - Prepare configurable-threshold sprint

- Completed: Renamed the What-If simulation parameter from `custom_weights` to `engine_config`, then introduced the first structured configuration section, `engine_config["indicator_weights"]`, in separate verified commits. `run_weight_simulation` and `replay_single_prop` extract simulated weights; `replay_historical_props` forwards the complete configuration. Confirmed the WNBA and recommendation layers still receive only the weight dictionary. Added direct `python -c` and multiline PowerShell here-string techniques to the separate Developer Playbook and synchronized both repositories.
- Decisions and architecture: Continue deliberate small refactors using rename -> verify -> commit, then structure -> verify -> commit. `engine_config` is the simulation source of truth, while the replay layer is the translation boundary that narrows it into explicit downstream arguments. Sport analysis and `get_basic_recommendation` must remain unaware of the broad configuration object. Defer configuration validation until the shape stabilizes, unless multiple constructors, external input, or contract-related bugs justify it sooner.
- Next steps: Begin a sprint that adds configurable hit-rate thresholds as the second independent `engine_config` section. First trace the existing `hit_rate_high_threshold` and `hit_rate_low_threshold` parameters from `get_basic_recommendation` through WNBA analysis and replay. Then design the minimal `thresholds` section, pass explicit threshold values across the replay translation boundary, verify that default values preserve current replay results, and prove alternate values can change results. Keep each conceptual change separately verified and committed.
- Known issues: The What-If replay router currently supports WNBA only. Weight comparison tolerates missing simulated weights, but recommendation scoring requires a complete weight dictionary; validation is intentionally postponed. The configuration currently has only `indicator_weights`, and the development invocation is its only constructor. In Windows PowerShell, multiline Python passed through `$code` required single-quoted Python dictionary keys to avoid native-command quote loss; this is documented in the Developer Playbook.
- Verification: Ran Python compilation and import checks, `git diff --check`, and the full What-If historical replay. The structured configuration produced the same results as the flat-dictionary baseline with default behavior, and changing the simulated hit-rate weight executed without errors. Confirmed no remaining active WNBA boundary treats the complete `engine_config` as a flat weight dictionary. Before this handoff edit, PrizePicks `main` was synchronized at `b9bc5f3` and Developer Playbook `main` at `ddfd32b`.

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

