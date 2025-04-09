"""Location for enum classes."""

import enum


class GridSpecs(enum.IntEnum):
    """Enums for grid specifications."""

    WIDTH = 400
    HEIGHT = 400
    GRID_SIZE = 20
    DELAY = 200  # in ms
    X_PROPORTION = WIDTH // GRID_SIZE
    Y_PROPORTION = HEIGHT // GRID_SIZE
