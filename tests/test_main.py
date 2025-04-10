import pytest
from unittest.mock import MagicMock
from znakegame.enums import GridSpecs
from znakegame.main import ZnakeGame


@pytest.fixture
def game() -> ZnakeGame:
    mock_root = MagicMock()
    game = ZnakeGame(mock_root)
    return game


@pytest.mark.parametrize(
    "start_position, direction, expected_head_position",
    [
        ((5, 5), "Right", (6, 5)),
        ((5, 5), "Left", (4, 5)),
        ((5, 5), "Up", (5, 4)),
        ((5, 5), "Down", (5, 6)),
    ],
)
def test_move_znake_with_direction(
    game: ZnakeGame,
    start_position: tuple[int, int],
    direction: str,
    expected_head_position: tuple[int, int],
) -> None:
    """Test head is in the new expected position after a move."""
    game.znake = [start_position]  # Only the head
    game.direction = direction
    game.move_znake()
    assert game.znake[0] == expected_head_position


def test_food_spawn_not_in_znake(game: ZnakeGame) -> None:
    """Test that food is not spawned on top of the znake."""
    game.znake = [(5, 5), (4, 5), (3, 5)]
    food_position = game.spawn_food()
    assert food_position not in game.znake


def test_food_spawn_within_grid(game: ZnakeGame) -> None:
    """Test that food is spawned within valid grid bounds."""
    food_position = game.spawn_food()
    x, y = food_position
    assert 0 <= x < GridSpecs.X_PROPORTION.value
    assert 0 <= y < GridSpecs.Y_PROPORTION.value


def test_food_spawn_randomness(game: ZnakeGame) -> None:
    """Test that food spawning is random."""
    food_positions = set()
    for _ in range(100):
        food_position = game.spawn_food()
        food_positions.add(food_position)

        # Test that the food does not spawn in the znake
        assert food_position not in game.znake

    # Ensure that food is spawning in multiple locations
    assert len(food_positions) > 1


def test_game_over_on_self_collision(game: ZnakeGame) -> None:
    """Test the game stops when the znake collides with itself."""
    game.znake = [(5, 5), (4, 5), (3, 5)]
    game.direction = "Right"

    game.znake.append((6, 5))
    game.move_znake()
    assert not game.running


def test_game_over_on_boundary_wrap(game: ZnakeGame) -> None:
    """Test the game doesn't crash when the znake wraps around the boundary."""
    game.znake = [(GridSpecs.X_PROPORTION.value, GridSpecs.Y_PROPORTION.value)]
    game.direction = "Right"
    game.move_znake()
    assert game.znake[0][0] == 0
    assert game.znake[0][1] == -1


def test_food_eaten(game: ZnakeGame) -> None:
    """Test that the znake grows when it eats food."""
    game.znake = [(5, 5), (4, 5), (3, 5)]
    game.food = (6, 5)
    game.direction = "Right"
    game.move_znake()
    assert len(game.znake) == 4
    assert game.food != (6, 5)
    assert game.score == 1


def test_handle_restart_starts_game(game: ZnakeGame) -> None:
    """Ensure game restart resets the game."""
    game.znake = [(1, 1), (2, 1), (3, 1)]
    game.awaiting_restart = True

    event = MagicMock()
    game.handle_restart(event)

    assert not game.awaiting_restart
    assert game.znake == [(6, 5), (5, 5), (4, 5)]
