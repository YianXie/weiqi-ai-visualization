from sgfmill import sgf
from sgfmill.boards import Board
import pygame

# Open the SGF file and read the game data
with open("data/2.sgf", "rb") as f:
    game = sgf.Sgf_game.from_bytes(f.read())

# Get the winner, board size, and players
winner = game.get_winner()
board_size = game.get_size()
root_node = game.get_root()
b_player = root_node.get("PB")
w_player = root_node.get("PW")
moves = [node.get_move() for node in game.get_main_sequence()]

board = Board(board_size)

# Constants for the Pygame display
SCREEN_SIZE = 800
STONE_SIZE = SCREEN_SIZE // board_size
MARGIN = STONE_SIZE // 2
BOARD_COLOR = (222, 184, 135)  # Wood color
DOT_COLOR = (28, 28, 28)  # Dark color for the 3-3 points

pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))


def draw_board():
    screen.fill(BOARD_COLOR)
    for i in range(board_size):
        # Horizontal lines
        pygame.draw.line(
            screen,
            (0, 0, 0),
            (MARGIN, MARGIN + i * STONE_SIZE),
            (MARGIN + (board_size - 1) * STONE_SIZE, MARGIN + i * STONE_SIZE),
        )
        # Vertical lines
        pygame.draw.line(
            screen,
            (0, 0, 0),
            (MARGIN + i * STONE_SIZE, MARGIN),
            (MARGIN + i * STONE_SIZE, MARGIN + (board_size - 1) * STONE_SIZE),
        )
        if board_size == 19 and i in [4 - 1, 10 - 1, 16 - 1]:
            for x in range(3):  # 3 dots per row/col
                # Horizontal dots
                pygame.draw.circle(
                    screen,
                    DOT_COLOR,
                    (
                        MARGIN + STONE_SIZE * i + (x * 6 * STONE_SIZE),
                        MARGIN + STONE_SIZE * i,
                    ),
                    STONE_SIZE // 5,
                )
                # Vertical dots
                pygame.draw.circle(
                    screen,
                    DOT_COLOR,
                    (
                        MARGIN + STONE_SIZE * i,
                        MARGIN + STONE_SIZE * i + (x * 6 * STONE_SIZE),
                    ),
                    STONE_SIZE // 5,
                )


def draw_stones():
    for x in range(board_size):
        for y in range(board_size):
            color = board.get(x, y)
            if color:
                pygame.draw.circle(
                    screen,
                    (0, 0, 0) if color == "b" else (255, 255, 255),
                    (
                        MARGIN + x * STONE_SIZE,
                        MARGIN + y * STONE_SIZE,
                    ),
                    STONE_SIZE // 2 - 3,
                )


running = True
move_index = 0
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if move_index < len(game.get_main_sequence()):
                color, move = moves[move_index]
                if move:
                    x, y = move
                    board.play(x, y, color)
                move_index += 1

    draw_board()
    draw_stones()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
