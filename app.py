"""Retentio application entrypoint."""

from dotenv import load_dotenv

from frontend.gradio_ui import build_interface


def main() -> None:
    load_dotenv()
    demo = build_interface()
    demo.launch()


if __name__ == "__main__":
    main()
