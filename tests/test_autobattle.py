from core.autobattle import AutoBattle


def test_calc_damage_formula():
    """Тест формулы расчета урона"""
    battle = AutoBattle.__new__(AutoBattle)

    assert battle._calc_damage(10, 3) == 7
    assert battle._calc_damage(5, 5) == 0
    assert battle._calc_damage(4, 10) == 0


def test_is_hit_true(monkeypatch, dummy_random):
    """Попадание, если hit_chance >= roll."""
    battle = AutoBattle.__new__(AutoBattle)
    rnd = dummy_random([20])
    monkeypatch.setattr("core.autobattle.random", rnd)
    assert battle._is_hit(50) is True


def test_is_hit_false(monkeypatch, dummy_random):
    """Промах, если hit_chance < roll."""
    battle = AutoBattle.__new__(AutoBattle)
    rnd = dummy_random([80])
    monkeypatch.setattr("core.autobattle.random", rnd)
    assert battle._is_hit(50) is False


def test_full_battle_player_wins(monkeypatch, dummy_random, player_and_enemy, capsys):
    """Игрок побеждает при гарантированном попадании."""
    player, enemy = player_and_enemy
    battle = AutoBattle(player, enemy)
    rnd = dummy_random([0] * 20)
    monkeypatch.setattr("core.autobattle.random", rnd)

    battle.run()

    assert enemy.is_alive is False
    assert player.is_alive is True


def test_is_hit_true_when_roll_less_or_equal(monkeypatch, dummy_random):
    """_is_hit возвращает True, если hit_chance ≥ случайного броска."""
    battle = AutoBattle.__new__(AutoBattle)
    rnd = dummy_random([20])  # randint -> 20
    monkeypatch.setattr("core.autobattle.random", rnd)

    assert battle._is_hit(50) is True


def test_is_hit_false_when_roll_greater(monkeypatch, dummy_random):
    """_is_hit возвращает False, если hit_chance < случайного броска."""
    battle = AutoBattle.__new__(AutoBattle)
    rnd = dummy_random([80])  # randint -> 80
    monkeypatch.setattr("core.autobattle.random", rnd)

    assert battle._is_hit(50) is False


def test_full_battle_player_wins(monkeypatch, dummy_random, make_player_enemy, capsys):
    """При 100% попадании игрока и 0% врага игрок всегда побеждает."""
    player, enemy = make_player_enemy
    battle = AutoBattle(player, enemy)

    rnd = dummy_random([0] * 20)
    monkeypatch.setattr("core.autobattle.random", rnd)

    battle.run()

    out = capsys.readouterr().out
    assert "Вы решительно бросаетесь на противника" in out
    assert "Вы одержали победу над" in out
    assert enemy.is_alive is False
    assert player.is_alive is True
    assert 0 < player.hp <= player.max_hp
