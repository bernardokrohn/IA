from search import *

# board example
b5x5 = [["_","O","O","O","_"],
        ["O","_","O","_","O"],
        ["_","O","_","O","_"],
        ["O","_","O","_","_"],
        ["_","O","_","_","_"]]

b4x4 = [["O","O","O","X"],
        ["O","O","O","O"],
        ["O","_","O","O"],
        ["O","O","O","O"]]

b4x5 = [["O","O","O","X","X"],
        ["O","O","O","O","O"],
        ["O","_","O","_","O"],
        ["O","O","O","O","O"]]

b4x6 = [["O","O","O","X","X","X"],
        ["O","_","O","O","O","O"],
        ["O","O","O","O","O","O"],
        ["O","O","O","O","O","O"]]


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

    moves = []
    board_height = len(board)
    board_width = len(board[0])

    if board_height > 0 :
        for i in range(board_height):
            if board_width > 0:
                for j in range(board_width):

                    if is_peg(board[i][j]):

                        if j > 1 and is_peg(board[i][j - 1]) and is_empty(board[i][j - 2]):
                        
                            moves.append(make_move(make_pos(i, j), make_pos(i, j - 2)))

                        if i > 1 and is_peg(board[i - 1][j]) and is_empty(board[i - 2][j]):
                        
                            moves.append(make_move(make_pos(i, j), make_pos(i - 2, j)))
                        
                        if i < board_height - 2 and is_peg(board[i + 1][j]) and is_empty(board[i + 2][j]):
                        
                            moves.append(make_move(make_pos(i, j), make_pos(i + 2, j)))
                        
                        if j < board_width - 2 and is_peg(board[i][j + 1]) and is_empty(board[i][j + 2]):
                        
                            moves.append(make_move(make_pos(i, j), make_pos(i, j + 2)))
                        
    return moves

#print(board_moves(b1))


def board_perform_move(board, move):

    """
    Performs the given move on the board 
    returning the resulting board
    """

    new_board = [i[:] for i in board]
    #new_board = copy.deepcopy(board)
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


def peg_number(board):
    
    number = 0

    for lines in board:
        for c in lines:
            if is_peg(c):
                number += 1
    return number

def board_dispersion(board):

    dispersion = 0
    peg_number = 0

    board_height = len(board)
    board_width = len(board[0])

    for i in range(board_height):
        for j in range(board_width):
            if is_peg(board[i][j]):
                peg_number += 1
                for ii in range(board_height):
                    for jj in range(board_width):
                        if is_peg(board[ii][jj]):
                            dispersion += abs(ii - i) + abs(jj -j)
    return dispersion/peg_number


class sol_state:

    def __init__(self, board):
        self.board = board
        self.peg_number = peg_number(board)
        self.moves = board_moves(board)
        self.board_dispersion = board_dispersion(board)

    def __lt__(self, other):
        return self.board_dispersion > other.board_dispersion



class solitaire(Problem):

    """Models a Solitaire problem as a satisfaction problem.
    A solution cannot have more than 1 peg left on the board.
    """
    
    def __init__(self, board):
        self.initial = sol_state(board)

    def actions(self, state):

        """
        Returns the list of board moves performable on the board
        of the given state
        """

        return state.moves

    def result(self, state, action):
        
        """
        Returns the resulting state from performing the given move
        on the given state
        """

        b = board_perform_move(state.board, action)
        s = sol_state(b) 
        return s
 
    def goal_test(self, state):
        
        """
        Returns whether there is exactly 1 peg left on the board
        on the given state
        """

        return state.peg_number == 1

   # def path_cost(self, c, state1, action, state2):

    
    def h(self, node):
        
        """
        Needed for informed search.
        """
        
        s = node.state
        return board_dispersion(s.board)


problem = solitaire(b4x5)
"""
n1 = breadth_first_tree_search(problem)
s1 = n1.state
print(s1.board)

n2 = breadth_first_search(problem)
s2 = n2.state
print(s2.board)

n3 = depth_first_graph_search(problem)
s3 = n3.state
print(s3.board)

n4 = iterative_deepening_search(problem)
s4 = n4.state
print(s4.board)

n5 = depth_limited_search(problem)
s5 = n5.state
print(s5.board)

n6 = recursive_best_first_search(problem)
s6 = n6.state
print(s6.board)
"""
compare_searchers([problem], ['Searcher', 'solitaire'])

"""
def greedy_search(problem, h=None):

    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, h)

n7 = greedy_search(problem)
s7 = n7.state
print(s7.board)
"""

