# Strategize and make best move.
# If it's my first turn, don't bother with rest, what's the best first
# move for O and X?
# 1) Can I win? [Danger in my benefit]
# 2) Can human win? [Danger for human benefit, must block if so]
# 3) Can I fork?
# 4) What?
def bestMove(self):
    import random
    if self.numTurn == 1:
#            if self.aiMark == 'X':
#                return random.choice(list(self.corners))
        if self.aiMark == 'O':
            if self.center & self.availSquares:
                return list(self.center).pop()
                
    dangerousSquares = self.evalDanger()
    forkOpps = self.evalForkability()

#If I can win, take the first available winning box!
    if dangerousSquares[self.aiMark]:
        return dangerousSquares[self.aiMark][0]
#If I can't win but human can on his next turn, block the first danger!!
    elif dangerousSquares[self.humanMark]:
        return dangerousSquares[self.humanMark][0]
#Can I create a fork?
    elif forkOpps[self.aiMark]:
        return forkOpps[self.aiMark][0]

    elif self.numTurn == 2:
        if self.aiMark == 'O':
            #If both X's are in corners, we know O is in middle.  Take an edge
            if len(self.corners & self.xSquares) == 2:
                return random.choice(list(self.edges & self.availSquares))
        else:
            #ai is X
            if list(self.oSquares)[0] not in self.center :
                return 5
#Can I create a dangerous situation?

#Can my opponent create a fork on his next turn? If so, take one of his forks?
    if forkOpps[self.humanMark]:
        return forkOpps[self.humanMark][0]

#Do something else if none of the above
    else:
        return self.availSquares.pop()


