from typing import Any


def get_user_id_from_request(request: Any) -> str:
    """Resolve per-user id from Gradio request/session context."""
    if request is None:
        return "default"
    return getattr(request, "session_hash", None) or "default"
