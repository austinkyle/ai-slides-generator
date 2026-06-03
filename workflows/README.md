# Workflows

Each file in this folder defines one workflow — a numbered, step-by-step procedure that Claude Code executes.

## Available Workflows

| File | Description |
|------|-------------|
| `docx_to_slides.md` | Convert a `.docx` document to a `.pptx` slide deck using Claude AI |

## How to Add a Workflow

1. Create a new `.md` file in this folder (e.g., `generate_slides.md`).
2. Structure it as a numbered list of steps.
3. Add a row to the table above.

## Workflow File Template

```markdown
# Workflow Name

**Goal:** One sentence describing what this workflow produces.

**Inputs:** What the agent needs before starting (files, user input, env vars).

**Outputs:** What gets written to `temp/outputs/`.

---

## Steps

1. Step one — what to do and where to look.
2. Step two — call tool `tools/some_script.py` with input from `temp/resources/`.
3. Step three — write result to `temp/outputs/result.md`.
4. Step four — confirm output with user.
```
