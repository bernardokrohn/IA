from search import *

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

    moves = []
    board_height = len(board)
    board_width = len(board[0])

    for i in range(board_height):
        for j in range(board_width):
            if is_peg(board[i][j]):
                if j > 1 and is_peg(board[i][j - 1]) and is_empty(board[i][j - 2]):
                
                    moves.append(make_move(make_pos(i, j), make_pos(i, j - 2)))
                
                if i > 1 and is_peg(board[i - 1][j]) and is_empty(board[i - 2][j]):
                
                    moves.append(make_move(make_pos(i, j), make_pos(i - 2, j)))

                if j < board_width - 2 and is_peg(board[i][j + 1]) and is_empty(board[i][j + 2]):
                
                    moves.append(make_move(make_pos(i, j), make_pos(i, j + 2)))
               
                if i < board_height - 2 and is_peg(board[i + 1][j]) and is_empty(board[i + 2][j]):
                
                    moves.append(make_move(make_pos(i, j), make_pos(i + 2, j)))
                        
    return moves


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


def board_value(board, board_moves):

    """
    Examines the given board for number of pegs, empty spaces
    number of pegs with no neighbours and number of corner placed pegs
    """
    
    pegs = 0
    empty = 0
    corner = 0
    solo_pegs = 0
    board_height = len(board)
    board_width = len(board[0])
    no_play_pegs = 0
    dispersion = 0

    if is_peg(board[0][0]):
        corner += 1
    if is_peg(board[0][board_width-1]):
        corner += 1
    if is_peg(board[board_height-1][0]):
        corner += 1
    if is_peg(board[board_height-1][board_width-1]):
        corner += 1

    for i in range(board_height):
        for j in range(board_width):
            if is_peg(board[i][j]):
                pegs += 1
                is_play = 1
                for m in board_moves:
                    if (i,j) in m:
                        is_play = 0
                        break;

                if (i > 0 and not(is_peg(board[i-1][j])) and
                    j > 0 and not(is_peg(board[i][j-1])) and
                    i < board_height - 1 and not(is_peg(board[i+1][j])) and
                    j < board_width - 1 and not(is_peg(board[i][j+1]))):

                    solo_pegs += 1
                no_play_pegs += is_play 

                for ii in range(board_height):
                    for jj in range(board_width):
                        if is_peg(board[ii][jj]):
                            dispersion += abs(ii - i) + abs(jj -j)   
                            
            elif is_empty(board[i][j]):
                empty += 1
            
    return (pegs, empty, corner, solo_pegs, no_play_pegs, dispersion/pegs)


class sol_state:

    def __init__(self, board):
        self.board = board 
        self.board_moves = board_moves(board)
        b = board_value(board, self.board_moves)
        self.peg_number = b[0]
        self.value =  b[4] + b[5]

    def __lt__(self, other):
        return self.peg_number >  other.peg_number


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
        
        return state.board_moves

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

    def path_cost(self, c, state1, action, state2):
        return c + 1
    
    def h(self, node):
        
        """
        Needed for informed search.
        """
        
        s = node.state
        return s.value
