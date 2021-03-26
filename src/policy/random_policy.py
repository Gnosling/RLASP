from typing import List, Dict, Set
import random

from src.mdp import MarkovDecisionProcedure

class RandomPolicy:

    def __init__(self):
        self._actions_for_state: Dict[Any, List[Any]] = dict()
   
    def suggest_action_for_state(self, state):
        choices = self._actions_for_state[state]
        if len(choices) > 0:
            return random.choice(choices)
        else:
            # ... in a terminal state
            return None

    def is_new_state(self, state) -> bool:
        return not state in self._actions_for_state

    def initialize_state(self, state, available_actions: Set):
        self._actions_for_state[state] = list(available_actions)

    def initialize_new_episode(self):
        # Nothing to prepare in this policy
        pass
