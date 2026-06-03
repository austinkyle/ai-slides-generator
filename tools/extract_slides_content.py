#!/usr/bin/env python3
"""
extract_slides_content.py — Reads a .docx file, calls the Claude API to extract
and structure slide content, and writes slides_content.json to temp/outputs/.

Usage:
  python3 tools/extract_slides_content.py --input temp/resources/report.docx
"""

import argparse
import json
import os
import re
import sys

import anthropic
from docx import Document
from dotenv import load_dotenv

load_dotenv()

TAG = "[extract_slides_content]"

SYSTEM_PROMPT = (
    "You are a presentation architect. Analyze documents and reorganize their "
    "content into clear, compelling slide deck structures. "
    "Return only valid JSON — no prose, no markdown fences, no commentary."
)

USER_PROMPT_TEMPLATE = """\
Analyze the following document and extract its content into a slide deck structure.

Rules:
1. Create exactly one title slide (first), body content slides, and exactly one closing slide (last).
2. Limit each slide to one focused idea. Do not overcrowd slides.
3. Bullet points must be concise — 10 words or fewer per bullet.
4. Aim for 8–16 slides total, scaled to content density.
5. The closing slide should be a call to action, key takeaway, or "Thank You."
6. Choose one thematic accent hex color (e.g. "#E63946") that fits the document's tone and subject.

Return ONLY valid JSON matching this exact schema — nothing else:

{{
  "deck_title": "string",
  "accent_color": "#RRGGBB",
  "slides": [
    {{
      "type": "title",
      "title": "string",
      "subtitle": "string or null"
    }},
    {{
      "type": "content",
      "title": "string",
      "bullets": ["string", "string"]
    }},
    {{
      "type": "closing",
      "title": "string",
      "subtitle": "string or null"
    }}
  ]
}}

Constraints:
- First slide type MUST be "title"
- Last slide type MUST be "closing"
- All other slides MUST have type "content"
- Each content slide MUST have a non-empty "bullets" array

DOCUMENT TEXT:
---
{doc_text}
---"""


def extract_docx_text(path):
    doc = Document(path)
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    return "\n\n".join(paragraphs)


def validate_schema(data):
    required = {"deck_title", "accent_color", "slides"}
    missing = required - data.keys()
    if missing:
        raise ValueError(f"Missing top-level keys: {missing}")

    if not re.match(r"^#[0-9A-Fa-f]{6}$", data["accent_color"]):
        raise ValueError(f"Invalid accent_color: {data['accent_color']!r}")

    slides = data["slides"]
    if not slides:
        raise ValueError("slides array is empty")
    if slides[0].get("type") != "title":
        raise ValueError("First slide must have type 'title'")
    if slides[-1].get("type") != "closing":
        raise ValueError("Last slide must have type 'closing'")
    for i, slide in enumerate(slides[1:-1], start=2):
        if slide.get("type") != "content":
            raise ValueError(
                f"Slide {i} must have type 'content', got {slide.get('type')!r}"
            )
        if not slide.get("bullets"):
            raise ValueError(f"Slide {i} (content) has no bullets")


def find_output_dir(input_path):
    abs_path = os.path.abspath(input_path)
    parts = abs_path.split(os.sep)
    for i, part in enumerate(parts):
        if part == "temp":
            project_root = os.sep.join(parts[:i])
            return os.path.join(project_root, "temp", "outputs")
    return os.path.join(os.getcwd(), "temp", "outputs")


def main():
    parser = argparse.ArgumentParser(
        description="Extract slide content from a .docx via Claude API"
    )
    parser.add_argument("--input", required=True, help="Path to the .docx file")
    args = parser.parse_args()

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print(f"{TAG} ERROR — ANTHROPIC_API_KEY not found in .env")
        sys.exit(1)

    if not os.path.exists(args.input):
        print(f"{TAG} ERROR — Input file not found: {args.input}")
        sys.exit(1)

    print(f"{TAG} Reading document: {args.input}")
    doc_text = extract_docx_text(args.input)
    print(f"{TAG} Extracted {len(doc_text):,} characters of text.")

    if len(doc_text) < 50:
        print(f"{TAG} ERROR — Document appears to be empty or has very little text.")
        sys.exit(1)

    model = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")
    print(f"{TAG} Calling Claude API ({model})...")

    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model=model,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": USER_PROMPT_TEMPLATE.format(doc_text=doc_text),
            }
        ],
    )

    raw = message.content[0].text.strip()
    print(f"{TAG} Received response. Validating JSON schema...")

    # Strip markdown fences if Claude added them despite instructions
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\n?", "", raw)
        raw = re.sub(r"\n?```$", "", raw)
        raw = raw.strip()

    out_dir = find_output_dir(args.input)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "slides_content.json")
    raw_path = os.path.join(out_dir, "claude_raw_response.txt")

    try:
        data = json.loads(raw)
        validate_schema(data)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"{TAG} ERROR — {e}")
        with open(raw_path, "w", encoding="utf-8") as f:
            f.write(raw)
        print(f"{TAG} Raw response saved to: {raw_path}")
        sys.exit(1)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    n_slides = len(data["slides"])
    print(f"{TAG} SUCCESS — wrote {out_path} ({n_slides} slides)")


if __name__ == "__main__":
    main()
