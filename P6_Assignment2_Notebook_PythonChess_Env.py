# Imports and requirements

import pdb
import time
import timeit
import random
import chess
import chess.svg

from chess.polyglot import zobrist_hash
from copy import deepcopy

# Live Visualisation
# Credit: https://bit.ly/3qImKaT

from IPython.display import display, HTML, clear_output


def who(player):
    # Credit: https://bit.ly/3qImKaT
    return "White" if player == chess.WHITE else "Black"


def display_board(board, use_svg):
    # Credit: https://bit.ly/3qImKaT
    if use_svg:
        return board._repr_svg_()
    else:
        return "<pre>" + str(board) + "</pre>"
    pass


def isDraw(board):
    return (board.is_fivefold_repetition() or
            board.is_seventyfive_moves() or 
            board.is_insufficient_material() or
            board.is_stalemate() or
            board.can_claim_draw() or 
            board.can_claim_fifty_moves() or
            board.can_claim_threefold_repetition())


def drawScore(board):
    return not isDraw(board)


def mateScore(board):
    return 1000 if board.is_checkmate() else 0


def boardScore(board, color):
    score = 0
    for piece, value in [(chess.ROOK, 5), 
                         (chess.QUEEN, 9), 
                         (chess.BISHOP, 3), 
                         (chess.KNIGHT, 3), 
                         (chess.PAWN, 1), 
                         (chess.KING, 0)]:
        score += len(board.pieces(piece, color)) * value
        score -= len(board.pieces(piece, not color)) * value
        pass
    
    score += mateScore(board)   # Check mate score
    score *= drawScore(board)   # Neutralise for draw
    
    return score


def play_game(player1, player2, 
              fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
              scoreFunc=boardScore,
              visual="svg", pause=0.00001):
    """
    playerN1, player2: functions that takes board, return uci move
    visual: "simple" | "svg" | None
    Credit: https://bit.ly/3qImKaT
    """
    use_svg = (visual == "svg")
    board = chess.Board(fen=fen)
    try:
        while not board.is_game_over(claim_draw=True):
            if board.turn == chess.WHITE:
                uci = player1(board)
            else:
                uci = player2(board)
            name = who(board.turn)
            board.push_uci(uci)
            board_stop = display_board(board, use_svg)
            html = "<b>Move %s %s, Play '%s', Score: %s</b><br/>%s" % (
                       len(board.move_stack), name, uci, scoreFunc(board, board.turn), board_stop)
            if visual is not None:
                if visual == "svg":
                    clear_output(wait=True)
                display(HTML(html))
                if visual == "svg":
                    time.sleep(pause)
    except KeyboardInterrupt:
        msg = "Game interrupted!"
        return (None, msg, board)
    result = None
    if board.is_checkmate():
        msg = "checkmate: " + who(not board.turn) + " wins!"
        result = not board.turn
    elif board.is_stalemate():
        msg = "draw: stalemate"
    elif board.is_fivefold_repetition():
        msg = "draw: 5-fold repetition"
    elif board.is_insufficient_material():
        msg = "draw: insufficient material"
    elif board.can_claim_draw():
        msg = "draw: claim"
    if visual is not None:
        print(msg)
    return (result, msg, board, scoreFunc(board, board.turn))

