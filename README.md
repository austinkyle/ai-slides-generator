# AI Slides Generator

> Upload a Word doc. Get a PowerPoint. No manual steps.

A web-based tool that converts a `.docx` document into a fully styled PowerPoint presentation using the Claude API. Upload your file, watch the pipeline run in real time, and download a polished `.pptx` — all from the browser.

---

## How It Works

```
┌─────────────┐     ┌──────────────────────────┐     ┌──────────────────────┐     ┌─────────────┐
│  .docx file │────▶│  Claude API              │────▶│  Python PPTX builder │────▶│  .pptx file │
│  (upload)   │     │  (slide structure JSON)  │     │  (formatted slides)  │     │  (download) │
└─────────────┘     └──────────────────────────┘     └──────────────────────┘     └─────────────┘

Step 1: Flask server accepts the uploaded .docx
Step 2: extract_slides_content.py reads the document and asks Claude to structure
        the content into a JSON slide plan (title, bullets, accent color, etc.)
Step 3: build_slides.py reads the JSON and builds a dark-themed .pptx using python-pptx
Step 4: The browser polls /status until complete, then offers the download
```

---

## Tech Stack

| Layer     | Technology                        |
|-----------|-----------------------------------|
| Backend   | Python 3, Flask                   |
| AI        | Anthropic Claude API (claude-sonnet-4-6) |
| Slides    | python-pptx                       |
| Docs      | python-docx                       |
| Frontend  | Vanilla HTML / CSS / JavaScript   |
| Config    | python-dotenv                     |

---

## Folder Structure

```
ai-slides-generator/
├── app.py                  ← Flask web server (all API routes)
├── requirements.txt        ← Python dependencies
├── .env.example            ← Environment variable template
├── .gitignore
├── CLAUDE.md               ← WAT framework master config (for Claude Code)
│
├── templates/
│   └── index.html          ← Single-page web UI (dark theme, embedded CSS+JS)
│
├── tools/
│   ├── extract_slides_content.py  ← .docx → Claude API → slides_content.json
│   └── build_slides.py            ← slides_content.json → .pptx
│
├── workflows/
│   └── docx_to_slides.md   ← CLI workflow definition (for Claude Code terminal use)
│
└── temp/                   ← Auto-created at startup (gitignored)
    ├── resources/          ← Uploaded .docx files
    │   └── images/         ← Cached stock photos for slides
    └── outputs/            ← Generated JSON and .pptx files
```

---

## Setup & Installation

### 1. Clone the repo

```bash
git clone https://github.com/therealaustinkyle/ai-slides-generator.git
cd ai-slides-generator
```

### 2. Create a virtual environment (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and add your Anthropic API key:

```
ANTHROPIC_API_KEY=sk-ant-...
```

### 5. Run the server

```bash
python app.py
```

Open your browser to **[http://localhost:5000](http://localhost:5000)**

---

## Environment Variables

| Variable           | Required | Default            | Description                        |
|--------------------|----------|--------------------|------------------------------------|
| `ANTHROPIC_API_KEY`| Yes      | —                  | Your Anthropic API key             |
| `CLAUDE_MODEL`     | No       | `claude-sonnet-4-6`| Claude model to use for extraction |
| `SLIDE_FONT`       | No       | `Calibri`          | Font used in the generated slides  |

---

## API Endpoints

| Method | Path        | Description                                      |
|--------|-------------|--------------------------------------------------|
| GET    | `/`         | Serves the web interface                         |
| POST   | `/upload`   | Accepts `.docx`, starts the pipeline             |
| GET    | `/status`   | Returns `{status, stage, filename, error}`       |
| GET    | `/download` | Downloads the finished `.pptx`                   |
| POST   | `/reset`    | Resets pipeline state to `idle`                  |

---

## Screenshots

> _Coming soon — add screenshots after running a demo._

---

## Roadmap

- [ ] Cloud deployment (Render / Railway / Fly.io)
- [ ] Multi-template support (light theme, minimal, branded)
- [ ] Google Slides export via Google Slides API
- [ ] Streaming status via Server-Sent Events (replace polling)
- [ ] Drag-and-drop slide reordering before export
- [ ] PDF export option

---

## License

MIT
