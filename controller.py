from model import Model, AppState, GameState


class Controller:
    def __init__(self, model: Model):
        self.model = model

    def start_infinite_cycle(self):
        while self.model.app_state != AppState.exit:
            if self.model.app_state == AppState.menu:
                possible_actions = {action.key: action for action in self.model.get_possible_actions()}
                user_input = input()
                while user_input not in possible_actions:
                    user_input = input()
                self.model.action(possible_actions[user_input])
            elif self.model.app_state == AppState.game:
                if self.model.game_state == GameState.leftTurn:
                    self.model.action(self.model.left_player.get_action(self.model.get_possible_actions()))
                elif self.model.game_state == GameState.rightTurn:
                    self.model.action(self.model.right_player.get_action(self.model.get_possible_actions()))
                elif self.model.game_state == GameState.finalScreen:
                    possible_actions = {action.key: action for action in self.model.get_possible_actions()}
                    user_input = input()
                    while user_input not in possible_actions:
                        user_input = input()
                    self.model.action(possible_actions[user_input])
