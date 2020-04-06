from tictactoe import *

board = initial_state()
board[0][0] = "X"
board[0][1] = "X"
board[0][2] = "X"
turn = player(board)
print(turn)
moves = actions(board)
print(moves)
# board = result(board,(0,2))
# print(board)
win = winner(board)
print(win)
print(utility(board))