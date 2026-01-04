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


def test_new_board_name_is_unique(tk_root, monkeypatch):
    app = _build_app(tk_root, monkeypatch)

    # Занимаем имя "Доска 2" заранее
    app.boards[0].name = "Доска 2"

    app.create_new_board()

    assert app.boards[-1].name == "Доска 3"


def test_board_rename_rejects_duplicates(tk_root, monkeypatch):
    errors: list[tuple] = []
    monkeypatch.setattr(main.messagebox, "showerror", lambda *args, **kwargs: errors.append(args))

    app = _build_app(tk_root, monkeypatch)
    app.create_new_board()

    original_name = app.boards[0].name

    app.start_edit_board_tab(0)
    app.editing_tab_value.set(app.boards[1].name)  # Пытаемся использовать уже существующее имя
    app.finish_edit_board_tab(save=True)

    assert app.boards[0].name == original_name
    assert errors, "Ожидали сообщение об ошибке"


def test_board_rename_rejects_invalid_characters(tk_root, monkeypatch):
    errors: list[tuple] = []
    monkeypatch.setattr(main.messagebox, "showerror", lambda *args, **kwargs: errors.append(args))

    app = _build_app(tk_root, monkeypatch)
    original_name = app.boards[0].name

    app.start_edit_board_tab(0)
    app.editing_tab_value.set("Неверное/имя?")
    app.finish_edit_board_tab(save=True)

    assert app.boards[0].name == original_name
    assert any("Допустимы" in err[1] for err in errors)


def test_board_tab_context_menu_triggers_rename(tk_root, monkeypatch):
    app = _build_app(tk_root, monkeypatch)

    app.board_context_tab_index = 0
    app._context_rename_board_tab()
    tk_root.update_idletasks()

    assert app.editing_tab_index == 0
    assert app.editing_tab_entry is not None


def test_editing_entry_is_removed_after_finish(tk_root, monkeypatch):
    app = _build_app(tk_root, monkeypatch)

    app.start_edit_board_tab(0)
    entry = app.editing_tab_entry

    assert entry is not None and entry.winfo_exists()

    app.finish_edit_board_tab(save=False)
    tk_root.update_idletasks()

    assert app.editing_tab_entry is None
    assert not entry.winfo_exists()
    assert not any(isinstance(child, tk.Entry) for child in app.board_tabs_container.winfo_children())
