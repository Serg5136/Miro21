import json

import tkinter as tk

from src import main


def test_save_reuses_last_path(monkeypatch, tmp_path, tk_root):
    save_calls: list[str] = []
    dialog_calls = {"asksave": 0}
    save_path = tmp_path / "board.json"

    def fake_ask_filename():
        dialog_calls["asksave"] += 1
        return str(save_path)

    def fake_save_to_path(data, filename):
        save_calls.append(filename)
        # Проверяем, что сохраняются сериализуемые данные борда
        json.dumps(data)
        return True

    class DummyAutoSave(main.AutoSaveService):
        def __init__(self):
            super().__init__(filename=tmp_path / "autosave.json")

    class DummyStore(main.LastSavePathStore):
        def __init__(self):
            super().__init__(filename=tmp_path / "state.json")

    # Используем заранее созданный tk_root, чтобы не поднимать новое окно
    monkeypatch.setattr(main.tk, "Tk", lambda: tk_root)
    monkeypatch.setattr(main, "AutoSaveService", DummyAutoSave)
    monkeypatch.setattr(main, "LastSavePathStore", DummyStore)
    monkeypatch.setattr(main.file_io, "ask_board_save_filename", fake_ask_filename)
    monkeypatch.setattr(main.file_io, "save_board_to_path", fake_save_to_path)

    app = main.BoardApp()

    app.save_board()
    app.save_board()

    assert dialog_calls["asksave"] == 1
    assert save_calls == [str(save_path), str(save_path)]
    assert app.last_save_path == str(save_path)
    # Убедимся, что путь сохранился на диск и читается заново
    fresh_store = DummyStore()
    assert fresh_store.last_save_path == str(save_path)

    # Очистим ссылки на root, чтобы фикстура могла завершиться корректно
    app.root = tk_root
