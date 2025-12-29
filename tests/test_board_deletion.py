from src import main
from src.main import BoardApp


def _build_app(tk_root, monkeypatch):
    monkeypatch.setattr(main.tk, "Tk", lambda: tk_root)
    monkeypatch.setattr(main.AutoSaveService, "save", lambda self, data=None: None)
    return BoardApp()


def test_delete_button_disabled_for_single_board(tk_root, monkeypatch):
    app = _build_app(tk_root, monkeypatch)

    assert app.board_delete_button.cget("state") == "disabled"


def test_delete_current_board(tk_root, monkeypatch):
    monkeypatch.setattr(main.messagebox, "askyesno", lambda *args, **kwargs: True)

    app = _build_app(tk_root, monkeypatch)
    app.create_new_board()

    assert app.board_delete_button.cget("state") == "normal"

    first_board_name = app.boards[0].name
    app.delete_current_board()

    assert len(app.boards) == 1
    assert app.active_board_index == 0
    assert app.boards[0].name == first_board_name
    assert app.board_delete_button.cget("state") == "disabled"
