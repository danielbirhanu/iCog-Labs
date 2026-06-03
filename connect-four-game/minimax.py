class MinimaxAgent:
    def __init__(self, depth=4):
        self.max_depth = depth
        # Positional heuristic scoring matrix to prioritize the center columns
        self.evaluation_matrix = [
            [3, 4, 5, 7, 5, 4, 3],
            [3, 4, 5, 7, 5, 4, 3],
            [3, 4, 7, 8, 7, 4, 3],
            [3, 4, 7, 8, 7, 4, 3],
            [4, 5, 8, 10, 8, 5, 4],
            [5, 6, 9, 11, 9, 6, 5]
        ]

    def evaluate_board(self, game):
        """Heuristic evaluation tracking positional strength."""
        score = 0
        for r in range(6):
            for c in range(7):
                if game.board[r][c] == 1:
                    score += self.evaluation_matrix[r][c]
                elif game.board[r][c] == -1:
                    score -= self.evaluation_matrix[r][c]
        return score

    def minimax(self, game, depth, alpha, beta, is_maximizing):
        winner = game.check_winner()
        
        # Terminal node states
        if winner == 1:
            return 100000 + depth, None
        if winner == -1:
            return -100000 - depth, None
        if winner == 0:
            return 0, None
        if depth == 0:
            return self.evaluate_board(game), None

        valid_moves = game.get_valid_moves()
        best_move = valid_moves[0] if valid_moves else None

        if is_maximizing:
            max_eval = -float('inf')
            for move in valid_moves:
                cloned_game = game.clone()
                cloned_game.make_move(move)
                evaluation, _ = self.minimax(cloned_game, depth - 1, alpha, beta, False)
                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = move
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break  # Beta cut-off
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in valid_moves:
                cloned_game = game.clone()
                cloned_game.make_move(move)
                evaluation, _ = self.minimax(cloned_game, depth - 1, alpha, beta, True)
                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = move
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break  # Alpha cut-off
            return min_eval, best_move

    def get_best_move(self, game):
        is_maximizing = True if game.current_player == 1 else False
        _, move = self.minimax(game, self.max_depth, -float('inf'), float('inf'), is_maximizing)
        return move