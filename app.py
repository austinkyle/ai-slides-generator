#!/usr/bin/env python3
"""
app.py — Flask web server for the AI Slides Generator.

Routes:
  GET  /         — Serve the single-page frontend
  POST /upload   — Accept .docx, start pipeline in background thread
  GET  /status   — Return current pipeline state as JSON
  GET  /download — Stream the finished .pptx file
  POST /reset    — Reset pipeline state to idle
"""

import sys
import threading
import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, send_file
from werkzeug.utils import secure_filename

load_dotenv()

BASE_DIR = Path(__file__).parent.resolve()
RESOURCES_DIR = BASE_DIR / "temp" / "resources"
OUTPUTS_DIR = BASE_DIR / "temp" / "outputs"

RESOURCES_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)

_lock = threading.Lock()
_state = {
    "status": "idle",   # idle | processing | complete | error
    "stage": None,      # uploading | extracting | building
    "filename": None,
    "error": None,
}


def _set(**kwargs):
    with _lock:
        _state.update(kwargs)


def _run_pipeline(docx_path: Path):
    """Background thread: extract JSON → build PPTX."""
    import subprocess

    try:
        # Stage 1: call Claude API to extract slide structure
        _set(status="processing", stage="extracting", error=None)
        r = subprocess.run(
            [sys.executable, "tools/extract_slides_content.py", "--input", str(docx_path)],
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
        )
        if r.returncode != 0:
            msg = (r.stderr or r.stdout or "extract_slides_content failed").strip()
            # Trim long stack traces to last 500 chars for readable error messages
            _set(status="error", stage=None, error=msg[-500:])
            return

        # Stage 2: build PPTX from extracted JSON
        json_path = OUTPUTS_DIR / "slides_content.json"
        _set(stage="building")
        r = subprocess.run(
            [sys.executable, "tools/build_slides.py", "--input", str(json_path)],
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
        )
        if r.returncode != 0:
            msg = (r.stderr or r.stdout or "build_slides failed").strip()
            _set(status="error", stage=None, error=msg[-500:])
            return

        # Find the most recently written .pptx in outputs
        candidates = sorted(OUTPUTS_DIR.glob("*.pptx"), key=lambda p: p.stat().st_mtime)
        if not candidates:
            _set(status="error", stage=None, error="Pipeline finished but no .pptx was produced.")
            return

        _set(status="complete", stage=None, filename=candidates[-1].name)

    except Exception as exc:
        _set(status="error", stage=None, error=str(exc))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    with _lock:
        if _state["status"] == "processing":
            return jsonify({"error": "Pipeline is already running. Please wait."}), 409

    if "file" not in request.files:
        return jsonify({"error": "No file field in request."}), 400

    f = request.files["file"]
    if not f.filename:
        return jsonify({"error": "No file selected."}), 400

    filename = secure_filename(f.filename)
    if not filename.lower().endswith(".docx"):
        return jsonify({"error": "Only .docx files are supported."}), 400

    save_path = RESOURCES_DIR / filename
    f.save(str(save_path))

    _set(status="processing", stage="uploading", filename=None, error=None)
    threading.Thread(target=_run_pipeline, args=(save_path,), daemon=True).start()

    return jsonify({"status": "processing"})


@app.route("/status")
def status():
    with _lock:
        return jsonify(dict(_state))


@app.route("/download")
def download():
    with _lock:
        if _state["status"] != "complete":
            return jsonify({"error": "No file ready for download."}), 404
        filename = _state["filename"]

    path = OUTPUTS_DIR / filename
    if not path.exists():
        return jsonify({"error": "Output file not found on disk."}), 404

    return send_file(str(path), as_attachment=True, download_name=filename)


@app.route("/reset", methods=["POST"])
def reset():
    _set(status="idle", stage=None, filename=None, error=None)
    return jsonify({"status": "idle"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"Starting AI Slides Generator on http://localhost:{port}")
    app.run(debug=True, host="0.0.0.0", port=port)
