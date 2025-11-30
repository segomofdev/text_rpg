from core.dungeon import Dungeon
from core.controller import GameController


if __name__ == "__main__":
    # Генерация
    dungeon = Dungeon(7, 3)
    game_map, rooms, player = dungeon.build()

    # Запуск игры
    controller = GameController(game_map, rooms, player)
    result = controller.run()
    if result:
        print(f"\n{result}")
