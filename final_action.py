from enum import Enum


class FinalAction(str, Enum):
    next_screen = 'next_screen'


final_actions_key_to_select = {
    FinalAction.next_screen: 'n'
}
