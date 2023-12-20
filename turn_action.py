from enum import Enum


class TurnAction(str, Enum):
    rock = 'rock'
    paper = 'paper'
    scissors = 'scissors'


turn_actions_key_to_select = {
    TurnAction.rock: 'r',
    TurnAction.paper: 'p',
    TurnAction.scissors: 's'
}
