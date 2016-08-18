import tttboard
"""
Mini-max Tic-Tac-Toe Player
"""

# SCORING VALUES - DO NOT MODIFY
SCORES = {tttboard.PLAYERX: 1,
          tttboard.DRAW: 0,
          tttboard.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    winner = board.check_win()
    if winner:
        return SCORES[winner], (-1, -1)
    empty_squares = board.get_empty_squares()
    moves = []
    for square in empty_squares:
        board_clone = board.clone()
        board_clone.move(square[0],square[1], player)
        winner = board_clone.check_win()
        if winner :
            return SCORES[winner], square             
        move = mm_move(board_clone, tttboard.switch_player(player))
        if move[0] * SCORES[player] == 1:
            return move[0], square
        moves.append((move[0]* SCORES[player],square))    
    move = max(moves)
    move = move[0]* SCORES[player], move[1]
    return move

def mm_move_wrapper(board, player):
    """
    wrapper for ai function
    """
    score, move = mm_move(board, player)
    return move

###############
#Test Function#
###############
def play_game(mm_move_function, reverse = False):
    """
    Function to play a game with two mini-max players.
    """
    # Setup game
    board = tttboard.TTTBoard(3, reverse)
    curplayer = tttboard.PLAYERX
    winner = None
    
    # Run game
    while winner == None:
        # Move
        score, move = mm_move_function(board, curplayer)
        row, col = move#if type(col) == tuple:
         #   row, col = col
        print row,col
        board.move(row, col, curplayer)

        # Update state
        winner = board.check_win()
        curplayer = tttboard.switch_player(curplayer)

        # Display board
        print board
        print
        
    # Print winner
    if winner == tttboard.PLAYERX:
        print "X wins!"
    elif winner == tttboard.PLAYERO:
        print "O wins!"
    elif winner == tttboard.DRAW:
        print "Tie!"
    else:
        print "Error: unknown winner"

