import math
import os.path
from typing import Tuple, List

import constants
import mcts
from constants import Color as C
from uttt import UTTT, draw_grids, translate_mouse_pos

try:
    import sys
    import pygame
    from pygame.locals import *
except ImportError as err:
    print(f"couldn't load module. {err}")
    sys.exit(2)


def update_main_view(background, screen, uttt):
    background.fill(C.WHITE.value)
    uttt.display_playable_zone(background)
    uttt.display_won_boards(background)
    uttt.display_board(background)
    draw_grids(background)
    screen.blit(background, (0, 0))
    pygame.display.flip()


def main():
    # Initialize ultimate ttt
    uttt = UTTT()

    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode(constants.SCREEN_SIZE)
    pygame.display.set_caption('Ultimate Tic Tac Toe')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(C.WHITE.value)

    # Display grids and playable zone
    uttt.display_playable_zone(background)
    draw_grids(background)

    screen.blit(background, (0, 0))

    # Update screen
    pygame.display.flip()
    check_move = False
    # Event loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_c:
                check_move = True
            elif event.type == MOUSEBUTTONDOWN:
                result = translate_mouse_pos(event.pos)
                if result is not None:
                    board, cell = result
                    if uttt.is_legal((board, cell)):
                        # uttt.print()
                        uttt.move((board, cell))
                        # print(uttt.current_board)
                        # uttt.print()
                        update_main_view(background, screen, uttt)
                        if uttt.is_win():
                            print('Human wins')
                            running = False

                        result = mcts.get_best_move(uttt)

                        uttt.move(result)
                        update_main_view(background, screen, uttt)

                        if uttt.is_win():
                            print('AI wins')
                            running = False


if __name__ == '__main__':
    main()
