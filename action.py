from final_action import FinalAction
from turn_action import TurnAction
from menu import Menu


class Action:
    def __init__(self, key: str):
        self.key: str = key


class MenuAction(Action):
    def __init__(self, key: str, menu: Menu):
        super().__init__(key=key)
        self.menu = menu


class GameAction(Action):
    def __init__(self, key: str, turn_action: TurnAction):
        super().__init__(key=key)
        self.turn_action = turn_action


class FinalGameAction(Action):
    def __init__(self, key: str, final_action: FinalAction, message: str = ''):
        super().__init__(key=key)
        self.final_action = final_action
        self.message = message
