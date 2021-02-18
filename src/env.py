from src.Card import Card 
# import Card
import copy

class BlackjackEnv():
    def __init__(self):
        self.player_score = self.draw(first=True)
        self.dealer_score = self.draw(first=True)

    def draw(self, first=False):
        '''
        Draws a card from the card and returns the amount to add to the score.
        If the card is red (-1), the value is subtracted. If the card is black (1) the value is added.

        Args:
        - first (bool): flag to specify if this is the first card drawn (if so, it has to be a black (positive) card)
        Returns:
        - value (int): total value to add to score
        '''
        card = Card()
        value = card.color * card.number

        # If this is the first card and the color is red (negative), then make it black (positive)
        if first == True and card.color == -1:
            value = abs(value)

        return value


    def step(self, state, action):
        '''     
        Given a state and action, returns the reward for that action along with a sample of the next state

        Args:
        - state (list): state in the form [dealer card, player sum]
        - action (int): action to take (either  0 (stick): don't draw a card, or 1 (hit): draw a card)
        Returns:
        - next_state: sample of the next state of the environment after the current action is taken
        - reward: value gained from performing action in the environment
        '''
        reward = 0
        dealer_sum = state[0]

        # Perform action
        next_state = copy.deepcopy(state)
        if action == 0: # hit
            next_state[1] = state[1] + self.draw()
        elif action == 1: # stick
            while 0 <= dealer_sum < 17:
                dealer_sum += self.draw()

        # Calculate reward
        sums = [next_state[1], dealer_sum]
        if min(sums) < 0 or max(sums) >= 21 or action == 1: # terminal states - bust or stick
            if next_state[1] == dealer_sum: # tie
                reward = 0
            elif next_state[1] in range(0,22) and dealer_sum in range(0,22): # both non-bust
                if next_state[1] > dealer_sum: # agent > dealer
                    reward = 1
                else: # dealer > agent
                    reward = -1
            else: # one bust
                if next_state[1] in range(0,22) and dealer_sum not in range(0,22):
                    reward = 1
                elif dealer_sum in range(0,22) and next_state[1] not in range(0,22):
                    reward = -1
                else:
                    raise ValueError('Aw we fucked up')
        else: # still in game
            reward = 0

        return next_state, reward