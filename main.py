import tkinter as tk

from enums import GridSpecs


class ZnakeGame:
    """A class to represent a Znake game."""

    def __init__(self, game_window) -> None:
        self.game_window = game_window
        self.game_window.title("znake Game")
        self.canvas = tk.Canvas(
            game_window,
            width=GridSpecs.WIDTH.value,
            height=GridSpecs.HEIGHT.value,
            bg="black",
        )
        self.canvas.pack()
        self.znake = [(5, 5), (4, 5), (3, 5)]
        self.direction = "Right"
        self.game_window.bind("<KeyPress>", self.change_direction)
        self.running = True
        self.game_loop()

    def game_loop(self) -> None:
        """
        The 'main' game function. This function checks for the self.running status and either continues or
        stops the game.
        If the game is continued, we wait for the specified 'delay' time, before running the game again.
        """
        if self.running:
            self.move_znake()
            self.draw()
            self.game_window.after(GridSpecs.DELAY, self.game_loop)
        else:
            self.canvas.create_text(
                GridSpecs.WIDTH // 2,
                GridSpecs.HEIGHT // 2,
                text="Game Over",
                fill="white",
                font=("Arial", 24),
            )

    def change_direction(self, event) -> None:
        """Based on user key input, change the direction of the znake."""
        if event.keysym in self.directions():
            new_dir = event.keysym
            # Prevent the znake from reversing directly
            if (
                self.directions()[new_dir][0] != -self.directions()[self.direction][0]
                or self.directions()[new_dir][1]
                != -self.directions()[self.direction][1]
            ):
                self.direction = new_dir

    def move_znake(self) -> None:
        """
        Calculate where the new znake head segment should be in the grid.
        This is added to the znake, while the oldest segment is removed.
        This simulates 'movement' of the znake.
        """

        head_x, head_y = self.znake[0]

        if head_x >= GridSpecs.X_PROPORTION:
            head_x = -1
        elif head_x == -1:
            head_x = GridSpecs.X_PROPORTION

        if head_y >= GridSpecs.Y_PROPORTION:
            head_y = -1
        elif head_y == -1:
            head_y = GridSpecs.Y_PROPORTION

        delta_x, delta_y = self.directions()[self.direction]
        new_head = (head_x + delta_x, head_y + delta_y)

        # Check collision
        if new_head in self.znake:
            self.running = False
            return

        self.znake.insert(0, new_head)
        self.znake.pop()

    def draw(self) -> None:
        """
        Draw the znake after deleting the full grid, to only show the current znake location.
        Drawing will be based on the current location of the znake segments.
        Each segment is scaled up in size to be more visible.
        """
        self.canvas.delete("all")

        # Draw znake
        for segment in self.znake:
            x, y = segment
            self.canvas.create_rectangle(
                x * GridSpecs.GRID_SIZE,
                y * GridSpecs.GRID_SIZE,
                (x + 1) * GridSpecs.GRID_SIZE,
                (y + 1) * GridSpecs.GRID_SIZE,
                fill="green",
            )

    @staticmethod
    def directions() -> dict[str, tuple[int, int]]:
        """The possible key bound directions."""
        return {"Up": (0, -1), "Down": (0, 1), "Left": (-1, 0), "Right": (1, 0)}


if __name__ == "__main__":
    """Main initialisation function."""
    game_window = tk.Tk()
    game = ZnakeGame(game_window)
    game_window.mainloop()
