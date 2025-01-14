import tkinter as tk
from tkinter import *
from decks import CardDeck, ExtendedDeck
from styles import MyButton, MyLabel, MyMenuButton
from player import Player

FONT = "Arial Narrow"
BOARD = "#011627"
BLACK = "#01101c"
WHITE = "#E4DFDA"
face_cards = ['j','q','k']

# main menu of the game
class MainMenu:
    def __init__(self, root):
        self.root = root
        
        #main menu frame
        self.menu_frame = tk.Frame(self.root, bg=BOARD)
        self.menu_frame.place(relwidth=1, relheight=1)

        #title and option buttons
        tk.Label(self.menu_frame, text="BLACKJACK", font=(FONT, 24, 'bold'), bg=BOARD, fg='white').pack(pady=80)
        MyMenuButton(self.menu_frame, text="Single Player", command=self.single_player).pack()
        MyMenuButton(self.menu_frame, text="One Opponent", command=self.one_opponent).pack()
        MyMenuButton(self.menu_frame, text="Two Opponents", command=self.two_opponents).pack()
        MyMenuButton(self.menu_frame, text="Quit", command=self.root.quit).pack()
        MyLabel(self.menu_frame, text="Number of decks").pack()
        self.s = Scale(self.menu_frame, from_=1, to=20, orient=HORIZONTAL)
        self.s.pack()
    
    # starts single player game
    def single_player(self):
        deck_num = self.s.get()
        self.menu_frame.destroy() 
        BlackjackGame(self.root, deck_num, 0)
    
    # starts game with one opponent
    def one_opponent(self):
        deck_num = self.s.get()
        self.menu_frame.destroy()  
        BlackjackGame(self.root, deck_num, 1)
    
    #starts game with two opponents
    def two_opponents(self):
        deck_num = self.s.get()
        self.menu_frame.destroy()  
        BlackjackGame(self.root, deck_num, 2)  

# main game loop       
class BlackjackGame:
    def __init__(self, root, num_decks, num_opponents):
        self.root = root
        self.goal = 21
        self.num_opponents = num_opponents
        self.winnings = 0
        self.round = -1
        
        self.extended_deck = ExtendedDeck()
        self.deck = CardDeck(num_decks)
        self.ed_card = None
        
        self.player = Player('User', 10)
        self.dealer = Player('Dealer', 0) 
        self.opponent_1 = None
        self.opponent_2 = None 
        
        self.make_opponents(num_opponents)
        self.make_buttons(self.root)
        self.hit_button.config(state=tk.DISABLED)
        self.stay_button.config(state=tk.DISABLED)
        self.new_round_button.config(state=tk.DISABLED)
        self.new_round()
    
    # initilizes opponents    
    def make_opponents(self,num_opponents):
        if num_opponents == 1:   
            self.opponent_1 = Player('Opponent 1', 10)
        elif num_opponents == 2:
            self.opponent_1 = Player('Opponent 1', 10)
            self.opponent_2 = Player('Opponent 2', 10)
    
    # creates player input buttons    
    def make_buttons(self, my_root):
        self.player_buttons_frame = tk.Frame(my_root, bg=BOARD)
        self.player_buttons_frame.place(relx=0.5, rely=1, anchor='s', relwidth=1)
        
        self.hit_button = MyButton(self.player_buttons_frame, text="Hit", command=self.hit)
        self.hit_button.pack(side=tk.LEFT)
        
        self.stay_button = MyButton(self.player_buttons_frame, text="Stay", command=self.stay)
        self.stay_button.pack(side=tk.LEFT)
        
        self.new_round_button = MyButton(self.player_buttons_frame, text="New Round", command=self.new_round)
        self.new_round_button.pack(side=tk.LEFT)
        
        self.exit_to_menu_button = MyButton(self.player_buttons_frame, text="Exit to Menu", command=self.exit_to_menu)
        self.exit_to_menu_button.pack(side=tk.LEFT)

    # starts new round
    def new_round(self):
        self.round += 1
        self.new_round_button.config(state=tk.DISABLED)
        
        self.goal = 21
        self.winnings = 0
        
        if self.round != 0:
            self.destroy_game_frames() 
        
        # opponents place bets    
        if self.opponent_1:
            self.opponent_1.opp_place_bet()
            self.winnings += self.opponent_1.bet
            if self.opponent_2:
                self.opponent_2.opp_place_bet()
                self.winnings += self.opponent_2.bet
        
        self.place_bet()  

    # allows user to place bet
    def place_bet(self):
        self.betframe = Frame(self.root, bg=BLACK)
        self.betframe.place(relx=0.5, rely=0.5, anchor="center")
        MyLabel(self.betframe, text="Place bet:", justify='center').pack()
        self.bet_scale = Scale(self.betframe, from_=0, to=self.player.bank, orient=HORIZONTAL)
        self.bet_scale.pack(pady=10)
        self.start_button = MyButton(self.betframe, text="Start", command=self.start)
        self.start_button.pack(pady=10) 
    
    # starts the game after player has placed bet    
    def start(self):
        # player bet is removed from their bank and added to the winnings pot
        self.player.bet = self.bet_scale.get()           
        self.player.bank -= self.player.bet
        self.winnings += self.player.bet
        
        # all players given a new hand
        self.player.hand = self.deck.new_hand()
        self.dealer.hand = self.deck.new_hand()
        
        if self.opponent_1:
            self.opponent_1.hand = self.deck.new_hand()
                
            if self.opponent_2:
                self.opponent_2.hand = self.deck.new_hand()
        
        # betting frame is removed from the window, the main game frames are created        
        self.betframe.destroy() 
        self.create_widgets()                
        self.update_all_cards()
        
        self.hit_button.config(state=tk.NORMAL)
        self.stay_button.config(state=tk.NORMAL)
    
    # widgets for the main game are created
    def create_widgets(self): 
        # game frame and game details          
        self.game_frame = tk.Frame(self.root, bg=BOARD, )
        self.game_frame.pack(fill= 'x', expand=True)
        
        self.cards_in_deck_frame = tk.Frame(self.game_frame, bg=BOARD)
        self.cards_in_deck_frame.pack()       
        
        self.cards_in_deck_label = MyLabel(self.cards_in_deck_frame, text=f"Cards in Deck:{self.deck.total_cards()} Current goal: {self.goal}")
        self.cards_in_deck_label.pack(side=tk.TOP)
        
        # player cards and details view
        self.player_frame = tk.Frame(self.game_frame, bg=BOARD)
        self.player_frame.pack(side = tk.BOTTOM)
        
        self.player_details_frame = tk.Frame(self.player_frame, bg=BOARD)
        self.player_details_frame.pack(side = tk.LEFT)
        
        MyLabel(self.player_details_frame, text="Your Hand:", font = ("Arial Narrow", 14, 'bold')).pack()
        
        self.player_bank_label = MyLabel(self.player_details_frame, text=f"Bank: {self.player.bank} \nCurrent bet: {self.player.bet}")
        self.player_bank_label.pack()

        self.player_cards_total = MyLabel(self.player_details_frame, text=f"Total:{self.player.total()}")
        self.player_cards_total.pack()
        
        self.player_cards_frame = tk.Frame(self.player_frame, bg=BOARD)
        self.player_cards_frame.pack()
         
        # dealer view
        self.dealer_frame = tk.Frame(self.game_frame, bg=BOARD)
        self.dealer_frame.pack()
        
        MyLabel(self.dealer_frame, text="Dealer's Hand:").pack(side=tk.LEFT)
        
        self.dealer_cards_total = MyLabel(self.dealer_frame, text=f"Total: ?")
        self.dealer_cards_total.pack(side=tk.LEFT)
        
        self.dealer_cards_frame = tk.Frame(self.dealer_frame, bg=BOARD)
        self.dealer_cards_frame.pack()
        
        # opponent view
        if self.opponent_1:
            self.opponent_frame = tk.Frame(self.game_frame, bg=BOARD)
            self.opponent_frame.pack(side= tk.LEFT)
            
            MyLabel(self.opponent_frame, text="Opponent 1's Hand:").pack()
            
            self.opp1_bet_label = MyLabel(self.opponent_frame, text=f"Current bet: {self.opponent_1.bet}")
            self.opp1_bet_label.pack()
            
            self.opponent_1_cards_frame = tk.Frame(self.opponent_frame, bg=BOARD)
            self.opponent_1_cards_frame.pack()
            
            if self.opponent_2:
                MyLabel(self.opponent_frame, text="Opponent 2's Hand:").pack()
                
                self.opp2_bet_label = MyLabel(self.opponent_frame, text=f"Current bet: {self.opponent_2.bet}")
                self.opp2_bet_label.pack()
                
                self.opponent_2_cards_frame = tk.Frame(self.opponent_frame, bg=BOARD)
                self.opponent_2_cards_frame.pack()
        
        # deck extension view
        self.ed_frame = tk.Frame(self.game_frame, bg=BOARD)
        self.ed_frame.pack(side = tk.RIGHT)
        self.ed_cards_frame = tk.Frame(self.ed_frame, bg=BOARD)
        self.ed_cards_frame.pack()
            
        self.buy_ed_card_button = MyButton(self.ed_frame, text="Buy extended deck card £3", command= lambda: self.buy_ed_card())
        self.buy_ed_card_button.pack()
            
        self.use_ed_card_button = MyButton(self.ed_frame, text="Use", command=lambda: self.use_ed_card())
        self.use_ed_card_button.pack()
            
        if self.ed_card:
            tk.Label(self.ed_cards_frame, image = self.ed_card['image'], bg=BOARD).pack()
            self.buy_ed_card_button.config(state=tk.DISABLED)
            self.use_ed_card_button.config(state=tk.NORMAL)
        else:
            tk.Label(self.ed_cards_frame, image = self.extended_deck.card_back, bg=BOARD).pack()
            self.use_ed_card_button.config(state=tk.DISABLED)
            if self.player.bank > 3:
                self.buy_ed_card_button.config(state=tk.NORMAL) 
                
        self.end_game_label = tk.Label(self.game_frame, text=f"Total pot: {self.winnings}", font=(FONT, 18), justify="center", fg=WHITE, bg=BOARD)
        self.end_game_label.place(relx=0.5, rely=0.5, anchor="center")
                    
    # allows user to buy an extended deck card if they have enough money in the bank
    def buy_ed_card(self):
        if self.player.bank > 3:
            self.player.bank -= 3
            self.player_bank_label.config(text=f"Bank: {self.player.bank} \nCurrent bet: {self.player.bet}")
            self.ed_card = self.extended_deck.draw_card()
            for each in self.ed_cards_frame.winfo_children():
                each.destroy()
            tk.Label(self.ed_cards_frame, image = self.ed_card['image'], bg=BOARD).pack()
            self.buy_ed_card_button.config(state=tk.DISABLED)
            self.use_ed_card_button.config(state=tk.NORMAL)
    
    # allows user to use extended deck card 
    def use_ed_card(self):
        if self.ed_card:
            if self.ed_card['card_type'] == 'double_dealer_face_up':
                self.change_card_value(self.dealer,2)
            elif self.ed_card['card_type'] == 'change_goal_by_05':
                self.change_goal(0.5)
            elif self.ed_card['card_type'] == 'change_goal_by_15':
                self.change_goal(1.5)
            elif self.ed_card['card_type'] == 'change_goal_by_2':
                self.change_goal(2)
            elif self.ed_card['card_type'] == 'multiply_pot_by_2':
                self.multiply_pot(2)
            elif self.ed_card['card_type'] == 'multiply_pot_by_5':
                self.multiply_pot(5)
            elif self.ed_card['card_type'] == 'multiply_pot_by_10':
                self.multiply_pot(10)
            elif self.ed_card['card_type'] == 'new_hand':
                if self.deck.total_cards() > 2:
                    for widget in self.player_cards_frame.winfo_children():
                        widget.destroy()
                    self.player.hand = self.deck.new_hand()
                    for card in self.player.hand:
                        self.update_card(self.player_cards_frame, card)
                    self.player_cards_total.config(text=f"Total:{self.player.total()}")
                    self.update_total_cards()
                else:
                    self.stay()
            
            self.ed_card = None
            for each in self.ed_cards_frame.winfo_children():
                each.destroy()
            tk.Label(self.ed_cards_frame, image = self.extended_deck.card_back, bg=BOARD).pack()
            self.use_ed_card_button.config(state=tk.DISABLED)
    
    # updates all cards to show the right image
    def update_all_cards(self):
        for widget in self.player_cards_frame.winfo_children():
            widget.destroy()
        for widget in self.dealer_cards_frame.winfo_children():
            widget.destroy()
        if self.opponent_1:
            for widget in self.opponent_1_cards_frame.winfo_children():
                widget.destroy()
            if self.opponent_2:
                for widget in self.opponent_2_cards_frame.winfo_children():
                    widget.destroy()
                    
        for card in self.player.hand:
            self.update_card(self.player_cards_frame, card)
        
        self.update_card(self.dealer_cards_frame, self.dealer.hand[0])
        tk.Label(self.dealer_cards_frame, image = self.deck.photo_image_back, bg=BOARD).pack(side=tk.LEFT)
           
        if self.opponent_1:
            tk.Label(self.opponent_1_cards_frame, image = self.deck.photo_image_back, bg=BOARD).pack(side=tk.LEFT)
            tk.Label(self.opponent_1_cards_frame, image = self.deck.photo_image_back, bg=BOARD).pack(side=tk.LEFT)
                
            if self.opponent_2:
                tk.Label(self.opponent_2_cards_frame, image = self.deck.photo_image_back, bg=BOARD).pack(side=tk.LEFT)
                tk.Label(self.opponent_2_cards_frame, image = self.deck.photo_image_back, bg=BOARD).pack(side=tk.LEFT)
        
        self.update_total_cards()
    
    # player picks a card and adds it to their hand    
    def hit(self):
        if self.deck.total_cards() >= 1:
            card = self.deck.draw_card()
            self.update_card(self.player_cards_frame, card)
            self.player.hand.append(card)
            self.update_total_cards()
            self.player_cards_total.config(text=f"Total:{self.player.total()}")
            
            # if the player goes above the current goal, the round ends
            if self.player.is_bust(self.goal):
                self.stay() 
        # if there are no cards, the game ends  
        else:
            self.player_cards_total.config(text=f"Total:{self.player.total()}")
            self.game_over()
    
    # turns over opponent and dealer cards, opponent and dealer have turns     
    def settle_up(self, my_frame, my_player, winning_opponent, winning_total):
        for widget in my_frame.winfo_children():
            widget.destroy()
            
        for card in my_player.hand:
            self.update_card(my_frame, card)     
                             
        while my_player.total() < self.goal-4 and self.deck.total_cards() > 0:
            card = self.deck.draw_card()
            self.update_card(my_frame,card)
            my_player.hand.append(card)
            
        winning_opponent, winning_total = self.check_win(my_player, winning_opponent, winning_total)
        return winning_opponent, winning_total
    
    # checks to see if the player has a winning hand   
    def check_win(self,my_player, winning_opponent, winning_total):
        if not my_player.is_bust(self.goal):
            if winning_opponent:
                if my_player.total() > winning_total:
                    winning_opponent = my_player
                    winning_total = my_player.total()
                elif my_player.total() == winning_total:
                    if isinstance(winning_opponent, list):
                        winning_opponent.append(my_player)
                    else:
                        current_reigning = winning_opponent
                        winning_opponent = [current_reigning, my_player] 
            else:
                winning_opponent = my_player
                winning_total = my_player.total()
        return winning_opponent, winning_total
    
    # ends the round            
    def stay(self):
        self.buy_ed_card_button.config(state=tk.DISABLED)
        self.use_ed_card_button.config(state=tk.DISABLED)
        winning_opponent = None
        winning_total = 0
        
        # opponent and dealer have their turns
        winning_opponent, winning_total = self.settle_up(self.dealer_cards_frame, self.dealer, winning_opponent, winning_total)       
        self.dealer_cards_total.config(text=f"Total:{self.dealer.total()}")
        
        if self.opponent_1: 
            winning_opponent, winning_total = self.settle_up(self.opponent_1_cards_frame, self.opponent_1, winning_opponent, winning_total)                  
            self.opp1_bet_label.config(text=f"Opponent 1 Hand Total: {self.opponent_1.total()}")
    
            if self.opponent_2: 
                winning_opponent, winning_total = self.settle_up(self.opponent_2_cards_frame, self.opponent_2, winning_opponent, winning_total)                       
                self.opp2_bet_label.config(text=f"Opponent 2 Hand Total: {self.opponent_2.total()}")
        
        # player has their turn       
        if not self.player.is_bust(self.goal):
            winning_opponent, winning_total = self.check_win(self.player, winning_opponent, winning_total)
        
        # checks if it is a draw and adds money to the bank                     
        if winning_opponent:
            if isinstance(winning_opponent, list):
                self.end_game("It's a draw!")
            else:
                if winning_opponent != self.dealer:
                    winning_opponent.bank += self.winnings * 1.5
                    winning_opponent.wins += 1
                    self.player_bank_label.config(text=f"Bank: {self.player.bank} Current bet: 0")
                self.end_game(f"{winning_opponent.name} wins")           
    
    # all frames are destroyed and the user is returned to the menu
    def exit_to_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy() 
        MainMenu(self.root)
    
    # destroys game frames   
    def destroy_game_frames(self):
        if hasattr(self, "game_frame") and self.game_frame.winfo_exists():
            for widget in self.game_frame.winfo_children():
                widget.destroy()
            self.game_frame.destroy()
    
    # card image is updated            
    def update_card(self, frame, card):
        tk.Label(frame, image = card['image'], bg=BOARD).pack(side=tk.LEFT)
    
    # label with the amount of cards in deck is updated         
    def update_total_cards(self):
        self.cards_in_deck_label.config(text=f"Cards in Deck:{self.deck.total_cards()} Current goal: {self.goal}")
    
    # end of game message is displayed            
    def end_game(self, message):       
        self.end_game_label.config(text=message, font=(FONT, 24))
        self.hit_button.config(state=tk.DISABLED)
        self.stay_button.config(state=tk.DISABLED)
        if self.deck.total_cards() > 4 + (self.num_opponents*2):
            self.new_round_button.config(state=tk.NORMAL)         
        else:
            self.game_over()
    
    # not enough cards are left
    def game_over(self):
        self.game_over_label = tk.Label(self.game_frame, text=f"You finish the game with £{self.player.bank} after winning {self.player.wins} rounds", font=(FONT, 24), justify="center", fg=WHITE, bg=BOARD)
        self.game_over_label.place(relx=0.5, rely=0.5, anchor="center")
    
    # extended deck card allows goal to be changed by a specified amount    
    def change_goal(self, mult):
        self.goal = int(self.goal * mult)
        self.cards_in_deck_label.config(text=f"Cards in Deck:{self.deck.total_cards()} Current goal: {self.goal}")
        if self.player.is_bust(self.goal):
            self.stay()
    
    # extended deck card allows card value to be changed by a specified amount
    def change_card_value(self, player, mult):
        if player.hand[0]['rank'] in face_cards:
            player.hand[0]['rank'] = 11 * mult
        else:
            player.hand[0]['rank'] = int(int(player.hand[0]['rank']) * mult)
        if player == self.dealer:
            self.dealer_cards_total.config(text=f"Total: At least {self.dealer.hand[0]["rank"]}")
        elif player == self.player:
            self.player_cards_total.config(text=f"Total:{self.player.total()}")
    
    # extended deck card allows winnings pot to be multiplied by a specified amount
    def multiply_pot(self, mult):
        self.winnings = self.winnings * mult
        self.end_game_label.config(text=f"Total pot: {self.winnings}")
        

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x720")
    root.resizable(True,True)
    root.title("Blackjack")
    root.configure(background=BLACK)
    MainMenu(root)
    root.mainloop()