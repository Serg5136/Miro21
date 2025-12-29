import tkinter as tk
from typing import Optional

from .sidebar import SidebarFactory
from .tooltips import add_canvas_tooltip, add_tooltip
from .events import EventBinder


class ToolbarFactory:
    def create(self, app) -> tk.Frame:
        toolbar = tk.Frame(app.root, bg="#e0e0e0", height=32)
        toolbar.grid(row=0, column=0, columnspan=3, sticky="new")

        btn_undo_toolbar = tk.Button(
            toolbar,
            text="⟲ Отменить",
            command=app.on_undo,
        )
        btn_undo_toolbar.pack(side="left", padx=(8, 2), pady=4)
        app.btn_undo_toolbar = btn_undo_toolbar
        add_tooltip(btn_undo_toolbar, "Отменить последнее действие")

        btn_redo_toolbar = tk.Button(
            toolbar,
            text="⟳ Повторить",
            command=app.on_redo,
        )
        btn_redo_toolbar.pack(side="left", padx=2, pady=4)
        app.btn_redo_toolbar = btn_redo_toolbar
        add_tooltip(btn_redo_toolbar, "Повторить отменённое действие")

        btn_attach_image = tk.Button(
            toolbar,
            text="📎 Прикрепить к карточке",
            command=app.attach_image_from_file,
        )
        btn_attach_image.pack(side="left", padx=(10, 2), pady=4)
        add_tooltip(
            btn_attach_image,
            "Прикрепить файл-изображение к выделенной карточке без создания новой",
        )

        btn_text_color = tk.Button(
            toolbar,
            text="🎨 Цвет текста",
            command=app.change_text_color,
        )
        btn_text_color.pack(side="left", padx=2, pady=4)
        add_tooltip(btn_text_color, "Изменить цвет текста карточек для текущей темы")

        size_frame = tk.Frame(toolbar, bg="#e0e0e0")
        size_frame.pack(side="left", padx=(12, 2), pady=4)

        tk.Label(size_frame, text="Ширина:", bg="#e0e0e0").grid(row=0, column=0, padx=(0, 4))
        spn_width = tk.Spinbox(
            size_frame,
            from_=60,
            to=1200,
            width=6,
            textvariable=app.var_card_width,
        )
        spn_width.grid(row=0, column=1, padx=(0, 8))
        add_tooltip(spn_width, "Задайте ширину карточки в пикселях")

        tk.Label(size_frame, text="Высота:", bg="#e0e0e0").grid(row=0, column=2, padx=(0, 4))
        spn_height = tk.Spinbox(
            size_frame,
            from_=40,
            to=1200,
            width=6,
            textvariable=app.var_card_height,
        )
        spn_height.grid(row=0, column=3, padx=(0, 8))
        add_tooltip(spn_height, "Задайте высоту карточки в пикселях")

        btn_apply_size = tk.Button(
            size_frame,
            text="Применить",
            command=app.apply_card_size_from_controls,
        )
        btn_apply_size.grid(row=0, column=4)
        add_tooltip(btn_apply_size, "Применить указанные ширину и высоту к выбранным карточкам")
        return toolbar


class BoardTabsFactory:
    def create(self, app) -> tk.Frame:
        container = tk.Frame(app.root, width=180, bg="#f6f6f6")
        container.grid(row=1, column=0, sticky="ns")
        container.grid_propagate(False)

        header = tk.Label(container, text="Доски", bg="#f6f6f6", font=("Arial", 12, "bold"))
        header.pack(fill="x", padx=10, pady=(12, 6))

        add_button = tk.Button(container, text="+ Новая доска", command=app.create_new_board)
        add_button.pack(fill="x", padx=10, pady=(0, 10))
        add_tooltip(add_button, "Создать пустую доску и переключиться на неё")
        app.board_add_button = add_button

        tabs_frame = tk.Frame(container, bg="#f6f6f6")
        tabs_frame.pack(fill="both", expand=True, padx=6, pady=(0, 10))

        app.board_tabs_container = tabs_frame
        return container


class CanvasFactory:
    def create_canvas(self, app) -> tk.Canvas:
        canvas = tk.Canvas(app.root, bg=app.theme["bg"])
        canvas.grid(row=1, column=1, sticky="nsew")
        canvas.config(scrollregion=(0, 0, 4000, 4000))
        return canvas


class MinimapFactory:
    def __init__(self, collapsed_size: int = 36):
        self.collapsed_size = collapsed_size

    def create(self, app) -> tk.Frame:
        container = tk.Frame(
            app.canvas, bg="#f8f8f8", highlightthickness=1, highlightbackground="#cccccc"
        )
        container.place(relx=1.0, rely=0.0, x=-10, y=10, anchor="ne")

        expanded_frame = tk.Frame(container, bg="#f8f8f8")
        expanded_frame.pack(fill="both", expand=True)

        header = tk.Frame(expanded_frame, bg="#f8f8f8")
        header.pack(fill="x", padx=8, pady=(8, 4))

        minimap_label = tk.Label(
            header, text="Мини карта", bg="#f8f8f8", font=("Arial", 12, "bold")
        )
        minimap_label.pack(side="left", fill="x", expand=True)

        toggle_button = tk.Button(
            header,
            text="−",
            width=2,
            command=lambda: set_collapsed(True),
        )
        toggle_button.pack(side="right", padx=(6, 0))

        app.minimap = tk.Canvas(
            expanded_frame,
            width=240,
            height=160,
            bg=app.theme["minimap_bg"],
            highlightthickness=1,
            highlightbackground="#cccccc",
        )
        app.minimap.pack(padx=8, pady=(0, 10))
        app.minimap.bind("<Button-1>", app.on_minimap_click)
        add_tooltip(app.minimap, "Нажмите, чтобы переместить вид по доске")
        add_canvas_tooltip(app.minimap, "minimap_card", "Карточка на доске")
        add_canvas_tooltip(app.minimap, "minimap_frame", "Рамка на доске")
        add_canvas_tooltip(app.minimap, "minimap_viewport", "Текущая область просмотра")

        collapsed_frame = tk.Frame(
            container,
            bg="#f8f8f8",
            width=self.collapsed_size,
            height=self.collapsed_size,
            highlightthickness=0,
        )
        collapsed_frame.pack_propagate(False)
        collapsed_button = tk.Button(
            collapsed_frame,
            text="+",
            font=("Arial", 10, "bold"),
            relief="flat",
            bd=0,
            bg="#f8f8f8",
            fg="#333333",
            activebackground="#e8e8e8",
            activeforeground="#000000",
            highlightthickness=1,
            highlightbackground="#cccccc",
            highlightcolor="#666666",
            command=lambda: set_collapsed(False),
        )
        collapsed_button.pack(expand=True, fill="both")
        collapsed_frame.pack_forget()

        app.minimap_collapsed = False
        app.minimap_toggle_button = toggle_button
        app.minimap_collapsed_button = collapsed_button
        app.minimap_container = container
        app.minimap_collapsed_frame = collapsed_frame
        app.minimap_expanded_frame = expanded_frame

        def set_collapsed(collapsed: bool):
            app.minimap_collapsed = collapsed
            if collapsed:
                container.update_idletasks()
                app._minimap_previous_size = (
                    max(container.winfo_width(), 1),
                    max(container.winfo_height(), 1),
                )
                expanded_frame.pack_forget()
                collapsed_frame.config(width=self.collapsed_size, height=self.collapsed_size)
                collapsed_frame.pack(fill="both", expand=True)
                container.config(width=self.collapsed_size, height=self.collapsed_size)
                toggle_button.config(text="+")
            else:
                collapsed_frame.pack_forget()
                expanded_frame.pack(fill="both", expand=True)
                prev_w, prev_h = getattr(app, "_minimap_previous_size", (None, None))
                container.config(width=prev_w or "", height=prev_h or "")
                toggle_button.config(text="−")
                if hasattr(app, "update_minimap"):
                    app.update_minimap()
            container.update_idletasks()

        app.toggle_minimap_collapsed = lambda: set_collapsed(not app.minimap_collapsed)

        add_tooltip(
            minimap_label,
            text=(
                "Подсказки:\n"
                "— Двойной клик по пустому месту: новая карточка\n"
                "— Двойной клик по карточке: редактировать текст\n"
                "— Двойной клик по связи: текст связи\n"
                "— ЛКМ по карточке: выбрать, перетаскивать\n"
                "— ЛКМ по пустому месту + движение: прямоугольное выделение\n"
                "— ЛКМ по связи: выбрать (Delete — удалить, Ctrl+Shift+D — направление)\n"
                "— Колёсико мыши: зум\n"
                "— Средняя кнопка: панорамирование\n"
                "— Правая кнопка: контекстное меню\n"
                "— Ctrl+Z / Ctrl+Y: отмена / повтор\n"
                "— Ctrl+C / Ctrl+V: копирование / вставка\n"
                "— Ctrl+D: дубликат\n"
                "— Delete: удалить выбранные карточки\n"
                "— Рамка: перетаскивание двигает и карточки внутри\n"
                "— Из карточки: кружок справа — перетягиваем на другую\n"
                "   карточку, чтобы соединить\n"
                "— Квадрат внизу справа — изменение размера карточки"
            ),
        )

        return container


class LayoutBuilder:
    def __init__(
        self,
        toolbar_factory: Optional[ToolbarFactory] = None,
        board_tabs_factory: Optional[BoardTabsFactory] = None,
        sidebar_factory: Optional[SidebarFactory] = None,
        canvas_factory: Optional[CanvasFactory] = None,
        minimap_factory: Optional[MinimapFactory] = None,
        events_binder: Optional[EventBinder] = None,
    ):
        self.toolbar_factory = toolbar_factory or ToolbarFactory()
        self.board_tabs_factory = board_tabs_factory or BoardTabsFactory()
        self.sidebar_factory = sidebar_factory or SidebarFactory()
        self.canvas_factory = canvas_factory or CanvasFactory()
        self.minimap_factory = minimap_factory or MinimapFactory()
        self.events_binder = events_binder or EventBinder()

    def configure_root_grid(self, root: tk.Tk) -> None:
        root.rowconfigure(0, weight=0)
        root.rowconfigure(1, weight=1)
        root.columnconfigure(0, weight=0)
        root.columnconfigure(1, weight=1)
        root.columnconfigure(2, weight=0)

    def build(self, app) -> None:
        self.configure_root_grid(app.root)
        self.toolbar_factory.create(app)
        self.board_tabs_factory.create(app)
        app.canvas = self.canvas_factory.create_canvas(app)
        self.minimap_factory.create(app)
        self.sidebar_factory.create(app)
        self.events_binder.bind(app)
