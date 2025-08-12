from sgfmill.boards import Board
import pygame


class GameBoard:
    """A class to draw stones and board for Weiqi game"""

    running = True
    event_listeners = []
    screen_size = 800
    board_color = (222, 184, 135)  # Wood color
    dot_color = (28, 28, 28)  # Dark color for the 3-3 points

    def __init__(self, size: int):
        """Initialize the game board with a specific size.

        Args:
            size (int): the size of the board (e.g., 19 for a 19x19 board).
        """
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size))
        self.board_size = size
        self.board = Board(size)
        self.stone_size = self.screen_size // self.board_size
        self.margin = self.stone_size // 2

    def draw_board(self):
        """Draw the Weiqi board with lines and dots."""
        self.screen.fill(self.board_color)
        for i in range(self.board_size):
            # Horizontal lines
            pygame.draw.line(
                self.screen,
                (0, 0, 0),
                (self.margin, self.margin + i * self.stone_size),
                (
                    self.margin + (self.board_size - 1) * self.stone_size,
                    self.margin + i * self.stone_size,
                ),
            )
            # Vertical lines
            pygame.draw.line(
                self.screen,
                (0, 0, 0),
                (self.margin + i * self.stone_size, self.margin),
                (
                    self.margin + i * self.stone_size,
                    self.margin + (self.board_size - 1) * self.stone_size,
                ),
            )

            # Only if the board size is 19, draw the 3-3 points
            if self.board_size == 19 and i in [4 - 1, 10 - 1, 16 - 1]:
                for x in range(3):  # 3 dots per row/col
                    # Horizontal dots
                    pygame.draw.circle(
                        self.screen,
                        self.dot_color,
                        (
                            self.margin
                            + self.stone_size * i
                            + (x * 6 * self.stone_size),
                            self.margin + self.stone_size * i,
                        ),
                        self.stone_size // 5,
                    )
                    # Vertical dots
                    pygame.draw.circle(
                        self.screen,
                        self.dot_color,
                        (
                            self.margin + self.stone_size * i,
                            self.margin
                            + self.stone_size * i
                            + (x * 6 * self.stone_size),
                        ),
                        self.stone_size // 5,
                    )

    def add_stone(self, color: str, x: int, y: int):
        """Add a stone to the board at the specified position.

        Args:
            x (int): The x-coordinate of the stone.
            y (int): The y-coordinate of the stone.
            color (str): The color of the stone ('b' for black, 'w' for white).
        """
        if color not in ["b", "w"]:
            raise ValueError("Color must be 'b' for black or 'w' for white.")
        self.board.play(x, y, color)

    def draw_stones(self):
        """A method to draw stones on the board.

        Args:
            board (class): A class representing the board state, where .get(x, y) returns the color of the stone at position (x, y).
        """
        for x in range(self.board_size):
            for y in range(self.board_size):
                color = self.board.get(x, y)
                if color:
                    pygame.draw.circle(
                        self.screen,
                        (0, 0, 0) if color == "b" else (255, 255, 255),
                        (
                            self.margin + x * self.stone_size,
                            self.margin + y * self.stone_size,
                        ),
                        self.stone_size // 2 - 3,
                    )

    def update_display(self):
        """Update the display to show the drawn board and stones."""
        pygame.display.flip()

    def add_event_listener(self, event_type: str, callback: callable):
        """Add an event listener for a specific event type.

        Args:
            event_type (int): The type of the event to listen for.
            callback (callable): The function to call when the event occurs.
        """
        self.event_listeners.append((event_type, callback))

    def run(self):
        """Run the game loop to keep the display active."""
        while self.running:
            for event in pygame.event.get():
                for event_type, callback in self.event_listeners:
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == event_type:
                        callback(event)
            self.update_display()
            self.draw_board()
            self.draw_stones()
            pygame.time.Clock().tick(30)

    def quit(self):
        """Quit the pygame display."""
        self.running = False
        pygame.quit()
