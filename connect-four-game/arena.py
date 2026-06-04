import time
from engine import ConnectFour
from mcts import MCTSAgent
from minimax import MinimaxAgent

def run_live_arena():
    print("=" * 40)
    print("      THE ADVERSARIAL AI SHOWDOWN       ")
    print("      MCTS (X)  vs.  MINIMAX (O)        ")
    print("=" * 40)
    
    # Initialize components
    game = ConnectFour()
    mcts_agent = MCTSAgent(iterations=800)     # Adjust for speed vs depth
    minimax_agent = MinimaxAgent(depth=5)      # Adjust depth for difficulty
    
    game.render()
    
    while game.check_winner() is None:
        if game.current_player == 1:
            print("\n[MCTS Agent (X) is calculating...]")
            start_time = time.time()
            move = mcts_agent.get_best_move(game)
            elapsed = time.time() - start_time
            print(f"MCTS chose column {move} in {elapsed:.2f}s")
        else:
            print("\n[Minimax Agent (O) is calculating...]")
            start_time = time.time()
            move = minimax_agent.get_best_move(game)
            elapsed = time.time() - start_time
            print(f"Minimax chose column {move} in {elapsed:.2f}s")
            
        game.make_move(move)
        game.render()
        time.sleep(0.5) # Structural pause for presentation flow
        
    # Declare Results
    result = game.check_winner()
    print("\n" + "=" * 40)
    print("               MATCH OVER               ")
    print("=" * 40)
    if result == 1:
        print("🏆 VICTOR: Monte Carlo Tree Search (MCTS) Agent!")
    elif result == -1:
        print("🏆 VICTOR: Minimax Agent with Alpha-Beta Pruning!")
    else:
        print("🤝 DRAW: Tactical Stalemate.")
    print("=" * 40)

if __name__ == "__main__":
    run_live_arena()