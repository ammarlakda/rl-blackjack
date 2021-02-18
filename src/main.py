from env import BlackjackEnv
import agent

if __name__ == '__main__':
    mc_epoch = 1000000
    agent = agent.Agent()

    Q_mc, V_prime = agent.mc(mc_epoch)