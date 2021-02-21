from env import BlackjackEnv
import numpy as np
from tqdm import tqdm
from sklearn.metrics import mean_squared_error

class Agent():
    def __init__(self):
        self.env = BlackjackEnv()
    
    def make_trajectory(self, env, policy):
        trajectory = []
        rewards = []
        epsilon = 0.01
        
        state = [env.dealer_score, env.player_score]
        action = np.argmax(policy[state[0], state[1]])

        while state != [0,0]:
            state_prime, reward, _ = env.step(state, action)
            trajectory.append((state, action))
            rewards.append(reward)

            state = state_prime
            # Choose A from S using policy
            if np.random.rand() < 1 - epsilon:
                # Picky greedily and break ties arbitrarily
                vals = policy[state[0], state[1]]
                if vals[0] == vals[1]:
                    action = 0 if np.random.rand() < 0.5 else 1
                else:
                    action = np.argmax(policy[state[0], state[1]])
            else:
                action = np.random.randint(0,2)

        return trajectory, rewards

    def mc(self, epoch):
        '''
        Solves our modified blackjack game using On-policy first-vist Monte Carlo Control

        Args:
        - epoch (int): number of cycles to run algorithm
        Returns:
        - Q (np.ndarray): action value function
        - V_star (np.ndarray): optimal state value function
        - policy (np.ndarray): optimal policy for our value function
        '''
        # Set array size as [11,22,2] to account for indexing the 10 dealer cards, 21 max player sum, and two actions
        N0 = 10
        N = np.zeros([11, 22, 2])
        V_star = np.zeros([11,22])
        
        policy = np.full([11, 22, 2], 0.5) # epsilon soft (equiprobable) policy 
        Q = np.zeros([11, 22, 2])

        for _ in tqdm(range(epoch + 1)):
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
                        policy[s[0], s[1], a] = (1-epsilon + (epsilon/2)) if a == A_star else epsilon/2

        # Get optimal value function
        for i in range(11):
            for j in range(22):
                V_star[i, j] = np.max(Q[i, j])

        return Q, V_star, policy

    def sarsa(self, epoch, Q_star=None):
        '''
        Solves our modified blackjack game using SARSA(0)

        Args:
        - epoch (int): number of cycles to run algorithm
        - Q_star (np.ndarray): value function to use when computing MSE
        Returns:
        - Q (np.ndarray): action value function
        - mses (list): mean squared error values calculated every 10,000 cycles
        '''
        Q = np.zeros([11, 22, 2])
        N0 = 10
        N = np.zeros([11, 22, 2])
        mses = []

        # Loop for each episode
        for cycle in tqdm(range(epoch + 1)):
            terminal = False
            env = BlackjackEnv()
            # Initialize S
            s = [env.dealer_score, env.player_score]
            epsilon = N0/(N0 + np.min(N[s[0], s[1]]))

            # Choose A from S using policy derived from Q
            if np.random.rand() < 1 - epsilon:
                # Picky greedily and break ties arbitrarily
                vals = Q[s[0], s[1]]
                if vals[0] == vals[1]:
                    a = 0 if np.random.rand() < 0.5 else 1
                else:
                    a = np.argmax(Q[s[0], s[1]])
            else:
                a = np.random.randint(0,2)
            
            # Loop for each step of episode until S is terminal
            while s[1] in range(0,22) and terminal == False:
                # Update update parameters
                N[s[0], s[1], a] += 1
                epsilon = N0/(N0 + np.min(N[s[0], s[1]]))
                alpha = 1/N[s[0], s[1], a]

                # Take action A, observe R, S'
                s_prime, r, terminal = env.step(s, a)    
                # Choose A' from S' using policy derived from Q
                if np.random.rand() < 1 - epsilon and s_prime[1] in range(0,22):
                    # Picky greedily and break ties
                    vals = Q[s_prime[0], s_prime[1]]
                    if vals[0] == vals[1]:
                        a_prime = 0 if np.random.rand() < 0.5 else 1
                    else:
                        a_prime = np.argmax(Q[s_prime[0], s_prime[1]])
                elif s_prime[1] in range(0,22):
                    a_prime = np.random.randint(0,2)
                else:
                    break

                # Update Q(S, A)
                if s_prime[1] in range(0,22): # if next state isnt terminal (doesnt have Q)
                    Q[s[0], s[1], a] += alpha * (r + Q[s_prime[0], s_prime[1], a_prime] - Q[s[0], s[1], a])
                else: # next state is terminal
                    Q[s[0], s[1], a] += alpha * (r - Q[s[0], s[1], a])
                    terminal = True
                s = s_prime
                a = a_prime

            if Q_star is not None:
                if cycle % 10000 == 0:
                    shape = Q_star.shape
                    mses.append(np.mean([mean_squared_error(Q_star[s], Q[s]) for s in range(shape[0])]))

        return Q, mses