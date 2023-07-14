# Import Modules & Libraries
import chess, random, time
import display_gui as gui
import global_vars as G


# Select Random Move
def random_selection():
    move_list = list(G.BOARD.legal_moves)
    move_count = len(move_list)
    random_number = random.randint(0, move_count - 1)
    move = move_list[random_number]
    return move

# Get Game Status
def calc_game_status():
    if G.BOARD.is_checkmate():
        if G.BOARD.turn:
            return -9999
        else:
            return 9999
    elif G.BOARD.is_stalemate():
        return 0
    elif G.BOARD.is_repetition():
        return 0
    elif G.BOARD.is_insufficient_material():
        return 0
    elif G.BOARD.is_seventyfive_moves():
        return 0
    else:
        return "continue"
# Get Board Score
def calc_board_score():
    game_status = calc_game_status()
    if game_status != "continue":
        return game_status
    w_pawns = G.BOARD.pieces(chess.PAWN, chess.WHITE)
    w_rooks = G.BOARD.pieces(chess.ROOK, chess.WHITE)
    w_bishops = G.BOARD.pieces(chess.BISHOP, chess.WHITE)
    w_knights = G.BOARD.pieces(chess.KNIGHT, chess.WHITE)
    w_queens = G.BOARD.pieces(chess.QUEEN, chess.WHITE)
    w_kings = G.BOARD.pieces(chess.KING, chess.WHITE)

    b_pawns = G.BOARD.pieces(chess.PAWN, chess.BLACK)
    b_rooks = G.BOARD.pieces(chess.ROOK, chess.BLACK)
    b_bishops = G.BOARD.pieces(chess.BISHOP, chess.BLACK)
    b_knights = G.BOARD.pieces(chess.KNIGHT, chess.BLACK)
    b_queens = G.BOARD.pieces(chess.QUEEN, chess.BLACK)
    b_kings = G.BOARD.pieces(chess.KING, chess.BLACK)

    w_score_p = sum([G.pawn_score[p] for p in w_pawns])
    w_score_r = sum([G.rook_score[r] for r in w_rooks])
    w_score_b = sum([G.bishop_score[b] for b in w_bishops])
    w_score_n = sum([G.knight_score[n] for n in w_knights])
    w_score_q = sum([G.queen_score[q] for q in w_queens])
    w_score_k = sum([G.king_score[k] for k in w_kings])

    b_score_p = sum([-G.pawn_score[p] for p in b_pawns])
    b_score_r = sum([-G.rook_score[r] for r in b_rooks])
    b_score_b = sum([-G.bishop_score[b] for b in b_bishops])
    b_score_n = sum([-G.knight_score[n] for n in b_knights])
    b_score_q = sum([-G.queen_score[q] for q in b_queens])
    b_score_k = sum([-G.king_score[k] for k in b_kings])

    pawns = len(w_pawns) - len(b_pawns) #
    rooks = len(w_rooks) - len(b_rooks)
    bishops = len(w_bishops) - len(b_bishops)
    knights = len(w_knights) - len(b_knights)
    queens = len(w_queens) - len(b_queens)
    kings = len(w_kings) - len(b_kings)

    material = (pawns * 1) + (knights * 1.5) + (bishops * 29) + (rooks * 30) + (queens * 20000)
    final = material + \
            w_score_p + b_score_p + \
            w_score_r + b_score_r + \
            w_score_q + b_score_q + \
            w_score_b + b_score_b + \
            w_score_n + b_score_n + \
            w_score_k + b_score_k
    if G.BOARD.turn:
        return final
    else:
        return -final

# Select Positional Move
def select_positional():
    best_move = chess.Move.null
    best_score = -99999
    for move in G.BOARD.legal_moves:
        G.BOARD.push(move)
        score = -calc_board_score()
        G.BOARD.pop()
        if score > best_score:
            best_move = move
            best_score = score
    return best_move
# Negamax with Alpha-Beta Pruning
def negamax_ab(alpha, beta, depthleft):
    high_score = -99999
    if depthleft == 0:
        return calc_board_score()
    for move in G.BOARD.legal_moves:
        G.BOARD.push(move)
        score = -negamax_ab(-beta, -alpha, depthleft - 1)
        G.BOARD.pop()
        if score >= beta:
            return score
        if score > high_score:
            high_score = score
        if score > alpha:
            alpha = score
    return high_score

# Quiescence Search

# Select Predictive Move
def select_predictive(depthleft):
    alpha = -99999
    beta = 99999
    best_score = -99999
    best_move = chess.Move.null()
    for move in G.BOARD.legal_moves:
        G.BOARD.push(move)
        score = -negamax_ab(-beta, -alpha, depthleft - 1)
        G.BOARD.pop()
        if score > best_score:
            best_score = score
            best_move = move
        if score > alpha:
            alpha = score
    return best_move
# Complete AI Move
def make_ai_move(move, delay):
    time.sleep(delay)
    if move != chess.Move.null():
        gui.draw_board()
        gui.draw_select_square(move.from_square)
        gui.draw_select_square(move.to_square)
    gui.print_san(move)
    G.BOARD.push(move)
