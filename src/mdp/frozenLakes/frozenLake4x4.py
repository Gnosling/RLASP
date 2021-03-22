from src.control.q_learning import QLearningControl
from src.policy.q_table_policy import QTablePolicy

"""
External environment given by openAi's gym.
The states are ordered numbers first row-wise, than column-wise, eg:
        0  1  2  3
        4  5  6  7
        8  9  10 11
        12 13 14 15
There are 4 different actions to take:
        # 3 = up
        # 2 = right
        # 1 = down
        # 0 = left
It uses the "frozenlake-v0"-environment:
    Winter is here. You and your friends were tossing around a frisbee at the
    park when you made a wild throw that left the frisbee out in the middle of
    the lake. The water is mostly frozen, but there are a few holes where the
    ice has melted. If you step into one of those holes, you'll fall into the
    freezing water. At this time, there's an international frisbee shortage, so
    it's absolutely imperative that you navigate across the lake and retrieve
    the disc. However, the ice is slippery, so you won't always move in the
    direction you intend.
    The surface is described using a grid like the following

        SFFF
        FHFH
        FFFH
        HFFG

    S : starting point, safe
    F : frozen surface, safe
    H : hole, fall to your doom
    G : goal, where the frisbee is located

    The episode ends when you reach the goal or fall in a hole.
    You receive a reward of 1 if you reach the goal, and zero otherwise.
"""

from .frozenLake import FrozenLake
import clingo


class FrozenLake4x4(FrozenLake):

    def __init__(self, discount_rate, learning_rate, episodes, time_steps, gym):
        super().__init__(discount_rate, learning_rate, episodes, time_steps, gym)
        self.planned_action = set()

    def set_action(self, m: clingo.Model):
        self.planned_action = set()
        for symbol in m.symbols(shown=True):
            sym = str(symbol)
            if sym.startswith("up"):
                self.planned_action.add(3)
            elif sym.startswith("right"):
                self.planned_action.add(2)
            elif sym.startswith("down"):
                self.planned_action.add(1)
            elif sym.startswith("left"):
                self.planned_action.add(0)

    def planning_for_state(self, current_state: int):
        ctl = clingo.Control()
        ctl.load("./src/mdp/frozenLakes/frozenLake4x4.lp")
        state = current_state
        ctl.add('base', [], "currentState(" + str(state) + ").")
        ctl.ground([("base", [])])
        ctl.solve(on_model=self.set_action)

    def run_environment(self):
        env = self.gym.make('FrozenLake-v0')
        qTable = QLearningControl(QTablePolicy(0.0), QTablePolicy(0.0), self.learning_rate)
        for i in range(16):
            qTable.try_initialize_state(i, {0, 1, 2, 3})

        for i_episode in range(self.episodes):
            print("__________________________")
            state = env.reset()

            for t in range(self.time_steps):
                # env.render()

                # action = env.action_space.sample()
                # 3 = up
                # 2 = right
                # 1 = down
                # 0 = left
                action = qTable.suggest_action_for_state(state)
                self.planning_for_state(state)
                planned_action = self.planned_action
                new_state, reward, done, info = env.step(action)
                qTable.policy_update_after_step_with_gym(state, float(action), new_state, reward, self.disount_rate)  # so?
                state = new_state

                # if i_episode == 99:
                #    env.render()

                if done:
                    # env.render()
                    msg = "successful"
                    if new_state==5 or new_state==7 or new_state==11 or new_state==12:
                        msg = "unsuccessful"
                    print("Episode finished after {} timesteps --> {}".format(t + 1, msg))
                    break
        env.close()