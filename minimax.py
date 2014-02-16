"""
implementation of the minimax algorithm (http://en.wikipedia.org/wiki/Minimax) for tic-tac-toe purposes
"""

class MinimaxCalculator:

    def __init__(self, moveCache={}):
        """
        moveCache is dict-like key-value store of moves and results
        """
        self.moveCache = moveCache

    def bestMove(self, player, board):
        """
        returns best move calculated by minimax
        move is tuple in form of (x, y)
        player is assumed to be either 'X' or 'O'
        """
        return self.minimax(player, board)[0]

    def minimax(self, player, board):
        """
        returns maximized move for player.
        player is assumed to be either 'X' or 'O'
        return value is tuple in form of (<move>, <score>)
        move is a tuple in form of (x, y)
        """
        cacheEntry = self.moveCache.get(board.boardHash(), None)
        if cacheEntry != None:
            playerMove = cacheEntry.get(player, None)
            if playerMove != None:
                return playerMove['move'], playerMove['score']
        bestScore = None
        bestMove = None
        for square in board.getEmptySquares():
            board.move(player, square[0], square[1])
            moveResult = board.finished()
            if moveResult[0]:
                if moveResult[1] == player:
                    score = 1
                elif moveResult[1] == None:
                    score = 0
                else:
                    score = -1
                adjustedScore = score
            else:
                opponentPlayer = 'O' if player=='X' else 'X'
                opponentMove, score = self.minimax(opponentPlayer, board)
                score *= -1
                if score > 0:
                    adjustedScore = 0.5#prefer winning now to winning later
                else:
                    adjustedScore = score
            if bestScore == None or adjustedScore > bestScore:
                bestScore = adjustedScore
                bestMove = square
            board.move(board.emptyMarker, square[0], square[1])#undoes last move
        cacheAddition = {'move':bestMove,'score':bestScore}
        if cacheEntry != None:
            cacheEntry[player] = cacheAddition
            self.moveCache[board.boardHash()] = cacheEntry
        else:
            self.moveCache[board.boardHash()] = {player: cacheAddition}
        return bestMove, bestScore

