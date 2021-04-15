import os
import clingo
import random

from typing import Set, List

class MarkovDecisionProcedure:

    @staticmethod
    def file_path(file_name):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)

    def __init__(self, state_initial: Set[str], state_static: Set[str], discount_rate: float,
                 problem_file_name: str):

        self.state: Set[str] = frozenset(state_initial)
        self.state_static: Set[str] = frozenset(state_static)
        self.discount_rate: float = discount_rate
        self.env = False

        # TODO: Needs to be separated from abstract MDP. -> Do it when introducing a second MDP
        self.interface_file_name: str = 'markov_decision_procedure.lp'
        self.problem_file_name: str = problem_file_name

        # MDP trajectory: S0, A0, R1, S1, A1, R2, S2, A2, ... 
        self.state_history: List[Set[str]] = [frozenset(state_initial)] # S0
        self.action_history: List[str] = [] #A0 will be given later once the first action is executed
        self.reward_history: List[float] = [None] # R0, which is undefined

        # self.available_actions = self._compute_available_actions
        self.available_actions = set()
        self._compute_available_actions

        self.action = ""

    @property
    def interface_file_path(self):
        return self.file_path(self.interface_file_name)

    @property
    def problem_file_path(self):
        return self.file_path(self.problem_file_name)

    def set_transition(self, model: clingo.Model):
        next_reward = None
        next_state = set()
        available_actions = set()

        for symbol in model.symbols(shown=True):

            if symbol.name == 'nextState':
                # ˙Atom is of the form `state(f(...))`
                # where`f(...)` is an uninterpreted function belonging to the state representation.
                f = symbol.arguments[0]
                next_state.add(str(f))

            if symbol.name == 'nextReward':
                # Atom is of the form `nextReward(r)`, and `r` is the reward.
                next_reward = symbol.arguments[0].number

            if symbol.name == 'nextExecutable':
                # Atom is of the form `nextExecutable(f(...))`
                # where`f(...)` is an uninterpreted function representing an executable action.
                available_actions.add(str(symbol.arguments[0]))

        self.state = frozenset(next_state)
        self.available_actions = available_actions

        # Update trajectory:
        self.action_history.append(self.action)  # A[t]
        self.state_history.append(frozenset(next_state))  # S[t+1]
        self.reward_history.append(next_reward)  # R[t+1]

    def transition(self, action: str):
        
        ctl = clingo.Control()

        ctl.load(self.file_path(self.interface_file_name))
        ctl.load(self.file_path(self.problem_file_name))
        ctl.add('base', [], ' '.join(f'currentState({s}).' for s in self.state))
        ctl.add('base', [], ' '.join(f'{s}.' for s in self.state_static))
        ctl.add('base', [], f'currentAction({action}).')
        ctl.add('base', [], '#show nextState/1. #show nextReward/1. #show nextExecutable/1.')

        ctl.ground(parts=[('base', [])])
        self.action = action
        ctl.solve(on_model=self.set_transition)

        return self.state, self.reward_history[-1]

    @property
    def return_history(self) -> List[float]:

        T = len(self.state_history)
        G = [0] * T

        for t in reversed(range(T-1)):
            G[t] = self.reward_history[t+1] + self.discount_rate * G[t+1]

        return G

    def set_available_actions(self, model: clingo.Model):
        available_actions = set()
        for symbol in model.symbols(shown=True):
            # We expect atoms of the form `currentExecutable(move(X, Y)`
            # but we are only interested in the first argument `move(X, Y)`
            available_actions.add(str(symbol.arguments[0]))

        self.available_actions = available_actions

    @property
    def _compute_available_actions(self) -> Set[str]:

        ctl = clingo.Control()

        ctl.load(self.file_path(self.interface_file_name))
        ctl.load(self.file_path(self.problem_file_name))
        ctl.add('base', [], ' '.join(f'currentState({s}).' for s in self.state))
        ctl.add('base', [], ' '.join(f'{s}.' for s in self.state_static))
        ctl.add('base', [], '#show currentExecutable/1.')

        ctl.ground(parts=[('base', [])])
        ctl.solve(on_model=self.set_available_actions)

        return self.available_actions

    def update_available_actions(self):
        ctl = clingo.Control()

        ctl.load(self.file_path(self.interface_file_name))
        ctl.load(self.file_path(self.problem_file_name))
        ctl.add('base', [], ' '.join(f'currentState({s}).' for s in self.state))
        ctl.add('base', [], ' '.join(f'{s}.' for s in self.state_static))
        ctl.add('base', [], '#show currentExecutable/1.')

        ctl.ground(parts=[('base', [])])
        ctl.solve(on_model=self.set_available_actions)

        return self.available_actions


    def set_env(self, env):
        self.env = env

    def set_env_level(self, level_name, is_slippery=False, is_random=False):
        self.env.set_level(level_name, is_slippery, is_random)

