from core import database as db_module
from services.project_manager import ProjectManager


def test_project_manager_isolates_projects_by_user(tmp_path):
    # Chuẩn bị DB tạm cho test
    db_path = tmp_path / "tinix_story_test.db"
    db_module.DB_DIR = str(tmp_path)
    db_module.DB_FILE = str(db_path)
    if db_module._connection is not None:
        db_module._connection.close()
    db_module._connection = None

    # Hai user tạo cùng 1 tiêu đề
    p1, _ = ProjectManager.create_project(
        "Truyện chung tên", "Fantasy", [], "char", "world", "plot", user_id="alice"
    )
    p2, _ = ProjectManager.create_project(
        "Truyện chung tên", "Fantasy", [], "char", "world", "plot", user_id="bob"
    )

    assert p1 is not None and p2 is not None
    assert p1.id != p2.id

    ok1, _ = ProjectManager.save_project(p1, user_id="alice")
    ok2, _ = ProjectManager.save_project(p2, user_id="bob")
    assert ok1 and ok2

    alice_projects = ProjectManager.list_projects(user_id="alice")
    bob_projects = ProjectManager.list_projects(user_id="bob")

    assert len(alice_projects) == 1
    assert len(bob_projects) == 1
    assert alice_projects[0]["id"] != bob_projects[0]["id"]

    loaded_alice, _ = ProjectManager.load_project(alice_projects[0]["id"], user_id="alice")
    loaded_bob, _ = ProjectManager.load_project(bob_projects[0]["id"], user_id="bob")
    assert loaded_alice is not None
    assert loaded_bob is not None

    # Không cho đọc chéo user
    cross, _ = ProjectManager.load_project(alice_projects[0]["id"], user_id="bob")
    assert cross is None
