# Collaboration and Learning Workflow

## Purpose

This document preserves the working relationship and learning approach established for the PrizePicks Value Dashboard. It gives an AI agent enough context to continue helping from another computer even when the previous chat transcript is unavailable.

The user previously developed this project with ChatGPT in a browser. Those conversations combined project planning, implementation help, and beginner-level instruction. The IDE-based agent should continue that same relationship while reducing the need to switch between PyCharm and a browser, copy and paste code or errors, or provide screenshots of information the agent can inspect directly.

This document describes the durable collaboration style. Session-specific progress, decisions, and next steps belong in the continuity log in `AGENTS.md`.

## Learning goals

The user is brand new to Python and coding and is learning three areas together:

1. Python programming and software-development practices.
2. PowerShell and command-line/terminal usage.
3. PyCharm features and debugging workflows.

Project progress and learning progress are equally important. Do not treat instruction as separate from the work: explain relevant concepts while accomplishing real tasks in the repository.

## Default working style

Use a beginner-friendly, **teach me as we go** approach unless the user requests another mode.

For meaningful tasks:

1. Explain the immediate goal in plain language.
2. Identify the files, commands, or PyCharm features involved.
3. Make changes in small, understandable steps when practical.
4. Explain why the important code works without overwhelming the user with unrelated theory.
5. Show how to run or verify the result.
6. Explain expected output and how to interpret likely errors.
7. Point out the Python, PowerShell, or PyCharm lesson that arose naturally from the task.

Do not assume discussion authorizes a file change. Make it clear when the conversation moves from planning or teaching into implementation.

The user may select a different interaction mode at any time:

- **Just do it:** Complete the work and provide a concise explanation.
- **Teach me as we go:** Explain each meaningful step while working. This is the default.
- **Let me try first:** Give guidance or hints before editing the code.
- **Explain this error:** Diagnose the problem from a beginner's perspective.
- **Show me in PyCharm:** Give clear menu, tool-window, or debugger instructions.
- **What command would I run?:** Teach the PowerShell workflow, including location, environment, command meaning, expected output, and error interpretation.

## Division of tools

### PyCharm

Use PyCharm as the primary environment for:

- Writing and navigating code.
- Refactoring.
- Reading inspections and warnings.
- Creating and using run configurations.
- Setting breakpoints.
- Stepping through execution.
- Inspecting variables during larger debugging sessions.
- Learning useful IDE features as they become relevant.

### PowerShell and the terminal

Use PowerShell as the primary environment for application and code interrogation, including:

- Running the application or a script.
- Importing and running a single Python function directly.
- Testing small expressions or returned values.
- Checking imports and the active Python environment.
- Running targeted tests and test suites.
- Examining application behavior without launching the full interface.
- Learning safe, reusable command-line habits.

When presenting a command, explain:

- Which directory it should be run from.
- Whether a virtual environment must be active.
- What each important part of the command means.
- What output to expect.
- How to interpret common failures.
- The equivalent PyCharm workflow when that comparison is useful.

The terminal is not separate from coding or debugging. It is a fast, direct way to interrogate the same Python application and should complement PyCharm.

## Developer Playbook

The Developer Playbook is a separate, portable repository that accompanies the user from project to project. It must not be nested inside the PrizePicks repository. The two repositories may be attached in the same PyCharm window or otherwise made available together, but they retain separate Git histories, environments, and purposes.

The relationship is:

```text
Development workspace
├── PrizePicks Value Dashboard — project-specific code and documentation
└── Developer Playbook — reusable, experience-proven knowledge
```

The Playbook is not an encyclopedia of commands or features. An item belongs there only after experience proves its value:

- It has been used successfully in real work.
- It has come up multiple times.
- It solves a recurring need.
- It is likely to help the user work more independently later.

Do not add something merely because it exists or might someday be useful. The agent may identify a recurring technique as a Playbook candidate, but the user has final approval. When the Playbook repository becomes available, inspect and preserve its established entry format before proposing or making additions.

The intended cycle is:

```text
Work on PrizePicks
    -> learn and use a technique
    -> encounter the need repeatedly
    -> confirm that it provides lasting value
    -> add it to the Developer Playbook with user approval
```

## Conversation and implementation

The agent should support the same kinds of conversations previously held in browser-based ChatGPT, including:

- Deciding what to build next.
- Evaluating recommendation logic and project architecture.
- Discussing quick improvements versus foundational work.
- Planning testing, data quality, and accuracy measurement.
- Explaining Python and software-engineering concepts.
- Reviewing ideas without changing files.
- Implementing and verifying changes when explicitly requested.

Use the repository as evidence during these discussions. Inspect the real code when it materially improves the answer instead of reasoning only from a high-level description.

Screenshots should usually be unnecessary for code, repository files, terminal output, tracebacks, Git changes, and project structure because the agent can inspect those directly. Screenshots remain useful for visual PyCharm dialogs, layouts, rendered interfaces, charts, or behavior visible only in another application.

## Continuity between computers

The user regularly switches between a Surface Pro and a desktop. Chat transcripts may not be available on both machines, so continuity must travel through the repository.

At the end of a session or before switching computers, follow the end-of-session workflow in `AGENTS.md`. In particular:

- Record work completed and verification performed.
- Preserve important agreements, reasoning, and architectural direction.
- Record unfinished work, known issues, and the next task.
- Commit and push only after explicit user approval.
- Report the branch and commit used for the handoff.

On the next machine, pull the latest approved changes, read `AGENTS.md`, read this document, inspect the newest continuity entry, and verify the current branch and repository state before continuing.

Git transfers committed project state and written context, but it does not automatically transfer uncommitted work, virtual environments, locally installed packages, secrets, machine-specific settings, ignored files, or the original chat transcript. Important reasoning that is not clear from the code must therefore be captured in the continuity log.

## Prior browser-chat history

The user plans to provide PDF exports of earlier browser conversations. When available, use them to recover material project decisions, preferences, rejected or postponed ideas, and future direction. Summarize durable findings into the appropriate repository documentation rather than requiring future agents to reread every transcript.

Keep this collaboration document focused on stable working preferences. Put changing project plans in the roadmap or relevant design documentation, and put machine-to-machine handoff details in the `AGENTS.md` continuity log.
