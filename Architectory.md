mini-miro-board/
├─ app.py                    # Точка входа для запуска приложения
├─ src/                      # Основной код приложения (пакет src)
│  ├─ __init__.py            # Определяет пакет
│  ├─ autosave.py            # Сервис автосохранения
│  ├─ board_model.py         # Модель данных (Card, Frame, Connection, BoardData)
│  ├─ canvas_view.py         # Отрисовка карточек, рамок и связей на Canvas
│  ├─ config.py              # Темы и загрузка/сохранение настроек
│  ├─ connect_controller.py  # Управление режимом соединения карточек
│  ├─ drag_controller.py     # Логика перетаскивания карточек и рамок
│  ├─ events.py              # Константы биндингов и EventBinder
│  ├─ files.py               # Сохранение/загрузка доски и экспорт
│  ├─ history.py             # История действий и команды
│  ├─ layout.py              # Построение тулбара и Canvas
│  ├─ selection_controller.py# Работа с выделением карточек
│  ├─ sidebar.py             # Сайдбар и вспомогательные контролы
│  └─ tooltips.py            # Подсказки для элементов интерфейса
│
├─ tests/                    # Автотесты
│  ├─ conftest.py
│  ├─ test_attachment_handlers.py
│  ├─ test_board_model.py
│  ├─ test_dummy.py
│  ├─ test_grid_settings.py
│  └─ test_history.py
│
├─ attachments/              # Пример ресурсов вложений
│  ├─ 1-1.jpg
│  └─ 4-1.png
│
├─ _mini_miro_autosave.json  # Пример сохранения борда
├─ _mini_miro_config.json    # Настройки темы/сетки
├─ README.md
├─ requirements.txt          # Зависимости (Pillow + опциональные)
├─ LICENSE                   # Лицензия
└─ ё1.json                   # Пример сохранённой доски



Архитектура
Модули

src/main.py

Класс BoardApp — основное окно и логика:

создание/редактирование карточек;

рамки;

связи;

обработка событий мыши/клавиатуры;

мини-карта;

сохранение/загрузка/экспорт;

применение темы и сетки.

src/board_model.py

Card, Frame, Connection — dataclasses для сущностей;

BoardData — агрегирует все сущности борда;

методы to_primitive() / from_primitive() для сериализации в/из JSON-совместимого dict.

src/history.py

SnapshotCommand(before, after) — команда, умеющая undo() / redo() через set_board_from_data;

History — менеджер истории:

хранит initial_state (борд до изменений);

хранит список команд;

реализует push(), undo(), redo(), current_state().