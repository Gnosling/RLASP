import copy
from mdp import BlocksWorldBuilder, VacuumCleanerWorldBuilder, SokobanBuilder
from src.mdp.frozenlake import FrozenLakeBuilder
from control import *
from policy import *
# import pandas as pd
# from matplotlib import pyplot as plt
# from tqdm import tqdm

import argparse
import os, sys, inspect
# marks the working directory as path for further imports
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import csv
import gym

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Train a RLASP agent in a given MDP.')

    parser.add_argument('--no_progress_bar', help='Don\'t show progress in stdout',
                        dest='show_progress_bar', action='store_false')
    parser.set_defaults(show_progress_bar=True)

    parser.add_argument('--db_file', help='Location to store the generated data. If `None`, no file will be generated.',
                        metavar='db_file.csv', default='out.csv')
    # parser.add_argument('--plt_file', help='Location to store the generated plot. if `None`, no file will be generated.', metavar='plt_file.pdf')

    parser.add_argument('--episodes', help='The number of episodes to train for.', type=int, default=100)
    parser.add_argument('--max_episode_length', help='The maximum number of steps within an episode.', type=int,
                        default=100)

    # Behavior policies
    parser.add_argument('--epsilon',
                        help='The "epsilon" parameter for the epsilon-greedy behavior policy. Does nothing for other behavior policies.',
                        type=float, default=0.3)
    parser.add_argument('--planning_horizon', help='The number of steps into the future considered by the planner',
                        type=int, default=4)

    parser.add_argument('--no_planning', help='Don\'t show progress in stdout',
                        dest='plan_for_new_states', action='store_false')
    parser.set_defaults(plan_for_new_states=True)

    # Control algorithms
    parser.add_argument('--control_algorithm', help='The control algorithm to be used for training',
                        default='q_learning',
                        choices={'monte_carlo', 'q_learning', 'q_learning_reversed_update'})

    parser.add_argument('--learning_rate',
                        help='The learning rate (also step-size parameter or alpha) considered by some control algorithms.',
                        type=float, default=0.3)

    # MDP's
    subparsers = parser.add_subparsers(help='The markov decision procedure which should be learned.',
                                       title='Markov decision procedure')

    parser_blocksworld = subparsers.add_parser('blocksworld', help='The classic blocksworld.')
    parser_blocksworld.add_argument('--blocks_world_size', help='The number of blocks in the blocks world.', type=int,
                                    default=5)
    parser_blocksworld.set_defaults(mdp='blocksworld', behavior_policy='planning_exploring_starts')

    parser_sokoban = subparsers.add_parser('sokoban', help='The sokoban game.')
    parser_sokoban.add_argument('--sokoban_level_name', help='The sokoban level name.', default='suitcase-05-01')
    parser_sokoban.set_defaults(mdp='sokoban', behavior_policy='planning_epsilon_greedy')

    parser_frozenLake = subparsers.add_parser('frozen_lake', help='OpenAi gym\'s frozenLake-environment.')
    parser_frozenLake.add_argument('--frozen_lake_level', help='4x4_A, 4x4_B or 8x8',
                                   default='4x4_A',
                                   choices={'4x4_A','4x4_B', '5x5_A', '8x8'})
    parser_frozenLake.add_argument('--is_slippery', help='defines whether the agent may slip',
                                   default='True',
                                   choices={'True', 'False'})
    parser_frozenLake.add_argument('--is_cautious', help='defines whether the agent tries to keep distance to holes or not',
                                   default='False',
                                   choices={'True', 'False'})
    parser_frozenLake.add_argument('--gym_environment_active', help='True or False',
                                   default='True',
                                   choices={'True', 'False'})
    parser_frozenLake.set_defaults(mdp='frozenLake', behavior_policy='planning_epsilon_greedy')

    args = parser.parse_args()

    initial_value_estimate = -1

    gym_active = False
    is_slippery = False
    frozen_lake_active = False
    frozen_lake_level = ""
    gym_env = ""
    if args.mdp == 'blocksworld':
        mdp_builder = BlocksWorldBuilder(args.blocks_world_size)
    elif args.mdp == 'sokoban':
        mdp_builder = SokobanBuilder(args.sokoban_level_name)
    elif args.mdp == 'frozenLake':
        mdp_builder = FrozenLakeBuilder(args.frozen_lake_level, args.is_cautious == 'True')
        frozen_lake_active = True
        if args.gym_environment_active == 'True':
            gym_active = True
            initial_value_estimate = 0
        else:
            gym_active = False
        if args.is_slippery == 'True':
            is_slippery = True
        else:
            is_slippery = False
        gym_env = 'FrozenLake-v0'
        frozen_lake_level = args.frozen_lake_level

    if args.behavior_policy == 'planning_exploring_starts':
        behavior_policy = PlanningExploringStartsPolicy(PlannerPolicy(args.planning_horizon, mdp_builder),
                                                        RandomPolicy(),
                                                        QTablePolicy(initial_value_estimate),
                                                        planning_factor=0,
                                                        plan_for_new_states=args.plan_for_new_states)

    elif args.behavior_policy == 'planning_epsilon_greedy':

        behavior_policy = PlanningEpsilonGreedyPolicy(PlannerPolicy(args.planning_horizon, mdp_builder),
                                                      RandomPolicy(),
                                                      QTablePolicy(initial_value_estimate),
                                                      args.epsilon,
                                                      args.plan_for_new_states)

    target_policy = QTablePolicy(initial_value_estimate)

    if args.control_algorithm == 'monte_carlo':
        control = FirstVisitMonteCarloControl(behavior_policy)

    elif args.control_algorithm == 'q_learning':
        control = QLearningControl(target_policy, behavior_policy, args.learning_rate)

    elif args.control_algorithm == 'q_learning_reversed_update':
        control = QLearningReversedUpdateControl(target_policy, behavior_policy, args.learning_rate)

    # df = pd.DataFrame()
    df = list()

    episode_ids = range(args.episodes)
    #    if args.show_progress_bar:
    #        episode_ids = tqdm(episode_ids, total=args.episodes)

    for episode_id in episode_ids:

        if args.show_progress_bar:
            print(f'\x1b[2K\rTraining:{episode_id * 100 / (args.episodes - 1):3.0f}%', end='')

        mdp = mdp_builder.build_mdp()
        if not gym_active:
            control.try_initialize_state(mdp.state, mdp.available_actions)
        else:
            # work around for frozen lake
            control.try_initialize_state(mdp.state, mdp.all_actions)
        # print()
        # print(f'Beginning episode {episode_id}')
        # print('Start state = ', mdp.state)
        # print(f'Estimated value for start state = {target_policy.optimal_value_for(mdp.state):4.2f}')

        # First, test the target policy and see how it would perform
        mdp_target = copy.deepcopy(mdp)

        if gym_active & frozen_lake_active:
            env1 = gym.make(gym_env)
            mdp.set_env(env1)
            mdp.env.set_level(frozen_lake_level, is_slippery)
            mdp.env.reset()
            env2 = gym.make(gym_env)
            mdp_target.set_env(env2)
            mdp_target.env.set_level(frozen_lake_level, is_slippery)
            mdp_target.env.reset()

        control.generate_episode_with_target_policy(mdp_target, gym_active, step_limit=args.max_episode_length)

        # Second, train the target policy and the behavior policy on the mdp
        # print('Updating states backwards...')
        control.learn_episode(mdp, gym_active, step_limit=args.max_episode_length)

        # Finally, store all results in the dataframe
        row = {

            **{f'arg_{k}': v for k, v in vars(args).items()},

            'episode_id': episode_id,
            'behavior_policy_return': mdp.return_history[0],
            'target_policy_return': mdp_target.return_history[0],
        }

        # df = df.append(pd.Series(row, name=episode_id))
        df.append(row)

        # print(f'Achieved return = {mdp.return_history[0]}')

    print()

    if True:
        # df.to_csv(args.db_file)
        csv_headers = set()
        for row in df:
            csv_headers |= row.keys()

        with open(args.db_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=list(csv_headers))
            writer.writeheader()
            writer.writerows(df)
