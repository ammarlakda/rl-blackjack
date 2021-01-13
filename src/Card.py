import numpy as np

class Card():
    def __init__(self):
        self.number = self.initialize_number()
        self.color = self.initialize_color()

    def initialize_number(self):
        '''
        Returns a random number between 1-10 (uniformly distributed)
        '''
        return np.random.randint(low=1, high=11)

    def initialize_color(self):
        '''
        Returns the color of our card with p(red) = 1/3, p(black) = 2/3.
        '''
        return 'red' if np.random.rand() <= 0.333333333334 else 'black'