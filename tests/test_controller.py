from core.models import Room
from core.controller import GameController


def test_start_empty_room_actions(mock_dungeon, monkeypatch):
    """В стартовой пустой комнате только 'Пойти дальше'."""
    mock_dungeon.current_room_index = 0

    def mock_input(prompt):
        return "1"

    monkeypatch.setattr(mock_dungeon, '_input', mock_input)
    action = mock_dungeon._get_valid_action()

    assert action == 1


def test_middle_empty_room_actions(mock_dungeon, monkeypatch):
    """В пустой средней комнате 'Дальше' + 'Назад'."""
    mock_dungeon.current_room_index = 1

    def mock_input(prompt):
        if mock_input.calls == 0:
            mock_input.calls += 1
            return "5"  # неверный
        return "2"  # назад

    mock_input.calls = 0
    monkeypatch.setattr(mock_dungeon, '_input', mock_input)
    action = mock_dungeon._get_valid_action()

    assert action == 2


def test_enemy_room_actions(mock_dungeon, monkeypatch):
    """В комнате с врагом доступно 'Атаковать'."""
    mock_dungeon.current_room_index = 2

    def mock_input(prompt):
        return "3"

    monkeypatch.setattr(mock_dungeon, '_input', mock_input)
    action = mock_dungeon._get_valid_action()

    assert action == 3


def test_controller_move_forward(mock_dungeon):
    """При '1' индекс увеличивается на 1."""
    mock_dungeon.current_room_index = 0
    mock_dungeon._execute_action(1)
    assert mock_dungeon.current_room_index == 1


def test_controller_move_back(mock_dungeon):
    """При '2' индекс уменьшается на 1."""
    mock_dungeon.current_room_index = 2
    mock_dungeon._execute_action(2)
    assert mock_dungeon.current_room_index == 1


def test_controller_does_not_go_beyond_bounds(mock_player):
    """Переход дальше из последней комнаты не ломает индекс."""
    game_map = ["St", "Ex"]
    rooms = [Room(0, "", None), Room(1, "", None)]
    controller = GameController(game_map, rooms, mock_player)
    controller.current_room_index = 1  # последняя

    controller._execute_action(1)  # попробовать идти дальше

    assert controller.current_room_index == 1  # не изменился
