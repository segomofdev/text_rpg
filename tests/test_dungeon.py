from core.dungeon import Dungeon
from core.models import Room


def test_dungeon_build():
    """build должен создавать карту, комнаты и живого игрока нужной длины."""
    dungeon = Dungeon(num_rooms=5, enemy_count=2)
    game_map, rooms, player = dungeon.build()

    assert len(game_map) == 5
    assert len(rooms) == 5
    assert game_map[0] == "St"
    assert game_map[-1] == "Ex"
    assert isinstance(rooms[0], Room)
    assert player.is_alive


def test_enemies_match_map():
    """Если в карте стоит 'E', в комнате должен быть враг, и наоборот."""
    dungeon = Dungeon(num_rooms=7, enemy_count=3)
    game_map, rooms, _ = dungeon.build()

    for symbol, room in zip(game_map, rooms):
        if symbol == "E":
            assert room.enemy is not None
        else:
            if room.enemy is not None:
                assert symbol == "E"


def test_start_room_has_no_enemy():
    """Стартовая комната всегда пустая."""
    dungeon = Dungeon(7, 3)
    game_map, rooms, _ = dungeon.build()

    assert game_map[0] == "St"
    assert rooms[0].enemy is None


def test_no_enemies_when_enemy_count_zero():
    """При enemy_count=0 нет врагов нигде."""
    dungeon = Dungeon(5, 0)
    game_map, rooms, _ = dungeon.build()

    assert "E" not in game_map
    assert all(room.enemy is None for room in rooms)
