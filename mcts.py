from __future__ import annotations

import random
from math import sqrt, log

from ttt import TTT
from copy import deepcopy


class Node:
    state: TTT
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

    def simulate(self) -> int:
        state = deepcopy(self.state)
        if state.is_win():
            return 1
        while not state.is_draw():
            action = state.get_legal_moves()[random.randint(0, len(state.get_legal_moves()) - 1)]
            state.move(action)
            if state.is_win():
                return 1
        return 0

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


def get_best_move(uttt):
    root = Node(uttt)
    for _ in range(10000):
        leaf = root.select()
        if leaf.is_terminal():
            result = leaf.simulate()
            leaf.backpropagate(result)
        else:
            child = leaf.expand()
            result = child.simulate()
            child.backpropagate(result)

    return root.get_best_move()


if __name__ == '__main__':
    uttt = TTT()
    uttt.print()
    while not uttt.is_full():
        while True:
            print("Enter position: ")
            pos = input().split(',')
            pos = (int(pos[0]), int(pos[1]))
            if uttt.is_legal(pos):
                break
        uttt.move(pos)
        uttt.print()
        if uttt.is_win():
            break
        best_move = get_best_move(uttt)
        uttt.move(best_move)
        uttt.print()
        if uttt.is_win():
            break
