# Portando um antigo codigo em Pascal de jogo da velha feito ainda na faculdade para Python
# Porting an old code I've done in Pascal during the college time.
# Jogo da Velha is the Brazilian name for Tic Tac Toe. [Programming and learning, it's all culture! :-)]

import random

def equals(list):
    #print "retorna vazio se todos os elementos de uma lista sao iguais ou se a lista eh igual a Vazio."
    return not list or list == [list[0]] * len(list)
    
Nobody = '.'
Player_X = 'x'
Player_O = 'o'

class Board:
    #print "Classe representando o Board."""
    def __init__(self):
        #print "Zerando o Board."
        self.places = [Nobody]*9
        self.freePlaces = '123456789'

    def showBoard(self):
        #print "Show the board on the screen."
        for line in [self.places[0:3], self.places[3:6], self.places[6:9]]:
            print ' '.join(line)
    
    def doMove(self, place, player):
       #print "Do a move."
        self.places[place] = player

    def undoMove(self, casa):
        #print "Undo a move."
        self.doMove(casa, Nobody)
    
    def getFreePlaces(self):
        #print "Return a list of available places to move."
        return [pos for pos in range(9) if self.places[pos] == Nobody]

    def getPlace(self, casa):
        #print "Return the number os the free places."
        return self.freePlaces[casa]

    def winner(self):
        #print "Tells if someone won the game, Player_X, Player_O or Nobody"
        winMoves = [[0,1,2],[3,4,5],[6,7,8],        # vertical
                        [0,3,6],[1,4,7],[2,5,8],    # horizontal
                        [0,4,8],[2,4,6]]            # diagonal
        for row in winMoves:
            if self.places[row[0]] != Nobody and equals([self.places[i] for i in row]):
                return self.places[row[0]]

    def endGame(self):
        #Print "Indica se o jogo acabou, se alguem ganhou ou fim das jogadas."
        return self.winner() or not self.getFreePlaces()


def player(Board, player):
    #print "Funcao do player."
    Board.showBoard()
    freePlaces = dict([(Board.getPlace(move), move) for move in Board.getFreePlaces()])
    move = raw_input("What's your move (%s)? " % (', '.join(sorted(freePlaces))))
    while move not in freePlaces:
        print "The move, '%s' is invalid. Try again." % move
        move = raw_input("What's your move (%s)? " % (', '.join(sorted(freePlaces))))
    Board.doMove(freePlaces[move], player)
    
def computer(Board, player):
    #print "Funcao para o computador"
    Board.showBoard()
    opponent = { Player_O : Player_X, Player_X : Player_O }

    def getWinner(winner):
        if winner == player:
            return +1
        if winner == None:
            return 0
        return -1

    #print "Aqui o computador avalia as possiveis jogadas para a tomada de decisao."
    def evaluateMove(move, p=player):
        #print "Entrando na funcao de avaliar a jogada."
        try:
            Board.doMove(move, p)
            if Board.endGame():
                return getWinner(Board.winner())
            results = (evaluateMove(next_move, opponent[p]) for next_move in Board.getFreePlaces())

            if p == player:
                #print "p = player"
                return min(results)
            else:
                #print "p <> player"
                return max(results)

        finally:
            Board.undoMove(move)

    moves = [(move, evaluateMove(move)) for move in Board.getFreePlaces()]
    random.shuffle(moves)
    moves.sort(key = lambda (move, winner): winner)
    #print moves
    #print "Checkpoint 1!"
    Board.doMove(moves[-1][0], player)
    
def game():
    #print "Rodando o jogo"
    b = Board()
    turn = 1
    while True:
        print "Move %i." % turn
        player(b, Player_O)
        if b.endGame(): 
            break
        computer(b, Player_X)
        if b.endGame(): 
            break
        turn += 1

    b.showBoard()
    if b.winner():
        print 'Player "%s" wins' % b.winner()
    else:
        print 'Nobody won.'
    
if __name__ == "__main__":
    game()