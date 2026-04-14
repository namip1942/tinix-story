import gradio as gr
from locales.i18n import t
from services.project_manager import ProjectManager, list_project_titles
from core.session import get_user_id_from_request
import logging

logger = logging.getLogger(__name__)

def build_projects_tab():
    with gr.Tab(t("tabs.projects")):
        gr.Markdown(f"### {t('projects.header')}")

        projects_table = gr.Dataframe(
            headers=["ID", t("ui.col_project_name"), t("ui.col_type"), t("ui.col_created_at"), t("ui.col_chapters")],
            interactive=False
        )
        refresh_projects_btn = gr.Button(t("projects.refresh_btn"))

        gr.Markdown(f"#### {t('projects.delete_header')}")
        delete_project_selector = gr.Dropdown(
            choices=list_project_titles(),
            label=t("projects.delete_select_project"),
            interactive=True
        )
        delete_project_btn = gr.Button(t("projects.delete_btn"), variant="stop")
        project_manage_status = gr.Textbox(label=t("projects.status_label"), interactive=False)

        def on_refresh_projects(request: gr.Request):
            user_id = get_user_id_from_request(request)
            try:
                projects = ProjectManager.list_projects(user_id=user_id)
                table_data = []
                for p in projects:
                    table_data.append([
                        p.get("id", ""),
                        p.get("title", ""),
                        p.get("genre", ""),
                        p.get("created_at", "")[:10] if p.get("created_at") else "",
                        f"{p.get('completed_chapters', 0)}/{p.get('chapter_count', 0)}"
                    ])
                titles = [p.get("title", "") for p in projects]
                return table_data, gr.update(choices=titles, value=None)
            except Exception as e:
                logger.error(f"Refresh projects failed: {e}")
                return [], gr.update()

        def on_delete_project(project_title, request: gr.Request):
            user_id = get_user_id_from_request(request)
            if not project_title or not project_title.strip():
                return f"❌ {t('projects.select_project_first')}", gr.update(), gr.update()

            try:
                project_data = ProjectManager.get_project_by_title(project_title, user_id=user_id)
                if not project_data:
                    return f"❌ {t('projects.project_not_found')}", gr.update(), gr.update()

                project_id = project_data.get("id")
                success, msg = ProjectManager.delete_project(project_id, user_id=user_id)
                if success:
                    new_table, new_dropdown = on_refresh_projects(request)
                    return f"✅ {t('projects.delete_success')}", new_table, new_dropdown
                return f"❌ {t('projects.delete_failed')}: {msg}", gr.update(), gr.update()
            except Exception as e:
                return f"❌ {str(e)}", gr.update(), gr.update()

        refresh_projects_btn.click(fn=on_refresh_projects, outputs=[projects_table, delete_project_selector])
        delete_project_btn.click(
            fn=on_delete_project,
            inputs=[delete_project_selector],
            outputs=[project_manage_status, projects_table, delete_project_selector]
        )
