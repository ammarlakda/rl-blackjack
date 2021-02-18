from env import BlackjackEnv
import numpy as np
from tqdm import tqdm

class Agent():
    def __init__(self):
        self.env = BlackjackEnv()

    def make_trajectory(self, env, policy):
        '''
        Given an environment and a policy to follow, simulates remained of states and returns trajectory

        Args:
        - env (env.BlackJackEnv): environment to act in
        - policy (np.ndarray): policy to follow
        Returns:
        - trajectory (list): (state, action) pairs for each step of the episode
        - rewards (list): rewards for each time step
        '''
        state = [env.dealer_score, env.player_score]
        trajectory = []
        rewards = []

        # Do all player moves
        while 0 <= state[1] < 21:
            # If equiprobable, pick at random, else pick greedily
            policy_s = policy[state[0], state[1]]
            if policy_s[0] == policy_s[1]:
                action = 0 if np.random.rand() < 0.5 else 1
            else:
                action = np.argmax(policy_s)
            state_prime, reward = env.step(state, action)

            if state[1] <= 21:
                trajectory.append((state, action))
                rewards.append(reward)

            if action == 1: # If we stuck, the state is now terminal
                break

            state=state_prime

        return trajectory, rewards

    def mc(self, epoch):
        '''
        Solves out blackjack game using On-policy first-vist Monte Carlo Control

        Args:
        - epoch (int): number of cycles to run algorithm
        Returns:
        - Q (np.ndarray): action value function
        - V_star (np.ndarray): optimal state value function
        '''
        # Set array size as [11,22,2] to account for indexing the 10 dealer cards, 21 max player sum, and two actions
        N0 = 10
        N = np.zeros([11, 22, 2])
        V_star = np.zeros([11,22])
        
        policy = np.full([11, 22, 2], 0.5) # epsilon soft (equiprobable) policy 
        Q = np.zeros([11, 22, 2])

        for _ in tqdm(range(epoch)):
            env = BlackjackEnv()
            
            # Generate an episode following policy
            trajectory, rewards = self.make_trajectory(env, policy)
            G = 0
            for t in range(len(trajectory)-1, -1, -1):
                s, a = trajectory[t]
                r = rewards[t]
                G += r

                # Update update parameters
                N[s[0], s[1], a] += 1
                epsilon = N0/(N0 + np.min(N[s[0], s[1]]))
                alpha = 1/N[s[0], s[1], a]
                if (s, a) not in trajectory[:t]:
                    Q[s[0], s[1], a] += alpha*(G - Q[s[0], s[1], a])
                    A_star = np.argmax(Q[s[0], s[1]])
                    for a in [0, 1]:
                        policy[s[0], s[1], a] = (1-epsilon + (epsilon)/2) if a == A_star else epsilon/2

        for i in range(11):
            for j in range(22):
                V_star[i, j] = np.max(Q[i, j])

        return Q, V_star

    def sarsa(self):
        pass