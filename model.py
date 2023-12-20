from enum import Enum
from typing import Optional, List

from action import Action, MenuAction, GameAction, FinalGameAction
from menu import Menu
from observer import Observer
from player import Player, HumanPlayer, RandomAIPlayer
from turn_action import TurnAction, turn_actions_key_to_select
from final_action import FinalAction, final_actions_key_to_select


class GameState(str, Enum):
    leftTurn = 'leftTurn'
    rightTurn = 'rightTurn'
    finalScreen = 'finalScreen'


class AppState(str, Enum):
    menu = 'menu'
    game = 'game'
    exit = 'exit'


class Turn(str, Enum):
    left = 'left'
    right = 'right'


class Model:
    def __init__(self):
        self.app_state: AppState = AppState.menu
        self.game_state: GameState = GameState.leftTurn
        self.left_player: Optional[Player] = None
        self.right_player: Optional[Player] = None
        self.current_turn: Turn = Turn.left
        self.left_action: Optional[GameAction] = None
        self.right_action: Optional[GameAction] = None
        self.left_points: int = 0
        self.right_points: int = 0
        self.count_of_points_to_win: int = 1
        self.__init_menu()
        self.observers: List[Observer] = []
        self.quick_message: str = ''

    def __init_menu(self):
        self.menu: Menu = Menu(title='TopOne', tip='top one menu')
        menu_items: List[Menu] = [
            Menu(title='Play', tip='Begin game', parent_menu=self.menu, key_to_select='p'),
            Menu(title='Exit', tip='Close game', parent_menu=self.menu, key_to_select='e')
        ]
        self.menu.menu_items = menu_items
        self.current_menu: Menu = self.menu

    # Play
    ## Random AI
    ## Rock AI
    # Exit

    def subscribe(self, observer: Observer) -> None:
        self.observers.append(observer)

    def notify(self):
        for o in self.observers:
            o.notify()
        self.quick_message = ''

    def get_possible_actions(self) -> List[Action]:
        if self.app_state == AppState.menu:
            return [MenuAction(key=menu_item.key_to_select, menu=menu_item) for menu_item in self.current_menu.menu_items]
        elif self.app_state == AppState.game:
            if self.game_state == GameState.finalScreen:
                def get_final_message() -> str:
                    if self.left_points >= self.count_of_points_to_win:
                        return 'Left won'
                    elif self.right_points >= self.count_of_points_to_win:
                        return 'Right won'
                return [FinalGameAction(key=final_actions_key_to_select[fa], final_action=fa, message=get_final_message())
                        for fa in (FinalAction.next_screen,)]
            return [
                GameAction(key=turn_actions_key_to_select[ta], turn_action=ta) for ta in
                (TurnAction.rock, TurnAction.paper, TurnAction.scissors)
            ]

    def action(self, action: Action):
        if self.app_state == AppState.menu:
            action: MenuAction = action
            if action.menu.title == 'Play':
                # Init game
                self.left_player = HumanPlayer()
                self.right_player = RandomAIPlayer()
                self.app_state = AppState.game
                # Start game
                pass
            if action.menu.title == 'Exit':
                self.app_state = AppState.exit
        elif self.app_state == AppState.game:
            if self.game_state in (GameState.leftTurn, GameState.rightTurn):
                action: GameAction = action
                self._turn(action=action)
            elif self.game_state == GameState.finalScreen:
                action: FinalGameAction = action
                if action.final_action == FinalAction.next_screen:
                    self.left_points = self.right_points = 0
                    self.app_state = AppState.menu
                    self.game_state = GameState.leftTurn
                    self.__init_menu()
        self.notify()

    def _turn(self, action: GameAction):
        a = action.turn_action
        if self.game_state == GameState.leftTurn:
            self.left_action = a
            self.game_state = GameState.rightTurn
        elif self.game_state == GameState.rightTurn:
            self.right_action = a
            self.game_state = GameState.leftTurn
        if self.left_action and self.right_action:
            if (self.left_action == TurnAction.rock and self.right_action == TurnAction.scissors or
                    self.left_action == TurnAction.scissors and self.right_action == TurnAction.paper or
                    self.left_action == TurnAction.paper and self.right_action == TurnAction.rock):
                self.left_points += 1
                self.quick_message = f'{self.left_action} x {self.right_action} -> left won ({self.left_points}:{self.right_points})'
            elif self.left_action == self.right_action:
                self.quick_message = f'{self.left_action} x {self.right_action} -> draw ({self.left_points}:{self.right_points})'
            else:
                self.right_points += 1
                self.quick_message = f'{self.left_action} x {self.right_action} -> right won ({self.left_points}:{self.right_points})'

            self.left_action = self.right_action = None
            self.game_state = GameState.leftTurn
            if self.left_points >= self.count_of_points_to_win or self.right_points >= self.count_of_points_to_win:
                self.game_state = GameState.finalScreen
