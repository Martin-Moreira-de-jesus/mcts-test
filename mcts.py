from __future__ import annotations

import random
from math import sqrt, log

from uttt import UTTT
from copy import deepcopy


class Node:
    state: UTTT
    parent: Node
    children: list[Node]
    wins: int
    visits: int
    actions_left: list[list[int, int], list[int, int]]

    def __init__(self, uttt, parent=None, action=None):
        self.action = action
        self.state = uttt
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0
        self.actions_left = self.state.get_legal_moves()
        self.current_player = self.state.current_player

    # is leaf node
    def is_leaf(self):
        return len(self.actions_left) != 0

    def select(self) -> Node | None:
        if self.is_leaf() or self.is_terminal():
            return self
        else:
            return self.get_best_child().select()

    def is_terminal(self):
        return self.state.is_win() or self.state.is_draw()

    def expand(self) -> Node:
        action = self.actions_left.pop()
        new_state = deepcopy(self.state)
        new_state.move(action)
        child = Node(new_state, self, action)
        self.children.append(child)
        return child

    def simulate(self) -> int | float:
        state = deepcopy(self.state)
        value = 1
        if state.is_win():
            return value
        while not state.is_draw():
            actions = state.get_legal_moves()
            for action in actions:
                if state.is_winnable(action):
                    return value
            action = actions[random.randint(0, len(actions) - 1)]
            state.move(action)
            if state.is_win():
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


def get_best_move(uttt, simulations=2000):
    root = Node(uttt)
    for _ in range(simulations):
        leaf = root.select()
        if leaf.is_terminal():
            result = leaf.simulate()
            leaf.backpropagate(result)
        else:
            child = leaf.expand()
            result = child.simulate()
            child.backpropagate(result)
    for child in root.children:
        print("action=", child.action)
        print(f'value=%.2f' % child.get_value())
        print(f'visits=%d' % child.visits)
        print(f'visits/parent=%.2f' % (child.visits / root.visits))
    return root.get_best_move()
