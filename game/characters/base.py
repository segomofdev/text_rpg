from __future__ import annotations
from abc import ABC, abstractmethod


class ICharacter(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    @abstractmethod
    def hp(self) -> int:
        ...

    @property
    @abstractmethod
    def max_hp(self) -> int:
        ...

    @property
    @abstractmethod
    def is_alive(self) -> bool:
        ...

    @abstractmethod
    def take_damage(self, amount: int) -> None:
        ...

    @abstractmethod
    def heal(self, amount: int) -> None:
        ...


class Character(ICharacter):
    def __init__(self, name: str, hp: int, weapon: str = None, armor: str = None):
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
    def weapon(self) -> str:
        return self._weapon

    @property
    def armor(self) -> str:
        return self._armor

    @property
    def is_alive(self) -> bool:
        return self._hp > 0

    def take_damage(self, amount: int) -> None:
        prev = self._hp
        self._hp = max(self._hp - amount, 0)
        self.check_damage(prev)

    def heal(self, amount: int) -> None:
        prev = self._hp
        self._hp = min(self._hp + amount, self._max_hp)
        self.check_heal(prev)

    def check_damage(self, prev_hp: int) -> None:
        if prev_hp > 0 and self._hp == 0:
            self.on_death()

    def check_heal(self, prev_hp: int) -> None:
        if prev_hp < self._max_hp and self._hp == self._max_hp:
            self.on_full_health()

    def on_death(self) -> None:
        print(f"{self.name} погиб.")

    def on_full_health(self) -> None:
        print(f"{self.name} полностью здоров.")
