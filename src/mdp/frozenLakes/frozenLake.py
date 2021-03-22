class FrozenLake:

    def __init__(self, discount_rate, learning_rate, episodes, time_steps, gym):
        self.disount_rate = discount_rate
        self. learning_rate = learning_rate
        self.episodes = episodes
        self.time_steps = time_steps
        self.gym = gym