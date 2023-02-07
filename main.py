import math
import os.path
import threading
from enum import Enum
from typing import Tuple, List

import constants
import mcts
from constants import Color as C
from constants import Scene
from uttt import UTTT, draw_grids, translate_mouse_pos

try:
    import sys
    import pygame
    from pygame.locals import *
except ImportError as err:
    print(f"couldn't load module. {err}")
    sys.exit(2)


def update_main_view(background, screen, uttt, player, scene):
    background.fill(C.WHITE.value)
    if scene == "turns" or player == uttt.current_player:
        uttt.display_playable_zone(background)
    uttt.display_won_boards(background)
    uttt.display_board(background)
    draw_grids(background)
    screen.blit(background, (0, 0))
    pygame.display.flip()


def display_main_menu(background, screen):
    background.fill(C.WHITE.value)
    # display title ultimate tic tac toe in the middle of the screen
    font = pygame.font.Font(None, 100)
    text = font.render("Ultimate Tic Tac Toe", 1, C.BLACK.value)
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    textpos.centery = background.get_rect().centery - 200
    background.blit(text, textpos)
    # display play button to play in turns
    font = pygame.font.Font(None, 50)
    text = font.render("Press t to play in turns", 1, C.BLACK.value)
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    textpos.centery = background.get_rect().centery
    background.blit(text, textpos)
    # display play button to play against AI
    font = pygame.font.Font(None, 50)
    text = font.render("Press a to play against AI", 1, C.BLACK.value)
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    textpos.centery = background.get_rect().centery + 100
    background.blit(text, textpos)
    # display play button to let AI play against AI
    font = pygame.font.Font(None, 50)
    text = font.render("Press s to let AI play against AI", 1, C.BLACK.value)
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    textpos.centery = background.get_rect().centery + 200
    background.blit(text, textpos)
    screen.blit(background, (0, 0))
    pygame.display.flip()


def threaded(f, daemon=False):
    import queue

    def wrapped_f(q, *args, **kwargs):
        '''this function calls the decorated function and puts the
        result in a queue'''
        ret = f(*args, **kwargs)
        q.put(ret)

    def wrap(*args, **kwargs):
        '''this is the function returned from the decorator. It fires off
        wrapped_f in a new thread and returns the thread object with
        the result queue attached'''

        q = queue.Queue()

        t = threading.Thread(target=wrapped_f, args=(q,) + args, kwargs=kwargs)
        t.daemon = daemon
        t.start()
        t.result_queue = q
        return t

    return wrap


@threaded
def compute_ia_move(uttt: UTTT):
    if uttt.current_player == -1:
        print("i get 2000")
        move = mcts.get_best_move(uttt, 2000)
    else:
        print("i get 1000")
        move = mcts.get_best_move(uttt, 1000)
    uttt.move(move)
    if uttt.is_win():
        print(f'Player {"blue" if uttt.current_player == 1 else "red"} wins')
        return True
    return False


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
    screen.blit(background, (0, 0))
    # Update screen
    pygame.display.flip()

    scene = Scene.MAIN_MENU
    # used for human vs IA and IA vs IA
    ia_win = False
    ia_move = None
    # Event loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif scene == Scene.MAIN_MENU:
                if event.type == KEYDOWN:
                    if event.key == K_t:
                        scene = Scene.TURNS
                    elif event.key == K_a:
                        scene = Scene.HUMAN_VS_IA
                    elif event.key == K_s:
                        scene = Scene.AI_VS_AI
            if scene == Scene.TURNS and event.type == MOUSEBUTTONDOWN:
                result = translate_mouse_pos(event.pos)
                if result is not None:
                    board, cell = result
                    if uttt.is_legal((board, cell)):
                        uttt.move((board, cell))
                        if uttt.is_win():
                            print(f'Player {"blue" if uttt.current_player == 1 else "red"} wins')
                            running = False
            if scene == Scene.HUMAN_VS_IA and event.type == MOUSEBUTTONDOWN:
                if uttt.current_player == 1:
                    result = translate_mouse_pos(event.pos)
                    if result is not None:
                        board, cell = result
                        if uttt.is_legal((board, cell)):
                            uttt.move((board, cell))
                            if uttt.is_win():
                                print(f'Player {"blue" if uttt.current_player == 1 else "red"} wins')
                                running = False
                            else:
                                ia_win = compute_ia_move(uttt)

        if scene == Scene.AI_VS_AI:
            if not ia_win:
                ia_win = compute_ia_move(uttt)
            else:
                try:
                    if not ia_win.is_alive():
                        ia_win = False
                except:
                    pass

        if ia_win == True:
            print(f'Player {"blue" if uttt.current_player == 1 else "red"} wins')
            running = False

        if scene == Scene.MAIN_MENU:
            display_main_menu(background, screen)
        else:
            update_main_view(background, screen, uttt, uttt.current_player, scene)
            # elif event.type == MOUSEBUTTONDOWN:
            #     result = translate_mouse_pos(event.pos)
            #     if result is not None:
            #         board, cell = result
            #         if uttt.is_legal((board, cell)):
            #             uttt.move((board, cell))
            #             update_main_view(background, screen, uttt, -uttt.current_player)
            #             if uttt.is_win():
            #                 print('Human wins')
            #                 running = False
            #
            #             result = mcts.get_best_move(uttt)
            #
            #             uttt.move(result)
            #             update_main_view(background, screen, uttt, uttt.current_player)
            #
            #             if uttt.is_win():
            #                 print('AI wins')
            #                 running = False


if __name__ == '__main__':
    main()
