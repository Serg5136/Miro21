import tkinter as tk

from src.layout import MinimapFactory


class _DummyApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()
        self.theme = {
            "minimap_bg": "#ffffff",
            "minimap_card_outline": "#888888",
            "minimap_frame_outline": "#aaaaaa",
            "minimap_viewport": "#ff0000",
        }
        self.on_minimap_click = lambda event: None
        self.update_minimap_calls = 0

    def update_minimap(self):
        self.update_minimap_calls += 1


def _create_minimap_app(root: tk.Tk) -> _DummyApp:
    app = _DummyApp(root)
    factory = MinimapFactory(collapsed_size=64)
    factory.create(app)
    root.update_idletasks()
    return app


def test_minimap_toggle_collapses_and_expands(tk_root):
    app = _create_minimap_app(tk_root)

    expanded_size = (app.minimap_container.winfo_width(), app.minimap_container.winfo_height())

    assert not app.minimap_collapsed
    assert app.minimap_toggle_button["text"] == "−"

    app.toggle_minimap_collapsed()
    tk_root.update_idletasks()

    assert app.minimap_collapsed
    assert app.minimap_collapsed_button["text"] == "+"
    assert app.minimap_container.winfo_width() == 64
    assert app.minimap_container.winfo_height() == 64

    app.toggle_minimap_collapsed()
    tk_root.update_idletasks()

    assert not app.minimap_collapsed
    assert app.minimap_toggle_button["text"] == "−"
    assert (app.minimap_container.winfo_width(), app.minimap_container.winfo_height()) == expanded_size
    assert app.update_minimap_calls == 1


def test_minimap_content_persists_across_toggle(tk_root):
    app = _create_minimap_app(tk_root)
    item = app.minimap.create_text(10, 10, text="X")

    app.toggle_minimap_collapsed()
    app.toggle_minimap_collapsed()
    tk_root.update_idletasks()

    assert item in app.minimap.find_all()


def test_minimap_icons_reflect_state(tk_root):
    app = _create_minimap_app(tk_root)

    assert app.minimap_toggle_button["text"] == "−"

    app.toggle_minimap_collapsed()
    tk_root.update_idletasks()

    assert app.minimap_collapsed_button["text"] == "+"
    app.toggle_minimap_collapsed()
    tk_root.update_idletasks()

    assert app.minimap_toggle_button["text"] == "−"
