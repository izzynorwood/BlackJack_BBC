import random
from PIL import Image, ImageTk

# standard deck
class CardDeck:
    def __init__(self, num_decks, card_width=96,card_height=135):
        suits = ['h', 'd', 'c', 's']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k', 'ace']
        self.deck = []
        image_back = Image.open("resources/card_back.png")  
        resized_image_back = image_back.resize((card_width, card_height), resample=0)  
        self.photo_image_back = ImageTk.PhotoImage(resized_image_back)  
        
        for suit in suits:
            for rank in ranks:
                image_path = f"resources/{suit}_{rank}.png"
                image = Image.open(image_path)  
                resized_image = image.resize((card_width, card_height), resample=0)  
                photo_image = ImageTk.PhotoImage(resized_image)  
                self.deck.append({'rank': rank, 'suit': suit, 'image': photo_image})
        
        self.deck = self.deck * num_decks
        random.shuffle(self.deck)
    
    # first card is removed from the deck
    def draw_card(self):
        if self.deck:
            return self.deck.pop(0)

    # player recieves a new hand
    def new_hand(self):
        return [self.draw_card(), self.draw_card()]
    
    # the total amount of cards in the deck is returned
    def total_cards(self):
        return len(self.deck) 

# extended deck card   
class ExtendedDeck:
    def __init__(self, card_width=115,card_height=162):
        self.card_width = card_width
        self.card_height = card_height
        self.deck = [{'card_type': 'double_dealer_face_up', 'image': self.load_image("resources/e_ddfu.png")},
                     {'card_type': 'change_goal_by_05', 'image': self.load_image("resources/e_cgb05.png")},
                     {'card_type': 'change_goal_by_15', 'image': self.load_image("resources/e_cgb15.png")},
                     {'card_type': 'change_goal_by_2', 'image': self.load_image("resources/e_cgb2.png")},
                     {'card_type': 'multiply_pot_by_2', 'image': self.load_image("resources/e_mpb2.png")},
                     {'card_type': 'multiply_pot_by_5', 'image': self.load_image("resources/e_mpb5.png")},
                     {'card_type': 'multiply_pot_by_10', 'image': self.load_image("resources/e_mpb10.png")},
                     {'card_type': 'new_hand', 'image': self.load_image("resources/e_nh.png")},
                     {'card_type': 'new_hand', 'image': self.load_image("resources/e_nh.png")},
                     {'card_type': 'new_hand', 'image': self.load_image("resources/e_nh.png")}] 
        self.deck_len = len(self.deck)
        self.card_back = self.load_image("resources/card_back.png")
        random.shuffle(self.deck)
    
    # random card is drawn from the deck
    def draw_card(self):
        if self.deck:
            r_ind = random.randint(0,self.deck_len)-1
            return self.deck[r_ind]
    
    # image is loaded from path   
    def load_image(self,path):
        open_image = Image.open(path)  
        resized_image = open_image.resize((self.card_width, self.card_height), resample=0)  
        image = ImageTk.PhotoImage(resized_image)
        return image
