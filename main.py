from game.dungeon.dungeon import create_dungeon


def print_dungeon_pretty(rooms, player):
    """Красивый игровой вывод подземелья."""
    print(f"🗡️ ИГРОК: {player.name} (HP: {player.hp}/{player.max_hp})")
    print("=" * 60)

    for room in rooms:
        # Иконки
        prefix = "🚪 " if room.is_start else "🔥 " if room.has_alive_enemy else "🕳️ "
        suffix = " 🏁" if room.is_exit else ""

        # Враг
        if room.has_alive_enemy:
            enemy_info = f"⚔️ Есть враг! {room.enemy.name} (HP: {room.enemy.hp}/{room.enemy.max_hp})"
        else:
            enemy_info = "Пусто"

        print(f"{prefix}Комната {room.index + 1}{suffix}")
        print(f"   {room.description}")
        print(f"   {enemy_info}")
        print("-" * 40)


if __name__ == "__main__":
    rooms, player = create_dungeon(5, 1)
    print_dungeon_pretty(rooms, player)


