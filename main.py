from ttt import TTT
import mcts

ttt = TTT()
while not ttt.is_full():
    ttt.print()
    print()
    while True:
        pos = input("Enter position: ")
        pos = pos.split(',')
        pos = (int(pos[0]), int(pos[1]))
        if ttt.is_legal(pos):
            break
        print("Illegal move")
    ttt.move(pos)
    if ttt.is_win():
        print(f'Player {ttt.current_player} wins!')
        exit(0)
    pos = mcts.get_best_move(ttt)
    ttt.move(pos)
    if ttt.is_win():
        print(f'Player {ttt.current_player} wins!')
        exit(0)

print("No more moves")