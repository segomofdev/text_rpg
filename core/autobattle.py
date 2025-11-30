import random
from .models import Player, Enemy


class AutoBattle:
    """Отвечает за автобой и вывод его хода"""

    def __init__(self, player: Player, enemy: Enemy):
        self.player = player
        self.enemy = enemy

    def run(self) -> None:
        """Запускает бой до смерти одного из участников"""
        print("\nВы решительно бросаетесь на противника. Завязался бой!")

        while self.player.is_alive and self.enemy.is_alive:
            self._player_turn()
            if not self.enemy.is_alive:
                break

            self._enemy_turn()
            if not self.player.is_alive:
                break

        if not self.enemy.is_alive:
            print(f"\nВы одержали победу над {self.enemy.name}!")
        elif not self.player.is_alive:
            print(f"\nВы пали в бою против {self.enemy.name}")

    # ходы сторон
    def _player_turn(self) -> None:
        print("\nВы наносите удар!")
        self._print_health()

        if self._is_hit(self.player.weapon.hit_chance):
            damage = self._calc_damage(self.player.weapon.damage, self.enemy.armor.defense)
            self.enemy.take_damage(damage)
            print(f"Удар пришелся точно в цель! "
                  f"Вы нанесли \"{damage}\" урона цели \"{self.enemy.name}\".")
        else:
            print(f"{self.enemy.name} увернулся от вашего удара.")

        self._print_enemy_health()

    def _enemy_turn(self) -> None:
        print(f"\n{self.enemy.name} наносит ответный удар. Берегитесь!")
        if self._is_hit(self.enemy.weapon.hit_chance):
            damage = self._calc_damage(self.enemy.weapon.damage,
                                       self.player.armor.defense)
            self.player.take_damage(damage)
            print(f"На этот раз вы не смогли увернуться... "
                  f"Противник нанес вам \"{damage}\" урона.")
        else:
            print("Удар был внезапным, но вы смогли увернуться. "
                  "Оружие пролетело в сантиметре от вашего лица.")

        self._print_player_health()

    # вспомогательные методы
    @staticmethod
    def _is_hit(hit_chance: int) -> bool:
        """Вероятность попадания по ТЗ: randint и сравнение с шансом."""
        roll = random.randint(0, 100)
        return hit_chance >= roll

    @staticmethod
    def _calc_damage(weapon_damage: int, armor_defense: int) -> int:
        """Урон по формуле из ТЗ."""
        if weapon_damage > armor_defense:
            return weapon_damage - armor_defense
        return 0

    def _print_health(self) -> None:
        print("\nСостояние здоровья у вас:")
        print(f"{self.player.name}. Здоровье: {self.player.hp}/{self.player.max_hp}")
        print(self._hp_bar(self.player.hp, self.player.max_hp))

        print("\nСостояние здоровья у противника:")
        print(f"{self.enemy.name}. Здоровье: {self.enemy.hp}/{self.enemy.max_hp}")
        print(self._hp_bar(self.enemy.hp, self.enemy.max_hp))

    def _print_player_health(self) -> None:
        print("\nСостояние здоровья у вас:")
        print(f"{self.player.name}. Здоровье: {self.player.hp}/{self.player.max_hp}")
        print(self._hp_bar(self.player.hp, self.player.max_hp))

    def _print_enemy_health(self) -> None:
        print("\nСостояние здоровья у противника:")
        print(f"{self.enemy.name}. Здоровье: {self.enemy.hp}/{self.enemy.max_hp}")
        print(self._hp_bar(self.enemy.hp, self.enemy.max_hp))

    @staticmethod
    def _hp_bar(hp: int, max_hp: int, width: int = 20) -> str:
        filled = int(width * hp / max_hp) if max_hp > 0 else 0
        return "[" + "█" * filled + " " * (width - filled) + "]"
