class TTT:
    board: list[list[int]]
    current_player: int

    def __init__(self):
        self.board = [[0 for _ in range(3)] for _ in range(3)]
        self.current_player = 1

    def print(self):
        for i in range(3):
            for j in range(3):
                print(self.board[i][j], end=' ')
            print()

    def move(self, pos):
        self.board[pos[0]][pos[1]] = self.current_player
        self.current_player = -self.current_player

    def is_legal(self, pos):
        return self.board[pos[0]][pos[1]] == 0

    def is_full(self):
        return all([self.board[i][j] != 0 for i in range(3) for j in range(3)])

    def is_win(self):
        return any([all([self.board[0][i] == -self.current_player for i in range(3)]),
                    all([self.board[1][i] == -self.current_player for i in range(3)]),
                    all([self.board[2][i] == -self.current_player for i in range(3)]),
                    all([self.board[i][0] == -self.current_player for i in range(3)]),
                    all([self.board[i][1] == -self.current_player for i in range(3)]),
                    all([self.board[i][2] == -self.current_player for i in range(3)]),
                    all([self.board[i][i] == -self.current_player for i in range(3)]),
                    all([self.board[i][2 - i] == -self.current_player for i in range(3)])])

    def is_draw(self):
        return self.is_full() and not self.is_win()

    def get_legal_moves(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == 0]

    def game_loop(self):
        player = 1
        while True:
            self.print()
            print()
            while True:
                pos = input("Enter position: ")
                pos = pos.split(',')
                pos = (int(pos[0]), int(pos[1]))
                if self.is_legal(pos):
                    break
                print("Illegal move")

            self.move(pos)
            if self.is_win():
                break
            player = -player


if __name__ == '__main__':
    game = TTT()
    # game.print()
    game.game_loop()