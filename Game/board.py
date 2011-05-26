#variable declarations 
Player_X = 'X'
Player_O = 'O'
empty = ' '
empty_board = [empty, empty, empty,
               empty, empty, empty,
               empty, empty, empty]
winning_layouts = [[0, 1, 2], [3, 4, 5], [6, 7, 8], #horizontal
                   [0, 3, 6], [1, 4, 7], [2, 5, 8], #vertical
                   [0, 4, 8], [2, 4, 6]]            #diagonal


def doesGameHaveWinner(board):
    #returnes true or fase to see if any winning layout has been used
    for layout in winning_layouts:
        if board[layout[0]] == board[layout[1]] == board[layout[2]] != empty:
            return True
    return False

def validMovesLeft(board):
    #see's if any free cells exist in the board
    for cell in board:
        if cell == empty:
            return True
    return False

def isGameOver(board):
    #checks to see if the game has been one
    #check to see if all blocks have some content
    return doesGameHaveWinner(board) or  not validMovesLeft(board)

def validMoves(board):
    #returns a list of empty cells
    freecells = []
    for cell in range(0, 9):
        if board[cell] == empty:
            freecells.append(cell)
    return freecells

def create_computer_move(board):
    #checks to see if the center cell has been taken, if not takes it
    if board[4] == empty:
        return 4

    #gets the list of free moves
    freecells = validMoves(board)

    #iterates through each of the free cell and plays player_O to see if its a winning
    #if the cell does not work, it empties the cell
    for cell in freecells:
        board[cell] = Player_O
        if doesGameHaveWinner(board):
            return cell
        board[cell] = empty

    #iterates through each of the free cell and plays player_x to see if its a winning
    #if the cell does not work, it empties the cell
    #if the cell is a winning combination for the opponent do not allow it

    for cell in freecells:
        board[cell] = Player_X
        if doesGameHaveWinner(board):
            return cell
        board[cell] = empty

    #if not valid, do some slides on the board
    sides = [1, 3, 5, 7]
    for move in sides:
        if empty in board[move]:
            return move

    #try moving in the corner
    corners = [0, 2, 6, 8]
    for move in corners:
        if empty in board[move]:
            return move
