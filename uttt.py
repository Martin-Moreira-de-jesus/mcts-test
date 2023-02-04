import math

import mcts
from ttt import TTT
import pygame
from constants import Color as C
from copy import deepcopy


def translate_mouse_pos(pos_clicked) -> tuple[tuple[int, int], tuple[int, int]] | None:
    # deduct where the player clicked
    # get the x and y of the subgrid
    board = (
        math.floor(pos_clicked[1] / 300),
        math.floor(pos_clicked[0] / 300)
    )

    # get the x and y of the cell
    # cell = (
    #     math.floor((pos_clicked[1] - board[1] * 300) / 100),
    #     math.floor((pos_clicked[0] - board[0] * 300) / 100)
    # )
    cell = (
        math.floor((pos_clicked[1] - board[0] * 300) / 100),
        math.floor((pos_clicked[0] - board[1] * 300) / 100)
    )

    if any([val > 2 for val in board + cell]):
        return None

    return board, cell


def draw_grids(surface: pygame.Surface) -> None:
    # Display main grid
    pygame.draw.line(surface, (0, 0, 0), (0, 300), (900, 300), 5)
    pygame.draw.line(surface, (0, 0, 0), (0, 600), (900, 600), 5)
    pygame.draw.line(surface, (0, 0, 0), (300, 0), (300, 900), 5)
    pygame.draw.line(surface, (0, 0, 0), (600, 0), (600, 900), 5)

    # Display the subgrids
    pygame.draw.line(surface, (0, 0, 0), (100, 20), (100, 280), 5)
    pygame.draw.line(surface, (0, 0, 0), (200, 20), (200, 280), 5)
    pygame.draw.line(surface, (0, 0, 0), (20, 100), (280, 100), 5)
    pygame.draw.line(surface, (0, 0, 0), (20, 200), (280, 200), 5)

    pygame.draw.line(surface, (0, 0, 0), (100, 320), (100, 580), 5)
    pygame.draw.line(surface, (0, 0, 0), (200, 320), (200, 580), 5)
    pygame.draw.line(surface, (0, 0, 0), (20, 400), (280, 400), 5)
    pygame.draw.line(surface, (0, 0, 0), (20, 500), (280, 500), 5)

    pygame.draw.line(surface, (0, 0, 0), (100, 620), (100, 880), 5)
    pygame.draw.line(surface, (0, 0, 0), (200, 620), (200, 880), 5)
    pygame.draw.line(surface, (0, 0, 0), (20, 700), (280, 700), 5)
    pygame.draw.line(surface, (0, 0, 0), (20, 800), (280, 800), 5)

    pygame.draw.line(surface, (0, 0, 0), (400, 20), (400, 280), 5)
    pygame.draw.line(surface, (0, 0, 0), (500, 20), (500, 280), 5)
    pygame.draw.line(surface, (0, 0, 0), (320, 100), (580, 100), 5)
    pygame.draw.line(surface, (0, 0, 0), (320, 200), (580, 200), 5)

    pygame.draw.line(surface, (0, 0, 0), (400, 320), (400, 580), 5)
    pygame.draw.line(surface, (0, 0, 0), (500, 320), (500, 580), 5)
    pygame.draw.line(surface, (0, 0, 0), (320, 400), (580, 400), 5)
    pygame.draw.line(surface, (0, 0, 0), (320, 500), (580, 500), 5)

    pygame.draw.line(surface, (0, 0, 0), (400, 620), (400, 880), 5)
    pygame.draw.line(surface, (0, 0, 0), (500, 620), (500, 880), 5)
    pygame.draw.line(surface, (0, 0, 0), (320, 700), (580, 700), 5)
    pygame.draw.line(surface, (0, 0, 0), (320, 800), (580, 800), 5)

    pygame.draw.line(surface, (0, 0, 0), (700, 20), (700, 280), 5)
    pygame.draw.line(surface, (0, 0, 0), (800, 20), (800, 280), 5)
    pygame.draw.line(surface, (0, 0, 0), (620, 100), (880, 100), 5)
    pygame.draw.line(surface, (0, 0, 0), (620, 200), (880, 200), 5)

    pygame.draw.line(surface, (0, 0, 0), (700, 320), (700, 580), 5)
    pygame.draw.line(surface, (0, 0, 0), (800, 320), (800, 580), 5)
    pygame.draw.line(surface, (0, 0, 0), (620, 400), (880, 400), 5)
    pygame.draw.line(surface, (0, 0, 0), (620, 500), (880, 500), 5)

    pygame.draw.line(surface, (0, 0, 0), (700, 620), (700, 880), 5)
    pygame.draw.line(surface, (0, 0, 0), (800, 620), (800, 880), 5)
    pygame.draw.line(surface, (0, 0, 0), (620, 700), (880, 700), 5)
    pygame.draw.line(surface, (0, 0, 0), (620, 800), (880, 800), 5)


class UTTT:
    def __init__(self):
        self.boards = [[TTT() for _ in range(3)] for _ in range(3)]
        self.current_player = 1
        self.current_board = (-1, -1)
        self.won_boards = [[0 for _ in range(3)] for _ in range(3)]

    def get_board(self, i, j):
        return self.boards[i][j]

    def get_current_board(self):
        return self.get_board(self.current_board[0], self.current_board[1])

    def get_won_board(self, i, j):
        return self.won_boards[i][j]

    def get_current_won_board(self):
        return self.get_won_board(self.current_board[0], self.current_board[1])

    def print(self):
        print(self.boards[0][0].board[0], '|', self.boards[0][1].board[0], '|', self.boards[0][2].board[0])
        print(self.boards[0][0].board[1], '|', self.boards[0][1].board[1], '|', self.boards[0][2].board[1])
        print(self.boards[0][0].board[2], '|', self.boards[0][1].board[2], '|', self.boards[0][2].board[2])
        print('-----------------')
        print(self.boards[1][0].board[0], '|', self.boards[1][1].board[0], '|', self.boards[1][2].board[0])
        print(self.boards[1][0].board[1], '|', self.boards[1][1].board[1], '|', self.boards[1][2].board[1])
        print(self.boards[1][0].board[2], '|', self.boards[1][1].board[2], '|', self.boards[1][2].board[2])
        print('-----------------')
        print(self.boards[2][0].board[0], '|', self.boards[2][1].board[0], '|', self.boards[2][2].board[0])
        print(self.boards[2][0].board[1], '|', self.boards[2][1].board[1], '|', self.boards[2][2].board[1])
        print(self.boards[2][0].board[2], '|', self.boards[2][1].board[2], '|', self.boards[2][2].board[2])
        print()

    def move(self, pos):
        pos_board = pos[0]
        pos_cell = pos[1]
        if self.current_board == (-1, -1):
            self.current_board = pos_board

        self.get_current_board().player_move(pos_cell, self.current_player)

        if self.get_current_board().is_player_win(self.current_player):
            self.won_boards[self.current_board[0]][self.current_board[1]] = self.current_player

        if self.won_boards[pos_cell[0]][pos_cell[1]] != 0:
            self.current_board = (-1, -1)
        else:
            self.current_board = pos_cell

        self.current_player = -self.current_player

    def is_legal(self, pos):
        return pos in self.get_legal_moves()

    def is_win(self):
        return any([
            all([self.won_boards[0][i] == -self.current_player for i in range(3)]),
            all([self.won_boards[1][i] == -self.current_player for i in range(3)]),
            all([self.won_boards[2][i] == -self.current_player for i in range(3)]),
            all([self.won_boards[i][0] == -self.current_player for i in range(3)]),
            all([self.won_boards[i][1] == -self.current_player for i in range(3)]),
            all([self.won_boards[i][2] == -self.current_player for i in range(3)]),
            all([self.won_boards[i][i] == -self.current_player for i in range(3)]),
            all([self.won_boards[i][2 - i] == -self.current_player for i in range(3)])
        ])

    def is_full(self):
        return all([self.boards[i][j].is_full() for i in range(3) for j in range(3)])

    def is_draw(self):
        return len(self.get_legal_moves()) == 0 and not self.is_win()

    def is_winnable(self, move) -> bool:
        uttt_copy = deepcopy(self)
        uttt_copy.move(move)
        return uttt_copy.is_win()

    def get_legal_moves(self):
        legal_moves = []
        if self.current_board == (-1, -1):
            for i in range(3):
                for j in range(3):
                    if self.won_boards[i][j] == 0:
                        cell_legal_moves = self.get_board(i, j).get_legal_moves()
                        for cell_legal_move in cell_legal_moves:
                            legal_moves.append(((i, j), cell_legal_move))
        else:
            cell_legal_moves = self.get_current_board().get_legal_moves()
            for cell_legal_move in cell_legal_moves:
                legal_moves.append((self.current_board, cell_legal_move))

        return legal_moves

    def print(self):
        print('-----------------------------')
        print(self.get_board(0, 0).board[0], '|', self.get_board(0, 1).board[0], '|', self.get_board(0, 2).board[0])
        print(self.get_board(0, 0).board[1], '|', self.get_board(0, 1).board[1], '|', self.get_board(0, 2).board[1])
        print(self.get_board(0, 0).board[2], '|', self.get_board(0, 1).board[2], '|', self.get_board(0, 2).board[2])
        print('-----------------------------')
        print(self.get_board(1, 0).board[0], '|', self.get_board(1, 1).board[0], '|', self.get_board(1, 2).board[0],
              '|', self.won_boards[0])
        print(self.get_board(1, 0).board[1], '|', self.get_board(1, 1).board[1], '|', self.get_board(1, 2).board[1],
              '|', self.won_boards[1])
        print(self.get_board(1, 0).board[2], '|', self.get_board(1, 1).board[2], '|', self.get_board(1, 2).board[2],
              '|', self.won_boards[2])
        print('-----------------------------')
        print(self.get_board(2, 0).board[0], '|', self.get_board(2, 1).board[0], '|', self.get_board(2, 2).board[0])
        print(self.get_board(2, 0).board[1], '|', self.get_board(2, 1).board[1], '|', self.get_board(2, 2).board[1])
        print(self.get_board(2, 0).board[2], '|', self.get_board(2, 1).board[2], '|', self.get_board(2, 2).board[2])
        print('-----------------------------')

    def can_play_anywhere(self):
        return self.current_board == (-1, -1)

    def display_board(self, surface: pygame.Surface):
        boards = self.boards
        for offset_x in [0, 300, 600]:
            for offset_y in [0, 300, 600]:
                for i in range(3):
                    curr_board = boards[offset_x // 300][offset_y // 300].board
                    for j in range(3):
                        if curr_board[i][j] == 1:
                            pygame.draw.circle(surface, C.RED.value,
                                               (50 + 100 * j + offset_y, 50 + 100 * i + offset_x), 30, 0)
                        elif curr_board[i][j] == -1:
                            pygame.draw.circle(surface, C.BLUE.value,
                                               (50 + 100 * j + offset_y, 50 + 100 * i + offset_x), 30, 0)

    def display_won_boards(self, surface: pygame.Surface):
        for offset_x in [0, 300, 600]:
            for offset_y in [0, 300, 600]:
                if self.won_boards[offset_x // 300][offset_y // 300] == 1:
                    pygame.draw.rect(surface, C.LIGHT_RED.value, (offset_y + 25, offset_x + 25, 250, 250))
                if self.won_boards[offset_x // 300][offset_y // 300] == -1:
                    pygame.draw.rect(surface, C.LIGHT_BLUE.value, (offset_y + 25, offset_x + 25, 250, 250))

    def display_playable_zone(self, surface: pygame.Surface):
        if self.can_play_anywhere():
            for offset_x in [0, 300, 600]:
                for offset_y in [0, 300, 600]:
                    pygame.draw.rect(surface, C.YELLOW.value, (offset_x + 25, offset_y + 25, 250, 250))
        else:
            pygame.draw.rect(surface, C.YELLOW.value,
                             (300 * self.current_board[1] + 25, 300 * self.current_board[0] + 25, 250, 250))
