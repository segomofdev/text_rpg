from core.models import Weapon, Armor, Player, Enemy


def test_character_take_damage_reduce_hp():
    """take_damage уменьшает hp на заданное значение."""
    w = Weapon("Скалка", 5, 100)
    a = Armor("Газета", 0)
    enemy = Enemy("Зубастик", 10, "desc", "dead", w, a)

    enemy.take_damage(3)
    assert enemy.hp == 7


def test_character_take_damage_not_below_zero():
    """take_damage не уменьшает hp ниже 0."""
    w = Weapon("Сабля", 5, 100)
    a = Armor("Полиэтилен", 0)
    enemy = Enemy("Гоблин", 5, "desc", "dead", w, a)

    enemy.take_damage(10)
    assert enemy.hp == 0


def test_character_is_alive_correct():
    """is_alive возвращает True только при hp > 0."""
    w = Weapon("Дробовик", 5, 100)
    a = Armor("Лента выпускника", 0)

    player = Player("p1", "Герой", 10, "desc", w, a, ["rip"])
    assert player.is_alive is True

    player.take_damage(10)
    assert player.is_alive is False


def test_player_on_death_prints_random_text():
    """Player.on_death выводит случайный текст из списка."""
    w = Weapon("Тест", 5, 100)
    a = Armor("Тест", 0)
    player = Player("p1", "Герой", 10, "desc", w, a, ["Текст 1", "Текст 2"])

    player.take_damage(10)  # hp=0 → on_death()
