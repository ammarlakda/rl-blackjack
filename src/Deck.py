import Card

class Deck():
    def __init__(self):
        self.first_card_dealer = self.draw_black_card()
        self.first_card_player = self.draw_black_card()

    def draw_card(self):
        '''
        Draws a card from the deck at random and returns the card
        '''
        return Card.Card()

    def draw_black_card(self):
        '''
        Draws a card from the deck at random and turns into black card, as per instructions
        '''
        first_card = Card.Card()
        first_card.color = 'black'
        return first_card