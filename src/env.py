import Card

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
        card = Card.Card()
        value = card.color * card.number

        # If this is the first card and the color is red (negative), then make it black (positive)
        if first == True and card.color == -1:
            value = abs(value)

        return value


    def step(self, state, action, agent=True):
        '''     
        Given a state and action, returns the reward for that action along with a sample of the next state

        Args:
        - state (list): state in the form [dealer card, player sum]
        - action (int): action to take (either  0 (stick): don't draw a card, or 1 (hit): draw a card)
        - agent=True (bool): specifies if agent is the one taking action
        Returns:
        - next_state: sample of the next state of the environment after the current action is taken
        - reward: value gained from performing action in the environment
        '''
        reward = 0

        # Perform action
        if action == 1:
            if agent:
                next_state = state[1] + self.draw()
            else:
                next_state = state[0] + self.draw()

        # Calculate reward
        if state == next_state or any(next_state > 21) or any(next_state < 0): # terminal states
            if next_state[1] > next_state[0] and next_state[1] in range(0, 22): # win
                reward = 1
            elif next_state[0] == next_state[1]: # tie
                reward = 0
            else:
                reward = -1

        return state, reward
## Note: set prev state before calling step. if state_prev[1] == state[1], start 