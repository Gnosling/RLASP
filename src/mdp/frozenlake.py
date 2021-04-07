import os
import clingo
import random
from typing import Set, List

from .markov_decision_procedure import MarkovDecisionProcedure


class FrozenLake(MarkovDecisionProcedure):
    def __init__(self, state_initial: Set[str], state_static: Set[str]):
        # No discounting in any blocks world
        # TODO: Discount ändern? --> denke nicht
        discount_rate = 1.0

        super().__init__(state_initial, state_static, discount_rate, 'frozenlake.lp')

    @staticmethod
    def translate_action(action: str):
        if action.count("left") == 1:
            return 0
        elif action.count("down") == 1:
            return 1
        elif action.count("right") == 1:
            return 2
        elif action.count("up") == 1:
            return 3
        else:
            return -1

    @staticmethod
    def translate_current_state(state: int):
        return frozenset({'currentPosition(' + str(state) + ')'})


class FrozenLakeBuilder:
    def __init__(self):
        sample_mdp = self.build_mdp()

        self.mdp_interface_file_path = sample_mdp.interface_file_path
        self.mdp_problem_file_path = sample_mdp.problem_file_path
        self.mdp_state_static = sample_mdp.state_static

    def build_mdp(self):
        # TODO: werte noch parametrisieren / aus level auslesen
        return FrozenLake(state_initial={"currentPosition(0)"}, state_static={"yolo(9)"})