# CLAUDE.md — Master Configuration for SLIDES GENERATOR WORKFLOW

This file is read by Claude Code at the start of every session. It defines the
project's structure, operating framework, and behavioral rules for the agent.

---

## The WAT Framework

This project is organized around the **WAT framework** — a three-part model for
structured agentic work:

| Letter | Stands For | What It Is |
|--------|------------|------------|
| **W**  | Workflows  | Step-by-step procedure files that define what gets done and in what order |
| **A**  | Agent      | Claude Code — the AI that reads the workflows, plans the steps, and executes them |
| **T**  | Tools      | Scripts and integrations the agent invokes to perform real work |

How the pieces fit together:

1. A **Workflow** describes a goal as an ordered sequence of steps.
2. Each step instructs the **Agent** (Claude Code) to do something — call a tool,
   read a file, make a decision, write an output.
3. The **Tools** are the executables, scripts, and API integrations the agent
   invokes to perform real work (file I/O, API calls, data transforms, content
   generation, etc.).

The agent is the connective tissue. Workflows and tools are inert without it.

---

## Folder Structure

```
SLIDES GENERATOR WORKFLOW/
├── CLAUDE.md              ← You are here. Master config for Claude Code.
├── .env                   ← API keys and secrets. NEVER commit this file.
├── .gitignore             ← Excludes .env and temp/ from version control.
├── workflows/             ← Workflow definition files (Markdown)
│   └── README.md          ← Index of available workflows
├── tools/                 ← Scripts and integrations the agent can run
│   └── README.md          ← Index of available tools and their usage
└── temp/                  ← Temporary working files (do not commit)
    ├── outputs/           ← Files produced by workflow runs (slides, exports)
    └── resources/         ← Input files and assets consumed by workflows
```

### Folder Purposes

**`/workflows/`**
Contains one file per workflow. Each workflow file describes a goal and breaks
it into numbered, actionable steps. Steps may instruct the agent to call a
tool, read or write a file, ask a clarifying question, or branch on a
condition. Workflows are the source of truth for "what are we trying to do."

**`/tools/`**
Contains scripts, CLI wrappers, and integration modules the agent executes.
Each tool should do one thing well. Tools are called by name from workflow
steps. Document every tool in `tools/README.md` with its name, purpose,
inputs, and outputs.

**`/temp/`**
Scratch space for the current session. Nothing here is permanent.

- `temp/outputs/` — files the agent writes as results of workflow runs
  (generated slide decks, exported PDFs, content drafts, etc.)
- `temp/resources/` — input files, uploaded assets, reference material,
  or downloaded content the agent needs during a run

The `temp/` tree is in `.gitignore`. Treat it as disposable.

**`.env`**
Holds API keys, secrets, and environment-specific configuration. Never read
aloud, never logged, never committed to version control.

---

## How Claude Code Should Behave in This Project

### Session Start

- Read this file (`CLAUDE.md`) at the start of every session before doing
  anything else.
- Check `workflows/README.md` for available workflow files.
- Load `.env` from the project root before running any workflow or tool.

### Reading and Running Workflows

- When a user names a workflow or describes a goal, find the matching file in
  `workflows/` and read it in full before taking any action.
- Execute workflow steps in order unless a step explicitly defines branching.
- Before starting a multi-step or destructive workflow, state the plan (brief
  summary of steps) and confirm with the user.
- If a step is ambiguous, pause and ask a clarifying question rather than
  guessing.
- Report progress as you go (e.g., "Completed step 2 of 5").

### Using Tools

- Tools live in `tools/`. Before calling a tool, confirm it exists in that
  directory and that you understand its expected inputs and outputs.
- Check `tools/README.md` for documented usage. Do not improvise tool
  invocations or pass undocumented flags without stating your reasoning.
- If a tool fails, report the error clearly, do not silently retry more than
  once, and surface the failure to the user before continuing.
- Never call a tool that sends external requests (API writes, emails,
  webhooks) or modifies production data without explicit user confirmation.

### Handling Temp Files

- Write all intermediate and final outputs to `temp/outputs/`.
- Place any input files, uploaded assets, or downloaded resources in
  `temp/resources/`.
- Do not treat anything in `temp/` as reliable across sessions — regenerate
  or re-fetch if needed.
- Do not delete or clean `temp/` unless the user explicitly asks.

### Conventions

- **Never modify workflow files** (`/workflows/`) without being explicitly
  told to do so by the user.
- **Never modify tool files** (`/tools/`) without being explicitly told to
  do so by the user.
- **Never commit files, push to remotes, or make external API calls** unless
  a workflow step or the user explicitly instructs it.
- **Never print or include `.env` values** in chat responses, output files,
  or logs.
- **Ask, don't assume.** When scope or intent is unclear, ask one focused
  question rather than proceeding on assumptions.

---

## Environment Variables (.env)

The `.env` file at the project root holds secrets and configuration values.

Rules:
- Load `.env` at the start of each session before running any workflow or tool.
- Never print, log, or include `.env` values in output files or chat responses.
- Never commit `.env` to version control — it is listed in `.gitignore`.
- If a required key is missing from `.env`, stop and notify the user before
  proceeding. Do not attempt to work around missing credentials.

Expected format:

```
# .env — API keys and secrets for SLIDES GENERATOR WORKFLOW
# Do not commit this file.

ANTHROPIC_API_KEY=your_key_here
SOME_SLIDES_API_KEY=your_key_here
```

---

## Quick Reference

| What you want to do              | Where to look / what to do                         |
|----------------------------------|----------------------------------------------------|
| Run a workflow                   | Find the file in `workflows/`, read it, execute    |
| See available workflows          | Read `workflows/README.md`                         |
| Add a new workflow               | Create a `.md` file in `workflows/`, update README |
| Call a tool                      | Find the script in `tools/`, check `tools/README.md` |
| Add a new tool                   | Add script to `tools/`, update `tools/README.md`   |
| Store a result or generated deck | Write to `temp/outputs/`                           |
| Use an input file or asset       | Place it in `temp/resources/`                      |
| Add an API key                   | Add to `.env`, never commit                        |
| Change agent behavior            | Edit this file (`CLAUDE.md`)                       |
| Change a workflow procedure      | Edit the relevant file in `workflows/`             |

---

*Last updated: 2026-05-29*
