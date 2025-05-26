# mcts.py
import random
import copy
from deuces import Evaluator
from poker_game import PokerGame

class Node:
    def __init__(self, state, parent=None, action=None):
        self.state = state  # The current game state
        self.parent = parent
        self.action = action  # The action that led to this state
        self.children = []  # List to store child nodes
        self.visits = 0  # Number of times the node has been visited
        self.wins = 0  # Number of wins from this node

    def add_child(self, child_state, action):
        """Create a new child node with the given state and action, and add it to children."""
        child_node = Node(state=child_state, parent=self, action=action)
        self.children.append(child_node)
        return child_node

    def update(self, result):
        """Update the node's visit count and win count."""
        self.visits += 1
        self.wins += result

    def best_child(self, exploration_weight=1.0):
        """Return the child node with the highest UCT value and its action."""
        if not self.children:
            return None, None

        def value(child):
            if child.visits == 0:
                return float('inf')
            return (child.wins / child.visits) + exploration_weight * (2 * (self.visits)**0.5) / (1 + child.visits)
        
        best_node = max(self.children, key=value)
        return best_node.action, best_node

class MCTS:
    def __init__(self, root_state, evaluator):
        self.root = Node(state=root_state)
        self.evaluator = evaluator

    def search(self, num_simulations):
        """Run the MCTS algorithm for a given number of simulations."""
        for _ in range(num_simulations):
            # Selection: Start from the root and choose the best node to explore
            node = self._select(self.root)

            # Expansion: Expand the node if it hasn't been fully expanded yet
            if node.visits == 0:
                result = self._simulate(node.state)
            else:
                possible_actions = self.get_possible_actions(node.state)
                action = random.choice(possible_actions)
                new_state = self.apply_action(node.state, action)
                new_node = node.add_child(new_state, action)  # Pass action here
                result = self._simulate(new_node.state)

            # Backpropagation: Backpropagate the result up the tree
            self._backpropagate(node, result)

    def _select(self, node):
        """Select the best node to explore."""
        while node.children:
            action, node = node.best_child()  # Unpack the tuple, but keep only the node
        return node

    def _expand(self, state):
        possible_actions = self.get_possible_actions(state)
        if not possible_actions:
            return state  # No actions to expand, return the same state

        for action in possible_actions:
            new_state = self.apply_action(state, action)
            self.root.add_child(new_state, action)

    def get_possible_actions(self, state):
        """Get a list of possible actions for the current state."""
        if state.round == "pre_flop":
            return ["fold", "call", "bet"]
        elif state.round in ["flop", "turn", "river"]:
            return ["fold", "check", "call", "bet", "raise"]
        else:
            return []

    def apply_action(self, state, action):
        """Apply the given action to the state and return the new state."""
        new_state = copy.deepcopy(state)

        if action == "fold":
            new_state.round = "end"
            new_state.winner = "opponent" if state.current_player == "player" else "player"
        elif action == "call":
            new_state.current_bet = state.current_bet
            new_state.pot += new_state.current_bet
        elif action == "check":
            pass  # Move to the next stage without betting
        elif action == "raise":
            new_state.current_bet += 20
            new_state.pot += new_state.current_bet

        new_state.current_player = "opponent" if state.current_player == "player" else "player"

        return new_state

    def _simulate(self, state):
        """Simulate a random playout from the given state."""
        current_state = copy.deepcopy(state)

        while current_state.round != "end":
            possible_actions = self.get_possible_actions(current_state)
            action = random.choice(possible_actions)
            current_state = self.apply_action(current_state, action)

            if current_state.round == "flop":
                current_state.community_cards.extend(current_state.deck.draw(3))
                current_state.round = "turn"
            elif current_state.round == "turn":
                current_state.community_cards.append(current_state.deck.draw(1))
                current_state.round = "river"
            elif current_state.round == "river":
                current_state.community_cards.append(current_state.deck.draw(1))
                current_state.round = "end"

        # Evaluate hands
        p1_hand = current_state.player1_hand
        p2_hand = current_state.player2_hand
        community_cards = current_state.community_cards
        
        if len(community_cards) < 5:
            # Ensure we have 5 community cards
            while len(community_cards) < 5:
                community_cards.append(current_state.deck.draw(1))
        
        # Evaluate hands: pass hand and community cards separately
        p1_score = self.evaluator.evaluate(p1_hand, community_cards)
        p2_score = self.evaluator.evaluate(p2_hand, community_cards)
        
        # Determine the result
        if p1_score < p2_score:
            return 1  # Player 1 wins
        elif p1_score > p2_score:
            return -1  # Player 2 wins
        else:
            return 0  # Tie

    def _backpropagate(self, node, result):
        """Backpropagate the simulation result up the tree."""
        while node is not None:
            node.update(result)
            node = node.parent
