from poker_game import PokerGame
from utils.utils import format_cards
from mcts import MCTS
import copy 
from deuces import Evaluator

# main.py
def main():
    game = PokerGame()
    game.deal_cards()

    evaluator = Evaluator()
    mcts = MCTS(root_state=game, evaluator=evaluator)

    print("Starting pre-flop")
    print(f"Player 1 hand: {format_cards(game.player1_hand)}")
    print(f"Player 2 hand: {format_cards(game.player2_hand)}")

    while game.round != "end":
        mcts.search(num_simulations=1000)
        best_action, best_node = mcts.root.best_child()

        if best_action is None:
            print("No valid action found. Ending the game.")
            break

        print(f"AI decided to: {best_action}")
        game.apply_action(best_action)

        if game.round in ["flop", "turn", "river"]:
            game.deal_community_cards()

        game.print_results()

        if game.round == "end":
            break

        mcts = MCTS(root_state=game, evaluator=evaluator)

    game.result()

if __name__ == "__main__":
    main()

