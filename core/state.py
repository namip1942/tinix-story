import threading
from typing import Optional
from services.novel_generator import NovelGenerator, get_generator, NovelProject

class AppState:
    """Trạng thái ứng dụng dùng chung giữa các tab"""
    def __init__(self):
        self.lock = threading.Lock()
        self.generator: Optional[NovelGenerator] = None
        self._session_state = {}

    def _ensure_session(self, user_id: str) -> dict:
        sid = user_id or "default"
        if sid not in self._session_state:
            self._session_state[sid] = {
                "is_generating": False,
                "stop_requested": False,
                "current_project": None,
            }
        return self._session_state[sid]

    def get_generator(self) -> NovelGenerator:
        """Lấy hoặc tạo generator"""
        if self.generator is None:
            self.generator = get_generator()
        return self.generator

    def get_current_project(self, user_id: str = "default") -> Optional[NovelProject]:
        return self._ensure_session(user_id).get("current_project")

    def set_current_project(self, project: Optional[NovelProject], user_id: str = "default") -> None:
        self._ensure_session(user_id)["current_project"] = project

    def get_is_generating(self, user_id: str = "default") -> bool:
        return bool(self._ensure_session(user_id).get("is_generating"))

    def set_is_generating(self, value: bool, user_id: str = "default") -> None:
        self._ensure_session(user_id)["is_generating"] = bool(value)

    def get_stop_requested(self, user_id: str = "default") -> bool:
        return bool(self._ensure_session(user_id).get("stop_requested"))

    def set_stop_requested(self, value: bool, user_id: str = "default") -> None:
        self._ensure_session(user_id)["stop_requested"] = bool(value)

# Global app state singleton
app_state = AppState()
