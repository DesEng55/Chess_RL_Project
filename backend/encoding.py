import numpy as np
import chess

def encode_board_advanced(board: chess.Board):
    """
    12x8x8 tensor:
    6 piece types × 2 colors
    """
    piece_map = board.piece_map()
    planes = np.zeros((12, 8, 8), dtype=np.float32)

    piece_to_plane = {
        chess.PAWN: 0,
        chess.KNIGHT: 1,
        chess.BISHOP: 2,
        chess.ROOK: 3,
        chess.QUEEN: 4,
        chess.KING: 5
    }

    for square, piece in piece_map.items():
        row = 7 - chess.square_rank(square)
        col = chess.square_file(square)
        offset = 0 if piece.color == chess.WHITE else 6
        plane = piece_to_plane[piece.piece_type] + offset
        planes[plane, row, col] = 1.0

    return planes
