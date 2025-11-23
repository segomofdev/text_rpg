from .base import Character


class Enemy(Character):
    def __init__(self, name: str, hp: int, description: str, death_text: str, weapon_id: str, armor_id: str):
        super().__init__(name, hp, weapon_id, armor_id)
        self.description = description
        self.death_text = death_text

    def on_death(self) -> None:
        print(f"{self.name} пал! {self.death_text}")

    def __str__(self):
        return f"{self.name} (HP: {self.hp}/{self.max_hp}) — {self.description}"
