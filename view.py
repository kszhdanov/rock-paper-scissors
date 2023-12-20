from model import Model, AppState, GameState
from observer import Observer


debug = False

class View(Observer):
    def __init__(self, model: Model):
        self.model = model
        model.subscribe(self)

    def notify(self):
        def current_player_is_human() -> bool:
            return (self.model.game_state == GameState.leftTurn and self.model.left_player.is_human or
                    self.model.game_state == GameState.rightTurn and self.model.right_player.is_human)
        lines = []

        if debug:
            lines.append(f'app: {self.model.app_state} | game: {self.model.game_state}')

        if self.model.quick_message:
            lines.append(f'[{self.model.quick_message}]')

        if self.model.app_state == AppState.menu:
            lines.append('-> menu <-')
            menu_actions = self.model.get_possible_actions()
            for m_a in menu_actions:
                lines.append(f'{m_a.key} - {m_a.menu.title} ({m_a.menu.tip})')
        elif self.model.app_state == AppState.game:
            if self.model.game_state in (GameState.leftTurn, GameState.rightTurn):
                lines.append(f'-> game ({"left" if self.model.game_state == GameState.leftTurn else "right"} player turn) <-')
                if current_player_is_human():
                    game_actions = self.model.get_possible_actions()
                    for g_a in game_actions:
                        lines.append(g_a.key)
                else:
                    lines.append('waiting...')
            elif self.model.game_state == GameState.finalScreen:
                final_game_actions = self.model.get_possible_actions()
                for f_g_a in final_game_actions:
                    lines.append(f'{f_g_a.key} | {f_g_a.message}')

        for line in lines:
            print(line)
        print('-----')
