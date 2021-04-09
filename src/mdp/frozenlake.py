import os
import clingo
import random
from typing import Set, List

from .markov_decision_procedure import MarkovDecisionProcedure
from .frozen_lake_levels.frozen_lake_level_builder import FrozenLakeLevelBuilder


class FrozenLake(MarkovDecisionProcedure):
    def __init__(self, state_initial: Set[str], state_static: Set[str]):
        # No discounting in any blocks world
        # TODO: Discount ändern? --> denke nicht
        discount_rate = 1.0

        super().__init__(state_initial, state_static, discount_rate, 'frozenlake.lp')

    @staticmethod
    def translate_action_to_env(action: str):
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
    def translate_action_from_env(action: int):
        if action == 0:
            return 'move(left)'
        elif action == 1:
            return 'move(down)'
        elif action == 2:
            return 'move(right)'
        elif action == 3:
            return 'move(up)'
        else:
            return ""

    @staticmethod
    def translate_current_state_to_env(state: frozenset):
        helper, = state
        return helper[16:-1]

    @staticmethod
    def translate_current_state_from_env(state: int):
        return frozenset({'currentPosition(' + str(state) + ')'})

    def transition_with_gym_env(self, action: str):
        translated_action = self.translate_action_to_env(action)
        next_state, next_reward, done, info = self.env.step(translated_action)
        next_state = self.translate_current_state_from_env(next_state)

        # due to side-effects, the normal transition will also be performed, however its return values are ignored
        self.transition(action)
        return next_state, next_reward


class FrozenLakeBuilder:
    def __init__(self, level: str):
        self.level = FrozenLakeLevelBuilder.build_level(level)
        sample_mdp = self.build_mdp()

        self.mdp_interface_file_path = sample_mdp.interface_file_path
        self.mdp_problem_file_path = sample_mdp.problem_file_path
        self.mdp_state_static = sample_mdp.state_static

    def build_mdp(self):
        return FrozenLake(state_initial=self.level.start, state_static=self.level.states)
