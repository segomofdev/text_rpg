import random
from typing import List


from game.characters.base import Weapon, Armor, Room
from game.characters.enemy import Enemy
from game.characters.player import Player
from utils.json_loader import load_json_file


def create_dungeon(num_rooms: int = 5, enemy_chance: float = 0.6) -> tuple[List[Room], Player]:
    """
    Создаёт подземелье:
    1. Загружает данные из json
    2. Создаёт игрока
    3. Создаёт комнаты (первая=St, последняя=Ex)
    4. Добавляет врагов с шансом enemy_chance
    :param num_rooms:
    :param enemy_chance:
    :return:
    """
    rooms_data = load_json_file("data/rooms.json")
    descriptions = rooms_data["rooms"]

    # 2. Игрок (возвращаем отдельно)
    player = create_player()

    # 3-4. Комнаты + враги
    rooms = []
    for i in range(num_rooms):
        # Случайное описание комнаты
        room_desc = random.choice(descriptions)

        # Враг с шансом enemy_chance (кроме старта и выхода)
        enemy = None
        if 0 < i < num_rooms - 1 and random.random() < enemy_chance:
            enemy = create_enemy()

        is_start = (i == 0)
        is_exit = (i == num_rooms - 1)

        rooms.append(Room(i, room_desc, enemy, is_start, is_exit))

    return rooms, player


def create_player() -> Player:
    """
    Создаёт случайного игрока из data/player.json.
    """
    data = load_json_file("data/players/players.json")
    player_def = random.choice(data["players"])
    death_texts = data["death_texts"]

    # Оружие/броня игрока
    weapons = {
        "dangerous_cudgel": Weapon("Опасная дубина", 5, 75)
    }
    armors = {
        "light_leather_armor": Armor("Лёгкий кожаный доспех", 2)
    }

    return Player(
        player_id=player_def["id"],
        name=player_def["name"],
        hp=player_def["hp"],
        desc=player_def["desc"],
        weapon=weapons[player_def["weapon_id"]],
        armor=armors[player_def["armor_id"]],
        death_texts=death_texts
    )


def create_enemy() -> Enemy:
    """
    Создаёт случайного врага из data/enemies.json.

    1. Загружает врагов и тексты смерти.
    2. Выбирает случайного врага + случайный текст смерти.
    3. Создаёт Weapon/Armor по ID.
    """
    data = load_json_file("data/enemies/enemies.json")
    enemy_def = random.choice(data["enemies"])
    death_text = random.choice(data["deaths"])

    weapons = {
        "bone": Weapon("Обглоданная кость", 5, 50),
        "rusty_knife": Weapon("Ржавый нож", 4, 75),
        "gravedigger_shovel": Weapon("Лопата могильщика", 5, 50)
    }

    # Броня врагов (по твоим ID)
    armors = {
        "tattered_rags": Armor("Рваные лохмотья", 1),
        "leather_armor": Armor("Кожаные доспехи", 3),
        "loincloth": Armor("Набедренная повязка", 0)
    }

    return Enemy(
        name=enemy_def["name"],
        hp=enemy_def["hp"],
        desc=enemy_def["desc"],
        death_text=death_text,  # ← Случайный!
        weapon=weapons[enemy_def["weapon_id"]],
        armor=armors[enemy_def["armor_id"]]
    )
