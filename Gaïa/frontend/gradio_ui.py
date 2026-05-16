"""Gradio interface for Retentio."""

from __future__ import annotations

import gradio as gr

from backend.service import reconstruct_from_inputs

APP_CSS = """
:root {
  --retentio-ink: #f5efe7;
  --retentio-muted: #b9aaa0;
  --retentio-bg: #11100f;
  --retentio-panel: rgba(255, 255, 255, 0.055);
  --retentio-line: rgba(255, 255, 255, 0.13);
  --retentio-accent: #d7a86e;
}

.gradio-container {
  background:
    radial-gradient(circle at 20% 0%, rgba(215, 168, 110, 0.16), transparent 28rem),
    linear-gradient(135deg, #11100f 0%, #171513 46%, #0b0b0d 100%);
  color: var(--retentio-ink);
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

#retentio-shell {
  max-width: 1180px;
  margin: 0 auto;
  padding: 30px 18px 42px;
}

#retentio-title h1 {
  font-size: clamp(2.3rem, 5vw, 5.4rem);
  line-height: 0.95;
  letter-spacing: 0;
  margin-bottom: 0.65rem;
  color: var(--retentio-ink);
}

#retentio-title p {
  max-width: 720px;
  color: var(--retentio-muted);
  font-size: 1.05rem;
}

.retentio-panel {
  background: var(--retentio-panel);
  border: 1px solid var(--retentio-line);
  border-radius: 8px;
  box-shadow: 0 24px 80px rgba(0, 0, 0, 0.28);
  backdrop-filter: blur(16px);
}

.retentio-output {
  min-height: 540px;
}

button.primary {
  background: linear-gradient(135deg, #f0c68f, #a96f43) !important;
  border: 0 !important;
  color: #17100b !important;
  font-weight: 760 !important;
}

textarea, input, .wrap, .block, .form, .panel, .tabs {
  border-radius: 8px !important;
}

label, .prose p, .prose li {
  color: var(--retentio-muted) !important;
}

.prose h1, .prose h2, .prose h3 {
  color: var(--retentio-ink) !important;
  letter-spacing: 0;
}

.prose a {
  color: var(--retentio-accent) !important;
}
"""

INTRO = """
# Retentio
Fragments become a memory you can stand inside again.
"""

PLACEHOLDER_OUTPUT = """
# Waiting For Traces

Upload a photo, paste fragments, or add a voice note. Retentio will reconstruct a careful timeline, emotional summary, and contextual frame.
""".strip()

DEMO_FRAGMENTS = """summer evening, train platform, orange light on the glass
my mother laughing about the suitcase wheel
I remember the smell of rain on warm pavement
maybe Lyon, maybe 2012, on the way back from the coast"""


def build_interface() -> gr.Blocks:
    with gr.Blocks(css=APP_CSS, title="Retentio") as demo:
        with gr.Column(elem_id="retentio-shell"):
            gr.Markdown(INTRO, elem_id="retentio-title")

            with gr.Row(equal_height=False):
                with gr.Column(scale=5, elem_classes=["retentio-panel"]):
                    text_fragments = gr.Textbox(
                        label="Fragments",
                        placeholder="Paste remembered words, dates, places, objects, messages, lyrics, smells, or half-scenes.",
                        lines=10,
                        value=DEMO_FRAGMENTS,
                    )
                    user_context = gr.Textbox(
                        label="Known context",
                        placeholder="Place, approximate year, people, mood, or anything that may help Retentio search context.",
                        lines=4,
                    )
                    photos = gr.Files(
                        label="Photos",
                        file_count="multiple",
                        file_types=["image"],
                    )
                    voice_note = gr.Audio(
                        label="Voice note",
                        type="filepath",
                    )
                    reconstruct_btn = gr.Button("Reconstruct Memory", variant="primary")

                with gr.Column(scale=7, elem_classes=["retentio-panel", "retentio-output"]):
                    output = gr.Markdown(PLACEHOLDER_OUTPUT)

            reconstruct_btn.click(
                fn=_handle_reconstruction,
                inputs=[text_fragments, photos, voice_note, user_context],
                outputs=output,
            )

    return demo


def _handle_reconstruction(
    text_fragments: str,
    photos: list[str] | None,
    voice_note: str | None,
    user_context: str,
) -> str:
    memory = reconstruct_from_inputs(
        text_fragments=text_fragments or "",
        photo_files=photos or [],
        voice_note=voice_note,
        user_context=user_context or "",
    )
    return memory.to_markdown()
