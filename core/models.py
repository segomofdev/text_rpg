from dataclasses import dataclass
from typing import Optional, List
from abc import ABC, abstractmethod
import random


@dataclass(frozen=True)
class Weapon:
    name: str
    damage: int
    hit_chance: int


@dataclass(frozen=True)
class Armor:
    name: str
    defense: int


@dataclass
class Room:
    index: int
    description: str
    enemy: Optional['Enemy'] = None
    is_start: bool = False
    is_exit: bool = False

    @property
    def has_alive_enemy(self) -> bool:
        return self.enemy is not None and self.enemy.is_alive


class ICharacter(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...
    @property
    @abstractmethod
    def hp(self) -> int: ...
    @property
    @abstractmethod
    def max_hp(self) -> int: ...
    @property
    @abstractmethod
    def is_alive(self) -> bool: ...
    @abstractmethod
    def take_damage(self, amount: int) -> None: ...


class Character(ICharacter):
    def __init__(self, name: str, hp: int, weapon: Weapon, armor: Armor):
        self._name = name
        self._max_hp = hp
        self._hp = hp
        self._weapon = weapon
        self._armor = armor

    @property
    def name(self) -> str: return self._name
    @property
    def hp(self) -> int: return self._hp
    @property
    def max_hp(self) -> int: return self._max_hp
    @property
    def weapon(self) -> Weapon: return self._weapon
    @property
    def armor(self) -> Armor: return self._armor
    @property
    def is_alive(self) -> bool: return self._hp > 0

    def take_damage(self, amount: int) -> None:
        assert amount > 0, f"Урон должен быть положительным: {amount}"
        prev = self._hp
        self._hp = max(self._hp - amount, 0)
        if prev > 0 and self._hp == 0:
            self.on_death()

    def on_death(self) -> None: pass


class Player(Character):
    def __init__(self, player_id: str, name: str, hp: int, desc: str,
                 weapon: Weapon, armor: Armor, death_texts: List[str]):
        super().__init__(name, hp, weapon, armor)
        self.player_id = player_id
        self.desc = desc
        self.death_texts = death_texts

    def on_death(self) -> None:
        print(random.choice(self.death_texts))

    def __str__(self) -> str:
        weapon_info = f"{self.weapon.name}(урон: {self.weapon.damage})"
        armor_info = f"{self.armor.name}(защита: {self.armor.defense})"
        return f"{self.name} (HP: {self.hp}/{self.max_hp}) — {self.desc}\nОружие:{weapon_info}\nБроня:{armor_info}"


class Enemy(Character):
    def __init__(self, name: str, hp: int, description: str, death_text: str,
                 weapon: Weapon, armor: Armor):
        super().__init__(name, hp, weapon, armor)
        self.description = description
        self.death_text = death_text

    def on_death(self) -> None:
        print(f"{self.name} пал! {self.death_text}")

    def __str__(self) -> str:
        return f"{self.name} (HP: {self.hp}/{self.max_hp}) — {self.description}"
