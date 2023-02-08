from __future__ import annotations

import copy
import random
from math import sqrt, log
from typing import Tuple

from uttt import UTTT
from copy import deepcopy


class Node:
    state: UTTT
    parent: Node
    children: list[Node]
    wins: int
    visits: int

    def __init__(self, parent=None, action=None):
        self.action = action
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0

    def actions_left(self, state):
        actions = state.get_legal_moves()
        for child in self.children:
            if child.action in actions:
                actions.remove(child.action)
        return actions

    # checks if node is a leaf
    # a leaf is a node that has actions left
    def is_leaf(self, state):
        return len(self.actions_left(state)) > 0

    def select(self, state: UTTT) -> tuple[Node, UTTT]:
        if self.parent is not None:
            state.move(self.action)
        else:
            state = copy.deepcopy(state)
        if self.is_leaf(state) or state.is_terminal():
            return self, state
        else:
            return self.get_best_child().select(state)

    def expand(self, state) -> tuple[Node, UTTT]:
        actions = self.actions_left(state)
        action = actions[random.randint(0, len(actions) - 1)]
        child = Node(self, action)
        self.children.append(child)
        state_copy = copy.deepcopy(state)
        state_copy.move(action)
        return child, state_copy

    def simulate(self, state) -> int | float:

        value = 1
        if state.is_win():
            return value
        state_copy = copy.deepcopy(state)
        while not state_copy.is_draw():
            actions = state_copy.get_legal_moves()
            # for action in actions:
            #     if state.is_winnable(action):
            #         return value
            action = actions[random.randint(0, len(actions) - 1)]
            state_copy.move(action)
            if state_copy.is_win():
                return value
            if value == 1:
                value = 0
            else:
                value = 1
        return 0.5

    def backpropagate(self, result) -> None:
        self.visits += 1
        self.wins += result
        if self.parent:
            self.parent.backpropagate(1 - result)

    def get_value(self):
        return self.wins / self.visits

    def get_ucb(self):
        return self.get_value() + sqrt(2 * log(self.parent.visits) / self.visits)

    def get_best_child(self):
        best = self.children[0]
        for child in self.children:
            if child.get_ucb() > best.get_ucb():
                best = child
        return best

    def get_best_move(self):
        return max(self.children, key=lambda c: c.get_value()).action


def build_state_from_moves(uttt, moves):
    uttt_copy = copy.copy(uttt)
    for move in moves:
        uttt_copy.move(move)
    return uttt_copy


def get_best_move(uttt, simulations=1000):
    root = Node()
    for _ in range(simulations):
        leaf, state = root.select(uttt)
        if state.is_terminal():
            result = leaf.simulate(state)
            leaf.backpropagate(result)
        else:
            child, state = leaf.expand(state)
            result = child.simulate(state)
            child.backpropagate(result)

    for child in root.children:
        print("action=", child.action)
        print("visits=", child.visits)
        print("wins=", child.wins)
        print("value=", child.get_value())
        print("ucb=", child.get_ucb())
        print()

    return root.get_best_move()


if __name__ == '__main__':
    from uttt import UTTT
    uttt = UTTT()
    uttt.print()
    while True:
        while True:
            if uttt.can_play_anywhere():
                pos_board = input("Enter board to play on :")
                pos_board = (int(pos_board[0]), int(pos_board[1]))
            else:
                pos_board = (-1, -1)

            pos_cell = input("Enter cell to play on :")
            pos_cell = (int(pos_cell[0]), int(pos_cell[1]))

            pos = (pos_board, pos_cell)

            if uttt.is_legal(pos):
                break

            print("Bad Input")

        uttt.move(pos)
        uttt.print()
        if uttt.is_win():
            print(f"Player {-uttt.current_player} won !")

        best_move = get_best_move(uttt, 1000)
        print(best_move)
