from . import OffPolicyControl

class QLearningControl(OffPolicyControl):

    def __init__(self, target_policy, behavior_policy, alpha):
        super().__init__(target_policy, behavior_policy)
        self.alpha = alpha

    def policy_update_after_step(self, current_state, current_action, next_state, next_reward,
                                 mdp):

            prediction = self.target_policy.value_for(current_state, current_action)
            target = next_reward + mdp.discount_rate * (self.target_policy.optimal_value_for(next_state)) - prediction
            delta = self.alpha * target
            self.update(current_state, current_action, delta)

    def policy_update_after_step_with_gym(self, current_state, current_action, next_state, next_reward, discount_rate):
        prediction = self.target_policy.value_for(current_state, current_action)
        target = next_reward + discount_rate * (self.target_policy.optimal_value_for(next_state)) - prediction
        delta = self.alpha * target
        self.update(current_state, current_action, delta)

    def policy_update_after_episode(self, mdp):
        # Learning happens each step. Nothing to do at the end of the episode!
        return 


class QLearningReversedUpdateControl(OffPolicyControl):

    def __init__(self, target_policy, behavior_policy, alpha):
        super().__init__(target_policy, behavior_policy)
        self.alpha = alpha
        self.replay_memory = list()

    def policy_update_after_step(self, current_state, current_action, next_state, next_reward,
                                 mdp):

        self.replay_memory.append((current_state, current_action, next_state, next_reward))

    def policy_update_after_episode(self, mdp):

        for current_state, current_action, next_state, next_reward in reversed(self.replay_memory): 

            prediction = self.target_policy.value_for(current_state, current_action)
            target = next_reward + mdp.discount_rate * (self.target_policy.optimal_value_for(next_state)) - prediction
            delta = self.alpha * target
            self.update(current_state, current_action, delta)

            #print(self.target_policy._q_table[current_state].values())
            #print(f' -> R[T+1] = {next_reward: 6.2f}, Q(S,A) = {prediction: 6.2f}, maxQ(S\',a) = {self.target_policy.optimal_value_for(next_state)}, R + gamma*maxQ(S\',a) - Q(S,A) = {target: 6.2f}, alpha * (R + ...) = {delta: 6.2f}')
            #print()

        self.replay_memory.clear()


