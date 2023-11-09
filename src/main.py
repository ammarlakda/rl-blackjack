from env import BlackjackEnv
import utils
import agent
import numpy as np

def check_Q(Q):
    '''
    Prints Q vals from Monte Carlo to test file

    Args:
    - Q (np.ndarray): 3D array to print
    '''
    shape = Q.shape
    assert len(shape) == 3, "Incorrect Q shape"
    with open('checkQ.txt', 'w') as file:
        file.write('Code formatted as (Dealer Card, Player Sum, Action): value \n')
        for s0 in range(shape[0]):
            for s1 in range(shape[1]):
                for a in range(shape[2]):
                    file.write('({}, {}, {}): {} \n'.format(s0 + 1, s1, a, Q[s0, s1, a]))

if __name__ == '__main__':
    mc_epoch = 1000000
    td_epoch = mc_epoch
    agent = agent.Agent()

    print('Testing Monte-Carlo Control')
    Q_mc, V_prime, policy = agent.mc(mc_epoch)
    print('Testing Sarsa(0)')
    Q_td, mses = agent.sarsa(td_epoch, Q_mc)

    # Print 3D value function graph
    utils.grapher3d(V_prime[1:,:].T, title='MC V_Prime ({} epochs)'.format(mc_epoch), save_file='3Dplot.png')

    # Print Sarsa(0) learning curve graph
    utils.grapher(mses, x_label='Iteration', y_label='MSE', save_file='mse.png')

    # Output checkQ file
    print(Q_mc)
    check_Q(Q_mc[1:,:,:])