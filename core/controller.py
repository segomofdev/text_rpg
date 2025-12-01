import random
from typing import List, Tuple
from utils.json_loader import load_json_file
from .models import Player, Room
from .dungeon import Dungeon
from .autobattle import AutoBattle


class GameController:
    """
    Контроллер – это часть программы, которая отвечает за запрос данных от пользователя (через input()),
    обработку введенных данных, изменение данных у игровых сущностей и вывод результата на экран.
    """
    def __init__(self, dungeon_map: List[str], rooms: List[Room], player: Player):
        self.dungeon_map = dungeon_map
        self.rooms = rooms
        self.player = player
        self.current_room_index = 0  # начинаем со St
        self.exited = False

    def _input(self, prompt: str) -> str:
        """Общий ввод с поддержкой exit/quit в любой момент."""
        value = input(prompt).strip()
        if value.lower() in ("exit", "quit"):
            raise SystemExit("Игра завершена по желанию игрока.")
        return value

    def run(self) -> str:
        """
         Запуск игры
        """
        print("\nВведите 'exit' или 'quit', чтобы выйти из игры в любой момент.")
        print(f"\n🗡️ {self.player}")
        print("=" * 200)

        try:
            while self.player.is_alive and not self.exited:
                if not (0 <= self.current_room_index < len(self.rooms)):
                    break

                self._show_current_room()
                action = self._get_valid_action()
                if action is None:
                    break
                self._execute_action(action)
        except SystemExit as e:
            print(f"\n{e}")
            return ""

        return self._get_game_result()

    def _show_current_room(self) -> None:
        """Показать комнату + врага"""
        room = self.rooms[self.current_room_index]
        room_type = self.dungeon_map[self.current_room_index]

        print(f"\n🚪 Комната {self.current_room_index + 1}:")
        print(f"   {room.description}")

        if room.is_exit:
            print("🔚 Это выход из подземелья!")

        if room.has_alive_enemy:
            enemy = room.enemy
            print(
                f"⚔️ {enemy.name} (HP: {enemy.hp}/{enemy.max_hp})"
                f"Оружие: {enemy.weapon.name} — {enemy.weapon.damage} урона, "
                f"шанс попадания {enemy.weapon.hit_chance}%. "
                f"Броня: {enemy.armor.name} — защита {enemy.armor.defense}."
            )
        else:
            print("   Пусто")

    def _get_valid_action(self) -> int | None:
        """Возвращает номер доступного действия"""
        room_type = self.dungeon_map[self.current_room_index]
        room = self.rooms[self.current_room_index]
        actions = []

        # действия по условиям
        # 1 — Пойти дальше: только если НЕ последняя комната и не Ex
        if self.current_room_index < len(self.rooms) - 1 and not room.has_alive_enemy and room_type != "Ex":
            actions.append("1. Пойти дальше")
        # 2 — Назад
        if self.current_room_index > 0:
            actions.append("2. Вернуться назад")
        # 3 — Атаковать
        if room.has_alive_enemy:
            actions.append("3. Атаковать")
        # 4 — Выйти (только в Ex)
        if room_type == "Ex":
            actions.append("4. Выйти")

        while True:
            print("\nДоступные действия:")
            for action in actions:
                print(action)

            choice = self._input("Ваш выбор (номер): ").strip()

            if choice == "1" and "1. Пойти дальше" in actions:
                return 1
            elif choice == "2" and "2. Вернуться назад" in actions:
                return 2
            elif choice == "3" and "3. Атаковать" in actions:
                return 3
            elif choice == "4" and "4. Выйти" in actions:
                return 4
            else:
                print("❌ Неверный выбор!")

    def _execute_action(self, action: int) -> None:
        """Выполняет действие + результат из JSON."""
        results = load_json_file("results.json")

        if action == 1:
            # Пойти дальше
            # Защита, чтобы не выйти за пределы
            if self.current_room_index < len(self.rooms) - 1:
                self.current_room_index += 1
                print(random.choice(results["move_forward"]))

        elif action == 2:
            # Назад
            if self.current_room_index > 0:
                self.current_room_index -= 1
                print(random.choice(results["move_back"]))

        elif action == 3:  # Атаковать
            battle = AutoBattle(self.player, self.rooms[self.current_room_index].enemy)
            battle.run()

        elif action == 4:  # Выйти
            print("🎉 Выход из подземелья!")
            self.exited = True

    def _get_game_result(self) -> str:
        """Результат игры."""
        if not self.player.is_alive:
            return "💀 ПОРАЖЕНИЕ"
        elif self.dungeon_map[self.current_room_index] == "Ex":
            return "🏆 ПОБЕДА!"
