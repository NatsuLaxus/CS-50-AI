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
    Returns player who has the NotImplementedErrorxt turn on a board.
    """
    count = 0
    turn = "X"
    for i in range(3):
        for j in range(3):
            if(board[i][j] == EMPTY):
                count = count+1
    if(count%2 == 0):
        turn = "O"
    return turn
    # raise NotImplementedError

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = []
    for i in range(3):
        for j in range(3):
            if(board[i][j] == EMPTY):
                moves.append((i,j))
    return moves
    # raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    temp_board = copy.deepcopy(board)
    turn = player(board)
    # print(action)
    temp_board[action[0]][action[1]] = turn
    return temp_board
    # raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winner = None
    for i in range(3):
        count1 = 0
        count2 = 0
        count3 = 0
        count4 = 0
        for j in range(3):
            if(board[i][j] == "X"):
                count1 = count1+1
            if(board[j][i] == "X"):
                count2 = count2+1
            if(board[i][j] == "O"):
                count3 = count3+1
            if(board[j][i] == "O"):
                count4 = count4+1
        if(count1 == 3):
            winner = "X"
        elif(count2 == 3):
            winner = "X"
        elif(count3 == 3):
            winner = "O"
        elif(count4 == 3):
            winner = "O"
    if(board[0][0] == "X" and board[1][1] == "X" and board[2][2] == "X"):
        winner = "X"
    elif(board[0][2] == "X" and board[1][1] == "X" and board[2][0] == "X"):
        winner = "X"
    elif(board[0][0] == "O" and board[1][1] == "O" and board[2][2] == "O"):
        winner = "O"
    elif(board[0][2] == "O" and board[1][1] == "O" and board[2][0] == "O"):
        winner = "O"
    return winner
    # raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    count = 0
    for i in range(3):
        for j in range(3):
            if(board[i][j] != EMPTY):
                count = count+1
    if(count == 9):
        return True
    if(winner(board) != None):
        return True
    return False
    # raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if(winner(board) == "X"):
        return 1
    if(winner(board) == "O"):
        return -1
    return 0
    # raise NotImplementedError


def minimax(board):
    s,ans = minimaxUtil(board)
    return ans
    # raise NotImplementedError


def minimaxUtil(board):
    moves = actions(board)
    if winner(board) == "X":
        return (1,(-1,-1))
    if winner(board) == "O":
        return (-1,(-1,-1))
    if len(moves) == 0:
        return (0,(-1,-1))  
    turn = player(board)
    ans = ()
    m = ()
    if turn == "X":
        initial_score = -2
        current = -2
        for move in moves:
            board = result(board,move)
            score,m = minimaxUtil(board)
            current = max(score,current)
            if current > initial_score :
                initial_score = current
                ans = (move[0],move[1])
            board[move[0]][move[1]] = EMPTY

    else:
        initial_score = 2
        current = 2
        for move in moves:
            board = result(board,move)
            score,m = minimaxUtil(board)
            current = min(score,current)
            if current < initial_score :
                initial_score = current
                ans = (move[0],move[1])
            board[move[0]][move[1]] = EMPTY
    return score, ans