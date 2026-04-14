import sqlite3

from core.database import init_db


def test_init_db_creates_core_tables_and_projects_sub_genres_column():
    conn = sqlite3.connect(":memory:")
    try:
        init_db(conn)

        tables = {
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }

        expected_tables = {
            "config",
            "backends",
            "config_backups",
            "response_cache",
            "generation_cache",
            "chapter_summaries",
            "projects",
            "chapters",
        }
        assert expected_tables.issubset(tables)

        project_columns = {
            row[1]
            for row in conn.execute("PRAGMA table_info(projects)").fetchall()
        }
        assert "sub_genres" in project_columns
    finally:
        conn.close()
