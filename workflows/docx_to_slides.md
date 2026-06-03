# Workflow: Docx to Slides

**Goal:** Convert a `.docx` document into a styled `.pptx` slide deck. Claude AI
reads the full document and intelligently organizes the content into slides.

**Inputs:**
- A `.docx` file in `temp/resources/`
- `ANTHROPIC_API_KEY` in `.env`

**Outputs:**
- `temp/outputs/slides_content.json` — intermediate structured slide content
- `temp/outputs/slides_<title>.pptx` — the final presentation file

---

## Steps

### Step 1 — Confirm Input File

Scan `temp/resources/` for `.docx` files.

- **One file found** → use it and proceed to Step 2.
- **Multiple files found** → list them and ask the user which one to process.
- **No files found** → stop. Ask the user to place a `.docx` file in
  `temp/resources/` before continuing.

### Step 2 — Verify Environment

Check that `.env` exists at the project root and contains `ANTHROPIC_API_KEY`.
If the key is missing or `.env` does not exist, stop and notify the user. Do
not proceed without a valid API key.

### Step 3 — Extract Slide Content via Claude API

Run (replace `<path>` with the `.docx` file path identified in Step 1):

```
python3 tools/extract_slides_content.py --input <path>
```

Show tool output to the user as it runs. If the tool exits with a non-zero
code, stop, display the error output, and do not proceed to Step 4.

On success, report: "Extracted N slides from the document."

### Step 4 — Review Extracted Content (Optional)

Ask the user: "Claude extracted N slides. Would you like to review the outline
before I build the deck, or shall I proceed?"

- **Review requested** → read `temp/outputs/slides_content.json` and print a
  clean numbered outline: slide number, type, title, and bullet count. Wait for
  the user to confirm before continuing.
- **Proceed** → go directly to Step 5.

### Step 5 — Build the PowerPoint Deck

Run:

```
python3 tools/build_slides.py --input temp/outputs/slides_content.json
```

Show tool output as it runs. If the tool exits with a non-zero code, stop,
display the error, and ask the user how to proceed.

On success, confirm the output `.pptx` file path to the user.

### Step 6 — Confirm Completion

Report:

- Output file path (e.g. `temp/outputs/slides_q3_strategy_review.pptx`)
- Total slide count
- Accent color used
- Any warnings from the tools

Then ask: "The deck is ready. Would you like to adjust anything — slide count,
theme, or specific content?"
