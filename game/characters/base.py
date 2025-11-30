from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class Weapon:
    name: str
    damage: int
    hit_chance: int


@dataclass
class Armor:
    name: str
    defense: int


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
    def name(self) -> str:
        return self._name

    @property
    def hp(self) -> int:
        return self._hp

    @property
    def max_hp(self) -> int:
        return self._max_hp

    @property
    def weapon(self) -> Weapon:
        return self._weapon

    @property
    def armor(self) -> Armor:
        return self._armor

    @property
    def is_alive(self) -> bool:
        """Проверяет жив ли персонаж, hp > 0"""
        return self._hp > 0

    def on_death(self) -> None:
        """Вызывается при смерти персонажа (hp <= 0)
        Поведение:
         - в базовом классе ничего не делает;
         - Player: выводит случайный текст при смерти;
         - Enemy: выводит текст смерти врага;
         - Контроллер проверяет is_alive() после боя.
        """
        pass  # переопределяется в наследниках

    def take_damage(self, amount: int) -> None:
        """Наносит урон персонажу т проверяет смерть
        :param amount - количество урона для нанесения (int, > 0)
        Поведение:
         - уменьшает hp на amount, но не ниже 0;
         - Если hp перешло с >0 в 0, вызывает on_death();
         - Игнорирует урон <=0.
        """
        assert amount > 0, f"Урон должен быть положительным: {amount}"

        prev = self._hp
        self._hp = max(self._hp - amount, 0)

        if prev > 0 and self._hp == 0:
            self.on_death()


@dataclass
class Room:
    from game.characters.enemy import Enemy
    index: int
    description: str
    enemy: Optional[Enemy] = None
    is_start: bool = False
    is_exit: bool = False

    @property
    def has_alive_enemy(self) -> bool:
        """Есть ли живой враг в комнате."""
        return self.enemy is not None and self.enemy.is_alive
