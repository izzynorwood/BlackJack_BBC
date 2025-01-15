import random
face_cards = ['j','q','k']

class Player:
    def __init__(self, name, bank):
        self.name = name
        self.hand = []
        self.bank = bank
        self.bet = 0
        self.wins = 0
        self.ace_value = 1
        self.has_ace = False
    
    # returns the total value of the player's hand
    def total(self):
        total = 0
        for each in self.hand:
            if each['rank'] in face_cards:
                total += 11
            elif each['rank'] == 'ace':
                total += self.ace_value
                self.has_ace = True
            else:
                total += int(each['rank'])
        return total
    
    # returns if value of the player's hand has exceeded the goal
    def is_bust(self, goal):
        return self.total() > goal
    
    # opponent places a bet that is between 0 and half the amount of money in their bank
    def opp_place_bet(self):
        if self.bank > 1:
            self.bet = random.randint(0, int(self.bank/2))
        if self.bank == 1:
            self.bet = random.randint(0, 1)
    
    def change_ace_value(self):
        if self.ace_value == 1:
            self.ace_value = 11
        else:
            self.ace_value = 1
