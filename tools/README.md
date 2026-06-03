# Tools

Each file in this folder is a script or integration the agent can invoke during a workflow run.

## Available Tools

| File | Purpose | Inputs | Outputs |
|------|---------|--------|---------|
| `extract_slides_content.py` | Reads a `.docx`, calls Claude API to extract structured slide content, writes `slides_content.json` | `--input <path/to/file.docx>` | `temp/outputs/slides_content.json` |
| `build_slides.py` | Reads `slides_content.json` and builds a dark/bold `.pptx` presentation | `--input <path/to/slides_content.json>` · `--output` (optional) | `temp/outputs/slides_<title>.pptx` |

## How to Add a Tool

1. Add a script to this folder (e.g., `generate_outline.py`).
2. Add a row to the table above documenting its name, purpose, inputs, and outputs.
3. Reference it by filename from workflow steps.

## Conventions

- Each tool should do one thing well.
- Tools read inputs from `temp/resources/` and write outputs to `temp/outputs/` unless a workflow step specifies otherwise.
- Tools should print clear success/error messages to stdout so the agent can report status.
- Never hardcode secrets — load them from `.env`.
