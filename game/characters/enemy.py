from .base import Character, Weapon, Armor


class Enemy(Character):
    def __init__(self, name: str, hp: int, desc: str, death_text: str, weapon: Weapon, armor: Armor):
        super().__init__(name, hp, weapon, armor)
        self.desc = desc
        self.death_text = death_text or "Противник повержен!"

    def on_death(self) -> None:
        """Выводит текст смерти врага."""
        print(f"{self.name} пал! {self.death_text}")

    def __str__(self) -> str:
        return f"{self.name} (HP: {self.hp}/{self.max_hp}) — {self.desc}, \n'Оружие': {self.weapon}\n'Броня'{self.armor}'"
