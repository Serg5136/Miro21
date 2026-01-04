import copy

from src.board_model import BoardData, Card, WorkspaceBoard, WorkspaceData, SCHEMA_VERSION


def test_workspace_roundtrip_preserves_names_and_active_index():
    board_one = BoardData(cards={1: Card(id=1, x=0, y=0, width=10, height=10)}, connections=[], frames={})
    board_two = BoardData(cards={}, connections=[], frames={})

    workspace = WorkspaceData(
        boards=[
            WorkspaceBoard(name="Первая", data=board_one, saved_history_index=0),
            WorkspaceBoard(name="Вторая", data=board_two, saved_history_index=3),
        ],
        active_board_index=1,
    )

    payload = workspace.to_primitive()
    assert payload["schema_version"] == SCHEMA_VERSION
    restored = WorkspaceData.from_primitive(copy.deepcopy(payload))

    assert len(restored.boards) == 2
    assert restored.active_board_index == 1
    assert restored.boards[0].name == "Первая"
    assert restored.boards[1].name == "Вторая"
    assert 1 in restored.boards[0].data.cards
    assert restored.boards[1].saved_history_index == 3


def test_workspace_accepts_legacy_single_board_format():
    single_board = BoardData(cards={}, connections=[], frames={}).to_primitive()

    restored = WorkspaceData.from_primitive(single_board)

    assert restored.active_board_index == 0
    assert len(restored.boards) == 1
    assert restored.boards[0].name == "Доска 1"
    assert restored.boards[0].data.cards == {}
