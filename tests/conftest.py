import pytest

from core.controller import GameController
from core.models import Weapon, Armor, Player, Enemy, Room


class DummyRandom:
    """random для тестов"""

    def __init__(self, values):
        self.values = iter(values)

    def randint(self, a: int, b: int) -> int:
        # игнорируем границы, просто возвращаем следующее значение
        return next(self.values)


@pytest.fixture()
def dummy_random():
    """Фикстура, возвращающая класс DummyRandom (не экземпляр)."""
    return DummyRandom


@pytest.fixture
def make_player_enemy():
    """Вспомогательная фабрика: игрок всегда попадает, враг никогда."""
    w_p = Weapon("Тестовая дубина", damage=5, hit_chance=100)
    a_p = Armor("Тестовая броня", defense=0)
    player = Player("p1", "Герой", 10, "desc", w_p, a_p, ["rip"])

    w_e = Weapon("Тестовое оружие", damage=3, hit_chance=0)
    a_e = Armor("Тестовый щит", defense=0)
    enemy = Enemy("Гоблин", 6, "desc", "dead", w_e, a_e)
    return player, enemy


@pytest.fixture
def mock_player():
    """Фикстура для игрока."""
    return Player("p1", "Тест", 10, "desc", None, None, [])


@pytest.fixture
def mock_dungeon():
    """Фикстура с простым подземельем для тестов контроллера"""
    game_map = ['St', " ", "E", "Ex"]

    rooms = [
        Room(0, "Старт", None, is_start=True, is_exit=False),  # пустая стартовая
        Room(1, "Пустая", None, False, False),  # пустая середина
        Room(2, "С врагом", Player(
            "e1",
            "Враг",
            10,
            "",
            None,
            None,
            []), False, False),  # с врагом
        Room(3, "Выход", None, False, is_exit=True),  # выход
    ]

    return GameController(game_map, rooms, mock_player)
