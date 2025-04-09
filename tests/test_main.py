"""Location for unit tests for main.py"""

import pytest
from unittest.mock import MagicMock
from znakegame.enums import GridSpecs
from znakegame.main import ZnakeGame


@pytest.fixture
def game() -> ZnakeGame:
    mock_root = MagicMock()
    game = ZnakeGame(mock_root)
    return game


def test_directions_keys(game: ZnakeGame) -> None:
    directions = game.directions()
    expected_keys = {"Up", "Down", "Left", "Right"}
    assert set(directions.keys()) == expected_keys


@pytest.mark.parametrize(
    "current_dir, key, expected",
    [
        ("Right", "Left", "Right"),  # should not reverse
        ("Left", "Right", "Left"),  # should not reverse
        ("Up", "Down", "Up"),  # should not reverse
        ("Down", "Up", "Down"),  # should not reverse
        ("Right", "Up", "Up"),  # valid change
        ("Down", "Left", "Left"),  # valid change
    ],
)
def test_change_direction_prevents_reverse(
    game: ZnakeGame, current_dir: str, key: str, expected: str
) -> None:
    game.direction = current_dir

    event = MagicMock()
    event.keysym = key
    game.change_direction(event)

    assert game.direction == expected


def test_move_znake_forward(game: ZnakeGame) -> None:
    game.znake = [(5, 5), (4, 5), (3, 5)]
    game.direction = "Right"
    game.move_znake()
    assert game.znake == [(6, 5), (5, 5), (4, 5)]


def test_move_znake_collision(game: ZnakeGame) -> None:
    game.znake = [(5, 5), (6, 5), (5, 5)]
    game.direction = "Right"
    game.move_znake()
    assert not game.running  # should stop game due to collision


def test_move_znake_wraparound_x(game: ZnakeGame) -> None:
    game.znake = [
        (GridSpecs.X_PROPORTION.value, 5),
        (GridSpecs.X_PROPORTION.value - 1, 5),
    ]
    game.direction = "Right"
    game.move_znake()
    head_x = game.znake[0][0]
    assert head_x == 0  # Should wrap to 0 after max


def test_move_znake_wraparound_y(game: ZnakeGame) -> None:
    game.znake = [(5, GridSpecs.Y_PROPORTION.value)]
    game.direction = "Down"
    game.move_znake()
    head_y = game.znake[0][1]
    assert head_y == 0  # Should wrap to 0 after max
