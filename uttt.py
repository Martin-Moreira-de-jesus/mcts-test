from ttt import TTT


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

    def move(self, pos_board, pos_cell):
        if self.current_board == (-1, -1):
            self.current_board = pos_board

        self.boards[self.current_board[0]][self.current_board[1]].move(pos_cell)

        if self.boards[self.current_board[0]][self.current_board[1]].is_win():
            self.won_boards[self.current_board[0]][self.current_board[1]] = self.current_player

        if self.won_boards[self.current_board[0]][self.current_board[1]] != 0:
            self.current_board = (-1, -1)
        else:
            self.current_board = pos_cell

        self.current_player = -self.current_player

    def is_legal(self, pos):
        return self.boards[self.current_board[0]][self.current_board[1]].is_legal(pos)

    def is_win(self):
        return any([
            all([self.won_boards[0][i] for i in range(3) if self.won_boards[0][i] == self.current_player]),
            all([self.won_boards[1][i] for i in range(3) if self.won_boards[1][i] == self.current_player]),
            all([self.won_boards[2][i] for i in range(3) if self.won_boards[2][i] == self.current_player]),
            all([self.won_boards[i][0] for i in range(3) if self.won_boards[i][0] == self.current_player]),
            all([self.won_boards[i][1] for i in range(3) if self.won_boards[i][1] == self.current_player]),
            all([self.won_boards[i][2] for i in range(3) if self.won_boards[i][2] == self.current_player]),
            all([self.won_boards[i][i] for i in range(3) if self.won_boards[i][i] == self.current_player]),
            all([self.won_boards[i][2 - i] for i in range(3) if self.won_boards[i][2 - i] == self.current_player])
        ])

    def is_full(self):
        return all([self.boards[i][j].is_full() for i in range(3) for j in range(3)])

    def is_draw(self):
        return self.is_full() and not self.is_win()

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


if __name__ == '__main__':
    game = UTTT()

