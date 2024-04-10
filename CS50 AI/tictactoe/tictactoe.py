"""
Tic Tac Toe Player
"""

import math
import copy


X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    # The player function should take a board state as input, and return which player’s turn it is (either X or O).
    # In the initial game state, X gets the first move. Subsequently, the player alternates with each additional move.
    # Any return value is acceptable if a terminal board is provided as input (i.e., the game is already over).

    Xcounter = 0
    Ocounter = 0
    for list in board:
        for item in list:
            if item == X:
                Xcounter += 1
            if item == O:
                Ocounter += 1
    if Xcounter > Ocounter:
        return O
    elif Xcounter == 0:
        return X
    elif Xcounter == Ocounter:
        return X
    else:
        return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    #The actions function should return a set of all of the possible actions that can be taken on a given board.
    #Each action should be represented as a tuple (i, j) where i corresponds to the row of the move (0, 1, or 2)
    # and j corresponds to which cell in the row corresponds to the move (also 0, 1, or 2).
    #Possible moves are any cells on the board that do not already have an X or an O in them.
    # Any return value is acceptable if a terminal board is provided as input.
    moves = set()
    row = -1
    for list in board:
        row += 1
        colum = -1
        for item in list:
            colum += 1
            if item == None:
                moves.add(tuple([row, colum]))
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("This action is not in the list of possible actions!")

    copy_board = copy.deepcopy(board)
    i = action[0]
    j = action[1]
    if copy_board[i][j] == None:
        copy_board[i][j] = player(board)
    return copy_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    #defining the winner - last person to play
    if player(board) == X:
        winner = O
    else:
        winner = X

    # checking the rows
    for sublist in board:
        resultO = all(i == O for i in sublist)
        resultX = all(i == X for i in sublist)
        if (resultX) or (resultO):
            return winner
    #checking the columns
    for column in range(3):
        if (board[0][column] == board[1][column] == board[2][column]) and (board[0][column] != None):
            return winner

    # back slash diag
    if (board[0][0] == board[1][1] == board[2][2]) and (board[2][2] != None):
        return winner

    # front slash diag
    if (board[0][2] == board[1][1] == board[2][0]) and (board[2][0] != None):
        return winner

    #if it has reached this far, no one has won, and return None - a tie game
    return None



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    #checking if there's a winner
    if winner(board) != None:
        return True

    #so no winners, but is there a free space?
    for list in board:
        for item in list:
            if item == None:
                return False

    #so no winners and no free spaces, the game is over - a tie game
    return True



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """


    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    #The minimax function should take a board as input, and return the optimal move for the player to move on that board.
    #The move returned should be the optimal action (i, j) that is one of the allowable actions on the board.
    # If multiple moves are equally optimal, any of those moves is acceptable.

    if terminal(board):
        return None

    if player(board) == X:
        pos_moves = []
        for action in actions(board):
            pos_moves.append([min_value(result(board, action), -math.inf, math.inf), action])
        return sorted(pos_moves, key=lambda x:x[0], reverse=True)[0][1]

    elif player(board) == O:
        pos_moves = []
        for action in actions(board):
            pos_moves.append([max_value(result(board, action), -math.inf, math.inf), action])
        return sorted(pos_moves, key=lambda x:x[0])[0][1]

#max value function - with alpha beta pruning
def max_value(state, alpha, beta):
    if terminal(state):
        return utility(state)

    v = float('-inf')
    for action in actions(state):
        v = max(v, min_value(result(state, action), alpha, beta))
        alpha = max(alpha, v)
        if alpha > beta:
            break
    return v

#max value function - with alpha beta pruning
def min_value(state, alpha, beta):
    if terminal(state) == True:
        return utility(state)
    v = float('inf')
    for action in actions(state):
        v = min(v, max_value(result(state, action), alpha, beta))
        beta = min(beta, v)
        if alpha > beta:
            break
    return v

