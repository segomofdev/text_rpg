import random
from typing import List, Tuple
from utils.json_loader import load_json_file
from .models import Player, Enemy, Room, Weapon, Armor


class Dungeon:
    """
    Генератор
    подземелья
    """
    def __init__(self, num_rooms: int = 7, enemy_count: int = 3):
        self.num_rooms = num_rooms
        self.enemy_count = enemy_count

    def build(self) -> Tuple[List[str], List[Room], Player]:
        """Создаёт подземелье по ТЗ."""
        # Карта символов
        dungeon_map = self._generate_map()

        # Полные комнаты
        rooms = self._generate_rooms(dungeon_map)

        # Игрок
        player = self._create_player()

        return dungeon_map, rooms, player

    def _generate_map(self) -> List[str]:
        """['St', ' ', 'E', ...]"""
        map_ = ['St'] + [' '] * (self.num_rooms - 2) + ['Ex']
        positions = random.sample(range(1, self.num_rooms - 1), min(self.enemy_count, self.num_rooms - 2))
        for pos in positions:
            map_[pos] = 'E'
        return map_

    def _generate_rooms(self, dungeon_map: List[str]) -> List[Room]:
        rooms_data = load_json_file("rooms.json")["rooms"]
        enemies_data = load_json_file("enemies/enemies.json")
        enemy_weapons = load_json_file("enemies/weapons.json")["weapons"]
        enemy_armors = load_json_file("enemies/armor.json")["armor"]

        rooms: List[Room] = []
        for i, room_type in enumerate(dungeon_map):
            desc = random.choice(rooms_data)
            enemy = None

            if room_type == 'E':
                enemy_def = random.choice(enemies_data["enemies"])
                death_text = random.choice(enemies_data["deaths"])

                weapon_def = random.choice(enemy_weapons)
                armor_def = random.choice(enemy_armors)

                weapon = Weapon(
                    name=weapon_def["name"],
                    damage=weapon_def["damage"],
                    hit_chance=weapon_def["hit_chance"],
                )
                armor = Armor(
                    name=armor_def["name"],
                    defense=armor_def["defense"],
                )

                enemy = Enemy(
                    name=enemy_def["name"],
                    hp=enemy_def["hp"],
                    description=enemy_def["desc"],
                    death_text=death_text,
                    weapon=weapon,
                    armor=armor,
                )

            rooms.append(
                Room(
                    index=i,
                    description=desc,
                    enemy=enemy,
                    is_start=(room_type == "St"),
                    is_exit=(room_type == "Ex"),
                )
            )

        return rooms

    def create_enemy(self) -> Enemy:
        """Создает случайного врага со случайным оружием и броней"""
        enemies_data = load_json_file("enemies/enemies.json")
        weapons_data = load_json_file("enemies/weapons.json")
        armors_data = load_json_file("enemies/armor.json")

        enemy_def = random.choice(enemies_data["enemies"])
        death_text = random.choice(enemies_data["deaths"])

        weapon_def = random.choice(weapons_data["weapons"])
        armor_def = random.choice(armors_data["armor"])

        weapon = Weapon(
            name=weapon_def["name"],
            damage=weapon_def["damage"],
            hit_chance=weapon_def["hit_chance"],
        )
        armor = Armor(
            name=armor_def["name"],
            defense=armor_def["defense"],
        )

        return Enemy(
            name=enemy_def["name"],
            hp=enemy_def["hp"],
            desc=enemy_def["desc"],
            death_text=death_text,
            weapon=weapon,
            armor=armor,
        )

    def _create_player(self) -> Player:
        """"""
        players_data = load_json_file("players/players.json")
        weapons_data = load_json_file("players/weapons.json")["weapons"]
        armor_data = load_json_file("players/armor.json")["armor"]

        player_def = random.choice(players_data["players"])
        death_texts = players_data["death_texts"]

        weapon_def = next(w for w in weapons_data if w["id"] == player_def["weapon_id"])
        armor_def = next(a for a in armor_data if a["id"] == player_def["armor_id"])

        weapon = Weapon(
            weapon_def["title"],
            weapon_def["damage"],
            weapon_def["hit_chance"]
        )
        armor = Armor(
            armor_def["title"],
            armor_def["defense"]
        )

        return Player(
            player_def["id"],
            player_def["name"],
            player_def["hp"],
            player_def["desc"],
            weapon,
            armor,
            death_texts
        )
