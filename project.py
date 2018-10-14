from search import Problem
from search import depth_first_tree_search
from search import depth_first_graph_search

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

#TAI board



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

#print(board_moves(b1))


def board_perform_move(board, move):

    """
    Performs the given move on the board 
    returning the resulting board
    """

    new_board = [i[:] for i in board]
    f = move_final(move)
    i = move_initial(move)
    f_l = pos_l(f)
    i_l = pos_l(i)
    f_c = pos_c(f)
    i_c = pos_c(i)

    if f_l == i_l:

        m_l = f_l
        m_c = (f_c + 1) if i_c > f_c else (i_c + 1)
    
    elif f_c == i_c:
        
        m_c = f_c
        m_l = (f_l + 1) if i_l > f_l else (i_l + 1)

    new_board[i_l][i_c] = c_empty()
    new_board[m_l][m_c] = c_empty()
    new_board[f_l][f_c] = c_peg()

    return new_board


class sol_state:

    def __init__(self, board):
       
        self.board = board

    def peg_number(self):
        
        """
        Returns the number of pegs on the saved board
        """
        number = 0

        for lines in self.board:
            for c in lines:
                if is_peg(c):
                    number += 1
        
        return number


class solitaire(Problem):

    """Models a Solitaire problem as a satisfaction problem.
    A solution cannot have more than 1 peg left on the board.
    """
    
    def __init__(self, board):
        self.board = board
        self.initial = sol_state(board)

    def actions(self, state):

        """
        Returns the list of board moves performable on the board
        of the given state
        """

        return board_moves(state.board)

    def result(self, state, action):
        
        """
        Returns the resulting state from performing the given move
        on the given state
        """

        b = board_perform_move(state.board, action)
        return sol_state(b)
 
    def goal_test(self, state):
        
        """
        Returns whether there is exactly 1 peg left on the board
        on the given state
        """

        return state.peg_number() == 1

    #def path_cost(self, c, state1, action, state2):
    
    #def h(self, node):
    #    """
    #    Needed for informed search.
    #    """


problem = solitaire(b1)

n1 = depth_first_graph_search(problem)
s1 = n1.state
print(s1.board)

n2 = depth_first_tree_search(problem)
s2 = n2.state
print(s2.board)





