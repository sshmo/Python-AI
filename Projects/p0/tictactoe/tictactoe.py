"""
Tic Tac Toe Player
"""
from random import randint
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
    n_o = 0
    n_x = 0
    for i in board:
        for j in i:
            if j == O:
                n_o += 1
            elif j == X:
                n_x += 1
    if n_o == n_x:
        return X
    if n_o == n_x - 1:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == None:
                actions.add((i, j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    temp = copy.deepcopy(board)
    if temp[action[0]][action[1]] != None:
        raise "O! O!"
    temp[action[0]][action[1]] = player(board)
    return temp


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if (board[0][0] == board[0][1] == board[0][2]
            or board[0][0] == board[1][1] == board[2][2]
            or board[0][0] == board[1][0] == board[2][0]):
        return board[0][0]
    if (board[1][0] == board[1][1] == board[1][2]
            or board[0][2] == board[1][1] == board[2][0]
            or board[0][1] == board[1][1] == board[2][1]):
        return board[1][1]
    if (board[2][0] == board[2][1] == board[2][2]
            or board[0][2] == board[1][2] == board[2][2]):
        return board[2][2]


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == None:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        if winner(board) == X:
            return 1
        if winner(board) == O:
            return -1
        return 0


def Max_v(board):
    """Finds Max of the Min player rezults"""
    v = -2
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = max(v, Min_v(result(board, action)))
    return v


def Min_v(board):
    """Finds Min of the Max player rezults"""
    v = 2
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = min(v, Max_v(result(board, action)))
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    outcome = []
    act = []
    if player(board) == O:
        for action in actions(board):
            outcome.append(Max_v(result(board, action)))
            act.append(action)
        return act[argmin(outcome)]
    if player(board) == X:
        if board == initial_state():
            return (randint(0, 2), randint(0, 2))
        for action in actions(board):
            outcome.append(Min_v(result(board, action)))
            act.append(action)
        return act[argmax(outcome)]


def argmax(iterable):
    """A function to finde argmax of any iterable"""
    return max(enumerate(iterable), key=lambda x: x[1])[0]


def argmin(iterable):
    """A function to finde argmin of any iterable"""
    return min(enumerate(iterable), key=lambda x: x[1])[0]  