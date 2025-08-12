from sgfmill import sgf
from katago import KataGo
from game_board import GameBoard
import pygame
import pprint

# Open the SGF file and read the game data
with open("data/sgf/1.sgf", "rb") as f:
    game = sgf.Sgf_game.from_bytes(f.read())

# Get the winner, board size, and players
winner = game.get_winner()
board_size = game.get_size()
root_node = game.get_root()
b_player = root_node.get("PB")
w_player = root_node.get("PW")
all_moves = [node.get_move() for node in game.get_main_sequence()]
current_moves = []
current_moves_katago_format = []

move_index = 0

katago = KataGo()
katago.start()


def handle_keydown(event):
    global move_index, current_moves
    if event.key == pygame.K_SPACE:
        if move_index < len(all_moves):
            move = all_moves[move_index]
            if move.count(None) == 0:
                game_board.add_stone(move[0], move[1][0], move[1][1])
                current_moves.append(move)
                current_moves_katago_format.append(
                    [move[0], f"{chr(move[1][0] + 97)}{move[1][1]}"]
                )
                request = {
                    "id": f"analysis_request_{move_index}",
                    "moves": current_moves_katago_format,
                    "rules": "japanese",
                    "komi": 6.5,
                    "boardXSize": 19,
                    "boardYSize": 19,
                    "maxVisits": 100,
                    "analyzeTurns": [
                        move_index,
                    ],
                }
                response = katago.send_request(request)
                pprint.pprint(response, indent=2)
            move_index += 1


game_board = GameBoard(board_size)
game_board.add_event_listener(pygame.KEYDOWN, handle_keydown)
game_board.run()
