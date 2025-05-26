import deuces
from deuces import Deck, Evaluator, Card # type: ignore
from utils.utils import format_cards, describe_hand
import random
import copy

class PokerGame:
    def __init__(self):
        # Initialize game components
        self.deck = Deck()
        self.evaluator = Evaluator()
        self.pot = 0 
        self.current_bet = 0 
        self.player1_hand = []
        self.player2_hand = []
        self.community_cards = []
        self.player1_money = 1000
        self.player2_money = 1000
        self.player1_bet = 0 
        self.player2_bet = 0 
        self.round = "pre_flop"
        self.current_player = "player 1"

    def switch_player(self):
        """Switch the current player."""
        self.current_player = "player2" if self.current_player == "player1" else "player1"

    def deal_cards(self):
        self.player1_hand = [self.deck.draw(1), self.deck.draw(1)]
        self.player2_hand = [self.deck.draw(1), self.deck.draw(1)]
    

    def deal_community_cards(self):
        if self.round == "pre_flop":
            self.round = "flop"
            self.community_cards = self.deck.draw(3) 
            # Deal the flop 
        elif self.round == "flop":
            self.round = "turn"
            self.community_cards.append(self.deck.draw(1))
            # Deal the turn 
        elif self.round == "turn":
            self.round = "river"
            self.community_cards.append(self.deck.draw(1))
            # Deal the river 
        elif self.round == "river":
            self.round = "end"
        else:
            raise Exception("Invalid Game State")

    def bet(self, player, amount):
        # Implement betting logic
        if player == 1:
            if amount > self.player1_money:
                raise ValueError("Insufficient Funds")
            self.player1_bet += amount
            self.player1_money -= amount
        else:
            if amount > self.player2_money:
                raise ValueError("Insufficient Funds")
            self.player2_bet += amount 
            self.player2_money -= amount
        self.pot += amount 
        self.current_bet = max(self.player1_bet, self.player2_bet)


    def call(self, player):
        if player == 1:
            call_amount = self.current_bet - self.player1_bet
            if call_amount > self.player1_money:
                raise ValueError("Insufficient Funds")
            self.bet(player, call_amount)
        elif player == 2:
            call_amount = self.current_bet - self.player2_bet
            if call_amount > self.player2_money:
                raise ValueError("Insufficient Funds")
            self.bet(player, call_amount)


    def fold(self, player):
        if player == 1:
            print("Player 1 folds. Player 2 wins.")
            self.player2_money += self.pot
        else:
            print("Player 2 folds. Player 1 wins.")
            self.player1_money += self.pot 
        self.pot = 0 
        self.round = "end"
    

    def check(self, player):
        if player == 1:
            print("Player 1 checks.")
        elif player == 2:
            print("Player 2 checks.")

    def apply_action(self, action):
        if self.current_player == "player1":
            if action == "bet":
                self.bet(player=1, amount=10)  # Example: player 1 bets 10
            elif action == "call":
                self.call(player=1)  # Example: player 1 calls
            elif action == "fold":
                self.fold(player=1)  # Example: player 1 folds
            elif action == "check":
                self.check(player=1)  # Example: player 1 checks
        elif self.current_player == "player2":
            if action == "bet":
                self.bet(player=2, amount=10)  # Example: player 2 bets 10
            elif action == "call":
                self.call(player=2)  # Example: player 2 calls
            elif action == "fold":
                self.fold(player=2)  # Example: player 2 folds
            elif action == "check":
                self.check(player=2)  # Example: player 2 checks

        # Switch to the other player
        self.switch_player()

    def evaluate_hands(self):
    # Ensure there are 5 community cards before evaluating
        while len(self.community_cards) < 5:
            self.community_cards.append(self.deck.draw(1))

        p1_score = self.evaluator.evaluate(self.player1_hand, self.community_cards)
        p2_score = self.evaluator.evaluate(self.player2_hand, self.community_cards)
        return p1_score, p2_score
    

    def print_results(self):
        p1_score, p2_score = self.evaluate_hands()
        p1_hand_description = describe_hand(self.evaluator.get_rank_class(p1_score))
        p2_hand_description = describe_hand(self.evaluator.get_rank_class(p2_score))
        print(f"Player 1 hand: {format_cards(self.player1_hand)}")
        print(f"Player 2 hand: {format_cards(self.player2_hand)}")
        print(f"Community cards: {format_cards(self.community_cards)}")
        print(f"Player 1 score: {p1_score} ({p1_hand_description}), Player 2 score: {p2_score} ({p2_hand_description})")
    
    
    def result(self):
        p1_score, p2_score = self.evaluate_hands()
        if p1_score < p2_score:
            print("Player 1 wins!")
            self.player1_money += self.pot
        elif p1_score > p2_score:
            print("Player 2 wins!")
            self.player2_money += self.pot
        else:
            print("Tie")
            self.player1_money += self.pot / 2
            self.player2_money += self.pot / 2

        self.pot = 0 
        self.player1_bet = 0 
        self.player2_bet = 0 

        print(f"Player 1 money: {self.player1_money}")
        print(f"Player 2 money: {self.player2_money}")
        print(f"Pot: {self.pot}")

    def copy(self):
        return copy.deepcopy(self)
    

