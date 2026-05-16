# Retentio

Retentio is an AI-assisted autobiographical memory reconstruction system that helps people reconnect with forgotten moments from fragmented life traces: photos, text notes, voice memos, places, and dates.

This repository contains a polished hackathon-ready MVP built with Python, Gradio, the OpenAI API, and the Tavily API.

## MVP Features

- Upload photos, text fragments, and voice notes
- Generate reconstructed autobiographical memory timelines
- Create emotional and contextual summaries
- Retrieve historical, cultural, and local context through Tavily
- Present reconstructed memories in a minimal cinematic Gradio interface
- Run with demo data even when API keys are not configured

## Project Structure

```text
/frontend       Gradio interface and visual presentation
/backend        App orchestration and request handling
/memory_engine  AI reconstruction, transcription, context retrieval
/demo_data      Sample fragments for demos and hackathon walkthroughs
/assets         Design notes and static asset placeholders
app.py          Application entrypoint
requirements.txt
```

## Quickstart

1. Create and activate a virtual environment.

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Add API keys as environment variables.

```bash
export OPENAI_API_KEY="your-openai-key"
export TAVILY_API_KEY="your-tavily-key"
```

On Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="your-openai-key"
$env:TAVILY_API_KEY="your-tavily-key"
```

4. Run the app.

```bash
python app.py
```

Open the local Gradio URL printed in the terminal.

## Demo Flow

1. Paste a few fragments from `demo_data/sample_fragments.txt`.
2. Upload one or more meaningful images.
3. Optionally upload a short voice note.
4. Add a place, year, or remembered detail in the context box.
5. Click **Reconstruct Memory**.

Without API keys, Retentio returns a graceful deterministic reconstruction so the UI remains demoable.

## Environment Variables

- `OPENAI_API_KEY`: Enables AI timeline reconstruction and voice transcription.
- `TAVILY_API_KEY`: Enables contextual web retrieval.
- `OPENAI_MODEL`: Optional, defaults to `gpt-4o-mini`.

## Hackathon Scope

This MVP is intentionally lean. It focuses on the emotional interaction loop: collect traces, enrich context, reconstruct a timeline, and show the result beautifully. It is not a production memory vault, user account system, or long-term storage layer yet.
