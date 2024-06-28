import chess
import chess.pgn
from io import StringIO
from stockfish import Stockfish

# Initialize Stockfish
stockfish = Stockfish(path="stockfish/stockfish-windows-x86-64-avx2.exe", depth=18)

# Function to get analysis for the current position
def get_position_analysis(fen, num_moves=10):
    stockfish.set_fen_position(fen)
    evaluation = stockfish.get_evaluation()
    moves = stockfish.get_top_moves(num_moves)
    analysis = {}
    
    print(f"Evaluation details: {evaluation}")
    
    for move in moves:
        eval_diff = move.get('Centipawn')
        
        
        
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
            analysis[move['Move']] = 'BLUNDER'
    
    return analysis

# Function to classify the player's move
def classify_move(player_move, fen):
    analysis = get_position_analysis(fen)
    return analysis.get(player_move, 'unknown')

# PGN to analyze
pgn_text = """
[Event "Live Chess"]
[Site "Chess.com"]
[Date "2024.06.28"]
[Round "-"]
[White "Nari2222"]
[Black "The_AI_Human"]
[Result "1-0"]
[CurrentPosition "Q2k4/p3b3/1p4p1/2pB1n1p/8/8/P4PPP/R3R1K1 b - -"]
[Timezone "UTC"]
[ECO "C45"]
[ECOUrl "https://www.chess.com/openings/Scotch-Game-3...exd4"]
[UTCDate "2024.06.28"]
[UTCTime "06:18:25"]
[WhiteElo "1010"]
[BlackElo "989"]
[TimeControl "600"]
[Termination "Nari2222 won by resignation"]
[StartTime "06:18:25"]
[EndDate "2024.06.28"]
[EndTime "06:27:07"]
[Link "https://www.chess.com/game/live/107975786262"]
[WhiteUrl "https://images.chesscomfiles.com/uploads/v1/user/59467046.d1fa8c9c.50x50o.1dc960eec4a1.jpg"]
[WhiteCountry "69"]
[WhiteTitle ""]
[BlackUrl "https://images.chesscomfiles.com/uploads/v1/user/317885267.62c7ccc5.50x50o.243d7145da48.jpg"]
[BlackCountry "69"]
[BlackTitle ""]
1. e4 e5 2. Nf3 Nc6 3. d4 exd4 4. Ng5 Be7 5. Nxf7 Kxf7 6. Bc4+ Ke8 7. Qh5+ g6 8. Qf3 Nf6 9. Bg5 Rf8 10. Bxf6 Rxf6 11. Qe2 d6 12. c3 h5 13. cxd4 Nxd4 14. Qd3 c5 15. Nc3 Qb6 16. O-O Qxb2 17. e5 Bf5 18. Qg3 Qxc3 19. Qxc3 Be6 20. exf6 Bxf6 21. Qg3 Bf5 22. Qxd6 b6 23. Rfe1+ Be6 24. Bxe6 Be7 25. Bd5 Nf5 26. Qc6+ Kd8 27. Qxa8+ 1-0
"""

# Parse PGN
pgn_io = StringIO(pgn_text)
game = chess.pgn.read_game(pgn_io)
board = game.board()

# Iterate through the moves and classify each one
for move in game.mainline_moves():
    player_move = board.san(move)
    fen = board.fen()
    move_classification = classify_move(board.uci(move), fen)
    print(f"The move {player_move} is classified as: {move_classification}")
    board.push(move)
