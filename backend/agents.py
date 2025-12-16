import random
import chess
import torch
import torch.optim as optim
import numpy as np
import time

from model import PolicyValueNet
from encoding import encode_board_advanced

class ChessAgent:
    def __init__(self, agent_id, lr=1e-3):
        self.id = agent_id
        self.model = PolicyValueNet()
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.elo = 1200
        
        # Statistics
        self.games_played = 0
        self.wins = 0
        self.losses = 0
        self.draws = 0
        
    def select_move(self, board):
        """Select best move based on position evaluation"""
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None
            
        scores = []
        
        for move in legal_moves:
            board.push(move)
            state = torch.tensor(
                encode_board_advanced(board),
                dtype=torch.float32
            ).unsqueeze(0)
            
            with torch.no_grad():
                _, value = self.model(state)
            
            # Negate value if it's opponent's turn after the move
            # Higher value = better for the side to move
            score = -value.item() if board.turn != chess.WHITE else value.item()
            scores.append(score)
            board.pop()
        
        best_idx = int(np.argmax(scores))
        return legal_moves[best_idx], scores[best_idx]
    
    def update_elo(self, opponent_elo, result):
        """Update ELO rating based on game result
        result: 1.0 for win, 0.5 for draw, 0.0 for loss
        """
        K = 32  # K-factor
        expected = 1 / (1 + 10 ** ((opponent_elo - self.elo) / 400))
        self.elo += K * (result - expected)
        
    def record_result(self, result):
        """Record game result in statistics"""
        self.games_played += 1
        if result == 1.0:
            self.wins += 1
        elif result == 0.0:
            self.losses += 1
        else:
            self.draws += 1
    
    def get_stats(self):
        """Get agent statistics as dict"""
        return {
            'id': self.id,
            'elo': self.elo,
            'games_played': self.games_played,
            'wins': self.wins,
            'losses': self.losses,
            'draws': self.draws
        }

class MultiAgentChessSystem:
    def __init__(self, population_size=4):
        self.agents = [ChessAgent(i) for i in range(population_size)]
        
    def play_match(self, socketio=None, match_num=None, total_matches=None):
        """Play a single match between two random agents"""
        board = chess.Board()
        white = random.choice(self.agents)
        black = random.choice(self.agents)
        
        # Avoid self-play if possible
        if len(self.agents) > 1:
            while black.id == white.id:
                black = random.choice(self.agents)
        
        # Emit initial board state
        if socketio:
            socketio.emit("board_update", {
                "fen": board.fen(),
                "white_agent": white.id,
                "black_agent": black.id
            })
            time.sleep(0.5)  # Brief pause to show initial position
        
        move_number = 0
        move_history = []
        
        # Play the game
        while not board.is_game_over() and move_number < 200:  # Max 200 moves to prevent infinite games
            agent = white if board.turn == chess.WHITE else black
            
            try:
                result = agent.select_move(board)
                if result is None:
                    break
                    
                move, evaluation = result
                san = board.san(move)
                board.push(move)
                move_number += 1
                
                move_history.append({
                    'san': san,
                    'move_number': move_number,
                    'evaluation': evaluation
                })
                
                # Emit move update
                if socketio:
                    socketio.emit("move_made", {
                        "fen": board.fen(),
                        "move_san": san,
                        "move_number": move_number,
                        "evaluation": evaluation,
                        "current_turn": "white" if board.turn == chess.WHITE else "black"
                    })
                    time.sleep(0.3)  # Delay between moves for visualization
                    
            except Exception as e:
                print(f"Error during move: {e}")
                break
        
        # Determine result
        result_str = board.result()
        
        # Update ELO ratings
        if result_str == "1-0":  # White wins
            white.update_elo(black.elo, 1.0)
            black.update_elo(white.elo, 0.0)
            white.record_result(1.0)
            black.record_result(0.0)
            winner = "White"
        elif result_str == "0-1":  # Black wins
            white.update_elo(black.elo, 0.0)
            black.update_elo(white.elo, 1.0)
            white.record_result(0.0)
            black.record_result(1.0)
            winner = "Black"
        else:  # Draw
            white.update_elo(black.elo, 0.5)
            black.update_elo(white.elo, 0.5)
            white.record_result(0.5)
            black.record_result(0.5)
            winner = "draw"
        
        # Emit match completion
        if socketio:
            socketio.emit("match_complete", {
                "result": result_str,
                "winner": winner,
                "white_agent": white.id,
                "black_agent": black.id,
                "white_elo": white.elo,
                "black_elo": black.elo,
                "total_moves": move_number
            })
            
            # Update agent list
            socketio.emit("agents_update", {
                "agents": [agent.get_stats() for agent in self.agents]
            })
        
        return {
            'result': result_str,
            'winner': winner,
            'white': white.id,
            'black': black.id,
            'moves': move_number,
            'white_elo': white.elo,
            'black_elo': black.elo
        }
    
    def train(self, num_matches=10, socketio=None):
        """Run multiple training matches"""
        if socketio:
            socketio.emit("training_started", {
                "num_matches": num_matches
            })
        
        results = []
        
        for i in range(num_matches):
            if socketio:
                socketio.emit("match_starting", {
                    "match_number": i + 1,
                    "total_matches": num_matches
                })
            
            try:
                result = self.play_match(socketio, i + 1, num_matches)
                results.append(result)
            except Exception as e:
                print(f"Error in match {i+1}: {e}")
                continue
        
        if socketio:
            socketio.emit("training_complete", {
                "total_matches": len(results)
            })
            
            # Final agent update
            socketio.emit("agents_update", {
                "agents": [agent.get_stats() for agent in self.agents]
            })
        
        return results
    
    def get_agents_stats(self):
        """Get statistics for all agents"""
        return [agent.get_stats() for agent in self.agents]