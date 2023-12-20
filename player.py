from time import sleep
from random import choice
from typing import List

from action import Action


class Player:
    def __init__(self, is_human: bool = False):
        self.is_human = is_human

    def get_action(self, actions: List[Action]) -> Action:
        raise NotImplemented()


class HumanPlayer(Player):
    def __init__(self):
        super().__init__(is_human=True)

    def get_action(self, actions: List[Action]) -> Action:
        possible_actions = {action.key: action for action in actions}
        user_input = input()
        while user_input not in possible_actions:
            user_input = input()
        return possible_actions[user_input]


class RandomAIPlayer(Player):
    def __init__(self):
        super().__init__(is_human=False)

    def get_action(self, actions: List[Action]) -> Action:
        sleep(3)
        return choice(actions)
