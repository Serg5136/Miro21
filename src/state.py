"""Persistent application state helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


STATE_FILENAME = "_mini_miro_state.json"


class LastSavePathStore:
    """Keeps track of the last path used to save a board.

    The information is stored in a small JSON file so it can be reused across
    application sessions.
    """

    def __init__(self, filename: str | Path = STATE_FILENAME) -> None:
        self.filename = Path(filename)
        self.last_save_path: str | None = None
        self._load()

    def _load(self) -> None:
        try:
            if not self.filename.exists():
                return
            with self.filename.open("r", encoding="utf-8") as f:
                data: dict[str, Any] = json.load(f)
            value = data.get("last_save_path")
            if isinstance(value, str) and value:
                self.last_save_path = value
        except Exception:
            self.last_save_path = None

    def set_last_save_path(self, path: str | Path | None) -> None:
        self.last_save_path = str(path) if path else None
        self._persist()

    def _persist(self) -> None:
        try:
            payload: dict[str, str] = {}
            if self.last_save_path:
                payload["last_save_path"] = self.last_save_path
            with self.filename.open("w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
