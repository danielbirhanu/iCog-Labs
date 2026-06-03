import math
import random

class MCTSNode:
    def __init__(self, game_state, move=None, parent=None):
        self.game_state = game_state  # ConnectFour instance
        self.move = move              # The move that led to this node
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0.0
        self.untried_moves = game_state.get_valid_moves()

    def uct_select_child(self, exploration_constant=1.414):
        """Uses the UCT formula to select the best child node."""
        best_score = -float('inf')
        best_child = None
        
        for child in self.children:
            # Standard Upper Confidence Bound for Trees formula
            exploitation = child.wins / child.visits
            exploration = exploration_constant * math.sqrt(math.log(self.visits) / child.visits)
            score = exploitation + exploration
            
            if score > best_score:
                best_score = score
                best_child = child
        return best_child

    def expand(self, move, child_state):
        """Phase 2: Expansion - Add a new child node to the tree."""
        child_node = MCTSNode(game_state=child_state, move=move, parent=self)
        self.untried_moves.remove(move)
        self.children.append(child_node)
        return child_node

    def update(self, result, player_who_moved):
        """Phase 4: Backpropagation - Update statistics up to the root."""
        self.visits += 1
        if result == 0:
            self.wins += 0.5  # Draw
        elif result == player_who_moved:
            self.wins += 1.0  # Win
        # Lose adds 0

class MCTSAgent:
    def __init__(self, iterations=1000):
        self.iterations = iterations

    def get_best_move(self, current_game):
        root = MCTSNode(game_state=current_game.clone())
        
        for _ in range(self.iterations):
            node = root
            state = current_game.clone()
            
            # --- PHASE 1: SELECTION ---
            while len(node.untried_moves) == 0 and len(node.children) > 0:
                node = node.uct_select_child()
                state.make_move(node.move)
                
            # --- PHASE 2: EXPANSION ---
            if len(node.untried_moves) > 0:
                move = random.choice(node.untried_moves)
                state.make_move(move)
                node = node.expand(move, state)
                
            # --- PHASE 3: SIMULATION (Rollout) ---
            winner = state.check_winner()
            while winner is None:
                valid_moves = state.get_valid_moves()
                state.make_move(random.choice(valid_moves))
                winner = state.check_winner()
                
            # --- PHASE 4: BACKPROPAGATION ---
            # Pass the simulated winner back up to the root node
            while node is not None:
                # The player who moved is the opponent of the player whose turn it *now* is
                player_who_moved = -node.game_state.current_player
                node.update(winner, player_who_moved)
                node = node.parent
                
        # Return the move with the highest overall visit count (robust child)
        return max(root.children, key=lambda c: c.visits).move