import gradio as gr
from locales.i18n import t
from services.genre_manager import GenreManager
from services.style_manager import StyleManager
from utils.file_parser import parse_novel_file
from core.state import app_state
import logging

logger = logging.getLogger(__name__)

def build_rewrite_tab():
    with gr.Tab(t("tabs.rewrite")):
        gr.Markdown(f"### {t('rewrite.header')}")

        rewrite_file_input = gr.File(label=t("rewrite.upload_file"), file_types=[".txt", ".docx", ".md", ".pdf"])
        
        genre_choices = GenreManager.get_genre_names()
        with gr.Row():
            rewrite_genre = gr.Dropdown(
                choices=genre_choices,
                label=t("create.genre_label"),
                value=genre_choices[0] if genre_choices else None,
                interactive=True,
                scale=1
            )
            
            style_choices = StyleManager.get_style_names()
            rewrite_style = gr.Dropdown(
                choices=style_choices,
                label=t("rewrite.preset_style"),
                value=style_choices[0] if style_choices else None,
                interactive=True,
                scale=1
            )
            
            use_reflection_checkbox = gr.Checkbox(label="Bật chế độ Tự kiểm duyệt", value=False, info="AI báo lỗi và viết lại cho hoàn chỉnh hơn.", scale=1)
                    
        rewrite_input = gr.Textbox(
            label=t("polish.original_text"),
            lines=10, placeholder="Dán nội dung cần viết lại..."
        )

        rewrite_btn = gr.Button(t("rewrite.start_rewrite"), variant="primary")
        rewrite_status = gr.Textbox(label=t("rewrite.parse_status"), interactive=False)
        rewrite_output = gr.Textbox(label=t("rewrite.full_rewritten"), lines=15, interactive=True)

        def on_file_upload(file):
            if file is None:
                return ""
            try:
                content = parse_novel_file(file.name)
                return content
            except Exception as e:
                return f"❌ {str(e)}"

        def on_rewrite(text, genre, style, use_reflection):
            yield "⏳ Đang gọi AI xử lý... Vui lòng chờ.", gr.update(), gr.update(interactive=False)
            instructions = f"Thể loại: {genre}\nPhong cách thiết lập: {style}"
            gen = app_state.get_generator()
            content, msg = gen.rewrite_paragraph(text, instructions, use_reflection=use_reflection)
            if content:
                yield f"✅ {msg}", content, gr.update(interactive=True)
            else:
                yield f"❌ {msg}", gr.update(), gr.update(interactive=True)

        rewrite_file_input.change(fn=on_file_upload, inputs=[rewrite_file_input], outputs=[rewrite_input])
        rewrite_btn.click(fn=on_rewrite, inputs=[rewrite_input, rewrite_genre, rewrite_style, use_reflection_checkbox], outputs=[rewrite_status, rewrite_output, rewrite_btn])
