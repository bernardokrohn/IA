#import search
#mport utils


# board example
b1 = [["_","O","O","O","_"], ["O","_","O","_","O"], ["_","O","_","O","_"],["O","_","O","_","_"], ["_","O","_","_","_"]]

#TAI content

def c_peg():
    return "O"
def c_empty():
    return "_"
def c_blocked():
    return "X"
def is_empty(e):
    return e == c_empty()
def is_peg(e):
    return e == c_peg()
def is_blocked(e):
    return e == c_empty()

# TAI pos
# Tuplo (l, c)
def make_pos(l, c):
    return (l, c)
def pos_l(pos):
    return pos[0]
def pos_c(pos):
    return pos[1] 

 # TAI move
# Lista [p_initial, p_final]
def make_move(i, f):
    return [i, f]
def move_initial(move):
    return move[0]
def move_final(move):
    return move[1] 

def board_moves(board):

    """
    Returns a list with all valid moves possible
    on the passed board
    """

    board_size = len(board)
    moves = []

    for i in range(0, board_size):

        for j in range(0, board_size):

            if is_empty(board[i][j]):

                if i > 1 and is_peg(board[i - 1][j]) and is_peg(board[i - 2][j]):
                
                    moves.append(make_move(make_pos(i - 2, j), make_pos(i, j)))
                
                if i < board_size - 2 and is_peg(board[i + 1][j]) and is_peg(board[i + 2][j]):
                
                    moves.append(make_move(make_pos(i + 2, j), make_pos(i, j)))
                
                if j < board_size - 2 and is_peg(board[i][j + 1]) and is_peg(board[i][j + 2]):
                
                    moves.append(make_move(make_pos(i, j + 2), make_pos(i, j)))
                
                if j > 1 and is_peg(board[i][j - 1]) and is_peg(board[i][j - 2]):
                
                    moves.append(make_move(make_pos(i, j - 2), make_pos(i, j)))
    return moves




print(board_moves(b1))








