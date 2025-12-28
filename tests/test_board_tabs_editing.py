import tkinter as tk

from src import main
from src.main import BoardApp


def _build_app(tk_root, monkeypatch):
    monkeypatch.setattr(main.tk, "Tk", lambda: tk_root)
    monkeypatch.setattr(main.AutoSaveService, "save", lambda self, data=None: None)
    app = BoardApp()
    return app


def test_board_tab_edit_state_resets_on_cancel(tk_root, monkeypatch):
    app = _build_app(tk_root, monkeypatch)

    original_name = app.boards[0].name
    app.start_edit_board_tab(0)

    assert app.editing_tab_index == 0
    assert isinstance(app.editing_tab_value, tk.StringVar)

    app.finish_edit_board_tab(save=False)

    assert app.editing_tab_index is None
    assert app.boards[0].name == original_name


def test_board_tab_rename_via_double_click_and_enter(tk_root, monkeypatch):
    app = _build_app(tk_root, monkeypatch)

    button = app.board_tab_buttons[0]
    button.event_generate("<Double-Button-1>")
    tk_root.update_idletasks()

    assert app.editing_tab_entry is not None
    app.editing_tab_entry.delete(0, tk.END)
    app.editing_tab_entry.insert(0, "Командная доска")
    app.editing_tab_entry.event_generate("<Return>")
    tk_root.update_idletasks()

    assert app.boards[0].name == "Командная доска"
    assert app.editing_tab_index is None
    assert any(btn.cget("text").startswith("Командная доска") for btn in app.board_tab_buttons)
