from flask import Flask, jsonify, request
from flask_cors import CORS
import chess
import chess.pgn
from io import StringIO
from stockfish import Stockfish

app = Flask(__name__)
CORS(app)

# Initialize Stockfish
stockfish = Stockfish(path="stockfish/stockfish-windows-x86-64-avx2.exe")

# Function to get analysis for the current position
def get_position_analysis(fen, num_moves=10):
    stockfish.set_fen_position(fen)
    moves = stockfish.get_top_moves(num_moves)
    analysis = {}
    
    for move in moves:
        eval_diff = move.get('Centipawn', 0)
        
        if eval_diff == None:
            continue
        
        if eval_diff >= 30 and eval_diff <= 55 or eval_diff == 0:
            analysis[move['Move']] = 'best move'
        elif eval_diff > 20:
            analysis[move['Move']] = 'excellent'
        elif eval_diff > 15:
            analysis[move['Move']] = 'good'
        elif abs(eval_diff) > 50:
            analysis[move['Move']] = 'mistake'
        elif abs(eval_diff) < abs(150):
            analysis[move['Move']] = 'mistake'  
        else:
            analysis[move['Move']] = 'blunder'
    
    return analysis

# Function to classify the player's move
def classify_move(player_move, fen):
    analysis = get_position_analysis(fen)
    return analysis.get(player_move, 'unknown')

# Route to analyze PGN
@app.route('/analyze', methods=['POST'])
def analyze_pgn():
    data = request.get_json()
    pgn_text = data.get('pgn')
    
    pgn_io = StringIO(pgn_text)
    game = chess.pgn.read_game(pgn_io)
    board = game.board()
    
    white_moves = {'best moves': [], 'excellent moves': [], 'good moves': [], 'mistakes': [], 'blunders': []}
    black_moves = {'best moves': [], 'excellent moves': [], 'good moves': [], 'mistakes': [], 'blunders': []}
    
    classification_mapping = {
        'best move': 'best moves',
        'excellent': 'excellent moves',
        'good': 'good moves',
        'mistake': 'mistakes',
        'blunder': 'blunders'
    }
    
    for move in game.mainline_moves():
        player_move = board.san(move)
        fen = board.fen()
        move_classification = classify_move(board.uci(move), fen)
        move_key = classification_mapping.get(move_classification, 'unknown')
        
        if board.turn == chess.WHITE:
            if move_key in white_moves:
                white_moves[move_key].append(player_move)
        else:
            if move_key in black_moves:
                black_moves[move_key].append(player_move)
        
        board.push(move)
    
    return jsonify({'White': white_moves, 'Black': black_moves})

if __name__ == '__main__':
    app.run(debug=True)
