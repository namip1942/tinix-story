"""
TiniX Story 1.0 - Main app
"""

import gradio as gr
from pathlib import Path
import os
import inspect

from locales.i18n import t
from core.logger import get_logger

logger = get_logger("app")
logger.info("=" * 60)
logger.info("TiniX Story 1.0 - Logger initialized")
logger.info("=" * 60)

WEB_HOST = os.getenv("NOVEL_TOOL_HOST", "0.0.0.0")
WEB_PORT = int(os.getenv("NOVEL_TOOL_PORT", os.getenv("PORT", "7860")))
WEB_SHARE = os.getenv("NOVEL_TOOL_SHARE", "false").lower() in ("1", "true", "yes")


def create_main_ui():
    """Create UI"""
    with gr.Blocks(title=t("app.title")) as app:
        gr.Markdown(f"""
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 20px;">
            <h1 style="color: white; margin: 0; font-size: 2.5em;">🚀 {t("app.title")}</h1>
            <h3 style="color: #f0f0f0; margin: 10px 0 0 0;">{t("app.subtitle")}</h3>
        </div>
        """)

        with gr.Tabs():
            from ui.create_tab import build_create_tab
            from ui.continue_tab import build_continue_tab
            from ui.rewrite_tab import build_rewrite_tab
            from ui.polish_tab import build_polish_tab
            from ui.export_tab import build_export_tab
            from ui.projects_tab import build_projects_tab
            from ui.settings_tab import build_settings_tab

            build_create_tab()
            build_continue_tab()
            build_rewrite_tab()
            build_polish_tab()
            build_export_tab()
            build_projects_tab()
            build_settings_tab()

        gr.Markdown("""
        <div style="text-align: center; padding: 15px; margin-top: 30px; border-top: 1px solid #e0e0e0; color: #666;">
            <p style="margin: 5px 0;">TiniX Story v1.0.0</p>
            <p style="margin: 5px 0; font-size: 0.8em; color: #999;">Made with ❤️ by TiniX AI</p>
        </div>
        """)

    return app


def load_custom_css() -> str:
    """Load custom.css if exists."""
    css_path = Path("custom.css")
    if css_path.exists():
        return css_path.read_text(encoding="utf-8")
    return ""


def main():
    """Start app"""
    logger.info(t("app.startup_log"))

    app = create_main_ui()
    custom_css = load_custom_css()

    launch_kwargs = {
        "server_name": WEB_HOST,
        "server_port": WEB_PORT,
        "share": WEB_SHARE,
        "show_error": True,
    }

    if "css" in inspect.signature(app.launch).parameters and custom_css:
        launch_kwargs["css"] = custom_css

    logger.info(t("app.gradio_start", port=WEB_PORT))
    app.queue(default_concurrency_limit=10).launch(**launch_kwargs)


if __name__ == "__main__":
    main()
