from typing import Dict, Tuple, Set
import random

from entities import State, Action

class SimpleMonteCarloControl:

    def __init__(self, markov_decision_procedure, initial_value_estimate=0, update_every_visit=False):

        self.markov_decision_procedure = markov_decision_procedure
        self.initial_value_estimate = initial_value_estimate
        self.update_every_visit = update_every_visit

        self.visits: Dict[State, Dict[Action, int]] = dict()
        self.action_value_estimates: Dict[State, Dict[Action, int]] = dict()
        self.current_best_actions: Dict[State, Action] = dict()
        self.available_actions: Dict[State, Set[Action]] = dict()

    def initialize_unexplored_state(self, state: State):

        self.visits[state] = dict()
        self.action_value_estimates[state] = dict()

        for action in self.markov_decision_procedure.available_actions_for_state(state):
            self.visits[state][action] = 0
            self.action_value_estimates[state][action] = self.initial_value_estimate

    def suggest_action_for_state(self, state: State) -> Action:
        return self.current_best_actions.get(state, None) 

    def iterate_policy_with_episode(self, states, actions, experienced_returns):

        visited_state_action_pairs = set()

        for state, action, experienced_return in zip(states, actions, experienced_returns):

            is_first_visit = (state, action) not in visited_state_action_pairs

            if is_first_visit or self.update_every_visit:

                self.evaluate_policy(state, action, experienced_return) 
                self.improve_policy(state, action)

                visited_state_action_pairs.add((state, action))

    def evaluate_policy(self, state: State, action: Action, experienced_return: float):

        if state not in self.action_value_estimates:
            self.initialize_unexplored_state(state)

        self.visits[state][action] += 1

        q = self.action_value_estimates[state][action]
        v = float(self.visits[state][action])
        self.action_value_estimates[state][action] += (experienced_return - q) / v 

    def improve_policy(self, state: State, action: Action):

        available_estimates = self.action_value_estimates[state].items()

        current_maximal_estimate = max(v for _,v in available_estimates) 

        current_optimal_actions = [a for (a, v) in available_estimates if v==current_maximal_estimate]

        self.current_best_actions[state] = random.choice(current_optimal_actions)

class SgdMonteCarloControl:

    def __init__(self, markov_decision_procedure, step_size_parameter, initial_value_estimate=0) :

        self.markov_decision_procedure = markov_decision_procedure
        self.initial_value_estimate = initial_value_estimate
        self.step_size_parameter = step_size_parameter

        self.action_value_estimates: Dict[State, Dict[Action, int]] = dict()
        self.current_best_actions: Dict[State, Action] = dict()
        self.available_actions: Dict[State, Set[Action]] = dict()

    def initialize_unexplored_state(self, state: State):

        self.action_value_estimates[state] = dict()

        for action in self.markov_decision_procedure.available_actions_for_state(state):
            self.action_value_estimates[state][action] = self.initial_value_estimate

    def suggest_action_for_state(self, state: State) -> Action:
        return self.current_best_actions.get(state, None) 

    def iterate_policy_with_episode(self, states, actions, experienced_returns):

        for state, action, experienced_return in zip(states, actions, experienced_returns):

            self.evaluate_policy(state, action, experienced_return) 
            self.improve_policy(state, action)

    def evaluate_policy(self, state: State, action: Action, experienced_return: float):

        if state not in self.action_value_estimates:
            self.initialize_unexplored_state(state)

        q = self.action_value_estimates[state][action]
        self.action_value_estimates[state][action] += self.step_size_parameter * (experienced_return - q) * 1 
        #TODO: Double-check if gradient is 1!

    def improve_policy(self, state: State, action: Action):

        available_estimates = self.action_value_estimates[state].items()

        current_maximal_estimate = max(v for _,v in available_estimates) 

        current_optimal_actions = [a for (a, v) in available_estimates if v==current_maximal_estimate]

        self.current_best_actions[state] = random.choice(current_optimal_actions)
