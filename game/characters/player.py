import random
from .base import Character, Weapon, Armor


class Player(Character):
    def __init__(self, player_id: str, name: str, hp: int, desc: str,
                 weapon: Weapon, armor: Armor, death_texts=list[str]):
        super().__init__(name, hp, weapon, armor)
        self.player_id = player_id
        self.desc = desc
        self.death_texts = death_texts or ["Вы погибли."]

    def on_death(self) -> None:
        """Выводит случайный текст смерти игрока"""
        print(random.choice(self.death_texts))

    def __str__(self) -> str:
        return f'{self.name} (HP: {self.hp}/{self.max_hp}) - {self.desc}'
